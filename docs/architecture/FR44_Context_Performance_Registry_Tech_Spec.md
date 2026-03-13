# Tech-Spec: FR44 — Context Performance Registry (DEP-ENG-045)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** CCP_Architecture_V5.0 (§8.2, §9), PRD FR44
**Skill Implementation:** `skills/research/context_performance_registry/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Architecture_V5.0.docx.md`

---

## 2. Overview

### Problem Statement
The JIT Compiler's Research Planner uses algorithmic routing rules to determine which CMM layers (Cultural Memory Map), stories, or humor mechanisms to deploy for a given coaching hook. However, static rules do not learn. If "Industry Mythology" constantly underperforms "Formative Texts" for a specific coach's audience, a static system will continue deploying Industry Mythology blindly because "the rules said so."

### Solution
FR44 establishes the **Context Performance Registry (DEP-ENG-045)**. This is the memory layer that transforms the Context Reasoning Layer from a static router into a self-improving engine. Every compilation session logs its specific Context Selection Object (the exact ingredients chosen) and the *rationale* for choosing them into a Supabase table. As the Data Analyst Agent retrieves performance metrics (FR42/FR43), the registry links the *reasoning* to the *result*. Over time, the compiler learns to override default routing priors in favor of empirically validated, audience-specific patterns.

### Scope
**In scope:**
- The Supabase schema for `context_performance_registry`.
- The generation of the Context Selection Object by the Research Planner (Phase 1).
- The feedback mechanism: Data Analyst Agent updating the registry with performance outcomes.
- The minimum session thresholds required before the system is allowed to override defaults.

**Out of scope:**
- The raw scraping of Publer analytics (handled in FR42).
- The actual execution of the research directive (handled in Phase 2).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-045` | Context Performance Registry | STORAGE — The Supabase table matching compiled context reasoning against eventual market performance. |
| Research Planner Phase 1 | Context Reasoner | INPUT — The agent that produces the logic and the Context Selection Object. |
| Data Analyst Agent | The Evaluator | UPDATER — The agent that flags which reasoning patterns consistently outperform defaults. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Test-Time Compute & Verification** | D. Silver / DeepMind | 2023 | Demonstrates that LLMs improve substantially when forced to explicitly state their reasoning paths (rationale) *before* arriving at a concluding answer, allowing post-hoc analysis of *why* an AI made a routing choice, rather than just grading the final output. |

### Technical Decisions
1. **Rationale Logging:** We do not just log "You chose M4." We log the LLM's explicit reasoning string for *why* it chose M4. This allows the Data Analyst to identify structural logic patterns that succeed, rather than just brute-force A/B testing ingredients.
2. **Cold Start Fallback (Confidence Scoring):** The registry starts entirely empty for a new coach. Therefore, Phase 1 Context Reasoning must output a `confidence_score`. If `N < 5` previous sessions match the current variables, confidence is `< 0.3`. The system proceeds using default hardcoded rules but flags the output for manual coach review to build baseline truth data safely.
3. **Threshold Gates:** The Data Analyst is mathematically prohibited from altering routing rules until a coach hits a minimum of 20 recorded sessions. A sample size smaller than this results in algorithmic overfitting.

---

## 4. Implementation Plan

### Stage 1: Registry Initialization & Handoff
*Agent:* Orchestrator / Startup Script
*Inputs:* Coach Onboarding Config.
*Outputs:* Instantiated `context_performance_registry` table.
*Failure Condition:* Table not created, causing Research Planner to throw 500 errors on first write attempt.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. During coach onboarding (V5.0 Step 0-D), deploy the `context_performance_registry` Supabase table schema (See Section 5).

### Stage 2: Context Selection (Pre-Compilation)
*Agent:* Research Planner (Phase 1 Context Reasoning Block)
*Inputs:* `[moment_id]`, `[mood_state]`, `[archetype]`, `[regulatory_frame]`, `[arc_phase]`.
*Outputs:* `Context Selection Object`.
*Failure Condition:* Agent fails to generate a rationale string, violating the Test-Time Compute standard.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Research Planner queries the `context_performance_registry` for similar prior sessions (`moment_id == current` AND `regulatory_frame == current`).
2. **Resolution Rule (Confidence):**
   - If `matched_sessions < 5`: `confidence_score = 0.2` (Rely entirely on default V5.0 rules).
   - If `matched_sessions >= 5` AND `outperformed_default = true` in history: `confidence_score = 0.8` (Override default rule and select the empirically proven CMM combination).
3. Evaluates 3 questions: 
   - Is there a relevant story in the Coach Story Archive? (`DEP-ENG-024`)
   - Which CMM layers apply, and should defaults be overridden? (`DEP-ENG-023`)
   - Which Humor Mechanism fits the current coupling phase?
4. Generates the structured `Context Selection Object` and passes it to Phase 2 (Directive Generation).
5. Writes the `Context Selection Object` directly into the Supabase registry.

### Stage 3: The Performance Handshake
*Agent:* Data Analyst Agent
*Inputs:* `content_performance` (from Publer), `context_performance_registry`.
*Outputs:* Registry Mutations.
*Failure Condition:* Data Analyst incorrectly overwrites historically valid sessions with anomalous data.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. During the weekly execution cycle (FR43), the Data Analyst takes the 7-day and 30-day performance snapshots from the `content_performance` table.
2. It executes an `UPDATE` on the `context_performance_registry` table, explicitly mapping the `engagement_rate`, `saves`, and `shares` to the original `Universal_Asset_ID`.
3. **Resolution Rule (Outperformed Default):** 
   - If the recorded `engagement_rate` is > 1.2x the coach's historical baseline for this specific `arc_phase`, the agent updates the column `outperformed_default = true`.
   - If <= baseline, `outperformed_default = false`.

### Stage 4: Rule Refinement (The Efficiency Report)
*Agent:* Data Analyst Agent (Quarterly/50-session cycle)
*Inputs:* Fully populated `context_performance_registry`.
*Outputs:* `Context_Efficiency_Report.md`.
*Failure Condition:* Agent hallucinates a pattern on `N=2` data points.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. **Hard Threshold Gate:** `IF total_rows < 50` → TERMINATE evaluating new rules. Pass.
2. If `N >= 50`, the Analyst identifies combinations where `outperformed_default == true` at a frequency greater than 60%.
3. (e.g., "When arc phase is Turning Point and regulatory frame is Prevention, CMM Collective Wound History outperforms CMM Formative Texts 72% of the time").
4. Generates a markdown report for human Operator approval before hardcoding the new rule into the `skills/research/planner` default configurations.

---

## 5. Primary Output Schema (DEP-ENG-045)

**Schema Name:** `supabase_cpr_row_insertion.json` (Structured as the `Context Selection Object` created in Phase 1)

```json
{
  "Universal_Asset_ID": "JP-CCF-20260313-001-CAROUSEL",
  "coach_id": "coach-v5-001",
  "moment_id": "M4_RESONANT",
  "context_combination": {
    "cmm_layers": ["Collective Wound History", "Aspirational Archetype"],
    "story_archive_utilized": true,
    "story_id": "story-7766",
    "humor_mechanism": "Violated Expectation (Status)",
    "regulatory_frame": "Promotion",
    "arc_phase": "Inciting Incident"
  },
  "selection_rationale": "Default rule implies Formative Texts. However, registry history indicates that for the Promotion frame during Inciting Incidents, this audience responds 1.5x better when we anchor to the Collective Wound first. CMM layers overridden.",
  "confidence_score": 0.85,
  "outride_flags_triggered": ["CMM_LAYER_OVERRIDE"],
  "performance_outcome": null, 
  "outperformed_default": null,
  "created_at": "2026-03-20T10:15:00Z"
}
```
*(Note: `performance_outcome` and `outperformed_default` are NULL at time of creation. They are populated by the Data Analyst in Stage 3, days/weeks later).*

---

## 6. Backward Compatibility Fallback
If the Supabase `context_performance_registry` table becomes inaccessible during compilation (Stage 2), the Research Planner encounters a 500 error when querying history. The `DamageControl` extension catches this, logs `DB_UNAVAILABLE`, and physically forces the compiler to rely on the static V5.0 default routing logic. The session continues uninterrupted, generating high-quality baseline content without the compounding intelligence injection.

---

## 7. Tasks

- [ ] **Task 1:** Execute the Supabase migration script to construct the `context_performance_registry` table schema directly mapping to Section 5.
- [ ] **Task 2:** Refactor the Research Planner from a 1-phase compiler to a 2-phase compiler (Reasoning -> Directive Generation) requiring the LLM to output its rationale explicitly.
- [ ] **Task 3:** Write the Python `cpr_query.py` tool. This tool enables the Research Planner to query `SELECT * FROM context_performance_registry WHERE moment_id = X AND regulatory_frame = Y AND outperformed_default = TRUE`.
- [ ] **Task 4:** Update the Data Analyst Agent (`FR43`) workflow. Add a final downstream Python task: After writing `content_performance`, `UPDATE context_performance_registry SET performance_outcome = X WHERE Universal_Asset_ID = Y`.
- [ ] **Task 5:** Build the threshold enforcer rule: Force `confidence_score = 0.2` if the `cpr_query` returns `< 5` rows.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Rationale Extraction):** Submit an Orchestrator handoff to the upgraded Research Planner. Assert the LLM generates a valid `Context Selection Object` JSON containing both the `context_combination` block AND a strictly populated `selection_rationale` string explaining *why* it chose those specific CMM layers. *Failure Example:* The system outputs just the arrays with no rationale, breaking the fundamental RLHF learning loop.
- [ ] **AC2 (Sparse Data Fallback):** Wipe the test registry to `N=2` rows. Submit a session. Assert the `cpr_query.py` tool returns the rows, but the Research Planner explicitly sets `confidence_score = 0.2` and executes using default routing rules due to insufficient sample size. *Failure Example:* The system overrides standard operations based on a sample size of 2, creating algorithmic hallucination.
- [ ] **AC3 (Performance Handshake):** Trigger the Data Analyst Agent on a 7-day milestone. Assert that the agent takes the `engagement_rate` decimal from the Publer sync and successfully writes it back to the exact `Universal_Asset_ID` in the `context_performance_registry`, mutating the `outperformed_default` boolean correctly relative to the coach baseline. *Failure Example:* The registry remains full of `NULL` performance records because the `Universal_Asset_ID` mapping failed.
- [ ] **AC4 (Override Execution):** Populate the registry with `N=40` sessions proving that `Pattern X` always beats `Pattern Y` for `M1_RELEVANT`. Run a compilation matching those parameters. Assert the Research Planner actively overrides the `Pattern Y` default, sets an `override_flag`, and sets `confidence_score > 0.8`. *Failure Example:* The system ignores its own database and continuously generates `Pattern Y` despite massive evidence against it.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Supabase `content_performance` | Internal | The ground-truth data evaluated by the Data Analyst during Stage 3 to write back to the CPR. |
| Coach Story Archive (`DEP-ENG-024`) | Internal | The system first checks if a literal coach story beats an abstract reasoning layer before diving into CMMs. |
| The 11 Pi Extensions | Internal | Needed during Stage 2: `InteractComp` ensures the DB query works, `TillDone` enforces the json schema output. |

---

## 10. Testing Strategy

### Unit Tests
- **Confidence Math validation:** Test the Research Planner logic. Provide `N=4` returned rows. Assert confidence returns `< 0.3`. Provide `N=15` returned rows. Assert confidence returns `> 0.6`.
- **Baseline Boolean Test:** Pass an engagement rate of `0.05` to the `Stage 3` evaluator, against a historical coach average of `0.04`. Assert `outperformed_default` returns `True`.

### Integration Tests
- **The Intelligence Lifecycle:**
  1. Trigger Phase 1 Context Reasoning.
  2. Validate the `.json` structure is correctly inserted into the Supabase table with `NULL` metrics.
  3. Pause. Inject mocked 7-day Publer metrics into the Data Analyst pipeline.
  4. Query the `context_performance_registry`.
  5. Assert the originally `NULL` metrics are now populated with exact numerical distributions and the `outperformed_default` boolean is resolved.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Context Bleed:** Execute parallel reasoning queries for Coach A and Coach B simultaneously. Assert that Coach A's Research Planner is strictly walled off via Row-Level Security (RLS) and cannot see or use Coach B's `Context Performance Registry` logic to alter its own confident scores.
