"""
ReactionRoutingService
Evaluates export gates, slop risk blocks, and determines routing/redemption logic
for reaction artifacts.
"""

from __future__ import annotations
from typing import Optional
from src.ccp.models.reaction_engine_models import (
    ReactionScoreCard,
    ReactionVisibleScoreSummary,
    ReactionSlopRiskState,
    ReactionPerceptualRoutingDecision,
    ReactionRouteAction,
    ReactionPerceptualVerdict,
)


class ReactionRoutingService:
    """Orchestrates reaction publishing, review, and redemption based on core scorecard and perceptual metrics."""

    @staticmethod
    def evaluate_routing(
        artifact_id: str,
        scorecard: ReactionScoreCard,
        visible_scores: Optional[ReactionVisibleScoreSummary] = None,
        slop_risk_state: Optional[ReactionSlopRiskState] = None,
        jury_vote_count: int = 0
    ) -> ReactionPerceptualRoutingDecision:
        """Determines export eligibility and next route step for a reaction artifact.
        Enforces both legacy mechanical thresholds and SFL perceptual quality checks.
        """
        # 1. Evaluate existing mechanical export gate
        # thresholds: impact_score >= 70, conviction_score >= 70, anti_centroid_charge >= 0.60
        # (note conviction_score here is normalized to 100 for score check if passed as float < 1.0)
        conv_val = scorecard.conviction_score * 100.0 if scorecard.conviction_score <= 1.0 else scorecard.conviction_score
        anti_val = scorecard.anti_centroid_charge

        mechanical_pass = (
            scorecard.impact_score >= 70.0 and
            conv_val >= 70.0 and
            anti_val >= 0.60
        )

        # 2. Check if SFL perceptual scores are available
        if visible_scores is None or slop_risk_state is None:
            # Fallback legacy path (Mode B): rely purely on mechanical gate
            action = ReactionRouteAction.PASS_TO_EXPORT_GATE if mechanical_pass else ReactionRouteAction.ROUTE_TO_REDEMPTION
            explanation = "Legacy mechanical routing: " + ("passed core thresholds." if mechanical_pass else "failed core thresholds.")
            return ReactionPerceptualRoutingDecision(
                artifact_id=artifact_id,
                route_action=action,
                export_gate_eligible=mechanical_pass,
                jury_visibility_allowed=mechanical_pass,
                social_promotion_allowed=mechanical_pass,
                trigger_redemption=not mechanical_pass,
                explanation=explanation
            )

        # 3. Analyze perceptual block conditions
        presence_score = visible_scores.presence.score_0_99
        trust_score = visible_scores.trust.score_0_99
        humanity_score = visible_scores.humanity.score_0_99
        slop_risk_score = slop_risk_state.overall_risk_score_0_99

        # AC-05-SFL-2: High slop risk override (score >= 50) routes to review or redemption even if technically clean
        slop_block = (slop_risk_score >= 50)

        # AC-05-SFL-1 / AC-05-SFL-4: High votes cannot promote weak presence, weak trust, or elevated slop risk
        weak_perceptual_profile = (presence_score < 50 or trust_score < 50 or humanity_score < 50)
        
        # If slop risk is high or profile is weak, block promotion regardless of votes
        promotion_blocked = slop_block or weak_perceptual_profile

        # Define route action and explain why
        route_action = ReactionRouteAction.PASS_TO_EXPORT_GATE
        explanation_parts = []
        trigger_redemption = False

        if not mechanical_pass:
            # AC-05-SFL-3: Charismatic/strong takes still cannot export if they fail mechanical gates
            route_action = ReactionRouteAction.ROUTE_TO_REDEMPTION
            trigger_redemption = True
            explanation_parts.append("Failed mechanical export gates (impact/conviction/anti-centroid thresholds).")
        
        if slop_block:
            # Override routing if slop risk is high
            route_action = ReactionRouteAction.ROUTE_TO_REDEMPTION
            trigger_redemption = True
            explanation_parts.append(f"Blocked by high AI slop risk (score: {slop_risk_score}, class: {slop_risk_state.slop_class.value}). Required correction: {slop_risk_state.required_correction}")
            
        elif weak_perceptual_profile:
            # Route to redemption or coaching review
            route_action = ReactionRouteAction.COACHING_INTERVENTION
            trigger_redemption = True
            
            # AC-05-SFL-6: Explanation must highlight exactly which perceptual failure occurred
            fail_reasons = []
            if presence_score < 50:
                fail_reasons.append(f"low presence ({presence_score})")
            if trust_score < 50:
                fail_reasons.append(f"low trust ({trust_score})")
            if humanity_score < 50:
                fail_reasons.append(f"low humanity ({humanity_score})")
            explanation_parts.append(f"Blocked by weak perceptual profile: {', '.join(fail_reasons)}.")

        if not explanation_parts:
            # Passed all checks!
            if jury_vote_count > 10:
                route_action = ReactionRouteAction.PASS_TO_EXPORT_GATE
                explanation_parts.append("Passed all mechanical and SFL checks with high jury engagement.")
            else:
                route_action = ReactionRouteAction.PASS_TO_EXPORT_GATE
                explanation_parts.append("Passed all mechanical and SFL checks.")

        explanation = " ".join(explanation_parts)

        # Determine promotion status
        # If promotion blocked by slop/quality, social promotion and jury visibility are capped or disabled
        social_allowed = mechanical_pass and not promotion_blocked
        jury_allowed = mechanical_pass and (slop_risk_score < 50)

        return ReactionPerceptualRoutingDecision(
            artifact_id=artifact_id,
            route_action=route_action,
            export_gate_eligible=mechanical_pass and not promotion_blocked,
            jury_visibility_allowed=jury_allowed,
            social_promotion_allowed=social_allowed,
            trigger_redemption=trigger_redemption,
            explanation=explanation
        )
