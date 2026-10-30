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
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from . import db, sla, nlu
from .eval import run_eval
from .routing import resolve
from .service import file_grievance, cluster_key
from .models import (GrievanceIn, GrievanceOut, ClassifyIn, CallWebhookIn,
                     Extracted, Caller, Locality)

load_dotenv()
app = FastAPI(title="Kural — civic grievance brain", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@app.on_event("startup")
def _startup():
    db.init_db()


@app.get("/")
def home():
    """Serve the Tailwind ops dashboard at the API origin — no CORS, no build."""
    return FileResponse(WEB_DIR / "index.html")


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


@app.api_route("/file", methods=["GET", "POST"])
def file_flat(sector: str = "other", locality: str = "", region: str = "",
              severity: str = "medium", name: str = "", phone: str = "",
              call_id: str = "", utterance: str = "",
              units: float | None = None, charged: float | None = None,
              expected: float | None = None):
    """Flat-params entry for Bolna's custom_task tool (templates %(name)s into a URL).
    For electricity bill disputes pass units/charged/(expected) -> the brain computes the
    over-charge + anomaly. Maps simple query params -> file_grievance."""
    extracted = Extracted(sector=sector or "other", severity=severity or "medium",
                          locality=Locality(text=locality or None, region=region or None))
    caller = Caller(name=name or None, phone=phone or None, raw_address=locality or None)
    billing = None
    if units is not None or charged is not None:
        billing = {"units_used": units, "amount_charged": charged, "expected_amount": expected}
    return file_grievance(extracted, caller, call_id or None,
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
def call_webhook(payload: CallWebhookIn):
    """Bolna post-call webhook -> persist the call and run KuralEval."""
    conn = db.get_conn()
    try:
        db.insert_call(conn, dict(
            id=payload.call_id, phone=payload.phone, started_at=db.now_iso(),
            ended_at=db.now_iso(), recording_url=payload.recording_url,
            transcript=payload.transcript, lang_mix=",".join(payload.lang_mix or [])))
        scores = run_eval(dict(transcript=payload.transcript, latency_ms=payload.latency_ms,
                               turns=payload.turns))
        scores["call_id"] = payload.call_id
        scores["created_at"] = db.now_iso()
        db.insert_eval(conn, scores)
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "eval": scores}


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
