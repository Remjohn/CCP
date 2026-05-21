# Tech-Spec: FR-ERA3-05g — Alphabet Challenge Mini App
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

**Created:** 2026-05-11

---

## Pre-Work Log

1. **PROTOCOL LOADED:** `ERA3_Tech_Spec_Writing_Protocol.md` §2.1 confirms model validation is Pydantic v2 under `src/ccp/models/`, and §2.2 confirms FastAPI route integration follows `app.include_router(..., prefix="/api")`.
2. **PRD LOADED:** The Era 3 mode registry defines this feature as: `"Timed, letter-based recall under pressure. Coach must respond with constraint (e.g., industry concepts starting with specific letters). High energy, visible pressure, strong pacing practice. Easy scoring."` The matching source-of-truth line says: `"This is the timed, category-based recall format where the coach must respond under pressure, often with a letter-based constraint."`
3. **EPIC LOADED:** First AC quoted exactly from Story 6.1: `"Given the timer starts,"` and `"When a letter appears, I must speak a valid industry term within 3 seconds."`
4. **CBAR AUDIT LOADED:** Phase2-M07 (The Client-Side Timing Rule) is explicitly confirmed in the audit, and this mode also inherits CORE mandates Phase2-M01 through Phase2-M04. Hallucination purge confirms legacy prefix corrections remain active.
5. **PRIMITIVES LOADED:** `EXP-FRC-006 "Hypnosedation Reframing"`; `EXP-FBK-001 "RIM Feedback Discipline"`; `EXP-PRG-002 "Discover -> On-board -> Immerse -> Master -> Replay"`. Note: Story 6.1 labels `EXP-FRC-006` as "Poka-Yoke / Constraint as Focus," but the verified YAML canonical name for that ID is `Hypnosedation Reframing`; the registry is treated as authoritative.
6. **BACKEND FILES READ:** `src/ccp/services/signal_source_loader.py` — `"def load(self) -> SignalBundle"`; `src/ccp/services/trait_scoring_engine.py` — `"def score_all_traits(self) -> list[ScoredTrait]"`; `src/ccp/services/dpa_engine.py` — `"async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = \"\", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive,)"`.
7. **TEST PATTERN:** Read `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`; both use direct pytest classes/functions, deterministic helpers, and a local `_run()` helper rather than `pytest-asyncio`.

---

## 1. Files Read

| # | File | Why It Was Read |
|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S11_FR-ERA3-05g_Alphabet_Challenge.md` | Prompt, output target, timing-rule emphasis |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure, stack, route pattern, mode registry |
| 3 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | Story 6.1 acceptance criteria and quality constraint |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | Phase2-M07 wording, primitive audit status, hallucination purge |
| 5 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Source-of-truth section `5.6.6 Alphabet Challenge` |
| 6 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Conscious Reactions module and brownfield context |
| 7 | `docs/architecture/april_updates/ERA3_Spec_Writing_Briefing.md` | Mode mapping and phase placement cross-check |
| 8 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Legacy mode inventory line preserving Alphabet Challenge |
| 9 | `primitives/experience/friction_ability/EXP-FRC-006.yaml` | Canonical primitive ID and name verification |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Immediate feedback primitive verification |
| 11 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Progression and challenge-scaling primitive verification |
| 12 | `src/ccp/services/signal_source_loader.py` | Existing shared dependency-loading contract |
| 13 | `src/ccp/services/trait_scoring_engine.py` | Shared downstream scoring service |
| 14 | `src/ccp/services/dpa_engine.py` | Existing mood/palette resolution service |
| 15 | `src/ccp/api/main.py` | FastAPI router registration pattern |
| 16 | `src/ccp/api/sacred_audio.py` | Upload endpoint style and handler conventions |
| 17 | `src/ccp/core/receipt_chain.py` | Immutable audit logging contract |
| 18 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Inherited upload/scoring/export behavior |
| 19 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Integration test pattern reference |
| 20 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Integration test pattern for timing/game-style flows |

## 2. Overview

### 2.1 Problem Statement

`Alphabet Challenge` is a timing-sensitive mode where fairness depends on the device clock, not the network. The prompt is explicit: 3-second validation must be client-side. If implemented casually:

- server receipt time will be used as the pass/fail clock, unfairly failing users on slow or unstable connections
- the UI will blur “spoke in time” and “spoke a valid answer,” producing impossible-to-debug round outcomes
- the mode will inherit long-form reaction assumptions and fail to feel like a sharp recall drill
- timing data will be sent to the backend without a formal verification contract, making the session hard to audit

### 2.2 Solution

Build a standalone Telegram Mini App launched as `startapp=react_alphabet` under `apps/react-alphabet/`. The backend provides an `AlphabetChallengePromptPack` containing:

- a category prompt
- an ordered set of letters
- the fixed `answer_window_ms=3000`
- TTL/session metadata

The client owns the timing-critical interaction loop for each round:

1. reveal letter
2. stamp `letter_revealed_at_client_ms` with `performance.now()`
3. wait for the first answer capture trigger
4. stamp `answer_detected_at_client_ms` with `performance.now()`
5. compute `elapsed_ms` locally
6. determine `timing_pass` locally
7. preserve the round result and continue the session

The backend never uses request arrival time to mark the round late. It receives client timing evidence post-round or at finalize, verifies internal consistency, and combines timing results with transcript/semantic validation and the shared CORE scoring/export path.

### 2.3 Scope In / Out

**In Scope**

- `react_alphabet` Mini App shell
- client-side 3-second timing validation using monotonic client timestamps
- prompt-pack contract for category + letter sequence
- round result journaling and post-session server verification
- semantic answer-validity evaluation after capture
- shared CORE handoff for upload, scoring, and export gating

**Out of Scope**

- server-side timing adjudication based on request arrival
- synchronous trivia-room / multiplayer behavior
- generic quiz mechanics unrelated to letter-based recall
- bypassing shared CORE scoring or export contracts

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object | Source | Purpose |
|---|---|---|---|
| DEP-REA-ALP-001 | `AlphabetChallengePromptPack` | Prompt + Story 6.1 | Category prompt, ordered letters, and time-window metadata |
| DEP-REA-ALP-002 | `AlphabetRoundResult` | Section 5 Schema | Atomic result for a single letter challenge |
| DEP-REA-ALP-003 | `AlphabetTimingCapture` | Section 5 Schema | Encapsulates all client-side clock evidence |
| DEP-REA-ALP-004 | `AlphabetTimingVerificationPayload` | Phase2-M07 | Formal server-side verification payload that preserves client timing authority |
| DEP-REA-ALP-005 | `AlphabetSessionProjection` | CORE inheritance | Shared recording/scoring/export session view plus round metadata |
| DEP-REA-ALP-006 | `AlphabetFinalizePayload` | Section 5 Schema | Payload bridging client completion to server scoring |
| DEP-REA-ALP-007 | `AlphabetRoundState` | Section 5 Schema | Tracks progression through the round loop |
| DEP-REA-ALP-008 | `AlphabetChallengeRoundPrompt` | Section 5 Schema | Specific letter and category constraint |

### 3.2 Existing Backend Integration

| File | Path | How Used |
|---|---|---|
| `SignalSourceLoader` | `src/ccp/services/signal_source_loader.py` | `def load(self) -> SignalBundle` remains the shared dependency-loading entry point for downstream scoring. Alphabet Challenge should reuse the same scoring substrate after session capture rather than creating a separate evaluation stack. |
| `TraitScoringEngine` | `src/ccp/services/trait_scoring_engine.py` | `def score_all_traits(self) -> list[ScoredTrait]` is the existing downstream trait-scoring contract. Alphabet Challenge contributes round/timing metadata into the same broader reaction score path. |
| `DPAEngine` | `src/ccp/services/dpa_engine.py` | `async def resolve(...)` provides the current palette and mood contract for high-pressure surfaces and final scorecards. The mode should reuse DPA styling rather than invent a disconnected visual system. |
| `api.main` | `src/ccp/api/main.py` | Shows the canonical router registration pattern for the new mode API. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | `@router.post("/sacred-audio/upload")` and `async def upload_sacred_audio(...)` establish handler style and upload-route expectations for shared recording flows. |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | `def log(... ) -> ReceiptEntry` is required for logging challenge completion, timing-verification anomalies, and scoring outcomes. |

### 3.3 ADR-05 Primitives

| ID | Name | Family | Constraint |
|---|---|---|---|
| `EXP-FRC-006` | Hypnosedation Reframing | friction_ability | Story 6.1 labels this ID as “Poka-Yoke / Constraint as Focus,” but the verified YAML names it `Hypnosedation Reframing`. The practical enforcement here is that the timer and constraint framing must increase instinctive recall rather than trigger panic. The UI should present the 3-second challenge as a clean drill, not a punitive alarm. |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Every round must immediately show the user whether they answered in time, and the overall challenge must move into the shared scoring path without ambiguous wait states. |
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | Alphabet Challenge should feel like a compact, repeatable mastery drill rather than a bloated quiz platform. Difficulty, round count, and letter/category complexity should be carried by the prompt pack so the mode can scale across maturity levels without changing core mechanics. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Inherited via CORE session issuance | `AlphabetChallengePromptPack` includes `issued_at`, `expires_at`, and `ttl_seconds`. Expired challenge packs cannot be resumed as valid sessions. |
| The Background Upload Rule | Phase2-M02 | Inherited via CORE finalize flow | If the mode records the response stream or consolidated defense clip, stop returns immediately with `upload_status="pending_background"` and the user moves into scoring without waiting for full upload. |
| The Streaming Audio SLA | Phase2-M03 | Inherited via CORE scoring flow | Shared recording/scoring still uses streamed chunks and a final <3s readiness path. Alphabet Challenge does not revert to end-of-recording batch transcription as the primary score path. |
| The Earned Export Gate | Phase2-M04 | Inherited via CORE artifact gate | High-speed recall performance does not bypass transcript quality, biometric, or anti-slop gates for downstream export. |
| The Client-Side Timing Rule | Phase2-M07 | Story 6.1 | `AlphabetRoundTimer` stamps reveal and answer events with `performance.now()` (or `Date.now()` fallback only when monotonic clock is unavailable), computes `elapsed_ms` locally, and sets `timing_pass` on-device. The backend may verify monotonic consistency and tamper anomalies, but it must never use server receive time to convert an in-time local pass into a fail. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Timing pass/fail is computed on the client using a monotonic clock | This is the direct implementation of Phase2-M07 and the only fair way to isolate latency | Use request arrival time on the server | Penalizes network conditions instead of user recall speed |
| Separate timing validity from semantic answer validity | A user can answer in time but still give an invalid term; these are distinct failure modes | Collapse both into one boolean called `correct` | Loses diagnostic clarity and weakens coaching value |
| Backend verifies consistency of client timestamps but does not override pass/fail based on latency | Preserves fairness while still allowing anomaly detection | Treat all client timing as untrusted and recompute from server logs | Reintroduces the exact unfairness M07 forbids |
| Pack-provided letters and category are deterministic for the session | Needed for auditability, replay protection, and testability | Let the frontend pick random letters live | Makes post-session verification and reproducibility weaker |
| Use local round journaling after every letter | Protects the session against refresh or transient webview suspension | Keep round state only in memory | One refresh would destroy timing evidence and round history |
| Continue reusing shared CORE scoring/export contracts | Prevents this mode from becoming a parallel scoring platform | Build an isolated alphabet-only engine | Duplicates infrastructure and creates drift across reaction modes |

## 4. Implementation Plan

### Phase 1 — Data Contracts

- [ ] Create `src/ccp/models/reaction_alphabet_models.py`
- [ ] Define `AlphabetChallengePromptPack`, `AlphabetChallengeRoundPrompt`, and `AlphabetChallengeSessionProjection`
- [ ] Define `AlphabetTimingCapture`, `AlphabetRoundResult`, and `TimingVerificationStatus` in `src/ccp/models/reaction_alphabet_models.py`
- [ ] Define `AlphabetFinalizePayload` in `src/ccp/models/reaction_alphabet_models.py`

### Phase 2 — API and Verification

- [ ] Create `src/ccp/api/reaction_alphabet_api.py`

### Phase 2.5 — Backend Pipeline Transformations

- **Stage 1: Intake & Validation**: `AlphabetAnswerValidationService` receives `(coach_id, round_prompt, captured_phrase)`. Transformation: Triggers NIM semantic similarity analysis against the `category_prompt`. Returns `semantic_validity` based on exact confidence thresholds.
- **Stage 2: Timing Verification**: `AlphabetTimingVerifier` receives `AlphabetTimingVerificationPayload`. Transformation: Evaluates `elapsed_ms` and cross-references monotonic timestamps. Outputs `verification_status`.
- **Stage 3: Session Reconciliation**: `AlphabetChallengeFinalizeAdapter` receives verification and validation outputs. Transformation: Aggregates `timing_pass` and `semantic_validity` arrays to compute `rounds_passed_in_time`, `rounds_semantically_valid`, and the final `scoring_status`. Maps orphaned UI states and routes to CORE.
- [ ] Add `POST /api/reactions/alphabet/session` in `src/ccp/api/reaction_alphabet_api.py`
- [ ] Add `POST /api/reactions/alphabet/finalize` in `src/ccp/api/reaction_alphabet_api.py`
- [ ] Create `src/ccp/services/alphabet_answer_validation_service.py`
- [ ] Create `src/ccp/services/alphabet_timing_verifier.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add mode-specific error codes in `src/ccp/core/circuit_breaker.py`

### Phase 3 — Mini App Client Timing Engine

- [ ] Create `apps/react-alphabet/package.json`
- [ ] Create `apps/react-alphabet/src/main.jsx`
- [ ] Create `apps/react-alphabet/src/App.jsx`
- [ ] Create `apps/react-alphabet/src/state/alphabetRoundTimer.js`
- [ ] Create `apps/react-alphabet/src/state/alphabetRoundJournal.js`
- [ ] Create `apps/react-alphabet/src/components/LetterPromptCard.jsx`
- [ ] Create `apps/react-alphabet/src/components/RoundProgressRail.jsx`
- [ ] Create `apps/react-alphabet/src/components/ChallengeScorePanel.jsx`
- [ ] Create `apps/react-alphabet/src/styles.css`

### Phase 4 — Shared CORE Handoff

- [ ] Attach round metadata to the shared reaction session envelope before finalize
- [ ] Reuse DPA mood resolution for challenge/score visuals
- [ ] Log timing anomalies and session completion via `src/ccp/core/receipt_chain.py`
- [ ] Preserve `upload_status="pending_background"` and shared finalize semantics from CORE

### Phase 5 — Verification

- [ ] Add `tests/unit/test_alphabet_round_timer.py`
- [ ] Add `tests/unit/test_alphabet_timing_verifier.py`
- [ ] Add `tests/integration/test_era3_fr05g_alphabet_api.py`
- [ ] Add `tests/integration/test_era3_fr05g_alphabet_timing.py`
- [ ] Add manual QA scenarios for latency and local-clock timing in Section 10

## 5. Primary Output Schema

The client owns timing authority for each round. The server owns verification, semantic validity, and session persistence. The schema must keep those boundaries explicit.

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TimingVerificationStatus(str, Enum):
    VERIFIED = "verified"
    VERIFIED_WITH_DRIFT = "verified_with_drift"
    SUSPICIOUS = "suspicious"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class AlphabetRoundState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ANSWER_CAPTURED = "answer_captured"
    TIMEOUT = "timeout"
    CLOSED = "closed"


class AlphabetChallengeRoundPrompt(BaseModel):
    round_index: int = Field(..., ge=1)
    letter: str = Field(..., min_length=1, max_length=1, description="Displayed constraint letter")
    category_prompt: str = Field(..., min_length=3, description="Domain/category for valid answers")
    answer_window_ms: Literal[3000] = Field(default=3000)


class AlphabetTimingCapture(BaseModel):
    client_clock_source: Literal["performance.now", "date.now_fallback"] = Field(...)
    letter_revealed_at_client_ms: float = Field(..., ge=0)
    answer_detected_at_client_ms: float | None = Field(default=None, ge=0)
    elapsed_ms: float | None = Field(default=None, ge=0)
    timing_pass: bool = Field(default=False)
    client_epoch_revealed_at_ms: int = Field(..., ge=0, description="Wall clock for coarse audit correlation")
    client_epoch_answered_at_ms: int | None = Field(default=None, ge=0)
    submission_enqueued_at_ms: int | None = Field(default=None, ge=0)
    submission_sent_at_ms: int | None = Field(default=None, ge=0)


class AlphabetRoundResult(BaseModel):
    prompt: AlphabetChallengeRoundPrompt = Field(...)
    state: AlphabetRoundState = Field(...)
    timing: AlphabetTimingCapture = Field(...)
    captured_phrase: str = Field(default="", description="Client-side captured answer text or first-pass transcript")
    semantic_validity: Literal[
        "pending",
        "valid",
        "invalid",
        "ambiguous",
    ] = Field(default="pending", description="valid (NIM confidence >= 0.85), invalid (< 0.60), ambiguous (0.60-0.84, preserves score but triggers async human review)")
    failure_reason: Literal[
        "none",
        "timeout",
        "invalid_term",
        "empty_answer",
        "suspicious_timing",
    ] = Field(default="none")


class AlphabetChallengePromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_alphabet"] = Field(default="react_alphabet")
    source_mode: Literal["alphabet_challenge"] = Field(default="alphabet_challenge")
    challenge_title: str = Field(..., min_length=3)
    rounds: list[AlphabetChallengeRoundPrompt] = Field(..., min_length=1, max_length=26)
    current_round_index: int = Field(default=1, ge=1)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=3600)


class AlphabetTimingVerificationPayload(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    round_results: list[AlphabetRoundResult] = Field(..., min_length=1, max_length=26)
    verification_status: TimingVerificationStatus = Field(...)
    suspicious_round_indexes: list[int] = Field(default_factory=list, max_length=26)
    server_received_at: datetime = Field(...)
    receipt_id: str | None = Field(default=None)


class AlphabetFinalizePayload(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: AlphabetChallengePromptPack = Field(...)
    timing_payload: AlphabetTimingVerificationPayload = Field(...)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)


class AlphabetChallengeSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: AlphabetChallengePromptPack = Field(...)
    round_results: list[AlphabetRoundResult] = Field(..., min_length=1, max_length=26)
    rounds_passed_in_time: int = Field(default=0, ge=0)
    rounds_semantically_valid: int = Field(default=0, ge=0)
    verification_status: TimingVerificationStatus = Field(...)
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

### Field Resolution Rules

The shared CORE engine and pipeline stages populate the Alphabet-specific projection fields as follows:
- `failure_reason`: Assigned dynamically during Stage 1/2. Defaults to `none`. Set to `timeout` if `timing_pass == False`. Set to `invalid_term` if `semantic_validity == "invalid"`. Set to `suspicious_timing` if `verification_status == "suspicious"`. Set to `empty_answer` if `captured_phrase` is empty.
- `scoring_status`: Mapped directly from the shared CORE `TraitScoringEngine`. `recording` until finalized, `processing` during NIM evaluation, `scored` upon success, `redemption_required` if biometric thresholds fail.
- `export_eligible`: True ONLY if `verification_status == "verified"` AND biometric CORE score >= minimum passing threshold. Suspicious timing explicitly forces this to False to prevent unverified artifacts from reaching the CMF.
- `score_ready`: Boolean flag indicating if the shared CORE `TraitScoringEngine` has returned the final `ScoredTrait` list.

### Client-Side Timing Validation Flow

The following flow is mandatory for every round:

1. Client renders the current letter.
2. Client immediately stamps `letter_revealed_at_client_ms = performance.now()`.
3. Client also stamps `client_epoch_revealed_at_ms = Date.now()` for coarse audit correlation only.
4. Client listens for the first answer-detected event.
   Valid trigger sources may be:
   - VAD threshold crossing
   - explicit transcript partial arrival from local/stream bridge
   - manual answer-lock trigger if voice path requires it
5. On detection, client stamps `answer_detected_at_client_ms = performance.now()`.
6. Client computes `elapsed_ms = answer_detected_at_client_ms - letter_revealed_at_client_ms`.
7. Client sets `timing_pass = elapsed_ms <= 3000`.
8. Only after local timing is latched may the answer metadata be sent or queued for server verification.

### Server Verification Rules

The backend may:

- recompute `elapsed_ms` from the two client monotonic timestamps
- verify timestamps are monotonic and non-negative
- compare coarse epoch timestamps to detect impossible or obviously tampered sequences (e.g., mark `suspicious` if `(client_epoch_answered_at_ms - client_epoch_revealed_at_ms) - elapsed_ms > 2000ms`)
- compare the answer timing against available audio-chunk/session evidence
- mark a round or session `suspicious`

### Projection Resolution Rules

When assembling the `AlphabetChallengeSessionProjection`, the backend must derive summary fields as follows:
- `rounds_passed_in_time`: Count of `AlphabetRoundResult` where `timing.timing_pass == True`.
- `rounds_semantically_valid`: Count of `AlphabetRoundResult` where `semantic_validity == "valid"`.
- `export_eligible`: Evaluates to `True` only if `rounds_semantically_valid >= (len(round_results) * 0.8)` AND the session passes all inherited CORE biometric and transcript gates.

The backend may **not**:

- use server request receive time as the primary pass/fail clock
- convert a locally in-time answer into a late answer because the packet arrived after 3 seconds
- punish transient network delay as user failure

## 6. Backward Compatibility Fallback

This feature must follow the `circuit_breaker.py` pattern and fail safely.

| Failure Condition | Fallback Behavior |
|---|---|
| `performance.now()` unavailable | Use `Date.now()` fallback, set `client_clock_source="date.now_fallback"`, and mark the session `verified_with_drift` if other data remains coherent. |
| Round metadata cannot be sent immediately due to connectivity | Persist the local round journal and queue the payload for later submission. Timing pass remains whatever the client computed at capture time. |
| Server finds timing metadata incomplete or suspicious | Mark `verification_status="suspicious"` or `insufficient_evidence`, log a receipt entry, and reconcile by preserving the client `timing_pass` for user feedback but setting `export_eligible=False` downstream to prevent unverified artifacts from reaching the CMF. |
| Shared audio upload interrupted | Preserve the completed round journal and continue with CORE retry semantics using `upload_status="failed_retryable"` if necessary. |
| Expired prompt pack opened | Invalidate the session under M01 and require a fresh pack rather than resuming stale timing rounds. |

**Non-Negotiable Rule**

Latency between device and server is never a valid reason to fail a 3-second round. It may justify a verification flag, but not a timing penalty.

## 7. Tasks

### Backend

- [ ] Add `src/ccp/models/reaction_alphabet_models.py`
- [ ] Add `src/ccp/api/reaction_alphabet_api.py`
- [ ] Add `src/ccp/services/alphabet_answer_validation_service.py`
- [ ] Add `src/ccp/services/alphabet_timing_verifier.py`
- [ ] Implement prompt-pack issuance in `src/ccp/api/reaction_alphabet_api.py`
- [ ] Implement finalize verification in `src/ccp/api/reaction_alphabet_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add receipt logging for suspicious or drifted sessions through `src/ccp/core/receipt_chain.py`
- [ ] Add alphabet-specific breaker codes in `src/ccp/core/circuit_breaker.py`

### Frontend

- [ ] Create `apps/react-alphabet/src/App.jsx` with dedicated `react_alphabet` challenge flow
- [ ] Create `apps/react-alphabet/src/state/alphabetRoundTimer.js` using `performance.now()` as the default clock
- [ ] Create `apps/react-alphabet/src/state/alphabetRoundJournal.js` for local persistence
- [ ] Create `apps/react-alphabet/src/components/LetterPromptCard.jsx`
- [ ] Create `apps/react-alphabet/src/components/RoundProgressRail.jsx`
- [ ] Create `apps/react-alphabet/src/components/ChallengeScorePanel.jsx`
- [ ] Create `apps/react-alphabet/src/styles.css`

### Testing

- [ ] Add unit tests for 3000ms threshold handling, fallback clock behavior, and suspicious-timing detection
- [ ] Add integration tests for API finalize, latency tolerance, and local pass preservation under delayed submission
- [ ] Add manual QA to validate M07 on high-latency simulated connections

## 8. Acceptance Criteria

### AC-6.1A — 3-Second Timing Must Be Validated Client-Side

**CBAR Mandate Enforced:** Phase2-M07 — The Client-Side Timing Rule  
**Primitive Reference:** Story 6.1, `EXP-FRC-006`

**Given** the timer starts,  
**When** a letter appears,  
**Then** the client stamps the reveal time locally,  
**And** the client determines whether the answer was started within 3 seconds using its own monotonic timestamps,  
**And** the backend does not substitute server receive time for the pass/fail judgment.

**FAILURE EXAMPLE:** The user begins speaking 2.4 seconds after the letter appears, but the packet reaches the backend 3.6 seconds later over a congested connection. The server marks the round failed because it used arrival time. This is a spec violation.

### AC-6.1B — Timing and Answer Validity Must Be Separated

**CBAR / Primitive Reference:** Story 6.1, `EXP-FBK-001`

**Given** the user answers within 3 seconds,  
**When** the system evaluates the round,  
**Then** `timing_pass` is computed independently from semantic validity,  
**And** the round can be "in time but invalid" without corrupting the timing result,  
**And** the score panel explains which dimension failed.

**FAILURE EXAMPLE:** The user says an unrelated filler phrase within 1.8 seconds. The system stores only `correct=false` with no distinction between lateness and invalidity, making coaching feedback meaningless. This is a spec violation.

### AC-6.1C — The Constraint Must Increase Focus, Not Panic

**CBAR / Primitive Reference:** Story 6.1, `EXP-FRC-006`

**Given** the coach is in an Alphabet Challenge round,  
**When** the timer is displayed,  
**Then** the UI frames the constraint as a focused drill or play-state mechanism,  
**And** the countdown treatment avoids panic-inducing alarm aesthetics that would increase performance anxiety,  
**And** the visual flow remains fast and clean enough to support instinctive retrieval.

**FAILURE EXAMPLE:** The app uses a flashing red siren timer with “FAIL IF YOU HESITATE” copy and an alarm sound on every round. The user freezes, not because the challenge is hard, but because the interface is hostile. This is a spec violation.

### AC-6.1D — Delayed Submission Must Preserve the Local Pass Result

**CBAR Mandate Enforced:** Phase2-M07  
**CBAR / Primitive Reference:** Phase2-M02

**Given** the user answered within 3 seconds on-device,  
**When** the round journal is transmitted after a network delay or reconnection,  
**Then** the stored local `timing_pass` remains intact,  
**And** the backend may only verify or flag the evidence, not rewrite the round as late because of transport delay.

**FAILURE EXAMPLE:** The user answers at 2.9 seconds while the webview is briefly offline. The payload is sent 12 seconds later and the backend rewrites the round to timeout because the network submission was delayed. This is a spec violation.

### AC-6.1E — Final Session Still Obeys Shared CORE Gates

**CBAR Mandate Enforced:** Phase2-M03 and Phase2-M04  
**Primitive Reference:** `EXP-FBK-001`

**Given** the Alphabet Challenge session is complete,  
**When** the user finalizes the capture,  
**Then** the app enters the shared background-upload and streaming-score path,  
**And** the final artifact/export verdict still depends on the shared quality gates,  
**And** quick recall performance alone does not auto-authorize export.

**FAILURE EXAMPLE:** The user responds quickly to every letter, but the audio is low quality and the final artifact fails transcript-quality checks. The system still auto-publishes because "timing was good." This is a spec violation.

## 9. Dependencies

### Internal

| Dependency | Type | Why Required |
|---|---|---|
| `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared spec dependency | Authoritative upload, streaming, scoring, and export lifecycle |
| `src/ccp/services/trait_scoring_engine.py` | Existing scoring service | Shared downstream scoring entry point |
| `src/ccp/services/signal_source_loader.py` | Existing dependency loader | Shared scoring dependency contract |
| `src/ccp/services/dpa_engine.py` | Existing visual service | Shared challenge/score palette resolution |
| `src/ccp/api/main.py` | Existing API composition | Router registration point |
| `src/ccp/api/sacred_audio.py` | Existing API pattern | Upload route style reference |
| `src/ccp/core/receipt_chain.py` | Existing audit infrastructure | Timing anomaly and finalize receipts |

### External

| Dependency | Type | Why Required |
|---|---|---|
| Telegram Mini App runtime | Client platform | Required launch surface for `react_alphabet` |
| Browser `performance.now()` / `Date.now()` | Client timing primitive | Required to implement Phase2-M07 |
| Browser local persistence | Client browser capability | Needed to preserve round journals across refresh or reconnection |
| Sovereign NIM stack | Deployment dependency | Required through CORE for scoring and transcript handling |

## 10. Testing Strategy

### Unit Tests

- `tests/unit/test_alphabet_round_timer.py::test_round_passes_when_answer_detected_at_2999ms`
- `tests/unit/test_alphabet_round_timer.py::test_round_fails_when_answer_detected_at_3001ms`
- `tests/unit/test_alphabet_round_timer.py::test_date_now_fallback_sets_clock_source`
- `tests/unit/test_alphabet_timing_verifier.py::test_server_verifier_never_uses_request_arrival_time`
- `tests/unit/test_alphabet_timing_verifier.py::test_suspicious_round_flagged_when_client_times_non_monotonic`

### Integration Tests

- `tests/integration/test_era3_fr05g_alphabet_api.py::test_session_endpoint_returns_react_alphabet_prompt_pack`
- `tests/integration/test_era3_fr05g_alphabet_api.py::test_finalize_preserves_local_timing_pass_under_network_delay`
- `tests/integration/test_era3_fr05g_alphabet_timing.py::test_client_side_timing_roundtrip_uses_monotonic_values`
- `tests/integration/test_era3_fr05g_alphabet_timing.py::test_timeout_round_stays_timeout_even_if_submission_arrives_quickly`

### Test Pattern Notes

- Follow the deterministic helper style from `test_ca11_fr15_dpa_engine.py` and `test_ca11_fr19_trivianar_engine.py`
- Prefer explicit fixtures for prompt packs and round journals
- Use a local `_run()` helper if async service calls are exercised
- Simulate latency by delaying payload submission, not by altering the client clock math

### Manual QA Checklist

1. Launch the mode with `startapp=react_alphabet` and verify the pack provides a category prompt and ordered letters.
2. Answer one round at 2.9 seconds and verify the client marks it `timing_pass=true`.
3. Artificially delay submission after a 2.9-second answer and verify the backend preserves the local pass.
4. Answer one round at 3.1 seconds and verify the client marks it late before any network submission occurs.
5. Disable `performance.now()` in a controlled test harness, fall back to `Date.now()`, and verify the session is marked with fallback clock metadata.
6. Force suspicious timestamp ordering and verify the backend flags the session instead of silently trusting corrupted timing data.
7. Finalize a completed challenge and verify the UI releases immediately while shared upload/scoring continues in the background.
8. Force a semantically invalid answer within 3 seconds and verify feedback distinguishes “in time” from “invalid term.”

---

## Appendix — Timing Fairness Rules

The implementation must preserve these fairness laws:

1. The user is judged on recall speed, not network speed.
2. Client timing evidence is authoritative for pass/fail, but not immune from anomaly flagging.
3. Verification is retrospective and diagnostic, not a hidden second timing judge.
4. A suspicious session may be quarantined or flagged for operator review, but it must not silently rewrite honest local timing outcomes based on transport delay.
5. The mode succeeds only if the coach experiences sharp pressure without feeling cheated by the machine.
