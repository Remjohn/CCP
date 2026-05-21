"""
FR-ERA3-39 Phase-0 Campaign Frontend and Batch Intake Workspace Models
========================================================================
Canonical Pydantic v2 schemas for the Phase-0 campaign frontend and batch workspace.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional, List, Dict
from pydantic import BaseModel, Field


class Phase0CoachBinding(BaseModel):
    binding_id: str
    provisional_label: Optional[str] = None
    coach_id: str
    coach_acronym: Optional[str] = None
    binding_state: Literal["PROVISIONAL", "RESOLVED", "INVALID"]
    created_at_utc: datetime
    resolved_at_utc: Optional[datetime] = None


class Phase0ReadinessSummary(BaseModel):
    phase0_packet_id: Optional[str] = None
    ready: bool
    missing_required_fields: List[str] = Field(default_factory=list)
    attached_file_count: int = Field(ge=0)
    grouped_file_count: int = Field(ge=0)
    audit_target_count: int = Field(ge=0)
    audience_present: bool
    business_intelligence_present: bool
    last_checked_at_utc: datetime


class Phase0CoachRow(BaseModel):
    row_id: str
    display_name: str
    coach_binding: Phase0CoachBinding
    row_state: Literal[
        "DRAFT",
        "BOUND_UNREADY",
        "READY_TO_EXECUTE",
        "RUNNING",
        "REVIEW_REQUIRED",
        "DELIVERED_AWAITING_PAYMENT",
        "PAID_UNLOCKED",
        "UPGRADED",
        "FAILED",
    ]
    readiness: Phase0ReadinessSummary
    phase0_packet_id: Optional[str] = None
    delivery_run_id: Optional[str] = None
    payment_state_label: str = ""
    next_action: str
    updated_at_utc: datetime


class Phase0BatchUploadSession(BaseModel):
    batch_upload_session_id: str
    workspace_id: str
    initiated_by_operator_id: str
    attached_file_names: List[str] = Field(default_factory=list)
    target_row_ids: List[str] = Field(default_factory=list)
    total_file_count: int = Field(ge=0)
    completed_at_utc: Optional[datetime] = None
    created_at_utc: datetime


class Phase0BulkAttachmentResult(BaseModel):
    batch_upload_session_id: str
    attached_count: int = Field(ge=0)
    failed_count: int = Field(ge=0)
    row_attachment_counts: Dict[str, int] = Field(default_factory=dict)
    unresolved_files: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class Phase0ExecutionRequest(BaseModel):
    request_id: str
    workspace_id: str
    row_ids: List[str] = Field(min_length=1)
    phase0_packet_ids: List[str] = Field(min_length=1)
    triggered_by_operator_id: str
    execution_mode: Literal["SINGLE", "BATCH"]
    require_review_gate: bool = True
    created_at_utc: datetime


class Phase0WorkspaceFilterState(BaseModel):
    readiness_filter: Literal["ALL", "READY", "BLOCKED", "PARTIAL"] = "ALL"
    delivery_filter: Literal["ALL", "NOT_STARTED", "RUNNING", "REVIEW", "DELIVERED"] = "ALL"
    payment_filter: Literal["ALL", "UNPAID", "PAID", "UPGRADED"] = "ALL"
    search_query: str = ""
    sort_key: Literal["UPDATED", "READY_FIRST", "NAME", "PAYMENT_STATE"] = "UPDATED"


class Phase0CampaignWorkspace(BaseModel):
    workspace_id: str
    title: str
    operator_id: str
    rows: List[Phase0CoachRow] = Field(default_factory=list)
    filter_state: Phase0WorkspaceFilterState
    selected_row_ids: List[str] = Field(default_factory=list)
    active_batch_upload_session_id: Optional[str] = None
    generated_at_utc: datetime


class Phase0WorkspaceHealth(BaseModel):
    workspace_id: str
    intake_api_ready: bool
    delivery_api_ready: bool
    commercial_api_ready: bool
    receipt_chain_ready: bool
    shared_storage_ready: bool
    checked_at_utc: datetime
