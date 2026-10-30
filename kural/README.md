# Kural (குரல்) — Tamil/English Civic Grievance Voice Router

An autonomous **Tanglish voice agent** for Tamil Nadu civic grievances: a citizen calls a number,
speaks their complaint in code-mixed Tamil/English, and Kural understands it, **resolves which of
the ~5 government bodies + department actually owns it**, files a tracked ticket with an SLA clock,
texts the citizen, and (the hiring-signal layer) **scores its own call quality**.

Built for the Bolna × Plivo Symphony Buildathon. Stack decided in
[`docs/architecture/02-tech-stack-decision.md`](../docs/architecture/02-tech-stack-decision.md);
design in [`docs/architecture/01-kural-system-design.md`](../docs/architecture/01-kural-system-design.md).

> **Runs fully offline out of the box.** With no API keys, SMS is logged and the eval uses a
> heuristic — so you can demo the whole loop (voice stack aside) on your laptop immediately.

## Quickstart (text-demo mode — no telephony, no keys)

```bash
cd kural
python -m venv .venv && . .venv/Scripts/activate      # Windows; use .venv/bin/activate on mac/linux
pip install -r requirements.txt
python scripts/seed.py                                 # sample tickets + a hotspot + eval rows
uvicorn app.main:app --reload                          # brain + dashboard on http://localhost:8000
# open the dashboard in a browser:  http://localhost:8000
# in a 2nd terminal, fire Tanglish complaints at the brain:
python scripts/demo_call.py
```

The dashboard is a self-contained **Tailwind** single-page UI (`web/index.html`) served by FastAPI
at `/` — live tickets, SLA countdowns, routing chart, KuralEval panel, hotspot alerts, and an inline
"file a complaint" box. No build step, no npm.

Then try your own: `python scripts/demo_call.py "Enga street-la pothole, bike விழுந்துடுச்சு"`

## Going live (voice) — the real demo
1. Fill `.env` (copy from `.env.example`): add `OPENAI_API_KEY` (eval + classification),
   `PLIVO_*` (SMS), optionally Sarvam/Cartesia keys in Bolna.
2. Deploy the brain (Render/Railway) to get a public HTTPS URL.
3. In **Bolna Agent Studio**, create an agent from `agent/system_prompt.md`, set
   transcriber=Sarvam, synthesizer=Cartesia (fallback Sarvam Bulbul), LLM=GPT-4o, telephony=Plivo,
   and add the `file_grievance` tool → `https://<deploy>/grievance` (see `agent/bolna_agent.json`).
   Set the post-call webhook → `https://<deploy>/call-webhook`.
4. Point a Plivo number at the agent and call it.

## Day-0 actions (from the stack risk register)
- **Start Plivo India KYC now** (can take a business day); keep a web-call/outbound fallback so the
  number is never on the critical path.
- **30-min Tanglish smoke test** through Sarvam before committing.
- Use **GPT-4o** for the tool-call (Sarvam function-calling in Bolna is unconfirmed).

## What's built vs shown
- **Built & runnable:** voice→(classify)→**deterministic routing**→ticket→SLA→SMS→dashboard→eval.
- **Shown/roadmap (stubs in place):** duplicate clustering (cluster_key + hotspot count are live),
  full ward→commissioner escalation (`app/sla.py` computes the level), WhatsApp/office dispatch,
  IIPGCMS integration.

## Layout
```
app/        routing.py (the deterministic resolver) · main.py (FastAPI) · nlu.py · eval.py
            db.py · models.py · sla.py · sms.py
web/        index.html (Tailwind ops dashboard, served at / )
agent/      system_prompt.md (Tanglish) · bolna_agent.json
scripts/    seed.py · demo_call.py
```

## The core idea
**Probabilistic understanding, deterministic routing.** The LLM handles the fuzzy Tanglish; the
owning-body resolution is a plain, auditable lookup table (`app/routing.py`) seeded from the R&D
dossiers — so Kural never *guesses* who owns a pothole.
