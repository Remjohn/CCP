# Spec Prompt: FR-ERA3-16 Update — Archetype Container Runtime for Living Commentary Bundles

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-16
SPEC_TITLE:      Update Archetype Container Runtime for Living Commentary Bundles
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02, PRD-06
MAPPED_STORIES:  Living Commentary archetype mapping, weekly package template routing, delivery recipe resolution per archetype, MCDA-ranked archetype deployment order
CBAR_MANDATES:   Archetype-Realization Separation Rule, No-New-Archetype-Ontology Rule, Delivery-Recipe-Per-Archetype Rule
BACKEND_REL:     UPDATE existing Archetype Container Runtime — MUST use the Complete Editing Session payload. MUST add delivery recipe resolution and Living Commentary bundle routing per archetype without creating new archetype ontology. All output compositions are compiled via the Remotion Node.js + @remotion/skia backend.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update folds `FR-ERA3-62` (Living Commentary Archetype Mapping And Output Bundles) into the existing Archetype Container Runtime.
>
> The doctrine is: **keep the archetypes, change the realization grammar.** This spec does NOT create new archetypes. It adds delivery recipe resolution and Living Commentary output bundle routing to existing archetype containers.
>
> Hard rule: do NOT create a new archetype ontology.
>
> **COMPLETE EDITING SESSION & TRIGGER-FIRST LOOP CONTEXT:**
> The archetype container routing must output directly into the Complete Editing Session state wrapper. The weekly package template must align chronologically with the Trigger-First execution sequence (Carousel → 3 Voice Notes → Record) so that no visual assets or research context is lost.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (10+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec_UPDATED_FOR_SFL.md`
> - `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_06_Conscious_Reactions.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-06`. **PROOF:** Quote the lines that define archetype routing and content realization ownership.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote the Complete Editing Session wrapper and Remotion backend rendering mandates.
4. Living Commentary source set: both doctrine docs above. **PROOF:** Quote the MCDA ranked archetype table (Section 9.2) and the weekly package logic (Section 10).
5. Existing FR-ERA3-16 specs: read both original and SFL-updated versions. **PROOF:** Quote the archetype container schema and routing logic.
6. Existing FR-ERA3-35B/35C specs: read both. **PROOF:** Quote how benchmark profiles and eval cards attach to archetype outputs.
7. Existing backend references: read real archetype runtime service files. **PROOF:** Quote real method signatures.
8. Existing models: read archetype container model files and session models.
8. Existing test patterns: read 2 `tests/integration/` files covering archetype routing or container behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Delivery recipe contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec** extending the existing Archetype Container Runtime
- Define canonical schemas for:
  - `ArchetypeDeliveryRecipe` — which communication modules dominate a given archetype, what order they appear in, what emotional temperature they carry, what realization layer best fits
  - `WeeklyPackageTemplate` — 1 cinematic story + 2 animated explainers + 2 quote commentary + 1 comparison/reaction + 1 atmospheric = 7 pieces from one 45-60 min interview
  - `ArchetypeToLivingCommentaryMapping` — routes archetype containers to their preferred Living Commentary format families
  - `ArchetypeDeliveryRecipeCompiler` — resolves which modules dominate, what order, what emotional temperature, what realization layer
- Map the MCDA-ranked archetypes with their scores:
  - Comparison Breakdown (193), Challenger/Frame Breaker (191), Myth Debunk (188), Authority Proof Stack (186), Wrong Way/Right Way Contrast (184), Relief Peak (182), Persuasive Tweets (181), Ranked Take (179), Core Educator (176), Observational Humor (174), Transformation Story (171), Case Study Breakdown (168), Witness Story (165)
- Define the per-archetype delivery recipe behavior from Source of Truth §7.4:
  - Challenger: intrigue + authority + objection softening + reframe → sharper contrast, faster reveal, stronger first-frame tension
  - Authority Proof Stack: authority + proof + identification + future trust → real-world receipts, stable camera, less decorative motion
  - Witness Story: identification + story + permission to be seen + hope → slower drift, softer audio, wider space, fewer text interruptions
  - Comparison Breakdown: positioning + contrast + decision guidance + close-through-clarity → binary composition, object separation, check/cross coding
- Define the commercial ladder alignment: $29.99 = 7 videos, $39.99 = program access, $99.99 = program + 32 videos

**REJECTION:** Creates new archetype ontology | no delivery recipe schema | no weekly package template | no MCDA-ranked mapping | no per-archetype realization behavior | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
