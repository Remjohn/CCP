"""
Phase-0 Commercial Bridge API Router
====================================
FastAPI endpoints for managing Phase-0 commercial projections, payment unlocks,
upgrade credit bridges, and manual operator repair sequences.
"""

from __future__ import annotations
from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Path, Body
from pydantic import BaseModel, Field

from src.ccp.models.phase0_delivery_models import Phase0OutputBundle
from src.ccp.models.cpsc_models import InvoicePayload
from src.ccp.models.phase0_commercial_models import (
    FirstProofUnlockRequest,
    FirstProofUnlockReceipt,
    UpgradeOfferBridge,
    Phase0UnlockProjection,
)
from src.ccp.services.phase0_commercial_bridge import Phase0CommercialBridgeService
from src.ccp.services.phase0_unlock_propagator import Phase0UnlockPropagator

router = APIRouter()

# Instantiate global service layers for Phase-0 Commercial Bridge
bridge_service = Phase0CommercialBridgeService()
unlock_propagator = Phase0UnlockPropagator(bridge_service=bridge_service)


# ── Request Body Schemas ───────────────────────────────────────────────

class UnlockInitiationRequest(BaseModel):
    delivery_run_id: str = Field(..., description="Unique active delivery run identifier")
    telegram_user_id: int = Field(..., description="Telegram user ID of the client")
    chat_id: int = Field(..., description="Telegram chat ID for invoice delivery")
    offer_copy_variant: Literal["standard", "loyalty_unlock", "phase0_unlock"] = "standard"
    output_bundle: Phase0OutputBundle = Field(..., description="The completed Phase-0 output bundle")


class PaymentSimulationRequest(BaseModel):
    request_id: str = Field(...)
    transaction_id: str = Field(...)
    status: Literal["success", "failure"] = "success"
    simulate_failure_during_propagation: bool = Field(default=False)


class UpgradeInitiationRequest(BaseModel):
    telegram_user_id: int = Field(...)
    chat_id: int = Field(...)
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"] = "SPEAKING_LEARNING"


class ManualRepairRequest(BaseModel):
    receipt_id: str = Field(..., description="The stuck/incomplete receipt ID to repair")


# ── API Endpoints ──────────────────────────────────────────────────────

@router.post("/commercial/{packet_id}/projection", response_model=Phase0UnlockProjection)
def project_unlock_offer(
    packet_id: str = Path(...),
    delivery_run_id: str = Body(..., embed=True),
    output_bundle: Phase0OutputBundle = Body(...)
):
    """AC1 & AC2: Projects first proof unlock details when the output bundle is fully generated."""
    try:
        return bridge_service.project_unlock_offer(
            packet_id=packet_id,
            delivery_run_id=delivery_run_id,
            output_bundle=output_bundle
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/commercial/{packet_id}/unlock", response_model=InvoicePayload)
async def initiate_unlock_invoice(
    packet_id: str = Path(...),
    payload: UnlockInitiationRequest = Body(...)
):
    """AC3 & AC4: Initiates one-time activation invoice for $29.99 via native Telegram Payment Handoff."""
    try:
        _, invoice = await bridge_service.initiate_unlock_invoice(
            packet_id=packet_id,
            delivery_run_id=payload.delivery_run_id,
            output_bundle=payload.output_bundle,
            telegram_user_id=payload.telegram_user_id,
            chat_id=payload.chat_id,
            offer_copy_variant=payload.offer_copy_variant
        )
        return invoice
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/commercial/simulate-payment", response_model=FirstProofUnlockReceipt)
def simulate_payment_callback(payload: PaymentSimulationRequest = Body(...)):
    """AC5 & AC6 & AC9: Simulates Telegram pre-checkout validation and successful payment events."""
    try:
        return unlock_propagator.process_payment_callback(
            request_id=payload.request_id,
            transaction_id=payload.transaction_id,
            status=payload.status,
            simulate_failure_during_propagation=payload.simulate_failure_during_propagation
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/commercial/{packet_id}/credit-bridge/{target_tier}", response_model=UpgradeOfferBridge)
def get_upgrade_bridge(
    packet_id: str = Path(...),
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"] = Path(...)
):
    """AC8: Returns the discounted continuity upgrade bridge summary ($29.99 applied)."""
    try:
        return bridge_service.get_upgrade_bridge(packet_id=packet_id, target_tier=target_tier)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/commercial/{packet_id}/upgrade", response_model=InvoicePayload)
async def initiate_upgrade_invoice(
    packet_id: str = Path(...),
    payload: UpgradeInitiationRequest = Body(...)
):
    """AC7: Initiates continuity upgrade, sending a custom discounted invoice utilizing credit."""
    try:
        _, invoice = await bridge_service.initiate_upgrade_invoice_with_credit(
            packet_id=packet_id,
            telegram_user_id=payload.telegram_user_id,
            chat_id=payload.chat_id,
            target_tier=payload.target_tier
        )
        return invoice
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/commercial/{packet_id}/upgrade/simulate-payment")
def simulate_upgrade_payment_success(
    packet_id: str = Path(...),
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"] = Body(..., embed=True)
):
    """Simulates upgrade subscription checkout completion webhook event to consume the credit."""
    try:
        unlock_propagator.process_upgrade_payment_success(
            packet_id=packet_id,
            target_tier=target_tier
        )
        return {"status": "success", "message": "Upgrade completed and credit consumed."}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/commercial/repair")
def repair_propagation(payload: ManualRepairRequest = Body(...)):
    """AC10: Executable endpoint for manual operator repair/recovery in case of network failures."""
    try:
        resolved = unlock_propagator.retry_failed_propagation(payload.receipt_id)
        return {"status": "success", "repaired": resolved}
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
