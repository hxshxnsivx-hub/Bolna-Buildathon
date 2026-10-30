# Phase 4 — Bolna Agent Wiring (step by step)

Wire the Kural voice agent in **Bolna Agent Studio** against your live brain
**`https://kural-brain.onrender.com`**. You can do steps 1–5 now with the $10 credit and test via
Bolna's web/test call — **no Plivo number needed** until step 6.

> Cold-start note: the free Render instance sleeps after ~15 min idle. **Open
> `https://kural-brain.onrender.com/health` once to wake it** before testing a call.

## 1. Create the agent
Bolna dashboard → create a new agent ("Kural"). Paste **`kural/agent/system_prompt.md`** as the
system prompt (the Tanglish persona + the confirm-before-file flow).

## 2. Voice stack
- **Transcriber (STT):** Sarvam **Saaras** — language `ta`, streaming on.
- **Synthesizer (TTS):** **Cartesia Sonic** (`ta`); keep Sarvam **Bulbul** as the fallback voice.
- **LLM:** any function-calling model — GPT-4o, or your free Gemini/Groq key.

## 3. Add the tool `file_grievance` (this is the integration)
Add a **custom function** (Bolna `custom_task`). Full JSON in `kural/agent/bolna_agent.json`; the key parts:
- **name:** `file_grievance`
- **description:** "Call AFTER the caller confirms. Files the civic grievance, returns a ticket number + owning body. Use for water, power, garbage, road, streetlight, drainage, etc."
- **parameters (flat):** `sector, locality, region, severity, name, phone, utterance` (required: `sector`, `locality`)
- **key:** `custom_task`
- **value:** `method = GET`, and **url** = your live flat endpoint with templated params:
  ```
  https://kural-brain.onrender.com/file?sector=%(sector)s&locality=%(locality)s&region=%(region)s&severity=%(severity)s&name=%(name)s&phone=%(phone)s&utterance=%(utterance)s
  ```
- **param:** map each name to `%(name)s` (matching the properties above).

The brain replies with the `ticket_id`, `owning_body`, and a Tanglish `spoken_confirmation` — the
agent reads the ticket number back to the caller.

> Why `/file` and not `/grievance`? Bolna's custom_task sends **flat** params via the URL; `/file`
> accepts them and maps to the internal contract. (`/grievance` is the nested JSON contract for
> non-Bolna callers.) If Bolna URL-encodes spaces oddly, test with a single-word locality first.

## 4. Post-call webhook (powers KuralEval)
Set the agent's **post-call webhook** → `https://kural-brain.onrender.com/call-webhook`. If Bolna
lets you include the transcript and speaker-tagged turns, do so — that enables the `lang_match`
(wrong-language) scoring. (Alternatively pull transcripts via Bolna's `get-executions` later.)

## 5. Test WITHOUT a phone number (do this first)
Use Bolna's **web call / test call** in the dashboard. Speak a Tanglish grievance, e.g.:
- *"Anna Nagar West-la தண்ணி வரலை, 4 naal aachu"* → should route to **CMWSSB**, SLA 1d.
- *"Enga street-la current போச்சு, transformer spark"* → **TNPDCL**.
Let it confirm back, then open **`https://kural-brain.onrender.com`** — the ticket should appear with
the correct owning body + SLA, and a KuralEval row after the call ends.

## 6. Go live on a phone number (after Plivo KYC clears)
1. In the Bolna agent, copy its **Inbound API URL**.
2. Plivo Console → **Voice → XML Application** → create one; paste the Bolna URL into **both**
   **Primary Answer URL** and **Hangup URL**; save.
3. Plivo → **Active Numbers** → pick your number → set the XML Application → **Update Number**.
4. Call the number → it connects to Kural.

## Checklist
- [ ] Agent created, system prompt pasted
- [ ] Sarvam STT + Cartesia TTS + LLM set
- [ ] `file_grievance` custom_task → `/file` URL
- [ ] post-call webhook → `/call-webhook`
- [ ] web-call test → ticket shows on the dashboard
- [ ] (later) Plivo number attached + live call

Docs: [Bolna custom functions](https://www.bolna.ai/docs/tool-calling/custom-function-calls) ·
[Plivo inbound calls](https://www.bolna.ai/docs/guides/telephony/plivo-inbound-calls) ·
[Using Plivo](https://www.bolna.ai/docs/plivo)
