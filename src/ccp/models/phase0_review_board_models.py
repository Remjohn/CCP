"""
src/ccp/models/phase0_review_board_models.py
=============================================
Pydantic v2 model definitions for FR-ERA3-40 Phase-0 Batch Execution Review and Approval Board.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field


class Phase0ArtifactReviewSet(BaseModel):
    """Structured set of review artifacts for the run."""
    audit_pdf_artifact_id: Optional[str] = Field(default=None)
    audit_pdf_preview_path: Optional[str] = Field(default=None)
    audit_card_board_artifact_id: Optional[str] = Field(default=None)
    audit_card_board_preview_path: Optional[str] = Field(default=None)
    audit_explainer_video_artifact_id: Optional[str] = Field(default=None)
    audit_explainer_video_preview_path: Optional[str] = Field(default=None)
    explainer_video_1_artifact_id: Optional[str] = Field(default=None)
    explainer_video_1_preview_path: Optional[str] = Field(default=None)
    explainer_video_2_artifact_id: Optional[str] = Field(default=None)
    explainer_video_2_preview_path: Optional[str] = Field(default=None)
    cinematic_video_artifact_id: Optional[str] = Field(default=None)
    cinematic_video_preview_path: Optional[str] = Field(default=None)
    carousel_artifact_id: Optional[str] = Field(default=None)
    meme_artifact_id: Optional[str] = Field(default=None)
    preview_bundle_path: Optional[str] = Field(default=None)
    
    missing_required_artifacts: List[str] = Field(default_factory=list)
    failed_optional_artifacts: List[str] = Field(default_factory=list)
    auto_passed_artifacts: List[str] = Field(default_factory=list)
    human_review_required_artifacts: List[str] = Field(default_factory=list)


class Phase0ApprovalDecision(BaseModel):
    """Canonical decision object for review actions."""
    decision_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    artifact_set_id: str = Field(..., min_length=1)
    decision_type: Literal["approve", "reject", "rerun", "revise"]
    operator_id: str = Field(..., min_length=1)
    reason_code: str = Field(..., min_length=1)
    note: Optional[str] = Field(default=None)
    target_artifact_ids: List[str] = Field(default_factory=list)
    created_at: datetime


class Phase0RerunRequest(BaseModel):
    """Request object for rerunning all or part of a run while preserving provenance."""
    rerun_request_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    source_run_id: str = Field(..., min_length=1)
    source_artifact_set_id: str = Field(..., min_length=1)
    target_scope: Literal[
        "full_package",
        "audit_only",
        "audit_video_only",
        "explainer_1_only",
        "explainer_2_only",
        "cinematic_only",
        "optional_assets_only",
    ]
    requested_by: str = Field(..., min_length=1)
    reason_code: str = Field(..., min_length=1)
    note: Optional[str] = Field(default=None)
    created_at: datetime


class Phase0RevisionRequest(BaseModel):
    """Request object for manual or semi-manual correction without implying a pure rerender."""
    revision_request_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    artifact_set_id: str = Field(..., min_length=1)
    severity: Literal["minor", "major", "blocking"]
    issue_code: str = Field(..., min_length=1)
    note: str = Field(..., min_length=1)
    requested_by: str = Field(..., min_length=1)
    created_at: datetime


class Phase0ReleaseState(BaseModel):
    """Review-gated release state independent from commercial entitlement."""
    status: Literal[
        "blocked",
        "review_in_progress",
        "core_ready_optional_missing",
        "core_ready_optional_failed",
        "release_ready",
        "released",
    ]
    release_blockers: List[str] = Field(default_factory=list)
    approved_required_artifacts: List[str] = Field(default_factory=list)
    pending_required_artifacts: List[str] = Field(default_factory=list)
    released_at: Optional[datetime] = None


class Phase0PaymentReadyState(BaseModel):
    """Commercial-bridge readiness state for $29.99 unlock flow."""
    status: Literal[
        "not_ready",
        "review_ready_but_commercial_blocked",
        "payment_ready",
        "unlock_initiated",
        "unlock_confirmed",
    ]
    bridge_compatible: bool
    commercial_state_ref: Optional[str] = Field(default=None)
    blockers: List[str] = Field(default_factory=list)
    updated_at: datetime


class Phase0ReviewRow(BaseModel):
    """Primary review row representing one effective run for one coach/prospect packet."""
    coach_id: str = Field(..., min_length=1)
    prospect_packet_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    prior_run_id: Optional[str] = Field(default=None)
    artifact_set_id: str = Field(..., min_length=1)
    coach_display_name: str = Field(..., min_length=1)
    content_type_mix: List[str] = Field(default_factory=list)
    execution_status: str = Field(..., min_length=1)
    review_status: str = Field(..., min_length=1)
    blocking_reason_codes: List[str] = Field(default_factory=list)
    artifact_review_set: Phase0ArtifactReviewSet
    release_state: Phase0ReleaseState
    payment_ready_state: Phase0PaymentReadyState
    latest_decision: Optional[Phase0ApprovalDecision] = Field(default=None)
    compare_targets: List[str] = Field(default_factory=list)
    updated_at: datetime


class Phase0BatchExecutionBoard(BaseModel):
    """Top-level board payload representing a filtered set of reviewable runs."""
    board_id: str = Field(..., min_length=1)
    generated_at: datetime
    filter_state: Dict[str, Any] = Field(default_factory=dict)
    total_rows: int = Field(default=0, ge=0)
    ready_rows: int = Field(default=0, ge=0)
    blocked_rows: int = Field(default=0, ge=0)
    payment_ready_rows: int = Field(default=0, ge=0)
    release_ready_rows: int = Field(default=0, ge=0)
    rows: List[Phase0ReviewRow] = Field(default_factory=list)
