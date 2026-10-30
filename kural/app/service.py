"""Grievance filing service — shared by the API (main.py) and the seed script.

Flow: resolve owning body -> DEDUP-MERGE (collapse repeat callers of the same issue+area into
one ticket with a reporter count) -> ticket + SLA -> office dispatch -> citizen SMS."""

import datetime as dt

from . import db, sla
from .routing import resolve
from .sms import send_sms
from .dispatch import report_to_office
from .models import Extracted, Caller, Locality, GrievanceOut


def cluster_key(body, region, sector, locality) -> str:
    loc = (locality or "").strip().lower()[:24]
    return f"{body}|{region}|{sector}|{loc}"


def spoken_confirmation(name, routing, locality, ticket_id) -> str:
    who = name or "நீங்க"
    return (f"{who} சொன்ன '{routing.sector}' பிரச்சனை, {locality or 'உங்க area'}-ல — "
            f"idhu {routing.owning_body}-ku ({routing.department}) anuppi-விட்டேன். "
            f"Ticket number {ticket_id}. SLA {routing.sla_days} naal. SMS-la kedaikum.")


def file_grievance(extracted: Extracted, caller: Caller,
                   call_id=None, utterance=None) -> GrievanceOut:
    loc = extracted.locality or Locality()
    routing = resolve(extracted.sector, region=loc.region, locality_text=loc.text)
    ck = cluster_key(routing.owning_body, routing.region, routing.sector, loc.text)

    conn = db.get_conn()
    try:
        dup = db.open_duplicate_ticket(conn, ck)
        if dup:
            # same issue + area already open -> attach this caller, no new ticket
            tid = dup["id"]
            count = db.increment_reporter(conn, tid)
            db.bump_severity(conn, tid, extracted.severity)
            db.add_reporter(conn, tid, caller.name, caller.phone, caller.raw_address)
            due, duplicate_of = dup["due_at"], tid
        else:
            tid = db.next_ticket_id(conn)
            due = sla.due_at(routing.sla_days, dt.datetime.now())
            row = dict(id=tid, call_id=call_id, sector=routing.sector,
                       owning_body=routing.owning_body, department=routing.department,
                       field_cadre=routing.field_cadre, channel=routing.channel,
                       zone=loc.zone, region=routing.region, locality=loc.text,
                       severity=extracted.severity, summary=(utterance or "")[:280],
                       status="open", sla_days=routing.sla_days,
                       created_at=db.now_iso(), due_at=due, cluster_key=ck,
                       reporter_count=1, dispatched=0, sms_sent=0)
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

    return GrievanceOut(
        ticket_id=tid, owning_body=routing.owning_body, department=routing.department,
        field_cadre=routing.field_cadre, zone=loc.zone, channel=routing.channel,
        region=routing.region, sla_days=routing.sla_days, due_at=due, sms_sent=sms_ok,
        duplicate_of=duplicate_of, cluster_size=count,
        spoken_confirmation=spoken_confirmation(caller.name, routing, loc.text, tid))
