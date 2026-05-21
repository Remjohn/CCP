"""
Phase-0 Commercial Bridge Service
=================================
Business logic for managing Phase-0 commercial states, Telegram invoices for $29.99
first proof unlock, and upgrade credit bridges into Speaking & Learning / Coach OS.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Literal, Tuple, Any, List

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_delivery_models import Phase0OutputBundle
from src.ccp.models.cpsc_models import (
    EligibilityCheckResult,
    EligibilityVerdict,
    InvoicePayload,
    StoredValueSnapshot,
)
from src.ccp.models.phase0_commercial_models import (
    Phase0CommercialStage,
    Phase0EntitlementLevel,
    Phase0CommercialState,
    FirstProofUnlockRequest,
    FirstProofUnlockReceipt,
    UpgradeCreditState,
    UpgradeOfferBridge,
    Phase0EntitlementState,
    Phase0UnlockProjection,
)
from src.ccp.services.telegram_invoice_handler import TelegramInvoiceHandler


class Phase0CommercialBridgeService:
    """Manages Phase-0 commercial states, projections, and continuity upgrade credit bridges."""

    def __init__(
        self,
        coach_acronym: str = "NDL",
        provider_token: str = "PROVIDER_TOKEN",
        bot_token: str = "BOT_TOKEN",
        supabase_client: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.provider_token = provider_token
        self.bot_token = bot_token
        self.supabase = supabase_client

        if receipt_chain is not None:
            self.receipt_chain = receipt_chain
        else:
            self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

        # In-memory persistence mirroring DB schemas
        self.commercial_states: Dict[str, Phase0CommercialState] = {}
        self.unlock_requests: Dict[str, FirstProofUnlockRequest] = {}
        self.unlock_receipts: Dict[str, FirstProofUnlockReceipt] = {}
        self.upgrade_credits: Dict[str, UpgradeCreditState] = {}
        self.upgrade_bridges: Dict[str, UpgradeOfferBridge] = {}
        self.entitlement_states: Dict[str, Phase0EntitlementState] = {}

    def get_or_create_commercial_state(
        self, packet_id: str, delivery_run_id: str
    ) -> Phase0CommercialState:
        """Retrieves or creates a commercial state row for the packet."""
        if packet_id not in self.commercial_states:
            state = Phase0CommercialState(
                commercial_state_id=f"comm-state-{uuid.uuid4().hex[:8]}",
                coach_id=self.coach_acronym,
                phase0_packet_id=packet_id,
                delivery_run_id=delivery_run_id,
                stage=Phase0CommercialStage.PROOF_VISIBLE,
                current_offer_key="phase0_proof_unlock",
                phase0_unlock_paid=False,
                upgrade_credit_available=False,
                upgrade_credit_consumed=False,
                updated_at_utc=datetime.now(timezone.utc),
            )
            self.commercial_states[packet_id] = state
        return self.commercial_states[packet_id]

    def get_or_create_entitlement_state(
        self, packet_id: str, bundle_id: str
    ) -> Phase0EntitlementState:
        """Retrieves or creates an entitlement state row for the packet."""
        if packet_id not in self.entitlement_states:
            state = Phase0EntitlementState(
                entitlement_state_id=f"ent-state-{uuid.uuid4().hex[:8]}",
                coach_id=self.coach_acronym,
                phase0_packet_id=packet_id,
                output_bundle_id=bundle_id,
                entitlement_level=Phase0EntitlementLevel.PREVIEW_ONLY,
                visible_asset_keys=["teaser", "score_cards", "preview_board"],
                downloadable_asset_keys=[],
                ownership_granted=False,
                audit_pdf_unlocked=False,
                audit_video_unlocked=False,
                proof_package_unlocked=False,
                updated_at_utc=datetime.now(timezone.utc),
            )
            self.entitlement_states[packet_id] = state
        return self.entitlement_states[packet_id]

    def project_unlock_offer(
        self, *, packet_id: str, delivery_run_id: str, output_bundle: Phase0OutputBundle
    ) -> Phase0UnlockProjection:
        """AC1 & AC2: Project first proof unlock offer if the bundle is ready."""
        # Gate G1 check
        if not output_bundle.payment_handoff_ready:
            raise ValueError("Output bundle is not payment-handoff-ready. Projection blocked.")

        state = self.get_or_create_commercial_state(packet_id, delivery_run_id)
        ent = self.get_or_create_entitlement_state(packet_id, output_bundle.output_bundle_id)

        # Update stage to offer ready if currently proof visible
        if state.stage == Phase0CommercialStage.PROOF_VISIBLE:
            state.stage = Phase0CommercialStage.UNLOCK_OFFER_READY
            state.updated_at_utc = datetime.now(timezone.utc)

        # Log projection
        self.receipt_chain.log(
            agent_id="phase0_commercial_bridge",
            action="unlock_projected",
            asset_id=output_bundle.output_bundle_id,
            person_id=packet_id,
            input_summary=f"Project first proof unlock offer for packet {packet_id}",
            output_summary=f"Visible: {ent.visible_asset_keys} | Locked: ['full_pdf_audit', 'explainer_video', 'proof_package']",
            decision="approved",
            metadata={"stage": state.stage.value, "amount_cents": 2999},
        )

        return Phase0UnlockProjection(
            coach_id=self.coach_acronym,
            phase0_packet_id=packet_id,
            current_stage=state.stage,
            free_visible_assets=ent.visible_asset_keys,
            locked_assets=["full_pdf_audit", "explainer_video", "proof_package"],
            unlock_offer_title="Unlock Full Audit & Premium Co-Creation Assets",
            unlock_offer_summary="Get download ownership of your 3D Audit PDF, Explainer Video, and custom assets.",
            amount_cents=2999,
            telegram_native=True,
        )

    async def initiate_unlock_invoice(
        self,
        *,
        packet_id: str,
        delivery_run_id: str,
        output_bundle: Phase0OutputBundle,
        telegram_user_id: int,
        chat_id: int,
        offer_copy_variant: Literal["standard", "loyalty_unlock", "phase0_unlock"] = "standard",
    ) -> Tuple[FirstProofUnlockRequest, InvoicePayload]:
        """AC3 & AC4: Initiates the first proof unlock transaction and sends a Telegram invoice."""
        # Gate G1 check
        if not output_bundle.payment_handoff_ready:
            raise ValueError("Output bundle is not payment-handoff-ready. Invoice initiation blocked.")

        state = self.get_or_create_commercial_state(packet_id, delivery_run_id)

        # Fallback F3: Check if a payment is already in-flight/pending to block duplicate invoices
        if state.stage in (Phase0CommercialStage.INVOICE_SENT, Phase0CommercialStage.PAYMENT_PENDING):
            # Try to return the existing request if it exists
            existing_req = next(
                (r for r in self.unlock_requests.values() if r.phase0_packet_id == packet_id),
                None,
            )
            if existing_req:
                # Mock payload representing the in-flight invoice
                existing_invoice = InvoicePayload(
                    invoice_id=state.last_invoice_id or f"inv-{uuid.uuid4().hex[:8]}",
                    chat_id=chat_id,
                    title="Unlock Full Audit & Premium Co-Creation Assets",
                    description="Get download ownership of your 3D Audit PDF, Explainer Video, and custom assets.",
                    payload=f"ccp_phase0_unlock:{existing_req.request_id}",
                    provider_token=self.provider_token,
                    currency="USD",
                    prices=[{"label": "Phase-0 Proof Unlock", "amount": 2999}],
                    tier="PHASE0_UNLOCK",
                    sent_at=datetime.now(timezone.utc).isoformat(),
                )
                return existing_req, existing_invoice

        request_id = f"req-{uuid.uuid4().hex[:8]}"
        request = FirstProofUnlockRequest(
            request_id=request_id,
            coach_id=self.coach_acronym,
            phase0_packet_id=packet_id,
            delivery_run_id=delivery_run_id,
            telegram_user_id=telegram_user_id,
            chat_id=chat_id,
            amount_cents=2999,
            currency="USD",
            offer_copy_variant=offer_copy_variant,
            output_bundle_id=output_bundle.output_bundle_id,
            created_at_utc=datetime.now(timezone.utc),
        )

        # Prepare description based on copy variant
        if offer_copy_variant == "loyalty_unlock":
            description = "You've proven your commitment. Unlock your full high-fidelity assets now."
        elif offer_copy_variant == "phase0_unlock":
            description = "Complete your Phase-0 diagnostic. Activate your premium proof package."
        else:
            description = "Get download ownership of your 3D Audit PDF, Explainer Video, and custom assets."

        # Interoperate with TelegramInvoiceHandler system natively (no external URL checkout)
        eligibility = EligibilityCheckResult(
            eligibility_id=f"el-{uuid.uuid4().hex[:8]}",
            telegram_user_id=telegram_user_id,
            coach_id=self.coach_acronym,
            target_tier="SPEAKING_LEARNING",  # dummy for interop
            current_stripe_status="free",
            stored_value=StoredValueSnapshot(cumulative_assets_stored=10),
            verdict=EligibilityVerdict.PASS_STANDARD.value,
            offer_copy_variant="standard",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

        invoice_handler = TelegramInvoiceHandler(
            provider_token=self.provider_token,
            bot_token=self.bot_token,
            receipt_chain=self.receipt_chain,
        )

        # Construct payload manually to match $29.99 instead of standard tiers
        invoice_id = f"inv-{uuid.uuid4().hex[:8]}"
        payload = InvoicePayload(
            invoice_id=invoice_id,
            chat_id=chat_id,
            title="First Proof Unlock",
            description=description,
            payload=f"ccp_phase0_unlock:{request_id}",
            provider_token=self.provider_token,
            currency="USD",
            prices=[{"label": "Phase-0 Proof Unlock", "amount": 2999}],
            tier="PHASE0_UNLOCK",
            sent_at=datetime.now(timezone.utc).isoformat(),
        )

        # Send it via Telegram Bot API sendInvoice
        if self.bot_token and self.bot_token != "BOT_TOKEN":
            import httpx
            url = f"https://api.telegram.org/bot{self.bot_token}/sendInvoice"
            invoice_data = {
                "chat_id": payload.chat_id,
                "title": payload.title,
                "description": payload.description,
                "payload": payload.payload,
                "provider_token": payload.provider_token,
                "currency": payload.currency,
                "prices": payload.prices,
            }
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=invoice_data)
                    response.raise_for_status()
            except Exception as e:
                # Fallback F2: Send invoice failure
                state.stage = Phase0CommercialStage.FAILED
                state.updated_at_utc = datetime.now(timezone.utc)
                self.receipt_chain.log(
                    agent_id="phase0_commercial_bridge",
                    action="invoice-send-failed",
                    asset_id=request_id,
                    person_id=packet_id,
                    input_summary="Telegram invoice delivery failure",
                    output_summary=str(e),
                    decision="flagged",
                )
                raise RuntimeError(f"Telegram invoice delivery failed: {e}")

        # Update state persistence
        state.stage = Phase0CommercialStage.INVOICE_SENT
        state.last_invoice_id = invoice_id
        state.telegram_chat_id = chat_id
        state.updated_at_utc = datetime.now(timezone.utc)

        self.unlock_requests[request_id] = request

        # Log invoice generation and transmission
        self.receipt_chain.log(
            agent_id="phase0_commercial_bridge",
            action="invoice_sent",
            asset_id=invoice_id,
            person_id=packet_id,
            input_summary=f"Initiate $29.99 unlock request: {request_id}",
            output_summary=f"Sent Telegram invoice {invoice_id} to chat {chat_id}",
            decision="approved",
            metadata={
                "request_id": request_id,
                "amount_cents": 2999,
                "variant": offer_copy_variant,
            },
        )

        return request, payload

    def get_upgrade_bridge(
        self, *, packet_id: str, target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"]
    ) -> UpgradeOfferBridge:
        """AC8: Produces a clean upgrade bridge offer applying the $29.99 credit if eligible."""
        # Find credit state
        credit = next(
            (c for c in self.upgrade_credits.values() if c.phase0_packet_id == packet_id),
            None,
        )

        base_amount = 3999 if target_tier == "SPEAKING_LEARNING" else 9999
        applied_credit = 0
        credit_state_id = None
        expires_at = None

        if credit:
            credit_state_id = credit.credit_state_id
            expires_at = credit.valid_until_utc
            now = datetime.now(timezone.utc)

            # Check eligibility rules (Gate G2): validity & single consumption
            if not credit.consumed and credit.valid_until_utc > now:
                applied_credit = credit.remaining_amount_cents

        final_amount = max(0, base_amount - applied_credit)

        tier_label = "Speaking & Learning" if target_tier == "SPEAKING_LEARNING" else "Coach OS"
        if applied_credit > 0:
            bridge_copy = (
                f"Continue your growth. Your $29.99 first proof unlock credit has been applied "
                f"to your first month of {tier_label}. You pay only ${final_amount / 100:.2f} today."
            )
        else:
            bridge_copy = (
                f"Upgrade to {tier_label} to unlock continuous biometric tracking and full coaching tools. "
                f"Price: ${final_amount / 100:.2f} / month."
            )

        bridge_id = f"br-{uuid.uuid4().hex[:8]}"
        bridge = UpgradeOfferBridge(
            bridge_id=bridge_id,
            coach_id=self.coach_acronym,
            phase0_packet_id=packet_id,
            target_tier=target_tier,
            base_amount_cents=base_amount,
            applied_credit_cents=applied_credit,
            final_amount_cents=final_amount,
            bridge_copy=bridge_copy,
            credit_state_id=credit_state_id,
            expires_at_utc=expires_at,
        )

        self.upgrade_bridges[bridge_id] = bridge
        return bridge

    async def initiate_upgrade_invoice_with_credit(
        self,
        *,
        packet_id: str,
        telegram_user_id: int,
        chat_id: int,
        target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"],
    ) -> Tuple[UpgradeOfferBridge, InvoicePayload]:
        """AC7: Generates a continuity upgrade invoice consuming the one-time credit."""
        bridge = self.get_upgrade_bridge(packet_id=packet_id, target_tier=target_tier)

        # Fallback F6: If credit state was expected but expired or missing, block discounted checkout
        credit = next(
            (c for c in self.upgrade_credits.values() if c.phase0_packet_id == packet_id),
            None,
        )
        if bridge.applied_credit_cents > 0 and (not credit or credit.consumed):
            raise ValueError("Credit is already consumed or invalid. Discount blocked.")

        # Construct and send Telegram invoice for final amount
        invoice_id = f"inv-{uuid.uuid4().hex[:8]}"
        payload = InvoicePayload(
            invoice_id=invoice_id,
            chat_id=chat_id,
            title=f"Upgrade to {'Speaking & Learning' if target_tier == 'SPEAKING_LEARNING' else 'Coach OS'}",
            description=bridge.bridge_copy,
            payload=f"ccp_upgrade:{packet_id}:{target_tier}:{bridge.bridge_id}",
            provider_token=self.provider_token,
            currency="USD",
            prices=[{"label": "Subscription Upgrade", "amount": bridge.final_amount_cents}],
            tier=target_tier,
            sent_at=datetime.now(timezone.utc).isoformat(),
        )

        if self.bot_token and self.bot_token != "BOT_TOKEN":
            import httpx
            url = f"https://api.telegram.org/bot{self.bot_token}/sendInvoice"
            invoice_data = {
                "chat_id": payload.chat_id,
                "title": payload.title,
                "description": payload.description,
                "payload": payload.payload,
                "provider_token": payload.provider_token,
                "currency": payload.currency,
                "prices": payload.prices,
            }
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=invoice_data)
                    response.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"Failed to transmit Telegram upgrade invoice: {e}")

        # State logging
        self.receipt_chain.log(
            agent_id="phase0_commercial_bridge",
            action="upgrade_invoice_sent",
            asset_id=invoice_id,
            person_id=packet_id,
            input_summary=f"Generate upgrade invoice with credit applied for packet {packet_id}",
            output_summary=f"Sent invoice {invoice_id} for {bridge.final_amount_cents} cents",
            decision="approved",
            metadata={
                "bridge_id": bridge.bridge_id,
                "applied_credit_cents": bridge.applied_credit_cents,
                "base_amount_cents": bridge.base_amount_cents,
                "final_amount_cents": bridge.final_amount_cents,
            },
        )

        return bridge, payload
