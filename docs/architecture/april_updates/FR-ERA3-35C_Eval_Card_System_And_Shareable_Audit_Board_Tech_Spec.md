# FR-ERA3-35C Eval Card System And Shareable Audit Board Tech Spec

## §1 Files Read

### 1.1 Prompt and Protocol
- `docs/architecture/april_updates/spec_prompts/P0_S03C_FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board.md`
- `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

### 1.2 Source PRDs
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
- `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

### 1.3 Mandatory Eval Source Set
- `lab/phase0_eval_card_scoring_model_v_1.md`
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/subliminal_function_layer_for_ccp_v_1.md`

### 1.4 Existing Backend and Presentation References
- `src/ccp/api/main.py`
- `src/ccp/services/scorecard_emitter.py`
- `src/ccp/services/dpa_engine.py`
- `src/ccp/models/score_viewer_models.py`
- `src/ccp/models/leadership_scorecard_models.py`
- `src/ccp/models/reaction_solo_models.py`
- `src/ccp/core/receipt_chain.py`

### 1.5 Existing Test Patterns
- `tests/integration/test_fr_era3_score_card_viewer.py`
- `tests/integration/test_era3_fr05a_solo_reaction_app_contracts.py`
- `tests/integration/test_era3_fr06_primitive_registry_api.py`

### 1.6 Pre-Work Evidence

#### Protocol evidence
- The protocol requires new specs to extend the existing backend: `"New specs EXTEND this — they don't reinvent it."`
- It also requires backend integration traceability and explicit testing strategy sections.

#### PRD-01 evidence
- PRD-01 says: `"The Conscious Coaching Platform is a human expression refinement ecosystem — not an AI content generation tool"`.
- PRD-01 also says the front-stage promise is: `"Become a better communicator, become harder to ignore, and turn your real voice into premium content and social proof."`
- This means card surfaces must feel like proof objects, not AI dashboards.

#### PRD-04 evidence
- PRD-04 says CCP should feel `"unusually human, clear, low-friction, and worth returning to."`
- It also says: `"The user should never have to understand the backend to feel the product quality."`
- The first-touch surface law includes:
  - `"one obvious action,"`
  - `"one meaningful output,"`
  - `"one emotionally satisfying reveal,"`
  - `"one clear next step."`

#### PRD-09 evidence
- PRD-09 says: `"free proof must feel real and fast"`.
- It defines the proof layer as visible but gated:
  - `"proof is visible, but activation, download, and usable ownership are gated."`
- It frames the commercial experience as:
  - `"delivery before brochure"`
  - `"benchmark before pitch"`
- It requires the first proof package to include:
  - audit
  - animated explainer audit
  - explainers
  - spread objects

#### Phase-0 score note evidence
- The card note says the visible surface must expose:
  - `"one overall score from 0-99"`
  - `"six main visible scores from 0-99"`
  - `"one negative warning score from 0-99"`
- It also says cards should feel like:
  - `"premium scouting cards"`
  - `"easy to screenshot"`
  - `"easy to share"`
- And every card should include:
  - `"large thumbnail image"`
  - `"overall score"`
  - `"card type"`
  - `"six visible scores"`

#### Fladlien evidence
- The note says: `"The Audit Must Sell Without Over-Explaining"`.
- It also defines the audit as part of a free proof deposit and first proof unlock sequence.
- This means the card system must be understandable at a glance and able to work inside both free proof and paid proof surfaces.

#### SFL evidence
- SFL says: `"SFL shapes perceptual potency and symbolic aliveness."`
- It also defines runtime artifacts such as:
  - `Perceptual Effect Metric`
  - `Influence Alignment Policy`
  - `PerceptualFailureReport`
- Card surfaces therefore must present perceptual results without collapsing into jargon-heavy internal artifact naming.

#### Existing backend signature evidence
- `ScorecardEmitter.emit(self, scorecard: LeadershipScorecard, raise_on_validation_failure: bool = True) -> tuple[LeadershipScorecard, list[str]]`
- `DPAEngine.resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = "", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None) -> DPAResult`
- `SoloReactionLaunchPayload(...)`
- `SoloScoreRevealPayload(...)`

#### Existing model/test evidence
- `ScoreCardViewerPayload` already separates:
  - data availability
  - theme
  - top insights
  - signal cards
  - production lock
- `SoloScoreRevealPayload` proves scoreboard/reveal payloads are already modeled as first-class view objects.
- `test_fr_era3_score_card_viewer.py` proves fallback honesty for visual score surfaces is already a required pattern.
- `test_era3_fr05a_solo_reaction_app_contracts.py` proves UI payloads are expected to be contract-tested, not hand-waved.

### 1.7 Dependency Reality Check
- `FR-ERA3-35A` and `FR-ERA3-35B` prompt files exist but their final tech specs are not yet in the workspace.
- `FR-ERA3-35` now exists and declares that it consumes card-system output.
- Therefore this card-system spec must define a provisional contract adapter boundary for missing upstream weighting/registry layers without inventing new score names.

---

## §2 Overview

### 2.1 Problem
Phase-0 needs a visible audit surface that is:
- easy to understand
- attractive enough to share
- serious enough to trust
- simple enough to consume inside Telegram / AFFiNE flows
- strong enough to act as a marketing object

Generic dashboards fail because they:
- overwhelm the user
- expose too much internal jargon
- kill emotional clarity
- look like software, not proof

### 2.2 Solution
Create a canonical `Eval Card System` and `Shareable Audit Board` that:
- consumes canonical evals and benchmark bundles
- projects them into simple visible scores
- renders a large-thumbnail-first card surface
- supports board layouts for:
  - single-card detail
  - audit spread
  - before/after comparison
  - screenshot-ready sharing

### 2.3 Design Philosophy
The card system should feel closer to:
- premium scouting cards
- FIFA Ultimate Team familiarity
- premium social proof objects

Not:
- enterprise BI dashboards
- pseudo-game fluff
- tarot-style mystique cards

### 2.4 Product Role
This layer serves three jobs simultaneously:
- internal operator review surface
- prospect-facing audit reveal surface
- shareable proof/marketing object

### 2.5 Non-Goal
This layer does not:
- define eval registry contents
- define benchmark weighting logic
- decide diagnosis
- decide prescription
- decide proof-of-prescription

Those belong to:
- `FR-ERA3-35A`
- `FR-ERA3-35B`
- `FR-ERA3-35`

This layer owns presentation contracts and board composition.

---

## §3.1 DEP-IDs

| DEP-ID | Name | Owned By | Purpose |
|---|---|---|---|
| `DEP-ERA3-35C-001` | Eval Card | FR-ERA3-35C | canonical rendered score card object |
| `DEP-ERA3-35C-002` | Eval Card Face | FR-ERA3-35C | visible front-face content |
| `DEP-ERA3-35C-003` | Eval Card Stat Line | FR-ERA3-35C | one visible stat row |
| `DEP-ERA3-35C-004` | Eval Card Board | FR-ERA3-35C | multi-card board payload |
| `DEP-ERA3-35C-005` | Eval Board Layout | FR-ERA3-35C | board layout instructions |
| `DEP-ERA3-35C-006` | Card Thumbnail Asset | FR-ERA3-35C | normalized thumbnail metadata |
| `DEP-ERA3-35C-007` | Card Verdict Block | FR-ERA3-35C | one-line verdict and one-line fix |
| `DEP-ERA3-35C-008` | Card Theme Projection | FR-ERA3-35C | DPA-projected visual theme |
| `DEP-ERA3-35C-009` | Shareable Audit Board Render Request | FR-ERA3-35C | renderer-facing board request |

### 3.1A Upstream Relationships

| Upstream Spec | Relationship | Notes |
|---|---|---|
| `FR-ERA3-35A` | consumes | visible score vocabulary and scoring-law references |
| `FR-ERA3-35B` | consumes | card weighting and card-role bundle logic |
| `FR-ERA3-35` | provides inputs to | diagnostics, verdicts, fix directions, proof links |
| `FR-ERA3-12` | hands off to | final rendered surfaces for PDF/video assets |

### 3.1B Downstream Relationships
- `FR-ERA3-35` should be able to emit payloads that this card system can consume.
- `FR-ERA3-39` and `FR-ERA3-40` should be able to use boards inside operator and batch-review surfaces.

---

## §3.2 Backend

### 3.2.1 Existing Backend Integration
This spec should extend:
- `src/ccp/models/score_viewer_models.py`
  - viewer-payload precedent
- `src/ccp/services/scorecard_emitter.py`
  - report emission precedent
- `src/ccp/services/dpa_engine.py`
  - card theming and brand-safe palette projection
- `src/ccp/models/reaction_solo_models.py`
  - score-reveal and startapp surface payload precedent
- `src/ccp/core/receipt_chain.py`
  - render lineage and board generation receipts

### 3.2.2 Existing Signatures To Mirror
- `ScorecardEmitter.emit(...) -> tuple[LeadershipScorecard, list[str]]`
- `DPAEngine.resolve(...) -> DPAResult`

### 3.2.3 Existing Model Patterns To Reuse
- `ScoreCardViewerPayload`
- `TraitInsightCard`
- `Fr61SignalDeltaCard`
- `ScoreViewerTheme`
- `SoloScoreRevealPayload`

These models show that CCP already separates:
- internal score computation
- viewer-facing payload
- themed projection

### 3.2.4 Recommended New Files
- `src/ccp/models/phase0_eval_card_models.py`
- `src/ccp/services/eval_card_projection_service.py`
- `src/ccp/services/eval_board_assembly_service.py`
- `src/ccp/api/phase0_eval_cards.py`
- `tests/integration/test_era3_fr35c_eval_card_system.py`
- `tests/models/test_phase0_eval_card_models.py`
- `tests/services/test_eval_board_assembly_service.py`

### 3.2.5 Rendering and Theme Integration
The card system should not hard-code flat styling.

It should consume theme projection from DPA:
- background colors
- accent colors
- text colors
- brand-safe contrast logic

### 3.2.6 Existing Test Pattern Alignment
- contract-test payload surfaces
- test graceful fallback when data is partial
- keep board APIs deterministic

---

## §3.3 Card / board artifact classes

### 3.3.1 Artifact Roles

#### Card artifacts
- single visual score objects
- used in PDF, audit board, Telegram previews, explainer-video scene composition

#### Board artifacts
- group cards into intentional spreads
- used for comparison, audit overview, and screenshot-ready proof

#### Theme artifacts
- ensure cards stay premium and brand-consistent

### 3.3.2 Card Surface Law
Every card must expose:
- big thumbnail
- overall score `0-99`
- visible scores `0-99`
- card type / role
- one-line verdict
- one-line fix or direction

### 3.3.3 Visible Score Vocabulary
The visible stat vocabulary is fixed:
- `Humanity`
- `Presence`
- `Trust`
- `Memorability`
- `Resonance`
- `Signal`
- `AI Slop Risk`

No other top-level visible stat names are allowed on the card face.

### 3.3.4 Card Roles
The system should support at minimum:
- `audit_primary`
- `audit_secondary`
- `before_snapshot`
- `after_snapshot`
- `marketing_preview`
- `operator_review`

### 3.3.5 Board Types
The board system must support:
- `single_card_detail`
- `audit_spread`
- `before_after_comparison`
- `shareable_summary`

### 3.3.6 Board Experience Role
Boards are not just grids.
They are structured reveal surfaces that should:
- lower cognitive load
- increase confidence
- make contrast obvious
- feel screenshot-worthy

### 3.3.7 Card Logic Boundaries
This layer may:
- display a visible score
- label a role
- style a verdict block
- place cards on a board

This layer may not:
- invent new score families
- change score values
- recalculate overall score
- reinterpret diagnosis independently of the audit engine

### 3.3.8 Presentation Law
The card surface should stay simple enough that a coach can understand it without learning CCP jargon, while still preserving canonical eval truth underneath.

---

## §3.4 Governance Constraints

### 3.4.1 Easy-To-Understand Surface Rule
The card must read immediately without requiring product training.

### 3.4.2 No-Jargon-On-Card Rule
Do not expose internal labels like:
- semantic integrity carry-through
- perceptual threshold modulation
- anti-centroid integrity

Those may exist underneath but not as top-level card stats.

### 3.4.3 Canonical-Evals-Underneath Rule
The card is a projection layer.
It must consume canonical evals rather than inventing scores at render time.

### 3.4.4 Shareable-Audit Rule
The board must be screenshot-ready and legible when exported or shared.

### 3.4.5 Marketing-Object-Without-Lying Rule
The card can be visually exciting, but it must remain grounded in real score inputs and real verdict logic.

### 3.4.6 Thumbnail-First Rule
The content image or key frame is the first anchor.
The user should see what is being judged before reading every number.

### 3.4.7 Human-First Surface Rule
The surface must feel like proof of human signal, not software telemetry.

### 3.4.8 Theme-Safety Rule
Brand application must preserve legibility and seriousness.
No decorative theme choice can reduce score clarity.

### 3.4.9 No-New-Score Rule
Even if internal metrics grow, the public card vocabulary stays fixed unless the upstream score note is formally updated.

### 3.4.10 Honest Partiality Rule
If data is partial, the card/board must honestly mark it instead of pretending complete audit coverage.

---

## §3.5 Technical Decisions

### 3.5.1 Decision: Fixed Visible Stat Vocabulary
Rationale:
- keeps recognition fast
- supports memorability
- prevents UI drift

### 3.5.2 Decision: Big Thumbnail Over Dense Diagnostics
Rationale:
- makes the judged artifact concrete
- supports screenshot sharing
- keeps the card emotionally legible

### 3.5.3 Decision: Card Face Separate From Card Model
Rationale:
- keeps renderer logic modular
- allows multiple board surfaces while preserving one canonical card object

### 3.5.4 Decision: Board Layout Is Typed
Rationale:
- supports deterministic rendering
- keeps audit spread composition reusable
- avoids ad-hoc frontend-only layout logic

### 3.5.5 Decision: DPA Theme Projection Is Consumed
Rationale:
- keeps cards aligned with CCP brand architecture
- avoids raw hard-coded colors becoming a parallel styling system

### 3.5.6 Decision: Overall Score Comes From Upstream
Rationale:
- prevents the presentation layer from recalculating or mutating truth

### 3.5.7 Decision: Verdict Block Is Mandatory
Rationale:
- scores without interpretation are less useful
- interpretation without brevity breaks shareability

### 3.5.8 Decision: Before/After Board Is First-Class
Rationale:
- progression is one of the strongest commercial proof mechanisms
- before/after contrast sells improvement faster than abstract theory

### 3.5.9 Decision: Partial Data Must Be Renderable
Rationale:
- Phase-0 will often operate on incomplete data
- a degraded but honest board is better than no visible output

### 3.5.10 Decision: Provisional Upstream Boundary Is Declared
Rationale:
- `35A/B` are not yet built
- card projection must therefore support provisional adapters while remaining strict about visible labels

---

## §4 Plan

### Phase 1: Core Model Contracts
1. Define `CardThumbnailAsset`.
2. Define `EvalCardStatLine`.
3. Define `CardVerdictBlock`.
4. Define `EvalCardFace`.
5. Define `EvalCard`.
6. Define `EvalBoardLayout`.
7. Define `EvalCardBoard`.

### Phase 2: Projection Service
8. Create `eval_card_projection_service.py`.
9. Implement visible score projection consumption from upstream report.
10. Implement overall score pass-through from upstream score bundle.
11. Implement card role mapping.
12. Implement DPA theme projection integration.

### Phase 3: Board Assembly
13. Create `eval_board_assembly_service.py`.
14. Implement single-card detail assembly.
15. Implement audit spread assembly.
16. Implement before/after comparison assembly.
17. Implement shareable summary board assembly.

### Phase 4: API and Export Readiness
18. Add `phase0_eval_cards.py` router.
19. Add endpoint for single-card payload retrieval.
20. Add endpoint for board payload retrieval.
21. Add screenshot/export render request payload support.

### Phase 5: Validation and Testing
22. Add model validation tests.
23. Add board layout tests.
24. Add theme fallback tests.
25. Add partial-data honesty tests.
26. Add integration tests for viewer/read API patterns.

---

## §5 Schema

### 5.1 Enum: `VisibleCardStatKey`
```python
class VisibleCardStatKey(str, Enum):
    humanity = "humanity"
    presence = "presence"
    trust = "trust"
    memorability = "memorability"
    resonance = "resonance"
    signal = "signal"
    ai_slop_risk = "ai_slop_risk"
```

### 5.2 Enum: `EvalCardRole`
```python
class EvalCardRole(str, Enum):
    audit_primary = "audit_primary"
    audit_secondary = "audit_secondary"
    before_snapshot = "before_snapshot"
    after_snapshot = "after_snapshot"
    marketing_preview = "marketing_preview"
    operator_review = "operator_review"
```

### 5.3 Enum: `EvalBoardKind`
```python
class EvalBoardKind(str, Enum):
    single_card_detail = "single_card_detail"
    audit_spread = "audit_spread"
    before_after_comparison = "before_after_comparison"
    shareable_summary = "shareable_summary"
```

### 5.4 Enum: `CardScoreBand`
```python
class CardScoreBand(str, Enum):
    weak = "weak"
    developing = "developing"
    strong = "strong"
    elite = "elite"
```

### 5.5 Enum: `BoardDensity`
```python
class BoardDensity(str, Enum):
    compact = "compact"
    standard = "standard"
    spacious = "spacious"
```

### 5.6 Model: `CardThumbnailAsset`
```python
class CardThumbnailAsset(BaseModel):
    asset_id: str = Field(..., min_length=1)
    storage_uri: str = Field(..., min_length=1)
    width: int = Field(..., ge=1)
    height: int = Field(..., ge=1)
    alt_text: str = Field(..., min_length=1)
    source_kind: str = Field(..., min_length=1)
```

### 5.7 Model: `EvalCardStatLine`
```python
class EvalCardStatLine(BaseModel):
    key: VisibleCardStatKey = Field(...)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=0, le=99)
    band: CardScoreBand = Field(...)
```

### 5.8 Model: `CardVerdictBlock`
```python
class CardVerdictBlock(BaseModel):
    verdict_line: str = Field(..., min_length=1)
    fix_line: str = Field(..., min_length=1)
    confidence_note: str | None = Field(default=None)
```

### 5.9 Model: `CardThemeProjection`
```python
class CardThemeProjection(BaseModel):
    background_primary: str = Field(..., min_length=1)
    background_secondary: str = Field(..., min_length=1)
    accent: str = Field(..., min_length=1)
    text_primary: str = Field(..., min_length=1)
    brand_hue_used: bool = Field(default=False)
```

### 5.10 Model: `EvalCardFace`
```python
class EvalCardFace(BaseModel):
    title: str = Field(..., min_length=1)
    subtitle: str | None = Field(default=None)
    thumbnail: CardThumbnailAsset = Field(...)
    overall_score: int = Field(..., ge=0, le=99)
    role: EvalCardRole = Field(...)
    card_type_label: str = Field(..., min_length=1)
    visible_stats: list[EvalCardStatLine] = Field(..., min_length=7, max_length=7)
    verdict: CardVerdictBlock = Field(...)
```

### 5.11 Model: `EvalCard`
```python
class EvalCard(BaseModel):
    card_id: str = Field(..., min_length=1)
    report_id: str = Field(..., min_length=1)
    face: EvalCardFace = Field(...)
    theme: CardThemeProjection = Field(...)
    source_content_type: str = Field(..., min_length=1)
    archetype_hint: str | None = Field(default=None)
    generated_at: str = Field(..., min_length=1)
    provisional_upstream_contract: bool = Field(default=False)
```

### 5.12 Model: `EvalBoardLayout`
```python
class EvalBoardLayout(BaseModel):
    board_kind: EvalBoardKind = Field(...)
    density: BoardDensity = Field(default=BoardDensity.standard)
    columns: int = Field(..., ge=1, le=6)
    featured_card_id: str | None = Field(default=None)
    card_order: list[str] = Field(default_factory=list)
    screenshot_safe: bool = Field(default=True)
```

### 5.13 Model: `EvalCardBoard`
```python
class EvalCardBoard(BaseModel):
    board_id: str = Field(..., min_length=1)
    report_id: str = Field(..., min_length=1)
    board_kind: EvalBoardKind = Field(...)
    title: str = Field(..., min_length=1)
    subtitle: str | None = Field(default=None)
    cards: list[EvalCard] = Field(default_factory=list)
    layout: EvalBoardLayout = Field(...)
    summary_line: str = Field(..., min_length=1)
    share_caption: str | None = Field(default=None)
```

### 5.14 Model: `ShareableAuditBoardRenderRequest`
```python
class ShareableAuditBoardRenderRequest(BaseModel):
    board: EvalCardBoard = Field(...)
    output_format: str = Field(..., min_length=1)
    target_surface: str = Field(..., min_length=1)
    watermark_enabled: bool = Field(default=True)
```

### 5.15 Schema Rules
- `visible_stats` must contain exactly:
  - Humanity
  - Presence
  - Trust
  - Memorability
  - Resonance
  - Signal
  - AI Slop Risk
- `overall_score` must be passed in from upstream scoring logic and never recomputed in this layer.
- `thumbnail` is mandatory for every visible card.
- `verdict` is mandatory for every visible card.
- boards must declare layout explicitly.
- board layouts must remain screenshot-safe.

---

## §6 Fallback

### 6.1 Missing Upstream Eval Registry Fallback
If `35A` is not implemented:
- use provisional visible-score vocabulary from `lab/phase0_eval_card_scoring_model_v_1.md`
- set `provisional_upstream_contract = true`

### 6.2 Missing Weighting Bundle Fallback
If `35B` is not implemented:
- accept upstream overall score and visible stat scores as already-resolved inputs
- do not invent weighting at the card layer

### 6.3 Missing Thumbnail Fallback
If no strong thumbnail is available:
- use a fallback frame or placeholder asset
- mark `confidence_note`
- keep the card renderable

### 6.4 Missing Theme Projection Fallback
If DPA theme resolution fails:
- use a neutral default theme
- preserve contrast and readability
- log fallback state

### 6.5 Partial Data Fallback
If some supporting audit details are missing:
- keep the visible card renderable
- show verdict/fix using available data
- add confidence note rather than blank space

### 6.6 Failure-Closed Law
If required visible stats are missing or renamed, card creation must fail validation rather than silently outputing malformed score surfaces.

---

## §7 Tasks

1. Create `phase0_eval_card_models.py`.
2. Add `VisibleCardStatKey` enum.
3. Add `EvalCardRole` enum.
4. Add `EvalBoardKind` enum.
5. Add `CardThumbnailAsset`.
6. Add `EvalCardStatLine`.
7. Add `CardVerdictBlock`.
8. Add `CardThemeProjection`.
9. Add `EvalCardFace`.
10. Add `EvalCard`.
11. Add `EvalBoardLayout`.
12. Add `EvalCardBoard`.
13. Add `ShareableAuditBoardRenderRequest`.
14. Create `eval_card_projection_service.py`.
15. Implement card projection from audit report inputs.
16. Implement visible-stat validation.
17. Integrate DPA theme projection.
18. Create `eval_board_assembly_service.py`.
19. Implement single-card detail board.
20. Implement audit spread board.
21. Implement before/after comparison board.
22. Implement shareable summary board.
23. Add `phase0_eval_cards.py` API router.
24. Add board retrieval endpoint.
25. Add shareable render request endpoint.
26. Add receipt chain logging.
27. Add model tests.
28. Add board assembly tests.
29. Add fallback honesty tests.
30. Add integration tests.

---

## §8 AC

### AC-1 Visible Score Vocabulary Lock
Cards expose exactly the seven allowed visible stats.

Failure example:
- a card face renders `Distinctiveness` or `Charisma` instead of the canonical labels.

### AC-2 Thumbnail-First Card
Every card includes a large thumbnail asset.

Failure example:
- board renders only number tiles with no content image.

### AC-3 Overall Score Exposure
Every card exposes one overall score from `0-99`.

Failure example:
- card hides the overall score and only shows micro-stats.

### AC-4 Verdict Block Presence
Every card includes:
- one-line verdict
- one-line fix or direction

Failure example:
- card is visually polished but has no interpretable takeaway.

### AC-5 Card Role Support
The system supports role labels such as:
- audit primary
- before snapshot
- after snapshot
- marketing preview

Failure example:
- board cannot distinguish diagnostic card from comparison card.

### AC-6 Board Type Support
The system supports:
- single-card detail
- audit board spread
- before/after comparison
- shareable summary

Failure example:
- only single card render exists and no multi-card board can be assembled.

### AC-7 Screenshot-Safe Layout
Boards are intentionally laid out for sharing and screenshot capture.

Failure example:
- text is clipped, card density is unreadable, or layout depends on scroll.

### AC-8 No Render-Time Score Invention
The presentation layer never recalculates or invents score values.

Failure example:
- frontend normalizes numbers differently from upstream report values.

### AC-9 Theme Safety
Themed cards remain legible and brand-safe.

Failure example:
- accent color destroys contrast on score numbers.

### AC-10 Honest Partiality
Partial data renders with explicit confidence note or fallback indication.

Failure example:
- card appears complete despite missing thumbnail or missing upstream confidence.

### AC-11 Audit/Marketing Dual Use
The same canonical card object can be used in both internal audit delivery and shareable outward-facing surfaces without changing score semantics.

Failure example:
- marketing export uses edited or “boosted” numbers not present in internal audit output.

---

## §9 Dependencies

### 9.1 Hard Dependencies
- `PRD-01`
- `PRD-04`
- `PRD-09`
- `lab/phase0_eval_card_scoring_model_v_1.md`

### 9.2 Upstream Phase-0 Dependencies
- future `FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy`
- future `FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles`
- `FR-ERA3-35_Audit_Intelligence_Engine`

### 9.3 Existing Backend Dependencies
- `src/ccp/services/dpa_engine.py`
- `src/ccp/services/scorecard_emitter.py`
- `src/ccp/core/receipt_chain.py`
- FastAPI mount via `src/ccp/api/main.py`

### 9.4 Downstream Rendering Dependencies
- `FR-ERA3-12` for media realization and PDF/video board surfaces

### 9.5 Test Dependencies
- payload/contract test pattern from `test_era3_fr05a_solo_reaction_app_contracts.py`
- viewer-surface fallback pattern from `test_fr_era3_score_card_viewer.py`

---

## §10 Testing

### 10.1 Integration Test File
- `tests/integration/test_era3_fr35c_eval_card_system.py`

### 10.2 Required Integration Cases
- build single `EvalCard` from valid upstream input
- build `audit_spread` board from multiple cards
- build `before_after_comparison` board
- build shareable summary board
- preserve visible score values exactly
- DPA theme projection applied
- fallback theme used when DPA unavailable

### 10.3 Model Test File
- `tests/models/test_phase0_eval_card_models.py`

### 10.4 Required Model Cases
- reject unknown visible stat keys
- reject out-of-range scores
- reject missing thumbnail
- reject board with invalid layout
- reject card with missing verdict block

### 10.5 Service Test File
- `tests/services/test_eval_board_assembly_service.py`

### 10.6 Required Service Cases
- single-card detail layout assembly
- audit spread layout assembly
- before/after ordering
- screenshot-safe layout defaults
- provisional upstream contract marking

### 10.7 Failure Tests
- theme resolution failure
- upstream score vocabulary mismatch
- duplicate stats
- incomplete card with no confidence note
- board creation with zero cards

### 10.8 Regression Tests
- visible score vocabulary stays fixed
- overall score pass-through preserved
- verdict lines remain short enough for card surfaces
- board output remains usable as both audit and marketing object

### 10.9 Acceptance Threshold
This spec is complete only if the system can produce:
- a clear card object
- a clear board object
- a screenshot-ready share surface
- and a presentation layer that remains simple while staying grounded in canonical CCP scoring truth.
