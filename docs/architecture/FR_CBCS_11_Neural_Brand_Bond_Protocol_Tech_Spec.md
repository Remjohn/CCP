# FR-CBCS-11: Neural Brand Bond Protocol — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F11, PRD §FR-CBCS-11

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Brands attempt to build loyalty by stating their values explicitly ("We believe in integrity and hard work"). However, the human brain processes abstract concepts in the semantic network, which is easily forgotten. True loyalty requires activation of the dorsomedial prefrontal cortex (dmPFC), which only fires when processing social information (stories about people).

### Solution
The Neural Brand Bond Protocol intercepts all brand value messaging (Capability Area 4) and forces the LLMs to translate abstract values into concrete social narratives. It utilizes the `dmPFC Semantic Gate` to guarantee that every brand message contains human actors and explicitly bans marketing clichés, ensuring the brand values are neurologically anchored.

### Scope
**In scope:**
- The `dmpfc-semantic-evaluator` executing string checks on generated assets.
- Enum resolution linking Core Brand Values to 3 distinct Story Structures.
- The `dmPFC Semantic Gate` handling PASS/PROVISIONAL/FAIL states.

**Out of scope:**
- Delivering the content to the app (handled by FR45).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-066` | dmPFC Gate Verdict | Quality filter for Brand nodes | FR-CBCS-11 | FR54 / FR17 |

### Academic Grounding
- **Research Paper:** *Neural Correlates of Narrative Persuasion* (Falk et al., 2010) + *The Neuroscience of Brand Trust* (Plassmann et al., 2012).
- **Mechanism:** Information presented as a narrative featuring human actors activates the dmPFC. Information presented as abstract facts ("synergy", "potential") activates the lateral prefrontal cortex. dmPFC activation is highly correlated with behavioral change and brand loyalty; lateral activation correlates with counter-arguing.

### Technical Decisions
- **Story Structuring:** The system does not allow the LLM to randomly invent stories. It maps the Coach's configured target brand value to one of three strictly defined structural frameworks, drastically reducing hallucination and maintaining tonal consistency.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Story Structure Mapping)
- **Agent:** `brand_story_planner.py` (Pre-processes before LLM trigger)
- **Variable Resolution Rule (Story Structure):** The `story_structure` Enum is populated by evaluating the string contained in `target_brand_value` (Origin: FR12 Core Schema):
  - **"HERO_JOURNEY"**: Evaluates `True` IF `target_brand_value` matches `(Expansion|Growth|Achievement|Success)`. *Instruction sent to LLM:* "Structure as a protagonist overcoming a specific external obstacle."
  - **"FAIL_STATE_WARNING"**: Evaluates `True` IF `target_brand_value` matches `(Security|Safety|Trust|Consistency|Discipline)`. *Instruction:* "Structure as a cautionary tale of a protagonist who ignored this value and suffered an avoidable consequence."
  - **"PARADIGM_SHIFT"**: Evaluates `True` IF `target_brand_value` matches `(Innovation|Disruption|Truth|Awakening)`. *Instruction:* "Structure as a sudden realization where a protagonist sees through a common industry lie."

### Stage 2: dmPFC Semantic Gating
- **Agent:** `dmpfc-semantic-evaluator` (Pi Extension executing post-generation)
- **Inputs:** 
  - `draft_brand_story` (DEP-ID: `DEP-ENG-054` / `DEP-ENG-017` — Produced By: FR54 / FR17 Generators)
  - `target_brand_value` (DEP-ID: `DEP-ENG-012` — Produced By: FR12 Core Schema Coach Config)
- **Outputs:** `PROPOSED: DEP-ENG-066` (dmPFC Gate Verdict JSON)
- **Failure Condition:** If the `draft_brand_story` string length is $<50$ words, throws `StoryTooShortException`, auto-failing to trigger the `rewind_generation()` loop.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `coach_id` + `eval_id` + `semantic_verdict` written to APM logs upon completion.

**Metrics Calculated via explicit parsing:**
- `social_nouns_count`: `REGEX_COUNT(draft, \b(person|friend|he|she|they|people|client|someone|brother|sister|manager)\b)`
- `brand_cliche_count`: `REGEX_COUNT(draft, \b(synergy|unlock your potential|next level|transform your life|scale your|10x|game changer|revolutionary)\b)`

### Stage 3: Quality Gate Extension
**Quality Gate:** **The dmPFC Semantic Gate**
- **Triggered when:** A brand storytelling asset (e.g., Z-Pattern Flyer, Friday Newsletter) finishes drafting.
- **Exact Thresholds:**
  - `Condition_1`: `social_nouns_count >= 2`  (Must have actors to trigger dmPFC).
  - `Condition_2`: `brand_cliche_count == 0` (Clichés trigger lateral PFC reactance).
  - `Condition_3`: `moral_sentiment_match == True` (NLP classification matches `target_brand_value`).
- **Verdict - PASS:** All 3 conditions are `True`. *Downstream Consequence:* Story is saved to the content delivery queue.
- **Verdict - PROVISIONAL:** Conditions 1 and 3 are `True`, BUT Condition 2 is `False` (`brand_cliche_count > 0`). *Downstream Consequence:* The story correctly uses humans to teach a moral, but relies on lazy marketing speak. The script pauses delivery and pushes the draft to the Operator Review queue flagged `"Marketing Speak Detected"`.
- **Verdict - FAIL:** Condition 1 is `False` (`social_nouns_count < 2`) OR Condition 3 is `False`. *Downstream Consequence:* The output is abstract philosophical rambling. The script intercepts, rejects it, and triggers `rewind_generation()`: "You wrote an essay, not a story. Inject a specific human character experiencing the consequence of this value."

### Stage 4: Resolution Rules for Output Schema
Every schema field maps to explicit integer strings calculated via regex:
- `eval_id`: `uuid.uuid4()`.
- `coach_id`: Extracted via config runtime context.
- `story_structure_used`: The specific String Enum resulting from Stage 1 mapping logic ("HERO_JOURNEY" | "FAIL_STATE_WARNING" | "PARADIGM_SHIFT").
- `semantic_verdict`: "PASS" | "PROVISIONAL_REVIEW" | "FAIL_REJECTED".
- `metrics_payload.social_nouns_found`: Driven strictly by `social_nouns_count` Regex execute.
- `metrics_payload.cliches_found`: Driven strictly by `brand_cliche_count` Regex execute.
- `evaluated_at`: `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type DmpfcGateVerdictRow = {
  eval_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  story_structure_used: "HERO_JOURNEY" | "FAIL_STATE_WARNING" | "PARADIGM_SHIFT";
  semantic_verdict: "PASS" | "PROVISIONAL_REVIEW" | "FAIL_REJECTED";
  metrics_payload: {
    social_nouns_found: number;
    cliches_found: number;
    moral_sentiment_matched: boolean;
  };
  evaluated_at: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
Active assets generated outside of the Storytelling Module (like pure educational worksheets) will bypass the `dmPFC Semantic Gate` entirely to prevent false negatives rejecting dry curriculum content. A schema tag `asset_type == 'NARRATIVE'` will functionally control the evaluator's activation path.

---

## 7. Tasks
- [ ] **Task 1: Pre-mapping Routing** - Write the dictionary mapping in `brand_story_planner.py` translating the arbitrary string values of the Core Brand config into the 3 strict Enums routing to the LLM system prompt.
- [ ] **Task 2: Regex Engine** - Maintain the strict list of "marketing-speak" phrases globally inside `brand_cliché_list.json` imported to `dmpfc-semantic-evaluator.py`.
- [ ] **Task 3: Operator Visibility** - In the CCF Next.js dashboard, display `metrics_payload.cliches_found` explicitly on the `PROVISIONAL_REVIEW` modal so the human knows exactly which words to delete.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Abstract Idea Prohibition):** "Integrity is the cornerstone of our coaching framework." evaluates `social_nouns_count = 0`. System MUST hit the Stage 3 rule evaluating `FAIL`, forcing a rewrite. **Failure Example:** The system passes the draft, flooding the Coach's Instagram with generic quotes that build zero narrative transportation.
- [ ] **AC2 (Cliche Detection Provisionality):** "When my client John used our framework, he unlocked his potential." validates `social_nouns = 1` and `cliche = 1`. System MUST hit PROVISIONAL evaluation. **Failure Example:** The LLM's weak verbiage slips through entirely, degrading the premium Sovereign brand image.
- [ ] **AC3 (Enum Framework Targeting):** A configured coach brand value of `"Discipline"` MUST successfully trace through Stage 1 resolving to `story_structure = 'FAIL_STATE_WARNING'`. **Failure Example:** The dictionary maps unmatched Strings to `null`, causing the LLM prompt to lack structural rules and hallucinating formats wildly.
