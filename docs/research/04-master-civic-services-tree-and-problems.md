# R&D Dossier v4 — Master TN Civic-Services Tree + Problem Map (for Kural)

**What this is:** the merged output of a 3-agent research sweep covering the *entire* Tamil Nadu
civic-services landscape (not just municipal corporations), as a **tree of distribution** (service
**class → subclass → owning body → paid/unpaid**), with the **current real-world problems** per
domain, and a mapping to **Kural's** voice-router feasibility. Builds on v1–v3.

_Compiled 2026-10-29. Legend: 💰 = paid (fee/tax) · 🆓 = free to complain/grievance · ⚠️ = verify (dated/secondary source)._

> **Build-time correction (important):** **TANGEDCO was restructured in 2024** — electricity
> *distribution* now sits with **TNPDCL** (Tamil Nadu Power Distribution Corp Ltd); generation =
> TNPGCL; green = TNGECL. Branding is migrating to TNPDCL but **"TANGEDCO" + helpline 1912 are
> still in common use**. Route on **TNPDCL** and alias TANGEDCO to it.
> ([DTNext](https://www.dtnext.in/news/tamilnadu/union-govt-approves-tangedco-renaming-to-tnpdcl-794611))

---

## 1. MASTER TREE OF DISTRIBUTION — TN Civic Services

```
TAMIL NADU CIVIC SERVICES
│
├── I. UTILITIES & PHYSICAL INFRASTRUCTURE
│   ├── Electricity — TNPDCL/TANGEDCO (TNEB)
│   │     ├─ Power outage / fuse-off / line / transformer / voltage        🆓  (→1912)
│   │     ├─ High bill / faulty meter  → escalate CGRF → TNERC             🆓
│   │     ├─ New connection / load change / name transfer                  💰
│   │     └─ Solar rooftop / net-metering approval                         💰+🆓(delay)
│   ├── Water supply
│   │     ├─ Chennai: no supply / low pressure / contamination / leak → CMWSSB   🆓 (→1916)
│   │     ├─ Chennai: tanker (lorry) booking → CMWSSB                      💰+🆓(non-delivery)
│   │     └─ Rest of TN: supply/quality → TWAD + ULB/Panchayat            🆓 (→PUNAL)
│   ├── Sewerage / UGD
│   │     ├─ Chennai: overflow / blocked sewer / manhole → CMWSSB          🆓
│   │     └─ Rest of TN: UGD blocks → ULB + TWAD                           🆓
│   ├── Roads & bridges
│   │     ├─ Internal/ward roads → ULB / GCC                               🆓 (→1913)
│   │     ├─ State highways / major district roads → TN Highways / PWD     🆓 (⚠️ no toll-free; via 1100)
│   │     ├─ National highways → NHAI                                      🆓 (→1033)
│   │     └─ Road-cut restoration after digging → GCC + cutting agency     🆓
│   ├── Storm-water drains & flood control → ULB / GCC                     🆓
│   └── Street lighting → ULB Electrical / GCC                             🆓
│
├── II. SANITATION, PUBLIC HEALTH & URBAN PLANNING
│   ├── Solid waste & conservancy — ULB / GCC / Village Panchayat
│   │     ├─ Garbage not collected / bins / door-to-door / segregation     🆓
│   │     ├─ Dead-animal removal, C&D debris (💰 fee+fine), burning         🆓/💰
│   │     └─ Illegal / legacy dumps (TNPCB, NGT-monitored)                 🆓
│   ├── Sanitation & public toilets — ULB  (pay-and-use = 💰)              🆓
│   ├── Public health — ULB Health / PHC / State Food Safety
│   │     ├─ Mosquito/dengue fogging; stray dogs (ABC); stray cattle (💰 fine) 🆓
│   │     └─ Unsanitary eateries / food safety → TN Food Safety Dept (NOT ULB) 🆓 (→9444042322)
│   ├── Town & country planning / buildings — CMDA (Chennai) / DTCP (rest) / ULB
│   │     ├─ Unauthorised construction / deviation (Sec 56/113-C)          🆓 (💰 regularise)
│   │     ├─ Building plan approval                                        💰
│   │     ├─ Encroachment on public land / roads / OSR                     🆓
│   │     └─ Illegal hoardings / flex / banners                            🆓 (💰 licence)
│   ├── Parks / playgrounds / markets / bus stands — ULB                   🆓 (💰 rent/fees)
│   └── Burial & cremation grounds — ULB / Village Panchayat               🆓
│
└── III. RECORDS, REVENUE, WELFARE & e-GOVERNANCE
    ├── Vital records — ULB + e-Sevai / Registration Dept
    │     ├─ Birth / Death certificate (ULB + e-Sevai)                     💰+🆓
    │     └─ Marriage registration (TNREGINET)                             💰+🆓
    ├── Municipal revenue — ULB / TN Urban e-Pay (GCC separate)
    │     ├─ Property tax, professional tax, vacant-land tax               💰+🆓
    │     ├─ Water/UGD tax; Trade licence; D&O licence                     💰+🆓
    │     └─ Rural: village-panchayat house/water/prof tax (vptax.tnrd)    💰+🆓
    ├── e-Sevai / TNeGA citizen services  (needs CAN)
    │     ├─ Community / Income / Nativity / OBC / First-Graduate certs    💰+🆓
    │     ├─ Patta / Chitta & transfer (Revenue: VAO+Tahsildar)            💰+🆓
    │     └─ Encumbrance certificate (TNREGINET)                           💰+🆓
    ├── PDS & welfare — Food & Civil Supplies / TNCSC / Social Welfare
    │     ├─ Ration/smart card (new/correction/surrender); PDS supply      🆓
    │     └─ Social-security pensions (OAP/widow/disability); welfare schemes 🆓
    └── Grievance channels (the routing targets themselves)
          ├─ CM Helpline 1100 / IIPGCMS (statewide, trackable)            🆓
          ├─ Ooratchi Mani 155340 (rural, RD&PR)                          🆓
          ├─ Makkaludan Mudhalvar camps (Revenue, 44 svc / 15 depts)      🆓
          └─ NHAI 1033 · CPGRAMS (central-funded overlap)                 🆓
```

---

## 2. The problems per domain (the "why this matters" — sourced)

### I. Utilities & infrastructure
- **Jurisdiction ambiguity is the #1 systemic failure citizens hit.** Chennai road/water/light
  complaints bounce between **GCC ↔ CMWSSB ↔ TNPDCL**; rural water between **panchayat ↔ TWAD**;
  roads between **GCC ↔ Highways ↔ NHAI**. Road-cut restoration stalls on NOC disputes (Tondiarpet:
  only 27 of 79 roads handed back). ([Citizen Matters](https://citizenmatters.in/chennai-road-digging-coc-cmwssb-tneb-brr-sewage-potholes/))
- **Electricity:** high-bill/meter disputes must climb to the **CGRF (TNERC)**; **solar net-metering
  delays** so chronic that TNERC imposed a **₹500/day penalty** on officials and scrapped the
  feasibility study for ≤10 kW. ([inkl/ETEnergyworld](https://www.inkl.com/news/tnerc-directs-tangedco-to-clear-pending-solar-rooftop-applications))
- **Water:** CAG audit (Sep 2025) — **50% of targeted households below the mandated 55 lpcd** under
  Jal Jeevan Mission; recurring **sewage ingress into drinking water**; rural scarcity (supply once
  in 3–25 days; families spending ₹36k/yr on private tankers). ([DTNext](https://www.dtnext.in/news/tamilnadu/jal-jeevan-mission-50-percent-households-face-water-shortfall-in-tamil-nadu-says-cag-report))
- **Roads/SWD/lights:** complaints **closed without a fix / falsely marked resolved**; potholes
  filled with **debris not bitumen**; **Cyclone Fengal — 553 waterlogged pockets**; GCC survey (Aug
  2025) — **>41,000 dysfunctional streetlights**. ([Citizen Matters](https://citizenmatters.in/complaint-against-potholes-in-chennai-grievance-redressal-by-corporation/) · [DTNext](https://www.dtnext.in/news/chennai/more-than-40000-streetlights-dysfunctional-across-chennai-reveals-gcc-survey-844468))

### II. Sanitation, health & planning
- **Waste:** NGT OA 606/2018 — ~2,000+ TPD **source-segregation gap**; **1913/Namma Chennai
  unreachable in the Dec 2023 floods**; C&D dumping (₹5,000/tonne fine, 15 zones). ([NGT report](https://www.greentribunal.gov.in/sites/default/files/news_updates/HALF%20YEARLY%20REPORT%20BY%20GOVT.%20OF%20TAMIL%20NADU%20IN%20OA%20NO.%20606%20of%202018%20(COMPLIANCE%20OF%20MSW%20MGT%20RULES,%202016%20AND%20OTHER%20ENV.%20ISSUES).pdf))
- **Toilets:** field audit — **>75% unclean/unsafe**; diffuse ownership (155 ward councillors
  control division toilets); women/PwD access near-absent. ([DTNext](https://www.dtnext.in/amp/story/news/chennai/the-dirty-picture-over-75-of-public-toilets-unclean-unsafe))
- **Public health:** inconsistent fogging (staff vacancies); stray-cattle fine escalated to
  ₹10,000+; **food safety is a separate state channel**, not the ULB. ([Citizen Matters](https://citizenmatters.in/chennais-mosquito-menace-fogging-drone-spray-polluted-drains-rivers-gcc/))
- **Planning:** OSR/public-land encroachment complaints via GCC portal **produce no action**
  (Kannagi Nagar); illegal hoardings reappear despite periodic drives (3,400 removed in a day). ([DTNext](https://www.dtnext.in/news/chennai/chennai-encroachments-on-pavements-osr-land-in-kannagi-nagar-trigger-political-sparring))
- **Burial grounds:** the most frequent complaint is **caste segregation / access denial** (Madras
  HC pushing common grounds). ([TNM](https://www.thenewsminute.com/article/denied-access-crematorium-madurai-dalits-forced-wait-corpse-rain-108246))

### III. Records, revenue, welfare & e-gov
- **e-Sevai outages:** a glitch once **shut 666 e-Sevai centres statewide for ~a week**; Chennai's
  online **death-certificate facility "comatose."** ([DTNext](https://www.dtnext.in/news/tamilnadu/software-glitch-shuts-down-666-eseva-centres-across-tamil-nadu))
- **Property tax online:** recurring **"money debited, no receipt"** (Avadi 2026; GCC ~10%
  affected); rural tax bills delayed **75+ days** by a software update. ([DTNext](https://www.dtnext.in/news/chennai/no-receipt-for-taxes-paid-on-tamil-nadu-urban-e-sevai-app-concerns-avadi-residents))
- **Certificates:** the **CAN gate** + document-rejection cycles; low-literacy users wholly
  dependent on centre operators.
- **Patta/Chitta:** delays, record errors, and **documented bribery** (DVAC trap, 2024); Madras HC:
  *"corruption emanates from Revenue Dept."* ([DTNext](https://www.dtnext.in/amp/story/news/tamilnadu/corruption-emanates-from-revenue-dept-madras-high-court))
- **PDS/pensions:** new ration-card printing **halted, 1 lakh+ stranded**; **~20 lakh** missed a
  pension payout (central SNA-SPARSH portal failure); unexplained multi-month stoppages. ([DTNext](https://www.dtnext.in/news/tamilnadu/tamil-nadu-over-a-lakh-waiting-for-ration-cards-since-may-854833))

---

## 3. Consolidated channel & SLA table (seed for Kural's router + clock)

| Domain | Primary channel | Owning body | Published SLA (if any) |
|---|---|---|---|
| Electricity | **1912** / WhatsApp / CGRF | TNPDCL/TANGEDCO | solar net-meter: 1 wk post-meter (CGRF-ordered) |
| Water/sewer — Chennai | **1916** / 044-4567-4567 | CMWSSB | tanker: 2-day assured ⚠️ |
| Water — rest of TN | **PUNAL** (punal.tn.gov.in) / WhatsApp 9499991916 | TWAD + ULB | — |
| Roads/SWD/lights — Chennai | **1913** / Namma Chennai app | GCC | pothole fill: 3 days (often missed) |
| National highways | **1033** / RajmargYatra | NHAI | — |
| State highways/PWD | ⚠️ no toll-free → **1100** | Highways/PWD | — |
| Waste/health/parks | **1913** (Chennai); ULB elsewhere | ULB/GCC | — |
| Food safety | **9444042322** (WhatsApp) | TN Food Safety Dept | — |
| Rural civic (all) | **Ooratchi Mani 155340** | RD&PR | **water 1d · lights 2d · garbage 2d · roads 5d** |
| Statewide fallback | **CM Helpline 1100 / IIPGCMS** | CM Cell / TNeGA | "time-bound per citizen charter" |
| Doorstep camps | Makkaludan Mudhalvar | Revenue Dept | **30-day** merit resolution |
| Certificates/tax/land | e-Sevai · TN Urban e-Pay · TNREGINET | TNeGA / Revenue | trade licence 15–30 d |

> **The Ooratchi Mani SLAs (water 1d / lights 2d / garbage 2d / roads 5d) and the 30-day Makkaludan
> target are the hardest published numbers found — use them directly to seed Kural's per-category SLA clock.**

---

## 4. The three cross-cutting findings that ARE Kural's pitch

1. **Jurisdiction ambiguity is the single most-cited failure** → Kural's **auto-router** attacks the
   #1 problem head-on. (Chennai = GCC + CMWSSB + TNPDCL; rest = ULB/panchayat + TWAD; roads span
   GCC/Highways/NHAI; food safety ≠ ULB; planning = CMDA vs DTCP.)
2. **"False closure" + no real tracking** is the top *process* grievance → Kural's **independent SLA
   clock + ticket tracking + auto-escalation** is a genuine differentiator the state system lacks.
3. **Low-literacy / rural citizens are structurally under-served** (the state literally created
   Makkaludan Mudhalvar *camps* because people can't navigate 15 departments) → validates Kural's
   **Tamil voice-call-first** thesis better than any slide.

---

## 5. Kural feasibility map (which services to actually support)

| Tier | Services | Why | Demo? |
|---|---|---|---|
| **Tier 1 — build now** | Electricity (outage/high-bill), Water (no-supply/contamination), Waste (garbage/bins), Streetlight, Drainage/overflow | High call volume, clear owning body, simple to state verbally, strong SLAs | ✅ core demo |
| **Tier 2 — support, lighter** | Roads/potholes, stray animals, public toilets, sewage | Common but routing nuance (GCC vs Highways; ULB vs CMWSSB) | ✅ 1–2 examples |
| **Tier 3 — classify + redirect only** | Certificates, patta, property tax, ration/pension | Transactional, need auth/documents — voice can *capture + redirect to e-Sevai/1100*, not resolve | 🔎 mention as roadmap |

**Three worked demo scenarios (one per segment) — your "three cases":**
1. **Utilities (urban):** *"Enga area-la current போயி 3 naal aachu, transformer-la spark"* → Electricity/outage → **TNPDCL**, zone, SLA 1912-class → ticket + SMS.
2. **Sanitation (rural):** *"village-la garbage collect பண்றதில்லை, bins overflow"* → Waste → **Village Panchayat / Ooratchi Mani**, SLA 2 days → ticket, escalate if cluster.
3. **Records/revenue (cross-agency):** *"property tax online pay பண்ணேன், money போச்சு receipt வரலை"* → Revenue/e-Pay failure → **ULB Revenue**, capture + redirect + ticket.

These three exercise the whole pipeline (voice → classify → **resolve owning body** → ticket → SLA
→ escalate) across all three service families — perfect for the dashboard you want next.

---

## 6. Open verification items (before production, not before the demo)
TNPDCL migration of 1912 routing; CMWSSB numbers (official .gov.in host was IP-blocked — news-sourced);
DTCP complaint portal; D&O-licence & EC complaint data; official **1100 disposal/pendency stats**
(not public); currency of 2025 hoarding numbers, cattle fines, ration-print targets.

*(Full per-source citations for every claim live in the three staged segment files + inline links above.)*
