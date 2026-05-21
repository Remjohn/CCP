from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum

class CommercialLadderState(str, Enum):
    ACTIVE_FREE = "ACTIVE_FREE"
    BOUNDARY_REACHED = "BOUNDARY_REACHED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    UPGRADED_TIER_1 = "UPGRADED_TIER_1"

class StealthCourseBoundary(str, Enum):
    STRUCTURE_ADAPTIVE_LAYER = "STRUCTURE_ADAPTIVE_LAYER"
    ADVANCED_FR61_INSIGHTS = "ADVANCED_FR61_INSIGHTS"

class StealthCourseTransitionRequest(BaseModel):
    client_id: UUID
    coach_id: UUID
    journey_id: UUID
    current_node_id: UUID

class LockedContentPreview(BaseModel):
    content_id: UUID
    title: str = Field(..., description="Title of the locked Stealth Course node")
    topic_cluster: str
    difficulty_level: str
    blurred_thumbnail_url: str

class TelegramInvoicePayload(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    payload: str = Field(..., description="Internal tracking payload for the bot")
    provider_token: str = Field(..., description="Stripe token via Telegram API")
    currency: str = "USD"
    prices_json: str = Field(..., description="JSON serialized array of LabeledPrice")

    @field_validator('payload')
    def validate_no_external_urls(cls, v):
        if "http://" in v or "https://" in v:
            raise ValueError("CBAR Phase5-M05 Violation: External URLs are strictly banned. Must use native Telegram payment payload.")
        return v

class StealthCourseTransitionResponse(BaseModel):
    client_id: UUID
    journey_id: UUID
    governor_evaluation_id: UUID
    locked_preview: LockedContentPreview
    invoice_payload: TelegramInvoicePayload
    stealth_course_upgrade_token: str = Field(..., description="Token for frontend Mini App to invoke the pay startapp")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StealthCourseUpgradeReceipt(BaseModel):
    client_id: UUID
    previous_tier: str
    new_tier: str
    governor_evaluation_id: UUID
    stripe_invoice_id: str
    unlocked_content_id: UUID
    timestamp: datetime
