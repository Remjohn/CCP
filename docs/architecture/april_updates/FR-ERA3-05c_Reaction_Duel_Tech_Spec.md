# Tech-Spec: FR-ERA3-05c - Reaction Duel Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 2 - Conscious Reactions
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.4 marks `trivianar_engine_service.py` as the legacy PRD-06 backend and
                      Section 5.1 classifies Reaction Duel as `startapp=react_duel`, a standalone Mini App
                      that is async first rather than a live synchronous room.
2. PRD LOADED:        PRD-06 source-of-truth line required by the protocol for Duel mode:
                      "Two coaches react to the same topic and are then compared."
3. EPIC LOADED:       "Given two coaches react to the same duel topic, When both artifacts hit `scored` status,
                      Then a unified Duel asset is generated allowing audiences to vote. And the matchmaking
                      engine must enforce tier-based brackets, only pairing coaches within their same local
                      bracket/tier to ensure safe failure."
4. CBAR AUDIT LOADED: Phase2-M06 The Bracket Matchmaking Rule confirmed. Hallucination purge also confirms
                      `EXP-TRB-*` references must be corrected to `EXP-TRS-*`, and `EXP-SFR-*` references
                      must be corrected to `EXP-SAF-*`.
5. PRIMITIVES LOADED: YAML headers verified as written:
                      `experience_primitive_id: "EXP-SOC-004"` / `canonical_name: "Balanced Social Status Architecture"`
                      `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
                      `experience_primitive_id: "EXP-SAF-004"` / `canonical_name: "Practical Play / Safe Failure"`
6. BACKEND FILES READ:`src/ccp/services/trait_scoring_engine.py` -
                      `def score_all_traits(self) -> list[ScoredTrait]`
                      `src/ccp/services/content_machine.py` -
                      `async def process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
                      `src/ccp/services/canvas_composition_service.py` -
                      `def create_composition(self, vcb_id: str, template_id: str, slide_count: int, dimensions: dict[str, Any], handle_bar: dict[str, Any], text_content: dict[int, dict[str, str]] | None = None, content_output_id: str | None = None,) -> CanvasComposition`
7. TEST PATTERN:      `tests/integration/test_ca11_fr15_dpa_engine.py` and
                      `tests/integration/test_ca11_fr19_trivianar_engine.py` both use a local `_run()` helper,
                      class-per-scenario grouping, fixture-style constants/builders, and direct assertions
                      against service outputs, constants, and SQL strings without `pytest-asyncio`.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S07_FR-ERA3-05c_Reaction_Duel.md` | 2026-05-11 | Assignment prompt, scope, output path |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, app separation doctrine, PRD-06 execution notes |
| 3 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | v6.0, 2026-05-06 | Conscious Reactions module and brownfield inventory |
| 4 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Current source-of-truth, loaded 2026-05-11 | Exact Duel mode definition and async-first product posture |
| 5 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | 2026-05-08 | Story 2.3 acceptance criteria and quality constraint |
| 6 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | 2026-05-10 | Adversarial audit and Phase2-M06 confirmation |
| 7 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | 2026-05-11 | Upstream contract for recording, scoring, social routing, and artifact lifecycle |
| 8 | `primitives/experience/social_referral/EXP-SOC-004.yaml` | Codified registry | Verified bracket/lane progression primitive |
| 9 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Verified immediate comparative feedback primitive |
| 10 | `primitives/experience/safe_failure_recovery/EXP-SAF-004.yaml` | Codified registry | Verified safe-failure / anti-humiliation primitive |
| 11 | `src/ccp/services/trait_scoring_engine.py` | Current backend implementation | Existing trait scoring input for new bracket calculation |
| 12 | `src/ccp/services/content_machine.py` | Current backend implementation | Existing CMF routing pipeline for duel-derived content |
| 13 | `src/ccp/services/canvas_composition_service.py` | Current backend implementation | Existing composition engine for unified VS duel asset |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI route registration and health extension point |
| 15 | `src/ccp/models/ca11_models.py` | Current shared model layer | Existing `ResolvedPalette` and `ContentMachineResult` types |
| 16 | `src/ccp/models/visual_engine_models.py` | Current shared visual model layer | Existing `CanvasComposition` and visual export models |
| 17 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Existing | Pytest pattern reference for `_run()` and grouped behavior tests |
| 18 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Existing | Pytest pattern reference for constants, SQL assertions, and grouped scenarios |

## 2. Overview

### 2.1 Problem Statement

Without a dedicated Reaction Duel spec, the platform will collapse three distinct concerns into a vague "competitive mode":
- coaches will be paired without bracket safety, producing humiliation blowouts instead of controlled skill contrast
- the system will drift toward synchronous/live assumptions even though the product is explicitly async first
- the resulting public artifact will either never unify both takes or will visually resemble a solo/debate card instead of a true head-to-head comparison

That breaks the purpose of Duel mode: a safe but high-contrast comparison format that sharpens performance relevance without requiring a crowd, a calendar, or a live room.

### 2.2 Solution

This spec builds `react_duel` as a standalone Telegram Mini App under `apps/react-duel/`. The app consumes `FR-ERA3-05-CORE` for topic intake, recording sessions, scorecards, and audience voting contracts, but adds the Duel-specific orchestration that CORE does not own: async-first challenger acceptance, tier-based bracket matchmaking from `TraitScoringEngine.score_all_traits()`, waiting-room state until both artifacts are scored, and unified duel artifact composition via `CanvasCompositionService`. After both sides are scored, the service generates a single VS duel asset that audiences can vote on through inherited CORE social-routing paths. Debate-style live back-and-forth is explicitly out of scope; the Duel mode is a controlled, bracket-safe async comparison surface.

### 2.3 Scope

**In scope:**
- `startapp=react_duel` launch and duel invitation bootstrap
- async-first duel challenge and acceptance flow
- bracket-safe coach pairing within the same local tier
- trait-derived bracket snapshot and duel eligibility projection
- separate recording sessions for each coach on the same duel topic
- wait state until both artifacts reach `scored`
- unified VS duel asset generation after both takes are scored
- audience-votable duel projection using inherited CORE jury mechanics
- duel-specific typed models and tests

**Out of scope:**
- live/synchronous WebRTC duel rooms
- open global matchmaking across all coaches
- Debate with Jury stance logic
- Solo Reaction flow
- redesign of CORE score generation
- generalized tournament ladder infrastructure beyond local duel brackets

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-REA-DUEL-001 | `ReactionDuelAppShell` | Story 2.3 | Standalone `react_duel` Mini App |
| DEP-REA-DUEL-002 | `DuelInviteProjection` | Story 2.3 | Shows the duel topic, rival identity envelope, and bracket-safe eligibility |
| DEP-REA-DUEL-003 | `DuelBracketMatcher` | Story 2.3 + Phase2-M06 | Computes local bracket/tier assignment from trait outputs and prevents unsafe mismatches |
| DEP-REA-DUEL-004 | `DuelAcceptanceCoordinator` | Story 2.3 | Manages invite, accept, expire, and decline states for async-first duel setup |
| DEP-REA-DUEL-005 | `DuelRecordingCoordinator` | Story 2.3 + CORE inheritance | Creates and binds independent recording sessions for both coaches against the same duel topic |
| DEP-REA-DUEL-006 | `DuelAwaitingComparisonState` | Story 2.3 | Holds the duel open until both artifacts reach `scored` status |
| DEP-REA-DUEL-007 | `UnifiedDuelArtifactComposer` | Story 2.3 | Generates the single side-by-side VS duel asset after both takes are scored |
| DEP-REA-DUEL-008 | `DuelAudienceVoteProjection` | Story 2.3 + CORE social routing inheritance | Exposes the unified duel asset to audience voting once published |
| DEP-REA-DUEL-009 | `DuelContentRoutingAdapter` | Post-duel content extraction | Adapts duel outcomes/highlights into `ContentMachinePipeline.process_session(...)` input |
| DEP-REA-DUEL-010 | `DuelInvitePayload` | Story 2.3 | Primary data object modeling the invite transmission and TTL bounds |
| DEP-REA-DUEL-011 | `DuelBracketSnapshot` | Story 2.3 | Immutable data object tracking a coach's bracket index and tier |
| DEP-REA-DUEL-012 | `DuelParticipantState` | Story 2.3 | Data object tracking session and artifact resolution per side |
| DEP-REA-DUEL-013 | `UnifiedDuelProjection` | Story 2.3 | Final data object exposing the VS duel for audience voting |
| DEP-REA-DUEL-014 | `OverlayRenderer` (Duel Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with duel recording UI for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream contract for topic, session, scorecard, artifact, and social-routing behavior |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Consumed through `score_all_traits()` to compute duel bracket projections from existing trait evidence rather than inventing a second scoring stack |
| `content_machine.py` | `src/ccp/services/content_machine.py` | Consumed through `ContentMachinePipeline.process_session(...)` for duel-derived content extraction after the unified asset is created |
| `canvas_composition_service.py` | `src/ccp/services/canvas_composition_service.py` | Consumed through `create_composition(...)`, `receive_asset(...)`, and `export_composition(...)` for the unified duel VS artifact |
| `main.py` | `src/ccp/api/main.py` | Registers Duel API routes and extends `/health` with bracket/composition readiness |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `ResolvedPalette` and `ContentMachineResult` |
| `visual_engine_models.py` | `src/ccp/models/visual_engine_models.py` | Reuses `CanvasComposition`, `ExportAssets`, and composition statuses |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs duel invites, pairings, acceptances, score-ready transitions, and unified-asset publication |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends schema for duel pairings and bracket projections |

**Existing database tables consumed:**
- `receipt_chain` - immutable audit trail for pairing and publish transitions
- `asset_registry` - duel artifact and share-asset identifiers
- `person_registry` - coach identity resolution
- `resolved_palettes` - DPA continuity across duel topic and VS artifact
- `reaction_topics` - shared topic envelope via CORE
- `reaction_sessions` - one session per coach for the same duel topic
- `reaction_artifacts` - scored artifacts for both sides before unification
- `reaction_votes` - audience voting once the unified duel asset is published

**New Duel-specific tables introduced by this spec:**
- `reaction_duels` - root duel row binding topic, both coaches, lifecycle state, and unified artifact ID
- `reaction_duel_brackets` - current bracket/tier snapshot per coach and topic lane
- `reaction_duel_invites` - invite token, acceptance state, and expiry metadata

**Existing API routes extended or called:**
- `GET /health` - extended with duel bracket/composition readiness
- `POST /api/reactions/duels` - create or propose a duel challenge
- `POST /api/reactions/duels/{duel_id}/accept` - accept a bracket-safe async duel
- `GET /api/reactions/duels/{duel_id}` - fetch duel projection and state
- `POST /api/reactions/duels/{duel_id}/record` - create the caller's bound recording session
- `POST /api/reactions/duels/{duel_id}/publish` - finalize unified duel asset after both sides are scored

**How existing services are actually consumed:**
- `TraitScoringEngine.score_all_traits()` provides the evidence-backed trait vector used to derive local bracket tiers
- `CanvasCompositionService.create_composition(...)` is the required entrypoint for unified side-by-side duel rendering; the app may not stitch cards client-side
- `ContentMachinePipeline.process_session(...)` remains backend-only and is called TWICE through the `DuelContentRoutingAdapter` (once per coach identity) so both coaches receive independent highlight derivations from the unified artifact.

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-SOC-004` | Balanced Social Status Architecture | social_referral | Duel matching must preserve upward mobility and avoid hopeless or humiliating pairings by staying inside local brackets |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Both coaches receive fast meaningful result transitions, and the unified duel asset appears immediately after the second score completes |
| `EXP-SAF-004` | Practical Play / Safe Failure | safe_failure_recovery | Duel losses remain developmentally useful rather than socially destructive, with bracket safety preventing obvious blowouts |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---|---|---|---|
| The Bracket Matchmaking Rule | Phase2-M06 | Story 2.3 | `DuelBracketMatcher` computes a `coach_local_bracket` from trait-score outputs and only allows pairings where both coaches share the same bracket key and progression tier. Cross-tier invites, manual overrides to stronger brackets, and unbounded global challenge links are rejected before any recording session is created. |
| The Ephemeral Decay Mandate | Phase2-M01 | Story 1.1 | Enforced by bounding the `DuelInvitePayload.expires_at` to strictly `min(now() + 12h, topic.expires_at)`. This guarantees an accepted duel always has valid topic TTL remaining for the invitee's recording session. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Keep Duel async first with no live room dependency | The prompt and source-of-truth both state async first; schedule-free participation is the point | Build a synchronous duel room first | Reintroduces calendar bottlenecks and performance anxiety |
| Create a new `DuelBracketMatcher` instead of overloading CORE social routing | No existing service handles coach tier-pairing | Reuse generic audience/social routing to infer pairings | Social routing does not compute safe comparison tiers |
| Derive bracket projections from `TraitScoringEngine.score_all_traits()` | Uses an existing evidence-backed skill profile instead of a second ranking engine | Invent a duel-only ELO or arbitrary score | Duplicates scoring and produces unexplained mismatch with leadership evidence |
| Wait for both artifacts to reach `scored` before publishing anything | Story 2.3 explicitly gates on both sides reaching `scored` | Publish the first take and append the second later | Undermines the head-to-head reveal and creates unfair early framing |
| Render the unified duel asset via `CanvasCompositionService` | Existing composition engine provides auditable export state and template controls | Merge media manually in the client or a throwaway script | Breaks consistency and weakens QA over the duel visual contract |
| Treat audience voting as inherited once the unified asset exists | Story 2.3 needs the duel to become votable, but jury infrastructure already exists upstream | Rebuild a second duel-only voting subsystem | Fragments voting logic and duplicates existing social-routing behavior |
| Block cross-bracket invitations before recording begins | Safe failure must be guaranteed early, not retroactively after embarrassment | Let users record first and reject the duel later | Wastes effort and still exposes the user to an unfair challenge setup |

## 4. Implementation Plan

### Phase 1 - Duel App Scaffold
- [ ] Create `apps/react-duel/package.json`
- [ ] Create `apps/react-duel/tsconfig.json`
- [ ] Create `apps/react-duel/next.config.mjs`
- [ ] Create `apps/react-duel/app/layout.tsx`
- [ ] Create `apps/react-duel/app/page.tsx`
- [ ] Create `apps/react-duel/app/globals.css`

### Phase 2 - Matchmaking and Invite Flow
- [ ] Create `apps/react-duel/app/lib/types.ts`
- [ ] Create `apps/react-duel/app/lib/api.ts`
- [ ] Create `apps/react-duel/app/lib/state.ts`
- [ ] Create `apps/react-duel/app/components/duel-invite-projection.tsx`
- [ ] Create `apps/react-duel/app/components/duel-bracket-card.tsx`
- [ ] Create `apps/react-duel/app/components/duel-acceptance-panel.tsx`

### Phase 3 - Backend Duel Orchestration
- [ ] Create `src/ccp/models/reaction_duel_models.py`
- [ ] Create `src/ccp/services/reaction_duel_service.py`
- [ ] Implement `DuelBracketMatcher` in `src/ccp/services/reaction_duel_service.py` using formula: `confidence_directness_index = (conviction_score + pacing_score) / 20.0` and `polarity_authority_index = (impact_score + (anti_centroid_charge * 100)) / 20.0`. Tier thresholds applied to `overall_trait_average`: `<4.0` (foundation), `4.0-6.9` (emerging), `7.0-8.9` (advanced), `>=9.0` (sovereign).
- [ ] Implement `DuelAcceptanceCoordinator` in `src/ccp/services/reaction_duel_service.py`
- [ ] Create `src/ccp/api/reaction_duel_api.py`
- [ ] Register Duel routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with duel tables and indexes

### Phase 4 - Artifact Unification and Publishing
- [ ] Implement `UnifiedDuelArtifactComposer` in `src/ccp/services/reaction_duel_service.py`
- [ ] Map `left_side` to `inviter_coach_id` and `right_side` to `invitee_coach_id` deterministically during projection generation.
- [ ] Call `CanvasCompositionService.create_composition(...)` from `src/ccp/services/reaction_duel_service.py`
- [ ] Call `CanvasCompositionService.export_composition(...)` from `src/ccp/services/reaction_duel_service.py`
- [ ] Set `audience_vote_open = True` on the `UnifiedDuelProjection` explicitly upon successful canvas export completion.
- [ ] Implement `DuelContentRoutingAdapter` in `src/ccp/services/reaction_duel_service.py`
- [ ] Call `ContentMachinePipeline.process_session(...)` TWICE from `src/ccp/services/reaction_duel_service.py` (once for `left_side.coach_id` and once for `right_side.coach_id`), creating two distinct content derivations from the same unified VS artifact.

### Phase 5 - Verification
- [ ] Create `tests/integration/test_era3_fr05c_reaction_duel_api.py`
- [ ] Create `tests/integration/test_era3_fr05c_reaction_duel_matchmaking.py`
- [ ] Create `tests/integration/test_era3_fr05c_reaction_duel_rendering.py`
- [ ] Create `apps/react-duel/app/__tests__/duel-bracket-card.test.tsx`
- [ ] Create `apps/react-duel/app/__tests__/duel-acceptance-panel.test.tsx`
- [ ] Create `apps/react-duel/app/__tests__/duel-invite-projection.test.tsx`

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/reaction_duel_models.py`

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
from src.ccp.models.visual_engine_models import CanvasComposition


class DuelLifecycleState(str, Enum):
    proposed = "proposed"
    accepted = "accepted"
    waiting_for_opponent = "waiting_for_opponent"
    awaiting_comparison = "awaiting_comparison"
    unified = "unified"
    closed = "closed"
    rejected_bracket = "rejected_bracket"


class DuelBracketTier(str, Enum):
    foundation = "foundation"
    emerging = "emerging"
    advanced = "advanced"
    sovereign = "sovereign"


class DuelBracketSnapshot(BaseModel):
    coach_id: str = Field(..., min_length=1)
    bracket_tier: DuelBracketTier = Field(...)
    local_bracket_key: str = Field(..., min_length=1)
    overall_trait_average: float = Field(..., ge=1.0, le=10.0)
    confidence_directness_index: float = Field(..., ge=1.0, le=10.0)
    polarity_authority_index: float = Field(..., ge=1.0, le=10.0)
    calculated_at: datetime = Field(...)


class DuelInvitePayload(BaseModel):
    startapp: Literal["react_duel"] = Field(default="react_duel")
    duel_id: str = Field(..., min_length=1)
    inviter_coach_id: str = Field(..., min_length=1)
    invitee_coach_id: str = Field(..., min_length=1)
    topic: ReactionTopicBrief = Field(...)
    palette: ResolvedPalette = Field(...)
    inviter_bracket: DuelBracketSnapshot = Field(...)
    invitee_bracket: DuelBracketSnapshot | None = None
    lifecycle_state: DuelLifecycleState = Field(default=DuelLifecycleState.proposed)
    async_only: Literal[True] = Field(default=True)
    expires_at: datetime = Field(..., description="Must be min(now + 12h, topic.expires_at) to avoid CORE rejection")


class DuelParticipantState(BaseModel):
    coach_id: str = Field(..., min_length=1)
    accepted_at: datetime | None = None
    session: ReactionSessionRecord | None = None
    artifact: ReactionArtifactRecord | None = None
    scorecard: ReactionScoreCard | None = None
    ready_for_unification: bool = Field(default=False)


class UnifiedDuelProjection(BaseModel):
    duel_id: str = Field(..., min_length=1)
    lifecycle_state: DuelLifecycleState = Field(...)
    topic_id: str = Field(..., min_length=1)
    bracket_tier: DuelBracketTier = Field(...)
    left_side: DuelParticipantState = Field(...)
    right_side: DuelParticipantState = Field(...)
    unified_artifact_id: str | None = None
    render_format: Literal["split_screen_vs"] = Field(default="split_screen_vs")
    composition: CanvasComposition | None = None
    audience_vote_open: bool = Field(default=False)
    content_machine_result: ContentMachineResult | None = None
```

**Schema notes:**
- `ReactionTopicBrief`, `ReactionSessionRecord`, `ReactionArtifactRecord`, and `ReactionScoreCard` remain CORE-owned contracts
- `ResolvedPalette` is reused from `src/ccp/models/ca11_models.py`
- `CanvasComposition` is reused from `src/ccp/models/visual_engine_models.py`
- bracket snapshots are persisted separately from the final duel so the system can audit why a pairing was or was not allowed

## 6. Backward Compatibility Fallback

This spec follows the explicit fail-closed posture established by `circuit_breaker.py`.

| Failure Mode | Graceful Degradation |
|---|---|
| Trait-scoring data is unavailable for one coach | The duel may not be created; the invite returns `rejected_bracket` or a retryable eligibility error instead of guessing a bracket. |
| Coaches fall into different local brackets | The system blocks the pairing before recording and may suggest waiting or another rival in the same bracket. |
| One coach records and the other never accepts or never finishes | The completed artifact remains private or solo-usable per CORE rules, but no unified duel asset is published. |
| One side scores and the other side fails scoring | The duel stays in `awaiting_comparison` or `closed` with no audience-votable artifact. |
| Unified VS composition fails | Both scored artifacts remain intact, but `audience_vote_open=false` and no duel share card is published. |
| Content routing after unification fails | The duel asset may still be published and votable, but post-duel content extraction is marked retryable and not falsely surfaced as delivered. |

## 7. Tasks

### Frontend
- [ ] Create the standalone Duel Mini App in `apps/react-duel/`
- [ ] Add typed duel invite, bracket, and unified projection contracts in `apps/react-duel/app/lib/types.ts`
- [ ] Implement duel creation, acceptance, and projection fetchers in `apps/react-duel/app/lib/api.ts`
- [ ] Implement duel app state in `apps/react-duel/app/lib/state.ts`
- [ ] Build the duel invite screen in `apps/react-duel/app/components/duel-invite-projection.tsx`
- [ ] Build the bracket explanation surface in `apps/react-duel/app/components/duel-bracket-card.tsx`
- [ ] Build the async acceptance and waiting surface in `apps/react-duel/app/components/duel-acceptance-panel.tsx`
- [ ] Build the score-ready comparison state in `apps/react-duel/app/components/unified-duel-status-card.tsx`

### Backend
- [ ] Create `src/ccp/models/reaction_duel_models.py`
- [ ] Create `src/ccp/services/reaction_duel_service.py`
- [ ] Create `src/ccp/api/reaction_duel_api.py`
- [ ] Register `reaction_duel_api` in `src/ccp/api/main.py`
- [ ] Add duel pairing tables and indexes in `src/ccp/scripts/setup_supabase.py`
- [ ] Implement bracket calculation from `TraitScoringEngine.score_all_traits()` in `src/ccp/services/reaction_duel_service.py`
- [ ] Implement unified duel rendering via `src/ccp/services/canvas_composition_service.py`
- [ ] Implement post-duel content routing via `src/ccp/services/content_machine.py`
- [ ] Write receipt events for pairing, acceptance, scoring-ready, and publication transitions

### Verification
- [ ] Create `tests/integration/test_era3_fr05c_reaction_duel_api.py`
- [ ] Create `tests/integration/test_era3_fr05c_reaction_duel_matchmaking.py`
- [ ] Create `tests/integration/test_era3_fr05c_reaction_duel_rendering.py`
- [ ] Create `apps/react-duel/app/__tests__/duel-bracket-card.test.tsx`
- [ ] Create `apps/react-duel/app/__tests__/duel-acceptance-panel.test.tsx`
- [ ] Create `apps/react-duel/app/__tests__/duel-invite-projection.test.tsx`

## 8. Acceptance Criteria

### AC-2.3A - Async Duel Unifies Only After Both Sides Are Scored

**CBAR Mandate enforced:** None directly

**Given** two coaches react to the same duel topic,
**When** both artifacts hit `scored` status,
**Then** a unified duel asset is generated,
**And** that unified asset becomes the audience-votable public object,
**And** the system does not require a live synchronous session at any point.

**FAILURE EXAMPLE:** Coach A records on Tuesday, Coach B records on Wednesday, but the system insists on both joining a live room to compare them, or publishes only Coach A's take as if the duel already exists. This is a spec violation.

**Measurable pass condition:** `unified_artifact_id` is created only when both `left_side.artifact` and `right_side.artifact` are `scored`, and `async_only == true` for all duel invitations.

### AC-2.3B - Matchmaking Enforces Same Local Bracket

**CBAR Mandate enforced:** Phase2-M06

**Given** a coach creates or accepts a duel challenge,
**When** the system evaluates both coaches for pairing,
**Then** the duel is allowed only if both coaches share the same local bracket/tier,
**And** cross-bracket pairings are rejected before recording begins,
**And** the rejection preserves the lower-tier coach from blowout humiliation.

**FAILURE EXAMPLE:** A Foundation-tier coach is paired against a Sovereign-tier coach because both happen to like the same topic. The result is an obvious mismatch that feels punishing rather than developmental. This is a spec violation.

**Measurable pass condition:** all accepted duels satisfy `inviter_bracket.local_bracket_key == invitee_bracket.local_bracket_key` and `inviter_bracket.bracket_tier == invitee_bracket.bracket_tier`; otherwise `lifecycle_state == rejected_bracket` and no sessions are created.

### AC-2.3C - Unified Duel Artifact Renders as Head-to-Head Comparison

**CBAR Mandate enforced:** None directly

**Given** both duel participants have completed scoring and the pairing remains valid,
**When** the system publishes the duel asset,
**Then** the resulting composition renders the two coaches side by side in a unified VS format,
**And** audiences can vote on who held frame better from that single artifact,
**And** the duel may not collapse into two separate solo cards.

**FAILURE EXAMPLE:** The system sends two unrelated solo cards in sequence and tells the audience to "mentally compare them." The comparison loses clarity and the mode no longer feels like a duel. This is a spec violation.

**Measurable pass condition:** all published duel assets have `render_format == "split_screen_vs"` and `audience_vote_open == true` only after `composition` exists for the unified duel projection.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream spec dependency | Topic, session, scorecard, artifact, and audience-voting contracts |
| `FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/services/trait_scoring_engine.py` | Runtime consumption | `score_all_traits()` for bracket projection inputs |
| `src/ccp/services/content_machine.py` | Runtime consumption | `ContentMachinePipeline.process_session(...)` for duel-derived content extraction |
| `src/ccp/services/canvas_composition_service.py` | Runtime consumption | Unified duel composition generation and export |
| `src/ccp/api/main.py` | Code extension | Duel route registration and health exposure |
| `src/ccp/models/ca11_models.py` | Model dependency | `ResolvedPalette` and `ContentMachineResult` |
| `src/ccp/models/visual_engine_models.py` | Model dependency | `CanvasComposition` and export assets |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Immutable audit log for pairings and publication |
| `src/ccp/scripts/setup_supabase.py` | Migration dependency | Duel bracket and invite schema |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Next.js | workspace-pinned | Duel Mini App runtime in `apps/react-duel/` |
| React | workspace-pinned | Duel UI and waiting-state management |
| TypeScript | workspace-pinned | Typed app-side contracts |
| FastAPI | existing backend dependency | Duel API surface |
| Pydantic v2 | existing backend dependency | Typed duel models |
| Supabase PostgreSQL | existing backend dependency | Permanent pairing, invite, and unified duel state |
| Telegram Web App API | current platform | Launching `react_duel` from challenge links |
| Telegram Bot API | current platform | Delivering duel challenge links and audience-votable artifacts |

## 10. Testing Strategy

### Unit Tests

**File:** `apps/react-duel/app/__tests__/duel-bracket-card.test.tsx`
- `describe("DuelBracketCard")`
- `it("renders the local bracket tier and bracket key")`
- `it("renders a safe mismatch message when duel is rejected")`

**File:** `apps/react-duel/app/__tests__/duel-acceptance-panel.test.tsx`
- `describe("DuelAcceptancePanel")`
- `it("shows async-only copy and no live-room affordance")`
- `it("prevents accept when bracket eligibility is false")`

**File:** `apps/react-duel/app/__tests__/duel-invite-projection.test.tsx`
- `describe("DuelInviteProjection")`
- `it("renders react_duel bootstrap state from the invite payload")`
- `it("shows awaiting comparison after one side is scored")`

### Integration Tests

Modeled explicitly on `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`:
- use a local `_run()` helper for async service calls
- group tests by scenario or acceptance criterion
- create fixture builders for bracket snapshots, invites, scored artifacts, and unified projections
- assert exact route, model, SQL, and service outputs directly

**File:** `tests/integration/test_era3_fr05c_reaction_duel_matchmaking.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestDuelBracketMatcher:
    def test_same_tier_pairing_allowed(self): ...
    def test_cross_tier_pairing_rejected_ac23b(self): ...
    def test_bracket_projection_uses_trait_scoring_output(self): ...
```

**File:** `tests/integration/test_era3_fr05c_reaction_duel_api.py`

```python
class TestDuelLifecycle:
    def test_duel_acceptance_creates_no_live_session_requirement(self): ...
    def test_unified_duel_waits_for_both_scored_artifacts_ac23a(self): ...
    def test_publish_requires_unified_composition(self): ...
```

**File:** `tests/integration/test_era3_fr05c_reaction_duel_rendering.py`

```python
class TestUnifiedDuelRendering:
    def test_canvas_composition_service_used_for_unified_duel(self): ...
    def test_render_format_is_split_screen_vs(self): ...


class TestDuelContentRouting:
    def test_content_machine_called_after_unification(self): ...
    def test_failed_content_machine_call_returns_retryable_state(self): ...
```

### Manual Verification

1. Launch a duel challenge and confirm `startapp=react_duel` opens the async duel invite surface.
2. Verify the invite surface shows bracket/tier information and no live-room or synchronous scheduling affordance.
3. Attempt to pair two coaches from different brackets and confirm the duel is rejected before any recording session is created.
4. Pair two coaches from the same bracket and confirm both can record independently on different times or days.
5. Confirm the duel remains in a waiting state after only one side has been scored.
6. Confirm the unified duel asset is generated only after the second side reaches `scored`.
7. Verify the published asset renders as a side-by-side VS composition rather than two separate solo cards.
8. Verify the resulting unified duel artifact becomes the audience-votable object.
9. Simulate a composition failure and confirm the duel is not published for voting.
10. Trigger post-duel content routing and confirm the backend adapter calls `ContentMachinePipeline.process_session(...)` rather than inventing a separate CMF path.
