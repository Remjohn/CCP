# Tech-Spec: FR-ERA3-26 - Subliminal Function Query and Profile Service
**Created:** 2026-05-19  
**Status:** Ready for Development  
**Version:** 1.0 (ERA3 Architecture - SFL Foundation)  
**Phase:** 6 - Subliminal Function Layer Foundation  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED: ERA3_Tech_Spec_Writing_Protocol.md. Confirmed the mandatory 10-section spec structure, existing-backend integration requirement, typed Pydantic schema requirement, and test-pattern reuse expectation.
2. PRD LOADED: PRD-02. Verified the exact runtime-law line now states: `truth -> transcription -> force -> delivery -> variation -> phenotype -> evaluation` and that the delivery layer explicitly contains `runtime DSPy modules, SFL function stack, composition depth profiles, archetype container logic`.
3. PRD LOADED: PRD-02. Verified the compiler sequence still preserves upstream semantic order: `signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> directional integrity validation -> JIT script contract -> render blueprint`.
4. PRD LOADED: PRD-08. Verified the sibling-boundary lines: `primitives are not the deepest ontology`, `SDA artifacts are not new primitive families`, and the runtime stack remains `context substrate -> SDA field -> primitive candidate field -> coalition -> archetype container -> SDA validation -> destination packet`.
5. PRD LOADED: PRD-08. Verified the biological placement line: `primitives apply force over the currently active field` while `SFL and downstream composition logic determine how that force is felt`.
6. SFL CORE DOC LOADED: lab/subliminal_function_layer_for_ccp_v_1.md. Verified the central law: `SDA protects semantic truthfulness` and `SFL shapes perceptual potency and symbolic aliveness`.
7. SFL CORE DOC LOADED: lab/subliminal_function_layer_for_ccp_v_1.md. Verified the refined runtime sequence includes `representation geometry binding -> subliminal function stack -> content archetype container -> directional integrity validation -> perceptual influence validation`.
8. SFL FUNCTION DOC LOADED: lab/Subliminal Functions for Agentic Content Architecture.md. Verified every association is framed as `a semantic operator`, `a perception modulation function`, `a meaning-shaping primitive`, and `a symbolic field mechanism`, which means query assembly must resolve functions deliberately rather than treating the 120 terms as flat rows.
9. ASSOCIATION CHAT LOADED: lab/120 subliminal associations Chat.md. Verified the key tension language: systems need both `semantic truthfulness` and `adaptive vitality`, and that alive systems should not become over-closed.
10. SDA CORE DOC LOADED: semantic_discernment_architecture_content_engine_v_1.md. Verified SDA still owns `existential invariants`, `representation geometry`, `directional integrity`, and protection against `deceptively close failure`.
11. SDA TAXONOMY DOC LOADED: semantic_discernment_architecture_artifact_taxonomy_v_1.md. Verified `Schemas must therefore be derived from role`, and the taxonomy keeps canonical objects, runtime packets, validation policies, adversarial assets, and crosswalks separate.
12. PRIMITIVE ARCHITECTURE DOC LOADED: Perceptual_Primitives_Architecture.md. Verified `primitives are not edges`, that primitives remain `transformation operators` and `candidate generators`, and that coalitions must route into the official CCF lattice rather than generic labels.
13. FR-ERA3-25 LOADED: FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md. Verified the canonical SFL substrate already defines the maintained artifact classes needed by this service:
    - `SubliminalFunctionFamilyRecord`
    - `SubliminalFunctionDefinitionRecord`
    - `FunctionFamilyCompressionRuleRecord`
    - `PrimitiveToFunctionFamilyCrosswalkRecord`
    - `RepresentationGeometryToFunctionProfileRecord`
    - `ArchetypeToFunctionProfileRecord`
    - `SurfaceConstraintProfileRecord`
14. PRIMITIVE YAMLs VERIFIED:
    - `PRM-BUS-001` = `Perception and Guidance Stack`
    - `PRM-BUS-002` = `Emotional Journey / Peak-End`
    - `EXP-FBK-001` = `RIM Feedback Discipline`
    - `EXP-FBK-002` = `Reflective Scoring`
    Verified current repository ID formats, aliases, fit floats, crosswalk IDs, conflict/synergy style, and the fact that these records already carry deterministic metadata this service can read but not duplicate.
15. BACKEND FILES READ:
    - `src/ccp/services/primitive_registry_service.py` -> `def query_by_id(self, primitive_id: str, plane: PrimitivePlane | None = None) -> PrimitiveRecord | None:`
    - `src/ccp/services/primitive_registry_service.py` -> `def query_batch(self, request: PrimitiveQueryRequest) -> PrimitiveQueryResponse:`
    - `src/ccp/services/sda_registry_service.py` -> `def get_invariant(self, artifact_id: str) -> ExistentialInvariantRecord | None:`
    - `src/ccp/services/sda_registry_service.py` -> `def get_crosswalk_bundle(self, name: str) -> dict[str, SDARegistryRecord]:`
    - `src/ccp/services/sda_registry_service.py` -> `def reload_artifact(self, path: str | Path) -> SDAArtifactReloadResult:`
16. TESTS READ:
    - `tests/integration/test_era3_fr20_sda_registry.py` confirmed startup warm receipts, false-registry rejection, scalar-layer rejection, targeted reload, and previous-good-state rollback.
    - `tests/integration/test_era3_fr06_primitive_registry.py` confirmed hot-path cache hits avoid additional YAML reads, family/plane queries preserve boundaries, and targeted invalidation reloads only the affected YAML.
17. PHASE-6 TRACEABILITY CHECK: There is still no dedicated Phase 6 epic file. This spec therefore uses the SFL doctrine source set plus the explicit CBAR mandates named in the spec prompt: Anti-Centroid Law preservation, Deterministic profile assembly, No-Function-Hallucination Rule, Primitive/SDA/SFL boundary rule, and Failure-closed profile resolution.
18. CROSSWALK EXPECTATION CONFIRMED: FR-ERA3-26 must consume maintained crosswalk evidence from FR-ERA3-25 and may not invent primitive-family links, geometry-profile links, archetype defaults, or surface constraints at runtime.
```

---

## 1. Files Read

| # | File | Date/Version | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S50_FR-ERA3-26_Subliminal_Function_Query_And_Profile_Service.md` | 2026-05-18 | Prompt source, scope boundary, mandatory outputs |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Current | Mandatory spec protocol and 10-section structure |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Version 6.0 | Runtime law, compiler boundary, delivery-layer placement |
| 4 | `docs/prd/modules/PRD_08_Conscious_Primitives.md` | Version 6.0 | Primitive/SDA/SFL boundary, force-layer placement |
| 5 | `lab/subliminal_function_layer_for_ccp_v_1.md` | 2026-05-18 | Canonical SFL doctrine and runtime placement |
| 6 | `lab/Subliminal Functions for Agentic Content Architecture.md` | Current lab source | Function framing for the 120 associations |
| 7 | `lab/120 subliminal associations Chat.md` | Current lab source | Adaptive-vitality and alive-system framing |
| 8 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Current lab source | SDA truth ownership, geometry, directional integrity |
| 9 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Current lab source | Role-before-schema law and artifact-class split |
| 10 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Current lab source | Primitive candidate, coalition, and edge-product ordering |
| 11 | `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | 2026-05-19 | Upstream SFL canonical substrate this spec consumes |
| 12 | `primitives/meaning/design_business/PRM-BUS-001.yaml` | Current repo artifact | Verified meaning primitive ID and crosswalk style |
| 13 | `primitives/meaning/design_business/PRM-BUS-002.yaml` | Current repo artifact | Verified memorability/peak-end primitive structure |
| 14 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Current repo artifact | Verified experience primitive structure and timing logic |
| 15 | `primitives/experience/feedback_scoring/EXP-FBK-002.yaml` | Current repo artifact | Verified reflective-scoring primitive structure |
| 16 | `src/ccp/services/primitive_registry_service.py` | Current code | Query-service pattern, warm cache, targeted invalidation |
| 17 | `src/ccp/services/sda_registry_service.py` | Current code | Manifest loading, path validation, reload rollback pattern |
| 18 | `tests/integration/test_era3_fr20_sda_registry.py` | Current tests | False-registry rejection and targeted reload pattern |
| 19 | `tests/integration/test_era3_fr06_primitive_registry.py` | Current tests | Query/cache determinism and invalidation pattern |

---

## 2. Overview

### 2.1 Problem Statement

`FR-ERA3-25` defines the canonical SFL substrate, but the platform still lacks a bounded runtime service that can:

- retrieve canonical function families
- retrieve canonical function definitions
- resolve maintained primitive-to-family links
- resolve maintained representation-geometry profile links
- resolve maintained archetype defaults
- resolve maintained delivery-surface constraint profiles
- assemble a deterministic `SubliminalFunctionStackPacket`

without:

- inventing new functions
- collapsing evaluator logic into lookup logic
- duplicating primitive ownership
- duplicating SDA ontology ownership
- letting profile assembly drift into prompt-time improvisation

Without `FR-ERA3-26`, downstream systems will either:

- hard-code function choices in multiple places
- guess perceptual profiles heuristically from prose
- mix SFL selection into rendering logic
- let evaluators quietly become selectors
- or bypass SFL entirely and flatten the delivery layer into generic tone instructions

That would violate the reason SFL exists: preserving perceptual force, symbolic aliveness, and bounded persuasion without compromising the deeper semantic stack.

### 2.2 Solution

This spec defines a dedicated internal query and profile-assembly service:

`SubliminalFunctionQueryService`

The service is a deterministic runtime substrate that:

- consumes canonical SFL artifacts from `FR-ERA3-25`
- queries the primitive registry for validated primitive evidence
- queries SDA for validated representation-geometry evidence
- resolves profile inputs through maintained crosswalks
- assembles a typed `SubliminalFunctionStackPacket`
- emits machine-readable assembly receipts, warnings, and fallback states
- fails closed when evidence is insufficient or contradictory

It is intentionally narrow.

It is:

- a lookup service
- a profile-resolution service
- a packet-assembly service

It is not:

- a content generator
- a scoring engine
- a semantic evaluator
- a substitute for FR-ERA3-27
- a substitute for FR-ERA3-28

### 2.3 Scope

**In scope:**

- typed query request and query response contracts
- canonical lookup by:
  - family
  - function id
  - primitive crosswalk
  - representation geometry crosswalk
  - archetype / container profile
  - delivery surface constraint profile
- deterministic profile assembly from maintained evidence only
- deterministic `SubliminalFunctionStackPacket` generation
- cache warm, local mirror, version stamp, and targeted reload expectations
- failure-closed fallback rules for:
  - partial crosswalk evidence
  - profile conflict
  - family-only fallback
- receipt logging and operator-visible assembly status

**Out of scope:**

- perceptual effect scoring
- false-depth / over-optimization evaluation
- crosswalk authoring or canonical artifact creation
- ontology mutation
- primitive candidate generation
- final render decisions
- UI consumption or editor workflows

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-SFL-026-01 | `SubliminalFunctionQueryService` | FR-ERA3-26 | Internal runtime lookup and deterministic profile assembly service |
| DEP-SFL-026-02 | `SubliminalFunctionQueryRequest` | FR-ERA3-26 | Typed request envelope for canonical lookup surfaces |
| DEP-SFL-026-03 | `SubliminalFunctionQueryResponse` | FR-ERA3-26 | Typed response envelope for resolved records and evidence trace |
| DEP-SFL-026-04 | `SubliminalFunctionProfileResolver` | FR-ERA3-26 | Applies precedence rules across primitive, geometry, archetype, and surface evidence |
| DEP-SFL-026-05 | `FunctionProfileAssemblyRequest` | FR-ERA3-26 | Typed input for runtime profile assembly |
| DEP-SFL-026-06 | `FunctionProfileAssemblyResult` | FR-ERA3-26 | Carries stack packet, resolution status, warnings, and receipts |
| DEP-SFL-026-07 | `SubliminalFunctionStackPacket` | FR-ERA3-26 | Machine-readable runtime packet for downstream consumption |
| DEP-SFL-026-08 | `FunctionProfileEvidenceRecord` | FR-ERA3-26 | Tracks exactly which maintained artifact or query result influenced the stack |
| DEP-SFL-026-09 | `SFLQueryCacheManager` | FR-ERA3-26 | Warm cache, hot-path mirror, versioning, and targeted reload support |
| DEP-SFL-026-10 | `ProfileConflictReport` | FR-ERA3-26 | Explains evidence collisions without invoking evaluator logic |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | Upstream canonical SFL substrate; all families, functions, compression rules, and crosswalks are consumed from here |
| `primitive_registry_service.py` | `src/ccp/services/primitive_registry_service.py` | Provides validated primitive lookup and batch query patterns; this service reads primitive evidence but never owns primitive state |
| `sda_registry_service.py` | `src/ccp/services/sda_registry_service.py` | Provides maintained representation geometry and crosswalk bundles plus targeted reload pattern |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Required for warm, lookup, assembly, conflict, and fallback receipts |
| `visual_format_constraint_adapter.py` | `src/ccp/services/visual_format_constraint_adapter.py` | Pattern reference for surface-constraint lookup and deterministic adapter behavior |
| `known_persons_registry_adapter.py` | `src/ccp/services/known_persons_registry_adapter.py` | Pattern reference for guardrail-first bounded registry clients |
| `tests/integration/test_era3_fr06_primitive_registry.py` | `tests/integration/test_era3_fr06_primitive_registry.py` | Hot-path cache, boundary-preserving query, and targeted invalidation pattern |
| `tests/integration/test_era3_fr20_sda_registry.py` | `tests/integration/test_era3_fr20_sda_registry.py` | Targeted reload rollback and failure-closed registry pattern |

This service should be implemented as new code, not as an overload of:

- `primitive_registry_service.py`
- `sda_registry_service.py`
- `content_machine.py`
- or any renderer

Recommended new code paths:

- `src/ccp/models/sfl_query_models.py`
- `src/ccp/services/sfl_query_service.py`
- `tests/integration/test_era3_fr26_sfl_query_service.py`
- `tests/integration/test_era3_fr26_sfl_profile_resolution.py`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied In This Spec |
|---|---|---|---|
| `PRM-BUS-001` | `Perception and Guidance Stack` | `design_business` | Confirms meaning-plane primitives can legitimately crosswalk into SFL families for attention guidance and routing pressure, but the service must read crosswalks rather than infer them from prose |
| `PRM-BUS-002` | `Emotional Journey / Peak-End` | `design_business` | Confirms memorability and end-state pressure may inform function-family resolution, especially trust/proof and repetition/imprint families |
| `EXP-FBK-001` | `RIM Feedback Discipline` | `feedback_scoring` | Confirms some experience-plane primitives can supply delivery-surface pressure and timing pressure without allowing SFL to absorb feedback-engine ownership |
| `EXP-FBK-002` | `Reflective Scoring` | `feedback_scoring` | Confirms high-trust vocabulary and premium-score framing may influence profile resolution, but final scoring still belongs to evaluator layers |

Primitive constraints for this service:

- every primitive reference must resolve through real repository IDs
- primitive evidence may shape SFL profile assembly only through maintained crosswalks
- primitive conflict logic remains primitive-registry responsibility
- this service never invents primitive-to-function mappings

### 3.4 SFL Governance Constraints

| Constraint | Origin | Enforcement Mechanism In This Spec |
|---|---|---|
| Anti-Centroid Law preservation | Prompt CBAR mandate + PRD-02 / PRD-08 | The assembly engine may cap active functions, prefer sparse stacks, and reject profile merges that create indiscriminate all-family activation |
| Deterministic profile assembly | Prompt CBAR mandate | The resolver must apply a fixed precedence order and emit the same packet for the same canonical inputs |
| No-Function-Hallucination Rule | Prompt CBAR mandate | Only `FR-ERA3-25` canonical function IDs and family IDs may appear in packets; raw text cannot produce net-new functions |
| Primitive/SDA/SFL boundary rule | Prompt CBAR mandate + PRD-08 | Primitive ownership stays in FR-ERA3-06, ontology ownership stays in FR-ERA3-20, and this service owns only lookup/profile assembly |
| Failure-closed profile resolution | Prompt CBAR mandate + PRD-08 fail-closed law | Conflicting or insufficient evidence must degrade to `review_required`, `family_only`, or `unresolved`; the service cannot silently invent a clean stack |
| Role-before-schema rule | SDA taxonomy | Separate models for canonical query responses, profile assembly inputs, runtime packets, and conflict reports |
| Surface-specific constraint discipline | FR-ERA3-25 doctrine | Delivery-surface rules are read from maintained surface profiles, not handwritten inside each caller |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Build a dedicated query/profile service rather than extending the registry loader | Keeps canonical ownership and runtime assembly separate | Put assembly inside `sfl_registry_service.py` | Would blur canonical artifact management with runtime selection |
| Use maintained crosswalk evidence only | Keeps packet assembly auditable and reproducible | Infer functions heuristically from primitive summaries or geometry names | Violates the No-Function-Hallucination Rule |
| Separate `lookup` requests from `assembly` requests | Clarifies query-only surfaces versus packet-building surfaces | One giant multi-purpose endpoint object | Too opaque and harder to validate |
| Precedence order is explicit and versioned | Prevents silent drift across releases | Caller-defined precedence | Would make outputs inconsistent across pipelines |
| Family-only fallback is allowed but must be marked degraded | Gives bounded utility when exact function evidence is missing | Fail everything without any fallback | Too rigid for early SFL rollout |
| Profile conflicts generate machine-readable reports, not probabilistic smoothing | Keeps evaluators and humans able to inspect real collisions | Average all preferred functions together | Creates centroid stacks and hides contradictions |
| Cache the canonical SFL mirror locally with targeted reload hooks | Matches existing registry/query patterns and supports fast runtime access | Read YAML on every profile assembly | Too slow and undermines determinism under load |

### 3.6 Deterministic Assembly Precedence

The service must resolve runtime function stacks in this exact order:

1. **Explicit function ID overrides**
2. **Delivery surface constraint profile**
3. **Archetype / container profile**
4. **Representation geometry profile**
5. **Primitive crosswalk family evidence**
6. **Family-level default function definitions**

Important interpretation:

- higher-priority layers may constrain or remove lower-priority candidates
- lower-priority layers may enrich a stack only if they do not violate an already-resolved higher-priority constraint
- precedence is not simple append order; it is constrained merge order

### 3.7 Boundary Law

This service may:

- read primitive IDs
- read representation geometry IDs
- read archetype names
- read surface keys
- resolve function families
- resolve canonical function IDs
- assemble a `SubliminalFunctionStackPacket`

This service may not:

- compute perceptual scores
- decide whether output quality is good enough
- decide whether persuasion is ethically acceptable in the final artifact
- mutate Voice DNA
- mutate primitives
- mutate SDA ontology
- generate rendered language or media

---

## 4. Implementation Plan

### Phase 1 - Typed Query and Assembly Models

- [ ] Create `src/ccp/models/sfl_query_models.py`
- [ ] Define enums for:
  - query mode
  - profile evidence kind
  - function selection source
  - assembly status
  - surface kind bridge
- [ ] Define request models for:
  - function lookup
  - family lookup
  - primitive crosswalk lookup
  - geometry profile lookup
  - archetype profile lookup
  - surface profile lookup
  - runtime profile assembly
- [ ] Define response models for:
  - query result
  - function profile
  - conflict report
  - runtime stack packet
  - assembly result

### Phase 2 - Service Skeleton and Canonical Dependency Wiring

- [ ] Create `src/ccp/services/sfl_query_service.py`
- [ ] Accept injected dependencies for:
  - `SFLRegistryService`
  - `PrimitiveRegistryQueryService`
  - `SDARegistryService`
  - `ReceiptChain`
- [ ] Add startup warm entrypoint:
  - `warm_query_cache()`
- [ ] Add health method:
  - `health()`

### Phase 3 - Query Surfaces

- [ ] Implement `query_family(family_id)`
- [ ] Implement `query_function(function_id)`
- [ ] Implement `query_by_primitive(primitive_id)`
- [ ] Implement `query_by_representation_geometry(geometry_id)`
- [ ] Implement `query_by_archetype(archetype_name)`
- [ ] Implement `query_by_surface(surface_key)`
- [ ] Implement generic dispatcher:
  - `query(request: SubliminalFunctionQueryRequest) -> SubliminalFunctionQueryResponse`

### Phase 4 - Deterministic Profile Assembly

- [ ] Implement `assemble_profile(request: FunctionProfileAssemblyRequest) -> FunctionProfileAssemblyResult`
- [ ] Resolve explicit overrides first
- [ ] Apply surface constraints
- [ ] Apply archetype defaults
- [ ] Apply representation-geometry profile
- [ ] Apply primitive family evidence
- [ ] Resolve family-level fallback where needed
- [ ] Emit:
  - `resolved_function_ids`
  - `suppressed_function_ids`
  - `evidence_trace`
  - `warnings`
  - `conflicts`
  - `assembly_status`

### Phase 5 - Cache, Versioning, and Reload Behavior

- [ ] Mirror canonical SFL records into an in-process cache
- [ ] Store resolved indexes for:
  - family -> function IDs
  - primitive ID -> family IDs
  - geometry ID -> preferred function IDs
  - archetype -> preferred function IDs
  - surface -> preferred/discouraged family IDs
- [ ] Add service version stamp sourced from:
  - SFL manifest hash
  - registry report hash if available
- [ ] Implement targeted invalidation when FR-ERA3-25 artifacts reload
- [ ] Preserve previous-good query indexes on failed rebuild

### Phase 6 - Receipts and Runtime Traceability

- [ ] Log startup warm receipt
- [ ] Log query hit/miss receipts
- [ ] Log profile assembly receipts
- [ ] Log degraded fallback receipts
- [ ] Log conflict receipts
- [ ] Log query-cache rebuild receipts

### Phase 7 - Tests

- [ ] Create `tests/integration/test_era3_fr26_sfl_query_service.py`
- [ ] Create `tests/integration/test_era3_fr26_sfl_profile_resolution.py`
- [ ] Add unit tests for schema validation and precedence ordering
- [ ] Add fixture SFL artifacts mirroring FR-ERA3-25 canonical shapes

---

## 5. Primary Output Schema

```python
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SFLQueryMode(str, Enum):
    BY_FAMILY = "by_family"
    BY_FUNCTION_ID = "by_function_id"
    BY_PRIMITIVE_CROSSWALK = "by_primitive_crosswalk"
    BY_REPRESENTATION_GEOMETRY = "by_representation_geometry"
    BY_ARCHETYPE_PROFILE = "by_archetype_profile"
    BY_SURFACE_PROFILE = "by_surface_profile"


class SFLAssemblyStatus(str, Enum):
    RESOLVED = "resolved"
    FAMILY_ONLY = "family_only"
    PARTIAL = "partial"
    REVIEW_REQUIRED = "review_required"
    UNRESOLVED = "unresolved"


class ProfileEvidenceKind(str, Enum):
    EXPLICIT_FUNCTION = "explicit_function"
    SURFACE_CONSTRAINT_PROFILE = "surface_constraint_profile"
    ARCHETYPE_PROFILE = "archetype_profile"
    REPRESENTATION_GEOMETRY_PROFILE = "representation_geometry_profile"
    PRIMITIVE_CROSSWALK = "primitive_crosswalk"
    FAMILY_DEFAULT = "family_default"


class FunctionSelectionSource(str, Enum):
    EXPLICIT_OVERRIDE = "explicit_override"
    REQUIRED_BY_SURFACE = "required_by_surface"
    PREFERRED_BY_SURFACE = "preferred_by_surface"
    PREFERRED_BY_ARCHETYPE = "preferred_by_archetype"
    REQUIRED_BY_ARCHETYPE = "required_by_archetype"
    PREFERRED_BY_GEOMETRY = "preferred_by_geometry"
    HINTED_BY_PRIMITIVE = "hinted_by_primitive"
    FALLBACK_FROM_FAMILY = "fallback_from_family"


class SFLQueryWarningCode(str, Enum):
    FAMILY_ONLY_FALLBACK = "family_only_fallback"
    PARTIAL_CROSSWALK_EVIDENCE = "partial_crosswalk_evidence"
    CONFLICT_REQUIRES_REVIEW = "conflict_requires_review"
    UNKNOWN_PRIMITIVE_REFERENCE = "unknown_primitive_reference"
    UNKNOWN_GEOMETRY_REFERENCE = "unknown_geometry_reference"
    SURFACE_CONSTRAINT_REMOVED_FUNCTION = "surface_constraint_removed_function"
    EXPLICIT_OVERRIDE_DISCOURAGED = "explicit_override_discouraged"


class DeliverySurfaceKind(str, Enum):
    TELEGRAM = "telegram"
    CAROUSEL = "carousel"
    SHORT_FORM_VIDEO = "short_form_video"
    LONG_FORM_VIDEO = "long_form_video"
    WEBINAR = "webinar"
    COMMERCIAL = "commercial"
    AUDIT = "audit"


class SFLVersionStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: str = Field(min_length=1)
    manifest_hash: str = Field(min_length=8)
    registry_hash: str | None = None


class SFLQueryWarning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: SFLQueryWarningCode
    message: str = Field(min_length=3)
    evidence_ref: str | None = None


class FunctionProfileEvidenceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_kind: ProfileEvidenceKind
    source_artifact_id: str = Field(min_length=3)
    source_label: str = Field(min_length=3)
    affected_family_ids: list[str] = Field(default_factory=list)
    affected_function_ids: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=3)
    precedence_rank: int = Field(ge=1, le=6)


class ResolvedFunctionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    function_id: str = Field(pattern=r"^SFL-FN-\d{3}$")
    canonical_name: str = Field(min_length=3)
    family_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    selection_source: FunctionSelectionSource
    rationale: str = Field(min_length=3)


class ResolvedFamilyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    family_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    canonical_name: str = Field(min_length=3)
    rationale: str = Field(min_length=3)


class ProfileConflictRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conflict_id: str = Field(min_length=3)
    higher_priority_evidence_ref: str = Field(min_length=3)
    lower_priority_evidence_ref: str = Field(min_length=3)
    conflict_scope: Literal["family", "function", "surface_rule", "archetype_rule", "geometry_rule"]
    affected_function_ids: list[str] = Field(default_factory=list)
    resolution: Literal["suppressed_lower_priority", "downgraded_to_family_only", "review_required"]
    rationale: str = Field(min_length=3)


class SubliminalFunctionProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str = Field(min_length=3)
    status: SFLAssemblyStatus
    resolved_families: list[ResolvedFamilyRecord] = Field(default_factory=list)
    resolved_functions: list[ResolvedFunctionRecord] = Field(default_factory=list)
    suppressed_function_ids: list[str] = Field(default_factory=list)
    evidence_trace: list[FunctionProfileEvidenceRecord] = Field(default_factory=list)
    conflicts: list[ProfileConflictRecord] = Field(default_factory=list)
    warnings: list[SFLQueryWarning] = Field(default_factory=list)


class SubliminalFunctionStackPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str = Field(min_length=3)
    coach_id: str | None = None
    content_archetype: str | None = None
    representation_geometry_id: str | None = Field(default=None, pattern=r"^SDA-RPG-\d{3}$")
    delivery_surface: DeliverySurfaceKind
    status: SFLAssemblyStatus
    active_family_ids: list[str] = Field(default_factory=list)
    active_function_ids: list[str] = Field(default_factory=list)
    suppressed_function_ids: list[str] = Field(default_factory=list)
    evidence_trace: list[FunctionProfileEvidenceRecord] = Field(default_factory=list)
    version_stamp: SFLVersionStamp
    lineage: dict[str, str] = Field(default_factory=dict)
    warnings: list[SFLQueryWarning] = Field(default_factory=list)


class SubliminalFunctionQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_mode: SFLQueryMode
    family_id: str | None = Field(default=None, pattern=r"^SFL-FAM-\d{3}$")
    function_id: str | None = Field(default=None, pattern=r"^SFL-FN-\d{3}$")
    primitive_id: str | None = Field(default=None, pattern=r"^(EXP|PRM)-[A-Z]{3}-\d{3}$")
    representation_geometry_id: str | None = Field(default=None, pattern=r"^SDA-RPG-\d{3}$")
    archetype_name: str | None = None
    delivery_surface: DeliverySurfaceKind | None = None
    include_functions: bool = True
    include_crosswalk_evidence: bool = True

    @model_validator(mode="after")
    def validate_target(self) -> "SubliminalFunctionQueryRequest":
        required_by_mode = {
            SFLQueryMode.BY_FAMILY: self.family_id,
            SFLQueryMode.BY_FUNCTION_ID: self.function_id,
            SFLQueryMode.BY_PRIMITIVE_CROSSWALK: self.primitive_id,
            SFLQueryMode.BY_REPRESENTATION_GEOMETRY: self.representation_geometry_id,
            SFLQueryMode.BY_ARCHETYPE_PROFILE: self.archetype_name,
            SFLQueryMode.BY_SURFACE_PROFILE: self.delivery_surface,
        }
        if not required_by_mode[self.query_mode]:
            raise ValueError(f"Missing required target for query_mode={self.query_mode.value}")
        return self


class SubliminalFunctionQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_id: str = Field(min_length=3)
    query_mode: SFLQueryMode
    ready: bool
    resolved_families: list[ResolvedFamilyRecord] = Field(default_factory=list)
    resolved_functions: list[ResolvedFunctionRecord] = Field(default_factory=list)
    evidence_trace: list[FunctionProfileEvidenceRecord] = Field(default_factory=list)
    warnings: list[SFLQueryWarning] = Field(default_factory=list)
    version_stamp: SFLVersionStamp
    cache_hit: bool
    latency_ms: float = Field(ge=0.0)


class FunctionProfileAssemblyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    coach_id: str | None = None
    content_archetype: str | None = None
    delivery_surface: DeliverySurfaceKind
    representation_geometry_id: str | None = Field(default=None, pattern=r"^SDA-RPG-\d{3}$")
    primitive_ids: list[str] = Field(default_factory=list)
    explicit_function_ids: list[str] = Field(default_factory=list)
    explicit_family_ids: list[str] = Field(default_factory=list)
    allow_family_only_fallback: bool = True
    require_complete_crosswalks: bool = False


class FunctionProfileAssemblyResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(min_length=3)
    status: SFLAssemblyStatus
    profile: SubliminalFunctionProfile
    stack_packet: SubliminalFunctionStackPacket | None = None
    warnings: list[SFLQueryWarning] = Field(default_factory=list)
    conflicts: list[ProfileConflictRecord] = Field(default_factory=list)
    version_stamp: SFLVersionStamp
    cache_hit: bool
    latency_ms: float = Field(ge=0.0)
```

### Schema Notes

- `SubliminalFunctionQueryRequest` is for query surfaces only.
- `FunctionProfileAssemblyRequest` is for runtime stack construction.
- `SubliminalFunctionProfile` is an intermediate resolved profile object.
- `SubliminalFunctionStackPacket` is the runtime artifact that downstream systems consume.
- No evaluator fields are allowed here:
  - no `cognitive_imprint_score`
  - no `symbolic_density_score`
  - no `human_congruence_score`
  - no pass/fail quality verdicts
- The packet preserves:
  - lineage
  - evidence trace
  - warnings
  - version stamp

### Assembly Rules Bound To Schema

The service must enforce the following:

1. `explicit_function_ids` may only reference canonical `SFL-FN-*` IDs.
2. `explicit_family_ids` may only reference canonical `SFL-FAM-*` IDs.
3. `primitive_ids` may only influence family/function selection through maintained crosswalks.
4. `representation_geometry_id` may only influence profile selection through maintained geometry profiles.
5. `content_archetype` may only influence profile selection through maintained archetype profiles.
6. `delivery_surface` is mandatory for packet assembly and may suppress lower-priority selections.

---

## 6. Backward Compatibility Fallback

If the SFL query service is unavailable or not ready:

1. downstream systems must not guess perceptual stacks from prose
2. downstream systems may degrade to:
   - primitive + SDA runtime only
   - explicit `SFL_QUERY_UNAVAILABLE` advisory state
   - no `SubliminalFunctionStackPacket`
3. if a caller explicitly requires SFL for its route, the request must fail closed into:
   - `review_required`
   - or `unresolved`

Allowed degraded behavior:

- surface caller receives a machine-readable warning
- caller continues without SFL packet if the route is marked optional
- family-only fallback is allowed only when canonical family evidence exists

Rejected degraded behavior:

- inventing function IDs from raw text
- inferring geometry preferences from naming similarity alone
- converting evaluator complaints into runtime selection logic
- blending conflicting profiles into one averaged stack without trace

### Fallback Matrix

| Condition | Allowed Outcome | Rejected Outcome |
|---|---|---|
| Primitive crosswalk missing but family default exists | `family_only` profile with warning | Fabricated canonical function ID |
| Geometry profile missing but archetype and surface exist | `partial` profile using remaining evidence | Guessing geometry-linked functions from archetype prose |
| Surface profile conflicts with explicit override | `review_required` or lower-priority suppression with receipt | Silent override of hard surface constraint |
| Registry warm failed | `unresolved` plus machine-readable reason | Soft success with incomplete mirror |
| Targeted reload failed | preserve previous-good state | mixed-state live registry |

---

## 7. Tasks

- [ ] Create `src/ccp/models/sfl_query_models.py`
- [ ] Define enums for query modes, evidence kinds, selection sources, warning codes, assembly statuses
- [ ] Define `SubliminalFunctionQueryRequest`
- [ ] Define `SubliminalFunctionQueryResponse`
- [ ] Define `FunctionProfileAssemblyRequest`
- [ ] Define `FunctionProfileAssemblyResult`
- [ ] Define `SubliminalFunctionProfile`
- [ ] Define `SubliminalFunctionStackPacket`
- [ ] Create `src/ccp/services/sfl_query_service.py`
- [ ] Inject `SFLRegistryService` dependency from FR-ERA3-25
- [ ] Inject `PrimitiveRegistryQueryService` dependency from FR-ERA3-06
- [ ] Inject `SDARegistryService` dependency from FR-ERA3-20
- [ ] Implement family lookup
- [ ] Implement function-id lookup
- [ ] Implement primitive-crosswalk lookup
- [ ] Implement representation-geometry profile lookup
- [ ] Implement archetype-profile lookup
- [ ] Implement surface-profile lookup
- [ ] Implement deterministic precedence merge
- [ ] Implement family-only fallback handling
- [ ] Implement profile conflict reporting
- [ ] Implement version stamp and registry hash propagation
- [ ] Implement query cache warm / rebuild path
- [ ] Implement targeted invalidation / previous-good rollback
- [ ] Create `tests/integration/test_era3_fr26_sfl_query_service.py`
- [ ] Create `tests/integration/test_era3_fr26_sfl_profile_resolution.py`
- [ ] Seed minimal SFL test fixtures referencing real primitive IDs and real SDA geometry IDs

---

## 8. Acceptance Criteria

### AC-26.1 - Query by family returns only canonical family-aligned functions

**Given** a warm SFL registry and a valid `SFL-FAM-*` family ID  
**When** `query_mode=by_family` is executed  
**Then** the response returns only canonical family metadata and canonical functions linked to that family, with no metrics, policies, or adversarial assets mixed into the payload

- Constraint enforced: `No-Function-Hallucination Rule`, `Role-before-Schema rule`
- Failure example: `cognitive_imprint_score` or `FalseDepthContrastCase` is returned as if it were a canonical function
- Measurable pass condition: all returned `function_id` values match `^SFL-FN-\d{3}$` and all evidence points back to FR-ERA3-25 canonical artifacts

### AC-26.2 - Query by primitive uses maintained crosswalk evidence only

**Given** a valid primitive ID such as `PRM-BUS-001` or `EXP-FBK-001`  
**When** `query_mode=by_primitive_crosswalk` is executed  
**Then** the service returns only families and functions supported by maintained primitive-to-family crosswalk artifacts and does not infer additional functions from primitive summaries or aliases

- Constraint enforced: `Primitive/SDA/SFL boundary rule`, `No-Function-Hallucination Rule`
- Failure example: the service reads a primitive summary mentioning "trust" and invents a trust/proof function without a crosswalk artifact
- Measurable pass condition: evidence trace contains `ProfileEvidenceKind.PRIMITIVE_CROSSWALK` entries only for canonical crosswalk IDs and no extra inferred function IDs

### AC-26.3 - Geometry profile resolution preserves SDA ownership

**Given** a valid representation geometry ID  
**When** `query_mode=by_representation_geometry` or packet assembly with `representation_geometry_id` is executed  
**Then** the service may read maintained geometry-profile crosswalks but may not emit ontology verdicts, invariant metrics, or directional-integrity evaluation fields

- Constraint enforced: `Primitive/SDA/SFL boundary rule`
- Failure example: the response includes `invariant_gravity`, `invariant_activation_intensity`, or a directional-integrity pass/fail verdict
- Measurable pass condition: the response contains only profile-resolution objects, warnings, and evidence trace records

### AC-26.4 - Deterministic profile assembly produces the same stack for the same inputs

**Given** the same warm SFL registry, the same primitive IDs, the same geometry ID, the same archetype, the same delivery surface, and the same explicit overrides  
**When** `assemble_profile()` is called repeatedly  
**Then** the resulting `SubliminalFunctionStackPacket.active_function_ids` and evidence trace ordering remain identical across runs

- Constraint enforced: `Deterministic profile assembly`
- Failure example: two identical calls yield different active functions because lower-priority hints were merged in non-deterministic order
- Measurable pass condition: repeated calls produce byte-equivalent ordered function ID lists and identical precedence-ranked evidence records

### AC-26.5 - Partial evidence degrades safely without silent invention

**Given** a request where only primitive crosswalk family evidence exists and exact function-level archetype or geometry evidence is missing  
**When** `assemble_profile()` is called with `allow_family_only_fallback=True`  
**Then** the service returns `status=family_only` or `status=partial`, emits explicit warnings, and builds a bounded packet from canonical family defaults only

- Constraint enforced: `Failure-closed profile resolution`
- Failure example: the service silently promotes arbitrary functions because the family had no exact preferred-function record
- Measurable pass condition: the packet is marked degraded and every active function has `selection_source=FALLBACK_FROM_FAMILY` or a higher-priority canonical source

### AC-26.6 - Conflicting profiles do not get averaged into centroid stacks

**Given** explicit function overrides or archetype defaults that conflict with hard surface constraints or higher-priority geometry rules  
**When** `assemble_profile()` is called  
**Then** the service either suppresses the lower-priority candidates with explicit conflict records or marks the assembly `review_required`

- Constraint enforced: `Anti-Centroid Law preservation`, `Failure-closed profile resolution`
- Failure example: conflicting function sets are naively unioned into a bloated all-family stack
- Measurable pass condition: conflict records identify higher- and lower-priority evidence and either suppress or escalate rather than unioning blindly

### AC-26.7 - Hot-path lookup avoids repeated disk reads after warm

**Given** a warmed query cache  
**When** canonical family/function/profile lookups are executed repeatedly on the hot path  
**Then** the service serves results from the in-process mirror without additional registry YAML reads unless targeted reload has invalidated the affected index

- Constraint enforced: deterministic runtime substrate
- Failure example: every lookup reparses the SFL YAML tree or reconstructs all crosswalks from disk
- Measurable pass condition: hot-path queries complete from the warmed mirror and targeted invalidation rebuilds only the affected indexes

### AC-26.8 - Failed targeted rebuild preserves previous good query state

**Given** the service is warm and a linked SFL artifact reload introduces an invalid function or crosswalk record  
**When** the query-cache rebuild or targeted invalidation path runs  
**Then** the service rejects the bad state and preserves the previous-good in-memory indexes and version stamp

- Constraint enforced: `Failure-closed profile resolution`
- Failure example: a bad crosswalk update partially replaces the primitive index and makes some queries silently wrong
- Measurable pass condition: rebuild returns failure, emits a receipt, and the previous valid lookup results remain unchanged

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | Canonical prerequisite | Families, function definitions, compression rules, and crosswalk artifacts |
| `FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md` | Reads / interop | Valid primitive lookup, batch-query pattern, and targeted invalidation semantics |
| `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Reads / interop | Valid representation geometry lookup and reload semantics |
| `src/ccp/core/receipt_chain.py` | Core runtime | Machine-readable receipt emission |
| `PRD_02_CCF_Content_Factory.md` | Source PRD | Runtime insertion point and compiler ownership boundary |
| `PRD_08_Conscious_Primitives.md` | Source PRD | Primitive/SDA/SFL boundary and fail-closed law |

### External

| API/Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed query, profile, and packet models |
| `pytest` | Current repo standard | Integration and unit testing |
| `PyYAML` | Current repo standard | Indirect canonical artifact loading through FR-ERA3-25 service |

---

## 10. Testing Strategy

### Unit Tests

Create `tests/unit/test_era3_fr26_sfl_query_models.py` with at least:

- `test_query_request_requires_matching_target_for_mode`
- `test_stack_packet_requires_valid_sfl_function_ids`
- `test_profile_conflict_record_restricts_scope_values`
- `test_assembly_request_rejects_noncanonical_override_ids`

### Integration Tests

Create:

- `tests/integration/test_era3_fr26_sfl_query_service.py`
- `tests/integration/test_era3_fr26_sfl_profile_resolution.py`

Model them on:

- `tests/integration/test_era3_fr06_primitive_registry.py`
- `tests/integration/test_era3_fr20_sda_registry.py`

Required integration cases:

1. `TestWarmAndLookup.test_ac261_query_by_family_returns_only_canonical_functions`
2. `TestWarmAndLookup.test_ac262_query_by_primitive_uses_crosswalk_evidence_only`
3. `TestBoundaryEnforcement.test_ac263_geometry_lookup_does_not_emit_sda_runtime_metrics`
4. `TestAssemblyDeterminism.test_ac264_same_inputs_produce_same_stack`
5. `TestFallbacks.test_ac265_partial_evidence_degrades_to_family_only_with_warning`
6. `TestConflictHandling.test_ac266_conflicting_profiles_do_not_union_into_centroid_stack`
7. `TestHotPathBehavior.test_ac267_repeated_queries_use_warmed_indexes`
8. `TestReloadSafety.test_ac268_failed_rebuild_preserves_previous_good_state`

### Fixture Requirements

The fixture set should include:

- at least 2 canonical SFL families
- at least 4 canonical SFL functions
- at least 1 primitive-to-family crosswalk using a real primitive ID
- at least 1 representation-geometry profile using a real `SDA-RPG-*` ID
- at least 1 archetype profile
- at least 2 surface constraint profiles
- at least 1 conflict scenario where surface rules suppress lower-priority function picks

### Manual Verification

1. Warm the FR-ERA3-25 registry and confirm the query service mirrors canonical data without mutating ownership.
2. Query a known family and verify only canonical functions are returned.
3. Query a known primitive crosswalk and verify the returned families match maintained crosswalk records.
4. Assemble a stack with:
   - one geometry ID
   - one archetype
   - one surface
   - two primitive IDs
   and confirm the packet contains ordered evidence trace records.
5. Remove the geometry profile from fixtures and confirm the service degrades to `partial` or `family_only` rather than inventing functions.
6. Introduce a hard conflict between explicit override and surface constraint and confirm the service emits `review_required` or suppresses the lower-priority selection.
7. Corrupt one linked crosswalk artifact and confirm targeted rebuild preserves previous-good query results.

### Exit Criteria

- all query surfaces operate against canonical SFL substrate only
- packet assembly is deterministic
- partial evidence handling is explicit and failure-closed
- no evaluator logic leaks into lookup/assembly
- no primitive or SDA ownership fields leak into SFL packets
- targeted rebuild and hot-path cache behavior are verified

