# Tech-Spec: FR-ERA3-07 - AFFiNE Studio Block Orchestration
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 4 - Pipelines & Engines
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms all new endpoints must extend `src/ccp/api/main.py`, Section 2.3
                      confirms schema work extends `src/ccp/scripts/setup_supabase.py`, Section 3 requires
                      direct mapping to existing services before introducing new ones, and the protocol's CBAR
                      note requires mandates to be declared explicitly in Section 3 rather than implied.
2. PRD LOADED:        PRD-01 exact FR definition: "AFFiNE Dashboard | Clean coach workspace — client cards,
                      progress rings, streak flames, content delivery, red flag feed, intercept buttons."
                      PRD-01 Section 6.3 also states: "The coach's dashboard follows a Lean Cognitive Load
                      mandate… It renders only the information required for the coach to take their next action:"
                      including Client Card, Progress Ring, Streak Flame, Conviction Score, Mood Indicator,
                      Red Flag Feed, and Intercept Button. PRD-07 governance rule: "Operators should be able to
                      inspect: generated structure, proof sources, hook families, extraction markers, and rep
                      score history inside the AFFiNE or operator review layer. This is important for governance.
                      The system should not become a black box that emits webinars no one can audit."
3. EPIC LOADED:       Phase 4 exact FR line: "FR-ERA3-07 (AFFiNE Studio Block Orchestration): The sovereign
                      command center allowing coaches to control and broadcast programs, review scorecards, and
                      intervene natively (PRD-01, PRD-04, PRD-07)." Story 1.1 first AC: "Given I log into the
                      AFFiNE command center, When I view the Client Card, Then I see the visual completion arc,
                      streak flame, composite Conviction Score, and Red Flag Feed, And each red flag entry
                      includes a qualitative diagnostic excerpt (e.g., "Client paused for 4 seconds after
                      mentioning pricing" or a transcription snippet of the flagged moment), And the intercept
                      voice recorder remains locked until I explicitly confirm review of the diagnostic excerpt."
4. CBAR LOADED:       Phase4-M01 confirmed from the Phase 4 CBAR audit. Exact rewrite demand: the Red Flag Feed
                      must include a qualitative transcription excerpt or diagnostic summary, and the UI must
                      enforce review before the intercept recorder unlocks. The hallucination purge also warns
                      against invented primitive IDs, especially false `EXP-TRB-*` references.
5. PRIMITIVES:        `experience_primitive_id: "EXP-PER-003"` / `canonical_name: "Cumulative Investment"`
                      `experience_primitive_id: "EXP-FBK-004"` / `canonical_name: "Bring the Data Forward"`
6. BACKEND:           `src/ccp/services/affine_sync.py` - `async def push_telemetry(self, payload: TelemetryPushPayload, workspace_id: Optional[str] = None) -> SyncResult`
                      `src/ccp/services/affine_sync.py` - `async def push_session(self, payload: SessionPushPayload, workspace_id: Optional[str] = None) -> SyncResult`
                      `src/ccp/services/affine_workspace_provisioner.py` - `def provision_coach_workspace(self, coach_soul: dict[str, Any], business_summary: dict[str, Any], coach_config: Optional[dict[str, Any]] = None) -> ProvisioningResult`
                      `src/ccp/services/affine_client_workspace.py` - `async def provision_client_workspace(self, client_id: str, coach_id: str, program_id: str, coach_theme_file: str, coping_position: int = 0, atlas_week: int = 0, capacity_track: str = "Foundation") -> ClientProvisioningResult`
                      `src/ccp/services/cross_system_intelligence_service.py` - `def run_sunday_bot_meeting(self, *, client_data: list[dict[str, Any]], period_start: Optional[str] = None, period_end: Optional[str] = None) -> Optional[SundayBotMeetingPayload]`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use scenario-oriented fixtures,
                      helper builders, direct typed assertions, schema constant checks, and focused integration
                      cases instead of generic smoke tests. Section 10 follows that pattern.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P4_S21_FR-ERA3-07_AFFiNE_Broadcasting_Pipeline.md` | 2026-05-11 | Assignment prompt, hard mandate, output path, and required backend audit |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Required backend mapping, schema extension points, and CBAR formatting rules |
| 3 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Epic 1 story text, FR line, acceptance criteria, and Canonical Mandate #1 |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | CBAR rewrite demand and hallucination purge for Phase 4 |
| 5 | `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` | v6.0, 2026-05-06 | Dual-interface architecture, AFFiNE dashboard definition, and Lean Cognitive Load rules |
| 6 | `docs/prd/modules/PRD_07_V2WS_Webinar.md` | v6.0, 2026-05-06 | Operator governance, AFFiNE broadcasting boundary, and auditability constraints |
| 7 | `primitives/experience/personalization_identity/EXP-PER-003.yaml` | Codified registry | Verified primary primitive for ownership and cumulative investment |
| 8 | `primitives/experience/feedback_scoring/EXP-FBK-004.yaml` | Codified registry | Verified supporting primitive for surfacing evidence instead of opaque alerts |
| 9 | `src/ccp/services/affine_sync.py` | Existing service | AFFiNE transport, idempotent create/update flow, telemetry/session section writes |
| 10 | `src/ccp/services/affine_workspace_provisioner.py` | Existing service | Coach workspace provisioning, root section template, and workspace registration |
| 11 | `src/ccp/services/affine_client_workspace.py` | Existing service | Client workspace provisioning, content unlock flow, and coach-client workspace linkage |
| 12 | `src/ccp/services/cross_system_intelligence_service.py` | Existing service | Coach-scoped client progress aggregation and Sunday Bot Meeting synthesis |
| 13 | `src/ccp/services/studio_block_service.py` | Existing service | Existing Studio Block session and stream orchestration boundary |
| 14 | `src/ccp/services/v2ws_interactive_service.py` | Existing service | Existing approval and step-lock precedent for gated operator workflows |
| 15 | `src/ccp/models/ca11_models.py` | Existing models | AFFiNE section constants and push payload shapes |
| 16 | `src/ccp/models/cross_system_models.py` | Existing models | `SBMAggregationMetrics`, `SBMStrategicSynthesis`, and `SundayBotMeetingPayload` |
| 17 | `src/ccp/api/main.py` | 1.0.0 | FastAPI extension point for new AFFiNE orchestration routes |
| 18 | `src/ccp/core/receipt_chain.py` | Current | Immutable decision logging for review, unlock, intercept, and broadcast actions |
| 19 | `src/ccp/core/circuit_breaker.py` | Current | Guarded fallback and integrity halt layer |
| 20 | `src/ccp/scripts/setup_supabase.py` | Current | Canonical PostgreSQL schema bootstrap extension point |
| 21 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Pattern reference for payload-centric integration tests |
| 22 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Pattern reference for orchestration, constants, and async service tests |

## 2. Overview

### 2.1 Problem Statement

The codebase already has AFFiNE workspace provisioning, AFFiNE sync transport, client workspace provisioning, and cross-system intelligence aggregation. What it still lacks is the actual sovereign orchestration layer that turns those backend pieces into an operator-ready command center.

Without that layer, the coach-facing AFFiNE surface stays structurally present but behaviorally incomplete:

- client progress exists in backend systems but not as a deterministic Client Card projection
- red flags can drift into abstract labels like `Low Confidence` rather than showing the exact moment that matters
- intercept actions can be launched without proof that the operator reviewed the triggering evidence
- broadcast controls can become detached from the same review surface that governs intervention

That is exactly the failure Epic 1 is preventing. The operator must be able to review meaningful evidence, take the next action quickly, and remain inside AFFiNE rather than switching to external dashboards or black-box automation layers.

### 2.2 Solution

This spec adds a dedicated AFFiNE orchestration layer inside the existing coach workspace, centered on the `command_center` root section and backed by the already-provisioned `client_intelligence_hub` plus existing session/push infrastructure.

The new layer introduces five missing capabilities:

- `ClientCardProjectionService` to build the lean dashboard card for each client
- `RedFlagExcerptAssembler` to convert numeric and behavioral signals into qualitative evidence-backed entries
- `InterceptReviewGateService` to enforce Phase4-M01 before the recorder unlocks
- `OperatorInterceptSessionService` to create, track, and audit intercept sessions
- `AFFiNEStudioOrchestrationService` to unify dashboard reads, review actions, and Studio Block launch actions

The result is not a new workspace system. It is a deterministic orchestration slice on top of the existing AFFiNE substrate, with explicit evidence gating and full receipt logging.

### 2.3 Scope

**In scope:**

- AFFiNE command center dashboard payloads for client cards
- qualitative Red Flag Feed assembly from client intelligence and session evidence
- explicit review acknowledgement state before intercept unlock
- intercept session creation, locking, unlock, launch, and audit trail
- AFFiNE-to-Studio-Block launch routing from the same operator surface
- coach workspace isolation, ownership validation, and receipt logging
- Supabase schema for projection rows, review acknowledgements, and intercept session records
- API routes for dashboard reads, flag review, intercept launch, and broadcast launch

**Out of scope:**

- replacing `AFFiNEWorkspaceProvisioner` or redefining the eight root workspace sections
- replacing `AFFiNESyncService` as the transport into AFFiNE
- replacing `ClientWorkspaceProvisioner` as the client-content unlock engine
- inventing a new scoring engine for Conviction Score or biometrics
- building the Telegram audience companion surface covered by separate webinar specs
- supporting generic broadcast starts that bypass dashboard review and receipts
- full standalone dashboard analytics views for the `EXP-FBK-004` primitive (only used here as a supporting inference for actionable Red Flag contexts)

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-AFF-001 | `DashboardSummary` | FR-ERA3-07 | Top-level payload representing the command center dashboard for the operator |
| DEP-AFF-002 | `ClientCardProjection` | Story 1.1 | Projected visual state of a client including progress arc, streak, and scores |
| DEP-AFF-003 | `ProgressArcSnapshot` | FR-ERA3-07 | Normalized progress metrics aggregated from cross-system intelligence and telemetry |
| DEP-AFF-004 | `RedFlagFeedEntry` | Story 1.1 / M-01 | Actionable alert entry containing qualitative evidence and gate status |
| DEP-AFF-005 | `DiagnosticExcerpt` | Story 1.1 | Qualitative snippet, rationale, and source evidence required for intercept review |
| DEP-AFF-006 | `ReviewAcknowledgementRequest` | Phase4-M01 | Payload submitted by the operator to acknowledge excerpt review and unlock the gate |
| DEP-AFF-007 | `ReviewAcknowledgementRecord` | Phase4-M01 | Persisted durable record proving the operator reviewed the explicit excerpt hash |
| DEP-AFF-008 | `InterceptStartRequest` | FR-ERA3-07 | Payload requesting the launch of a new intercept session |
| DEP-AFF-009 | `InterceptSessionRecord` | Story 1.1 | Durable state and lifecycle boundaries of an active or completed intercept |
| DEP-AFF-010 | `BroadcastQueueItem` | PRD-07 | Projected state of a pending or active studio broadcast session |
| DEP-AFF-011 | `BroadcastLaunchRequest` | FR-ERA3-07 | Payload requesting the start or resumption of a broadcast program |
| DEP-AFF-012 | `BroadcastLaunchResult` | FR-ERA3-07 | Result containing session identifiers, status, and launch receipt |
| DEP-AFF-013 | `EvidencePointer` | Story 1.1 | Strict mapping to the upstream session and workspace entry that triggered the flag |
| DEP-AFF-014 | `ConvictionScoreBreakdown` | FR-ERA3-07 | The composite conviction metric projected for the lean cognitive dashboard |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `affine_sync.py` | `src/ccp/services/affine_sync.py` | Reuses `push_telemetry(...)` and `push_session(...)` to keep the AFFiNE-facing workspace sections current. This spec does not create a parallel sync stack. |
| `affine_workspace_provisioner.py` | `src/ccp/services/affine_workspace_provisioner.py` | Extends the existing coach workspace model. The AFFiNE orchestration UI lives inside the existing provisioned workspace and its `command_center` / `client_intelligence_hub` structure. |
| `affine_client_workspace.py` | `src/ccp/services/affine_client_workspace.py` | Provides authoritative coach-client workspace linkage and client workspace URLs used by client cards and operator deep links. |
| `cross_system_intelligence_service.py` | `src/ccp/services/cross_system_intelligence_service.py` | Supplies coach-scoped progress synthesis. `run_sunday_bot_meeting(...)` and related aggregation helpers are used as evidence inputs, not as UI payloads directly. |
| `studio_block_service.py` | `src/ccp/services/studio_block_service.py` | Existing Studio Block session creation and stream-start behavior are reused for operator broadcast actions initiated from AFFiNE. |
| `v2ws_interactive_service.py` | `src/ccp/services/v2ws_interactive_service.py` | Existing approval-gate precedent informs the explicit lock state machine for intercept review. |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `WorkspaceSectionType.CLIENT_INTELLIGENCE_HUB`, existing payload vocabulary, and coach workspace semantics. |
| `cross_system_models.py` | `src/ccp/models/cross_system_models.py` | Reuses `SBMAggregationMetrics`, `SBMStrategicSynthesis`, and `SundayBotMeetingPayload` as typed upstream structures for aggregation and synthesis. |
| `main.py` | `src/ccp/api/main.py` | Registers the orchestration router and extends `/health` with dashboard dependency readiness. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Adds deterministic schema for dashboard projections, flag evidence, review acknowledgements, and intercept sessions. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Records immutable decisions for dashboard review, excerpt acknowledgement, intercept launch, broadcast launch, and failure fallback. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Stops launch or unlock actions when evidence integrity, workspace isolation, or downstream service health fails. |

**Existing AFFiNE sections and stores consumed:**

- `command_center` for the operator-facing orchestration landing view
- `client_intelligence_hub` for synchronized telemetry and client intelligence entries
- `session_archive` for referenced session evidence rows already written by `push_session(...)`

**New data stores introduced by this spec:**

- `affine_client_card_projections`
- `affine_red_flag_evidence`
- `affine_intercept_review_acks`
- `affine_intercept_sessions`
- `affine_broadcast_queue`

**New API routes introduced by this spec:**

- `GET /api/affine/studio/dashboard/{coach_id}`
- `GET /api/affine/studio/client-card/{coach_id}/{client_id}`
- `POST /api/affine/studio/red-flags/{flag_id}/review`
- `POST /api/affine/studio/red-flags/{flag_id}/start-intercept`
- `GET /api/affine/studio/intercepts/{intercept_id}`
- `POST /api/affine/studio/broadcast-sessions`
- `POST /api/affine/studio/broadcast-sessions/{session_id}/launch`
- `GET /api/affine/studio/health/{coach_id}`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-PER-003` | Cumulative Investment | personalization_identity | The operator must see evidence that feels specific to the actual client journey. Client cards, progress arcs, and intercept recommendations must point back to accumulated behavioral evidence rather than generic AI labels. |
| `EXP-FBK-004` | Bring the Data Forward | feedback_scoring | Red Flag Feed entries must surface interpretable evidence, not abstract scores alone. This is a supporting primitive inference used to keep the dashboard explanatory and action-oriented. |

### 3.4 CBAR Mandates

| Mandate | Story | Required Behavior | Implementation Mechanism |
|---|---|---|---|
| Phase4-M01 - Intelligence-Gated Intercept Rule | Epic 1 Story 1.1 | Intercept recorder remains locked until the operator explicitly confirms review of the diagnostic excerpt that triggered the flag. | `InterceptReviewGateService` stores a durable acknowledgement row keyed by `flag_id`, `coach_id`, `client_id`, and `reviewed_excerpt_hash`. `OperatorInterceptSessionService` refuses to create or unlock a recorder session unless that acknowledgement exists and matches the current excerpt revision. |

**M-01 anti-patterns explicitly forbidden:**

- no Red Flag Feed row may contain only numeric labels such as `Low Confidence 0.32`
- opening a flag drawer does not count as review acknowledgement
- hovering, previewing, or scrolling does not unlock the recorder
- a stale acknowledgement for an older excerpt revision does not unlock a newer flagged event
- operators cannot deep-link directly to recorder start and bypass the review route

### 3.5 Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| Workspace surface | Reuse existing coach AFFiNE workspace | `AFFiNEWorkspaceProvisioner` already creates the command center. Replacing it would duplicate working infrastructure. |
| Dashboard data source | Projection-first | AFFiNE should read prepared dashboard payloads, not recompute synthesis on every page render. |
| Evidence format | Qualitative excerpt plus typed metadata | This is the only way to satisfy Story 1.1 and make the operator action legible. |
| Gate persistence | Durable Supabase ack row | Unlock state must survive refreshes and remain auditable. |
| Broadcast launch path | Route through existing Studio Block service | The orchestration surface chooses and launches sessions; it does not replace the Studio Block engine. |
| Score handling | Display composite score only, never raw unframed internals | PRD-01 requires lean cognitive load. The operator needs the composite and evidence, not raw metric dumps. |
| Fallback rule | Hard-lock when excerpt integrity is missing | Allowing generic intercepts would violate the core mandate. |
| Sync strategy | Use existing AFFiNE section pushes plus local projection tables | AFFiNE pages stay current while the API can still serve a deterministic dashboard payload quickly. |
| Projection Updates | Async background worker triggered by `CrossSystemIntelligenceService` events | Projections must not drift from the canonical source. The dashboard API reads instantly; the background worker computes and updates the projection rows when upstream intelligence signals change. |

## 4. Plan

### Phase 1 - Data and Model Foundation

| Task # | Task | Output |
|---|---|---|
| 1 | Create `src/ccp/models/affine_broadcast_models.py` | Typed enums and Pydantic v2 models for dashboard, flags, acknowledgements, intercepts, and broadcast sessions |
| 2 | Extend `src/ccp/scripts/setup_supabase.py` | New tables, indexes, uniqueness constraints, and RLS policy hooks |
| 3 | Add projection SQL helpers | Insert/update logic for client cards, flag evidence, and review acknowledgements. Must include the async background worker handler that updates `affine_client_card_projections` when triggered by `CrossSystemIntelligenceService` events. |

### Phase 2 - Evidence Projection and Gating

| Task # | Task | Output |
|---|---|---|
| 4 | Implement `CrossSystemProgressAdapter` | Typed normalized progress snapshot from cross-system intelligence plus AFFiNE telemetry rows |
| 5 | Implement `ClientCardProjectionService` | Visual completion arc, streak flame, conviction score, mood summary, CTA state |
| 6 | Implement `DiagnosticExcerptEvidenceResolver` | Transcript snippet, pause pattern, source session pointer, and excerpt hash |
| 7 | Implement `RedFlagExcerptAssembler` | Ranked Red Flag Feed rows with severity, rationale, and excerpt metadata |
| 8 | Implement `InterceptReviewGateService` | Review-ack write/read, excerpt hash validation, and state transitions |

### Phase 3 - Operator Actions and Studio Launch

| Task # | Task | Output |
|---|---|---|
| 9 | Implement `OperatorInterceptSessionService` | Locked/ready/recording/completed intercept lifecycle |
| 10 | Implement `StudioBlockLaunchBridge` | Create or attach studio sessions from AFFiNE dashboard actions |
| 11 | Implement `BroadcastQueueProjector` | Lean active/pending program control list for AFFiNE command center |
| 12 | Implement `AFFiNEStudioOrchestrationService` | Single orchestration facade consumed by API routes |

### Phase 4 - API, AFFiNE Binding, and Receipts

| Task # | Task | Output |
|---|---|---|
| 13 | Extend `src/ccp/api/main.py` with router registration | New orchestration endpoints available through FastAPI |
| 14 | Add `CommandCenterApiRouter` module | Dashboard, review, intercept, broadcast, and health routes |
| 15 | Add receipt events for review/unlock/start/launch/fallback | Immutable audit chain for operator actions |

### Phase 5 - Verification and Hardening

| Task # | Task | Output |
|---|---|---|
| 16 | Add unit tests for projection and gate logic | Deterministic model and service verification |
| 17 | Add integration tests for lock/unlock behavior and workspace isolation | Story 1.1 and M-01 enforcement coverage |
| 18 | Add health/fallback checks | Dependency-readiness and degraded-mode behavior coverage |

## 5. Schema

**New model file:** `src/ccp/models/affine_broadcast_models.py`

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class RedFlagSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class DiagnosticExcerptSource(str, Enum):
    transcript_snippet = "transcript_snippet"
    pause_pattern = "pause_pattern"
    scoring_evidence = "scoring_evidence"
    session_summary = "session_summary"


class InterceptGateStatus(str, Enum):
    locked = "locked"
    ready = "ready"
    recording = "recording"
    completed = "completed"
    blocked = "blocked"


class BroadcastSessionStatus(str, Enum):
    draft = "draft"
    queued = "queued"
    ready = "ready"
    live = "live"
    completed = "completed"
    failed = "failed"


class EvidencePointer(BaseModel):
    session_id: str = Field(..., min_length=1)
    asset_id: str = Field(..., min_length=1)
    workspace_section: str = Field(..., min_length=1)
    workspace_entry_id: str = Field(..., min_length=1)


class ConvictionScoreBreakdown(BaseModel):
    composite_score: float = Field(..., ge=0.0, le=100.0)


class ProgressArcSnapshot(BaseModel):
    completion_percent: float = Field(..., ge=0.0, le=100.0)
    current_program_step: str = Field(..., min_length=1)
    streak_days: int = Field(..., ge=0)
    mood_indicator: str = Field(..., min_length=1)
    next_required_action: str = Field(..., min_length=1)


class DiagnosticExcerpt(BaseModel):
    excerpt_id: str = Field(..., min_length=1)
    source_type: DiagnosticExcerptSource
    display_excerpt: str = Field(..., min_length=8, max_length=500)
    rationale: str = Field(..., min_length=8, max_length=300)
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    evidence_pointer: EvidencePointer
    flagged_at: datetime
    confidence_label: str = Field(..., min_length=1)


class RedFlagFeedEntry(BaseModel):
    flag_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    severity: RedFlagSeverity
    flag_title: str = Field(..., min_length=3, max_length=120)
    flag_summary: str = Field(..., min_length=8, max_length=240)
    excerpt: DiagnosticExcerpt
    gate_status: InterceptGateStatus = Field(default=InterceptGateStatus.locked)
    created_at: datetime


class ClientCardProjection(BaseModel):
    projection_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    client_display_name: str = Field(..., min_length=1, max_length=120)
    client_workspace_url: HttpUrl
    progress_arc: ProgressArcSnapshot
    conviction: ConvictionScoreBreakdown
    red_flags: list[RedFlagFeedEntry] = Field(default_factory=list)
    primary_cta: str = Field(..., min_length=1, max_length=80)
    updated_at: datetime


class BroadcastQueueItem(BaseModel):
    broadcast_session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    program_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=160)
    status: BroadcastSessionStatus
    planned_start_at: datetime | None = None
    studio_session_id: str = Field(default="", max_length=120)
    audience_surface: str = Field(..., min_length=1, max_length=80)


class DashboardSummary(BaseModel):
    coach_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    generated_at: datetime
    client_cards: list[ClientCardProjection] = Field(default_factory=list)
    broadcast_queue: list[BroadcastQueueItem] = Field(default_factory=list)


class ReviewAcknowledgementRequest(BaseModel):
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    acknowledgement_phrase: str = Field(
        ...,
        pattern=r"^I have reviewed this$",
    )


class ReviewAcknowledgementRecord(BaseModel):
    acknowledgement_id: str = Field(..., min_length=1)
    flag_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    acknowledged_at: datetime
    gate_status_after_ack: InterceptGateStatus = Field(
        default=InterceptGateStatus.ready
    )


class InterceptStartRequest(BaseModel):
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    flag_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)


class InterceptSessionRecord(BaseModel):
    intercept_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    flag_id: str = Field(..., min_length=1)
    gate_status: InterceptGateStatus
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    recorder_session_id: str = Field(default="", max_length=120)
    workspace_id: str = Field(..., min_length=1)


class BroadcastLaunchRequest(BaseModel):
    coach_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    program_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=160)
    target_surface: str = Field(..., min_length=1, max_length=80)


class BroadcastLaunchResult(BaseModel):
    broadcast_session_id: str = Field(..., min_length=1)
    studio_session_id: str = Field(..., min_length=1)
    status: BroadcastSessionStatus
    launch_receipt_id: str = Field(..., min_length=1)
```

**Supabase tables to add in `setup_supabase.py`:**

| Table | Key Columns | Constraints |
|---|---|---|
| `affine_client_card_projections` | `projection_id`, `coach_id`, `client_id`, `workspace_id`, `projection_json`, `updated_at` | unique(`coach_id`, `client_id`), index on `coach_id`, JSON payload must store current `ClientCardProjection` |
| `affine_red_flag_evidence` | `flag_id`, `coach_id`, `client_id`, `severity`, `excerpt_hash`, `excerpt_text`, `source_type`, `session_id`, `asset_id`, `workspace_entry_id`, `created_at` | unique(`flag_id`), index on `coach_id`, index on `client_id`, index on `excerpt_hash` |
| `affine_intercept_review_acks` | `acknowledgement_id`, `flag_id`, `coach_id`, `client_id`, `excerpt_hash`, `ack_phrase`, `acknowledged_at` | unique(`flag_id`, `coach_id`, `excerpt_hash`), enforce exact ack phrase, index on `acknowledged_at` |
| `affine_intercept_sessions` | `intercept_id`, `flag_id`, `coach_id`, `client_id`, `workspace_id`, `recorder_session_id`, `gate_status`, `started_at`, `completed_at` | unique active session per `flag_id`, check gate status enum, index on `coach_id` |
| `affine_broadcast_queue` | `broadcast_session_id`, `coach_id`, `workspace_id`, `program_id`, `studio_session_id`, `status`, `planned_start_at`, `created_at` | index on `coach_id`, index on `status`, unique(`coach_id`, `program_id`, `status`) for active statuses |

**Required route behavior contracts:**

- `GET /api/affine/studio/dashboard/{coach_id}` returns `DashboardSummary`
- `POST /api/affine/studio/red-flags/{flag_id}/review` accepts `ReviewAcknowledgementRequest` and returns `ReviewAcknowledgementRecord`
- `POST /api/affine/studio/red-flags/{flag_id}/start-intercept` accepts `InterceptStartRequest` and returns `InterceptSessionRecord`
- `POST /api/affine/studio/broadcast-sessions/{session_id}/launch` accepts `BroadcastLaunchRequest` and returns `BroadcastLaunchResult`

**State machine for Phase4-M01:**

| Current State | Event | Next State | Allowed |
|---|---|---|---|
| `locked` | dashboard view | `locked` | yes |
| `locked` | excerpt opened | `locked` | yes |
| `locked` | review acknowledgement persisted | `ready` | yes |
| `locked` | start intercept requested | `blocked` | no - return 409 and reason `EXCERPT_REVIEW_REQUIRED` |
| `ready` | start intercept requested | `recording` | yes |
| `ready` | excerpt revision changes | `locked` | yes |
| `recording` | recorder completes | `completed` | yes |
| `recording` | workspace mismatch detected | `blocked` | yes |

## 6. Fallback

| Failure | Detection | Operator Experience | System Action |
|---|---|---|---|
| AFFiNE API unavailable | `AFFiNESyncService.health_check()` false or create/update exception | Dashboard still loads last successful projection with stale badge; no new launch actions allowed | Serve cached projections, pause projection refresh, write failure receipt |
| Cross-system intelligence unavailable | `CrossSystemProgressAdapter` cannot build fresh synthesis | Existing projections remain visible; cards show `fresh intelligence unavailable` note | Do not recompute conviction deltas from missing aggregate data; use last successful snapshot |
| Excerpt evidence missing | `RedFlagExcerptAssembler` cannot resolve transcript/pause/session evidence | Red flag row is suppressed from actionable feed; no intercept button rendered | Write `FLAG_SUPPRESSED_NO_QUALITATIVE_EVIDENCE` receipt and keep gate locked |
| Review acknowledgement stale | current `excerpt_hash` does not match stored ack | Operator sees `Review again to unlock` | Reset gate to `locked`, keep prior ack for audit only |
| Workspace ownership mismatch | `WorkspaceOwnershipGuard` fails | Request rejected | Return 403, write security receipt, do not expose payload |
| Recorder or Studio Block downstream failure | launch bridge error | Operator sees retryable failure with preserved context | Session remains `ready` or `queued`, no silent status promotion |

**Hard-stop rules:**

- If there is no qualitative excerpt, the system must not fall back to generic intercept text.
- If acknowledgement persistence fails, the UI must remain locked even if the operator clicked the confirmation button.
- If workspace ownership cannot be validated, no partial payload may be returned.

## 7. Tasks

1. Create [src/ccp/models/affine_broadcast_models.py](D:/Work/The Conscious Coaching Factory/src/ccp/models/affine_broadcast_models.py) with the typed models and enums defined in Section 5.
2. Extend [src/ccp/scripts/setup_supabase.py](D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with SQL DDL for the five new tables, indexes, and uniqueness constraints.
3. Add `AFFiNEDashboardRepository` in [src/ccp/services/](D:/Work/The Conscious Coaching Factory/src/ccp/services/) to read and write projection rows.
4. Add `CrossSystemProgressAdapter` to normalize `SundayBotMeetingPayload`, AFFiNE telemetry snapshots, and client workspace linkage into one per-client summary.
5. Add `ClientCardProjectionService` to compute progress arc, streak flame, composite conviction projection, mood label, and CTA state.
6. Add `DiagnosticExcerptEvidenceResolver` to resolve transcript snippets, pause summaries, and section entry references from session evidence.
7. Add `RedFlagExcerptAssembler` to rank and shape actionable flag entries with excerpt hashes and severity.
8. Add `InterceptReviewGateService` to persist the exact acknowledgement phrase and compute gate state transitions.
9. Add `OperatorInterceptSessionService` to create intercept sessions only after a valid acknowledgement exists.
10. Add `StudioBlockLaunchBridge` to route AFFiNE broadcast actions into existing Studio Block session APIs.
11. Add `BroadcastQueueProjector` so the AFFiNE command center can show pending and live sessions without opening another tool.
12. Add `AFFiNEStudioOrchestrationService` as the main orchestration facade.
13. Add a new FastAPI router module under [src/ccp/api/](D:/Work/The Conscious Coaching Factory/src/ccp/api/) for the Section 3.2 routes.
14. Register the router and health dependency checks in [src/ccp/api/main.py](D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
15. Extend [src/ccp/core/receipt_chain.py](D:/Work/The Conscious Coaching Factory/src/ccp/core/receipt_chain.py) integration calls so review, unlock, intercept, broadcast, and suppression actions are immutable.
16. Add unit tests for projection, excerpt assembly, and gate transitions.
17. Add integration tests for M-01 lock enforcement, qualitative excerpt payloads, and workspace mismatch rejection.
18. Verify all new route payloads use Pydantic v2 models with no `Any`.

## 8. Acceptance Criteria

### Story 1.1 - Operator Intervention and Dashboard Review

**AC1 - Lean Client Card Projection**

- Given a coach opens the AFFiNE command center
- When the dashboard payload is loaded for a valid workspace they own
- Then each client card includes `completion_percent`, `streak_days`, `composite_score`, `mood_indicator`, and a next action CTA
- And the card does not expose raw metric internals as the default primary view

**AC2 - Qualitative Red Flag Feed**

- Given a client has a red flag-worthy event
- When the Red Flag Feed is assembled
- Then each actionable entry includes a qualitative excerpt such as a transcript snippet or pause-pattern summary
- And the entry includes a stable `excerpt_hash`, `session_id`, and evidence pointer
- And no actionable row is emitted if only a numeric label exists

**AC3 - Mandatory Review Before Unlock**

- Given a flag is visible on the client card
- When the operator has not yet submitted the exact acknowledgement phrase
- Then the intercept recorder state remains `locked`
- And any `start-intercept` request returns `409 EXCERPT_REVIEW_REQUIRED`

**AC4 - Ack Creates a Narrow Unlock**

- Given the operator explicitly submits `I have reviewed this`
- When the `excerpt_hash` matches the currently displayed evidence
- Then the gate transitions from `locked` to `ready`
- And only that specific `flag_id` for that specific `coach_id` and `client_id` is unlocked

**AC5 - Stale Evidence Relocks**

- Given an acknowledgement already exists
- When the underlying excerpt changes and a new `excerpt_hash` is produced
- Then the gate returns to `locked`
- And the operator must review the new evidence before recording

**AC6 - AFFiNE-to-Studio Launch Consistency**

- Given the operator launches a broadcast session from the AFFiNE command center
- When the workspace is valid and downstream Studio Block services are healthy
- Then the session is created or resumed through the existing Studio Block boundary
- And the launch action is recorded in `receipt_chain`
- And the operator stays within the same orchestrated AFFiNE control model rather than switching to an unmanaged launch path

**Failure Example**

- A dashboard card shows `Low Confidence 0.31` with a bright red intercept button.
- The operator clicks `Record Intercept` without ever seeing a transcript snippet, pause explanation, or acknowledgement step.
- The system starts a recorder session immediately.
- This is a spec failure. It violates Story 1.1, Phase4-M01, the Lean Cognitive Load doctrine, and the qualitative-evidence requirement from the CBAR audit.

**Mandate Proof**

- Phase4-M01 is satisfied only if the unlock condition depends on a persisted acknowledgement of the specific current excerpt hash.
- Merely opening the flag detail panel, viewing a hovercard, or loading the dashboard does not satisfy the mandate.

## 9. Dependencies

| Dependency | Type | Why It Matters |
|---|---|---|
| `src/ccp/services/affine_sync.py` | Existing service | Required to keep AFFiNE sections synchronized and to reuse existing ownership-aware sync behavior |
| `src/ccp/services/affine_workspace_provisioner.py` | Existing service | Provides the command center workspace shell this feature depends on |
| `src/ccp/services/affine_client_workspace.py` | Existing service | Supplies client workspace mapping and deep-link targets |
| `src/ccp/services/cross_system_intelligence_service.py` | Existing service | Supplies aggregated progress and strategy evidence used in client card projection |
| `src/ccp/services/studio_block_service.py` | Existing service | Required for broadcast orchestration and session launch |
| `src/ccp/models/ca11_models.py` | Existing models | Existing AFFiNE workspace constants and payload semantics |
| `src/ccp/models/cross_system_models.py` | Existing models | Existing intelligence payload types and synthesis containers |
| `src/ccp/api/main.py` | Existing API gateway | Required registration point for new routes |
| `src/ccp/scripts/setup_supabase.py` | Existing schema bootstrap | Required to create durable persistence for projections and acknowledgements |
| `src/ccp/core/receipt_chain.py` | Cross-system infrastructure | Required for immutable review and launch auditability |
| `src/ccp/core/circuit_breaker.py` | Cross-system infrastructure | Required to halt unsafe unlock and launch paths |
| AFFiNE workspace availability | External platform dependency | Dashboard surface cannot refresh live data without it |
| Supabase RLS configuration | Data security dependency | Coach-scoped workspace isolation depends on correct policies |

## 10. Testing Strategy

### Unit Tests

| Test Name | File | What It Verifies |
|---|---|---|
| `test_client_card_projection_builds_visual_completion_arc_and_cta` | `tests/unit/test_affine_studio_orchestration.py` | `ClientCardProjectionService` emits the lean client card fields required by Story 1.1 |
| `test_red_flag_excerpt_assembler_suppresses_numeric_only_alerts` | `tests/unit/test_affine_studio_orchestration.py` | `RedFlagExcerptAssembler` refuses to create actionable flags without qualitative evidence |
| `test_intercept_review_gate_requires_exact_phrase_and_hash_match` | `tests/unit/test_affine_studio_orchestration.py` | `InterceptReviewGateService` only unlocks on exact phrase plus current `excerpt_hash` |
| `test_intercept_gate_relocks_when_excerpt_revision_changes` | `tests/unit/test_affine_studio_orchestration.py` | stale acknowledgements are invalidated correctly |

### Integration Tests

| Test Name | File | What It Verifies |
|---|---|---|
| `test_dashboard_payload_contains_qualitative_red_flag_excerpt` | `tests/integration/test_affine_fr_era3_07_studio_orchestration.py` | full route payload contains transcript/pause excerpt, evidence pointer, and lock state |
| `test_start_intercept_rejected_until_review_ack_is_persisted` | `tests/integration/test_affine_fr_era3_07_studio_orchestration.py` | `POST /start-intercept` returns 409 before ack and succeeds after ack |
| `test_workspace_mismatch_blocks_dashboard_and_launch_actions` | `tests/integration/test_affine_fr_era3_07_studio_orchestration.py` | ownership validation prevents cross-tenant reads and starts |
| `test_broadcast_launch_reuses_existing_studio_block_boundary` | `tests/integration/test_affine_fr_era3_07_studio_orchestration.py` | AFFiNE launch path creates or resumes a valid Studio Block session and records receipts |

### Test Pattern Notes

- Mirror the scenario-style structure used in `test_cpsc_fr52_webinar_brief.py` and `test_ca11_fr16_studio_block.py`.
- Prefer helper builders for client card inputs, red-flag evidence rows, and session launch payloads.
- Assert concrete field values and status transitions rather than only checking `200 OK`.
- Include direct assertions on `excerpt_hash`, `gate_status`, `workspace_id`, and `receipt action` names.

### Minimum Verification Bar Before Merge

- all unit tests in the new orchestration module pass
- all new integration tests pass
- `GET /health` reports orchestration dependency readiness
- stale acknowledgements are proven to relock the recorder
- at least one integration test proves numeric-only flags are suppressed instead of exposed
