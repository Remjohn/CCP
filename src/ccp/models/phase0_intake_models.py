"""
FR-ERA3-33 Phase-0 Prospect Intake Console Models
==================================================
Canonical Pydantic v2 schemas and enums for Phase-0 Prospect Intake.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────

class Phase0AuditTargetContentType(str, Enum):
    """Supported content types for Phase-0 audit targets."""
    SINGLE_IMAGE_CAPTION = "single_image_caption"
    CAROUSEL_CAPTION = "carousel_caption"
    REEL_CAPTION = "reel_caption"


class Phase0InputState(str, Enum):
    """Status of an individual input family within Phase-0 intake."""
    MISSING = "missing"
    ATTACHED = "attached"
    VALIDATED = "validated"
    REJECTED = "rejected"
    DERIVED = "derived"
    OPTIONAL_MISSING = "optional_missing"


class Phase0ProspectStatus(str, Enum):
    """Workflow status of the prospect record."""
    DRAFT = "draft"
    COLLECTING_INPUTS = "collecting_inputs"
    AWAITING_VALIDATION = "awaiting_validation"
    READY_FOR_PHASE0 = "ready_for_phase0"
    BLOCKED_MISSING_INPUTS = "blocked_missing_inputs"
    HANDED_OFF = "handed_off"
    ARCHIVED = "archived"


class Phase0DeliveryReadiness(str, Enum):
    """Readiness scoring for 24h proof package delivery SLA."""
    NOT_READY = "not_ready"
    CONDITIONALLY_READY = "conditionally_ready"
    READY = "ready"
    READY_HIGH_CONFIDENCE = "ready_high_confidence"


# ── Models ─────────────────────────────────────────────────────────────

class Phase0MediaSourceRef(BaseModel):
    """Reference to uploaded multimodal source media."""
    source_id: str = Field(default_factory=lambda: f"MREF-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    coach_id: Optional[str] = Field(default=None)
    media_kind: str = Field(
        ...,
        description="Value from: interview_video, interview_audio, audit_target_image, audit_target_video, supporting_reference"
    )
    storage_uri: str = Field(...)
    original_filename: str = Field(...)
    mime_type: Optional[str] = Field(default=None)
    file_size_bytes: int = Field(..., ge=0)
    duration_seconds: Optional[float] = Field(default=None, ge=0.0)
    image_width: Optional[int] = Field(default=None, ge=0)
    image_height: Optional[int] = Field(default=None, ge=0)
    checksum_sha256: str = Field(...)
    upload_receipt_id: str = Field(...)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0TranscriptSourceRef(BaseModel):
    """Reference to an attached interview or media transcript."""
    transcript_id: str = Field(default_factory=lambda: f"TXREF-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    source_kind: str = Field(
        ...,
        description="Value from: uploaded_file, inline_text, derived_from_media"
    )
    linked_media_source_id: Optional[str] = Field(default=None)
    storage_uri: Optional[str] = Field(default=None)
    raw_text: Optional[str] = Field(default=None)
    language_hint: Optional[str] = Field(default="en")
    word_count: Optional[int] = Field(default=None, ge=0)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0VoiceDnaSourceRef(BaseModel):
    """Reference to voice DNA assets used downstream for proof voice matching."""
    voice_dna_source_id: str = Field(default_factory=lambda: f"VDNA-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    linked_media_source_ids: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None)
    quality_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0VoiceCloneSourceRef(BaseModel):
    """Reference to voice clone parameters used downstream."""
    voice_clone_source_id: str = Field(default_factory=lambda: f"VCLON-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    linked_media_source_ids: List[str] = Field(default_factory=list)
    duration_seconds_total: float = Field(default=0.0, ge=0.0)
    quality_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    consent_status: Optional[str] = Field(default="granted")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0AvatarRef(BaseModel):
    """Reference to avatar image sources."""
    avatar_ref_id: str = Field(default_factory=lambda: f"AVREF-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    image_source_ids: List[str] = Field(default_factory=list)
    style_notes: Optional[str] = Field(default=None)
    pose_notes: Optional[str] = Field(default=None)
    quality_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0TargetAudienceProfile(BaseModel):
    """Captures target audience profile parameters for audit personalization."""
    prospect_id: str = Field(...)
    primary_audience_label: str = Field(...)
    pain_points: List[str] = Field(default_factory=list)
    desires: List[str] = Field(default_factory=list)
    market_context: Optional[str] = Field(default=None)
    offer_context: Optional[str] = Field(default=None)
    tone_notes: Optional[str] = Field(default=None)
    language_notes: Optional[str] = Field(default=None)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0GuardianBusinessIntelligenceBundle(BaseModel):
    """Guardian-derived business intelligence output."""
    guardian_bundle_id: str = Field(default_factory=lambda: f"GIBN-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    market_summary: str = Field(...)
    offer_summary: str = Field(...)
    positioning_notes: Optional[str] = Field(default=None)
    objections: List[str] = Field(default_factory=list)
    differentiation_notes: Optional[str] = Field(default=None)
    proof_notes: Optional[str] = Field(default=None)
    raw_artifact_refs: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0CaptionAttachment(BaseModel):
    """Attached caption or copy block for the target audit target."""
    caption_id: str = Field(default_factory=lambda: f"CAPT-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    audit_target_id: str = Field(...)
    caption_text: str = Field(...)
    language_hint: Optional[str] = Field(default="en")
    source_kind: str = Field(
        ...,
        description="Value from: manual_entry, uploaded_file, imported_reference"
    )
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0AuditTargetDescriptor(BaseModel):
    """Defines an audit target (e.g. image post, carousel post, reel video) to diagnose."""
    audit_target_id: str = Field(default_factory=lambda: f"AUDT-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    content_type: Phase0AuditTargetContentType = Field(...)
    primary_media_source_ids: List[str] = Field(default_factory=list)
    caption_id: Optional[str] = Field(default=None)
    platform_hint: Optional[str] = Field(default="instagram")
    content_url: Optional[str] = Field(default=None)
    archetype_hint: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Phase0MissingInputState(BaseModel):
    """Details a missing input flagged during validation."""
    prospect_id: str = Field(...)
    missing_code: str = Field(...)
    severity: str = Field(..., description="Value from: blocking, warning, optional")
    message: str = Field(...)
    resolution_hint: str = Field(...)


class Phase0ProspectReadinessState(BaseModel):
    """State of validation and delivery readiness for the prospect."""
    prospect_id: str = Field(...)
    packet_status: Phase0ProspectStatus = Field(...)
    delivery_readiness: Phase0DeliveryReadiness = Field(...)
    blocking_missing_inputs: List[Phase0MissingInputState] = Field(default_factory=list)
    warning_missing_inputs: List[Phase0MissingInputState] = Field(default_factory=list)
    readiness_summary: str = Field(...)
    validated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    validation_receipt_id: str = Field(...)


class Phase0ProspectPacket(BaseModel):
    """The canonical handoff packet emitted by the intake console."""
    packet_id: str = Field(default_factory=lambda: f"PKT-{uuid.uuid4().hex[:8].upper()}")
    prospect_id: str = Field(...)
    coach_id: Optional[str] = Field(default=None)
    display_name: str = Field(...)
    status: Phase0ProspectStatus = Field(default=Phase0ProspectStatus.DRAFT)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    media_sources: List[Phase0MediaSourceRef] = Field(default_factory=list)
    transcript_sources: List[Phase0TranscriptSourceRef] = Field(default_factory=list)
    voice_dna_sources: List[Phase0VoiceDnaSourceRef] = Field(default_factory=list)
    voice_clone_sources: List[Phase0VoiceCloneSourceRef] = Field(default_factory=list)
    avatar_refs: List[Phase0AvatarRef] = Field(default_factory=list)
    
    target_audience_profile: Optional[Phase0TargetAudienceProfile] = Field(default=None)
    guardian_business_intelligence_bundle: Optional[Phase0GuardianBusinessIntelligenceBundle] = Field(default=None)
    
    audit_targets: List[Phase0AuditTargetDescriptor] = Field(default_factory=list)
    captions: List[Phase0CaptionAttachment] = Field(default_factory=list)
    missing_input_states: List[Phase0MissingInputState] = Field(default_factory=list)
    readiness_state: Optional[Phase0ProspectReadinessState] = Field(default=None)
    
    campaign_metadata: Dict[str, Any] = Field(default_factory=dict)
    handoff_notes: Optional[str] = Field(default=None)
    receipt_chain_refs: List[str] = Field(default_factory=list)
