# Tech-Spec: FR-ERA3-17 - Voice Prompt Engine
**Created:** 2026-05-12
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 4 - Pipelines & Engines
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2 requires new backend behavior to extend the existing FastAPI, model,
                      service, and schema layers instead of inventing parallel infrastructure. Section 3
                      requires explicit mapping to existing services before introducing new ones. Section 4
                      requires the 10-section spec format. The CBAR note requires named mandate enforcement in
                      Section 3 rather than implied compliance.
2. PRD LOADED:        PRD-04 exact brownfield definition: "Implement a strictly governed Voice Prompt Engine
                      where every voice note performs exactly *one* emotional job (Orient, Relieve, Validate,
                      Invite, Redirect, Celebrate) using a controlled sonic palette." PRD-04 exact packet
                      contract: "The `VoicePromptPacket` should minimally include: `emotional_job`: orient,
                      relieve, validate, invite, redirect, celebrate". PRD-04 exact doctrine: "every voice
                      note should do **one emotional job** extremely well."
3. EPIC LOADED:       Phase 4 Story 6.1 first AC: "Given a system prompt needs to be delivered, When the
                      `VoicePromptPacket` is generated, Then it dynamically selects exactly one emotional job
                      (Orient, Relieve, Validate, Invite, Redirect, Celebrate) and applies the correct tone
                      profile and sonic bed, And the voice output is rendered exclusively through the premium
                      `ConsciousVoice` TTS model (or pre-recorded human coach audio), And the output passes a
                      sonic quality gate that rejects robotic, low-fidelity, or tonally mismatched renders
                      before delivery to the user."
4. CBAR LOADED:       Phase4-M06 confirmed from the Phase 4 audit. Exact rewrite demand: the
                      `VoicePromptPacket` must enforce strict sonic quality gates and mandate premium
                      `ConsciousVoice` TTS or pre-recorded human coach audio. Generic robotic TTS is banned
                      because it destroys the premium illusion and the user will not share or trust it.
5. PRIMITIVES:        `experience_primitive_id: "EXP-TRS-003"` / `canonical_name: "Reflective Social Proof
                      (The Status Share)"`
                      `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
6. BACKEND:           `src/ccp/services/soundboard_service.py` - `async def get_preferences(self, coach_id:
                      str) -> StudioPreferences`
                      `src/ccp/services/soundboard_service.py` - `async def save_preferences(self, prefs:
                      StudioPreferences) -> SoundboardResult`
                      `src/ccp/services/soundboard_service.py` - `def build_mixer(self, voice_volume: float =
                      VOICE_GAIN_DEFAULT) -> AudioMixerConfig`
                      `src/ccp/services/engagement_feedback.py` - `def ingest(self, metrics:
                      EngagementMetrics) -> EngagementMetrics`
                      `src/ccp/services/engagement_feedback.py` - `def get_top_performing(self, limit: int =
                      10) -> list[EngagementMetrics]`
7. TESTS:             `tests/integration/test_ca11_fr17_soundboard.py` and
                      `tests/integration/test_fr18_psych_routing.py` both use acceptance-criterion-oriented
                      classes, helper builders, deterministic field assertions, and explicit fallback-path
                      verification. Section 10 follows that pattern.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P4_S26_FR-ERA3-17_Voice_Prompt_Engine.md` | 2026-05-12 | Assignment prompt, M-06 ban, and required audits |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-12 | Required backend mapping, schema extension points, and structure rules |
| 3 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Story 6.1 first AC and Sonic Prestige mandate |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | M-06 rewrite demand and primitive correction context |
| 5 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | v6.0, 2026-05-06 | Voice-first doctrine, packet contract, emotional jobs, sonic palette, and brownfield requirements |
| 6 | `docs/architecture/FR3_Voice_DNA_Extraction_Tech_Spec.md` | 2026-03-13 | Existing Voice DNA dependency and extraction boundary |
| 7 | `docs/architecture/april_updates/FR-ERA3-13_Four_Surface_Async_Skill_Ladder_Tech_Spec.md` | 2026-05-11 | Existing inline routing and next-step response pattern |
| 8 | `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` | 2026-05-12 | Existing actionable rejection and re-record voice-loop dependency |
| 9 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Codified registry | Verified governing primitive for premium, share-worthy voice delivery |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Verified supporting primitive for immediate meaningful voice feedback |
| 11 | `src/ccp/services/soundboard_service.py` | Existing service | Sonic palette, fade, mixer, and audio preference precedent |
| 12 | `src/ccp/services/engagement_feedback.py` | Existing service | Performance telemetry and resonance-marker precedent |
| 13 | `src/ccp/api/telegram_webhook.py` | Existing API | Telegram voice/text dispatch boundary and latency target |
| 14 | `src/ccp/agents/vidye_router.py` | Existing router | Current message routing boundary for user-facing responses |
| 15 | `src/ccp/models/voice_dna_models.py` | Existing models | Existing Voice DNA contract boundary to align synthesis settings |
| 16 | `src/ccp/models/ca11_models.py` | Existing models | Existing `AudioMixerConfig`, `FadeSpec`, `SoundboardResult`, and audio-preference types |
| 17 | `tests/integration/test_ca11_fr17_soundboard.py` | Existing | Acceptance-oriented audio test pattern |
| 18 | `tests/integration/test_fr18_psych_routing.py` | Existing | State-machine test pattern with fallback coverage |

## 2. Overview

### 2.1 Problem Statement

PRD-04 treats voice as the lead relational instrument of the platform, not as a notification wrapper around text.

The repo already contains useful adjacent pieces:

- `telegram_webhook.py` handles low-latency ingress
- `VidyeRouter` routes message types
- `soundboard_service.py` defines an audio preference and fade vocabulary
- Voice DNA extraction already exists as a separate intelligence layer

What the codebase still lacks is the engine that turns system intent into a governed `VoicePromptPacket`, renders that packet through a premium voice path, and guarantees that each audio prompt performs exactly one emotional job.

Without that engine, five failures are predictable:

- voice prompts collapse into generic text relays or ad hoc strings
- multiple emotional jobs get mixed into one note, creating synthetic or confusing guidance
- sonic delivery drifts into cheap or robotic fallback behavior
- voice prompt quality cannot be validated before dispatch
- prompt performance cannot feed back into later experience calibration

Story 6.1 exists to close those gaps. The system must select one emotional job, attach the right tone and sonic bed, render only through `ConsciousVoice` or pre-recorded human audio, and reject low-prestige output before the user hears it.

### 2.2 Solution

This spec introduces a new backend service, `VoicePromptEngineService`, responsible for the full packet-to-audio lifecycle for system-generated coaching voice notes.

The new engine adds seven layers:

1. `VoicePromptDecisionResolver` to select exactly one emotional job from upstream context
2. `VoicePromptComposer` to build the spoken script and packet metadata via deterministic LLM prompt contracts enforcing single-job transformation rules
3. `VoiceDNAAlignmentBridge` to apply coach-specific vocal constraints without redoing Voice DNA extraction
4. `SonicBedResolver` to bind a controlled audio bed and fade envelope
5. `ConsciousVoiceSynthesisAdapter` to render premium TTS
6. `SonicPrestigeGate` to reject robotic, low-fidelity, or job-mismatched renders
7. `VoicePromptDispatchCoordinator` to deliver, retry, or route to pre-recorded fallback packs without ever using generic TTS

This is not a replacement for the studio soundboard and not a rewrite of Telegram routing. It is the runtime engine that makes PRD-04's six emotional jobs executable as a premium coaching layer.

### 2.3 Scope

**In scope:**

- new `VoicePromptEngineService`
- `VoicePromptPacket` resolution and one-job state machine
- premium synthesis contract for `ConsciousVoice`
- pre-recorded human fallback pack strategy
- sonic bed selection and fade behavior
- quality gate before dispatch
- queue-and-retry strategy when `ConsciousVoice` is unavailable
- dispatch contract to Telegram and other async-first surfaces
- performance telemetry for prompt effectiveness
- persistence and audit logging

**Out of scope:**

- replacing `soundboard_service.py`
- replacing `VidyeRouter`
- re-implementing Voice DNA extraction
- building a full generic audio engine for arbitrary media assets
- adding robotic TTS fallback
- changing the core FR18/CBCS scoring logic

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Responsibility |
|---|---|---|---|
| DEP-VPE-001 | `VoicePromptTriggerContext` | Story 6.1 | Normalized upstream trigger state and JobSelectionReason |
| DEP-VPE-002 | `VoicePromptPacket` | PRD-04 §3.3 | Immutable definition of the prompt script, emotional job, and synthesis constraints |
| DEP-VPE-003 | `SonicBedProfile` | PRD-04 §6.8 | Governed audio bed and fade envelope |
| DEP-VPE-004 | `PreRecordedFallbackPack` | Phase4-M06 | Coach-owned human fallback audio for a specific job and locale |
| DEP-VPE-005 | `VoicePromptRenderAttempt` | Story 6.1 | Record of provider synthesis attempt, gate metrics, and failure reasons |
| DEP-VPE-006 | `VoicePromptDeliveryRecord` | FR-ERA3-17 | Delivery tracking, retry state, and routing metadata |
| DEP-VPE-007 | `VoicePromptTelemetryRecord` | PRD-04 | Long-tail performance and resonance markers |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `soundboard_service.py` | `src/ccp/services/soundboard_service.py` | Reuses fade concepts, mixer vocabulary, and audio preference patterns. The new engine must not overload studio SFX slots, but it may reuse `FadeSpec`-style transitions and preference-storage patterns. |
| `engagement_feedback.py` | `src/ccp/services/engagement_feedback.py` | Provides the resonance-marker precedent for identifying high-performing prompt types. This spec may bridge summary telemetry into that subsystem but does not route real-time delivery through it. |
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | Existing transport boundary and latency target for inbound/outbound Telegram interactions. |
| `vidye_router.py` | `src/ccp/agents/vidye_router.py` | Existing user-facing routing surface that can request or trigger voice prompts, but should not own job selection or synthesis quality gates. |
| `voice_dna_models.py` | `src/ccp/models/voice_dna_models.py` | Existing Voice DNA output contract boundary that the engine must consume for synthesis style settings. |
| `FR3_Voice_DNA_Extraction_Tech_Spec.md` | `docs/architecture/FR3_Voice_DNA_Extraction_Tech_Spec.md` | Confirms Voice DNA is already extracted upstream and must not be reimplemented here. |
| `FR-ERA3-13` spec | `docs/architecture/april_updates/FR-ERA3-13_Four_Surface_Async_Skill_Ladder_Tech_Spec.md` | Existing inline response contract for immediate next-step experiences. Voice prompts are one of the valid next-step payload types. |
| `FR-ERA3-16` spec | `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` | Existing rejection loop may trigger `Redirect` or `Relieve` job prompts after anti-centroid failure. |

### 3.3 Primitives

| Primitive ID | Name | Why It Governs This Spec | Runtime Enforcement |
|---|---|---|---|
| `EXP-TRS-003` | `Reflective Social Proof (The Status Share)` | Story 6.1 is fundamentally about whether the voice sounds premium enough to reinforce status and trust. | `ConsciousVoice` or coach-owned human fallback only; low-prestige audio is rejected. |
| `EXP-FBK-001` | `RIM Feedback Discipline` | Voice prompts often carry corrective or confirmatory guidance and must remain immediate and meaningful. | Packets must resolve quickly, use one clear job, and explain the next step without multi-purpose drift. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Story | Enforcement in This Spec |
|---|---|---|
| `Phase4-M06 - The Sonic Prestige Rule` | Story 6.1 | `VoicePromptPacket` render path may use only `ConsciousVoice` synthesis or `PRE_RECORDED_HUMAN` fallback packs. Generic TTS providers are not valid enum values. |
| `Phase4-M06 - The Sonic Prestige Rule` | Story 6.1 | `SonicPrestigeGate` blocks robotic, low-fidelity, clipping, or tonally mismatched audio before dispatch. Failed renders are queued for retry or switched to pre-recorded human fallback if available. |
| `Phase4-M06 - The Sonic Prestige Rule` | Story 6.1 | `VoicePromptDecisionResolver` emits exactly one `EmotionalJob`. Mixed-job packets are invalid model states and must fail validation. |

### 3.5 Technical Decisions

| Decision | Rationale | Consequence |
|---|---|---|
| Keep studio soundboard and voice prompt runtime separate | `soundboard_service.py` is a studio/operator audio utility. PRD-04 voice prompts are end-user coaching artifacts. | Reuse audio patterns, not UI slot semantics or the `studio_preferences` table directly. |
| Define a strict one-job enum and validation gate | PRD-04 explicitly bans multipurpose notes. | A packet with multiple jobs, composite jobs, or empty job is a schema error, not a warning. |
| Ban generic TTS at the type system level | The prompt and mandate both make the ban non-negotiable. | No "fallback_provider='system_tts'" field may exist. |
| Prefer queue-and-retry over degraded voice quality | Premium illusion is more important than instant cheap audio. | Some prompts may be delayed, but none may degrade into robotic output. |
| Allow pre-recorded human fallback packs only when job-matched | A celebratory human clip cannot stand in for a corrective redirect. | Fallback packs are indexed by `coach_id + emotional_job + locale`. |
| Use telemetry as a one-way learning input, not a real-time routing dependency | Prompt delivery cannot wait on analytics writes. | Telemetry failures never block dispatch. |
| Reuse Voice DNA as an upstream dependency, not a new extraction step | FR3 already owns extraction. | This engine consumes a resolved voice profile reference only. |

## 4. Implementation Plan

### Phase 1 - Models, Tables, and Route Layer

1. Create `src/ccp/models/voice_prompt_engine_models.py`.
2. Define `VoicePromptPacket`, `VoicePromptRenderAttempt`, `VoicePromptDeliveryRecord`, and `PreRecordedFallbackPack`.
3. Add `EmotionalJob`, `JobSelectionReason`, `RenderSource`, and `PromptStatus` enums.
4. Extend `src/ccp/scripts/setup_supabase.py` with voice prompt tables.
5. Add `src/ccp/api/voice_prompt_api.py`.
6. Register new routes in `src/ccp/api/main.py`.

### Phase 2 - Job Selection and Composition

7. Implement `VoicePromptDecisionResolver`.
8. Implement the one-job state machine and packet validation rules.
9. Implement `VoicePromptComposer` with a strict CBAR-compliant LLM prompt contract per emotional job. The LLM prompt must enforce exactly one EmotionalJob and explicitly map `score_delta` or `streak_days` into the script without appending any secondary calls to action.
10. Add `VoiceDNAAlignmentBridge` for style settings and timing guidance.
11. Add locale handling and coach-scoped prompt preferences.

### Phase 3 - Render, Gate, and Dispatch

12. Implement `ConsciousVoiceSynthesisAdapter`.
13. Implement `SonicBedResolver` using controlled bed profiles and fade envelopes.
14. Implement `SonicPrestigeGate`.
15. Implement `PreRecordedFallbackPackResolver`.
16. Implement `VoicePromptDispatchCoordinator` for Telegram delivery and deferred queue release.

### Phase 4 - Telemetry, Retry, and Validation

17. Implement retry policy for `ConsciousVoice` outages.
18. Implement summary telemetry capture for replay/completion/forward behavior.
19. Add `VoicePromptTelemetryBridge` to produce resonance summaries compatible with `engagement_feedback.py` patterns.
20. Add receipt chain entries for resolve, render, gate, fallback, dispatch, and retry.
21. Add unit and integration tests.

## 5. Schema

### 5.1 New Model File

Create:

`src/ccp/models/voice_prompt_engine_models.py`

### 5.2 Pydantic v2 Models

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EmotionalJob(str, Enum):
    ORIENT = "orient"
    RELIEVE = "relieve"
    VALIDATE = "validate"
    INVITE = "invite"
    REDIRECT = "redirect"
    CELEBRATE = "celebrate"


class JobSelectionReason(str, Enum):
    SESSION_START = "session_start"
    HESITATION_RECOVERY = "hesitation_recovery"
    DISCLOSURE_ACK = "disclosure_ack"
    ACTION_READY = "action_ready"
    CORRECTION_REQUIRED = "correction_required"
    WIN_CONFIRMED = "win_confirmed"


class RenderSource(str, Enum):
    CONSCIOUS_VOICE = "conscious_voice"
    PRE_RECORDED_HUMAN = "pre_recorded_human"


class PromptStatus(str, Enum):
    RESOLVED = "resolved"
    RENDER_QUEUED = "render_queued"
    RENDERED = "rendered"
    GATE_REJECTED = "gate_rejected"
    DISPATCHED = "dispatched"
    RETRY_PENDING = "retry_pending"
    FALLBACK_RENDERED = "fallback_rendered"
    FAILED_PRESTIGE_GUARD = "failed_prestige_guard"


class DeliverySurface(str, Enum):
    TELEGRAM = "telegram"
    MINI_APP = "mini_app"
    AFFINE = "affine"


class SonicBedProfile(BaseModel):
    bed_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    emotional_job: EmotionalJob
    fade_in_ms: int = Field(ge=0)
    fade_out_ms: int = Field(ge=0)
    target_gain: float = Field(ge=0.0, le=1.0)
    duration_ceiling_seconds: int = Field(gt=0, le=90)


class VoicePromptTriggerContext(BaseModel):
    coach_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    surface: DeliverySurface
    reason: JobSelectionReason
    locale: str = Field(min_length=2, max_length=8)
    source_session_id: str | None = None
    score_delta: float | None = Field(default=None, ge=-100.0, le=100.0)
    streak_days: int | None = Field(default=None, ge=0)


class VoicePromptPacket(BaseModel):
    voice_prompt_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    emotional_job: EmotionalJob
    job_selection_reason: JobSelectionReason
    surface: DeliverySurface
    locale: str = Field(min_length=2, max_length=8)
    script_text: str = Field(min_length=1, max_length=1200)
    sonic_bed_profile: SonicBedProfile
    voice_dna_profile_ref: str = Field(min_length=1)
    render_source_preference: RenderSource = RenderSource.CONSCIOUS_VOICE
    duration_target_seconds: int = Field(gt=0, le=90)
    created_at: datetime


class PreRecordedFallbackPack(BaseModel):
    fallback_pack_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    emotional_job: EmotionalJob
    locale: str = Field(min_length=2, max_length=8)
    audio_asset_id: str = Field(min_length=1)
    transcript_reference: str = Field(min_length=1)
    duration_seconds: int = Field(gt=0, le=90)


class VoicePromptRenderAttempt(BaseModel):
    render_attempt_id: str = Field(min_length=1)
    voice_prompt_id: str = Field(min_length=1)
    render_source: RenderSource
    provider_reference: str = Field(min_length=1)
    audio_asset_id: str | None = None
    sample_rate_hz: int = Field(gt=0)
    duration_seconds: int = Field(gt=0, le=90)
    prestige_gate_passed: bool = False
    rejection_reason: str | None = None
    created_at: datetime


class VoicePromptDeliveryRecord(BaseModel):
    delivery_id: str = Field(min_length=1)
    voice_prompt_id: str = Field(min_length=1)
    surface: DeliverySurface
    dispatched_at: datetime | None = None
    delivery_status: PromptStatus
    retry_count: int = Field(ge=0)
    telegram_chat_id: str | None = None


class VoicePromptTelemetryRecord(BaseModel):
    telemetry_id: str = Field(min_length=1)
    voice_prompt_id: str = Field(min_length=1)
    replay_count: int = Field(ge=0)
    completion_count: int = Field(ge=0)
    forward_count: int = Field(ge=0)
    reply_count: int = Field(ge=0)
    resonance_marker: bool = False
    recorded_at: datetime
```

### 5.3 One-Job State Machine

The job-selection state machine is deterministic and exclusive.

Upstream services must submit a `VoicePromptTriggerContext.reason` value from this controlled set:

- `SESSION_START`
- `HESITATION_RECOVERY`
- `DISCLOSURE_ACK`
- `ACTION_READY`
- `CORRECTION_REQUIRED`
- `WIN_CONFIRMED`

Job mapping:

| Trigger Reason | Selected Emotional Job | Notes |
|---|---|---|
| `SESSION_START` | `ORIENT` | Gives context, where we are, and what this moment means |
| `HESITATION_RECOVERY` | `RELIEVE` | Softens shame or anxiety after friction or poor performance |
| `DISCLOSURE_ACK` | `VALIDATE` | Mirrors the user's truth and acknowledges vulnerability |
| `ACTION_READY` | `INVITE` | Calls for the next concrete action without adding correction or praise |
| `CORRECTION_REQUIRED` | `REDIRECT` | Re-aims behavior or framing after a wrong turn |
| `WIN_CONFIRMED` | `CELEBRATE` | Locks in progress, victory, or earned completion |

Validation rules:

- exactly one trigger reason is required
- exactly one emotional job must be derived
- jobs may not be combined
- template composition may not append a second job CTA
- `Celebrate + Redirect`, `Validate + Invite`, and all other pairs are invalid states

### 5.4 API Contract

#### Resolve and issue prompt

`POST /api/cve/voice-prompts/issue`

```json
{
  "coach_id": "coach-001",
  "user_id": "user-998",
  "surface": "telegram",
  "reason": "win_confirmed",
  "locale": "en",
  "source_session_id": "arena-44",
  "score_delta": 12.5,
  "streak_days": 5,
  "failure_detected": false,
  "win_detected": true,
  "disclosure_detected": false,
  "correction_required": false
}
```

#### Success response

```json
{
  "voice_prompt_id": "VPE-001",
  "coach_id": "coach-001",
  "user_id": "user-998",
  "emotional_job": "celebrate",
  "job_selection_reason": "win_confirmed",
  "surface": "telegram",
  "locale": "en",
  "script_text": "That was a strong finish. You held the line, stayed clear, and earned this score jump.",
  "sonic_bed_profile": {
    "bed_id": "bed_celebrate_01",
    "display_name": "Warm Lift",
    "emotional_job": "celebrate",
    "fade_in_ms": 120,
    "fade_out_ms": 220,
    "target_gain": 0.42,
    "duration_ceiling_seconds": 24
  },
  "voice_dna_profile_ref": "VDNA-COACH-001",
  "render_source_preference": "conscious_voice",
  "duration_target_seconds": 18,
  "created_at": "2026-05-12T10:20:00Z"
}
```

#### Render attempt success

```json
{
  "render_attempt_id": "VPE-RENDER-001",
  "voice_prompt_id": "VPE-001",
  "render_source": "conscious_voice",
  "provider_reference": "cv-job-771",
  "audio_asset_id": "AST-AUDIO-991",
  "sample_rate_hz": 48000,
  "duration_seconds": 18,
  "prestige_gate_passed": true,
  "rejection_reason": null,
  "created_at": "2026-05-12T10:20:02Z"
}
```

#### Queue-and-retry response

```json
{
  "voice_prompt_id": "VPE-002",
  "status": "retry_pending",
  "retry_after_seconds": 20,
  "fallback_pack_available": false,
  "queue_reason": "conscious_voice_provider_unavailable"
}
```

#### Human fallback response

```json
{
  "render_attempt_id": "VPE-RENDER-009",
  "voice_prompt_id": "VPE-003",
  "render_source": "pre_recorded_human",
  "provider_reference": "fallback-pack-validate-en",
  "audio_asset_id": "AST-AUDIO-HUMAN-77",
  "sample_rate_hz": 48000,
  "duration_seconds": 21,
  "prestige_gate_passed": true,
  "rejection_reason": null,
  "created_at": "2026-05-12T10:20:10Z"
}
```

### 5.5 Required Tables

```sql
CREATE TABLE IF NOT EXISTS voice_prompt_packets (
    voice_prompt_id              TEXT PRIMARY KEY,
    coach_id                     TEXT NOT NULL,
    user_id                      TEXT NOT NULL,
    emotional_job                TEXT NOT NULL,
    job_selection_reason         TEXT NOT NULL,
    delivery_surface             TEXT NOT NULL,
    locale                       TEXT NOT NULL,
    script_text                  TEXT NOT NULL,
    voice_dna_profile_ref        TEXT NOT NULL,
    render_source_preference     TEXT NOT NULL,
    prompt_status                TEXT NOT NULL,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_prompt_render_attempts (
    render_attempt_id            TEXT PRIMARY KEY,
    voice_prompt_id              TEXT NOT NULL,
    render_source                TEXT NOT NULL,
    provider_reference           TEXT NOT NULL,
    audio_asset_id               TEXT,
    sample_rate_hz               INTEGER NOT NULL,
    duration_seconds             INTEGER NOT NULL,
    prestige_gate_passed         BOOLEAN NOT NULL DEFAULT FALSE,
    rejection_reason             TEXT,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_prompt_delivery_records (
    delivery_id                  TEXT PRIMARY KEY,
    voice_prompt_id              TEXT NOT NULL,
    delivery_surface             TEXT NOT NULL,
    delivery_status              TEXT NOT NULL,
    retry_count                  INTEGER NOT NULL DEFAULT 0,
    telegram_chat_id             TEXT,
    dispatched_at                TIMESTAMPTZ,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_prompt_fallback_packs (
    fallback_pack_id             TEXT PRIMARY KEY,
    coach_id                     TEXT NOT NULL,
    emotional_job                TEXT NOT NULL,
    locale                       TEXT NOT NULL,
    audio_asset_id               TEXT NOT NULL,
    transcript_reference         TEXT NOT NULL,
    duration_seconds             INTEGER NOT NULL,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS voice_prompt_telemetry (
    telemetry_id                 TEXT PRIMARY KEY,
    voice_prompt_id              TEXT NOT NULL,
    replay_count                 INTEGER NOT NULL DEFAULT 0,
    completion_count             INTEGER NOT NULL DEFAULT 0,
    forward_count                INTEGER NOT NULL DEFAULT 0,
    reply_count                  INTEGER NOT NULL DEFAULT 0,
    resonance_marker             BOOLEAN NOT NULL DEFAULT FALSE,
    recorded_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## 6. Backward Compatibility Fallback

### 6.1 `ConsciousVoice` unavailable

If the premium provider is unavailable:

1. check for a coach-scoped, emotional-job-matched `PreRecordedFallbackPack`
2. if present, render through `PRE_RECORDED_HUMAN` and hydrate `VoicePromptPacket.script_text` using the string retrieved from `transcript_reference` to ensure downstream analytic parity
3. if absent, mark the packet `RETRY_PENDING`, enqueue a retry, and do not dispatch low-quality synthetic audio

Generic TTS fallback is never allowed.

### 6.2 Prestige gate failure

If audio renders but fails `SonicPrestigeGate` due to strict biometric and acoustic thresholds (e.g., `provider_confidence_score < 0.85`, `clipping_ratio > 0.01`, or acoustic `tonal_match_score < 0.80` against the emotional job centroid):

- do not dispatch
- if a human fallback pack exists for that exact job and locale, switch to it
- otherwise queue a re-render with a refined synthesis profile

### 6.3 Missing Voice DNA profile

If `voice_dna_profile_ref` cannot be resolved:

- use the coach's default premium voice configuration if one exists
- maintain the same emotional job and sonic bed
- mark `voice_dna_alignment_status=degraded_default`
- never switch to generic TTS

### 6.4 Missing sonic bed mapping

If no bed is configured for the selected job:

- fall back to a job-specific silent-bed profile only if clarity is preserved
- do not pick a random music track
- store `bed_fallback_status=silent_profile`

### 6.5 Telemetry write failure

If prompt telemetry cannot be written:

- dispatch still proceeds
- a receipt entry records `telemetry_status=deferred`
- a retry job backfills telemetry later

### 6.6 Legacy string notification callers

Legacy callers that currently send flat text notifications must be wrapped by a `VoicePromptIntentAdapter`:

- string source + context in
- valid `VoicePromptTriggerContext` out

Direct string-to-TTS dispatch is obsolete and must be removed from future paths.

## 7. Tasks

- [ ] Create `src/ccp/models/voice_prompt_engine_models.py`.
- [ ] Create `src/ccp/services/voice_prompt_engine.py`.
- [ ] Add new voice prompt tables to `src/ccp/scripts/setup_supabase.py`.
- [ ] Add `VoicePromptDecisionResolver`.
- [ ] Implement exact one-job state machine.
- [ ] Add `VoicePromptComposer` with one template family per emotional job.
- [ ] Add `VoiceDNAAlignmentBridge`.
- [ ] Add `SonicBedResolver`.
- [ ] Add `ConsciousVoiceSynthesisAdapter`.
- [ ] Add `SonicPrestigeGate`.
- [ ] Add `PreRecordedFallbackPackResolver`.
- [ ] Add `VoicePromptDispatchCoordinator`.
- [ ] Add `VoicePromptTelemetryBridge`.
- [ ] Add internal route file and register it in `main.py`.
- [ ] Refactor legacy string notification call sites to emit `VoicePromptTriggerContext`.

## 8. Acceptance Criteria

### AC1 - Exactly one emotional job is selected for every prompt

**Given** a valid `VoicePromptTriggerContext`,  
**When** the voice prompt engine resolves the packet,  
**Then** it selects exactly one `EmotionalJob`,  
**And** that job is derived deterministically from the `JobSelectionReason`,  
**And** the final `VoicePromptPacket` contains no secondary emotional job or blended CTA.

**FAILURE EXAMPLE:** A note starts by celebrating a win, then shifts into course correction and ends with a new task invitation. That is a spec violation because the packet has performed `Celebrate + Redirect + Invite` in one prompt.

**Mandate:** Story 6.1 and `Phase4-M06` one-job enforcement.

### AC2 - All dynamic prompts render through `ConsciousVoice` or pre-recorded human fallback only

**Given** a prompt is ready to render,  
**When** synthesis begins,  
**Then** `render_source` must be either `CONSCIOUS_VOICE` or `PRE_RECORDED_HUMAN`,  
**And** no generic system TTS provider may be selected,  
**And** any unsupported provider choice is a terminal validation error.

**FAILURE EXAMPLE:** `ConsciousVoice` times out, so the engine falls back to a default mobile TTS voice to keep things moving. That is a direct spec violation and a direct violation of `Phase4-M06`.

**Mandate:** `Phase4-M06 - The Sonic Prestige Rule`.

### AC3 - `ConsciousVoice` outages trigger retry or human fallback, not degraded audio

**Given** the premium provider is temporarily unavailable,  
**When** a prompt cannot render through `ConsciousVoice`,  
**Then** the engine either uses a job-matched pre-recorded human fallback pack or marks the prompt `RETRY_PENDING`,  
**And** the system records the retry reason and retry count,  
**And** the user never receives a robotic degraded substitute.

**FAILURE EXAMPLE:** The engine logs the outage correctly but sends a text-read MP3 through a low-quality fallback provider. That is a spec violation.

**Mandate:** `Phase4-M06 - The Sonic Prestige Rule`.

### AC4 - Sonic prestige gate blocks robotic or tonally mismatched renders before dispatch

**Given** a render attempt completes,  
**When** `SonicPrestigeGate` evaluates the result,  
**Then** failure to meet the hard thresholds (`provider_confidence_score >= 0.85`, `clipping_ratio <= 0.01`, `tonal_match_score >= 0.80`) causes `prestige_gate_passed=false`,  
**And** the prompt is not dispatched,  
**And** the engine retries or switches to human fallback if available.

**FAILURE EXAMPLE:** A `Relieve` prompt is synthesized with harsh, energetic delivery and still gets sent because the waveform is technically valid. That is a spec violation because tone-job mismatch is a gate failure, not a cosmetic issue.

**Mandate:** Story 6.1 and `Phase4-M06`.

### AC5 - The selected sonic bed matches the emotional job and uses a controlled palette

**Given** a `VoicePromptPacket` has been resolved,  
**When** the engine binds a sonic bed,  
**Then** the bed comes from a controlled job-specific registry,  
**And** fade behavior is explicit,  
**And** no random library track or uncontrolled soundboard slot is used.

**FAILURE EXAMPLE:** `Celebrate` receives a random studio music track because it happened to be configured in `studio_preferences`. That is a spec violation because the voice prompt engine is not allowed to improvise its sonic palette from operator soundboard state.

**Mandate:** PRD-04 controlled sonic palette rule, supports `Phase4-M06`.

### AC6 - Prompt telemetry captures resonance without blocking delivery

**Given** a prompt is dispatched,  
**When** replay, completion, forward, or reply behavior is observed,  
**Then** the engine records a `VoicePromptTelemetryRecord`,  
**And** high-performing prompt patterns may be summarized into resonance markers,  
**And** telemetry failure never blocks prompt delivery.

**FAILURE EXAMPLE:** A valid `Invite` prompt is fully rendered but dispatch is delayed because telemetry storage is down. That is a spec violation because analytics is not on the critical path.

**Mandate:** Supporting quality gate for PRD-04 evaluation, no CBAR conflict.

## 9. Dependencies

### Internal services

| Dependency | Type | Use |
|---|---|---|
| `SoundboardService` | Existing service | Fade semantics, audio preference patterns, and audio-config vocabulary |
| `EngagementFeedback` | Existing service | Resonance-marker precedent for prompt performance summaries |
| `VidyeRouter` | Existing agent | Delivery request source and trigger integration surface |
| `telegram_webhook` | Existing API | Telegram transport boundary |
| Voice DNA extraction outputs | Existing upstream intelligence | Coach-specific vocal alignment inputs |

### Internal models and storage

| Dependency | Type | Use |
|---|---|---|
| `voice_dna_models.py` | Existing models | Voice profile reference and alignment constraints |
| `ca11_models.py` audio types | Existing models | Audio mixer and fade vocabulary reuse |
| Supabase | Existing infra | Voice prompt packet, render, and delivery persistence |
| `receipt_chain` | Existing core | Immutable lifecycle audit trail |

### New external or sidecar assumptions

| Dependency | Assumption |
|---|---|
| `ConsciousVoice` provider | Available through a premium TTS integration or internal sidecar adapter |
| Pre-recorded human fallback packs | Stored as coach-scoped or org-scoped approved audio assets |
| Telegram send-audio capability | Existing bot credentials can deliver rendered voice note assets |

## 10. Testing Strategy

This section follows the style of `tests/integration/test_ca11_fr17_soundboard.py` and `tests/integration/test_fr18_psych_routing.py`: named AC classes, helper builders, deterministic assertions, and explicit fallback-path tests.

### 10.1 Unit tests

#### `test_frera317_job_selection.py`

- `test_session_start_selects_orient_only`
- `test_hesitation_recovery_selects_relieve_only`
- `test_correction_required_selects_redirect_only`
- `test_win_confirmed_selects_celebrate_only`

#### `test_frera317_prestige_gate.py`

- `test_robotic_render_fails_prestige_gate`
- `test_tonally_mismatched_relieve_prompt_fails_gate`
- `test_clean_consciousvoice_render_passes_gate`

#### `test_frera317_fallback_policy.py`

- `test_consciousvoice_outage_sets_retry_pending_when_no_human_pack`
- `test_job_matched_human_pack_is_used_when_available`
- `test_generic_tts_provider_is_rejected_at_model_validation`

### 10.2 Integration tests

#### `tests/integration/test_frera317_voice_prompt_engine.py`

Scenario class: `TestAC1SingleEmotionalJob`

- Build one `VoicePromptTriggerContext` per `JobSelectionReason`.
- Assert the resulting packet contains exactly one `EmotionalJob`.
- Assert the script does not contain a second-job appendage.

Scenario class: `TestAC2PremiumRenderPath`

- Render through mocked `ConsciousVoice`.
- Assert `render_source == conscious_voice`.
- Assert dispatch never references a generic provider.

Scenario class: `TestAC4PrestigeGate`

- Feed a mocked low-fidelity render.
- Assert `prestige_gate_passed is False`.
- Assert no delivery record is marked `DISPATCHED`.

#### `tests/integration/test_frera317_retry_and_fallback.py`

Scenario class: `TestAC3RetryOrHumanFallback`

- Simulate provider outage with and without a matching fallback pack.
- Assert fallback pack is used only when `coach_id + emotional_job + locale` matches.
- Assert otherwise the prompt becomes `RETRY_PENDING`.

Scenario class: `TestAC6TelemetryNonBlocking`

- Dispatch a prompt while telemetry write is mocked to fail.
- Assert prompt still reaches `DISPATCHED`.
- Assert receipt metadata records `telemetry_status=deferred`.

### 10.3 Non-regression requirements

- No test may pass if a packet contains more than one emotional job.
- No test may pass if a generic TTS provider is configured as fallback.
- No test may pass if a failed prestige gate render still dispatches.
- No test may pass if `studio_preferences` random tracks are used as uncontrolled prompt beds.
