# Spec Prompt: FR-ERA3-49 — Transformational Webinar Program And Module Compiler

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-49
SPEC_TITLE:      Transformational Webinar Program And Module Compiler
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-07 (V2WS Webinar), PRD-05 (CBCS Law28)
MAPPED_STORIES:  Webinar program instance, module compilation pipeline, delivery rehearsal, weekly live-event preparation, long-form editing upsell lane (+$9.99), V2WS as module compiler and mastery system
CBAR_MANDATES:   Live-Is-North-Star Rule, Module-Compiler-Not-Deck-Maker Rule, Brownfield-Integration Rule, Absorbs-FR-ERA3-49B Rule
BACKEND_REL:     NEW program runtime — MUST use the Complete Editing Session payload. MUST integrate with existing V2WS webinar companion (FR-ERA3-01), existing Loom studio block (FR-CA11-16), Excalidraw workspace (FR-CA11-10), Communication Module Library (FR-ERA3-50A), and SSS card (FR-ERA3-49A). All recorded rehearsals and edited vertical webinars are compiled via the Remotion Node.js backend.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-49_Transformational_Webinar_Program_And_Module_Compiler_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a NEW spec, but brownfield-first on top of V2WS services, webinar briefing, Excalidraw, Loom, and module adjusters.
>
> This spec **absorbs FR-ERA3-49B** (Long Form Delivery Edit And Refinement Upsell). FR-ERA3-49B does NOT become a standalone spec. Its +$9.99 upsell lane is defined as a subsection within this spec.
>
> Key doctrine corrections:
> - V2WS is now a module-writing system, module compiler, rehearsal/refinement surface, and delivery-mastery system
> - Live and streaming = north star. Recorded webinars = 1-3 month fluency-building lane
> - Coaches should reason through modules as communication tools, not memorize scripts
> - Weekly cadence: at least 1 live long-form selling event per week once ready
>
> **COMPLETE EDITING SESSION & REMOTION PIPELINE:**
> All webinar projects, drafts, rehearsals, and edited replays are managed within the Complete Editing Session state wrapper. Rehearsal streams, recordings, and CTA video elements are compiled using the Remotion Node.js rendering backend.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion and Complete Editing Session mandate)
> - `docs/architecture/april_updates/FR-ERA3-01_Webinar_Companion_Tech_Spec.md`
> - `docs/prd/modules/PRD_07_V2WS_Webinar.md` (PRD Module)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)
> - `docs/architecture/FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` (Studio Block)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-07`, `PRD-05`. **PROOF:** Quote lines on V2WS purpose and CBCS delivery mastery.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote the Complete Editing Session wrapper and Remotion backend rendering mandates for webinar assets.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the W5 workflow (Roadmap §4.1), the two-program split (§2.6), the live-is-north-star doctrine (§2.3), and the +$9.99 upsell (§4.1 W5B).
5. Existing webinar companion: read FR-ERA3-01 spec. **PROOF:** Quote webinar session schemas.
6. Existing V2WS code: read `src/ccp/services/v2ws_interactive_service.py`, `src/ccp/services/session_to_course.py` or equivalents. **PROOF:** Quote real method signatures.
7. Existing studio block: read FR-CA11-16 spec for Loom recording mode.
8. Existing test patterns: read 1 `tests/integration/` file covering webinar or V2WS behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 350 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Program and compiler contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `WebinarProgramInstance` — coach-local program state, enrolled modules, current webinar projects, cadence config
  - `WebinarModuleDraft` — a single module draft (topic, communication module mapping, offer/angle, persuasion architecture)
  - `ModuleCompilationPipeline` — stage sequence: topic discovery → offer brainstorm → module writing → persuasion architecture build → delivery rehearsal → recording or live → editing → packaging → distribution → telemetry → follow-up → SSS update
  - `DeliveryRehearsalSession` — rehearsal config, recording mode (Loom teleprompted or live), scoring hooks
  - `WeeklyLiveEventPreparation` — preparation checklist, module readiness check, audience state input
- Define the +$9.99 long-form editing upsell lane:
  - `LongFormEditingUpsellConfig` — cleanup, noise removal, visual enrichment, pacing refinement, replay-ready edit
- Define how V2WS exports its strongest persuasion modules into the Persuasive Speaking Program
- Define the Duarte `what is / what could be` engine as a structural pattern for webinar architecture

**REJECTION:** Treats webinar as deck-making tool | no module compilation pipeline | no live-event preparation | no +$9.99 upsell lane | no SSS integration | ignores existing V2WS code | no delivery rehearsal schema | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
