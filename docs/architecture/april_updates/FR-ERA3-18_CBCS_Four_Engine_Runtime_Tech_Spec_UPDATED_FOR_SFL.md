# FR-ERA3-18 CBCS Four Engine Runtime Tech Spec Updated for SFL

## Pre-Work Log

### 1. Protocol Read
- Read `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`.
- Binding protocol rule captured: Era 3 specs must extend the existing FastAPI, Pydantic, service, pipeline, and agent stack rather than inventing a parallel runtime.
- Binding protocol rule captured: the tech spec must include explicit backend integration, explicit brownfield constraints, and `tests/integration/` alignment.

### 2. PRD Proof - CBCS Runtime Purpose
- Read `docs/prd/modules/PRD_05_CBCS_Law28.md`.
- Exact quote establishing runtime purpose:
  - "CBCS should be understood as a universal self-coding transformation engine."
- Exact quote establishing engine decomposition:
  - "For implementation clarity, PRD-05 treats CBCS as four interacting runtime engines: Diagnostic Engine, Ritual Engine, Evidence Engine, Relationship Engine."
- Exact quote establishing the daily runtime loop:
  - "state check -> route selection -> daily prompt or drill -> user recording or reflection -> transcription and scoring -> context update -> next-step feedback -> continuity memory update"

### 3. PRD Proof - Primitive Boundary
- Read `docs/prd/modules/PRD_08_Conscious_Primitives.md`.
- Exact quote establishing primitive role:
  - "Primitives are the active conscious faculties that shape how meaning is experienced, directed, and transformed."
- Exact quote establishing system-wide reuse:
  - "Every content pipeline — CCF scripts, CMF visuals, CBCS coaching notes, Conscious Reactions scoring, V²WS webinar slides — draws from this registry..."
- Exact quote establishing that primitives are not the deepest truth layer:
  - "SDA is a sibling intelligence stack. Primitives are not the deepest ontology; they are the active force layer that shapes experience and directed transformation."

### 4. SFL Source Set Read - Structural Claims
- Read `lab/subliminal_function_layer_for_ccp_v_1.md`.
  - Structural claim captured:
    - "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness."
- Read `lab/phase0_eval_card_scoring_model_v_1.md`.
  - Structural claim captured:
    - visible score set = `Humanity`, `Presence`, `Trust`, `Memorability`, `Resonance`, `Signal`
  - warning score captured:
    - `AI Slop Risk`
- Read `lab/ccp_biological_orchestration_model_v_1.md`.
  - Structural claim captured:
    - runtime chain = `DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation`
  - CBCS implication captured:
    - downstream systems should consume delivery/effect outputs rather than try to recompute truth ownership.

### 5. Existing FR Specs Read
- Read `docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec.md`.
  - Relevant responsibility captured:
    - the previous runtime already centralizes user-safe delivery through a Relationship Engine rather than exposing raw diagnostic output directly.
- Read `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`.
  - Relevant responsibility captured:
    - FR-27 owns perceptual effect evaluation and "does not re-evaluate semantic coherence" when FR-22 / DI already holds semantic ownership.
- Attempted read: `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
  - Result:
    - file not present in the workspace at spec-writing time.
  - Consequence:
    - this update spec must declare FR-ERA3-35 as a downstream dependency and define a provisional intake contract instead of pretending a built audit-engine spec already exists.

### 6. Existing Backend References Read - Real Method Signatures
- Read `src/ccp/services/identity_anchor_protocol.py`.
  - Signature captured:
    - `def evaluate(self, sequence_text: str) -> ReactanceGateResult:`
- Read `src/ccp/services/scorecard_emitter.py`.
  - Signatures captured:
    - `def assemble_scorecard(...) -> LeadershipScorecard:`
    - `def validate(self, scorecard: LeadershipScorecard) -> list[str]:`
    - `def emit(self, scorecard: LeadershipScorecard, raise_on_validation_failure: bool = True) -> tuple[LeadershipScorecard, list[str]]:`
- Read `src/ccp/services/dynamic_journaling_engine.py`.
  - Signature captured:
    - `def generate(`
- Read `src/ccp/services/trait_scoring_engine.py`.
  - Signature captured:
    - `def score_all_traits(self) -> list[ScoredTrait]:`
- Read `src/ccp/services/change_talk_vault.py`.
  - Signatures captured:
    - `def extract(... ) -> list[ChangeTalkArchiveRow]:`
    - `def query_vault(... ) -> VaultQueryResult:`
- Read `src/ccp/services/learning_path_builder.py`.
  - Signature captured:
    - `def classify(... ) -> LearningPathEntry:`
- Read `src/ccp/services/ritual_scheduler.py`.
  - Signature captured:
    - `async def generate_ritual(... ) -> str:`
- Read `src/ccp/services/engagement_feedback.py`.
  - Signatures captured:
    - `def ingest(self, metrics: EngagementMetrics) -> EngagementMetrics:`
    - `def get_resonance_markers(self) -> list[dict]:`

### 7. Existing Models Read
- Read `src/ccp/models/cbcs_models.py`.
  - Confirmed existing CBCS model style: strict Pydantic models, enum-heavy contracts, threshold constants, and coach-boundary fields.
- Read `src/ccp/models/leadership_scorecard_models.py`.
  - Confirmed existing score/evidence pattern:
    - `ScoredTrait`
    - `TraitEvidence`
    - history-driven progression and evidence-backed scoring.

### 8. Existing Test Patterns Read
- Read `tests/integration/test_cbcs09_habit_architecture.py`.
  - Relevant pattern captured:
    - runtime behavior is asserted through verdict-bearing models and receipt-side effects, not only string outputs.
- Read `tests/integration/test_fr7_leadership_scorecard.py`.
  - Relevant pattern captured:
    - integration tests validate exact error codes, exact gating behavior, and evidence-presence rules.

### 9. Biological / Runtime Doctrine Confirmation
- Read `lab/ccp_biological_orchestration_model_v_1.md` in relation to CBCS.
- Confirmed runtime placement:
  - primitives belong to the force layer
  - SFL belongs to the delivery layer
  - visible score carryover and perceptual effect summaries are phenotype/evaluation outputs
  - CBCS must consume those outputs rather than restating ontology, primitive activation law, or evaluator ownership locally.

---

## §1 Files Read

1. `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. `docs/prd/modules/PRD_05_CBCS_Law28.md`
3. `docs/prd/modules/PRD_08_Conscious_Primitives.md`
4. `lab/subliminal_function_layer_for_ccp_v_1.md`
5. `lab/phase0_eval_card_scoring_model_v_1.md`
6. `lab/ccp_biological_orchestration_model_v_1.md`
7. `docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec.md`
8. `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
9. `src/ccp/models/cbcs_models.py`
10. `src/ccp/models/leadership_scorecard_models.py`
11. `src/ccp/services/identity_anchor_protocol.py`
12. `src/ccp/services/scorecard_emitter.py`
13. `src/ccp/services/dynamic_journaling_engine.py`
14. `src/ccp/services/trait_scoring_engine.py`
15. `src/ccp/services/change_talk_vault.py`
16. `src/ccp/services/learning_path_builder.py`
17. `src/ccp/services/ritual_scheduler.py`
18. `src/ccp/services/engagement_feedback.py`
19. `tests/integration/test_cbcs09_habit_architecture.py`
20. `tests/integration/test_fr7_leadership_scorecard.py`

Missing but referenced by prompt:
- `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
  - not found at spec-writing time
  - treated below as a downstream dependency with a provisional intake boundary.

---

## §2 Overview

### Problem
The existing CBCS runtime already honors the four-engine conceptual split from PRD-05, but it is not yet SFL-aware. It can process evidence, route drills, and issue accountability prompts, yet it does not formally ingest:

- visible score families
- card-oriented audit outputs
- perceptual weakness / strength signals
- anti-slop warnings
- audit-to-coaching prescription continuity

This creates four failure modes:

1. CBCS guidance can remain semantically correct but perceptually tone-deaf.
2. Voice-note and accountability guidance can miss concrete presence/humanity/trust deficits already known upstream.
3. Audit outputs and coaching loops can drift apart into separate products.
4. CBCS can accidentally sound synthetic or over-smoothed even when the upstream audit stack already diagnosed that exact risk.

### Goal
Update the CBCS Four Engine Runtime so it consumes SFL and audit-layer outputs intelligently, without turning CBCS into:

- a rendering engine
- a replacement evaluator
- a duplicate audit engine
- a semantic-truth owner

Instead, CBCS becomes the coaching/runtime consumer of:

- `PerceptualEffectSummary`
- `VisibleScoreCarryover`
- audit prescriptions
- perceptual evaluator findings
- card-based score surfaces

### Runtime Principle
CBCS sits downstream of:

- SDA truth ownership
- primitive force activation
- SFL perceptual delivery shaping
- perceptual evaluation
- audit card synthesis

CBCS therefore owns:

- recommendation quality
- speaking guidance
- accountability prescriptions
- live reaction coaching continuation
- relationship-safe reframing

CBCS does **not** own:

- ontology selection
- primitive registry truth
- SFL family resolution
- perceptual scoring computation
- card rendering itself

### Scope
In scope:

- updated four-engine runtime contracts
- SFL/evaluator/audit input contracts
- visible score carryover
- perceptual-aware coaching recommendations
- voice-note guidance and accountability prescription models
- human-first reframe requirements

Out of scope:

- rebuilding FR-27 inside CBCS
- computing cards inside CBCS
- creating the PDF audit surface
- creating the audit explainer video surface
- implementing FR-ERA3-35 directly in this spec

---

## §3.1 DEP-IDs

| DEP-ID | Name | Status | Purpose |
|---|---|---|---|
| `DEP-CBCS-SFL-501` | CBCS Perceptual Intake Envelope | NEW | Canonical inbound packet carrying visible scores, perceptual effects, audit links, and source references |
| `DEP-CBCS-SFL-502` | Perceptual Effect Summary | NEW | Compact effect-level summary consumed by Diagnostic, Ritual, and Relationship engines |
| `DEP-CBCS-SFL-503` | Visible Score Carryover | NEW | Canonical normalized carryover of `Humanity`, `Presence`, `Trust`, `Memorability`, `Resonance`, `Signal`, and `AI Slop Risk` |
| `DEP-CBCS-SFL-504` | CBCS Perceptual Recommendation | NEW | Engine-safe recommendation object derived from visible scores and effect signals |
| `DEP-CBCS-SFL-505` | Voice Note Perceptual Guidance | NEW | Runtime contract for human-first voice-note coaching guidance |
| `DEP-CBCS-SFL-506` | Accountability Perceptual Prescription | NEW | Accountability and ritual mutation plan derived from perceptual weaknesses/strengths |
| `DEP-CBCS-SFL-507` | Audit Coaching Continuity Link | NEW | Traceable bridge from audit outputs into CBCS coaching follow-up |
| `DEP-CBCS-SFL-508` | Relationship Reframe Surface | NEW | Final user-safe coaching surface enriched by perceptual findings without sounding synthetic |
| `DEP-CBCS-SFL-509` | Perceptual Source Reference | NEW | Typed reference to FR-27 or future FR-35 source artifacts |
| `DEP-CBCS-SFL-510` | Card Evidence Snapshot | NEW | Lightweight card/board snapshot reference for coaching continuity without rendering duplication |
| `DEP-ENG-026` | Leadership Scorecard | EXISTING | Evidence and long-range pattern source already emitted by scorecard runtime |
| `DEP-CBCS-402` | CBCS Evidence Packet | EXISTING | Existing evidence-layer packet that now gains perceptual adjuncts rather than being replaced |

### DEP Relationship Rule
- `DEP-CBCS-SFL-501` wraps but does not replace `DEP-CBCS-402`.
- `DEP-CBCS-SFL-503` may be computed only by upstream audit/evaluator owners.
- `DEP-CBCS-SFL-504` through `506` are **CBCS-owned derived contracts**, not upstream evaluator artifacts.
- `DEP-CBCS-SFL-508` is the only user-facing delivery surface from this update path.

---

## §3.2 Backend (>=4 files)

### Existing Backend Files Consumed

#### 1. `src/ccp/services/change_talk_vault.py`
Relevant signatures:

```python
def extract(...) -> list[ChangeTalkArchiveRow]:
def query_vault(...) -> VaultQueryResult:
```

Use in this update:
- keep motivation / commitment evidence in the CBCS Evidence Engine
- combine motivational evidence with perceptual weakness summaries
- avoid prescribing high-exposure rituals when commitment evidence is weak and `Presence` is low

#### 2. `src/ccp/services/trait_scoring_engine.py`
Relevant signature:

```python
def score_all_traits(self) -> list[ScoredTrait]:
```

Use in this update:
- continue treating score-backed traits as evidence inputs
- do not convert FR7 leadership trait scoring into visible score ownership
- allow Diagnostic Engine mapping such as low embodied confidence trait support for low `Presence`

#### 3. `src/ccp/services/scorecard_emitter.py`
Relevant signatures:

```python
def assemble_scorecard(...) -> LeadershipScorecard:
def validate(self, scorecard: LeadershipScorecard) -> list[str]:
def emit(self, scorecard: LeadershipScorecard, raise_on_validation_failure: bool = True) -> tuple[LeadershipScorecard, list[str]]:
```

Use in this update:
- leadership scorecard artifacts may be cited as longitudinal evidence
- CBCS may consume emitted scorecards or their summaries
- CBCS must not mutate FR7 emission rules or revalidate scorecards using a separate hidden standard

#### 4. `src/ccp/services/dynamic_journaling_engine.py`
Relevant signature:

```python
def generate(
```

Use in this update:
- journaling fallback is a Ritual Engine target when live-speaking load should temporarily decrease
- journaling prompts must be informed by perceptual deficits without parroting card jargon

#### 5. `src/ccp/services/learning_path_builder.py`
Relevant signature:

```python
def classify(...) -> LearningPathEntry:
```

Use in this update:
- route perceptual prescriptions into content/learning pathways
- maintain continuity between diagnosed perceptual weakness and subsequent learning assets

#### 6. `src/ccp/services/ritual_scheduler.py`
Relevant signature:

```python
async def generate_ritual(...) -> str:
```

Use in this update:
- Ritual Engine uses this to materialize message delivery
- Relationship Engine must constrain the prompt framing inputs so the generated ritual does not collapse into generic bot coaching tone

#### 7. `src/ccp/services/engagement_feedback.py`
Relevant signatures:

```python
def ingest(self, metrics: EngagementMetrics) -> EngagementMetrics:
def get_resonance_markers(self) -> list[dict]:
```

Use in this update:
- engagement feedback remains real-world outcome evidence
- resonance markers can reinforce strengths for `Signal`, `Memorability`, and `Resonance`
- low-performing outputs may support accountability shifts, but never replace semantic or perceptual truth

#### 8. `src/ccp/services/identity_anchor_protocol.py`
Relevant signature:

```python
def evaluate(self, sequence_text: str) -> ReactanceGateResult:
```

Use in this update:
- Relationship Engine may use reactance-gating as a guard on final coaching phrasing
- no CBCS final message may knowingly push a user into bot-like pressure or misaligned authority tone

### Existing Models Consumed
- `src/ccp/models/cbcs_models.py`
  - used as the home for new or adjacent CBCS runtime models if no stronger module split is needed
- `src/ccp/models/leadership_scorecard_models.py`
  - evidence-backed scoring pattern reused as style precedent

### Brownfield Integration Rule
This update must extend:

- existing CBCS services
- existing Pydantic model style
- existing receipt-chain mutation logging
- existing coaching boundary fields

This update must not introduce:

- a second hidden scoring framework inside CBCS
- duplicated perceptual evaluators
- a new card-rendering subsystem inside CBCS
- a separate coaching microservice stack outside current `src/ccp/services/`

---

## §3.3 Report / Recommendation Contracts

### Contract Ownership Split

| Contract | Owner | CBCS Role |
|---|---|---|
| `DirectionalIntegrityReport` | FR-22 | consume only when present |
| `PerceptualInfluenceEvaluationReport` | FR-27 | consume only, never recompute |
| `AuditSummary` / future FR-35 contract | FR-35 | consume only, provisional interface until built |
| `VisibleScoreCarryover` | FR-35 or upstream adapter | consume and propagate |
| `CbcsPerceptualRecommendation` | FR-18 | derive locally |
| `VoiceNotePerceptualGuidance` | FR-18 | derive locally |
| `AccountabilityPerceptualPrescription` | FR-18 | derive locally |

### Required Inbound Contracts
CBCS must accept one of two inbound paths:

1. direct evaluator path
   - FR-27 output present
   - visible score carryover present
   - optional card snapshot present

2. audit path
   - future FR-35 audit output present
   - visible score carryover present
   - optional card / board references present

### Provisional FR-35 Boundary
Because `FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md` is not built yet, this spec defines a provisional intake boundary named:

- `AuditIntelligenceSummaryInput`

This provisional boundary exists only so FR-18 can be implemented without pretending FR-35 is already canonical.

When FR-35 lands:
- the provisional boundary must be replaced or adapter-mapped
- field semantics must remain backward-compatible where possible
- CBCS must not silently change coaching behavior due to renamed audit fields

### Required Outbound Contracts
CBCS must emit:

- `CbcsPerceptualRecommendation`
- `VoiceNotePerceptualGuidance`
- `AccountabilityPerceptualPrescription`
- `RelationshipFramedCoachingMessage`
- `CbcsPerceptualRuntimeReceipt`

### Report Consumption Rule
CBCS may read:

- overall perceptual warnings
- visible score deltas
- primary weaknesses
- primary strengths
- card evidence snapshot references
- improvement prescriptions

CBCS may not read and then reinterpret:

- raw SFL family resolution as if it owned the family selector
- semantic integrity scores as if it owned truth verification
- audit card rendering data as a design surface
- evaluator confidence fields as an excuse to run its own parallel scoring

---

## §3.4 Governance Constraints

### 1. Human-First Coaching Rule
All user-facing CBCS outputs must sound like:

- grounded coaching
- specific human guidance
- contextual support

They must not sound like:

- dashboard narration
- robotic score recitation
- gamified humiliation
- generic AI encouragement

### 2. Voice-Feels-Alive Rule
If `AI Slop Risk` is elevated, the Relationship Engine and Ritual Engine must actively reduce:

- over-smoothed phrasing
- motivational filler
- ungrounded certainty
- dead-perfect summary language

### 3. No-Synthetic-Coach-Tone Rule
The final message may never simply say:

- "Your Presence score is 42"
- "Increase your resonance by 18 points"
- "Your AI Slop Risk is high, please be more authentic"

Instead it must translate score findings into lived coaching language.

### 4. SFL Subordinate-to-SDA Rule
If a perceptual recommendation would improve charisma but conflict with semantic truth or directional integrity:

- semantic truth wins
- directional integrity wins
- CBCS must decline the stronger-perception shortcut

### 5. Recommendation-From-Effects Rule
CBCS recommendations must derive from:

- visible score families
- effect summaries
- linked audit prescriptions
- evidence signals

They must not be improvised from general intuition alone when structured packets are available.

### 6. No Local Full-Stack Recompute Rule
CBCS must not rerun:

- full visible score generation
- full perceptual evaluator logic
- full audit diagnosis logic
- card composition logic

It may only derive coaching actions from provided outputs.

### 7. Relationship Intercept Rule
All downgrade-sensitive outputs must pass through the Relationship Engine.
Examples:

- lower-intensity speaking assignment
- journaling fallback
- request for more raw A-roll
- advice to reduce polish and increase lived signal

### 8. Card Awareness Without Card Ownership Rule
CBCS may cite the existence of:

- a low-scoring card cluster
- a strong card surface
- an audit board pattern

But CBCS must not act as the renderer or design owner of those surfaces.

---

## §3.5 Technical Decisions

### Decision 1 - Add a Perceptual Intake Envelope
Adopt `CbcsPerceptualIntakeEnvelope` as the single runtime handoff object from evaluator/audit surfaces into CBCS.

Reason:
- avoids loose dict passing
- makes FR-27 / FR-35 interop testable
- supports partial data fallback

### Decision 2 - Visible Scores Are First-Class Carryover
The visible score set is explicitly embedded:

- `Humanity`
- `Presence`
- `Trust`
- `Memorability`
- `Resonance`
- `Signal`
- `AI Slop Risk`

Reason:
- these are now the clearest coaching bridge from audit to CBCS
- they are human-readable enough to drive explanation but structured enough to drive routing

### Decision 3 - Separate Effect Summary from Coaching Recommendation
`PerceptualEffectSummary` describes what upstream found.
`CbcsPerceptualRecommendation` describes what CBCS should do about it.

Reason:
- preserves ownership boundaries
- avoids evaluator/coaching contract collapse

### Decision 4 - Voice Note Guidance Is a First-Class Artifact
`VoiceNotePerceptualGuidance` is not a string blob.
It is its own typed contract.

Reason:
- speaking quality is one of the main ways CBCS acts on these findings
- it needs traceable fields for review and testing

### Decision 5 - Accountability Prescription Is Distinct from Ritual Text
`AccountabilityPerceptualPrescription` describes:

- target behavior
- drill intensity
- repetition strategy
- improvement path

It is not the final message text.

Reason:
- preserves separation between planning and relationship-safe delivery

### Decision 6 - Provisional FR-35 Adapter
Implement an adapter layer now for future FR-35 audit inputs.

Reason:
- unblocks FR-18 implementation
- avoids hard-coding nonexistent schema assumptions directly into the runtime

### Decision 7 - Receipt-First Traceability
Every perceptual-aware CBCS decision must log:

- source contract ids
- visible score snapshot
- chosen recommendation class
- relationship reframe decision
- fallback mode if triggered

Reason:
- required for debugging batch coaching behavior
- required for future DSPy / calibration work

---

## §4 Plan

### Phase 1 - Model and Contract Layer
1. Create `VisibleScoreCarryover` Pydantic model.
2. Create `PerceptualEffectSummary` Pydantic model.
3. Create `PerceptualSourceReference` Pydantic model.
4. Create `CardEvidenceSnapshot` Pydantic model.
5. Create provisional `AuditIntelligenceSummaryInput` Pydantic model.
6. Create `CbcsPerceptualIntakeEnvelope` Pydantic model.

### Phase 2 - Engine Derivation Layer
7. Add `CbcsPerceptualRecommendation` derivation service.
8. Add `VoiceNotePerceptualGuidance` derivation service.
9. Add `AccountabilityPerceptualPrescription` derivation service.
10. Add mapping rules from visible score thresholds to coaching intents.
11. Add mapping rules from elevated `AI Slop Risk` to anti-synthetic coaching actions.

### Phase 3 - Four Engine Runtime Integration
12. Update Evidence Engine to attach perceptual intake adjuncts without taking ownership.
13. Update Diagnostic Engine to merge evidence signals with effect summaries.
14. Update Ritual Engine to choose voice-note, journaling, accountability, or reaction tasks using perceptual-aware routing.
15. Update Relationship Engine to translate score/effect findings into human-first language.
16. Add reactance / synthetic-tone safeguards before final message release.

### Phase 4 - Fallback and Interop Layer
17. Add FR-27 direct-consumption path.
18. Add provisional FR-35 adapter path.
19. Add partial-data fallback path when only visible scores are available.
20. Add no-perceptual-data fallback path that preserves legacy CBCS behavior.

### Phase 5 - Testing and Receipts
21. Add integration tests for perceptual intake consumption.
22. Add failure tests for forbidden local recompute behavior.
23. Add downgrade intercept tests with low `Presence` and low commitment evidence.
24. Add tests for human-first translation of visible-score findings.
25. Add receipt assertions for recommendation and relationship reframe steps.

---

## §5 Schema (Pydantic v2, no Any)

```python
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VisibleScoreName(str, Enum):
    HUMANITY = "humanity"
    PRESENCE = "presence"
    TRUST = "trust"
    MEMORABILITY = "memorability"
    RESONANCE = "resonance"
    SIGNAL = "signal"
    AI_SLOP_RISK = "ai_slop_risk"


class PerceptualSeverity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CoachingSurfaceType(str, Enum):
    VOICE_NOTE = "voice_note"
    ACCOUNTABILITY_MESSAGE = "accountability_message"
    LIVE_REACTION_PROMPT = "live_reaction_prompt"
    JOURNALING_PROMPT = "journaling_prompt"
    RELATIONSHIP_REFRAME = "relationship_reframe"


class RecommendationClass(str, Enum):
    REINFORCE = "reinforce"
    REPAIR = "repair"
    SLOW_DOWN = "slow_down"
    SHARPEN = "sharpen"
    HUMANIZE = "humanize"
    DECOMPRESS = "decompress"
    PROOF_GROUND = "proof_ground"


class SourceSystem(str, Enum):
    FR27 = "fr_era3_27"
    FR35 = "fr_era3_35"
    LEGACY_CBCS = "legacy_cbcs"


class PerceptualSourceReference(BaseModel):
    source_system: SourceSystem = Field(...)
    source_contract_id: str = Field(..., min_length=1)
    source_artifact_id: str = Field(..., min_length=1)
    source_version: str = Field(..., min_length=1)
    generated_at_utc: str = Field(..., min_length=1)


class ScoreBand(BaseModel):
    score_0_99: int = Field(..., ge=0, le=99)
    severity: PerceptualSeverity = Field(...)
    rationale: str = Field(..., min_length=1)


class VisibleScoreCarryover(BaseModel):
    humanity: ScoreBand = Field(...)
    presence: ScoreBand = Field(...)
    trust: ScoreBand = Field(...)
    memorability: ScoreBand = Field(...)
    resonance: ScoreBand = Field(...)
    signal: ScoreBand = Field(...)
    ai_slop_risk: ScoreBand = Field(...)


class PerceptualWeaknessSignal(BaseModel):
    signal_id: str = Field(..., min_length=1)
    score_name: VisibleScoreName = Field(...)
    severity: PerceptualSeverity = Field(...)
    label: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    coaching_implication: str = Field(..., min_length=1)


class PerceptualStrengthSignal(BaseModel):
    signal_id: str = Field(..., min_length=1)
    score_name: VisibleScoreName = Field(...)
    severity: PerceptualSeverity = Field(...)
    label: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    preservation_note: str = Field(..., min_length=1)


class PerceptualEffectSummary(BaseModel):
    summary_id: str = Field(..., min_length=1)
    primary_weaknesses: list[PerceptualWeaknessSignal] = Field(default_factory=list)
    primary_strengths: list[PerceptualStrengthSignal] = Field(default_factory=list)
    anti_slop_warning_active: bool = Field(...)
    synthetic_tone_risk_active: bool = Field(...)
    recommendation_hint: str = Field(..., min_length=1)


class CardEvidenceSnapshot(BaseModel):
    board_id: str = Field(..., min_length=1)
    card_ids: list[str] = Field(default_factory=list)
    thumbnail_asset_ids: list[str] = Field(default_factory=list)
    primary_card_labels: list[str] = Field(default_factory=list)
    review_url: Optional[str] = Field(default=None)


class AuditPrescriptionItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    target_score: VisibleScoreName = Field(...)
    plain_language_problem: str = Field(..., min_length=1)
    plain_language_fix: str = Field(..., min_length=1)
    urgency: PerceptualSeverity = Field(...)


class AuditIntelligenceSummaryInput(BaseModel):
    audit_id: str = Field(..., min_length=1)
    summary_headline: str = Field(..., min_length=1)
    visible_scores: VisibleScoreCarryover = Field(...)
    effect_summary: PerceptualEffectSummary = Field(...)
    prescription_items: list[AuditPrescriptionItem] = Field(default_factory=list)
    card_snapshot: Optional[CardEvidenceSnapshot] = Field(default=None)
    source_reference: PerceptualSourceReference = Field(...)


class CbcsPerceptualIntakeEnvelope(BaseModel):
    envelope_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    visible_scores: VisibleScoreCarryover = Field(...)
    effect_summary: PerceptualEffectSummary = Field(...)
    source_reference: PerceptualSourceReference = Field(...)
    card_snapshot: Optional[CardEvidenceSnapshot] = Field(default=None)
    audit_prescriptions: list[AuditPrescriptionItem] = Field(default_factory=list)
    relationship_context_note: Optional[str] = Field(default=None)


class CbcsPerceptualRecommendation(BaseModel):
    recommendation_id: str = Field(..., min_length=1)
    recommendation_class: RecommendationClass = Field(...)
    target_surface: CoachingSurfaceType = Field(...)
    primary_score_target: VisibleScoreName = Field(...)
    plain_language_goal: str = Field(..., min_length=1)
    recommended_behavior: str = Field(..., min_length=1)
    prohibited_behavior: str = Field(..., min_length=1)
    explanation_for_operator: str = Field(..., min_length=1)


class VoiceNotePerceptualGuidance(BaseModel):
    guidance_id: str = Field(..., min_length=1)
    focus_score: VisibleScoreName = Field(...)
    target_duration_seconds: int = Field(..., ge=10, le=600)
    delivery_instruction: str = Field(..., min_length=1)
    pacing_instruction: str = Field(..., min_length=1)
    proof_instruction: str = Field(..., min_length=1)
    anti_slop_instruction: str = Field(..., min_length=1)
    example_prompt: str = Field(..., min_length=1)


class AccountabilityPerceptualPrescription(BaseModel):
    prescription_id: str = Field(..., min_length=1)
    focus_scores: list[VisibleScoreName] = Field(default_factory=list)
    accountability_task: str = Field(..., min_length=1)
    repetition_window_days: int = Field(..., ge=1, le=30)
    review_signal: str = Field(..., min_length=1)
    escalation_condition: str = Field(..., min_length=1)
    downgrade_sensitive: bool = Field(...)


class RelationshipFramedCoachingMessage(BaseModel):
    message_id: str = Field(..., min_length=1)
    target_surface: CoachingSurfaceType = Field(...)
    safe_headline: str = Field(..., min_length=1)
    safe_body: str = Field(..., min_length=1)
    long_loop_reference: str = Field(..., min_length=1)
    score_translation_note: str = Field(..., min_length=1)
    mentions_cards: bool = Field(...)


class CbcsPerceptualRuntimeReceipt(BaseModel):
    receipt_id: str = Field(..., min_length=1)
    envelope_id: str = Field(..., min_length=1)
    recommendation_id: str = Field(..., min_length=1)
    relationship_message_id: str = Field(..., min_length=1)
    fallback_mode: Optional[str] = Field(default=None)
    source_contract_id: str = Field(..., min_length=1)
```

### Score Interpretation Standard
- `0-24`: severe failure band
- `25-44`: weak band
- `45-64`: unstable / transitional band
- `65-79`: strong band
- `80-99`: high-confidence strength band

### Mandatory Score Translation Logic
- low `Humanity` must map to more lived examples, more process exposure, or less over-smoothed phrasing
- low `Presence` must map to conviction, pacing, breath, pause, or firmer stance work
- low `Trust` must map to proof grounding, congruence, specificity, or claim-calibration work
- low `Memorability` must map to phrase compression, stronger contrast, or stronger point architecture
- low `Resonance` must map to emotional specificity, subtext, or human consequence
- low `Signal` must map to sharper worldview, opinion, boundary, or niche clarity
- high `AI Slop Risk` must map to de-smoothing, de-templating, rawness, and anti-generic correction

---

## §6 Fallback

### Fallback Mode A - Full Intake Present
Inputs present:
- visible scores
- effect summary
- source reference
- optional card snapshot
- optional audit prescriptions

Behavior:
- full perceptual-aware recommendation path

### Fallback Mode B - Evaluator Present, No Audit Prescriptions
Inputs present:
- visible scores
- effect summary
- source reference from FR-27

Behavior:
- derive recommendations only from visible scores + effect summary
- no audit continuity language that requires absent prescription items

### Fallback Mode C - Audit Present, Missing Card Snapshot
Inputs present:
- visible scores
- effect summary
- audit prescriptions

Behavior:
- CBCS continues normally
- card mentions disabled
- receipt marks `card_snapshot_missing`

### Fallback Mode D - Visible Scores Only
Inputs present:
- `VisibleScoreCarryover` only

Behavior:
- derive coarse coaching guidance from visible scores alone
- Relationship Engine must avoid overclaiming confidence
- no deep cause language allowed

### Fallback Mode E - No Perceptual Inputs
Inputs present:
- legacy CBCS evidence only

Behavior:
- preserve previous CBCS runtime behavior
- receipt marks `legacy_cbcs_only`
- no score-family-specific language allowed

### Hard Failure Conditions
Fail closed if:
- `coach_id` or `client_id` missing
- visible score packet malformed
- source reference missing on a non-legacy path
- relationship surface requested without relationship reframe pass

---

## §7 Tasks

### Task 1 - Add Intake Models
- implement all §5 models in CBCS model layer
- keep coach/client ids explicit on intake boundaries
- keep enum-backed score names

### Task 2 - Add Upstream Adapter Layer
- create adapter for FR-27 output -> `CbcsPerceptualIntakeEnvelope`
- create provisional adapter for future FR-35 audit output -> `CbcsPerceptualIntakeEnvelope`
- ensure adapter failure is explicit and receipted

### Task 3 - Extend Evidence Engine
- attach perceptual intake to existing evidence pass
- preserve legacy evidence fields
- never mutate upstream perceptual score values locally

### Task 4 - Extend Diagnostic Engine
- merge evidence-derived coaching context with perceptual effect summaries
- produce `CbcsPerceptualRecommendation`
- explicitly support live reaction, voice note, journaling, and accountability surfaces

### Task 5 - Extend Ritual Engine
- emit `VoiceNotePerceptualGuidance`
- emit `AccountabilityPerceptualPrescription`
- support reduced-intensity journaling fallback
- support stronger proof-grounding assignments when `Trust` is low

### Task 6 - Extend Relationship Engine
- convert score/effect findings into human-first language
- block card-jargon recitation
- mention card board only when helpful and present
- run reactance/synthetic-tone check before delivery

### Task 7 - Add Receipt Logging
- log source contract ids
- log score snapshot
- log chosen recommendation class
- log fallback mode
- log final relationship intercept result

### Task 8 - Update Integration Tests
- add direct FR-27 intake tests
- add provisional FR-35 adapter tests
- add visible-scores-only fallback tests
- add anti-synthetic-tone tests
- add downgrade intercept tests

---

## §8 Acceptance Criteria

### AC-18-SFL-1
When CBCS receives a perceptual intake envelope with low `Presence` and high `AI Slop Risk`,
then it must emit:

- a `VoiceNotePerceptualGuidance`
- an `AccountabilityPerceptualPrescription`
- and a relationship-safe final message

without rerunning the full perceptual evaluator locally.

Failure example:
- CBCS recomputes its own alternative `Presence` score or asks the model to "judge confidence again" from scratch.

### AC-18-SFL-2
When upstream visible scores show low `Trust`,
then CBCS must convert that into a proof-grounding or congruence recommendation rather than generic motivation.

Failure example:
- the user receives "keep going, you’ve got this" with no advice about proof, specificity, or claim calibration.

### AC-18-SFL-3
When a card snapshot is present,
then CBCS may reference the diagnosed pattern in plain language but must not become a card renderer or score reader.

Failure example:
- the final message says "Card 7 is red and Card 12 is weak in resonance."

### AC-18-SFL-4
When only visible scores are present and no effect summary is available,
then CBCS must enter visible-scores-only fallback and lower explanatory confidence.

Failure example:
- CBCS claims precise root causes that were never supplied by upstream evaluation.

### AC-18-SFL-5
When FR-35 is absent from the build chain,
then CBCS implementation remains unblocked through the provisional audit-summary adapter and explicit dependency declaration.

Failure example:
- the engineer must guess a nonexistent FR-35 schema to continue implementation.

### AC-18-SFL-6
When a recommendation implies lower exposure or slower progression,
then the Relationship Engine must contextualize it against long-loop growth and preserve dignity.

Failure example:
- the final message says the user is regressing or should "do an easier task because they are weak."

### AC-18-SFL-7
When `AI Slop Risk` is elevated,
then final coaching language must reduce generic polish and increase grounded humanness.

Failure example:
- the final message becomes even more templated, symmetrical, and coach-bot-like than before.

### AC-18-SFL-8
When `Humanity` and `Resonance` are already strong,
then CBCS must preserve those strengths instead of flattening them in the name of safer coaching.

Failure example:
- the ritual text strips out all specificity and turns a vivid speaking pattern into generic accountability prose.

---

## §9 Dependencies

### Upstream Required
- `FR-ERA3-22`
  - directional integrity / semantic ownership
- `FR-ERA3-25`
  - SFL taxonomy and function library
- `FR-ERA3-26`
  - SFL query and profile service
- `FR-ERA3-27`
  - perceptual influence evaluator
- `FR-ERA3-28`
  - perceptual failure corpus and contrast harness

### Upstream Strongly Preferred
- `FR-ERA3-35A`
  - eval registry and scoring taxonomy
- `FR-ERA3-35B`
  - benchmark profiles and weighting bundles
- `FR-ERA3-35C`
  - card system and audit board

### Downstream / Not Yet Built at Spec Time
- `FR-ERA3-35`
  - Audit Intelligence Engine tech spec file not yet present in workspace
  - this spec therefore uses a provisional intake interface to avoid blocking FR-18 update work

### Parallel Existing Systems Consumed
- PRD-05 CBCS services
- FR7 leadership scorecard artifacts
- engagement feedback loop
- learning path routing
- identity anchor reactance gate

---

## §10 Testing

### Test File Strategy
Add or extend:

- `tests/integration/test_fr_era3_18_cbcs_sfl_runtime.py`
- and, where appropriate, adjacent CBCS runtime tests

### Required Test Cases

1. `test_cbcs_consumes_fr27_perceptual_intake_without_local_recompute`
   - assert recommendation produced
   - assert no secondary evaluator call path

2. `test_cbcs_visible_scores_only_fallback_reduces_explanatory_confidence`
   - visible scores present
   - effect summary absent
   - output remains valid and receipted

3. `test_low_presence_and_high_slop_emit_voice_note_guidance_and_relationship_reframe`
   - ensures both planning and relationship outputs are generated

4. `test_low_trust_maps_to_proof_grounding_not_generic_encouragement`
   - assert recommendation class = `PROOF_GROUND`

5. `test_card_snapshot_presence_does_not_turn_message_into_card_jargon`
   - assert final text contains no card-id style references

6. `test_missing_source_reference_fails_closed_on_non_legacy_path`
   - malformed intake should fail

7. `test_legacy_cbcs_only_mode_preserves_backward_compatibility`
   - no perceptual inputs
   - runtime still functions through existing path

8. `test_relationship_engine_preserves_dignity_on_downgrade_sensitive_prescription`
   - lower-intensity recommendation
   - final message must include long-loop framing

9. `test_high_humanity_strength_is_preserved_not_flattened`
   - strong existing humanity should be reinforced, not scrubbed

10. `test_receipt_contains_source_contract_and_fallback_mode`
   - receipt assertions for tracing

### Test Governance Rules
- assert exact fallback mode strings
- assert exact recommendation class enums
- assert exact visible score names when referenced internally
- assert no direct user-facing score dump strings are emitted
- assert coach/client boundary fields are always preserved

### Manual Validation Checklist
- inspect at least one generated low-presence coaching message
- inspect at least one high-slop anti-smoothing recommendation
- inspect one visible-scores-only fallback output
- inspect one downgrade-sensitive accountability message

---

## Build Notes and Future Integration

- When `FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md` is built, replace the provisional `AuditIntelligenceSummaryInput` with the canonical audit-engine contract or a thin adapter.
- When CBCS phase-0 audit operations become live, ensure the review board can display:
  - the source card snapshot
  - the derived CBCS recommendation
  - the final human-first coaching message
  side by side for operator QA.
- This update intentionally keeps CBCS as a consumer of perceptual intelligence, not the owner of perceptual truth.
