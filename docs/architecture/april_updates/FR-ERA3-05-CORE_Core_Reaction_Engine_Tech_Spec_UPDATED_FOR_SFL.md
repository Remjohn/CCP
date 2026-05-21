# Tech-Spec: FR-ERA3-05-CORE - Core Reaction Engine Updated for SFL

## Pre-Work Log

### 1. Protocol Read
- Read `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`.
- Confirmed this update must extend the existing backend stack, preserve real brownfield contracts, and define typed implementation surfaces and tests instead of theory-only architecture notes.

### 2. Source PRD Read - Reaction Scoring Purpose
- Read `docs/prd/modules/PRD_06_Conscious_Reactions.md`.
- Exact quote captured establishing product purpose:
  - "`Conscious Reactions` is the default async branded engine and the primary acquisition event for the Conscious Coaching Platform (CCP)."
- Exact quote captured establishing the human-first rule:
  - "We are not automating fake expertise; we are extracting, refining, and broadcasting real judgment."
- Exact quote captured establishing measurable benchmarking:
  - "The reaction is recorded simply under constraint, the delivery is biologically benchmarked, and the output is instantly shareable."
- Exact quote captured establishing negative-metric scoring:
  - "The DSPy pipeline and NIM reasoning models immediately score the reaction not just on conviction and pacing, but commercially via the `Damage Index` and `Compounding Forecast`..."
- Exact quote captured establishing anti-slop posture:
  - "The system enforces the Anti-Centroid Law by refusing to publish slop..."

### 3. Source PRD Read - Primitive / Truth Boundary
- Read `docs/prd/modules/PRD_08_Conscious_Primitives.md`.
- Exact quote captured:
  - "Primitives are **conscious faculties** — stable transformation operators..."
- Exact quote captured:
  - "**Meaning Plane (Plane A)** governs the coaching ontology..."
- Exact quote captured:
  - "**Experience Plane (Plane B)** governs the delivery layer..."
- Exact quote captured:
  - "`truth substrate -> primitive candidate field -> coalition -> edge product -> delivery stack -> variation stack -> validation -> destination packet`"
- Exact quote captured:
  - "the **truth substrate** includes Voice DNA, Negative Space, and SDA"
  - "the **delivery stack** includes SFL and composition depth profiles"

### 4. SFL Source Set Read - Structural Claims
- Read `lab/subliminal_function_layer_for_ccp_v_1.md`.
  - Structural claim:
    - "SDA protects semantic truthfulness."
    - "SFL shapes perceptual potency and symbolic aliveness."
  - Governance claim:
    - "SFL is anti-blandness, anti-deadness, anti-false-depth, and anti-misaligned influence."
- Read `lab/phase0_eval_card_scoring_model_v_1.md`.
  - Visible score language captured:
    - `Humanity`
    - `Presence`
    - `Trust`
    - `Memorability`
    - `Resonance`
    - `Signal`
    - `AI Slop Risk`
- Read `lab/ccp_biological_orchestration_model_v_1.md`.
  - Runtime-chain claim:
    - `DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation`
  - Runtime substrate claim:
    - DSPy can operate at runtime as typed orchestration substrate.

### 5. Existing FR Specs Read
- Read `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md`.
  - Existing threshold quote captured:
    - `export_eligible == true` only when `impact_score >= 70`, `conviction_score >= 70`, and `anti_centroid_charge >= 0.60`
  - Existing scorecard ownership confirmed:
    - `ReactionScoreCard` remains the primary CORE reaction scoring surface.
- Read `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`.
  - Ownership claim captured:
    - FR-27 "does not re-evaluate semantic coherence."
  - Human-congruence claim captured:
    - `human_congruence_score` is mandatory first-class dimension.
- Prompt referenced:
  - `docs/architecture/april_updates/FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy_Tech_Spec.md`
  - Result:
    - file not present in workspace at spec-writing time.
  - Consequence:
    - treat FR-35A as downstream scoring-taxonomy dependency and define a provisional alignment boundary instead of pretending the file exists.

### 6. Existing Backend References Read - Real Method Signatures
- Read `src/ccp/services/trait_scoring_engine.py`.
  - Signature captured:
    - `def score_all_traits(self) -> list[ScoredTrait]:`
- Read `src/ccp/services/dpa_engine.py`.
  - Signature captured:
    - `async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = "", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None) -> DPAResult:`
- Read `src/ccp/services/trivianar_engine_service.py`.
  - Signatures captured:
    - `def start_session(self, config: TriviaSessionConfig) -> TrivianarResult:`
    - `def score_response(self, question: TriviaQuestion, answer: str, elapsed_ms: int, game_mode: str = TriviaGameMode.COUNTDOWN.value, wager: int = 0, previous_responses: Optional[list[TriviaResponse]] = None) -> ScoringResult:`
    - `def compute_leaderboard(...)`
    - `def extract_cbcs_mapping(...)`
    - `def select_reaction(...)`

### 7. Existing Models Read
- Read `src/ccp/models/ca11_models.py`.
  - Relevant model surface captured:
    - `TriviaQuestion`
    - `TriviaResponse`
    - `LeaderboardEntry`
    - `ScoringResult`
    - `TrivianarResult`
    - `ResolvedPalette`

### 8. Existing Test Patterns Read
- Read `tests/integration/test_ca11_fr19_trivianar_engine.py`.
  - Confirmed class-per-AC organization, fixture builders, direct score assertions, and gate/leaderboard testing style.
- Read `tests/integration/test_ca11_fr15_dpa_engine.py`.
  - Confirmed async helper style and evidence-focused surface assertions.

### 9. Visible-Score Doctrine Confirmation
- Confirmed the visible score system is not a replacement for deeper metrics.
- Confirmed visible score language is meant to simplify explanation while preserving deeper internal scoring and evaluator structure.
- Therefore reaction benchmarking must align with visible card-language externally without flattening:
  - transcript structure
  - conviction metrics
  - anti-centroid logic
  - negative metrics
  - jury/social routing mechanics

---

## §1 Files Read

1. `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. `docs/prd/modules/PRD_06_Conscious_Reactions.md`
3. `docs/prd/modules/PRD_08_Conscious_Primitives.md`
4. `lab/subliminal_function_layer_for_ccp_v_1.md`
5. `lab/phase0_eval_card_scoring_model_v_1.md`
6. `lab/ccp_biological_orchestration_model_v_1.md`
7. `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md`
8. `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
9. `src/ccp/services/trait_scoring_engine.py`
10. `src/ccp/services/dpa_engine.py`
11. `src/ccp/services/trivianar_engine_service.py`
12. `src/ccp/models/ca11_models.py`
13. `tests/integration/test_ca11_fr19_trivianar_engine.py`
14. `tests/integration/test_ca11_fr15_dpa_engine.py`

Missing but referenced by prompt:
- `docs/architecture/april_updates/FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy_Tech_Spec.md`
  - not found in workspace at spec-writing time

---

## §2 Overview

### Problem
The existing CORE Reaction Engine spec already defines:

- topic TTL
- recording flow
- chunk streaming
- negative metrics
- earned export gates
- jury routing
- redemption

But it does not yet formally ingest the SFL-visible score language that now matters for human authority benchmarking:

- `Humanity`
- `Presence`
- `Trust`
- `Memorability`
- `Resonance`
- `Signal`
- `AI Slop Risk`

Without this update, the reaction system remains vulnerable to three distortions:

1. it can score reaction performance in a technically competent way while missing whether the take feels alive or synthetic
2. it can drift toward competitive point scoring or “who got more heat” instead of real human authority
3. it cannot align its feedback language with the same visible score system used by audit cards and downstream coaching surfaces

### Goal
Update the Core Reaction Engine so reaction scoring becomes:

- more human-first
- more presence-aware
- anti-slop aware
- aligned with the visible score vocabulary
- still grounded in the existing negative-metrics and earned-export logic

### Core Principle
Reaction scoring is **not**:

- generic engagement scoring
- like-count optimization
- dopamine formatting
- shallow competition mechanics

Reaction scoring **is**:

- human authority benchmarking under pressure
- biologically and perceptually informed speaking evaluation
- anti-centroid and anti-slop filtering
- a bridge from reaction performance into better speaking, better proof, and better public trust

### Scope
In scope:

- visible-score-aware reaction score summaries
- presence/resonance/signal weighting
- anti-slop detection in reaction scoring
- benchmark carryover aligned with card score language
- jury/social routing guardrails against vanity optimization
- updated score/result schemas for SFL interop

Out of scope:

- building the audit card UI itself
- replacing the original `ReactionScoreCard`
- reimplementing FR-27 inside CORE
- re-owning semantic truth from FR-22
- converting reactions into pure social media growth scoring

---

## §3.1 DEP-IDs

| DEP-ID | Name | Status | Purpose |
|---|---|---|---|
| `DEP-REA-005` | `ReactionScoreCard` | EXISTING | Core reaction result surface with biometric and commercial gates |
| `DEP-REA-SFL-051` | `ReactionPerceptualScore` | NEW | Typed perceptual scoring adjunct for reaction-local SFL-aligned evaluation |
| `DEP-REA-SFL-052` | `ReactionVisibleScoreSummary` | NEW | Visible score language mapped onto reaction performance in a human-readable form |
| `DEP-REA-SFL-053` | `ReactionPresenceSignal` | NEW | Specialized contract for conviction / charge / pacing / speaker-force interpretation |
| `DEP-REA-SFL-054` | `ReactionSlopRiskState` | NEW | Anti-slop state for centroid collapse, synthetic smoothness, and dead-polish risk |
| `DEP-REA-SFL-055` | `ReactionBenchmarkCarryover` | NEW | Cross-surface bridge linking reaction performance to visible score and benchmark language |
| `DEP-REA-SFL-056` | `ReactionPerceptualRoutingDecision` | NEW | Routing-level decision for publish, review, redemption, or coach intervention based on reaction + perceptual state |
| `DEP-REA-SFL-057` | `ReactionVisibleMetricEvidence` | NEW | Evidence packet supporting visible score translation without collapsing internal metrics |
| `DEP-SFL-027-01` | `PerceptualInfluenceEvaluator` | PLANNED / EXTERNAL | Optional upstream evaluator source when available |
| `DEP-REA-007` | `AudienceVoteRecord` | EXISTING | Social participation record that must not become vanity-optimization bait |

### DEP Relationship Rule
- `DEP-REA-005` remains the canonical reaction scorecard.
- `DEP-REA-SFL-*` contracts enrich it and translate it.
- These new contracts do not replace:
  - `impact_score`
  - `conviction_score`
  - `anti_centroid_charge`
  - `damage_index`
  - `compounding_forecast`

They sit beside those metrics and make the reaction engine more humanly intelligent.

---

## §3.2 Backend (>=4 files)

### Existing Backend Files Consumed

#### 1. `src/ccp/services/trait_scoring_engine.py`
Relevant signature:

```python
def score_all_traits(self) -> list[ScoredTrait]:
```

Use in this update:
- continue consuming evidence-backed speaking/authority traits
- support reaction-visible mappings, especially for:
  - conviction / embodied force
  - directness
  - emotional depth
  - polarizing clarity

#### 2. `src/ccp/services/dpa_engine.py`
Relevant signature:

```python
async def resolve(...) -> DPAResult:
```

Use in this update:
- preserve premium trust surface for reaction artifacts
- allow DPA surfaces to remain trust-enhancing without mistaking polish for human authority

#### 3. `src/ccp/services/trivianar_engine_service.py`
Relevant signatures:

```python
def start_session(self, config: TriviaSessionConfig) -> TrivianarResult:
def score_response(...) -> ScoringResult:
def compute_leaderboard(...)
def extract_cbcs_mapping(...)
def select_reaction(...)
```

Use in this update:
- legacy competitive patterns remain a reference for score events and low-friction participation
- but the reaction runtime must not inherit game-show psychology as its governing logic

#### 4. `src/ccp/models/ca11_models.py`
Relevant model surface:

- `TriviaQuestion`
- `TriviaResponse`
- `LeaderboardEntry`
- `ScoringResult`
- `TrivianarResult`
- `ResolvedPalette`

Use in this update:
- brownfield precedent for scoring results, vote state, and surface payload style
- not the final canonical home for advanced reaction-SFL models

### Brownfield Constraint
At spec-writing time:

- the original FR-ERA3-05-CORE implementation is still specification-first
- no SFL-aware reaction runtime file exists yet
- FR-27 runtime backend files are also not present yet

Therefore:

- this update must define the reaction-side contracts and interop points clearly
- but must not pretend a fully implemented perceptual evaluator already exists in code

### Rejection Rules
Reject any implementation that:

- replaces `ReactionScoreCard` with a shallow social score
- optimizes only for vote count or virality
- drops `Damage Index`, `Compounding Forecast`, or `anti_centroid_charge`
- treats DPA polish as proof of human authority
- lets leaderboard logic override human-first coaching logic

---

## §3.3 Reaction Score / Benchmark Contracts

### Contract Ownership Split

| Contract | Owner | Role |
|---|---|---|
| `ReactionScoreCard` | FR-ERA3-05-CORE | primary reaction scoring surface |
| `ReactionPerceptualScore` | FR-ERA3-05-CORE update | reaction-local perceptual adjunct |
| `ReactionVisibleScoreSummary` | FR-ERA3-05-CORE update | visible score translation layer |
| `ReactionBenchmarkCarryover` | FR-ERA3-05-CORE update | benchmark bridge to cards/audits/challenges |
| FR-27 full PI report | FR-ERA3-27 | optional upstream perceptual input when available |
| FR-35A scoring taxonomy | downstream dependency | future canonical score-family alignment source |

### Visible Score Translation Rule
The reaction engine must expose visible score language:

- `Humanity`
- `Presence`
- `Trust`
- `Memorability`
- `Resonance`
- `Signal`
- `AI Slop Risk`

But it must derive these from deeper reaction evidence such as:

- conviction density
- pacing
- hedging frequency
- anti-centroid charge
- transcript structure
- stance sharpness
- proof grounding
- acoustic force under pressure

### Reaction vs Generic Engagement Scoring
Reaction scoring must explicitly differ from:

#### Generic engagement scoring
Generic systems optimize for:
- hooks
- likes
- shares
- watch-time tricks
- controversy spikes

#### CORE reaction scoring
CORE reaction scoring optimizes for:
- human authority under pressure
- conviction without synthetic posturing
- stance clarity without dumb polarization
- memorability without fake depth
- trust without flattening
- resonance without sentimentality

### Benchmark Carryover Rule
`ReactionBenchmarkCarryover` must allow reactions to flow into:

- challenge invitations
- speaking accountability
- audit continuity
- future card-based comparison surfaces

without making the reaction engine responsible for rendering those surfaces.

### Anti-Slop Rule
Reaction scoring must detect at least these three reaction-specific failure classes:

1. **Centroid safety**
   - too balanced
   - too hedged
   - no real stance

2. **Synthetic force**
   - superficially strong but hollow delivery
   - over-smoothed rhetoric
   - performative authority

3. **Dead polish**
   - technically neat
   - socially acceptable
   - emotionally flat
   - no memorable pressure

---

## §3.4 Governance Constraints

### 1. Reaction-Feels-Human Rule
The final reaction benchmark must reward:

- lived pressure response
- human texture
- authentic force
- real judgment

It must not reward merely:

- clean phrasing
- safe professionalism
- generic persuasive formatting

### 2. Presence-Over-Flat-Engagement Rule
If a reaction gets attention because it is inflammatory but has weak `Presence`, weak `Trust`, or high `AI Slop Risk`,
the system must not treat it as a benchmark success.

### 3. No-Dead-Polish Rule
High production cleanliness or smooth transcript structure cannot compensate for:

- low conviction
- low signal
- low humanity
- high slop risk

### 4. SFL Subordinate-to-SDA Rule
If a reaction is charismatic but semantically corrupt:

- semantic truth still wins
- export and routing must remain constrained by FR-22 / anti-centroid / existing gates

### 5. Human-First-Competition Rule
Jury, leaderboard, and vote mechanics exist to:

- increase participation
- create proof pressure
- sharpen speaking

They do not exist to turn the platform into shallow spectacle or humiliation loops.

### 6. Visible-Score-Without-Flattening Rule
Visible score summaries must simplify explanation.
They must not erase deeper internals such as:

- `damage_index`
- `compounding_forecast`
- `anti_centroid_charge`
- acoustic and transcript evidence

### 7. Export Gate Preservation Rule
The existing earned export gate remains binding:

- `impact_score >= 70`
- `conviction_score >= 70`
- `anti_centroid_charge >= 0.60`

Perceptual strength may enrich interpretation, but it may not waive these gates.

---

## §3.5 Technical Decisions

### Decision 1 - Keep `ReactionScoreCard` as Primary
Do not replace `ReactionScoreCard`.

Reason:
- it already anchors:
  - biometric scores
  - commercial scores
  - export gates
  - redemption routing

### Decision 2 - Add Reaction-Local Visible Score Summary
Add `ReactionVisibleScoreSummary` as a translation layer.

Reason:
- aligns reactions with the audit/card language
- improves continuity with later coaching and proof surfaces

### Decision 3 - Make `Presence` First-Class
`Presence` gets its own contract: `ReactionPresenceSignal`.

Reason:
- reactions are primarily spoken-pressure events
- speaker force, conviction, pause architecture, and charge are central
- `Action` is downstream, but `Presence` is the felt cause

### Decision 4 - Add Reaction-Specific Slop State
Use `ReactionSlopRiskState`.

Reason:
- reaction surfaces are especially vulnerable to:
  - fake certainty
  - dopamine formatting
  - synthetic conflict
  - bland safe takes

### Decision 5 - Benchmark Carryover, Not Card Ownership
Use `ReactionBenchmarkCarryover`.

Reason:
- reactions should feed shared benchmark language
- but the card system stays outside CORE ownership

### Decision 6 - Jury Metrics Are Secondary
Votes and jury participation can influence visibility and progression,
but must not outrank:

- semantic integrity
- conviction
- trust
- presence
- anti-slop protection

### Decision 7 - Provisional FR-35A Alignment Adapter
Because the referenced FR-35A tech spec file is missing, this update must define a provisional visible-score alignment boundary rather than hard-coding absent taxonomy artifacts.

---

## §4 Plan

### Phase 1 - Model and Contract Layer
1. Add `ReactionPerceptualScore` model.
2. Add `ReactionVisibleMetricEvidence` model.
3. Add `ReactionVisibleScoreSummary` model.
4. Add `ReactionPresenceSignal` model.
5. Add `ReactionSlopRiskState` model.
6. Add `ReactionBenchmarkCarryover` model.

### Phase 2 - Scoring Derivation Layer
7. Extend `ReactionScoreAdapter` logic to derive visible-score-aligned outputs.
8. Add reaction-specific translation from conviction/pacing/hedging to `Presence`.
9. Add reaction-specific translation from proof/stance clarity to `Trust` and `Signal`.
10. Add anti-slop derivation from centroid collapse, hedging, and synthetic smoothness signals.
11. Add evidence-backed visible score rationale fields.

### Phase 3 - Routing and Governance Layer
12. Add `ReactionPerceptualRoutingDecision`.
13. Preserve earned export gate thresholds unchanged.
14. Add publish/review/redemption routing rules using perceptual adjuncts.
15. Add jury/leaderboard guardrails preventing vanity engagement from overriding quality.

### Phase 4 - Continuity / Carryover Layer
16. Add benchmark carryover mapping to challenge and accountability surfaces.
17. Add receipt fields for visible score summaries and slop risk states.
18. Add provisional alignment adapter for future FR-35A scoring taxonomy.

### Phase 5 - Testing
19. Add integration tests for visible score derivation.
20. Add tests for slop-risk-triggered redemption behavior.
21. Add tests ensuring high votes do not override low trust/high slop states.
22. Add tests for benchmark carryover continuity.

---

## §5 Schema (Pydantic v2, no Any)

```python
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ReactionVisibleScoreName(str, Enum):
    HUMANITY = "humanity"
    PRESENCE = "presence"
    TRUST = "trust"
    MEMORABILITY = "memorability"
    RESONANCE = "resonance"
    SIGNAL = "signal"
    AI_SLOP_RISK = "ai_slop_risk"


class ReactionPerceptualVerdict(str, Enum):
    STRONG = "strong"
    UNSTABLE = "unstable"
    WEAK = "weak"
    BLOCKING = "blocking"


class ReactionSlopClass(str, Enum):
    NONE = "none"
    CENTROID_SAFETY = "centroid_safety"
    SYNTHETIC_FORCE = "synthetic_force"
    DEAD_POLISH = "dead_polish"
    HOLLOW_HEAT = "hollow_heat"


class ReactionRouteAction(str, Enum):
    PASS_TO_EXPORT_GATE = "pass_to_export_gate"
    REVIEW_BEFORE_EXPORT = "review_before_export"
    ROUTE_TO_REDEMPTION = "route_to_redemption"
    COACHING_INTERVENTION = "coaching_intervention"
    JURY_ONLY_NO_PROMOTION = "jury_only_no_promotion"


class ReactionVisibleMetricEvidence(BaseModel):
    metric_id: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    source_signal: str = Field(..., min_length=1)
    source_value: float = Field(...)
    contribution: float = Field(..., ge=-1.0, le=1.0)


class ReactionPerceptualScore(BaseModel):
    score_name: ReactionVisibleScoreName = Field(...)
    score_0_99: int = Field(..., ge=0, le=99)
    verdict: ReactionPerceptualVerdict = Field(...)
    rationale: str = Field(..., min_length=1)
    evidence: list[ReactionVisibleMetricEvidence] = Field(default_factory=list)


class ReactionPresenceSignal(BaseModel):
    presence_score_0_99: int = Field(..., ge=0, le=99)
    conviction_density: float = Field(..., ge=0.0, le=100.0)
    pacing_score: float = Field(..., ge=0.0, le=100.0)
    pause_weight_score: float = Field(..., ge=0.0, le=1.0)
    stance_force_score: float = Field(..., ge=0.0, le=1.0)
    hedge_pressure_score: float = Field(..., ge=0.0, le=1.0)
    interpretation: str = Field(..., min_length=1)


class ReactionSlopRiskState(BaseModel):
    overall_risk_score_0_99: int = Field(..., ge=0, le=99)
    slop_class: ReactionSlopClass = Field(...)
    centroid_collapse_detected: bool = Field(default=False)
    synthetic_smoothness_detected: bool = Field(default=False)
    false_force_detected: bool = Field(default=False)
    dead_polish_detected: bool = Field(default=False)
    required_correction: str = Field(..., min_length=1)


class ReactionVisibleScoreSummary(BaseModel):
    humanity: ReactionPerceptualScore = Field(...)
    presence: ReactionPerceptualScore = Field(...)
    trust: ReactionPerceptualScore = Field(...)
    memorability: ReactionPerceptualScore = Field(...)
    resonance: ReactionPerceptualScore = Field(...)
    signal: ReactionPerceptualScore = Field(...)
    ai_slop_risk: ReactionPerceptualScore = Field(...)
    top_strengths: list[str] = Field(default_factory=list)
    top_weaknesses: list[str] = Field(default_factory=list)


class ReactionBenchmarkCarryover(BaseModel):
    artifact_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    reaction_mode: str = Field(..., min_length=1)
    visible_scores: ReactionVisibleScoreSummary = Field(...)
    presence_signal: ReactionPresenceSignal = Field(...)
    slop_risk_state: ReactionSlopRiskState = Field(...)
    challenge_readiness: bool = Field(...)
    speaker_course_recommended: bool = Field(...)
    accountability_followup_recommended: bool = Field(...)
    benchmark_headline: str = Field(..., min_length=1)


class ReactionPerceptualRoutingDecision(BaseModel):
    artifact_id: str = Field(..., min_length=1)
    route_action: ReactionRouteAction = Field(...)
    export_gate_eligible: bool = Field(...)
    jury_visibility_allowed: bool = Field(...)
    social_promotion_allowed: bool = Field(...)
    trigger_redemption: bool = Field(...)
    explanation: str = Field(..., min_length=1)
```

### Mandatory Translation Logic
- low `Humanity`:
  - generic language
  - no lived specificity
  - emotionally thin
- low `Presence`:
  - weak conviction
  - unstable pacing
  - hedging overload
  - flat speaker energy
- low `Trust`:
  - weak proof
  - overclaiming
  - unstable credibility
- low `Memorability`:
  - no anchor phrase
  - no sharp line
  - no lasting contrast
- low `Resonance`:
  - low felt consequence
  - emotionally flat
  - no subtext pressure
- low `Signal`:
  - average opinion
  - safe centroid stance
  - weak worldview signature
- high `AI Slop Risk`:
  - smooth but synthetic
  - safe but dead
  - forceful but fake

### Existing Gate Preservation
These perceptual adjuncts must never erase:

- `impact_score`
- `conviction_score`
- `anti_centroid_charge`
- `damage_index`
- `compounding_forecast`

---

## §6 Fallback

### Mode A - Full Reaction + Perceptual Adjunct Path
Inputs present:
- core reaction biometric snapshot
- transcript evidence
- visible score derivation inputs

Behavior:
- full visible-score summary
- slop-risk state
- benchmark carryover
- routing decision

### Mode B - Legacy Reaction Path Only
Inputs present:
- core reaction metrics only
- no visible-score derivation support

Behavior:
- preserve original scorecard and export-gate behavior
- no fake visible-score claims

### Mode C - Visible Summary Partial
Inputs present:
- enough signal for `Presence`, `Signal`, and `AI Slop Risk`
- insufficient detail for full resonance/humanity derivation

Behavior:
- partial visible summary allowed internally
- public-facing summary must lower confidence and avoid overclaiming

### Mode D - High Slop Risk Override
Inputs present:
- passing raw engagement/social momentum
- high slop risk

Behavior:
- social hype cannot auto-promote artifact
- route to review or redemption according to policy

### Hard Failure Conditions
Fail closed if:
- `artifact_id` missing
- core scorecard missing on a non-legacy path
- export gate attempted without required primary metrics
- reaction summary tries to publish visible-score pass with unresolved slop-risk block

---

## §7 Tasks

### Task 1 - Model Layer
- implement all §5 models in reaction model layer
- preserve Pydantic v2 style
- keep existing scorecard model intact

### Task 2 - Reaction Score Adapter Extension
- extend `ReactionScoreAdapter` to derive visible-score-aligned outputs
- preserve existing primary metric calculations
- keep evidence trace per visible score

### Task 3 - Presence Logic
- implement `ReactionPresenceSignal`
- derive from:
  - conviction density
  - pacing
  - pause behavior
  - hedging pressure
  - stance force

### Task 4 - Slop Logic
- implement `ReactionSlopRiskState`
- include:
  - centroid safety detection
  - synthetic force detection
  - dead polish detection
  - hollow heat detection

### Task 5 - Visible Score Translation
- map internal reaction evidence to:
  - `Humanity`
  - `Presence`
  - `Trust`
  - `Memorability`
  - `Resonance`
  - `Signal`
  - `AI Slop Risk`

### Task 6 - Routing Layer
- implement `ReactionPerceptualRoutingDecision`
- ensure high engagement cannot override poor human-authority state
- preserve earned export gate as final mechanical gate

### Task 7 - Benchmark Carryover
- emit `ReactionBenchmarkCarryover`
- support challenge and speaking-course continuity
- support future audit/card continuity without renderer ownership

### Task 8 - Tests
- create or extend integration tests for:
  - visible score derivation
  - slop-risk blocks
  - presence-aware routing
  - jury-vs-quality conflict
  - benchmark carryover continuity

---

## §8 Acceptance Criteria

### AC-05-SFL-1
When a reaction has strong raw activity but weak `Presence` and weak `Trust`,
then the reaction engine must not treat it as a benchmark success.

Failure example:
- a loud, chaotic take with shallow substance ranks as excellent because it attracted votes or felt heated.

### AC-05-SFL-2
When `AI Slop Risk` is high,
then the reaction engine must be able to route the artifact to review or redemption even if the take is technically clean.

Failure example:
- smooth but empty reactions keep publishing because they passed pacing alone.

### AC-05-SFL-3
When a reaction is high in `Signal` and `Presence` but fails export thresholds,
then the artifact still cannot become `export_eligible`.

Failure example:
- a charismatic but under-threshold take bypasses `impact_score >= 70` or `anti_centroid_charge >= 0.60`.

### AC-05-SFL-4
When a take is highly voted but has poor `Humanity` and elevated `AI Slop Risk`,
then jury participation must not automatically create public promotion status.

Failure example:
- vote count becomes the real ranking logic and reaction quality governance collapses.

### AC-05-SFL-5
When the reaction engine emits a visible score summary,
then it must preserve deeper internal metrics and not flatten them into one vanity score.

Failure example:
- `Damage Index`, `Compounding Forecast`, and `anti_centroid_charge` disappear from operational use.

### AC-05-SFL-6
When a weak reaction is routed to redemption,
then the perceptual adjunct must help explain whether the problem was:

- low `Presence`
- low `Signal`
- low `Trust`
- or high `AI Slop Risk`

Failure example:
- every failed reaction receives the same generic “be more confident” advice.

### AC-05-SFL-7
When visible score alignment data is missing,
then the engine must preserve legacy reaction scoring behavior without faking visible-score certainty.

Failure example:
- null or guessed visible scores are shown as if they were measured outputs.

---

## §9 Dependencies

### Upstream Required
- `PRD-06`
- `PRD-08`
- existing FR-ERA3-05-CORE mechanical gates

### Upstream Strongly Preferred
- `FR-ERA3-27`
  - perceptual evaluator spec exists
  - backend implementation files not present yet
- future / missing `FR-ERA3-35A`
  - scoring taxonomy file referenced by prompt is not present in workspace
  - this update therefore uses provisional visible-score alignment rather than canonical FR-35A artifacts

### Existing Brownfield Consumers
- `TraitScoringEngine`
- `DPAEngine`
- Telegram jury callback path
- future CORE reaction runtime implementation

### Downstream Consumers
- challenge escalation
- speaking/accountability continuity
- future audit board / card systems
- CMF export routing review

---

## §10 Testing

### Integration Test Files
Create or extend:

- `tests/integration/test_era3_fr05_core_reaction_engine_sfl.py`
- `tests/integration/test_era3_fr05_core_reaction_engine_routing.py`
- `tests/integration/test_era3_fr05_core_reaction_engine_benchmark_carryover.py`

### Required Test Groups

#### A. Contract Tests
- visible score summary serializes with all seven score families
- presence signal serializes with conviction/pacing/hedge evidence
- slop-risk state serializes with exact failure class

#### B. Routing Tests
- high slop risk can force review/redemption despite decent technical cleanliness
- high votes cannot override weak human-authority state
- export gate remains bound to existing thresholds

#### C. Translation Tests
- low conviction + high hedging lowers `Presence`
- safe average transcript lowers `Signal`
- over-smoothed confident transcript raises `AI Slop Risk`
- strong lived specificity lifts `Humanity`

#### D. Carryover Tests
- benchmark carryover marks speaker-course recommendation when reaction failures repeat
- accountability follow-up toggles correctly
- challenge-readiness does not trigger on weak trust/high slop combinations

#### E. Legacy Fallback Tests
- missing visible-score support preserves legacy scorecard
- no fake visible-score outputs are emitted in fallback mode

### Seed Test Scenarios

1. **Strong take, clean authority**
   - high conviction
   - high anti-centroid charge
   - strong `Presence`, `Signal`, `Trust`
   - expected export gate pass when core thresholds also pass

2. **Loud but hollow take**
   - heated delivery
   - weak proof
   - high synthetic force
   - expected high slop warning and non-promotional routing

3. **Balanced but boring centroid take**
   - low anti-centroid
   - weak signal
   - hedged language
   - expected redemption or coaching intervention

4. **Technically neat but dead polish**
   - stable pacing
   - smooth transcript
   - weak resonance and humanity
   - expected review or redemption

5. **High-vote but low-trust artifact**
   - jury engagement exists
   - trust weak
   - expected no automatic benchmark success

### Manual Validation Checklist
- verify a weak reaction does not get socially “rewarded” just because it created activity
- verify a strong reaction preserves existing export-gate logic
- verify reaction feedback language uses visible scores without flattening internals
- verify slop-risk states actually change routing behavior

---

**End of Spec**
