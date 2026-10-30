"""Grievance filing service — shared by the API (main.py) and the seed script.

Flow: resolve owning body (city-aware) -> billing anomaly analysis (if an electricity bill
dispute) -> DEDUP-MERGE repeat callers -> ticket + SLA -> office dispatch -> citizen SMS."""

import datetime as dt

from . import db, sla, billing as billing_mod
from .routing import resolve
from .sms import send_sms
from .dispatch import report_to_office
from .models import Extracted, Caller, Locality, GrievanceOut


def cluster_key(body, region, sector, locality) -> str:
    loc = (locality or "").strip().lower()[:24]
    return f"{body}|{region}|{sector}|{loc}"


def spoken_confirmation(name, routing, locality, ticket_id, bill=None) -> str:
    who = name or "நீங்க"
    line = (f"{who} சொன்ன '{routing.sector}' பிரச்சனை, {locality or 'உங்க area'}-ல — "
            f"idhu {routing.owning_body}-ku ({routing.department}) anuppi-விட்டேன். "
            f"Ticket number {ticket_id}. SLA {routing.sla_days} naal. SMS-la kedaikum.")
    if bill and bill.get("anomaly"):
        line += (f" Ungaluku சுமார் ₹{bill['amount_over']:.0f} ({bill['pct_over']:.0f}%) "
                 f"extra charge aagirukku — idhai CGRF / TNERC-ku escalate pannuvom.")
    return line


def file_grievance(extracted: Extracted, caller: Caller,
                   call_id=None, utterance=None, billing=None) -> GrievanceOut:
    loc = extracted.locality or Locality()
    routing = resolve(extracted.sector, region=loc.region, locality_text=loc.text)
    ck = cluster_key(routing.owning_body, routing.region, routing.sector, loc.text)
    zone = routing.city.title() if routing.city else loc.zone

    # billing-dispute analysis (electricity over-charge)
    bill = None
    if billing and (billing.get("units_used") or billing.get("amount_charged")):
        bill = billing_mod.analyze(billing.get("units_used"),
                                   billing.get("amount_charged"),
                                   billing.get("expected_amount"))

    conn = db.get_conn()
    try:
        dup = db.open_duplicate_ticket(conn, ck)
        if dup:
            tid = dup["id"]
            count = db.increment_reporter(conn, tid)
            db.bump_severity(conn, tid, extracted.severity)
            db.add_reporter(conn, tid, caller.name, caller.phone, caller.raw_address)
            due, duplicate_of = dup["due_at"], tid
        else:
            tid = db.next_ticket_id(conn)
            due = sla.due_at(routing.sla_days, dt.datetime.now())
            b = bill or {}
            row = dict(id=tid, call_id=call_id, sector=routing.sector,
                       owning_body=routing.owning_body, department=routing.department,
                       field_cadre=routing.field_cadre, channel=routing.channel,
                       zone=zone, region=routing.region, locality=loc.text,
                       severity=extracted.severity, summary=(utterance or "")[:280],
                       status="open", sla_days=routing.sla_days,
                       created_at=db.now_iso(), due_at=due, cluster_key=ck,
                       reporter_count=1, dispatched=0,
                       units_used=b.get("units_used"), amount_charged=b.get("amount_charged"),
                       expected_amount=b.get("expected_amount"), amount_over=b.get("amount_over"),
                       anomaly=1 if b.get("anomaly") else 0, sms_sent=0)
            db.insert_ticket(conn, row)
            db.add_reporter(conn, tid, caller.name, caller.phone, caller.raw_address)
            report_to_office(row)
            db.mark_dispatched(conn, tid)
            count, duplicate_of = 1, None

        sms_ok = send_sms(caller.phone,
                          f"Kural: Ticket {tid} registered ({routing.sector} -> "
                          f"{routing.owning_body}). SLA {routing.sla_days} working days.")
        if sms_ok and not dup:
            conn.execute("UPDATE tickets SET sms_sent=1 WHERE id=?", (tid,))
        conn.commit()
    finally:
        conn.close()

    out = GrievanceOut(
        ticket_id=tid, owning_body=routing.owning_body, department=routing.department,
        field_cadre=routing.field_cadre, zone=zone, channel=routing.channel,
        region=routing.region, sla_days=routing.sla_days, due_at=due, sms_sent=sms_ok,
        duplicate_of=duplicate_of, cluster_size=count,
        spoken_confirmation=spoken_confirmation(caller.name, routing, loc.text, tid, bill))
    if bill:
        out.units_used = bill["units_used"]
        out.amount_charged = bill["amount_charged"]
        out.expected_amount = bill["expected_amount"]
        out.amount_over = bill["amount_over"]
        out.pct_over = bill["pct_over"]
        out.anomaly = bill["anomaly"]
    return out
