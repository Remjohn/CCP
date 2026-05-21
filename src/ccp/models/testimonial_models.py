from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class MomentumTriggerKind(str, Enum):
    benchmark_delta = "benchmark_delta"
    challenge_completion = "challenge_completion"
    streak_milestone = "streak_milestone"
    public_recognition = "public_recognition"
    coach_flagged_breakthrough = "coach_flagged_breakthrough"
    first_win_tier_boundary = "first_win_tier_boundary"


class CaptureMediaMode(str, Enum):
    voice = "voice"
    video = "video"


class CaptureStep(str, Enum):
    warm_prompt = "warm_prompt"
    reflection_record = "reflection_record"
    optional_attachment = "optional_attachment"
    metadata_tagging = "metadata_tagging"
    proof_review = "proof_review"
    consent_decision = "consent_decision"


class ConsentLevel(str, Enum):
    private_archive = "private_archive"
    close_community = "close_community"
    public_share = "public_share"


class UserCardTier(str, Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"
    prismatic = "prismatic"


class PeerGateVerdict(str, Enum):
    locked = "locked"
    pending = "pending"
    unlocked = "unlocked"
    unavailable = "unavailable"


class PeerEvidenceType(str, Enum):
    debate_victory = "debate_victory"
    certified_jury_votes = "certified_jury_votes"


class ShareDestination(str, Enum):
    community_gallery = "community_gallery"
    telegram_feed = "telegram_feed"
    accountability_thread = "accountability_thread"


class CaptureSessionStatus(str, Enum):
    triggered = "triggered"
    in_progress = "in_progress"
    awaiting_review = "awaiting_review"
    awaiting_consent = "awaiting_consent"
    finalized = "finalized"
    shared = "shared"
    blocked = "blocked"


class TestimonialMediaAsset(BaseModel):
    asset_id: str = Field(..., min_length=1)
    asset_type: Literal["audio", "video", "image"] = Field(...)
    storage_path: str = Field(..., min_length=1)
    duration_seconds: int | None = Field(default=None, ge=1)
    mime_type: str = Field(..., min_length=1)


class MomentumTriggerEvent(BaseModel):
    trigger_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    trigger_kind: MomentumTriggerKind = Field(...)
    trigger_source: str = Field(..., min_length=1)
    score_before: float | None = Field(default=None, ge=0)
    score_after: float | None = Field(default=None, ge=0)
    delta_value: float | None = Field(default=None)
    streak_count: int | None = Field(default=None, ge=0)
    challenge_layer: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)


class CaptureTagSet(BaseModel):
    trigger_kind: MomentumTriggerKind = Field(...)
    program_week: int | None = Field(default=None, ge=0)
    emotional_state: str = Field(..., min_length=1)
    strongest_primitive_id: str | None = Field(default=None)
    benchmark_delta_summary: str | None = Field(default=None)
    active_layer_label: str | None = Field(default=None)


class TestimonialCaptureSession(BaseModel):
    capture_session_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    trigger: MomentumTriggerEvent = Field(...)
    preferred_media_mode: CaptureMediaMode = Field(...)
    status: CaptureSessionStatus = Field(...)
    current_step: CaptureStep = Field(...)
    reflection_text_transcript: str | None = Field(default=None)
    primary_media_asset_id: str | None = Field(default=None)
    attachment_asset_ids: list[str] = Field(default_factory=list)
    tags: CaptureTagSet | None = Field(default=None)
    consent_level: ConsentLevel | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)
    updated_at_utc: str = Field(..., min_length=1)


class TransformationProofObject(BaseModel):
    proof_object_id: str = Field(..., min_length=1)
    capture_session_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    narrative_summary: str = Field(..., min_length=1)
    primary_media_asset_id: str = Field(..., min_length=1)
    attachment_asset_ids: list[str] = Field(default_factory=list)
    consent_level: ConsentLevel = Field(...)
    trigger_kind: MomentumTriggerKind = Field(...)
    delta_headline: str | None = Field(default=None)
    share_ready: bool = Field(default=False)
    created_at_utc: str = Field(..., min_length=1)


class UserCardMetric(BaseModel):
    metric_key: str = Field(..., min_length=1)
    current_value: float = Field(..., ge=0)
    delta_value: float = Field(...)
    display_label: str = Field(..., min_length=1)


class UserCardSoloProjection(BaseModel):
    snapshot_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    weekly_period_key: str = Field(..., min_length=1)
    solo_tier: UserCardTier = Field(...)
    strongest_primitive_id: str | None = Field(default=None)
    streak_count: int = Field(..., ge=0)
    metrics: list[UserCardMetric] = Field(default_factory=list)
    created_at_utc: str = Field(..., min_length=1)


class PeerEndorsementEvidence(BaseModel):
    evidence_type: PeerEvidenceType = Field(...)
    evidence_id: str = Field(..., min_length=1)
    certified_peer_count: int = Field(..., ge=0)
    threshold_required: int = Field(..., ge=1)
    evidence_summary: str = Field(..., min_length=1)


class PeerEndorsementDecision(BaseModel):
    verdict_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    verdict: PeerGateVerdict = Field(...)
    evidence: PeerEndorsementEvidence | None = Field(default=None)
    rationale: str = Field(..., min_length=1)
    locked_message: str | None = Field(default=None)
    decided_at_utc: str = Field(..., min_length=1)


class UserCardProjection(BaseModel):
    person_id: str = Field(..., min_length=1)
    public_tier: UserCardTier = Field(...)
    solo_projection: UserCardSoloProjection = Field(...)
    peer_decision: PeerEndorsementDecision = Field(...)
    avatar_asset_id: str | None = Field(default=None)
    profile_name: str = Field(..., min_length=1)
    program_identity: str = Field(..., min_length=1)
    card_asset_id: str | None = Field(default=None)
    prismatic_gate_copy: str = Field(..., min_length=1)


class ShareArtifactRequest(BaseModel):
    artifact_kind: Literal["proof_object", "user_card"] = Field(...)
    artifact_id: str = Field(..., min_length=1)
    destinations: list[ShareDestination] = Field(..., min_length=1)


class ShareArtifactResponse(BaseModel):
    share_event_id: str = Field(..., min_length=1)
    artifact_kind: Literal["proof_object", "user_card"] = Field(...)
    artifact_id: str = Field(..., min_length=1)
    published_destinations: list[ShareDestination] = Field(default_factory=list)
    silent_referral_routed: bool = Field(default=False)
    receipt_id: str = Field(..., min_length=1)
