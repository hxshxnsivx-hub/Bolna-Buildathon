"""Deterministic owning-body resolver — the heart of Kural.

Given a civic-grievance SECTOR and the caller's REGION, return the single
government body + department + field cadre + official channel + SLA that owns it.

This is intentionally a plain lookup table, NOT an LLM: in Kural the LLM does the
fuzzy *understanding* (speech -> {sector, locality, severity}), but the *ownership
resolution* is deterministic so it is auditable and can never be hallucinated.
Seeded from the R&D dossiers (docs/research/01-04, docs/architecture/01).
"""

from dataclasses import dataclass, asdict
from typing import Optional

# Regions we distinguish. locality text -> region is resolved by guess_region().
REGION_CHENNAI = "chennai"   # Greater Chennai Corporation area
REGION_URBAN = "urban"       # other corporations / municipalities / town panchayats
REGION_RURAL = "rural"       # village panchayats
REGIONS = (REGION_CHENNAI, REGION_URBAN, REGION_RURAL)

# Canonical sectors the voice agent classifies into.
SECTORS = [
    "electricity", "water_supply", "sewerage", "roads_internal", "roads_highway",
    "stormwater", "streetlight", "solid_waste", "sanitation_toilet",
    "public_health", "stray_animals", "town_planning", "property_tax", "other",
]

# SLA day anchors (business days). Hard published numbers where they exist:
# Ooratchi Mani — water 1, streetlight 2, garbage 2, roads 5; else GCC grievance 15.
_DEFAULT_SLA = 15


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


# Major TN cities -> (corporation name, is_chennai). Used to route ULB-owned issues to the
# right city body and to infer the region. Electricity stays TNPDCL statewide but records the city.
CITY_CORP = {
    "chennai": ("Greater Chennai Corporation", True),
    "coimbatore": ("Coimbatore City Municipal Corporation", False),
    "kuniyamuthur": ("Coimbatore City Municipal Corporation", False),   # Coimbatore locality
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
    """Find a known TN city/locality in free text -> (city_key, corporation, is_chennai)."""
    t = (text or "").lower()
    for city, (corp, is_chennai) in CITY_CORP.items():
        if city in t:
            return city, corp, is_chennai
    return None, None, None


def _r(owning_body, department, field_cadre, channel, sla_days, note=""):
    # partial Routing (sector/region filled in by resolve())
    return dict(owning_body=owning_body, department=department,
                field_cadre=field_cadre, channel=channel,
                sla_days=sla_days, note=note)


# TABLE[sector][region] -> partial routing. "*" = applies to every region.
TABLE = {
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
                "CM Helpline 1100", 7,
                "National highways -> NHAI 1033; no state-highway toll-free line."),
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
        "*": _r("ULB Health Dept", "Public Health", "Sanitary Inspector",
                "1913 / ULB", 3,
                "Food-safety complaints go to TN Food Safety Dept (9444042322), not the ULB."),
    },
    "stray_animals": {
        "*": _r("Urban Local Body", "Veterinary / Public Health", "Veterinary Officer",
                "1913 / ULB", 5),
    },
    "town_planning": {
        REGION_CHENNAI: _r("CMDA", "Enforcement", "Town Planning Inspector",
                           "CMDA (cmdachennai.gov.in)", 15,
                           "Unauthorised construction / encroachment."),
        "*": _r("DTCP / ULB", "Town Planning", "Town Planning Inspector",
                "DTCP / ULB", 15),
    },
    "property_tax": {
        "*": _r("Urban Local Body (Revenue)", "Revenue", "Revenue Inspector",
                "TN Urban e-Pay / ULB", 15,
                "Transactional: capture + redirect to e-Pay, not resolved on call."),
    },
}

# Safe fallback when the sector is unknown / unmapped.
_FALLBACK = _r("CM Helpline (IIPGCMS)", "Routing Cell", "Case Officer",
               "1100", _DEFAULT_SLA, "Unmapped sector -> statewide helpline.")


def guess_region(locality_text: Optional[str]) -> str:
    """Cheap heuristic: locality string -> region. The agent may override this."""
    t = (locality_text or "").lower()
    if "chennai" in t:
        return REGION_CHENNAI
    rural_markers = ("village", "panchayat", "gramam", "oor", "ur ", "rural", "hamlet")
    if any(m in t for m in rural_markers):
        return REGION_RURAL
    return REGION_URBAN


def resolve(sector: str, region: Optional[str] = None,
            locality_text: Optional[str] = None) -> Routing:
    """(sector x region) -> the owning body that must act, specialised to the city. Never raises."""
    sector = (sector or "other").strip().lower()
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
    # specialise a generic ULB/GCC owner to the actual city corporation when we know the city
    if corp and r.owning_body in ("Urban Local Body", "Greater Chennai Corporation"):
        r.owning_body = corp
    return r
