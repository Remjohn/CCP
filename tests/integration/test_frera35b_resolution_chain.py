"""
tests/integration/test_frera35b_resolution_chain.py
===================================================
Integration tests verifying the complete resolution chain from profiles to overall score calculation under FR-ERA3-35B.
"""

import pytest
from src.ccp.models.archetype_container_runtime_models import ArchetypeChoice
from src.ccp.models.benchmark_profile_models import (
    ContentType,
    CardRole,
    VisibleScoreKey,
    ScoreEmphasis,
    ArchetypeScoreBundle,
    SINGLE_IMAGE_BASELINE,
    CAROUSEL_BASELINE,
    REEL_BASELINE,
    VisibleScoreWeightMap
)
from src.ccp.services.benchmark_profile_services import (
    BenchmarkProfileRegistry,
    ArchetypeBundleResolver,
    CardWeightingResolver,
    OverallScoreCalculator
)


class TestACBEN1ContentTypeDifferentiation:
    """Verifies that different content types produce distinct weight mappings (AC-BEN-1)."""

    def test_content_type_differentiation(self):
        profile_reg = BenchmarkProfileRegistry(coach_acronym="SYS")
        profile_reg.register_profile(SINGLE_IMAGE_BASELINE)
        profile_reg.register_profile(CAROUSEL_BASELINE)
        profile_reg.register_profile(REEL_BASELINE)

        # 1. Resolve all profiles
        img = profile_reg.resolve_profile(ContentType.SINGLE_IMAGE_POST).base_weights
        car = profile_reg.resolve_profile(ContentType.CAROUSEL).base_weights
        reel = profile_reg.resolve_profile(ContentType.REEL).base_weights

        # 2. Assert they differ from each other
        assert img != car
        assert img != reel
        assert car != reel

        # 3. Assert specific weighting emphasis laws
        # Static image emphasizes Trust and Signal to cut through feed noise
        assert img.trust > reel.trust
        assert img.signal > reel.signal

        # Reel emphasizes Presence and Humanity to show embodied authority
        assert reel.presence > img.presence
        assert reel.humanity > car.humanity

        # Carousel dominates on Memorability because it relies on sequential swiping progression
        assert car.memorability > img.memorability
        assert car.memorability > reel.memorability


class TestACBEN2ArchetypeOverlay:
    """Verifies that archetype-specific bundles overlay and adjust baselines correctly (AC-BEN-2)."""

    def test_archetype_overlay(self):
        profile_reg = BenchmarkProfileRegistry(coach_acronym="SYS")
        bundle_res = ArchetypeBundleResolver(coach_acronym="SYS")
        weight_res = CardWeightingResolver(profile_reg, bundle_res, coach_acronym="SYS")

        profile_reg.register_profile(REEL_BASELINE)

        # Define myth debunk bundle that shifts Presence +0.15 and Signal +0.10
        myth_debunk_bundle = ArchetypeScoreBundle(
            bundle_id="ASB-MYTH-REEL",
            archetype_choice=ArchetypeChoice.ARC_MYTH_DEBUNK,
            content_type=ContentType.REEL,
            emphasis_adjustments=[
                ScoreEmphasis(score_key=VisibleScoreKey.PRESENCE, emphasis_delta=0.15, rationale="Myth-debunk presence boost"),
                ScoreEmphasis(score_key=VisibleScoreKey.SIGNAL, emphasis_delta=0.10, rationale="Myth-debunk signal boost")
            ],
            bundle_rationale="Emphasize raw authority and niche sharpness"
        )
        bundle_res.register_bundle(myth_debunk_bundle)

        # Resolve weights
        resolved = weight_res.resolve_card_weights(
            ContentType.REEL,
            ArchetypeChoice.ARC_MYTH_DEBUNK,
            CardRole.AUDIT_CARD
        )

        # Assert resolved weights are different from base profile
        assert resolved.resolved_weights != REEL_BASELINE.base_weights

        # Assert specific shifts
        assert resolved.resolved_weights.presence > REEL_BASELINE.base_weights.presence
        assert resolved.resolved_weights.signal > REEL_BASELINE.base_weights.signal

        # Assert weights sum to 1.0 within floating point precision
        resolved_sum = (
            resolved.resolved_weights.humanity +
            resolved.resolved_weights.presence +
            resolved.resolved_weights.trust +
            resolved.resolved_weights.memorability +
            resolved.resolved_weights.resonance +
            resolved.resolved_weights.signal
        )
        assert 0.999 <= resolved_sum <= 1.001


class TestACBEN3OverallScoreComputation:
    """Verifies overall score calculation, penalty application, and strict capping laws (AC-BEN-3 & AC-BEN-4 & AC-BEN-6)."""

    def test_overall_score_computation(self):
        profile_reg = BenchmarkProfileRegistry(coach_acronym="SYS")
        bundle_res = ArchetypeBundleResolver(coach_acronym="SYS")
        weight_res = CardWeightingResolver(profile_reg, bundle_res, coach_acronym="SYS")
        calculator = OverallScoreCalculator(coach_acronym="SYS")

        profile_reg.register_profile(SINGLE_IMAGE_BASELINE)

        # Resolve clean equal weights or baseline weights
        card_weights = weight_res.resolve_card_weights(
            ContentType.SINGLE_IMAGE_POST,
            ArchetypeChoice.ARC_MYTH_DEBUNK,
            CardRole.AUDIT_CARD
        )

        # Low Trust (28 < 30 floor) and Low Humanity (22 < 25 floor)
        # Trust floor cap: 65, Humanity floor cap: 60
        raw_scores = {
            "humanity": 22.0,
            "presence": 85.0,
            "trust": 28.0,
            "memorability": 70.0,
            "resonance": 60.0,
            "signal": 75.0,
            "ai_slop_risk": 15.0
        }

        comp = calculator.compute_overall(raw_scores, card_weights)

        # 1. Assert caps applied
        assert "trust_floor_cap" in comp.caps_applied
        assert "humanity_floor_cap" in comp.caps_applied
        
        # 2. Strictest cap is 60 (Humanity floor cap). Final score must be bounded at 60.
        assert comp.final_overall <= 60


class TestACBEN5ReelVideoDimensions:
    """Verifies that the Reel Modality profile correctly includes shot-boundary and temporal dimensions (AC-BEN-5)."""

    def test_reel_video_dimensions(self):
        profile_reg = BenchmarkProfileRegistry(coach_acronym="SYS")
        profile_reg.register_profile(REEL_BASELINE)

        profile = profile_reg.resolve_profile(ContentType.REEL)
        dimensions = profile.modality_profile.dimensions

        # Assert dimensions are present
        dim_ids = [d.dimension_id for d in dimensions]
        assert "REEL-D3" in dim_ids  # shot_transition_quality
        assert "REEL-D4" in dim_ids  # temporal_coherence
        assert "REEL-D7" in dim_ids  # discontinuity_absence

        # Verify feeds cluster
        transitions_dim = [d for d in dimensions if d.dimension_id == "REEL-D3"][0]
        assert transitions_dim.feeds_cluster == "temporal_craft"
        
        coherence_dim = [d for d in dimensions if d.dimension_id == "REEL-D4"][0]
        assert coherence_dim.feeds_cluster == "temporal_craft"
