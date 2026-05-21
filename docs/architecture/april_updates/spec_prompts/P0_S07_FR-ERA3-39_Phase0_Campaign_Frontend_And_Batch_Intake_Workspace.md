# Spec Prompt: FR-ERA3-39 - Phase-0 Campaign Frontend and Batch Intake Workspace

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-39
SPEC_TITLE:      Phase-0 Campaign Frontend and Batch Intake Workspace
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-04, PRD-09
MAPPED_STORIES:  campaign frontend for Phase-0, coach-ID-based intake, bulk file upload, shared main-environment execution surface, fast batch preparation for 12 packages/day
CBAR_MANDATES:   Main-Environment-Reuse Rule, Coach-ID-Bound Intake Rule, Batch-Speed Rule, Shared-Workspace-First Rule, No-Full-Container-Before-Payment Rule, Human-Operator-Leverage Rule
BACKEND_REL:     NEW frontend/control surface - MUST reuse the same backend process patterns already used by Telegram and AFFiNE pipelines, but run them in a shared internal campaign environment instead of one separate container per coach
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-39_Phase0_Campaign_Frontend_And_Batch_Intake_Workspace_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the actual campaign frontend used internally to run Phase-0 outreach and proof-package generation.
>
> It is not just an admin form. It must let operators:
> - create or bind a coach record by `coach_id`
> - upload or attach source files quickly
> - organize many coaches in one session
> - validate readiness at a glance
> - trigger the shared Phase-0 backend pipeline from the main environment
>
> The UI must be optimized for batch throughput, not generic dashboard aesthetics.

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`
> - `docs/architecture/april_updates/spec_prompts/P0_S01_FR-ERA3-33_Phase0_Prospect_Intake_Console.md`
> - `docs/architecture/april_updates/spec_prompts/P0_S02_FR-ERA3-34_Phase0_Prospect_Workspace_And_Artifact_Store.md`
> - `docs/architecture/april_updates/spec_prompts/P0_S06_FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker.md`

> [!IMPORTANT]
> **CAMPAIGN-FRONTEND REQUIREMENT:**
> The frontend must assume the same exact backend process logic already exists in the broader CCP ecosystem for content creation, but this surface runs those flows inside one shared main environment rather than provisioning separate coach containers at Phase-0.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-01`, `PRD-04`. **PROOF:** Quote the exact lines that establish Telegram/AFFiNE command surfaces, human-first experience constraints, and Trial Phase-0 commercial flow.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files for FastAPI app entry, upload/asset intake, campaign/admin/internal tool patterns if present, and any coach-binding / workspace patterns. **PROOF:** Quote real method signatures.
5. Existing models: read intake, packet, artifact, workspace, and state models relevant to Phase-0.
6. Existing frontend / interface precedents: read any AFFiNE-facing or internal surface files that establish current UX or model-binding patterns.
7. Existing test patterns: read 2 `tests/integration/` files covering intake, upload, or internal API surface behavior.
8. Existing main-environment reuse precedent: confirm what backend pipelines already exist that should be reused instead of rebuilt.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 340 LINES

§1 Files Read (>=10) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Frontend/workspace artifacts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=5 phases, >=16 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `Phase0CampaignWorkspace`
  - `Phase0CoachRow`
  - `Phase0CoachBinding`
  - `Phase0BatchUploadSession`
  - `Phase0ReadinessSummary`
  - `Phase0ExecutionRequest`
  - `Phase0WorkspaceFilterState`
  - `Phase0BulkAttachmentResult`
- The frontend must support:
  - coach ID entry / lookup / binding
  - drag-drop upload
  - bulk multi-coach staging
  - file grouping per coach
  - readiness-at-a-glance
  - per-coach and multi-select execution triggers
  - status filtering by readiness, missing inputs, delivery state, and payment state
- The spec must explicitly define:
  - how files are organized under the shared system
  - how coach namespaces are separated without separate containers
  - how operators can move fast without losing artifact lineage
  - how this frontend triggers existing backend pipelines from the main environment
- The spec must avoid building a decorative CRM. It is a production control surface.

**REJECTION:** generic dashboard spec | no coach-id binding model | no batch upload model | assumes separate container per coach | no main-environment reuse law | no execution trigger flow | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
