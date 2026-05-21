# Tech-Spec: FR-ERA3-05a - Solo Reaction Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture - CBAR-Hardened)
**Phase:** 2 - Conscious Reactions
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms the existing FastAPI route `POST /api/sacred-audio/upload`,
                      and Section 5.1 defines Solo Reaction as `startapp=react_solo` where the coach
                      receives a topic briefing and records a constrained 2-5 minute take.
2. PRD LOADED:        "The default onboarding experience. The user receives the topic briefing and records
                      a solo take. This take is scored, timestamped, clipped, and turned into premium content.
                      It requires only one person to execute, making it the highest-velocity entry point."
3. EPIC LOADED:       "Given I complete the CORE loop, When I approve the take, Then it is evaluated against
                      a biometric threshold. If passed, it is routed to the CMF for glossy extraction
                      (`deployed_to_cmf`). If it fails, the system does NOT deploy it and instead routes me
                      to the Redemption Round."
4. CBAR AUDIT LOADED: Phase2-M04 The Earned Export Gate confirmed. Hallucination purge also confirms that
                      `EXP-TRB-*` references must be corrected to `EXP-TRS-*`, and `EXP-SFR-*` references
                      must be corrected to `EXP-SAF-*`.
5. PRIMITIVES LOADED: YAML headers verified as actually written:
                      `experience_primitive_id: "EXP-TRG-002"` / `canonical_name: "Hook Cycle Velocity"`
                      `experience_primitive_id: "EXP-FRC-003"` / `canonical_name: "The B=MAP Friction Audit"`
                      `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
                      `experience_primitive_id: "EXP-PRG-002"` / `canonical_name: "Discover -> On-board -> Immerse -> Master -> Replay"`
6. BACKEND FILES READ:`src/ccp/services/content_machine.py` -
                      `async def process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
                      from `ContentMachinePipeline`.
7. TEST PATTERN:      `tests/integration/test_ca11_fr15_dpa_engine.py` and
                      `tests/integration/test_ca11_fr19_trivianar_engine.py` both use a local `_run()` helper,
                      class-per-behavior test grouping, explicit fixture builders/constants, and direct
                      assertions against SQL/constants/service results without `pytest-asyncio`.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S05_FR-ERA3-05a_Solo_Reaction.md` | 2026-05-11 | Assignment prompt, scope boundary, required output path |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, existing backend stack, Mini App separation doctrine |
| 3 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | v6.0, 2026-05-06 | Canonical product definition, brownfield inventory, Solo FR text |
| 4 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | 2026-05-08 | Acceptance criteria, quality gates, CBAR mandates for Phase 2 |
| 5 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | 2026-05-10 | Adversarial audit and primitive hallucination corrections |
| 6 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | 2026-05-11 | Upstream dependency spec for topic intake, session lifecycle, scoring, redemption |
| 7 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | Codified registry | Topic urgency and 24-hour cadence constraint |
| 8 | `primitives/experience/friction_ability/EXP-FRC-003.yaml` | Codified registry | Friction reduction for entry, record, and stop flow |
| 9 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Immediate score reveal and latency constraint |
| 10 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Codified registry | Earned reward / gated export constraint |
| 11 | `src/ccp/services/content_machine.py` | Current backend implementation | Existing CMF handoff pipeline and actual method signature |
| 12 | `src/ccp/models/ca11_models.py` | Current shared model layer | Existing `ResolvedPalette`, `ContentMachineResult`, and `SessionContentPiece` model definitions |
| 13 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Existing | Pytest pattern for async helper and class-based organization |
| 14 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Existing | Pytest pattern for SQL/constant assertions and grouped scenarios |

## 2. Overview

### 2.1 Problem Statement - What breaks without this spec?

Without a dedicated Solo Reaction Mini App spec, the first and most important Conscious Reactions surface will drift in three dangerous ways:
- the UI will re-implement CORE contracts differently from Debate, Duel, and later Mini Apps
- the coach will experience blocking upload waits or stale-topic launches, collapsing the "highest-velocity entry point" promised by the PRD
- weak takes will be allowed to masquerade as premium content because the pass-to-CMF / fail-to-Redemption branch is not explicitly defined at the surface layer

The result is a broken first impression: the coach does not know when the topic expires, does not get immediate score feedback, and cannot tell whether a take truly earned export or merely got routed optimistically.

### 2.2 Solution

This spec builds `react_solo` as a standalone Telegram Mini App under `apps/react-solo/`. The app consumes the `FR-ERA3-05-CORE` engine for topic issuance, recording session lifecycle, streaming-score completion, and redemption routing. It adds the Solo-specific surface contract: topic brief display, constrained recording UI, score reveal, explicit approval to deploy, and a deployment decision branch that either triggers an existing `ContentMachinePipeline.process_session(...)` handoff for CMF routing or returns the coach to Redemption Round. The Solo app does not invent new scoring logic; it is the thin, fast, and enforceable first-use surface on top of the CORE engine.

### 2.3 Scope

**In scope:**
- `startapp=react_solo` launch and bootstrap payload
- Solo topic brief screen with source link, briefing audio, and expiry countdown
- Constrained 2-5 minute recording flow for one coach
- Stop-state transition into scoring while full-fidelity upload continues in the background
- Score reveal screen using CORE output, not duplicate scoring logic
- Explicit approve-to-deploy action after score reveal
- Deployment decision branch: pass -> CMF routing, fail -> Redemption Round
- CMF status surfacing using `ContentMachinePipeline` output and 20-minute delivery SLA
- Solo-specific typed models and tests

**Out of scope:**
- biometric scoring implementation internals already owned by `FR-ERA3-05-CORE`
- audience voting, supervisor pairing, and vote-then-react logic
- Debate with Jury and Reaction Duel surfaces
- downstream glossy video rendering internals after the CMF handoff
- new Telegram identity flows or alternate auth systems
- reusing `tools/tierlist-app/`, which is a different desktop tool

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Payload | Source FR | What It Does |
|---|---|---|---|
| DEP-REA-SOLO-001 | `SoloReactionLaunchPayload` | PRD-06 Section 2.2.1 | Bootstrap payload for the `react_solo` Mini App surface |
| DEP-REA-SOLO-002 | `SoloTopicBriefView` | CORE Story 1.1 inheritance + PRD-06 Section 2.2.1 | Encapsulates topic, source URL, audio brief, countdown, and expiration data |
| DEP-REA-SOLO-003 | `SoloRecordingViewState` | CORE Stories 1.2 and 1.3 inheritance | Encapsulates constrained recording boundaries, timer, streaming status, and upload ticket |
| DEP-REA-SOLO-004 | `SoloScoreRevealPayload` | PRD-06 Section 2.2.1 | Delivers conviction, pacing, authority, timestamps, and export eligibility |
| DEP-REA-SOLO-005 | `SoloDeploymentProjection` | Phase 2 Story 2.1 | Projects CMF delivery ETA, queue status, or redemption branch routing |
| DEP-REA-SOLO-006 | `OverlayRenderer` (Solo Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with Solo recording UI for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream contract for `ReactionTopicBrief`, recording sessions, streaming-score delivery, Redemption Round, and export eligibility |
| `content_machine.py` | `src/ccp/services/content_machine.py` | Consumed through `ContentMachinePipeline.process_session(...)` after a take passes the earned-export gate |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `ResolvedPalette`, `SessionContentPiece`, `ContentMachineArray`, and `ContentMachineResult` types |
| `main.py` | `src/ccp/api/main.py` | Registers a thin Solo route module or launch bridge if the Mini App needs explicit bootstrap endpoints |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | Pattern reference for audio upload validation and private `sacred-audio` storage behavior |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Existing audit trail for launch, stop, approve, deploy, and redemption transitions |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends schema only if Solo needs app-local state or delivery projections not already covered by CORE tables |

**Existing database tables consumed:**
- `receipt_chain` - immutable event log for launch, approve, deploy, and fail states
- `asset_registry` - artifact and audio asset identifiers
- `person_registry` - coach identity and Telegram user mapping
- `resolved_palettes` - DPA theme continuity across brief, score reveal, and export

**CORE-owned tables this app reads/writes via API contracts:**
- `reaction_topics`
- `reaction_sessions`
- `reaction_artifacts`
- `reaction_upload_sessions`
- `reaction_redemptions`

**API routes this spec depends on:**
- `POST /api/sacred-audio/upload` - existing upload/storage pattern reference
- `GET /api/reactions/solo/topic/next` - CORE-backed launch contract for `react_solo`
- `POST /api/reactions/sessions` - create Solo recording session
- `POST /api/reactions/sessions/{session_id}/finalize` - stop recording and move immediately into scoring
- `POST /api/reactions/solo/artifacts/{artifact_id}/approve` - explicit coach approval before deployment branch
- `GET /api/reactions/solo/artifacts/{artifact_id}/deployment-status` - project CMF queue, delivery ETA, or redemption branch

**How `content_machine.py` is actually consumed:**
- the Solo surface never calls CMF directly from the browser
- a backend adapter builds a reaction-shaped `session_report` by mapping `ReactionArtifactRecord` and `ReactionScoreCard` data: `key_insights` are derived from the artifact's highest scoring semantic beats, `breakthrough_moments` map directly to `ReactionScoreCard` timestamped evidence, and `emotional_beats` map to conviction/pacing trajectory vectors
- the adapter calls `await ContentMachinePipeline.process_session(session_report, coach_id, coach_acronym)`
- the Mini App reads only the resulting deployment projection, not the raw CMF internals

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-TRG-002` | Hook Cycle Velocity | trigger_timing | Solo launch must surface only fresh topics, with countdown and expiry behavior that preserves a 24-hour loop |
| `EXP-FRC-003` | The B=MAP Friction Audit | friction_ability | A coach must move from Telegram launch to active recording with minimal taps and must not wait on full upload after stop |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Score reveal must remain immediate and meaningful, using CORE's pre-streamed scoring state rather than delayed batch analysis |
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | Glossy export must remain earned, not default; failed takes route to Redemption instead of public reward |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Story 1.1, inherited from CORE | `SoloTopicBriefView` must include `expires_at` and `expires_in_seconds`; the record CTA disables at expiry and the app forces a fresh topic fetch instead of replaying cached stale briefs |
| The Background Upload Rule | Phase2-M02 | Story 1.2, inherited from CORE | `SoloRecordingConsole` treats finalize acknowledgement as the transition point into scoring; full binary upload continues in the background with resumable state |
| The Streaming Audio SLA | Phase2-M03 | Story 1.3, inherited from CORE | The app never starts a new post-stop transcript wait flow; it polls or subscribes only for final scorecard completion against the CORE 3-second SLA |
| The Earned Export Gate | Phase2-M04 | Story 2.1 | The app exposes the deploy branch only after score reveal and only if the backend returns `export_eligible=true` (requiring Conviction Score >= 0.85); otherwise the same approve action returns `redemption_required` and no CMF CTA appears |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Build the Solo surface in `apps/react-solo/` using the repo's existing `apps/` convention | The workspace already contains a modern app structure under `apps/animation-studio/`; Solo should fit that layout | Put the app in `tools/tierlist-app/` | That tool is explicitly a different desktop experience and not a Telegram Mini App |
| Keep scoring logic fully upstream in CORE | The prompt explicitly says do not re-specify the biometric scoring engine | Add Solo-only scoring code in the Mini App or a duplicate backend route | Duplicates logic, guarantees drift, and breaks shared Phase 2 behavior |
| Require an explicit "Approve for Deployment" action after the score reveal | Story 2.1 says "When I approve the take" before the pass/fail export branch | Auto-deploy every passing take immediately after score reveal | Removes the coach's approval checkpoint and makes content extraction feel pushy |
| Route passing takes into `ContentMachinePipeline.process_session(...)` via an adapter | This reuses an actual existing backend contract instead of inventing a fake CMF API | Create a new reaction-specific CMF service from scratch | Reinvents the content-routing layer and ignores the existing pipeline |
| Model CMF success as a queued/delivered projection, not a synchronous export | `content_machine.py` is async and may push content non-blockingly; the surface must show truthful state | Pretend the glossy asset exists immediately when the coach taps approve | Misrepresents pipeline state and creates false success on failed/delayed jobs |
| Keep Redemption in the same app as a follow-up branch | Solo is the foundational entry point; failure recovery must feel adjacent, not like exile | Kick the coach out to Telegram chat or a separate app on failure | Adds friction exactly where the user is most vulnerable to drop-off |
| Enforce 2-5 minute bounded takes at the Solo surface | The protocol defines Solo as a constrained 2-5 minute take | Allow unlimited recording length | Breaks habit-loop velocity and undermines scoring consistency |

## 4. Implementation Plan

### Phase 1 - App Scaffold and Launch Contract
- [ ] Create `apps/react-solo/package.json`
- [ ] Create `apps/react-solo/tsconfig.json`
- [ ] Create `apps/react-solo/next.config.mjs`
- [ ] Create `apps/react-solo/app/layout.tsx`
- [ ] Create `apps/react-solo/app/page.tsx`
- [ ] Create `apps/react-solo/app/globals.css`

### Phase 2 - Client Contracts and Recorder State
- [ ] Create `apps/react-solo/app/lib/types.ts`
- [ ] Create `apps/react-solo/app/lib/api.ts`
- [ ] Create `apps/react-solo/app/lib/state.ts`
- [ ] Create `apps/react-solo/app/lib/upload-worker.ts`
- [ ] Create `apps/react-solo/app/lib/telegram.ts`

### Phase 3 - Solo UI Surfaces
- [ ] Create `apps/react-solo/app/components/topic-brief-screen.tsx`
- [ ] Create `apps/react-solo/app/components/recording-console.tsx`
- [ ] Create `apps/react-solo/app/components/recording-timer.tsx`
- [ ] Create `apps/react-solo/app/components/score-reveal-screen.tsx`
- [ ] Create `apps/react-solo/app/components/deployment-decision-card.tsx`
- [ ] Create `apps/react-solo/app/components/redemption-redirect-card.tsx`
- [ ] Create `apps/react-solo/app/components/cmf-status-card.tsx`

### Phase 4 - Backend Bridge and Deployment Adapter
- [ ] Create `src/ccp/models/reaction_solo_models.py`
- [ ] Create `src/ccp/services/solo_reaction_deployment.py`
- [ ] Create `src/ccp/api/solo_reaction_api.py`
- [ ] Modify `src/ccp/api/main.py` to register the Solo route module
- [ ] Modify `src/ccp/scripts/setup_supabase.py` only if additional Solo projection tables are required beyond CORE

### Phase 5 - CMF Routing and Verification
- [ ] Implement `ReactionToSessionReportAdapter` inside `src/ccp/services/solo_reaction_deployment.py` ensuring `key_insights`, `breakthrough_moments`, and `emotional_beats` are explicitly mapped from the `ReactionScoreCard` evidence
- [ ] Consume `ContentMachinePipeline.process_session(...)` inside `src/ccp/services/solo_reaction_deployment.py`
- [ ] Create `tests/integration/test_era3_fr05a_solo_reaction_api.py`
- [ ] Create `tests/integration/test_era3_fr05a_solo_reaction_deployment.py`
- [ ] Create `tests/integration/test_era3_fr05a_solo_reaction_app_contracts.py`
- [ ] Create `apps/react-solo/app/__tests__/recording-console.test.tsx`
- [ ] Create `apps/react-solo/app/__tests__/deployment-decision-card.test.tsx`

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/reaction_solo_models.py`

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ContentMachineResult, ResolvedPalette
from src.ccp.models.reaction_engine_models import (
    ReactionArtifactRecord,
    ReactionScoreCard,
    ReactionSessionRecord,
    ReactionTopicBrief,
)


class SoloUiPhase(str, Enum):
    brief = "brief"
    recording = "recording"
    scoring = "scoring"
    score_reveal = "score_reveal"
    deployed = "deployed"
    redemption = "redemption"


class SoloDeploymentDecision(str, Enum):
    deployed_to_cmf = "deployed_to_cmf"
    pending_cmf_retry = "pending_cmf_retry"
    redemption_required = "redemption_required"


class SoloTopicBriefView(ReactionTopicBrief):
    startapp: Literal["react_solo"] = Field(default="react_solo")
    palette: ResolvedPalette = Field(...)
    min_duration_seconds: int = Field(default=120, ge=120, le=300)
    max_duration_seconds: int = Field(default=300, ge=120, le=300)
    briefing_audio_required: bool = Field(default=True)
    expires_in_seconds: int = Field(..., ge=1, le=86400)
    source_label: str = Field(..., min_length=1)


class SoloRecordingViewState(BaseModel):
    session: ReactionSessionRecord = Field(...)
    phase: SoloUiPhase = Field(default=SoloUiPhase.recording)
    elapsed_seconds: int = Field(default=0, ge=0, le=300)
    max_duration_seconds: int = Field(default=300, ge=120, le=300)
    upload_ticket: str = Field(..., min_length=1)
    upload_status: Literal[
        "not_started",
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(default="not_started")
    stream_status: Literal["connected", "degraded", "recovered"] = Field(default="connected")
    stop_acknowledged_at: datetime | None = None
    local_blob_persisted: bool = Field(default=False)


class SoloScoreRevealPayload(BaseModel):
    artifact: ReactionArtifactRecord = Field(...)
    scorecard: ReactionScoreCard = Field(...)
    export_decision: SoloDeploymentDecision | None = Field(default=None)
    export_eligible: bool = Field(default=False)
    approval_required: bool = Field(default=True)
    coaching_cues: list[str] = Field(default_factory=list, max_length=2)
    cmf_delivery_deadline_at: datetime | None = None


class SoloDeploymentProjection(BaseModel):
    artifact_id: str = Field(..., min_length=1)
    decision: SoloDeploymentDecision = Field(...)
    content_machine_result: ContentMachineResult | None = None
    queue_status: Literal["not_queued", "queued", "delivered", "failed_retryable"] = Field(default="not_queued")
    delivery_eta_minutes: int | None = Field(default=None, ge=1, le=20)
    delivered_at: datetime | None = None
    redemption_session_id: str | None = None


class SoloReactionLaunchPayload(BaseModel):
    coach_id: str = Field(..., min_length=1)
    startapp: Literal["react_solo"] = Field(default="react_solo")
    ui_phase: SoloUiPhase = Field(default=SoloUiPhase.brief)
    topic: SoloTopicBriefView = Field(...)
    active_recording: SoloRecordingViewState | None = None
    last_score_reveal: SoloScoreRevealPayload | None = None
```

**Schema notes:**
- `ReactionTopicBrief`, `ReactionSessionRecord`, `ReactionScoreCard`, and `ReactionArtifactRecord` are owned by `FR-ERA3-05-CORE`
- `ResolvedPalette` is reused from `src/ccp/models/ca11_models.py`
- `ContentMachineResult` is surfaced only at the deployment projection layer so the app can show truthful CMF status without exposing raw service internals everywhere

## 6. Backward Compatibility Fallback

This spec follows the explicit fail-closed posture established by `circuit_breaker.py`.

| Failure Mode | Graceful Degradation |
|---|---|
| Topic expires while the app is open | The app disables record immediately, shows `topic_expired`, and forces a fresh fetch. It may not keep recording against a stale topic ID. |
| Upload worker is interrupted after stop | The score reveal may continue if CORE already completed scoring, but deployment approval is blocked until the artifact's upload state returns to a valid backend state. |
| Streaming score state is degraded | The app stays in `scoring` with a visible degraded banner and does not fabricate a pass/fail decision. Export remains blocked until CORE returns a final scorecard. |
| `ContentMachinePipeline.process_session(...)` fails | The app keeps the artifact scored and approved but sets deployment state to `pending_cmf_retry`; it must not falsely claim `deployed_to_cmf`. |
| DPA payload is missing or incomplete | The app falls back to safe default tokens supplied by CORE while logging a degraded branding state; recording still works. |
| Legacy backend paths still reference Trivianar artifacts | Solo does not expose any Trivianar-specific labels, overlays, or modes. Compatibility stays upstream in CORE and is hidden from the Solo surface. |

## 7. Tasks

### Frontend
- [ ] Create the standalone Mini App in `apps/react-solo/` with `app/page.tsx`, `app/layout.tsx`, and `app/globals.css`
- [ ] Add typed launch, session, and deployment contracts in `apps/react-solo/app/lib/types.ts`
- [ ] Implement Telegram launch helpers and viewport bindings in `apps/react-solo/app/lib/telegram.ts`
- [ ] Implement the topic fetch / session create / finalize / approve flow in `apps/react-solo/app/lib/api.ts`
- [ ] Implement resumable upload state in `apps/react-solo/app/lib/upload-worker.ts`
- [ ] Build the topic brief UI in `apps/react-solo/app/components/topic-brief-screen.tsx`
- [ ] Build the constrained recorder UI in `apps/react-solo/app/components/recording-console.tsx`
- [ ] Build the score reveal UI in `apps/react-solo/app/components/score-reveal-screen.tsx`
- [ ] Build the pass/fail branch card in `apps/react-solo/app/components/deployment-decision-card.tsx`
- [ ] Build the failed-take branch in `apps/react-solo/app/components/redemption-redirect-card.tsx`
- [ ] Build the CMF queue / delivery ETA surface in `apps/react-solo/app/components/cmf-status-card.tsx`

### Backend
- [ ] Create `src/ccp/models/reaction_solo_models.py` for Solo-specific typed payloads
- [ ] Create `src/ccp/services/solo_reaction_deployment.py` as the backend adapter between CORE artifacts and `ContentMachinePipeline`
- [ ] Create `src/ccp/api/solo_reaction_api.py` for Solo launch and deployment projection endpoints
- [ ] Register `solo_reaction_api` in `src/ccp/api/main.py`
- [ ] Append any needed Solo projection schema in `src/ccp/scripts/setup_supabase.py`
- [ ] Write receipt events for launch, approve, deploy, fail, and redemption transitions via `src/ccp/core/receipt_chain.py`

### Verification
- [ ] Create `tests/integration/test_era3_fr05a_solo_reaction_api.py`
- [ ] Create `tests/integration/test_era3_fr05a_solo_reaction_deployment.py`
- [ ] Create `tests/integration/test_era3_fr05a_solo_reaction_app_contracts.py`
- [ ] Create `apps/react-solo/app/__tests__/topic-brief-screen.test.tsx`
- [ ] Create `apps/react-solo/app/__tests__/recording-console.test.tsx`
- [ ] Create `apps/react-solo/app/__tests__/deployment-decision-card.test.tsx`

## 8. Acceptance Criteria

### AC-2.1A - Solo Topic Brief Honors Freshness and Countdown

**CBAR Mandate enforced:** Phase2-M01 (inherited)

**Given** a coach launches `startapp=react_solo`,
**When** the app requests the next Solo topic from CORE,
**Then** the UI displays the topic brief, `source_url`, and `briefing_audio_path`,
**And** the app shows a live countdown derived from `expires_at`,
**And** the record CTA becomes unavailable immediately after expiry.

**FAILURE EXAMPLE:** A coach reopens yesterday's topic, still sees the old brief, and can record against it with no expiry warning. The topic is culturally stale and the experience has lost its urgency. This is a spec violation.

**Measurable pass condition:** every rendered brief contains `expires_at`, `expires_in_seconds > 0` at first render, and attempts to start recording after expiry return `TOPIC_EXPIRED`.

### AC-2.1B - Stop Does Not Wait for Full Upload

**CBAR Mandate enforced:** Phase2-M02 (inherited)

**Given** a coach records a Solo take,
**When** the coach taps stop,
**Then** the app transitions into `scoring` immediately after finalize acknowledgement,
**And** the upload continues under the same `upload_ticket` in the background,
**And** the coach is not blocked on full binary transfer before seeing the next state.

**FAILURE EXAMPLE:** The app freezes on a blocking upload spinner for several seconds after stop, the operating system suspends Telegram, and the take is lost. This is a spec violation.

**Measurable pass condition:** finalize acknowledgement returns within 500ms of stop under normal network conditions, and the UI phase changes to `scoring` before `upload_status == uploaded`.

### AC-2.1C - Score Reveal Arrives as an Immediate Next Moment

**CBAR Mandate enforced:** Phase2-M03 (inherited)

**Given** the CORE engine has been receiving streaming audio chunks during the take,
**When** the Solo session finalizes,
**Then** the app renders a `SoloScoreRevealPayload` from the final `ReactionScoreCard`,
**And** the reveal contains conviction, pacing, authority, and timestamped evidence,
**And** the app does not trigger a second slow post-stop scoring flow.

**FAILURE EXAMPLE:** The coach stops recording and waits 25 seconds while the app says "transcribing..." because scoring starts only after the full file upload completes. The immediate feedback loop is broken. This is a spec violation.

**Measurable pass condition:** P95 `score_reveal_rendered_at - session.stopped_at <= 3000ms`.

### AC-2.1D - Approval Branch Enforces Earned Export

**CBAR Mandate enforced:** Phase2-M04

**Given** a coach completes the CORE loop and views the Solo score reveal,
**When** the coach taps "Approve for Deployment",
**Then** the backend evaluates the artifact against the biometric threshold (Conviction Score >= 0.85),
**And** a passing take returns `deployed_to_cmf`,
**And** a failing take returns `redemption_required` with no glossy deployment state exposed.

**FAILURE EXAMPLE:** A low-conviction take that fails the threshold still shows a "Your premium asset is on the way" banner, or a passing take is always pushed without explicit coach approval. Either case breaks the earned-export contract. This is a spec violation.

**Measurable pass condition:** `export_eligible == true` is the only condition under which the response may contain `decision == deployed_to_cmf`; all other approvals must return `decision == redemption_required`.

### AC-2.1E - Passed Takes Surface Truthful CMF Delivery Status Within 20 Minutes

**CBAR Mandate enforced:** Phase2-M04 plus Story 2.1 quality constraint

**Given** a passing Solo take has been approved for deployment,
**When** the deployment adapter converts it into a `session_report` and calls `ContentMachinePipeline.process_session(...)`,
**Then** the app surfaces a truthful queue or delivery state from the resulting projection,
**And** the extracted CMF asset is delivered within 20 minutes,
**And** failed or retrying CMF jobs remain visibly pending rather than silently claiming success.

**FAILURE EXAMPLE:** The coach taps approve, sees a fake success screen immediately, and forty minutes later still has no asset and no explanation. The reward loop is broken and the deployment state was dishonest. This is a spec violation.

**Measurable pass condition:** for approved passing artifacts, `delivered_at - approved_at <= 20 minutes`; otherwise the app must show `queue_status == failed_retryable` or `pending_cmf_retry`, never `deployed_to_cmf`.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream spec dependency | Canonical topic, session, scorecard, artifact, and redemption contracts |
| `FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/services/content_machine.py` | Runtime consumption | `ContentMachinePipeline.process_session(...)` for CMF routing |
| `src/ccp/models/ca11_models.py` | Model dependency | `ResolvedPalette`, `ContentMachineResult`, and content-piece model reuse |
| `src/ccp/api/main.py` | Code extension | Route registration for Solo launch / projection endpoints |
| `src/ccp/api/sacred_audio.py` | Pattern dependency | Private audio upload semantics and validation posture |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Event logging for launch, approve, deploy, retry, and redemption |
| `src/ccp/scripts/setup_supabase.py` | Migration dependency | Solo projection schema if needed beyond CORE tables |
| `apps/react-solo/` | New app dependency | Standalone Telegram Mini App implementation target |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Next.js | workspace-pinned | Solo Mini App runtime in `apps/react-solo/` |
| React | workspace-pinned | UI components and recorder state transitions |
| TypeScript | workspace-pinned | Typed client contracts |
| FastAPI | existing backend dependency | Thin Solo bootstrap and deployment-projection routes |
| Pydantic v2 | existing backend dependency | Solo typed response models |
| Telegram WebApp SDK | current platform | Launch context, viewport control, and Telegram container integration |
| Browser `MediaRecorder` | modern mobile browser capability | Constrained voice recording and chunk capture |
| Browser IndexedDB | modern mobile browser capability | Retry-safe local blob persistence for background upload |

## 10. Testing Strategy

### Unit Tests

**File:** `apps/react-solo/app/__tests__/topic-brief-screen.test.tsx`
- `describe("TopicBriefScreen")`
- `it("renders source link, briefing audio CTA, and countdown from expires_at")`
- `it("disables record when expires_in_seconds reaches zero")`

**File:** `apps/react-solo/app/__tests__/recording-console.test.tsx`
- `describe("RecordingConsole")`
- `it("enters scoring immediately after finalize acknowledgement")`
- `it("preserves upload ticket and retry state when upload fails")`
- `it("enforces the 300-second maximum duration")`

**File:** `apps/react-solo/app/__tests__/deployment-decision-card.test.tsx`
- `describe("DeploymentDecisionCard")`
- `it("shows approve CTA only when score reveal is complete")`
- `it("shows redemption branch when export_eligible is false")`
- `it("shows pending or delivered CMF states truthfully")`

### Integration Tests

Modeled explicitly on `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`:
- use a local `_run()` helper for async service calls
- group by class per scenario or acceptance criterion
- create small fixture builders for topics, sessions, scorecards, and content-machine results
- assert exact contract fields and queue states directly

**File:** `tests/integration/test_era3_fr05a_solo_reaction_api.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestSoloLaunch:
    def test_topic_contains_source_audio_and_expiry(self): ...
    def test_expired_topic_rejected(self): ...


class TestFinalizeFlow:
    def test_finalize_returns_scoring_state_before_upload_completes(self): ...
    def test_score_reveal_contract_contains_conviction_pacing_authority(self): ...


class TestApprovalBranch:
    def test_passing_take_returns_deployed_to_cmf(self): ...
    def test_failed_take_returns_redemption_required(self): ...
```

**File:** `tests/integration/test_era3_fr05a_solo_reaction_deployment.py`

```python
class TestReactionToSessionReportAdapter:
    def test_maps_reaction_artifact_to_content_machine_session_report(self): ...
    def test_uses_actual_content_machine_process_session_contract(self): ...


class TestCmfProjection:
    def test_delivery_projection_surfaces_queue_state(self): ...
    def test_failed_content_machine_call_returns_pending_cmf_retry(self): ...
    def test_passed_artifact_delivery_meets_20_minute_sla(self): ...
```

**File:** `tests/integration/test_era3_fr05a_solo_reaction_app_contracts.py`

```python
class TestSoloContracts:
    def test_launch_payload_uses_startapp_react_solo(self): ...
    def test_recording_state_contains_upload_ticket(self): ...
    def test_score_reveal_payload_requires_approval_before_deploy(self): ...
    def test_redemption_branch_contains_no_cmf_success_state(self): ...
```

### Manual Verification

1. Launch the Telegram Mini App with `startapp=react_solo`.
2. Confirm the first visible state is the topic brief, not a blank recorder.
3. Verify the topic brief displays a source link, a briefing-audio action, and a live expiry countdown.
4. Start recording and confirm the session enforces a bounded timer between 2 and 5 minutes.
5. Stop recording and confirm the UI moves into scoring immediately while upload state continues independently.
6. Verify the score reveal returns conviction, pacing, authority, and timestamped evidence inside the 3-second SLA window.
7. Approve a passing take and confirm the app returns a deployment status card rather than fabricating an instant glossy asset.
8. Verify the deployment status advances from queued to delivered within 20 minutes for a passing take.
9. Approve a failing take and confirm the app returns the Redemption branch with no `deployed_to_cmf` state and no public-share success language.
10. Simulate a CMF pipeline failure and confirm the app shows a retryable pending state instead of false success.
