# FR-ERA3-39 — Phase-0 Campaign Frontend and Batch Intake Workspace Tech Spec

## §1 Files Read

### Core Prompt
- `docs/architecture/april_updates/spec_prompts/P0_S07_FR-ERA3-39_Phase0_Campaign_Frontend_And_Batch_Intake_Workspace.md`

### Source PRD Modules
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
- `docs/prd/modules/PRD_04_CVE_Experience_Design.md`

### Mandatory Phase-0 Source Set
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/ccp_biological_orchestration_model_v_1.md`
- `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`
- `docs/architecture/april_updates/spec_prompts/P0_S01_FR-ERA3-33_Phase0_Prospect_Intake_Console.md`
- `docs/architecture/april_updates/spec_prompts/P0_S02_FR-ERA3-34_Phase0_Prospect_Workspace_And_Artifact_Store.md`
- `docs/architecture/april_updates/spec_prompts/P0_S06_FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker.md`

### Existing Phase-0 Runtime Specs
- `docs/architecture/april_updates/FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-37_Phase0_Commercial_Bridge_And_Payment_Runtime_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker_Tech_Spec.md`

### Existing Backend / API / Model / Interface Files
- `src/ccp/api/main.py`
- `src/ccp/api/sacred_audio.py`
- `src/ccp/api/affine_studio_api.py`
- `src/ccp/core/receipt_chain.py`
- `src/ccp/models/ca11_models.py`
- `src/ccp/models/affine_broadcast_models.py`
- `src/ccp/models/commercial_ladder_models.py`
- `src/ccp/services/content_machine.py`
- `src/ccp/services/cmf_arc_governed_rendering.py`
- `src/ccp/services/payment_flow_orchestrator.py`
- `apps/challenge-arena/app/page.tsx`
- `apps/animation-studio/app/page.tsx`

### Existing Test Files
- `tests/integration/test_fr2_sacred_audio.py`
- `tests/integration/test_era3_fr10_anonymous_onboarding_flow.py`
- `tests/integration/test_com01_billing_integration.py`

### Pre-Work Log

#### Protocol and Structural Read
This spec follows the same Era-3 spec-writing discipline already used in the current wave:
- explicit pre-work evidence
- typed state ownership
- shared-runtime honesty
- UI surface built on real backend/state contracts instead of aesthetic-only description

#### Proof from `PRD-09`
`PRD-09` explicitly establishes the Trial Phase-0 flow and throughput target:

- `PRD-09`, line 1216:
  - `### 1.3A Trial Phase-0 Delivery Runtime`
- `PRD-09`, line 1217:
  - `Introduce a lightweight Trial Phase-0 delivery runtime that lets CCP ingest a prospect's existing material inside a shared pre-container workspace and output audits, previews, first-proof assets, and payment links within 24h max`
- `PRD-09`, line 1219:
  - `deliver up to 12 outreach packages per day`
- `PRD-09`, line 555:
  - `The product should not require the outreach operator to explain the whole system.`
- `PRD-09`, line 892:
  - `The commercial layer should preserve machine-readable state packets for each user or operator.`

These lines establish that the frontend must support:
- shared pre-container work
- machine-readable operator state
- 24h package movement
- operator leverage rather than operator burden

#### Proof from `PRD-01`
`PRD-01` establishes the two-surface command model:

- `PRD-01`, line 346:
  - `| AFFiNE Dashboard | Clean coach workspace — client cards, progress rings, streak flames, content delivery, red flag feed, intercept buttons |`
- `PRD-01`, line 347:
  - `| Telegram | ... payments |`
- `PRD-01`, line 349:
  - `There is no separate web portal, no mobile app, no content studio interface, no media factory dashboard.`
- `PRD-01`, line 369:
  - `It does not attempt to surface every metric or every option. It renders only the information required for the coach to take their next action`
- `PRD-01`, line 582:
  - `AFFiNE serves as the Sovereign Command Center for the coach`
- `PRD-01`, line 585:
  - `Complete "Invisible App" continuity`

These lines establish that the Phase-0 campaign frontend should behave like:
- a command workspace
- low cognitive load
- next-action first
- not an ornamental CRM

#### Proof from `PRD-04`
`PRD-04` establishes the experience constraints:

- `PRD-04`, line 46:
  - `CCP wins ... because the experience of using it feels unusually human, clear, low-friction`
- `PRD-04`, line 140:
  - `low-friction entry`
- `PRD-04`, line 141:
  - `clear next action`
- `PRD-04`, line 204:
  - `one obvious action`
- `PRD-04`, line 207:
  - `one clear next step`
- `PRD-04`, line 921:
  - `Friction Validator`
- `PRD-04`, line 1006:
  - `enforce one primary next action per state`

These lines establish the UX rule for this frontend:
- every row and state should expose one next useful action
- multi-step confusion is a design failure

#### Proof from Mandatory Phase-0 Source Set

From `Fladlien_Sales_Insights.md`:
- `A coach uploads or links content`
- `activation and download require payment`
- `Preview of Produced Assets`
- `The Affine Dashboard gives them full control over User Activity and Admin Activity`

From `ccp_biological_orchestration_model_v_1.md`:
- `DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation`
- `receipts and packets should begin preserving more of the DNA -> RNA -> phenotype lineage`

This matters because the campaign frontend belongs primarily at the `RNA / transcription` boundary and must preserve packet lineage across many coaches in one workspace.

From `CCP_System_Documentation.md`:
- `Zero-UI delivery`
- `Telegram as an invisible app`
- `Layer 6: Governance & Guardrails`
- `Layer 5: Orchestration (The Pi Coding Agent)`

This confirms that the frontend should be a thin command surface over a real orchestrated runtime, not a manual production room.

From `P0_S01` prompt:
- the intake console is a typed packet boundary for shared Phase-0 production

From `P0_S02` prompt:
- the workspace must support:
  - intake artifacts
  - audit artifacts
  - preview artifacts
  - produced proof assets
  - payment handoff artifacts
  - upgrade handoff metadata

From `P0_S06` prompt:
- the operator console must support:
  - queue visibility
  - readiness visibility
  - delivery status
  - 24h countdowns
  - missing-input alerts
  - payment-state visibility
  - upgrade-handoff visibility

The campaign frontend must therefore be the preparation and execution surface that feeds those operational views.

#### Existing Backend Signatures Verified

From `src/ccp/api/main.py`:
- `app.include_router(...)` pattern confirms the main environment already hosts many bounded surfaces under one FastAPI app

From `src/ccp/api/sacred_audio.py`:
- `@router.post("/sacred-audio/upload")`
- `@router.get("/sacred-audio/list/{coach_acronym}")`

From `src/ccp/api/affine_studio_api.py`:
- `@router.get("/affine/studio/dashboard/{coach_id}")`
- `@router.post("/affine/studio/broadcast-sessions")`
- `@router.post("/affine/studio/broadcast-sessions/{session_id}/launch")`

From `src/ccp/services/content_machine.py`:
- `async def process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`

From `src/ccp/services/cmf_arc_governed_rendering.py`:
- `def create_job(self, spine: CoalitionSpineInput) -> ArcRenderJobRecord`

From `src/ccp/services/payment_flow_orchestrator.py`:
- `async def initiate_upgrade(self, *, telegram_user_id: int, chat_id: int, coach_id: str, target_tier: PaymentTier) -> tuple[EligibilityCheckResult, InvoicePayload | None]`

These prove that:
- the main environment already supports many internal command surfaces
- upload, launch, queue, render, and payment flows already exist as callable bounded services
- Phase-0 should trigger these, not rebuild them

#### Existing Models Verified

From `ca11_models.py`:
- typed workspace, section, provisioning, sync, and delivery-target contracts already exist and provide a strong precedent for workspace-bound typed frontend state

From `affine_broadcast_models.py`:
- `BroadcastQueueItem`
- `DashboardSummary`
- `ClientCardProjection`
- `BroadcastLaunchRequest`

These are strong precedents for:
- queue rows
- summary boards
- card-based operational UI

From `commercial_ladder_models.py`:
- `CommercialLadderState`
- `TelegramInvoicePayload`
- `StealthCourseTransitionResponse`

These provide precedent for commercial-state-aware UI binding.

#### Existing Frontend / Interface Precedents

From `apps/challenge-arena/app/page.tsx`:
- simple composition pattern:
  - `SessionHeader`
  - `ProgressionRail`
  - `DailyRouteCard`

From `apps/animation-studio/app/page.tsx`:
- complex internal tool pattern with:
  - gate evaluation on boot
  - explicit fail/pass/legacy mode
  - top header
  - sidebar + center layout
  - export action
  - review notes

This matters because the Phase-0 campaign frontend is closer to an internal tool like Animation Studio than a public landing page. It needs:
- clear modes
- explicit readiness gating
- operational layout

#### Existing Test Patterns Verified

From `test_fr2_sacred_audio.py`:
- upload acceptance/rejection logic
- receipt chain integrity
- retry/drop patterns

From `test_era3_fr10_anonymous_onboarding_flow.py`:
- teaser-before-auth flow precedent

From billing integration tests:
- state transitions tied to payment are already a runtime concern

#### Existing Main-Environment Reuse Precedent Confirmed
The current CCP ecosystem already reuses one main app/runtime surface to host:
- onboarding
- challenge arena
- score viewer
- AFFiNE studio
- billing
- webhook flows
- render routes
- reaction routes

This confirms the Phase-0 campaign frontend should be another bounded internal surface in the main environment, not a justification to spin up a full per-coach container at this stage.

---

## §2 Overview

`FR-ERA3-39` defines the internal campaign frontend and batch intake workspace used to run Phase-0 outreach and proof-package generation in practice.

This surface is where operators:
- create or bind coaches by `coach_id`
- stage source materials
- bulk upload assets across many prospects
- organize files under shared namespaces
- see readiness at a glance
- trigger Phase-0 backend execution per coach or in batches
- hand off into review, payment, and continuity states

It is not:
- a marketing website
- a decorative dashboard
- a CRM clone
- a separate production stack

It is a production control surface for the Phase-0 machine.

### Core Job
The frontend must make the following operational loop fast:

1. create/bind coach row
2. attach or upload inputs
3. group files per coach/prospect packet
4. validate missing fields and readiness
5. select one or many ready rows
6. trigger shared backend pipeline execution
7. watch state change into audit/render/review/payment

### Human-Operator Objective
The surface should reduce the operator’s mental load to:
- who is ready
- who is blocked
- what is missing
- what should run next

Everything else belongs under the hood.

### Main-Environment Reuse Rule
This frontend assumes the same exact backend logic patterns already exist in the wider CCP ecosystem for:
- uploads
- packetization
- rendering
- scoring
- payment

The job of this surface is to coordinate those flows inside one shared Phase-0 environment rather than provisioning separate coach containers.

### UX Law
The frontend must obey:

> one obvious action per state, batch speed over decoration, and no hidden lineage loss.

---

## §3.1 DEP-IDs

### Primary Dependencies
- `DEP-FR-ERA3-33`
  - intake packet logic and readiness fields

- `DEP-FR-ERA3-34`
  - shared workspace and artifact-store substrate
  - not yet finalized as a tech spec in workspace at the time of writing

- `DEP-FR-ERA3-36`
  - execution request and delivery run ownership

- `DEP-FR-ERA3-38`
  - operator queue / status semantics

### Supporting Dependencies
- `DEP-FASTAPI-MAIN`
  - route registration and app hosting precedent

- `DEP-SACRED-UPLOAD`
  - upload and file persistence precedent

- `DEP-AFFINE-STUDIO`
  - internal dashboard/queue/control surface precedent

- `DEP-PAYMENT-FLOW`
  - later payment state visibility hooks

### Future Dependencies
- `DEP-FR-ERA3-40`
  - batch execution review and approval board

### Dependency Rule
The frontend may:
- read and stage inputs
- invoke intake and execution APIs
- show readiness and run states
- allow retry/trigger actions through approved backend endpoints

The frontend may not:
- directly mutate delivery/commercial truth without backend confirmation
- bypass packet validation
- invent its own artifact lineage state

---

## §3.2 Backend

### Runtime Position
The campaign frontend sits above:
- intake packet creation
- workspace/artifact binding
- shared delivery orchestration
- operator queue state

It is the launchpad surface for Phase-0 work.

### Existing Backend Patterns To Reuse

#### 1. `src/ccp/api/main.py`
Use:
- route registration discipline
- bounded sub-surface approach

This frontend should likely become another router family under `/api/phase0/...`.

#### 2. `src/ccp/api/sacred_audio.py`
Use:
- drag/drop upload semantics mapped to backend file writes
- coach-bound validation
- local/shared path persistence
- receipt logging

#### 3. `src/ccp/api/affine_studio_api.py`
Use:
- dashboard fetch pattern
- create queue item pattern
- launch action pattern
- health/readiness route pattern

#### 4. `src/ccp/services/content_machine.py`
Use:
- session processing as reusable content compilation backend

#### 5. `src/ccp/services/cmf_arc_governed_rendering.py`
Use:
- render job creation backend

#### 6. `src/ccp/services/payment_flow_orchestrator.py`
Use:
- payment visibility / continuity handoff status later in the same workspace row

### Recommended Implementation Roots
- `src/ccp/models/phase0_campaign_frontend_models.py`
- `src/ccp/services/phase0_campaign_workspace_service.py`
- `src/ccp/api/routes/phase0_campaign_workspace.py`
- `apps/phase0-campaign-workspace/` or equivalent internal app surface

### Recommended Internal Backend Endpoints
- `GET /api/phase0/workspace`
- `POST /api/phase0/workspace/coach-bind`
- `POST /api/phase0/workspace/upload`
- `POST /api/phase0/workspace/batch-upload`
- `POST /api/phase0/workspace/execute`
- `GET /api/phase0/workspace/{phase0_packet_id}`
- `GET /api/phase0/workspace/health`

### Shared Namespace Law
All coach rows in this frontend must resolve to shared-environment namespaces built from:
- `coach_id`
- `phase0_packet_id`
- `delivery_run_id`

This gives separation without container sprawl.

---

## §3.3 Frontend / Workspace Artifacts

This section defines the canonical frontend concepts.

### Required Workspace Concepts

#### 1. Campaign Workspace
The top-level surface listing many coach/prospect rows in one batch-working session.

#### 2. Coach Row
A row or card representing one active Phase-0 prospect package preparation unit.

#### 3. Coach Binding
The relationship between:
- internal prospect row
- bound `coach_id`
- packet namespace

#### 4. Batch Upload Session
A single operator action set where many files are staged and attached across one or many coach rows.

#### 5. Readiness Summary
Compact per-row summary of:
- ready
- blocked
- partial
- missing data

#### 6. Execution Request
The structured trigger sent from this frontend into the delivery/runtime backend.

#### 7. Workspace Filter State
The current operator filter/sort state for fast queue handling.

#### 8. Bulk Attachment Result
The structured result of multi-file upload/grouping across one or many coach rows.

### Core Visible Frontend Regions

#### Header Bar
Shows:
- workspace title
- active batch count
- ready count
- blocked count
- execute-selected CTA

#### Filter Rail
Quick filters for:
- all
- ready
- missing inputs
- running
- delivered awaiting payment
- paid/unlocked

#### Coach Grid / Table
Each row shows:
- coach/prospect name
- `coach_id`
- attached asset counts
- readiness chip
- delivery state chip
- payment state chip
- next action button

#### Bulk Dropzone
Supports:
- drag/drop upload
- file selection
- coach-targeted attachment
- auto grouping hints

#### Detail Drawer / Panel
Shows:
- grouped files
- captions
- audience
- BI attachment
- missing inputs
- packet IDs
- last receipt / status

### Batch-Speed Requirement
The operator must be able to:
- stage multiple prospects in one session
- drag and drop a mixed file set
- quickly assign or reassign files to coach rows
- launch selected ready rows in a few actions

This is more important than generic dashboard beauty.

---

## §3.4 Governance Constraints

### G1. Main-Environment-Reuse Rule
The frontend must reuse the shared CCP backend runtime.

### G2. Coach-ID-Bound Intake Rule
Every row must bind to a stable `coach_id` or a provisional-to-final binding path.

### G3. Batch-Speed Rule
The workspace must optimize for many rows and repeated uploads, not single-form perfection only.

### G4. Shared-Workspace-First Rule
The frontend must assume shared namespaces, not per-coach dedicated runtime environments.

### G5. No-Full-Container-Before-Payment Rule
The frontend must not expose or require container provisioning actions at Phase 0.

### G6. Human-Operator-Leverage Rule
The operator should not need to repeat the same metadata steps manually for every row when the system can infer grouping safely.

### G7. Artifact-Lineage Preservation Rule
Bulk work must never destroy traceability of which file belongs to which packet/coach row.

### G8. Readiness-At-A-Glance Rule
Operators must be able to identify blocked vs ready rows instantly.

### G9. One Primary Action Per Row State
Do not expose a cluttered row action matrix.

### G10. No Decorative CRM Drift
This surface is for production control, not relationship notes theater.

---

## §3.5 Technical Decisions

### TD1. Use a Hybrid Table/Card Workspace
Decision:
- rows should support dense scanning, but expandable detail should expose richer packet context

Reason:
- batch speed plus enough context for fixing blocked rows

### TD2. Support Bulk Upload Sessions as First-Class Objects
Decision:
- represent batch upload attempts structurally

Reason:
- needed for multi-coach drag/drop traceability
- easier retries and debugging

### TD3. Keep Readiness Summary Separate from Delivery State
Decision:
- row readiness and pipeline execution state are not the same

Reason:
- a row can be intake-ready but not yet executed

### TD4. Trigger Backend Execution Through Typed Requests
Decision:
- frontend execution uses canonical request objects

Reason:
- avoids ad hoc launch payloads

### TD5. Preserve Provisional Coach Binding
Decision:
- allow provisional rows before full final `coach_id` normalization when needed, but require resolution before execution

Reason:
- supports fast staging

### TD6. Use Shared Artifact Paths with Coach-Bound Subgrouping
Decision:
- keep one workspace root with namespaced row folders

Reason:
- shared runtime economics
- later migration possible

### TD7. Mirror AFFiNE / Internal Tool Composition Style
Decision:
- use a lean internal app layout with clear panels and status bands

Reason:
- matches existing internal tool ergonomics more than public-app patterns

---

## §4 Plan

### Phase 1. Models and Namespace Foundations
1. Create `Phase0CampaignWorkspace`
2. Create `Phase0CoachRow`
3. Create `Phase0CoachBinding`
4. Create `Phase0BatchUploadSession`
5. Create `Phase0ReadinessSummary`
6. Create `Phase0ExecutionRequest`
7. Create `Phase0WorkspaceFilterState`
8. Create `Phase0BulkAttachmentResult`

### Phase 2. Backend Workspace Services
9. Build workspace-list aggregation service
10. Build coach-binding service
11. Build bulk-upload grouping service
12. Build readiness recomputation service

### Phase 3. Frontend Surface
13. Create campaign workspace app surface
14. Build header metrics strip
15. Build filter rail
16. Build coach table/grid rows
17. Build detail drawer
18. Build drag/drop staging panel

### Phase 4. Execution Triggers
19. Add per-row execute action
20. Add multi-select execute action
21. Add disabled-state logic for blocked rows
22. Add execution confirmation and status transitions

### Phase 5. Status and Payment Visibility
23. Bind row states to operator-console and commercial state views
24. Surface payment state and unlock state in the same row
25. Surface upgrade handoff indicators

### Phase 6. Reliability and Throughput
26. Add receipt-backed upload/result history
27. Add failed upload recovery
28. Add mis-grouped file reassignment flow
29. Test 12-row active batch interaction

---

## §5 Schema

### Enum: `Phase0CoachRowState`
- `DRAFT`
- `BOUND_UNREADY`
- `READY_TO_EXECUTE`
- `RUNNING`
- `REVIEW_REQUIRED`
- `DELIVERED_AWAITING_PAYMENT`
- `PAID_UNLOCKED`
- `UPGRADED`
- `FAILED`

### Pydantic Model: `Phase0CoachBinding`
```python
class Phase0CoachBinding(BaseModel):
    binding_id: str
    provisional_label: str | None = None
    coach_id: str
    coach_acronym: str | None = None
    binding_state: Literal["PROVISIONAL", "RESOLVED", "INVALID"]
    created_at_utc: datetime
    resolved_at_utc: datetime | None = None
```

### Pydantic Model: `Phase0ReadinessSummary`
```python
class Phase0ReadinessSummary(BaseModel):
    phase0_packet_id: str | None = None
    ready: bool
    missing_required_fields: list[str] = Field(default_factory=list)
    attached_file_count: int = Field(ge=0)
    grouped_file_count: int = Field(ge=0)
    audit_target_count: int = Field(ge=0)
    audience_present: bool
    business_intelligence_present: bool
    last_checked_at_utc: datetime
```

### Pydantic Model: `Phase0CoachRow`
```python
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
    phase0_packet_id: str | None = None
    delivery_run_id: str | None = None
    payment_state_label: str = ""
    next_action: str
    updated_at_utc: datetime
```

### Pydantic Model: `Phase0BatchUploadSession`
```python
class Phase0BatchUploadSession(BaseModel):
    batch_upload_session_id: str
    workspace_id: str
    initiated_by_operator_id: str
    attached_file_names: list[str] = Field(default_factory=list)
    target_row_ids: list[str] = Field(default_factory=list)
    total_file_count: int = Field(ge=0)
    completed_at_utc: datetime | None = None
    created_at_utc: datetime
```

### Pydantic Model: `Phase0BulkAttachmentResult`
```python
class Phase0BulkAttachmentResult(BaseModel):
    batch_upload_session_id: str
    attached_count: int = Field(ge=0)
    failed_count: int = Field(ge=0)
    row_attachment_counts: dict[str, int] = Field(default_factory=dict)
    unresolved_files: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
```

### Pydantic Model: `Phase0ExecutionRequest`
```python
class Phase0ExecutionRequest(BaseModel):
    request_id: str
    workspace_id: str
    row_ids: list[str] = Field(min_length=1)
    phase0_packet_ids: list[str] = Field(min_length=1)
    triggered_by_operator_id: str
    execution_mode: Literal["SINGLE", "BATCH"]
    require_review_gate: bool = True
    created_at_utc: datetime
```

### Pydantic Model: `Phase0WorkspaceFilterState`
```python
class Phase0WorkspaceFilterState(BaseModel):
    readiness_filter: Literal["ALL", "READY", "BLOCKED", "PARTIAL"] = "ALL"
    delivery_filter: Literal["ALL", "NOT_STARTED", "RUNNING", "REVIEW", "DELIVERED"] = "ALL"
    payment_filter: Literal["ALL", "UNPAID", "PAID", "UPGRADED"] = "ALL"
    search_query: str = ""
    sort_key: Literal["UPDATED", "READY_FIRST", "NAME", "PAYMENT_STATE"] = "UPDATED"
```

### Pydantic Model: `Phase0CampaignWorkspace`
```python
class Phase0CampaignWorkspace(BaseModel):
    workspace_id: str
    title: str
    operator_id: str
    rows: list[Phase0CoachRow] = Field(default_factory=list)
    filter_state: Phase0WorkspaceFilterState
    selected_row_ids: list[str] = Field(default_factory=list)
    active_batch_upload_session_id: str | None = None
    generated_at_utc: datetime
```

### Auxiliary Model: `Phase0WorkspaceHealth`
```python
class Phase0WorkspaceHealth(BaseModel):
    workspace_id: str
    intake_api_ready: bool
    delivery_api_ready: bool
    commercial_api_ready: bool
    receipt_chain_ready: bool
    shared_storage_ready: bool
    checked_at_utc: datetime
```

---

## §6 Fallback

### F1. Upload Grouping Ambiguity
If the system cannot confidently assign files to a row:
- keep them unresolved
- do not guess silently
- require operator assignment

### F2. Provisional Coach Binding Unresolved
If a row remains provisional:
- allow staging
- block execution
- highlight required binding action

### F3. Shared Storage Failure
If shared storage write fails:
- no file attachment should appear as successful
- emit failed attachment results
- preserve operator-visible warning

### F4. Backend Execution Trigger Failure
If an execution request fails at trigger time:
- keep row state unchanged or move to explicit `FAILED`
- do not mark `RUNNING`

### F5. Filter/State Load Failure
If workspace aggregation partially fails:
- show rows that can be resolved
- show health/degradation banner
- preserve retry action

### F6. Missing Packet ID for Ready Row
If a row appears ready but no packet ID exists:
- block execution
- mark inconsistency
- alert for packet regeneration

### F7. Payment State Not Yet Known
If delivery is complete but payment state is unavailable:
- use explicit label `PAYMENT_STATE_PENDING_SYNC`
- do not guess unpaid/paid

---

## §7 Tasks

### T1. Create `phase0_campaign_frontend_models.py`
Define all canonical models from this spec.

### T2. Create `phase0_campaign_workspace_service.py`
Implement workspace aggregation and row-state synthesis.

### T3. Add coach-binding endpoints
Support create/bind/update validation.

### T4. Add batch upload endpoint
Support multi-file upload and grouping.

### T5. Add shared attachment persistence layer
Write artifacts into shared namespaced paths.

### T6. Add readiness recomputation endpoint
Update readiness after upload or field change.

### T7. Add per-row execution endpoint
Run one coach/prospect packet through shared runtime.

### T8. Add batch execution endpoint
Run many selected rows through shared runtime.

### T9. Add workspace query endpoint
Return workspace rows and filter state.

### T10. Add workspace health endpoint
Show dependency readiness for operators.

### T11. Build frontend app shell
Header, filters, grid/table, detail drawer.

### T12. Build drag/drop upload region
Support mixed file sets and coach-targeted grouping.

### T13. Build row-level next-action logic
One primary CTA per row state.

### T14. Build selection and batch-action logic
Enable multi-select execute only for valid rows.

### T15. Bind commercial labels
Show payment/unlock/upgrade states in the row.

### T16. Add tests
Upload, grouping, binding, readiness, execution trigger, and filter behavior.

---

## §8 AC

### AC1
An operator can create or bind many coach rows in one workspace session.

### AC2
The frontend supports drag/drop upload and standard file-pick upload.

### AC3
The frontend can stage multiple coaches in the same session without assuming separate containers.

### AC4
Files are grouped per coach row with preserved lineage.

### AC5
Each row exposes readiness-at-a-glance.

### AC6
A ready row can trigger the shared Phase-0 backend pipeline.

### AC7
Multiple selected ready rows can trigger batch execution.

### AC8
Filters can narrow by readiness, delivery state, and payment state.

### AC9
The frontend can show payment-related state without becoming a billing app.

### AC10
The frontend can survive ambiguous file assignment without silently corrupting lineage.

### FAILURE EXAMPLE
Bad behavior that must be rejected:
- operator drops 20 files for 5 coaches
- frontend guesses several attachments incorrectly
- rows appear ready
- batch execution runs on the wrong file groupings
- artifact lineage is lost

This is a hard failure because it breaks:
- coach-id-bound intake
- shared-workspace safety
- batch throughput trust
- and downstream audit/render validity

---

## §9 Dependencies

### Confirmed Present in Workspace
- FastAPI main environment app
- upload endpoint precedent
- AFFiNE studio API precedent
- receipt chain
- queue/dashboard model precedents
- Phase-0 intake, delivery, commercial, and operator specs

### Not Yet Finalized but Assumed
- `FR-ERA3-34` tech spec for shared workspace/artifact store is not yet present in workspace at the time of writing

This spec therefore treats storage and namespace laws as a required dependency boundary rather than pretending final implementation already exists.

### Future Integration
This frontend should later pair tightly with:
- `FR-ERA3-40` review and approval board
- `FR-ERA3-34` shared workspace substrate

---

## §10 Testing

### Unit Tests
- coach binding validation
- row-state resolver
- readiness summary computation
- filter-state application
- batch-upload result aggregation

### Integration Tests
- create row -> upload files -> readiness recompute
- provisional bind -> resolve coach_id -> ready to execute
- single-row execution request
- multi-row batch execution request
- payment-state label propagation

### Failure Tests
- unsupported files rejected correctly
- unresolved files remain unresolved
- storage write failure surfaces warning
- execution trigger failure does not fake running state
- missing packet ID blocks execution

### Throughput Tests
- workspace can render and interact with at least 12 active rows
- mixed ready/blocked/running rows remain filterable
- multi-select execution only includes valid rows

### UX Regression Tests
- each row state exposes one primary next action
- no critical friction dead end exists after upload
- blocked rows show actionable missing-state explanation

### Build Notes and Future Integration
This surface should feel like:
- an internal command workspace
- a batch staging room
- a fast control panel

It should not feel like:
- a CRM
- a client-facing dashboard
- or a pseudo-container orchestration terminal

Its job is simple:
- stage
- bind
- validate
- launch
- and keep lineage intact while the shared Phase-0 runtime does the heavy work.
