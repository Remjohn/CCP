# Tech-Spec: FR-ERA3-05h — Last One Standing Mini App
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

**Created:** 2026-05-11

---

## Pre-Work Log

1. **PROTOCOL LOADED:** `ERA3_Tech_Spec_Writing_Protocol.md` §2.1 confirms model validation is Pydantic v2 under `src/ccp/models/`, and §2.2 confirms mode APIs must register through the existing FastAPI `app.include_router(..., prefix="/api")` pattern.
2. **PRD LOADED:** The Era 3 mode registry defines this feature as: `"Elimination format — multiple options narrowed one by one. Strong side-taking, strong comment behavior, intuitive audience participation, natural tension escalation. Excellent for industry hot takes + ranking disagreements."` The matching source-of-truth line says: `"This is the elimination format where multiple options are narrowed down one by one."`
3. **EPIC LOADED:** First AC quoted exactly from Story 5.3: `"Given 8 starting options,"` and `"When I speak, I must eliminate one option per 10-second round."`
4. **CBAR AUDIT LOADED:** No story-specific Phase 2 mandate is attached to Story 5.3; this mode inherits CORE mandates Phase2-M01 through Phase2-M04. The audit hallucination purge also confirms legacy `EXP-SFR-*` references are invalid, so any protocol shorthand pointing to `SFR` must be corrected to verified registry primitives.
5. **PRIMITIVES LOADED:** `EXP-PRG-004 "Long Loops for Habit Formation"`; `EXP-FBK-001 "RIM Feedback Discipline"`; `EXP-PRG-002 "Discover -> On-board -> Immerse -> Master -> Replay"`.
6. **BACKEND FILES READ:** `src/ccp/services/signal_source_loader.py` — `"def load(self) -> SignalBundle"`; `src/ccp/services/trait_scoring_engine.py` — `"def score_all_traits(self) -> list[ScoredTrait]"`; `src/ccp/services/dpa_engine.py` — `"async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = \"\", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive,)"`.
7. **TEST PATTERN:** Read `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`; both use deterministic pytest helpers, explicit classes/functions, and a local `_run()` helper rather than `pytest-asyncio`.

---

## 1. Files Read

| # | File | Why It Was Read |
|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S12_FR-ERA3-05h_Last_One_Standing.md` | Prompt, output target, CSS escalation requirement |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure, stack, route pattern, mode registry |
| 3 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | Story 5.3 acceptance criteria and primitive quality constraint |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | Primitive audit status and hallucination purge |
| 5 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Source-of-truth section `5.6.7 Last One Standing` |
| 6 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Conscious Reactions module and brownfield context |
| 7 | `docs/architecture/april_updates/ERA3_Spec_Writing_Briefing.md` | Mode registry and phase placement cross-check |
| 8 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Legacy format inventory line preserving Last One Standing |
| 9 | `primitives/experience/progression_replay/EXP-PRG-004.yaml` | Canonical pacing-escalation primitive verification |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Immediate feedback primitive verification |
| 11 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Macro progression and repeatability primitive verification |
| 12 | `src/ccp/services/signal_source_loader.py` | Shared downstream dependency-loading contract |
| 13 | `src/ccp/services/trait_scoring_engine.py` | Shared scoring service entry point |
| 14 | `src/ccp/services/dpa_engine.py` | Shared mood/palette resolution service |
| 15 | `src/ccp/api/main.py` | FastAPI router registration pattern |
| 16 | `src/ccp/api/sacred_audio.py` | Upload endpoint style and handler conventions |
| 17 | `src/ccp/core/receipt_chain.py` | Immutable audit logging contract |
| 18 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Inherited upload/scoring/export behavior |
| 19 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Integration test pattern reference |
| 20 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Game-state integration test pattern reference |

## 2. Overview

### 2.1 Problem Statement

`Last One Standing` is not a normal sortable list. It is an elimination ladder where narrative tension comes from irreversible attrition and from the timer becoming harsher as fewer options remain. If implemented loosely:

- the app will let users reorder or “soft eliminate” items after the fact, breaking the mode’s narrative arc
- the timer will remain visually flat across all rounds, ignoring the escalation rule in Story 5.3
- the mode will degrade into a static voting board rather than a paced elimination performance
- elimination order will not be preserved as a first-class artifact, making the final content narrative impossible to reconstruct accurately

### 2.2 Solution

Build a standalone Telegram Mini App launched as `startapp=react_elimination` under `apps/react-elimination/`. The backend provides a `LastOneStandingPromptPack` containing eight starting options plus session metadata. The client owns the round cadence:

- one active 10-second elimination round at a time
- exactly one option eliminated per round (if the 10-second timer expires without user action, the system forces a random elimination)
- permanently recorded elimination order
- progressively more aggressive timer presentation as the active option set shrinks

The mode runs as a single continuous elimination session that hands the final elimination ladder and recording metadata into the shared CORE pipeline for background upload, scoring, and export gating.

### 2.3 Scope In / Out

**In Scope**

- `react_elimination` Mini App shell
- 8-option elimination ladder with one elimination per 10-second round
- permanent elimination-order journal
- timer aggression profiles expressed as explicit CSS/visual states
- final survivor projection and narrative-order persistence
- shared CORE upload/scoring/export handoff

**Out of Scope**

- collaborative audience reordering or multiplayer elimination
- mid-session undo or eliminated-option restoration
- a desktop or Excalidraw surface for this mode
- replacing shared CORE recording/scoring contracts

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Purpose |
|---|---|---|---|
| DEP-REA-LOS-001 | `LastOneStandingAppShell` | Story 5.3 | Dedicated Telegram Mini App launched with `startapp=react_elimination` |
| DEP-REA-LOS-002 | `LastOneStandingPromptPack` | Prompt + Story 5.3 | Eight-option session payload with round and TTL metadata |
| DEP-REA-LOS-003 | `EliminationRoundStateMachine` | Prompt-specific context | Drives round progression and one-elimination-per-round enforcement |
| DEP-REA-LOS-004 | `EliminationJournal` | Prompt-specific context | Persists irreversible elimination order locally and in finalize payload |
| DEP-REA-LOS-005 | `RemainingOptionsProjection` | Story 5.3 | Live board of active vs eliminated options |
| DEP-REA-LOS-006 | `TimerAggressionProfile` | `EXP-PRG-004` | CSS animation contract that intensifies as options dwindle |
| DEP-REA-LOS-007 | `EliminationNarrativeArc` | Prompt-specific context | Final ordered elimination sequence used for content narrative reconstruction |
| DEP-REA-LOS-008 | `LastOneStandingFinalizeAdapter` | CORE inheritance | Persists completed ladder and enters shared recording/scoring/export path |
| DEP-REA-LOS-009 | `LastOneStandingSessionProjection` | Schema Definition | Canonical state envelope exiting the pipeline into the shared CORE engine |
| DEP-AR-001 | `OverlayRenderer` (Elimination Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with elimination board for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How Used |
|---|---|---|
| `SignalSourceLoader` | `src/ccp/services/signal_source_loader.py` | `def load(self) -> SignalBundle` remains the shared dependency-loading entry point for downstream scoring. Last One Standing should feed its finalized session into the same scoring substrate, not an isolated elimination-only engine. |
| `TraitScoringEngine` | `src/ccp/services/trait_scoring_engine.py` | `def score_all_traits(self) -> list[ScoredTrait]` is the existing downstream scoring contract used after shared finalize. |
| `DPAEngine` | `src/ccp/services/dpa_engine.py` | `async def resolve(...)` is the existing visual mood/palette contract. The timer aggression states should escalate within a DPA-compatible palette rather than invent a disconnected style system. |
| `api.main` | `src/ccp/api/main.py` | Shows the canonical router registration pattern for the new mode API. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | `@router.post("/sacred-audio/upload")` and `async def upload_sacred_audio(...)` provide the current upload-route style and file-handling conventions that the mode finalize path should align with. |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | `def log(... ) -> ReceiptEntry` is required for logging elimination-order summaries, expired sessions, and finalized artifacts. |

### 3.3 ADR-05 Primitives

| ID | Name | Family | Constraint |
|---|---|---|---|
| `EXP-PRG-004` | Long Loops for Habit Formation | progression_replay | Story 5.3 uses this primitive to require pacing escalation. For this mode, the actionable constraint is not “long-term analytics,” but cumulative tension across a multi-round sequence: the timer and board pressure must intensify as the field narrows. |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Each elimination must immediately update the board, the remaining-count signal, and the next-round pacing state so the user never feels uncertain about whether the cut was registered. |
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | Last One Standing should function as a repeatable challenge lane, with structured rounds and a clear finish state, rather than a free-form endless ranking tool. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Inherited via CORE session issuance | `LastOneStandingPromptPack` includes `issued_at`, `expires_at`, and `ttl_seconds`. Expired elimination sessions cannot be resumed as valid content sessions. |
| The Background Upload Rule | Phase2-M02 | Inherited via CORE finalize flow | When the user ends the elimination performance, the UI returns immediately with `upload_status="pending_background"` and shared background upload semantics. |
| The Streaming Audio SLA | Phase2-M03 | Inherited via CORE scoring flow | Shared streamed chunks remain the primary path for rapid post-session scoring; Last One Standing does not wait for a full end-of-recording batch to begin evaluation. |
| The Earned Export Gate | Phase2-M04 | Inherited via CORE artifact gate | An elimination ladder only routes to export if the final recorded performance passes shared quality gates. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Use a client-owned elimination state machine with permanent order capture | The prompt centers on round cadence and irreversible narrative arc | Recompute elimination order only from transcript later | Too ambiguous and prone to drift from actual round interactions |
| Run the mode as one continuous elimination session | Story 5.3 describes sequential timed rounds inside one crescendo | Create isolated micro-sessions per elimination | Fragments the narrative arc and weakens escalation |
| Encode timer aggression as explicit profiles (`calm`, `pressured`, `intense`, `final`) | The CSS escalation rule must be testable and deterministic | Tell frontend to “make it feel faster” without a contract | Too vague to implement or verify reliably |
| Persist elimination order locally after each cut | Protects against refresh/suspension while preserving narrative order | Keep state only in React memory | A refresh would destroy the elimination arc unfairly |
| No re-entry of eliminated options | The elimination order is the mode’s core artifact | Allow undo or “revive” actions | Violates the permanent narrative ladder requirement |
| Treat protocol `SFR` references as invalid shorthand | Audit explicitly says `EXP-SFR-*` is hallucinated | Copy `SFR` labels from protocol tables into the spec | Would encode a known-invalid primitive family into implementation docs |

## 4. Implementation Plan

### Phase 1 — Data Contracts

- [ ] Create `src/ccp/models/reaction_elimination_models.py`
- [ ] Define `EliminationOption`, `EliminationRoundPrompt`, and `LastOneStandingPromptPack`
- [ ] Define `TimerAggressionLevel`, `TimerAggressionProfile`, and `EliminationRoundResult` in `src/ccp/models/reaction_elimination_models.py`
- [ ] Define `RemainingOptionsProjection`, `EliminationNarrativeArc`, and `LastOneStandingSessionProjection`

### Phase 2 — API and Finalize Bridge

- [ ] Create `src/ccp/api/reaction_elimination_api.py`
- [ ] Add `POST /api/reactions/elimination/session` in `src/ccp/api/reaction_elimination_api.py`
- [ ] Add `POST /api/reactions/elimination/finalize` in `src/ccp/api/reaction_elimination_api.py`
- [ ] Create `src/ccp/services/elimination_finalize_adapter.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add elimination-specific breaker/error codes in `src/ccp/core/circuit_breaker.py`

### Phase 3 — Mini App State and Animation

- [ ] Create `apps/react-elimination/package.json`
- [ ] Create `apps/react-elimination/src/main.jsx`
- [ ] Create `apps/react-elimination/src/App.jsx`
- [ ] Create `apps/react-elimination/src/state/eliminationMachine.js` (Include double-tap gesture listener to trigger `eliminated_option_id` to prevent accidental single-tap eliminations)
- [ ] Create `apps/react-elimination/src/state/eliminationJournal.js`
- [ ] Create `apps/react-elimination/src/components/EliminationBoard.jsx`
- [ ] Create `apps/react-elimination/src/components/RoundTimer.jsx`
- [ ] Create `apps/react-elimination/src/components/SurvivorRevealPanel.jsx`
- [ ] Create `apps/react-elimination/src/styles.css`

### Phase 4 — Shared CORE Handoff and Styling

- [ ] Attach final elimination narrative metadata to the shared reaction session envelope
- [ ] Resolve palette/token inputs for timer aggression through DPA-compatible visual rules
- [ ] Log elimination-order summary receipts through `src/ccp/core/receipt_chain.py`
- [ ] Preserve `upload_status="pending_background"` and shared finalize semantics from CORE

### Phase 5 — Verification

- [ ] Add `tests/unit/test_elimination_state_machine.py`
- [ ] Add `tests/unit/test_timer_aggression_profiles.py`
- [ ] Add `tests/integration/test_era3_fr05h_elimination_api.py`
- [ ] Add `tests/integration/test_era3_fr05h_elimination_flow.py`
- [ ] Add manual QA scenarios for timer escalation and elimination permanence in Section 10

## 5. Primary Output Schema

The backend owns the prompt pack and finalized elimination ladder. The client owns the per-round transitions and timer aggression state, but those states must still be typed so testing and receipts remain deterministic.

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TimerAggressionLevel(str, Enum):
    CALM = "calm"
    PRESSURED = "pressured"
    INTENSE = "intense"
    FINAL = "final"


class EliminationRoundState(str, Enum):
    READY = "ready"
    ROUND_ACTIVE = "round_active"
    OPTION_ELIMINATED = "option_eliminated"
    ROUND_CLOSED = "round_closed"
    LADDER_COMPLETE = "ladder_complete"
    PROCESSING = "processing"
    SCORED = "scored"
    REDEMPTION_REQUIRED = "redemption_required"
    EXPIRED = "expired"


class EliminationOption(BaseModel):
    option_id: str = Field(...)
    surface_text: str = Field(..., min_length=2)
    subtitle: str = Field(default="")
    eliminated: bool = Field(default=False)
    eliminated_round: int | None = Field(default=None, ge=1, le=7)
    survived_to_end: bool = Field(default=False)


class TimerAggressionProfile(BaseModel):
    level: TimerAggressionLevel = Field(...)
    pulse_duration_ms: int = Field(..., ge=200, le=3000)
    accent_token: str = Field(..., min_length=1, description="CSS variable/token name")
    scale_amplitude: float = Field(..., ge=0.0, le=0.5)
    border_flash_enabled: bool = Field(default=False)


class EliminationRoundPrompt(BaseModel):
    round_index: int = Field(..., ge=1, le=7)
    round_duration_seconds: Literal[10] = Field(default=10)
    active_option_count: int = Field(..., ge=2, le=8)
    aggression_profile: TimerAggressionProfile = Field(...)


class EliminationRoundResult(BaseModel):
    round_prompt: EliminationRoundPrompt = Field(...)
    eliminated_option_id: str = Field(...)
    eliminated_at: datetime = Field(...)
    remaining_option_ids: list[str] = Field(..., min_length=1, max_length=7)
    state_after_round: EliminationRoundState = Field(...)


class LastOneStandingPromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_elimination"] = Field(default="react_elimination")
    source_mode: Literal["last_one_standing"] = Field(default="last_one_standing")
    title: str = Field(..., min_length=3)
    options: list[EliminationOption] = Field(..., min_length=8, max_length=8)
    rounds: list[EliminationRoundPrompt] = Field(..., min_length=7, max_length=7)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=3600)


class RemainingOptionsProjection(BaseModel):
    session_id: str = Field(...)
    active_option_ids: list[str] = Field(..., min_length=1, max_length=8)
    eliminated_option_ids: list[str] = Field(default_factory=list, max_length=7)
    current_round_index: int = Field(..., ge=1, le=7)
    current_state: EliminationRoundState = Field(...)
    current_aggression_level: TimerAggressionLevel = Field(...)


class EliminationNarrativeArc(BaseModel):
    session_id: str = Field(...)
    elimination_order: list[str] = Field(..., min_length=7, max_length=7, description="Ordered first-out to last-out")
    survivor_option_id: str = Field(...)
    total_rounds_completed: Literal[7] = Field(default=7)


class LastOneStandingSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: LastOneStandingPromptPack = Field(...)
    round_results: list[EliminationRoundResult] = Field(..., min_length=1, max_length=7)
    remaining_projection: RemainingOptionsProjection = Field(...)
    narrative_arc: EliminationNarrativeArc | None = Field(default=None)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)
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

### Timer Aggression Mapping

The client must apply these timer profiles deterministically:

| Active Options Remaining | Aggression Level | Required CSS Behavior |
|---|---|---|
| 8-6 | `calm` | steady pulse, low-contrast accent, minimal scale |
| 5-4 | `pressured` | faster pulse, stronger accent shift, visible border activity |
| 3-2 | `intense` | short pulse cycle, stronger chroma contrast, larger scale amplitude |
| 1 survivor decision pending | `final` | fastest pulse, highest contrast within accessibility bounds, explicit final-survivor emphasis |

The timer visual must never remain flat across all seven rounds.

## 6. Backward Compatibility Fallback

This feature must follow the `circuit_breaker.py` pattern and fail safely.

| Failure Condition | Fallback Behavior |
|---|---|
| Prompt pack expired before ladder completion | Return `EXPIRED` state and require a fresh session. Partial elimination ladders are not resumed as valid publishable sessions. |
| Browser refresh mid-ladder | Restore from `EliminationJournal` if available. If journal data is absent or corrupt, invalidate the session instead of guessing elimination order. |
| User attempts to re-activate an eliminated option | Reject locally, preserve current state, and keep the elimination order immutable. |
| Shared upload interrupted after ladder completion | Preserve `narrative_arc` and continue with shared CORE retry semantics. |
| Shared CORE scoring/export path fails | Preserve the elimination ladder and survivor result; scoring failure triggers a transition to the Redemption Round (FR-06-09). |

**Non-Negotiable Rule**

Once an option is eliminated in a round, it cannot re-enter the ladder in the same session.

## 7. Tasks

### Backend

- [ ] Add `src/ccp/models/reaction_elimination_models.py`
- [ ] Add `src/ccp/api/reaction_elimination_api.py`
- [ ] Add `src/ccp/services/elimination_finalize_adapter.py`
- [ ] Implement prompt-pack issuance in `src/ccp/api/reaction_elimination_api.py`
- [ ] Implement finalize persistence in `src/ccp/api/reaction_elimination_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add elimination-specific breaker codes in `src/ccp/core/circuit_breaker.py`
- [ ] Log elimination-order and survivor summaries through `src/ccp/core/receipt_chain.py`

### Frontend

- [ ] Create `apps/react-elimination/src/App.jsx` with dedicated `react_elimination` flow
- [ ] Create `apps/react-elimination/src/state/eliminationMachine.js`
- [ ] Create `apps/react-elimination/src/state/eliminationJournal.js`
- [ ] Create `apps/react-elimination/src/components/EliminationBoard.jsx`
- [ ] Create `apps/react-elimination/src/components/RoundTimer.jsx`
- [ ] Create `apps/react-elimination/src/components/SurvivorRevealPanel.jsx`
- [ ] Create `apps/react-elimination/src/styles.css` with explicit aggression-level selectors

### Testing

- [ ] Add unit tests for one-elimination-per-round enforcement and survivor correctness
- [ ] Add unit tests for CSS aggression-profile selection by remaining-option count
- [ ] Add integration tests for finalize payload persistence and refresh recovery
- [ ] Add manual QA to verify that timer aggression intensifies correctly from round to round

## 8. Acceptance Criteria

### AC-5.3A — One Option Must Be Eliminated Per 10-Second Round

**Primitive Reference:** Story 5.3, `EXP-PRG-004`

**Given** 8 starting options,  
**When** the coach speaks during an active round and executes a double-tap gesture on an option,  
**Then** exactly one option is eliminated in that 10-second round,  
**And** if the 10-second timer expires before a gesture is registered, the system auto-eliminates a random active option,  
**And** the remaining-option count decreases by one,  
**And** the eliminated option cannot be restored in the same session.

**FAILURE EXAMPLE:** The user reaches the end of a round without a committed elimination, and the app quietly advances anyway with all prior options still active, instead of forcing a random elimination. This is a spec violation.

### AC-5.3B — Elimination Order Must Be Permanent and Narrative-Bearing

**Primitive Reference:** Story 5.3, prompt-specific context

**Given** the coach has completed multiple elimination rounds,  
**When** the session state is finalized,  
**Then** the app preserves the full ordered elimination sequence from first-out to last-out,  
**And** the final survivor is derived from that same sequence,  
**And** no later interaction mutates the prior elimination order.

**FAILURE EXAMPLE:** The user eliminates Option C in Round 2, but after refresh the system reconstructs the board only from the final survivor and loses the intermediate elimination sequence. The narrative arc is destroyed. This is a spec violation.

### AC-5.3C — Timer Pressure Must Escalate Visually as Options Dwindle

**Primitive Reference:** Story 5.3, `EXP-PRG-004`

**Given** the challenge progresses from 8 options toward a final survivor,  
**When** fewer options remain,  
**Then** the timer visual becomes more aggressive through faster pulse cadence, stronger color shift, or more intense border/scale behavior,  
**And** the escalation follows deterministic aggression levels that can be tested by remaining-option count.

**FAILURE EXAMPLE:** Round 1 and Round 7 use the exact same timer pulse, color, and emphasis. The mode feels flat instead of escalating. This is a spec violation.

### AC-5.3D — Finalize Must Use Shared CORE Upload and Scoring Contracts

**CBAR Mandate Enforced:** Phase2-M02 and Phase2-M03  
**Primitive Reference:** `EXP-FBK-001`

**Given** the final survivor has been determined,  
**When** the session is finalized,  
**Then** the client receives `upload_status="pending_background"` immediately,  
**And** the session moves into the shared streaming-score path without waiting for the full file upload,  
**And** the elimination ladder remains attached to the session projection.

**FAILURE EXAMPLE:** After the survivor is chosen, the user is blocked on a synchronous upload spinner for 25 seconds before the app acknowledges completion. This is a spec violation.

### AC-5.3E — Export Must Still Be Earned

**CBAR Mandate Enforced:** Phase2-M04  
**Primitive Reference:** `EXP-FBK-001`

**Given** the elimination session has a dramatic narrative arc,  
**When** shared scoring completes,  
**Then** export remains conditional on the shared quality gates,  
**And** a strong ladder alone does not auto-authorize CMF publication,  
**And** any sub-threshold performance must immediately route the user to the Redemption Round (FR-06-09).

**FAILURE EXAMPLE:** The elimination order is entertaining, but the recorded performance is low quality and fails transcript/biometric checks. The system still publishes automatically instead of routing to the Redemption Round. This is a spec violation.

## 9. Dependencies

### Internal

| Dependency | Type | Why Required |
|---|---|---|
| `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared spec dependency | Authoritative upload, streaming, scoring, and export lifecycle |
| `docs/architecture/april_updates/FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/services/trait_scoring_engine.py` | Existing scoring service | Shared downstream scoring entry point |
| `src/ccp/services/signal_source_loader.py` | Existing dependency loader | Shared scoring dependency contract |
| `src/ccp/services/dpa_engine.py` | Existing visual service | Shared palette/mood resolution for escalating timer visuals |
| `src/ccp/api/main.py` | Existing API composition | Router registration point |
| `src/ccp/api/sacred_audio.py` | Existing API pattern | Upload route style reference |
| `src/ccp/core/receipt_chain.py` | Existing audit infrastructure | Elimination-order and finalize receipts |

### External

| Dependency | Type | Why Required |
|---|---|---|
| Telegram Mini App runtime | Client platform | Required launch surface for `react_elimination` |
| Browser local persistence | Client browser capability | Needed to preserve elimination order across refresh or suspension |
| CSS animation engine in browser | Client rendering capability | Required for deterministic timer aggression states |
| Sovereign NIM stack | Deployment dependency | Required through CORE for scoring and transcript handling |

## 10. Testing Strategy

### Unit Tests

- `tests/unit/test_elimination_state_machine.py::test_exactly_one_option_eliminated_per_round`
- `tests/unit/test_elimination_state_machine.py::test_eliminated_option_cannot_reenter_ladder`
- `tests/unit/test_elimination_state_machine.py::test_survivor_is_last_non_eliminated_option`
- `tests/unit/test_timer_aggression_profiles.py::test_aggression_profile_escalates_at_option_thresholds`
- `tests/unit/test_timer_aggression_profiles.py::test_final_profile_has_fastest_pulse`

### Integration Tests

- `tests/integration/test_era3_fr05h_elimination_api.py::test_session_endpoint_returns_react_elimination_prompt_pack`
- `tests/integration/test_era3_fr05h_elimination_api.py::test_finalize_preserves_elimination_narrative_arc`
- `tests/integration/test_era3_fr05h_elimination_flow.py::test_refresh_restores_elimination_order_from_journal`
- `tests/integration/test_era3_fr05h_elimination_flow.py::test_scoring_failure_does_not_reopen_eliminated_options`

### Test Pattern Notes

- Follow the deterministic helper style from `test_ca11_fr15_dpa_engine.py` and `test_ca11_fr19_trivianar_engine.py`
- Prefer explicit prompt-pack and round-result factories
- Use a local `_run()` helper for async service calls where needed
- Keep aggression-profile assertions tied to explicit remaining-option counts rather than screenshot-only checks

### Manual QA Checklist

1. Launch the mode with `startapp=react_elimination` and verify exactly 8 options render initially.
2. Complete one round and verify exactly one option is marked eliminated and cannot be reactivated.
3. Repeat until three options remain and verify the timer has escalated into a visibly more aggressive profile than Round 1.
4. Reach the final rounds and verify the timer uses the strongest aggression state without violating readability/accessibility.
5. Refresh the page mid-ladder and verify the elimination order restores from the local journal.
6. Corrupt or clear the local journal mid-session and verify the app invalidates the session instead of inventing the missing elimination order.
7. Finalize a completed ladder and verify the UI releases immediately while shared upload/scoring continues in the background.
8. Force a poor-quality final recording and verify the elimination ladder remains preserved while export is still blocked by shared quality gates.

---

## Appendix — CSS Escalation Rules

The frontend must expose explicit style hooks for aggression levels:

1. `[data-aggression="calm"]`
2. `[data-aggression="pressured"]`
3. `[data-aggression="intense"]`
4. `[data-aggression="final"]`

At minimum, each level must differ across:

- pulse duration
- accent color intensity
- scale amplitude or border emphasis

The point is not decorative animation. The timer must communicate that the elimination lane is tightening as the field narrows.
