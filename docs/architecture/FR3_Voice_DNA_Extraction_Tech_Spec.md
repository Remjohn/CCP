# Tech-Spec: FR3 — 3-Dimensional Voice DNA Extraction

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §7 (JIT Skill Compiler & CCSB — Block A), §7.6 (Script Generation Skill Type Guide, Mandates 4 & 8), §11.5 (Quality Gates), §12.3 (V5.0 Onboarding Prerequisites)

---

## Overview

### Problem Statement

Voice DNA extraction is the most critical operation in the entire Genesis Pipeline. Everything downstream — every script generated for every archetype, every CBCS interaction, every webinar slide — is compiled from what this pipeline produces. Failure here produces a platform that generates content that doesn't sound like the coach. Success here produces a platform that generates content the coach reads and says: *"I couldn't have written this better myself."*

The challenge: the voice is not in the words. It's in the syntactic substructure beneath the words — the functional skeleton that remains invariant when the coach discusses maximally different topics. A topic-specific style tic is not Voice DNA. An invariant syntactic fingerprint across 5 different subjects IS Voice DNA. This distinction requires a 10-step extraction pipeline, not a single-pass transcription analysis.

### Solution

A 10-step agentic extraction pipeline that processes the validated Authentic Material Payload (≥3,000 words from FR2) into two dependency objects: the Negative Space Object (DEP-ENG-004) and the Positive Space Object (DEP-ENG-003). The pipeline enforces Mandate 4 (Negative Space before Positive Space), runs adversarial validation, and concludes with a V5.0 extension that seeds the Cultural Memory Map (DEP-ENG-023) and Coach Story Archive (DEP-ENG-024) using the same source material — eliminating a separate onboarding session.

### Scope

**In scope:**
- Complete 10-step Voice DNA extraction pipeline
- Two output objects: DEP-ENG-003, DEP-ENG-004
- Cross-Topic Invariance Test
- Mandate 4 enforcement: DEP-ENG-004 extracted before DEP-ENG-003
- Adversarial Validation (Step 12)
- V5.0 extension: CMM extraction trigger (Step 0-A) and Story Archive seeding (Step 0-B)
- Humor Spec Block (Mandate 8) — populated from DEP-ENG-003 analysis
- Storage to `coach_soul.json` and Supabase

**Out of scope:**
- Emotional DNA Object extraction (DEP-LIB-001). This is owned exclusively by FR4. FR3 terminates at DEP-ENG-003 and DEP-ENG-004 emission.
- Sacred Audio ingestion (FR2 Tech Spec — prerequisite)
- Context Premise extraction (FR4 — separate spec)
- CMM extraction pipeline (Step 0-A — referenced here but defined in its own spec)
- Story Archive extraction pipeline (Step 0-B — referenced here but defined in its own spec)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-003` | Positive Space (60-Variable Stylometry Profile) | PRIMARY OUTPUT — extracted in FR3 |
| `DEP-ENG-004` | Negative Space (Forbidden Vocabulary + Structural Exclusions) | PRIMARY OUTPUT — extracted in FR3 (BEFORE DEP-ENG-003 per Mandate 4) |
| `DEP-ENG-019` | Session Transcript Intelligence | INPUT — the validated Authentic Material Payload from FR2 |
| `DEP-ENG-023` | Cultural Memory Map | DOWNSTREAM — extraction triggered after Step 12 completes (Step 0-A) |
| `DEP-ENG-024` | Coach Story Archive | DOWNSTREAM — seeding triggered after Step 12 completes (Step 0-B) |
| `DEP-PROTO-015` | Humor Mechanism Tagging Protocol | DOWNSTREAM INPUT — Mandate 8 Block A Humor Spec fields populated here |

### Script Generation Skill Type Guide — Relevant Mandates (§7.6)

| Mandate | Requirement | How Satisfied in This Pipeline |
|---|---|---|
| **Mandate 4** | DEP-ENG-004 (Negative Space) MUST be built before DEP-ENG-003 (Positive Space) | Steps 6-7 extract DEP-ENG-004. Steps 8-10 extract DEP-ENG-003. Pipeline enforced — Steps 8-10 cannot start if Step 7 has not produced a valid DEP-ENG-004 object. |
| **Mandate 7** | Emotional DNA Integration Test before filing | Step 11: inject L3 wound architecture. Test: would someone in this wound recognize their experience in the first 30 words of generated sample? |
| **Mandate 8** | Block A Humor Spec fields must be populated | Step 10-B: Humor Style Classification (Architecture 6 inputs) derived from DEP-ENG-003 and logged to `coach_soul.json`. |

### Key Files to Reference

| File | Purpose |
|---|---|
| `coach_soul.json` | Primary output target — DNA objects written here at completion |
| `coach_soul.json → extraction_readiness.authenticated_word_count` | Prerequisite gate — must be ≥3,000 before this pipeline starts |
| `Supabase: coach_soul_json` | Persistent storage backup |
| `Supabase: cultural_memory_map` | Populated post-FR3 via Step 0-A |
| `Supabase: coach_story_archive` | Seeded post-FR3 via Step 0-B |
| `ttt_baseline.json` | Secondary output — Sophia's calibration baseline for TTT drift gate |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Mandate 4 as a pipeline gate, not a principle** | DEP-ENG-003 generation with an LLM is guided by DEP-ENG-004 as a constraint. If DEP-ENG-004 doesn't exist, the LLM fills the void with its own priors (the centroid problem). The gate enforces this computationally — not by agent instruction. |
| **Cross-Topic Invariance (Steps 4-5)** | A topic-specific style tic (e.g., short sentences only when angry) is NOT Voice DNA. DNA is what remains invariant when maximally different topics are compared. This test is the single hardest quality gate in the pipeline — it's also the single most valuable one. |
| **Adversarial Validation as a quality gate** | An LLM trained to find fault with a voice profile catches drift that rule-based validation misses. The Adversary is prompted with a hostile brief: "Find any sentence or structure that the coach would disown." This is structurally different from Sophia's TTT drift check, which measures alignment, not failure. |
| **Humor Style Classification at extraction time** | Architecture 6 (Voice Style Humor Classifier) requires `affiliative`/`self_enhancing` classification from the coach's source material. This is most accurate when freshly extracted from Sacred Audio — the same authentic material used for stylometry. |

---

## Implementation Plan

### Prerequisite Gate

**Condition:** `coach_soul.json → extraction_readiness.authenticated_word_count ≥ 3000`

If not met → pipeline does not start. Morgan (Setup Orchestrator) queues a notification encouraging more Sacred Audio sessions.

---

### Step 1: Corpus Assembly

**Agent:** Valeriane (Client Soul Extractor)

**Action:** Load all validated Thought_Units from `DEP-ENG-019` (all sessions to date). Concatenate into a single extraction corpus. Tag each unit with `session_id` and `unit_type`.

**Output:** `extraction_corpus.json` — unified array of Thought_Units with metadata

**Gate:** Minimum 3,000 unique authenticated words (not total, not with duplicates collapsed). If below threshold after deduplication → halt, request more Sacred Audio.

**Receipt Write (Stage 1):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-1",
  "previous_receipt_hash": "{FR2_FINAL_RECEIPT}",
  "input_payload_hash": "{FR2_PAYLOAD_HASH}",
  "output_payload_hash": "{EXTRACTION_CORPUS_HASH}",
  "stage_name": "VDNA-CORPUS-ASSEMBLY",
  "agent_name": "Valeriane",
  "timestamp": "{ISO8601}" }
```

---

### Step 2: Discourse Marker Census

**Agent:** Valeriane + spaCy POS tagging

**Action:** Scan the full corpus for transitional glue words: `actually`, `so`, `look`, `right`, `I mean`, `you know`, `basically`, `literally`. For each:
- Count total occurrences
- Map their syntactic position: sentence-opening, sentence-middle, clause-bridging
- Calculate the position distribution (e.g., "so" appears 73% at sentence-opening, 27% mid-sentence)

**Output:** `discourse_marker_map.json` — each marker with occurrence count + position distribution

**Receipt Write (Stage 2):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-2",
  "previous_receipt_hash": "{STEP_1_RECEIPT_HASH}",
  "input_payload_hash": "{EXTRACTION_CORPUS_HASH}",
  "output_payload_hash": "{DISCOURSE_MARKER_MAP_HASH}",
  "stage_name": "DISCOURSE-MARKER-CENSUS",
  "agent_name": "Valeriane",
  "timestamp": "{ISO8601}" }
```

---

### Step 3: Cross-Topic Invariance Test

**Agent:** Valeriane

**This is the hardest and most important step in the pipeline.**

**Action:**
1. From the corpus, identify 5 maximally different subject clusters (e.g., professional development, personal health, relationships, finances, industry critique)
2. Run Step 2's discourse marker analysis separately for EACH cluster
3. Compare results: a marker's position distribution must remain consistent (within ±15%) across all 5 clusters to qualify as Voice DNA
4. Markers with >15% variance across clusters → flagged as TOPIC-SPECIFIC, excluded from DEP-ENG-003
5. Only invariant markers advance to DEP-ENG-003

**Gate:** Minimum 12 invariant markers required to produce a robust DEP-ENG-003. If fewer than 12 invariant markers: expand corpus (more Sacred Audio) or broaden subject clusters.

**Receipt Write (Stage 3):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-3",
  "previous_receipt_hash": "{STEP_2_RECEIPT_HASH}",
  "input_payload_hash": "{DISCOURSE_MARKER_MAP_HASH}",
  "output_payload_hash": "{INVARIANT_MARKERS_HASH}",
  "stage_name": "CROSS-TOPIC-INVARIANCE",
  "agent_name": "Valeriane",
  "timestamp": "{ISO8601}" }
```

---

### Step 4: Sentence Skeleton Extraction (Stylometry Profiling)

**Agent:** Valeriane + spaCy dependency parser

**Action:** Strip all content nouns and verbs from each Thought_Unit. Retain only: function words, conjunctions, prepositions, determiners, pronouns, punctuation, and discourse markers. Calculate:
- **Type-Token Ratio (TTR)** — lexical diversity
- **Hapax Legomena Frequency** — unique word density
- **WAN Metrics** — Function Word Adjacency Networks: transition probabilities between prepositions and conjunctions
- **WPS Flow** — Word-Per-Sentence pattern (rhythm of sentence length changes)
- **Punctuation Density** — em-dashes per 100 words, ellipsis frequency, comma position patterns
- **Function Word Ratios** — and/but/so density as fraction of total function words

These 6 cluster groups form the core of the **Positive Space Object (60-variable profile)**.

**Receipt Write (Stage 4):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-4",
  "previous_receipt_hash": "{STEP_3_RECEIPT_HASH}",
  "input_payload_hash": "{CORPUS_HASH}",
  "output_payload_hash": "{STYLOMETRY_PROFILE_HASH}",
  "stage_name": "SENTENCE-SKELETON-EXTRACT",
  "agent_name": "Valeriane",
  "timestamp": "{ISO8601}" }
```

---

### Step 5: Negative Space Excavation (MANDATE 4 — First DEP)

> **GATE: This step must complete and produce a validated DEP-ENG-004 before subsequent steps can execute. This is hardcoded in the pipeline orchestrator — not a prompt instruction.**

**Agent:** Valeriane

**Mechanism:** Mathematical extrapolation of the opposite of the invariant markers from Step 3.

**Three components of DEP-ENG-004:**

**A. Lexical Blacklist** — Words never used by the coach in the corpus. Categorized:
- Academic vocabulary (words present in 0% of corpus but common in coaching content generally)
- Spiritual vocabulary (words present in coaching discourse generally but absent from this coach's corpus)
- Superlatives and intensifiers the coach never uses (`absolutely`, `incredibly`, `amazing`, `transformative`)

**B. Syntactic Impossibilities** — Structural patterns the coach never employs:
- Derived from the sentence skeleton analysis: patterns with zero occurrence across all subject clusters
- Format: `"The coach NEVER {syntactic pattern}"`
- Examples: *"The coach never opens a thought with a rhetorical question."* / *"The coach never ends on a resolved, neat summary."*

**C. Structural Exclusions** — Macro-level content structures never present:
- Content opening types the coach never uses (thesis-first declaration, motivational quote lead, statistic-first hook)
- Closing patterns the coach never uses (CTA-explicit close, listicle summary, callback-to-opening close)

**DEP-ENG-004 JSON structure:**
```json
{
  "lexical_blacklist": {
    "academic": ["leverage", "paradigm", "holistic", "synergy"],
    "spiritual": ["journey", "manifest", "universe", "vibration"],
    "banned_intensifiers": ["absolutely", "incredibly", "amazing"]
  },
  "syntactic_impossibilities": [
    "Opens thought with rhetorical question",
    "Uses passive voice for personal experience claims",
    "Ends with resolved, tidy summary"
  ],
  "structural_exclusions": {
    "forbidden_openings": ["thesis-first declaration", "motivational quote lead"],
    "forbidden_closings": ["CTA-explicit close", "listicle summary bullet points"]
  }
}
```

**Receipt Write (Stage 5):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-5",
  "previous_receipt_hash": "{STEP_4_RECEIPT_HASH}",
  "input_payload_hash": "{EXTRACTED_PATTERNS_HASH}",
  "output_payload_hash": "{DEP_ENG_004_HASH}",
  "stage_name": "NEGATIVE-SPACE-EXCAVATION",
  "agent_name": "Valeriane",
  "timestamp": "{ISO8601}" }
```

---

### Steps 6-8: Positive Space Extraction (DEP-ENG-003)

**Prerequisite gate:** DEP-ENG-004 exists in `coach_soul.json`

**Agent:** Valeriane

**The 5 stylometry cluster groups → DEP-ENG-003:**

| Cluster | Variables | Source Data |
|---|---|---|
| **Lexical/Morphological** | TTR, hapax legomena frequency, vocabulary density | Step 4 calculations |
| **Subconscious Syntactic Distributions** | Function word ratios (and/but/so densities), clause connective patterns | Step 3 invariant markers |
| **Relational WAN Metrics** | Preposition-conjunction transition probabilities, adjacency network map | Step 4 WAN calculations |
| **Graphical Habits** | Punctuation density (em-dash frequency, ellipsis position, comma load), capitalization anomalies | Step 4 punctuation profiling |
| **Structural Complexity** | WPS flow pattern (rhythm of sentence length changes across claims), paragraph-to-paragraph length variance | Step 4 WPS tracking |

**Construction method:** For each cluster, generate the numerical profile AND a prose description suitable for inclusion in Block A of compiled SKILL.md files. The prose description is what the generation agent reads — it translates the mathematical profile into a voice instruction.

**Step 8: Humor Style Classification (Mandate 8 input)**

Post-DEP-ENG-003: analyze the coach's natural expressions in corpus for humor signals:
- Frequency and position of self-referential humor attempts
- Frequency of observational irony vs self-deprecation vs absurdist references
- Presence/absence of aggressive humor targeting (classify per Architecture 6 — `affiliative`/`self_enhancing`/`aggressive`/`self_defeating`)
- Write `humor_style_classification` to `coach_soul.json` → Block A Humor Spec fields

**Receipt Write (Stage 6-8):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-6-8",
  "previous_receipt_hash": "{STEP_5_RECEIPT_HASH}",
  "input_payload_hash": "{STYLOMETRY_CLUSTER_HASH}",
  "output_payload_hash": "{DEP_ENG_003_HASH}",
  "stage_name": "POSITIVE-SPACE-EXTRACT",
  "agent_name": "Valeriane",
  "timestamp": "{ISO8601}" }
```

---

### Step 9: Emotional DNA Integration Test (Mandate 7)

**Prerequisite gate:** DEP-LIB-001 must exist from FR4 execution.

**Agent:** Valeriane + Charlotte (Stream of Consciousness Generator)

**Action:**
1. Inject the coach's full DEP-LIB-001 wound architecture (L3 emotional layer: top moral foundation violation + trigger specificity threshold)
2. Generate 3 opening sample sentences using DEP-ENG-003 + DEP-ENG-004 as constraints
3. Evaluate: do the samples activate the wound architecture rather than describe it?

**Test criterion (Mandate 7):** *Would someone who shares this coach's specific wound architecture recognize their own experience in the first 30 words?*

If no → Charlotte rewrites with deeper L3 activation instructions. Cycle repeats up to 3 times.
If 3 cycles fail and Mandate 7 criterion is not met → flag for operator review (this is a signal of a corpus that doesn't contain enough wound-level material — more Sacred Audio required).

**Receipt Write (Stage 9):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-9",
  "previous_receipt_hash": "{STEP_8_RECEIPT_HASH}",
  "input_payload_hash": "{DEP_LIB_001_HASH}_AND_DEP003_DEP004",
  "output_payload_hash": "{FAILED_OR_PASSED_SAMPLES_HASH}",
  "stage_name": "EMOTIONAL-DNA-TEST",
  "agent_name": "Charlotte",
  "timestamp": "{ISO8601}" }
```

---

### Step 10: Adversarial Validation

**Agent:** Sophia (TTT validator) + Adversarial Validator Agent

**Action:**
1. Generate 5 sample outputs using the newly compiled Voice DNA (DEP-ENG-003 + DEP-ENG-004)
2. **Sophia:** Measures TTT alignment — drift score < 15% required
3. **Adversarial Validator:** Independent hostile evaluation. Brief: *"You are trying to find a single phrase or sentence structure that the coach would disown. Scan all 5 samples. If you find one, flag it with the specific structure and why the coach would reject it."*
4. If Adversary flags nothing → Voice DNA passes. Write to `ttt_baseline.json`.
5. If Adversary flags a phrase → pipeline rewinds to Step 5 to harden the Negative Space. The flagged structure is added to DEP-ENG-004's `synactic_impossibilities` list.
6. Maximum 3 rewind cycles. After 3 cycles without passing → operator review required.

**Quality gates applied at Step 10:**
- TTT drift < 15% (Sophia — §11.5)
- AI detection rate < 5% on all 5 samples (Chen — §11.5)
- Boredom Ban: each sample ≤0.85 cosine similarity to any existing content in episodic memory (§11.5)

**Receipt Write (Stage 10):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-VDNA-10",
  "previous_receipt_hash": "{STEP_9_RECEIPT_HASH}",
  "input_payload_hash": "{ADVERSARIAL_SAMPLES_HASH}",
  "output_payload_hash": "{TTT_BASELINE_HASH}",
  "stage_name": "ADVERSARIAL-VALIDATION",
  "agent_name": "Adversarial Validator",
  "timestamp": "{ISO8601}" }
```

Write DEP-ENG-003 + DEP-ENG-004 + `ttt_baseline.json` to `coach_soul.json` and Supabase.

---

### V5.0 Extension: Post-Step 12 Onboarding Chain

When Step 12 passes, the extraction pipeline has completed. The V5.0 onboarding prerequisites (§12.3) now proceed in order:

**Step 0-A (CMM Extraction):** Morgan (Setup Orchestrator) triggers the CMM extraction pass. Uses the same Sacred Audio corpus plus onboarding questionnaire outputs. Populates `Supabase: cultural_memory_map` with ≥4 of 7 CMM layers. Completion criteria: ≥3 entries per populated layer, operator review, confirmation.

**Step 0-B (Story Archive Seeding):** Morgan triggers the structured story extraction interview via Telegram. Coach's most significant transformation stories, client testimonial moments, and industry experience narratives are extracted and structured using the Hartian 5-element schema. Each story tagged by mechanism type, arc phase fit, CRAL moment fit, emotional register. DEP-PROTO-016 approval gate run for each entry. Completion criteria: ≥3 approved entries across ≥2 story types.

**Step 0-C (Humor Mechanism Registry):** Create empty `humor_mechanism_registry` table entry for this coach. Architecture 10 variety gate is now operational.

**Step 0-D (Context Performance Registry):** Create empty `context_performance_registry` table entry. Confidence score defaults to routing rules until ≥5 sessions are recorded.

**Production unlock:** The Minister of Identity (§6.3) generates the Leadership Scorecard from DEP-ENG-003 + DEP-ENG-001. Production pipeline is locked until the Leadership Scorecard meets all coverage requirements (5 trait categories, each explicitly addressed).

---

## Tasks

- [ ] **Task 1:** Build corpus assembly and prerequisite gate (authenticated word count check)
- [ ] **Task 2:** Implement Discourse Marker Census with position mapping
- [ ] **Task 3:** Implement Cross-Topic Invariance Test (5-cluster comparison, ±15% variance threshold)
- [ ] **Task 4:** Implement Sentence Skeleton Extraction with spaCy (6 cluster variable groups)
- [ ] **Task 5:** Implement Negative Space Excavation (DEP-ENG-004) with 3-component structure + pipeline gate enforcing Mandate 4
- [ ] **Task 6-8:** Implement Positive Space Extraction (DEP-ENG-003) — 5 clusters → numerical profile + prose description
- [ ] **Task 7:** Implement Humor Style Classification (Step 8) → Block A Humor Spec fields
- [ ] **Task 8:** Implement Emotional DNA Integration Test (Mandate 7 — 3-cycle limit) with prerequisite mapping to FR4
- [ ] **Task 9:** Implement Adversarial Validation with Sophia + Adversarial Validator + 3-rewind limit
- [ ] **Task 10:** Implement V5.0 Post-Step-10 onboarding chain trigger (Step 0-A through 0-D) + Minister of Identity scorecard gate
- [ ] **Task 11:** Integrate Receipt Chain Guard at every step with hash chaining

---

## Acceptance Criteria

- [ ] **AC1 (Gate):** Pipeline does not start when `authenticated_word_count < 3000`. When word count = 3000, pipeline starts within the same Morgan execution cycle.
- [ ] **AC2 (Mandate 4):** If Step 7 (DEP-ENG-004 output) is manually deleted and Steps 8-10 are triggered, the pipeline halts with a `DEP-ENG-004_NOT_FOUND` error (not a prompt failure — a code-level gate).
- [ ] **AC3 (Cross-Topic Invariance):** Given a synthetic corpus with 3 intentionally topic-specific markers and 15 invariant markers, the test correctly classifies all 3 as TOPIC-SPECIFIC and excludes them from DEP-ENG-003.
- [ ] **AC4 (Negative Space completeness):** DEP-ENG-004 produced from a real corpus contains all 3 components: lexical_blacklist (≥3 entries per category), syntactic_impossibilities (≥3), structural_exclusions (≥2 openings + ≥2 closings).
- [ ] **AC5 (Mandate 7):** Test Emotional DNA Integration Test with a deliberately "safe" opening sample. The evaluator must flag it as failing Mandate 7. After 1 Charlotte rewrite cycle, sample passes.
- [ ] **AC6 (Adversarial Validation pass):** A complete Voice DNA built from 3,500 authenticated words produces 5 samples. Adversarial Validator finds no flaggable structures. TTT drift < 15%. AI detection < 5% on all 5 samples. Pipeline writes to `ttt_baseline.json`.
- [ ] **AC7 (Adversarial rewind):** An intentionally weak Negative Space (no syntactic impossibilities) causes the Adversary to flag a sample. Pipeline rewinds to Step 7. Flagged structure is added to DEP-ENG-004. Second pass with hardened Negative Space: Adversary finds nothing — pass.
- [ ] **AC8 (Humor Classification):** Step 10-B correctly classifies a corpus with no aggressive/self-defeating patterns as `affiliative + self_enhancing` and writes this to `coach_soul.json`.
- [ ] **AC9 (V5.0 chain):** Step 12 completion triggers Step 0-A activation within same execution cycle. Morgan receives trigger. `cultural_memory_map` Supabase table entry is created.
- [ ] **AC10 (Production lock):** Without a complete Leadership Scorecard (Minister of Identity), any attempt to trigger the CCF production pipeline returns `PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD`.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR2 Sacred Audio Ingestion pipeline | Internal prerequisite | Must be complete with ≥3,000 authenticated words |
| spaCy dependency parser | Python package | en_core_web_sm + locale variants |
| LIWC-22 dictionary | License | Used in Step 4 (discourse markers) — already loaded in FR2, share instance |
| MFQ-2 scoring dictionary | Internal | Must be embedded in Valeriane's skill |
| Charlotte (Stream of Consciousness Generator) | Agent | Required for Step 11 sample generation |
| Sophia (TTT Validator) | Agent | Required for Step 12 drift gate |
| Adversarial Validator | Agent | New agent — must be configured with hostile brief |
| Moses (Minister of Identity) or equivalent | Agent | Required for Leadership Scorecard gate |
| Receipt Chain Guard | Infrastructure | All 12 steps must write linked receipts |

---

## Testing Strategy

### Unit Tests
- MFQ-2 scoring: 20 synthetic coach statements with pre-coded foundation alignments → validate scoring
- Cross-Topic Invariance: 2 synthetic corpora (one with clear topic-locked markers, one with genuinely invariant patterns) → validate classification
- Mandate 4 gate: code-level test that DEP-ENG-003 extraction function throws error when DEP-ENG-004 is empty

### Integration Tests
- Full 12-step run on a synthetic 3,500-word corpus (human-written coaching material) → validate all 3 DEP objects are populated in `coach_soul.json`
- Adversarial rewind cycle: intentionally weaken Negative Space → validate rewind triggers and hardening adds new entries

### Quality Validation
- Voice DNA output evaluated by reading 5 Adversary-passed samples without context: a human coach who knows the source material should confirm alignment ≥4 out of 5 samples

### V5.0 Chain Test
- Simulate Step 12 completion → verify Step 0-A is triggered, Step 0-C creates empty registry tables, and Minister of Identity is activated with source materials
