# Spec Prompt: FR-ERA3-35C Update — Eval Card System for Living Commentary And SSS

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-35C
SPEC_TITLE:      Update Eval Card System for Living Commentary And SSS
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02, PRD-05
MAPPED_STORIES:  Living Commentary eval card types, Seminar Speaking Score card integration, delivery module eval cards, Elite Seminar Master badge progression
CBAR_MANDATES:   Eval-Card-Preserves-Ownership Rule, SSS-Progression-Visibility Rule
BACKEND_REL:     UPDATE existing eval card system — MUST add Living Commentary eval card types and Seminar Speaking Score (SSS) card integration
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update extends the eval card system with new card types for Living Commentary quality evaluation and the Seminar Speaking Score (SSS) progression system.
>
> The SSS card tracks a coach's long-form delivery competence across module families and updates after rehearsal, recorded runs, and live events. The progression includes visible level states up to `Elite Seminar Master`.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion and Complete Editing Session mandate)
> - `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-05`. **PROOF:** Quote lines on coach progression and eval card expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote details about the SSS (Seminar Speaking Score) progression and trigger loop integration.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the SSS card concept and Elite Seminar Master progression from the Roadmap (§4.2, §5 Wave C).
5. Existing FR-ERA3-35C spec: read fully. **PROOF:** Quote the existing eval card schema and shareable board logic.
6. Existing backend: read eval card model files and audit board code. **PROOF:** Quote real method signatures.
6. Existing test patterns: read 1 `tests/integration/` file covering eval card behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=6) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Eval card contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `LivingCommentaryEvalCard` — eval card type for judging Living Commentary output quality (motion grammar adherence, sound discipline, primitive expression, delivery presence)
  - `SeminarSpeakingScoreCard` — the SSS card tracking long-form delivery competence across module families
  - `DeliveryModuleEvalCard` — card type for evaluating individual delivery module performance (authority, hope, objection, etc.)
  - `EliteSeminarMasterBadgeProgression` — badge tiers and progression rules leading to Elite Seminar Master
- Define SSS update triggers: module rehearsal → recorded runs → live events → scorecard update → badge progression
- Define how SSS cards appear on the shareable audit board

**REJECTION:** No SSS card schema | no Living Commentary eval card | no badge progression tiers | no delivery module eval card | no shareable board integration | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
