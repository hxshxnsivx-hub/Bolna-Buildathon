"""Seed the DB with the 3 demo scenarios + a MERGED hotspot (3 callers -> 1 ticket)
+ sample eval rows, so the dashboard looks alive.  Run:  python scripts/seed.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # import `app`

from app import db                                                # noqa: E402
from app.service import file_grievance                            # noqa: E402
from app.models import Extracted, Caller, Locality                # noqa: E402
from app.eval import run_eval                                     # noqa: E402

# (utterance, sector, region, locality, severity, name, phone)
SCENARIOS = [
    ("Enga area-la current போயி 3 naal aachu, transformer-la spark varudhu",
     "electricity", "chennai", "Velachery 6th Street", "high", "Murugan", "+919000000001"),
    ("village-la garbage collect பண்றதில்லை, bins overflow aagudhu",
     "solid_waste", "rural", "Melur village panchayat", "medium", "Lakshmi", "+919000000002"),
    ("Street light 2 வாரமா work aagala, ரொம்ப dark-a iruku, safety problem",
     "streetlight", "chennai", "Adyar 3rd Main", "high", "Ravi", "+919000000003"),
    # 3 callers, same water issue + area -> MERGES into one hotspot ticket
    ("தண்ணி வரலை 4 naal-a, Anna Nagar West",
     "water_supply", "chennai", "Anna Nagar West", "high", "Kumar", "+919000000004"),
    ("No water supply Anna Nagar West, pipe leak",
     "water_supply", "chennai", "Anna Nagar West", "high", "Devi", "+919000000005"),
    ("Anna Nagar West-la water illa, 4 days",
     "water_supply", "chennai", "Anna Nagar West", "medium", "Fathima", "+919000000006"),
]


def main():
    db.init_db()
    for utt, sector, region, loc, sev, name, phone in SCENARIOS:
        g = file_grievance(
            Extracted(sector=sector, severity=sev,
                      locality=Locality(text=loc, region=region)),
            Caller(name=name, phone=phone, raw_address=loc), utterance=utt)
        tag = (f"(merged -> {g.duplicate_of}, {g.cluster_size} reporters)"
               if g.duplicate_of else "")
        print(f"  {g.ticket_id}: {sector} -> {g.owning_body} {tag}")

    conn = db.get_conn()
    try:
        eval_demos = [
            ("demo-call-1", "வணக்கம் Kural... current போச்சு... correct-ah? சரி... Ticket KRL", None),
            ("demo-call-2", "garbage problem village... ok ticket number", None),
            # a FAILED call: caller speaks Tanglish, agent replies English-only -> lang_match_ok=0
            ("demo-call-3", "thanni varala help pannunga",
             [{"speaker": "user", "text": "தண்ணி வரலை, help பண்ணுங்க"},
              {"speaker": "agent", "text": "Sure, your complaint has been registered."}]),
        ]
        for cid, tr, turns in eval_demos:
            e = run_eval(dict(transcript=tr, latency_ms=720, turns=turns))
            e.update(call_id=cid, created_at=db.now_iso())
            db.insert_eval(conn, e)
        conn.commit()
    finally:
        conn.close()
    print("Seed complete.")


if __name__ == "__main__":
    main()
