"""
Phase-0 Commercial Bridge and Payment Runtime Models
=====================================================
Pydantic v2 models, enums, and constants for FR-ERA3-37.
Provides canonical types for tracking first proof activation, entitlement states,
upgrade credit bridges, and Telegram-native checkout handoffs.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class Phase0CommercialStage(str, Enum):
    PROOF_VISIBLE = "PROOF_VISIBLE"
    UNLOCK_OFFER_READY = "UNLOCK_OFFER_READY"
    INVOICE_SENT = "INVOICE_SENT"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PHASE0_UNLOCKED = "PHASE0_UNLOCKED"
    UPGRADE_BRIDGE_READY = "UPGRADE_BRIDGE_READY"
    CREDIT_CONSUMED = "CREDIT_CONSUMED"
    FAILED = "FAILED"


class Phase0EntitlementLevel(str, Enum):
    PREVIEW_ONLY = "PREVIEW_ONLY"
    PHASE0_UNLOCKED = "PHASE0_UNLOCKED"
    CONTINUITY_UNLOCKED = "CONTINUITY_UNLOCKED"
    COACH_OS_UNLOCKED = "COACH_OS_UNLOCKED"


class Phase0CommercialState(BaseModel):
    commercial_state_id: str = Field(..., description="Unique state tracking ID")
    coach_id: str = Field(..., description="Coach identifier (e.g. NDL)")
    phase0_packet_id: str = Field(..., description="Prospect packet ID")
    delivery_run_id: str = Field(..., description="Delivery execution run ID")
    stage: Phase0CommercialStage = Field(default=Phase0CommercialStage.PROOF_VISIBLE)
    current_offer_key: str = Field(default="phase0_proof_unlock")
    phase0_unlock_paid: bool = Field(default=False)
    upgrade_credit_available: bool = Field(default=False)
    upgrade_credit_consumed: bool = Field(default=False)
    telegram_chat_id: Optional[int] = Field(default=None)
    last_invoice_id: Optional[str] = Field(default=None)
    updated_at_utc: datetime = Field(default_factory=datetime.utcnow)


class FirstProofUnlockRequest(BaseModel):
    request_id: str = Field(...)
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    delivery_run_id: str = Field(...)
    telegram_user_id: int = Field(...)
    chat_id: int = Field(...)
    amount_cents: int = Field(default=2999, ge=2999, le=2999)
    currency: str = Field(default="USD")
    offer_copy_variant: Literal["standard", "loyalty_unlock", "phase0_unlock"] = "standard"
    output_bundle_id: str = Field(...)
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)


class FirstProofUnlockReceipt(BaseModel):
    receipt_id: str = Field(...)
    request_id: str = Field(...)
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    invoice_id: Optional[str] = Field(default=None)
    transaction_id: Optional[str] = Field(default=None)
    amount_cents: int = Field(default=2999, ge=2999)
    payment_status: Literal[
        "INVOICE_SENT",
        "PRE_CHECKOUT_CONFIRMED",
        "REQUIRES_ACTION",
        "PAYMENT_SUCCESSFUL",
        "PAYMENT_FAILED",
        "REWARD_DISPATCHED",
        "PROVISIONING_COMPLETE",
    ] = "INVOICE_SENT"
    unlock_propagated: bool = Field(default=False)
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)
    completed_at_utc: Optional[datetime] = Field(default=None)


class UpgradeCreditState(BaseModel):
    credit_state_id: str = Field(...)
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    source_unlock_receipt_id: str = Field(...)
    original_amount_cents: int = Field(default=2999, ge=2999)
    remaining_amount_cents: int = Field(default=2999, ge=0, le=2999)
    eligible_target_tiers: List[str] = Field(default_factory=lambda: ["SPEAKING_LEARNING", "COACH_OS"])
    valid_until_utc: datetime = Field(...)
    consumed: bool = Field(default=False)
    consumed_at_utc: Optional[datetime] = Field(default=None)
    consumed_by_target_tier: Optional[Literal["SPEAKING_LEARNING", "COACH_OS"]] = Field(default=None)


class UpgradeOfferBridge(BaseModel):
    bridge_id: str = Field(...)
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"]
    base_amount_cents: int = Field(..., ge=0)
    applied_credit_cents: int = Field(..., ge=0)
    final_amount_cents: int = Field(..., ge=0)
    bridge_copy: str = Field(...)
    credit_state_id: Optional[str] = Field(default=None)
    expires_at_utc: Optional[datetime] = Field(default=None)


class Phase0EntitlementState(BaseModel):
    entitlement_state_id: str = Field(...)
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    output_bundle_id: str = Field(...)
    entitlement_level: Phase0EntitlementLevel = Field(default=Phase0EntitlementLevel.PREVIEW_ONLY)
    visible_asset_keys: List[str] = Field(default_factory=list)
    downloadable_asset_keys: List[str] = Field(default_factory=list)
    ownership_granted: bool = Field(default=False)
    audit_pdf_unlocked: bool = Field(default=False)
    audit_video_unlocked: bool = Field(default=False)
    proof_package_unlocked: bool = Field(default=False)
    updated_at_utc: datetime = Field(default_factory=datetime.utcnow)


class Phase0UpgradeInvoiceRequest(BaseModel):
    telegram_user_id: int = Field(...)
    chat_id: int = Field(...)
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"]
    credit_state_id: Optional[str] = Field(default=None)
    applied_credit_cents: int = Field(default=0, ge=0)


class Phase0UnlockProjection(BaseModel):
    coach_id: str = Field(...)
    phase0_packet_id: str = Field(...)
    current_stage: Phase0CommercialStage
    free_visible_assets: List[str] = Field(default_factory=list)
    locked_assets: List[str] = Field(default_factory=list)
    unlock_offer_title: str = Field(...)
    unlock_offer_summary: str = Field(...)
    amount_cents: int = Field(default=2999)
    telegram_native: bool = Field(default=True)
