"""
src/ccp/models/phase0_delivery_models.py
=========================================
Pydantic v2 model definitions and enums for FR-ERA3-36 Phase-0 Delivery Orchestrator.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field


class Phase0DeliveryRunStatus(str, Enum):
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    AWAITING_REVIEW = "AWAITING_REVIEW"
    DEGRADED_READY = "DEGRADED_READY"
    COMPLETED = "COMPLETED"
    PARTIAL_FAILURE = "PARTIAL_FAILURE"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class Phase0SequenceStepType(str, Enum):
    AUDIT_CORE = "AUDIT_CORE"
    CARD_RENDER = "CARD_RENDER"
    PDF_AUDIT_ASSEMBLY = "PDF_AUDIT_ASSEMBLY"
    AUDIT_EXPLAINER_VIDEO = "AUDIT_EXPLAINER_VIDEO"
    EXPLAINER_VIDEO = "EXPLAINER_VIDEO"
    CINEMATIC_VIDEO = "CINEMATIC_VIDEO"
    CAROUSEL_ASSET = "CAROUSEL_ASSET"
    MEME_ASSET = "MEME_ASSET"
    PREVIEW_ASSEMBLY = "PREVIEW_ASSEMBLY"
    PAYMENT_HANDOFF = "PAYMENT_HANDOFF"
    RELEASE_STEP = "RELEASE_STEP"


class Phase0ExecutionMode(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    OPERATOR_REVIEW_REQUIRED = "OPERATOR_REVIEW_REQUIRED"
    MANUAL_ONLY = "MANUAL_ONLY"


class Phase0SequenceStep(BaseModel):
    step_id: str = Field(..., min_length=1)
    step_key: str = Field(..., min_length=1)
    step_type: Phase0SequenceStepType
    order_index: int = Field(..., ge=0)
    execution_mode: Phase0ExecutionMode
    required: bool = Field(default=True)
    review_gate: bool = Field(default=False)
    depends_on_step_ids: List[str] = Field(default_factory=list)
    target_output_key: str = Field(..., min_length=1)


class Phase0DeliveryPlan(BaseModel):
    plan_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    package_variant: str = Field(..., min_length=1)
    requested_outputs: List[str] = Field(..., min_length=1)
    generation_order: List[Phase0SequenceStep] = Field(..., min_length=1)
    release_order: List[Phase0SequenceStep] = Field(..., min_length=1)
    review_required: bool = Field(default=True)
    optional_outputs_enabled: List[str] = Field(default_factory=list)
    sla_deadline_utc: datetime
    commercial_target: str = Field(default="phase0_proof_unlock", min_length=1)
    created_at_utc: datetime


class Phase0RenderRequest(BaseModel):
    render_request_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    delivery_run_id: str = Field(..., min_length=1)
    target_surface: str = Field(..., min_length=1)
    artifact_family: str = Field(..., min_length=1)
    source_payload_ids: List[str] = Field(..., min_length=1)
    template_key: Optional[str] = Field(default=None)
    priority: Literal["HIGH", "NORMAL", "LOW"] = "NORMAL"
    review_required: bool = Field(default=True)
    delivery_context: Dict[str, Any] = Field(default_factory=dict)


class Phase0SequenceStepResult(BaseModel):
    step_id: str = Field(..., min_length=1)
    status: Literal["PENDING", "RUNNING", "SUCCEEDED", "FAILED", "SKIPPED", "BLOCKED"]
    produced_artifact_ids: List[str] = Field(default_factory=list)
    failure_reason: Optional[str] = Field(default=None)
    degraded: bool = Field(default=False)
    started_at_utc: Optional[datetime] = None
    completed_at_utc: Optional[datetime] = None


class Phase0DeliveryReceipt(BaseModel):
    receipt_id: str = Field(..., min_length=1)
    delivery_run_id: str = Field(..., min_length=1)
    step_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    outcome: Literal["SUCCEEDED", "FAILED", "SKIPPED", "DEGRADED"]
    artifact_ids: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    started_at_utc: Optional[datetime] = None
    completed_at_utc: Optional[datetime] = None
    retryable: bool = Field(default=False)


class Phase0OutputBundle(BaseModel):
    output_bundle_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    audit_report_id: Optional[str] = Field(default=None)
    pdf_audit_payload_id: Optional[str] = Field(default=None)
    audit_explainer_video_payload_id: Optional[str] = Field(default=None)
    explainer_video_1_asset_id: Optional[str] = Field(default=None)
    explainer_video_2_asset_id: Optional[str] = Field(default=None)
    cinematic_video_asset_id: Optional[str] = Field(default=None)
    carousel_asset_ids: List[str] = Field(default_factory=list)
    meme_asset_ids: List[str] = Field(default_factory=list)
    score_card_board_ids: List[str] = Field(default_factory=list)
    preview_bundle_ids: List[str] = Field(default_factory=list)
    delivery_ready: bool = Field(default=False)
    release_blockers: List[str] = Field(default_factory=list)
    payment_handoff_ready: bool = Field(default=False)


class Phase0DeliveryRun(BaseModel):
    delivery_run_id: str = Field(..., min_length=1)
    plan_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: Optional[str] = Field(default=None)
    status: Phase0DeliveryRunStatus
    started_at_utc: Optional[datetime] = None
    completed_at_utc: Optional[datetime] = None
    current_step_id: Optional[str] = Field(default=None)
    step_results: List[Phase0SequenceStepResult] = Field(default_factory=list)
    output_bundle_id: Optional[str] = Field(default=None)
    review_state: str = Field(default="NOT_STARTED", min_length=1)
    failure_state: Optional[str] = Field(default=None)
    receipts: List[Phase0DeliveryReceipt] = Field(default_factory=list)


class Phase0PaymentHandoffPacket(BaseModel):
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    delivery_run_id: str = Field(..., min_length=1)
    output_bundle_id: str = Field(..., min_length=1)
    commercial_offer_key: str = Field(..., min_length=1)
    payment_ready: bool
    release_ready: bool
    upgrade_credit_eligible: bool = Field(default=True)
