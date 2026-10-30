# R&D Dossier v5 — Will Kural impress *Bolna*? (Novelty × Feasibility × Company Fit)

**The real question:** not "is Kural a good project," but "will *this* project, built for *this*
buildathon, reach the finals and get admired by *Bolna* enough to open a job door." Answered from
Bolna's open-source repo, team, customers, community, and — most revealing — their **live job post**.
_Compiled 2026-10-29._

---

## 1. Who Bolna is (and what that implies)

- **Company:** YC F25, General Catalyst-backed, **$6.3M seed (Jan 2026)**, **~25 people**, **1,050+
  paying customers**, Bengaluru. ([YourStory](https://yourstory.com/ai-story/voice-ai-startup-bolna-raises-63m-led-by-general-catalyst) · [GC job post](https://jobs.generalcatalyst.com/companies/bolna-2-b823d889-50fe-4a6b-8bb0-c1fbbce7cbf8/jobs/95343431-ai-solutions-engineer))
- **Founders:** CEO **Maitreya Wagh** (IIT Delhi, Bain, Probo founder's office — business/strategy);
  CTO **Prateek Sachan** (Zomato, BrowserStack, Atlassian — serious infra engineer, owns the
  model-orchestration thesis).
- **The product / OSS:** `github.com/bolna-ai/bolna` — **MIT, Python**, ~**806★ / 384 forks**. An
  async, **websocket streaming orchestration** of **ASR → LLM → TTS**, provider-abstracted
  (Deepgram, OpenAI/LiteLLM, Cartesia, ElevenLabs…), **telephony via Twilio & Plivo**, agents
  defined by **JSON config**. ([GitHub](https://github.com/bolna-ai/bolna))
- **Who they sell to (their ICP):** **BFSI & collections**, D2C/e-commerce, **fintech**,
  **healthcare**, recruitment, logistics — enterprise inbound/outbound calling (lead-qual,
  collections, reminders, COD confirmation, screening). ([AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-b2zrltwmqdxey))

> **Implication #1 (the honest one):** Kural's vertical — **civic / govtech / social-impact — is NOT
> Bolna's commercial core.** They make money on enterprise outbound. So the civic use case alone
> won't win you points; what wins is **demonstrated voice-agent craft that transfers to their ICP.**

---

## 2. The answer key — Bolna's live job post (AI Solutions Engineer)

This is the single most useful artifact for your question. It's **early-career / freshers**,
Bengaluru/Delhi, and it tells you *exactly* what they evaluate. Map Kural against it:

| What the Bolna role does / wants | Does a well-built Kural demo prove it? |
|---|---|
| "Write, test, iterate **system prompts** for voice agents" | ✅ Kural's whole brain is prompt + flow design |
| "**Review real call recordings** to find agent failures and fix them" | ✅ building Kural = doing exactly this for 2 days |
| "Build **conversation flows / call pathways**" | ✅ the intake→confirm→route→close flow |
| "**Test vernacular inputs — Hindi, Hinglish, regional languages**" | ✅✅ Kural is **Tamil/Tanglish** — stronger than what they list |
| "Close attention to **language and tone**… strong ear for how speech sounds" | ✅ the confirm-and-repair loop is this |
| "See issues from **customer's and end-user's** perspective" | ✅ citizen + department dual view |
| "Comfort making decisions **without a full playbook**" | ✅ a solo buildathon under time pressure |
| Nice-to-have: "experience with **voice AI tools such as Bolna**, Vapi, ElevenLabs" | ✅ *if you build on Bolna's stack* |
| Nice-to-have: "small **vibe-coded projects** (automations, chatbots)" | ✅ Kural is exactly that |
| Nice-to-have: "understand **LLM internals** (context window, temperature, hallucination)" | ✅ show it in the pitch |
| "**No heavy coding** needed; basic scripting is enough" | ✅ lowers the bar — this is a *craft* role, not hardcore SWE |

> **Implication #2 (the opportunity):** Bolna hires early-career people for **voice-agent craft and
> vernacular prompt engineering**, not heavy systems coding. **A polished Tanglish Kural demo is
> almost a tailor-made audition for this exact role.** Build it on Bolna's stack and you tick the
> nice-to-haves too.

Source: [Bolna — AI Solutions Engineer (General Catalyst jobs)](https://jobs.generalcatalyst.com/companies/bolna-2-b823d889-50fe-4a6b-8bb0-c1fbbce7cbf8/jobs/95343431-ai-solutions-engineer)

---

## 3. The feasibility & fit scorecard

| Dimension | Score | Why |
|---|---|---|
| **Novelty** | 🟢 High | Autonomous Tanglish voice call + cross-agency ownership resolution + offline-first — a gap the state's own IIPGCMS RfP confirms is unfilled (dossier v2). |
| **Thesis fit** (vernacular / "next billion") | 🟢 High | Exactly Bolna's public mission; Tamil/Tanglish is their declared frontier. |
| **Vertical/ICP fit** (commercial) | 🟡 Medium | Civic ≠ their BFSI/enterprise revenue core. Admirable, not commercially central. |
| **Skills-match to hiring** | 🟢 High | Hits almost every line of their live JD (table above). |
| **Technical feasibility in 48 h** | 🟢 High (if scoped) | Build on Bolna + Plivo + Sarvam; MVP spine only (dossier v1 §B.3). |
| **Execution risk** | 🔴 The real risk | ~2 days, **zero code written**. For *this* judge a janky call is worst-case — they literally grade call quality. |

**Verdict:** **Feasible and genuinely competitive for the finals *and* admired by Bolna — on one
condition:** it ships as a **polished, voice-craft-forward demo**, not a feature list. The idea and
thesis-fit are already strong; the deciding variable now is **demo polish vs. the clock**, not the
concept.

---

## 4. How to position Kural so Bolna admires it

1. **Make it a voice-craft showcase, not a civic-portal pitch.** The civic domain is the *stage*;
   the *act* they're judging is: Tanglish understanding, sub-second latency, barge-in,
   confirmation/repair, graceful failure. Nail 3 of those deeply.
2. **Build on Bolna's own stack** (OSS or hosted) + Plivo + Sarvam/Cartesia. It ticks their JD
   nice-to-haves and shows you can do the day-job.
3. **Frame the vertical honestly in the pitch:** *"Civic grievances are the hardest possible
   vernacular voice test — noisy, code-mixed, low-literacy, cross-agency. If an agent handles this,
   it handles collections or healthcare reminders easily."* That bridges civic → their ICP.
4. **Talk in their language** in the demo write-up & interview: system prompts, call-failure review,
   context windows, temperature, hallucination control, end-user empathy.
5. **Play the funnel:** the buildathon *is* the hiring top-of-funnel for the Bengaluru/Delhi
   early-career role. Be active and helpful in their Slack; ship a clean public GitHub; post the
   demo video tagging Bolna.

---

## 5. The one risk that outweighs all the analysis

You have **five deep dossiers and zero lines of product code**, and submissions close **Oct 31 (~2
days)**. For most judges, research depth partly compensates for a weak demo. **For Bolna it does
not** — their whole craft is *how the call actually sounds*, and their team reviews call recordings
for a living. A broken or absent demo is the single most likely reason a strong idea misses the cut
here.

**So the feasibility answer is: yes — high feasibility to reach finals and be admired, but only if
we stop researching now and spend the remaining time building one genuinely good call.** The
research is already more than enough to win on substance.

---

### Sources
- [Bolna — AI Solutions Engineer job (the answer key)](https://jobs.generalcatalyst.com/companies/bolna-2-b823d889-50fe-4a6b-8bb0-c1fbbce7cbf8/jobs/95343431-ai-solutions-engineer)
- [bolna-ai/bolna — open-source voice-agent framework](https://github.com/bolna-ai/bolna)
- [Bolna raises $6.3M; vernacular voice infra (YourStory)](https://yourstory.com/ai-story/voice-ai-startup-bolna-raises-63m-led-by-general-catalyst)
- [Bolna on Y Combinator](https://www.ycombinator.com/companies/bolna-ai)
- [Bolna verticals/use-cases (AWS Marketplace)](https://aws.amazon.com/marketplace/pp/prodview-b2zrltwmqdxey)
- [Bolna × Cartesia Voc-a-thon (community build-sprint)](https://luma.com/ubu85bxv)
