# Tech-Spec: FR-ERA3-ScoreCard - Score Card Viewer Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - RIM-Hardened)
**Phase:** 3 - Experience Mini Apps
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new Mini App routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      Supabase schema changes extend `src/ccp/scripts/setup_supabase.py`, Section 3 requires the
                      spec to map directly onto existing services instead of reinventing them, and Section 4
                      requires explicit mandate enforcement even when the governing rule is primitive-driven rather
                      than a numbered phase conflict.
2. PRD LOADED:        PRD-05 exact evidence definition: "The speaking-evidence packet should minimally capture:
                      conviction density, hedge frequency, pause architecture, pitch stability, selected
                      stylometric indicators, trend deltas from baseline, and notable raw language anchors."
                      PRD-05 also states: "FR61-type metrics are powerful not just because they are measurable,
                      but because they convert fuzzy self-perception into undeniable progression." PRD-04 exact
                      experience rule: "PRD-04 should treat score reveals as branded rituals, not just data dumps.
                      A bad score should create: reflection, a viable comeback path, and belief that improvement
                      is possible."
3. EPIC LOADED:       Epic 5 exact goal: "Present the FR61 evidence contract (Conviction Density, Hedge
                      Frequency, Pause Architecture, Pitch Stability) as a reflective, status-bearing artifact
                      rather than a punishing clinical report." Story 5.1 first AC: "Given my continuous voice
                      submissions have generated an FR61 evidence packet, When I open the Score Card Viewer, Then
                      I see my trend deltas for hedge frequency and conviction density, paired explicitly with a
                      developmental insight or next-step recommendation."
4. CBAR LOADED:       The Phase 3 audit contains no dedicated Epic 5 rewrite and the Phase 3 story matrix marks
                      Score Card Viewer as "Pass — No Changes Required." There is therefore no numbered fatal
                      conflict for this spec, but `EXP-FBK-001` remains binding: bare score numbers without
                      interpretation are banned.
5. PRIMITIVES:        `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
                      `experience_primitive_id: "EXP-FBK-004"` / `canonical_name: "Bring the Data Forward"`
6. BACKEND:           `src/ccp/services/scorecard_emitter.py` - `def emit(self, scorecard: LeadershipScorecard, raise_on_validation_failure: bool = True) -> tuple[LeadershipScorecard, list[str]]`
                      `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
                      `src/ccp/services/dpa_engine.py` - `async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = "", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None) -> DPAResult`
                      `src/ccp/models/leadership_scorecard_models.py` - `def get_weak_traits(self, threshold: int = WEAK_TRAIT_THRESHOLD) -> list[ScoredTrait]`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper functions, typed model
                      assertions, scenario-oriented test classes, and direct verification of contract fields rather
                      than generic black-box smoke tests.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P3_S19_Score_Card_Viewer.md` | 2026-05-11 | Assignment prompt, source boundary, and output target |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory stack, route, schema, and CBAR formatting requirements |
| 3 | `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | 2026-05-10 | Epic 5 goal, Story 5.1 AC, and `EXP-FBK-001` quality standard |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | 2026-05-10 | Confirmation that Epic 5 has no rewrite and no hallucination correction affecting this story |
| 5 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | v6.0, 2026-05-06 | Score reveal ritual, reflection, comeback-path doctrine, and Mini App experience rules |
| 6 | `docs/prd/modules/PRD_05_CBCS_Law28.md` | v6.0, 2026-05-06 | FR61 evidence contract, progression evidence, and scorecard rendering intent |
| 7 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Verified governing primitive for relevant/immediate/meaningful feedback |
| 8 | `primitives/experience/feedback_scoring/EXP-FBK-004.yaml` | Codified registry | Verified supporting primitive for clear delta surfacing |
| 9 | `src/ccp/services/scorecard_emitter.py` | Existing service | Canonical producer of `leadership_scorecard.json` |
| 10 | `src/ccp/services/trait_scoring_engine.py` | Existing service | Upstream trait/evidence source feeding the emitter |
| 11 | `src/ccp/models/leadership_scorecard_models.py` | Existing models | Canonical 12-trait, evidence, history, category, and production-lock schema |
| 12 | `src/ccp/services/dpa_engine.py` | Existing service | Existing branding/palette contract for a non-clinical reflective viewer |
| 13 | `src/ccp/services/engagement_feedback.py` | Existing service | Existing feedback-ingestion pattern and receipt-chain discipline |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI registration and `/health` extension point |
| 15 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit trail for viewer opens and reflection acknowledgements |
| 16 | `src/ccp/core/circuit_breaker.py` | Current | Failure protection and high-risk halt rules |
| 17 | `src/ccp/scripts/setup_supabase.py` | Current | Canonical schema extension point |
| 18 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and receipt assertions |
| 19 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async helper style and scenario grouping |
| 20 | `docs/architecture/april_updates/FR-ERA3-11_Challenge_Arena_Tech_Spec.md` | 2026-05-11 draft | Confirmed prior Era3 usage of named FR61 metrics and delta cards as a read-side projection pattern |

## 2. Overview

### 2.1 Problem Statement

The backend already produces a validated leadership scorecard, but there is still no participant-facing surface that turns that file into a usable developmental experience. `scorecard_emitter.py` writes `leadership_scorecard.json` with 12 scored traits, evidence citations, category coverage, history, and production-lock metadata. That is enough to support a powerful reflection ritual, but only if the UI interprets it correctly.

Without a dedicated Score Card Viewer Mini App, the current system fails in four ways:

- the participant never sees the scorecard as a first-class artifact inside Telegram
- raw scores can be exposed without interpretation, violating `EXP-FBK-001`
- evidence citations remain buried in JSON instead of becoming coach-readable proof
- low scores can feel clinical or punitive instead of actionable, which directly contradicts PRD-04

There is also a source-shape wrinkle we need to handle honestly: the emitted scorecard is trait-centric, while the story names FR61 signal deltas like hedge frequency and conviction density. This spec solves that by adding a visualization-only projection layer that reads the emitted scorecard and derives the display packet without changing how scoring works.

### 2.2 Solution

This spec creates `startapp=score` as a Telegram Mini App that reads the emitted leadership scorecard and renders it as a reflective, status-bearing artifact. The app remains visualization-only. It does not rescore, mutate, or reinterpret source truth through a new scoring engine. Instead it adds four read-side layers:

- `ScorecardFileReader` to load `leadership_scorecard.json`
- `Fr61SignalProjectionAdapter` to build named signal cards and deltas from existing emitted scorecard history and `config/fr61_evidence_packet.json`
- `ScoreMeaningProjector` to pair every score with a deterministic developmental interpretation
- `ScoreCardViewerThemeResolver` to apply DPA-driven reflective theming so the surface feels like guidance, not punishment

The resulting viewer has five core visual zones:

1. a status-bearing score reveal header
2. four FR61 delta cards
3. a 12-trait radar visualization
4. evidence citations and source availability
5. next-step recommendations and comeback-path copy

### 2.3 Scope

**In scope:**

- `startapp=score` Mini App shell and launch contract
- read-only load of `leadership_scorecard.json`
- 12-trait radar visualization
- evidence citation display per trait
- deterministic interpretation and next-step rendering per score
- FR61 signal cards for conviction density, hedge frequency, pause architecture, and pitch stability
- trend projection from scorecard history and supporting view data
- production-lock and weak/strong trait projection in participant-safe language
- DPA-resolved visual theme for a branded score ritual
- receipt logging for viewer opens and reflection acknowledgements

**Out of scope:**

- changing `TraitScoringEngine`
- changing `ScorecardEmitter`
- creating or modifying the underlying FR61 extraction pipeline
- inventing a new clinical benchmark schema
- replacing the coaching logic in Challenge Arena or Sunday Postcard
- public testimonial or user-card sharing flows, which belong to other specs

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Payload Object | Source FR | What It Does |
|---|---|---|---|
| DEP-SCV-001 | `ScoreCardViewerPayload` | FR-ERA3-ScoreCard | Main projection payload sent to the Mini App containing traits, evidence, and signal deltas |
| DEP-SCV-002 | `ScoreViewerAckRequest` | FR-ERA3-ScoreCard | Participant acknowledgement of a specific insight or next-step recommendation |
| DEP-SCV-003 | `ScoreViewerAckResponse` | FR-ERA3-ScoreCard | Backend confirmation of the recorded acknowledgement with receipt ID |
| DEP-SCV-004 | `TraitDetailPayload` | FR-ERA3-ScoreCard | Single-trait deep-dive payload with specific evidence citations and historical trend |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `scorecard_emitter.py` | `src/ccp/services/scorecard_emitter.py` | Treats `emit(...)` as the sole producer of `leadership_scorecard.json`. The viewer never writes to that file and never recomputes scores. |
| `leadership_scorecard_models.py` | `src/ccp/models/leadership_scorecard_models.py` | Reuses `LeadershipScorecard`, `ScoredTrait`, `TraitEvidence`, `SignalSourceAvailability`, `ProductionLockResult`, and trait-history helpers instead of inventing parallel score schemas. |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Referenced only as an upstream provenance source. The viewer may expose its outputs but may not call it on-demand for the participant UI. |
| `dpa_engine.py` | `src/ccp/services/dpa_engine.py` | Uses `resolve(...)` to theme the viewer as a reflective ritual, not a sterile report card. |
| `engagement_feedback.py` | `src/ccp/services/engagement_feedback.py` | Provides an existing pattern for analytics ingestion and receipt discipline if viewer interactions later need capture. |
| `main.py` | `src/ccp/api/main.py` | Registers the Score Card Viewer router and extends `/health` with viewer-readiness data. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs viewer opens, missing-scorecard fallback, and reflection acknowledgement events. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Protects any automated outreach or escalation copy that could follow a risky score reflection context. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends schema for viewer sessions, acknowledgements, and cached projections where needed. |

**Existing data artifacts consumed:**

- `config/leadership_scorecard.json` - canonical emitted scorecard artifact
- `config/fr61_evidence_packet.json` - canonical FR61 metrics input
- `receipt_chain` - immutable audit records
- `asset_registry` - optional visual asset pointers if branded cards or images are generated later
- `person_registry` - participant and coach identity mapping
- `resolved_palettes` - optional DPA palette audit trail when theme resolution is persisted

**New score viewer tables introduced by this spec:**

- `score_viewer_sessions` - one row per user-viewed scorecard session
- `score_viewer_reflection_acks` - explicit acknowledgement of insights, weak-trait focus, or next-step acceptance
- `score_viewer_projection_cache` - cached UI projection rows keyed by scorecard version and timestamp

**Existing API routes extended or called:**

- `GET /health` - extended with Score Card Viewer readiness

**New API routes introduced by this spec:**

- `GET /api/score/{coach_id}/current` - fetch the current projected score viewer payload
- `GET /api/score/{coach_id}/history` - fetch historical projected sessions where available
- `POST /api/score/{coach_id}/ack` - acknowledge a selected insight, next step, or comeback target
- `GET /api/score/{coach_id}/trait/{trait_name}` - fetch a single-trait deep-dive payload and evidence list

**Important source-boundary rule**

The score viewer may read:

- `leadership_scorecard.json`
- its trait history
- production-lock metadata
- `config/fr61_evidence_packet.json` (read-only input providing the raw FR61 signal deltas)

The score viewer may not:

- call `score_all_traits()` on demand for the participant
- mutate `leadership_scorecard.json`
- write back to `coach_soul.json`, `ttt_baseline.json`, or `tribe_soul.json`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Every score and every named FR61 signal must be paired with an interpretation that is relevant to a behavior, immediate to the current state, and meaningful as a next move. Bare numbers are banned. |
| `EXP-FBK-004` | Bring the Data Forward | feedback_scoring | Trend deltas and evidence anchors must be surfaced before interpretation drifts into generic motivational copy. The participant should first see what changed, then why it matters. |

### 3.4 CBAR Mandate Enforcement

This spec has no direct numbered Phase 3 fatal-conflict mandate. However, Epic 5 is still governed by a binding primitive quality rule from `EXP-FBK-001`.

| Governing Rule | Story | Implementation Mechanism |
|---|---|---|
| RIM Feedback Discipline | Story 5.1 | `ScoreMeaningProjector` attaches a meaning block and next-step recommendation to every trait and FR61 delta card. Routes must reject payloads that expose raw scores without interpretation. |
| Bring the Data Forward | Story 5.1 | `Fr61SignalProjectionAdapter` and `EvidenceCitationProjector` place delta/evidence cards ahead of recommendation copy so the score feels grounded instead of decorative. |

**Formal interpretation invariant**

| Display Element | Required Companion |
|---|---|
| trait score | short developmental interpretation + one next step |
| FR61 delta card | trend direction + why-it-matters copy |
| weak-trait callout | comeback-path recommendation |
| production-lock explanation | human-readable unlock guidance |
| evidence citation | named source + quote/description + rubric contribution |

**Hard fail cases**

- a route returns numeric traits with empty interpretation blocks
- a radar chart renders without any evidence drill-down path
- low scores are shown with punitive or shame-coded copy
- hedge frequency / conviction density deltas are omitted when the projection source has the data
- the viewer fabricates unavailable metric numbers instead of marking them unavailable

### 3.5 Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Viewer type | Read-only reflection Mini App | Prompt explicitly limits this spec to visualization, not scoring |
| File source of truth | `leadership_scorecard.json` | `scorecard_emitter.py` is already the canonical producer |
| Signal-delta handling | Add a read-only projection adapter | Story 5.1 names FR61 deltas that are not fully represented as first-class top-level fields in the emitted scorecard |
| Trait visualization | 12-point radar plus category grouping | Matches the existing 12-trait schema and helps participants see pattern shape, not just list order |
| Recommendation generation | Deterministic mapping, not freeform LLM copy | Keeps RIM compliance stable and testable |
| Theme system | DPA-driven reflective palette | PRD-04 requires score reveals to feel branded and meaningful rather than clinical |
| Production lock exposure | Translate internal gate into developmental language | Raw internal gate jargon is useful for engineers, not participants |
| Acknowledgement capture | Explicit insight acknowledgement route | Lets the system record what guidance resonated without changing the score artifact |

## 4. Implementation Plan

### Phase 1 - Core Read Path and Mini App Shell

| Task ID | Task | Output |
|---|---|---|
| P1-T1 | Register `startapp=score` router in `main.py` | Mini App becomes addressable and health-reportable |
| P1-T2 | Create `score_viewer_sessions`, `score_viewer_reflection_acks`, and `score_viewer_projection_cache` tables | Canonical persistence for view sessions and cached projections |
| P1-T3 | Implement `ScorecardFileReader` | Safe load/validate path for `leadership_scorecard.json` |
| P1-T4 | Implement `ScorecardProjectionService` | Single backend entrypoint for assembling the viewer payload |
| P1-T5 | Add `GET /api/score/{coach_id}/current` route | Participant load path |
| P1-T6 | Emit receipt events for scorecard open and missing-scorecard fallback | Audit trail |

### Phase 2 - Trait Radar and Evidence Layer

| Task ID | Task | Output |
|---|---|---|
| P2-T1 | Implement `TraitRadarProjector` | 12-trait radar points, axis ordering, and score bands |
| P2-T2 | Implement `EvidenceCitationProjector` | Normalized citation cards from `TraitEvidence` |
| P2-T3 | Implement `WeakStrongTraitSummarizer` | Participant-safe focus areas from weak/strong traits |
| P2-T4 | Add single-trait deep-dive API route | `GET /api/score/{coach_id}/trait/{trait_name}` |
| P2-T5 | Expose signal-source availability state | Source completeness banner and fallback logic |
| P2-T6 | Cache projected radar/evidence payloads | Faster repeated opens without modifying scoring |

### Phase 3 - FR61 Delta Cards and Meaning Layer

| Task ID | Task | Output |
|---|---|---|
| P3-T1 | Implement `Fr61SignalProjectionAdapter` | Named cards for conviction density, hedge frequency, pause architecture, and pitch stability |
| P3-T2 | Implement `ScoreMeaningProjector` | Deterministic interpretation and next-step blocks |
| P3-T3 | Implement `ProductionLockExplainer` | Readable unlock guidance for incomplete categories |
| P3-T4 | Add `GET /api/score/{coach_id}/history` route | Historical trend visualization support |
| P3-T5 | Add `POST /api/score/{coach_id}/ack` route | Insight acknowledgement persistence |
| P3-T6 | Enforce payload validation: no raw score without interpretation | RIM guardrail at the API boundary |

### Phase 4 - Theming, Fallbacks, and Verification

| Task ID | Task | Output |
|---|---|---|
| P4-T1 | Implement `ScoreCardViewerThemeResolver` with `DPAEngine.resolve(...)` | Reflective viewer palette and emphasis rules |
| P4-T2 | Add source-unavailable and stale-scorecard states | Honest fallback rather than fabricated confidence |
| P4-T3 | Integrate `circuit_breaker.py` for risky follow-up or outreach suppression | Safe reflection behavior |
| P4-T4 | Extend `/health` with score-viewer readiness | Operational visibility |
| P4-T5 | Write unit tests for projection, meaning, and availability rules | Regression safety |
| P4-T6 | Write integration tests for file load, payload contract, and fallback behavior | End-to-end confidence |

## 5. Output Schema

All contracts below use Pydantic v2 style and avoid `Any`. They define the viewer projection layer, not the upstream scoring layer.

```python
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ViewerScoreBand(str, Enum):
    low = "low"
    developing = "developing"
    strong = "strong"


class TrendDirection(str, Enum):
    up = "up"
    down = "down"
    flat = "flat"
    unavailable = "unavailable"


class SignalMetricKey(str, Enum):
    conviction_density = "conviction_density"
    hedge_frequency = "hedge_frequency"
    pause_architecture = "pause_architecture"
    pitch_stability = "pitch_stability"


class RecommendationPriority(str, Enum):
    primary = "primary"
    secondary = "secondary"


class ProjectionAvailability(str, Enum):
    available = "available"
    partial = "partial"
    unavailable = "unavailable"


class TraitRadarPoint(BaseModel):
    trait_name: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=1, le=10)
    max_score: int = Field(default=10, ge=1)
    category: str = Field(..., min_length=1)
    score_band: ViewerScoreBand = Field(...)


class EvidenceCitationCard(BaseModel):
    signal_source: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    rubric_points: int = Field(..., ge=0)


class ScoreMeaningBlock(BaseModel):
    headline: str = Field(..., min_length=1)
    interpretation: str = Field(..., min_length=1)
    why_it_matters: str = Field(..., min_length=1)
    next_step: str = Field(..., min_length=1)
    priority: RecommendationPriority = Field(default=RecommendationPriority.primary)


class TraitInsightCard(BaseModel):
    trait_name: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=1, le=10)
    category: str = Field(..., min_length=1)
    evidence: list[EvidenceCitationCard] = Field(default_factory=list)
    meaning: ScoreMeaningBlock = Field(...)
    is_weak_focus: bool = Field(default=False)
    is_strength_anchor: bool = Field(default=False)


class Fr61SignalDeltaCard(BaseModel):
    metric_key: SignalMetricKey = Field(...)
    label: str = Field(..., min_length=1)
    current_value: float | None = Field(default=None)
    baseline_value: float | None = Field(default=None)
    delta_value: float | None = Field(default=None)
    direction: TrendDirection = Field(...)
    availability: ProjectionAvailability = Field(...)
    explanation: str = Field(..., min_length=1)
    next_step: str = Field(..., min_length=1)


class ProductionLockExplanation(BaseModel):
    all_categories_met: bool = Field(default=False)
    locked_categories: list[str] = Field(default_factory=list)
    unlock_message: str = Field(default="")
    participant_copy: str = Field(..., min_length=1)


class ScoreViewerTheme(BaseModel):
    mood_key: str = Field(..., min_length=1)
    background_primary: str = Field(..., min_length=1)
    background_secondary: str = Field(..., min_length=1)
    text_primary: str = Field(..., min_length=1)
    accent: str = Field(..., min_length=1)
    brand_hue_used: bool = Field(default=False)


class ScoreDataAvailability(BaseModel):
    scorecard_file: ProjectionAvailability = Field(...)
    signal_cards: ProjectionAvailability = Field(...)
    evidence_citations: ProjectionAvailability = Field(...)
    production_lock: ProjectionAvailability = Field(...)


class ScoreCardViewerPayload(BaseModel):
    coach_id: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    scored_at: str = Field(..., min_length=1)
    last_updated: str = Field(..., min_length=1)
    availability: ScoreDataAvailability = Field(...)
    dominant_trait_label: str | None = Field(default=None)
    weak_focus_labels: list[str] = Field(default_factory=list)
    radar_points: list[TraitRadarPoint] = Field(default_factory=list)
    signal_cards: list[Fr61SignalDeltaCard] = Field(default_factory=list)
    top_insights: list[TraitInsightCard] = Field(default_factory=list)
    production_lock: ProductionLockExplanation = Field(...)
    theme: ScoreViewerTheme = Field(...)
    source_availability_banner: str = Field(..., min_length=1)


class ScoreViewerAckRequest(BaseModel):
    insight_key: str = Field(..., min_length=1)
    acknowledged_next_step: str = Field(..., min_length=1)


class ScoreViewerAckResponse(BaseModel):
    coach_id: str = Field(..., min_length=1)
    ack_id: str = Field(..., min_length=1)
    insight_key: str = Field(..., min_length=1)
    receipt_id: str = Field(..., min_length=1)


class TraitDetailPayload(BaseModel):
    coach_id: str = Field(..., min_length=1)
    trait_name: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=1, le=10)
    score_band: ViewerScoreBand = Field(...)
    category: str = Field(..., min_length=1)
    evidence: list[EvidenceCitationCard] = Field(default_factory=list)
    meaning: ScoreMeaningBlock = Field(...)
    history_points: list[int] = Field(default_factory=list)
```

**Schema notes**

- `ScoreMeaningBlock` is mandatory anywhere a participant sees a score.
- `Fr61SignalDeltaCard` allows `None` numeric fields because the viewer must be able to tell the truth when a named delta is unavailable instead of fabricating a value.
- `ScoreDataAvailability` lets the frontend render partial states deliberately instead of silently dropping sections.

## 6. Backward Compatibility Fallback

The viewer is read-only, so backward compatibility is mainly about safe degradation when source artifacts are missing, stale, or partial.

### 6.1 Fallback States

| Failure Case | Detection | Fallback Behavior |
|---|---|---|
| `leadership_scorecard.json` missing | file not found | render a `score_pending` state with a participant-safe message and no fabricated scores |
| `leadership_scorecard.json` invalid | Pydantic validation error | render a `score_unavailable` state, log a receipt, and show a retry/support message |
| signal deltas unavailable | projection adapter has insufficient source data | still render trait radar and evidence; signal cards show `availability=unavailable` and no numeric fiction |
| evidence partially missing | malformed or incomplete trait evidence | hide only the broken citation row, flag `partial`, and surface a source-availability banner |
| production-lock absent | legacy or incomplete scorecard version | omit lock explanation and show a non-blocking informational banner |
| DPA theme resolution fails | `resolve(...)` error | fall back to a safe neutral reflective palette, not raw default browser styling |

### 6.2 Circuit Breaker Integration

Even though the viewer is mostly read-only, it can still participate in emotionally sensitive flows. The viewer must check `circuit_breaker.py` before:

- sending any automated follow-up nudge based on a weak score
- surfacing a push recommendation that would automatically route into another experience
- auto-suggesting public or social escalation from the score surface

If the breaker is active (i.e., `circuit_breaker.get_state(coach_id).is_active == True` indicating a high-risk escalation threshold > 0.85 was reached in the past 24 hours):

- the score remains viewable
- automated follow-up prompts are suppressed
- a receipt is written for the suppressed escalation
- the UI stays reflective rather than persuasive

### 6.3 No-Rescore Guarantee

Fallback logic may never:

- call `TraitScoringEngine.score_all_traits()` from the participant viewer
- rewrite `leadership_scorecard.json`
- replace missing numbers with guessed values

If data is missing, the system must say it is missing.

## 7. Tasks

1. Add the Score Card Viewer router to [main.py](/D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
2. Extend [setup_supabase.py](/D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with `score_viewer_sessions`, `score_viewer_reflection_acks`, and `score_viewer_projection_cache`.
3. Create score-viewer read models in `src/ccp/models/`.
4. Implement `ScorecardFileReader` to load and validate `config/leadership_scorecard.json`.
5. Implement `ScorecardProjectionService` as the single projection entrypoint.
6. Implement `TraitRadarProjector` for the 12-trait radar data contract.
7. Implement `EvidenceCitationProjector` for normalized evidence display cards.
8. Implement `WeakStrongTraitSummarizer` using `get_weak_traits()`, `get_strong_traits()`, and `dominant_trait()`.
9. Implement `Fr61SignalProjectionAdapter` for named metric cards and availability-aware deltas.
10. Implement `ScoreMeaningProjector` with deterministic interpretation and next-step mappings.
11. Implement `ProductionLockExplainer` to translate internal gate state into participant-safe copy.
12. Implement `ScoreCardViewerThemeResolver` using [dpa_engine.py](/D:/Work/The Conscious Coaching Factory/src/ccp/services/dpa_engine.py).
13. Add `GET /api/score/{coach_id}/current`, `GET /api/score/{coach_id}/history`, `GET /api/score/{coach_id}/trait/{trait_name}`, and `POST /api/score/{coach_id}/ack`.
14. Add receipt-chain logging for open, fallback, and acknowledgement events.
15. Add circuit-breaker suppression rules for automated follow-up prompts.
16. Write unit and integration tests matching existing typed scenario patterns.

## 8. Acceptance Criteria

### Story 5.1 - Actionable Biometric Reflection

**AC-5.1-A**

- Given continuous voice submissions have generated an FR61 evidence packet and an emitted `leadership_scorecard.json`
- When the participant opens `startapp=score`
- Then the viewer loads a projected score payload from the emitted scorecard rather than rescoring on demand
- And the payload contains trend cards for hedge frequency and conviction density when source data is available
- And each of those cards is paired with a developmental explanation and next-step recommendation
- Mandate ref: Story 5.1, `EXP-FBK-001`
- Failure example: the app shows `hedge_frequency=3.1` and `conviction_density=0.58` as bare numbers with no explanation of what to do next

**AC-5.1-B**

- Given a valid projected score payload exists
- When the radar view is rendered
- Then all 12 traits from `LeadershipScorecard.traits` appear in the radar projection
- And the participant can open a trait detail view showing evidence citations, a meaning block, and a specific next-step recommendation
- Mandate ref: Story 5.1, `EXP-FBK-001`
- Failure example: the radar is decorative only, and clicking a low trait yields no evidence, no meaning, and no improvement path

**AC-5.1-C**

- Given a participant has one or more weak traits
- When the viewer summarizes their current state
- Then weak traits are framed as developmental focus areas with comeback-path language
- And the copy must not shame, punish, or treat the participant as deficient
- Mandate ref: PRD-04 Section 5.6, `EXP-FBK-001`
- Failure example: the viewer labels a low score as “bad leadership” or “failing” without any viable next move

**AC-5.1-D**

- Given the scorecard includes evidence citations and category/lock metadata
- When the participant opens the deep-dive sections
- Then they can see source-linked evidence descriptions and an understandable explanation of any production-lock condition
- And the explanation is translated into participant-safe improvement language rather than raw internal gate jargon
- Mandate ref: Story 5.1, `EXP-FBK-004`
- Failure example: the API exposes `PRODUCTION_LOCKED_CATEGORY_INCOMPLETE` with no explanation of what needs to improve

## 9. Dependencies

| Dependency Type | Name | Why It Matters |
|---|---|---|
| Existing service | `ScorecardEmitter.emit(...)` | Sole producer of the canonical scorecard file |
| Existing model | `LeadershipScorecard` / `ScoredTrait` / `TraitEvidence` | Canonical schema for traits, evidence, history, and lock state |
| Existing helper methods | `get_weak_traits()` / `get_strong_traits()` / `dominant_trait()` | Stable read-side semantics for focus areas and dominant strengths |
| Existing service | `DPAEngine.resolve(...)` | Required for branded, reflective score reveal theming |
| Existing service | `TraitScoringEngine.score_all_traits()` | Upstream provenance only; used to define what this viewer must not re-run |
| Existing core | `receipt_chain.py` | Immutable viewer-open and acknowledgement audit trail |
| Existing core | `circuit_breaker.py` | Suppresses risky automated follow-up flows |
| Existing storage | `config/leadership_scorecard.json` | Primary read artifact |
| Existing database | `person_registry` / `asset_registry` / `resolved_palettes` | Identity, optional assets, and theming persistence |
| Platform | Telegram Mini App runtime | Launch and interaction container for `startapp=score` |

**Dependency constraints**

- The viewer depends on emitted scorecard data, not live rescoring.
- The viewer may cache projections, but the cache may never become a source of truth over the underlying scorecard file.
- Theme resolution may enhance presentation, but it may not change the meaning or ordering of score data.

## 10. Testing Strategy

The testing structure must follow the typed, scenario-first style already used in:

- [test_cpsc_fr52_webinar_brief.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_cpsc_fr52_webinar_brief.py)
- [test_ca11_fr16_studio_block.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_ca11_fr16_studio_block.py)

### 10.1 Unit Tests

| Test Name | Purpose |
|---|---|
| `test_scorecard_projection_service_rejects_raw_scores_without_meaning_blocks` | Verifies the API payload cannot return score elements without interpretation |
| `test_trait_radar_projector_emits_twelve_points_in_registry_order` | Verifies radar output covers all 12 traits in stable order |
| `test_fr61_signal_projection_adapter_marks_missing_deltas_unavailable` | Verifies unavailable signal data is represented honestly instead of fabricated |
| `test_weak_strong_trait_summarizer_uses_model_helpers` | Verifies weak/strong summaries follow the scorecard model helpers |
| `test_production_lock_explainer_translates_internal_error_code` | Verifies lock state becomes participant-readable guidance |

### 10.2 Integration Tests

| Test Name | Purpose |
|---|---|
| `test_score_viewer_loads_current_payload_from_emitted_scorecard_file` | End-to-end file read, validation, and projection contract |
| `test_score_viewer_trait_detail_includes_evidence_and_next_step` | End-to-end deep-dive route proving evidence plus recommendation rendering |
| `test_score_viewer_fallback_honestly_marks_missing_signal_cards` | End-to-end partial-data fallback proving no fabricated FR61 numbers appear |

### 10.3 Test Data Requirements

- one valid `leadership_scorecard.json` fixture with 12 traits and evidence for each
- one partial scorecard fixture with missing signal projection inputs
- one scorecard fixture with weak traits and production-lock state
- DPA theme fixture or stubbed `resolve(...)` result
- receipt-chain assertions for viewer open and acknowledgement events

### 10.4 Mandatory Assertions

Every Story 5.1 integration test must assert all of the following:

- the returned payload includes interpretation for every visible score element
- at least one trait deep-dive includes evidence citations with source names
- weak-trait messaging includes a next-step recommendation
- missing signal metrics are labeled unavailable rather than guessed
- the route does not invoke any live score recomputation path

### 10.5 Non-Goals for Testing

This spec's tests do not need to:

- retest `TraitScoringEngine` internals
- retest `ScorecardEmitter` validation logic beyond consuming a valid emitted file
- benchmark radar-chart frontend rendering performance at scale
- validate public sharing or commercial conversion flows outside the viewer

