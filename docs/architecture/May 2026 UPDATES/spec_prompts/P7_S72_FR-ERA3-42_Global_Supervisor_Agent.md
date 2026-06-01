# Spec Prompt: FR-ERA3-42 — Global Supervisor Agent

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-42
SPEC_TITLE:      Global Supervisor Agent
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-01 (Platform Strategy)
MAPPED_STORIES:  Telegram-accessible supervisor agent, bounded operational verbs, secure delegation into containers, telemetry digest consumption, notification routing
CBAR_MANDATES:   Bounded-Verb-Set Rule, Secure-Delegation Rule, Container-Isolation-Respect Rule
BACKEND_REL:     NEW supervisor agent — MUST integrate with existing Global Admin Dashboard (FR-COM-02), existing Telegram bot framework, existing telemetry constitution (FR-ERA3-41), and existing container orchestration
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-42_Global_Supervisor_Agent_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a NEW spec that extends the current global admin into an agent-accessible supervisor layer. It is NOT a replacement for global admin. It is the agent interface on top of it.
>
> The supervisor agent has a **bounded** set of operational verbs: inspect, rerun, revise, suspend, migrate, notify. It must never bypass container isolation.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (10+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `src/ccp/services/global_admin_service.py` (Local Code Reference)
> - `src/ccp/services/vidye_router.py` (Local Code Reference)
> - `src/ccp/services/pi_extension_harness.py` (Local Code Reference)
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` (PRD Module)
> - `docs/architecture/FR-COM-02_Global_Admin_Dashboard_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-41_Global_Signal_Telemetry_Constitution_Tech_Spec.md` (or prompt for it)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRD: `PRD-01`. **PROOF:** Quote lines on global supervision and platform control.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote supervisor intervention details and anomaly detection rules in editing sessions.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the separation of concerns (Roadmap §2.1 Global Supervisor Layer) and W8 Supervisor Intervention workflow.
5. Existing global admin: read `src/ccp/services/global_admin_service.py` or equivalent. **PROOF:** Quote real method signatures.
6. Existing FR-COM-02 spec: read Global Admin Dashboard. **PROOF:** Quote current architecture.
7. Existing Telegram framework: read `src/ccp/services/vidye_router.py` or equivalent. **PROOF:** Quote handler patterns.
8. Existing Pi harness: read `src/ccp/services/pi_extension_harness.py` or equivalent. **PROOF:** Quote extension patterns.
8. Existing test patterns: read 1 `tests/integration/` file covering admin or operator behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=7) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Supervisor agent contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `SupervisorAgentInstance` — agent config, Telegram channel binding, permission scope
  - `SupervisorNotification` — notification payload with severity, source, context, recommended action
  - `OperationalVerb` — bounded enum: `inspect`, `rerun`, `revise`, `suspend`, `migrate`, `notify`
  - `SecureDelegationContract` — how the supervisor delegates actions into containers without violating isolation
  - `TelemetryDigest` — summarized telemetry view consumed by the supervisor agent
- Define Telegram accessibility: command interface, notification routing, digest summaries
- Define secure delegation: the supervisor can trigger actions inside a container only through the loopback gateway, never through direct database access

**REJECTION:** Unbounded operational verbs | no secure delegation contract | no telemetry digest integration | ignores existing global admin | bypasses container isolation | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
