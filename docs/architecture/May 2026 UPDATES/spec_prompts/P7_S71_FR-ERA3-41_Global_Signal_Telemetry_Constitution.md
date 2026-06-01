# Spec Prompt: FR-ERA3-41 — Global Signal Telemetry Constitution

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-41
SPEC_TITLE:      Global Signal Telemetry Constitution
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-01 (Platform Strategy)
MAPPED_STORIES:  Canonical telemetry packets, minimum 48 signal points, aggregation rules, history store, anomaly detection, receipt behavior
CBAR_MANDATES:   Telemetry-Sovereignty Rule, Minimum-48-Signals Rule, Receipt-Chain-Preservation Rule
BACKEND_REL:     NEW governance substrate — MUST integrate with existing receipt chain guard (FR47), existing health endpoints, existing Phase 0 operator console (FR-ERA3-38), and existing scoring systems
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-41_Global_Signal_Telemetry_Constitution_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a foundational NEW spec that defines the telemetry constitution for the entire platform. It is the data backbone for the Global Supervisor Agent (FR-ERA3-42).
>
> Signal families: content production, delivery quality, engagement, commercial conversion, coaching progression, system health, error rates, pipeline throughput.
>
> Minimum 48 signal points across all families.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (9+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `src/ccp/services/receipt_chain.py` (Local Code Reference)
> - `src/ccp/services/global_admin_service.py` (Local Code Reference)
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` (PRD Module)
> - `docs/architecture/april_updates/FR-ERA3-38_Phase0_Operator_Console_And_SLA_Tracker_Tech_Spec.md`
> - `docs/architecture/FR47_Receipt_Chain_Guard_Tech_Spec.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRD: `PRD-01`. **PROOF:** Quote lines on platform telemetry and supervision expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to the 48-signals platform telemetry and SLA operator console expectations.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the W8 Supervisor Intervention workflow and the delivery telemetry dimensions from Roadmap §4.4.
5. Existing receipt chain: read `src/ccp/services/receipt_chain.py` or equivalent. **PROOF:** Quote real method signatures.
6. Existing global admin: read `src/ccp/services/global_admin_service.py` or equivalent. **PROOF:** Quote real method signatures.
7. Existing Phase 0 operator console: read FR-ERA3-38. **PROOF:** Quote SLA tracking contracts.
7. Existing scoring systems: read existing scoring model files. **PROOF:** Quote schemas.
8. Existing test patterns: read 1 `tests/integration/` file covering health or receipt behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 350 LINES

§1 Files Read (>=7) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Telemetry contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `TelemetryPacket` — canonical telemetry event with signal_id, family, value, timestamp, source_container, metadata
  - `TelemetrySignalPoint` — definition of a single signal (minimum 48 across all families)
  - `TelemetryAggregationRule` — how signals are rolled up over time windows
  - `TelemetryHistoryStore` — retention, partitioning, query interface
  - `AnomalyDetectionThreshold` — per-signal anomaly thresholds and alert triggers
  - `ReceiptBehavior` — how telemetry events chain into the receipt audit trail
- Define signal families with minimum signal counts:
  - Content production (>=6), Delivery quality (>=8), Engagement (>=6), Commercial conversion (>=6), Coaching progression (>=8), System health (>=6), Error rates (>=4), Pipeline throughput (>=4)
- Define how telemetry integrates with existing receipt chain

**REJECTION:** Fewer than 48 signal points | no anomaly detection | no receipt behavior | no aggregation rules | ignores existing receipt chain | no signal family breakdown | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
