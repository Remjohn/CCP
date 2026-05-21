"""
Phase-0 Unlock Propagator Service
=================================
Processes successful payment events to propagate Phase-0 asset unlock states,
grant downloadable entitlements, generate upgrade credits, and log audited receipts.
Also provides a repair routine for manual operators in case of runtime sync errors.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Any

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_commercial_models import (
    Phase0CommercialStage,
    Phase0EntitlementLevel,
    Phase0CommercialState,
    FirstProofUnlockRequest,
    FirstProofUnlockReceipt,
    UpgradeCreditState,
    Phase0EntitlementState,
)
from src.ccp.services.phase0_commercial_bridge import Phase0CommercialBridgeService


class Phase0UnlockPropagator:
    """Manages post-payment state transitions, asset delivery unlocks, and operator repair tools."""

    def __init__(
        self,
        bridge_service: Phase0CommercialBridgeService,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.bridge_service = bridge_service
        if receipt_chain is not None:
            self.receipt_chain = receipt_chain
        else:
            self.receipt_chain = bridge_service.receipt_chain

    def process_payment_callback(
        self,
        *,
        request_id: str,
        transaction_id: str,
        status: Literal["success", "failure"],
        simulate_failure_during_propagation: bool = False,
    ) -> FirstProofUnlockReceipt:
        """AC5 & AC6 & AC9: Processes first proof payment callback from Telegram webhook."""
        request = self.bridge_service.unlock_requests.get(request_id)
        if not request:
            raise ValueError(f"Unlock request with ID {request_id} not found.")

        packet_id = request.phase0_packet_id
        state = self.bridge_service.get_or_create_commercial_state(
            packet_id, request.delivery_run_id
        )

        receipt_id = f"rcpt-{uuid.uuid4().hex[:8]}"

        # AC9: If unlock payment fails, retain preview only
        if status == "failure":
            state.stage = Phase0CommercialStage.FAILED
            state.updated_at_utc = datetime.now(timezone.utc)

            receipt = FirstProofUnlockReceipt(
                receipt_id=receipt_id,
                request_id=request_id,
                coach_id=self.bridge_service.coach_acronym,
                phase0_packet_id=packet_id,
                transaction_id=transaction_id,
                amount_cents=request.amount_cents,
                payment_status="PAYMENT_FAILED",
                unlock_propagated=False,
                created_at_utc=datetime.now(timezone.utc),
                completed_at_utc=datetime.now(timezone.utc),
            )
            self.bridge_service.unlock_receipts[receipt_id] = receipt

            self.receipt_chain.log(
                agent_id="phase0_unlock_propagator",
                action="payment_failed",
                asset_id=transaction_id,
                person_id=packet_id,
                input_summary=f"Payment failure registered for request {request_id}",
                output_summary="User remains in preview-only state",
                decision="flagged",
            )
            return receipt

        # Log payment success
        self.receipt_chain.log(
            agent_id="phase0_unlock_propagator",
            action="payment_confirmed",
            asset_id=transaction_id,
            person_id=packet_id,
            input_summary=f"Payment success registered for request {request_id}",
            output_summary=f"Charge of {request.amount_cents} cents confirmed",
            decision="approved",
            metadata={"request_id": request_id},
        )

        # AC10: Handle simulated failure during propagation (repair state testing)
        if simulate_failure_during_propagation:
            receipt = FirstProofUnlockReceipt(
                receipt_id=receipt_id,
                request_id=request_id,
                coach_id=self.bridge_service.coach_acronym,
                phase0_packet_id=packet_id,
                transaction_id=transaction_id,
                amount_cents=request.amount_cents,
                payment_status="PAYMENT_SUCCESSFUL",
                unlock_propagated=False,
                created_at_utc=datetime.now(timezone.utc),
                completed_at_utc=None,
            )
            self.bridge_service.unlock_receipts[receipt_id] = receipt
            # Keep commercial stage as payment pending to reflect manual review need
            state.stage = Phase0CommercialStage.PAYMENT_PENDING
            state.updated_at_utc = datetime.now(timezone.utc)

            self.receipt_chain.log(
                agent_id="phase0_unlock_propagator",
                action="propagation_failed",
                asset_id=receipt_id,
                person_id=packet_id,
                input_summary="Unlock propagation crashed during DB handshake",
                output_summary="Repairable inconsistent state created",
                decision="flagged",
            )
            return receipt

        # Standard successful propagation (AC5 & AC6)
        receipt = FirstProofUnlockReceipt(
            receipt_id=receipt_id,
            request_id=request_id,
            coach_id=self.bridge_service.coach_acronym,
            phase0_packet_id=packet_id,
            transaction_id=transaction_id,
            amount_cents=request.amount_cents,
            payment_status="PROVISIONING_COMPLETE",
            unlock_propagated=True,
            created_at_utc=datetime.now(timezone.utc),
            completed_at_utc=datetime.now(timezone.utc),
        )
        self.bridge_service.unlock_receipts[receipt_id] = receipt

        self._execute_propagation_state_updates(packet_id, request.output_bundle_id, receipt_id)
        return receipt

    def _execute_propagation_state_updates(
        self, packet_id: str, output_bundle_id: str, receipt_id: str
    ) -> None:
        """Mutates entitlements and creates the upgrade credit state row."""
        state = self.bridge_service.commercial_states.get(packet_id)
        if not state:
            raise ValueError(f"Commercial state not found for packet {packet_id}")

        ent = self.bridge_service.get_or_create_entitlement_state(packet_id, output_bundle_id)

        # 1. Update Entitlements (AC5)
        ent.entitlement_level = Phase0EntitlementLevel.PHASE0_UNLOCKED
        ent.ownership_granted = True
        ent.audit_pdf_unlocked = True
        ent.audit_video_unlocked = True
        ent.proof_package_unlocked = True
        ent.downloadable_asset_keys = [
            "full_pdf_audit",
            "audit_explainer_video",
            "proof_package_zip",
        ]
        ent.updated_at_utc = datetime.now(timezone.utc)

        # 2. Update Commercial State stage
        state.stage = Phase0CommercialStage.PHASE0_UNLOCKED
        state.phase0_unlock_paid = True
        state.upgrade_credit_available = True
        state.updated_at_utc = datetime.now(timezone.utc)

        self.receipt_chain.log(
            agent_id="phase0_unlock_propagator",
            action="unlock_propagated",
            asset_id=output_bundle_id,
            person_id=packet_id,
            input_summary=f"Propagate asset entitlements for packet {packet_id}",
            output_summary=f"Entitlement level: {ent.entitlement_level.value} | Downloadable: {ent.downloadable_asset_keys}",
            decision="approved",
            metadata={"receipt_id": receipt_id},
        )

        # 3. Create Upgrade Credit State (AC6)
        credit_state_id = f"crd-{uuid.uuid4().hex[:8]}"
        valid_until = datetime.now(timezone.utc) + timedelta(days=7)  # Valid for 7 days
        credit = UpgradeCreditState(
            credit_state_id=credit_state_id,
            coach_id=self.bridge_service.coach_acronym,
            phase0_packet_id=packet_id,
            source_unlock_receipt_id=receipt_id,
            original_amount_cents=2999,
            remaining_amount_cents=2999,
            eligible_target_tiers=["SPEAKING_LEARNING", "COACH_OS"],
            valid_until_utc=valid_until,
            consumed=False,
        )
        self.bridge_service.upgrade_credits[credit_state_id] = credit

        self.receipt_chain.log(
            agent_id="phase0_unlock_propagator",
            action="credit_created",
            asset_id=credit_state_id,
            person_id=packet_id,
            input_summary=f"Generate upgrade credit of 2999 cents for packet {packet_id}",
            output_summary=f"Valid until {valid_until.isoformat()}",
            decision="approved",
            metadata={"credit_state_id": credit_state_id},
        )

    def retry_failed_propagation(self, receipt_id: str) -> bool:
        """AC10: Operator manual repair tool to execute a stalled propagation state."""
        receipt = self.bridge_service.unlock_receipts.get(receipt_id)
        if not receipt:
            raise ValueError(f"Unlock receipt {receipt_id} not found.")

        if receipt.unlock_propagated:
            return True  # Already propagated

        request = self.bridge_service.unlock_requests.get(receipt.request_id)
        if not request:
            raise ValueError(f"Associated unlock request {receipt.request_id} not found.")

        # Re-execute updates
        self._execute_propagation_state_updates(
            receipt.phase0_packet_id, request.output_bundle_id, receipt_id
        )

        # Update receipt status
        receipt.unlock_propagated = True
        receipt.payment_status = "PROVISIONING_COMPLETE"
        receipt.completed_at_utc = datetime.now(timezone.utc)

        self.receipt_chain.log(
            agent_id="phase0_unlock_propagator",
            action="manual_repair_resolved",
            asset_id=receipt_id,
            person_id=receipt.phase0_packet_id,
            input_summary=f"Operator manually repaired propagation for receipt {receipt_id}",
            output_summary="Unlock successfully completed and credit generated",
            decision="approved",
        )
        return True

    def process_upgrade_payment_success(
        self, *, packet_id: str, target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"]
    ) -> None:
        """Consumes the upgrade credit upon successful continuity subscription payment success."""
        credit = next(
            (
                c
                for c in self.bridge_service.upgrade_credits.values()
                if c.phase0_packet_id == packet_id
            ),
            None,
        )

        state = self.bridge_service.commercial_states.get(packet_id)

        if credit and not credit.consumed:
            credit.consumed = True
            credit.remaining_amount_cents = 0
            credit.consumed_at_utc = datetime.now(timezone.utc)
            credit.consumed_by_target_tier = target_tier

            if state:
                state.stage = Phase0CommercialStage.CREDIT_CONSUMED
                state.upgrade_credit_available = False
                state.upgrade_credit_consumed = True
                state.updated_at_utc = datetime.now(timezone.utc)

            # Update entitlement level to continuity
            ent = next(
                (
                    e
                    for e in self.bridge_service.entitlement_states.values()
                    if e.phase0_packet_id == packet_id
                ),
                None,
            )
            if ent:
                if target_tier == "SPEAKING_LEARNING":
                    ent.entitlement_level = Phase0EntitlementLevel.CONTINUITY_UNLOCKED
                else:
                    ent.entitlement_level = Phase0EntitlementLevel.COACH_OS_UNLOCKED
                ent.updated_at_utc = datetime.now(timezone.utc)

            self.receipt_chain.log(
                agent_id="phase0_unlock_propagator",
                action="credit_consumed",
                asset_id=credit.credit_state_id,
                person_id=packet_id,
                input_summary=f"Consume $29.99 upgrade credit for packet {packet_id}",
                output_summary=f"Continuity upgrade tier {target_tier} fully activated",
                decision="approved",
                metadata={
                    "credit_state_id": credit.credit_state_id,
                    "target_tier": target_tier,
                },
            )
