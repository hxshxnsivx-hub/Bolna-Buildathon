# Kural — Phased Project Plan (Work Breakdown Structure)

Legend: ✅ done · 🔨 in progress · ⬜ to do · 🔑 needs your accounts/keys (voice go-live)
Target: Bolna × Plivo Symphony Buildathon — submission **Oct 31, 2026**.

---

## PHASE 0 — Research & Design  ✅ COMPLETE
- **0.1 Opportunity analysis** ✅ — hackathon, Bolna company & hiring fit (dossiers 05).
- **0.2 Domain R&D** ✅ — TN civic-services tree + problems (dossiers 01–04, 06).
- **0.3 Architecture & stack** ✅ — system design + council verdict (architecture 01–02).

## PHASE 1 — Core Brain  ✅ COMPLETE
- **1.1 Deterministic routing table** ✅ — `app/routing.py` (14 sectors × 3 regions).
- **1.2 Ticketing + SLA engine** ✅ — `app/db.py`, `app/sla.py` (business-day due dates).
- **1.3 Tanglish NLU classifier** ✅ — `app/nlu.py` (LLM + heuristic fallback).
- **1.4 SMS dispatch** ✅ — `app/sms.py` (Plivo; stubs offline).
- **1.5 KuralEval scorecard** ✅ — `app/eval.py` (LLM-as-judge + heuristic).
- **1.6 API + smoke test** ✅ — `app/main.py`; verified.

## PHASE 2 — Dashboard UI  ✅ COMPLETE
- **2.1 Tailwind ops console** ✅ — `web/index.html` (dark gov-tech, Tamil fonts).
- **2.2 Live polling + file box + toasts** ✅.
- **2.3 Served from FastAPI at `/`** ✅ (same-origin, zero-build).

## PHASE 3 — Hardening  🔨 THIS PHASE (code I own, fully testable)
- **3.1 Duplicate merge** 🔨 — collapse N callers of the same issue+area into ONE ticket with
  a reporter count; hotspot when reporters ≥ 3. (`/grievance` append-on-duplicate.)
- **3.2 Escalation engine** 🔨 — `GET /api/escalations`: breached tickets with ward→zonal→
  regional→commissioner level (hotspots jump a tier).
- **3.3 Ticket lifecycle** 🔨 — `GET /ticket/{id}` (with reporters), `POST /ticket/{id}/resolve`.
- **3.4 Office dispatch stub** 🔨 — `app/dispatch.py`: record a WhatsApp/email "report filed to
  <office>" per ticket (stub now, real channel later).
- **3.5 Test suite** 🔨 — `tests/test_kural.py` (pytest): routing, SLA, dedup, API.
- **3.6 Dashboard: reporters + escalation badges** 🔨.

## PHASE 4 — Voice Go-Live  ⬜ 🔑 (needs your accounts)
- **4.1 Plivo India number + KYC** 🔑 — start immediately (longest pole).
- **4.2 Bolna agent build** ⬜ — import `agent/system_prompt.md`; wire `file_grievance` → `/grievance`.
- **4.3 Sarvam ASR + Cartesia TTS** ⬜ — configure; 30-min Tanglish smoke test.
- **4.4 Deploy brain** ⬜ — Render/Railway; public HTTPS webhook URL.
- **4.5 Live end-to-end call** ⬜ — real inbound Tanglish call → ticket → SMS → dashboard.

## PHASE 5 — Demo & Submission  ⬜ (final 24h)
- **5.1 Demo video (2.5 min)** ⬜ — 3 scenarios (utility/urban, sanitation/rural, cross-agency).
- **5.2 Pitch + README polish** ⬜ — "built on Bolna; hardest vernacular voice test" narrative.
- **5.3 Public GitHub + submission form** ⬜.
- **5.4 Bolna Slack visibility** ⬜.

## PHASE 6 — Roadmap (post-MVP, narrate don't build)  ⬜
- **6.1 SLA scheduler/cron** · **6.2 IIPGCMS API dispatch** · **6.3 Offline queue-and-forward**
  · **6.4 Self-healing prompt optimization** (KuralEval → auto prompt-fix).

---

### Execution order & dependencies
Phase 3 (now) is independent of accounts → finish & test today. Phase 4 unblocks only after
you start Plivo KYC and give Bolna/Sarvam keys. Phase 5 depends on 4. Phase 6 is pitch-only.
