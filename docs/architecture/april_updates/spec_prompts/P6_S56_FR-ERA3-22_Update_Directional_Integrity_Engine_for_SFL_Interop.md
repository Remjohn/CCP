# Spec Prompt: FR-ERA3-22 Update - Directional Integrity Engine for SFL Interop

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-22
SPEC_TITLE:      Update Directional Integrity Engine for SFL Interop
PHASE:           6 - SFL Runtime Integration
SOURCE_PRD:      PRD-01, PRD-02, PRD-08
MAPPED_STORIES:  SFL Wave 2 validator interop - integrate perceptual effects without collapsing DI into a style judge, preserve truth-vs-delivery boundary, expose joint reports cleanly
CBAR_MANDATES:   SFL Subordinate-to-SDA Rule, Truth-Vs-Delivery Boundary Rule, No-Style-Only-Pass Rule, Joint-Report-Without-Swallowing Rule
BACKEND_REL:     UPDATE existing DI engine - MUST interoperate with FR-ERA3-27 and FR-ERA3-28 while preserving DI ownership of truth/direction/hard-negative logic
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec_UPDATED_FOR_SFL_INTEROP.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is an interop update, not a replacement of directional integrity.
>
> The goal is to explain:
> - what DI continues to own
> - what the perceptual evaluator owns
> - how the two interact
> - how joint decision states are expressed without duplication
>
> Hard rule: SFL can never override semantic failure.

> [!IMPORTANT]
> **MANDATORY SFL SOURCE SET - READ IN EVERY SFL INTEGRATION SPEC SESSION:**
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
> - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
> - `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-28_Perceptual_Failure_Corpus_And_Contrast_Harness_Tech_Spec.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-01`, `PRD-02`, `PRD-08`. **PROOF:** Quote the exact lines that establish Anti-Slop, SDA, and primitive/SFL boundaries.
3. SFL source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing FR specs: read `FR-ERA3-22`, `FR-ERA3-27`, and `FR-ERA3-28`. **PROOF:** Quote the specific validator/failure ownership from each.
5. Existing backend references: read real files for DI, semantic guards, evaluator or report aggregation logic. **PROOF:** Quote real method signatures.
6. Existing models: read DI report, failure report, and evaluator result models.
7. Existing test patterns: read 2 `tests/integration/` files covering validator or guard behavior.
8. Existing biological/runtime doctrine: confirm truth/protection layers remain distinct from delivery/variation layers.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Report / interop contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `DirectionalIntegrityInteropReport`
  - `SemanticVsPerceptualDecisionState`
  - `PerceptualAttachmentSummary`
  - `JointFailureSurface`
- Explicitly define:
  - what DI owns
  - what SFL evaluator owns
  - how they compose
  - what happens when semantic pass + perceptual fail
  - what happens when semantic fail + perceptual pass
- Preserve hard precedence:
  - semantic failure blocks
  - perceptual failure can downgrade, route to review, or block where required

**REJECTION:** SFL overrides DI | no clean ownership split | no joint-report contract | no failure-state matrix | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
