"""
ReactionBenchmarkCarryoverService
Translates reaction scores to challenge readiness, speaking recommendations,
and provides a provisional FR-35A taxonomy adapter.
"""

from __future__ import annotations
from typing import Dict, Any, List
from src.ccp.models.reaction_engine_models import (
    ReactionScoreCard,
    ReactionVisibleScoreSummary,
    ReactionPresenceSignal,
    ReactionSlopRiskState,
    ReactionBenchmarkCarryover,
    ReactionSlopClass,
)


class ReactionBenchmarkCarryoverService:
    """Manages benchmark carryover from spoken reaction performances to challenges, courses, and card profiles."""

    @staticmethod
    def assemble_carryover(
        artifact_id: str,
        coach_id: str,
        reaction_mode: str,
        scorecard: ReactionScoreCard,
        visible_scores: ReactionVisibleScoreSummary,
        presence_signal: ReactionPresenceSignal,
        slop_risk_state: ReactionSlopRiskState,
        historical_failures: List[str] = None
    ) -> ReactionBenchmarkCarryover:
        """Assembles a ReactionBenchmarkCarryover profile, calculating recommendations and readiness.
        Integrates deeper metrics (damage index, anti-centroid charge) into the benchmark headline.
        """
        history = historical_failures or []
        
        # 1. Challenge readiness: requires passing core mechanical thresholds AND trust > 60 AND slop risk < 40
        # AC-05-SFL-4 / AC-05-SFL-1: Challenge readiness does not trigger on weak trust or high slop combinations
        trust_val = visible_scores.trust.score_0_99
        slop_val = slop_risk_state.overall_risk_score_0_99
        
        mechanical_pass = (
            scorecard.impact_score >= 70.0 and
            scorecard.anti_centroid_charge >= 0.60
        )
        
        challenge_readiness = mechanical_pass and (trust_val >= 60) and (slop_val < 40)

        # 2. Speaker course recommended: triggered when presence is low or slop risk is high, or when failures repeat
        presence_val = presence_signal.presence_score_0_99
        low_presence = presence_val < 55
        high_slop = slop_val >= 50
        
        # Repetitive failures check
        repeated_failure = ("low_presence" in history and low_presence) or ("high_slop" in history and high_slop)
        speaker_course_recommended = low_presence or high_slop or repeated_failure

        # 3. Accountability follow-up: recommended if there's high slop risk or weak trust
        accountability_followup = (slop_val > 45) or (trust_val < 55)

        # 4. Benchmark Headline: integrates visible score + deep metrics (damage index & anti-centroid charge)
        # AC-05-SFL-5: Preserve deeper internal metrics in summaries without flattening
        headline = (
            f"Reaction Mode: {reaction_mode} | Presence Score: {presence_val}/99 | "
            f"Anti-Centroid Charge: {scorecard.anti_centroid_charge:.2f} | "
            f"Damage Index: {scorecard.damage_index:.1f}% | "
            f"Compounding Forecast: {scorecard.compounding_forecast:+.1f}"
        )

        return ReactionBenchmarkCarryover(
            artifact_id=artifact_id,
            coach_id=coach_id,
            reaction_mode=reaction_mode,
            visible_scores=visible_scores,
            presence_signal=presence_signal,
            slop_risk_state=slop_risk_state,
            challenge_readiness=challenge_readiness,
            speaker_course_recommended=speaker_course_recommended,
            accountability_followup_recommended=accountability_followup,
            benchmark_headline=headline
        )

    @staticmethod
    def provisional_taxonomy_adapt(
        visible_scores: ReactionVisibleScoreSummary
    ) -> Dict[str, Any]:
        """Provisional alignment adapter for downstream FR-35A Scoring Taxonomy.
        Maps the 7 core SFL visible scores into a provisional taxonomy structure.
        """
        return {
            "taxonomy_version": "PROVISIONAL-ALIGNMENT-FR35A",
            "dimensions": {
                "meaning_plane_alpha": {
                    "humanity": visible_scores.humanity.score_0_99,
                    "trust": visible_scores.trust.score_0_99,
                    "signal": visible_scores.signal.score_0_99,
                },
                "experience_plane_beta": {
                    "presence": visible_scores.presence.score_0_99,
                    "memorability": visible_scores.memorability.score_0_99,
                    "resonance": visible_scores.resonance.score_0_99,
                },
                "guardrails": {
                    "ai_slop_risk": visible_scores.ai_slop_risk.score_0_99,
                    "verdict": visible_scores.ai_slop_risk.verdict.value,
                }
            },
            "status": "aligned_provisional"
        }
