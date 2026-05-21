"""
CA11 Quad-Platform Intelligence Layer Models
=============================================
Pydantic models, enums, and constants for Phase 4 CA11 specs (FR-CA11-01 through FR-CA11-15).
Models are appended in dependency order as each spec is built.

DEP-ID range: DEP-ENG-071 through DEP-ENG-086 (all PROPOSED until registered).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-01 — Coach Workspace Provisioning
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class WorkspaceSectionType(str, Enum):
    """The 8 mandatory root sections in the coach AFFiNE workspace.

    Spec §4 Stage 1 Step 1: 8 root pages required.
    PRD-Update-CA11 §4.1 FR-CA11-01: mirrors retired Notion dashboard (Parent PRD §9.8).
    """
    COMMAND_CENTER = "command_center"
    CONTENT_CALENDAR = "content_calendar"
    CLIENT_INTELLIGENCE_HUB = "client_intelligence_hub"
    CPSC_CAMPAIGN_CONSOLE = "cpsc_campaign_console"
    CRAL_EVIDENCE_VAULT = "cral_evidence_vault"
    GUARDIAN_AGENT_CONSOLE = "guardian_agent_console"
    VISUAL_PRODUCTION_CONSOLE = "visual_production_console"
    PROGRAM_CONTENT_LIBRARY = "program_content_library"


class WorkspaceProvisioningError(str, Enum):
    """Error types for workspace provisioning pipeline."""
    TEMPLATE_VALIDATION_FAILED = "TEMPLATE_VALIDATION_FAILED"
    TEMPLATE_MISSING_SECTIONS = "TEMPLATE_MISSING_SECTIONS"
    THEME_EXTRACTION_FAILED = "THEME_EXTRACTION_FAILED"
    THEME_MISSING_BRAND_TOKENS = "THEME_MISSING_BRAND_TOKENS"
    AFFINE_API_UNREACHABLE = "AFFINE_API_UNREACHABLE"
    WORKSPACE_CREATION_FAILED = "WORKSPACE_CREATION_FAILED"
    SUPABASE_REGISTRATION_FAILED = "SUPABASE_REGISTRATION_FAILED"
    FALLBACK_TO_NOTION = "FALLBACK_TO_NOTION"


class ProvisioningStatus(str, Enum):
    """Status of a workspace provisioning operation."""
    SUCCESS = "SUCCESS"
    FAILED_FALLBACK_NOTION = "FAILED_FALLBACK_NOTION"
    FAILED_NO_FALLBACK = "FAILED_NO_FALLBACK"
    PENDING_RETRY = "PENDING_RETRY"


# ── Constants ──────────────────────────────────────────────────────────

# Exactly 8 sections required (§4 Stage 1, AC1)
REQUIRED_SECTION_COUNT: int = 8

# All required section IDs (used for template validation)
REQUIRED_SECTIONS: frozenset[str] = frozenset(s.value for s in WorkspaceSectionType)

# Default CCP theme fallback (§4 Stage 2 Failure Condition)
DEFAULT_CCP_PRIMARY: str = "#1A1A2E"
DEFAULT_CCP_ACCENT: str = "#E94560"
DEFAULT_CCP_FONT: str = "Inter"

# Template version (§5 schema)
TEMPLATE_VERSION: str = "1.0.0"


# ── Models ─────────────────────────────────────────────────────────────


class ThemeTokens(BaseModel):
    """Brand tokens extracted from coach_soul.json and DEP-ENG-050.

    Spec §4 Stage 2: Theme Token Extraction outputs.
    """
    primary_color: str = Field(
        ...,
        description="CSS hex color from dominant Mood State affinity → --ccp-primary",
    )
    accent_color: str = Field(
        ...,
        description="CSS hex color from secondary Mood State → --ccp-accent",
    )
    business_name: str = Field(
        ...,
        description="Coach's business name from DEP-ENG-050 → workspace title",
    )
    tagline: str = Field(
        default="",
        description="Coach's tagline from DEP-ENG-050 → workspace subtitle",
    )
    logo_url: str = Field(
        default="",
        description="Logo URL from DEP-ENG-050 → --ccp-logo-url",
    )
    font_preference: str = Field(
        default=DEFAULT_CCP_FONT,
        description="Font preference from coach config → --ccp-font",
    )


class WorkspaceSectionSchema(BaseModel):
    """Schema definition for a single workspace section in the master template.

    Each section has a type, a title, and a list of expected database columns.
    """
    section_type: WorkspaceSectionType = Field(...)
    title: str = Field(...)
    database_columns: list[str] = Field(
        default_factory=list,
        description="Expected database column names for this section (if database view)",
    )


class MasterTemplateValidationResult(BaseModel):
    """Result of master template validation (Gate TEMPLATE-VALID).

    Spec §4 Stage 1 Failure Condition: Template does not contain all 8 required sections.
    """
    is_valid: bool = Field(...)
    sections_found: list[str] = Field(default_factory=list)
    sections_missing: list[str] = Field(default_factory=list)
    total_sections: int = Field(default=0)
    template_version: str = Field(default="")
    validation_errors: list[str] = Field(default_factory=list)


class ReceiptChainGuardRef(BaseModel):
    """Receipt Chain Guard schema reference per FR47 DEP-ENG-041.

    CA11 Revision (Global Fix): All receipt chain entries use cryptographic
    hash schema, not string literals.
    """
    schema_ref: str = Field(
        default="DEP-ENG-041",
        description="Reference to the Receipt Chain Guard schema",
    )


class WorkspaceProvisioningPayload(BaseModel):
    """Primary output schema — DEP-ENG-071 PROPOSED.

    Spec §5: Coach Workspace Provisioning Payload.
    CA11 Revision Fix 1: DEP-ID assigned as DEP-ENG-071 PROPOSED.
    CA11 Revision Fix 2: receipt_chain_guard uses schema_ref not string literal.
    """
    transaction_timestamp: str = Field(
        ...,
        description="ISO 8601 UTC timestamp of provisioning",
    )
    coach_id: str = Field(
        ...,
        description="UUID of the coach",
    )
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=5,
        description="Coach's acronym identifier",
    )
    workspace_id: str = Field(
        ...,
        description="AFFiNE workspace UUID",
    )
    workspace_url: str = Field(
        ...,
        description="Full URL to the coach's AFFiNE workspace",
    )
    theme_file: str = Field(
        ...,
        description="Filename of the generated CSS theme file",
    )
    template_version: str = Field(
        default=TEMPLATE_VERSION,
        description="Version of the master workspace template used",
    )
    sections_provisioned: list[str] = Field(
        ...,
        min_length=REQUIRED_SECTION_COUNT,
        max_length=REQUIRED_SECTION_COUNT,
        description="List of all 8 provisioned section IDs",
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
        description="Receipt Chain Guard schema reference (DEP-ENG-041)",
    )


class ProvisioningResult(BaseModel):
    """Full result of a workspace provisioning operation.

    Includes status, payload (if successful), error details, and fallback info.
    """
    status: ProvisioningStatus = Field(...)
    payload: Optional[WorkspaceProvisioningPayload] = Field(default=None)
    error: Optional[WorkspaceProvisioningError] = Field(default=None)
    error_detail: str = Field(default="")
    fallback_active: bool = Field(
        default=False,
        description="True if Notion fallback was activated",
    )
    notion_dashboard_id: Optional[str] = Field(
        default=None,
        description="Notion page ID if fallback was used",
    )


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-02 — AFFiNE Sync Service
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class DeliveryTarget(str, Enum):
    """Feature flag for per-coach delivery routing (§6 Backward Compatibility).

    Stored in coach_config.delivery_target. Controls whether content
    is pushed to AFFiNE, Notion, or both during migration.
    """
    AFFINE_ONLY = "AFFINE_ONLY"
    NOTION_ONLY = "NOTION_ONLY"
    BOTH = "BOTH"


class SyncEventType(str, Enum):
    """Types of sync events recorded in affine_sync_events table."""
    CONTENT_PUSH = "CONTENT_PUSH"
    TELEMETRY_PUSH = "TELEMETRY_PUSH"
    SESSION_PUSH = "SESSION_PUSH"
    LEARNING_PATH_PUSH = "LEARNING_PATH_PUSH"
    CANVA_APPROVE = "CANVA_APPROVE"


class SyncEventStatus(str, Enum):
    """Status of a sync event."""
    SUCCESS = "SUCCESS"
    RETRY = "RETRY"
    FAILED = "FAILED"


class SyncErrorType(str, Enum):
    """Error types for sync operations."""
    AFFINE_API_UNREACHABLE = "AFFINE_API_UNREACHABLE"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    PAYLOAD_VALIDATION_FAILED = "PAYLOAD_VALIDATION_FAILED"
    COACH_WORKSPACE_MISMATCH = "COACH_WORKSPACE_MISMATCH"
    MAX_RETRIES_EXCEEDED = "MAX_RETRIES_EXCEEDED"
    NOTION_FALLBACK_FAILED = "NOTION_FALLBACK_FAILED"


# ── Constants ──────────────────────────────────────────────────────────

# Retry configuration (§4 Stage 2 Failure Condition)
SYNC_MAX_RETRIES: int = 5
SYNC_BACKOFF_SCHEDULE: tuple[float, ...] = (5.0, 10.0, 20.0, 40.0, 80.0)

# Default delivery target during migration
DEFAULT_DELIVERY_TARGET: DeliveryTarget = DeliveryTarget.BOTH

# Service metadata
SYNC_SERVICE_VERSION: str = "1.0.0"


# ── Models ─────────────────────────────────────────────────────────────


class VisualAssetRef(BaseModel):
    """A single visual asset within a content push payload."""
    slide_number: int = Field(..., ge=1, description="Slide number in the carousel")
    image_url: str = Field(..., description="R2 storage URL for the image")
    agss_score: float = Field(..., ge=0.0, le=10.0, description="AGSS quality score")
    tiar_nouns: list[str] = Field(
        default_factory=list,
        description="TIAR identity nouns used in the visual",
    )


class ContentPayloadBody(BaseModel):
    """Content body within a content push payload."""
    script_markdown: str = Field(..., description="Compiled script in Markdown format")
    posting_notes: str = Field(default="", description="Posting time and hashtag guidance")
    why_this_post: str = Field(
        default="",
        description="Voice DNA rationale — why this post was created",
    )
    leadership_farming: str = Field(
        default="",
        description="Leadership Farming dimension exercised and score",
    )


class ContentPushPayload(BaseModel):
    """Primary output schema — DEP-ENG-072 PROPOSED.

    Spec §5: Content Push Payload for AFFiNE sync.
    CA11 Revision Fix 1: DEP-ID assigned as DEP-ENG-072 PROPOSED.
    CA11 Revision Fix 2: receipt_chain_guard uses schema_ref not string literal.
    """
    asset_id: str = Field(
        ...,
        description="Universal Asset ID (DEP-ENG-040) — idempotency key",
    )
    coach_id: str = Field(..., description="UUID of the coach")
    fingerprint_id: str = Field(
        ...,
        description="Fingerprint Archive Index ID (DEP-ENG-020)",
    )
    content: ContentPayloadBody = Field(...)
    visual_assets: list[VisualAssetRef] = Field(default_factory=list)
    voice_note_url: str = Field(
        default="",
        description="R2 URL for the source voice note",
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
        description="Receipt Chain Guard schema reference (DEP-ENG-041)",
    )


class TelemetryPushPayload(BaseModel):
    """Payload for pushing CBCS aggregated telemetry to Client Intelligence Hub."""
    coach_id: str = Field(..., description="UUID of the coach")
    period: str = Field(..., description="Reporting period (e.g. '2026-W13')")
    spt_distribution: dict[str, int] = Field(
        default_factory=dict,
        description="SPT stage distribution counts",
    )
    tribe_ict_breakdown: dict[str, float] = Field(
        default_factory=dict,
        description="Tribe-level ICT breakdown",
    )
    avg_intimacy_index: float = Field(
        default=0.0,
        ge=0.0,
        le=10.0,
        description="Average Intimacy Index across clients",
    )
    engagement_heatmap: dict[str, Any] = Field(
        default_factory=dict,
        description="Engagement heatmap data for visualization",
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
    )


class SessionPushPayload(BaseModel):
    """Payload for pushing session intelligence reports to Session Archive."""
    coach_id: str = Field(..., description="UUID of the coach")
    session_id: str = Field(..., description="Unique session identifier")
    session_date: str = Field(..., description="ISO 8601 date of the session")
    client_id: str = Field(default="", description="Client person ID")
    session_summary: str = Field(default="", description="AI-generated session summary")
    key_insights: list[str] = Field(default_factory=list, description="Key session insights")
    action_items: list[str] = Field(default_factory=list, description="Action items")
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
    )


class LearningPathPushPayload(BaseModel):
    """Payload for pushing categorized content to Program Content Library."""
    coach_id: str = Field(..., description="UUID of the coach")
    content_category: str = Field(..., description="Content category/module")
    content_items: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of categorized content items",
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
    )


class CanvaApprovePayload(BaseModel):
    """Payload for CVE Canva App approval webhook."""
    coach_id: str = Field(..., description="UUID of the coach")
    design_id: str = Field(..., description="Canva design ID")
    asset_id: str = Field(..., description="Universal Asset ID of the approved design")
    approval_status: str = Field(default="approved", description="Approval status")
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
    )


class SyncEvent(BaseModel):
    """An event record in the affine_sync_events Supabase table (§4, Task 3).

    Every sync operation writes one of these for audit trail.
    """
    event_id: str = Field(..., description="UUID of the event")
    event_type: SyncEventType = Field(...)
    target_workspace_id: str = Field(..., description="AFFiNE workspace UUID")
    payload_hash: str = Field(..., description="SHA-256 hash of the payload")
    status: SyncEventStatus = Field(...)
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
    receipt_chain_id: str = Field(
        default="",
        description="Receipt Chain entry ID linking to DEP-ENG-041",
    )
    error_detail: str = Field(default="", description="Error details if failed/retry")
    retry_count: int = Field(default=0, ge=0, description="Number of retries attempted")


class SyncResult(BaseModel):
    """Result of a sync push operation."""
    success: bool = Field(...)
    event: SyncEvent = Field(...)
    was_update: bool = Field(
        default=False,
        description="True if this was an idempotent update (not new creation)",
    )
    error_type: Optional[SyncErrorType] = Field(default=None)
    delivery_targets_completed: list[str] = Field(
        default_factory=list,
        description="Which targets were delivered to (e.g. ['AFFINE', 'NOTION'])",
    )


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-03 — Client Workspace Provisioning (Gated Learning Environment)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class ContentPermission(str, Enum):
    """Permission level for content blocks in client workspace."""
    READ_ONLY = "READ_ONLY"
    READ_WRITE = "READ_WRITE"


class ClientWorkspaceSection(str, Enum):
    """The 4 root sections in a client AFFiNE workspace (§4 Stage 1)."""
    DASHBOARD = "dashboard"
    LEARNING_LIBRARY = "learning_library"
    JOURNAL = "journal"
    RESOURCES = "resources"


class ClientProvisioningStatus(str, Enum):
    """Status of a client workspace provisioning operation."""
    SUCCESS = "SUCCESS"
    QUEUED = "QUEUED"
    FAILED_TELEGRAM_ONLY = "FAILED_TELEGRAM_ONLY"


# ── Constants ──────────────────────────────────────────────────────────

CLIENT_WORKSPACE_SECTIONS_COUNT: int = 4

CLIENT_REQUIRED_SECTIONS: frozenset[str] = frozenset(
    s.value for s in ClientWorkspaceSection
)

# Sections with read-write permission (§4 Stage 1 Step 1)
CLIENT_READWRITE_SECTIONS: frozenset[str] = frozenset({"journal"})

# All other sections are read-only for CCP-managed content
CLIENT_READONLY_SECTIONS: frozenset[str] = CLIENT_REQUIRED_SECTIONS - CLIENT_READWRITE_SECTIONS


# ── Models ─────────────────────────────────────────────────────────────


class UnlockCondition(BaseModel):
    """Gating condition for a content block.

    Content is provisioned (made to exist) only when both coping_position
    and atlas_week thresholds are met. §4 Stage 3: Gating by Absence.
    """
    min_coping_position: int = Field(
        ...,
        ge=0,
        description="Minimum coping_trajectory position to unlock",
    )
    min_atlas_week: int = Field(
        ...,
        ge=0,
        description="Minimum atlas_roadmap week to unlock",
    )


class ContentBlock(BaseModel):
    """A single content block in the client's Learning Library.

    Blocks that are not yet unlocked do NOT exist in the workspace
    (not hidden — absent). Provisioned by Noémie when unlock_condition is met.
    """
    block_id: str = Field(..., description="Unique block identifier")
    title: str = Field(..., description="Display title")
    content_type: str = Field(
        ...,
        description="Type: video, article, worksheet, excalidraw, exercise",
    )
    program_tag: str = Field(..., description="Program module/tag this belongs to")
    unlock_condition: UnlockCondition = Field(...)
    permission: ContentPermission = Field(default=ContentPermission.READ_ONLY)


class GatingSnapshot(BaseModel):
    """Snapshot of a client's gating state at provisioning time.

    Captures coping_position, atlas_week, and capacity_track for audit.
    """
    coping_position: int = Field(default=0, ge=0)
    atlas_week: int = Field(default=0, ge=0)
    capacity_track: str = Field(default="Foundation")


class ClientWorkspaceProvisioningPayload(BaseModel):
    """Primary output schema — DEP-ENG-073 PROPOSED.

    Spec §5: Client Workspace Provisioning Payload.
    CA11 Revision Fix 1: DEP-ID assigned as DEP-ENG-073 PROPOSED.
    CA11 Revision Fix 2: receipt_chain_guard uses schema_ref not string literal.
    """
    client_id: str = Field(..., description="UUID of the client")
    coach_id: str = Field(..., description="UUID of the coach")
    program_id: str = Field(..., description="Coaching program identifier")
    workspace_id: str = Field(..., description="AFFiNE workspace UUID for client")
    workspace_url: str = Field(..., description="Full URL to client's workspace")
    theme_inherited_from: str = Field(
        ...,
        description="CSS theme filename inherited from coach (FR-CA11-01)",
    )
    sections_provisioned: list[str] = Field(
        ...,
        description="Root sections created in the workspace",
    )
    learning_library_blocks_unlocked: int = Field(
        default=0,
        ge=0,
        description="Number of content blocks unlocked at provision time",
    )
    learning_library_blocks_total: int = Field(
        default=0,
        ge=0,
        description="Total content blocks in the program template",
    )
    gating_snapshot: GatingSnapshot = Field(
        default_factory=GatingSnapshot,
        description="Client's gating state at provision time",
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
        description="Receipt Chain Guard schema reference (DEP-ENG-041)",
    )


class ClientProvisioningResult(BaseModel):
    """Full result of a client workspace provisioning operation."""
    status: ClientProvisioningStatus = Field(...)
    payload: Optional[ClientWorkspaceProvisioningPayload] = Field(default=None)
    error_detail: str = Field(default="")
    telegram_fallback_active: bool = Field(
        default=False,
        description="True if workspace failed and client is on Telegram-only",
    )


class ContentUnlockResult(BaseModel):
    """Result of a content unlock operation by Noémie."""
    client_id: str = Field(...)
    blocks_unlocked: list[str] = Field(
        default_factory=list,
        description="Block IDs newly unlocked",
    )
    blocks_already_provisioned: list[str] = Field(
        default_factory=list,
        description="Block IDs that were already in the workspace",
    )
    new_gating_snapshot: GatingSnapshot = Field(...)
    telegram_notified: bool = Field(default=False)

# ══════════════════════════════════════════════════════════════════════════════
# FR-CA11-04 — Continuous Learning Path Builder (DEP-ENG-074)
# Agent: Gabrielle (Learning Path Agent, Strategy Department)
# ══════════════════════════════════════════════════════════════════════════════


class LearningContentType(str, Enum):
    """Content types for learning path registry.

    CA11 Revision Decision 2: expanded with 'course_chapter'.
    Consumed by FR-CA11-06 (Voice Note → Course Material)
    and FR-CA11-07 (Session-to-Course Pipeline).
    """
    SCRIPT = "script"
    VIDEO = "video"
    VOICE_LESSON = "voice_lesson"
    WEBINAR = "webinar"
    SESSION_RECAP = "session_recap"
    DIAGRAM = "diagram"
    COURSE_VIDEO = "course_video"
    COURSE_CHAPTER = "course_chapter"


class DifficultyLevel(str, Enum):
    """Difficulty level mapped from Audience Maturity Lifecycle (FR20).

    new = surface-level awareness content
    developing = intermediate depth
    loyal = deep transformation content
    """
    NEW = "new"
    DEVELOPING = "developing"
    LOYAL = "loyal"


class LearningPathEntry(BaseModel):
    """DEP-ENG-074 PROPOSED — Learning Path Registry entry.

    Created by Gabrielle when any CCP pipeline produces content.
    Stored in learning_path_registry Supabase table.
    """
    content_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="UUID primary key for this registry entry",
    )
    asset_id: str = Field(
        ...,
        description="Universal Asset ID (DEP-ENG-040)",
    )
    fingerprint_id: str = Field(
        ...,
        description="Skill Fingerprint ID (DEP-ENG-020) for traceability",
    )
    coach_id: str = Field(...)
    content_type: LearningContentType = Field(...)
    topic_cluster: str = Field(
        ...,
        description="Mapped from Context Premise Map dimensions (DEP-ENG-006)",
    )
    difficulty_level: DifficultyLevel = Field(...)
    program_tag: Optional[str] = Field(
        default=None,
        description="Coach's program identifier (nullable)",
    )
    journey_id: Optional[str] = Field(
        default=None,
        description="UUID of the learning journey this belongs to",
    )
    sequence_position: Optional[int] = Field(
        default=None,
        ge=0,
        description="Position within the journey DAG",
    )
    unlock_condition: Optional[UnlockCondition] = Field(
        default=None,
        description="Gating rules consumed by Noémie (FR-CA11-03)",
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
        description="Receipt Chain Guard schema reference (DEP-ENG-041)",
    )


class JourneyNode(BaseModel):
    """A node in a learning journey DAG (stored in Neo4j)."""
    content_id: str = Field(...)
    asset_id: str = Field(...)
    title: str = Field(...)
    content_type: LearningContentType = Field(...)
    difficulty_level: DifficultyLevel = Field(...)
    topic_cluster: str = Field(...)
    sequence_position: int = Field(ge=0)
    completed: bool = Field(default=False)


class JourneyEdge(BaseModel):
    """Prerequisite edge in a learning journey DAG."""
    from_content_id: str = Field(
        ..., description="Prerequisite content ID"
    )
    to_content_id: str = Field(
        ..., description="Dependent content ID"
    )
    edge_type: str = Field(
        default="prerequisite",
        description="Edge relationship type",
    )


class LearningProgressEntry(BaseModel):
    """Client completion tracking for learning content."""
    client_id: str = Field(...)
    content_id: str = Field(...)
    journey_id: str = Field(...)
    completed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


class NextContentRecommendation(BaseModel):
    """Recommended next content piece for a client."""
    content_id: str = Field(...)
    asset_id: str = Field(...)
    title: str = Field(...)
    content_type: LearningContentType = Field(...)
    topic_cluster: str = Field(...)
    difficulty_level: DifficultyLevel = Field(...)
    reason: str = Field(
        default="next_in_sequence",
        description="Why this content is recommended",
    )
    preview_text: Optional[str] = Field(default=None)


# FR-CA11-04 Constants
LEARNING_CONTENT_TYPES: frozenset[str] = frozenset(
    ct.value for ct in LearningContentType
)

DIFFICULTY_LEVELS: frozenset[str] = frozenset(
    dl.value for dl in DifficultyLevel
)

# Difficulty ordering for journey construction (new → developing → loyal)
DIFFICULTY_ORDER: dict[DifficultyLevel, int] = {
    DifficultyLevel.NEW: 0,
    DifficultyLevel.DEVELOPING: 1,
    DifficultyLevel.LOYAL: 2,
}


# ══════════════════════════════════════════════════════════════════════════════
# FR-CA11-05 — AI Session Recap Generator (DEP-ENG-075)
# Agent: Lena (Session Intelligence Analyst, Perception Department)
# ══════════════════════════════════════════════════════════════════════════════


class MoodState(str, Enum):
    """Emotional mood states for session emotional beats."""
    PROCESSING = "Processing"
    ESCAPE = "Escape"
    DISCOVERY = "Discovery"
    STATUS = "Status"


class DarnCatCategory(str, Enum):
    """DARN-CAT motivational interviewing categories for change talk."""
    DESIRE = "Desire"
    ABILITY = "Ability"
    REASON = "Reason"
    NEED = "Need"
    COMMITMENT = "Commitment"
    ACTIVATION = "Activation"
    TAKING_STEPS = "Taking Steps"


class KeyInsight(BaseModel):
    """A key coaching moment extracted from session transcript."""
    timestamp: str = Field(
        ..., description="Transcript timestamp (HH:MM:SS)",
    )
    coach_statement: str = Field(...)
    client_response: str = Field(...)
    psychological_significance: str = Field(...)


class ActionItem(BaseModel):
    """Implementation Intention (Gollwitzer) formatted action item."""
    implementation_intention: str = Field(
        ..., description="When [X], I will [Y] format",
    )
    context_premise_dimension: str = Field(
        default="general",
        description="Context Premise Map dimension this relates to",
    )
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.NEW)


class EmotionalBeat(BaseModel):
    """Emotional intensity data point in a session timeline."""
    timestamp: str = Field(
        ..., description="Transcript timestamp",
    )
    intensity: float = Field(
        ..., ge=0.0, le=1.0,
        description="Emotional intensity (0.0 to 1.0)",
    )
    mood_state: MoodState = Field(...)


class BreakthroughMoment(BaseModel):
    """DARN-CAT change talk marker detected in session."""
    timestamp: str = Field(...)
    darn_cat_category: DarnCatCategory = Field(...)
    raw_text: str = Field(...)


class SessionIntelligenceReport(BaseModel):
    """DEP-ENG-075 PROPOSED — Session Intelligence Report.

    Generated by Lena (Session Intelligence Analyst) from
    OBS session recording transcription via Whisper STT.
    """
    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="UUID for this session",
    )
    coach_id: str = Field(...)
    client_id: str = Field(...)
    recording_url: str = Field(
        ..., description="S3 URL for the recording",
    )
    transcript_url: str = Field(
        ..., description="S3 URL for the timestamped transcript",
    )
    key_insights: list[KeyInsight] = Field(
        default_factory=list,
        description="3-7 key coaching moments",
    )
    action_items: list[ActionItem] = Field(
        default_factory=list,
        description="2-5 concrete takeaways for the client",
    )
    emotional_beats: list[EmotionalBeat] = Field(
        default_factory=list,
        description="Emotional intensity timeline",
    )
    topic_clusters: list[str] = Field(
        default_factory=list,
        description="Thematic categories mapped to Context Premise dimensions",
    )
    breakthrough_moments: list[BreakthroughMoment] = Field(
        default_factory=list,
        description="DARN-CAT change talk markers",
    )
    mind_map_url: Optional[str] = Field(
        default=None,
        description="S3 URL for .excalidraw mind map JSON",
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
        description="Receipt Chain Guard schema reference (DEP-ENG-041)",
    )


class MindMapNode(BaseModel):
    """Node in a session mind map (Excalidraw structure)."""
    node_id: str = Field(...)
    label: str = Field(...)
    node_type: str = Field(
        default="topic",
        description="central | topic | insight",
    )
    x: float = Field(default=0.0)
    y: float = Field(default=0.0)
    color: Optional[str] = Field(default=None)


class MindMapEdge(BaseModel):
    """Edge in a session mind map."""
    from_id: str = Field(...)
    to_id: str = Field(...)


class SessionMindMap(BaseModel):
    """Session Mind Map structure for Excalidraw rendering."""
    session_id: str = Field(...)
    nodes: list[MindMapNode] = Field(default_factory=list)
    edges: list[MindMapEdge] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# FR-CA11-06 — Voice Note → Course Material Pipeline (DEP-ENG-076)
# ---------------------------------------------------------------------------

class PracticalExercise(BaseModel):
    """Implementation Intention formatted exercise (FR-CBCS-09)."""
    implementation_intention: str = Field(..., min_length=1)
    duration: str = Field(..., min_length=1)


class ConceptDiagramNode(BaseModel):
    """Node in a hierarchical concept diagram."""
    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    label: str = Field(..., min_length=1)
    level: int = Field(..., ge=0)
    parent_id: Optional[str] = None


class ConceptDiagramEdge(BaseModel):
    """Edge in a concept diagram (parent → child)."""
    from_id: str = Field(...)
    to_id: str = Field(...)


class LearningPathRegistryRef(BaseModel):
    """Learning path tagging metadata for a lesson."""
    topic_cluster: str = Field(..., min_length=1)
    difficulty_level: str = Field(...)
    content_type: str = Field(default="voice_lesson")


class VoiceNoteLessonPayload(BaseModel):
    """DEP-ENG-076 — Structured lesson output from voice note pipeline."""
    lesson_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    key_takeaways: list[str] = Field(..., min_length=1)
    detailed_explanation_markdown: str = Field(..., min_length=1)
    practical_exercise: PracticalExercise = Field(...)
    concept_diagram_url: Optional[str] = None
    learning_path_registry: LearningPathRegistryRef = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LessonResult(BaseModel):
    """Result of voice-to-lesson pipeline execution."""
    success: bool = Field(...)
    lesson: Optional[VoiceNoteLessonPayload] = None
    affine_page_id: Optional[str] = None
    diagram_generated: bool = Field(default=False)
    learning_path_tagged: bool = Field(default=False)
    fallback_used: bool = Field(default=False)
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# FR-CA11-07 — Session-to-Course Auto Pipeline (DEP-ENG-077)
# ---------------------------------------------------------------------------

class CourseChapter(BaseModel):
    """Single chapter within an auto-assembled course."""
    chapter_number: int = Field(..., ge=1)
    session_id: str = Field(...)
    title: str = Field(..., min_length=1)
    key_timestamps: list[str] = Field(default_factory=list)
    key_insight: str = Field(..., min_length=1)
    action_item: str = Field(..., min_length=1)


class DripSchedule(BaseModel):
    """Delivery schedule tied to Atlas roadmap active days."""
    client_id: str = Field(...)
    chapter_delivery_dates: list[str] = Field(default_factory=list)
    delivery_time: str = Field(default="09:00")
    timezone: str = Field(default="Europe/Paris")


class CourseDefinition(BaseModel):
    """DEP-ENG-077 — Auto-assembled course from session intelligence reports."""
    course_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    topic_clusters: list[str] = Field(..., min_length=1)
    chapters: list[CourseChapter] = Field(default_factory=list)
    total_chapters: int = Field(default=0)
    drip_schedule: Optional[DripSchedule] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DripDeliveryResult(BaseModel):
    """Result of a single drip delivery attempt."""
    chapter_number: int = Field(...)
    telegram_sent: bool = Field(default=False)
    affine_pushed: bool = Field(default=False)
    page_id: Optional[str] = None
    error: Optional[str] = None


class CourseAssemblyResult(BaseModel):
    """Result of the course assembly pipeline."""
    success: bool = Field(...)
    course: Optional[CourseDefinition] = None
    courses_created: int = Field(default=0)
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# FR-CA11-08 — Live Coaching → Content Machine Pipeline (DEP-ENG-078)
# ---------------------------------------------------------------------------

class SessionContentType(str, Enum):
    """Content types extractable from coaching sessions."""
    telegram_insight_card = "telegram_insight_card"
    instagram_caption = "instagram_caption"
    short_form_video_script = "short_form_video_script"


class ValidationStatus(str, Enum):
    """Triple-Pass Validation Gate status."""
    pending = "PENDING"
    passed = "PASSED"
    failed = "FAILED"


class QueueStatus(str, Enum):
    """Routing destination for session-derived content."""
    batch_included = "batch_included"
    session_content_queue = "session_content_queue"


class SessionContentPiece(BaseModel):
    """Single micro-content piece extracted from a coaching session."""
    asset_id: str = Field(..., min_length=1)
    content_type: SessionContentType = Field(...)
    text: str = Field(..., min_length=1)
    source_insight_timestamp: Optional[str] = None
    validation_status: ValidationStatus = Field(default=ValidationStatus.pending)
    fingerprint_id: Optional[str] = None
    source_type: str = Field(default="SESSION")
    batch_included: bool = Field(default=False)
    queue_status: QueueStatus = Field(default=QueueStatus.session_content_queue)


class ContentMachineArray(BaseModel):
    """DEP-ENG-078 — Content Machine output from session intelligence."""
    session_id: str = Field(...)
    content_pieces: list[SessionContentPiece] = Field(default_factory=list)
    total_extracted: int = Field(default=0)
    batch_included_count: int = Field(default=0)
    queued_count: int = Field(default=0)


class ContentMachineResult(BaseModel):
    """Result of the Content Machine Pipeline execution."""
    success: bool = Field(...)
    output: Optional[ContentMachineArray] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# FR-CA11-09 — Accountability Check-in Visualization (DEP-ENG-079)
# ---------------------------------------------------------------------------

class MoodTrajectory(str, Enum):
    """Weekly mood trend direction."""
    ascending = "ascending"
    descending = "descending"
    stable = "stable"


class DailyDataPoint(BaseModel):
    """Single day's accountability check-in data."""
    client_id: str = Field(...)
    date: str = Field(...)
    energy_rating: int = Field(..., ge=1, le=10)
    habits_completed: list[str] = Field(default_factory=list)
    habits_missed: list[str] = Field(default_factory=list)
    mood_state: str = Field(default="Processing")
    streak_count: int = Field(default=0, ge=0)


class MilestoneBadge(str, Enum):
    """Streak milestone badges."""
    day_7 = "7_day"
    day_14 = "14_day"
    day_21 = "21_day"
    day_30 = "30_day"
    day_60 = "60_day"
    day_90 = "90_day"


class WeeklyChart(BaseModel):
    """Weekly Excalidraw progress chart payload."""
    chart_url: Optional[str] = None
    week_number: int = Field(..., ge=1)
    energy_trend: list[int] = Field(default_factory=list)
    habits_completed_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    current_streak: int = Field(default=0, ge=0)
    milestone_badges: list[str] = Field(default_factory=list)
    mood_trajectory: MoodTrajectory = Field(default=MoodTrajectory.stable)


class AccountabilityVisualPayload(BaseModel):
    """DEP-ENG-079 — Accountability visual chart payload."""
    client_id: str = Field(...)
    weekly_chart: Optional[WeeklyChart] = None
    daily_data_point: Optional[DailyDataPoint] = None


class AccountabilityResult(BaseModel):
    """Result of accountability pipeline operations."""
    success: bool = Field(...)
    data_point_stored: bool = Field(default=False)
    chart_generated: bool = Field(default=False)
    milestone_triggered: Optional[str] = None
    streak_reset: bool = Field(default=False)
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# FR-CA11-10 — Excalidraw Embedded Workspace (DEP-ENG-080)
# ---------------------------------------------------------------------------

class EmbedMode(str, Enum):
    """Excalidraw embed display mode."""
    view = "view"
    edit = "edit"


class ExcalidrawState(BaseModel):
    """Excalidraw canvas state (JSON-serialisable)."""
    type: str = Field(default="excalidraw")
    version: int = Field(default=2)
    elements: list[dict[str, Any]] = Field(default_factory=list)
    app_state: dict[str, Any] = Field(default_factory=dict)
    files: dict[str, Any] = Field(default_factory=dict)


class ExcalidrawEmbedBlock(BaseModel):
    """DEP-ENG-080 — Excalidraw embed block schema for AFFiNE BlockSuite."""
    block_type: str = Field(default="excalidraw-embed")
    block_id: str = Field(default_factory=lambda: f"block-{uuid.uuid4().hex[:12]}")
    excalidraw_state: ExcalidrawState = Field(default_factory=ExcalidrawState)
    mode: EmbedMode = Field(default=EmbedMode.view)
    width: str = Field(default="100%")
    height: str = Field(default="600px")
    source_asset_id: Optional[str] = None
    fallback_png_url: Optional[str] = None


class EmbedInjectionRequest(BaseModel):
    """Request to inject an Excalidraw embed block into an AFFiNE page."""
    workspace_id: str = Field(..., min_length=1)
    page_id: str = Field(..., min_length=1)
    excalidraw_json: dict[str, Any] = Field(...)
    mode: EmbedMode = Field(default=EmbedMode.view)
    position: int = Field(default=0, ge=0)
    source_asset_id: Optional[str] = None


class EmbedInjectionResult(BaseModel):
    """Result of embedding an Excalidraw block."""
    success: bool = Field(...)
    block_id: Optional[str] = None
    page_id: Optional[str] = None
    fallback_used: bool = Field(default=False)
    error: Optional[str] = None


# ===================================================================
# FR-CA11-11 — CVE Canva Clone → AFFiNE Delivery
# ===================================================================

class DeliveryTargetFlag(str, Enum):
    """Feature flag: where VPO is sent."""
    affine_only = "AFFINE_ONLY"
    notion_only = "NOTION_ONLY"
    both = "BOTH"


class SlideEntry(BaseModel):
    """Single slide in a visual composition."""
    slide_number: int = Field(..., ge=1)
    png_url: str = Field(..., min_length=1)
    agss_score: float = Field(..., ge=0.0, le=10.0)


class VisualProductionOutput(BaseModel):
    """DEP-ENG-081 — Visual Production Console database entry."""
    asset_id: str = Field(..., min_length=1)
    composition_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    slides: list[SlideEntry] = Field(..., min_length=1)
    horizontal_stitch_url: str = Field(..., min_length=1)
    zip_download_url: str = Field(..., min_length=1)
    recipe_name: str = Field(..., min_length=1)
    visual_style: str = Field(..., min_length=1)
    why_this_visual: str = Field(default="")
    leadership_farming_note: str = Field(default="")
    tiar_decay_audit: dict[str, Any] = Field(default_factory=dict)
    receipt_chain_status: str = Field(default="PENDING")
    fingerprint_id: Optional[str] = None


class CanvaApproveWebhookPayload(BaseModel):
    """Payload sent from Canva App on composition approval."""
    vpo: VisualProductionOutput = Field(...)
    coach_workspace_id: str = Field(..., min_length=1)
    delivery_target: DeliveryTargetFlag = Field(default=DeliveryTargetFlag.affine_only)
    canva_app_deep_link: Optional[str] = None


class VPODeliveryResult(BaseModel):
    """Result of delivering VPO to target(s)."""
    success: bool = Field(...)
    affine_delivered: bool = Field(default=False)
    notion_delivered: bool = Field(default=False)
    affine_page_id: Optional[str] = None
    error: Optional[str] = None


# ===================================================================
# FR-CA11-12 — Course Video Generation via CMF Pipeline
# ===================================================================

class VisualAidType(str, Enum):
    """Type of visual aid in course video."""
    excalidraw_diagram = "excalidraw_diagram"
    stock_image = "stock_image"
    photo_deck = "photo_deck"


class AmbientMoodProfile(str, Enum):
    """Allowed ambient audio mood profiles for course videos."""
    focus = "focus"
    contemplation = "contemplation"


class CaptionStyle(str, Enum):
    """Caption rendering style."""
    clean_centered = "clean_centered"
    rapid_fire = "rapid_fire"


class VisualAid(BaseModel):
    """Single visual aid used in a course video."""
    type: VisualAidType = Field(...)
    url: str = Field(..., min_length=1)
    source: Optional[str] = None
    query: Optional[str] = None


class CourseVideoEditorialTemplate(BaseModel):
    """Editorial template configuration for course videos."""
    template_name: str = Field(default="course_video")
    duration_range_seconds: tuple[int, int] = Field(default=(300, 600))
    caption_style: CaptionStyle = Field(default=CaptionStyle.clean_centered)
    scene_change_interval_seconds: tuple[int, int] = Field(default=(15, 30))
    audio_mood_profiles: list[AmbientMoodProfile] = Field(
        default_factory=lambda: [AmbientMoodProfile.focus, AmbientMoodProfile.contemplation],
    )
    broll_allowed: bool = Field(default=False)
    intro_duration_seconds: int = Field(default=5)
    outro_duration_seconds: int = Field(default=10)


class LearningPathRegistration(BaseModel):
    """Learning path metadata for a course video."""
    topic_cluster: str = Field(..., min_length=1)
    difficulty_level: str = Field(default="developing")
    content_type: str = Field(default="course_video")
    program_tag: Optional[str] = None


class CourseVideoManifest(BaseModel):
    """DEP-ENG-082 — Course video manifest after successful generation."""
    video_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    duration_seconds: int = Field(..., ge=1)
    video_url: str = Field(..., min_length=1)
    editorial_template: str = Field(default="course_video")
    visual_aids: list[VisualAid] = Field(default_factory=list)
    ambient_audio_mood: AmbientMoodProfile = Field(default=AmbientMoodProfile.contemplation)
    learning_path_registration: Optional[LearningPathRegistration] = None


class CourseVideoResult(BaseModel):
    """Result of course video generation pipeline."""
    success: bool = Field(...)
    manifest: Optional[CourseVideoManifest] = None
    fallback_text_delivered: bool = Field(default=False)
    error: Optional[str] = None


# ===================================================================
# FR-CA11-13 — OBS Recording Pipeline Controller
# ===================================================================

class OBSConnectionState(str, Enum):
    """OBS WebSocket connection state."""
    disconnected = "disconnected"
    connecting = "connecting"
    connected = "connected"
    authenticated = "authenticated"


class RecordingState(str, Enum):
    """OBS recording state."""
    idle = "idle"
    recording = "recording"
    paused = "paused"
    stopping = "stopping"


class PipelineStatus(str, Enum):
    """Post-recording pipeline status."""
    pending_upload = "PENDING_UPLOAD"
    uploading = "UPLOADING"
    pending_transcription = "PENDING_TRANSCRIPTION"
    processing = "PROCESSING"
    completed = "COMPLETED"
    failed = "FAILED"


class RecordingStatusPayload(BaseModel):
    """DEP-ENG-083 — Recording status payload."""
    recording_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recording_file: Optional[str] = None
    recording_duration_seconds: int = Field(default=0, ge=0)
    obs_scenes_used: list[str] = Field(default_factory=list)
    recording_started_at: Optional[datetime] = None
    recording_stopped_at: Optional[datetime] = None
    pipeline_triggered: bool = Field(default=False)
    pipeline_status: PipelineStatus = Field(default=PipelineStatus.pending_upload)


class OBSCommandResult(BaseModel):
    """Result of an OBS controller command."""
    success: bool = Field(...)
    message: str = Field(default="")
    recording_state: Optional[RecordingState] = None
    scene_name: Optional[str] = None
    error: Optional[str] = None


# ===================================================================
# FR-CA11-14 — Excalidraw Live OBS Annotation Overlay
# ===================================================================

class OverlayStatus(str, Enum):
    """OBS overlay activation state."""
    active = "active"
    inactive = "inactive"


class OverlayTheme(str, Enum):
    """Excalidraw overlay theme."""
    dark = "dark"
    light = "light"


class OBSOverlayPayload(BaseModel):
    """DEP-ENG-084 — OBS overlay status payload."""
    overlay_status: OverlayStatus = Field(default=OverlayStatus.inactive)
    excalidraw_url: str = Field(default="http://localhost:9876/overlay")
    obs_source_name: str = Field(default="CCP_Overlay")
    resolution: str = Field(default="1920x1080")
    background: str = Field(default="transparent")
    theme: OverlayTheme = Field(default=OverlayTheme.dark)
    brand_colors: list[str] = Field(default_factory=lambda: ["#2E86AB", "#F18F01", "#FFFFFF"])


class OverlayActivationResult(BaseModel):
    """Result of overlay activation/deactivation."""
    success: bool = Field(...)
    overlay_status: OverlayStatus = Field(default=OverlayStatus.inactive)
    message: str = Field(default="")
    error: Optional[str] = None


# ===================================================================
# FR-CA11-15 — Contextual Branding Engine with DPA
# ===================================================================

class OverrideMode(str, Enum):
    """Branding override mode."""
    adaptive = "adaptive"
    brand_saturated = "brand_saturated"


class PADVector(BaseModel):
    """Pleasure-Arousal-Dominance vector."""
    P: float = Field(default=0.0, ge=-1.0, le=1.0)
    A: float = Field(default=0.0, ge=-1.0, le=1.0)
    D: float = Field(default=0.0, ge=-1.0, le=1.0)


class BrandHueAnalysis(BaseModel):
    """Coach's primary hue PAD decomposition."""
    primary_hue: str = Field(..., min_length=1)
    hue_name: str = Field(default="")
    inherent_pad: PADVector = Field(default_factory=PADVector)
    kelvin_equivalent: str = Field(default="")
    temperature_class: str = Field(default="neutral")
    congruent_moods: list[str] = Field(default_factory=list)
    incongruent_moods: list[str] = Field(default_factory=list)


class MoodPaletteColors(BaseModel):
    """Color set within a mood palette."""
    background_primary: str = Field(..., min_length=1)
    background_gradient: str = Field(default="")
    accent: str = Field(..., min_length=1)
    text_primary: str = Field(..., min_length=1)
    text_secondary: str = Field(default="")
    overlay: str = Field(default="")


class MoodPalette(BaseModel):
    """A single mood palette (Escape, Processing, Discovery, Status)."""
    description: str = Field(default="")
    kelvin_range: str = Field(default="")
    target_pad: PADVector = Field(default_factory=PADVector)
    colors: MoodPaletteColors = Field(...)


class ArchetypePADTarget(BaseModel):
    """PAD target for a content archetype."""
    pad: PADVector = Field(default_factory=PADVector)
    mood_base: str = Field(..., min_length=1)
    saturation_shift: float = Field(default=0.0, ge=-1.0, le=1.0)


class ResolvedPalette(BaseModel):
    """DEP-ENG-085 — Output of DPA engine palette resolution."""
    resolved_palette_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    content_archetype: str = Field(..., min_length=1)
    audience_mood_state: str = Field(default="")
    target_pad: PADVector = Field(default_factory=PADVector)
    bhcs: float = Field(default=0.0, ge=0.0, le=1.0)
    brand_hue_used: bool = Field(default=False)
    identity: dict[str, Any] = Field(default_factory=dict)
    palette: MoodPaletteColors = Field(...)
    kelvin_range: str = Field(default="")
    saturation_adjustment: float = Field(default=0.0)
    override_active: bool = Field(default=False)


class DPAResult(BaseModel):
    """Result of DPA engine resolution."""
    success: bool = Field(...)
    resolved: Optional[ResolvedPalette] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-16 — CCP Studio Block (Recording & Streaming)
# DEP-ENG-087 through DEP-ENG-093 (corrected from spec-internal 060-066)
# Agent: Diego (Studio Session Conductor)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class RecordingMode(str, Enum):
    """§4 Stage 1: Five recording modes supported by CCP Studio Block."""
    YOUTUBE_LONGFORM = "youtube_longform"
    SHORT_FORM_VERTICAL = "short_form_vertical"
    WEBINAR_VOD = "webinar_vod"
    COURSE_VIDEO = "course_video"
    LOOM_QUICK = "loom_quick"


class StudioAspectRatio(str, Enum):
    """§4 Stage 2 Step 7: Aspect ratios."""
    LANDSCAPE_16_9 = "16:9"
    PORTRAIT_9_16 = "9:16"


class StudioResolution(str, Enum):
    """Quality tiers per FB §3.2."""
    HD_1080 = "1080p"
    HD_720 = "720p"


class StudioSessionStatus(str, Enum):
    """Session lifecycle states. §5 Output Schema."""
    RECORDING = "recording"
    PAUSED = "paused"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"
    STREAMING = "streaming"


class StudioBlockError(str, Enum):
    """Error types for CCP Studio Block pipeline."""
    PLUGIN_REGISTRATION_FAILED = "PLUGIN_REGISTRATION_FAILED"
    CAPTURE_INIT_FAILED = "CAPTURE_INIT_FAILED"
    RECORDER_INIT_FAILED = "RECORDER_INIT_FAILED"
    UPLOAD_FAILED = "UPLOAD_FAILED"
    CMF_TRIGGER_FAILED = "CMF_TRIGGER_FAILED"
    STREAM_CONNECTION_FAILED = "STREAM_CONNECTION_FAILED"
    CHUNK_SAVE_FAILED = "CHUNK_SAVE_FAILED"
    INVALID_MODE_RESOLUTION = "INVALID_MODE_RESOLUTION"
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    TELEPROMPTER_LOAD_FAILED = "TELEPROMPTER_LOAD_FAILED"


class AssetType(str, Enum):
    """§4 Stage 4 Step 1: Asset types extracted from block tree."""
    IMAGE = "image"
    EXCALIDRAW = "excalidraw"
    CANVA = "canva"


# ── Constants ──────────────────────────────────────────────────────────

# §4 Stage 2 Step 4: MediaRecorder timeslice (1s chunks to MediaRecorder)
MEDIARECORDER_TIMESLICE_MS: int = 1000

# Stress Test Q34: IndexedDB chunk interval (5s Blob)
INDEXEDDB_CHUNK_INTERVAL_SECONDS: float = 5.0

# §4 Stage 2 Step 6: Periodic S3 chunk saves (30s)
S3_PERIODIC_SAVE_INTERVAL_SECONDS: int = 30

# Default framerate (§4 Stage 2 Step 4: 30fps)
DEFAULT_FRAMERATE: int = 30

# §4 Stage 2 Step 4: Video bitrate (8 Mbps)
DEFAULT_VIDEO_BITRATE_BPS: int = 8_000_000

# Teleprompter: §4 Stage 3 Step 4: Speed range 1.0–5.0 words-per-second
TELEPROMPTER_SPEED_MIN_WPS: float = 1.0
TELEPROMPTER_SPEED_MAX_WPS: float = 5.0

# §4 Stage 3 Step 5: Font size options
TELEPROMPTER_FONT_SIZES: list[int] = [18, 24, 32, 48]

# Default teleprompter speed
TELEPROMPTER_DEFAULT_SPEED_WPS: float = 2.5

# Default teleprompter font size
TELEPROMPTER_DEFAULT_FONT_SIZE_PX: int = 24

# §4 Stage 5: Mode → CMF pipeline template mapping
CMF_TEMPLATE_MAP: dict[str, str] = {
    RecordingMode.YOUTUBE_LONGFORM.value: "youtube_longform",
    RecordingMode.SHORT_FORM_VERTICAL.value: "short_form_vertical",
    RecordingMode.WEBINAR_VOD.value: "webinar_vod",
    RecordingMode.COURSE_VIDEO.value: "course_video",
    RecordingMode.LOOM_QUICK.value: "loom_quick",
}

# FB §3.2: Quality tiers (mode → default config)
QUALITY_TIERS: dict[str, dict[str, Any]] = {
    RecordingMode.YOUTUBE_LONGFORM.value: {
        "aspect_ratio": StudioAspectRatio.LANDSCAPE_16_9.value,
        "default_resolution": StudioResolution.HD_1080.value,
        "selectable_resolutions": [StudioResolution.HD_1080.value, StudioResolution.HD_720.value],
        "bitrate_bps": 8_000_000,
        "width": 1920,
        "height": 1080,
    },
    RecordingMode.SHORT_FORM_VERTICAL.value: {
        "aspect_ratio": StudioAspectRatio.PORTRAIT_9_16.value,
        "default_resolution": StudioResolution.HD_1080.value,
        "selectable_resolutions": [StudioResolution.HD_1080.value],
        "bitrate_bps": 8_000_000,
        "width": 1080,
        "height": 1920,
    },
    RecordingMode.WEBINAR_VOD.value: {
        "aspect_ratio": StudioAspectRatio.LANDSCAPE_16_9.value,
        "default_resolution": StudioResolution.HD_1080.value,
        "selectable_resolutions": [StudioResolution.HD_1080.value, StudioResolution.HD_720.value],
        "bitrate_bps": 6_000_000,
        "width": 1920,
        "height": 1080,
    },
    RecordingMode.COURSE_VIDEO.value: {
        "aspect_ratio": StudioAspectRatio.LANDSCAPE_16_9.value,
        "default_resolution": StudioResolution.HD_1080.value,
        "selectable_resolutions": [StudioResolution.HD_1080.value, StudioResolution.HD_720.value],
        "bitrate_bps": 8_000_000,
        "width": 1920,
        "height": 1080,
    },
    RecordingMode.LOOM_QUICK.value: {
        "aspect_ratio": StudioAspectRatio.LANDSCAPE_16_9.value,
        "default_resolution": StudioResolution.HD_720.value,
        "selectable_resolutions": [StudioResolution.HD_720.value],
        "bitrate_bps": 3_000_000,
        "width": 1280,
        "height": 720,
    },
}

# Crash recovery: minimum recoverable seconds (AC9)
CRASH_RECOVERY_MIN_SECONDS: int = 60

# Stream health defaults
STREAM_HEALTH_CHECK_INTERVAL_SECONDS: int = 5

# Receipt agent name (C-11 compliant: used in orchestration only)
STUDIO_AGENT_NAME: str = "Diego"


# ── Models ─────────────────────────────────────────────────────────────


class RecordingQualityConfig(BaseModel):
    """Resolved quality configuration for a recording session.

    §4 Stage 2 Steps 3-4 + FB §3.2 Quality Tiers.
    """
    resolution: str = Field(..., description="1080p or 720p")
    aspect_ratio: str = Field(..., description="16:9 or 9:16")
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    video_bitrate_bps: int = Field(..., gt=0)
    framerate: int = Field(default=DEFAULT_FRAMERATE, gt=0)
    mime_type: str = Field(
        default="video/webm;codecs=vp9",
        description="§4 Stage 2 Step 4: MediaRecorder mimeType",
    )


class StudioBlockRegistration(BaseModel):
    """DEP-ENG-087 — Plugin Registration configuration.

    §4 Stage 1: /studio command registration, UI shell structure.
    """
    command: str = Field(default="/studio", description="AFFiNE slash command")
    block_type: str = Field(default="ccp-studio-block")
    panels: list[str] = Field(
        default_factory=lambda: [
            "preview",
            "controls",
            "teleprompter",
            "assets",
            "soundboard",
        ],
    )
    recording_modes: list[str] = Field(
        default_factory=lambda: [m.value for m in RecordingMode],
    )


class IndexedDBChunk(BaseModel):
    """Stress Test Q34: 5-second Blob chunk persisted to IndexedDB.

    Each chunk is immediately committed to IndexedDB for crash recovery.
    """
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(..., min_length=1)
    sequence_number: int = Field(..., ge=0)
    blob_size_bytes: int = Field(..., ge=0)
    duration_seconds: float = Field(default=INDEXEDDB_CHUNK_INTERVAL_SECONDS)
    stored_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class TeleprompterConfig(BaseModel):
    """DEP-ENG-089 — Teleprompter configuration.

    §4 Stage 3: Auto-scrolling text overlay.
    """
    source_page_id: Optional[str] = Field(
        default=None,
        description="AFFiNE page ID for script text. None = current page.",
    )
    speed_wps: float = Field(
        default=TELEPROMPTER_DEFAULT_SPEED_WPS,
        ge=TELEPROMPTER_SPEED_MIN_WPS,
        le=TELEPROMPTER_SPEED_MAX_WPS,
    )
    font_size_px: int = Field(default=TELEPROMPTER_DEFAULT_FONT_SIZE_PX)
    mirror_mode: bool = Field(default=False)
    is_scrolling: bool = Field(default=False)


class TeleprompterScrollResult(BaseModel):
    """Result of teleprompter scroll duration calculation (AC4)."""
    word_count: int = Field(..., ge=0)
    speed_wps: float = Field(..., gt=0)
    scroll_duration_seconds: float = Field(..., ge=0)


class AssetPanelEntry(BaseModel):
    """DEP-ENG-090 — Single asset entry in the Studio asset panel.

    §4 Stage 4 Step 1: Filtered from page block tree.
    """
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_type: str = Field(..., description="image, excalidraw, or canva")
    source_block_id: str = Field(..., min_length=1)
    thumbnail_url: Optional[str] = None
    is_overlay_active: bool = Field(default=False)


class S3UploadRequest(BaseModel):
    """§4 Stage 5 Step 1: Request for pre-signed S3 upload URL."""
    recording_mode: str = Field(...)
    coach_id: str = Field(..., min_length=1)
    file_size: int = Field(..., gt=0)


class S3UploadResponse(BaseModel):
    """§4 Stage 5 Step 1: Pre-signed URL response."""
    upload_url: str = Field(...)
    s3_key: str = Field(...)
    expires_at: datetime = Field(...)


class CMFTriggerPayload(BaseModel):
    """§4 Stage 5 Steps 3-4: CMF pipeline trigger request.

    POST /studio/complete payload.
    """
    s3_url: str = Field(...)
    recording_mode: str = Field(...)
    coach_id: str = Field(..., min_length=1)
    source_page_id: Optional[str] = None
    duration: int = Field(..., ge=0)


class CMFTriggerResult(BaseModel):
    """Result of CMF pipeline trigger."""
    cmf_job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cmf_pipeline_template: str = Field(...)
    success: bool = Field(...)
    error: Optional[str] = None


class StreamDestination(BaseModel):
    """§4 Stage 6 Step 4: Stream destination config.

    YouTube Live, Facebook Live, Custom RTMP.
    """
    platform: str = Field(..., description="youtube_live, facebook_live, custom_rtmp")
    rtmp_url: str = Field(..., min_length=1)
    stream_key: str = Field(default="")


class StreamHealthMetrics(BaseModel):
    """§4 Stage 6 Step 6: Push metrics from ccp-stream-service."""
    bitrate_kbps: float = Field(default=0.0, ge=0.0)
    frame_drops: int = Field(default=0, ge=0)
    connection_status: str = Field(default="disconnected")
    viewer_count: int = Field(default=0, ge=0)


class StreamConfig(BaseModel):
    """DEP-ENG-093 — Streaming engine configuration.

    §4 Stage 6: ccp-stream-service WebSocket + RTMP.
    """
    session_id: str = Field(..., min_length=1)
    websocket_url: str = Field(default="")
    destinations: list[StreamDestination] = Field(default_factory=list)
    parallel_s3_archive: bool = Field(default=True)
    health: StreamHealthMetrics = Field(default_factory=StreamHealthMetrics)


class StudioSessionRecord(BaseModel):
    """§5 Primary Output Schema: Studio Session Record.

    Matches the JSON schema defined in spec §5.
    """
    transaction_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    source_page_id: Optional[str] = None
    recording_mode: str = Field(...)
    aspect_ratio: str = Field(...)
    resolution: str = Field(...)
    s3_recording_url: Optional[str] = None
    s3_vod_url: Optional[str] = None
    duration_seconds: int = Field(default=0, ge=0)
    is_stream: bool = Field(default=False)
    stream_destinations: list[str] = Field(default_factory=list)
    cmf_pipeline_template: Optional[str] = None
    cmf_job_id: Optional[str] = None
    status: str = Field(default=StudioSessionStatus.RECORDING.value)
    receipt_chain_guard: dict[str, Any] = Field(
        default_factory=lambda: {"schema_ref": "DEP-ENG-041"},
    )


class CrashRecoveryResult(BaseModel):
    """Stress Test Q34 + AC9: Result of crash recovery from IndexedDB chunks."""
    session_id: str = Field(...)
    chunks_recovered: int = Field(default=0, ge=0)
    total_duration_seconds: float = Field(default=0.0, ge=0.0)
    is_recoverable: bool = Field(default=False)
    s3_multipart_upload_url: Optional[str] = None


class StudioBlockResult(BaseModel):
    """Top-level result wrapper for Studio Block operations."""
    success: bool = Field(...)
    session: Optional[StudioSessionRecord] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-17 — Studio Soundboard & Programmable Audio
# DEP-ENG-094 through DEP-ENG-098 (corrected from spec-internal 070-073)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class MusicTrackType(str, Enum):
    """§4 Stage 3: Four music button types."""
    INTRO = "intro"
    OUTRO = "outro"
    CELEBRATION = "celebration"
    SAD = "sad"


class SoundboardError(str, Enum):
    """Error types for Soundboard pipeline."""
    INVALID_SLOT_INDEX = "INVALID_SLOT_INDEX"
    INVALID_TRACK_TYPE = "INVALID_TRACK_TYPE"
    UPLOAD_TOO_LARGE = "UPLOAD_TOO_LARGE"
    UPLOAD_TOO_LONG = "UPLOAD_TOO_LONG"
    INVALID_FORMAT = "INVALID_FORMAT"
    DECODE_FAILED = "DECODE_FAILED"
    PREFERENCES_NOT_FOUND = "PREFERENCES_NOT_FOUND"


# ── Constants ──────────────────────────────────────────────────────────

# §4 Stage 1: Default gain levels
VOICE_GAIN_DEFAULT: float = 1.0
SFX_GAIN_DEFAULT: float = 0.8
MUSIC_GAIN_DEFAULT: float = 0.5

# §4 Stage 3: Fade transition parameters
MUSIC_FADE_MS: int = 500
STOP_ALL_RAMP_MS: int = 100

# §4 Stage 4 Step 4: Upload constraints
SFX_MAX_DURATION_SECONDS: int = 10
MUSIC_MAX_DURATION_SECONDS: int = 60
AUDIO_MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB
ALLOWED_AUDIO_FORMATS: list[str] = ["mp3", "wav"]

# Total slot counts
SFX_SLOT_COUNT: int = 5
MUSIC_TRACK_COUNT: int = 4

# S3 paths
S3_SFX_DEFAULTS_PREFIX: str = "s3://ccp-assets/studio/sfx/defaults/"
S3_MUSIC_DEFAULTS_PREFIX: str = "s3://ccp-assets/studio/music/defaults/"

# Default SFX slots (§4 Stage 2 Step 1)
DEFAULT_SFX_SLOTS: list[dict[str, Any]] = [
    {"slot": 1, "label": "Drumroll", "s3_url": f"{S3_SFX_DEFAULTS_PREFIX}drumroll.mp3", "volume": SFX_GAIN_DEFAULT},
    {"slot": 2, "label": "Comedy Horn", "s3_url": f"{S3_SFX_DEFAULTS_PREFIX}comedy_horn.mp3", "volume": SFX_GAIN_DEFAULT},
    {"slot": 3, "label": "Applause", "s3_url": f"{S3_SFX_DEFAULTS_PREFIX}applause.mp3", "volume": SFX_GAIN_DEFAULT},
    {"slot": 4, "label": "Record Scratch", "s3_url": f"{S3_SFX_DEFAULTS_PREFIX}record_scratch.mp3", "volume": SFX_GAIN_DEFAULT},
    {"slot": 5, "label": "Ding", "s3_url": f"{S3_SFX_DEFAULTS_PREFIX}ding.mp3", "volume": SFX_GAIN_DEFAULT},
]

# Default music tracks (§4 Stage 3 Step 1)
DEFAULT_MUSIC_TRACKS: dict[str, dict[str, Any]] = {
    MusicTrackType.INTRO.value: {"s3_url": f"{S3_MUSIC_DEFAULTS_PREFIX}intro_upbeat.mp3", "volume": MUSIC_GAIN_DEFAULT, "fade_ms": MUSIC_FADE_MS},
    MusicTrackType.OUTRO.value: {"s3_url": f"{S3_MUSIC_DEFAULTS_PREFIX}outro_warm.mp3", "volume": MUSIC_GAIN_DEFAULT, "fade_ms": MUSIC_FADE_MS},
    MusicTrackType.CELEBRATION.value: {"s3_url": f"{S3_MUSIC_DEFAULTS_PREFIX}celebration_fanfare.mp3", "volume": 0.6, "fade_ms": MUSIC_FADE_MS},
    MusicTrackType.SAD.value: {"s3_url": f"{S3_MUSIC_DEFAULTS_PREFIX}sad_dramatic.mp3", "volume": MUSIC_GAIN_DEFAULT, "fade_ms": MUSIC_FADE_MS},
}


# ── Models ─────────────────────────────────────────────────────────────


class SFXSlotConfig(BaseModel):
    """Single SFX slot configuration. §4 Stage 2."""
    slot: int = Field(..., ge=1, le=SFX_SLOT_COUNT)
    label: str = Field(..., min_length=1, max_length=50)
    s3_url: str = Field(..., min_length=1)
    volume: float = Field(default=SFX_GAIN_DEFAULT, ge=0.0, le=1.0)


class MusicTrackConfig(BaseModel):
    """Single music track configuration. §4 Stage 3."""
    s3_url: str = Field(..., min_length=1)
    volume: float = Field(default=MUSIC_GAIN_DEFAULT, ge=0.0, le=1.0)
    fade_ms: int = Field(default=MUSIC_FADE_MS, ge=0)


class AudioUploadRequest(BaseModel):
    """§4 Stage 4 Step 4: Audio file upload request."""
    coach_id: str = Field(..., min_length=1)
    file_name: str = Field(..., min_length=1)
    file_size_bytes: int = Field(..., gt=0)
    duration_seconds: float = Field(..., gt=0)
    is_sfx: bool = Field(default=True)


class AudioUploadValidation(BaseModel):
    """Result of audio upload validation."""
    is_valid: bool = Field(...)
    error: Optional[str] = None
    max_duration: int = Field(default=0)
    max_size: int = Field(default=0)


class FadeSpec(BaseModel):
    """Audio fade transition specification."""
    start_volume: float = Field(..., ge=0.0, le=1.0)
    end_volume: float = Field(..., ge=0.0, le=1.0)
    duration_ms: int = Field(..., ge=0)


class MixerChannelConfig(BaseModel):
    """Configuration for a single channel in the Web Audio mixer graph."""
    channel_name: str = Field(...)
    gain: float = Field(default=1.0, ge=0.0, le=1.0)
    is_muted: bool = Field(default=False)


class AudioMixerConfig(BaseModel):
    """DEP-ENG-095 — Web Audio API mixer graph configuration."""
    voice_channel: MixerChannelConfig = Field(
        default_factory=lambda: MixerChannelConfig(channel_name="voice", gain=VOICE_GAIN_DEFAULT),
    )
    sfx_channels: list[MixerChannelConfig] = Field(default_factory=list)
    music_channel: MixerChannelConfig = Field(
        default_factory=lambda: MixerChannelConfig(channel_name="music", gain=MUSIC_GAIN_DEFAULT),
    )
    sample_rate: int = Field(default=48000)


class StudioPreferences(BaseModel):
    """DEP-ENG-097 — Per-coach studio preferences. §5 Data Model."""
    preferences_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    sfx_slots: list[SFXSlotConfig] = Field(default_factory=list)
    music_tracks: dict[str, MusicTrackConfig] = Field(default_factory=dict)
    voice_volume: float = Field(default=VOICE_GAIN_DEFAULT, ge=0.0, le=1.0)
    guest_layout: str = Field(default="pip")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SoundboardResult(BaseModel):
    """Top-level result wrapper for Soundboard operations."""
    success: bool = Field(...)
    preferences: Optional[StudioPreferences] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-18 — Conscious Social Scheduling & Performance Analysis
# DEP-ENG-099 through DEP-ENG-103 (corrected from spec-internal 075-079)
# Agent: Sofia (Social Performance Analyst)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class SocialPlatform(str, Enum):
    """Supported social media platforms."""
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    X = "x"


class SocialPostStatus(str, Enum):
    """Post lifecycle states. §5 Data Model."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class CollectionCycle(str, Enum):
    """§4 Stage 3: Performance metric collection windows."""
    H6 = "6h"
    H24 = "24h"
    H48 = "48h"
    H168 = "168h"


class SocialSchedulingError(str, Enum):
    """Error types for Social Scheduling pipeline."""
    QUEUE_FAILED = "QUEUE_FAILED"
    PUBLISH_FAILED = "PUBLISH_FAILED"
    INGESTION_FAILED = "INGESTION_FAILED"
    TEMPORAL_MUTEX_VIOLATION = "DAG_VIOLATION_COLLISION"
    INVALID_PLATFORM = "INVALID_PLATFORM"
    MISSING_CONTENT = "MISSING_CONTENT"


# ── Constants ──────────────────────────────────────────────────────────

# §4 Stage 3 Step 5: Top performer threshold (2x rolling average)
TOP_PERFORMER_THRESHOLD: float = 2.0

# Collection cycles for metric polling
COLLECTION_CYCLES: list[str] = [c.value for c in CollectionCycle]

# Stress Test Q39: ±4h temporal mutex
TEMPORAL_MUTEX_HOURS: int = 4

# Rolling average window (30 days)
ROLLING_AVERAGE_WINDOW_DAYS: int = 30

# Engagement score weights (views=0.1, likes=0.2, shares=0.3, comments=0.25, saves=0.15)
ENGAGEMENT_WEIGHTS: dict[str, float] = {
    "views": 0.1,
    "likes": 0.2,
    "shares": 0.3,
    "comments": 0.25,
    "saves": 0.15,
}

# Agent name for receipts
SOCIAL_AGENT_NAME: str = "Sofia"


# ── Models ─────────────────────────────────────────────────────────────


class QueuePostRequest(BaseModel):
    """§4 Stage 2 Step 1: POST /social/queue payload."""
    coach_id: str = Field(..., min_length=1)
    content_id: Optional[str] = None
    caption: str = Field(default="")
    media_urls: list[dict[str, str]] = Field(default_factory=list)
    hashtags: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(..., min_length=1)
    scheduled_time: datetime = Field(...)
    is_human_scheduled: bool = Field(default=False)


class SocialPostRecord(BaseModel):
    """§5 Data Model: social_posts row."""
    post_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    content_id: Optional[str] = None
    platform: str = Field(...)
    caption: str = Field(default="")
    media_urls: list[dict[str, str]] = Field(default_factory=list)
    hashtags: list[str] = Field(default_factory=list)
    scheduler_post_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    status: str = Field(default=SocialPostStatus.DRAFT.value)
    is_human_scheduled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EngagementMetrics(BaseModel):
    """§4 Stage 3 Step 2: Raw engagement data from scheduler API."""
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    saves: int = Field(default=0, ge=0)
    ctr: float = Field(default=0.0, ge=0.0)


class SocialPerformanceRecord(BaseModel):
    """§5 Data Model: social_performance row."""
    performance_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    post_id: str = Field(..., min_length=1)
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    saves: int = Field(default=0, ge=0)
    ctr: float = Field(default=0.0, ge=0.0)
    engagement_score: float = Field(default=0.0, ge=0.0)
    collection_cycle: str = Field(...)
    is_top_performer: bool = Field(default=False)
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TemporalMutexResult(BaseModel):
    """Stress Test Q39: ±4h temporal mutex check result."""
    is_clear: bool = Field(...)
    conflicting_post_id: Optional[str] = None
    conflict_platform: Optional[str] = None
    conflict_time: Optional[datetime] = None
    human_priority_override: bool = Field(default=False)


class SocialSchedulingResult(BaseModel):
    """Top-level result wrapper for Social Scheduling operations."""
    success: bool = Field(...)
    posts: list[SocialPostRecord] = Field(default_factory=list)
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-19 — Interactive Trivianar Engine
# DEP-ENG-104 through DEP-ENG-113 (corrected from spec-internal 080-086)
# Agent: Marco (Trivianar Engine Operator)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class TriviaGameMode(str, Enum):
    """§4 Stage 2: Six game modes."""
    COUNTDOWN = "countdown"
    TEAM = "team"
    MULTI_ROUND = "multi_round"
    WAGERING = "wagering"
    SURVIVOR = "survivor"
    POLLS = "polls"


class QuestionDifficulty(str, Enum):
    """Difficulty levels per question."""
    ACCESSIBLE = "accessible"
    MODERATE = "moderate"
    CHALLENGING = "challenging"


class ReactionPool(str, Enum):
    """§4 Stage 4: Reaction atmosphere pools."""
    PRE_QUESTION_HYPE = "pre_question_hype"
    CORRECT_ANSWER_CELEBRATION = "correct_answer_celebration"
    WRONG_ANSWER_SHOCK = "wrong_answer_shock"
    SPEED_RECORD = "speed_record"
    COMMITMENT_EMPOWERMENT = "commitment_empowerment"


class TriviaError(str, Enum):
    """Error types for Trivianar Engine."""
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    QUESTION_NOT_FOUND = "QUESTION_NOT_FOUND"
    USER_ELIMINATED = "USER_ELIMINATED"
    INVALID_WAGER = "INVALID_WAGER"
    TIME_EXPIRED = "TIME_EXPIRED"
    DUPLICATE_ANSWER = "DUPLICATE_ANSWER"


# ── Constants ──────────────────────────────────────────────────────────

# §4 Stage 2 Step 1: Countdown scoring
COUNTDOWN_MAX_SCORE: int = 1000
COUNTDOWN_DIVISOR: int = 10

# Default question time limit (§5 schema)
DEFAULT_TIME_LIMIT_SECONDS: int = 15

# §4 Stage 4 Step 7: Reaction delivery delay
REACTION_DELAY_MS: int = 500

# Speed record threshold (AC5: answer < 2s)
SPEED_RECORD_THRESHOLD_MS: int = 2000

# Leaderboard display size (§4 Stage 6 Step 1)
LEADERBOARD_SIZE: int = 10

# §4 Stage 2 Step 4: Wager range
WAGER_MIN: int = 100
WAGER_MAX: int = 500

# Agent name
TRIVIA_AGENT_NAME: str = "Marco"


# ── Models ─────────────────────────────────────────────────────────────


class TriviaQuestion(BaseModel):
    """§5 Data Model: trivia_questions row."""
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = Field(..., min_length=1)
    surface_text: str = Field(..., min_length=1)
    answer_options: list[dict[str, Any]] = Field(..., min_length=2)
    correct_answer: str = Field(..., min_length=1, max_length=1)
    dimension: Optional[str] = None
    difficulty: str = Field(default=QuestionDifficulty.ACCESSIBLE.value)
    time_limit_seconds: int = Field(default=DEFAULT_TIME_LIMIT_SECONDS, gt=0)
    media_url: Optional[str] = None
    fun_fact: Optional[str] = None
    cbcs_mapping: Optional[dict[str, Any]] = None
    round_id: Optional[str] = None


class TriviaResponse(BaseModel):
    """§5 Data Model: trivia_responses row."""
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = Field(..., gt=0)
    question_id: str = Field(..., min_length=1)
    stream_id: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1, max_length=1)
    is_correct: bool = Field(...)
    score: int = Field(default=0)
    response_time_ms: int = Field(default=0, ge=0)
    team_id: Optional[str] = None
    is_eliminated: bool = Field(default=False)
    qualifying_assessment: Optional[dict[str, Any]] = None
    responded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LeaderboardEntry(BaseModel):
    """§4 Stage 6: Single leaderboard row."""
    rank: int = Field(..., ge=1)
    user_id: int = Field(..., gt=0)
    display_name: str = Field(default="")
    total_score: int = Field(default=0)
    games_played: int = Field(default=0)
    win_count: int = Field(default=0)
    current_streak: int = Field(default=0)


class TriviaSessionConfig(BaseModel):
    """§4 Stage 1 Step 4: POST /trivia/start payload."""
    stream_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    question_set_id: Optional[str] = None
    game_mode: str = Field(default=TriviaGameMode.COUNTDOWN.value)
    telegram_group_id: Optional[str] = None


class ScoringResult(BaseModel):
    """Result of a scoring calculation."""
    score: int = Field(default=0)
    is_correct: bool = Field(default=False)
    is_speed_record: bool = Field(default=False)
    is_eliminated: bool = Field(default=False)


class MicrocommitmentResponse(BaseModel):
    """§4 Stage 3 (Microcommitment Checkpoint — DEP-ENG-110)."""
    user_id: int = Field(..., gt=0)
    stream_id: str = Field(..., min_length=1)
    commitment_text: str = Field(..., min_length=1)
    is_cbcs_priority: bool = Field(default=True)
    responded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BatchReceiptPayload(BaseModel):
    """§4 Stage 6 Step 5: Batch receipt for end-of-stream responses."""
    stream_id: str = Field(..., min_length=1)
    total_responses: int = Field(default=0, ge=0)
    total_users: int = Field(default=0, ge=0)
    response_hash: str = Field(default="")


class TrivianarResult(BaseModel):
    """Top-level result wrapper for Trivianar Engine operations."""
    success: bool = Field(...)
    session_config: Optional[TriviaSessionConfig] = None
    leaderboard: list[LeaderboardEntry] = Field(default_factory=list)
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-20 — Trivianar Lead Generation Viral Loop
# DEP-ENG-114 through DEP-ENG-116 (corrected from spec-internal 090-092)
# Agent: Marco (Lead Capture Operator)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class NurtureStatus(str, Enum):
    """§5 Data Model: nurture_status column values."""
    NEW = "new"
    ACTIVE = "active"
    PASSIVE = "passive"
    CONVERTED = "converted"


class LeadCaptureError(str, Enum):
    """Error types for Lead Capture."""
    LEAD_NOT_FOUND = "LEAD_NOT_FOUND"
    DUPLICATE_LEAD = "DUPLICATE_LEAD"
    COOLDOWN_ACTIVE = "COOLDOWN_ACTIVE"
    INSUFFICIENT_RESPONSES = "INSUFFICIENT_RESPONSES"
    INVALID_CONTACT = "INVALID_CONTACT"


# ── Constants ──────────────────────────────────────────────────────────

# §4 Stage 3 Step 4: 21-day commercial cooldown
COMMERCIAL_COOLDOWN_DAYS: int = 21

# §4 Stage 3 Step 1: Minimum qualifying responses for CBCS warm start
MIN_QUALIFYING_RESPONSES: int = 3

# Agent name (shared with FR-CA11-19 Marco)
LEAD_CAPTURE_AGENT_NAME: str = "Marco"


# ── Models ─────────────────────────────────────────────────────────────


class TriviaLead(BaseModel):
    """§5 Data Model: trivia_leads row."""
    lead_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    telegram_user_id: int = Field(..., gt=0)
    first_name: str = Field(default="")
    phone_number: Optional[str] = None
    email: Optional[str] = None
    referred_by_user_id: Optional[int] = None
    coach_id: str = Field(..., min_length=1)
    stream_id: Optional[str] = None
    cbcs_initial_assessment: Optional[dict[str, Any]] = None
    nurture_status: str = Field(default=NurtureStatus.NEW.value)
    commercial_cooldown_until: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LeadContactUpdate(BaseModel):
    """Update payload for contact capture DM flow."""
    telegram_user_id: int = Field(..., gt=0)
    coach_id: str = Field(..., min_length=1)
    phone_number: Optional[str] = None
    email: Optional[str] = None


class CBCSWarmStartPayload(BaseModel):
    """§4 Stage 3: CBCS warm start entry for a captured lead."""
    lead_id: str = Field(..., min_length=1)
    telegram_user_id: int = Field(..., gt=0)
    coach_id: str = Field(..., min_length=1)
    qualifying_responses: int = Field(..., ge=0)
    cbcs_initial_assessment: dict[str, Any] = Field(default_factory=dict)
    warm_start: bool = Field(default=True)


class CooldownCheck(BaseModel):
    """Result of 21-day commercial cooldown check."""
    is_active: bool = Field(...)
    cooldown_until: Optional[datetime] = None
    days_remaining: int = Field(default=0, ge=0)


class LeadCaptureResult(BaseModel):
    """Top-level result wrapper for Lead Capture operations."""
    success: bool = Field(...)
    lead: Optional[TriviaLead] = None
    warm_start: Optional[CBCSWarmStartPayload] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-21 — Studio Guest Join (WebRTC Multi-Party)
# DEP-ENG-117 through DEP-ENG-121 (corrected from spec-internal 093-097)
# Agent: Diego (Studio Guest Join Operator)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class GuestLayoutMode(str, Enum):
    """§5 Data Model: layout_mode values."""
    PIP = "pip"
    SIDE_BY_SIDE = "side_by_side"


class GuestSessionStatus(str, Enum):
    """§5 Data Model: status values."""
    PENDING = "pending"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class GuestJoinError(str, Enum):
    """Error types for Guest Join."""
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_NOT_FOUND = "TOKEN_NOT_FOUND"
    TOKEN_ALREADY_USED = "TOKEN_ALREADY_USED"
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    CONNECTION_FAILED = "CONNECTION_FAILED"


# ── Constants ──────────────────────────────────────────────────────────

# §4 Stage 2 Step 2: Token configuration
INVITE_TOKEN_LENGTH: int = 64
TOKEN_EXPIRY_MINUTES: int = 30

# §4 Stage 3 Step 3: PiP sizing
PIP_SIZE_DEFAULT: float = 0.25
PIP_SIZE_MIN: float = 0.15
PIP_SIZE_MAX: float = 0.35

# Agent name (shared with FR-CA11-16 Diego)
GUEST_JOIN_AGENT_NAME: str = "Diego"

# §3 Technical Decisions: ICE servers
DEFAULT_ICE_SERVERS: list[dict[str, Any]] = [
    {"urls": "stun:stun.l.google.com:19302"},
    {"urls": "turn:turn.ccp.aws.com:3478", "username": "ccp", "credential": "ccp-turn"},
]


# ── Models ─────────────────────────────────────────────────────────────


class GuestInvite(BaseModel):
    """§4 Stage 2 Step 1: POST /studio/guest-invite response."""
    invite_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(..., min_length=1)
    coach_name: str = Field(default="")
    token: str = Field(..., min_length=1)
    invite_url: str = Field(default="")
    expires_at: datetime = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GuestSessionRecord(BaseModel):
    """§5 Data Model: studio_guest_sessions row."""
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = Field(..., min_length=1)
    guest_name: str = Field(..., min_length=1)
    join_token: str = Field(..., min_length=1)
    token_expires_at: datetime = Field(...)
    layout_mode: str = Field(default=GuestLayoutMode.PIP.value)
    status: str = Field(default=GuestSessionStatus.PENDING.value)
    connected_at: Optional[datetime] = None
    disconnected_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GuestCanvasRect(BaseModel):
    """Computed canvas rectangle for guest video rendering."""
    x: float = Field(..., ge=0)
    y: float = Field(..., ge=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)


class GuestLayoutConfig(BaseModel):
    """Coach-controlled layout settings."""
    layout_mode: str = Field(default=GuestLayoutMode.PIP.value)
    pip_size: float = Field(default=PIP_SIZE_DEFAULT, ge=PIP_SIZE_MIN, le=PIP_SIZE_MAX)
    guest_rect: Optional[GuestCanvasRect] = None


class GuestAudioConfig(BaseModel):
    """Guest audio merge settings."""
    gain: float = Field(default=1.0, ge=0.0, le=2.0)
    muted: bool = Field(default=False)


class GuestJoinResult(BaseModel):
    """Top-level result wrapper for Guest Join operations."""
    success: bool = Field(...)
    invite: Optional[GuestInvite] = None
    session: Optional[GuestSessionRecord] = None
    layout: Optional[GuestLayoutConfig] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════
# FR-CA11-22 — Studio Stream Overlay & Trivianar Display
# DEP-ENG-122 through DEP-ENG-126 (corrected from spec-internal 098-102)
# Agent: Diego (Studio Overlay Operator)
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class OverlayState(str, Enum):
    """§4 Stage 1 Step 2: State machine states."""
    IDLE = "idle"
    QUESTION = "question"
    DISTRIBUTION = "distribution"
    LEADERBOARD = "leaderboard"
    WINNER = "winner"


class OverlayEventType(str, Enum):
    """§4 Stage 1 Step 3: WebSocket event types."""
    QUESTION_SENT = "question_sent"
    ANSWER_DISTRIBUTION = "answer_distribution"
    LEADERBOARD_UPDATED = "leaderboard_updated"
    WINNER_REVEAL = "winner_reveal"
    CLEAR = "clear"


class OverlayError(str, Enum):
    """Error types for Overlay."""
    INVALID_TRANSITION = "INVALID_TRANSITION"
    UNKNOWN_EVENT = "UNKNOWN_EVENT"
    MISSING_DATA = "MISSING_DATA"


# ── Constants ──────────────────────────────────────────────────────────

# §7 AC2: Countdown tolerance
COUNTDOWN_BAR_TOLERANCE_MS: int = 500

# §4 Stage 4: Leaderboard display
LEADERBOARD_DISPLAY_SIZE: int = 5
LEADERBOARD_AUTO_DISMISS_SECONDS: int = 5

# §4 Stage 5: Winner reveal timing
WINNER_HOLD_3RD_SECONDS: int = 2
WINNER_HOLD_2ND_SECONDS: int = 2
WINNER_HOLD_1ST_SECONDS: int = 3
WINNER_TOTAL_SECONDS: int = 8
CONFETTI_DURATION_SECONDS: int = 3

# Default overlay card background
OVERLAY_CARD_BG: str = "rgba(0,0,0,0.75)"

# Agent name
OVERLAY_AGENT_NAME: str = "Diego"


# ── Models ─────────────────────────────────────────────────────────────


class OverlayQuestionOption(BaseModel):
    """§5: Single answer option in question_sent event."""
    key: str = Field(..., min_length=1, max_length=1)
    text: str = Field(..., min_length=1)
    color: str = Field(default="#FFFFFF")


class OverlayQuestionEvent(BaseModel):
    """§5: question_sent WebSocket event payload."""
    question_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    options: list[OverlayQuestionOption] = Field(..., min_length=2)
    time_limit_seconds: int = Field(default=DEFAULT_TIME_LIMIT_SECONDS, gt=0)


class AnswerDistributionEntry(BaseModel):
    """§5: Single answer distribution entry."""
    count: int = Field(default=0, ge=0)
    percentage: float = Field(default=0.0, ge=0.0, le=100.0)


class OverlayDistributionEvent(BaseModel):
    """§5: answer_distribution WebSocket event payload."""
    question_id: str = Field(..., min_length=1)
    correct_answer: str = Field(..., min_length=1, max_length=1)
    distribution: dict[str, AnswerDistributionEntry] = Field(default_factory=dict)


class OverlayLeaderboardEntry(BaseModel):
    """§5: Single leaderboard entry for overlay panel."""
    rank: int = Field(..., ge=1)
    name: str = Field(default="")
    score: int = Field(default=0)
    change: str = Field(default="")


class OverlayLeaderboardEvent(BaseModel):
    """§5: leaderboard_updated WebSocket event payload."""
    top_5: list[OverlayLeaderboardEntry] = Field(default_factory=list)


class WinnerEntry(BaseModel):
    """§5: Single winner in reveal sequence."""
    rank: int = Field(..., ge=1, le=3)
    name: str = Field(..., min_length=1)
    score: int = Field(default=0)


class OverlayWinnerEvent(BaseModel):
    """§5: winner_reveal WebSocket event payload."""
    winners: list[WinnerEntry] = Field(..., min_length=1, max_length=3)


class OverlayBrandConfig(BaseModel):
    """DPA branding for overlay styling (FR-CA11-15)."""
    primary_color: str = Field(default="#2E86AB")
    accent_color: str = Field(default="#E74C3C")
    font_family: str = Field(default="Inter, sans-serif")
    card_bg: str = Field(default=OVERLAY_CARD_BG)


class OverlayResult(BaseModel):
    """Top-level result wrapper for Overlay operations."""
    success: bool = Field(...)
    state: str = Field(default=OverlayState.IDLE.value)
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# FR-CA11-16 — CCP Studio Block (Full Stack Recording & Streaming)
# Agent: Diego (Studio Session Conductor, Production Department)
# ══════════════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class RecordingMode(str, Enum):
    """6 recording modes supported by the Studio Block (§4 Stage 1 Step 2).

    Each mode constrains aspect ratio, resolution, and CMF pipeline template.
    """
    YOUTUBE_LONGFORM = "youtube_longform"
    SHORT_FORM_VERTICAL = "short_form_vertical"
    WEBINAR_VOD = "webinar_vod"
    COURSE_VIDEO = "course_video"
    LOOM_QUICK = "loom_quick"
    AFFINE_BROADCAST = "affine_broadcast"


class StudioSessionStatus(str, Enum):
    """Status progression for a studio session."""
    RECORDING = "recording"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"
    STREAMING = "streaming"
    BROADCASTING = "broadcasting"


class AspectRatio(str, Enum):
    """Supported canvas aspect ratios."""
    LANDSCAPE_16_9 = "16:9"
    PORTRAIT_9_16 = "9:16"


class Resolution(str, Enum):
    """Supported recording resolutions."""
    HD_1080P = "1080p"
    HD_720P = "720p"


class BroadcastState(str, Enum):
    """State of an AFFiNE broadcast session."""
    IDLE = "idle"
    SIGNALING = "signaling"
    ACTIVE = "active"
    RECONNECTING = "reconnecting"
    ENDED = "ended"
    FAILED_FALLBACK_HLS = "failed_fallback_hls"


# ── Constants ──────────────────────────────────────────────────────────

# Mode → CMF pipeline template mapping (§4 Stage 5 Step 4, AC7)
MODE_TEMPLATE_MAP: dict[RecordingMode, str] = {
    RecordingMode.YOUTUBE_LONGFORM: "youtube_longform",
    RecordingMode.SHORT_FORM_VERTICAL: "short_form_vertical",
    RecordingMode.WEBINAR_VOD: "webinar_vod",
    RecordingMode.COURSE_VIDEO: "course_video",
    RecordingMode.LOOM_QUICK: "loom_quick",
    RecordingMode.AFFINE_BROADCAST: "course_video",
}

# Mode → Aspect ratio constraint (§4 Stage 1 Step 4)
MODE_ASPECT_MAP: dict[RecordingMode, AspectRatio] = {
    RecordingMode.YOUTUBE_LONGFORM: AspectRatio.LANDSCAPE_16_9,
    RecordingMode.SHORT_FORM_VERTICAL: AspectRatio.PORTRAIT_9_16,
    RecordingMode.WEBINAR_VOD: AspectRatio.LANDSCAPE_16_9,
    RecordingMode.COURSE_VIDEO: AspectRatio.LANDSCAPE_16_9,
    RecordingMode.LOOM_QUICK: AspectRatio.LANDSCAPE_16_9,
    RecordingMode.AFFINE_BROADCAST: AspectRatio.LANDSCAPE_16_9,
}

# Mode → Allowed resolutions
MODE_RESOLUTION_MAP: dict[RecordingMode, list[Resolution]] = {
    RecordingMode.YOUTUBE_LONGFORM: [Resolution.HD_1080P, Resolution.HD_720P],
    RecordingMode.SHORT_FORM_VERTICAL: [Resolution.HD_1080P],
    RecordingMode.WEBINAR_VOD: [Resolution.HD_1080P, Resolution.HD_720P],
    RecordingMode.COURSE_VIDEO: [Resolution.HD_1080P, Resolution.HD_720P],
    RecordingMode.LOOM_QUICK: [Resolution.HD_1080P, Resolution.HD_720P],
    RecordingMode.AFFINE_BROADCAST: [Resolution.HD_1080P, Resolution.HD_720P],
}

# Canvas dimensions by resolution + aspect ratio
CANVAS_DIMENSIONS: dict[tuple[Resolution, AspectRatio], tuple[int, int]] = {
    (Resolution.HD_1080P, AspectRatio.LANDSCAPE_16_9): (1920, 1080),
    (Resolution.HD_720P, AspectRatio.LANDSCAPE_16_9): (1280, 720),
    (Resolution.HD_1080P, AspectRatio.PORTRAIT_9_16): (1080, 1920),
}

# Bitrate targets (§4 Stage 2 Step 3)
BITRATE_1080P: int = 8_000_000  # 8 Mbps
BITRATE_720P: int = 4_000_000   # 4 Mbps

# MediaRecorder timeslice (§4 Stage 2 Step 4)
CHUNK_TIMESLICE_MS: int = 1000

# S3 multipart minimum chunk (§4 Stage 5 Step 2)
S3_MULTIPART_CHUNK_BYTES: int = 5 * 1024 * 1024  # 5 MB

# Retry backoff schedule for S3 upload (§4 Stage 5 Step 2)
S3_UPLOAD_RETRY_BACKOFF: tuple[float, ...] = (2.0, 4.0, 8.0, 16.0)

# Codec preference order (§4 Stage 2 Step 3)
CODEC_PREFERENCE_ORDER: list[str] = [
    "video/webm;codecs=vp9,opus",
    "video/webm;codecs=vp8,opus",
    "video/mp4;codecs=avc1,mp4a.40.2",
]

# Teleprompter font size presets (§4 Stage 3 Step 4)
TELEPROMPTER_FONT_SIZES: list[int] = [18, 24, 32, 48]

# PiP (Picture-in-Picture) coordinates for canvas compositing (§4 Stage 2 Step 2)
PIP_WIDTH: int = 480
PIP_HEIGHT: int = 270
PIP_MARGIN: int = 40

# Receipt stage names
STUDIO_RECEIPT_STAGES: dict[str, str] = {
    "RECORDING_STARTED": "studio-recording-started",
    "UPLOAD_INITIATED": "studio-upload-initiated",
    "UPLOAD_COMPLETE": "studio-upload-complete",
    "CMF_TRIGGERED": "studio-cmf-triggered",
    "BROADCAST_STARTED": "studio-broadcast-started",
    "BROADCAST_ENDED": "studio-broadcast-ended",
}


# ── Models ─────────────────────────────────────────────────────────────


class StudioSessionRecord(BaseModel):
    """Primary output schema — §5 Studio Session Record.

    DEP-ENG-060 through DEP-ENG-070 data object.
    Stored in studio_sessions Supabase table.
    """
    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="UUID primary key for this studio session",
    )
    coach_id: str = Field(..., description="UUID of the coach")
    source_page_id: Optional[str] = Field(
        default=None,
        description="AFFiNE page UUID where /studio was invoked",
    )
    recording_mode: RecordingMode = Field(...)
    aspect_ratio: AspectRatio = Field(...)
    resolution: Resolution = Field(...)
    s3_recording_url: Optional[str] = Field(
        default=None,
        description="S3 URL for the raw recording file",
    )
    s3_vod_url: Optional[str] = Field(
        default=None,
        description="S3 URL for the processed VOD asset",
    )
    duration_seconds: Optional[int] = Field(
        default=None, ge=0,
        description="Total recording duration in seconds",
    )
    is_stream: bool = Field(
        default=False,
        description="True if session was a live stream (RTMP or broadcast)",
    )
    stream_destinations: list[str] = Field(
        default_factory=list,
        description="RTMP destination URLs for streaming sessions",
    )
    affine_broadcast_target_page_id: Optional[str] = Field(
        default=None,
        description="AFFiNE page UUID for broadcast target (affine_broadcast mode only)",
    )
    cmf_pipeline_template: Optional[str] = Field(
        default=None,
        description="CMF pipeline template name triggered on completion",
    )
    cmf_job_id: Optional[str] = Field(
        default=None,
        description="UUID of the triggered CMF job",
    )
    status: StudioSessionStatus = Field(
        default=StudioSessionStatus.RECORDING,
    )
    started_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of session start",
    )
    ended_at: Optional[str] = Field(
        default=None,
        description="ISO 8601 UTC timestamp of session end",
    )
    receipt_chain_guard: ReceiptChainGuardRef = Field(
        default_factory=ReceiptChainGuardRef,
        description="Receipt Chain Guard schema reference (DEP-ENG-041)",
    )


class BroadcastSignal(BaseModel):
    """WebRTC signaling payload for AFFiNE broadcast path.

    DEP-ENG-070: SDP Signaling Payload.
    Used by POST /studio/broadcast/signal endpoint.
    """
    session_id: str = Field(..., description="Studio session UUID")
    signal_type: str = Field(
        ...,
        description="Signal type: 'offer', 'answer', or 'candidate'",
    )
    sdp: Optional[str] = Field(
        default=None,
        description="SDP offer or answer string",
    )
    candidate: Optional[str] = Field(
        default=None,
        description="ICE candidate string",
    )
    target_page_id: str = Field(
        ...,
        description="AFFiNE page UUID that will receive the broadcast",
    )


class BroadcastStatePayload(BaseModel):
    """CRDT state payload injected into target AFFiNE page.

    DEP-ENG-067: AFFiNE Broadcast Router state.
    Written to the target page's Yjs document for viewer discovery.
    """
    session_id: str = Field(...)
    sfu_endpoint: str = Field(
        ...,
        description="WebRTC SFU endpoint URL (wss://sfu.ccf.internal)",
    )
    is_active: bool = Field(default=True)
    coach_name: str = Field(default="")
    hls_fallback_url: Optional[str] = Field(
        default=None,
        description="HLS .m3u8 fallback URL if WebRTC fails",
    )


class WorkspaceListPayload(BaseModel):
    """DEP-ENG-069: Hierarchical list of authorized broadcast target pages.

    Returned by GET /api/affine/workspaces for broadcast mode UI.
    """
    workspace_id: str = Field(...)
    workspace_name: str = Field(...)
    pages: list[dict[str, str]] = Field(
        default_factory=list,
        description="List of {page_id, page_title} dicts",
    )


class StudioUploadInitRequest(BaseModel):
    """Request payload for POST /studio/upload/init."""
    session_id: str = Field(...)
    coach_id: str = Field(...)
    recording_mode: RecordingMode = Field(...)
    resolution: Resolution = Field(...)
    aspect_ratio: AspectRatio = Field(...)


class StudioUploadInitResponse(BaseModel):
    """Response payload from POST /studio/upload/init."""
    upload_id: str = Field(..., description="S3 multipart upload ID")
    pre_signed_urls: list[str] = Field(
        ...,
        description="Array of pre-signed S3 PUT URLs for chunk upload",
    )
    s3_key: str = Field(
        ...,
        description="S3 object key for the final assembled file",
    )


class StudioCompleteRequest(BaseModel):
    """Request payload for POST /studio/complete."""
    session_id: str = Field(...)
    upload_id: str = Field(...)
    parts: list[dict[str, Any]] = Field(
        ...,
        description="Array of {PartNumber, ETag} from completed uploads",
    )
    duration_seconds: int = Field(..., ge=0)


class StudioSessionResult(BaseModel):
    """Top-level result wrapper for Studio operations."""
    success: bool = Field(...)
    session: Optional[StudioSessionRecord] = Field(default=None)
    error: Optional[str] = Field(default=None)
    cmf_job_id: Optional[str] = Field(default=None)