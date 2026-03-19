# Tech-Spec: FR6 — Tribe Profile & L1/L2/L3-Stratified Context Premise Map

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §Layer 2 (MEMORY — Neo4j HGM), §5.2 (Corrected Intake Flow — Tribe Extraction), §Context_Premise_Trigger_Matching_Layer
**Skill Implementations:** `skills/ccf/setup/tribe-soul-extraction/SKILL.md`, `skills/ccf/distillation/tribe-distiller/SKILL.md`

---

## Overview

### Problem Statement

The Trigger-First Engine solves the coach side of the content equation: what permanently fires this coach, and how to activate it authentically. But content that carries the coach's authentic fire and lands in the wrong room — the audience's psychological territory that doesn't match the coach's trigger architecture — produces neural comprehension without neural coupling (Hasson 2005). The audience processes the content. They do not inhabit it.

The audience side requires an equivalent depth of structural intelligence: not what the audience says they want (L1 — public statements), not what they struggle with privately (L2 — communal disclosure), but what they will not say out loud but feel deeply (L3 — unspoken, visceral, 2am-test-verified experience). Only L3 data provides the structural ground from which the Trigger Matching Layer can identify four-axis congruence between the coach's trigger origin and the audience's current reality (Clark & Brennan Common Ground Theory: structural L3 ground is the only level that produces deep neural coupling).

The legacy system treated audience intelligence as demographic profiling with pain-point lists. The result: content relevant to the topic, not the territory. Professional empathy, not structural recognition. The Tribe Profile and Context Premise Map replace this with a 12-dimensional psychological map of the audience's internal worldview, depth-stratified across L1/L2/L3, stored as a graph ontology in Neo4j, completely isolated per coach, serving as the foundational reality for every downstream content generation decision.

### Solution

A two-stage extraction pipeline:

1. **Stage A — Tribe Soul Extraction (Genesis Setup):** The Audience Empathy Agent conducts digital ethnography across the coach's audience spaces, producing a high-volume verbatim corpus. The `tribe-soul-extraction/` skill processes this corpus into a structured `tribe_profile.json` covering cultural artifacts, humor DNA, emotional resonance, visual recognition codes, and in-group language — governed by the 4 Laws of Tribe Profile Distillation.

2. **Stage B — Context Premise Distillation (Distillation Phase):** The `tribe-distiller/` skill transforms the raw tribe profile into a depth-stratified Context Premise Map (DEP-ENG-006), mode-mapping every insight to T/V/R emotional modes, classifying every entry to L1/L2/L3 depth, and storing the result as a graph ontology in Neo4j with nodes for each of the 12 psychological dimensions + 5 psychometric extensions.

**Output artifacts:**
- `tribe_profile.json` — raw tribe cultural intelligence (Stage A)
- `tribe_profile_distilled.json` — mode-mapped, depth-stratified profile (Stage B)
- Context Premise Map (DEP-ENG-006) — Neo4j graph ontology (Stage B output persisted to graph)

### Scope

**In scope:**
- Tribe Profile (`tribe_profile.json`) structure and schema
- Context Premise Map (DEP-ENG-006) — 12 base dimensions + 5 psychometric extensions
- L1/L2/L3 depth stratification with verifiable 2am test criteria
- Neo4j graph ontology schema (nodes, relationships, isolation per coach)
- 4 Laws of Tribe Profile Distillation enforcement
- T/V/R emotional mode mapping
- In-group language registry (safe/sacred/outsider)
- Visual recognition code library
- Coach-tribe resonance cross-reference
- Backward compatibility fallback when Context Premise Map does not exist
- Acceptance criteria and testing strategy

**Out of scope:**
- Trigger Matching Layer 4-axis engine (downstream consumer — FR7)
- Activation Event seed construction (Stage 3 of Trigger-First Engine — downstream)
- CBCS client-side Context Premise extraction via Aria (FR29 — separate pipeline)
- Context Premise Engine Mode A/B/C adaptive architecture (Phase 2+ implementation)
- V²WS webinar-specific context mapping (CBCS feature)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-006` | Context Premise Map | PRIMARY OUTPUT — the 12+5 dimension graph ontology |
| `DEP-LIB-001` | Emotional DNA Profile | DOWNSTREAM CONSUMER — Trigger Matching Layer uses DEP-LIB-001 + DEP-ENG-006 for 4-axis matching |
| `DEP-LIB-002` | Trigger Map | DOWNSTREAM CONSUMER — Trigger Map moral foundations matched against DEP-ENG-006 audience emotional triggers |
| `DEP-ENG-023` | Cultural Memory Map | CROSS-REFERENCE — CMM Layer 7 (Shared Enemy Typology) aligns with Context Premise `enemies` dimension |
| `DEP-ENG-019` | Session Transcript Intelligence | FEEDBACK INPUT — weekly voice notes update L3 depth verification scores |

### Academic Research Grounding

| Component | Framework | Key Papers | Lab Reference |
|---|---|---|---|
| L1/L2/L3 depth stratification | Clark & Brennan Common Ground Theory (1991) | Clark & Brennan (1991) *Grounding in Communication*; Clark (1996) *Using Language* | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 3 Pillar 3 |
| L3 verification / 2am test | Mind After Midnight Hypothesis; Online Disinhibition Effect | Tubbs et al. (2022) *Mind After Midnight*; Suler (2004) *Online Disinhibition* | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) |
| LIWC-22 authenticity scoring | Pennebaker LIWC-22 | Pennebaker et al. (2015); Newman et al. (2003) *Lying Words* | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) §LIWC-22 |
| Digital ethnography | Kozinets Netnography (2020) | Kozinets (2020) *Netnography: The Essential Guide* (3rd ed.) | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) §§1-2 |
| Audience appraisal profiling | Scherer Component Process Model | Scherer (2009) *Dynamic Architecture of Emotion*; Revised CPM parallel constraint satisfaction | [Audience Appraisal Profiling Framework](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Audience%20Appraisal%20Profiling%20Framework.md) |
| Coping trajectory staging | Lazarus & Folkman Transactional Model | Lazarus & Folkman (1984) *Stress, Appraisal, and Coping* | [Coping Trajectory Staging Framework](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Coping%20Trajectory%20Staging%20Framework.md) |
| Hermeneutical injustice detection | Fricker Epistemic Injustice; Dotson Testimonial Smothering | Fricker (2007); Dotson (2011) *Tracking Epistemic Violence*; Medina (2013) *Epistemology of Resistance* | [Detecting Hermeneutical Injustice Computationally](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Detecting%20Hermeneutical%20Injustice%20Computationally.md) |
| Regulatory focus | Higgins Regulatory Focus Theory (1997) | Higgins (1997) *Beyond Pleasure and Pain* | [Integrating Regulatory Focus Theory](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Integrating%20Regulatory%20Focus%20Theory.md) |
| Moral emotions → foundations | Haidt MFT; eMFD | Atari et al. (2023) MFQ-2; Hopp et al. (2021) eMFD | [Mapping Moral Emotions to Foundations](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Mapping%20Moral%20Emotions%20to%20Foundations.md) |
| Audience reconsolidation | Nader Memory Reconsolidation; Prediction Error | Nader (2000); NEAS vmPFC predictive hierarchy | [Audience Reconsolidation and Content Impact](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Audience%20Reconsolidation%20and%20Content%20Impact.md) |
| PTG dual-layer encoding | Tedeschi & Calhoun PTG (2004) | Tedeschi & Calhoun (2004) *Posttraumatic Growth* | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 3 Pillar 1 |
| Meaning transmission | Frankl Logotherapy | Frankl (1946/2006) *Man's Search for Meaning* | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 3 Pillar 2 |
| Data provenance | C2PA Content Provenance | C2PA Specification v2.0 (2024) | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) §C2PA |

### Key Files

| File | Purpose |
|---|---|
| `skills/ccf/setup/tribe-soul-extraction/SKILL.md` | Stage A — raw tribe extraction (Audience Empathy Agent) |
| `skills/ccf/distillation/tribe-distiller/SKILL.md` | Stage B — distillation into mode-mapped, depth-stratified profile |
| `intelligence/tribe/tribe_profile.json` | Stage A output |
| `intelligence/tribe/tribe_profile_distilled.json` | Stage B output |
| `intelligence/tribe/audience_analysis.md` | Human-readable tribe analysis |
| `intelligence/tribe/H9_DISTILLATION_RECEIPT.md` | Distillation law compliance receipt |
| `CBCS/backend/intelligence_library/context_premise_map.json` | Reference schema (12+5 dimensions) |
| `config.yaml` | Session status tracking |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Neo4j graph ontology, not flat JSON** | The 12 dimensions are not independent lists — they form an interconnected network. A `hidden_belief` node connects to specific `fear` nodes, specific `coping_mechanism` nodes, and specific `emotional_trigger` nodes. These relationships ARE the intelligence. Flat JSON captures the entries; the graph captures the architecture of how they interact inside the audience's psyche. |
| **Per-coach isolation (zero shared infrastructure)** | Voice DNA (`coach_soul.json`) is the coach's IP. Context Premises contain the most sensitive psycho-emotional data possible — fears, traumas, internal battlefields. Mixing any data layer risks cross-coach contamination catastrophic to platform trust. ADR-01 mandates zero tolerance for shared infrastructure. |
| **L1/L2/L3 stratification as hard structure, not metadata** | The Trigger Matching Layer operates EXCLUSIVELY on L3 data (Context_Premise_Trigger_Matching_Layer §Part 2 Law 2). An L1-dominant Context Premise cannot feed the matching engine regardless of research quality. Depth is not a nice-to-have tag — it determines functional capability. |
| **12 base + 5 psychometric extension dimensions** | The original 12 dimensions (frustrations, wants, dreams, fears, suspicions, insecurities, envy_feelings, enemies, coping_mechanism, hidden_beliefs, emotional_triggers, success_markers) capture the audience's psychological landscape. The 5 extensions (regulatory_focus_orientation, moral_foundation_violated, coping_trajectory_position, hermeneutical_gap_markers, reconsolidation_sensitivity) provide the psychometric precision required for structural matching — they are the bridge from qualitative research to quantitative matching coordinates. |
| **Two-stage pipeline (extraction then distillation)** | Raw tribe data (H11) is high-volume, verbatim, unstructured. Distillation is a separate analytical act — mode-mapping, depth-stratification, cross-referencing with coach philosophy. Combining them in one stage would either sacrifice volume (cutting research short to do analysis) or sacrifice analysis quality (distilling without enough raw material). |
| **4 Laws as hard gates, not suggestions** | Law compliance determines whether the profile is AUTHENTICATED, PROVISIONAL, or FAILED. A FAILED profile cannot feed downstream stages. This prevents the most common failure mode: a tribe profile that is generic enough to describe any audience in the industry, carrying no tribal specificity. |

---

## Implementation Plan

### Stage A: Tribe Soul Extraction (Genesis Setup)

**Agent:** Tribe Soul Extraction Engine V2 (The Tribe Cartographer)
**Pi Extensions:** `InteractComp`, `MemoryFolder`
**CCP Layer:** Memory (L2)

---

#### Phase A1: INGEST

**Steps:**
1. Load `config.yaml` for input paths
2. Load `coach_soul.json` (from soul-extract session) — needed for coach-tribe alignment
3. Load `coach_philosophy_brief_v{N}.md` (from philosophy-brief session) — which tribe dynamics this coach's philosophy addresses
4. Load H11 Tribe Dossier (produced by FR0B Tribe Soul Research) if available
5. Load audience raw data: social comments, Reddit threads, forum posts, industry group discussions
6. Load Tshala SentimentReport JSON (if available) — seeds RTTR fields
7. **PRE-FLIGHT:** Verify audience raw data exists and is non-empty. If missing → HALT with error: "Cannot extract tribe profile. Audience raw data not found. Conduct audience research first."
8. **Receipt Write (Phase A1):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-TRIBE-INGEST",
  "previous_receipt_hash": "{FR0B_FINAL_RECEIPT_HASH}",
  "input_payload_hash": "{H11_DOSSIER_AND_RAW_DATA_HASH}",
  "output_payload_hash": "{NULL_TRIBE_TEMPLATE_HASH}",
  "stage_name": "TRIBE-EXTRACT-INGEST",
  "agent_name": "Tribe Soul Extraction Engine V2",
  "timestamp": "{ISO8601}" }
```

---

#### Phase A2: RESEARCH PLANNING

**Agent Mode:** Digital Ethnographer — high-volume, verbatim data collection

Execute the 4-dimensional research planning framework:

| Dimension | Target Data Type | Volume Quota | Sources |
|---|---|---|---|
| **D1: Cultural Artifact Archiving** | Tribe slang, acronyms, jargon, inside jokes, shared narratives, heroes, villains | 100–150 verbatim examples of slang; 75–100 hero/enemy posts | Subreddits, Discord channels, closed Facebook groups, industry forums |
| **D2: Humor Profile Deconstruction** | Dominant humor styles, targets of humor, taboo topics | Top 50–100 humor/meme posts; ≥3 examples per humor style | Flair-filtered posts, top-voted funny content, downvoted humor analysis |
| **D3: Emotional Landscape Mapping** | Raw emotional expressions — aspirations, anxieties, trigger events | Top 5–7 aspiration quotes + 5–7 anxiety quotes + 3 positive/negative triggers | Rant/vent threads, success/celebration posts, high-engagement discussions |
| **D4: Social Dynamics & Hierarchy** | In-group signals, status markers, unwritten rules | Observation of member interactions, boundary enforcement behaviors | Newcomer correction threads, moderation actions, status signaling |

**Output:** A 25–30 page "Tribe Dossier" of raw, verbatim data ready for extraction.

---

#### Phase A3: CULTURAL HARVESTING (I-R-E-V-C REASON)

Using the Tribe Dossier, the Cultural Harvester agent systematically extracts:

**3A: Cultural Artifacts**
- Tribe slang: minimum 10–15 terms, each with verbatim example quote in context
- Inside jokes & lore: minimum 5–7, each with description and reference quote
- Shared heroes: minimum 5, each with evidence quote demonstrating status
- Common enemies: minimum 5, each with evidence quote demonstrating villain status

**3B: Humor DNA Profiling**
- Dominant + secondary humor styles with ≥3 verbatim examples per style
- Humor targets: minimum 5, each with example joke
- Taboos & no-go zones: minimum 2–3, with evidence of negative reactions

**3C: Emotional Resonance Mapping**
- Primary aspirations: minimum 5–7 verbatim quotes expressing desire/hope/goals
- Core anxieties: minimum 5–7 verbatim quotes expressing fear/frustration/pain
- High-arousal triggers: minimum 3 positive + 3 negative event types with verbatim reaction quotes

**3D: V2 Law Extensions**
- **Law 1 — Visual Recognition Codes:** ≥5 insider visual objects, ≥3 visual rejection triggers
- **Law 2 — Emotional Mode Mapping:** Every artifact tagged T (Tension) / V (Vulnerability) / R (Recognition)
- **Law 3 — Depth Stratification:** Surface / Mechanism / Collision classification. ≥30% mechanism, ≥10% collision.
- **Law 4 — Anti-Aspirational Markers:** ≥3 items the tribe actively rejects (performative wellness, fake inclusivity, "tourist" language)

---

#### Phase A4: EMIT

Write structured output:
- `intelligence/tribe/tribe_profile.json` — full schema per SKILL.md
- `intelligence/tribe/audience_analysis.md` — human-readable analysis narrative
- **Receipt Write (Phase A4):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-TRIBE-EMIT",
  "previous_receipt_hash": "{PHASE_A1_RECEIPT_HASH}",
  "input_payload_hash": "{TRIBE_DOSSIER_EXTRACTED_DATA_HASH}",
  "output_payload_hash": "{TRIBE_PROFILE_JSON_HASH}",
  "stage_name": "TRIBE-EXTRACT-EMIT",
  "agent_name": "Tribe Soul Extraction Engine V2",
  "timestamp": "{ISO8601}" }
```

---

#### Phase A5: VALIDATE

Schema-validate `tribe_profile.json`:
- [ ] `cultural_artifacts.tribe_slang` ≥ 10 terms, each with mode tag
- [ ] `cultural_artifacts.inside_jokes` ≥ 5, each with mode tag
- [ ] `cultural_artifacts.shared_heroes` ≥ 5
- [ ] `cultural_artifacts.common_enemies` ≥ 5
- [ ] `humor_profile.dominant_style` + `secondary_style` + `style_examples` ≥ 3 each
- [ ] `humor_profile.humor_targets` ≥ 5
- [ ] `humor_profile.taboos_and_no_go_zones` ≥ 2
- [ ] `emotional_resonance.primary_aspirations` ≥ 5 verbatim quotes
- [ ] `emotional_resonance.core_anxieties` ≥ 5 verbatim quotes
- [ ] `emotional_resonance.high_arousal_triggers` ≥ 3 positive + 3 negative
- [ ] `visual_recognition_codes.insider_objects` ≥ 5
- [ ] `visual_recognition_codes.rejection_triggers` ≥ 3
- [ ] `anti_aspirational_markers` ≥ 3
- [ ] `depth_distribution: mechanism ≥ 30%, collision ≥ 10%`

---

#### Phase A6: CHECKPOINT

- Update `config.yaml`: `sessions.setup.tribe_extract.status = "complete"`
- Log: cultural artifacts count, verbatim quotes count, visual codes count, depth distribution, mode coverage

---

### Stage B: Context Premise Distillation & Neo4j Graph Persistence

**Agent:** Tribe Profile Distiller (The Tribe Psychologist)
**Pi Extensions:** `MemoryFolder`, `InteractComp`
**CCP Layer:** Deep Reasoning (L3)
**Depends on:** Stage A completion (`tribe_profile.json` exists)

---

#### Phase B1: INGEST

**Steps:**
1. Load `config.yaml` for project paths
2. Load `tribe_profile.json` from Stage A — the raw extraction
3. Load `coach_soul.json` (H8) — for coach voice cross-reference
4. Load `coach_philosophy_brief_v{N}.md` (H10) — for coach-tribe alignment analysis
5. Load H11 Tribe Dossier context premises (if available in `intelligence/context_premises/`)
6. **PRE-FLIGHT:** Verify `tribe_profile.json` exists and is non-empty. If missing → HALT with error: "Cannot distill tribe profile. H11 Tribe Dossier not found. Run `/ccf-context-premises` first."
7. **Receipt Write (Phase B1):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-TRIBE-DISTILL-INGEST",
  "previous_receipt_hash": "{PHASE_A4_RECEIPT_HASH}",
  "input_payload_hash": "{TRIBE_PROFILE_RAW_HASH}",
  "output_payload_hash": "{NULL_DISTILLED_TEMPLATE_HASH}",
  "stage_name": "TRIBE-DISTILL-INGEST",
  "agent_name": "Tribe Profile Distiller",
  "timestamp": "{ISO8601}" }
```

---

#### Phase B2: DEPTH STRATIFICATION (L1/L2/L3)

For each of the 12 base dimensions, classify every entry:

| Level | Behavioral Mode | Verification Criteria | Evidence Required |
|---|---|---|---|
| **L1 — Public Statements** | Performative broadcast | High self-monitoring. Polished language. Could appear on LinkedIn/Instagram. | Surface-level observation — public posts, professional commentary |
| **L2 — Private Struggles** | Communal in-group disclosure | Moderated by group norms. Confessional but guarded. Uses in-group qualifiers. | Access-restricted immersion — closed groups, Slack channels, member threads |
| **L3 — Unspoken Feelings** | Authentic anonymous disinhibition | Passes the 2am test (Tubbs et al.). Low self-monitoring. Unpolished. Raw. | Verified behavioral observation — anonymous forums, late-night posts, DMs. LIWC-22 authenticity score ≥70th percentile. |

**Hard gate (Law 2 from Context_Premise_Trigger_Matching_Layer):** L2 entries must be ≥30% of all insights. L3 entries must be ≥10% of all insights. An L1-dominant profile CANNOT feed the Trigger Matching Layer.

**Neuroscience grounding for L3 verification (Mind After Midnight hypothesis):**
- Amygdala-PFC decoupling during circadian nadir → reduced self-regulation → spontaneous disclosure
- LIWC-22 markers of L3: high personal pronouns (I/me/my), lower cognitive complexity, increased negative emotion words, narrative style
- Conversely, L1 markers: low personal pronouns, managed emotions, polished/formal style, high social monitoring

---

#### Phase B3: EMOTIONAL MODE MAPPING (T/V/R)

For every trigger, celebration, grief pattern, and solidarity signal:

| Mode | Definition | Example | Content Routing Implication |
|---|---|---|---|
| **T — Tension** | Creates confrontation. Common enemies, wounds, injustices. | "Medical neglect of our community" | Routes to high-temperature archetypes (TTT-07+): `myth_indignation`, `reaction_outrage` |
| **V — Vulnerability** | Reveals private pain. Core anxieties, unspoken fears, taboos. | "Postpartum isolation — nobody talks about it" | Routes to low-temperature archetypes (TTT-02/03): `story_transformation`, `story_recognition` |
| **R — Recognition** | Triggers recognition/belonging. Daily rituals, insider language, shared memories. | "Missing home cooking — the smell of matembélé" | Routes to recognition archetypes: `tweet_recognition`, `listicle_relatable` |

**Additional fields per trigger:**
- `intensity`: dormant / active / nuclear
- `activation_conditions`: What fires this trigger in current events/themes

**Gate:** ≥3 triggers per mode. If any mode has <3 → profile is MODE-INCOMPLETE → return to H11 for enrichment.

---

#### Phase B4: VISUAL RECOGNITION CODE & LANGUAGE REGISTRY

**Visual Recognition Codes:**
```
INSIDER OBJECTS (≥5):
  Objects/scenes tribe recognizes INSTANTLY as "us"
  
REJECTION TRIGGERS (≥3):
  Visuals that signal "outsider" or "tourist"
  
SACRED OBJECTS (≥2):
  Visuals the tribe considers precious — handle with care
```

**In-Group Language Registry:**
```
SAFE vocabulary (≥10 terms):
  { term, context, emotional_register, example_usage }
  Can use freely in content.
  
SACRED vocabulary:
  { term, context, required_mode, misuse_risk }
  Use only in specific emotional contexts.
  
OUTSIDER vocabulary (≥5 terms):
  { term, why_rejected, what_to_use_instead }
  NEVER use — signals inauthenticity.
```

**Gate (Law 3 from tribe-distiller):** ≥10 safe terms, ≥5 outsider terms. Below threshold → language research incomplete.

---

#### Phase B5: COACH-TRIBE RESONANCE CROSS-REFERENCE

Using `coach_philosophy_brief` (H10) and `coach_soul.json` (H8):

| Analysis | Minimum | Purpose |
|---|---|---|
| **Alignment Points** | ≥3 documented | Where coach's philosophy ADDRESSES tribe's pain → content leverage points |
| **Friction Points** | ≥1 documented | Where coach's belief CONTRADICTS tribe's experience → authenticity risk zones |
| **Gaps** | Free count | Tribe pains the coach's philosophy doesn't address yet → content opportunity areas |

> **Missing friction is a red flag.** If coach and tribe are in perfect agreement on everything, the relationship is idealized, not real. Real resonance includes productive tension.

---

#### Phase B6: PSYCHOMETRIC EXTENSION MAPPING (5 dimensions)

Beyond the base 12, each segment receives 5 psychometric extensions grounded in the 7 Context Premise research papers:

| Extension Dimension | Framework | What It Captures | Data Source |
|---|---|---|---|
| `regulatory_focus_orientation` | Higgins Regulatory Focus Theory (1997) | Promotion-focused (seeking gains, growth, ideals) vs. prevention-focused (avoiding losses, safety, duties) | Eager vs. vigilant language markers from audience text |
| `moral_foundation_violated` | Haidt MFT / MFQ-2; eMFD | Which of the 6 moral foundations is activated in the audience's L3 pain | Reverse-engineered from moral emotion linguistic signatures (LIWC function words + eMFD probability vectors) |
| `coping_trajectory_position` | Lazarus & Folkman (1984) | Current phase in the stress-coping cycle: SEARCH (peak intervention receptivity), ACTIVE, EXHAUSTED | Temporal language shifts, agency attribution changes, question-type evolution |
| `hermeneutical_gap_markers` | Fricker (2007); Dotson (2011) | Evidence of unarticulated experience — the audience's reality they cannot yet name | Discourse truncation (cosine similarity drops mid-post), affective parabola (sentiment regression within single post), metaphor novelty via MelBERT |
| `reconsolidation_sensitivity` | Nader (2000); NEAS framework | Readiness for memory reconsolidation — prediction error sensitivity | Save rate, comment depth, share velocity, DM response rate as behavioral engagement proxies |

---

#### Phase B7: NEO4J GRAPH ONTOLOGY PERSISTENCE

**Node Types (per coach, fully isolated):**

| Node Type | From Dimension | Properties |
|---|---|---|
| `:Frustration` | `frustrations` | `text`, `depth_level` (L1/L2/L3), `mode` (T/V/R), `intensity`, `source_evidence`, `provenance_score` |
| `:Want` | `wants` | Same properties |
| `:Dream` | `dreams` | Same properties |
| `:Fear` | `fears` | Same properties |
| `:Suspicion` | `suspicions` | Same properties |
| `:Insecurity` | `insecurities` | Same properties |
| `:EnvyFeeling` | `envy_feelings` | Same properties |
| `:Enemy` | `enemies` | Same properties |
| `:CopingMechanism` | `coping_mechanism` | Same properties + `trajectory_position` |
| `:HiddenBelief` | `hidden_beliefs` | Same properties |
| `:EmotionalTrigger` | `emotional_triggers` | Same properties + `activation_keywords[]`, `moral_foundation` |
| `:SuccessMarker` | `success_markers` | Same properties |
| `:Segment` | Audience segment (e.g., "aspiring_investor") | `id`, `dhd_label`, `regulatory_focus`, `coping_stage`, `reconsolidation_readiness` |
| `:HermeneuticalGap` | `hermeneutical_gap_markers` | `text`, `detection_method` (truncation/parabola/novelty), `confidence_score` |

**Relationship Types:**

| Relationship | Pattern | What It Captures |
|---|---|---|
| `TRIGGERS` | `(:Fear)-[:TRIGGERS]->(:CopingMechanism)` | Which fears activate which coping behaviors |
| `CONTRADICTS` | `(:HiddenBelief)-[:CONTRADICTS]->(:Want)` | Where stated desires conflict with private beliefs (L3 collision) |
| `FUELS` | `(:Enemy)-[:FUELS]->(:EmotionalTrigger)` | Enemy perceptions that power trigger activation |
| `MASKS` | `(:SuccessMarker)-[:MASKS]->(:Insecurity)` | What they chase publicly to hide what they feel privately |
| `VIOLATES` | `(:EmotionalTrigger)-[:VIOLATES]->(:MoralFoundation)` | Which moral foundation each trigger activates |
| `BELONGS_TO` | `(:*)-[:BELONGS_TO]->(:Segment)` | Segment membership for all nodes |
| `AT_DEPTH` | `(:*)-[:AT_DEPTH {level: "L3"}]->(:DepthLevel)` | L1/L2/L3 classification edge |
| `RESONATES_WITH` | `(:EmotionalTrigger)-[:RESONATES_WITH]->(:CoachTrigger)` | Coach-tribe structural congruence (populated by Trigger Matching Layer) |

**Isolation constraint:** Each coach's graph operates in a dedicated Neo4j database or labeled graph partition. Zero cross-coach queries permitted. If coach exits platform → secure purge of all graph data (ADR-01).

**Performance requirement:** Graph read for real-time personalization: **<500ms** per query (PRD §Non-Functional Requirements).

---

#### Phase B8: EMIT

Write outputs:
- `intelligence/tribe/tribe_profile_distilled.json` — full distilled profile
- `intelligence/tribe/H9_DISTILLATION_RECEIPT.md` — law compliance receipt
- Neo4j graph populated with all nodes and relationships
- **Receipt Write (Phase B8):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-TRIBE-DISTILL-EMIT",
  "previous_receipt_hash": "{PHASE_B1_RECEIPT_HASH}",
  "input_payload_hash": "{DISTILLED_GRAPH_DATA_HASH}",
  "output_payload_hash": "{TRIBE_DISTILLED_JSON_HASH}",
  "stage_name": "TRIBE-DISTILL-EMIT",
  "agent_name": "Tribe Profile Distiller",
  "timestamp": "{ISO8601}" }
```

---

#### Phase B9: VALIDATE — 4 Laws of Tribe Profile Distillation

**Law 1 — Mode-Mapped Emotional Triggers:**
- [ ] ≥3 triggers per mode (T/V/R)
- [ ] Every trigger has `mode`, `intensity`, `activation_conditions`
- [ ] Untagged triggers → returned to H11

**Law 2 — Visual Recognition Code Library:**
- [ ] ≥5 insider visual objects
- [ ] ≥3 visual rejection triggers
- [ ] ≥2 sacred objects with handling notes

**Law 3 — In-Group Language Registry:**
- [ ] ≥10 safe vocabulary terms
- [ ] ≥5 outsider vocabulary terms (NEVER use)
- [ ] Each term has context, emotional register, usage example

**Law 4 — Tribe Authenticity Gate (4 checks):**
- [ ] CHECK 1 — Experiential Verification: Every trigger/pain/code based on actual tribe behavior (from H11 research), not coach assumptions
- [ ] CHECK 2 — Depth Distribution: L2 ≥30%, L3 ≥10%
- [ ] CHECK 3 — Coach-Tribe Cross-Reference: ≥3 alignment points, ≥1 friction point
- [ ] CHECK 4 — Interchangeability Test: Profile could NOT describe a different community's tribe

**Verdict:**
- ALL 4 PASS → **AUTHENTICATED**
- 3 PASS → **PROVISIONAL** (usable with flags)
- ≤2 PASS → **FAILED** (return to H11 for deeper research)

---

#### Phase B10: CHECKPOINT

- Update `config.yaml`: `sessions.distillation.tribe_distill.status = "complete"`
- Update `config.yaml`: `sessions.setup.tribe_extract.status = "complete"` (if not already)
- Write H9_DISTILLATION_RECEIPT.md with law compliance, depth distribution, mode coverage
- Log: mode distribution (T:n / V:n / R:n), depth distribution (L1:n% / L2:n% / L3:n%), visual code count, language registry count, authentication verdict

---

## Context Premise Map Schema (DEP-ENG-006)

The full 12+5 dimension schema stored in Neo4j and serialized to `context_premise_map.json`:

```json
{
  "dep_id": "DEP-ENG-006",
  "version": "3.0",
  "coach_id": "isolated_per_coach",
  "dimensions": {
    "frustrations": {
      "entries": [
        { "text": "", "depth": "L1|L2|L3", "mode": "T|V|R", "intensity": "dormant|active|nuclear", "source": "" }
      ]
    },
    "wants": { "entries": [] },
    "dreams": { "entries": [] },
    "fears": { "entries": [] },
    "suspicions": { "entries": [] },
    "insecurities": { "entries": [] },
    "envy_feelings": { "entries": [] },
    "enemies": { "entries": [] },
    "coping_mechanism": { "entries": [] },
    "hidden_beliefs": { "entries": [] },
    "emotional_triggers": {
      "entries": [
        { "text": "", "depth": "L1|L2|L3", "mode": "T|V|R", "activation_keywords": [], "moral_foundation": "", "source": "" }
      ]
    },
    "success_markers": { "entries": [] }
  },
  "psychometric_extensions": {
    "regulatory_focus_orientation": "promotion|prevention|mixed",
    "moral_foundation_violated": {
      "primary": "care_harm|fairness_cheating|loyalty_betrayal|authority_subversion|sanctity_degradation|liberty_oppression",
      "secondary": "",
      "weighting": {}
    },
    "coping_trajectory_position": "search|active|exhausted",
    "hermeneutical_gap_markers": [
      { "text": "", "detection_method": "truncation|parabola|novelty", "confidence": 0.0 }
    ],
    "reconsolidation_sensitivity": {
      "overall_score": 0.0,
      "engagement_proxies": {
        "save_rate": 0.0,
        "comment_depth": 0.0,
        "share_velocity": 0.0,
        "dm_response_rate": 0.0
      }
    }
  },
  "segments": [],
  "depth_distribution": { "L1": 0.0, "L2": 0.0, "L3": 0.0 },
  "mode_distribution": { "T": 0, "V": 0, "R": 0 },
  "authentication_status": "AUTHENTICATED|PROVISIONAL|FAILED",
  "last_updated": "ISO8601"
}
```

---

## Backward Compatibility — Legacy Fallback

**Condition:** Context Premise Map (DEP-ENG-006) does not exist for this coach.

**Fallback behavior:**
1. Content generation uses `coach_soul.json` values and topic-based prompts instead of audience-matched structural seeds
2. The Trigger Matching Layer's 4-axis engine cannot execute — content is generated from coach triggers without audience structural matching
3. Archetype selection uses coach emotional state only, not audience mode routing
4. DARN-CAT questions are topic-generic, not L3-vocabulary-anchored

**Limitation:** Content without the Context Premise Map delivers professional empathy (comprehension without coupling). Expected neural coupling quality will be significantly lower. The audience feels informed but not recognized.

**Exit from fallback:** When Stage A + Stage B complete → `tribe_profile_distilled.json` exists + Neo4j populated → weekly pipeline automatically reads DEP-ENG-006 for Trigger Matching. No manual intervention needed.

---

## Tasks

- [ ] **Task 1:** Implement Stage A INGEST — loading audience raw data, coach_soul, philosophy brief, Tshala SentimentReport
- [ ] **Task 2:** Implement Research Planning Engine — 4-dimension research framework (cultural artifacts, humor profiling, emotional landscape, social dynamics)
- [ ] **Task 3:** Implement Cultural Harvesting — extraction from Tribe Dossier with volume quotas (slang ≥10, heroes ≥5, enemies ≥5, humor examples ≥3 per style, aspirations ≥5, anxieties ≥5)
- [ ] **Task 4:** Implement Law 1 V2 extensions — visual recognition codes (≥5 insider, ≥3 rejection) + emotional mode mapping (T/V/R tagging)
- [ ] **Task 5:** Implement Law 3 V2 extensions — depth stratification (surface/mechanism/collision ≥30%/≥10%) + anti-aspirational markers (≥3)
- [ ] **Task 6:** Implement Stage A EMIT + VALIDATE — schema validation of `tribe_profile.json` against all volume quotas
- [ ] **Task 7:** Implement Stage B INGEST — loading `tribe_profile.json`, coach cross-reference data
- [ ] **Task 8:** Implement L1/L2/L3 depth stratification — classification per entry with LIWC-22 authenticity scoring for L3 verification
- [ ] **Task 9:** Implement T/V/R emotional mode mapping — trigger mode classification with intensity and activation conditions
- [ ] **Task 10:** Implement visual recognition codes + in-group language registry — insider/rejection/sacred objects + safe/sacred/outsider vocabulary
- [ ] **Task 11:** Implement coach-tribe resonance cross-reference — alignment points, friction points, gap analysis
- [ ] **Task 12:** Implement 5 psychometric extension mappings — regulatory focus, moral foundation, coping trajectory, hermeneutical gap markers, reconsolidation sensitivity
- [ ] **Task 13:** Implement Neo4j graph ontology schema — node types (12 dimensions + segments + gaps), relationship types (TRIGGERS, CONTRADICTS, FUELS, MASKS, VIOLATES, BELONGS_TO, AT_DEPTH), per-coach isolation
- [ ] **Task 14:** Implement Stage B VALIDATE — 4 Laws of Tribe Profile Distillation (mode triggers, visual codes, language registry, authenticity gate with 4 checks)
- [ ] **Task 15:** Implement Stage B EMIT + CHECKPOINT — write distilled profile, H9 receipt, populate Neo4j, update config
- [ ] **Task 16:** Implement backward compatibility fallback — `context_premise_map.json` existence check, legacy topic-based content generation when absent

---

## Acceptance Criteria

- [ ] **AC1 (Prerequisite Gate — Stage A):** Pipeline halts with descriptive error when audience raw data is empty or missing.
- [ ] **AC2 (Prerequisite Gate — Stage B):** Pipeline halts with descriptive error when `tribe_profile.json` does not exist.
- [ ] **AC3 (Volume Quotas):** `tribe_profile.json` contains: ≥10 slang terms, ≥5 inside jokes, ≥5 heroes, ≥5 enemies, ≥3 humor examples per style, ≥5 aspiration quotes, ≥5 anxiety quotes, ≥3 pos + 3 neg high-arousal triggers. Any quota unmet → validation fails.
- [ ] **AC4 (Depth Stratification):** `tribe_profile_distilled.json` depth distribution: L2 ≥30% AND L3 ≥10%. A profile with 80% L1 / 15% L2 / 5% L3 → FAILED (L3 <10%).
- [ ] **AC5 (Mode Coverage):** ≥3 triggers per mode (T/V/R). A profile with 10 Tension triggers, 4 Vulnerability triggers, 0 Recognition triggers → MODE-INCOMPLETE.
- [ ] **AC6 (Visual Codes):** ≥5 insider objects, ≥3 rejection triggers present. Insider objects must be specific to THIS tribe, not generic stock imagery.
- [ ] **AC7 (Language Registry):** ≥10 safe terms with context examples, ≥5 outsider terms with "use instead" alternatives. "Self-care" tagged as outsider → correct. "Journey" tagged as safe → requires evidence.
- [ ] **AC8 (Interchangeability Test):** Profile fails Law 4 Check 4 if it could describe a different community's tribe — i.e., replacing the coach's industry name with a different industry would not invalidate any entry.
- [ ] **AC9 (Neo4j Isolation):** A query from Coach A's graph CANNOT return nodes from Coach B's graph. Cross-coach contamination = critical security violation.
- [ ] **AC10 (Neo4j Performance):** Context Premise graph read for personalization completes in <500ms per query.
- [ ] **AC11 (Authentication Verdict):** Profile classified as AUTHENTICATED (4/4 laws pass), PROVISIONAL (3/4), or FAILED (≤2/4). FAILED profile returns error and cannot feed downstream stages.
- [ ] **AC12 (Coach-Tribe Resonance):** ≥3 alignment points and ≥1 friction point documented. Zero friction points → WARNING: relationship is idealized.
- [ ] **AC13 (Backward Compatibility):** A coach without Context Premise Map → content generated using topic-based prompts from coach_soul.json. No errors. All downstream phases complete. Trigger Matching Layer gracefully degrades.
- [ ] **AC14 (Psychometric Extensions):** All 5 extensions populated or explicitly null with reasoning. `moral_foundation_violated` must use MFT/MFQ-2 framework labels, not free-text.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Coach Soul extraction (`coach_soul.json`) | Internal prerequisite | From `ccf-init` / soul-extract session |
| Philosophy Brief (`coach_philosophy_brief_v{N}.md`) | Internal prerequisite | From philosophy-brief session — needed for coach-tribe cross-reference |
| H11 Audience Research | External input | Raw audience data must be collected before pipeline runs |
| Neo4j database | Infrastructure | Dedicated per-coach instance or labeled graph partition |
| LIWC-22 scoring | License | For L3 authenticity verification |
| Receipt Chain Guard | Infrastructure | Receipts at INGEST + EMIT for both stages |

---

## Testing Strategy

### Unit Tests
- **Depth classification:** 9 synthetic audience entries (3 L1, 3 L2, 3 L3) → validate correct depth assignment using LIWC-22 markers
- **Mode mapping:** 9 synthetic triggers (3 T, 3 V, 3 R) → validate correct mode classification
- **Volume quota validation:** Tribe profile with exactly 9 slang terms (below quota) → validation fails. With 10 → passes.
- **Interchangeability test:** Generic profile ("People in this industry want success") → fails Check 4. Specific profile ("Congolese diaspora mothers fear their children losing Lingala") → passes.
- **Language registry:** 3 outsider terms without "use instead" alternatives → validation fails

### Integration Tests
- **Full Stage A → Stage B pipeline:** Run tribe extraction on synthetic audience data → validate: `tribe_profile.json` meets all quotas, `tribe_profile_distilled.json` meets all 4 Laws, Neo4j populated with correct node types and relationships
- **Neo4j isolation:** Create graphs for 2 synthetic coaches. Run cross-coach query → must return empty result set (zero contamination).
- **Neo4j performance:** Populate graph with 200+ nodes across 12 dimensions. Run 10 concurrent Context Premise queries → all return in <500ms.

### Safety Tests
- **Cross-coach contamination:** Attempt to read Coach B's `:Fear` nodes from Coach A's connection → must fail with authentication/isolation error.
- **Coach exit purge:** Delete coach from platform → verify all Neo4j nodes, relationships, and graph partition are completely removed. Zero residual data.
- **FAILED profile gate:** Submit a FAILED profile to the Trigger Matching Layer → must be rejected with descriptive error before any matching occurs.
