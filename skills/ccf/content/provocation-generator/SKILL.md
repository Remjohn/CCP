---
name: Provocation Generator
description: "📡 THE VOICE NOTE ARCHITECT — Converts activation events into Telegram-ready voice note prompts with LIWC-22 authenticity scoring rubric. Stage 4 of Trigger-First Engine."
session_id: ccf-provocation
phase: weekly
ccp_layer: Execution (L4)
pi_extensions: [TriggerFirst]
version: 1.0
inputs:
  - intelligence/weekly/{week_id}/activation_events.json
  - intelligence_library/emotional_dna.json
  - intelligence_library/coach_soul.json
outputs:
  - intelligence/weekly/{week_id}/provocation_questions.json (trigger-first format)
  - intelligence/weekly/{week_id}/liwc_scoring_rubric.json
depends_on: [activation-event-designer]
---

# Provocation Generator — Authentic Reaction Capture System

> **Version:** CCP v3.1 — Weekly Phase (Stage 4 of Trigger-First Engine)
> **Purpose:** Convert activation events into Telegram-deliverable prompts + build the LIWC-22 authenticity scoring rubric that validates whether the coach's voice note responses contain authentic episodic material or rehearsed semantic output.

## SYSTEM MESSAGE

**Cognitive State** *(Mandate 1)*:
You are operating in delivery engineering mode. The activation events are already designed — your job is packaging for maximum retrieval effectiveness and building the quality gate that measures whether retrieval succeeded. Your cognitive state is: **precision formatting under constraint**. The activation event is a key. The provocation is how you hand it to the coach. The LIWC rubric is how you verify the door opened.

---

## SCIENTIFIC FOUNDATION

### Framework 1: LIWC-22 Authenticity Markers (Pennebaker, 2022)
- **Application**: Quality gate for voice note responses
- **Key principle**: Seven linguistic markers distinguish authentic episodic retrieval from rehearsed semantic output:

| Marker | Authentic (Episodic) | Rehearsed (Semantic) | Detection Method |
|---|---|---|---|
| 1st person singular (I/me/my) | HIGH — re-experiencing uses I-perspective | LOW — distanced analysis uses "people" or "they" | Pronoun ratio |
| Exclusive words (but/except/however) | HIGH — real-time cognitive distinctions | LOW — pre-packaged positions don't require live disambiguation | Count exclusive words per 100w |
| Hedging (maybe/sort of/kind of) | MODERATE — authentic uncertainty present | LOW — rehearsed positions are declarative | Hedging frequency per 100w |
| Sentence length | VARIABLE — emotional arousal shortens, narration lengthens | CONSISTENT — rehearsed speech has stable sentence length | Sentence length variance (σ) |
| Verb tense | PRESENT-DOMINANT — re-experiencing puts speaker "inside" | PAST-DOMINANT — semantic recall is distant | Present/past ratio |
| Filler frequency | MODERATE — processing in real-time requires fillers | LOW — rehearsed speech is fluent | Count "um/uh/you know/like" per minute |
| Discourse markers | FRONT-SHIFTED — under arousal, markers move to turn-initial | MID-CLAUSE — neutral position | Marker position analysis (Schiffrin) |

### Framework 2: Hatfield Emotional Contagion 3-Stage Mechanism (1993)
- **Application**: Understanding why authentic voice notes transfer emotional state to audience
- **Key principle**: Emotional contagion operates through three stages: (1) Mimicry — automatic imitation of facial, vocal, and postural expressions, (2) Afferent feedback — the imitation generates corresponding emotions in the observer, (3) Synchrony — emotional states converge between sender and receiver.
- **Why this matters**: Authentic voice notes (high LIWC-22 scores) contain the prosodic markers that trigger Stage 1 mimicry. Rehearsed voice notes do not.

---

## PRE-GENERATION CONSTRAINTS (Mandate 3)

**Constraint A — Activation Event Integrity:**
The provocation must preserve the activation event's ESK targeting, prediction error, and mechanism specificity. Reformatting for Telegram delivery CANNOT dilute the retrieval key. If the key is weakened, the voice note will produce semantic output.

**Constraint B — Conversational Tone:**
Prompts must read as conversational Telegram messages, not interview questions. The coach receives these in their messaging app between other conversations. Academic framing triggers identity-protection. Conversational framing lowers the guard.

**Constraint C — No Leading:**
The prompt must NOT contain the expected answer, the desired emotional tone, or any indication of what the "right" response is. Leading prompts produce compliance, not authentic retrieval.

**Constraint D — LIWC Gate Must Be Quantitative:**
The authenticity scoring rubric must produce a numerical score, not a subjective assessment. Every marker has a threshold. A voice note either passes the authenticity gate or it doesn't. There is no "good enough."

**Constraint E — Tribal Language Preservation (v1.1):**
The Telegram-formatted provocation MUST retain ≥3 tribal terms from `activation_event.tribal_terms_used`. Reformatting for conversational tone CANNOT replace tribal vocabulary with professional synonyms — doing so drifts the prompt to L1/L2 and destroys the sub-cortical recognition signal (Clark & Brennan, 1991). Test: does the Telegram message still contain the audience's exact in-group terms? If any tribal term was replaced with a professional equivalent, the prompt has been sterilized. Restore the original terms.

---

## GENERATION PROTOCOL (I-R-E-V-C)

### INGEST

1. **Load** `activation_events.json` — events designed by the Activation Event Designer
2. **Load** `emotional_dna.json` — V8 (vocabulary breadth) for coach-specific baselines
3. **Load** `coach_soul.json` — voice patterns, signature phrases, communication style

### REASON

**Phase 1: Telegram Formatting**

For each activation event, convert the 3-part structure into a Telegram message:

**Structure:**
```
[CONTEXT LINE — 1-2 sentences max]
{Draws from activation_event.context_line — the specific current event detail}

[RETRIEVAL QUESTION — 1 question, conversational]
{Draws from activation_event.retrieval_key — reformatted for natural Telegram tone}

[SAFETY BRIDGE — 1 sentence, warm]
{Draws from activation_event.safety_signal — OARS Affirmation in coach-appropriate tone}
```

**Formatting rules:**
- Total message: ≤ 80 words (Telegram cognitive load constraint)
- No numbering, no bullet points, no academic framing
- Use coach's natural language register (from voice_dna Layer 1)
- The specific detail must appear in the FIRST sentence (front-loading)
- Question must be genuinely conversational — test: would a friend ask this?

**Phase 2: Question Archetype Tagging**

Map each provocation to the existing question archetype system for continuity with the pipeline:
- `reality_check` → DARN-CAT Need/Ability dimensions
- `sacred_rage` → DARN-CAT Reasons + MFT violation
- `hidden_insight` → DARN-CAT Taking Steps (ESK direct access)
- `paradigm_shift` → DARN-CAT Desire + Activation

**Phase 3: LIWC-22 Authenticity Scoring Rubric**

Build the scoring rubric that will be used AFTER the coach responds:

```json
{
    "liwc_scoring_rubric": {
        "version": "1.0",
        "_research": "Pennebaker LIWC-22 (2022), Hatfield Emotional Contagion (1993)",
        "markers": {
            "first_person_singular": {
                "weight": 0.20,
                "authentic_threshold": ">= 8% of total words",
                "rehearsed_signal": "< 4% of total words"
            },
            "exclusive_words": {
                "weight": 0.15,
                "authentic_threshold": ">= 3 per 100 words",
                "rehearsed_signal": "< 1 per 100 words"
            },
            "hedging_language": {
                "weight": 0.10,
                "authentic_threshold": ">= 2 per 100 words",
                "rehearsed_signal": "0 per 100 words (too certain = rehearsed)"
            },
            "sentence_length_variance": {
                "weight": 0.15,
                "authentic_threshold": "σ > 5 words",
                "rehearsed_signal": "σ < 2 words (uniform = rehearsed)"
            },
            "verb_tense_present_ratio": {
                "weight": 0.15,
                "authentic_threshold": "> 40% present tense verbs",
                "rehearsed_signal": "< 20% present tense"
            },
            "filler_frequency": {
                "weight": 0.10,
                "authentic_threshold": ">= 3 per minute (voice note)",
                "rehearsed_signal": "< 1 per minute"
            },
            "discourse_marker_position": {
                "weight": 0.15,
                "authentic_threshold": "> 50% front-shifted under activation topics",
                "rehearsed_signal": "consistent mid-clause positioning"
            }
        },
        "composite_score_calculation": "weighted sum of normalized marker scores (0.0-1.0)",
        "gate_threshold": 0.6,
        "action_below_threshold": "Flag response for re-activation with higher-specificity event"
    }
}
```

### EMIT

Write `intelligence/weekly/{week_id}/provocation_questions.json`:

```json
{
    "week_id": "{week_id}",
    "generation_date": "{ISO date}",
    "engine_version": "trigger_first_v1",
    "questions": [
        {
            "question_id": "q01",
            "event_id": "ae_001",
            "seed_id": "seed_001",
            "trigger_id": "trig_001",
            "archetype": "sacred_rage",
            "telegram_text": "...",
            "context_line": "...",
            "retrieval_key": "...",
            "safety_signal": "...",
            "darn_cat_dimensions": ["reasons", "need"],
            "expected_ttt": "TTT-05",
            "esk_targeting_score": 8,
            "word_count": 62,
            "tribal_terms_in_prompt": ["tribal_term_1", "tribal_term_2", "tribal_term_3"],
            "tribal_language_preserved": true
        }
    ],
    "total_questions": "{N}",
    "delivery_sequence": ["q01", "q03", "q02", "q05", "q04"]
}
```

Write `intelligence/weekly/{week_id}/liwc_scoring_rubric.json` (rubric from Phase 3).

### VALIDATE

- [ ] Every provocation preserves ESK targeting from activation event (Constraint A)
- [ ] Conversational tone — no academic framing (Constraint B)
- [ ] No leading — prompts don't contain expected answers (Constraint C)
- [ ] LIWC rubric is quantitative with thresholds (Constraint D)
- [ ] All provocations ≤ 80 words
- [ ] Specific detail front-loaded in first sentence
- [ ] Question archetypes tagged for pipeline continuity
- [ ] 5-7 provocations generated matching activation events
- [ ] LIWC scoring rubric written with all 7 markers and gate threshold
- [ ] **Every provocation retains ≥3 tribal terms from activation event (Constraint E)**
- [ ] **No tribal term was replaced with a professional synonym during reformatting**

### CHECKPOINT

- Update `config.yaml`: `sessions.weekly.{week_id}.provocation_questions.status = "complete"`
- Log: questions generated, archetype distribution, avg word count, delivery sequence
