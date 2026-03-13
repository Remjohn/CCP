# Tech-Spec: FR9 — Audience Empathy Agent & Per-Theme Context Premise Generation

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.1)
**Architecture Reference:** §Context_Premise_Trigger_Matching_Layer Part 2, §Layer 2 (MEMORY — Neo4j HGM), §5.2 (Corrected Intake Flow — Tribe Extraction)
**Skill Implementation:** `skills/ccf/production/audience-empathy-agent/SKILL.md`

---

## Overview

### Problem Statement

FR6 solves the foundational problem: extracting a coach's Tribe Profile and constructing the Context Premise Map (DEP-ENG-006) as a one-time setup operation. But the Context Premise Map is a standing intelligence artifact — a permanent psychological atlas of the audience's internal worldview. It does not answer the production-time question: *for this specific content theme, which audience segments are most structurally relevant, and what does their L3 reality look like right now?*

The Trigger Matching Layer (Context_Premise_Trigger_Matching_Layer §Part 4) requires theme-specific L3 structural coordinates to construct activation event seeds. It needs to know, for a given content topic — say, "overcoming financial shame" — exactly which audience segments carry relevant hidden beliefs, which emotional triggers fire, and which coping mechanisms are active. The standing Context Premise Map provides the substrate. The Audience Empathy Agent provides the theme-specific extraction that makes the substrate operationally useful for each content production session.

Without per-theme extraction, the Trigger Matching Layer receives the entire Context Premise Map unfiltered — equivalent to searching for a specific intersection on a map without knowing which city you're in. The Four-Axis Structural Matching Engine (Context_Premise_Trigger_Matching_Layer §Part 4 Component 1) needs *focused* L3 input: the specific moral foundation violations, coping patterns, agency attributions, and hidden beliefs that are relevant to *this* content theme for *this* production window.

The Four Laws of Audience Research Distillation (Context_Premise_Trigger_Matching_Layer §Part 2) govern the quality of this extraction. Violations of any law — surface-depth content masquerading as depth, inferred rather than observed insights, generic language instead of tribal vocabulary, or unverifiable provenance — produce an L1-dominant output that cannot feed the Trigger Matching Layer regardless of how much research was conducted (Law 2: L2 ≥30%, L3 ≥10% hard gate).

### Solution

The Audience Empathy Agent is the system's runtime intelligence function for the audience side of the structural map. The System Operator invokes it per content theme. It produces a **theme-specific Context Premise** covering **6 audience segments × 12 psychological categories**, depth-stratified across L1/L2/L3, governed by the Four Laws of Audience Research Distillation.

**Agent architecture:**

1. **INGEST** — Load the standing Context Premise Map (DEP-ENG-006 from FR6), the content theme, and any fresh audience intelligence (recent forum data, current events, weekly voice note context).

2. **SEGMENT** — Identify or confirm 6 distinct audience segments for this theme, each mapped to a specific Deep Human Desire (DHD) from the DHD reference library. Segments are not demographics — they are psychological positions on the coping trajectory (Lazarus & Folkman Transactional Model).

3. **EXTRACT** — For each segment (6) × each category (12) = 72 cells minimum, extract depth-stratified insights. Each cell classified L1/L2/L3.

4. **VALIDATE** — Enforce the Four Laws as hard gates. Compute depth distribution. Verify provenance. Apply the 2am test. Apply the genericness test to tribal language.

5. **EMIT** — Output the theme-specific Context Premise as a structured artifact, ready for consumption by the Trigger Matching Layer and the Four-Axis Structural Matching Engine.

**Output artifact:**
- `intelligence/context_premises/{theme_slug}_context_premise.json` — 6 segments × 12 categories × L1/L2/L3 depth-stratified, Four Laws validated

### Scope

**In scope:**
- Per-theme Context Premise generation (6 segments × 12 psychological categories)
- Four Laws of Audience Research Distillation enforcement
- L1/L2/L3 depth stratification with 2am test verification
- Data provenance validation (Law 4)
- Genericness test for tribal language (Law 3)
- Structural weight designation for Hidden Beliefs, Emotional Triggers, and Coping Mechanism categories
- Integration with standing Context Premise Map (DEP-ENG-006 from FR6)
- Theme-specific segment identification with DHD mapping
- Acceptance criteria and testing strategy

**Out of scope:**
- Standing Context Premise Map creation and Neo4j graph persistence (FR6)
- Tribe Profile extraction and distillation (FR6 Stage A/B)
- Trigger Matching Layer four-axis engine operation (downstream consumer)
- Activation Event seed construction (downstream consumer)
- TTT resolution (FR8 — TTT is a runtime value resolved via DEP-ENG-005)
- CBCS client-side Context Premise extraction via Aria (FR29)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-006` | Context Premise Map | INPUT — standing 12+5 dimension graph ontology from FR6, provides the substrate |
| `DEP-LIB-001` | Emotional DNA Profile | DOWNSTREAM — Trigger Matching Layer uses theme-specific L3 output + DEP-LIB-001 for 4-axis matching |
| `DEP-LIB-002` | Trigger Map | DOWNSTREAM — activation event seeds use L3 tribal language from this agent's output |
| `DEP-ENG-005` | Authentication Certificate | DOWNSTREAM — TTT resolved at production time; this agent provides the audience structural coordinates that inform content direction, not TTT values |
| `DEP-ENG-019` | Session Transcript Intelligence | FEEDBACK INPUT — weekly voice notes may update theme relevance and audience resonance data |
| `DEP-ENG-023` | Cultural Memory Map | CROSS-REFERENCE — CMM Layer 7 (Shared Enemy Typology) aligns with `enemies` category extraction |

### Academic Research Grounding

| Component | Framework | Key Papers | Lab Reference |
|---|---|---|---|
| Four Laws of Audience Research Distillation | Clark & Brennan Common Ground Theory (1991) | Clark & Brennan (1991) *Grounding in Communication*; Clark (1996) *Using Language* | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 2 |
| L1/L2/L3 depth stratification | Clark Common Ground Levels; Suler Online Disinhibition (2004) | Clark (1991) three levels of common ground; Suler (2004) *Online Disinhibition Effect* | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 3 Pillar 3; [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) |
| 2am test neurobiological verification | Mind After Midnight Hypothesis; Circadian Neurobiology | Tubbs et al. (2022) *Mind After Midnight*; PFC–amygdala decoupling during circadian nadir | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) §§2am Test Neurobiology |
| LIWC-22 authenticity scoring | Pennebaker LIWC-22 Framework | Pennebaker et al. (2015); Newman et al. (2003) *Lying Words* | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) §LIWC-22 |
| Digital ethnography methodology | Kozinets Netnography (2020) | Kozinets (2020) *Netnography: The Essential Guide* (3rd ed.) — 6 movements: initiation, investigation, immersion, integration, incarnation, output | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) §§1-2 |
| Audience appraisal profiling | Scherer Component Process Model (CPM) | Scherer (2009) *Dynamic Architecture of Emotion*; Pérez-Rosas et al. (RoBERTa clause-level appraisal extraction) | [Audience Appraisal Profiling Framework](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Audience%20Appraisal%20Profiling%20Framework.md) |
| Coping trajectory staging | Lazarus & Folkman Transactional Model (1984) | Lazarus & Folkman (1984) *Stress, Appraisal, and Coping*; SEARCH phase identification via temporal language shifts, agency attribution changes, question-type evolution | [Coping Trajectory Staging Framework](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Coping%20Trajectory%20Staging%20Framework.md) |
| Memory reconsolidation / prediction error | Nader Memory Reconsolidation; NEAS Framework | Nader (2000); NEAS vmPFC predictive hierarchy; Hasson (2005) neural coupling | [Audience Reconsolidation and Content Impact](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Audience%20Reconsolidation%20and%20Content%20Impact.md) |
| Hermeneutical gap detection | Fricker Epistemic Injustice (2007) | Fricker (2007); Dotson (2011) *Tracking Epistemic Violence* — audiences in hermeneutical injustice lack language for their own experience | [Detecting Hermeneutical Injustice Computationally](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Detecting%20Hermeneutical%20Injustice%20Computationally.md) |
| Moral foundation mapping | Haidt MFT / MFQ-2; eMFD | Atari et al. (2023) MFQ-2; Hopp et al. (2021) eMFD probability vectors | [Mapping Moral Emotions to Foundations](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Mapping%20Moral%20Emotions%20to%20Foundations.md) |
| Regulatory focus profiling | Higgins Regulatory Focus Theory (1997) | Higgins (1997) *Beyond Pleasure and Pain* — promotion vs. prevention orientation | [Integrating Regulatory Focus Theory](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Integrating%20Regulatory%20Focus%20Theory.md) |

### Key Files

| File | Purpose |
|---|---|
| `skills/ccf/production/audience-empathy-agent/SKILL.md` | Agent skill definition — per-theme Context Premise generation |
| `intelligence/context_premises/{theme_slug}_context_premise.json` | Theme-specific output artifact (6×12 matrix, depth-stratified) |
| `intelligence/tribe/tribe_profile_distilled.json` | FR6 Stage B output — standing distilled tribe profile (input) |
| `CBCS/backend/intelligence_library/context_premise_map.json` | DEP-ENG-006 reference schema (input) |
| `intelligence/tribe/tribe_profile.json` | FR6 Stage A output — raw tribe intelligence (input) |
| `config.yaml` | Session state tracking |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Per-theme generation, not static lookup** | The standing Context Premise Map (DEP-ENG-006) is a permanent atlas. But content themes activate different regions of that atlas. "Financial shame" activates different hidden beliefs, coping mechanisms, and moral foundations than "postpartum isolation." Per-theme extraction focuses the Trigger Matching Layer on the relevant L3 coordinates. |
| **6 segments (not fewer)** | The Four Laws specify 6 audience segments per theme (Context_Premise_Trigger_Matching_Layer §Part 2). Fewer segments collapse distinct psychological positions into averages. The audience is not homogeneous — different segments hold different hidden beliefs about the same theme, use different coping mechanisms, and sit at different positions on the coping trajectory. |
| **12 categories as structural, not cosmetic** | The 12 categories (wants, frustrations, dreams, fears, suspicions, insecurities, envy feelings, enemies, coping mechanism, hidden beliefs, emotional triggers, success markers) are not equal. Three carry disproportionate structural weight for the Trigger Matching Layer: Hidden Beliefs (location of structural ground), Emotional Triggers (activation event seeds), and Coping Mechanism (positional congruence axis). These three must receive enhanced extraction depth. |
| **L2 ≥30%, L3 ≥10% as hard gates** | Law 2 mandates minimum depth distributions. An L1-dominant output "cannot feed the matching engine regardless of research quality" (Context_Premise_Trigger_Matching_Layer §Part 2). The Trigger Matching Layer operates EXCLUSIVELY on L3 data. |
| **2am test as neurobiological verification** | The 2am test is grounded in the Mind After Midnight hypothesis (Tubbs et al. 2022): PFC–amygdala decoupling during circadian nadir produces spontaneous disclosure. LIWC-22 markers (high personal pronouns, lower cognitive complexity, increased negative emotion words) provide computational verification for L3 classification. |
| **Genericness test for tribal language** | Law 3 mandates every extracted term must FAIL the genericness test. If a term could appear in any industry's audience research, it is not tribal. Minimum 10 in-group terms, 5 rejection terms. The tribal language is the surface of the activation event seed — the coach must encounter the audience's reality in the audience's exact words. |
| **Verifiable data provenance** | Law 4 mandates every insight traces to a verifiable source (research finding, forum post, interview transcript). Inferred audience behavior produces inferred structural matches. This prevents the most dangerous failure: LLM inference masquerading as observed audience reality. |

---

## Implementation Plan

### Phase 1: INGEST — Theme Context Loading

**Steps:**

1. Receive content theme from System Operator (e.g., "overcoming financial shame," "rebuilding trust after betrayal")
2. Load standing Context Premise Map (DEP-ENG-006) from FR6 — the 12+5 dimension graph ontology
3. Load `tribe_profile_distilled.json` — the standing distilled tribe profile
4. Load `coach_soul.json` — coach voice DNA for alignment verification
5. Load fresh audience intelligence (if available):
   - Recent forum threads, social media discussions relevant to theme
   - Current events / news affecting the audience's reality on this theme
   - Weekly voice note context from DEP-ENG-019 (if available)
6. **PRE-FLIGHT:** Verify standing Context Premise Map (DEP-ENG-006) exists. If missing → HALT with error: "Cannot run Audience Empathy Agent. Standing Context Premise Map (DEP-ENG-006) not found. Complete FR6 Tribe Profile extraction first."
7. Write `receipt` → Receipt Chain Guard (Audience Empathy Agent — Phase 1 Ingest)

---

### Phase 2: SEGMENT — Six Audience Segment Identification

For the specified content theme, identify 6 distinct audience segments. Each segment represents a different psychological position relative to the theme.

**Segment identification criteria:**
- Each segment maps to a specific Deep Human Desire (DHD) from the DHD reference library
- Each segment occupies a distinct position on the coping trajectory (Lazarus & Folkman): SEARCH, ACTIVE, or EXHAUSTED
- Segments are defined by psychological position, not demographics
- Segment boundaries must be non-overlapping — if two segments share the same hidden beliefs AND coping mechanisms, they are the same segment

**Per-segment metadata:**
```json
{
  "segment_id": "aspiring_healers",
  "dhd_label": "Deep Human Desire label",
  "coping_trajectory_position": "SEARCH|ACTIVE|EXHAUSTED",
  "regulatory_focus": "promotion|prevention|mixed",
  "primary_moral_foundation_violated": "care_harm|fairness_cheating|loyalty_betrayal|authority_subversion|sanctity_degradation|liberty_oppression",
  "description": "One-paragraph psychological portrait"
}
```

**Gate:** Exactly 6 segments required. Fewer than 6 → indicates insufficient understanding of audience diversity. More than 6 → indicates failure to identify genuine psychological boundaries vs. surface variations.

---

### Phase 3: EXTRACT — 6 × 12 Matrix Population

For each of the 6 segments, extract insights across all 12 psychological categories:

| # | Category | Extraction Focus | Structural Weight |
|---|---|---|---|
| 1 | Wants | What they say they desire publicly | Standard |
| 2 | Frustrations | What blocks them — stated and unstated | Standard |
| 3 | Dreams | Aspirational future states — the ideal self | Standard |
| 4 | Fears | What threatens their current identity | Standard |
| 5 | Suspicions | Who/what they don't trust — and why | Standard |
| 6 | Insecurities | Private doubts about self-competence | Standard |
| 7 | Envy Feelings | Who they compare themselves to — upward and lateral | Standard |
| 8 | Enemies | Who/what they blame — agency attribution target | Standard |
| 9 | **Coping Mechanism** | What they do when the pain becomes unmanageable | **HIGH — positional congruence axis** |
| 10 | **Hidden Beliefs** | Beliefs that contradict their public position — the cognitive architecture beneath the surface narrative | **HIGH — structural ground location** |
| 11 | **Emotional Triggers** (array) | Specific activation events that produce involuntary emotional response — mechanisms, not topics | **HIGH — candidate seeds for Trigger Matching** |
| 12 | Success Markers | What they consider evidence of having "made it" | Standard |

**Per-cell extraction requirements:**

Each cell (segment × category) must contain:
```json
{
  "text": "The specific insight in the audience's own language",
  "depth": "L1|L2|L3",
  "source": "Verifiable source reference (forum URL, interview timestamp, research citation)",
  "tribal_terms": ["array of in-group vocabulary used"],
  "two_am_test": true|false
}
```

**Depth classification criteria (per Clark & Brennan Common Ground Theory):**

| Level | Definition | Verification | Coupling Depth |
|---|---|---|---|
| **L1 — Public Statements** | What they say publicly. High self-monitoring. Polished language. Could appear on LinkedIn/Instagram. | Surface-level observation — public posts, professional commentary | Shallow — conversational familiarity, no coupling signal |
| **L2 — Private Struggles** | What they struggle with privately. Moderated by group norms. Confessional but guarded. Uses in-group qualifiers. | Access-restricted immersion — closed groups, Slack channels, member threads | Intermediate — emotional attunement, still constructed empathy |
| **L3 — Unspoken Feelings** | What they will not say out loud but feel deeply. Passes the 2am test. Low self-monitoring. Unpolished. Raw. | Verified behavioral observation — anonymous forums, late-night posts, DMs. LIWC-22 authenticity score ≥70th percentile. | Deep — produces neural coupling. The credibility signal fires automatically. |

**Enhanced extraction for the three structurally weighted categories:**

1. **Hidden Beliefs** — Must identify the precise location where the coach's original formative experience and the audience's current reality are most likely to share structural ground. Each hidden belief must articulate the contradiction: "They publicly say X, but privately believe Y."

2. **Emotional Triggers (array)** — Each trigger is a discrete structural unit. Must be expressed as specific activation mechanisms, not topics. Each trigger is a candidate seed for the Trigger Matching Engine. Must include:
   - `activation_keywords[]` — specific words/phrases that fire the trigger
   - `moral_foundation` — which MFT foundation this trigger violates
   - `involuntary_response` — the immediate, unreflective emotional response

3. **Coping Mechanism** — Must reveal the audience's agency attribution pattern and coping potential assessment. A coach whose trigger was formed while using the same coping mechanism the audience is currently using has exact positional congruence — not similar, identical.

---

### Phase 4: VALIDATE — Four Laws Enforcement

The Four Laws of Audience Research Distillation are applied as hard gates. Failure on any law either degrades the profile status or triggers re-extraction.

---

#### Law 1 — Lived Reality (The 2am Test)

**Requirement:** Every insight must pass the 2am test. Does this describe something the audience actually experiences at 2am when no one is watching?

**Verification method:**
- For L3 entries: LIWC-22 authenticity scoring. An L3 entry must achieve an authenticity score ≥70th percentile based on markers: high personal pronouns (I/me/my), lower cognitive complexity, increased negative emotion words, narrative rather than analytical style.
- Neurobiological grounding (Mind After Midnight hypothesis): L3 entries originate from contexts of PFC–amygdala decoupling — anonymous forums, late-night posts (adjusted for timezone and population wakefulness patterns), DMs during emotional crises.
- **Failure mode:** An insight that reads like a LinkedIn post ("I struggle with work-life balance") fails the 2am test. An insight that reads like a 2am Reddit confession ("I pretend I have it together but I cry in the car after dropping the kids off and I don't know why I can't stop") passes.

**Gate:** Only 2am-verified material qualifies for L3 depth classification. Surface insights that are tagged L3 without passing the 2am test produce surface coupling — the most common failure mode.

---

#### Law 2 — Depth Stratification

**Requirement:** L2 content must comprise ≥30% and L3 content must comprise ≥10% of all insights across all 72 cells.

**Computation:**
```
total_cells = count(all insights across 6 segments × 12 categories)
l2_percentage = count(depth == "L2") / total_cells
l3_percentage = count(depth == "L3") / total_cells

IF l2_percentage < 0.30 → DEPTH-INSUFFICIENT (L2)
IF l3_percentage < 0.10 → DEPTH-INSUFFICIENT (L3)
```

**Why this matters:** The Trigger Matching Layer operates exclusively on L3 data. An agent that produces L1-dominant output (e.g., 80% L1, 15% L2, 5% L3) cannot feed the matching engine regardless of research quality. The 30%/10% thresholds are minimum viable depth — they ensure enough structural ground exists for four-axis matching.

**Gate:** Hard fail. An L1-dominant profile is returned to the operator with diagnostic details on which segments and categories lack depth.

---

#### Law 3 — Tribal Language

**Requirement:** Every extracted term must fail the genericness test to qualify. Minimum 10 in-group terms, 5 rejection terms across all segments.

**Genericness test:** If a marketing consultant outside this specific tribe could have written the same term, it fails. "Self-care" is generic. "Matembélé" is tribal. "Accountability partner" is generic. "The 3am feed and the silence afterward" is tribal.

**Why this matters:** Tribal language is the surface of the activation event seed. The coach must encounter the audience's reality in the exact words the audience uses internally — not the professional translation of those words. When the activation event uses the audience's exact words, the coach recognizes the terrain immediately and sub-cortically, not after translation (Context_Premise_Trigger_Matching_Layer §Part 4 Component 2).

**Gate:** Below 10 in-group terms and 5 rejection terms → LANGUAGE-INSUFFICIENT. Return to research for deeper immersion in audience spaces.

---

#### Law 4 — Data Provenance

**Requirement:** Every insight must trace to a verifiable source. Accepted sources: research finding, forum post (with URL), interview transcript (with timestamp), social media thread (with reference), survey response.

**Prohibited:** LLM inference from secondary sources. Insights that "seem likely" based on aggregated industry knowledge. Assumptions about audience behavior not grounded in observed data.

**Why this matters:** Inferred audience behavior produces inferred structural matches. The Trigger Matching Layer will construct activation event seeds from this data. If the L3 data is inferred rather than observed, the structural match is built on phantom coordinates — the coach's dual-layer encoding will be activated at the wrong position on the map. The content may feel relevant but will lack the credibility signal that fires at Clark's structural ground level.

**Gate:** Any insight without a verifiable source reference → PROVENANCE-UNVERIFIED. More than 20% unverified insights → PROVENANCE-FAILED.

---

### Phase 5: EMIT — Output Generation

**Output artifact structure:**

```json
{
  "theme": "content_theme_string",
  "generated_at": "ISO8601",
  "agent_version": "1.0",
  "standing_dep_eng_006_version": "reference to standing Context Premise Map version used",
  "segments": [
    {
      "segment_id": "string",
      "dhd_label": "Deep Human Desire label",
      "coping_trajectory_position": "SEARCH|ACTIVE|EXHAUSTED",
      "regulatory_focus": "promotion|prevention|mixed",
      "primary_moral_foundation_violated": "MFT label",
      "categories": {
        "wants": [{ "text": "", "depth": "L1|L2|L3", "source": "", "tribal_terms": [], "two_am_test": false }],
        "frustrations": [],
        "dreams": [],
        "fears": [],
        "suspicions": [],
        "insecurities": [],
        "envy_feelings": [],
        "enemies": [],
        "coping_mechanism": [{ "text": "", "depth": "", "source": "", "tribal_terms": [], "two_am_test": false, "agency_attribution_pattern": "", "coping_potential_assessment": "" }],
        "hidden_beliefs": [{ "text": "", "depth": "", "source": "", "tribal_terms": [], "two_am_test": false, "public_contradiction": "" }],
        "emotional_triggers": [{ "text": "", "depth": "", "source": "", "tribal_terms": [], "two_am_test": false, "activation_keywords": [], "moral_foundation": "", "involuntary_response": "" }],
        "success_markers": []
      }
    }
  ],
  "depth_distribution": { "L1": 0.0, "L2": 0.0, "L3": 0.0 },
  "tribal_language_registry": {
    "in_group_terms": [{ "term": "", "context": "", "example_usage": "" }],
    "rejection_terms": [{ "term": "", "why_rejected": "", "what_to_use_instead": "" }]
  },
  "four_laws_status": {
    "law_1_lived_reality": "PASS|FAIL",
    "law_2_depth_stratification": "PASS|FAIL",
    "law_3_tribal_language": "PASS|FAIL",
    "law_4_data_provenance": "PASS|FAIL",
    "overall_status": "AUTHENTICATED|PROVISIONAL|FAILED"
  },
  "provenance_report": {
    "total_insights": 0,
    "verified_count": 0,
    "unverified_count": 0,
    "provenance_percentage": 0.0
  }
}
```

**Verdict logic:**
- ALL 4 Laws PASS → **AUTHENTICATED** — ready for Trigger Matching Layer consumption
- 3 Laws PASS → **PROVISIONAL** — usable with flags, operator warned
- ≤2 Laws PASS → **FAILED** — cannot feed downstream stages, return to operator for deeper research

**Write receipt** → Receipt Chain Guard (Audience Empathy Agent — Phase 5 Emit)

---

## The Three Structurally Weighted Categories — Why They Matter

The Context_Premise_Trigger_Matching_Layer (§Part 2) identifies three of the 12 categories as carrying disproportionate structural weight for the Trigger Matching Layer's Four-Axis Structural Matching Engine:

| Category | Why It Carries Structural Weight | What It Provides to Trigger Matching |
|---|---|---|
| **Hidden Beliefs** | These are the beliefs the audience holds that contradict their public position. They represent the cognitive architecture underneath the surface narrative — the thing they know is true but cannot say. | The hidden belief is the precise location where the coach's original formative experience and the audience's current reality are most likely to share structural ground. |
| **Emotional Triggers** (array) | These are the specific activation events that produce involuntary emotional response in the audience — not topics but mechanisms. Expressed as an array because each trigger is a discrete structural unit. | Each trigger in the array is a candidate seed for the Trigger Matching engine. The match is evaluated at the structural level, not the thematic level. |
| **Coping Mechanism** | This describes what the audience does when the pain becomes unmanageable. It reveals their agency attribution pattern and their coping potential assessment — two of the four structural matching axes. | A coach whose trigger was formed while using the same coping mechanism the audience is currently using has exact positional congruence on the map. Not similar. Identical. |

These three categories must receive enhanced extraction depth:
- Minimum 2 L3-verified entries per structurally weighted category per segment (18 total across all segments)
- Hidden beliefs must include the public/private contradiction
- Emotional triggers must include activation keywords, moral foundation, and involuntary response
- Coping mechanisms must include agency attribution pattern and coping potential assessment

---

## Integration with Downstream Systems

### Trigger Matching Layer (Downstream Consumer)

The Audience Empathy Agent's output feeds directly into Stage 2 of the 9-stage architectural flow (Context_Premise_Trigger_Matching_Layer §Part 5):

| Stage | System | This Agent's Role |
|---|---|---|
| 1. Audience Research | **Audience Empathy Agent (THIS)** | Produces the theme-specific Context Premise: 6 segments × 12 categories, L1/L2/L3 stratified, tribal language extracted, 2am test verified |
| 2. L3 Extraction | Trigger Matching Layer — Input Processing | Receives THIS agent's output and extracts L3 structural coordinates: moral foundation violations, coping mechanism patterns, agency attribution patterns, hidden beliefs in tribal language, emotional triggers array |
| 3. Coach Emotional DNA | Emotional DNA Extraction System | Coach-side processing (independent of this agent) |
| 4. Structural Match | Four-Axis Engine | Uses L3 structural coordinates from Stage 2 + Coach Emotional DNA from Stage 3 |
| 5-9 | Downstream stages | Seed construction → Coach activation → Content generation |

### Standing Context Premise Map (DEP-ENG-006) — Input

The theme-specific Context Premise does not replace DEP-ENG-006. It is a focused extraction *from* DEP-ENG-006, enriched with theme-specific fresh intelligence. The standing map is the atlas; each theme-specific extraction is a focused route through that atlas.

When fresh audience intelligence is available (recent forum data, current events), the agent enriches the standing map's entries with current context. These enrichments are theme-ephemeral — they exist only in the theme-specific output, not persisted back to the standing DEP-ENG-006.

---

## Tasks

- [ ] **Task 1:** Implement Phase 1 INGEST — loading DEP-ENG-006, tribe profile, coach soul, fresh audience intelligence, and theme context. Include pre-flight gate for DEP-ENG-006 existence.
- [ ] **Task 2:** Implement Phase 2 SEGMENT — 6-segment identification engine with DHD mapping, coping trajectory position, regulatory focus, and moral foundation classification per segment.
- [ ] **Task 3:** Implement Phase 3 EXTRACT — 6×12 matrix population with per-cell depth classification (L1/L2/L3), source provenance, tribal term extraction, and 2am test markers.
- [ ] **Task 4:** Implement enhanced extraction for structurally weighted categories — Hidden Beliefs (public/private contradiction), Emotional Triggers (activation keywords, moral foundation, involuntary response array), Coping Mechanism (agency attribution pattern, coping potential assessment).
- [ ] **Task 5:** Implement Phase 4 Law 1 — Lived Reality (2am test) enforcement with LIWC-22 authenticity scoring for L3 classification verification. Define computational 2am test criteria using Mind After Midnight markers.
- [ ] **Task 6:** Implement Phase 4 Law 2 — Depth Stratification enforcement with L2 ≥30% / L3 ≥10% computation and hard-fail gating.
- [ ] **Task 7:** Implement Phase 4 Law 3 — Tribal Language enforcement with genericness test, minimum 10 in-group terms, 5 rejection terms.
- [ ] **Task 8:** Implement Phase 4 Law 4 — Data Provenance enforcement with verifiable source requirement and ≤20% unverified threshold.
- [ ] **Task 9:** Implement Phase 5 EMIT — output artifact generation with full 6×12 matrix, depth distribution, tribal language registry, Four Laws status, provenance report, and authentication verdict.
- [ ] **Task 10:** Implement integration point with Trigger Matching Layer — ensure output artifact schema is consumable by the Four-Axis Structural Matching Engine's L3 extraction stage (Stage 2 of 9-stage flow).
- [ ] **Task 11:** Implement theme-specific freshness enrichment — mechanism for incorporating recent forum data, current events, and weekly voice note context into standing DEP-ENG-006 entries without persisting back to the standing map.

---

## Acceptance Criteria

- [ ] **AC1 (Prerequisite Gate):** Pipeline halts with descriptive error when standing Context Premise Map (DEP-ENG-006) does not exist. Error message directs operator to complete FR6 first.
- [ ] **AC2 (Segment Count):** Exactly 6 audience segments produced per theme. Each segment has a unique `segment_id`, DHD label, coping trajectory position, regulatory focus, and moral foundation classification.
- [ ] **AC3 (Matrix Completeness):** 6 segments × 12 categories = minimum 72 cells populated. No empty cells. Each cell contains at least 1 insight with text, depth, source, and tribal terms.
- [ ] **AC4 (Depth Stratification — Law 2):** L2 ≥30% AND L3 ≥10% of all insights. A profile with 80% L1 / 15% L2 / 5% L3 → FAILED (L3 <10%). Display actual depth distribution in output.
- [ ] **AC5 (2am Test — Law 1):** Every L3-classified insight has `two_am_test: true` and is verified against LIWC-22 authenticity markers. An insight tagged L3 without passing the 2am test → reclassified to L2 or L1.
- [ ] **AC6 (Tribal Language — Law 3):** ≥10 in-group terms and ≥5 rejection terms in the tribal language registry. Each term fails the genericness test: a marketing consultant outside this tribe could NOT have written it.
- [ ] **AC7 (Data Provenance — Law 4):** Every insight has a verifiable source reference. ≤20% unverified insights → PROVENANCE-PASS. >20% → PROVENANCE-FAILED.
- [ ] **AC8 (Structural Weight Categories):** Hidden Beliefs include `public_contradiction` field. Emotional Triggers include `activation_keywords[]`, `moral_foundation`, and `involuntary_response`. Coping Mechanism includes `agency_attribution_pattern` and `coping_potential_assessment`. Minimum 2 L3-verified entries per structurally weighted category per segment.
- [ ] **AC9 (Authentication Verdict):** Output classified as AUTHENTICATED (4/4 Laws PASS), PROVISIONAL (3/4), or FAILED (≤2/4). FAILED output cannot feed the Trigger Matching Layer — hard gate.
- [ ] **AC10 (DHD Mapping):** Each segment maps to a distinct DHD from the reference library. No two segments share the same DHD + coping trajectory position combination.
- [ ] **AC11 (Trigger Matching Layer Compatibility):** Output artifact passes schema validation for consumption by the Four-Axis Structural Matching Engine. Specifically: L3 entries for emotional triggers contain activation keywords and moral foundation — the data fields required for Axis 1 (Moral Foundation) and Axis 4 (Temporal Position) matching.
- [ ] **AC12 (Fresh Intelligence Integration):** When fresh audience data is provided (recent forums, current events), the output incorporates theme-relevant enrichments without modifying the standing DEP-ENG-006.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR6 — Tribe Profile & Context Premise Map (DEP-ENG-006) | Internal prerequisite | Standing Context Premise Map must exist before this agent can run |
| `tribe_profile_distilled.json` | Internal prerequisite | FR6 Stage B output — standing distilled tribe profile |
| `coach_soul.json` | Internal prerequisite | Coach voice DNA for alignment verification |
| LIWC-22 scoring | License | For Law 1 — 2am test authenticity verification of L3 entries |
| DHD Reference Library | Internal reference | Deep Human Desire labels for segment mapping |
| Receipt Chain Guard | Infrastructure | Receipts at INGEST and EMIT phases |
| Trigger Matching Layer | Downstream consumer | Consumes the output for 4-axis structural matching |

---

## Testing Strategy

### Unit Tests
- **Depth distribution computation:** 72 synthetic cells with known depth assignments → verify L2% and L3% calculations. Test edge cases: exactly 30% L2 / 10% L3 → PASS. 29% L2 → FAIL.
- **2am test classification:** 6 synthetic L3 candidates: 3 with LIWC-22 authenticity ≥70th percentile (PASS), 3 with authenticity <70th percentile (reclassified to L2).
- **Genericness test:** 10 synthetic terms: "self-care" → FAIL (generic). "Matembélé" → PASS (tribal). "Accountability partner" → FAIL. "The 3am feed and the silence afterward" → PASS.
- **Provenance validation:** 20 synthetic insights: 16 with verifiable source (80%) → PROVENANCE-PASS. Set 5 without source (75%) → PROVENANCE-FAILED.
- **Segment boundary validation:** 2 synthetic segments sharing identical hidden beliefs AND coping mechanisms → detected as duplicate, error raised.
- **Structural weight enforcement:** Hidden belief entry without `public_contradiction` → schema validation fails. Emotional trigger without `moral_foundation` → schema validation fails.

### Integration Tests
- **Full pipeline execution:** Provide synthetic theme + standing DEP-ENG-006 → validate: 6 segments produced, 72+ cells populated, depth distribution within thresholds, Four Laws evaluated, authentication verdict computed, output artifact schema-valid for Trigger Matching Layer.
- **Downstream compatibility:** Feed output artifact into Trigger Matching Layer L3 extraction module → verify L3 structural coordinates (moral foundations, coping patterns, agency attributions) are correctly extracted from the theme-specific Context Premise.
- **Fresh intelligence enrichment:** Run agent twice on same theme: once without fresh data, once with synthetic forum data → verify second output contains enriched entries without modifying standing DEP-ENG-006.

### Safety Tests
- **FAILED profile gate:** Submit a FAILED (≤2 Laws) Context Premise to the Trigger Matching Layer → must be rejected with descriptive error before any matching occurs.
- **L1-dominant rejection:** Submit a profile with 85% L1 / 12% L2 / 3% L3 → agent correctly identifies DEPTH-INSUFFICIENT, returns diagnostic details on which segments lack depth.
- **Inference detection:** Submit 5 insights with sources like "likely based on industry trends" or "inferred from similar audiences" → agent correctly flags as PROVENANCE-UNVERIFIED.
