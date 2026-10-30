"""SLA clock + escalation. Business-day due dates; tiered escalation ladder
(ward -> zonal -> regional -> commissioner) driven off the owning department."""

import datetime as dt

ESCALATION_LADDER = ["ward", "zonal", "regional", "commissioner"]


def add_business_days(start: dt.datetime, days: int) -> dt.datetime:
    d = start
    added = 0
    while added < days:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:          # Mon-Fri
            added += 1
    return d


def due_at(sla_days: int, start: dt.datetime | None = None) -> str:
    start = start or dt.datetime.now()
    return add_business_days(start, max(sla_days, 1)).replace(microsecond=0).isoformat()


def is_breached(due_iso: str, now: dt.datetime | None = None) -> bool:
    try:
        return (now or dt.datetime.now()) > dt.datetime.fromisoformat(due_iso)
    except (ValueError, TypeError):
        return False


def escalation_level(due_iso: str, cluster_size: int = 1,
                     now: dt.datetime | None = None) -> str:
    """How far up the ladder this ticket should be, given lateness + how many
    callers reported the same thing (a hotspot escalates faster)."""
    now = now or dt.datetime.now()
    if not is_breached(due_iso, now):
        return "ward"
    try:
        overdue_days = (now - dt.datetime.fromisoformat(due_iso)).days
    except (ValueError, TypeError):
        overdue_days = 0
    idx = 1 + overdue_days // 3            # +1 tier per ~3 business days overdue
    if cluster_size >= 5:                  # hotspot: jump a tier
        idx += 1
    return ESCALATION_LADDER[min(idx, len(ESCALATION_LADDER) - 1)]
