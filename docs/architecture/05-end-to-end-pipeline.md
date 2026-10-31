# Kural — End-to-End Pipeline & Workflow

The complete live system: a citizen's Tamil/English phone call becomes a routed, tracked civic
grievance. **Verified in production** — real calls have filed real tickets on the live dashboard.

---

## 1. Live topology (what runs where)

```
 ┌───────────┐   phone call (Tamil/Tanglish)
 │  CITIZEN  │────────────────────────────────┐
 └───────────┘                                 ▼
                                   ┌──────────────────────────────┐
                                   │  BOLNA  (hosted voice agent)  │
                                   │  Sarvam/Soniox ASR  ──►  LLM  │
                                   │  (azure gpt-4.1-mini) ──► TTS │
                                   │  Cartesia Sonic-3 (Tamil)     │
                                   └───────────┬──────────────────┘
                     tool call: file_grievance │ (GET, confirmed fields)
                     post-call: /call-webhook  │
                                               ▼
                           ┌──────────────────────────────────────┐
                           │  KURAL BRAIN  (FastAPI on Render)     │
                           │  kural-brain.onrender.com             │
                           │  /file  /grievance  /area-status      │
                           │  /ticket-status  /call-webhook  /api* │
                           │                                       │
                           │  normalize → classify → RESOLVE owning│
                           │  body (31 sectors × city × region)    │
                           │  → billing anomaly → dedup-merge →    │
                           │  ticket + SLA → office dispatch → SMS │
                           │  → KuralEval (per-call scorecard)     │
                           └───────────┬───────────────┬──────────┘
                                       │               │
                                 SQLite DB        Plivo SMS (citizen)
                                       │
                                       ▼
                           ┌──────────────────────────┐
                           │  DASHBOARD  (served at /) │  live tickets, hotspots,
                           │  Tailwind SPA             │  billing over-charge, eval
                           └──────────────────────────┘

 Source: github.com/hxshxnsivx-hub/Bolna-Buildathon  →  auto-deploys to Render on push
```

---

## 2. The end-to-end call flow (one real grievance)

```
1. Citizen dials the Bolna number (or web-call).
2. Agent greets in Tamil: "வணக்கம்! நான் Kural..."
3. Citizen speaks freely in Tanglish; Bolna streams ASR → LLM each turn.
4. LLM extracts { sector, locality, severity, (bill: units/charged/expected) },
   asks ONE clarifying question if the place/name is unclear.
5. Agent CONFIRMS back in the caller's language → repair loop if wrong.
6. On "yes" → LLM calls tool file_grievance (GET /file?sector=...&locality=...).
7. BRAIN:  normalize_sector → resolve(sector × city × region) → owning body +
   dept + channel + SLA ; if electricity bill → billing.analyze (over-charge +
   anomaly) ; dedup-merge against open tickets ; create ticket + SLA clock ;
   dispatch report to the office ; Plivo SMS to the citizen.
8. BRAIN returns { ticket_id, owning_body, sla_days, spoken_confirmation, over-charge }.
9. Agent reads the ticket number back in Tamil; closes the call.
10. On hangup → Bolna POSTs /call-webhook → KuralEval scores the call
    (ASR / language-switch / language-match / task / repair).
11. DASHBOARD reflects every ticket + score live.
```

**Verified live:** calls have produced e.g. `KRL-2026-00001 · electricity · coimbatore → TNPDCL`
and a water-supply grievance — the agent→brain→ticket→dashboard loop works end to end.

---

## 3. The capability pipeline (what the brain does, in order)

| Stage | Module | What it does |
|---|---|---|
| 1. Understand | Bolna LLM / `app/nlu.py` | Tanglish speech → `{sector, locality, severity, billing?}` |
| 2. Normalize | `routing.normalize_sector` | "water supply"/"Power"/"garbage" → canonical key |
| 3. Resolve | `app/routing.py` | **31 sectors × city × region → owning body, dept, cadre, channel, SLA** (deterministic, auditable) |
| 4. Billing | `app/billing.py` | electricity bill: expected vs charged → over-charge + anomaly flag |
| 5. Dedup | `app/service.py` + `db` | merge repeat callers of same issue+area → one ticket, reporter count, hotspot ≥3 |
| 6. Ticket + SLA | `app/sla.py` + `db` | business-day due date; tiered escalation ward→zonal→regional→commissioner |
| 7. Dispatch | `app/dispatch.py` | report "filed to <office>"; Plivo SMS to citizen |
| 8. Autonomy tools | `/area-status`, `/ticket-status` | "already N reported?"; returning-caller status lookup |
| 9. Quality | `app/eval.py` (KuralEval) | per-call vernacular QA: ASR, language-switch, **language-match**, task, repair |
| 10. Present | `web/index.html` | live dashboard: tickets, routing chart, hotspots, over-charge badges, eval |

Anything unmapped → **CM Helpline 1100** fallback, so the router is *always* valid.

---

## 4. Deployment & CI workflow

```
code (local)  ──git push──►  GitHub (main)  ──auto-deploy──►  Render (kural-brain)
    │                                                              │
    └─ pytest (21 tests: routing, billing, dedup, SLA, eval,       └─ serves API + dashboard
       sector coverage, autonomy tools) — green before push           + Bolna webhooks (HTTPS)
```
- **Secrets** via env (never committed): `LLM_API_KEY`, `PLIVO_*` — all optional (offline fallbacks).
- **Bolna** holds the agent config (prompt + 3 tools → the live `/file`, `/area-status`,
  `/ticket-status` + post-call `/call-webhook`).

---

## 5. Status

| Layer | State |
|---|---|
| Brain (routing, billing, dedup, SLA, tools, eval) | ✅ built, 21 tests, deployed |
| Dashboard | ✅ live at `/` |
| GitHub + Render (auto-deploy) | ✅ live |
| **Bolna voice agent** | ✅ **wired — real calls file tickets** |
| Plivo phone number (inbound) | ⬜ after KYC (web-call works now) |
| Post-call eval webhook | ⚠️ verify it fires on call end (tickets confirmed; eval rows to confirm) |
| Demo video + submission | ⬜ final step |

**Open items:** confirm the Bolna post-call webhook reaches `/call-webhook` (so KuralEval scores
populate); attach a Plivo number once KYC clears; record the demo.
