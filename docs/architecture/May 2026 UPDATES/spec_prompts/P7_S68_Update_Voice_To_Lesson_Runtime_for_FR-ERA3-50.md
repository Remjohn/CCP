# Spec Prompt: FR-ERA3-50 Update — Voice-To-Lesson Runtime for Live Lesson Compilation And Delivery

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-50
SPEC_TITLE:      Update Voice-To-Lesson Runtime for Live Lesson Compilation And Delivery
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-04 (CVE), PRD-02 (CCF)
MAPPED_STORIES:  Live lesson compilation from voice notes, delivery tagging, AFFiNE lesson cards, Telegram drip delivery
CBAR_MANDATES:   Brownfield-Update Rule, Real-Code-Reference Rule
BACKEND_REL:     UPDATE existing voice-to-lesson runtime — MUST extend the current voice_to_lesson.py service to wrap lessons inside the Complete Editing Session state wrapper. All parsed transcript fragments, generated templates, and audio assets must reside in this session.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-50_Voice_Note_To_Live_Lesson_Tech_Spec_UPDATED.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is an **update/bridge** prompt around the existing `voice_to_lesson.py`, NOT a greenfield build.
>
> The flow: coach voice note → transcript → lesson structuring → edit/render → AFFiNE tagging → Telegram or drip delivery.
>
> This is the W3 workflow from the Roadmap.
>
> **COMPLETE EDITING SESSION CONTEXT:**
> Every live lesson compilation must be bound to a Complete Editing Session wrapper, ensuring that early transcript chunks, research, and visual attachments are fully saved, versioned, and retrievable.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (10+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session mandate)
> - `src/ccp/services/voice_to_lesson.py` (Local Code Reference)
> - `src/ccp/services/session_to_course.py` (Local Code Reference)
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_04_CVE_Experience_Design.md` (PRD Module)
> - `docs/architecture/FR-CA11-06_Voice_Note_Course_Material_Tech_Spec.md`
> - `docs/architecture/FR-CA11-07_Session_to_Course_Pipeline_Tech_Spec.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-04`, `PRD-02`. **PROOF:** Quote lines on voice-to-lesson pipeline expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to lesson compilation and Complete Editing Session integration.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote W3 Voice-Note-to-Lesson workflow from Roadmap §4.1.
5. **Existing code — CRITICAL:** Read `src/ccp/services/voice_to_lesson.py` fully. **PROOF:** Quote at least 3 real method signatures.
6. Existing code: read `src/ccp/services/session_to_course.py`. **PROOF:** Quote real method signatures.
7. Existing specs: read FR-CA11-06 and FR-CA11-07. **PROOF:** Quote pipeline stage contracts.
8. Existing test patterns: read 1 `tests/integration/` file covering voice-to-lesson behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=7) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Lesson compilation contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec** extending the existing voice-to-lesson service
- Define canonical schemas for:
  - `LessonCompilationPacket` — structured lesson output from voice note input
  - `DeliveryTagSet` — tags for lesson type, communication module used, difficulty, audience level
  - `TelegramDripSchedule` — drip delivery config for Telegram channel/group
  - `AFFiNELessonCard` — AFFiNE workspace card representing a compiled lesson
- Define the updated pipeline: voice note → transcript → lesson structuring → edit/render → AFFiNE tagging → Telegram or drip delivery
- Must reference and extend existing `voice_to_lesson.py` methods, not replace them

**REJECTION:** Treats as greenfield | no reference to existing voice_to_lesson.py | no real method signatures cited | no drip delivery schema | no AFFiNE lesson card | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
