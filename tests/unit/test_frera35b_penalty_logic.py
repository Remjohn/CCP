"""
tests/unit/test_frera35b_penalty_logic.py
=========================================
Unit tests for AI Slop Risk penalties, floor thresholds, and overall score capping logic under FR-ERA3-35B.
"""

import pytest
from src.ccp.models.benchmark_profile_models import (
    CardWeightingBundle,
    VisibleScoreWeightMap,
    PenaltyAdjustmentMap,
    ContentType,
    CardRole
)
from src.ccp.models.archetype_container_runtime_models import ArchetypeChoice
from src.ccp.services.benchmark_profile_services import OverallScoreCalculator


@pytest.fixture
def test_weighting_bundle():
    """Returns a baseline weighting bundle with default weights and penalties for testing."""
    # Balanced baseline: equal weights of 1/6 (approx 0.1667 each)
    equal_weights = VisibleScoreWeightMap(
        humanity=0.167,
        presence=0.167,
        trust=0.167,
        memorability=0.167,
        resonance=0.166,
        signal=0.166
    )
    # Default penalties
    penalties = PenaltyAdjustmentMap(
        ai_slop_penalty_multiplier=0.15,
        trust_floor=30.0,
        humanity_floor=25.0,
        overall_cap_when_trust_below_floor=65.0,
        overall_cap_when_humanity_below_floor=60.0,
        overall_cap_when_slop_above_threshold=55.0,
        slop_danger_threshold=70.0,
        presence_without_trust_cap=70.0
    )
    return CardWeightingBundle(
        bundle_id="CWB-TEST-001",
        content_type=ContentType.SINGLE_IMAGE_POST,
        archetype_choice=ArchetypeChoice.ARC_MYTH_DEBUNK,
        card_role=CardRole.AUDIT_CARD,
        resolved_weights=equal_weights,
        resolved_penalties=penalties,
        modality_dimensions=[],
        source_profile_id="CBP-TEST",
        source_bundle_id="ASB-TEST",
        resolution_trace="TEST TRACE"
    )


def test_trust_below_floor_caps_overall(test_weighting_bundle):
    """Verify that when Trust is below its floor, the overall score is capped appropriately."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    # Humanity is fine (80), Trust is critically low (20), other scores high
    raw_scores = {
        "humanity": 80.0,
        "presence": 80.0,
        "trust": 20.0,
        "memorability": 80.0,
        "resonance": 80.0,
        "signal": 80.0,
        "ai_slop_risk": 10.0
    }
    comp = calculator.compute_overall(raw_scores, test_weighting_bundle)
    assert "trust_floor_cap" in comp.caps_applied
    # The cap should limit the overall score to overall_cap_when_trust_below_floor (65)
    assert comp.final_overall <= 65


def test_humanity_below_floor_caps_overall(test_weighting_bundle):
    """Verify that when Humanity is below its floor, the overall score is capped appropriately."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    # Trust is fine (80), Humanity is critically low (20), other scores high
    raw_scores = {
        "humanity": 20.0,
        "presence": 80.0,
        "trust": 80.0,
        "memorability": 80.0,
        "resonance": 80.0,
        "signal": 80.0,
        "ai_slop_risk": 10.0
    }
    comp = calculator.compute_overall(raw_scores, test_weighting_bundle)
    assert "humanity_floor_cap" in comp.caps_applied
    # The cap should limit the overall score to overall_cap_when_humanity_below_floor (60)
    assert comp.final_overall <= 60


def test_slop_above_threshold_caps_overall(test_weighting_bundle):
    """Verify that when AI Slop Risk exceeds the danger threshold, the overall score is capped."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    # All visible scores are high, but AI Slop Risk is 85 (above threshold 70)
    raw_scores = {
        "humanity": 90.0,
        "presence": 90.0,
        "trust": 90.0,
        "memorability": 90.0,
        "resonance": 90.0,
        "signal": 90.0,
        "ai_slop_risk": 85.0
    }
    comp = calculator.compute_overall(raw_scores, test_weighting_bundle)
    assert "slop_danger_cap" in comp.caps_applied
    # Should cap at overall_cap_when_slop_above_threshold (55)
    assert comp.final_overall <= 55


def test_presence_without_trust_caps_overall(test_weighting_bundle):
    """Verify that high Presence but low Trust triggers the presence_without_trust_cap."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    # Presence is very high (90), but Trust is below its floor (25 < 30)
    raw_scores = {
        "humanity": 80.0,
        "presence": 90.0,
        "trust": 25.0,
        "memorability": 80.0,
        "resonance": 80.0,
        "signal": 80.0,
        "ai_slop_risk": 0.0
    }
    comp = calculator.compute_overall(raw_scores, test_weighting_bundle)
    # Both trust_floor_cap (65) and presence_without_trust_cap (70) are triggered
    assert "trust_floor_cap" in comp.caps_applied
    assert "presence_without_trust_cap" in comp.caps_applied
    # The strictest cap applies (minimum of 65 and 70 is 65)
    assert comp.final_overall <= 65


def test_multiple_caps_apply_strictest(test_weighting_bundle):
    """Verify that when multiple caps are triggered, the strictest (minimum) cap is applied."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    # Trust is low (20 -> triggers cap 65)
    # Humanity is low (15 -> triggers cap 60)
    # Slop is high (85 -> triggers cap 55)
    raw_scores = {
        "humanity": 15.0,
        "presence": 90.0,
        "trust": 20.0,
        "memorability": 90.0,
        "resonance": 90.0,
        "signal": 90.0,
        "ai_slop_risk": 85.0
    }
    comp = calculator.compute_overall(raw_scores, test_weighting_bundle)
    assert "trust_floor_cap" in comp.caps_applied
    assert "humanity_floor_cap" in comp.caps_applied
    assert "slop_danger_cap" in comp.caps_applied
    # Strictest cap is slop_danger_cap (55)
    assert comp.final_overall <= 55


def test_no_caps_when_all_scores_healthy(test_weighting_bundle):
    """Verify that no caps are applied when all metrics are well within healthy bounds."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    raw_scores = {
        "humanity": 75.0,
        "presence": 75.0,
        "trust": 75.0,
        "memorability": 75.0,
        "resonance": 75.0,
        "signal": 75.0,
        "ai_slop_risk": 10.0
    }
    comp = calculator.compute_overall(raw_scores, test_weighting_bundle)
    assert len(comp.caps_applied) == 0
    # Expected weighted average: 75.0, slop penalty = 10 * 0.15 = 1.5, overall = 73
    assert comp.final_overall == 73


def test_slop_penalty_multiplier_reduces_base(test_weighting_bundle):
    """Verify that the AI Slop Risk score reduces the final overall score according to its multiplier."""
    calculator = OverallScoreCalculator(coach_acronym="SYS")
    # Baseline with slop = 0
    raw_scores_no_slop = {
        "humanity": 80.0,
        "presence": 80.0,
        "trust": 80.0,
        "memorability": 80.0,
        "resonance": 80.0,
        "signal": 80.0,
        "ai_slop_risk": 0.0
    }
    comp_no_slop = calculator.compute_overall(raw_scores_no_slop, test_weighting_bundle)
    
    # Baseline with slop = 50
    raw_scores_with_slop = raw_scores_no_slop.copy()
    raw_scores_with_slop["ai_slop_risk"] = 50.0
    comp_with_slop = calculator.compute_overall(raw_scores_with_slop, test_weighting_bundle)
    
    # Slop penalty = 50 * 0.15 = 7.5 points deduction
    assert comp_no_slop.final_overall == 80
    assert comp_with_slop.final_overall == 72
