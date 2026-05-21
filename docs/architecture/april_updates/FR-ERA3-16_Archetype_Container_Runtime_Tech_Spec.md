# Tech-Spec: FR-ERA3-16 - Archetype Container Runtime
**Created:** 2026-05-12
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 4 - Pipelines & Engines
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2 requires extension of the existing FastAPI, Supabase, service, and model
                      layers instead of greenfield invention. Section 3 requires explicit backend mapping before
                      introducing new runtime services. Section 4 requires the 10-section format. The protocol's
                      CBAR note requires named mandate enforcement in Section 3, not implied compliance.
2. PRD LOADED:        PRD-02 exact runtime law: "CCF should therefore treat archetypes as first-class runtime
                      containers." PRD-02 exact sequence: "signal -> coach reaction -> primitive coalition ->
                      archetype container -> JIT script contract -> render blueprint". Brownfield exact FR
                      definition: "Elevate Archetypes (e.g., Achievement Story, Myth Debunk, Observational Humor)
                      into first-class runtime containers. The compiler must structure the meaning into these
                      archetypes *before* any downstream media format (carousel, video) is selected."
3. EPIC LOADED:       Phase 4 Story 5.1 first AC: "Given a validated Primitive Coalition Signature, When it is
                      processed by the runtime, Then it generates a specific Archetype Container that dictates the
                      narrative pacing and logic, passing this as the `CCFRoutingRecommendation` to the CMF, And
                      if the Anti-Centroid Validator rejects the take, the failure response payload must return
                      the exact transcript sentences that triggered the centroid collapse, along with specific
                      coaching feedback ..., And the coach is re-routed to the voice recording modal with the
                      specific failing sentences highlighted as a re-recording prompt."
4. CBAR LOADED:       Phase4-M05 confirmed from the Phase 4 audit. Exact rewrite demand: the
                      `CCFRoutingRecommendation` failure state must return exact transcript sentences, quantified
                      similarity, and a specific coaching fix. Generic "too generic" rejection text is banned.
                      The audit also states the coach must not feel judged by a black box.
5. PRIMITIVES:        `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
                      `experience_primitive_id: "EXP-FRC-006"` / `canonical_name: "Hypnosedation Reframing"`
                      `experience_primitive_id: "EXP-TRS-004"` / `canonical_name: "Epic Meaning Framing (The
                      Crusade Narrative)"`
6. BACKEND:           `src/ccp/services/content_machine.py` - `async def process_session(self, session_report:
                      dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
                      `src/ccp/services/research_synthesis_protocol.py` - `def execute(self, step_input:
                      Step35Input) -> Step35Result`
                      `src/ccp/services/psych_routing_engine.py` - `def resolve(self, mood_context:
                      MoodContextMap, maturity_profile: AudienceMaturityProfile) -> PsychologicalClassification`
                      `src/ccp/services/tiar_adapter.py` - `def inject_upstream(self, coach_id: str,
                      content_output_id: str = "upstream", tribe_id: str = "default", simulate_timeout: bool =
                      False) -> TIARInjectionResult`
                      `src/ccp/services/semantic_affinity_guard.py` - `def evaluate(self, batch_metadata:
                      BatchMetadata, pain_map: PainMapInput) -> SemanticAffinityClearance`
7. TESTS:             `tests/integration/test_fr18_psych_routing.py` and
                      `tests/integration/test_fr19_semantic_affinity.py` both use helper builders, scenario-
                      oriented test classes, explicit acceptance-criterion wording in docstrings, deterministic
                      field assertions, fallback-path checks, and named failure-state verification. Section 10
                      follows that pattern.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P4_S25_FR-ERA3-16_Archetype_Container_Runtime.md` | 2026-05-12 | Assignment prompt, M-05 payload demand, and audit checklist |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-12 | Required backend mapping, schema extension points, and spec structure |
| 3 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Story 5.1 first AC and mandate definition |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | M-05 rewrite demand and hallucination purge context |
| 5 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | v6.0, 2026-05-06 | Archetype doctrine, anti-centroid law, and brownfield requirements |
| 6 | `docs/architecture/april_updates/FR-ERA3-15_Trigger_First_Execution_Guard_Tech_Spec.md` | 2026-05-11 | Upstream capture handoff contract and reroute expectations |
| 7 | `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec.md` | 2026-05-11 | Downstream CMF contract and render-boundary expectations |
| 8 | `docs/architecture/april_updates/FR-ERA3-13_Four_Surface_Async_Skill_Ladder_Tech_Spec.md` | 2026-05-11 | Existing inline routing style and packet-first state patterns |
| 9 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Verified governing primitive for rejection payload quality |
| 10 | `primitives/experience/friction_ability/EXP-FRC-006.yaml` | Codified registry | Verified supporting primitive for non-shaming re-record flow |
| 11 | `primitives/experience/trust_branding/EXP-TRS-004.yaml` | Codified registry | Verified supporting primitive for preserving emotional intensity downstream |
| 12 | `src/ccp/services/content_machine.py` | Existing service | Current compilation boundary that will consume runtime output |
| 13 | `src/ccp/services/research_synthesis_protocol.py` | Existing service | Existing deterministic evidence-conflict pass reused before container commitment |
| 14 | `src/ccp/services/psych_routing_engine.py` | Existing service | Existing deterministic mood-classification engine reused for container shaping |
| 15 | `src/ccp/services/semantic_affinity_guard.py` | Existing service | Existing C-06 pain-domain guard that must remain separate from anti-centroid logic |
| 16 | `src/ccp/services/tiar_adapter.py` | Existing service | Existing dual-stage validation pattern used as a design precedent for upstream/downstream checks |
| 17 | `src/ccp/services/trigger_archetype_mapper.py` | Existing service | Existing archetype mapping precedent and naming vocabulary |
| 18 | `src/ccp/pipelines/container_module_pipeline.py` | Existing pipeline | Existing Step 6 "container module" boundary that must not be overloaded by this runtime |
| 19 | `src/ccp/models/container_module_models.py` | Existing models | Existing naming collision and DEP-ID precedent to avoid duplicating |
| 20 | `src/ccp/api/main.py` | 1.0.0 | FastAPI registration point |
| 21 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit trail for compile, reject, and reroute outcomes |
| 22 | `src/ccp/scripts/setup_supabase.py` | Current | Schema bootstrap extension point |
| 23 | `tests/integration/test_fr18_psych_routing.py` | Existing | Deterministic scenario-based test pattern |
| 24 | `tests/integration/test_fr19_semantic_affinity.py` | Existing | Guard-style acceptance/fallback test pattern |

## 2. Overview

### 2.1 Problem Statement

PRD-02 already defines the correct runtime order:

`signal -> coach reaction -> primitive coalition -> archetype container -> JIT script contract -> render blueprint`

The current codebase still lacks the actual backend layer that turns a validated reaction plus coalition into a typed archetype container before CMF formatting begins.

That missing layer causes five concrete failures:

- the system can still drift from reaction meaning straight into format or content-family guesses without locking the deeper persuasion geometry
- anti-centroid enforcement remains diffuse instead of being attached to the exact handoff where conviction is most likely to be flattened
- downstream CMF can receive a payload that is semantically plausible but psychologically under-specified
- coaches can be rejected without sentence-level evidence, quantified similarity, and a concrete recovery path
- the existing `ContainerModulePipeline` naming can be confused with this runtime even though it solves an older audience/trigger matching problem

Story 5.1 is explicitly about closing that gap. The runtime must produce a specific archetype container or a fully actionable rejection. There is no acceptable middle state where the system says "generic" and leaves the coach stranded.

### 2.2 Solution

This spec introduces a new backend service, `ArchetypeContainerRuntimeService`, that sits between `CoachResponseCapture` and downstream CMF.

The service performs six deterministic jobs:

1. validate compile inputs and evidence context
2. run pre-container conflict checks using the existing research synthesis boundary when CRAL/evidence data is present
3. run a sentence-level Anti-Centroid Validator that measures charge loss without reusing `semantic_affinity_guard.py`
4. either emit a rejection-grade `CCFRoutingRecommendation` with exact failing sentences, quantified similarity, and a coaching fix
5. or select a concrete archetype container through a deterministic selection matrix and build a typed container manifest
6. emit a success-grade `CCFRoutingRecommendation` for CMF and downstream script assembly

This is not a new LLM router and not a rewrite of existing C-06 pain-domain safety logic. It is the missing runtime containerization layer for PRD-02.

### 2.3 Scope

**In scope:**

- new `ArchetypeContainerRuntimeService`
- typed compile request, sentence audit, container manifest, and routing recommendation models
- deterministic archetype selection matrix
- sentence-level anti-centroid validation and exact rejection payload
- re-record prompt generation and upstream trigger-guard bridge contract
- CMF handoff contract for successful containers
- Supabase persistence for runtime sessions, manifests, and rejection audits
- FastAPI routes for compile, inspect, and re-record preparation
- receipt logging and deterministic fallback behavior

**Out of scope:**

- replacing `ContentMachinePipeline.process_session(...)`
- replacing `PsychVariableMatrix.resolve(...)`
- replacing `SemanticAffinityGuard.evaluate(...)`
- redesigning `TIARAdapter` or visual noun validation
- implementing full JIT script generation
- implementing CMF rendering itself
- creating the actual Telegram modal UI

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Payload / Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-ACR-001 | `CoachResponseCapturePacket` | FR-ERA3-15 | Upstream signal containing transcript, asset ID, and trigger metadata |
| DEP-ACR-002 | `CoalitionInputs` | PRD-02 | Validated multi-source context driving container selection |
| DEP-ACR-003 | `SentenceAuditRecord` | FR-ERA3-16 | Granular scoring ledger tracking hedge hits and similarity bands per sentence |
| DEP-ACR-004 | `ContainerIntensityProfile` | Epic 5 | The narrative pacing and emotional job assigned to the container |
| DEP-ACR-005 | `ArchetypeContainerManifest` | FR-ERA3-16 | The compiled psychological container preserving narrative pacing and logic |
| DEP-ACR-006 | `ActionableRejectionPayload` | Phase4-M05 | Failure response containing specific failing sentences and coaching fixes |
| DEP-ACR-007 | `CCFRoutingRecommendation` | FR-ERA3-16 | The canonical routing envelope passed to downstream CMF or upstream execution guard |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `content_machine.py` | `src/ccp/services/content_machine.py` | Downstream consumer of success-grade routing output. This spec does not rewrite it; it inserts a containerization gate before content compilation proceeds. |
| `research_synthesis_protocol.py` | `src/ccp/services/research_synthesis_protocol.py` | Reused to clear or block evidence conflicts before the runtime commits to an archetype. Type 3 authenticity conflicts remain terminal here too. |
| `psych_routing_engine.py` | `src/ccp/services/psych_routing_engine.py` | Reused to shape container mood behavior and pacing hints through deterministic mood classification. |
| `semantic_affinity_guard.py` | `src/ccp/services/semantic_affinity_guard.py` | Explicitly not reused as the anti-centroid validator. Its job stays limited to C-06 pain-domain affinity for mood-safe batch compilation. |
| `tiar_adapter.py` | `src/ccp/services/tiar_adapter.py` | Used only as a design precedent for staged validation and audit persistence. No noun registry dependency is added here. |
| `trigger_archetype_mapper.py` | `src/ccp/services/trigger_archetype_mapper.py` | Supplies archetype vocabulary precedent and TTT-threshold selection style. The new runtime may reuse names but not the same emotional-state-only mapping. |
| `container_module_pipeline.py` | `src/ccp/pipelines/container_module_pipeline.py` | Existing Step 6 audience/trigger matching pipeline is left intact. This spec must not overload that class or its naming domain. |
| `container_module_models.py` | `src/ccp/models/container_module_models.py` | Existing "container module" models are not the right schema for FR-ERA3-16. A separate `archetype_container_runtime_models.py` file is required. |
| `main.py` | `src/ccp/api/main.py` | Registers new runtime routes. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs sentence audit, archetype selection, rejection payload, and reroute preparation. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Adds runtime persistence tables. |
| `FR-ERA3-15` spec | `docs/architecture/april_updates/FR-ERA3-15_Trigger_First_Execution_Guard_Tech_Spec.md` | Upstream handoff contract for `CoachResponseCapturePacket`, resume token, and reroute behavior. |
| `FR-ERA3-12` spec | `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec.md` | Downstream contract for narrative pacing, render hints, and emotional intensity preservation. |

### 3.3 Primitives

| Primitive ID | Name | Why It Governs This Spec | Runtime Enforcement |
|---|---|---|---|
| `EXP-FBK-001` | `RIM Feedback Discipline` | Story 5.1 explicitly requires exact, immediate, meaningful rejection feedback. | Rejections must include sentence evidence, similarity score, and coaching fix in the first payload. |
| `EXP-FRC-006` | `Hypnosedation Reframing` | Re-record loops must not feel like punishment or a dead wall. | Rejection payload includes a recovery-oriented voice prompt and highlighted retry segment, not a vague halt. |
| `EXP-TRS-004` | `Epic Meaning Framing (The Crusade Narrative)` | Archetype selection exists to preserve emotional weight before format. | Success manifests carry intensity and pacing directives so downstream CMF cannot flatten the message. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Story | Enforcement in This Spec |
|---|---|---|
| `Phase4-M05 - The Actionable Rejection Rule` | Story 5.1 | `AntiCentroidValidator` must emit `failing_sentence_ids`, `failing_sentences`, `similarity_score`, `similarity_band`, `collapse_reasons`, `coaching_fix`, and `rerecord_prompt`. Generic string-only rejections are invalid schema states. |
| `Phase4-M04 - The Frictionless Block Rule` | Story 4.1 dependency | Rejection payload includes `trigger_guard_reroute` metadata so the upstream execution guard can reopen voice capture without extra navigation. |
| `Phase4-M02 - The Cinematic Meaning Rule` | Story 2.1 dependency | Success manifests include `intensity_profile`, `narrative_arc`, and `render_authority_hints` so CMF receives preserved meaning rather than a bland format guess. |

### 3.5 Technical Decisions

| Decision | Rationale | Consequence |
|---|---|---|
| Use a new file family named `archetype_container_runtime_*` | `container_module_*` already means Step 6 audience/trigger matching. Reusing the name would create architectural ambiguity. | No edits rename the older Step 6 pipeline. New runtime stays clearly isolated. |
| Keep anti-centroid validation separate from `semantic_affinity_guard.py` | C-06 evaluates content-domain proximity to pain maps. Story 5.1 needs sentence-level coach-specific genericness detection. These are different mathematical questions. | No reuse-by-analogy. A new validator service is required. |
| Make `CCFRoutingRecommendation` the canonical output object | PRD-02 already names it as the routing envelope between coalition logic and downstream systems. | Both success and rejection variants must serialize through the same top-level type. |
| Run evidence conflict checks before archetype selection | Archetype commitment on contradictory evidence would lock invalid meaning into a strong container. | `ResearchSynthesisProtocol` is an upstream precondition whenever evidence bundles are present. |
| Use deterministic archetype selection, not open-ended generation | The runtime is a compiler boundary, not a creative free-for-all. | Archetype choices come from explicit matrices and thresholds. |
| Reject with sentence IDs tied to stable offsets | The prompt specifically requires exact transcript sentences. | Sentence tokenization must be persisted so UI/Telegram surfaces can highlight the right lines consistently. |
| Support `ARC-COMP` only for multi-source payloads | PRD-02 gives `ARC-COMP` explicit structural invariants including minimum 3 sources. | Single-take reactions cannot be mislabeled as compilations. |

## 4. Implementation Plan

### Phase 1 - Runtime Boundaries and Persistence

1. Create `src/ccp/models/archetype_container_runtime_models.py`.
2. Add `ArchetypeRuntimeCompileRequest`, `ArchetypeContainerManifest`, `CCFRoutingRecommendation`, and rejection payload models.
3. Add `ArchetypeChoice`, `SentenceAuditRecord`, `SimilarityBand`, and `ContainerIntensityProfile` enums/models.
4. Extend `src/ccp/scripts/setup_supabase.py` with new runtime tables.
5. Add repository methods in a new `ArchetypeRuntimeRepository`.
6. Register new routes in `src/ccp/api/main.py`.

### Phase 2 - Validation and Selection Core

7. Implement `SentenceLedgerBuilder` with deterministic sentence splitting and offset capture.
8. Implement `AntiCentroidValidator` with sentence-level similarity scoring and hedge-pattern detection. Rejection triggers deterministically when any sentence `similarity_score` crosses the exact numeric threshold of `>= 0.75`, placing it in the terminal `SimilarityBand`.
9. Implement `EvidenceConflictGateBridge` that wraps `ResearchSynthesisProtocol.execute(...)`.
10. Implement `ArchetypeContractRegistry` as a typed in-code registry of supported contracts.
11. Implement `ArchetypeSelectionMatrix` using coalition, mood, stance, and source-count inputs. The matrix maps the `intended_business_job` to populate `downstream_family_targets`, and maps the selected archetype invariants to populate `authorized_render_targets` in the manifest.
12. Add explicit guards that prevent `ARC-COMP` when fewer than 3 source reactions exist.

### Phase 3 - Upstream and Downstream Bridges

13. Implement `TriggerGuardBridge` to accept `CoachResponseCapturePacket` and emit reroute metadata on rejection.
14. Implement `CMFRecommendationBridge` that packages success manifests for the CMF boundary.
15. Add optional `PsychologicalClassification` enrichment using `PsychVariableMatrix.resolve(...)`.
16. Attach `ContentMachinePipeline` integration so successful container manifests can move into downstream compilation safely.

### Phase 4 - Auditing, Fallbacks, and Verification

17. Write receipt-chain entries for compile start, evidence-clear, sentence-audit, rejection, container-select, and CMF-hand-off.
18. Implement fallback states for missing CRAL, missing mood packet, and transient persistence failure.
19. Add unit tests for sentence segmentation, archetype selection, and rejection payload shape.
20. Add integration tests for successful compile, actionable rejection, and trigger-guard reroute loops.

## 5. Schema

### 5.1 New Model File

Create:

`src/ccp/models/archetype_container_runtime_models.py`

### 5.2 Pydantic v2 Models

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RuntimeStatus(str, Enum):
    COMPILED = "compiled"
    REJECTED_ACTIONABLE = "rejected_actionable"
    BLOCKED_EVIDENCE_CONFLICT = "blocked_evidence_conflict"
    PENDING_RERECORD = "pending_rerecord"


class SimilarityBand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    TERMINAL = "terminal"


class ArchetypeChoice(str, Enum):
    ARC_MYTH_DEBUNK = "ARC-MYTH-DEBUNK"
    ARC_ACHIEVEMENT_STORY = "ARC-ACH-STORY"
    ARC_OBSERVATIONAL_HUMOR = "ARC-OBS-HUMOR"
    ARC_WITNESS = "ARC-WITNESS"
    ARC_CONTRAST = "ARC-CONTRAST"
    ARC_COMP = "ARC-COMP"


class SentenceAuditRecord(BaseModel):
    sentence_id: str = Field(min_length=1)
    sentence_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    start_offset: int = Field(ge=0)
    end_offset: int = Field(gt=0)
    hedge_hits: list[str] = Field(default_factory=list)
    named_specificity_hits: list[str] = Field(default_factory=list)
    similarity_score: float = Field(ge=0.0, le=1.0)
    similarity_band: SimilarityBand
    collapse_reason: str = Field(min_length=1)
    failed: bool = False


class CoalitionInputs(BaseModel):
    coalition_id: str = Field(min_length=1)
    family_mix: list[str] = Field(min_length=1)
    stance_polarity: str = Field(min_length=1)
    source_count: int = Field(ge=1)
    evidence_strength: float = Field(ge=0.0, le=1.0)
    intended_business_job: str = Field(min_length=1)


class CoachResponseCapturePacket(BaseModel):
    capture_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    transcript_text: str = Field(min_length=1)
    transcript_language: str = Field(min_length=2, max_length=8)
    captured_at: datetime
    source_asset_id: str = Field(min_length=1)
    trigger_guard_session_id: str | None = None


class ContainerIntensityProfile(BaseModel):
    narrative_arc: str = Field(min_length=1)
    intensity_level: str = Field(min_length=1)
    pacing_profile: str = Field(min_length=1)
    emotional_job: str = Field(min_length=1)


class ArchetypeContainerManifest(BaseModel):
    runtime_session_id: str = Field(min_length=1)
    container_id: str = Field(min_length=1)
    selected_archetype: ArchetypeChoice
    archetype_intent: str = Field(min_length=1)
    activation_condition_summary: str = Field(min_length=1)
    structural_invariants: list[str] = Field(min_length=1)
    anti_draft_profile: list[str] = Field(min_length=1)
    distillation_funnel: list[str] = Field(min_length=1)
    accepted_sentence_ids: list[str] = Field(min_length=1)
    coalition_inputs: CoalitionInputs
    intensity_profile: ContainerIntensityProfile
    cmf_render_hints: list[str] = Field(min_length=1)
    authorized_render_targets: list[str] = Field(min_length=1)
    created_at: datetime


class ActionableRejectionPayload(BaseModel):
    runtime_session_id: str = Field(min_length=1)
    rejection_code: str = Field(min_length=1)
    similarity_score: float = Field(ge=0.0, le=1.0)
    similarity_band: SimilarityBand
    failing_sentence_ids: list[str] = Field(min_length=1)
    failing_sentences: list[str] = Field(min_length=1)
    collapse_reasons: list[str] = Field(min_length=1)
    coaching_fix: str = Field(min_length=1)
    rerecord_prompt: str = Field(min_length=1)
    trigger_guard_reroute_token: str | None = None
    trigger_guard_session_id: str | None = None


class CCFRoutingRecommendation(BaseModel):
    runtime_session_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    status: RuntimeStatus
    selected_archetype: ArchetypeChoice | None = None
    container_manifest: ArchetypeContainerManifest | None = None
    rejection_payload: ActionableRejectionPayload | None = None
    downstream_family_targets: list[str] = Field(default_factory=list)
    downstream_system_targets: list[str] = Field(default_factory=list)
    receipt_chain_hash: str = Field(min_length=1)
    generated_at: datetime
```

### 5.3 API and Service Contracts

#### Compile request

`POST /api/ccf/archetype-runtime/compile`

```json
{
  "coach_response_capture": {
    "capture_id": "CAP-001",
    "coach_id": "coach-123",
    "transcript_text": "Most coaches copy the market because they are scared to say who they actually disagree with...",
    "transcript_language": "en",
    "captured_at": "2026-05-12T08:14:00Z",
    "source_asset_id": "AST-VOICE-001",
    "trigger_guard_session_id": "TG-7788"
  },
  "coalition_inputs": {
    "coalition_id": "COL-42",
    "family_mix": ["STR", "PRS", "VOC"],
    "stance_polarity": "high_contrast",
    "source_count": 1,
    "evidence_strength": 0.81,
    "intended_business_job": "authority_content"
  },
  "mood_context": {
    "mood_id": "MOOD-001",
    "primary_vector": "aggressive_certainty",
    "intensity": 0.85
  },
  "evidence_bundle": {
    "bundle_id": "EVB-99",
    "authenticity_score": 0.92,
    "conflict_flags": []
  }
}
```

#### Success response

```json
{
  "runtime_session_id": "ACR-SESSION-001",
  "coach_id": "coach-123",
  "status": "compiled",
  "selected_archetype": "ARC-MYTH-DEBUNK",
  "container_manifest": {
    "runtime_session_id": "ACR-SESSION-001",
    "container_id": "ACR-CONTAINER-001",
    "selected_archetype": "ARC-MYTH-DEBUNK",
    "archetype_intent": "Expose a market lie and replace it with coach-owned proof order.",
    "activation_condition_summary": "High contrast stance + evidence-backed disagreement + single-take authority mode.",
    "structural_invariants": [
      "open with the named false belief",
      "state why it persists",
      "insert coach proof or anecdote",
      "replace belief with sharper frame"
    ],
    "anti_draft_profile": [
      "do not hedge both sides equally",
      "do not replace proof with abstract consensus language"
    ],
    "distillation_funnel": [
      "preserve named enemy",
      "preserve coach-owned example",
      "compress only repetition"
    ],
    "accepted_sentence_ids": ["S1", "S2", "S4"],
    "coalition_inputs": {
      "coalition_id": "COL-42",
      "family_mix": ["STR", "PRS", "VOC"],
      "stance_polarity": "high_contrast",
      "source_count": 1,
      "evidence_strength": 0.81,
      "intended_business_job": "authority_content"
    },
    "intensity_profile": {
      "narrative_arc": "confrontation",
      "intensity_level": "high",
      "pacing_profile": "tight_accelerating",
      "emotional_job": "challenge_false_belief"
    },
    "cmf_render_hints": [
      "high-contrast close-up start",
      "fast proof turn after accusation"
    ],
    "authorized_render_targets": ["short_form_video", "carousel", "telegram_voice_teaser"],
    "created_at": "2026-05-12T08:14:04Z"
  },
  "downstream_family_targets": ["authority_content"],
  "downstream_system_targets": ["cmf_arc_governed_rendering"],
  "receipt_chain_hash": "RCP-123",
  "generated_at": "2026-05-12T08:14:04Z"
}
```

#### Rejection response

```json
{
  "runtime_session_id": "ACR-SESSION-002",
  "coach_id": "coach-123",
  "status": "rejected_actionable",
  "selected_archetype": null,
  "container_manifest": null,
  "rejection_payload": {
    "runtime_session_id": "ACR-SESSION-002",
    "rejection_code": "ANTI_CENTROID_COLLAPSE",
    "similarity_score": 0.91,
    "similarity_band": "terminal",
    "failing_sentence_ids": ["S3", "S4"],
    "failing_sentences": [
      "Every business should just focus on authenticity.",
      "At the end of the day we all need to be ourselves."
    ],
    "collapse_reasons": [
      "industry-consensus abstraction with no named stake",
      "no coach-owned proof or contrarian edge"
    ],
    "coaching_fix": "Replace the generic advice with one named client moment or one explicit claim you believe the market gets wrong.",
    "rerecord_prompt": "Re-record the section after sentence S2. Name the exact belief you reject and the client moment that made you reject it.",
    "trigger_guard_reroute_token": "TG-REROUTE-991",
    "trigger_guard_session_id": "TG-7788"
  },
  "downstream_family_targets": [],
  "downstream_system_targets": ["trigger_first_execution_guard"],
  "receipt_chain_hash": "RCP-456",
  "generated_at": "2026-05-12T08:14:03Z"
}
```

### 5.4 Required Tables

```sql
CREATE TABLE IF NOT EXISTS archetype_runtime_sessions (
    runtime_session_id          TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    capture_id                  TEXT NOT NULL,
    coalition_id                TEXT NOT NULL,
    runtime_status              TEXT NOT NULL,
    selected_archetype          TEXT,
    trigger_guard_session_id    TEXT,
    receipt_chain_hash          TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS archetype_runtime_sentence_audits (
    sentence_audit_id           TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    sentence_id                 TEXT NOT NULL,
    sentence_index              INTEGER NOT NULL,
    sentence_text               TEXT NOT NULL,
    start_offset                INTEGER NOT NULL,
    end_offset                  INTEGER NOT NULL,
    similarity_score            DOUBLE PRECISION NOT NULL,
    similarity_band             TEXT NOT NULL,
    collapse_reason             TEXT NOT NULL,
    failed                      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS archetype_container_manifests (
    container_id                TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    selected_archetype          TEXT NOT NULL,
    manifest_json               JSONB NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS archetype_runtime_rejections (
    rejection_id                TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    rejection_code              TEXT NOT NULL,
    similarity_score            DOUBLE PRECISION NOT NULL,
    coaching_fix                TEXT NOT NULL,
    rerecord_prompt             TEXT NOT NULL,
    reroute_token               TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## 6. Backward Compatibility Fallback

### 6.1 Missing CRAL / evidence bundle

If the compile request lacks a CRAL or auth evidence bundle, `EvidenceConflictGateBridge` records `evidence_gate_status=skipped_absent` and continues. This mirrors `ResearchSynthesisProtocol.execute(...)`, which already supports an `ABSENT` fast path. Missing evidence is not enough to bypass anti-centroid checks.

### 6.2 Missing mood packet

If `MoodContextMap` or `AudienceMaturityProfile` is absent, the runtime falls back to a stored neutral-processing classification profile:

- `narrative_arc = witness`
- `intensity_level = medium`
- `pacing_profile = measured`
- `emotional_job = clarify`

This fallback may influence container shaping, but it must not soften rejection thresholds.

### 6.3 Anti-centroid scoring component degraded

If the higher-resolution sentence similarity scorer crashes, the runtime must not silently pass the take. It falls back to a deterministic hedge-and-specificity heuristic:

- hedge phrase count per sentence
- named entity / numeral / concrete-example detection
- abstract universal phrase detection

Fallback mode is allowed only for rejection or operator review. It cannot produce a success-grade compile.

### 6.4 Persistence failure

If Supabase write fails after a recommendation is computed:

- the response is still returned to the caller
- `receipt_chain_hash` must still be written locally
- `persistence_status=deferred_retry` is appended to the receipt metadata
- CMF handoff is blocked until the manifest row is retried successfully

### 6.5 Trigger-guard transport unavailable

If reroute-token creation succeeds but the upstream transport cannot launch the modal immediately, the runtime still returns the full actionable rejection payload. The coach can retry from the stored `rerecord_prompt`. Under no condition may the rejection be collapsed into "try again later".

## 7. Tasks

- [ ] Create `src/ccp/models/archetype_container_runtime_models.py`.
- [ ] Create `src/ccp/services/archetype_container_runtime.py`.
- [ ] Add `ArchetypeRuntimeRepository` methods and Supabase table bootstrap.
- [ ] Add `SentenceLedgerBuilder` with stable offsets and sentence IDs.
- [ ] Add `AntiCentroidValidator` with sentence-level scoring and heuristic fallback.
- [ ] Add `ArchetypeContractRegistry` with initial contracts:
- `ARC-MYTH-DEBUNK`
- `ARC-ACH-STORY`
- `ARC-OBS-HUMOR`
- `ARC-WITNESS`
- `ARC-CONTRAST`
- `ARC-COMP`
- [ ] Add `ArchetypeSelectionMatrix`.
- [ ] Add `EvidenceConflictGateBridge` wrapping `ResearchSynthesisProtocol`.
- [ ] Add `TriggerGuardBridge` and reroute-token creation.
- [ ] Add `CMFRecommendationBridge`.
- [ ] Add internal authenticated routes in `src/ccp/api/archetype_runtime.py`.
- [ ] Register routes in `src/ccp/api/main.py`.
- [ ] Add receipt-chain logging for every state transition.
- [ ] Add unit and integration tests in `tests/integration/` and `tests/unit/` if the repo already separates them locally.

## 8. Acceptance Criteria

### AC1 - Successful containerization emits a concrete archetype manifest

**Given** a valid `CoachResponseCapturePacket` and a validated coalition with sufficient edge,  
**When** the runtime compiles the payload,  
**Then** it selects exactly one `ArchetypeChoice`,  
**And** it emits a success-grade `CCFRoutingRecommendation`,  
**And** the attached `ArchetypeContainerManifest` includes structural invariants, anti-draft profile, accepted sentence IDs, intensity profile, and authorized render targets,  
**And** the recommendation names `cmf_arc_governed_rendering` as the downstream system target.

**FAILURE EXAMPLE:** The runtime returns only `selected_archetype="ARC-MYTH-DEBUNK"` plus a short note like "send to CMF", with no manifest fields, no accepted sentence IDs, and no intensity profile. That is a spec violation because the psychological container has not actually been formalized.

**Mandate:** Supports Story 5.1 and preserves the downstream emotional integrity required by `Phase4-M02`.

### AC2 - Anti-centroid rejection returns exact failing sentences and coaching fix

**Given** a transcript whose key sentences collapse into generic industry consensus,  
**When** `AntiCentroidValidator` rejects the take,  
**Then** the runtime returns `status=rejected_actionable`,  
**And** `rejection_payload.failing_sentence_ids` and `rejection_payload.failing_sentences` identify the exact collapsed sentences,  
**And** `similarity_score` is populated with a value in `[0.0, 1.0]`,  
**And** `coaching_fix` explicitly tells the coach what to add or sharpen,  
**And** `rerecord_prompt` is specific enough to drive the next recording attempt immediately.

**FAILURE EXAMPLE:** The runtime returns `{"status":"rejected_actionable","message":"Too generic. Try again."}`. That is a direct spec violation and a direct violation of `Phase4-M05`.

**Mandate:** `Phase4-M05 - The Actionable Rejection Rule`.

### AC3 - Rejection loops route back into trigger-first capture without extra navigation

**Given** a rejected compile request that originated from a trigger-guard session,  
**When** the runtime builds the rejection payload,  
**Then** it includes `trigger_guard_session_id` and `trigger_guard_reroute_token`,  
**And** the downstream target list is `["trigger_first_execution_guard"]`,  
**And** the payload is sufficient for the upstream execution guard to reopen the voice-capture path with the failing sentences highlighted.

**FAILURE EXAMPLE:** The runtime identifies the exact bad sentences but leaves the coach in a dead-end inspect page requiring manual navigation back to capture. That is a spec violation because the recovery path has been broken.

**Mandate:** Dependency enforcement of `Phase4-M04`, plus Story 5.1's explicit re-record loop.

### AC4 - Evidence conflicts block container commitment before archetype selection

**Given** CRAL/auth evidence is present and `ResearchSynthesisProtocol.execute(...)` returns a terminal authenticity block,  
**When** the runtime receives the compile request,  
**Then** it returns `status=blocked_evidence_conflict`,  
**And** no `selected_archetype` is emitted,  
**And** no CMF target is named,  
**And** the receipt chain records that container commitment was halted before selection.

**FAILURE EXAMPLE:** The runtime sees a Type 3 authenticity conflict but still selects `ARC-ACH-STORY` because the transcript itself sounds strong. That is a spec violation because the system would be locking invalid evidence inside a persuasive container.

**Mandate:** Story 5.1 integrity requirement plus existing FR17 deterministic conflict law.

### AC5 - `ARC-COMP` is only emitted for valid multi-source compilations

**Given** a runtime request has fewer than 3 source reactions,  
**When** the selection matrix evaluates archetype candidates,  
**Then** `ARC-COMP` is ineligible,  
**And** the runtime must choose a non-compilation archetype or reject the payload for a different reason.

**FAILURE EXAMPLE:** A single-take coach rant is labeled `ARC-COMP` because the code confuses "strong contrast" with "multi-source compilation". That is a spec violation and contradicts PRD-02's explicit `ARC-COMP` invariants.

**Mandate:** PRD-02 §3.4I structural invariants.

### AC6 - The runtime does not duplicate `semantic_affinity_guard.py`

**Given** a compile request enters the archetype runtime,  
**When** anti-centroid evaluation runs,  
**Then** the rejection reasoning is sentence-level and coach-specific,  
**And** it does not reuse C-06 pain-domain affinity as a proxy for centroid collapse,  
**And** the two services remain independently testable and independently callable.

**FAILURE EXAMPLE:** The implementation reuses `SemanticAffinityGuard.evaluate(...)` and maps `Escape + HIGH` to "generic". That is a spec violation because C-06 measures mood-safety proximity, not sentence-level flattening.

**Mandate:** Prompt-specific audit instruction and architectural separation requirement.

## 9. Dependencies

### Internal services

| Dependency | Type | Use |
|---|---|---|
| `ResearchSynthesisProtocol` | Existing service | Evidence conflict pass before container commitment |
| `PsychVariableMatrix` | Existing service | Deterministic mood shaping |
| `ContentMachinePipeline` | Existing service | Downstream content compilation consumer |
| `ReceiptChain` | Existing core | Immutable audit logging |
| `TriggerFirstExecutionGuardService` | Existing/new adjacent spec | Upstream capture and reroute transport |
| `CMFArcGovernedRenderingPipeline` | Adjacent Phase 4 spec | Downstream render consumer |

### Internal models and storage

| Dependency | Type | Use |
|---|---|---|
| `src/ccp/models/psych_routing_models.py` | Existing models | Mood context typing |
| `src/ccp/models/research_synthesis_models.py` | Existing models | `Step35Result` and conflict statuses |
| Supabase | Existing infra | Runtime session, manifest, and rejection persistence |
| `asset_registry` / `receipt_chain` | Existing tables | Source and audit references |

### External or cross-module assumptions

| Dependency | Assumption |
|---|---|
| Transcript quality | Upstream STT already produced a usable transcript before compile begins |
| Coach identity scope | `coach_id` remains the tenant isolation key |
| CMF contract | CMF accepts render hints and container-intensity metadata without needing the raw validator internals |
| Trigger guard contract | Upstream system can consume reroute token plus highlighted sentences and reopen recording |

## 10. Testing Strategy

This section follows the patterns in `tests/integration/test_fr18_psych_routing.py` and `tests/integration/test_fr19_semantic_affinity.py`: helper builders, AC-named scenario classes, explicit failure docstrings, deterministic field assertions, and fallback-path coverage.

### 10.1 Unit tests

#### `test_frera316_sentence_ledger_builder.py`

- `test_sentence_ids_and_offsets_are_stable_for_same_transcript`
- `test_sentence_splitter_preserves_exact_text_for_rejection_quotes`
- `test_sentence_ledger_marks_empty_or_whitespace_only_transcript_invalid`

#### `test_frera316_anti_centroid_validator.py`

- `test_generic_consensus_sentences_return_terminal_similarity_band`
- `test_specific_named_example_reduces_similarity_score_below_rejection_threshold`
- `test_rejection_payload_contains_exact_sentence_ids_and_coaching_fix`

#### `test_frera316_archetype_selection_matrix.py`

- `test_high_contrast_single_take_selects_arc_myth_debunk`
- `test_multi_source_three_or_more_sources_can_select_arc_comp`
- `test_arc_comp_rejected_when_source_count_below_three`

### 10.2 Integration tests

#### `tests/integration/test_frera316_archetype_runtime_compile.py`

Scenario class: `TestAC1SuccessfulContainerization`

- Build a valid capture packet, coalition, and mood context.
- Assert `status == compiled`.
- Assert `container_manifest.selected_archetype` is populated.
- Assert `container_manifest.accepted_sentence_ids` is non-empty.
- Assert `downstream_system_targets == ["cmf_arc_governed_rendering"]`.

Scenario class: `TestAC4EvidenceConflictBlock`

- Feed a mocked `Step35Result` with terminal block.
- Assert `status == blocked_evidence_conflict`.
- Assert `selected_archetype is None`.
- Assert CMF target list is empty.

#### `tests/integration/test_frera316_actionable_rejection_loop.py`

Scenario class: `TestAC2ActionableRejection`

- Feed a transcript with generic consensus statements.
- Assert `status == rejected_actionable`.
- Assert `failing_sentence_ids` and `failing_sentences` are exact and ordered.
- Assert `coaching_fix` is not empty.
- Assert `similarity_score >= 0.75`.

Scenario class: `TestAC3TriggerGuardReroute`

- Start from a request carrying `trigger_guard_session_id`.
- Assert the rejection payload includes reroute token plus session ID.
- Assert downstream target list is `["trigger_first_execution_guard"]`.

### 10.3 Non-regression expectations

- No test may treat `semantic_affinity_guard.py` output as a valid anti-centroid substitute.
- No test may accept a rejection payload without exact sentence text.
- No test may allow success-grade compile when the anti-centroid scorer is in degraded fallback mode.
- No test may allow `ARC-COMP` when `source_count < 3`.
