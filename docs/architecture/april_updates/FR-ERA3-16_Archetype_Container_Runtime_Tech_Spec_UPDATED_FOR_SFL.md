# Tech-Spec: FR-ERA3-16 (SFL Update) — Archetype Container Runtime for SFL
**Created:** 2026-05-19
**Status:** Ready for Development
**Version:** 2.0 (ERA3 — SFL Runtime Integration)
**Phase:** 6 — SFL Runtime Integration
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
**Base Spec:** `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` v1.0

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. §2 requires extending existing backend. §3 requires explicit backend mapping. §4 requires 10-section format. CBAR note requires named mandate enforcement.
2. PRD-02 LOADED:     Exact runtime law: "signal -> coach reaction -> primitive coalition -> archetype container -> JIT script contract -> render blueprint". §3.4I structural invariants. Updated compiler law adds SDA field, geometry bind, function stack, and depth profile between coalition and archetype container.
3. PRD-08 LOADED:     §3.6: "primitives are not the deepest ontology." §6.1 biological hierarchy: "SFL and downstream composition logic determine how that force is felt." Stack: "truth substrate -> primitive candidate field -> coalition -> edge product -> delivery stack -> variation stack -> validation -> destination packet". DSPy dual-role doctrine: "DSPy is both a runtime orchestration substrate and an optimization substrate."
4. SFL CORE LOADED:   lab/subliminal_function_layer_for_ccp_v_1.md. Central law: "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness." §6.7 required crosswalks: Primitive-to-SubliminalFunctionFamily, RepresentationGeometry-to-SubliminalFunctionProfile, Archetype-to-FunctionStackProfile, Surface-to-FunctionConstraintProfile.
5. PHASE0 EVAL LOADED: lab/phase0_eval_card_scoring_model_v_1.md. Visible score set: Humanity, Presence, Trust, Memorability, Resonance, Signal, AI Slop Risk. SFL delivery mechanics affect all seven perceptual scores.
6. BIO MODEL LOADED:  lab/ccp_biological_orchestration_model_v_1.md. Runtime organism: "DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation". RNA includes SubliminalFunctionStackPacket, CompositionDepthPacket, VariationProfile. §9.4: "DSPy is both a runtime orchestration substrate and an optimization substrate. It should never again be described as only outside runtime."
7. SDA ENGINE LOADED: lab/semantic_discernment_architecture_content_engine_v_1.md. Deceptively close failure, existential invariants, directional integrity. SDA truth decisions remain upstream of archetype.
8. SDA TAXONOMY LOADED: lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md. Role-before-schema, no false registry, canonical/derived separation.
9. FR-ERA3-16 v1 LOADED: Existing archetype container runtime spec. ArchetypeContainerRuntimeService.compile() accepts CoachResponseCapturePacket + CoalitionInputs + mood_context + evidence_bundle. Returns CCFRoutingRecommendation with ArchetypeContainerManifest or ActionableRejectionPayload. 6 archetype choices. No SFL consumption exists.
10. FR-ERA3-20 LOADED: SDA ontology and registry. ExistentialInvariantRecord, RepresentationGeometryRecord, ArchetypalGeometryRecord. Canonical SDA substrate.
11. FR-ERA3-21 LOADED: SDA query and crosswalk service. SDAQueryAndCrosswalkService provides resolve_archetype_to_geometry() and query surfaces.
12. FR-ERA3-25 LOADED: SFL library and taxonomy. SubliminalFunctionFamilyRecord, SubliminalFunctionDefinitionRecord, SFLRegistryService, ArchetypeToFunctionProfileRecord, SurfaceConstraintProfileRecord. 12 FamilyKind values.
13. BACKEND LOADED:    src/ccp/services/archetype_container_runtime.py — ArchetypeContainerRuntimeService.__init__(supabase_client, receipt_chain, research_synthesis, psych_routing). compile(capture, coalition, mood_context, evidence_bundle) -> CCFRoutingRecommendation.
14. MODELS LOADED:     src/ccp/models/archetype_container_runtime_models.py — RuntimeStatus, SimilarityBand, ArchetypeChoice, SentenceAuditRecord, CoalitionInputs, CoachResponseCapturePacket, ContainerIntensityProfile, ArchetypeContainerManifest, ActionableRejectionPayload, CCFRoutingRecommendation.
15. TESTS LOADED:      tests/integration/test_frera316_archetype_runtime_compile.py and test_frera316_actionable_rejection_loop.py. Scenario-based, AC-named classes, deterministic assertions.
16. BIO DOCTRINE:      Runtime DSPy lives inside RNA/transcription and nervous-system/delivery layers. "JIT-created should usually mean dynamically assembled, typed, and at least partially executable." Skill contracts: doctrine -> schema -> executable implementation.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S53_FR-ERA3-16_Update_Archetype_Container_Runtime_for_SFL.md` | Update prompt, SFL consumption mandate |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory spec format |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Runtime law, archetype placement, SDA packet dependencies |
| 4 | `docs/prd/modules/PRD_08_Conscious_Primitives.md` | Primitive/SFL separation, biological hierarchy, DSPy dual-role |
| 5 | `lab/subliminal_function_layer_for_ccp_v_1.md` | SFL doctrine, function families, crosswalk requirements |
| 6 | `lab/phase0_eval_card_scoring_model_v_1.md` | Perceptual scoring model |
| 7 | `lab/ccp_biological_orchestration_model_v_1.md` | Runtime organism, DNA/RNA/force/delivery/variation chain |
| 8 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | SDA truth layer |
| 9 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | SDA artifact taxonomy |
| 10 | `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` | Base spec being updated |
| 11 | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | SDA canonical registry |
| 12 | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | SDA query surfaces |
| 13 | `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | SFL registry, families, crosswalks |
| 14 | `src/ccp/services/archetype_container_runtime.py` | Existing runtime implementation |
| 15 | `src/ccp/models/archetype_container_runtime_models.py` | Existing Pydantic models |
| 16 | `tests/integration/test_frera316_archetype_runtime_compile.py` | Existing compile test patterns |
| 17 | `tests/integration/test_frera316_actionable_rejection_loop.py` | Existing rejection test patterns |

---

## 2. Overview

### 2.1 Problem Statement

FR-ERA3-16 v1.0 established the archetype container runtime with six deterministic jobs: validate, evidence-check, anti-centroid, reject, select, and route. That spec is correct and remains the structural foundation.

However, the archetype container runtime does not yet consume the SFL delivery layer. Without this update:

- the archetype container emits `ArchetypeContainerManifest` with `cmf_render_hints` and `intensity_profile` but no perceptual function-stack binding, meaning CMF receives a psychological container with no delivery intelligence
- composition depth profiles (`RepetitionWithVariation`, `LayeredInterpretation`, `RhythmicStructure`, `StrategicAmbiguity`) have no binding point, so downstream rendering cannot distinguish rhythmic from layered from ambiguous delivery
- the biological organism chain (`truth -> force -> delivery -> variation -> phenotype`) breaks at the force-to-delivery handoff because the archetype container only preserves force decisions and skips delivery shaping
- variation profiles have no archetype-level anchor, so mathematical variation cannot be tuned per-container
- runtime DSPy has no typed execution contract inside the archetype runtime, leaving skill orchestration as prose-only rather than executable

### 2.2 Solution

This update spec extends the existing `ArchetypeContainerRuntimeService` and `ArchetypeContainerManifest` to consume three new SFL-era packets:

1. **`SubliminalFunctionStackPacket`** — the selected perceptual function stack for this container
2. **`CompositionDepthPacket`** — the composition depth profile governing cross-medium delivery
3. **`VariationProfileBinding`** — the variation-layer anchor for mathematical aliveness

It also introduces:

4. **`ArchetypeSflExecutionContract`** — the typed DSPy-compatible execution contract binding archetype + SFL + composition + variation into a single executable skill unit
5. **`ArchetypeVariationDecision`** — the explicit variation-layer decision record

The archetype container remains a structural container, not a style blob. SFL packets are consumed as delivery directives, not absorbed into the container's identity.

### 2.3 Scope

**In scope:**

- new Pydantic models for SFL consumption packets
- extension of `ArchetypeContainerManifest` with SFL binding fields
- extension of `ArchetypeContainerRuntimeService.compile()` to accept and bind SFL inputs
- typed `ArchetypeSflExecutionContract` for runtime DSPy interoperability
- `ArchetypeVariationDecision` for variation-layer anchoring
- new Supabase columns for SFL binding persistence
- updated acceptance criteria and test coverage
- fallback behavior when SFL registry is unavailable

**Out of scope:**

- rewriting the base anti-centroid, evidence-gate, or selection-matrix logic (FR-ERA3-16 v1.0)
- implementing the SFL registry itself (FR-ERA3-25)
- implementing the SFL query service (FR-ERA3-26)
- implementing the perceptual influence evaluator (FR-ERA3-27)
- implementing the perceptual failure corpus (FR-ERA3-28)
- implementing downstream CMF rendering changes (FR-ERA3-12)

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Payload / Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-ACR-008 | `SubliminalFunctionStackPacket` | FR-ERA3-16 v2 | Selected perceptual function stack bound to this container |
| DEP-ACR-009 | `CompositionDepthPacket` | FR-ERA3-16 v2 | Cross-medium delivery depth profile |
| DEP-ACR-010 | `VariationProfileBinding` | FR-ERA3-16 v2 | Mathematical variation anchor for this container |
| DEP-ACR-011 | `ArchetypeSflExecutionContract` | FR-ERA3-16 v2 | Typed DSPy-compatible execution contract |
| DEP-ACR-012 | `ArchetypeVariationDecision` | FR-ERA3-16 v2 | Explicit variation-layer decision record |

Existing DEP-ACR-001 through DEP-ACR-007 from v1.0 remain unchanged.

### 3.2 Existing Backend Integration

| File | Path | How This Update Uses It |
|---|---|---|
| `archetype_container_runtime.py` | `src/ccp/services/archetype_container_runtime.py` | Extended with SFL consumption in `compile()`. New optional params: `sfl_function_stack`, `composition_depth`, `variation_profile`. |
| `archetype_container_runtime_models.py` | `src/ccp/models/archetype_container_runtime_models.py` | Extended with five new models. `ArchetypeContainerManifest` gains SFL binding fields. |
| `sfl_registry_models.py` | `src/ccp/models/sfl_registry_models.py` | Consumed read-only. `SubliminalFunctionFamilyRecord`, `SubliminalFunctionDefinitionRecord`, `ArchetypeToFunctionProfileRecord` used for crosswalk resolution. |
| `sfl_registry_service.py` | `src/ccp/services/sfl_registry_service.py` | Queried for archetype-to-function-profile crosswalks and surface constraints. |
| `sda_query_service.py` | `src/ccp/services/sda_query_service.py` | Queried for archetype-to-geometry resolution to inform SFL profile selection. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Extended receipt entries for SFL bind, variation bind, and execution contract assembly. |

### 3.3 Runtime Packets and Profiles

| Packet | Biological Layer | What It Carries |
|---|---|---|
| `SubliminalFunctionStackPacket` | Nervous/Delivery | Ordered list of active SFL function IDs, family bindings, polarity, and per-function weight |
| `CompositionDepthPacket` | Nervous/Delivery | Active composition depth class (repetition_with_variation, layered_interpretation, rhythmic_structure, strategic_ambiguity), intensity, and cross-surface applicability |
| `VariationProfileBinding` | Variation | Asymmetry target, resonance spacing, predictability break threshold, paradox retention flag |
| `ArchetypeSflExecutionContract` | RNA/Transcription | Typed skill contract binding archetype invariants + SFL stack + depth profile + variation into executable DSPy signature |
| `ArchetypeVariationDecision` | Variation | Explicit record of which variation axes were applied and why |

### 3.4 SFL Runtime Integration Constraints

| Constraint | Origin | Enforcement in This Spec |
|---|---|---|
| SFL Subordinate-to-SDA Rule | PRD-08 + SFL doctrine | SFL packets consumed after SDA truth decisions. Archetype container never overrides SDA invariant or geometry with SFL preferences. |
| No-Flat-120 Rule | SFL doctrine | Function stacks reference canonical family IDs from FR-ERA3-25, never raw association terms. |
| Runtime-Function-Stack Rule | SFL doctrine + Bio model | Function stack is bound at archetype container time, not invented at render time. |
| Composition-Depth Binding Rule | Bio model §7 | Composition depth profile is bound to the container, not left as a downstream guess. |
| Variation-Before-Render Rule | Bio model §8 | Variation decisions are made at container time and passed to render, not applied post-render. |
| Typed-Skill-Execution Rule | Bio model §10.1 | Execution contracts are typed DSPy-compatible signatures, not prose-only instructions. |

### 3.5 Technical Decisions

| Decision | Rationale | Consequence |
|---|---|---|
| SFL inputs are optional on `compile()` | Backward compatibility with v1.0 callers. SFL registry may be unavailable. | When absent, container emits `sfl_binding_status=SFL_NOT_BOUND`. |
| Function stack is bound, not generated | Archetype runtime is a compiler boundary, not a creative engine. | SFL function selection must happen upstream or via crosswalk resolution. |
| Composition depth is one of four canonical classes | Bio model §7 defines exactly four. | No open-ended depth profiles. |
| Variation profile is anchored, not executed | Archetype runtime anchors variation decisions; render executes them. | Container carries variation metadata; CMF applies it. |
| Execution contract uses typed DSPy signature shape | Bio model §9.4 requires runtime DSPy. | Contract can be consumed by DSPy modules without parsing prose. |
| SFL binding does not affect anti-centroid or rejection logic | SFL is delivery, not truth or force. | Rejection thresholds remain unchanged from v1.0. |

---

## 4. Implementation Plan

### Phase 1 — Model Extensions (Tasks 1–4)

1. Add `SubliminalFunctionStackPacket` to `archetype_container_runtime_models.py`.
2. Add `CompositionDepthPacket` to `archetype_container_runtime_models.py`.
3. Add `VariationProfileBinding` and `ArchetypeVariationDecision` to `archetype_container_runtime_models.py`.
4. Add `ArchetypeSflExecutionContract` to `archetype_container_runtime_models.py`.

### Phase 2 — Manifest Extension (Tasks 5–7)

5. Extend `ArchetypeContainerManifest` with `sfl_function_stack`, `composition_depth`, `variation_binding`, `sfl_binding_status`, and `execution_contract` fields.
6. Extend `CCFRoutingRecommendation` with `sfl_binding_status` field.
7. Add `SflBindingStatus` enum.

### Phase 3 — Service Extension (Tasks 8–12)

8. Extend `ArchetypeContainerRuntimeService.__init__()` with optional `sfl_registry` and `sda_query` dependencies.
9. Add `SflCrosswalkResolver` that resolves archetype-to-function-profile crosswalks from FR-ERA3-25.
10. Add `CompositionDepthResolver` that selects depth class from archetype + mood + intensity.
11. Add `VariationAnchorBuilder` that creates variation binding from archetype + SFL + composition.
12. Extend `compile()` to accept optional SFL, composition, and variation inputs and bind them into the manifest.

### Phase 4 — Execution Contract Assembly (Tasks 13–15)

13. Add `ExecutionContractAssembler` that builds typed `ArchetypeSflExecutionContract` from manifest + SFL stack + depth + variation.
14. Define the DSPy-compatible signature shape as typed fields, not prose.
15. Add receipt-chain entries for SFL bind, variation bind, and execution contract assembly.

### Phase 5 — Persistence and Fallback (Tasks 16–18)

16. Add `sfl_function_stack_json`, `composition_depth_json`, `variation_binding_json` columns to `archetype_container_manifests` table.
17. Add `archetype_sfl_execution_contracts` Supabase table.
18. Implement fallback: when SFL unavailable, emit `SFL_NOT_BOUND` and continue with v1.0 behavior.

### Phase 6 — Testing (Tasks 19–22)

19. Add unit tests for SFL crosswalk resolution, depth selection, and variation anchoring.
20. Add integration tests for SFL-bound compile, SFL-absent fallback, and execution contract shape.
21. Update existing compile and rejection tests to confirm SFL absence does not break v1.0 behavior.
22. Add non-regression test confirming SFL does not affect anti-centroid thresholds.

---

## 5. Schema

### 5.1 New Models — add to `src/ccp/models/archetype_container_runtime_models.py`

```python
# ── New enums ──

class SflBindingStatus(str, Enum):
    SFL_BOUND = "sfl_bound"
    SFL_NOT_BOUND = "sfl_not_bound"
    SFL_PARTIAL = "sfl_partial"
    SFL_UNAVAILABLE = "sfl_unavailable"


class CompositionDepthClass(str, Enum):
    REPETITION_WITH_VARIATION = "repetition_with_variation"
    LAYERED_INTERPRETATION = "layered_interpretation"
    RHYTHMIC_STRUCTURE = "rhythmic_structure"
    STRATEGIC_AMBIGUITY = "strategic_ambiguity"


# ── New packet models ──

class SflFunctionBinding(BaseModel):
    function_id: str = Field(min_length=1, pattern=r"^SFL-FN-\d{3}$")
    family_id: str = Field(min_length=1, pattern=r"^SFL-FAM-\d{3}$")
    canonical_name: str = Field(min_length=1)
    polarity: str = Field(min_length=1)
    weight: float = Field(ge=0.0, le=1.0)
    binding_rationale: str = Field(min_length=1)


class SubliminalFunctionStackPacket(BaseModel):
    stack_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    active_functions: list[SflFunctionBinding] = Field(min_length=1, max_length=8)
    crosswalk_source_id: str = Field(min_length=1)
    total_weight: float = Field(ge=0.0, le=1.0)
    binding_surface: str = Field(min_length=1)
    anti_bloat_check_passed: bool = True


class CompositionDepthPacket(BaseModel):
    depth_id: str = Field(min_length=1)
    depth_class: CompositionDepthClass
    intensity: float = Field(ge=0.0, le=1.0)
    cross_surface_applicable: bool = True
    governing_rationale: str = Field(min_length=1)


class VariationProfileBinding(BaseModel):
    variation_id: str = Field(min_length=1)
    asymmetry_target: float = Field(ge=0.0, le=1.0)
    resonance_spacing: float = Field(ge=0.0, le=1.0)
    predictability_break_threshold: float = Field(ge=0.0, le=1.0)
    paradox_retention: bool = False
    variation_rationale: str = Field(min_length=1)


class ArchetypeVariationDecision(BaseModel):
    decision_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    applied_axes: list[str] = Field(min_length=1)
    variation_binding: VariationProfileBinding
    depth_class_influence: CompositionDepthClass
    decision_rationale: str = Field(min_length=1)


class ArchetypeSflExecutionContract(BaseModel):
    contract_id: str = Field(min_length=1)
    runtime_session_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    structural_invariants: list[str] = Field(min_length=1)
    anti_draft_profile: list[str] = Field(min_length=1)
    sfl_function_stack: SubliminalFunctionStackPacket
    composition_depth: CompositionDepthPacket
    variation_binding: VariationProfileBinding
    intensity_profile: ContainerIntensityProfile
    coalition_family_mix: list[str] = Field(min_length=1)
    authorized_render_targets: list[str] = Field(min_length=1)
    dspy_signature_fields: dict[str, str] = Field(min_length=1)
    skill_execution_mode: str = Field(default="typed_dspy_module")
```

### 5.2 Extended `ArchetypeContainerManifest` — new optional fields

```python
# Add to existing ArchetypeContainerManifest:
    sfl_function_stack: SubliminalFunctionStackPacket | None = None
    composition_depth: CompositionDepthPacket | None = None
    variation_binding: VariationProfileBinding | None = None
    variation_decision: ArchetypeVariationDecision | None = None
    execution_contract: ArchetypeSflExecutionContract | None = None
    sfl_binding_status: SflBindingStatus = SflBindingStatus.SFL_NOT_BOUND
```

### 5.3 Extended `CCFRoutingRecommendation` — new field

```python
# Add to existing CCFRoutingRecommendation:
    sfl_binding_status: SflBindingStatus = SflBindingStatus.SFL_NOT_BOUND
```

### 5.4 New Supabase DDL

```sql
ALTER TABLE archetype_container_manifests
    ADD COLUMN IF NOT EXISTS sfl_function_stack_json JSONB,
    ADD COLUMN IF NOT EXISTS composition_depth_json JSONB,
    ADD COLUMN IF NOT EXISTS variation_binding_json JSONB,
    ADD COLUMN IF NOT EXISTS sfl_binding_status TEXT NOT NULL DEFAULT 'sfl_not_bound';

CREATE TABLE IF NOT EXISTS archetype_sfl_execution_contracts (
    contract_id              TEXT PRIMARY KEY,
    runtime_session_id       TEXT NOT NULL,
    archetype_choice         TEXT NOT NULL,
    contract_json            JSONB NOT NULL,
    sfl_binding_status       TEXT NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 5.5 Extended Compile Request

```json
{
  "coach_response_capture": { "..." },
  "coalition_inputs": { "..." },
  "mood_context": { "..." },
  "evidence_bundle": { "..." },
  "sfl_function_stack": {
    "stack_id": "SFL-STK-001",
    "archetype_choice": "ARC-MYTH-DEBUNK",
    "active_functions": [
      {
        "function_id": "SFL-FN-001",
        "family_id": "SFL-FAM-001",
        "canonical_name": "Contrast Framing",
        "polarity": "positive",
        "weight": 0.4,
        "binding_rationale": "High-contrast stance demands perceptual opposition framing"
      },
      {
        "function_id": "SFL-FN-007",
        "family_id": "SFL-FAM-003",
        "canonical_name": "Symbolic Compression",
        "polarity": "positive",
        "weight": 0.35,
        "binding_rationale": "Myth debunk requires compressed symbolic payload"
      }
    ],
    "crosswalk_source_id": "SFL-XW-AR-001",
    "total_weight": 0.75,
    "binding_surface": "short_form_video",
    "anti_bloat_check_passed": true
  },
  "composition_depth": {
    "depth_id": "CDP-001",
    "depth_class": "rhythmic_structure",
    "intensity": 0.7,
    "cross_surface_applicable": true,
    "governing_rationale": "High-contrast myth debunk benefits from rhythmic acceleration"
  },
  "variation_profile": {
    "variation_id": "VAR-001",
    "asymmetry_target": 0.6,
    "resonance_spacing": 0.4,
    "predictability_break_threshold": 0.3,
    "paradox_retention": false,
    "variation_rationale": "Myth debunk should feel asymmetric but not paradoxical"
  }
}
```

---

## 6. Backward Compatibility Fallback

All v1.0 behavior is preserved unchanged. SFL-related inputs are additive and optional.

### 6.1 SFL Registry Unavailable

If `SFLRegistryService` is not warm or unreachable:

- `compile()` continues with v1.0 logic
- `sfl_binding_status = SFL_UNAVAILABLE` on the manifest and recommendation
- no function stack, composition depth, or variation binding is emitted
- CMF receives the v1.0 manifest shape and operates without SFL delivery guidance
- receipt chain logs `sfl_bind_skipped` with reason `registry_unavailable`

### 6.2 SFL Inputs Absent from Request

If the caller does not supply `sfl_function_stack`, `composition_depth`, or `variation_profile`:

- `sfl_binding_status = SFL_NOT_BOUND`
- the archetype container is fully valid without SFL
- downstream systems must treat absent SFL as "operate without perceptual modulation guidance" not "invent SFL heuristically"

### 6.3 Partial SFL Binding

If only some SFL inputs are provided (e.g. function stack but no variation):

- `sfl_binding_status = SFL_PARTIAL`
- present packets are bound; absent packets are `None`
- execution contract is NOT assembled (requires all three inputs)
- receipt chain logs which packets were present and which were absent

### 6.4 SFL Does Not Affect Rejection Thresholds

Anti-centroid rejection remains at `similarity_score >= 0.75`. SFL binding status has no influence on whether a take is accepted or rejected. SFL is delivery, not truth or force.

### 6.5 Existing v1.0 Tests Must Continue Passing

All existing integration tests (`test_frera316_archetype_runtime_compile.py`, `test_frera316_actionable_rejection_loop.py`) must pass without modification. New SFL parameters default to `None`.

---

## 7. Tasks

### Model Extension

- [ ] Add `SflBindingStatus` enum to `archetype_container_runtime_models.py`
- [ ] Add `CompositionDepthClass` enum to `archetype_container_runtime_models.py`
- [ ] Add `SflFunctionBinding` model
- [ ] Add `SubliminalFunctionStackPacket` model
- [ ] Add `CompositionDepthPacket` model
- [ ] Add `VariationProfileBinding` model
- [ ] Add `ArchetypeVariationDecision` model
- [ ] Add `ArchetypeSflExecutionContract` model

### Manifest Extension

- [ ] Extend `ArchetypeContainerManifest` with SFL optional fields
- [ ] Extend `CCFRoutingRecommendation` with `sfl_binding_status`

### Service Extension

- [ ] Extend `ArchetypeContainerRuntimeService.__init__()` with optional `sfl_registry` and `sda_query`
- [ ] Add `SflCrosswalkResolver` for archetype-to-function-profile resolution
- [ ] Add `CompositionDepthResolver` for depth class selection
- [ ] Add `VariationAnchorBuilder` for variation binding creation
- [ ] Extend `compile()` with optional SFL, composition, and variation params
- [ ] Add `ExecutionContractAssembler` for typed DSPy contract assembly

### Persistence

- [ ] Add SFL columns to `archetype_container_manifests` table
- [ ] Add `archetype_sfl_execution_contracts` table
- [ ] Extend manifest persistence to include SFL JSON

### Receipt Chain

- [ ] Add receipt entries for `sfl_bind`, `composition_bind`, `variation_bind`, `execution_contract_assembled`, `sfl_bind_skipped`

### Testing

- [ ] Add unit tests for SFL crosswalk resolution
- [ ] Add unit tests for composition depth selection
- [ ] Add unit tests for variation anchoring
- [ ] Add integration tests for SFL-bound compile
- [ ] Add integration tests for SFL-absent fallback
- [ ] Add non-regression test confirming SFL does not affect anti-centroid
- [ ] Update existing tests to confirm backward compatibility

---

## 8. Acceptance Criteria

### AC-SFL-1 — SFL-bound compile emits function stack and composition depth on manifest

**Given** a valid compile request with `sfl_function_stack`, `composition_depth`, and `variation_profile` all provided,
**When** the runtime compiles successfully,
**Then** `ArchetypeContainerManifest.sfl_function_stack` is populated with the bound function stack,
**And** `ArchetypeContainerManifest.composition_depth` is populated with the depth profile,
**And** `ArchetypeContainerManifest.variation_binding` is populated,
**And** `sfl_binding_status == SFL_BOUND`,
**And** function IDs in the stack reference canonical `SFL-FN-*` IDs from FR-ERA3-25.

**FAILURE EXAMPLE:** The runtime accepts raw association terms like "framing" or "symbolic compression" as function identifiers instead of canonical `SFL-FN-001` IDs. That violates the No-Flat-120 Rule and makes downstream resolution impossible.

**Constraint:** No-Flat-120 Rule, Runtime-Function-Stack Rule.

### AC-SFL-2 — Execution contract is typed and DSPy-compatible

**Given** a successful SFL-bound compile with all three delivery-layer inputs,
**When** `ExecutionContractAssembler` builds the contract,
**Then** `ArchetypeSflExecutionContract` includes `dspy_signature_fields` as a typed dictionary mapping field names to types,
**And** `skill_execution_mode == "typed_dspy_module"`,
**And** the contract includes structural invariants, anti-draft profile, SFL stack, depth, and variation in typed fields.

**FAILURE EXAMPLE:** The execution contract contains a prose string like "use framing and symbolic compression with rhythmic pacing" instead of typed fields. That violates the Typed-Skill-Execution Rule and cannot be consumed by DSPy modules.

**Constraint:** Typed-Skill-Execution Rule, Bio model §9.4.

### AC-SFL-3 — SFL absence does not break v1.0 compile

**Given** a valid compile request with NO SFL inputs (v1.0 shape),
**When** the runtime compiles,
**Then** the result matches v1.0 behavior exactly,
**And** `sfl_binding_status == SFL_NOT_BOUND`,
**And** `sfl_function_stack`, `composition_depth`, `variation_binding`, and `execution_contract` are all `None`,
**And** all existing v1.0 acceptance criteria (AC1–AC6) continue to pass.

**FAILURE EXAMPLE:** The runtime crashes or returns a validation error because `sfl_function_stack` is required. That breaks backward compatibility with all existing callers.

**Constraint:** Backward compatibility mandate.

### AC-SFL-4 — SFL does not affect anti-centroid rejection thresholds

**Given** a transcript with generic consensus sentences that triggers anti-centroid rejection,
**When** the compile request includes a valid SFL function stack,
**Then** the runtime still rejects with `status=rejected_actionable`,
**And** the rejection threshold remains `similarity_score >= 0.75`,
**And** SFL inputs are ignored in the rejection payload.

**FAILURE EXAMPLE:** The runtime accepts a generic transcript because the SFL function stack "sounds strong enough" to compensate. That violates the truth-before-delivery law: SDA decides truth, SFL decides delivery. Delivery cannot override truth failure.

**Constraint:** SFL Subordinate-to-SDA Rule.

### AC-SFL-5 — Composition depth is one of four canonical classes

**Given** a compile request with `composition_depth`,
**When** the depth class is validated,
**Then** it must be one of: `repetition_with_variation`, `layered_interpretation`, `rhythmic_structure`, `strategic_ambiguity`,
**And** any other value is rejected with a validation error.

**FAILURE EXAMPLE:** A caller sends `depth_class: "creative_flow"` and the system accepts it. That creates open-ended depth profiles outside the canonical four, violating Bio model §7.

**Constraint:** Composition-Depth Binding Rule.

### AC-SFL-6 — Variation decisions are anchored at container time

**Given** a successful SFL-bound compile,
**When** `ArchetypeVariationDecision` is emitted,
**Then** it includes explicit `applied_axes`, the `variation_binding` reference, and `decision_rationale`,
**And** downstream CMF receives the variation anchor rather than inventing variation post-render.

**FAILURE EXAMPLE:** The container emits no variation decision and CMF applies random asymmetry because "it looked better." That violates the Variation-Before-Render Rule and makes variation non-deterministic and non-auditable.

**Constraint:** Variation-Before-Render Rule.

---

## 9. Dependencies

### Internal Services

| Dependency | Type | Use |
|---|---|---|
| `FR-ERA3-16 v1.0` | Base spec | All existing runtime logic preserved |
| `FR-ERA3-25 SFL Library` | Read dependency | Canonical function families, definitions, crosswalks |
| `FR-ERA3-26 SFL Query Service` | Optional runtime dependency | Function-stack resolution if not provided by caller |
| `FR-ERA3-20 SDA Ontology` | Read dependency | Archetype-to-geometry crosswalk for SFL profile selection |
| `FR-ERA3-21 SDA Query` | Optional runtime dependency | Geometry resolution for crosswalk-informed SFL binding |
| `FR-ERA3-27 Perceptual Evaluator` | Downstream consumer | Evaluates SFL-bound manifests for perceptual quality |
| `ReceiptChain` | Existing core | Extended with SFL-specific receipt entries |
| `ResearchSynthesisProtocol` | Existing service | Unchanged from v1.0 |
| `PsychVariableMatrix` | Existing service | Unchanged from v1.0 |

### Internal Models

| Dependency | Type | Use |
|---|---|---|
| `sfl_registry_models.py` | Read-only consumption | `SubliminalFunctionDefinitionRecord`, `ArchetypeToFunctionProfileRecord` |
| `sda_registry_models.py` | Read-only consumption | `ArchetypalGeometryRecord` for crosswalk resolution |
| `archetype_container_runtime_models.py` | Extended | Five new models, two extended models |
| Supabase | Existing infra | Extended tables |

### External

| Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed model definitions |
| `dspy` | Current | Execution contract signature compatibility |

---

## 10. Testing Strategy

### 10.1 Unit Tests

#### `test_frera316_sfl_crosswalk_resolver.py`

- `test_archetype_myth_debunk_resolves_framing_and_contrast_family`
- `test_crosswalk_source_id_references_canonical_sfl_xw_ar_id`
- `test_unknown_archetype_returns_empty_resolution`

#### `test_frera316_composition_depth_resolver.py`

- `test_high_intensity_myth_debunk_selects_rhythmic_structure`
- `test_reflective_witness_selects_strategic_ambiguity`
- `test_invalid_depth_class_rejected`

#### `test_frera316_variation_anchor_builder.py`

- `test_variation_binding_includes_all_required_axes`
- `test_paradox_retention_false_by_default`
- `test_variation_rationale_is_not_empty`

#### `test_frera316_execution_contract_assembler.py`

- `test_contract_includes_dspy_signature_fields`
- `test_contract_skill_execution_mode_is_typed_dspy_module`
- `test_contract_requires_all_three_sfl_inputs`
- `test_contract_preserves_structural_invariants`

### 10.2 Integration Tests

#### `tests/integration/test_frera316_sfl_bound_compile.py`

Scenario class: `TestACSFL1SflBoundCompile`

- Build valid capture + coalition + mood + evidence + SFL stack + composition + variation.
- Assert `status == compiled`.
- Assert `sfl_binding_status == SFL_BOUND`.
- Assert `container_manifest.sfl_function_stack` is populated.
- Assert `container_manifest.composition_depth.depth_class` is one of four canonical classes.
- Assert `container_manifest.execution_contract.dspy_signature_fields` is non-empty dict.

Scenario class: `TestACSFL3SflAbsentFallback`

- Build valid capture + coalition (v1.0 shape, no SFL inputs).
- Assert `status == compiled`.
- Assert `sfl_binding_status == SFL_NOT_BOUND`.
- Assert `sfl_function_stack is None`.
- Assert `execution_contract is None`.
- Assert all v1.0 manifest fields are present and valid.

Scenario class: `TestACSFL4SflDoesNotAffectRejection`

- Build transcript with generic consensus + valid SFL stack.
- Assert `status == rejected_actionable`.
- Assert `rejection_payload.similarity_score >= 0.75`.
- Assert SFL inputs are not referenced in rejection payload.

#### `tests/integration/test_frera316_sfl_execution_contract.py`

Scenario class: `TestACSFL2ExecutionContract`

- Build full SFL-bound compile.
- Assert `execution_contract.contract_id` is non-empty.
- Assert `execution_contract.dspy_signature_fields` maps field names to type strings.
- Assert `execution_contract.skill_execution_mode == "typed_dspy_module"`.
- Assert `execution_contract.sfl_function_stack.active_functions` length > 0.

Scenario class: `TestACSFL5DepthClassValidation`

- Attempt compile with invalid `depth_class`.
- Assert validation error.
- Attempt compile with each of the four canonical classes.
- Assert all four succeed.

### 10.3 Non-Regression Expectations

- No existing v1.0 test may break when SFL parameters are absent.
- No test may accept raw association terms as function IDs.
- No test may allow SFL binding to change rejection thresholds.
- No test may accept an execution contract without typed `dspy_signature_fields`.
- No test may accept a composition depth class outside the canonical four.
- No test may allow variation decisions to be invented downstream instead of anchored at container time.
