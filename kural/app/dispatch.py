"""Office dispatch — hands a filed grievance to the owning office.

Stub: logs/records a WhatsApp/email "report filed to <office>". Swap the body for a real
channel (WhatsApp Business API / email / IIPGCMS API) later — the call site never changes."""


def report_to_office(ticket: dict) -> dict:
    line = (f"[OFFICE DISPATCH] -> {ticket['owning_body']} / {ticket.get('department', '')} "
            f"via {ticket.get('channel', '')}: Ticket {ticket['id']} | {ticket['sector']} | "
            f"{ticket.get('locality', '')} | severity {ticket.get('severity', '')} | "
            f"SLA {ticket.get('sla_days')}d")
    print(line)
    return {"to": ticket["owning_body"], "channel": ticket.get("channel"),
            "status": "queued"}
