"""API schemas — the stable Agent <-> Brain contract (docs/architecture/01 Section 4)."""

from typing import Optional, List
from pydantic import BaseModel, Field


class Caller(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    raw_address: Optional[str] = None


class Locality(BaseModel):
    text: Optional[str] = None
    region: Optional[str] = None     # chennai | urban | rural (agent may omit -> guessed)
    ward: Optional[str] = None
    zone: Optional[str] = None


class Extracted(BaseModel):
    sector: str = "other"
    locality: Locality = Field(default_factory=Locality)
    severity: str = "medium"         # low | medium | high
    language_mix: List[str] = Field(default_factory=lambda: ["ta", "en"])


class GrievanceIn(BaseModel):
    call_id: Optional[str] = None
    caller: Caller = Field(default_factory=Caller)
    utterance: Optional[str] = None
    extracted: Extracted = Field(default_factory=Extracted)


class GrievanceOut(BaseModel):
    ticket_id: str
    owning_body: str
    department: str
    field_cadre: str
    zone: Optional[str] = None
    channel: str
    region: str
    sla_days: int
    due_at: str
    sms_sent: bool
    duplicate_of: Optional[str] = None
    cluster_size: int = 1
    spoken_confirmation: str = ""    # Tanglish line the agent can read back


class ClassifyIn(BaseModel):
    """Demo/text mode: free-text utterance -> structured grievance (no telephony needed)."""
    utterance: str
    caller: Caller = Field(default_factory=Caller)


class CallWebhookIn(BaseModel):
    """Bolna post-call webhook payload (subset) -> drives KuralEval."""
    call_id: str
    phone: Optional[str] = None
    transcript: Optional[str] = None
    status: Optional[str] = None
    recording_url: Optional[str] = None
    duration_ms: Optional[int] = None
    latency_ms: Optional[int] = None
    lang_mix: Optional[List[str]] = None
    turns: Optional[List[dict]] = None   # [{"speaker":"user|agent","text":"..."}] -> enables lang-match scoring
