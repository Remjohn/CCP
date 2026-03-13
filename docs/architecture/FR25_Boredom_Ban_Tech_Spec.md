# Tech-Spec: FR25 — Boredom Ban Novelty Enforcement (DEP-PROTO-015)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §8.2.4 (Boredom Ban), JIT_Skill_Compiler_Architecture
**Skill Implementation:** `orchestration/ccf-multi-theme/` & `research/critic/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\JIT_Skill_Compiler_Architecture.docx.md`

---

## 2. Overview

### Problem Statement
In automated high-volume content production (36 variations per week), LLMs inevitably orbit their preferred "safe" analogies, narrative structures, and semantic themes. Without forced variance, a coach's feed will feature the same "climbing a mountain" metaphor or "three steps to freedom" listicle structure every two weeks. This predictable cadence induces audience fatigue (boredom), destroying engagement metrics regardless of how factually accurate the content is. 

### Solution
FR25 implements the **Boredom Ban (Novelty Enforcement) Protocol (DEP-PROTO-015)**. The system utilizes `MemoryFolder` (Episodic Memory lookup) to actively track the Fingerprint IDs and extracted semantic/structural payloads of all content generated over a sliding 8-week window. Enforced heavily by Agent Grâce (Draft Tester), if the orchestrator detects an overlap exceeding the similarity threshold, it immediately Rejects the draft and invokes a `TillDone` rewrite cycle. The LLM is explicitly commanded to mutate the offending variable (metaphor, theme, or structure) before it is allowed back into the production queue.

### Scope
**In scope:**
- Stage 1: Theme Discovery Novelty Check.
- Stage 2: Wisdom Forge Metaphor Extraction.
- Stage 3: Draft Tester Evaluation (Agent Grâce).
- Semantic overlap thresholds and `TillDone` generation resets.

**Out of scope:**
- Discarded content not published to the audience (the clock only measures against what the audience actually saw or what survived Compilation).
- Routine memory purges (Episodic Memory handles 8-week discarding intrinsically).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Concept | Name | Role in This Pipeline |
|---|---|---|
| `DEP-PROTO-015` | Novelty Enforcement Protocol | LOGIC — Overarching rule set for duplication checks. |
| `MemoryFolder` | Episodic Memory Store | INPUT — Database containing the 8-week sliding window of past creations. |
| Grâce (Draft Tester) | Novelty Evaluator Agent | AGENT — Gatekeeper assessing the compiled draft against historical memory. |
| `DEP-ENG-020` | Fingerprint Archive | INPUT — Supplies structural history (which Archetypes have been overused). |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Optimal Incongruity** | - | - | Attention is highest when an input is sufficiently familiar to be recognized but incongruous enough to be surprising. Repetition destroys incongruity. The Boredom Ban forces exactly this required delta. |

### Technical Decisions
1. **Three-Vector Comparison:** Novelty is enforced across three vectors independently: `Thematic Payload` (are we talking about the same specific problem?), `Structural Pattern` (are we using the same Archetype?), and `Metaphorical Vehicle` (are we using the same analogy?). 
2. **Early Elimination:** The enforcement protocol runs multiple times—first at Theme Discovery, again at Wisdom Forge, and finally at Draft Evaluation. Catching a duplicate theme early saves downstream generation tokens. 

---

## 4. Implementation Plan

### Stage 1: Early-Phase Theme Discovery Check
*Agent Name:* Divine (Theme Generator)
*Inputs:* Output of `dynamic-theme-generator`, `MemoryFolder` (Episodic).
*Outputs:* `final_selection.md` (2 verified novel themes).
*Failure Condition:* Theme collision circuit breaker.
If generated themes collide with the 8-week Fingerprint Archive on 3 consecutive attempts:
1. Set flag: `FATIGUE_OVERRIDE_GRANTED: true`
2. Bypass the collision check for this batch slot only
3. Log override to operator dashboard with collision details for manual review
4. Proceed with generation # REVISED: Replaced infinite loop with Fatigue Override circuit breaker
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format with override support
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'FATIGUE-OVERRIDE',
  agent_name: 'Divine',
  collision_count: 3,
  override_granted: true,
  slot_id, timestamp }

**Steps:**
1. Divine generates 10 potential theme iterations based on the Trigger-First provocation.
2. Query the `MemoryFolder` extension: *"Return all `thematic_payload` extractions from the past 56 days."*
3. Compare via Embedding Cosine Similarity. If Cosine > `0.80`, flag as `[REJECT: BOREDOM_BAN]`.
4. Rank the remaining novel themes and pass the top 2 forward.

### Stage 2: Mid-Phase Metaphor Extraction (Wisdom Forge)
*Agent Name:* Lionel / Jordan (The Analyst)
*Inputs:* Raw Research RAG output.
*Outputs:* Novel `metaphor_vehicle`.
*Failure Condition:* Fallback generation of generic business analogies if `TillDone` maxes out.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'METAPHOR-EXTRACTION',
  agent_name: 'Lionel-Jordan',
  timestamp }

**Steps:**
1. During the MINE -> FORGE -> TEMPER process of `wisdom-forge`, the agent selects a metaphorical vehicle.
2. Query the `MemoryFolder` extension: *"Return all `metaphor_vehicles` from the past 56 days."*
3. Direct exact-match/synonym overlap check. If TRUE, trigger `TillDone` rewrite: *"Metaphor [X] was used 14 days ago. Generate a new conceptual vehicle from an unrelated domain (e.g., biology, architecture, thermodynamics)."*

### Stage 3: Late-Phase Draft Testing Validation
*Agent Name:* Grâce (Draft Tester)
*Inputs:* `draft_v1.md`, `DEP-ENG-020` Fingerprint History.
*Outputs:* `Validation_Score` or `TillDone Payload`.
*Failure Condition:* Grâce misses a semantic overlap due to token chunking limits.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'DRAFT-TESTER-VALIDATION',
  agent_name: 'Grace',
  timestamp }

**Steps:**
1. This is the final safety net before Stage D Validation (Sophia/Marcus/Chen).
2. Grâce processes the fully assembled draft against the 8-week structural Fingerprint Ledger.
3. If the Coach's output queue assigns `LIST02` (Shocking Listicle) to an idea, but `LIST02` has been used >3 times in the last 14 days: `[REJECT: STRUCTURAL_FATIGUE]`.
4. The generation agent is commanded via `TillDone` to mutate the script into `STORY01` or another assigned, non-fatigued Archetype pattern.

---

## 5. Primary Output Schema (Novelty Check Ledger subset)

**Schema Name:** Attached into the broader `assembly_report.json`

```json
{
  "protocol_invocation": "DEP-PROTO-015_BOREDOM_BAN",
  "8_week_window_start": "2026-01-16",
  "vectors_checked": {
    "thematic_similarity": {
      "score": 0.42,
      "status": "PASS",
      "closest_match_id": "OUT-STORY01-EMI-20260211-001"
    },
    "metaphor_collision": {
      "score": 0.95,
      "status": "REJECT_TILL_DONE_TRIGGERED",
      "offending_vehicle": "Running a marathon",
      "closest_match_id": "OUT-CASE03-EMI-20260301-001"
    },
    "structural_fatigue": {
      "format": "STORY01",
      "frequency_14_days": 1,
      "status": "PASS"
    }
  },
  "till_done_iterations_required": 1,
  "final_clearance": true
}
```

---

## 6. Backward Compatibility Fallback
If the `MemoryFolder` extension is unavailable or the Episodic Memory cache has been wiped (a cold start condition):
1. The 8-week sliding window query will return `null` or `[]`.
2. The `Boredom Ban Protocol` auto-defaults to `PASS`, inserting `[MEMORY_ABSENT_ASSUMED_NOVEL]` in the receipt log.
3. It will not halt the pipeline; it will allow the generation to proceed to prevent halting production for a new coach with no history.

---

## 7. Tasks

- [ ] **Task 1:** Implement the `Episodic-Memory-Query-API` inside the `MemoryFolder` module that accepts a date range (Now - 56 days) and a target specific slice (theme, structure, metaphor) to return a clean comparison list.
- [ ] **Task 2:** Add Cosine Similarity calculation logic (using a lightweight open-source embedding model or direct text classification) to Divine's Theme Discovery prompt check.
- [ ] **Task 3:** Wire Grâce (Draft Tester) directly into the Output Generation loop just before `ccf-validate` receives it, enabling the `TillDone` extension to forcefully instruct Emilio/Artisan to *"Mutate the vehicle."*
- [ ] **Task 4:** Modify JIT Assembly tracking so that `metaphor_vehicle` and `thematic_core` are formalized data properties extracted from every successfully produced script, populating the `MemoryFolder` automatically on post-production.
- [ ] **Task 5:** Add Receipt Chain Guard writes for all 3 Novelty check stages.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Metaphor Collision Catch):** During Wisdom Forge, the LLM attempts to use the "Building a house foundation" metaphor. The coach used this 32 days ago. Grâce explicitly rejects it, and the `TillDone` rewrite log shows the LLM adapting to "Sailing a ship". *Failure Example:* The system allows the house metaphor to pass because 32 days exceeded a hardcoded 30-day (instead of 56-day) limit.
- [ ] **AC2 (Theme Similarity Catch):** Divine suggests the theme "Overcoming Imposter Syndrome" which triggers a `0.85` cosine similarity against a post from 3 weeks prior. Divine drops it and replaces it with "Scaling past $10k months". *Failure Example:* The system crashes trying to compute the embeddings of 50 past scripts.
- [ ] **AC3 (Structural Fatigue Check):** The orchestrator plans 4 `Shocking Listicle` (LIST02) layouts in the same week. Stage 3 structural check throws `[REJECT: STRUCTURAL_FATIGUE]` on the 4th, forcing it to reshape into a `Case Study`. *Failure Example:* The system allows 4 identical listicles to be output, boring the audience.
- [ ] **AC4 (ADR-01 Strict Isolation):** When tracking the 8-week history of Coach Maria's metaphors, the query absolutely cannot read Coach Emilio's Episodic Memory. *Failure Example:* The system prevents Maria from using a marathon metaphor simply because Emilio used it yesterday.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `MemoryFolder` (Episodic) | Upstream | Required for the 8-week array lookup. |
| Cosine Similarity Engine | Internal | Mathematical library required for text-distance measurement on themes. |
| `TillDone` Extension | Downstream | Orchestration tool utilized to force the generative do-overs cleanly. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Cosine Embedding Test:** Feed the Theme similarity checker "Why diets don't work" and "The failure of modern diet culture." Assert a cosine similarity `>0.80` resulting in a `REJECT`. Feed it "Why diets don't work" and "How to strength train." Assert `<0.40` resulting in a `PASS`.
- **String Matching Test:** Test the direct synonym mapping of Metaphor extraction. Feed it "Climbing Mt. Everest" when the DB shows "Scaling a mountain". Assert a collision.

### Integration Tests
- **The Pipeline Rewrite Loop:** Seed the `MemoryFolder` with a specific target output. Run the Weekly Pipeline and purposefully coerce the RAG output to hit the target. Assert that the terminal log explicitly shows `[REJECT_TILL_DONE_TRIGGERED]` from Gracias/Divine, and watch the CLI auto-restart the sub-agent with the negative constraint appended to its generation prompt.
- **Cold Start Pass:** Clear the tenant's Episodic Memory database. Run the pipeline. Assert the Boredom Ban gracefully yields `[MEMORY_ABSENT_ASSUMED_NOVEL]` without throwing `NoneType` errors.

### Safety Tests (ADR-01 Quarantine Security)
- **Cross-Contamination Test:** Seed Coach A's DB with Metaphor "X". Request Metaphor "X" in Coach B's compilation. Assert that Coach B successfully uses it without interference from Coach A's dataset restrictions.
