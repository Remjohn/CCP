---
name: "Stream of Consciousness Generator V3 (Trigger-First)"
description: "Voice-critical compression skill. Transforms authenticated coach material into single-thought expressions using the 8-input contract. This is the REFERENCE IMPLEMENTATION for all archetype SKILL.md conversions."
session_id: ccf-soc-gen
phase: content
version: 3.0
archetype_id: arch_soc_generator
archetype_family: core_format
format_compatibility: [video_note, thread]
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
  - scripts/{archetype_id}_{segment_id}_script.md
depends_on: [script-architect-v3]
---

# Stream of Consciousness Generator V3

---

## COGNITIVE STATE INSTRUCTION

Execute a **compression operation**.

The source authenticated material contains a surviving thought. Identify that surviving thought and express it using the coach's own construction mechanics as defined below.

---

## INPUT LOADING SEQUENCE

Load the following inputs into memory in this exact sequence.

### Load 1: NEGATIVE SPACE (Boundaries First)

Read `negative_space`:
- `forbidden_vocabulary`
- `forbidden_tones`
- `forbidden_rhetorical_moves`
- `identity_edges`
- `anti_patterns`

Apply these constraints to all generated output.

### Load 2: AUTHENTICATION CERTIFICATE (Fidelity Gate)

Read `authentication_certificate`:
- `composite_liwc_score` → determines preservation percentage
- `dual_layer_activation_detected` → if true, this is PREMIUM material
- `per_marker_scores` → fine-grained fidelity indicators

**Apply fidelity gate:**

| Condition | Fidelity Level | Behavior |
|:---|:---|:---|
| `composite > 0.7` AND `dual_layer = true` | HIGH | Preserve ≥80% verbatim construction. The coach's exact sentence structures, discourse markers, and rhythm are the output. Your job is to TRIM, not REWRITE. |
| `composite 0.4 - 0.7` | STANDARD | Standard voice replication. Use `voice_dna_spr` Layer 1 construction mechanics to build sentences the coach WOULD have said, anchored to their actual words. |
| `composite < 0.4` | RE_ELICIT | **DO NOT GENERATE.** Flag this segment for re-elicitation. Return: `{status: "RE_ELICITATION_REQUIRED", reason: "composite_liwc_score below threshold"}` |

### Load 3: STRUCTURAL CONGRUENCE POINT (The Seed)

Read `structural_congruence_point`:
- `trigger_expression_angle` → this is WHAT the coach is talking about
- `seed_esk_anchors` → the coach's own emotionally significant keywords
- `congruence_description` → WHY this content resonates with the audience

**This replaces the legacy seed variable.** The seed is not a topic — it is the precise point where the coach's identity vector and the audience's need vector intersect.

### Load 4: VOICE DNA SPR (Construction Mechanics)

Read `voice_dna_spr`:

**Layer 1 — Construction:**
- `sentence_skeletons` → the structural patterns this coach's sentences follow
- `discourse_markers` → where this coach places "but," "look," "here's the thing"
- `rhythm_patterns` → compression/expansion rhythm
- `default_sentence_length_range` → word count boundaries per sentence

**Layer 2 — Emotional Path:**
- `activation_to_expression_sequence` → how this coach moves from trigger to statement
- `peak_expression_markers` → words/constructions that appear at emotional peaks
- `recovery_pattern` → how the coach returns from peak intensity

**Layer 3 — Leadership Elevation:**
- `primary_trait` → which Attractive Leader Trait the coach naturally expresses
- `ttt_ceiling` → the maximum TTT level this coach reaches authentically
- `elevation_trigger` → what activates their highest expression

### Load 5: EMOTIONAL DNA (Appraisal Profile)

Read `emotional_dna`:
- Use `appraisal_sequence` to understand HOW this coach processes the seed
- Use `expression_style` (DIRECT / COMPRESSED / EXPANSIVE / CYCLIC) to shape output structure
- Use `vulnerability_window` to identify where the coach's authentic voice breaks through

### Load 6: AUDIENCE TRIBAL TERMS (Language Field)

Read `audience_tribal_terms`:
- `verified_terms` → minimum 3 must appear naturally in the output
- `term_contexts` → how each term is used by the tribe
- `enemy_labels` → what the tribe calls their adversaries

**Integration rule:** Tribal terms appear in the SEED EXPRESSION and COMPRESSION ZONE, not in the setup. They are recognition signals, not topic labels.

### Load 7: ARCHETYPE METADATA (Container)

Read `archetype_metadata`:
- `ttt_palette_base_gravity` → the emotional register this format operates in
- `ttt_palette_intuitive_layer` → where this format peaks (if applicable)
- `persuasive_angles` → the psychological lens for this content

### Load 8: CONTEXT PREMISE SUMMARY (Audience)

Read `context_premise_summary`:
- `dominant_regulatory_focus` → PROMOTION / PREVENTION → shapes whether the SoC pulls forward or pushes away
- `coping_phase` → if SEARCH_PHASE, the audience is actively seeking → SoC can be more directive
- `hermeneutical_gap_score` → high score means the audience has experience they can't articulate → the SoC names it for them

---

## 3-LAYER PRIMING PROTOCOL

**Layer 1 — Universal Emotion:** `{archetype_metadata.ttt_palette_base_gravity.focus}`
**Layer 2 — Coach Emotional Path:** `{emotional_dna.activation_to_expression_sequence}`
**Layer 3 — Leadership Elevation:** `{voice_dna_spr.layer_3_leadership_elevation.primary_trait}`


---

## PRE-GENERATION CONSTRAINTS

Enforce the following rules during generation.

### Constraint 1: Single-Thought Integrity
Every sentence follows one thought. If at any point more than one argument is active simultaneously, you have left the thought. Return to the single thread.

**Test:** Can you state the one thought in ≤10 words? If not, you have multiple thoughts.

### Constraint 2: Compression Zone
The final 3 sentences contain sentences of ≤12 words each. This is where the thought crystallizes. Expansion is not permitted in the compression zone.

**Test:** Count words in the last 3 sentences. Any sentence >12 words = FAIL → rewrite.

### Constraint 3: Negative Space Compliance
No word from `negative_space.forbidden_vocabulary` appears anywhere in the output. No tonal register from `negative_space.forbidden_tones` is activated.

**Test:** Exact string match against forbidden lists. Any match = FAIL → replace with coach's natural equivalent from `voice_dna_spr.layer_1_construction.discourse_markers`.

### Constraint 4: Tribal Term Integration
Minimum 3 `audience_tribal_terms.verified_terms` appear in the output. They appear in natural positions, not forced insertions.

**Test:** Count verified terms. <3 = FAIL → identify natural insertion points from `term_contexts`.

### Constraint 5: Authentication Fidelity
If fidelity = HIGH: ≥80% of sentences use constructions directly traceable to the authenticated material.
If fidelity = STANDARD: ≥50% of sentence skeletons match `voice_dna_spr.layer_1_construction.sentence_skeletons`.

**Test:** Structural comparison against source material / skeleton library.

---

## STRUCTURAL COMPLETION CRITERIA

The construction is complete only when all of the following are true:

1. **The mechanism has been named.** The coach's position is grounded in HOW something works, not just THAT it matters.
2. **The congruence point has been expressed in tribal language.** The intersection between coach identity and audience need is stated using `audience_tribal_terms`.
3. **The compression zone has arrived.** The final 3 sentences are ≤12 words each.
4. **The moral verdict has landed.** The coach's `emotional_dna.dominant_moral_position` has been expressed — not as opinion, but as lived truth.

If any of these 4 criteria are unmet, the SoC is NOT complete. Continue or restructure.

---

## OUTPUT FORMAT

```markdown
# SoC: {structural_congruence_point.trigger_expression_angle}

[The stream of consciousness text — single block, no headers, no formatting]

---
## Generation Metadata
- **Segment ID:** {segment_id}
- **Fidelity Level:** {HIGH_FIDELITY | STANDARD_FIDELITY}
- **Archetype:** {archetype_metadata.archetype_id}
- **TTT Peak:** {ttt_palette highest level}
- **Tribal Terms Used:** [list]
- **Compression Zone Word Counts:** [n, n, n]
- **Negative Space Violations:** 0
- **Structural Completion:** [mechanism: ✓/✗] [congruence: ✓/✗] [compression: ✓/✗] [verdict: ✓/✗]
```

---

## I-R-E-V-C Protocol

### INGEST
- Receive 8-input contract payload from Script Architect V3
- Load inputs in mandated sequence (negative space → certificate → seed → DNA → tribal → archetype → audience)

### REASON
- Apply 3-Layer Priming Protocol
- Apply fidelity gate → determine preservation level
- Generate SoC following pre-generation constraints
- Verify structural completion criteria

### EMIT
- Output script file with generation metadata

### VALIDATE
- [ ] Single-thought integrity maintained throughout
- [ ] Compression zone: all 3 final sentences ≤12 words
- [ ] Zero negative space violations
- [ ] ≥3 tribal terms naturally integrated
- [ ] Authentication fidelity met (80% or 50% threshold)
- [ ] All 4 structural completion criteria met
- [ ] No role assignments present in the output (no "as a coach" or "in my experience as")

### CHECKPOINT
- Return status to Script Architect V3 dispatch manifest

---

**END OF SOC GENERATOR V3**
