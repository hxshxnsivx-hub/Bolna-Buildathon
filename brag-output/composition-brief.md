# Hyperframes Composition Brief: Kural

## Objective
A short, polished launch-style brag video for Kural — an autonomous Tanglish civic-grievance voice agent for Tamil Nadu.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 20 seconds

## Source Material
- Project root: `C:\Users\harsh\Bolna-AI-Builathon`
- Primary files read: `kural/web/index.html` (palette/fonts/chips), `kural/app/routing.py` (31 sectors, owning bodies), `kural/app/billing.py` (over-charge anomaly), `kural/app/main.py` (seeded Coimbatore ₹2000 bill demo), `kural/web/tn_districts.json` (37 districts), `docs/research/03` (TN budget)
- Product name: Kural (குரல்)
- Tagline / strongest claim: "One voice call. The right department."
- Key UI to recreate: the glassmorphic routing chips + copper கு logo from the live dashboard
- Copy that must appear verbatim:
  - "200 units use pannen, aana bill ₹2000 vandhuchu" (seeded demo utterance)
  - "TNPDCL · TANGEDCO", "₹1,765 flagged", "CGRF · TNERC", "SLA ticket filed · SMS sent"

## Creative Direction
- Tone preset: polished
- Creative direction: assured premium product film, pitched like an expert founder
- Interpretation: few scenes, long holds, soft crossfades, calm deliberate motion
- Angle: "One call, the right door" — messy spoken Tanglish in, correctly-routed SLA ticket out
- Hook: கு glyph + Kural wordmark present at frame 0; lines settle
- Outro / punchline: "Tamil Nadu is investing ₹398 crore in AI governance" → Kural · குரல் — the people's voice
- Avoid: generic SaaS language, abstract filler, unrelated redesign

## Visual Identity
- Background: warm beige (#f4ead7 → #e3d3b6), paper grain
- Text: ink #3a2c1c; muted #6e5c43
- Accent: copper #b87333 (dark #8c5424); alerts rust #b4430f, ochre #8a6208, sage #4f7a52
- Display font: Inter 700-900; Tamil: Noto Sans Tamil; mono: JetBrains Mono (caller line)
- Visual references: copper கு badge, glass chips, stat tiles, stylized TN silhouette + pin

## Storyboard
See `brag-output/brag-plan.md` (creative contract).

Scene summary:
1. Hook / brand — 4.5s — கு logo + Kural + "One voice call. The right department." + Tamil
2. The call — 5s — caller Senthil (Coimbatore); Tanglish line types out; listen-pulse
3. Routing — 6s — chips: Electricity → TNPDCL → ⚡₹1,765 over-charge → CGRF; pin; SLA ticket filed
4. Proof + outro — 4.5s — 31 sectors · 37 districts · Tanglish · Self-eval; ₹398 cr tailwind; logo

## Audio
- Audio role: warm professional bed, low and confident
- Audio arc: enters warm, steady under the call, lifts into the over-charge payoff, fades under the closing logo
- Music: happy-beats-business-moves-vol-1-by-ende-dot-app.mp3 (bundled), volume 0.5, media-start 2.4s, fade-in 0.6s, fade-out 1.6s
- Music cue guidance: bundled preset (120 BPM, 0.5s grid). Routing chips beat-gridded at ~10.1/10.7/11.3/12.0s; over-charge chip beat-locked ~11.3s
- Audio-reactive treatment: subtle (listen-pulse glow) — implemented as a CSS pulse for determinism
- SFX: left minimal/none in this pass for polished restraint; can add key ticks + card ticks + confirm cue in a v2
- Audio files: in `composition/assets/music/`

## Notes
- `npx hyperframes check` passes (0 errors). Remaining warnings are decorative brand-glyph contrast (கு/S on copper) and one structural hold — acceptable for this piece.
- Creation and rendering are fully local.
