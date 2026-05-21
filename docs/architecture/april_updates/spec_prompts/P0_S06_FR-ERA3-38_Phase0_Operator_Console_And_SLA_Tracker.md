# Spec Prompt: FR-ERA3-38 - Phase-0 Operator Console and SLA Tracker

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-38
SPEC_TITLE:      Phase-0 Operator Console and SLA Tracker
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-09
MAPPED_STORIES:  12-packages-per-day operator workflow, 24h max SLA tracking, package-status visibility, missing-input and stuck-run recovery
CBAR_MANDATES:   Human-Operator-Leverage Rule, 24h Delivery Readiness Rule, Shared-Workspace-First Rule, Clear-State-Visibility Rule, Recovery-Before-Churn Rule
BACKEND_REL:     NEW operator console surface - MUST sit on top of shared Phase-0 runtime and existing state/receipt infrastructure rather than bypassing it
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the operator console for Phase-0 package throughput. It is the internal control surface that makes the Phase-0 machine usable in practice.
>
> Minimum scope:
> - queue visibility
> - readiness visibility
> - delivery status
> - 24h SLA countdowns
> - missing-input alerts
> - payment-state visibility
> - upgrade-handoff visibility

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-01`. **PROOF:** Quote the exact lines that establish Trial Phase-0, Telegram/AFFiNE command surfaces, and operator leverage expectations.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files for internal console/admin patterns, state visibility, receipts, and queue/job tracking if present. **PROOF:** Quote real method signatures.
5. Existing models: read state, receipt, queue, or job-result model files.
6. Existing test patterns: read 2 `tests/integration/` files covering stateful dashboards, queues, or status APIs.
7. Existing failure-recovery patterns: confirm what the current architecture uses for stuck tasks, missing dependencies, and retryable states.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Operator states / views | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `Phase0OperatorQueueView`
  - `Phase0SlaState`
  - `Phase0Alert`
  - `Phase0RunStatus`
  - `Phase0MissingInputState`
  - `Phase0EscalationState`
- Define operator-ready states for:
  - new intake
  - blocked / missing inputs
  - audit in progress
  - assets rendering
  - ready to deliver
  - delivered awaiting payment
  - paid / unlocked
  - upgraded / handed off
- Preserve the ability to manage throughput without requiring full bespoke project management tooling
- Define alerting and escalation rules that support `12 packages/day` without chaos

**REJECTION:** vague internal console | no SLA state model | no operator queue model | no recovery states | no alert design | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
