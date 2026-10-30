"""SQLite persistence for Kural. Single-file DB, zero-ops — upgradeable to
Supabase/Postgres later without touching the API (schema mirrors docs/architecture/01)."""

import os
import sqlite3
import datetime as dt
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent          # .../kural
DB_PATH = BASE_DIR / os.getenv("KURAL_DB", "kural.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id            TEXT PRIMARY KEY,
    call_id       TEXT,
    sector        TEXT,
    owning_body   TEXT,
    department    TEXT,
    field_cadre   TEXT,
    channel       TEXT,
    zone          TEXT,
    region        TEXT,
    locality      TEXT,
    severity      TEXT,
    summary       TEXT,
    status        TEXT DEFAULT 'open',
    sla_days      INTEGER,
    created_at    TEXT,
    due_at        TEXT,
    cluster_key   TEXT,
    reporter_count INTEGER DEFAULT 1,
    dispatched    INTEGER DEFAULT 0,
    units_used     REAL,
    amount_charged REAL,
    expected_amount REAL,
    amount_over    REAL,
    anomaly        INTEGER DEFAULT 0,
    sms_sent      INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS reporters (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id  TEXT,
    name       TEXT,
    phone      TEXT,
    raw_address TEXT
);
CREATE TABLE IF NOT EXISTS calls (
    id            TEXT PRIMARY KEY,
    phone         TEXT,
    started_at    TEXT,
    ended_at      TEXT,
    recording_url TEXT,
    transcript    TEXT,
    lang_mix      TEXT
);
CREATE TABLE IF NOT EXISTS eval_scores (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    call_id          TEXT,
    asr_ok           INTEGER,
    lang_switch_ok   INTEGER,
    task_complete    INTEGER,
    repair_ok        INTEGER,
    latency_ms       INTEGER,
    hallucination    INTEGER,
    compliance_ok    INTEGER,
    lang_match_ok    INTEGER DEFAULT 1,
    tamil_ratio      INTEGER DEFAULT 0,
    romanized_tamil  INTEGER DEFAULT 0,
    overall          REAL,
    notes            TEXT,
    created_at       TEXT
);
"""


def init_db():
    conn = get_conn()
    try:
        conn.executescript(SCHEMA)
        # lightweight migrations for pre-existing DBs
        for tbl, col, ddl in (("tickets", "reporter_count", "INTEGER DEFAULT 1"),
                              ("tickets", "dispatched", "INTEGER DEFAULT 0"),
                              ("tickets", "units_used", "REAL"),
                              ("tickets", "amount_charged", "REAL"),
                              ("tickets", "expected_amount", "REAL"),
                              ("tickets", "amount_over", "REAL"),
                              ("tickets", "anomaly", "INTEGER DEFAULT 0"),
                              ("eval_scores", "lang_match_ok", "INTEGER DEFAULT 1"),
                              ("eval_scores", "tamil_ratio", "INTEGER DEFAULT 0"),
                              ("eval_scores", "romanized_tamil", "INTEGER DEFAULT 0")):
            try:
                conn.execute(f"ALTER TABLE {tbl} ADD COLUMN {col} {ddl}")
            except sqlite3.OperationalError:
                pass  # column already exists
        conn.commit()
    finally:
        conn.close()


def now_iso() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def next_ticket_id(conn) -> str:
    year = dt.date.today().year
    n = conn.execute("SELECT COUNT(*) AS c FROM tickets").fetchone()["c"] + 1
    return f"KRL-{year}-{n:05d}"


def find_open_duplicate(conn, cluster_key: str) -> Optional[str]:
    """Dedup stretch: an open ticket with the same (body x locality x sector)."""
    row = conn.execute(
        "SELECT id FROM tickets WHERE cluster_key = ? AND status = 'open' "
        "ORDER BY created_at LIMIT 1", (cluster_key,)).fetchone()
    return row["id"] if row else None


def insert_ticket(conn, t: dict):
    cols = ("id", "call_id", "sector", "owning_body", "department", "field_cadre",
            "channel", "zone", "region", "locality", "severity", "summary", "status",
            "sla_days", "created_at", "due_at", "cluster_key", "reporter_count",
            "dispatched", "units_used", "amount_charged", "expected_amount",
            "amount_over", "anomaly", "sms_sent")
    conn.execute(
        f"INSERT INTO tickets ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
        tuple(t.get(c) for c in cols))


def add_reporter(conn, ticket_id, name, phone, raw_address):
    conn.execute("INSERT INTO reporters (ticket_id, name, phone, raw_address) "
                 "VALUES (?,?,?,?)", (ticket_id, name, phone, raw_address))


def cluster_count(conn, cluster_key: str) -> int:
    return conn.execute("SELECT COUNT(*) AS c FROM tickets WHERE cluster_key = ?",
                        (cluster_key,)).fetchone()["c"]


def open_duplicate_ticket(conn, cluster_key: str):
    """The open ticket (if any) for this body x locality x sector — the merge target."""
    row = conn.execute(
        "SELECT * FROM tickets WHERE cluster_key=? AND status='open' "
        "ORDER BY created_at LIMIT 1", (cluster_key,)).fetchone()
    return dict(row) if row else None


def increment_reporter(conn, ticket_id: str) -> int:
    conn.execute("UPDATE tickets SET reporter_count = reporter_count + 1 WHERE id=?",
                 (ticket_id,))
    return conn.execute("SELECT reporter_count AS c FROM tickets WHERE id=?",
                        (ticket_id,)).fetchone()["c"]


def bump_severity(conn, ticket_id: str, severity: str):
    if severity == "high":
        conn.execute("UPDATE tickets SET severity='high' WHERE id=?", (ticket_id,))


def mark_dispatched(conn, ticket_id: str):
    conn.execute("UPDATE tickets SET dispatched=1 WHERE id=?", (ticket_id,))


def get_reporters(conn, ticket_id: str):
    return [dict(r) for r in conn.execute(
        "SELECT name, phone, raw_address FROM reporters WHERE ticket_id=?",
        (ticket_id,)).fetchall()]


def resolve_ticket(conn, ticket_id: str) -> bool:
    cur = conn.execute("UPDATE tickets SET status='resolved' WHERE id=? AND status='open'",
                       (ticket_id,))
    return cur.rowcount > 0


def breached_open(conn):
    return [dict(r) for r in conn.execute(
        "SELECT * FROM tickets WHERE status='open' AND due_at < ? ORDER BY due_at",
        (now_iso(),)).fetchall()]


def list_tickets(conn, limit=200):
    return [dict(r) for r in conn.execute(
        "SELECT * FROM tickets ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()]


def get_ticket(conn, ticket_id):
    row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return dict(row) if row else None


def insert_call(conn, c: dict):
    conn.execute(
        "INSERT OR REPLACE INTO calls (id, phone, started_at, ended_at, "
        "recording_url, transcript, lang_mix) VALUES (?,?,?,?,?,?,?)",
        (c.get("id"), c.get("phone"), c.get("started_at"), c.get("ended_at"),
         c.get("recording_url"), c.get("transcript"), c.get("lang_mix")))


def insert_eval(conn, e: dict):
    cols = ("call_id", "asr_ok", "lang_switch_ok", "lang_match_ok", "tamil_ratio",
            "romanized_tamil", "task_complete", "repair_ok", "latency_ms",
            "hallucination", "compliance_ok", "overall", "notes", "created_at")
    conn.execute(
        f"INSERT INTO eval_scores ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
        tuple(e.get(c) for c in cols))


def list_evals(conn, limit=200):
    return [dict(r) for r in conn.execute(
        "SELECT * FROM eval_scores ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()]


def stats(conn) -> dict:
    total = conn.execute("SELECT COUNT(*) AS c FROM tickets").fetchone()["c"]
    by_status = {r["status"]: r["c"] for r in conn.execute(
        "SELECT status, COUNT(*) AS c FROM tickets GROUP BY status")}
    by_body = {r["owning_body"]: r["c"] for r in conn.execute(
        "SELECT owning_body, COUNT(*) AS c FROM tickets GROUP BY owning_body")}
    breached = conn.execute(
        "SELECT COUNT(*) AS c FROM tickets WHERE status='open' AND due_at < ?",
        (now_iso(),)).fetchone()["c"]
    hotspots = conn.execute(
        "SELECT COUNT(*) AS c FROM tickets WHERE reporter_count >= 3").fetchone()["c"]
    return {"total": total, "by_status": by_status, "by_body": by_body,
            "breached": breached, "hotspots": hotspots}
