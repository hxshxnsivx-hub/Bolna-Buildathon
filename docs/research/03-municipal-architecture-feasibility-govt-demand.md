# R&D Dossier v3 — Municipal Anatomy, Fusion Feasibility & Government Demand

**Scope (the three things you asked for):**
1. **Part A** — End-to-end anatomy of a Tamil Nadu municipal corporation: wings, departments,
   zones, wards, field cadres, and *how it actually operates* — with a new Tree of Distribution.
2. **Part B** — Feasibility of fusing the **two ideas** — the *Grievance Resolution Router* and
   the *Kural voice-first ideology* — into one coherent, buildathon-winning product ("PB&J").
3. **Part C** — R&D on whether the **TN government is actively investing** in exactly these gaps.

Builds on v1 (`Civic-services/docs/research/01-…`) and v2 (`docs/research/02-…`). _Compiled 2026-10-29._

---

## PART A — Anatomy of a Tamil Nadu Municipal Corporation

A TN corporation is **two parallel wings** over a **geographic tier stack**. Get this picture
right and the router's dispatch granularity falls out of it.

### A.1 The two wings

**① Political (deliberative) wing** — *decides & oversees, does not execute*
- **Council** of elected **ward councillors** (one per ward), headed by a **Mayor** + Deputy Mayor.
- **Standing committees:** Works, Public Health, Town Planning & Improvement, Taxation & Finance,
  Education, Accounts.
- **Ward committees / zonal chairpersons** at the zone level.
- *Relevance to you:* the councillor is the **political escalation target** for a ward — a useful
  final rung in an SLA escalation chain, but **not** who physically fixes a pothole.

**② Executive (administrative) wing** — *executes; this is who your router dispatches to*
- Headed by the **Commissioner** (IAS/state service) — the executive authority.
- **Assisted by:** Deputy Commissioner(s), **City Engineer**, **City Health Officer**, City
  Education Officer, **Executive Engineers (2+)**, **Assistant Commissioners**, + others.

### A.2 The executive departments (the "domains")

Corporations run **6–7 functional departments** (slight variation by city):

| Department | Owns these grievances | Field cadre that acts |
|---|---|---|
| **Engineering** | internal roads, potholes, storm-water drains, buildings, streetlight infra | Executive Engineer → Assistant Engineer → **Junior Engineer (JE)** → maestri/contractor |
| **Public Health & Sanitation** | garbage, bins, dead animals, public toilets, fogging, dengue, stray animals | City Health Officer → Sanitary Officer → **Sanitary Inspector (SI)** → Sanitary Supervisor → conservancy workers |
| **Town Planning** | unauthorised construction, encroachment, building-plan violations | City/Asst Town Planner → **Town Planning Inspector** |
| **Revenue** | property tax, profession tax, trade licence, D&O licence | Asst Commissioner (Revenue) → **Revenue Inspector / Bill Collector / Assessor** |
| **General Administration / Personnel** | staff, RTI, coordination, records | — |
| **Finance & Accounts** | budgets, payments | — |
| **IT** (where present) | the complaint portal/app, e-services, MIS | IT cell |
| *(Education — Madurai; varies)* | corporation schools | City Education Officer |

> **The key operational insight for routing:** v1/v2 answered *"which agency owns it"* (ULB vs
> CMWSSB vs TANGEDCO…). Part A answers the next level down — *"inside the ULB, which **department +
> field officer** actually resolves it."* That is the real dispatch target. A **streetlight** →
> Engineering (JE); **garbage** → Public Health (Sanitary Inspector); **encroachment** → Town
> Planning (TP Inspector). Your router should carry this **department + cadre** tag on every ticket,
> because the SLA clock and escalation chain are *per department*, not generic.

### A.3 The geographic tier stack (where a complaint physically lands)

```
MUNICIPAL CORPORATION  (Commissioner)
│   e.g. Madurai = 5 zones / 100 wards ;  Greater Chennai = 3 regions / 15 zones / 200 wards
│
├── REGION          (large corps only — GCC has 3: North/Central/South; Regional Dy. Commissioner)
│   │
│   └── ZONE        (the real operational unit — each zone replicates 4 sections:)
│       │                ├─ Engineering section     (zonal JE/AE)
│       │                ├─ Public Health section   (zonal Sanitary Officer + SIs)
│       │                ├─ Town Planning section   (zonal TP Inspector)
│       │                └─ Revenue section         (zonal Revenue Inspector)
│       │           headed operationally by a ZONAL OFFICER / Assistant Commissioner
│       │
│       └── WARD     (one elected councillor; the SLA + inspection unit)
│           │           • field staff attached: Sanitary Inspector, JE, Bill Collector
│           │           • Zonal Officers brief ward councillors on field inspections
│           │
│           └── STREET / AREA / LOCALITY   ← the citizen & the actual grievance location
```

**How it operates (the as-is loop):** complaint → logged (1913/app/portal) → **auto-diverted to the
concerned zone** → **zonal section** (Engineering/Health/etc.) tasks the **ward field officer**
(JE/SI) → rectify ("a day or two" target) → head-office complaint cell follows up at **10–15 days**
→ unresolved cases surface at **Commissioner review meetings**. (Soft, human-graded SLA — your
improvement surface, per v1 §1.6.)

> **Build takeaway — don't over-model this.** For the 48-hour demo you need exactly: `sector →
> {owning body, department, field cadre, zonal unit}` as a lookup, plus a per-department SLA clock.
> The full 100-ward councillor roster and committee structure is *reference*, not build scope. Model
> **one corporation (Chennai or Madurai), ~3 sectors, zone-level routing** — that's enough to prove it.

Sources: [Madurai Municipal Corporation (structure, 5 zones/100 wards, 7 depts)](https://en.wikipedia.org/wiki/Madurai_Municipal_Corporation) ·
[Tiruchirappalli City Municipal Corporation](https://en.wikipedia.org/wiki/Tiruchirappalli_City_Municipal_Corporation) ·
[PRAJA Urban Governance Study — Tamil Nadu (zone sections)](https://praja.org/praja_docs/praja_downloads/Urban%20Governance%20Report%20on%20Tamil%20Nadu.pdf) ·
[Greater Chennai Corporation](https://en.wikipedia.org/wiki/Greater_Chennai_Corporation) ·
[GCC zonal officers brief ward councillors (DTNext)](https://www.dtnext.in/news/chennai/councillors-requests-civic-authorities-to-increase-salary-for-contract-workers-745316)

*Caveat: field-cadre reporting lines (SI/JE → zonal officer) are the standard TN municipal pattern
assembled from multiple corporations + recruitment cadre notices; confirm exact titles per
corporation against its official site / the TN Municipal Service rules before production.*

---

## PART B — Feasibility of fusing the two ideas (the PB&J)

### B.1 They are not two rival ideas — they are two halves of one product

| | **Idea 1 — Grievance Resolution Router** | **Idea 2 — "Kural" voice-first ideology** |
|---|---|---|
| Role | The **brain / back-end** | The **mouth & ears / front-end** |
| Does | classify → resolve owning body + dept → dedup → ticket → SLA clock → tiered escalation → close-loop | autonomous **Tamil/English (Tanglish) voice call** intake + confirmation + spoken status, no app/literacy needed |
| Alone it is… | "just another portal" — the govt already has routing portals (v2) | "a transcription toy" — captures speech but does nothing with it |
| Together | **the gem:** the voice front door the state system lacks, feeding a cross-agency routing brain | |

**Peanut butter (Kural voice) + jelly (the router) = the sandwich.** The fusion is *natural
composition*, not a forced merge: the voice agent is the **intake & interaction layer**; the router
is the **resolution & accountability layer**. The hand-off is a single structured object:

```
VOICE AGENT (Kural)                          ROUTER (grievance engine)
 call → ASR(Tanglish) → NLU                   receives {sector, locality, severity, text}
 extract {sector, locality, severity} ──────▶ resolve owning body + dept + field cadre + zone
 confirm back in caller's language ◀────────  dedup vs open tickets (body × locality)
 speak ticket id + ETA                        create ticket, start per-dept SLA clock
 (later: call back with status) ◀──────────── escalate ward→zonal→regional→commissioner on breach
                                              SMS close-loop (Plivo)
```

### B.2 Feasibility verdict — **HIGH**, with disciplined scope

| Dimension | Verdict | Notes |
|---|---|---|
| **Conceptual coherence** | ✅ Strong | Front-end + back-end of one system; each covers the other's weakness. |
| **Technical (48 h)** | ✅ Feasible | Voice = Bolna + Sarvam Saaras v4 + Plivo (config, not from-scratch). Router = deterministic `sector→{body,dept,cadre,zone}` lookup + LLM classifier (reuse civic-services logic). Ticket store + dashboard + SMS = a day. |
| **Demo** | ✅ Excellent | **One phone call demonstrates BOTH ideas end-to-end** in ~2 min: speak → classify → route → ticket → SMS → dashboard. Judges see the whole sandwich in one bite. |
| **Novelty fit** | ✅ Exactly the v2 gap | Voice front door + cross-agency routing = the unduplicated wedge the IIPGCMS RfP confirmed is missing. |
| **Main risk** | ⚠️ Scope creep | Full dedup-clustering + multi-tier escalation + multi-corporation = *not* 48 h. |

### B.3 What to BUILD vs what to SHOW (the line that saves you)

- **BUILD (MVP spine):** Tanglish voice intake → classify to sector → resolve `{body, dept, cadre,
  zone}` for **one corporation + ~3 sectors** → confirmation/repair turn → ticket id → Plivo SMS →
  live dashboard row. One **urban** + one **rural** demo call.
- **SHOW (architecture/roadmap slide, not coded):** duplicate clustering ("10 callers, 1 ticket"),
  full ward→zonal→regional→commissioner SLA escalation, dispatch-into-IIPGCMS via its integration
  API, offline queue-and-forward. Narrate these as the vision; don't sink 48 h into them.

> **One-line pitch for the fused product:** *"Kural is the voice front door for Tamil Nadu's civic
> grievances — a citizen calls one number, speaks in Tamil-English, and an AI agent figures out which
> of the 5 owning bodies and which municipal department is responsible, files a tracked ticket with
> an SLA clock, and texts them the number — no app, no form, no literacy required. It plugs into the
> state's existing grievance backend rather than replacing it."*

---

## PART C — Is the TN government actively investing in these gaps? (Yes — strongly)

This is the demand-side validation. The evidence that TN is **actively funding exactly this
direction** is unusually strong for 2026:

| Signal | What it says | Why it matters for Kural |
|---|---|---|
| **TN Revised Budget 2026-27** | Proposes **AI-enabled governance**: *agentic AI workflows* and **speech-to-text aids for officials**, AI planning-approval system, upgraded single-window portal | The state is *literally budgeting for agentic + speech AI in governance* — Kural is a textbook instance |
| **₹398 crore** to the **AI, IT & Digital Services dept** (revised estimates) | Real money behind the AI agenda | Funded priority, not rhetoric |
| **AI City "Arivagam"** + deep-tech & AI skilling | Dedicated AI infrastructure & talent push | Ecosystem + hiring tailwind |
| **TN Artificial Intelligence Mission (TNAIM)** via **TNeGA** | Responsible AI adoption in governance, expanding to quantum/AR-VR | TNeGA also owns IIPGCMS — the grievance + AI owners are the same body |
| **Tamil-language AI push (May 2026)** — datasets, DPI, **talks with Sarvam AI**, state GPU capacity | State is building Tamil AI and *already engaging Sarvam* | Your exact stack (Tamil + Sarvam) sits inside a state priority |
| **AI Open Data Platform** for startups (TNGSS 2025) | Clean govt data for training/testing AI | Potential data + legitimacy path |
| **StartupTN onboarding AI/IT firms** to improve govt services | A procurement/empanelment on-ramp for startups | *This is the realistic route from demo → paid pilot* |
| **IIPGCMS re-procurement RfP (2025, TNeGA)** | Actively rebuilding the grievance system | A live modernization moment Kural could ride into |
| **2020: first state** with AI/blockchain/cybersecurity + **Safe & Ethical AI** policy | Long-standing govtech leadership | Low institutional friction to AI |

**Verdict:** Kural is **not a speculative idea hunting for a problem** — it lands inside at least
four *simultaneously active, funded* TN priorities: (1) grievance-redressal modernization, (2)
Tamil-language AI, (3) agentic/speech AI in governance, (4) startup onboarding for gov-services.
That is a rare alignment. **Use it in your pitch and your Bolna interview:** position Kural as a
ready-made pilot for the state's own stated 2026-27 roadmap, with a concrete on-ramp (StartupTN
empanelment / TNeGA engagement) rather than a hypothetical.

*Caveat: budget lines and announcements are intent, not signed contracts; verify the TNAIM G.O. and
2026-27 allocations against official TN budget documents, and treat the Sarvam "talks" report as
unconfirmed. The procurement path for a startup runs through StartupTN/TNeGA, not a direct sale.*

Sources: [TN Budget 2026 — AI governance, speech-to-text (The News Minute)](https://www.thenewsminute.com/tamil-nadu/tn-budget-2026-vetri-laptop-scheme-ai-governance-among-key-announcements) ·
[TN Budget 2026 — AI City Arivagam, deep tech (AI Front Page)](https://aifront-page.com/tamil-nadu-budget-2026-ai-arivagam-deep-tech-ai-skilling/) ·
[₹398 cr to AI/IT dept; responsible AI (Deccan Chronicle)](https://www.deccanchronicle.com/southern-states/tamil-nadu/artificial-intelligence-rules-government-thought-process-1976971) ·
[TN AI Mission via TNeGA (DTNext)](https://www.dtnext.in/news/tamilnadu/tn-govt-to-soon-implement-tamil-nadu-artificial-intelligence-mission-810098) ·
[TN AI open data platform for startups (DTNext)](https://www.dtnext.in/news/tamilnadu/tamil-nadu-to-launch-ai-open-data-platform-for-startups-says-ptr-849223) ·
[StartupTN to onboard AI/IT firms (DTNext)](https://www.dtnext.in/news/tamilnadu/startuptn-to-onboard-ai-it-firms-to-improve-services) ·
[TN first state with AI/blockchain/cyber policies (IndiaAI)](https://indiaai.gov.in/news/tamilnadu-first-state-to-produce-ai-blockchain-and-cybersecurity-policies-in-india) ·
[TNeGA IIPGCMS RfP 2025 (PDF)](https://www.medianama.com/wp-content/uploads/2025/10/Tamil-Nadu-Helpline-RfP.pdf)

---

## Bottom line across A + B + C

- **A:** The dispatch target isn't just "the agency" — it's a **department + field cadre (JE/SI/TP
  Inspector/Revenue Inspector) at a zone**. Tag every ticket with that; keep the model to one
  corporation + a few sectors for the demo.
- **B:** The router and Kural are **one product** (brain + voice). Fusion is highly feasible in 48 h
  **if** you build the spine and *show* the rest. One call demos both.
- **C:** The state is **actively funding this exact direction** (agentic + speech AI, Tamil AI,
  grievance modernization, startup onboarding) — strong, citable demand that de-risks the pitch.

**Next:** turn Part A's `sector → {body, dept, cadre, zone}` map into a concrete classifier/routing
spec you can code for Kural.
