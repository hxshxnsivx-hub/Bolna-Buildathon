# Kural — Tech-Stack Decision (Chair's Verdict)

Three advocate agents argued three whole-stack philosophies against the system architecture
(`01-kural-system-design.md`). This is the adjudication. _Decided 2026-10-29._

- **Advocate A** — *Ship fastest, Bolna-hosted* (Bolna Agent Studio managed runtime)
- **Advocate B** — *Fork & self-host `bolna-ai/bolna`* (build inside the employer's codebase)
- **Advocate C** — *Best-of-breed* (LiveKit/Pipecat + Cartesia, max latency control)

---

## 1. Where the council AGREED (locked, no debate)

All three independently converged here — so these are settled:

| Layer | Locked choice | Rationale (unanimous) |
|---|---|---|
| **Telephony + SMS** | **Plivo** | Co-sponsor; India inbound; same creds for SMS. |
| **ASR (Tamil/Tanglish)** | **Sarvam Saaras** (v3/v4, auto language-detect, telephony-trained) | Only Indic-first, code-mix-tuned, telephony-grade option; a sponsor. |
| **Dialogue + extraction LLM** | **GPT-4o** (function-calling) — Claude as alt | Reliable JSON/tool-calling to emit `{sector, location, severity}` and hit the brain. |
| **Business brain** | **Python FastAPI** + **deterministic routing table** | Owning-body resolution is a lookup table, never an LLM guess — auditable, demo-safe. |
| **Eval layer (KuralEval)** | **LLM-as-judge** over Bolna's **post-call webhook** (transcript + metadata) | The hiring-signal differentiator, built cheaply from data you already receive. |

> The deterministic routing table + the eval-from-webhook were endorsed by **all three** advocates —
> treat them as the non-negotiable core of Kural.

---

## 2. The one real contest — the orchestration layer

This was the whole debate. Verdict first, then why.

### 🏆 Verdict: **Advocate A — Bolna's hosted runtime (Agent Studio) — wins as the core**, with two borrowings.

**Final stack:**
- **Orchestration:** **Bolna hosted (Agent Studio)** — managed ASR→LLM→TTS streaming, barge-in/VAD/turn-taking you don't build.
- **TTS:** **Cartesia Sonic** (borrowed from C — lowest time-to-first-audio, Tamil confirmed) **A/B against Sarvam Bulbul** (more native Tamil timbre); pick by ear on the demo call.
- **Datastore:** **SQLite** (ship-fast) → upgrade to **Supabase** only if you want the dashboard ticket to pop in realtime during the call.
- **Dashboard:** **Streamlit** (≈40 lines, no frontend toolchain) — the speed pick.
- **Deploy:** **Render/Railway** (one `git push`, public HTTPS webhook URL).
- **Hiring-signal borrow from B:** you don't fork the repo, but you **read `bolna-ai/bolna` and say so** — your README/pitch references their orchestrator architecture and how you'd extend it (offline-first, barge-in tuning). You get B's "I understand your codebase" signal without B's Day-1 Docker risk.

**Net custom surface you actually write:** one FastAPI app + one Streamlit file + one routing table + the Tanglish prompts. That's it.

### Why A over B (the closest call)
B's thesis is "forking your codebase is the hiring signal." True — but the Bolna role you can realistically land is the **AI Solutions Engineer** (early-career, *"no heavy coding needed,"* prompt + call-review + vernacular testing — dossier 05). That JD is served **better** by a flawless hosted agent + a rigorous eval than by a risky infra fork. And B's own brief admits the **Day-1 Docker/ngrok/redis window is "make-or-break"** — that's exactly the time that should go into the call quality you're judged on. B's best ideas (deterministic routing, eval, sponsor lock-in) are **already in A**. You keep B's narrative edge by *reading* the repo, not betting the weekend on self-hosting it.

### Why A over C
C has the best audio *ceiling* but the worst 2-day *floor*: a 5-vendor SIP↔orchestrator↔ASR↔LLM↔TTS chain is the largest failure surface under deadline, and it's the **least Bolna-aligned** stack in a contest Bolna judges. We **borrow C's one decisive insight — Cartesia for low-latency TTS** — into A, getting the audio win without the integration risk. (Keep Vapi/LiveKit in your back pocket only as a written "here's the alternative I considered.")

### The principle behind the verdict
> In a 48-hour build judged on *how the call sounds*, by the *vendor whose platform it is*, with a
> solo builder at *zero code*: **minimize failure surface, buy call quality, align with the host, and
> spend every saved hour on Tanglish prompt craft + the eval.** A does that; B and C spend scarce
> hours proving infra skill this specific role doesn't primarily hire for.

---

## 3. The final locked stack (one glance)

```
Telephony/SMS … Plivo
Orchestration … Bolna hosted (Agent Studio)         [barge-in/turn-taking: bought]
ASR ………………… Sarvam Saaras (ta, auto-detect, streaming)
TTS ………………… Cartesia Sonic  ⇄ A/B ⇄  Sarvam Bulbul
LLM ………………… GPT-4o (function-calling)  [Claude alt]
Brain …………… Python FastAPI = extractor + DETERMINISTIC routing table + ticket + SLA
Data …………… SQLite  (→ Supabase if realtime dashboard wanted)
Dashboard …… Streamlit  (→ React+Supabase if time)
Eval …………… LLM-as-judge on Bolna post-call webhook
Deploy ……… Render / Railway
```

---

## 4. Risk register + Day-0 actions (all three advocates flagged these)

| Risk | Mitigation (do on Hour 0) |
|---|---|
| **Plivo India number KYC** can take a business day / reject | Start KYC immediately **and** demo via Bolna web-call widget or outbound-to-your-own-phone — the number is then a "production-ready" talking point, never a blocker. |
| **Tanglish ASR accuracy is a vendor claim** (no published WER) | **30-min smoke test**: push 15–20 real Tanglish grievance clips through Sarvam Saaras before committing. Go/no-go. |
| **Sarvam-LLM function-calling unconfirmed inside Bolna** | Use **GPT-4o** for the tool-call; Sarvam for STT/TTS only. |
| **Tamil TTS prosody** uncertain | A/B Cartesia vs Sarvam Bulbul early; pick by ear. |
| No working call by end of Day 1 | Cut line: one Sarvam ASR + Cartesia TTS, drop A/B, keep the live call + dashboard + one scorecard. |

---

## 5. Bottom line
The spine (`01`) is vendor-agnostic; this verdict fills it with the **lowest-risk, most
Bolna-aligned, fastest-to-a-good-call** stack, and borrows Cartesia's latency and B's codebase
narrative to cover A's only weak spots. **The stack is decided. The next action is to scaffold the
FastAPI brain + routing table + Streamlit dashboard and configure the Bolna agent — i.e., start
building.** No further stack analysis is needed.
