# Spec Prompt: FR-ERA3-48 — Persuasive Speaking Program Runtime And Telemetry

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-48
SPEC_TITLE:      Persuasive Speaking Program Runtime And Telemetry
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-05 (CBCS Law28), PRD-02 (CCF)
MAPPED_STORIES:  Coach-local speaking program instance, module-level scoring, daily drip cadence, delivery telemetry, short-form / long-form transfer scoring
CBAR_MANDATES:   Coach-Local-Ownership Rule, Module-Level-Scoring Rule, Brownfield-Integration Rule
BACKEND_REL:     NEW coach-local program runtime — MUST use the Complete Editing Session payload. MUST integrate with existing CBCS Four-Engine Runtime (FR-ERA3-18), existing scorecard system (FR-ERA3-35B/35C), Voice Prompt Engine (FR-ERA3-17), and Four-Surface Async Skill Ladder (FR-ERA3-13). All generated prototype carousels are compiled via the Remotion Node.js + @remotion/skia backend.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-48_Persuasive_Speaking_Program_Runtime_And_Telemetry_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a NEW spec, but **brownfield-first** on top of existing CBCS, scorecards, voice prompts, and skill ladder systems.
>
> The program trains coaches to carry communication modules naturally. Its promise is: "we will make your voice more capable of creating trust, movement, conviction, and emotional clarity across content and live communication."
>
> Modules trained: hook, positioning, authority, proof/testimonials, identification, permission to be seen, commitment/micro-commitment, objection softening/smashing, hope, intrigue, transitions, close, humor, storytelling, contextual explanation.
>
> Cadence law: daily drip and repetition for short-form; at-will training for long-form transfer.
>
> **The 16-Minute Trigger-First Ingestion Loop:**
> 1. Ingest Coach DNA/Context.
> 2. Daily CRAL research discovers audience feelings.
> 3. Generate **Internal Prototype Carousels** & Voice Note (4+ images) as the *Daily Lesson*.
> 4. Coach reacts via Voice Note (Correction Mode: tonality, pacing, alignment).
> 5. Final Voice Note triggers the coach to record and upload the final `.mp4`.
>
> **COMPLETE EDITING SESSION & REMOTION INTEGRATION:**
> Every speaking practice session is encapsulated as a Complete Editing Session state wrapper to preserve transcription, correction voice notes, and prototype assets. The final uploaded `.mp4` and intermediate prototype carousels must be rendered via the Remotion Node.js backend using `@remotion/skia`.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (10+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion and Complete Editing Session mandate)
> - `docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec_UPDATED_FOR_SFL.md`
> - `docs/architecture/april_updates/FR-ERA3-17_Voice_Prompt_Engine_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-13_Four_Surface_Async_Skill_Ladder_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-05`. **PROOF:** Quote lines on CBCS coaching loops and content creation as practice surface.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote the Complete Editing Session wrapper and Remotion backend rendering mandates.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the two-program split (§2.2, §2.6 of the Roadmap), the W4 Delivery Module Mastery workflow, and the 8 operating laws.
5. Existing CBCS runtime: read FR-ERA3-18 spec. **PROOF:** Quote engine contracts and scoring patterns.
6. Existing skill ladder: read FR-ERA3-13 spec. **PROOF:** Quote skill progression schemas.
7. Existing backend references: read `src/ccp/services/trait_scoring_engine.py`, `src/ccp/services/voice_to_lesson.py` or equivalents. **PROOF:** Quote real method signatures.
7. Existing test patterns: read 2 `tests/integration/` files covering CBCS or scoring behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 350 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Program runtime contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `SpeakingProgramInstance` — coach-local program state, enrolled modules, cadence config
  - `ModulePracticeTask` — a single practice assignment (which module, what format, what constraints)
  - `DeliveryScoreRecord` — per-practice scoring result
  - `SpeakingTelemetryPacket` — telemetry for pause quality, transition strength, emotional modulation, story retention, humor landing, objection clarity, close integrity
  - `DailyDripSchedule` — cadence scheduler for daily module rotation
- Define the module inventory as skill contracts: hook, positioning, authority, proof stack, testimonial deployment, identification, permission to be seen, commitment, micro-commitment, objection softening, objection smashing, hope, intrigue, transition, story arc, humor relief, contextual explanation, close
- Define the **Trigger-First Ingestion Loop** schemas and state machine (Context → CRAL → Prototype Carousel + Voice Note → Ping-Pong Correction → `.mp4` Upload).
- Define how practice tasks produce content outputs (practice = content creation surface)
- Define short-form vs long-form transfer scoring

**REJECTION:** No daily drip schedule | no module-level scoring | no telemetry packets | ignores existing CBCS/scorecard/skill ladder systems | no short-form/long-form distinction | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
