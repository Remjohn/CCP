"""
Unit tests for FR-ERA3-33 Phase-0 Intake Console Pydantic Models.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.ccp.models.phase0_intake_models import (
    Phase0AuditTargetContentType,
    Phase0InputState,
    Phase0ProspectStatus,
    Phase0DeliveryReadiness,
    Phase0MediaSourceRef,
    Phase0TranscriptSourceRef,
    Phase0VoiceDnaSourceRef,
    Phase0VoiceCloneSourceRef,
    Phase0AvatarRef,
    Phase0TargetAudienceProfile,
    Phase0GuardianBusinessIntelligenceBundle,
    Phase0CaptionAttachment,
    Phase0AuditTargetDescriptor,
    Phase0MissingInputState,
    Phase0ProspectReadinessState,
    Phase0ProspectPacket
)


def test_prospect_packet_defaults():
    packet = Phase0ProspectPacket(
        prospect_id="P-12345",
        display_name="John Doe"
    )
    assert packet.status == Phase0ProspectStatus.DRAFT
    assert packet.packet_id.startswith("PKT-")
    assert len(packet.media_sources) == 0
    assert len(packet.captions) == 0
    assert packet.target_audience_profile is None


def test_media_source_ref_validation():
    with pytest.raises(ValidationError):
        # file_size_bytes is negative
        Phase0MediaSourceRef(
            prospect_id="P-123",
            media_kind="interview_video",
            storage_uri="s3://bucket/video.mp4",
            original_filename="video.mp4",
            file_size_bytes=-100,
            checksum_sha256="abc",
            upload_receipt_id="rcpt-1"
        )


def test_audit_target_content_types():
    assert Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION == "single_image_caption"
    assert Phase0AuditTargetContentType.CAROUSEL_CAPTION == "carousel_caption"
    assert Phase0AuditTargetContentType.REEL_CAPTION == "reel_caption"


def test_missing_input_state_severities():
    state = Phase0MissingInputState(
        prospect_id="P-1",
        missing_code="missing_interview_material",
        severity="blocking",
        message="No material.",
        resolution_hint="Upload audio."
    )
    assert state.severity == "blocking"
