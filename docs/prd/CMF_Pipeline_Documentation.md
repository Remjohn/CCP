# CMF Pipeline — Complete Architecture & Sequential Execution Guide

> **Version:** v3.0 Documentation
> **Date:** 2026-03-23
> **Purpose:** Document the complete Conscious Movie Factory pipeline — the system that transforms a single coach testimonial transcript into a fully-orchestrated cinematic short film with synchronized A-roll storyboards, B-roll motion graphics, ambient cinema, AI-generated music, and automated video assembly via the 9-module Video Pipeline.

---

## Executive Summary

The CMF pipeline converts raw coach-client testimonial transcripts (typically 15-45 minute interviews) into 60-90 second cinematic short films. Unlike the CCF pipeline (which produces text scripts for social media), the CMF produces **visual production assets** and now **finished video files** — storyboard prompts, motion graphic prompts, ambient cinema prompts, music lyrics, beat timing data, and fully-rendered MP4 outputs at three quality tiers (preview 540p, review 720p, final 1080p).

The pipeline operates in **3 phases** across **30 commands** powered by **75 specialized skills** organized into **11 skill families**. Phase 1 (narrative + visual prompt composition) produces **75+ output files** per project. Phase 2 generates static assets. Phase 3 — the **Automated Video Pipeline** — orchestrates 9 Python modules with 22 JSON schemas, 6 constraint gates, and a 16-state lifecycle machine to assemble raw assets into rendered video. Backed by **480 automated tests**.

---

## The 13-Arc Routing System

Every CMF project is governed by a narrative arc detected from the transcript. The arc determines which specific Hunter, Analyst, Composer, and Commander skills are loaded — ensuring that quote extraction, enrichment, premise composition, and validation are all structurally aligned to the story's emotional architecture.

| Arc | Emotional Engine | Cluster Structure |
|-----|-----------------|-------------------|
| The Witness | Emotional breakdown → witnessed healing | W1-W5 (HOOK → PROBLEM → MECHANISM → PROOF → CLOSE) |
| The Breakthrough | Epiphany → sudden insight | B1-B6 |
| The Shared Struggle | Community → collective healing | SS1-SS5 |
| The Confrontation | Callout → uncomfortable truth | C1-C5 |
| The Core Transformation | Origin story → identity shift | CT1-CT6 |
| The Warning | Cautionary tale → prevention | WA1-WA5 |
| The Rally | Comeback → resilience proof | R1-R5 |
| The Divine Spark | Spiritual awakening → purpose | DS1-DS5 |
| The Call to Adventure | Hero's journey → leap of faith | CA1-CA5 |
| The Ticking Clock | Urgency → deadline pressure | TC1-TC5 |
| The Comedic Reframe | Humor → reframed insight | CR1-CR5 |
| The Sacred Return | Full circle → homecoming | SR1-SR5 |
| The Quiet Reflection | Contemplation → gentle wisdom | QR1-QR5 |

> [!IMPORTANT]
> The arc selection is not decorative. It determines the physical structure of the entire video — which quotes get extracted, how the premise is assembled, what emotional beats drive the storyboard, and how the music's tempo curve is shaped. Choosing the wrong arc produces a structurally incoherent film.

---

## The 11 Skill Families

| Family | Count | Purpose |
|--------|-------|---------|
| `core/` | 3 | Foundation: Story Doctor (arc diagnosis), Brand Avatar Builder, Visual Commander |
| `hunters/` | 13 | Arc-specific verbatim quote extraction (24-32 quotes per project) |
| `analysts/` | 13 | V3 enrichment: THEMATIC_FIT, PACING_CLASS, POLARITY, GLUE_SCORE, HIGH_AFFINITY_SEQUENCES |
| `composers/` | 13 | Premise assembly: 60-90 second narrative from enriched quotes |
| `commanders/` | 14 | 14-point authorization: validate or reject premises with actionable feedback |
| `narrative/` | 1 | Beat Cluster Extractor: groups quotes into visual concept clusters with VCPs |
| `visual/` | 4 | Storyboard pipeline: PRIMAL analysis, T/V-Code assignment, 6-block photography prompts |
| `sonic/` | 1 | Sonic Scribe: Suno V5 lyrics with T-Code/V-Code markers |
| `motion/` | 10 | GMG (6 Experts + Composer + Analyst) + CAC (Composer + Analyst) |
| `eroll/` | 18 | E-Roll research: arc-specific deep research + browser-verified asset planning |
| `video/` | 9 | **Automated Video Pipeline:** 9 modules (T2I, I2V, quality gate, fingerprinting, audio, captions, manifest, rendering, orchestration) |

---

## End-to-End Pipeline Flow

```
TRANSCRIPT INPUT
    ↓
[Phase 1A] Arc Detection & Narrative Extraction
    ├─ /cmf-diagnose → 13-arc routing + narrative DNA
    ├─ Brand Avatar → Character Anchor Lock
    ├─ /cmf-hunt → 24-32 verbatim quotes
    ├─ /cmf-analyze → V3 enrichment scoring
    ├─ /cmf-compose → Premise assembly (60-90s)
    ├─ /cmf-authorize → 14-point validation gate
    └─ /cmf-script → Final production script
    ↓
[Bridge] Beat Clustering & Research
    ├─ /cmf-beat-cluster → Visual Cinematic Premises
    └─ /cmf-eroll → Deep research (browser-verified)
    ↓
[Phase 1B] Visual, Sonic & Motion Composition
    ├─ /cmf-storyboard → 26 A-Roll hero frame files
    ├─ /cmf-sonic → Suno V5 music prompt
    ├─ /cmf-motion GMG → 21 B-Roll motion files
    ├─ /cmf-motion CAC → 16 ambient cinema files
    └─ /cmf-visual-auth → Cross-modal authorization
    ↓
[Phase 2] Static Asset Generation
    ├─ T2I generation (OpenRouter / Seedream 4.5)
    ├─ I2V animation (ComfyUI workflows)
    └─ Music generation (Suno V5)
    ↓
[Phase 3] Automated Video Pipeline (cmf-assembler)
    ├─ FR-VID-06 Audio Engine → Whisper + Demucs + ducking
    ├─ FR-VID-02 T2I Generation → RunningHub keyframes
    ├─ FR-VID-04 Quality Gate → CLIP scoring + artifacts
    ├─ FR-VID-03 I2V Generation → RunningHub 48GB clips
    ├─ FR-VID-05 Fingerprinting → Dual-stage tracking + regen
    ├─ FR-VID-01 Manifest Assembly → Beat cluster → Remotion
    ├─ FR-VID-07 Captions → Word-by-word typography
    ├─ FR-VID-08 Rendering → Remotion 3-tier output
    └─ FR-VID-09 Commander → 16-state orchestration + review UI
    ↓
FINAL MP4 OUTPUT (preview 540p → review 720p → final 1080p)
```

---

## Phase 1A: Narrative Extraction (8 Output Files)

Phase 1A transforms the raw transcript into a validated, authorized narrative premise ready for visual production. Every step has a hard dependency on the previous step's output.

### Step 1: `/cmf-diagnose {project_id}` — Story Doctor

**Skill:** `core/story-doctor` | **Input:** Raw transcript
**Process:** Pre-flight verification → 5 diagnostic questions → arc detection via 13-arc decision tree (≥0.75 confidence) → build `narrative_dna` (state_alpha, the_abyss, the_spark, state_omega, sensory_anchors, coach_role) → distill `spr_text` (48-60 word SPR for latent space priming) → 13-point validation gate.

**Output:** `{project_id}_strategy_brief.json`

### Step 2: Brand Avatar Definition

**Tool:** `python tools/generate_brand_avatar.py`
**Input:** Avatar image file (provided by coach)
**Process:** Extract the coach's physical DNA — exact visual description (skin tone, hair, facial features, clothing, body language) that becomes the **Character Anchor Lock** embedded verbatim into every visual prompt downstream.

**Output:** `😎 {project_id} - The Brand Avatar 😎.md`

### Step 3: `/cmf-hunt {project_id}` — Arc-Specific Quote Mining

**Skill:** `hunters/{arc}-hunter` | **Input:** transcript + strategy_brief.json
**Process:** SPR-primed extraction of 24-32 **verbatim** quotes with exact timestamps. Score each on Surprise, Emotion, Specificity (1-10 each, /30 total). 6-point validation gate. **"If it is not in the timecode, it does not exist."**

**Output:** `{project_id}_Quote_Manifest.md`

### Step 4: `/cmf-analyze {project_id}` — V3 Enrichment

**Skill:** `analysts/{arc}-analyst` | **Input:** Quote_Manifest.md
**Process:** Enrich every quote with 6 metadata tags (THEMATIC_FIT, PACING_CLASS, POLARITY, PHILOSOPHICAL_WEIGHT, GLUE_SCORE, HIGH_AFFINITY_SEQUENCES). 8-point validation.
**Output:** `{project_id}_Quote_Manifest_Enriched.md`

### Step 5: `/cmf-compose {project_id}` — Premise Assembly

**Skill:** `composers/{arc}-composer` | **Input:** Quote_Manifest_Enriched.md + strategy_brief.json
**Process:** Select highest-scoring quotes per cluster, assemble into 60-90 second coherent story arc with timing markers and transition types.
**Output:** `{project_id}_premise_analysis.json` + `{project_id}_COMPOSITION_LOG.md`

### Step 6: `/cmf-authorize {project_id}` — 14-Point Validation

**Skill:** `commanders/{arc}-commander` | **Input:** premise_analysis.json + strategy_brief.json
**Process:** 14-point authorization checklist (arc fidelity, emotional coherence, timing integrity, quote accuracy, cluster coverage). Binary: AUTHORIZED or REJECTED with remediation.
**Output:** `{project_id}_{ARC}_AUTHORIZED.md` or `{project_id}_REJECTION.md`

### Step 7: `/cmf-script {project_id}` — Final Script Generation

**Input:** premise_analysis.json (authorized) + strategy_brief.json
**Process:** Scene-by-scene production script with exact quotes, timecodes, visual direction, and transitions. Master document for Phase 1B.
**Output:** `{project_id}_final_script.json` + `SCRIPT_AUTHORIZED.md`

---

## Bridge: Beat Cluster + E-Roll Research

These two commands bridge Phase 1A (narrative) and Phase 1B (visual). They generate the conceptual foundation that the storyboard, motion, and sonic commands need.

### Step 8: `/cmf-beat-cluster {project_id}` — Visual Concept Clusters

**Skill:** `narrative/beat-cluster-extractor` | **Input:** premise_analysis.json + enriched quotes + Brand Avatar
**Process:** Group quotes into narrative beats, derive Visual Cinematic Premises (VCPs) per cluster for storyboard interpretation.
**Output:** `{project_id}_beat_cluster.json`

### Step 9: `/cmf-eroll {project_id}` — E-Roll Deep Research

**Skill:** `eroll/{various planners}` (18 skills) | **Input:** strategy_brief + premise + beat_cluster + Brand Avatar
**Process:** Depth-stratified research (12 questions × 3 levels), browser-based verification (real URLs required), H2/H4 Distillation Gates, 24 culturally-grounded search queries.

> [!WARNING]
> This command **requires real browser access**. If browser tools are unavailable, the command halts.

**Output:** `{project_id}_ERoll_Deep_Research_Report.md` + `{project_id}_search_queries.json`

---

## Phase 1B: Visual, Sonic & Motion Production (63+ Output Files)

Phase 1B reads the narrative assets from 1A and the bridge commands, then generates all the visual, audio, and motion prompts needed for downstream generation.

### Step 10: `/cmf-storyboard {project_id}` — A-Roll Hero Frames (26 files)

**Skills:** `visual/storyboard-architect` → `visual/compassionate-photographer` → `visual/storyboard-commander`
**Process:** PRIMAL analysis (Psychological, Relational, Identity, Metaphorical, Aesthetic, Liminal) → T-Code/V-Code assignment → 6-block photography prompts (Anchor, Contact, Composition, Atmosphere, Imperfection, Lens) → 12-point analyst validation → VFS ≥90 commander authorization.
**Output:** 5 scenes × 5 files (T2I, I2I, I2V, ENRICHED, metadata) + manifest = **~26 files**

### Step 11: `/cmf-sonic {project_id}` — Music Prompt Engineering

**Skill:** `sonic/sonic-scribe` | **Input:** final_script.json + strategy_brief.json
**Process:** Scene-to-music mapping, tempo/mood/instrumentation, T-Code/V-Code lyrics, Suno V5 flow markers. 4-point validation.
**Output:** `{project_id}_suno_prompt.txt` (300-500 words)

### Step 12: `/cmf-motion {project_id}` — GMG + CAC B-Roll (37 files)

**Part A: Generative Motion Graphics (GMG) — 21 files**

**Skills:** `motion/gmg-composer` → 6 Experts → `motion/gmg-analyst`
**Process:** Route scenes to GMG Experts by narrative function (6 palette/vocabulary rule sets). GMG Analyst validates 7 checks (G1-G7).
**Output:** 15 prompt files + 5 enriched + 1 manifest = **21 files** in `prompts/GMG/`

**Part B: Conscious Ambient Cinema (CAC) — 16 files**

**Skills:** `motion/cac-composer` → `motion/cac-analyst`
**Process:** El Shaddai 6-section prompts with 95% Frozen Body motion spec (BODY_STRENGTH: 0.15-0.25). CAC Analyst validates 9 checks (C1-C9).
**Output:** 10 prompt files + 5 enriched + 1 manifest = **16 files** in `prompts/CAC/`

### Step 13: `/cmf-visual-auth {project_id}` — Final 15-Point Visual Authorization

**Skill:** `core/visual-commander` | **Input:** All storyboard, GMG, and CAC files
**Process:** Cross-modal consistency gate (storyboard ↔ GMG ↔ CAC), Brand Avatar DNA persistence, palette coherence.
**Output:** `PROMPTS_AUTHORIZED.md`

---

## Phase 2: Static Asset Generation (Non-LLM)

Phase 2 uses the authorized prompts from Phase 1B to generate actual images, videos, and music via external tools. These are **Python scripts** and external services, not LLM skills.

| Tool | Purpose | Output |
|------|---------|--------|
| `run_batch_prep.ps1` | Populates `SCENES_BATCH.json` for ComfyUI workflows | Batch configuration |
| `cmf_image_generator.py` | T2I/I2I generation via OpenRouter + Seedream 4.5 | Generated images |
| ComfyUI workflows | I2V animation from hero frames (LTX-Video, Wan 2.2) | Generated video clips |
| Suno V5 (external) | Music generation from `suno_prompt.txt` | Generated music track |

**ComfyUI Workflow Library** (`comfyui-workflows/`):
| Workflow | Purpose |
|----------|---------|
| `cmf_t2i_hero.json` | Text-to-image hero keyframe generation |
| `cmf_i2v_distilled.json` | Image-to-video clip generation |
| `cmf_interpolation_i2v.json` | Frame interpolation for smooth transitions |
| `cmf_video_upscale.json` | Video upscaling to final resolution |
| `cmf_image_edit.json` | Selective image editing and inpainting |
| `cmf_gmg_qwen.json` | GMG generation with Qwen image model |

Phase 2 outputs become the inputs to Phase 3's automated video pipeline.

---

## Phase 3: Automated Video Pipeline (`apps/cmf-assembler/`)

Phase 3 is the **fully automated video assembly system** — 9 Python modules governed by 9 tech specs (FR-VID-01 through FR-VID-09), connected by 22 JSON schemas (DEP-VID-001 through DEP-VID-027), protected by 6 constraint gates, and validated by **480 automated tests**. The Pipeline Commander (FR-VID-09) orchestrates the entire flow through a 16-state lifecycle machine.

### Module Execution Order

The modules execute in dependency order. T2I and Audio run in parallel (no data dependency). All other modules are sequential:

| Order | Module | Spec | Gate | Purpose |
|-------|--------|------|------|---------|
| 1 | Audio Engine | FR-VID-06 | Gate I (4Q) | Whisper STT + Demucs separation + ducking curve |
| 2 | T2I Generation | FR-VID-02 | Gate D (5Q) | RunningHub keyframe generation (parallel with audio) |
| 3 | T2I Quality Gate | FR-VID-04 | — | CLIP-based scoring + artifact detection + regeneration verdict |
| 4 | I2V Generation | FR-VID-03 | Gate F (5Q) | RunningHub 48GB video clip generation |
| 5 | Fingerprint & Regen | FR-VID-05 | — | Dual-stage fingerprinting + surgical regeneration plans |
| 6 | Manifest Assembly | FR-VID-01 | Gate E (5Q) | Beat cluster → Remotion video manifest |
| 7 | Caption Engine | FR-VID-07 | — | Word-by-word timed caption components |
| 8 | Remotion Renderer | FR-VID-08 | Gate K (5Q) | 3-tier quality renders (preview/review/final) |
| 9 | Pipeline Commander | FR-VID-09 | Gate L (6Q) | 16-state orchestration + review UI + batch queue |

### FR-VID-06: Audio Engine

**File:** `audio_engine.py` | **Skill:** SKILL-VID-006 | **Gate I** (4Q)
Whisper STT with word-level timestamps, Demucs stem separation, ducking curve computation. Gate I validates file integrity, language, music duration, ducking targets.
**Schemas:** DEP-VID-004, 005 | **Receipt:** `AUDIO_PROCESS`

### FR-VID-02: RunningHub T2I Generation

**File:** `runninghub_client.py` | **Skill:** SKILL-VID-002 | **Gate D** (5Q)
Submits T2I jobs to RunningHub proxy, monitors with exponential backoff, collects keyframes. Gate D validates prompt-PSSL coherence, negative prompts, seed strategy, resolution.
**Schemas:** DEP-VID-007, 008 | **Receipt:** `T2I_GENERATE`

### FR-VID-04: T2I Quality Gate

**File:** `t2i_quality_gate.py` | **Skill:** SKILL-VID-004
CLIP-based scoring (~100ms/image, no VLM cost), artifact detection (blur, banding, overexposure), regeneration verdicts (PASS/REGENERATE/MANUAL_REVIEW).
**Schemas:** DEP-VID-012, 013 | **Receipt:** `T2I_QUALITY_CHECK`

### FR-VID-03: RunningHub I2V Generation

**File:** `runninghub_client.py` | **Skill:** SKILL-VID-003 | **Gate F** (5Q)
I2V on RunningHub 48GB GPU with arc-stage motion presets (e.g., Witness W1 → slow push-in). Requires 48GB VRAM — no 24GB fallback.
**Schemas:** DEP-VID-010, 011 | **Receipt:** `I2V_GENERATE`

### FR-VID-05: Fingerprint & Regeneration Manager

**File:** `fingerprint_tracker.py` + `regeneration_handler.py` | **Skill:** SKILL-VID-005
Dual-stage fingerprints (T2I + I2V per beat), 3 regeneration modes (T2I-only, I2V-only, Both), max 10 attempts per beat, cascade logic for stage re-runs.
**Schemas:** DEP-VID-014, 015, 016 | **Receipts:** `FINGERPRINT_UPDATE`, `REGENERATION_PLAN`

### FR-VID-01: Beat Cluster → Remotion Manifest

**File:** `beat_cluster_parser.py` | **Skill:** SKILL-VID-001 | **Gate E** (5Q)
Parses beat clusters into a declarative Remotion manifest — reviewable and updateable. Gate E validates frame continuity, asset completeness, audio-beat alignment, transition budget, arc sequence.
**Schemas:** DEP-VID-001, 002, 003 | **Receipt:** `MANIFEST_ASSEMBLE`

### FR-VID-07: Caption & Typography Engine

**File:** `caption_engine.py` | **Skill:** SKILL-VID-007
Word-by-word timed captions synchronized to Whisper timestamps, positioned in 9:16 safe zones, styled per arc stage.
**Schemas:** DEP-VID-020, 021 | **Receipt:** `CAPTION_GENERATE`

### FR-VID-08: Remotion Video Composition & Rendering

**File:** `render_orchestrator.py` | **Skill:** SKILL-VID-008
**Input:** Remotion manifest + caption components + all assets
**Process:** Resolves arc-specific Remotion composition templates (3 arc templates: Witness, Breakthrough, Call-to-Adventure), constructs render job specifications, detects Ken Burns fallback beats (static image with CSS pan/zoom when video clip is missing), and processes renders at 3 quality tiers. Gate K validates manifest completeness, asset accessibility, audio-video duration match (±0.5s tolerance), template compatibility, and render budget (final requires prior review approval).

**3-Tier Quality System:**
| Tier | Resolution | Bitrate | CRF | Use Case |
|------|-----------|---------|-----|----------|
| `preview` | 540×960 | 1000 kbps | 32 | Quick feedback (~10s render) |
| `review` | 720×1280 | 2500 kbps | 26 | Operator approval (~30s render) |
| `final` | 1080×1920 | 5000 kbps | 18 | Production output (~2min render) |

**Schemas:** DEP-VID-022 (Arc Template Registry), DEP-VID-023 (Render Job Result), DEP-VID-024 (Render Quality Presets)
**Receipts:** `TEMPLATE_COMPILE`, `VIDEO_RENDER`

### FR-VID-09: Pipeline Commander (Orchestrator)

**File:** `pipeline_commander.py` | **Skill:** SKILL-VID-009
**Input:** All upstream outputs + operator decisions
**Process:** The Pipeline Commander is the orchestration brain — a 16-state lifecycle machine that sequences all 8 downstream modules, manages parallel execution (T2I and audio start simultaneously), provides checkpoint/resume for failure recovery, handles batch queue processing (FIFO with priority override, default 3 concurrent), and builds the review UI state for operator approval.

**16 Pipeline States:**
`PENDING` → `GENERATING_T2I` / `PROCESSING_AUDIO` (parallel) → `AUDIO_COMPLETE` → `QUALITY_GATE` → `GENERATING_I2V` → `FINGERPRINTING` → `ASSEMBLING_MANIFEST` → `GENERATING_CAPTIONS` → `RENDERING_PREVIEW` → `READY_FOR_REVIEW` → `REGENERATING` (loop) or `RENDERING_FINAL` → `APPROVED` → `PUBLISHED`

Any state can transition to `FAILED` (terminal). `PUBLISHED` is also terminal.

**Key Capabilities:** Beat-level approval (approve/regenerate/reject per beat with revision notes), auto-approve when all beats ≥ 0.8 quality, cost tracking ($0.02/T2I + $0.06/I2V per beat), JSON checkpoint/resume (never re-runs completed stages), and batch queue (up to 3 concurrent videos, FIFO + priority).

**Schemas:** DEP-VID-025 (Pipeline State), DEP-VID-026 (Pipeline Job Queue), DEP-VID-027 (Review UI State)
**Receipts:** `PIPELINE_INIT`, `BATCH_QUEUE_MANAGE`

---

## Constraint Gate Network

Every Phase 3 module that interacts with external services or produces irreversible outputs is protected by a constraint gate — a set of validation questions that must all pass before execution proceeds. Gates are implemented in Python (`apps/cmf-assembler/gates/`).

| Gate | Module | Questions | Key Constraints |
|------|--------|-----------|-----------------|
| **Gate D** | T2I Generation | 5 | Prompt-PSSL coherence, negative prompts, seed strategy, resolution match, workflow registered |
| **Gate E** | Manifest Assembly | 5 | Frame continuity, asset completeness, audio-beat alignment, transition budget, arc sequence |
| **Gate F** | I2V Generation | 5 | Motion parameters, VRAM requirements (48GB), keyframe approval, clip duration, workflow registered |
| **Gate I** | Audio Engine | 4 | File integrity, language detection, music duration match, ducking target levels |
| **Gate K** | Remotion Renderer | 5 | Manifest completeness, asset accessibility, audio-video duration (±0.5s), template compatibility, render budget |
| **Gate L** | Pipeline Commander | 6 | Upstream assets present, RunningHub endpoints reachable, concurrent budget, disk space (≥10GB), module health (9 modules), resume detection (informational) |

> [!NOTE]
> Gate L Q6 (resume detection) is informational only — it detects existing checkpoints but never blocks pipeline initialization.

---

## Schema Registry (DEP-VID-001 through DEP-VID-027)

All inter-module data contracts are defined as JSON schemas in `apps/cmf-assembler/schemas/`. The 22 schemas cover:

- **Input/Config schemas** (6): Beat Cluster (001), Transition Presets (003), Workflow Registry (007), I2V Motion Presets (010), Gate Configuration (013), Caption Style Config (020)
- **Generation result schemas** (4): T2I Result (008), I2V Result (011), Quality Score (012), Render Job Result (023)
- **Audio schemas** (2): Whisper Transcript (004), Ducking Curve (005)
- **Manifest & caption schemas** (3): Remotion Manifest (002), Caption Components (021), Arc Template Registry (022)
- **Fingerprint & regen schemas** (3): Beat Fingerprint Map (014), Regeneration Request (015), Regeneration History (016)
- **Orchestration schemas** (3): Pipeline State (025), Job Queue (026), Review UI State (027)
- **Render preset schema** (1): Render Quality Presets (024)

---

## Fix & Re-Compose Commands (Remediation)

When validation fails at any stage, these per-format fix commands handle targeted remediation:

| Command | Target | Purpose |
|---------|--------|---------|
| `/cmf-fix-gmg` | GMG prompts | Fix specific GMG validation failures (G1-G7) |
| `/cmf-fix-cac` | CAC prompts | Fix specific CAC validation failures (C1-C9) |
| `/cmf-fix-sb` | Storyboard prompts | Fix storyboard validation failures |

### Per-Format Compose Variants

For granular control, individual compose commands exist:

| Command | Format | Purpose |
|---------|--------|---------|
| `/cmf-compose-gmg-01` through `-06` | GMG Expert 01-06 | Generate GMG for a specific Expert |
| `/cmf-compose-sb` | Storyboard | Compose storyboard only |
| `/cmf-compose-cac` | CAC | Compose CAC only |
| `/cmf-analyze-gmg` | GMG | Analyze GMG only |
| `/cmf-analyze-cac` | CAC | Analyze CAC only |
| `/cmf-analyze-sb` | Storyboard | Analyze storyboard only |

---

## Complete Output File Inventory (Per Project)

| Phase | File Category | Count |
|-------|--------------|-------|
| **1A** | strategy_brief.json | 1 |
| **1A** | Brand Avatar .md | 1 |
| **1A** | Quote_Manifest.md | 1 |
| **1A** | Quote_Manifest_Enriched.md | 1 |
| **1A** | premise_analysis.json | 1 |
| **1A** | COMPOSITION_LOG.md | 1 |
| **1A** | {ARC}_AUTHORIZED.md | 1 |
| **1A** | final_script.json | 1 |
| **Bridge** | beat_cluster.json | 1 |
| **Bridge** | ERoll_Deep_Research_Report.md | 1 |
| **Bridge** | search_queries.json | 1 |
| **1B** | Storyboard prompts + enriched + manifest | ~26 |
| **1B** | suno_prompt.txt | 1 |
| **1B** | GMG prompts + enriched + manifest | 21 |
| **1B** | CAC prompts + enriched + manifest | 16 |
| **1B** | PROMPTS_AUTHORIZED.md | 1 |
| **2** | Generated images (T2I/I2I) | ~10-15 |
| **2** | Generated video clips (I2V) | ~5-12 |
| **2** | Music track (Suno V5) | 1 |
| **3** | Whisper transcript + ducking curve | 2 |
| **3** | Remotion manifest | 1 |
| **3** | Caption components | 1 |
| **3** | Rendered videos (preview + review + final) | 3 |
| **3** | Pipeline state + checkpoint | 2 |
| **TOTAL** | | **~115+ files** |

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **RunningHub 48GB for I2V** | SVD/CogVideoX require 40+ GB VRAM; no fallback to 24GB |
| **CLIP-based T2I scoring** | ~100ms per image, deterministic, no VLM cost |
| **Dual-stage fingerprints** | Track T2I and I2V independently; enable surgical regeneration |
| **3 regeneration modes** | T2I-only, I2V-only, Both — cascade logic pre-defined |
| **16-state pipeline SM** | Explicit state machine (not event-driven) enforces correct sequencing |
| **Parallel T2I + Audio** | No data dependency between visual and audio; saves ~15s per video |
| **Motion presets by arc stage** | Deterministic mapping: same arc stage → same camera motion grammar |
| **Manifest = declarative** | Not imperative; reviewable before render, updateable after regeneration |
| **3-tier render quality** | Fast previews for iteration, review for approval, final for distribution |
| **Auto-approve at ≥0.8** | Skip manual review when all beats pass quality threshold |
| **Max 10 regens per beat** | Prevent infinite loops; surface persistent quality issues to operator |
| **Checkpoint/resume** | JSON-based; resume never re-runs completed stages |

---

## Request Count per Project

| Step | Command | Requests |
|------|---------|----------|
| 1 | `/cmf-diagnose` | 1 |
| 2 | Brand Avatar | 1 (Python, not LLM) |
| 3 | `/cmf-hunt` | 1 |
| 4 | `/cmf-analyze` | 1 |
| 5 | `/cmf-compose` | 1 |
| 6 | `/cmf-authorize` | 1 |
| 7 | `/cmf-script` | 1 |
| 8 | `/cmf-beat-cluster` | 1 |
| 9 | `/cmf-eroll` | 1 |
| 10 | `/cmf-storyboard` (4 skills) | 4 |
| 11 | `/cmf-sonic` | 1 |
| 12 | `/cmf-motion` GMG (composer + 5 experts + analyst) | 7 |
| 12 | `/cmf-motion` CAC (composer + analyst) | 2 |
| 13 | `/cmf-visual-auth` | 1 |
| 14 | Phase 2 static generation | 1 (automated scripts) |
| 15 | Phase 3 video pipeline | 1 (automated — Commander orchestrates all 9 modules) |
| | **Fix loops (estimated)** | ~2-4 |
| **TOTAL** | | **~27-30 requests per project** |

> [!NOTE]
> If running via the `/cmf-full` orchestrator, all steps from 1-13 execute in a single session. The `// turbo-all` directive auto-approves all tool calls within the session. Phase 3's Pipeline Commander operates autonomously once initiated — the only human touchpoint is the beat-level review UI (unless auto-approve triggers at ≥0.8).

---

## Infrastructure & Deployment

| Component | Technology | Location |
|-----------|-----------|----------|
| **Phase 1 Skills** | LLM-powered (Claude/GPT) | `skills/cmf/` (75 skill files) |
| **Phase 1 Commands** | VS Code slash commands | `commands/` (30 command files) |
| **Phase 2 Scripts** | Python + PowerShell | `tools/`, `scripts/` |
| **Phase 3 Pipeline** | Python 3.12 + pytest | `apps/cmf-assembler/` |
| **ComfyUI Workflows** | JSON workflow files | `comfyui-workflows/` |
| **Docker Runtime** | Containerized handler | `cmf-docker/` |
| **Architecture Docs** | 9 FR-VID tech specs | `docs/architecture/` |
| **Test Suite** | 480 tests, 0 failures | `apps/cmf-assembler/tests/` |

### Video Pipeline Test Coverage

| Module | Test File | Tests |
|--------|-----------|-------|
| FR-VID-06 Audio Engine | `test_audio_engine.py` | 23 |
| FR-VID-02 T2I Generation | `test_runninghub_client.py` | 14 |
| FR-VID-04 Quality Gate | `test_t2i_quality_gate.py` | 54 |
| FR-VID-03 I2V Generation | `test_i2v_client.py` | 49 |
| FR-VID-05 Fingerprinting | `test_fingerprint_tracker.py` | 68 |
| FR-VID-01 Manifest Assembly | `test_beat_cluster_parser.py` | 60 |
| FR-VID-07 Captions | `test_caption_engine.py` | 54 |
| FR-VID-08 Rendering | `test_render_orchestrator.py` + `test_gate_k.py` | 71 |
| FR-VID-09 Commander | `test_pipeline_commander.py` + `test_gate_l.py` | 87 |
| **TOTAL** | | **480** |
