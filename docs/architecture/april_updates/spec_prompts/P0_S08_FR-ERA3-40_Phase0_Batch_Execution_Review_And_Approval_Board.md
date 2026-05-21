# Spec Prompt: FR-ERA3-40 - Phase-0 Batch Execution Review and Approval Board

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-40
SPEC_TITLE:      Phase-0 Batch Execution Review and Approval Board
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-03, PRD-09
MAPPED_STORIES:  batch execution controls, produced-results review, operator approval loop, payment-ready package release, batch retry and revision management
CBAR_MANDATES:   Review-Before-Release Rule, Batch-Execution-Visibility Rule, Shared-Workspace-First Rule, Human-Approval Rule, Payment-Handoff-Readiness Rule
BACKEND_REL:     NEW review/approval surface - MUST sit on top of the shared Phase-0 runtime and existing artifact/state/receipt infrastructure, not bypass it
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-40_Phase0_Batch_Execution_Review_And_Approval_Board_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the board where operators review produced Phase-0 results before release.
>
> It must let the team:
> - run backend jobs in batches
> - inspect generated audits, PDFs, scoring cards, audit explainer videos, preview assets, and produced content
> - accept, reject, re-run, or mark for revision
> - attach payment/unlock state
> - release approved packages cleanly
>
> This is the true production-review surface for Phase-0.

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `docs/architecture/april_updates/spec_prompts/P0_S03_FR-ERA3-35_Audit_Intelligence_Engine.md`
> - `docs/architecture/april_updates/spec_prompts/P0_S04_FR-ERA3-36_Phase0_Delivery_Orchestrator.md`
> - `docs/architecture/april_updates/spec_prompts/P0_S06_FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker.md`

> [!IMPORTANT]
> **REVIEW-SURFACE REQUIREMENT:**
> The board must treat these as first-class review artifacts:
> - PDF audit
> - audit scoring cards
> - audit explainer video built from scoring cards
> - generated explainers
> - cinematic proof artifact
> - optional meme / carousel outputs

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-01`, `PRD-03`. **PROOF:** Quote the exact lines that establish proof-package sequencing, human review expectations, and media artifact responsibilities.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files for pipeline execution, artifact state, reviewable outputs, receipts, and status transitions. **PROOF:** Quote real method signatures.
5. Existing models: read delivery-run, artifact, receipt, render-result, and payment-state models.
6. Existing test patterns: read 2 `tests/integration/` files covering pipeline execution, approval, or artifact-result flows.
7. Existing retry/recovery precedent: confirm how the architecture handles partial failures and reruns.
8. Existing review-sequencing precedent: confirm what should be reviewed before release and what can be auto-approved.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 340 LINES

§1 Files Read (>=10) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Review/approval artifacts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=5 phases, >=16 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `Phase0BatchExecutionBoard`
  - `Phase0ReviewRow`
  - `Phase0ArtifactReviewSet`
  - `Phase0ApprovalDecision`
  - `Phase0RerunRequest`
  - `Phase0RevisionRequest`
  - `Phase0ReleaseState`
  - `Phase0PaymentReadyState`
- The review board must support:
  - single-run review
  - batch-run review
  - side-by-side comparison
  - before/after audit card comparison
  - PDF audit preview
  - audit explainer video preview
  - approve / reject / rerun / revise actions
  - payment-ready and release-ready markers
- The spec must explicitly define:
  - what artifacts require human review
  - what can be auto-passed
  - what happens on partial failures
  - how reruns preserve lineage and prior results
  - how release integrates with the payment/unlock runtime

**REJECTION:** vague review board | no PDF/video review support | no rerun law | no approval-state model | no release-state model | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
