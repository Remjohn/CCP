"""
Unit tests for FR-ERA3-35 Phase-0 Audit Intelligence Engine Service.
"""

from __future__ import annotations

import pytest
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0AuditTargetDescriptor as IntakeTargetDescriptor,
    Phase0CaptionAttachment,
    Phase0AuditTargetContentType,
    Phase0MediaSourceRef
)
from src.ccp.models.phase0_audit_models import (
    AuditTargetContentType,
    BridgeTierRecommendation,
    VideoStructureAvailability
)
from src.ccp.services.audit_intelligence_engine import AuditIntelligenceEngine


@pytest.fixture
def base_packet():
    """Returns a basic handoff-ready prospect packet."""
    target = IntakeTargetDescriptor(
        audit_target_id="AUDT-TGT-001",
        prospect_id="PRSP-TST-100",
        content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION,
        primary_media_source_ids=[],
        caption_id="CAPT-TGT-001"
    )
    
    caption = Phase0CaptionAttachment(
        caption_id="CAPT-TGT-001",
        prospect_id="PRSP-TST-100",
        audit_target_id="AUDT-TGT-001",
        caption_text="We must revolutionize our target audience by offering key value metrics delving into authentic testaments.",
        source_kind="manual_entry"
    )

    return Phase0ProspectPacket(
        prospect_id="PRSP-TST-100",
        display_name="Audrey Beat Cluster",
        coach_id="JP1",
        audit_targets=[target],
        captions=[caption]
    )


def test_audit_generation_single_image(base_packet):
    """Verify that a single-image audit generates correct scores, damage, and PDF/video payloads."""
    engine = AuditIntelligenceEngine(coach_acronym="JP1")
    report = engine.generate_audit(packet=base_packet, target_id="AUDT-TGT-001", provisional_override=True)
    
    # 1. Assertions on Report Metadata
    assert report.report_id.startswith("RPT-")
    assert report.prospect_id == "PRSP-TST-100"
    assert report.provisional_upstream_contract is True
    
    # 2. Check Visible Scores
    scores = report.visible_scores
    assert 0 <= scores.humanity <= 99
    # Expect moderate-to-high AI slop due to "revolutionize", "delving", "testaments" in caption
    assert scores.ai_slop_risk > 30

    # 3. Check Damage Index Calculations
    damage = report.damage_index
    assert 0 <= damage.overall_damage_score <= 99
    assert damage.authority_dilution_score > 0
    assert "overall damage index" in damage.explanation.lower()

    # 4. Check Compounding Forecast and Bridge Tier Recommendation
    forecast = report.compounding_forecast
    assert forecast.thirty_day_risk_score > 0
    
    bridge = report.continuity_bridge
    assert bridge.recommended_tier in [
        BridgeTierRecommendation.PROOF_UNLOCK_2999,
        BridgeTierRecommendation.SPEAKING_LEARNING_3999,
        BridgeTierRecommendation.COACH_OS_9999
    ]

    # 5. Modality validation check
    assert report.audit_target.content_type == AuditTargetContentType.SINGLE_IMAGE_CAPTION
    assert report.single_image_block is not None
    assert report.carousel_block is None
    assert report.reel_block is None

    # 6. PDF payload extraction
    pdf_payload = engine.extract_pdf_payload(report)
    assert pdf_payload.report_id == report.report_id
    assert "Audit" in pdf_payload.title
    assert pdf_payload.visible_scores.humanity == scores.humanity

    # 7. Video payload extraction
    video_payload = engine.extract_video_payload(report)
    assert video_payload.report_id == report.report_id
    assert len(video_payload.scene_script_blocks) == 5
    assert "Welcome" in video_payload.voiceover_script


def test_reel_structure_heuristic_fallback(base_packet):
    """Verify that a reel post registers video_structure with heuristic fallback when media is absent."""
    # Modify packet target to REEL_CAPTION
    base_packet.audit_targets[0].content_type = Phase0AuditTargetContentType.REEL_CAPTION
    
    engine = AuditIntelligenceEngine(coach_acronym="JP1")
    report = engine.generate_audit(packet=base_packet, target_id="AUDT-TGT-001")
    
    assert report.audit_target.content_type == AuditTargetContentType.REEL_CAPTION
    assert report.reel_block is not None
    assert report.single_image_block is None

    # Verify fallback triggers honestly (Section 6.2)
    video_struct = report.reel_block.video_structure
    assert video_struct.availability == VideoStructureAvailability.UNAVAILABLE
    assert "No source video attachment available" in video_struct.fallback_mode_reason
    assert video_struct.hook_retention_score > 0
