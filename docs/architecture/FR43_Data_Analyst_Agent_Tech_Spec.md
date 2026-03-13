# Tech-Spec: FR43 — Data Analyst Agent (DEP-ENG-038)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** CE_Data_Infrastructure_v1.0 (§IV), PRD FR43
**Skill Implementation:** `skills/analyst/performance_evaluator/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CE_Data_Infrastructure_v1.0.docx.md`

---

## 2. Overview

### Problem Statement
Collecting raw performance metrics (FR42) solves data visibility, but it does not solve "System Stagnation." If the CCP compiles 40 scripts a month using a static set of pedagogical constraints, it will continue generating the same archetypes regardless of market reception. An agent generating content without interpreting its own performance history is operating at a Volume × 0 compound learning state, which merely leads to noise at scale.

### Solution
FR43 establishes the **Data Analyst Agent (DEP-ENG-038)**. This agent runs on a strict weekly cadence (or manual trigger) to ingest the raw metrics gathered in Supabase. It doesn't just "report" data; it *evaluates* it through 6 specific algorithmic matrices (Arc Performance, Psychological Mode, CRAL Impact, etc.). Based on statistically significant trends, it authors `parameter_update.json`, a system-facing payload that automatically mutates the CCF compiler weights for the upcoming production cycle. 

### Scope
**In scope:**
- The 3-Phase Execution Architecture (Data Prep, Pattern Evaluation, Output).
- The 6 Evaluation Frameworks defining the analytical reasoning.
- The Notion API integration for the Coach-facing intelligence report.
- The `parameter_update.json` structure (`DEP-ENG-038`).

**Out of scope:**
- The actual *retrieval* of data from social platforms (handled by FR42).
- The execution of the updated weights (handled by the CCF skill builder/compiler).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-038` | Parameter Update Payload | OUTPUT — The structured JSON file that alters future CCF compilations. |
| Supabase `content_performance` | The Raw Data | INPUT — The 7-day snapshots gathered by Python CRON. |
| Notion `System Intelligence` DB | The Coach Report | OUTPUT — The plain-language translation of the technical parameter updates. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Reinforcement Learning from Human Feedback (RLHF)** | Ouyang | 2022 | The Data Analyst Agent acts as an automated RLHF proxy. Instead of users giving manual "thumbs up" to outputs, the Agent uses audience virality metrics (Shares + Saves) as the absolute reward signal to re-weight internal generation policies. |

### Technical Decisions
1. **7-Day Maturity Gate:** The agent *only* evaluates data that has reached its 7-day snapshot. Evaluating 24-hour data leads to extreme volatility in parameter weighting, causing the system to chase immediate virality rather than stable, repeatable resonance patterns.
2. **Minimum Sample Threshold Guard:** The agent refuses to execute parameter updates if `N < 5` for a specific arc type. Pattern detection on `< 5` samples is statistically invalid and causes algorithmic whiplash.
3. **Dual Output Streams:** The system explicitly separates the *technical* output (`parameter_update.json`) from the *human* output (Notion Intelligence Report) to ensure the coach is never burdened with reviewing raw JSON weights.

---

## 4. Implementation Plan

### Stage 1: Data Preparation
*Agent:* Data Analyst
*Inputs:* `content_performance`, `fingerprint_archive`, `scripts` (Supabase).
*Outputs:* `evaluation_payload.json` (Internal memory object).
*Failure Condition:* Missing primary keys prevent joining the performance data to the narrative metadata, rendering the metrics meaningless.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Connect via Supabase RPC.
2. Execute `SELECT` on `content_performance` where `day_7_snapshot IS NOT NULL` AND `analyst_reviewed = false`.
3. Apply `INNER JOIN` to `fingerprint_archive` (to retrieve `archetype`, `mood_state`, `regulatory_frame`, `cral_coverage_status`).
4. Validate minimum threshold (`N >= 10` globally, `N >= 5` per arc-type).
   - *Resolution Rule:* If threshold not met, set `status = INSUFFICIENT_DATA`, log a warning, and exit pipeline cleanly.
5. Structure the payload grouping by `coach_id` → `arc_type` → `mood_state`.

### Stage 2: Pattern Evaluation (The 6 Matrices)
*Agent:* Data Analyst
*Inputs:* `evaluation_payload.json`.
*Outputs:* Internal Analytical Vectors.
*Failure Condition:* Agent identifies mathematical anomalies (e.g., bot farms skewing likes without watch-time) and over-weights a bad asset.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
The Agent executes 6 LLM-assisted Python Pandas evaluation frameworks:
1. **Arc Performance:** Ranks the 13 CMF arcs by `engagement_rate`. Identifies Top 3 / Bottom 3.
2. **Psychological Mode:** Maps highest resonance to Mood × Regulatory Frame (e.g., Status × Promotion).
3. **CRAL Impact:** Correlates specific `M1-M7` CRAL elements to `shares` (virality) vs `saves` (loyalty).
4. **CRAL Degradation:** Calculates the exact CTR/Engagement penalty when CRAL coverage = `PARTIAL` vs `COMPLETE`.
5. **Platform Delta:** Identifies format disparities (e.g., Reels outperforming Shorts by 3x natively).
6. **Timing Analysis:** Identifies day/hour clusters for peak engagement.

### Stage 3: Intelligence Output (The Updates)
*Agent:* Data Analyst
*Inputs:* Evaluated Vectors.
*Outputs:* `parameter_update.json` (`DEP-ENG-038`), Notion Report, Supabase Row Updates.
*Failure Condition:* Target Notion Database ID is invalid or missing in `coach_config`.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. **Output A (Coach Report):** Uses an LLM pass to translate the vectors into plain-language. Calls Notion API `POST /v1/pages` to write the summary to the `System Intelligence` database.
2. **Output B (System Payload):** Generates `parameter_update.json` mapping the required weight adjustments (INCREASE/DECREASE) based on the metrics.
3. **Output C (Archive Tagging):** Executes a bulk Supabase `UPDATE`, setting `analyst_reviewed = true` and writing the `Performance Tag` (HIGH/AVERAGE/UNDER) to prevent double-processing next week.

---

## 5. Primary Output Schema (DEP-ENG-038)

**Schema Name:** `parameter_update.json`

```json
{
  "coach_id": "uuid-8899-2233",
  "evaluation_period": "2026-W11",
  "arc_priority_weights": {
    "Achievement_Story": 1.4,
    "Myth_Debunk": 0.7,
    "Transformation_Arc": 1.1
  },
  "cral_moment_priority": {
    "M7_RELATABLE": "HIGH",
    "M2_BELIEVABLE": "HIGH",
    "M1_RELEVANT": "MEDIUM"
  },
  "mode_routing_adjustments": {
    "Processing_Prevention": "INCREASE",
    "Status_Promotion": "DECREASE"
  },
  "scheduling_updates": {
    "instagram": {"optimal_days": ["TUE","THU"], "optimal_hours": [8,19]},
    "linkedin": {"optimal_days": ["MON","WED"], "optimal_hours": [7,12]}
  },
  "next_cycle_directive": "Prioritize Achievement Story x Prevention Frame. CRAL degradation currently causing 40% reach penalty; strictly enforce COMPLETE coverage.",
  "timestamp_generated": "2026-03-16T06:00:00Z"
}
```

---

## 6. Backward Compatibility Fallback
If the Data Analyst Agent fails to execute (e.g., due to an API timeout with the LLM orchestrator), the CCF compilation pipeline smoothly defaults to the last known `parameter_update.json` on record. If no historical file exists, it defaults to `1.0` (baseline neutrality) for all priority weights, guaranteeing that production does not stall due to an intelligence layer outage.

---

## 7. Tasks

- [ ] **Task 1:** Write the scheduled Python script trigger logic that checks the `analyst_reviewed` thresholds every Monday at 06:00 UTC.
- [ ] **Task 2:** Write the Supabase SQL `JOIN` query required to merge `content_performance` with `fingerprint_archive` and `scripts`.
- [ ] **Task 3:** Implement the 6 Pandas dataframe evaluation functions.
- [ ] **Task 4:** Write the Langchain/Pi Agent prompt that translates the Pandas dataframes into the plain-language Notion Markdown report.
- [ ] **Task 5:** Build the `parameter_update.json` generation and the subsequent Supabase `UPDATE` loop to mark the batch as processed.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Minimum Sample Guard):** Force-trigger the Agent on a database with only 3 unevaluated 7-day snapshots. Assert the Agent logs `INSUFFICIENT_DATA_THRESHOLD_MET` and aborts without touching the DB. *Failure Example:* The Agent processes 3 random posts and tells the CCF that "Humorous Content" is 100% ineffective because the sample size was too small.
- [ ] **AC2 (Weight Mutation):** Mock a data set where `Myth_Debunk` arcs average 0.02 engagement, and `Achievement_Story` averages 0.15 engagement. Run the pipeline. Assert the generated `parameter_update.json` returns an `arc_priority_weights` value `> 1.0` for Achievement and `< 1.0` for Myth. *Failure Example:* The system fails to mathematically prefer the higher-performing format.
- [ ] **AC3 (Notion Human Translation):** Pass a completed parameter JSON and assert the Notion Report successfully translates `arc_priority_weights: Myth_Debunk 0.7` into human-readable text: "We are temporarily reducing the frequency of Myth Debunk videos as they are underperforming baseline." *Failure Example:* The Coach opens Notion and sees raw JSON code or Pandas dataframes.
- [ ] **AC4 (Idempotent Tagging):** Run the Agent over 15 unreviewed posts. Run it a second time 1 minute later. Assert the second run processes 0 posts because the first run successfully updated `analyst_reviewed = true`. *Failure Example:* The agent evaluates the same 15 posts every week indefinitely.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Supabase `fingerprint_archive` | Internal | Vital for joining post-publication analytics back to pre-publication psychological parameters. |
| Notion `System Intelligence` DB | External | The required output vector for the human-facing report. |
| Pandas / Python | Internal | Strictly required for deterministic evaluation; the LLM should *not* do raw math, it should interpret the Pandas output. |

---

## 10. Testing Strategy

### Unit Tests
- **CRAL Degradation Math:** Pass a mocked dataframe containing 5 `COMPLETE` coverage posts averaging 1000 reach, and 5 `PARTIAL` coverage posts averaging 600 reach. Assert the Pandas evaluation function accurately outputs a 40% degradation penalty warning.

### Integration Tests
- **The Intelligence Handshake:**
  1. Populate Supabase with 15 unevaluated snapshot rows.
  2. Trigger the Data Analyst Agent.
  3. Validate `parameter_update.json` appears in the correct S3/Supabase storage bucket.
  4. Validate the Notion API successfully appended a new page to the Coach's Intelligence DB.

### Safety Tests (ADR-01 Quarantine Security)
- **Cross-Tenant Vector Validation:** Load 10 rows for Coach A and 10 rows for Coach B. Assert that the resulting `parameter_update.json` for Coach A does not contain any weighting influences derived from Coach B's data, strictly maintaining the tenant firewall during Pandas operations.
