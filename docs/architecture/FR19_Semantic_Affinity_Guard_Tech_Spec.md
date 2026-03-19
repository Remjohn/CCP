# Tech-Spec: FR19 — Semantic Affinity Guard Protocol (DEP-PROTO-011)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.0 / Mood State Architecture v1.0)
**Architecture Reference:** Mood_State_Architecture_Documentation §Section 05, CCP_Evolution_Architecture_Report_V3
**Skill Implementation:** `skills/ccf/compiler/semantic-affinity-guard/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Mood_State_Architecture_Documentation.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Evolution_Architecture_Report_V3.docx.md`

---

## 2. Overview

### Problem Statement
A highly frequent content failure occurs when a brilliantly executed low-arousal ("relaxing") piece of content is deployed to a high-stress audience segment, but the *topic* of the piece is exactly the domain causing their anxiety. For example, a career coach posting an insightful joke about workplace burnout to an audience currently exhausted by workplace burnout. The piece fails to relieve stress—it adds to the semantic load. The system historically lacked a mechanism to block this specific misalignment.

### Solution
FR19 implements the **Semantic Affinity Guard Protocol (DEP-PROTO-011)**. Operating as an inescapable "stealth kill switch," it executes during the batch-finalization check (specifically at Gate C-06 before compilation). It maps the audience's active L3 Pain Domain against every single piece slotted for **Escape Mode**. If it flags a `HIGH` semantic affinity (i.e., the content's domain perfectly matches the audience's pain domain), it forcefully blocks the deployment. It is mathematically impossible for the compiler to produce Escape Mode content with a `HIGH` semantic affinity rating. 

### Scope
**In scope:**
- Stage 1: Batch slot and Context Premise ingestion.
- Stage 2: NLP Domain Mapping (Content Domain vs L3 Pain Domain).
- Stage 3: Enforcement of the C-06 Block Logic.
- Cryptographic Receipt Chain Guard checks at each transition.

**Out of scope:**
- Trigger Authentication.
- Assembly routing for non-Escape modes (Processing, Status, Discovery allow medium/high affinity contexts).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-006` | Context Premise (Pain Map) | INPUT — Provides the L1/L2/L3 stratified client pain landscape (the domain they are currently suffering in). |
| `batch_metadata` | Batch Composer Slot | INPUT — The intended content target and Mood Mode. |
| `DEP-PROTO-011` | Semantic Affinity Guard | ENFORCER — The strict blocking logic protocol itself. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Mood Management Theory (Semantic Affinity)** | Zillmann | 1988 | High semantic affinity between a media piece's domain and the user's active stress domain actively prevents mood repair and heightens anxiety. To successfully execute mood repair/escape, the semantic domains must strongly diverge. |

### Technical Decisions
1. **Escape Mode Exclusivity:** This protocol is purely targeted at Escape Mode. Processing Mode demands `HIGH` affinity (facing the pain directly). Status Mode and Discovery Mode can tolerate `MEDIUM`. Only Escape Mode collapses under `HIGH` affinity.
2. **Terminal C-06 Gate:** The C-06 gate physically halts the compiler if a HIGH affinity Escape slot is detected. Bypassing this block is intentionally unsupported. The System Operator must select a domain swap or reclassify the content entirely.
3. **Ghost Variable Prevention Gate:** All input sources [DEP-ID] must be verified cryptographically prior to payload unpacking. Any field resolving to NULL or UNDEFINED triggers a hard compiler pipeline halt. The error schema emitted is: `{ "error": "DAG_VIOLATION", "missing_dep": "[DEP-ID]" }`

---

## 4. Implementation Plan

### Stage 1: Batch Composition & Payload Ingestion
*Agent Name:* Batch-Finalization-Core
*Inputs:* Compiled `batch_metadata` (including `mood_state`), `DEP-ENG-006` (Pain Map).
*Outputs:* Normalized textual domain clusters.
*Failure Condition:* Null pain map provided for targeted isolated coach.

**Steps:**
1. Fetch the proposed batch allocation parameters for the active tenant.
2. Isolate all array items tagged with `mood_state: "Escape"`.
3. Extract the active L3 pain domain narrative from `DEP-ENG-006` Output 1.
4. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-1-SA-INGEST',
  agent_name: 'Batch-Finalization-Core',
  timestamp }

### Stage 2: Cross-Reference Affinity Module
*Agent Name:* Semantic-Distance-Analyzer
*Inputs:* Content working domain string, L3 Pain Domain string.
*Outputs:* `affinity_score_enum` array per batch item.
*Failure Condition:* Fails to detect strong synonym correlation between the pain and the topic.

**Logic Gate:**
- **Trigger:** Evaluate the vector distance between the proposed Escape content's conceptual domain and the audience's active pain domain.
- **Verdict: LOW:** Target topics sit in entirely separate domains. (e.g., Pain = Corporate Hustle; Target = Golf). -> `Proceed`
- **Verdict: MEDIUM:** Target topics are adjacent logically but functionally distinct. (e.g., Pain = Management; Target = Public Speaking). -> `Flag for Operator Review` (Warns of friction).
- **Verdict: HIGH:** Target topics share the exact L3 semantic vocabulary field. (e.g., Pain = Overwhelm; Target = Wellness routine exhaustion). -> `Hard Block`
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-2-AFFINITY-ANALYSIS',
  agent_name: 'Semantic-Distance-Analyzer',
  timestamp }

### Stage 3: Enforcement Gate C-06
*Agent Name:* Batch-Finalization-Core
*Inputs:* `affinity_score_enum`.
*Outputs:* `batch_compilation_clearance` or `fatal_compilation_error`.
*Failure Condition:* System proceeds to compile a `HIGH` affinity Escape slot.

**Steps:**
1. Evaluate validation array returned by Stage 2.
2. If `HIGH` in any Escape slot -> Invoke C-06 Terminal Error. Abort compilation.
3. Emit `c-06_kill_switch_trigger_event` to the System Operator Dashboard displaying two mandated resolution paths:
   - `Resolution A:` Mutate template (reframe hook using domain swapping to a distant semantic field).
   - `Resolution B:` Reclassify template as `Processing Mode` (where high affinity is productive). **When the operator selects this reclassification, the pipeline rewinds automatically. FR18 re-executes with the new mode classification. No operator intervention is required beyond the initial reclassification click in the console.**
4. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-3-ENFORCE',
  agent_name: 'Batch-Finalization-Core',
  timestamp }

### Stage 4: Post-Assembly Re-Evaluation
**Dual-Stage Evaluation Protocol:**
The Semantic Affinity Guard MUST execute twice for all content mapped to Target Mood: ESCAPE.
1. **Pre-Flight (Tier 0):** Evaluates baseline topic affinity against Neo4j L3 Context Premises.
2. **Post-Assembly (Tier 3 Post-Flight):** Evaluates the fully compiled output string, accounting for any newly injected `DEP-ENG-021` (CRAL) findings or real-time Neo4j shifts that occurred during batch processing. If Stage 2 trips the guard, the script is quarantined.

---

## 5. Primary Output Schema (DEP-PROTO-011 Log Execution)

The guard yields an execution object that determines whether the design brief compiler unlocks or halts.

**Schema Name:** `semantic_affinity_clearance.json`

```json
{
  "protocol_id": "DEP-PROTO-011",
  "receipt_chain_hash": "sa_guard_f73ad...",
  "tenant_id": "coach_88ab",
  "active_l3_pain_domain": "Systemic workplace exhaustion and imposter syndrome",
  "batch_evaluation": [
    {
      "slot_id": 1,
      "intended_mode": "Escape",
      "content_domain": "Fitness supplement absurdities",
      "affinity_rating": "LOW",
      "c06_clearance": "PASS"
    },
    {
      "slot_id": 2,
      "intended_mode": "Escape",
      "content_domain": "Corporate email sign-offs causing stress",
      "affinity_rating": "HIGH",
      "c06_clearance": "FAIL_TERMINAL"
    }
  ],
  "batch_clearance_status": "BLOCKED"
}
```

---

## 6. Backward Compatibility Fallback
This guard serves as a kill switch prioritizing audience safety over output velocity. Consequently, **no automated fallback exists that allows a HIGH rating to bypass C-06.**
If the NLP Domain Mapping module crashes (API outage), the system will treat all Escape slots as `PROVISIONAL_MEDIUM` and throw them to the System Operator queue for manual visual clearance, ensuring `HIGH` affinity content never slips through by default.

---

## 7. Tasks

- [ ] **Task 1:** Implement the NLP Semantic Distance calculation to reliably parse and compare domain distance rather than simple keyword matches (accounting for synonyms).
- [ ] **Task 2:** Update the Builder Engine execution array to prepend `C-06 Semantic Affinity Guard` immediately before the final compilation lock.
- [ ] **Task 3:** Implement the execution loop for Stage 3 routing that intercepts a `HIGH` block and formats the specific UI payload presenting the structural mutation options to the operator.
- [ ] **Task 4:** Add explicit handling for `MEDIUM` affinity, treating it as an Operator Queue flag rather than a terminal kill.
- [ ] **Task 5:** Inject Receipt Chain Guard writes across all stages enforcing ADR-01 Coach Graph constraints, guaranteeing `DEP-ENG-006` pain maps are queried strictly per isolated tenant.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Hard Block Priority):** If an Escape Mode slot evaluates to `HIGH` semantic affinity, the engine throws a terminal compiling error at C-06 and explicitly refuses to compile the brief. *Failure Example:* The system recognizes `HIGH` affinity and logs a warning but proceeds to compile the Design Brief anyway.
- [ ] **AC2 (Processing Pass Through):** If a `Processing Mode` slot evaluates to `HIGH` semantic affinity against the same Pain Map, the engine ignores it and allows C-06 clearance. *Failure Example:* The system applies the stealth kill switch universally across all mood states, halting the entire pipeline whenever the coach speaks to their core trigger.
- [ ] **AC3 (Medium Review Flag):** If a slot evaluates to `MEDIUM` affinity, the system pauses compilation and pushes the task to the Operator Dashboard for manual validation. *Failure Example:* The system assumes `MEDIUM` is acceptable and auto-merges it without human oversight.
- [ ] **AC4 (ADR-01 Strict Isolation):** During the cross-referencing process, the agent must fetch the context Pain Map exclusively from the targeted tenant database. *Failure Example:* The guard compares the batch against a globally aggregated L3 pain map, hallucinating risks that don't belong to the coach's direct audience.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-006` (Pain Map) | Upstream | Required baseline for the exclusion calculation. |
| `batch_metadata` | Upstream | Provides the `mood_state` labels for calculation inclusion. |
| Design Brief Compiler | Downstream | Target consumer that honors the generated `C-06` block. |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Zillmann Evaluation Metric:** Submit an exact duplicate string for both the Pain Map and the Target Domain tagged `Escape`. Assert that the evaluation engine deterministically outputs `HIGH` and strictly raises the `FAIL_TERMINAL` block.
- **Exclusion Mapping:** Submit the identical `HIGH` payload but re-tag the input mode as `Processing`. Assert the C-06 Gate completely bypasses the check and outputs `PASS`.

### Integration Tests
- **Terminal Execution Halt:** Trigger a `HIGH` flag through a simulated Batch Composer workflow run. Assert that the resulting `.catch()` or event listener captures the `c-06_kill_switch_trigger_event`, permanently halting execution prior to invoking the assembler adapters.
- **Fail-Safe Fallback:** Disconnect the NLP evaluation vector DB and execute a standard pipeline check. Assert that the system accurately degrades to a `PROVISIONAL_MEDIUM` state, refusing to pass an Escape Mode content piece without explicit operator override.

### Safety Tests (ADR-01 & Receipt Isolation)
- **Tenant Context Bleed Check:** Provide Coach A and Coach B with radically different Pain Maps. Evaluate a batch from Coach B using Coach A's content. Validate that the system only computes distances based on Coach B's active `.json` contexts without bleeding into A's domain constraints.
