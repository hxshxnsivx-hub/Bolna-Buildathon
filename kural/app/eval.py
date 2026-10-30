"""KuralEval — per-call quality scorecard, tuned for VERNACULAR (Tamil/English/Tanglish) voice.

Beyond generic ASR/task checks, it grades the things that actually break a code-mixed agent:
  - lang_switch_ok : was code-mixing (Tamil + English) present & handled
  - lang_match_ok  : did the AGENT answer in the caller's language (fails if caller spoke
                     Tamil/Tanglish and the agent replied English-only) — needs speaker-tagged turns
  - tamil_ratio    : % of Tamil-script characters (a mix measure)
  - romanized_tamil: did the caller use romanized Tamil ("thanni", "iruku") vs script
Plus task_complete, repair_ok, latency, hallucination, compliance.

LLM-as-judge for the 0/1 judgments when OPENAI_API_KEY is set; the language metrics are always
computed deterministically from the text. Falls back to a pure heuristic with no key."""

from . import llm

_TAMIL = range(0x0B80, 0x0C00)        # Tamil Unicode block
# Common romanized-Tamil ("Tanglish") markers — caller typing/speaking Tamil in Latin script.
_ROMAN = ("vanakkam", "thanni", "illa", "iruku", "irukku", "aagala", "aagla", "aachu", "naal",
          "enga", "romba", "seri", "sari", "panna", "pannu", "pannunga", "panni", "kuppai",
          "theru", "vandhu", "venum", "kedaikum", "anuppu", "pukar", "varala", "poachu", "poyi")


def _has_tamil(s): return any(ord(c) in _TAMIL for c in s)
def _has_latin(s): return any("a" <= c.lower() <= "z" for c in s)
def _has_roman_tamil(s):
    low = (s or "").lower()
    return any(w in low for w in _ROMAN)


def _tamil_ratio(s: str) -> int:
    t = sum(1 for c in s if ord(c) in _TAMIL)
    l = sum(1 for c in s if c.isascii() and c.isalpha())
    tot = t + l
    return round(100 * t / tot) if tot else 0


def _split_turns(call):
    """Return (user_text, agent_text) from speaker-tagged turns, if provided."""
    turns = call.get("turns") or []
    u = " ".join(t.get("text", "") for t in turns if t.get("speaker") == "user")
    a = " ".join(t.get("text", "") for t in turns if t.get("speaker") == "agent")
    return u, a, bool(turns)


def _lang_match(call) -> int:
    """1 if the agent matched the caller's language; 0 if caller used Tamil/Tanglish but the
    agent replied English-only. Without turns we can't tell -> assume ok (1)."""
    user, agent, have = _split_turns(call)
    if not (have and agent.strip()):
        return 1
    caller_tamil = _has_tamil(user) or _has_roman_tamil(user)
    agent_tamil = _has_tamil(agent) or _has_roman_tamil(agent)
    return 0 if (caller_tamil and not agent_tamil) else 1


def _finalize(flags: dict, call: dict, notes: str) -> dict:
    tr = call.get("transcript") or ""
    flags["lang_match_ok"] = flags.get("lang_match_ok", _lang_match(call))
    flags["tamil_ratio"] = _tamil_ratio(tr)
    flags["romanized_tamil"] = 1 if _has_roman_tamil(tr) else 0
    flags["latency_ms"] = call.get("latency_ms")
    binary = [flags.get(k, 0) for k in
              ("asr_ok", "lang_switch_ok", "lang_match_ok", "task_complete",
               "repair_ok", "compliance_ok")] + [1 - flags.get("hallucination", 0)]
    flags["overall"] = round(100 * sum(binary) / len(binary), 1)
    flags["notes"] = notes
    return flags


def _heuristic(call: dict) -> dict:
    tr = call.get("transcript") or ""
    low = tr.lower()
    flags = dict(
        asr_ok=1 if tr.strip() else 0,
        lang_switch_ok=1 if (_has_tamil(tr) and _has_latin(tr)) else 0,
        lang_match_ok=_lang_match(call),
        task_complete=1 if ("krl-" in low or "ticket" in low or "புகார்" in tr) else 0,
        repair_ok=1 if ("correct" in low or "சரி" in tr or "right" in low) else 0,
        hallucination=0, compliance_ok=1)
    return _finalize(flags, call, "heuristic")


def _llm(call: dict) -> dict | None:
    tr = call.get("transcript")
    if not tr:
        return None
    sys = ("You are a strict QA judge for a Tamil/English (Tanglish) civic voice agent. "
           "Return ONLY JSON with integer 0/1 fields: asr_ok, lang_switch_ok, lang_match_ok "
           "(did the agent reply in the caller's language?), task_complete, repair_ok, "
           "hallucination, compliance_ok, and a short 'notes' string.")
    d = llm.chat_json(sys, tr)
    if not d:
        return None
    flags = {k: int(d.get(k, 0)) for k in
             ("asr_ok", "lang_switch_ok", "lang_match_ok", "task_complete",
              "repair_ok", "hallucination", "compliance_ok")}
    return _finalize(flags, call, d.get("notes", "llm-judge"))


def run_eval(call: dict) -> dict:
    return _llm(call) or _heuristic(call)
