# Tech-Spec: FR5 — Standing Trigger Map & Activation History Feedback Loop

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §5.2 (Corrected Intake Flow — Trigger-First), §5.3 (Genesis Pipeline — Stage 1 Emotional DNA), §5.4 (Weekly Pipeline — Stage 5 Trigger Architecture Update), §5.8 (Standing Trigger Intelligence Library)
**Skill Implementation:** `skills/ccf/setup/trigger-map-builder/SKILL.md`

---

## Overview

### Problem Statement

The Trigger-First Engine inverts the causal direction of content generation: instead of asking what the coach should say about current events, it asks what permanently fires this coach — then uses current events as fuel for a fire already burning (Trigger-First Engine Architecture v3.0 §Part 2).

This inversion requires a standing artifact — `trigger_map.json` — that maps each coach's permanent trigger architecture with enough granularity to:
1. **Predict activation** before voice notes are recorded (Haidt MFQ-2 → Which current events will fire which moral foundation?)
2. **Design activation events** that reach Event-Specific Knowledge instead of Lifetime Period or General Event synthesis (Conway AKB hierarchy)
3. **Protect the coach** from unsafe re-activation of unresolved trauma (Tedeschi & Calhoun PTG classification)
4. **Compound learning** across sessions by feeding LIWC-22 authenticity scores back into trigger precedence ranking

The legacy system had no Trigger Map. Intelligence scanning was topic-first — the system identified what was trending and asked the coach to react. This produced mask output (Kahan identity-protective cognition): semantic synthesis filtered through professional identity, not episodic invocation of authentic material. FR5 eliminates this by providing the intelligence radar (Stage 2) with a structural target: the specific moral violations and sensory anchors that this coach's appraisal system is already calibrated to detect.

### Solution

A 6-phase Trigger Map builder (Genesis Phase 0) + a weekly feedback loop (Weekly Pipeline Stage 5) that updates trigger activation precedence based on measured authenticity scores. The map has two states:
- **Cold start (Genesis):** Map built from `emotional_dna.json` + interview corpus. `activation_history` is empty.
- **Warm operation (Weekly):** Each production session writes a new `activation_history` entry with LIWC-22 score, trigger used, archetype assigned, and content performance data. Triggers that consistently produce high-authenticity responses climb in precedence ranking. Triggers that consistently produce mask output fall.

### Scope

**In scope:**
- `trigger_map.json` structure and schema (DEP-LIB-002)
- 6-phase extraction pipeline (I-R-E-V-C protocol from SKILL.md)
- Conway AKB origin classification per trigger
- Tedeschi & Calhoun PTG resolution status with safety gate
- McAdams narrative identity positioning per trigger
- Nader reconsolidation sensitivity assessment
- Archetype mapping per trigger (Trigger-First Engine Stage 5)
- `activation_history` feedback loop from weekly pipeline
- Backward compatibility fallback when `trigger_map.json` does not exist
- Acceptance criteria and testing strategy

**Out of scope:**
- Emotional DNA extraction (FR4 Tech Spec — prerequisite, produces DEP-LIB-001)
- Activation Event design (Stage 3 of Trigger-First Engine — downstream consumer)
- LIWC-22 authenticity scoring mechanics (FR2 Tech Spec — used here as input only)
- Standing Trigger Intelligence Library research evidence seeding (FR1 Genesis Pipeline Phase 2 — parallel process)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-LIB-002` | Trigger Map | PRIMARY OUTPUT — the map itself |
| `DEP-LIB-001` | Emotional DNA (10-Variable Profile) | REQUIRED INPUT — V1 (Trigger Specificity), V4 (Norm Compatibility), V5 (Agency Attribution), V6–V10 (MFQ-2 Moral Foundations) drive trigger identification |
| `DEP-ENG-003` | Positive Space (Voice DNA) | DOWNSTREAM CONSUMER — Voice DNA compilation reads trigger archetype mapping for rhythm profile selection |
| `DEP-ENG-005` | Trigger Taxonomy | DOWNSTREAM CONSUMER — Stage 2 intelligence scanning uses trigger category indexing |
| `DEP-ENG-019` | Session Transcript Intelligence | FEEDBACK INPUT — weekly LIWC-22 scores from authenticated voice notes feed `activation_history` |
| `DEP-ENG-023` | Cultural Memory Map | CROSS-REFERENCE — CMM Layer 7 (Shared Enemy Typology) aligns with trigger moral foundations |

### Academic Research Grounding

| Component | Framework | Key Papers | Lab Reference |
|---|---|---|---|
| Trigger origin classification | Conway Self-Memory System / AKB Hierarchy (2005) | Conway (2005) *The Self and Autobiographical Memory* | [Memory Retrieval vs. Semantic Construction.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Memory%20Retrieval%20vs.%20Semantic%20Construction.md) |
| PTG resolution status | Tedeschi & Calhoun Post-Traumatic Growth (2004) | Tedeschi & Calhoun (2004) *Post-Traumatic Growth: Conceptual Foundations* | SKILL.md §Framework 2 |
| Narrative positioning | McAdams Narrative Identity Theory (2001) | McAdams (2001) *The Psychology of Life Stories* | SKILL.md §Framework 3 |
| Reconsolidation sensitivity | Nader Memory Reconsolidation (2000) | Nader et al. (2000) *Fear memories require protein synthesis for reconsolidation after retrieval* | [Memory Retrieval vs. Semantic Construction.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Memory%20Retrieval%20vs.%20Semantic%20Construction.md) (§Nader) |
| Moral foundation mapping | Haidt MFQ-2 (2012/2023) | Graham et al. (2013); Atari et al. (2023) MFQ-2 | [Moral Foundations Theory for Trigger Prediction.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Moral%20Foundations%20Theory%20for%20Trigger%20Prediction.md) |
| Mask bypass / Authentic elicitation | Kahan Identity-Protective Cognition; Festinger Cognitive Dissonance; Edmondson Psychological Safety | Kahan (2013); Festinger (1957); Edmondson (1999) | [Identity Protection and Authentic Expression.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Identity%20Protection%20and%20Authentic%20Expression.md) |
| Sensory-specific activation | Conway AKB → ESK retrieval; Schacter Focal Enhancement | Schacter (1999) *Seven Sins of Memory* | [Memory Retrieval vs. Semantic Construction.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Memory%20Retrieval%20vs.%20Semantic%20Construction.md) (§Schacter) |

### Key Files

| File | Purpose |
|---|---|
| `skills/ccf/setup/trigger-map-builder/SKILL.md` | Existing skill definition — I-R-E-V-C protocol, 6-phase extraction |
| `intelligence_library/trigger_map.json` | Primary output target |
| `intelligence_library/emotional_dna.json` | Required input (from FR4) |
| `intelligence_library/coach_soul.json` | Identity + pipeline status |
| `config.yaml` | Session status tracking |
| `raw/transcripts/` | Source corpus |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Emotional DNA required before Trigger Map** | V4 (Norm Compatibility) and V6–V10 (MFQ-2) from `emotional_dna.json` are structurally required — they define WHAT fires the coach. Without them, trigger identification would rely on surface-level topic analysis (the exact topic-first failure the Trigger-First Engine is designed to eliminate). |
| **PTG classification as a hard safety gate** | `raw_unresolved` triggers must be excluded from the activation pipeline — not flagged, not discounted, EXCLUDED. Activating unresolved trauma in a content production context is an ethical boundary, not a quality consideration. |
| **ESK-level as highest value** | Conway's AKB hierarchy demonstrates that only Event-Specific Knowledge contains the full appraisal cascade (Scherer CPM) + sensory-perceptual records needed for episodic invocation. General Event and Lifetime Period triggers produce semantic synthesis — which is mask output. |
| **`activation_history` as feedback, not override** | Weekly LIWC-22 scores update trigger PRECEDENCE, not trigger existence. A trigger that consistently produces low-authenticity responses drops in activation precedence for the intelligence radar, but it is never deleted — it may indicate a deeper interview is needed to surface the ESK. |
| **Backward compatibility fallback** | If `trigger_map.json` does not exist (new coach still in Genesis setup, or pre-V3.1 coach), the weekly pipeline falls back to legacy DARN-CAT question generation. This ensures production continuity during gradual rollout. |
| **Candidate triggers vs confirmed triggers** | Triggers without corpus evidence are hypotheses. They go in `candidate_triggers[]`, not in the primary `triggers[]` array. This prevents the LLM from populating the map with its own constructed patterns (the exact Schacter Bias sin that contaminates semantic synthesis). |

---

## Implementation Plan

### Prerequisite Gate

**Condition:** `emotional_dna.json → extraction_status.confidence ≥ 0.5`

If not met → Pipeline runs with WARNING. Trigger map will be partial. If `emotional_dna.json` does not exist → Pipeline does NOT run.

---

### Phase 1: INGEST

**Agent:** Trigger Map Builder (operating in archaeological mode — structural pattern recognition)
**Pi Extensions:** `SoulResonance`, `TriggerFirst`

**Steps:**
1. Load `emotional_dna.json` — verify extraction is complete.
2. Gate: If `extraction_status.confidence` < 0.5 → WARN (map will be partial). If file does not exist → STOP.
3. Load `coach_soul.json` — read existing identity data.
4. Load all transcripts from `raw/transcripts/`.
5. Load `trigger_map.json` template with empty arrays.
6. Write `receipt` → Receipt Chain Guard (Trigger Map — Phase 1 Ingest).

---

### Phase 2: REASON — Trigger Identification

**Uses:** V4 (Norm Compatibility Threshold) + V6–V10 (MFQ-2 Moral Foundations) from `emotional_dna.json`

**Action:** Search the corpus for trigger activation passages — moments where the coach shifts from intellectual discussion to activated response.

**Identification Markers (LIWC-22 aligned):**
| Marker | Signal | What It Means |
|---|---|---|
| Sentence length compression | Shorter under emotional arousal | Working memory hijacked — Kensinger selective accuracy |
| Pronoun shift (I/me increase) | Ownership claimed | Authentic activation — Pennebaker |
| Verb tense shift (present-dominant) | Immediate engagement | Episodic invocation, not rehearsed narrative |
| Hedging language drops | "but, sort of, maybe" disappear | Certainty increases — no social softening |
| Exclusive word increase | "but, except, however" spike | Cognitive distinctions being made in real time |
| Discourse marker displacement | Markers shift to intonation-unit initial | Speech planning disrupted by emotional load |

**For each identified trigger passage:**
1. **Label** the trigger (the specific mechanism/violation)
2. **Map** to moral foundation from V6–V10 profile
3. **Record** the activation keywords and mechanism phrases
4. **Cite** the specific corpus passage (Mandate 7 — provenance)

---

### Phase 3: REASON — Origin Classification (Conway AKB Hierarchy)

**Framework:** Conway Self-Memory System (2005) — Autobiographical Knowledge Base Hierarchy

For each trigger, search the corpus for the originating experience:

| AKB Level | Corpus Evidence | Classification | Value for Activation |
|---|---|---|---|
| **Event-Specific Knowledge (ESK)** | Coach describes a specific moment: a date, a place, sensory detail, who was present, what was said | `esk` | **Highest** — full appraisal cascade available. Contains the sensory anchors needed for Nader reconsolidation labilization. |
| **General Events (GE)** | Coach describes a pattern: "the clients I kept seeing get misled" — cluster of related experiences | `general_event` | **Medium** — produces thematic activation but not episodic invocation. Flag for deeper interview. |
| **Lifetime Periods (LP)** | Coach describes a chapter: "my years in corporate" — broad temporal segment | `lifetime_period` | **Low** — produces semantic synthesis. The mask architecture operates most effectively at this level (Conway). |

**If ESK evidence exists:** Record sensory anchors — the specific room, the specific document, the specific sentence someone said, the smell, the time of day. These become the raw material for Stage 3 Activation Event Design.

**If only GE/LP evidence exists:** Flag as `needs_deeper_interview = true`. Place in primary `triggers[]` array only if moral foundation mapping is confirmed; otherwise → `candidate_triggers[]`.

---

### Phase 4: REASON — PTG Assessment (Tedeschi & Calhoun)

**Framework:** Post-Traumatic Growth Theory (2004) — Dual-Layer Encoding

For each trigger, assess resolution status by searching for two types of evidence:

**Step A — Search for pain passages:** Does the coach describe the original violation with emotional activation? (Evidence of primary neural encoding intact)

**Step B — Search for resolution passages:** Does the coach describe how they navigated through this? (Evidence of secondary "path out" network superimposed over original encoding)

**Classification:**

| Status | Evidence Required | Content Suitability | Pipeline Action |
|---|---|---|---|
| `resolved_dual_layer` | Pain passages ✅ + Resolution passages ✅ | **Highest** — Coach can access BOTH the original pain AND the resolution. Content carries the full arc. | Include in activation pipeline. |
| `active_processing` | Pain passages ✅ + Partial/incomplete resolution ⚠️ | **Moderate** — Content has heat but incomplete resolution signal. | Include with monitoring flag: `emotional_load_monitor = true`. |
| `raw_unresolved` | Recent/raw emotional language without analytical distance 🛑 | **NOT suitable** — Live trauma. | **EXCLUDE from activation pipeline. Hard safety gate.** |

> **Constraint B enforcement:** Any trigger classified as `raw_unresolved` is IMMEDIATELY excluded from the activation pipeline AND from intelligence radar targeting. This is not a prompt instruction — it is a code-level filter in the weekly pipeline that checks PTG status before selecting triggers.

**Minimum viable map:** At least 2 triggers must be classified `resolved_dual_layer` for the map to be declared complete. If < 2 → map status = `partial`, pipeline can operate but with reduced activation coverage.

---

### Phase 5: REASON — Narrative Identity (McAdams 2001)

**Framework:** Narrative Identity Theory — Redemption/Contamination Sequences

For each trigger, identify:

**Sequence Type:**
- **Redemption sequence** (bad → good): "I went through this → here's what I learned → here's how I help others now"
- **Contamination sequence** (good → bad): "Things were good → this happened → everything changed"
- **Mixed/Evolving:** Both patterns present for the same trigger — coach is still processing the narrative structure

**Narrative Positioning:**

| Position | Pattern | Content Implication |
|---|---|---|
| `reluctant_hero` | "I didn't want to speak up, but I had to" | Content arc: from silence to voice. Audience identifies with the hesitation. |
| `whistleblower` | "I'm exposing what others won't say" | Content arc: from insider knowledge to public truth. High Liberty/Oppression activation. |
| `reformed_insider` | "I was part of the problem, now I fight it" | Content arc: from complicity to advocacy. Highest authenticity ceiling — vulnerability. |
| `outsider_witness` | "I watched this damage people from the outside" | Content arc: from observation to intervention. Care/Harm foundation. |
| `survivor_guide` | "I went through it, now I map the territory" | Content arc: from personal pain to shared wisdom. Strongest redemption sequence. |

---

### Phase 6: REASON — Reconsolidation Sensitivity (Nader 2000)

**Framework:** Memory Reconsolidation Theory — Prediction Error Requirement for Trace Labilization

For each trigger, assess how much prediction error is required to labilize the episodic trace:

| Sensitivity | Score | Corpus Evidence | Activation Event Design Implication |
|---|---|---|---|
| **High sensitivity (low threshold)** | 1–3 | Coach re-activates easily when topic is raised, even in generic terms. Even Lifetime Period prompts reach emotional activation. | Low-specificity activation events work. Intelligence radar can use broad current event matching. |
| **Medium sensitivity** | 4–6 | Coach requires specific mechanism detail to shift from intellectual to activated. General Event evidence but not immediate ESK. | Medium-specificity activation events. Intelligence radar needs mechanism-level matching. |
| **Low sensitivity (high threshold)** | 7–10 | Coach requires highly specific, sensory-detailed activation events to access ESK. Maintains analytical distance unless precise mechanism is presented. | High-specificity activation events ONLY. Intelligence radar must match exact mechanism patterns. |

**Cross-validation:** Reconsolidation sensitivity MUST correlate with V1 (Trigger Specificity Threshold) from `emotional_dna.json`. If V1 = 8 (high specificity) but reconsolidation = 2 (low threshold) → incoherence. Flag for review.

---

### Phase 7: REASON — Archetype Mapping (Trigger-First Engine Stage 5)

For each trigger, map the emotional state it produces to the content archetype table:

| Emotional State When Trigger Fires | Primary Archetype Candidates | TTT Requirement |
|---|---|---|
| Disgust + protective fury (Sanctity/Degradation) | `myth_indignation` / `reaction_outrage` | TTT-07+ |
| Betrayal-anger (Loyalty/Betrayal) | `myth_indignation` / `comparison_outrageous` | TTT-07/08 |
| Outrage at mechanism opacity (Fairness/Cheating) | `listicle_shocking` / `comparison_shocking` | TTT-05/06 |
| Protective urgency (Care/Harm + Liberty/Oppression) | `myth_fear_anxiety` / `tweet_warning` | TTT-05+ |
| Righteous authority (Fairness + Authority) | `tier_list_controversial` / `myth_empowering` | TTT-05/06 |
| Grief-tinged outrage (Care/Harm high weighting) | `story_transformation` / `story_recognition` | TTT-03+ |

**TTT compatibility check:** Can this coach credibly occupy the temperature required by this archetype for this trigger? Check against `ttt_baseline.json` (from FR3). Set `coach_eligible = true/false` per mapping.

---

### Phase 8: EMIT — Write Output

Write populated `trigger_map.json` to `intelligence_library/trigger_map.json`:

```json
{
  "dep_id": "DEP-LIB-002",
  "version": "1.0",
  "map_status": {
    "total_triggers_mapped": 0,
    "total_candidate_triggers": 0,
    "resolved_dual_layer_count": 0,
    "confidence": 0.0,
    "last_built": "ISO8601",
    "last_feedback_update": null,
    "emotional_dna_confidence": 0.0
  },
  "triggers": [
    {
      "trigger_id": "TRG-001",
      "label": "descriptive label of the violation/mechanism",
      "moral_foundation": "care_harm|fairness_cheating|loyalty_betrayal|authority_subversion|sanctity_degradation|liberty_oppression",
      "moral_foundation_weight": 0.0,
      "activation_keywords": [],
      "mechanism_description": "the specific violation mechanism",
      "origin": {
        "akb_level": "esk|general_event|lifetime_period",
        "sensory_anchors": [],
        "temporal_context": "",
        "needs_deeper_interview": false
      },
      "ptg_status": "resolved_dual_layer|active_processing|raw_unresolved",
      "ptg_evidence": {
        "pain_passages": [],
        "resolution_passages": []
      },
      "narrative": {
        "sequence_type": "redemption|contamination|mixed",
        "positioning": "reluctant_hero|whistleblower|reformed_insider|outsider_witness|survivor_guide"
      },
      "reconsolidation_sensitivity": {
        "score": 0,
        "scale": "1-10",
        "v1_correlation_check": "pass|fail|review"
      },
      "archetype_mapping": {
        "emotional_state": "",
        "primary_archetypes": [],
        "ttt_requirement": "",
        "coach_eligible": false
      },
      "activation_history": [],
      "activation_precedence": null,
      "evidence_passages": []
    }
  ],
  "candidate_triggers": [],
  "trigger_archetype_map": {
    "last_updated": "ISO8601",
    "mappings": []
  }
}
```

---

### Phase 9: VALIDATE & CHECKPOINT

**Validation checks:**
- [ ] `emotional_dna.json` was loaded and verified before extraction began
- [ ] Every trigger in `triggers[]` has ≥1 evidence passage (Mandate 7)
- [ ] Every trigger has a moral foundation mapping consistent with V6–V10
- [ ] Every trigger has PTG status assessed
- [ ] NO `raw_unresolved` triggers remain in the activation pipeline (hard gate)
- [ ] At least 2 triggers are classified `resolved_dual_layer`
- [ ] Archetype compatibility checked against TTT baseline
- [ ] Reconsolidation sensitivity correlated with V1 (Trigger Specificity Threshold)
- [ ] Narrative positioning consistent across triggers (or explicitly noted as variable)

**Checkpoint:**
- Update `config.yaml`: `sessions.setup.trigger_map.status = "complete"`
- Update `coach_soul.json`: `extraction_pipeline_status.trigger_map_complete = true`
- Log: triggers mapped, PTG distribution, ESK/GE/LP counts, archetype eligibility summary
- Write `receipt` → Receipt Chain Guard (Trigger Map — Complete)

---

## Weekly Feedback Loop — Stage 5: Trigger Architecture Update

> **This is NOT part of Genesis setup. This runs during every weekly production session as Stage 5 of the Weekly Pipeline.**

### Trigger

After `ccf-validate` completes (all 36 scripts pass Sophia + Marcus + Chen validation), the pipeline writes feedback into `trigger_map.json`.

### Feedback Data

For each trigger used in this production session:

```json
{
  "session_id": "weekly_session_2026-W12",
  "trigger_id": "TRG-001",
  "timestamp": "ISO8601",
  "authenticity_score": 0.0,
  "archetype_assigned": "myth_indignation",
  "ttt_achieved": "TTT-07",
  "content_performance": {
    "sophia_drift": 0.0,
    "chen_ai_detection": 0.0,
    "engagement_7d": null
  }
}
```

### Precedence Update Logic

After ≥3 activation history entries exist for a trigger:

1. Calculate `mean_authenticity` across all entries
2. Calculate `trend` (is authenticity improving, stable, or declining over last 3 entries?)

| Pattern | Precedence Action |
|---|---|
| `mean_authenticity ≥ 7/10` AND `trend = improving/stable` | **Climb** — trigger moves UP in activation precedence. Intelligence radar prioritizes current events that match this moral foundation. |
| `mean_authenticity 5–7/10` AND `trend = stable` | **Hold** — trigger maintains current precedence. No change. |
| `mean_authenticity < 5/10` OR `trend = declining` | **Fall** — trigger moves DOWN in activation precedence. Intelligence radar deprioritizes. Flag for review: is the activation event design too generic? Does the coach need a deeper interview to surface ESK? |
| `mean_authenticity < 3/10` across ≥3 sessions | **Dormant** — trigger is marked `dormant`. NOT deleted — it may indicate that the coach's relationship to this trigger has changed (life event, identity shift). Schedule re-interview. |

### Standing Trigger Intelligence Library Integration

When a trigger with `activation_precedence = "high"` produces CRAL research, that research enters the Standing Trigger Intelligence Library (§5.8) indexed by `trigger_category_id` — NOT by archetype. This builds the compounding knowledge base described in FR1 Genesis Pipeline Phase 2.

---

## Backward Compatibility — Legacy Fallback

**Condition:** `trigger_map.json` does not exist for this coach.

**Fallback behavior:**
1. The Scheduled Monitor Agent still runs daily community surveillance
2. Instead of mapping observations against the coach's trigger architecture, the system generates a DARN-CAT formatted question using legacy logic (topic-based, not trigger-first)
3. Coach receives a standard question: "What's on your mind about [topic]?" instead of a trigger-specific observation + DARN-CAT question
4. LIWC-22 authenticity scoring still applies to the voice note response
5. All downstream production pipeline phases operate normally

**Limitation of fallback:** Legacy question generation produces semantic synthesis (mask output), not episodic invocation. Expected authenticity scores will be 15–30% lower. The coach will receive content that sounds like them but does not carry the emotional architecture of their authentic trigger response.

**Exit from fallback:** When FR4 (Emotional DNA) + FR5 (Trigger Map) are completed, the weekly pipeline automatically switches to trigger-first operation. No manual intervention needed — the pipeline checks for `trigger_map.json` existence at session start.

---

## Tasks

- [ ] **Task 1:** Implement INGEST phase — `emotional_dna.json` gate, corpus loading, template initialization
- [ ] **Task 2:** Implement Trigger Identification — LIWC-22 marker detection (6 markers), moral foundation mapping from V6–V10
- [ ] **Task 3:** Implement AKB Origin Classification — ESK/GE/LP classification logic, sensory anchor recording, `needs_deeper_interview` flagging
- [ ] **Task 4:** Implement PTG Assessment — pain/resolution passage search, dual-layer classification, `raw_unresolved` hard safety gate (code-level exclusion from activation pipeline)
- [ ] **Task 5:** Implement McAdams Narrative Identity — sequence type classification, narrative positioning categorization
- [ ] **Task 6:** Implement Nader Reconsolidation Sensitivity — prediction error threshold scoring, V1 cross-validation
- [ ] **Task 7:** Implement Archetype Mapping — emotional state → archetype lookup, TTT compatibility check against `ttt_baseline.json`
- [ ] **Task 8:** Implement EMIT — `trigger_map.json` schema serialization with `triggers[]` and `candidate_triggers[]` separation
- [ ] **Task 9:** Implement VALIDATE — 9 validation checks + Receipt Chain Guard
- [ ] **Task 10:** Implement Weekly Feedback Loop (Stage 5) — `activation_history` entry writing, precedence update logic (climb/hold/fall/dormant)
- [ ] **Task 11:** Implement backward compatibility fallback — `trigger_map.json` existence check at session start, legacy DARN-CAT question generation
- [ ] **Task 12:** Implement Standing Trigger Intelligence Library integration — high-precedence trigger research → library ingestion indexed by `trigger_category_id`

---

## Acceptance Criteria

- [ ] **AC1 (Prerequisite Gate):** Pipeline does NOT start when `emotional_dna.json` does not exist. Returns `EMOTIONAL_DNA_REQUIRED` error.
- [ ] **AC2 (PTG Safety Gate):** A trigger classified as `raw_unresolved` never appears in the intelligence radar's trigger selection. A code-level filter in the weekly pipeline excludes it — not a prompt instruction.
- [ ] **AC3 (Mandate 7 — provenance):** Every trigger in `triggers[]` has ≥1 evidence passage from the corpus. A trigger identified without evidence goes to `candidate_triggers[]`, NOT `triggers[]`.
- [ ] **AC4 (Origin Classification):** A trigger with the corpus passage "I remember sitting in that boardroom on March 15th, the fluorescent light flickering, when John said 'we're restructuring'" → classified as `esk`. A trigger with "this kind of thing kept happening to my clients" → classified as `general_event`.
- [ ] **AC5 (Feedback Loop):** After 3 weekly sessions where trigger TRG-001 produces LIWC-22 authenticity scores of 8.2, 7.8, 8.5 → `activation_precedence` is set to "high". After 3 sessions with scores 2.1, 2.5, 1.8 → trigger is marked `dormant`.
- [ ] **AC6 (Backward Compatibility):** A coach without `trigger_map.json` receives a standard DARN-CAT topic question instead of a trigger-specific observation. All downstream pipeline phases complete successfully. No error thrown.
- [ ] **AC7 (Minimum Viable Map):** A map with only 1 `resolved_dual_layer` trigger → `map_status.confidence` reflects partial status. Pipeline operates with warning. A map with 0 → pipeline blocks production with `INSUFFICIENT_TRIGGERS` message.
- [ ] **AC8 (V1 Cross-Validation):** A trigger with reconsolidation sensitivity = 2 (low threshold) and V1 = 8 (high specificity) → cross-validation returns `fail`. Flag written to trigger entry.
- [ ] **AC9 (Archetype Eligibility):** A coach with TTT ceiling of TTT-04 → trigger archetype mapping for `myth_indignation` (requires TTT-07+) sets `coach_eligible = false`.
- [ ] **AC10 (Library Integration):** A high-precedence trigger's CRAL research enters the Standing Trigger Intelligence Library indexed by `trigger_category_id`. Research submitted with `archetype_id` as primary index → rejected.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR4 Emotional DNA Extraction | Internal prerequisite | `emotional_dna.json` must exist with confidence ≥ 0.5 |
| `ttt_baseline.json` | Internal | From FR3 — needed for archetype eligibility |
| `coach_soul.json` | Internal | From `ccf-init` (Genesis Phase 0) |
| LIWC-22 scoring | License | Weekly feedback loop reads authenticity scores |
| Receipt Chain Guard | Infrastructure | Receipts at INGEST + VALIDATE |

---

## Testing Strategy

### Unit Tests
- **Trigger identification:** 3 synthetic transcripts with known activation passages (markers present/absent) → validate detection rate
- **AKB classification:** 6 synthetic passages (2 ESK, 2 GE, 2 LP) → validate correct level classification
- **PTG classification:** 3 synthetic transcripts (resolved, active, raw) → validate correct status assignment + raw exclusion
- **Reconsolidation sensitivity:** 3 synthetic triggers with known V1 values → validate scoring + cross-validation flag on incoherence
- **Precedence update:** Synthetic `activation_history` arrays with 3 entries → validate climb/hold/fall/dormant logic

### Integration Tests
- **Full Genesis build:** Run FR4 → FR5 on a real coach transcript. Validate: trigger map contains ≥2 `resolved_dual_layer` triggers, all have moral foundation mapping, all have evidence passages.
- **Weekly feedback loop:** Simulate 3 weekly sessions with synthetic LIWC-22 scores. Validate: `activation_history` entries written, precedence updated correctly.
- **Backward compatibility:** Start weekly pipeline with no `trigger_map.json`. Validate: legacy DARN-CAT questions generated, no errors, downstream phases complete.

### Safety Tests
- **PTG gate:** Insert a `raw_unresolved` trigger into `trigger_map.json`. Run weekly pipeline. Validate: trigger NEVER selected by intelligence radar. No activation event designed for it.
- **Dormant trigger protection:** Mark a trigger as `dormant`. Validate: intelligence radar does not select it. Trigger entry persists (not deleted). Re-interview scheduling triggered.
