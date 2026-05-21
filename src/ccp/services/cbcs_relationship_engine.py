from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4
from src.ccp.models.cbcs_models import (
    CBCSEvidencePacket, CumulativeInvestmentStats, DiagnosticCapacityDecision, DiagnosticChangeType,
    MacroTrendSnapshot, RelationshipFramedNotification, RelationshipInterceptionReason,
    RelationshipTrendContext, RitualAdjustmentPlan, TrendWindowStatus,
    CbcsPerceptualRecommendation, CbcsPerceptualIntakeEnvelope, VoiceNotePerceptualGuidance,
    AccountabilityPerceptualPrescription, RelationshipFramedCoachingMessage, RecommendationClass,
    CoachingSurfaceType, VisibleScoreName, CardEvidenceSnapshot,
)
from src.ccp.models.sda_models import DirectionalIntegrityReport, VerificationStatus

BANNED_REGRESSION_PHRASES = ["going backward", "you failed", "you struggled", "score dropped", "score fell", "downgraded", "easier because you failed", "lowering difficulty"]
DIRECTIONAL_INTEGRITY_THRESHOLD = 0.85


class CBCSRelationshipEngineService:
    """Intercepts downgrade-class events, builds long-loop context, and shapes safe user-facing
    notifications. Enforces Phase4-M07. Validates identity artifacts via DirectionalIntegrityPolicy."""

    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None, ritual_resonance: Any = None, engagement_feedback: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._ritual_resonance = ritual_resonance
        self._engagement_feedback = engagement_feedback

    async def build_trend_context(self, *, client_id: str, coach_id: str) -> RelationshipTrendContext:
        fourteen_day = MacroTrendSnapshot(window_days=14, status=TrendWindowStatus.INSUFFICIENT, headline_metric="N/A", supporting_sentence="Insufficient data for 14-day trend.")
        thirty_day = MacroTrendSnapshot(window_days=30, status=TrendWindowStatus.INSUFFICIENT, headline_metric="N/A", supporting_sentence="Insufficient data for 30-day trend.")
        cumulative = CumulativeInvestmentStats(total_sessions_completed=0, total_words_spoken=0, current_streak_days=0)
        resonance_hint = None
        dominant_invariant = None

        if self._supabase is not None:
            # Load 14-day and 30-day aggregates
            try:
                agg_result = self._supabase.table("trait_score_history").select("*").eq("client_id", client_id).eq("coach_id", coach_id).order("computed_at", desc=True).limit(30).execute()
                if agg_result and hasattr(agg_result, "data") and agg_result.data:
                    scores = [float(r.get("composite_score", 0)) for r in agg_result.data if r.get("composite_score") is not None]
                    if len(scores) >= 14:
                        first_half = sum(scores[7:14]) / 7
                        second_half = sum(scores[0:7]) / 7
                        delta = second_half - first_half
                        if delta > 0.05:
                            fourteen_day = MacroTrendSnapshot(window_days=14, status=TrendWindowStatus.POSITIVE, headline_metric=f"+{delta:.1%} improvement", positive_delta_label=f"{delta:.1%} growth", supporting_sentence="Your 14-day trajectory shows consistent progress.")
                        elif delta < -0.05:
                            fourteen_day = MacroTrendSnapshot(window_days=14, status=TrendWindowStatus.NEGATIVE, headline_metric="Consolidation phase", supporting_sentence="Your recent metrics suggest a temporary recalibration.")
                        else:
                            fourteen_day = MacroTrendSnapshot(window_days=14, status=TrendWindowStatus.FLAT, headline_metric="Stable baseline", supporting_sentence="Your performance has been steady over the past two weeks.")
                    if len(scores) >= 30:
                        first_half_30 = sum(scores[15:30]) / 15
                        second_half_30 = sum(scores[0:15]) / 15
                        delta_30 = second_half_30 - first_half_30
                        if delta_30 > 0.05:
                            thirty_day = MacroTrendSnapshot(window_days=30, status=TrendWindowStatus.POSITIVE, headline_metric=f"+{delta_30:.1%} growth", positive_delta_label=f"{delta_30:.1%} monthly growth", supporting_sentence="Your 30-day arc demonstrates meaningful development.")
                        elif delta_30 < -0.05:
                            thirty_day = MacroTrendSnapshot(window_days=30, status=TrendWindowStatus.NEGATIVE, headline_metric="Strategic recalibration", supporting_sentence="Your monthly view shows a period of adjustment.")
                        else:
                            thirty_day = MacroTrendSnapshot(window_days=30, status=TrendWindowStatus.FLAT, headline_metric="Consistent effort", supporting_sentence="Your 30-day performance has remained stable.")
            except Exception:
                pass

            # Load cumulative investment stats (EXP-FBK-004)
            try:
                session_result = self._supabase.table("cbcs_sessions").select("id").eq("client_id", client_id).eq("coach_id", coach_id).execute()
                if session_result and hasattr(session_result, "data"):
                    cumulative = CumulativeInvestmentStats(total_sessions_completed=len(session_result.data), total_words_spoken=0, current_streak_days=0)
            except Exception:
                pass

        # Resonance enrichment
        if self._ritual_resonance is not None:
            try:
                enhancement = self._ritual_resonance.get_resonance_enhancement(client_id=client_id, coach_id=coach_id)
                if enhancement and hasattr(enhancement, "marker_hint"):
                    resonance_hint = enhancement.marker_hint
            except Exception:
                pass

        return RelationshipTrendContext(
            context_id=str(uuid4()), client_id=client_id, coach_id=coach_id,
            fourteen_day=fourteen_day, thirty_day=thirty_day, cumulative_stats=cumulative,
            resonance_marker_hint=resonance_hint, dominant_invariant_field=dominant_invariant,
        )

    async def frame_notification(self, *, diagnostic: DiagnosticCapacityDecision, ritual_plan: RitualAdjustmentPlan, trend_context: RelationshipTrendContext, evidence: CBCSEvidencePacket) -> RelationshipFramedNotification | None:
        """Build the safe user-facing notification. Returns None if framing fails (dispatch blocked)."""
        now = datetime.now(timezone.utc)

        # Determine interception reason
        interception_reason = RelationshipInterceptionReason.NONE
        if diagnostic.change_type == DiagnosticChangeType.DOWNGRADE:
            interception_reason = RelationshipInterceptionReason.CAPACITY_TRACK_DOWNGRADE
        elif diagnostic.change_type == DiagnosticChangeType.RITUAL_INTENSITY_REDUCTION:
            interception_reason = RelationshipInterceptionReason.RITUAL_INTENSITY_REDUCTION
        elif diagnostic.change_type == DiagnosticChangeType.REFLECTION_SUBSTITUTION:
            # Check for corrosive loop
            has_corrosive = any(loop.is_negative for loop in evidence.semantic_dynamics.identified_feedback_loops)
            if has_corrosive:
                interception_reason = RelationshipInterceptionReason.CORROSIVE_LOOP_INTERRUPTION
            else:
                interception_reason = RelationshipInterceptionReason.RITUAL_INTENSITY_REDUCTION

        # Determine if early journey
        is_early_journey = (trend_context.fourteen_day.status == TrendWindowStatus.INSUFFICIENT and trend_context.thirty_day.status == TrendWindowStatus.INSUFFICIENT)
        if is_early_journey and interception_reason != RelationshipInterceptionReason.NONE:
            interception_reason = RelationshipInterceptionReason.EARLY_JOURNEY_SAFE_FRAMING

        # Build safe headline and body
        visible_macro_metric = None
        visible_cumulative_metric = None

        if diagnostic.requires_relationship_intercept:
            if trend_context.fourteen_day.status == TrendWindowStatus.POSITIVE:
                safe_headline = "Your bigger picture keeps growing"
                safe_body = f"{trend_context.fourteen_day.supporting_sentence} Tomorrow's session is calibrated to deepen that momentum."
                visible_macro_metric = trend_context.fourteen_day.headline_metric
            elif trend_context.thirty_day.status == TrendWindowStatus.POSITIVE:
                safe_headline = "Your monthly trajectory speaks volumes"
                safe_body = f"{trend_context.thirty_day.supporting_sentence} Tomorrow's focus is strategically adjusted for sustained growth."
                visible_macro_metric = trend_context.thirty_day.headline_metric
            elif is_early_journey:
                safe_headline = "Building your foundation"
                safe_body = "Tomorrow's session is calibrated as foundation work — establishing the baseline that will reveal your growth arc over time."
                if trend_context.cumulative_stats.total_sessions_completed > 0:
                    visible_cumulative_metric = f"{trend_context.cumulative_stats.total_sessions_completed} sessions invested"
            elif trend_context.cumulative_stats.total_sessions_completed > 0:
                safe_headline = "Your investment keeps compounding"
                safe_body = f"You've completed {trend_context.cumulative_stats.total_sessions_completed} sessions. Tomorrow's practice is strategically focused for your next phase."
                visible_cumulative_metric = f"{trend_context.cumulative_stats.total_sessions_completed} sessions, ongoing streak"
            else:
                safe_headline = "Strategic focus for tomorrow"
                safe_body = "Tomorrow's session is strategically calibrated to meet you where you are right now."
        else:
            safe_headline = "Your next step is ready"
            safe_body = ritual_plan.draft_prompt if len(ritual_plan.draft_prompt) <= 1200 else ritual_plan.draft_prompt[:1197] + "..."

        # Enforce no banned regression phrases
        for phrase in BANNED_REGRESSION_PHRASES:
            if phrase.lower() in safe_headline.lower() or phrase.lower() in safe_body.lower():
                if self._receipt_chain is not None:
                    self._receipt_chain.log(action="relationship-frame-blocked", metadata={"reason": f"Banned phrase detected: {phrase}", "client_id": diagnostic.client_id})
                return None

        # DirectionalIntegrityPolicy validation for identity artifacts
        integrity_report = None
        if interception_reason in (RelationshipInterceptionReason.CAPACITY_TRACK_DOWNGRADE, RelationshipInterceptionReason.CORROSIVE_LOOP_INTERRUPTION, RelationshipInterceptionReason.EARLY_JOURNEY_SAFE_FRAMING):
            integrity_report = self._validate_directional_integrity(safe_headline, safe_body)
            if integrity_report and integrity_report.verification_status in (VerificationStatus.FAIL_HARD_NEGATIVE.value, VerificationStatus.FAIL_REPRESENTATION_DRIFT.value):
                if self._receipt_chain is not None:
                    self._receipt_chain.log(action="relationship-frame-blocked", metadata={"reason": integrity_report.failure_reason or "Directional integrity failure", "client_id": diagnostic.client_id})
                return None

        notification = RelationshipFramedNotification(
            notification_id=str(uuid4()), client_id=diagnostic.client_id, coach_id=diagnostic.coach_id,
            interception_reason=interception_reason, safe_headline=safe_headline, safe_body=safe_body,
            visible_macro_metric=visible_macro_metric, visible_cumulative_metric=visible_cumulative_metric,
            dispatch_channel="telegram", integrity_report=integrity_report, created_at=now,
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="downgrade-interception", metadata={"notification_id": notification.notification_id, "interception_reason": interception_reason.value})

        return notification

    def _validate_directional_integrity(self, headline: str, body: str) -> DirectionalIntegrityReport:
        """Check headline and body for fear-weighted or shame-coded representations."""
        import hashlib
        content_hash = hashlib.sha256(f"{headline}{body}".encode()).hexdigest()[:16]
        shame_indicators = ["shame", "failure", "weak", "pathetic", "worthless", "inadequate", "embarrass"]
        fear_indicators = ["scared", "afraid", "terrified", "panic", "dread"]
        full_text = f"{headline} {body}".lower()

        has_shame = any(indicator in full_text for indicator in shame_indicators)
        has_fear = any(indicator in full_text for indicator in fear_indicators)

        if has_shame or has_fear:
            return DirectionalIntegrityReport(
                report_id=str(uuid4()), artifact_type="notification", artifact_content_hash=content_hash,
                verification_status=VerificationStatus.FAIL_HARD_NEGATIVE.value, invariant_alignment_score=0.3,
                failure_reason="Content contains shame-coded or fear-weighted representations.",
                evaluated_at=datetime.now(timezone.utc).isoformat(),
            )

        return DirectionalIntegrityReport(
            report_id=str(uuid4()), artifact_type="notification", artifact_content_hash=content_hash,
            verification_status=VerificationStatus.PASS.value, invariant_alignment_score=1.0,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

    def _de_smooth_text(self, text: str) -> str:
        fluffy_words = {
            "delve": "focus",
            "tapestry": "journey",
            "testament": "proof",
            "moreover": "also",
            "furthermore": "also",
            "embark": "start",
            "unravel": "understand",
        }
        words = text.split()
        new_words = []
        for w in words:
            clean_w = w.lower().strip(",.?!;:()\"'")
            if clean_w in fluffy_words:
                replaced = fluffy_words[clean_w]
                if w[0].isupper():
                    replaced = replaced.capitalize()
                prefix = w[:w.find(clean_w)]
                suffix = w[w.find(clean_w) + len(clean_w):]
                new_words.append(prefix + replaced + suffix)
            else:
                new_words.append(w)
        return " ".join(new_words)

    def _strip_card_ids(self, text: str, card_snapshot: Optional[CardEvidenceSnapshot]) -> str:
        import re
        text = re.sub(r'\b(card|board)-[a-zA-Z0-9_\-]+\b', 'your tasks', text)
        if card_snapshot:
            for card_id in card_snapshot.card_ids:
                if card_id in text:
                    text = text.replace(card_id, 'your task')
            if card_snapshot.board_id in text:
                text = text.replace(card_snapshot.board_id, 'your board')
        return text

    def _validate_reactance_guard(self, text: str) -> bool:
        prohibited = ["you must", "you have to", "you failed", "required to", "obey", "do as I say"]
        text_lower = text.lower()
        return not any(p in text_lower for p in prohibited)

    async def frame_coaching_message(
        self,
        *,
        recommendation: CbcsPerceptualRecommendation,
        vn_guidance: Optional[VoiceNotePerceptualGuidance] = None,
        acc_prescription: Optional[AccountabilityPerceptualPrescription] = None,
        intake: CbcsPerceptualIntakeEnvelope,
        trend_context: RelationshipTrendContext,
    ) -> RelationshipFramedCoachingMessage:
        """Frame a safe, human-first coaching message based on recommendations, avoiding raw ID exposure."""
        scores = intake.visible_scores
        headline = "Next step is ready"
        body = ""

        has_humanity_strength = scores.humanity.score_0_99 >= 80
        has_resonance_strength = scores.resonance.score_0_99 >= 80

        if recommendation.recommendation_class == RecommendationClass.HUMANIZE:
            headline = "Let's keep this conversation grounded and real"
            body = "We're focusing on organic pacing for tomorrow's session. Share your thoughts naturally without scripting."
        elif recommendation.recommendation_class == RecommendationClass.PROOF_GROUND:
            headline = "Building on solid ground"
            body = f"We are tracking our alignment. Let's work on this task: {recommendation.plain_language_goal}."
        elif recommendation.recommendation_class == RecommendationClass.SHARPEN:
            headline = "Direct and focused next steps"
            body = "Tomorrow's reaction drill is designed to be short, punchy, and direct."
        elif recommendation.recommendation_class == RecommendationClass.DECOMPRESS:
            headline = "Taking space to integrate"
            body = "Let's take a step back and reflect. Answer this open journaling prompt when you are ready."
        else:
            headline = "Your next calibration"
            body = "Tomorrow's session is prepared. We are continuing with the standard ritual."

        if has_humanity_strength:
            headline = f"Your voice brings unique clarity here — {headline}"
            body += " I really appreciate how real you have been in these notes. Let's keep that going."
        elif has_resonance_strength:
            headline = f"Resonating deeply with your progress — {headline}"

        # Strip Card/Board IDs
        headline = self._strip_card_ids(headline, intake.card_snapshot)
        body = self._strip_card_ids(body, intake.card_snapshot)

        # Check if slop risk is active
        slop_risk_active = intake.effect_summary.anti_slop_warning_active or (scores.ai_slop_risk.score_0_99 >= 45)
        if slop_risk_active:
            headline = self._de_smooth_text(headline)
            body = self._de_smooth_text(body)
            body = "Conversational focus: " + body

        # Reactance guard check
        if not self._validate_reactance_guard(body):
            body = "Tomorrow's session is ready. Feel free to explore it when you can."

        long_loop_ref = ""
        if trend_context.fourteen_day.status == TrendWindowStatus.POSITIVE:
            long_loop_ref = f"14-day trend: {trend_context.fourteen_day.headline_metric}"
        elif trend_context.thirty_day.status == TrendWindowStatus.POSITIVE:
            long_loop_ref = f"30-day trend: {trend_context.thirty_day.headline_metric}"
        else:
            long_loop_ref = f"Cumulative: {trend_context.cumulative_stats.total_sessions_completed} sessions"

        msg = RelationshipFramedCoachingMessage(
            message_id=f"msg-{uuid4().hex[:6]}",
            target_surface=recommendation.target_surface,
            safe_headline=headline,
            safe_body=body,
            long_loop_reference=long_loop_ref,
            score_translation_note=f"Score target: {recommendation.primary_score_target.value}",
            mentions_cards=False,
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(
                action="downgrade-interception",
                metadata={
                    "message_id": msg.message_id,
                    "safe_headline": headline,
                    "slop_risk_active": slop_risk_active,
                }
            )

        return msg
