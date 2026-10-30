"""Kural test suite — routing, SLA, dedup-merge, and the API. Run:  pytest -q"""

import os
import sys
import datetime as dt
from pathlib import Path

KURAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KURAL))
os.environ["KURAL_DB"] = "test_kural.db"          # isolate from the real DB (lives in kural/)

_dbfile = KURAL / "test_kural.db"
if _dbfile.exists():
    _dbfile.unlink()

from fastapi.testclient import TestClient          # noqa: E402
from app import db, sla, billing                   # noqa: E402
from app.routing import resolve                    # noqa: E402
from app.main import app                           # noqa: E402

db.init_db()
client = TestClient(app)


# ---------- routing ----------
def test_electricity_statewide():
    assert "TNPDCL" in resolve("electricity", region="rural").owning_body


def test_water_region_split():
    assert "CMWSSB" in resolve("water_supply", region="chennai").owning_body
    rr = resolve("water_supply", region="rural")
    assert "TWAD" in rr.owning_body and rr.sla_days == 1


def test_roads_chennai_gcc():
    r = resolve("roads_internal", region="chennai")
    assert r.owning_body == "Greater Chennai Corporation" and r.sla_days == 5


def test_unknown_sector_falls_back():
    assert resolve("banana").owning_body.startswith("CM Helpline")


# ---------- SLA ----------
def test_business_days_skip_weekend():
    d = dt.datetime(2026, 1, 1)
    while d.weekday() != 4:                        # find a Friday
        d += dt.timedelta(days=1)
    due = dt.datetime.fromisoformat(sla.due_at(1, d))
    assert due.weekday() == 0                      # +1 business day -> Monday


def test_escalation_ladder():
    future = (dt.datetime.now() + dt.timedelta(days=5)).isoformat()
    assert sla.escalation_level(future) == "ward"
    past = (dt.datetime.now() - dt.timedelta(days=10)).isoformat()
    assert sla.escalation_level(past) in ("regional", "commissioner")


# ---------- API + dedup ----------
def _p(sector, text, region, sev="high", phone="+910000000000"):
    return {"caller": {"name": "T", "phone": phone}, "utterance": text,
            "extracted": {"sector": sector, "severity": sev,
                          "locality": {"text": text, "region": region}}}


def test_grievance_routes_and_files():
    d = client.post("/grievance", json=_p("roads_internal", "Velachery 6th St", "chennai")).json()
    assert d["owning_body"] == "Greater Chennai Corporation"
    assert d["ticket_id"].startswith("KRL-")


def test_dedup_merges_same_area():
    a = client.post("/grievance", json=_p("water_supply", "T Nagar 2nd St", "chennai", phone="+911")).json()
    b = client.post("/grievance", json=_p("water_supply", "T Nagar 2nd St", "chennai", phone="+912")).json()
    assert b["duplicate_of"] == a["ticket_id"]     # merged, not a second ticket
    assert b["cluster_size"] == 2


def test_ticket_lifecycle():
    tid = client.post("/grievance", json=_p("streetlight", "Mylapore", "chennai")).json()["ticket_id"]
    assert client.get(f"/ticket/{tid}").json()["id"] == tid
    assert client.post(f"/ticket/{tid}/resolve").json()["status"] == "resolved"
    assert client.get("/ticket/NOPE").status_code == 404


def test_escalations_is_list():
    assert isinstance(client.get("/api/escalations").json(), list)


def test_flat_file_endpoint():
    # Bolna's custom_task calls /file with flat query params
    d = client.get("/file", params={"sector": "water_supply", "locality": "Besant Nagar Chennai",
                                     "region": "chennai", "severity": "high",
                                     "name": "T", "phone": "+91"}).json()
    assert d["owning_body"] == "CMWSSB (Chennai Metro Water)"
    assert d["ticket_id"].startswith("KRL-") and d["spoken_confirmation"]


# ---------- billing + city + autonomy tools ----------
def test_billing_anomaly_and_normal():
    b = billing.analyze(units=200, amount_charged=2000)      # expected ~235
    assert b["anomaly"] is True and b["amount_over"] > 1000
    assert billing.analyze(units=200, amount_charged=235)["anomaly"] is False


def test_city_routing_coimbatore():
    r = resolve("solid_waste", locality_text="Kuniyamuthur 12th Street Coimbatore")
    assert r.city == "coimbatore" and "Coimbatore" in r.owning_body and r.region == "urban"
    r2 = resolve("electricity", locality_text="Coimbatore")
    assert "TNPDCL" in r2.owning_body and r2.city == "coimbatore"


def test_file_with_billing_overcharge():
    d = client.get("/file", params={"sector": "electricity", "locality": "RS Puram Coimbatore",
                                     "region": "urban", "severity": "high",
                                     "units": 200, "charged": 2000}).json()
    assert d["anomaly"] is True and d["amount_over"] > 0 and "TNPDCL" in d["owning_body"]


def test_area_and_ticket_status():
    g = client.get("/file", params={"sector": "water_supply", "locality": "KK Nagar Madurai spot",
                                     "region": "urban", "severity": "high", "phone": "+91777"}).json()
    a = client.get("/area-status", params={"locality": "KK Nagar Madurai spot",
                                            "sector": "water_supply"}).json()
    assert a["existing_reports"] >= 1
    s = client.get(f"/ticket-status/{g['ticket_id']}").json()
    assert s["found"] is True and s["ticket_id"] == g["ticket_id"]
    assert client.get("/ticket-status/NOPE").json()["found"] is False


def test_eval_webhook_scores():
    e = client.post("/call-webhook", json={
        "call_id": "t1", "latency_ms": 650,
        "transcript": "வணக்கம் current போச்சு correct-ah சரி Ticket KRL"}).json()
    assert 0 <= e["eval"]["overall"] <= 100


def test_eval_detects_wrong_language():
    # caller spoke Tamil/Tanglish, agent replied English-only -> vernacular failure
    e = client.post("/call-webhook", json={"call_id": "lm1", "latency_ms": 600,
        "transcript": "தண்ணி வரலை help பண்ணுங்க Sure registered",
        "turns": [{"speaker": "user", "text": "தண்ணி வரலை, help பண்ணுங்க"},
                  {"speaker": "agent", "text": "Sure, I have registered your complaint."}]}).json()
    assert e["eval"]["lang_match_ok"] == 0


def test_eval_romanized_and_match_ok():
    e = client.post("/call-webhook", json={"call_id": "lm2", "latency_ms": 600,
        "transcript": "thanni varala",
        "turns": [{"speaker": "user", "text": "thanni varala"},
                  {"speaker": "agent", "text": "சரி, ticket register பண்ணிட்டேன்"}]}).json()
    assert e["eval"]["romanized_tamil"] == 1 and e["eval"]["lang_match_ok"] == 1
