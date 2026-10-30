# R&D Dossier v2 — Deepening Pass (Tamil Nadu Grievance Router / "Kural")

**Purpose:** This is a *deepening pass* on top of the existing v1 dossier
(`Civic-services/docs/research/01-tamilnadu-civic-services-RnD.md`, compiled 2026-07-29).
v1 already covers the governance hierarchy, both trees of distribution, the sector/owning-body
map, paid/unpaid + building flags, and the first-cut existing-solutions scan — **all of it still
holds.** This v2 does three things v1 flagged as "open items":

1. **Refreshes the 3-month-old figures** (one correction: the GCC ward/zone numbers).
2. **Closes the 5 open items** v1 left to verify (SLA, 1100/IIPGCMS scope, area-office routing,
   Sarvam/Bhashini quality, rural channels).
3. **Sharpens the Phase-2 novelty claim with *primary-source* evidence** — the official
   TNeGA IIPGCMS RfP — which materially changes *which part* of your idea is actually novel.

_Compiled 2026-10-29. Verify live portals before building against them._

---

## 0. The headline that changes your pitch

I read the **official TNeGA RfP for the IIPGCMS / CM Helpline 1100 system** (the statewide
grievance platform). This is the authoritative spec for the government's own system, not
secondary reporting. What it **does** mandate:

- **Omnichannel intake** — web portal, mobile app, email, SMS, and **auto-ingestion from social
  media (Facebook, Twitter, WhatsApp, LinkedIn, Instagram)** — grievances posted to official
  handles are created automatically.
- A **"robust routing mechanism"** and **"time-bound redressal of grievances as per the citizen
  charter of Govt of Tamil Nadu"**, monitored up through Collectors → HoDs → Secretaries → CM Office.
- **Bilingual** UI, SMS/email notifications, a monitoring/analytics dashboard, master-data
  management, **third-party integration via API** (e.g., TNSDC statuses written back through an API).
- Scale: an end-to-end system used by **3,000+ active official users daily**; a **human call
  centre** at the CM cell is the phone front-end.

What it **does NOT contain — anywhere in 74 pages:**

- ❌ No **autonomous AI voice agent / voicebot**.
- ❌ No **IVR automation, ASR (speech-to-text), or TTS**.
- ❌ No **conversational / free-speech intake** of any kind — the phone channel is a *human* call centre.
- ❌ No **code-mixed ("Tanglish") speech understanding**. "Bilingual" = Tamil/English UI text, not conversation.

> **Strategic consequence.** The government *already claims* routing and SLA-per-citizen-charter on
> paper, and already does WhatsApp/social intake. So those are **weaker novelty claims** than v1
> implied. Your genuinely defensible, unduplicated wedge narrows to exactly three things:
>
> 1. **An autonomous AI voice agent that handles the whole call** — no app, no literacy, no human
>    agent — in **code-mixed Tamil/English**.
> 2. **Cross-agency owning-body resolution at the moment of the call** (ULB vs CMWSSB/TWAD vs
>    TANGEDCO vs Highways), rather than dumping into one human queue to be sorted later.
> 3. **Offline-first / phone-only reach** for tier-3 & rural citizens the digital channels miss.
>
> Lead your pitch with #1 and #2. Do **not** claim "first to route" or "first to do SLA" — the
> state's own RfP will contradict you. Claim "first to make the *call itself* autonomous and
> cross-agency, in the language people actually speak."

Source: [TNeGA IIPGCMS RfP (PDF)](https://www.medianama.com/wp-content/uploads/2025/10/Tamil-Nadu-Helpline-RfP.pdf) ·
[About IIPGCMS / Mudhalvarin Mugavari](https://cmhelpline.tnega.org/portal/en/kb/articles/about-us)

---

## 1. Correction to v1 — GCC zones/wards & delimitation

v1 said GCC = 15 zones / 200 wards "→ 20 zones / 300 wards by 2027." **Update that:**

- GCC currently operates **15 zones / 200 wards** (unchanged and still correct for your lookup table).
- The expansion figure is **not 300 wards**; reporting cites a planned move to **~22 zones**, but
  **urban delimitation is postponed** pending Census 2027, and **TN civic-body elections are
  likely deferred to early 2027**. Chennai ward/zone boundaries are **frozen for now**; the GCC's
  absorption of fringe panchayats (Vanagaram, Adayalampattu) is on hold.
- **Build implication:** hard-code today's **15 zones / 200 wards** for the location→ward lookup;
  don't design against the unconfirmed 300-ward map. Treat boundaries as stable through 2026.

Sources: [TN civic polls likely deferred to early 2027 (Deccan Chronicle)](https://www.deccanchronicle.com/southern-states/tamil-nadu/tn-civic-polls-likely-to-be-deferred-to-early-2027-1974575) ·
[TN Dec-31 boundary-redraw deadline / 15→22 zones (DTNext)](https://www.dtnext.in/news/tamilnadu/tn-sets-dec-31-deadline-to-redraw-administrative-boundaries-ahead-of-2027-census-844456)

---

## 2. Open item #1 — per-category SLA days

No single clean per-category table is published centrally, but these are the usable anchors:

| Grievance type | Documented time limit | Source |
|---|---|---|
| GCC **online grievance** | **15 working days** | older GCC citizen-charter excerpt |
| GCC **CM-office petition** | **7 working days** | same |
| **RTI** request | 30 days | same |
| Central **CPGRAMS** benchmark | **21 days** (cut from 30) | Govt of India |
| GCC zonal "informal" target | "a day or two," head-office follow-up at **10–15 days** | Citizen Matters / DTNext |
| Statewide IIPGCMS | "time-bound **as per citizen charter**" (per-category values live in the charter) | IIPGCMS RfP |

- **Build implication:** seed your SLA timers with **15 working days** as the default grievance
  clock, **7 days** for escalated/CM-class, with tiered auto-escalation (ward → zonal → regional →
  commissioner). For the demo, a *visible hard timer* already beats the as-is (human follow-up at
  10–15 days). Pull exact per-category values from the live **GCC PGR** before production:
  `erp.chennaicorporation.gov.in/pgr`.

Sources: [Centre cuts grievance redressal to 21 days (Tribune)](https://www.tribuneindia.com/news/india/centre-cuts-public-grievances-redressal-time-to-21-days/amp) ·
[Citizen Matters — Chennai 1913 / Namma Chennai flow](https://citizenmatters.in/chennai-citizen-clinic-1913-namma-chennai-rwa-complaints-activists/)

---

## 3. Open item #2 — integrate vs replace (1100/IIPGCMS API)

- The IIPGCMS RfP confirms the system **exposes/consumes APIs for third-party integration**
  (status write-backs like TNSDC), but **no public API reference, endpoint list, or auth spec** is
  published. Access would require a TNeGA engagement.
- **Build implication / positioning:** Kural is a **parallel autonomous-voice intake layer that
  can later dispatch *into* IIPGCMS via its integration API**. Frame it to judges as
  *complementary, not competitive* — "the voice front door the state system doesn't have, that
  hands a clean, classified, geo-resolved ticket to the existing backend." That's both more
  credible and more hireable than "replace the government's system."

Sources: [IIPGCMS RfP (routing + API + third-party integration)](https://www.medianama.com/wp-content/uploads/2025/10/Tamil-Nadu-Helpline-RfP.pdf) ·
[IIPGCMS workflow / nodal-officer routing (ComplaintHub)](https://citizen.complainthub.org/t/how-can-you-file-complaints-about-government-offices-to-tamil-nadu-public-grievance-cm-helpline-management-system-iipgcms/1955)

---

## 4. Open item #4 — Sarvam / Bhashini for code-mixed telephony (build-critical)

This directly sets your Kural speech stack.

- **Sarvam (recommended primary):** flagship ASR was **Saarika v2.5** (now being **deprecated**);
  the current recommendation is **Saaras v3** (`mode="transcribe"`) with **Saaras v4** as the newer,
  higher-accuracy option. Vendor states: **optimized for 8 kHz telephony**, **handles mid-sentence
  code-mixed (Tanglish) language switches**, **~sub-150 ms time-to-first-token**, trained on **1M+
  hours**. Tamil page explicitly markets agglutinative morphology + Tanglish switching.
- **Caveat:** these are **vendor claims — no independent WER** for Tamil / code-mixed / telephony
  was found. **Bhashini** surfaced no usable benchmark either.
- **Build implication:**
  1. Default to **Sarvam Saaras v4** for ASR (it's a buildathon sponsor *and* the strongest Indic +
     telephony + Tanglish story — double win).
  2. **Self-benchmark early:** record 15–20 real Tanglish complaint utterances over an 8 kHz phone
     path and measure yourself in Hour 2–8. Don't trust the datasheet; the demo lives or dies here.
  3. Keep **Deepgram** as a fallback STT and **Cartesia** for low-latency TTS (both sponsors).

Sources: [Sarvam Saarika/Saaras model docs](https://docs.sarvam.ai/api-reference-docs/asr/models/saarika) ·
[Sarvam Speech-to-Text (Tamil / Tanglish)](https://www.sarvam.ai/apis/speech-to-text/tamil)

---

## 5. Open item #5 — rural / panchayat grievance channels

This is where your offline-first, voice-only thesis is **strongest** — the digital channels are thinnest here.

- **Ooratchi Mani** (ஊராட்சி மணி) — RD&PR's dedicated rural grievance system: toll-free **155340**,
  portal **ooratchimani.gov.in**; **PA (Development) to the District Collector** is the nodal officer.
- **IIPGCMS / CM Helpline 1100** also accepts complaints **against panchayat-raj bodies**
  (burning waste, broken streetlights, open manholes, waterlogging, etc.).
- **TNRTP / Vazhndhu Kattuvom** has a project-scoped grievance line **1800 599 1600** (not general civic).
- **Finding:** there is **no per-village-panchayat online portal**. Rural intake is a toll-free
  number + a district-level human nodal officer. **Build implication:** a Tamil voice agent on a
  single number that *auto-resolves which body owns the issue* is a materially bigger leap in rural
  TN than in Chennai — make at least one demo call a **rural/panchayat** scenario to show that reach.

Sources: [Stalin launches Ooratchi Mani (155340) — DTNext](https://www.dtnext.in/news/tamilnadu/stalin-to-launch-ooratchi-mani-to-address-rural-issues-738002) ·
[TN CM Helpline / IIPGCMS covers panchayat bodies (ComplaintHub)](https://complainthub.org/tamil-nadu-cm-helpline-iipgcms/)

---

## 6. Updated novelty statement (supersedes v1 §2.3)

> Grievance portals, cross-agency routing, SLA-per-citizen-charter, and even WhatsApp/social
> intake **already exist** in TN's official IIPGCMS. What does **not** exist — confirmed against the
> state's own RfP — is an **autonomous AI voice agent that conducts the entire grievance call in
> code-mixed Tamil/English, resolves which of the ~5 owning bodies is responsible at the caller's
> location, and does so offline-first for phone-only tier-3 & rural citizens.** That specific
> intersection is the defensible, unduplicated thesis for **Kural**. Position it as the **voice
> front door that plugs into** the existing state backend — complementary, not a replacement.

---

## 7. Carry-forward to the build (Kural)

1. **Pitch framing:** autonomous Tanglish *voice call* + cross-agency ownership resolution; "plugs
   into IIPGCMS," doesn't replace it. Avoid claiming routing/SLA as novel.
2. **Speech stack:** Sarvam **Saaras v4** ASR (self-benchmark on 8 kHz Tanglish) + Cartesia TTS; Deepgram fallback.
3. **Routing table:** reuse v1's sector→owning-body map; hard-code **GCC 15 zones / 200 wards** +
   TANGEDCO section / CMWSSB area / TWAD+panchayat for rural.
4. **SLA timer:** 15 working-day default, 7-day escalated, tiered auto-escalation; visible countdown in the dashboard.
5. **Demo set:** include one **urban** call (e.g., Chennai streetlight → GCC zone) and one **rural**
   call (e.g., village water → TWAD/panchayat) to show cross-agency + offline reach.

---

### New sources added in v2
- [TNeGA IIPGCMS RfP (PDF, 74pp)](https://www.medianama.com/wp-content/uploads/2025/10/Tamil-Nadu-Helpline-RfP.pdf)
- [TN civic polls deferred to early 2027 — Deccan Chronicle](https://www.deccanchronicle.com/southern-states/tamil-nadu/tn-civic-polls-likely-to-be-deferred-to-early-2027-1974575)
- [TN boundary-redraw deadline / 15→22 zones — DTNext](https://www.dtnext.in/news/tamilnadu/tn-sets-dec-31-deadline-to-redraw-administrative-boundaries-ahead-of-2027-census-844456)
- [Centre cuts grievance redressal to 21 days — Tribune](https://www.tribuneindia.com/news/india/centre-cuts-public-grievances-redressal-time-to-21-days/amp)
- [Sarvam Saarika/Saaras ASR docs](https://docs.sarvam.ai/api-reference-docs/asr/models/saarika)
- [Sarvam Tamil STT (Tanglish)](https://www.sarvam.ai/apis/speech-to-text/tamil)
- [Ooratchi Mani rural grievance (155340) — DTNext](https://www.dtnext.in/news/tamilnadu/stalin-to-launch-ooratchi-mani-to-address-rural-issues-738002)
- [TN CM Helpline / IIPGCMS (panchayat coverage) — ComplaintHub](https://complainthub.org/tamil-nadu-cm-helpline-iipgcms/)
- [IIPGCMS workflow / routing — ComplaintHub citizen forum](https://citizen.complainthub.org/t/how-can-you-file-complaints-about-government-offices-to-tamil-nadu-public-grievance-cm-helpline-management-system-iipgcms/1955)
