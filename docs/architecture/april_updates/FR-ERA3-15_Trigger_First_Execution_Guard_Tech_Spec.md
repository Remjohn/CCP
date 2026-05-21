# Tech-Spec: FR-ERA3-15 - Trigger-First Execution Guard
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 4 - Pipelines & Engines
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new backend routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      schema work extends `src/ccp/scripts/setup_supabase.py`, Section 3 requires direct mapping
                      to existing services before introducing new ones, and the protocol's CBAR note requires
                      mandates to be named explicitly in Section 3.
2. PRD LOADED:        PRD-02 exact architecture law: "If there is no authentic response, there is no right to
                      render." PRD-02 exact brownfield definition: "Enforce the Trigger-First execution flow
                      (signal → provocation → reaction → primitive distillation → compilation) across all content
                      pipelines, physically preventing blank-page generative "prompting"."
3. EPIC LOADED:       Phase 4 Story 4.1 first AC: "Given the content factory receives an execution request,
                      When the request lacks an authenticated source dependency (e.g., `CoachResponseCapture`),
                      Then the execution guard halts compilation and instantly surfaces the Telegram Voice
                      recording modal, And the modal is pre-loaded with a specific, provocative prompt derived
                      from the coach's initial intent (e.g., "Tell me why your competitors are wrong about this"),
                      And upon voice capture, the system immediately feeds the reaction into the Archetype
                      Container Runtime (Epic 5) without requiring additional navigation."
4. CBAR LOADED:       Phase4-M04 confirmed from the Phase 4 audit. Exact rewrite demand: the block must transform
                      into a frictionless path to compliance, instantly surfacing a Telegram voice modal with a
                      specific provocative prompt instead of a static error. Verdict in audit: REWRITE REQUIRED.
5. PRIMITIVES:        `experience_primitive_id: "EXP-FRC-006"` / `canonical_name: "Hypnosedation Reframing"`
                      `experience_primitive_id: "EXP-TRG-003"` / `canonical_name: "Kairos / Opportune Moment"`
6. BACKEND:           `src/ccp/services/psych_routing_engine.py` - `def resolve(self, mood_context: MoodContextMap, maturity_profile: AudienceMaturityProfile) -> PsychologicalClassification`
                      `src/ccp/services/content_machine.py` - `async def process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
                      `src/ccp/agents/morgan_orchestrator.py` - `def run_post_fr3_initialization(self, coach_id: str) -> dict`
                      `src/ccp/api/sacred_audio.py` - `async def upload_sacred_audio(file: UploadFile = File(...), coach_acronym: str = "")`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, scenario-
                      oriented test classes, direct field assertions, and explicit lifecycle/state checks. Section
                      10 follows that pattern.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P4_S24_FR-ERA3-15_Trigger_First_Execution_Guard.md` | 2026-05-11 | Assignment prompt, M-04 constraint, and required service audit |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Required backend mapping, schema extension points, and CBAR structure |
| 3 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Epic 4 story text, first AC, and mapped primitive constraint |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | M-04 failure scenario and rewrite demand |
| 5 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | v6.0, 2026-05-06 | Trigger-first chain, runtime layer model, and brownfield enforcement language |
| 6 | `primitives/experience/friction_ability/EXP-FRC-006.yaml` | Codified registry | Verified friction-reduction primitive used for block reframing |
| 7 | `primitives/experience/trigger_timing/EXP-TRG-003.yaml` | Codified registry | Verified timing primitive used for contextual prompt timing |
| 8 | `src/ccp/services/psych_routing_engine.py` | Existing service | Deterministic psychological classification engine used to shape provocative prompt envelopes |
| 9 | `src/ccp/models/psych_routing_models.py` | Existing models | Typed psychological input/output structures consumed by the routing engine |
| 10 | `src/ccp/services/content_machine.py` | Existing service | Existing content pipeline boundary that must never run without authenticated source capture |
| 11 | `src/ccp/agents/morgan_orchestrator.py` | Existing orchestrator | Existing orchestration context and hard-gate precedent |
| 12 | `src/ccp/api/sacred_audio.py` | Existing API | Existing audio-upload pattern reused for reaction-capture ingestion design |
| 13 | `src/ccp/api/telegram_webhook.py` | Existing API | Telegram ingress boundary for downstream voice-capture flow |
| 14 | `src/ccp/agents/vidye_router.py` | Existing router | Existing Telegram routing boundary that must route guard-trigger capture flows correctly |
| 15 | `src/ccp/api/main.py` | 1.0.0 | FastAPI extension point for guard endpoints |
| 16 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit trail for block/pass/resume outcomes |
| 17 | `src/ccp/core/circuit_breaker.py` | Current | Hard-stop precedent for guarded failure states |
| 18 | `src/ccp/scripts/setup_supabase.py` | Current | Schema bootstrap extension point |
| 19 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and helper style |
| 20 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Explicit lifecycle assertion pattern for richer systems |

## 2. Overview

### 2.1 Problem Statement

PRD-02 makes Trigger-First a hard architectural law, but the current codebase still lacks a formal execution guard that sits in front of content generation and turns missing source capture into an immediate corrective behavior rather than a dead-end rejection.

Without that guard, three failures happen:

- generation requests can drift into blank-page or topic-first prompting without authentic voice evidence
- blocked requests return static, shaming, or vague error states that do not move the coach forward
- even when the system knows a source is missing, it lacks a deterministic way to derive the right provocative voice-capture prompt from the original intent

Epic 4 is targeting those exact failures. The absence of authenticated source capture must not produce a normal API error. It must become the trigger that drives the coach directly into the missing reaction step.

### 2.2 Solution

This spec introduces a new backend service, `TriggerFirstExecutionGuardService`, that evaluates all content execution requests before any compilation path is allowed to proceed. If authenticated source capture exists, the request passes through with a signed source reference. If it does not exist, the service returns a structured `ExecutionGuardDecision` that blocks compilation, derives a contextual provocative prompt using deterministic psychological routing plus intent templates, opens a Telegram voice-capture path immediately, and resumes the downstream runtime as soon as the capture is uploaded.

The guard is therefore not a passive validator. It is an active trigger conversion engine.

### 2.3 Scope

**In scope:**

- deterministic pass/block guard in front of content execution
- typed `TriggerFirstIntentPacket` and `CoachResponseCapturePacket`
- authenticated source validation rules
- provocative prompt derivation from original execution intent
- Telegram voice-modal launch payload generation
- capture-session persistence and resume-token flow
- immediate post-capture handoff contract into the Archetype Container Runtime boundary
- FastAPI routes for evaluate, capture-complete, session-status, and resume
- receipt logging and safe fallback behavior

**Out of scope:**

- implementing the full Archetype Container Runtime from Epic 5
- replacing `PsychVariableMatrix.resolve(...)`
- replacing `ContentMachinePipeline.process_session(...)`
- redesigning Telegram webhook ingestion from scratch
- training or rendering voice notes
- implementing the full Voice Prompt Engine from Epic 6

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Responsibility |
|---|---|---|---|
| DEP-TFG-001 | `TriggerFirstExecutionGuardService` | FR-ERA3-15 | Top-level gate for all content execution requests |
| DEP-TFG-002 | `AuthenticatedSourceResolver` | Story 4.1 | Validates whether a request already has a valid `CoachResponseCapture` dependency |
| DEP-TFG-003 | `MorganExecutionContextAdapter` | Story 4.1 | Normalizes orchestration context, requested artifact, and original intent into a guard-safe request packet |
| DEP-TFG-004 | `ProvocationPromptDeriver` | Story 4.1 / M-04 | Derives a provocative contextual voice-capture prompt from the original intent |
| DEP-TFG-005 | `PsychPromptEnvelopeResolver` | Story 4.1 | Uses deterministic psychological classification to shape the prompt envelope and emotional job |
| DEP-TFG-006 | `TelegramVoiceModalLauncher` | Phase4-M04 | Emits the payload required to instantly route the coach into the Telegram recording experience |
| DEP-TFG-007 | `TriggerBlockSessionRepository` | FR-ERA3-15 | Persists blocked request sessions, resume tokens, prompt payloads, and capture state |
| DEP-TFG-008 | `ReactionCaptureCompletionBridge` | Story 4.1 | Accepts uploaded voice capture and binds it back to the blocked execution session |
| DEP-TFG-009 | `ArchetypeRuntimeResumeBridge` | Story 4.1 | Hands authenticated capture into the next runtime layer without extra navigation |
| DEP-TFG-010 | `ContentMachinePassGate` | FR-ERA3-15 | Prevents `ContentMachinePipeline.process_session(...)` from executing without authenticated source linkage |
| DEP-TFG-011 | `TriggerFirstApiRouter` | FR-ERA3-15 | FastAPI route layer for evaluate, capture-complete, session read, and resume |
| DEP-TFG-012 | `TriggerGuardReceiptBridge` | FR-ERA3-15 | Writes block/pass/prompt/capture/resume/fallback receipts |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `psych_routing_engine.py` | `src/ccp/services/psych_routing_engine.py` | Reuses deterministic `resolve(...)` output to shape prompt tone, regulatory frame, and emotional delivery without using an LLM for the envelope. |
| `psych_routing_models.py` | `src/ccp/models/psych_routing_models.py` | Reuses `MoodContextMap`, `AudienceMaturityProfile`, and `PsychologicalClassification` as typed prompt-envelope inputs and outputs. |
| `content_machine.py` | `src/ccp/services/content_machine.py` | `process_session(...)` is treated as a downstream content path that must not run until the guard has authenticated a source capture. |
| `morgan_orchestrator.py` | `src/ccp/agents/morgan_orchestrator.py` | Provides orchestration precedent and upstream execution context. This spec consumes Morgan-owned request context data, not a new orchestration agent. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | Reuses the existing upload-validation pattern for accepted audio formats, asset generation, and receipt logging in the reaction-capture completion path. |
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | Existing Telegram ingress remains the transport boundary once the voice capture path is launched. |
| `vidye_router.py` | `src/ccp/agents/vidye_router.py` | Existing Telegram routing will need a guard-aware route branch so resumed capture flows return to the correct blocked session. |
| `main.py` | `src/ccp/api/main.py` | Registers new guard routes and extends `/health` with guard readiness. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs every pass, block, prompt derivation, capture acceptance, and resume decision. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Supplies the failure-handling pattern for safe degraded behavior when capture or resume cannot proceed. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Adds durable tables for block sessions, capture packets, prompt packets, and resume outcomes. |

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
- `trigger_first_guard_prompts`
- `trigger_first_guard_captures`
- `trigger_first_guard_resumes`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FRC-006` | Hypnosedation Reframing | friction_ability | The block must neutralize anxiety and feel invitational rather than punitive. The coach should feel drawn into a low-resistance recording action rather than judged by an error wall. |
| `EXP-TRG-003` | Kairos / Opportune Moment | trigger_timing | The provocative prompt must arrive at the exact blocked moment, using the coach's current intent as the timing advantage rather than forcing them to re-enter context later. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Story | Required Behavior | Implementation Mechanism |
|---|---|---|---|
| Phase4-M04 - Frictionless Block Rule | Epic 4 Story 4.1 | Missing authenticated source must instantly become a Telegram voice recording opportunity, not a static backend error. | `TriggerFirstExecutionGuardService` returns a structured `blocked_capture_required` decision containing a pre-derived prompt and launch payload. `TelegramVoiceModalLauncher` immediately creates the capture launch packet. `TriggerBlockSessionRepository` stores a resume token so the same request can continue after capture with no extra navigation. |

**M-04 anti-patterns explicitly forbidden:**

- returning `Blocked: Authenticated Source Required` as plain text
- requiring the coach to manually navigate to another screen to start recording
- asking the coach to restate their intent after the block
- launching a generic recorder with no contextual prompt
- dropping the original execution request after capture instead of resuming it

### 3.5 Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| Guard location | Pre-compilation hard gate before any content execution path | PRD-02 says no authentic response means no right to render. |
| Prompt derivation | Deterministic template library plus psychological envelope resolution | The prompt must be reliable, auditable, and grounded in current intent rather than free-form AI improvisation. |
| Resume strategy | Persist blocked session plus resume token | The block must become a seamless trigger, not a dead-end that forces re-entry. |
| Capture ingestion | Reuse sacred-audio upload patterns | Existing audio format, asset, and receipt patterns already exist. |
| Morgan integration | Consume orchestration context packet rather than inventing a second orchestration stack | Morgan is already the orchestration authority for hard-coded gates and sequencing patterns. |
| Downstream handoff | Introduce a formal runtime input packet for Epic 5, while also guarding current `content_machine` paths | This spec must protect current pipelines and prepare the clean handoff for the next epic. |
| Failure mode | Safe block with actionable fallback instead of silent pass-through | Any silent bypass would destroy Trigger-First integrity. |

## 4. Plan

### Phase 1 - Models and Persistence

| Task # | Task | Output |
|---|---|---|
| 1 | Create `src/ccp/models/trigger_first_guard_models.py` | Typed intent, source, prompt, block, capture, and resume models |
| 2 | Extend `src/ccp/scripts/setup_supabase.py` | New tables, enums, indexes, and uniqueness constraints |
| 3 | Add `TriggerBlockSessionRepository` | Session, prompt, capture, and resume persistence helpers |

### Phase 2 - Guard and Prompt Derivation

| Task # | Task | Output |
|---|---|---|
| 4 | Implement `MorganExecutionContextAdapter` | Normalize execution intent and orchestration context into a guard-safe packet |
| 5 | Implement `AuthenticatedSourceResolver` | Deterministic pass/fail validation for source dependency presence and freshness |
| 6 | Implement `PsychPromptEnvelopeResolver` | Deterministic psychological envelope from `PsychVariableMatrix.resolve(...)` |
| 7 | Implement `ProvocationPromptDeriver` | Contextual provocative prompt templates tied to original intent classes |
| 8 | Implement `TelegramVoiceModalLauncher` | Launch payload for Telegram voice capture flow |

### Phase 3 - Capture Completion and Resume

| Task # | Task | Output |
|---|---|---|
| 9 | Implement `ReactionCaptureCompletionBridge` | Accept capture payload, persist it, bind it to blocked session |
| 10 | Implement `ArchetypeRuntimeResumeBridge` | Emit runtime-ready packet to Epic 5 boundary or guarded fallback path |
| 11 | Implement `ContentMachinePassGate` | Prevent current content execution from running without authenticated source |
| 12 | Implement `TriggerFirstExecutionGuardService` | Single orchestration facade for evaluate, block, capture-complete, and resume |

### Phase 4 - API and Transport Integration

| Task # | Task | Output |
|---|---|---|
| 13 | Add FastAPI router module under `src/ccp/api/` | Evaluate, session read, capture-complete, and resume endpoints |
| 14 | Register new routes in `src/ccp/api/main.py` | Guard routes live in API gateway |
| 15 | Add guard-aware resume branch to `src/ccp/agents/vidye_router.py` | Voice captures return to the correct blocked request |

### Phase 5 - Verification and Hardening

| Task # | Task | Output |
|---|---|---|
| 16 | Add receipt logging across all transitions | Full auditability of pass, block, prompt, capture, and resume |
| 17 | Add unit tests for source resolution and prompt derivation | Deterministic guard behavior verification |
| 18 | Add integration tests for block-to-capture-to-resume flow | End-to-end M-04 enforcement |

## 5. Schema

**New model file:** `src/ccp/models/trigger_first_guard_models.py`

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
    source_capture: CoachResponseCapturePacket | None = None
    prompt_packet: ProvocationPromptPacket | None = None
    telegram_launch: TelegramVoiceLaunchPacket | None = None
    rationale: str = Field(..., min_length=8, max_length=320)
    decided_at: datetime


class ArchetypeRuntimeInputPacket(BaseModel):
    guard_session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    original_intent_text: str = Field(..., min_length=8, max_length=500)
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
| `trigger_first_guard_prompts` | `prompt_id`, `guard_session_id`, `intent_class`, `headline`, `body`, `spoken_prompt`, `envelope_json`, `created_at` | unique(`guard_session_id`), index on `intent_class` |
| `trigger_first_guard_captures` | `capture_id`, `guard_session_id`, `source_asset_id`, `source_asset_url`, `source_duration_seconds`, `authenticated`, `captured_at` | unique(`guard_session_id`, `capture_id`), index on `authenticated` |
| `trigger_first_guard_resumes` | `resume_id`, `guard_session_id`, `resume_token`, `downstream_target`, `resumed`, `resumed_at` | unique(`guard_session_id`, `resume_token`) |

**Deterministic prompt-derivation table:**

| Intent Signal | PromptIntentClass | Example Prompt Shape |
|---|---|---|
| contains `wrong`, `mistake`, `myth`, `competitor`, `enemy` | `contrarian_rebuttal` | `Tell me why {target} is wrong about {topic}.` |
| contains `believe`, `stand for`, `why I`, `what I know` | `conviction_declaration` | `Say the thing you believe that most people in your industry are too careful to say.` |
| contains `pain`, `stuck`, `afraid`, `avoid`, `struggle` | `pain_revelation` | `Describe the real pain your client is sitting in that polite marketing language hides.` |
| contains `result`, `client`, `proof`, `before/after`, `win` | `transformation_proof` | `Tell me about the moment a client changed because of this principle.` |
| no strong class match | `stakes_clarifier` | `Why does this matter enough that someone should stop scrolling and listen right now?` |

**Hard guard rules:**

- `allow_execution = true` only if `source_status == present` and `source_capture.authenticated == true`
- `source_status == missing` must always return `blocked_capture_required`, never `blocked_invalid_context`
- `blocked_capture_required` decisions must include both `prompt_packet` and `telegram_launch`
- `telegram_launch.spoken_prompt` must be identical to `prompt_packet.spoken_prompt`
- resume requires exact `resume_token` match

## 6. Fallback

| Failure | Detection | User-Facing Result | System Action |
|---|---|---|---|
| No source capture | `AuthenticatedSourceResolver` returns `missing` | Instant Telegram voice-launch path with contextual prompt | Persist blocked session and prompt |
| Invalid orchestration context | `MorganExecutionContextAdapter` cannot normalize minimal request fields | Return actionable blocked-invalid-context message with retry guidance | Log receipt and do not execute compilation |
| Prompt derivation cannot classify intent | no deterministic class match | Use `stakes_clarifier` fallback prompt | Persist fallback classification explicitly |
| Capture upload fails validation | bad format, oversize, or missing file | Return capture-specific error while preserving blocked session | Keep session open for retry |
| Resume token mismatch | bad or stale token | Do not resume downstream runtime | Log security/fallback receipt, keep original session unchanged |
| Downstream runtime unavailable | resume bridge cannot hand off | Return resumable blocked state, not silent loss | Persist pending resume status and retry option |

**Hard-stop rules:**

- The system must never silently bypass the guard because prompt derivation failed.
- The system must never replace a contextual prompt with a static generic error.
- The system must never discard the blocked request after successful capture.

## 7. Tasks

1. Create `D:\Work\The Conscious Coaching Factory\src\ccp\models\trigger_first_guard_models.py`.
2. Extend `D:\Work\The Conscious Coaching Factory\src\ccp\scripts\setup_supabase.py` with the four new guard tables and indexes.
3. Create `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
4. Add `MorganExecutionContextAdapter` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
5. Add `AuthenticatedSourceResolver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
6. Add `PsychPromptEnvelopeResolver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
7. Add `ProvocationPromptDeriver` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
8. Add `TelegramVoiceModalLauncher` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
9. Add `ReactionCaptureCompletionBridge` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
10. Add `ArchetypeRuntimeResumeBridge` in `D:\Work\The Conscious Coaching Factory\src\ccp\services\trigger_first_execution_guard.py`.
11. Add `ContentMachinePassGate` wiring to `D:\Work\The Conscious Coaching Factory\src\ccp\services\content_machine.py` integration points.
12. Create `D:\Work\The Conscious Coaching Factory\src\ccp\api\trigger_first_guard.py`.
13. Register the router in `D:\Work\The Conscious Coaching Factory\src\ccp\api\main.py`.
14. Add guard-aware resume handling to `D:\Work\The Conscious Coaching Factory\src\ccp\agents\vidye_router.py`.
15. Reuse upload-validation patterns from `D:\Work\The Conscious Coaching Factory\src\ccp\api\sacred_audio.py` for capture acceptance.
16. Add unit tests in `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py`.
17. Add integration tests in `D:\Work\The Conscious Coaching Factory\tests\integration\test_fr_era3_15_trigger_first_execution_guard.py`.
18. Extend receipt coverage for pass/block/prompt/capture/resume decisions.

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

**AC3 - Prompt Derived From Original Intent**

- Given the blocked request includes original intent text
- When the guard derives the prompt
- Then the chosen prompt template reflects the request's intent class deterministically
- And the spoken prompt contains intent-specific wording rather than a generic "record your thoughts" instruction
- CBAR Mandate enforced: `Phase4-M04`
- Measurable pass condition: derived `intent_class` matches deterministic template rules and `spoken_prompt` length is between 12 and 320 characters
- FAILURE EXAMPLE: every blocked request gets the same generic recording prompt regardless of what the coach asked to create

**AC4 - Immediate Resume After Capture**

- Given the coach completes the requested voice capture
- When the capture completion endpoint accepts the authenticated audio asset
- Then the blocked session resumes into the Archetype Runtime input boundary without requiring the coach to resubmit the original execution request
- CBAR Mandate enforced: `Phase4-M04`
- Measurable pass condition: `TriggerGuardResumeResult.resumed == true` and `runtime_packet` is populated on successful resume
- FAILURE EXAMPLE: the coach records the voice note successfully but must manually go back and click "Generate" again

**Failure Example**

- The coach clicks `Generate LinkedIn Post` in AFFiNE.
- The backend responds with `Blocked: Authenticated Source Required`.
- No prompt, no voice launch path, and no resume token are returned.
- The coach has to figure out manually where to record, loses the original emotional context, and abandons the attempt.
- This is a spec failure. It violates Story 4.1, Phase4-M04, and the Trigger-First law from PRD-02.

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
| `FR-ERA3-16` (future Epic 5 runtime) | Downstream contract | Accepts `ArchetypeRuntimeInputPacket` after capture completion |

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
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `ProvocationPromptDeriver` | `derives_contrarian_prompt_from_enemy_language_intent` | prompt template classification is deterministic and intent-specific |
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `TelegramVoiceModalLauncher` | `copies_spoken_prompt_and_resume_token_into_launch_packet` | launch payload matches prompt packet and is resume-safe |
| `D:\Work\The Conscious Coaching Factory\tests\unit\test_trigger_first_execution_guard.py` | `ArchetypeRuntimeResumeBridge` | `resumes_without_resubmitting_original_request` | successful capture continues flow immediately |

### Integration Tests

Modeled on:

- `D:\Work\The Conscious Coaching Factory\tests\integration\test_cpsc_fr52_webinar_brief.py`
- `D:\Work\The Conscious Coaching Factory\tests\integration\test_ca11_fr16_studio_block.py`

Named integration tests:

- `test_blocked_execution_returns_prompt_and_telegram_launch_same_response`
- `test_capture_completion_resumes_session_into_runtime_packet`
- `test_static_error_only_response_is_never_returned_for_missing_source`

Pattern requirements:

- use helper builders for `TriggerFirstIntentPacket`, blocked sessions, and capture payloads
- assert concrete `decision`, `allow_execution`, `intent_class`, and `resumed` fields
- assert no integration path returns plain static block text without a prompt packet

### Manual Verification

1. Submit a content execution request with no authenticated source capture.
2. Confirm the API returns a blocked decision with a contextual prompt and Telegram launch payload.
3. Confirm no downstream compilation begins before capture is supplied.
4. Upload a valid voice capture tied to the blocked session.
5. Confirm the session resumes automatically without re-entering the original request.
6. Submit a request whose intent contains explicit contrarian language and verify the prompt uses the contrarian template.
7. Submit a request with an ambiguous intent and verify the deterministic fallback prompt class is `stakes_clarifier`.
8. Submit an invalid capture file and confirm the blocked session remains retryable rather than being lost.
