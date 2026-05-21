# Tech-Spec: FR-ERA3-35B — Content Benchmark Profiles and Card Weighting Bundles
**Created:** 2026-05-19
**Status:** Ready for Development
**Version:** 1.0 (ERA3 — Phase-0 Trial Commercial Runtime)
**Phase:** 0 — Trial Phase-0 Commercial Runtime
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. §2: extend existing backend (201 services, 45 model files). §3: pre-flight with real backend mapping. §4: 10-section format, min 320 lines.
2. PRD-02 LOADED:     Content compiler chain: "SCRE/CRAL signal -> primary signal packet -> edge selection -> coach provocation -> authenticated response capture -> primitive candidate -> coalition survival -> subliminal function and depth selection -> variation shaping -> route recommendation -> source artifact emission -> downstream rendering." §2.3: CCF emits Coalition Script Spine, Format Blueprint, Content Manifest. §2.1: "truth -> transcription -> force -> delivery -> variation -> phenotype -> evaluation."
3. PRD-03 LOADED:     CMF rendering constitution: "CCF compiles the meaning. CMF renders the felt experience of that meaning." §2.4: CMF outputs include cinematic video assets, structured social visuals, carousel and multi-frame packs, webinar visual assets, reaction-derived motion assets. §9.2: validators for meaning fidelity, identity continuity, expression/pose, first frame, audio sync, premium surface, routeability. §3.2: NarrativeRenderProfile, BeatClusterPacket, VisualCompositionBrief, SonicRenderProfile.
4. PRD-09 LOADED:     Commercial proof-package logic: "$0 proof layer -> $29.99 first proof unlock -> $39.99/mo speaking & learning -> $99.99/mo Coach OS." §6.1: OFO deposits value first — "free proof, visible previews, sharp audit." §6.4: proof object must be "specific, dignified, fast to understand, emotionally accurate." Audit teaser + animated video audit + full audit chain.
5. EVAL CARD LOADED:  lab/phase0_eval_card_scoring_model_v_1.md. 7 visible scores: Humanity, Presence, Trust, Memorability, Resonance, Signal, AI Slop Risk. §4: 7 internal metric clusters with 7 metrics each. §5: hidden support clusters: Structure, Actionability, Visual Proof, Caption Alignment, Temporal Craft. §6: card types share same visible vocabulary but weighting changes by content type, structural archetype, and commercial role. §7: overall_score law — weighted by card type, adjusted by content type, penalized by AI slop risk, optionally gated by hard failures.
6. SFL LOADED:        lab/subliminal_function_layer_for_ccp_v_1.md. "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness." SFL families govern delivery mechanics that directly affect all 7 visible scores on the eval card.
7. OMNISHOTCUT LOADED: lab/OmniShotCut Holistic Relational Shot Boundary.md. Key structural claims: intra-shot relations (vanilla, dissolve, wipe, push, slide, zoom, fade, doorway), inter-shot relations (hard-cut, sudden-jump, transition). Shot-query transformer for temporal range + relation classification. CCP implication: informs video-structure benchmark dimensions for reels (shot transition quality, temporal coherence, discontinuity detection) without replacing CCP-specific perceptual evaluation.
8. BACKEND LOADED:    src/ccp/services/archetype_container_runtime.py — ArchetypeContainerRuntimeService.compile(). 6 ArchetypeChoice values. ARCHETYPE_CONTRACTS dict with intent, structural_invariants, anti_draft_profile, distillation_funnel, render_targets, activation_stances per archetype.
9. MODELS LOADED:     src/ccp/models/archetype_container_runtime_models.py — ArchetypeChoice enum (ARC-MYTH-DEBUNK, ARC-ACH-STORY, ARC-OBS-HUMOR, ARC-WITNESS, ARC-CONTRAST, ARC-COMP). ContainerIntensityProfile(narrative_arc, intensity_level, pacing_profile, emotional_job).
10. CMF MODELS LOADED: src/ccp/models/cmf_arc_render_models.py — ArcRenderJobStatus, CoalitionSpineInput, FirstFrameVerdict, EpicMeaningVerdict. CMFArcGovernedRenderingPipeline with dual-gate release (first-frame + epic-meaning).
11. TESTS LOADED:     tests/integration/test_frera316_archetype_runtime_compile.py — AC-named classes, scenario-based, deterministic assertions. tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py — dual-gate pass/fail, corporate blandness block, release receipt chain.
12. VIDEO DOCTRINE:   OmniShotCut informs reel benchmark dimensions (shot segmentation, intra-shot relations, inter-shot relations, discontinuity detection) but does not replace CCP perceptual evaluation. It contributes to the Temporal Craft hidden support cluster.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P0_S03B_FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles.md` | Spec prompt |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory format |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Content compiler, archetype routing, artifact classes |
| 4 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | Media rendering, validators, benchmark metrics |
| 5 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | Commercial proof logic, OFO, audit chain |
| 6 | `lab/phase0_eval_card_scoring_model_v_1.md` | 7 visible scores, internal clusters, weighting doctrine |
| 7 | `lab/subliminal_function_layer_for_ccp_v_1.md` | SFL delivery mechanics affecting perceptual scores |
| 8 | `lab/OmniShotCut Holistic Relational Shot Boundary.md` | Video-structure analysis for reel benchmarks |
| 9 | `src/ccp/services/archetype_container_runtime.py` | Existing archetype contracts and selection matrix |
| 10 | `src/ccp/models/archetype_container_runtime_models.py` | ArchetypeChoice enum, coalition inputs |
| 11 | `src/ccp/models/cmf_arc_render_models.py` | CMF render models, gate verdicts |
| 12 | `tests/integration/test_frera316_archetype_runtime_compile.py` | Existing test patterns |
| 13 | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | CMF gate test patterns |

---

## 2. Overview

### 2.1 Problem Statement

The Phase-0 eval card scoring model defines 7 visible scores, 7 internal metric clusters, 5 hidden support clusters, and a content-type-aware weighting doctrine. But no spec currently formalizes:

- how the same visible score vocabulary is weighted differently for a single image post vs a carousel vs a reel
- how archetype-specific scoring works (a reaction reel vs an explainer reel vs a proof carousel should emphasize different scores)
- how the overall score is computed with caps, penalties, and hard-failure gates
- how video-mode benchmarks incorporate shot-transition quality, temporal coherence, and script semantics without replacing CCP perceptual evaluation
- how card-type weighting bundles are resolved and consumed by downstream audit/card rendering

Without this, the eval card system either applies identical weights to all formats (violating the No-One-Score-Fits-All Rule) or invents ad-hoc weights at render time (creating non-deterministic, non-auditable scoring).

### 2.2 Solution

This spec defines the canonical benchmark profile and weighting substrate that sits between the eval registry (FR-ERA3-35A) and the card/audit rendering system (FR-ERA3-35C). It introduces six schemas:

1. **`ContentBenchmarkProfile`** — content-type-specific weight maps for visible scores
2. **`ArchetypeScoreBundle`** — archetype-specific score emphasis and penalty adjustments
3. **`CardWeightingBundle`** — resolved, consumption-ready weighting for a specific card instance
4. **`VisibleScoreWeightMap`** — the canonical 7-score weight distribution
5. **`PenaltyAdjustmentMap`** — score-specific caps, floors, and penalty multipliers
6. **`ModalitySupportProfile`** — modality-specific benchmark dimensions (image, carousel, reel)

### 2.3 Scope

**In scope:** canonical weighting schemas, content-type baselines (image/carousel/reel), archetype-specific bundles, overall-score computation law, video-structure benchmark dimensions, Supabase persistence, fallback behavior.

**Out of scope:** the eval registry taxonomy (FR-ERA3-35A), card UI rendering (FR-ERA3-35C), the audit intelligence engine (FR-ERA3-35), individual evaluator implementations (FR-ERA3-27), SFL library (FR-ERA3-25).

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Payload / Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-BEN-001 | `ContentBenchmarkProfile` | FR-ERA3-35B | Content-type weight baselines |
| DEP-BEN-002 | `ArchetypeScoreBundle` | FR-ERA3-35B | Archetype-specific score emphasis |
| DEP-BEN-003 | `CardWeightingBundle` | FR-ERA3-35B | Resolved card-instance weighting |
| DEP-BEN-004 | `VisibleScoreWeightMap` | FR-ERA3-35B | Canonical 7-score weight distribution |
| DEP-BEN-005 | `PenaltyAdjustmentMap` | FR-ERA3-35B | Score caps, floors, penalty multipliers |
| DEP-BEN-006 | `ModalitySupportProfile` | FR-ERA3-35B | Modality-specific benchmark dimensions |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `archetype_container_runtime.py` | `src/ccp/services/` | Reads `ArchetypeChoice` to resolve archetype-specific bundles |
| `archetype_container_runtime_models.py` | `src/ccp/models/` | Consumes `ArchetypeChoice` enum for bundle keying |
| `cmf_arc_render_models.py` | `src/ccp/models/` | Reads `CoalitionSpineInput.selected_format` for content-type resolution |
| `content_machine.py` | `src/ccp/services/` | Upstream: content type determined during route recommendation |

### 3.3 Benchmark Artifact Classes

| Artifact | Layer | What It Governs |
|---|---|---|
| `ContentBenchmarkProfile` | Benchmark substrate | Base weight map for single-image, carousel, or reel |
| `ArchetypeScoreBundle` | Benchmark substrate | Score emphasis overlay per archetype (reaction reel, explainer reel, proof carousel, etc.) |
| `CardWeightingBundle` | Consumption layer | Fully resolved weights for one specific card instance |
| `VisibleScoreWeightMap` | Data contract | The 7-weight vector (Humanity, Presence, Trust, Memorability, Resonance, Signal, AI Slop Risk) |
| `PenaltyAdjustmentMap` | Governance | Score-level caps, floors, and penalty multipliers |
| `ModalitySupportProfile` | Benchmark substrate | Modality-specific dimensions (image proof, carousel sequencing, reel temporal craft) |

### 3.4 Governance Constraints

| Constraint | Origin | Enforcement |
|---|---|---|
| No-One-Score-Fits-All Rule | Eval card model §6 | Different content types MUST have different weight maps |
| Archetype-Aware Scoring Rule | Eval card model §6.2 | Different archetypes MUST emphasize different scores |
| Multimodal-Benchmark Rule | Eval card model §8 | Image, carousel, and reel each have distinct benchmark dimensions |
| Content-Type Weighting Rule | Eval card model §6.1 | Weights change by content type without changing the score vocabulary |
| Internal Consistency Rule | Eval card model §2 | All cards share the same 7 visible scores — only weights differ |
| Overall-Score Law | Eval card model §7 | Overall score is weighted, adjusted, penalized, and optionally gated |

### 3.5 Technical Decisions

| Decision | Rationale | Consequence |
|---|---|---|
| Weights are floats that sum to 1.0 | Enables weighted-average computation | Pydantic validator enforces sum constraint |
| AI Slop Risk is a penalty, not a positive weight | High slop must reduce overall score | Separate penalty multiplier, not additive weight |
| Archetype bundles overlay content-type baselines | Archetype emphasis is relative to content type | Bundle resolution: base + archetype overlay = final weights |
| Video-structure dimensions feed hidden clusters | OmniShotCut informs Temporal Craft, not visible scores directly | Shot-transition quality contributes to Presence, Memorability, AI Slop Risk via hidden cluster |
| Hard-failure gates can cap overall score | Eval card §7: weak Trust or Humanity caps top-end | PenaltyAdjustmentMap contains per-score floor thresholds |
| Profiles are registered, not generated at runtime | Deterministic, auditable | Profiles stored in Supabase, versioned, immutable per version |

---

## 4. Implementation Plan

### Phase 1 — Core Models (Tasks 1–4)

1. Define `VisibleScoreWeightMap` with 7 typed weight fields and sum-to-1.0 validator.
2. Define `PenaltyAdjustmentMap` with per-score caps, floors, and penalty multipliers.
3. Define `ContentBenchmarkProfile` keyed by `ContentType` enum.
4. Define `ModalitySupportProfile` with modality-specific dimension lists.

### Phase 2 — Archetype and Bundle Models (Tasks 5–8)

5. Define `ArchetypeScoreBundle` keyed by `ArchetypeChoice` + `ContentType`.
6. Define `CardWeightingBundle` as the resolved, consumption-ready output.
7. Define `OverallScoreComputation` model with weighted sum, penalty application, and cap logic.
8. Define `ContentType` and `CardRole` enums.

### Phase 3 — Resolution Service (Tasks 9–12)

9. Create `BenchmarkProfileRegistry` service with `resolve_profile(content_type)`.
10. Create `ArchetypeBundleResolver` service with `resolve_bundle(archetype, content_type)`.
11. Create `CardWeightingResolver` service with `resolve_card_weights(content_type, archetype, card_role)`.
12. Create `OverallScoreCalculator` service with `compute_overall(raw_scores, card_weighting_bundle)`.

### Phase 4 — Content-Type Baselines (Tasks 13–15)

13. Register canonical baseline profiles for single-image, carousel, and reel.
14. Register archetype-specific bundles for all 6 archetypes × 3 content types.
15. Register reel-specific `ModalitySupportProfile` with video-structure dimensions.

### Phase 5 — Persistence and Fallback (Tasks 16–18)

16. Create `benchmark_profiles` Supabase table.
17. Create `archetype_score_bundles` and `card_weighting_bundles` tables.
18. Implement fallback: when profile unavailable, use equal-weight baseline with warning.

### Phase 6 — Testing (Tasks 19–22)

19. Unit tests for weight sum validation, penalty application, cap logic.
20. Unit tests for archetype bundle overlay mechanics.
21. Integration tests for full resolution chain (content type → archetype → resolved bundle).
22. Non-regression tests confirming different content types produce different weights.

---

## 5. Schema

### 5.1 Enums

```python
class ContentType(str, Enum):
    SINGLE_IMAGE_POST = "single_image_post"
    CAROUSEL = "carousel"
    REEL = "reel"


class CardRole(str, Enum):
    AUDIT_CARD = "audit_card"
    PROOF_CARD = "proof_card"
    COMPARISON_CARD = "comparison_card"
    PROGRESS_CARD = "progress_card"


class VisibleScoreKey(str, Enum):
    HUMANITY = "humanity"
    PRESENCE = "presence"
    TRUST = "trust"
    MEMORABILITY = "memorability"
    RESONANCE = "resonance"
    SIGNAL = "signal"
    AI_SLOP_RISK = "ai_slop_risk"
```

### 5.2 Core Weight Models

```python
class VisibleScoreWeightMap(BaseModel):
    humanity: float = Field(ge=0.0, le=1.0)
    presence: float = Field(ge=0.0, le=1.0)
    trust: float = Field(ge=0.0, le=1.0)
    memorability: float = Field(ge=0.0, le=1.0)
    resonance: float = Field(ge=0.0, le=1.0)
    signal: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def weights_sum_to_one(self) -> "VisibleScoreWeightMap":
        total = (self.humanity + self.presence + self.trust
                 + self.memorability + self.resonance + self.signal)
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total:.4f}")
        return self


class PenaltyAdjustmentMap(BaseModel):
    ai_slop_penalty_multiplier: float = Field(ge=0.0, le=1.0, default=0.15)
    trust_floor: float = Field(ge=0.0, le=100.0, default=30.0)
    humanity_floor: float = Field(ge=0.0, le=100.0, default=25.0)
    overall_cap_when_trust_below_floor: float = Field(ge=0.0, le=100.0, default=65.0)
    overall_cap_when_humanity_below_floor: float = Field(ge=0.0, le=100.0, default=60.0)
    overall_cap_when_slop_above_threshold: float = Field(ge=0.0, le=100.0, default=55.0)
    slop_danger_threshold: float = Field(ge=0.0, le=100.0, default=70.0)
    presence_without_trust_cap: float = Field(ge=0.0, le=100.0, default=70.0)
```

### 5.3 Benchmark Profile

```python
class ModalityDimension(BaseModel):
    dimension_id: str = Field(min_length=1)
    dimension_name: str = Field(min_length=1)
    feeds_cluster: str = Field(min_length=1)
    weight_in_cluster: float = Field(ge=0.0, le=1.0)


class ModalitySupportProfile(BaseModel):
    modality_id: str = Field(min_length=1)
    content_type: ContentType
    dimensions: list[ModalityDimension] = Field(min_length=1)


class ContentBenchmarkProfile(BaseModel):
    profile_id: str = Field(min_length=1)
    profile_version: str = Field(min_length=1, default="1.0")
    content_type: ContentType
    base_weights: VisibleScoreWeightMap
    penalties: PenaltyAdjustmentMap
    modality_profile: ModalitySupportProfile
    rationale: str = Field(min_length=1)
```

### 5.4 Archetype Score Bundle

```python
class ScoreEmphasis(BaseModel):
    score_key: VisibleScoreKey
    emphasis_delta: float = Field(ge=-0.3, le=0.3)
    rationale: str = Field(min_length=1)


class ArchetypeScoreBundle(BaseModel):
    bundle_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    content_type: ContentType
    emphasis_adjustments: list[ScoreEmphasis] = Field(min_length=1)
    penalty_overrides: PenaltyAdjustmentMap | None = None
    bundle_rationale: str = Field(min_length=1)
```

### 5.5 Card Weighting Bundle (Resolved Output)

```python
class CardWeightingBundle(BaseModel):
    bundle_id: str = Field(min_length=1)
    content_type: ContentType
    archetype_choice: ArchetypeChoice
    card_role: CardRole
    resolved_weights: VisibleScoreWeightMap
    resolved_penalties: PenaltyAdjustmentMap
    modality_dimensions: list[ModalityDimension] = Field(default_factory=list)
    source_profile_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    resolution_trace: str = Field(min_length=1)


class OverallScoreComputation(BaseModel):
    raw_scores: dict[str, float] = Field(min_length=7)
    card_weighting_bundle: CardWeightingBundle
    weighted_base: float = Field(ge=0.0, le=100.0)
    slop_penalty_applied: float = Field(ge=0.0, le=100.0)
    caps_applied: list[str] = Field(default_factory=list)
    final_overall: int = Field(ge=0, le=99)
    computation_trace: str = Field(min_length=1)
```

### 5.6 Canonical Content-Type Baselines

```python
SINGLE_IMAGE_BASELINE = ContentBenchmarkProfile(
    profile_id="CBP-IMG-001",
    content_type=ContentType.SINGLE_IMAGE_POST,
    base_weights=VisibleScoreWeightMap(
        humanity=0.20, presence=0.12, trust=0.22,
        memorability=0.20, resonance=0.10, signal=0.16,
    ),
    penalties=PenaltyAdjustmentMap(),
    modality_profile=ModalitySupportProfile(
        modality_id="MOD-IMG-001",
        content_type=ContentType.SINGLE_IMAGE_POST,
        dimensions=[
            ModalityDimension(dimension_id="IMG-D1", dimension_name="screenshot_proof_quality", feeds_cluster="visual_proof", weight_in_cluster=0.4),
            ModalityDimension(dimension_id="IMG-D2", dimension_name="visual_authority_cues", feeds_cluster="visual_proof", weight_in_cluster=0.3),
            ModalityDimension(dimension_id="IMG-D3", dimension_name="visual_genericity_risk", feeds_cluster="ai_slop_risk", weight_in_cluster=0.2),
            ModalityDimension(dimension_id="IMG-D4", dimension_name="caption_image_coherence", feeds_cluster="caption_alignment", weight_in_cluster=0.4),
        ],
    ),
    rationale="Image posts are static. Signal, Trust, and Memorability dominate because the post must cut through feed noise with a single frame plus caption.",
)

CAROUSEL_BASELINE = ContentBenchmarkProfile(
    profile_id="CBP-CAR-001",
    content_type=ContentType.CAROUSEL,
    base_weights=VisibleScoreWeightMap(
        humanity=0.14, presence=0.10, trust=0.22,
        memorability=0.24, resonance=0.16, signal=0.14,
    ),
    penalties=PenaltyAdjustmentMap(),
    modality_profile=ModalitySupportProfile(
        modality_id="MOD-CAR-001",
        content_type=ContentType.CAROUSEL,
        dimensions=[
            ModalityDimension(dimension_id="CAR-D1", dimension_name="slide_sequence_logic", feeds_cluster="structure", weight_in_cluster=0.35),
            ModalityDimension(dimension_id="CAR-D2", dimension_name="frame_to_frame_proof_movement", feeds_cluster="structure", weight_in_cluster=0.25),
            ModalityDimension(dimension_id="CAR-D3", dimension_name="visual_narrative_progression", feeds_cluster="structure", weight_in_cluster=0.25),
            ModalityDimension(dimension_id="CAR-D4", dimension_name="caption_interaction", feeds_cluster="caption_alignment", weight_in_cluster=0.4),
        ],
    ),
    rationale="Carousels are sequential. Memorability and Trust dominate because carousels must reward swiping with proof progression.",
)

REEL_BASELINE = ContentBenchmarkProfile(
    profile_id="CBP-REEL-001",
    content_type=ContentType.REEL,
    base_weights=VisibleScoreWeightMap(
        humanity=0.20, presence=0.22, trust=0.12,
        memorability=0.18, resonance=0.18, signal=0.10,
    ),
    penalties=PenaltyAdjustmentMap(),
    modality_profile=ModalitySupportProfile(
        modality_id="MOD-REEL-001",
        content_type=ContentType.REEL,
        dimensions=[
            ModalityDimension(dimension_id="REEL-D1", dimension_name="script_semantic_density", feeds_cluster="structure", weight_in_cluster=0.25),
            ModalityDimension(dimension_id="REEL-D2", dimension_name="keyframe_quality", feeds_cluster="visual_proof", weight_in_cluster=0.2),
            ModalityDimension(dimension_id="REEL-D3", dimension_name="shot_transition_quality", feeds_cluster="temporal_craft", weight_in_cluster=0.3),
            ModalityDimension(dimension_id="REEL-D4", dimension_name="temporal_coherence", feeds_cluster="temporal_craft", weight_in_cluster=0.3),
            ModalityDimension(dimension_id="REEL-D5", dimension_name="pacing_rhythm", feeds_cluster="temporal_craft", weight_in_cluster=0.2),
            ModalityDimension(dimension_id="REEL-D6", dimension_name="caption_video_alignment", feeds_cluster="caption_alignment", weight_in_cluster=0.4),
            ModalityDimension(dimension_id="REEL-D7", dimension_name="discontinuity_absence", feeds_cluster="temporal_craft", weight_in_cluster=0.2),
        ],
    ),
    rationale="Reels are temporal. Presence and Humanity dominate because reels expose the speaker's embodied authority. Temporal Craft dimensions from OmniShotCut inform shot-transition quality and discontinuity detection.",
)
```

### 5.7 Supabase DDL

```sql
CREATE TABLE IF NOT EXISTS benchmark_profiles (
    profile_id           TEXT PRIMARY KEY,
    profile_version      TEXT NOT NULL DEFAULT '1.0',
    content_type         TEXT NOT NULL,
    profile_json         JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS archetype_score_bundles (
    bundle_id            TEXT PRIMARY KEY,
    archetype_choice     TEXT NOT NULL,
    content_type         TEXT NOT NULL,
    bundle_json          JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (archetype_choice, content_type)
);

CREATE TABLE IF NOT EXISTS card_weighting_bundles (
    bundle_id            TEXT PRIMARY KEY,
    content_type         TEXT NOT NULL,
    archetype_choice     TEXT NOT NULL,
    card_role            TEXT NOT NULL,
    resolved_json        JSONB NOT NULL,
    source_profile_id    TEXT NOT NULL REFERENCES benchmark_profiles(profile_id),
    source_bundle_id     TEXT NOT NULL REFERENCES archetype_score_bundles(bundle_id),
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 6. Backward Compatibility and Fallback

### 6.1 Profile Not Found

If `BenchmarkProfileRegistry.resolve_profile(content_type)` finds no registered profile:

- return the equal-weight fallback: `VisibleScoreWeightMap(humanity=0.167, presence=0.167, trust=0.167, memorability=0.167, resonance=0.166, signal=0.166)`
- log `benchmark_profile_fallback` with reason `profile_not_found` to receipt chain
- set `resolution_trace = "FALLBACK: equal-weight baseline used"`
- downstream systems consume the bundle normally but audit cards should display a warning indicator

### 6.2 Archetype Bundle Not Found

If no `ArchetypeScoreBundle` exists for the given `(archetype, content_type)` pair:

- use the content-type baseline without archetype overlay
- `resolution_trace = "FALLBACK: no archetype overlay applied"`
- receipt chain logs `archetype_bundle_fallback`

### 6.3 Unknown Content Type

If the content type is not one of the three canonical types:

- reject with validation error
- no fallback — unknown content types must be registered before use

### 6.4 Weight Sum Violation

If archetype emphasis deltas cause the resolved weight sum to drift outside `[0.99, 1.01]`:

- the `CardWeightingResolver` renormalizes to 1.0 after applying deltas
- logs `weight_renormalized` to receipt chain with original and normalized values

### 6.5 Existing Systems Unaffected

The benchmark profile substrate is additive. Existing archetype runtime, CMF rendering, and SFL binding logic are not modified. The benchmark system consumes `ArchetypeChoice` and `ContentType` as read-only inputs.

---

## 7. Tasks

### Model Definition

- [ ] Add `ContentType` enum to `benchmark_profile_models.py`
- [ ] Add `CardRole` enum to `benchmark_profile_models.py`
- [ ] Add `VisibleScoreKey` enum to `benchmark_profile_models.py`
- [ ] Add `VisibleScoreWeightMap` model with sum-to-1.0 validator
- [ ] Add `PenaltyAdjustmentMap` model with caps, floors, and multipliers
- [ ] Add `ModalityDimension` and `ModalitySupportProfile` models
- [ ] Add `ContentBenchmarkProfile` model
- [ ] Add `ScoreEmphasis` and `ArchetypeScoreBundle` models
- [ ] Add `CardWeightingBundle` model
- [ ] Add `OverallScoreComputation` model

### Canonical Baselines

- [ ] Register `SINGLE_IMAGE_BASELINE` profile
- [ ] Register `CAROUSEL_BASELINE` profile
- [ ] Register `REEL_BASELINE` profile with OmniShotCut-informed temporal dimensions
- [ ] Register archetype bundles for ARC-MYTH-DEBUNK × 3 content types
- [ ] Register archetype bundles for ARC-ACH-STORY × 3 content types
- [ ] Register archetype bundles for ARC-OBS-HUMOR × 3 content types
- [ ] Register archetype bundles for ARC-WITNESS × 3 content types
- [ ] Register archetype bundles for ARC-CONTRAST × 3 content types
- [ ] Register archetype bundles for ARC-COMP × 3 content types

### Resolution Services

- [ ] Create `BenchmarkProfileRegistry` service
- [ ] Create `ArchetypeBundleResolver` service
- [ ] Create `CardWeightingResolver` service with overlay + renormalization logic
- [ ] Create `OverallScoreCalculator` service with weighted sum + penalty + cap logic

### Persistence

- [ ] Create `benchmark_profiles` table
- [ ] Create `archetype_score_bundles` table
- [ ] Create `card_weighting_bundles` table
- [ ] Implement profile persistence and retrieval

### Receipt Chain

- [ ] Add receipt entries for `benchmark_profile_resolved`, `archetype_bundle_resolved`, `card_weights_resolved`, `overall_score_computed`, `benchmark_profile_fallback`, `weight_renormalized`

### Testing

- [ ] Unit tests for weight sum validation
- [ ] Unit tests for penalty cap logic
- [ ] Unit tests for archetype overlay mechanics
- [ ] Integration tests for full resolution chain
- [ ] Non-regression tests for content-type differentiation

---

## 8. Acceptance Criteria

### AC-BEN-1 — Different content types produce different weight maps

**Given** a request to resolve benchmark profiles for `single_image_post`, `carousel`, and `reel`,
**When** the `BenchmarkProfileRegistry` resolves each profile,
**Then** all three `VisibleScoreWeightMap` instances have different weight distributions,
**And** the image profile emphasizes Signal and Trust more than the reel profile,
**And** the reel profile emphasizes Presence and Humanity more than the image profile,
**And** the carousel profile emphasizes Memorability more than both others.

**FAILURE EXAMPLE:** All three content types return `VisibleScoreWeightMap(humanity=0.167, presence=0.167, trust=0.167, memorability=0.167, resonance=0.166, signal=0.166)`. That applies identical weights to fundamentally different formats, violating the No-One-Score-Fits-All Rule and making all cards score the same way regardless of whether the content is a static image or a 60-second reel.

**Constraint:** No-One-Score-Fits-All Rule, Content-Type Weighting Rule.

### AC-BEN-2 — Archetype-specific bundles modify baseline weights

**Given** a `reel` content type with archetype `ARC-MYTH-DEBUNK` (reaction reel style),
**When** the `ArchetypeBundleResolver` resolves the bundle and overlays it on the reel baseline,
**Then** the resolved weights shift Presence and Signal higher relative to the reel baseline,
**And** the emphasis deltas are within `[-0.3, +0.3]`,
**And** the resolved weights still sum to 1.0 after overlay.

**FAILURE EXAMPLE:** The archetype bundle for a myth-debunk reel returns the same weights as an achievement-story reel. That ignores the fundamental difference between confrontational authority content and narrative proof content, producing identical scoring for content that requires different emphasis.

**Constraint:** Archetype-Aware Scoring Rule.

### AC-BEN-3 — Overall score respects penalty and cap law

**Given** raw scores `{humanity: 22, presence: 85, trust: 28, memorability: 70, resonance: 60, signal: 75, ai_slop_risk: 15}`,
**When** the `OverallScoreCalculator` computes the overall score,
**Then** the overall is capped at `overall_cap_when_trust_below_floor` (65) because Trust (28) < `trust_floor` (30),
**And** the overall is further capped at `overall_cap_when_humanity_below_floor` (60) because Humanity (22) < `humanity_floor` (25),
**And** AI Slop Risk (15) does not trigger the slop cap (threshold 70),
**And** the `caps_applied` list contains `["trust_floor_cap", "humanity_floor_cap"]`,
**And** the final overall score is ≤ 60.

**FAILURE EXAMPLE:** The system computes a naive weighted average of 62 and reports that as the overall score, ignoring that Trust and Humanity are dangerously low. That creates "false greatness" where high Presence compensates for missing credibility, violating the Overall-Score Law.

**Constraint:** Overall-Score Law.

### AC-BEN-4 — High AI Slop Risk caps overall score

**Given** raw scores with `ai_slop_risk: 82` (above `slop_danger_threshold` of 70),
**When** the overall score is computed,
**Then** the overall is capped at `overall_cap_when_slop_above_threshold` (55),
**And** `caps_applied` includes `"slop_danger_cap"`,
**And** the `slop_penalty_applied` field shows the penalty deduction.

**FAILURE EXAMPLE:** A piece with strong visible scores but 82% AI Slop Risk gets an overall score of 78. That rewards highly generic, over-smoothed content that looks competent but feels synthetic, directly contradicting the eval model's core law that "strong visible scores cannot fully compensate for very high AI Slop Risk."

**Constraint:** Overall-Score Law, Eval card model §7.

### AC-BEN-5 — Reel benchmark includes video-structure dimensions

**Given** a `reel` content type profile resolution,
**When** the `ModalitySupportProfile` is returned,
**Then** it includes dimensions for `shot_transition_quality`, `temporal_coherence`, `pacing_rhythm`, and `discontinuity_absence`,
**And** all video-structure dimensions feed the `temporal_craft` hidden support cluster,
**And** `temporal_craft` influences Presence, Memorability, and AI Slop Risk visible scores.

**FAILURE EXAMPLE:** The reel benchmark profile contains only the same dimensions as the image profile (screenshot proof, visual authority). That ignores temporal craft entirely, meaning a reel with terrible pacing, jump cuts, and incoherent transitions scores the same as one with polished shot structure.

**Constraint:** Multimodal-Benchmark Rule.

### AC-BEN-6 — Presence without Trust is capped

**Given** raw scores with `presence: 90` and `trust: 25` (below `trust_floor` of 30),
**When** the overall score is computed,
**Then** the overall is capped at `presence_without_trust_cap` (70),
**And** `caps_applied` includes `"presence_without_trust_cap"`.

**FAILURE EXAMPLE:** A coach with explosive delivery charisma but zero proof, zero credibility, and zero earned authority gets an overall of 88 because Presence alone carries the score. That creates the exact "false greatness" the eval model warns about — high Presence without Trust should not create the illusion of quality.

**Constraint:** Overall-Score Law, Eval card model §7.

---

## 9. Dependencies

### Internal Services

| Dependency | Type | Use |
|---|---|---|
| `FR-ERA3-35A Eval Registry` | Upstream | Provides canonical eval taxonomy consumed by benchmark profiles |
| `FR-ERA3-35C Eval Card System` | Downstream consumer | Renders cards using resolved `CardWeightingBundle` |
| `FR-ERA3-35 Audit Intelligence Engine` | Downstream consumer | Uses profiles for automated audit scoring |
| `FR-ERA3-16 Archetype Container Runtime` | Read dependency | `ArchetypeChoice` enum for bundle keying |
| `FR-ERA3-12 CMF Arc-Governed Rendering` | Read dependency | Content type and format family information |
| `ReceiptChain` | Existing core | Extended with benchmark-specific receipt entries |

### Internal Models

| Dependency | Type | Use |
|---|---|---|
| `archetype_container_runtime_models.py` | Read-only | `ArchetypeChoice` enum |
| `cmf_arc_render_models.py` | Read-only | `CoalitionSpineInput.selected_format` for content-type inference |
| `benchmark_profile_models.py` | New | All 6 new models defined in this spec |
| Supabase | Existing infra | 3 new tables |

### External

| Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed model definitions with validators |

---

## 10. Testing Strategy

### 10.1 Unit Tests

#### `test_frera35b_weight_validation.py`

- `test_weight_sum_exactly_one_passes`
- `test_weight_sum_below_099_fails`
- `test_weight_sum_above_101_fails`
- `test_individual_weight_negative_fails`
- `test_individual_weight_above_one_fails`

#### `test_frera35b_penalty_logic.py`

- `test_trust_below_floor_caps_overall`
- `test_humanity_below_floor_caps_overall`
- `test_slop_above_threshold_caps_overall`
- `test_presence_without_trust_caps_overall`
- `test_multiple_caps_apply_strictest`
- `test_no_caps_when_all_scores_healthy`
- `test_slop_penalty_multiplier_reduces_base`

#### `test_frera35b_archetype_overlay.py`

- `test_myth_debunk_reel_shifts_presence_higher`
- `test_witness_reel_shifts_resonance_higher`
- `test_overlay_renormalizes_to_one`
- `test_emphasis_delta_bounded_minus_03_to_03`
- `test_no_overlay_when_bundle_absent`

### 10.2 Integration Tests

#### `tests/integration/test_frera35b_resolution_chain.py`

Scenario class: `TestACBEN1ContentTypeDifferentiation`

- Resolve profiles for all three content types.
- Assert all three `VisibleScoreWeightMap` instances differ.
- Assert image emphasizes Trust > reel Trust.
- Assert reel emphasizes Presence > image Presence.
- Assert carousel emphasizes Memorability > both others.

Scenario class: `TestACBEN2ArchetypeOverlay`

- Resolve reel baseline + ARC-MYTH-DEBUNK overlay.
- Assert resolved weights differ from reel baseline.
- Assert resolved weights sum to 1.0.
- Assert emphasis deltas within bounds.

Scenario class: `TestACBEN3OverallScoreComputation`

- Compute overall with low Trust and low Humanity.
- Assert caps are applied.
- Assert final overall ≤ min(trust_cap, humanity_cap).
- Assert `caps_applied` list is non-empty.

#### `tests/integration/test_frera35b_reel_modality.py`

Scenario class: `TestACBEN5ReelVideoDimensions`

- Resolve reel modality profile.
- Assert `shot_transition_quality` dimension present.
- Assert `temporal_coherence` dimension present.
- Assert `discontinuity_absence` dimension present.
- Assert all video dimensions feed `temporal_craft` cluster.

### 10.3 Non-Regression Expectations

- No test may accept identical weights for different content types.
- No test may accept an overall score above the applicable cap when a floor is violated.
- No test may accept a reel benchmark without video-structure dimensions.
- No test may accept archetype emphasis deltas outside `[-0.3, +0.3]`.
- No test may accept a resolved weight map that does not sum to 1.0.
- No test may accept an overall score that ignores AI Slop Risk penalty.
