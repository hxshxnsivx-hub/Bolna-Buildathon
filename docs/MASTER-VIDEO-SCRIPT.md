# Kural — Master Video Script & Production Brief (90s, premium)

A cinematic 1:30 film: **Hook → Problem → Workflow → Live call (proof) → Dashboard (proof) → Results & engineering → Close.** Built to look like a funded product film, not a slideshow.

---

## 0 · THE MASTER PROMPT (paste-ready)

> Create a 90-second premium product film for **Kural**, an autonomous Tamil–English (Tanglish) AI voice agent that lets any Tamil Nadu citizen call one number, speak a civic complaint, and have it auto-routed to the exact government office, bill-overcharge flagged, filed as an SLA-tracked ticket, and self-scored for quality. Tone: confident, warm, cinematic — a funded startup launch film. **Visual system:** warm beige canvas with copper and deep-copper accents, ink-brown text, subtle paper grain, soft radial light pools, glassmorphic cards with copper hairline borders and long soft shadows; display type in Inter (800–900, tight tracking), Tamil in Noto Sans Tamil, data/transcript in JetBrains Mono. **Motion language:** deliberate easing (power3.out, back.out), staggered reveals, kinetic typography, line-draw animations, number count-ups, a slow 2–3% push on real footage, match-cuts on the music's downbeats; no cheesy wipes. **Composite real proof footage** — a recorded phone call with the agent, and a screen-recording of the live dashboard — color-matched into the beige/copper world. **Sound:** warm cinematic underscore that builds, soft UI ticks on reveals, one low confirm-swell on "ticket filed," and the real call audio featured in the demo. End on the copper கு logo and the line "One voice. The right door." Deliver 1920×1080, ~90s.

Use the shot list below as the exact build.

---

## 1 · VISUAL STYLE BIBLE

**Palette (the whole film lives here):**
- Canvas: `#f4ead7 → #ecdfc8 → #e3d3b6` (warm beige gradient) + paper grain at 7% + two soft radial light pools.
- Copper: `#b87333`, deep `#8c5424`, light `#d89a63`, highlight `#e9b685`.
- Ink text `#3a2c1c`, muted `#6e5c43`. Alert: rust `#b4430f`. Success: sage `#4f7a52`.
- Cards: frosted glass `rgba(255,250,240,.6)` + 1px copper hairline + 30–80px soft shadow.

**Type:** Inter (800/900 for headlines, tight −1 to −3 tracking) · Noto Sans Tamil · JetBrains Mono (transcript, ticket IDs, metrics).

**Motion grammar (this is what makes it look expensive):**
- Entrances: fast-in + settle (0.3–0.6s), `back.out` on hero elements, `power3.out` on text.
- Kinetic typography: key words scale/weight-shift on the beat; numbers **count up**.
- Line-draw: the workflow pipeline draws itself; the TN map strokes in.
- Depth: layered cards with parallax; a 2–3° tilt on the dashboard; a slow 2–3% push on all real footage.
- Transitions: soft cross-dissolve by default; **one hard match-cut** into the live call on a downbeat.
- Restraint: nothing strobes, nothing spins. Confidence through stillness and timing.

**Color-match the proof footage:** grade the call UI and dashboard screen-recording slightly warm so they belong to the beige/copper world (don't drop raw blue-white screenshots in).

---

## 2 · SOUND DESIGN

- **Underscore:** warm, minimal, building — piano/pad bed that lifts once at the demo and once at results, then resolves under the logo.
- **SFX:** soft key-ticks under typed text; a single card-tick per pipeline node; a low **confirm swell** on "SLA ticket filed"; a gentle riser into the dashboard reveal.
- **The hero sound is the real call** — duck the music to ~0.15 under it so the Tanglish voice agent is unmistakably real.
- **VO:** calm, slower-than-natural, confident. Your voice or a clean neutral AI voice. Pauses after the hook and before the demo.

---

## 3 · THE 90-SECOND SHOT LIST

Legend — 🎙️ **VO** (say) · 🎬 **SHOW** (on screen) · 🌀 **MOTION** · 🔊 **SOUND**

### ① HOOK — cold open (0:00–0:12)
🎬 Black-beige. A single line of Tamil types in mono, then the English under it. The கு logo glows faintly.
🎙️ "Every day in Tamil Nadu, a complaint dies before it's ever filed."
🌀 Text types on; a slow push in; grain alive.
🔊 Low drone + first piano note. A held breath.

### ② PROBLEM — the stakes (0:12–0:28)
🎬 Three quick glass cards flick in: 💧 "No water, 3 days" · ⚡ "Bill ₹2,000 for 200 units" · 💡 "Streetlight out, 2 weeks." Then they scatter and a question lands center.
🎙️ "No water. A wrong power bill. A broken light. To report it, you must know which of five offices owns the problem — and use an app, in English. So most people stay silent."
🌀 Cards stagger in on the beat, then dissolve; the question scales up.
🔊 Ticks per card; music swells gently.

### ③ THE TURN + SOLUTION (0:28–0:40)
🎬 Everything clears to calm beige. The கு logo blooms; "Kural" wordmark; line settles.
🎙️ "What if you could just… call, and speak? This is Kural. One number. You talk — Tamil, English, or both. And the right office opens."
🌀 Logo back.out bloom; wordmark rises; Tamil subline fades under.
🔊 Music resolves warm; a soft chime on the logo.

### ④ WORKFLOW — the pipeline draws itself (0:40–0:55)
🎬 A horizontal copper pipeline draws left→right; six nodes light in turn: 📞 Call · 👂 Understand · 🧭 Route · ⚡ Check · 🎫 File · ✅ Self-eval. A one-line caption under each.
🎙️ "Here's what happens in that one call. It listens. It understands. It finds the *exact* office. It checks your bill. It files a tracked ticket. And it grades its own call — in Tamil."
🌀 Line-draw; each node pops on its word; progress line fills.
🔊 One tick per node, snapped to the beat.

### ⑤ LIVE CALL — the proof (0:55–1:12)  ← hard match-cut in
🎬 Cut to the **real recorded call** (your demo file) in a framed phone UI; bilingual captions (Tanglish + small English). Over it, two data chips animate in: `TNPDCL` and `⚡ ₹1,765 over-charge`.
🎙️ (before audio) "This isn't a mockup. Listen." → let the call play → (after) "Two hundred units, a two-thousand-rupee bill. Kural catches the ₹1,765 overcharge, routes it to the electricity board, and files the ticket."
🌀 Match-cut on the downbeat; music ducks to 0.15; chips slide in; 2% push on the footage.
🔊 **Real call audio up front.** Low confirm-swell as the ticket chip lands.

### ⑥ DASHBOARD — it's live (1:12–1:22)
🎬 The **real dashboard screen-recording**, warm-graded, with a slow push. Copper callout rings hit, in turn: the `KRL-2026-00001 · ₹1,765 over` ticket → the Anna Nagar **hotspot (3×)** → the **KuralEval** score. Caption strip: "Live console — routed · SLA-tracked · hotspot-merged · self-scored."
🎙️ "And it lands here — live. Every complaint: routed, tracked, flagged, grouped into hotspots, and scored."
🌀 Rings scale-in on beats; KPI numbers count up; routing-load bars grow.
🔊 Music lifts; soft ticks on each ring.

### ⑦ RESULTS & ENGINEERING (1:22–1:28)
🎬 A tight stat/engineering grid assembles: **31 sectors** · **37 districts** · **deterministic routing (auditable)** · **KuralEval 85.7** · **26/26 tests passing** · **deployed & callable**. A faint architecture line behind: `voice → understand → route → compute → file → eval`. Then the tailwind line.
🎙️ "Under the hood: thirty-one civic sectors, routing you can audit, a vernacular evaluation layer the English-first tools don't have, twenty-six tests passing, deployed today — while the state invests ₹398 crore in exactly this."
🌀 Tiles snap in staggered; numbers count up; architecture line draws.
🔊 A confident build to a clean peak.

### ⑧ CLOSE (1:28–1:30)
🎬 Resolve to beige. The copper கு logo + **"One voice. The right door."** + "Kural · குரல்."
🎙️ "Kural. One voice. The right door."
🌀 Logo settle; hold 2s; grain alive.
🔊 Underscore resolves and fades.

---

## 4 · PROOF / ASSET CHECKLIST (capture these first)

- [ ] **Real call recording** (the demo file) — the Coimbatore ₹2,000-bill call; clean audio, ~15–20s usable.
- [ ] **Dashboard screen-recording** at 1080p — settled state: the ₹1,765 ticket, the 3× hotspot, KuralEval score, routing-load chart. *(We already captured crisp stills; a short screen-rec is even better.)*
- [ ] **Test output** — a frame of `26/26 passing` for the engineering beat.
- [ ] **Deployed proof** — the live URL / a shot of the running app.
- [ ] **Logo asset** — the copper கு badge (already in the brag/explainer files).
- [ ] **Music bed** — warm cinematic (not the busy one; something with a slow build).

---

## 5 · HOW TO BUILD IT (two routes)

**A — Hyperframes (free, local, full control) — recommended.** The animated sections (hook, problem, pipeline, results, close) are built as a Hyperframes composition in this brand system; the **real call** and **dashboard** footage are composited in as video layers, warm-graded. I can build this here, section by section, and render it — no credits. This is the closest to the "$2000" look with zero spend.

**B — Editor route (InVideo/CapCut/Descript).** Use this script as the shot list; drop the animated bumpers + real footage on a timeline, add VO + music. More manual; needs credits for InVideo.

---

### Narration, clean (for recording in one pass)
> Every day in Tamil Nadu, a complaint dies before it's ever filed. No water. A wrong power bill. A broken light. To report it, you must know which of five offices owns the problem — and use an app, in English. So most people stay silent.
> What if you could just… call, and speak? This is Kural. One number. You talk — Tamil, English, or both — and the right office opens.
> Here's what happens in that one call. It listens. It understands. It finds the exact office. It checks your bill. It files a tracked ticket. And it grades its own call — in Tamil.
> This isn't a mockup. Listen. … Two hundred units, a two-thousand-rupee bill. Kural catches the ₹1,765 overcharge, routes it to the electricity board, and files the ticket.
> And it lands here, live. Every complaint: routed, tracked, flagged, grouped into hotspots, and scored.
> Under the hood: thirty-one civic sectors, routing you can audit, a vernacular evaluation layer the English-first tools don't have, twenty-six tests passing, deployed today — while the state invests ₹398 crore in exactly this.
> Kural. One voice. The right door.
