# Spec Prompt: FR39 Update — Pi Extension Harness for Semantic And Perceptual Extensions

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR39 (Pi Extension Harness)
SPEC_TITLE:      Update Pi Extension Harness for Semantic And Perceptual Extensions
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-08 (Conscious Primitives), PRD-02 (CCF)
MAPPED_STORIES:  SDA validation extension, primitive activation extension, SFL profile resolver extension, composition depth extension, variation profile extension
CBAR_MANDATES:   Update-Not-Replace Rule, Extension-Consumes-Not-Owns Rule
BACKEND_REL:     UPDATE existing Pi Extension Harness — MUST add semantic and perceptual extensions that consume FR-ERA3-06, FR-ERA3-20, FR-ERA3-25, FR-ERA3-27 without duplicating their ownership
OUTPUT_FILE:     docs/architecture/april_updates/FR39_Pi_Extension_Harness_Tech_Spec_UPDATED_FOR_SEMANTIC_PERCEPTUAL.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is the second Pi harness update. It folds `FR-ERA3-52` (Pi Semantic And Perceptual Extensions) into the existing harness.
>
> These extensions make the Pi pipeline semantically and perceptually aware by consuming existing registries and evaluators as extension stages.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (11 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `src/ccp/services/pi_extension_harness.py` (Local Code Reference)
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_08_Conscious_Primitives.md` (PRD Module)
> - `docs/architecture/april_updates/FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-08`, `PRD-02`. **PROOF:** Quote lines on primitive and semantic analysis pipeline expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote details about primitive activators and Perceptual Evaluators inside execution flows.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote Wave D FR-ERA3-52 purpose from Roadmap §5.
5. **Existing code — CRITICAL:** Read `src/ccp/services/pi_extension_harness.py`. **PROOF:** Quote real method signatures.
6. Existing FR-ERA3-06, FR-ERA3-20, FR-ERA3-25, FR-ERA3-27 specs. **PROOF:** Quote the service contracts each extension must consume.
6. Existing test patterns: read 1 `tests/integration/` file covering Pi harness or semantic validation.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=7) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Extension contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define extension stage schemas for:
  - `SDAValidationExtension` — validates content against SDA ontology constraints
  - `PrimitiveActivationExtension` — resolves primitive coalition for the pipeline context
  - `SFLProfileResolverExtension` — resolves SFL function profile for the content type
  - `CompositionDepthExtension` — applies composition depth profile to render plan
  - `VariationProfileExtension` — applies variation/aliveness profile
- Each extension must:
  - declare its dependency on upstream service (FR-ERA3-06/20/25/27)
  - define input/output contracts
  - never duplicate the upstream service's ownership
- Must reference existing `pi_extension_harness.py` extension patterns

**REJECTION:** Extensions duplicate registry ownership | no input/output contracts | no dependency declarations | treats as greenfield | no real code references | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
