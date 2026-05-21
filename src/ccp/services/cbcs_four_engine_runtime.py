from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4
from src.ccp.models.cbcs_models import (
    CBCSEvidencePacket, CBCSRuntimeSession, CBCSSubmissionKind, CapacityTrack,
    DiagnosticCapacityDecision, RelationshipFramedNotification, RitualAdjustmentPlan,
    CbcsPerceptualIntakeEnvelope, CbcsPerceptualRecommendation, CbcsPerceptualRuntimeReceipt,
    RelationshipInterceptionReason, DiagnosticChangeType,
)
from src.ccp.services.cbcs_evidence_engine import CBCSEvidenceEngineService
from src.ccp.services.cbcs_diagnostic_engine import CBCSDiagnosticEngineService
from src.ccp.services.cbcs_ritual_engine import CBCSRitualEngineService
from src.ccp.services.cbcs_relationship_engine import CBCSRelationshipEngineService


class CBCSFourEngineRuntimeService:
    """Single orchestration entrypoint composing the four physically separate engines.
    Process: evidence -> diagnostic -> ritual -> relationship framing.
    Only RelationshipFramedNotification may be dispatched to the user."""

    def __init__(self, evidence_engine: CBCSEvidenceEngineService, diagnostic_engine: CBCSDiagnosticEngineService, ritual_engine: CBCSRitualEngineService, relationship_engine: CBCSRelationshipEngineService, receipt_chain: Any = None) -> None:
        self._evidence = evidence_engine
        self._diagnostic = diagnostic_engine
        self._ritual = ritual_engine
        self._relationship = relationship_engine
        self._receipt_chain = receipt_chain

    async def process_submission(self, *, client_id: str, coach_id: str, submission_kind: CBCSSubmissionKind, transcript: str = "", previous_track: CapacityTrack = CapacityTrack.FOUNDATION, perceptual_intake: Optional[CbcsPerceptualIntakeEnvelope] = None) -> CBCSRuntimeSession:
        session_id = str(uuid4())

        # Stage 1: Evidence extraction (with optional perceptual intake)
        evidence = await self._evidence.extract_evidence(client_id=client_id, coach_id=coach_id, submission_kind=submission_kind, transcript=transcript, perceptual_intake=perceptual_intake)

        # Stage 2: Diagnostic decision (internal-only)
        diagnostic = await self._diagnostic.diagnose(evidence=evidence, previous_track=previous_track)
        perceptual_rec = await self._diagnostic.diagnose_perceptual(evidence=evidence)

        # Stage 3: Ritual planning
        ritual_plan = await self._ritual.plan_ritual(diagnostic=diagnostic)
        vn_guidance = None
        acc_prescription = None
        if perceptual_rec is not None and perceptual_intake is not None:
            vn_guidance, acc_prescription = await self._ritual.generate_perceptual_plans(recommendation=perceptual_rec, intake=perceptual_intake)

        # Stage 4: Relationship context + framing
        trend_context = await self._relationship.build_trend_context(client_id=client_id, coach_id=coach_id)

        notification = None
        coaching_msg = None
        if perceptual_rec is not None and perceptual_intake is not None:
            coaching_msg = await self._relationship.frame_coaching_message(
                recommendation=perceptual_rec,
                vn_guidance=vn_guidance,
                acc_prescription=acc_prescription,
                intake=perceptual_intake,
                trend_context=trend_context,
            )

            # Map the coaching message to the official user notification
            interception_reason = RelationshipInterceptionReason.NONE
            if diagnostic.change_type == DiagnosticChangeType.DOWNGRADE:
                interception_reason = RelationshipInterceptionReason.CAPACITY_TRACK_DOWNGRADE
            elif diagnostic.change_type == DiagnosticChangeType.RITUAL_INTENSITY_REDUCTION:
                interception_reason = RelationshipInterceptionReason.RITUAL_INTENSITY_REDUCTION
            elif diagnostic.change_type == DiagnosticChangeType.REFLECTION_SUBSTITUTION:
                interception_reason = RelationshipInterceptionReason.CORROSIVE_LOOP_INTERRUPTION

            notification = RelationshipFramedNotification(
                notification_id=coaching_msg.message_id,
                client_id=client_id,
                coach_id=coach_id,
                interception_reason=interception_reason,
                safe_headline=coaching_msg.safe_headline[:180],
                safe_body=coaching_msg.safe_body[:1200],
                visible_macro_metric=coaching_msg.long_loop_reference[:100] if coaching_msg.long_loop_reference else None,
                visible_cumulative_metric=coaching_msg.score_translation_note[:100] if coaching_msg.score_translation_note else None,
                dispatch_channel="telegram",
                integrity_report=None,
                created_at=datetime.now(timezone.utc),
            )

        # Legacy fallback if no perceptual path was executed or framing failed
        if notification is None:
            notification = await self._relationship.frame_notification(diagnostic=diagnostic, ritual_plan=ritual_plan, trend_context=trend_context, evidence=evidence)

        if notification is None:
            # Framing failed — block dispatch, return internal hold
            if self._receipt_chain is not None:
                self._receipt_chain.log(action="relationship-frame-blocked", metadata={"session_id": session_id, "client_id": client_id})
            # Create a hold notification
            notification = RelationshipFramedNotification(
                notification_id=str(uuid4()), client_id=client_id, coach_id=coach_id,
                interception_reason=diagnostic.change_type.value if hasattr(diagnostic.change_type, 'value') else "none",
                safe_headline="Session processing", safe_body="Your session has been recorded and is being reviewed.",
                dispatch_channel="internal_hold", created_at=datetime.now(timezone.utc),
            )

        # Final dispatch and receipt logging
        if perceptual_rec is not None and perceptual_intake is not None and coaching_msg is not None:
            fallback_mode = None
            if perceptual_intake.source_reference.source_contract_id == "FALLBACK_SFL_EVAL":
                fallback_mode = "visible_scores_only"

            receipt = CbcsPerceptualRuntimeReceipt(
                receipt_id=f"rcpt-{uuid4().hex[:6]}",
                envelope_id=perceptual_intake.envelope_id,
                recommendation_id=perceptual_rec.recommendation_id,
                relationship_message_id=coaching_msg.message_id,
                fallback_mode=fallback_mode,
                source_contract_id=perceptual_intake.source_reference.source_contract_id,
            )

            if self._receipt_chain is not None:
                self._receipt_chain.log(
                    action="final-dispatch",
                    metadata={
                        "receipt_id": receipt.receipt_id,
                        "envelope_id": receipt.envelope_id,
                        "fallback_mode": receipt.fallback_mode,
                        "source_contract_id": receipt.source_contract_id,
                    }
                )

        elif self._receipt_chain is not None:
            self._receipt_chain.log(action="final-dispatch", metadata={"session_id": session_id, "dispatch_channel": notification.dispatch_channel, "interception_reason": notification.interception_reason.value if hasattr(notification.interception_reason, 'value') else str(notification.interception_reason)})

        session = CBCSRuntimeSession(
            session_id=session_id, client_id=client_id, coach_id=coach_id,
            submission_kind=submission_kind, evidence_packet=evidence,
            diagnostic_decision=diagnostic, ritual_plan=ritual_plan,
            relationship_context=trend_context, user_notification=notification,
            perceptual_recommendation=perceptual_rec,
        )

        return session

