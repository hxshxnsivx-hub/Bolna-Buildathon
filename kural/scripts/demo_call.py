"""Simulate a call without telephony: send a Tanglish sentence to the running brain.

Usage:
  python scripts/demo_call.py "Enga street-la pothole, bike விழுந்துடுச்சு"
  python scripts/demo_call.py            # runs the 3 built-in demo lines

Requires the API running:  uvicorn app.main:app --reload
"""

import sys
import json
import requests

API = "http://localhost:8000/intake"
DEMOS = [
    "Enga area-la current போயி 3 naal aachu, transformer-la spark",
    "village-la garbage collect பண்றதில்லை, bins overflow",
    "property tax online pay பண்ணேன், money போச்சு receipt வரலை",
]


def fire(utterance: str):
    r = requests.post(API, json={"utterance": utterance,
                                 "caller": {"name": "Demo", "phone": "+919000000000"}},
                      timeout=30)
    r.raise_for_status()
    d = r.json()
    print(f"\n🗣️  {utterance}")
    print(f"   → ticket {d['ticket_id']} | {d['owning_body']} / {d['department']} "
          f"({d['field_cadre']}) | region={d['region']} | SLA {d['sla_days']}d | "
          f"dup_of={d['duplicate_of']} | cluster={d['cluster_size']}")
    print(f"   🔊 {d['spoken_confirmation']}")


if __name__ == "__main__":
    args = sys.argv[1:]
    for u in (args or DEMOS):
        try:
            fire(u)
        except Exception as e:                  # noqa: BLE001
            print(f"   ! error: {e}  (is the API running on :8000?)")
