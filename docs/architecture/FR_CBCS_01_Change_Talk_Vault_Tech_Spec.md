# FR-CBCS-01: Change Talk Vault — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F1, PRD §FR-CBCS-01

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CCP update/Context about CCP updates.md`

---

## 2. Overview

### Problem Statement
Standard CRMs send re-engagement messages that begin with the company's message. This forces the client into a defensive or evaluation posture, where they must decide whether they agree with the external entity's argument.

### Solution
The Change Talk Vault is an autonomous commitment reactivation engine. It detects, tags, and archives commitment-language from client CBCS interactions using the DARN-CAT framework. When the Campaign Orchestration Agent prepares a conversion sequence, it queries the Vault to mirror the client's own highest-intensity commitment statements back to them, placing the commitment in a memory reconsolidation labile state.

### Scope
**In scope:**
- Real-time scanning of client CBCS interactions for DARN-CAT dimensions
- Tagging and storing statements in the `change_talk_archive` Supabase table
- Execution of the `change-talk-tagger` Skill
- Providing queried data to downstream Campaign Orchestration (Capability Area 9)

**Out of scope:**
- Actual generation of the conversion sequence copy (handled by FR53)
- Emotional tracking independent of commitment (handled by FR4)

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `change_talk_archive` | Change Talk Supabase Table | Stores extracted DARN-CAT commitment phrases | FR-CBCS-01 | FR53, FR54, FR-CBCS-05 |
| `PROPOSED: DEP-ENG-054` | DARN-CAT Tagger Payload | Intermediate scoring output | FR-CBCS-01 | `change_talk_archive` |

### Academic Grounding
- **Research Paper:** *Motivational Interviewing: Helping People Change* (Miller & Rollnick, 2012) + *Client Commitment Language During Motivational Interviewing Predicts Drug Use Outcomes* (Amrhein et al., 2003)
- **Mechanism:** Client-generated commitment language is a stronger predictor of behavioral follow-through than external arguments. Mirroring commitment statements forces self-consistency evaluation.

### Technical Decisions
- **Storage:** Stored in Supabase (`change_talk_archive`) rather than a JSON blob, allowing querying by highest emotional intensity, specific DARN-CAT dimension, and date.
- **Continuous Tagging:** The `change-talk-tagger` runs continuously on new CBCS messages (as part of the background worker sequence triggered by `liwc22_cbcs_analyzer.py`).

---

## 4. Implementation Plan

### Stage 1: Change Talk Scanning and Tagging
- **Agent:** `change-talk-tagger` (Python NLP Tool/Skill fine-tuned on MI corpus)
- **Inputs:** 
  - `raw_client_message_text` (DEP-ID: `DEP-ENG-045` — Produced By: FR45 Webhook Gateway)
  - `client_id` (DEP-ID: `DEP-ENG-045` — Produced By: FR45 Webhook Gateway)
  - `current_coping_position` (DEP-ID: `information_coping_trajectory` — Produced By: FR-CBCS-04)
  - `emotional_mode` (DEP-ID: `DEP-ENG-018` — Produced By: FR18 CRAL)
- **Outputs:** `PROPOSED: DEP-ENG-054` (DARN-CAT Tagger Payload)
- **Failure Condition:** If the tagger encounters an unsupported language or a completely empty text payload (`length == 0`), extraction is bypassed. Error logged locally; process exits safely without writing to DB.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + processing timestamp written to system audit log at the conclusion of Stage 1, regardless of DARN-CAT match success.

### Stage 2: Archive Storage
- **Agent:** SQL Coder Agent / Database Worker
- **Inputs:** `PROPOSED: DEP-ENG-054`
- **Outputs:** Database row insertion in `change_talk_archive`
- **Failure Condition:** Database timeout or duplicate primary key collision. Aborts transaction, logs `DB_WRITE_ERROR` to APM layer, prevents duplicate entries.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `statement_text` + `darn_cat_dimension` written to system audit log upon successful DB insert.
- **ADR-01 Isolation Constraint:** The `change_talk_archive` RLS policy MUST execute `WHERE coach_id = auth.uid()` to ensure no cross-coach leakage of highly sensitive therapeutic commitments.

### Stage 3: Variable Resolution Rules (Exact Input Conditions)
The following rules determine exactly how the ENUM values for `darn_cat_dimension` are computed during Stage 1:

- **"Desire"**: Evaluates `True` IF `raw_client_message_text` contains regex match for `(want|wish|desire|hope to)` AND dependency parser links it to a targeted behavioral change.
- **"Ability"**: Evaluates `True` IF text contains `(can|able to|possible to|could)`.
- **"Reasons"**: Evaluates `True` IF text contains `(because|since|so that)` immediately preceding a positive outcome statement.
- **"Need"**: Evaluates `True` IF text contains `(must|have to|need to|got to)`.
- **"Commitment"**: Evaluates `True` IF text contains `(will|promise|swear|guarantee|definitely going to)`.
- **"Activation"**: Evaluates `True` IF text contains `(ready|prepared|starting tomorrow|willing)`.
- **"Taking_Steps"**: Evaluates `True` IF text contains `(started|did|completed|just finished)` + a past-tense action verb.

### Stage 4: Resolution Rules for Output Schema
Every field in the `ChangeTalkArchiveRow` is populated via the following exact logic:
- `entry_id`: Generated dynamically via `uuid.uuid4()` at time of DB insert.
- `client_id`: Passed directly from `client_id` input payload.
- `coach_id`: Retrieved synchronously via database lookup mapping `client_id` to its parent `coach_id`.
- `statement_text`: Regex substring extraction of the specific sentence containing the matched DARN-CAT trigger phrase, truncated at the first terminal punctuation mark (`.`, `!`, `?`).
- `darn_cat_dimension`: Assigned directly from the result of the Variable Resolution Rule (Stage 3). 
- `liwc_intensity_score`: The raw percentage frequency of matched dictionary words divided by total word count of the `statement_text`, multiplied by 100.
- `coping_stage_at_time`: Passed directly from the `current_coping_position` input variable.
- `emotional_mode`: Passed directly from the `emotional_mode` input variable.
- `timestamp`: Populated via Python `datetime.now(timezone.utc).isoformat()` at the exact moment of extraction.

### Stage 5: Quality Gate & Retrieval
- **Quality Gate:** **Minimum Vault Threshold Gate**
- **Triggered when:** Campaign Orchestrator queries Vault to fetch commitment statements.
- **Exact Threshold:** `SELECT COUNT(*) FROM change_talk_archive WHERE client_id = target_id AND darn_cat_dimension IN ('Commitment', 'Taking_Steps')`
  - **Verdict - PASS:** `Count >= 3`. *Downstream Consequence:* The single highest `liwc_intensity_score` statement is attached to the prompt execution context for FR53.
  - **Verdict - PROVISIONAL:** `Count == 1 OR Count == 2`. *Downstream Consequence:* Statement is passed, but the `confidence_flag` is set to `PROVISIONAL`. FR53 is instructed to wrap the quote in soft framing ("You mentioned earlier...") rather than aggressive anchoring ("You promised yourself...").
  - **Verdict - FAIL:** `Count == 0`. *Downstream Consequence:* Query returns strict null payload. FR53 is instructed to use purely systemic Identity Priming without pulling direct client quotes. 

---

## 5. Primary Output Schema (change_talk_archive)

```typescript
type ChangeTalkArchiveRow = {
  entry_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  statement_text: string; // Substring extraction
  darn_cat_dimension: "Desire" | "Ability" | "Reasons" | "Need" | "Commitment" | "Activation" | "Taking_Steps"; 
  liwc_intensity_score: number; // Float 0.0-100.0
  coping_stage_at_time: number; // Int 1-5
  emotional_mode: "Escape" | "Processing" | "Discovery" | "Status" | "Tension" | "Vulnerability" | "Recognition"; 
  timestamp: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For clients deployed prior to V3.0 with zero entries in the `change_talk_archive`:
- The system will NOT run historical processing scripts over dormant journals to backfill data.
- During any Campaign sequence, these clients will hit the `Minimum Vault Threshold Gate`, returning a `Count == 0`, immediately failing the gate and engaging the safe-degradation fallback (Identity Priming without direct mirroring).

---

## 7. Tasks
- [ ] **Task 1: AI NLP Skill Implementation** - Code the Python NLP regex & dependency-parsing blocks to map the 7 precise ENUM outcomes based on trigger words.
- [ ] **Task 2: Database Architecture** - Create the `change_talk_archive` Supabase table and apply strictly enforced RLS policies mapped to `coach_id`.
- [ ] **Task 3: Pipeline Integration** - Scaffold the inputs, handling the `UPSTREAM UNDEFINED` webhook variables alongside the `DEP-ENG-058` integration.
- [ ] **Task 4: Gate Implementation** - Write the `COUNT(*)` integer evaluation function that routes to PASS, PROVISIONAL, and FAIL verdicts.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Extraction Accuracy & Enum Resolution):** System ingests: "I must do this because I was promised a raise." Evaluates to: `darn_cat_dimension = 'Need'` based on the presence of "must". **Failure Example:** The system parses "promised" and generates a `Commitment` tag, skipping the leading necessity modifier.
- [ ] **AC2 (Provisional Gating):** Querying a `client_id` with exactly 2 entries in the DB MUST return a `PROVISIONAL` verdict to FR53, shifting prompt tone. **Failure Example:** System rounds up and treats 2 entries as a `PASS`, generating aggressive "You promised!" copywriting entirely disconnected from a robust trendline.
- [ ] **AC3 (ADR-01 Violation Block):** Explicit SQL query against `change_talk_archive` using an auth token matching `Coach A` attempting to read `Client B` (assigned to `Coach B`) MUST return 0 rows. **Failure Example:** Database returns sensitive commitment phrases due to missing RLS configuration.
