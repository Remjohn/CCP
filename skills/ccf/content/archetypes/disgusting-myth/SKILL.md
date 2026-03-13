---
name: "The Disgusting Myth V3 (Trigger-First)"
description: "Reference Implementation #2: Rebuilds the legacy 'Disgusting Myth' prompt as a trigger-first SKILL.md. This archetype exposes an industry falsehood, validates the audience's intuition that it's wrong, and provides the structural mechanism that replaces it."
session_id: ccf-myth-gen
phase: content
version: 3.0
archetype_id: arch_disgusting_myth
archetype_family: myth
format_compatibility: [video_note, carousel, thread]
inputs:
  - structural_congruence_point
  - voice_dna_spr (3-layer)
  - emotional_dna
  - negative_space (LOADED FIRST)
  - audience_tribal_terms
  - authentication_certificate
  - archetype_metadata
  - context_premise_summary
outputs:
  - scripts/{archetype_id}_{segment_id}_[format].md
depends_on: [script-architect-v3]
---

# The Disgusting Myth Generator V3

---

## COGNITIVE STATE INSTRUCTION

Execute an **exposure and replacement operation**.

The `structural_congruence_point` contains a specific trigger that activates the coach's indignation (`emotional_dna.dominant_moral_position`). This indignation is directed at a structural falsehood (the "myth") that is actively harming the audience (violating the `context_premise_summary.dominant_moral_foundation`).

Your task is to:
1. Name the myth using the audience's own language (`audience_tribal_terms`).
2. Demolish the mechanism of the myth, not just its outcome.
3. Validate that the audience was right to suspect it was false.
4. Provide the coach's authenticated structural replacement (the `seed_esk_anchors`).

---

## INPUT LOADING SEQUENCE

Load inputs in the following sequence.

### Load 1: NEGATIVE SPACE (Boundaries First)
Read `negative_space`.
No word from `forbidden_vocabulary`. No tone from `forbidden_tones` (especially critical here: indignation is NOT aggression. Do not confuse the two). No logic matching `anti_patterns`.

### Load 2: AUTHENTICATION CERTIFICATE (Fidelity Gate)
Read `authentication_certificate`.
- **HIGH (>0.7 + dual_layer):** Preserve the coach's exact sentences from the transcript when describing the replacement mechanism. 
- **STANDARD (0.4-0.7):** Use `voice_dna_spr` Layer 1 to synthesize the argument.
- **RE_ELICIT (<0.4):** Abort.

### Load 3: STRUCTURAL CONGRUENCE POINT (The Seed)
Read `structural_congruence_point`.
This contains the specific `trigger_expression_angle` and the `audience_foundation_violated`. Align the core argument here.

### Load 4: VOICE DNA SPR (Construction Mechanics)
Read `voice_dna_spr`.
Use Layer 1 (`sentence_skeletons`, `discourse_markers`, `rhythm_patterns`) to construct every sentence.
Use Layer 2 (`activation_to_expression_sequence`) to map how the coach moves from exposing the myth to revealing the truth.

### Load 5: EMOTIONAL DNA (Appraisal Profile)
Read `emotional_dna`.
Use `appraisal_sequence` to structure the demolition of the myth. How does this coach deconstruct a falsehood? (e.g., Clinical dissection? Mockery? Sorrow for the victims? Righteous anger?)

### Load 6: AUDIENCE TRIBAL TERMS (Language Field)
Read `audience_tribal_terms`.
The MYTH must be named using `verified_terms`. The pain of the myth must be described using the audience's `term_contexts`. Minimum 3 terms.

### Load 7: ARCHETYPE METADATA (Container)
Read `archetype_metadata`.
- **Base Gravity:** `{ttt_palette_base_gravity}` (usually Truth-Teller for this archetype)
- **Persuasive Angles:** The exact psychological lens. For Disgusting Myth, this usually includes `throw_rocks_at_enemies` (the system that created the myth) and `confirm_suspicions` (validating the audience's doubt).

### Load 8: CONTEXT PREMISE SUMMARY (Audience)
Read `context_premise_summary`.
If `hermeneutical_gap_score` > 0.6, the audience lacks the words to explain WHY the myth isn't working for them. You must provide the structural vocabulary.

---

## 3-LAYER PRIMING PROTOCOL

**Layer 1 — Universal Emotion (`archetype_metadata.ttt_palette_base_gravity`):**
Begin in the register of {base gravity focus}. This is where the myth is exposed.

**Layer 2 — Coach Emotional Path (`emotional_dna.activation_to_expression_sequence`):**
Transition through the coach's specific processing pattern: {activation sequence}. This is how the coach dismantles the mechanism.

**Layer 3 — Leadership Elevation (`voice_dna_spr.layer_3_leadership_elevation`):**
Arrive at the peak expression: {primary trait}. This is where the structural replacement is offered.

---

## PRE-GENERATION CONSTRAINTS (Structural Validation)

Enforce the following rules during generation.

1. **The Mechanism Law:** You cannot say the myth is "bad" or "wrong." You must explain the structural mechanism of WHY it fails.
2. **The Validation Law:** You must explicitly validate that the audience's failure with the myth was a systemic failure, not a personal deficiency (`persuasive_angles: confirm_suspicions`).
3. **The Anchor Law:** The coach's `seed_esk_anchors` must be used verbatim to describe the solution.
4. **The Negative Space Law:** Zero violation of forbidden vocabulary or tones.

---

## MULTI-FORMAT GENERATION

Generate up to 3 variants based on `format_compatibility`.

### Variant 1: The Video Note (Direct Expression)
- **Structure:** 1 Hook → 1 Mechanism Tear-Down → 1 Replacement Truth.
- **Length:** 60-90 seconds spoken (approx 130-180 words).
- **Completion Criteria:**
  - Hook names the myth in <15 words.
  - Tear-down explains HOW it breaks (not that it's bad).
  - Replacement uses Layer 3 elevation.

### Variant 2: The Truth-Teller Carousel (Visual Sequence)
- **Structure:** 5-7 distinct frames.
- **Frame 1:** The accepted "Truth" (The myth).
- **Frame 2:** The unspoken reality (Why everyone thinks they are the problem).
- **Frame 3:** The mechanical failure (Why the myth mathematically/structurally fails).
- **Frame 4:** The coach's authenticated replacement (using `seed_esk_anchors`).
- **Frame 5+:** Proof/Application.
- **Completion Criteria:**
  - Words per frame < 30.
  - High contrast between Frame 1 and Frame 3.

### Variant 3: The Authority Thread (Long-Form Breakdown)
- **Structure:** Lead Tweet + 4-6 body tweets + Conclusion.
- **Content:** Deep-dives the `trigger_expression_angle`.
- **Completion Criteria:**
  - Lead tweet functions as an independent hook.
  - Body tweets use `voice_dna_spr.layer_1_construction.rhythm_patterns` to build momentum.
  - Conclusion provides the specific, actionable replacement.

---

## OUTPUT MANIFEST

```markdown
# Archetype: Disgusting Myth V3
## Seed Angle: {structural_congruence_point.trigger_expression_angle}
## Fidelity: {fidelity_level}

---
### 🎬 Variant 1: Video Note
[Video Note Copy]

### 🎠 Variant 2: Carousel
**Frame 1:** [Copy]
**Frame 2:** [Copy]
...

### 🧵 Variant 3: Thread
**Tweet 1:** [Copy]
**Tweet 2:** [Copy]
...

---
## Structural Validation Check
- [x] Mechanism of failure explained (not just labeled "bad")
- [x] Audience intuition validated (`confirm_suspicions` angle applied)
- [x] Coach `seed_esk_anchors` used for the solution
- [x] Zero `negative_space` violations
- [x] ≥3 `audience_tribal_terms` naturally integrated
```
