"""
FR-ERA3-37 Commercial Bridge and Payment Runtime Integration Tests
=====================================================================
Tests the complete Phase-0 Paid Activation ($29.99), entitlement propagation,
upgrade credit bridges ($29.99 credit applied to continuity tiers), and
manual operator repair workflows end-to-end using the FastAPI client.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient

from src.ccp.api.main import app
from src.ccp.models.phase0_delivery_models import Phase0OutputBundle
from src.ccp.models.phase0_commercial_models import (
    Phase0CommercialStage,
    Phase0EntitlementLevel,
    Phase0UnlockProjection,
    FirstProofUnlockReceipt,
    UpgradeOfferBridge,
)
from src.ccp.services.phase0_commercial_bridge import Phase0CommercialBridgeService
from src.ccp.services.phase0_unlock_propagator import Phase0UnlockPropagator
from src.ccp.core.receipt_chain import ReceiptChain


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestFRERA337CommercialBridgeSystem:

    def test_unlock_projection_ready_vs_not_ready(self, client: TestClient):
        """Verifies that ready bundles project correctly while not-ready bundles are blocked (Gate G1)."""
        packet_id = "pkt-test-proj-1"
        delivery_run_id = "run-test-proj-1"

        # 1. Test NOT-READY bundle: Should raise 400 error via the API (ValueError under the hood)
        not_ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-not-ready",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=False
        )

        proj_payload = {
            "delivery_run_id": delivery_run_id,
            "output_bundle": not_ready_bundle.model_dump(mode="json")
        }

        response = client.post(f"/api/phase0/commercial/{packet_id}/projection", json=proj_payload)
        assert response.status_code == 400
        assert "not payment-handoff-ready" in response.json()["detail"]

        # 2. Test READY bundle: Should project correctly
        ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-ready",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=True
        )

        proj_payload["output_bundle"] = ready_bundle.model_dump(mode="json")
        response = client.post(f"/api/phase0/commercial/{packet_id}/projection", json=proj_payload)
        assert response.status_code == 200
        
        projection = Phase0UnlockProjection.model_validate(response.json())
        assert projection.coach_id == "NDL"
        assert projection.phase0_packet_id == packet_id
        assert projection.current_stage == Phase0CommercialStage.UNLOCK_OFFER_READY
        assert projection.amount_cents == 2999
        assert "full_pdf_audit" in projection.locked_assets

        # Check that receipt was written for projection
        rc = ReceiptChain(coach_acronym="NDL")
        receipts = [r for r in rc.query(action="unlock_projected") if r.person_id == packet_id]
        assert len(receipts) >= 1
        assert any(r.person_id == packet_id for r in receipts)

    def test_initiate_unlock_invoice_and_block_duplicate(self, client: TestClient):
        """Verifies that initiate_unlock_invoice generates the $29.99 invoice and blocks duplicate in-flight requests."""
        packet_id = "pkt-test-inv-2"
        delivery_run_id = "run-test-inv-2"

        ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-test-inv-2",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=True
        )

        payload = {
            "delivery_run_id": delivery_run_id,
            "telegram_user_id": 123456,
            "chat_id": 987654,
            "offer_copy_variant": "loyalty_unlock",
            "output_bundle": ready_bundle.model_dump(mode="json")
        }

        # 1. Initiate invoice the first time
        response = client.post(f"/api/phase0/commercial/{packet_id}/unlock", json=payload)
        assert response.status_code == 200
        
        invoice = response.json()
        assert invoice["prices"] == [{"label": "Phase-0 Proof Unlock", "amount": 2999}]
        assert invoice["chat_id"] == 987654
        assert invoice["tier"] == "PHASE0_UNLOCK"
        assert "proven your commitment" in invoice["description"]

        # 2. Try to initiate invoice again while first is in-flight: Should return same existing invoice (block duplicates)
        response_dup = client.post(f"/api/phase0/commercial/{packet_id}/unlock", json=payload)
        assert response_dup.status_code == 200
        invoice_dup = response_dup.json()
        assert invoice_dup["invoice_id"] == invoice["invoice_id"]
        assert invoice_dup["payload"] == invoice["payload"]

        # Verify receipt was written
        rc = ReceiptChain(coach_acronym="NDL")
        receipts = [r for r in rc.query(action="invoice_sent") if r.person_id == packet_id]
        assert len(receipts) >= 1
        assert any(r.asset_id == invoice["invoice_id"] for r in receipts)

    def test_payment_callback_failure(self, client: TestClient):
        """Verifies that a simulated payment failure keeps the state preview-only."""
        packet_id = "pkt-test-fail-3"
        delivery_run_id = "run-test-fail-3"

        ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-test-fail-3",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=True
        )

        # First trigger an invoice to create the unlock request
        payload = {
            "delivery_run_id": delivery_run_id,
            "telegram_user_id": 123456,
            "chat_id": 987654,
            "offer_copy_variant": "standard",
            "output_bundle": ready_bundle.model_dump(mode="json")
        }
        client.post(f"/api/phase0/commercial/{packet_id}/unlock", json=payload)

        # Get the request ID from the in-memory service registry or parse it from invoice payload
        from src.ccp.api.phase0_commercial import bridge_service
        req_id = list(bridge_service.unlock_requests.keys())[-1]

        # Simulate failed payment callback
        sim_payload = {
            "request_id": req_id,
            "transaction_id": "tx-failed-123",
            "status": "failure"
        }
        response = client.post("/api/phase0/commercial/simulate-payment", json=sim_payload)
        assert response.status_code == 200
        
        receipt = FirstProofUnlockReceipt.model_validate(response.json())
        assert receipt.payment_status == "PAYMENT_FAILED"
        assert receipt.unlock_propagated is False

        # Verify commercial state stage is updated to FAILED
        state = bridge_service.commercial_states[packet_id]
        assert state.stage == Phase0CommercialStage.FAILED

        # Verify entitlement remains PREVIEW_ONLY
        ent = bridge_service.get_or_create_entitlement_state(packet_id, ready_bundle.output_bundle_id)
        assert ent.entitlement_level == Phase0EntitlementLevel.PREVIEW_ONLY
        assert not ent.ownership_granted

        # Verify receipt was written for payment failure
        rc = ReceiptChain(coach_acronym="NDL")
        receipts = [r for r in rc.query(action="payment_failed") if r.person_id == packet_id]
        assert len(receipts) >= 1

    def test_payment_callback_success_and_entitlement_propagation(self, client: TestClient):
        """Verifies successful payment callback unlocks assets, writes receipts, and generates a 7-day upgrade credit."""
        packet_id = "pkt-test-success-4"
        delivery_run_id = "run-test-success-4"

        ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-test-success-4",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=True
        )

        # 1. Trigger unlock invoice creation
        payload = {
            "delivery_run_id": delivery_run_id,
            "telegram_user_id": 111222,
            "chat_id": 333444,
            "offer_copy_variant": "standard",
            "output_bundle": ready_bundle.model_dump(mode="json")
        }
        client.post(f"/api/phase0/commercial/{packet_id}/unlock", json=payload)

        from src.ccp.api.phase0_commercial import bridge_service
        req_id = list(bridge_service.unlock_requests.keys())[-1]

        # 2. Simulate successful payment callback
        sim_payload = {
            "request_id": req_id,
            "transaction_id": "tx-success-456",
            "status": "success"
        }
        response = client.post("/api/phase0/commercial/simulate-payment", json=sim_payload)
        assert response.status_code == 200
        
        receipt = FirstProofUnlockReceipt.model_validate(response.json())
        assert receipt.payment_status == "PROVISIONING_COMPLETE"
        assert receipt.unlock_propagated is True
        assert receipt.completed_at_utc is not None

        # 3. Check expanded entitlements (download keys unlocked)
        ent = bridge_service.get_or_create_entitlement_state(packet_id, ready_bundle.output_bundle_id)
        assert ent.entitlement_level == Phase0EntitlementLevel.PHASE0_UNLOCKED
        assert ent.ownership_granted is True
        assert ent.audit_pdf_unlocked is True
        assert "full_pdf_audit" in ent.downloadable_asset_keys
        assert "audit_explainer_video" in ent.downloadable_asset_keys
        assert "proof_package_zip" in ent.downloadable_asset_keys

        # Check updated commercial state
        state = bridge_service.commercial_states[packet_id]
        assert state.stage == Phase0CommercialStage.PHASE0_UNLOCKED
        assert state.phase0_unlock_paid is True
        assert state.upgrade_credit_available is True

        # 4. Check 7-day Upgrade Credit generated (Gate G2 validation)
        credits = [c for c in bridge_service.upgrade_credits.values() if c.phase0_packet_id == packet_id]
        assert len(credits) == 1
        credit = credits[0]
        assert credit.original_amount_cents == 2999
        assert credit.remaining_amount_cents == 2999
        assert credit.consumed is False
        
        now = datetime.now(timezone.utc)
        time_diff = credit.valid_until_utc - now
        assert timedelta(days=6) < time_diff <= timedelta(days=7)

        # Check receipts logged in receipt chain
        rc = ReceiptChain(coach_acronym="NDL")
        assert len([r for r in rc.query(action="payment_confirmed") if r.person_id == packet_id]) >= 1
        assert len([r for r in rc.query(action="unlock_propagated") if r.person_id == packet_id]) >= 1
        assert len([r for r in rc.query(action="credit_created") if r.person_id == packet_id]) >= 1

    def test_upgrade_credit_bridge_pricing_and_consumption(self, client: TestClient):
        """Verifies upgrade credit applies correct discounts, generates invoice, and consumes it exactly once."""
        packet_id = "pkt-test-upgrade-5"
        delivery_run_id = "run-test-upgrade-5"

        ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-test-upgrade-5",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=True
        )

        # Setup: Buy the first proof unlock to generate credit
        payload = {
            "delivery_run_id": delivery_run_id,
            "telegram_user_id": 999888,
            "chat_id": 777666,
            "offer_copy_variant": "standard",
            "output_bundle": ready_bundle.model_dump(mode="json")
        }
        client.post(f"/api/phase0/commercial/{packet_id}/unlock", json=payload)

        from src.ccp.api.phase0_commercial import bridge_service
        req_id = list(bridge_service.unlock_requests.keys())[-1]

        client.post("/api/phase0/commercial/simulate-payment", json={
            "request_id": req_id,
            "transaction_id": "tx-upgrade-setup",
            "status": "success"
        })

        # 1. Query the Upgrade Offer Bridge for Speaking & Learning ($39.99 base)
        response_sl = client.get(f"/api/phase0/commercial/{packet_id}/credit-bridge/SPEAKING_LEARNING")
        assert response_sl.status_code == 200
        bridge_sl = UpgradeOfferBridge.model_validate(response_sl.json())
        assert bridge_sl.base_amount_cents == 3999
        assert bridge_sl.applied_credit_cents == 2999
        assert bridge_sl.final_amount_cents == 1000  # $39.99 - $29.99 = $10.00
        assert "pay only $10.00 today" in bridge_sl.bridge_copy

        # 2. Query the Upgrade Offer Bridge for Coach OS ($99.99 base)
        response_cos = client.get(f"/api/phase0/commercial/{packet_id}/credit-bridge/COACH_OS")
        assert response_cos.status_code == 200
        bridge_cos = UpgradeOfferBridge.model_validate(response_cos.json())
        assert bridge_cos.base_amount_cents == 9999
        assert bridge_cos.applied_credit_cents == 2999
        assert bridge_cos.final_amount_cents == 7000  # $99.99 - $29.99 = $70.00
        assert "pay only $70.00 today" in bridge_cos.bridge_copy

        # 3. Initiate discounted continuity upgrade invoice
        upgrade_payload = {
            "telegram_user_id": 999888,
            "chat_id": 777666,
            "target_tier": "SPEAKING_LEARNING"
        }
        res_inv = client.post(f"/api/phase0/commercial/{packet_id}/upgrade", json=upgrade_payload)
        assert res_inv.status_code == 200
        inv_data = res_inv.json()
        assert inv_data["prices"] == [{"label": "Subscription Upgrade", "amount": 1000}]
        assert inv_data["tier"] == "SPEAKING_LEARNING"

        # 4. Simulate successful upgrade checkout completion
        res_checkout = client.post(f"/api/phase0/commercial/{packet_id}/upgrade/simulate-payment", json={
            "target_tier": "SPEAKING_LEARNING"
        })
        assert res_checkout.status_code == 200
        assert res_checkout.json()["status"] == "success"

        # Verify credit is consumed exactly once
        credits = [c for c in bridge_service.upgrade_credits.values() if c.phase0_packet_id == packet_id]
        credit = credits[0]
        assert credit.consumed is True
        assert credit.remaining_amount_cents == 0
        assert credit.consumed_by_target_tier == "SPEAKING_LEARNING"

        # Verify entitlement is updated to CONTINUITY_UNLOCKED
        ent = bridge_service.get_or_create_entitlement_state(packet_id, ready_bundle.output_bundle_id)
        assert ent.entitlement_level == Phase0EntitlementLevel.CONTINUITY_UNLOCKED

        # Verify commercial stage is CREDIT_CONSUMED
        state = bridge_service.commercial_states[packet_id]
        assert state.stage == Phase0CommercialStage.CREDIT_CONSUMED

        # Verify receipt was written for credit consumption
        rc = ReceiptChain(coach_acronym="NDL")
        assert len([r for r in rc.query(action="credit_consumed") if r.person_id == packet_id]) >= 1

        # 5. Fallback check: Second upgrade checkout attempt with same packet_id should fail to apply credit
        response_expired = client.get(f"/api/phase0/commercial/{packet_id}/credit-bridge/COACH_OS")
        bridge_expired = UpgradeOfferBridge.model_validate(response_expired.json())
        assert bridge_expired.applied_credit_cents == 0
        assert bridge_expired.final_amount_cents == 9999

    def test_manual_repair_workflow(self, client: TestClient):
        """Verifies that the manual repair routine resolves propagation DB handshake failures cleanly (AC10)."""
        packet_id = "pkt-test-repair-6"
        delivery_run_id = "run-test-repair-6"

        ready_bundle = Phase0OutputBundle(
            output_bundle_id="bndl-test-repair-6",
            coach_id="NDL",
            phase0_packet_id=packet_id,
            payment_handoff_ready=True
        )

        # 1. Trigger invoice
        payload = {
            "delivery_run_id": delivery_run_id,
            "telegram_user_id": 555444,
            "chat_id": 222111,
            "offer_copy_variant": "standard",
            "output_bundle": ready_bundle.model_dump(mode="json")
        }
        client.post(f"/api/phase0/commercial/{packet_id}/unlock", json=payload)

        from src.ccp.api.phase0_commercial import bridge_service
        req_id = list(bridge_service.unlock_requests.keys())[-1]

        # 2. Simulate payment success but with propagation failure
        sim_payload = {
            "request_id": req_id,
            "transaction_id": "tx-repair-789",
            "status": "success",
            "simulate_failure_during_propagation": True
        }
        res_fail = client.post("/api/phase0/commercial/simulate-payment", json=sim_payload)
        assert res_fail.status_code == 200
        
        receipt = FirstProofUnlockReceipt.model_validate(res_fail.json())
        assert receipt.payment_status == "PAYMENT_SUCCESSFUL"
        assert receipt.unlock_propagated is False

        # Commercial stage should be payment pending indicating the error
        state = bridge_service.commercial_states[packet_id]
        assert state.stage == Phase0CommercialStage.PAYMENT_PENDING

        # Entitlement remains preview only
        ent = bridge_service.get_or_create_entitlement_state(packet_id, ready_bundle.output_bundle_id)
        assert ent.entitlement_level == Phase0EntitlementLevel.PREVIEW_ONLY

        # 3. Trigger manual repair endpoint via the API
        repair_payload = {
            "receipt_id": receipt.receipt_id
        }
        res_repair = client.post("/api/phase0/commercial/repair", json=repair_payload)
        assert res_repair.status_code == 200
        assert res_repair.json()["status"] == "success"
        assert res_repair.json()["repaired"] is True

        # Verify entitlement is now fully unlocked
        ent_repaired = bridge_service.get_or_create_entitlement_state(packet_id, ready_bundle.output_bundle_id)
        assert ent_repaired.entitlement_level == Phase0EntitlementLevel.PHASE0_UNLOCKED
        assert ent_repaired.ownership_granted is True
        assert "full_pdf_audit" in ent_repaired.downloadable_asset_keys

        # Verify updated stage is phase0 unlocked
        state_repaired = bridge_service.commercial_states[packet_id]
        assert state_repaired.stage == Phase0CommercialStage.PHASE0_UNLOCKED

        # Verify repair is logged
        rc = ReceiptChain(coach_acronym="NDL")
        assert len([r for r in rc.query(action="manual_repair_resolved") if r.person_id == packet_id]) >= 1
