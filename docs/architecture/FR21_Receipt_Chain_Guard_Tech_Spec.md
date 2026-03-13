# Tech-Spec: FR21 — Receipt Chain Guard Protocol (DEP-PROTO-010)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0)
**Architecture Reference:** Architecture_Synthesis_Report §Section 9, CCP_Evolution_Architecture_Report_V4
**Skill Implementation:** `infrastructure/ccp/security/receipt-chain-guard/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Evolution_Architecture_Report_V4.docx.md`

---

## 2. Overview

### Problem Statement
In deeply stacked agentic pipelines, "silent fail-forwards" are catastrophic. If a Phase 1 parser drops a critical L3 mapping matrix but the Phase 2 generator still receives a technically sound, empty JSON object, the system will hallucinate a statistically generic output. Without a deterministic tracking architecture that enforces successful execution at every single node, a partially formed or fundamentally degraded Design Brief can leak into production, eroding the coach's trust and audience relationship.

### Solution
FR21 implements the **Receipt Chain Guard Protocol (DEP-PROTO-010)**. This protocol acts as the foundational governance layer across the entire 8-component JIT Compiler pipeline. Every component (from CRAL intake through to the Final Block C validation) must explicitly emit a cryptographic receipt confirming structural success. If an agent attempts to pass its payload to the next stage without a cryptographically verified receipt from the previous stage, the Receipt Chain Guard physically breaks the connection, halts the entire pipeline, quarantines the data, and alerts the System Operator.

FR21 defines DEP-PROTO-010 — the Receipt Chain Guard Protocol. This is the ruleset governing WHEN and HOW receipt writes occur across all pipeline stages. The physical infrastructure executing these writes is DEP-ENG-041, defined in FR47. All specs reference DEP-ENG-041 as the write target. DEP-PROTO-010 is the compliance standard they must conform to. # REVISED: Clarified protocol vs engine infrastructure boundaries.

### Scope
**In scope:**
- Stage 1: Receipt Generation logic at the individual node level.
- Stage 2: Handoff Verification by the downstream node.
- Stage 3: The Circuit Breaker / Quarantine execution mechanism.
- Registration of the `assembly_status` to the `assembly_report.json`.

**Out of scope:**
- Individual component business logic (the guard only manages the handoffs, not the internal component work).
- Live Telegram Crisis intervention (`Liliane` the Crisis Guardian).
- Physical receipt infrastructure and storage engine (owned by FR47, DEP-ENG-041). # REVISED: Added to out of scope per Architect.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-PROTO-010` | Receipt Chain Guard | The overarching protocol enforced at every JIT transaction boundary. |
| `assembly_report.json` | Assembly Status Tracker | OUTPUT — The final ledger storing the cryptographic chain for the Fingerprint Archive. |
| `All DEP-IDs` | Any upstream output | INPUT — Must be accompanied by its `receipt_hash` to be considered valid by the consumer. |
| `DEP-ENG-041` | Receipt Chain Guard Engine | DOWNSTREAM INFRASTRUCTURE — Physical write target for all receipt blocks. Defined in FR47. This spec defines the protocol rules only. # REVISED: Added physical write target defined in FR47. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Deterministic Data Provenance** | - | - | Borrowing from fundamental cryptographic ledger architectures, deterministic data provenance ensures that at layer L(x), the system can mathematically prove that layer L(x-1) not only executed but executed successfully and completely, preventing "Ghost Variables." |

### Technical Decisions
1. **Pessimistic Locking:** The system defaults to `REJECTED/HALTED`. A node cannot proceed unless it actively holds the valid `receipt_hash` from the direct upstream provider.
2. **Immutable Ledgers:** Once a receipt is generated and passed, it cannot be edited. It is hashed into the `assembly_report.json`.
3. **Quarantine Without Deletion:** A broken chain quarantines the batch, sending it to `PARTIAL_MANUAL` status for the System Operator. It does not delete the work done up to the failure point (to save token/compute costs during recovery).

---

## 4. Implementation Plan

### Stage 1: Receipt Generation (Node Emit)
*Agent Name:* Any executing Agent/Adapter (e.g., Builder Engine, CRAL Orchestrator)
*Inputs:* Component `execution_status`, Component `Payload`
*Outputs:* `receipt_hash` string appended to the Payload.
*Failure Condition:* Agent fails to generate a hash because `execution_status` != `SUCCESS`.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'RECEIPT-GENERATION',
  agent_name: 'Any-Executing-Agent',
  timestamp }

**Steps:**
1. Component finishes its assigned intelligence task (e.g., generating `DEP-ENG-016`).
2. Component evaluates its own output against its specific pass/fail schema.
3. If `<PASS>`, the component generates a deterministic hash (e.g., SHA-256 containing `timestamp + node_id + payload_checksum`).
4. Append `receipt_chain_hash: <hash>` to the root of the emitted JSON/YAML object.
5. Transmit to the pipeline bus.

### Stage 2: Handoff Verification (Node Intake)
*Agent Name:* Downstream Consumer Agent
*Inputs:* Incoming Payload containing `receipt_chain_hash`.
*Outputs:* `chain_verified_boolean`
*Failure Condition:* Missing, empty, or statistically invalid hash structure.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'HANDOFF-VERIFICATION',
  agent_name: 'Downstream-Consumer-Agent',
  timestamp }

**Steps:**
1. Downstream agent receives payload from the orchestration bus.
2. Intercept before passing to internal logic.
3. Check for existence and structural validity of `receipt_chain_hash`.
4. If missing/invalid, trigger Stage 3 (Circuit Breaker).
5. If valid, proceed with internal logic.

### Stage 3: Circuit Breaker & Quarantine
*Agent Name:* Master-Pipeline-Orchestrator (Receipt Guard Subsystem)
*Inputs:* Stage 2 Verification Failure Event.
*Outputs:* `quarantine_ticket_id`, Alert API payload.
*Failure Condition:* Cannot reach the Operator Dashboard API (must fallback to local log fatal error).
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'CIRCUIT-BREAKER-QUARANTINE',
  agent_name: 'Master-Pipeline-Orchestrator',
  timestamp }

**Steps:**
1. Catch the invalid/missing receipt exception.
2. Immediately force a `<HALT>` signal to the JIT Compiler array.
3. Wrap the active state of the current compiling batch into a quarantine object.
4. Set `assembly_status: REJECTED_BROKEN_CHAIN`.
5. Push the exact node failure point (e.g., `Failed at: Builder Engine Step 3.5 -> Assembler Tier 1 Handoff`) to the System Operator queue.
6. Kill the current orchestration instance.

---

## 5. Primary Output Schema (assembly_report.json subset)

While the Receipt Guard operates universally, it logs its chain into the final assembly report for archiving.

**Schema Name:** `assembly_report_chain_ledger.json`

```json
{
  "compilation_request_id": "REQ-20260313-099",
  "assembly_status": "HALTED",
  "receipt_ledger": {
    "cral_generation_m1": "rcpt_m1_738abc...",
    "cral_generation_m7": "rcpt_m7_88b1f...",
    "builder_engine_step_1": "rcpt_be1_991c...",
    "builder_engine_step_3_5": "rcpt_be35_1a2b...",
    "assembler_tier_0_preflight": "rcpt_ast0_00x0..."
  },
  "chain_break_event": {
    "failed_at_node": "assembler_tier_1_mandatory",
    "missing_upstream_receipt": "rcpt_ast0_preflight",
    "timestamp": "2026-03-13T08:15:22Z",
    "quarantine_status": "PARTIAL_MANUAL",
    "operator_action_required": true
  }
}
```

---

## 6. Backward Compatibility Fallback
Because the entire purpose of the Receipt Chain Guard is to enforce an absolute block on unverified data passing between systems, **there is ZERO backward compatibility fallback.**
If a legacy script or agent attempts to submit a payload without generating a valid receipt (e.g., an outdated v1.1 template skill missing the hashing adapter), the system violently rejects it. It will not auto-approve, it will not bypass. The legacy component must be upgraded to support `DEP-PROTO-010`.

---

## 7. Tasks

- [ ] **Task 1:** Implement the `Receipt-Generator-Utility` module that can be universally imported across all 8 components (CRAL, Builder, Assembler, etc.) to securely hash outputs based on checksums.
- [ ] **Task 2:** Implement the `Receipt-Verification-Interceptor` at the intake port of the Orchestration Bus to guarantee no payload reaches an Agent without being checked first.
- [ ] **Task 3:** Define the explicit `Circuit Breaker` error handler that catches verification failures, safely wraps the current RAM state into a quarantine JSON object, and clears the execution pipeline.
- [ ] **Task 4:** Modify the JIT Assembler v2.0 `assembly_report.json` writer to ingest and format the `receipt_ledger` array for tracking.
- [ ] **Task 5:** Implement ADR-01 validation during the quarantine process, ensuring the dumped RAM state is explicitly tagged to the tenant's exact UUID to prevent cross-coach data leaks during manual operator review.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Broken Chain Halt):** A payload correctly generated by the Builder Engine is manually stripped of its `receipt_chain_hash` before being passed to the Assembler. The Assembler immediately throws a `HALT` execution error and refuses to read Block A. *Failure Example:* The Assembler ignores the missing receipt, reads the data, and outputs a generic skill file.
- [ ] **AC2 (Quarantine Packaging):** Upon a Stage 3 Circuit Breaker trip, the system successfully writes the exact failure node to `assembly_report.json` under `chain_break_event`. *Failure Example:* The system crashes silently and leaves the operator guessing which component failed to emit the receipt.
- [ ] **AC3 (No-Bypass Rule):** An outdated script lacking receipt support is injected into the testing environment. The `Receipt-Verification-Interceptor` consistently blocks it 100% of the time. *Failure Example:* The Interceptor flags a warning to the console but allows the script to process anyway because the JSON body "looked mostly correct."
- [ ] **AC4 (ADR-01 Strict Isolation):** When a batch is quarantined and surfaced to the System Operator, the data dump explicitly prohibits access or querying of variables belonging to any tenant other than the one currently executing. *Failure Example:* The quarantine log accidentally dumps shared memory showing another coach's private extracted pain data.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| All 8 Upstream Components | Upstream | Must all be individually updated to consume and execute `Receipt-Generator-Utility`. |
| Pipeline Orchestrator Bus | Downstream | The physical routing layer where the Interceptor sits. |
| Operator Dashboard API | Downstream | Target consumer for `quarantine_status` alerts. |

---

## 10. Testing Strategy

### Unit Tests
- **Hash Stability:** Feed the `Receipt-Generator-Utility` an identical JSON payload 50 times. Assert it produces the exact same deterministic hash 50 times.
- **Circuit Breaker Trip:** Directly invoke the `Circuit Breaker` class with a mock failure event. Assert that the resulting `.json` object correctly contains the `chain_break_event` schema with `operator_action_required: true`.

### Integration Tests
- **End-to-End Pipeline Execution:** Run a mock `DEP-ENG-021` payload completely through the 8 stages. Assert that the ultimate `assembly_report.json` contains a perfectly intact `receipt_ledger` displaying 8 subsequent, distinct verification hashes.
- **Induced Handoff Failure:** Force the `Builder Engine Step 3.5` to return a `SUCCESS` payload but sabotage the hash generation. Assert that `Assembler Tier 0` catches the fault, immediately halts the test suite, and emits the quarantine ticket.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Context Bleed Check:** Initiate simultaneous pipeline compilations for Coach A and Coach B. Sabotage Coach A's chain. Assert that the resulting quarantine alert ticket strictly isolates Coach A's dumped payload variables and includes absolutely zero memory crossover from Coach B's currently executing pipeline.
