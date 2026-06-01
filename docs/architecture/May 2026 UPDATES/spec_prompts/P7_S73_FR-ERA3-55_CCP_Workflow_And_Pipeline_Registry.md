# Spec Prompt: FR-ERA3-55 — CCP Workflow And Pipeline Registry

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-55
SPEC_TITLE:      CCP Workflow And Pipeline Registry
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-01 (Platform Strategy)
MAPPED_STORIES:  Canonical workflow inventory (W1-W8), entry commands, packets, downstream owners, review points, telemetry outputs
CBAR_MANDATES:   Workflow-Registry-Governance Rule, All-Workflows-Cataloged Rule
BACKEND_REL:     NEW canonical registry — MUST catalog all existing and new workflows with their entry commands, packets, downstream owners, review points, and telemetry outputs. Workflows W1 (Signal-to-Commentary), W1A (Unified Assembling), and W3 (Voice-to-Lesson) must utilize the Complete Editing Session payload and compile vertical videos using the Remotion Node.js backend.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-55_CCP_Workflow_And_Pipeline_Registry_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is the governance-layer registry that makes all CCP workflows discoverable, auditable, and operationally trackable. It catalogs the W1-W8 workflow classes defined in the Living Commentary Roadmap plus any additional workflows from the existing system.
>
> **COMPLETE EDITING SESSION & REMOTION PIPELINES:**
> In W1, W1A, and W3, the pipeline execution must wrap around a Complete Editing Session state, tracking all intermediate assets and variables to prevent context loss. All vertical video files are compiled via the Remotion Node.js rendering backend using `@remotion/skia`.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md` (especially §4 Workflow And Pipeline Inventory)
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion and Complete Editing Session mandate)
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` (PRD Module)
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md` (PRD Module)
> - `src/ccp/services/` (Local Service Directory)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRD: `PRD-01`. **PROOF:** Quote lines on platform workflow expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to the 8 workflow definitions, Complete Editing Sessions, and Remotion rendering pipeline.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the entire §4.1 workflow inventory (W1 through W8) from the Roadmap.
5. Existing pipeline code: scan `src/ccp/services/` for pipeline and workflow files. **PROOF:** List found files and quote key method signatures.
6. Existing test patterns: read 1 `tests/integration/` file covering pipeline or workflow behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=5) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Workflow registry contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `WorkflowDefinition` — id, name, description, entry_commands, stages, downstream_owners, review_points, telemetry_outputs
  - `PipelineStage` — stage_id, name, input_contract, output_contract, owner_service, timeout, retry_policy
  - `WorkflowEntryCommand` — command string, source surface (Telegram, AFFiNE, API), required permissions
  - `WorkflowPacket` — intermediate data packet passed between stages
  - `ReviewPoint` — stage at which human review is required before proceeding
  - `TelemetryOutput` — what signals this workflow emits into the telemetry constitution
  - `WorkflowRegistry` — the queryable registry of all workflow definitions
- Must catalog ALL workflows:
  - W1: Signal-to-Commentary (SCRE/CRAL → reaction → recording → primitive coalition → Living Commentary → review → deployment)
  - W1A: Unified Assembling Pipeline (Uploaded `.mp4` → Dynamic routing into 4 formats: Cinematic [CMF], Living Commentary, 2D Avatar Explainer [Animation Studio], and Conscious Reactions editing).
  - W2: Interview-to-Weekly-Package (45-60 min interview → source extraction → archetype routing → package assembly → review → deployment)
  - W3: Voice-Note-to-Lesson (voice note → transcript → lesson → edit/render → AFFiNE → Telegram drip)
  - W4: Delivery Module Mastery (practice task → record → score → feedback → content extraction → longitudinal progress)
  - W5: Transformational Webinar Construction And Delivery (topic → brainstorm → V2WS → rehearsal → recording/live → edit → Telegram → discussion → telemetry → SSS update)
  - W5A: Seminar Speaking Score Loop (module practice → record/live → review → SSS update → badge → next drill)
  - W5B: Long-Form Editing Upsell (recorded session → cleanup → visual enrichment → pacing → replay-ready → +$9.99)
  - W6: Reaction-to-Program Conversion (reaction → score + package → speaking invitation → continuity program)
  - W7: Phase-0 Prospect Bridge (intake → audit → card board → PDF → unlock → migration into container)
  - W8: Supervisor Intervention (telemetry anomaly → supervisor summary → operator command → local rerun/revise/inspect/notify)

**REJECTION:** Fewer than 8 workflow definitions | no entry command mapping | no review points | no telemetry output mapping | no pipeline stage contracts | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
