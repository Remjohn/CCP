# Tech-Spec: FR17 — Research Synthesis Protocol (Builder Engine Step 3.5)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0)
**Architecture Reference:** CCP_Evolution_Architecture_Report_V4 §4.2, CRAL_Documentation_V1 §Integration Point 2
**Skill Implementation:** `skills/ccf/compiler/builder-engine-step-3-5/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CRAL_Documentation_V1.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Evolution_Architecture_Report_V4.docx.md`

---

## 2. Overview

### Problem Statement
In previous architecture versions, research synthesis happened implicitly during the final generation step. With the introduction of the CRAL subsystem, the platform receives two distinct streams of high-conviction intelligence: the authenticated coach's voice (`DEP-ENG-010` Source of Context) and the externally validated societal findings (`DEP-ENG-021` CRAL Index). If these two streams produce contradictory structural assertions (e.g., the coach says the mechanism is X, but the CRAL research asserts the societal mechanism is Y), pushing both into the Assembler produces schizophrenic, contradictory content that silently fails the logic test.

### Solution
FR17 implements the **Research Synthesis Protocol (Builder Engine Step 3.5)**. Positioned between DEP resolution (Step 3) and Template Selection (Step 4), this step runs a deterministic conflict-detection pass. Its primary function is to resolve strict proximity hierarchy clashes (e.g., Internal Institutional Evidence outranking External Documentary Evidence) and to surface unresolvable structural mismatches directly to the System Operator before the generation process burns computation on a broken logical scaffold.

### Scope
**In scope:**
- Stage 1: Load and parse `DEP-ENG-021`, `DEP-ENG-010`, and `DEP-ENG-005`.
- Stage 2: Execute the 3 Defined Conflict Detection Types.
- Stage 3: Auto-Resolution Logic (Hierarchical proximity).
- Stage 4: Operator Flagging Logic (Structural contradiction blocking).
- Execution tracking written to `assembly_report.json`.

**Out of scope:**
- Generation Agent logic.
- Template Block B population (Step 5).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-021` | CRAL Finding Index | INPUT — The societal/diagonal research findings. |
| `DEP-ENG-010` | Source of Context (SoC) Batch | INPUT — The coach's authenticated structural language and narrative. |
| `DEP-ENG-005` | Authentication Cerificate | INPUT — The definitive statement of the coach's authenticated result/mechanism. |
| `assembly_report.json` | Assembly Report | OUTPUT — The compilation log containing the `cral_conflict_resolution[]` array, capturing all decisions. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Cognitive Dissonance in Narrative** | Festinger | 1957 | A narrative that contains two structurally opposing pieces of "evidence" without acknowledging the contradiction forces the audience to reject the entire narrative text as unreliable. |
| **Source Proximity Hierarchy** | Various (Journalistic Stds) | - | Internal, primary admissions mathematically outrank external, secondary analysis when claims conflict. |

### Technical Decisions
1. **Deterministic Resolution vs. AI Arbitration:** Conflict Type 1 (Source Proximity) is resolved deterministically based on source location, *not* by asking an LLM which source "feels better".
2. **Operator Flagging (Non-destructive Block):** When a Structural Mismatch (Conflict Type 2 or 3) is found, the pipeline does not delete the entry; it HALTS and places the draft string into a holding queue for human operator review. 
3. **Triggered Execution only:** Step 3.5 only executes if `cral_coverage_status ≠ ABSENT`. If the system is degrading completely to the v1.1 source chain, there is no CRAL index to conflict with.

---

## 4. Implementation Plan

### Stage 1: Dependency Ingestion & Payload Initialization
*Agent Name:* Builder-Engine-Logic-Core
*Inputs:* `DEP-ENG-021`, `DEP-ENG-010`, `DEP-ENG-005`.
*Outputs:* Normalized working memory objects state.
*Failure Condition:* Null objects returned on required tier dependencies.

**Steps:**
1. Check `cral_coverage_status`. If `ABSENT`, write standard skip event to `assembly_report` and proceed to Step 4.
2. Load all 3 input objects into the working memory of the protocol agent.
3. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-1-STEP35-INIT',
  agent_name: 'Builder-Engine-Logic-Core',
  timestamp }

### Stage 2: Type 1 Conflict Pass (Source Proximity)
*Agent Name:* Builder-Engine-Logic-Core
*Inputs:* `DEP-ENG-021[M2_BELIEVABLE]`, `DEP-ENG-021[M6_IRREFUTABLE]`.
*Outputs:* `resolution_decision` object.
*Failure Condition:* Agent hallucination failing to recognize hierarchical source tags.

**Logic Gate:**
- **Trigger:** M2 (External Documentary Evidence) and M6 (Internal Institutional Evidence) make contradictory claims regarding the same base mechanism.
- **Verdict: PASS (Auto-Resolve):** The protocol strictly enforces the hierarchy. M6 (Internal source) overrides M2 (External source). 
- **Consequence:** The Builder forces the M6 finding as the canonical mechanism evidence. Appends decision to `cral_conflict_resolution[]`.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-2-TYPE-1-CONFLICT',
  agent_name: 'Builder-Engine-Logic-Core',
  timestamp }

### Stage 3: Type 2 Conflict Pass (Structural Mismatch)
*Agent Name:* Builder-Engine-Logic-Core
*Inputs:* `DEP-ENG-021[M4_RESONANT]`, `DEP-ENG-010` (SoC).
*Outputs:* `resolution_decision` object.
*Failure Condition:* Fails to detect an explicitly contrarian statement in the SoC payload compared to the CRAL narrative.

**Logic Gate:**
- **Trigger:** The M4 CRAL narrative unit and the DEP-ENG-010 authentic voice passage represent fundamentally differing mechanism trajectories.
- **Verdict: PROVISIONAL (Flag):** Ensure CRAL M4 provides the evidentiary structure, and SoC provides authentic voice. However, if the root mechanism differs materially (e.g., M4 describes a systemic failure; SoC describes a personal mindset failure), the agent FLAGS the conflict.
- **Consequence:** Do NOT auto-resolve. Place the session in the `Operator_Conflict_Queue`. Block until cleared by human operator.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-3-TYPE-2-CONFLICT',
  agent_name: 'Builder-Engine-Logic-Core',
  timestamp }

### Stage 4: Type 3 Conflict Pass (Authenticity Conflict)
*Agent Name:* Builder-Engine-Logic-Core
*Inputs:* `DEP-ENG-021[M6_IRREFUTABLE]`, `DEP-ENG-005` (Trigger Certificate).
*Outputs:* `resolution_decision` OR Terminate Signal.
*Failure Condition:* Fails to issue terminal halt when societal research contradicts the coach's authenticated reality.

**Logic Gate:**
- **Trigger:** M6 Irrefutable evidence directly contradicts the coach's documented result inside `DEP-ENG-005`.
- **Verdict: FAIL (Terminal Block):** M6 cannot contradict the coach's authenticated result from the ingestion phase.
- **Consequence:** Hard Block. Return `conflict_type_3 + resolution_instruction` to Phase 1. Do not proceed to Step 4 (Template Selection). Appends the halt command log to `assembly_report.json`.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-4-TYPE-3-CONFLICT',
  agent_name: 'Builder-Engine-Logic-Core',
  timestamp }

---

## 5. Primary Output Schema (Assembly Report Extension)

The Research Synthesis Protocol outputs its decisions explicitly into the existing `assembly_report.json` for compilation auditing.

**Schema Context:** `assembly_report -> cral_conflict_resolution`

```json
{
  "cral_conflict_resolution": [
    {
      "conflict_type": "TYPE_1_PROXIMITY",
      "status": "AUTO_RESOLVED",
      "details": "M2 (News Article) asserted mechanism A; M6 (Whistleblower Memo) asserted derivative mechanism A1. M6 overrides M2 based on internal proximity precedence.",
      "action_taken": "M6 forced as primary evidentiary anchor for script template.",
      "receipt_hash": "step35_t1_d92e..."
    },
    {
      "conflict_type": "TYPE_2_STRUCTURAL",
      "status": "FLAGGED_FOR_OPERATOR",
      "details": "M4 CRAL finding emphasizes structural debt as root cause. SoC DEP-ENG-010 emphasizes poor leadership mindset as root cause.",
      "action_taken": "Execution Halted. Placed in Operator Resolution Queue ID: REQ-3921",
      "receipt_hash": "step35_t2_f088..."
    }
  ],
  "step_35_status": "PENDING_OPERATOR_CLEARANCE"
}
```

---

## 6. Backward Compatibility Fallback
If the entire step fails to load due to module timeouts, the pipeline assumes a hyper-conservative stance: It treats this as an **ABSENT CRAL State** (`cral_coverage_status = ABSENT`).
1. It ignores `DEP-ENG-021`.
2. It falls back to the V1.1 source chain (relying entirely on `DEP-ENG-010` and generation-time intelligence mapping).
3. The resulting content will be flagged as `CRAL_DEGRADED` to notify the operator that societal depth was skipped.

---

## 7. Tasks

- [ ] **Task 1:** Inject the `Step 3.5 Protocol` hook directly into the Phase 1 Builder Engine execution path, directly following the Psychological Routing Brief generation.
- [ ] **Task 2:** Build the Hierarchy Logic module handling the deterministic Type 1 Conflict auto-resolution (Internal M6 > External M2).
- [ ] **Task 3:** Implement the LLM-assisted semantic diffing module required for Type 2 and Type 3 to determine whether the mechanisms in the arrays are semantically misaligned.
- [ ] **Task 4:** Construct the `Operator_Conflict_Queue` webhook and dashboard interface to allow operators to clear or override PROVISIONAL/FAIL flags.
- [ ] **Task 5:** Inject Receipt Chain Guard writes across all stages, ensuring every operator intervention or automated block is cryptographically logged.

---

## 8. Acceptance Criteria

- [ ] **AC1 (M6 vs M2 Hierarchy Overrule):** Provided M2 data indicating a mechanism of "High Interest Rates" (Forbes article) and M6 data indicating "Credit Score Manipulation Algorithmic Throttling" (Leaked bank memo), the protocol deterministically selects the M6 vector without raising an operator flag. *Failure Example:* The system presents both conflicting points in the output, forcing the generation agent to synthesize an impossible hybrid.
- [ ] **AC2 (SoC Voice vs CRAL Narrative):** Provided an SoC stating "discipline is the only tool you need" and an M4 finding stating "biological reality dictates discipline fails without physiological support," the system detects the semantic collision and halts with `FLAGGED_FOR_OPERATOR`. *Failure Example:* The system assumes CRAL overrides the coach and generates a script contradicting the coach's explicit fundamental belief.
- [ ] **AC3 (Authenticity Terminal Block):** Provided an M6 finding that states "This diet protocol has a 0% success rate," but the `DEP-ENG-005` Authentication Certificate carries the coach's authenticated claim of a "100% success rate," the protocol issues a `Terminal Block` (Type 3). *Failure Example:* The Builder Engine attempts to flag it for operator manual repair instead of throwing the mandated terminal error back to Phase 1.
- [ ] **AC4 (Skip on Degraded State):** If `cral_coverage_status == ABSENT` is detected, Step 3.5 completes execution in under 20ms and logs the skip code in the assembly report. *Failure Example:* The system crashes attempting to parse a null `DEP-ENG-021` index.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-021` | Upstream | Must be fully assembled by Orchestrator before this step fires. |
| `DEP-ENG-010` | Upstream | Authentic voice source material. |
| `DEP-ENG-005` | Upstream | Definitive truth anchor. |
| `Operator Dashboard` | System | UI layer required to display `FLAGGED_FOR_OPERATOR` statuses to humans. |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Proximity Logic Sorting:** Pass a mocked `DEP-ENG-021` payload with explicitly contradicting strings into M2 and M6 variables. Assert the script forces the M6 string into the resolved variable.
- **Null Safety Check:** Pass `{ "cral_coverage_status": "ABSENT" }`. Assert the function returns immediately with consequence `skip_step_3_5` without throwing errors on missing array keys.

### Integration Tests
- **The Type 2 Operator Flag Pipeline:** Push a functionally contradicting `DEP-ENG-010` and `DEP-ENG-021[M4]` payload through the Builder Engine. Assert that the builder pauses execution and correctly issues the webhook payload to the Operator Dashboard API containing the exact `REQ-ID` correlation.
- **The Operator Override Loop:** Using the paused state from the previous test, send a synthetic POST request simulating the operator selecting "Override: Force CRAL" as the resolution. Assert the pipeline resumes execution and correctly updates the `cral_conflict_resolution` log entry from `FLAGGED` to `RESOLVED_BY_OPERATOR`.

### Safety Tests (ADR-01 & Receipt Isolation)
- **Dependency Sandboxing:** Run Step 3.5. Ensure the LLM semantic diffing prompt contains strict instructions that it must only evaluate the objects provided within the isolated context payload, explicitly preventing it from accessing external LLM parametric knowledge to resolve the collision.
