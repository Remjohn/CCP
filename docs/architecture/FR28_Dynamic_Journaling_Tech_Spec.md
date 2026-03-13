# Tech-Spec: FR28 — Dynamic Journaling Rituals (DEP-ENG-024)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Atlas
**Skill Implementation:** `CBCS/backend/core/atlas.py`, `CBCS/backend/core/scheduler.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCBS\SKILL_AUTHORING_GUIDE_V4.md`

---

## 2. Overview

### Problem Statement
Static, calendar-based journaling prompts (e.g., generic "Reflection Friday" emails) suffer from massive attrition because they lack situational awareness. If a user is experiencing an acute crisis on Wednesday, sending them a high-friction productivity prompt on Thursday accelerates burnout. To maintain the illusion of a dedicated, empathetic coach, proactive check-ins must be deeply calibrated to the user's specific progress across the 30-day coaching journey and their immediate emotional state.

### Solution
FR28 formally defines the **Dynamic Journaling Engine (DEP-ENG-024)** administered by Agent Atlas (The Strategic Planner). Driven by the `scheduler.py` cron sequence, Atlas triggers 2-3 journaling prompts per week per user. Rather than pulling from a static list, Atlas dynamically cross-references two vectors to generate the prompt: 
1. The user's position on the `Atlas Roadmap` (Recovery, Foundation, Growth, Momentum, or Peak).
2. The user's most recent `ContextExtraction` (Aria's 12-dimension emotional parsing of their last Telegram interaction).

This guarantees that the prompt deepens the *current* coaching work required for that specific day.

### Scope
**In scope:**
- Stage 1: The Asynchronous Trigger & User State Retrieval.
- Stage 2: Atlas Roadmap Trajectory Mapping (The 5 Capacity Tracks).
- Stage 3: Generative Assembly (Agent Artisan).
- Tracking completion rates (≥80% KPI).

**Out of scope:**
- Immediate processing of the user's response (this routes back into the standard CBCS `<2s Latency Protocol` handling intent classification).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-024` | Dynamic Journaling Directive | OUTPUT — The structural prompt schema passed to Artisan to generate the final Telegram message. |
| Atlas | The Strategic Planner | AGENT — The intelligence defining the 30-day roadmap and identifying the appropriate prompt trajectory. |
| Artisan | The Master Copywriter | AGENT — The language synthesis engine that writes the actual text taking the TTT baseline. |
| `PantryConfig` | Coach Settings | INPUT — Dictates the exact frequency (e.g., 2 or 3 times per week) per coach program. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Motivational Interviewing (MI) Adaptability** | Miller & Rollnick | 2012 | MI requires that the coach's intervention match the client's current stage of change. Pushing action during a contemplation phase triggers resistance. Atlas explicitly encodes this by locking high-intensity prompts behind the "Growth" and "Momentum" capacity tracks, preventing escalation during "Recovery." |

### Technical Decisions
1. **The 4+1+2 Structure:** Atlas operates on a strict weekly modulation pattern: 4 Active Rituals, 1 Reflection Point, and 2 Rest Days. The 2-3 journaling prompts are exclusively mapped to the *Reflection* and *Active* slots, ensuring Rest Days remain sacred and silent.
2. **Anti-Escalation Protocol:** The system physically cannot escalate a user from "Recovery" to high-friction "Peak" prompting within the first 14 days of a roadmap. This is a hard guardrail in Atlas to prevent coaching toxicity.

---

## 4. Implementation Plan

### Stage 1: Asynchronous Scheduled Trigger
*Script:* `core/scheduler.py`
*Agent Name:* Master Cron Job
*Inputs:* `PantryConfig`, User `Dormancy_Timer`.
*Outputs:* Execution Wake Command.
*Failure Condition:* System schedules a prompt on a designated Rest Day.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'ASYNCHRONOUS-TRIGGER',
  agent_name: 'Master-Cron-Job',
  timestamp }

**Steps:**
1. Background cron evaluates all users daily. 
2. Checks user pacing: If user has a journaling slot available (based on the `2-3x/week` constraint in `PantryConfig`) AND today is an Active or Reflection day (not a Rest day), invoke Atlas.
3. Skip execution if the user's `Dormancy_Timer` is triggered (they haven't responded to previous prompts), routing them to the Dormancy Recovery loop instead.

### Stage 2: Strategic Trajectory Mapping
*Script:* `core/atlas.py`
*Agent Name:* Atlas (The Strategic Planner)
*Inputs:* `ContextExtraction` (from last session), `User_Roadmap_State`.
*Outputs:* `DEP-ENG-024` Directive JSON.
*Failure Condition:* Atlas attempts to trigger a "Peak" intensity prompt while the user is still in the "Recovery" window.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STRATEGIC-TRAJECTORY-MAPPING',
  agent_name: 'Atlas',
  timestamp }

**Steps:**
1. Atlas retrieves the user's current track `[Recovery, Foundation, Growth, Momentum, Peak]`.
2. Atlas retrieves Aria's last analyzed state (e.g., `distressed`, `apathetic`, `motivated`).
3. Atlas generates the dynamic constraint setup based on intersection logic:
   - *Example Mapping:* If Track = `Recovery` AND State = `distressed` → *Prompt Type: Grounding/Sensory. Tone: High empathy. Intensity: Low.*
   - *Example Mapping:* If Track = `Momentum` AND State = `motivated` → *Prompt Type: Friction/Challenge. Tone: Direct. Intensity: 10% higher than last week.*
4. Atlas outputs `DEP-ENG-024` as an instruction blob.

### Stage 3: Generative Assembly & Delivery
*Script:* `core/artisan.py` -> `core/telegram.py`
*Agent Name:* Artisan
*Inputs:* `DEP-ENG-024`, `coach_soul.json`.
*Outputs:* Formatted Telegram Message.
*Failure Condition:* Artisan generates a generic prompt ignoring the coach's TTT baseline.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'GENERATIVE-ASSEMBLY-DELIVERY',
  agent_name: 'Artisan',
  timestamp }

**Steps:**
1. Artisan absorbs the Atlas structural constraint (`DEP-ENG-024`).
2. Artisan generates the final user-facing text leveraging the coach's specific Voice DNA (`coach_soul.json`) and the 6-Beat Conscious Arc.
3. Output length is strictly capped to `<75 words` to emulate a quick, casual SMS check-in rather than a heavy email assignment.
4. Delivered via the standard Telegram webhook pipeline API.

---

## 5. Primary Output Schema (DEP-ENG-024)

**Schema Name:** `dynamic_journaling_directive.json`

```json
{
  "user_id": "USR-8f7d9a",
  "coach_id": "EMI",
  "scheduled_date": "2026-03-15",
  "roadmap_context": {
    "current_day": 12,
    "capacity_track": "Foundation",
    "structural_day": "Reflection Point"
  },
  "psychological_context": {
    "last_interaction_mood": "anxious_avoidant",
    "intensity_override": "decrease_10_percent"
  },
  "artisan_directive": {
    "prompt_category": "deconstruction",
    "emotional_target": "safety_establishment",
    "required_constraint": "Must not ask the user for a new commitment today. Must only ask them to pause and label the anxiety.",
    "max_words": 75
  }
}
```

---

## 6. Backward Compatibility Fallback
If Aria's `ContextExtraction` from the previous session corrupted or failed to save (yielding a `null` emotional state), Atlas gracefully falls back to the static baseline trajectory of the active Capacity Track. It removes the personalized behavioral modifier but strictly enforces the Anti-Escalation protocol (e.g., defaulting to the baseline "Growth" archetype prompt without adding the dynamic +10% friction modifier).

---

## 7. Tasks

- [ ] **Task 1:** Encode the mapping framework inside `core/atlas.py` that translates the 5 Capacity Tracks and 12-dimension emotional states into the 3 discrete prompt variables (Category, Target, Constraint).
- [ ] **Task 2:** Build the Anti-Escalation guardrail logic within Atlas that physically blocks `Growth`, `Momentum`, or `Peak` categorizations if `current_day < 14`.
- [ ] **Task 3:** Modify the `scheduler.py` background worker to pull the config frequency from `PantryConfig` while strictly skipping the 2 dynamically assigned `Rest Days` from the 7-day rolling window. 
- [ ] **Task 4:** Create a hard generation cap in Artisan's journaling prompt template enforcing conciseness (`max_output_tokens: 100`) to guarantee an SMS-style UX delivery.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Anti-Escalation Safety):** A scheduled user is on Day 6 of their journey and their recent mood is "Highly Motivated." Atlas attempts mapping. The script correctly truncates the prompt to the `Foundation` track despite the high motivation, obeying the `<14 day` escalation block. *Failure Example:* The system allows the user to accelerate into `Peak` on Day 6, causing cognitive burnout by Day 12.
- [ ] **AC2 (Rest Day Protection):** The `PantryConfig` dictates 3x/week journaling. The scheduler attempts to place the 3rd prompt on Sunday. The system recognizes Sunday is user's mapped `Rest Day 2`. It actively blocks generation and shifts the task to Monday. *Failure Example:* The coach bot texts the user on their mandated rest day, breaking the 4+1+2 architectural boundary.
- [ ] **AC3 (Dynamic Assembly):** For a user in `Momentum` feeling `Complacent`, Artisan synthesizes the prompt. The resulting output contains exactly 58 words and incorporates a clear friction challenge. *Failure Example:* The LLM generates a 400-word diary assignment using generic therapist phrasing instead of the coach's Voice DNA.
- [ ] **AC4 (ADR-01 Strict Isolation):** During the nightly Cron sweep of all users, Atlas evaluates User X (belonging to Coach A). Atlas explicitly mounts the `PantryConfig` belonging to Coach A, realizing Coach A only does 1x/week journaling, and skips the trigger. *Failure Example:* A shared namespace causes Coach A's users to receive Coach B's 3x/week cadence.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `PantryConfig` | Upstream | Determines the global coach settings for frequency. |
| `ContextExtraction` (Aria) | Upstream | The emotional memory driving the real-time adaptation. |
| Telegram Bot API | External | End delivery. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Guardrail Test:** Pass `current_day: 10` and `desired_track: Peak` to the atlas evaluation engine. Assert that the engine mutates the track backward to `Foundation`. Pass `current_day: 16`. Assert that it allows `Peak`.
- **Rest Day Sync Check:** Input a 7 day array with Rest Days on integers 3 and 7. Pass a request to schedule on integer 3. Assert a hard rejection. 

### Integration Tests
- **The Journaling Loop:** Trigger the `scheduler.py` journaling worker for a mock user whose last interaction mapped as `distressed`. Follow the generation through Atlas and Artisan without firing the final webhook. Verify the `DEP-ENG-024` directive sets `intensity_override: lower` and the final Artisan copy incorporates high empathy.
- **Latency Consistency:** Ensure the background async initiation of the prompt evaluation does not block or stack up in the main `FastAPI` event loop, allowing the API to continue serving inbound webhooks at `<2s` latency.

### Safety Tests (ADR-01 Quarantine Security)
- **Multi-Tenant Cron Sweep:** Trigger the cron scheduler for 1,000 distinct users across 50 coaches simultaneously. Monitor the Redis state loaders. Assert that 0 variables bleed between the iterations (i.e. User 999 does not accidentally receive User 2's capacity track).
