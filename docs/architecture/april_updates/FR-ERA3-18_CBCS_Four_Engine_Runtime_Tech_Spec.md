# FR-ERA3-18 CBCS Four-Engine Runtime Tech Spec

## Pre-Work Log

### 1. Protocol Read
- Read `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`.
- Extracted the mandatory backend-extension rule from Section 2: Era 3 specs must extend the existing FastAPI, Pydantic, pipeline, agent, and service stack rather than inventing a parallel architecture.
- Extracted the Section 3 pre-flight requirement that the spec must load the PRD module, referenced specs, relevant primitives, the phase epic, and the CBAR audit before writing.
- Extracted the Section 4 format rule requiring 10 sections, explicit Existing Backend Integration, explicit CBAR Mandate Enforcement, and testing aligned to `tests/integration/`.

### 2. PRD Module Read
- Read `docs/prd/modules/PRD_05_CBCS_Law28.md`.
- Exact implementation-definition quote captured from the PRD: "For implementation clarity, PRD-05 treats CBCS as four interacting runtime engines: Diagnostic Engine, Ritual Engine, Evidence Engine, Relationship Engine."
- Exact system-definition quote captured from the PRD: "CBCS should be understood as a universal self-coding transformation engine."
- Extracted the daily loop: state check -> route selection -> daily prompt or drill -> user recording or reflection -> transcription and scoring -> context update -> next-step feedback -> continuity memory update.
- Brownfield read result:
  - EXISTING: `trait_scoring_engine.py`, `change_talk_vault.py`, `spt_stage_engine.py`, `identity_anchor_protocol.py`, `counterfactual_activation.py`, `learning_path_builder.py`, `dynamic_journaling_engine.py`, `scorecard_emitter.py`.
  - NEW for this spec: an explicit runtime orchestrator plus hard service separation between the four engines.
  - OBSOLETE: any monolithic "CBCS engine" that directly emits user-facing downgrade messaging without relationship-layer reframing.

### 3. Phase Epic Read
- Read `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md`.
- First acceptance-criteria line captured for Story 7.1:
  - "When the Evidence Engine extracts my FR61 biometric scores,"
  - "Then the Diagnostic Engine updates my capacity track and the Ritual Engine modifies tomorrow's drill to address the specific performance delta,"
  - "And if the Diagnostic Engine downgrades a capacity track or assigns an easier ritual, the Relationship Engine intercepts the notification and contextualizes it against my positive Long Loop macro trend..."
- Extracted the quality standard:
  - The user must never see only that they are "going backward".
  - All user-facing CBCS communication must route through the Relationship Engine framing layer.

### 4. CBAR Audit Read
- Read `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md`.
- Confirmed Phase4-M07 is binding and was rewritten against the real primitive registry.
- Audit quote captured:
  - "When the Diagnostic Engine downgrades a capacity track or assigns an easier ritual, the `Relationship Engine` MUST intercept the notification and contextualize it against the Long Loop."
- Hallucination purge confirmed:
  - `EXP-PRG-004` is not "Flow Through Grinding"; it is the actual registry primitive "Long Loops for Habit Formation."
- Banned primitive family check passed: no `EXP-TRB-*` primitives are used in this spec.

### 5. Primitive YAMLs Read
- Read `primitives/experience/progression_replay/EXP-PRG-004.yaml`.
  - `experience_primitive_id: "EXP-PRG-004"`
  - `canonical_name: "Long Loops for Habit Formation"`
- Read `primitives/experience/feedback_scoring/EXP-FBK-004.yaml`.
  - `experience_primitive_id: "EXP-FBK-004"`
  - `canonical_name: "Bring the Data Forward"`
- Why both are required here:
  - `EXP-PRG-004` governs the macro-trend framing rule during downgrades.
  - `EXP-FBK-004` governs the cumulative-investment metrics that the Relationship Engine can surface when raw daily performance dips.

<!-- UPDATED: Adding SDA pre-work proof explicitly as required by spec prompt -->
### 6. SDA Proof of Gap
- Quoting existing gap in the previous iteration of this spec:
  - "The `RelationshipTrendContext` is built purely from macro-trend statistics (14/30 day aggregates + cumulative investment)."
  - "The `RelationshipFramedNotification` schema's `safe_headline` and `safe_body` fields are text strings with no directional-integrity validation."
  - This shows the previous spec interpreted progress and identity without SDA-aware direction/loop logic. The Relationship Engine used math instead of existential geometry.

### 7. SDA Source Set Read
- Read `lab/semantic_discernment_architecture_content_engine_v_1.md`.
- Read `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`.
- Read `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`.
- Read `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`.
- Extracted mandatory packet inclusions for runtime evaluation: `InvariantFieldPacket`, `RepresentationGeometryPacket`, `EmergentContextualInvariant`, `FeedbackLoop`, `RecursivePattern`, `DirectionalIntegrityReport`.
<!-- /UPDATED -->

### 8. Backend Python Files Read
- Read and verified concrete signatures in the real codebase:
  - `src/ccp/services/trait_scoring_engine.py`
  - `src/ccp/services/learning_path_builder.py`
  - `src/ccp/services/habit_architecture.py`
  - `src/ccp/services/ritual_scheduler.py`
  - `src/ccp/services/ritual_resonance.py`
  - `src/ccp/services/dormancy_recovery_service.py`
  - `src/ccp/services/change_talk_vault.py`
  - `src/ccp/services/spt_stage_engine.py`
  - `src/ccp/services/identity_anchor_protocol.py`
  - `src/ccp/services/counterfactual_activation.py`
  - `src/ccp/services/dynamic_journaling_engine.py`
- Read supporting runtime-adjacent files:
  - `src/ccp/api/telegram_webhook.py`
  - `src/ccp/agents/vidye_router.py`
  - `src/ccp/models/cbcs_models.py`
  - `src/ccp/models/leadership_scorecard_models.py`
  - `src/ccp/services/scorecard_emitter.py`
  - `src/ccp/services/engagement_feedback.py`

### 9. Test Files Read
- Read `tests/integration/test_cbcs09_habit_architecture.py`.
- Read `tests/integration/test_fr7_leadership_scorecard.py`.

## 1. Files Read

1. `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. `docs/prd/modules/PRD_05_CBCS_Law28.md`
3. `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md`
4. `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md`
5. `docs/architecture/april_updates/spec_prompts/P6_S42_FR-ERA3-18_Update_CBCS_Four_Engine_Runtime_for_SDA.md`
6. `primitives/experience/progression_replay/EXP-PRG-004.yaml`
7. `primitives/experience/feedback_scoring/EXP-FBK-004.yaml`
8. `lab/semantic_discernment_architecture_content_engine_v_1.md`
9. `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
10. `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
11. `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`
12. `src/ccp/api/telegram_webhook.py`
13. `src/ccp/agents/vidye_router.py`
14. `src/ccp/models/cbcs_models.py`
15. `src/ccp/models/leadership_scorecard_models.py`
16. `src/ccp/services/trait_scoring_engine.py`
17. `src/ccp/services/change_talk_vault.py`
18. `src/ccp/services/spt_stage_engine.py`
19. `src/ccp/services/identity_anchor_protocol.py`
20. `src/ccp/services/counterfactual_activation.py`
21. `src/ccp/services/learning_path_builder.py`
22. `src/ccp/services/dynamic_journaling_engine.py`
23. `src/ccp/services/habit_architecture.py`
24. `src/ccp/services/ritual_scheduler.py`
25. `src/ccp/services/ritual_resonance.py`
26. `src/ccp/services/dormancy_recovery_service.py`
27. `src/ccp/services/engagement_feedback.py`
28. `src/ccp/services/scorecard_emitter.py`
29. `tests/integration/test_cbcs09_habit_architecture.py`
30. `tests/integration/test_fr7_leadership_scorecard.py`

## 2. Overview

### Problem
PRD-05 already defines CBCS as four interacting runtime engines, but the current brownfield backend is still a collection of powerful point services rather than an explicit runtime boundary. The dangerous gap is user-facing downgrade delivery. Evidence can be extracted and rituals can be changed, but without a hard intercept layer the system can accidentally tell the user they are "going backward", which violates Phase4-M07 and creates shame-based churn. 
<!-- UPDATED: Adding SDA integration context -->
Additionally, without Semantic Discernment Architecture (SDA) integration, identity commentary and challenge notifications operate on raw statistics instead of maintaining directional integrity, risking the introduction of corrosive feedback loops and misaligned representation geometry.
<!-- /UPDATED -->

### Solution
Implement a new orchestration layer named `CBCSFourEngineRuntimeService` that composes four physically separate services:

1. `CBCSEvidenceEngineService`
2. `CBCSDiagnosticEngineService`
3. `CBCSRitualEngineService`
4. `CBCSRelationshipEngineService`

The runtime accepts a fresh voice/reflection event, routes evidence extraction first, computes a diagnostic decision second, derives the next ritual adjustment third, and only then allows the Relationship Engine to decide what may be shown to the user. Diagnostic output is internal-only. Any downgrade or easier-drill assignment is intercepted and reframed against 14-day / 30-day macro trend context before notification delivery.
<!-- UPDATED: SDA solution components -->
Crucially, the Relationship Engine now utilizes SDA objects (`EmergentContextualInvariant`, `FeedbackLoop`, `RecursivePattern`) to evaluate semantic direction, while the generated identity artifacts (Sunday Postcards, User Cards, and escalations) undergo mandatory `DirectionalIntegrityPolicy` validation to ensure representation geometry alignment before reaching the user.
<!-- /UPDATED -->

### Scope
- In scope:
  - Runtime orchestration and service separation
  - New Pydantic contracts for cross-engine handoff
  - Long-loop context retrieval and framing
  - Downgrade interception and safe notification shaping
  - Integration with existing PRD-05 services and Telegram routing
  <!-- UPDATED: SDA scope additions -->
  - Integration of SDA metrics (`InvariantFieldPacket`, `RepresentationGeometryPacket`) into relationship framing
  - Tracking of `FeedbackLoop` and `RecursivePattern` objects across the challenge duration
  - `DirectionalIntegrityReport` generation for Sunday Postcards, User Cards, and escalation messaging
  <!-- /UPDATED -->
- Out of scope:
  - Rewriting FR61 scoring logic
  - Replacing existing habit, journaling, or dormancy services
  - New Mini App surfaces
  - Commercial routing or offer-tier logic
  <!-- UPDATED: SDA out of scope -->
  - Building the full canonical SDA ontology registry (this is an interpretation update, not an ontology registry spec)
  <!-- /UPDATED -->

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Name | Status | Purpose |
|---|---|---|---|
| `DEP-CBCS-401` | CBCS Runtime Session | NEW | Envelope for a single evidence-routing pass triggered by a voice note or reflection |
| `DEP-CBCS-402` | CBCS Evidence Packet | NEW | Canonical evidence output from FR61 scoring + CBCS sub-engines |
| `DEP-CBCS-403` | Diagnostic Capacity Decision | NEW | Internal-only capacity-track and difficulty adjustment decision |
| `DEP-CBCS-404` | Ritual Adjustment Plan | NEW | Next ritual/drill mutation plan produced from the diagnostic delta |
| `DEP-CBCS-405` | Relationship Trend Context | NEW | 14/30-day macro-trend snapshot plus cumulative investment metrics |
| `DEP-CBCS-406` | Relationship Framed Notification | NEW | The only user-facing message contract allowed out of this runtime |
| `DEP-ENG-025` | Dormancy Recovery Payload | EXISTING | Dormancy-aware suppression and recovery support |
| `DEP-ENG-026` | Leadership Scorecard | EXISTING | Existing FR61 score projection used as evidence substrate |
<!-- UPDATED: Adding SDA DEP-IDs -->
| `DEP-SDA-101` | Directional Integrity Report | EXISTING (FR-ERA3-20) | Verification object ensuring messages preserve invariant alignment |
| `DEP-SDA-102` | Semantic Evolution Record | EXISTING (FR-ERA3-20) | Longitudinal tracking of recursive patterns and feedback loops |
<!-- /UPDATED -->

### 3.2 Existing Backend Integration

This spec extends the current backend rather than replacing it.

#### Existing files consumed directly
- `src/ccp/services/trait_scoring_engine.py`
  - Source of FR61 biometric scoring.
  - Runtime usage: generate fresh short-loop evidence for the current submission.
- `src/ccp/services/change_talk_vault.py`
  - Source of DARN-CAT commitment evidence.
  - Runtime usage: enrich the evidence packet with motivation / resistance signals.
- `src/ccp/services/spt_stage_engine.py`
  - Source of disclosure-depth classification.
  - Runtime usage: enrich relationship safety and delivery-context evaluation.
- `src/ccp/services/habit_architecture.py`
  - Runtime usage: verify whether the user is operating from a concrete habit cue/action structure when adjusting drills.
- `src/ccp/services/learning_path_builder.py`
  - Runtime usage: convert diagnostic findings into a next-step recommendation and intensity boundary.
- `src/ccp/services/dynamic_journaling_engine.py`
  - Runtime usage: generate journaling fallback when the ritual plan chooses reflection instead of repetition.
- `src/ccp/services/ritual_scheduler.py`
  - Runtime usage: materialize the next ritual copy and dispatch metadata.
- `src/ccp/services/ritual_resonance.py`
  - Runtime usage: weave resonance references into the final safe delivery.
- `src/ccp/services/dormancy_recovery_service.py`
  - Runtime usage: suppress aggressive ritual mutations for dormant users and support recovery-mode routing.
- `src/ccp/services/engagement_feedback.py`
  - Runtime usage: pull resonance markers to support Relationship Engine framing.

#### Existing files intentionally not modified semantically
- `src/ccp/services/scorecard_emitter.py`
  - Remains the FR7 scorecard writer/validator.
  - This runtime may read scorecard outputs but must not redefine FR7 scorecard emission rules.
- `src/ccp/models/leadership_scorecard_models.py`
  - Remains the scorecard source model.
  - This spec adds CBCS runtime models separately in `cbcs_models.py` or a new adjacent model file.

#### API and routing integration
- `src/ccp/api/telegram_webhook.py`
  - Inline route target remains the ingestion surface for Telegram messages.
  - CBCS runtime must preserve the webhook's low-latency handling pattern and queue heavy work behind the existing routing boundary.
- `src/ccp/agents/vidye_router.py`
  - CBCS runtime is invoked as a routed capability, not a parallel webhook stack.

#### Data stores touched
- `receipt_chain`
  - Logs evidence extraction, diagnostic decision, downgrade interception, and final delivery decision.
- `person_registry`
  - Resolves client identity and coach boundary.
- `asset_registry`
  - Registers evidence-linked assets when a source audio or transcript artifact is referenced.
- CBCS / coach-local persisted artifacts
  - Existing habit, scorecard, dormancy, and resonance files continue to act as brownfield signal sources.
  <!-- UPDATED: Data store for SDA -->
  - `semantic_evolution_record` (New/Extended) for tracking longitudinal feedback loops and recursive patterns.
  <!-- /UPDATED -->

### 3.3 ADR-05 Primitives

#### Primary primitive: `EXP-PRG-004`
- Registry ID: `EXP-PRG-004`
- Registry name: `Long Loops for Habit Formation`
- Binding constraint for this spec:
  - A local failure must never erase the visible macro arc.
  - A downgrade notification must be accompanied by a 14-day or 30-day positive context signal when available.
  - The framing layer must convert short-loop failure into strategic-pause language.

#### Supporting primitive: `EXP-FBK-004`
- Registry ID: `EXP-FBK-004`
- Registry name: `Bring the Data Forward`
- Binding constraint for this spec:
  - The system must surface cumulative investment metrics, not just daily scores.
  - The Relationship Engine should cite hidden-progress statistics such as sessions completed, words spoken, streaks, or filler-word reduction when shaping recovery-safe feedback.

#### Primitive usage rule
- The Diagnostic Engine may compute raw regression.
- The Relationship Engine may expose only contextualized regression.
- The final user-facing payload must show either:
  - positive 14-day/30-day trend context, or
  - cumulative-investment proof plus non-regressive strategic framing when early-journey data is insufficient.

<!-- UPDATED: Adding SDA concepts block -->
### 3.3B Semantic Discernment Architecture (SDA) Rules
- **Existential Invariants & Representation Geometry**: The Relationship Engine must evaluate active invariants (e.g., status, identity, belonging) when crafting downgrade reframes, ensuring the representation geometry avoids fear-weighted or shame-coded constructs.
- **Emergent Contextual Invariants**: Framing must respect coach-specific or user-specific boundaries (e.g., "this user requires high-authority directness without status humiliation").
- **Directional Integrity Validation**: All high-stakes identity artifacts—specifically Sunday Postcards, User Cards, and escalation messages—must pass a `DirectionalIntegrityPolicy` check. If the check fails (i.e., detects a hard negative or representation drift), the artifact is blocked from dispatch and queued for rewrite.
- **Recursive Pattern & Feedback Loop Tracking**: The runtime must log behavioral repetitions to a `SemanticEvolutionRecord` to detect corrosive loops (e.g., recurring shame-to-authority cycles) across the challenge.
<!-- /UPDATED -->

### 3.4 CBAR Mandate Enforcement

| Mandate | Origin | Requirement | Enforcement in this spec |
|---|---|---|---|
| `Phase4-M07` | Epic 7, Story 7.1 | Any algorithm-driven downgrade in difficulty must be framed by the Relationship Engine against positive long-loop context | Diagnostic output is internal-only; all user-facing payloads must pass through `CBCSRelationshipEngineService.frame_notification(...)` |
| `Phase4-M07` | Epic 7, Story 7.1 | Raw downgrade messages are banned | `DiagnosticCapacityDecision` has no transport adapter to Telegram; only `RelationshipFramedNotification` may be dispatched |
| `Phase4-M07` | Epic 7, Story 7.1 | Macro progression must remain visible during setbacks | `RelationshipTrendContext` requires 14-day / 30-day trend computation plus cumulative metrics |
| `Phase4-M07` | Audit rewrite | Relationship Engine must intercept easier-drill assignments too, not just track downgrades | `interception_reason` enum includes both `capacity_track_downgrade` and `ritual_intensity_reduction` |

### 3.5 Technical Decisions

1. Physical service separation is mandatory.
Reason:
The prompt explicitly requires physically separate services. This prevents a future refactor from collapsing downgrade logic back into the Diagnostic Engine.

2. The Evidence Engine owns extraction, not messaging.
Reason:
`trait_scoring_engine.py`, `change_talk_vault.py`, and `spt_stage_engine.py` are analytics producers. Their outputs are useful only when mediated by downstream logic.

3. The Diagnostic Engine is internal-only.
Reason:
M-07 bans raw user exposure. The cleanest enforcement is architectural: diagnostic payloads are never valid notification payloads.

4. The Ritual Engine may lower tomorrow's difficulty but cannot explain it directly.
Reason:
The ritual mutation is operational truth; the explanation is a relationship-layer responsibility.

5. Relationship framing must retrieve both macro trend and cumulative investment.
Reason:
`EXP-PRG-004` covers long-loop framing and `EXP-FBK-004` covers proof-of-investment. Using both produces a resilient fallback during early or noisy data windows.

6. Early-journey users require a safe fallback path.
Reason:
`EXP-PRG-004` explicitly suppresses long-loop visuals on Day 1-3 when no meaningful arc exists. The system still must avoid raw regression language. Therefore, early-journey downgrades use strategic focus framing plus cumulative effort stats if available.

<!-- UPDATED: Adding SDA Technical Decisions -->
7. Directional Integrity validates identity artifacts before dispatch.
Reason:
Sunday Postcards and User Cards are high-gravity identity structures. Validating them against `DirectionalIntegrityPolicy` prevents deceptively close failures where the content sounds polished but subtly corrupts the user's semantic trajectory.

8. Longitudinal tracking must capture semantic feedback loops.
Reason:
Evaluating a single submission for coherence is insufficient. Storing `RecursivePattern` and `FeedbackLoop` data allows the Relationship Engine to recognize and interrupt long-term corrosive patterns.
<!-- /UPDATED -->

9. Telegram delivery remains routed through existing webhook + router infrastructure.
Reason:
The protocol requires extension of existing backend architecture, not a new transport subsystem.

## 4. Implementation Plan

### Phase 1: Model and service scaffolding
1. Add new Pydantic models for `DEP-CBCS-401` through `DEP-CBCS-406`.
2. Create `src/ccp/services/cbcs_evidence_engine.py`.
3. Create `src/ccp/services/cbcs_diagnostic_engine.py`.
4. Create `src/ccp/services/cbcs_ritual_engine.py`.
5. Create `src/ccp/services/cbcs_relationship_engine.py`.
6. Create `src/ccp/services/cbcs_four_engine_runtime.py`.
<!-- UPDATED: Adding SDA models to Phase 1 -->
7. Add SDA models `SemanticEvolutionRecord`, `DirectionalIntegrityReport`, and integration for `InvariantFieldPacket` / `RepresentationGeometryPacket`.
<!-- /UPDATED -->

### Phase 2: Evidence and diagnostic composition
8. Wrap `TraitScoringEngine.score_all_traits()` into a normalized evidence adapter.
9. Add Change Talk extraction and SPT classification enrichment to the evidence packet.
10. Read habit verification status through `ImplementationIntentionParser.parse_and_verify(...)` outputs where available.
11. Define `DiagnosticCapacityDecision` heuristics for:
   - track hold
   - track upgrade
   - track downgrade
   - ritual intensity reduction
   - journaling substitution
<!-- UPDATED: SDA Evidence integration -->
12. Append observed `RecursivePattern` and active `EmergentContextualInvariant` data to the evidence packet from longitudinal memory.
<!-- /UPDATED -->

### Phase 3: Ritual planning and recovery safeguards
13. Wire `LearningPathBuilder.recommend_next(...)` into ritual mutation planning.
14. Allow `DynamicJournalingEngine.generate(...)` as a reflection-mode fallback when repetition would be counterproductive.
15. Check `DormancyRecoveryService.classify_tier(...)` before aggressive drill escalation.
16. Generate draft ritual text through `RitualScheduler.generate_ritual(...)`.

### Phase 4: Relationship interception and long-loop framing
17. Build `RelationshipTrendContext` from 14-day and 30-day aggregates plus cumulative investment metrics.
18. Add `intercept_diagnostic_downgrade(...)` logic to capture:
   - previous vs new capacity track
   - previous vs new ritual intensity
   - macro trend delta
   - cumulative proof metrics
   <!-- UPDATED: SDA Interception tracking -->
   - feedback loop tracking (identifying if the user is stuck in an ongoing recursive failure loop).
   <!-- /UPDATED -->
19. Add `RitualResonance.get_resonance_enhancement(...)` support to soften delivery without self-promotional drift.
20. Ban any direct Telegram serialization of `DiagnosticCapacityDecision`.
<!-- UPDATED: SDA Directional Integrity -->
21. Implement `DirectionalIntegrityPolicy` validation hook for all generated Sunday Postcards, User Cards, and escalation messaging to ensure representation geometry alignment before finalization.
<!-- /UPDATED -->

### Phase 5: Runtime orchestration and API handoff
22. Add `CBCSFourEngineRuntimeService.process_submission(...)` as the single orchestration entrypoint.
23. Integrate it into `VidyeRouter` routing for CBCS-related voice/reflection flows.
24. Ensure inline runtime work returns a stable decision envelope quickly while heavier analytics persistence can complete asynchronously.
25. Log receipts for evidence extraction, diagnostic decision, ritual mutation, interception, and final dispatch.
<!-- UPDATED: SDA Semantic record flush -->
26. Flush updated `SemanticEvolutionRecord` (recursive patterns, loop history) asynchronously.
<!-- /UPDATED -->

### Phase 6: Hardening
27. Add explicit error codes for missing trend data, invalid coach scope, and blocked direct-diagnostic delivery attempts.
28. Add unit tests and integration tests aligned to existing CBCS / FR7 test patterns.
<!-- UPDATED: SDA Hardening -->
29. Add tests verifying `DirectionalIntegrityPolicy` rejections of hard-negative frames (e.g., shame-coded downgrade text).
<!-- /UPDATED -->

## 5. Primary Output Schema

The following models define the runtime handoff and enforce the interception boundary.

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from ccp.models.sda_models import (
    DirectionalIntegrityReport,
    SemanticEvolutionRecord,
    InvariantFieldPacket,
    RepresentationGeometryPacket,
    RecursivePattern,
    FeedbackLoop,
    EmergentContextualInvariant
)


class CBCSSubmissionKind(str, Enum):
    VOICE_NOTE = "voice_note"
    TEXT_REFLECTION = "text_reflection"
    JOURNAL_RESPONSE = "journal_response"


class CapacityTrack(str, Enum):
    RECOVERY = "recovery"
    FOUNDATION = "foundation"
    GROWTH = "growth"
    MOMENTUM = "momentum"
    PEAK = "peak"


class DiagnosticChangeType(str, Enum):
    HOLD = "hold"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    RITUAL_INTENSITY_REDUCTION = "ritual_intensity_reduction"
    REFLECTION_SUBSTITUTION = "reflection_substitution"


class RelationshipInterceptionReason(str, Enum):
    NONE = "none"
    CAPACITY_TRACK_DOWNGRADE = "capacity_track_downgrade"
    RITUAL_INTENSITY_REDUCTION = "ritual_intensity_reduction"
    EARLY_JOURNEY_SAFE_FRAMING = "early_journey_safe_framing"
    # <!-- UPDATED: Added SDA interception reasons -->
    CORROSIVE_LOOP_INTERRUPTION = "corrosive_loop_interruption"
    DIRECTIONAL_INTEGRITY_FAILURE = "directional_integrity_failure"
    # <!-- /UPDATED -->


class TrendWindowStatus(str, Enum):
    POSITIVE = "positive"
    FLAT = "flat"
    NEGATIVE = "negative"
    INSUFFICIENT = "insufficient"

# <!-- UPDATED: Added SDA enums and supporting objects -->
# Note: DirectionalIntegrityReport and IntegrityVerificationResult are imported from FR-ERA3-20

class SemanticDynamicsContext(BaseModel):
    active_recursive_patterns: list[RecursivePattern] = Field(default_factory=list)
    identified_feedback_loops: list[FeedbackLoop] = Field(default_factory=list)
    emergent_contextual_invariants: list[EmergentContextualInvariant] = Field(default_factory=list)
    invariant_field_packet: Optional[InvariantFieldPacket] = Field(default=None)
    representation_geometry_packet: Optional[RepresentationGeometryPacket] = Field(default=None)
# <!-- /UPDATED -->

class EvidenceMetric(BaseModel):
    metric_name: str = Field(..., min_length=1)
    current_value: float = Field(...)
    previous_value: Optional[float] = Field(default=None)
    delta_value: Optional[float] = Field(default=None)
    interpretation: str = Field(..., min_length=1)


class EvidenceCitation(BaseModel):
    source_system: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    excerpt: str = Field(..., min_length=1)


class CBCSEvidencePacket(BaseModel):
    evidence_packet_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    submission_kind: CBCSSubmissionKind = Field(...)
    generated_at: datetime = Field(...)
    trait_metrics: list[EvidenceMetric] = Field(default_factory=list)
    change_talk_summary: list[str] = Field(default_factory=list)
    spt_stage: Optional[int] = Field(default=None, ge=1, le=4)
    habit_verified: Optional[bool] = Field(default=None)
    citations: list[EvidenceCitation] = Field(default_factory=list)
    # <!-- UPDATED: Added SDA dynamics context -->
    semantic_dynamics: SemanticDynamicsContext = Field(default_factory=SemanticDynamicsContext)
    # <!-- /UPDATED -->


class DiagnosticCapacityDecision(BaseModel):
    decision_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    previous_track: CapacityTrack = Field(...)
    new_track: CapacityTrack = Field(...)
    change_type: DiagnosticChangeType = Field(...)
    rationale: str = Field(..., min_length=1)
    weaker_signal_names: list[str] = Field(default_factory=list)
    stronger_signal_names: list[str] = Field(default_factory=list)
    requires_relationship_intercept: bool = Field(...)
    created_at: datetime = Field(...)


class RitualAdjustmentPlan(BaseModel):
    plan_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    ritual_type: str = Field(..., min_length=1)
    intensity_level: int = Field(..., ge=1, le=5)
    replaced_with_reflection: bool = Field(default=False)
    learning_path_reason: str = Field(..., min_length=1)
    draft_prompt: str = Field(..., min_length=1)
    scheduled_for_iso: Optional[datetime] = Field(default=None)


class MacroTrendSnapshot(BaseModel):
    window_days: int = Field(..., ge=1)
    status: TrendWindowStatus = Field(...)
    headline_metric: str = Field(..., min_length=1)
    positive_delta_label: Optional[str] = Field(default=None)
    supporting_sentence: str = Field(..., min_length=1)


class CumulativeInvestmentStats(BaseModel):
    total_sessions_completed: int = Field(..., ge=0)
    total_words_spoken: int = Field(..., ge=0)
    current_streak_days: int = Field(..., ge=0)
    strongest_hidden_gain: Optional[str] = Field(default=None)


class RelationshipTrendContext(BaseModel):
    context_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    fourteen_day: MacroTrendSnapshot = Field(...)
    thirty_day: MacroTrendSnapshot = Field(...)
    cumulative_stats: CumulativeInvestmentStats = Field(...)
    resonance_marker_hint: Optional[str] = Field(default=None)
    # <!-- UPDATED: Including existential context for framing decisions -->
    dominant_invariant_field: Optional[str] = Field(default=None)
    # <!-- /UPDATED -->


class RelationshipFramedNotification(BaseModel):
    notification_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    interception_reason: RelationshipInterceptionReason = Field(...)
    safe_headline: str = Field(..., min_length=1, max_length=180)
    safe_body: str = Field(..., min_length=1, max_length=1200)
    visible_macro_metric: Optional[str] = Field(default=None)
    visible_cumulative_metric: Optional[str] = Field(default=None)
    dispatch_channel: str = Field(..., min_length=1)
    # <!-- UPDATED: Linking the SDA integrity report -->
    integrity_report: Optional[DirectionalIntegrityReport] = Field(default=None)
    # <!-- /UPDATED -->
    created_at: datetime = Field(...)


class CBCSRuntimeSession(BaseModel):
    session_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    submission_kind: CBCSSubmissionKind = Field(...)
    evidence_packet: CBCSEvidencePacket = Field(...)
    diagnostic_decision: DiagnosticCapacityDecision = Field(...)
    ritual_plan: RitualAdjustmentPlan = Field(...)
    relationship_context: RelationshipTrendContext = Field(...)
    user_notification: RelationshipFramedNotification = Field(...)
```

### Schema rules
- `DiagnosticCapacityDecision` is never sent directly to Telegram.
- `RelationshipFramedNotification` is the only schema permitted for user-facing runtime delivery.
- `RelationshipTrendContext` must be computed even when the final message does not expose every field.
- No `Any` fields are permitted.
<!-- UPDATED: SDA Schema Rule -->
- Identity artifacts (Sunday Postcards, User Cards, escalations) encapsulated within or derived from `RelationshipFramedNotification` MUST pass a populated `integrity_report` with `verification_status == PASS` before delivery.
<!-- /UPDATED -->

## 6. Backward Compatibility Fallback

### Brownfield compatibility rules
1. If FR61 trait scoring is unavailable for the current submission, the runtime must fail closed and preserve the existing CBCS delivery path without generating a fake diagnostic decision.
2. If Change Talk, SPT, or habit verification data is unavailable, the Evidence Engine may emit a partial packet with explicit missing-signal flags; it must not invent values.
3. If 30-day data is unavailable but 14-day data is positive, the Relationship Engine may frame against the 14-day snapshot only.
4. If both 14-day and 30-day windows are `INSUFFICIENT`, the Relationship Engine must:
   - suppress all regression language,
   - avoid numerical downgrade disclosure,
   - surface strategic-focus language plus cumulative investment evidence when available.
5. If cumulative investment metrics are also empty because the user is truly new, the system may still assign an easier ritual internally, but the message must describe the next drill as calibration or foundation work rather than reduction.
6. If Relationship Engine framing fails entirely, the notification is not dispatched. The runtime logs `RELATIONSHIP_FRAME_BLOCKED` and returns an operator-safe internal hold state.
<!-- UPDATED: SDA Fallback Rules -->
7. If the `DirectionalIntegrityPolicy` validation service is temporarily unavailable, Sunday Postcards and User Cards must drop to a neutral, metric-only fallback state with no identity commentary appended.
8. If an `EmergentContextualInvariant` conflicts directly with a universal existential invariant, the universal invariant takes precedence during framing generation.
<!-- /UPDATED -->

### Explicit bans
- No direct `DiagnosticCapacityDecision` serialization to Telegram.
- No fallback to a raw numeric message such as "Your score dropped, so tomorrow will be easier."
- No monolithic "CBCS engine" class that merges all four responsibilities into a single file.

## 7. Tasks

### Service creation
- [ ] Create `CBCSEvidenceEngineService`.
- [ ] Create `CBCSDiagnosticEngineService`.
- [ ] Create `CBCSRitualEngineService`.
- [ ] Create `CBCSRelationshipEngineService`.
- [ ] Create `CBCSFourEngineRuntimeService`.

### Models
- [ ] Add `DEP-CBCS-401` through `DEP-CBCS-406` models in a CBCS model module.
- [ ] Add enums for capacity track, diagnostic change type, interception reason, and trend status.
<!-- UPDATED: SDA Model Tasks -->
- [ ] Import `DirectionalIntegrityReport` and `SemanticEvolutionRecord` from FR-ERA3-20.
- [ ] Add `SemanticDynamicsContext` model utilizing FR-ERA3-23 objects.
<!-- /UPDATED -->

### Evidence Engine
- [ ] Adapt `TraitScoringEngine.score_all_traits()` output into `CBCSEvidencePacket`.
- [ ] Integrate `ChangeTalkVault.extract(...)`.
- [ ] Integrate `SPTStageEngine.classify_client(...)`.
- [ ] Read habit-verification state via existing habit tracker artifacts.
<!-- UPDATED: SDA Evidence Task -->
- [ ] Read longitudinal `RecursivePattern` and `FeedbackLoop` states from `SemanticEvolutionRecord`.
<!-- /UPDATED -->

### Diagnostic Engine
- [ ] Implement explicit track-comparison logic.
- [ ] Implement easier-drill detection separate from track downgrade detection.
- [ ] Emit `requires_relationship_intercept=True` for both downgrade categories.

### Ritual Engine
- [ ] Integrate `LearningPathBuilder.recommend_next(...)`.
- [ ] Integrate `DynamicJournalingEngine.generate(...)` fallback.
- [ ] Integrate dormancy suppression via `DormancyRecoveryService`.
- [ ] Generate ritual copy via `RitualScheduler.generate_ritual(...)`.

### Relationship Engine
- [ ] Build 14-day and 30-day trend aggregators.
- [ ] Build cumulative investment stats loader.
- [ ] Add resonance-hint enrichment via `RitualResonance.get_resonance_enhancement(...)`.
- [ ] Implement safe-headline / safe-body framing templates.
- [ ] Add hard block against raw downgrade dispatch.
<!-- UPDATED: SDA Relationship Tasks -->
- [ ] Inject `EmergentContextualInvariant` data into template selection bounds.
- [ ] Execute `DirectionalIntegrityPolicy` check on generated Sunday Postcards, User Cards, and escalation messages.
<!-- /UPDATED -->

### Orchestration and transport
- [ ] Wire runtime invocation into `VidyeRouter`.
- [ ] Preserve `telegram_webhook.py` response discipline.
- [ ] Add receipt-chain logging at every stage.

### Quality hardening
- [ ] Add unit tests for intercept logic and trend fallback.
- [ ] Add integration tests for full routed runtime behavior.
<!-- UPDATED: SDA Hardening Task -->
- [ ] Add tests for `DirectionalIntegrityReport` validation failures.
<!-- /UPDATED -->

## 8. Acceptance Criteria

### AC1: Evidence routing produces a complete internal runtime session
- Given a CBCS voice-note submission with valid transcript and coach scope
- When `CBCSFourEngineRuntimeService.process_submission(...)` runs
- Then it returns a `CBCSRuntimeSession` containing:
  - `evidence_packet`
  - `diagnostic_decision`
  - `ritual_plan`
  - `relationship_context`
  - `user_notification`
- And `user_notification` is the only user-facing payload exported from the session
- FAILURE EXAMPLE:
  - The runtime emits a score delta and a new track but never creates a relationship context, so the webhook sends a partially internal object to the user.
- Mandate:
  - `Phase4-M07`

### AC2: Capacity-track downgrades are intercepted before delivery
- Given the Diagnostic Engine moves a user from `growth` to `foundation`
- When the runtime prepares the outbound message
- Then `requires_relationship_intercept=True`
- And `RelationshipFramedNotification.interception_reason == capacity_track_downgrade`
- And no transport adapter may access the raw diagnostic message
- FAILURE EXAMPLE:
  - The Telegram message says "You were downgraded to Foundation after today's result."
- Mandate:
  - `Phase4-M07`

### AC3: Easier-drill assignments are treated as downgrade-class events
- Given the capacity track stays the same but the Ritual Engine reduces intensity from level 4 to level 2
- When the session is framed for delivery
- Then the Relationship Engine must still intercept it as `ritual_intensity_reduction`
- And the visible message must describe the change as strategic consolidation rather than regression
- FAILURE EXAMPLE:
  - The system keeps the track label unchanged and therefore skips the intercept, sending "Tomorrow's drill is easier because you struggled."
- Mandate:
  - `Phase4-M07`

### AC4: Long-loop context must be visible when positive trend data exists
- Given a downgrade event and a positive 14-day or 30-day trend snapshot
- When the Relationship Engine builds the final message
- Then `visible_macro_metric` must be populated with concrete positive context
- And the body must include an identity-safe explanation of the temporary step-back
- FAILURE EXAMPLE:
  - The system has a positive 30-day delta in storage but still sends only the easier-drill instruction with no macro framing.
- Mandate:
  - `Phase4-M07`, `EXP-PRG-004`

### AC5: Early-journey users never receive raw regression language
- Given the user has insufficient 14-day and 30-day data
- When a downgrade-class event occurs
- Then the runtime may adjust the internal ritual plan
- But the user-facing message must use strategic calibration language and must not expose explicit "going backward" phrasing
- FAILURE EXAMPLE:
  - A Day-2 user receives "Your score fell today, so we are lowering difficulty."
- Mandate:
  - `Phase4-M07`, `EXP-PRG-004`

### AC6: Cumulative investment proof is surfaced when macro trend is thin or noisy
- Given the macro window is insufficient or flat but cumulative activity data exists
- When the Relationship Engine frames the message
- Then `visible_cumulative_metric` must be populated with an investment proof such as sessions completed, words spoken, or streak continuity
- FAILURE EXAMPLE:
  - The system knows the user has completed 18 sessions and spoken 9,400 words but sends a generic "keep going" note with no evidence of accumulated progress.
- Mandate:
  - `EXP-FBK-004`

### AC7: Relationship framing failure blocks dispatch
- Given the Diagnostic Engine emits a downgrade-class decision
- And the Relationship Engine cannot build a safe framed notification
- When dispatch is attempted
- Then the runtime must block user delivery, log a receipt, and return an internal hold status
- FAILURE EXAMPLE:
  - Relationship framing crashes and the transport layer falls back to the raw diagnostic string.
- Mandate:
  - `Phase4-M07`

<!-- UPDATED: Added SDA Acceptance Criteria -->
### AC8: Identity Artifacts Must Pass Directional Integrity Validation
- Given the Relationship Engine generates a Sunday Postcard, User Card, or escalation message
- When the system prepares for final serialization
- Then it must run a `DirectionalIntegrityPolicy` check on the artifact
- And if the check returns `FAIL_REPRESENTATION_DRIFT` or `FAIL_HARD_NEGATIVE` (triggered when `invariant_alignment_score < 0.85`)
- Then the artifact must be blocked from dispatch
- FAILURE EXAMPLE:
  - A Sunday Postcard is generated using a shame-coded authority representation and is sent to the user because it passed spellcheck.
- Mandate:
  - `SDA-Integrity-Gate`

### AC9: Corrosive Feedback Loops Trigger Automatic Interception
- Given the Evidence Engine detects a recurring `RecursivePattern` linked to a negative `FeedbackLoop` (e.g., repeating failure followed by self-deprecating reflection)
- When the runtime evaluates the next intervention
- Then the Relationship Engine must intercept the next delivery with `interception_reason == corrosive_loop_interruption`
- And the notification body must explicitly break the expected loop pattern
- FAILURE EXAMPLE:
  - A user constantly apologizes in voice notes and receives the exact same drill structure each time, reinforcing the failure identity loop.
- Mandate:
  - `SDA-Recursive-Discernment`
<!-- /UPDATED -->

## 9. Dependencies

### Internal services
- `trait_scoring_engine.py`
- `change_talk_vault.py`
- `spt_stage_engine.py`
- `habit_architecture.py`
- `learning_path_builder.py`
- `dynamic_journaling_engine.py`
- `ritual_scheduler.py`
- `ritual_resonance.py`
- `dormancy_recovery_service.py`
- `engagement_feedback.py`
- `vidye_router.py`
- `telegram_webhook.py`
- `receipt_chain.py`
<!-- UPDATED: SDA Dependency -->
- `directional_integrity_validator.py` (assumed new SDA infrastructure)
<!-- /UPDATED -->

### Internal models / stores
- `cbcs_models.py`
- `leadership_scorecard_models.py`
- `person_registry`
- `asset_registry`
- `receipt_chain`
<!-- UPDATED: SDA Store Dependency -->
- `semantic_evolution_record`
<!-- /UPDATED -->

### External/runtime dependencies
- Telegram Bot API transport already used by the platform
- Existing LLM provider dependency already used by ritual/resonance generators
- Supabase / coach-local persistence already used by the brownfield CBCS services

### Dependency constraints
- No dependency may bypass `CBCSRelationshipEngineService` for downgrade-class notifications.
- No dependency may introduce cross-coach trend aggregation; all trend context is single-tenant.

## 10. Testing Strategy

### Unit tests

1. `test_cbcs_four_engine_marks_track_downgrade_for_intercept`
- Build a `DiagnosticCapacityDecision` from `growth -> foundation`.
- Assert `requires_relationship_intercept=True`.
- Assert no direct notification serializer accepts the raw decision object.

2. `test_cbcs_relationship_engine_uses_macro_trend_when_positive`
- Provide a positive 14-day snapshot and a downgrade-class event.
- Assert `visible_macro_metric` is populated.
- Assert the final copy contains strategic framing language and excludes explicit regression phrasing.

3. `test_cbcs_relationship_engine_falls_back_to_cumulative_investment`
- Provide insufficient macro windows but non-zero cumulative stats.
- Assert `visible_cumulative_metric` is set.
- Assert the body still avoids raw regression language.

4. `test_cbcs_relationship_engine_blocks_dispatch_when_unframed`
- Force framing construction failure.
- Assert return status is internal hold.
- Assert a receipt is logged with a framing-block code.

<!-- UPDATED: SDA Unit Tests -->
5. `test_cbcs_directional_integrity_blocks_hard_negative_postcard`
- Provide a Sunday Postcard containing fear-weighted representation geometry.
- Assert `integrity_report.verification_status == FAIL_HARD_NEGATIVE`.
- Assert the runtime blocks dispatch.

6. `test_cbcs_evidence_engine_loads_recursive_patterns`
- Mock `SemanticEvolutionRecord` returning an active corrosive loop.
- Assert the `CBCSEvidencePacket` includes this in `semantic_dynamics`.
<!-- /UPDATED -->

### Integration tests

1. `test_cbcs_runtime_voice_note_downgrade_is_relationship_framed`
- Pattern after `test_fr7_leadership_scorecard.py`.
- Feed a realistic evidence packet with declining short-loop metrics and positive 14-day macro trend.
- Assert the runtime session is complete.
- Assert the raw diagnostic decision is internal-only.
- Assert the final outbound message includes long-loop framing.

2. `test_cbcs_runtime_easier_ritual_same_track_still_intercepts`
- Pattern after `test_cbcs09_habit_architecture.py`.
- Keep the track stable but reduce ritual intensity.
- Assert `interception_reason == ritual_intensity_reduction`.
- Assert the user-facing message does not use "easier because you failed" language.

3. `test_cbcs_runtime_day2_user_uses_safe_calibration_fallback`
- Simulate an early-journey user with no 14/30-day windows.
- Assert the runtime still adjusts tomorrow's plan internally.
- Assert the final notification uses calibration/foundation phrasing and no raw regression disclosure.

### Non-goals for this test suite
- Re-scoring FR61 trait math itself.
- Re-testing Telegram transport mechanics already owned by existing webhook coverage.
- Re-testing FR7 scorecard emission rules already covered by `test_fr7_leadership_scorecard.py`.

### Verification notes
- Follow the existing integration-test style:
  - local helper builders
  - exact error-code assertions
  - coach-scope validation
  - receipt side-effect checks
- Do not write vague snapshot tests for wording. Assert presence of required framing artifacts and absence of banned regression phrases.
<!-- UPDATED: SDA Verification Note -->
- For SDA integration, test the structural presence of `DirectionalIntegrityReport` evaluation boundaries, rather than evaluating live LLM semantic discernment in unit tests.
<!-- /UPDATED -->

