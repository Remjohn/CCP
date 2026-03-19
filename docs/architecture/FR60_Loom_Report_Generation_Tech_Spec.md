# FR60: Loom Report Generation — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_Sales_Cycle_Documentation_V1 §FR60, CCP_Architecture_Documentation_V2 §FR60

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_Sales_Cycle_Documentation_V1.docx.md`
- `lab/CCP update/CCP_Architecture_Documentation_V2.docx.md`

---

## 2. Overview

### Problem Statement
Standard software platforms present users with dashboards full of charts (conversion rate: 4%). Coaches are not data scientists; they ignore the dashboards, rendering the entire FR56 precision logging architecture useless. If the machine cannot translate its deep psychological metrics into actionable intelligence natively, it is an over-engineered failure.

### Solution
The Loom Report Generation module acts as the data translator. When a Campaign Cycle concludes, it ingests the `campaign_performance_registry` blocks. Rather than plotting dots, it uses the LLM to write a coach-facing Narrative Document delivered to Notion. It explains *why* the campaign succeeded based explicitly on Coping Positions and Change Talk data logged, formulating actionable recommendations.

### Scope
**In scope:**
- The `loom-intelligence-translator` synthesizing DB numeric arrays.
- Narrative Section Enums tracking Report construction.
- The `Actionable Threshold Gate` ensuring recommendations aren't hallucinated.

**Out of scope:**
- Recording an actual video (`Loom Report` is a structural metaphor for a detailed narrative brief mimicking the depth of a video update, not `.mp4` generation).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-080` | Loom Intelligence Narrative | Formatted Notion Markdown | FR60 | Operator/Coach Notion |

### Academic Grounding
- **Mechanism:** Information Design (Tufte). Humans process narratives orders of magnitude more effectively than statistical arrays. By transforming `Tier 3 Conversion = 12%` into: "Clients currently in the Selective Engagement phase responded incredibly well to the identity anchor," data becomes operable.

### Key Files
- `performance_calculator.py`
- `loom_translator.py`

### Technical Decisions
- **Anti-Hallucination Regex Formatting:** The system is explicitly blocked from giving "general marketing advice." Every single bullet point must trace mathematically to a defined matrix shift in the Supabase performance arrays.
- **ADR-01 Isolation:** The aggregate conversion models compile logic locally per tenant execution UUID.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Narrative Synthesis)
- **Agent:** `loom-intelligence-translator`
- **Inputs:** 
  - `campaign_performance_registry` (DEP-ID: `DEP-ENG-051` — Produced By: FR56)
  - `campaign_id` parameter arrays.
- **Outputs:**
  - Logic maps driving the final string generation loop sections.
- **Failure Condition:** Missing Campaign IDs evaluates null loops bypassing generation entirely.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `campaign_execution_id` + `coach_id` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Recommendation Logic):** The script parses the `conversion_outcome` counts grouped mathematically by `coping_tier_at_launch`. The pipeline constructs boolean evaluations routing string blocks:
- **`conversion_spike_detected`**: IF `Group_A_Conversion` > `Baseline_Conversion` * 1.5. *LLM Instruction parsed context:* "Focus narrative explaining why Group A reacted so positively." Outputs strings to `psychological_signal_block`.
- **`conversion_crash_detected`**: IF `Group_B_Conversion` < `Baseline_Conversion` / 2.0. *LLM Instruction parsed context:* "Highlight misalignment warning. State commitment price was overwhelming for Coping Tier B." Outputs strings to `actionable_recommendation_block`.

### Stage 2: Quality Gate Extension
- **Agent:** `loom-intelligence-translator`
- **Inputs:** Generated output string blocks `summary_block`, `signal_block`, `recommendation_block`.
- **Outputs:** `LoomNarrativeReportRow` (DEP-ENG-080).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `report_id` logged. **(Mandatory Execution)**.
- **Failure Condition:** Regex rule violation tracking blocks generation outputs.

**Quality Gate:** **The Actionable Threshold Gate**
- **Triggered when:** Node drafts 5-point markdown block preparing Notion API JSON parameter bindings.
- **Exact Thresholds:** Evaluates `actionable_recommendation_block` string against mathematical numeric bounds identified and Python Regex blacklists.
- **Verdict - PASS:** Recommendation string explicitly cites exact numbers calculated in Stage 1 arrays. Regex passes. *Downstream Consequence:* Document synced via webhook to Notion integration securely. `gate_verdict = PASS`.
- **Verdict - PROVISIONAL:** Text contains no hard numerical array bounds, adopting vague phrasing ("Some clients did well"). *Downstream Consequence:* Generation pauses. Pushes context to Review Queue: `"Warning: LLM returning empty rhetorical summary. Data lacked statistical significance. Transmit generic?"` Sets `gate_verdict = PROVISIONAL_VAGUE_SUMMARY`.
- **Verdict - FAIL:** The LLM hallucinates instructing random external software action mapping (e.g. "Run Facebook ads"). Regex detects phrases. *Downstream Consequence:* Execute `Hard Reject` block if text contains blacklisted platform terminology outside CCP boundaries. Triggers LLM rewrite. Sets `gate_verdict = FAIL_HALLUCINATED_ADVICE`.

### Phase 3: Field-by-Field Schema Mapping
Every schema field specifies exact evaluation origin:
- `report_id`: Returns `uuid.uuid4()`.
- `campaign_execution_id`: Returns string ID mapped exactly tracking the orchestrator log.
- `coach_id`: Returns `auth.uid()` request context reinforcing ADR-01 bound.
- `gate_verdict`: Returns String mapped by Stage 2 ("PASS" | "PROVISIONAL_VAGUE_SUMMARY" | "FAIL_HALLUCINATED_ADVICE").
- `loom_sections.summary_block`: Returns String parsed directly containing numerical outcome counts limits.
- `loom_sections.psychological_signal_block`: Returns String mapping Change Talk impact factors generated in Stage 1.
- `loom_sections.actionable_recommendation_block`: Returns the String output checked mathematically by Stage 2.
- `computation_timestamp`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LoomNarrativeReportRow (DEP-ENG-080)",
  "type": "object",
  "properties": {
    "report_id": { "type": "string", "format": "uuid" },
    "campaign_execution_id": { "type": "string", "format": "uuid" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "gate_verdict": { "type": "string", "enum": ["PASS", "PROVISIONAL_VAGUE_SUMMARY", "FAIL_HALLUCINATED_ADVICE"] },
    "loom_sections": {
      "type": "object",
      "properties": {
        "summary_block": { "type": "string" },
        "psychological_signal_block": { "type": "string" },
        "actionable_recommendation_block": { "type": "string" }
      }
    },
    "computation_timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "report_id", "campaign_execution_id", "coach_id", "gate_verdict",
    "loom_sections", "computation_timestamp"
  ]
}
```

---

## 6. Backward Compatibility Fallback
For FR59 cycles run with `PROVISIONAL_LEGACY_MODE` executing missing CBCS DB intelligence variables:
System correctly evaluates boolean loop paths triggering `PROVISIONAL_VAGUE_SUMMARY` gate path exclusively. Output strings acknowledge inability to provide deep emotional guidance, reverting entirely to rendering simplistic numerical boundaries arrays inside standard Markdown objects (acting as a basic funnel report).

---

## 7. Tasks
- [ ] Task 1: Complete `performance_calculator.py` scanning 14-day trailing Postgres DB rows writing the calculation blocks isolating Baseline Baseline, Spike, and Crash limits parameters.
- [ ] Task 2: Build `re_blocklist.search()` logic regex string evaluation list tracking explicitly banned generic marketing words ("Facebook ads", "Clickfunnels") mapping directly to `FAIL_HALLUCINATED_ADVICE`.
- [ ] Task 3: Develop Notion sync node mapping JSON arrays directly parsing the `loom_sections` layout dictionary definitions explicitly mirroring visually clean design modules.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Hallucination Rejection):** Final LLM returns `"Try running TikTok ad campaigns."` Pattern `re.search` evaluates. Gate MUST map Enum `FAIL_HALLUCINATED_ADVICE`. **Failure Example:** The LLM violates scientific methodology, advising algorithmic noise over tribal relationship-building logic loops.
- [ ] **AC2 (Provisional Vague Trimming):** Database math checks return flatlines entirely (no spike boundaries crossed). Gate MUST compile resolving `PROVISIONAL_VAGUE_SUMMARY`. **Failure Example:** LLM parses math noise hallucinating false causal connections misdirecting the operator's strategy entirely.
- [ ] **AC3 (Enum Field Construction):** A completely evaluated compilation script MUST process writing exactly 3 valid strings inside the array map, structurally preserving `psychological_signal_block`. **Failure Example:** Generator builds flat summary omitting key intel, making platform indistinguishable from raw MailChimp APIs.

---

## 9. Dependencies
- **Upstream:**
  - `FR56`: Campaign Performance Registry Arrays (`DEP-ENG-051`).
  - `FR59`: Campaign Execution parameters loop.
- **Downstream:**
  - `FR45`: Notion Sync Hook processes `DEP-ENG-080` payload matrices.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Conversion_Math_Ratio_Detection`: Inject Data Dictionary dictating Baseline `1.0` and Coping 4 Group representing logic integer `3.5`. Assert calculation pipeline assigns Boolean variable `True` identifying `"conversion_spike_detected"`.
- `Test_Regex_Dictionary_Sanitization`: Push mock string payload testing string variables `"You really need more Instagram traffic"`. Execute `Gateway()` eval loops. Assert array checks map string directly mapping to `FAIL_HALLUCINATED_ADVICE`.

### Integration Tests
- `Test_Notion_API_Formatting_Integrity`: Push synthetic UUID mock representing Stage 2 Pass loop boundaries explicitly. Assert `notion_sync.py` extracts `.summary_block` mapping cleanly executing standard Notion format block without encoding syntax format errors.

### Safety / Isolation Tests
- `Test_Isolated_Tenant_Calculations`: Provide Execution Node referencing Campaign `X` mapping to `coach_id=123`. Ensure executing `db.query()` logic returns numerical values excluding entirely records containing mapping `coach_id=456`. Assert Receipt API stores cryptographic validation block ensuring data separation at computation evaluation timing.
