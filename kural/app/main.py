"""Kural — the business brain (FastAPI) + the Tailwind dashboard at /.

Endpoints:
  GET  /                     the ops dashboard (web/index.html)
  POST /grievance            structured contract the Bolna voice agent calls on confirm
  POST /intake               TEXT demo mode: raw Tanglish utterance -> classify -> file
  GET  /ticket/{id}          one ticket + its reporters + escalation level
  POST /ticket/{id}/resolve  close a ticket
  GET  /api/escalations      breached-open tickets with ward->commissioner level
  POST /call-webhook         Bolna post-call webhook -> store call + KuralEval
  GET  /api/tickets  /api/stats  /api/evals   dashboard data
  GET  /health
"""

from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from . import db, sla, nlu
from .eval import run_eval
from .routing import resolve
from .service import file_grievance, cluster_key
from .models import (GrievanceIn, GrievanceOut, ClassifyIn, FlatGrievanceIn,
                     Extracted, Caller, Locality)

load_dotenv()
app = FastAPI(title="Kural — civic grievance brain", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@app.on_event("startup")
def _startup():
    db.init_db()
    try:
        _seed_if_empty()
    except Exception as e:            # noqa: BLE001
        print(f"[seed] {e}")


def _seed_if_empty():
    """Keep the dashboard populated after a free-host restart (SQLite is ephemeral)."""
    conn = db.get_conn()
    try:
        n = conn.execute("SELECT COUNT(*) AS c FROM tickets").fetchone()["c"]
    finally:
        conn.close()
    if n:
        return
    demos = [
        ("electricity", "Kuniyamuthur Coimbatore", "urban", "high", "Senthil", "+919000000007",
         "200 units use pannen aana bill 2000 vandhuchu", {"units_used": 200, "amount_charged": 2000}),
        ("water_supply", "Anna Nagar West Chennai", "chennai", "high", "Kumar", "+910001", None, None),
        ("water_supply", "Anna Nagar West Chennai", "chennai", "high", "Devi", "+910002", None, None),
        ("water_supply", "Anna Nagar West Chennai", "chennai", "medium", "Fathima", "+910003", None, None),
        ("streetlight", "Adyar Chennai", "chennai", "high", "Ravi", "+910004", None, None),
        ("solid_waste", "Madurai", "urban", "medium", "Lakshmi", "+910005", None, None),
        ("roads_internal", "Thanjavur", "urban", "medium", "Mani", "+910006", None, None),
        ("solid_waste", "Salem", "urban", "medium", "Raja", "+910008", None, None),
    ]
    for sec, loc, reg, sev, nm, ph, utt, bill in demos:
        file_grievance(Extracted(sector=sec, severity=sev,
                                 locality=Locality(text=loc, region=reg)),
                       Caller(name=nm, phone=ph, raw_address=loc), utterance=utt, billing=bill)


@app.get("/")
def home():
    """Serve the Tailwind ops dashboard at the API origin — no CORS, no build."""
    return FileResponse(WEB_DIR / "index.html")


@app.get("/tn_districts.json")
def tn_districts():
    """Real Tamil Nadu district geometry (projected SVG paths) for the map background."""
    return FileResponse(WEB_DIR / "tn_districts.json")


@app.get("/health")
def health():
    return {"ok": True, "service": "kural-brain"}


@app.post("/grievance", response_model=GrievanceOut)
def grievance(payload: GrievanceIn):
    """Called by the Bolna voice agent (tool/custom-function) after the caller confirms."""
    billing = payload.billing.model_dump() if payload.billing else None
    return file_grievance(payload.extracted, payload.caller,
                          payload.call_id, payload.utterance, billing=billing)


@app.post("/intake", response_model=GrievanceOut)
def intake(payload: ClassifyIn):
    """TEXT demo mode: classify a raw Tanglish sentence, then file it — no telephony."""
    c = nlu.classify(payload.utterance)
    extracted = Extracted(sector=c.get("sector", "other"),
                          severity=c.get("severity", "medium"),
                          locality=Locality(text=c.get("locality"), region=c.get("region")))
    return file_grievance(extracted, payload.caller, None, payload.utterance)


def _clean(x):
    """Strip whitespace; treat empty or an unsubstituted '%(name)s' template as blank."""
    x = (x or "").strip()
    return "" if (x == "" or x.startswith("%(")) else x


def _num(x):
    x = _clean(x)
    try:
        return float(x) if x else None
    except ValueError:
        return None


@app.api_route("/file", methods=["GET", "POST"])
def file_flat(sector: str = "other", locality: str = "", region: str = "",
              severity: str = "medium", name: str = "", phone: str = "",
              call_id: str = "", utterance: str = "",
              units: str | None = None, charged: str | None = None,
              expected: str | None = None):
    """Flat-params entry for Bolna's custom_task tool (templates %(name)s into a URL).
    Robust to empty / unsubstituted billing params. For electricity bill disputes pass
    units/charged/(expected) -> the brain computes the over-charge + anomaly."""
    sector = _clean(sector) or "other"
    severity = _clean(severity) or "medium"
    locality, region = _clean(locality), _clean(region)
    name, phone, utterance = _clean(name), _clean(phone), _clean(utterance)
    u, c, e = _num(units), _num(charged), _num(expected)

    extracted = Extracted(sector=sector, severity=severity,
                          locality=Locality(text=locality or None, region=region or None))
    caller = Caller(name=name or None, phone=phone or None, raw_address=locality or None)
    billing = {"units_used": u, "amount_charged": c, "expected_amount": e} if (u or c) else None
    return file_grievance(extracted, caller, _clean(call_id) or None,
                          utterance or locality or None, billing=billing)


@app.post("/v1/grievance", response_model=GrievanceOut)
def grievance_flat(p: FlatGrievanceIn):
    """PII-safe flat JSON body for Bolna's custom_task POST -> file_grievance (no PII in the URL)."""
    sector = _clean(p.sector) or "other"
    severity = _clean(p.severity) or "medium"
    locality, region = _clean(p.locality), _clean(p.region)
    name, phone, utterance = _clean(p.name), _clean(p.phone), _clean(p.utterance)
    u, c, e = _num(p.units), _num(p.charged), _num(p.expected)
    extracted = Extracted(sector=sector, severity=severity,
                          locality=Locality(text=locality or None, region=region or None))
    caller = Caller(name=name or None, phone=phone or None, raw_address=locality or None)
    billing = {"units_used": u, "amount_charged": c, "expected_amount": e} if (u or c) else None
    return file_grievance(extracted, caller, _clean(p.call_id) or None,
                          utterance or locality or None, billing=billing)


@app.get("/area-status")
def area_status(locality: str = "", sector: str = "other"):
    """Agent tool: how many open reports already exist for this issue+area (dedup/hotspot).
    Lets the agent say 'already N reported — you're the next, idhu priority-ku pogum'."""
    r = resolve(sector, locality_text=locality)
    ck = cluster_key(r.owning_body, r.region, r.sector, locality)
    conn = db.get_conn()
    try:
        row = db.open_duplicate_ticket(conn, ck)
        count = row.get("reporter_count", 0) if row else 0
        return {"locality": locality, "sector": r.sector, "owning_body": r.owning_body,
                "existing_reports": count, "hotspot": count >= 3,
                "ticket_id": row["id"] if row else None}
    finally:
        conn.close()


@app.get("/ticket-status/{ticket_id}")
def ticket_status(ticket_id: str):
    """Agent tool: a returning caller gives their ticket number and hears the status."""
    conn = db.get_conn()
    try:
        t = db.get_ticket(conn, ticket_id)
        if not t:
            return {"found": False,
                    "spoken": f"Ticket {ticket_id} kedaikala. Number sariya sollunga."}
        breached = t["status"] == "open" and t["due_at"] < db.now_iso()
        spoken = (f"Ticket {ticket_id}: {t['owning_body']}-la status '{t['status']}'. "
                  + ("SLA over aayiduchu, escalate aagudhu." if breached
                     else "SLA kulla iruku, work nadakudhu."))
        return {"found": True, "ticket_id": ticket_id, "status": t["status"],
                "owning_body": t["owning_body"], "due_at": t["due_at"],
                "breached": breached, "spoken": spoken}
    finally:
        conn.close()


@app.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: str):
    conn = db.get_conn()
    try:
        t = db.get_ticket(conn, ticket_id)
        if not t:
            raise HTTPException(404, "ticket not found")
        t["reporters"] = db.get_reporters(conn, ticket_id)
        t["escalation_level"] = sla.escalation_level(t["due_at"], t.get("reporter_count", 1))
        return t
    finally:
        conn.close()


@app.post("/ticket/{ticket_id}/resolve")
def resolve_ticket_route(ticket_id: str):
    conn = db.get_conn()
    try:
        ok = db.resolve_ticket(conn, ticket_id)
        conn.commit()
        if not ok:
            raise HTTPException(404, "ticket not found or already resolved")
        return {"ok": True, "ticket_id": ticket_id, "status": "resolved"}
    finally:
        conn.close()


@app.get("/api/escalations")
def api_escalations():
    """Breached-open tickets with their current escalation rung (hotspots jump a tier)."""
    conn = db.get_conn()
    try:
        out = []
        for t in db.breached_open(conn):
            out.append({
                "ticket_id": t["id"], "owning_body": t["owning_body"],
                "department": t["department"], "sector": t["sector"],
                "locality": t["locality"], "reporter_count": t.get("reporter_count", 1),
                "due_at": t["due_at"],
                "escalation_level": sla.escalation_level(t["due_at"], t.get("reporter_count", 1)),
            })
        return out
    finally:
        conn.close()


@app.post("/call-webhook")
async def call_webhook(request: Request):
    """Bolna post-call webhook -> persist the call + run KuralEval. Accepts ANY JSON shape
    (our flat form OR Bolna's nested execution object) and never 422s / never 500s."""
    try:
        body = await request.json()
    except Exception:                 # noqa: BLE001 - tolerate non-JSON / empty bodies
        body = {}
    if not isinstance(body, dict):
        body = {}

    call_id = str(body.get("call_id") or body.get("execution_id") or body.get("id")
                  or f"call-{db.now_iso()}")
    tr = body.get("transcript") or body.get("conversation") or body.get("messages") or ""
    turns = body.get("turns") if isinstance(body.get("turns"), list) else None
    if turns is None and isinstance(tr, list):        # transcript arrived as a turn list
        turns = [t for t in tr if isinstance(t, dict)]
    if isinstance(tr, list):
        tr = " ".join(str(t.get("text", "")) for t in tr if isinstance(t, dict))
    tr = str(tr or "")
    latency = body.get("latency_ms") or body.get("latency")
    lang = body.get("lang_mix")

    conn = db.get_conn()
    try:
        db.insert_call(conn, dict(
            id=call_id, phone=body.get("phone") or body.get("from"),
            started_at=db.now_iso(), ended_at=db.now_iso(),
            recording_url=body.get("recording_url") or body.get("recording"),
            transcript=tr, lang_mix=",".join(lang) if isinstance(lang, list) else (lang or "")))
        scores = run_eval(dict(transcript=tr, latency_ms=latency, turns=turns))
        scores["call_id"] = call_id
        scores["created_at"] = db.now_iso()
        db.insert_eval(conn, scores)
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "call_id": call_id, "eval": scores}


@app.get("/api/tickets")
def api_tickets():
    conn = db.get_conn()
    try:
        return db.list_tickets(conn)
    finally:
        conn.close()


@app.get("/api/stats")
def api_stats():
    conn = db.get_conn()
    try:
        return db.stats(conn)
    finally:
        conn.close()


@app.get("/api/evals")
def api_evals():
    conn = db.get_conn()
    try:
        return db.list_evals(conn)
    finally:
        conn.close()
