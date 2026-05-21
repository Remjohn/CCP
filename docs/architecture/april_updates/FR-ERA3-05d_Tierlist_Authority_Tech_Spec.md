# Tech-Spec: FR-ERA3-05d - Tierlist Authority Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 2 - Conscious Reactions
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms the existing FastAPI route `POST /api/sacred-audio/upload`,
                      and Section 5.1 classifies Tierlist Authority as `startapp=react_tierlist`, a standalone
                      Mini App distinct from the existing desktop tierlist tool.
2. PRD LOADED:        PRD-06 source-of-truth line required by the protocol for this mode:
                      "The coach is presented with elements to rank. They speak their choices verbally.
                      The UI or post-render system then updates the ranking state according to:
                      - spoken decision
                      - timestamp"
3. EPIC LOADED:       "Given a set of 5 elements, When I say "[Element] goes in S Tier",
                      Then the UI visually moves the element to the S row."
4. CBAR AUDIT LOADED: No direct Tierlist-specific Phase 2 mandate is declared in the audit. This spec inherits
                      CORE mandates Phase2-M01, Phase2-M02, and Phase2-M03 from the shared engine path.
                      Hallucination purge also confirms `EXP-TRB-*` references must be corrected to `EXP-TRS-*`,
                      and `EXP-SFR-*` references must be corrected to `EXP-SAF-*`.
5. PRIMITIVES LOADED: YAML headers verified as written:
                      `experience_primitive_id: "EXP-FBK-004"` / `canonical_name: "Bring the Data Forward"`
                      `experience_primitive_id: "EXP-FRC-003"` / `canonical_name: "The B=MAP Friction Audit"`
                      `experience_primitive_id: "EXP-PRG-002"` / `canonical_name: "Discover -> On-board -> Immerse -> Master -> Replay"`
6. BACKEND FILES READ:BACKEND_REL names no reusable `src/ccp/services/*.py` implementation for Tierlist mode.
                      Verified the explicit non-reuse boundary by reading the existing desktop tool:
                      `tools/tierlist-app/src/App.jsx` - `export default function App()`
                      `tools/tierlist-app/src/main.jsx` - `ReactDOM.createRoot(document.getElementById('root')).render(...)`
                      `tools/tierlist-app/package.json` confirms a Vite/React desktop app with `@excalidraw/excalidraw`,
                      which is not a Telegram Mini App backend service.
7. TEST PATTERN:      `tests/integration/test_ca11_fr15_dpa_engine.py` and
                      `tests/integration/test_ca11_fr19_trivianar_engine.py` both use a local `_run()` helper,
                      class-per-scenario organization, fixture builders/constants, and direct assertions
                      against models, constants, and service results without `pytest-asyncio`.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S08_FR-ERA3-05d_Tierlist_Authority.md` | 2026-05-11 | Assignment prompt, non-reuse boundary, output path |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, Mini App separation doctrine, PRD-06 execution notes |
| 3 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | v6.0, 2026-05-06 | Conscious Reactions module and brownfield inventory |
| 4 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Current source-of-truth, loaded 2026-05-11 | Exact Tierlist Authority mode definition |
| 5 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | 2026-05-08 | Story 5.1 acceptance criteria and quality constraint |
| 6 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | 2026-05-10 | Adversarial audit and primitive hallucination corrections |
| 7 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | 2026-05-11 | Upstream contract for topic, recording, scoring, and upload mandates |
| 8 | `primitives/experience/feedback_scoring/EXP-FBK-004.yaml` | Codified registry | Verified feedback primitive referenced by the story for snap payoff |
| 9 | `primitives/experience/friction_ability/EXP-FRC-003.yaml` | Codified registry | Verified low-friction recording and interaction primitive |
| 10 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Codified registry | Verified progressive unlock / replay primitive |
| 11 | `src/ccp/api/main.py` | 1.0.0 | FastAPI route registration and health extension point |
| 12 | `tools/tierlist-app/package.json` | Current desktop tool package | Confirms existing tool is Vite + React + Excalidraw desktop app |
| 13 | `tools/tierlist-app/src/App.jsx` | Current desktop tool source | Confirms existing tool is full-screen Excalidraw/video-overlay studio |
| 14 | `tools/tierlist-app/src/main.jsx` | Current desktop tool bootstrap | Confirms browser-root render model and no Telegram Mini App shell |
| 15 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Existing | Pytest pattern reference for `_run()` and grouped tests |
| 16 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Existing | Pytest pattern reference for builders, constants, and direct assertions |

## 2. Overview

### 2.1 Problem Statement

Without a dedicated Tierlist Authority Mini App spec, this mode will fail in two predictable ways:
- teams will try to repurpose the existing `tools/tierlist-app/` desktop Excalidraw studio, producing the wrong interaction model, wrong layout assumptions, and no Telegram-native experience
- the core loop will be reduced to a static board plus manual editing instead of the intended "speak -> item snaps into tier" moment that gives the format its authority and replay value

That turns one of the strongest structured content-creation experiences in the system into either a desktop production tool or a dead, low-feedback ranking board.

### 2.2 Solution

This spec builds `react_tierlist` as a standalone Telegram Mini App under `apps/react-tierlist/`. It consumes `FR-ERA3-05-CORE` for topic intake, bounded recording, upload, and score reveal, but adds the new client-side component Tierlist mode uniquely requires: a real-time speech-to-tier-assignment loop that interprets spoken ranking commands and updates board state during recording. The board is not driven by Excalidraw. It is a purpose-built Mini App surface with tier rows, draggable fallback controls, timestamped move events, and a required snap transition when an item lands in a row. The app inherits CORE mandates for topic freshness, background upload, and streaming score readiness while keeping Tierlist-specific state and animation local to the new Mini App.

### 2.3 Scope

**In scope:**
- `startapp=react_tierlist` launch and board bootstrap
- 5-element tierlist board with `S`, `A`, `B`, `C`, and optional lower rows as configured by payload
- real-time speech-to-tier assignment while recording
- timestamped ranking events and board state updates
- visual snap animation when an element lands in a tier row
- bounded recording and score reveal inherited from CORE
- manual fallback controls when speech parsing is degraded
- typed app and backend contracts for Tierlist board state and ranking events

**Out of scope:**
- reuse of `tools/tierlist-app/`
- Excalidraw canvas workflows
- desktop studio overlays, commentary sidebars, or floating video windows
- debate/jury social routing
- tierlist-specific backend scoring engine separate from CORE
- generalized drag-and-drop editor for arbitrary canvases

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-REA-TIER-001 | `TierlistAuthorityAppShell` | Story 5.1 | Standalone `react_tierlist` Telegram Mini App |
| DEP-REA-TIER-002 | `TierlistBoardProjection` | Story 5.1 | Renders rows, elements, current placements, and remaining unranked items |
| DEP-REA-TIER-003 | `VoiceToTierAssignmentLoop` | Story 5.1 | Interprets spoken commands like "`[element]` goes in S Tier" into board mutations |
| DEP-REA-TIER-004 | `TierlistMoveEventLog` | Story 5.1 | Stores timestamped ranking events in sequence order |
| DEP-REA-TIER-005 | `TierSnapAnimationController` | Story 5.1 quality constraint | Produces the required visual payoff when an element lands in a row |
| DEP-REA-TIER-006 | `TierlistManualFallbackControls` | CORE degradation inheritance | Allows tap/drag/manual reassignment if speech parsing is degraded |
| DEP-REA-TIER-007 | `TierlistScoreRevealProjection` | CORE inheritance | Shows the final board and score after recording completes |
| DEP-REA-TIER-008 | `TierlistApiBridge` | FR-ERA3-05d | Thin API layer between app state and CORE-backed recording sessions |
| DEP-REA-TIER-009 | `OverlayRenderer` (Tierlist Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with tier board for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream contract for topic freshness, recording lifecycle, background upload, and sub-3s score reveal behavior |
| `main.py` | `src/ccp/api/main.py` | Registers the Tierlist route module and extends `/health` with tierlist client-readiness diagnostics |
| `tools/tierlist-app/package.json` | `tools/tierlist-app/package.json` | Negative integration boundary proving the existing tool is a Vite desktop app and not a reusable Telegram Mini App |
| `tools/tierlist-app/src/App.jsx` | `tools/tierlist-app/src/App.jsx` | Negative integration boundary proving the existing tool is an Excalidraw/video-overlay studio rather than a tier-row recording Mini App |
| `tools/tierlist-app/src/main.jsx` | `tools/tierlist-app/src/main.jsx` | Negative integration boundary proving standard desktop root rendering, not Telegram shell behavior |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `ResolvedPalette` for DPA theming continuity |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs session start, ranking mutations, finalize, and degraded speech fallback transitions |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends schema to create mandatory `reaction_tierlist_sessions` and `reaction_tierlist_moves` tables for persistent projection storage |

**Existing database tables consumed:**
- `receipt_chain` - audit trail for board mutation and finalize events
- `asset_registry` - board artifact and recording asset IDs
- `resolved_palettes` - DPA continuity across topic and final board state
- `reaction_topics` - topic and payload envelope via CORE
- `reaction_sessions` - bounded recording session state via CORE
- `reaction_artifacts` - final scored artifact via CORE

**Mandatory Tierlist-specific tables introduced by this spec:**
- `reaction_tierlist_sessions` - current board snapshot plus active row placements
- `reaction_tierlist_moves` - ordered, timestamped move log for each ranked item

**Existing API routes extended or called:**
- `POST /api/sacred-audio/upload` - inherited upload/storage pattern through CORE
- `GET /health` - extended with tierlist readiness and degraded speech status
- `GET /api/reactions/tierlist/{session_id}` - board projection read
- `POST /api/reactions/tierlist/{session_id}/move` - manual fallback move
- `POST /api/reactions/tierlist/{session_id}/interpret` - optional explicit speech-command normalization endpoint if the client uses backend-assisted validation

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FBK-004` | Bring the Data Forward | feedback_scoring | Although the story names a "Signature Moment," the canonical YAML is `Bring the Data Forward`; in this spec it governs immediate visible board-state confirmation and cumulative move surfacing rather than a dead static list |
| `EXP-FRC-003` | The B=MAP Friction Audit | friction_ability | Speaking a rank should update the board without manual editing or desktop tooling overhead |
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | The board and ranking interaction should feel structured and replayable rather than dumping users into a complex editing workspace |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Inherited from CORE Story 1.1 | Tierlist sessions may only launch from fresh topic payloads with active expiry windows; stale tierlist boards are not resumable against expired topics |
| The Background Upload Rule | Phase2-M02 | Inherited from CORE Story 1.2 | Recording stop returns immediate control to the Tierlist board/result state while full-fidelity upload continues in the background |
| The Streaming Audio SLA | Phase2-M03 | Inherited from CORE Story 1.3 | Tierlist score reveal and final board projection rely on streaming-state completion rather than waiting for full post-stop transcription |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Build a new `apps/react-tierlist/` Mini App instead of reusing `tools/tierlist-app/` | The prompt explicitly says the existing tool is different and not reusable | Reuse the desktop Excalidraw app | Wrong surface, wrong interaction model, wrong layout assumptions |
| Keep voice-to-tier assignment client-side first | The prompt explicitly calls it a new client-side component and the board must feel immediate during recording | Wait for backend transcription before updating the board | Destroys the live ranking illusion and the snap payoff |
| Persist a move log in addition to final board state | Timestamped spoken decisions are part of the mode definition and enable replay/debugging | Store only the final row for each item | Loses event history and prevents explanation or recovery |
| Add manual fallback move controls | Speech parsing can degrade and the coach still needs to finish the loop | Force restart whenever parsing is ambiguous | Turns a recoverable recognition miss into a failed session |
| Define the snap as an explicit CSS/JS transition requirement | The prompt requires a specified visual payoff | Leave animation quality undefined | Produces bland board updates and misses the core emotional reward |
| Treat the desktop tool only as a negative boundary, not a code dependency | The desktop tool demonstrates what not to inherit | Cherry-pick components from the Excalidraw studio | Imports the wrong abstraction and bloats the Telegram surface |

## 4. Implementation Plan

### Phase 1 - Tierlist App Scaffold
- [ ] Create `apps/react-tierlist/package.json`
- [ ] Create `apps/react-tierlist/tsconfig.json`
- [ ] Create `apps/react-tierlist/next.config.mjs`
- [ ] Create `apps/react-tierlist/app/layout.tsx`
- [ ] Create `apps/react-tierlist/app/page.tsx`
- [ ] Create `apps/react-tierlist/app/globals.css`

### Phase 2 - Board and Voice Interpretation Contracts
- [ ] Create `apps/react-tierlist/app/lib/types.ts`
- [ ] Create `apps/react-tierlist/app/lib/api.ts`
- [ ] Create `apps/react-tierlist/app/lib/state.ts`
- [ ] Create `apps/react-tierlist/app/lib/speech-to-tier.ts`
- [ ] Create `apps/react-tierlist/app/components/tierlist-board.tsx`
- [ ] Create `apps/react-tierlist/app/components/tier-row.tsx`
- [ ] Create `apps/react-tierlist/app/components/unranked-pool.tsx`

### Phase 3 - Ranking Loop and Fallback Controls
- [ ] Create `apps/react-tierlist/app/components/recording-ranking-console.tsx`
- [ ] Create `apps/react-tierlist/app/components/speech-command-chip.tsx`
- [ ] Create `apps/react-tierlist/app/components/manual-move-controls.tsx`
- [ ] Create `apps/react-tierlist/app/components/tier-snap-overlay.tsx`
- [ ] Create `apps/react-tierlist/app/components/score-reveal-board.tsx`

### Phase 4 - Backend Bridge and Persistence
- [ ] Create `src/ccp/models/reaction_tierlist_models.py`
- [ ] Create `src/ccp/services/reaction_tierlist_projection.py`
- [ ] Create `src/ccp/api/reaction_tierlist_api.py`
- [ ] Register Tierlist routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with mandatory tierlist move/state tables
- [ ] Implement `ReactionTierlistProjection` to calculate `total_move_count` and `words_ranked_count` by querying `reaction_tierlist_moves`

### Phase 5 - Verification
- [ ] Create `tests/integration/test_era3_fr05d_tierlist_api.py`
- [ ] Create `tests/integration/test_era3_fr05d_tierlist_projection.py`
- [ ] Create `tests/integration/test_era3_fr05d_tierlist_contracts.py`
- [ ] Create `apps/react-tierlist/app/__tests__/tierlist-board.test.tsx`
- [ ] Create `apps/react-tierlist/app/__tests__/speech-to-tier.test.tsx`
- [ ] Create `apps/react-tierlist/app/__tests__/tier-snap-overlay.test.tsx`

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/reaction_tierlist_models.py`

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ResolvedPalette
from src.ccp.models.reaction_engine_models import (
    ReactionArtifactRecord,
    ReactionScoreCard,
    ReactionSessionRecord,
    ReactionTopicBrief,
)


class TierLabel(str, Enum):
    s = "S"
    a = "A"
    b = "B"
    c = "C"
    d = "D"
    f = "F"


class TierlistItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    asset_url: str | None = None
    current_tier: TierLabel | None = None
    current_rank_index: int | None = Field(default=None, ge=0)


class TierlistMoveEvent(BaseModel):
    event_id: str = Field(..., min_length=1)
    item_id: str = Field(..., min_length=1)
    spoken_phrase: str = Field(..., min_length=1)
    target_tier: TierLabel = Field(...)
    target_rank_index: int = Field(..., ge=0)
    confidence: float = Field(..., ge=0.0, le=1.0) # Fallback threshold: < 0.85
    created_at: datetime = Field(...)
    source: Literal["speech", "manual_fallback"] = Field(default="speech")


class TierlistBoardProjection(BaseModel):
    startapp: Literal["react_tierlist"] = Field(default="react_tierlist")
    topic: ReactionTopicBrief = Field(...)
    session: ReactionSessionRecord | None = None
    tiers: list[TierLabel] = Field(default_factory=lambda: [TierLabel.s, TierLabel.a, TierLabel.b, TierLabel.c])
    ranked_items: list[TierlistItem] = Field(default_factory=list)
    unranked_items: list[TierlistItem] = Field(default_factory=list)
    move_events: list[TierlistMoveEvent] = Field(default_factory=list)
    snap_animation_enabled: bool = Field(default=True)
    speech_degraded: bool = Field(default=False)


class TierlistResultProjection(BaseModel):
    artifact: ReactionArtifactRecord = Field(...)
    final_board: TierlistBoardProjection = Field(...)
    total_move_count: int = Field(default=0, ge=0)
    words_ranked_count: int = Field(default=0, ge=0)
```

**Schema notes:**
- `ReactionTopicBrief`, `ReactionSessionRecord`, `ReactionArtifactRecord`, and `ReactionScoreCard` remain CORE-owned contracts
- `ResolvedPalette` is reused from `src/ccp/models/ca11_models.py`
- the board model is intentionally simple and row-based; it must not depend on Excalidraw scene state

## 6. Backward Compatibility Fallback

This spec follows the explicit fail-closed posture established by `circuit_breaker.py`.

| Failure Mode | Graceful Degradation |
|---|---|
| Speech interpretation confidence `< 0.85` | The move is not auto-applied; the app surfaces a manual confirm or fallback move control instead of guessing silently |
| Client-side speech loop disconnects or degrades mid-recording | Recording may continue under CORE rules, but board updates switch to manual fallback mode and `speech_degraded=true` |
| Topic expires before recording starts | The board is locked and the app requests a fresh topic rather than ranking against stale context |
| Background upload is interrupted after stop | The final board can remain locally visible while upload retry state continues; the score/result publish path follows CORE retry behavior |
| Snap animation cannot run on a low-capability device | The board still updates functionally, but a reduced-motion transition is used instead of skipping visible confirmation entirely |

## 7. Tasks

### Frontend
- [ ] Create the standalone Tierlist Mini App in `apps/react-tierlist/`
- [ ] Add typed board, item, and move contracts in `apps/react-tierlist/app/lib/types.ts`
- [ ] Implement topic/session fetch and finalize clients in `apps/react-tierlist/app/lib/api.ts`
- [ ] Implement local board state in `apps/react-tierlist/app/lib/state.ts`
- [ ] Implement voice command normalization in `apps/react-tierlist/app/lib/speech-to-tier.ts`
- [ ] Build the tierlist board in `apps/react-tierlist/app/components/tierlist-board.tsx`
- [ ] Build the ranked row renderer in `apps/react-tierlist/app/components/tier-row.tsx`
- [ ] Build the unranked pool in `apps/react-tierlist/app/components/unranked-pool.tsx`
- [ ] Build the recording/ranking console in `apps/react-tierlist/app/components/recording-ranking-console.tsx`
- [ ] Build the manual fallback controls in `apps/react-tierlist/app/components/manual-move-controls.tsx`
- [ ] Build the snap payoff overlay in `apps/react-tierlist/app/components/tier-snap-overlay.tsx`
- [ ] Build the score reveal board in `apps/react-tierlist/app/components/score-reveal-board.tsx`

### Backend
- [ ] Create `src/ccp/models/reaction_tierlist_models.py`
- [ ] Create `src/ccp/services/reaction_tierlist_projection.py`
- [ ] Create `src/ccp/api/reaction_tierlist_api.py`
- [ ] Register Tierlist routes in `src/ccp/api/main.py`
- [ ] Add mandatory tierlist session/move tables in `src/ccp/scripts/setup_supabase.py`
- [ ] Calculate `total_move_count` and `words_ranked_count` via the move log query in `reaction_tierlist_projection.py`
- [ ] Write receipt events for ranking moves, finalize, and degraded speech fallback transitions

### Verification
- [ ] Create `tests/integration/test_era3_fr05d_tierlist_api.py`
- [ ] Create `tests/integration/test_era3_fr05d_tierlist_projection.py`
- [ ] Create `tests/integration/test_era3_fr05d_tierlist_contracts.py`
- [ ] Create `apps/react-tierlist/app/__tests__/tierlist-board.test.tsx`
- [ ] Create `apps/react-tierlist/app/__tests__/speech-to-tier.test.tsx`
- [ ] Create `apps/react-tierlist/app/__tests__/tier-snap-overlay.test.tsx`

## 8. Acceptance Criteria

### AC-5.1A - Spoken Rank Moves the Correct Element into the Correct Row

**CBAR Mandate enforced:** Inherited Phase2-M03 timing assumptions through CORE

**Given** a set of 5 elements,
**When** I say "`[Element]` goes in S Tier",
**Then** the app resolves that spoken command to the correct element,
**And** the board updates by moving that element into the `S` row,
**And** the move is stored as a timestamped ranking event.

**FAILURE EXAMPLE:** The coach says "Email nurture goes in S Tier," the app either does nothing or moves the wrong card into `A`, and the board state no longer matches the spoken take. This is a spec violation.

**Measurable pass condition:** a recognized command produces exactly one `TierlistMoveEvent` with the correct `item_id`, `target_tier`, and monotonic timestamp order.

### AC-5.1B - The Tier Snap Produces Immediate Visual Payoff

**CBAR Mandate enforced:** None directly

**Given** a ranking command has been accepted,
**When** the destination row is updated,
**Then** the moved element snaps into place with an explicit visual transition,
**And** that transition provides immediate micro-feedback during recording,
**And** the board never updates as a silent static re-render.

**FAILURE EXAMPLE:** An item teleports into a row with no animation, no tactile payoff, and no visible confirmation that the system heard the coach correctly. The mode feels broken and inert. This is a spec violation.

**Measurable pass condition:** every accepted move triggers the `TierSnapAnimationController` or its reduced-motion equivalent within the same interaction cycle as the board mutation.

### AC-5.1C - The Telegram Mini App Does Not Reuse the Desktop Excalidraw Tool

**CBAR Mandate enforced:** Inherited Phase2-M01 through fresh-launch discipline

**Given** the Tierlist Authority surface is launched from Telegram,
**When** the app renders,
**Then** it uses the dedicated `react_tierlist` Mini App board and state model,
**And** it does not mount the desktop Excalidraw/video-overlay studio from `tools/tierlist-app/`,
**And** the coach can complete the ranking loop entirely inside the Telegram-native surface.

**FAILURE EXAMPLE:** The Telegram launch opens a cramped Excalidraw canvas with sidebar notes and floating video controls copied from the desktop studio. The mode is unusable on mobile and violates the prompt boundary. This is a spec violation.

**Measurable pass condition:** the deployed Mini App bundle excludes `@excalidraw/excalidraw` and renders the dedicated row-based Tierlist board for 100% of Tierlist sessions.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream spec dependency | Topic, recording, upload, and score-reveal contracts |
| `FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/api/main.py` | Code extension | Tierlist route registration and readiness exposure |
| `src/ccp/models/ca11_models.py` | Model dependency | `ResolvedPalette` reuse |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Ordered move and session transition logging |
| `src/ccp/scripts/setup_supabase.py` | Migration dependency | Optional persistent board/move storage |
| `tools/tierlist-app/package.json` | Negative boundary dependency | Proof that the existing tool is not a reusable Mini App dependency |
| `tools/tierlist-app/src/App.jsx` | Negative boundary dependency | Proof that existing Excalidraw/video overlay UI is the wrong surface |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Next.js | workspace-pinned | Tierlist Mini App runtime in `apps/react-tierlist/` |
| React | workspace-pinned | Board state, animation, and fallback controls |
| TypeScript | workspace-pinned | Typed client-side contracts |
| FastAPI | existing backend dependency | Thin Tierlist API bridge |
| Pydantic v2 | existing backend dependency | Typed Tierlist models |
| Telegram Web App API | current platform | Launch and Telegram container behavior |
| Browser `MediaRecorder` | modern mobile browser capability | Voice recording while ranking |
| Browser `SpeechRecognition` or equivalent local speech adapter | browser/runtime capability | Client-side phrase-to-tier interpretation |

## 10. Testing Strategy

### Unit Tests

**File:** `apps/react-tierlist/app/__tests__/speech-to-tier.test.tsx`
- `describe("speech-to-tier")`
- `it("maps '[element] goes in S Tier' to the correct item and tier")`
- `it("rejects low-confidence ambiguous commands without mutating the board")`

**File:** `apps/react-tierlist/app/__tests__/tierlist-board.test.tsx`
- `describe("TierlistBoard")`
- `it("renders ranked rows and unranked items from the projection payload")`
- `it("applies a move event to the correct row and rank index")`

**File:** `apps/react-tierlist/app/__tests__/tier-snap-overlay.test.tsx`
- `describe("TierSnapAnimationController")`
- `it("fires a snap transition when a move is accepted")`
- `it("uses reduced-motion fallback when animation is unavailable")`

### Integration Tests

Modeled explicitly on `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`:
- use a local `_run()` helper for async service calls
- organize tests by scenario or acceptance criterion class
- create small builders for board payloads, move events, and degraded speech cases
- assert exact model fields and route behavior directly

**File:** `tests/integration/test_era3_fr05d_tierlist_projection.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestTierlistProjection:
    def test_spoken_move_creates_timestamped_move_event(self): ...
    def test_board_projection_excludes_excalidraw_scene_state(self): ...
```

**File:** `tests/integration/test_era3_fr05d_tierlist_api.py`

```python
class TestTierlistApi:
    def test_tierlist_session_uses_react_tierlist_startapp(self): ...
    def test_manual_move_fallback_updates_board_when_speech_degraded(self): ...
    def test_expired_topic_blocks_tierlist_start(self): ...
```

**File:** `tests/integration/test_era3_fr05d_tierlist_contracts.py`

```python
class TestTierlistContracts:
    def test_snap_animation_flag_enabled_on_board_projection(self): ...
    def test_final_board_embeds_scorecard_projection(self): ...
    def test_move_event_source_tracks_speech_vs_manual_fallback(self): ...
```

### Manual Verification

1. Launch the Mini App with `startapp=react_tierlist` from Telegram.
2. Confirm the UI is a row-based tier board and not the desktop Excalidraw studio.
3. Verify the board loads with 5 items and an unranked pool.
4. Start recording and say a clear command such as "`Item X` goes in S Tier."
5. Confirm the correct item moves into the `S` row and a visible snap transition fires.
6. Repeat for several items and confirm the move order is preserved in the board projection.
7. Force a low-confidence or ambiguous phrase and confirm the app does not silently mutate the wrong row.
8. Use the manual fallback controls and confirm the board still updates correctly when speech is degraded.
9. Stop recording and confirm the app transitions immediately into result/reveal flow while full upload continues per CORE behavior.
10. Verify the final projection includes the board state and scorecard without any Excalidraw-specific scene payload.
