from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4
from src.ccp.models.cbcs_models import (
    DiagnosticCapacityDecision, DiagnosticChangeType, RitualAdjustmentPlan,
    CbcsPerceptualRecommendation, CbcsPerceptualIntakeEnvelope, VoiceNotePerceptualGuidance,
    AccountabilityPerceptualPrescription, CoachingSurfaceType, RecommendationClass, VisibleScoreName,
)


class CBCSRitualEngineService:
    """Converts diagnostic decisions into ritual/drill mutation plans.
    Integrates LearningPathBuilder, DynamicJournalingEngine, DormancyRecoveryService, RitualScheduler."""

    def __init__(self, learning_path_builder: Any = None, journaling_engine: Any = None, dormancy_service: Any = None, ritual_scheduler: Any = None, receipt_chain: Any = None) -> None:
        self._learning_path = learning_path_builder
        self._journaling = journaling_engine
        self._dormancy = dormancy_service
        self._ritual_scheduler = ritual_scheduler
        self._receipt_chain = receipt_chain

    async def plan_ritual(self, *, diagnostic: DiagnosticCapacityDecision) -> RitualAdjustmentPlan:
        now = datetime.now(timezone.utc)
        ritual_type = "repetition_drill"
        intensity_level = 3
        replaced_with_reflection = False
        learning_path_reason = "Standard ritual continuation."
        draft_prompt = "Continue with your current practice."

        # Check dormancy suppression before escalation
        if self._dormancy is not None:
            try:
                tier = self._dormancy.classify_tier(client_id=diagnostic.client_id, coach_id=diagnostic.coach_id)
                if tier and hasattr(tier, "dormancy_tier") and tier.dormancy_tier in ("HIGH", "CRITICAL"):
                    intensity_level = 1
                    learning_path_reason = "Dormancy recovery mode active. Gentle re-engagement."
                    draft_prompt = "Welcome back. Take a moment to reflect on one thing you remember from your last session."
            except Exception:
                pass

        # Apply diagnostic change type
        if diagnostic.change_type == DiagnosticChangeType.DOWNGRADE:
            intensity_level = max(1, intensity_level - 2)
            learning_path_reason = "Track adjustment requires reduced intensity for consolidation."
        elif diagnostic.change_type == DiagnosticChangeType.RITUAL_INTENSITY_REDUCTION:
            intensity_level = max(1, intensity_level - 1)
            learning_path_reason = "Minor performance delta addressed through intensity calibration."
        elif diagnostic.change_type == DiagnosticChangeType.REFLECTION_SUBSTITUTION:
            replaced_with_reflection = True
            ritual_type = "guided_reflection"
            learning_path_reason = "Reflection substitution to break repetitive loop."
        elif diagnostic.change_type == DiagnosticChangeType.UPGRADE:
            intensity_level = min(5, intensity_level + 1)
            learning_path_reason = "Consistent improvement supports increased challenge."

        # Consult learning path builder
        if self._learning_path is not None:
            try:
                rec = self._learning_path.recommend_next(client_id=diagnostic.client_id, coach_id=diagnostic.coach_id)
                if rec and hasattr(rec, "reason"):
                    learning_path_reason = rec.reason
            except Exception:
                pass

        # Generate reflection fallback if needed
        if replaced_with_reflection and self._journaling is not None:
            try:
                journal = self._journaling.generate(client_id=diagnostic.client_id, coach_id=diagnostic.coach_id)
                if journal and hasattr(journal, "prompt"):
                    draft_prompt = journal.prompt
            except Exception:
                pass

        # Generate ritual copy
        if not replaced_with_reflection and self._ritual_scheduler is not None:
            try:
                ritual = self._ritual_scheduler.generate_ritual(client_id=diagnostic.client_id, coach_id=diagnostic.coach_id, intensity=intensity_level)
                if ritual and hasattr(ritual, "prompt_text"):
                    draft_prompt = ritual.prompt_text
            except Exception:
                pass

        plan = RitualAdjustmentPlan(
            plan_id=str(uuid4()), client_id=diagnostic.client_id, coach_id=diagnostic.coach_id,
            ritual_type=ritual_type, intensity_level=intensity_level,
            replaced_with_reflection=replaced_with_reflection, learning_path_reason=learning_path_reason,
            draft_prompt=draft_prompt, scheduled_for_iso=None,
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="ritual-mutation", metadata={"plan_id": plan.plan_id, "intensity_level": intensity_level, "replaced_with_reflection": replaced_with_reflection})

        return plan

    async def generate_perceptual_plans(
        self, *, recommendation: CbcsPerceptualRecommendation, intake: CbcsPerceptualIntakeEnvelope
    ) -> tuple[VoiceNotePerceptualGuidance | None, AccountabilityPerceptualPrescription | None]:
        """Translate perceptual recommendation into voice note guidance and/or accountability prescriptions."""
        vn_guidance = None
        acc_prescription = None

        anti_slop_inst = "Maintain natural organic phrasing."
        if intake.effect_summary.anti_slop_warning_active:
            anti_slop_inst = "Strictly avoid smoothed transition phrases. Keep delivery raw, conversational, and direct."

        # Voice note surface mapping
        if recommendation.target_surface in (CoachingSurfaceType.VOICE_NOTE, CoachingSurfaceType.LIVE_REACTION_PROMPT, CoachingSurfaceType.JOURNALING_PROMPT):
            duration = 90
            if recommendation.recommendation_class == RecommendationClass.HUMANIZE:
                duration = 120
            elif recommendation.recommendation_class == RecommendationClass.SHARPEN:
                duration = 60

            # Enforce CBAR limit: 10 <= duration <= 600
            duration = max(10, min(600, duration))

            vn_guidance = VoiceNotePerceptualGuidance(
                guidance_id=f"vn-{uuid4().hex[:6]}",
                focus_score=recommendation.primary_score_target,
                target_duration_seconds=duration,
                delivery_instruction=f"Focus on: {recommendation.plain_language_goal}",
                pacing_instruction=recommendation.recommended_behavior,
                proof_instruction=f"Do NOT: {recommendation.prohibited_behavior}",
                anti_slop_instruction=anti_slop_inst,
                example_prompt=f"Deliver a {duration}-second message targeting {recommendation.primary_score_target.value}.",
            )

        # Accountability surface mapping
        if recommendation.target_surface == CoachingSurfaceType.ACCOUNTABILITY_MESSAGE or vn_guidance is None:
            rep_days = 7
            if recommendation.primary_score_target == VisibleScoreName.TRUST:
                rep_days = 3

            # Enforce CBAR limit: 1 <= window <= 30
            rep_days = max(1, min(30, rep_days))

            acc_prescription = AccountabilityPerceptualPrescription(
                prescription_id=f"acc-{uuid4().hex[:6]}",
                focus_scores=[recommendation.primary_score_target],
                accountability_task=recommendation.plain_language_goal,
                repetition_window_days=rep_days,
                review_signal="client_habit_log_submission",
                escalation_condition="missing_submission_threshold_reached",
                downgrade_sensitive=True,
            )

        if self._receipt_chain is not None:
            self._receipt_chain.log(
                action="ritual-mutation",
                metadata={
                    "vn_guidance_id": vn_guidance.guidance_id if vn_guidance else None,
                    "acc_prescription_id": acc_prescription.prescription_id if acc_prescription else None,
                }
            )

        return vn_guidance, acc_prescription

