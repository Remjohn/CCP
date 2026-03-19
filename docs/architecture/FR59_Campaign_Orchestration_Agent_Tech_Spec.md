# FR59: Campaign Orchestration Agent — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §FR59

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CCP update/CCP_Sales_Cycle_Documentation_V1.docx.md`

---

## 2. Overview

### Problem Statement
An ecosystem containing 54 specialized AI agents working simultaneously risks generating pure chaos. If systems aren't rigidly orchestrated, a client might simultaneously receive a Day 1 webinar invitation, a Day 3 counterfactual prompt, and a Day 7 checkout reminder, destroying the timeline logic of a coherent sequence.

### Solution
The Campaign Orchestration Agent (FR59) functions as the master timeline governor. It binds all individual generative units (FR51-FR58) into a single, cohesive execution pipeline. Crucially, it enforces the "Operator-Triggered Only" constraint. It manages Pi Extensions, enforces the 21-day cooldown gate, and sequentially fires the 72-Hour Anchor hooks natively.

### Scope
**In scope:**
- The `campaign-orchestration-agent` managing the master state loop.
- The `Campaign Initialization Gate` enforcing manual Operator verification matrices.
- Timeline state Enums indicating exact sequence positions.

**Out of scope:**
- Creating the specific strings for the emails (handled by FR51-54).
- Actually sending the telegram webhook.

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-079` | Campaign Execution Log | Tracks active pipeline bounds | FR59 | FR56 / FR60 |

### Academic Grounding
- **Mechanism:** Sequential behavioral milestones. Human cognition requires linear narrative progression. Presenting a Close before an Opening breaks the psychological timeline. The orchestrator guarantees steps cannot fire randomly.

### Key Files
- `orchestrator_governor.py`
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **Manual Trigger Prohibition:** The PRD states: **"Critical architectural constraint: campaigns are operator-triggered, never autonomous."** The Orchestrator will reject internal API calls attempting to launch Campaigns. It ONLY accepts context linked to human UI or Telegram inputs.
- **ADR-01 Isolation:** The orchestrator loop spins up at the tenant scale verifying `coach_id` parameters precisely.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Execution State)
- **Agent:** `campaign-orchestration-agent`
- **Inputs:** 
  - `telegram_slash_command` string (Origin: UI / Bot interface)
  - `target_client_arrays` (Origin: FR58 approved UUIDs)
- **Outputs:**
  - `master_campaign_state` String Enums mapping progression bounds.
- **Failure Condition:** Missing UI trigger completely blocks state.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `operator_auth_id` + `campaign_blueprint_id` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Pipeline Status):** The Orchestrator manages `master_campaign_state` Enum through python time progression logic:
- **"QUEUED_PENDING_LAUNCH"**: Evaluates `True` IF operator triggered launch BUT `datetime.now() < scheduled_start_date`.
- **"ANCHORING_DAY_1_TO_3"**: Evaluates `True` IF `current_date` falls inside 72-hour window. Orchestrator allows FR53 identity prompts; commercial links locked out.
- **"CONVERSION_WINDOW_ACTIVE"**: Evaluates `True` IF `current_date > Day 3` AND `< Day 7`. Releases lockdown.
- **"COOLDOWN_RESOLVED"**: Evaluates `True` IF `current_date > Day 7`. Maps client to FR-CBCS-14 Cooldown Governor natively.

### Stage 2: Quality Gate Extension
- **Agent:** `campaign-orchestration-agent`
- **Inputs:** Boolean validation routines.
- **Outputs:** `CampaignExecutionLogRow` JSON (DEP-ENG-079).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `roster_size_at_launch` logged. **(Mandatory Execution)**.
- **Failure Condition:** Operator Context missing.

**Quality Gate:** **The Campaign Initialization Gate**
- **Triggered when:** Operator inputs `/cpsc-campaign-start [campaign_id]` or clicks Launch UI.
- **Exact Thresholds:** Validates 3 exact conditions. `Condition_1`: Caller ID matches `admin` mapping. `Condition_2`: Target Roster count `> 0` (via FR58). `Condition_3`: `campaign_id` asserts a linked FR51/52 brief ID.
- **Verdict - PASS:** All conditions meet. *Downstream Consequence:* `master_campaign_state` updates to `"QUEUED_PENDING_LAUNCH"`. Sets `gate_verdict = PASS_AUTHORIZED`.
- **Verdict - PROVISIONAL:** Conditions 1 & 2 pass, BUT `brief_id = -1` (legacy broadcast). *Downstream Consequence:* Pauses launch. Prompts Operator UI: `"Launching campaign devoid of CBCS intelligence. Confirm?"` Sets `gate_verdict = PROVISIONAL_LEGACY_MODE`.
- **Verdict - FAIL:** Condition 1 evaluates `False` OR Roster == 0. *Downstream Consequence:* Hard reject. `"Error: Unauthorized launch or Zero target roster."` `gate_verdict = FAIL_ABORTED`.

### Phase 3: Field-by-Field Schema Mapping
Every schema field specifies exact evaluation origin:
- `execution_run_id`: Returns `uuid.uuid4()`.
- `campaign_blueprint_id`: Returns passed parameter matching FR51 or FR52 output arrays.
- `coach_id`: Returns `auth.uid()` enforcing ADR-01 bound.
- `operator_auth_id`: Returns Context object Caller ID mapping exact user who executed `/cpsc-campaign-start`.
- `master_campaign_state`: Returns mapped Stage 1 logic string ("QUEUED" | "ANCHORING" | "CONVERSION" | "COOLDOWN").
- `gate_verdict`: Returns String mapped by Stage 2 ("PASS_AUTHORIZED" | "PROVISIONAL_LEGACY_MODE" | "FAIL_ABORTED").
- `roster_size_at_launch`: Returns Integer count parsed from length of FR58 array response.
- `started_at`: Returns UTC timestamp `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CampaignExecutionLogRow (DEP-ENG-079)",
  "type": "object",
  "properties": {
    "execution_run_id": { "type": "string", "format": "uuid" },
    "campaign_blueprint_id": { "type": "string", "format": "uuid" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "operator_auth_id": { "type": "string" },
    "master_campaign_state": { "type": "string", "enum": ["QUEUED_PENDING_LAUNCH", "ANCHORING_DAY_1_TO_3", "CONVERSION_WINDOW_ACTIVE", "COOLDOWN_RESOLVED"] },
    "gate_verdict": { "type": "string", "enum": ["PASS_AUTHORIZED", "PROVISIONAL_LEGACY_MODE", "FAIL_ABORTED"] },
    "roster_size_at_launch": { "type": "integer", "minimum": 0 },
    "started_at": { "type": "string", "format": "date-time" }
  },
  "required": [
    "execution_run_id", "campaign_blueprint_id", "coach_id", "operator_auth_id",
    "master_campaign_state", "gate_verdict", "roster_size_at_launch", "started_at"
  ]
}
```

---

## 6. Backward Compatibility Fallback
For Coaches demanding raw CSV email blasts:
System catches CSV uploads enforcing them through `PROVISIONAL_LEGACY_MODE`. Permits send, but stamps execution record bypassing the `Campaign Performance Registry` calculations in FR56 (since it lacks baseline psychological arrays data).

---

## 7. Tasks
- [ ] Task 1: Instantiate the `TillDone` parent object sequence structure locking subprocess timing modules ensuring Day 2 logic explicitly waits functionally for Day 1 payload dispatches.
- [ ] Task 2: Code python RBAC caller dependencies extracting `ctx.user.id` on Telegram `/cpsc-campaign-start` enforcing system rejection if user misses mapped Admin array variables.
- [ ] Task 3: Plumb rigorous Boolean logic stripping commercial URL elements off FR54 objects mapping evaluated State `ANCHORING_DAY_1_TO_3` to prevent early pitch accidents.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Automation Lockdown):** Background cron job attempts `initiate_campaign()`. Context role = `discord_bot`. Gate MUST evaluate `FAIL_ABORTED` strictly requiring human clearance. **Failure Example:** Autonomous agent accidentally starts selling $3000 product based on faulty schedule integer.
- [ ] **AC2 (Provisional Legacy Mode Integrity):** Operator forces generic CSV broadcast loop. Gate MUST evaluate `PROVISIONAL_LEGACY_MODE`. **Failure Example:** System crashes trying to locate missing FR51 brief payload tying loops infinitely.
- [ ] **AC3 (Enum Timeline Phasing):** System clock progresses Day 8 post-launch. Evaluator MUST advance Enum from `"CONVERSION_WINDOW_ACTIVE"` to `"COOLDOWN_RESOLVED"`. **Failure Example:** Loop freezes on Conversion Active, endlessly messaging clients.

---

## 9. Dependencies
- **Upstream:**
  - `FR58`: Consumes Validated Offer Brief Roster target variables.
  - `FR51`/`FR52`: Links structural payloads to ID routing.
  - `TillDone Extension`: Supabase scheduling logic integration paths.
- **Downstream:**
  - `FR53`: Sends sequence triggers.
  - `FR56`: Creates performance ledger hooks.
  - `FR-CBCS-14`: Receives resolved clients into array blocks.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Gateway_Admin_Role_Check`: Execute launch block providing Context Header `.role_id="Assistant"`. Assert algorithm routes purely mapping to `FAIL_ABORTED`.
- `Test_State_Progression_Timing`: Initialize object array parsing fake Datetime integers referencing `+5 Days`. Assert state explicitly evaluates mapping `CONVERSION_WINDOW_ACTIVE`.

### Integration Tests
- `Test_Roster_Size_Count_Array`: Mock logic piping UUID objects tracking `["A", "B", "C"]` into the Orchestrator loop instance variable mappings. Assert API passes evaluation bounds setting parameter `roster_size_at_launch = 3`.

### Safety / Isolation Tests
- `Test_URL_Stripping_Blocker`: Hard-compile an outbound email text array including `"www.stripe.com"` link formatting while state dictates `"ANCHORING_DAY_1_TO_3"`. Assert Orchestrator Regex filter engine scrubs payload entirely throwing generic error logs, confirming the absolute temporal safety constraints protecting relational progression.
