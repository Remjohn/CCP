# FR-CBCS-04: Information Coping Trajectory Mapper — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F4, PRD §FR-CBCS-04

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CCP update/Context about CCP updates.md`

---

## 2. Overview

### Problem Statement
Most communities and CRMs treat clients as a homogeneous group, assuming standard curriculum pacing works for everyone. However, a client in shock (Position 1) and a client in mastery (Position 5) cannot receive the same information or the same commercial offers without one of them experiencing alienation or reactance. 

### Solution
The Information Coping Trajectory (ICT) Mapper classifies each client into one of 5 coping positions using LIWC-22 linguistic patterns. 
Crucially, it maps coping at **two levels**:
1. **Individual Level:** Dictates what commercial invitations and challenges a specific client can receive.
2. **Tribe Level:** Aggregates individual ICT scores into a unified tribe position, driving the entire weekly CCF content strategy (archetypes, emotional register, discovery/escape vs status routing).

### Scope
**In scope:**
- 5-position classification of individuals via the `ict-mapper` skill.
- Aggregation of tribe-level positions via the `tribe-ict-aggregator`.
- Storage logic for `information_coping_trajectory` and `tribe_ict_snapshot` Supabase tables.
- Integration with the Data Analyst Agent's Weekly Cycle to inform CCF planners (Capability Area 10).

**Out of scope:**
- The actual execution of the 5-tiered commercial routing (handled by FR-CBCS-12 Coping Diagnostic Invitation Engine).
- Publishing the actual CCF content (handled by FR14/FR18/FR17).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `information_coping_trajectory` | ICT Individual DB | Client 1-5 positions over time | FR-CBCS-04 | FR-CBCS-02, FR-CBCS-12 |
| `tribe_ict_snapshot` | Aggregate Tribe DB | Overall weekly tribe status | FR-CBCS-04 | CCF Planners, Data Analyst |
| `PROPOSED: DEP-ENG-058` | Tribe ICT Aggregate Payload | JIT parameter routing | FR-CBCS-04 | FR10/FR17 |

### Academic Grounding
- **Research Paper:** *Information Coping Trajectories* + *Health Communication Tailoring* (Kreuter & Strecher, 1996).
- **Mechanism:** Information must be tailored to the recipient's psychological capacity to receive it. Individuals map through:
  - Position 1: Deficiency (shock/avoidance)
  - Position 2: Ill-Informed (fear/denial/passive)
  - Position 3: Needs Injection (active seeking/selective)
  - Position 4: Information Health (confident/active engagement)
  - Position 5: Information Donor (mastery/altruistic)
  
### Technical Decisions
- **Execution Level:** Individual mapping runs weekly against the trailing 7 days of CBCS messages. Tribe mapping runs immediately after, aggregating the individual data.
- **Tribe Algorithm:** The `tribe_ict_snapshot` uses a weighted distribution calculation prioritizing critical masses to shift entire curriculum phases.

---

## 4. Implementation Plan

### Stage 1: Individual ICT Mapping
- **Agent:** `ict-mapper` (Python classification tool)
- **Inputs:** 
  - `liwc_scores_jsonb` (DEP-ID: `DEP-ENG-047` — Produced By: FR47 LIWC-22 Global Analyzer)
- **Outputs:** Database row insertion in `information_coping_trajectory`.
- **Failure Condition:** If the client has $0$ interactions in the trailing 7 days, the algorithm defaults to reading their previous table row. If $0$ interactions exist globally, it defaults to Position 2. Database write commits safely.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id`, `position`, and `classification_confidence` score written to APM tracker.
- **ADR-01 Isolation Constraint:** The queries driving the mapper must restrict data analysis `WHERE coach_id = auth.uid()`.

### Stage 2: Variable Resolution Rules for Individual Positions (1-5)
The scalar `position` integer evaluates sequentially (top-down, highest match takes priority) based strictly on these `liwc_scores_jsonb` input conditions:
- **5 (Information Donor):** Evaluates `True` IF `liwc_scores.social_words > 0.15` AND `liwc_scores.insight > 0.05` + client has sustained Position 4 for $>30$ days.
- **4 (Information Health):** Evaluates `True` IF `liwc_scores.cognitive_processes > 0.15` AND `liwc_scores.positive_emotion > 0.05` AND `liwc_scores.insight > 0.03`.
- **3 (Needs Injection):** Evaluates `True` IF `liwc_scores.information_seeking > 0.1` AND `liwc_scores.future_focus > 0.05`.
- **2 (Ill-Informed):** Evaluates `True` IF `liwc_scores.cognitive_processes < 0.1` AND `liwc_scores.anxiety > 0.02`.
- **1 (Deficiency):** Evaluates `True` IF `liwc_scores.cognitive_processes < 0.1` AND `liwc_scores.negative_emotion > 0.05` AND CBCS interaction frequency $< 1$ per week.
- **Fallback:** Defaults to 2 if no threshold met.

### Stage 3: Tribe Level Aggregation & Quality Gate
- **Agent:** `tribe-ict-aggregator`
- **Inputs:** `SELECT position FROM information_coping_trajectory WHERE active = true`
- **Outputs:** `tribe_ict_snapshot` Supabase row + `PROPOSED: DEP-ENG-058` (Tribe ICT Aggregate Payload).

**Quality Gate:** **Minimum Tribe Sample Gate**
- **Triggered when:** The weekly CCF Data Analyst attempts to compute the Tribe Snapshot.
- **Exact Threshold:** `COUNT(active_clients)` in the scope of `coach_id`.
  - **Verdict - PASS:** `COUNT >= 5`. *Downstream Consequence:* Aggregation algorithm executes normally and outputs weighted position distribution mathematically.
  - **Verdict - PROVISIONAL:** `COUNT >= 1 AND COUNT < 5`. *Downstream Consequence:* Statistical sample too low for distribution weighting. Outputs the median position integer directly instead of percentage bands to prevent 1 outlier skewing the 100% block.
  - **Verdict - FAIL:** `COUNT == 0`. *Downstream Consequence:* Evaluation aborted. Outputs standard fallback `aggregate_position = 2`.

### Stage 4: Resolution Rules for Output Schemas
**InformationCopingTrajectoryRow:**
- `ict_id`: Generated via `uuid.uuid4()`.
- `client_id` & `coach_id`: Passed synchronously.
- `position`: Evaluating the Stage 2 scalar logic.
- `position_label`: Switch/Case string mapping -> `{1: "Deficiency", 2: "Ill-Informed", 3: "Needs Injection", 4: "Information Health", 5: "Information Donor"}`.
- `liwc_markers_snapshot`: The raw `liwc_scores_jsonb` object saved for historical tracing.
- `classification_confidence`: Mathematical proxy: `(Number of boolean conditions met by LIWC markers for resulting position) / (Total boolean conditions required for stage) * 1.0`.
- `last_updated`: UTC `datetime.now().isoformat()`.

**TribeIctSnapshotRow:**
- `snapshot_id`: `uuid.uuid4()`.
- `aggregate_position`: Evaluates to whichever integer (1-5) accounts for the largest chunk of the `position_distribution` percentile. IF tie, evaluates to the lower number (conservative bias).
- `position_distribution`: Math evaluating `COUNT(position = X) / TOTAL_COUNT`. 
- `recommended_content_archetype`: 
  - IF `aggregate_position <= 2`: evaluates to String `"Validation/Defense"`.
  - IF `aggregate_position == 3`: evaluates to String `"Curiosity/Bridge"`.
  - IF `aggregate_position >= 4`: evaluates to String `"Expansion/Agency"`.

---

## 5. Primary Output Schema

```typescript
type InformationCopingTrajectoryRow = {
  ict_id: string; 
  client_id: string; 
  coach_id: string; // ADR-01 boundary
  position: 1 | 2 | 3 | 4 | 5; 
  position_label: string; 
  liwc_markers_snapshot: Record<string, number>; 
  classification_confidence: number; 
  last_updated: string; // ISO8601
};

type TribeIctSnapshotRow = {
  snapshot_id: string; 
  coach_id: string; 
  aggregate_position: 1 | 2 | 3 | 4 | 5;
  position_distribution: { p1: number, p2: number, p3: number, p4: number, p5: number }; 
  recommended_content_archetype: "Validation/Defense" | "Curiosity/Bridge" | "Expansion/Agency"; 
  computed_date: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For active `client_id`s with no `information_coping_trajectory` DB row available when FR-CBCS-12 attempts to route them:
- They dynamically inherit their `aggregate_position` from their Coach's master `tribe_ict_snapshot`.
- If their Coach has 0 active tracked clients, they inherit `2` globally, ensuring highly conservative behavior matching the established Fail Gate logic.

---

## 7. Tasks
- [ ] **Task 1: Position Algorithm** - Develop `ict_classifier.py` chaining the 5 explicit boolean sets linking LIWC dimensions to positions.
- [ ] **Task 2: Individual Storage Validation** - Deploy `information_coping_trajectory` PostgreSQL schemas and verify RLS boundaries block cross-coach extraction.
- [ ] **Task 3: Tribe Aggregator & Gate** - Develop `tribe-ict-aggregator` to compute percentage bins, executing the exact `Minimum Tribe Sample Gate` logic.
- [ ] **Task 4: Analyst Hook** - Code the Python handler injecting `recommended_content_archetype` from `TribeIctSnapshotRow` into the `parameter_update.json` output for FR10 planners.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Exacting Enum Mapping):** Passing `liwc_scores.cognitive_processes: 0.05` AND `liwc_scores.anxiety: 0.08` MUST evaluate cleanly to `position = 2` without rounding errors. **Failure Example:** The script falls through to position 3 due to missing boundary clamps, sending $9 challenges inappropriately.
- [ ] **AC2 (Tribe Aggregation Threshold Provisionality):** Executing `tribe-ict-aggregator` on an account mapping 3 active clients MUST trigger a `PROVISIONAL` verdict on the minimum sample gate, outputting median integers rather than triggering skewed 33.3% distributions that crash UI widgets. **Failure Example:** Evaluates to PASS blindly, generating massive standard deviation margins driving irrelevant content curation.
- [ ] **AC3 (Enum Field Resolution):** Evaluated `aggregate_position = 3` MUST translate exactly to the schema output `recommended_content_archetype: "Curiosity/Bridge"`. **Failure Example:** Null pointer due to mismatched typo between `"Curiosity/Bridge"` and the database enum limit.
