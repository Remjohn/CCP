# FR-CBCS-09: Habit Architecture Module — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F9, PRD §FR-CBCS-09

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Standard check-in sequences rely on high motivation ("Did you do the thing?"). When motivation drops, compliance drops, leading to client shame and eventual churn. Telling clients to "try harder" is scientifically invalid behavior change. 

### Solution
The Habit Architecture Module enforces the psychological construct of "Implementation Intentions" (If/Then planning). When a client sets a goal inside the CBCS, the Module intervenes and forces them to explicitly state the contextual cue ('If/When') and the concrete action ('Then'). This shifts cognitive load from active working memory (motivation) to environmental triggers (automation).

### Scope
**In scope:**
- The `implementation-intention-parser` examining client goals.
- The `Implementation Intention Verification Gate` grading the structural validity of the client's reply.
- The `habit_architecture_tracker` SQL table tracking Enum states.
- Follow-up messaging resolving habit status.

**Out of scope:**
- General emotional validation (handled by FR10).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `habit_architecture_tracker` | SQL Enforced Goal state | Tracks If->Then compliance | FR-CBCS-09 | FR10, FR53 |
| `PROPOSED: DEP-ENG-064` | Habit Verification Verdict | Controls follow-up replies | FR-CBCS-09 | CBCS Generator |

### Academic Grounding
- **Research Paper:** *Implementation Intentions: Strong Effects of Simple Plans* (Gollwitzer, 1999).
- **Mechanism:** Goal intentions ("I want to exercise") rarely predict behavior. Implementation intentions ("If it is 8 AM, then I will run") create mental links between situations and actions. The situation cues the action automatically, overcoming ego-depletion.

### Technical Decisions
- **Regex Parsing:** We don't need a massive LLM to grade habit structure. A strict Regex matching algorithm is faster, cheaper, and more accurate for "If [Environment], Then [Action]" syntax gating.
- **State Machine Tracking:** The tracker manages 4 exact states indicating where the habit resides in the lifecycle, preventing the bot from nagging about `ABANDONED` habits.

---

## 4. Implementation Plan

### Stage 1: Intention Parsing
- **Agent:** `implementation-intention-parser` (Python Text Scanner)
- **Inputs:** 
  - `raw_client_message_text` (DEP-ID: `DEP-ENG-045` — Produced By: FR45 Webhook Gateway)
  - `current_coping_position` (DEP-ID: `information_coping_trajectory` — Produced By: FR-CBCS-04)
- **Outputs:** Database row interaction with `habit_architecture_tracker`.
- **Failure Condition:** If `raw_client_message_text` is empty or malformed data type, script terminates early without throwing unhandled exceptions. DB write skips safely.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `habit_status` written to APM.
- **ADR-01 Isolation Constraint:** The DB `SELECT/UPDATE` executions operate explicitly inside `WHERE coach_id = auth.uid()` scopes.

### Stage 2: Variable Resolution Rules (Metrics)
The script calculates specific text metrics to power the Gate:
- **`if_then_syntax_found`**: Evaluates `True` IF `REGEX(message, \b(if|when)\b.*\b(then|i will|i'm going to)\b)` matches.
- **`concrete_action_found`**: Evaluates `True` IF NLP dependency parser identifies a root Action Verb (e.g., 'drink', 'walk', 'write') connected to a specific noun/quantity object, rather than an abstract verb ("feel", "be").

### Stage 3: Quality Gate Extension
**Quality Gate:** **Implementation Intention Verification Gate**
- **Triggered when:** The CBCS detects the client attempting to establish a new habit or goal.
- **Exact Thresholds:**
  - `Condition_1`: `if_then_syntax_found == True`
  - `Condition_2`: `concrete_action_found == True`
- **Verdict - PASS:** Both conditions are `True`. *Downstream Consequence:* Client correctly structured the psychology. Database saves intention logic. Module replies with positive reinforcement and schedules tracking.
- **Verdict - PROVISIONAL:** `Condition_1` is `True` BUT `Condition_2` is `False`. (e.g., "If I feel sad, then I will be better"). *Downstream Consequence:* Client understands the If/Then structure but is using abstract actions. Module loops back, prompting: "I see the trigger. What exactly does 'be better' physically look like? Be specific." Status updates to `FORMING`.
- **Verdict - FAIL:** `Condition_1` is `False`. *Downstream Consequence:* No environmental cue established. Module replies with the educational Gollwitzer template intervention: "Goals fail without triggers. Let's build an implementation intention. *If [X happens], then I will [do Y].* Give it a try." Status updates to `FORMING`.

### Stage 4: Resolution Rules for State and Schema Enum
The `habit_status` String Enum resolves exactly via:
- **"FORMING"**: Maps IF the Gate evaluated to `PROVISIONAL` or `FAIL`. (They are trying to build it, but it's structurally flawed).
- **"VERIFIED"**: Maps IF the Gate evaluated to `PASS`.
- **"BROKEN"**: Maps IF client explicitly replies "I didn't do it" or "I missed my habit" to a check-in prompt.
- **"ABANDONED"**: Maps automatically via cron job IF `last_checked_date > 14 days` AND no client updates received.

Output Schema explicitly maps variables:
- `tracker_id`: `uuid.uuid4()`.
- `client_id` / `coach_id`: Synchronous passage.
- `environmental_cue`: NLP string extraction of the text between "If/When" and "Then/I will". Null if `if_then_syntax_found == False`.
- `concrete_action`: NLP string extraction of the text following "Then/I will". Null if `concrete_action_found == False`.
- `habit_status`: Exact Enum mapping ("FORMING" | "VERIFIED" | "BROKEN" | "ABANDONED").
- `verification_verdict`: Exact Gate mapping ("PASS" | "PROVISIONAL" | "FAIL").
- `last_checked_date`: UTC ISO8601 updated upon any state change.

---

## 5. Primary Output Schema

```typescript
type HabitArchitectureTrackerRow = {
  tracker_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  environmental_cue: string | null; 
  concrete_action: string | null; 
  habit_status: "FORMING" | "VERIFIED" | "BROKEN" | "ABANDONED"; // Exact Enum map
  verification_verdict: "PASS" | "PROVISIONAL" | "FAIL"; // Gate state 
  last_checked_date: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
Active clients attempting to track goals using the V2 unstructured "To-Do List" pipeline:
- Their legacy unstructured goals are ported into `habit_architecture_tracker` with `habit_status = "FORMING"`.
- The very next check-in interaction will execute the `FAIL` gate protocol, coercing them into re-submitting their goal using proper "If/Then" syntax to upgrade to `VERIFIED`.

---

## 7. Tasks
- [ ] **Task 1: Parsing Engine** - Write `implementation_parser.py` utilizing the strict regex pattern matching enforcing the syntax variables.
- [ ] **Task 2: State Machine Schema** - Deploy PostgreSQL schema matching `HabitArchitectureTrackerRow` mapping Enum limits and ADR-01 RLS security policies.
- [ ] **Task 3: Module Prompts** - Create the exact generative fallback strings (e.g., the Gollwitzer template intervention) stored in the prompt library for `FAIL` and `PROVISIONAL` verdicts.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Syntax Verification Gate):** Client inputs "I will go to the gym tomorrow". Regex parses `if_then_syntax_found = False`. Gate MUST evaluate `FAIL` assigning `habit_status: FORMING`. **Failure Example:** System evaluates it as a valid goal, perpetuating weak behavior science and validating abstract motivation.
- [ ] **AC2 (Provisional Abstract Parsing):** Client inputs "When I wake up, then I will focus." Regex passes, but `verb = focus` triggers abstract noun rejection (`concrete_action_found = False`). Gate MUST evaluate `PROVISIONAL`. **Failure Example:** The system approves "I will focus", leaving the client with no measurable physical action to take when they wake up.
- [ ] **AC3 (Abandonment Auto-Prune):** Cron string evaluator detects `last_checked_date = 15 Days Ago` where `habit_status = VERIFIED`. Script MUST strictly update database row to `ABANDONED`. **Failure Example:** Script ignores temporal decay, and the bot asks a client about a meditation habit they stopped doing 4 months ago, demonstrating memory loss.
