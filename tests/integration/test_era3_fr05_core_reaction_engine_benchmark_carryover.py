"""
Integration tests for Core Reaction Engine Benchmark Carryover and taxonomy adaptions.
"""

from __future__ import annotations
import pytest
from src.ccp.models.reaction_engine_models import (
    ReactionScoreCard,
)
from src.ccp.services.reaction_score_adapter import ReactionScoreAdapter
from src.ccp.services.reaction_benchmark_carryover_service import ReactionBenchmarkCarryoverService


def test_carryover_assembled_correctly_with_headline():
    """Verify carryover assembled with correct fields and unflattened metrics headline."""
    scorecard = ReactionScoreCard(
        impact_score=80.0,
        anti_centroid_charge=0.75,
        damage_index=15.0,
        compounding_forecast=-4.5
    )
    
    transcript = "This is a highly specific take. Sarah did it in January 2024."
    acoustic = {
        "conviction_density": 85.0,
        "pacing_score": 75.0
    }
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    presence = ReactionScoreAdapter.derive_presence_signal(
        scorecard=scorecard,
        acoustic_features=acoustic,
        transcript_text=transcript
    )
    slop = ReactionScoreAdapter.derive_slop_risk(
        scorecard=scorecard,
        transcript_text=transcript,
        acoustic_features=acoustic
    )
    
    carryover = ReactionBenchmarkCarryoverService.assemble_carryover(
        artifact_id="ART-CO-1",
        coach_id="COACH-X",
        reaction_mode="solo",
        scorecard=scorecard,
        visible_scores=summary,
        presence_signal=presence,
        slop_risk_state=slop
    )
    
    assert carryover.artifact_id == "ART-CO-1"
    assert carryover.coach_id == "COACH-X"
    # Headline must keep deeper metrics
    assert "Anti-Centroid Charge: 0.75" in carryover.benchmark_headline
    assert "Damage Index: 15.0%" in carryover.benchmark_headline
    assert "Compounding Forecast: -4.5" in carryover.benchmark_headline


def test_carryover_challenge_readiness_and_recommendations():
    """Verify challenge readiness logic and course recommendations behavior."""
    # Scenario A: Passing take
    scorecard_pass = ReactionScoreCard(impact_score=80.0, anti_centroid_charge=0.75)
    transcript_pass = "Sarah did it in January 2024."
    acoustic_pass = {"conviction_density": 85.0, "pacing_score": 75.0}
    
    summary_pass = ReactionScoreAdapter.derive_scores(scorecard_pass, transcript_pass, acoustic_pass)
    presence_pass = ReactionScoreAdapter.derive_presence_signal(scorecard_pass, acoustic_pass, transcript_pass)
    slop_pass = ReactionScoreAdapter.derive_slop_risk(scorecard_pass, transcript_pass, acoustic_pass)
    
    carryover_pass = ReactionBenchmarkCarryoverService.assemble_carryover(
        artifact_id="ART-CO-PASS",
        coach_id="COACH-X",
        reaction_mode="solo",
        scorecard=scorecard_pass,
        visible_scores=summary_pass,
        presence_signal=presence_pass,
        slop_risk_state=slop_pass
    )
    assert carryover_pass.challenge_readiness
    assert not carryover_pass.speaker_course_recommended

    # Scenario B: Weak presence -> recommends course
    scorecard_fail = ReactionScoreCard(impact_score=65.0, anti_centroid_charge=0.45)
    transcript_fail = "Maybe we sort of can do something."
    acoustic_fail = {"conviction_density": 40.0, "pacing_score": 50.0}
    
    summary_fail = ReactionScoreAdapter.derive_scores(scorecard_fail, transcript_fail, acoustic_fail)
    presence_fail = ReactionScoreAdapter.derive_presence_signal(scorecard_fail, acoustic_fail, transcript_fail)
    slop_fail = ReactionScoreAdapter.derive_slop_risk(scorecard_fail, transcript_fail, acoustic_fail)
    
    carryover_fail = ReactionBenchmarkCarryoverService.assemble_carryover(
        artifact_id="ART-CO-FAIL",
        coach_id="COACH-X",
        reaction_mode="solo",
        scorecard=scorecard_fail,
        visible_scores=summary_fail,
        presence_signal=presence_fail,
        slop_risk_state=slop_fail
    )
    assert not carryover_fail.challenge_readiness
    assert carryover_fail.speaker_course_recommended
    assert carryover_fail.accountability_followup_recommended


def test_provisional_taxonomy_adapt():
    """Verify that provisional taxonomy mapping maps the 7 score families."""
    scorecard = ReactionScoreCard()
    transcript = "Sarah lost 40 clients in January 2024."
    
    summary = ReactionScoreAdapter.derive_scores(
        scorecard=scorecard,
        transcript_text=transcript
    )
    
    adapted = ReactionBenchmarkCarryoverService.provisional_taxonomy_adapt(summary)
    
    assert adapted["taxonomy_version"] == "PROVISIONAL-ALIGNMENT-FR35A"
    assert "meaning_plane_alpha" in adapted["dimensions"]
    assert "experience_plane_beta" in adapted["dimensions"]
    assert "guardrails" in adapted["dimensions"]
    assert adapted["dimensions"]["meaning_plane_alpha"]["humanity"] == summary.humanity.score_0_99
    assert adapted["dimensions"]["guardrails"]["ai_slop_risk"] == summary.ai_slop_risk.score_0_99
