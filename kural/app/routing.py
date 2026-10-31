"""Deterministic owning-body resolver — the heart of Kural.

Given a civic-grievance SECTOR (+ the caller's location/region), return the single government
body + department + field cadre + official channel + SLA that owns it. Covers ALL civic-service
classes and sub-classes from the R&D master tree (docs/research/04): utilities, sanitation /
health / planning, and records / revenue / welfare / e-governance.

This is a plain lookup table, NOT an LLM: the LLM does the fuzzy understanding (speech ->
{sector, locality, severity}); ownership resolution is deterministic so it is auditable and can
never be hallucinated. Anything unmapped falls back to the statewide CM Helpline (1100), so the
router is always valid for any complaint.
"""

import re
from dataclasses import dataclass, asdict
from typing import Optional

REGION_CHENNAI = "chennai"   # Greater Chennai Corporation area
REGION_URBAN = "urban"       # other corporations / municipalities / town panchayats
REGION_RURAL = "rural"       # village panchayats
REGIONS = (REGION_CHENNAI, REGION_URBAN, REGION_RURAL)

# Canonical sectors / sub-classes the voice agent classifies into (full civic-service tree).
SECTORS = [
    # --- I. Utilities & physical infrastructure ---
    "electricity", "water_supply", "sewerage", "roads_internal", "roads_highway",
    "roads_national", "stormwater", "streetlight",
    # --- II. Sanitation, public health & urban planning ---
    "solid_waste", "sanitation_toilet", "public_health", "stray_animals", "food_safety",
    "town_planning", "building_approval", "hoardings", "parks", "burial_grounds",
    # --- III. Records, revenue, welfare & e-governance ---
    "birth_certificate", "death_certificate", "marriage_registration",
    "property_tax", "professional_tax", "trade_licence",
    "community_certificate", "income_certificate", "nativity_certificate",
    "patta_chitta", "encumbrance_certificate", "ration_card", "pension",
    "other",
]

_DEFAULT_SLA = 15

# Normalise the loose phrasing an LLM may emit into a canonical sector key.
_ALIASES = {
    "power": "electricity", "eb": "electricity", "current": "electricity",
    "electricity_bill": "electricity", "water": "water_supply", "drinking_water": "water_supply",
    "drainage": "sewerage", "garbage": "solid_waste", "trash": "solid_waste",
    "waste": "solid_waste", "road": "roads_internal", "pothole": "roads_internal",
    "street_light": "streetlight", "street_lights": "streetlight",
    "mosquito": "public_health", "dog": "stray_animals", "dogs": "stray_animals",
    "cattle": "stray_animals", "encroachment": "town_planning",
    "ration": "ration_card", "patta": "patta_chitta",
}


def normalize_sector(sector: str) -> str:
    """Canonicalise: lowercase, spaces/hyphens -> underscores, then alias-map."""
    s = (sector or "other").strip().lower().replace(" ", "_").replace("-", "_")
    if s not in TABLE and s in _ALIASES:
        s = _ALIASES[s]
    return s


@dataclass
class Routing:
    sector: str
    owning_body: str
    department: str
    field_cadre: str
    channel: str
    sla_days: int
    region: str = ""
    city: str = ""
    note: str = ""

    def as_dict(self):
        return asdict(self)


# Major TN cities -> (corporation name, is_chennai). Routes ULB-owned issues to the right city
# body and infers region. Electricity stays TNPDCL statewide but records the city.
CITY_CORP = {
    "chennai": ("Greater Chennai Corporation", True),
    "coimbatore": ("Coimbatore City Municipal Corporation", False),
    "kuniyamuthur": ("Coimbatore City Municipal Corporation", False),
    "madurai": ("Madurai Municipal Corporation", False),
    "trichy": ("Tiruchirappalli City Municipal Corporation", False),
    "tiruchirappalli": ("Tiruchirappalli City Municipal Corporation", False),
    "salem": ("Salem City Municipal Corporation", False),
    "tirunelveli": ("Tirunelveli City Municipal Corporation", False),
    "erode": ("Erode City Municipal Corporation", False),
    "vellore": ("Vellore City Municipal Corporation", False),
    "thoothukudi": ("Thoothukudi City Municipal Corporation", False),
    "tuticorin": ("Thoothukudi City Municipal Corporation", False),
    "tiruppur": ("Tiruppur City Municipal Corporation", False),
    "thanjavur": ("Thanjavur Municipal Corporation", False),
    "dindigul": ("Dindigul Municipal Corporation", False),
}


def resolve_city(text):
    """Match a known city as a WHOLE token (so 'eroded' no longer matches 'erode')."""
    toks = set(re.findall(r"[a-z]+", (text or "").lower()))
    for city, (corp, is_chennai) in CITY_CORP.items():
        if city in toks:
            return city, corp, is_chennai
    return None, None, None


def _r(owning_body, department, field_cadre, channel, sla_days, note=""):
    return dict(owning_body=owning_body, department=department, field_cadre=field_cadre,
                channel=channel, sla_days=sla_days, note=note)


# TABLE[sector][region] -> partial routing. "*" applies to every region.
TABLE = {
    # ---------------- I. Utilities & physical infrastructure ----------------
    "electricity": {
        "*": _r("TNPDCL (TANGEDCO/TNEB)", "Distribution", "Section Office / Lineman",
                "1912", 2, "Billing/meter disputes escalate to CGRF -> TNERC."),
    },
    "water_supply": {
        REGION_CHENNAI: _r("CMWSSB (Chennai Metro Water)", "Water Supply",
                           "Area Engineer / Depot", "1916", 1),
        REGION_URBAN: _r("TWAD Board + ULB", "Water Supply", "Municipal Engineer",
                         "PUNAL (punal.tn.gov.in)", 1),
        REGION_RURAL: _r("TWAD Board + Village Panchayat", "Water Supply",
                         "Panchayat Secretary", "Ooratchi Mani 155340", 1),
    },
    "sewerage": {
        REGION_CHENNAI: _r("CMWSSB (Chennai Metro Water)", "Sewerage / UGD",
                           "Area Engineer", "1916", 3),
        "*": _r("ULB + TWAD", "Sewerage / UGD", "Municipal Engineer", "ULB / 1913", 3),
    },
    "roads_internal": {
        REGION_CHENNAI: _r("Greater Chennai Corporation", "Engineering",
                           "Junior Engineer", "1913", 5),
        REGION_URBAN: _r("Urban Local Body", "Engineering", "Junior Engineer",
                         "ULB helpline", 5),
        REGION_RURAL: _r("Village Panchayat / Block", "Engineering",
                         "Panchayat Secretary", "Ooratchi Mani 155340", 5),
    },
    "roads_highway": {
        "*": _r("TN Highways Dept / PWD", "Highways", "Assistant Engineer",
                "CM Helpline 1100", 7, "State highways / major district roads."),
    },
    "roads_national": {
        "*": _r("NHAI", "Highways", "Project Director", "1033", 7,
                "National highways; RajmargYatra app / CPGRAMS."),
    },
    "stormwater": {
        REGION_CHENNAI: _r("Greater Chennai Corporation", "Storm Water Drain",
                           "Junior Engineer", "1913", 3),
        "*": _r("Urban Local Body", "Storm Water Drain", "Junior Engineer",
                "ULB helpline", 3),
    },
    "streetlight": {
        REGION_CHENNAI: _r("Greater Chennai Corporation", "Engineering (Electrical)",
                           "Junior Engineer", "1913", 2),
        REGION_URBAN: _r("Urban Local Body", "Engineering (Electrical)",
                         "Junior Engineer", "ULB helpline", 2),
        REGION_RURAL: _r("Village Panchayat", "Electrical", "Panchayat Secretary",
                         "Ooratchi Mani 155340", 2),
    },

    # ---------------- II. Sanitation, public health & urban planning ----------------
    "solid_waste": {
        REGION_CHENNAI: _r("Greater Chennai Corporation", "Public Health / Conservancy",
                           "Sanitary Inspector", "1913", 2),
        REGION_URBAN: _r("Urban Local Body", "Public Health", "Sanitary Inspector",
                         "ULB helpline", 2),
        REGION_RURAL: _r("Village Panchayat", "Sanitation", "Panchayat Secretary",
                         "Ooratchi Mani 155340", 2),
    },
    "sanitation_toilet": {
        "*": _r("Urban Local Body / GCC", "Public Health", "Sanitary Inspector",
                "1913 / ULB", 3),
    },
    "public_health": {
        "*": _r("ULB Health Dept", "Public Health (Vector Control)", "Sanitary Inspector",
                "1913 / ULB", 3, "Mosquito/dengue fogging, hygiene nuisances."),
    },
    "stray_animals": {
        "*": _r("Urban Local Body", "Veterinary / Public Health", "Veterinary Officer",
                "1913 / ULB", 5, "Stray dogs (ABC), stray cattle (owner fine)."),
    },
    "food_safety": {
        "*": _r("TN Food Safety Dept (State Health)", "Food Safety", "Food Safety Officer",
                "9444042322 (WhatsApp)", 7, "Unhygienic eateries / adulteration — NOT the ULB."),
    },
    "town_planning": {
        REGION_CHENNAI: _r("CMDA", "Enforcement", "Town Planning Inspector",
                           "CMDA (cmdachennai.gov.in)", 15,
                           "Unauthorised construction / deviation / encroachment (Sec 56)."),
        "*": _r("DTCP / ULB", "Town Planning", "Town Planning Inspector",
                "DTCP / ULB", 15, "Unauthorised construction / encroachment."),
    },
    "building_approval": {
        REGION_CHENNAI: _r("CMDA", "Planning Permission", "Planning Officer",
                           "CMDA", 30, "💰 Building plan approval (statutory fees)."),
        "*": _r("DTCP / ULB", "Planning Permission", "Planning Officer",
                "DTCP / ULB", 30, "💰 Building plan approval."),
    },
    "hoardings": {
        "*": _r("Urban Local Body / GCC", "Licensing", "Licensing Inspector",
                "1913 / ULB", 7, "Illegal flex / banners / hoardings."),
    },
    "parks": {
        "*": _r("Urban Local Body", "Parks & Playfields", "Parks Supervisor",
                "1913 / ULB", 10, "Parks, playgrounds, markets, bus stands upkeep."),
    },
    "burial_grounds": {
        REGION_RURAL: _r("Village Panchayat", "Sanitation", "Panchayat Secretary",
                         "Ooratchi Mani 155340", 10, "Maintenance / access."),
        "*": _r("Urban Local Body", "Public Health", "Sanitary Inspector",
                "1913 / ULB", 10, "Burial/cremation ground maintenance / access."),
    },

    # ---------------- III. Records, revenue, welfare & e-governance ----------------
    "birth_certificate": {
        "*": _r("Urban Local Body + e-Sevai", "Registration of Births & Deaths",
                "Registrar (B&D)", "e-Sevai / tnesevai.tn.gov.in", 15,
                "Transactional: capture + guide to e-Sevai."),
    },
    "death_certificate": {
        "*": _r("Urban Local Body + e-Sevai", "Registration of Births & Deaths",
                "Registrar (B&D)", "e-Sevai / tnesevai.tn.gov.in", 15),
    },
    "marriage_registration": {
        "*": _r("Registration Dept (TNREGINET)", "Registration", "Sub-Registrar",
                "tnreginet.gov.in", 15),
    },
    "property_tax": {
        "*": _r("Urban Local Body (Revenue)", "Revenue", "Revenue Inspector",
                "TN Urban e-Pay / ULB", 15, "Transactional: capture + redirect to e-Pay."),
    },
    "professional_tax": {
        "*": _r("Urban Local Body (Revenue)", "Revenue", "Revenue Inspector",
                "TN Urban e-Pay / ULB", 15),
    },
    "trade_licence": {
        "*": _r("Urban Local Body", "Licensing", "Sanitary Inspector (verification)",
                "TN Urban e-Pay / ULB", 20, "💰 Trade / D&O licence."),
    },
    "community_certificate": {
        "*": _r("Revenue Dept (Tahsildar/RDO)", "Revenue", "VAO / Tahsildar",
                "e-Sevai (needs CAN)", 15, "Appeal rejections to the RDO."),
    },
    "income_certificate": {
        "*": _r("Revenue Dept (Tahsildar)", "Revenue", "VAO / Tahsildar",
                "e-Sevai (needs CAN)", 15),
    },
    "nativity_certificate": {
        "*": _r("Revenue Dept (Tahsildar/RDO)", "Revenue", "VAO / Tahsildar",
                "e-Sevai (needs CAN)", 15),
    },
    "patta_chitta": {
        "*": _r("Revenue Dept", "Survey & Land Records", "VAO + Tahsildar",
                "Tamil Nilam / e-Sevai", 30, "Transfer delays -> Tahsildar -> RTI."),
    },
    "encumbrance_certificate": {
        "*": _r("Registration Dept (TNREGINET)", "Registration", "Sub-Registrar",
                "tnreginet.gov.in", 7),
    },
    "ration_card": {
        "*": _r("Food & Civil Supplies Dept / TNCSC", "PDS", "Taluk Supply Officer",
                "TNPDS (tnpds.gov.in)", 30, "New / correction / surrender."),
    },
    "pension": {
        "*": _r("Social Welfare / Revenue (District)", "Social Security", "VAO / Collectorate",
                "CM Helpline 1100", 30, "OAP / widow / disability pensions."),
    },
}

# Safe fallback — the router is always valid: anything unmapped -> statewide helpline.
_FALLBACK = _r("CM Helpline (IIPGCMS)", "Routing Cell", "Case Officer",
               "1100", _DEFAULT_SLA, "Unmapped grievance -> statewide helpline.")


_RURAL = frozenset({"village", "panchayat", "gramam", "rural", "hamlet", "ooru", "oorani"})


def guess_region(locality_text: Optional[str]) -> str:
    """Whole-token rural check — 'thanjavur'/'floor' no longer mis-flag as rural."""
    t = (locality_text or "").lower()
    if "chennai" in t:
        return REGION_CHENNAI
    if _RURAL & set(re.findall(r"[a-z]+", t)):
        return REGION_RURAL
    return REGION_URBAN


def resolve(sector: str, region: Optional[str] = None,
            locality_text: Optional[str] = None) -> Routing:
    """(sector x region) -> the owning body that must act, specialised to the city. Never raises."""
    sector = normalize_sector(sector)
    city, corp, is_chennai = resolve_city(locality_text)
    if region:
        region = region.strip().lower()
    elif city:
        region = REGION_CHENNAI if is_chennai else REGION_URBAN
    else:
        region = guess_region(locality_text)
    if region not in REGIONS:
        region = guess_region(locality_text)

    entry = TABLE.get(sector)
    if entry is None:
        part = _FALLBACK
    else:
        part = entry.get(region) or entry.get("*") or next(iter(entry.values()))
    r = Routing(sector=sector, region=region, city=(city or ""), **part)
    if corp and r.owning_body in ("Urban Local Body", "Greater Chennai Corporation",
                                  "Urban Local Body / GCC"):
        r.owning_body = corp
    return r
