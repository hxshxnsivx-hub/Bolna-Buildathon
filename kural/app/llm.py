"""Provider-agnostic LLM helper (OpenAI-compatible).

Works with OpenAI, Groq, Google Gemini (OpenAI-compat endpoint), Sarvam-M, or OpenRouter —
just set env (LLM_API_KEY / LLM_BASE_URL / LLM_MODEL). Returns None on ANY failure so callers
fall back to heuristics; Kural never hard-depends on an LLM or on a specific vendor."""

import os
import json


def _config():
    key = (os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
           or os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY"))
    base = os.getenv("LLM_BASE_URL") or None          # None => OpenAI default
    model = os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    return key, base, model


def available() -> bool:
    return bool(_config()[0])


def chat_json(system: str, user: str) -> dict | None:
    """One-shot JSON completion. None on no-key or any error."""
    key, base, model = _config()
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=base) if base else OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            response_format={"type": "json_object"}, temperature=0)
        return json.loads(resp.choices[0].message.content)
    except Exception as e:                      # noqa: BLE001
        print(f"[llm fallback] {e}")
        return None
