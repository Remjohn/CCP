# Tech-Spec: FR-VIS-16 — First Frame Composer (Iris)

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0 (Aligned to PRD Visual Control Layer Amendment v1.0)
**Architecture Reference:** PRD §CA10 Visual Control Layer, ADR-08
**Skill Implementation:** `skills/visuals/iris_first_frame_composer.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/prd/prd-update-visual-control-layer.md` — FR-VIS-16 definition, DEP-VIS-012
- `docs/architecture/FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md` — Expression presets consumed by FFC
- `docs/architecture/FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md` — Pose atoms consumed by FFC
- `docs/architecture/FR-VIS-01_Visual_Composition_Brief_Tech_Spec.md` — VCB schema reference
- `first_frame_agent_architecture.md` (brain artifact) — Full FFC architecture analysis, decision engine, routing table
- `visual_hooks_mcda_audit.md` (brain artifact) — 38 MCDA-validated hook compositions as reference presets
- `lab/CVE + CPSC research papers/Gaze Cueing in Design Framework.md` — Gaze vector theory
- `lab/Memetic Engine/` — 14 humor architectures requiring FFC visual support

---

## 2. Overview

### Problem Statement
Every content format the CCP produces — short-form video, carousel, thumbnail, webinar cover, flyer, poll visual, story — requires a **First Frame**: the single visual composition that determines whether a human stops scrolling. Currently, zero agents in the pipeline own this function. CAC composes editorial scenes with all frames weighted equally. GMG composes abstract animations where the first frame is just the last frame reversed. Carousels and thumbnails have no visual composer at all. The scroll-stop frame — the highest-ROI visual in the entire pipeline — is either an afterthought picked in post-production or a generic Canva template.

### Solution
FR-VIS-16 defines the **First Frame Composer (FFC)** — code-named **Iris** — a cross-format visual composition agent that engineers the scroll-stop first frame upstream of all format-specific composers. Iris receives the Psychological Routing Brief (mood state, CBCS tier), the Beat Cluster (concept, VCP, core emotion), and the coach's identity context, then composes a deterministic `first_frame_spec.json` specifying every visual parameter: CP-IDs for body/hands/gaze/scene/mood, ConsciousSmile expression channels, text overlay specification, ControlNet asset paths, and Identity LoRA reference. This spec is then routed to the appropriate format-specific pipeline (CAC, GMG, Carousel Builder, Thumbnail Renderer).

### Scope
**In scope:**
- Iris agent 6-step decision engine (Format Constraints → Mood Visual → Gaze Vector → Text Hook → Expression → Compose)
- `first_frame_spec.json` output schema
- Format-specific output routing (video, carousel, thumbnail, flyer, webinar, poll, story, email)
- Anti-draft architecture (2-level: stock thumbnail + format-specific)
- Named composition presets derived from MCDA-validated hooks
- Database schema for first frame specs and performance tracking

**Out of scope:**
- Frame-by-frame video composition (CAC/GMG downstream)
- ControlNet map rendering (handled by FR-VIS-15)
- Expression training (handled by FR-VIS-14)
- Text hook copywriting (handled by content pipeline; Iris receives hooks, doesn't write them)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-VIS-012` | First Frame Spec | OUTPUT — `first_frame_spec.json` consumed by format pipelines. |
| `DEP-VIS-010` | ConsciousPose Library | INPUT — Iris queries pose atoms by mood state + archetype. |
| `DEP-VIS-008` | ConsciousSmile Adapter | INPUT — Iris specifies expression channel values. |
| `DEP-VIS-011` | Identity LoRA Registry | INPUT — Iris resolves coach LoRA path. |
| `DEP-ENG-016` | Psychological Routing Brief | INPUT — Mood state, CBCS tier, regulatory frame. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Composition decisions recorded. |
| `DEP-VIS-005` | VCB Schema | SIBLING — FFC produces a specialized VCB for frame 1 only. |

### Academic Grounding

| Framework | Author | Year | Mechanism Applied |
|---|---|---|---|
| **Scroll-Stop Economics** | Facebook/Meta Research | 2021 | Users make a stop/scroll decision within 0.4 seconds. The first frame must trigger a pattern interrupt within this window. Iris optimizes composition variables (face presence, gaze vector, color contrast) for sub-400ms visual processing. |
| **Emotional Contagion via Face** | Hatfield et al. | 1994 | A human face with a specific expression is the single highest-converting element in the first frame. Iris always includes a face in the first frame and specifies ConsciousSmile channels matched to the content's emotional payload. |
| **Benign Violation Theory** | McGraw & Warren | 2010 | For memetic content, the first frame must contain the Violation or the Benignness signal (never both — the other lives in the text/caption). Iris routes BVT composition: violation visual + benign text, or benign visual + violation text. |
| **Gaze Cueing** | Friesen & Kingstone | 1998 | Cold audiences (CBCS 0-3) respond to either averted contemplative gaze (curiosity) or provocative direct gaze (scroll-stop). Warm audiences (CBCS 4-7) respond to near-direct gaze. Hot audiences (CBCS 8-10) respond to confident invitation gaze. |

### Technical Decisions

1. **Cross-Format Agent:** Iris is separate from CAC/GMG because the first frame is a cross-format concern. CAC optimizes for editorial consistency across ALL frames; Iris optimizes for the scroll-stop trigger of frame 1 ONLY.
2. **Deterministic Composition (no LLM):** Iris's 6-step decision engine is a deterministic rule engine, NOT an LLM reasoning call. The Psychological Routing Brief + CBCS tier + format → a specific composition via decision tree. LLM reasoning would introduce latency and non-reproducibility.
3. **Anti-Draft as Constraint, Not Filter:** The 2-level anti-draft is a CONSTRAINT on the decision engine (negative rules that prune the composition space), not a post-hoc filter that evaluates the output.

---

## 4. Implementation Plan

### Stage 1: Decision Engine Core
*Agent:* Iris (First Frame Composer)
*Inputs:* Psychological Routing Brief, Beat Cluster, output_format, cbcs_tier
*Outputs:* `first_frame_spec.json`

**6-Step Decision Engine:**

| Step | Decision | Inputs | Output |
|---|---|---|---|
| 1 | **Format Constraints** | output_format | dimensions, face position rule, text zone |
| 2 | **Mood Visual** | mood_state from DEP-ENG-016 | CP-MV-* selection (lighting/color) |
| 3 | **Gaze Vector** | cbcs_tier + mood_state | CP-G-* selection |
| 4 | **Text Hook** | concept + core_emotion + regulatory_frame | headline text, position, font treatment |
| 5 | **Expression** | mood_state + core_emotion + memetic_intent | ConsciousSmile channel values |
| 6 | **Compose & Audit** | All above + body + hands + scene + props | Complete first_frame_spec.json + Write Receipt Chain Guard |

### Stage 2: Format Routing Table
*Outputs:* Routing configuration for 8 format pipelines

| Format | Dimensions | Face Rule | FFC Output → Next Pipeline |
|---|---|---|---|
| Short video | 1080×1920 (9:16) | Top 40% | → CAC/GMG (Frame 1 locked) |
| Carousel | 1080×1350 (4:5) | Centered | → Carousel Builder (Cover locked) |
| Thumbnail | 1920×1080 (16:9) | Left/Right third | → Thumbnail Renderer (direct) |
| Flyer | Variable | Full-body OK | → Static Composition (direct) |
| Webinar | 1920×1080 (16:9) | Professional framing | → Event Page Builder |
| Story | 1080×1920 (9:16) | Top-center | → Story Renderer |
| Poll/Quiz | 1080×1080 (1:1) | Split-screen OK | → Crowdpurr Template |
| Email | 600×400 (3:2) | Centered | → Email Hero Renderer |

### Stage 3: Anti-Draft Constraint System
*Outputs:* Negative composition rules

**Level 1 — Stock Thumbnail Anti-Draft:** Compositions that trigger Level 1 are automatically rejected:
- Studio lighting (CP-MV with Kelvin > 5500K AND saturation < 40%) + white/plain background + generic smile (preset `warm_confidence` at default values without any channel customization) → REJECT

**Level 2 — Format-Specific Anti-Draft:** Per-format rejection patterns:
- Carousel cover with no face (text-only slide 1) → REJECT
- Thumbnail with centered face (no rule-of-thirds) → REJECT
- Video frame 1 identical to frame 1 of any other video generated in the last 30 days for the same coach → REJECT (deduplication via CLIP similarity)

### Stage 4: Named Composition Presets
*Source:* 38 MCDA-validated hook compositions from audit
*Outputs:* `first_frame_presets` database table

Presets serve as starting points that Iris can reference, not constraints. Each preset maps to a mood × archetype × format combination with validated CP-ID selections and expression channels.

---

## 5. Data Model

### Table: `first_frame_specs`

```sql
CREATE TABLE IF NOT EXISTS first_frame_specs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    spec_id VARCHAR(50) NOT NULL UNIQUE,            -- 'FFS-JP-20260330-001'
    coach_id UUID NOT NULL,
    content_output_id VARCHAR(50),                  -- Link to DEP-ENG-011
    beat_cluster_id VARCHAR(50),
    output_format VARCHAR(30) NOT NULL,
    dimensions VARCHAR(20) NOT NULL,                -- '1080x1350'
    mood_state VARCHAR(30) NOT NULL,
    cbcs_tier VARCHAR(10) NOT NULL,                 -- 'cold', 'warm', 'hot'
    body_cp_id VARCHAR(20),
    hands_cp_id VARCHAR(20),
    gaze_cp_id VARCHAR(20),
    scene_cp_id VARCHAR(20),
    mood_visual_cp_id VARCHAR(20),
    props_cp_id VARCHAR(20),
    expression_spec JSONB NOT NULL,                 -- {"mode": "preset", "preset_name": "...", "channel_overrides": {...}}
    text_headline TEXT,
    text_position VARCHAR(30),
    text_font_treatment VARCHAR(50),
    controlnet_depth_path TEXT,
    controlnet_openpose_path TEXT,
    identity_lora_path TEXT NOT NULL,
    adapter_path TEXT NOT NULL,
    negative_prompt TEXT,
    reasoning JSONB,                                -- Decision rationale per step
    anti_draft_passed BOOLEAN DEFAULT true,
    routed_to VARCHAR(50),                          -- 'cac_composer', 'carousel_builder', etc.
    generated_image_path TEXT,
    clip_embedding VECTOR(512),                     -- For deduplication
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ffs_coach ON first_frame_specs(coach_id);
CREATE INDEX idx_ffs_format ON first_frame_specs(output_format);

ALTER TABLE first_frame_specs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own specs" ON first_frame_specs
    FOR SELECT USING (auth.uid() = coach_id);
```

### Table: `first_frame_presets`

```sql
CREATE TABLE IF NOT EXISTS first_frame_presets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    preset_name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    mood_state VARCHAR(30),
    archetype_family VARCHAR(50),
    output_format VARCHAR(30),
    composition JSONB NOT NULL,                     -- Full CP-ID + expression spec
    anti_draft_patterns JSONB,                      -- Negative patterns to avoid
    mcda_score FLOAT,                               -- From hook audit
    source_hook_id VARCHAR(20),                     -- Reference to MCDA audit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 6. Backward Compatibility

If the FFC agent is not yet deployed, downstream composers (CAC, GMG, Carousel Builder) continue operating without a first_frame_spec. They treat all frames equally, which is the current behavior. A `FFC_NOT_AVAILABLE` flag bypasses the FFC step in the CMF Pipeline Commander. Once deployed, the CMF Pipeline Commander inserts the FFC step before format-specific composers.

---

## 7. Tasks

- [ ] **Task 1:** Implement the 6-step deterministic decision engine in `iris_first_frame_composer.py`.
- [ ] **Task 2:** Build the format routing table (8 formats with dimension/face/text rules).
- [ ] **Task 3:** Implement 2-level anti-draft constraint system.
- [ ] **Task 4:** Seed `first_frame_presets` table with 38 MCDA-validated hook compositions.
- [ ] **Task 5:** Build CLIP-based deduplication: reject first frames with > 0.92 cosine similarity to any spec generated for the same coach in the last 30 days.
- [ ] **Task 6:** Integrate with CMF Pipeline Commander: insert FFC step between Beat Cluster → format composers.
- [ ] **Task 7:** Build `first_frame_spec.json` validator (all CP-IDs must exist, all expression channels must be valid, ControlNet paths must resolve).
- [ ] **Task 8:** Register DEP-VIS-012 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Carousel Cover):** Submit Beat Cluster with mood `Escape`, CBCS `cold`, format `carousel`. Assert Iris produces a first_frame_spec with: face present, warm lighting (CP-MV-007..012), provocative/playful gaze, expression with non-zero `smile` OR `smirk` channel. *Failure:* Output has no face, studio lighting, and a generic neutral expression.
- [ ] **AC2 (Thumbnail Rule-of-Thirds):** Submit format `thumbnail`. Assert face is positioned in left OR right third. Assert text overlay is in the opposite third. *Failure:* Face is dead-center with text overlapping the face region.
- [ ] **AC3 (Anti-Draft Rejection):** Submit composition with CP-MV-014 (lab clinical, 5500K, 40% sat) + no expression customization + plain background. Assert Level 1 anti-draft triggers rejection. Assert Iris re-composes with a non-stock alternative.
- [ ] **AC4 (Deduplication):** Generate 2 carousel covers for the same coach 5 days apart. Assert CLIP cosine similarity < 0.92 (they must look distinct). *Failure:* Both covers use identical body/gaze/expression/scene — the coach's feed looks repetitive.
- [ ] **AC5 (Format Routing):** Submit format `short_video`. Assert Iris routes `first_frame_spec.json` to CAC/GMG composer. Assert the composer treats Frame 1 as locked (not re-composed). *Failure:* CAC overrides the FFC spec and generates its own Frame 1.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-012 (First Frame Spec) | Output | `first_frame_spec.json`. |
| DEP-VIS-010 (ConsciousPose) | Input | Pose atoms queried by mood/archetype. |
| DEP-VIS-008 (ConsciousSmile) | Input | Expression channels specified. |
| DEP-VIS-011 (Identity LoRA) | Input | Coach LoRA path resolved. |
| DEP-ENG-016 (Psych Routing Brief) | Input | Mood state + CBCS tier. |
| FR-VIS-14 (ConsciousSmile) | Prerequisite | Adapter must exist for expression spec. |
| FR-VIS-15 (ConsciousPose) | Prerequisite | Library must exist for pose spec. |
| FR-VIS-17 (Identity LoRA) | Prerequisite | Coach LoRA must exist. |
| CMF Pipeline Commander | Integration | FFC inserted as pipeline step. |
| CAC/GMG Composers | Downstream | Receive Frame 1 spec as constraint. |

---

## 10. Testing Strategy

### Unit Tests
- **Decision Engine Determinism:** Same inputs (mood=Escape, cbcs=cold, format=carousel) → same output composition across 100 runs.
- **Format Dimension Enforcement:** Assert format=`short_video` → 1080×1920, format=`thumbnail` → 1920×1080.
- **Anti-Draft Rule Matching:** Provide 5 known-stock compositions. Assert all 5 are caught by Level 1.

### Integration Tests
- **Full Pipeline:** Beat Cluster → FFC → Carousel Builder → ComfyUI → Generated image. Assert the generated image matches the first_frame_spec's composition (body position, expression, scene match visually).
- **Commander Integration:** Trigger a full CMF batch. Assert FFC runs before CAC/GMG. Assert FFC spec is present in the Receipt Chain.

### Safety Tests
- **Text Injection:** Inject `<script>alert('xss')</script>` into text_headline field. Assert Iris sanitizes the text before including it in the spec.
- **Non-Existent CP-ID:** Provide mood state that maps to a non-existent CP-MV-999. Assert resolver returns fallback to closest valid atom.
