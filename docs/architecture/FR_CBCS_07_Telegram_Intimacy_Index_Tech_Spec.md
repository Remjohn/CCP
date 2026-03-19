# FR-CBCS-07: Telegram Intimacy Index — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F7, PRD §FR-CBCS-07

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Standard systems measure engagement (open rates, click-through rates), not intimacy. A client who passively consumes content may have high engagement but low intimacy. Sending a commercial invitation to a non-intimate client feels transactional, breaking trust.

### Solution
The Telegram Intimacy Index (TII) computes a parasocial bond strength score (0.0-1.0) for each client. By evaluating 6 specific interaction vectors (latency, depth, initiative, disclosure, voice usage, and consistency), it gates all CPSC campaigns. No campaign can target a client whose TII score falls below 0.4.

### Scope
**In scope:**
- Computation of the 6 behavioral signals via `telegram-intimacy-calculator`.
- The `psr-stage-classifier` mapping TII to Parasocial Stages (Entertainment-Social, Intense-Personal, Borderline).
- Storage and tracking in the `telegram_intimacy_index` Supabase table.
- Integration as the 4th condition into the `Delivery Permission Gate`.

**Out of scope:**
- Triggering the actual engagement events (the Telegram bot logs these passively).
- Social Penetration stage calculation (handled by FR-CBCS-02, read by TII).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `telegram_intimacy_index` | TII SQL Table | Stores client bond metrics | FR-CBCS-07 | FR-CBCS-02 |
| `PROPOSED: DEP-ENG-062` | TII Delivery Threshold Gate | Pass/fail check > 0.4 | FR-CBCS-07 | FR53 |

### Academic Grounding
- **Research Paper:** *Mass Communication and Para-Social Interaction* (Horton & Wohl, 1956) + *Parasocial Interaction: A Review of the Literature and a Model for Future Research* (Giles, 2002) + *Mobile Communication and Parasocial Relationships* (Baek et al., 2013).
- **Mechanism:** Mobile devices foster relationships closer to real friendships than traditional media. Parasocial Relationship (PSR) intensity dictates whether an outreach feels like a broadcast or a personal note.

### Technical Decisions
- **Periodic Update:** TII runs via a weekly cron job executed by the Data Analyst Agent (`tii_calculator.py`), smoothing out daily anomalies.
- **Component Weights:** The TII score uses a weighted algorithm prioritizing Disclosure Depth mapping directly from `DEP-ID: social_penetration_depth_gauge`.

---

## 4. Implementation Plan

### Stage 1: TII Calculation Pipeline
- **Agent:** `telegram-intimacy-calculator` (Python background tool)
- **Inputs:** 
  - `client_message_history` (DEP-ID: `DEP-ENG-045` — Produced By: FR45 Webhook Gateway)
  - `spt_stage` (DEP-ID: `social_penetration_depth_gauge` — Produced By: FR-CBCS-02)
- **Outputs:** Database row mapping to `telegram_intimacy_index`.
- **Failure Condition:** If `client_message_history` returns 0 rows, execution halts, writing `0.0` for all scores to safely degrade the index without throwing `ZeroDivisionError`.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `composite_tii` + `computed_date` written to the logging platform verifying the weekly evaluation block updated.
- **ADR-01 Isolation Constraint:** The SQL query calculating `initiative_frequency_score` and `voice_note_ratio_score` requires an active `WHERE coach_id = auth.uid()` clause to stop cross-pollination. 

### Stage 2: Quality Gate Extension
- **Agent:** `IntelligenceGateRouter` (extending FR-CBCS-02)
- **Quality Gate:** **The TII Delivery Threshold Gate**
- **Triggered when:** FR53 sequences or broadcast planners request list building access.
- **Exact Thresholds:** `composite_tii` decimal evaluated simultaneously with `consistency_score`.
  - **Verdict - PASS:** `composite_tii >= 0.4`. *Downstream Consequence:* Campaign executes natively.
  - **Verdict - PROVISIONAL:** `composite_tii >= 0.3 AND composite_tii < 0.4` AND `consistency_score > 0.8`. *Downstream Consequence:* Client is highly consistent but intimacy is stuck shallow. Campaign automatic launch pauses. Route alert to human operator queue: "Ready for manual Deep Disclosure / Voice Note connection rather than automated funnel block."
  - **Verdict - FAIL:** `composite_tii < 0.3`. *Downstream Consequence:* Client is alienated. Completely blocked from commercial funnels. System falls back strictly to relationship-building sequences via FR-CBCS-10.

### Stage 3: Variable Resolution Rules (Exact Input Conditions)
The ENUM values for `psr_stage` are translated directly from the calculated `composite_tii` block via specific clamping logic:
- **"Entertainment-Social"**: Evaluates `True` IF `composite_tii < 0.4`. (Client views the relationship as mass media consumption).
- **"Intense-Personal"**: Evaluates `True` IF `composite_tii >= 0.4` AND `composite_tii < 0.8`. (Client feels a dedicated one-on-one bond).
- **"Borderline"**: Evaluates `True` IF `composite_tii >= 0.8`. (Warning sign for dependency / over-attachment requiring clinical boundary-holding by the coach).

### Stage 4: Resolution Rules for Output Schema
Every schema field maps to explicit integer/float metrics calculated strictly via these equations:
- `tii_id`: `uuid.uuid4()`.
- `interaction_frequency_score`: `(Message_Count / 30) / Max_Expected_Frequency (3)`. Clamped at `1.0`.
- `consistency_score`: `(Days_Active_In_Last_30 / 30)`. Clamped at `1.0`.
- `disclosure_depth_score`: Mapped directly: `spt_stage / 4.0`.
- `response_latency_score`: `(24_hours - Math.min(24_hours, Avg_Response_Time)) / 24_hours`.
- `voice_note_ratio_score`: `(Voice_Message_Count / Total_Client_Messages) * 2.0`. Clamped at `1.0`.
- `initiative_frequency_score`: `(Days_Client_Initiated / Days_Active_In_Last_30)`.
- `composite_tii`: Standard weighted average: `(0.1*freq + 0.15*consist + 0.3*disclosure + 0.1*latency + 0.1*voice + 0.25*init)`.
- `psr_stage`: Result of the Stage 3 ENUM assignment block linking to `composite_tii`.
- `last_computed`: `datetime.now().isoformat()`.

---

## 5. Primary Output Schema

```typescript
type TelegramIntimacyIndexRow = {
  tii_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  interaction_frequency_score: number; // Float 0.0-1.0
  consistency_score: number; // Float 0.0-1.0
  disclosure_depth_score: number; // Float 0.0-1.0
  response_latency_score: number; // Float 0.0-1.0
  voice_note_ratio_score: number; // Float 0.0-1.0
  initiative_frequency_score: number; // Float 0.0-1.0
  composite_tii: number; // Float 0.0 - 1.0
  psr_stage: "Entertainment-Social" | "Intense-Personal" | "Borderline"; // Explicit enum map
  last_computed: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For active clients currently in a standard CRM lifecycle tag with missing legacy Telegram database log mappings:
- Because the math clamps correctly, 0 interactions resolves cleanly to `0.0`. 
- `0.0` automatically triggers `FAIL` routing for the CPSC Campaigns via `composite_tii < 0.3`. 
- Client defaults to the FR10/FR11 Relationship pipeline, aggressively building the necessary intimacy metrics before any future sales blasts hit their phone.

---

## 7. Tasks
- [ ] **Task 1: Calculator Math** - Develop `tii_calculator.py` isolating the 6 metric functions to invert latencies correctly and gracefully handle Python `ZeroDivisionError` on clients with no voice notes or missing histories.
- [ ] **Task 2: Stage 3 Enum Triggers** - Tie the database insert sequence linearly to the 3-State Enum string resolution mapping logic.
- [ ] **Task 3: Slash Commands** - Create `/cbcs-intel tii [client_id]` returning a formatted string print of the 6 core metrics defining the composite score.
- [ ] **Task 4: Gate Integration** - Reconfigure the `delivery_permission_gates` module (FR-CBCS-02) adding `PROVISIONAL` logic explicitly requiring human queue intervention if the score lies between `0.3` and `0.4`.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard TII Gate):** A client evaluating `composite_tii = 0.29` triggers the CPSC batch script. Execution MUST return a pure `FAIL` condition, blocking the message payload locally on the server. **Failure Example:** The system incorrectly rounds `0.29` UP to `0.3` evaluating to `PROVISIONAL`, triggering a human review queue for an account that is fully disengaged.
- [ ] **AC2 (Composite Ratio Math Check):** Passing `Days_Active_In_Last_30 = 0` MUST cleanly assign `composite_tii = 0.0` bypassing arithmetic division crashes. **Failure Example:** Python throws `ZeroDivisionError: division by zero` in `initiative_frequency_score` math, bringing down the entire weekly cron job container.
- [ ] **AC3 (Enum Resolution):** Evaluated `composite_tii = 0.82` MUST insert into PostgreSQL `psr_stage = 'Borderline'`. **Failure Example:** Logic maps exclusively up to `0.80` forcing a default fallback setting it artificially low, masking dangerous boundary conditions from the operator dashboards.
