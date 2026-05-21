"""
FR-ERA3-33 Phase-0 Prospect Intake API Router
===============================================
FastAPI endpoints exposing the Prospect Intake Console.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Path, Body

from src.ccp.services.phase0_intake_service import Phase0IntakeService
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0MediaSourceRef,
    Phase0TranscriptSourceRef,
    Phase0VoiceDnaSourceRef,
    Phase0VoiceCloneSourceRef,
    Phase0AvatarRef,
    Phase0TargetAudienceProfile,
    Phase0GuardianBusinessIntelligenceBundle,
    Phase0CaptionAttachment,
    Phase0AuditTargetDescriptor,
    Phase0ProspectReadinessState
)
from pydantic import BaseModel, Field

router = APIRouter()
service = Phase0IntakeService()


# ── Request Body Schemas ───────────────────────────────────────────────

class ProspectCreateRequest(BaseModel):
    prospect_id: str = Field(..., description="Unique internal identifier for the prospect")
    display_name: str = Field(..., description="Display/human-readable name")
    coach_id: Optional[str] = Field(default=None, description="Optional bound coach identifier")
    campaign_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Outreach campaign metadata")


class MediaUploadRequest(BaseModel):
    media_kind: str = Field(..., description="Value from: interview_video, interview_audio, audit_target_image, audit_target_video, supporting_reference")
    storage_uri: str = Field(...)
    original_filename: str = Field(...)
    file_size_bytes: int = Field(..., ge=0)
    mime_type: Optional[str] = Field(default=None)
    duration_seconds: Optional[float] = Field(default=None, ge=0.0)
    image_width: Optional[int] = Field(default=None, ge=0)
    image_height: Optional[int] = Field(default=None, ge=0)
    checksum_sha256: Optional[str] = Field(default=None)


class TranscriptAttachRequest(BaseModel):
    source_kind: str = Field(..., description="Value from: uploaded_file, inline_text, derived_from_media")
    raw_text: Optional[str] = Field(default=None)
    storage_uri: Optional[str] = Field(default=None)
    linked_media_source_id: Optional[str] = Field(default=None)
    language_hint: Optional[str] = Field(default="en")


class VoiceDnaAttachRequest(BaseModel):
    linked_media_source_ids: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None)
    quality_confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class VoiceCloneAttachRequest(BaseModel):
    linked_media_source_ids: List[str] = Field(default_factory=list)
    duration_seconds_total: float = Field(..., ge=0.0)
    quality_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    consent_status: Optional[str] = Field(default="granted")


class AvatarAttachRequest(BaseModel):
    image_source_ids: List[str] = Field(default_factory=list)
    style_notes: Optional[str] = Field(default=None)
    pose_notes: Optional[str] = Field(default=None)
    quality_confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class AudienceProfileRequest(BaseModel):
    primary_audience_label: str = Field(...)
    pain_points: List[str] = Field(default_factory=list)
    desires: List[str] = Field(default_factory=list)
    market_context: Optional[str] = Field(default=None)
    offer_context: Optional[str] = Field(default=None)
    tone_notes: Optional[str] = Field(default=None)
    language_notes: Optional[str] = Field(default=None)


class GuardianBiRequest(BaseModel):
    market_summary: str = Field(...)
    offer_summary: str = Field(...)
    positioning_notes: Optional[str] = Field(default=None)
    objections: List[str] = Field(default_factory=list)
    differentiation_notes: Optional[str] = Field(default=None)
    proof_notes: Optional[str] = Field(default=None)
    raw_artifact_refs: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AuditTargetRequest(BaseModel):
    content_type: str = Field(..., description="Value from: single_image_caption, carousel_caption, reel_caption")
    primary_media_source_ids: Optional[List[str]] = Field(default_factory=list)
    platform_hint: Optional[str] = Field(default="instagram")
    content_url: Optional[str] = Field(default=None)
    archetype_hint: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)


class CaptionAttachRequest(BaseModel):
    caption_text: str = Field(...)
    source_kind: str = Field(..., description="Value from: manual_entry, uploaded_file, imported_reference")
    language_hint: Optional[str] = Field(default="en")


# ── REST API Endpoints ─────────────────────────────────────────────────

@router.post("/prospects", response_model=Phase0ProspectPacket)
def create_prospect(payload: ProspectCreateRequest):
    """Creates a draft prospect intake record."""
    try:
        return service.create_prospect(
            prospect_id=payload.prospect_id,
            display_name=payload.display_name,
            coach_id=payload.coach_id,
            campaign_metadata=payload.campaign_metadata
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/prospects/{prospect_id}", response_model=Phase0ProspectPacket)
def get_prospect(prospect_id: str = Path(...)):
    """Retrieves full prospect intake state."""
    packet = service.get_prospect(prospect_id)
    if not packet:
        raise HTTPException(status_code=404, detail=f"Prospect with ID {prospect_id} not found")
    return packet


@router.post("/prospects/{prospect_id}/media/upload", response_model=Phase0MediaSourceRef)
def attach_media(prospect_id: str = Path(...), payload: MediaUploadRequest = Body(...)):
    """Registers and persists uploaded media references."""
    try:
        return service.attach_media(
            prospect_id=prospect_id,
            media_kind=payload.media_kind,
            storage_uri=payload.storage_uri,
            original_filename=payload.original_filename,
            file_size_bytes=payload.file_size_bytes,
            mime_type=payload.mime_type,
            duration_seconds=payload.duration_seconds,
            image_width=payload.image_width,
            image_height=payload.image_height,
            checksum_sha256=payload.checksum_sha256
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/transcripts", response_model=Phase0TranscriptSourceRef)
def attach_transcript(prospect_id: str = Path(...), payload: TranscriptAttachRequest = Body(...)):
    """Attaches a transcribable media transcript."""
    try:
        return service.attach_transcript(
            prospect_id=prospect_id,
            source_kind=payload.source_kind,
            raw_text=payload.raw_text,
            storage_uri=payload.storage_uri,
            linked_media_source_id=payload.linked_media_source_id,
            language_hint=payload.language_hint
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/voice-dna-sources", response_model=Phase0VoiceDnaSourceRef)
def attach_voice_dna(prospect_id: str = Path(...), payload: VoiceDnaAttachRequest = Body(...)):
    """Attaches voice DNA source refs."""
    try:
        return service.attach_voice_dna(
            prospect_id=prospect_id,
            linked_media_source_ids=payload.linked_media_source_ids,
            notes=payload.notes,
            quality_confidence=payload.quality_confidence
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/voice-clone-sources", response_model=Phase0VoiceCloneSourceRef)
def attach_voice_clone(prospect_id: str = Path(...), payload: VoiceCloneAttachRequest = Body(...)):
    """Attaches voice clone parameters."""
    try:
        return service.attach_voice_clone(
            prospect_id=prospect_id,
            linked_media_source_ids=payload.linked_media_source_ids,
            duration_seconds_total=payload.duration_seconds_total,
            quality_confidence=payload.quality_confidence,
            consent_status=payload.consent_status
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/avatar-refs", response_model=Phase0AvatarRef)
def attach_avatar(prospect_id: str = Path(...), payload: AvatarAttachRequest = Body(...)):
    """Attaches facial portrait / avatar image source references."""
    try:
        return service.attach_avatar(
            prospect_id=prospect_id,
            image_source_ids=payload.image_source_ids,
            style_notes=payload.style_notes,
            pose_notes=payload.pose_notes,
            quality_confidence=payload.quality_confidence
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/audience-profile", response_model=Phase0TargetAudienceProfile)
def set_audience_profile(prospect_id: str = Path(...), payload: AudienceProfileRequest = Body(...)):
    """Creates or updates target audience persona profiles."""
    try:
        return service.set_audience_profile(
            prospect_id=prospect_id,
            primary_audience_label=payload.primary_audience_label,
            pain_points=payload.pain_points,
            desires=payload.desires,
            market_context=payload.market_context,
            offer_context=payload.offer_context,
            tone_notes=payload.tone_notes,
            language_notes=payload.language_notes
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/guardian-bi", response_model=Phase0GuardianBusinessIntelligenceBundle)
def attach_guardian_bi(prospect_id: str = Path(...), payload: GuardianBiRequest = Body(...)):
    """Attaches a Guardian BI analytical bundle."""
    try:
        return service.attach_guardian_bi(
            prospect_id=prospect_id,
            market_summary=payload.market_summary,
            offer_summary=payload.offer_summary,
            positioning_notes=payload.positioning_notes,
            objections=payload.objections,
            differentiation_notes=payload.differentiation_notes,
            proof_notes=payload.proof_notes,
            raw_artifact_refs=payload.raw_artifact_refs
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/audit-targets", response_model=Phase0AuditTargetDescriptor)
def create_audit_target(prospect_id: str = Path(...), payload: AuditTargetRequest = Body(...)):
    """Creates a baseline audit target descriptor for content mapping."""
    try:
        return service.create_audit_target(
            prospect_id=prospect_id,
            content_type=payload.content_type,
            primary_media_source_ids=payload.primary_media_source_ids,
            platform_hint=payload.platform_hint,
            content_url=payload.content_url,
            archetype_hint=payload.archetype_hint,
            notes=payload.notes
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/audit-targets/{audit_target_id}/caption", response_model=Phase0CaptionAttachment)
def attach_caption(
    prospect_id: str = Path(...),
    audit_target_id: str = Path(...),
    payload: CaptionAttachRequest = Body(...)
):
    """Attaches a baseline caption COPY to a target descriptor."""
    try:
        return service.attach_caption(
            prospect_id=prospect_id,
            audit_target_id=audit_target_id,
            caption_text=payload.caption_text,
            source_kind=payload.source_kind,
            language_hint=payload.language_hint
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/validate", response_model=Phase0ProspectReadinessState)
def validate_readiness(prospect_id: str = Path(...)):
    """Evaluates Rule-based completeness validation constraints."""
    try:
        return service.validate_readiness(prospect_id)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/prospects/{prospect_id}/handoff", response_model=Phase0ProspectPacket)
def emit_handoff_packet(prospect_id: str = Path(...)):
    """Emits the frozen, immutable handoff packet downstream."""
    try:
        return service.emit_handoff_packet(prospect_id)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
