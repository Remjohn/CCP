# Spec Prompt: FR-ERA3-49A — Seminar Speaking Score Card And Badge Runtime

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-49A
SPEC_TITLE:      Seminar Speaking Score Card And Badge Runtime
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-05 (CBCS Law28)
MAPPED_STORIES:  SSS card definition, badge progression tiers, Elite Seminar Master state, module rehearsal and live event scoring triggers, visible coach progression
CBAR_MANDATES:   Bridge-Existing-Systems Rule, Visible-Progression Rule, Elite-Seminar-Master Rule
BACKEND_REL:     NEW bridge spec — MUST integrate with existing ScoreCard system (FR-ERA3-ScoreCard, FR-ERA3-35C), existing badge logic, and existing trait scoring engine
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-49A_Seminar_Speaking_Score_Card_And_Badge_Runtime_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a bridge spec. The scorecard and badge systems already exist. This spec defines a new **card type** (SSS) and a new **badge progression** for long-form delivery competence.
>
> The Seminar Speaking Score (SSS) tracks a coach's progression across module families. It updates after module rehearsal, recorded runs, and live events. The final progression state is `Elite Seminar Master`.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-ScoreCard_Score_Card_Viewer_Tech_Spec.md`
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRD: `PRD-05`. **PROOF:** Quote lines on coach progression and mastery levels.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to badge levels up to Elite Seminar Master and the speaking program execution telemetry.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the SSS concept (Roadmap §4.2 W5A), the Elite Seminar Master progression, and the +$9.99 upsell context.
5. Existing FR-ERA3-35C spec: read fully. **PROOF:** Quote existing eval card and badge schemas.
6. Existing ScoreCard Viewer spec: read P3_S19 or equivalent. **PROOF:** Quote score card display patterns.
7. Existing backend: read `src/ccp/services/trait_scoring_engine.py` or equivalent and badge/progression model files. **PROOF:** Quote real method signatures.
7. Existing test patterns: read 1 `tests/integration/` file covering scoring or badge behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=6) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 SSS contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `SeminarSpeakingScore` — composite SSS score with module family breakdown
  - `SSSCardInstance` — an individual coach's SSS card state
  - `SSSBadgeProgression` — tier definitions and rules (Beginner → Developing → Proficient → Advanced → Expert → Elite Seminar Master)
  - `SSSUpdateEvent` — event payload for score updates triggered by rehearsal, recording, or live event
  - `ModuleFamilyScore` — per-family score (authority family, objection family, hope family, humor family, etc.)
- Define update triggers: module rehearsal → recorded runs → live events → scorecard update → badge progression
- Define visible progression states and unlock conditions for each tier
- Define how SSS cards appear on the shareable audit board

**REJECTION:** No SSS card schema | no badge progression tiers | no Elite Seminar Master state | ignores existing scorecard system | no update event schema | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
