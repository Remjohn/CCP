# Tech-Spec: FR-ERA3-12 - CMF Arc-Governed Rendering Updated for SFL
**Created:** 2026-05-19  
**Status:** Ready for Development  
**Version:** 2.0 (ERA3 Architecture - SFL Runtime Integration)  
**Phase:** 6 - SFL Runtime Integration  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed all new specs must extend the existing Python/FastAPI backend, cite real backend files before inventing new ones, declare CBAR mandates explicitly, and use typed Pydantic schemas and brownfield implementation language.
2. PRD-02 LOADED:     Exact runtime-law proof captured from PRD-02: "signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> subliminal function stack -> composition depth profile -> variation profile -> directional integrity validation -> perceptual influence validation -> JIT script contract -> render blueprint". Confirms render blueprint is downstream of SFL, DI, and perceptual validation, not a place where CMF can improvise new meaning or evaluator logic.
3. PRD-03 LOADED:     Exact architectural claim captured: "CCF compiles the meaning. CMF renders the felt experience of that meaning." Also captured: "A powerful idea can still die on screen through weak framing, generic pacing, bad sonic decisions, flat sequencing, or visuals that feel synthetic and socially unbelievable." Confirms CMF owns realization quality but does not own source truth.
4. SFL CORE DOC READ: lab/subliminal_function_layer_for_ccp_v_1.md. Concrete structural claim captured: "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness." Confirms this update must make CMF realize SFL intent without redefining it.
5. CARD MODEL DOC READ: lab/phase0_eval_card_scoring_model_v_1.md. Concrete structural claim captured: every visible audit card should expose "a large content thumbnail", "six main visible scores", and visible score families including Humanity, Presence, Trust, Memorability, Resonance, Signal, plus AI Slop Risk. Confirms CMF must render score-card and audit-board compatible media surfaces, not only cinematic outputs.
6. BIOLOGICAL MODEL READ: lab/ccp_biological_orchestration_model_v_1.md. Concrete structural claim captured: CCP runtime is "DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation" and `SFL` belongs in the delivery layer while variation sits downstream. Confirms CMF should be the phenotypic render engine for already-transcribed delivery and variation packets, not the owner of upstream truth or force.
7. OMNISHOTCUT NOTE READ: OmniShotCut note explicitly argues each detected shot should carry more than a temporal range and should include "intra-shot" and "inter-shot" relational information, with special attention to subtle but harmful discontinuities like sudden jumps. Confirms CMF should consume temporal relation hints for shot coherence and transition quality, but not let SBD concerns dominate semantic arc ownership.
8. EXISTING FR-ERA3-12 READ: Existing spec explicitly states Beat Clusters are first-class persisted artifacts, First Frame Composer check must run before full render, and Epic Meaning gate blocks corporate-aesthetic release. Confirms this update is a real extension, not a replacement.
9. FR-ERA3-25 READ: Confirmed canonical SFL ownership of function families, function definitions, and crosswalks, and confirmed the explicit separation rule that metrics belong elsewhere. CMF must consume function stacks and profile bundles, not author them.
10. FR-ERA3-27 READ: Confirmed perceptual influence validation is a distinct runtime stage, that FR-ERA3-27 owns perceptual scoring and surface-specific threshold profiles, and that UI surfacing is out of scope there. Confirms CMF can consume evaluator outputs and preservation instructions, but must not swallow evaluator ownership.
11. BACKEND FILE READ: src/ccp/services/cmf_arc_governed_rendering.py. Verified live methods:
    - `NarrativeRenderingModel.translate(self, spine: CoalitionSpineInput) -> list[BeatClusterPlan]`
    - `FirstFrameAuthorityGate.evaluate(...) -> FirstFrameAuthorityCheck`
    - `EpicMeaningGate.evaluate(...) -> EpicMeaningGateResult`
    - `CMFArcGovernedRenderingPipeline.create_job(...) -> ArcRenderJobRecord`
    - `build_manifest(...) -> ArcRenderManifest`
    - `release(...) -> ArcRenderReleaseResult | None`
    Confirms real render runtime already exists and should be updated, not replaced.
12. BACKEND FILE READ: src/ccp/services/abel_vcb_generator.py. Verified `generate(self, inp: VCBGenerationInput) -> VisualCompositionBrief`. Confirms Abel remains the VCB planning boundary.
13. BACKEND FILE READ: src/ccp/services/canvas_composition_service.py. Verified:
    - `create_composition(...) -> CanvasComposition`
    - `request_regeneration(...) -> tuple[CanvasComposition, RegenerationRequest]`
    - `approve(...) -> CanvasComposition`
    Confirms Canvas remains the composition and approval boundary for card boards, audit boards, and render outputs.
14. BACKEND FILE READ: src/ccp/services/course_video_cmf.py. Verified `VisualAidAssembler.assemble(...)` and `CourseVideoPipeline.execute(...)` behavior, confirming CMF already handles longer-form educational video assembly and should share SFL-aware temporal and perceptual realization rules.
15. BACKEND FILE READ: src/ccp/services/saliency_analysis_service.py. Verified `analyze(...) -> tuple[SaliencyAnalysisOutput, Optional[SaliencyOverrideInfo], str]`. Confirms text safe zones, subject masks, and saliency regions are already real render inputs and should be used for audit cards and score-card thumbnails.
16. BACKEND FILE READ: apps/animation-studio/services/frame_export_service.py. Verified `create_export_job(...)`, `create_carousel_pose_job(...)`, and naming verification helpers. Confirms CMF can target both temporal frame exports and pose/card surfaces with deterministic export jobs.
17. MODELS READ:
    - src/ccp/models/cmf_arc_render_models.py for BeatClusterPlan, ArcRenderManifest, ArcRenderJobRecord
    - src/ccp/models/visual_engine_models.py for VisualCompositionBrief / Canvas composition-adjacent contracts
    - src/ccp/models/ca11_models.py for CourseVideoManifest and learning-path media outputs
    Confirms there are already render, composition, and media output contracts to extend.
18. TESTS READ:
    - tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py confirms dual-gate release discipline and targeted cluster retry behavior
    - tests/integration/test_ca11_fr12_course_video.py confirms editorial-template, render-output, and learning-path pipeline testing style
19. OMNISHOTCUT INTERPRETATION LOCKED:
    OmniShotCut should inform temporal segmentation, transition semantics, sudden-jump avoidance, and frame-level interpretability.
    It should not dominate meaning ownership, arc selection, or SFL policy selection.
20. UPDATE SCOPE LOCKED:
    This spec must update CMF so it realizes:
    - `SubliminalFunctionStackPacket`
    - `CompositionDepthRenderProfile`
    - `VariationRenderHints`
    - score-card / audit-board compatible outputs
    while remaining subordinate to SDA and FR-ERA3-27 evaluator ownership.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S54_FR-ERA3-12_Update_CMF_Arc_Governed_Rendering_for_SFL.md` | Prompt scope, output file contract, and mandatory source set |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Brownfield spec-writing protocol |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | CCF -> CMF runtime placement and render blueprint law |
| 4 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | CMF architectural claim, runtime layers, and render preservation doctrine |
| 5 | `lab/subliminal_function_layer_for_ccp_v_1.md` | Canonical SFL doctrine and ownership boundary |
| 6 | `lab/phase0_eval_card_scoring_model_v_1.md` | Audit card / score-card surface requirements |
| 7 | `lab/ccp_biological_orchestration_model_v_1.md` | Runtime organism model and render placement |
| 8 | `lab/OmniShotCut Holistic Relational Shot Boundary.md` | Shot / transition / temporal relation precedent |
| 9 | `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec.md` | Existing CMF arc-governed rendering spec to be updated |
| 10 | `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | SFL canonical function and crosswalk substrate |
| 11 | `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md` | Perceptual evaluator ownership and downstream threshold logic |
| 12 | `src/ccp/services/cmf_arc_governed_rendering.py` | Existing arc-governed render runtime to extend |
| 13 | `src/ccp/services/abel_vcb_generator.py` | Existing VCB generation boundary |
| 14 | `src/ccp/services/canvas_composition_service.py` | Existing composition / review / regeneration boundary |
| 15 | `src/ccp/services/course_video_cmf.py` | Existing CMF long-form / educational assembly boundary |
| 16 | `src/ccp/services/saliency_analysis_service.py` | Existing saliency / text-safe-zone / subject-mask render input layer |
| 17 | `apps/animation-studio/services/frame_export_service.py` | Existing deterministic export-job and pose-export boundary |
| 18 | `src/ccp/models/cmf_arc_render_models.py` | Existing render packet and job models |
| 19 | `src/ccp/models/visual_engine_models.py` | Existing composition / format / VCB-related visual models |
| 20 | `src/ccp/models/ca11_models.py` | Existing course-video media output contracts |
| 21 | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | Existing render gate and release behavior tests |
| 22 | `tests/integration/test_ca11_fr12_course_video.py` | Existing media pipeline / render-result test pattern |

---

## 2. Overview

### 2.1 Problem Statement

The current CMF arc-governed rendering runtime is already better than a generic montage engine. It knows about Beat Clusters, First Frame gating, Epic Meaning, and manifest-driven release. But after the SFL wave, that is no longer enough.

The current system still lacks a formal render contract for:

- subliminal function intent realization
- composition depth realization
- repetition with variation across media assets
- rhythmic structure as render logic rather than script-only intent
- strategic ambiguity preservation under visual and temporal translation
- mathematical variation cues like asymmetry, resonance carry, and salience distribution
- score-card and audit-board surfaces that need to look premium, interpretable, and shareable

Without this update:

- CMF can preserve arc while still flattening SFL intent into generic visual polish.
- the runtime can pass semantic and perceptual gates but still render overly literal, too smooth, or rhythmically dead outputs.
- single-image, carousel, reel, and audit-card surfaces will drift into inconsistent realization styles.
- Phase-0 audit PDFs and audit explainer videos will have no formal CMF contract for card-thumbnail selection, board composition, or score-overlay timing.
- OmniShotCut-inspired transition awareness will remain isolated from actual CMF timing, scene-boundary, and frame-selection behavior.

### 2.2 Solution

This update extends `FR-ERA3-12` into a true **SFL-aware realization layer**.

CMF will remain subordinate to:

- SDA truth and directional integrity
- archetype/runtime outputs
- FR-ERA3-25 canonical function and crosswalk ownership
- FR-ERA3-27 perceptual scoring ownership

But CMF will now formally own the realization of:

- `SubliminalFunctionStackPacket`
- `CompositionDepthRenderProfile`
- `VariationRenderHints`
- `TemporalCraftHints`
- `RenderPerceptualPlan`
- `RenderPreservationReport`

Across:

- single-image outputs
- carousel outputs
- reel / short-form video outputs
- scoring-card / audit-board surfaces
- longer-form proof and course-video surfaces where applicable

### 2.3 Update Scope

This is an **update spec**, not a new media engine spec.

**In scope**

- extending the existing CMF arc-governed runtime
- new SFL-aware render packets and realization stages
- composition-depth and variation-aware render planning
- temporal craft hints informed by shot structure
- render preservation and downgrade behavior based on FR-27 outputs
- score-card / audit-board render compatibility
- PDF-ready and explainer-video-ready render surfaces

**Out of scope**

- redefining SFL functions (`FR-ERA3-25`)
- redefining perceptual scoring ownership (`FR-ERA3-27`)
- inventing a separate frontend app
- replacing Abel, Canvas, or course-video CMF
- full UI/editor designs beyond machine contracts
- full Phase-0 operator workflow specs

---

## 3. Context for Development

### 3.1 DEP-IDs

| DEP-ID | Component | Source | What It Does |
|---|---|---|---|
| `DEP-CMF-SFL-012-01` | `RenderPerceptualPlan` | FR-ERA3-12 update | Top-level render-ready plan that carries SFL realization intent into CMF |
| `DEP-CMF-SFL-012-02` | `CompositionDepthRenderProfile` | FR-ERA3-12 update | Realization profile for repetition-with-variation, layered interpretation, rhythmic structure, and strategic ambiguity |
| `DEP-CMF-SFL-012-03` | `VariationRenderHints` | FR-ERA3-12 update | Render-time hints for asymmetry, resonance carry, salience distribution, and paradox retention |
| `DEP-CMF-SFL-012-04` | `TemporalCraftHints` | FR-ERA3-12 update | Shot, boundary, transition, pause-weight, and pacing hints informed by arc and OmniShotCut-like structure |
| `DEP-CMF-SFL-012-05` | `RenderPreservationReport` | FR-ERA3-12 update | Records what SFL intent, depth, variation, and evaluator constraints were preserved or degraded |
| `DEP-CMF-SFL-012-06` | `ScoreCardRenderBundle` | FR-ERA3-12 update | CMF-ready output contract for a single visible audit card |
| `DEP-CMF-SFL-012-07` | `AuditBoardRenderBundle` | FR-ERA3-12 update | Multi-card board render bundle for PDF audit pages and board surfaces |
| `DEP-CMF-SFL-012-08` | `AuditExplainerTimeline` | FR-ERA3-12 update | Time-ordered card/video overlay structure for audit explainer videos |
| `DEP-CMF-SFL-012-09` | `PerceptualThumbnailSelection` | FR-ERA3-12 update | Selects the most diagnostic and strongest thumbnail / hero frame for cards and boards |
| `DEP-CMF-SFL-012-10` | `SFLAwareArcRenderPipeline` | FR-ERA3-12 update | Updated CMF runtime that realizes SFL and variation plans without redefining them |

### 3.2 Existing Backend Integration

| File | Path | How This Update Uses It |
|---|---|---|
| `cmf_arc_governed_rendering.py` | `src/ccp/services/cmf_arc_governed_rendering.py` | Primary runtime to extend. Existing methods like `translate`, `create_job`, `run_epic_meaning_gate`, `build_manifest`, and `release` remain core boundaries. |
| `abel_vcb_generator.py` | `src/ccp/services/abel_vcb_generator.py` | Abel remains the `VisualCompositionBrief` generator. This update enriches its inputs with SFL-aware render directives rather than replacing it. |
| `canvas_composition_service.py` | `src/ccp/services/canvas_composition_service.py` | Existing composition creation, targeted regeneration, and approval lifecycle will receive score-card, audit-board, and card-grid output bundles. |
| `course_video_cmf.py` | `src/ccp/services/course_video_cmf.py` | Existing long-form video pipeline should consume the same temporal craft and variation rules so educational video outputs do not become smooth but dead. |
| `saliency_analysis_service.py` | `src/ccp/services/saliency_analysis_service.py` | Existing safe-zone, subject-mask, and saliency output will inform hero-frame selection, score overlays, and thumbnail cropping. |
| `frame_export_service.py` | `apps/animation-studio/services/frame_export_service.py` | Existing beat-level export jobs and pose export paths become compatible render targets for card systems, audit-board stills, and animated explainers. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Required audit trail for SFL realization, temporal hint generation, card frame selection, and render preservation reporting. |

### 3.3 Render Packets / Media Contracts

The existing CMF runtime already has:

- `CoalitionSpineInput`
- `BeatClusterPlan`
- `FirstFrameAuthorityCheck`
- `EpicMeaningGateResult`
- `ArcRenderManifest`
- `ArcRenderJobRecord`

This update adds render packets that sit between archetype/runtime outputs and final manifest generation:

```text
archetype/runtime output
-> SubliminalFunctionStackPacket (owned upstream)
-> CompositionDepthRenderProfile
-> VariationRenderHints
-> TemporalCraftHints
-> RenderPerceptualPlan
-> Abel / Canvas / sidecar / frame-export realization
-> RenderPreservationReport
```

These contracts must support:

1. **single-image outputs**
   - hero frame composition
   - card thumbnails
   - score overlays
   - asymmetry-preserving crop logic

2. **carousel outputs**
   - repetition with variation across slides
   - swipe-sequence rhythm
   - visual proof distribution
   - board-layout compatibility

3. **reels / short-form videos**
   - beat-cluster pacing
   - transition semantics
   - pause-weight preservation
   - caption / frame / timing alignment

4. **score-card and audit-board outputs**
   - large thumbnail
   - six visible scores
   - AI Slop Risk warning surface
   - PDF-safe typography regions
   - explainer-video card reveal timing

### 3.4 Governance Constraints

| Constraint | Origin | Implementation Mechanism |
|---|---|---|
| Render-Preserves-Meaning Rule | PRD-02, PRD-03 | CMF may not alter validated source meaning; SFL realization remains downstream of DI and perceptual validation |
| Composition-Depth Render Rule | SFL doctrine + prompt | render plans must explicitly realize repetition with variation, layered interpretation, rhythmic structure, and strategic ambiguity |
| Variation-Aliveness Rule | biological model + SFL doctrine | render plans must honor asymmetry, resonance carry, salience distribution, and paradox retention where specified |
| No-Dead-Polish Rule | PRD-03, FR-ERA3-27, FR-ERA3-28 | render pipeline must not maximize smoothness, cleanliness, or symmetry at the expense of human texture and memorability |
| SFL Subordinate-to-SDA Rule | PRD-08, SFL doctrine | CMF may not use SFL intent to override semantic truth, geometry, or directional integrity results |
| Evaluator Ownership Rule | FR-ERA3-27 | CMF consumes evaluator outputs and preservation constraints; it does not rescore perceptual dimensions |
| Audit-Surface Readiness Rule | Phase-0 card model | CMF must render score-card and audit-board compatible surfaces as first-class outputs, not as afterthought exports |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Keep CMF as realization engine, not evaluator | preserves FR-27 ownership and clear runtime roles | make CMF score perceptual dimensions directly | collapses realization and judgment into one layer |
| Insert `RenderPerceptualPlan` before manifest generation | makes SFL realization explicit and traceable | hide all SFL decisions inside manifest fields | too opaque for debugging, receipts, and audit boards |
| Use `CompositionDepthRenderProfile` as a typed packet | depth logic must survive across image, carousel, and reel surfaces | re-derive depth heuristically per surface | drift risk and inconsistent outputs |
| Use `VariationRenderHints` instead of raw formulas in CMF | CMF should realize variation, not own the full mathematical layer | embed variation math directly in every render service | too coupled and hard to tune |
| Make `TemporalCraftHints` OmniShotCut-informed but not OmniShotCut-owned | transition semantics and sudden-jump awareness help render quality | let raw shot-boundary logic drive all cut decisions | would overfit SBD concerns and swallow narrative ownership |
| Treat score cards and audit boards as CMF outputs | they are now real campaign/proof surfaces | leave them as downstream PDF-only formatting | breaks visual consistency and wastes existing render stack |
| Reuse Canvas for audit-board assembly | Canvas already owns composition lifecycle | invent a separate audit layout engine | duplicates composition logic and review flow |

---

## 4. Plan

### Phase 1 - Contract Extension

- [ ] **Task 1:** Create `src/ccp/models/cmf_sfl_render_models.py`.
- [ ] **Task 2:** Define `RenderPerceptualPlan`.
- [ ] **Task 3:** Define `CompositionDepthRenderProfile`.
- [ ] **Task 4:** Define `VariationRenderHints`.
- [ ] **Task 5:** Define `TemporalCraftHints`.
- [ ] **Task 6:** Define `RenderPreservationReport`.

### Phase 2 - Runtime Wiring

- [ ] **Task 7:** Extend `CMFArcGovernedRenderingPipeline.create_job()` to accept upstream SFL/runtime packets.
- [ ] **Task 8:** Add `build_render_perceptual_plan(...)`.
- [ ] **Task 9:** Add `build_composition_depth_profile(...)`.
- [ ] **Task 10:** Add `build_variation_render_hints(...)`.
- [ ] **Task 11:** Add `build_temporal_craft_hints(...)`.
- [ ] **Task 12:** Preserve links to `DirectionalIntegrityReport` and `PerceptualInfluenceReport` without re-evaluation.

### Phase 3 - Surface Realization

- [ ] **Task 13:** Extend Abel input augmentation to include composition-depth and variation directives for single images and carousel slides.
- [ ] **Task 14:** Extend manifest builder to include temporal craft hints for reels and course videos.
- [ ] **Task 15:** Add hero-frame selection logic for score cards and audit thumbnails using saliency and temporal hints.
- [ ] **Task 16:** Add score-card render bundle generation.
- [ ] **Task 17:** Add audit-board render bundle generation for PDF pages and board spreads.
- [ ] **Task 18:** Add audit explainer timeline generation for card-based audit videos.

### Phase 4 - Preservation and Downgrade Logic

- [ ] **Task 19:** Add `RenderPreservationReport` generation after manifest build and after preview render.
- [ ] **Task 20:** Detect realization failures such as dead polish, over-literalization, broken rhythm, and card illegibility.
- [ ] **Task 21:** Route to Canvas targeted regeneration for slide/cluster/card-level failures.
- [ ] **Task 22:** Add downgrade rules for:
  - missing temporal craft hints on video outputs
  - missing card-safe thumbnail on score-card surfaces
  - evaluator warning requiring reduced polish / simpler realization

### Phase 5 - Persistence and API

- [ ] **Task 23:** Add persistence fields/tables for SFL render plans and preservation reports.
- [ ] **Task 24:** Extend CMF routes to return SFL-aware render planning state.
- [ ] **Task 25:** Add route support for score-card and audit-board preview retrieval.

### Phase 6 - Verification

- [ ] **Task 26:** Create integration tests for single-image, carousel, reel, and audit-board realization.
- [ ] **Task 27:** Add regression tests ensuring CMF does not override evaluator ownership.
- [ ] **Task 28:** Add tests proving OmniShotCut hints influence timing and cuts without owning arc selection.

---

## 5. Schema

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RenderSurfaceType(str, Enum):
    SINGLE_IMAGE = "single_image"
    CAROUSEL = "carousel"
    REEL = "reel"
    AUDIT_CARD = "audit_card"
    AUDIT_BOARD = "audit_board"
    AUDIT_EXPLAINER = "audit_explainer"
    COURSE_VIDEO = "course_video"


class CompositionDepthMode(str, Enum):
    REPETITION_WITH_VARIATION = "repetition_with_variation"
    LAYERED_INTERPRETATION = "layered_interpretation"
    RHYTHMIC_STRUCTURE = "rhythmic_structure"
    STRATEGIC_AMBIGUITY = "strategic_ambiguity"


class VariationHintMode(str, Enum):
    ASYMMETRY_BALANCE = "asymmetry_balance"
    RESONANCE_CARRY = "resonance_carry"
    SALIENCE_DISTRIBUTION = "salience_distribution"
    PARADOX_RETENTION = "paradox_retention"
    PREDICTABILITY_BREAK = "predictability_break"


class TemporalRelationType(str, Enum):
    VANILLA_SHOT = "vanilla_shot"
    TRANSITION = "transition"
    HARD_CUT = "hard_cut"
    SUDDEN_JUMP_RISK = "sudden_jump_risk"


class RenderFallbackDecision(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    DOWNGRADE = "downgrade"
    BLOCK = "block"


class ScoreCardVisibleScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(..., min_length=2, max_length=32)
    score_0_99: int = Field(..., ge=0, le=99)


class ScoreCardRenderBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    card_id: str = Field(..., min_length=1, max_length=80)
    content_thumbnail_asset_id: str = Field(..., min_length=1, max_length=120)
    surface_type: RenderSurfaceType = Field(default=RenderSurfaceType.AUDIT_CARD)
    overall_score_0_99: int = Field(..., ge=0, le=99)
    ai_slop_risk_0_99: int = Field(..., ge=0, le=99)
    visible_scores: list[ScoreCardVisibleScore] = Field(..., min_length=6, max_length=6)
    verdict_line: str = Field(..., min_length=8, max_length=240)
    format_ratio: str = Field(..., min_length=2, max_length=8)


class AuditBoardRenderBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    board_id: str = Field(..., min_length=1, max_length=80)
    card_ids: list[str] = Field(..., min_length=1)
    hero_thumbnail_asset_id: str = Field(..., min_length=1, max_length=120)
    board_layout_template_id: str = Field(..., min_length=1, max_length=120)
    page_count: int = Field(..., ge=1, le=50)
    export_targets: list[str] = Field(default_factory=list)


class TemporalCraftHint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cluster_id: str = Field(..., min_length=1, max_length=80)
    relation_type: TemporalRelationType
    cut_ms: int = Field(..., ge=0)
    hold_ms: int = Field(..., ge=0)
    pause_weight_ms: int = Field(..., ge=0)
    transition_label: str = Field(..., min_length=1, max_length=80)
    sudden_jump_risk: float = Field(..., ge=0.0, le=1.0)
    interpretability_note: str = Field(..., min_length=8, max_length=240)


class TemporalCraftHints(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hint_set_id: str = Field(..., min_length=1, max_length=80)
    source_video_asset_id: str = Field(default="", max_length=120)
    hints: list[TemporalCraftHint] = Field(default_factory=list)
    rhythm_summary: str = Field(..., min_length=8, max_length=240)


class CompositionDepthRenderProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str = Field(..., min_length=1, max_length=80)
    surface_type: RenderSurfaceType
    repetition_with_variation_weight: float = Field(..., ge=0.0, le=1.0)
    layered_interpretation_weight: float = Field(..., ge=0.0, le=1.0)
    rhythmic_structure_weight: float = Field(..., ge=0.0, le=1.0)
    strategic_ambiguity_weight: float = Field(..., ge=0.0, le=1.0)
    preserve_subtext: bool = Field(default=True)
    allow_explicit_exposition: bool = Field(default=False)


class VariationRenderHints(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hint_id: str = Field(..., min_length=1, max_length=80)
    surface_type: RenderSurfaceType
    asymmetry_balance_target: float = Field(..., ge=0.0, le=1.0)
    resonance_carry_target: float = Field(..., ge=0.0, le=1.0)
    salience_distribution_target: float = Field(..., ge=0.0, le=1.0)
    paradox_retention_target: float = Field(..., ge=0.0, le=1.0)
    predictability_break_target: float = Field(..., ge=0.0, le=1.0)
    notes: list[str] = Field(default_factory=list)


class RenderPerceptualPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(..., min_length=1, max_length=80)
    content_output_id: str = Field(..., min_length=1, max_length=120)
    coach_id: str = Field(..., min_length=1, max_length=120)
    surface_type: RenderSurfaceType
    function_stack_packet_id: str = Field(..., min_length=1, max_length=120)
    directional_integrity_report_id: str = Field(..., min_length=1, max_length=120)
    perceptual_influence_report_id: str = Field(..., min_length=1, max_length=120)
    depth_profile: CompositionDepthRenderProfile
    variation_hints: VariationRenderHints
    temporal_hints: TemporalCraftHints
    target_thumbnail_count: int = Field(..., ge=1, le=24)
    card_safe: bool = Field(default=False)
    pdf_safe: bool = Field(default=False)
    generated_at: datetime


class PreservationDimensionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension_name: str = Field(..., min_length=3, max_length=64)
    intended_level: float = Field(..., ge=0.0, le=1.0)
    realized_level: float = Field(..., ge=0.0, le=1.0)
    preserved: bool
    rationale: str = Field(..., min_length=8, max_length=240)


class RenderPreservationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(..., min_length=1, max_length=80)
    plan_id: str = Field(..., min_length=1, max_length=80)
    manifest_id: str = Field(default="", max_length=80)
    fallback_decision: RenderFallbackDecision
    dimensions: list[PreservationDimensionResult] = Field(default_factory=list)
    lost_intents: list[str] = Field(default_factory=list)
    downgraded_surfaces: list[str] = Field(default_factory=list)
    reviewer_notes: list[str] = Field(default_factory=list)
    created_at: datetime
```

### 5.1 Schema Notes

- `RenderPerceptualPlan` is the main handoff packet into CMF realization.
- `CompositionDepthRenderProfile` is surface-aware and must differ across image, carousel, reel, and audit-board surfaces.
- `VariationRenderHints` carries targets, not raw algorithm ownership.
- `TemporalCraftHints` is where OmniShotCut-like structure informs transitions and sudden-jump avoidance.
- `RenderPreservationReport` records whether the render actually preserved the intended delivery texture.

---

## 6. Fallback

### 6.1 Required Fallback Behavior

CMF must fail closed or downgrade on realization gaps, not silently proceed.

| Failure | Fallback |
|---|---|
| Missing `SubliminalFunctionStackPacket` | block render-plan generation |
| Missing `PerceptualInfluenceReport` on high-risk surfaces | block release and route to review |
| Missing `TemporalCraftHints` for reel / audit explainer / course video | downgrade to still or low-motion assembly, never fake confident timing |
| Missing safe hero thumbnail for card surfaces | block card export and request thumbnail re-selection |
| Variation targets impossible on surface | preserve depth profile, downgrade variation complexity, log report |
| Saliency analysis unavailable for score cards | fallback to conservative crop + review flag |
| Card board layout overflow | split into more pages / boards, never auto-shrink into unreadability |

### 6.2 Surface-Specific Fallback Rules

- `SINGLE_IMAGE`
  - may downgrade to simpler asymmetry while preserving signal hierarchy
- `CAROUSEL`
  - may reduce motion assumptions but must preserve repetition-with-variation
- `REEL`
  - may reduce transition complexity but must not normalize all pauses away
- `AUDIT_CARD`
  - must keep thumbnail, overall score, six visible scores, AI Slop Risk visible
- `AUDIT_BOARD`
  - must preserve legible multi-card arrangement and page-safe composition
- `AUDIT_EXPLAINER`
  - may downgrade animation richness, but must keep timing relation between card reveals and spoken diagnosis

---

## 7. Tasks

### 7.1 Code Files to Add or Update

- `src/ccp/models/cmf_sfl_render_models.py`
- `src/ccp/services/cmf_arc_governed_rendering.py`
- `src/ccp/services/abel_vcb_generator.py`
- `src/ccp/services/canvas_composition_service.py`
- `src/ccp/services/course_video_cmf.py`
- `src/ccp/services/saliency_analysis_service.py`
- `src/ccp/scripts/setup_supabase.py`
- `tests/integration/test_fr_era3_12_cmf_sfl_rendering.py`

### 7.2 Runtime Responsibilities

1. CCF and archetype/runtime layers produce source truth, function stack, and upstream reports.
2. CMF builds `RenderPerceptualPlan`.
3. CMF maps the plan into:
   - VCB augmentation
   - temporal craft hints
   - manifest instructions
   - score-card and board output bundles
4. CMF renders or assembles outputs.
5. CMF emits `RenderPreservationReport`.
6. Canvas and downstream review surfaces consume the outputs.

### 7.3 Hard Prohibitions

CMF must not:

- redefine SFL function families
- invent new evaluator scores
- override directional-integrity failures
- normalize all surfaces toward the same visual smoothness
- treat audit cards as second-class exports
- let OmniShotCut logic replace narrative arc ownership

---

## 8. Acceptance Criteria

### AC-12-SFL.1 - SFL-aware render planning

CMF SHALL produce a `RenderPerceptualPlan` before manifest assembly for any surface that consumes SFL/runtime outputs.

**Failure example:** CMF goes directly from `BeatClusterPlan` to `ArcRenderManifest`, so the final output has no explicit realization contract for function stack, depth profile, or variation hints.

### AC-12-SFL.2 - Composition depth realization

CMF SHALL realize `CompositionDepthRenderProfile` across:

- single image
- carousel
- reel
- audit card / board surfaces

**Failure example:** a reel and a carousel both use the same uniform spacing, cadence, and exposition density despite radically different depth requirements.

### AC-12-SFL.3 - Variation-aware rendering

CMF SHALL consume `VariationRenderHints` and preserve asymmetry, resonance carry, salience distribution, and predictability break where specified.

**Failure example:** an artifact with high paradox retention and asymmetry targets is rendered as centered, perfectly balanced, over-smoothed corporate symmetry.

### AC-12-SFL.4 - Temporal craft realization

CMF SHALL consume `TemporalCraftHints` for reel, audit explainer, and course-video surfaces and use them to influence:

- cuts
- holds
- pause weight
- transition semantics
- sudden-jump avoidance

**Failure example:** the render uses arbitrary equal-length cuts and generic dissolves even though the arc and hints require confrontation pauses and semantic hard cuts.

### AC-12-SFL.5 - Audit-card readiness

CMF SHALL support score-card and audit-board compatible outputs with:

- large content thumbnail
- overall score
- six visible scores
- AI Slop Risk visibility
- legible board composition

**Failure example:** CMF can render cinematic clips but cannot produce a premium card thumbnail and board layout for the same audit asset.

### AC-12-SFL.6 - Evaluator ownership preserved

CMF SHALL consume `PerceptualInfluenceReport` and preservation constraints but SHALL NOT rescore perceptual dimensions or redefine their thresholds.

**Failure example:** CMF invents its own version of `Humanity` or `Resonance` scores during render time and uses them to override FR-27 decisions.

### AC-12-SFL.7 - Render preservation reporting

CMF SHALL emit `RenderPreservationReport` after preview and/or manifest build to record which intended perceptual properties were preserved or degraded.

**Failure example:** a render clearly loses rhythmic structure and subtext, but the pipeline has no record of the loss and no downgrade route.

---

## 9. Dependencies

### 9.1 Upstream Dependencies

- `FR-ERA3-16` archetype/runtime outputs
- `FR-ERA3-22` directional integrity reports
- `FR-ERA3-25` canonical SFL function and crosswalk substrate
- `FR-ERA3-26` query/profile assembly outputs
- `FR-ERA3-27` perceptual influence reports
- `FR-ERA3-28` perceptual failure corpus for negative render examples and future contrast validation

### 9.2 Existing Runtime Dependencies

- `abel_vcb_generator.py`
- `canvas_composition_service.py`
- `course_video_cmf.py`
- `saliency_analysis_service.py`
- `frame_export_service.py`
- `cmf_arc_governed_rendering.py`

### 9.3 Downstream Consumers

- Phase-0 audit engine and PDF package generation
- audit explainer video generation
- score-card and audit-board rendering
- webinar / course-video proof surfaces
- social proof and commercial trust-transfer assets

---

## 10. Testing

### 10.1 New Integration Tests

- `tests/integration/test_fr_era3_12_cmf_sfl_rendering.py`

### 10.2 Required Test Cases

1. **Single-image realization**
   - verifies `RenderPerceptualPlan` is generated
   - verifies card-safe crop and thumbnail selection

2. **Carousel realization**
   - verifies repetition-with-variation across slides
   - verifies board-safe export compatibility

3. **Reel realization**
   - verifies `TemporalCraftHints` influence cut and hold patterns
   - verifies sudden-jump risk drives safer transition choices

4. **Audit-card surface**
   - verifies large thumbnail, six visible scores, and AI Slop Risk remain present
   - verifies Canvas composition accepts bundle without extra manual mapping

5. **Audit-board surface**
   - verifies multi-card board export remains page-safe and legible
   - verifies split-page fallback when board overflow occurs

6. **Evaluator boundary**
   - verifies CMF consumes `PerceptualInfluenceReport` but does not emit new perceptual scores

7. **Fallback tests**
   - missing temporal hints downgrades motion surfaces
   - missing card thumbnail blocks audit-card export
   - missing evaluator report on high-risk surface blocks release

### 10.3 Test Pattern Notes

Follow the existing repo style from:

- `test_fr_era3_12_cmf_arc_governed_rendering.py`
  - direct gate assertions
  - targeted retry behavior
  - release-block discipline

- `test_ca11_fr12_course_video.py`
  - full-pipeline scenario tests
  - editorial-template and output-structure assertions
  - surface-specific output validation

### 10.4 Summary

This update turns CMF from an arc-aware render engine into an **SFL-aware realization engine**.

It does not replace:

- CCF meaning ownership
- archetype/runtime packet assembly
- FR-27 perceptual scoring

It makes CMF do the thing the runtime chain now requires:

`truth -> force -> delivery -> variation -> render`

with delivery and variation preserved visibly across every real surface CCP now depends on, including cards, boards, reels, audit PDFs, and explainer videos.
