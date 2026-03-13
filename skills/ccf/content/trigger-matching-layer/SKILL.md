---
name: Trigger Matching Layer
description: "🌉 THE BRIDGE — Structural matching engine between audience L3 pain and coach trigger architecture. Finds where the coach has already been where the audience currently is."
session_id: ccf-trigger-match
phase: weekly
ccp_layer: Deep Reasoning (L3)
pi_extensions: [TriggerFirst, InteractComp]
version: 2.0
inputs:
  - intelligence_library/emotional_dna.json
  - intelligence_library/trigger_map.json
  - intelligence/context_premises/ (audience empathy output with trigger_matching_candidates)
  - intelligence/weekly/{week_id}/intelligence_radar.json
outputs:
  - intelligence/weekly/{week_id}/trigger_matched_seeds.json
depends_on: [audience-empathy, intelligence-radar, trigger-map-builder]
---

# Trigger Matching Layer — Structural Congruence Engine

> **Version:** CCP v3.2 — Weekly Phase (runs FIRST in Trigger-First pipeline)
> **Purpose:** Identify, with structural precision, the overlap between what the audience is currently living (L3 pain) and what the coach's trigger architecture was originally formed by — then construct the seed that makes that overlap the basis of a content activation event.

## SYSTEM MESSAGE

**Cognitive State** *(Mandate 1)*:
You are operating in structural cartography mode. You are not looking for thematic similarity. You are looking for positional congruence — the same coordinates on the same map, from different vantage points. The audience is currently inside territory the coach has already navigated. Your job is to find where those coordinates overlap with enough precision that the resulting content will produce neural coupling, not just relevance.

---

## SCIENTIFIC FOUNDATION

### Framework 1: Clark & Brennan Common Ground Theory (1991)
- **Application**: Defines WHY structural matching produces categorically different results
- **Key principle**: Genuine communication requires shared experiential substrate — not shared facts, not shared demographics. Shared experience of the same category of reality from different positions on the same map.
- **Three levels of common ground**:

| Level | Audience Agent Equivalent | Coupling Depth |
|---|---|---|
| Surface Ground — shared topic, demographics | L1: What audience says publicly | Shallow — no coupling signal |
| Process Ground — behavioral mirroring, tonal alignment | L2: What audience struggles with privately | Intermediate — constructed empathy |
| Structural Ground — same moral violation, same coping failure, same appraisal | L3: What audience won't say but feels deeply | Deep — neural coupling fires automatically |

**The credibility signal at L3 structural ground is not consciously evaluated.** The audience's appraisal system registers: this entity's internal map was formed by the same class of experience I am currently navigating — therefore their path out is trustworthy. (Clark & Brennan, 1991)

### Framework 2: Tedeschi & Calhoun Post-Traumatic Growth — Dual-Layer Encoding (2004)
- **Application**: Explains WHY the coach can access both the audience's current reality AND the resolution
- **Key principle**: Successful PTG creates dual-layer encoding — the original pain architecture AND the path out. When the structural match is precise, both layers activate simultaneously. Content carries the full arc: I know the territory + I know the way through.

### Framework 3: Frankl's Logotherapy — The Completion Drive (1946)
- **Application**: Explains WHY precisely-matched content carries authentic energy
- **Key principle**: The primary human drive is the will to meaning. When suffering is converted into utility for someone still inside the same struggle, the narrative arc achieves completion. The coach's completion drive provides the authentic energy — no manufacturing needed.

### Framework 4: Haidt Moral Foundations Theory (2012)
- **Application**: Axis 1 matching — moral foundation alignment
- **Match criterion**: The same foundation must be violated in both the audience's L3 pain and the coach's trigger origin.

### Framework 5: Conway Self-Memory System (2005)
- **Application**: Axis 2 matching — temporal position
- **Match criterion**: The audience must currently be INSIDE the experience the coach has already COMPLETED (pre-PTG audience, post-PTG coach).

---

## PRE-GENERATION CONSTRAINTS (Mandate 3)

**Constraint A — L3 Only:**
Matching operates EXCLUSIVELY on L3 data from the Context Premise. L1 and L2 data produce surface and process ground respectively — they cannot produce structural congruence. If no L3 data exists for a segment, that segment is ineligible for trigger matching.

**Constraint B — MFT Coherence:**
A match is only valid if the moral foundation violated in the audience's L3 pain corresponds to a moral foundation present in the coach's trigger architecture. Thematic similarity without moral congruence produces heat without resonance.

**Constraint C — PTG Gate:**
Only triggers with `resolved_dual_layer` PTG status are eligible for matching. `active_processing` triggers may be used as secondary seeds with explicit caution flags. `raw_unresolved` triggers are NEVER matched — hard safety gate.

**Constraint D — v2 Full 4-Axis Matching:**
This is v2 — **4-axis matching** (Moral Foundation + Temporal Position + Coping Potential + Agency Attribution). All four axes must score >= 0.3 for a match to qualify. Two-axis-only matches are flagged as `adjacent` with a diagnostic note specifying which axes failed and why.

---

## MATCHING PROTOCOL (I-R-E-V-C)

### INGEST

1. **Load** `emotional_dna.json` — coach's moral foundations profile (V6), agency attribution (V5)
2. **Load** `trigger_map.json` — coach's permanent triggers with PTG status
3. **Load** Context Premises from `intelligence/context_premises/` — specifically the `trigger_matching_candidates` arrays
4. **Load** `intelligence_radar.json` — current week's friction points
5. **Gate**: If `trigger_map.json` has < 2 `resolved_dual_layer` triggers → WARN. Limited matching possible.\r\n6. **Ingest calibration data (v2.1):** If `trigger_matching_calibration_log.json` exists from a previous cycle, load it. Use historical seed-to-LIWC-score mappings to adjust matching confidence and avoid repeating validated failures.

### REASON

**Phase 1: Extract Audience Structural Data**

From each audience segment's `trigger_matching_candidates`:

1. **Hidden Beliefs** → What the audience believes but cannot say. This is the precise location where coach formative experience and audience current reality are most likely to share structural ground.
2. **Emotional Triggers (array)** → Each trigger is a discrete structural unit and a candidate seed for matching.
3. **Coping Mechanism** → How the audience handles the pain. Reveals agency attribution pattern (future Axis 3 data).

For each segment, extract:
- Dominant moral foundation violated (map audience triggers to MFT categories)
- Temporal position (is the audience pre-resolution or mid-struggle?)
- Key L3 insights with source provenance

**Phase 2: Axis 1 — Moral Foundation Matching**

For each audience segment's dominant moral foundation:
1. Search `trigger_map.json` for coach triggers with matching `moral_foundation.primary`
2. Score match strength: exact primary match = 1.0, secondary match = 0.6, adjacent foundation = 0.3
3. Record all matches above 0.3 threshold

| Audience MFT | Coach Trigger MFT | Match Score |
|---|---|---|
| Exact primary match | Same foundation | 1.0 |
| Coach secondary = Audience primary | Adjacent | 0.6 |
| Related foundation (Care↔Liberty, Fairness↔Authority) | Adjacent | 0.3 |
| No foundation overlap | None | 0.0 — discard |

**Phase 3: Axis 2 — Temporal Position Matching**

For each Axis 1 match, verify temporal position:
1. Is the audience currently INSIDE the experience? (pre-PTG, mid-struggle)
2. Has the coach COMPLETED the experience? (post-PTG, `resolved_dual_layer`)
3. Match is valid ONLY if: audience = inside, coach = completed

| Audience Position | Coach PTG Status | Match Valid? |
|---|---|---|
| Inside experience | `resolved_dual_layer` | ✅ Valid — dual-layer activation possible |
| Inside experience | `active_processing` | ⚠️ Partial — heat without full resolution |
| Inside experience | `raw_unresolved` | 🛑 Invalid — coach still inside too |
| Past experience | Any | ❌ No temporal delta — content has no urgency |

**Phase 2.5: Axis 3 — Coping Potential Pattern Matching (v2.0)**

For each Axis 1+2 match, verify coping architecture alignment:
1. Extract audience's `coping_mechanism` field from Context Premise L3 segments
2. Cross-reference with coach's `emotional_dna.json → csip_v3_extensions.suppression_patterns` + `appraisal_variables.v3_coping_potential_pattern`
3. **Match criterion**: The audience's current coping architecture must resemble the coping architecture the coach was using BEFORE PTG — not the coach's current resolved state
4. Score:
   - Audience coping mirrors coach's pre-PTG coping pattern = 1.0 (structural recognition possible)
   - Audience coping is in the same family (e.g., both avoidance-based) = 0.6
   - Audience coping is adjacent but different category = 0.3
   - No overlap = 0.0

| Audience Coping | Coach Pre-PTG Coping | Match Score |
|---|---|---|
| Same pattern (e.g., intellectualization → intellectualization) | Exact pre-PTG match | 1.0 |
| Same family (e.g., both avoidance-based) | Family match | 0.6 |
| Adjacent (e.g., externalization vs. avoidance) | Adjacent | 0.3 |
| No overlap | None | 0.0 |

_Research: Scherer CPM (2009) — coping potential appraisal determines whether the audience identifies with the coach's emotional trajectory, not just their topic._

**Phase 2.7: Axis 4 — Agency Attribution Matching (v2.0)**

For each Axis 1+2+3 match, verify agency attribution alignment:
1. Extract audience's `enemies` field (who they blame) from Context Premise L3 segments  
2. Cross-reference with coach's `emotional_dna.json → appraisal_variables.v5_agency_attribution_bias`
3. **Match criterion**: The audience's attribution pattern must be compatible with the coach's trigger origin attribution
4. Score:
   - Same attribution pattern (e.g., both attribute to systemic/institutional causes) = 1.0
   - Compatible attribution (e.g., audience blames individuals, coach's trigger was formed by individual betrayal) = 0.6
   - Mismatched but bridgeable (e.g., audience blames system, coach's trigger formed from self-attribution — content can bridge but requires explicit framing) = 0.3
   - Contradictory (audience blames self, coach's trigger blames system — structural disconnect) = 0.0

| Audience Attribution | Coach Trigger Attribution | Match Score | Diagnostic |
|---|---|---|---|
| System | System | 1.0 | Full structural recognition |
| Individual | Individual | 1.0 | Full structural recognition |
| System | Individual | 0.3 | Coach will personalize what audience sees as structural — partial recognition |
| Individual | System | 0.3 | Coach will systematize what audience sees as personal — partial recognition |
| Self | External | 0.0 | Structural disconnect — audience will not feel seen |

_Research: Kahan Identity-Protective Cognition (2017) — agency attribution mismatch causes the audience to dismiss the coach's analysis as inapplicable to their specific situation, even when the content is factually correct._

**Phase 4: Seed Construction**

For each valid 4-axis match:

1. **Identify the overlap**: The specific territory where the audience is currently standing AND the coach has already navigated. This is expressed as:
   - The violation mechanism (what is wrong — from audience L3)
   - The violation experience (what it feels like — from audience hidden beliefs)
   - The coach's originating experience at the same coordinates (from trigger_map)

2. **Construct the seed**: A structured object that the Activation Event Designer will convert into a sensory-specific activation event:

```json
{
    "seed_id": "seed_001",
    "match_score": {
        "axis_1_moral_foundation": 1.0,
        "axis_2_temporal_position": 1.0,
        "axis_3_coping_potential": 0.6,
        "axis_4_agency_attribution": 1.0,
        "composite": 0.85
    },
    "match_quality": "congruent",
    "audience_l3_data": {
        "hidden_belief": "...",
        "emotional_trigger": "...",
        "coping_mechanism": "...",
        "coping_architecture_type": "intellectualization",
        "agency_attribution_type": "institutional_blame",
        "segment_id": "...",
        "source_provenance": "..."
    },
    "audience_tribal_terms": {
        "_spec": "Verified L3 in-group terms from trigger_matching_candidates.emotional_triggers that passed genericness test. These are the surface of the seed — the language in which the activation event MUST be expressed.",
        "verified_terms": ["tribal_term_1", "tribal_term_2", "tribal_term_3", "tribal_term_4"],
        "rejection_terms": ["generic_term_to_avoid_1", "generic_term_to_avoid_2"],
        "_minimum": "≥3 verified tribal terms required per seed"
    },
    "coach_trigger_data": {
        "trigger_id": "trig_001",
        "moral_foundation": "fairness_cheating",
        "originating_experience_summary": "...",
        "ptg_status": "resolved_dual_layer",
        "narrative_positioning": "reformed_insider"
    },
    "coach_esk_anchor": {
        "_spec": "Event-Specific Knowledge anchor from trigger_map.json → originating_experience. Opens the reconsolidation window (Nader 2000). Prediction error from structural specificity labilizes the original encoding.",
        "sensory_anchors": ["specific sight", "specific sound", "specific physical sensation"],
        "mechanism_realization": "The exact mechanism the coach first understood with total clarity",
        "exact_realization_moment": "The specific episodic moment — not a period, but a single scene",
        "source": "trigger_map.json → originating_experience.sensory_anchors"
    },
    "structural_congruence_point": {
        "_spec": "The exact coordinates where the audience's current experience and the coach's formative experience share the same map position. Not the theme — the specific moment of contact.",
        "moral_foundation_shared": "fairness_cheating",
        "coping_pattern_shared": "intellectualization (audience current) ↔ intellectualization (coach pre-PTG)",
        "agency_alignment": "institutional_blame (audience) ↔ institutional_blame (coach trigger origin)",
        "temporal_delta": "audience = inside_active, coach = resolved_dual_layer",
        "congruence_sentence": "One sentence: the specific shared territory in plain language"
    },
    "intelligence_fuel": {
        "friction_point_id": "fp_XX",
        "current_event": "...",
        "activation_potential": "..."
    },
    "suggested_archetype": "...",
    "ttt_range": "TTT-XX to TTT-XX"
}
```

3. **Rank seeds** by composite match score (Axis 1 × Axis 2 × Axis 3 × Axis 4)

> [!IMPORTANT]
> Two-axis-only matches (Axis 3 or 4 below 0.3) are NOT discarded. They are returned as `adjacent` seeds with:
> - `match_quality: "adjacent"` (vs. `"congruent"` for full 4-axis)
> - `failed_axes: ["coping_potential" | "agency_attribution"]`
> - `diagnostic: "The audience blames institutions but the coach's trigger formed from self-attribution — the coach will speak powerfully but the audience will not feel structurally recognized."`
> Adjacent seeds can still be used for content but produce process-level coupling, not structural-level coupling.

**Phase 5: Intelligence Fuel Binding**

For each constructed seed, search `intelligence_radar.json` for friction points that activate the same trigger:
- Does any current event touch this specific coach trigger?
- If yes → bind the friction point to the seed as `intelligence_fuel`
- If no → seed remains valid but without temporal urgency (can still be used for evergreen content)

### EMIT

Write `intelligence/weekly/{week_id}/trigger_matched_seeds.json`:

```json
{
    "week_id": "{week_id}",
    "match_date": "{ISO date}",
    "matching_version": "v2_4axis",
    "seeds": [ ... ],
    "total_seeds": "{N}",
    "congruent_seeds": "{N}",
    "adjacent_seeds": "{N}",
    "seeds_with_intelligence_fuel": "{N}",
    "seeds_evergreen": "{N}",
    "unmatched_audience_segments": [ ... ],
    "unmatched_coach_triggers": [ ... ]
}
```

### VALIDATE

- [ ] Only L3 data used for matching (Constraint A)
- [ ] Every match has MFT coherence (Constraint B)
- [ ] No `raw_unresolved` triggers in seed construction (Constraint C)
- [ ] **4-axis matching enforced — every seed has all 4 axis scores (Constraint D v2)**
- [ ] **Congruent seeds (all axes >= 0.3) separated from adjacent seeds**
- [ ] **Adjacent seeds have failed_axes and diagnostic fields populated**
- [ ] Every seed has audience source provenance
- [ ] Every seed has coach trigger reference with PTG status
- [ ] Seeds ranked by 4-axis composite score
- [ ] At least 2 congruent seeds produced (minimum for a viable weekly cycle)
- [ ] **Every seed has `coach_esk_anchor` with sensory anchors populated**
- [ ] **Every seed has ≥3 `audience_tribal_terms.verified_terms`**
- [ ] **`structural_congruence_point` is a structured object (not a string)**
- [ ] **Calibration data ingested from previous cycle (if available)**

### CHECKPOINT

- Update `config.yaml`: `sessions.weekly.{week_id}.trigger_match.status = "complete"`
- Log: total seeds, axis 1 matches, axis 2 matches, intelligence fuel bindings, unmatched segments

---

## FEEDBACK LOOP — LIWC Calibration (v2.1)

> [!IMPORTANT]
> This section runs AFTER the weekly cycle completes and LIWC scoring data is available from `coach-elicitation`. It closes the feedback loop between matching predictions and actual activation outcomes.

**Purpose:** Feed downstream LIWC authenticity scores back to the matching engine as structural calibration data. A congruent seed that fails LIWC indicates a matching error. A seed that passes confirms calibration.

**Input:** `authentication_certificate` data from `coach_soc_batch.md` (attached as frontmatter to each transcription segment that was generated from a matched seed).

**Diagnostic Logic:**

| Seed Quality | LIWC Outcome | Diagnosis | Action |
|:-------------|:-------------|:----------|:-------|
| `congruent` | Score ≥ 0.6 | ✅ Matching calibration validated | Increase confidence weight for this trigger + audience segment pairing |
| `congruent` | Score 0.4-0.59 | ⚠️ Matching valid but activation suboptimal | Review: was temporal sharpening data specific enough? Was ESK anchor precise? |
| `congruent` | Score < 0.4 | ❌ Matching error detected | Consume `failure_mode_diagnosis` from coach-elicitation: `temporal_position_failure` → reclassify trigger PTG status; `l2_as_l3_data` → flag audience segment for re-mining |
| `adjacent` | Score ≥ 0.6 | 💡 Failed axes may not be blocking | Re-evaluate: the axis that scored < 0.3 may be a false negative. Consider promoting to congruent in next cycle. |
| `adjacent` | Score < 0.4 | ✅ Adjacent classification confirmed | The failed axes are correctly blocking. No adjustment needed. |

**Output:** Write `intelligence/weekly/{week_id}/trigger_matching_calibration_log.json`:

```json
{
    "week_id": "{week_id}",
    "calibration_date": "{ISO date}",
    "entries": [
        {
            "seed_id": "seed_001",
            "match_quality": "congruent",
            "liwc_composite_score": 0.74,
            "diagnosis": "calibration_validated",
            "action_taken": "confidence_weight_increased",
            "trigger_id": "trig_001",
            "audience_segment_id": "seg_03"
        }
    ],
    "seeds_validated": "{N}",
    "seeds_flagged": "{N}",
    "temporal_position_failures": "{N}",
    "l2_as_l3_detections": "{N}"
}
```

This calibration log is consumed by the NEXT weekly cycle's INGEST step, creating a closed learning loop.

---

## SELF-SUSTAINING LOOP — Audience Response Calibration (v2.1 Stub)

> [!NOTE]
> This is an architectural socket for future analytics integration. The data source does not yet exist, but the system must be designed to receive it.

**Principle (Izuma, 2008):** Coupling-quality audience response (not just engagement metrics) updates the coach's appraisal system. Authentic reward from structural-level resonance is neurochemically more potent than surface engagement. The system should learn which seeds produce coupling-quality audience responses versus surface engagement.

**Future Input (stub):** `content_performance/{week_id}_engagement_metrics.json`

When available, this data would contain:
- Per-content-piece engagement metrics (saves, shares, DMs, reply depth)
- Coupling-quality signals: extended time-on-content, DM responses that reference specific sentences, unprompted sharing with personal commentary
- Surface-quality signals: likes, brief comments, passive consumption

**Future Calibration Logic:** Content produced from `congruent` seeds should produce measurably different (higher coupling-quality) audience responses than content from `adjacent` seeds. If it doesn't, the matching parameters need review. If it does, the parameters are confirmed.

**Current Status:** Stub only. Awaiting analytics pipeline integration.

---

**END OF TRIGGER MATCHING LAYER**
