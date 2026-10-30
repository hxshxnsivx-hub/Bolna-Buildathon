# Kural — Phase 4 Go-Live Runbook (voice)

Everything here is ready in code; this is the checklist to flip Kural from the offline demo to a
real inbound Tanglish call once your accounts/credits clear. Order matters (KYC is the long pole).

## 0. Accounts
- **Plivo** (telephony + SMS) — start India-number KYC **first** (can take a business day).
- **Bolna** (orchestration) — Agent Studio.
- **Sarvam** (ASR Saaras + TTS Bulbul) · **Cartesia** (low-latency TTS).
- **LLM** — a free key is fine: Google **Gemini** (AI Studio) or **Groq**. No OpenAI needed.

## 1. Pick an LLM (no OpenAI required)
Set env on the deploy (and locally in `.env`). Examples in `.env.example`:
```
LLM_API_KEY=<your key>
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/   # Gemini
LLM_MODEL=gemini-2.0-flash
```
Blank = Kural still runs on its heuristics. `app/llm.py` is OpenAI-compatible, so Groq/Gemini/Sarvam-M all work by just changing these three.

## 2. Deploy the brain (get a public HTTPS URL)
Bolna must reach your webhooks over HTTPS. Pick one:
- **Render** — repo → New Web Service → **Root Directory = `kural`** → it reads `render.yaml`.
  Add the secret env vars in the dashboard.
- **Railway** — new project from repo, root `kural`, uses `Procfile`.
- **Docker** — `docker build -t kural kural/ && docker run -p 8000:8000 --env-file kural/.env kural`.
Verify: open `https://<deploy-url>/` (dashboard) and `https://<deploy-url>/health` → `{"ok":true}`.

> SQLite is ephemeral on free hosts (resets on redeploy) — fine for the demo. Swap to Supabase/
> Postgres later (schema in `app/db.py`) if you need persistence.

## 3. Build the Bolna agent (Agent Studio)
1. New agent; paste `kural/agent/system_prompt.md` as the system prompt.
2. **Transcriber:** Sarvam `saaras` (language `ta`, streaming).
3. **Synthesizer:** Cartesia `sonic` (`ta`); set Sarvam `bulbul` as fallback.
4. **LLM:** your chosen model (reliable function-calling — Gemini/Groq/GPT all fine).
5. **Tool / custom function** `file_grievance` → `POST https://<deploy-url>/grievance`
   (schema in `kural/agent/bolna_agent.json`). Agent calls it after the caller confirms.
6. **Post-call webhook** → `POST https://<deploy-url>/call-webhook`.
7. Attach the Plivo number to the agent.

### Payloads (what Bolna sends — already matches the brain)
`file_grievance` body:
```json
{ "call_id": "...", "utterance": "road-la pothole, bike விழுந்துடுச்சு",
  "caller": { "name": "...", "phone": "+91...", "raw_address": "..." },
  "extracted": { "sector": "roads_internal", "severity": "high",
                 "locality": { "text": "Velachery 6th St", "region": "chennai" } } }
```
Post-call webhook (include **speaker-tagged `turns`** so KuralEval can score language-match):
```json
{ "call_id": "...", "phone": "+91...", "transcript": "full text",
  "latency_ms": 680, "lang_mix": ["ta","en"],
  "turns": [ {"speaker":"user","text":"..."}, {"speaker":"agent","text":"..."} ] }
```

## 4. Smoke-test Sarvam Tanglish (30 min, before the real call)
Record 15–20 real code-mixed grievance clips over an 8 kHz path; push through Sarvam; confirm the
sector/locality come out right. This is the make-or-break for the demo — do it early.

## 5. Live call → verify the loop
Call the Plivo number, speak a Tanglish grievance, confirm. Then check:
- a **ticket** appears on the dashboard, routed to the correct body/dept with an SLA clock,
- a **confirmation SMS** arrives,
- a **KuralEval** scorecard row shows (mix / match / task).

## Fallbacks (keep the demo safe)
- **No India number in time:** demo via Bolna's web-call widget or an outbound call to your own
  phone — the full pipeline is identical; the number becomes a "production-ready" talking point.
- **Self-host latency issues:** stay on Bolna hosted (that's the plan) — same prompts, same tools.
- Never commit `.env` (it's gitignored). Rotate any key that leaks.
