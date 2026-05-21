# Tech-Spec: FR-ERA3-05i — Authority Quiz Mini App
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

**Created:** 2026-05-11

---

## Pre-Work Log

1. **PROTOCOL LOADED:** `ERA3_Tech_Spec_Writing_Protocol.md` §2.1 confirms model validation is Pydantic v2 under `src/ccp/models/`, and §2.2 confirms new mode APIs must register through the existing `app.include_router(..., prefix="/api")` pattern.
2. **PRD LOADED:** The Era 3 mode registry defines this feature as: `"Escalating-stakes question format inspired by high-stakes quiz mechanics. Visible pressure + urgency + dramatic answer moments. Fast authority proof + answer-under-pressure speaking practice."` The matching source-of-truth line says: `"This is the timed question format inspired by high-stakes quiz structures."`
3. **EPIC LOADED:** First AC quoted exactly from Story 6.2: `"Given I answer correctly,"` and `"When the next question appears, the visual intensity increases."`
4. **CBAR AUDIT LOADED:** No direct story-specific Phase 2 mandate is attached to Story 6.2, so this spec inherits CORE mandates Phase2-M01 through Phase2-M04. Hallucination purge remains relevant because older protocol tables still use outdated `TRB` shorthand, while the verified primitive here is `EXP-TRS-003`.
5. **PRIMITIVES LOADED:** `EXP-TRS-003 "Visceral Hooking"`; `EXP-FBK-001 "RIM Feedback Discipline"`; `EXP-PRG-002 "First Major Win-State"`.
6. **BACKEND FILES READ:** `src/ccp/services/dpa_engine.py` — `"async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = \"\", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None,) -> DPAResult"`; `src/ccp/services/signal_source_loader.py` — `"def load(self) -> SignalBundle"`; `src/ccp/services/trait_scoring_engine.py` — `"def score_all_traits(self) -> list[ScoredTrait]"`.
7. **TEST PATTERN:** Read `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`; both use deterministic pytest helpers, explicit classes/functions, and a local `_run()` helper instead of `pytest-asyncio`.

---

## 1. Files Read

| # | File | Why It Was Read |
|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S13_FR-ERA3-05i_Authority_Quiz.md` | Prompt, output target, DPA escalation requirement |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure, stack, route pattern, mode registry |
| 3 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | Story 6.2 acceptance criteria and primitive quality constraint |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | Primitive audit status and hallucination purge |
| 5 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Source-of-truth section `5.6.8 Authority Quiz / Millionaire-Style Pressure Ladder` |
| 6 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Conscious Reactions module and brownfield context |
| 7 | `docs/architecture/april_updates/ERA3_Spec_Writing_Briefing.md` | Mode registry and phase placement cross-check |
| 8 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Legacy format inventory line preserving Authority Quiz |
| 9 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Canonical DPA/status-share primitive verification |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Immediate feedback primitive verification |
| 11 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Ladder/progression primitive verification |
| 12 | `src/ccp/services/dpa_engine.py` | Current DPA resolve signature and escalation integration boundary |
| 13 | `src/ccp/services/signal_source_loader.py` | Shared downstream dependency-loading contract |
| 14 | `src/ccp/services/trait_scoring_engine.py` | Shared scoring service entry point |
| 15 | `src/ccp/api/main.py` | FastAPI router registration pattern |
| 16 | `src/ccp/api/sacred_audio.py` | Upload endpoint style and handler conventions |
| 17 | `src/ccp/core/receipt_chain.py` | Immutable audit logging contract |
| 18 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Inherited upload/scoring/export behavior |
| 19 | `tests/integration/test_ca11_fr15_dpa_engine.py` | DPA integration test pattern reference |
| 20 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Timed-question/state-ladder integration test pattern reference |

## 2. Overview

### 2.1 Problem Statement

`Authority Quiz` is a pressure ladder, not a flat quiz deck. The mode must intensify visually as the coach keeps answering correctly, and the prompt explicitly requires that this happen through DPA mood-token escalation. If implemented loosely:

- the UI will show identical visual pressure from question 1 through the final round, breaking Story 6.2
- the escalation logic will be hacked into frontend CSS alone, bypassing the existing DPA system and creating style drift
- developers will overload `audience_mood_state` for escalation even though mood and pressure level are separate concepts
- the output will drift too close to protected game-show trade dress instead of borrowing only the underlying mechanics

### 2.2 Solution

Build a standalone Telegram Mini App launched as `startapp=react_authority_quiz` under `apps/react-authority-quiz/`. The backend provides an `AuthorityQuizPromptPack` containing an ordered ladder of questions and level metadata. The client owns the level progression UI and answer flow, but DPA escalation is resolved through an explicit extension to the existing `DPAEngine.resolve(...)` contract:

- base archetype and mood still define the palette family
- a new `escalation_profile` input defines per-level pressure increase
- each correct answer triggers the next question with a stronger resolved palette
- each incorrect answer or fail state stops further escalation and hands the session into the shared CORE scoring/finalize path

### 2.3 Scope In / Out

**In Scope**

- `react_authority_quiz` Mini App shell
- ordered authority-question ladder
- per-correct-answer DPA pressure escalation contract
- explicit escalation profile passed into `DPAEngine.resolve(...)`
- final session projection and shared CORE handoff
- protected-brand-safe implementation that borrows mechanics without copying TV trade dress

**Out of Scope**

- cloning the look/sound/copy of any protected quiz show
- replacing DPA with a one-off authority-quiz styling engine
- multiplayer live-host behavior
- bypassing shared CORE upload/scoring/export gates

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Purpose |
|---|---|---|---|
| DEP-REA-AQZ-001 | `AuthorityQuizAppShell` | Story 6.2 | Dedicated Telegram Mini App launched with `startapp=react_authority_quiz` |
| DEP-REA-AQZ-002 | `AuthorityQuizPromptPack` | Prompt + Story 6.2 | Ordered question ladder with level metadata |
| DEP-REA-AQZ-003 | `AuthorityQuizLevelStateMachine` | Prompt-specific context | Handles correct-answer progression and stop conditions |
| DEP-REA-AQZ-004 | `AuthorityQuizEscalationProfile` | Prompt-specific context | Formal DPA escalation contract for each ladder level |
| DEP-REA-AQZ-005 | `AuthorityQuizDPAAdapter` | Prompt + `dpa_engine.py` | Wraps `DPAEngine.resolve(...)` with escalation-aware input |
| DEP-REA-AQZ-006 | `AuthorityQuizVisualPressureProjection` | Story 6.2 + `EXP-TRS-003` | Captures the resolved intensified palette and pressure metadata |
| DEP-REA-AQZ-007 | `AuthorityQuizSessionProjection` | CORE inheritance | Shared session envelope plus level and escalation state |
| DEP-REA-AQZ-008 | `AuthorityQuizFinalizeAdapter` | CORE inheritance | Bridges completed ladder state into shared recording/scoring/export path |
| DEP-OVR-001 | `OverlayRenderer` (Authority Quiz Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with pressure ladder for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How Used |
|---|---|---|
| `DPAEngine` | `src/ccp/services/dpa_engine.py` | `async def resolve(...) -> DPAResult` is the primary integration boundary. This spec extends that call with an explicit escalation contract rather than replacing the engine. |
| `SignalSourceLoader` | `src/ccp/services/signal_source_loader.py` | `def load(self) -> SignalBundle` remains the shared dependency-loading gateway for downstream scoring and post-quiz evaluation. |
| `TraitScoringEngine` | `src/ccp/services/trait_scoring_engine.py` | `def score_all_traits(self) -> list[ScoredTrait]` is the existing downstream scoring entry point that the shared CORE engine wraps. Authority Quiz finalization must feed into the same scoring ecosystem. |
| `api.main` | `src/ccp/api/main.py` | Shows the canonical router registration pattern for the new mode API. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | `@router.post("/sacred-audio/upload")` and `async def upload_sacred_audio(...)` establish upload-route style and finalize expectations for shared recording paths. |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | `def log(... ) -> ReceiptEntry` is required for escalation-level logging, question-ladder completion, and finalize outcomes. |

### 3.3 ADR-05 Primitives

| ID | Name | Family | Constraint |
|---|---|---|---|
| `EXP-TRS-003` | Visceral Hooking | trust_branding | Story 6.2 requires ambient DPA background intensification. The actionable constraint here is that each step up the ladder should make the coach look more authoritative and high-status, turning the final surface into a stronger credential if they perform well. |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Every correct or incorrect answer must immediately update the ladder, pressure state, and overall status so the user never feels uncertain about whether they advanced. |
| `EXP-PRG-002` | First Major Win-State | progression_replay | The authority ladder should feel like a compact progressive challenge that can scale by question difficulty and level count, not a flat pool of disconnected trivia cards. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Inherited via CORE session issuance | `AuthorityQuizPromptPack` includes `issued_at`, `expires_at`, and `ttl_seconds`. Expired question ladders cannot be resumed as valid sessions. |
| The Background Upload Rule | Phase2-M02 | Inherited via CORE finalize flow | When the quiz session is finalized, the API returns immediately with `upload_status="pending_background"` and the user moves into scoring without blocking on full upload. |
| The Streaming Audio SLA | Phase2-M03 | Inherited via CORE scoring flow | Shared streamed chunks remain the primary path for rapid post-session scoring; Authority Quiz does not wait for a full end-of-recording batch to begin evaluation. |
| The Earned Export Gate | Phase2-M04 | Inherited via CORE artifact gate | A visually intense pressure ladder does not bypass shared biometric, transcript, or anti-slop gates for export. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Add a new `escalation_profile` parameter to `DPAEngine.resolve(...)` | Prompt explicitly requires a new escalation parameter and DPA is the authoritative visual engine | Encode escalation only in frontend CSS without DPA awareness | Breaks backend/frontend visual consistency and makes escalation impossible to audit |
| Keep `audience_mood_state` separate from escalation level | Mood and pressure are orthogonal concerns; a reflective/status palette can intensify over multiple levels | Overload `audience_mood_state` strings like `status_level_3` | Conflates state dimensions and pollutes DPA’s existing mental model |
| Use a structured escalation object instead of a single integer | Needed to specify darkening, contrast boost, and PAD drift explicitly | Pass `level_index` only and let each caller improvise | Too vague for deterministic implementation |
| Preserve protected-brand distance | Source-of-truth explicitly bans imitating protected brands or trade dress | Recreate a famous TV quiz interface directly | Legal/brand risk and unnecessary design copying |
| Reuse shared CORE finalize/scoring path | Prevents a one-off authority-quiz scoring stack | Build a separate authority-only processing engine | Duplicates infrastructure and creates drift across modes |
| Treat older protocol `TRB` shorthand as non-canonical | Verified registry and prompt anchor to `TRS` | Copy protocol family labels literally into implementation docs | Would encode known-invalid family naming into the spec |

## 4. Implementation Plan

### Phase 1 — Data Contracts

- [ ] Create `src/ccp/models/reaction_authority_quiz_models.py`
- [ ] Define `AuthorityQuizQuestion`, `AuthorityQuizPromptPack`, and `AuthorityQuizLevelResult`
- [ ] Define `AuthorityQuizEscalationProfile`, `AuthorityQuizEscalationDelta`, and `AuthorityQuizVisualPressureProjection`
- [ ] Define `AuthorityQuizSessionProjection` in `src/ccp/models/reaction_authority_quiz_models.py`

### Phase 2 — DPA Escalation Extension

- [ ] Extend `src/ccp/services/dpa_engine.py` with an explicit escalation-aware input parameter
- [ ] Create `src/ccp/services/authority_quiz_dpa_adapter.py`
- [ ] Define escalation-to-palette transformation rules in `src/ccp/services/authority_quiz_dpa_adapter.py`
- [ ] Preserve backward compatibility for existing `DPAEngine.resolve(...)` callers when no escalation profile is passed

### Phase 3 — API and Session Flow

- [ ] Create `src/ccp/api/reaction_authority_quiz_api.py`
- [ ] Add `POST /api/reactions/authority-quiz/session` in `src/ccp/api/reaction_authority_quiz_api.py`
- [ ] Add `POST /api/reactions/authority-quiz/finalize` in `src/ccp/api/reaction_authority_quiz_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add authority-quiz-specific breaker/error codes in `src/ccp/core/circuit_breaker.py`

### Phase 4 — Mini App Surface

- [ ] Create `apps/react-authority-quiz/package.json`
- [ ] Create `apps/react-authority-quiz/src/main.jsx`
- [ ] Create `apps/react-authority-quiz/src/App.jsx`
- [ ] Create `apps/react-authority-quiz/src/state/authorityQuizMachine.js`
- [ ] Create `apps/react-authority-quiz/src/components/QuestionLadder.jsx`
- [ ] Create `apps/react-authority-quiz/src/components/PressureBackdrop.jsx`
- [ ] Create `apps/react-authority-quiz/src/components/ResultThresholdPanel.jsx`
- [ ] Create `apps/react-authority-quiz/src/styles.css`

### Phase 5 — Verification

- [ ] Add `tests/unit/test_authority_quiz_dpa_adapter.py`
- [ ] Add `tests/unit/test_authority_quiz_state_machine.py`
- [ ] Add `tests/integration/test_era3_fr05i_authority_quiz_api.py`
- [ ] Add `tests/integration/test_era3_fr05i_authority_quiz_dpa.py`
- [ ] Add manual QA scenarios for escalation and protected-brand distance in Section 10

## 5. Primary Output Schema

The backend owns the question ladder and the DPA escalation contract. The client owns level progression and rendering, but the intensified visual state must still be represented as typed data so it can be tested and preserved.

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class AuthorityQuizLevelState(str, Enum):
    READY = "ready"
    QUESTION_ACTIVE = "question_active"
    ANSWERED_CORRECT = "answered_correct"
    ANSWERED_INCORRECT = "answered_incorrect"
    LADDER_ADVANCED = "ladder_advanced"
    LADDER_COMPLETE = "ladder_complete"
    PROCESSING = "processing"
    SCORED = "scored"
    REDEMPTION_REQUIRED = "redemption_required"
    EXPIRED = "expired"


class AuthorityQuizQuestion(BaseModel):
    question_id: str = Field(...)
    level_index: int = Field(..., ge=1)
    prompt_text: str = Field(..., min_length=5)
    answer_options: list[str] = Field(..., min_length=2, max_length=6)
    correct_answer_key: str = Field(..., min_length=1, max_length=2)
    stakes_label: str = Field(..., min_length=2, description="Visible level framing")
    time_limit_seconds: int = Field(default=20, ge=5, le=120)


class AuthorityQuizEscalationDelta(BaseModel):
    luminance_drop_pct: float = Field(..., ge=0.0, le=0.8)
    contrast_boost_pct: float = Field(..., ge=0.0, le=1.0)
    saturation_boost_pct: float = Field(..., ge=0.0, le=1.0)
    pad_dominance_delta: float = Field(..., ge=0.0, le=1.0)
    pad_arousal_delta: float = Field(..., ge=0.0, le=1.0)


class AuthorityQuizEscalationProfile(BaseModel):
    level_index: int = Field(..., ge=1)
    total_levels: int = Field(..., ge=1)
    escalation_fraction: float = Field(..., ge=0.0, le=1.0)
    delta: AuthorityQuizEscalationDelta = Field(...)


class AuthorityQuizVisualPressureProjection(BaseModel):
    level_index: int = Field(..., ge=1)
    escalation_profile: AuthorityQuizEscalationProfile = Field(...)
    audience_mood_state: str = Field(..., min_length=1)
    palette_token_version: str = Field(default="1.0")
    background_primary: str = Field(..., min_length=4)
    background_secondary: str = Field(..., min_length=4)
    accent: str = Field(..., min_length=4)
    border_emphasis: float = Field(..., ge=0.0, le=1.0)
    ambient_glow_strength: float = Field(..., ge=0.0, le=1.0)


class AuthorityQuizLevelResult(BaseModel):
    question_id: str = Field(...)
    level_index: int = Field(..., ge=1)
    selected_answer_key: str = Field(..., min_length=1, max_length=2)
    was_correct: bool = Field(default=False)
    answered_at: datetime = Field(...)
    state_after_answer: AuthorityQuizLevelState = Field(...)
    pressure_projection: AuthorityQuizVisualPressureProjection = Field(...)


class AuthorityQuizPromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_authority_quiz"] = Field(default="react_authority_quiz")
    source_mode: Literal["authority_quiz"] = Field(default="authority_quiz")
    title: str = Field(..., min_length=3)
    questions: list[AuthorityQuizQuestion] = Field(..., min_length=3, max_length=10)
    base_mood_state: str = Field(..., min_length=1)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=86400)


class AuthorityQuizSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: AuthorityQuizPromptPack = Field(...)
    level_results: list[AuthorityQuizLevelResult] = Field(..., min_length=1, max_length=10)
    current_level_index: int = Field(..., ge=1)
    current_state: AuthorityQuizLevelState = Field(...)
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

### DPA Escalation API Contract

The current DPA engine signature is:

```python
async def resolve(
    coach_id: str,
    content_archetype: str,
    audience_mood_state: str = "",
    brand_hue_analysis: BrandHueAnalysis | None = None,
    override_mode: OverrideMode = OverrideMode.adaptive,
    identity_tokens: dict[str, Any] | None = None,
) -> DPAResult
```

This spec wraps the existing engine via `AuthorityQuizDPAAdapter`. The adapter handles the escalation rather than modifying the upstream `DPAEngine` signature directly (unless explicit Architect approval is granted to migrate `escalation_profile` into the CORE spec):

```python
async def resolve_with_escalation(
    coach_id: str,
    content_archetype: str,
    audience_mood_state: str = "",
    brand_hue_analysis: BrandHueAnalysis | None = None,
    override_mode: OverrideMode = OverrideMode.adaptive,
    identity_tokens: dict[str, Any] | None = None,
    escalation_profile: AuthorityQuizEscalationProfile | None = None,
) -> DPAResult
```

**Contract Rules**

1. `audience_mood_state` remains the base palette family selector.
2. `escalation_profile` is optional and defaults to `None` for all existing callers.
3. If `escalation_profile` is present (applied via the Adapter):
   - darken background values according to `luminance_drop_pct`
   - increase contrast according to `contrast_boost_pct`
   - increase saturation according to `saturation_boost_pct`
   - drift PAD emphasis toward more dramatic authority vectors using `pad_dominance_delta` and `pad_arousal_delta`
   - calculate `border_emphasis` and `ambient_glow_strength` proportionally based on the `escalation_fraction`
4. The adapter must preserve WCAG-safe output and DPA identity tokens.
5. The result must include enough metadata to prove which escalation level was applied.

## 6. Backward Compatibility Fallback

This feature must follow the `circuit_breaker.py` pattern and fail safely.

| Failure Condition | Fallback Behavior |
|---|---|
| `escalation_profile` omitted | `DPAEngine.resolve(...)` behaves exactly as it does today with no escalation applied. |
| DPA escalation application fails for a level | Fall back to the non-escalated base mood token for that level, mark the level degraded in receipt metadata, and continue the quiz. |
| Prompt pack expires mid-ladder | Return `EXPIRED` state and require a fresh session rather than resume stale pressure-ladder content. |
| Shared upload interrupted after ladder completion | Preserve the completed level results and continue with shared CORE retry semantics. |
| Shared scoring/export path fails | Preserve the level ladder and DPA pressure history; scoring failure never rewinds the completed ladder. |

**Non-Negotiable Rule**

Authority Quiz may degrade to a base DPA palette if escalation fails, but it may not silently replace DPA escalation with arbitrary frontend-only color hacks that diverge from the engine contract.

## 7. Tasks

### Backend

- [ ] Add `src/ccp/models/reaction_authority_quiz_models.py`
- [ ] Extend `src/ccp/services/dpa_engine.py` with `escalation_profile`
- [ ] Add `src/ccp/services/authority_quiz_dpa_adapter.py`
- [ ] Add `src/ccp/api/reaction_authority_quiz_api.py`
- [ ] Implement prompt-pack issuance in `src/ccp/api/reaction_authority_quiz_api.py`
- [ ] Implement finalize persistence in `src/ccp/api/reaction_authority_quiz_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add authority-quiz-specific breaker codes in `src/ccp/core/circuit_breaker.py`
- [ ] Log ladder progression and degraded escalation events through `src/ccp/core/receipt_chain.py`

### Frontend

- [ ] Create `apps/react-authority-quiz/src/App.jsx` with dedicated `react_authority_quiz` flow
- [ ] Create `apps/react-authority-quiz/src/state/authorityQuizMachine.js`
- [ ] Create `apps/react-authority-quiz/src/components/QuestionLadder.jsx`
- [ ] Create `apps/react-authority-quiz/src/components/PressureBackdrop.jsx`
- [ ] Create `apps/react-authority-quiz/src/components/ResultThresholdPanel.jsx`
- [ ] Create `apps/react-authority-quiz/src/styles.css`

### Testing

- [ ] Add unit tests for escalation-profile math, backward compatibility, and ladder advancement
- [ ] Add integration tests for DPA escalation round-trips and finalize persistence
- [ ] Add manual QA to verify visual intensification per correct answer and protected-brand-safe presentation

## 8. Acceptance Criteria

### AC-6.2A — Each Correct Answer Must Intensify Visual Pressure

**Primitive Reference:** Story 6.2, `EXP-TRS-003`

**Given** the coach answers correctly,  
**When** the next question appears,  
**Then** the DPA-resolved visual pressure increases for that next level,  
**And** the intensified state is derived from an explicit escalation profile,  
**And** the visual layer is darker, higher-contrast, or otherwise more dramatic than the prior correct level.

**FAILURE EXAMPLE:** The user answers levels 1, 2, and 3 correctly, but every question screen uses the exact same palette and ambient intensity because escalation was left as a frontend TODO. This is a spec violation.

### AC-6.2B — DPA Escalation Must Be Passed Through an Explicit Engine Contract

**Primitive Reference:** Prompt-specific context, `EXP-TRS-003`

**Given** Authority Quiz uses the shared DPA engine,  
**When** a new pressure level is resolved,  
**Then** the caller passes an `AuthorityQuizEscalationProfile` into `DPAEngine.resolve(...)`,  
**And** escalation is not encoded by mutating `audience_mood_state` into ad hoc level strings,  
**And** callers without an escalation profile keep current DPA behavior unchanged.

**FAILURE EXAMPLE:** The implementation sets `audience_mood_state="status_level_4_superdark"` and relies on undocumented string parsing inside the DPA layer. Existing DPA callers become brittle and the escalation contract is untestable. This is a spec violation.

### AC-6.2C — The Mode Must Borrow Mechanics, Not Protected Trade Dress

**Primitive Reference:** Source-of-truth §5.6.8

**Given** the Authority Quiz is inspired by high-stakes quiz structures,  
**When** the Mini App renders the ladder,  
**Then** it may use escalating pressure, timed questions, and dramatic answer moments,  
**And** it must not directly imitate protected TV/game-show branding, copy, or trade dress.

**FAILURE EXAMPLE:** The app reproduces a famous game show’s exact color treatment, wording patterns, and signature layout instead of building a CCP-native pressure ladder. This is a spec violation.

### AC-6.2D — Finalize Must Use Shared CORE Upload and Scoring Contracts

**CBAR Mandate Enforced:** Phase2-M02 and Phase2-M03  
**Primitive Reference:** `EXP-FBK-001`

**Given** the ladder ends through completion or failure,  
**When** the session finalizes,  
**Then** the API returns immediately with `upload_status="pending_background"`,  
**And** the session moves into the shared streamed scoring path,  
**And** the level results and pressure history remain attached to the session projection.

**FAILURE EXAMPLE:** After the final question, the user is blocked on a synchronous upload wait before the app confirms that the ladder has completed. This is a spec violation.

### AC-6.2E — Export Must Still Be Earned

**CBAR Mandate Enforced:** Phase2-M04  
**Primitive Reference:** `EXP-FBK-001`

**Given** the coach reaches high visual pressure and answers multiple questions correctly,  
**When** shared scoring completes,  
**Then** export remains conditional on the shared quality gates,  
**And** dramatic ladder aesthetics do not auto-authorize CMF publication.

**FAILURE EXAMPLE:** The user’s ladder looks elite and intense, but the final recorded performance fails transcript or biometric quality checks. The system still publishes because “the pressure ladder looked premium.” This is a spec violation.

## 9. Dependencies

### Internal

| Dependency | Type | Why Required |
|---|---|---|
| `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared spec dependency | Authoritative upload, streaming, scoring, and export lifecycle |
| `docs/architecture/april_updates/FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/services/dpa_engine.py` | Existing visual service | Base palette and escalation integration boundary |
| `src/ccp/services/trait_scoring_engine.py` | Existing scoring service | Shared downstream scoring entry point |
| `src/ccp/services/signal_source_loader.py` | Existing dependency loader | Shared scoring dependency contract |
| `src/ccp/api/main.py` | Existing API composition | Router registration point |
| `src/ccp/api/sacred_audio.py` | Existing API pattern | Upload route style reference |
| `src/ccp/core/receipt_chain.py` | Existing audit infrastructure | Ladder progression and escalation receipts |

### External

| Dependency | Type | Why Required |
|---|---|---|
| Telegram Mini App runtime | Client platform | Required launch surface for `react_authority_quiz` |
| Browser rendering/CSS transitions | Client browser capability | Required to render escalating pressure states |
| Sovereign NIM stack | Deployment dependency | Required through CORE for scoring and transcript handling |

## 10. Testing Strategy

### Unit Tests

- `tests/unit/test_authority_quiz_dpa_adapter.py::test_level_two_is_more_intense_than_level_one`
- `tests/unit/test_authority_quiz_dpa_adapter.py::test_resolve_without_escalation_profile_preserves_legacy_behavior`
- `tests/unit/test_authority_quiz_dpa_adapter.py::test_escalation_profile_applies_pad_and_contrast_deltas`
- `tests/unit/test_authority_quiz_state_machine.py::test_correct_answer_advances_ladder`
- `tests/unit/test_authority_quiz_state_machine.py::test_incorrect_answer_stops_further_escalation`

### Integration Tests

- `tests/integration/test_era3_fr05i_authority_quiz_api.py::test_session_endpoint_returns_react_authority_quiz_prompt_pack`
- `tests/integration/test_era3_fr05i_authority_quiz_api.py::test_finalize_preserves_level_results_and_pressure_history`
- `tests/integration/test_era3_fr05i_authority_quiz_dpa.py::test_dpa_resolve_accepts_escalation_profile`
- `tests/integration/test_era3_fr05i_authority_quiz_dpa.py::test_degraded_escalation_falls_back_to_base_palette`

### Test Pattern Notes

- Follow the deterministic helper style from `test_ca11_fr15_dpa_engine.py` and `test_ca11_fr19_trivianar_engine.py`
- Prefer explicit ladder and profile factories rather than hidden fixtures
- Use a local `_run()` helper for async DPA calls where needed
- Keep escalation comparisons numeric where possible instead of relying only on screenshot assertions

### Manual QA Checklist

1. Launch the mode with `startapp=react_authority_quiz` and verify the initial ladder renders with a base DPA palette.
2. Answer the first question correctly and verify the next level visibly intensifies.
3. Continue through multiple correct answers and verify the backdrop keeps escalating rather than plateauing.
4. Trigger a DPA escalation failure in a test harness and verify the UI falls back to the base palette while preserving ladder continuity.
5. Confirm that the rendered surface feels pressure-driven but does not copy a protected quiz-show layout or branding pattern.
6. Finalize a completed ladder and verify the UI releases immediately while shared upload/scoring continues in the background.
7. Force a poor-quality final performance and verify export remains blocked despite successful ladder progression.

---

## Appendix — Escalation Rules

The escalation contract must obey these rules:

1. Level 1 is the base mood token with no escalation delta.
2. Each subsequent correct-answer level must be strictly more intense than the previous one on at least one measurable axis.
3. Escalation is cumulative within a session but resets for a new `session_id`.
4. Identity tokens and core brand structure remain stable even as pressure intensifies.
5. Pressure escalation serves authority projection, not brand imitation.
