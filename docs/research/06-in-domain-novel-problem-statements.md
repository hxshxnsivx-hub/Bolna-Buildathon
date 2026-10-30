# R&D Dossier v6 — In-Domain Novel Problem Statements (maximize Bolna approval)

**Goal:** find a problem statement that is (a) **inside Bolna's commercial domain** (voice-agent
infra for BFSI/fintech/healthcare/e-comm/recruitment/logistics), (b) **genuinely novel** — needs a
unique solution, (c) **buildable in ~48 h**, (d) **differentiated from the sea of other teams**, and
(e) **leverages your unique asset** (Tamil/Tanglish vernacular craft). This is the "which project
maximizes approval + hire odds" question. _Compiled 2026-10-29._

---

## 1. The frontier: what's actually hard/unsolved in enterprise voice AI (2026)

From the current literature + vendor landscape (sources below):

- **Latency / turn-taking** — natural turn-taking needs ~600–800 ms round-trip; LLM time-to-first-token (~1 s) is the bottleneck. *(Infra problem — not a 48 h project.)* ([Kore.ai](https://www.kore.ai/blog/voice-ai-challenges-and-how-to-fix))
- **Interruption semantics (barge-in)** — telling a cough/backchannel from a real interruption is *understudied*; teams detune sensitivity and agents feel robotic. ([Kore.ai](https://www.kore.ai/blog/voice-ai-challenges-and-how-to-fix))
- **Hallucination on complex turns** — "the competition has moved to handling the most complex turns without hallucination." ([Appinventiv](https://appinventiv.com/blog/why-ai-voice-agents-fail/))
- **Tool use under disfluency** — combining tool-calls with low latency under real-world speech is an open benchmark gap (Full-Duplex-Bench-v3). ([arXiv](https://arxiv.org/pdf/2604.04847))
- **Action/integration failure** — agent "understands but doesn't update the CRM / trigger the refund." ([SoftwareSeni](https://www.softwareseni.com/voice-agents-in-production-the-enterprise-guide-to-what-works-now/))
- **Eval & observability** — a hot category (Maxim, Cekura, Bluejay, Roark, Hamming, LangWatch, Cyara) scoring STT accuracy, tool-call correctness, turn-taking, P95 latency, sentiment, abrupt-termination — **but English-first.** ([Maxim AI](https://www.getmaxim.ai/articles/best-voice-agent-evaluation-tools-in-2026/) · [Confident AI](https://www.confident-ai.com/knowledge-base/compare/best-voice-ai-evaluation-and-observability-tools-2026))
- **Compliance in collections (BFSI, Bolna's #1 vertical)** — RBI Fair Practice Code, 8 AM–7 PM window, TRAI consent/DND, data residency, audit logging; vendors *claim* "guardrails" but provable real-time enforcement is thin. ([Exotel](https://exotel.com/blog/ai-voice-agents-india-debt-collection-exotel/) · [ThePrint/DROS](https://theprint.in/ani-press-releases/with-ai-scrutiny-growing-in-debt-collection-dros-ai-launches-voice-agents-with-compliance-guardrails/2957081/))

**The whitespace that is ALSO your asset:** every eval/QA and compliance tool above is **English /
Hinglish at best — none handle deep code-mixed vernacular (Tamil/Tanglish) over noisy 8 kHz
telephony.** Bolna's declared frontier *is* Indian languages. That intersection is your edge.

---

## 2. Candidate problem statements (ranked)

### ⭐ #1 — "KuralEval": a QA / eval layer for **vernacular** voice agents
*Catch where a Tamil/Hinglish voice agent fails — hallucination, wrong language-switch, missed
intent, compliance breach, task-not-completed — from real call recordings, and suggest the prompt fix.*
- **In-domain?** 🟢 It's *infra for voice agents* = Bolna's exact world, and it solves their **literal
  daily job** (their JD: "review real call recordings to find agent failures and fix them").
- **Novel?** 🟢 Eval tools exist but are English-first; **vernacular/code-mixed + telephony eval is
  whitespace.** You'd be the Indian-language QA layer.
- **48 h?** 🟢 Ingest recording/transcript → LLM-judge scorecard (STT-accuracy, language-switch
  correctness, hallucination, intent/task completion, sentiment, interruption handling) → dashboard
  of flagged calls + suggested prompt diff.
- **Impress Bolna?** 🟢🟢 Highest — a tool *they themselves would use*; shows you understand agent
  internals. Could be offered to them directly.
- **Differentiation?** 🟢 Most teams build end-user bots; a **builder tool / meta-layer** stands out.
- **Leverages your asset?** 🟢 Your Tamil/Tanglish depth is the moat.
- **Risk:** eval is a crowded category (nail the *vernacular* wedge), and a dashboard has less
  "live-call wow" → **mitigate by demoing it live against a real Tanglish call.**

### ⭐ #2 — "Tanglish collections/reminder agent + real-time RBI/TRAI compliance guardrail"
*An in-domain voice agent (EMI reminder / payment / appointment) in code-mixed Tamil, with a live
compliance layer that blocks out-of-window calls, detects harassment/threat language, enforces the
disclosure script, and emits an audit log.*
- **In-domain?** 🟢🟢 Collections is Bolna's #1 vertical; compliance is the enterprise *blocker*.
- **Novel?** 🟡→🟢 Collections bots are crowded, but **provable real-time compliance enforcement +
  vernacular** is the differentiator (vendors only claim it).
- **48 h?** 🟢 Live call (your strength) + a guardrail monitor + audit log.
- **Impress Bolna?** 🟢 Compliance is what unlocks BFSI revenue — solving it *helps them sell*.
- **Differentiation?** 🟡 Medium (many collections demos; the compliance+vernacular twist lifts it).
- **Leverages asset?** 🟢 Reuses your Tanglish voice craft directly; best **live-call wow**.

### #3 — "Self-healing agent": auto-diagnose failed calls → suggest/apply prompt fix → re-test
- In-domain 🟢 (their workflow), **very novel** 🟢, but **48 h feasibility 🟡** (needs eval + optimizer
  + simulation). Ambitious; a scoped version = a strong stretch goal on top of #1.

### #4 — Interruption-robust / full-duplex tool-use agent
- **Very novel** 🟢 (research frontier) but **infra-heavy, 48 h risky 🔴.** Skip for the timeline.

### #5 — Plain objection-handling / negotiation collections bot
- In-domain 🟢 but **low novelty/differentiation 🔴** (every vendor claims it). Skip.

---

## 3. Scorecard

| Candidate | In-domain | Novelty | 48 h | Impress Bolna | Differentiation | Uses your asset | Verdict |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **#1 KuralEval (vernacular QA)** | 🟢 | 🟢 | 🟢 | 🟢🟢 | 🟢 | 🟢 | **Top (novelty)** |
| **#2 Tanglish agent + compliance** | 🟢🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | **Top (safe + wow)** |
| #3 Self-healing | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | stretch goal |
| #4 Full-duplex | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | 🟡 | too risky |
| #5 Plain collections | 🟢 | 🔴 | 🟢 | 🟡 | 🔴 | 🟢 | skip |
| *(civic) Kural grievance router* | 🟡 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | thesis-fit, off-ICP |

---

## 4. Recommendation + decision rule

**Two winners, depending on your appetite:**

- **If you want maximum novelty + "they'd hire the person who built this":** → **#1 KuralEval**, the
  vernacular voice-agent QA layer. It's the one project on this list that is *a tool for Bolna
  itself*, in genuine whitespace, and impossible to confuse with the other teams' end-user bots.
  Demo it **live against a real Tanglish call** so you keep the voice-craft wow.

- **If you want the safest strong demo that reuses your Tanglish work and has the best live-call
  wow:** → **#2**, a code-mixed in-domain agent (EMI reminder / appointment) **with a real-time
  compliance guardrail**. Squarely in their #1 vertical, with a defensible novelty twist.

**My pick: #2 as the core, with #1's eval view bolted on as the "and we also measured it" slide.**
That gives you (a) a live Tanglish in-domain call (wow + your asset), (b) a compliance guardrail
(in-domain novelty that unblocks their revenue), and (c) an eval scorecard (shows builder-depth,
their daily pain) — three things Bolna cares about, in one demo, all reusing the vernacular craft you
already have from the civic project.

**Decision rule if torn:** pick the one you can get a *clean working call* on in 36 hours. For Bolna,
one flawless Tanglish call > any amount of ambition. Everything on this page assumes you **start
building immediately.**

---

## 5. The unavoidable truth (6th dossier, still zero code)
You now have **six R&D dossiers and no product**, and submissions close **Oct 31 (~2 days)**. This is
the **last** analysis that helps; a seventh will only cost you build time. The research has given you
everything needed to choose. **Pick #1 or #2 now and let's build the call today.**

### Sources
- [Kore.ai — 9 voice AI challenges](https://www.kore.ai/blog/voice-ai-challenges-and-how-to-fix) · [Appinventiv — why voice agents fail](https://appinventiv.com/blog/why-ai-voice-agents-fail/) · [SoftwareSeni — voice agents in production](https://www.softwareseni.com/voice-agents-in-production-the-enterprise-guide-to-what-works-now/)
- [Maxim AI — eval tools 2026](https://www.getmaxim.ai/articles/best-voice-agent-evaluation-tools-in-2026/) · [Confident AI — eval/observability tools](https://www.confident-ai.com/knowledge-base/compare/best-voice-ai-evaluation-and-observability-tools-2026) · [Cekura — testing platforms](https://www.cekura.ai/blogs/best-ai-voice-testing-platforms-2026)
- [Full-Duplex-Bench-v3 (arXiv)](https://arxiv.org/pdf/2604.04847)
- [Exotel — AI voice debt collection India](https://exotel.com/blog/ai-voice-agents-india-debt-collection-exotel/) · [ThePrint/DROS — compliance guardrails](https://theprint.in/ani-press-releases/with-ai-scrutiny-growing-in-debt-collection-dros-ai-launches-voice-agents-with-compliance-guardrails/2957081/) · [Oriserve — RBI-compliant AI collections](https://oriserve.com/blog/rbi-compliant-ai-collections-in-india)
