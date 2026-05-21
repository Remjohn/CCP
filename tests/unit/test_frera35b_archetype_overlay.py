"""
tests/unit/test_frera35b_archetype_overlay.py
============================================
Unit tests for archetype-specific weight overlays, emphasis validation, and normalization behaviors.
"""

import pytest
from pydantic import ValidationError
from src.ccp.models.archetype_container_runtime_models import ArchetypeChoice
from src.ccp.models.benchmark_profile_models import (
    ContentType,
    CardRole,
    VisibleScoreKey,
    ScoreEmphasis,
    ArchetypeScoreBundle,
    REEL_BASELINE,
    VisibleScoreWeightMap
)
from src.ccp.services.benchmark_profile_services import (
    BenchmarkProfileRegistry,
    ArchetypeBundleResolver,
    CardWeightingResolver
)


@pytest.fixture
def resolvers_setup():
    """Sets up registries and resolvers for overlay testing."""
    profile_reg = BenchmarkProfileRegistry(coach_acronym="SYS")
    bundle_res = ArchetypeBundleResolver(coach_acronym="SYS")
    weight_res = CardWeightingResolver(
        profile_registry=profile_reg,
        bundle_resolver=bundle_res,
        coach_acronym="SYS"
    )
    return profile_reg, bundle_res, weight_res


def test_myth_debunk_reel_shifts_presence_higher(resolvers_setup):
    """Verify that the myth-debunk archetype shifts Presence and Signal higher on a reel baseline."""
    profile_reg, bundle_res, weight_res = resolvers_setup

    # Register reel baseline
    profile_reg.register_profile(REEL_BASELINE)

    # Define myth-debunk score bundle (reaction reel style, emphasizing presence and signal)
    myth_debunk_bundle = ArchetypeScoreBundle(
        bundle_id="ASB-MYTH-REEL",
        archetype_choice=ArchetypeChoice.ARC_MYTH_DEBUNK,
        content_type=ContentType.REEL,
        emphasis_adjustments=[
            ScoreEmphasis(score_key=VisibleScoreKey.PRESENCE, emphasis_delta=0.15, rationale="Myth-debunk requires intense delivery authority."),
            ScoreEmphasis(score_key=VisibleScoreKey.SIGNAL, emphasis_delta=0.10, rationale="Confrontational myth-debunk requires razor sharp niche signal.")
        ],
        bundle_rationale="Emphasize raw presence authority and niche signal sharpness."
    )
    bundle_res.register_bundle(myth_debunk_bundle)

    # Resolve weighting
    resolved = weight_res.resolve_card_weights(
        ContentType.REEL,
        ArchetypeChoice.ARC_MYTH_DEBUNK,
        CardRole.AUDIT_CARD
    )

    # Base Presence on Reel: 0.22, Shift: +0.15 -> 0.37
    # Base Signal on Reel: 0.10, Shift: +0.10 -> 0.20
    # Base Sum: 1.0 + 0.25 = 1.25. Let's make sure it was renormalized properly.
    assert resolved.resolved_weights.presence > REEL_BASELINE.base_weights.presence
    assert resolved.resolved_weights.signal > REEL_BASELINE.base_weights.signal
    
    # Assert that weights still sum to exactly 1.0 (approx)
    total = sum([
        resolved.resolved_weights.humanity,
        resolved.resolved_weights.presence,
        resolved.resolved_weights.trust,
        resolved.resolved_weights.memorability,
        resolved.resolved_weights.resonance,
        resolved.resolved_weights.signal
    ])
    assert 0.99 <= total <= 1.01


def test_witness_reel_shifts_resonance_higher(resolvers_setup):
    """Verify that the witness archetype shifts Resonance higher on a reel baseline."""
    profile_reg, bundle_res, weight_res = resolvers_setup

    profile_reg.register_profile(REEL_BASELINE)

    witness_bundle = ArchetypeScoreBundle(
        bundle_id="ASB-WITNESS-REEL",
        archetype_choice=ArchetypeChoice.ARC_WITNESS,
        content_type=ContentType.REEL,
        emphasis_adjustments=[
            ScoreEmphasis(score_key=VisibleScoreKey.RESONANCE, emphasis_delta=0.20, rationale="Witness style relies heavily on emotional resonance.")
        ],
        bundle_rationale="Emphasize subtextual emotional weight."
    )
    bundle_res.register_bundle(witness_bundle)

    resolved = weight_res.resolve_card_weights(
        ContentType.REEL,
        ArchetypeChoice.ARC_WITNESS,
        CardRole.AUDIT_CARD
    )

    # Base Resonance: 0.18, Shift: +0.20 -> 0.38
    assert resolved.resolved_weights.resonance > REEL_BASELINE.base_weights.resonance


def test_overlay_renormalizes_to_one(resolvers_setup):
    """Verify that resolved weights are renormalized to exactly 1.0 when adjustments cause a sum drift."""
    profile_reg, bundle_res, weight_res = resolvers_setup

    profile_reg.register_profile(REEL_BASELINE)

    # Trigger a drift by using very high positive deltas
    drift_bundle = ArchetypeScoreBundle(
        bundle_id="ASB-DRIFT-REEL",
        archetype_choice=ArchetypeChoice.ARC_COMP,
        content_type=ContentType.REEL,
        emphasis_adjustments=[
            ScoreEmphasis(score_key=VisibleScoreKey.PRESENCE, emphasis_delta=0.30, rationale="Big positive drift"),
            ScoreEmphasis(score_key=VisibleScoreKey.SIGNAL, emphasis_delta=0.30, rationale="Big positive drift")
        ],
        bundle_rationale="Drift test bundle"
    )
    bundle_res.register_bundle(drift_bundle)

    resolved = weight_res.resolve_card_weights(
        ContentType.REEL,
        ArchetypeChoice.ARC_COMP,
        CardRole.AUDIT_CARD
    )

    # Ensure renormalized sum is within [0.99, 1.01] (and practically exactly 1.0 due to division)
    total = sum([
        resolved.resolved_weights.humanity,
        resolved.resolved_weights.presence,
        resolved.resolved_weights.trust,
        resolved.resolved_weights.memorability,
        resolved.resolved_weights.resonance,
        resolved.resolved_weights.signal
    ])
    assert abs(total - 1.0) < 0.001


def test_emphasis_delta_bounded_minus_03_to_03():
    """Verify that emphasis deltas must lie between -0.3 and +0.3 inclusive."""
    # Bounded values should pass
    valid_emphasis = ScoreEmphasis(
        score_key=VisibleScoreKey.HUMANITY,
        emphasis_delta=0.30,
        rationale="Valid boundary"
    )
    assert valid_emphasis.emphasis_delta == 0.30

    # Over positive boundary
    with pytest.raises(ValidationError) as exc_info:
        ScoreEmphasis(
            score_key=VisibleScoreKey.HUMANITY,
            emphasis_delta=0.31,
            rationale="Too high"
        )
    assert "Emphasis delta must be in [-0.3, +0.3]" in str(exc_info.value)

    # Under negative boundary
    with pytest.raises(ValidationError) as exc_info:
        ScoreEmphasis(
            score_key=VisibleScoreKey.HUMANITY,
            emphasis_delta=-0.31,
            rationale="Too low"
        )
    assert "Emphasis delta must be in [-0.3, +0.3]" in str(exc_info.value)


def test_no_overlay_when_bundle_absent(resolvers_setup):
    """Verify that baseline weights are preserved unchanged if no archetype bundle is registered."""
    profile_reg, bundle_res, weight_res = resolvers_setup

    profile_reg.register_profile(REEL_BASELINE)
    # Do not register any bundle for ARC_WITNESS on REEL

    resolved = weight_res.resolve_card_weights(
        ContentType.REEL,
        ArchetypeChoice.ARC_WITNESS,
        CardRole.AUDIT_CARD
    )

    # Resolved weights should match baseline reel weights exactly
    assert resolved.resolved_weights.humanity == REEL_BASELINE.base_weights.humanity
    assert resolved.resolved_weights.presence == REEL_BASELINE.base_weights.presence
    assert resolved.resolved_weights.trust == REEL_BASELINE.base_weights.trust
    assert resolved.resolved_weights.memorability == REEL_BASELINE.base_weights.memorability
    assert resolved.resolved_weights.resonance == REEL_BASELINE.base_weights.resonance
    assert resolved.resolved_weights.signal == REEL_BASELINE.base_weights.signal
