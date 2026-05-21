# FR-ERA3-16: Archetype Container Runtime Technical Specification

## 1. Files Read
<!-- UPDATED: Added mandatory SDA source set and PRD modules to ensure semantic validation context is preserved. -->
- `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` (Original)
- `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
- `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (Wave 0)
- `docs/prd/modules/PRD_08_Conscious_Primitives.md`
- `lab/semantic_discernment_architecture_content_engine_v_1.md`
- `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`

## 2. Overview
<!-- UPDATED: Redefined the runtime objective to explicitly incorporate SDA as a mandatory semantic validation layer. -->
The Archetype Container Runtime is the core execution engine of the CCF Content Factory. It is responsible for taking a selected primitive coalition, wrapping it in an appropriate structural archetype, enforcing anti-centroid constraints, and producing a validated JIT script contract for downstream rendering. 

This update integrates the **Semantic Discernment Architecture (SDA)** into the existing runtime as a mandatory semantic validation wrapper. It prevents "structure-first but direction-blind compilation" by ensuring every artifact maintains directional integrity, existential alignment, and archetypal coherence before it reaches production. The existing service architecture is preserved; SDA acts as an adversarial stage-gate surrounding the containerization process.

## 3. Context & Baseline
<!-- UPDATED: Replaced the old runtime law with the Wave 0 PRD SDA-aware runtime law and added scaling constraints. -->
**Baseline Architecture:**
The pre-SDA runtime followed this sequence: `signal -> coach reaction -> primitive coalition -> archetype container -> JIT script contract -> render blueprint`

**Updated Runtime Architecture (Wave 0):**
The runtime must now explicitly execute the following pipeline:
`signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> directional integrity validation -> JIT script contract -> render blueprint`

**Key SDA Concepts Introduced:**
- **Invariant Gravity:** The inherent human weight an existential invariant carries.
- **Invariant Activation Intensity:** How strongly the current artifact activates an invariant.
- **Invariant Resonance Multiplier:** How much the active invariant amplifies emotional charge and memory persistence when combined with the coalition and geometry.
- **Recursive Patterns & Emergent Contextual Invariants:** Runtime semantic-dynamics objects guiding field constraints.
- **Feedback-Loop Projections:** Ensuring the semantic trajectory does not drift under mutation.

## 4. Implementation Plan
<!-- UPDATED: Detailed the SDA stage gates injected into the ArchetypeContainerRuntimeService. -->
The `ArchetypeContainerRuntimeService` will be updated to execute SDA validation passes. This is a non-destructive wrap of the existing logic.

1.  **Invariant Field Processing:** Before the primitive coalition is finalized, the runtime extracts the `InvariantFieldPacket` to capture `Invariant Activation Intensity`.
2.  **Edge Product & Geometry Selection:** The resulting `EdgeProductPacket` dictates the `ArchetypalGeometryPacket`. The system selects the archetype container based on this geometry.
3.  **Representation Geometry Formulation:** The system infers the `RepresentationGeometryPacket` to capture authority flow, status distribution, and directional risks.
4.  **Directional Integrity Validation:** An adversarial check is executed against the populated container, issuing a `DirectionalIntegrityReport`.
5.  **Hard Negative Evaluation:** The system performs a contrastive check to avoid deceptively close semantic failures, logging a `HardNegativeEvaluationReport`.
6.  **JIT Script Contract Locking:** Only if all SDA validators pass is the `CCFRoutingRecommendation` generated and the contract locked.

## 5. Schema, Code, and Data Definitions
<!-- UPDATED: Added SDA packet contracts to the runtime schema requirements and updated CCFRoutingRecommendation. -->
```python
# pydantic/sda_contracts.py

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class InvariantFieldPacket(BaseModel):
    active_invariants: List[str]
    invariant_weights: Dict[str, float]
    invariant_activation_intensity: float
    evidence_anchors: List[str]
    pressure_summary: str

class ArchetypalGeometryPacket(BaseModel):
    active_topology: str
    authority_flow: str
    agency_distribution: str
    sacrifice_transformation_pattern: str

class RepresentationGeometryPacket(BaseModel):
    authority_encoding: str
    fear_weighting: float
    status_distribution: str
    identity_framing: str
    directional_risks: List[str]

class SpeciesHypothesisPacket(BaseModel):
    derived_species_guess: str
    invariant_lineage: List[str]
    geometry_lineage: List[str]
    shadow_drift_notes: Optional[str]

class DirectionalIntegrityReport(BaseModel):
    validator_verdict: str  # "PASS" | "FAIL" | "WARN"
    drift_flags: List[str]
    preserved_invariants: List[str]
    invariant_resonance_multiplier: float
    mutation_test_outcomes: Dict[str, str]

class HardNegativeEvaluationReport(BaseModel):
    evaluation_verdicts: Dict[str, str]
    deceptive_adjacency_risk: float
    failing_divergence_axes: List[str]
    escalation_state: Optional[str]

# Updated CCFRoutingRecommendation payload
class CCFRoutingRecommendation(BaseModel):
    destination_families: List[str]
    format_surfaces: List[str]
    coalition_signature_id: str
    archetype_container_id: str
    # SDA Injection
    directional_integrity_report: DirectionalIntegrityReport
    hard_negative_report: Optional[HardNegativeEvaluationReport]
```

## 6. Backward Compatibility & Migration
<!-- UPDATED: Enforced the constraint that existing DEP-IDs are unmodified and old endpoints handle fallback. -->
-   **Zero Modification to DEP-IDs:** Existing deployment IDs for the container service remain untouched.
-   **Fallback Support:** If SDA validation times out or the semantic registry is unreachable, the runtime will fail-closed and return a `503 Service Unavailable` with a dedicated `SDA_TIMEOUT` error code, preventing unchecked content generation. 

## 7. Tasks & Work Breakdown
<!-- UPDATED: Added tasks specific to wiring SDA packet generation and validation into the runtime engine. -->
-   [ ] Task 1: Integrate `pydantic/sda_contracts.py` into the core models directory.
-   [ ] Task 2: Refactor `ArchetypeContainerRuntimeService` to require `InvariantFieldPacket` generation prior to containerization.
-   [ ] Task 3: Implement the `DirectionalIntegrityValidation` stage gate before JIT contract lock.
-   [ ] Task 4: Implement `HardNegativeEvaluation` contrastive checking.
-   [ ] Task 5: Update `CCFRoutingRecommendation` emission to include SDA reports.
-   [ ] Task 6: Add logging for `Invariant Gravity`, `Activation Intensity`, and `Resonance Multiplier` telemetry.

## 8. Acceptance Criteria
<!-- UPDATED: Bound acceptance to CBAR mandates, specifically Anti-Slop and Traceability. -->
-   **Traceability:** Every JIT script contract must carry a lineage mapping back to the `InvariantFieldPacket` and `ArchetypalGeometryPacket`.
-   **Anti-Slop Validation:** The `DirectionalIntegrityReport` must explicitly register a `PASS` before the archetype container allows routing to downstream rendering.
-   **Deterministic Flow:** The updated 10-step runtime law (`signal -> ... -> render blueprint`) executes synchronously and sequentially without skipping SDA validation.

## 9. Dependencies
<!-- UPDATED: Explicitly linked SDA Ontology Registry alongside the Primitive Registry. -->
-   `Primitive Registry Service`: For resolving the `primitive coalition`.
-   `SDA Ontology Registry`: For resolving `Existential Invariants`, `Representation Geometries`, and `Archetypal Geometries`.
-   `Edging & Content Orchestrator`: Provides the initial `signal`, `coach reaction`, and `edge product`.

## 10. Testing & Verification
<!-- UPDATED: Mandated hard-negative contrast testing to verify SDA failure detection. -->
-   **Contrastive Stress Test:** Inject known "hard negative" payload (e.g., superficially sound but semantically drifting) into the runtime; verify that `DirectionalIntegrityReport` fails and blocks rendering.
-   **Resonance Multiplier Validation:** Assert that the generated `Invariant Resonance Multiplier` is mathematically derived from the active invariant field and is not a static fallback value.
-   **End-to-End Pipeline:** Run `ArchetypeContainerRuntimeService.execute()` from end to end and assert the output `CCFRoutingRecommendation` structure contains complete SDA metrics.
