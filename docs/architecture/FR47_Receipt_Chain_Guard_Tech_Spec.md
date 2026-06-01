# Tech-Spec: FR47 — Receipt Chain Guard (DEP-ENG-041)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §8.2.1, Architecture Synthesis Report
**Skill Implementation:** `skills/governance/receipt_chain_guard/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`

---

## 2. Overview

### Problem Statement
A system orchestrating 65 independent active agents across multiple complex pipelines (CCF, CBCS, V2WS) poses catastrophic hallucination risks. Relying solely on a final "post-generation" quality check is insufficient for safety; if a sub-agent deep in the pipeline (e.g., an extractive research node) hallucinates or produces a malformed JSON, downstream agents will blindly compound that error. Without immutable, step-by-step cryptographic logging, debugging a ruined batch becomes a black-box guessing game, and "partial publications" of degraded content become inevitable.

### Solution
FR47 defines the **Receipt Chain Guard (DEP-ENG-041)**. Acting as the foundational cornerstone of the CCP's integrity layer, this is a deterministic, unforgiving boundary wall. Every single agent interaction, API call, and state transition emits a structured JSON receipt that cryptographically hashes the input and output. These receipts form a definitive linked list. If any node fails a structural check or times out, the chain breaks. The entire session batch is instantly quarantined, rendering partial or degraded publication architecturally impossible.

### Scope
**In scope:**
- The Receipt Chain standard schema `[agent, timestamp, input_hash, output_hash, extension_triggered, mode, confidence]`.
- The linked-list hashing mechanism (`previous_receipt_hash`).
- The Quarantine execution (halting the Orchestrator).
- Storage vector (Supabase `receipt_chain` table).

**Out of scope:**
- The semantic evaluation of the content (handled by the Validation Team: Marcus, Sophia, Chen).
- The Crisis Protocol (handled by Liliane).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-041` | Receipt Chain Guard | CORE PROTOCOL — The cryptographic logging enforcer wrapping every agent execution. |
| Supabase `receipt_chain` | The Audit Ledger | STORAGE — The immutable append-only table housing the chain. |
| The 11 Pi Extensions | The Emitters | INPUT — The programmatic hooks (`InteractComp`, `MemoryFolder`, etc.) that execute the exact receipt writes pre/post generation. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Hash Chains / Blockchain Data Structures** | Haber & Stornetta | 1991 | The mathematical linkage of sequential records. By injecting `Receipt[N-1]`'s hash into `Receipt[N]`, the CCP guarantees chronological lineage and ensures that no rogue agent can silently inject or alter a variable mid-pipeline without irreparably breaking the chain signature. |

### Technical Decisions
1. **Hash Over payload:** The Receipt Chain does not store the massive 4,000-token LLM payload strings in its primary columns (which would bloat the database rapidly). It stores `SHA-256` hashes of those payloads, alongside pointers to the S3/Supabase storage buckets. This keeps the audit queries blazing fast while maintaining cryptographic proof of origin.
2. **Boolean Quarantine Logic:** The Guard does not "try to fix" broken chains. If an agent returns `HTTP 500`, or outputs a string instead of JSON, the `TillDone` extension throws an exception to the Guard. The Guard definitively writes `status: QUARANTINED` to the master session and physically kills the Orchestrator thread.

---

## 4. Implementation Plan

### Stage 1: Genesis Block Creation
*Agent:* Orchestrator (Morgan / Alex / Vidye)
*Inputs:* `Universal_Asset_ID` (`DEP-ENG-040`), `Coach_ID`.
*Outputs:* `Receipt_Block_0`.
*Failure Condition:* Database timeout executing the insert. Orchestrator hangs and aborts session.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Upon initiating any pipeline, the Orchestrator calls `receipt_chain_guard.py::initialize_chain()`.
2. Generates `Receipt_Block_0` containing the `Asset_ID`, session start timestamp, and an empty `previous_receipt_hash` (`"GENESIS"`).
3. Executes a `POST` to the Supabase `receipt_chain` table.
4. Mounts the returned `current_hash` to the active agent environment variables.

### Stage 2: Middle-Node Execution (The Pi Extension Hook)
*Agent:* Any Agent (via Pi Extensions e.g., `InteractComp`, `MemoryFolder`)
*Inputs:* `LLM_Input_Payload`, `LLM_Output_Payload`, `current_hash`.
*Outputs:* `Receipt_Block_N`.
*Failure Condition:* Agent outputs a schema mismatch or times out.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Pre-execution: The Pi Extension captures the `LLM_Input_Payload`.
2. Post-execution: The Pi Extension captures the `LLM_Output_Payload`.
3. Calls `receipt_chain_guard.py::append_receipt()`.
4. The Guard calculates `hash(Input)` and `hash(Output)`.
5. **Resolution Rule (Validation):**
   - If `status_code == 200` AND output passes `TillDone` Pydantic checks: Write `Receipt_Block_N` with `previous_receipt_hash = current_hash`. Return the new hash to the environment.
   - If `status_code != 200` OR output fails schema: Throw `ChainBrokenException`.

### Stage 3: The Quarantine Trigger (Damage Control)
*Agent:* `DamageControl` Extension
*Inputs:* `ChainBrokenException`.
*Outputs:* Session Termination & Alert.
*Failure Condition:* Uncaught exception bleeds the corrupted payload to the next agent in the queue.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. If Stage 2 fails, the `DamageControl` extension catches the exception.
2. It attempts exactly one isolated retry of the specific node.
3. If the retry fails, it invokes `receipt_chain_guard.py::quarantine_chain()`.
4. The Guard executes a global atomic update: `UPDATE pipeline_sessions SET status = 'QUARANTINED' WHERE asset_id = X`.
5. Emits a Telegram webhook to the System Operator defining exactly which agent failed, the exact prompt, and the validation error.

### Stage 4: Publication Gate (The Final Hash Check)
*Agent:* Final Orchestrator Step
*Inputs:* Complete Session Hash Chain.
*Outputs:* `READY_TO_PUBLISH` status flag.
*Failure Condition:* Chain verification reveals a missing step or mismatched hash, blocking publication.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Before writing the finalized artifact (script, image) to the Coach's Notion delivery queue (FR45), the Orchestrator runs `verify_chain_integrity(asset_id)`.
2. The Guard iterates over every receipt in `receipt_chain` for that `asset_id`, summing the hashes recursively from GENESIS to the final node.
3. If the computed final hash matches the active memory hash AND no node reads `QUARANTINED`, it returns `True`. The Orchestrator allows publication.

---

## 5. Primary Output Schema (DEP-ENG-041)

**Schema Name:** `Receipt_Block_N.json` (Mapped to the Supabase Table insert)

```json
{
  "receipt_id": "uuid-7777-8888",
  "asset_id": "JP-CCF-20260312-001-CAROUSEL",
  "timestamp": "2026-03-12T14:32:05Z",
  "executing_agent": "Aria_Synthesizer",
  "pi_extensions_triggered": ["TeamOrchestrator", "MemoryFolder"],
  "mode": "EXECUTION",
  "confidence_score": 0.92,
  "input_payload_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "output_payload_hash": "f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2",
  "previous_receipt_hash": "a4d8c6b3e9f...",
  "current_receipt_hash": "b2f9a7d3c...", 
  "status_code": "SUCCESS"
}
```

---

## 6. Backward Compatibility Fallback
The Receipt Chain Guard is absolute. There is no backward compatibility fallback that allows a pipeline to execute without it. If the `receipt_chain` component fails to reach the Supabase database due to a global network outage, the CCF *must* stall. An undocumented AI generation is considered a critical security violation of ADR-01. The pipeline halts in memory and waits in an exponential back-off loop until database parity is restored.

---

## 7. Tasks

- [ ] **Task 1:** Create the Supabase `receipt_chain` table with an append-only Row Level Security (RLS) policy ensuring no agent can execute an `UPDATE` or `DELETE` on a past receipt.
- [ ] **Task 2:** Write `receipt_chain_guard.py` containing the core cryptographic logic: `initialize_chain()`, `append_receipt()`, `quarantine_chain()`, and `verify_chain_integrity()`.
- [ ] **Task 3:** Embed the `append_receipt()` call natively into the base class for the 11 Pi Extensions, ensuring that every time an agent utilizes an extension, the invocation is logged identically regardless of which pipeline is running.
- [ ] **Task 4:** Refactor the `DamageControl` Python extension to instantly call `quarantine_chain()` on a terminal LLM failure.
- [ ] **Task 5:** Write the Telegram Webhook alert logic for the System Operator when a batch is quarantined.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Cryptographic Linkage):** Execute a 4-step pipeline test. Assert that `Receipt_Block_3.previous_receipt_hash` exactly equals `Receipt_Block_2.current_receipt_hash`. *Failure Example:* The hashes do not match, breaking the linked list and invalidating the audit trail.
- [ ] **AC2 (Immediate Quarantine Enforcement):** Intentionally force an agent to output a malformed payload (e.g., text instead of JSON). Assert that the `DamageControl` extension catches the Pydantic error, writes a `status: QUARANTINED` receipt, and the Orchestrator permanently halts processing of that specific `asset_id`. *Failure Example:* The error is logged, but the Orchestrator ignores it and blindly publishes the malformed text to the Coach's Notion.
- [ ] **AC3 (Final Gate integrity Check):** Manually insert a forged `SUCCESS` receipt into the database targeting the middle of an active session. Trigger `verify_chain_integrity()`. Assert the function returns `False` and halts publication because the forged receipt broke the chronological hash calculation. *Failure Example:* The final gate only checks the very last receipt, allowing maliciously or erroneously injected data to bypass validation.
- [ ] **AC4 (Immutable Storage):** Attempt to execute an `UPDATE` on a previously written `receipt_chain` row using the standard Agent Service Key. Assert the Supabase database returns an HTTP 403 Forbidden due to RLS append-only rules. *Failure Example:* The receipt is successfully altered, destroying the legal auditability of the system.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Supabase `receipt_chain` | Internal | The immutable ledger. Requires strict RLS policies. |
| The 11 Pi Extensions (`DEP-ENG-034`) | Internal | The architectural wrappers that actually execute the Guard calls, removing the responsibility from individual prompts. |
| `id_generator.py` (`DEP-ENG-040`) | Internal | Provides the `Universal_Asset_ID` that binds the Receipt Chain together. |

---

## 10. Testing Strategy

### Unit Tests
- **SHA-256 Determinism:** Pass an identical 4000-word input string to the hashing function twice. Assert the exact same hexadecimal string is generated both times.
- **Verification Loop:** Provide a mocked array of 5 valid receipts. Assert `verify_chain_integrity()` returns `True`. Alter 1 character in Receipt 2's hash. Assert `verify_chain_integrity()` returns `False`.

### Integration Tests
- **The Quarantine Simulation:** 
  1. Trigger a full CCF compilation.
  2. Intercept the network request for Agent 4 and replace it with an HTTP 500 error.
  3. Validate that the Receipt Chain logs the failure.
  4. Validate that the master session state moves to `QUARANTINED`.
  5. Validate that a Telegram alert is dispatched.
  6. Assert that `notion_sync.py` is NEVER called for this asset.

### Safety Tests (ADR-01 Quarantine Security)
- **Data Leakage Check:** After quarantining a batch, trigger the next scheduled CCF asset for the same coach. Assert that the Orchestrator spins up an entirely fresh context window, perfectly insulated from the corrupted context window of the quarantined batch.
