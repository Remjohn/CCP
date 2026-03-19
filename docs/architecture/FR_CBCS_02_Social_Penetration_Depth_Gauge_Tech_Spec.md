# FR-CBCS-02: Social Penetration Depth Gauge — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F2, PRD §FR-CBCS-02

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Standard CRMs send campaigns based on behavioral triggers (clicked an email, tagged with "lead"). They fail to measure whether reaching the client feels transactional or intimate, resulting in premature commercial outreach that damages the therapeutic relationship.

### Solution
The Social Penetration Depth Gauge measures the actual quality of the psychological relationship via the `spt-stage-classifier`. It computes the client's current penetration stage (from Orientation down to Stable Exchange) by analyzing the client's continuous Voice DNA disclosure markers. It pairs this depth with mood and coping status to form an un-bypassable delivery permission gate.

### Scope
**In scope:**
- Computations mapping LIWC-22 outputs to the 4 Social Penetration Theory (SPT) stages.
- Storage of the depth score in the `social_penetration_depth_gauge` system.
- Execution of the `spt-stage-classifier` and `Delivery Permission Gate`.
- Integration with Voice DNA Client Profiler (`voice_dna_client_profiler.py`).

**Out of scope:**
- The actual Voice DNA Client processing of raw voice messages (handled directly by Voice DNA subsystem).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `social_penetration_depth_gauge` | State SQL Table | Stores client SPT stage, history | FR-CBCS-02 | FR53, FR55 |
| `client_disclosure_voice_profiles` | Stateful SQL Trace | Voice-DNA markers | Voice DNA Client | FR-CBCS-02 |
| `PROPOSED: DEP-ENG-055` | Triple-Condition Delivery Gate | Hard stop logic payload | FR-CBCS-02 | CCF Campaigns |

### Academic Grounding
- **Research Paper:** *Social Penetration: The Development of Interpersonal Relationships* (Altman & Taylor, 1973) + *Self-Disclosure and Liking: A Meta-Analytic Review* (Collins & Miller, 1994).
- **Mechanism:** Relationships deepen via reciprocal self-disclosure ("onion model"). Depth drives psychological attachment. Passing the Affective Exchange threshold signals attachment is verified.

### Technical Decisions
- **Storage:** Depth gauges are persisted in `social_penetration_depth_gauge` Supabase table and updated on a weekly sweep via `spt_stage_engine.py`.
- **Triple-Condition Gate:** No campaign can fire unless 3 variables independently pass, ensuring deep, multi-dimensional safety. The evaluator tool `delivery_gate_evaluator.py` is called synchronously on campaign trigger requests.

---

## 4. Implementation Plan

### Stage 1: Social Penetration Classification
- **Agent:** `spt-stage-classifier` (Python computation executed during weekly swept updates)
- **Inputs:** 
  - `client_disclosure_voice_profiles` (DEP-ID: `DEP-ENG-003` / `DEP-ENG-004` — Produced By: FR3 Voice DNA Extraction)
- **Outputs:** Database row insertion/update in `social_penetration_depth_gauge`
- **Failure Condition:** If there is zero data in `client_disclosure_voice_profiles` for a specific client, catching a `KeyError`, the algorithm safely defaults the client to `(1) Orientation` via fallback assignment. DB write completes. No false elevations.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + computed `spt_stage` written to the APM log upon successful weekly computation.
- **ADR-01 Isolation Constraint:** The classifier processes records explicitly executing `WHERE coach_id = auth.uid()` to enforce strict multi-tenant boundary isolation.

### Stage 2: Variable Resolution Rules (Exact Input Conditions)
The following rules determine exactly how the ENUM values for `spt_stage` (1-4) are computed during Stage 1 from the 14-day trailing average of LIWC markers:

- **(1) Orientation**: Evaluates `True` IF `liwc_scores.first_person_freq < 0.05` AND `liwc_scores.emotional_complexity < 0.2`.
- **(2) Exploratory Affective**: Evaluates `True` IF `liwc_scores.first_person_freq >= 0.05` AND `liwc_scores.emotional_complexity >= 0.2`.
- **(3) Affective Exchange**: Evaluates `True` IF `liwc_scores.exclusive_words > 0.1` AND `liwc_scores.hedging_words < 0.05` + meets `Exploratory Affective` baseline.
- **(4) Stable Exchange**: Evaluates `True` IF `liwc_scores.cognitive_processes > 0.15` + meets `Affective Exchange` baseline sustained over a trailing 30-day window instead of 14-day.

### Stage 3: Triple-Condition Delivery Gate 
- **Agent:** `IntelligenceGateRouter` (Pi Extension logic layer)
- **Inputs:** 
  - `spt_stage` (DEP-ID: `social_penetration_depth_gauge` — Produced By: FR-CBCS-02)
  - `mood_state` (DEP-ID: `DEP-ENG-018` — Produced By: FR18 CRAL)
  - `coping_position` (DEP-ID: `information_coping_trajectory` — Produced By: FR-CBCS-04)
- **Outputs:** `PROPOSED: DEP-ENG-055` (Delivery Permission Gate Payload - Pass/Fail matrix).

**Quality Gate:** **The Delivery Permission Gate**
- **Triggered when:** Campaign Generator FR53/FR55 requests dispatch permission.
- **Exact Thresholds:**
  - **Condition 1:** `spt_stage >= 3`
  - **Condition 2:** `mood_state NOT IN ('Processing', 'Tension', 'Escape')`
  - **Condition 3:** `coping_position >= 3`
- **Verdict - PASS:** All 3 conditions evaluate to `True`. *Downstream Consequence:* Campaign dispatch permitted; execution passes to FR53 queue.
- **Verdict - PROVISIONAL:** Condition 1 and 3 are `True`, but Condition 2 (Mood) evaluates `False`. *Downstream Consequence:* Yields to a 24-hour sleep delay in the FR53 queue, to see if the transient mood spike settles before abandoning the entire sequence loop. Re-evaluated tomorrow.
- **Verdict - FAIL:** Condition 1 or Condition 3 evaluates to `False`. *Downstream Consequence:* Campaign is held indefinitely. Operator notified of blocking condition via payload `blocking_reason`.

### Stage 4: Resolution Rules for Output Schema
Every field in the `DeliveryPermissionGateEval` schema is populated via the following exact logic:
- `gate_id`: Generated via `uuid.uuid4()` at instantiation.
- `client_id`: Passed synchronously from the parent campaign trigger payload.
- `coach_id`: Extracted via DB relation constraint linked to `client_id`.
- `spt_condition`: Computed as Boolean cast: `social_penetration_depth_gauge.spt_stage >= 3`.
- `mood_condition`: Computed as Boolean cast: `DEP-ENG-018.mood_state NOT IN [...]`.
- `coping_condition`: Computed as Boolean cast: `information_coping_trajectory.position >= 3`.
- `all_passed`: `(spt_condition == True AND mood_condition == True AND coping_condition == True)`.
- `blocking_reason`: An array populated by string pushes: `['SPT_FAILED']` if `spt_condition == False`, etc.
- `last_evaluated`: UTC string populated by Python `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type DeliveryPermissionGateEval = {
  gate_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  spt_condition: boolean; 
  mood_condition: boolean; 
  coping_condition: boolean; 
  all_passed: boolean; 
  blocking_reason: string[]; // Resolution exactly matches False conditions
  last_evaluated: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For active clients already in campaigns who never generated sufficient Voice DNA to reach `Affective Exchange`:
- They will inherit `spt_stage = 1` from the Stage 1 failure condition.
- The `IntelligenceGateRouter` will evaluate `Condition 1 = False`, triggering a `FAIL` verdict.
- System operator will receive alerts on "Campaigns Held" due to SPT depth deficits. 
- Coaches will need to engage Deep Disclosure Protocol (FR-CBCS-10) to migrate the client properly.

---

## 7. Tasks
- [ ] **Task 1: Weekly Stage Engine** - Implement `spt_stage_engine.py` using NumPy pandas filtering to track trailing 14-day and 30-day LIWC threshold crossings mapping the exact Stage 1-4 logic.
- [ ] **Task 2: Supabase Storage** - Create `social_penetration_depth_gauge` and `delivery_permission_gates` tables under ADR-01 RLS schemas isolating constraints to `coach_id = auth.uid()`.
- [ ] **Task 3: IntelligenceGateRouter** - Write the `delivery_gate_evaluator.py` logic tracking the `PASS / PROVISIONAL / FAIL` sequence branching constraints synchronously against live campaign dispatch events.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Gate Enforcement):** Requesting permission for a `client_id` with `spt_stage = 3`, `coping_position = 4`, but `mood_state = Processing` MUST evaluate to a `PROVISIONAL` verdict, queueing a 24-hr delay. **Failure Example:** The CRM module dispatches a $3k product blindly to a client actively grieving a loss because they are mechanically in stage 3.
- [ ] **AC2 (Safe Defaults / Handling undefined):** An evaluation requested where `client_disclosure_voice_profiles` does not exist MUST trigger the Stage 1 fallback returning `(1) Orientation`, chaining to a `Condition 1` `False` evaluating immediately to a `FAIL` verdict. **Failure Example:** An empty payload parses as `null` math resulting in a `TypeError: > cannot be compared with null` crashing the campaign router entirely.
- [ ] **AC3 (Operator Visibility Resolution):** A `FAIL` verdict executed via Condition 3 returning `False` MUST append exactly the string `'COPING_FAILED'` into `blocking_reason` array in the database payload. **Failure Example:** The campaign fails silently leaving the operator thinking the system crashed with an empty array.

---

## 9. Dependencies
| Dependency | Type | Notes |
|---|---|---|
| Voice DNA Client | Internal Upstream | Derives the actual `client_disclosure_voice_profiles` |
| FR18 CRAL | Internal Upstream | Provides `mood_state` |
| FR-CBCS-04 ICT Mapper | Internal Upstream | Provides `coping_position` |
| Campaign Orchestrator (FR59) | Internal Downstream | Halts execution if gate blocks |

---

## 10. Testing Strategy

### Unit Testing
- Mock `client_disclosure_voice_profiles` data containing `liwc_scores.exclusive_words = 0.01` and `liwc_scores.first_person_freq = 0.01`. Assert the `spt_stage_engine.py` executes the Variable Resolution Rule evaluating to `Orientation` (Stage 1).
- Mock `liwc_scores.exclusive_words = 0.12` and assert it crosses the Stage 3 rule evaluating to `Affective Exchange`.

### Integration Testing
- Inject a synthetic campaign trigger for a valid client (`Stage 3`, `Mood = Discovery`, `Coping = 4`). Ensure the `IntelligenceGateRouter` returns `all_passed: true` and writes the audit log containing the `gate_id` hash output.

### Safety Testing
- Drop the `mood_state` row entirely for an active client and execute a gate check. The system must degrade gracefully catching the `KeyError` mapping to an implicit `FAIL` condition with no stack traces breaking the queue.
