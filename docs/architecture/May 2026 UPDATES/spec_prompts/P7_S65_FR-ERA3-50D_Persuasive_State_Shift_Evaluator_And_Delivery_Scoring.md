# Spec Prompt: FR-ERA3-50D — Persuasive State Shift Evaluator And Delivery Scoring

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-50D
SPEC_TITLE:      Persuasive State Shift Evaluator And Delivery Scoring
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02, PRD-05
MAPPED_STORIES:  Module selection quality scoring, delivery coherence evaluation, primitive congruence checks, pathos/logos/ethos balance, anti-slop integrity, speaking and webinar delivery scorecards
CBAR_MANDATES:   Evaluator-Separate-From-Registry Rule, Score-Effect-Not-Vanity Rule, Anti-Slop-Integrity Rule
BACKEND_REL:     NEW evaluator — MUST integrate with existing eval scoring taxonomy (FR-ERA3-35A/B), Perceptual Influence Evaluator (FR-ERA3-27), and existing trait scoring engine without duplicating their ownership
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-50D_Persuasive_State_Shift_Evaluator_And_Delivery_Scoring_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This evaluator judges whether communication modules actually produced persuasive state movement — not just shallow engagement metrics. It scores whether the audience experienced recognition, trust, curiosity, hope, relief, conviction, and readiness.
>
> It is a **separate scoring layer** from the module library (FR-ERA3-50A) and the recipe library (FR-ERA3-50C). It consumes their outputs and judges them.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (9+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-05`. **PROOF:** Quote lines on content quality and delivery evaluation.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to delivery coherence and state shifts evaluation inside the Complete Editing Session.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the evaluator section (Roadmap §4.2–4.3 evaluators subsection) and the persuasive delivery modules section (Source of Truth §7.3).
5. Existing eval taxonomy: read FR-ERA3-35A/B specs. **PROOF:** Quote scoring schemas.
6. Existing perceptual evaluator: read FR-ERA3-27 spec. **PROOF:** Quote how perceptual influence is currently scored.
7. Existing backend: read `src/ccp/services/trait_scoring_engine.py` or equivalent. **PROOF:** Quote real method signatures.
7. Existing test patterns: read 1 `tests/integration/` file covering scoring or evaluation.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=7) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Evaluator contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `PersuasiveStateShiftScore` — composite score measuring: recognition, trust, curiosity, hope, relief, conviction, readiness
  - `DeliveryCoherenceReport` — whether the delivery matched the module intent
  - `ModuleSelectionQualityScore` — whether the right module was selected for the context
  - `SpeakingDeliveryScorecard` — aggregated short-form delivery scores
  - `WebinarDeliveryScorecard` — aggregated long-form delivery scores
- Scoring dimensions must include:
  - selection quality, delivery coherence, primitive congruence, pathos/logos/ethos balance, objection weakening success, future-picture vividness, pressure vs safety balance, anti-slop integrity
- Must integrate with but not duplicate: FR-ERA3-35A/B eval taxonomy, FR-ERA3-27 perceptual evaluator

**REJECTION:** Duplicates eval taxonomy ownership | no delivery coherence scoring | no anti-slop check | no distinction between short-form and long-form scorecards | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
