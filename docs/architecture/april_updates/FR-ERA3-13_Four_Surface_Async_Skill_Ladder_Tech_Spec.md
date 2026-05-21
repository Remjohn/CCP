# Tech-Spec: FR-ERA3-13 - Four-Surface Async Skill Ladder
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.1 (CBAR Revision Updates)
**Phase:** 4 - Pipelines & Engines
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      schema changes extend `src/ccp/scripts/setup_supabase.py`, Section 3 requires explicit
                      reuse of existing backend services, and the protocol's CBAR note requires every mandate to
                      be declared explicitly rather than left implicit.
2. PRD LOADED:        PRD-04 exact architecture definition: "The new experience center is the async-first
                      communication skill ladder: 1. Law28 Public Speaking 2. Webinar Sales Delivery 3.
                      Networking Conversations Mastery (OFAP) 4. Social Co-Creations Charisma / Conscious
                      Reactions." PRD-04 also defines the central runtime object table: "ExperienceStatePacket |
                      current user state, stage, momentum level, safety profile, active surface." Brownfield
                      exact requirement: "Shift the primary experience layer to four async-first skill surfaces
                      (Law28 Public Speaking, Webinar Sales Delivery, Networking Mastery, Conscious Reactions)
                      that compound daily. Move definitively away from high-friction live/synchronous events."
3. EPIC LOADED:       Phase 4 exact FR line: "FR-ERA3-13 (Four-Surface Async Skill Ladder):" in Epic 3. Story
                      3.1 first AC: "Given my `ExperienceStatePacket` dictates my next developmental task, When
                      I interact with the system via Telegram voice notes, Then the backend routes my practice
                      into the correct surface (Law28, Webinar, Networking, or Social) and returns me to the
                      next logical step (the reward, the scorecard, or the rebuttal prompt) inline within < 3
                      seconds, And the corresponding content exhaust is generated automatically without requiring
                      a separate batch processing step."
4. CBAR LOADED:       Phase4-M03 confirmed from the Phase 4 audit. Exact rewrite demand: the `ExperienceStatePacket`
                      routing must execute inline and instantly (< 3 seconds) regardless of surface. The failure
                      case is a voice note that enters a deferred "Processing..." path and severs the action →
                      reward loop. Verdict in audit: REWRITE REQUIRED.
5. PRIMITIVES:        `experience_primitive_id: "EXP-PRG-001"` / `canonical_name: "Hook Cycle Velocity"`
                      `experience_primitive_id: "EXP-PRG-002"` / `canonical_name: "Discover -> On-board ->
                      Immerse -> Master -> Replay"`
6. BACKEND:           `src/ccp/services/learning_path_builder.py` - `def recommend_next(self, client_id: str, journey_id: str, coping_position: int = 0, atlas_week: int = 0) -> Optional[NextContentRecommendation]`
                      `src/ccp/services/habit_architecture.py` - `def parse_and_verify(self, client_id: str, raw_client_message_text: str) -> HabitArchitectureTrackerRow`
                      `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
                      `src/ccp/services/v2ws_interactive_service.py` - `def create_session(self) -> InteractiveV2WSState`
                      `src/ccp/services/trivianar_engine_service.py` - `def start_session(self, config: TriviaSessionConfig) -> TrivianarResult`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, explicit
                      scenario classes, concrete field assertions, and lifecycle-state assertions instead of
                      generic smoke tests. Section 10 mirrors that structure.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P4_S23_FR-ERA3-13_Four_Surface_Async_Skill_Ladder.md` | 2026-05-11 | Assignment prompt, M-03 constraint, and output target |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Required backend mapping, schema extension points, and CBAR formatting rules |
| 3 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Epic 3 story, first AC, and Inline Routing SLA wording |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | M-03 UX failure scenario and rewrite demand |
| 5 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | v6.0, 2026-05-06 | Four-surface ladder, runtime chain, core objects, and async-first doctrine |
| 6 | `primitives/experience/progression_replay/EXP-PRG-001.yaml` | Codified registry | Verified governing primitive for tight action-reward loops |
| 7 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Codified registry | Verified lifecycle-routing primitive for stage progression |
| 8 | `src/ccp/api/telegram_webhook.py` | Existing API | Telegram voice-note ingress and response-time baseline |
| 9 | `src/ccp/agents/vidye_router.py` | Existing router | Current message routing boundary and current voice-note handoff behavior |
| 10 | `src/ccp/services/learning_path_builder.py` | Existing service | Journey DAG and next-content recommendation boundary |
| 11 | `src/ccp/services/habit_architecture.py` | Existing service | Habit verification and comeback-signal boundary |
| 12 | `src/ccp/services/trait_scoring_engine.py` | Existing service | Surface-affinity and growth-snapshot scoring source |
| 13 | `src/ccp/services/v2ws_interactive_service.py` | Existing service | Webinar surface session boundary and step-lock precedent |
| 14 | `src/ccp/services/trivianar_engine_service.py` | Existing service | Existing interactive social session boundary and fast-start pattern |
| 15 | `src/ccp/models/ca11_models.py` | Existing models | `NextContentRecommendation`, `TriviaSessionConfig`, and result types |
| 16 | `src/ccp/models/cross_system_models.py` | Existing models | `InteractiveV2WSState` and phase state patterns |
| 17 | `src/ccp/models/cbcs_models.py` | Existing models | `HabitArchitectureTrackerRow` contract |
| 18 | `src/ccp/api/main.py` | 1.0.0 | FastAPI extension point for ladder routes |
| 19 | `src/ccp/core/receipt_chain.py` | Current | Immutable routing, reward, and fallback audit trail |
| 20 | `src/ccp/core/circuit_breaker.py` | Current | Crisis and unsafe-state hard-stop logic |
| 21 | `src/ccp/scripts/setup_supabase.py` | Current | Schema bootstrap extension point |
| 22 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and helper style |
| 23 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async orchestration pattern and concrete state assertions |

## 2. Overview

### 2.1 Problem Statement

PRD-04 hard-defines the experience center as an async-first four-surface skill ladder, but the current runtime still does not own that ladder as a deterministic backend system. Telegram ingress exists. `telegram_webhook.py` already targets sub-2-second responses. `VidyeRouter` already branches message types. `LearningPathBuilder`, `HabitArchitecture`, and `TraitScoringEngine` already encode progress, continuity, and developmental signals.

What is missing is the ladder runtime that turns those pieces into one coherent stateful routing engine.

Without that runtime, the experience breaks in predictable ways:

- voice notes enter generic handlers instead of surface-specific progression logic
- surface selection drifts into ad hoc or LLM-shaped routing rather than a deterministic state machine
- the next-step response can be deferred behind "Processing..." behavior, breaking Hook Cycle Velocity
- growth across Law28, Webinar, Networking, and Social cannot compound because there is no central `ExperienceStatePacket`

Epic 3 is explicitly preventing those failures. The system must decide the next surface and next action inline, within the same request cycle, and must do so using a deterministic packet and state machine rather than a probabilistic classifier.

### 2.2 Solution

This spec introduces a new backend service, `FourSurfaceAsyncRouterService`, centered on a precise `ExperienceStatePacket`.

The new ladder service adds seven orchestration layers:

- `ExperienceStateRepository` to persist and retrieve the authoritative per-user packet
- `SurfaceReadinessResolver` to project readiness for Law28, Webinar, Networking, and Social
- `MomentumAndComebackEngine` to fold habit and continuity state into routing
- `DeterministicSurfaceStateMachine` to choose the next surface and next logical step without LLM discretion
- `InlineRewardComposer` to return the reward, scorecard step, rebuttal prompt, or recovery invitation within the request
- `AsyncContentExhaustLauncher` to trigger downstream exhaust generation without deferring the user-facing route. Job mappings are deterministic: `law28` triggers `transcript_analysis_and_cmf_render`, `webinar` triggers `session_telemetry_aggregation`, `networking` triggers `ofap_connection_scoring`, and `social` triggers `reaction_clip_export`.
- `SurfaceAdapterBridge` to hand off to downstream surface executors only after the inline route is already resolved

This is not a generic orchestration broker. It is the runtime spine for PRD-04's four-surface ladder.

### 2.3 Scope

**In scope:**

- precise `ExperienceStatePacket` model and persistence
- deterministic routing across Law28, Webinar, Networking/OFAP, and Social Reaction
- inline route decision and next-step response under 3 seconds
- explicit inline-vs-background operation contract
- reuse of journey DAGs, habit state, and trait score snapshots
- Telegram voice-note ingress integration
- routes for packet load, voice-note routing, state advance, and health
- downstream handoff contracts for Webinar and Social session start patterns
- fallback logic that avoids "Processing..." dead ends

**Out of scope:**

- replacing Telegram webhook ingress
- replacing `LearningPathBuilder`, `HabitArchitecture`, or `TraitScoringEngine`
- rebuilding the full internals of Law28, OFAP, Webinar, or Conscious Reactions
- live synchronous rooms or WebRTC practice flows
- heavy transcript analysis, CMF rendering, or deep content compilation as inline operations

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-LAD-001 | `ExperienceStatePacket` | Story 3.1 | Canonical routing object holding stage, surface, momentum, safety, readiness, and next-step state |
| DEP-LAD-002 | `SurfaceReadinessSnapshot` | Story 3.1 | Snapshot of per-surface readiness derived from learning path and scoring signals |
| DEP-LAD-003 | `RouteDecisionPacket` | Story 3.1 / M-03 | Deterministic record of surface choice, transition reason, and SLA latency |
| DEP-LAD-004 | `InlineRewardPacket` | Story 3.1 / M-03 | Immediate next-step response payload generated within the SLA window |
| DEP-LAD-005 | `AsyncExhaustJob` | Story 3.1 | Downstream background generation request object created after inline response |
| DEP-LAD-006 | `VoiceNoteIngressPacket` | FR-ERA3-13 | Standardized payload for Telegram voice-note entry into the routing system |
| DEP-LAD-007 | `RouteVoiceNoteRequest` | FR-ERA3-13 | Top-level API request payload for voice-note routing |
| DEP-LAD-008 | `RouteVoiceNoteResponse` | FR-ERA3-13 | Top-level API response payload containing the inline reward and state packet |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | Existing Telegram voice-note ingress remains the entrypoint. This spec inserts the ladder runtime after message parsing, not before webhook handling. |
| `vidye_router.py` | `src/ccp/agents/vidye_router.py` | Current voice-note path to `AriaProcessor` becomes insufficient for ladder routing. This spec introduces a deterministic bypass for voice-note ladder participants so no LLM-like classification decides the surface. |
| `learning_path_builder.py` | `src/ccp/services/learning_path_builder.py` | Uses `recommend_next(...)` against prebuilt journey DAGs for the inline `next_content` recommendation. DAG construction itself remains outside the inline SLA path. |
| `habit_architecture.py` | `src/ccp/services/habit_architecture.py` | Uses `parse_and_verify(...)` and broken-habit detection outputs to set comeback pressure, compliance confidence, and continuity flags. |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Consumes persisted or cached trait snapshots produced by `score_all_traits()` to build per-surface readiness without re-running a full rescore inline on every voice note. |
| `v2ws_interactive_service.py` | `src/ccp/services/v2ws_interactive_service.py` | Uses `create_session()` when the deterministic route moves the user into the Webinar surface and no active webinar session exists. |
| `trivianar_engine_service.py` | `src/ccp/services/trivianar_engine_service.py` | Provides an existing fast-start interactive pattern for social session activation. This spec may reuse `start_session(...)` for social reaction microgames where applicable, but it does not redefine PRD-06 internals. |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `NextContentRecommendation` and existing result-model vocabulary. |
| `cross_system_models.py` | `src/ccp/models/cross_system_models.py` | Reuses `InteractiveV2WSState` shape and phase-state design precedent. |
| `cbcs_models.py` | `src/ccp/models/cbcs_models.py` | Reuses `HabitArchitectureTrackerRow` as the continuity signal carrier. |
| `main.py` | `src/ccp/api/main.py` | Registers ladder routes and extends `/health` with ladder readiness state. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Adds durable state-packet, route-event, readiness-snapshot, and async-exhaust tables. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs route choice, inline response type, SLA timing, fallback selection, and background-launch receipts. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Continues to own crisis / hard-stop behavior before ladder routing proceeds. |

**Existing route behavior reused:**

- Telegram webhook request handling and dedup
- existing crisis scanning and command handling in the broader router stack
- existing webinar session-state contract

**New routes introduced by this spec:**

- `POST /api/experience/route-voice-note`
- `GET /api/experience/state/{client_id}`
- `POST /api/experience/state/{client_id}/advance`
- `POST /api/experience/state/{client_id}/resume`
- `GET /api/experience/health`

**New persistence tables introduced by this spec:**

- `experience_state_packets`
- `experience_route_events`
- `surface_readiness_snapshots`
- `inline_reward_packets`
- `async_content_exhaust_jobs`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-PRG-001` | Hook Cycle Velocity | progression_replay | Governing primitive. The user must receive the next logical step inside the same interaction window. No deferred "come back later" route resolution is allowed. |
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | Supporting lifecycle primitive. The packet must carry a stage value that changes routing expectations across the four surfaces. |

### 3.4 CBAR Mandates

| Mandate | Story | Required Behavior | Implementation Mechanism |
|---|---|---|---|
| Phase4-M03 - Inline Routing SLA | Epic 3 Story 3.1 | Voice-note routing across all four surfaces must complete inline within 3 seconds, and the user must receive the next logical step without a deferred processing promise. | `DeterministicSurfaceStateMachine` computes surface and next-step inline. `InlineRewardComposer` builds the response inline. `AsyncContentExhaustLauncher` starts background work only after the inline response has been committed. |

**M-03 anti-patterns explicitly forbidden:**

- no "Processing..." state that promises later surface routing
- no overnight or cron-based routing from one surface bucket to another
- no LLM-based surface choice for voice-note progression
- no requirement to wait for a live event before progression resumes
- no blocking on full trait re-score, CMF render, or heavy content compilation before returning the next step

### 3.5 Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| Central routing object | `ExperienceStatePacket` is the only authoritative route input | PRD-04 explicitly names it as the core experience object. |
| Surface choice | Deterministic state machine, not probabilistic classification | Prompt and M-03 both require deterministic routing. |
| Inline data sources | Only precomputed or O(1)/cheap reads allowed inline | The 3-second SLA cannot rely on heavy recomputation. |
| Trait scoring use | Consume latest persisted snapshot inline, refresh in background | `score_all_traits()` is valuable, but full rescoring is too expensive to be mandatory in-request. |
| Journey recommendation use | `recommend_next(...)` allowed inline only if journey DAG already exists | DAG construction is not SLA-safe; recommendation lookup is. |
| Surface adapters | Webinar uses existing session API; Law28 / Networking / Social adapters issue deterministic task tickets | Keeps the ladder focused on routing rather than re-implementing every surface. |
| Telegram integration | Voice notes enter ladder via webhook/router branch override | Current voice path is generic; ladder participants need route-aware handling. |
| Recovery logic | Habit/comeback pressure changes route priority, not only message tone | PRD-04 frames comeback as a first-class experience law. |

## 4. Plan

### Phase 1 - Models and Persistence

| Task # | Task | Output |
|---|---|---|
| 1 | Create `src/ccp/models/experience_ladder_models.py` | Typed packet, route, reward, and SLA models |
| 2 | Extend `src/ccp/scripts/setup_supabase.py` | New tables, indexes, enums, and uniqueness constraints |
| 3 | Add `ExperienceStateRepository` | Load/save packet and route-event persistence helpers |

### Phase 2 - Core Routing Inputs

| Task # | Task | Output |
|---|---|---|
| 4 | Implement `SurfaceReadinessResolver` | Per-surface readiness snapshot from journey, traits, and continuity |
| 5 | Implement `MomentumAndComebackEngine` | Momentum state, missed-day pressure, and comeback packet updates |
| 6 | Implement `TraitSurfaceAffinityProjector` | Background trait snapshot refresh, inline-safe affinity reads, and population of `last_score_band` into the packet |
| 7 | Implement `JourneyRecommendationProjector` | Inline-safe `recommend_next(...)` wrapper with cache expectations, and population of `coping_position` and `atlas_week` into the packet |

### Phase 3 - Deterministic State Machine

| Task # | Task | Output |
|---|---|---|
| 8 | Implement `DeterministicSurfaceStateMachine` | Rule table for stage × surface × momentum × recovery routing |
| 9 | Implement `InlineRewardComposer` | Immediate `reward`, `scorecard_step`, `rebuttal_prompt`, or `recovery_invitation` packet |
| 10 | Implement `AsyncContentExhaustLauncher` | Background launch contract for heavier downstream work |
| 11 | Implement `Law28SurfaceAdapter` | Deterministic practice ticket launch |
| 12 | Implement `WebinarSurfaceAdapter` | `create_session()` or session-resume bridge |
| 13 | Implement `NetworkingSurfaceAdapter` | OFAP practice ticket launch |
| 14 | Implement `SocialReactionSurfaceAdapter` | Reaction task ticket or optional fast-session bridge |

### Phase 4 - Ingress and API Integration

| Task # | Task | Output |
|---|---|---|
| 15 | Add ladder-aware voice-note branch to `vidye_router.py` | Deterministic route path for ladder participants |
| 16 | Add route API module under `src/ccp/api/` | New endpoints for route, load, resume, and advance |
| 17 | Register routes and health checks in `main.py` | Ladder service exposed through FastAPI |
| 18 | Add receipt-chain events | Route, reward, SLA, fallback, and launch audit trail |

### Phase 5 - Verification and Hardening

| Task # | Task | Output |
|---|---|---|
| 19 | Add unit tests | State machine, packet validity, and SLA-safe operation tests |
| 20 | Add integration tests | Voice-note route flow and anti-batch enforcement |
| 21 | Add timing instrumentation | Inline execution time measurement and alerting |

## 5. Schema

**New model file:** `src/ccp/models/experience_ladder_models.py`

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SurfaceType(str, Enum):
    law28 = "law28"
    webinar = "webinar"
    networking = "networking"
    social = "social"


class LadderStage(str, Enum):
    discover = "discover"
    onboard = "onboard"
    immerse = "immerse"
    master = "master"
    replay = "replay"


class MomentumLevel(str, Enum):
    low = "low"
    stable = "stable"
    rising = "rising"
    hot = "hot"


class SafetyProfile(str, Enum):
    normal = "normal"
    sensitive = "sensitive"
    cooldown_required = "cooldown_required"


class RecoveryState(str, Enum):
    none = "none"
    comeback_due = "comeback_due"
    habit_broken = "habit_broken"
    shame_sensitive = "shame_sensitive"


class NextStepType(str, Enum):
    reward = "reward"
    scorecard_step = "scorecard_step"
    rebuttal_prompt = "rebuttal_prompt"
    recovery_invitation = "recovery_invitation"
    next_drill = "next_drill"


class RouteReason(str, Enum):
    active_surface_continuation = "active_surface_continuation"
    journey_progression = "journey_progression"
    comeback_recovery = "comeback_recovery"
    surface_rotation = "surface_rotation"
    readiness_override = "readiness_override"


class SurfaceReadinessSnapshot(BaseModel):
    surface: SurfaceType
    readiness_score: float = Field(..., ge=0.0, le=1.0)
    active_task_id: str = Field(default="", max_length=120)
    has_open_session: bool = False
    journey_id: str = Field(default="", max_length=120)
    journey_content_id: str = Field(default="", max_length=120)
    recommended_action_label: str = Field(..., min_length=1, max_length=120)


class ExperienceStatePacket(BaseModel):
    packet_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    stage: LadderStage
    active_surface: SurfaceType
    momentum_level: MomentumLevel
    safety_profile: SafetyProfile
    recovery_state: RecoveryState
    current_journey_id: str = Field(default="", max_length=120)
    current_task_id: str = Field(default="", max_length=120)
    last_score_band: str = Field(default="", max_length=40)
    streak_days: int = Field(default=0, ge=0)
    missed_days: int = Field(default=0, ge=0)
    coping_position: int = Field(default=0, ge=0)
    atlas_week: int = Field(default=0, ge=0)
    readiness: list[SurfaceReadinessSnapshot] = Field(default_factory=list)
    next_step_type: NextStepType
    next_step_label: str = Field(..., min_length=1, max_length=160)
    next_prompt_text: str = Field(..., min_length=1, max_length=320)
    inline_deadline_ms: int = Field(default=3000, ge=500, le=3000)
    updated_at: datetime


class VoiceNoteIngressPacket(BaseModel):
    client_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    telegram_message_id: str = Field(..., min_length=1)
    voice_file_id: str = Field(..., min_length=1)
    voice_duration_seconds: int = Field(..., ge=1, le=600)
    submitted_at: datetime


class RouteDecisionPacket(BaseModel):
    route_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    from_surface: SurfaceType
    to_surface: SurfaceType
    reason: RouteReason
    next_step_type: NextStepType
    next_step_label: str = Field(..., min_length=1, max_length=160)
    route_latency_ms: int = Field(..., ge=0, le=3000)
    decided_at: datetime


class InlineRewardPacket(BaseModel):
    reward_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    surface: SurfaceType
    next_step_type: NextStepType
    headline: str = Field(..., min_length=1, max_length=160)
    body: str = Field(..., min_length=1, max_length=360)
    voice_prompt_job: str = Field(..., min_length=1, max_length=80)
    task_ticket_id: str = Field(default="", max_length=120)
    created_at: datetime


class AsyncExhaustJob(BaseModel):
    job_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    surface: SurfaceType
    source_route_id: str = Field(..., min_length=1)
    job_type: str = Field(..., min_length=1, max_length=120)
    status: str = Field(..., min_length=1, max_length=40)
    created_at: datetime


class RouteVoiceNoteRequest(BaseModel):
    ingress: VoiceNoteIngressPacket


class RouteVoiceNoteResponse(BaseModel):
    state_packet: ExperienceStatePacket
    route_decision: RouteDecisionPacket
    inline_reward: InlineRewardPacket
    exhaust_job: AsyncExhaustJob | None = None
```

**Supabase tables to add in `setup_supabase.py`:**

| Table | Key Columns | Constraints |
|---|---|---|
| `experience_state_packets` | `packet_id`, `client_id`, `coach_id`, `active_surface`, `stage`, `momentum_level`, `recovery_state`, `packet_json`, `updated_at` | unique(`client_id`, `coach_id`), index on `coach_id`, index on `active_surface` |
| `experience_route_events` | `route_id`, `client_id`, `coach_id`, `from_surface`, `to_surface`, `reason`, `next_step_type`, `route_latency_ms`, `created_at` | index on `client_id`, index on `to_surface`, check `route_latency_ms <= 3000` |
| `surface_readiness_snapshots` | `snapshot_id`, `client_id`, `surface`, `readiness_score`, `journey_id`, `active_task_id`, `calculated_at` | unique(`client_id`, `surface`), index on `surface`, index on `readiness_score` |
| `inline_reward_packets` | `reward_id`, `client_id`, `surface`, `next_step_type`, `headline`, `body`, `task_ticket_id`, `created_at` | index on `client_id`, index on `surface` |
| `async_content_exhaust_jobs` | `job_id`, `client_id`, `surface`, `source_route_id`, `job_type`, `status`, `created_at` | index on `source_route_id`, index on `status` |

**Inline vs background contract for M-03:**

| Operation | Execution Mode | Deadline | Notes |
|---|---|---|---|
| Telegram dedup, secret check, message parse | inline | `<250ms` | existing webhook path |
| Load latest `ExperienceStatePacket` | inline | `<150ms` | single indexed read |
| Load readiness snapshot and latest journey recommendation | inline | `<500ms` | only cached/prebuilt journey DAG lookups are allowed |
| Load latest trait snapshot | inline | `<200ms` | read only; no full re-score |
| Run deterministic state machine | inline | `<150ms` | pure in-memory rule evaluation |
| Build `InlineRewardPacket` and persist route event | inline | `<500ms` | commit before response |
| Return route response to Telegram runtime | inline | `<3000ms total` | required by M-03 |
| Full `TraitScoringEngine.score_all_traits()` refresh | background | no inline allowance | may refresh readiness after response |
| Journey DAG construction / rebuild | background | no inline allowance | `construct_journeys()` or full build is not SLA-safe |
| Heavy transcript analysis / content exhaust generation | background | kicked off inline, completed later | user-facing route is already returned |
| AFFiNE sync / deep reporting | background | kicked off inline, completed later | must not block reward loop |

**Deterministic route table:**

| Stage | Current Surface | Recovery State | Primary Route | Next Step Type |
|---|---|---|---|---|
| `discover` | any | `none` | `law28` | `next_drill` |
| `discover` | any | `comeback_due` or `habit_broken` | `law28` | `recovery_invitation` |
| `onboard` | `law28` | `none` | `law28` or `webinar` if webinar readiness > law28 readiness by `>=0.15` | `scorecard_step` |
| `immerse` | `law28` or `webinar` | `none` | highest readiness among `law28`, `webinar`, `networking` | `rebuttal_prompt` or `next_drill` |
| `master` | any | `none` | rotate to lowest-recently-served eligible surface | `reward` |
| `replay` | any | `none` | surface with highest replay-readiness and lowest friction | `reward` |
| any | any | `shame_sensitive` | keep same or simpler surface; never escalate complexity | `recovery_invitation` |

**Required deterministic invariants:**

- `recovery_state != none` overrides surface rotation and favors the lowest-friction viable surface
- no route may target a surface whose readiness score is below `0.35` unless every surface is below `0.35`
- if an active webinar session exists, `webinar` continuity beats a lateral switch unless recovery override is active
- if no packet exists, bootstrap as `discover + law28 + next_drill`
- no route choice may call an LLM or depend on free-form model judgment

## 6. Fallback

| Failure | Detection | User-Facing Behavior | System Action |
|---|---|---|---|
| No existing state packet | repository miss | user still gets a next step instantly | bootstrap default `discover` packet and write first state row |
| Journey DAG unavailable | no cached journey or `recommend_next(...)` returns `None` | route remains inline using current surface continuity drill | schedule background journey rebuild |
| Trait snapshot stale or missing | snapshot absent or older than 24 hours (86400000 ms) | use readiness defaults and keep same/lowest-friction surface | schedule background `score_all_traits()` refresh |
| Webinar adapter unavailable | `create_session()` fails | return same-request fallback drill on current or Law28 surface | log fallback receipt; do not show "Processing..." |
| Social adapter unavailable | downstream adapter error | return immediate alternative next step on Law28 or Networking | enqueue retry only after response |
| Route exceeds 3 seconds budget | timing instrumentation breach | return best known continuity step before deadline | log SLA breach receipt and degrade to no-switch route |

**Hard-stop rules:**

- No deferred "we'll compile this later" route response is allowed.
- No background rebuild may be required to decide the immediate user-facing next step.
- No fallback may wait for a live room or scheduled session before progression resumes.

## 7. Tasks

1. Create [src/ccp/models/experience_ladder_models.py](D:/Work/The Conscious Coaching Factory/src/ccp/models/experience_ladder_models.py) with the packet, route, reward, and exhaust models from Section 5.
2. Extend [src/ccp/scripts/setup_supabase.py](D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with the five new tables and indexes.
3. Add `ExperienceStateRepository` in [src/ccp/services/](D:/Work/The Conscious Coaching Factory/src/ccp/services/) for packet and route persistence.
4. Add `SurfaceReadinessResolver` to project readiness for all four surfaces using cached journey and score data.
5. Add `MomentumAndComebackEngine` to merge habit status, missed-day pressure, and comeback needs into the packet.
6. Add `TraitSurfaceAffinityProjector` to consume persisted trait snapshots and launch background refreshes when stale.
7. Add `JourneyRecommendationProjector` to wrap `LearningPathBuilder.recommend_next(...)` in an inline-safe way.
8. Add `DeterministicSurfaceStateMachine` implementing the route table and invariants in Section 5.
9. Add `InlineRewardComposer` to emit `reward`, `scorecard_step`, `rebuttal_prompt`, `recovery_invitation`, or `next_drill` packets.
10. Add `AsyncContentExhaustLauncher` so heavier content generation starts without delaying the inline response. Implement deterministic job mappings: `law28` -> `transcript_analysis_and_cmf_render`, `webinar` -> `session_telemetry_aggregation`, `networking` -> `ofap_connection_scoring`, `social` -> `reaction_clip_export`.
11. Add `Law28SurfaceAdapter` for deterministic public-speaking task tickets.
12. Add `WebinarSurfaceAdapter` using [src/ccp/services/v2ws_interactive_service.py](D:/Work/The Conscious Coaching Factory/src/ccp/services/v2ws_interactive_service.py) session creation/resume.
13. Add `NetworkingSurfaceAdapter` for OFAP-oriented async prompt tickets.
14. Add `SocialReactionSurfaceAdapter` for PRD-06 reaction-ticket launch and optional fast interactive starts.
15. Update [src/ccp/agents/vidye_router.py](D:/Work/The Conscious Coaching Factory/src/ccp/agents/vidye_router.py) so ladder participants use the deterministic ladder route for voice notes.
16. Add a new FastAPI router module under [src/ccp/api/](D:/Work/The Conscious Coaching Factory/src/ccp/api/) for route-state endpoints.
17. Register the router and health readiness checks in [src/ccp/api/main.py](D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
18. Extend [src/ccp/core/receipt_chain.py](D:/Work/The Conscious Coaching Factory/src/ccp/core/receipt_chain.py) integration calls for route, reward, SLA, fallback, and background-launch events.
19. Add unit tests for packet validation, state-machine decisions, and SLA-safe operation classification.
20. Add integration tests for Telegram voice-note routing, anti-batch enforcement, and fallback behavior.

## 8. Acceptance Criteria

### Story 3.1 - Voice-First Asynchronous Progression

**AC1 - Packet-Led Deterministic Routing**

- Given an `ExperienceStatePacket` exists for a participant
- When a Telegram voice note arrives
- Then the next surface is selected by the deterministic state machine using the packet and readiness snapshots
- And no LLM or free-form model judgment is used to choose among Law28, Webinar, Networking, or Social

**AC2 - Inline Reward Loop**

- Given a voice note enters the ladder router
- When routing completes successfully
- Then the user receives the next logical step inline within 3 seconds
- And that next step is one of `reward`, `scorecard_step`, `rebuttal_prompt`, `recovery_invitation`, or `next_drill`

**AC3 - Async-First Progression**

- Given the user's next surface would traditionally require a live event
- When the ladder computes the route
- Then it selects an async-capable next step instead of blocking on synchronous attendance
- And progression continues without waiting for a scheduled room

**AC4 - Background Exhaust Starts Without Delaying Route**

- Given the user receives an inline route response
- When corresponding content exhaust is needed
- Then the system launches the exhaust job automatically in the same request cycle
- And the user-facing response is not delayed waiting for the exhaust result

**AC5 - Recovery Overrides Complexity**

- Given the user has a comeback-due or broken-habit recovery state
- When a new voice note arrives
- Then the ladder favors the lowest-friction viable surface and a recovery-oriented next step
- And it does not escalate complexity purely because another surface has a slightly higher readiness score

**Failure Example**

- A user sends a Telegram voice note.
- The system replies with "Processing your submission. We'll sort it into the right program later tonight."
- No next step, reward, scorecard reveal, or rebuttal prompt is returned in the same interaction.
- This is a spec failure. It violates Story 3.1, Phase4-M03, `EXP-PRG-001`, and the PRD-04 async-first doctrine.

**Mandate Proof**

- M-03 is satisfied only if the route decision and next-step payload are both returned inline within 3 seconds.
- Triggering a background job alone is not compliance if the user-facing route is deferred.

## 9. Dependencies

| Dependency | Type | Why It Matters |
|---|---|---|
| `src/ccp/api/telegram_webhook.py` | Existing API ingress | Ladder runtime depends on Telegram voice-note entry |
| `src/ccp/agents/vidye_router.py` | Existing router | Current voice-note branch must be extended for deterministic ladder participants |
| `src/ccp/services/learning_path_builder.py` | Existing service | Supplies journey DAG recommendations for inline progression |
| `src/ccp/services/habit_architecture.py` | Existing service | Supplies comeback and habit-status signals |
| `src/ccp/services/trait_scoring_engine.py` | Existing service | Supplies readiness-affinity snapshots for surface routing |
| `src/ccp/services/v2ws_interactive_service.py` | Existing service | Webinar session start/resume boundary |
| `src/ccp/services/trivianar_engine_service.py` | Existing service | Optional fast-start social interaction pattern and existing session result model |
| `src/ccp/models/ca11_models.py` | Existing models | `NextContentRecommendation` and social session vocabulary |
| `src/ccp/models/cross_system_models.py` | Existing models | Webinar interactive session-state patterns |
| `src/ccp/models/cbcs_models.py` | Existing models | Habit tracker row contract |
| `src/ccp/api/main.py` | Existing API gateway | Route registration and health extension point |
| `src/ccp/scripts/setup_supabase.py` | Existing schema bootstrap | Durable packet, route, and exhaust persistence |
| `src/ccp/core/receipt_chain.py` | Cross-system infrastructure | Immutable route and SLA audit trail |
| `src/ccp/core/circuit_breaker.py` | Cross-system infrastructure | Crisis hard-stop before routing |

## 10. Testing Strategy

### Unit Tests

| Test Name | File | What It Verifies |
|---|---|---|
| `test_state_machine_routes_discover_stage_to_law28_by_default` | `tests/unit/test_four_surface_async_skill_ladder.py` | new users bootstrap into the lowest-friction Law28 drill path |
| `test_comeback_state_overrides_higher_readiness_surface` | `tests/unit/test_four_surface_async_skill_ladder.py` | recovery pressure beats raw readiness score when choosing the next surface |
| `test_inline_operation_classifier_rejects_full_trait_rescore_as_sla_safe` | `tests/unit/test_four_surface_async_skill_ladder.py` | `score_all_traits()` refresh is background-only and cannot enter the inline path |
| `test_experience_state_packet_requires_explicit_next_step_and_deadline` | `tests/unit/test_four_surface_async_skill_ladder.py` | packet validation remains strict and deterministic |

### Integration Tests

| Test Name | File | What It Verifies |
|---|---|---|
| `test_voice_note_route_returns_next_step_within_inline_budget` | `tests/integration/test_fr_era3_13_four_surface_async_skill_ladder.py` | end-to-end route returns a deterministic next step under the configured SLA |
| `test_route_response_never_returns_processing_placeholder` | `tests/integration/test_fr_era3_13_four_surface_async_skill_ladder.py` | anti-batch / anti-deferred-response rule is enforced |
| `test_webinar_route_creates_session_inline_and_enqueues_exhaust_afterward` | `tests/integration/test_fr_era3_13_four_surface_async_skill_ladder.py` | Webinar adapter uses `create_session()` without blocking on heavier downstream work |
| `test_missing_journey_snapshot_falls_back_to_same_surface_continuity_step` | `tests/integration/test_fr_era3_13_four_surface_async_skill_ladder.py` | fallback remains inline and usable when recommendation data is absent |

### Test Pattern Notes

- Follow the helper-builder style used in `test_cpsc_fr52_webinar_brief.py`.
- Follow the explicit lifecycle and status assertions used in `test_ca11_fr16_studio_block.py`.
- Assert concrete `to_surface`, `next_step_type`, `route_latency_ms`, and `job.status` values rather than only checking HTTP 200.
- Include one direct assertion that no returned string contains `Processing...` or any promise of deferred compilation.

### Minimum Verification Bar Before Merge

- all unit tests in the ladder module pass
- all new integration tests pass
- at least one integration test proves the route remains inline when a background exhaust job is still pending
- at least one integration test proves stale journey or trait data does not force a deferred response
- health checks report state repository, journey snapshot, and surface adapter readiness clearly
