# FR-ERA3-36 — Phase-0 Delivery Orchestrator Tech Spec

## §1 Files Read

### Core Prompt
- `docs/architecture/april_updates/spec_prompts/P0_S04_FR-ERA3-36_Phase0_Delivery_Orchestrator.md`

### Upstream Phase-0 Specs
- `docs/architecture/april_updates/FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`

### Source PRD Modules
- `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
- `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

### Existing Service / Runtime Evidence
- `src/ccp/services/content_machine.py`
- `src/ccp/services/cmf_arc_governed_rendering.py`
- `src/ccp/services/course_video_cmf.py`
- `src/ccp/services/campaign_orchestrator.py`
- `src/ccp/services/payment_flow_orchestrator.py`

### Additional Context
- `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec_UPDATED_FOR_SFL.md`
- `docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec_UPDATED_FOR_SFL.md`
- `lab/phase0_eval_card_scoring_model_v_1.md`

### Pre-Work Log
This spec was written after verifying the live direction of CCP across:
- the trigger-first content compiler law in `PRD-02`
- the staged realization law in `PRD-03`
- the paid proof-package ladder and Phase-0 runtime need in `PRD-09`
- the existing packetized orchestration patterns already present in `content_machine.py`, `cmf_arc_governed_rendering.py`, and `course_video_cmf.py`

The central conclusion from the pre-read is that CCP already has most of the production backbone. What is missing is a shared, explicit, low-overhead orchestration layer that can:
- accept a validated `Phase0ProspectPacket`
- trigger audits and proof-package generation in one main environment
- preserve reviewability before release
- produce deliverables in a concrete sequence
- hand off to payment and continuity without requiring a full coach container first

This spec formalizes that missing orchestration runtime.

---

## §2 Overview

`FR-ERA3-36` defines the shared pre-container delivery runtime used to produce the `$29.99` Phase-0 proof package inside CCP's main environment.

The orchestrator is responsible for:
- receiving a validated `Phase0ProspectPacket` from `FR-ERA3-33`
- generating or coordinating the audit and media outputs required by `PRD-09`
- assembling reviewable preview bundles before release
- sequencing deliverables for external presentation
- preserving operator checkpoints for quality
- emitting canonical receipts and run state for internal batching and SLA tracking
- handing off completion state to the payment and upgrade runtime

This runtime is intentionally **shared** and **pre-container**:
- it does **not** provision a full custom coach container
- it does **not** require deep per-coach model setup
- it does **not** pretend that sovereign runtime economics apply at this stage

Instead it exists to maximize:
- speed
- consistency
- batch throughput
- low setup overhead
- concrete proof production inside `24h max`

### Canonical External Package Scope
The default public proof package defined by this orchestrator is:

1. `Explainer Video 1 (60s)` from the coach's existing material
2. `Explainer Video 2 (60s)` from the coach's existing material or enhanced voice path
3. `1 Cinematic Storytelling Video (60s)`
4. `1 Full Audit`
5. `1 Animated Explainer Audit (120s)`
6. `Carousel and meme/spread layers when relevant`
7. `Payment / activation handoff`

### Important Runtime Distinction
The orchestrator separates:
- **generation order**
- **review order**
- **external release order**

This is required because:
- the audit often needs to exist before media can be framed properly
- preview bundles should exist before payment release
- the public experience should still follow the wow-sequencing defined in `PRD-09`

### Runtime Law
The orchestrator follows this law:

> Generate from judgment, review before release, sequence for persuasion, and degrade honestly when optional assets fail.

---

## §3.1 DEP-IDs

### Primary Dependencies
- `DEP-FR-ERA3-33`
  - `FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md`
  - provides `Phase0ProspectPacket` and intake validation outputs

- `DEP-FR-ERA3-35`
  - `FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
  - provides canonical audit payloads and diagnosis/prescription outputs

- `DEP-FR-ERA3-35C`
  - `FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
  - provides scoring-card render payloads and shareable board surfaces

### Supporting Dependencies
- `DEP-PRD-02`
  - `PRD_02_CCF_Content_Factory.md`
  - meaning compilation and source artifact generation

- `DEP-PRD-03`
  - `PRD_03_CMF_Media_Factory.md`
  - staged realization and render validation logic

- `DEP-PRD-09`
  - `PRD_09_CPSC_Silent_Referral.md`
  - commercial sequence, proof-package scope, and 24h runtime expectation

- `DEP-FR-ERA3-12`
  - CMF render realization

- `DEP-FR-ERA3-18`
  - coaching carryover and continuity guidance consumption

### Provisional / Not Yet Finalized
- `DEP-FR-ERA3-35A`
  - eval registry and scoring taxonomy
  - not yet built in workspace

- `DEP-FR-ERA3-35B`
  - benchmark profiles and weighting bundles
  - not yet built in workspace

This spec must remain honest about those gaps. Any field that depends on `35A/35B` must be modeled with adapter boundaries instead of pretending those services already exist.

---

## §3.2 Backend

### Runtime Position
The Phase-0 Delivery Orchestrator sits between:
- validated intake
- canonical audit generation
- media realization
- payment release

It is the runtime conductor for the fast proof-package lane.

### Runtime Responsibilities
The backend must:
- accept validated Phase-0 intake packets
- compute the package plan
- stage audit-first and media-first generation tasks correctly
- call the correct production backends for each output family
- collect outputs into one coherent bundle
- preserve operator review checkpoints
- emit receipts and run state for queue / SLA systems

### Existing Backend Patterns To Reuse
The implementation should reuse patterns already proven in the workspace:

#### From `content_machine.py`
- extraction pipeline stages
- batch evaluation stages
- triple-pass validation
- packet/result object discipline

#### From `cmf_arc_governed_rendering.py`
- job record creation
- manifest assembly
- release gating
- receipt logging
- explicit lifecycle states

#### From `course_video_cmf.py`
- command-to-video orchestration
- fallback handling
- protocol-based media engines
- graceful degradation when high-fidelity render stages fail

### Service Boundary Recommendation
Recommended implementation roots:
- `src/ccp/services/phase0_delivery_orchestrator.py`
- `src/ccp/models/phase0_delivery_models.py`
- `src/ccp/api/routes/phase0_delivery.py`
- `tests/services/test_phase0_delivery_orchestrator.py`

### Recommended Internal Collaborators
The orchestrator should coordinate with adapters or services that map onto:
- intake packet retrieval
- audit generation
- score-card board rendering
- CMF media rendering
- PDF package assembly
- audit explainer video assembly
- payment-link generation
- operator-review state persistence

### Shared-Environment Law
At Phase 0:
- the orchestrator runs in the main CCP environment
- jobs are isolated by packet and namespace
- coaches are **not** provisioned into dedicated containers
- artifacts are namespaced by `coach_id`, `phase0_packet_id`, and `delivery_run_id`

This preserves batch speed and shared-runtime economics.

---

## §3.3 Packets / Runtime Results

This spec defines six canonical runtime contracts.

### 1. `Phase0DeliveryPlan`
Purpose:
- declarative plan for what the package should produce
- one per package attempt

Required fields:
- `plan_id: str`
- `coach_id: str`
- `phase0_packet_id: str`
- `package_variant: str`
- `requested_outputs: list[str]`
- `generation_order: list[Phase0SequenceStep]`
- `release_order: list[Phase0SequenceStep]`
- `review_required: bool`
- `optional_outputs_enabled: list[str]`
- `sla_deadline_utc: datetime`
- `commercial_target: str`
- `created_at_utc: datetime`

### 2. `Phase0DeliveryRun`
Purpose:
- stateful execution record of one plan

Required fields:
- `delivery_run_id: str`
- `plan_id: str`
- `coach_id: str`
- `status: Phase0DeliveryRunStatus`
- `started_at_utc: datetime | None`
- `completed_at_utc: datetime | None`
- `current_step_id: str | None`
- `step_results: list[Phase0SequenceStepResult]`
- `output_bundle_id: str | None`
- `review_state: str`
- `failure_state: str | None`
- `receipts: list[Phase0DeliveryReceipt]`

### 3. `Phase0OutputBundle`
Purpose:
- unified bundle of generated assets and review surfaces

Required fields:
- `output_bundle_id: str`
- `coach_id: str`
- `phase0_packet_id: str`
- `audit_report_id: str | None`
- `pdf_audit_payload_id: str | None`
- `audit_explainer_video_payload_id: str | None`
- `explainer_video_1_asset_id: str | None`
- `explainer_video_2_asset_id: str | None`
- `cinematic_video_asset_id: str | None`
- `carousel_asset_ids: list[str]`
- `meme_asset_ids: list[str]`
- `score_card_board_ids: list[str]`
- `preview_bundle_ids: list[str]`
- `delivery_ready: bool`
- `release_blockers: list[str]`
- `payment_handoff_ready: bool`

### 4. `Phase0SequenceStep`
Purpose:
- declarative unit in generation and release sequence

Required fields:
- `step_id: str`
- `step_key: str`
- `step_type: Phase0SequenceStepType`
- `order_index: int`
- `execution_mode: Phase0ExecutionMode`
- `required: bool`
- `review_gate: bool`
- `depends_on_step_ids: list[str]`
- `target_output_key: str`

### 5. `Phase0RenderRequest`
Purpose:
- normalized handoff into rendering or asset-assembly layers

Required fields:
- `render_request_id: str`
- `coach_id: str`
- `phase0_packet_id: str`
- `delivery_run_id: str`
- `target_surface: str`
- `artifact_family: str`
- `source_payload_ids: list[str]`
- `template_key: str | None`
- `priority: str`
- `review_required: bool`
- `delivery_context: dict[str, Any]`

### 6. `Phase0DeliveryReceipt`
Purpose:
- auditable record of each completed or failed orchestration step

Required fields:
- `receipt_id: str`
- `delivery_run_id: str`
- `step_id: str`
- `coach_id: str`
- `outcome: str`
- `artifact_ids: list[str]`
- `notes: list[str]`
- `started_at_utc: datetime | None`
- `completed_at_utc: datetime | None`
- `retryable: bool`

### Additional Runtime Result Objects
Recommended support objects:
- `Phase0SequenceStepResult`
- `Phase0ReviewBundle`
- `Phase0ReleasePacket`
- `Phase0DegradedDeliveryState`
- `Phase0PaymentHandoffPacket`

---

## §3.4 Governance Constraints

### G1. Shared Pre-Container Runtime Only
The orchestrator must not provision full custom coach containers in Phase 0.

### G2. Audit Ownership Must Stay Canonical
The orchestrator does not invent its own scoring logic. It consumes audit outputs from `FR-ERA3-35`.

### G3. Cards Must Stay Presentation-Side
The orchestrator can request score-card render surfaces, but it does not own card scoring itself.

### G4. Honest Degradation
If optional outputs fail:
- the bundle may still complete in degraded mode
- the degradation must be explicit
- no fake “full package complete” state may be emitted

### G5. Core Package Minimum
The orchestrator may only mark a package as `delivery_ready=True` if these are present:
- canonical audit report
- PDF audit payload
- at least one reviewable preview bundle
- payment handoff packet

### G6. High-Value Asset Review Gate
The following should default to operator review before external release:
- Explainer Video 1
- Explainer Video 2
- Cinematic Storytelling Video
- Animated Explainer Audit

### G7. External Sequencing Must Match Commercial Doctrine
Public release order must follow `PRD-09`, unless an explicit product decision revises the package doctrine.

### G8. Internal Generation May Differ From External Release
The runtime is allowed to generate audit assets before public explainer assets if this improves quality and speed.

### G9. Packetized Receipts Required
Every major step must emit a receipt. Batch scaling and SLA monitoring depend on that.

### G10. No Shadow Payment Release
The orchestrator may prepare payment / activation packets, but payment ownership belongs to the commercial bridge runtime.

---

## §3.5 Technical Decisions

### TD1. Separate Generation Order From Release Order
Decision:
- keep two explicit ordered sequences

Reason:
- audit assets often need to exist first
- public persuasion sequence should still feel staged and intentional

### TD2. Reviewable Preview Bundles Are First-Class
Decision:
- preview bundles are canonical outputs, not ad hoc conveniences

Reason:
- operators need a clear review surface
- payment and release should not happen blind

### TD3. PDF Audit and Audit Explainer Video Are Core Assets
Decision:
- both are first-class outputs in this runtime

Reason:
- the user explicitly wants scoring cards to feed PDF audit and audit explainer video
- this also standardizes explainer template creation

### TD4. Optional Spread Assets Stay Optional
Decision:
- carousel and meme/spread outputs are optional by package fit

Reason:
- they are valuable but should not hard-block the entire run

### TD5. Heuristic-First Video Structure Is Acceptable
Decision:
- reel segmentation and timing can begin heuristic-first and later deepen

Reason:
- `FR-ERA3-35` already preserves this path
- we should not block Phase 0 on full advanced video segmentation

### TD6. One Main Environment, Namespaced Jobs
Decision:
- all runs execute in a shared environment with artifact namespacing

Reason:
- required for 12-pack/day speed goals
- avoids premature custom infra cost

### TD7. Explicit Review Gates Over Implicit Human Intervention
Decision:
- review stages must be modeled in data, not hand-waved operationally

Reason:
- improves reproducibility
- supports batch queueing and partial automation

---

## §4 Plan

### Phase-0 Runtime Plan

#### Step 1. Resolve Validated Intake
- load validated `Phase0ProspectPacket`
- verify required input families are present
- compute package variant and optional outputs

#### Step 2. Build Delivery Plan
- create `Phase0DeliveryPlan`
- define generation order
- define release order
- compute SLA deadline

#### Step 3. Run Audit Core
- request canonical audit generation from `FR-ERA3-35`
- capture:
  - report
  - PDF audit payload
  - audit explainer video payload
  - score-card board references

#### Step 4. Generate Render Requests
- create `Phase0RenderRequest` objects for:
  - PDF assembly
  - score-card surfaces
  - audit explainer video
  - Explainer Video 1
  - Explainer Video 2
  - Cinematic Storytelling Video
  - optional carousel/meme assets

#### Step 5. Execute Media Realization
- route requests into CMF-compatible realization paths
- collect asset ids and intermediate statuses

#### Step 6. Assemble Reviewable Preview Bundle
- create preview surfaces for operator review
- aggregate verdicts, thumbnails, and package completeness state

#### Step 7. Apply Review Gates
- release automatically only what is allowed
- hold high-value assets for operator review when configured

#### Step 8. Build Release Packet
- convert internal outputs into the public delivery sequence
- attach payment / activation bridge packet

#### Step 9. Emit Final Receipts
- write per-step receipts
- write aggregate run status
- publish `Phase0OutputBundle`

### Recommended Internal Generation Order
1. Validate intake packet
2. Compute delivery plan
3. Generate audit intelligence report
4. Generate score-card and board surfaces
5. Generate PDF audit package
6. Generate audit explainer video
7. Generate Explainer Video 1
8. Generate Explainer Video 2
9. Generate Cinematic Storytelling Video
10. Generate optional carousel/meme spread assets
11. Assemble review bundle
12. Prepare payment handoff packet

### Recommended External Release Order
1. Explainer Video 1
2. Explainer Video 2
3. Cinematic Storytelling Video
4. Full Audit PDF
5. Animated Explainer Audit
6. Optional carousel and meme/spread assets
7. Payment / activation bridge

This aligns with the current `PRD-09` package framing.

---

## §5 Schema

### Enum: `Phase0DeliveryRunStatus`
- `PLANNED`
- `READY`
- `RUNNING`
- `AWAITING_REVIEW`
- `DEGRADED_READY`
- `COMPLETED`
- `PARTIAL_FAILURE`
- `FAILED`
- `BLOCKED`

### Enum: `Phase0SequenceStepType`
- `AUDIT_CORE`
- `CARD_RENDER`
- `PDF_AUDIT_ASSEMBLY`
- `AUDIT_EXPLAINER_VIDEO`
- `EXPLAINER_VIDEO`
- `CINEMATIC_VIDEO`
- `CAROUSEL_ASSET`
- `MEME_ASSET`
- `PREVIEW_ASSEMBLY`
- `PAYMENT_HANDOFF`
- `RELEASE_STEP`

### Enum: `Phase0ExecutionMode`
- `AUTOMATIC`
- `OPERATOR_REVIEW_REQUIRED`
- `MANUAL_ONLY`

### Pydantic Model: `Phase0SequenceStep`
```python
class Phase0SequenceStep(BaseModel):
    step_id: str
    step_key: str
    step_type: Literal[
        "AUDIT_CORE",
        "CARD_RENDER",
        "PDF_AUDIT_ASSEMBLY",
        "AUDIT_EXPLAINER_VIDEO",
        "EXPLAINER_VIDEO",
        "CINEMATIC_VIDEO",
        "CAROUSEL_ASSET",
        "MEME_ASSET",
        "PREVIEW_ASSEMBLY",
        "PAYMENT_HANDOFF",
        "RELEASE_STEP",
    ]
    order_index: int
    execution_mode: Literal["AUTOMATIC", "OPERATOR_REVIEW_REQUIRED", "MANUAL_ONLY"]
    required: bool = True
    review_gate: bool = False
    depends_on_step_ids: list[str] = Field(default_factory=list)
    target_output_key: str
```

### Pydantic Model: `Phase0DeliveryPlan`
```python
class Phase0DeliveryPlan(BaseModel):
    plan_id: str
    coach_id: str
    phase0_packet_id: str
    package_variant: str
    requested_outputs: list[str]
    generation_order: list[Phase0SequenceStep]
    release_order: list[Phase0SequenceStep]
    review_required: bool = True
    optional_outputs_enabled: list[str] = Field(default_factory=list)
    sla_deadline_utc: datetime
    commercial_target: str = "phase0_proof_unlock"
    created_at_utc: datetime
```

### Pydantic Model: `Phase0RenderRequest`
```python
class Phase0RenderRequest(BaseModel):
    render_request_id: str
    coach_id: str
    phase0_packet_id: str
    delivery_run_id: str
    target_surface: str
    artifact_family: str
    source_payload_ids: list[str]
    template_key: str | None = None
    priority: Literal["HIGH", "NORMAL", "LOW"] = "NORMAL"
    review_required: bool = True
    delivery_context: dict[str, Any] = Field(default_factory=dict)
```

### Pydantic Model: `Phase0SequenceStepResult`
```python
class Phase0SequenceStepResult(BaseModel):
    step_id: str
    status: Literal["PENDING", "RUNNING", "SUCCEEDED", "FAILED", "SKIPPED", "BLOCKED"]
    produced_artifact_ids: list[str] = Field(default_factory=list)
    failure_reason: str | None = None
    degraded: bool = False
    started_at_utc: datetime | None = None
    completed_at_utc: datetime | None = None
```

### Pydantic Model: `Phase0DeliveryReceipt`
```python
class Phase0DeliveryReceipt(BaseModel):
    receipt_id: str
    delivery_run_id: str
    step_id: str
    coach_id: str
    outcome: Literal["SUCCEEDED", "FAILED", "SKIPPED", "DEGRADED"]
    artifact_ids: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    started_at_utc: datetime | None = None
    completed_at_utc: datetime | None = None
    retryable: bool = False
```

### Pydantic Model: `Phase0OutputBundle`
```python
class Phase0OutputBundle(BaseModel):
    output_bundle_id: str
    coach_id: str
    phase0_packet_id: str
    audit_report_id: str | None = None
    pdf_audit_payload_id: str | None = None
    audit_explainer_video_payload_id: str | None = None
    explainer_video_1_asset_id: str | None = None
    explainer_video_2_asset_id: str | None = None
    cinematic_video_asset_id: str | None = None
    carousel_asset_ids: list[str] = Field(default_factory=list)
    meme_asset_ids: list[str] = Field(default_factory=list)
    score_card_board_ids: list[str] = Field(default_factory=list)
    preview_bundle_ids: list[str] = Field(default_factory=list)
    delivery_ready: bool = False
    release_blockers: list[str] = Field(default_factory=list)
    payment_handoff_ready: bool = False
```

### Pydantic Model: `Phase0DeliveryRun`
```python
class Phase0DeliveryRun(BaseModel):
    delivery_run_id: str
    plan_id: str
    coach_id: str
    status: Literal[
        "PLANNED",
        "READY",
        "RUNNING",
        "AWAITING_REVIEW",
        "DEGRADED_READY",
        "COMPLETED",
        "PARTIAL_FAILURE",
        "FAILED",
        "BLOCKED",
    ]
    started_at_utc: datetime | None = None
    completed_at_utc: datetime | None = None
    current_step_id: str | None = None
    step_results: list[Phase0SequenceStepResult] = Field(default_factory=list)
    output_bundle_id: str | None = None
    review_state: str = "NOT_STARTED"
    failure_state: str | None = None
    receipts: list[Phase0DeliveryReceipt] = Field(default_factory=list)
```

### Auxiliary Model: `Phase0PaymentHandoffPacket`
```python
class Phase0PaymentHandoffPacket(BaseModel):
    coach_id: str
    phase0_packet_id: str
    delivery_run_id: str
    output_bundle_id: str
    commercial_offer_key: str
    payment_ready: bool
    release_ready: bool
    upgrade_credit_eligible: bool = True
```

---

## §6 Fallback

### F1. Audit Failure
If the canonical audit cannot be produced:
- the run must fail closed
- no package may be marked complete
- no public release packet may be emitted

Reason:
- the audit is the judgment core and commercial logic bridge

### F2. PDF Assembly Failure
If the audit exists but PDF assembly fails:
- hold release
- mark `delivery_ready=False`
- allow retry after payload repair

### F3. Audit Explainer Video Failure
If the audit report and PDF are valid but animated audit video fails:
- package may continue only in degraded mode
- degraded state must be explicit in review board
- payment handoff may proceed only if commercial policy allows the missing asset

### F4. Explainer Video Failure
If one explainer video fails:
- keep the run alive
- mark partial failure
- hold that asset in release order
- allow operator rerun

### F5. Cinematic Asset Failure
If cinematic generation fails:
- mark degraded state
- do not silently substitute generic output
- allow run to complete only if policy permits a proof-lite package

### F6. Optional Spread Failure
If carousel or meme/spread assets fail:
- do not block core package
- mark optional output degraded
- preserve receipt trail

### F7. Preview Bundle Failure
If preview bundle assembly fails:
- block public release
- operator review cannot be bypassed for gated assets

### F8. Payment Handoff Failure
If payment handoff packet cannot be built:
- package may be internally complete
- commercial release state must remain blocked

---

## §7 Tasks

### T1. Create Delivery Models
- add `phase0_delivery_models.py`
- implement all canonical schemas from this spec

### T2. Create Orchestrator Service
- add `phase0_delivery_orchestrator.py`
- implement plan/build/run/finalize flow

### T3. Add Intake Adapter
- consume `Phase0ProspectPacket` from `FR-ERA3-33`

### T4. Add Audit Adapter
- consume canonical outputs from `FR-ERA3-35`

### T5. Add Card/Board Adapter
- consume score-card and audit-board outputs from `FR-ERA3-35C`

### T6. Add Media Render Adapter
- normalize render requests into CMF-facing job requests

### T7. Add PDF Audit Assembly Path
- convert canonical audit payload into deliverable PDF packet/result

### T8. Add Audit Explainer Video Path
- convert scoring-card-driven audit payload into explainer video output

### T9. Add Preview Bundle Assembly
- produce operator-reviewable preview sets

### T10. Add Release and Payment Handoff Packets
- finalize public sequence and commercial handoff packet

### T11. Add Receipt Persistence
- emit per-step receipts and aggregate run state

### T12. Add API Routes
Recommended routes:
- `POST /api/phase0/delivery/plans`
- `POST /api/phase0/delivery/runs`
- `GET /api/phase0/delivery/runs/{delivery_run_id}`
- `POST /api/phase0/delivery/runs/{delivery_run_id}/retry`
- `POST /api/phase0/delivery/runs/{delivery_run_id}/review-decision`

---

## §8 AC

### AC1
Given a valid `Phase0ProspectPacket`, the system can produce a canonical `Phase0DeliveryPlan`.

### AC2
The system differentiates internal generation order from public release order.

### AC3
The runtime can orchestrate:
- PDF audit payload production
- scoring-card board assembly
- animated audit explainer production
- proof-video production

### AC4
The runtime preserves explicit review gates for high-value assets.

### AC5
The runtime emits a canonical `Phase0OutputBundle`.

### AC6
The runtime emits receipts for all required steps.

### AC7
Optional asset failures do not incorrectly mark the run as full success.

### AC8
Audit failure blocks the package completely.

### AC9
Preview assembly failure blocks public release.

### AC10
Payment handoff state is explicit and not conflated with content generation success.

### AC11
The runtime supports the shared pre-container model and does not assume a dedicated coach container exists.

### AC12
The runtime is batch-safe through namespacing by:
- `coach_id`
- `phase0_packet_id`
- `delivery_run_id`

---

## §9 Dependencies

### Confirmed Present In Workspace
- `FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md`
- `FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
- `FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
- `FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec_UPDATED_FOR_SFL.md`
- `FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec_UPDATED_FOR_SFL.md`

### Not Yet Present As Final Upstream Tech Specs
- `FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy_Tech_Spec.md`
- `FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`

### Dependency Rule
Implementation may proceed before `35A/35B` exist only if:
- card-visible score fields are treated as adapter-fed values
- weighting-specific logic remains isolated behind service boundaries
- no hard-coded fake benchmark canon is introduced in this orchestrator

### Future Integration Touchpoints
Later integrations should connect to:
- campaign frontend and batch intake workspace
- operator review board
- commercial bridge runtime
- SLA tracker

---

## §10 Testing

### Unit Tests
- plan creation from valid packet
- generation order assembly
- release order assembly
- required vs optional step behavior
- degradation logic for optional assets
- audit-failure hard block
- preview-failure hard block
- payment-handoff readiness logic

### Integration Tests
- valid prospect packet -> full delivery run
- audit outputs -> PDF + scoring-card assets + audit explainer request
- CMF adapter receives normalized render requests
- preview bundle assembled with expected artifacts
- final output bundle reflects actual produced state

### Failure Tests
- missing audit report
- PDF generation failure
- one explainer asset failure
- cinematic failure
- optional spread failure
- missing review approval
- payment handoff failure

### Batch-Safety Tests
- two runs for different coaches do not collide
- two runs for same coach but different packets do not collide
- receipts are correctly namespaced

### Regression Tests
- external release order remains stable unless explicitly changed
- required core outputs remain required
- no code path marks a degraded bundle as a full success

### Build Notes and Future Integration
This spec intentionally defines the orchestration core before:
- the final eval registry canon
- the final benchmark weighting canon
- the campaign frontend runtime
- the operator review board runtime

That is acceptable because:
- the delivery orchestrator's ownership is coordination, not score invention
- upstream score canon can stabilize behind adapters later
- Phase-0 survival speed depends on orchestrating existing CCP backbone pieces now

This spec should next integrate with:
- `FR-ERA3-37` commercial bridge
- `FR-ERA3-38` operator console / SLA tracker
- `FR-ERA3-39` campaign frontend
- `FR-ERA3-40` batch execution review board
