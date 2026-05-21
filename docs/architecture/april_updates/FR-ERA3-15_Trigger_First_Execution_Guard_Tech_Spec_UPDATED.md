# Tech-Spec: FR-ERA3-15 - Trigger-First Execution Guard
**Created:** 2026-05-11  
**Updated:** 2026-05-14  
**Status:** Ready for Development  
**Version:** 1.1 (ERA3 - SDA Semantic Upgrade)  
**Phase:** 4 / 6 Bridge - Existing Spec Update  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

<!-- UPDATED: update file created as a full revised copy with targeted SDA-aware changes only -->

## Pre-Work Log

```text
1. UPDATE PROMPT LOADED: P6_S44_FR-ERA3-15_Update_Trigger_First_Execution_Guard_for_Invariant_Field.md. Confirmed this is a semantic-upgrade pass, not a full redesign. Required changes: connect trigger logic to existential invariant pressure, distinguish broad-signal extraction from edge-product formation, and carry invariant-field evidence forward.
2. EXISTING SPEC READ:  FR-ERA3-15 current file reviewed in full. Exact proof of update locus:
   - Overview §2.2: "If it does not exist, the service returns a structured `ExecutionGuardDecision` that blocks compilation, derives a contextual provocative prompt using deterministic psychological routing plus intent templates..."
   - Architecture §3.1: `DEP-TFG-004 ProvocationPromptDeriver` is defined only as deriving prompt from original intent.
   - Schema §5 deterministic prompt table maps directly from `Intent Signal -> PromptIntentClass`.
   These are the exact places where broad-signal / invariant-aware pre-trigger semantics must now be inserted.
3. PROTOCOL LOADED:    ERA3_Tech_Spec_Writing_Protocol.md. Confirmed full-file output, traceable update comments, and architecture-grounded brownfield editing.
4. PRD-02 READ:       Confirmed Trigger-First remains the law and the updated runtime sequence is now `signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> directional integrity validation -> JIT script contract -> render blueprint`.
5. SDA CORE DOC READ: `lab/semantic_discernment_architecture_content_engine_v_1.md`. Confirmed existential invariants are deep semantic anchors and directional integrity depends on preserving invariant alignment, not only emotional coherence.
6. SDA TAXONOMY READ: `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`. Confirmed `Invariant Field Packet` is a runtime execution packet, `Directional Integrity Policy` is a validation-policy artifact, and `Hard Negative` is an adversarial evaluation asset. Also confirmed scalar separation: `Invariant Gravity` is canonical, `Invariant Activation Intensity` and `Invariant Resonance Multiplier` are runtime-only.
7. PPA DOC READ:      `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`. Confirmed the pre-trigger role of broad primary signal extraction and the post-trigger role of coalition/edge emergence. Exact doctrine: "the first signal must be broad enough to elicit truth; the second edge should be sharp enough to organize execution."
8. MATRIX OF EDGING READ: `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`. Confirmed broad primary signal is pre-trigger pressure selection while edge product is post-trigger force. This update therefore must not let the guard pretend it has already formed an edge product before capture.
9. FOUNDATION FR READ: FR-ERA3-20. Confirmed canonical `Existential Invariants` live in SDA ontology and that the guard should produce runtime evidence packets rather than invent local pseudo-ontology.
10. FOUNDATION FR READ: FR-ERA3-21. Confirmed the guard can query maintained primitive-to-invariant / archetype-to-geometry context through the SDA query service without absorbing ontology ownership.
11. FOUNDATION FR READ: FR-ERA3-22. Confirmed downstream `DirectionalIntegrityEngine` expects typed runtime packets and that `InvariantFieldPacket` / `DirectionalIntegrityReport` are distinct from the trigger guard's pre-trigger evidence generation.
12. ORIGINAL SOURCE SET RECHECKED:
    - `Phase 4 Story 4.1` still requires the block to become a trigger.
    - `Phase4-M04` still forbids static error walls.
    - `EXP-FRC-006` and `EXP-TRG-003` still govern friction reduction and opportune timing.
13. BACKEND RECHECKED: Existing guard integration points remain valid:
    - `psych_routing_engine.py`
    - `content_machine.py`
    - `morgan_orchestrator.py`
    - `sacred_audio.py`
    The semantic upgrade does not replace these dependencies; it enriches what is passed through them.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S44_FR-ERA3-15_Update_Trigger_First_Execution_Guard_for_Invariant_Field.md` | 2026-05-14 | Update assignment and mandatory SDA scope |
| 2 | `docs/architecture/april_updates/FR-ERA3-15_Trigger_First_Execution_Guard_Tech_Spec.md` | 2026-05-11 | Existing spec to revise in-place semantically |
| 3 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-14 | Required full-file update format and architecture traceability |
| 4 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | v6.0, 2026-05-06 | Trigger-First law and updated runtime sequence with invariant field |
| 5 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | 2026-05-12 | Existential invariant and directional-integrity doctrine |
| 6 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | 2026-05-12 | Artifact-role rules and runtime packet taxonomy |
| 7 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | 2026-05-02 | Broad-signal extraction and post-trigger edge emergence |
| 8 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | 2026-05-03 | Broad primary signal vs edge-product distinction |
| 9 | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | 2026-05-12 | Canonical ontology boundary for existential invariants |
| 10 | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | 2026-05-12 | SDA query/crosswalk ownership |
| 11 | `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md` | 2026-05-12 | Downstream validator packet expectations |
| 12 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Story 4.1 source and original trigger-first behavior |
| 13 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | M-04 rewrite rule |
| 14 | `primitives/experience/friction_ability/EXP-FRC-006.yaml` | Codified registry | Existing friction-reduction primitive |
| 15 | `primitives/experience/trigger_timing/EXP-TRG-003.yaml` | Codified registry | Existing timing primitive |
| 16 | `src/ccp/services/psych_routing_engine.py` | Existing service | Deterministic psychological envelope resolution |
| 17 | `src/ccp/models/psych_routing_models.py` | Existing models | Typed mood and regulatory structures |
| 18 | `src/ccp/services/content_machine.py` | Existing service | Current downstream content boundary |
| 19 | `src/ccp/agents/morgan_orchestrator.py` | Existing orchestrator | Execution context source |
| 20 | `src/ccp/api/sacred_audio.py` | Existing API | Audio capture ingress pattern |
| 21 | `src/ccp/api/telegram_webhook.py` | Existing API | Telegram ingress boundary |
| 22 | `src/ccp/agents/vidye_router.py` | Existing router | Resume routing boundary |
| 23 | `src/ccp/api/main.py` | Existing API gateway | Route registration boundary |
| 24 | `src/ccp/core/receipt_chain.py` | Existing core | Immutable audit trail |
| 25 | `src/ccp/core/circuit_breaker.py` | Existing core | Hard-stop precedent |
| 26 | `src/ccp/scripts/setup_supabase.py` | Existing bootstrap | Persistence extension point |
| 27 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Test structure precedent |
| 28 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Lifecycle assertion precedent |

## 2. Overview

### 2.1 Problem Statement

PRD-02 still makes Trigger-First a hard law, and the original `FR-ERA3-15` already solved the biggest brownfield failure: a missing authentic response must become an immediate recording trigger instead of a static block.

What the original spec did **not** yet formalize is the semantic layer between:

- raw execution intent
- the provocative prompt
- the later runtime's invariant-field and edge-product work

Without that semantic layer, the guard still works mechanically, but it remains too shallow in one important way:

- it derives prompt shape directly from intent-class heuristics
- it does not name the pre-trigger `Broad Primary Signal`
- it does not preserve provisional `Existential Invariant` evidence
- it risks blurring pre-trigger elicitation with post-trigger edge formation

That gap matters because the PPA and Matrix of Edging docs now make the architecture explicit:

- the **first signal** must be broad enough to elicit truth
- the **edge product** only emerges after authenticated reaction and downstream coalition work

So this update adds the missing semantic middle layer without changing the core guard behavior.

<!-- UPDATED: overview now makes the guard SDA-aware without redesigning its trigger-first mechanism -->
### 2.2 Solution

This revised spec keeps the existing `TriggerFirstExecutionGuardService` and the existing `blocked_capture_required` behavior, but upgrades the guard so it performs a new pre-trigger semantic step before prompt launch:

1. normalize the incoming request and original intent
2. extract a **Broad Primary Signal** from the request
3. derive **provisional Invariant Field evidence** from that broad signal
4. shape the provocative prompt using:
   - intent class
   - psychological envelope
   - broad-signal pressure
   - invariant-field evidence
5. return the same frictionless Telegram capture launch as before
6. pass forward the broad-signal and invariant evidence after capture so downstream runtime layers do not restart from zero

This update does **not** let the guard form an edge product. That remains downstream, after authenticated coach reaction, primitive candidate survival, coalition organization, and actual content runtime processing.

### 2.3 Scope

**In scope:**

- explicit broad-primary-signal extraction before prompt derivation
- provisional invariant-field evidence packet generation
- updated handoff payloads carrying semantic evidence forward
- preserving the existing block-to-capture-to-resume mechanism
- explicit separation between broad-signal elicitation and final edge-product formation

**Out of scope:**

- redesigning the full Trigger-First mechanism
- forming primitive coalitions or edge products inside the guard
- implementing the full `InvariantFieldPacket` downstream runtime resolution
- implementing `DirectionalIntegrityEngine`
- changing Telegram or audio ingress behavior outside what is needed to carry the new packets

## 3. Context for Development

### 3.1 Architecture Traceability

### 3.1a DEP-ID Registry (Data Exchange Payloads)

| DEP-ID | Schema Object | Purpose |
|---|---|---|
| DEP-TFG-001 | `TriggerFirstIntentPacket` | Upstream request holding raw execution intent and context. |
| DEP-TFG-002 | `BroadPrimarySignalPacket` | Extracted broad pre-trigger pressure signal. |
| DEP-TFG-003 | `InvariantFieldEvidencePacket` | Provisional existential invariant evidence mapped from the broad signal. |
| DEP-TFG-004 | `CoachResponseCapturePacket` | Authenticated media asset captured from the coach. |
| DEP-TFG-005 | `ProvocationPromptPacket` | Contextual prompt derived to trigger capture. |
| DEP-TFG-006 | `TelegramVoiceLaunchPacket` | Routing payload for Telegram Mini App ingestion. |
| DEP-TFG-007 | `ExecutionGuardDecision` | The formal block/pass verdict returned to the client. |
| DEP-TFG-008 | `ArchetypeRuntimeInputPacket` | Final structured handoff payload sent to downstream Epic 5 runtime. |

### 3.1b Service Component Traceability

| Service Node | Source | Responsibility |
|---|---|---|
| `TriggerFirstExecutionGuardService` | FR-ERA3-15 | Top-level gate for all content execution requests |
| `AuthenticatedSourceResolver` | Story 4.1 | Validates whether a request already has a valid `CoachResponseCapture` dependency |
| `MorganExecutionContextAdapter` | Story 4.1 | Normalizes orchestration context, requested artifact, and original intent into a guard-safe request packet |
| `ProvocationPromptDeriver` | Story 4.1 / M-04 | Derives a provocative contextual voice-capture prompt from the original intent |
| `PsychPromptEnvelopeResolver` | Story 4.1 | Uses deterministic psychological classification to shape the prompt envelope and emotional job |
| `TelegramVoiceModalLauncher` | Phase4-M04 | Emits the payload required to instantly route the coach into the Telegram recording experience |
| `TriggerBlockSessionRepository` | FR-ERA3-15 | Persists blocked request sessions, resume tokens, prompt payloads, and capture state |
| `ReactionCaptureCompletionBridge` | Story 4.1 | Accepts uploaded voice capture and binds it back to the blocked execution session |
| `ArchetypeRuntimeResumeBridge` | Story 4.1 | Hands authenticated capture into the next runtime layer without extra navigation |
| `ContentMachinePassGate` | FR-ERA3-15 | Prevents `ContentMachinePipeline.process_session(...)` from executing without authenticated source linkage |
| `TriggerFirstApiRouter` | FR-ERA3-15 | FastAPI route layer for evaluate, capture-complete, session read, and resume |
| `TriggerGuardReceiptBridge` | FR-ERA3-15 | Writes block/pass/prompt/capture/resume/fallback receipts |
<!-- UPDATED: added semantic pre-trigger components required by SDA -->
| `BroadPrimarySignalExtractor` | PRD-02 / PPA / Matrix of Edging | Extracts the broad pre-trigger pressure signal from execution intent before capture |
| `InvariantFieldEvidenceResolver` | PRD-02 / FR-ERA3-20 / FR-ERA3-21 | Resolves provisional existential-invariant evidence tied to the broad primary signal |
| `PreTriggerSemanticPacketAssembler` | FR-ERA3-15 update | Packages broad-signal and invariant evidence into handoff-safe runtime packets |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `psych_routing_engine.py` | `src/ccp/services/psych_routing_engine.py` | Reuses deterministic `resolve(...)` output to shape prompt tone, regulatory frame, and emotional delivery without using an LLM for the envelope. |
| `psych_routing_models.py` | `src/ccp/models/psych_routing_models.py` | Reuses `MoodContextMap`, `AudienceMaturityProfile`, and `PsychologicalClassification` as typed prompt-envelope inputs and outputs. |
| `content_machine.py` | `src/ccp/services/content_machine.py` | `process_session(...)` is treated as a downstream content path that must not run until the guard has authenticated a source capture and emitted pre-trigger semantic evidence. |
| `morgan_orchestrator.py` | `src/ccp/agents/morgan_orchestrator.py` | Provides orchestration precedent and upstream execution context. This spec consumes Morgan-owned request context data, not a new orchestration agent. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | Reuses the existing upload-validation pattern for accepted audio formats, asset generation, and receipt logging in the reaction-capture completion path. |
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | Existing Telegram ingress remains the transport boundary once the voice capture path is launched. |
| `vidye_router.py` | `src/ccp/agents/vidye_router.py` | Existing Telegram routing will need a guard-aware route branch so resumed capture flows return to the correct blocked session with semantic evidence intact. |
| `main.py` | `src/ccp/api/main.py` | Registers new guard routes and extends `/health` with guard readiness. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs every pass, block, broad-signal extraction, invariant-field evidence resolution, prompt derivation, capture acceptance, and resume decision. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Supplies the failure-handling pattern for safe degraded behavior when capture or resume cannot proceed. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Adds durable tables for block sessions, semantic evidence, capture packets, prompt packets, and resume outcomes. |

**Existing routes consumed or extended:**

- `POST /api/sacred-audio/upload`
  Usage: upload pattern reference for capture acceptance.
- `POST /api/telegram/webhook`
  Usage: transport boundary for resumed voice-note capture flow.

**New routes introduced by this spec:**

- `POST /api/ccf/trigger-guard/evaluate`
- `GET /api/ccf/trigger-guard/session/{guard_session_id}`
- `POST /api/ccf/trigger-guard/session/{guard_session_id}/capture-complete`
- `POST /api/ccf/trigger-guard/session/{guard_session_id}/resume`

**New persistence tables introduced by this spec:**

- `trigger_first_guard_sessions`
- `trigger_first_guard_semantic_evidence`
- `trigger_first_guard_prompts`
- `trigger_first_guard_captures`
- `trigger_first_guard_resumes`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FRC-006` | Poka-Yoke / Constraint as Focus | friction_ability | The block must neutralize anxiety and feel invitational rather than punitive. The coach should feel drawn into a low-resistance recording action rather than judged by an error wall. |

<!-- UPDATED: explicit SDA guardrail added without changing original M-04 behavior -->
### 3.4 SDA Constraint Layer

This update adds four semantic rules on top of the existing trigger-first behavior:

1. **Broad Primary Signal First**
   - The guard must extract a broad signal before prompt wording is finalized.
   - This signal is pre-trigger and is meant to elicit authentic reaction, not to prescribe the final content edge.

2. **Provisional Invariant Field Evidence**
   - The guard must derive provisional `Existential Invariant` pressure evidence from the broad signal.
   - This evidence is carried forward as a runtime packet, not stored as canonical ontology.

3. **No Edge Product at Guard Stage**
   - The guard must never claim to have formed the final edge product before authenticated response exists.
   - Primitive coalition and edge-product formation remain downstream responsibilities.

4. **Semantic Handoff, Not Just Block Status**
   - A blocked session must resume with the semantic evidence gathered during pre-trigger analysis so the downstream runtime starts from an informed field, not a blank slate.

### 3.5 CBAR Mandate Enforcement

| Mandate | Story | Required Behavior | Implementation Mechanism |
|---|---|---|---|
| Phase4-M04 - Frictionless Block Rule | Epic 4 Story 4.1 | Missing authenticated source must instantly become a Telegram voice recording opportunity, not a static backend error. | `TriggerFirstExecutionGuardService` returns a structured `blocked_capture_required` decision containing a pre-derived prompt and launch payload. `TelegramVoiceModalLauncher` immediately creates the capture launch packet. `TriggerBlockSessionRepository` stores a resume token so the same request can continue after capture with no extra navigation. |

**M-04 anti-patterns explicitly forbidden:**

- returning `Blocked: Authenticated Source Required` as plain text
- requiring the coach to manually navigate to another screen to start recording
- asking the coach to restate their intent after the block
- launching a generic recorder with no contextual prompt
- dropping the original execution request after capture instead of resuming it
- collapsing broad-signal extraction and edge-product formation into one step

### 3.6 Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| Guard location | Pre-compilation hard gate before any content execution path | PRD-02 says no authentic response means no right to render. |
| Prompt derivation | Deterministic template library plus psychological envelope resolution | The prompt must be reliable, auditable, and grounded in current intent rather than free-form AI improvisation. |
| <!-- UPDATED: semantic upgrade --> Broad-signal stage | Add `BroadPrimarySignalExtractor` before prompt derivation | The first signal must be broad enough to elicit truth and must be distinguished from the later edge product. |
| <!-- UPDATED: semantic upgrade --> Invariant evidence | Add provisional `InvariantFieldEvidencePacket` before capture and pass it forward after capture | Downstream runtime now expects invariant-aware context; the guard should not discard what it learned at the blocked moment. |
| Resume strategy | Persist blocked session plus resume token | The block must become a seamless trigger, not a dead-end that forces re-entry. |
| Capture ingestion | Reuse sacred-audio upload patterns | Existing audio format, asset, and receipt patterns already exist. |
| Morgan integration | Consume orchestration context packet rather than inventing a second orchestration stack | Morgan is already the orchestration authority for hard-coded gates and sequencing patterns. |
| <!-- UPDATED: semantic boundary --> Edge-product ownership | Do not emit edge products from the guard | PPA and Matrix of Edging place edge emergence after authenticated reaction and coalition work. |
| Downstream handoff | Introduce a formal runtime input packet for Epic 5, while also guarding current `content_machine` paths | This spec must protect current pipelines and prepare the clean handoff for the next epic. |
| Failure mode | Safe block with actionable fallback instead of silent pass-through | Any silent bypass would destroy Trigger-First integrity. |

## 4. Plan

### Phase 1 - Models and Persistence

| Task # | Task | Output |
|---|---|---|
| 1 | Create `src/ccp/models/trigger_first_guard_models.py` | Typed intent, semantic evidence, source, prompt, block, capture, and resume models |
| 2 | Extend `src/ccp/scripts/setup_supabase.py` | New tables, enums, indexes, and uniqueness constraints |
| 3 | Add `TriggerBlockSessionRepository` | Session, semantic evidence, prompt, capture, and resume persistence helpers |

### Phase 2 - Guard and Prompt Derivation

| Task # | Task | Output |
|---|---|---|
| 4 | Implement `MorganExecutionContextAdapter` | Normalize execution intent and orchestration context into a guard-safe `TriggerFirstIntentPacket` by strictly mapping: `request_id`, `coach_id`, `origin_surface`, `requested_artifact`, and mapping raw string arrays into `target_audience_label` and `execution_context_label`, while persisting the raw Morgan payload trace into `morgan_context_token`. |
| 5 | Implement `AuthenticatedSourceResolver` | Deterministic pass/fail validation for source dependency presence and freshness (strictly enforcing a maximum 60-minute freshness threshold; any capture older than 60 minutes is marked `stale` and rejected) |
| <!-- UPDATED: new pre-trigger semantic stage --> 6 | Implement `BroadPrimarySignalExtractor` | Broad pre-trigger pressure signal derived from original intent and execution context (utilizing `target_audience_label` and `execution_context_label` from the intent packet to accurately weight the extracted conflict/stakes pressure) |
| <!-- UPDATED: new pre-trigger semantic stage --> 7 | Implement `InvariantFieldEvidenceResolver` | Provisional invariant evidence derived from broad signal using SDA query service |
| 8 | Implement `PsychPromptEnvelopeResolver` | Deterministic psychological envelope from `PsychVariableMatrix.resolve(...)` |
| 9 | Implement `ProvocationPromptDeriver` | Contextual provocative prompt templates tied to original intent class plus broad-signal pressure |
| 10 | Implement `TelegramVoiceModalLauncher` | Launch payload for Telegram voice capture flow |

### Phase 3 - Capture Completion and Resume

| Task # | Task | Output |
|---|---|---|
| 11 | Implement `ReactionCaptureCompletionBridge` | Accept capture payload, persist it, bind it to blocked session |
| <!-- UPDATED: richer handoff --> 12 | Implement `ArchetypeRuntimeResumeBridge` | Emit runtime-ready packet containing capture plus broad-signal and invariant evidence |
| 13 | Implement `ContentMachinePassGate` | Prevent current content execution from running without authenticated source |
| 14 | Implement `TriggerFirstExecutionGuardService` | Single orchestration facade for evaluate, block, capture-complete, and resume |

### Phase 4 - API and Transport Integration

| Task # | Task | Output |
|---|---|---|
| 15 | Add FastAPI router module under `src/ccp/api/` | Evaluate, session read, capture-complete, and resume endpoints |
| 16 | Register new routes in `src/ccp/api/main.py` | Guard routes live in API gateway |
| 17 | Add guard-aware resume branch to `src/ccp/agents/vidye_router.py` | Voice captures return to the correct blocked request with semantic evidence intact |

### Phase 5 - Verification and Hardening

| Task # | Task | Output |
|---|---|---|
| 18 | Add receipt logging across all transitions | Full auditability of pass, block, broad-signal, invariant evidence, prompt, capture, and resume |
| 19 | Add unit tests for signal extraction, invariant evidence, source resolution, and prompt derivation | Deterministic guard behavior verification |
| 20 | Add integration tests for block-to-capture-to-resume flow | End-to-end M-04 enforcement with SDA-aware handoff |

## 5. Schema

**New model file:** `src/ccp/models/trigger_first_guard_models.py`

<!-- UPDATED: schema extended only where the prompt required semantic-upgrade behavior -->
```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from src.ccp.models.psych_routing_models import (
    ArousalDirection,
    MoodStatePrimary,
    RegulatoryFrame,
    SDTNeedPrimary,
    ValenceDelivery,
)


class ExecutionSurface(str, Enum):
    affine = "affine"
    telegram_chat = "telegram_chat"
    telegram_mini_app = "telegram_mini_app"
    api = "api"


class RequestedArtifactKind(str, Enum):
    linkedin_post = "linkedin_post"
    short_video = "short_video"
    carousel = "carousel"
    webinar_module = "webinar_module"
    reaction_script = "reaction_script"
    generic_content = "generic_content"


class GuardDecisionType(str, Enum):
    allow = "allow"
    blocked_capture_required = "blocked_capture_required"
    blocked_invalid_context = "blocked_invalid_context"


class SourceCaptureStatus(str, Enum):
    present = "present"
    missing = "missing"
    stale = "stale"
    invalid = "invalid"


class PromptIntentClass(str, Enum):
    contrarian_rebuttal = "contrarian_rebuttal"
    conviction_declaration = "conviction_declaration"
    pain_revelation = "pain_revelation"
    transformation_proof = "transformation_proof"
    stakes_clarifier = "stakes_clarifier"


class BroadPrimarySignalClass(str, Enum):
    conflict_pressure = "conflict_pressure"
    conviction_pressure = "conviction_pressure"
    pain_pressure = "pain_pressure"
    proof_pressure = "proof_pressure"
    stakes_pressure = "stakes_pressure"


class InvariantEvidenceStatus(str, Enum):
    provisional = "provisional"
    resolved = "resolved"
    weak = "weak"


class TriggerFirstIntentPacket(BaseModel):
    request_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    origin_surface: ExecutionSurface
    requested_artifact: RequestedArtifactKind
    original_intent_text: str = Field(..., min_length=8, max_length=500)
    target_audience_label: str = Field(default="", max_length=120)
    execution_context_label: str = Field(default="", max_length=120)
    morgan_context_token: str = Field(default="", max_length=120)
    submitted_at: datetime


class BroadPrimarySignalPacket(BaseModel):
    signal_id: str = Field(..., min_length=1)
    signal_class: BroadPrimarySignalClass
    summary: str = Field(..., min_length=8, max_length=220)
    rationale: str = Field(..., min_length=8, max_length=320)
    confidence: float = Field(..., ge=0.0, le=1.0)


class InvariantEvidenceEntry(BaseModel):
    invariant_id: str = Field(..., min_length=1, max_length=80)
    canonical_name: str = Field(..., min_length=2, max_length=120)
    pressure_role: str = Field(..., min_length=2, max_length=120)
    activation_hint: float = Field(..., ge=0.0, le=1.0)
    evidence_rationale: str = Field(..., min_length=8, max_length=320)


class InvariantFieldEvidencePacket(BaseModel):
    packet_id: str = Field(..., min_length=1)
    status: InvariantEvidenceStatus
    broad_primary_signal_id: str = Field(..., min_length=1)
    evidence_entries: list[InvariantEvidenceEntry] = Field(default_factory=list)
    note: str = Field(default="", max_length=320)


class CoachResponseCapturePacket(BaseModel):
    capture_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    source_asset_id: str = Field(..., min_length=1)
    source_asset_url: str = Field(..., min_length=1, max_length=500)
    source_transcript_excerpt: str = Field(default="", max_length=500)
    source_duration_seconds: int = Field(..., ge=1, le=900)
    captured_at: datetime
    authenticated: bool = Field(default=False)


class PromptEnvelopePacket(BaseModel):
    mood_state_primary: MoodStatePrimary
    arousal_direction: ArousalDirection
    valence_delivery: ValenceDelivery
    regulatory_frame: RegulatoryFrame
    sdt_need_primary: SDTNeedPrimary


class ProvocationPromptPacket(BaseModel):
    prompt_id: str = Field(..., min_length=1)
    intent_class: PromptIntentClass
    broad_primary_signal: BroadPrimarySignalPacket
    invariant_evidence: InvariantFieldEvidencePacket
    headline: str = Field(..., min_length=8, max_length=120)
    body: str = Field(..., min_length=8, max_length=280)
    spoken_prompt: str = Field(..., min_length=12, max_length=320)
    envelope: PromptEnvelopePacket
    launch_surface: ExecutionSurface = Field(default=ExecutionSurface.telegram_chat)
    resume_token: str = Field(..., min_length=1, max_length=120)


class TelegramVoiceLaunchPacket(BaseModel):
    guard_session_id: str = Field(..., min_length=1)
    telegram_deep_link: str = Field(..., min_length=1, max_length=500)
    voice_entry_label: str = Field(..., min_length=1, max_length=80)
    spoken_prompt: str = Field(..., min_length=12, max_length=320)
    resume_token: str = Field(..., min_length=1, max_length=120)


class ExecutionGuardDecision(BaseModel):
    guard_session_id: str = Field(..., min_length=1)
    decision: GuardDecisionType
    source_status: SourceCaptureStatus
    allow_execution: bool = Field(default=False)
    broad_primary_signal: BroadPrimarySignalPacket | None = None
    invariant_evidence: InvariantFieldEvidencePacket | None = None
    source_capture: CoachResponseCapturePacket | None = None
    prompt_packet: ProvocationPromptPacket | None = None
    telegram_launch: TelegramVoiceLaunchPacket | None = None
    rationale: str = Field(..., min_length=8, max_length=320)
    decided_at: datetime


class ArchetypeRuntimeInputPacket(BaseModel):
    guard_session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    original_intent_text: str = Field(..., min_length=8, max_length=500)
    broad_primary_signal: BroadPrimarySignalPacket
    invariant_evidence: InvariantFieldEvidencePacket
    capture: CoachResponseCapturePacket
    requested_artifact: RequestedArtifactKind
    resume_token: str = Field(..., min_length=1, max_length=120)


class TriggerGuardResumeResult(BaseModel):
    guard_session_id: str = Field(..., min_length=1)
    resumed: bool = Field(default=False)
    runtime_packet: ArchetypeRuntimeInputPacket | None = None
    downstream_target: str = Field(..., min_length=1, max_length=120)
    resumed_at: datetime
```

**Supabase tables to add in `setup_supabase.py`:**

| Table | Key Columns | Constraints |
|---|---|---|
| `trigger_first_guard_sessions` | `guard_session_id`, `request_id`, `coach_id`, `origin_surface`, `requested_artifact`, `original_intent_text`, `decision`, `source_status`, `resume_token`, `created_at` | unique(`request_id`), index on `coach_id`, index on `decision` |
| <!-- UPDATED: semantic evidence table --> `trigger_first_guard_semantic_evidence` | `semantic_packet_id`, `guard_session_id`, `signal_class`, `signal_summary`, `signal_rationale`, `signal_confidence`, `invariant_evidence_json`, `status`, `created_at` | unique(`guard_session_id`), index on `signal_class`, index on `status` |
| `trigger_first_guard_prompts` | `prompt_id`, `guard_session_id`, `intent_class`, `headline`, `body`, `spoken_prompt`, `envelope_json`, `created_at` | unique(`guard_session_id`), index on `intent_class` |
| `trigger_first_guard_captures` | `capture_id`, `guard_session_id`, `source_asset_id`, `source_asset_url`, `source_duration_seconds`, `authenticated`, `captured_at` | unique(`guard_session_id`, `capture_id`), index on `authenticated` |
| `trigger_first_guard_resumes` | `resume_id`, `guard_session_id`, `resume_token`, `downstream_target`, `resumed`, `resumed_at` | unique(`guard_session_id`, `resume_token`) |

<!-- UPDATED: broad-signal stage inserted ahead of prompt templates -->
**Deterministic broad-signal extraction and prompt-derivation table:**

| Intent Signal | BroadPrimarySignalClass | PromptIntentClass | Example Prompt Shape |
|---|---|---|---|
| contains `wrong`, `mistake`, `myth`, `competitor`, `enemy` | `conflict_pressure` | `contrarian_rebuttal` | `Tell me why {target} is wrong about {topic}.` |
| contains `believe`, `stand for`, `why I`, `what I know` | `conviction_pressure` | `conviction_declaration` | `Say the thing you believe that most people in your industry are too careful to say.` |
| contains `pain`, `stuck`, `afraid`, `avoid`, `struggle` | `pain_pressure` | `pain_revelation` | `Describe the real pain your client is sitting in that polite marketing language hides.` |
| contains `result`, `client`, `proof`, `before/after`, `win` | `proof_pressure` | `transformation_proof` | `Tell me about the moment a client changed because of this principle.` |
| no strong class match | `stakes_pressure` | `stakes_clarifier` | `Why does this matter enough that someone should stop scrolling and listen right now?` |

**Hard guard rules:**

- `allow_execution = true` only if `source_status == present` and `source_capture.authenticated == true`
- `source_status == missing` must always return `blocked_capture_required`, never `blocked_invalid_context`
- `blocked_capture_required` decisions must include:
  - `broad_primary_signal`
  - `invariant_evidence`
  - `prompt_packet`
  - `telegram_launch`
- `telegram_launch.spoken_prompt` must be identical to `prompt_packet.spoken_prompt`
- `prompt_packet.broad_primary_signal.signal_id` must equal `invariant_evidence.broad_primary_signal_id`
- the guard must never emit `edge_product` or any final coalition object
- resume requires exact `resume_token` match

## 6. Fallback

| Failure | Detection | User-Facing Result | System Action |
|---|---|---|---|
| No source capture | `AuthenticatedSourceResolver` returns `missing` | Instant Telegram voice-launch path with contextual prompt | Persist blocked session, broad signal, invariant evidence, and prompt |
| Invalid orchestration context | `MorganExecutionContextAdapter` cannot normalize minimal request fields | Return actionable blocked-invalid-context message with retry guidance | Log receipt and do not execute compilation |
| <!-- UPDATED: semantic fallback --> Broad-signal extraction cannot classify strongly | no deterministic class match | Use `stakes_pressure` + `stakes_clarifier` fallback | Persist fallback signal and mark invariant evidence `weak` |
| <!-- UPDATED: semantic fallback --> Invariant evidence is partial | SDA query or mapping confidence insufficient | Still launch contextual prompt, but persist `provisional` or `weak` evidence for downstream runtime | Never collapse to generic static error |
| Capture upload fails validation | bad format, oversize, or missing file | Return capture-specific error while preserving blocked session | Keep session open for retry |
| Resume token mismatch | bad or stale token | Do not resume downstream runtime | Log security/fallback receipt, keep original session unchanged |
| Downstream runtime unavailable | resume bridge cannot hand off | Return resumable blocked state, not silent loss | Persist pending resume status and retry option |

**Hard-stop rules:**

- The system must never silently bypass the guard because prompt derivation failed.
- The system must never replace a contextual prompt with a static generic error.
- The system must never discard the blocked request after successful capture.
- The system must never claim final invariant resolution or final edge-product formation before authenticated reaction exists.

## 7. Tasks

1. Create `D:\Work\The Conscious Coaching Factory\src\ccp\models\trigger_first_guard_models.py`.
2. Extend `D:\Work\The Conscious Coaching Factory\src\ccp\scripts\setup_supabase.py` with the five guard tables and indexes.
3. Create `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
4. Add `MorganExecutionContextAdapter` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
5. Add `AuthenticatedSourceResolver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
<!-- UPDATED: new SDA-aware tasks -->
6. Add `BroadPrimarySignalExtractor` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
7. Add `InvariantFieldEvidenceResolver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
8. Add `PsychPromptEnvelopeResolver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
9. Add `ProvocationPromptDeriver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
10. Add `TelegramVoiceModalLauncher` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
11. Add `ReactionCaptureCompletionBridge` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
12. Add `ArchetypeRuntimeResumeBridge` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
13. Add `ContentMachinePassGate` wiring to `D:\Work\The Conscious Coaching Factory\src\ccp\services\content_machine.py` integration points.
14. Create `D:\Work\The Conscious Coaching Factory\src\ccp\api\trigger_first_guard.py`.
15. Register the router in `D:\Work\The Conscious Coaching Factory\src\ccp\api\main.py`.
16. Add guard-aware resume handling to `D:\Work\The Conscious Coaching Factory\src\ccp\agents\vidye_router.py`.
17. Reuse upload-validation patterns from `D:\Work\The Conscious Coaching Factory\src\ccp\api\sacred_audio.py` for capture acceptance.
18. Add unit tests in `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py`.
19. Add integration tests in `D:\Work\The Conscious Coaching Factory\tests\integration\test_fr_era3_15_trigger_first_execution_guard.py`.
20. Extend receipt coverage for pass/block/broad-signal/invariant-evidence/prompt/capture/resume decisions.

## 8. Acceptance Criteria

### Story 4.1 - The Blank-Page Prevention Block

**AC1 - Hard Stop Before Compilation**

- Given the content factory receives an execution request
- When the request lacks an authenticated source dependency
- Then the guard rejects compilation before any downstream content execution begins
- And `ContentMachinePipeline.process_session(...)` or any equivalent execution path is not invoked
- CBAR Mandate enforced: `Phase4-M04`
- Measurable pass condition: returned decision is `blocked_capture_required` and `allow_execution == false`
- FAILURE EXAMPLE: the system begins content generation and only later warns that the source was missing

**AC2 - Frictionless Trigger Replacement**

- Given the request is blocked for missing source capture
- When the guard returns its decision
- Then it includes a contextual provocative prompt and a Telegram voice-launch packet in the same response
- And no static error message is returned as the primary user-facing action
- CBAR Mandate enforced: `Phase4-M04`
- Measurable pass condition: both `prompt_packet` and `telegram_launch` are non-null in the blocked response
- FAILURE EXAMPLE: the API returns only `Blocked: Authenticated Source Required`

<!-- UPDATED: new acceptance criterion for broad signal -->
**AC3 - Broad Primary Signal Is Extracted Before Prompting**

- Given the blocked request includes original intent text
- When the guard derives the semantic pre-trigger context
- Then it emits a `BroadPrimarySignalPacket` before final prompt wording is chosen
- And that signal is broad enough to provoke authentic speech rather than prescribe a finished content edge
- Measurable pass condition: `broad_primary_signal` is non-null and `signal_class` is one of the deterministic classes
- FAILURE EXAMPLE: the system jumps directly from raw intent to prompt wording with no explicit broad-signal stage

<!-- UPDATED: invariant evidence handoff -->
**AC4 - Invariant Field Evidence Is Passed Forward**

- Given the blocked request has a resolved or provisional broad signal
- When the guard returns `blocked_capture_required`
- Then it also returns `InvariantFieldEvidencePacket`
- And after successful capture the resume packet still contains that same evidence
- Measurable pass condition: `invariant_evidence` exists on both `ExecutionGuardDecision` and resumed `ArchetypeRuntimeInputPacket`
- FAILURE EXAMPLE: the system launches capture but discards the semantic field it inferred at the blocked moment

**AC5 - Prompt Derived From Original Intent and Broad Pressure**

- Given the blocked request includes original intent text
- When the guard derives the prompt
- Then the chosen prompt template reflects the request's intent class deterministically
- And the spoken prompt also aligns to the extracted broad pressure signal
- And the prompt contains intent-specific wording rather than a generic `record your thoughts` instruction
- CBAR Mandate enforced: `Phase4-M04`
- Measurable pass condition: derived `intent_class` matches deterministic template rules and `spoken_prompt` length is between 12 and 320 characters
- FAILURE EXAMPLE: every blocked request gets the same generic recording prompt regardless of what the coach asked to create

<!-- UPDATED: explicit edge-product boundary -->
**AC6 - Guard Does Not Form Final Edge Product**

- Given the request is still in the pre-trigger block stage
- When the guard emits semantic context
- Then it may emit broad-signal and invariant evidence
- But it must not emit a final primitive coalition or edge product
- Measurable pass condition: no guard model contains `edge_product` fields or downstream-force labels pretending final execution force already exists
- FAILURE EXAMPLE: the guard returns a narrow execution edge before the coach has authentically reacted

**AC7 - Immediate Resume After Capture**

- Given the coach completes the requested voice capture
- When the capture completion endpoint accepts the authenticated audio asset
- Then the blocked session resumes into the Archetype Runtime input boundary without requiring the coach to resubmit the original execution request
- And the resume packet includes original intent, broad-signal packet, invariant evidence, and capture packet
- CBAR Mandate enforced: `Phase4-M04`
- Measurable pass condition: `TriggerGuardResumeResult.resumed == true` and `runtime_packet` is populated on successful resume
- FAILURE EXAMPLE: the coach records the voice note successfully but must manually go back and click `Generate` again

**Failure Example**

- The coach clicks `Generate LinkedIn Post` in AFFiNE.
- The backend responds with `Blocked: Authenticated Source Required`.
- No broad signal, no invariant evidence, no prompt, no voice launch path, and no resume token are returned.
- Or the system returns a final execution edge before any real reaction exists.
- The coach has to figure out manually where to record, loses the original emotional context, and abandons the attempt.
- This is a spec failure. It violates Story 4.1, Phase4-M04, the Trigger-First law from PRD-02, and the SDA distinction between broad pre-trigger signal and post-trigger edge product.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `src/ccp/services/psych_routing_engine.py` | Existing service | Deterministic psychological envelope resolution for provocative prompts |
| `src/ccp/models/psych_routing_models.py` | Existing models | Typed mood, regulatory, and SDT prompt-shaping fields |
| `src/ccp/services/content_machine.py` | Existing service | Downstream content execution path that must be gated |
| `src/ccp/agents/morgan_orchestrator.py` | Existing orchestrator | Upstream execution context and hard-gate precedent |
| `src/ccp/api/sacred_audio.py` | Existing API pattern | Audio-upload validation and receipt pattern reference |
| `src/ccp/api/telegram_webhook.py` | Existing transport | Telegram voice-capture ingress boundary |
| `src/ccp/agents/vidye_router.py` | Existing router | Guard-aware resume routing after voice capture |
| `src/ccp/core/receipt_chain.py` | Cross-system infrastructure | Immutable auditability |
| `src/ccp/core/circuit_breaker.py` | Cross-system infrastructure | Safe degraded fallback behavior |
| <!-- UPDATED: new SDA dependencies --> `FR-ERA3-20` | Foundation spec | Canonical existential-invariant ontology |
| <!-- UPDATED: new SDA dependencies --> `FR-ERA3-21` | Foundation spec | Query/crosswalk access for provisional invariant evidence |
| `FR-ERA3-16` (future Epic 5 runtime) | Downstream contract | Accepts `ArchetypeRuntimeInputPacket` after capture completion |
| `FR-ERA3-22` | Downstream validator | Later consumes the invariant-aware packet stream this guard now seeds |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Telegram Bot / Mini App interaction surface | Existing Telegram platform | Delivery of the voice capture launch experience |
| Supabase Storage | Existing platform dependency | Storage destination for accepted voice capture assets |

## 10. Testing Strategy

### Unit Tests

| Test File | Describe Block | Test Name | What It Verifies |
|---|---|---|---|
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `AuthenticatedSourceResolver` | `returns_blocked_capture_required_when_source_missing` | missing source always blocks before execution |
| <!-- UPDATED: new semantic-stage test --> `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `BroadPrimarySignalExtractor` | `extracts_conflict_pressure_from_enemy_language_intent` | broad signal is explicit and deterministic before prompt derivation |
| <!-- UPDATED: new semantic-stage test --> `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `InvariantFieldEvidenceResolver` | `returns_provisional_invariant_evidence_for_conflict_pressure` | invariant evidence is produced as runtime evidence rather than skipped |
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `ProvocationPromptDeriver` | `derives_contrarian_prompt_from_enemy_language_intent` | prompt template classification is deterministic and intent-specific |
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `TelegramVoiceModalLauncher` | `copies_spoken_prompt_and_resume_token_into_launch_packet` | launch payload matches prompt packet and is resume-safe |
| <!-- UPDATED: boundary test --> `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `TriggerFirstExecutionGuardService` | `does_not_emit_edge_product_pre_capture` | guard preserves the broad-signal/edge-product distinction |
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `ArchetypeRuntimeResumeBridge` | `resumes_without_resubmitting_original_request` | successful capture continues flow immediately |

### Integration Tests

Modeled on:

- `D:\Work\The Conscious Coaching Factory\tests\integration\test_cpsc_fr52_webinar_brief.py`
- `D:\Work\The Conscious Coaching Factory\tests\integration\test_ca11_fr16_studio_block.py`

Named integration tests:

- `test_blocked_execution_returns_prompt_and_telegram_launch_same_response`
- `test_blocked_execution_returns_broad_signal_and_invariant_evidence`
- `test_capture_completion_resumes_session_into_runtime_packet_with_semantic_evidence`
- `test_static_error_only_response_is_never_returned_for_missing_source`
- `test_guard_never_returns_edge_product_at_pretrigger_stage`

Pattern requirements:

- use helper builders for `TriggerFirstIntentPacket`, blocked sessions, semantic evidence, and capture payloads
- assert concrete `decision`, `allow_execution`, `intent_class`, `signal_class`, and `resumed` fields
- assert no integration path returns plain static block text without a prompt packet
- assert resumed packets preserve semantic evidence continuity

### Manual Verification

1. Submit a content execution request with no authenticated source capture.
2. Confirm the API returns a blocked decision with:
   - a broad primary signal
   - invariant-field evidence
   - a contextual prompt
   - a Telegram launch payload
3. Confirm no downstream compilation begins before capture is supplied.
4. Confirm the response does not contain any final edge-product or coalition label pretending execution force is already resolved.
5. Upload a valid voice capture tied to the blocked session.
6. Confirm the session resumes automatically without re-entering the original request.
7. Confirm the resumed runtime packet contains the original intent, broad signal, invariant evidence, and authenticated capture.
8. Submit a request whose intent contains explicit contrarian language and verify:
   - `BroadPrimarySignalClass == conflict_pressure`
   - `PromptIntentClass == contrarian_rebuttal`
9. Submit a request with an ambiguous intent and verify the deterministic fallback classes are:
   - `BroadPrimarySignalClass == stakes_pressure`
   - `PromptIntentClass == stakes_clarifier`
10. Submit an invalid capture file and confirm the blocked session remains retryable rather than being lost.
