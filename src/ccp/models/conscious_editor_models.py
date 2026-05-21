from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class EditorTier(str, Enum):
    artifact_review = "artifact_review"
    media_validation = "media_validation"


class RerenderScope(str, Enum):
    caption_text_patch = "caption_text_patch"
    composition_reflow = "composition_reflow"
    visual_slide_regeneration = "visual_slide_regeneration"
    cmf_full_regen_from_compiled_meaning = "cmf_full_regen_from_compiled_meaning"
    source_restart_required = "source_restart_required"


class EditorSessionStatus(str, Enum):
    pending_artifact = "pending_artifact"
    artifact_ready = "artifact_ready"
    provisional_warnings = "provisional_warnings"
    media_ready = "media_ready"
    rerender_in_progress = "rerender_in_progress"
    ready_for_approval = "ready_for_approval"
    approved = "approved"
    escalated = "escalated"
    blocked = "blocked"


class OperatorDecision(str, Enum):
    approve = "approve"
    edit_and_approve = "edit_and_approve"
    request_regeneration = "request_regeneration"
    escalate = "escalate"


class TranscriptSourceKind(str, Enum):
    raw_engine_output = "raw_engine_output"
    operator_revision = "operator_revision"


class LineageNodeType(str, Enum):
    source_audio = "source_audio"
    transcript = "transcript"
    semantic_artifact = "semantic_artifact"
    visual_composition_brief = "visual_composition_brief"
    canvas_composition = "canvas_composition"
    export_bundle = "export_bundle"


class TranscriptTokenPatch(BaseModel):
    token_index: int = Field(..., ge=0)
    original_text: str = Field(..., min_length=1)
    revised_text: str = Field(..., min_length=1)
    start_ms: int = Field(..., ge=0)
    end_ms: int = Field(..., ge=0)
    semantic_change_flag: bool = Field(default=False)


class TranscriptRevision(BaseModel):
    revision_id: str = Field(..., min_length=1)
    editor_session_id: str = Field(..., min_length=1)
    source_kind: TranscriptSourceKind = Field(...)
    author_person_id: str = Field(..., min_length=1)
    revision_note: str = Field(default="")
    revised_plaintext: str = Field(..., min_length=1)
    revised_json_payload: str = Field(..., min_length=2)
    token_patches: list[TranscriptTokenPatch] = Field(default_factory=list)
    requires_timing_reflow: bool = Field(default=False)
    created_at_utc: str = Field(..., min_length=1)


class ScopedRerenderDecision(BaseModel):
    decision_id: str = Field(..., min_length=1)
    editor_session_id: str = Field(..., min_length=1)
    revision_id: str = Field(..., min_length=1)
    scope: RerenderScope = Field(...)
    rationale: str = Field(..., min_length=1)
    affected_slide_indices: list[int] = Field(default_factory=list)
    requires_vcb_refresh: bool = Field(default=False)
    requires_audio_rerecord: bool = Field(default=False)
    requires_nim_rerun: bool = Field(default=False)
    created_at_utc: str = Field(..., min_length=1)


class EditorArtifactSummary(BaseModel):
    content_output_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    archetype_container: str = Field(..., min_length=1)
    content_piece_ids: list[str] = Field(default_factory=list)
    coalition_signature: str | None = Field(default=None)
    anti_centroid_warnings: list[str] = Field(default_factory=list)
    trigger_first_verified: bool = Field(default=True)


class MediaReviewSummary(BaseModel):
    vcb_id: str = Field(..., min_length=1)
    composition_id: str = Field(..., min_length=1)
    composition_status: str = Field(..., min_length=1)
    slide_count: int = Field(..., ge=1)
    transcript_revision_id: str | None = Field(default=None)
    editable_transcript_enabled: bool = Field(default=True)
    latest_scope: RerenderScope | None = Field(default=None)
    export_ready: bool = Field(default=False)


class LineageNode(BaseModel):
    node_id: str = Field(..., min_length=1)
    node_type: LineageNodeType = Field(...)
    referenced_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    parent_node_id: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)


class EditorLineageGraph(BaseModel):
    editor_session_id: str = Field(..., min_length=1)
    root_source_audio_asset_id: str = Field(..., min_length=1)
    nodes: list[LineageNode] = Field(default_factory=list)
    trigger_first_chain_verified: bool = Field(default=True)
    source_restart_required: bool = Field(default=False)


class ConsciousEditorSession(BaseModel):
    editor_session_id: str = Field(..., min_length=1)
    tier: EditorTier = Field(...)
    status: EditorSessionStatus = Field(...)
    coach_id: str = Field(..., min_length=1)
    source_audio_asset_id: str = Field(..., min_length=1)
    content_output_id: str | None = Field(default=None)
    vcb_id: str | None = Field(default=None)
    composition_id: str | None = Field(default=None)
    artifact_summary: EditorArtifactSummary | None = Field(default=None)
    media_summary: MediaReviewSummary | None = Field(default=None)
    lineage: EditorLineageGraph | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)
    updated_at_utc: str = Field(..., min_length=1)


class CreateTranscriptRevisionRequest(BaseModel):
    revised_plaintext: str = Field(..., min_length=1)
    revised_json_payload: str = Field(..., min_length=2)
    revision_note: str = Field(default="")
    token_patches: list[TranscriptTokenPatch] = Field(default_factory=list)


class CreateTranscriptRevisionResponse(BaseModel):
    revision: TranscriptRevision = Field(...)
    scope_decision: ScopedRerenderDecision = Field(...)


class ExecuteRerenderRequest(BaseModel):
    revision_id: str = Field(..., min_length=1)
    operator_override_scope: RerenderScope | None = Field(default=None)
    operator_reason: str = Field(default="")


class ExecuteRerenderResponse(BaseModel):
    decision: ScopedRerenderDecision = Field(...)
    resulting_status: EditorSessionStatus = Field(...)
    refreshed_media_summary: MediaReviewSummary | None = Field(default=None)


class OperatorDecisionRequest(BaseModel):
    decision: OperatorDecision = Field(...)
    decision_note: str = Field(default="")


class OperatorDecisionResponse(BaseModel):
    editor_session_id: str = Field(..., min_length=1)
    decision: OperatorDecision = Field(...)
    resulting_status: EditorSessionStatus = Field(...)
    receipt_event_id: str = Field(..., min_length=1)
