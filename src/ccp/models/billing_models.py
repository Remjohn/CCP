from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID


class BillingTier(str, Enum):
    PROOF_LAYER = "proof_layer"
    SPEAKING_LEARNING = "speaking_learning"
    COACH_OS = "coach_os"
    ELITE = "elite"


class BillingStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class BillingEventType(str, Enum):
    ALACARTE_VIDEO = "alacarte_video"
    SUBSCRIPTION_PAYMENT = "subscription_payment"
    PAYMENT_FAILED = "payment_failed"


class BillingErrorCode(str, Enum):
    SUBSCRIPTION_INACTIVE = "SUBSCRIPTION_INACTIVE"
    TIER_CEILING_EXCEEDED = "TIER_CEILING_EXCEEDED"


TIER_MONTHLY_PRICE_CENTS: dict[str, int] = {
    "proof_layer": 0,
    "speaking_learning": 3999,
    "coach_os": 9999,
    "elite": 19999,
}

ALACARTE_VIDEO_PRICE_CENTS: int = 999

REDIS_KEY_STATUS = "coach:{coach_id}:status"
REDIS_KEY_TIER = "coach:{coach_id}:tier"


class BillingError(Exception):
    def __init__(self, code: str, message: str, redirect: str = "") -> None:
        self.code = code
        self.message = message
        self.redirect = redirect
        super().__init__(message)


class CoachSubscriptionRow(BaseModel):
    id: str = Field(...)
    coach_id: str = Field(...)
    stripe_customer_id: str = Field(...)
    stripe_subscription_id: str = Field(...)
    stripe_metered_item_id: str = Field(default="")
    tier: str = Field(default="proof_layer")
    monthly_base_price_cents: int = Field(default=0)
    alacarte_video_price_cents: int = Field(default=999)
    status: str = Field(default="active")
    payment_method_last4: str = Field(default="")
    current_period_start: str = Field(default="")
    current_period_end: str = Field(default="")
    total_monthly_cost_cents: int = Field(default=0)
    created_at: str = Field(default="")
    updated_at: str = Field(default="")


class BillingEventRow(BaseModel):
    id: str = Field(...)
    coach_id: str = Field(...)
    event_type: str = Field(...)
    stripe_event_id: str = Field(default="")
    amount_cents: int = Field(default=0)
    description: str = Field(default="")
    receipt_chain_block: str = Field(default="")
    created_at: str = Field(default="")


class WalletDisplayPayload(BaseModel):
    coach_id: str = Field(...)
    tier: str = Field(...)
    tier_display_name: str = Field(...)
    monthly_base_cents: int = Field(...)
    alacarte_video_count: int = Field(default=0)
    alacarte_video_total_cents: int = Field(default=0)
    total_monthly_cost_cents: int = Field(...)
    status: str = Field(...)
    payment_method_last4: str = Field(default="")
    current_period_end: str = Field(default="")
