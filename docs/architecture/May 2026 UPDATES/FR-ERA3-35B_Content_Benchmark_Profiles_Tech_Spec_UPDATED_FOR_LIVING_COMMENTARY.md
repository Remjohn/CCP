# Tech-Spec: FR-ERA3-35B — Content Benchmark Profiles UPDATED FOR LIVING COMMENTARY
**Created:** 2026-05-19
**Updated:** 2026-05-24
**Status:** Ready for Development
**Version:** 2.0 (ERA3 — Phase 7 Living Commentary & Coach Communication Stack)
**Phase:** 7 — Living Commentary & Coach Communication Stack
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. §2: extend existing backend (201 services, 45 model files). §3: pre-flight with real backend mapping. §4: 10-section format, min 280 lines. §7: CBAR mandates must be loaded from Phase Epic files.
2. PRD-02 LOADED:     docs/prd/modules/PRD_02_CCF_Content_Factory.md. Content compiler chain: "truth → transcription → force → delivery → variation → phenotype → evaluation." §2.3: CCF emits Coalition Script Spine, Format Blueprint, Content Manifest. Living Commentary correction §2.4: "keep the archetypes, change the realization grammar."
3. PRD-03 LOADED:     docs/prd/modules/PRD_03_CMF_Media_Factory.md. CMF rendering constitution: "CCF compiles the meaning. CMF renders the felt experience of that meaning." §9.2: validators for meaning fidelity, identity continuity, expression/pose, first frame, audio sync, premium surface, routeability.
4. HANDOVER LOADED:   docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md. §1.B: VIE deprecation reversal — Hybrid Component Pipeline retained. §1.B bottom: "4 Vertical Video Realization Formats" — Format 1 (Cinematic Story), Format 2 (2D Animated Explainer), Format 3 (Living Commentary Reactions), Format 4 (Conscious Reactions Editing). §1.C: "The Complete Editing Session" and "Before final editing, the recorded video's performance is formally scored."
5. PIVOTS AUDIT:      docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md. §7 SWOT Weaknesses: "Delivery quality dependence — if the coach delivers poorly, even great visuals cannot save the output." §3: The 4 Vertical Video Editing Formats with memetic sound limits (1/30s for Formats 1-3, 1/10s for Format 4). §8: Absolute ban on synthetic voice.
6. LIVING COMMENTARY SOURCE:  lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md. §2.2: "Living Commentary surfaces reintroduce what the AI-saturated market still struggles to fake: delivery, atmosphere, conviction, timing, judgment." §3.5: "Living Commentary gives us a better vessel for persuasive delivery itself." §4: Six format families — Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer. §5: Motion Grammar vocabulary (parallax, 2.5D, drift, selective float, grain, flicker). §6: Sound Doctrine — punctuation, atmosphere, timing reinforcement, memetic cues at 1/30s max.
7. ROADMAP LOADED:    lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md. §4.4: "Delivery Telemetry Layer" — pause quality, transition strength, emotional modulation, story retention, humor landing, objection clarity, close integrity, replay usefulness. §4.4: "Seminar Speaking Score Card Layer" — coach-facing scored progression with visible states including Elite Seminar Master.
8. EXISTING SPEC:     docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md (v1.0). §5.1: ContentType enum (SINGLE_IMAGE_POST, CAROUSEL, REEL). §5.2: VisibleScoreWeightMap (6 fields, sum-to-1.0 validator). §5.2: PenaltyAdjustmentMap (slop penalty, trust floor, humanity floor, caps). §5.3: ContentBenchmarkProfile, ModalitySupportProfile. §5.4: ArchetypeScoreBundle with ScoreEmphasis. §5.5: CardWeightingBundle, OverallScoreComputation. §5.6: Three canonical baselines — CBP-IMG-001, CBP-CAR-001, CBP-REEL-001.
9. BACKEND LOADED:    src/ccp/models/benchmark_profile_models.py (203 lines). ContentType, CardRole, VisibleScoreKey enums. VisibleScoreWeightMap with @model_validator(mode="after") weights_sum_to_one(). PenaltyAdjustmentMap with defaults. SINGLE_IMAGE_BASELINE, CAROUSEL_BASELINE, REEL_BASELINE canonical constants.
10. SCORING LOADED:   src/ccp/services/trait_scoring_engine.py (969 lines). TraitScoringEngine.__init__(signal_bundle) scores 12 traits independently (Deep Empathy, Authentic Vulnerability, Embodied Confidence, etc.) on 1-10 scale. Uses ScoredTrait model with TraitEvidence citations. Method pattern: _score_deep_empathy() → tuple[int, list[TraitEvidence]]. Score clamping: max(TRAIT_SCORE_MIN, min(TRAIT_SCORE_MAX, raw_score)).
11. TESTS LOADED:     tests/integration/test_frera35b_resolution_chain.py (172 lines). 4 test classes: TestACBEN1ContentTypeDifferentiation, TestACBEN2ArchetypeOverlay, TestACBEN3OverallScoreComputation, TestACBEN5ReelVideoDimensions. Uses BenchmarkProfileRegistry.resolve_profile(), ArchetypeBundleResolver, CardWeightingResolver.resolve_card_weights(), OverallScoreCalculator.compute_overall(). All assertion patterns verified.
12. EVAL REGISTRY:    tests/integration/test_era3_fr35a_eval_registry.py — confirms eval taxonomy exists and is consumed downstream.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section format, backend mapping, CBAR mandates |
| 2 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Content compiler chain, Living Commentary correction, archetype-to-realization doctrine |
| 3 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | CMF rendering constitution, validators, rendering families |
| 4 | `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` | 4 Vertical Video formats, Complete Editing Session, performance scoring mandate |
| 5 | `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` | SWOT delivery weakness, memetic sound limits, synthetic voice ban |
| 6 | `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md` | 6 format families, motion grammar, sound doctrine, persuasive delivery modules |
| 7 | `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md` | Delivery Telemetry Layer (8 dimensions), Seminar Speaking Score, Elite Seminar Master |
| 8 | `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md` | Base spec v1.0 — all existing schemas, baselines, resolution services |
| 9 | `src/ccp/models/benchmark_profile_models.py` | Existing Pydantic v2 models for benchmark profiles (203 lines) |
| 10 | `src/ccp/services/trait_scoring_engine.py` | Existing trait scoring engine (969 lines) — scoring pattern reference |
| 11 | `tests/integration/test_frera35b_resolution_chain.py` | Existing integration tests (172 lines) — test pattern reference |
| 12 | `tests/integration/test_era3_fr35a_eval_registry.py` | Eval registry taxonomy test |

---

## 2. Overview

### 2.1 Problem Statement

The v1.0 FR-ERA3-35B spec defines benchmark profiles, weight maps, and scoring machinery for **static content types**: single-image posts, carousels, and reels. The existing `ContentType` enum (`SINGLE_IMAGE_POST`, `CAROUSEL`, `REEL`) and the three canonical baselines (`CBP-IMG-001`, `CBP-CAR-001`, `CBP-REEL-001`) were designed for social media surfaces where the coach is not visibly present delivering the content.

Living Commentary fundamentally breaks that assumption. In Living Commentary:

- **The coach's visible delivery, judgment, timing, and presence are the primary carrier of value** (Source of Truth §2.2).
- **Content is performance-led**, not design-led — a Quote Commentary with weak delivery is worse than a static quote card, not better.
- **Delivery quality has scorable dimensions** that do not exist in the current benchmark system: pause quality, transition strength, emotional modulation, story retention, humor landing, objection clarity, close integrity, replay usefulness (Roadmap §4.4).
- **Each Living Commentary format family** (Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer) has **distinct benchmark criteria** that the current single-modality profiles cannot express.
- **Anti-slop criteria** must specifically reject the "talking head with captions" degradation — content that uses Living Commentary infrastructure but fails to activate the motion grammar, atmospheric field, or sonic doctrine.

Without this update, the benchmark system will either:
1. Apply carousel/reel weights to Living Commentary (violating the No-One-Score-Fits-All Rule), or
2. Score Living Commentary without measuring delivery presence (creating "false greatness" where polished visuals mask weak coach delivery).

### 2.2 Solution

This update **extends** the existing v1.0 benchmark profile substrate with three new schema families and two integration bridges:

1. **`PresenceWeightProfile`** — how much the coach's delivery presence is weighted in overall content quality scoring, per format family.
2. **`DeliveryQualityDimensions`** — the 8 scored dimensions of delivery quality (from Roadmap §4.4).
3. **`LivingCommentaryBenchmarkCard`** — format-family-specific benchmark cards with criteria per Living Commentary family.
4. **SSS Integration Bridge** — how presence weighting feeds into the Seminar Speaking Score (SSS) progression.
5. **Anti-Slop Benchmark Gate** — format-specific floor criteria that reject "talking head with captions" degradation.

### 2.3 Scope

**In scope:** Presence weighting models, delivery quality scoring dimensions, format-family benchmark cards, SSS bridge schema, anti-slop benchmark criteria, extension of `ContentType` enum, new `LivingCommentaryFormatFamily` enum, new Supabase tables, new test coverage.

**Out of scope:** The SSS card itself (FR-ERA3-35C), the eval registry taxonomy (FR-ERA3-35A), the CMF rendering pipeline (FR-ERA3-12), the Archetype Container Runtime (FR-ERA3-16), the Persuasive Speaking Program runtime (FR-ERA3-48).

### 2.4 Relationship to v1.0

This spec is **additive**. All v1.0 schemas (`VisibleScoreWeightMap`, `PenaltyAdjustmentMap`, `ContentBenchmarkProfile`, `ArchetypeScoreBundle`, `CardWeightingBundle`, `OverallScoreComputation`) remain unchanged. New models extend the existing file (`benchmark_profile_models.py`). New content types extend the `ContentType` enum. Existing baselines (`CBP-IMG-001`, `CBP-CAR-001`, `CBP-REEL-001`) remain valid and active.

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Payload / Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-BEN-001 | `ContentBenchmarkProfile` | FR-ERA3-35B v1.0 | Content-type weight baselines (retained) |
| DEP-BEN-002 | `ArchetypeScoreBundle` | FR-ERA3-35B v1.0 | Archetype-specific score emphasis (retained) |
| DEP-BEN-003 | `CardWeightingBundle` | FR-ERA3-35B v1.0 | Resolved card-instance weighting (retained) |
| DEP-BEN-007 | `PresenceWeightProfile` | FR-ERA3-35B v2.0 | Delivery-presence weighting per format family |
| DEP-BEN-008 | `DeliveryQualityDimensions` | FR-ERA3-35B v2.0 | 8 scored delivery quality dimensions |
| DEP-BEN-009 | `LivingCommentaryBenchmarkCard` | FR-ERA3-35B v2.0 | Format-family-specific benchmark criteria |
| DEP-BEN-010 | `SSSBridgePacket` | FR-ERA3-35B v2.0 | Presence score → SSS progression feed |
| DEP-BEN-011 | `AntiSlopBenchmarkGate` | FR-ERA3-35B v2.0 | Anti-slop floor criteria per format family |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `benchmark_profile_models.py` | `src/ccp/models/` | **EXTENDS** with new models: `PresenceWeightProfile`, `DeliveryQualityDimensions`, `LivingCommentaryBenchmarkCard`, `LivingCommentaryFormatFamily` enum, extended `ContentType` enum |
| `benchmark_profile_services.py` | `src/ccp/services/` | **EXTENDS** `BenchmarkProfileRegistry` with `resolve_lc_profile()`, adds `PresenceWeightResolver`, `DeliveryQualityScorer`, `AntiSlopGateEnforcer` |
| `trait_scoring_engine.py` | `src/ccp/services/` | **READ** — scoring pattern reference: evidence-based rubric, `tuple[int, list[TraitEvidence]]` return pattern, clamping logic |
| `archetype_container_runtime_models.py` | `src/ccp/models/` | **READ** — `ArchetypeChoice` enum for bundle keying (retained from v1.0) |
| `cmf_arc_render_models.py` | `src/ccp/models/` | **READ** — `CoalitionSpineInput.selected_format` for content-type inference |
| `test_frera35b_resolution_chain.py` | `tests/integration/` | **EXTENDS** with new test classes for Living Commentary benchmark resolution |

### 3.3 Benchmark Profile Contracts

| Artifact | Layer | What It Governs |
|---|---|---|
| `PresenceWeightProfile` | Presence substrate | How much the coach's delivery presence dominates the overall quality score per format family |
| `DeliveryQualityDimensions` | Delivery substrate | 8 scored dimensions of delivery quality (pause, transition, modulation, retention, humor, objection, close, replay) |
| `LivingCommentaryBenchmarkCard` | Format-family substrate | Format-specific benchmark criteria (per Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer) |
| `SSSBridgePacket` | Integration bridge | Aggregated delivery scores that feed the Seminar Speaking Score progression system (FR-ERA3-35C) |
| `AntiSlopBenchmarkGate` | Governance | Anti-slop floor criteria — rejects "talking head with captions" degradation |

### 3.4 Governance Constraints

| Constraint | Origin | Enforcement |
|---|---|---|
| Benchmark-Preserves-Delivery Rule | Living Commentary Source of Truth §2.2 | Living Commentary benchmarks MUST score delivery presence as a primary weight dimension |
| Format-Specific-Card Rule | Living Commentary Source of Truth §4 | Each of the 6 format families MUST have a dedicated benchmark card with format-specific criteria |
| Anti-Slop Benchmark Rule | Architectural Audit §7 SWOT | Benchmark system MUST reject content that degrades to "talking head with captions" by enforcing floor criteria on motion grammar, sonic doctrine, and atmospheric field activation |
| No-One-Score-Fits-All Rule | Eval card model §6 (retained from v1.0) | Different content types MUST have different weight maps |
| Overall-Score Law | Eval card model §7 (retained from v1.0) | Overall score is weighted, adjusted, penalized, and optionally gated |
| Presence-Without-Trust Cap | v1.0 §5.2 PenaltyAdjustmentMap | High Presence without Trust still caps overall score (retained) |
| Delivery Quality Dependence Warning | Audit SWOT §7 Weaknesses | System must acknowledge that weak delivery degrades output quality regardless of visual sophistication |
| Memetic Sound Limit Rule | Audit §3 | Format 1-3: max 1 memetic cue per 30s. Format 4: max 1 per 10s |

### 3.5 Technical Decisions

| Decision | Rationale | Consequence |
|---|---|---|
| Extend `ContentType` enum with Living Commentary types | Living Commentary surfaces are fundamentally different modalities from static social posts | New enum values: `LIVING_COMMENTARY_QUOTE`, `LIVING_COMMENTARY_COMPARISON`, `LIVING_COMMENTARY_SCREENSHOT`, `LIVING_COMMENTARY_ATMOSPHERIC`, `LIVING_COMMENTARY_CINEMATIC_STORY`, `LIVING_COMMENTARY_ANIMATED_EXPLAINER` |
| Separate `LivingCommentaryFormatFamily` enum for format-family grouping | Enables format-family-level benchmark cards without overloading `ContentType` | Used for `LivingCommentaryBenchmarkCard` keying |
| `PresenceWeightProfile` is per-format-family, not per-content-type | Delivery presence importance varies by format family (Atmospheric vs Animated Explainer), not by base content type | Profile resolution: format family → presence weight |
| `DeliveryQualityDimensions` are scored 0–100 each with evidence citations | Matches `TraitScoringEngine` pattern (evidence-based, scored, clamped) | Each dimension has a floor threshold for anti-slop gating |
| Anti-slop gate is a hard gate, not a penalty | "Talking head with captions" must be rejected, not merely penalized | `AntiSlopBenchmarkGate.evaluate()` returns pass/fail with rejection reasons |
| SSS bridge is a one-way feed, not a dependency | This spec exports aggregated delivery scores; FR-ERA3-35C consumes them | No circular dependency between 35B and 35C |
| New models extend existing file rather than creating a new one | Maintains single-source-of-truth for all benchmark models | `benchmark_profile_models.py` grows to ~400 lines |

---

## 4. Implementation Plan

### Phase 1 — Delivery Quality Models (Tasks 1–4)

1. Add `LivingCommentaryFormatFamily` enum to `benchmark_profile_models.py` with 6 values: `QUOTE`, `COMPARISON`, `SCREENSHOT`, `ATMOSPHERIC`, `CINEMATIC_STORY`, `ANIMATED_EXPLAINER`.
2. Extend `ContentType` enum with 6 new Living Commentary content types.
3. Define `DeliveryQualityDimensions` model with 8 scored float fields (0–100 each), evidence list, and computed `composite_delivery_score`.
4. Define `DeliveryDimensionEvidence` model following `TraitEvidence` pattern.

### Phase 2 — Presence Weight Models (Tasks 5–8)

5. Define `PresenceWeightProfile` model keyed by `LivingCommentaryFormatFamily`, containing `presence_weight` (0.0–1.0), `delivery_quality_weight` (0.0–1.0), `visual_craft_weight` (0.0–1.0), with sum-to-1.0 validator.
6. Define `LivingCommentaryBenchmarkCard` model with format-specific criteria, presence weight profile, delivery quality dimension thresholds, and anti-slop floor criteria.
7. Define `SSSBridgePacket` model aggregating delivery scores into a single feed for FR-ERA3-35C.
8. Define `AntiSlopBenchmarkGate` model with per-format-family floor criteria for motion grammar activation, sonic doctrine compliance, and atmospheric field presence.

### Phase 3 — Resolution Services (Tasks 9–13)

9. Add `resolve_lc_profile(format_family)` method to `BenchmarkProfileRegistry`.
10. Create `PresenceWeightResolver` service with `resolve_presence_weights(format_family)`.
11. Create `DeliveryQualityScorer` service with `score_delivery(audio_metrics, video_metrics)` returning `DeliveryQualityDimensions`.
12. Create `AntiSlopGateEnforcer` service with `evaluate(content_type, delivery_quality, motion_grammar_active, sonic_doctrine_active)` returning pass/fail verdict.
13. Create `SSSBridgeEmitter` service with `emit_sss_packet(delivery_quality_dimensions, format_family)` returning `SSSBridgePacket`.

### Phase 4 — Canonical Living Commentary Baselines (Tasks 14–19)

14. Register `CBP-LC-QUOTE-001` benchmark profile for Quote Living Commentary.
15. Register `CBP-LC-COMP-001` benchmark profile for Comparison Living Commentary.
16. Register `CBP-LC-SCREENSHOT-001` benchmark profile for Screenshot Living Commentary.
17. Register `CBP-LC-ATMOS-001` benchmark profile for Atmospheric Living Commentary.
18. Register `CBP-LC-CINEMATIC-001` benchmark profile for Cinematic Story Living Commentary.
19. Register `CBP-LC-EXPLAINER-001` benchmark profile for Animated Explainer Living Commentary.

### Phase 5 — Anti-Slop Gate Baselines (Tasks 20–22)

20. Register anti-slop gate thresholds for each format family: motion grammar activation floors, sonic doctrine compliance floors, atmospheric field presence floors.
21. Register delivery quality dimension floors per format family (e.g., pause quality ≥ 35 for Cinematic Story, humor landing ≥ 30 for Animated Explainer).
22. Implement anti-slop gate evaluation logic with rejection reasons and receipt chain logging.

### Phase 6 — Persistence and Integration (Tasks 23–25)

23. Create `living_commentary_benchmark_profiles` Supabase table.
24. Create `delivery_quality_scores` Supabase table.
25. Create `anti_slop_gate_verdicts` Supabase table.

### Phase 7 — Testing (Tasks 26–30)

26. Unit tests for `DeliveryQualityDimensions` validation (floor enforcement, composite calculation).
27. Unit tests for `PresenceWeightProfile` sum-to-1.0 validation.
28. Unit tests for `AntiSlopBenchmarkGate` pass/fail logic.
29. Integration tests for Living Commentary benchmark resolution chain.
30. Non-regression tests confirming v1.0 baselines remain unchanged.

---

## 5. Schema

### 5.1 New Enums

```python
class LivingCommentaryFormatFamily(str, Enum):
    """The 6 Living Commentary format families from Source of Truth §4."""
    QUOTE = "quote"
    COMPARISON = "comparison"
    SCREENSHOT = "screenshot"
    ATMOSPHERIC = "atmospheric"
    CINEMATIC_STORY = "cinematic_story"
    ANIMATED_EXPLAINER = "animated_explainer"
```

### 5.2 Extended ContentType Enum

```python
class ContentType(str, Enum):
    # --- v1.0 retained ---
    SINGLE_IMAGE_POST = "single_image_post"
    CAROUSEL = "carousel"
    REEL = "reel"
    # --- v2.0 Living Commentary additions ---
    LIVING_COMMENTARY_QUOTE = "living_commentary_quote"
    LIVING_COMMENTARY_COMPARISON = "living_commentary_comparison"
    LIVING_COMMENTARY_SCREENSHOT = "living_commentary_screenshot"
    LIVING_COMMENTARY_ATMOSPHERIC = "living_commentary_atmospheric"
    LIVING_COMMENTARY_CINEMATIC_STORY = "living_commentary_cinematic_story"
    LIVING_COMMENTARY_ANIMATED_EXPLAINER = "living_commentary_animated_explainer"
```

### 5.3 Delivery Quality Dimensions

```python
class DeliveryDimensionEvidence(BaseModel):
    """Evidence citation for a single delivery quality dimension score."""
    signal_source: str = Field(min_length=1)
    description: str = Field(min_length=1)
    rubric_points: float = Field(ge=0.0, le=100.0)


class DeliveryQualityDimensions(BaseModel):
    """8 scored delivery quality dimensions from Roadmap §4.4.

    Each dimension is scored 0–100. Together they form the delivery
    quality substrate that Living Commentary benchmarks require.
    """
    pause_quality: float = Field(ge=0.0, le=100.0,
        description="Quality of intentional pauses — stillness that creates weight, not dead air")
    transition_strength: float = Field(ge=0.0, le=100.0,
        description="Coherence of movement between ideas — bridging, not jumping")
    emotional_modulation: float = Field(ge=0.0, le=100.0,
        description="Dynamic range of emotional expression — contrast, not monotone")
    story_retention: float = Field(ge=0.0, le=100.0,
        description="Ability to hold narrative thread across the piece — continuity, not fragments")
    humor_landing: float = Field(ge=0.0, le=100.0,
        description="Effectiveness of humor when attempted — relief and warmth, not awkwardness")
    objection_clarity: float = Field(ge=0.0, le=100.0,
        description="Clarity of objection handling — precise weakening, not defensive rambling")
    close_integrity: float = Field(ge=0.0, le=100.0,
        description="Strength of the close — earned invitation, not desperate ask")
    replay_usefulness: float = Field(ge=0.0, le=100.0,
        description="How valuable the piece is on second watch — depth, not novelty dependence")

    evidence: list[DeliveryDimensionEvidence] = Field(default_factory=list)

    @property
    def composite_delivery_score(self) -> float:
        """Weighted composite across all 8 dimensions.

        Weights reflect the Source of Truth's emphasis on delivery
        presence as the primary carrier of value. Pause quality and
        emotional modulation carry slightly higher weight because they
        are the hardest to fake and most visible to the audience.
        """
        weights = {
            "pause_quality": 0.15,
            "transition_strength": 0.12,
            "emotional_modulation": 0.15,
            "story_retention": 0.13,
            "humor_landing": 0.10,
            "objection_clarity": 0.12,
            "close_integrity": 0.12,
            "replay_usefulness": 0.11,
        }
        total = (
            self.pause_quality * weights["pause_quality"]
            + self.transition_strength * weights["transition_strength"]
            + self.emotional_modulation * weights["emotional_modulation"]
            + self.story_retention * weights["story_retention"]
            + self.humor_landing * weights["humor_landing"]
            + self.objection_clarity * weights["objection_clarity"]
            + self.close_integrity * weights["close_integrity"]
            + self.replay_usefulness * weights["replay_usefulness"]
        )
        return round(total, 2)
```

### 5.4 Presence Weight Profile

```python
class PresenceWeightProfile(BaseModel):
    """Governs how much the coach's delivery presence contributes
    to the overall quality score for a given format family.

    The 3 weight channels MUST sum to 1.0:
    - presence_weight:       coach delivery quality (DeliveryQualityDimensions composite)
    - visual_craft_weight:   motion grammar, atmospheric field, sonic doctrine activation
    - content_weight:        archetype coherence, primitive alignment, script quality
    """
    profile_id: str = Field(min_length=1)
    format_family: LivingCommentaryFormatFamily
    presence_weight: float = Field(ge=0.0, le=1.0)
    visual_craft_weight: float = Field(ge=0.0, le=1.0)
    content_weight: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def channels_sum_to_one(self) -> "PresenceWeightProfile":
        total = self.presence_weight + self.visual_craft_weight + self.content_weight
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Presence/visual/content weights must sum to 1.0, got {total:.4f}"
            )
        return self
```

### 5.5 Anti-Slop Benchmark Gate

```python
class AntiSlopFloorCriteria(BaseModel):
    """Floor criteria for rejecting 'talking head with captions' degradation.

    Each field represents a boolean or threshold requirement that MUST
    be met for the content to pass the anti-slop gate.
    """
    motion_grammar_active: bool = Field(
        description="At least one motion vocabulary element from §5.1 must be present (parallax, drift, selective float, etc.)")
    sonic_doctrine_compliant: bool = Field(
        description="Sound meets punctuation/atmosphere/timing requirements from §6")
    atmospheric_field_present: bool = Field(
        description="Background climate or mid-background field objects exist (layer model §5.3)")
    min_delivery_composite: float = Field(ge=0.0, le=100.0, default=40.0,
        description="Minimum composite delivery score to pass")
    min_pause_quality: float = Field(ge=0.0, le=100.0, default=25.0,
        description="Minimum pause quality score")
    min_emotional_modulation: float = Field(ge=0.0, le=100.0, default=25.0,
        description="Minimum emotional modulation score")
    memetic_sound_compliant: bool = Field(
        description="Memetic cues respect format-specific limits (1/30s or 1/10s)")


class AntiSlopGateVerdict(BaseModel):
    """Result of anti-slop gate evaluation."""
    passed: bool
    format_family: LivingCommentaryFormatFamily
    failures: list[str] = Field(default_factory=list,
        description="List of specific floor criteria that failed")
    rejection_reason: str = Field(default="",
        description="Human-readable explanation of why the content was rejected")
    evaluated_at: str = Field(min_length=1,
        description="ISO 8601 timestamp of evaluation")
```

### 5.6 Living Commentary Benchmark Card

```python
class FormatSpecificCriterion(BaseModel):
    """A single benchmark criterion specific to a format family."""
    criterion_id: str = Field(min_length=1)
    criterion_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    weight_in_card: float = Field(ge=0.0, le=1.0)
    scoring_rubric: str = Field(min_length=1)


class LivingCommentaryBenchmarkCard(BaseModel):
    """Format-family-specific benchmark card for Living Commentary content.

    Unlike v1.0 ContentBenchmarkProfile which uses VisibleScoreWeightMap
    (7 generic visible scores), this card combines:
    - Presence weight profile (how much delivery matters)
    - Delivery quality dimension thresholds (minimum quality per dimension)
    - Format-specific criteria (unique to this format family)
    - Anti-slop floor criteria
    """
    card_id: str = Field(min_length=1)
    card_version: str = Field(default="1.0", min_length=1)
    format_family: LivingCommentaryFormatFamily
    content_type: ContentType
    presence_profile: PresenceWeightProfile
    base_weights: VisibleScoreWeightMap
    penalties: PenaltyAdjustmentMap
    delivery_dimension_floors: dict[str, float] = Field(
        min_length=1,
        description="Minimum scores per delivery dimension (dimension_name → floor)")
    format_criteria: list[FormatSpecificCriterion] = Field(min_length=1)
    anti_slop_floors: AntiSlopFloorCriteria
    rationale: str = Field(min_length=1)
```

### 5.7 SSS Bridge Packet

```python
class SSSBridgePacket(BaseModel):
    """Aggregated delivery score packet exported to FR-ERA3-35C
    for Seminar Speaking Score (SSS) progression updates.

    This is a one-way feed. This spec (35B) produces it;
    the eval card system (35C) consumes it.
    """
    packet_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    format_family: LivingCommentaryFormatFamily
    delivery_dimensions: DeliveryQualityDimensions
    composite_delivery_score: float = Field(ge=0.0, le=100.0)
    presence_weight_applied: float = Field(ge=0.0, le=1.0)
    anti_slop_passed: bool
    content_asset_id: str = Field(min_length=1)
    scored_at: str = Field(min_length=1,
        description="ISO 8601 timestamp")
```

### 5.8 Canonical Living Commentary Baselines

```python
# --- Presence Weight Profiles per Format Family ---

QUOTE_PRESENCE_PROFILE = PresenceWeightProfile(
    profile_id="PWP-QUOTE-001",
    format_family=LivingCommentaryFormatFamily.QUOTE,
    presence_weight=0.50,
    visual_craft_weight=0.20,
    content_weight=0.30,
    rationale="Quote commentary is judgment-led. The coach's interpretive delivery "
              "carries the piece. Visual craft supports but does not dominate.",
)

COMPARISON_PRESENCE_PROFILE = PresenceWeightProfile(
    profile_id="PWP-COMP-001",
    format_family=LivingCommentaryFormatFamily.COMPARISON,
    presence_weight=0.45,
    visual_craft_weight=0.25,
    content_weight=0.30,
    rationale="Comparison commentary requires strong judgment AND clear visual "
              "opposition layout. Both channels share importance.",
)

SCREENSHOT_PRESENCE_PROFILE = PresenceWeightProfile(
    profile_id="PWP-SCREEN-001",
    format_family=LivingCommentaryFormatFamily.SCREENSHOT,
    presence_weight=0.55,
    visual_craft_weight=0.15,
    content_weight=0.30,
    rationale="Screenshot commentary is maximally reaction-led. The proof object is "
              "static — value comes from the coach's interpretation.",
)

ATMOSPHERIC_PRESENCE_PROFILE = PresenceWeightProfile(
    profile_id="PWP-ATMOS-001",
    format_family=LivingCommentaryFormatFamily.ATMOSPHERIC,
    presence_weight=0.35,
    visual_craft_weight=0.40,
    content_weight=0.25,
    rationale="Atmospheric commentary depends heavily on the visual and sonic field to "
              "create the emotional environment. Delivery is important but the felt "
              "atmosphere carries a larger share.",
)

CINEMATIC_STORY_PRESENCE_PROFILE = PresenceWeightProfile(
    profile_id="PWP-CINEMA-001",
    format_family=LivingCommentaryFormatFamily.CINEMATIC_STORY,
    presence_weight=0.40,
    visual_craft_weight=0.35,
    content_weight=0.25,
    rationale="Cinematic story commentary fuses layered memory-object imagery with "
              "emotional pacing. Visual craft and delivery presence are nearly equal.",
)

ANIMATED_EXPLAINER_PRESENCE_PROFILE = PresenceWeightProfile(
    profile_id="PWP-EXPLAINER-001",
    format_family=LivingCommentaryFormatFamily.ANIMATED_EXPLAINER,
    presence_weight=0.45,
    visual_craft_weight=0.20,
    content_weight=0.35,
    rationale="Animated explainer commentary requires confident delivery AND strong "
              "content structure. Visual craft is simpler (2D/Excalidraw) but content "
              "accuracy is paramount.",
)


# --- Living Commentary Benchmark Cards ---
# (One example card shown; all 6 follow the same pattern)

QUOTE_LC_BENCHMARK_CARD = LivingCommentaryBenchmarkCard(
    card_id="LCBC-QUOTE-001",
    format_family=LivingCommentaryFormatFamily.QUOTE,
    content_type=ContentType.LIVING_COMMENTARY_QUOTE,
    presence_profile=QUOTE_PRESENCE_PROFILE,
    base_weights=VisibleScoreWeightMap(
        humanity=0.22, presence=0.28, trust=0.15,
        memorability=0.15, resonance=0.12, signal=0.08,
    ),
    penalties=PenaltyAdjustmentMap(
        presence_without_trust_cap=65.0,
    ),
    delivery_dimension_floors={
        "pause_quality": 30.0,
        "transition_strength": 25.0,
        "emotional_modulation": 35.0,
        "story_retention": 20.0,
        "humor_landing": 15.0,
        "objection_clarity": 20.0,
        "close_integrity": 25.0,
        "replay_usefulness": 30.0,
    },
    format_criteria=[
        FormatSpecificCriterion(
            criterion_id="QUOTE-FC-01",
            criterion_name="interpretive_stance_clarity",
            description="Coach takes a clear interpretive stance on the quote — agrees, disagrees, reframes, or elevates — rather than just reading it aloud",
            weight_in_card=0.30,
            scoring_rubric="0–40: reads quote with no stance. 41–70: stance implied but weak. 71–100: clear, owned, confident stance.",
        ),
        FormatSpecificCriterion(
            criterion_id="QUOTE-FC-02",
            criterion_name="atmospheric_field_activation",
            description="Visual field creates emotional context around the quote — not a plain text card with talking head",
            weight_in_card=0.20,
            scoring_rubric="0–40: flat background, no atmosphere. 41–70: basic ambient field. 71–100: Living Still doctrine with depth, grain, selective motion.",
        ),
        FormatSpecificCriterion(
            criterion_id="QUOTE-FC-03",
            criterion_name="sonic_punctuation_coherence",
            description="Sound accents reinforce key moments (contrast, reveal, emphasis) rather than being randomly placed",
            weight_in_card=0.15,
            scoring_rubric="0–40: no sound or random placement. 41–70: some alignment. 71–100: sound punctuates exactly the right beats.",
        ),
        FormatSpecificCriterion(
            criterion_id="QUOTE-FC-04",
            criterion_name="coach_cutout_presence",
            description="Coach is visually present in the composition — cutout or direct video — not just voice-over",
            weight_in_card=0.20,
            scoring_rubric="0–40: voice only, no visual presence. 41–70: static thumbnail. 71–100: dynamic cutout with gesture emphasis.",
        ),
        FormatSpecificCriterion(
            criterion_id="QUOTE-FC-05",
            criterion_name="anti_slop_integrity",
            description="Content does NOT degrade to 'talking head with captions' — uses at least 3 of the 7 motion grammar elements",
            weight_in_card=0.15,
            scoring_rubric="0: fails anti-slop gate. 50: barely passes. 71–100: rich Living Still activation.",
        ),
    ],
    anti_slop_floors=AntiSlopFloorCriteria(
        motion_grammar_active=True,
        sonic_doctrine_compliant=True,
        atmospheric_field_present=True,
        min_delivery_composite=40.0,
        min_pause_quality=25.0,
        min_emotional_modulation=25.0,
        memetic_sound_compliant=True,
    ),
    rationale="Quote Living Commentary is judgment-led. The coach's interpretive delivery carries "
              "the piece. Presence and Humanity dominate because the audience is watching a human "
              "take a position, not reading a static card. Anti-slop gate prevents degradation to "
              "generic 'talking head reads text aloud' content.",
)
```

### 5.9 Supabase DDL (New Tables)

```sql
-- Living Commentary Benchmark Profiles
CREATE TABLE IF NOT EXISTS living_commentary_benchmark_profiles (
    card_id              TEXT PRIMARY KEY,
    card_version         TEXT NOT NULL DEFAULT '1.0',
    format_family        TEXT NOT NULL,
    content_type         TEXT NOT NULL,
    card_json            JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Delivery Quality Scores
CREATE TABLE IF NOT EXISTS delivery_quality_scores (
    score_id             TEXT PRIMARY KEY,
    coach_id             TEXT NOT NULL,
    content_asset_id     TEXT NOT NULL,
    format_family        TEXT NOT NULL,
    dimensions_json      JSONB NOT NULL,
    composite_score      FLOAT NOT NULL,
    anti_slop_passed     BOOLEAN NOT NULL,
    scored_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Anti-Slop Gate Verdicts
CREATE TABLE IF NOT EXISTS anti_slop_gate_verdicts (
    verdict_id           TEXT PRIMARY KEY,
    content_asset_id     TEXT NOT NULL,
    format_family        TEXT NOT NULL,
    passed               BOOLEAN NOT NULL,
    failures_json        JSONB NOT NULL DEFAULT '[]',
    rejection_reason     TEXT NOT NULL DEFAULT '',
    evaluated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Presence Weight Profiles
CREATE TABLE IF NOT EXISTS presence_weight_profiles (
    profile_id           TEXT PRIMARY KEY,
    format_family        TEXT NOT NULL UNIQUE,
    profile_json         JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 6. Backward Compatibility and Fallback

### 6.1 v1.0 Baselines Unchanged

All v1.0 models, baselines, and resolution services remain active and unchanged. The three canonical baselines (`CBP-IMG-001`, `CBP-CAR-001`, `CBP-REEL-001`) are still resolved via `BenchmarkProfileRegistry.resolve_profile(content_type)` for non-Living-Commentary content.

### 6.2 Living Commentary Profile Not Found

If `BenchmarkProfileRegistry.resolve_lc_profile(format_family)` finds no registered Living Commentary benchmark card:

- Return the `QUOTE_LC_BENCHMARK_CARD` as a fallback (most conservative presence weighting).
- Log `lc_benchmark_fallback` with reason `card_not_found` to receipt chain.
- Set `resolution_trace = "FALLBACK: default Quote LC card used"`.

### 6.3 Delivery Quality Dimensions Not Available

If delivery quality scoring data is unavailable (e.g., audio metrics missing):

- All 8 dimensions default to `50.0` (neutral).
- Anti-slop gate skips delivery dimension checks but still enforces motion grammar, sonic doctrine, and atmospheric field criteria.
- Log `delivery_quality_fallback` to receipt chain.

### 6.4 Format Family Not Recognized

If an unknown `LivingCommentaryFormatFamily` is requested:

- Reject with validation error — no fallback for unknown format families.

### 6.5 Anti-Slop Gate Failure

When the anti-slop gate fails:

- Content is flagged with `anti_slop_failed` status.
- The overall score is capped at `overall_cap_when_slop_above_threshold` (55 from v1.0 PenaltyAdjustmentMap).
- Receipt chain logs `anti_slop_gate_rejection` with specific failure reasons.
- Content is still rendered but audit card displays prominent anti-slop warning.

---

## 7. Tasks

### Model Definition

- [ ] Add `LivingCommentaryFormatFamily` enum to `benchmark_profile_models.py`
- [ ] Extend `ContentType` enum with 6 Living Commentary values
- [ ] Add `DeliveryDimensionEvidence` model
- [ ] Add `DeliveryQualityDimensions` model with 8 scored fields and composite property
- [ ] Add `PresenceWeightProfile` model with sum-to-1.0 validator
- [ ] Add `AntiSlopFloorCriteria` model
- [ ] Add `AntiSlopGateVerdict` model
- [ ] Add `FormatSpecificCriterion` model
- [ ] Add `LivingCommentaryBenchmarkCard` model
- [ ] Add `SSSBridgePacket` model

### Canonical Baselines

- [ ] Register 6 `PresenceWeightProfile` constants (one per format family)
- [ ] Register `QUOTE_LC_BENCHMARK_CARD` with 5 format-specific criteria
- [ ] Register `COMPARISON_LC_BENCHMARK_CARD` with format-specific criteria
- [ ] Register `SCREENSHOT_LC_BENCHMARK_CARD` with format-specific criteria
- [ ] Register `ATMOSPHERIC_LC_BENCHMARK_CARD` with format-specific criteria
- [ ] Register `CINEMATIC_STORY_LC_BENCHMARK_CARD` with format-specific criteria
- [ ] Register `ANIMATED_EXPLAINER_LC_BENCHMARK_CARD` with format-specific criteria
- [ ] Register anti-slop floor thresholds per format family

### Resolution Services

- [ ] Add `resolve_lc_profile(format_family)` to `BenchmarkProfileRegistry`
- [ ] Create `PresenceWeightResolver` service
- [ ] Create `DeliveryQualityScorer` service
- [ ] Create `AntiSlopGateEnforcer` service
- [ ] Create `SSSBridgeEmitter` service

### Persistence

- [ ] Create `living_commentary_benchmark_profiles` table
- [ ] Create `delivery_quality_scores` table
- [ ] Create `anti_slop_gate_verdicts` table
- [ ] Create `presence_weight_profiles` table

### Receipt Chain

- [ ] Add receipt entries for `lc_benchmark_resolved`, `delivery_quality_scored`, `anti_slop_gate_passed`, `anti_slop_gate_rejected`, `sss_bridge_emitted`, `lc_benchmark_fallback`, `delivery_quality_fallback`

### Testing

- [ ] Unit tests for `DeliveryQualityDimensions` validation and composite calculation
- [ ] Unit tests for `PresenceWeightProfile` sum-to-1.0 validation
- [ ] Unit tests for `AntiSlopBenchmarkGate` pass/fail logic
- [ ] Integration tests for Living Commentary benchmark resolution chain
- [ ] Non-regression tests confirming v1.0 baselines remain unchanged
- [ ] Integration tests for SSS bridge packet emission

---

## 8. Acceptance Criteria

### AC-LC-BEN-1 — Each format family has a distinct presence weight profile

**Given** a request to resolve presence weight profiles for all 6 Living Commentary format families,
**When** the `PresenceWeightResolver` resolves each profile,
**Then** all 6 profiles have different weight distributions,
**And** Screenshot commentary has the highest `presence_weight` (≥0.50),
**And** Atmospheric commentary has the highest `visual_craft_weight` (≥0.35),
**And** Animated Explainer has the highest `content_weight` (≥0.30),
**And** all 3 channels (presence, visual_craft, content) sum to 1.0 for each profile.

**FAILURE EXAMPLE:** All 6 format families return `PresenceWeightProfile(presence_weight=0.33, visual_craft_weight=0.33, content_weight=0.34)`. That applies identical presence weighting to a judgment-led Screenshot Commentary and an atmosphere-led Cinematic Story, ignoring that delivery presence is the primary value carrier in reaction-style content while visual craft dominates atmospheric content. This produces false equivalence scores.

**Constraint:** Benchmark-Preserves-Delivery Rule, Format-Specific-Card Rule.

### AC-LC-BEN-2 — Delivery quality dimensions produce meaningful composite scores

**Given** delivery quality metrics `{pause_quality: 80, transition_strength: 70, emotional_modulation: 85, story_retention: 65, humor_landing: 50, objection_clarity: 75, close_integrity: 70, replay_usefulness: 60}`,
**When** the `DeliveryQualityScorer` computes the composite delivery score,
**Then** the composite is a weighted average across all 8 dimensions,
**And** pause quality and emotional modulation have higher weight than humor landing,
**And** the composite score is between 0 and 100,
**And** each dimension has at least one evidence citation.

**FAILURE EXAMPLE:** The system computes a simple arithmetic mean of all 8 dimensions (69.375) and reports that as the composite. That ignores the Source of Truth's emphasis that pause quality and emotional modulation are the hardest to fake and most visible to the audience — they should carry more weight than humor landing, which is optional in many format families.

**Constraint:** Benchmark-Preserves-Delivery Rule.

### AC-LC-BEN-3 — Anti-slop gate rejects "talking head with captions"

**Given** a Living Commentary piece with `motion_grammar_active=False`, `sonic_doctrine_compliant=False`, `atmospheric_field_present=False`, and `composite_delivery_score=55`,
**When** the `AntiSlopGateEnforcer` evaluates the content,
**Then** the gate returns `passed=False`,
**And** the `failures` list includes `"motion_grammar_inactive"`, `"sonic_doctrine_noncompliant"`, `"atmospheric_field_absent"`,
**And** the `rejection_reason` explains that the content degrades to "talking head with captions",
**And** the overall score is capped at 55 (the `overall_cap_when_slop_above_threshold`).

**FAILURE EXAMPLE:** The system scores a Living Commentary piece at 78 overall despite the content being nothing more than the coach speaking to camera with subtitle text overlaid on a flat white background, no motion grammar, no sonic punctuation, and no atmospheric field. That rewards the exact commodity format that Living Commentary was designed to replace, directly contradicting the Source of Truth §2.1 which states that "the problem is that a huge percentage of carousel-like assets now signal easy production, AI familiarity, weak authorship."

**Constraint:** Anti-Slop Benchmark Rule.

### AC-LC-BEN-4 — Living Commentary baselines differ from v1.0 baselines

**Given** the 6 Living Commentary benchmark cards and the 3 v1.0 baselines,
**When** comparing their `VisibleScoreWeightMap` distributions,
**Then** all Living Commentary cards emphasize Presence more than the v1.0 single-image baseline,
**And** the Quote LC card emphasizes Presence more than the v1.0 carousel baseline,
**And** the Atmospheric LC card emphasizes Memorability more than the v1.0 reel baseline,
**And** the v1.0 baselines (`CBP-IMG-001`, `CBP-CAR-001`, `CBP-REEL-001`) remain completely unchanged.

**FAILURE EXAMPLE:** The Living Commentary Quote card returns the same weights as `CBP-REEL-001` (humanity=0.20, presence=0.22, trust=0.12, memorability=0.18, resonance=0.18, signal=0.10). That treats a judgment-led commentary piece identically to a generic reel, ignoring that Living Commentary is fundamentally performance-led and requires higher Presence weighting.

**Constraint:** No-One-Score-Fits-All Rule, Benchmark-Preserves-Delivery Rule.

### AC-LC-BEN-5 — SSS bridge packet is emitted correctly

**Given** a scored Living Commentary piece with `composite_delivery_score=72`, `format_family=QUOTE`, `anti_slop_passed=True`,
**When** the `SSSBridgeEmitter` emits an SSS bridge packet,
**Then** the packet contains all 8 delivery quality dimension scores,
**And** the `composite_delivery_score` matches the computed value,
**And** the `presence_weight_applied` matches the format family's presence weight,
**And** the packet includes `coach_id`, `content_asset_id`, and `scored_at` timestamp.

**FAILURE EXAMPLE:** The SSS bridge emits only the composite score (72) without the individual dimension breakdown. That prevents FR-ERA3-35C from identifying which delivery dimensions are weak (e.g., humor landing at 35 while all others are above 70), making the Seminar Speaking Score a generic number instead of a diagnostic tool.

**Constraint:** SSS integration bridge contract.

### AC-LC-BEN-6 — Format-specific criteria are scorable per format family

**Given** the Quote Living Commentary benchmark card,
**When** inspecting its `format_criteria` list,
**Then** it contains at least 4 format-specific criteria,
**And** each criterion has a `criterion_id`, `criterion_name`, `description`, `weight_in_card`, and `scoring_rubric`,
**And** the weights of all criteria in the card sum to 1.0 within tolerance,
**And** the criteria include `interpretive_stance_clarity` (specific to Quote commentary, not applicable to Atmospheric commentary).

**FAILURE EXAMPLE:** All 6 format families share the same 5 generic criteria (e.g., "visual quality", "audio clarity", "engagement", "relevance", "coherence"). That makes the benchmark cards interchangeable and meaningless — a Quote commentary should be scored on interpretive stance clarity while an Atmospheric commentary should be scored on emotional field immersion. Generic criteria cannot distinguish between format families.

**Constraint:** Format-Specific-Card Rule.

---

## 9. Dependencies

### Internal Services

| Dependency | Type | Use |
|---|---|---|
| `FR-ERA3-35A Eval Registry` | Upstream | Provides canonical eval taxonomy consumed by benchmark profiles |
| `FR-ERA3-35C Eval Card System` | Downstream consumer | Consumes `SSSBridgePacket` for SSS progression updates |
| `FR-ERA3-35 Audit Intelligence Engine` | Downstream consumer | Uses profiles for automated audit scoring |
| `FR-ERA3-16 Archetype Container Runtime` | Read dependency | `ArchetypeChoice` enum for bundle keying (retained from v1.0) |
| `FR-ERA3-12 CMF Arc-Governed Rendering` | Read dependency | Content type, format family, motion grammar activation status |
| `FR-ERA3-48 Persuasive Speaking Program` | Downstream consumer | Delivery quality dimensions inform practice task selection |
| `ReceiptChain` | Existing core | Extended with Living Commentary benchmark-specific receipt entries |

### Internal Models

| Dependency | Type | Use |
|---|---|---|
| `archetype_container_runtime_models.py` | Read-only | `ArchetypeChoice` enum (retained from v1.0) |
| `cmf_arc_render_models.py` | Read-only | `CoalitionSpineInput.selected_format` for content-type inference |
| `benchmark_profile_models.py` | Extended | 10 new models + 6 new enum values added to existing file |
| Supabase | Existing infra | 4 new tables |

### External

| Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed model definitions with validators |

---

## 10. Testing Strategy

### 10.1 Unit Tests

#### `test_frera35b_v2_delivery_quality.py`

- `test_delivery_dimensions_all_within_range`
- `test_delivery_dimensions_negative_fails`
- `test_delivery_dimensions_above_100_fails`
- `test_composite_score_weighted_correctly`
- `test_composite_score_with_all_zeros_returns_zero`
- `test_composite_score_with_all_100_returns_100`
- `test_pause_and_modulation_outweigh_humor`

#### `test_frera35b_v2_presence_weight.py`

- `test_presence_profile_sum_exactly_one_passes`
- `test_presence_profile_sum_below_099_fails`
- `test_presence_profile_sum_above_101_fails`
- `test_presence_weight_negative_fails`
- `test_each_format_family_has_distinct_profile`

#### `test_frera35b_v2_anti_slop_gate.py`

- `test_all_criteria_met_passes_gate`
- `test_motion_grammar_inactive_fails`
- `test_sonic_doctrine_noncompliant_fails`
- `test_atmospheric_field_absent_fails`
- `test_composite_below_floor_fails`
- `test_multiple_failures_all_reported`
- `test_talking_head_with_captions_rejected`

### 10.2 Integration Tests

#### `tests/integration/test_frera35b_v2_lc_resolution_chain.py`

Scenario class: `TestACLCBEN1PresenceWeightDifferentiation`

- Resolve presence weight profiles for all 6 format families.
- Assert all 6 have different weight distributions.
- Assert Screenshot has highest `presence_weight`.
- Assert Atmospheric has highest `visual_craft_weight`.
- Assert all channels sum to 1.0.

Scenario class: `TestACLCBEN2DeliveryQualityComposite`

- Score delivery quality with known metrics.
- Assert composite score matches expected weighted average.
- Assert pause quality and emotional modulation have higher impact than humor landing.

Scenario class: `TestACLCBEN3AntiSlopGate`

- Submit content with no motion grammar, no sonic doctrine, no atmospheric field.
- Assert gate returns `passed=False` with specific failure reasons.
- Assert overall score is capped at 55.

Scenario class: `TestACLCBEN4BaselineDifferentiation`

- Resolve all 6 LC cards and all 3 v1.0 baselines.
- Assert LC cards emphasize Presence more than v1.0 image baseline.
- Assert v1.0 baselines remain unchanged.

#### `tests/integration/test_frera35b_v2_sss_bridge.py`

Scenario class: `TestACLCBEN5SSSBridgeEmission`

- Score a Living Commentary piece.
- Emit SSS bridge packet.
- Assert packet contains all 8 dimension scores, composite, presence weight, coach ID, asset ID, timestamp.

### 10.3 Non-Regression Expectations

- No test may accept identical presence weights for all format families.
- No test may accept a Living Commentary piece that passes the anti-slop gate without active motion grammar.
- No test may accept an SSS bridge packet without all 8 delivery dimension scores.
- No test may accept a composite delivery score that gives equal weight to all 8 dimensions.
- No test may allow v1.0 baselines (`CBP-IMG-001`, `CBP-CAR-001`, `CBP-REEL-001`) to be modified.
- No test may accept a format-specific criterion list shared identically across all 6 format families.
- No test may accept a `PresenceWeightProfile` whose 3 channels do not sum to 1.0.
