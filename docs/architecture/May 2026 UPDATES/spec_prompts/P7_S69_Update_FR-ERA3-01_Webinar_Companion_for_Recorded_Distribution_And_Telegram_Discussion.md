# Spec Prompt: FR-ERA3-01 Update — Webinar Companion for Recorded Distribution And Telegram Discussion

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-01
SPEC_TITLE:      Update Webinar Companion for Recorded Distribution And Telegram Discussion
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-07 (V2WS Webinar)
MAPPED_STORIES:  Recorded webinar as canonical delivery object, Telegram distribution pipeline, replay management, CTA routing, discussion thread linking
CBAR_MANDATES:   Update-Not-Standalone Rule, Live-First-Doctrine Rule
BACKEND_REL:     UPDATE existing Webinar Companion runtime — MUST add recorded webinar distribution, Telegram replay management, CTA routing, and discussion integration. Folds FR-ERA3-44 into existing companion.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-01_Webinar_Companion_Tech_Spec_UPDATED_FOR_DISTRIBUTION.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update folds `FR-ERA3-44` (V2WS Recorded Webinar Distribution And Telegram Discussion) into the existing Webinar Companion.
>
> The webinar companion must now support recorded webinar as a canonical delivery object alongside live events. Recorded webinars are the 1-3 month fluency-building lane, not the philosophical center.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion and Complete Editing Session mandate)
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
2. Source PRD: `PRD-07`. **PROOF:** Quote lines on V2WS webinar distribution.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to webinar replay management and Telegram distribution within the execution graphs.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the webinar correction doctrine (Roadmap §2.3) and the W5 workflow.
5. Existing FR-ERA3-01 spec: read fully. **PROOF:** Quote existing webinar session and companion schemas.
6. Existing backend: read `src/ccp/services/v2ws_interactive_service.py` or equivalent. **PROOF:** Quote real method signatures.
6. Existing test patterns: read 1 `tests/integration/` file covering webinar behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=6) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Distribution contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `RecordedWebinarDeliveryObject` — canonical object representing a recorded webinar (video, transcript, module mapping, metadata)
  - `TelegramDistributionPlan` — channel, schedule, replay link, CTA attachment
  - `ReplayManagementConfig` — expiry, access control, view tracking
  - `CTARoutingTable` — routes CTA clicks to appropriate conversion surfaces
  - `DiscussionThreadLink` — links a webinar to its Telegram discussion thread

**REJECTION:** Treats as standalone spec instead of update | no recorded delivery object | no Telegram distribution plan | no replay management | no CTA routing | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
