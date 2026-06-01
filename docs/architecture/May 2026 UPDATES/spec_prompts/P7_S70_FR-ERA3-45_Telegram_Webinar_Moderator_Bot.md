# Spec Prompt: FR-ERA3-45 — Telegram Webinar Moderator Bot

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-45
SPEC_TITLE:      Telegram Webinar Moderator Bot
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-07 (V2WS Webinar), PRD-04 (CVE)
MAPPED_STORIES:  Webinar discussion moderation, objection capture, FAQ routing, community hygiene, replay distribution, CTA reinforcement
CBAR_MANDATES:   Integrate-Existing-Bot-Framework Rule, Moderation-Discipline Rule
BACKEND_REL:     NEW Telegram bot service — MUST integrate with existing Telegram bot framework (vidye_router.py), existing webinar companion (FR-ERA3-01), and existing CBCS engagement logic
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-45_Telegram_Webinar_Moderator_Bot_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a genuinely NEW spec because the moderator behavior is a missing product surface. However, it must be built on the existing Telegram bot framework — not a parallel bot system.
>
> The moderator bot manages webinar discussion threads: moderation, objection capture, FAQ routing, community hygiene, replay link distribution, and CTA reinforcement.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (9+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `src/ccp/services/vidye_router.py` (Local Code Reference)
> - `docs/architecture/april_updates/FR-ERA3-01_Webinar_Companion_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-02_In_Chat_Telegram_Payments_Tech_Spec.md`
> - `docs/prd/modules/PRD_04_CVE_Experience_Design.md` (PRD Module)
> - `docs/prd/modules/PRD_07_V2WS_Webinar.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-07`, `PRD-04`. **PROOF:** Quote lines on webinar community and discussion expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to bot interactions and conversion triggers in the speaker program workflows.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the W5 workflow Telegram distribution and moderated discussion stages.
5. Existing Telegram framework: read `src/ccp/services/vidye_router.py` or equivalent. **PROOF:** Quote real handler signatures and routing patterns.
6. Existing bot handlers: read other Telegram handler files. **PROOF:** Quote patterns.
7. Existing FR-ERA3-01 and FR-ERA3-02 specs. **PROOF:** Quote webinar and payment contracts.
7. Existing test patterns: read 1 `tests/integration/` file covering Telegram bot behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=6) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Bot service contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `ModeratorBotInstance` — bot config per webinar discussion thread
  - `DiscussionModerationRules` — spam filter, off-topic detection, escalation triggers
  - `ObjectionCaptureService` — captures audience objections from discussion, routes to objection intelligence (FR-ERA3-50F)
  - `FAQRoutingEngine` — detects FAQ patterns, auto-responds or routes to coach
  - `CommunityHygienePolicy` — rules for thread cleanup, warning system, ban policy
- Define bot capabilities: discussion moderation, objection capture, FAQ/follow-up routing, community hygiene, replay link distribution, CTA reinforcement
- Define how captured objections feed into FR-ERA3-50F Objection Intelligence

**REJECTION:** No moderation rules schema | no objection capture | no FAQ routing | ignores existing Telegram framework | creates parallel bot system | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
