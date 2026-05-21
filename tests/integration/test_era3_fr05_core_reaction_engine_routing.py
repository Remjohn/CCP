"""
Integration tests for Core Reaction Engine Routing, export gates, and slop overrides.
"""

from __future__ import annotations
import pytest
from src.ccp.models.reaction_engine_models import (
    ReactionScoreCard,
    ReactionRouteAction,
)
from src.ccp.services.reaction_score_adapter import ReactionScoreAdapter
from src.ccp.services.reaction_routing_service import ReactionRoutingService


def test_high_slop_risk_forces_redemption_or_review():
    """AC-05-SFL-2: High slop risk override routes to review/redemption even if technically clean."""
    scorecard = ReactionScoreCard(
        impact_score=80.0,
        conviction_score=0.8,
        anti_centroid_charge=0.70
    )
    
    # Over-smoothed take with zero specificity -> high slop risk
    transcript = "Authentic growth is the only way to scale. Everyone should always focus on the outcome."
    acoustic = {
        "conviction_density": 88.0,
        "pacing_score": 88.0
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    slop_state = ReactionScoreAdapter.derive_slop_risk(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    assert summary is not None
    assert slop_state.overall_risk_score_0_99 >= 50
    
    decision = ReactionRoutingService.evaluate_routing(
        artifact_id="ART-SLOP-TEST",
        scorecard=scorecard,
        visible_scores=summary,
        slop_risk_state=slop_state,
        jury_vote_count=100
    )
    
    # Must override to redemption/review and block export
    assert decision.route_action in (ReactionRouteAction.ROUTE_TO_REDEMPTION, ReactionRouteAction.COACHING_INTERVENTION)
    assert not decision.export_gate_eligible
    assert "Blocked by high AI slop risk" in decision.explanation or "Blocked by weak perceptual profile" in decision.explanation


def test_high_votes_cannot_override_weak_profile():
    """AC-05-SFL-4: Jury engagement does not auto-promote if Humanity or Presence are weak."""
    scorecard = ReactionScoreCard(
        impact_score=80.0,
        conviction_score=0.85,
        anti_centroid_charge=0.65
    )
    
    # Loud but empty take -> high votes (activity) but weak presence (due to hedging) and low humanity (no details)
    transcript = "I guess maybe we can focus on it but sort of kind of maybe not."
    acoustic = {
        "conviction_density": 50.0,
        "pacing_score": 50.0
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    slop_state = ReactionScoreAdapter.derive_slop_risk(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    decision = ReactionRoutingService.evaluate_routing(
        artifact_id="ART-VOTE-TEST",
        scorecard=scorecard,
        visible_scores=summary,
        slop_risk_state=slop_state,
        jury_vote_count=500  # High votes
    )
    
    assert decision.route_action == ReactionRouteAction.COACHING_INTERVENTION or decision.route_action == ReactionRouteAction.ROUTE_TO_REDEMPTION
    assert not decision.social_promotion_allowed
    assert not decision.export_gate_eligible


def test_export_gate_remains_bound_to_mechanical_thresholds():
    """AC-05-SFL-3: Charismatic/strong takes still cannot export if they fail core mechanical thresholds."""
    # Fails mechanical gate: anti_centroid_charge < 0.60
    scorecard = ReactionScoreCard(
        impact_score=85.0,
        conviction_score=0.90,
        anti_centroid_charge=0.45
    )
    
    # Highly specific, charismatic take
    transcript = "Sarah lost 40 clients in January 2024 because of the cold email templates."
    acoustic = {
        "conviction_density": 85.0,
        "pacing_score": 80.0
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    slop_state = ReactionScoreAdapter.derive_slop_risk(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    decision = ReactionRoutingService.evaluate_routing(
        artifact_id="ART-MECH-FAIL-TEST",
        scorecard=scorecard,
        visible_scores=summary,
        slop_risk_state=slop_state
    )
    
    assert not decision.export_gate_eligible
    assert decision.route_action == ReactionRouteAction.ROUTE_TO_REDEMPTION
    assert "Failed mechanical export gates" in decision.explanation


def test_explanatory_redemption_for_weak_presence():
    """AC-05-SFL-6: Redemptions explain specific failure causes."""
    scorecard = ReactionScoreCard(
        impact_score=80.0,
        conviction_score=0.8,
        anti_centroid_charge=0.65
    )
    
    # Hedged take -> low presence
    transcript = "Maybe we could possibly think about it, kind of sort of."
    acoustic = {
        "conviction_density": 45.0,
        "pacing_score": 60.0
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    slop_state = ReactionScoreAdapter.derive_slop_risk(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    decision = ReactionRoutingService.evaluate_routing(
        artifact_id="ART-RED-TEST",
        scorecard=scorecard,
        visible_scores=summary,
        slop_risk_state=slop_state
    )
    
    assert decision.trigger_redemption
    assert "low presence" in decision.explanation or "Blocked by high AI slop risk" in decision.explanation
