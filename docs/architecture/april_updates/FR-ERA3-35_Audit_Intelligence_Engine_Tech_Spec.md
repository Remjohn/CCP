# FR-ERA3-35 Audit Intelligence Engine Tech Spec

## §1 Files Read

### 1.1 Prompt and Protocol
- `docs/architecture/april_updates/spec_prompts/P0_S03_FR-ERA3-35_Audit_Intelligence_Engine.md`
- `docs/architecture/april_updates/spec_prompts/P0_S03A_FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy.md`
- `docs/architecture/april_updates/spec_prompts/P0_S03B_FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles.md`
- `docs/architecture/april_updates/spec_prompts/P0_S03C_FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board.md`
- `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

### 1.2 Source PRDs
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
- `docs/prd/modules/PRD_05_CBCS_Law28.md`
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

### 1.3 Mandatory Phase-0 Source Set
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Human_First_Brand_Doctrine.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md`
- `lab/ccp_biological_orchestration_model_v_1.md`
- `lab/phase0_eval_card_scoring_model_v_1.md`
- `lab/OmniShotCut Holistic Relational Shot Boundary.md`

### 1.4 Existing Backend and Model References
- `src/ccp/api/main.py`
- `src/ccp/core/receipt_chain.py`
- `src/ccp/services/trait_scoring_engine.py`
- `src/ccp/services/scorecard_emitter.py`
- `src/ccp/services/trivianar_engine_service.py`
- `src/ccp/models/leadership_scorecard_models.py`
- `src/ccp/models/score_viewer_models.py`
- `src/ccp/models/ca11_models.py`

### 1.5 Existing Test Patterns
- `tests/integration/test_fr2_sacred_audio.py`
- `tests/integration/test_era3_fr06_primitive_registry_api.py`
- `tests/integration/test_era3_fr18_cbcs_integration.py`
- `tests/integration/test_fr_era3_score_card_viewer.py`

### 1.6 Pre-Work Evidence

#### Protocol evidence
- The protocol says: `"New specs EXTEND this — they don't reinvent it."`
- The protocol also requires: `"Section 3 must include an "Existing Backend Integration" subsection"`.

#### PRD-01 evidence
- PRD-01 states: `"The Conscious Coaching Platform is a human expression refinement ecosystem — not an AI content generation tool"`.
- PRD-01 also states: `"The Anti-Slop Mandate is not an aesthetic preference. It is a business rule enforced across every system output."`
- PRD-01 further codifies the runtime chain: ``DNA / truth -> RNA / transcription -> force -> delivery -> variation -> rendered phenotype -> evaluation``.

#### PRD-05 evidence
- PRD-05 says CBCS: `diagnoses communication weakness`, `captures real evidence of change`, and produces `"Proof of change - through FR61-style communication metrics and voice evidence."`
- PRD-05 also says: `"Silence should be treated as a clinical or strategic signal, not merely an analytics event."`
- PRD-05 minimum standards include: `clear next ritual | required`.

#### PRD-09 evidence
- PRD-09 says: `"free proof must feel real and fast"`.
- PRD-09 says the commercial layer should feel like `"a transformation engine powered by continuous proof"`.
- PRD-09 defines the first bridge: `"free proof → $29.99 activation → $39.99 continuity or $99.99 Coach OS"`.
- PRD-09 also fixes the sales order as: `"delivery before brochure"` and `"benchmark before pitch"`.

#### Fladlien evidence
- The note says: `"The Audit Must Sell Without Over-Explaining"`.
- It says the audit should sell by: `"proving the prescription with the coach's own material"`.
- It also defines the free proof layer with `"Damage Index, Compounding Forecast, and Impact Score"` and the `"Animated Explainer Audit (120s)"`.

#### Human-First Brand Doctrine evidence
- The doctrine says CCP is `"a human-first communication and intelligence brand"`.
- It also says: `"The content is proof of that improvement."`
- It explicitly preserves `"real voice"`, `"real convictions"`, `"real stories"`, and `"real proof"`.

#### Conscious Reactions evidence
- The source of truth says reactions transform hot-topic response into `"a speaking improvement engine"`, `"a content generation engine"`, and `"a social proof engine"`.
- It also states: `"jury voting must remain separate from delivery scoring."`

#### Biological orchestration evidence
- The biological model keeps the system ordered as `DNA / truth -> RNA / transcription -> force -> delivery -> variation -> phenotype -> evaluation`.
- Audit belongs after renderable artifact assembly begins but before commercial routing and continuity escalation.

#### Phase-0 card scoring evidence
- The score note fixes the visible score families:
  - `Humanity`
  - `Presence`
  - `Trust`
  - `Memorability`
  - `Resonance`
  - `Signal`
  - `AI Slop Risk`
- It also states: `"the eval system is canonical; the card system is the visible game layer on top of it."`

#### OmniShotCut evidence
- OmniShotCut treats video segmentation as `"structured relational prediction"`.
- It adds `"intra-shot relations"` and `"inter-shot relations"` rather than naive cut detection only.
- This is useful as a future-ready reel-structure reference, not as the totality of CCP audit logic.

#### Existing backend signature evidence
- `TraitScoringEngine.score_all_traits(self) -> list[ScoredTrait]`
- `ScorecardEmitter.emit(self, scorecard: LeadershipScorecard, raise_on_validation_failure: bool = True) -> tuple[LeadershipScorecard, list[str]]`
- `calculate_countdown_score(elapsed_ms: int, is_correct: bool) -> int`
- `ReceiptChain.log(...) -> ReceiptEntry`

#### Existing model/test evidence
- `ScoreCardViewerPayload` already models layered viewer outputs rather than raw internal calculations.
- `ScoredTrait` requires evidence and fails if none exists.
- `test_era3_fr06_primitive_registry_api.py` proves route-level registry contract testing is already normal in this repo.
- `test_fr_era3_score_card_viewer.py` proves viewer-surface fallback honesty is already an accepted integration-test pattern.

### 1.7 Dependency Reality Check
- `FR-ERA3-35A`, `FR-ERA3-35B`, and `FR-ERA3-35C` prompt files exist.
- Their implementation specs do **not** exist in the workspace yet.
- Therefore this spec must define how `FR-ERA3-35` consumes those layers through a strict provisional contract boundary until those upstream specs are built.

---

## §2 Overview

### 2.1 Problem
Phase-0 needs an audit engine that does more than output a generic score report.

It must:
- diagnose real weakness
- reinforce real strength
- quantify compounding damage
- prescribe the next correction
- prove the prescription using the coach's own material
- point naturally toward:
  - speaking improvement
  - live reactions / authority building
  - accountability
  - the `$29.99 -> $39.99 -> $99.99` ladder

Without this, the proof layer collapses into either:
- generic marketing copy
- shallow content diagnostics
- or pretty-but-empty score cards

### 2.2 Solution
Introduce a canonical `Audit Intelligence Engine` that:
- consumes canonical eval definitions and visible score vocab from upstream layers
- evaluates multimodal content targets
- emits typed diagnostic, prescription, and proof payloads
- produces outputs suitable for:
  - PDF audit generation
  - scoring-card audit boards
  - avatar-led or animated explainer audit videos
  - internal review interfaces

### 2.3 Scope
This spec defines:
- audit ownership
- modality-specific audit logic
- damage and reinforcement modeling
- prescription and proof-of-prescription structures
- continuity bridge recommendation logic
- PDF and video payload outputs

This spec does not define:
- canonical eval registry contents
- benchmark weighting bundles
- card visual presentation layer
- final PDF renderer implementation
- final video renderer implementation

### 2.4 Architectural Position
The audit engine sits after intake and before delivery orchestration.

In runtime sequence:
- intake normalizes inputs
- eval / benchmark layers provide scoring law
- audit interprets and packages meaning
- render layers materialize PDF and video artifacts
- commercial bridge routes activation and upgrade

### 2.5 Guiding Law
The audit sells by:
- diagnosis
- prescription
- proof

Never by long explanation first.

---

## §3.1 DEP-IDs

| DEP-ID | Name | Owned By | Purpose |
|---|---|---|---|
| `DEP-ERA3-35-001` | Audit Intelligence Report | FR-ERA3-35 | Master typed audit result |
| `DEP-ERA3-35-002` | Damage Index | FR-ERA3-35 | Quantifies present weakness and current cost |
| `DEP-ERA3-35-003` | Compounding Forecast | FR-ERA3-35 | Projects likely continuation cost if unchanged |
| `DEP-ERA3-35-004` | Strength Reinforcement Block | FR-ERA3-35 | Reinforces what should be preserved or doubled down on |
| `DEP-ERA3-35-005` | Prescription Block | FR-ERA3-35 | Describes fix path |
| `DEP-ERA3-35-006` | Proof Of Prescription Block | FR-ERA3-35 | Ties the prescription to visible transformed proof |
| `DEP-ERA3-35-007` | Continuity Bridge Recommendation | FR-ERA3-35 | Points toward $29.99 / $39.99 / $99.99 logic |
| `DEP-ERA3-35-008` | Multimodal Audit Target Descriptor | FR-ERA3-35 | Unified description of image, carousel, or reel target |
| `DEP-ERA3-35-009` | Caption Audit Block | FR-ERA3-35 | Caption/copy-specific findings |
| `DEP-ERA3-35-010` | Single Image Audit Block | FR-ERA3-35 | Image-post-specific findings |
| `DEP-ERA3-35-011` | Carousel Audit Block | FR-ERA3-35 | Carousel-specific findings |
| `DEP-ERA3-35-012` | Reel Audit Block | FR-ERA3-35 | Reel-specific findings |
| `DEP-ERA3-35-013` | Video Structure Audit Block | FR-ERA3-35 | Reel shot/pacing/transition structure findings |
| `DEP-ERA3-35-014` | PDF Audit Payload | FR-ERA3-35 | Structured payload for PDF renderers |
| `DEP-ERA3-35-015` | Explainer Audit Video Payload | FR-ERA3-35 | Structured payload for animated audit video renderers |

### 3.1A Upstream DEP Relationships

| Upstream Spec | Relationship | Notes |
|---|---|---|
| `FR-ERA3-33` | consumes | intake packet and audit target refs |
| `FR-ERA3-35A` | consumes | canonical eval definitions and score families |
| `FR-ERA3-35B` | consumes | weighting bundles by content type and archetype |
| `FR-ERA3-35C` | consumes | card/board formatting contracts |
| `FR-ERA3-12` | hands off to | downstream media and audit video rendering |
| `FR-ERA3-18` | hands off to | coaching implications for accountability and speaking |
| `FR-ERA3-05-CORE` | hands off to | reactions and visible score carryover |

---

## §3.2 Backend

### 3.2.1 Existing Backend Integration
This spec extends existing CCP patterns rather than inventing a detached reporting stack.

Relevant existing files:
- `src/ccp/api/main.py`
  - new audit routes must be added through the existing FastAPI app
- `src/ccp/core/receipt_chain.py`
  - audit generation and state transitions must be receipt-loggable
- `src/ccp/services/trait_scoring_engine.py`
  - precedent for score engines that operate over canonical inputs and produce evidence-backed outputs
- `src/ccp/services/scorecard_emitter.py`
  - precedent for validating and emitting typed report artifacts
- `src/ccp/services/trivianar_engine_service.py`
  - precedent for deterministic scoring helpers and typed game/runtime results

### 3.2.2 Existing Service Signatures To Mirror
- `TraitScoringEngine.score_all_traits(self) -> list[ScoredTrait]`
- `ScorecardEmitter.validate(self, scorecard: LeadershipScorecard) -> list[str]`
- `ScorecardEmitter.emit(self, scorecard: LeadershipScorecard, raise_on_validation_failure: bool = True) -> tuple[LeadershipScorecard, list[str]]`
- `ReceiptChain.log(...) -> ReceiptEntry`
- `calculate_countdown_score(elapsed_ms: int, is_correct: bool) -> int`

### 3.2.3 Existing Model Patterns To Reuse
- `ScoredTrait` enforces evidence presence
- `ScoreCardViewerPayload` separates internal interpretation from viewer-facing surface
- `ca11_models.py` shows established upload/result packet conventions

### 3.2.4 Recommended New Files
- `src/ccp/models/phase0_audit_models.py`
- `src/ccp/services/audit_intelligence_engine.py`
- `src/ccp/api/phase0_audit.py`
- `tests/integration/test_era3_fr35_audit_intelligence_engine.py`
- `tests/services/test_phase0_audit_intelligence_engine.py`
- `tests/models/test_phase0_audit_models.py`

### 3.2.5 Existing Tables and Persistence Alignment
The engine should align with existing storage/audit trail patterns:
- `receipt_chain`
- `asset_registry`
- prospective future `trial-phase0 package lineage` state mentioned in PRD-09

### 3.2.6 Existing Test Pattern Alignment
Use these test styles:
- route contract testing from `test_era3_fr06_primitive_registry_api.py`
- viewer-fallback honesty from `test_fr_era3_score_card_viewer.py`
- relationship-sensitive coaching wording from `test_era3_fr18_cbcs_integration.py`
- receipt-chain and pipeline provenance expectations from `test_fr2_sacred_audio.py`

---

## §3.3 Scores / Packets / Reports

### 3.3.1 Audit Engine Ownership
FR-ERA3-35 owns:
- audit interpretation
- damage modeling
- reinforcement modeling
- prescription modeling
- proof-of-prescription packaging
- continuity bridge recommendation
- PDF/video payload assembly

FR-ERA3-35 does **not** own:
- visible score vocabulary definition
- normalization law
- content-type weighting bundles
- card visual layout law

### 3.3.2 Score Consumption Rule
The engine must consume upstream visible score families exactly as:
- `Humanity`
- `Presence`
- `Trust`
- `Memorability`
- `Resonance`
- `Signal`
- `AI Slop Risk`

No local synonyms may replace them in payload contracts.

### 3.3.3 Internal Audit Themes
Beyond generic quality, the audit must explicitly evaluate and interpret:
- authority dilution
- memorability weakness
- proof weakness
- visible humanity weakness
- genericity / red-ocean blending
- experiential deficit
- speaking gap
- live reaction / live authority gap

### 3.3.4 Master Artifact Classes
- report artifact
- damage artifact
- reinforcement artifact
- prescription artifact
- proof artifact
- continuity artifact
- modality-specific audit blocks
- render payloads

### 3.3.5 Audit Output Families

#### Internal operator outputs
- complete typed report
- readiness flags
- blocker list
- review summary

#### Prospect-facing outputs
- score cards
- PDF audit
- animated/voice-led audit explainer
- before/after comparisons

### 3.3.6 Commercial Interpretation Law
The audit must answer:
- what is hurting them now?
- what will keep hurting them if unchanged?
- what is already strong?
- what should they do next?
- what did CCP already prove is possible?
- what continuity path makes sense?

### 3.3.7 Modality Split
The engine must treat these as distinct modalities:
- single-image post + caption
- carousel + caption
- reel + caption

This prevents image and video audits from collapsing into caption-only scoring.

---

## §3.4 Governance Constraints & CBAR Mandates

### 3.4A CBAR Mandate Enforcement

The Audit Intelligence Engine is governed by 6 Trial Phase-0 CBAR Mandates. The following table maps each mandate to its originating story, governing experience primitive, and programmatic enforcement mechanism:

| Mandate ID & Name | Governing Story | Governing Primitive | Programmatic Enforcement Mechanism |
|---|---|---|---|
| **Phase0-M1: Audit-Sells-By-Diagnosis Rule** | Story P0-S3.1 | `EXP-FBK-001` (Reflective Scoring) | Handled in `_calculate_damage_index()`. Evaluates exact gap breakdowns instead of marketing pitches; outputs must reflect diagnostic reality. |
| **Phase0-M2: Human-First Proof Rule** | Story P0-S3.2 | `EXP-TRS-004` (Reflective Social Proof) | Verified by ensuring case study assets, voice DNA source references, or transcripts are linked in `ProofOfPrescriptionBlock.transformed_asset_refs`. |
| **Phase0-M3: No-Explanation-First Rule** | Story P0-S3.3 | `EXP-FBK-001` (Reflective Scoring) | Enforced by schema layout order. The report leads directly with `visible_scores` and `damage_index` blocks. Conceptual guides without diagnostics fail validation. |
| **Phase0-M4: Damage-Before-Delight Rule** | Story P0-S3.4 | `EXP-TRS-001` (Visceral Hooking) | Enforced by requiring `damage_index` and `compounding_forecast` blocks before strengths/prescriptions, and detailing dilution risks first in participant summaries. |
| **Phase0-M5: Prescription-With-Proof Rule** | Story P0-S3.5 | `EXP-TRS-004` (Reflective Social Proof) | Enforced in Pydantic schema validation. An `AuditIntelligenceReport` is invalid unless it contains both a `PrescriptionBlock` and a `ProofOfPrescriptionBlock`. |
| **Phase0-M6: Continuity-Bridge Rule** | Story P0-S3.6 | `EXP-FRC-002` (B=MAP Friction Audit) | Enforced by `ContinuityBridgeRecommendation` which maps the overall damage score directly to one of three paid tiers (`proof_unlock_2999`, `speaking_learning_3999`, `coach_os_9999`). |

### 3.4B General Governance Rules

#### 3.4.1 Audit-Sells-By-Diagnosis Rule
The audit must not spend its primary energy explaining CCP as a product. It must diagnose the coach’s current signal and make the need legible.

#### 3.4.2 Human-First Proof Rule
The audit must favor interpretation grounded in real voice, real image choices, real story material, real audience context, and real proof artifacts.

#### 3.4.3 No-Explanation-First Rule
Long category explanation without diagnosis is forbidden.

#### 3.4.4 Damage-Before-Delight Rule
The audit must surface what is being lost or diluted before drifting into generic encouragement.

#### 3.4.5 Prescription-With-Proof Rule
Every major prescription must be paired with a visible or renderable proof-of-prescription object.

#### 3.4.6 Continuity-Bridge Rule
The audit must naturally support:
- `$29.99` first proof unlock
- `$39.99` speaking / learning continuity
- `$99.99` deployment / weekly proof engine

#### 3.4.7 No Ad-Hoc Score Vocabulary
Until `FR-ERA3-35A/B/C` are built, the engine may use only the score vocabulary fixed in `lab/phase0_eval_card_scoring_model_v_1.md`.

#### 3.4.8 No Caption-Only Reel Audit
Reel audits must include temporal or structural interpretation, even if the first implementation uses light-weight fallback instead of full OmniShotCut-style segmentation.

#### 3.4.9 Reinforcement Is Mandatory
If the content already does something strong, the audit must capture and reinforce it.

#### 3.4.10 Dignity Constraint
The tone must not shame the prospect or frame weakness as identity failure. This is especially important because PRD-05 treats silence and weak performance as relationally sensitive signals.

---

## §3.5 Technical Decisions

### 3.5.1 Decision: Upstream Eval Layers Are Consumed, Not Recreated
Rationale:
- keeps audit logic consistent with future internal QA
- prevents score drift
- preserves card vocabulary stability

### 3.5.2 Decision: Audit Owns Interpretation, Not Raw Measurement
Rationale:
- raw measurement belongs to eval and benchmark layers
- audit adds diagnosis, reinforcement, and prescription packaging

### 3.5.3 Decision: Multimodal Audit Blocks Are First-Class
Rationale:
- images, carousels, and reels have genuinely different failure surfaces
- caption-only reporting would violate the prompt and the product truth

### 3.5.4 Decision: Reel Structure Contract Is Future-Ready
Rationale:
- OmniShotCut proves shot structure can be modeled as relations, not just clips
- first implementation can use lighter heuristics
- schema should already support richer video-structure interpretation later

### 3.5.5 Decision: PDF and Audit Video Payloads Are Canonical Outputs
Rationale:
- makes Phase-0 delivery orchestration deterministic
- makes template-building easier downstream
- avoids bespoke per-surface report logic

### 3.5.6 Decision: Bridge Recommendation Is Typed
Rationale:
- keeps commercial routing explainable
- prevents vague “maybe buy more” endings

### 3.5.7 Decision: Hard Dependency Gap Is Declared Honestly
Rationale:
- `FR-ERA3-35A/B/C` are not built yet
- this spec therefore defines a provisional adapter contract instead of pretending those layers already ship

### 3.5.8 Decision: Strength Reinforcement Is Separate From Delight Copy
Rationale:
- reinforcement preserves dignity
- reinforcement also identifies what CCP should preserve rather than overwrite

### 3.5.9 Decision: Visible Score Summary and Hidden Support Data Coexist
Rationale:
- visible scores keep the audit easy to understand
- hidden support metrics allow modality nuance without cluttering card faces

### 3.5.10 Decision: Audit Engine Stays Relationship-Aware
Rationale:
- PRD-05 explicitly says silence and weak performance are relational signals
- audit copy and upgrade logic should reflect that instead of behaving like an aggressive SaaS analyzer

---

## §4 Plan

### Phase 1: Contract and Boundary Foundation
1. Define `phase0_audit_models.py`.
2. Declare all canonical report and block schemas.
3. Add provisional adapters for missing upstream specs `35A/B/C`.
4. Fix visible score family enum to the exact seven values.

### Phase 2: Multimodal Interpretation Engine
5. Implement `CaptionAuditBlock` generation.
6. Implement `SingleImageAuditBlock` generation.
7. Implement `CarouselAuditBlock` generation.
8. Implement `ReelAuditBlock` generation.
9. Implement `VideoStructureAuditBlock` fallback heuristics.

### Phase 3: Diagnostic Intelligence
10. Implement damage-index calculation.
11. Implement compounding forecast logic.
12. Implement strength reinforcement extraction.
13. Implement prescription generation.
14. Implement proof-of-prescription generation.
15. Implement continuity bridge recommendation generation.

### Phase 4: Payload Emission and Persistence
16. Implement `AuditIntelligenceReport` assembly.
17. Implement `PdfAuditPayload` assembly.
18. Implement `ExplainerAuditVideoPayload` assembly.
19. Add receipt logging around audit build phases.
20. Add storage/persistence contract for audit artifacts and packet lineage.

### Phase 5: API and Orchestration
21. Add `phase0_audit.py` FastAPI router.
22. Add endpoint to generate audit from `Phase0ProspectPacket`.
23. Add endpoint to retrieve audit report.
24. Add endpoint to retrieve PDF/video payloads.

### Phase 6: Validation and QA
25. Add integration tests for all modalities.
26. Add failure tests for missing eval adapters.
27. Add fallback tests for incomplete video structure data.
28. Add viewer-surface honesty tests.

---

## §5 Schema

### 5.1 Enum: `AuditSeverity`
```python
class AuditSeverity(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"
```

### 5.2 Enum: `AuditTargetContentType`
```python
class AuditTargetContentType(str, Enum):
    single_image_caption = "single_image_caption"
    carousel_caption = "carousel_caption"
    reel_caption = "reel_caption"
```

### 5.3 Enum: `BridgeTierRecommendation`
```python
class BridgeTierRecommendation(str, Enum):
    proof_unlock_2999 = "proof_unlock_2999"
    speaking_learning_3999 = "speaking_learning_3999"
    coach_os_9999 = "coach_os_9999"
```

### 5.4 Enum: `ForecastDirection`
```python
class ForecastDirection(str, Enum):
    improving = "improving"
    flat = "flat"
    degrading = "degrading"
```

### 5.5 Enum: `VideoStructureAvailability`
```python
class VideoStructureAvailability(str, Enum):
    unavailable = "unavailable"
    heuristic = "heuristic"
    segmented = "segmented"
```

### 5.6 Model: `VisibleScoreSnapshot`
```python
class VisibleScoreSnapshot(BaseModel):
    humanity: int = Field(..., ge=0, le=99)
    presence: int = Field(..., ge=0, le=99)
    trust: int = Field(..., ge=0, le=99)
    memorability: int = Field(..., ge=0, le=99)
    resonance: int = Field(..., ge=0, le=99)
    signal: int = Field(..., ge=0, le=99)
    ai_slop_risk: int = Field(..., ge=0, le=99)
```

### 5.7 Model: `AuditFinding`
```python
class AuditFinding(BaseModel):
    finding_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    severity: AuditSeverity = Field(...)
    description: str = Field(..., min_length=1)
    evidence_summary: str = Field(..., min_length=1)
```

### 5.8 Model: `DamageIndex`
```python
class DamageIndex(BaseModel):
    overall_damage_score: int = Field(..., ge=0, le=99)
    authority_dilution_score: int = Field(..., ge=0, le=99)
    memorability_weakness_score: int = Field(..., ge=0, le=99)
    proof_weakness_score: int = Field(..., ge=0, le=99)
    humanity_weakness_score: int = Field(..., ge=0, le=99)
    genericity_blending_score: int = Field(..., ge=0, le=99)
    experiential_deficit_score: int = Field(..., ge=0, le=99)
    speaking_gap_score: int = Field(..., ge=0, le=99)
    reaction_gap_score: int = Field(..., ge=0, le=99)
    explanation: str = Field(..., min_length=1)
```

### 5.9 Model: `CompoundingForecast`
```python
class CompoundingForecast(BaseModel):
    direction: ForecastDirection = Field(...)
    thirty_day_risk_score: int = Field(..., ge=0, le=99, alias="30_day_risk_score")
    ninety_day_risk_score: int = Field(..., ge=0, le=99, alias="90_day_risk_score")
    trust_decay_risk: int = Field(..., ge=0, le=99)
    authority_decay_risk: int = Field(..., ge=0, le=99)
    invisibility_risk: int = Field(..., ge=0, le=99)
    summary: str = Field(..., min_length=1)

    class Config:
        populate_by_name = True
```

### 5.10 Model: `StrengthReinforcementBlock`
```python
class StrengthReinforcementBlock(BaseModel):
    retained_strengths: list[str] = Field(default_factory=list)
    why_they_work: list[str] = Field(default_factory=list)
    preserve_instructions: list[str] = Field(default_factory=list)
    reinforcement_summary: str = Field(..., min_length=1)
```

### 5.11 Model: `PrescriptionBlock`
```python
class PrescriptionBlock(BaseModel):
    primary_shift: str = Field(..., min_length=1)
    supporting_shifts: list[str] = Field(default_factory=list)
    speaking_improvement_path: list[str] = Field(default_factory=list)
    reaction_improvement_path: list[str] = Field(default_factory=list)
    content_improvement_path: list[str] = Field(default_factory=list)
    why_now: str = Field(..., min_length=1)
```

### 5.12 Model: `ProofOfPrescriptionBlock`
```python
class ProofOfPrescriptionBlock(BaseModel):
    proof_summary: str = Field(..., min_length=1)
    transformed_asset_refs: list[str] = Field(default_factory=list)
    scoring_card_refs: list[str] = Field(default_factory=list)
    before_after_claim: str = Field(..., min_length=1)
    confidence_score: int = Field(..., ge=0, le=99)
```

### 5.13 Model: `ContinuityBridgeRecommendation`
```python
class ContinuityBridgeRecommendation(BaseModel):
    recommended_tier: BridgeTierRecommendation = Field(...)
    reason: str = Field(..., min_length=1)
    ladder_copy: str = Field(..., min_length=1)
    upgrade_credit_note: str = Field(default="")
    next_best_action: str = Field(..., min_length=1)
```

### 5.14 Model: `AuditTargetDescriptor`
```python
class AuditTargetDescriptor(BaseModel):
    audit_target_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    content_type: AuditTargetContentType = Field(...)
    primary_media_source_ids: list[str] = Field(default_factory=list)
    caption_id: str | None = Field(default=None)
    platform_hint: str | None = Field(default=None)
    archetype_hint: str | None = Field(default=None)
    content_url: str | None = Field(default=None)
```

### 5.15 Model: `CaptionAuditBlock`
```python
class CaptionAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: list[AuditFinding] = Field(default_factory=list)
    caption_alignment_notes: list[str] = Field(default_factory=list)
    proof_language_notes: list[str] = Field(default_factory=list)
    genericity_notes: list[str] = Field(default_factory=list)
    summary: str = Field(..., min_length=1)
```

### 5.16 Model: `SingleImageAuditBlock`
```python
class SingleImageAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: list[AuditFinding] = Field(default_factory=list)
    visual_authority_notes: list[str] = Field(default_factory=list)
    proof_density_notes: list[str] = Field(default_factory=list)
    image_caption_coherence_notes: list[str] = Field(default_factory=list)
    summary: str = Field(..., min_length=1)
```

### 5.17 Model: `CarouselAuditBlock`
```python
class CarouselAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: list[AuditFinding] = Field(default_factory=list)
    sequencing_notes: list[str] = Field(default_factory=list)
    frame_to_frame_logic_notes: list[str] = Field(default_factory=list)
    caption_interaction_notes: list[str] = Field(default_factory=list)
    summary: str = Field(..., min_length=1)
```

### 5.18 Model: `VideoStructureAuditBlock`
```python
class VideoStructureAuditBlock(BaseModel):
    availability: VideoStructureAvailability = Field(...)
    hook_retention_score: int = Field(..., ge=0, le=99)
    pacing_coherence_score: int = Field(..., ge=0, le=99)
    shot_transition_coherence_score: int = Field(..., ge=0, le=99)
    temporal_salience_score: int = Field(..., ge=0, le=99)
    structure_notes: list[str] = Field(default_factory=list)
    fallback_mode_reason: str = Field(default="")
```

### 5.19 Model: `ReelAuditBlock`
```python
class ReelAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: list[AuditFinding] = Field(default_factory=list)
    script_semantic_notes: list[str] = Field(default_factory=list)
    key_frame_notes: list[str] = Field(default_factory=list)
    caption_video_alignment_notes: list[str] = Field(default_factory=list)
    video_structure: VideoStructureAuditBlock = Field(...)
    summary: str = Field(..., min_length=1)
```

### 5.20 Model: `AuditIntelligenceReport`
```python
class AuditIntelligenceReport(BaseModel):
    report_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    coach_id: str | None = Field(default=None)
    audit_target: AuditTargetDescriptor = Field(...)
    visible_scores: VisibleScoreSnapshot = Field(...)
    damage_index: DamageIndex = Field(...)
    compounding_forecast: CompoundingForecast = Field(...)
    strength_reinforcement: StrengthReinforcementBlock = Field(...)
    prescription: PrescriptionBlock = Field(...)
    proof_of_prescription: ProofOfPrescriptionBlock = Field(...)
    continuity_bridge: ContinuityBridgeRecommendation = Field(...)
    caption_block: CaptionAuditBlock = Field(...)
    single_image_block: SingleImageAuditBlock | None = Field(default=None)
    carousel_block: CarouselAuditBlock | None = Field(default=None)
    reel_block: ReelAuditBlock | None = Field(default=None)
    operator_summary: str = Field(..., min_length=1)
    participant_summary: str = Field(..., min_length=1)
    receipt_ids: list[str] = Field(default_factory=list)
```

### 5.21 Model: `PdfAuditPayload`
```python
class PdfAuditPayload(BaseModel):
    report_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    cover_thumbnail_asset_id: str | None = Field(default=None)
    visible_scores: VisibleScoreSnapshot = Field(...)
    card_refs: list[str] = Field(default_factory=list)
    sections: list[str] = Field(default_factory=list)
    summary_copy: str = Field(..., min_length=1)
    render_template_key: str = Field(..., min_length=1)
```

### 5.22 Model: `ExplainerAuditVideoPayload`
```python
class ExplainerAuditVideoPayload(BaseModel):
    report_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    visible_scores: VisibleScoreSnapshot = Field(...)
    card_refs: list[str] = Field(default_factory=list)
    scene_script_blocks: list[str] = Field(default_factory=list)
    voiceover_script: str = Field(..., min_length=1)
    avatar_ref_id: str | None = Field(default=None)
    render_template_key: str = Field(..., min_length=1)
```

### 5.23 Schema Rules
- Only one of:
  - `single_image_block`
  - `carousel_block`
  - `reel_block`
  may be populated, based on `audit_target.content_type`.
- `CaptionAuditBlock` is mandatory for all modalities.
- `VideoStructureAuditBlock` is mandatory inside every reel audit, even when availability is `heuristic` or `unavailable`.
- `AuditIntelligenceReport.visible_scores` must match the canonical visible score vocabulary exactly.
- `PdfAuditPayload` and `ExplainerAuditVideoPayload` must be derivable directly from a valid `AuditIntelligenceReport`.

---

## §6 Fallback

### 6.1 Upstream Spec Missing Fallback
If `FR-ERA3-35A/B/C` are not yet implemented:
- load provisional vocabulary and weighting contracts from:
  - `lab/phase0_eval_card_scoring_model_v_1.md`
  - prompt-defined requirements for `35A/B/C`
- mark report metadata with `provisional_upstream_contract = true`

### 6.2 Incomplete Reel Structure Fallback
If no full video-segmentation layer is available:
- compute lightweight structure features from:
  - transcript pacing
  - clip duration
  - heuristic frame samples
  - simple scene/transition markers when available
- set `VideoStructureAvailability = heuristic`

### 6.3 Missing Transcript Fallback
If transcript is missing for a reel:
- attempt caption + frame-first provisional audit
- require explicit degraded-confidence note
- cap final confidence and prevent “high-confidence” prescription claims

### 6.4 Missing Proof Transformation Fallback
If proof-of-prescription artifact generation is not yet available:
- return a non-empty block with:
  - proposed proof strategy
  - missing artifact note
  - reduced confidence
- do not silently omit the block

### 6.5 Missing Guardian BI Fallback
If audience/business context is incomplete:
- allow audit generation
- degrade compounding and ladder-confidence claims
- surface warning in operator summary

### 6.6 Missing Card Renderer Fallback
If `35C` presentation layer is absent:
- still emit `card_refs` placeholders and canonical score payloads
- leave visual realization to downstream renderer once built

### 6.7 Failure-Closed Law
If the engine cannot determine:
- modality
- visible score projection
- or continuity recommendation

it must fail closed and return a typed validation error rather than fabricate certainty.

---

## §7 Tasks

1. Create `phase0_audit_models.py`.
2. Add `VisibleScoreSnapshot` model.
3. Add `DamageIndex` model.
4. Add `CompoundingForecast` model.
5. Add `StrengthReinforcementBlock` model.
6. Add `PrescriptionBlock` model.
7. Add `ProofOfPrescriptionBlock` model.
8. Add `ContinuityBridgeRecommendation` model.
9. Add `CaptionAuditBlock`.
10. Add `SingleImageAuditBlock`.
11. Add `CarouselAuditBlock`.
12. Add `VideoStructureAuditBlock`.
13. Add `ReelAuditBlock`.
14. Add `AuditIntelligenceReport`.
15. Add `PdfAuditPayload`.
16. Add `ExplainerAuditVideoPayload`.
17. Create `audit_intelligence_engine.py`.
18. Implement upstream contract adapter.
19. Implement modality switch logic.
20. Implement caption analysis entrypoint.
21. Implement image analysis entrypoint.
22. Implement carousel analysis entrypoint.
23. Implement reel analysis entrypoint.
24. Implement video-structure fallback analyzer.
25. Implement damage index computation.
26. Implement compounding forecast computation.
27. Implement strength reinforcement extraction.
28. Implement prescription synthesis.
29. Implement proof-of-prescription synthesis.
30. Implement continuity bridge recommendation.
31. Implement PDF payload assembly.
32. Implement explainer video payload assembly.
33. Add receipt logging around generation.
34. Add API routes.
35. Add route-level validation tests.
36. Add modality-specific integration tests.

---

## §8 AC

### AC-1 Multimodal Support
The engine accepts and audits single image + caption, carousel + caption, and reel + caption.
- **Tested Mandate:** `Phase0-M2: Human-First Proof Rule` (Story P0-S3.2)
- **Failure example:** A reel is scored only from caption text and no reel block is emitted.

### AC-2 Canonical Visible Score Use
The engine never invents new visible score labels.
- **Tested Mandate:** `Phase0-M3: No-Explanation-First Rule` (Story P0-S3.3)
- **Failure example:** Output uses `Distinction` or `Charisma` as top-level visible score families.

### AC-3 Damage Modeling
The engine emits a `DamageIndex` that includes authority, memorability, proof, humanity, genericity, experiential, speaking, and reaction gaps.
- **Tested Mandate:** `Phase0-M4: Damage-Before-Delight Rule` & `Phase0-M1: Audit-Sells-By-Diagnosis Rule` (Stories P0-S3.4, P0-S3.1)
- **Failure example:** Report says “needs improvement” with no structured damage object.

### AC-4 Reinforcement Block
The engine reinforces what is already working when evidence exists.
- **Tested Mandate:** `Phase0-M4: Damage-Before-Delight Rule` (Story P0-S3.4)
- **Failure example:** Report lists only weaknesses even when Humanity and Trust are already strong.

### AC-5 Prescription With Proof
Every audit includes both `PrescriptionBlock` and `ProofOfPrescriptionBlock`.
- **Tested Mandate:** `Phase0-M5: Prescription-With-Proof Rule` (Story P0-S3.5)
- **Failure example:** Report gives advice but no proof strategy or transformed-asset linkage.

### AC-6 Reel Structure Logic
Every reel audit includes `VideoStructureAuditBlock`.
- **Tested Mandate:** `Phase0-M2: Human-First Proof Rule` (Story P0-S3.2)
- **Failure example:** Reel audit has script notes only and no pacing/structure object.

### AC-7 PDF Payload Emission
Every successful report can emit a `PdfAuditPayload`.
- **Tested Mandate:** `Phase0-M3: No-Explanation-First Rule` (Story P0-S3.3)
- **Failure example:** Report exists but cannot be rendered into a PDF package because card or summary payload is missing.

### AC-8 Explainer Video Payload Emission
Every successful report can emit an `ExplainerAuditVideoPayload`.
- **Tested Mandate:** `Phase0-M5: Prescription-With-Proof Rule` (Story P0-S3.5)
- **Failure example:** Audit video requires manual rewriting because no structured voiceover or scene blocks were emitted.

### AC-9 Continuity Bridge
Every audit returns a typed continuity recommendation tied to the CCP ladder.
- **Tested Mandate:** `Phase0-M6: Continuity-Bridge Rule` (Story P0-S3.6)
- **Failure example:** Report ends with generic “book a call” language and no ladder logic.

### AC-10 Honest Fallback
When upstream eval/card layers or video segmentation are incomplete, the report marks degraded confidence explicitly.
- **Tested Mandate:** `Phase0-M2: Human-First Proof Rule` (Story P0-S3.2)
- **Failure example:** Audit acts fully certain while using heuristic-only reel structure analysis.

### AC-11 Relationship-Safe Tone
Prospect-facing summary preserves dignity and avoids shame framing.
- **Tested Mandate:** `Phase0-M1: Audit-Sells-By-Diagnosis Rule` (Story P0-S3.1)
- **Failure example:** “Your content is bad and nobody will trust you” instead of precise, evidence-backed diagnosis.

### AC-12 No Generic Report Card Drift
The report must feel like a CCP diagnostic object, not a generic content-grade sheet.
- **Tested Mandate:** `Phase0-M1: Audit-Sells-By-Diagnosis Rule` (Story P0-S3.1)
- **Failure example:** Only gives broad engagement tips and formatting advice with no authority/proof/humanity logic.

---

## §9 Dependencies

### 9.1 Hard Dependencies
- `FR-ERA3-33 Phase0 Prospect Intake Console`
- future `FR-ERA3-35A Eval Registry and Scoring Taxonomy`
- future `FR-ERA3-35B Content Benchmark Profiles and Card Weighting Bundles`
- future `FR-ERA3-35C Eval Card System and Shareable Audit Board`

### 9.2 Soft Dependencies
- `FR-ERA3-12 CMF Arc Governed Rendering`
- `FR-ERA3-18 CBCS Four-Engine Runtime`
- `FR-ERA3-05-CORE Core Reaction Engine`

### 9.3 Existing Runtime Dependencies
- `src/ccp/core/receipt_chain.py`
- FastAPI route inclusion via `src/ccp/api/main.py`

### 9.4 Source Doctrine Dependencies
- Human-First Brand Doctrine
- Conscious Reactions Source of Truth
- Biological orchestration model
- Phase-0 eval card scoring model
- Fladlien commercial layer note

### 9.5 External Research Dependency
- OmniShotCut is a design reference for future reel-structure segmentation and relational transition understanding.
- It is not a mandatory first-implementation runtime dependency.

---

## §10 Testing

### 10.1 Integration Test File
- `tests/integration/test_era3_fr35_audit_intelligence_engine.py`

### 10.2 Required Integration Cases
- single image + caption report generation
- carousel + caption report generation
- reel + caption report generation
- PDF payload emission
- explainer video payload emission
- receipt logging after audit build
- upstream contract fallback when `35A/B/C` are absent

### 10.3 Service Test File
- `tests/services/test_phase0_audit_intelligence_engine.py`

### 10.4 Required Service Cases
- damage index computation
- compounding forecast computation
- reinforcement extraction
- prescription synthesis
- proof-of-prescription synthesis
- continuity bridge recommendation
- reel structure heuristic fallback

### 10.5 Model Test File
- `tests/models/test_phase0_audit_models.py`

### 10.6 Required Model Cases
- invalid visible score labels rejected
- out-of-range scores rejected
- invalid modality block combinations rejected
- missing reel structure block rejected for reels

### 10.7 Failure Tests
- no caption attached
- unknown content type
- missing upstream score adapter
- transcript absent for reel with no fallback note
- PDF payload requested from invalid report
- bridge recommendation omitted

### 10.8 Regression Tests
- ensure no new visible score names are introduced
- ensure prospect summary remains human-readable
- ensure operator summary can expose missing context without corrupting participant tone

### 10.9 Golden-Path Fixtures
Create fixtures for:
- strong human proof single-image example
- weak generic carousel example
- reel with strong script but weak pacing
- reel with strong presence but weak trust

### 10.10 Acceptance Threshold
This spec is only satisfied when the audit engine can produce, from one canonical report:
- a coherent operator diagnosis
- a dignified participant-facing audit
- a PDF-ready payload
- a video-ready payload
- and a commercially aligned next-step recommendation

If any one of those must be manually invented after the report returns, the engine is incomplete.
