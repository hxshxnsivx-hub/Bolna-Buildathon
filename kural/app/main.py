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
from .service import file_grievance
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
    return file_grievance(payload.extracted, payload.caller,
                          payload.call_id, payload.utterance)


@app.post("/intake", response_model=GrievanceOut)
def intake(payload: ClassifyIn):
    """TEXT demo mode: classify a raw Tanglish sentence, then file it — no telephony."""
    c = nlu.classify(payload.utterance)
    extracted = Extracted(sector=c.get("sector", "other"),
                          severity=c.get("severity", "medium"),
                          locality=Locality(text=c.get("locality"), region=c.get("region")))
    return file_grievance(extracted, payload.caller, None, payload.utterance)


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
def resolve(ticket_id: str):
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
