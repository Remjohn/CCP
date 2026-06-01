# Spec Prompt: FR-ERA3-50F — Objection Intelligence And Response Compiler

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-50F
SPEC_TITLE:      Objection Intelligence And Response Compiler
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-07 (V2WS Webinar), PRD-05 (CBCS Law28)
MAPPED_STORIES:  Universal and offer-specific objection catalogs, objection softening and smashing flows, webinar/reaction/speaking/content routing, audience-state integration
CBAR_MANDATES:   Objection-Before-Close Rule, Audience-State-Aware Rule, Integrate-Existing-Systems Rule
BACKEND_REL:     NEW intelligence compiler — MUST tie into existing tribe profiles, webinar module adjustment, CRAL audience-state reasoning, and Telegram moderator bot objection capture (FR-ERA3-45)
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-50F_Objection_Intelligence_And_Response_Compiler_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec maintains objection catalogs and compiles objection handling flows. The key doctrine from the webinar and speaking materials: **objections should be weakened early, not treated as a last-minute rebuttal exercise.**
>
> Objection types: money, time, ability, trust, fear, confusion, conflict, timing.
>
> The compiler produces objection handling flows that route into: webinars, reactions, speaking practice, content generation.
>
> It consumes objections captured by the Telegram Webinar Moderator Bot (FR-ERA3-45) and enriches them with audience-state context from CRAL.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion and Complete Editing Session mandate)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)
> - `docs/prd/modules/PRD_07_V2WS_Webinar.md` (PRD Module)
> - `docs/architecture/april_updates/FR-ERA3-45_Telegram_Webinar_Moderator_Bot_Tech_Spec.md` (or prompt for it)
> - `src/ccp/services/` (scan for CRAL, audience-state, tribe profile files)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-07`, `PRD-05`. **PROOF:** Quote lines on objection handling and audience conversion.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote details about objection compiler structures and capture bot interactions in editing sessions.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the objection doctrine from Source of Truth §7.3 (objection work starts before the ask) and the objection recipes from Roadmap §4.2.
5. Existing CRAL/audience-state code: scan `src/ccp/services/` for CRAL, audience-state, tribe profile files. **PROOF:** Quote real method signatures.
6. Existing FR-ERA3-45 prompt: understand the Telegram Moderator Bot objection capture flow.
7. Existing test patterns: read 1 `tests/integration/` file covering CRAL or audience-state behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=5) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Objection intelligence contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `ObjectionCatalog` — universal + offer-specific objection inventory
  - `ObjectionEntry` — id, objection_text, objection_type (money|time|ability|trust|fear|confusion|conflict|timing), source, frequency, audience_segment, severity
  - `ObjectionSofteningFlow` — pre-close objection weakening sequence (acknowledge → validate → reframe → provide target)
  - `ObjectionSmashingFlow` — direct objection demolition sequence for close-time use
  - `ObjectionResponseCompilation` — compiled response package ready for webinar module, reaction script, or speaking practice
  - `ObjectionRoutingConfig` — routes compiled objection responses into: webinar modules, reaction content, speaking practice drills, content generation pipelines
- Define the objection delivery pattern: acknowledge and soften → validate and reframe → provide a target
- Define how captured objections from FR-ERA3-45 (Telegram Moderator Bot) feed into this compiler
- Define how CRAL audience-state context enriches objection intelligence

**REJECTION:** No objection catalog schema | no softening vs smashing distinction | no routing config | no audience-state integration | no Telegram moderator bot bridge | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
