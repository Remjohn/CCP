# FR51: Challenge Funnel Intelligence Builder — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_Sales_Cycle_Documentation_V1, CCP_Architecture_Documentation_V2 §FR51

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_Sales_Cycle_Documentation_V1.docx.md`
- `lab/CCP update/CCP_Architecture_Documentation_V2.docx.md`
- `lab/CVE + CPSC research papers/Behavioral Science Fuels Challenge Funnel.md`

---

## 2. Overview

### Problem Statement
Standard digital marketing funnels rely on demographic assumptions and generic "pain/agitate/solve" templates. Pitching a generic "transformation" to a client operating in Coping Position 3 (Selective Engagement) causes them to abandon the funnel entirely. Furthermore, high-friction, purely educational funnels fail because they assume continuous motivation rather than structural commitment.

### Solution
The Challenge Funnel Intelligence Builder (FR51) transforms the concept of a "lead magnet" into a psychologically targeted, 5-to-7 day micro-commitment gateway. It explicitly queries the Tribe's dominant Information Coping Trajectory (ICT), extracting their exact resistance language. It enforces "Implementation Intentions" through the challenge's daily structure, using a carefully calculated $9 entry fee to filter passive scrollers and trigger psychological consistency.

### Scope
**In scope:**
- The `challenge-funnel-architect` agent compiling psychological inputs into a structured brief.
- Enum resolution mapping Coping Positions to exact Challenge Step configurations.
- The `Commitment Device Validation Gate` enforcing the $9 threshold rule.

**Out of scope:**
- Rendering the PDF flyer (handled by FR54 using FR51's output).
- Sending the CPSC messages (handled by FR59 Orchestrator).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-072` | Challenge Funnel Brief | Blueprint JSON for FR54 creation | FR51 | FR54, FR59 |

### Academic Grounding
- **Research Paper:** *Implementation Intentions: Strong Effects of Simple Plans* (Gollwitzer, 1999) + *Hyperbolic Discounting and Procrastination* (Bisin & Hyndman, 2014).
- **Mechanism:** "Naive" hyperbolic discounters procrastinate because they lack structural decision boundaries. The $9 commitment acts as a bounded "reductive activity," explicitly ending the SEARCH phase (FR-CBCS-06) and initiating the Action phase without requiring massive intrinsic motivation.

### Key Files
- `challenge_routing.py` (New script to manage coping array math)
- `bmad-bmm-workflows-cpsc-generator.md` (Workflow definitions)

### Technical Decisions
- **Character Lexicon Anchoring:** Unlike V1 templates, FR51 explicitly queries `DEP-ENG-017` (Character Lexicon) Category 1 (Heroes) for the success frame, and Category 4 (Enemies) for the failure contrast state, guaranteeing tribal resonance.
- **ADR-01 Isolation Constraint:** All generated briefs map strictly to the `coach_id`. Data cannot cross-pollinate between instances.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Challenge Duration & Tone)
- **Agent:** `challenge-funnel-architect`
- **Inputs:** 
  - `tribe_ict_aggregate` (DEP-ID: `PROPOSED: DEP-ENG-058` — Produced By: FR-CBCS-04)
  - `character_lexicon` (DEP-ID: `DEP-ENG-017` — Produced By: FR0C)
  - `coach_voice_dna` (DEP-ID: `DEP-LIB-002` — Produced By: FR3)
  - `user_requested_price` (DEP-ID: `frontend_ui_input` — Produced By: Operator Dashboard)
- **Outputs:**
  - JSON parameters mapped in schema.
- **Failure Condition:** If `character_lexicon` returns `null` for Category 1 Heroes, generation throws `MissingTribalAnchorException`, halting compilation.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `coach_id` + `configured_price` + `generation_timestamp` + `tribe_modal_coping_position` logged to Subabase. **(Mandatory Execution)**.

**Variable Resolution Rule:** The `challenge_duration_days` (Enum: `5` | `7`) and `structure_focus` string Enums resolve mapping the mathematical Mode of the Tribe's `coping_position` array from `tribe_ict_aggregate`:
- **"5_DAY_MOMENTUM"**: Evaluates `True` IF `tribe_modal_coping_position <= 2` (Ill-Informed Bridge). *Logic:* Shorter duration prioritizes quick wins before fatigue. Focus is basic education. `challenge_duration_days` resolves to `5`.
- **"7_DAY_IDENTITY"**: Evaluates `True` IF `tribe_modal_coping_position >= 3` (Selective Engagement). *Logic:* Longer duration pushes through cognitive resistance. Focus is abstract identity shift. `challenge_duration_days` resolves to `7`.

### Stage 2: Commitment Device Validation Gating
- **Agent:** `challenge-funnel-architect`
- **Inputs:** `user_requested_price` (Float)
- **Outputs:** `challenge_funnel_brief` (Final JSON, DEP-ENG-072)
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `commitment_price` logged mapping to `funnel_blueprint_id`. **(Mandatory Execution)**.
- **Failure Condition:** Hard block on >$17 evaluation.

**Quality Gate:** **The Commitment Device Validation Gate**
- **Triggered when:** The node evaluates the `user_requested_price` prior to LLM compilation.
- **Exact Thresholds:**
- **Verdict - PASS:** `user_requested_price >= 1` AND `<= 17`. *Downstream Consequence:* Value is locked as `commitment_price`. System populates `gate_verdict = PASS`. Funnel generation authorized.
- **Verdict - PROVISIONAL:** `user_requested_price == 0`. *Downstream Consequence:* System pauses generation. Pushes UI warning modal: "Free challenge violates commitment science. Operator must click 'Acknowledge Reduced Conversion'." System populates `gate_verdict = PROVISIONAL_FREE_ACCEPTED`.
- **Verdict - FAIL:** `user_requested_price > 17`. *Downstream Consequence:* Generation hard blocked. UI Error: "Price exceeds psychological friction boundaries for Coping Tier 3." System populates `gate_verdict = FAIL_OVERPRICED`, script aborts returning `null` payload.

### Phase 3: Field-by-Field Schema Mapping
Every field in the JSON maps explicitly:
- `funnel_blueprint_id`: Returns `uuid.uuid4()`.
- `coach_id`: Returns `auth.uid()` from request context enforcing ADR-01.
- `challenge_duration_days`: Returns Integer (`5` or `7`) derived from Stage 1 ICT Math mapping rule.
- `structure_focus`: Returns String Enum (`"5_DAY_MOMENTUM"` | `"7_DAY_IDENTITY"`) derived from Stage 1 mapping.
- `commitment_price`: Returns Float locked by the Stage 2 Commitment Gate.
- `hero_anchor_noun`: Returns `character_lexicon["category_1_heroes"][0]` mapped directly.
- `enemy_contrast_noun`: Returns `character_lexicon["category_4_enemies"][0]` mapped directly.
- `flyer_hook_text`: Returns LLM generation explicitly constrained by system prompt: `len(hook.split()) <= 6`.
- `gate_verdict`: Returns String mapped explicitly by Stage 2 ("PASS" | "PROVISIONAL_FREE_ACCEPTED" | "FAIL_OVERPRICED").
- `generated_at`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ChallengeFunnelBrief (DEP-ENG-072)",
  "type": "object",
  "properties": {
    "funnel_blueprint_id": { "type": "string", "format": "uuid" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "challenge_duration_days": { "type": "integer", "enum": [5, 7] },
    "structure_focus": { "type": "string", "enum": ["5_DAY_MOMENTUM", "7_DAY_IDENTITY"] },
    "commitment_price": { "type": "number", "minimum": 0 },
    "hero_anchor_noun": { "type": "string" },
    "enemy_contrast_noun": { "type": "string" },
    "flyer_hook_text": { "type": "string" },
    "gate_verdict": { "type": "string", "enum": ["PASS", "PROVISIONAL_FREE_ACCEPTED", "FAIL_OVERPRICED"] },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "required": [
    "funnel_blueprint_id", "coach_id", "challenge_duration_days", "structure_focus",
    "commitment_price", "hero_anchor_noun", "enemy_contrast_noun", "flyer_hook_text", 
    "gate_verdict", "generated_at"
  ]
}
```

---

## 6. Backward Compatibility Fallback
Active campaigns using unstructured "Free 28-Day PDF" funnels configured prior to this architectural upgrade cannot be programmatically modified to charge $9 retroactively to avoid Stripe integration collisions. 
The system allows them to complete their lifecycle, but the "Duplicate Funnel" UI button relies on FR51 and will force the user through the `Commitment Device Validation Gate` on duplication, pushing compliance on the next iteration.

---

## 7. Tasks
- [ ] Task 1: Code `challenge_routing.py` to calculate the mathematical Mode of `coping_position` arrays passing outputs to the Stage 1 resolution logic.
- [ ] Task 2: Implement the `CommitmentGateEvaluator` Python class managing the float boundary math (`>=1`, `<=17`) and returning the defined Enums before the LLM hook.
- [ ] Task 3: Plumb `Receipt Chain Guard` writes into both Stage 1 and Stage 2 Python definitions using cryptographic hashes.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Price Block):** User inputs `$49` for the challenge price into the UI. Gate MUST evaluate `FAIL_OVERPRICED` and abort. **Failure Example:** The system passes the value to the PDF generator, creating a "micro-commitment" flyer advertising a high-friction price, instantly killing conversions.
- [ ] **AC2 (Provisional Acknowledgement):** User inputs `$0` and hits submit. Gate MUST evaluate `PROVISIONAL_FREE_ACCEPTED` after UI click. **Failure Example:** The LLM auto-generates a free challenge assuming it's optimal without warning the operator, ignoring the Hyperbolic Discounting defense mechanism.
- [ ] **AC3 (Lexicon Binding Verification):** System executes for a Coach mapping with Category 4 Enemy `["The Hustle Culture"]`. Output schema `enemy_contrast_noun` MUST explicitly equal `"The Hustle Culture"`. **Failure Example:** The LLM hallucinates generic enemy nouns like `"laziness"`, losing all tribal connection.

---

## 9. Dependencies
- **Upstream:**
  - `FR-CBCS-04`: Produces Tribe ICT Aggregate (`PROPOSED: DEP-ENG-058`).
  - `FR0C`: Produces Character Lexicon (`DEP-ENG-017`).
  - `FR3`: Produces Voice DNA (`DEP-LIB-002`).
  - **UPSTREAM UNDEFINED**: Operator UI Input for `user_requested_price`.
- **Downstream:**
  - `FR54`: Consumes output (`PROPOSED: DEP-ENG-072`) for Asset rendering.
  - `FR59`: Consumes output for orchestration timelines.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)` API.
  - `Supabase` (for DB reads/writes isolated by ADR-01).

---

## 10. Testing Strategy

### Unit Tests
- `Test_Commitment_Gate_Float_Math`: Inject Synthetic Floats `[0.0, 9.0, 17.5, 99.9]`. Assert Gate Enum returns map perfectly `[PROVISIONAL_FREE_ACCEPTED, PASS, FAIL_OVERPRICED, FAIL_OVERPRICED]`.
- `Test_ICT_Mode_Evaluation`: Inject Synthetic Array `[1, 2, 2, 2, 5]`. Assert Mode = 2. Assert `challenge_duration_days` = 5 and `structure_focus` = `5_DAY_MOMENTUM`.

### Integration Tests
- `Test_Lexicon_Injection_DB_Fetch`: Mock `DEP-ENG-017` read. Pass to Architect node. Assert schema field `hero_anchor_noun` identically matches the database mock without LLM paraphrasing. Assert Receipt Chain logs the UUID hash.

### Safety / Isolation Tests
- `Test_ADR_01_Boundary`: Force query requesting Lexicon for `coach_id="A"` while authenticating as `coach_id="B"`. Assert complete pipeline crash via Supabase RLS triggering `UnauthorizedResourceException`.
