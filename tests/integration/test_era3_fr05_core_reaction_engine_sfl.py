"""
Integration tests for Core Reaction Engine SFL translation and contracts.
"""

from __future__ import annotations
import pytest
from src.ccp.models.reaction_engine_models import (
    ReactionScoreCard,
    ReactionVisibleScoreName,
    ReactionPerceptualVerdict,
)
from src.ccp.services.reaction_score_adapter import ReactionScoreAdapter


def test_contract_serialization_all_seven_scores():
    """Verify that all seven score families are correctly represented in the visible summary."""
    scorecard = ReactionScoreCard(
        conviction_score=0.85,
        impact_score=75.0,
        anti_centroid_charge=0.70,
        damage_index=10.0,
        compounding_forecast=9.0
    )
    
    transcript = "This is a specific test case where Sarah launched her course in January 2024 and generated 15 sales."
    acoustic = {
        "conviction_density": 85.0,
        "pacing_score": 75.0,
        "pause_weight_score": 0.6,
        "stance_force_score": 0.8
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    assert summary is not None
    # All 7 core families must exist
    assert summary.humanity is not None
    assert summary.presence is not None
    assert summary.trust is not None
    assert summary.memorability is not None
    assert summary.resonance is not None
    assert summary.signal is not None
    assert summary.ai_slop_risk is not None
    
    assert summary.humanity.score_name == ReactionVisibleScoreName.HUMANITY
    assert summary.presence.score_name == ReactionVisibleScoreName.PRESENCE
    assert summary.trust.score_name == ReactionVisibleScoreName.TRUST


def test_presence_signal_evidence_serialization():
    """Verify presence signal correctly captures conviction, pacing, and hedging metrics."""
    scorecard = ReactionScoreCard(conviction_score=0.8)
    acoustic = {
        "conviction_density": 80.0,
        "pacing_score": 70.0,
        "pause_weight_score": 0.4,
        "stance_force_score": 0.7
    }
    transcript = "This is sort of a test where we probably kind of hedge a lot."
    
    signal = ReactionScoreAdapter.derive_presence_signal(
        scorecard=scorecard,
        acoustic_features=acoustic,
        transcript_text=transcript
    )
    
    assert signal.conviction_density == 80.0
    assert signal.pacing_score == 70.0
    assert signal.pause_weight_score == 0.4
    assert signal.hedge_pressure_score < 1.0  # must show hedge presence


def test_translation_pacing_hedging_lowers_presence():
    """Verify that low conviction and high hedging lowers the presence score."""
    scorecard = ReactionScoreCard(conviction_score=0.4)
    # High hedging transcript
    transcript = "Maybe we could sort of probably kind of try to think about something."
    acoustic = {"conviction_density": 40.0, "pacing_score": 50.0}
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    assert summary is not None
    assert summary.presence.score_0_99 < 50
    assert summary.presence.verdict in (ReactionPerceptualVerdict.WEAK, ReactionPerceptualVerdict.BLOCKING)


def test_translation_centroid_lowers_signal():
    """Verify that a safe, boring centroid take lowers the signal score."""
    scorecard = ReactionScoreCard(anti_centroid_charge=0.3)
    transcript = "We should always make sure we balance all viewpoints and never make anyone upset."
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript
    )
    
    assert summary is not None
    assert summary.signal.score_0_99 < 40


def test_translation_oversmoothed_raises_slop_risk():
    """Verify that an over-smoothed, highly-pacing transcript with zero specificity raises slop risk."""
    scorecard = ReactionScoreCard(conviction_score=0.9, anti_centroid_charge=0.4)
    transcript = "Always focus on authentic growth. The mindset must be cultivated continuously through leverage."
    acoustic = {
        "conviction_density": 90.0,
        "pacing_score": 90.0,
        "pause_weight_score": 0.8
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    assert summary is not None
    assert summary.ai_slop_risk.score_0_99 >= 50


def test_translation_lived_specificity_lifts_humanity():
    """Verify that high lived specificity (names, numbers, quotes) lifts the humanity score."""
    scorecard = ReactionScoreCard()
    # High specificity transcript
    transcript = "Sarah lost 40 clients in 'January 2024' because she used the wrong template."
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript
    )
    
    assert summary is not None
    assert summary.humanity.score_0_99 >= 70
    assert "High specificity and lived texture" in summary.top_strengths


def test_legacy_fallback_mode():
    """Verify that legacy mode returns None for visible summary and makes no fake score claims."""
    scorecard = ReactionScoreCard()
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text="Test",
        legacy_mode=True
    )
    assert summary is None
