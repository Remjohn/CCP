from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4
from src.ccp.models.cbcs_models import (
    CBCSEvidencePacket, CapacityTrack, DiagnosticCapacityDecision, DiagnosticChangeType,
    CbcsPerceptualRecommendation, RecommendationClass, CoachingSurfaceType, VisibleScoreName,
)

CAPACITY_TRACK_ORDER = [CapacityTrack.RECOVERY, CapacityTrack.FOUNDATION, CapacityTrack.GROWTH, CapacityTrack.MOMENTUM, CapacityTrack.PEAK]


class CBCSDiagnosticEngineService:
    """Computes capacity-track and difficulty decisions from evidence. Output is internal-only.
    DiagnosticCapacityDecision has NO transport adapter to Telegram (Phase4-M07)."""

    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    async def diagnose(self, *, evidence: CBCSEvidencePacket, previous_track: CapacityTrack = CapacityTrack.FOUNDATION) -> DiagnosticCapacityDecision:
        now = datetime.now(timezone.utc)
        weaker_signals: list[str] = []
        stronger_signals: list[str] = []

        # Analyze trait metrics for regression/improvement
        for metric in evidence.trait_metrics:
            if metric.delta_value is not None:
                if metric.delta_value < -0.1:
                    weaker_signals.append(metric.metric_name)
                elif metric.delta_value > 0.1:
                    stronger_signals.append(metric.metric_name)

        # Determine change type
        change_type = DiagnosticChangeType.HOLD
        new_track = previous_track
        rationale = "Performance within expected range. Track maintained."

        prev_idx = CAPACITY_TRACK_ORDER.index(previous_track)

        if len(weaker_signals) >= 2 and len(stronger_signals) == 0:
            # Track downgrade
            if prev_idx > 0:
                new_track = CAPACITY_TRACK_ORDER[prev_idx - 1]
                change_type = DiagnosticChangeType.DOWNGRADE
                rationale = f"Multiple declining signals detected ({', '.join(weaker_signals)}). Track lowered for recovery."
        elif len(stronger_signals) >= 2 and len(weaker_signals) == 0:
            # Track upgrade
            if prev_idx < len(CAPACITY_TRACK_ORDER) - 1:
                new_track = CAPACITY_TRACK_ORDER[prev_idx + 1]
                change_type = DiagnosticChangeType.UPGRADE
                rationale = f"Consistent improvement in {', '.join(stronger_signals)}. Track elevated."
        elif len(weaker_signals) == 1 and len(stronger_signals) <= 1:
            # Ritual intensity reduction — same track, easier drill
            change_type = DiagnosticChangeType.RITUAL_INTENSITY_REDUCTION
            rationale = f"Minor dip in {weaker_signals[0]}. Ritual intensity reduced for consolidation."

        # Check for corrosive feedback loop interception
        if evidence.semantic_dynamics.identified_feedback_loops:
            for loop in evidence.semantic_dynamics.identified_feedback_loops:
                if loop.is_negative:
                    change_type = DiagnosticChangeType.REFLECTION_SUBSTITUTION
                    rationale = f"Corrosive feedback loop detected: {loop.description}. Substituting reflection."
                    break

        requires_intercept = change_type in (DiagnosticChangeType.DOWNGRADE, DiagnosticChangeType.RITUAL_INTENSITY_REDUCTION, DiagnosticChangeType.REFLECTION_SUBSTITUTION)

        decision = DiagnosticCapacityDecision(
            decision_id=str(uuid4()), client_id=evidence.client_id, coach_id=evidence.coach_id,
            previous_track=previous_track, new_track=new_track, change_type=change_type,
            rationale=rationale, weaker_signal_names=weaker_signals, stronger_signal_names=stronger_signals,
            requires_relationship_intercept=requires_intercept, created_at=now,
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="diagnostic-decision", metadata={"decision_id": decision.decision_id, "change_type": change_type.value, "requires_intercept": requires_intercept})

        return decision

    async def diagnose_perceptual(self, *, evidence: CBCSEvidencePacket) -> CbcsPerceptualRecommendation | None:
        """Map visible scores & effects from perceptual intake to a CbcsPerceptualRecommendation."""
        if not evidence.perceptual_intake:
            return None

        intake = evidence.perceptual_intake
        scores = intake.visible_scores

        # Check fallback mode
        fallback_mode = None
        if intake.source_reference.source_contract_id == "FALLBACK_SFL_EVAL":
            fallback_mode = "visible_scores_only"

        # Default recommendation values (reinforce stable)
        rec_class = RecommendationClass.REINFORCE
        target_surface = CoachingSurfaceType.VOICE_NOTE
        focus_score = VisibleScoreName.HUMANITY
        plain_goal = "Maintain and reinforce human congruence and raw authentic expression."
        recommended_behavior = "Continue sharing personal stories and raw client context."
        prohibited_behavior = "Avoid overly polished or scripted language."
        explanation = "All visible scores are stable. Reinforcing positive humanness."

        # Routing Matrix:
        # 1. humanity severe (0-24) -> HUMANIZE / voice note
        if scores.humanity.score_0_99 < 25:
            rec_class = RecommendationClass.HUMANIZE
            target_surface = CoachingSurfaceType.VOICE_NOTE
            focus_score = VisibleScoreName.HUMANITY
            plain_goal = "Inject organic pacing and imperfect delivery to counteract robotic smoothness."
            recommended_behavior = "Use pauses, sighs, and informal transitions."
            prohibited_behavior = "Do not read from a script or use monotone pacing."
            explanation = "Humanity score is in severe failure band (0-24). Urgent humanization required."
        # 2. trust severe (0-24) -> PROOF_GROUND / accountability task
        elif scores.trust.score_0_99 < 25:
            rec_class = RecommendationClass.PROOF_GROUND
            target_surface = CoachingSurfaceType.ACCOUNTABILITY_MESSAGE
            focus_score = VisibleScoreName.TRUST
            plain_goal = "Provide concrete proof and check-in to build trust."
            recommended_behavior = "Reference specific historical commitments and client goals."
            prohibited_behavior = "Avoid generic motivational phrases."
            explanation = "Trust score is in severe failure band (0-24). Establishing grounded proof-points."
        # 3. presence weak (25-44) -> SHARPEN / live reaction prompt
        elif scores.presence.score_0_99 < 45:
            rec_class = RecommendationClass.SHARPEN
            target_surface = CoachingSurfaceType.LIVE_REACTION_PROMPT
            focus_score = VisibleScoreName.PRESENCE
            plain_goal = "Increase punchiness and command attention."
            recommended_behavior = "Deliver short, high-energy instructions."
            prohibited_behavior = "Avoid long, rambling introductions."
            explanation = "Presence score is in weak band (25-44). Sharpening delivery presence."
        # 4. resonance unstable (45-64) -> DECOMPRESS / journaling prompt
        elif scores.resonance.score_0_99 < 65:
            rec_class = RecommendationClass.DECOMPRESS
            target_surface = CoachingSurfaceType.JOURNALING_PROMPT
            focus_score = VisibleScoreName.RESONANCE
            plain_goal = "Allow space for the client's internal integration."
            recommended_behavior = "Ask open-ended reflective questions."
            prohibited_behavior = "Do not overload the client with multiple calls-to-action."
            explanation = "Resonance score is in unstable band (45-64). Decompressing ritual intensity."

        if fallback_mode == "visible_scores_only":
            explanation += " [LOWER CONFIDENCE: Running in visible-scores-only fallback mode.]"

        rec = CbcsPerceptualRecommendation(
            recommendation_id=f"rec-{uuid4().hex[:6]}",
            recommendation_class=rec_class,
            target_surface=target_surface,
            primary_score_target=focus_score,
            plain_language_goal=plain_goal,
            recommended_behavior=recommended_behavior,
            prohibited_behavior=prohibited_behavior,
            explanation_for_operator=explanation,
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(
                action="diagnostic-decision",
                metadata={
                    "recommendation_id": rec.recommendation_id,
                    "recommendation_class": rec_class.value,
                    "target_surface": target_surface.value,
                    "focus_score": focus_score.value,
                    "fallback_mode": fallback_mode,
                }
            )

        return rec

