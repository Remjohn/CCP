# FR-ERA3-38 — Phase-0 Operator Console and SLA Tracker Tech Spec

## §1 Files Read

### Core Prompt
- `docs/architecture/april_updates/spec_prompts/P0_S06_FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker.md`

### Source PRD Modules
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`

### Mandatory Phase-0 Source Set
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/ccp_biological_orchestration_model_v_1.md`
- `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`

### Existing Phase-0 Runtime Specs
- `docs/architecture/april_updates/FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-37_Phase0_Commercial_Bridge_And_Payment_Runtime_Tech_Spec.md`

### Existing Backend / State / Queue Files
- `src/ccp/core/receipt_chain.py`
- `src/ccp/services/campaign_orchestrator.py`
- `src/ccp/services/affine_studio_orchestration.py`
- `src/ccp/api/billing_api.py`
- `src/ccp/models/affine_broadcast_models.py`
- `src/ccp/models/commercial_ladder_models.py`

### Existing Integration Test Files
- `tests/integration/test_era3_fr10_anonymous_onboarding_flow.py`
- `tests/integration/test_fr2_sacred_audio.py`
- `tests/integration/test_com01_billing_integration.py`
- `tests/integration/test_com01_billing_middleware.py`

### Pre-Work Log

#### Protocol and Structure
This spec follows the same Era-3 spec pattern now established across the workspace:
- explicit pre-work evidence
- real dependency acknowledgement
- typed state ownership
- runtime interoperability instead of detached tooling

#### Proof from `PRD-09`
`PRD-09` now explicitly establishes the existence and purpose of Phase-0 operations:

- `PRD-09`, line 1216:
  - `### 1.3A Trial Phase-0 Delivery Runtime`
- `PRD-09`, line 1217:
  - `Introduce a lightweight Trial Phase-0 delivery runtime that lets CCP ingest a prospect's existing material inside a shared pre-container workspace and output audits, previews, first-proof assets, and payment links within 24h max`
- `PRD-09`, line 1219:
  - `deliver up to 12 outreach packages per day`
- `PRD-09`, line 892:
  - `The commercial layer should preserve machine-readable state packets for each user or operator.`
- `PRD-09`, line 954:
  - `### 8.8 Operator Review Layer`
- `PRD-09`, line 958:
  - `An operator should be able to review:`
- `PRD-09`, line 987:
  - `For churches and operators, dashboards should surface:`
- `PRD-09`, line 1027:
  - `The system should surface different scoreboards for different operator types.`

These lines establish:
- operator visibility is required
- machine-readable state is required
- dashboards/scoreboards are required
- 24h Phase-0 readiness is required

#### Proof from `PRD-01`
`PRD-01` establishes the platform surfaces and lean dashboard doctrine:

- `PRD-01`, line 346:
  - `| AFFiNE Dashboard | Clean coach workspace — client cards, progress rings, streak flames, content delivery, red flag feed, intercept buttons |`
- `PRD-01`, line 347:
  - `| Telegram | ... payments |`
- `PRD-01`, line 349:
  - `There is no separate web portal, no mobile app, no content studio interface, no media factory dashboard.`
- `PRD-01`, line 367:
  - `### 6.3 The AFFiNE Dashboard — Lean Cognitive Load`
- `PRD-01`, line 369:
  - `It does not attempt to surface every metric or every option. It renders only the information required for the coach to take their next action`
- `PRD-01`, line 582:
  - `AFFiNE serves as the Sovereign Command Center for the coach`
- `PRD-01`, line 585:
  - `Complete "Invisible App" continuity`

These lines establish:
- the operator console should feel like a lean command surface
- it should not become a bloated generic project manager
- it should sit on top of the real runtime packets and queues

#### Proof from Mandatory Phase-0 Source Set

From `Fladlien_Sales_Insights.md`:
- `The Benchmark Tool can sit there passively, scoring everything they produce`
- `Preview only, activation gated`
- `First activation event: explainers, cinematic proof, audit, and spread objects`
- `The Affine Dashboard gives them full control over User Activity and Admin Activity`

From `ccp_biological_orchestration_model_v_1.md`:
- `DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation`
- `receipts and packets should begin preserving more of the DNA -> RNA -> phenotype lineage`
- `downgrade / quarantine / review rules`

This matters because the operator console should visualize:
- where a Phase-0 packet sits in the runtime organism
- where it is blocked
- what review or downgrade state exists

From `CCP_System_Documentation.md`:
- `Zero-UI delivery`
- `Telegram as an invisible app`
- `The internal runtime organism is better described as DNA / truth -> RNA / transcription -> force -> delivery -> variation -> phenotype -> evaluation`
- `Layer 6: Governance & Guardrails ... Receipt Chain Guard`

This confirms that:
- the operator console is not an ornamental UI
- it is a governance and recovery surface over a real state machine

#### Existing Backend Signatures Verified

From `receipt_chain.py`:
- `def log(...) -> ReceiptEntry`
- `def query(...) -> list[ReceiptEntry]`
- `def get_provenance(self, asset_id: str) -> list[ReceiptEntry]`

From `campaign_orchestrator.py`:
- `def launch(...) -> CampaignExecutionLogRow`
- contains `CampaignStateResolver` and `CampaignInitializationGate`

From `affine_studio_orchestration.py`:
- `def build_snapshot(self, *, client_id: str, coach_id: str) -> dict`
- `def build_card(self, *, client_id: str, coach_id: str, display_name: str = "Client") -> ClientCardProjection`
- `def assemble(self, *, coach_id: str, client_id: str, signals: list[dict]) -> list[RedFlagFeedEntry]`

These show:
- queue/state models already exist in adjacent surfaces
- card/queue/dashboard summary patterns already exist
- receipt querying is already a real system capability

#### Existing Models Verified

From `affine_broadcast_models.py`:
- `BroadcastSessionStatus`
- `BroadcastQueueItem`
- `DashboardSummary`
- `RedFlagFeedEntry`
- `InterceptSessionRecord`

From `commercial_ladder_models.py`:
- `CommercialLadderState`
- `StealthCourseTransitionRequest`
- `TelegramInvoicePayload`
- `StealthCourseUpgradeReceipt`

These give real design precedents for:
- queue items
- summary boards
- operational status enums
- payment-visibility states

#### Existing Test Patterns Verified

From `test_era3_fr10_anonymous_onboarding_flow.py`:
- teaser-before-auth flow is expected

From `test_fr2_sacred_audio.py`:
- receipt chain integrity
- silent rejection and gentle recovery
- persistent failure and drop-after-retries patterns

From billing tests:
- payment status and gating states already matter to internal flow correctness

#### Existing Failure-Recovery Patterns Confirmed
The current architecture already uses:
- fail-closed gates
- non-blocking receipt sync fallback
- retryable states
- graceful degradation
- operator-visible blocked conditions

The Phase-0 operator console should inherit those patterns rather than invent new failure semantics.

---

## §2 Overview

`FR-ERA3-38` defines the internal operator console and SLA tracker for the shared Phase-0 delivery machine.

Its purpose is to make the Phase-0 engine operable at the target throughput of up to `12 packages/day` without:
- bespoke PM software
- manual spreadsheet juggling
- hidden state
- invisible failures
- or commercial drift between delivery and payment

The console must sit on top of:
- intake packet state
- delivery run state
- audit state
- render state
- preview/review state
- commercial bridge state
- receipt trails

It is not a replacement for those systems.
It is the internal visibility and recovery layer over them.

### Minimum Operator Questions It Must Answer
For every Phase-0 package, the operator must be able to answer:
- did intake complete?
- what is still missing?
- is audit running?
- are render jobs blocked or active?
- is operator review required right now?
- is the package ready to deliver?
- was it delivered but not yet paid?
- did payment happen?
- did unlock propagate?
- was continuity offered or consumed?
- how much SLA time remains?
- what requires intervention first?

### Surface Philosophy
This console must follow the same lean-cognitive-load law as the AFFiNE dashboard:
- one screen can show many packages
- each package exposes the next useful action
- alert severity is obvious
- operators do not need to read logs first to know what matters

### Core Runtime Law
The operator console obeys this law:

> show state early, highlight blockers before churn, and make recovery faster than confusion.

---

## §3.1 DEP-IDs

### Primary Dependencies
- `DEP-FR-ERA3-33`
  - intake state and packet readiness

- `DEP-FR-ERA3-36`
  - delivery plan, run, step results, receipts, output bundle

- `DEP-FR-ERA3-37`
  - commercial bridge state, payment readiness, unlock status, credit bridge state

### Supporting Dependencies
- `DEP-RECEIPT-CHAIN`
  - append-only provenance queries

- `DEP-AFFINE-PATTERNS`
  - dashboard/queue/card view patterns from `affine_broadcast_models.py`

- `DEP-BILLING-STATE`
  - billing and payment visibility from existing billing/payment models

### Future Dependencies
- `DEP-FR-ERA3-39`
  - campaign frontend and batch intake workspace

- `DEP-FR-ERA3-40`
  - batch review and approval board

### Dependency Rule
The operator console is strictly a state-aggregation surface.
It may:
- read runtime states
- aggregate queue health
- compute alerts and SLA state
- initiate approved retry/escalation actions

It may not:
- bypass downstream runtime rules
- directly mutate truth-critical payloads without audit trails
- fake completion or clear blockers without receipts

---

## §3.2 Backend

### Runtime Position
The operator console backend sits above the shared Phase-0 runtime and below the AFFiNE-facing or internal admin-facing surface.

It should aggregate from:
- prospect intake store
- delivery orchestrator state
- commercial bridge state
- receipt chain
- optional render-job adapters

### Existing Backend Patterns To Reuse

#### 1. `receipt_chain.py`
Use:
- append-only receipts
- provenance query patterns
- asset/run-level trace lookups

#### 2. `campaign_orchestrator.py`
Use:
- gate-based status reasoning
- explicit queue state modeling
- operator-only launch constraints

#### 3. `affine_studio_orchestration.py`
Use:
- dashboard summary assembly
- card projection style
- red-flag feed semantics
- next-action centric view logic

#### 4. `billing_api.py` and commercial state files
Use:
- payment/billing status visibility
- unlock-state awareness

### Recommended Implementation Roots
- `src/ccp/models/phase0_operator_console_models.py`
- `src/ccp/services/phase0_operator_console_service.py`
- `src/ccp/services/phase0_sla_tracker.py`
- `src/ccp/api/routes/phase0_operator_console.py`
- `tests/services/test_phase0_operator_console.py`

### Recommended Aggregation Inputs
- `Phase0ProspectPacket`
- `Phase0DeliveryPlan`
- `Phase0DeliveryRun`
- `Phase0OutputBundle`
- `Phase0CommercialState`
- `Phase0EntitlementState`
- relevant receipts

### Operator-Action Boundaries
Allowed console actions:
- refresh state
- retry a failed run segment
- mark missing input requested
- mark review completed
- escalate blocked state
- open provenance trace
- open payment status view

Disallowed console actions:
- silent unblock without evidence
- edit score or audit values directly
- bypass payment state
- mark package delivered when no delivery receipt exists

---

## §3.3 Operator States / Views

This section defines the canonical operator-facing visibility model.

### Required Operator-Ready States

#### 1. `NEW_INTAKE`
Packet exists but no run has started yet.

#### 2. `BLOCKED_MISSING_INPUTS`
Packet or run is blocked due to missing inputs.

#### 3. `AUDIT_IN_PROGRESS`
Audit generation is actively running or queued.

#### 4. `ASSETS_RENDERING`
Audit exists and media generation/render work is active.

#### 5. `READY_TO_DELIVER`
Preview and review gates are satisfied; package can be delivered.

#### 6. `DELIVERED_AWAITING_PAYMENT`
Package has been externally delivered / shown in the proof flow but the unlock payment has not yet completed.

#### 7. `PAID_UNLOCKED`
Payment succeeded and unlock propagation completed.

#### 8. `UPGRADED_HANDED_OFF`
The coach upgraded into continuity or Coach OS; Phase-0 run is commercially complete and handed off.

### Required View Modes

#### Queue View
Fast scan across all active packages, showing:
- coach/prospect label
- state
- SLA timer
- next action
- alert severity

#### Package Detail View
One package deep-dive showing:
- intake completeness
- run steps
- render status
- payment state
- receipts
- escalation history

#### Alert Feed
Sorted list of issues requiring action:
- SLA risk
- missing inputs
- stuck run
- failed unlock propagation
- payment pending too long

#### Recovery View
List of retryable or blocked packages with:
- exact blocking reason
- recommended next operator action
- provenance evidence links

### Console Design Law
This console should be understandable in under 10 seconds per package row.
That means:
- minimal jargon
- explicit statuses
- obvious severity coding
- one primary action per row

---

## §3.4 Governance Constraints

### G1. Human-Operator-Leverage Rule
The console exists to amplify operator throughput, not to force operators into manual micromanagement.

### G2. 24h Delivery Readiness Rule
Every active package must carry a visible SLA countdown against the `24h max` target.

### G3. Shared-Workspace-First Rule
The console assumes shared-runtime Phase-0 execution, not custom coach-container ownership.

### G4. Clear-State-Visibility Rule
Every package must always have an explicit operator state.

### G5. Recovery-Before-Churn Rule
Blockers and retry states must be surfaced before prospects silently decay out of the pipeline.

### G6. Receipt-Backed Visibility Rule
Any “done,” “blocked,” “failed,” “retryable,” or “delivered” state must correspond to real runtime or receipt evidence.

### G7. No Shadow PM Tool Rule
The console must not become a generic Kanban/project-management clone.

### G8. Payment State Must Remain Visible
Operators must not have to switch systems blindly to know whether a package is merely delivered, truly paid, or fully unlocked.

### G9. Escalations Must Be Typed
Escalation must be explicit and queryable, not hidden in chat or ad hoc notes.

### G10. Upgrade Handoff Must Be Visible
Phase-0 commercial completion must include visibility into whether the lead remained at `$29.99`, upgraded to `$39.99`, or progressed to `$99.99`.

---

## §3.5 Technical Decisions

### TD1. Build a Lean State Aggregator, Not a Separate Workflow Engine
Decision:
- the console reads and summarizes runtime state rather than replacing the orchestrator

Reason:
- avoids state duplication
- respects existing runtime ownership

### TD2. Use One Canonical Operator Row State
Decision:
- map multiple low-level runtime states into one top-level operator state per package

Reason:
- scanning speed
- less ambiguity

### TD3. Separate Alerts from States
Decision:
- keep `state` and `alert` distinct

Reason:
- a package can be `ASSETS_RENDERING` and still have an SLA warning

### TD4. Track SLA Independently from Package State
Decision:
- SLA must be modeled as its own packet

Reason:
- packages in identical states may have different urgency

### TD5. Missing Input Must Be First-Class
Decision:
- missing-input issues should not appear as vague block reasons only

Reason:
- this is one of the highest-frequency operator interventions in a 12-pack/day workflow

### TD6. Escalation Must Support Multiple Severities
Decision:
- operator, system, and managerial escalations should be typed

Reason:
- not every issue deserves the same interruption level

### TD7. Payment and Upgrade Visibility Stay in the Same Console
Decision:
- do not split delivery ops and commercial state into disconnected surfaces for Phase 0

Reason:
- the whole point of this runtime is speed and continuity

---

## §4 Plan

### Phase 1. Model Foundations
1. Define `Phase0RunStatus`
2. Define `Phase0SlaState`
3. Define `Phase0Alert`
4. Define `Phase0MissingInputState`
5. Define `Phase0EscalationState`
6. Define `Phase0OperatorQueueView`

### Phase 2. State Aggregation
7. Build runtime-state mapper from intake + delivery + commercial states
8. Build top-level operator row-state resolver
9. Build next-action resolver
10. Build missing-input summarizer

### Phase 3. SLA and Alerting
11. Implement SLA tracker service
12. Implement countdown and risk-band computation
13. Implement alert synthesis rules
14. Implement escalation-state propagation

### Phase 4. API and Surface Delivery
15. Add queue-view API
16. Add package-detail API
17. Add alert-feed API
18. Add retry and escalation action endpoints

### Phase 5. Recovery and Reliability
19. Add retryable-state classifier
20. Add stuck-run detector
21. Add payment-pending-too-long detector
22. Add unlock-propagation-failure detector

### Phase 6. Testing and Throughput Validation
23. Test 12-package queue aggregation
24. Test mixed-state operator scan
25. Test SLA warning bands
26. Test blocked and retry flows

---

## §5 Schema

### Enum: `Phase0TopLevelState`
- `NEW_INTAKE`
- `BLOCKED_MISSING_INPUTS`
- `AUDIT_IN_PROGRESS`
- `ASSETS_RENDERING`
- `READY_TO_DELIVER`
- `DELIVERED_AWAITING_PAYMENT`
- `PAID_UNLOCKED`
- `UPGRADED_HANDED_OFF`
- `FAILED`

### Enum: `Phase0AlertSeverity`
- `INFO`
- `WARNING`
- `HIGH`
- `CRITICAL`

### Enum: `Phase0EscalationLevel`
- `NONE`
- `OPERATOR_REVIEW`
- `SAME_DAY_RECOVERY`
- `MANAGER_ATTENTION`
- `MANUAL_OVERRIDE_REQUIRED`

### Pydantic Model: `Phase0RunStatus`
```python
class Phase0RunStatus(BaseModel):
    coach_id: str
    phase0_packet_id: str
    delivery_run_id: str | None = None
    top_level_state: Literal[
        "NEW_INTAKE",
        "BLOCKED_MISSING_INPUTS",
        "AUDIT_IN_PROGRESS",
        "ASSETS_RENDERING",
        "READY_TO_DELIVER",
        "DELIVERED_AWAITING_PAYMENT",
        "PAID_UNLOCKED",
        "UPGRADED_HANDED_OFF",
        "FAILED",
    ]
    intake_ready: bool
    audit_ready: bool
    render_ready: bool
    review_required: bool
    delivered: bool
    payment_completed: bool
    unlock_propagated: bool
    upgraded_target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"] | None = None
    updated_at_utc: datetime
```

### Pydantic Model: `Phase0SlaState`
```python
class Phase0SlaState(BaseModel):
    coach_id: str
    phase0_packet_id: str
    sla_started_at_utc: datetime
    sla_deadline_utc: datetime
    minutes_remaining: int
    risk_band: Literal["GREEN", "YELLOW", "ORANGE", "RED", "BREACHED"]
    breached: bool = False
    based_on_run_id: str | None = None
    updated_at_utc: datetime
```

### Pydantic Model: `Phase0Alert`
```python
class Phase0Alert(BaseModel):
    alert_id: str
    coach_id: str
    phase0_packet_id: str
    severity: Literal["INFO", "WARNING", "HIGH", "CRITICAL"]
    alert_type: str
    title: str
    summary: str
    recommended_action: str
    source_state_ref: str
    created_at_utc: datetime
    acknowledged_at_utc: datetime | None = None
```

### Pydantic Model: `Phase0MissingInputState`
```python
class Phase0MissingInputState(BaseModel):
    coach_id: str
    phase0_packet_id: str
    missing_fields: list[str]
    blocking: bool = True
    last_request_sent_at_utc: datetime | None = None
    operator_note: str | None = None
    updated_at_utc: datetime
```

### Pydantic Model: `Phase0EscalationState`
```python
class Phase0EscalationState(BaseModel):
    escalation_id: str
    coach_id: str
    phase0_packet_id: str
    escalation_level: Literal[
        "NONE",
        "OPERATOR_REVIEW",
        "SAME_DAY_RECOVERY",
        "MANAGER_ATTENTION",
        "MANUAL_OVERRIDE_REQUIRED",
    ]
    escalation_reason: str
    linked_alert_ids: list[str]
    active: bool = True
    created_at_utc: datetime
    resolved_at_utc: datetime | None = None
```

### Pydantic Model: `Phase0OperatorQueueItem`
```python
class Phase0OperatorQueueItem(BaseModel):
    coach_id: str
    phase0_packet_id: str
    display_name: str
    run_status: Phase0RunStatus
    sla_state: Phase0SlaState
    active_alert_count: int = Field(ge=0)
    highest_alert_severity: Literal["INFO", "WARNING", "HIGH", "CRITICAL"] | None = None
    next_action: str
    payment_state_label: str
    upgrade_state_label: str
```

### Pydantic Model: `Phase0OperatorQueueView`
```python
class Phase0OperatorQueueView(BaseModel):
    workspace_id: str
    generated_at_utc: datetime
    total_active_packages: int = Field(ge=0)
    green_count: int = Field(ge=0)
    yellow_count: int = Field(ge=0)
    orange_count: int = Field(ge=0)
    red_count: int = Field(ge=0)
    breached_count: int = Field(ge=0)
    items: list[Phase0OperatorQueueItem] = Field(default_factory=list)
```

### Auxiliary Model: `Phase0PackageDetailView`
```python
class Phase0PackageDetailView(BaseModel):
    coach_id: str
    phase0_packet_id: str
    run_status: Phase0RunStatus
    sla_state: Phase0SlaState
    missing_input_state: Phase0MissingInputState | None = None
    escalation_state: Phase0EscalationState | None = None
    alerts: list[Phase0Alert] = Field(default_factory=list)
    receipt_ids: list[str] = Field(default_factory=list)
    primary_review_action: str | None = None
```

---

## §6 Fallback

### F1. Missing Runtime Dependency
If one upstream runtime state is unavailable:
- preserve the last known operator row state
- emit a `HIGH` alert
- mark the package as partially observable

### F2. Receipt Query Failure
If receipt query fails:
- do not block all console visibility
- degrade provenance links only
- raise a recovery alert

### F3. Stuck Run Without Recent Receipt
If no progress receipt arrives within the configured stale threshold:
- mark alert type `STUCK_RUN`
- escalate to `SAME_DAY_RECOVERY`

### F4. Missing Inputs Not Requested
If a package is blocked on missing inputs and no request timestamp exists:
- emit `WARNING`
- recommend immediate operator request action

### F5. Payment Success But Unlock Missing
If payment completed but unlock propagation is false:
- alert severity `CRITICAL`
- escalation `MANUAL_OVERRIDE_REQUIRED`

### F6. SLA Breach
If deadline is crossed:
- risk band becomes `BREACHED`
- package remains visible at top of queue until resolved

### F7. Upgrade State Unknown
If the commercial bridge reports ambiguous upgrade handoff:
- keep package in `PAID_UNLOCKED`
- do not guess `UPGRADED_HANDED_OFF`
- alert for reconciliation

---

## §7 Tasks

### T1. Create `phase0_operator_console_models.py`
Add canonical models from this spec.

### T2. Create `phase0_sla_tracker.py`
Implement:
- SLA start/deadline resolution
- minute countdown
- risk-band classification

### T3. Create `phase0_operator_console_service.py`
Implement queue aggregation and package detail assembly.

### T4. Add state-mapping adapter
Map:
- intake states
- delivery states
- commercial states
into one top-level operator state.

### T5. Add alert synthesis rules
Implement typed alert generation.

### T6. Add escalation synthesis rules
Map alerts and stale conditions into escalation levels.

### T7. Add missing-input summarizer
Promote missing input into first-class operator state.

### T8. Add receipt-trace resolver
Allow package-level provenance lookup via receipt IDs.

### T9. Add queue view API
Suggested route:
- `GET /api/phase0/operator/queue`

### T10. Add package detail API
Suggested route:
- `GET /api/phase0/operator/package/{phase0_packet_id}`

### T11. Add alert-feed API
Suggested route:
- `GET /api/phase0/operator/alerts`

### T12. Add operator action routes
Suggested routes:
- `POST /api/phase0/operator/package/{phase0_packet_id}/retry`
- `POST /api/phase0/operator/package/{phase0_packet_id}/escalate`
- `POST /api/phase0/operator/package/{phase0_packet_id}/acknowledge-alert`

---

## §8 AC

### AC1
The console can render a queue of active Phase-0 packages with explicit top-level states.

### AC2
The console can show `24h max` SLA countdowns for all active packages.

### AC3
The console can distinguish:
- blocked by missing inputs
- audit in progress
- assets rendering
- ready to deliver
- delivered awaiting payment
- paid/unlocked
- upgraded/handed off

### AC4
The console can surface typed alerts with severity and recommended action.

### AC5
The console can surface escalation state independently from run state.

### AC6
The console can show payment-state visibility without leaving the Phase-0 workflow.

### AC7
The console can show whether continuity handoff happened after payment.

### AC8
The console remains usable as a batch-scan surface for at least 12 simultaneous packages.

### AC9
The console does not require bespoke project-management concepts beyond package queue, alerts, and next actions.

### FAILURE EXAMPLE
Bad behavior that must be rejected:
- package misses inputs
- audit never starts
- no SLA alert appears
- operator only learns of the problem after the 24h window is already lost

This is a hard failure because it breaks:
- throughput
- recovery-before-churn
- clear-state-visibility
- and the survivability goal of Phase 0

---

## §9 Dependencies

### Confirmed Present in Workspace
- receipt chain logging/query system
- AFFiNE queue and dashboard model patterns
- campaign state/gate patterns
- billing/payment visibility patterns
- Phase-0 delivery and commercial runtime specs

### Required New Components
- `Phase0OperatorQueueView`
- `Phase0SlaState`
- `Phase0Alert`
- `Phase0RunStatus`
- `Phase0MissingInputState`
- `Phase0EscalationState`
- queue aggregation service
- SLA tracker service

### Dependency Rule
This console depends on upstream state truth from:
- intake
- delivery orchestration
- commercial bridge

It must not re-own those state machines.

### Future Integration
This spec should later integrate with:
- `FR-ERA3-39` campaign frontend and batch intake workspace
- `FR-ERA3-40` batch execution review and approval board

---

## §10 Testing

### Unit Tests
- top-level state resolver
- SLA risk-band resolver
- alert-generation rules
- escalation-level rules
- next-action mapping

### Integration Tests
- intake ready -> new queue item
- blocked missing inputs -> correct alert and state
- audit running -> correct state and countdown
- rendering state -> correct state and no false delivery label
- delivered awaiting payment -> commercial state visible
- paid unlocked -> unlock state visible
- upgraded handed off -> final handoff visible

### Failure Tests
- receipt-query degradation
- stuck-run detection
- unlock propagation failure alert
- SLA breach ordering
- missing-input request absent

### Throughput Tests
- queue view renders 12 active packages
- mixed severities sort correctly
- breached packages float above green packages

### Regression Tests
- no package enters `READY_TO_DELIVER` without supporting runtime state
- no package enters `PAID_UNLOCKED` without payment completion
- no package enters `UPGRADED_HANDED_OFF` on ambiguous commercial state

### Build Notes and Future Integration
The operator console is the practical human-control layer that makes Phase-0 survivable.

It should remain:
- lean
- state-backed
- alert-driven
- recovery-oriented

It should never become:
- a generic ops sprawl surface
- a state-guessing tool
- or a parallel workflow engine detached from CCP runtime truth
