# Tech-Spec: FR1 — Genesis Pipeline — Coach Onboarding & First Production Session

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §5.2 (Corrected Intake Flow), §5.3 (Genesis Pipeline), §5.4 (Weekly Pipeline), §12.3 (V5.0 Onboarding Prerequisites), §12.4 (V5.0 Build Sub-Steps), §5.8 (Standing Trigger Intelligence Library)

---

## Overview

### Problem Statement

The Genesis Pipeline is not a feature — it is the entire foundation of the CCP. Every dependency object, every compilation instruction, every intelligence layer downstream is built during or immediately after Genesis. A Genesis Pipeline that completes incorrectly produces a platform that generates content at scale that doesn't sound like the coach. There is no recovery from a bad foundation — it must be rebuilt from scratch.

The legacy Genesis Pipeline (v1) had two critical architectural flaws:
1. **Wrong initiation model:** It described production as beginning when the coach submits a trigger via Telegram. This is architecturally incorrect in V5.0. The Scheduled Monitor Agent initiates production by identifying culturally relevant tensions and presenting the coach with an observation. The coach responds. The response becomes the session input.
2. **Missing V5.0 dependency chain:** The original 7-stage Trigger-First model had no pathway for Cultural Memory Map (DEP-ENG-023), Coach Story Archive (DEP-ENG-024), Humor Mechanism Registry, or Context Performance Registry initialization. These are V5.0 required tables — without them, the Memetic Engine, Context Reasoning Layer, and Data Analyst cycles have no substrate to operate on.

### Solution

A complete 3-phase Genesis architecture:
- **Phase 0 (Onboarding):** Sacred Audio extraction, Voice DNA compilation, V5.0 data infrastructure initialization, Leadership Scorecard — all must pass before any production content is generated.
- **Phase 1 (Corrected Weekly Production):** Scheduled Monitor Agent initiates; coach responds with authenticity; CRAL executes; Context Reasoning Layer reasons; generation compiles deterministically.
- **Phase 2 (Standing Library Seeding):** First 8 sessions populate the Standing Trigger Intelligence Library with quality-gated research evidence. Compounding begins.

### Scope

**In scope:**
- Complete Phase 0 onboarding sequence (Sacred Audio through Production Unlock)
- V5.0 dependency initialization (CMM, Story Archive, Humor Registry, CPR)
- Corrected V5.0 Weekly Production Flow (all phases A through E)
- Standing Trigger Intelligence Library seeding rules
- Scheduled Monitor Agent setup (Step 11-A)
- Production unlock gates (Leadership Scorecard + minimum DEP completion)
- Acceptance criteria and testing strategy

**Out of scope:**
- Sacred Audio ingestion mechanics (FR2 Tech Spec — prerequisite)
- Voice DNA extraction mechanics (FR3 Tech Spec — prerequisite)
- CBCS real-time pipeline (separate spec)
- V²WS webinar pipeline (separate spec)

---

## Context for Development

### Architecture Traceability

| DEP-ID / DEP-PROTO | Name | Role in Genesis |
|---|---|---|
| `DEP-ENG-003` | Positive Space (Voice DNA) | Required before production phases — produced by FR3 |
| `DEP-ENG-004` | Negative Space | Required before production phases — produced by FR3 |
| `DEP-LIB-001` | Emotional DNA | Required before production phases — produced by FR3 |
| `DEP-ENG-001` | Tribe Soul | Produced by `ccf-tribe-extract` (Dilaya) |
| `DEP-ENG-005` | Trigger Taxonomy | Governs trigger classification, used from M1 onward |
| `DEP-ENG-021` | Human Evidence Bias Protocol | Gate for all CRAL research entering Standing Trigger Library |
| `DEP-ENG-023` | Cultural Memory Map | V5.0 — Initialized in Step 0-A (post-FR3) |
| `DEP-ENG-024` | Coach Story Archive | V5.0 — Initialized in Step 0-B (post-Step 0-A) |
| `DEP-ENG-045` | Context Performance Registry | V5.0 — Initialized in Step 0-D |
| `DEP-ENG-052` | Genesis Clearance Certificate | Prerequisite gate — issued by Guardian Agent after FR0A-FR0E sequence |
| `DEP-PROTO-014` | CMM Extraction Protocol | Step 0-A execution protocol |
| `DEP-PROTO-016` | Story Archive Approval Gate | Step 0-B quality gate |

### Agent Roster for Genesis

| Agent | Phase | Role |
|---|---|---|
| **Morgan** | Phase 0 | Setup Orchestrator — coordinates all Phase 0 commands |
| **Valeriane** | Phase 0 | Client Soul Extractor — Voice DNA, emotional mapping |
| **Kimya** | Phase 0 | Business Analyst — onboarding elicitation |
| **Dilaya** | Phase 0 | Tribe Soul Extractor — DEP-ENG-001 |
| **Emmanuel** | Phase 0 | Strategy Architect — content pillars + philosophy brief + blueprint |
| **Minister of Identity (Sophia-Identity)** | Phase 0 | Leadership Scorecard + production lock gate |
| **Scheduled Monitor Agent** | Phase 1 | V5.0 — daily community surveillance, session initiation |
| **Alex** | Phase 1 | Content Orchestrator — weekly batch commands 8-28 |
| **Divine** | Phase 1 | Theme Discoverer |
| **CRAL Research Team** | Phase 1 | M1-M7 execution (7 skills across 9 analysts) |
| **Research Planner V4.0** | Phase 1 | Context Reasoning Layer — checks Story Archive + CMM + CPR |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Scheduled Monitor Agent initiates production, not coach** | Architecture §5.2 Corrected Intake Flow. The coach doesn't identify what's culturally relevant — the system does. The coach's judgment matters most at the response step, not the initiation step. |
| **V5.0 tables initialized at zero, not skipped** | All 4 V5.0 tables must exist before the first production session even if they are empty. An empty Context Performance Registry is architecturally correct. A missing one breaks the Context Reasoning Layer. |
| **Standing Library seeding threshold = 8 sessions** | Per §12.3 Data Analyst monthly cycle: meaningful library depth requires ≥8 sessions. Sessions 1-7 are the seeding phase — library grows but is not yet sufficient for pattern-level intelligence. |
| **Production unlock requires Leadership Scorecard** | Architecture §5.3: `leadership_scorecard.json` must exist before ANY production pipeline runs. This is not advisory — it is a hard gate enforced by Morgan's orchestrator. |
| **Onboarding Steps 0-A through 0-D are run by Morgan, not manually** | Human-initiated onboarding steps introduce sequencing errors. Morgan orchestrates Steps 0-A through 0-D programmatically after FR3 completion is confirmed. |

---

## Implementation Plan

---

### Phase 0: Onboarding — Sequence & Gate Architecture

Phase 0 consists of 7 commands + 4 V5.0 initialization steps. All must complete before any Phase 1 (production) run is authorized.

#### Phase 0, Step 1: `ccf-init`

**Agent:** Morgan
**Action:** Initialize workspace structure, `config.yaml`, coach registry entry. Create Supabase tables for this coach (`coach_soul_json`, `memory_episodic`, `receipts`, `content_performance`).
**Creates:** `config.yaml`, workspace directory structure, empty Supabase tables
**Completion gate:** `coach_registry.json` created with `coach_id` and `status: onboarding`

---

#### Phase 0, Step 2: `ccf-elicit`

**Agent:** Kimya (Business Analyst) + Valeriane
**Extensions:** `SoulResonance`
**Action:** Business context elicitation via structured interview protocol. 5 domains: business model, coaching niche, audience demographics, transformation promise, growth targets.
**Output:** `01_business_canvas.md`
**Completion gate:** Receipt written. `01_business_canvas.md` exists.

---

#### Phase 0, Step 3: `ccf-soul-extract` → triggers FR2 + FR3

**Agent:** Valeriane (coordinated by Morgan)
**Action:** This command initiates the Sacred Audio ingestion + Voice DNA extraction pipeline. FR2 (Sacred Audio) and FR3 (Voice DNA) execute as sub-processes. Morgan monitors and cannot proceed until both complete.

**Sub-process: FR2 Sacred Audio**
- Minimum: 15+ seconds per voice note, accepted formats (.ogg/.mp3/.m4a)
- LIWC-22 gate: ≥7/10 authenticity threshold
- Exit condition: ≥3,000 authenticated words accumulated

**Sub-process: FR3 Voice DNA**
- 12-step extraction pipeline
- Mandate 4 enforced: DEP-ENG-004 before DEP-ENG-003
- Adversarial Validation: TTT drift <15%, AI detection <5%
- Exit condition: all 3 DEP objects written to `coach_soul.json`

**Output:** `coach_soul.json` (with DEP-ENG-003, DEP-ENG-004, DEP-LIB-001) + `ttt_baseline.json`
**Completion gate:** Receipt chain intact (FR2 stages A-E + FR3 steps 1-12). `coach_soul.json` has all 3 DEP objects populated.

---

#### Phase 0, Step 4: `ccf-tribe-extract` (FR6)

**Agent:** Dilaya (Tribe Soul Extractor)
**Extensions:** `InteractComp`
**Action:** Structured tribe analysis across 8 cultural layers. Source: onboarding questionnaire + social listening data + coach's described audience.
**Output:** `tribe_soul.json` (DEP-ENG-001)
**Completion gate:** Receipt written. DEP-ENG-001 populated with 8 cultural layers.

---

#### Phase 0, Step 4.5: `ccf-trigger-extract` (FR5)

**Agent:** Trigger Map Builder
**Action:** Synthesizes FR2/FR3 inputs into 7 primary trigger categories.
**Output:** `trigger_map.json` (DEP-LIB-002)
**Completion gate:** Receipt written. Trigger Map populated and validated.

---

#### Phase 0, Step 5: `ccf-pillar-build`

**Agent:** Emmanuel (Strategy Architect)
**Action:** Define content pillars from Voice DNA + Tribe Soul intersection. Pillars are not topics — they are recurring audience tension territories that the coach's identity architecture is equipped to resolve.
**Output:** Content Pillar document (5 pillars minimum)
**Completion gate:** Receipt written. Pillars reviewed by operator.

---

#### Phase 0, Step 6: `ccf-philosophy-brief`

**Agent:** Emmanuel
**Action:** Extract the coach's philosophical position from the Soul extraction material. Not their opinion — their worldview architecture: how they understand causality, what they believe about human potential, what institutional structures they fundamentally oppose.
**Output:** Philosophy framework document
**Completion gate:** Receipt written.

---

#### Phase 0, Step 7: `ccf-blueprint`

**Agent:** Emmanuel
**Action:** Synthesize all Phase 0 extraction objects into a production content strategy.
**Output:** `02_content_strategy.md`
**Completion gate:** Receipt written. `02_content_strategy.md` exists.

---

#### Phase 0, Step 7.5: `ccf-leadership-score` → Production Lock Gate

**Agent:** Minister of Identity
**Action:** Score the coach across 12 Leadership Traits (Deep Empathy, Authentic Vulnerability, Embodied Confidence, etc.) using signal sources from `coach_soul.json`, `ttt_baseline.json`, `tribe_soul.json`.
**Output:** `leadership_scorecard.json`
**Completion gate (PRODUCTION LOCK):** `leadership_scorecard.json` must exist AND must cover all 5 minimum trait categories before Morgan will authorize any production pipeline run. This is a hard code gate — not a prompt instruction.

**Format assignments derived from Leadership Scorecard:** Weak traits receive more exercise content, strong traits receive more showcase content. Format weighting written to `02_content_strategy.md`.

---

#### Phase 0, Step 0-A: CMM Extraction (V5.0)

**Trigger:** FR3 Step 12 passes (Voice DNA complete)
**Protocol:** DEP-PROTO-014 CMM Extraction
**Action:** Morgan runs the CMM extraction pass using all onboarding source material (Sacred Audio transcripts, business canvas, tribe soul, philosophy brief). Operator reviews all 7 CMM layer entries.
**Output:** `Supabase: cultural_memory_map` — populated with ≥4 of 7 layers, ≥3 entries per layer
**Completion gate:** Operator confirms all entries via Telegram review prompt. CMM is NOT written automatically — the Agent identifies, the operator decides.

**7 CMM Layers:**
1. Formative Texts & Works
2. Collective Wound History
3. Industry Mythology
4. Generational Signature
5. Linguistic Template Library
6. Aspirational Archetype
7. Shared Enemy Typology (input for Memetic Engine Architecture 9 — Tribal Sync Targeting)

---

#### Phase 0, Step 0-B: Coach Story Archive Seeding (V5.0)

**Trigger:** Step 0-A confirmed complete
**Protocol:** DEP-PROTO-016 Story Archive Approval Gate
**Action:** Morgan dispatches a structured story extraction interview via Telegram. Coach is asked for 5 categories of stories: personal transformation moments, professional failures, client breakthrough testimonials, inflection points, and collective wound experiences.

Each story is structured using the Hartian 5-element schema:
1. Protagonist status (what was the coach's position/state before)
2. Moment of contact (the specific event or encounter)
3. Internal shift (the precise moment of realization)
4. Outcome (what changed as a result)
5. Tribal markers (phrases, references, or cultural touchstones the audience will recognize)

**DEP-PROTO-016 Approval Gate:** Each story is reviewed and the operator approves/rejects each entry.
**Tagging:** Each approved story tagged with: `story_type`, `mechanism_tag`, `arc_phase_fit`, `cral_moment_fit`, `emotional_register`
**Completion gate:** ≥3 approved entries across ≥2 story types

---

#### Phase 0, Step 0-C: Humor Mechanism Registry Init (V5.0)

**Action:** Create empty `humor_mechanism_registry` table entry for this coach. `coach_id` initialized. No entries yet — populated after first production sessions.
**Completion gate:** Table entry exists (status: initialized)

---

#### Phase 0, Step 0-D: Context Performance Registry Init (V5.0)

**Action:** Create empty `context_performance_registry` table entry. `coach_id` initialized. Confidence score defaults to routing rules until ≥5 sessions are recorded.
**Completion gate:** Table entry exists (status: initialized, confidence_model: default_routing_rules)

---

#### Phase 0, Step 11-A: Scheduled Monitor Agent Setup (V5.0)

**Action (Build Step 11-A from §12.4):** Configure and activate the Scheduled Monitor Agent:
1. Define the coach's community monitoring channels (Instagram, LinkedIn, TikTok, Facebook Group)
2. Set monitoring cadence: daily (default 6:00 AM coach timezone)
3. Wire monitor output to M1 RELEVANT source hierarchy in CRAL — community signals become the first evidence layer for M1
4. Configure output format: Telegram observation delivery to coach via structured message format:
   - `Observation:` [specific cultural tension observed]
   - `Question:` [DARN-CAT formatted question linking the tension to the coach's trigger architecture]
5. Wire Scheduled Monitor Agent to the `semantic_affinity` pipeline for cultural NOW validation

**Completion gate:** Agent is live. A test observation runs successfully and delivers a correctly formatted Telegram message to the coach instance.

---

### Phase 0 — Completion Summary & Production Unlock

Production unlock criteria (all must be TRUE before Alex can trigger Phase 1):

| Gate | Required | Check |
|---|---|---|
| Genesis Clearance Certificate (DEP-ENG-052) | ✅ Required | Guardian Agent issuance proof via DEP-PROTO-019/020 success |
| `coach_soul.json` with DEP-ENG-003, DEP-ENG-004, DEP-LIB-001 | ✅ Required | FR3 completion receipt |
| `ttt_baseline.json` | ✅ Required | FR3 Step 12 receipt |
| `tribe_soul.json` (DEP-ENG-001) | ✅ Required | `ccf-tribe-extract` receipt |
| `trigger_map.json` (DEP-LIB-002) | ✅ Required | `ccf-trigger-extract` receipt |
| `02_content_strategy.md` | ✅ Required | `ccf-blueprint` receipt |
| `leadership_scorecard.json` | ✅ Required | `ccf-leadership-score` receipt |
| `cultural_memory_map` — ≥4 layers populated | ✅ Required | Step 0-A operator confirmation |
| `coach_story_archive` — ≥3 approved entries | ✅ Required | Step 0-B DEP-PROTO-016 gate |
| `humor_mechanism_registry` — initialized | ✅ Required | Step 0-C initialization |
| `context_performance_registry` — initialized | ✅ Required | Step 0-D initialization |
| Scheduled Monitor Agent — live | ✅ Required | Step 11-A verification |
| Genesis Unlock Receipt | ✅ Required | Global Receipt Chain Guard format |

**Receipt Write (Genesis Unlock):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-GENESIS-UNLOCK",
  "previous_receipt_hash": "{LAST_PHASE_0_RECEIPT}",
  "input_payload_hash": "{SCORECARD_HASH}",
  "output_payload_hash": "{CLEARANCE_CERT_HASH}",
  "stage_name": "GENESIS-UNLOCK",
  "agent_name": "Guardian Agent",
  "timestamp": "{ISO8601}" }
```

---

### Phase 1: Corrected Weekly Production Flow (V5.0)

> **Critical:** The coach does NOT initiate production. The Scheduled Monitor Agent does.

#### Phase 1, Step 0: System Initiation (Scheduled Monitor)

**Agent:** Scheduled Monitor Agent (daily cadence)
**Action:**
1. Monitors coach's community channels for cultural tensions, emerging debates, and audience signal patterns
2. Cross-references signals with `semantic_affinity` table (audience trending domains)
3. Cross-references signals with CMM Layer 3 (Industry Mythology) and Layer 7 (Shared Enemy Typology) from `cultural_memory_map`
4. Generates one observation + one DARN-CAT question and delivers it via Telegram to the coach

**Output:** Coach receives a Telegram message framing a specific cultural moment and asking for their genuine reaction.

#### Phase 1, Step 1: Coach Authentic Response

**Channel:** Telegram voice note (preferred) or text
**Gate:** If voice note → runs through FR2 LIWC-22 gate (not the full extraction pipeline — just authenticity verification for this session input). If score <7/10 → system asks a deeper OARS question. If text → bypasses LIWC-22 gate, proceeds directly.
**Output:** Authenticated coach response becomes the M1 RELEVANT source material for this production session.

#### Phase 1, Steps 2-3: Phase A (Discovery & Research) — CRAL Execution

**Commands:** `ccf-theme-discover` → `ccf-radar` → `ccf-raw-research` → `ccf-relevance-check` → `ccf-research-deep` → `ccf-research-fresh`

**CRAL M1–M7 research sequence (7 JIT moments):**

| CRAL Moment | Focus | Agent(s) |
|---|---|---|
| M1 RELEVANT | Cultural NOW confirmation from Monitor research | Scheduled Monitor output + Tshala |
| M2 RECOGNIZED | Audience recognition bridge — what makes them feel seen | Lila + Maeva |
| M3 RIGOROUS | Evidence depth — academic/practitioner validation | Lionel + Remgion |
| M4 RESONANT | Story Archive query: does DEP-ENG-024 contain a first-person story for this CRAL moment? If yes → prioritize over external research | Research Planner + Story Archive query |
| M5 RELEVANT-PROOF | Mechanism proof — specific named examples, regulations, organizations | Research Planner + Firecrawl/Tavily |
| M6 RELATIONSHIP | Trust bridge — coach credibility signal for this specific audience segment | Lila + Atlas |
| M7 RITUAL | Standing Trigger Library query: existing evidence for this trigger category + moment | CRAL Research Planner |

**Context Reasoning Layer (Phase 1 upgrade — from §12.4 Step 11-B):**
Before compiling the research directive, the Research Planner V4.0 asks 3 questions:
1. Does `coach_story_archive` contain a first-person story that outperforms external research for M4 RESONANT?
2. Which CMM layers have the strongest performance history for this audience in this trigger category and arc phase?
3. Which humor mechanism has the strongest precedent for this arc phase and regulatory frame?

Answers logged as Context Selection Object → `context_performance_registry`.

#### Phase 1, Steps 4-5: Phase B (Ideation & Mapping)

**Commands:** `ccf-vibe-comments` → `ccf-question` → `ccf-analyze` → `ccf-timing-check` → `ccf-eroll-plan`

**Psychological Routing:**
- `ccf-question` (Lila) extracts CCF Context Premise JSON — the audience's active internal monologue for this content cycle
- `ccf-analyze` produces `ideas.json` with 12 viral concept candidates
- `ccf-timing-check` (Minister of Timing) validates seasonal calendar alignment (4-layer influence stack)
- `ccf-eroll-plan` (Emmanuel) assigns 36 format assignments across archetypes using `leadership_scorecard.json` weighting

**Memetic Engine integration at this phase:**
- For each of the 36 assignments, the Block A compilation includes Memetic Engine architecture fields (per Mandate 8 + §12.4 Step 11-C)
- Architecture 1 (BVT) → violation_target drawn from DEP-ENG-004 + DEP-ENG-005
- Architecture 3 (Arc-Phase Coupling) → arc phase confirmed from `ccf-eroll-plan` output
- Architecture 9 (Tribal Sync) → Enemy Typology from CMM Layer 7
- Architecture 14 (Cultural Pre-Loading) → CMM queried FIRST before `semantic_affinity`

#### Phase 1, Steps 6-8: Phase C/D (Production & Validation)

**Commands:** `ccf-eroll-research` → `ccf-soc` → `ccf-anti-draft` → `ccf-generate` → `ccf-wisdom` → `ccf-adapt` → `ccf-visual` → `ccf-visual-assets` → `ccf-validate`

**Anti-Draft Protocol:**
1. Less capable model (same context as Cesare) generates 36 anchors
2. Cesare receives: anchor + 5-Point Contrastive Anchor Protocol + Voice DNA (DEP-ENG-003 + DEP-ENG-004) + CRAL research + Block A Humor Spec
3. Generation executes deterministically — not descriptive prompting

**Validation (all 3 must pass):**
- Sophia (Minister of Identity): TTT drift <15%
- Marcus (Minister of Timing): Seasonal calendar alignment ≥0.3 timing_score
- Chen (AI Detector): AI detection rate <5%

**Humor Mechanism Tagging (Step 11-D from §12.4):**
Post-generation, each script receives `humor_mechanism_tag` JSONB appended to `content_performance` table. This is the data source for Architecture 12 (Feedback Loop) and the Data Analyst weekly cycle.

#### Phase 1, Steps 9-10: Phase E (Orchestration & Memory)

**Commands:** `ccf-batch` → `ccf-weekly` → `ccf-memory` → `ccf-tierlist`

**Memory promotion:** Azaria (Sunday Archivist) promotes validated intelligence from Working → Episodic → Semantic tiers per the 3-tier memory architecture.

**Notion delivery:** All 36 validated scripts + Tierlist output + Visual assets delivered to coach's Notion workspace. Each script includes:
- Original coach voice note (linked)
- "Why This Post" section tracing to coach's Telegram response
- Leadership Farming notes (trait exercise or showcase designation)
- Receipt chain link (full audit trail)

---

### Phase 2: Standing Trigger Intelligence Library Seeding

Per §5.8 Standing Trigger Intelligence Library:

**Sessions 1-8:** Each CRAL research run populates the library with quality-gated evidence. Entry gate:
- Quality score ≥0.65 (MCDA from Research Analyst self-evaluation)
- Human Evidence Bias gate (DEP-ENG-021): minimum 3 verified real-person examples
- Cultural NOW window check: entry date within freshness window for the trigger category

**Trigger category indexing:** Library entries indexed by the 7 trigger categories (Worth, Transformation, Certainty, Belonging, Authority, Resistance, Legacy) — NOT by archetype. This is a hard constraint enforced at ingestion.

**By Session 8:** Library contains ≥8 sets of quality-gated evidence across the coach's primary trigger categories. Monthly Story Gap Report (Data Analyst) begins generating meaningful analysis.

**Compounding economics:** Session 9 onward, the Research Planner has 90% of M7 RITUAL evidence already researched for frequently-used trigger categories. CRAL execution time decreases. Directive quality increases.

---

## Tasks

- [ ] **Task 1:** Implement Morgan orchestrator with Phase 0 gate checks (production lock enforcement)
- [ ] **Task 2:** Build `ccf-init` command — workspace creation, Supabase table initialization
- [ ] **Task 3:** Build `ccf-elicit` command — Kimya 5-domain business elicitation
- [ ] **Task 4:** Build `ccf-soul-extract` command — coordinates FR2 + FR3 sub-processes with receipt monitoring
- [ ] **Task 5:** Build `ccf-tribe-extract` command — Dilaya 8-layer tribe analysis
- [ ] **Task 6:** Build `ccf-pillar-build`, `ccf-philosophy-brief`, `ccf-blueprint` commands
- [ ] **Task 7:** Build `ccf-leadership-score` command + Minister of Identity trait scoring + production lock gate (code-level, not prompt)
- [ ] **Task 8:** Implement Step 0-A (CMM extraction protocol DEP-PROTO-014 + operator confirmation flow)
- [ ] **Task 9:** Implement Step 0-B (Story Archive extraction interview + Hartian schema + DEP-PROTO-016 gate)
- [ ] **Task 10:** Implement Steps 0-C and 0-D (empty table initialization for Humor Registry + CPR)
- [ ] **Task 11:** Build and deploy Scheduled Monitor Agent (community monitoring, DARN-CAT question generation, Telegram delivery) — Step 11-A
- [ ] **Task 12:** Implement Context Reasoning Layer in Research Planner V4.0 (3-question sequence + Context Selection Object logging) — Step 11-B
- [ ] **Task 13:** Implement Memetic Engine Block A integration in CCSB compilation (Architecture fields 1-14) — Step 11-C
- [ ] **Task 14:** Implement `humor_mechanism_tag` post-assembly tagging — Step 11-D
- [ ] **Task 15:** Implement Standing Trigger Intelligence Library ingestion with trigger-category indexing + entry gate

---

## Acceptance Criteria

- [ ] **AC1 (Production Lock):** Without a complete `leadership_scorecard.json`, triggering `ccf-batch` returns `PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD` from Morgan's gate — not a prompt failure.
- [ ] **AC2 (V5.0 Tables):** After Step 0-C and 0-D complete, `humor_mechanism_registry` and `context_performance_registry` exist in Supabase for the coach's `coach_id` — even if empty. Querying them returns empty arrays (not errors).
- [ ] **AC3 (CMM Completion Gate):** Attempting to trigger Phase 1 without Step 0-A operator confirmation fails with `CMM_NOT_CONFIRMED` error.
- [ ] **AC4 (Scheduled Monitor Initiation):** A production session cannot be initiated via manual coach Telegram trigger. Only the Scheduled Monitor Agent can initiate a production session. Manual trigger returns: *"Got it — I'll work this into the next batch. Your weekly session starts when I identify the right cultural moment for this."*
- [ ] **AC5 (Context Reasoning Layer):** A production session where `coach_story_archive` contains a relevant M4 story selects that story over external research and logs `story_archive_used: true` in the Context Selection Object.
- [ ] **AC6 (Library Indexing):** A research finding submitted with `archetype_id` as the primary index key is rejected at ingestion. Library accepts only `trigger_category_id` as the primary key.
- [ ] **AC7 (Library Entry Gate):** A research finding with quality score 0.60 (below 0.65) is discarded at the end of the session. It is not saved to the library. A finding with quality score 0.65 is saved.
- [ ] **AC8 (Humor Tagging):** After `ccf-generate` completes, every generated script has a `humor_mechanism_tag` JSONB field populated in `content_performance`. An empty tag is not acceptable (if no humor architecture fires, the tag should contain `{"architectures_fired": [], "reason": "no_applicable_mechanism"}`)
- [ ] **AC9 (Full Genesis Receipt Chain):** After complete Phase 0, all receipts from `ccf-init` through Step 0-D are stored in Supabase `receipts` table with resolvable predecessor_receipt fields. A receipt chain integrity check passes end-to-end.
- [ ] **AC10 (TTT Alignment):** Generated scripts from the first production session score TTT drift <15% against `ttt_baseline.json`. Test: generate 5 scripts, run Sophia validation — all 5 pass without manual revision.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR2 Sacred Audio Ingestion | Internal prerequisite | Must complete before `ccf-soul-extract` can complete |
| FR3 Voice DNA Extraction | Internal prerequisite | Must complete before production phases |
| Groq API | External service | Transcription in FR2 sub-process |
| Google Gemini API | External service | Generation agent (Cesare) |
| Supabase | External service | All storage targets |
| Neo4j | External service | Context Premise graph (CCF Context Premise) |
| Redis | External service | Message queue, state management |
| Telegram Bot API | External service | Coach communication, re-elicitation |
| Publer API | External service | Social content scheduling (Phase E) |
| LangGraph | Internal framework | Agent orchestration + extension hooks |

---

## Testing Strategy

### Phase 0 Integration Test
- Run complete Phase 0 against a test coach instance with synthetic Sacred Audio (pre-certified as authentic)
- Validate: all 10 production unlock gate conditions pass
- Validate: Receipt chain A through Step 0-D is intact

### Phase 1 Integration Test
- Simulate Scheduled Monitor Agent identifying a cultural tension → deliver Telegram message → submit test coach voice response → run Phase 1 A through E
- Validate: Context Selection Object logged in `context_performance_registry`
- Validate: All 36 scripts pass Sophia + Marcus + Chen validation
- Validate: `humor_mechanism_tag` populated on all 36 scripts

### Data Isolation Test
- Run complete Genesis for Coach A and Coach B simultaneously
- Validate: Coach A's CMM, Story Archive, Voice DNA never appear in Coach B's compilation

### Performance Test
- Phase 0 complete: <12 hours calendar time (most of this is coach's Sacred Audio recording sessions — system processing time should be <30 min across all steps)
- Phase 1 (weekly batch): complete within 30 minutes autonomous running
- Scheduled Monitor Agent: Telegram prompt delivered within 2 minutes of daily monitoring cycle completion

