"""
Unit tests for FR-ERA3-35 Phase-0 Audit Intelligence Engine Pydantic Models.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.ccp.models.phase0_audit_models import (
    VisibleScoreSnapshot,
    DamageIndex,
    CompoundingForecast,
    ForecastDirection,
    StrengthReinforcementBlock,
    PrescriptionBlock,
    ProofOfPrescriptionBlock,
    ContinuityBridgeRecommendation,
    BridgeTierRecommendation,
    AuditTargetDescriptor,
    AuditTargetContentType,
    CaptionAuditBlock,
    SingleImageAuditBlock,
    CarouselAuditBlock,
    VideoStructureAuditBlock,
    VideoStructureAvailability,
    ReelAuditBlock,
    AuditIntelligenceReport,
    AuditSeverity,
    AuditFinding
)


def test_visible_scores_range_validation():
    """Verify that scores outside [0, 99] range are rejected."""
    # Valid snapshot compiles cleanly
    valid = VisibleScoreSnapshot(
        humanity=90, presence=80, trust=75, memorability=70, resonance=85, signal=95, ai_slop_risk=15
    )
    assert valid.humanity == 90

    # humanity out of range (too high)
    with pytest.raises(ValidationError):
        VisibleScoreSnapshot(
            humanity=100, presence=80, trust=75, memorability=70, resonance=85, signal=95, ai_slop_risk=15
        )

    # trust out of range (too low)
    with pytest.raises(ValidationError):
        VisibleScoreSnapshot(
            humanity=90, presence=80, trust=-1, memorability=70, resonance=85, signal=95, ai_slop_risk=15
        )


def test_damage_index_validation():
    """Verify that DamageIndex enforces range bounds and min string lengths."""
    valid_dmg = DamageIndex(
        overall_damage_score=40,
        authority_dilution_score=50,
        memorability_weakness_score=30,
        proof_weakness_score=20,
        humanity_weakness_score=10,
        genericity_blending_score=60,
        experiential_deficit_score=25,
        speaking_gap_score=35,
        reaction_gap_score=45,
        explanation="Visually generic signal"
    )
    assert valid_dmg.overall_damage_score == 40

    # explanation empty
    with pytest.raises(ValidationError):
        DamageIndex(
            overall_damage_score=40,
            authority_dilution_score=50,
            memorability_weakness_score=30,
            proof_weakness_score=20,
            humanity_weakness_score=10,
            genericity_blending_score=60,
            experiential_deficit_score=25,
            speaking_gap_score=35,
            reaction_gap_score=45,
            explanation=""
        )


def test_modality_block_exclusivity():
    """Verify that report model requires matching content blocks and rejects illegal duplicates."""
    target_desc = AuditTargetDescriptor(
        audit_target_id="AUDT-1",
        prospect_id="PRSP-1",
        content_type=AuditTargetContentType.SINGLE_IMAGE_CAPTION,
        primary_media_source_ids=[],
        caption_id="CAPT-1"
    )
    
    scores = VisibleScoreSnapshot(
        humanity=70, presence=70, trust=70, memorability=70, resonance=70, signal=70, ai_slop_risk=20
    )

    caption_b = CaptionAuditBlock(
        visible_scores=scores,
        key_findings=[],
        caption_alignment_notes=[],
        proof_language_notes=[],
        genericity_notes=[],
        summary="Solid baseline writing"
    )

    single_image_b = SingleImageAuditBlock(
        visible_scores=scores,
        key_findings=[],
        visual_authority_notes=[],
        proof_density_notes=[],
        image_caption_coherence_notes=[],
        summary="Visually clean post"
    )

    # Valid SINGLE_IMAGE_CAPTION setup
    report = AuditIntelligenceReport(
        report_id="RPT-1",
        prospect_id="PRSP-1",
        audit_target=target_desc,
        visible_scores=scores,
        damage_index=DamageIndex(
            overall_damage_score=30, authority_dilution_score=30, memorability_weakness_score=30,
            proof_weakness_score=30, humanity_weakness_score=30, genericity_blending_score=30,
            experiential_deficit_score=30, speaking_gap_score=30, reaction_gap_score=30,
            explanation="Moderate overall gaps"
        ),
        compounding_forecast=CompoundingForecast(
            direction=ForecastDirection.FLAT, thirty_day_risk_score=35, ninety_day_risk_score=40,
            trust_decay_risk=30, authority_decay_risk=30, invisibility_risk=30, summary="Flat trajectory"
        ),
        strength_reinforcement=StrengthReinforcementBlock(
            retained_strengths=["Sincerity"], why_they_work=["Simple"], preserve_instructions=[],
            reinforcement_summary="Nice authentic work"
        ),
        prescription=PrescriptionBlock(
            primary_shift="More live proof", supporting_shifts=[], speaking_improvement_path=[],
            reaction_improvement_path=[], content_improvement_path=[], why_now="Market saturation"
        ),
        proof_of_prescription=ProofOfPrescriptionBlock(
            proof_summary="Synthesized visual grid", transformed_asset_refs=[], scoring_card_refs=[],
            before_after_claim="Transformed layout", confidence_score=75
        ),
        continuity_bridge=ContinuityBridgeRecommendation(
            recommended_tier=BridgeTierRecommendation.PROOF_UNLOCK_2999,
            reason="Good foundation", ladder_copy="Unlock board", next_best_action="Purchase"
        ),
        caption_block=caption_b,
        single_image_block=single_image_b,
        operator_summary="Diagnosed single post",
        participant_summary="Dignified single post review"
    )
    assert report.single_image_block is not None

    # Invalid: SINGLE_IMAGE_CAPTION but single_image_block is missing
    with pytest.raises(ValidationError):
        AuditIntelligenceReport(
            report_id="RPT-2",
            prospect_id="PRSP-1",
            audit_target=target_desc,
            visible_scores=scores,
            damage_index=report.damage_index,
            compounding_forecast=report.compounding_forecast,
            strength_reinforcement=report.strength_reinforcement,
            prescription=report.prescription,
            proof_of_prescription=report.proof_of_prescription,
            continuity_bridge=report.continuity_bridge,
            caption_block=caption_b,
            single_image_block=None,  # Missing!
            operator_summary="Fails closed",
            participant_summary="Dignified review"
        )

    # Invalid: SINGLE_IMAGE_CAPTION but carousel_block is populated as well
    carousel_b = CarouselAuditBlock(
        visible_scores=scores, key_findings=[], sequencing_notes=[],
        frame_to_frame_logic_notes=[], caption_interaction_notes=[], summary="Slide transitions"
    )
    with pytest.raises(ValidationError):
        AuditIntelligenceReport(
            report_id="RPT-3",
            prospect_id="PRSP-1",
            audit_target=target_desc,
            visible_scores=scores,
            damage_index=report.damage_index,
            compounding_forecast=report.compounding_forecast,
            strength_reinforcement=report.strength_reinforcement,
            prescription=report.prescription,
            proof_of_prescription=report.proof_of_prescription,
            continuity_bridge=report.continuity_bridge,
            caption_block=caption_b,
            single_image_block=single_image_b,
            carousel_block=carousel_b,  # Double populating!
            operator_summary="Fails closed",
            participant_summary="Dignified review"
        )
