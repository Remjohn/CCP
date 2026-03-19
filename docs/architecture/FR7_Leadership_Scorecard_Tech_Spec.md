# Tech-Spec: FR7 — Leadership Scorecard & Coach Development Engine

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §6.3 (Governance Ministers — Minister of Identity), §11.6 (Leadership Trait Governance), §5.3 (Genesis Pipeline Phase 0.5), §12.1 (Build Sequence Step 2)
**Skill Implementation:** NEW — `skills/ccf/setup/leadership-scorecard/SKILL.md` (to be created)
**MCDA Reference:** [MCDA_Leadership_Trait_Architecture.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/MCDA_Leadership_Trait_Architecture.md)

---

## Overview

### Problem Statement

Content factories produce content. They do not develop the person producing it. A coach who generates 36 scripts per week through the CCF pipeline receives content that sounds like them — but if the content assignments are random with respect to the coach's leadership profile, the coach's development is accidental. Strong traits get no showcase. Weak traits get no exercise. The coach produces competent content without growing as a leader.

The Leadership Scorecard inverts this: it maps each coach across 12 irreducible leadership traits, identifies where they are strong and where they are weak, and uses that map to govern content format assignment. Weak traits are assigned formats that exercise and develop them. Strong traits are assigned formats that showcase the coach's natural authority. Every weekly production session becomes a deliberate act of leadership development — not just content generation.

This is also the production lock gate. The CCP will not generate content for a coach who has not been scored. A coach without a Leadership Scorecard is a coach whose content assignments have no developmental intelligence — and a platform that generates undirected content at scale is indistinguishable from a template factory.

### Solution

The Minister of Identity — an embedded inference-time evaluation agent (§6.3) — operates at Phase 0.5 of the Genesis Pipeline (after all extraction is complete, before production unlocks). It reads the coach's Voice DNA (`coach_soul.json`), TTT baseline (`ttt_baseline.json`), and Tribe Soul (`tribe_soul.json`) to score 12 Leadership Traits. Each trait receives a signal-strength score (1–10) with evidence citations. The resulting `leadership_scorecard.json` is then consumed by the format assignment engine (`ccf-eroll-plan`) to weight which archetypes exercise weak traits and which showcase strong traits.

The Minister of Identity is **read-only** with respect to content — it scores and annotates, never rewrites. A minister veto halts the pipeline at the checkpoint, resumable only after coach input.

### Scope

**In scope:**
- The 12 Leadership Trait model with signal sources and scoring methodology
- `leadership_scorecard.json` schema (DEP-ENG-026)
- Signal extraction from `coach_soul.json`, `ttt_baseline.json`, `tribe_soul.json`
- Scoring pipeline (I-R-E-V-C protocol)
- Production lock gate (hard code-level enforcement)
- Format governance rules (weak → exercise, strong → showcase)
- Weekly scorecard evolution (trait scores update based on content performance)
- Acceptance criteria and testing strategy

**Out of scope:**
- Voice DNA extraction mechanics (FR3 — prerequisite, produces signal sources)
- Tribe Soul extraction mechanics (FR6 — prerequisite)
- Archetype assignment mechanics (`ccf-eroll-plan` — downstream consumer)
- Content generation pipeline (FR1 — downstream consumer)
- CBCS trait development tracking (Phase 2 feature)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-026` | Leadership Scorecard | PRIMARY OUTPUT — the 12-trait map |
| `DEP-ENG-003` | Positive Space (Voice DNA) | SIGNAL SOURCE — vocal authority markers, confidence patterns, storytelling rhythms |
| `DEP-ENG-004` | Negative Space | SIGNAL SOURCE — vulnerability markers, hedging patterns, avoidance zones |
| `DEP-ENG-005` | TTT Baseline | SIGNAL SOURCE — temperature range, tone consistency, temperament ceiling |
| `DEP-LIB-001` | Emotional DNA Profile | SIGNAL SOURCE — trigger specificity, appraisal architecture, moral foundation weighting |
| `DEP-ENG-001` | Tribe Soul | SIGNAL SOURCE — audience understanding depth, polarization patterns, enemy naming clarity |
| `DEP-ENG-023` | Cultural Memory Map | SIGNAL SOURCE — cultural grounding depth (7 CMM layers) |
| `DEP-ENG-024` | Coach Story Archive | SIGNAL SOURCE — narrative capability, transformation proof, archetypal storytelling |

### The 12 Leadership Traits (MCDA First-Principles Decomposition)

| # | Trait | Why It Creates Followers | Architectural Strength |
|---|---|---|---|
| 1 | **Deep Empathy** | Precondition for trust — leader who feels what the tribe feels before they say it | Strong |
| 2 | **Authentic Vulnerability** | Costly signal — vulnerability is socially expensive, making it trustworthy | Strong |
| 3 | **Embodied Confidence** | Authority that lives in the body (vocal tonality, pacing, word choice), not just the argument | Strong |
| 4 | **Emotional Depth** | Capacity to articulate emotions beneath the obvious ones — content that is kept, not just consumed | Strong |
| 5 | **Devotional Passion** | The fire that proves this is not just a job — cannot be manufactured, only amplified | Medium-High |
| 6 | **Mystique & Aura** | Strategic management of revelation — sense that this person knows something you don't | Medium |
| 7 | **Archetypal Storytelling** | Weaving personal experience into universal narrative — storytelling as meaning-making technology | Strongest |
| 8 | **Transformation Proof** | Evidence that the method works — before/after, testimonials, documented journeys | Strong |
| 9 | **Polarizing Clarity** | Willingness to draw a line and lose the wrong people — gravitational force for tribe binding | Strong |
| 10 | **Expansion Energy** | Being near this person makes you bigger — audience feels enlarged, not extracted from | Medium-High |
| 11 | **Comic Honesty** | Hard truths told through humor — the Trojan horse of truth | Weak |
| 12 | **Directness** | Saying what needs to be said without decoration — radical in a world of hedged statements | Strong |

### Signal Sources per Trait

| Trait | Primary Signal Source | What to Extract | Secondary Source |
|---|---|---|---|
| **Deep Empathy** | `tribe_soul.json` | L1/L2/L3 depth coverage in tribe understanding. Does coach demonstrate awareness of L3 (unspoken) audience pain? | `coach_soul.json` — presence of tribe-referencing language in voice notes |
| **Authentic Vulnerability** | `coach_soul.json` (DEP-ENG-004 Negative Space) | Hedging patterns, avoidance zones, emotional markers (voice cracks, speed changes). A coach with rich Negative Space data IS vulnerably authentic. | Sacred Audio emotional charge flags |
| **Embodied Confidence** | `ttt_baseline.json` (DEP-ENG-005) | TTT ceiling, consistency across recordings, temperature range breadth. A coach whose TTT ceiling is TTT-08+ with <15% drift has embodied confidence. | `coach_soul.json` — vocal authority markers |
| **Emotional Depth** | `coach_soul.json` (DEP-ENG-003 + DEP-ENG-004) | Linguistic complexity in emotional passages. Use of metaphor, narrative layering, sub-surface emotion naming (grief beneath anger, fear beneath ambition). | LIWC-22 emotional tone distribution |
| **Devotional Passion** | `coach_soul.json` | Emotional intensity markers in voice. Frequency of unprompted expansion (coach goes deeper than asked). Volume of Sacred Audio beyond minimum. | Interview corpus — does coach discuss craft with fire? |
| **Mystique & Aura** | Content Pillar scope vs. revealed scope | Breadth of knowledge territory mapped in pillars vs. what the coach has shared publicly. Wide territory = high mystique potential. | `coach_soul.json` — strategic withholding patterns |
| **Archetypal Storytelling** | `DEP-ENG-024` (Coach Story Archive) | Number and quality of structured stories. Hartian 5-element schema completion. Arc diversity (redemption/contamination/mixed). | Voice DNA narrative rhythm patterns |
| **Transformation Proof** | `DEP-ENG-024` + CBCS performance data (if available) | Client transformation testimonials, documented before/after evidence, specific measurable outcomes cited. | Interview corpus — does coach cite specific results? |
| **Polarizing Clarity** | `tribe_soul.json` | Specificity of enemy naming. Does the tribe profile contain named enemies with mechanism description (not abstract "the system")? | `coach_soul.json` — does coach use definitive language or hedge? |
| **Expansion Energy** | `coach_soul.json` + `tribe_soul.json` | Generosity markers: does the coach give away key insights freely? Does content aim to reduce dependency? | Philosophy brief — explicit growth vs. dependency stance |
| **Comic Honesty** | `coach_soul.json` | Humor markers in voice notes: irony, self-deprecation, comedic timing, comedic subversion. LIWC-22 humor category scores. | Tribe humor profile (from FR6) — is coach's humor aligned with tribe's? |
| **Directness** | `coach_soul.json` (DEP-ENG-003 Positive Space) | Low hedging language. Short declarative sentences. Absence of qualifiers ("sort of", "kind of", "maybe"). Chen AI-detection score (low = human directness). | TTT temperature ceiling — high temperature coaches tend to be more direct |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **12 traits scored independently, not composited** | Each trait is an irreducible dimension. A composite score (averaging all 12) would hide the exercise/showcase information that makes the scorecard useful. A coach who scores 9/10 on Directness and 3/10 on Comic Honesty needs format assignments that DIFFER for those traits, not an average of 6. |
| **Minister of Identity is inference-time, not training-time** | The minister evaluates at a specific checkpoint using the extraction data already produced. It does not require a training loop — it reads the existing DEP objects and scores against defined rubrics. |
| **Production lock as code-level gate, not prompt instruction** | A prompt instruction ("don't generate without the scorecard") is bypassable. A code-level check in Morgan's orchestrator that returns `PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD` is not. |
| **Weak traits ≠ bad traits** | A trait scored 3/10 does not mean the coach fails. It means the content format assignments for THAT trait should prioritize exercise formats (e.g., assign Storytelling formats to a coach weak in Archetypal Storytelling). The scorecard is developmental, not evaluative. |
| **Scores evolve weekly** | After each production session, content performance data feeds back into the scorecard. A coach whose exercise-format content for a weak trait consistently performs well → trait score climbs. The scorecard tracks growth, not just baseline. |
| **Two architectural gaps are features** | Devotional Passion and Comic Honesty are the two traits where the system CANNOT substitute for the coach. This is the defensibility moat: coaches who lack genuine passion or humor will be exposed, not saved, by the system's amplification. |

---

## Implementation Plan

### Prerequisite Gate

**Condition:** ALL of the following must exist before the Minister of Identity can score:
- `coach_soul.json` with DEP-ENG-003 (Positive Space) + DEP-ENG-004 (Negative Space) + DEP-LIB-001 (Emotional DNA)
- `ttt_baseline.json` (DEP-ENG-005)
- `tribe_soul.json` (DEP-ENG-001)

If any are missing → `CANNOT_SCORE_MISSING_DEPENDENCIES` error with list of missing objects.

**Optional enrichments (improve scoring but not required):**
- `DEP-ENG-023` (Cultural Memory Map) — improves Cultural Grounding score
- `DEP-ENG-024` (Coach Story Archive) — improves Archetypal Storytelling and Transformation Proof scores
- Philosophy Brief — improves Expansion Energy score

---

### Phase 1: INGEST

**Agent:** Minister of Identity (Sophia-Identity variant)
**Checkpoint:** Post-Genesis (Phase 0.5) — after all extraction, before production

**Steps:**
1. Load `coach_soul.json` — verify DEP-ENG-003, DEP-ENG-004, DEP-LIB-001 populated
2. Load `ttt_baseline.json` — verify TTT profile exists
3. Load `tribe_soul.json` — verify DEP-ENG-001 populated
4. Load `cultural_memory_map` (Supabase) — if exists, enriches scoring (optional)
5. Load `coach_story_archive` (Supabase) — if exists, enriches scoring (optional)
6. Load Philosophy Brief (if exists) — enriches scoring (optional)
7. **Receipt Write (Phase 1):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-LEADERSHIP-INGEST",
  "previous_receipt_hash": "{ALL_REQUIRED_DEP_HASHES}",
  "input_payload_hash": "{COACH_SOUL_TTT_TRIBE_HASH}",
  "output_payload_hash": "{NULL_SCORECARD_TEMPLATE_HASH}",
  "stage_name": "LEADERSHIP-SCORECARD-INGEST",
  "agent_name": "Minister of Identity",
  "timestamp": "{ISO8601}" }
```

---

### Phase 2: SCORE — 12 Trait Evaluation

For each of the 12 traits, the Minister evaluates signal evidence and assigns a score:

#### Trait 1: Deep Empathy (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| L1/L2/L3 depth coverage | `tribe_soul.json` | L3 ≥10% → +3. L2 ≥30% → +2. L1 only → 0 |
| Audience emotional references in voice | `coach_soul.json` | ≥5 tribe-referencing emotional passages → +2 |
| Mode coverage (T/V/R) | `tribe_soul.json` | All 3 modes covered with ≥3 triggers each → +2 |
| Empathy language markers | LIWC-22 from Sacred Audio | Social referencing words above 50th percentile → +1 |

#### Trait 2: Authentic Vulnerability (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Negative Space richness | DEP-ENG-004 | ≥5 documented avoidance zones → +3 |
| Emotional charge markers | Sacred Audio | ≥3 voice cracks/pauses/speed changes flagged → +3 |
| Hedging language in emotional passages | `coach_soul.json` | Low hedging → +2 (coach doesn't soften vulnerability) |
| Self-referential depth | LIWC-22 | High I-word frequency in vulnerability passages → +2 |

#### Trait 3: Embodied Confidence (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| TTT ceiling | `ttt_baseline.json` | TTT-08+ → +3. TTT-06/07 → +2. TTT-05 or below → +1 |
| TTT consistency (drift) | `ttt_baseline.json` | Drift <10% → +3. <15% → +2. ≥15% → +1 |
| Temperature range breadth | `ttt_baseline.json` | Can credibly operate across ≥4 TTT levels → +2 |
| Vocal authority markers | DEP-ENG-003 | Strong declarative rhythms, low uptalk → +2 |

#### Trait 4: Emotional Depth (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Metaphor density | DEP-ENG-003 + DEP-ENG-004 | ≥3 original metaphors in voice corpus → +3 |
| Sub-surface emotion naming | `coach_soul.json` | Names 2+ emotions beneath surface emotion → +3 |
| Linguistic complexity in emotional passages | LIWC-22 | Cognitive complexity score above 60th percentile → +2 |
| Narrative layering | Voice DNA narrative patterns | Multi-layer narrative structure detected → +2 |

#### Trait 5: Devotional Passion (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Emotional intensity markers | Sacred Audio | Peak emotional intensity ≥80th percentile → +3 |
| Unprompted expansion | Interview corpus | Coach expands beyond question scope ≥3 times → +2 |
| Sacred Audio volume | `config.yaml` | Submitted words significantly exceed 3,000 minimum → +2 |
| Craft discussion fire | `coach_soul.json` | Evidence of intrinsic motivation language (LIWC: achievement + positive emotion) → +3 |

#### Trait 6: Mystique & Aura (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Content Pillar breadth | Pillar document | ≥7 content territories mapped → +3 |
| Strategic withholding | `coach_soul.json` | Coach implies deeper knowledge without revealing it ≥2 times → +2 |
| Knowledge territory ratio | Pillars vs. public sharing | Wide gap between known territory and revealed territory → +3 |
| Information gap creation | Voice DNA patterns | Uses open-loop language ("there's more to this but let me focus on...") → +2 |

#### Trait 7: Archetypal Storytelling (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Story count | DEP-ENG-024 (Story Archive) | ≥5 structured stories → +2. ≥10 → +3 |
| Hartian 5-element completion | DEP-ENG-024 | All 5 elements present in ≥3 stories → +3 |
| Arc diversity | DEP-ENG-024 | Both redemption AND contamination sequences present → +2 |
| Narrative rhythm | DEP-ENG-003 | Natural story cadence detected in Voice DNA → +2 |

#### Trait 8: Transformation Proof (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Client transformation stories | DEP-ENG-024 | ≥2 documented client transformations with specific outcomes → +3 |
| Measurable outcomes cited | Interview corpus | Coach cites specific numbers/metrics → +3 |
| Before/after evidence | Story Archive | ≥1 clear before/after journey → +2 |
| CBCS tracking data | CBCS (if available) | Active client tracking with documented progress → +2 |

#### Trait 9: Polarizing Clarity (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Enemy naming specificity | `tribe_soul.json` | Named enemies with mechanism descriptions (not abstract) → +3 |
| Definitive language | DEP-ENG-003 (Positive Space) | Low qualification markers, strong declarative style → +2 |
| Position staking | Voice DNA | Coach takes unambiguous positions ≥3 times in corpus → +3 |
| Tribal alignment pattern | `tribe_soul.json` | Clear in-group/out-group boundary articulated → +2 |

#### Trait 10: Expansion Energy (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Generosity markers | `coach_soul.json` | Coach gives away key insights (not hoarding) → +3 |
| Growth vs. dependency stance | Philosophy Brief | Explicit commitment to audience independence → +3 |
| Empowerment language | LIWC-22 | Achievement + power language directed OUTWARD (toward audience) → +2 |
| Teaching frame | Voice DNA | Instructional generosity — explains "how" not just "what" → +2 |

#### Trait 11: Comic Honesty (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Humor markers in voice | `coach_soul.json` | Self-deprecation, ironic framing, comedic timing detected → +3 |
| LIWC-22 humor category | Sacred Audio LIWC | Humor word frequency above 50th percentile → +2 |
| Tribe humor alignment | Tribe profile humor DNA | Coach humor style matches tribe's dominant humor style → +3 |
| Strategic truth deployment | Voice corpus | Uses humor to deliver uncomfortable truths ≥1 time → +2 |

> **Note:** This is the system's weakest trait-servicing capability. Scores below 4/10 are expected and normal — the gap is a feature, not a flaw. Coaches must bring genuine humor; the system formats and distributes but cannot originate comedy.

#### Trait 12: Directness (1–10)

| Signal | Source | Scoring Rubric |
|---|---|---|
| Low hedging language | DEP-ENG-003 | Absence of "sort of", "kind of", "maybe" in declarative passages → +3 |
| Sentence brevity | Voice DNA | Mean sentence length in declarative passages below corpus median → +2 |
| Chen AI-detection score | FR3 validation | Low AI detection = high human directness → +3 |
| TTT temperature consistency | `ttt_baseline.json` | High-temperature coaches (TTT-07+) with consistency → +2 |

---

### Phase 3: CATEGORIZE — 5 Trait Categories (Architecture §11.6)

After individual scoring, traits are grouped into 5 coverage categories for the production lock gate:

| Category | Traits | DEP Source | Coverage Requirement |
|---|---|---|---|
| **Core Philosophy** | Devotional Passion, Expansion Energy | DEP-ENG-001 (Transformation Blueprint) | At least 1 trait ≥ 4/10 |
| **Audience Understanding** | Deep Empathy, Polarizing Clarity | DEP-ENG-002 (Avatar) + DEP-ENG-007 (Tribe Intelligence) | At least 1 trait ≥ 5/10 with L1/L2/L3 depth |
| **Voice Authenticity** | Authentic Vulnerability, Embodied Confidence, Directness | DEP-ENG-003 + DEP-ENG-004 | At least 2 traits ≥ 5/10 |
| **Teaching Method** | Emotional Depth, Archetypal Storytelling, Transformation Proof | DEP-ENG-005 (TTT) | At least 1 trait ≥ 5/10 covering all 3 T/V/R modes |
| **Cultural Grounding** | Mystique & Aura, Comic Honesty | DEP-ENG-023 (Cultural Memory Map) | Minimum 4 of 7 CMM layers populated |

**Production lock gate:** ALL 5 categories must meet their coverage requirement. If ANY category fails → `PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD` with specific category failure message.

---

### Phase 4: FORMAT GOVERNANCE — Exercise/Showcase Assignment

Once scored, the scorecard governs the `ccf-eroll-plan` format assignment (Emmanuel's 36-format weekly allocation):

**Exercise Assignment (weak traits, score ≤ 5/10):**

| Weak Trait | Assigned Archetype Family | Why This Exercises the Trait |
|---|---|---|
| Deep Empathy | `story_recognition` / `tweet_recognition` | Forces coach to address audience's L3 reality directly |
| Authentic Vulnerability | `story_transformation` / `myth_fear_anxiety` | Requires personal vulnerability disclosure |
| Embodied Confidence | `tier_list_controversial` / `myth_indignation` | Demands high-temperature conviction |
| Emotional Depth | `comparison_profound` / `story_transformation` | Requires sub-surface emotional articulation |
| Devotional Passion | `myth_empowering` / `tweet_conviction` | Channels intrinsic fire into public format |
| Mystique & Aura | `reaction_surprising` / `comparison_conceptual` | Reveals depth while maintaining withholding |
| Archetypal Storytelling | `story_transformation` / `story_recognition` | Explicitly narrative-structured formats |
| Transformation Proof | `listicle_helpful` / `comparison_outrageous` | Requires evidence-based content |
| Polarizing Clarity | `myth_indignation` / `tier_list_controversial` | Demands position-staking and enemy naming |
| Expansion Energy | `listicle_helpful` / `tweet_wisdom` | Channels generosity and empowerment |
| Comic Honesty | `reaction_funny` / `tweet_recognition` (with humor directive) | Creates safe space for comedic attempts |
| Directness | `tweet_warning` / `myth_indignation` | Short-form demanding unhedged language |

**Showcase Assignment (strong traits, score ≥ 7/10):**

| Strong Trait | Assigned Archetype Family | Why This Showcases the Trait |
|---|---|---|
| Deep Empathy | `story_recognition` / `myth_fear_anxiety` | Coach's natural empathy amplified |
| Authentic Vulnerability | `story_transformation` | Coach's vulnerability becomes signature content |
| Embodied Confidence | `myth_indignation` / `tier_list_controversial` | Coach's authority positioned at its maximum |
| Emotional Depth | `comparison_profound` / `story_transformation` | Coach's depth becomes their brand differentiator |
| Devotional Passion | `myth_empowering` / `tweet_conviction` | Coach's fire is the content |
| Mystique & Aura | `reaction_surprising` / `comparison_shocking` | Strategic revelation pacing |
| Archetypal Storytelling | All story formats | Coach is a natural storyteller — give them the stage |
| Transformation Proof | `listicle_shocking` / `comparison_outrageous` | Hard proof positions the coach as results-backed |
| Polarizing Clarity | `myth_indignation` / `tier_list_controversial` | Coach's line-drawing becomes movement-defining |
| Expansion Energy | `listicle_helpful` / `tweet_wisdom` | Coach's generosity attracts the right tribe |
| Comic Honesty | `reaction_funny` / `tweet_recognition` | Coach's humor becomes their signature weapon |
| Directness | `tweet_warning` / `myth_indignation` | Coach's directness cuts through noise |

**Weighting formula:**
- Weekly allocation of 36 formats: **60% showcase** (strong traits drive content authority), **40% exercise** (weak traits receive development reps)
- Within exercise allocation: traits with lowest scores get highest format weight
- Format assignments written to `02_content_strategy.md` with trait-to-format mapping

---

### Phase 5: EMIT

Write populated `leadership_scorecard.json`:

```json
{
  "dep_id": "DEP-ENG-026",
  "version": "1.0",
  "coach_id": "",
  "scored_at": "ISO8601",
  "last_updated": "ISO8601",
  "signal_sources": {
    "coach_soul": true,
    "ttt_baseline": true,
    "tribe_soul": true,
    "cultural_memory_map": false,
    "coach_story_archive": false,
    "philosophy_brief": false
  },
  "traits": [
    {
      "trait_id": 1,
      "name": "deep_empathy",
      "label": "Deep Empathy",
      "score": 0,
      "max_score": 10,
      "evidence": [],
      "category": "audience_understanding",
      "format_assignment": "exercise|showcase|neutral",
      "exercise_archetypes": [],
      "showcase_archetypes": [],
      "history": []
    }
  ],
  "categories": {
    "core_philosophy": {
      "traits": ["devotional_passion", "expansion_energy"],
      "coverage_met": false,
      "threshold": "At least 1 trait ≥ 4/10"
    },
    "audience_understanding": {
      "traits": ["deep_empathy", "polarizing_clarity"],
      "coverage_met": false,
      "threshold": "At least 1 trait ≥ 5/10 with L1/L2/L3 depth"
    },
    "voice_authenticity": {
      "traits": ["authentic_vulnerability", "embodied_confidence", "directness"],
      "coverage_met": false,
      "threshold": "At least 2 traits ≥ 5/10"
    },
    "teaching_method": {
      "traits": ["emotional_depth", "archetypal_storytelling", "transformation_proof"],
      "coverage_met": false,
      "threshold": "At least 1 trait ≥ 5/10 covering all 3 T/V/R modes"
    },
    "cultural_grounding": {
      "traits": ["mystique_and_aura", "comic_honesty"],
      "coverage_met": false,
      "threshold": "Minimum 4 of 7 CMM layers populated"
    }
  },
  "production_lock": {
    "all_categories_met": false,
    "locked_categories": [],
    "unlock_message": ""
  },
  "format_governance": {
    "showcase_ratio": 0.6,
    "exercise_ratio": 0.4,
    "assignments_written_to": "02_content_strategy.md"
  }
}
```

---

### Phase 6: VALIDATE & PRODUCTION LOCK GATE

**Validation checks:**
- [ ] All 12 traits have a score between 1 and 10
- [ ] Every score has ≥1 evidence citation from the signal sources
- [ ] All 5 trait categories evaluated for coverage
- [ ] If any category fails coverage → `production_lock.locked_categories` lists the failing category with message

**Production lock enforcement (CODE-LEVEL — Morgan orchestrator):**
```
IF leadership_scorecard.json does NOT exist:
  RETURN PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD
  
IF ANY category in categories has coverage_met = false:
  RETURN PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: {category_name}
  MESSAGE: "The coach needs additional [category] evidence before production can begin.
            Options: (1) Additional Sacred Audio session, (2) Deeper tribe research,
            (3) Story Archive enrichment"
            
ELSE:
  production_lock.all_categories_met = true
  UNLOCK production pipeline
```

**Checkpoint:**
- Update `config.yaml`: `sessions.setup.leadership_score.status = "complete"`
- Update `coach_soul.json`: `pipeline_status.leadership_scored = true`
- **Receipt Write (Phase 6):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-LEADERSHIP-COMPLETE",
  "previous_receipt_hash": "{PHASE_1_RECEIPT_HASH}",
  "input_payload_hash": "{SCORED_TRAITS_HASH}",
  "output_payload_hash": "{FINAL_SCORECARD_JSON_HASH}",
  "stage_name": "LEADERSHIP-SCORECARD-COMPLETE",
  "agent_name": "Minister of Identity",
  "timestamp": "{ISO8601}" }
```
- Write format governance to `02_content_strategy.md`

---

## Weekly Scorecard Evolution

> **This is NOT part of Genesis setup. This runs after each weekly production session.**

### Trigger

After `ccf-validate` completes (all 36 scripts pass Sophia + Marcus + Chen), the pipeline updates `leadership_scorecard.json`.

### Evolution Data

For each week's content production:

```json
{
  "session_id": "weekly_session_2026-W12",
  "trait_updates": [
    {
      "trait_id": 1,
      "name": "deep_empathy",
      "formats_assigned": ["story_recognition", "tweet_recognition"],
      "assignment_type": "exercise",
      "content_performance": {
        "sophia_alignment": 0.0,
        "chen_detection": 0.0,
        "audience_engagement_7d": null
      }
    }
  ]
}
```

### Score Evolution Logic

After ≥3 weekly sessions with exercise assignments for a trait:

| Pattern | Score Action |
|---|---|
| Exercise content consistently passes Sophia alignment ≥85% AND engagement metrics above coach average | **Climb** — trait score increases by +1 (max 10). Coach is developing this trait through practice. |
| Exercise content passes validation but engagement below average | **Hold** — no change. Coach is practicing but audience hasn't responded yet. |
| Exercise content consistently fails Sophia validation OR Chen detection high | **Decline** — trait score decreases by -1 (min 1). Coach may be forcing this trait unnaturally. Reduce exercise allocation, increase alternative trait exercise. |

### Quarterly Rescoring

Every 12 weeks, the Minister of Identity performs a full rescore using the LATEST `coach_soul.json` (which may have been updated if the coach submitted new Sacred Audio). This catches genuine coach development that occurred outside the content pipeline (e.g., new testimonials, deeper tribe understanding from CBCS interactions, public speaking growth).

---

## Backward Compatibility

**Condition:** `leadership_scorecard.json` does not exist.

**Behavior:** Production pipeline is LOCKED. The system returns `PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD` from Morgan's orchestrator. There is no fallback — the scorecard is required.

**Rationale:** Unlike the Trigger Map (FR5) or Context Premise Map (FR6) which have legacy DARN-CAT fallbacks, the Leadership Scorecard has no degraded mode. Content produced without format governance is undirected — the coach receives no developmental benefit from production. The entire value proposition of the Coach Development Engine depends on scored format assignment.

---

## Tasks

- [ ] **Task 1:** Create `skills/ccf/setup/leadership-scorecard/SKILL.md` — Minister of Identity skill definition with I-R-E-V-C protocol
- [ ] **Task 2:** Implement INGEST phase — load and verify all 3 required DEP objects + 3 optional enrichments
- [ ] **Task 3:** Implement 12-trait scoring engine — signal extraction from each DEP source per trait rubric
- [ ] **Task 4:** Implement Deep Empathy scoring (Trait 1) — L1/L2/L3 depth analysis + audience emotional references + mode coverage
- [ ] **Task 5:** Implement Authentic Vulnerability scoring (Trait 2) — Negative Space richness + emotional charge markers + hedging analysis
- [ ] **Task 6:** Implement Embodied Confidence scoring (Trait 3) — TTT ceiling + drift + range + vocal authority
- [ ] **Task 7:** Implement Emotional Depth + Devotional Passion + Mystique scoring (Traits 4–6) — metaphor density, intensity markers, knowledge territory ratio
- [ ] **Task 8:** Implement Archetypal Storytelling + Transformation Proof scoring (Traits 7–8) — Story Archive analysis, Hartian schema completion, measureable outcomes
- [ ] **Task 9:** Implement Polarizing Clarity + Expansion Energy + Comic Honesty + Directness scoring (Traits 9–12) — enemy naming, generosity markers, humor markers, hedging language
- [ ] **Task 10:** Implement 5-category coverage evaluation — aggregate trait scores into categories, evaluate coverage requirements
- [ ] **Task 11:** Implement production lock gate — code-level enforcement in Morgan orchestrator (not prompt instruction)
- [ ] **Task 12:** Implement format governance engine — exercise/showcase assignment per trait, 60/40 weighting, write to `02_content_strategy.md`
- [ ] **Task 13:** Implement weekly scorecard evolution — `activation_history` entries, climb/hold/decline logic
- [ ] **Task 14:** Implement quarterly rescoring trigger — full 12-trait rescore from updated DEP objects

---

## Acceptance Criteria

- [ ] **AC1 (Production Lock — Missing Scorecard):** Triggering `ccf-batch` without `leadership_scorecard.json` → returns `PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD`. Not a prompt failure — a code-level gate in Morgan's orchestrator.
- [ ] **AC2 (Production Lock — Category Failure):** A coach with all 12 traits scored but Core Philosophy category failing (Devotional Passion = 2/10, Expansion Energy = 3/10) → returns `PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: core_philosophy`.
- [ ] **AC3 (Evidence Requirement):** Every trait score has ≥1 evidence citation. A trait scored 7/10 with zero evidence citations → validation error.
- [ ] **AC4 (Format Governance — Exercise):** A coach with Deep Empathy = 3/10 → the weekly format allocation contains ≥2 empathy-exercise archetypes (`story_recognition` or `tweet_recognition`).
- [ ] **AC5 (Format Governance — Showcase):** A coach with Archetypal Storytelling = 9/10 → the weekly format allocation contains high-weight story formats.
- [ ] **AC6 (Format Ratio):** Weekly allocation is approximately 60% showcase / 40% exercise. A production run with 100% showcase or 100% exercise → rejected by Emmanuel's format governance validator.
- [ ] **AC7 (Weekly Evolution):** After 3 consecutive weeks where exercise content for Embodied Confidence passes Sophia ≥85% AND audience engagement above coach average → `embodied_confidence` score increases by +1.
- [ ] **AC8 (Score Bounds):** No trait can score below 1 or above 10. A score evolution that would push below 1 → stays at 1. Above 10 → stays at 10.
- [ ] **AC9 (Prerequisite Gate):** Minister of Identity activated without `ttt_baseline.json` → returns `CANNOT_SCORE_MISSING_DEPENDENCIES: ttt_baseline.json`.
- [ ] **AC10 (Minister Read-Only):** The Minister of Identity scores and annotates. It never modifies `coach_soul.json`, `ttt_baseline.json`, or `tribe_soul.json`. Verification: read/write audit shows zero write operations to any DEP source.
- [ ] **AC11 (Comic Honesty Expectation):** A coach scoring 2/10 on Comic Honesty → this does NOT trigger production lock (Comic Honesty is in the Cultural Grounding category which checks CMM layers, not individual trait scores). System acknowledges the gap as architectural and assigns light exercise formats.
- [ ] **AC12 (Quarterly Rescore):** After 12 weeks, a rescore using updated `coach_soul.json` (new Sacred Audio) produces different scores than the Genesis baseline for at least 1 trait.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR3 Voice DNA Extraction | Internal prerequisite | Produces `coach_soul.json` + `ttt_baseline.json` |
| FR6 Tribe Profile | Internal prerequisite | Produces `tribe_soul.json` |
| FR1 Genesis Pipeline Phase 0, Step 7.5 | Internal | Orchestration context — Morgan coordinates scorecard timing |
| `ccf-eroll-plan` (Emmanuel) | Downstream consumer | Reads scorecard for format assignment weighting |
| LIWC-22 scoring | License | Used for signal extraction on Sacred Audio |
| Receipt Chain Guard | Infrastructure | Receipt at INGEST + VALIDATE |

---

## Testing Strategy

### Unit Tests
- **Trait scoring:** 12 synthetic coaches, each with one trait deliberately high (rich evidence) and one deliberately low (sparse evidence) → validate correct scoring for each trait
- **Category coverage:** 5 synthetic scorecard configurations, each with one category failing → validate correct `PRODUCTION_LOCKED_CATEGORY_INCOMPLETE` error for each
- **Format governance:** Synthetic scorecard with known scores → validate exercise/showcase assignments match expected archetype families
- **Score bounds:** Synthetic evolution data pushing a trait to 11 → validate capped at 10. Pushing to 0 → validate floored at 1
- **Missing dependencies:** Attempt to score without `ttt_baseline.json` → validate `CANNOT_SCORE_MISSING_DEPENDENCIES`

### Integration Tests
- **Full Genesis flow:** Run FR2 → FR3 → FR6 → FR7 on a real coach. Validate: `leadership_scorecard.json` exists, all 12 traits scored, all 5 categories evaluated, production lock resolved
- **Format assignment propagation:** After scorecard creation, run `ccf-eroll-plan` → validate: format assignments in `02_content_strategy.md` reflect scorecard weighting (weak traits get exercise formats)
- **Weekly evolution:** Simulate 3 weekly sessions with synthetic performance data → validate: trait scores update correctly per climb/hold/decline logic

### Safety Tests
- **Minister read-only:** Run full scoring pipeline → verify zero write operations to any source DEP object (coach_soul, ttt_baseline, tribe_soul)
- **Production lock enforcement:** Attempt to run `ccf-batch` with a deliberately incomplete scorecard → verify Morgan blocks at code level, not prompt level
