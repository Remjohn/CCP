# Spec Prompt: FR-ERA3-50C — Communication Module Recipe Library And Delivery Patterns

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-50C
SPEC_TITLE:      Communication Module Recipe Library And Delivery Patterns
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-05 (CBCS Law28)
MAPPED_STORIES:  Reusable delivery recipes beneath fixed modules, objection/hope/proof/humor/transition/close pattern encoding, versioned callable sequences
CBAR_MANDATES:   Recipe-Below-Skill Rule, No-Top-Level-Promotion Rule, Consume-50A Rule
BACKEND_REL:     NEW recipe store — MUST consume Communication Module Library (FR-ERA3-50A) as its upstream skill contract authority
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-50C_Communication_Module_Recipe_Library_And_Delivery_Patterns_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> Recipes sit **beneath** fixed skills. They are reusable delivery patterns — callable and versioned — but they must NOT be promoted to top-level ontology. The module library (FR-ERA3-50A) owns the skill contracts. This spec owns the execution patterns.
>
> Example recipes: acknowledge/soften/validate/reframe/target, agree/redefine/prove/target, then-and-now positioning, authority through proxy, sympathy before challenge, future picture before ask, proof-before-claim.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (7 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-50A_Communication_Module_Library_And_Primitive_Crosswalk_Tech_Spec.md` (or the prompt)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)
> - `docs/prd/modules/PRD_08_Conscious_Primitives.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-05`, `PRD-08`. **PROOF:** Quote lines on coaching delivery patterns and primitives mapping.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to recipe execution and aliveness patterns inside editing sessions.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the recipe examples from Roadmap §4.2–4.3 (recipes and playbooks section).
5. FR-ERA3-50A: read the spec or prompt. **PROOF:** Quote the module skill contract schema this spec must consume.
6. Existing backend: read CBCS model files and scoring patterns. **PROOF:** Quote real method signatures.
6. Existing test patterns: read 1 `tests/integration/` file covering CBCS or delivery behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=5) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Recipe contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `DeliveryRecipe` — id, name, parent_module_id, steps, variant_id, version
  - `RecipeStep` — step_index, instruction, expected_effect, anti_pattern
  - `RecipeVariant` — variant_id, recipe_id, context_label, modification_notes
- Define the initial recipe inventory:
  - Objection: acknowledge / soften / validate / reframe / target
  - Objection alt: agree / redefine / prove / target
  - Positioning: then-and-now
  - Authority: authority through proxy
  - Hope: sympathy before challenge
  - Commitment: future picture before ask
  - Proof: proof-before-claim
- Recipes must be versioned and callable
- Recipes must link to their parent fixed skill (from FR-ERA3-50A)

**REJECTION:** Recipes become top-level ontology | no versioning | no link to parent skill contracts | duplicates FR-ERA3-50A module definitions | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
