# Tech-Spec: FR10 — Four-Axis Structural Matching Engine & Activation Event Seed Construction

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.1)
**Architecture Reference:** §Context_Premise_Trigger_Matching_Layer Part 4, §Trigger-First Engine Architecture v3.0 Part 2, §5.4 (Weekly Pipeline — Stage 3 Structural Match + Stage 4 Seed Construction)
**Skill Implementation:** `skills/ccf/production/trigger-matching-engine/SKILL.md`

---

## Overview

### Problem Statement

The CCP has two extraction systems running in parallel. On the coach side: FR4 (Emotional DNA, DEP-LIB-001) maps the 10-variable appraisal and moral foundation architecture, and FR5 (Trigger Map, DEP-LIB-002) maps the permanent trigger architecture — Conway AKB origin, PTG resolution status, sensory anchors, reconsolidation sensitivity. On the audience side: FR6 (DEP-ENG-006) builds the standing Context Premise Map, and FR9 (Audience Empathy Agent) generates theme-specific Context Premises with 6 segments × 12 psychological categories depth-stratified across L1/L2/L3.

Both systems are highly sophisticated. Both produce authenticated, provenance-verified intelligence. And without a bridge between them, the coach produces authentic content that lands in the wrong room. The audience receives relevant content that carries no structural recognition signal. Neural comprehension without neural coupling (Hasson 2005).

The bridge is the Four-Axis Structural Matching Engine. It does not search for thematic similarity between coach triggers and audience pain — thematic matches produce content with heat but not resonance (Context_Premise_Trigger_Matching_Layer §Part 4 Component 1). It searches for **structural congruence** across four specific axes simultaneously: the same moral foundation violated, the same coping mechanism pattern, the same agency attribution target, and the correct temporal position (audience pre-PTG, coach post-PTG). All four must align. One-axis or two-axis matches are explicitly labeled **adjacent, not congruent** — they are returned to the engine for resolution, not passed downstream.

When a four-axis match is confirmed, the engine synthesizes it into an **Activation Event Seed** — a specific invocation event built from three elements: the coach's Event-Specific Knowledge (ESK) anchor from their AKB hierarchy, the audience's L3 tribal language, and the structural congruence point that makes both positions the same map coordinates. This seed, expressed in DARN-CAT evocative question architecture (Miller & Rollnick), activates the coach's dual-layer encoding (Tedeschi & Calhoun PTG) — the original formative experience running simultaneously with the resolution path — producing content that carries biological authenticity, not constructed empathy.

### Solution

A 6-phase engine operating as Stage 3 + Stage 4 of the Weekly Pipeline:

1. **INGEST** — Load coach-side intelligence (DEP-LIB-001 + DEP-LIB-002) and audience-side intelligence (FR9 theme-specific Context Premise)
2. **L3 EXTRACT** — Extract L3 structural coordinates from the theme-specific Context Premise: moral foundation violations, coping mechanism patterns, agency attribution patterns, hidden beliefs in tribal language, emotional triggers array
3. **FOUR-AXIS MATCH** — For each coach trigger × each audience L3 coordinate, evaluate congruence across all four axes simultaneously
4. **SEED CONSTRUCT** — For confirmed four-axis matches, build Activation Event Seeds from ESK anchor + L3 tribal language + structural congruence point
5. **FAILURE GATE** — Apply the Three Failure Prevention Gates (Adjacent vs. Congruent, Language Drift Prevention, Authenticity Score Feedback Loop)
6. **EMIT** — Output ranked match results and constructed seeds ready for Telegram Elicitation Protocol

**Output artifacts:**
- `intelligence/matching/{theme_slug}_match_results.json` — all evaluated matches with axis-by-axis scores
- `intelligence/matching/{theme_slug}_activation_seeds.json` — constructed Activation Event Seeds for confirmed four-axis matches

### Scope

**In scope:**
- Four-Axis Structural Matching Engine (Moral Foundation, Coping Potential, Agency Attribution, Temporal Position)
- L3 structural coordinate extraction from FR9 output
- Adjacent match detection and return for resolution
- Match ranking by structural congruence depth
- Acceptance criteria and testing strategy

**Out of scope:**
- Activation Event Seed construction (owned by FR11).
- Three Failure Prevention Gates (owned by FR12).
- This spec terminates at match scoring and DEP-ENG-010 emission.
- Emotional DNA extraction (FR4 — upstream producer)
- Trigger Map building (FR5 — upstream producer)
- Audience Empathy Agent operation (FR9 — upstream producer)
- Coach activation via Telegram Elicitation Protocol (downstream consumer)
- TTT resolution (FR8 — runtime value via DEP-ENG-005, independent of matching)
- Content generation from activated voice notes (downstream multi-agent SoC)
- Archetype selection from authenticated emotional state (downstream, post-activation)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-LIB-001` | Emotional DNA (10-Variable Profile) | INPUT — V3 Coping Potential Pattern, V4 Norm Compatibility Threshold, V5 Agency Attribution Bias, V6–V10 MFQ-2 Moral Foundation weights |
| `DEP-LIB-002` | Trigger Map | INPUT — Trigger entries with AKB origin (ESK/GE/LP), PTG status, sensory anchors, moral foundation mapping, reconsolidation sensitivity |
| `DEP-ENG-006` | Context Premise Map | INPUT (via FR9) — Standing 12+5 dimension graph ontology, enriched by FR9's per-theme extraction |
| `DEP-ENG-010` | Four-Axis Match Object | OUTPUT — Four-Axis Match Object. Consumed by FR11 (Activation Event Seed) and FR12 (Failure Prevention Gates). |
| `DEP-ENG-005` | Authentication Certificate | DOWNSTREAM — TTT resolved at production time from authenticated voice note, NOT from this engine |
| `DEP-ENG-023` | Cultural Memory Map | CROSS-REFERENCE — CMM Layer 7 (Shared Enemy Typology) provides supplementary enemy-axis data |

### Academic Research Grounding

| Component | Framework | Key Papers | Lab Reference |
|---|---|---|---|
| Four-Axis matching architecture | Clark & Brennan Common Ground Theory (1991) | Clark & Brennan (1991) *Grounding in Communication* — structural L3 ground demands alignment across appraisal architecture AND moral foundation simultaneously | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 4 |
| Dual-layer encoding / temporal position | Tedeschi & Calhoun Post-Traumatic Growth (2004) | Tedeschi & Calhoun (2004) — original encoding remains intact; secondary "path out" network superimposed. Dual-layer activation = content from both simultaneously. | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 3 Pillar 1 |
| Completion drive / meaning transmission | Frankl Logotherapy — Will to Meaning | Frankl (1946/2006) — DMN infra-slow oscillations require narrative arc completion. Coach's authentic conviction = biological compulsion when structural match is precise. | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 3 Pillar 2 |
| Seed construction — ESK anchor | Tulving Episodic/Semantic; Conway AKB Hierarchy; Nader Reconsolidation | Conway (2005) ESK = full appraisal cascade + sensory-perceptual records; Nader (2000) prediction error labilizes trace; Tulving autonoetic consciousness | [Memory Retrieval vs. Semantic Construction](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Memory%20Retrieval%20vs.%20Semantic%20Construction.md) |
| Seed construction — tribal language | Pennebaker LIWC-22 Authenticity | L3 tribal language carries sub-cortical recognition signal; translated/abstracted language drifts seed to L1 | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) |
| Activation event expression | Miller & Rollnick DARN-CAT (Motivational Interviewing) | Taking Steps dimension = behavioral specificity accessing ESK; Reasons dimension = surfaces moral foundation in coach's own language | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 4 Component 2 |
| Moral foundation matching | Haidt MFT / MFQ-2; eMFD | Atari et al. (2023) MFQ-2 — same foundation must be violated in both audience L3 pain and coach trigger origin | [Moral Foundations Theory for Trigger Prediction](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Moral%20Foundations%20Theory%20for%20Trigger%20Prediction.md) |
| Coping pattern matching | Lazarus & Folkman Transactional Model (1984) | Coping Potential Assessment pattern — audience's current coping mechanism must match coach's coping architecture during trigger formation | [Coping Trajectory Staging Framework](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Coping%20Trajectory%20Staging%20Framework.md) |
| Agency attribution matching | Scherer CPM — Causal Attribution SEC | Coach's V5 Agency Attribution Bias must align with audience's enemies field (who they blame) | [Audience Appraisal Profiling Framework](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Audience%20Appraisal%20Profiling%20Framework.md) |
| Authenticity feedback loop | LIWC-22 Authenticity Algorithm (Pennebaker) | Post-activation authenticity score diagnoses structural match quality — low score on confirmed match reveals either live trauma or L2 masquerading as L3 | [Audience Reconsolidation and Content Impact](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Audience%20Reconsolidation%20and%20Content%20Impact.md) |
| Neural coupling output | Hasson Neural Coupling Research (Princeton) | L3 structural ground + dual-layer activation produces DMN + anterior insula synchrony; credibility signal (Clark) is precondition for coupling (Hasson) | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 7 |

### Key Files

| File | Purpose |
|---|---|
| `skills/ccf/production/trigger-matching-engine/SKILL.md` | Engine skill definition |
| `intelligence_library/emotional_dna.json` | Coach Emotional DNA (DEP-LIB-001) — input |
| `intelligence_library/trigger_map.json` | Coach Trigger Map (DEP-LIB-002) — input |
| `intelligence/context_premises/{theme_slug}_context_premise.json` | FR9 theme-specific Context Premise — input |
| `intelligence/matching/{theme_slug}_match_results.json` | Match evaluation output |
| `intelligence/matching/{theme_slug}_activation_seeds.json` | Constructed Activation Event Seeds — output |
| `config.yaml` | Session state tracking |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **All four axes must align — no partial match passthrough** | One-axis or two-axis matches produce content with heat but not resonance. An audience blaming themselves (internal agency) matched with a coach whose trigger was built on blaming institutions (external agency) shares emotional intensity but not structural ground. The audience will feel inspired but not *recognized*. Adjacent matches are labeled and returned to the engine — never passed downstream. |
| **Structural congruence, not thematic similarity** | The engine does not search for topics that overlap. It searches for identical structural mapping: same moral violation, same coping mechanism, same agency attribution target, same temporal position. Two coaches discussing "financial shame" can produce different structural matches because their moral foundations, agency attributions, and coping patterns differ. |
| **ESK-level anchors required for seed construction** | Conway's AKB hierarchy demonstrates that only Event-Specific Knowledge contains the full appraisal cascade + sensory-perceptual records needed for episodic invocation. GE and LP triggers produce semantic synthesis — mask output. Seeds built from GE/LP anchors generate topic-based content, not structurally invoked content. |
| **Minimum 3 verified tribal terms in the seed** | Language Drift Prevention (Gate 2): when the seed is constructed from audience L3 tribal language but expressed using different language, the activation event loses the sub-cortical recognition signal. Any prompt a marketer outside the tribe could have written is a drifted prompt. |
| **Authenticity score as diagnostic feedback, not quality gate** | Gate 3 feeds back LIWC-22 authenticity scores as structural calibration data. A low score on a confirmed four-axis match reveals one of two diagnosable failure modes: (1) temporal position wrong — coach's trigger is live trauma, not resolved PTG; (2) L3 data was L2 masquerading as L3. Both are correctable before the next session. |
| **PTG status = hard prerequisite for temporal position axis** | A coach whose trigger is classified `raw_unresolved` (FR5 Phase 4) cannot participate in four-axis matching for that trigger. Dual-layer activation is not available — only the primary encoding is running. This is a safety gate, not a quality filter. |

---

## Implementation Plan

### Phase 1: INGEST — Dual-Side Intelligence Loading

**Steps:**

1. Receive content theme from weekly pipeline (same theme sent to FR9)
2. Load coach-side intelligence:
   - `emotional_dna.json` (DEP-LIB-001) — V3 Coping Potential Pattern, V5 Agency Attribution Bias, V6–V10 Moral Foundation weights
   - `trigger_map.json` (DEP-LIB-002) — all `triggers[]` entries (NOT `candidate_triggers[]`) with AKB origin, PTG status, sensory anchors, moral foundation mapping
3. Load audience-side intelligence:
   - `{theme_slug}_context_premise.json` (FR9 output) — 6 segments × 12 categories, L1/L2/L3 stratified, Four Laws validated
4. **PRE-FLIGHT GATES:**
   - Gate A: `emotional_dna.json` exists AND `extraction_status.confidence ≥ 0.5`. If missing → HALT: `EMOTIONAL_DNA_REQUIRED`.
   - Gate B: `trigger_map.json` exists AND `map_status.resolved_dual_layer_count ≥ 1`. If missing → HALT: `TRIGGER_MAP_REQUIRED`. If resolved count = 0 → HALT: `NO_RESOLVED_TRIGGERS`.
   - Gate C: FR9 output exists AND `four_laws_status.overall_status ≠ "FAILED"`. If missing → HALT: `CONTEXT_PREMISE_REQUIRED`. If FAILED → HALT: `CONTEXT_PREMISE_FAILED — depth insufficient for structural matching`.
   - Gate D: Filter coach triggers — EXCLUDE any trigger with `ptg_status = "raw_unresolved"`. Log exclusion.
5. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PHASE-1-INGEST',
  agent_name: 'Four-Axis-Matching-Engine',
  timestamp }

---

### Phase 2: L3 EXTRACT — Audience Structural Coordinate Extraction

From the FR9 theme-specific Context Premise, extract the L3 structural coordinates required by each matching axis:

| Axis | Required L3 Data | Source Fields in FR9 Output |
|---|---|---|
| Axis 1 — Moral Foundation | Which moral foundations are violated in the audience's L3 pain | `emotional_triggers[].moral_foundation` + `enemies` category (L3 entries) |
| Axis 2 — Coping Potential | Current coping mechanism pattern | `coping_mechanism[].agency_attribution_pattern` + `coping_mechanism[].coping_potential_assessment` (L3 entries) |
| Axis 3 — Agency Attribution | Who the audience blames | `enemies` category (L3 entries) + `suspicions` category (L3 entries) |
| Axis 4 — Temporal Position | Audience is currently inside the experience | `frustrations` + `hidden_beliefs` + `coping_mechanism` category (L3 entries) → infer pre-PTG/in-experience status |

**L3 filter:** Only L3-classified entries feed the matching engine. L1 and L2 entries are excluded at this phase. This is the structural enforcement of Law 2 from Context_Premise_Trigger_Matching_Layer §Part 2: "The Trigger Matching Layer operates exclusively on L3 data."

**Per-segment extraction:** Extract L3 structural coordinates independently for each of the 6 audience segments. Different segments may match different coach triggers — a segment in the SEARCH coping stage may match a different trigger than a segment in the EXHAUSTED stage.

**Output:** A structured set of L3 coordinate objects:

```json
{
  "segment_id": "string",
  "l3_coordinates": {
    "moral_foundations_violated": ["care_harm", "liberty_oppression"],
    "coping_mechanism_pattern": {
      "mechanism": "avoidance_distancing",
      "agency_attribution": "institutional",
      "coping_potential_assessment": "low"
    },
    "agency_attribution_target": "institutional",
    "temporal_position_evidence": {
      "currently_inside": true,
      "frustration_indicators": [],
      "hidden_belief_indicators": [],
      "search_phase_markers": []
    },
    "tribal_language_terms": []
  }
}
```

---

### Phase 3: FOUR-AXIS MATCH — Structural Congruence Evaluation

For each coach trigger (from `trigger_map.json → triggers[]`, excluding `raw_unresolved`) × each audience segment L3 coordinate set (from Phase 2), evaluate congruence across all four axes:

---

#### Axis 1 — Moral Foundation

**What is being matched:** The same moral foundation must be violated in both the audience's L3 pain and the coach's trigger origin.

| Data Source — Coach | Data Source — Audience |
|---|---|
| Trigger entry `moral_foundation` + DEP-LIB-001 V4 (Norm Compatibility Threshold) + V6–V10 (MFQ-2 weights) | Audience `emotional_triggers[].moral_foundation` + `enemies` field (L3 entries) |

**Scoring:**
- `EXACT` — Same foundation violated (e.g., both Care/Harm). Score = 1.0
- `ADJACENT` — Related foundation cluster (e.g., coach = Care/Harm, audience = Liberty/Oppression — both Individualizing cluster). Score = 0.5
- `NONE` — Different foundations, different clusters. Score = 0.0

**Failure mode if missed:** "Thematic similarity without moral congruence. Coach is fired up. Audience does not feel the coach has been in their specific moral territory."

---

#### Axis 2 — Coping Potential Pattern

**What is being matched:** The audience's current coping mechanism must match the coping architecture the coach was using when the trigger was forming — before the PTG path was developed.

| Data Source — Coach | Data Source — Audience |
|---|---|
| DEP-LIB-001 V3 (Coping Potential Assessment Pattern) — the coach's action/reflective ratio during trigger formation | Audience `coping_mechanism` field from Context Premise L3 segments — `agency_attribution_pattern` + `coping_potential_assessment` |

**Scoring:**
- `CONGRUENT` — Same coping architecture (e.g., both avoidance/emotion-focused, or both action/problem-focused). Score = 1.0
- `PARTIAL` — Similar but different intensity (e.g., coach was active-coping, audience is search-phase). Score = 0.5
- `NONE` — Opposite coping architectures. Score = 0.0

**Failure mode if missed:** "Coach has the answer but the audience's appraisal system doesn't recognize the question being answered. Credibility gap remains."

---

#### Axis 3 — Agency Attribution

**What is being matched:** The audience's enemies field (who they blame) must align with the coach's Agency Attribution Bias — who the coach was attributing agency to when the trigger was building.

| Data Source — Coach | Data Source — Audience |
|---|---|
| DEP-LIB-001 V5 (Agency Attribution Bias) — `self` / `individual` / `institutional` / `systemic` | Audience `enemies` field + `suspicions` field from Context Premise (L3 entries) |

**Scoring:**
- `CONGRUENT` — Same attribution target (e.g., both institutional). Score = 1.0
- `ADJACENT` — Related target (e.g., coach = institutional, audience = individual within institution). Score = 0.5
- `NONE` — Opposite targets (e.g., coach blames system, audience blames self). Score = 0.0

**Failure mode if missed:** "Coach content addresses the wrong agent. Audience is blaming institutions; coach is addressing personal failure. Signal is adjacent, not congruent."

---

#### Axis 4 — Temporal Position

**What is being matched:** The audience must currently be inside the experience the coach has already completed. Not the same theme — the same stage. Pre-PTG audience, post-PTG coach.

| Data Source — Coach | Data Source — Audience |
|---|---|
| Trigger entry `ptg_status` — MUST be `resolved_dual_layer` or `active_processing`. The "path out" must be encoded. | Audience `frustrations` + `hidden_beliefs` + `coping_mechanism` field (L3 entries) — evidence that the audience is currently navigating the experience, not looking back on it. |

**Scoring:**
- `CONGRUENT` — Coach post-PTG (`resolved_dual_layer`) AND audience currently inside (pre-PTG). Score = 1.0
- `PARTIAL` — Coach `active_processing` (partial resolution) AND audience currently inside. Score = 0.5. Flag: `emotional_load_monitor = true`
- `INVALID` — Coach `raw_unresolved` → excluded in Phase 1. Never reaches scoring.
- `NONE` — Both coach and audience are post-PTG (coach has completed, audience has completed). No structural need. Score = 0.0

**Failure mode if missed:** "Coach is still inside the experience — it is live trauma, not formative encoding. Dual-layer activation is not available. Content may be raw and real but lacks the resolution signal the audience's appraisal system is seeking."

---

#### Match Classification

| Total Score (sum of 4 axes) | Classification | Action |
|---|---|---|
| 4.0 (all EXACT/CONGRUENT) | **CONFIRMED — Four-Axis Congruent** | Proceed to Seed Construction (Phase 4) |
| 3.0–3.5 | **STRONG — Three axes congruent + one adjacent** | Proceed to Seed Construction with `strength: strong`. Flag adjacent axis for monitoring. |
| 2.0–2.5 | **ADJACENT — Two-axis match** | DO NOT construct seed. Return to engine. Log as adjacent match with axis-by-axis diagnostic. |
| < 2.0 | **NO MATCH** | Discard. Not structurally congruent. |

**Critical gate:** Two-axis matches are explicitly flagged as ADJACENT and returned. They are NOT passed downstream. "An audience blaming themselves and a coach whose trigger was built on blaming institutions share emotional intensity but not structural ground."

---

### Phase 4: Match Object Emission
Agent: Four-Axis-Matching-Engine
Input: Resolved axis scores from Phase 3
Output: DEP-ENG-010 (Four-Axis Match Object)
Failure Condition: Any axis score returns null or match_classification cannot be resolved
Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'MATCH-EMIT',
  agent_name: 'Four-Axis-Matching-Engine',
  timestamp }

Steps:
1. Serialize the four axis scores into DEP-ENG-010
2. Assign match_classification:
   CONFIRMED (sum = 4.0),
   STRONG (sum 3.0-3.9, no axis = 0.0),
   ADJACENT (any axis = 0.0 OR sum < 3.0)
3. Write DEP-ENG-010 to dependency layer
4. Emit DEP-ENG-010 to FR11 input queue
5. Write receipt

---

### Phase 6: EMIT — Output Generation

**Match Results Output:**

```json
{
  "theme": "content_theme_string",
  "generated_at": "ISO8601",
  "engine_version": "1.0",
  "inputs_used": {
    "emotional_dna_version": "",
    "trigger_map_version": "",
    "context_premise_version": ""
  },
  "triggers_evaluated": 0,
  "segments_evaluated": 6,
  "total_combinations_evaluated": 0,
  "matches": {
    "confirmed": [],
    "strong": [],
    "adjacent": [],
    "no_match": 0
  },
  "exclusions": {
    "raw_unresolved_triggers_excluded": [],
    "l1_l2_entries_filtered": 0
  }
}
```

**Activation Seeds Output:**

```json
{
  "theme": "content_theme_string",
  "generated_at": "ISO8601",
  "seeds": [
    {
      "seed_id": "",
      "match_classification": "",
      "match_score": 0.0,
      "axis_scores": {},
      "elements": {},
      "activation_event": {},
      "flags": {},
      "priority_rank": 0
    }
  ],
  },
  "exclusions": {
    "raw_unresolved_triggers_excluded": [],
    "l1_l2_entries_filtered": 0
  }
}
```

Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PHASE-6-EMIT',
  agent_name: 'Four-Axis-Matching-Engine',
  timestamp }

---

## The Complete Architectural Flow (Stages 1–9)

This engine occupies Stages 3–5 in the 9-stage architectural flow from Context_Premise_Trigger_Matching_Layer §Part 5. The full flow, showing this engine's position:

| Stage | System | Input | Output |
|---|---|---|---|
| 1 | **FR9 Audience Empathy Agent** | Raw audience research, soul values, tribe profile, content theme | Context Premise: 6 segments × 12 categories per theme. L1/L2/L3 stratified. |
| 2 | **THIS ENGINE — L3 Extraction** | Context Premise (full document) | L3 structural coordinates: moral foundation violations, coping mechanism patterns, agency attribution patterns, hidden beliefs in tribal language, emotional triggers array |
| 3 | FR4/FR5 Coach Emotional DNA + Trigger Map | Coach corpus, voice notes, interview transcripts | 10-variable Emotional DNA + standing Trigger Map with PTG status |
| 4 | **THIS ENGINE — Four-Axis Match** | L3 structural coordinates + Coach Emotional DNA + Trigger Map | Confirmed four-axis matches with structural congruence points identified. Adjacent matches flagged and returned. |
| 5 | **THIS ENGINE — Seed Construction** | Confirmed matches + coach ESK anchor + audience tribal language | Activation event seeds in DARN-CAT architecture |
| 6 | Telegram Elicitation Protocol | Activation event seed | Authentic voice note produced from dual-layer activation. LIWC-22 scoring applied. Score fed back to Gate 3. |
| 7 | Emotional State → Archetype Mapping | Authenticated voice note + emotional state | Content archetype selected. TTT resolved via DEP-ENG-005. |
| 8 | Deep Research Agent (CRAL) | Structural congruence point + coach's activated position | Evidence sharpening the specific mechanism at the intersection |
| 9 | Multi-Agent SoC | All upstream outputs | Content produced from the shared experiential substrate |

---

## Tasks

- [ ] **Task 1:** Implement Phase 1 INGEST — dual-side intelligence loading with 4 pre-flight gates (DEP-LIB-001 existence, DEP-LIB-002 resolved trigger count, FR9 authentication status, PTG raw_unresolved exclusion)
- [ ] **Task 2:** Implement Phase 2 L3 EXTRACT — L3 structural coordinate extraction from FR9 output for all 6 segments, filtering out L1/L2, extracting per-axis data fields (moral foundations from emotional triggers, coping patterns, agency from enemies/suspicions, temporal position from frustrations/hidden beliefs/coping)
- [ ] **Task 3:** Implement Axis 1 scoring — Moral Foundation matching between coach trigger `moral_foundation` + V6–V10 weights and audience `emotional_triggers[].moral_foundation` + `enemies` (EXACT / ADJACENT cluster / NONE)
- [ ] **Task 4:** Implement Axis 2 scoring — Coping Potential Pattern matching between coach V3 and audience `coping_mechanism[].agency_attribution_pattern` + `coping_potential_assessment` (CONGRUENT / PARTIAL / NONE)
- [ ] **Task 5:** Implement Axis 3 scoring — Agency Attribution matching between coach V5 and audience `enemies` + `suspicions` L3 entries (CONGRUENT / ADJACENT / NONE)
- [ ] **Task 6:** Implement Axis 4 scoring — Temporal Position matching between coach `ptg_status` and audience L3 evidence of currently-inside-experience status (CONGRUENT / PARTIAL / INVALID / NONE)
- [ ] **Task 7:** Implement match classification logic — total score computation, CONFIRMED (≥3.5) / STRONG (3.0–3.5) / ADJACENT (2.0–2.5) / NO MATCH (<2.0) bucketing with axis-by-axis diagnostic
- [ ] **Task 8:** Implement Phase 4 Seed Construction — ESK anchor extraction, L3 tribal language selection (minimum 3 terms), structural congruence point articulation, DARN-CAT question composition (Taking Steps + Reasons dimensions)
- [ ] **Task 9:** Implement Gate 1 — Adjacent vs. Congruent detection and return. Ensure ADJACENT matches never enter seed construction.
- [ ] **Task 10:** Implement Gate 2 — Language Drift Prevention. Tribal term count validation in activation event text (≥3 verified = pass, 1–2 = warning, 0 = reject + reconstruct).
- [ ] **Task 11:** Implement Gate 3 — Authenticity Score Feedback Loop. Receive LIWC-22 score post-voice-note, diagnose structural match quality, feed corrective actions back to FR5 (trigger precedence) and FR9 (Context Premise re-validation).
- [ ] **Task 12:** Implement Phase 6 EMIT — match results serialization, seed output with priority ranking (match score → ESK quality → tribal term count), receipt chain guard.
- [ ] **Task 13:** Implement match evaluation iteration — cross-product of all coach triggers × all audience segments with early termination for `raw_unresolved` and `FAILED` Context Premisess.

---

## Acceptance Criteria

- [ ] **AC1 (Prerequisite Gates):** Engine halts with descriptive error when: (a) DEP-LIB-001 missing → `EMOTIONAL_DNA_REQUIRED`, (b) DEP-LIB-002 missing → `TRIGGER_MAP_REQUIRED`, (c) FR9 output missing → `CONTEXT_PREMISE_REQUIRED`, (d) FR9 output FAILED → `CONTEXT_PREMISE_FAILED`.
- [ ] **AC2 (PTG Safety Gate):** A coach trigger with `ptg_status = "raw_unresolved"` is EXCLUDED from matching in Phase 1. It never reaches axis scoring. Exclusion is logged.
- [ ] **AC3 (L3-Only Matching):** Only L3-classified entries from FR9 output feed the matching engine. An FR9 output with 85% L1 entries → matching engine receives only the 15% L2+L3 entries. L1 entries are never used in axis scoring.
- [ ] **AC4 (Four-Axis All-or-Nothing):** A match scoring EXACT on Moral Foundation + Coping Potential + Agency Attribution but NONE on Temporal Position (total = 3.0 with one zero) → classified ADJACENT (not CONFIRMED). Seed construction does NOT proceed for this match.
- [ ] **AC5 (Adjacent Match Handling):** Two-axis matches (score 2.0–2.5) are classified ADJACENT with axis-by-axis diagnostic. They are NEVER passed to seed construction. They produce a diagnostic report, not a seed.
- [ ] **AC6 (Tribal Language Minimum):** An activation event seed with 0 verified tribal terms → REJECTED by Gate 2 (Language Drift). An event with 3+ terms → PASS. An event with 1–2 terms → WARNING flag set.
- [ ] **AC7 (ESK Anchor Quality):** A seed built from an ESK-level anchor (`origin.akb_level = "esk"`) → `anchor_quality: full`. A seed built from a General Event anchor → `anchor_quality: degraded`. Both are constructed but the degraded seed ranks lower in priority.
- [ ] **AC8 (DARN-CAT Expression):** Every activation event seed is expressed using Taking Steps (behavioral specificity) and/or Reasons (moral foundation surfacing) dimensions. A seed that reads like a generic topic question ("What do you think about financial shame?") → fails DARN-CAT validation.
- [ ] **AC9 (Authenticity Feedback — Failure Mode 1):** A confirmed four-axis match producing LIWC-22 authenticity < 5/10 across 2 consecutive sessions → triggers PTG re-assessment for the matched coach trigger. System diagnoses possible temporal position error.
- [ ] **AC10 (Authenticity Feedback — Failure Mode 2):** A confirmed four-axis match producing LIWC-22 authenticity < 5/10 → triggers FR9 Context Premise re-validation flag for the matched audience segments. System diagnoses possible L2-masquerading-as-L3.
- [ ] **AC11 (Match Ranking):** Multiple confirmed matches for the same theme are ranked by: (1) match score descending, (2) ESK anchor quality (full > degraded), (3) tribal term count. Top-ranked seed is sent to Telegram Elicitation Protocol first.
- [ ] **AC12 (Cross-Product Evaluation):** All combinations of coach triggers × audience segments are evaluated. For 5 coach triggers × 6 audience segments = 30 combinations, all 30 receive axis-by-axis scoring.
- [ ] **AC13 (Structural Congruence Point):** Every constructed seed contains a `structural_congruence_point` field that articulates the specific overlap — not the theme, but the exact coordinates where the audience's current experience and the coach's formative experience share the same map position.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR4 Emotional DNA (DEP-LIB-001) | Internal prerequisite | V3, V5, V6–V10 used for axis scoring |
| FR5 Trigger Map (DEP-LIB-002) | Internal prerequisite | Trigger entries with AKB origin, PTG status, sensory anchors, moral foundation |
| FR9 Audience Empathy Agent | Internal prerequisite | Theme-specific Context Premise with Four Laws validation |
| Telegram Elicitation Protocol | Downstream consumer | Receives activation event seeds |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Receipts at INGEST + EMIT |

---

## Testing Strategy

### Unit Tests
- **Axis 1 scoring:** Synthetic coach trigger (moral_foundation = "care_harm") + synthetic audience segment (emotional_triggers[0].moral_foundation = "care_harm") → score = 1.0 (EXACT). Same coach + audience (moral_foundation = "fairness_cheating") → score = 0.5 (ADJACENT — same Individualizing cluster). Same coach + audience (moral_foundation = "authority_subversion") → score = 0.0 (NONE — different cluster).
- **Axis 4 temporal position:** Synthetic coach trigger (ptg_status = "resolved_dual_layer") + synthetic audience segment (currently inside experience) → score = 1.0 (CONGRUENT). Coach trigger (ptg_status = "raw_unresolved") → excluded in Phase 1, never reaches scoring.
- **Match classification:** Synthetic evaluation with scores [1.0, 1.0, 1.0, 0.0] (total = 3.0 with one zero) → classified ADJACENT (has a zero axis). Scores [1.0, 1.0, 1.0, 0.5] (total = 3.5) → classified STRONG.
- **Tribal language validation:** Seed with 0 tribal terms → Gate 2 REJECT. Seed with 3 tribal terms → Gate 2 PASS.
- **DARN-CAT validation:** Seed question "What do you think about X?" → fails. Seed question "When you saw [specific tribal term] happening to [audience's enemy], what was the first thing you wanted to do?" → passes (Taking Steps + behavioral specificity).

### Integration Tests
- **Full pipeline:** Provide synthetic DEP-LIB-001 + DEP-LIB-002 + FR9 output → validate: all coach trigger × audience segment combinations evaluated, confirmed matches produce seeds, adjacent matches produce diagnostics, seeds contain ≥3 tribal terms, ESK anchor quality assessed.
- **Gate 3 feedback loop:** Simulate 2 consecutive low-authenticity sessions on a confirmed match → validate: PTG re-assessment triggered for the coach trigger, FR9 re-validation flagged for the audience segments.
- **Cross-product completeness:** 4 coach triggers × 6 audience segments → validate 24 combinations scored with axis-by-axis detail.

### Safety Tests
- **PTG exclusion:** Insert a `raw_unresolved` trigger into `trigger_map.json`. Run engine → validate: trigger excluded in Phase 1, never appears in match results, exclusion logged.
- **FAILED Context Premise rejection:** Provide FR9 output with `four_laws_status.overall_status = "FAILED"` → engine halts with `CONTEXT_PREMISE_FAILED`.
- **Adjacent match firewall:** Generate a two-axis match (score = 2.0) → validate: no seed constructed, diagnostic report generated, match classified ADJACENT.
