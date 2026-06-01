# Spec Prompt: FR-ERA3-56 — Command Surface And Experience Router

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-56
SPEC_TITLE:      Command Surface And Experience Router
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-01 (Platform Strategy), PRD-04 (CVE)
MAPPED_STORIES:  Telegram commands, AFFiNE triggers, operator commands, supervisor commands, slash-command conventions, experience routing across surfaces
CBAR_MANDATES:   Bridge-Existing-Surfaces Rule, Command-Convention-Rule, No-Parallel-Router Rule
BACKEND_REL:     NEW bridge-oriented spec — MUST wire existing Telegram, Mini App, AFFiNE, and API routing surfaces into a unified command convention. Any command triggering a lesson or vertical video generation workflow must instantiate or link to a Complete Editing Session state wrapper.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-56_Command_Surface_And_Experience_Router_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a NEW spec but bridge-oriented. It does not replace existing routers. It defines the **command convention layer** that sits above them.
>
> The programs (Persuasive Speaking, Transformational Webinar, Reactions) become operable through commands. The Roadmap (§4.5) defines examples: `/record-reaction`, `/build-quote-commentary`, `/compile-webinar-module`, `/rehearse-close`, `/score-delivery`, `/push-lesson`, `/run-objection-drill`.
>
> This spec defines how those commands route across Telegram, AFFiNE, Mini App, and API surfaces.
>
> **COMPLETE EDITING SESSION CONTEXT:**
> Slash commands triggering media or research steps must operate within a linked Complete Editing Session payload, passing the session ID parameter to prevent assets or parameters from being lost.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (9+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `src/ccp/services/vidye_router.py` (Local Code Reference)
> - `docs/architecture/april_updates/FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-07_AFFiNE_Studio_Block_Orchestration_Tech_Spec.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` (PRD Module)
> - `docs/prd/modules/PRD_04_CVE_Experience_Design.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-01`, `PRD-04`. **PROOF:** Quote lines on platform command surfaces and experience routing.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote details about command routing structures and session linking conventions.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the command examples from Roadmap §4.5 and the workflow entry commands from §4.1.
5. Existing Telegram router: read `src/ccp/services/vidye_router.py` or equivalent. **PROOF:** Quote real handler and routing patterns.
6. Existing Mini App Host Shell: read FR-ERA3-08 spec. **PROOF:** Quote command routing contracts.
7. Existing AFFiNE pipeline: read FR-ERA3-07 spec. **PROOF:** Quote trigger contracts.
7. Existing test patterns: read 1 `tests/integration/` file covering command routing.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=6) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Command surface contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `CommandDefinition` — command_id, slash_syntax, description, required_permissions, source_surfaces, target_workflow, parameters
  - `ExperienceRoute` — maps a command to its rendering surface (Telegram inline, Mini App, AFFiNE block, API response)
  - `CommandRegistry` — queryable registry of all available commands per role (coach, operator, supervisor)
  - `SurfaceAdapter` — interface contract for each surface (Telegram, Mini App, AFFiNE, API) to receive and execute commands
- Define the initial command inventory:
  - `/record-reaction` — triggers W1 Signal-to-Commentary
  - `/build-quote-commentary` — triggers Living Commentary Quote format
  - `/build-comparison-commentary` — triggers Living Commentary Comparison format
  - `/compile-webinar-module` — triggers W5 module compilation stage
  - `/rehearse-close` — triggers W4 Delivery Module Mastery for close module
  - `/score-delivery` — triggers delivery scoring evaluation
  - `/push-lesson` — triggers W3 Voice-Note-to-Lesson delivery
  - `/run-objection-drill` — triggers objection practice from FR-ERA3-50F
- Define role-based command visibility: coach commands, operator commands, supervisor commands

**REJECTION:** No command registry | no surface adapter contracts | no role-based visibility | fewer than 8 command definitions | creates parallel router instead of wiring existing ones | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
