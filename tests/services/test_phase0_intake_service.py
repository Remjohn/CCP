"""
Unit tests for FR-ERA3-33 Phase-0 Prospect Intake Service.
"""

from __future__ import annotations

import pytest
from src.ccp.services.phase0_intake_service import Phase0IntakeService
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectStatus,
    Phase0DeliveryReadiness
)


def test_service_create_draft():
    service = Phase0IntakeService()
    packet = service.create_prospect(
        prospect_id="P-001",
        display_name="Audrey Beat",
        coach_id="COACH-001"
    )
    assert packet.prospect_id == "P-001"
    assert packet.display_name == "Audrey Beat"
    assert packet.status == Phase0ProspectStatus.DRAFT
    assert len(packet.receipt_chain_refs) == 1


def test_service_validation_blocked():
    service = Phase0IntakeService()
    service.create_prospect(
        prospect_id="P-002",
        display_name="Sonic Phase"
    )
    
    # Newly created draft has NO media or audit target -> Validation must block
    state = service.validate_readiness("P-002")
    assert state.packet_status == Phase0ProspectStatus.BLOCKED_MISSING_INPUTS
    assert state.delivery_readiness == Phase0DeliveryReadiness.NOT_READY
    assert len(state.blocking_missing_inputs) == 2  # missing_interview_material and missing_audit_target

    # Refuses to handoff a blocked packet
    with pytest.raises(ValueError):
        service.emit_handoff_packet("P-002")


def test_service_validation_conditionally_ready_to_ready():
    service = Phase0IntakeService()
    service.create_prospect(
        prospect_id="P-003",
        display_name="Beat Cluster",
        coach_id="COACH-003"
    )

    # Attach transcript (resolves missing_interview_material blocking condition)
    service.attach_transcript(
        prospect_id="P-003",
        source_kind="inline_text",
        raw_text="This is a real voice transcript containing business intelligence insights."
    )

    # Attach audit target (resolves missing_audit_target blocking condition)
    target = service.create_audit_target(
        prospect_id="P-003",
        content_type="single_image_caption",
        platform_hint="instagram"
    )

    # Validate readiness -> No blocking constraints, but should have warnings
    state = service.validate_readiness("P-003")
    assert state.packet_status == Phase0ProspectStatus.AWAITING_VALIDATION
    assert state.delivery_readiness == Phase0DeliveryReadiness.CONDITIONALLY_READY
    assert len(state.blocking_missing_inputs) == 0
    assert len(state.warning_missing_inputs) > 0  # missing caption, missing audience, missing voice source, etc.

    # Conditionally ready packets CAN be emitted downstream!
    packet = service.emit_handoff_packet("P-003")
    assert packet.status == Phase0ProspectStatus.HANDED_OFF

    # Now let's resolve all warnings to reach full READY status!
    service.attach_caption(
        prospect_id="P-003",
        audit_target_id=target.audit_target_id,
        caption_text="This is an awesome post caption.",
        source_kind="manual_entry"
    )
    service.set_audience_profile(
        prospect_id="P-003",
        primary_audience_label="Tech Creators",
        pain_points=["high cost", "slop"],
        desires=["clarity", "premium quality"]
    )
    service.attach_guardian_bi(
        prospect_id="P-003",
        market_summary="Niche tech coaching market",
        offer_summary="High-ticket group transformation program"
    )
    service.attach_voice_dna(
        prospect_id="P-003",
        linked_media_source_ids=[],
        quality_confidence=0.95
    )
    service.attach_avatar(
        prospect_id="P-003",
        image_source_ids=[],
        style_notes="Dark glassmorphism modern tone"
    )

    # Validate again -> All warnings resolved!
    state2 = service.validate_readiness("P-003")
    assert state2.packet_status == Phase0ProspectStatus.READY_FOR_PHASE0
    assert state2.delivery_readiness == Phase0DeliveryReadiness.READY
    assert len(state2.blocking_missing_inputs) == 0
    assert len(state2.warning_missing_inputs) == 0
