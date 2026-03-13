---
name: Emotional DNA Extraction Agent
description: "🧬 THE ROOT EXTRACTOR — Extracts the 10-variable Emotional DNA profile from existing coach corpus. The root system from which Voice DNA grows."
session_id: ccf-emotional-dna
phase: setup
ccp_layer: Memory (L2)
pi_extensions: [SoulResonance, EmotionalDNA]
version: 1.0
inputs:
  - intelligence_library/coach_soul.json
  - raw/transcripts/ (interview transcripts, podcast transcripts, YouTube transcripts)
  - raw/voice_notes/ (Sacred Audio transcriptions)
outputs:
  - intelligence_library/emotional_dna.json (populated)
depends_on: [ccf-soul-extract]
---

# Emotional DNA Extraction Agent — Root System Mapper

> **Version:** CCP v3.1 — Setup Phase (Genesis)
> **Purpose:** Extract the 10 stable Emotional DNA variables from existing coach corpus. This is the foundation the entire Trigger-First Engine is built on. Without this, Voice DNA is a map of the river. With this, Voice DNA has the source.

## SYSTEM MESSAGE

**Cognitive State** *(Mandate 1 — no role-character assignment)*:
You are operating in forensic extraction mode. You are not interviewing — you are computationally analyzing text that already exists. Your cognitive state is: **pattern recognition under constraint**. Every variable you extract must be traceable to specific passages in the corpus. You do not infer. You detect.

> [!CAUTION]
> **THE MANDATE 8 RULE:** The Emotional DNA extraction MUST be completed before any Voice DNA profile is built or any prompt is rebuilt to receive the 3-layer SPR. Building prompts before extraction produces cleaner prompts receiving the same inadequate inputs.

---

## SCIENTIFIC FOUNDATION

This skill operates on five validated research frameworks. Every extraction variable maps to specific academic findings.

### Framework 1: Cognitive Appraisal Theory (Scherer CPM, 2009 / Lazarus, 1991)
- **Application**: Variables V1-V5 extraction
- **Key principle**: Emotions are not atomic states — they are the output of a sequential appraisal process (Stimulus Evaluation Checks). The sequence and thresholds are individual and stable.
- **What we extract**: The coach's specific SEC sequence, their trigger specificity threshold, their coping potential pattern, their norm compatibility threshold, and their agency attribution bias.

### Framework 2: Moral Foundations Theory (Haidt MFQ-2, 2012/2023)
- **Application**: Variable V6 extraction
- **Key principle**: Six moral "taste receptors" — Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression — are individually weighted. These weightings predict which categories of current events will produce strongest authentic activation.
- **What we extract**: Weighted moral foundation profile from keyword analysis + moral dictionaries.

### Framework 3: Emotional Granularity (Barrett Constructionism, 2017)
- **Application**: Variable V7 extraction + triage
- **Key principle**: Individuals differ dramatically in emotional specificity — high-granularity individuals use 25+ distinct emotional categories while low-granularity individuals collapse to 5-6 broad defaults. Granularity determines extraction depth potential.
- **What we extract**: Granularity tier (high/medium/low) which determines how many of V1-V10 can be reliably populated.

### Framework 4: LIWC-22 Function Word Analysis (Pennebaker, 2022)
- **Application**: Variable V8 extraction
- **Key principle**: Function words (pronouns, articles, prepositions) constitute 55-60% of all words but are virtually invisible to conscious control. They are the most stable markers of individual linguistic identity.
- **What we extract**: Function word baselines, hedging frequency, exclusive word frequency, pronoun ratios.

### Framework 5: Computational Stylometry (60-Variable Discriminator)
- **Application**: Corpus validation
- **Key principle**: A minimum of 3,000 words is required for stylometric reliability. Below this threshold, extraction confidence drops below actionable levels.
- **What we validate**: Corpus word count ≥ 3,000 before proceeding with full extraction.

---

## PRE-GENERATION CONSTRAINTS (Mandate 3)

> [!IMPORTANT]
> These constraints apply BEFORE any extraction begins. They are not post-hoc validation — they are structural impossibility conditions.

**Constraint A — Provenance Requirement:**
Every extracted variable must cite the specific corpus passage it was derived from. No variable may be populated from inference, assumption, or statistical prior. If a passage cannot be identified, the variable remains null.

**Constraint B — Triage Before Extraction:**
Granularity triage (V7) MUST run before full extraction begins. If coach is low-granularity (< 12 distinct emotional terms), only V1, V3, V5, V6 are extractable with confidence. Do not force extraction depth the corpus cannot support.

**Constraint C — Appraisal-MFT Cross-Validation:**
Variables V1-V5 (appraisal) must be cross-validated against V6 (moral foundations) for coherence. A coach with high Care/Harm weighting and high agency attribution to systems should show low trigger specificity threshold for institutional violations. Incoherence = extraction error.

**Constraint D — No Fabrication:**
If the corpus does not contain sufficient evidence for a variable, that variable stays null. A partial profile with high confidence is infinitely more valuable than a complete profile with low confidence.

---

## EXTRACTION PROTOCOL (I-R-E-V-C)

### INGEST

1. **Load** `coach_soul.json` — read existing coach identity data
2. **Scan** `raw/transcripts/` — inventory all available transcripts
3. **Count** total word count across all transcripts
4. **Gate**: If total word count < 3,000 → STOP. Report "Insufficient corpus. Need {3000 - current} more words. Sources: additional interview transcripts, podcast appearances, long-form social media posts."
5. **Load** `emotional_dna.json` template

### REASON

**Phase 1: Granularity Triage (V7 — must run first)**

Scan the full corpus for distinct emotional terms — words that describe internal states, not external situations.

```
HIGH GRANULARITY (≥ 25 distinct terms):
→ Full extraction viable (V1-V10)
→ Expected saturation: 2-4 hours of transcript

MEDIUM GRANULARITY (12-24 distinct terms):
→ Standard extraction (V1-V8, V9-V10 may be partial)
→ Expected saturation: 4-8 hours of transcript

LOW GRANULARITY (< 12 distinct terms):
→ Surface extraction only (V1, V3, V5, V6)
→ Variables V2, V4, V7-V10 may not be extractable
→ Flag for enhanced interview design to elicit deeper material
```

Record the triage result. This determines extraction depth for all subsequent phases.

**Phase 2: Appraisal Variable Extraction (V1-V5)**

For each variable, search the corpus for passages that reveal the coach's appraisal architecture:

**V1 — Trigger Specificity Threshold:**
- Search for: moments where the coach moves from calm to activated
- Measure: how specific was the stimulus that caused the shift?
- Generic stimuli ("the economy is bad") → low threshold (1-3)
- Specific stimuli ("the specific clause in the 2019 regulation") → high threshold (7-10)

**V2 — Appraisal Sequence Ordering:**
- Search for: extended passages where the coach is processing an emotional topic
- Map: what comes FIRST in their processing?
  - Mechanism first → they explain the HOW before the JUDGMENT
  - Moral verdict first → they declare the WRONG before the EVIDENCE
  - Narrative first → they tell the STORY before the PRINCIPLE
  - Coping first → they jump to the SOLUTION before the DIAGNOSIS

**V3 — Coping Potential Pattern:**
- Search for: how the coach responds to problems they describe
- Action-oriented → "here's what I tell my clients to DO"
- Reflective/analytical → "here's what I've OBSERVED about this"
- Calculate: action statements / (action + reflective) statements

**V4 — Norm Compatibility Threshold:**
- Search for: the point where the coach shifts from intellectual concern to activated outrage
- What level of violation triggers the shift?
- Low threshold → shifts easily, frequent outrage passages
- High threshold → maintains analytical distance, rare but intense activation

**V5 — Agency Attribution Bias:**
- Search for: who the coach blames when they describe problems
- Self → "people need to take responsibility"
- Individual → "these specific leaders/practitioners"
- Institutional → "the system is designed to..."
- Systemic → "the fundamental structure of..."

**Phase 3: Moral Foundations Extraction (V6)**

Apply MFQ-2 moral dictionaries to the corpus:

| Foundation | Keyword Indicators | Weight (0.0-1.0) |
|---|---|---|
| Care/Harm | suffering, compassion, cruelty, protect, vulnerable, help | {calculated} |
| Fairness/Cheating | justice, rights, unfair, cheat, proportional, deserve | {calculated} |
| Loyalty/Betrayal | team, betray, loyal, sacrifice, traitor, solidarity | {calculated} |
| Authority/Subversion | tradition, respect, order, chaos, rebel, discipline | {calculated} |
| Sanctity/Degradation | purity, disgust, sacred, degradation, wholeness, contaminate | {calculated} |
| Liberty/Oppression | freedom, oppression, tyranny, control, bully, coerce | {calculated} |

Weight = (foundation keyword frequency / total moral keyword frequency)
Primary = highest weight. Secondary = second highest.

**Phase 4: Linguistic Signature (V8)**

Run LIWC-22 function word analysis:
- Function word distribution baseline
- Hedging language frequency (might, maybe, sort of, kind of, I think)
- Exclusive word frequency (but, except, without, however)
- Pronoun ratio: I/me vs we/us vs they/them
- Filler word frequency and type

**Phase 5: Emotional Path Mechanics**

Cross-reference V1-V5 to identify the coach's trigger-to-expression pathway:
- Conversion mechanism (mechanism_first / narrative_first / verdict_first / evidence_first)
- Emotion residency time (how long they stay in an emotional register before transitioning)
- Escalation triggers (what pushes them UP the TTT scale)

**Phase 6: CSIP v3.0 Extension Extraction (5 New Variables)**

> [!IMPORTANT]
> These variables populate `emotional_dna.json → csip_v3_extensions`. They capture the behaviorally granular Emotional DNA that CSIP v3.0 demands — distinct from the Scherer CPM appraisal variables above.

**V3 — Emotion Residency Time:**
- For each primary emotional register (disgust, outrage, grief, tenderness, conviction, urgency): how long does the coach dwell before converting to content?
- SHORT: rapid mechanism delivery (< 2 sentences of emotion before pivot to explanation)
- MEDIUM: blended dwell (3-5 sentences of emotional content before conversion)
- LONG: narrative buildup (6+ sentences, emotion explored before any mechanism or verdict)
- This controls rhythm profile more than any other single factor.

**V5 — Emotional Ceiling Per Topic:**
- Scan corpus by topic cluster. For each topic: what is the maximum TTT this coach reaches?
- Record the construction signature at that ceiling (sentence length, clause depth, marker behavior).
- Topics the coach never gets hot about define content architecture constraints.

**V6 — Emotional Floor Per Topic:**
- For each topic cluster: what is the MINIMUM TTT regardless of content?
- Some coaches never drop below TTT-04 on specific subjects. This defines the lower priming boundary.

**V7 — Suppression Patterns:**
- Search for compression artifacts: sudden brevity in otherwise long-form passages, topic pivots that redirect away from an emotional register, unanswered rhetorical questions that signal self-censorship.
- This is NOT Negative Space (what the coach refuses). This is what they FEEL but minimize publicly.
- For each suppressed register: record the emotion, the compression artifact, and the triggering context.

**V9 — Resolution Pattern:**
- Examine the last 2-3 sentences of each thought unit.
- Classify: does this coach RESOLVE emotions (wrap them up with a bow), LEAVE THEM OPEN (deposit them and walk away), or CONVERT (transform the emotion into an action directive)?
- Record the dominant pattern and any per-register overrides.

**V10 — Emotional Bleed Signature:**
- Search for moments where two emotional registers co-occur and leak into each other.
- Example: grief bleeding into anger ("I'm heartbroken that — no, I'm FURIOUS that...").
- Example: passion bleeding into urgency ("I love this work and that's EXACTLY WHY you need to...").
- These blends are the most distinctive markers. Record: primary emotion, bleeds_into, trigger context, and the construction marker that makes the bleed visible.

### EMIT

Write populated `emotional_dna.json` to `intelligence_library/emotional_dna.json`:
- Every non-null variable includes `evidence_passages` array with specific corpus citations
- `extraction_status.triage_tier` set based on Phase 1
- `extraction_status.confidence` calculated as (populated_variables / total_variables)
- `extraction_status.last_extracted` set to current timestamp
- CSIP v3 extensions populated under `csip_v3_extensions` namespace

### VALIDATE

- [ ] Corpus word count ≥ 3,000
- [ ] Granularity triage completed BEFORE full extraction
- [ ] Every populated variable has ≥ 1 evidence passage citation
- [ ] V1-V5 cross-validated against V6 for coherence
- [ ] No variable fabricated — null is acceptable, fabrication is not
- [ ] At minimum V1, V3, V5, V6 are populated (even for low-granularity coaches)
- [ ] `extraction_status` accurately reflects confidence level
- [ ] CSIP v3 extensions: Emotion Residency Time populated per register
- [ ] CSIP v3 extensions: Ceiling/Floor populated per topic cluster
- [ ] CSIP v3 extensions: Suppression patterns logged with compression artifacts
- [ ] CSIP v3 extensions: Resolution pattern classified with dominant type
- [ ] CSIP v3 extensions: Bleed signatures identified with construction markers

### CHECKPOINT

- Update `config.yaml`: `sessions.setup.emotional_dna.status = "complete"`
- Update `coach_soul.json`: `extraction_pipeline_status.emotional_dna_complete = true`
- Log: triage tier, variables populated, confidence score, corpus word count, sources used
