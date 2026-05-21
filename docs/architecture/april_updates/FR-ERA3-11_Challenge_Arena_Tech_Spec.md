# Tech-Spec: FR-ERA3-11 - Challenge Arena Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 3 - Experience Mini Apps
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new Mini App routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      Supabase tables extend `src/ccp/scripts/setup_supabase.py`, and Section 5.3 reserves
                      `startapp=challenge` for Challenge Arena.
2. PRD LOADED:        PRD-05 exact architecture definition:
                      "Even if Law28 uses a 28-day marketing frame, its real architecture should be adaptive layers
                      rather than fixed topic weeks."
3. EPIC LOADED:       "Given my continuous FR61 voice evidence and diagnostic state, When I open the Challenge Arena on
                      any given day, Then the Adaptive Engine assigns the next ritual from the 28-Command Operating
                      Layer based on my specific Capacity Track."
4. CBAR LOADED:       Phase3-M03 (Lateral Progression Rule) and Phase3-M04 (Telemetry Surfacing Rule) confirmed from
                      the Phase 3 audit. The hallucination purge also confirms `EXP-PRG-001` is wrong for this story;
                      the correct progression primitive is `EXP-PRG-002`, and Sunday Postcard must use the real
                      `EXP-FBK-004` registry name.
5. PRIMITIVES:        `experience_primitive_id: "EXP-PRG-002"` / `canonical_name: "Discover -> On-board -> Immerse -> Master -> Replay"`
                      `experience_primitive_id: "EXP-FBK-004"` / `canonical_name: "Bring the Data Forward"`
6. BACKEND:           `src/ccp/services/learning_path_builder.py` - `def recommend_next(self, client_id: str, journey_id: str, coping_position: int = 0, atlas_week: int = 0) -> Optional[NextContentRecommendation]`
                      `src/ccp/services/habit_architecture.py` - `def parse_and_verify(self, client_id: str, raw_client_message_text: str) -> HabitArchitectureTrackerRow`
                      `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, direct typed
                      assertions, class-per-scenario organization, and local `_run()` wrappers for async service calls.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P3_S16_FR-ERA3-11_Challenge_Arena.md` | 2026-05-11 | Assignment prompt, output target, and explicit M-03 / M-04 constraints |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, Mini App routing, backend extension rules, and schema extension points |
| 3 | `docs/prd/modules/PRD_05_CBCS_Law28.md` | v6.0, 2026-05-06 | Source PRD, adaptive layers, capacity tracks, Sunday Postcard doctrine, and brownfield inventory |
| 4 | `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | 2026-05-10 | Story 2.1 and 2.2 acceptance criteria plus Phase 3 mandates |
| 5 | `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | 2026-05-10 | Audit corrections for M-03 / M-04 and primitive hallucination purge |
| 6 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Codified registry | Verified progression primitive for adaptive challenge routing |
| 7 | `primitives/experience/feedback_scoring/EXP-FBK-004.yaml` | Codified registry | Verified telemetry-surfacing primitive for Sunday Postcard |
| 8 | `src/ccp/services/learning_path_builder.py` | Existing service | Recommendation and journey constraints that Challenge Arena must consume rather than replace |
| 9 | `src/ccp/services/habit_architecture.py` | Existing service | Habit verification parser for If/Then challenge commitments |
| 10 | `src/ccp/services/trait_scoring_engine.py` | Existing service | FR61-adjacent trait evidence source for challenge readiness and postcard enrichment |
| 11 | `src/ccp/models/cbcs_models.py` | Existing models | Existing habit-verification enums and tracker row shape |
| 12 | `src/ccp/api/main.py` | 1.0.0 | FastAPI route registration and `/health` extension point |
| 13 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit trail for routing, habit, completion, and postcard events |
| 14 | `src/ccp/core/circuit_breaker.py` | Current | Crisis halt contract for challenge automation fallback |
| 15 | `src/ccp/scripts/setup_supabase.py` | Current | Existing schema bootstrap and migration extension point |
| 16 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Service-test structure, receipt assertions, and fallback-path examples |
| 17 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async helper style, integration scenario layout, and schema-constant assertions |

## 2. Overview

### 2.1 Problem Statement

PRD-05 already defines the adaptive challenge doctrine, the weekly rhythm, the FR61 evidence contract, and the Sunday Postcard ritual, but the repo does not yet contain the dedicated Telegram Mini App that turns those backend ideas into a coherent daily operating surface. The current gap creates four practical failures:

- participants can still fall into a static day-counter mentality instead of evidence-gated progression
- a vertical lock can easily degrade into the same blocked screen being shown over and over again
- habit verification exists as an isolated parser, not as part of the daily challenge loop
- Sunday summaries can collapse into generic LLM praise unless the Mini App enforces quantitative telemetry as a first-class artifact

That is exactly what Story 2.1 and Story 2.2 are trying to prevent. The backend has useful pieces, but there is no sovereign `startapp=challenge` surface that makes adaptive routing feel alive, non-stalling, and visibly cumulative.

### 2.2 Solution

This spec creates `startapp=challenge` as the Challenge Arena Mini App for the CBCS / Law28 runtime. The Mini App is not the adaptive engine itself. It is the presentation, state-projection, and mandate-enforcement layer that consumes the existing backend services and adds the missing challenge-specific orchestration:

- a formal lateral-progression state machine that guarantees forward movement when vertical advancement is blocked
- a challenge-specific adapter around `LearningPathBuilder.recommend_next(...)` so journey recommendations can be used without misusing the learning-path service as the entire challenge engine
- habit-verification checkpoints using `ImplementationIntentionParser.parse_and_verify(...)`
- FR61 evidence and trait-summary projection so readiness is visible, auditable, and explainable
- a Sunday Postcard artifact that always includes cumulative numbers, prior-week deltas, and a forecasted next unlock

### 2.3 Scope

**In scope:**
- `startapp=challenge` Telegram Mini App scaffold and routing
- adaptive daily route projection based on capacity track, layer, and evidence state
- formal M-03 lateral-progression fallback
- session-index progression that continues even when conceptual layer escalation is locked
- habit-intention capture and verification
- daily drill completion and telemetry rollup capture
- Sunday Postcard rendering and acknowledgement flow
- receipt logging and crisis-halt compatibility

**Out of scope:**
- rebuilding FR61 extraction itself
- replacing `learning_path_builder.py`, `habit_architecture.py`, or `trait_scoring_engine.py`
- generic leaderboard or guild gameplay beyond what PRD-05 explicitly needs
- public User Card rendering, which belongs to FR-ERA3-19
- Notion calendar-based challenge progression
- live synchronous coaching dependencies as the primary challenge path

## 3. Context for Development

### 3.1 Architecture Traceability

| ID | Data Object / Component | Source FR | What It Does |
|---|---|---|---|
| UI-CHA-ARE-001 | `ChallengeArenaAppShell` | FR-ERA3-11 | Standalone Telegram Mini App loaded by `startapp=challenge` |
| ENG-CHA-ARE-002 | `ChallengeArenaSessionResolver` | Story 2.1 | Resolves participant state into the current day/session projection |
| DEP-CHA-ARE-003 | `LateralProgressionState` | Story 2.1 | Data object representing the current capacity track, layer, and lateral routing state |
| ENG-CHA-ARE-004 | `AdaptiveLayerStateMachine` | Phase3-M03 | Formal vertical-vs-lateral routing state machine with deterministic transitions |
| SVC-CHA-ARE-005 | `LateralVariationLedger` | Phase3-M03 | Prevents the same locked variation from being served on consecutive eligible routing cycles |
| DEP-CHA-ARE-006 | `ChallengeAssignment` | Story 2.1 | Data object representing the resolved daily drill assignment and metadata |
| SVC-CHA-ARE-007 | `HabitVerificationAdapter` | Story 2.1 | Adapts `parse_and_verify(...)` outputs into challenge-session gates |
| DEP-CHA-ARE-008 | `Fr61EvidenceSnapshot` | Story 2.1 / Story 2.2 | Data object containing raw FR61 metrics and optional trait summaries |
| DEP-CHA-ARE-009 | `WeeklyTelemetryRollup` | Story 2.2 / Phase3-M04 | Data object containing aggregated hard weekly metrics and prior-week deltas |
| DEP-CHA-ARE-010 | `SundayPostcardProjection` | Story 2.2 | Data object representing the private weekly coaching artifact |
| DEP-CHA-ARE-011 | `ChallengeArenaSessionProjection` | FR-ERA3-11 | Canonical API payload containing the fully resolved daily challenge state |
| SVC-CHA-ARE-012 | `ChallengeArenaAuditBridge` | FR-ERA3-11 | Logs every route, lock, lateral fallback, session completion, postcard publication, and acknowledgement to the Receipt Chain |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `learning_path_builder.py` | `src/ccp/services/learning_path_builder.py` | Consumes `recommend_next(...)` as a candidate-selector for challenge drill journeys; this spec explicitly does not convert the learning-path service into the challenge state machine |
| `habit_architecture.py` | `src/ccp/services/habit_architecture.py` | Consumes `parse_and_verify(...)` to validate the participant's daily If/Then commitment and stores the result alongside the challenge session |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Consumes `score_all_traits()` as supplementary readiness evidence and postcard enrichment, while raw FR61 metrics remain the hard gating source |
| `cbcs_models.py` | `src/ccp/models/cbcs_models.py` | Reuses `HabitArchitectureTrackerRow`, `HabitStatus`, and `HabitVerificationVerdict`; notably, it does not yet define `ProgramProgressRecord`, `CapacityTrackAssignment`, or Sunday Postcard models |
| `main.py` | `src/ccp/api/main.py` | Registers the Challenge Arena router and extends `/health` with challenge readiness |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs route resolutions, locked-vertical decisions, lateral variation assignments, habit verdicts, session completions, and postcard publications |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Halts automated routing and postcard delivery when challenge submissions surface crisis patterns |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends the canonical schema with challenge-specific tables and indexes |

**Existing database tables consumed:**
- `person_registry` - participant identity resolution from Telegram
- `asset_registry` - challenge asset IDs, postcard artifacts, and optional downloadable drill attachments
- `receipt_chain` - immutable event logging
- `content_performance` - optional downstream joins for challenge-generated content and evidence provenance

**New challenge tables introduced by this spec:**
- `challenge_arena_participants` - participant-level adaptive state, capacity track, layer, and current session counters
- `challenge_arena_sessions` - one row per routed challenge session, including command, variation, readiness verdict, and completion status
- `challenge_arena_variation_history` - ledger preventing consecutive repeat locked-screen assignments
- `challenge_arena_weekly_rollups` - quantitative weekly telemetry aggregates and delta snapshots
- `challenge_arena_sunday_postcards` - private postcard artifact records and acknowledgement timestamps

**Existing API routes extended or called:**
- `GET /health` - extended with Challenge Arena readiness
- `POST /api/sacred-audio/upload` - existing audio ingestion route used by challenge recordings
- `GET /api/challenge/{participant_id}` - current challenge projection
- `POST /api/challenge/{participant_id}/daily-route` - resolve today's assignment
- `POST /api/challenge/{participant_id}/habit-intention` - verify If/Then commitment
- `POST /api/challenge/{participant_id}/session-complete` - finalize session telemetry and evidence snapshot
- `GET /api/challenge/{participant_id}/postcard/current` - fetch current Sunday Postcard
- `POST /api/challenge/{participant_id}/postcard/ack` - mark the weekly artifact as seen

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | The challenge surface must evolve with maturity while still preserving visible motion. A participant can remain in the same conceptual layer, but the challenge interaction must still progress through new, different, and interpretable assignments. |
| `EXP-FBK-004` | Bring the Data Forward | feedback_scoring | The Sunday Postcard must surface cumulative, undeniable work already performed. Numbers are mandatory and must be placed before any LLM interpretation layer. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| Lateral Progression Rule | Phase3-M03 | Story 2.1 | `AdaptiveLayerStateMachine` separates conceptual advancement from visible session movement. When vertical advancement fails, the session is re-routed into a different variation inside the same layer and the route is persisted in `challenge_arena_variation_history`. |
| Telemetry Surfacing Rule | Phase3-M04 | Story 2.2 | `WeeklyTelemetryRollupEngine` computes `cumulative_words_spoken`, `cumulative_micro_pauses`, `sessions_completed`, and prior-week deltas before `SundayPostcardAssembler` is allowed to render narrative copy. A postcard without hard numbers is invalid. |

**Formal state machine for Phase3-M03**

| State | Entry Condition | Allowed Transition | Hard Rule |
|---|---|---|---|
| `route_evaluation_pending` | Participant opens Challenge Arena or previous session closes | `vertical_candidate_selected` or `vertical_gate_blocked` | Routing always begins from current evidence and track, never from a static day number alone |
| `vertical_candidate_selected` | Next layer candidate exists and readiness check passes | `habit_verification_pending` | Candidate may change layer only if exact evidence thresholds pass (`conviction_density >= 0.85` and `hedge_frequency <= 2.0`) |
| `vertical_gate_blocked` | Readiness check fails for next layer (`conviction_density < 0.85` or `hedge_frequency > 2.0`) | `lateral_variation_selected` | A blocked vertical path may not render a dead-end screen |
| `lateral_variation_selected` | Same-layer alternate variation exists | `habit_verification_pending` | `variation_key` must differ from the most recent completed-or-expired locked assignment for that participant and layer |
| `habit_verification_pending` | Assignment chosen | `session_in_progress` or `habit_revision_requested` | `parse_and_verify(...)` FAIL requires a rewrite prompt; PROVISIONAL may proceed with a warning banner |
| `session_in_progress` | Participant started the drill | `session_completed` or `session_abandoned` | Completion always emits telemetry and a receipt event |
| `session_completed` | Evidence snapshot persisted | `route_evaluation_pending` or `weekly_postcard_pending` | `session_index` increments on every completed routed session, including lateral sessions |
| `weekly_postcard_pending` | Weekly cadence boundary reached | `weekly_postcard_published` | Postcard generation is blocked until quantitative rollup is complete |
| `weekly_postcard_published` | Postcard row persisted | `route_evaluation_pending` | Postcard acknowledgement does not change the layer; it only closes the weekly reflection loop |

**Non-negotiable M-03 invariants**

- `session_index` is the visible forward-motion counter; it increments on every completed challenge session regardless of whether `current_layer` changed.
- `current_layer` changes only on vertical unlock.
- If the participant refreshes the app during the same active session, the same unresolved assignment may be shown again. The no-repeat rule applies to the next eligible routing cycle after completion, expiry, or explicit skip.
- `ui_route_fingerprint = "{layer}:{command_key}:{variation_key}"` may not equal the previous locked-cycle fingerprint for the same participant and same layer on the next eligible routing cycle.
- `notion_content_builder.py` is explicitly barred from acting as the progression gatekeeper. Calendar position may decorate memory views only.

**Non-negotiable M-04 invariants**

- `cumulative_words_spoken`, `cumulative_micro_pauses`, and `sessions_completed` are required numeric fields in every published Sunday Postcard.
- At least one delta metric versus the prior week is required.
- The qualitative interpretation must quote or reference specific numeric fields.
- A postcard may fall back to a numbers-only render if narrative generation fails, but it may never fall back to narrative-only.

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Build a challenge-specific adapter around `LearningPathBuilder` | The existing service can recommend next journey nodes, but it is not the full adaptive challenge orchestrator | Move all challenge logic directly into `learning_path_builder.py` | Blurs service boundaries and turns a registry/journey service into a monolith |
| Track visible movement via `session_index`, not just `current_layer` | M-03 requires the participant to feel forward motion even while conceptually locked | Show only the layer name and keep the day/session label frozen | Produces the churn pattern the audit explicitly warns about |
| Store lateral variation history in its own ledger | M-03 needs deterministic no-repeat enforcement | Infer no-repeat only from the latest session row | Too brittle once retries, skipped sessions, and expired sessions exist |
| Keep `parse_and_verify(...)` as the verification engine and adapt its outputs | The parser already returns typed verdicts and statuses | Re-implement habit parsing inside the Mini App | Duplicates tested logic and creates divergent verdict semantics |
| Use raw FR61 metrics as the vertical gate, with trait summaries as secondary context | The prompt ties challenge progression to FR61 evidence, while `TraitScoringEngine` is broader and more interpretive | Gate advancement purely by leadership trait scores | Too indirect and not aligned with the PRD's explicit speaking metrics |
| Treat Sunday Postcard as a private weekly artifact, not a public status card | PRD-05 distinguishes private reflection from public identity proof | Merge postcard and public User Card into one artifact | Conflates two different emotional jobs and crosses into FR-ERA3-19 scope |

## 4. Implementation Plan

### Phase 1 - Mini App Scaffold and Route Registration
- [ ] Create `apps/challenge-arena/package.json`
- [ ] Create `apps/challenge-arena/tsconfig.json`
- [ ] Create `apps/challenge-arena/app/layout.tsx`
- [ ] Create `apps/challenge-arena/app/page.tsx`
- [ ] Create `apps/challenge-arena/app/globals.css`
- [ ] Create `src/ccp/api/challenge_arena_api.py`
- [ ] Register the router in `src/ccp/api/main.py`

### Phase 2 - Adaptive Routing and Lateral Progression
- [ ] Create `src/ccp/models/challenge_arena_models.py`
- [ ] Create `src/ccp/services/challenge_arena_projection.py`
- [ ] Create `src/ccp/services/challenge_arena_progression.py`
- [ ] Create `src/ccp/services/challenge_journey_adapter.py`
- [ ] Map `why_now` and `prompt_text` directly from the `JourneyNode` metadata returned by `LearningPathBuilder`
- [ ] Implement `AdaptiveLayerStateMachine`
- [ ] Implement `LateralVariationLedger`
- [ ] Add `ui_route_fingerprint` generation and repeat protection
- [ ] Calculate `streak_count` and `active_days_this_week` by querying completed `challenge_arena_sessions` records within the 7-day window

### Phase 3 - Habit Verification and Evidence Completion
- [ ] Create `src/ccp/services/challenge_habit_adapter.py`
- [ ] Wire `ImplementationIntentionParser.parse_and_verify(...)` into the daily challenge flow
- [ ] Directly read and mutate the canonical `HabitArchitectureTrackerRow` via `habit_architecture.py` (no duplicate challenge habit table)
- [ ] Create `src/ccp/services/challenge_evidence_projection.py`
- [ ] Map raw FR61 metrics and optional `score_all_traits()` output into one readiness snapshot
- [ ] Add `POST /api/challenge/{participant_id}/session-complete`

### Phase 4 - Weekly Telemetry and Sunday Postcard
- [ ] Create `src/ccp/services/challenge_weekly_rollup.py`
- [ ] Create `src/ccp/services/challenge_postcard_service.py`
- [ ] Implement the `PROMPT-SYS-POSTCARD-001` LLM generation contract, injecting the `WeeklyTelemetryRollup` fields into the context window to produce the `qualitative_interpretation` and `forward_forecast`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with challenge tables and indexes
- [ ] Add `GET /api/challenge/{participant_id}/postcard/current`
- [ ] Add `POST /api/challenge/{participant_id}/postcard/ack`
- [ ] Implement quantitative fallback postcard mode for narrative-generation failures

### Phase 5 - UI Surfaces and Verification
- [ ] Create `apps/challenge-arena/app/components/session-header.tsx`
- [ ] Create `apps/challenge-arena/app/components/daily-route-card.tsx`
- [ ] Create `apps/challenge-arena/app/components/habit-intention-sheet.tsx`
- [ ] Create `apps/challenge-arena/app/components/progression-rail.tsx`
- [ ] Create `apps/challenge-arena/app/components/telemetry-strip.tsx`
- [ ] Create `apps/challenge-arena/app/components/sunday-postcard.tsx`
- [ ] Create `apps/challenge-arena/app/components/unlock-forecast.tsx`

### Phase 6 - Tests and Operational Hardening
- [ ] Create `tests/integration/test_era3_fr11_challenge_arena_api.py`
- [ ] Create `tests/integration/test_era3_fr11_challenge_arena_progression.py`
- [ ] Create `tests/integration/test_era3_fr11_sunday_postcard.py`
- [ ] Create `tests/unit/test_challenge_arena_progression.py`
- [ ] Create `tests/unit/test_challenge_weekly_rollup.py`
- [ ] Create `tests/unit/test_challenge_habit_adapter.py`
- [ ] Create `apps/challenge-arena/app/__tests__/lateral-progression-machine.test.ts`
- [ ] Create `apps/challenge-arena/app/__tests__/sunday-postcard.test.tsx`

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/challenge_arena_models.py`

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ChallengeLayer(str, Enum):
    FOUNDATION = "foundation"
    STRUCTURE = "structure"
    NUANCE = "nuance"
    COMMAND = "command"


class CapacityTrack(str, Enum):
    RECOVERY = "recovery"
    FOUNDATION = "foundation"
    GROWTH = "growth"
    MOMENTUM = "momentum"
    PEAK = "peak"


class JourneyPhase(str, Enum):
    DISCOVER = "discover"
    ONBOARD = "onboard"
    IMMERSE = "immerse"
    MASTER = "master"
    REPLAY = "replay"


class AssignmentKind(str, Enum):
    VERTICAL = "vertical"
    LATERAL = "lateral"
    RECOVERY = "recovery"


class ProgressionDecision(str, Enum):
    VERTICAL_ADVANCE = "vertical_advance"
    LATERAL_VARIATION = "lateral_variation"
    HOLD_FOR_REVISION = "hold_for_revision"


class SessionStatus(str, Enum):
    ROUTED = "routed"
    HABIT_PENDING = "habit_pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    EXPIRED = "expired"


class PostcardStatus(str, Enum):
    NOT_DUE = "not_due"
    PENDING = "pending"
    PUBLISHED = "published"
    ACKNOWLEDGED = "acknowledged"


class TraitScoreSummary(BaseModel):
    trait_id: str = Field(..., min_length=3)
    label: str = Field(..., min_length=2)
    score: int = Field(..., ge=1, le=10)


class Fr61EvidenceSnapshot(BaseModel):
    conviction_density: float = Field(..., ge=0.0, le=1.0)
    hedge_frequency: float = Field(..., ge=0.0)
    micro_pause_count: int = Field(..., ge=0)
    pitch_stability: float = Field(..., ge=0.0, le=1.0)
    words_spoken: int = Field(..., ge=0)
    evidence_captured_at: datetime = Field(...)
    trait_scores: list[TraitScoreSummary] = Field(default_factory=list)


class HabitVerificationProjection(BaseModel):
    tracker_id: UUID = Field(...)
    environmental_cue: str | None = Field(default=None, max_length=280)
    concrete_action: str | None = Field(default=None, max_length=280)
    habit_status: str = Field(...)
    verification_verdict: str = Field(...)
    last_checked_date: datetime = Field(...)


class LateralProgressionState(BaseModel):
    current_layer: ChallengeLayer = Field(...)
    capacity_track: CapacityTrack = Field(...)
    journey_phase: JourneyPhase = Field(...)
    session_index: int = Field(..., ge=1)
    layer_attempt_count: int = Field(..., ge=0)
    vertical_ready: bool = Field(...)
    blocked_reason: str | None = Field(default=None, max_length=120)
    previous_locked_fingerprint: str | None = Field(default=None, max_length=120)
    current_fingerprint: str = Field(..., min_length=3, max_length=120)
    same_screen_protection_active: bool = Field(...)


class ChallengeAssignment(BaseModel):
    assignment_id: UUID = Field(...)
    journey_id: str = Field(..., min_length=3)
    journey_node_id: str = Field(..., min_length=3)
    command_key: str = Field(..., min_length=3)
    variation_key: str = Field(..., min_length=3)
    assignment_kind: AssignmentKind = Field(...)
    decision: ProgressionDecision = Field(...)
    target_layer: ChallengeLayer = Field(...)
    target_capacity_track: CapacityTrack = Field(...)
    session_index: int = Field(..., ge=1)
    prompt_text: str = Field(..., min_length=10)
    why_now: str = Field(..., min_length=10)
    expires_at: datetime = Field(...)


class WeeklyTelemetryRollup(BaseModel):
    week_start_utc: datetime = Field(...)
    week_end_utc: datetime = Field(...)
    sessions_completed: int = Field(..., ge=0)
    cumulative_words_spoken: int = Field(..., ge=0)
    cumulative_micro_pauses: int = Field(..., ge=0)
    avg_hedge_frequency: float = Field(..., ge=0.0)
    prior_week_avg_hedge_frequency: float = Field(..., ge=0.0)
    delta_words_spoken: int = Field(...)
    delta_hedge_frequency: float = Field(...)


class SundayPostcardProjection(BaseModel):
    postcard_id: UUID = Field(...)
    participant_id: str = Field(..., min_length=3)
    coach_id: str = Field(..., min_length=3)
    status: PostcardStatus = Field(...)
    telemetry: WeeklyTelemetryRollup = Field(...)
    qualitative_interpretation: str = Field(..., min_length=20)
    forward_forecast: str = Field(..., min_length=10)
    published_at: datetime = Field(...)
    acknowledged_at: datetime | None = Field(default=None)


class ChallengeArenaSessionProjection(BaseModel):
    startapp: Literal["challenge"] = Field(default="challenge")
    participant_id: str = Field(..., min_length=3)
    coach_id: str = Field(..., min_length=3)
    current_state: LateralProgressionState = Field(...)
    assignment: ChallengeAssignment = Field(...)
    latest_habit_verification: HabitVerificationProjection | None = Field(default=None)
    latest_evidence: Fr61EvidenceSnapshot | None = Field(default=None)
    postcard_status: PostcardStatus = Field(...)
    streak_count: int = Field(..., ge=0)
    active_days_this_week: int = Field(..., ge=0, le=7)


class ChallengeDailyRouteRequest(BaseModel):
    participant_id: str = Field(..., min_length=3)
    coach_id: str = Field(..., min_length=3)
    journey_id: str = Field(..., min_length=3)
    coping_position: int = Field(..., ge=0)
    atlas_week: int = Field(..., ge=0)
    current_layer: ChallengeLayer = Field(...)
    capacity_track: CapacityTrack = Field(...)


class ChallengeSessionCompletionRequest(BaseModel):
    participant_id: str = Field(..., min_length=3)
    assignment_id: UUID = Field(...)
    words_spoken: int = Field(..., ge=0)
    micro_pause_count: int = Field(..., ge=0)
    conviction_density: float = Field(..., ge=0.0, le=1.0)
    hedge_frequency: float = Field(..., ge=0.0)
    pitch_stability: float = Field(..., ge=0.0, le=1.0)
    completed_at: datetime = Field(...)
```

**Schema notes**

- Every major data object maps to a registered DEP-ID from Section 3.1: `LateralProgressionState` (DEP-CHA-ARE-003), `ChallengeAssignment` (DEP-CHA-ARE-006), `Fr61EvidenceSnapshot` (DEP-CHA-ARE-008), `WeeklyTelemetryRollup` (DEP-CHA-ARE-009), `SundayPostcardProjection` (DEP-CHA-ARE-010), and `ChallengeArenaSessionProjection` (DEP-CHA-ARE-011).
- `ChallengeArenaSessionProjection` is the canonical Mini App payload returned by `GET /api/challenge/{participant_id}` and `POST /api/challenge/{participant_id}/daily-route`.
- `session_index` is intentionally separate from `target_layer`. This is the key structural requirement behind M-03.
- `current_fingerprint` is persisted to enforce the no-repeat locked-screen rule.
- `WeeklyTelemetryRollup` makes the mandatory Sunday numeric fields unskippable at the type level.
- `qualitative_interpretation` is typed as required but may be filled by a deterministic template when generative narrative fails.

## 6. Backward Compatibility Fallback

This feature must fail soft without collapsing the challenge loop. All challenge orchestration services must be wrapped with the existing `CircuitBreaker` and a challenge-specific degraded-mode policy.

| Failure Mode | Detection | Fallback Behavior | Circuit Breaker Interaction |
|---|---|---|---|
| `LearningPathBuilder.recommend_next(...)` returns `None` for a participant with an otherwise valid journey | No candidate returned after prerequisite and gating checks | Reuse the most recent unresolved safe assignment if it has not expired; otherwise route a deterministic same-layer recovery variation tagged `assignment_kind="recovery"` | No circuit breaker unless the user submission itself contains crisis language |
| Habit parser fails or returns malformed output | Exception or invalid tracker row | Accept a provisional manual intent capture, mark `verification_verdict="PROVISIONAL"`, and allow session start with a visible revision banner | No circuit breaker by default |
| Trait scoring enrichment unavailable | `score_all_traits()` throws or upstream bundle missing | Proceed with raw FR61 numeric gating only (`conviction_density >= 0.85`, `hedge_frequency <= 2.0`) and mark `trait_scores=[]` in the session projection | No circuit breaker by default |
| Sunday qualitative generation fails | Narrative assembler error or timeout | Publish a numbers-first postcard using a deterministic sentence template that references `sessions_completed`, `cumulative_words_spoken`, and one delta field | No circuit breaker by default |
| User submission contains crisis patterns | `CircuitBreaker.scan_for_crisis(...)` returns `True` | Halt route refreshes, suppress postcard nudges, and stop automated prompts for that participant until reset | Circuit breaker activates immediately and coach notification path is used |

**Fallback rules**

- A fallback may reduce polish but may not violate M-03 or M-04.
- Quantitative postcard delivery is higher priority than qualitative wording.
- Lateral fallback is still mandatory in degraded mode; a service outage is not permission to show a dead-end lock screen.

## 7. Tasks

| Task ID | Task | Primary Artifact | Done When |
|---|---|---|---|
| CHA-01 | Build Challenge Arena Mini App shell | `apps/challenge-arena/` | Telegram opens `startapp=challenge` into a branded app shell |
| CHA-02 | Define canonical challenge models | `challenge_arena_models.py` | API and frontend consume one shared typed contract |
| CHA-03 | Implement route projection service | `challenge_arena_projection.py` | Participant open returns a complete session projection |
| CHA-04 | Implement lateral progression machine | `challenge_arena_progression.py` | Vertical locks always produce an alternate same-layer assignment |
| CHA-05 | Implement variation ledger | `challenge_arena_variation_history` | Consecutive eligible locked routes cannot repeat the same fingerprint |
| CHA-06 | Adapt `LearningPathBuilder` for challenge drill routing | `challenge_journey_adapter.py` | Challenge uses journey recommendations without mutating the builder service contract |
| CHA-07 | Wire habit verification into the daily loop | `challenge_habit_adapter.py` | If/Then submissions create typed verification rows attached to sessions |
| CHA-08 | Persist session completions and FR61 metrics | `challenge_arena_sessions` | Every completion stores numeric evidence required for progression and postcards |
| CHA-09 | Build weekly telemetry rollup service | `challenge_weekly_rollup.py` | Weekly rollup computes hard numbers and deltas from session data |
| CHA-10 | Build Sunday Postcard service | `challenge_postcard_service.py` | Postcard rows cannot publish without telemetry payloads |
| CHA-11 | Register API routes and health checks | `challenge_arena_api.py`, `main.py` | FastAPI serves challenge routes and readiness data |
| CHA-12 | Extend Supabase schema | `setup_supabase.py` | All challenge tables and indexes exist in one canonical migration entrypoint |
| CHA-13 | Add receipt logging on every critical branch | `receipt_chain.py` calls | Route, lock, lateral, completion, postcard, and ack events are auditable |
| CHA-14 | Add crisis-halt compatibility | `circuit_breaker.py` integration | Challenge automation stops correctly for flagged users |
| CHA-15 | Add backend unit and integration tests | `tests/unit/`, `tests/integration/` | M-03 and M-04 are tested directly, not inferred |
| CHA-16 | Add frontend projection and postcard tests | `apps/challenge-arena/app/__tests__/` | Visible progression and telemetry rendering are deterministic |

## 8. Acceptance Criteria

### AC-2.1A - Capacity Track Routing

**Given** a participant opens Challenge Arena with a resolved `capacity_track`, `current_layer`, and valid challenge journey,  
**When** the app requests the next route,  
**Then** the route returned by `ChallengeJourneyAdapter` must include one concrete assignment from the 28-command operating layer, scoped to that participant's track and current maturity phase, and the payload must state both `target_capacity_track` and `target_layer`.

**Mandate reference:** Story 2.1 baseline AC, supports Phase3-M03 by making the current route explicit before fallback logic is applied.

**Failure example:** The participant is in `capacity_track="recovery"` with weak recent evidence, but the API returns a generic `"Speak for 5 minutes on any topic"` card with no track label, no layer, and no `command_key`. This is a spec violation because the system is not actually routing from a typed challenge state.

### AC-2.1B - Lateral Progression Fallback

**Given** a participant's evidence fails the vertical threshold for the next layer,  
**When** `AdaptiveLayerStateMachine` evaluates the route,  
**Then** the system must issue a `decision="lateral_variation"` assignment in the same layer with a different `variation_key` from the previous eligible locked routing cycle, and the `session_index` shown in the UI must continue to progress after completion even though `current_layer` does not change.

**Mandate reference:** Phase3-M03 Lateral Progression Rule.

**Failure example:** A participant is blocked from moving from Foundation to Structure on Monday. On Tuesday the app shows the exact same locked Foundation card, same text, same `variation_key`, and the same `"Day 3"` label. This is a direct M-03 failure and must be rejected.

### AC-2.1C - Habit Verification Gate

**Given** the participant receives a routed daily assignment,  
**When** they submit their pre-session intent statement,  
**Then** `parse_and_verify(...)` must produce a stored verification row and the UI must distinguish PASS, PROVISIONAL, and FAIL exactly as returned by the existing habit service. FAIL must request a revision before recording begins; PROVISIONAL may proceed with a visible warning.

**Mandate reference:** Supports Story 2.1 by ensuring the daily ritual is attached to a concrete implementation intention rather than a vague aspiration.

**Failure example:** The participant writes `"I should speak more"` and the app quietly marks the habit verified without cue extraction, action extraction, or any displayed verdict. This is a spec violation because the challenge loop has bypassed the verification engine it is required to consume.

### AC-2.2A - Quantitative Sunday Postcard

**Given** the participant has reached the weekly cadence boundary,  
**When** Sunday Postcard generation runs,  
**Then** the published artifact must include `sessions_completed`, `cumulative_words_spoken`, and `cumulative_micro_pauses` as hard numbers, plus at least one prior-week delta metric.

**Mandate reference:** Phase3-M04 Telemetry Surfacing Rule.

**Failure example:** The postcard says only `"You showed up bravely this week and your confidence is growing"` with no numbers, no session count, and no delta. This is a direct M-04 failure and must be rejected.

### AC-2.2B - Interpreted but Evidence-Grounded Postcard

**Given** a valid quantitative rollup exists,  
**When** the qualitative interpretation is rendered,  
**Then** the interpretation must reference specific numeric telemetry and end with a forward forecast naming the next layer or drill unlocking path.

**Mandate reference:** Story 2.2 and Phase3-M04.

**Failure example:** The postcard includes numbers at the top but the narrative says only `"Keep going, greatness is coming"` and does not mention any measured behavior or any next unlock. This is a spec violation because the interpretation layer has detached from the evidence layer.

## 9. Dependencies

| Dependency | Type | Why It Is Required |
|---|---|---|
| `src/ccp/services/learning_path_builder.py` | Internal service | Provides journey-aware `recommend_next(...)` candidate selection |
| `src/ccp/services/habit_architecture.py` | Internal service | Provides typed If/Then habit verification |
| `src/ccp/services/trait_scoring_engine.py` | Internal service | Provides optional scored-trait enrichment for readiness and postcard context |
| `src/ccp/models/cbcs_models.py` | Internal models | Supplies existing habit status and verification vocabularies |
| `src/ccp/core/receipt_chain.py` | Core platform | Mandatory audit trail for all route and postcard mutations |
| `src/ccp/core/circuit_breaker.py` | Core platform | Mandatory automation halt path for crisis signals |
| `src/ccp/api/main.py` | API gateway | Required registration point for all new challenge endpoints |
| `src/ccp/scripts/setup_supabase.py` | Schema bootstrap | Required migration extension point for challenge persistence |
| Supabase / PostgreSQL | External platform service | Stores participant state, session history, and weekly rollups |
| Telegram Web App API | External platform service | Hosts `startapp=challenge` Mini App session and user context |
| Existing sacred audio upload path | Existing platform route | Receives challenge-session recordings for evidence generation |

## 10. Testing Strategy

The testing style must mirror the existing integration suite: helper builders for service setup, direct typed assertions, scenario-grouped test classes, and local `_run()` wrappers for async endpoints where needed.

### Unit tests

- `tests/unit/test_challenge_arena_progression.py::TestAdaptiveLayerStateMachine::test_vertical_ready_promotes_layer`
  Verifies that a passing evidence packet yields `decision="vertical_advance"` and updates `target_layer`.

- `tests/unit/test_challenge_arena_progression.py::TestAdaptiveLayerStateMachine::test_vertical_blocked_assigns_different_variation`
  Verifies M-03 directly by asserting the new `variation_key` differs from the prior eligible locked routing cycle.

- `tests/unit/test_challenge_arena_progression.py::TestAdaptiveLayerStateMachine::test_session_index_advances_on_lateral_completion`
  Verifies visible forward motion continues even when conceptual layer remains unchanged.

- `tests/unit/test_challenge_habit_adapter.py::TestHabitVerificationAdapter::test_fail_verdict_blocks_session_start`
  Confirms FAIL from `parse_and_verify(...)` forces a revision state instead of silently allowing recording.

- `tests/unit/test_challenge_weekly_rollup.py::TestWeeklyTelemetryRollup::test_postcard_requires_all_mandated_numeric_fields`
  Verifies `sessions_completed`, `cumulative_words_spoken`, and `cumulative_micro_pauses` are required before publication.

- `apps/challenge-arena/app/__tests__/lateral-progression-machine.test.ts`
  Verifies the frontend correctly renders lateral fallback copy and does not relabel a lateral session as a vertical unlock.

- `apps/challenge-arena/app/__tests__/sunday-postcard.test.tsx`
  Verifies the postcard UI renders the mandatory numeric telemetry before the qualitative paragraph.

### Integration tests

- `tests/integration/test_era3_fr11_challenge_arena_api.py`
  End-to-end API test for route resolution, habit verification, session completion, and receipt logging.

- `tests/integration/test_era3_fr11_challenge_arena_progression.py`
  Multi-session scenario proving that a blocked participant receives different same-layer variations across eligible cycles and that `session_index` still increments.

- `tests/integration/test_era3_fr11_sunday_postcard.py`
  Weekly scenario proving quantitative rollup fields, prior-week deltas, fallback postcard behavior, and acknowledgement persistence.

### Mandatory assertions

- Assert the response model is `ChallengeArenaSessionProjection` or `SundayPostcardProjection`, not an untyped dict shape.
- Assert every route mutation writes a receipt entry with action names that distinguish `vertical_route`, `lateral_route`, `habit_verdict`, `session_complete`, and `postcard_publish`.
- Assert `challenge_arena_variation_history` prevents repeated `ui_route_fingerprint` values on consecutive eligible locked cycles.
- Assert the postcard cannot publish when any mandated numeric telemetry field is missing.
- Assert circuit-breaker activation suppresses future automated route refreshes for that participant until reset.

### Manual QA checklist

1. Launch `startapp=challenge` and confirm the participant lands on a typed daily route rather than a generic dashboard.
2. Force a vertical unlock pass and confirm the layer changes.
3. Force a vertical unlock fail twice in a row and confirm the second eligible route uses a different same-layer variation.
4. Submit one FAIL and one PROVISIONAL habit statement and confirm the UI behavior differs.
5. Complete enough sessions to trigger a weekly postcard and confirm the artifact contains the three mandated numbers plus one delta.
6. Trigger the quantitative fallback postcard path and verify the weekly artifact still publishes with numbers-first content.
