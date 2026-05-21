from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

class OnboardingState(str, Enum):
    anonymous_session_created = "anonymous_session_created"
    recording_in_progress = "recording_in_progress"
    audit_uploaded = "audit_uploaded"
    teaser_processing = "teaser_processing"
    teaser_revealed = "teaser_revealed"
    offer_revealed = "offer_revealed"
    registration_optional = "registration_optional"
    identity_linked = "identity_linked"
    challenge_handoff_ready = "challenge_handoff_ready"
    processing_failed = "processing_failed"
    abandoned = "abandoned"
    session_closed_anonymous = "session_closed_anonymous"

class ReferralChannel(str, Enum):
    telegram_message = "telegram_message"
    debate_share = "debate_share"
    gallery_share = "gallery_share"
    direct_link = "direct_link"

class AuditUploadStatus(str, Enum):
    pending = "pending"
    uploaded = "uploaded"
    processed = "processed"
    failed = "failed"

class LeadMagnetDecision(str, Enum):
    viewed = "viewed"
    accepted = "accepted"
    dismissed = "dismissed"

class RegistrationMode(str, Enum):
    telegram_link = "telegram_link"
    email_capture = "email_capture"
    phone_capture = "phone_capture"
    skipped = "skipped"

class AnonymousReferralToken(BaseModel):
    referral_token_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    source_artifact_id: str | None = Field(default=None)
    channel: ReferralChannel = Field(...)
    created_at_utc: str = Field(..., min_length=1)

class AnonymousOnboardingSession(BaseModel):
    session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    referral_token_id: str | None = Field(default=None)
    anonymous_device_nonce: str = Field(..., min_length=1)
    benchmark_revealed_at: str | None = Field(default=None)
    linked_person_id: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)
    updated_at_utc: str = Field(..., min_length=1)

class AnonymousAuditAsset(BaseModel):
    audit_asset_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    storage_path: str = Field(..., min_length=1)
    duration_seconds: int = Field(..., ge=1, le=120)
    mime_type: str = Field(..., min_length=1)
    upload_status: AuditUploadStatus = Field(...)
    uploaded_at_utc: str = Field(..., min_length=1)

class BenchmarkTeaserScore(BaseModel):
    teaser_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    benchmark_score: int = Field(..., ge=0, le=100)
    score_label: str = Field(..., min_length=1)
    one_line_insight: str = Field(..., min_length=1)
    next_move_hint: str = Field(..., min_length=1)
    confidence_note: str = Field(..., min_length=1)
    revealed_at_utc: str = Field(..., min_length=1)

class LeadMagnetOfferProjection(BaseModel):
    session_id: str = Field(..., min_length=1)
    client_id_for_governor: str = Field(..., min_length=1)
    offer_tier_ceiling: str = Field(..., min_length=1)
    target_campaign_tier: int = Field(..., ge=1)
    gate_verdict: str = Field(..., min_length=1)
    offer_title: str = Field(..., min_length=1)
    offer_summary: str = Field(..., min_length=1)
    decision: LeadMagnetDecision | None = Field(default=None)

class AnonymousRegistrationLink(BaseModel):
    link_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    registration_mode: RegistrationMode = Field(...)
    person_id: str | None = Field(default=None)
    lead_id: str | None = Field(default=None)
    linked_at_utc: str | None = Field(default=None)

class OnboardingLaunchResponse(BaseModel):
    session: AnonymousOnboardingSession = Field(...)
    allowed_next_action: Literal["record_60s_audit"] = Field(default="record_60s_audit")

class TeaserRevealResponse(BaseModel):
    session_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    teaser: BenchmarkTeaserScore = Field(...)
    auth_required_before_next_step: bool = Field(default=False)

class OfferRevealResponse(BaseModel):
    session_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    teaser_already_revealed: bool = Field(default=True)
    offer: LeadMagnetOfferProjection = Field(...)

class RegistrationRequest(BaseModel):
    registration_mode: RegistrationMode = Field(...)
    telegram_user_id: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)
    first_name: str | None = Field(default=None)

class RegistrationResponse(BaseModel):
    session_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    link: AnonymousRegistrationLink = Field(...)
    next_action: Literal["challenge_handoff_available", "followup_routing_available"] = Field(...)
