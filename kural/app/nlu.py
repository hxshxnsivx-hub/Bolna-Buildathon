"""Understanding layer: free-text (Tanglish) utterance -> {sector, severity, region, locality}.

Used for the TEXT demo mode (no telephony needed) and as a server-side fallback.
In production the Bolna voice agent does this extraction and calls /grievance directly.
Uses the LLM when OPENAI_API_KEY is set; otherwise a transparent keyword heuristic."""

from .routing import SECTORS, guess_region
from . import llm

# Tanglish / Tamil / English keyword cues per sector (lowercased substring match).
_CUES = {
    "electricity": ["current", "power", "powercut", "eb ", "tangedco", "tnpdcl", "transformer",
                     "voltage", "bill", "meter", "மின்", "கரண்ட்", "மின்சாரம்"],
    "water_supply": ["water", "thanni", "tanker", "pipe", "supply", "தண்ணி", "தண்ணீர்", "குடிநீர்"],
    "sewerage": ["sewage", "sewer", "drainage", "manhole", "ugd", "சாக்கடை", "கழிவுநீர்"],
    "roads_internal": ["road", "pothole", "ரோடு", "சாலை", "குழி", "pothole"],
    "roads_highway": ["highway", "நெடுஞ்சாலை", "nh ", "bypass"],
    "stormwater": ["flood", "waterlogging", "stagnat", "தண்ணீர் தேங்", "வெள்ளம்"],
    "streetlight": ["street light", "streetlight", "lamp", "விளக்கு", "தெரு விளக்கு"],
    "solid_waste": ["garbage", "waste", "trash", "bin", "kuppai", "குப்பை", "கழிவு"],
    "sanitation_toilet": ["toilet", "கழிப்பிடம்", "latrine"],
    "public_health": ["mosquito", "dengue", "fogging", "கொசு", "டெங்கு"],
    "stray_animals": ["dog", "cattle", "cow", "நாய்", "மாடு", "stray"],
    "town_planning": ["construction", "encroach", "building", "ஆக்கிரமிப்பு", "கட்டிடம்"],
    "property_tax": ["tax", "வரி", "property tax", "receipt"],
}
_HIGH = ["accident", "விழுந்த", "விழுந்து", "injured", "danger", "spark", "fire", "தீ",
         "weeks", "வாரம்", "days", "நாள்", "naal", "emergency"]


def _heuristic(utterance: str) -> dict:
    t = (utterance or "").lower()
    sector = "other"
    for s in SECTORS:
        for cue in _CUES.get(s, []):
            if cue in t:
                sector = s
                break
        if sector != "other":
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
