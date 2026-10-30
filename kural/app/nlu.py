"""Understanding layer: free-text (Tanglish) utterance -> {sector, severity, region, locality}.

Used for the TEXT demo mode (no telephony needed) and as a server-side fallback.
In production the Bolna voice agent does this extraction and calls /grievance directly.
Uses the LLM when OPENAI_API_KEY is set; otherwise a transparent keyword heuristic."""

from .routing import SECTORS, guess_region
from . import llm

# Tanglish / Tamil / English keyword cues per sector (lowercased substring match).
_CUES = {
    # --- utilities ---
    "electricity": ["current", "power", "powercut", "eb ", "tangedco", "tnpdcl", "transformer",
                    "voltage", "electricity bill", "meter", "மின்", "கரண்ட்", "மின்சாரம்"],
    "water_supply": ["water", "thanni", "tanker", "pipe", "supply", "தண்ணி", "தண்ணீர்", "குடிநீர்"],
    "sewerage": ["sewage", "sewer", "drainage", "manhole", "ugd", "சாக்கடை", "கழிவுநீர்"],
    "roads_national": ["national highway", "nhai", "nh ", "toll"],
    "roads_highway": ["state highway", "highway", "நெடுஞ்சாலை", "bypass"],
    "roads_internal": ["road", "pothole", "ரோடு", "சாலை", "குழி"],
    "stormwater": ["flood", "waterlogging", "stagnat", "தண்ணீர் தேங்", "வெள்ளம்"],
    "streetlight": ["street light", "streetlight", "lamp", "விளக்கு", "தெரு விளக்கு"],
    # --- sanitation / health / planning ---
    "food_safety": ["food safety", "adulterat", "unhygienic", "restaurant", "hotel food", "உணவு பாதுகாப்பு"],
    "solid_waste": ["garbage", "waste", "trash", "bin", "kuppai", "குப்பை", "கழிவு"],
    "sanitation_toilet": ["toilet", "கழிப்பிடம்", "latrine"],
    "public_health": ["mosquito", "dengue", "fogging", "கொசு", "டெங்கு"],
    "stray_animals": ["dog", "cattle", "cow", "நாய்", "மாடு", "stray"],
    "building_approval": ["building plan", "plan approval", "building permit", "கட்டிட அனுமதி"],
    "town_planning": ["unauthorised", "unauthorized", "encroach", "illegal construction",
                      "ஆக்கிரமிப்பு"],
    "hoardings": ["hoarding", "banner", "flex", "விளம்பர"],
    "parks": ["park", "playground", "bus stand", "market", "பூங்கா"],
    "burial_grounds": ["burial", "cremation", "graveyard", "சுடுகாடு", "இடுகாடு"],
    # --- records / revenue / welfare ---
    "birth_certificate": ["birth certificate", "birth cert", "பிறப்பு சான்று"],
    "death_certificate": ["death certificate", "death cert", "இறப்பு சான்று"],
    "marriage_registration": ["marriage registration", "marriage register", "திருமண பதிவு"],
    "professional_tax": ["professional tax", "தொழில் வரி"],
    "property_tax": ["property tax", "house tax", "சொத்து வரி"],
    "trade_licence": ["trade licence", "trade license", "d&o licence", "வணிக உரிமம்"],
    "community_certificate": ["community certificate", "caste certificate", "சாதி சான்று", "சமுதாய சான்று"],
    "income_certificate": ["income certificate", "வருமான சான்று"],
    "nativity_certificate": ["nativity certificate", "பூர்வீக சான்று"],
    "patta_chitta": ["patta", "chitta", "பட்டா", "adangal", "land record"],
    "encumbrance_certificate": ["encumbrance", "ec certificate", "வில்லங்க"],
    "ration_card": ["ration card", "smart card", "குடும்ப அட்டை", "ரேஷன்"],
    "pension": ["pension", "old age pension", "widow pension", "ஓய்வூதியம்"],
}
_HIGH = ["accident", "விழுந்த", "விழுந்து", "injured", "danger", "spark", "fire", "தீ",
         "weeks", "வாரம்", "days", "நாள்", "naal", "emergency"]


def _heuristic(utterance: str) -> dict:
    t = (utterance or "").lower()
    sector = "other"
    for s, cues in _CUES.items():        # _CUES order = priority (specific sectors first)
        if any(cue in t for cue in cues):
            sector = s
            break
    severity = "high" if any(h in t for h in _HIGH) else "medium"
    return {"sector": sector, "severity": severity,
            "region": guess_region(utterance), "locality": utterance[:80]}


def _llm(utterance: str) -> dict | None:
    sys = ("You extract a Tamil/English civic grievance into JSON. "
           f"sector must be one of {SECTORS}. "
           "region is one of chennai|urban|rural. severity is low|medium|high. "
           "locality is the place mentioned (string). "
           'Respond ONLY as JSON: {"sector","severity","region","locality"}.')
    data = llm.chat_json(sys, utterance)
    if not data:
        return None
    if data.get("sector") not in SECTORS:
        data["sector"] = "other"
    return data


def classify(utterance: str) -> dict:
    return _llm(utterance) or _heuristic(utterance)
