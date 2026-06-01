# Spec Prompt: FR39 Update — Pi Extension Harness for ERA3 Execution Graph

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR39 (Pi Extension Harness)
SPEC_TITLE:      Update Pi Extension Harness for ERA3 Execution Graph
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-01 (Platform Strategy)
MAPPED_STORIES:  Canonical extension registry, dependency ordering, stage execution contracts, Living Commentary pipeline extensions
CBAR_MANDATES:   Update-Not-Replace Rule, Extension-Registry-Governance Rule
BACKEND_REL:     UPDATE existing Pi Extension Harness — MUST add canonical extension registry, dependency ordering, and stage execution contracts for ERA3 pipeline stages
OUTPUT_FILE:     docs/architecture/april_updates/FR39_Pi_Extension_Harness_Tech_Spec_UPDATED_FOR_ERA3_EXECUTION_GRAPH.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is an UPDATE prompt against the existing FR39 / Pi Extension Harness. It folds `FR-ERA3-51` (Pi Extension Registry And Execution Graph) into the existing harness.
>
> The Pi harness already exists as code. This update adds formalized extension registry governance, dependency ordering, and execution graph semantics for ERA3 pipelines.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session mandate)
> - `src/ccp/services/pi_extension_harness.py` (Local Code Reference)
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` (PRD Module)
> - `docs/architecture/FR39_Core_Orchestration_11_Pi_Extensions.md`
> - `docs/architecture/FR39_Pi_Agent_Tech_Spec.md` (or equivalent)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRD: `PRD-01`. **PROOF:** Quote lines on Pi agent and extension expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote details about the Pi extension graph and stage execution contracts within the Complete Editing Session.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote Wave D Pi Harness Expansion specs from Roadmap §5.
5. **Existing code — CRITICAL:** Read `src/ccp/services/pi_extension_harness.py` fully. **PROOF:** Quote at least 3 real method signatures and the current extension pattern.
6. Existing FR39 spec: read the Pi Agent spec. **PROOF:** Quote harness architecture.
6. Existing test patterns: read 1 `tests/integration/` file covering Pi harness behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=5) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Extension registry contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec** extending the existing Pi Extension Harness
- Define canonical schemas for:
  - `ExtensionDefinition` — id, name, stage, dependencies, input_contract, output_contract, timeout, retry_policy
  - `ExtensionRegistry` — queryable registry of all registered extensions
  - `ExecutionGraph` — DAG of extension dependencies with topological execution order
  - `StageExecutionContract` — input/output type contracts per pipeline stage
  - `ExtensionHealthCheck` — health and readiness probes per extension
- Define how Living Commentary pipeline stages register as extensions
- Must reference and extend existing `pi_extension_harness.py` methods, not replace them

**REJECTION:** Treats as greenfield | no reference to existing pi_extension_harness.py | no real method signatures cited | no execution graph DAG | no dependency ordering | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
