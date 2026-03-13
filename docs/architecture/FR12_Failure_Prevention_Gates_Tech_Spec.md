# Tech-Spec: FR12 — Three Failure Prevention Gates

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.1)
**Architecture Reference:** §Context_Premise_Trigger_Matching_Layer Part 4, Component 3
**Skill Implementation:** `skills/ccf/production/failure-prevention-gates/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were read and absorbed prior to formulating this specification:
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Context_Premise_Trigger_Matching_Layer.md`
- `d:\Work\The Conscious Coaching Factory\lab\Context Premises\Audience Reconsolidation and Content Impact.md`
- `d:\Work\The Conscious Coaching Factory\lab\Context Premises\Verified L3 Data Through Digital Ethnography.md`
- `d:\Work\The Conscious Coaching Factory\lab\Trigger Map Flow\Memory Retrieval vs. Semantic Construction.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR10_Four_Axis_Structural_Matching_Engine_Tech_Spec.md` (Self-reference)
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR11_Activation_Event_Seed_Construction_Tech_Spec.md` (Self-reference)

---

## 2. Overview

### Problem Statement
The Trigger-First Engine aligns coach Emotional DNA with audience L3 pain, but the fidelity of this match degrades through three specific operational drift vectors:  
1. **Structural Decay:** The system finds partial thematic overlap and proceeds as if it is structural congruence ("Adjacent matching"). This produces content that the audience agrees with intellectually but does not feel recognized by emotionally.  
2. **Linguistic Abstraction:** The system successfully extracts L3 tribal language but an intermediate LLM prompt rewrites it into generic, normalized professional coaching phrasing. This strips the sub-cortical recognition signal (the "2am test") from the activation event.  
3. **Temporal Misalignment / Data Opaqueness:** The coach produces the Voice Note, but the system cannot diagnose *why* it failed. A structurally "perfect" match might fail because the coach is actually experiencing live trauma (pre-PTG) instead of resolved integration (post-PTG), or because the audience data was L2 masquerading as L3.

### Solution
FR12 establishes the **Three Failure Prevention Gates** as an independent validation micro-service intercepting the output of the Four-Axis Structural Matching Engine (FR10) and Activation Event Seed Construction (FR11). 
- **Gate 1 (Adjacent vs. Congruent):** Ensures exactly 4 of 4 axes align on a match matrix.
- **Gate 2 (Language Drift Prevention):** Enforces a rigid ≥3 verified L3 tribal keyword minimum constraint against the generated prompt strings.
- **Gate 3 (Authenticity Score Feedback Loop):** Uses the LIWC-22 algorithm on the output of the Telegram Elicitation Protocol to diagnostically score the resulting resonance and implement automatic parameter correction for both the coach and audience profiles.

### Scope
**In scope:**
- Gate 1 processing of the `DEP-ENG-010` (Four-Axis Match Object).
- Gate 2 lexical analysis on `DEP-ENG-011` (Activation Event Seed).
- Gate 3 integration with the `DEP-ENG-019` (Session Transcript Intelligence).
- Dynamic error resolution protocols for PASS/FAIL/PROVISIONAL verdicts.
- Receipt Chain Guard logging for auditable trace provenance.
- Enforcement of ADR-01 Coach Isolation constraints on all feedback mechanisms.

**Out of scope:**
- The creation of the Initial Four-Axis match (FR10).
- The formulation logic of the DARN-CAT prompt (FR11).
- The Telegram bot infrastructure.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-010` | Four-Axis Match Object | INPUT — Produced by FR10 |
| `DEP-ENG-011` | Activation Event Seed | INPUT — Produced by FR11 |
| `DEP-ENG-019` | Session Transcript Intelligence | INPUT — Produced by FR2 (Sacred Audio Ingestion) via LIWC-22 scoring pipeline |
| [PROPOSED] `DEP-ENG-027` | Gate Diagnostic Certificate | OUTPUT — A formal, auditable JSON manifest documenting the PASS/FAIL matrices for the three gates |
| `DEP-LIB-002` | Trigger Map | OUTPUT (Target) — Gate 3 initiates updates to coach `ptg_status` |
| `DEP-ENG-006` | Context Premise Map | OUTPUT (Target) — Gate 3 initiates validation flags on audience segment definitions |

*Note: `DEP-ENG-027` (Gate Diagnostic Certificate) has no existing DEP-ID and is PROPOSED. Proceeding under the assumption that this object must be registered within the pipeline payload architecture.*

### Academic Grounding

| Algorithm / Gate | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Gate 1 - Common Ground Alignment** | Clark & Brennan | 1991 | **Grounding in Communication:** Communication fails when the structural foundations (appraisal + moral) are only "adjacent." Explicit 1:1 mapping across all axes is required to achieve shared ground. |
| **Gate 2 - Sub-cortical Language Signal** | Pennebaker | 2022 | **Linguistic Inquiry and Word Count (LIWC):** Authentic emotional resonance requires specific, non-abstracted linguistic markers. Genericizing vocabulary shifts audience processing from affective (sub-cortical) to cognitive (cortical). |
| **Gate 3 - Dual-Layer Encoding Verification** | Tedeschi & Calhoun | 2004 | **Post-Traumatic Growth:** Successful PTG retains the original trauma network alongside the resolution network. A low authenticity score on a "resolved" trigger indicates live trauma (incomplete dual-layer encoding). |
| **Gate 3 - Episodic vs. Semantic Masking** | Conway | 2005 | **Self-Memory System (SMS):** When L2 data masquerades as L3, or when triggers lack ESK anchors, the brain defaults to semantic synthesis. LIWC-22 algorithms detect this shift in physiological language markers. |

### Technical Decisions
1. **Gate 1 is Binary:** 3.5/4 is categorized as STRONG but still fundamentally requires a manual over-ride or a specific programmatic path. Anything ≤ 2.5 is hard-rejected as ADJACENT. There is no partial pass.
2. **Gate 2 uses Exact Match Regex + Lemmatization:** To prevent trivial matching errors, the 3 tribal terms must be lemmatized using spaCy before comparison, but abstract synonyms are strictly forbidden. It must be their exact *tribal* term root.
3. **ADR-01 Coach Isolation Explicit Enforcement:** Gate 3 updates the Coach's Trigger Map (DEP-LIB-002). At no point does the coach's failure profile map into the general audience database, and the audience data does not mutate the coach's core biographical history. They are isolated.

---

## 4. Implementation Plan

### Stage 1: Pipeline Ingestion & Receipt Initialization
*Agent Name:* Gatekeeper-Orchestrator
*Inputs:* `DEP-ENG-010` (Four-Axis Match Object), `DEP-ENG-011` (Activation Event Seed).
*Outputs:* Receipt ID initialization.
*Failure Condition:* Missing `DEP-ENG-010` or `DEP-ENG-011` schemas.

**Steps:**
1. Ingest payload from FR11 pipeline queue.
2. Verify schema compliance of `DEP-ENG-010` and `DEP-ENG-011`.
3. Generate a global validation session ID.
4. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-1-INGEST',
  agent_name: 'Gatekeeper-Orchestrator',
  timestamp }

### Stage 2: Gate 1 — Adjacent vs. Congruent Validation
*Agent Name:* Structural-Congruence-Validator
*Inputs:* `DEP-ENG-010` (Four-Axis Match Scores).
*Outputs:* `gate_1_verdict` (Boolean/Enum).
*Failure Condition:* Score array sum < 3.0. Axis score array contains a 0.0 value.

**Gate Logic:**
- **Exact Threshold:** `sum(axis_scores) ≥ 3.5` AND `min(axis_scores) > 0.0`.
- **Verdict: PASS:** All axes > 0.0, total sum ≥ 3.5. Proceed to Gate 2.
- **Verdict: PROVISIONAL:** Total sum = 3.0, but all axes > 0.0 (one axis is partial, none are NONE). Downstream: Proceed to Gate 2 with `flag_adjacent_monitor=true`.
- **Verdict: FAIL:** Any axis = 0.0 OR total sum < 3.0. Downstream: Abort. Log as ADJACENT. Reject payload back to FR10 orchestrator queue for logging.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-2-GATE-1',
  agent_name: 'Structural-Congruence-Validator',
  timestamp }

### Stage 3: Gate 2 — Language Drift Prevention
*Agent Name:* Lexical-Authenticity-Validator
*Inputs:* `DEP-ENG-011` (Activation Event Seed prompt text), FR9 verified tribal terms registry.
*Outputs:* `gate_2_verdict`, `matched_terms[]`.
*Failure Condition:* Less than 3 verified terms mathematically present in the prompt string.

**Gate Logic:**
- **Exact Threshold:** `len(matched_terms) ≥ 3`.
- **Verdict: PASS:** ≥ 3 matching terms found via lemmatized checking. Proceed to Emit.
- **Verdict: PROVISIONAL:** 2 terms found. Downstream: Flag `language_drift_warning`, proceed to Emit, but flag for Review in admin dashboard.
- **Verdict: FAIL:** 0 or 1 terms found. Downstream: Abort. Payload rejected back to FR11 Prompt generator explicitly demanding the missing keywords.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-3-GATE-2',
  agent_name: 'Lexical-Authenticity-Validator',
  timestamp }

### Stage 4: Emit Cleared Seed
*Agent Name:* Gatekeeper-Orchestrator
*Inputs:* `gate_1_verdict`, `gate_2_verdict`.
*Outputs:* [PROPOSED] `DEP-ENG-027` (Gate Diagnostic Certificate) affixed to `DEP-ENG-011`.
*Failure Condition:* Any verdict = FAIL.

**Steps:**
1. Package the specific Gate 1 and Gate 2 results into the `DEP-ENG-027` object.
2. Affix the certificate to the seed payload.
3. Transmit to Telegram Elicitation Protocol.
4. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-4-EMIT',
  agent_name: 'Gatekeeper-Orchestrator',
  timestamp }

### Stage 5: Gate 3 — Authenticity Score Feedback Loop (Post-Recording Async)
*Agent Name:* Temporal-Reconsolidation-Auditor
*Inputs:* `DEP-ENG-019` (Session Transcript Intelligence carrying LIWC-22 score), `DEP-ENG-027` (Gate Diagnostic Certificate).
*Outputs:* Mutated `DEP-LIB-002` (ptg_status update), Mutated `DEP-ENG-006` (FR9 Validation flag).
*Failure Condition:* Missing LIWC-22 score in `DEP-ENG-019`.

*ADR-01 Coach Isolation Explicit Constraint:* Gate 3 operates strictly within isolated state silos. The coach's `DEP-LIB-002` trigger mapping file is mutated exclusively within the coach's local storage zone. The audience's `DEP-ENG-006` map validation flags are mutated within the audience intelligence store. No bi-directional data leakage occurs.

**Gate Logic:**
- **Trigger:** Webhook received from Telegram pipeline that `DEP-ENG-019` transcript is parsed and scored via LIWC-22.
- **Exact Thresholds:** LIWC-22 Authenticity Score (Range: 0-10).
- **Verdict: PASS:** Score ≥ 7.0. Downstream: Increase trigger activation precedence matrix score by 15% in `DEP-LIB-002`.
- **Verdict: PROVISIONAL:** Score 5.0 - 6.9. Downstream: Flag ESK anchor as potentially degraded. Schedule specific coach interview question generation.
- **Verdict: FAIL (Coach Temporal Error):** Score < 5.0 AND `DEP-ENG-027` proves Gate 1 and Gate 2 were PASS. AND historical trigger performance indicates decay. Downstream: Re-categorize coach's trigger in `DEP-LIB-002` from `resolved_dual_layer` to `active_processing` (Live trauma).
- **Verdict: FAIL (Audience Extraction Error):** Score < 5.0 AND `DEP-ENG-027` proves Gate 1 and Gate 2 were PASS. AND historical trigger performance is flawless. Downstream: L2 masquerading as L3. Flag specific audience segment within `DEP-ENG-006` requiring immediate re-validation of the "2am test".
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-5-GATE-3',
  agent_name: 'Temporal-Reconsolidation-Auditor',
  timestamp }

---

## 5. Primary Output Schema (DEP-ENG-027 - PROPOSED)

**Schema Name:** `gate_diagnostic_certificate.json`

```json
{
  "gate_certificate_id": "CERT-88192-AABB",
  "seed_reference_id": "SEED-financial_shame-trig_44-seg_1",
  "timestamp": "2026-03-13T14:32:00Z",
  "receipt_chain_hash": "a4fddbf91823ab...",
  "gate_1_structural_congruence": {
    "verdict": "PASS",
    "total_score": 4.0,
    "axis_matrix": {
      "moral_foundation": 1.0,
      "coping_potential": 1.0,
      "agency_attribution": 1.0,
      "temporal_position": 1.0
    },
    "adjacent_flag": false
  },
  "gate_2_language_drift": {
    "verdict": "PASS",
    "required_count": 3,
    "actual_count": 4,
    "matched_terms_lemmatized": [
      "hustle guilt",
      "algorithm tax",
      "shadow_ban",
      "engagement_prison"
    ],
    "language_drift_warning": false
  },
  "gate_3_authenticity_feedback": {
    "status": "AWAITING_TELEGRAM_PAYLOAD",
    "liwc_22_score_received": null,
    "verdict": null,
    "downstream_mutations": {
      "dep_lib_002_mutated": false,
      "dep_eng_006_mutated": false
    }
  }
}
```

---

## 6. Backward Compatibility Fallback
If the entire matching system fails, or the payload queue is perpetually failing at Gate 1 or Gate 2 without resolution (e.g., 3 consecutive regenerations rejected by Gate 2):
1. Write a `system_fallback_invoked` state to the pipeline monitor.
2. Emit a structured, explicit notification to the Telegram Elicitation Protocol requesting a default, overarching "General Event" check-in instead of a Four-Axis structural prompt. 
3. This prevents deadlocks where the coach receives zero messages on their scheduled cadence by reverting to generic check-in logic completely bypassing FR10/FR11.

---

## 7. Tasks

- [ ] **Task 1:** Implement Receipt Chain Guard interface for the `skills/ccf/production/failure-prevention-gates/SKILL.md` orchestrator to generate hashes at Stages 1, 2, 3, 4, and 5.
- [ ] **Task 2:** Implement Gate 1 mathematical parsing. Build the schema validation for `DEP-ENG-010` and implement the strict `sum ≥ 3.5` and `min > 0.0` logic. Return binary PASS, PROVISIONAL, or FAIL routing flags.
- [ ] **Task 3:** Implement Gate 2 Lexical Analysis. Integrate spaCy lemmatization pipeline to extract the root of the input string and compare against the FR9 keyword array. Implement the `>=3` counting logic and loopback rejection trigger.
- [ ] **Task 4:** Register `DEP-ENG-027` (Gate Diagnostic Certificate) in the central schema repository and implement serialization of the JSON payload.
- [ ] **Task 5:** Implement Gate 3 `DEP-ENG-019` Webhook Receiver. Parse incoming LIWC-22 scores asynchronously.
- [ ] **Task 6:** Implement Gate 3 Coach Mutation rules (ADR-01 Context). Write logic to transition `resolved_dual_layer` to `active_processing` when score < 5.0. Secure under Coach-DB silo.
- [ ] **Task 7:** Implement Gate 3 Audience Mutation rules (ADR-01 Context). Write logic to set `revalidate_l3_flag: true` in `DEP-ENG-006` when score < 5.0. Secure under Audience-DB silo.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Gate 1 Rejection):** If a `DEP-ENG-010` object sum is 3.0, but one axis is strictly 0.0 (e.g., [1.0, 1.0, 1.0, 0.0]), Gate 1 returns a `FAIL` verdict and halts the pipeline immediately. *Failure Example Implementation:* Pipeline passes a [1.0, 1.0, 1.0, 0.0] array through, emitting the seed incorrectly.
- [ ] **AC2 (Gate 2 Minimum String Compliance):** If the input seed text contains precisely 2 lemmatized matches against the FR9 registry, the system must set `verdict: PROVISIONAL` and append `language_drift_warning: true` to the Certificate. *Failure Example Implementation:* Prompt containing 2 matches halts the queue instead of passing provisionally, or passes without appending the critical warning flag. 
- [ ] **AC3 (Receipt Chain Integrity):** The log structure must contain 5 explicit hashes verifying the payload state across phases (Init, Gate 1, Gate 2, Emit, Gate 3). *Failure Example Implementation:* A generated `gate_diagnostic_certificate.json` has a null value for `receipt_chain_hash`.
- [ ] **AC4 (Gate 3 Coach Retrograde):** When a session transcript (`DEP-ENG-019`) returns a LIWC-22 score of 4.2 for a supposedly `resolved_dual_layer` trigger that has underperformed twice previously, the system mutates the Coach's `DEP-LIB-002` replacing the status with `active_processing`. *Failure Example Implementation:* Score of 4.2 logged, but the Trigger Map PTG state retains `resolved_dual_layer`, indicating the feedback loop broke.
- [ ] **AC5 (ADR-01 Silo Verification):** The Gate 3 mutation routines utilize strictly isolated memory pointers; Audience mutation functions cannot legally access Coach object references. *Failure Example Implementation:* A bug in the coach downgrade logic accidentally writes a coach's live-trauma status note into an audience's L3 hidden belief array.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-010` Match Object | Upstream | Produced by FR10. Required for Gate 1 evaluation. |
| `DEP-ENG-011` Activation Seed | Upstream | Produced by FR11. Required for Gate 2 evaluation. |
| LIWC-22 API Data | Upstream | Produced by FR2 via `DEP-ENG-019`. Evaluated externally, handed to this engine. |
| spaCy Python Module | System | Required for lemmatizing the Gate 2 Lexical check efficiently. |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Generates exact provenance signatures for execution integrity. |

---

## 10. Testing Strategy

### Unit Tests
- **Gate 1 Logic Check:** Inject synthetic arrays: `[1.0, 1.0, 1.0, 1.0]` (Expect PASS), `[1.0, 1.0, 0.5, 0.5]` (Expect PROVISIONAL), `[1.0, 1.0, 1.0, 0.0]` (Expect FAIL).
- **Gate 2 String Logic Analysis:** Pass text: `"We hate the system."` with dictionary: `["system", "algorithm", "tax"]`. Detected = 1. Expect FAIL. Pass text: `"The algorithm system feels like a tax."` Detected = 3. Expect PASS.
- **Coach Silo Mutation Logic:** Ensure `mutate_coach_ptg_status(trigger_id, new_status)` does not accept arguments pertaining to a `theme_slug` or segment.

### Integration Tests
- **Full Fallback Invocation Test:** Force Gate 2 to FAIL 3 times in a row by hard-coding a mock LLM prompt return of missing data. Verify that the orchestrator captures the limit, outputs `system_fallback_invoked`, and pushes the generic "General Event" check-in payload instead of failing silently.
- **Webhook E2E Receipt Loop:** Simulate the Telegram bot pinging the Gate 3 Webhook with a mocked JSON containing `liwc_score: 8.5`. Verify that `DEP-ENG-027` updates locally and the Receipt Chain Guard successfully records `GATE-3-VERDICT`.

### Safety Tests (ADR-01)
- **Isolation Breach Simulation:** Attempt to execute an audience dictionary update procedure within the execution context bounds of the `Temporal-Reconsolidation-Auditor` operating on an isolated coach thread. Assure that an immediate memory-access denial or explicit scope Error is thrown preventing structural intermingling.
