# FR-ERA3-40 - Phase-0 Batch Execution Review and Approval Board Tech Spec

## §1 Files Read

### Source PRDs and doctrine read for this spec
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
- `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
- `lab/phase0_eval_card_scoring_model_v_1.md`
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/ccp_biological_orchestration_model_v_1.md`

### Phase-0 and SFL specs read for this spec
- `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-37_Phase0_Commercial_Bridge_And_Payment_Runtime_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-39_Phase0_Campaign_Frontend_And_Batch_Intake_Workspace_Tech_Spec.md`

### Prompt files explicitly reviewed
- `docs/architecture/april_updates/spec_prompts/P0_S03_FR-ERA3-35_Audit_Intelligence_Engine.md`
- `docs/architecture/april_updates/spec_prompts/P0_S04_FR-ERA3-36_Phase0_Delivery_Orchestrator.md`
- `docs/architecture/april_updates/spec_prompts/P0_S06_FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker.md`
- `docs/architecture/april_updates/spec_prompts/P0_S08_FR-ERA3-40_Phase0_Batch_Execution_Review_And_Approval_Board.md`

### Existing implementation and test anchors reviewed
- `src/ccp/models/score_viewer_models.py`
- `src/ccp/services/scorecard_emitter.py`
- `tests/integration/test_fr_era3_score_card_viewer.py`
- `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py`

### Key takeaways from the source set
- `PRD-09` establishes the commercial ladder and makes Phase-0 a proof-first conversion layer rather than a full sovereign coach runtime.
- `PRD-03` requires preview, review, and final tiers, and explicitly separates concept, asset creation, and assembly so review can happen at the right stage.
- `FR-ERA3-36` already defines internal generation order, operator review order, and external release order; this spec must become the operator surface that enforces those rules.
- `FR-ERA3-35` defines the audit as a first-class product output with PDF and audit explainer payloads; the board must preview and approve those outputs explicitly.
- `FR-ERA3-35C` defines the scoring cards and audit boards as first-class deliverables; this review surface must treat them as core proof objects, not side assets.
- `FR-ERA3-37` defines payment and unlock boundaries; this spec must never blur approval state with commercial entitlement state.
- `FR-ERA3-38` provides queue and SLA visibility, but intentionally avoids becoming the deep review workspace; this spec fills that gap.
- `FR-ERA3-39` defines how operators stage and batch-run many coaches in one shared environment; this spec handles the downstream review, correction, and release workflow after execution.

## §2 Overview

`FR-ERA3-40` defines the internal operator board used to review, compare, approve, reject, revise, rerun, and release Phase-0 packages after backend execution. It is the final human gating surface between generation and commercial handoff.

This board exists because the Phase-0 machine is intentionally optimized for:
- shared runtime execution
- high batch throughput
- low-cost proof generation
- rapid operator review
- strict protection of delivery quality before a prospect sees the result

The board is not a passive gallery. It is a production-control surface with explicit decisions, lineage, and release state. Operators need to see:
- what ran
- what was produced
- what is ready
- what is weak
- what is blocked
- what should be rerun
- what is safe to release
- what is payment-ready but still locked

The board must support:
- single-run review
- batch-run review
- side-by-side comparison of two runs
- before/after audit card comparison
- preview of the PDF audit
- preview of the audit explainer video
- preview of the two explainers and the cinematic video
- approve / reject / rerun / revise actions
- payment-ready and release-ready markers

This spec intentionally keeps ownership boundaries clean:
- `FR-ERA3-35` owns diagnosis and prescription output formation
- `FR-ERA3-35C` owns card and audit-board display contracts
- `FR-ERA3-36` owns orchestration and output sequencing
- `FR-ERA3-37` owns payment and unlock state
- `FR-ERA3-38` owns queue and SLA monitoring
- `FR-ERA3-39` owns the batch intake workspace
- `FR-ERA3-40` owns deep review and approval state over the produced outputs

The board sits on top of a shared Phase-0 runtime. It must never assume one isolated coach container per prospect. Every row, artifact set, and decision must be namespaced by canonical IDs and receipt lineage so many coaches can be handled in the same environment without artifact confusion.

## §3.1 DEP-IDs

### Core dependencies
- `DEP-FR-ERA3-35-AUDIT-ENGINE`
- `DEP-FR-ERA3-35C-EVAL-CARD-SYSTEM`
- `DEP-FR-ERA3-36-DELIVERY-ORCHESTRATOR`
- `DEP-FR-ERA3-37-COMMERCIAL-BRIDGE`
- `DEP-FR-ERA3-38-OPERATOR-CONSOLE`
- `DEP-FR-ERA3-39-CAMPAIGN-FRONTEND`

### Supporting implementation dependencies
- `DEP-CCP-RECEIPT-CHAIN`
- `DEP-CMF-RENDER-MANIFEST`
- `DEP-SCORE-VIEWER-PAYLOADS`
- `DEP-TELEGRAM-PAYMENT-HANDOFF`

### Dependency expectations
- `FR-ERA3-40` must be able to render a coherent review row even if some downstream previews are still generating, but it must do so honestly.
- `FR-ERA3-40` must degrade visibly when upstream specs are provisional or partially implemented.
- `FR-ERA3-40` must not fabricate missing artifacts, missing previews, or missing payment states.

## §3.2 Backend

### Purpose
The backend for this spec aggregates Phase-0 execution outputs into a reviewable, decisionable board. It loads run state from the shared artifact store, groups the outputs into review bundles, calculates readiness and blocking state, accepts operator decisions, emits lineage receipts, and coordinates release handoff with the commercial runtime.

### Backend responsibilities
- read `Phase0DeliveryRun` and `Phase0OutputBundle` data from `FR-ERA3-36`
- read audit payload availability from `FR-ERA3-35`
- read card/board payload availability from `FR-ERA3-35C`
- read payment and entitlement state from `FR-ERA3-37`
- aggregate into `Phase0ReviewRow`
- allow decision writes:
  - approve
  - reject
  - rerun
  - revise
- preserve prior run lineage across reruns
- compute release readiness
- compute payment readiness
- publish the current approval surface to the operator UI

### Backend boundaries
- This backend does not generate media.
- This backend does not compute audit scores.
- This backend does not create invoices directly.
- This backend does not own the SLA queue.
- This backend does not replace the batch intake workspace.

### Canonical service responsibilities
The implementation should eventually expose a dedicated service layer, likely under `src/ccp/services/phase0_review_board_service.py`, with responsibilities such as:
- assemble board views
- load row details
- create revision decisions
- create rerun requests
- compute release state
- mark payment-ready state
- emit review receipts

### Suggested API surfaces
- `GET /api/phase0/review-board`
- `GET /api/phase0/review-board/{coach_id}`
- `GET /api/phase0/review-board/run/{run_id}`
- `POST /api/phase0/review-board/{run_id}/approve`
- `POST /api/phase0/review-board/{run_id}/reject`
- `POST /api/phase0/review-board/{run_id}/rerun`
- `POST /api/phase0/review-board/{run_id}/revise`
- `POST /api/phase0/review-board/{run_id}/mark-release-ready`

### Storage and lineage expectations
Every board decision must be receipt-backed and lineaged. At minimum:
- `run_id`
- `coach_id`
- `prospect_packet_id`
- `artifact_set_id`
- `prior_run_id` when rerun
- `source_decision_id` when revising a prior decision
- timestamp
- operator identity
- reason code
- human-readable notes

## §3.3 Review/approval artifacts

### Required review artifacts
The board must treat the following as first-class review artifacts:
- `Explainer Video 1`
- `Explainer Video 2`
- `Cinematic Storytelling Video`
- `Full Audit PDF`
- `Audit Scoring Cards / Audit Board`
- `Animated Audit Explainer Video`

### Optional review artifacts
These may exist depending on package composition or fallback path:
- `Carousel`
- `Meme Visual`
- `Shareable Audit Summary Board`
- `Internal Preview Bundle`

### Human review requirements
The following artifacts require human review by default before release:
- `Explainer Video 1`
- `Explainer Video 2`
- `Cinematic Storytelling Video`
- `Full Audit PDF`
- `Audit Scoring Cards / Audit Board`
- `Animated Audit Explainer Video`
- any optional artifact intended for external delivery

### Auto-pass candidates
These may be auto-passed when present because they are support surfaces rather than prospect-facing truth objects:
- internal preview derivatives
- non-public transcoded helper files
- internal render manifests
- internal thumbnail extractions
- internal artifact health snapshots

### Why the review default is conservative
The Phase-0 offer is low-cost, but it is still a proof product. The whole commercial ladder depends on the first package being:
- coherent
- impressive
- aligned
- emotionally persuasive
- safe to show

That means the operator board must prefer human review over premature automation for externally visible proof assets.

### Review bundle logic
For each run, the board must assemble a `Phase0ArtifactReviewSet` that contains:
- artifact references
- preview URLs or local paths
- presence / missing state
- blocking / non-blocking classification
- operator comments
- prior decisions
- current effective version

### Comparison modes
The review board must support:
- current artifact only
- current vs previous version
- current vs another run for the same coach
- before vs after card comparison
- before vs after audit summary comparison

## §3.4 Governance Constraints

### GC-1 Review-Before-Release
No prospect-facing package may be marked release-ready until all required review artifacts either:
- pass human review
- or are explicitly waived under a future governance exception policy

Phase-0 v1 does not support silent waivers for core artifacts.

### GC-2 Core Artifact Blocking
If any required core artifact is missing or failed:
- release must remain blocked
- payment-ready must remain false
- the board must expose the blocker clearly

### GC-3 Honest Partial Failure Handling
Optional artifact failure must not pretend the package is fully complete.

The board must show one of:
- `core_ready_optional_missing`
- `core_ready_optional_failed`
- `core_blocked`
- `full_ready`

### GC-4 Lineage Preservation
Reruns and revisions must append lineage, not overwrite history.

Operators must be able to see:
- what was produced first
- what was rejected
- what was rerun
- what was revised
- what is now the active approved version

### GC-5 Commercial Separation
Approval state and entitlement state are separate.

A run can be:
- review-approved but still locked
- payment-ready but not yet paid
- partially visible as free proof
- fully unlocked after payment

This spec must never collapse review approval into entitlement.

### GC-6 Shared Runtime Safety
Because many coaches run in the same environment, board actions must always bind to:
- `coach_id`
- `run_id`
- `artifact_set_id`
- `prospect_packet_id`

No board action may rely on ambiguous filenames alone.

### GC-7 Audit Truth Priority
If the audit PDF, audit cards, or audit explainer disagree with the delivery state, the board must block release until the inconsistency is resolved. The audit package is not decorative; it is part of the commercial truth.

### GC-8 Sequential Release Awareness
The board must understand `FR-ERA3-36` external release order and support staged release preparation:
1. `Explainer Video 1`
2. `Explainer Video 2`
3. `Cinematic Storytelling Video`
4. `Full Audit PDF`
5. `Animated Audit Explainer Video`
6. optional `Carousel / Meme`
7. payment / activation handoff

## §3.5 Technical Decisions

### TD-1 Review surface is distinct from queue surface
`FR-ERA3-38` remains the operator queue and SLA monitor.
`FR-ERA3-40` is the deep artifact review and decision board.

This separation keeps:
- queue scanning fast
- review interactions richer
- state aggregation clean

### TD-2 Rerun is not revise
`rerun` means the pipeline re-executes generation for a targeted scope.
`revise` means the operator records a review issue and requests correction work or adjusted inputs.

Both are decisions, but they imply different downstream actions and different lineage.

### TD-3 Compare-first UX is a first-class requirement
Because Phase-0 is batch-heavy and iterative, the board must make comparison fast:
- before/after cards
- run vs rerun outputs
- audit board deltas
- prior rejection vs corrected version

### TD-4 Card board is a review primitive
The scoring card board defined by `FR-ERA3-35C` must not be treated as a cosmetic export only. It is a central review primitive because it exposes:
- signal quality
- AI slop risk
- diagnosis clarity
- commercial proof strength

### TD-5 Release readiness requires both artifact approval and commercial compatibility
The board may only mark `payment_ready` or `release_ready` if:
- the review gate passes
- required artifacts exist
- the `FR-ERA3-37` commercial state can accept the transition

### TD-6 Prior versions remain inspectable
Rejected or superseded artifacts remain viewable for:
- quality learning
- operator accountability
- before/after proof
- future evaluator calibration

### TD-7 Preview availability must be honest
If a preview is missing:
- the board must say so
- the artifact must not silently appear as blank success
- the missing preview state must not destroy the rest of the row if the source artifact exists

## §4 Plan

### Phase A - domain modeling
1. Define canonical review-board models under `src/ccp/models/phase0_review_board_models.py`.
2. Define core enums for review state, release state, payment-ready state, rerun scope, and revision severity.
3. Define artifact role constants for required and optional Phase-0 deliverables.

### Phase B - aggregation service
4. Build a board aggregation service that loads run data from `FR-ERA3-36`.
5. Add audit/card availability adapters against `FR-ERA3-35` and `FR-ERA3-35C`.
6. Add commercial state adapters against `FR-ERA3-37`.
7. Add current-vs-prior artifact lineage assembly from receipt-chain provenance.

### Phase C - review decisions
8. Build `approve` decision flow.
9. Build `reject` decision flow.
10. Build `rerun` request flow with scoped targets.
11. Build `revise` request flow with operator notes and issue tags.
12. Emit review receipts for every decision.

### Phase D - release coordination
13. Compute `Phase0ReleaseState` from effective decisions and artifact readiness.
14. Compute `Phase0PaymentReadyState` from release state plus commercial compatibility.
15. Expose release gating information back to the operator console and campaign frontend.

### Phase E - UI surfaces
16. Build batch board list view.
17. Build row detail panel with artifact previews.
18. Build side-by-side compare mode.
19. Build before/after card-board compare mode.
20. Build PDF preview launcher and audit video preview launcher.
21. Build explicit action controls for approve / reject / rerun / revise.

### Phase F - validation and regression coverage
22. Add unit tests for release-state computation.
23. Add integration tests for rerun lineage preservation.
24. Add UI/state tests for missing preview honesty.
25. Add regression coverage for payment-ready state not activating before review approval.

## §5 Schema

### `Phase0BatchExecutionBoard`
Top-level board payload representing a filtered set of reviewable runs.

```python
class Phase0BatchExecutionBoard(BaseModel):
    board_id: str
    generated_at: datetime
    filter_state: dict[str, Any]
    total_rows: int
    ready_rows: int
    blocked_rows: int
    payment_ready_rows: int
    release_ready_rows: int
    rows: list["Phase0ReviewRow"]
```

### `Phase0ReviewRow`
Primary review row representing one effective run for one coach/prospect packet.

```python
class Phase0ReviewRow(BaseModel):
    coach_id: str
    prospect_packet_id: str
    run_id: str
    prior_run_id: str | None = None
    artifact_set_id: str
    coach_display_name: str
    content_type_mix: list[str]
    execution_status: str
    review_status: str
    blocking_reason_codes: list[str] = Field(default_factory=list)
    artifact_review_set: "Phase0ArtifactReviewSet"
    release_state: "Phase0ReleaseState"
    payment_ready_state: "Phase0PaymentReadyState"
    latest_decision: "Phase0ApprovalDecision | None" = None
    compare_targets: list[str] = Field(default_factory=list)
    updated_at: datetime
```

### `Phase0ArtifactReviewSet`
Structured set of review artifacts for the run.

```python
class Phase0ArtifactReviewSet(BaseModel):
    audit_pdf_artifact_id: str | None = None
    audit_pdf_preview_path: str | None = None
    audit_card_board_artifact_id: str | None = None
    audit_card_board_preview_path: str | None = None
    audit_explainer_video_artifact_id: str | None = None
    audit_explainer_video_preview_path: str | None = None
    explainer_video_1_artifact_id: str | None = None
    explainer_video_1_preview_path: str | None = None
    explainer_video_2_artifact_id: str | None = None
    explainer_video_2_preview_path: str | None = None
    cinematic_video_artifact_id: str | None = None
    cinematic_video_preview_path: str | None = None
    carousel_artifact_id: str | None = None
    meme_artifact_id: str | None = None
    preview_bundle_path: str | None = None
    missing_required_artifacts: list[str] = Field(default_factory=list)
    failed_optional_artifacts: list[str] = Field(default_factory=list)
    auto_passed_artifacts: list[str] = Field(default_factory=list)
    human_review_required_artifacts: list[str] = Field(default_factory=list)
```

### `Phase0ApprovalDecision`
Canonical decision object for review actions.

```python
class Phase0ApprovalDecision(BaseModel):
    decision_id: str
    coach_id: str
    run_id: str
    artifact_set_id: str
    decision_type: Literal["approve", "reject", "rerun", "revise"]
    operator_id: str
    reason_code: str
    note: str | None = None
    target_artifact_ids: list[str] = Field(default_factory=list)
    created_at: datetime
```

### `Phase0RerunRequest`
Request object for rerunning all or part of a run while preserving provenance.

```python
class Phase0RerunRequest(BaseModel):
    rerun_request_id: str
    coach_id: str
    source_run_id: str
    source_artifact_set_id: str
    target_scope: Literal[
        "full_package",
        "audit_only",
        "audit_video_only",
        "explainer_1_only",
        "explainer_2_only",
        "cinematic_only",
        "optional_assets_only",
    ]
    requested_by: str
    reason_code: str
    note: str | None = None
    created_at: datetime
```

### `Phase0RevisionRequest`
Request object for manual or semi-manual correction without implying a pure rerender.

```python
class Phase0RevisionRequest(BaseModel):
    revision_request_id: str
    coach_id: str
    run_id: str
    artifact_set_id: str
    severity: Literal["minor", "major", "blocking"]
    issue_code: str
    note: str
    requested_by: str
    created_at: datetime
```

### `Phase0ReleaseState`
Review-gated release state independent from commercial entitlement.

```python
class Phase0ReleaseState(BaseModel):
    status: Literal[
        "blocked",
        "review_in_progress",
        "core_ready_optional_missing",
        "core_ready_optional_failed",
        "release_ready",
        "released",
    ]
    release_blockers: list[str] = Field(default_factory=list)
    approved_required_artifacts: list[str] = Field(default_factory=list)
    pending_required_artifacts: list[str] = Field(default_factory=list)
    released_at: datetime | None = None
```

### `Phase0PaymentReadyState`
Commercial-bridge readiness state for `$29.99` unlock flow.

```python
class Phase0PaymentReadyState(BaseModel):
    status: Literal[
        "not_ready",
        "review_ready_but_commercial_blocked",
        "payment_ready",
        "unlock_initiated",
        "unlock_confirmed",
    ]
    bridge_compatible: bool
    commercial_state_ref: str | None = None
    blockers: list[str] = Field(default_factory=list)
    updated_at: datetime
```

### Derived UI state notes
The UI may derive convenience booleans such as:
- `can_approve`
- `can_reject`
- `can_rerun`
- `can_revise`
- `can_release`
- `can_open_payment_handoff`

But those must be derived from canonical state, not persisted as separate truth.

## §6 Fallback

### Missing preview but artifact exists
If the artifact exists but the preview derivative is missing:
- show the artifact as present
- show the preview as unavailable
- do not auto-approve
- allow operator to open the raw artifact if supported

### Audit PDF failed, other assets passed
If the audit PDF is missing or failed:
- the package is blocked
- `release_state.status = blocked`
- `payment_ready_state.status = not_ready`
- board must surface `audit_pdf_missing` or `audit_pdf_failed`

### Audit cards present but audit explainer missing
If audit cards are present but audit explainer video failed:
- release remains blocked because audit explainer is a required artifact in Phase-0 v1
- operator may rerun `audit_video_only`

### Optional assets fail
If carousel or meme fail:
- the board may move to `core_ready_optional_failed`
- operator can still approve the core package
- the optional failure remains visible

### Payment bridge temporarily unavailable
If review passes but payment bridge is unavailable:
- `release_state` may be `release_ready`
- `payment_ready_state` becomes `review_ready_but_commercial_blocked`
- the board must show a clear commercial blocker rather than pretending the package can proceed

### Rerun requested on stale run
If a rerun is requested against a run that is no longer the active latest version:
- allow only if lineage is explicit
- otherwise require operator confirmation in UI
- never overwrite the current active approved version silently

### Conflicting decisions
If one operator approves and another submits a blocking revision against the same effective run:
- latest non-superseded blocking decision must dominate
- board should show decision conflict state
- release remains blocked until reconciled

## §7 Tasks

### Task group 1 - models and enums
- Add `phase0_review_board_models.py`.
- Add enums for review decision and release readiness.
- Add validation rules ensuring required artifact fields match artifact role presence.

### Task group 2 - provenance and aggregation
- Integrate with receipt chain for decision lineage.
- Build artifact-set assembly from Phase-0 output bundle records.
- Build comparison-target discovery for prior run versions.

### Task group 3 - board service
- Build board listing query.
- Build row detail query.
- Build artifact preview resolver.
- Build release-state calculator.
- Build payment-ready calculator.

### Task group 4 - decision execution
- Implement approval endpoint.
- Implement rejection endpoint.
- Implement rerun request endpoint.
- Implement revision request endpoint.
- Emit consistent receipts for each action.

### Task group 5 - frontend board
- Add batch board list view.
- Add row detail drawer or page.
- Add comparison view.
- Add before/after card board mode.
- Add PDF and video preview launch flows.
- Add visible release/payment markers.

### Task group 6 - integration
- Wire `FR-ERA3-39` row selection into board opening.
- Wire `FR-ERA3-38` queue states into deep-review navigation.
- Wire `FR-ERA3-37` payment handoff affordance into approved rows.

### Task group 7 - tests
- Unit test release blocking.
- Unit test payment-ready transition.
- Integration test rerun lineage.
- Integration test partial optional failure.
- UI-state test preview honesty.

## §8 AC

### AC-1 Required artifact visibility
Given a completed run with all required outputs present,
when the board loads the row,
then the operator sees all required artifacts grouped into one review set with preview references or honest missing-preview markers.

### AC-2 Blocking on missing core artifact
Given a run missing the audit PDF,
when the board computes release state,
then the row is blocked and cannot be marked payment-ready.

### AC-3 Separate approval and commercial state
Given a fully approved package before payment handoff,
when the board computes state,
then it may be `release_ready` while still showing `payment_ready` or `unlock_initiated`, never `unlock_confirmed` unless the commercial runtime confirms it.

### AC-4 Rerun lineage preservation
Given an operator reruns only `Explainer Video 2`,
when the new run appears,
then the board preserves:
- source run reference
- source artifact set reference
- operator reason
- prior version visibility

### AC-5 Side-by-side comparison
Given a row with a prior rejected version,
when the operator opens compare mode,
then the board shows before/after artifact and card comparison without losing current effective version identity.

### AC-6 Optional asset degradation
Given all core assets pass and the meme visual fails,
when the release state is computed,
then the row may move to `core_ready_optional_failed` and remain approvable as a core package.

### AC-7 No silent auto-release
Given all artifacts exist but human review has not yet happened,
when the board loads,
then the package must not be marked released or unlock-confirmed.

### AC-8 Honest missing preview state
Given an artifact exists but the preview file is unavailable,
when the row renders,
then the UI must show the artifact as present with a missing-preview warning, not as a blank success card.

### AC-9 Failure example
This spec fails if:
- a cinematic video bypasses human review
- the audit PDF is missing but the package is shown as payment-ready
- a rerun overwrites the old version without provenance
- approval and unlock status collapse into one state

## §9 Dependencies

### Upstream dependencies
- `FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
- `FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
- `FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md`
- `FR-ERA3-37_Phase0_Commercial_Bridge_And_Payment_Runtime_Tech_Spec.md`
- `FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker_Tech_Spec.md`
- `FR-ERA3-39_Phase0_Campaign_Frontend_And_Batch_Intake_Workspace_Tech_Spec.md`

### Implementation dependencies
- receipt-chain append / provenance read helpers
- artifact storage and preview path resolution
- score-viewer style preview payload patterns
- CMF preview-tier and review-tier outputs

### Honest implementation notes
- `FR-ERA3-35A` and `FR-ERA3-35B` are still not built in the workspace at the time of this spec authoring, so visible score provenance and weighting provenance will initially remain adapter-driven.
- This spec still proceeds because the review board can operate on produced artifacts and effective payloads even while some scoring substrate remains provisional.

## §10 Testing

### Unit tests
- test `Phase0ReleaseState` blocks when any required artifact is missing
- test `Phase0PaymentReadyState` remains blocked when commercial bridge is incompatible
- test optional failure yields `core_ready_optional_failed`
- test latest blocking decision dominates conflicting earlier approval

### Integration tests
- load a completed batch run and verify all rows aggregate correctly
- approve a row and verify review receipt emission
- request rerun and verify provenance to source run is preserved
- reject one artifact set and verify release remains blocked
- confirm approved row can transition to payment-ready when commercial runtime allows it

### UI-state tests
- batch board shows readiness markers and blockers
- side-by-side compare renders prior and current versions correctly
- before/after audit card comparison renders the correct score families:
  - Humanity
  - Presence
  - Trust
  - Memorability
  - Resonance
  - Signal
  - AI Slop Risk
- PDF preview button resolves when preview exists
- missing preview state is labeled honestly when preview is unavailable

### Regression anchors
- keep parity with score-viewer honesty patterns for missing signals and fallback states
- keep release-state calculations aligned with `FR-ERA3-36` sequencing and `FR-ERA3-37` payment boundary
- verify no silent release path appears during batch throughput optimizations

### Build Notes and Future Integration
- Future iterations may introduce selective auto-approval for highly reliable optional assets, but Phase-0 v1 should remain conservative.
- A later version may add reviewer assignment, multi-operator concurrence, or team audit lanes.
- The board should eventually expose structured improvement analytics so repeated rejection patterns can feed evaluator and generator improvements.
- When `FR-ERA3-35A` and `FR-ERA3-35B` are implemented, this board should display score provenance and weighting bundle metadata directly in compare mode without changing the decision contracts in this spec.
