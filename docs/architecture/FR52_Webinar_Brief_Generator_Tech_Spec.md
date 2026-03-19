# FR52: Webinar Brief Generator — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_Sales_Cycle_Documentation_V1 §FR52

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_Sales_Cycle_Documentation_V1.docx.md`
- `lab/CVE + CPSC research papers/Behavioral Science Fuels Challenge Funnel.md`

---

## 2. Overview

### Problem Statement
Standard webinar scripts utilize uniform persuasive pressure throughout a 60-minute presentation. Clients attending the webinar are spread across completely different psychological readiness boundaries. Applying heavy conversion logic in the first 15 minutes triggers psychological reactance to a Position 2 client, while failing to apply it at minute 50 bores a Position 5 client into abandonment. 

### Solution
The Webinar Brief Generator (FR52) cross-references the CBCS client intelligence pool to construct segmented Presentation Briefs. Instead of generating a generic script, it maps specific webinar modules (Intro, Content, Close) explicitly to Information Coping Trajectories. It actively queries the Coach's Change Talk Vault to extract the most statistically frequent commitment phrases actually used by their audience, injecting these verbatim into the generated brief to enforce deep identity resonance.

### Scope
**In scope:**
- The `webinar-brief-architect` extracting raw text arrays.
- Enum logic segmenting the triad of webinar modules.
- The `Structural Coping Alignment Gate` validating phrase injections.

**Out of scope:**
- Rendering the final `.excalidraw` webinar deck (handled by the down-stream FR33-FR34 V²WS pipeline processing this brief).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-073` | Webinar Conversion Brief | Seed JSON for V2WS | FR52 | FR33 |

### Academic Grounding
- **Research Paper:** *Readiness to Change and Information Processing* (Prochaska & DiClemente, 1983) + *Elaboration Likelihood Model* (Petty & Cacioppo, 1986).
- **Mechanism:** To transition a user from Peripheral processing (skeptical observation) to Central processing (active commitment), the argument must mirror their pre-existing internal narratives. Using their exact phrasing bypasses cognitive counter-arguing walls perfectly.

### Key Files
- `webinar_brief_builder.py` (Core architect logic executing mappings)
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **Verbatim Injection Rule:** The LLM is strictly prohibited from paraphrasing the Change Talk array findings. It must perform a literal string injection of the database text. Paraphrasing dilutes the psychological anchor.
- **ADR-01 Isolation:** Webinar briefs are generated containing highly sensitive coach-specific Change Talk metrics, isolated via Supabase RLS mapping to the active JWT.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Segment Targeting & Extraction)
- **Agent:** `webinar-brief-architect`
- **Inputs:** 
  - `change_talk_archive` (DEP-ID: `change_talk_vault` — Produced By: FR-CBCS-01)
  - `tribe_ict_aggregate` (DEP-ID: `PROPOSED: DEP-ENG-058` — Produced By: FR-CBCS-04)
- **Outputs:**
  - `intro_instruction_string` and `close_instruction_string` parameters.
- **Failure Condition:** If `change_talk_archive` returns `0` records, script routes to Fallback logic, skipping the substring evaluation.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `coach_id` + `dominant_coping_target` + `len(change_talk_records_fetched)` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Module Segmentation):** The JSON brief dynamically resolves configuration strings based on the mathematical Mode of `tribe_ict_aggregate`:
- **`intro_instruction` Mapping**: IF `Mode <= 3` (Ill-Informed $\rightarrow$ Selective), injects: `"Instruct V2WS: Spend 15% of slide count validating the pain state. Do not mention solutions."` (Focusing on validation for skeptical viewers).
- **`close_instruction` Mapping**: IF `Mode >= 4` (Active $\rightarrow$ Mastery), injects: `"Instruct V2WS: Spend 35% of slide count on offer parameters. Inject exact Change Talk phrases here."` (Focusing on heavy conversion pressure).

### Stage 2: Quality Gate Extension
- **Agent:** `webinar-brief-architect`
- **Inputs:** Raw drafted JSON containing `change_module_quotes` array, original `change_talk_archive` DB strings.
- **Outputs:** Final `webinar_conversion_brief` JSON (`DEP-ENG-073`).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `webinar_brief_id` string logged. **(Mandatory Execution)**.
- **Failure Condition:** 0 exact matches found blocks the pipeline.

**Quality Gate:** **The Structural Coping Alignment Gate**
- **Triggered when:** The architect node completes formulation of the JSON but before returning the payload to FR33 ingestion.
- **Exact Thresholds:** Evaluates the generated string array `change_talk_injected_quotes` against the original DB query array using a Python boolean exact substring match (`isSubstring()`).
- **Verdict - PASS:** At least 2 sentences stored in the output array are identical character-for-character substrings found in the primary DB query. *Downstream Consequence:* Brief clears validation, `gate_verdict=PASS`, dispatches to FR33.
- **Verdict - PROVISIONAL:** Only 1 sentence matches exactly, OR 2 sentences match with Levenshtein distance $< 3$. *Downstream Consequence:* System populates `gate_verdict=PROVISIONAL_PARAPHRASED`. Sends payload to Human Review Queue tagged: `"Warning: LLM actively paraphrasing client language."`
- **Verdict - FAIL:** 0 sentences match EXACTLY (Levenshtein distance >= 3). *Downstream Consequence:* Generation hard block. Triggers internal `rewind_generation()` to the LLM sending error message, `gate_verdict=FAIL_HALLUCINATED`.

### Phase 3: Field-by-Field Schema Mapping
Every field in the JSON maps explicitly:
- `webinar_brief_id`: Returns `uuid.uuid4()`.
- `coach_id`: Returns `auth.uid()`, enforcing ADR-01.
- `dominant_coping_target`: Returns the Integer (1-5) derived mathematically by calculating Mode from `tribe_ict_aggregate` in Stage 1.
- `change_talk_injected_quotes`: Returns Array of Strings containing the substrings validated by the Stage 2 PASS gate.
- `gate_verdict`: Returns String mapped explicitly by Stage 2 ("PASS" | "PROVISIONAL_PARAPHRASED" | "FAIL_HALLUCINATED").
- `intro_instruction_string`: Returns the String compiled by Stage 1 mapping logic.
- `close_instruction_string`: Returns the String compiled by Stage 1 mapping logic.
- `computation_timestamp`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WebinarConversionBrief (DEP-ENG-073)",
  "type": "object",
  "properties": {
    "webinar_brief_id": { "type": "string", "format": "uuid" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "dominant_coping_target": { "type": "integer", "enum": [1, 2, 3, 4, 5] },
    "change_talk_injected_quotes": { 
      "type": "array", 
      "items": { "type": "string" } 
    },
    "gate_verdict": { "type": "string", "enum": ["PASS", "PROVISIONAL_PARAPHRASED", "FAIL_HALLUCINATED"] },
    "intro_instruction_string": { "type": "string" },
    "close_instruction_string": { "type": "string" },
    "computation_timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "webinar_brief_id", "coach_id", "dominant_coping_target", "change_talk_injected_quotes",
    "gate_verdict", "intro_instruction_string", "close_instruction_string", "computation_timestamp"
  ]
}
```

---

## 6. Backward Compatibility Fallback
For legacy generic Webinar Briefs executing inside CCF instances prior to the `change_talk_archive` reaching sufficient volume (>5 items, where Stage 1 DB fetch returns 0):
- The `webinar-brief-architect` suppresses the Change Talk query.
- The `Structural Coping Alignment Gate` auto-bypasses the substring matching module. 
- It evaluates to `PASS_FALLBACK`, forcing the LLM to use the `Category 4 Enemy Nouns` (FR0C) as primary agitation mechanism until genuine user data accumulates, ensuring system stability.

---

## 7. Tasks
- [ ] Task 1: Execute a mathematically sorted Supabase `SELECT` in `webinar_brief_builder.py` returning the `TOP 3` highest `liwc_intensity_score` rows from the Change Talk table.
- [ ] Task 2: Code the Python validation loop checking `string_a in string_b` executing against the LLM's drafted JSON payload for the `FAIL/PASS` logic.
- [ ] Task 3: Map the output schema to the FR33 (Alessandro) webhook ingestion node to replace manual prompt typing.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Substring Validation):** Top DB string reads "I am tired of waiting." LLM outputs `"The user is exhausted."` Substring match == `False`. Gate MUST evaluate `FAIL_HALLUCINATED` triggering rewrite loop. **Failure Example:** System allows LLM to dilute the visceral emotional vocabulary of the tribe, reducing conversion.
- [ ] **AC2 (Provisional Paraphrase Alert):** DB string reads "I can't take this anymore." LLM outputs `"I cannot take this anymore."` (Levenshtein distance = 2). Gate MUST evaluate `PROVISIONAL_PARAPHRASED`. **Failure Example:** The LLM's grammar correction alters raw syntax, breaking the authentic voice reflection pattern.
- [ ] **AC3 (Enum Segmentation Rule):** A tribe mapped `dominant_coping_target = 4`. The resulting `intro_instruction_string` MUST strictly allocate lower percentage constraint. **Failure Example:** System allocates 70% of the webinar to validating pain for an audience that is in active solution-seeking mode, boring them to leave.

---

## 9. Dependencies
- **Upstream:**
  - `FR-CBCS-01`: Produces Change Talk Vault (`change_talk_vault`).
  - `FR-CBCS-04`: Produces Tribe ICT Aggregate (`PROPOSED: DEP-ENG-058`).
- **Downstream:**
  - `FR33`: Consumes output (`PROPOSED: DEP-ENG-073`) to feed V2WS pipeline.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)` API.
  - `Supabase` (ADR-01 RLS enforced).

---

## 10. Testing Strategy

### Unit Tests
- `Test_Substring_Gate_Evaluator`: Inject Synthetic DB Array `["Phrase A", "Phrase B"]`. Inject LLM Mock `["Phrase A", "Phrase C"]`. Assert Gate Enum returns `PROVISIONAL_PARAPHRASED` (since logic is >=2 matches for PASS).
- `Test_ICT_Module_Segmentation`: Inject `Mode = 5`. Assert `close_instruction_string` evaluates to the 35% concentration logic path correctly.

### Integration Tests
- `Test_Change_Talk_DB_Fetch`: Execute node requesting Top 3 quotes for `coach_id="mock"`. Assert Supabase returns correct rows sorted by `liwc_intensity_score` DESC. Assert Receipt Chain logs the length hash correctly.

### Safety / Isolation Tests
- `Test_Paraphrase_Prevention_Loop`: Force mock LLM to repeatedly return hallucinated syntax. Assert system triggers `rewind_generation()` exactly 3 times before entering a hard-fail state and alerting operator, avoiding infinite execution loops.
