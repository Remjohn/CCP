# Tech-Spec: FR-ERA3-25 - Subliminal Function Library and Taxonomy
**Created:** 2026-05-19  
**Status:** Ready for Development  
**Version:** 1.0 (ERA3 Architecture - SFL Foundation)  
**Phase:** 6 - Subliminal Function Layer Foundation  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed the mandatory 10-section spec structure, architecture traceability requirement, typed-model expectation, exact file-read log requirement, and CBAR mandate enforcement table discipline.
2. PRD LOADED:        PRD-02. Confirmed the runtime architecture follows a strict causal order and already separates `Invariant Activation Intensity` from `Invariant Resonance Multiplier`, which means SFL must plug in after semantic-field determination and before final render commitment.
3. PRD LOADED:        PRD-08. Confirmed §3.6 establishes SDA as a sibling intelligence stack with different roles and runtime behaviors, and the runtime stack remains `context substrate -> SDA field -> primitive candidate field -> coalition -> archetype container -> SDA validation -> destination packet`.
4. SFL CORE DOC LOADED: lab/subliminal_function_layer_for_ccp_v_1.md. Confirmed the central law: `SDA protects semantic truthfulness` while `SFL shapes perceptual potency and symbolic aliveness`, and that SFL artifacts split into function families, functions, metrics, policies, adversarial assets, crosswalks, and longitudinal records.
5. SFL FUNCTION DOC LOADED: lab/Subliminal Functions for Agentic Content Architecture.md. Confirmed the 120 associations are explicitly framed as `semantic operators`, `symbolic field functions`, `emotional topology mechanisms`, and `perception-shaping primitives`, not as a flat ontology.
6. ASSOCIATION CHAT LOADED: lab/120 subliminal associations Chat.md. Confirmed the architectural tension between `semantic truthfulness` and `adaptive vitality`, the need to avoid semantic ossification, and the recommendation for dynamic meaning systems rather than over-closed systems.
7. SDA CORE / TAXONOMY LOADED:
   - semantic_discernment_architecture_content_engine_v_1.md confirmed deceptively close failure, existential invariants, representation geometry, hard negatives, and directional integrity remain the deep truth layer.
   - semantic_discernment_architecture_artifact_taxonomy_v_1.md confirmed the role-before-schema law and the existing artifact-class split between canonical, runtime, policy, adversarial, packet, memory, and crosswalk objects.
8. PPA DOC LOADED: Perceptual_Primitives_Architecture.md. Confirmed primitives remain encoded meaning spaces, transformation operators, and candidate generators, which means SFL must not flatten perceptual functions into primitive ownership.
9. PRIMITIVE YAMLs VERIFIED:
   - EXP-FBK-001 = "RIM Feedback Discipline"
   - EXP-FBK-002 = "Reflective Scoring"
   - PRM-BUS-001 = "Perception and Guidance Stack"
   - PRM-BUS-002 = "Emotional Journey / Peak-End"
   Verified current repository conventions for canonical IDs, aliases, fit structures, conflicts/synergies, and crosswalk expectations.
10. BACKEND FILES READ:
   - src/ccp/services/primitive_registry_service.py -> `def query_by_id(self, primitive_id: str, plane: PrimitivePlane | None = None) -> PrimitiveRecord | None:`
   - src/ccp/services/primitive_registry_service.py -> `def query_batch(self, request: PrimitiveQueryRequest) -> PrimitiveQueryResponse:`
   - src/ccp/services/sda_registry_service.py -> `def get_invariant(self, artifact_id: str) -> ExistentialInvariantRecord | None:`
   - src/ccp/services/sda_registry_service.py -> `def get_crosswalk_bundle(self, name: str) -> dict[str, SDARegistryRecord]:`
   - src/ccp/services/sda_registry_service.py -> `def reload_artifact(self, path: str | Path) -> SDAArtifactReloadResult:`
   - src/ccp/services/visual_format_constraint_adapter.py -> deterministic registry-load and sealed-registry pattern
   - src/ccp/services/known_persons_registry_adapter.py -> registry-query and guardrail pattern
11. TEST PATTERNS READ:
   - tests/integration/test_era3_fr20_sda_registry.py -> startup warm, false-registry rejection, targeted reload rollback
   - tests/integration/test_era3_fr06_primitive_registry.py -> deterministic warm-cache behavior, targeted invalidation, and cache-hit expectations
12. WAVE-0 TRACEABILITY CHECK: No dedicated Phase 6 epic file exists yet. This spec therefore uses the SFL doctrine note, the SFL source set, and the existing PRD-02 / PRD-08 boundary laws as the authoritative traceability base.
```

---

## 1. Files Read

| # | File | Date/Version | Purpose |
|---|------|--------------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S49_FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy.md` | 2026-05-18 | Prompt source, scope boundary, and mandatory source set |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Current | Spec-writing protocol and mandatory format |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Current | Runtime law and compiler integration boundary |
| 4 | `docs/prd/modules/PRD_08_Conscious_Primitives.md` | Current | Primitive/SDA sibling-boundary doctrine |
| 5 | `lab/subliminal_function_layer_for_ccp_v_1.md` | 2026-05-18 | Canonical SFL doctrine and artifact taxonomy |
| 6 | `lab/Subliminal Functions for Agentic Content Architecture.md` | Current lab source | 120-association function framing and semantic-system labels |
| 7 | `lab/120 subliminal associations Chat.md` | Current lab source | Association clustering, adaptive-vitality framing, and paradox language |
| 8 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Current lab source | Deep semantic truth layer and deceptively-close-failure problem |
| 9 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Current lab source | Existing SDA artifact classes and role-before-schema law |
| 10 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Current lab source | Primitive spaces and coalition/edge-product sequence |
| 11 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Current repo artifact | Verified primitive ID and naming convention |
| 12 | `primitives/experience/feedback_scoring/EXP-FBK-002.yaml` | Current repo artifact | Verified primitive ID and naming convention |
| 13 | `primitives/meaning/design_business/PRM-BUS-001.yaml` | Current repo artifact | Verified meaning-plane primitive and crosswalk precedent |
| 14 | `primitives/meaning/design_business/PRM-BUS-002.yaml` | Current repo artifact | Verified meaning-plane primitive and experiential-memory relevance |
| 15 | `src/ccp/services/primitive_registry_service.py` | Current code | Query-service, cache, and crosswalk-adjacent substrate pattern |
| 16 | `src/ccp/services/sda_registry_service.py` | Current code | Registry manifest, path validation, and targeted reload pattern |
| 17 | `src/ccp/services/visual_format_constraint_adapter.py` | Current code | Deterministic registry-load and integrity-seal pattern |
| 18 | `src/ccp/services/known_persons_registry_adapter.py` | Current code | Registry query, guardrail, and hard-prohibition pattern |
| 19 | `tests/integration/test_era3_fr20_sda_registry.py` | Current tests | Canonical taxonomy, false-registry rejection, and reload rollback test pattern |
| 20 | `tests/integration/test_era3_fr06_primitive_registry.py` | Current tests | Warm-cache, targeted invalidation, and hot-path test pattern |

---

## 2. Overview

### 2.1 Problem Statement

SFL doctrine now exists in the lab architecture, but the codebase has no canonical machine-readable substrate for perceptual-semantic functions. Without `FR-ERA3-25`:

- the `120 subliminal associations` remain prose and cannot be consumed deterministically by runtime services
- future implementers will likely flatten all 120 terms into one bad registry shape, violating the role-before-schema law already established for SDA
- `covert suggestion`, `soft control`, `hidden intention`, `framing`, `symbolic compression`, and `quiet persuasion` will be treated inconsistently across rendering, evaluation, and content compilation
- `false depth` and `over-optimization` risk being misclassified as valid functions instead of adversarial failure targets
- `FR-ERA3-26`, `FR-ERA3-27`, and `FR-ERA3-28` cannot rely on stable IDs, family compression rules, or maintained crosswalks
- `PRD-08`’s primitive boundary can be violated by accidentally codifying perceptual functions as primitives
- `PRD-02` cannot safely add `SubliminalFunctionStackPacket` and `PerceptualEffectProfile` runtime objects because no canonical substrate exists

The result would be a shallow, inconsistent, and likely bloated implementation of SFL that duplicates SDA in the wrong places and leaves rendering/evaluation layers underspecified.

### 2.2 Solution

This spec establishes the canonical `Subliminal Function Library and Taxonomy` as a **repo-backed, typed, deterministic, sibling substrate** to both the Primitive Registry and SDA. It defines:

- stable `SubliminalFunctionFamily` objects that compress the 120 associations into maintainable families
- callable `SubliminalFunctionDefinition` objects that describe valid perceptual modulation units
- explicit separation between:
  - functions
  - metrics
  - policies
  - adversarial perceptual failure assets
  - crosswalks
  - longitudinal records
- maintained crosswalk bundles connecting:
  - primitives to function families
  - representation geometries to function profiles
  - archetypes to function-stack defaults
  - surfaces to constraint profiles
- deterministic manifest loading, artifact validation, and targeted reload semantics

This is a **foundation spec**. It does not generate content, evaluate content, or own semantic ontology. It defines what the canonical SFL objects are, how they are stored, how they are validated, and how future runtime and evaluator services can safely depend on them.

### 2.3 Scope

**In scope:**

- canonical storage layout for SFL families, function definitions, and maintained crosswalks
- typed Pydantic models for canonical SFL artifact classes
- manifest and boot-time loader for SFL artifacts
- family compression rules for the 120 associations
- explicit rejection rules for:
  - flat-120 designs
  - false-depth stored as function canon
  - runtime metrics stored as canonical function definitions
  - primitive-ownership leakage
  - SDA-ontology duplication
- targeted artifact reload behavior with rollback protection
- receipt-chain logging and service health reporting

**Out of scope:**

- runtime query API surface (`FR-ERA3-26`)
- evaluator metrics and decisions (`FR-ERA3-27`)
- adversarial corpus and contrast harness execution (`FR-ERA3-28`)
- modifications to existing primitive YAMLs
- modifications to existing SDA canonical artifacts
- UI/editor surfacing for SFL selection or review
- DSPy orchestration details
- mathematical/fractal runtime scoring formulas beyond naming future compatibility points

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-SFL-025-01 | `SFLRegistryManifest` | FR-ERA3-25 | Declares canonical directory layout, allowed families, and expected counts |
| DEP-SFL-025-02 | `SFLArtifactValidator` | FR-ERA3-25 | Enforces function-vs-metric-vs-policy separation and path contract |
| DEP-SFL-025-03 | `SFLRegistryService` | FR-ERA3-25 | Loads, validates, caches, and exposes canonical SFL artifacts |
| DEP-SFL-025-04 | `SubliminalFunctionFamilyRecord` | FR-ERA3-25 | Canonical family object for clustered perceptual force types |
| DEP-SFL-025-05 | `SubliminalFunctionDefinitionRecord` | FR-ERA3-25 | Canonical function definition object for runtime function selection |
| DEP-SFL-025-06 | `FunctionFamilyCompressionRuleRecord` | FR-ERA3-25 | Maintains controlled mapping from raw associations into canonical families |
| DEP-SFL-025-07 | `PrimitiveToFunctionFamilyCrosswalkRecord` | FR-ERA3-25 | Maintained mapping from primitives into perceptual function families |
| DEP-SFL-025-08 | `RepresentationGeometryToFunctionProfileRecord` | FR-ERA3-25 | Maintained mapping from SDA geometry into favored function profile |
| DEP-SFL-025-09 | `ArchetypeToFunctionProfileRecord` | FR-ERA3-25 | Maintained mapping from content archetype / container to default function profile |
| DEP-SFL-025-10 | `SurfaceConstraintProfileRecord` | FR-ERA3-25 | Canonical constraint bundle for Telegram, carousel, short-form, webinar, commercial, and audit surfaces |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `primitive_registry_service.py` | `src/ccp/services/primitive_registry_service.py` | Pattern reference for warm-cache, targeted invalidation, query discipline, and crosswalk-adjacent service ownership |
| `sda_registry_service.py` | `src/ccp/services/sda_registry_service.py` | Primary pattern reference for canonical artifact validation, manifest loading, allowed-path enforcement, and targeted reload rollback |
| `visual_format_constraint_adapter.py` | `src/ccp/services/visual_format_constraint_adapter.py` | Pattern reference for deterministic registry loading, integrity protection, and registry health reads |
| `known_persons_registry_adapter.py` | `src/ccp/services/known_persons_registry_adapter.py` | Pattern reference for guardrail-first registry query logic and hard-failure boundaries |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Required receipt log substrate for warm, reject, reload, and rollback stages |
| `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Structural reference for role-before-schema, false-registry rejection, and canonical manifest discipline |
| `tests/integration/test_era3_fr20_sda_registry.py` | `tests/integration/test_era3_fr20_sda_registry.py` | Test pattern for artifact-class guards and reload rollback behavior |
| `tests/integration/test_era3_fr06_primitive_registry.py` | `tests/integration/test_era3_fr06_primitive_registry.py` | Test pattern for deterministic warm and targeted reload semantics |

This spec must not create a generic “semantic super-registry” service. It must create a bounded SFL substrate that interoperates with:

- primitive registry ownership
- SDA ontology ownership
- future evaluator/runtime services

without duplicating their responsibilities.

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FBK-001` | `RIM Feedback Discipline` | `feedback_scoring` | SFL crosswalks must support feedback-delivery functions such as repetition, reflective scoring texture, and perceptual clarity without absorbing feedback mechanics into SFL ownership |
| `EXP-FBK-002` | `Reflective Scoring` | `feedback_scoring` | SFL must allow trust/status reflective cues and identity-signaling function families to map to feedback-facing surfaces |
| `PRM-BUS-001` | `Perception and Guidance Stack` | `design_business` | SFL taxonomy must respect the existing meaning-plane concept that perception and guidance form a unified stack, but still keep perceptual delivery functions separate from meaning ontology |
| `PRM-BUS-002` | `Emotional Journey / Peak-End` | `design_business` | SFL must preserve memorability and signal-density concerns as metrics and runtime effects, not flatten them into vague content-quality labels |

### 3.4 SFL Governance Constraints

| Constraint | Origin | Implementation Mechanism |
|---|---|---|
| Anti-Centroid Law preservation | PRD-08 + SFL doctrine | Family definitions must include anti-bloat guidance and maximum active-profile expectations; no registry design may imply “use all functions” behavior |
| ADR-05 primitive traceability | Existing primitive protocol | All primitive-linked SFL crosswalks must reference real primitive IDs verified in repository YAMLs |
| Role-before-Schema Rule | SDA taxonomy + SFL doctrine | Artifact validator rejects any object whose file path, artifact class, and semantic role disagree |
| No-Flat-120 Rule | SFL prompt + SFL doctrine | Compression-rule artifacts are mandatory; 120 raw associations cannot be loaded as canonical primary records |
| Function-vs-Metric Separation Rule | SFL doctrine | Validator rejects metrics stored as function definitions and rejects functions stored as metric entries |
| SFL Subordinate-to-SDA Rule | PRD-08 + SFL doctrine | SFL records cannot declare existential invariants, representation geometries, or directional-integrity ownership fields reserved for SDA |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Store SFL under a dedicated `sfl/` root rather than `primitives/` or `sda/` | Preserves ownership separation and makes reload/versioning predictable | Add SFL families under `primitives/meaning/` | Would violate PRD-08 primitive boundary and confuse transformation operators with perceptual modulation |
| Canonicalize families and definitions, not all 120 terms | Keeps substrate stable and maintainable | 120 flat rows | Too synonym-heavy, role-mixed, and unstable for canonical ownership |
| Treat `false depth` and `over-optimization` as failure classes, not functions | Matches doctrine and avoids rewarding corrupted outputs | Store them as negative functions | Blurs runtime composition with adversarial evaluation assets |
| Make crosswalks first-class maintained artifacts | Prevents drift between primitives, geometries, archetypes, and surfaces | Compute all crosswalks heuristically at runtime | Too unstable for foundational behavior and too opaque for auditability |
| Use targeted reload with rollback | Matches FR-ERA3-20 and avoids full warm for small doctrine edits | Force full rebuild on every artifact change | Slower, noisier, and weaker for operator workflows |
| Require family compression rules as canonical artifacts | Prevents uncontrolled synonym spread | Leave clustering implicit in code | Encourages hidden logic and later taxonomy drift |

---

## 4. Implementation Plan

### Phase 1 - Storage Root and Manifest Contract

- [ ] Create `sfl/registry_manifest.yaml`
- [ ] Create `sfl/families/` canonical directory
- [ ] Create `sfl/functions/` canonical directory
- [ ] Create `sfl/compression_rules/` canonical directory
- [ ] Create `sfl/crosswalks/primitive_to_function_family/` canonical directory
- [ ] Create `sfl/crosswalks/representation_geometry_to_function_profile/` canonical directory
- [ ] Create `sfl/crosswalks/archetype_to_function_profile/` canonical directory
- [ ] Create `sfl/crosswalks/surface_to_constraint_profile/` canonical directory

### Phase 2 - Typed Model Layer

- [ ] Create `src/ccp/models/sfl_registry_models.py`
- [ ] Define typed record models for families, definitions, compression rules, and crosswalk bundles
- [ ] Define typed health, issue, and reload-result models
- [ ] Define enums for artifact class, family kind, function polarity, and surface kind

### Phase 3 - Registry Validation and Warm Service

- [ ] Create `src/ccp/services/sfl_registry_service.py`
- [ ] Implement manifest loader
- [ ] Implement allowed-path resolution
- [ ] Implement family compression-rule validation
- [ ] Implement function-vs-metric-vs-policy rejection
- [ ] Implement primitive-ID verification against repository primitives
- [ ] Implement startup warm and registry health reporting
- [ ] Implement targeted artifact reload with previous-good-state rollback

### Phase 4 - Seed Canonical Fixtures

- [ ] Add initial `SFL-FAM-*` family fixtures for at least 8 families
- [ ] Add initial `SFL-FN-*` function definition fixtures for at least 12 functions
- [ ] Add initial `SFL-CR-*` compression-rule fixtures mapping raw terms to families
- [ ] Add initial `SFL-XW-PF-*` primitive crosswalk fixture(s)
- [ ] Add initial `SFL-XW-RG-*` representation geometry crosswalk fixture(s)
- [ ] Add initial `SFL-XW-AR-*` archetype-profile crosswalk fixture(s)
- [ ] Add initial `SFL-XW-SF-*` surface-constraint fixture(s)

### Phase 5 - Tests and Safety Gates

- [ ] Create `tests/integration/test_era3_fr25_sfl_registry.py`
- [ ] Create `tests/integration/test_era3_fr25_sfl_crosswalks.py`
- [ ] Add tests for false function-class violations
- [ ] Add tests for flat-120 rejection
- [ ] Add tests for primitive-ID reference integrity
- [ ] Add tests for reload rollback behavior

---

## 5. Primary Output Schema

```python
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class SFLArtifactClass(str, Enum):
    CANONICAL_FUNCTION_FAMILY = "canonical_function_family"
    FUNCTION_DEFINITION = "function_definition"
    COMPRESSION_RULE = "compression_rule"
    CROSSWALK = "crosswalk"


class FunctionPolarity(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    DUAL_USE = "dual_use"


class SurfaceKind(str, Enum):
    TELEGRAM = "telegram"
    CAROUSEL = "carousel"
    SHORT_FORM_VIDEO = "short_form_video"
    LONG_FORM_VIDEO = "long_form_video"
    WEBINAR = "webinar"
    COMMERCIAL = "commercial"
    AUDIT = "audit"


class FamilyKind(str, Enum):
    FRAMING_AND_CONTRAST = "framing_and_contrast"
    REPETITION_AND_IMPRINT = "repetition_and_imprint"
    SYMBOLIC_COMPRESSION = "symbolic_compression"
    SUGGESTIVE_GUIDANCE = "suggestive_guidance"
    ATMOSPHERE_AND_FIELD_SHAPING = "atmosphere_and_field_shaping"
    IDENTITY_SIGNALING = "identity_signaling"
    EMOTIONAL_PRIMING = "emotional_priming"
    NARRATIVE_TENSION_PRESERVATION = "narrative_tension_preservation"
    TRUST_AND_PROOF_REINFORCEMENT = "trust_and_proof_reinforcement"
    MEMETIC_AND_RECALL_HOOKS = "memetic_and_recall_hooks"
    PERCEPTUAL_THRESHOLD_MODULATION = "perceptual_threshold_modulation"
    ADAPTIVE_AMBIGUITY_AND_PARADOX = "adaptive_ambiguity_and_paradox"


class SourceDocumentRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=3)
    note: str = Field(min_length=3)


class FunctionEffectRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    effect_key: str = Field(pattern=r"^[a-z0-9_]+$")
    description: str = Field(min_length=3)


class ConstraintRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constraint_key: str = Field(pattern=r"^[a-z0-9_]+$")
    description: str = Field(min_length=3)


class PrimitiveLinkRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primitive_id: str = Field(pattern=r"^(EXP|PRM)-[A-Z]{3}-\d{3}$")
    rationale: str = Field(min_length=3)


class GeometryLinkRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    geometry_id: str = Field(pattern=r"^SDA-(RPG|ARG)-\d{3}$")
    rationale: str = Field(min_length=3)


class ArchetypeLinkRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    archetype_name: str = Field(min_length=3)
    rationale: str = Field(min_length=3)


class AssociationAliasRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_term: str = Field(min_length=2)
    normalization_note: str = Field(min_length=3)


class FunctionBoundaryRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed_when: str = Field(min_length=3)
    disallowed_when: str = Field(min_length=3)
    downgrade_behavior: str = Field(min_length=3)


class SubliminalFunctionFamilyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    artifact_class: Literal["canonical_function_family"] = "canonical_function_family"
    canonical_name: str = Field(min_length=3)
    family_kind: FamilyKind
    definition: str = Field(min_length=20)
    purpose: str = Field(min_length=20)
    positive_space_role: str = Field(min_length=20)
    negative_space_boundary: str = Field(min_length=20)
    anti_bloat_guidance: str = Field(min_length=20)
    related_raw_terms: list[AssociationAliasRef] = Field(min_length=1)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class SubliminalFunctionDefinitionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-FN-\d{3}$")
    artifact_class: Literal["function_definition"] = "function_definition"
    canonical_name: str = Field(min_length=3)
    family_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    polarity: FunctionPolarity
    definition: str = Field(min_length=20)
    positive_operation: str = Field(min_length=20)
    negative_operation: str = Field(min_length=20)
    intended_effects: list[FunctionEffectRef] = Field(min_length=1)
    alignment_rules: list[FunctionBoundaryRule] = Field(min_length=1)
    primitive_links: list[PrimitiveLinkRef] = Field(default_factory=list)
    geometry_links: list[GeometryLinkRef] = Field(default_factory=list)
    archetype_links: list[ArchetypeLinkRef] = Field(default_factory=list)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class FunctionFamilyCompressionRuleRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-CR-\d{3}$")
    artifact_class: Literal["compression_rule"] = "compression_rule"
    canonical_family_id: str = Field(pattern=r"^SFL-FAM-\d{3}$")
    raw_terms: list[AssociationAliasRef] = Field(min_length=1)
    compression_rationale: str = Field(min_length=20)
    duplicate_rejection_terms: list[str] = Field(default_factory=list)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class PrimitiveToFunctionFamilyCrosswalkRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-PF-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    primitive_links: list[PrimitiveLinkRef] = Field(min_length=1)
    target_family_ids: list[str] = Field(min_length=1)
    mapping_rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class RepresentationGeometryToFunctionProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-RG-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    geometry_links: list[GeometryLinkRef] = Field(min_length=1)
    preferred_function_ids: list[str] = Field(min_length=1)
    discouraged_function_ids: list[str] = Field(default_factory=list)
    mapping_rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class ArchetypeToFunctionProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-AR-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    archetype_links: list[ArchetypeLinkRef] = Field(min_length=1)
    preferred_function_ids: list[str] = Field(min_length=1)
    required_family_ids: list[str] = Field(default_factory=list)
    discouraged_family_ids: list[str] = Field(default_factory=list)
    mapping_rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class SurfaceConstraintProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(pattern=r"^SFL-XW-SF-\d{3}$")
    artifact_class: Literal["crosswalk"] = "crosswalk"
    surface: SurfaceKind
    preferred_family_ids: list[str] = Field(default_factory=list)
    discouraged_family_ids: list[str] = Field(default_factory=list)
    hard_constraints: list[ConstraintRef] = Field(default_factory=list)
    rationale: str = Field(min_length=20)
    source_documents: list[SourceDocumentRef] = Field(min_length=1)


class SFLManifestExpectedCounts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    families: int = Field(ge=1)
    functions: int = Field(ge=1)
    compression_rules: int = Field(ge=1)
    primitive_to_function_family_crosswalks: int = Field(ge=0)
    representation_geometry_crosswalks: int = Field(ge=0)
    archetype_profile_crosswalks: int = Field(ge=0)
    surface_constraint_profiles: int = Field(ge=0)


class SFLRegistryManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = Field(min_length=1)
    artifact_root: str = Field(min_length=1)
    family_path: str = Field(min_length=1)
    function_path: str = Field(min_length=1)
    compression_rule_path: str = Field(min_length=1)
    crosswalk_paths: list[str] = Field(min_length=1)
    expected_counts: SFLManifestExpectedCounts


class SFLRegistryIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error_code: str = Field(min_length=3)
    artifact_path: str = Field(min_length=3)
    artifact_id: str | None = None
    message: str = Field(min_length=3)
    severity: Literal["warning", "error"]


class SFLRegistryAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ready: bool
    family_count: int = Field(ge=0)
    function_count: int = Field(ge=0)
    compression_rule_count: int = Field(ge=0)
    primitive_to_function_family_crosswalk_count: int = Field(ge=0)
    representation_geometry_crosswalk_count: int = Field(ge=0)
    archetype_profile_crosswalk_count: int = Field(ge=0)
    surface_constraint_profile_count: int = Field(ge=0)
    issues: list[SFLRegistryIssue] = Field(default_factory=list)


class SFLArtifactReloadResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_path: str = Field(min_length=3)
    success: bool
    error_code: str | None = None
    message: str = Field(min_length=3)
    report: SFLRegistryAuditReport
```

### Schema Notes

- `SubliminalFunctionFamilyRecord` is the highest-level canonical clustering object.
- `SubliminalFunctionDefinitionRecord` is the callable canonical function unit.
- Metrics such as `cognitive_imprint_score` and `symbolic_density_score` are intentionally **not** stored here as canonical records. They belong to `FR-ERA3-27`.
- Failure objects such as `FalseDepthContrastCase` and `DeadPolishContrastCase` are intentionally **not** stored here as canonical records. They belong to `FR-ERA3-28`.
- `artifact_class` is deliberately narrow to prevent role leakage.

---

## 6. Backward Compatibility Fallback

If the SFL registry service is unavailable:

1. downstream runtime services must **not** invent function families heuristically
2. the system should degrade to:
   - primitive-only + SDA-only runtime compilation
   - explicit `SFL_UNAVAILABLE` advisory state
   - no perceptual function-stack injection
3. any service that requires canonical SFL evidence for pass/fail enforcement must fail closed into:
   - operator review
   - or downgrade path

This should follow the same operational logic used by `circuit_breaker.py`-style failure containment:

- isolate the unavailable subsystem
- preserve previous good state if present
- emit machine-readable reason codes
- avoid silent fallback into invented behavior

Allowed degraded behavior:

- render without SFL-specific modulation guidance
- mark output as `SFL_NOT_EVALUATED`

Rejected degraded behavior:

- guess function families from raw strings
- auto-promote arbitrary “subliminal” terms into runtime function definitions
- load partial canonical state and claim registry readiness

---

## 7. Tasks

- [ ] Create `sfl/registry_manifest.yaml`
- [ ] Create `sfl/families/` seed artifact directory
- [ ] Create `sfl/functions/` seed artifact directory
- [ ] Create `sfl/compression_rules/` seed artifact directory
- [ ] Create `sfl/crosswalks/primitive_to_function_family/`
- [ ] Create `sfl/crosswalks/representation_geometry_to_function_profile/`
- [ ] Create `sfl/crosswalks/archetype_to_function_profile/`
- [ ] Create `sfl/crosswalks/surface_to_constraint_profile/`
- [ ] Add `src/ccp/models/sfl_registry_models.py`
- [ ] Add `src/ccp/services/sfl_registry_service.py`
- [ ] Implement manifest loader and path contract validation
- [ ] Implement family compression-rule validator
- [ ] Implement flat-120 rejection logic
- [ ] Implement function-vs-metric separation checks
- [ ] Implement SFL-vs-SDA ownership separation checks
- [ ] Implement primitive-ID reference verification using existing primitive registry substrate
- [ ] Implement targeted artifact reload with rollback
- [ ] Create `tests/integration/test_era3_fr25_sfl_registry.py`
- [ ] Create `tests/integration/test_era3_fr25_sfl_crosswalks.py`
- [ ] Seed canonical family, function, compression-rule, and crosswalk fixture files

---

## 8. Acceptance Criteria

### AC-25.1 - Canonical family and function warm succeeds

**Given** a valid `sfl/` root with manifest, family artifacts, function artifacts, compression rules, and crosswalk bundles  
**When** `SFLRegistryService.warm()` runs at startup  
**Then** the registry reports `ready=True`, expected counts match, and all canonical artifact classes are loaded into memory

- Constraint enforced: `Role-before-Schema Rule`, `SFL Subordinate-to-SDA Rule`
- Failure example: startup warm passes while `functions/` contains metric-like records or while crosswalk counts do not match manifest counts
- Measurable pass condition: warm completes with `issues == []` and count parity for every manifest class

### AC-25.2 - Flat-120 designs are rejected

**Given** a directory of raw “120 subliminal associations” entries stored as independent canonical artifacts  
**When** the validator warms the SFL registry  
**Then** the registry rejects the artifact set with a `FLAT_120_VIOLATION` or equivalent error and `ready=False`

- Constraint enforced: `No-Flat-120 Rule`
- Failure example: the system loads `framing`, `mental framing`, `resonance`, `emotional resonance`, `symbolism`, and `symbol` as six unrelated canonical rows with no compression-rule discipline
- Measurable pass condition: any uncompressed raw-term bundle causes deterministic rejection during warm

### AC-25.3 - Metrics cannot masquerade as functions

**Given** an artifact under `sfl/functions/` that declares a runtime metric such as `cognitive_imprint_score` as if it were a canonical function definition  
**When** the validator loads the artifact  
**Then** the registry rejects it as a function-vs-metric separation violation

- Constraint enforced: `Function-vs-Metric Separation Rule`
- Failure example: `SFL-FN-019` defines `symbolic_density_score` with no operation semantics and is still accepted into the registry
- Measurable pass condition: the warm audit report contains a machine-readable error code and `function_count` excludes the invalid artifact

### AC-25.4 - Primitive references must trace to real repository IDs

**Given** a primitive crosswalk artifact references nonexistent IDs or hallucinated prefixes  
**When** the validator checks `PrimitiveToFunctionFamilyCrosswalkRecord` entries  
**Then** the registry rejects the crosswalk and preserves `ready=False` until corrected

- Constraint enforced: `ADR-05 primitive traceability`
- Failure example: a crosswalk references `EXP-TRB-001` or `PRM-XYZ-999` and still loads successfully
- Measurable pass condition: every primitive-linked crosswalk reference resolves against repository primitives before `ready=True`

### AC-25.5 - SFL cannot take SDA ontology ownership

**Given** an SFL function or family artifact attempts to declare existential invariant, representation geometry, or directional-integrity ownership fields reserved for SDA  
**When** the validator loads the artifact  
**Then** the artifact is rejected as an ownership boundary violation

- Constraint enforced: `SFL Subordinate-to-SDA Rule`
- Failure example: a function definition directly stores `invariant_gravity`, `representation_geometry_type`, or `directional_integrity_policy` as native canonical fields
- Measurable pass condition: any SDA-owned field on an SFL canonical artifact triggers deterministic rejection

### AC-25.6 - Targeted reload preserves previous good state

**Given** the registry is warm and a single family or function artifact is edited  
**When** `reload_artifact()` is called on that path  
**Then** the service reloads only the target artifact, updates in-memory state if valid, and restores the previous snapshot if the edited artifact is invalid

- Constraint enforced: deterministic reload safety
- Failure example: one bad `SFL-FN-*` edit corrupts the whole in-memory registry or causes partial mixed state
- Measurable pass condition: successful reload changes only targeted artifact state; failed reload returns `success=False` and preserves prior good object values

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md` | Reads / interop | Real primitive ID verification and crosswalk referential integrity |
| `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Structural sibling | Artifact-class discipline, manifest/reload patterns, and SDA ownership separation |
| `src/ccp/core/receipt_chain.py` | Core runtime | Receipt emission for warm, rejection, reload, and rollback |
| `PRD_02_CCF_Content_Factory.md` | Source PRD | Runtime insertion point and future packet expectations |
| `PRD_08_Conscious_Primitives.md` | Source PRD | Primitive ownership boundary and anti-centroid law framing |

### External

| API/Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed model definitions and validation |
| `PyYAML` | Current repo standard | YAML artifact loading |
| `pytest` | Current repo standard | Integration and unit test execution |

---

## 10. Testing Strategy

### Unit Tests

Create `tests/unit/test_era3_fr25_sfl_registry_models.py` with at least:

- `test_family_record_rejects_empty_related_raw_terms`
- `test_function_definition_rejects_missing_family_id`
- `test_compression_rule_rejects_empty_raw_term_list`
- `test_surface_constraint_profile_requires_known_surface_kind`

### Integration Tests

Create:

- `tests/integration/test_era3_fr25_sfl_registry.py`
- `tests/integration/test_era3_fr25_sfl_crosswalks.py`

Model these on:

- `tests/integration/test_era3_fr20_sda_registry.py`
- `tests/integration/test_era3_fr06_primitive_registry.py`

Required integration test cases:

1. `TestManifestBoot.test_ac251_warm_loads_all_required_sfl_classes`
2. `TestArtifactClassGuards.test_flat_120_rows_are_rejected`
3. `TestArtifactClassGuards.test_metric_payload_in_functions_dir_is_rejected`
4. `TestArtifactClassGuards.test_sda_owned_fields_on_sfl_artifact_are_rejected`
5. `TestCrosswalkIntegrity.test_primitive_crosswalk_rejects_unknown_primitive_id`
6. `TestReloadBehavior.test_single_artifact_reload_updates_only_target`
7. `TestReloadBehavior.test_failed_reload_preserves_previous_good_state`

### Manual Verification

1. Add a valid `SFL-FAM-*` family artifact and confirm startup warm reports it in count totals.
2. Add a valid `SFL-FN-*` function artifact that maps to a known family and confirm targeted reload updates only that function.
3. Add a fake raw-term artifact set representing uncompressed 120-word canonization and confirm warm fails with a flat-120 violation.
4. Add an invalid function definition that contains a metric-only field such as `cognitive_imprint_score` and confirm rejection.
5. Add a primitive crosswalk using `EXP-TRB-001` and confirm the registry rejects it.
6. Add an SFL function record that claims an SDA-native field and confirm rejection.
7. Corrupt one valid function record after successful warm and confirm `reload_artifact()` returns failure while preserving previous-good state.

### Exit Criteria

- registry warm succeeds on clean fixtures
- all artifact-class guard tests pass
- all crosswalk integrity tests pass
- rollback behavior is verified
- no primitive, SDA, or evaluator ownership leakage exists in canonical SFL artifacts

