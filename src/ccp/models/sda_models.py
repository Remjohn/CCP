from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    PASS = "PASS"
    FAIL_REPRESENTATION_DRIFT = "FAIL_REPRESENTATION_DRIFT"
    FAIL_HARD_NEGATIVE = "FAIL_HARD_NEGATIVE"


class RecursivePattern(BaseModel):
    pattern_id: str = Field(...)
    pattern_type: str = Field(...)
    description: str = Field(...)
    occurrence_count: int = Field(default=1, ge=1)
    is_corrosive: bool = Field(default=False)
    first_observed_at: str = Field(default="")
    last_observed_at: str = Field(default="")


class FeedbackLoop(BaseModel):
    loop_id: str = Field(...)
    loop_type: str = Field(...)
    description: str = Field(...)
    is_negative: bool = Field(default=False)
    trigger_pattern_id: Optional[str] = Field(default=None)
    detected_at: str = Field(default="")


class EmergentContextualInvariant(BaseModel):
    invariant_id: str = Field(...)
    invariant_type: str = Field(...)
    description: str = Field(...)
    boundary_strength: float = Field(default=0.5, ge=0.0, le=1.0)
    source_context: str = Field(default="")


class InvariantFieldPacket(BaseModel):
    packet_id: str = Field(...)
    client_id: str = Field(...)
    active_invariants: list[str] = Field(default_factory=list)
    dominant_invariant: Optional[str] = Field(default=None)
    computed_at: str = Field(default="")


class RepresentationGeometryPacket(BaseModel):
    packet_id: str = Field(...)
    client_id: str = Field(...)
    geometry_type: str = Field(default="standard")
    alignment_score: float = Field(default=0.0, ge=0.0, le=1.0)
    fear_weighted: bool = Field(default=False)
    shame_coded: bool = Field(default=False)
    computed_at: str = Field(default="")


class DirectionalIntegrityReport(BaseModel):
    report_id: str = Field(...)
    artifact_type: str = Field(...)
    artifact_content_hash: str = Field(default="")
    verification_status: str = Field(...)
    invariant_alignment_score: float = Field(default=1.0, ge=0.0, le=1.0)
    failure_reason: Optional[str] = Field(default=None)
    evaluated_at: str = Field(default="")


class SemanticEvolutionRecord(BaseModel):
    record_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    recursive_patterns: list[RecursivePattern] = Field(default_factory=list)
    feedback_loops: list[FeedbackLoop] = Field(default_factory=list)
    last_updated_at: str = Field(default="")
