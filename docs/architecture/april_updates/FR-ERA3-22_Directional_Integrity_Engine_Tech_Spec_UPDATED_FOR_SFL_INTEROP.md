# Tech-Spec: FR-ERA3-22 - Directional Integrity Engine Updated for SFL Interop

## Pre-Work Log

### 1. Protocol Read
- Read `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`.
- Confirmed this update spec must preserve the existing backend stack, show explicit brownfield integration, use typed schemas, and define testable implementation boundaries rather than abstract architectural prose.

### 2. Source PRD Read - Runtime Law
- Read `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`.
  - Proof quote captured:
    - `DNA / truth -> RNA / transcription -> force -> delivery -> variation -> rendered phenotype -> evaluation`
  - Boundary quote captured:
    - `Meaning Plane (Plane A)` governs truth and ontology.
    - `Experience Plane (Plane B)` governs delivery and user encounter.
- Read `docs/prd/modules/PRD_02_CCF_Content_Factory.md`.
  - Canonical runtime law quote captured:
    - `signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> subliminal function stack -> composition depth profile -> variation profile -> directional integrity validation -> perceptual influence validation -> JIT script contract -> render blueprint`
  - Meaning-compiler quote captured:
    - `CCF is therefore the meaning compiler for the platform. It decides the logic and source truth of what will be said. Other modules decide the cinematic treatment, interface delivery, or experiential framing.`
- Read `docs/prd/modules/PRD_08_Conscious_Primitives.md`.
  - Plane-separation quote captured:
    - `Meaning Plane (Plane A)` answers what truth is present.
    - `Experience Plane (Plane B)` answers how the user encounters the meaning.
  - Placement quote captured:
    - `the truth substrate includes Voice DNA, Negative Space, and SDA`
    - `the delivery stack includes SFL and composition depth profiles`
    - `the variation stack includes asymmetry, resonance, salience distribution, and paradox retention`

### 3. SFL / Doctrine Source Set Read
- Read `lab/subliminal_function_layer_for_ccp_v_1.md`.
  - Structural claim:
    - `SDA protects semantic truthfulness.`
    - `SFL shapes perceptual potency and symbolic aliveness.`
  - Governance claim:
    - `SFL is not anti-persuasion.`
    - `SFL is anti-blandness, anti-deadness, anti-false-depth, and anti-misaligned influence.`
- Read `lab/ccp_biological_orchestration_model_v_1.md`.
  - Runtime chain claim:
    - `DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation`
  - DSPy/runtime claim:
    - `DSPy is both a runtime orchestration substrate and an optimization substrate.`
    - It must not be described as only outside runtime.

### 4. Existing FR Specs Read
- Read `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`.
  - Ownership claim captured:
    - FR-22 already owns semantic direction validation through invariant preservation, representation drift, hard-negative adjacency, and trajectory risk.
  - Safety claim captured:
    - high-risk surfaces fail closed on degraded dependencies.
- Read `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`.
  - Ownership claim captured:
    - FR-27 "does not re-evaluate semantic coherence."
  - Interop claim captured:
    - FR-27 consumes the DI report as a prerequisite input and evaluates a different question: perceptual aliveness, symbolic density, human congruence, and memorability.
- Read `docs/architecture/april_updates/FR-ERA3-28_Perceptual_Failure_Corpus_And_Contrast_Harness_Tech_Spec.md` indirectly through build context and prompt relation.
  - Interop requirement:
    - FR-28 strengthens false-depth, dead-polish, and synthetic-authority detection but does not replace DI ownership.

### 5. Existing Backend References Read
- Read `src/ccp/models/directional_integrity_models.py`.
  - Verified existing typed contracts:
    - `DirectionalIntegrityRequest`
    - `DirectionalIntegrityReport`
    - `DirectionalIntegrityEngineResult`
    - `DirectionalIntegrityDecisionSummary`
- Read `src/ccp/services/directional_integrity_engine.py`.
  - Verified real method signatures:
    - `def evaluate(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:`
    - `def validate_for_planning(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:`
    - `def validate_for_release(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:`
  - Verified real decision behavior:
    - semantic dependency degradation on high-risk surfaces fails closed
    - review and hard block routes already exist
- Read `src/ccp/services/semantic_affinity_guard.py`.
  - Verified real deterministic gate precedent:
    - `SemanticAffinityGuard.evaluate(...)`
    - PASS / OPERATOR_REVIEW / FAIL_TERMINAL
    - explicit fallback behavior
- Read `src/ccp/services/content_machine.py`.
  - Verified real upstream compile entrypoint:
    - `async def process_session(`

### 6. Existing Tests Read
- Read `tests/integration/test_era3_fr22_directional_integrity_engine.py`.
  - Confirmed typed contract tests, fail-closed tests, surface override tests, and lineage assertions already exist.
- Attempted discovery for FR-27 test files referenced in the FR-27 spec:
  - `tests/integration/test_era3_fr27_perceptual_influence_evaluator.py`
  - `tests/integration/test_era3_fr27_perceptual_influence_fallbacks.py`
  - result: files not found in workspace at spec-writing time.

### 7. Implementation-State Finding
- The FR-27 spec exists, but the following implementation files are not present yet:
  - `src/ccp/models/perceptual_influence_models.py`
  - `src/ccp/services/perceptual_influence_evaluator.py`
  - `src/ccp/services/perceptual_influence_policy_registry.py`
- Consequence:
  - this FR-22 update must define the DI-side interop contracts and precedence rules now
  - and must mark FR-27 runtime code as a downstream implementation dependency rather than pretending the files already exist.

---

## §1 Files Read

1. `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
3. `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
4. `docs/prd/modules/PRD_08_Conscious_Primitives.md`
5. `lab/subliminal_function_layer_for_ccp_v_1.md`
6. `lab/ccp_biological_orchestration_model_v_1.md`
7. `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`
8. `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
9. `src/ccp/models/directional_integrity_models.py`
10. `src/ccp/services/directional_integrity_engine.py`
11. `src/ccp/services/semantic_affinity_guard.py`
12. `src/ccp/services/content_machine.py`
13. `tests/integration/test_era3_fr22_directional_integrity_engine.py`

Missing implementation files confirmed:
- `src/ccp/models/perceptual_influence_models.py`
- `src/ccp/services/perceptual_influence_evaluator.py`
- `src/ccp/services/perceptual_influence_policy_registry.py`

Missing tests confirmed:
- `tests/integration/test_era3_fr27_perceptual_influence_evaluator.py`
- `tests/integration/test_era3_fr27_perceptual_influence_fallbacks.py`

---

## §2 Overview

### Problem
FR-ERA3-22 currently defines the semantic truth validator correctly, and FR-ERA3-27 defines the perceptual evaluator correctly at the architectural level, but the platform still lacks a **typed interop contract** that makes their relationship executable and unambiguous.

Without this update, four bad outcomes remain possible:

1. DI gets treated as a style judge even though it owns semantic truth and trajectory, not charisma or aliveness.
2. SFL/perceptual evaluation gets treated as an optional garnish even though PRD-02 names it as a formal runtime stage.
3. A semantically failed artifact could be cosmetically "rescued" by perceptual pass language.
4. A perceptually failed artifact could be misread as semantically false, collapsing truth and delivery into one noisy validator.

### Goal
Update FR-ERA3-22 so the Directional Integrity Engine:

- preserves clear ownership of semantic truth, direction, drift, and hard-negative logic
- exposes a typed interop surface for perceptual attachments
- composes cleanly with FR-27 and FR-28
- emits a joint report when both validators are present
- enforces hard precedence:
  - semantic failure blocks
  - perceptual failure downgrades, reviews, or blocks based on surface and policy

### Runtime Placement
Under the current CCP organism model:

- DI belongs to the **truth/protection boundary**
- SFL belongs to the **delivery layer**
- perceptual evaluation belongs to the **evaluation of delivery/variation outcome**

Therefore:

- DI validates whether the emergent product is directionally admissible
- PI validates whether the admitted product is alive, human, memorable, and non-false-deep
- joint reporting must preserve this order rather than flattening them into one score blob

### What This Update Changes
This update does not turn FR-22 into the perceptual evaluator.
It adds:

- a DI-side interop schema
- a joint decision state model
- a failure-state matrix
- explicit composition rules for FR-27 / FR-28
- explicit downstream routing behavior for mixed semantic/perceptual outcomes

### What This Update Does Not Change
This update does not:

- move SFL metrics into DI ownership
- re-score charisma or resonance inside DI
- remove FR-22 fail-closed behavior on semantic failures
- relax hard-negative or trajectory-risk governance

---

## §3.1 DEP-IDs

| DEP-ID | Name | Status | Purpose |
|---|---|---|---|
| `DEP-SDA-020` | `DirectionalIntegrityEngine` | EXISTING | Core semantic validator for direction, drift, hard-negative proximity, and trajectory risk |
| `DEP-SDA-022` | `DirectionalIntegrityInteropReport` | NEW | DI-owned joint wrapper that carries semantic verdict plus optional perceptual attachment |
| `DEP-SDA-023` | `SemanticVsPerceptualDecisionState` | NEW | Explicit combined-state contract for semantic/perceptual precedence and downstream routing |
| `DEP-SDA-024` | `PerceptualAttachmentSummary` | NEW | Optional attachment carrying PI outcome summary without transferring PI ownership into DI |
| `DEP-SDA-025` | `JointFailureSurface` | NEW | Failure-state matrix object describing semantic/perceptual outcome combinations and required routing |
| `DEP-SDA-026` | `JointValidatorRoutingDecision` | NEW | Canonical downstream routing output for compile/review/block/degrade behavior |
| `DEP-SFL-027-01` | `PerceptualInfluenceEvaluator` | PLANNED / EXTERNAL | Upstream perceptual evaluator whose output may be attached but not recomputed by DI |
| `DEP-SFL-028-01` | `PerceptualFailureCorpus` | PLANNED / EXTERNAL | Contrastive support for false-depth / dead-polish / synthetic-authority findings |

### DEP Law
- `DEP-SDA-020` remains the semantic authority.
- `DEP-SDA-022` through `025` exist only to make interop and routing executable.
- No new DEP in this update may cause DI to own perceptual metrics.

---

## §3.2 Backend (>=4 files)

### Existing Brownfield Files

#### 1. `src/ccp/models/directional_integrity_models.py`
Relevant existing models:

- `DirectionalIntegrityRequest`
- `DirectionalIntegrityDecisionSummary`
- `DirectionalIntegrityReport`
- `DirectionalIntegrityEngineResult`

Important existing traits:

- strict typed enums
- `lineage_refs`
- `fallback_reason`
- surface-aware decisions

Update rule:
- interop models should live here or in an adjacent DI model file
- they must preserve this exact style and forbid extra fields

#### 2. `src/ccp/services/directional_integrity_engine.py`
Relevant signatures:

```python
def evaluate(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
def validate_for_planning(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
def validate_for_release(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
```

Existing behavior preserved:

- fail closed on degraded semantic dependencies for high-risk surfaces
- PASS / REVIEW / FAIL semantics
- hard block on semantic failure
- `should_continue_automation`
- `should_queue_operator_review`
- `should_trigger_regeneration`
- `should_trip_circuit_break`

Update rule:
- add interop composition step after semantic evaluation when perceptual attachment is supplied
- do not let composition mutate the original semantic verdict

#### 3. `src/ccp/services/semantic_affinity_guard.py`
Relevant precedent:

- deterministic gate
- operator review state
- terminal failure state
- explicit fallback behavior

Update rule:
- use this as the local precedent for mixed-state composition and fail-safe interop
- not as a semantic owner

#### 4. `src/ccp/services/content_machine.py`
Relevant entrypoint:

```python
async def process_session(
```

Update rule:
- downstream pipelines need one typed object that explains both semantic and perceptual routing
- that object should be the interop report from this spec

### Implementation-State Constraint
The perceptual evaluator implementation files are not present yet.
Therefore:

- FR-22 must specify the DI-side input/attachment contract
- FR-27 implementation later must conform to it or provide an adapter
- FR-22 must not hard-depend on importing nonexistent FR-27 backend classes today

### Brownfield Rejection Rules
Reject any implementation that:

- imports speculative FR-27 runtime modules that do not exist yet
- replaces `DirectionalIntegrityReport` instead of wrapping it
- rewrites DI into a monolithic semantic+style scorer
- changes DI PASS/REVIEW/FAIL semantics to mirror PI PASS/REVIEW/DOWNGRADE directly

---

## §3.3 Joint Report / Ownership Contract

### DI Owns
Directional Integrity owns:

- invariant preservation
- representation drift
- hard-negative adjacency
- trajectory risk
- semantic fallbacks
- hard semantic block/review/pass semantics
- semantic lineage refs
- semantic required corrections

### SFL / PI Owns
Perceptual evaluation owns:

- human congruence
- symbolic density as perceptual force
- memorability / imprint
- anti-false-depth
- anti-dead-polish
- anti-synthetic-smoothness
- surface-specific perceptual downgrade/review/pass logic

### Composition Rule
DI and PI compose as:

1. DI runs first or is already present as prerequisite.
2. PI may run only on top of a DI result or an explicit low-risk exception policy.
3. DI verdict is never rewritten by PI.
4. PI verdict can modify downstream routing only within the semantic envelope allowed by DI.

### Required Composition Outcomes

| Semantic | Perceptual | Allowed Meaning | Routing Consequence |
|---|---|---|---|
| PASS | PASS | Truth preserved and delivery alive | continue |
| PASS | REVIEW | Truth preserved, delivery uncertain | operator review or regeneration based on surface |
| PASS | DOWNGRADE | Truth preserved, delivery weak or false-deep | downgrade or block based on surface policy |
| REVIEW | PASS | Truth uncertain, delivery alive | review remains review; PI pass is advisory only |
| REVIEW | REVIEW | both uncertain | review |
| REVIEW | DOWNGRADE | semantic uncertainty + perceptual weakness | review or block on high-risk surfaces |
| FAIL | PASS | semantic corruption present despite alive delivery | fail |
| FAIL | REVIEW | semantic corruption present | fail |
| FAIL | DOWNGRADE | both bad | fail |

### Joint Report Law
The joint report must:

- preserve the original `DirectionalIntegrityReport` intact
- attach a perceptual summary rather than absorb it
- expose a combined decision state for downstream services
- make the precedence rule explicit in one object

### No-Style-Only-Pass Rule
An artifact must never proceed because:

- it feels powerful
- it sounds charismatic
- it looks polished

if semantic direction has failed or remained unresolved on a high-risk surface.

---

## §3.4 Governance Constraints

### 1. SFL Subordinate-to-SDA Rule
If perceptual aliveness conflicts with semantic truth:

- semantic truth wins
- DI verdict governs the ceiling

### 2. Truth-Vs-Delivery Boundary Rule
DI may inspect perceptual attachment presence and routing implications.
DI may not compute perceptual force metrics itself.

### 3. Joint-Report-Without-Swallowing Rule
The interop report must not swallow either side into a single undifferentiated score.
It must preserve:

- semantic report object
- perceptual attachment object
- combined routing state

### 4. No Semantic Override by Styling Rule
Perceptual pass cannot:

- convert semantic fail to review
- convert semantic review to pass
- mask hard-negative block

### 5. No Semantic Downgrade by Mere Flatness Rule
Perceptual weakness alone does not mean semantic falsehood.
It means:

- weak delivery
- weak human force
- weak memorability
- or false-depth risk

### 6. High-Risk Surface Rule
On:

- `COMMERCIAL_TRUST_TRANSFER`
- `RENDER_RELEASE`
- `LONG_FORM_AUTHORITY`

perceptual downgrade may escalate to block if policy requires it, but only after semantic truth has already passed or reviewed.

### 7. Missing-Perceptual-Dependency Rule
If semantic DI passes but the perceptual evaluator is required and unavailable:

- high-risk surfaces must not silently pass
- interop state must explicitly record missing perceptual prerequisite
- routing must become review or block by policy

---

## §3.5 Technical Decisions

### Decision 1 - Keep `DirectionalIntegrityReport` Intact
Do not mutate the existing DI report structure to carry all PI detail.

Reason:
- avoids ownership collapse
- preserves existing FR-22 tests and contracts
- keeps DI usable even before FR-27 runtime files land

### Decision 2 - Add Interop Wrapper Rather Than Merge Validators
Use `DirectionalIntegrityInteropReport` as the wrapper.

Reason:
- respects sequential runtime law
- makes downstream consumers read one packet while preserving distinct authorities

### Decision 3 - Use Explicit Combined-State Enum
Adopt `SemanticVsPerceptualDecisionState` instead of implicit if/else logic.

Reason:
- routing logic becomes testable
- operator review surfaces become explainable
- mixed outcomes stop being hidden heuristics

### Decision 4 - Make Perceptual Attachment Optional but Typed
Use `PerceptualAttachmentSummary` as an optional attachment.

Reason:
- FR-27 runtime code is not present yet
- low-risk semantic planning can still function without PI
- high-risk surfaces can explicitly enforce PI presence later

### Decision 5 - Add Joint Failure Matrix Object
Use `JointFailureSurface`.

Reason:
- captures exact failure-state semantics
- supports downstream engine decisions without recomputing precedence

### Decision 6 - Preserve DI Hard Failure Semantics
Keep DI `FAIL` terminal within the interop state.

Reason:
- semantic corruption is not a soft style issue
- existing circuit-breaker behavior depends on that distinction

### Decision 7 - Allow Perceptual Block Only by Policy
Perceptual weakness may block only:

- where explicit surface policy says so
- after semantic state is non-failing

Reason:
- stops style preferences from masquerading as truth governance

---

## §4 Plan

### Phase 1 - Interop Model Layer
1. Add `SemanticVsPerceptualDecisionState` enum.
2. Add `PerceptualAttachmentSummary` model.
3. Add `JointFailureSurface` model.
4. Add `JointValidatorRoutingDecision` model.
5. Add `DirectionalIntegrityInteropReport` model.

### Phase 2 - DI Engine Interop Composition
6. Add optional perceptual attachment input handling to DI-side composition utility.
7. Preserve raw `DirectionalIntegrityReport` generation unchanged.
8. Add composition function that derives combined state from semantic + perceptual decisions.
9. Add policy-aware routing function for mixed outcomes.
10. Add dependency-missing handling for perceptual prerequisite on high-risk surfaces.

### Phase 3 - Surface Policy and Routing Rules
11. Define which surfaces require PI attachment before final release.
12. Define which surfaces allow semantic-only review path temporarily.
13. Define policy for `semantic PASS + perceptual DOWNGRADE`.
14. Define policy for `semantic REVIEW + perceptual PASS`.
15. Define policy for `semantic FAIL + perceptual PASS`.

### Phase 4 - Downstream Integration
16. Add DI-side SDK/helper for downstream consumers to read interop report.
17. Update content/runtime integration points to prefer interop report where available.
18. Preserve legacy `DirectionalIntegrityEngineResult` consumption path where no PI attachment exists.

### Phase 5 - Testing and Migration
19. Extend FR-22 integration tests for interop states.
20. Add tests for missing FR-27 dependency on high-risk surfaces.
21. Add tests for joint report lineage and audit visibility.
22. Add tests ensuring semantic fail remains terminal regardless of perceptual pass.

---

## §5 Schema (Pydantic v2, no Any)

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PerceptualInteropDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    DOWNGRADE = "DOWNGRADE"
    BLOCK = "BLOCK"
    MISSING = "MISSING"


class SemanticVsPerceptualDecisionState(str, Enum):
    SEMANTIC_PASS__PERCEPTUAL_PASS = "SEMANTIC_PASS__PERCEPTUAL_PASS"
    SEMANTIC_PASS__PERCEPTUAL_REVIEW = "SEMANTIC_PASS__PERCEPTUAL_REVIEW"
    SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE = "SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE"
    SEMANTIC_PASS__PERCEPTUAL_BLOCK = "SEMANTIC_PASS__PERCEPTUAL_BLOCK"
    SEMANTIC_PASS__PERCEPTUAL_MISSING = "SEMANTIC_PASS__PERCEPTUAL_MISSING"
    SEMANTIC_REVIEW__PERCEPTUAL_PASS = "SEMANTIC_REVIEW__PERCEPTUAL_PASS"
    SEMANTIC_REVIEW__PERCEPTUAL_REVIEW = "SEMANTIC_REVIEW__PERCEPTUAL_REVIEW"
    SEMANTIC_REVIEW__PERCEPTUAL_DOWNGRADE = "SEMANTIC_REVIEW__PERCEPTUAL_DOWNGRADE"
    SEMANTIC_REVIEW__PERCEPTUAL_BLOCK = "SEMANTIC_REVIEW__PERCEPTUAL_BLOCK"
    SEMANTIC_REVIEW__PERCEPTUAL_MISSING = "SEMANTIC_REVIEW__PERCEPTUAL_MISSING"
    SEMANTIC_FAIL__PERCEPTUAL_PASS = "SEMANTIC_FAIL__PERCEPTUAL_PASS"
    SEMANTIC_FAIL__PERCEPTUAL_REVIEW = "SEMANTIC_FAIL__PERCEPTUAL_REVIEW"
    SEMANTIC_FAIL__PERCEPTUAL_DOWNGRADE = "SEMANTIC_FAIL__PERCEPTUAL_DOWNGRADE"
    SEMANTIC_FAIL__PERCEPTUAL_BLOCK = "SEMANTIC_FAIL__PERCEPTUAL_BLOCK"
    SEMANTIC_FAIL__PERCEPTUAL_MISSING = "SEMANTIC_FAIL__PERCEPTUAL_MISSING"


class JointRoutingAction(str, Enum):
    CONTINUE = "CONTINUE"
    REGENERATE = "REGENERATE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    DOWNGRADE_SURFACE = "DOWNGRADE_SURFACE"
    HOLD_FOR_PERCEPTUAL_PREREQUISITE = "HOLD_FOR_PERCEPTUAL_PREREQUISITE"
    HARD_BLOCK = "HARD_BLOCK"
    CIRCUIT_BREAK = "CIRCUIT_BREAK"


class JointFailureClass(str, Enum):
    NONE = "NONE"
    SEMANTIC_FAILURE = "SEMANTIC_FAILURE"
    PERCEPTUAL_FAILURE = "PERCEPTUAL_FAILURE"
    MIXED_FAILURE = "MIXED_FAILURE"
    MISSING_PERCEPTUAL_PREREQUISITE = "MISSING_PERCEPTUAL_PREREQUISITE"


class PerceptualAttachmentSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    perceptual_report_id: str = Field(..., min_length=3)
    perceptual_decision: PerceptualInteropDecision = Field(...)
    human_congruence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    cognitive_imprint_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    false_depth_detected: bool = Field(default=False)
    dead_polish_detected: bool = Field(default=False)
    dependency_warnings: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)
    lineage_refs: list[str] = Field(default_factory=list)


class JointFailureSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")
    failure_class: JointFailureClass = Field(...)
    combined_state: SemanticVsPerceptualDecisionState = Field(...)
    semantic_failure_present: bool = Field(...)
    perceptual_failure_present: bool = Field(...)
    missing_perceptual_prerequisite: bool = Field(...)
    summary: str = Field(..., min_length=1)
    blocking_reasons: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)


class JointValidatorRoutingDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: JointRoutingAction = Field(...)
    should_continue_automation: bool = Field(...)
    should_queue_operator_review: bool = Field(...)
    should_trigger_regeneration: bool = Field(...)
    should_trip_circuit_break: bool = Field(...)
    explanation: str = Field(..., min_length=1)


class DirectionalIntegrityInteropReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    interop_report_id: str = Field(..., min_length=3)
    semantic_report_id: str = Field(..., min_length=3)
    semantic_decision: str = Field(..., min_length=3)
    combined_state: SemanticVsPerceptualDecisionState = Field(...)
    semantic_report_generated_at_utc: datetime = Field(...)
    perceptual_attachment: Optional[PerceptualAttachmentSummary] = Field(default=None)
    failure_surface: JointFailureSurface = Field(...)
    routing_decision: JointValidatorRoutingDecision = Field(...)
    lineage_refs: list[str] = Field(default_factory=list)
    dependency_warnings: list[str] = Field(default_factory=list)
```

### Semantic Ownership Mapping
- `DirectionalIntegrityReport` remains the semantic source of truth
- `DirectionalIntegrityInteropReport` is a wrapper, not a replacement

### Perceptual Attachment Mapping
The perceptual attachment may carry only summary fields needed for routing and operator clarity.
It must not inline the full FR-27 report structure unless an adapter explicitly maps it.

### Combined-State Resolver Rules
1. If semantic decision is `FAIL`, combined state is always one of `SEMANTIC_FAIL__*`.
2. If semantic decision is `REVIEW`, PI pass cannot elevate to semantic pass.
3. If semantic decision is `PASS`, PI may keep pass, force review, force downgrade, or force policy block.
4. Missing perceptual prerequisite becomes its own state, not a null hidden edge case.

---

## §6 Fallback and Failure-State Matrix

### Interop Availability Modes

#### Mode A - Semantic Only, Low-Risk Surface
- semantic DI present
- no perceptual attachment
- low-risk planning or internal review surface

Result:
- semantic result may proceed as legacy FR-22 behavior
- interop report optional

#### Mode B - Semantic Only, High-Risk Surface Requiring PI
- semantic DI present
- no perceptual attachment
- high-risk public/commercial/render surface

Result:
- do not silently pass
- combined state = `SEMANTIC_PASS__PERCEPTUAL_MISSING` or equivalent
- route = `HOLD_FOR_PERCEPTUAL_PREREQUISITE` or stronger policy block

#### Mode C - Semantic Pass, Perceptual Review
- truth preserved
- delivery uncertain

Result:
- review or regeneration depending on surface

#### Mode D - Semantic Pass, Perceptual Downgrade
- truth preserved
- delivery too dead, false-deep, synthetic, or weak

Result:
- downgrade surface or block based on policy

#### Mode E - Semantic Fail, Perceptual Pass
- alive but corrupt

Result:
- fail remains fail
- perceptual pass retained only as diagnostic context, never routing override

### Canonical Failure-State Matrix

| Combined State | Failure Class | Default Routing |
|---|---|---|
| `SEMANTIC_PASS__PERCEPTUAL_PASS` | `NONE` | continue |
| `SEMANTIC_PASS__PERCEPTUAL_REVIEW` | `PERCEPTUAL_FAILURE` | review / regenerate |
| `SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE` | `PERCEPTUAL_FAILURE` | downgrade or block by policy |
| `SEMANTIC_PASS__PERCEPTUAL_BLOCK` | `PERCEPTUAL_FAILURE` | block |
| `SEMANTIC_PASS__PERCEPTUAL_MISSING` | `MISSING_PERCEPTUAL_PREREQUISITE` | hold or review by policy |
| `SEMANTIC_REVIEW__PERCEPTUAL_PASS` | `SEMANTIC_FAILURE` | review |
| `SEMANTIC_REVIEW__PERCEPTUAL_REVIEW` | `MIXED_FAILURE` | review |
| `SEMANTIC_REVIEW__PERCEPTUAL_DOWNGRADE` | `MIXED_FAILURE` | review or block by policy |
| `SEMANTIC_REVIEW__PERCEPTUAL_BLOCK` | `MIXED_FAILURE` | block |
| `SEMANTIC_REVIEW__PERCEPTUAL_MISSING` | `MIXED_FAILURE` | review / hold |
| `SEMANTIC_FAIL__PERCEPTUAL_PASS` | `SEMANTIC_FAILURE` | hard block |
| `SEMANTIC_FAIL__PERCEPTUAL_REVIEW` | `SEMANTIC_FAILURE` | hard block |
| `SEMANTIC_FAIL__PERCEPTUAL_DOWNGRADE` | `MIXED_FAILURE` | hard block |
| `SEMANTIC_FAIL__PERCEPTUAL_BLOCK` | `MIXED_FAILURE` | hard block |
| `SEMANTIC_FAIL__PERCEPTUAL_MISSING` | `SEMANTIC_FAILURE` | hard block |

### Rejection Conditions
Reject any interop implementation that:

- upgrades semantic fail because PI passed
- downgrades semantic truth into style commentary only
- silently ignores missing PI requirement on high-risk surfaces
- emits a joint report without preserving original semantic report id and lineage refs

---

## §7 Tasks

### Task Group A - Model Updates
- [ ] Add `SemanticVsPerceptualDecisionState`
- [ ] Add `PerceptualAttachmentSummary`
- [ ] Add `JointFailureSurface`
- [ ] Add `JointValidatorRoutingDecision`
- [ ] Add `DirectionalIntegrityInteropReport`

### Task Group B - DI Service Interop
- [ ] Add pure composition helper that accepts `DirectionalIntegrityReport` and optional `PerceptualAttachmentSummary`
- [ ] Add explicit state resolver for semantic/perceptual combinations
- [ ] Add policy-aware routing resolver for mixed outcomes
- [ ] Add missing-PI prerequisite path for high-risk surfaces

### Task Group C - Adapter and SDK Layer
- [ ] Add DI-side adapter interface that can accept future FR-27 output summaries
- [ ] Add helper for downstream consumers to request interop packet instead of only raw DI result
- [ ] Preserve legacy raw-DI path for consumers that are not yet PI-aware

### Task Group D - Pipeline Integration
- [ ] Update compile/runtime integration guidance so `content_machine.py` and future consumers can read interop packet
- [ ] Keep DI request validation unchanged
- [ ] Keep DI report generation unchanged
- [ ] Ensure interop wrapper is post-semantic, pre-release routing

### Task Group E - Tests
- [ ] Add combined-state resolver tests
- [ ] Add semantic precedence tests
- [ ] Add high-risk missing-PI prerequisite tests
- [ ] Add lineage and report-wrapping tests

---

## §8 Acceptance Criteria

### AC-22-SFL-1
Given a semantic `FAIL` and a perceptual `PASS`,
when the interop report is composed,
then the routing result must remain blocking and the combined state must be `SEMANTIC_FAIL__PERCEPTUAL_PASS`.

Failure example:
- the artifact proceeds because it feels strong or human despite semantic corruption.

### AC-22-SFL-2
Given a semantic `PASS` and a perceptual `DOWNGRADE`,
when the target surface is high-risk,
then the interop report must route to downgrade or block according to policy, without mutating the semantic report itself.

Failure example:
- DI report is rewritten to `REVIEW` just because PI found dead polish.

### AC-22-SFL-3
Given no perceptual attachment on a surface that requires perceptual validation,
then the interop report must emit a missing-prerequisite failure class and must not silently continue.

Failure example:
- commercial trust-transfer content ships on semantic pass alone with no perceptual guard.

### AC-22-SFL-4
Given a semantic `REVIEW` and a perceptual `PASS`,
then the combined state must remain review-oriented and PI pass must be marked advisory only.

Failure example:
- semantic ambiguity is hidden because the content sounds alive.

### AC-22-SFL-5
Given both DI and PI outputs are available,
then the joint report must preserve:

- original semantic report id
- combined state
- perceptual attachment summary
- lineage refs

Failure example:
- downstream systems receive only a flattened overall score and cannot tell which layer failed.

### AC-22-SFL-6
Given a high-risk surface and semantic fail caused by hard-negative adjacency,
then perceptual attachment presence or absence must not affect the hard block.

Failure example:
- perceptual review causes the engine to downgrade instead of block.

### AC-22-SFL-7
Given a low-risk semantic-planning surface and no perceptual attachment,
then the legacy semantic-only path may continue if policy allows, while still making the absence explicit when an interop report is requested.

Failure example:
- the engine either hard-fails all low-risk planning without PI or hides that PI was absent.

---

## §9 Dependencies

### Required Upstream Dependencies
- `FR-ERA3-22` existing semantic validator implementation
- `PRD-01`, `PRD-02`, `PRD-08`
- SDA query/crosswalk and hard-negative substrate already assumed by FR-22

### Planned Interop Dependencies
- `FR-ERA3-27`
  - perceptual evaluator spec exists
  - backend implementation files not yet present
- `FR-ERA3-28`
  - perceptual failure corpus spec exists
  - strengthens perceptual side but does not alter DI ownership

### Known Downstream Consumers
- `FR-ERA3-16` updated CCF runtime
- `FR-ERA3-12` updated CMF rendering/runtime
- `FR-ERA3-18` updated CBCS runtime
- `FR-ERA3-05-CORE` updated reactions runtime

### Dependency Risks
1. FR-27 code absent
   - mitigate with optional typed attachment summary and adapters
2. FR-27 tests absent
   - mitigate with DI-side interop tests and future FR-27 conformance tests
3. consumer confusion between semantic fail and perceptual downgrade
   - mitigate with explicit combined-state enum and joint failure matrix

---

## §10 Testing

### New / Updated Test Files
Update or create:

- `tests/integration/test_era3_fr22_directional_integrity_engine.py`
- `tests/integration/test_era3_fr22_directional_integrity_interop.py`
- `tests/integration/test_era3_fr22_directional_integrity_interop_fallbacks.py`

### Required Test Classes

#### A. Contract Tests
- interop report wraps semantic report without mutation
- optional perceptual attachment serializes cleanly
- combined-state enum resolves correctly for every allowed pair

#### B. Precedence Tests
- semantic fail + perceptual pass => hard block
- semantic review + perceptual pass => review
- semantic pass + perceptual downgrade => downgrade/block by policy

#### C. Missing Dependency Tests
- high-risk surface + missing perceptual attachment => hold/review/block by policy
- low-risk planning + missing perceptual attachment => legacy semantic path allowed

#### D. Lineage Tests
- interop report keeps semantic report id
- interop report keeps semantic lineage refs
- perceptual attachment lineage refs remain separate and additive

#### E. Downstream Routing Tests
- downstream receives one routing action object
- `should_continue_automation`
- `should_queue_operator_review`
- `should_trigger_regeneration`
- `should_trip_circuit_break`
  all remain deterministic

### Seed Test Scenarios

1. **Semantically healthy, perceptually alive**
   - semantic PASS
   - perceptual PASS
   - expected continue

2. **Semantically healthy, perceptually dead**
   - semantic PASS
   - perceptual DOWNGRADE
   - expected downgrade/review depending on surface

3. **Semantically corrupt, perceptually compelling**
   - semantic FAIL
   - perceptual PASS
   - expected hard block

4. **Semantically uncertain, perceptually polished**
   - semantic REVIEW
   - perceptual PASS
   - expected review

5. **High-risk surface missing perceptual prerequisite**
   - semantic PASS
   - perceptual MISSING
   - expected hold/review/block by policy

### Manual Validation Checklist
- verify DI report remains unchanged when interop wrapper is added
- verify no consumer can confuse PI downgrade with semantic corruption
- verify no semantic fail is softened by style success
- verify missing FR-27 implementation state is explicit in code comments or adapter boundaries, not hidden behind magic imports

---

**End of Spec**
