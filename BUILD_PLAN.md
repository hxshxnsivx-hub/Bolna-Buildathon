# Symphony Buildathon — 48-Hour Build Plan

> **Deadline: Oct 31, 2026 (submissions close).** Today is **Oct 29**. You have ~2 days.
> **Step 0, do it right now:** register at https://www.bolna.ai/symphony/buildathon and join the Bolna Slack (bolna.ai/join-slack). Nothing below matters if you miss the form.

---

## The product

**Working name: `Kural`** (குரல் = "voice" in Tamil; also nods to Thirukkural). Alt: *Makkal Kural* ("people's voice").

**One line:** A callable Tamil/English civic-grievance line — a citizen calls, speaks their complaint naturally in Tanglish, the agent confirms it back in their language, classifies it, routes it to the right department, and texts them a ticket ID.

This is an adaptation of your existing **offline-first TN grievance router / Tamil–English voice intake / cross-agency routing** project. The rules explicitly allow "a voice layer on something you've already built" — so you are *not* starting from zero, and that is your biggest unfair advantage.

### Call flow (the demo spine)
1. Citizen calls a phone number.
2. Agent greets in Tamil + English, asks them to describe the problem.
3. Citizen speaks code-mixed: *"Enga street la street light two weeks-a work aagala."*
4. STT → LLM extracts `{issue_type, location, urgency}`.
5. **Agent confirms back in the caller's language** and offers repair: *"Street light repair, [area]-la — correct-ah?"*
6. On "yes": classify → department (e.g., TNEB / Municipal Corp / Water Board), generate `ticket_id`, store.
7. **SMS confirmation** with the ticket ID (Plivo SMS).
8. Dashboard shows: complaint → category → department → ticket → status.

### Why this is the one that wins *and* gets you hired
- **Vernacular + code-mixing** is Bolna's exact moat; most teams will ship a generic English GPT-voice toy.
- **It completes a task** (routes + files), not just chats. Judges remember "it actually did something."
- **Callable + a dashboard** = proof, not slides.
- **India-scale, social-impact** narrative maps 1:1 onto their "next billion" thesis.
- Built on *their* stack → direct hiring signal.

---

## Scope discipline (read this before you build anything)

**MUST (the demo fails without these):**
- One phone number that answers.
- Tamil/English code-mixed understanding of a spoken complaint.
- Spoken confirmation + one repair turn ("did you mean…?").
- Classification → department routing → ticket ID.
- A visible result (SMS and/or dashboard row).

**NICE (add only if MUST is solid):**
- Sub-second latency tuning + barge-in / interruption handling.
- Mid-call language auto-switch.
- Status lookup ("call back, say ticket number, hear status").

**CUT (do NOT build in 48h — mention in pitch instead):**
- Real government API integration.
- Full offline sync engine (describe it; show the architecture).
- Auth / user accounts / multi-tenant.
- Anything that isn't on screen in the demo video.

> **Depth beats breadth.** Pick ONE hard thing — the code-mixed confirm-and-repair loop — and make it genuinely good. That single axis is what separates a winner from a demo.

---

## Tech stack (optimized for speed + sponsor-points)

| Layer | Use | Why |
|---|---|---|
| **Voice agent** | **Bolna agent builder** | Fastest multilingual path; building on the organizer's stack is a hiring signal. Confirm telephony + webhook/"tool" support in their docs/Slack first. |
| **Telephony / SMS** | **Plivo** (number, inbound call, SMS) | It's the Buildathon partner. ⚠️ Indian numbers need KYC and can take days — see risks. |
| **STT / TTS (Indic)** | **Sarvam** (or Deepgram for STT, Cartesia for low-latency TTS) | All are sponsors; Sarvam is strongest on Indian languages. |
| **Routing logic + ticket store** | Small webhook backend (FastAPI/Express) + SQLite/Supabase | Reuse your civic-services classification/routing code here. |
| **Dashboard** | One page (Streamlit / Next.js) reading the ticket store | The "it did something" visual. |
| **Deploy** | Render / Railway / Fly.io | Keep the webhook + dashboard live for the demo. |

> You don't need to confirm exact Bolna/Plivo API shapes from memory — pull them from their docs and ask in Slack. Being active in Slack is itself part of the recruiting play.

---

## The 48-hour timeline

### Phase 0 — Setup (Hr 0–2)
- [ ] Register for the buildathon. Join Slack.
- [ ] Create accounts: Bolna, Plivo, Sarvam/Deepgram.
- [ ] **Start the Plivo number / KYC process immediately** (slowest item — unblock it first).
- [ ] Pull your civic-services repo; isolate the classification/routing logic.

### Phase 1 — Voice spine (Hr 2–8)
- [ ] Configure Bolna agent: system prompt, Tamil+English, greeting.
- [ ] Wire STT/TTS (Sarvam for Indic).
- [ ] Get **one full call working**: call in → agent speaks → you speak → it responds.
- [ ] Test with real code-mixed sentences; fix the obvious failures.

### Phase 2 — The task logic / your differentiator (Hr 8–16)
- [ ] Webhook: receive transcript → extract `{issue, location, urgency}` → classify → `ticket_id` → store. (Reuse civic-services code.)
- [ ] Add the **confirmation + repair** turn in the agent.
- [ ] Fire **Plivo SMS** on confirmation.

### Phase 3 — Depth polish (Hr 16–24)
- [ ] Latency pass (<1s target).
- [ ] Barge-in / interruption handling.
- [ ] Edge cases: silence, unclear input, "no that's wrong" → re-ask gracefully.
- [ ] (Nice) mid-call language switch.

### Phase 4 — Proof surface (Hr 24–30)
- [ ] Dashboard: live table of complaint → department → ticket → status.
- [ ] Seed 4–5 realistic sample complaints so it looks alive.

### Phase 5 — Demo + narrative (Hr 30–38)  ← highest leverage
- [ ] **Record a 2.5-min demo video** (script below). This is what the virtual round is judged on.
- [ ] Clean README with the architecture diagram + the offline-first/cross-agency story.
- [ ] Deploy backend + dashboard; keep the number live.

### Phase 6 — Submit (Hr 38–44)
- [ ] Make GitHub repo public.
- [ ] Fill the submission form (copy below). **Submit a full day early**, not at the cutoff.
- [ ] Update LinkedIn so the Bolna team can find you.

### Phase 7 — Buffer + visibility (Hr 44–48)
- [ ] Fix anything broken; re-record if needed.
- [ ] Post your build in Slack / tag Bolna. Be a visible, generous community member.

---

## Submission form copy (draft — edit the specifics)

**Project name:** Kural — a Tamil/English civic-grievance voice line

**What are you building, and where does voice AI fit?**
> Kural is a phone line for citizens to file municipal grievances by *speaking* — in natural Tamil–English code-mixed speech, the way people actually talk. Voice is the entire product: a caller describes a problem ("the street light has been out for two weeks"), the agent confirms it back in their own language, extracts the issue, location and urgency, routes it to the correct department, and texts back a ticket ID. It's built for people who can't or won't use a web form — low-literacy, low-connectivity, non-English-first users. It adapts an offline-first grievance-routing system I built for Tamil Nadu, now with a production voice front-end on Bolna + Plivo, tuned for the code-mixing and noise that real Indian calls have. It targets exactly the "next billion" voice problem — vernacular, task-completing, over a plain phone call.

---

## 2.5-minute demo video script

1. **(0:00–0:20) The problem.** "A citizen in Tamil Nadu wants to report a broken street light. A web form in English is useless to them. So they just… call."
2. **(0:20–1:30) The live call.** Call the number on speaker. Speak a real code-mixed complaint. Let the agent **confirm it back in Tamil**, correct one detail on purpose (show the repair loop), then confirm. Stay quiet for the latency — let it feel fast.
3. **(1:30–2:00) The result.** Show the **SMS** arriving with the ticket ID. Cut to the **dashboard**: the complaint now sits under the right department with a status.
4. **(2:00–2:30) The thesis.** 10-second architecture diagram + one line: "Vernacular, offline-capable, cross-agency routing — built for the next billion callers. Built on Bolna and Plivo."

Keep it real-footage, no fake screens. One genuine call beats ten polished slides.

---

## Risks to kill early
- **Plivo Indian-number KYC delay** → start it in Hour 0. Fallback: use Bolna's built-in telephony if available, or a Plivo trial/US number purely for the demo and *say* production uses an Indian DID.
- **Latency feels sluggish** → prioritize a fast Indic TTS (Cartesia) and streaming STT; it's the difference between "wow" and "meh."
- **Code-mixing breaks the LLM** → test with 15–20 real Tanglish sentences early; tune the prompt / pick Sarvam.
- **Over-building** → if MUST isn't done by Hour 24, cut every NICE immediately.

## The recruiting plays (your actual goal)
- Be active and helpful in **Bolna Slack** from Hour 0 — ask sharp questions, help others.
- Name their thesis back to them in the submission ("next billion", vernacular, task-completing).
- Public GitHub + clean README + a LinkedIn post tagging Bolna with the demo video.
- If you reach interviews (Nov 5–7), talk in *their* language: latency, interruptions, language-switching, deployment, call volume.
