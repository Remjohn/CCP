# Tech-Spec: FR-ERA3-05f — Blind Rank Reveal Mini App
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

**Created:** 2026-05-11

---

## Pre-Work Log

1. **PROTOCOL LOADED:** `ERA3_Tech_Spec_Writing_Protocol.md` §2.1 confirms Pydantic v2 models under `src/ccp/models/`, and §2.2 confirms new mode routes must follow the existing `app.include_router(..., prefix="/api")` pattern.
2. **PRD LOADED:** PRD-06 mode definition as surfaced in the Era 3 protocol/router line for this feature: `"Coach makes a ranking/preference judgment BEFORE the full context is revealed, then defends it."` The matching source-of-truth section says: `"The coach makes a ranking or preference judgment before the full set or full context is revealed. Then they must defend it."`
3. **EPIC LOADED:** First AC quoted exactly from Story 5.2: `"Given an unknown list of 5 items,"` and `"When Item 1 appears, I must assign it a slot (1-5) permanently before Item 2 is revealed."`
4. **CBAR AUDIT LOADED:** No direct Phase 2 mandate is attached to Story 5.2 in the audit; this spec inherits the CORE session mandates Phase2-M01 through Phase2-M04. The audit and hallucination purge also require correcting legacy `EXP-SFR-*` references to verified `EXP-SAF-*` primitives.
5. **PRIMITIVES LOADED:** `EXP-SAF-002 "Possible-Win Scarcity"`; `EXP-FBK-001 "RIM Feedback Discipline"`; `EXP-TRG-002 "Hook Cycle Velocity"`.
6. **BACKEND FILES READ:** `src/ccp/services/signal_source_loader.py` — `"def load(self) -> SignalBundle"`; `src/ccp/services/trait_scoring_engine.py` — `"def score_all_traits(self) -> list[ScoredTrait]"`; `src/ccp/services/dpa_engine.py` — `"async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = \"\", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive,)"`.
7. **TEST PATTERN:** Read `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`; both use explicit pytest classes/functions, deterministic helper factories, and a local `_run()` helper instead of `pytest-asyncio`.

---

## 1. Files Read

| # | File | Why It Was Read |
|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S10_FR-ERA3-05f_Blind_Rank_Reveal.md` | Prompt, feature scope, output target, irreversibility requirement |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure, stack, route pattern, mode registry |
| 3 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | Story 5.2 acceptance criteria and primitive quality constraint |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | Primitive audit status and hallucination purge |
| 5 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Source-of-truth section `5.6.5 Blind Rank Reveal / Blind Rank Defense` |
| 6 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Conscious Reactions module and brownfield context |
| 7 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Legacy mode inventory line preserving Blind Rank format |
| 8 | `docs/architecture/april_updates/ERA3_Spec_Writing_Briefing.md` | Mode registry and phase mapping cross-check |
| 9 | `primitives/experience/safe_failure_recovery/EXP-SAF-002.yaml` | Canonical safe-failure primitive verification |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Immediate feedback primitive verification |
| 11 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | Loop-cadence primitive verification |
| 12 | `src/ccp/services/signal_source_loader.py` | Existing dependency-loading contract used downstream by shared scoring |
| 13 | `src/ccp/services/trait_scoring_engine.py` | Shared scoring entry point and signal usage pattern |
| 14 | `src/ccp/services/dpa_engine.py` | Existing visual mood/palette resolution contract for final board presentation |
| 15 | `src/ccp/api/main.py` | FastAPI router registration pattern |
| 16 | `src/ccp/api/sacred_audio.py` | Upload route style and error-handling pattern |
| 17 | `src/ccp/core/receipt_chain.py` | Immutable receipt logging contract |
| 18 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Inherited session mandates and shared finalize/export behavior |
| 19 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Integration test style for async service verification |
| 20 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Integration test style for game/state-machine contracts |

## 2. Overview

### 2.1 Problem Statement

`Blind Rank Reveal` only works if the coach is structurally prevented from overthinking. The prompt is explicit: item 1 must be ranked permanently before item 2 appears. If the mode is implemented loosely:

- the frontend will leak future items too early, destroying the blind-judgment mechanic
- teams will add undo, drag-reorder, or “edit before submit” affordances that erase the engineered regret/humor loop
- developers will push irreversibility into the backend and accidentally block the user on server round-trips for what should be a local interaction
- the mode will collapse into a normal ranking UI instead of a pre-context instinct capture format

### 2.2 Solution

Build a standalone Telegram Mini App launched as `startapp=react_blind_rank` under `apps/react-blind-rank/`. The backend supplies a `BlindRankPromptPack` containing an ordered hidden list of five items and session metadata. The Mini App owns a formal local state machine:

- reveal exactly one item
- require the coach to place it into one remaining slot
- lock that slot permanently
- reveal the next item only after the lock commits
- repeat until all five slots are filled
- transition into the defense-recording stage after the board becomes fully immutable

The backend does not adjudicate every slot click in real time. It only provides the prompt pack, receives the finalized immutable board state, and then hands the session into the shared CORE recording/upload/scoring/export path.

### 2.3 Scope In / Out

**In Scope**

- `react_blind_rank` Mini App shell
- formal blind-rank frontend state machine with irreversible slot locking
- prompt-pack contract for ordered hidden items
- local state journaling to survive transient refreshes
- finalize route that persists the completed board and enters CORE recording/scoring
- receipt logging for board completion and irreversible assignments summary

**Out of Scope**

- reimplementing transcription, biometric scoring, or CMF export
- building collaborative blind rank or audience reorder features
- allowing in-session undo or slot reassignment
- adding a desktop tool or Excalidraw surface for this mode

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Purpose |
|---|---|---|---|
| DEP-REA-BRR-001 | `BlindRankRevealAppShell` | Story 5.2 | Dedicated Telegram Mini App launched with `startapp=react_blind_rank` |
| DEP-REA-BRR-002 | `BlindRankPromptPack` | Prompt + Story 5.2 | Ordered hidden-item payload for a single blind-rank session |
| DEP-REA-BRR-003 | `BlindRankStateMachine` | Prompt-specific context | Pure frontend lock/reveal state machine |
| DEP-REA-BRR-004 | `BlindRankStateJournal` | Prompt-specific context | Local durable journal of reveal/lock transitions |
| DEP-REA-BRR-005 | `BlindRankBoardProjection` | Story 5.2 | Immutable board state after each permanent assignment |
| DEP-REA-BRR-006 | `BlindRankFinalizeAdapter` | CORE inheritance | Persists completed blind-rank state and enters shared recording path |
| DEP-REA-BRR-007 | `BlindRankDefenseSession` | Source-of-truth §5.6.5 | Post-board defense recording surface |
| DEP-REA-BRR-008 | `BlindRankRegretCueRenderer` | `EXP-SAF-002` | UI cues that highlight mismatch tension without allowing reversal |
| DEP-OVR-001 | `OverlayRenderer` (Blind Rank Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with blind rank board for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How Used |
|---|---|---|
| `SignalSourceLoader` | `src/ccp/services/signal_source_loader.py` | `def load(self) -> SignalBundle` is the current dependency-loading gateway for downstream scoring. Blind Rank finalize must hand the completed session into the same scoring ecosystem rather than inventing a mini-app-specific scoring branch. |
| `TraitScoringEngine` | `src/ccp/services/trait_scoring_engine.py` | `def score_all_traits(self) -> list[ScoredTrait]` is the existing scoring entry point the CORE engine wraps. Blind Rank uses the same post-recording scoring path after the final board is committed. |
| `DPAEngine` | `src/ccp/services/dpa_engine.py` | `async def resolve(...)` provides the current visual mood/palette resolution contract. The completed board reveal and scorecard should reuse the resolved palette path rather than hard-coding a separate look. |
| `api.main` | `src/ccp/api/main.py` | Shows the authoritative router registration pattern via `app.include_router(..., prefix="/api")`. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | `@router.post("/sacred-audio/upload")` and `async def upload_sacred_audio(...)` establish the existing FastAPI input style and file-handling conventions the mode-specific finalize route should mirror where relevant. |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | `def log(... ) -> ReceiptEntry` is the required immutable audit layer for board completion, session expiry, and degraded outcomes. |

### 3.3 ADR-05 Primitives

| ID | Name | Family | Constraint |
|---|---|---|---|
| `EXP-SAF-002` | Possible-Win Scarcity | safe_failure_recovery | The protocol tables still contain the hallucinated `SFR` family, but the verified registry requires `SAF`. For Blind Rank, the actionable constraint is finite irreversible choice: once a slot is used, the coach must live with it and move forward. The tension is entertaining, but the overall environment remains psychologically safe because the failure is private until export-qualified. |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Every assignment must produce immediate, meaningful local feedback: slot lock, next reveal, remaining-slot countdown, and eventual post-recording score reveal through CORE. Delayed or ambiguous lock feedback breaks the game loop. |
| `EXP-TRG-002` | Hook Cycle Velocity | trigger_timing | The action loop must stay tight: reveal → lock → reveal → lock with no extra confirmation screens. Long pauses, modals, or optional review stages weaken instinct capture and habit-forming cadence. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Inherited via CORE session issuance | `BlindRankPromptPack` includes `issued_at`, `expires_at`, and `ttl_seconds`. If the user opens an expired pack, the mode must reject it and request a fresh session rather than resume stale ranking content. |
| The Background Upload Rule | Phase2-M02 | Inherited via CORE finalize flow | Once the full board is complete and the coach records the defense, stop returns immediately and the defense audio uploads in the background. Blind Rank never blocks on full file upload before feedback. |
| The Streaming Audio SLA | Phase2-M03 | Inherited via CORE scoring flow | Defense scoring uses the same shared streaming chunk path and 3-second readiness SLA. Blind Rank does not run a separate end-of-session transcription batch. |
| The Earned Export Gate | Phase2-M04 | Inherited via CORE artifact gate | A funny or tense blind-rank board does not auto-publish. The defense take must still pass the shared biometric and anti-centroid gates before CMF/export is allowed. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Keep the lock/reveal mechanic entirely client-side | The prompt explicitly defines it as a pure frontend state machine and it requires instant transitions | Round-trip each assignment through the backend before revealing the next item | Adds latency, brittle offline behavior, and unnecessary complexity |
| Backend provides an ordered five-item pack, not a pre-ranked board | The system must control reveal order while preserving blind judgment | Let the frontend generate or shuffle items itself | Weakens determinism and testability |
| No in-session undo or slot swapping after a lock | Story 5.2 requires permanence; regret is the product mechanic | Allow a brief undo timer | Softens the core tension and creates argument over what “permanent” means |
| Persist a local state journal after each assignment | Protects against accidental refresh or tab suspension without moving the mechanic into server orchestration | Keep state only in React memory | One refresh would destroy the session unfairly |
| Transition to recording only after all five slots are locked | The source-of-truth says the coach must defend the final blind judgment | Record commentary after each item | Changes the format into a running commentary instead of a full-reveal defense |
| Reset requires a new session ID after the first lock | Prevents “infinite mulligans” within the same blind-rank challenge | Offer a soft reset button mid-session | Violates irreversibility and undermines `EXP-SAF-002` scarcity |

## 4. Implementation Plan

### Phase 1 — Data Contracts

- [ ] Create `src/ccp/models/reaction_blind_rank_models.py`
- [ ] Define `BlindRankItem`, `BlindRankSlot`, `BlindRankPromptPack`, and `BlindRankBoardProjection`
- [ ] Define `BlindRankStateName` and `BlindRankTransitionName` enums in `src/ccp/models/reaction_blind_rank_models.py`
- [ ] Define `BlindRankFinalizePayload` and `BlindRankSessionProjection` in `src/ccp/models/reaction_blind_rank_models.py`

### Phase 2 — API and Persistence

- [ ] Create `src/ccp/api/reaction_blind_rank_api.py`
- [ ] Add `POST /api/reactions/blind-rank/session` in `src/ccp/api/reaction_blind_rank_api.py`
- [ ] Add `POST /api/reactions/blind-rank/finalize` in `src/ccp/api/reaction_blind_rank_api.py`
- [ ] Register `reaction_blind_rank_api.py` in `src/ccp/api/main.py`
- [ ] Add blind-rank-specific circuit-breaker codes in `src/ccp/core/circuit_breaker.py`
- [ ] Add blind-rank receipt logging adapter in `src/ccp/services/blind_rank_finalize_adapter.py`

### Phase 3 — Mini App State Machine

- [ ] Create `apps/react-blind-rank/package.json`
- [ ] Create `apps/react-blind-rank/src/main.jsx`
- [ ] Create `apps/react-blind-rank/src/App.jsx`
- [ ] Create `apps/react-blind-rank/src/state/blindRankMachine.js`
- [ ] Create `apps/react-blind-rank/src/components/RevealCard.jsx`
- [ ] Create `apps/react-blind-rank/src/components/BlindRankBoard.jsx`
- [ ] Create `apps/react-blind-rank/src/components/DefenseRecordPanel.jsx`
- [ ] Create `apps/react-blind-rank/src/styles.css`

### Phase 4 — Recovery, Visual Tension, and Final Handoff

- [ ] Add local journal persistence in `apps/react-blind-rank/src/state/blindRankJournal.js`
- [ ] Add visible regret cues in `apps/react-blind-rank/src/components/BlindRankBoard.jsx`
- [ ] Resolve final reveal palette through shared DPA integration at the finalize stage
- [ ] Attach blind-rank board metadata to the shared CORE session envelope before recording/scoring

### Phase 5 — Verification

- [ ] Add `tests/unit/test_blind_rank_state_machine.py`
- [ ] Add `tests/integration/test_era3_fr05f_blind_rank_api.py`
- [ ] Add `tests/integration/test_era3_fr05f_blind_rank_state_machine.py`
- [ ] Add manual QA coverage in this spec’s Section 10

## 5. Primary Output Schema

The backend owns the prompt pack and the finalized immutable board payload. The frontend owns the transition logic between states, but those state names and transition contracts must still be typed so backend and client logs remain consistent.

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class BlindRankStateName(str, Enum):
    SESSION_READY = "session_ready"
    ITEM_REVEALED = "item_revealed"
    AWAITING_SLOT_LOCK = "awaiting_slot_lock"
    SLOT_LOCKED = "slot_locked"
    NEXT_ITEM_PENDING = "next_item_pending"
    BOARD_COMPLETE = "board_complete"
    DEFENSE_RECORDING = "defense_recording"
    PROCESSING = "processing"
    SCORED = "scored"
    REDEMPTION_REQUIRED = "redemption_required"
    EXPIRED = "expired"


class BlindRankTransitionName(str, Enum):
    REVEAL_FIRST_ITEM = "reveal_first_item"
    LOCK_SLOT = "lock_slot"
    REVEAL_NEXT_ITEM = "reveal_next_item"
    COMPLETE_BOARD = "complete_board"
    START_DEFENSE_RECORDING = "start_defense_recording"
    FINALIZE_DEFENSE = "finalize_defense"
    EXPIRE_SESSION = "expire_session"


class BlindRankItem(BaseModel):
    item_id: str = Field(..., description="Deterministic item identifier inside this session")
    reveal_index: int = Field(..., ge=1, le=5)
    surface_text: str | None = Field(default=None, description="The visible label. Null until JIT fetched/revealed (AC-5.2B)")
    surface_text_encrypted: str = Field(..., description="Encrypted string for initial payload to prevent inspection")
    subtitle: str | None = Field(default=None)
    revealed: bool = Field(default=False)
    locked_slot: int | None = Field(default=None, ge=1, le=5, description="Computed projection from event log")


class BlindRankSlot(BaseModel):
    slot_number: Literal[1, 2, 3, 4, 5] = Field(...)
    label: str = Field(..., min_length=1, description="Human label for the slot")
    occupied_item_id: str | None = Field(default=None, description="Computed projection from event log")
    locked: bool = Field(default=False)
    locked_at: datetime | None = Field(default=None)


class BlindRankAssignmentEvent(BaseModel):
    assignment_index: int = Field(..., ge=1, le=5)
    item_id: str = Field(...)
    slot_number: Literal[1, 2, 3, 4, 5] = Field(...)
    irreversible: Literal[True] = Field(default=True, description="Canonical source of truth for assignments")
    assigned_at: datetime = Field(...)
    state_after_assignment: BlindRankStateName = Field(...)


class BlindRankPromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_blind_rank"] = Field(default="react_blind_rank")
    source_mode: Literal["blind_rank_reveal"] = Field(default="blind_rank_reveal")
    slot_labels: list[str] = Field(..., min_length=5, max_length=5, description="Visible labels for rank positions")
    ordered_items: list[BlindRankItem] = Field(..., min_length=5, max_length=5, description="Unrevealed text remains encrypted")
    current_state: BlindRankStateName = Field(default=BlindRankStateName.SESSION_READY)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=86400, description="Phase2-M01 Ephemeral Decay mandate")


class BlindRankBoardProjection(BaseModel):
    session_id: str = Field(...)
    slots: list[BlindRankSlot] = Field(..., min_length=5, max_length=5)
    revealed_item_ids: list[str] = Field(default_factory=list, max_length=5)
    remaining_slot_numbers: list[int] = Field(default_factory=list, max_length=5)
    current_item_id: str | None = Field(default=None)
    locked_assignments: list[BlindRankAssignmentEvent] = Field(default_factory=list, max_length=5)
    state_name: BlindRankStateName = Field(...)
    board_complete: bool = Field(default=False)


class BlindRankFinalizePayload(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    recording_session_id: str = Field(..., description="Links board state to streaming audio/video artifact")
    prompt_pack: BlindRankPromptPack = Field(...)
    board_projection: BlindRankBoardProjection = Field(...)
    defense_started_at: datetime = Field(...)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)


class BlindRankSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: BlindRankPromptPack = Field(...)
    board_projection: BlindRankBoardProjection = Field(...)
    scoring_status: Literal[
        "recording",
        "processing",
        "scored",
        "redemption_required",
    ] = Field(...)
    export_eligible: bool = Field(default=False)
    score_ready: bool = Field(default=False)
    receipt_id: str | None = Field(default=None)
```

### Formal State Machine Rules

The frontend state machine must obey the following transition contract:

1. `SESSION_READY -> ITEM_REVEALED`
   Condition: first unrevealed item becomes visible.
2. `ITEM_REVEALED -> AWAITING_SLOT_LOCK`
   Condition: the revealed item is active and at least one open slot exists.
3. `AWAITING_SLOT_LOCK -> SLOT_LOCKED`
   Condition: coach taps one unoccupied slot for the current item.
4. `SLOT_LOCKED -> NEXT_ITEM_PENDING`
   Condition: assignment journal write succeeds locally.
5. `NEXT_ITEM_PENDING -> ITEM_REVEALED`
   Condition: remaining unrevealed items exist.
6. `SLOT_LOCKED -> BOARD_COMPLETE`
   Condition: the fifth assignment has been committed.
7. `BOARD_COMPLETE -> DEFENSE_RECORDING`
   Condition: coach starts final defense recording.
8. `DEFENSE_RECORDING -> PROCESSING`
   Condition: coach stops recording and CORE finalize begins.
9. `PROCESSING -> SCORED` or `REDEMPTION_REQUIRED`
   Condition: shared CORE scoring completes.

**Forbidden Transitions**

- `SLOT_LOCKED -> AWAITING_SLOT_LOCK` for the same item
- any transition that changes `occupied_item_id` for an already locked slot
- revealing item `n+1` before item `n` has been locked
- entering `DEFENSE_RECORDING` before `board_complete == true`

## 6. Backward Compatibility Fallback

This feature must use the `circuit_breaker.py` pattern and fail safely.

| Failure Condition | Fallback Behavior |
|---|---|
| Prompt pack expired before completion | Return `EXPIRED` state and require a fresh session. Previously locked choices are not re-editable inside the expired session. |
| Browser refresh after one or more assignments | Restore from `BlindRankStateJournal` if present. If local journal is missing or corrupted, invalidate the session and require a new one rather than guessing prior assignments. |
| User attempts illegal transition (e.g., reveal next item before lock, reuse occupied slot) | Reject the client action locally, preserve the current state, and log a client diagnostic event. |
| Defense recording upload interrupted | Preserve the finalized board projection and let the shared CORE background-upload retry logic continue or resume. |
| Shared CORE scoring/export path fails | Return the shared degraded session status and preserve the immutable board. The board is never reopened for editing because scoring failed. |

**Non-Negotiable Rule**

After the first slot has been locked, there is no in-session reset or undo. The only valid recovery path is local journal restore or a brand-new session with a new `session_id`.

## 7. Tasks

### Backend

- [ ] Add `src/ccp/models/reaction_blind_rank_models.py` with the state and payload contracts from Section 5
- [ ] Add `src/ccp/api/reaction_blind_rank_api.py`
- [ ] Implement prompt-pack issuance in `src/ccp/api/reaction_blind_rank_api.py`
- [ ] Implement finalize handoff in `src/ccp/api/reaction_blind_rank_api.py`
- [ ] Add `src/ccp/services/blind_rank_finalize_adapter.py`
- [ ] Log immutable board summaries through `src/ccp/core/receipt_chain.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add blind-rank-specific breaker/error codes in `src/ccp/core/circuit_breaker.py`

### Frontend

- [ ] Create `apps/react-blind-rank/src/App.jsx` with dedicated `react_blind_rank` session flow
- [ ] Create `apps/react-blind-rank/src/state/blindRankMachine.js` with the formal transitions from Section 5
- [ ] Create `apps/react-blind-rank/src/state/blindRankJournal.js` to persist each lock event locally
- [ ] Create `apps/react-blind-rank/src/components/RevealCard.jsx`
- [ ] Create `apps/react-blind-rank/src/components/BlindRankBoard.jsx`
- [ ] Create `apps/react-blind-rank/src/components/DefenseRecordPanel.jsx`
- [ ] Create `apps/react-blind-rank/src/styles.css`

### Testing

- [ ] Add unit tests for forbidden transitions, slot locking, and board completion
- [ ] Add integration tests for prompt-pack issuance, finalize handoff, and local-state restoration semantics
- [ ] Add manual QA to verify that every locked slot remains immutable even under refresh and network interruption

## 8. Acceptance Criteria

### AC-5.2A — Each Item Must Be Permanently Ranked Before the Next Item Reveals

**CBAR / Primitive Reference:** Story 5.2, `EXP-SAF-002`

**Given** an unknown list of 5 items,  
**When** Item 1 appears,  
**Then** the coach must assign it to exactly one open slot before Item 2 is revealed,  
**And** that assignment becomes permanently locked for the current session,  
**And** the UI provides no control that can move, swap, or clear the locked item.

**FAILURE EXAMPLE:** Item 1 is placed into Slot 4, Item 2 appears, and the coach can still drag Item 1 into Slot 2 because the app keeps the board “editable until submit.” This is a spec violation.

### AC-5.2B — Reveal Order Must Stay Blind

**CBAR / Primitive Reference:** Story 5.2, source-of-truth §5.6.5

**Given** a valid `BlindRankPromptPack`,  
**When** the session starts,  
**Then** only the first item is visible,  
**And** items 2-5 remain hidden until the preceding item has been locked,  
**And** the app never exposes the full ordered list in previews, metadata drawers, or DOM-hidden text that can be trivially inspected by the user.

**FAILURE EXAMPLE:** The board shows item 1 visibly, but item titles 2-5 are already rendered faintly below it or embedded in a side drawer labeled “upcoming.” This is a spec violation.

### AC-5.2C — Later Reveals Must Create Visible Regret Without Reversal

**CBAR / Primitive Reference:** Story 5.2, `EXP-SAF-002`

**Given** the coach has already committed one or more slots,  
**When** a later item reveals that would have fit an earlier slot better,  
**Then** the UI must visibly show that tension through board contrast, occupied-slot emphasis, or remaining-slot scarcity,  
**And** the prior assignment remains locked,  
**And** the app does not auto-correct or suggest rewriting the prior slot decision.

**FAILURE EXAMPLE:** Item 4 clearly belongs at the top, but because Slot 1 is already occupied the UI silently treats it like any other card and offers a hidden “re-evaluate previous slot” affordance. This is a spec violation.

### AC-5.2D — Defense Recording Starts Only After the Board Is Fully Immutable

**CBAR / Primitive Reference:** Source-of-truth §5.6.5, Phase2-M02, Phase2-M03

**Given** the fifth and final slot has been locked,  
**When** the board reaches `BOARD_COMPLETE`,  
**Then** the app transitions into the defense recording state,  
**And** the finalized board projection is attached to the defense session payload,  
**And** post-stop processing follows the shared CORE background-upload and streaming-score path.

**FAILURE EXAMPLE:** After the third item the app offers a “start defending your ranking now” recording button, producing a partial-defense format that no longer matches Blind Rank Reveal. This is a spec violation.

### AC-5.2E — Scoring and Export Still Obey CORE Gates

**CBAR / Primitive Reference:** Phase2-M04, `EXP-FBK-001`

**Given** the coach finishes the blind-rank defense recording,  
**When** shared scoring completes,  
**Then** the user receives the same immediate private score/status feedback contract as other reaction modes,  
**And** export remains blocked unless the defense take passes the shared quality gates,  
**And** a humorous blind-rank board alone does not bypass the export gate.

**FAILURE EXAMPLE:** The board itself looks entertaining, so the system auto-publishes the artifact even though the defense audio is weak, hedged, and fails the anti-centroid threshold. This is a spec violation.

## 9. Dependencies

### Internal

| Dependency | Type | Why Required |
|---|---|---|
| `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared spec dependency | Authoritative recording/upload/scoring/export lifecycle |
| `docs/architecture/april_updates/FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/services/trait_scoring_engine.py` | Existing scoring service | Shared scoring entry point used downstream by CORE |
| `src/ccp/services/signal_source_loader.py` | Existing dependency loader | Shared signal ingestion contract for scoring dependencies |
| `src/ccp/services/dpa_engine.py` | Existing visual service | Shared palette/mood resolution for final board and scorecard presentation |
| `src/ccp/api/main.py` | Existing API composition | Router registration point |
| `src/ccp/api/sacred_audio.py` | Existing API pattern | Upload route style reference |
| `src/ccp/core/receipt_chain.py` | Existing audit infrastructure | Immutable board/finalize receipts |

### External

| Dependency | Type | Why Required |
|---|---|---|
| Telegram Mini App runtime | Client platform | Required launch surface for `react_blind_rank` |
| Browser `MediaRecorder` + local storage | Client browser capability | Needed for defense recording and local state journaling |
| Sovereign NIM stack | Deployment dependency | Required through CORE for streaming transcript and scoring |

## 10. Testing Strategy

### Unit Tests

- `tests/unit/test_blind_rank_state_machine.py::test_item_two_cannot_reveal_before_item_one_lock`
- `tests/unit/test_blind_rank_state_machine.py::test_locked_slot_cannot_be_reassigned`
- `tests/unit/test_blind_rank_state_machine.py::test_board_complete_only_after_fifth_assignment`
- `tests/unit/test_blind_rank_state_machine.py::test_session_reset_forbidden_after_first_lock`

### Integration Tests

- `tests/integration/test_era3_fr05f_blind_rank_api.py::test_prompt_pack_uses_react_blind_rank_startapp`
- `tests/integration/test_era3_fr05f_blind_rank_api.py::test_finalize_preserves_immutable_board_projection`
- `tests/integration/test_era3_fr05f_blind_rank_state_machine.py::test_refresh_restores_from_local_journal`
- `tests/integration/test_era3_fr05f_blind_rank_state_machine.py::test_illegal_transition_does_not_mutate_state`

### Test Pattern Notes

- Follow the deterministic helper style used in `test_ca11_fr15_dpa_engine.py` and `test_ca11_fr19_trivianar_engine.py`
- Prefer explicit factory helpers for prompt packs and board states
- Use a local `_run()` helper if async service calls are exercised
- Keep state-transition assertions direct and sequential rather than hiding them behind complex fixtures

### Manual QA Checklist

1. Launch the mode with `startapp=react_blind_rank` and verify only one item is visible at session start.
2. Assign Item 1 to a slot and verify Item 2 does not appear until the lock animation/journal commit completes.
3. Attempt to move a previously locked item and verify no drag, tap, or hidden edit affordance changes it.
4. Refresh the page after two assignments and verify the local journal restores the same board and current item.
5. Clear local storage after two assignments and verify the app invalidates the session instead of guessing prior state.
6. Complete all five assignments and verify the app transitions to defense recording only after the board is full.
7. Stop recording and verify the UI releases immediately while upload continues in the background under CORE semantics.
8. Force a poor-quality defense take and verify the board remains immutable while export is blocked by the shared gate.

---

## Appendix — Blind Rank UI Rules

The frontend must enforce the following presentation rules:

1. Remaining open slots must be visually obvious after each lock.
2. Locked slots must use a distinct visual treatment from open slots.
3. Hidden items must remain semantically absent from the visible UI until reveal, not merely visually dimmed.
4. The fifth reveal must feel final; once all slots are occupied, the board should shift from “choice mode” to “defense mode.”
5. Regret cues should heighten humor and tension, not shame. The coach is being challenged, not punished.

This format succeeds only if the user feels the irreversible squeeze while still trusting the environment enough to keep playing through the reveal sequence.
