# FR56: Campaign Performance Registry — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §FR56

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`

---

## 2. Overview

### Problem Statement
Standard analytics dashboards track vanity metrics (conversion rate, click-throughs) but fail to explain *why* a conversion happened. Knowing a campaign converted at 8% provides zero instructional value. We must know the psychological state of the 8% who converted versus the 92% who did not, in order to train the Content Generation algorithms recursively.

### Solution
The Campaign Performance Registry (FR56) acts as the data ingestion backbone mapping commercial outcomes backwards into pre-existing psychological states. It logs exactly *where* a client was located psychologically (Coping position, SPT depth, Intimacy score) at the exact moment the campaign launched. It tracks their subsequent outcome, generating the empirical feedback loop validating or invalidating the system's targeting theories.

### Scope
**In scope:**
- The `campaign-performance-logger` script parsing Stripe/Telegram generic outcome webhooks.
- Explicit Schema definition mapping 9 specific variables to `.jsonb`.
- The `Registry Completeness Gate` ensuring no orphaned variables.

**Out of scope:**
- Generating the actual Campaign (handled by FR59).
- Generating the Loom Report output (handled by FR60).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `DEP-ENG-051` | Campaign Performance Registry | Core system feedback memory | FR56 | FR60 / FR43 |

### Academic Grounding
- **Mechanism:** Operant Conditioning. A system cannot improve unless the reward function (Conversions) tightly correlates to initial stimuli context (The psychological combination). By recording all variables synchronously, machine-learning regression computes efficacy accurately.

### Key Files
- `campaign_performance_logger.py` (Parser and DB insertion script)
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **T_Minus_1 Trailing Math:** The true indicator of psychological targeting logic relies on evaluating state bounds $T-1H$ prior to the webhook triggering. Doing asynchronous evaluation at purchase timestamp corrupts data (since the purchase itself alters intimacy arrays violently).
- **ADR-01 Isolation:** Registry data binds strictly to the `coach_id`. Financial bounds and psychological conversions cannot drift into global aggregates.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Logging Assembly)
- **Agent:** `campaign-performance-logger`
- **Inputs:** 
  - `commercial_outcome_webhook` (DEP-ID: `DEP-ENG-045` — Produced By: FR45 Webhook Gateway / Stripe response)
  - `historical_cbcs_snapshot` (DEP-ID: `social_penetration_depth_gauge`, `information_coping_trajectory`, `telegram_intimacy_index` — Produced By: FR-CBCS-02, 04, 07)
- **Outputs:**
  - Extracted string variables mapping mapped Schema Enums.
- **Failure Condition:** If `commercial_outcome_webhook` fails to include a traceable `client_id`, the row returns `NULL` and aborts tracking.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `campaign_execution_id` + `conversion_outcome` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Outcome State):** The `conversion_outcome` String Enum resolves based exactly on parsing the `commercial_outcome_webhook` payload variables:
- **"BOOKED_CONVERTED"**: Evaluates `True` IF webhook contains a valid `checkout.session.completed` OR `invitee.created` linked to campaign UUID.
- **"DECLINED_OPT_OUT"**: Evaluates `True` IF webhook contains string `/stop` or clicking inline "No Thanks".
- **"NO_RESPONSE_DORMANT"**: Evaluates `True` IF mathematical subtraction `current_time - offer_delivery_time > 72_hours` and zero input.

### Stage 2: Quality Gate Extension
- **Agent:** `campaign-performance-logger`
- **Inputs:** Generated strings and upstream arrays.
- **Outputs:** `CampaignPerformanceRegistryRow` (DEP-ENG-051).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `coping_tier` logged. **(Mandatory Execution)**.
- **Failure Condition:** Incomplete psychological array logic prevents `.jsonb` insertions completely to maintain structural integrity.

**Quality Gate:** **The Registry Completeness Gate**
- **Triggered when:** The background script calls the `write_to_supabase()` function passing the `DEP-ENG-051` schema structure.
- **Exact Thresholds:** Validates the presence of `psych_snapshot_at_launch` mapped JSON integers.
- **Verdict - PASS:** Null checks clear. `coping_tier` != `null`, `spt_stage` != `null`, `intimacy_score` != `null`. *Downstream Consequence:* Row is written to Supabase permanently. `gate_verdict = PASS`.
- **Verdict - PROVISIONAL:** Missing non-critical metadata (e.g., Change Talk depth density logs blank). *Downstream Consequence:* Acknowledges partial log. Row is written to Supabase properly, but populated `gate_verdict = PROVISIONAL_PARTIAL`.
- **Verdict - FAIL:** Critical routing identifiers missing (`coping_tier` == `null`). *Downstream Consequence:* Write is rejected entirely. Triggers exception: `"Attempting to log commercial run without psychological context invalidates data integrity."` `gate_verdict = FAIL_CORRUPTED`.

### Phase 3: Field-by-Field Schema Mapping
Every schema field specifies exact evaluation origin:
- `registry_id`: Returns `uuid.uuid4()`.
- `campaign_execution_id`: Returns UUID tracking from FR59 Orchestrator.
- `client_id`: Returns matched parsed UID from webhook.
- `coach_id`: Returns mapped context verifying ADR-01 bound.
- `conversion_outcome`: Returns String Enum mapped by Stage 1 ("BOOKED_CONVERTED" | "DECLINED_OPT_OUT" | "NO_RESPONSE_DORMANT").
- `psych_snapshot_at_launch.coping_tier`: Returns Int (1-5) via PostgreSQL lookup at execution T-1.
- `psych_snapshot_at_launch.spt_stage`: Returns Int (1-4) via PostgreSQL lookup.
- `psych_snapshot_at_launch.intimacy_score`: Returns Float via PostgreSQL TII table lookup.
- `time_to_conversion_hours`: Returns numerical subtraction Float `Conversion_Timestamp - Launch_Timestamp`. Null if no conversion.
- `gate_verdict`: Returns String mapped by Stage 2 thresholds ("PASS" | "PROVISIONAL_PARTIAL" | "FAIL_CORRUPTED").
- `log_timestamp`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CampaignPerformanceRegistryRow (DEP-ENG-051)",
  "type": "object",
  "properties": {
    "registry_id": { "type": "string", "format": "uuid" },
    "campaign_execution_id": { "type": "string", "format": "uuid" },
    "client_id": { "type": "string" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "conversion_outcome": { "type": "string", "enum": ["BOOKED_CONVERTED", "DECLINED_OPT_OUT", "NO_RESPONSE_DORMANT"] },
    "psych_snapshot_at_launch": {
      "type": "object",
      "properties": {
        "coping_tier": { "type": "integer" },
        "spt_stage": { "type": "integer" },
        "intimacy_score": { "type": "number" }
      }
    },
    "time_to_conversion_hours": { "type": ["number", "null"] },
    "gate_verdict": { "type": "string", "enum": ["PASS", "PROVISIONAL_PARTIAL", "FAIL_CORRUPTED"] },
    "log_timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "registry_id", "campaign_execution_id", "client_id", "coach_id", "conversion_outcome",
    "gate_verdict", "log_timestamp"
  ]
}
```

---

## 6. Backward Compatibility Fallback
Legacy CPSC campaigns that fired historically without executing the complex `historical_cbcs_snapshot`:
Schema strictly explicitly permits the `PROVISIONAL_PARTIAL` definition logic path to allow parsing of generic webhook conversions so total revenue numbers do not incorrectly break on visual coach dashboards due to missing deep integers.

---

## 7. Tasks
- [ ] Task 1: Deploy Supabase SQL architecture establishing `campaign_performance_registry` mirroring exact primary schema integer constraints.
- [ ] Task 2: Code `campaign_performance_logger.py` handling Stripe JSON parsing, extracting internal `client_id` meta parameters to feed Stage 1 mappings.
- [ ] Task 3: Write $T_{minus-1}$ DB query logic enforcing script to map psychological states *prior* to message string distribution timeline.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Corrupted Data Rejection):** System attempts to write `BOOKED_CONVERTED` record where `coping_tier=null`. Gate MUST evaluate `FAIL_CORRUPTED`. Row MUST NOT write to DB. **Failure Example:** Blind conversions accumulate, irreparably breaking Data Analyst computations.
- [ ] **AC2 (Valid Provisional Handling):** System evaluates `NO_RESPONSE_DORMANT` where `coping_tier=3`, but `intimacy_score=null`. Gate MUST evaluate `PROVISIONAL_PARTIAL` and log row accurately. **Failure Example:** Throwing away valid outcome telemetry on a minor missing snapshot lag, destroying macro accuracy.
- [ ] **AC3 (Enum Variable Extraction):** Stripe webhook containing `charge.succeeded` impacts pipeline. Stage 1 logic MUST map parameter explicitly mapping `conversion_outcome == BOOKED_CONVERTED`. **Failure Example:** Script logs mere click link events as final purchases skewing statistical validity.

---

## 9. Dependencies
- **Upstream:**
  - `FR59`: Campaign Orchestration Execution ID routing.
  - `FR45`: External Stripe/Calendly event webhooks (`DEP-ENG-045`).
  - `FR-CBCS-02`, `FR-CBCS-04`, `FR-CBCS-07`: Trailing Database Snapshot arrays for `spt` and `coping`.
- **Downstream:**
  - `FR43`: Consumes data for mathematical correlation finding.
  - `FR60`: Consumes output for Narrative formatting routines.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Conversion_Outcome_Enum_Map`: Pass mock generic dictionaries containing Stripe keys `checkout.session.completed` versus telegram string `"/stop"`. Assert logic routes JSON correctly resolving to `BOOKED_CONVERTED` vs `DECLINED_OPT_OUT`.
- `Test_Corrupted_Null_Rejection`: Execute insertion map carrying `coping_tier` set explicitly to `None`. Assert python Gateway Evaluation routine fails completely assigning enum `FAIL_CORRUPTED` bypassing PostgreSQL injection methods.

### Integration Tests
- `Test_T_Minus_1_DB_Verification`: Trigger script hook at `T0`. Assert internal query script fires timestamps explicitly bound requesting `T_minus_2_hours` records only.

### Safety / Isolation Tests
- `Test_Webhook_ADR01_Enforcement`: Hit script endpoint parsing external generic Stripe hook. Ensure absence of active Supabase Token forces rejection. Ensure script successfully decrypts `coach_id` embedded in Stripe metadata prior to attempting any DB internal logic hooks, preventing global table mixing.
