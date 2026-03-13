# Tech-Spec: FR30 — Tiered Dormancy Recovery Protocol (DEP-ENG-025)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Client Lifecycle, §7.5 CBCS Pipeline
**Skill Implementation:** `CBCS/backend/core/scheduler.py`, `CBCS/backend/core/state.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`

---

## 2. Overview

### Problem Statement
In digital coaching and education, user silence is the leading indicator of churn. Most automated systems respond to silence with generic, administrative nudges ("We miss you!", "Don't forget to log in!"). These messages generate massive cognitive friction because they induce guilt without providing value. The user begins to view the system as a taskmaster rather than a coach, accelerating abandonment.

### Solution
FR30 institutes the **Tiered Dormancy Recovery Protocol (DEP-ENG-025)**. Silence is treated strictly as a clinical signal. Managed by Agent Vidye (State Orchestrator), the system tracks user unresponsiveness against 4 escalation thresholds: 3, 5, 10, and 30 days. When a threshold is crossed, the system queries the `MemoryFolder` for the user's previously stated L3 pain points or stalled milestones, and Artisan generates a highly contextual, low-friction re-engagement prompt. The goal is to restart the conversation by focusing entirely on the user's structural pain, not their administrative failure to use the app.

### Scope
**In scope:**
- Stage 1: Continuous Threshold Monitoring (Cron).
- Stage 2: Memory Retrieval (Stalled Milestones & L3 Context Premise).
- Stage 3: Generative Assembly of Tiered Responses.
- Stage 4: Active state modification marking the user as `DORMANT`.

**Out of scope:**
- Billing/payment churn protocols (this handles behavioral dormancy, not financial).
- Standard scheduled journaling (this entirely overrides the FR28 Dynamic Journaling queue until the user responds).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-025` | Dormancy Recovery Payload | OUTPUT — The contextual directive triggering a re-engagement attempt. |
| Vidye | State Orchestrator | AGENT — Owns the state machine, calculating the `Dormancy_Timer` delta. |
| `MemoryFolder` | Episodic Memory store | INPUT — Provides the contextual hook (what was the user working on before they vanished?). |
| Artisan | Script Artisan | AGENT — Generates the personalized text. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Fogg Behavior Model (B=MAP)** | B.J. Fogg | 2009 | Behavior = Motivation × Ability × Prompt. When a user is dormant, their Motivation is low or they perceive the Ability threshold as too high (too much effort). Traditional "we miss you" prompts fail because they don't lower the Ability barrier. Tiered recovery prompts *must* be low-friction (i.e., easy to answer) and highly relevant (leveraging prior Context Premise data) to succeed. |

### Technical Decisions
1. **The 4-Tier Escalation Path:** The protocol changes tone based on the exact threshold crossed. 
   - *Day 3:* Gentle nudge checking connection ("Did that last prompt feel too heavy?").
   - *Day 5:* Refocusing on the goal ("We were working on X. Still stuck there?").
   - *Day 10:* Pattern interruption (Aria identifies the silence as an active psychological defense mechanism: "Sometimes silence means you've hit the exact wall we need to break.")
   - *Day 30:* The Off-Ramp ("No judgment. I'll be here when you are ready to resume.")
2. **Journaling Override:** The moment Vidye flags a user at the `Day 3` threshold, the FR28 Journaling system is hard-locked. The system will physically not send standard curriculum updates to a dormant user.

---

## 4. Implementation Plan

### Stage 1: Continuous Threshold Monitoring
*Script:* `core/scheduler.py` -> `core/state.py`
*Agent Name:* Vidye (Orchestrator)
*Inputs:* User `last_interaction_timestamp`.
*Outputs:* Routing Command (`TRIGGER_RECOVERY_TIER_X`).
*Failure Condition:* The scheduler incorrectly evaluates timezone deltas and triggers a Day 3 warning on Day 2.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Nightly cron evaluates `current_time - last_interaction_timestamp`.
2. Matches exact threshold boundaries (3, 5, 10, 30 days). If the delta lands in between thresholds (e.g., Day 7), Vidye skips execution.
3. If a boundary is hit, Vidye flips the user's pipeline state to `RECOVERY_MODE` and calls the `MemoryFolder` hook.

### Stage 2: Contextual Memory Retrieval
*Script:* `core/state.py`
*Agent Name:* Azaria (Memory Curator)
*Inputs:* `user_id`.
*Outputs:* `stalled_milestone`, `last_l3_fear`.
*Failure Condition:* No memory exists because the user went dormant on Day 1.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Azaria executes a targeted query against the Neo4j Graph.
2. Extracts the most recent `ContextExtraction` (specifically `Fears` and `Frustrations`).
3. Extracts the last active step assigned via the Atlas Roadmap.
4. Bundles this data for Artisan.

### Stage 3: Generative Assembly & Delivery
*Script:* `core/artisan.py`
*Agent Name:* Artisan (Copywriter)
*Inputs:* Dormancy Tier (1-4), Azaria's Context Memory, `coach_soul.json`.
*Outputs:* Telegram Message.
*Failure Condition:* Artisan generates a generic "How are you?" message instead of utilizing the contextual variables.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Artisan receives the payload and the strict prompt modifier for the specific tier.
2. If `Tier 2` (5-Day), Artisan injects the memory variable. (e.g., *"Coach Voice: Hey. We were digging into [Stalled_Milestone] on Tuesday and then it got quiet. Is [Last_L3_Fear] acting up again? Hit me with a voice note."*).
3. Artisan caps output at `<50 tokens` to ensure ultra-low friction for the user to read.
4. Message is dispatched via `core/telegram.py`.

---

## 5. Primary Output Schema (DEP-ENG-025)

**Schema Name:** `dormancy_recovery_payload.json`

```json
{
  "user_id": "USR-114A",
  "coach_id": "EMI",
  "trigger_timestamp": "2026-03-25T00:00:00Z",
  "dormancy_tier": 2,
  "days_silent": 5,
  "recovery_context": {
    "stalled_milestone": "Identifying the 'Inner Critic' dialogue",
    "last_l3_fear": "Being exposed as a fraud at work",
    "required_friction_level": "ultra_low_yes_no_question"
  },
  "pipeline_state_update": {
    "previous_state": "ACTIVE_MOMENTUM",
    "new_state": "RECOVERY_MODE_TIER_2",
    "journaling_queue": "PAUSED"
  }
}
```

---

## 6. Backward Compatibility Fallback
If the user went dormant immediately upon entering the ecosystem (Day 1 Churn) and there is no Neo4j `MemoryFolder` data to retrieve, Stage 2 yields `null`. Artisan falls back to a structural curiosity prompt calibrated by the coach's TTT baseline (e.g., *"Usually when people go quiet this early, it's because they're overwhelmed. Is that what's happening right now?"*) rather than failing to compile entirely.

---

## 7. Tasks

- [ ] **Task 1:** Encode the `[3, 5, 10, 30]` threshold arrays into Vidye's state machine logic within `core/state.py`.
- [ ] **Task 2:** Build the Neo4j query within `graph_db.py` specifically optimized to retrieve the most recent `L3_Fear` and `Active_Milestone` edges associated with a specific user node.
- [ ] **Task 3:** Update the `core/scheduler.py` background worker to pause/bypass the FR28 Dynamic Journaling queue if the user's state flag is currently set to `RECOVERY_MODE`.
- [ ] **Task 4:** Create the 4 strict Tier prompt templates for Artisan. Each tier must enforce the B=MAP directive to lower prompt friction the deeper the dormancy extends.
- [ ] **Task 5:** Implement ADR-01 multi-tenancy rules ensuring the nightly unresponsiveness sweep maps the correct timezone and schedule relative to the specific Coach instance.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The 3-Day Trigger):** A user has not sent a Telegram message in exactly 72 hours. The nightly cron executes. Vidye changes the user's state to `RECOVERY_MODE_TIER_1` and Artisan fires the first low-friction nudge. *Failure Example:* The system triggers a "we miss you" message at 24 hours, feeling excessively needy and ruining the coaching dynamic.
- [ ] **AC2 (Journaling Suppression):** A user is 6 days dormant (`RECOVERY_MODE_TIER_2`). The regular Atlas Journaling schedule attempts to run. The system evaluates the state and immediately aborts the journaling payload, maintaining silence. *Failure Example:* The system sends an aggressive Day 5 check-in prompt from Vidye, and three hours later sends a dense journaling assignment from Atlas, overwhelming the user.
- [ ] **AC3 (Memory Injection):** A user who previously expressed a fear of "letting my team down" goes 10 days silent. Artisan's generated message explicitly mentions taking a pause regarding the team dynamics. *Failure Example:* The system generates "Are you still there?" completely ignoring the user's previously extracted Context Premise.
- [ ] **AC4 (ADR-01 Strict Isolation):** During the nightly dormancy sweep, calculating deltas for 5000 users. The system successfully flags Coach A's users without accidentally resetting or modifying Coach B's users' timer metrics. *Failure Example:* A shared variable resets Coach B's dormancy timers every time Coach A runs a sweep, meaning Coach B's clients never receive recovery prompts.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `MemoryFolder` (Azaria) | Upstream | Required to pull Context Premise for personalization. |
| `ContextExtraction` (Aria) | Upstream | The psychological data being retrieved. |
| Telegram Bot API | External | Delivery of the re-engagement payload. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Boundary Math Check:** Feed `last_interaction_timestamp` as exactly `7.0` days ago into Vidye's state evaluator. Assert state remains unchanged (neither 5 nor 10). Feed `10.1` days ago. Assert state flips to `RECOVERY_MODE_TIER_3`.
- **Fallback Generation:** Feed Artisan a `null` memory payload. Assert it successfully falls back to the generic (but TTT calibrated) curiosity script instead of throwing a `KeyError`.

### Integration Tests
- **The Journaling Block:** Instantiate a mock user with `state: RECOVERY_MODE`. Programmatically force the FR28 journaling cron to attempt to push a payload to this user. Assert the pipeline rejects the push returning an `[ABORT: USER_DORMANT]` code.
- **The Recovery Payload Generation:** Force a Tier 2 (Day 5) trigger for a mock user whose last known Context Premise is populated in the local Neo4j container. View the generated prompt. Assert the `stalled_milestone` is distinctly identifiable within the generated output string.

### Safety Tests (ADR-01 Quarantine Security)
- **Timezone Segregation:** Emulate Coach A situated in `UTC-8` and Coach B situated in `UTC+10`. Trigger the dormancy evaluation loop. Ensure the duration calculations adhere strictly to the timezone of the target coach's tenant instance, preventing premature midnight triggers across borders.
