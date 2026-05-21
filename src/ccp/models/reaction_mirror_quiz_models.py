from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

class MirrorQuizGenerationStatus(str, Enum):
    READY = "ready"
    DEGRADED_STORYLESS = "degraded_storyless"
    BLOCKED_CMM_NOT_READY = "blocked_cmm_not_ready"
    BLOCKED_NO_APPROVED_TENSIONS = "blocked_no_approved_tensions"

class MirrorQuizReadinessStatus(str, Enum):
    READY = "ready"
    CMM_NOT_READY = "cmm_not_ready"
    CMM_TOO_THIN = "cmm_too_thin"
    STORY_ARCHIVE_MISSING = "story_archive_missing"

class MirrorQuizEvidenceQuote(BaseModel):
    evidence_id: str = Field(..., description="Deterministic ID for the selected CMM evidence row")
    cmm_id: str = Field(..., description="Source CulturalMemoryMap identifier")
    layer_type: Literal[
        "collective_wound",
        "industry_mythology",
        "linguistic_templates",
        "shared_enemy",
        "aspirational_archetype",
    ] = Field(...)
    source_material: Literal[
        "sacred_audio_transcript",
        "business_canvas",
        "tribe_soul",
        "philosophy_brief",
        "unknown",
    ] = Field(...)
    quoted_text: str = Field(..., min_length=8, description="Exact approved audience-memory phrasing")
    normalized_tension: str = Field(..., min_length=8, description="System-normalized tension label")
    selection_reason: str = Field(..., min_length=8, description="Why this quote was chosen for the question")

class StoryArchiveHint(BaseModel):
    story_id: str = Field(..., description="Approved coach story identifier")
    story_type: str = Field(..., min_length=2)
    cral_moment_fit: str = Field(default="")
    mechanism_tag: str = Field(default="")
    hook_line: str = Field(..., min_length=8, description="Short private reminder for the coach")
    why_relevant: str = Field(..., min_length=8)

class AudienceMirrorQuestion(BaseModel):
    question_id: str = Field(..., description="Deterministic question identifier")
    ordinal: int = Field(..., ge=1, le=5)
    surface_text: str = Field(..., min_length=12, description="Coach-facing prompt text")
    audience_verbatim: str = Field(..., min_length=8, description="Exact audience wording shown in the UI")
    primary_tension: str = Field(..., min_length=8)
    coaching_intent: Literal[
        "resolve_belief_conflict",
        "answer_hidden_objection",
        "name_shared_enemy",
        "reframe_failed_assumption",
        "validate_audience_identity",
    ] = Field(...)
    answer_time_limit_seconds: int = Field(default=90, ge=30, le=180)
    evidence_quotes: list[MirrorQuizEvidenceQuote] = Field(
        default_factory=list,
        min_length=1,
        max_length=3,
        description="Approved CMM evidence proving personalization"
    )
    story_hint: StoryArchiveHint | None = Field(
        default=None,
        description="Optional private answer prompt from approved story archive"
    )

class MirrorQuizQuestionPack(BaseModel):
    pack_id: str = Field(..., description="Primary identifier for this generated pack")
    coach_id: str = Field(..., description="Single-tenant coach scope")
    startapp: Literal["react_mirror_quiz"] = Field(default="react_mirror_quiz")
    source_mode: Literal["audience_mirror_quiz"] = Field(default="audience_mirror_quiz")
    cmm_id: str = Field(..., description="Approved CMM record used to build the pack")
    question_pack_version: str = Field(default="1.0")
    generation_status: MirrorQuizGenerationStatus = Field(...)
    readiness_status: MirrorQuizReadinessStatus = Field(...)
    questions: list[AudienceMirrorQuestion] = Field(default_factory=list)
    story_archive_used: bool = Field(default=False)
    receipt_id: str = Field(..., description="Receipt chain entry for generation traceability")
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=86400)

class MirrorQuizSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    question_pack: MirrorQuizQuestionPack = Field(...)
    selected_question_id: str = Field(...)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)
    scoring_status: Literal[
        "recording",
        "processing",
        "scored",
        "redemption_required",
    ] = Field(...)
    export_eligible: bool = Field(default=False)
    score_ready: bool = Field(default=False)
    score_receipt_id: str | None = Field(default=None)
