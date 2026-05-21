# Spec Prompt: FR-ERA3-16 Update - Archetype Container Runtime for SFL

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-16
SPEC_TITLE:      Update Archetype Container Runtime for SFL
PHASE:           6 - SFL Runtime Integration
SOURCE_PRD:      PRD-02, PRD-08
MAPPED_STORIES:  SFL Wave 2 runtime propagation - function-stack consumption, composition depth profile binding, variation-aware archetype execution, runtime DSPy interoperability
CBAR_MANDATES:   SFL Subordinate-to-SDA Rule, No-Flat-120 Rule, Runtime-Function-Stack Rule, Composition-Depth Binding Rule, Variation-Before-Render Rule, Typed-Skill-Execution Rule
BACKEND_REL:     UPDATE existing archetype runtime - MUST consume FR-ERA3-25/26 artifacts and remain interoperable with FR-ERA3-20 SDA ontology, FR-ERA3-21 query surfaces, and FR-ERA3-27 evaluator outputs
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec_UPDATED_FOR_SFL.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is not a greenfield archetype spec. It is a revision spec.
>
> The purpose is to update the archetype container runtime so it can consume:
> - `SubliminalFunctionStackPacket`
> - `CompositionDepthPacket`
> - `VariationProfile`
> - SFL-aware runtime DSPy skill orchestration
>
> The archetype container must still preserve:
> - SDA truth and geometry decisions upstream
> - primitive coalition and edge-product ownership
> - downstream render independence
>
> Hard rule: archetypes remain structural containers, not giant style blobs.

> [!IMPORTANT]
> **MANDATORY SFL SOURCE SET - READ IN EVERY SFL INTEGRATION SPEC SESSION:**
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/semantic_discernment_architecture_content_engine_v_1.md`
> - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
> - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
> - `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md`

> [!WARNING]
> **TRACEABILITY NOTE:**
> There is no dedicated Phase 6 epic file yet. For this spec, use the SFL source set, the SFL note's Wave 2 integration section, and the affected PRD doctrine as the traceability base. In Section 3.4, use `SFL Runtime Integration Constraints` if no formal `PhaseX-M#` mandate exists.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` - §2 backend, §3 Pre-Flight, §4 Format
2. Source PRDs: `PRD-02`, `PRD-08`. **PROOF:** Quote the exact lines that establish archetype runtime placement, primitive/SFL separation, and truth -> force -> delivery -> variation placement.
3. SFL source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing FR specs: read `FR-ERA3-16`, `FR-ERA3-20`, `FR-ERA3-21`, and `FR-ERA3-25`. **PROOF:** Quote the specific runtime or packet claim from each.
5. Existing backend references: read real files for archetype runtime, routing, packet consumption, and DSPy/tool execution patterns. **PROOF:** Quote real method signatures.
6. Existing models: read packet / runtime / archetype / result models under `src/ccp/models/`.
7. Existing test patterns: read 2 `tests/integration/` files covering runtime orchestration or packetized services.
8. Existing biological/runtime doctrine: confirm how runtime DSPy should live inside the nervous/delivery layer rather than be treated as offline-only optimization.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=10) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Runtime packets / profiles | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**, not a greenfield replacement
- Define canonical runtime schemas for:
  - `SubliminalFunctionStackPacket`
  - `CompositionDepthPacket`
  - `VariationProfileBinding`
  - `ArchetypeSflExecutionContract`
  - `ArchetypeVariationDecision`
- Define exactly how the archetype container consumes:
  - coalition output
  - edge product
  - SFL function stack
  - composition depth profile
  - variation profile
- Preserve the law:
  - SDA decides truth
  - primitives decide force
  - SFL decides delivery mechanics
  - variation layer decides aliveness adjustments
- Make runtime DSPy explicit as executable orchestration substrate, not prose-only adjunct

**REJECTION:** archetype becomes a style soup | SFL duplicates primitive logic | no runtime packet contracts | no DSPy execution role | no failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
