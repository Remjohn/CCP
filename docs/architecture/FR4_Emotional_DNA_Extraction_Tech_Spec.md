# Tech-Spec: FR4 — 10-Variable Emotional DNA Extraction

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §7.1 (JIT Skill Compiler Block A — Emotional DNA as pre-load), §5.3 (Genesis Pipeline — Stage 1), §12.3 (V5.0 Onboarding Prerequisites)
**Skill Implementation:** `skills/ccf/setup/emotional-dna-extraction/SKILL.md`

---

## Overview

### Problem Statement

Every dependency in the CCP — from Voice DNA (DEP-ENG-003/004) to CRAL research directives to Memetic Engine humor specifications — assumes the existence of a stable emotional identity map for the coach. Without this map, the system generates content from the LLM's default appraisal profile — what USC Institute for Creative Technologies research identifies as the **Powerless Observer Bias**: high agreeableness, high emotional competence, but low power, low life satisfaction, and low self-efficacy (USC ICT, Marsella & Gratch). The LLM cannot produce content that sounds like a human with deep conviction because its default "personality" has no convictions.

Emotional DNA is not what the coach believes. It is what the coach **cannot stop responding to** — the trigger architecture formed by their history, their violations, their experiences. This architecture is extractable because it is stable: Cognitive Appraisal Theory (Lazarus 1991, Scherer CPM 2001) demonstrates that an individual's appraisal sequence — which Stimulus Evaluation Check fires first, what threshold must be crossed to convert concern to outrage, whether they attribute agency to self or system — remains consistent across maximally different topics with test-retest reliability scores of 0.80–0.90 (SAM, Peacock & Wong 1990).

The 10-variable profile grounds this extraction in two validated psychometric frameworks: Cognitive Appraisal Theory (V1–V5) and Moral Foundations Theory with MFQ-2 instrumentation (V6–V10). Every variable requires a **corpus citation** (Mandate 7: Evidence-Grounded Variables) — no variable may be populated from inference, assumption, or statistical prior.

### Solution

A 6-phase forensic extraction pipeline (I-R-E-V-C protocol) that processes the coach's validated Sacred Audio corpus (≥3,000 authenticated words from FR2) into a 10-variable `emotional_dna.json` profile (DEP-LIB-001). The pipeline enforces granularity triage before extraction, cross-validates appraisal variables against moral foundation weights for coherence, and produces every variable with corpus-level citation evidence.

### Scope

**In scope:**
- 10-variable Emotional DNA profile extraction (V1–V10)
- Granularity triage (determines extraction depth)
- CSIP v3.0 extension variables (5 behavioral-level variables)
- Appraisal–MFT cross-validation (Constraint C)
- Corpus citation provenance for every populated variable (Mandate 7)
- Output to `emotional_dna.json` (DEP-LIB-001) + `coach_soul.json` integration
- LIWC-22 function word baseline extraction (used by downstream generation and authenticity gates)

**Out of scope:**
- Sacred Audio ingestion (FR2 Tech Spec — prerequisite, produces the corpus)
- Voice DNA extraction (FR3 Tech Spec — downstream consumer, uses DEP-LIB-001 in Step 3)
- Trigger Activation Event design (Stage 3 of the Trigger-First Engine — uses DEP-LIB-001 as input but is a separate pipeline)
- Content generation from Emotional DNA (downstream, uses DEP-LIB-001 + DEP-ENG-003/004 together)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-LIB-001` | Emotional DNA (10-Variable Profile) | PRIMARY OUTPUT — the full extraction product |
| `DEP-ENG-019` | Session Transcript Intelligence | INPUT — the validated Authentic Material Payload from FR2 |
| `DEP-ENG-003` | Positive Space (Voice DNA) | DOWNSTREAM CONSUMER — FR3 Step 3 reads DEP-LIB-001 for emotion residency and coping pattern |
| `DEP-ENG-004` | Negative Space | DOWNSTREAM CONSUMER — FR3 Step 7 uses Norm Compatibility Threshold to identify structural exclusions |
| `DEP-ENG-005` | Trigger Taxonomy | DOWNSTREAM CONSUMER — Stage 2 of the Trigger-First Engine maps intelligence signals against DEP-LIB-001 |
| `DEP-ENG-023` | Cultural Memory Map | CROSS-REFERENCE — CMM Layer 7 (Shared Enemy Typology) aligns with V6 Moral Foundations to predict tribal activation |

### Academic Research Grounding

| Variable Group | Framework | Key Papers | Lab Reference |
|---|---|---|---|
| V1–V5 | Cognitive Appraisal Theory | Lazarus (1991) *Emotion and Adaptation*; Scherer (2001) Component Process Model; Marsella & Gratch EMA Architecture | [Cognitive Appraisal Theory_ Emotional DNA.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/emotional%20DNA/Cognitive%20Appraisal%20Theory_%20Emotional%20DNA.md) |
| V6–V10 | Moral Foundations Theory (MFQ-2) | Haidt (2012) *The Righteous Mind*; Graham et al. (2013) MFQ Validation; Atari et al. (2023) MFQ-2 | [Moral Foundations Theory for Trigger Prediction.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Moral%20Foundations%20Theory%20for%20Trigger%20Prediction.md) |
| Extraction pipeline | Trigger-First Engine Architecture | CCP CCF Architecture v3.0, Stage 1 | [Trigger_First_Engine_Documentation.docx.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Trigger_First_Engine_Documentation.docx.md) |
| LIWC-22 baseline | Computational Linguistics | Pennebaker (2022) LIWC-22 Function Word Analysis | [Emotion, Discourse, and Language Production.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/emotional%20DNA/Emotion%2C%20Discourse%2C%20and%20Language%20Production.md) |
| Granularity triage | Constructionist Emotion Theory | Barrett (2017) Emotional Granularity and Affect Labeling | [Emotional Granularity and Affective Signatures.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/emotional%20DNA/Emotional%20Granularity%20and%20Affective%20Signatures.md) |
| Corpus validation | Computational Stylometry | Authorship attribution — minimum 3,000 word threshold | [Computational Stylometry for Authorship Attribution.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/emotional%20DNA/Computational%20Stylometry%20for%20Authorship%20Attribution.md) |
| LLM bias compensation | Affective Computing | USC ICT — LLM Powerless Observer Profile (Marsella, Gratch) | [Cognitive Appraisal Theory_ Emotional DNA.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/emotional%20DNA/Cognitive%20Appraisal%20Theory_%20Emotional%20DNA.md) (§LLM Emotional Reasoning) |

### Key Files

| File | Purpose |
|---|---|
| `skills/ccf/setup/emotional-dna-extraction/SKILL.md` | Existing skill definition — I-R-E-V-C protocol, extraction phases, constraints |
| `intelligence_library/emotional_dna.json` | Primary output target |
| `intelligence_library/coach_soul.json` | Secondary integration point — `extraction_pipeline_status.emotional_dna_complete` |
| `config.yaml` | Session status tracking — `sessions.setup.emotional_dna.status` |
| `raw/transcripts/` | Source corpus directory (interview transcripts, podcast transcripts, Sacred Audio transcriptions) |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Granularity triage before extraction** | Barrett (2017): individuals differ dramatically in emotional specificity. A low-granularity coach (< 12 distinct emotional terms) cannot reliably populate all 10 variables. Forcing extraction from insufficient material produces fabricated variables — worse than null. |
| **Mandate 7 (corpus citation provenance)** | Every variable must trace to a specific passage. This prevents the LLM extraction agent from filling variables with its own priors (the exact failure mode USC ICT documents as "machine personality"). |
| **Appraisal–MFT cross-validation (Constraint C)** | A coach with high Care/Harm and system-level agency attribution should show low trigger specificity threshold for institutional violations. Incoherence between V1–V5 and V6–V10 is an extraction error, not a personality type. |
| **V6–V10 as individual weights, not a single block** | FR4 definition and the MFQ-2 instrument both treat each foundation as an independently weighted receptor. Collapsing them into a single "moral profile" loses the predictive specificity needed by the Trigger-First Engine Stage 2. |
| **CSIP v3 extensions as behavioral overlay** | The 5 CSIP v3 variables (Emotion Residency, Ceiling, Floor, Suppression, Resolution, Bleed) are behaviorally granular — they describe how the coach *processes* emotions, not which emotions fire. This level is needed for Voice DNA rhythm and CCSB compilation fidelity. |

---

## Implementation Plan

### Prerequisite Gate

**Condition:** `coach_soul.json → extraction_readiness.authenticated_word_count ≥ 3000`

The FR2 pipeline has already validated and stored ≥3,000 authenticated words via LIWC-22 authenticity gate. This pipeline reads FROM that validated corpus — it never touches raw audio.

If not met → pipeline halts. Morgan queues Sacred Audio session requests.

---

### Phase 1: INGEST

**Agent:** Emotional DNA Extraction Agent (operating in forensic extraction mode — Mandate 1, no role-character assignment)
**Pi Extensions:** `SoulResonance`, `EmotionalDNA`

**Steps:**
1. Load `coach_soul.json` — read existing coach identity data and extraction pipeline status
2. Scan `raw/transcripts/` — inventory all available transcripts (interview, podcast, Sacred Audio transcriptions)
3. Count total word count across all available transcripts
4. **Gate:** If total word count < 3,000 → STOP. Report: *"Insufficient corpus. Need {3000 - current} more words. Sources: additional interview transcripts, podcast appearances, long-form social media posts."*
5. Load `emotional_dna.json` template with all 10 variable slots set to null
6. **Receipt Write (Phase 1):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-EDNA-INGEST",
  "previous_receipt_hash": "{FR2_FINAL_RECEIPT_HASH}",
  "input_payload_hash": "{RAW_TRANSCRIPT_DIR_HASH}",
  "output_payload_hash": "{NULL_TEMPLATE_HASH}",
  "stage_name": "EDNA-INGEST",
  "agent_name": "Emotional DNA Extraction Agent",
  "timestamp": "{ISO8601}" }
```

---

### Phase 2: REASON — Granularity Triage (MUST execute before full extraction)

> **This phase determines extraction depth. V7 equivalent — Barrett Constructionism (2017).**

**Action:** Scan full corpus for distinct emotional terms — words describing internal states, not external situations.

| Tier | Distinct Terms | Extraction Depth | Expected Corpus |
|---|---|---|---|
| **HIGH** | ≥ 25 | Full extraction viable (V1–V10 + all CSIP v3) | 2–4 hours transcript |
| **MEDIUM** | 12–24 | Standard extraction (V1–V10; CSIP v3 may be partial) | 4–8 hours transcript |
| **LOW** | < 12 | Surface extraction (V1, V3, V5, V6–V10 only; V2, V4 may not be extractable) | Flag for enhanced interview |

Record triage result in `emotional_dna.json → extraction_status.triage_tier`. This gate is non-negotiable — extraction below triage depth produces fabricated variables.

---

### Phase 3: REASON — Core Variable Extraction

#### Variables V1–V5: Cognitive Appraisal Architecture (Lazarus/Scherer)

**V1 — Trigger Specificity Threshold** (Scale: 1–10)

*Scherer CPM: Goal Relevance SEC + Novelty Check*

How specific must a stimulus be to activate an emotional response in this coach?

| Score Range | Behavior | Corpus Signal |
|---|---|---|
| 1–3 (low threshold) | Activates on generic stimuli ("the economy is bad") | Broad triggers, frequent activation passages, many topics produce emotion |
| 4–6 (medium) | Requires domain-specific stimulus ("advisor fee structures") | Activation limited to known domains |
| 7–10 (high threshold) | Requires precise mechanism stimulus ("the specific clause in the 2019 regulation") | Rare activation, but intense when triggered; very specific naming |

**Extraction method:** Identify all corpus passages where the coach transitions from analytical/calm to emotionally activated. For each: measure the specificity of the activating stimulus. Calculate median specificity across passages.

**Citation requirement (Mandate 7):** Minimum 3 passages with labeled specificity level.

---

**V2 — Appraisal Sequence Ordering** (Categorical)

*Scherer CPM: SEC cascade ordering — which check fires first*

What is the coach's default processing sequence when encountering an emotional trigger?

| Type | First Check | Corpus Pattern |
|---|---|---|
| `mechanism_first` | Implication checks | Coach explains the HOW before the JUDGMENT |
| `moral_verdict_first` | Norm checks | Coach declares the WRONG before the EVIDENCE |
| `narrative_first` | Relevance checks via story | Coach tells the STORY before the PRINCIPLE |
| `coping_first` | Coping checks | Coach jumps to the SOLUTION before the DIAGNOSIS |

**Extraction method:** Find 5+ extended passages (≥200 words) where the coach is processing an emotional topic. For each passage, label the first evaluative move. Calculate the dominant pattern. If no clear dominant pattern (distributed across types): record as `mixed` with percentage breakdown.

**Citation requirement:** Minimum 5 passages with ordered first-move labels.

---

**V3 — Coping Potential Pattern** (Numeric ratio: 0.0–1.0)

*Lazarus: Secondary Appraisal — controllability assessment; EMA: coping strategy selection*

Does the coach's content naturally orient toward action (problem-focused coping) or reflection (emotion-focused coping)?

**Extraction method:** Classify all corpus passages where the coach responds to a described problem:
- **Action statements:** "here's what I tell my clients to DO" / "the solution is to..." / imperative verbs
- **Reflective statements:** "here's what I've OBSERVED about this" / "what this reveals is..." / analytical framing

**Score:** `action_count / (action_count + reflective_count)`
- 0.0–0.3 = highly reflective coach
- 0.4–0.6 = balanced
- 0.7–1.0 = highly action-oriented coach

**Citation requirement:** Minimum 5 action-classified + 5 reflective-classified passages.

---

**V4 — Norm Compatibility Threshold** (Scale: 1–10)

*Scherer CPM: Internal Standards SEC; Lazarus: Type of Ego-Involvement*

What level of moral violation must occur to shift the coach from intellectual concern to activated outrage?

| Score Range | Behavior | Corpus Signal |
|---|---|---|
| 1–3 (low threshold) | Shifts easily, frequent outrage passages | Many topics trigger moral language, high virtue/vice density |
| 4–6 (medium) | Shifts on clear violations | Outrage reserved for specific categories of violation |
| 7–10 (high threshold) | Maintains analytical distance | Rare outrage, but extreme intensity when triggered; long buildup before shift |

**Extraction method:** Identify all passages containing moral language (virtue/vice terms, should/must statements, explicit judgment). For each: rate the severity of the triggering violation (from minor norm bend to fundamental institutional betrayal). Map the coach's activation point — where concern becomes outrage.

**Citation requirement:** Minimum 3 outrage passages + 3 analytical-distance passages on comparable topics.

---

**V5 — Agency Attribution Bias** (Categorical + dominant direction)

*EMA: Causal Attribution — back-tracing to identify responsible agent*

When describing problems, who does this coach assign responsibility to?

| Type | Corpus Pattern | Downstream Impact |
|---|---|---|
| `self` | "People need to take responsibility" / "You chose this" | Generation leans into personal accountability framing |
| `individual` | "These specific leaders/practitioners failed" / named agents | Generation targets specific actors |
| `institutional` | "The system is designed to..." / named organizations | Generation targets structures |
| `systemic` | "The fundamental architecture of..." / no single agent | Generation operates at paradigm level |

**Extraction method:** Classify all passages where the coach attributes blame or credit. Count per category. Dominant = highest count. Record secondary if ≥25% of total.

**Citation requirement:** Minimum 5 attribution passages across ≥2 categories.

---

#### Variables V6–V10: Moral Foundations Weighting (Haidt MFQ-2)

Each variable represents one moral taste receptor weighted via MFQ-2 psychometric analysis applied to the corpus. Weight = foundation keyword frequency / total moral keyword frequency. Range: 0.0–1.0 per foundation. Sum across V6–V10 = 1.0.

**V6 — Care/Harm Weight**

| Keyword Indicators | Authentic Activation Signal |
|---|---|
| suffering, compassion, cruelty, protect, vulnerable, help, harm, gentle, kind, nurture | Coach activates when perceiving distress, neglect, or cruelty toward individuals or vulnerable groups |

---

**V7 — Fairness/Cheating Weight**

| Keyword Indicators | Authentic Activation Signal |
|---|---|
| justice, rights, unfair, cheat, proportional, deserve, equality, merit, free-rider, reciprocity | Coach activates when perceiving unearned reward or unpunished exploitation |

**MFQ-2 distinction (critical for predictive accuracy):** Does this coach's fairness fire on **Equality** (everyone receives the same) or **Proportionality** (rewards match contributions)? Record the sub-type.

---

**V8 — Loyalty/Betrayal Weight**

| Keyword Indicators | Authentic Activation Signal |
|---|---|
| team, betray, loyal, sacrifice, traitor, solidarity, abandonment, fidelity, in-group, tribe | Coach activates when perceiving institutional betrayal, abandonment, or traitors within the in-group |

---

**V9 — Authority/Subversion Weight**

| Keyword Indicators | Authentic Activation Signal |
|---|---|
| tradition, respect, order, chaos, rebel, discipline, hierarchy, deference, legitimate, structure | Coach activates when perceiving subversion of legitimate authority or disrespect for earned position |

---

**V10 — Sanctity-Degradation & Liberty-Oppression Combined Weight**

> **Note:** The MFQ-2 identifies 6 foundations, but the FR4 definition specifies 10 total variables (V1–V5 + V6–V10). V10 combines the remaining two foundations as a paired weight:

**V10a — Sanctity/Degradation:**

| Keyword Indicators | Authentic Activation Signal |
|---|---|
| purity, disgust, sacred, degradation, wholeness, contaminate, toxic, clean, noble | Coach activates when perceiving degradation, pollution, or violation of what they consider sacred |

**V10b — Liberty/Oppression:**

| Keyword Indicators | Authentic Activation Signal |
|---|---|
| freedom, oppression, tyranny, control, bully, coerce, autonomy, constraint, reactance | Coach activates when perceiving constraint on autonomy or institutional overreach |

Record both sub-weights. The dominant one predicts the coach's primary political-level activation pattern (Iyer et al. 2012).

---

#### MFQ-2 Extraction Method (V6–V10)

1. Apply Moral Foundations Dictionary 2.0 (eMFD extended) keyword lists to the full corpus
2. For each foundation: count keyword occurrences, adjust for corpus length
3. Calculate weight: `foundation_keyword_frequency / total_moral_keyword_frequency`
4. Record Primary Foundation (highest weight) and Secondary Foundation (second highest)
5. Record cluster alignment: Individualizing (Care + Fairness + Liberty) vs Binding (Loyalty + Authority + Sanctity) — this predicts blind spots
6. **ME2-BERT cross-validation (when available):** Run ME2-BERT (events + emotions fine-tuned model) on corpus to validate keyword-based weights. If ME2-BERT and keyword analysis diverge by >15% on any foundation, flag for manual review.

**Citation requirement (Mandate 7):** For Primary and Secondary foundations — minimum 3 passages each demonstrating activation at that foundation.

---

### Phase 4: REASON — CSIP v3.0 Extension Variables

> These 5 behavioral-level variables populate `emotional_dna.json → csip_v3_extensions`. They describe HOW the coach processes emotions — distinct from V1–V10 which describe WHICH emotions fire.

**EXT-1: Emotion Residency Time** (per emotional register)

For each primary register (disgust, outrage, grief, tenderness, conviction, urgency):
- **SHORT:** Rapid mechanism delivery (< 2 sentences of emotion before pivot to explanation)
- **MEDIUM:** Blended dwell (3–5 sentences before conversion)
- **LONG:** Narrative buildup (6+ sentences of emotion explored before mechanism or verdict)

This controls rhythm profile more than any other single factor. A coach with LONG residency in grief and SHORT in conviction produces a fundamentally different content signature than the reverse.

---

**EXT-2: Emotional Ceiling Per Topic** (per topic cluster)

Scan corpus by topic cluster. For each: what is the maximum TTT this coach reaches? Record the construction signature at that ceiling (sentence length, clause depth, marker behavior). Topics the coach never gets hot about define content architecture constraints — the system will never assign high-temperature archetypes to cold topics.

---

**EXT-3: Emotional Floor Per Topic** (per topic cluster)

For each topic cluster: what is the minimum TTT regardless of prompt? Some coaches never drop below TTT-04 on specific subjects. This defines the lower priming boundary for generation.

---

**EXT-4: Suppression Patterns** (per register)

Search for compression artifacts: sudden brevity in otherwise long-form passages, topic pivots that redirect away from an emotional register, unanswered rhetorical questions signaling self-censorship. This is NOT Negative Space (what the coach refuses to say). This is what they FEEL but minimize publicly. For each suppressed register: record the emotion, the compression artifact, and the triggering context.

---

**EXT-5: Resolution Pattern + Emotional Bleed Signature**

**Resolution Pattern:** Classify the last 2–3 sentences of each thought unit:
- `resolves` — wraps emotion up with a bow (tied ending)
- `leaves_open` — deposits the emotion and walks away
- `converts` — transforms emotion into an action directive

Record dominant pattern + per-register overrides.

**Emotional Bleed Signature:** Search for moments where two emotional registers co-occur and leak into each other:
- Grief → Anger: *"I'm heartbroken that — no, I'm FURIOUS that..."*
- Passion → Urgency: *"I love this work and that's EXACTLY WHY you need to..."*

These blends are among the most distinctive Voice DNA markers. Record: primary emotion, bleeds_into, trigger context, construction marker that makes the bleed visible.

---

### Phase 5: EMIT — Write Output

**Agent:** Emotional DNA Extraction Agent

Write populated `emotional_dna.json` to `intelligence_library/emotional_dna.json`:

```json
{
  "dep_id": "DEP-LIB-001",
  "version": "1.0",
  "extraction_status": {
    "triage_tier": "HIGH|MEDIUM|LOW",
    "confidence": 0.0,
    "populated_variables": 0,
    "total_variables": 10,
    "csip_v3_populated": 0,
    "csip_v3_total": 5,
    "last_extracted": "ISO8601",
    "corpus_word_count": 0,
    "sources_used": []
  },
  "appraisal_variables": {
    "V1_trigger_specificity_threshold": {
      "score": null,
      "scale": "1-10",
      "evidence_passages": []
    },
    "V2_appraisal_sequence_ordering": {
      "type": null,
      "options": ["mechanism_first", "moral_verdict_first", "narrative_first", "coping_first", "mixed"],
      "percentage_breakdown": {},
      "evidence_passages": []
    },
    "V3_coping_potential_pattern": {
      "ratio": null,
      "scale": "0.0-1.0 (action/total)",
      "action_count": 0,
      "reflective_count": 0,
      "evidence_passages": []
    },
    "V4_norm_compatibility_threshold": {
      "score": null,
      "scale": "1-10",
      "evidence_passages": []
    },
    "V5_agency_attribution_bias": {
      "dominant": null,
      "secondary": null,
      "options": ["self", "individual", "institutional", "systemic"],
      "distribution": {},
      "evidence_passages": []
    }
  },
  "moral_foundations": {
    "V6_care_harm": {"weight": null, "evidence_passages": []},
    "V7_fairness_cheating": {
      "weight": null,
      "sub_type": "equality|proportionality",
      "evidence_passages": []
    },
    "V8_loyalty_betrayal": {"weight": null, "evidence_passages": []},
    "V9_authority_subversion": {"weight": null, "evidence_passages": []},
    "V10_sanctity_degradation": {"weight": null, "evidence_passages": []},
    "V10b_liberty_oppression": {"weight": null, "evidence_passages": []},
    "primary_foundation": null,
    "secondary_foundation": null,
    "cluster_alignment": "individualizing|binding|balanced"
  },
  "csip_v3_extensions": {
    "emotion_residency_time": {},
    "emotional_ceiling_per_topic": {},
    "emotional_floor_per_topic": {},
    "suppression_patterns": [],
    "resolution_pattern": {
      "dominant": null,
      "per_register_overrides": {}
    },
    "emotional_bleed_signatures": []
  }
}
```

**Confidence calculation:** `populated_variables / total_variables` (where "populated" = non-null + has ≥1 evidence passage)

---

### Phase 6: VALIDATE — Cross-Validation & Coherence Checks

**Constraint A — Provenance:** Every non-null variable has ≥1 corpus evidence passage. Any variable without a citation is forced to null.

**Constraint B — Triage Respected:** No variable populated beyond the triage tier's extraction depth ceiling.

**Constraint C — Appraisal–MFT Cross-Validation:**

| If V6–V10 shows... | Then V1–V5 should show... | Incoherence Signal |
|---|---|---|
| High Care/Harm (V6) + system agency (V5) | Low trigger specificity (V1) for institutional violations | If V1 is 7+ for institutional triggers → extraction error |
| High Liberty/Oppression (V10b) | "institutional" or "systemic" agency (V5) | If V5 is "self" → extraction error |
| High Loyalty/Betrayal (V8) | Low Norm Compatibility Threshold (V4) for betrayal events | If V4 is 7+ for betrayal events → extraction error |
| High Sanctity/Degradation (V10a) | "moral_verdict_first" appraisal sequence (V2) | If V2 is "coping_first" → review needed |

On any incoherence: flag for operator review with the conflicting variables and evidence passages. Do NOT auto-correct — the human decides.

**Constraint D — No Fabrication:** Any variable that cannot be supported by corpus evidence stays null. A partial profile with high confidence is infinitely more valuable than a complete profile with low confidence.

**Receipt Write (Phase 6):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-EDNA-VALIDATE",
  "previous_receipt_hash": "{PHASE_1_RECEIPT_HASH}",
  "input_payload_hash": "{EXTRACTED_VARIABLES_HASH}",
  "output_payload_hash": "{VALIDATED_EDNA_OUTPUT_HASH}",
  "stage_name": "EDNA-VALIDATION-COMPLETE",
  "agent_name": "Emotional DNA Extraction Agent",
  "timestamp": "{ISO8601}" }
```

---

### Phase 7: CHECKPOINT — Integration

1. Write `emotional_dna.json` to `intelligence_library/`
2. Update `coach_soul.json`: `extraction_pipeline_status.emotional_dna_complete = true`
3. Update `config.yaml`: `sessions.setup.emotional_dna.status = "complete"`
4. Log: triage tier, variables populated, confidence score, corpus word count, sources used
5. Trigger FR3 readiness check — if FR2 corpus threshold (≥3,000 words) is met AND DEP-LIB-001 is complete, FR3 Voice DNA pipeline can proceed (FR3 Step 3 reads DEP-LIB-001 for Cognitive Appraisal Variables)

---

## Tasks

- [ ] **Task 1:** Implement INGEST phase — corpus loading, word count gate, template initialization
- [ ] **Task 2:** Implement Granularity Triage — emotional term inventory, tier classification, extraction depth gating
- [ ] **Task 3:** Implement V1 (Trigger Specificity) — passage identification, activation-point scoring, median calculation
- [ ] **Task 4:** Implement V2 (Appraisal Sequence) — extended passage analysis, first-move labeling, dominant pattern calculation
- [ ] **Task 5:** Implement V3 (Coping Potential) — action/reflective classification, ratio scoring
- [ ] **Task 6:** Implement V4 (Norm Compatibility) — moral language detection, violation severity mapping, activation-point identification
- [ ] **Task 7:** Implement V5 (Agency Attribution) — blame/credit passage classification, category distribution
- [ ] **Task 8:** Implement V6–V10 (MFQ-2 Moral Foundations) — keyword dictionary application, frequency weighting, Equality/Proportionality sub-typing for V7
- [ ] **Task 9:** Implement CSIP v3 Extension extraction (EXT-1 through EXT-5) — residency time, ceiling/floor, suppression, resolution, bleed
- [ ] **Task 10:** Implement Constraint C cross-validation logic (appraisal ↔ MFT coherence checks with incoherence flagging)
- [ ] **Task 11:** Implement `emotional_dna.json` EMIT with evidence passage serialization + confidence calculation
- [ ] **Task 12:** Implement CHECKPOINT integration — coach_soul.json update, config.yaml status, FR3 readiness trigger
- [ ] **Task 13:** Integrate Receipt Chain Guard at INGEST + VALIDATE phases

---

## Acceptance Criteria

- [ ] **AC1 (Gate):** Pipeline does not start when corpus < 3,000 words. At exactly 3,000 words, pipeline starts.
- [ ] **AC2 (Triage):** A synthetic corpus with only 8 distinct emotional terms → triage tier = LOW. V2 and V4 are NOT extracted (remain null). V1, V3, V5, V6–V10 ARE extracted.
- [ ] **AC3 (Mandate 7 — provenance):** Every populated variable in the output `emotional_dna.json` has a non-empty `evidence_passages` array with ≥1 specific corpus passage. A variable populated without evidence is rejected and forced to null by validation.
- [ ] **AC4 (Constraint C — cross-validation):** A synthetic corpus where V6 (Care/Harm) = 0.45 (highest) AND V5 = "self" (self-agency attribution) → cross-validation flags incoherence. Operator review is triggered. Variables are NOT auto-corrected.
- [ ] **AC5 (No fabrication):** A synthetic corpus with no moral language whatsoever → V6–V10 all remain null. Confidence score reflects 0/5 for moral foundations. Profile is accepted as valid (partial).
- [ ] **AC6 (V2 classification):** A synthetic corpus with 10 extended passages: 7 mechanism_first, 2 narrative_first, 1 coping_first → V2 = `mechanism_first` (dominant), evidence cites all 10 passages with labels.
- [ ] **AC7 (V7 sub-typing):** A synthetic corpus where fairness activation fires on "unearned privilege" (equality-type) → V7 records `sub_type: equality`. A separate corpus where fairness fires on "lazy people getting rewarded" (proportionality-type) → V7 records `sub_type: proportionality`.
- [ ] **AC8 (CSIP v3 — bleed):** A corpus containing *"I'm heartbroken that — no, I'm FURIOUS that they..."* → EXT-5 records: `{primary: "grief", bleeds_into: "anger", marker: "dash-negation pivot"}`.
- [ ] **AC9 (Integration):** On extraction completion, `coach_soul.json → extraction_pipeline_status.emotional_dna_complete = true` is set. FR3 readiness check runs within the same execution cycle.
- [ ] **AC10 (Confidence):** A coach with 7/10 core variables populated + 4/5 CSIP v3 variables → confidence = 0.70 (core) and csip_confidence = 0.80. Both values stored in `extraction_status`.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR2 Sacred Audio pipeline | Internal prerequisite | Corpus ≥3,000 authenticated words |
| `coach_soul.json` | Internal | Must exist from `ccf-init` (Genesis Phase 0, Step 1) |
| LIWC-22 scoring dictionary | License | Used for function word baseline extraction |
| MFQ-2 / eMFD keyword dictionaries | Internal | Moral Foundations Dictionary 2.0 (extended) embedded in skill |
| ME2-BERT model (optional) | External | Cross-validation of keyword-based MFQ-2 weights — not required, enhances confidence |
| spaCy | Python package | POS tagging for keyword context disambiguation |
| Receipt Chain Guard | Infrastructure | Receipts at INGEST + VALIDATE phases |

---

## Testing Strategy

### Unit Tests
- Granularity triage: 3 synthetic corpora (HIGH: 30 emotional terms, MEDIUM: 18, LOW: 8) → validate tier classification
- V1–V5 extraction: 5 synthetic coaching transcripts with pre-coded appraisal patterns → validate variable scoring
- V6–V10 extraction: 5 synthetic transcripts with known moral foundation keywords (controlled density) → validate weight calculation
- Cross-validation (Constraint C): 4 incoherent variable combinations → validate flagging

### Integration Tests
- Full pipeline on a real 4,000-word coaching transcript → validate all 10 core variables + CSIP v3 extensions are populated with evidence passages
- Provenance check: scan output JSON → every non-null variable has ≥1 evidence passage containing actual corpus text

### Regression Tests
- Re-run extraction on the same corpus twice → validate identical output (deterministic extraction)
- Add 1,000 new words to corpus → re-run → validate that previously-extracted variables remain stable (appraisal signatures are stable per Lazarus/Scherer — re-extraction should not produce >10% drift on any variable)
