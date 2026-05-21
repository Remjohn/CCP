# Tech-Spec: FR-ERA3-05-CORE — Core Reaction Engine
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — CBAR-Hardened)
**Phase:** 2 — Conscious Reactions
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md §7

---

## Pre-Work Log

```
1. PROTOCOL LOADED:   §2.4 marks PRD-06's existing backend as `trivianar_engine_service.py` under Conscious Reactions,
                      while §2.2 confirms `POST /api/sacred-audio/upload` already exists in the FastAPI app.
2. PRD LOADED:        PRD-06 Brownfield §1.1 exact FR definition: "Shift the primary acquisition and content generation
                      event from classic, unstructured long-form interviews to highly constrained, async "Reactions"
                      triggered by trending topics." Brownfield §1.2 says the sovereign scoring stack exists already via
                      FR61/FR3, and §3 marks standalone Trivianar as obsolete.
3. EPIC LOADED:       Story 1.1 AC: "Given a high-charge topic is selected by SCRE, When the Mini App initializes,
                      Then the UI displays the `ReactionTopicBrief` payload including the `source_url` and plays the
                      `briefing_audio_path`."
4. CBAR AUDIT LOADED: Phase2-M01 (Ephemeral Decay Mandate), Phase2-M02 (Background Upload Rule), Phase2-M03
                      (Streaming Audio SLA), and Phase2-M04 (Earned Export Gate) confirmed. Hallucination purge also
                      confirms `EXP-TRB-*` and `EXP-SFR-*` references are invalid; use verified `EXP-TRS-*` and `EXP-SAF-*`.
5. PRIMITIVES LOADED: EXP-TRG-002 "Hook Cycle Velocity"; EXP-FRC-003 "The B=MAP Friction Audit";
                      EXP-FBK-001 "RIM Feedback Discipline"; EXP-TRS-004 "Attractive Things Work Better";
                      EXP-PRG-002 "First Major Win-State";
                      EXP-FRC-002 "Friction-Zero Ability"; EXP-TRG-005 "External to Internal Trigger Mapping";
                      EXP-SOC-005 "Recruit Your Allies"; EXP-SAF-004 "Richter Rescue".
6. BACKEND FILES READ:trait_scoring_engine.py — `def score_all_traits(self) -> list[ScoredTrait]`
                      dpa_engine.py — `async def resolve(self, coach_id: str, content_archetype: str, audience_mood_state: str = "", brand_hue_analysis: BrandHueAnalysis | None = None, override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None,) -> DPAResult`
                      trivianar_engine_service.py — `def score_response(self, question: TriviaQuestion, answer: str, elapsed_ms: int, game_mode: str = TriviaGameMode.COUNTDOWN.value, wager: int = 0, previous_responses: Optional[list[TriviaResponse]] = None,) -> ScoringResult`
7. TEST PATTERN:      `test_ca11_fr15_dpa_engine.py` + `test_ca11_fr19_trivianar_engine.py` read.
                      Pattern: local `_run()` helper for async, class-per-acceptance-criterion organization,
                      helper fixture builders (`_make_question`, constants, identity fixtures), direct SQL/constant assertions,
                      and no `pytest-asyncio`.
```

---

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|------|-------------|---------|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Current protocol, loaded 2026-05-11 | Mandatory spec-writing protocol, backend stack, API routes, DB schema, Phase execution order |
| 2 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | v6.0, 2026-05-06 | Source PRD for Conscious Reactions, brownfield inventory, obsolete Trivianar declaration |
| 3 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | 2026-05-08 | Epic acceptance criteria and Primitive Quality Constraints for Phase 2 |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | 2026-05-10 | Adversarial audit, canonical mandate resolutions, primitive hallucination corrections |
| 5 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | Codified | Verified TTL / velocity primitive for topic intake |
| 6 | `primitives/experience/friction_ability/EXP-FRC-003.yaml` | Codified | Verified friction-reduction primitive for recording and upload |
| 7 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified | Verified RIM feedback primitive for scoring SLA |
| 8 | `primitives/experience/trust_branding/EXP-TRS-001.yaml` | Codified | Verified premium authority aesthetic primitive for DPA surface quality |
| 9 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Codified | Verified progression/gating primitive for earned export |
| 10 | `primitives/experience/friction_ability/EXP-FRC-002.yaml` | Codified | Verified low-friction jury entry primitive |
| 11 | `primitives/experience/trigger_timing/EXP-TRG-005.yaml` | Codified | Verified escalation/earned action primitive for vote-then-react |
| 12 | `primitives/experience/social_referral/EXP-SOC-005.yaml` | Codified | Verified supervisor-role primitive |
| 13 | `primitives/experience/safe_failure_recovery/EXP-SAF-004.yaml` | Codified | Verified safe-failure primitive for Redemption Round |
| 14 | `src/ccp/services/trait_scoring_engine.py` | FR61 implementation | Existing biometric/leadership scoring engine to be consumed, not replaced |
| 15 | `src/ccp/services/signal_source_loader.py` | FR7 implementation | Existing `SignalBundle` dependency and missing-dependency gate for score derivation |
| 16 | `src/ccp/services/dpa_engine.py` | FR-CA11-15 | Existing DPA branding engine producing `DPAResult` / `ResolvedPalette` |
| 17 | `src/ccp/services/trivianar_engine_service.py` | FR-CA11-19 | Legacy reaction/gamification engine to be replaced and marked obsolete |
| 18 | `src/ccp/services/studio_block_service.py` | FR-CA11-16 | Existing WebSocket + chunk/recovery pattern reference for streaming and crash tolerance |
| 19 | `src/ccp/api/main.py` | 1.0.0 | FastAPI entrypoint for router registration and health extension |
| 20 | `src/ccp/api/sacred_audio.py` | Task 1.08 | Existing audio ingestion route and storage pattern for `sacred-audio` |
| 21 | `src/ccp/api/telegram_webhook.py` | Task 3.01 | Existing Telegram identity / callback ingress pattern |
| 22 | `src/ccp/core/circuit_breaker.py` | Task 3.08 | Graceful-degradation / fail-closed reference |
| 23 | `src/ccp/core/receipt_chain.py` | Task 1.06 | Immutable audit log mechanism for all state transitions |
| 24 | `src/ccp/models/ca11_models.py` | Current shared model layer | Existing `ResolvedPalette` and legacy Trivianar models |
| 25 | `src/ccp/scripts/setup_supabase.py` | Current schema bootstrap | Existing tables, storage buckets, and migration extension point |
| 26 | `requirements.txt` | Current | Verified runtime dependencies already present (`fastapi`, `pydantic`, `redis`, `supabase`, `httpx`) |
| 27 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Existing | Pytest style reference for async helper, constants, and DPA assertions |
| 28 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Existing | Pytest style reference for class-per-AC grouping and SQL/constant assertions |

---

## 2. Overview

### 2.1 Problem Statement — What breaks without this spec?

Without a shared Core Reaction Engine, every Conscious Reactions surface must independently solve topic intake, recording state, streaming score orchestration, DPA theming, social routing, and failure recovery. The result is architectural fragmentation and product breakage:
- topics become stale because no canonical TTL is enforced
- recording completion blocks on file upload, causing dropped takes on unstable mobile networks
- scoring misses the 3-second RIM latency mandate because audio is processed only after recording ends
- low-quality takes get exported as glossy CMF assets, destroying the platform's status economy
- audience voting, supervisor pairing, and redemption logic are bolted on differently per surface instead of enforced centrally
- legacy `trivianar_engine_service.py` semantics keep an obsolete synchronous mental model alive even though PRD-06 explicitly deprecates standalone Trivianar

### 2.2 Solution

This spec builds a new `CoreReactionEngine` as the Phase 2 shared backend for all Conscious Reactions Mini Apps. It replaces the legacy Trivianar service with a topic-intake orchestrator, recording-session manager, WebSocket chunk-stream scoring gateway, background-upload contract, DPA palette injection, audience-jury routing, supervisor notifications, and Redemption Round handling. It consumes the existing FR61 `TraitScoringEngine` and FR-CA11-15 `DPAEngine`, reads and stores full-fidelity recordings in the existing `sacred-audio` bucket, and exposes typed FastAPI endpoints and WebSocket contracts that all downstream reaction surfaces (`react_solo`, `react_debate`, `react_duel`, and Specs 8-14) consume instead of reinventing.

### 2.3 Scope

**In scope:**
- `ReactionTopicBrief` intake with 24-hour TTL enforcement and charge gating
- constrained recording-session lifecycle for Phase 2 reaction flows
- streaming 10-second audio chunk ingestion during active recording
- post-stop instant UI release with resilient background upload contract
- reaction scorecard assembly using FR61 trait scoring plus reaction-local acoustic metrics
- DPA palette resolution for topic intake and score/artifact rendering
- audience-jury voting, vote-then-react escalation, and supervisor pairing as CORE engine roles
- Redemption Round routing and private quarantine of failed takes
- earned CMF-export gate based on biometric threshold and anti-centroid checks
- replacement/deprecation plan for `trivianar_engine_service.py`
- typed Pydantic v2 models, new Supabase tables, receipt logging, and integration tests

**Out of scope:**
- implementation of the standalone Mini App UIs for `react_solo`, `react_debate`, `react_duel`, or Specs 8-14
- CMF rendering internals and final visual composition pipelines
- SCRE topic-generation logic itself
- synchronous WebRTC debate rooms
- payment, tier pricing, or upgrade checkout logic
- full Voice DNA extraction pipeline redesign
- generalized leaderboard/game-show logic from legacy Trivianar that is unrelated to reaction flows

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Payload | Source FR | What It Is |
|--------|--------------|-----------|------------|
| DEP-REA-001 | `ReactionTopicBrief` | Story 1.1 | The bounded intake payload containing TTL and DPA palette |
| DEP-REA-002 | `ReactionSessionRecord` | Story 1.2 | The recording session state, managing stream and upload status |
| DEP-REA-003 | `ReactionChunkEnvelope` | Story 1.3 | 10-second streaming audio chunk for sub-3s scoring |
| DEP-REA-004 | `ReactionBiometricSnapshot` | Story 1.3 | Pre-aggregated acoustic metrics before full transcription |
| DEP-REA-005 | `ReactionScoreCard` | Story 1.3 | Final evaluated evidence matrix mapped from FR61 |
| DEP-REA-006 | `ReactionArtifactRecord` | Story 2.1 | Canonical, version-controlled reaction result |
| DEP-REA-007 | `AudienceVoteRecord` | Story 3.1 | Stance vote cast by jury members |
| DEP-REA-008 | `VoteThenReactPrompt` | Story 3.2 | Escalation prompt tied to prior stance |
| DEP-REA-009 | `SupervisorAssignment` | Story 3.3 | Pairing contract emitting asymmetric progress summaries |
| DEP-REA-010 | `RedemptionRoundPayload` | Story 4.1 | Structured coaching cues and retry metadata |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `main.py` | `src/ccp/api/main.py` | **EXTENDED** — registers `core_reaction_router`, initializes health diagnostics, and exposes engine status |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | **PATTERN REFERENCE** — existing audio upload validation and storage conventions reused for reaction upload tickets and `sacred-audio` path structure |
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | **EXTENDED** — callback-query and stance-vote entry path for Audience Jury without forcing Mini App launch |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | **CONSUMED** — `TraitScoringEngine(score_bundle).score_all_traits()` produces the evidence-backed score substrate for reaction scorecards |
| `signal_source_loader.py` | `src/ccp/services/signal_source_loader.py` | **CONSUMED** — `SignalBundle` loading and missing-dependency semantics reused for coach baseline dependencies |
| `dpa_engine.py` | `src/ccp/services/dpa_engine.py` | **CONSUMED** — `DPAEngine.resolve()` injects `ResolvedPalette` into topic, scorecard, and artifact state |
| `studio_block_service.py` | `src/ccp/services/studio_block_service.py` | **PATTERN REFERENCE** — existing chunk interval, crash-recovery, and WebSocket URL conventions inform recording stream design |
| `trivianar_engine_service.py` | `src/ccp/services/trivianar_engine_service.py` | **REPLACED** — legacy engine is marked obsolete and reduced to compatibility wrapper or deprecation shim |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | **CONSUMED** — all topic issuance, session mutations, scoring, votes, retries, and export gates are immutably logged |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | **PATTERN REFERENCE** — fallback handling and explicit degraded-state behavior follow the same fail-closed philosophy |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | **CONSUMED** — imports `ResolvedPalette` and provides the legacy Trivianar model surface that must be decommissioned safely |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | **EXTENDED** — appends Phase 2 reaction tables and indexes into `SCHEMA_SQL` |

**Existing API routes extended or called:**
- `POST /api/sacred-audio/upload` — current upload contract and validation semantics
- `POST /api/telegram/webhook` — Audience Jury callbacks, supervisor invites, and vote-to-react hooks
- `GET /health` — extended with reaction engine readiness and degraded-mode flags

**Existing database tables consumed:**
- `receipt_chain` — immutable audit trail
- `asset_registry` — reaction artifact and audio asset registration
- `person_registry` — Telegram voter / coach / supervisor identity resolution
- `resolved_palettes` — DPA palette audit history

**New database tables created:**
- `reaction_topics`
- `reaction_sessions`
- `reaction_artifacts`
- `reaction_votes`
- `reaction_supervisors`
- `reaction_redemptions`
- `reaction_upload_sessions`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|-------------|------|--------|--------------------|
| `EXP-TRG-002` | Hook Cycle Velocity | trigger_timing | Every issued topic must carry a hard 24-hour TTL and countdown to preserve urgency and daily habit compression |
| `EXP-FRC-003` | The B=MAP Friction Audit | friction_ability | Stopping a recording must return control instantly; upload cannot block the user's flow |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Final reaction scorecard must arrive within 3 seconds of stop using pre-streamed chunks |
| `EXP-TRS-004` | Attractive Things Work Better | trust_branding | DPA surface cannot fall back to generic gray UI; palette + typography must act as a trust anchor |
| `EXP-PRG-002` | First Major Win-State | progression_replay | Glossy export is not a default right; state progression and reward gates must remain earned |
| `EXP-FRC-002` | Friction-Zero Ability | friction_ability | Audience Jury entry starts with one-tap inline voting and only then escalates to recording asks |
| `EXP-TRG-005` | External to Internal Trigger Mapping | trigger_timing | Vote-then-react copy must convert a tiny action into a meaningful next-step challenge tied to the user's chosen stance |
| `EXP-SOC-005` | Recruit Your Allies | social_referral | Supervisor pairing is a distinct role with asymmetric participation and persistent progress summaries |
| `EXP-SAF-004` | Richter Rescue | safe_failure_recovery | Failed takes stay private by default and immediately offer a structured retry via Redemption Round |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---------|----------|--------------|--------------------------|
| **The Ephemeral Decay Mandate** | Phase2-M01 | Story 1.1 | `ReactionTopicBrief` includes `expires_at`, `issued_at`, and `ttl_seconds`. Topic intake rejects expired payloads with HTTP 410 / `TOPIC_EXPIRED`. UI countdown is mandatory, and replaying a stale topic is banned unless the provocation engine explicitly issues a deeper-take variant with a fresh topic ID. |
| **The Background Upload Rule** | Phase2-M02 | Story 1.2 | Recording stop returns a `ReactionSessionRecord` immediately with `upload_status="pending_background"`, an upload ticket, and client retry instructions. Full-fidelity audio is stored by a resilient client worker with local cache / retry metadata; backend never blocks score reveal on full binary upload completion. |
| **The Streaming Audio SLA** | Phase2-M03 | Story 1.3 | `StreamingBiometricGateway` ingests 10-second chunks over WebSocket during recording. Prosody, transcript partials, and hedge counters are accumulated before stop so the final scorecard is assembled and delivered within 3 seconds after finalize. End-of-recording linear transcription of the full file is banned as the primary path. |
| **The Earned Export Gate** | Phase2-M04 | Story 2.1 | `ReactionArtifactRecord.export_eligible` becomes true only if biometric threshold, anti-centroid floor, and transcript quality gates pass. Failed takes are forced to `redemption_required` and cannot trigger CMF. Public share links and social routing are disabled for sub-threshold artifacts. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|---------------------|--------------|
| Replace `trivianar_engine_service.py` with `core_reaction_engine.py` plus a compatibility shim | PRD-06 explicitly marks standalone Trivianar obsolete; CORE must define the new async reaction architecture | Keep extending `trivianar_engine_service.py` directly | Preserves obsolete synchronous/game-show semantics and blurs the deprecation boundary |
| Separate streaming chunk ingress from full-fidelity background upload | Needed to satisfy both M02 and M03 simultaneously | Wait for full upload, then transcribe/score | Breaks 3-second scoring SLA and blocks the user on network physics |
| Reuse the private `sacred-audio` bucket with a reactions namespace | Existing storage path, privacy posture, and API semantics already exist | Introduce a new public reaction-audio bucket | Duplicates infrastructure and weakens privacy defaults for failed takes |
| Wrap FR61 scoring with a `ReactionScoreAdapter` instead of editing `TraitScoringEngine` | Protects the existing FR61 engine as a reusable dependency | Add reaction-specific branches into `TraitScoringEngine` | Couples two product surfaces and muddies FR61's existing trait-scoring contract |
| Audience Jury voting enters through Telegram webhook callbacks, not a mandatory Mini App | Story 3.1 requires zero-performance-pressure participation | Force every voter into the Mini App first | Adds avoidable friction and violates the low-friction jury-entry requirement |
| DPA palette is resolved at topic issue time and persisted to the artifact | Ensures stable visual identity across topic, scorecard, and export | Resolve palette separately at each surface render | Risks visual drift and inconsistent branding across the same reaction |
| Failed takes remain private until explicitly re-qualified | Safe failure is central to adoption and retention | Auto-publish everything, then let users delete later | Violates `EXP-SAF-004` and makes the platform feel punishing rather than coach-like |

---

## 4. Implementation Plan

### Phase 1: Models, Enums, and Storage Schema (Tasks 1-4)

- [ ] **Task 1:** Create `src/ccp/models/reaction_engine_models.py` with all Phase 2 reaction enums, thresholds, SQL constants, and Pydantic v2 models.
- [ ] **Task 2:** Define `REACTION_TOPICS_SQL`, `REACTION_SESSIONS_SQL`, `REACTION_ARTIFACTS_SQL`, `REACTION_VOTES_SQL`, `REACTION_SUPERVISORS_SQL`, `REACTION_REDEMPTIONS_SQL`, and `REACTION_UPLOAD_SESSIONS_SQL` in `src/ccp/models/reaction_engine_models.py`.
- [ ] **Task 3:** Extend `src/ccp/scripts/setup_supabase.py` to append the new reaction tables and indexes to `SCHEMA_SQL`.
- [ ] **Task 4:** Export the new reaction models from `src/ccp/models/__init__.py` only if package-level export maintenance is required by the current repo pattern.

### Phase 2: Core Orchestration Service (Tasks 5-9)

- [ ] **Task 5:** Create `src/ccp/services/core_reaction_engine.py` with `TopicIntakeCoordinator`, `ReactionSessionManager`, `StreamingBiometricGateway`, `ReactionScoreAdapter`, `ReactionSocialRouter`, `RedemptionRoundCoordinator`, and `CoreReactionEngine`.
- [ ] **Task 6:** Implement `TopicIntakeCoordinator.next_topic()` in `src/ccp/services/core_reaction_engine.py` to enforce `charge_level > 0.7`, attach TTL, call `DPAEngine.resolve()`, and inject the specific `target_primitives_meaning` and `viral_threshold_multiplier` from the SCRE topic schema.
- [ ] **Task 7:** Implement WebSocket chunk accumulation in `StreamingBiometricGateway` using 10-second envelopes and pre-stop score aggregation.
- [ ] **Task 8:** Implement `ReactionScoreAdapter` so it consumes `SignalBundle` + `TraitScoringEngine.score_all_traits()` and maps the result into `ReactionBiometricSnapshot` using exact derivations: `conviction_score` and `pacing_score` copy directly from base traits; `hedge_frequency` aggregates exact match counts from transcripts; `damage_index` calculates from semantic hesitation markers; and `anti_centroid_charge` derives from the vector distance of the transcript against baseline CMM data. Additionally, generate `compounding_forecast` and `feedback_sentence` using the `TraitScoringEngine`'s secondary diagnostic hooks. Map this snapshot into `ReactionScoreCard`.
- [ ] **Task 9:** Implement `CoreReactionEngine.finalize_reaction()` so it applies the earned export gate, triggers redemption for failures, and writes receipt entries for every state mutation.

### Phase 3: Upload, Social Routing, and Role Features (Tasks 10-13)

- [ ] **Task 10:** Add background-upload ticket issuance and retry metadata in `src/ccp/services/core_reaction_engine.py`, reusing `sacred-audio` naming and size-validation rules.
- [ ] **Task 11:** Extend `src/ccp/api/telegram_webhook.py` to parse Audience Jury vote callbacks, vote-then-react stance payloads, and supervisor-link actions.
- [ ] **Task 12:** Implement `ReactionSocialRouter.register_vote()`, `build_vote_then_react_prompt()`, and `assign_supervisor()` in `src/ccp/services/core_reaction_engine.py`, enforcing mandatory Receipt Chain Guard writes for every vote cast and supervisor assigned to preserve the immutable audit trail.
- [ ] **Task 13:** Implement `RedemptionRoundCoordinator.build_retry()` so every `redemption_required` artifact emits exactly two cues plus a retry deadline.

### Phase 4: API Surface and App Wiring (Tasks 14-17)

- [ ] **Task 14:** Create `src/ccp/api/core_reaction_api.py` with `GET /api/reactions/topics/next`, `POST /api/reactions/sessions/start`, `WS /api/reactions/sessions/{session_id}/stream`, `POST /api/reactions/sessions/{session_id}/finalize`, and `GET /api/reactions/artifacts/{artifact_id}`.
- [ ] **Task 15:** Add `POST /api/reactions/artifacts/{artifact_id}/vote`, `POST /api/reactions/artifacts/{artifact_id}/vote-then-react`, `POST /api/reactions/artifacts/{artifact_id}/supervisor`, and `POST /api/reactions/artifacts/{artifact_id}/redemption`.
- [ ] **Task 16:** Modify `src/ccp/api/main.py` to register `core_reaction_router` and extend `/health` with engine readiness, degraded-mode, and queue counters.
- [ ] **Task 17:** Create a `TrivianarCompatibilityShim` inside `src/ccp/services/trivianar_engine_service.py` that marks the service obsolete and forwards only explicitly supported transitional calls.

### Phase 5: Verification, Deprecation, and Test Coverage (Tasks 18-21)

- [ ] **Task 18:** Create `tests/integration/test_era3_fr05_core_reaction_engine.py` covering topic TTL, upload semantics, scorecard assembly, DPA injection, and export gating.
- [ ] **Task 19:** Create `tests/integration/test_era3_fr05_core_reaction_api.py` covering HTTP/WebSocket contracts, health state, and expired-topic rejection.
- [ ] **Task 20:** Create `tests/integration/test_era3_fr05_core_reaction_social_routing.py` covering Audience Jury, vote-then-react copy, supervisor notifications, and redemption privacy.
- [ ] **Task 21:** Mark `docs/architecture/FR-CA11-19_Interactive_Trivianar_Engine_Tech_Spec.md` obsolete in the architecture inventory and remove any new product references that still describe Trivianar as an active standalone surface.

---

## 5. Primary Output Schema

```python
# src/ccp/models/reaction_engine_models.py
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

from src.ccp.models.ca11_models import ResolvedPalette
from src.ccp.models.leadership_scorecard_models import ScoredTrait


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REACTION_TOPIC_TTL_HOURS: int = 24
DEFAULT_RECORDING_LIMIT_SECONDS: int = 300
STREAM_CHUNK_SECONDS: int = 10
SCORING_SLA_SECONDS: int = 3
ANTI_CENTROID_MIN: float = 0.60
CMF_PASS_THRESHOLD: float = 70.0
MIN_AUDIO_SECONDS: int = 15
REDEMPTION_CUE_COUNT: int = 2

REACTION_TOPICS_SQL = """
CREATE TABLE IF NOT EXISTS reaction_topics (
    topic_id                    TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    source_url                  TEXT NOT NULL,
    charge_level                REAL NOT NULL,
    briefing_audio_path         TEXT NOT NULL,
    target_primitives_meaning   JSONB NOT NULL DEFAULT '[]',
    target_primitives_experience JSONB NOT NULL DEFAULT '[]',
    time_constraint_seconds     INTEGER NOT NULL DEFAULT 300,
    debate_enabled              BOOLEAN NOT NULL DEFAULT TRUE,
    viral_threshold_multiplier  REAL NOT NULL DEFAULT 1.0,
    issued_at                   TIMESTAMPTZ NOT NULL,
    expires_at                  TIMESTAMPTZ NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

REACTION_SESSIONS_SQL = """
CREATE TABLE IF NOT EXISTS reaction_sessions (
    session_id                  TEXT PRIMARY KEY,
    topic_id                    TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    mode                        TEXT NOT NULL,
    started_at                  TIMESTAMPTZ NOT NULL,
    stopped_at                  TIMESTAMPTZ,
    time_limit_seconds          INTEGER NOT NULL DEFAULT 300,
    stream_status               TEXT NOT NULL DEFAULT 'pending',
    upload_status               TEXT NOT NULL DEFAULT 'pending_background',
    chunk_count                 INTEGER NOT NULL DEFAULT 0,
    upload_ticket               TEXT NOT NULL DEFAULT '',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

REACTION_ARTIFACTS_SQL = """
CREATE TABLE IF NOT EXISTS reaction_artifacts (
    artifact_id                 TEXT PRIMARY KEY,
    session_id                  TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    topic_id                    TEXT NOT NULL,
    raw_audio_path              TEXT NOT NULL,
    transcript                  TEXT NOT NULL DEFAULT '',
    conviction_score            REAL NOT NULL DEFAULT 0,
    pacing_score                REAL NOT NULL DEFAULT 0,
    hedge_frequency             INTEGER NOT NULL DEFAULT 0,
    damage_index                REAL NOT NULL DEFAULT 0,
    impact_score                REAL NOT NULL DEFAULT 0,
    anti_centroid_charge        REAL NOT NULL DEFAULT 0,
    artifact_status             TEXT NOT NULL,
    visibility                  TEXT NOT NULL DEFAULT 'private',
    export_eligible             BOOLEAN NOT NULL DEFAULT FALSE,
    cmf_export_ids              JSONB NOT NULL DEFAULT '[]',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

REACTION_VOTES_SQL = """
CREATE TABLE IF NOT EXISTS reaction_votes (
    vote_id                     TEXT PRIMARY KEY,
    artifact_id                 TEXT NOT NULL,
    voter_telegram_user_id      BIGINT NOT NULL,
    selected_side               TEXT NOT NULL,
    prompt_reaction_after_vote  BOOLEAN NOT NULL DEFAULT TRUE,
    voted_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

REACTION_SUPERVISORS_SQL = """
CREATE TABLE IF NOT EXISTS reaction_supervisors (
    assignment_id               TEXT PRIMARY KEY,
    artifact_id                 TEXT NOT NULL,
    coach_telegram_user_id      BIGINT NOT NULL,
    supervisor_telegram_user_id BIGINT NOT NULL,
    active                      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

REACTION_REDEMPTIONS_SQL = """
CREATE TABLE IF NOT EXISTS reaction_redemptions (
    redemption_id               TEXT PRIMARY KEY,
    artifact_id                 TEXT NOT NULL,
    retry_session_id            TEXT NOT NULL DEFAULT '',
    coaching_cues               JSONB NOT NULL DEFAULT '[]',
    retry_deadline              TIMESTAMPTZ NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

REACTION_UPLOAD_SESSIONS_SQL = """
CREATE TABLE IF NOT EXISTS reaction_upload_sessions (
    upload_ticket               TEXT PRIMARY KEY,
    session_id                  TEXT NOT NULL,
    artifact_id                 TEXT NOT NULL,
    mime_type                   TEXT NOT NULL,
    total_bytes                 BIGINT NOT NULL DEFAULT 0,
    uploaded_bytes              BIGINT NOT NULL DEFAULT 0,
    upload_status               TEXT NOT NULL DEFAULT 'pending_background',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at                TIMESTAMPTZ
);
"""


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ReactionMode(str, Enum):
    SOLO = "react_solo"
    DEBATE = "react_debate"
    DUEL = "react_duel"


class ReactionJourneyPhase(str, Enum):
    DISCOVER = "discover"
    ONBOARD = "onboard"
    IMMERSE = "immerse"
    MASTER = "master"
    REPLAY = "replay"


class StreamStatus(str, Enum):
    PENDING = "pending"
    STREAMING = "streaming"
    FINALIZING = "finalizing"
    COMPLETE = "complete"
    DEGRADED = "degraded"


class UploadStatus(str, Enum):
    PENDING_BACKGROUND = "pending_background"
    UPLOADING = "uploading"
    STORED = "stored"
    FAILED_RETRYABLE = "failed_retryable"


class ArtifactStatus(str, Enum):
    PROCESSING = "processing"
    SCORED = "scored"
    REJECTED_SLOP = "rejected_slop"
    REDEMPTION_REQUIRED = "redemption_required"
    DEPLOYED_TO_CMF = "deployed_to_cmf"


class ArtifactVisibility(str, Enum):
    PRIVATE = "private"
    JURY_ELIGIBLE = "jury_eligible"
    PUBLIC = "public"


class AudienceVoteChoice(str, Enum):
    FOR = "for"
    AGAINST = "against"
    STRONGER_TAKE = "stronger_take"


# ---------------------------------------------------------------------------
# Topic / Session Models
# ---------------------------------------------------------------------------

class ReactionTopicBrief(BaseModel):
    topic_id: str = Field(min_length=1)
    source_url: HttpUrl
    charge_level: float = Field(ge=0.0, le=1.0)
    briefing_audio_path: str = Field(min_length=1)
    target_primitives_meaning: list[str] = Field(default_factory=list)
    target_primitives_experience: list[str] = Field(default_factory=list)
    time_constraint_seconds: int = Field(default=DEFAULT_RECORDING_LIMIT_SECONDS, ge=1)
    debate_enabled: bool = Field(default=True)
    viral_threshold_multiplier: float = Field(default=1.0, ge=0.1)
    issued_at: str = Field(min_length=1)
    expires_at: str = Field(min_length=1)
    palette: ResolvedPalette


class ReactionSessionCreateRequest(BaseModel):
    coach_id: str = Field(min_length=1)
    coach_acronym: str = Field(min_length=3, max_length=3)
    topic_id: str = Field(min_length=1)
    mode: ReactionMode
    client_session_id: str = Field(min_length=1)
    journey_phase: ReactionJourneyPhase = Field(default=ReactionJourneyPhase.ONBOARD)


class ReactionSessionRecord(BaseModel):
    session_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    topic_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    mode: ReactionMode
    started_at: str = Field(min_length=1)
    stopped_at: str = Field(default="")
    time_limit_seconds: int = Field(default=DEFAULT_RECORDING_LIMIT_SECONDS, ge=1)
    stream_status: StreamStatus = Field(default=StreamStatus.PENDING)
    upload_status: UploadStatus = Field(default=UploadStatus.PENDING_BACKGROUND)
    chunk_count: int = Field(default=0, ge=0)
    upload_ticket: str = Field(default="")
    visibility: ArtifactVisibility = Field(default=ArtifactVisibility.PRIVATE)


class ReactionChunkEnvelope(BaseModel):
    session_id: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    started_at_ms: int = Field(ge=0)
    duration_seconds: int = Field(default=STREAM_CHUNK_SECONDS, ge=1)
    mime_type: Literal["audio/webm", "audio/ogg", "audio/wav"]
    sample_rate_hz: int = Field(ge=8000)
    byte_count: int = Field(ge=0)
    sequence_hash: str = Field(min_length=1)


# ---------------------------------------------------------------------------
# Score / Artifact Models
# ---------------------------------------------------------------------------

class ReactionBiometricSnapshot(BaseModel):
    conviction_score: float = Field(ge=0.0, le=100.0)
    pacing_score: float = Field(ge=0.0, le=100.0)
    hedge_frequency: int = Field(ge=0)
    damage_index: float = Field(ge=0.0, le=100.0)
    impact_score: float = Field(ge=0.0, le=100.0)
    anti_centroid_charge: float = Field(ge=0.0, le=1.0)
    delivered_within_sla: bool = Field(default=True)


class ReactionScoreCard(BaseModel):
    artifact_id: str = Field(min_length=1)
    biometric_snapshot: ReactionBiometricSnapshot
    scored_traits: list[ScoredTrait] = Field(default_factory=list)
    compounding_forecast: str = Field(min_length=1)
    feedback_sentence: str = Field(min_length=1)
    detected_meaning_primitives: list[str] = Field(default_factory=list)
    detected_experience_primitives: list[str] = Field(default_factory=list)
    delivered_at: str = Field(min_length=1)


class ReactionArtifactRecord(BaseModel):
    artifact_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    topic_id: str = Field(min_length=1)
    raw_audio_path: str = Field(min_length=1)
    transcript: str = Field(default="")
    scorecard: ReactionScoreCard
    status: ArtifactStatus = Field(default=ArtifactStatus.PROCESSING)
    visibility: ArtifactVisibility = Field(default=ArtifactVisibility.PRIVATE)
    export_eligible: bool = Field(default=False)
    cmf_export_ids: list[str] = Field(default_factory=list)
    palette: ResolvedPalette


# ---------------------------------------------------------------------------
# Social Routing / Recovery Models
# ---------------------------------------------------------------------------

class AudienceVoteRecord(BaseModel):
    vote_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    voter_telegram_user_id: int = Field(gt=0)
    selected_side: AudienceVoteChoice
    prompt_reaction_after_vote: bool = Field(default=True)
    voted_at: str = Field(min_length=1)


class VoteThenReactPrompt(BaseModel):
    artifact_id: str = Field(min_length=1)
    voter_telegram_user_id: int = Field(gt=0)
    selected_side: AudienceVoteChoice
    prompt_copy: str = Field(min_length=1)
    expires_at: str = Field(min_length=1)


class SupervisorAssignment(BaseModel):
    assignment_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    coach_telegram_user_id: int = Field(gt=0)
    supervisor_telegram_user_id: int = Field(gt=0)
    active: bool = Field(default=True)
    summary_text: str = Field(min_length=1)


class RedemptionRoundPayload(BaseModel):
    artifact_id: str = Field(min_length=1)
    failure_reasons: list[str] = Field(default_factory=list, min_length=1)
    coaching_cues: list[str] = Field(default_factory=list, min_length=REDEMPTION_CUE_COUNT, max_length=REDEMPTION_CUE_COUNT)
    retry_allowed: bool = Field(default=True)
    retry_deadline: str = Field(min_length=1)

    @field_validator("coaching_cues")
    @classmethod
    def validate_cues(cls, value: list[str]) -> list[str]:
        if len(value) != REDEMPTION_CUE_COUNT:
            raise ValueError("Redemption Round must emit exactly 2 coaching cues.")
        return value


class CoreReactionResult(BaseModel):
    success: bool = Field(default=True)
    topic: ReactionTopicBrief | None = Field(default=None)
    session: ReactionSessionRecord | None = Field(default=None)
    artifact: ReactionArtifactRecord | None = Field(default=None)
    vote_prompt: VoteThenReactPrompt | None = Field(default=None)
    redemption: RedemptionRoundPayload | None = Field(default=None)
    error_code: str = Field(default="")
    error_detail: str = Field(default="")
```

---

## 6. Backward Compatibility Fallback

Following the `circuit_breaker.py` fail-closed pattern:

| Failure Mode | Degradation Strategy |
|-------------|----------------------|
| **WebSocket streaming unsupported or disconnected mid-recording** | The session is marked `stream_status=degraded`, full-fidelity upload still proceeds, and the artifact remains private until delayed scoring completes. The user may still finish the take, but public export and social routing are blocked because M03 was not satisfied. |
| **Background upload interrupted by mobile OS / connectivity loss** | The client keeps the local chunk cache and upload ticket, and the backend leaves the session in `upload_status=failed_retryable`. No artifact is deleted; retry resumes against the same upload ticket. |
| **FR61 signal dependencies missing (`coach_soul.json`, `ttt_baseline.json`, `tribe_soul.json`)** | The engine catches `MissingDependencyError`, returns `error_code="CANNOT_SCORE_MISSING_DEPENDENCIES"`, emits a receipt entry, and prevents CMF export. The coach may still receive a limited placeholder status, but not a public scorecard. |
| **DPA palette resolution fails** | The engine falls back to a safe default palette profile and logs the degraded state. Recording and scoring continue, but `brand_degraded=true` is surfaced in health and receipt metadata. |
| **CMF export target unavailable** | A passing take remains `export_eligible=true` but `status=scored` until the downstream CMF queue is healthy. The user receives the scorecard immediately; glossy export is retried asynchronously. |
| **Legacy code still imports `TrivianarEngine`** | `trivianar_engine_service.py` remains as a transitional shim that exposes a deprecation error for synchronous/game-show-only paths and forwards only explicitly mapped shared helpers during one migration window. |

---

## 7. Tasks

### Sprint 1: Schema and Data Contracts
- [ ] Create `src/ccp/models/reaction_engine_models.py`
- [ ] Add reaction SQL DDL constants in `src/ccp/models/reaction_engine_models.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with reaction table migrations
- [ ] Add model exports if package-level exports are required

### Sprint 2: Core Engine
- [ ] Create `TopicIntakeCoordinator` in `src/ccp/services/core_reaction_engine.py`
- [ ] Create `ReactionSessionManager` in `src/ccp/services/core_reaction_engine.py`
- [ ] Create `StreamingBiometricGateway` in `src/ccp/services/core_reaction_engine.py`
- [ ] Create `ReactionScoreAdapter` in `src/ccp/services/core_reaction_engine.py`
- [ ] Create `CoreReactionEngine` orchestrator in `src/ccp/services/core_reaction_engine.py`

### Sprint 3: Roles and Recovery
- [ ] Create `ReactionSocialRouter` in `src/ccp/services/core_reaction_engine.py`
- [ ] Implement Audience Jury vote persistence and callback handling
- [ ] Implement Vote Then React prompt generation tied to prior stance
- [ ] Implement supervisor assignment and summary-notification payloads
- [ ] Implement `RedemptionRoundCoordinator` with private quarantine and retry state

### Sprint 4: API and App Wiring
- [ ] Create `src/ccp/api/core_reaction_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/api/telegram_webhook.py` for jury callbacks and supervisor actions
- [ ] Extend `/health` in `src/ccp/api/main.py` with reaction-engine status
- [ ] Add upload-ticket issuance and finalize routes for the background upload contract

### Sprint 5: Replacement and Test Coverage
- [ ] Convert `src/ccp/services/trivianar_engine_service.py` into an obsolete compatibility shim
- [ ] Add `tests/integration/test_era3_fr05_core_reaction_engine.py`
- [ ] Add `tests/integration/test_era3_fr05_core_reaction_api.py`
- [ ] Add `tests/integration/test_era3_fr05_core_reaction_social_routing.py`
- [ ] Mark the legacy Trivianar architecture doc obsolete in the documentation inventory

---

## 8. Acceptance Criteria

### AC-1.1: Context-Aware Topic Intake with TTL

**CBAR Mandate Enforced:** Phase2-M01 — The Ephemeral Decay Mandate

**Given** a high-charge topic is selected by SCRE,
**When** the Mini App requests the next topic from the CORE engine,
**Then** the engine returns a `ReactionTopicBrief` containing `source_url`, `briefing_audio_path`, `issued_at`, and `expires_at`,
**And** the topic expires exactly 24 hours after issue,
**And** expired topics are rejected and may not be recorded against.

**FAILURE EXAMPLE:** A coach taps a reaction prompt three days after the topic peaked and still receives the same brief without a countdown or expiry block. The topic no longer feels culturally alive, so the experience degrades into an administrative chore. This is a spec violation.

**Measurable pass condition:** `expires_at - issued_at == 24h` for all issued topics, and requests for expired topic IDs return HTTP 410 / `TOPIC_EXPIRED`.

---

### AC-1.2: Constrained Recording with Instant UI Return

**CBAR Mandate Enforced:** Phase2-M02 — The Background Upload Rule

**Given** the user finishes a constrained recording,
**When** they hit stop,
**Then** the API immediately returns a `ReactionSessionRecord` with `upload_status="pending_background"` and an upload ticket,
**And** the client enters scoring state without waiting for the full audio file to upload,
**And** upload retry metadata is preserved if the network fails.

**FAILURE EXAMPLE:** The user taps stop and the Mini App stalls on a blocking 20MB upload spinner for 14 seconds. The OS suspends Telegram, the upload dies, and the take is lost. This is a spec violation.

**Measurable pass condition:** API finalize acknowledgment returns within 500ms of stop, while the full-fidelity upload may continue asynchronously under the same `upload_ticket`.

---

### AC-1.3: Streaming Scorecard Delivery in Under 3 Seconds

**CBAR Mandate Enforced:** Phase2-M03 — The Streaming Audio SLA

**Given** a reaction session is actively recording,
**When** the client streams 10-second audio chunks during the session and the user finalizes,
**Then** the engine assembles the final `ReactionScoreCard` using the precomputed chunk state,
**And** the complete scorecard is delivered within 3 seconds of stop,
**And** full-file post-stop transcription is not the primary scoring path.

**FAILURE EXAMPLE:** The system waits until the end of a 300-second recording to begin transcription and scoring, causing the coach to wait 35 seconds after stop. The emotional context is gone and the feedback no longer feels immediate. This is a spec violation.

**Measurable pass condition:** `scorecard.delivered_at - session.stopped_at <= 3000ms` for P95 reaction sessions with streaming enabled.

---

### AC-1.4: Dynamic Whitelabel DPA Injection

**CBAR Mandate Enforced:** None directly

**Given** a coach opens a CORE reaction topic,
**When** the topic envelope is generated,
**Then** the engine calls `DPAEngine.resolve()` and attaches a `ResolvedPalette` to the topic and artifact state,
**And** the palette remains stable across topic, scorecard, and export surfaces,
**And** the fallback path is explicitly logged if branding resolution degrades.

**FAILURE EXAMPLE:** The topic brief renders in a generic gray theme, the scorecard renders in a different palette, and the final artifact uses a third visual style. The coach experiences the product as unbranded SaaS instead of a premium authority tool. This is a spec violation.

**Measurable pass condition:** the same `ResolvedPalette` identifier or equivalent immutable palette payload is present on the topic brief, artifact record, and scorecard response for a single reaction.

---

### AC-2.1: Earned Export Gate for CMF Routing

**CBAR Mandate Enforced:** Phase2-M04 — The Earned Export Gate

**Given** a scored reaction artifact is ready for post-processing,
**When** the engine evaluates export eligibility,
**Then** it triggers CMF only if biometric thresholds and anti-centroid minimums pass,
**And** failed takes are marked `redemption_required`,
**And** sub-threshold takes remain private and unshareable.

**FAILURE EXAMPLE:** A weak, hedged take scores badly but still receives a premium CMF export and public share link. The reward feels unearned and collapses the prestige of the system. This is a spec violation.

**Measurable pass condition:** `export_eligible == true` only when `impact_score >= 70`, `conviction_score >= 70`, and `anti_centroid_charge >= 0.60`; otherwise `status == redemption_required` and `cmf_export_ids == []`.

---

### AC-3.1: Audience Jury Voting Without Performance Friction

**CBAR Mandate Enforced:** None directly

**Given** an audience member receives a shared debate or duel artifact,
**When** they listen and tap a Telegram inline vote button,
**Then** the vote is registered without requiring a Mini App launch or account registration,
**And** the artifact records the vote against the correct side and voter ID.

**FAILURE EXAMPLE:** The user taps a vote button and is forced to open a Mini App, authenticate, and navigate additional UI before the vote counts. Low-friction social entry is destroyed. This is a spec violation.

**Measurable pass condition:** a vote callback produces a persisted `AudienceVoteRecord` in one webhook round-trip with no Mini App dependency and no manual registration step.

---

### AC-3.2: Vote Then React Escalation Tied to Chosen Stance

**CBAR Mandate Enforced:** None directly

**Given** a voter has just cast a stance vote,
**When** the CORE engine builds the escalation prompt,
**Then** the prompt copy explicitly references the side they chose,
**And** the prompt invites recording without context switching into generic onboarding language.

**FAILURE EXAMPLE:** After voting, the user sees a cold modal saying only "Record your own take." It does not reference who they backed or why they are being asked, so it feels like spam rather than a natural progression. This is a spec violation.

**Measurable pass condition:** `VoteThenReactPrompt.prompt_copy` includes a stance-tethered reference every time, such as "You voted for X. Hit record to tell the jury why you're right."

---

### AC-3.3: Supervisor Accountability Pairing

**CBAR Mandate Enforced:** None directly

**Given** a coach assigns a supervisor or friend witness,
**When** the coach records a new scored reaction,
**Then** the engine generates a summary payload for the paired supervisor,
**And** the summary emphasizes change over time rather than raw public humiliation,
**And** the supervisor role remains asymmetric from a jury role.

**FAILURE EXAMPLE:** A supervisor receives the same public artifact everyone else sees, without contextual progress framing or role-specific summary. The support role collapses into generic spectatorship. This is a spec violation.

**Measurable pass condition:** each active `SupervisorAssignment` results in a supervisor-specific summary payload containing at least one improvement delta and no public-share URL as the sole payload.

---

### AC-4.1: Redemption Round with Private Quarantine

**CBAR Mandate Enforced:** None directly

**Given** a reaction fails the biometric or anti-centroid gates,
**When** the user views the score result,
**Then** the artifact is kept private by default,
**And** the engine returns exactly 2 coaching cues and a retry action,
**And** no public share or CMF route is exposed until a successful retry passes.

**FAILURE EXAMPLE:** The coach receives a failing score and the low-quality artifact is still visible to peers or is routed to export. The system feels punitive and unsafe, which discourages practice. This is a spec violation.

**Measurable pass condition:** all failed artifacts have `visibility == private`, `status == redemption_required`, `len(coaching_cues) == 2`, and `cmf_export_ids == []`.

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|-------------|-----------------|------------------------------|
| `src/ccp/api/main.py` | Code extension | Router registration, lifecycle bootstrap, and health diagnostics |
| `src/ccp/api/sacred_audio.py` | Pattern reference | Upload validation, file-size checks, and private-audio storage conventions |
| `src/ccp/api/telegram_webhook.py` | Code extension | Inline Audience Jury callbacks and vote-triggered role routing |
| `src/ccp/services/trait_scoring_engine.py` | Runtime consumption | Existing FR61 scoring substrate via `score_all_traits()` |
| `src/ccp/services/signal_source_loader.py` | Runtime consumption | `SignalBundle` loading and missing-dependency error semantics |
| `src/ccp/services/dpa_engine.py` | Runtime consumption | `DPAEngine.resolve()` for whitelabel branding state |
| `src/ccp/services/studio_block_service.py` | Pattern reference | WebSocket, chunk, and crash-recovery conventions |
| `src/ccp/services/trivianar_engine_service.py` | Replacement target | Transitional obsolete wrapper during migration |
| `src/ccp/core/receipt_chain.py` | Runtime consumption | Immutable logging for every CORE-engine transition |
| `src/ccp/core/circuit_breaker.py` | Pattern reference | Degraded-state behavior and explicit fail-closed semantics |
| `src/ccp/models/ca11_models.py` | Model dependency | `ResolvedPalette` and legacy Trivianar model compatibility |
| `src/ccp/scripts/setup_supabase.py` | Code extension | Canonical migration entrypoint for reaction tables |
| `PRD-06 Conscious Reactions` | Requirements dependency | Canonical product loop, brownfield obsolete inventory, and data contracts |
| `FR61 / FR3 scoring architecture` | Runtime dependency | Existing voice/trait scoring stack the CORE engine wraps rather than replaces |

### External

| API/Library | Version | Purpose |
|------------|---------|---------|
| `fastapi` | `>=0.110.0` | HTTP + WebSocket API surface |
| `pydantic` | `>=2.6.0` | Typed contracts and validation |
| `redis` | `>=5.0.0` | Optional transient streaming/session state and retry-safe queue metadata |
| `supabase` | `>=2.3.0` | PostgreSQL tables and `sacred-audio` storage integration |
| `httpx` | `>=0.27.0` | Telegram Bot API calls and internal async HTTP operations |
| `python-multipart` | `>=0.0.9` | Upload handling for reaction finalize/upload flows |
| Telegram Bot API / Telegram Web App API | Current platform dependency | Jury callbacks, Mini App launch context, and inline participation |
| Browser `MediaRecorder` + IndexedDB | Modern mobile browser capability | 10-second chunk capture and resilient background upload worker |
| Sovereign NIM stack | Deployment-managed | Streaming STT and semantic scoring during active recording |

---

## 10. Testing Strategy

### Unit Tests

**File:** `tests/integration/test_era3_fr05_core_reaction_engine.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestTopicIntakeCoordinator:
    def test_ac11_topic_contains_expires_at_and_source_url()
    def test_expired_topic_returns_topic_expired()
    def test_charge_level_below_threshold_rejected()
    def test_dpa_palette_attached_to_topic()


class TestReactionSessionManager:
    def test_ac12_finalize_returns_upload_ticket_immediately()
    def test_time_limit_defaults_to_300_seconds()
    def test_retryable_upload_failure_preserves_ticket()


class TestReactionScoreAdapter:
    def test_ac13_scorecard_delivered_within_sla_flag()
    def test_trait_scoring_engine_results_mapped_into_scorecard()
    def test_missing_signal_bundle_raises_cannot_score_dependencies()


class TestExportGate:
    def test_ac21_threshold_pass_sets_export_eligible()
    def test_subthreshold_take_routes_to_redemption_required()
    def test_failed_take_has_no_cmf_exports()
```

**File:** `tests/integration/test_era3_fr05_core_reaction_social_routing.py`

```python
class TestAudienceJuryRouting:
    def test_ac31_vote_persists_without_mini_app()
    def test_duplicate_vote_same_user_rejected()


class TestVoteThenReact:
    def test_ac32_prompt_copy_references_selected_side()
    def test_prompt_has_expiry()


class TestSupervisorPairing:
    def test_ac33_supervisor_summary_contains_progress_delta()
    def test_inactive_supervisor_receives_no_summary()


class TestRedemptionRound:
    def test_ac41_exactly_two_coaching_cues_emitted()
    def test_failed_take_visibility_private()
```

**File:** `tests/integration/test_era3_fr05_core_reaction_api.py`

```python
class TestCoreReactionAPI:
    def test_get_next_topic_returns_typed_topic_brief()
    def test_finalize_returns_session_record_and_upload_ticket()
    def test_health_reports_degraded_streaming_state()
    def test_expired_topic_returns_410()
    def test_websocket_chunk_updates_session_chunk_count()
```

### Integration Tests

Modeled on `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`:
- use a local `_run()` helper instead of `pytest-asyncio`
- organize tests by acceptance-criterion class
- create small fixture builders for topic briefs, sessions, chunks, and vote payloads
- assert SQL strings, constants, and receipt outputs directly

**File:** `tests/integration/test_era3_fr05_core_reaction_engine.py`

```python
class TestCoreLoopFoundation:
    def test_ac11_topic_ttl_is_24_hours(self)
    def test_ac12_finalize_ack_before_full_upload(self)
    def test_ac13_streamed_chunks_enable_sub_3s_scorecard(self)
    def test_ac14_dpa_palette_consistent_across_topic_and_artifact(self)


class TestEarnedExportGate:
    def test_ac21_passing_take_routes_to_cmf()
    def test_ac21_failed_take_is_quarantined_and_redemption_required(self)
```

**File:** `tests/integration/test_era3_fr05_core_reaction_social_routing.py`

```python
class TestSocialRouting:
    def test_ac31_audience_jury_vote_inline_callback(self)
    def test_ac32_vote_then_react_prompt_is_stance_tethered(self)
    def test_ac33_supervisor_role_is_distinct_from_jury_role(self)


class TestRecovery:
    def test_ac41_redemption_round_private_quarantine(self)
    def test_redemption_retry_creates_new_session_id(self)
```

**File:** `tests/integration/test_era3_fr05_core_reaction_api.py`

```python
class TestCompatibilityAndDeprecation:
    def test_trivianar_compatibility_shim_marks_service_obsolete(self)
    def test_health_payload_exposes_reaction_engine_status(self)
    def test_websocket_fallback_sets_stream_status_degraded(self)
```

### Manual Verification

1. Start the FastAPI app and confirm `/health` reports the CORE reaction engine as ready.
2. Request a new topic and verify the payload includes `source_url`, `briefing_audio_path`, `issued_at`, `expires_at`, and a `ResolvedPalette`.
3. Open the recording flow in a test Mini App session, record a short take, hit stop, and confirm the UI receives an upload ticket immediately before the full file is uploaded.
4. Inspect the WebSocket stream and verify 10-second chunk envelopes are received during recording, not only after stop.
5. Verify a complete scorecard arrives within 3 seconds of stop on a normal network path.
6. Force an upload interruption after stop and confirm the take remains resumable using the same upload ticket.
7. Submit a deliberately weak/hedged take and verify it is marked `redemption_required`, remains private, and returns exactly 2 coaching cues.
8. Submit a strong take and verify `export_eligible=true` and CMF trigger state is emitted while the artifact remains brand-consistent.
9. Share a test debate artifact to a Telegram test account and verify Audience Jury voting works through inline buttons without a Mini App launch.
10. After a vote, verify the next prompt explicitly references the side the user selected.
11. Assign a supervisor and verify the summary they receive contains progress framing rather than a raw public artifact only.
12. Call the legacy Trivianar path and verify the compatibility layer clearly reports deprecation instead of silently pretending synchronous Trivianar is still an active product surface.
