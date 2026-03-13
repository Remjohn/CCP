# Tech-Spec: FR26 — Validation Team Gate (DEP-PROTO-016)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §8.2.3 (Validation Team Gate), Architecture_Synthesis_Report
**Skill Implementation:** `research/critic/`, `orchestration/ccf-validate/`
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
In automated high-volume content production, unchecked LLM drift is inevitable. Structural errors, regression to generic AI "slop" (template bleed), and tonal homogenization consistently degrade output quality over time. Without an unforgiving pre-distribution quality gate, these degraded assets pollute the public feed, eroding the coach’s authentic voice and violating the 30-Day Movement Season strategy.

### Solution
FR26 formalizes the **Validation Team Gate (DEP-PROTO-016)**—a stringent, triple-pass architectural boundary executed by three distinct agents: Sophia (Soul Validator), Marcus (Protocol Validator), and Chen (Mimicry Validator). Every generated draft must pass all three checkpoints simultaneously. If a draft fails at any gate, it is canonically classified as a `<FAIL>` and instantly routed to the `TillDone` rewrite cycle. The system does not allow partial scores or "silent failures."

### Scope
**In scope:**
- Stage 1: Sophia's TTT Drift Detection (<15% deviation).
- Stage 2: Marcus's Structural Compliance Check (100% match against the active 30-Day Season).
- Stage 3: Chen's Mimicry/AI Detection (<5% artifact threshold).
- Stage 4: `TillDone` Extension routing and batch quarantine rules.

**Out of scope:**
- Modifying the coach's `coach_soul.json` base DNA (the validators only read it as a baseline).
- Generating the drafts (this protocol strictly evaluates existing output).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Concept | Name | Role in This Pipeline |
|---|---|---|
| `DEP-PROTO-016` | Validation Team Gate | LOGIC — Overarching rule set for the triple-pass QA check. |
| Sophia | Soul Validator | AGENT — Measures TTT alignment against `coach_soul.json`. |
| Marcus | Protocol Validator | AGENT — Enforces the 30-Day Movement Season mandate. |
| Chen | Mimicry Validator | AGENT — Detects generalized AI boilerplate. |
| `coach_soul.json` | Voice/Soul Baseline | INPUT — Contains the TTT metrics used by Sophia. |
| `CURRENT_SEASON_MANDATE` | Movement Season State | INPUT — The environmental state (e.g., *The Forge*, *The Tribe*) Marcus enforces. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Stylometry Discrimination** | - | - | Computational classification of authorship bases authenticity on the statistical variance of specific vocabulary use, sentence length, and pacing. Sophia employs these exact stylometric principles to measure TTT drift against the biological baseline. |

### Technical Decisions
1. **Unforgiving Binary Rejection:** To guarantee absolute quality, the system does not average scores. A draft that scores perfectly with Sophia and Marcus but fails Chen’s mimicry check is rejected entirely. 
2. **Contextual 30-Day Seasons:** Marcus does not evaluate generic "good structure." He evaluates against 1 of 4 rotational mandates (`Deconstruction`, `The Forge`, `The Mirror`, `The Tribe`). A script that is technically flawless but uses "Tribe" connection rhetoric during a "Deconstruction" season will fail.

---

## 4. Implementation Plan

### Stage 1: Sophia — Soul Validation (TTT Drift)
*Agent Name:* Sophia
*Inputs:* `draft_v1.md`, `coach_soul.json`
*Outputs:* `sophia_validation.json` (PASS/FAIL)
*Failure Condition:* TTT divergence exceeds 15% from the biological baseline.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'SOUL-VALIDATION',
  agent_name: 'Sophia',
  timestamp }

**Steps:**
1. Sophia ingests the draft and the coach’s baseline `coach_soul.json` (specifically the Temperature, Tone, and Temperament metrics).
2. Sophia calculates the TTT score of the generated draft using the same extraction algorithm employed during Genesis.
3. Calculate Delta: If `Abs(Draft_Score - Baseline_Score) > 15%` → `<FAIL>`.
4. If `<FAIL>`, Sophia generates precisely worded negative constraints for the rewrite (e.g., *"Temperament is too placid. Inject the coach's inherent urgency."*).

### Stage 2: Marcus — Protocol Validation (30-Day Season)
*Agent Name:* Marcus
*Inputs:* `draft_v1.md`, `CURRENT_SEASON_MANDATE` env config.
*Outputs:* `marcus_validation.json` (PASS/FAIL)
*Failure Condition:* Structural/Thematic compliance is `<100%`.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PROTOCOL-VALIDATION',
  agent_name: 'Marcus',
  timestamp }

**Steps:**
1. Marcus checks the `CURRENT_SEASON_MANDATE` state variable.
2. Example states/requirements:
   - **Deconstruction:** Must challenge false beliefs.
   - **The Forge:** Must require hard actionable steps.
   - **The Mirror:** Must focus on introspective storytelling.
   - **The Tribe:** Must focus on community and "We" language.
3. If the script relies on a mandate outside the active season, Marcus throws `<FAIL>`.
4. Marcus generates structural rewrite constraints (e.g., *"Convert the generic advice list into an actionable 'Forge' discipline set."*).

### Stage 3: Chen — Mimicry Validation (AI Artifacts)
*Agent Name:* Chen
*Inputs:* `draft_v1.md`
*Outputs:* `chen_validation.json` (PASS/FAIL)
*Failure Condition:* Detected AI artifact likelihood is `>5%`.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'MIMICRY-VALIDATION',
  agent_name: 'Chen',
  timestamp }

**Steps:**
1. Chen runs the draft against a proprietary zero-shot classification matrix scanning for:
   - "Crucial," "vital," "navigating," "in today's busy world."
   - Symmetrical transition sentences (template bleed).
   - Unnaturally balanced paragraph lengths.
2. If `Artifact_Score > 0.05` → `<FAIL>`.
3. Chen outputs the specific flagged AI phrasing responsible for the failure to guide the rewrite.

### Stage 4: Orchestration Routing (The TillDone Loop)
*Agent Name:* Master Orchestrator (Alex)
*Inputs:* The 3 validation JSONs.
*Outputs:* Approved Script OR `TillDone` Rewrite payload.
*Failure Condition:* On 3 failed TillDone iterations: The slot is NOT dropped. The orchestrator invokes the FR24 Stage 3C Reference Template Fallback Protocol. The batch slot is fulfilled with a fingerprinted reference template. generation_status is set to REFERENCE_FALLBACK. Batch count is maintained at 36. # REVISED: Handled 3 failure threshold with Reference protocol
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'ORCHESTRATION-ROUTING',
  agent_name: 'Master-Orchestrator-Alex',
  timestamp }

**Steps:**
1. Alex aggregates the scores. `If (Sophia == PASS) AND (Marcus == PASS) AND (Chen == PASS) -> APPROVE`.
2. If ANY validator throws `<FAIL>`, Alex merges all the *Negative Constraints* from the failed checks into a single prompt injection.
3. Alex invokes the `TillDone` extension, handing the failed draft back to `ccf-generate` (Script Artisan).
4. **Retry Loop:** Max 3 attempts.

---

## 5. Primary Output Schema (Validation Report)

**Schema Name:** `validation_report.json`

```json
{
  "script_id": "OUT-STORY01-EMI-20260317-004",
  "validation_timestamp": "2026-03-17T08:30:00Z",
  "final_verdict": "FAIL_TRIGGER_REWRITE",
  "iteration_count": 1,
  "validators": {
    "sophia_soul": {
      "status": "PASS",
      "ttt_drift_percentage": 0.08,
      "feedback": null
    },
    "marcus_protocol": {
      "status": "PASS",
      "active_season": "THE_FORGE",
      "compliance": 1.0,
      "feedback": null
    },
    "chen_mimicry": {
      "status": "FAIL",
      "artifact_score": 0.12,
      "feedback": "Template Bleed Detected. Remove the symmetrical transition sentence 'But here's the crucial thing' and the term 'navigating'."
    }
  },
  "till_done_payload": "Rewrite Required. Chen [Mimicry_Violation]: Remove the symmetrical transition sentence 'But here's the crucial thing' and the term 'navigating'."
}
```

---

## 6. Backward Compatibility Fallback
The `ccf-validate` script assumes the presence of all 3 agents. However, if the `coach_soul.json` base file is corrupted or unreadable, Sophia cannot baseline the TTT scores. The orchestrator catches the file exception, logs `[SOPHIA_BASELINE_MISSING]`, automatically flags Sophia's pass as `<PROVISIONAL_PASS>` (thus avoiding an infinite block loop), but throws a high-priority Discord alert to the engineering team forcing a `ccf-soul-extract` rerun. Marcus and Chen operate independently of the Voice DNA and will execute normally.

---

## 7. Tasks

- [ ] **Task 1:** Build Sophia's `ttt-drift-detector` script leveraging the original Genesis extraction algorithm to compare the generation output against `coach_soul.json`.
- [ ] **Task 2:** Build Marcus's `season-mandate-checker`. It must dynamically pull `CURRENT_SEASON_MANDATE` and evaluate the script's psychological center of gravity against the matching enum requirements.
- [ ] **Task 3:** Implement Chen's zero-shot artifact scoring matrix, supplying a heavy penalty dictionary of common AI idioms.
- [ ] **Task 4:** Wire the `ccf-validate` command logic to aggregate the 3 results, enforce the `AND` pass logic, and trigger the `TillDone` rewrite cycle.
- [ ] **Task 5:** Enforce ADR-01 variables ensure Sophia only loads the correct coach's Voice DNA during batch executions.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The Unforgiving Gate):** A drafted script returns `Sophia: PASS`, `Marcus: PASS`, `Chen: FAIL`. The orchestrator immediately rejects the script and triggers `TillDone`. *Failure Example:* The orchestrator uses a "best 2 out of 3" vote and incorrectly lets the AI-slop script leak into generation.
- [ ] **AC2 (TTT Drift Threshold):** Sophia evaluates a script at a `16%` deviation from the baseline. The script fails. *Failure Example:* The math rounding algorithm drops the `16%` check to a `10%` bin and incorrectly yields a pass.
- [ ] **AC3 (Season Mandate Flip):** The environment variable is flipped from `THE_FORGE` to `THE_MIRROR`. A hard-hitting discipline script passes Sophia and Chen, but Marcus immediately throws `<FAIL>` with instructions to convert the advice into introspective narrative storytelling. *Failure Example:* Marcus ignores the env flag and passes the script because the structure is technically sound for a listicle.
- [ ] **AC4 (ADR-01 Isolation):** Sophia validates a batch for Coach A. The system explicitly verifies it is loading `coach_soul_A.json` and not `coach_soul_B.json`. *Failure Example:* A thread-leak causes Sophia to cross-validate Coach A's draft against Coach B's TTT baseline, rejecting the entire perfect batch because she thinks the voice is wrong.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `coach_soul.json` | Upstream | Required for Sophia's baseline. |
| `CURRENT_SEASON_MANDATE` | Upstream Config | Global configuration dictating the 30-Day behavioral strategy. |
| `TillDone` Extension | Downstream | Handles the rewrite invocation and negative constraint prompting. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Chen's Matrix Test:** Feed Chen 10 human-written scripts and 10 raw ChatGPT-4 scripts. Assert that Chen successfully detects artificial transitions and flags all 10 AI scripts `>0.05` while passing the 10 human scripts.
- **Season Swap Test:** Supply an introspective narrative. Evaluate it with `THE_MIRROR` env state. Assert `PASS`. Manually swap the state to `DECONSTRUCTION` and evaluate the identical script. Assert `FAIL`.

### Integration Tests
- **TillDone Integration Sync:** Feed a intentionally bad draft down the pipeline. Monitor the `ccf-validate` terminal output. Assert that the script is flagged `<FAIL>`, the negative constraints are successfully parsed into a JSON, and the `TillDone` orchestrator accurately hands the feedback payload back to the Script Artisan.
- **Max Iteration Burnout:** Deliberately break the LLM's prompt parameters so it refuses to fix the draft. Ensure that after 3 iterations, Alex cleanly drops the corrupted draft from the `weekly_production_batch` array and continues without taking down the server.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Context Bleed Check:** Initiate simultaneous batch validation runs for Coach A and Coach B. Verify that Sophia securely mounts the tenant-specific file path when evaluating the biological baseline. Assert zero cross-contamination.
