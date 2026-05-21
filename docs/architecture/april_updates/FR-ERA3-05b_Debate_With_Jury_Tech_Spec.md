# Tech-Spec: FR-ERA3-05b - Debate with Jury Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture - CBAR-Hardened)
**Phase:** 2 - Conscious Reactions
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms the existing route `POST /api/telegram/webhook`, and
                      Section 5.1 defines Debate with Jury as `startapp=react_debate`, a standalone
                      reaction-mode Mini App separate from CORE's bot-level jury entry paths.
2. PRD LOADED:        "A high-charge topic is dropped into a specific ecosystem lane. One user records
                      a take, which is then opened for `For / Against` voting and counter-takes from peers.
                      This mode creates side-taking, social identity, and highly commentable compilation
                      content, serving as the strongest silent referral mechanic."
3. EPIC LOADED:       "Given I receive a Debate artifact, When I tap "Counter-React", Then I must select
                      a stance before recording my opposing voice note. And the resulting CMF artifact must
                      explicitly render as a split-screen or "VS" visual format to maximize tribal alignment
                      and social stakes."
4. CBAR AUDIT LOADED: Phase2-M05 The Visual Adversary Rule confirmed. Hallucination purge also confirms
                      `EXP-TRB-*` references must be corrected to `EXP-TRS-*`, and `EXP-SFR-*` references
                      must be corrected to `EXP-SAF-*`.
5. PRIMITIVES LOADED: YAML headers verified as written:
                      `experience_primitive_id: "EXP-SOC-002"` / `canonical_name: "Social Capital and Self-Esteem Economy"`
                      `experience_primitive_id: "EXP-FRC-002"` / `canonical_name: "System 1 to System 2 Escalation"`
                      `experience_primitive_id: "EXP-TRG-005"` / `canonical_name: "First Major Win-State"`
                      `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
                      `experience_primitive_id: "EXP-TRS-004"` / `canonical_name: "Epic Meaning Framing (The Crusade Narrative)"`
                      `experience_primitive_id: "EXP-PER-003"` / `canonical_name: "Cumulative Investment"`
6. BACKEND FILES READ:`src/ccp/api/telegram_webhook.py` -
                      `async def telegram_webhook(request: Request)`
                      `src/ccp/services/content_machine.py` -
                      `async def process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
                      `src/ccp/services/canvas_composition_service.py` -
                      `def create_composition(self, vcb_id: str, template_id: str, slide_count: int, dimensions: dict[str, Any], handle_bar: dict[str, Any], text_content: dict[int, dict[str, str]] | None = None, content_output_id: str | None = None,) -> CanvasComposition`
7. TEST PATTERN:      `tests/integration/test_ca11_fr15_dpa_engine.py` and
                      `tests/integration/test_ca11_fr19_trivianar_engine.py` both use a local `_run()` helper,
                      class-per-behavior grouping, explicit constants and fixture builders, and direct
                      assertions against service outputs, SQL strings, and model fields without `pytest-asyncio`.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S06_FR-ERA3-05b_Debate_With_Jury.md` | 2026-05-11 | Assignment prompt, Mini App / bot split, output path |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, backend stack, Mini App separation doctrine |
| 3 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | v6.0, 2026-05-06 | Canonical Debate, Jury, and Vote Then React product definition |
| 4 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | 2026-05-08 | Story 2.2, 3.1, 3.2 acceptance criteria and quality constraints |
| 5 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | 2026-05-10 | Adversarial audit and Phase2-M05 enforcement source |
| 6 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | 2026-05-11 | Upstream contract for reaction sessions, scoring, artifact lifecycle, and social routing |
| 7 | `primitives/experience/social_referral/EXP-SOC-002.yaml` | Codified registry | Verified social proof / status primitive for debate sharing |
| 8 | `primitives/experience/friction_ability/EXP-FRC-002.yaml` | Codified registry | Verified low-friction inline voting primitive |
| 9 | `primitives/experience/trigger_timing/EXP-TRG-005.yaml` | Codified registry | Verified post-vote escalation trigger primitive |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Verified immediate tally / score feedback primitive |
| 11 | `primitives/experience/trust_branding/EXP-TRS-004.yaml` | Codified registry | Verified mission framing / debate lane narrative primitive |
| 12 | `primitives/experience/personalization_identity/EXP-PER-003.yaml` | Codified registry | Verified stored-value and stance-history primitive |
| 13 | `src/ccp/api/telegram_webhook.py` | Current backend implementation | Existing Telegram ingress to extend for inline jury callbacks |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI route registration and health extension point |
| 15 | `src/ccp/services/content_machine.py` | Current backend implementation | Existing CMF routing pipeline for debate-derived content |
| 16 | `src/ccp/services/canvas_composition_service.py` | Current backend implementation | Existing composition engine used to generate VS/split-screen artifacts |
| 17 | `src/ccp/models/ca11_models.py` | Current shared model layer | Existing `ResolvedPalette` and `ContentMachineResult` model source |
| 18 | `src/ccp/models/visual_engine_models.py` | Current shared visual model layer | Existing `CanvasComposition`, `ExportAssets`, and composition statuses |
| 19 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Existing | Pytest pattern reference for async helper and DPA assertions |
| 20 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Existing | Pytest pattern reference for grouped scenarios and SQL/constant assertions |

## 2. Overview

### 2.1 Problem Statement - What breaks without this spec?

Without a dedicated Debate with Jury spec, the system will fail in three precise ways:
- jurors will be incorrectly forced through a Mini App before they can vote, destroying the low-friction silent-referral loop
- debate artifacts will visually collapse into solo cards or generic content cards, violating the adversarial side-taking mechanic that makes the mode spread
- post-vote escalation will be untethered from the user's chosen side, so the staircase from passive participation to counter-take recording will feel like random spam instead of identity-consistent progression

The net effect is that Debate Mode stops being the "strongest silent referral mechanic" described in PRD-06 and degrades into a slower copy of Solo Reaction with no true jury layer.

### 2.2 Solution

This spec builds `react_debate` as a standalone Telegram Mini App under `apps/react-debate/` for speakers and counter-speakers, while keeping jury voting in native Telegram via inline buttons handled by `telegram_webhook.py`. The app consumes `FR-ERA3-05-CORE` for topic intake, stance-bound recording sessions, scoring, and debate artifact state. It adds the Debate-specific surface and routing contracts: forced `For / Against` stance selection before counter-recording, debate lane context, split-screen VS artifact composition, inline jury callback registration, and a post-vote `Vote Then React` prompt that opens the Mini App only after a vote is cast. The CMF branch reuses `ContentMachinePipeline.process_session(...)` for extractive routing and `CanvasCompositionService.create_composition(...)` for the new VS visual template, ensuring debate media can never visually resemble Solo artifacts.

### 2.3 Scope

**In scope:**
- `startapp=react_debate` launch, bootstrap, and debate-lane payload
- forced `For / Against` stance selection before counter-take recording
- Debate-specific counter-react recording flow on top of CORE session/scoring contracts
- native Telegram inline jury voting without opening the Mini App
- post-vote escalation prompt and deep-link into `react_debate`
- split-screen / VS artifact composition path using `canvas_composition_service.py`
- debate-derived CMF routing and deployment projection using `content_machine.py`
- typed models, receipt logging, and integration tests for Debate mode

**Out of scope:**
- Solo Reaction UI and deployment flow
- Reaction Duel matchmaking and bracket logic
- Supervisor Pairing flows
- synchronous live debates or WebRTC rooms
- redesign of CORE biometric scoring internals
- fully generic social sharing infrastructure outside debate artifacts

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-REA-DEB-001 | `DebateReactionAppShell` | PRD-06 Section 2.2.2 | Standalone `react_debate` speaker Mini App |
| DEP-REA-DEB-002 | `DebateLaneBriefScreen` | Story 2.2 | Renders the source artifact, lane framing, side stakes, and counter-react CTA |
| DEP-REA-DEB-003 | `DebateStanceGate` | Story 2.2 | Forces `for` or `against` selection before recording, rejecting neutral entry |
| DEP-REA-DEB-004 | `DebateCounterTakeRecorder` | Story 2.2 + CORE inheritance | Launches a counter-take recording session bound to an opponent artifact and stance |
| DEP-REA-DEB-005 | `AudienceJuryWebhookAdapter` | Story 3.1 | Registers inline Telegram votes through `telegram_webhook.py` without opening a Mini App |
| DEP-REA-DEB-006 | `VoteThenReactPromptBuilder` | Story 3.2 | Builds stance-tethered copy and deep links into `react_debate` after vote registration |
| DEP-REA-DEB-007 | `DebateVsArtifactComposer` | Story 2.2 + Phase2-M05 | Converts scored debate artifacts into a split-screen / VS visual composition |
| DEP-REA-DEB-008 | `DebateContentRoutingAdapter` | PRD-06 social deployment | Adapts debate wins / highlights into `ContentMachinePipeline.process_session(...)` input |
| DEP-REA-DEB-009 | `DebateTallyProjection` | Stories 3.1-3.2 | Projects real-time and permanent vote state into share surfaces and app refreshes |
| DEP-REA-DEB-010 | `DebateLaunchPayload` | Schema | Payload bootstrapping the `react_debate` mini app |
| DEP-REA-DEB-011 | `DebateCounterTakeIntent` | Schema | Payload representing intent to record a counter-take with an explicit stance |
| DEP-REA-DEB-012 | `AudienceJuryInlineVote` | Schema | Payload mapping the inline Telegram vote action |
| DEP-REA-DEB-013 | `VoteThenReactPrompt` | Schema | Payload containing post-vote deep link and copy |
| DEP-REA-DEB-014 | `DebateVsArtifactProjection` | Schema | Projection binding root and counter artifacts for VS composition and tallying |
| DEP-REA-DEB-015 | `OverlayRenderer` (Debate Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with debate lane UI for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream contract for recording sessions, scorecards, reaction artifacts, vote persistence, and share-safe gating |
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | Extended to parse `callback_query` vote payloads, deduplicate them, persist jury votes, and return a post-vote deep-link prompt |
| `main.py` | `src/ccp/api/main.py` | Registers Debate API routes and extends `/health` with Debate composition readiness |
| `content_machine.py` | `src/ccp/services/content_machine.py` | Consumed through `ContentMachinePipeline.process_session(...)` for debate highlight and post-debate content routing |
| `canvas_composition_service.py` | `src/ccp/services/canvas_composition_service.py` | Consumed through `create_composition(...)`, `receive_asset(...)`, and `export_composition(...)` for VS artifact assembly |
| `visual_engine_models.py` | `src/ccp/models/visual_engine_models.py` | Reuses `CanvasComposition`, `ExportAssets`, and composition status enums |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `ResolvedPalette` and `ContentMachineResult` |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs vote callbacks, stance selection, counter-take creation, and VS artifact publication |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends schema for debate-specific linkage tables if CORE tables are insufficient |

**Existing database tables consumed:**
- `receipt_chain` - immutable event log for vote, stance, composition, and deployment actions
- `asset_registry` - primary artifact and share-asset identifiers
- `person_registry` - coach and juror identity mapping from Telegram IDs
- `resolved_palettes` - DPA continuity across debate brief, score reveal, and VS artifact
- `reaction_artifacts` - CORE-owned reaction artifacts used as debate roots and counter-takes
- `reaction_votes` - CORE-owned permanent jury vote storage

**New or Debate-specific tables introduced by this spec:**
- `reaction_debates` - binds root artifact, counter artifact, chosen stances, lane, and render state
- `reaction_vote_prompts` - stores post-vote escalation prompts, deep-link tokens, and expiry windows
- `reaction_debate_compositions` - optional projection table for VS composition status if not stored directly on `reaction_debates`

**Existing API routes extended or called:**
- `POST /api/telegram/webhook` - native jury voting and vote-then-react prompt delivery
- `GET /api/canvas/*` and `POST /api/canvas/*` - existing canvas router namespace leveraged by the debate VS composition path
- `GET /api/reactions/debates/{debate_id}` - Debate projection read
- `POST /api/reactions/debates/{debate_id}/counter-react` - stance-bound counter-take launch
- `POST /api/reactions/debates/{debate_id}/approve` - explicit approval before VS artifact publication
- `GET /api/reactions/debates/{debate_id}/vote-prompt/{prompt_id}` - opens `react_debate` after a jury vote

**How existing services are actually consumed:**
- `telegram_webhook.py` currently only parses `message`; this spec extends it to handle `callback_query` for inline votes without introducing a second Telegram ingress
- `ContentMachinePipeline.process_session(...)` is not called directly from the browser; a backend adapter converts winning or high-signal debate content into the `session_report` shape it already expects
- `CanvasCompositionService.create_composition(...)` is the authoritative entrypoint for VS layout assembly; Debate mode may not invent an ad hoc image stitcher

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-SOC-002` | Identity-Driven Social Proof | social_referral | Debate artifacts must feel like status-bearing, share-worthy wins rather than neutral discussion cards |
| `EXP-FRC-002` | Friction-Zero Ability | friction_ability | Jury participation starts with a one-tap vote in Telegram; only then may the system ask for a deeper counter-take |
| `EXP-TRG-005` | External to Internal Trigger Mapping | trigger_timing | Vote Then React and post-victory share prompts must arrive after a meaningful identity investment or win state |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Vote registration, tally refresh, and counter-take scoring must feel immediate and meaningful, not batch-delayed |
| `EXP-TRS-004` | Attractive Things Work Better | trust_branding | Debate lane framing and share copy must present the take as an industry-level argument, not a generic comment thread |
| `EXP-PER-003` | Tailoring & Suggestion | personalization_identity | Debate stance history, jury profile links, and archived wins become stored value that compounds silent referral over time |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---|---|---|---|
| The Visual Adversary Rule | Phase2-M05 | Story 2.2 | Debate artifacts are persisted with `render_format="split_screen_vs"` and composed exclusively through a debate-specific VS template ID. `DebateStanceGate` forbids neutral stance selection, and `DebateVsArtifactComposer` rejects publication if either side would render as a solo card, single-speaker card, or non-oppositional composition. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Keep inline jury voting in `telegram_webhook.py`, not the Mini App | The prompt explicitly requires native Telegram inline buttons with no Mini App launch | Route every juror through `react_debate` before they can vote | Adds friction and breaks Story 3.1's zero-performance-pressure entry |
| Force explicit `for` or `against` stance before recording | Story 2.2 forbids neutral ambiguity and requires side-taking | Let users record a counter-take first and label it later | Allows centroid behavior and weakens tribal alignment |
| Use `apps/react-debate/` as a standalone app target | The repo already uses `apps/` for app surfaces, and the protocol defines Debate as its own Mini App | Reuse `tools/tierlist-app/` or mix Debate inside Solo | Wrong product surface and guarantees UI drift across modes |
| Build VS artifacts through `CanvasCompositionService` using a debate-only template | This is the existing composition engine and enforces the Visual Adversary Rule with a named template boundary | Stitch screenshots or concatenate solo cards client-side | Produces inconsistent visuals and lets Debate assets resemble Solo |
| Route debate-derived content through `ContentMachinePipeline.process_session(...)` via an adapter | This reuses a real backend pipeline and keeps CMF routing centralized | Create a one-off debate CMF microservice | Reinvents the content extraction layer and fragments delivery state |
| Return the Vote Then React deep link only after vote persistence succeeds | Story 3.2 says the prompt appears when the vote is registered | Show the prompt optimistically before or without persistence | Breaks the staircase-of-commitment sequencing and risks orphan prompt tokens |
| Treat a root take and a counter-take as separate scored artifacts bound by a debate table | This keeps CORE scoring per artifact intact while giving Debate a pairwise overlay | Invent a special dual-speaker scoring artifact from the start | Couples debate orchestration with scoring internals and makes retry flows brittle |

## 4. Implementation Plan

### Phase 1 - Debate App Scaffold
- [ ] Create `apps/react-debate/package.json`
- [ ] Create `apps/react-debate/tsconfig.json`
- [ ] Create `apps/react-debate/next.config.mjs`
- [ ] Create `apps/react-debate/app/layout.tsx`
- [ ] Create `apps/react-debate/app/page.tsx`
- [ ] Create `apps/react-debate/app/globals.css`

### Phase 2 - Stance and Counter-Take Flow
- [ ] Create `apps/react-debate/app/lib/types.ts`
- [ ] Create `apps/react-debate/app/lib/api.ts`
- [ ] Create `apps/react-debate/app/lib/state.ts`
- [ ] Create `apps/react-debate/app/components/debate-lane-brief-screen.tsx`
- [ ] Create `apps/react-debate/app/components/stance-selection-gate.tsx`
- [ ] Create `apps/react-debate/app/components/counter-take-recorder.tsx`
- [ ] Create `apps/react-debate/app/components/jury-tally-card.tsx`

### Phase 3 - Jury Callback and Escalation Path
- [ ] Create `src/ccp/models/reaction_debate_models.py`
- [ ] Create `src/ccp/services/debate_with_jury_service.py`
- [ ] Modify `src/ccp/api/telegram_webhook.py` to parse and validate `callback_query`
- [ ] Create vote callback token parsing and deduplication in `src/ccp/services/debate_with_jury_service.py`
- [ ] Create `VoteThenReactPromptBuilder` in `src/ccp/services/debate_with_jury_service.py`
- [ ] Create `src/ccp/api/debate_with_jury_api.py`
- [ ] Register Debate routes in `src/ccp/api/main.py`

### Phase 4 - VS Composition and Content Routing
- [ ] Create `DebateVsArtifactComposer` in `src/ccp/services/debate_with_jury_service.py`
- [ ] Call `CanvasCompositionService.create_composition(...)` from `src/ccp/services/debate_with_jury_service.py`
- [ ] Call `CanvasCompositionService.export_composition(...)` from `src/ccp/services/debate_with_jury_service.py`
- [ ] Create `DebateContentRoutingAdapter` in `src/ccp/services/debate_with_jury_service.py`
- [ ] Call `ContentMachinePipeline.process_session(...)` from `src/ccp/services/debate_with_jury_service.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with `reaction_debates` and `reaction_vote_prompts`

### Phase 5 - Verification
- [ ] Create `tests/integration/test_era3_fr05b_debate_api.py`
- [ ] Create `tests/integration/test_era3_fr05b_debate_jury_webhook.py`
- [ ] Create `tests/integration/test_era3_fr05b_debate_rendering.py`
- [ ] Create `apps/react-debate/app/__tests__/stance-selection-gate.test.tsx`
- [ ] Create `apps/react-debate/app/__tests__/jury-tally-card.test.tsx`
- [ ] Create `apps/react-debate/app/__tests__/vote-then-react-prompt.test.tsx`

### Phase 6 - Data Resolution & Transformation Rules
- **`DebateContentRoutingAdapter` Transformation:** The adapter maps a `DebateVsArtifactProjection` into the `session_report` dictionary expected by `ContentMachinePipeline.process_session(...)` using the following exact transformation:
  - `session_report["topic"]` = `root_artifact.topic`
  - `session_report["primary_speaker"]` = The winner of the debate (based on final tally) or the root speaker if tied.
  - `session_report["context_payload"]` = `{ "format": "debate_vs", "tally_for": tally_for, "tally_against": tally_against, "stances": [...] }`
  - `session_report["audio_assets"]` = Array containing both `root_artifact.audio_url` and `counter_artifact.audio_url`.
- **`DebateLaunchPayload` Tally Resolution:** The `latest_tally_for` and `latest_tally_against` fields are synchronously read from the Redis-backed `reaction_debates_tally` cache upon App launch request. If the cache is cold, they are recalculated from `reaction_votes`.
- **`DebateLaunchPayload` Neutral Gate:** `neutral_allowed` is hardcoded to `False` across all debate initializations to enforce the Visual Adversary Rule (Phase2-M05).
- **`DebateVsArtifactProjection.content_machine_result` Resolution:** Populated asynchronously when `ContentMachinePipeline.process_session(...)` returns success. The `DebateContentRoutingAdapter` handles this state update.

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/reaction_debate_models.py`

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


class DebateStance(str, Enum):
    for_side = "for"
    against_side = "against"


class JuryVoteStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    duplicate = "duplicate"
    expired = "expired"


class DebateLaunchPayload(BaseModel):
    startapp: Literal["react_debate"] = Field(default="react_debate")
    debate_id: str = Field(..., min_length=1)
    lane_key: str = Field(..., min_length=1)
    lane_title: str = Field(..., min_length=1)
    topic: ReactionTopicBrief = Field(...)
    palette: ResolvedPalette = Field(...)
    source_artifact_id: str = Field(..., min_length=1)
    source_speaker_person_id: str = Field(..., min_length=1)
    allowed_stances: list[DebateStance] = Field(
        default_factory=lambda: [DebateStance.for_side, DebateStance.against_side],
        min_length=2,
        max_length=2,
    )
    neutral_allowed: Literal[False] = Field(default=False)
    latest_tally_for: int = Field(default=0, ge=0)
    latest_tally_against: int = Field(default=0, ge=0)


class DebateCounterTakeIntent(BaseModel):
    debate_id: str = Field(..., min_length=1)
    source_artifact_id: str = Field(..., min_length=1)
    selected_stance: DebateStance = Field(...)
    prior_vote_id: str | None = None
    must_select_before_recording: bool = Field(default=True)
    session: ReactionSessionRecord | None = None


class AudienceJuryInlineVote(BaseModel):
    vote_id: str = Field(..., min_length=1)
    debate_id: str = Field(..., min_length=1)
    artifact_id: str = Field(..., min_length=1)
    voter_person_id: str = Field(..., min_length=1)
    voted_side: DebateStance = Field(...)
    callback_token: str = Field(..., min_length=1)
    status: JuryVoteStatus = Field(default=JuryVoteStatus.pending)
    registered_at: datetime | None = None
    opens_mini_app: Literal[False] = Field(default=False)


class VoteThenReactPrompt(BaseModel):
    prompt_id: str = Field(..., min_length=1)
    source_vote_id: str = Field(..., min_length=1)
    selected_stance: DebateStance = Field(...)
    prompt_copy: str = Field(..., min_length=1)
    cta_label: str = Field(..., min_length=1)
    deep_link_url: str = Field(..., min_length=1)
    startapp: Literal["react_debate"] = Field(default="react_debate")
    expires_at: datetime = Field(...)


class DebateVsArtifactProjection(BaseModel):
    debate_id: str = Field(..., min_length=1)
    root_artifact: ReactionArtifactRecord = Field(...)
    counter_artifact: ReactionArtifactRecord | None = None
    root_scorecard: ReactionScoreCard | None = None
    counter_scorecard: ReactionScoreCard | None = None
    render_format: Literal["split_screen_vs"] = Field(default="split_screen_vs")
    composition: CanvasComposition | None = None
    content_machine_result: ContentMachineResult | None = None
    tally_for: int = Field(default=0, ge=0)
    tally_against: int = Field(default=0, ge=0)
    visual_adversary_passed: bool = Field(default=False)
    public_share_ready: bool = Field(default=False)
```

**Schema notes:**
- `ReactionTopicBrief`, `ReactionSessionRecord`, `ReactionArtifactRecord`, and `ReactionScoreCard` remain CORE-owned types
- `ResolvedPalette` is reused from `src/ccp/models/ca11_models.py`
- `CanvasComposition` is reused from `src/ccp/models/visual_engine_models.py`
- `public_share_ready` remains false until the VS render exists; a debate may not silently fall back to a solo composition

## 6. Backward Compatibility Fallback

This spec follows the explicit fail-closed posture established by `circuit_breaker.py`.

| Failure Mode | Graceful Degradation |
|---|---|
| Telegram callback payload is malformed or expired | The webhook returns a non-success status, no vote is persisted, and no Vote Then React deep link is issued. The user may retry from the original message. |
| Duplicate inline vote from the same callback token | The vote is marked `duplicate`, existing tallies remain unchanged, and the system does not trigger a second escalation prompt. |
| Counter-take app launch occurs without stance | `DebateStanceGate` stops progression immediately and does not create a CORE session. |
| Counter artifact is missing while the root artifact is already scored | The debate remains in `challenge_open` state and only the source artifact is visible; no VS composition is published. |
| VS composition fails or the wrong template is loaded | The debate stays private or limited to app-local preview, `visual_adversary_passed=false`, and no public debate share card is emitted. |
| `ContentMachinePipeline.process_session(...)` fails for a winning debate | The debate artifact remains valid and shareable, but post-debate content routing is marked retryable and may not be represented as delivered. |
| Redis-style tally cache is stale or unavailable | Permanent vote state falls back to PostgreSQL-backed totals; live tally may lag, but final vote integrity must remain correct. |

## 7. Tasks

### Frontend
- [ ] Create the standalone Debate Mini App in `apps/react-debate/`
- [ ] Add typed launch, vote-prompt, and VS projection contracts in `apps/react-debate/app/lib/types.ts`
- [ ] Implement Debate fetch and counter-react API clients in `apps/react-debate/app/lib/api.ts`
- [ ] Implement stance-bound app state in `apps/react-debate/app/lib/state.ts`
- [ ] Build the debate-lane brief screen in `apps/react-debate/app/components/debate-lane-brief-screen.tsx`
- [ ] Build the mandatory stance gate in `apps/react-debate/app/components/stance-selection-gate.tsx`
- [ ] Build the counter-take recorder in `apps/react-debate/app/components/counter-take-recorder.tsx`
- [ ] Build the jury tally card in `apps/react-debate/app/components/jury-tally-card.tsx`
- [ ] Build the post-vote entry surface in `apps/react-debate/app/components/vote-then-react-entry.tsx`
- [ ] Build the VS artifact projection card in `apps/react-debate/app/components/vs-artifact-card.tsx`

### Backend
- [ ] Create `src/ccp/models/reaction_debate_models.py`
- [ ] Create `src/ccp/services/debate_with_jury_service.py`
- [ ] Modify `src/ccp/api/telegram_webhook.py` for callback-query handling
- [ ] Create `src/ccp/api/debate_with_jury_api.py`
- [ ] Register Debate routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with Debate tables and indexes
- [ ] Write receipt-chain events for vote registration, stance selection, and VS publication
- [ ] Bind Debate CMF routing to `src/ccp/services/content_machine.py`
- [ ] Bind Debate VS rendering to `src/ccp/services/canvas_composition_service.py`

### Verification
- [ ] Create `tests/integration/test_era3_fr05b_debate_api.py`
- [ ] Create `tests/integration/test_era3_fr05b_debate_jury_webhook.py`
- [ ] Create `tests/integration/test_era3_fr05b_debate_rendering.py`
- [ ] Create `apps/react-debate/app/__tests__/stance-selection-gate.test.tsx`
- [ ] Create `apps/react-debate/app/__tests__/jury-tally-card.test.tsx`
- [ ] Create `apps/react-debate/app/__tests__/vote-then-react-prompt.test.tsx`

## 8. Acceptance Criteria

### AC-2.2A - Counter-React Requires a Bound Stance

**CBAR Mandate enforced:** Phase2-M05

**Given** I receive a Debate artifact,
**When** I tap `Counter-React`,
**Then** I must choose either `For` or `Against` before any recording session is created,
**And** the selected stance is permanently bound to the counter-take artifact,
**And** neutral or unlabeled counter-takes are rejected.

**FAILURE EXAMPLE:** A coach enters a debate, records a response without choosing a side, and later publishes a meandering middle-ground take that cannot be classified as adversarial. The mode loses all tribal alignment. This is a spec violation.

**Measurable pass condition:** all counter-take launch payloads contain `selected_stance in {"for", "against"}` and `neutral_allowed == false`, or the API returns a stance-required error and no `session_id`.

### AC-2.2B - Debate Artifacts Must Render as VS, Never Solo

**CBAR Mandate enforced:** Phase2-M05

**Given** both the root take and the counter-take have reached a publishable state,
**When** the debate artifact is composed for public sharing,
**Then** the output render format is `split_screen_vs`,
**And** the composition uses a debate-specific template through `CanvasCompositionService`,
**And** a debate asset may not fall back to a solo visual layout.

**FAILURE EXAMPLE:** The system posts a single-speaker quote card with a vote tally badge and calls it a debate. Jurors cannot visually perceive the opposition, so the asset behaves like Solo content and the adversarial mechanic disappears. This is a spec violation.

**Measurable pass condition:** all published debate share artifacts have `render_format == "split_screen_vs"` and `visual_adversary_passed == true`; any other format blocks public-share readiness.

### AC-3.1A - Audience Jury Voting Works in Native Telegram

**CBAR Mandate enforced:** None directly

**Given** a Debate or Duel artifact is shared to me,
**When** I tap an inline Telegram vote button,
**Then** the vote is registered through `POST /api/telegram/webhook` without opening a Mini App,
**And** no account registration or extra navigation is required,
**And** the tally is persisted against the correct debate side.

**FAILURE EXAMPLE:** A juror taps `Vote For`, is kicked into a Mini App splash screen, and abandons before the vote counts. The social-entry loop collapses under unnecessary friction. This is a spec violation.

**Measurable pass condition:** one inline button callback yields a persisted vote record in a single webhook round-trip, with `opens_mini_app == false` on the vote event and no manual registration step.

### AC-3.2A - Vote Then React Opens Only After Vote Registration

**CBAR Mandate enforced:** None directly

**Given** I cast a vote as an Audience Jury member,
**When** the vote is successfully registered,
**Then** I receive a prompt offering me the chance to defend my vote,
**And** the prompt contains a deep link into `startapp=react_debate`,
**And** no recording prompt is emitted before the vote has been stored.

**FAILURE EXAMPLE:** A user sees a generic "Record your take" prompt before the vote is even saved, or after closing the prompt the system cannot tell which side they chose. The staircase of commitment is broken. This is a spec violation.

**Measurable pass condition:** every prompt contains a valid `source_vote_id` and a `deep_link_url` for `react_debate`, and prompts are generated only from accepted vote events.

### AC-3.2B - Escalation Copy Must Explicitly Tether to the Chosen Side

**CBAR Mandate enforced:** None directly

**Given** I have already voted on a Debate artifact,
**When** the Vote Then React prompt is rendered,
**Then** the prompt copy explicitly references the side I backed,
**And** the Debate Mini App opens with that stance pre-bound or preselected,
**And** the wording feels like defending my position rather than generic onboarding.

**FAILURE EXAMPLE:** After voting `For`, the user receives a neutral message saying only "Want to record something?" with no reference to the side they chose or the argument they endorsed. The prompt reads like spam, not progression. This is a spec violation.

**Measurable pass condition:** prompt copy contains a stance-tethered reference for 100% of generated prompts, and app bootstrap contains the same `selected_stance` as the source vote.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream spec dependency | Topic, session, scorecard, artifact, and vote state contracts |
| `FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/api/telegram_webhook.py` | Code extension | Existing Telegram ingress for inline jury voting and post-vote escalation |
| `src/ccp/api/main.py` | Code extension | Debate route registration and health exposure |
| `src/ccp/services/content_machine.py` | Runtime consumption | `ContentMachinePipeline.process_session(...)` for debate-derived content routing |
| `src/ccp/services/canvas_composition_service.py` | Runtime consumption | `create_composition(...)`, `receive_asset(...)`, and `export_composition(...)` for VS rendering |
| `src/ccp/models/visual_engine_models.py` | Model dependency | `CanvasComposition` and composition statuses |
| `src/ccp/models/ca11_models.py` | Model dependency | `ResolvedPalette` and `ContentMachineResult` |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Immutable logging for vote and composition events |
| `src/ccp/scripts/setup_supabase.py` | Migration dependency | Debate linkage, prompt, and composition projection schema |
| `PRD-06 Conscious Reactions` | Requirements dependency | Canonical Debate, Jury, and silent-referral behavior |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Next.js | workspace-pinned | Debate Mini App runtime in `apps/react-debate/` |
| React | workspace-pinned | Debate UI, stance gate, and projection rendering |
| TypeScript | workspace-pinned | Typed app-side contracts |
| FastAPI | existing backend dependency | Debate API and Telegram webhook extensions |
| Pydantic v2 | existing backend dependency | Typed Debate payload models |
| Redis | existing / planned backend cache | High-velocity vote tally state and dedup support |
| Supabase PostgreSQL | existing backend dependency | Permanent debate, vote, and prompt storage |
| Telegram Bot API | current platform | Inline keyboard callbacks and message edits |
| Telegram Web App API | current platform | Opening `react_debate` only after jury vote |

## 10. Testing Strategy

### Unit Tests

**File:** `apps/react-debate/app/__tests__/stance-selection-gate.test.tsx`
- `describe("StanceSelectionGate")`
- `it("blocks recording until for or against is selected")`
- `it("does not expose a neutral option")`

**File:** `apps/react-debate/app/__tests__/jury-tally-card.test.tsx`
- `describe("JuryTallyCard")`
- `it("renders for and against counts from the projection payload")`
- `it("shows a lag indicator when tally state is degraded")`

**File:** `apps/react-debate/app/__tests__/vote-then-react-prompt.test.tsx`
- `describe("VoteThenReactEntry")`
- `it("renders stance-tethered copy for a for-side vote")`
- `it("renders stance-tethered copy for an against-side vote")`
- `it("opens react_debate with the selected stance token")`

### Integration Tests

Modeled explicitly on `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`:
- use a local `_run()` helper for async service calls
- group tests by acceptance-criterion or behavior class
- create small fixture builders for debate roots, counter-takes, callback payloads, and VS projections
- assert exact model fields, SQL strings, and route behavior directly

**File:** `tests/integration/test_era3_fr05b_debate_api.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestDebateLaunch:
    def test_launch_payload_uses_startapp_react_debate(self): ...
    def test_counter_react_requires_stance_before_session_creation(self): ...


class TestDebateApproval:
    def test_debate_publish_blocks_without_vs_render(self): ...
    def test_visual_adversary_flag_required_for_public_share(self): ...
```

**File:** `tests/integration/test_era3_fr05b_debate_jury_webhook.py`

```python
class TestAudienceJuryWebhook:
    def test_inline_vote_persists_without_mini_app_launch(self): ...
    def test_duplicate_callback_token_does_not_double_count_vote(self): ...
    def test_vote_then_react_prompt_only_emitted_after_vote_accept(self): ...


class TestVoteThenReactPrompt:
    def test_prompt_copy_tethers_to_selected_stance(self): ...
    def test_prompt_deep_link_targets_react_debate(self): ...
```

**File:** `tests/integration/test_era3_fr05b_debate_rendering.py`

```python
class TestVisualAdversaryRule:
    def test_vs_template_used_for_published_debate(self): ...
    def test_solo_template_rejected_for_debate_publish(self): ...


class TestDebateContentRouting:
    def test_content_machine_called_with_debate_adapter_payload(self): ...
    def test_failed_content_machine_call_returns_retryable_projection(self): ...
```

### Manual Verification

1. Share a debate artifact to a Telegram test user and verify the message includes inline jury vote buttons.
2. Tap a vote button and confirm the vote is processed through `POST /api/telegram/webhook` without opening a Mini App.
3. Verify the tally updates in the stored projection and the callback cannot be replayed to double-count.
4. Confirm the post-vote prompt only appears after the vote is accepted.
5. Confirm the prompt copy explicitly references the side the user chose.
6. Open the deep link and verify `startapp=react_debate` launches with the chosen stance preselected.
7. Attempt to record a counter-take without choosing a stance and confirm the session is blocked.
8. Record a valid counter-take and confirm the resulting artifact remains stance-bound.
9. After both sides are publishable, verify the generated debate asset renders as a split-screen / VS composition rather than a solo card.
10. Simulate a missing or invalid VS template and confirm public share is blocked with `visual_adversary_passed=false`.
11. Trigger debate-derived CMF routing and confirm the backend adapter uses `ContentMachinePipeline.process_session(...)`.
12. Verify a published debate can still show delayed or retryable post-debate content routing without falsifying delivery success.
