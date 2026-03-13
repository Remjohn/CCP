# H8: Coach Soul Values Update — Implementation Architecture

**Hypothesis:** The Soul Values are the coach's extracted emotional DNA — vocabulary, metaphors, internal temperature, voice patterns. Currently, they are a static snapshot from a single transcript. They must become a dynamic, depth-stratified, monthly-updated intelligence layer.

**Pipeline Position:** CCF Setup Phase → feeds H3 (SoC Voice), all research analysts (Tone Emulation Protocol), all scripts, visual recipes  
**Existing Infrastructure:** `Conscious_Soul_Values.md` (48 lines, Coach Adele), `soul_values.json` (loaded by every CCF skill)  
**Gap Classification:** HIGH — Exists but static, single-source, surface-level  
**MCDA Score:** 8.65 / 10 (Rank #2)  
**Dependency:** Receives from H10 (Coach Philosophy Brief)

---

## Section 1: The Input Quality Problem

Soul Values currently extract from a single transcript and freeze. The coach's emotional vocabulary evolves — new metaphors emerge, old phrases are abandoned, the internal temperature shifts as the coach's life changes. A coach who was fiery and confrontational in January may have shifted to reflective and nurturing by June. The frozen Soul Values would still instruct all agents to write in January's voice.

### Input Saturation Gate

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| Coach Philosophy Brief (H10) | Must exist (even in BOOTSTRAP mode) | H10 output |
| Coach transcripts | ≥ 1 new transcript per update cycle | Interview recordings, voice notes |
| Previous `soul_values.json` | Must be loaded as baseline | Previous cycle output |
| Content performance data | Optional but enhances accuracy | Which voice patterns got highest engagement |

**Saturation test:** Soul Values cannot be updated without the H10 Philosophy Brief as context. The Philosophy Brief tells the extractor WHAT the coach believes; the Soul Values extraction tells the extractor HOW the coach talks about those beliefs.

---

## Section 2: The 4 Laws of Soul Values Distillation

### Law 1 — Emotional Vocabulary Stratification

The current Soul Values contain a flat list of positive and negative words. This is L1 extraction only. The law requires three layers:

- **L1 — Public Vocabulary:** Words the coach uses consistently in professional contexts. Their brand language. Example: *"transformation," "ancestral wisdom," "protocol."*

- **L2 — Intimate Vocabulary:** Words the coach uses only in vulnerable moments — when speaking about personal failure, family, fear, or unresolved pain. These words appear rarely but carry maximum emotional weight. Example: *"déracinée" (uprooted), "ma mère me disait..." (my mother used to tell me...).*

- **L3 — Collision Vocabulary:** Words or phrases that the coach uses inconsistently — sometimes positive, sometimes negative, depending on context. These reveal philosophical tension. Example: A coach who uses "discipline" positively when talking about health protocols but negatively when talking about colonial education. The word carries contradictory emotional charge.

**Depth distribution minimum:** ≥ 20% L2 vocabulary items, ≥ 5% L3 vocabulary items. A Soul Values file with only L1 vocabulary produces tone emulation that sounds like the coach's LinkedIn profile, not the coach's voice.

### Law 2 — Metaphor System with Provenance

The current Soul Values list metaphors without context. The law requires each metaphor to carry:

- **Source transcript:** Which session(s) did this metaphor appear in?
- **Emotional context:** What was the coach feeling when they used this metaphor? (TENSION / VULNERABILITY / RECOGNITION)
- **Frequency:** How often is this metaphor used? (Signature = ≥ 3 appearances; Emerging = 1-2 appearances; Abandoned = appeared in early transcripts, absent in recent ones)
- **Evolution tracking:** Has the metaphor changed form? A coach who initially said "life is a battle" but now says "life is a dance" has undergone a philosophical shift. Both versions must be recorded with their time period.

**Metaphor system test:** Take the 3 most frequent metaphors. Can each be traced to a specific transcript moment? If not, the extraction failed provenance.

### Law 3 — Internal Temperature Map (Dynamic)

The current Soul Values capture a single "internal temperature" — a general emotional intensity level. The law requires a **topic-indexed temperature map:** the coach's emotional intensity varies by subject.

| Topic | Temperature | Evidence |
|:------|:-----------|:---------|
| Health protocols | Hot — confrontational, urgent, prescriptive | "Il faut arrêter de..." (We must stop...) |
| Motherhood | Warm — tender, nostalgic, self-aware | "Quand j'ai eu mon premier enfant..." |
| Colonial legacy | Volcanic — raw anger, historical pain | Voice rises, sentences shorten, switches to Creole |
| Business/money | Cool — strategic, measured, pragmatic | Longer sentences, more qualifiers |
| Personal failure | Cold — withdrawn, minimal, deflective | Subject changes, short answers |

**Temperature map minimum:** ≥ 5 topic-temperature entries. The map must be re-evaluated monthly — new topics appear, temperatures shift as the coach processes experiences.

### Law 4 — Voice Authenticity Gate

Before the Soul Values update is finalized, it must pass 4 checks:

1. **Voice sample test:** Generate 3 paragraphs using the updated Soul Values as a voice guide. Read them without context. Do they sound like one person with a consistent voice, or like a committee? If committee, the extraction is capturing breadth without coherence.

2. **Depth verification:** L2 + L3 vocabulary items exist. Without them, downstream agents will emulate the coach's brand voice, not the coach's real voice.

3. **Temperature consistency:** Does the temperature map for a given topic match the actual transcript moments? Randomly verify 2 topic temperatures against source material.

4. **Evolution markers:** If this is an update (not initial creation), at least 2 evolution markers must be present: vocabulary items that changed status (new, strengthened, abandoned), metaphors that evolved, temperatures that shifted. If nothing changed, the update is either unnecessary or the extraction missed the changes.

---

## Section 3: The Monthly Update Loop

```
Month 1: Initial extraction (from H10 BOOTSTRAP brief + transcript)
  → soul_values_v1.json created
  → Marked as INITIAL

Month 2+: New transcript processed
  → Cross-reference against existing soul_values
  → New vocabulary classified (L1/L2/L3)
  → Metaphor system updated (new, evolved, abandoned)
  → Temperature map re-evaluated
  → Evolution delta recorded

Delta Output: What changed between v(N-1) and v(N)
  → New L2/L3 vocabulary discovered
  → Metaphors that evolved or were abandoned
  → Temperature shifts on specific topics
  → This delta feeds back to H10 Evolution Agenda
```

---

## Section 4: Output Format

```
soul_values_v{N}.json

├── metadata
│   ├── coach, version, date, transcript_sources
│   └── update_mode: INITIAL | MONTHLY_UPDATE
│
├── emotional_vocabulary
│   ├── L1_public: [{ word, frequency, usage_context }]
│   ├── L2_intimate: [{ word, frequency, emotional_context, transcript_source }]
│   └── L3_collision: [{ word, positive_context, negative_context, transcript_sources }]
│
├── metaphor_system
│   ├── signature: [{ metaphor, frequency, mode, transcript_sources, evolution_notes }]
│   ├── emerging: [{ metaphor, frequency, mode, transcript_source }]
│   └── abandoned: [{ metaphor, last_seen, replacement }]
│
├── internal_temperature_map
│   └── [{ topic, temperature, evidence_quote, transcript_source }]
│
├── voice_patterns
│   ├── sentence_rhythm: { avg_length, variation_pattern }
│   ├── profanity_level: 0-5
│   ├── code_switching: { triggers, patterns }
│   └── pacing: { fast_topics, slow_topics }
│
├── physical_description (brand avatar DNA — unchanged)
│
└── evolution_delta (if update)
    ├── new_vocabulary: []
    ├── evolved_metaphors: []
    ├── temperature_shifts: []
    └── abandoned_items: []
```

---

## Section 5: 5 Micro-Hypothesis Evaluations

**MH1 — Depth Distribution Test:** Count vocabulary items per layer. L2 < 20% or L3 < 5% → FAIL. Verifiable: parse the JSON and compute ratios.

**MH2 — Metaphor Provenance Test:** Select 3 signature metaphors. Each must trace to ≥ 1 specific transcript with timestamp/quote. Verifiable: check `transcript_sources` field against raw material.

**MH3 — Temperature Map Coverage Test:** The temperature map must cover ≥ 5 topics. Each topic must have an `evidence_quote` from a real transcript. Verifiable: count entries and check evidence fields.

**MH4 — Voice Coherence Test:** Generate 3 paragraphs using the Soul Values as voice guide, each on a different topic at different temperatures. Do they sound like the same person at different emotional intensities? If they sound like 3 different people, the extraction is fragmented. Verifiable: human evaluation or LLM consistency scoring.

**MH5 — Downstream Tone Emulation Test:** Feed the updated Soul Values to one research analyst (e.g., nostalgia-story deep analyst). Compare the research brief's voice quality against a brief generated with the old, flat Soul Values. Does the new brief sound more like the coach? Verifiable: A/B comparison of output voice.

---

## Validation Receipt

```
H8 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━
Coach:           [name]
Version:         [N]
Update Mode:     [INITIAL | MONTHLY_UPDATE]
Transcripts:     [count] sources processed
Date:            [timestamp]
H10 Brief:       [version used]

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Vocabulary Stratification:  [L1: X% | L2: Y% | L3: Z%]  [PASS/FAIL]
Law 2 — Metaphor Provenance:        [signature: n, emerging: n, abandoned: n]  [PASS/FAIL]
Law 3 — Temperature Map:            [n topics mapped]  [PASS/FAIL if < 5]
Law 4 — Authenticity Gate:          [4/4 checks passed]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Depth Distribution:    [PASS/FAIL]
MH2 Metaphor Provenance:   [PASS/FAIL]
MH3 Temperature Coverage:  [PASS/FAIL]
MH4 Voice Coherence:       [PASS/FAIL]
MH5 Downstream Tone:       [PASS/FAIL]

EVOLUTION DELTA (if update)
━━━━━━━━━━━━━━━━━━━━━━━━━━
New vocabulary:      [count]
Evolved metaphors:   [count]
Temperature shifts:  [count]
Abandoned items:     [count]

STATUS: [AUTHENTICATED / INITIAL / FAILED]
```
