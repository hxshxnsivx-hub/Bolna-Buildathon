# Kural — System Architecture & Design (the spine)

**Goal:** a 10/10, buildathon-grade design for Kural — an autonomous Tamil/English (Tanglish) voice
agent that takes a civic grievance call, understands it, resolves the owning body + department,
files a tracked ticket with an SLA clock, notifies the citizen, and (the hiring-signal layer) scores
its own call quality. Designed so the **spine is solid** and features bolt on without rework.

---

## 1. Design principles (why this is a 10/10, not just a diagram)

1. **Separation of concerns — 4 independent layers:** *voice runtime* (telephony + ASR/LLM/TTS),
   *business brain* (extraction + routing + ticket + SLA), *presentation* (dashboard), *quality*
   (eval). Each is swappable and testable alone. The agent talks to the brain over a **thin webhook /
   tool-call contract** — so your logic is portable off any vendor.
2. **Stateless agent, stateful backend.** The agent holds only live conversation state; all tickets,
   SLA timers, clusters, and transcripts live in the backend DB. → reliable, demoable, replayable.
3. **Probabilistic understanding, deterministic routing.** The LLM *extracts & classifies* (fuzzy
   Tanglish); the **owning-body resolution is a deterministic lookup table** (auditable, always
   correct). This is the detail most demos get wrong — never let the LLM guess who owns the issue.
4. **Confirm-before-commit.** The agent always reads the parsed grievance back in the caller's
   language and offers one repair turn before a ticket is created. Trust + a visible "repair loop."
5. **Graceful degradation.** Low ASR confidence → re-ask; backend down → queue-and-forward
   (offline-first hook); unknown sector → safe fallback to CM Helpline 1100 routing.
6. **Hard MVP/vision boundary.** The spine ships in 48 h; the ambitious parts are *shown*, not built
   (see §7).

---

## 2. Component architecture (layers)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CITIZEN (phone call, Tamil/English)                                      │
└───────────────┬───────────────────────────────────────────────────────────┘
                │ PSTN / inbound DID
┌───────────────▼─────────────── LAYER 1 · TELEPHONY & MEDIA ───────────────┐
│  • Inbound number (DID), 8 kHz audio bridge, SMS egress                    │
│  • Provider: [telephony]  (council to decide)                             │
└───────────────┬───────────────────────────────────────────────────────────┘
                │ media stream (websocket)
┌───────────────▼─────────────── LAYER 2 · VOICE ORCHESTRATION ─────────────┐
│  Streaming pipeline:  ASR ──► LLM/NLU ──► TTS   (barge-in, turn-taking)    │
│  • Session/turn state, interruption handling, endpointing                 │
│  • Provider/runtime: [voice stack]  (council to decide)                   │
└───────────────┬───────────────────────────────────────────────────────────┘
                │ tool-calls / webhook  (the contract, §4)
┌───────────────▼─────────────── LAYER 3 · BUSINESS BRAIN (your code) ───────┐
│  (a) Extractor/Classifier → {sector, locality, severity, citizen}          │
│  (b) Ownership Resolver  (sector × location) → {body, dept, cadre, zone,    │
│                                                  channel, SLA}  [DETERMINISTIC]│
│  (c) Dedup/Cluster  (body × locality × sector)        [stretch]             │
│  (d) Ticketing + SLA engine  (create, clock, escalate)                     │
│  (e) Dispatch  (SMS to citizen, report to office)                          │
└──────┬───────────────────────────────────┬────────────────────────────────┘
       │                                    │
┌──────▼─────── LAYER 4 · DATA ───────┐  ┌──▼─────── LAYER 5 · PRESENTATION ───┐
│  tickets · reporters · clusters ·   │  │  Ops dashboard: live tickets →      │
│  sla_timers · calls · transcripts   │  │  sector → body/dept → zone → status │
│  [datastore — council to decide]    │  │  → SLA countdown · hotspot view     │
└──────┬──────────────────────────────┘  └─────────────────────────────────────┘
       │ transcripts + recordings + traces
┌──────▼─────────────────── LAYER 6 · KuralEval (quality / hiring signal) ────┐
│  Per-call scorecard: ASR/language-switch correctness · intent/task          │
│  completion · confirm-repair success · latency · hallucination/compliance   │
│  flags → agent-health dashboard. (LLM-as-judge over each call.)             │
└─────────────────────────────────────────────────────────────────────────────┘
          ▲ SLA monitor (scheduler) drives escalation ward→zonal→regional→commissioner
```

---

## 3. Runtime sequence (one call, end to end)

```
1. Citizen dials DID ─► Telephony answers ─► bridges audio to Voice Orchestration.
2. Agent greets (Tamil): "வணக்கம், நான் Kural. உங்க புகாரை சொல்லுங்க."
3. Citizen speaks Tanglish grievance (free-form).
4. ASR (streaming) ─► LLM extracts {sector, locality, severity, name/addr}.
5. Agent CONFIRMS back in caller's language; caller corrects → repair loop.
6. On confirm → tool-call → Brain:
      Resolver(sector, locality) → {body, dept, cadre, zone, channel, SLA_days}
      Ticket.create(...) → ticket_id ; SLA clock starts ; (cluster check)
7. Agent speaks ticket_id + expected SLA ; Dispatch sends SMS (Plivo) + office report (stub).
8. Hangup → recording + transcript persisted → KuralEval scores the call.
9. Scheduler watches SLA; on breach or hotspot cluster → escalate + notify.
10. Dashboard reflects every step live.
```

---

## 4. The key interface — Agent ⇄ Brain contract (keep this stable)

The agent calls the backend with a single structured payload (LLM function-call / webhook). This
contract is the backbone — vendors above it can change without touching your logic.

```jsonc
// POST /grievance   (agent → brain, on confirm)
{
  "call_id": "c_01H…",
  "caller": { "name": "…", "phone": "+91…", "raw_address": "…" },
  "utterance": "road-la பெரிய pothole, bike விழுந்துடுச்சு",
  "extracted": {
    "sector": "roads_internal",          // from dossier-04 taxonomy
    "locality": { "text": "Velachery 6th St", "ward": null, "zone": null },
    "severity": "high",
    "language_mix": ["ta","en"]
  }
}
// ← response (brain → agent)
{
  "ticket_id": "KRL-2026-00042",
  "owning_body": "GCC",
  "department": "Engineering",
  "field_cadre": "Junior Engineer",
  "zone": "Zone-13 (Adyar)",
  "channel": "1913",
  "sla_days": 3,
  "sms_sent": true,
  "duplicate_of": null
}
```

## 5. Data model (minimal, sufficient)

```
tickets(id, call_id, sector, owning_body, department, cadre, zone, locality,
        severity, status, sla_days, due_at, created_at, cluster_id)
reporters(id, ticket_id, name, phone, raw_address)
calls(id, phone, started_at, ended_at, recording_url, transcript, lang_mix)
clusters(id, body, locality, sector, count, is_hotspot)           -- stretch
sla_events(id, ticket_id, level, fired_at)                        -- escalation log
eval_scores(id, call_id, asr_ok, lang_switch_ok, task_complete,
            repair_ok, latency_ms, hallucination_flag, compliance_flag, notes)
```

## 6. Cross-cutting
- **Observability:** every call → recording + transcript + timing trace (feeds KuralEval).
- **Config-driven agent:** system prompt + the routing table as data (dossier 04), not hardcode.
- **Security/PII:** phone/address are personal → store minimally, no secrets in logs, test data only.

## 7. Scope boundary — BUILD vs SHOW (protects the 48 h)

| | Build now (the spine) | Show as roadmap (narrate, don't code) |
|---|---|---|
| Voice | Tanglish intake + confirm/repair + 1 urban + 1 rural call | emotion detection, full barge-in tuning |
| Brain | extractor + **deterministic resolver** + ticket + SLA start | dedup clustering, full ward→commissioner escalation |
| Dispatch | **SMS to citizen** | WhatsApp/email to office, IIPGCMS API integration |
| Data | SQLite/managed table | multi-corporation, offline queue-and-forward |
| Eval | per-call scorecard on the demo calls | agent-health trends, auto prompt-fix (self-healing) |

---

## 8. What the council decides (next)
The architecture is **vendor-agnostic by design**. The open slots are: **[telephony]**, **[voice
orchestration/runtime]**, **[ASR]**, **[TTS]**, **[LLM]**, **[backend]**, **[datastore]**,
**[dashboard]**, **[deploy]**. The 3-agent advocate council argues three whole-stack philosophies for
filling these in 48 h; verdict appended as `docs/architecture/02-tech-stack-decision.md`.
