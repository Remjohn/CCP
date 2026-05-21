# Tech-Spec: FR-ERA3-22 - Directional Integrity Engine
**Created:** 2026-05-12  
**Status:** Ready for Development  
**Version:** 1.0 (ERA3 Architecture - SDA Foundation)  
**Phase:** 6 - Semantic Discernment Foundation  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROMPT LOADED:     P6_S37_FR-ERA3-22_Directional_Integrity_Engine.md. Confirmed this spec must define the new semantic validator engine, include a pre-work trace, prove source grounding, declare pass/review/fail behavior, and distinguish blocking vs advisory drift.
2. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed required 10-section format, file-read log, architecture traceability, typed schema requirement, and implementation-first brownfield style.
3. SOURCE PRD READ:   PRD-02 §3.1/§3.2/§3.4A. Confirmed compiler/runtime law now includes `directional integrity validation` after `archetype container` and before `JIT script contract`; confirmed new packets `InvariantFieldPacket`, `ArchetypalGeometryPacket`, `RepresentationGeometryPacket`, `SpeciesHypothesisPacket`, `DirectionalIntegrityReport`, and `HardNegativeEvaluationReport`.
4. SOURCE PRD READ:   PRD-03 §3.3A + Brownfield §1.5. Proof quote captured: rendering is not allowed to preserve only emotional intensity while mutating semantic direction. Confirmed CMF must preserve active invariant field, intended archetypal geometry, admissible representation geometry, and downstream directional integrity.
5. SOURCE PRD READ:   PRD-04 §3.5C + Brownfield §1.5. Confirmed CVE surfaces must not create belonging, status, or identity pressure loops that violate SDA direction even when interaction metrics look strong.
6. SOURCE PRD READ:   PRD-05 §7.1A + Brownfield §1.5. Proof quote captured: a coaching intervention can improve short-term energy while still distorting identity, misreading local invariants, or reinforcing an unhealthy loop. Confirmed CBCS requires meaning-aware interpretation, not behavior-only success.
7. SOURCE PRD READ:   PRD-06 §5.3A + Brownfield §1.4. Proof quote captured: reactions constantly activate status, belonging, authority, shame, redemption, conflict, recognition, and tribal alignment, so the system must ask which invariants are activated, what edge product was operationalized, what representation geometry is taught, and what feedback loops are normalized.
8. SOURCE PRD READ:   PRD-07 §4.4A + Brownfield §1.6. Confirmed long-form webinar arcs can retain persuasive shape while flattening invariant gravity or drifting from earned authority into manipulative pressure.
9. SOURCE PRD READ:   PRD-09 §5.3A + Brownfield §1.4. Proof quote captured: growth/commercial systems are where deceptively close semantic corruption is especially dangerous. Confirmed commercial flows must distinguish healthy authority from prestige theater, belonging from social capture, urgency from coercion, and proof from vanity.
10. SDA CORE DOC READ: lab/semantic_discernment_architecture_content_engine_v_1.md. Validator-relevant claim captured: the main failure class is deceptively close output that passes superficial coherence while corrupting meaning, identity, and trajectory. Confirmed required evaluation layers: existential invariant analysis, representation geometry analysis, archetypal structure validation, recursive hard-negative adversarial analysis.
11. SDA TAXONOMY DOC READ: lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md. Validator-relevant claim captured: `Directional Integrity Policy` is a validation-policy artifact, `Hard Negative` is an adversarial evaluation asset, and `DirectionalIntegrityReport` / `HardNegativeEvaluationReport` are runtime execution packets. Confirmed role-before-schema, no-false-registry, and scalar separation rules.
12. PPA DOC READ:     Perceptual_Primitives_Architecture.md. Validator-relevant claim captured: primitives are not edges; the stack is `CRAL evidence -> primitive spaces -> candidate survival -> coalition signature -> edge product -> CCF routing`. Confirms FR-ERA3-22 must validate the emergent semantic product, not primitive ontology itself.
13. EDGING DOC READ:  Matrix of Edging.md. Validator-relevant claim captured: an edge is a high-magnitude tension site at a meaningful human boundary; broad primary signal is pre-trigger and edge product is post-trigger. Confirms validator inputs must distinguish pre-trigger field from operationalized force.
14. FOUNDATION FR READ: FR-ERA3-20. Confirmed canonical registries are `Existential Invariants`, `Representation Geometries`, `Archetypal Geometries`, and `Species Composition Grammar`; confirmed scalar separation: `invariant_gravity` is canonical while activation/resonance are runtime-only.
15. FOUNDATION FR READ: FR-ERA3-21. Confirmed the SDA query service owns canonical ontology/grammar lookup and maintained crosswalk resolution; confirmed non-canonical runtime objects such as `DirectionalIntegrityReport`, `HardNegativeEvaluationReport`, `RecursivePattern`, and `FeedbackLoop` are not query surfaces and must be produced by this engine or later engines.
16. BACKEND FILE READ: src/ccp/services/content_machine.py. Verified live integration target `ContentMachinePipeline.process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult` and existing internal validation staging precedent through `TriplePassValidator.validate(...)`.
17. BACKEND FILE READ: src/ccp/services/canvas_composition_service.py. Verified review/regeneration precedent through `create_composition(...)`, `approve(...)`, `request_regeneration(...) -> tuple[CanvasComposition, RegenerationRequest]`, `edit_and_approve(...)`, and `validate_edge_bleeds(...)`.
18. BACKEND FILE READ: src/ccp/services/trait_scoring_engine.py. Verified evidence-backed scoring precedent via `TraitScoringEngine.score_all_traits(self) -> list[ScoredTrait]`; confirms DI scoring should preserve per-dimension evidence instead of opaque scalar output.
19. BACKEND FILE READ: src/ccp/services/conversion_sequence_router.py. Verified failure-closed commercial gate precedent: `ConversionSequenceRouter.route(...) -> ConversionSequencePayloadRow` halts on `DormancyGateVerdict.FAIL_DORMANT_ABORT` and pivots on provisional states instead of pretending everything passed.
20. BACKEND FILE READ: src/ccp/core/circuit_breaker.py. Verified explicit halt pattern: `CircuitBreaker.scan_for_crisis(...)`, `activate(...)`, `is_active(...)`, and `reset(...)` show the repository already supports hard-stop semantics with receipt logging and explicit manual reset.
21. BACKEND FILE READ: src/ccp/services/semantic_affinity_guard.py. Confirmed deterministic gate precedent with hard halt (`C06TerminalError`), operator review, fallback-to-review, ghost-variable prevention, and typed clearance decisions.
22. PRIMITIVE YAMLs VERIFIED:
    - EXP-FBK-001 = `RIM Feedback Discipline`
    - EXP-TRG-002 = `Hook Cycle Velocity`
    - EXP-TRS-003 = `Reflective Social Proof (The Status Share)`
    - EXP-PRG-002 = `Discover -> On-board -> Immerse -> Master -> Replay`
    Confirmed these artifacts expose real social/status/feedback/progression pressure examples the validator must sometimes permit and sometimes block depending on representation drift.
23. TEST PATTERNS READ:
    - tests/integration/test_vis07_format_constraint.py = deterministic registry completeness, envelope sealing, and safety-failure assertions
    - tests/integration/test_vis02_tiar_integration.py = active/blocked partitioning, stale fallback, downstream validation, and audit completeness
    These tests confirm the local style for failure-closed gates and traceable audit outputs.
24. TAXONOMY DISTINCTION CONFIRMED:
    - policy = `Directional Integrity Policy`
    - packet = `DirectionalIntegrityReport`, `HardNegativeEvaluationReport`
    - adversarial asset = `Hard Negative`, `Mutation Stress Suite`
    This spec must not collapse those roles into one registry object.
25. WAVE-0 TRACEABILITY NOTE:
    No Phase 6 epic file exists yet. Architectural authority for this spec therefore comes from the Wave 0 PRD updates plus the four SDA main documents and the two foundation FRs above.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S37_FR-ERA3-22_Directional_Integrity_Engine.md` | Prompt scope, mandatory outputs, required proof set |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure and brownfield spec rules |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Core compiler law and SDA packet dependencies |
| 4 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | Representation-preservation requirement for rendering |
| 5 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | Experience-level identity/belonging/status integrity constraints |
| 6 | `docs/prd/modules/PRD_05_CBCS_Law28.md` | Meaning-aware coaching interpretation requirement |
| 7 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Status/belonging/conflict governance in reaction systems |
| 8 | `docs/prd/modules/PRD_07_V2WS_Webinar.md` | Long-form authority/invariant preservation constraints |
| 9 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | Commercial integrity and deceptively-close risk doctrine |
| 10 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Core SDA validator doctrine and failure taxonomy |
| 11 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Artifact taxonomy and role boundaries |
| 12 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Primitive/edge separation and upstream lineage |
| 13 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | Broad-signal vs edge-product distinction |
| 14 | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Canonical SDA ontology/grammar contracts |
| 15 | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | Query/crosswalk ownership and lineage contracts |
| 16 | `src/ccp/services/content_machine.py` | CCF integration target and validation staging precedent |
| 17 | `src/ccp/services/canvas_composition_service.py` | Review/regeneration/approval precedent |
| 18 | `src/ccp/services/trait_scoring_engine.py` | Evidence-backed scoring precedent |
| 19 | `src/ccp/services/conversion_sequence_router.py` | Failure-closed commercial gating precedent |
| 20 | `src/ccp/core/circuit_breaker.py` | Hard-stop, receipt, and reset precedent |
| 21 | `src/ccp/services/semantic_affinity_guard.py` | Typed gate decisions, fallback, and hard-halt precedent |
| 22 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Real feedback primitive and crosswalk anchor |
| 23 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | Real timing primitive and crosswalk anchor |
| 24 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Real social/status primitive and crosswalk anchor |
| 25 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Real progression primitive and crosswalk anchor |
| 26 | `tests/integration/test_vis07_format_constraint.py` | Deterministic gate and audit test precedent |
| 27 | `tests/integration/test_vis02_tiar_integration.py` | Stale fallback and downstream validation test precedent |

---

## 2. Overview

### 2.1 Problem Statement - What breaks without this spec?

Wave 0 and the two foundation FRs established that CCP now has:

- canonical SDA ontology and grammar
- maintained SDA crosswalks
- an updated CCF runtime law that explicitly inserts directional integrity validation

What the platform still does **not** have is the actual engine that decides whether a candidate artifact preserves or corrupts semantic direction.

Without `FR-ERA3-22`:

- `PRD-02` is incomplete in practice. The compiler law names `directional integrity validation`, but no executable validator exists between archetype container selection and JIT contract generation.
- downstream organisms will drift independently. CCF, CMF, CBCS, Reactions, Webinar, and Commercial flows will each invent local heuristics for “good meaning” and silently disagree.
- high-performing but semantically corrupt outputs will ship. This is the exact “deceptively close” failure class the SDA core document warns about.
- the system will confuse polish with direction. A clip, scorecard, webinar transition, or referral card can feel sharp while teaching prestige theater, tribal capture, or coercive belonging.
- hard-negative awareness will remain decorative. `Hard Negative` and `Mutation Stress Suite` will exist conceptually, but no runtime contract will say when adjacency is acceptable, review-worthy, or blocking.
- failure handling will be inconsistent. Some systems may silently degrade to pass when ontology or crosswalk dependencies fail, which directly violates the failure-closed doctrine now present in the PRDs.

### 2.2 Solution

Create a new service, `DirectionalIntegrityEngine`, that evaluates candidate semantic outputs against intended SDA direction and returns a typed, evidence-backed decision:

- `PASS` = semantic direction preserved and safe to continue
- `REVIEW` = ambiguity or moderate drift exists; safe continuation depends on surface risk and downstream policy
- `FAIL` = semantic direction is compromised or cannot be confidently validated; execution blocks or reroutes

The engine will:

- consume canonical ontology/grammar via `FR-ERA3-20`
- consume crosswalk and lineage resolution via `FR-ERA3-21`
- evaluate candidate outputs on four mandatory score dimensions:
  - `invariant_preservation_score`
  - `representation_drift_score`
  - `hard_negative_adjacency_score`
  - `trajectory_risk_score`
- preserve per-dimension evidence, not only scalars
- distinguish **blocking drift** from **advisory drift**
- expose deterministic behavior for high-risk downstream consumers such as CMF release, commercial trust transfer, and public social proof artifacts
- fail closed when required dependencies or validator evidence are missing

### 2.3 Scope

**In scope**

- engine input contract and output report
- pass/review/fail decision states
- policy evaluation against invariant, geometry, species, and hard-negative expectations
- blocking vs advisory drift rules by downstream domain
- service integration patterns for:
  - CCF
  - CMF
  - CBCS
  - Reactions
  - Webinar
  - Commercial / Silent Referral / OFO-like flows
- failure-closed and circuit-breaker style fallback behavior
- audit logging and integration test design

**Out of scope**

- authoring SDA ontology or crosswalk files (`FR-ERA3-20`, `FR-ERA3-21`)
- maintaining the hard-negative corpus itself (`FR-ERA3-24`)
- longitudinal recursive dynamics computation (`FR-ERA3-23`)
- generic LLM search policy or inference-time compute orchestration
- replacing existing domain engines; this engine validates them, it does not own their core generation logic

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | What It Does |
|--------|-----------|--------|--------------|
| `DEP-SDA-020` | `DirectionalIntegrityEngine` | FR-ERA3-22 | Main orchestrator for semantic-direction validation |
| `DEP-SDA-021` | `DirectionalIntegrityPolicyRegistry` | FR-ERA3-22 + Taxonomy | Stores compiled validation policy bundles by surface/domain |
| `DEP-SDA-022` | `InvariantPreservationAnalyzer` | FR-ERA3-22 | Scores whether intended existential invariants are preserved |
| `DEP-SDA-023` | `RepresentationDriftAnalyzer` | FR-ERA3-22 | Detects encoding/weighting drift against target representation geometry |
| `DEP-SDA-024` | `HardNegativeAdjacencyAnalyzer` | FR-ERA3-22 | Scores distance to known deceptive near-neighbors |
| `DEP-SDA-025` | `TrajectoryRiskAnalyzer` | FR-ERA3-22 | Estimates whether downstream meaning trajectory is drifting into harmful patterns |
| `DEP-SDA-026` | `DirectionalIntegrityDecisionRouter` | FR-ERA3-22 | Maps raw scores to `PASS`, `REVIEW`, or `FAIL` using surface policy |
| `DEP-SDA-027` | `DirectionalIntegrityReport` | PRD-02 / FR-ERA3-22 | Runtime packet passed to downstream engines |
| `DEP-SDA-028` | `HardNegativeEvaluationReport` | PRD-02 / FR-ERA3-22 | Runtime packet preserving hard-negative evidence and adjacency |
| `DEP-SDA-029` | `SDAQueryAndCrosswalkService` | FR-ERA3-21 | Canonical ontology/grammar and crosswalk resolution dependency |
| `DEP-SDA-030` | `SDAOntologyRegistry` | FR-ERA3-20 | Source of invariant, geometry, and species-composition canonical truth |
| `DEP-SDA-031` | `InvariantFieldPacket` | PRD-02 / FR-ERA3-22 | Primary field input conveying activated invariants |
| `DEP-SDA-032` | `ArchetypalGeometryPacket` | PRD-02 / FR-ERA3-22 | Structural meaning input defining persuasive geometry |
| `DEP-SDA-033` | `RepresentationGeometryPacket` | PRD-02 / FR-ERA3-22 | Encoding direction input conveying target authority/belonging mode |
| `DEP-SDA-034` | `SpeciesHypothesisPacket` | PRD-02 / FR-ERA3-22 | Derived form context indicating specific target species |
| `DEP-SDA-035` | `DirectionalIntegrityRequest` | FR-ERA3-22 | Incoming evaluation request aggregating all candidate context |

### 3.2 Why This Engine Exists in the SDA Stack

This engine sits after ontology resolution and before irreversible downstream execution.

Target runtime stack:

```text
signal
-> coach reaction / source artifact
-> invariant field
-> primitive coalition
-> edge product
-> archetypal geometry check
-> archetype container
-> directional integrity validation   <-- FR-ERA3-22
-> JIT script contract / render blueprint / commercial payload
```

This placement follows the four SDA main documents:

- the SDA core doc defines the target problem as **directional corruption despite surface coherence**
- the taxonomy says `Directional Integrity Policy` is a policy artifact and `DirectionalIntegrityReport` is a runtime packet
- Perceptual Primitives Architecture says primitives are not edges
- Matrix of Edging says broad signal and edge product are distinct phases

So this engine must validate the **emergent semantic product** given its intended field and geometry lineage, not treat primitive selection or affective excitement as sufficient proof.

### 3.3 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `content_machine.py` | `src/ccp/services/content_machine.py` | Main CCF integration target. `ContentMachinePipeline.process_session(...)` is the clearest location for blocking DI checks before content compilation leaves semantic planning. |
| `canvas_composition_service.py` | `src/ccp/services/canvas_composition_service.py` | Review/regeneration precedent. DI `REVIEW` and `FAIL` must map cleanly to regeneration or operator review paths similar to `request_regeneration(...)`. |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Evidence-backed scoring style precedent. DI dimensions should emit cited evidence and rationale, not only opaque numeric grades. |
| `conversion_sequence_router.py` | `src/ccp/services/conversion_sequence_router.py` | Commercial gate precedent. `FAIL_DORMANT_ABORT` / provisional reroute show the repo already prefers explicit block-or-pivot behavior over silent permissiveness. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Hard-stop precedent. DI must support “automation halted until explicit correction” semantics on the highest-risk surfaces. |
| `semantic_affinity_guard.py` | `src/ccp/services/semantic_affinity_guard.py` | Deterministic threshold/fallback precedent with `PASS`, `OPERATOR_REVIEW`, and terminal failure. |

### 3.4 Downstream Surface Classes

Not every consumer carries the same risk. This engine must know the difference.

| Surface Class | Examples | Default DI Behavior |
|---------------|----------|---------------------|
| `SEMANTIC_PLANNING` | CCF planning, edge-product shaping | `FAIL` blocks compile; `REVIEW` may allow internal iteration but not final release |
| `RENDER_RELEASE` | CMF render/export/share artifacts | `FAIL` blocks export; `REVIEW` routes to regeneration or editor review |
| `COACHING_INTERVENTION` | CBCS interpretation, coach nudges | `FAIL` blocks delivery; `REVIEW` may queue operator review depending on intimacy and identity stakes |
| `SOCIAL_REACTION` | Debate, Duel, Authority Quiz, Tierlist | `FAIL` blocks score reveal/share path; `REVIEW` may allow local gameplay but blocks public or status-bearing artifacts |
| `LONG_FORM_AUTHORITY` | Webinar slide prompts, recap CTAs | `FAIL` blocks publish or CTA transition; `REVIEW` routes to edit before release |
| `COMMERCIAL_TRUST_TRANSFER` | Silent Referral, proof cards, conversion copy | `FAIL` always blocks; `REVIEW` blocks auto-send and requires explicit human approval |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|----------------------|--------------|
| Make DI a separate engine, not a method inside `semantic_affinity_guard.py` | SDA direction is broader than mood/pain affinity and already has separate ontology/crosswalk sources | Extend semantic affinity into universal meaning validator | Conflates pain-domain safety with worldview direction and breaks the taxonomy |
| Use explicit `PASS / REVIEW / FAIL` states | Matches existing repository gate style and supports surface-specific routing | Binary pass/fail only | Too coarse for ambiguous but important drift cases |
| Preserve evidence per score dimension | Mirrors `TraitScoringEngine` and supports auditability | Emit only summary score | Impossible to debug or improve without evidence |
| Fail closed on missing ontology/crosswalk/policy dependencies for high-risk surfaces | Directly required by prompt and PRDs | Soft-pass on dependency outage | Would allow the most sensitive surfaces to ship without validation |
| Keep hard negatives external but callable | Taxonomy says hard negatives are adversarial assets, not registry entries | Embed hard-negative descriptions directly in DI policy | Collapses policy with benchmark corpus and prevents independent evolution |

---

## 4. Implementation Plan

### Phase A: Models and Policy Contracts

- [ ] **Task 1:** Create `src/ccp/models/directional_integrity_models.py` with:
  - request models
  - policy models
  - evidence models
  - scorecard models
  - decision/report packet models
- [ ] **Task 2:** Define enums for:
  - `DirectionalIntegrityDecision`
  - `DirectionalIntegritySurfaceClass`
  - `DirectionalIntegritySeverity`
  - `DirectionalIntegrityFallbackReason`
  - `DirectionalIntegrityResolutionPath`
- [ ] **Task 3:** Add constants for default thresholds and domain-policy profiles.
- [ ] **Task 4:** Define `DIRECTIONAL_INTEGRITY_AUDIT_SQL` and receipt-stage names for CI and runtime audit consistency.

### Phase B: Core Analyzer Services

- [ ] **Task 5:** Create `src/ccp/services/directional_integrity_engine.py` with `DirectionalIntegrityEngine`.
- [ ] **Task 6:** Implement `InvariantPreservationAnalyzer`. Must use LLM prompt contract (`PROMPT-DI-INV`) to compare `candidate_text` against canonical invariant profiles. Also calculate and populate the `invariant_resonance_multiplier` based on intensity match vs canonical profile.
- [ ] **Task 7:** Implement `RepresentationDriftAnalyzer`. Must use LLM prompt contract (`PROMPT-DI-REP`) to detect prestige/coercive weighting vs intended representation geometry. Calculate and populate `identity_proximity` via vector distance to intended identity frame.
- [ ] **Task 8:** Implement `HardNegativeAdjacencyAnalyzer` with an abstract dependency interface that later consumes `FR-ERA3-24`. Calculate and populate `symbolic_density` as the ratio of high-gravity symbols to total tokens.
- [ ] **Task 9:** Implement `TrajectoryRiskAnalyzer`. Must use a rule-based heuristic check combined with an LLM prompt (`PROMPT-DI-TRAJ`) mapping output species against downstream risk matrices.
- [ ] **Task 10:** Implement `DirectionalIntegrityDecisionRouter` that maps dimensional evidence to `PASS`, `REVIEW`, `FAIL`.

### Phase C: Dependency Integration and Fallback

- [ ] **Task 11:** Integrate `FR-ERA3-21` query service for invariant, geometry, species-composition, and crosswalk resolution.
- [ ] **Task 12:** Create a `DirectionalIntegrityPolicyRegistry` loaded from repo policy YAML or typed Python config.
- [ ] **Task 13:** Add failure-closed behavior:
  - missing ontology/policy
  - missing crosswalk lineage
  - hard-negative service unavailable
  - null packet / ghost variable
- [ ] **Task 14:** Add receipt-chain logging for:
  - evaluation started
  - policy resolved
  - dependency degraded
  - review requested
  - execution blocked
  - pass released

### Phase D: Generic Integration SDKs

- [ ] **Task 15:** Build the `DIServiceClient` SDK for upstream semantic planning execution boundaries. (Actual CCF integration is delegated to FR-ERA3-16).
- [ ] **Task 16:** Build the `DIRenderReleaseGuard` SDK for media generation execution boundaries. (Actual CMF integration is delegated to FR-ERA3-12).
- [ ] **Task 17:** Build surface-class helper functions mapping `COMMERCIAL_TRUST_TRANSFER`, `COACHING_INTERVENTION`, `SOCIAL_REACTION`, and `LONG_FORM_AUTHORITY` intents to standard validation payloads. (Actual downstream insertion is delegated to their respective FRs).
- [ ] **Task 18:** Add operator-facing remediation payloads describing which dimension failed and what must be corrected.

### Phase E: Test and Audit Hardening

- [ ] **Task 19:** Create `tests/integration/test_era3_fr22_directional_integrity_engine.py`.
- [ ] **Task 20:** Create `tests/integration/test_era3_fr22_directional_integrity_fallbacks.py`.
- [ ] **Task 21:** Create fixture policies and fixture ontology/crosswalk bundles.
- [ ] **Task 22:** Add representative negative cases for:
  - prestige theater
  - coercive urgency
  - false belonging
  - public-shame reward framing

---

## 5. Primary Output Schema

```python
# src/ccp/models/directional_integrity_models.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class DirectionalIntegrityDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FAIL = "FAIL"


class DirectionalIntegritySurfaceClass(str, Enum):
    SEMANTIC_PLANNING = "SEMANTIC_PLANNING"
    RENDER_RELEASE = "RENDER_RELEASE"
    COACHING_INTERVENTION = "COACHING_INTERVENTION"
    SOCIAL_REACTION = "SOCIAL_REACTION"
    LONG_FORM_AUTHORITY = "LONG_FORM_AUTHORITY"
    COMMERCIAL_TRUST_TRANSFER = "COMMERCIAL_TRUST_TRANSFER"


class DirectionalIntegritySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"


class DirectionalIntegrityResolutionPath(str, Enum):
    CONTINUE = "CONTINUE"
    REGENERATE = "REGENERATE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    HARD_BLOCK = "HARD_BLOCK"
    CIRCUIT_BREAK = "CIRCUIT_BREAK"


class DirectionalIntegrityFallbackReason(str, Enum):
    NONE = "NONE"
    MISSING_POLICY = "MISSING_POLICY"
    MISSING_ONTOLOGY = "MISSING_ONTOLOGY"
    MISSING_CROSSWALK = "MISSING_CROSSWALK"
    MISSING_HARD_NEGATIVE_SERVICE = "MISSING_HARD_NEGATIVE_SERVICE"
    NULL_RUNTIME_PACKET = "NULL_RUNTIME_PACKET"
    SDA_QUERY_DEGRADED = "SDA_QUERY_DEGRADED"
    INTERNAL_ANALYZER_ERROR = "INTERNAL_ANALYZER_ERROR"


class DirectionalIntegrityDomain(str, Enum):
    CCF = "CCF"
    CMF = "CMF"
    CBCS = "CBCS"
    REACTIONS = "REACTIONS"
    WEBINAR = "WEBINAR"
    COMMERCIAL = "COMMERCIAL"


class DirectionalIntegrityDimension(str, Enum):
    INVARIANT_PRESERVATION = "INVARIANT_PRESERVATION"
    REPRESENTATION_DRIFT = "REPRESENTATION_DRIFT"
    HARD_NEGATIVE_ADJACENCY = "HARD_NEGATIVE_ADJACENCY"
    TRAJECTORY_RISK = "TRAJECTORY_RISK"


class DirectionalIntegrityArtifactRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(..., min_length=3)
    artifact_kind: str = Field(..., min_length=3)
    artifact_path: Optional[str] = None
    artifact_hash: Optional[str] = None


class DirectionalIntegrityEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    source_kind: Literal[
        "invariant_field",
        "archetypal_geometry",
        "representation_geometry",
        "species_hypothesis",
        "candidate_text",
        "candidate_media",
        "crosswalk_resolution",
        "hard_negative",
        "policy_rule",
        "operator_note",
    ]
    summary: str
    cited_values: dict[str, Any] = Field(default_factory=dict)
    artifact_ref: Optional[DirectionalIntegrityArtifactRef] = None


class DirectionalIntegrityDimensionScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension: DirectionalIntegrityDimension
    score: float = Field(..., ge=0.0, le=1.0)
    severity: DirectionalIntegritySeverity
    threshold_warning: float = Field(..., ge=0.0, le=1.0)
    threshold_block: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)
    blocking: bool = False


class InvariantFieldPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    primary_invariant_ids: list[str] = Field(default_factory=list)
    secondary_invariant_ids: list[str] = Field(default_factory=list)
    invariant_activation_intensity: dict[str, float] = Field(default_factory=dict)
    invariant_resonance_multiplier_hint: Optional[dict[str, float]] = None
    source_evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)


class ArchetypalGeometryPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    geometry_id: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    required_preservations: list[str] = Field(default_factory=list)
    forbidden_drifts: list[str] = Field(default_factory=list)
    source_evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)


class RepresentationGeometryPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    representation_geometry_id: str
    authority_source: Optional[str] = None
    belonging_mode: Optional[str] = None
    identity_frame: Optional[str] = None
    coercion_risk_budget: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    source_evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)


class SpeciesHypothesisPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    species_label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    derivation_refs: list[str] = Field(default_factory=list)
    shadow_drifts: list[str] = Field(default_factory=list)


class HardNegativeCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hard_negative_id: str
    adjacency_score: float = Field(..., ge=0.0, le=1.0)
    divergence_axes: list[str] = Field(default_factory=list)
    failure_reason: str
    evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)


class HardNegativeEvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str
    top_matches: list[HardNegativeCandidate] = Field(default_factory=list)
    strongest_adjacency_score: float = Field(..., ge=0.0, le=1.0)
    blocked_by_hard_negative: bool = False
    fallback_reason: DirectionalIntegrityFallbackReason = (
        DirectionalIntegrityFallbackReason.NONE
    )


class DirectionalIntegrityPolicyRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    dimension: DirectionalIntegrityDimension
    warning_threshold: float = Field(..., ge=0.0, le=1.0)
    block_threshold: float = Field(..., ge=0.0, le=1.0)
    applies_to_surface: DirectionalIntegritySurfaceClass
    applies_to_domain: DirectionalIntegrityDomain
    description: str


class DirectionalIntegrityPolicyBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    domain: DirectionalIntegrityDomain
    surface_class: DirectionalIntegritySurfaceClass
    version: str
    fail_closed: bool = True
    rules: list[DirectionalIntegrityPolicyRule]
    review_if_dependency_degraded: bool = True
    block_if_dependency_degraded: bool = True
    notes: Optional[str] = None


class DirectionalIntegrityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    domain: DirectionalIntegrityDomain
    surface_class: DirectionalIntegritySurfaceClass
    actor_id: str
    coach_id: Optional[str] = None
    content_archetype: Optional[str] = None
    edge_product_label: Optional[str] = None
    candidate_text: Optional[str] = None
    candidate_media_refs: list[DirectionalIntegrityArtifactRef] = Field(default_factory=list)
    invariant_field: InvariantFieldPacket
    archetypal_geometry: ArchetypalGeometryPacket
    representation_geometry: RepresentationGeometryPacket
    species_hypothesis: Optional[SpeciesHypothesisPacket] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DirectionalIntegrityDecisionSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: DirectionalIntegrityDecision
    resolution_path: DirectionalIntegrityResolutionPath
    blocking: bool
    advisory_only: bool
    summary: str


class DirectionalIntegrityReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str
    request_id: str
    domain: DirectionalIntegrityDomain
    surface_class: DirectionalIntegritySurfaceClass
    policy_id: str
    evaluated_at_utc: datetime
    decision_summary: DirectionalIntegrityDecisionSummary
    invariant_preservation_score: DirectionalIntegrityDimensionScore
    representation_drift_score: DirectionalIntegrityDimensionScore
    hard_negative_adjacency_score: DirectionalIntegrityDimensionScore
    trajectory_risk_score: DirectionalIntegrityDimensionScore
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    invariant_resonance_multiplier: dict[str, float] = Field(default_factory=dict)
    symbolic_density: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    identity_proximity: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    hard_negative_report: Optional[HardNegativeEvaluationReport] = None
    fallback_reason: DirectionalIntegrityFallbackReason = (
        DirectionalIntegrityFallbackReason.NONE
    )
    dependency_warnings: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)
    lineage_refs: list[str] = Field(default_factory=list)


class DirectionalIntegrityEngineResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report: DirectionalIntegrityReport
    should_continue_automation: bool
    should_queue_operator_review: bool
    should_trigger_regeneration: bool
    should_trip_circuit_break: bool
```

### 5.1 Score Direction Semantics

To avoid ambiguity:

- `invariant_preservation_score`
  - higher is better
  - `1.0` = target invariant field is strongly preserved
- `representation_drift_score`
  - higher is worse
  - `1.0` = maximum harmful drift from intended representation geometry
- `hard_negative_adjacency_score`
  - higher is worse
  - `1.0` = extremely close to a known deceptive near-neighbor
- `trajectory_risk_score`
  - higher is worse
  - `1.0` = strong evidence the output is teaching a bad semantic trajectory even if it looks persuasive

This asymmetry is deliberate. The engine should not hide the fact that some dimensions measure preservation while others measure risk.

### 5.2 Default Threshold Profile

Recommended starting thresholds:

| Dimension | Warning | Block |
|-----------|---------|-------|
| `invariant_preservation_score` | `< 0.78` | `< 0.62` |
| `representation_drift_score` | `>= 0.28` | `>= 0.45` |
| `hard_negative_adjacency_score` | `>= 0.24` | `>= 0.40` |
| `trajectory_risk_score` | `>= 0.30` | `>= 0.48` |

These are global defaults only. Policy bundles may tighten them per surface.

---

## 6. Backward Compatibility Fallback

### 6.1 Dependency Degradation Policy

This engine must not silently pass high-risk surfaces when core SDA dependencies degrade.

| Failure Condition | Low-Risk Internal Planning | Public / Coaching / Commercial |
|------------------|----------------------------|--------------------------------|
| Missing policy bundle | `REVIEW` | `FAIL` |
| Missing ontology record | `FAIL` | `FAIL` |
| Missing crosswalk lineage | `REVIEW` if non-essential | `FAIL` |
| Hard-negative service unavailable | `REVIEW` | `FAIL` for `RENDER_RELEASE`, `LONG_FORM_AUTHORITY`, `COMMERCIAL_TRUST_TRANSFER` |
| Null or malformed runtime packet | `FAIL` | `FAIL` |
| Internal analyzer exception | `REVIEW` only if explicitly configured and not public | `FAIL` |

### 6.2 Failure-Closed Behavior

The failure-closed doctrine should follow existing patterns already present in:

- `semantic_affinity_guard.py`
- `conversion_sequence_router.py`
- `circuit_breaker.py`

Required behaviors:

- dependency failure is logged with a typed fallback reason
- high-risk automation halts rather than degrades into a silent pass
- the report still returns enough evidence for operator repair
- a circuit-break style halt is available for repeated or severe DI failures on the same flow

### 6.3 Circuit-Break Conditions

`DirectionalIntegrityEngine` may set `should_trip_circuit_break = True` when any of these happen:

- repeated `FAIL` on the same commercial proof surface within a configurable window
- repeated coercive-belonging or prestige-theater drift from the same workflow template
- missing hard-negative service plus high representation drift on a public status-bearing artifact
- downstream domain explicitly marks the combination as unacceptable

This is not the same as crisis detection. It is a semantic execution halt until explicit correction.

---

## 7. Tasks

### 7.1 Core Build Tasks

- [ ] Create `src/ccp/models/directional_integrity_models.py`
- [ ] Create `src/ccp/services/directional_integrity_engine.py`
- [ ] Create `src/ccp/services/directional_integrity_policy_registry.py`
- [ ] Create `src/ccp/services/hard_negative_adapter.py` as a temporary abstraction interface for `FR-ERA3-24`
- [ ] Add receipt stage constants and audit event names

### 7.2 Integration Tasks by Domain

- [ ] **CCF:** insert DI validation after archetype selection and before any JIT script contract / render blueprint handoff
- [ ] **CMF:** require DI pass or approved-review path before `export_composition(...)` and before share-asset packaging
- [ ] **CBCS:** require DI validation on high-stakes interpretive messaging, especially identity, authority, redemption, and relapse framing
- [ ] **Reactions:** validate public-facing score reveal copy, victory/share assets, redemption framing, and authority escalation
- [ ] **Webinar:** validate slide transition copy, recap payloads, and CTA transitions that move from insight to commercial pressure
- [ ] **Commercial:** validate referral cards, authority proof stacks, vanity-proof visuals, and conversion sequence payloads before release

### 7.3 Policy Authoring Tasks

- [ ] Author default domain bundles with the following exact mandatory thresholds (Warning / Block):
  - `DI-POL-CCF-001` (Internal Planning): Inv: <0.70/<0.60 | Rep: >=0.30/>=0.45 | HN: >=0.25/>=0.40 | Traj: >=0.30/>=0.45
  - `DI-POL-CMF-001` (Render Release): Inv: <0.75/<0.65 | Rep: >=0.25/>=0.40 | HN: >=0.22/>=0.38 | Traj: >=0.28/>=0.42
  - `DI-POL-CBCS-001` (Coaching): Inv: <0.80/<0.70 | Rep: >=0.20/>=0.35 | HN: >=0.20/>=0.35 | Traj: >=0.25/>=0.40
  - `DI-POL-REACTIONS-001` (Social): Inv: <0.78/<0.68 | Rep: >=0.25/>=0.40 | HN: >=0.24/>=0.40 | Traj: >=0.28/>=0.45
  - `DI-POL-WEBINAR-001` (Authority): Inv: <0.82/<0.72 | Rep: >=0.22/>=0.38 | HN: >=0.20/>=0.35 | Traj: >=0.25/>=0.40
  - `DI-POL-COMMERCIAL-001` (Commercial Trust): Inv: <0.85/<0.75 | Rep: >=0.15/>=0.30 | HN: >=0.15/>=0.30 | Traj: >=0.20/>=0.35
- [ ] Enforce the numeric overrides defined above for public status-bearing surfaces
- [ ] Define blocklists for known forbidden drifts:
  - prestige theater
  - coercive urgency
  - humiliation-as-motivation
  - synthetic belonging capture
  - mystical authority inflation

### 7.4 Audit Tasks

- [ ] Emit lineage refs back to SDA ontology/crosswalk artifacts
- [ ] Preserve per-dimension evidence in receipts
- [ ] Add “why blocked” repair guidance for operator queues
- [ ] Add report hash or version stamp to downstream artifacts when relevant

---

## 8. Acceptance Criteria

### AC1 - Typed Request/Report Contract

Given a valid SDA request with invariant, geometry, and representation packets,  
when `DirectionalIntegrityEngine.evaluate(...)` runs,  
then it returns a `DirectionalIntegrityReport` containing all four required dimensions, a typed decision summary, lineage refs, and fallback metadata.

### AC2 - Invariant Preservation Is Evaluated Separately From Drift

Given a candidate that retains emotional force but weakens the intended existential invariants,  
when the engine evaluates it,  
then `invariant_preservation_score` falls below warning or block thresholds even if the artifact still appears compelling.

### AC3 - Representation Drift Can Block Even With High Energy

Given a candidate that preserves activation energy but shifts toward prestige theater, coercive belonging, or manipulative authority,  
when the representation analyzer runs,  
then `representation_drift_score` is elevated and can independently trigger `REVIEW` or `FAIL`.

### AC4 - Hard-Negative Adjacency Is First-Class

Given a candidate artifact that is deceptively close to a known forbidden near-neighbor,  
when the hard-negative analyzer runs,  
then the engine emits a `HardNegativeEvaluationReport` and uses adjacency score in the final decision instead of treating hard negatives as an optional note.

### AC5 - High-Risk Surfaces Fail Closed

Given a `COMMERCIAL_TRUST_TRANSFER`, `RENDER_RELEASE`, or `LONG_FORM_AUTHORITY` request with missing policy or missing hard-negative dependency,  
when the engine cannot confidently validate direction,  
then the result is `FAIL` with explicit fallback reason and automation does not continue.

### AC6 - Review Path Is Supported for Ambiguous Cases

Given a medium-risk internal planning or render-regeneration scenario where thresholds land in the review band,  
when evaluation completes,  
then the engine emits `REVIEW` with required corrections and a deterministic resolution path (`REGENERATE` or `OPERATOR_REVIEW`).

### AC7 - Surface Policy Overrides Work

Given the same semantic candidate evaluated once for internal planning and once for commercial proof distribution,  
when policy bundles differ,  
then the commercial surface uses stricter thresholds and can block a case that would only review in planning.

### AC8 - Dependency and Packet Errors Never Silent-Pass

Given a null runtime packet, missing ontology, or broken crosswalk lineage,  
when evaluation starts,  
then the engine records the exact failure class and returns `FAIL` or `REVIEW` per policy instead of fabricating a pass.

### AC9 - Downstream Adapter Mapping Is Explicit

Given each supported downstream domain,  
when DI emits `PASS`, `REVIEW`, or `FAIL`,  
then the adapter behavior is deterministic:

- CCF: continue / iterate / block compile
- CMF: approve / regenerate-review / block export
- CBCS: deliver / queue human review / block intervention
- Reactions: continue local loop / withhold public escalation / block surface
- Webinar: continue slide flow / queue edit / block publish or CTA
- Commercial: continue / manual approval only / block send

### AC10 - Audit Trail Is Complete

Given any DI evaluation,  
when the receipt chain is inspected,  
then it contains:

- request identity
- resolved policy bundle
- dependency state
- four dimension outcomes
- final decision
- resolution path

---

## 9. Dependencies

### 9.1 Required Upstream Dependencies

| Dependency | Source | Why Required |
|------------|--------|--------------|
| `SDAOntologyRegistry` | FR-ERA3-20 | Canonical invariant, geometry, and species-composition truth |
| `SDAQueryAndCrosswalkService` | FR-ERA3-21 | Canonical lookup and maintained lineage resolution |
| `Directional Integrity Policy Bundle` | FR-ERA3-22 | Surface-specific thresholds and block/review rules |
| `HardNegativeAdapter` | FR-ERA3-24 | Near-neighbor deception evaluation |
| `InvariantFieldPacket` | PRD-02 / upstream runtime | Primary field input |
| `ArchetypalGeometryPacket` | PRD-02 / upstream runtime | Structural meaning input |
| `RepresentationGeometryPacket` | PRD-02 / upstream runtime | Encoding-direction input |
| `SpeciesHypothesisPacket` | PRD-02 / upstream runtime | Optional derived-form context |

### 9.2 Known Downstream Consumers

| Consumer | Current/Planned Spec | DI Role |
|----------|----------------------|---------|
| CCF | `FR-ERA3-16` update | Blocks or approves semantic compile progression |
| CMF | `FR-ERA3-12` update | Guards render/export/share direction |
| CBCS | `FR-ERA3-18` update | Guards identity-sensitive coaching interpretation |
| Reactions CORE | `FR-ERA3-05-CORE` update | Guards status/belonging/conflict framing |
| Webinar | future update | Guards educational authority and CTA transitions |
| Silent Referral / OFO / Commercial | `FR-ERA3-03`, `FR-ERA3-04`, `FR-ERA3-14` updates | Guards trust-transfer and prestige integrity |
| Conscious Editor | `FR-ERA3-09` update | Surfaces drift findings during review |

### 9.3 Future Couplings

This engine should later read:

- `RecursivePatternRegistry` / contextual dynamic outputs from `FR-ERA3-23`
- hard-negative mutation harness outputs from `FR-ERA3-24`
- optional inference-time compute policies if the platform later introduces evaluator-guided runtime branching

Those future couplings must enrich the engine, not change the current role boundary.

---

## 10. Testing Strategy

### 10.1 Integration Test Files

Create:

- `tests/integration/test_era3_fr22_directional_integrity_engine.py`
- `tests/integration/test_era3_fr22_directional_integrity_fallbacks.py`
- `tests/integration/test_era3_fr22_directional_integrity_domain_policies.py`

### 10.2 Required Test Classes

#### A. Contract Tests

- valid request returns typed report
- malformed request fails before silent evaluation
- per-dimension evidence arrays survive serialization

#### B. Dimension Tests

- invariant preservation drops when candidate flattens intended belonging / sacrifice / identity field
- representation drift rises when earned authority becomes prestige theater
- hard-negative adjacency rises when candidate is deceptively close to known manipulative template
- trajectory risk rises when artifact teaches coercive or dependency-forming next-step logic

#### C. Fallback Tests

- missing policy on commercial surface -> `FAIL`
- missing hard-negative adapter on CMF public release -> `FAIL`
- missing hard-negative adapter on low-risk planning -> `REVIEW`
- null runtime packet -> `FAIL`
- broken crosswalk lineage -> `FAIL` on public surface

#### D. Domain Policy Tests

- same artifact passes internal planning but fails commercial trust transfer
- same artifact reviews in reactions but fails public share escalation
- webinar CTA transition blocks when authority source drifts from earned to coercive

#### E. Audit Tests

- receipt chain contains dependency state and policy id
- report retains lineage refs to ontology / crosswalk artifacts
- `required_corrections` populated on `REVIEW` and `FAIL`

### 10.3 Seed Test Scenarios

At minimum include these fixtures:

1. **Healthy authority proof**
   - intended: earned authority + invitational belonging
   - expected: `PASS`

2. **Prestige theater share card**
   - intended: reflective social proof
   - actual drift: vanity-proof domination framing
   - expected: `FAIL` for commercial/social public surfaces

3. **Fast but fake reward loop**
   - intended: `EXP-FBK-001` + `EXP-TRG-002`
   - actual drift: instant but meaningless vanity feedback
   - expected: low invariant preservation or high trajectory risk

4. **Replay ladder with coercive upgrade**
   - intended: `EXP-PRG-002`
   - actual drift: progression framed as shame and status exclusion
   - expected: `REVIEW` or `FAIL` depending on surface

5. **Healthy status share**
   - intended: `EXP-TRS-003`
   - actual output preserves user authority without platform ego capture
   - expected: `PASS`

### 10.4 Manual Validation Checklist

- verify the engine never reports `PASS` with unresolved missing ontology
- verify all public or commercial surfaces fail closed when hard-negative support is unavailable
- verify a `REVIEW` result always includes actionable correction text
- verify downstream adapters do not reinterpret `FAIL` as advisory
- verify the taxonomy distinction remains intact:
  - policy resolved from policy bundle
  - packet emitted by engine
  - hard negatives consumed as adversarial assets, not inlined prose rules

---

**End of Spec**
