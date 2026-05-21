import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class AdminActionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REGENERATE = "regenerate"
    PAUSE_PIPELINE = "pause_pipeline"
    RESUME_PIPELINE = "resume_pipeline"
    RETRY_FAILED = "retry_failed"
    SEND_NUDGE = "send_nudge"
    SEND_PAYMENT_REMINDER = "send_payment_reminder"


class AdminAction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    admin_user_id: str
    action_type: AdminActionType
    target_coach_id: Optional[str] = None
    target_content_id: Optional[str] = None
    notes: Optional[str] = None
    receipt_chain_block: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PipelineHealthSnapshot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    snapshot_time: datetime = Field(default_factory=datetime.utcnow)
    active_renders: int = 0
    failed_24h: int = 0
    failed_by_type: dict[str, int] = Field(default_factory=dict)
    avg_render_time_seconds: float = 0.0
    gpu_utilization_pct: float = 0.0
    total_active_coaches: int = 0
    total_pending_review: int = 0
    total_cbcs_users_week: int = 0
    revenue_week_cents: int = 0
    aws_cost_week_cents: int = 0
    margin_pct: float = 0.0


class TenantContainerConfig(BaseModel):
    tenant_id: str
    coach_acronym: str
    container_name: str
    ip_address: str
    port: int
    api_token: str
    status: str = "running"
