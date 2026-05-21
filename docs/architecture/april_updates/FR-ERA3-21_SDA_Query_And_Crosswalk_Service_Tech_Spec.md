# Tech-Spec: FR-ERA3-21 — SDA Query and Crosswalk Service
**Created:** 2026-05-12
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — SDA Foundation)
**Phase:** 6 — Semantic Discernment Architecture Foundation
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROMPT LOADED:     P6_S36_FR-ERA3-21_SDA_Query_And_Crosswalk_Service.md — defines a sibling query service for SDA registries and crosswalks, with explicit ban on merging SDA into the primitive registry.
2. SOURCE PRDS READ:  PRD-02 §3.1-3.4A adds SDA packets (`InvariantFieldPacket`, `ArchetypalGeometryPacket`, `RepresentationGeometryPacket`, `SpeciesHypothesisPacket`, `DirectionalIntegrityReport`, `HardNegativeEvaluationReport`) and compiler law `signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> directional integrity validation -> JIT script contract -> render blueprint`.
3. SOURCE PRDS READ:  PRD-08 §3.6 states primitives remain transformation operators while SDA artifacts are sibling intelligence structures; stack is `context substrate -> SDA field -> primitive candidate field -> coalition -> archetype container -> SDA validation -> destination packet`.
4. SDA SOURCES READ:  `semantic_discernment_architecture_content_engine_v_1.md` — existential invariants are "high-gravity semantic attractors"; hard negatives are deceptively close failures; directional integrity must be validated, not assumed.
5. SDA SOURCES READ:  `semantic_discernment_architecture_artifact_taxonomy_v_1.md` — canonical ontology = `Existential Invariants`, `Representation Geometries`; canonical structural grammar = `Archetypal Geometries`, `Species Composition Grammar`; crosswalks = `Primitive-to-Invariant`, `Edge-to-Species`, `Archetype-to-Geometry`; runtime-derived forms and semantic-dynamics objects are NOT canonical query surfaces by default.
6. SDA SOURCES READ:  `Perceptual_Primitives_Architecture.md` — `CRAL evidence -> primitive spaces -> candidate survival -> coalition signature -> edge product -> CCF routing`; edge products are emergent products, not basis objects.
7. SDA SOURCES READ:  `Matrix of Edging.md` — broad primary signal is pre-trigger pressure; edge product formation is post-trigger force; edging selects force while experience primitives deliver force.
8. FR READ:           FR-ERA3-20 SDA Ontology and Registry — canonical SDA registries are `Existential Invariants`, `Representation Geometries`, `Archetypal Geometries`, `Species Composition Grammar`; crosswalk registries are `Primitive-to-Invariant` and `Archetype-to-Geometry`; `Content Species`, `Hard Negatives`, `Recursive Patterns`, and `Feedback Loops` are explicitly rejected as canonical registries.
9. FR READ:           FR-ERA3-06 Primitive Registry Query Service — primitive service owns primitive YAML loading, plane/family queries, conflict resolution, and cache invalidation. This FR must interoperate with, not absorb or duplicate, that ownership.
10. BACKEND FILES READ:
    - `src/ccp/services/cpr_query_service.py` — `CPRQueryService.__init__(coach_id, supabase_client=None, receipt_chain=None)` and `query_registry(...) -> CPRQueryResult`
    - `src/ccp/services/known_persons_registry_adapter.py` — staged registry query, context validation, fallback logic, and audit logging
    - `src/ccp/services/tiar_adapter.py` — fresh/stale cache handling, query + validation split, upstream injection and downstream validation pattern
11. TEST PATTERNS READ:
    - `tests/integration/test_vis12_known_persons.py`
    - `tests/integration/test_vis02_tiar_integration.py`
    Both show class-per-AC organization, explicit fallback tests, and receipt/audit verification.
12. LIVE PRIMITIVES VERIFIED:
    - `EXP-FBK-001` RIM Feedback Discipline (`crosswalk_id: XW-FBK-RIM`)
    - `EXP-PRG-001` Hook Cycle Velocity (`crosswalk_id: XW-PRG-VELOCITY`)
    - `EXP-TRS-003` Reflective Social Proof (`crosswalk_id: XW-TRS-PROOF`)
    These IDs are real and suitable for primitive-to-invariant crosswalk examples in this spec.
13. PHASE TRACEABILITY NOTE:
    No dedicated Phase 6 epic file exists yet. Architectural authority for this spec comes from the Wave 0 PRD updates plus the four SDA main documents above.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S36_FR-ERA3-21_SDA_Query_And_Crosswalk_Service.md` | Prompt requirements and output constraints |
| 2 | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Canonical SDA registry boundaries |
| 3 | `docs/architecture/april_updates/FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md` | Sibling primitive service ownership and route patterns |
| 4 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | CCF runtime law and SDA packet dependency |
| 5 | `docs/prd/modules/PRD_08_Conscious_Primitives.md` | Primitive/SDA boundary and orchestration stack |
| 6 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Deep SDA doctrine: invariants, hard negatives, directional integrity |
| 7 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Artifact taxonomy and crosswalk classes |
| 8 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Edge product and coalition lineage |
| 9 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | Broad signal vs edge-product phase split |
| 10 | `src/ccp/services/cpr_query_service.py` | Query service pattern and receipt integration |
| 11 | `src/ccp/services/known_persons_registry_adapter.py` | Registry adapter pattern with fallback rules |
| 12 | `src/ccp/services/tiar_adapter.py` | Fresh/stale cache, validation split, audit style |
| 13 | `tests/integration/test_vis12_known_persons.py` | Integration test organization and fallback expectations |
| 14 | `tests/integration/test_vis02_tiar_integration.py` | Cache/fallback test patterns |
| 15 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Real primitive ID and crosswalk anchor |
| 16 | `primitives/experience/progression/EXP-PRG-001.yaml` | Real primitive ID and crosswalk anchor |
| 17 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Real primitive ID and crosswalk anchor |

---

## 2. Overview

### 2.1 Problem Statement — What breaks without this spec?

`FR-ERA3-20` defines what SDA artifacts exist, but it does not yet provide the runtime query layer that allows other systems to resolve those artifacts safely and consistently. Without this service:

- `FR-ERA3-16` and future CCF runtimes cannot retrieve canonical invariant, geometry, and species-composition records without direct file access or bespoke adapters.
- primitive-to-invariant and archetype-to-geometry reasoning drifts into ad hoc logic inside downstream services, producing duplicated mapping rules and silent disagreement.
- edge-to-species resolution risks pretending derived `Content Species` objects are canonical registry rows, violating the taxonomy and confusing runtime semantics with ontology.
- provenance is lost. A caller can receive a semantic answer without knowing which registry version, crosswalk row, or source file justified it.
- the platform will be tempted to expand `FR-ERA3-06` into a "universal meaning service," collapsing the primitive/SDA separation that `PRD-08` now explicitly protects.

### 2.2 Solution

Build a dedicated `SDAQueryAndCrosswalkService` that:

- loads and caches canonical SDA registries defined by `FR-ERA3-20`
- exposes typed query surfaces for canonical ontology and structural grammar
- resolves maintained crosswalk objects for:
  - primitive -> invariant
  - archetype container -> archetypal geometry
  - edge product -> species reference bundle
- returns lineage and version provenance with every response
- rejects non-canonical runtime objects as default query targets
- interoperates with `FR-ERA3-06` instead of duplicating primitive ownership

### 2.3 Scope

**In scope**

- Canonical query surfaces for:
  - `Existential Invariants`
  - `Representation Geometries`
  - `Archetypal Geometries`
  - `Species Composition Grammar`
- Maintained crosswalk query surfaces for:
  - `Primitive-to-Invariant`
  - `Archetype-to-Geometry`
  - `Edge-to-Species`
- cache warm/load/refresh behavior and version-consistency rules
- request/response contracts with provenance and lineage
- explicit queryability rules for canonical vs derived vs runtime-only SDA artifacts
- FastAPI routes under `/api/sda/*`
- receipt logging and integration testing

**Out of scope**

- Authoring or editing SDA ontology files
- Generating `InvariantFieldPacket`, `SpeciesHypothesisPacket`, `DirectionalIntegrityReport`, or `HardNegativeEvaluationReport`
- running semantic evaluation itself (`FR-ERA3-22`)
- maintaining the hard-negative corpus (`FR-ERA3-24`)
- changing primitive query semantics already owned by `FR-ERA3-06`

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object | Source | What It Does |
|--------|-------------|--------|--------------|
| DEP-SDA-001 | `ExistentialInvariantRecord` | FR-ERA3-21 | Canonical invariant ontology payload |
| DEP-SDA-002 | `RepresentationGeometryRecord` | FR-ERA3-21 | Canonical representation geometry payload |
| DEP-SDA-003 | `ArchetypalGeometryRecord` | FR-ERA3-21 | Canonical archetypal geometry payload |
| DEP-SDA-004 | `SpeciesCompositionRuleRecord` | FR-ERA3-21 | Canonical species composition grammar payload |
| DEP-SDA-005 | `PrimitiveInvariantResolutionResult` | FR-ERA3-21 | Primitive-to-invariant crosswalk payload |
| DEP-SDA-006 | `ArchetypeGeometryResolutionResult` | FR-ERA3-21 | Archetype-to-geometry crosswalk payload |
| DEP-SDA-007 | `EdgeSpeciesResolutionResult` | FR-ERA3-21 | Edge-to-species crosswalk payload |

### 3.2 Canonical vs Maintained vs Runtime Query Surfaces

The service must make this separation explicit in code and API contracts:

| Artifact | Queryable Here? | Why |
|----------|------------------|-----|
| `Existential Invariant` | Yes | Canonical ontology from `FR-ERA3-20` |
| `Representation Geometry` | Yes | Canonical ontology from `FR-ERA3-20` |
| `Archetypal Geometry` | Yes | Canonical structural grammar |
| `Species Composition Grammar` | Yes | Canonical structural grammar |
| `Primitive-to-Invariant Crosswalk` | Yes | Maintained mapping object |
| `Archetype-to-Geometry Crosswalk` | Yes | Maintained mapping object |
| `Edge-to-Species Crosswalk` | Yes, as maintained mapping bundle | Taxonomy allows it as mapping object, but not as canonical species registry |
| `Content Species` | No, not as canonical row | Derived semantic form; resolved elsewhere or returned only as reference candidates |
| `Edge Product` | No, not as canonical row | Derived runtime form |
| `Recursive Pattern` | No | Runtime semantic-dynamics object |
| `Emergent Contextual Invariant` | No | Runtime inference object |
| `Feedback Loop` | No | Longitudinal runtime object |
| `DirectionalIntegrityReport` | No | Runtime evaluation packet |
| `HardNegativeEvaluationReport` | No | Runtime evaluation packet |

### 3.3 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `cpr_query_service.py` | `src/ccp/services/cpr_query_service.py` | Service initialization and receipt pattern. `query_registry(...) -> CPRQueryResult` is the closest existing query-service precedent. |
| `known_persons_registry_adapter.py` | `src/ccp/services/known_persons_registry_adapter.py` | Context-validation and fallback-query pattern. The new service should mirror "query -> validate -> resolve -> log" staging. |
| `tiar_adapter.py` | `src/ccp/services/tiar_adapter.py` | Fresh/stale cache policy and upstream/downstream validation split. The new service uses the same idea for stale crosswalk fallback. |
| `FR-ERA3-06` | `docs/architecture/april_updates/FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md` | Defines primitive-service ownership that this spec must preserve. |
| `PRD-02` | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Consumes outputs of this service through later runtime packets and routing layers. |
| `PRD-08` | `docs/prd/modules/PRD_08_Conscious_Primitives.md` | Establishes primitives as operators and SDA as sibling stack. |

### 3.4 File-System Source Layout

This spec assumes the registry layout established by `FR-ERA3-20`:

```text
semantic_discernment/
  ontology/
    existential_invariants/
      SDA-INV-*.yaml
    representation_geometries/
      SDA-RPG-*.yaml
  grammar/
    archetypal_geometries/
      SDA-ARG-*.yaml
    species_composition/
      SDA-SCG-*.yaml
  crosswalks/
    primitive_to_invariant/
      XW-PRI-*.yaml
    archetype_to_geometry/
      XW-ATG-*.yaml
    edge_to_species/
      XW-ETS-*.yaml
```

The exact file count is expected to grow, so the service must index by typed surface and not by hand-maintained file lists.

### 3.5 Boundary With FR-ERA3-06 Primitive Registry Query Service

This is the most important non-negotiable in the spec.

`FR-ERA3-06` keeps ownership of:

- primitive YAML parsing
- primitive cache warm/load/invalidation
- primitive plane/family/tag query
- primitive conflict resolution
- primitive metadata truth

`FR-ERA3-21` owns:

- SDA ontology query
- SDA grammar query
- maintained crosswalk query
- lineage between primitives, archetypes, edge products, and SDA objects

So a primitive-to-invariant resolution must:

1. validate the primitive IDs through `FR-ERA3-06`
2. resolve invariant mappings through SDA crosswalk files
3. return lineage showing both surfaces

It must **not** duplicate primitive registry state locally beyond lightweight read-through cache summaries needed for resolution.

### 3.6 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|---------------------|--------------|
| Separate SDA query service | Keeps ontology/query responsibilities distinct from primitive registry | Expand `FR-ERA3-06` into SDA | Violates `PRD-08` boundary and muddies ownership |
| Query canonical + maintained surfaces only | Preserves taxonomy law | Query every SDA artifact uniformly | Treats runtime packets and derived forms as if they were canonical ontology |
| Return edge-to-species as candidate reference bundle | Taxonomy allows maintained mapping without falsely canonizing `Content Species` | Build canonical `ContentSpeciesRegistry` here | Direct contradiction with `FR-ERA3-20` |
| Read-through cache with stale fallback | Matches `tiar_adapter.py` resilience pattern | Hard fail on any cache inconsistency | Too brittle for a registry service that other runtimes depend on |
| Explicit provenance block on every response | Supports audits and downstream explainability | Bare semantic result only | Loses lineage and makes drift debugging impossible |

---

## 4. Implementation Plan

### Phase A: Models and Registry Contracts

- [ ] **Task 1:** Create `src/ccp/models/sda_query_models.py` with typed canonical-record and crosswalk-response models.
- [ ] **Task 2:** Define `SDA_QUERY_AUDIT_SQL` and registry/cache constants in `sda_query_models.py`.
- [ ] **Task 3:** Add enums for `SDAQueryableSurface`, `SDAResolutionStatus`, and `SDAFallbackReason`.

### Phase B: Loader, Cache, and Resolver

- [ ] **Task 4:** Create `src/ccp/services/sda_query_service.py` with `SDARegistryLoader` to recursively load canonical registry and crosswalk files.
- [ ] **Task 4a:** Implement file hashing (SHA-256) and `source_version` extraction for each loaded YAML file in the `SDARegistryLoader` to populate the `SDAProvenanceBlock` fields (`source_hash`, `source_version`).
- [ ] **Task 5:** Implement `SDARegistryCacheManager` with per-surface cache keys, manifest hash storage, and stale-fallback state.
- [ ] **Task 6:** Implement `SDACrosswalkResolver` with dedicated resolution methods for primitive/invariant, archetype/geometry, and edge/species.
- [ ] **Task 6a:** Parse the `confidence` values for primitive-to-invariant and edge-to-species candidates directly from the maintained crosswalk YAML files; do not calculate them dynamically.
- [ ] **Task 6b:** Parse the `carrier_strength` value for archetype-to-geometry candidates directly from the maintained crosswalk YAML files; do not compute it dynamically.
- [ ] **Task 7:** Add read-through interop to `FR-ERA3-06` for primitive existence/metadata verification during primitive crosswalk resolution.

### Phase C: API Layer

- [ ] **Task 8:** Create `src/ccp/api/sda_query_api.py` and expose typed routes for canonical query and crosswalk resolution.
- [ ] **Task 9:** Add `/api/sda/queryable-surfaces` and `/api/sda/health` to make surface ownership and cache health explicit.
- [ ] **Task 10:** Register the router in `src/ccp/api/main.py` and warm caches during app startup.

### Phase D: Testing and Auditability

- [ ] **Task 11:** Create `tests/integration/test_era3_fr21_sda_query_service.py`.
- [ ] **Task 12:** Create `tests/integration/test_era3_fr21_crosswalk_resolution.py`.
- [ ] **Task 13:** Create `tests/integration/test_era3_fr21_sda_query_api.py`.
- [ ] **Task 14:** Wire `ReceiptChain.log()` calls for warm, query, resolve, fallback, and refresh operations.

---

## 5. Primary Output Schema

```python
# src/ccp/models/sda_query_models.py
from __future__ import annotations

from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field


SDA_QUERY_AUDIT_SQL = """
CREATE TABLE IF NOT EXISTS sda_query_audit (
    audit_id              TEXT PRIMARY KEY,
    action_type           TEXT NOT NULL,
    queryable_surface     TEXT NOT NULL,
    request_payload       JSONB NOT NULL,
    response_summary      JSONB NOT NULL,
    provenance_bundle     JSONB NOT NULL,
    used_stale_fallback   BOOLEAN NOT NULL DEFAULT FALSE,
    fallback_reason       TEXT,
    latency_ms            REAL NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


class SDAQueryableSurface(str, Enum):
    EXISTENTIAL_INVARIANT = "existential_invariant"
    REPRESENTATION_GEOMETRY = "representation_geometry"
    ARCHETYPAL_GEOMETRY = "archetypal_geometry"
    SPECIES_COMPOSITION_GRAMMAR = "species_composition_grammar"
    PRIMITIVE_TO_INVARIANT = "primitive_to_invariant_crosswalk"
    ARCHETYPE_TO_GEOMETRY = "archetype_to_geometry_crosswalk"
    EDGE_TO_SPECIES = "edge_to_species_crosswalk"


class SDAResolutionStatus(str, Enum):
    RESOLVED = "resolved"
    PARTIAL = "partial"
    NOT_FOUND = "not_found"
    REJECTED_NON_CANONICAL = "rejected_non_canonical"


class SDAFallbackReason(str, Enum):
    NONE = "none"
    STALE_CACHE = "stale_cache"
    DOWNSTREAM_PRIMITIVE_UNAVAILABLE = "downstream_primitive_unavailable"
    MANIFEST_MISMATCH = "manifest_mismatch"


class SDAProvenanceBlock(BaseModel):
    registry_surface: SDAQueryableSurface
    source_file: str
    source_version: str
    source_hash: str
    loaded_at: str
    registry_manifest_hash: str
    supporting_refs: list[str] = Field(default_factory=list)


class ExistentialInvariantRecord(BaseModel):
    invariant_id: str
    canonical_name: str
    definition: str
    invariant_gravity: float = Field(ge=0.0, le=1.0)
    tension_poles: list[str] = Field(default_factory=list)
    distortion_modes: list[str] = Field(default_factory=list)
    provenance: SDAProvenanceBlock


class RepresentationGeometryRecord(BaseModel):
    geometry_id: str
    canonical_name: str
    authority_structure: str
    identity_framing: str
    fear_weighting: float = Field(ge=0.0, le=1.0)
    drift_risks: list[str] = Field(default_factory=list)
    provenance: SDAProvenanceBlock


class ArchetypalGeometryRecord(BaseModel):
    geometry_id: str
    canonical_name: str
    definition: str
    authority_flow: str
    agency_distribution: str
    transformation_pattern: str
    provenance: SDAProvenanceBlock


class SpeciesCompositionRuleRecord(BaseModel):
    rule_id: str
    canonical_name: str
    admissible_bindings: list[str] = Field(default_factory=list)
    forbidden_pairings: list[str] = Field(default_factory=list)
    instability_triggers: list[str] = Field(default_factory=list)
    provenance: SDAProvenanceBlock


class PrimitiveReference(BaseModel):
    primitive_id: str
    primitive_plane: Literal["experience", "meaning"]
    canonical_name: str | None = None
    family: str | None = None


class PrimitiveInvariantCandidate(BaseModel):
    invariant_id: str
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)
    crosswalk_id: str
    provenance: SDAProvenanceBlock


class PrimitiveInvariantResolutionResult(BaseModel):
    status: SDAResolutionStatus
    primitive: PrimitiveReference
    invariant_candidates: list[PrimitiveInvariantCandidate] = Field(default_factory=list)
    used_stale_fallback: bool = False
    fallback_reason: SDAFallbackReason = SDAFallbackReason.NONE


class ArchetypeGeometryCandidate(BaseModel):
    archetype_id: str
    archetype_label: str
    geometry_id: str
    rationale: str
    carrier_strength: float = Field(ge=0.0, le=1.0)
    crosswalk_id: str
    provenance: SDAProvenanceBlock


class ArchetypeGeometryResolutionResult(BaseModel):
    status: SDAResolutionStatus
    candidates: list[ArchetypeGeometryCandidate] = Field(default_factory=list)
    used_stale_fallback: bool = False
    fallback_reason: SDAFallbackReason = SDAFallbackReason.NONE


class EdgeProductReference(BaseModel):
    edge_product_id: str
    edge_label: str
    coalition_signature_id: str | None = None
    invariant_field_id: str | None = None


class EdgeSpeciesCandidate(BaseModel):
    species_reference_id: str
    species_label: str
    composition_rule_id: str
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)
    canonical_species_record_exists: bool = False
    crosswalk_id: str
    provenance: SDAProvenanceBlock


class EdgeSpeciesResolutionResult(BaseModel):
    status: SDAResolutionStatus
    edge_product: EdgeProductReference
    species_candidates: list[EdgeSpeciesCandidate] = Field(default_factory=list)
    note: str = Field(
        default="Content Species are derived semantic forms. This service returns maintained candidate references, not canonical species rows."
    )
    used_stale_fallback: bool = False
    fallback_reason: SDAFallbackReason = SDAFallbackReason.NONE


class SDAQueryableSurfaceManifest(BaseModel):
    canonical_surfaces: list[SDAQueryableSurface]
    maintained_crosswalk_surfaces: list[SDAQueryableSurface]
    rejected_runtime_surfaces: list[str]
    sibling_service_dependencies: list[str]
    manifest_hash: str


class SDAHealthStatus(BaseModel):
    cached_surfaces: dict[str, int]
    registry_manifest_hash: str
    stale_surfaces: list[str] = Field(default_factory=list)
    primitive_service_reachable: bool
    last_warm_at: str
```

### 5.1 Service Class Contract

```python
class SDAQueryAndCrosswalkService:
    def __init__(
        self,
        coach_id: str,
        supabase_client: Any = None,
        receipt_chain: ReceiptChain | None = None,
        primitive_registry_client: PrimitiveRegistryQueryService | None = None,
    ) -> None: ...

    def query_invariant(self, invariant_id: str) -> ExistentialInvariantRecord | None: ...
    def query_representation_geometry(self, geometry_id: str) -> RepresentationGeometryRecord | None: ...
    def query_archetypal_geometry(self, geometry_id: str) -> ArchetypalGeometryRecord | None: ...
    def query_species_composition_rule(self, rule_id: str) -> SpeciesCompositionRuleRecord | None: ...

    def resolve_primitive_to_invariant(
        self,
        primitive_ids: list[str],
    ) -> list[PrimitiveInvariantResolutionResult]: ...

    def resolve_archetype_to_geometry(
        self,
        archetype_ids: list[str],
    ) -> list[ArchetypeGeometryResolutionResult]: ...

    def resolve_edge_to_species(
        self,
        edges: list[EdgeProductReference],
    ) -> list[EdgeSpeciesResolutionResult]: ...

    def query_surface_manifest(self) -> SDAQueryableSurfaceManifest: ...
    def refresh_registry(self, surfaces: list[SDAQueryableSurface] | None = None) -> SDAHealthStatus: ...
    def health(self) -> SDAHealthStatus: ...
```

### 5.2 API Surface

```text
GET  /api/sda/invariants/{invariant_id}
GET  /api/sda/representation-geometries/{geometry_id}
GET  /api/sda/archetypal-geometries/{geometry_id}
GET  /api/sda/species-composition-rules/{rule_id}

POST /api/sda/crosswalks/primitive-to-invariant/resolve
POST /api/sda/crosswalks/archetype-to-geometry/resolve
POST /api/sda/crosswalks/edge-to-species/resolve

GET  /api/sda/queryable-surfaces
GET  /api/sda/health
POST /api/sda/refresh
```

### 5.3 Example Response Notes

- `primitive-to-invariant` responses must include the primitive ID, the verified primitive plane if known, candidate invariants, and crosswalk provenance.
- `archetype-to-geometry` responses must include carrier-strength style ranking because one archetype may validly carry more than one geometry.
- `edge-to-species` responses must explicitly state that species candidates are references to derived forms, not canonical ontology records.

---

## 6. Backward Compatibility Fallback

This service should degrade safely, not optimistically hallucinate semantic answers.

1. **Canonical registry cache is stale but parseable**
   - Serve the last known cached record.
   - Mark `used_stale_fallback = true`.
   - Return `fallback_reason = stale_cache`.
   - Log a receipt entry naming the stale surface.

2. **Primitive registry dependency is unavailable during primitive-to-invariant resolution**
   - Do not fabricate primitive metadata locally.
   - Return `status = partial` if the crosswalk row exists but primitive verification failed.
   - Include `fallback_reason = downstream_primitive_unavailable`.
   - Allow invariant candidates only if the request explicitly says "best-effort crosswalk without primitive verification"; default behavior is partial, not success.

3. **Manifest hash mismatch between cached surface and current on-disk bundle**
   - Reject full-surface success.
   - Serve stale rows only when the caller is non-authoritative and the stale data is still parseable.
   - Mark `fallback_reason = manifest_mismatch`.

4. **Request targets non-canonical runtime objects**
   - Return `status = rejected_non_canonical`.
   - Include a clear note that the object is runtime-derived and must be resolved by the relevant engine (`FR-ERA3-22`, `FR-ERA3-23`, or future runtime).
   - Do not silently reinterpret the request as a different surface.

5. **Edge-to-species row exists but no current species library match is active**
   - Return candidate references using the crosswalk and composition-rule lineage.
   - Set `canonical_species_record_exists = false`.
   - This is valid behavior, not an error, because the taxonomy says `Content Species` are derived.

---

## 7. Tasks

### Sprint 1: Models and Surface Manifest

- [ ] Create `src/ccp/models/sda_query_models.py` with canonical-record models, crosswalk-resolution models, manifest models, and health/fallback enums.
- [ ] Add `SDA_QUERY_AUDIT_SQL` and cache-key constants such as `sda:inv:{id}`, `sda:rpg:{id}`, `sda:arg:{id}`, `sda:scg:{id}`, `sda:xw:pri:{id}`, `sda:xw:atg:{id}`, `sda:xw:ets:{id}`.
- [ ] Extend `src/ccp/scripts/setup_supabase.py` to append `sda_query_audit` table DDL into the canonical schema bootstrap if audit persistence is being used there.

### Sprint 2: Loader, Cache, and Resolver

- [ ] Create `src/ccp/services/sda_query_service.py` with `SDARegistryLoader` that walks `semantic_discernment/ontology`, `semantic_discernment/grammar`, and `semantic_discernment/crosswalks`.
- [ ] Implement `SDARegistryCacheManager` with per-surface cache warming, manifest hashing, stale-surface tracking, and targeted surface refresh.
- [ ] Implement `SDACrosswalkResolver.resolve_primitive_to_invariant()` that verifies primitive IDs through `FR-ERA3-06` before yielding invariant candidates.
- [ ] Implement `SDACrosswalkResolver.resolve_archetype_to_geometry()` using maintained archetype-carrier mappings rather than runtime inference.
- [ ] Implement `SDACrosswalkResolver.resolve_edge_to_species()` so it returns candidate references backed by `Edge-to-Species` crosswalk rows plus `Species Composition Grammar`.

### Sprint 3: API Wiring

- [ ] Create `src/ccp/api/sda_query_api.py` with the canonical query routes and the three resolution routes.
- [ ] Add `GET /api/sda/queryable-surfaces` that explicitly shows what this service owns vs rejects.
- [ ] Add `POST /api/sda/refresh` guarded as an internal-only maintenance endpoint.
- [ ] Register the router in `src/ccp/api/main.py` and initialize the service at startup after the primitive registry client is available.

### Sprint 4: Test Coverage

- [ ] Add `tests/integration/test_era3_fr21_sda_query_service.py` for cache warm, canonical query, non-canonical rejection, and health.
- [ ] Add `tests/integration/test_era3_fr21_crosswalk_resolution.py` for primitive/invariant, archetype/geometry, and edge/species behavior.
- [ ] Add `tests/integration/test_era3_fr21_sda_query_api.py` for route registration, status codes, provenance shape, and refresh guards.
- [ ] Verify receipt logging for warm, query, resolve, stale fallback, and rejected non-canonical requests.

---

## 8. Acceptance Criteria

### AC-21.1: Canonical Surface Queryability

**Given** the service has warmed the SDA registries from `FR-ERA3-20`,
**When** a caller queries an invariant, representation geometry, archetypal geometry, or species composition rule by ID,
**Then** the service returns a typed record from cache,
**And** the response includes a provenance block with file path, version, hash, and manifest hash,
**And** no direct file I/O occurs on the hot path.

**FAILURE EXAMPLE:** `GET /api/sda/invariants/SDA-INV-001` works, but the response omits source lineage and the service reparses YAML on every request. This breaks auditability and cache guarantees.

**Measurable pass condition:** 100 hot-path canonical queries complete with zero additional disk reads after warm, and every response includes a non-empty `provenance` block.

---

### AC-21.2: Primitive-to-Invariant Resolution Preserves FR-ERA3-06 Ownership

**Given** a caller requests invariant mappings for real primitive IDs such as `EXP-FBK-001`, `EXP-PRG-001`, and `EXP-TRS-003`,
**When** the service resolves `primitive-to-invariant`,
**Then** it verifies the primitive references through `FR-ERA3-06`,
**And** it resolves invariant candidates through maintained SDA crosswalk rows,
**And** it returns lineage showing both the primitive ID and the crosswalk source,
**And** it does not expose duplicated primitive registry records as local SDA truth.

**FAILURE EXAMPLE:** The SDA service answers primitive-to-invariant requests from its own private primitive cache and returns mappings for a primitive ID that the primitive registry no longer recognizes. This violates service ownership and can drift silently.

**Measurable pass condition:** If a primitive is unknown to `FR-ERA3-06`, the result is `partial` or `not_found`, never `resolved`, and known primitives return at least one invariant candidate with a crosswalk provenance record.

---

### AC-21.3: Archetype-to-Geometry Resolution Uses Maintained Carriers

**Given** a caller resolves one or more content archetype IDs,
**When** the service handles `archetype-to-geometry`,
**Then** it returns candidate `ArchetypalGeometry` mappings from the maintained crosswalk surface,
**And** each candidate includes a `carrier_strength` score and rationale,
**And** the response clearly distinguishes carrier validity from runtime semantic inference.

**FAILURE EXAMPLE:** The service guesses a geometry directly from the archetype label using an LLM or embedding similarity without a maintained crosswalk row. The answer may sound plausible but is not canonical or auditable.

**Measurable pass condition:** Every returned geometry candidate references a stored `crosswalk_id`, and deleting that crosswalk row removes the candidate from subsequent results.

---

### AC-21.4: Edge-to-Species Resolution Does Not Falsely Canonize Content Species

**Given** a caller submits an `EdgeProductReference`,
**When** the service resolves `edge-to-species`,
**Then** it returns candidate species references backed by `Edge-to-Species` mapping rows and composition-rule lineage,
**And** it explicitly states that `Content Species` remain derived semantic forms,
**And** it does not claim to fetch a canonical species registry row unless such a future registry actually exists.

**FAILURE EXAMPLE:** The response presents `Content Species` as if they were canonical ontology records with stable registry IDs, even though the taxonomy explicitly marks them as derived forms. Downstream systems then treat species as static truth instead of runtime hypotheses.

**Measurable pass condition:** Every `EdgeSpeciesCandidate` can be traced to a crosswalk row and a composition rule, and the response note explicitly says the result is a candidate reference bundle, not a canonical species record.

---

### AC-21.5: Explicit Rejection of Non-Canonical Runtime Surfaces

**Given** a caller attempts to query `RecursivePattern`, `EmergentContextualInvariant`, `FeedbackLoop`, `DirectionalIntegrityReport`, or `HardNegativeEvaluationReport` through this service,
**When** the request is processed,
**Then** the service returns `rejected_non_canonical`,
**And** it names the relevant runtime/validator engine that owns that object class,
**And** it never silently maps the request to some canonical record type.

**FAILURE EXAMPLE:** A caller requests `DirectionalIntegrityReport` and the service returns an `ArchetypalGeometry` because "it was close enough." That hides an architectural mistake instead of surfacing it.

**Measurable pass condition:** All rejected runtime-surface queries return the same typed rejection status and a deterministic explanatory note.

---

### AC-21.6: Stale Fallback and Version Consistency

**Given** one crosswalk surface becomes stale or its manifest hash no longer matches the warmed cache,
**When** a query hits that surface,
**Then** the service either refreshes it successfully or returns a typed stale-fallback result,
**And** the fallback status and reason are visible in the response and receipt log,
**And** unrelated query surfaces remain available.

**FAILURE EXAMPLE:** A single stale `primitive_to_invariant` file causes the entire SDA query service to fail closed for invariant and geometry lookup even though those canonical surfaces are healthy. This creates unnecessary platform-wide outage.

**Measurable pass condition:** A stale crosswalk surface only taints that surface, `SDAHealthStatus.stale_surfaces` names it explicitly, and healthy surfaces remain queryable.

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | Why It Matters |
|--------------|-----------------|----------------|
| `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Hard architectural dependency | Defines which SDA artifacts are canonical registries and which are not |
| `FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md` | Sibling runtime dependency | Owns primitive verification and primitive metadata truth |
| `PRD_02_CCF_Content_Factory.md` | Downstream consumer | Future CCF runtime uses this service before archetype container and integrity validation |
| `PRD_08_Conscious_Primitives.md` | Governance dependency | Protects primitive/SDA separation |
| `src/ccp/services/cpr_query_service.py` | Pattern reference | Query-service lifecycle and receipt style |
| `src/ccp/services/known_persons_registry_adapter.py` | Pattern reference | Resolution staging and degraded fallback style |
| `src/ccp/services/tiar_adapter.py` | Pattern reference | Cache freshness and stale-surface policy |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Immutable query/resolve audit trail |
| `src/ccp/api/main.py` | Code extension | Router registration and startup warm |
| `semantic_discernment/**` | Data contract | Canonical ontology, grammar, and crosswalk source files |

### External

| Library | Purpose |
|---------|---------|
| `fastapi` | API routing |
| `pydantic` | Typed request/response models |
| `PyYAML` | Parsing SDA registry files |
| `redis` | Optional cache sharing across workers |
| PostgreSQL / Supabase | Optional audit persistence beyond receipt logs |

---

## 10. Testing Strategy

### 10.1 Unit and Integration Test Files

**File:** `tests/integration/test_era3_fr21_sda_query_service.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestCanonicalSurfaceQueries:
    def test_query_invariant_returns_provenance()
    def test_query_representation_geometry_returns_typed_record()
    def test_query_archetypal_geometry_returns_typed_record()
    def test_query_species_composition_rule_returns_typed_record()


class TestQueryableSurfaceBoundaries:
    def test_runtime_surface_request_is_rejected_non_canonical()
    def test_surface_manifest_lists_canonical_and_rejected_surfaces()


class TestHealthAndFallback:
    def test_health_reports_stale_surfaces()
    def test_stale_crosswalk_uses_typed_fallback()
```

**File:** `tests/integration/test_era3_fr21_crosswalk_resolution.py`

```python
class TestPrimitiveToInvariantResolution:
    def test_exp_fbk_001_resolves_with_crosswalk_provenance()
    def test_exp_prg_001_resolves_with_crosswalk_provenance()
    def test_exp_trs_003_resolves_with_crosswalk_provenance()
    def test_unknown_primitive_becomes_partial_or_not_found()


class TestArchetypeToGeometryResolution:
    def test_candidate_rows_require_crosswalk_id()
    def test_deleted_crosswalk_row_removes_candidate()


class TestEdgeToSpeciesResolution:
    def test_returns_candidate_reference_bundle_not_canonical_species_row()
    def test_requires_composition_rule_lineage()
```

**File:** `tests/integration/test_era3_fr21_sda_query_api.py`

```python
class TestSDAQueryAPI:
    def test_get_invariant_route_returns_200()
    def test_get_unknown_geometry_returns_404()
    def test_post_primitive_to_invariant_returns_lineage()
    def test_post_edge_to_species_returns_candidate_note()
    def test_refresh_requires_internal_guard()
```

### 10.2 Test Design Rules

Follow the patterns seen in:

- `tests/integration/test_vis12_known_persons.py`
- `tests/integration/test_vis02_tiar_integration.py`

That means:

- class-per-acceptance-criterion grouping
- explicit fallback-path tests
- deterministic receipt assertions
- no hidden network or model dependencies

### 10.3 Manual Verification

1. Start the API and confirm cache warm logs for all seven SDA query surfaces.
2. Call `GET /api/sda/queryable-surfaces` and confirm canonical vs maintained vs rejected surfaces match this spec.
3. Query a known invariant ID and verify provenance contains file path, version, and manifest hash.
4. Resolve `primitive-to-invariant` for `EXP-FBK-001`, `EXP-PRG-001`, and `EXP-TRS-003` and verify the response includes both primitive IDs and crosswalk lineage.
5. Resolve `archetype-to-geometry` for a known content archetype and verify the result references a stored `crosswalk_id`.
6. Resolve `edge-to-species` and verify the note explicitly says species are derived semantic forms.
7. Request a rejected runtime surface and verify `rejected_non_canonical` is returned instead of a silent fallback.
8. Force one crosswalk bundle stale, then verify canonical surfaces remain healthy while that surface reports stale fallback state.

