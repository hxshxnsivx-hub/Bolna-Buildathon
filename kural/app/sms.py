"""Citizen confirmation SMS via Plivo. Gracefully stubs (logs) when creds are absent,
so the whole loop runs offline."""

import os
import requests


def send_sms(to: str | None, body: str) -> bool:
    aid = os.getenv("PLIVO_AUTH_ID")
    tok = os.getenv("PLIVO_AUTH_TOKEN")
    src = os.getenv("PLIVO_SRC_NUMBER")
    if not (aid and tok and src and to):
        print(f"[SMS stub] -> {to or '<no number>'}: {body}")
        return False
    try:
        r = requests.post(
            f"https://api.plivo.com/v1/Account/{aid}/Message/",
            auth=(aid, tok), timeout=10,
            json={"src": src, "dst": to, "text": body})
        if r.status_code in (200, 201, 202):
            return True
        print(f"[SMS error] {r.status_code} {r.text[:200]}")
        return False
    except Exception as e:                      # noqa: BLE001 - never break a call over SMS
        print(f"[SMS exception] {e}")
        return False
