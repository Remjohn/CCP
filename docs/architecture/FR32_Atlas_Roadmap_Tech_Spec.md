# Tech-Spec: FR32 — Dynamic Capacity Tracks & 4-Week Roadmap (DEP-ENG-027)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Atlas (The Strategic Planner)
**Skill Implementation:** `CBCS/backend/strategy/atlas.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`

---

## 2. Overview

### Problem Statement
Standard coaching apps deliver a linear sequence of content to all users (e.g., Day 1 = Lesson 1, Day 2 = Lesson 2) regardless of the user's psychological readiness or available bandwidth. If a user is actively recovering from burnout, receiving a high-intensity "Growth" assignment will trigger abandonment. Conversely, a user with high momentum will easily become bored by foundational pacing. The system needs a strategic orchestrator capable of parsing a user's psychological state and mathematically mapping out a customized, intensity-gated curriculum architecture.

### Solution
FR32 formally defines the **Capacity Tracking and 4-Week Roadmap Generation Protocol (DEP-ENG-027)**, operated by Agent Atlas (The Strategic Planner). When a user completes onboarding, Atlas ingests their `ContextExtraction` (provided by Aria) and classifies them into one of five Capacity Tracks: `Recovery`, `Foundation`, `Growth`, `Momentum`, or `Peak`. Atlas then dynamically builds a 30-day (4-week) ritual roadmap. This roadmap strictly enforces a `4+1+2` template (4 active days, 1 reflection day, 2 rest days) and programmatically ramps up the intensity load by `+10%` per week, while physically enforcing anti-escalation parameters to protect vulnerable users.

### Scope
**In scope:**
- Stage 1: The Initial Capacity Track Classification (Recovery → Peak).
- Stage 2: The 4-Week structural roadmap assembly (`4+1+2` block generation).
- Stage 3: The +10% Weekly Progressive Overload logic.
- Stage 4: Strict compliance with Anti-Pattern constraints (e.g., the 14-day hold).

**Out of scope:**
- The *generation* of the daily content text. Atlas builds the *architecture* (the empty skeleton framework). Artisan fills the frame later.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-027` | 30-Day Ritual Roadmap | OUTPUT — The master timeline assigning an intensity value and ritual category to every single day for a 4-week span. |
| Atlas | The Strategic Planner | AGENT — The intelligence block evaluating capacity and writing the schedule. |
| `atlas.py` | Implementation Script | LOGIC — Executes the `+10%` multiplier loop and the `4+1+2` matrix grid. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Progressive Overload Principle** | Thomas Delorme | 1945 | Originally formulated for physical resistance training, the principle dictates that adaptation (growth) only occurs when the load incrementally exceeds the system's current capacity, followed by mandatory rest. Atlas applies this to psychological capacity—incrementing cognitive load (`+10%`) slightly above the baseline each week, while enforcing 2 absolute rest days for neural consolidation. |

### Technical Decisions
1. **The 4+1+2 Constraint:** This is mechanically hard-coded. No LLM logic is allowed to decide "maybe this user needs 6 active days". The array matrix for a 7-day week is definitively structured as: `[Active, Active, Rest, Active, Active, Reflection, Rest]`. The LLM only gets to pick *which* specific active ritual occupies the `Active` slots.
2. **The 14-Day Recovery Block:** A user placed in the `Recovery` track cannot be escalated out of that track for the first 14 days, regardless of what they say in their transcripts. This is a non-negotiable psychological safety guardrail preventing the system from accelerating deeply exhausted users too quickly just because they experienced a minor dopamine spike on Day 4.

---

## 4. Implementation Plan

### Stage 1: Capacity Track Classification
*Script:* `strategy/atlas.py`
*Agent Name:* Atlas
*Inputs:* `DEP-ENG-006` (Context Premise), Onboarding Assessment Score.
*Outputs:* `Capacity_Track` Enum.
*Failure Condition:* Atlas fails to classify and defaults to `null`.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Atlas reads Aria's latest Context Premise outputs and the user's base TTT (Truth, Trauma, Triumph) state.
2. Evaluates the enum mapping logic against the ContextExtraction psychometric array scores (0.0–1.0 scale): # REVISED: Replacing qualitative descriptors with explicit numeric thresholds per Architect decision.
   - **Recovery Track:** fear_score ≥ 0.8 OR coping_exhaustion ≥ 0.75
   - **Foundation Track:** fear_score 0.6–0.79 AND coping_exhaustion < 0.75
   - **Growth Track:** fear_score 0.4–0.59 AND agency_score ≥ 0.5
   - **Momentum Track:** fear_score 0.2–0.39 AND agency_score ≥ 0.65
   - **Peak Track:** fear_score < 0.2 AND agency_score ≥ 0.8
3. Assigns the `Capacity_Track` to the user's profile in the Neo4j ontology.

### Stage 2: 4-Week Base Matrix Generation
*Script:* `strategy/atlas.py`
*Inputs:* `Capacity_Track`
*Outputs:* 28-Day base grid array.
*Failure Condition:* The generated array has fewer than 28 elements or violates the rest structure.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Atlas instantiates a clean 28-day array.
2. It loops 4 times (4 weeks). For each loop, it stamps the `4+1+2` structural template. 
   *(Example Week: Day 1=Active, Day 2=Active, Day 3=Rest, Day 4=Active, Day 5=Active, Day 6=Reflection, Day 7=Rest)*.
3. It sets milestones at array index `[6, 13, 20, 27]`.

### Stage 3: The +10% Progressive Overload Curve
*Script:* `strategy/atlas.py`
*Inputs:* 28-day base matrix, `Capacity_Track` baseline load factor.
*Outputs:* `DEP-ENG-027` Roadmap JSON.
*Failure Condition:* Intensity calculation produces an integer overflow or NaN.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Atlas sets the `Week 1` Intensity Base (e.g., Recovery = 0.20, Growth = 0.60).
2. For Week 2, the `Active` days receive `Intensity = Base * 1.10`.
3. For Week 3, the `Active` days receive `Intensity = Previous * 1.10`.
4. For Week 4, the `Active` days receive `Intensity = Previous * 1.10`.
5. For all weeks, `Rest` days are hard-coded to `Intensity = 0.00`.
6. Atlas selects the specific rituals from the database that match the requisite float `Intensity` thresholds for the `Active` blocks.

### Stage 4: Anti-Escalation Check (The 14-Day Block)
*Script:* `strategy/atlas.py`
*Inputs:* Proposed `DEP-ENG-027`
*Outputs:* Validated Roadmap.
*Failure Condition:* A `Recovery` track user is upgraded to `Foundation` on Day 8.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Pre-commit hook: The system checks if `User.Track == "Recovery"`.
2. If `TRUE`, it evaluates the user's lifecycle day (from Day 1 onboarding).
3. If `< 14 days`, it actively blocks any dynamic track escalations proposed by mid-week sentiment scans. The intensity curve can rise `+10%` within the Recovery tier scope, but the user cannot cross the boundary into `Foundation` until `Day 15`.

---

## 5. Primary Output Schema (DEP-ENG-027)

**Schema Name:** `atlas_30_day_roadmap.json`

```json
{
  "user_id": "USR-199X",
  "coach_id": "EMI",
  "generation_date": "2026-03-13T00:00:00Z",
  "capacity_track": "Recovery",
  "roadmap_architecture": [
    {
      "day": 1,
      "week_number": 1,
      "type": "ACTIVE",
      "assigned_intensity_load": 0.20,
      "ritual_category_selection": "Grounding Practice"
    },
    {
      "day": 2,
      "week_number": 1,
      "type": "ACTIVE",
      "assigned_intensity_load": 0.20,
      "ritual_category_selection": "Breathing Protocol"
    },
    {
      "day": 3,
      "week_number": 1,
      "type": "REST",
      "assigned_intensity_load": 0.00,
      "ritual_category_selection": "NONE"
    }
    // ... continues for 28 days ...
  ],
  "milestone_checkpoints": [7, 14, 21, 28],
  "anti_pattern_locks": {
    "escalation_lock_expiry": "14_DAYS",
    "track_locked_until": "2026-03-27T00:00:00Z"
  }
}
```

---

## 6. Backward Compatibility Fallback
If Aria's Context Extraction payload fails to provide sufficient psychometric data to make an accurate Track classification, Atlas completely defaults to the `Foundation` track. The system will never default to `Growth` or `Peak` on partial data, ensuring it never inadvertently burns out a highly stressed user who failed to transmit proper context indicators.

---

## 7. Tasks

- [ ] **Task 1:** Encode the Enum mapping logic in `strategy/atlas.py` linking Aria's Context Premise outputs to the 5 Capacity Tracks.
- [ ] **Task 2:** Build the `array_matrix_generator` function that programmatically produces the 28-day json object strictly enforcing the `4+1+2` template without LLM variance.
- [ ] **Task 3:** Implement the exponential `+10%` load calculator for Weeks 2, 3, and 4, ensuring it rounds safely to standard float formats and assigns it solely to `ACTIVE` blocks.
- [ ] **Task 4:** Build the programmatic query connecting computed `Intensity` scores to matching ritual categories in the Supabase content library (e.g., Intensity 0.82 maps to "Shadow Work", Intensity 0.20 maps to "Grounding").
- [ ] **Task 5:** Enforce the 14-day Anti-Escalation guard logic within `atlas.py` to hardline the `Recovery` track quarantine.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Track Designation):** A user whose last Context Extraction heavily featured the term "exhausted" and "giving up" (Coping Mechanism = Withdrawal). Atlas successfully maps them strictly to the `Recovery` track. *Failure Example:* Atlas maps a highly exhausted user to the `Momentum` track because they mentioned wanting to "succeed", resulting in immediate user burnout.
- [ ] **AC2 (The 4+1+2 Matrix Constraint):** Atlas generates a 28-day JSON roadmap. A program runs against the JSON checking day types. Assert that exactly 16 days are `ACTIVE`, 4 are `REFLECTION`, and 8 are `REST`. *Failure Example:* Atlas's LLM hallucinates an aggressive "push week" yielding 6 Active days and 1 Rest day, breaking the core physiological methodology.
- [ ] **AC3 (Progressive Overload Math):** The intensity variable on Week 1 Day 1 is `0.50`. Assert the intensity variable on Week 2 Day 1 is precisely `0.55` (a +10% increment). *Failure Example:* The baseline calculation adds +1.10 instead of substituting via multiplication, throwing an out-of-bounds `1.60` intensity map that breaks downstream generation.
- [ ] **AC4 (The 14-Day Lock):** A user is designated `Recovery` on Day 1. On Day 7, a sentiment sweep assesses high positivity. The Mid-Cycle Rebalancer attempts to push them to `Foundation`. Assert the Atlas system refuses the state change and retains them in `Recovery` due to the 14-day hold. *Failure Example:* The system upgrades the user pre-maturely, breaking the psychological safety limit.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-006` (Context Premise) | Upstream | Required for base track assignment. |
| Supabase Ritual Library | Database | Required to map float intensities to actual category strings. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **The Matrix Validator Test:** Run the `4+1+2` matrix generator function 100 times isolated from the LLM. Assert 100% of the returned arrays have a `day[2]` and `day[6]` typed precisely as `"REST"`.
- **The Exponential Overload Test:** Initialize a baseline user at `0.10` limit. Run the 4-week loop. Assert Week 4 intensity strictly equals mathematical expected value `((0.10 * 1.1) * 1.1) * 1.1 = 0.133`.

### Integration Tests
- **Ritual Matching E2E:** Inject a fully formed `DEP-ENG-027` Roadmap JSON (with generated float intensities) into the pipeline step that calls Artisan for the Daily generation. Assert the correct class of ritual (e.g. Grounding vs. Deep Dive) is correctly fetched from Supabase based on the intensity metadata.
- **Onboarding Pipeline Hand-off:** Run the full Genesis pipeline. At Step 8, transition the thread to Atlas. Assert Atlas can successfully read the newly onboarded user's psychometric profile and instantaneously produce the 28-day curriculum.

### Safety Tests (ADR-01 Quarantine Security)
- **Track Assignment Quarantine:** Evaluate Coach A's client and Coach B's client concurrently. Assert Atlas writes Coach A's roadmap output string exclusively to Coach A's isolated Neo4j relationship tenant schema, preventing a track misallocation across differing global contexts.
