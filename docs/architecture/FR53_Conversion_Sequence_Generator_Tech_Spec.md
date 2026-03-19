# FR53: Conversion Sequence Generator — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_Sales_Cycle_Documentation_V1, CCP_CBCS_CPSC_V3 §FR53

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Standard email marketing systems execute linear drip sequences based entirely on chronological timestamps regardless of client behavior. If a client goes dormant, predicting these linear paths force-pushes Day 2 offers, actively destroying the parasocial bond by exposing the interaction as a blind algorithmic automaton.

### Solution
The Conversion Sequence Generator (FR53) executes the 72-Hour Identity Anchor Protocol (FR-CBCS-05) at scale with native psychological safety triggers. It merges the client's Social Penetration Depth stage and interaction history to customize message vulnerability depth. It implements built-in Dormancy Recovery logic, tracking real-time unread/unresponded states. If a client drops off, the sequence pivots dynamically to a contextually aware re-engagement prompt rather than force-pitching.

### Scope
**In scope:**
- The `conversion-sequence-router` dispatching multi-day prompt arrays.
- Enum resolution tracking `Sequence Interaction Status` real-time values.
- The `Dormancy Recovery Gate` pivoting message paths based on chronometric lag integers.

**Out of scope:**
- Creating the core Day 0 Offer URL (handled by Stripe APIs).
- Validating the 21-Day Cooldown bounds (handled exclusively by FR-CBCS-14).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-074` | Conversion Sequence Payloads | Multi-stage text block | FR53 | Webhook Extractor |

### Academic Grounding
- **Research Paper:** *Interaction Dynamics and Dormancy Recovery in Parasocial Settings* (Giles, 2002) + *Consistency and Commitment* (Cialdini, 1984).
- **Mechanism:** Human relationships possess a natural autonomic tempo. Persisting with a monologue when the other party is distracted triggers reactance. A contextually relevant pause and behavioral ping ("Hey, I know life gets busy") demonstrates empathy, reinforcing the peer-to-peer relationship instead of a brand-to-consumer coercion.

### Key Files
- `sequence_router.py` (Core logic path defining arrays)
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **Manual Trigger Prohibition:** The PRD explicitly forbids fully automated execution. No sequence can ever execute without an explicit Operator command (`/cpsc-campaign-start` bound in FR59). FR53 compiles the payload arrays, but halts execution bounds completely pending operator trigger.
- **ADR-01 Isolation:** Sequence generation queries specific user activity logs (webhook read times) bound securely by `coach_id` ensuring zero cross-tenant timing leakages.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Sequence Vulnerability Calibration)
- **Agent:** `conversion-sequence-router`
- **Inputs:** 
  - `spt_stage` Integer (DEP-ID: `social_penetration_depth_gauge` — Produced By: FR-CBCS-02)
  - `challenge_funnel_brief` (DEP-ID: `PROPOSED: DEP-ENG-072` — Produced By: FR51)
- **Outputs:**
  - Generation instruction parameters sent to LLM.
- **Failure Condition:** If `spt_stage` evaluates to `null` due to missing history, mathematical bounds default to `-1` to ensure clinical output.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `coach_id` + `spt_stage` + `timestamp` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Linguistic Depth):** The `sequence_vulnerability_mode` String Enum resolves mathematically to the client's individual `spt_stage` integer:
- **"OBJECTIVE_REFLECTIVE"**: Evaluates `True` IF `spt_stage <= 2` (Orientation / Exploratory). *LLM Instruction applied to context array:* "Maintain professional structure. Minimize deep emotional assumptions."
- **"AFFECTIVE_ATTACHMENT"**: Evaluates `True` IF `spt_stage >= 3` (Affective / Stable). *LLM Instruction applied to context array:* "Utilize 'We' language. Reference shared history implicitly."

### Stage 2: Dormancy Recovery Gating
- **Agent:** `TeamOrchestrator` Extension (during execution phase)
- **Inputs:** `hours_since_last_client_message` (Derived Float numeric calculation based on Webhook timestamp logs).
- **Outputs:** Final string `next_payload_string` mapping to DB.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `hours_lag` logged. **(Mandatory Execution)**.
- **Failure Condition:** Missing timestamp logs auto-evaluate to FAIL\_DORMANT\_ABORT to prevent accidental broadcast.

**Quality Gate:** **The Dormancy Recovery Gate**
- **Triggered when:** The system attempts to fetch `Day 2` logic dispatching the secondary anchor ping. 
- **Exact Thresholds:** Evaluates Float `hours_since_last_client_message`.
- **Verdict - PASS:** `< 36.00`. *Downstream Consequence:* Client is actively engaged. Sequence continues exactly as drafted. `gate_verdict = PASS_ACTIVE`.
- **Verdict - PROVISIONAL:** `>= 36.00` AND `< 72.00`. *Downstream Consequence:* Client distracted. The script intercepts generation, rewrites prompt instructing a lightweight confirmation ping. Logs `gate_verdict = PROVISIONAL_DORMANT_RECOVERY`. Halts core commercial campaign progression.
- **Verdict - FAIL:** `>= 72.00`. *Downstream Consequence:* Hard freeze. Campaign sequence is aborted completely. Logic writes `gate_verdict = FAIL_DORMANT_ABORT`. Evaluates `next_payload_string` strictly to `null` preventing payload dispatch into a dead chat.

### Phase 3: Field-by-Field Schema Mapping
Every field in the JSON maps explicitly:
- `sequence_execution_id`: Returns `uuid.uuid4()`.
- `client_id`: Returns string mapping to prospect ID.
- `coach_id`: Returns `auth.uid()` from context reinforcing ADR-01 isolation.
- `sequence_vulnerability_mode`: Returns String Enum explicitly derived from Stage 1 mapping math ("OBJECTIVE_REFLECTIVE" | "AFFECTIVE_ATTACHMENT").
- `gate_verdict`: Returns String mapped by Stage 2 thresholds ("PASS_ACTIVE" | "PROVISIONAL_DORMANT_RECOVERY" | "FAIL_DORMANT_ABORT").
- `current_sequence_step_integer`: Returns INT (1, 2, or 3) representing structural day.
- `next_payload_string`: Returns the drafted text block; evaluates to `null` IF `gate_verdict` is `FAIL_DORMANT_ABORT`.
- `execution_timestamp`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ConversionSequencePayloadRow (DEP-ENG-074)",
  "type": "object",
  "properties": {
    "sequence_execution_id": { "type": "string", "format": "uuid" },
    "client_id": { "type": "string" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "sequence_vulnerability_mode": { "type": "string", "enum": ["OBJECTIVE_REFLECTIVE", "AFFECTIVE_ATTACHMENT"] },
    "gate_verdict": { "type": "string", "enum": ["PASS_ACTIVE", "PROVISIONAL_DORMANT_RECOVERY", "FAIL_DORMANT_ABORT"] },
    "current_sequence_step_integer": { "type": "integer", "enum": [1, 2, 3] },
    "next_payload_string": { "type": ["string", "null"] },
    "execution_timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "sequence_execution_id", "client_id", "coach_id", "sequence_vulnerability_mode",
    "gate_verdict", "current_sequence_step_integer", "next_payload_string", "execution_timestamp"
  ]
}
```

---

## 6. Backward Compatibility Fallback
Active pipeline executions where `social_penetration_depth_gauge` returns `null` because the client originated from an off-platform squeeze page and has never sent a native text interaction:
Default `spt_stage` integer calculation evaluates to `-1`. 
This triggers the Stage 1 standard `OBJECTIVE_REFLECTIVE` syntax bounds, ensuring no false intimacy breaks the initial interaction barrier with a functional stranger.

---

## 7. Tasks
- [ ] Task 1: Deploy logic mapping the numeric `spt_stage` bounds to the two specific String Enums assigning generation modes in Stage 1.
- [ ] Task 2: Embed the `hours_since_last_client_message` calculation subtraction loop logic explicitly executing before the `dispatch_webhook` node.
- [ ] Task 3: Hard-code the `next_payload_string == null` assignment directly to the `FAIL_DORMANT_ABORT` logic path in Python.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Dormancy Abandonment):** A client's last webhook timestamp occurs 75 hours ago. Gate MUST evaluate `FAIL_DORMANT_ABORT`. Schema MUST write `null` for `next_payload_string`. **Failure Example:** The system mindlessly blasts an ignored user with a complex Day 3 objection pitch, validating to the user that they are speaking to a dumb bot.
- [ ] **AC2 (Provisional Recovery Ping):** A client's last webhook was 46 hours ago. Gate MUST evaluate `PROVISIONAL_DORMANT_RECOVERY` and trigger rewrite pivot. **Failure Example:** Expected logic halts, aborting completely and losing a user who was genuinely simply busy at work but still interested.
- [ ] **AC3 (Enum Integrity on Mode Assignment):** Given `spt_stage = 4`, Stage 1 logic MUST definitively evaluate and assign `sequence_vulnerability_mode` == `"AFFECTIVE_ATTACHMENT"`. **Failure Example:** Defaults to clinical mode, treating deeply intimate client like a stranger, breaking the relational sequence loop.

---

## 9. Dependencies
- **Upstream:**
  - `FR-CBCS-02`: Produces Social Penetration Depth (`social_penetration_depth_gauge`).
  - `FR51`: Produces Challenge Funnel Brief (`PROPOSED: DEP-ENG-072`).
  - `FR45`: Produces Webhook inbound timestamp arrays (`DEP-ENG-045` - Webhook Gateway) for chronological subtraction logic.
- **Downstream:**
  - Telegram / WhatsApp generic outbound webhooks consume `next_payload_string`.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.
  - `TeamOrchestrator` Extension.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Dormancy_Gate_Temporal_Math`: Inject Synthetic Floats representing hours passed `[12.0, 48.0, 80.0]`. Execute Stage 2 evaluation. Assert Gateway returns proper mapping `[PASS_ACTIVE, PROVISIONAL_DORMANT_RECOVERY, FAIL_DORMANT_ABORT]`.
- `Test_SPT_Vulnerability_Resolver`: Inject `spt_stage = -1` (null fallback constraint). Assert logic outputs `OBJECTIVE_REFLECTIVE`.

### Integration Tests
- `Test_Null_Payload_Abort`: Trigger `FAIL_DORMANT_ABORT`. Assert that downstream webhook function `dispatch_message()` correctly catches the `null` payload object and aborts POST request cleanly. Asssert Receipt Chain writes log showing interception.

### Safety / Isolation Tests
- `Test_Manual_Trigger_Requirement`: Inject chron job attempting execution of Sequence array step 1. Provide Context Role of `cron_worker`. Assert complete script rejection via FR59 orchestration rules demanding operator UID. 
