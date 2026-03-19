# FR-CBCS-08: Transportation Score Gate — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F8, PRD §FR-CBCS-08

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
When LLMs draft scripts for audio/voice delivery (Voice Notes, Podcasts), they default to logical, expository structures. Humans do not bond over logic; they bond over shared narrative experiences. Expository AI scripts fail to achieve "Narrative Transportation"—the psychological mechanism where a listener gets lost in a story, suspending disbelief and defensive counter-arguing.

### Solution
The Transportation Score Gate is a strict algorithmic quality filter applied to all Voice Delivery drafts prior to dispatch or Text-to-Speech (ElevenLabs) generation. It grades the draft against four components of Transportation Theory: Sensory Detail, Direct Conviction (Zero Distancing), Prosodic Match (Voice DNA parity), and Narrative Arc. 

### Scope
**In scope:**
- The `transportation-score-evaluator` analyzing drafted text arrays.
- Regex constraint mapping for Distancing Language and Sensory detail.
- Cosine similarity checking against Voice DNA metrics.
- Outputting the `PROPOSED: DEP-ENG-063` Transportation Gate Verdict.

**Out of scope:**
- Actually generating the voice audio (handled by FR55 or Operator).
- The initial LLM script generation prompt (handled by FR53 or FR10).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-063` | Transportation Gate Verdict | Hard gate for TTS audio | FR-CBCS-08 | Voice Note / TTS Pipelines |

### Academic Grounding
- **Research Paper:** *Transportation Into Narrative Worlds* (Green & Brock, 2000).
- **Mechanism:** Narrative Transportation requires rich imagery, emotional resonance, and a coherent timeline. When highly transported, listeners show significantly reduced counter-arguing (reactance) regardless of their prior beliefs, making it the most persuasive form of communication. Distancing language ("maybe", "I think") immediately breaks the spell.

### Technical Decisions
- **Execution Level:** The gate operates synchronously inside the `TillDone` Pi Extension loop immediately after the LLM agent finalizes the draft string.
- **Strict Prohibition:** "Maybe" and "Perhaps" are totally forbidden in CCF Voice Notes. They convey a lack of sovereign authority.

---

## 4. Implementation Plan

### Stage 1: Transportation Component Analysis
- **Agent:** `transportation-score-evaluator` (Python Pi Extension)
- **Inputs:** 
  - `voice_message_script_draft` (DEP-ID: `DEP-ENG-053` — Produced By: FR53 / FR10 Text Generator)
  - `coach_soul_json` (DEP-ID: `DEP-LIB-002` — Produced By: Voice DNA framework)
- **Outputs:** Evaluated metric integers and boolean arrays.
- **Failure Condition:** If `voice_message_script_draft` is completely empty, the system throws `ScriptEmptyException`, routing directly to a FAIL verdict. 
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `script_hash` + `gate_verdict` written to APM logs to verify the text was evaluated before audio generation.

### Stage 2: Variable Resolution Rules (Metrics)
The script calculates four specific metrics using explicit text parsing boundaries:
- **`sensory_detail_count`**: Evaluates `REGEX_COUNT(draft, \b(see|smell|hear|feel|taste|look|sound|dark|bright|cold|hot|heavy|light)\b)`.
- **`distancing_language_count`**: Evaluates `REGEX_COUNT(draft, \b(maybe|might|could|probably|perhaps|i think|sort of|kind of|guess)\b)`.
- **`prosodic_match`**: Evaluates `COSINE_SIMILARITY(draft_syntax_frequencies, coach_soul_json.syntax_baseline)`. Returns Float `0.0-1.0`.
- **`narrative_arc_present`**: Evaluates `True` IF NLP dependency matcher finds a transition from explicit past-tense context vectors to present/future-tense vectors (indicating movement/story).

### Stage 3: Quality Gate Extension
**Quality Gate:** **The Transportation Score Gate**
- **Triggered when:** LLM finishes generating the textual draft intended for audio rendering.
- **Exact Thresholds:**
  - `Condition_1`: `sensory_detail_count > 0`
  - `Condition_2`: `distancing_language_count == 0`
  - `Condition_3`: `prosodic_match >= 0.85`
  - `Condition_4`: `narrative_arc_present == True`
- **Verdict - PASS:** All 4 conditions evaluate to `True`. *Downstream Consequence:* Draft is permanently saved and dispatched to the Text-To-Speech engine.
- **Verdict - PROVISIONAL_REVIEW:** Conditions 2, 3, and 4 are `True`, BUT Condition 1 (`sensory_detail`) is `False`. *Downstream Consequence:* The script is structurally safe and maintains Voice DNA, but lacks vivid imagery to invoke high transportation. Draft is saved but pushed to the `operator_review_queue` UI tagged "Missing Imagery" rather than hard-failing the generation loop. Operator can choose to manually approve or edit.
- **Verdict - FAIL:** Condition 2 is `False` OR Condition 3 is `False` OR Condition 4 is `False`. *Downstream Consequence:* Draft is strictly rejected. Triggers `rewind_generation()` passing the `failure_details` array back to the LLM agent to execute a rewrite constraint loop (Max 3 attempts).

### Stage 4: Resolution Rules for Output Schema
Every schema field maps to the following exact pipeline logic variables:
- `evaluation_id`: `uuid.uuid4()`.
- `script_hash`: SHA-256 string hash of the evaluated `voice_message_script_draft`.
- `gate_verdict`: Driven explicitly by the Enum outcomes defined in Stage 3 ("PASS" | "FAIL" | "PROVISIONAL_REVIEW").
- `metrics_payload.sensory_count`: Mapped directly to Stage 2 `sensory_detail_count`.
- `metrics_payload.distancing_count`: Mapped directly to Stage 2 `distancing_language_count`.
- `metrics_payload.prosodic_match_score`: Mapped directly to Stage 2 `prosodic_match`. 
- `metrics_payload.narrative_arc_found`: Mapped directly to Stage 2 boolean.
- `failure_details`: An array of strings. IF Enum == FAIL, system appends specific errors: `["Failed Condition 2: Remove distancing language.", "Failed Condition 4: No narrative structure detected."]`. Empty array if PASS.
- `evaluated_at`: `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type TransportationGateVerdict = {
  evaluation_id: string; // uuid4
  script_hash: string; // sha-256
  gate_verdict: "PASS" | "FAIL" | "PROVISIONAL_REVIEW"; // Explicit enum map
  metrics_payload: {
    sensory_count: number;
    distancing_count: number;
    prosodic_match_score: number; // Float 0.0-1.0
    narrative_arc_found: boolean;
  };
  failure_details: string[]; // Resolution exactly matches False conditions
  evaluated_at: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For FR10 Daily Ritual voice notes generated prior to the V3 pipeline:
- These historical texts are bypassed. The `Transportation Score Gate` only evaluates net-new strings emitted via the real-time Generator nodes.

---

## 7. Tasks
- [ ] **Task 1: NLP Evaluator Script** - Create `transportation_evaluator.py` containing the precise regex boundaries blocking the specific 9 Distancing words and gating the 13 Sensory words.
- [ ] **Task 2: Cosine Similarity Hook** - Integrate the NumPy math measuring `prosodic_match` against the upstream Voice DNA JSON library schema.
- [ ] **Task 3: TillDone Extension** - Integrate the `PASS/FAIL/PROVISIONAL_REVIEW` gate routing logic directly into the AI synthesizer to trigger regenerative loops.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Zero Distancing Prohibition):** Draft input "I think maybe we should focus on..." evaluates to `distancing_language_count = 2`. The gate MUST evaluate to `FAIL`, rejecting the script. **Failure Example:** The system ignores the regex constraint and synthesizes a weak, uncertain Voice Note that undermines the Sovereign Image Rule.
- [ ] **AC2 (Provisional Imagery Escalation):** Draft input passes Distancing, achieves `0.88` Prosodic Match, and contains a past->present shift, BUT contains zero sensory nouns. Gate MUST evaluate to `PROVISIONAL_REVIEW`. **Failure Example:** The script gets hard-rejected and caught in an infinite rewrite loop because the LLM struggles to generate irrelevant visual imagery for a purely philosophical topic.
- [ ] **AC3 (Valid Output Resolution):** An evaluated script hitting `PASS` MUST return `failure_details` as an explicitly empty array `[]`. **Failure Example:** Evaluates to a `null` object pointer crashing the downstream JSON ingestion script passing data to ElevenLabs.
