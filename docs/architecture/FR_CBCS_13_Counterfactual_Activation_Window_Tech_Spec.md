# FR-CBCS-13: Counterfactual Activation Window — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F13, PRD §FR-CBCS-13

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Standard scarcity mechanisms ("Doors close tonight!") trigger immediate reactance. They force compliance through temporal panic, shifting the locus of control externally. This creates "buyer's remorse" built on coercion rather than internal Sovereign alignment.

### Solution
The Counterfactual Activation Window replaces artificial scarcity with Epistemic Scarcity. Instead of threatening a disappearing offer, the system utilizes "Counterfactual Thinking" (If/Then scenario simulation). It generates a highly tailored prompt 72 hours after an unanswered offer, forcing the client to mentally simulate the reality where they take action versus the reality where they do not. The client creates their own internal urgency.

### Scope
**In scope:**
- The `counterfactual-generator-agent`.
- Enum resolution for Upward vs Downward counterfactuals based on Identity profiles.
- The `Epistemic Check-in Gate` managing temporal delivery bounds.

**Out of scope:**
- Delivering the Day 0 Offer (handled by FR53).
- Tracking general open rates (handled natively by Telegram/Mail hooks).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-068` | Epistemic Gate Verdict | Prevents premature nagging | FR-CBCS-13 | Counterfactual Agent |

### Academic Grounding
- **Research Paper:** *Counterfactual Thinking and Regulatory Focus* (Roese et al., 1999) + *Anticipated Regret and Behavior* (Zeelenberg, 1999).
- **Mechanism:** Humans weigh losses heavier than gains. Downward counterfactuals ("Imagine if things get worse") drive immediate action for security-focused individuals. Upward counterfactuals ("Imagine how good it could be") drive action for expansion-focused individuals. Both shift the urgency internally.

### Technical Decisions
- **Temporal Enforcement:** The script enforces a rigid 72-hour `time_since_offer_sent` gate. A 24-hour follow-up is universally perceived as nagging. 72 hours allows the offer to metabolize.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Activation Mode)
- **Agent:** `counterfactual_trigger_router.py` (Pre-processes before LLM trigger)
- **Variable Resolution Rule:** The `activation_mode` String Enum resolves based on the client's `unified_identity_profile`:
  - **"UPWARD_COUNTERFACTUAL"**: Evaluates `True` IF `unified_identity_profile.emotional_architecture.primary_driver` matches `(Expansion|Autonomy|Growth|Achievement)`. *Instruction sent to LLM:* "Frame the scenario focusing on the positive future state they miss out on by not taking action."
  - **"DOWNWARD_COUNTERFACTUAL"**: Evaluates `True` IF `primary_driver` matches `(Security|Belonging|Safety|Connection)`. *Instruction:* "Frame the scenario focusing on the compounding negative state they remain stuck in by avoiding action."

### Stage 2: Epistemic Delivery Gating
- **Agent:** `EpistemicDeliveryGuard` (Python cron job module)
- **Inputs:** 
  - `time_since_offer_sent` (Numeric hours)
  - `client_replied_to_offer` (Boolean)
  - `liwc_scores_jsonb` trailing (DEP-ID: `DEP-ENG-047` — Produced By: FR47 LIWC-22 Global Analyzer)
- **Outputs:** `PROPOSED: DEP-ENG-068` (Epistemic Gate Verdict JSON).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `gate_verdict` written to APM log validating the gate evaluation.

**Quality Gate:** **The Epistemic Check-in Gate**
- **Triggered when:** The cron sweeps for pending Day 3 / Day 7 post-offer interactions spanning the CRM.
- **Exact Thresholds:**
  - `Condition_1`: `time_since_offer_sent >= 72`
  - `Condition_2`: `client_replied_to_offer == False`
- **Verdict - PASS:** Both conditions are `True`. *Downstream Consequence:* `counterfactual-generator-agent` executes the script and dispatches the payload via Telegram.
- **Verdict - PROVISIONAL:** `time_since_offer_sent >= 48` AND `< 72` BUT the client has sent a message to the bot in the last 12 hours where `liwc_scores.cognitive_processes > 0.1` (indicating they are thinking actively, just distracted). *Downstream Consequence:* The script flags `PROVISIONAL_EARLY_FIRE`. It pushes the Counterfactual Script draft to the Operator Review queue to authorize an early send while they are actively engaged.
- **Verdict - FAIL:** `client_replied_to_offer == True` OR `time_since_offer_sent < 72` (without passing the Provisional cognitive ping). *Downstream Consequence:* The system is blocked from messaging the client. Prevents double-texting or nagging.

### Stage 3: Resolution Rules for Output Schema
Every schema field maps to explicit variables parsed during the workflow:
- `eval_id`: `uuid.uuid4()`.
- `client_id` / `coach_id`: Synchronous mapping.
- `activation_mode_assigned`: The strict String Enum derived from the Stage 1 dictionary matcher ("UPWARD_COUNTERFACTUAL" | "DOWNWARD_COUNTERFACTUAL").
- `gate_verdict`: "PASS" | "PROVISIONAL_EARLY_FIRE" | "FAIL_BLOCKED".
- `hours_elapsed_since_offer`: Numeric Float calculation `Current_UTC - Offer_Sent_UTC`.
- `dispatched_text`: The finalized Counterfactual script (ONLY populated if PASS or Operator override). Null otherwise.
- `last_evaluated`: `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type EpistemicActivationRow = {
  eval_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  activation_mode_assigned: "UPWARD_COUNTERFACTUAL" | "DOWNWARD_COUNTERFACTUAL";
  gate_verdict: "PASS" | "PROVISIONAL_EARLY_FIRE" | "FAIL_BLOCKED";
  hours_elapsed_since_offer: number; // Float
  dispatched_text: string | null;
  last_evaluated: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For legacy promotional sequences that relied on generic "This offer expires soon!" emails built in standard CRMs:
- The system will NOT intercept emails already in flight. 
- All new Telegram/Voice-based CPSC campaign trees are completely forbidden from triggering "Countdown Clocks" via textual hooks. The Counterfactual Window acts as the sole authorized method for prompting action on inactive leads.

---

## 7. Tasks
- [ ] **Task 1: Pre-mapping Routing** - Build the dict arrays assigning `primary_driver` Strings correctly to the `UPWARD/DOWNWARD` Enum limit boundaries.
- [ ] **Task 2: Cron Job Temporal Gate** - Code the Postgres Timestamp comparison logic enforcing `Condition_1` precisely at the `>= 72.00` hour float cutoff.
- [ ] **Task 3: Provisional Cognitive Trigger** - Implement the Python subroutine scanning for the 48-72h trailing `liwc_scores.cognitive_processes > 0.1` edge-case exception.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Temporal Gate Enforcement):** A background chron triggers at 71.5 hours since offer dispatch. Gate MUST evaluate exactly to `FAIL_BLOCKED`, suppressing generation. **Failure Example:** Off-by-one roundups trigger the sequence natively at 60 hours, nagging the user prematurely.
- [ ] **AC2 (Provisional Cognitive Fire):** At Hour 50 post-offer, the client sends a message containing "I'm thinking about it." `liwc.cognitive = 0.15`. Gate MUST evaluate `PROVISIONAL_EARLY_FIRE` routing to review. **Failure Example:** The system blindly ignores the active engagement ping and waits another 22 hours to reply, losing the conversion window.
- [ ] **AC3 (Enum Architecture Enforcement):** A client mapped with Identity driver `"Security"` runs the generator. Field `activation_mode_assigned` MUST insert `"DOWNWARD_COUNTERFACTUAL"`. **Failure Example:** The logic dictionary defaults improperly to UPWARD, creating dissonance that triggers avoidance behavior.
