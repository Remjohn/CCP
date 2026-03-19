# FR55: Session Booking Intelligence — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §FR55

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`

---

## 2. Overview

### Problem Statement
Standard CRMs trigger "book a call" prompts based on arbitrary digital actions (e.g., "Client clicked 3 links"). These actions demonstrate curiosity, not psychological readiness. Pushing a high-ticket sales call on a client operating in Coping Position 2 causes friction that destroys the relationship. Booking logic must be grounded in multi-dimensional psychological convergence.

### Solution
The Session Booking Intelligence module acts as the highest-tier conversion guard. It never autonomously books a call. Instead, it continuously monitors 4 specific CBCS metric arrays. When all four signals converge indicating peak psychological readiness, it synthesizes a comprehensive briefing for the human Operator, recommending exact timing and offer tiers for a 1:1 engagement.

### Scope
**In scope:**
- The `convergence-detector` background script calculating the 4-signal matrix.
- The `Booking Readiness Gate` driving recommendation limits.
- The compiled Operator Brief JSON payload (`DEP-ENG-076`).

**Out of scope:**
- Calendar scheduling links (handled by external Calendly/Stripe integrations).
- Autonomous sending (Operator MUST click approve).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-076` | Operator Booking Brief | Human-facing Intel Summary | FR55 | Operator Dashboard |

### Academic Grounding
- **Mechanism:** Utilizing Signal Detection Theory, the system filters out the "noise" of passive engagement. By demanding the simultaneous convergence of Intimacy (TII), Vulnerability (SPT), Capacity (ICT), and Receptivity (SEARCH), it effectively zeros out the False Positive rate for high-ticket pitches, preventing brand burnout.

### Key Files
- `convergence-detector.py` (Script managing cron and multi-table Joins)
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **Human-in-the-loop Mandate:** FR55 generates *recommendations*, never autonomous actions. High-ticket 1:1 boundaries strictly require operator intuitive confirmation.
- **ADR-01 Isolation:** The aggregation of coping trajectories and intimacy models is the most sensitive data in the CCP. All computations run at the tenant (`coach_id`) execution level.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (4-Signal Convergence Matrix)
- **Agent:** `convergence-detector`
- **Inputs:** 
  - `information_coping_trajectory` (DEP-ID: `information_coping_trajectory` — Produced By: FR-CBCS-04)
  - `spt_stage` (DEP-ID: `social_penetration_depth_gauge` — Produced By: FR-CBCS-02)
  - `search_phase_status` (DEP-ID: `search_phase_detections` — Produced By: FR-CBCS-06)
  - `composite_tii` (DEP-ID: `telegram_intimacy_index` — Produced By: FR-CBCS-07)
- **Outputs:**
  - `recommendation_status` (Enum string) and `confidence_score` (Float).
- **Failure Condition:** Missing any of the 4 requisite arrays returns null default tracking, enforcing baseline safety exclusion.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `confidence_score_calc` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Convergence Score):** The system resolves the `confidence_score_calc` explicitly mapping to exact boundary limits across 4 vectors:
- **"HIGH_CONFIDENCE_READY"**: Evaluates `True` IF `coping_trajectory >= 4` AND `spt_stage >= 3` AND `search_phase_status == 'CONFIRMED'` AND `composite_tii >= 0.4`. *Calculation:* `confidence_score = 1.0`.
- **"WATCHLIST_BUILDING"**: Evaluates `True` IF `coping_trajectory >= 3` AND `spt_stage >= 3` AND `composite_tii >= 0.3`. (SEARCH Phase CONFIRMED is not strictly required). *Calculation:* `confidence_score = 0.6`.

### Stage 2: Quality Gate Extension
- **Agent:** `convergence-detector`
- **Inputs:** Generated `recommendation_status` Enum from Stage 1.
- **Outputs:** `OperatorBookingBriefRow` (JSON Array, DEP-ENG-076).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `briefing_id` logged. **(Mandatory Execution)**.
- **Failure Condition:** Score math = 0.

**Quality Gate:** **The Booking Readiness Gate**
- **Triggered when:** The background chron completes its sweep evaluating `recommendation_status`.
- **Exact Thresholds:** Evaluates the generated Enum string precisely.
- **Verdict - PASS:** Enum == `"HIGH_CONFIDENCE_READY"`. *Downstream Consequence:* Detailed Operator Brief is compiled. Pushed to UI Dashboard's `Priority Actions` list. Sets `gate_verdict = PASS`.
- **Verdict - PROVISIONAL:** Enum == `"WATCHLIST_BUILDING"`. *Downstream Consequence:* Client is placed silently on an operator monitoring dashboard. No push alerts fired. Sets `gate_verdict = PROVISIONAL_WATCHLIST`.
- **Verdict - FAIL:** ANY metric falls below "Watchlist" thresholds. *Downstream Consequence:* Client completely stripped from commercial consideration. Pipeline halted, returning `gate_verdict = FAIL_NURTURE_MODE`. Does not output JSON rows to dashboard table.

### Phase 3: Field-by-Field Schema Mapping
Every field in the JSON specifies exact origin metrics:
- `briefing_id`: Returns `uuid.uuid4()`.
- `client_id`: Returns string mapping to prospect context.
- `coach_id`: Returns `auth.uid()` from request enforcing ADR-01 bound.
- `recommendation_status`: Returns Stage 1 mapped Enum ("HIGH_CONFIDENCE_READY" | "WATCHLIST_BUILDING" | "NOT_READY").
- `confidence_score_calc`: Returns Float exactly calculating Stage 1 scores (1.0 | 0.6 | 0.0).
- `gate_verdict`: Returns String mapped by Stage 2 thresholds ("PASS" | "PROVISIONAL_WATCHLIST" | "FAIL_NURTURE_MODE").
- `qualifying_metrics.tii_snapshot`: Returns numeric Float pull of `composite_tii`.
- `qualifying_metrics.spt_snapshot`: Returns Integer numeric pull of `spt_stage`.
- `evaluated_at`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OperatorBookingBriefRow (DEP-ENG-076)",
  "type": "object",
  "properties": {
    "briefing_id": { "type": "string", "format": "uuid" },
    "client_id": { "type": "string" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "recommendation_status": { "type": "string", "enum": ["HIGH_CONFIDENCE_READY", "WATCHLIST_BUILDING", "NOT_READY"] },
    "confidence_score_calc": { "type": "number", "minimum": 0, "maximum": 1.0 },
    "gate_verdict": { "type": "string", "enum": ["PASS", "PROVISIONAL_WATCHLIST", "FAIL_NURTURE_MODE"] },
    "qualifying_metrics": {
      "type": "object",
      "properties": {
        "tii_snapshot": { "type": "number" },
        "spt_snapshot": { "type": "integer" },
        "search_confirmed": { "type": "boolean" },
        "coping_tier": { "type": "integer" }
      }
    },
    "evaluated_at": { "type": "string", "format": "date-time" }
  },
  "required": [
    "briefing_id", "client_id", "coach_id", "recommendation_status",
    "confidence_score_calc", "gate_verdict", "qualifying_metrics", "evaluated_at"
  ]
}
```

---

## 6. Backward Compatibility Fallback
For legacy leads stored in generic CRM tag systems devoid of psychological markers:
The `convergence-detector` will resolve `null` for all 4 query dependencies. Math computes to `0.0`, resulting in universally applied `FAIL_NURTURE_MODE`. The system legally cannot recommend a high-ticket booking parameter without verified psychological transparency parameters tracking minimum relational boundaries.

---

## 7. Tasks
- [ ] Task 1: Write the massive `INNER JOIN` SQL cron statement grouping 4 required parameters across their distinct Supabase tables keyed on `client_id`.
- [ ] Task 2: Build Python logic block strictly hard-coding `<, >, ==` logical comparators assigning `Score = 1.0` ONLY when exactly matching the FR55 Stage 1 parameter specs.
- [ ] Task 3: Plumb Receipt Chain API logger into the script, specifically hashing the `qualifying_metrics` array to construct the permanent audit trail backing the call recommendation.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Convergence Requirement):** Client has `coping = 4`, `spt = 4`, `tii = 0.9` BUT `search_phase_status = PENDING`. Gate MUST evaluate `PROVISIONAL_WATCHLIST`. **Failure Example:** Triggers aggressive high-ticket meeting ping based purely on relationship depth, ignoring the critical fact that client isn't actively looking for solution intervention.
- [ ] **AC2 (Provisional UI Silence):** Script evaluates a client to `WATCHLIST_BUILDING`. The Row MUST insert successfully to Supabase but trigger exactly 0 push notifications via Notification endpoint. **Failure Example:** Operator phone buzzes 45 times a week with "Maybe Ready" alerts causing notification fatigue.
- [ ] **AC3 (Valid Pass Logging):** A `PASS` computation MUST record explicitly all 4 elements inside `qualifying_metrics` mapping precise array states at evaluation time. **Failure Example:** System records `tii_snapshot = null` due to async lookup errors, leaving Operator blind to intelligence logic.

---

## 9. Dependencies
- **Upstream:**
  - `FR-CBCS-02`: SPT Stage Integer (`social_penetration_depth_gauge`).
  - `FR-CBCS-04`: Coping Trajectory (`information_coping_trajectory`).
  - `FR-CBCS-06`: Search Phase Status (`search_phase_detections`).
  - `FR-CBCS-07`: TII Score (`telegram_intimacy_index`).
- **Downstream:**
  - Operator UI App Dashboard (NextJS).
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.
  - Cron scheduling execution worker.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Four_Point_Convergence_Boolean`: Inject mock payload `{"coping":5, "spt":3, "search":"CONFIRMED", "tii":0.8}`. Assert Python boundary logic outputs `HIGH_CONFIDENCE_READY` with `confidence = 1.0`. Set `search` to `PENDING`. Assert fall back to `WATCHLIST_BUILDING` with `confidence = 0.6`.
- `Test_Fail_Nurture_Bound`: Inject mock payload `{"coping":1, "spt":2}`. Assert logic skips watchlist entirely, terminating on logic layer 3 for `FAIL_NURTURE_MODE`.

### Integration Tests
- `Test_Cron_Supabase_Join`: Execute `convergence-detector` pointing to a mock table ID containing 5 users. Verify `SQL JOIN` returns accurate row metrics combining the 4 upstream DEP-IDs without generating duplicates or dropping relations.

### Safety / Isolation Tests
- `Test_Autonomous_Execution_Blocker`: Attempt to execute the webhook call creating a calendly invite natively inside the script based on a `1.0` array match. Assert absence of module. Assert module exists explicitly to output a String Array brief only, never initiating outbound actions to enforce the non-negotiable "Operator trigger" rule.
