# Tech-Spec: FR-ERA3-10 - Zero-Config Onboarding Flow Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 3 - Experience Mini Apps
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new Mini App routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      schema changes extend `src/ccp/scripts/setup_supabase.py`, Section 3 requires a concrete
                      anonymous session model if auth is deferred, and Section 4 requires explicit CBAR mandate
                      enforcement in both Section 3 and Section 8.
2. PRD LOADED:        PRD-01 exact platform rule: "Establish the foundational platform split: AFFiNE serves as
                      the Sovereign Command Center for the coach... Telegram (via chat and native Mini Apps)
                      serves as the Sovereign Execution Surface for the client/audience..." PRD-01 also states:
                      "This is not a marketing funnel — it is a trust-transfer mechanism where the product itself
                      is the referral. The commercial truth: free proof gets them inside..." and defines the
                      `$0` Lead Magnet as "free 4-asset package ... free benchmark teaser." PRD-04 exact brownfield
                      rule: "Lock the entire user experience into exactly two sovereign surfaces... complex UI
                      interactions ... must be handled by a native Telegram Mini App Companion." PRD-04 also makes
                      the experience rule explicit: "one obvious action" and fast first-session value.
3. EPIC LOADED:       Story 6.1 first AC: "Given I tap a Silent Referral link and enter the Telegram Mini App,
                      When I complete the single, obvious 60-second baseline voice audit, Then the system
                      immediately delivers a meaningful benchmark teaser score within the Telegram chat UI or
                      anonymous Mini App session — no registration, email verification, or authentication gate is
                      triggered before this reveal."
4. CBAR LOADED:       Phase3-M07 is absolute. The audit note states: "The benchmark teaser MUST be delivered
                      instantly within the Telegram chat UI or the anonymous Mini App session without triggering
                      any registration or auth walls." Verdict: PASS WITH NOTE, provided no auth wall precedes the
                      reveal.
5. PRIMITIVES:        `experience_primitive_id: "EXP-FRC-002"` / `canonical_name: "System 1 to System 2 Escalation"`
                      `experience_primitive_id: "EXP-TRG-002"` / `canonical_name: "Hook Cycle Velocity"`
6. BACKEND:           `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
                      `src/ccp/services/offer_tier_governor.py` - `def evaluate(self, *, client_id: str, coping_position: int | None, target_campaign_tier: int, historical_purchased_tiers: list[Any] | None = None) -> OfferTierGovernorRow`
                      `src/ccp/services/conversion_sequence_router.py` - `def route(self, *, client_id: str, spt_stage: int | None, hours_since_last_message: float, current_sequence_step: int, next_payload_string: str | None) -> ConversionSequencePayloadRow`
                      `src/ccp/services/lead_capture_service.py` - `def capture_new_member(self, telegram_user_id: int, first_name: str, coach_id: str, stream_id: str, referred_by_user_id: Optional[int] = None) -> LeadCaptureResult`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, async wrappers,
                      direct typed assertions, and class-per-scenario organization rather than loose smoke tests.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P3_S20_FR-ERA3-10_Onboarding_Flow.md` | 2026-05-11 | Assignment prompt, output target, and M-07 hard rule |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory stack, route, schema, and CBAR requirements |
| 3 | `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | 2026-05-10 | Epic 6 story text, AC, and Friction-Zero quality standard |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | 2026-05-10 | M-07 audit note and auth-wall rejection language |
| 5 | `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` | v6.0, 2026-05-06 | Telegram-first execution surface, free-proof ladder, and Lead Magnet pricing architecture |
| 6 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | v6.0, 2026-05-06 | Two-touchpoint Mini App doctrine, low-friction first-session design, and onboarding warmth |
| 7 | `primitives/experience/friction_ability/EXP-FRC-002.yaml` | Codified registry | Verified friction primitive used for the anonymous-first first-session architecture |
| 8 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | Codified registry | Verified timing primitive for immediate teaser reveal |
| 9 | `src/ccp/services/trait_scoring_engine.py` | Existing service | Baseline audit scoring engine consumed through an adapter, not redefined |
| 10 | `src/ccp/services/signal_source_loader.py` | Existing service | Reveals the `SignalBundle` input contract that the anonymous scoring adapter must satisfy |
| 11 | `src/ccp/services/offer_tier_governor.py` | Existing service | Post-reveal Lead Magnet routing and offer ceiling governance |
| 12 | `src/ccp/services/conversion_sequence_router.py` | Existing service | Optional post-registration follow-up routing after the teaser and offer reveal |
| 13 | `src/ccp/services/lead_capture_service.py` | Existing service | Existing capture and referral-attribution pattern for users who opt into registration |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI registration and `/health` extension point |
| 15 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit trail for anonymous session, teaser reveal, offer display, and identity link |
| 16 | `src/ccp/core/circuit_breaker.py` | Current | Failure protection and high-risk halt rules |
| 17 | `src/ccp/scripts/setup_supabase.py` | Current | Canonical schema extension point |
| 18 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and receipt assertions |
| 19 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async helper style and scenario grouping |
| 20 | `docs/architecture/april_updates/FR-ERA3-19_Testimonial_Builder_User_Cards_Tech_Spec.md` | 2026-05-11 draft | Confirms Era3 precedent for anonymous/session-first capture before optional identity linkage |

## 2. Overview

### 2.1 Problem Statement

The platform already has strong downstream coaching and conversion engines, but it still lacks the first-touch Mini App that makes a cold lead feel immediate value before the system asks for anything back. Epic 6 is trying to solve exactly that problem: turn a Silent Referral tap into one obvious action, one meaningful reveal, and one clear next step.

Without a dedicated anonymous onboarding flow, three failures happen:

- the user hits a registration or identity wall before seeing proof
- the teaser score is delayed long enough to break the dopamine moment
- the Lead Magnet layer appears as a bait-and-switch ask rather than a natural continuation of value

The CBAR audit is unambiguous that the first failure is fatal. If the score is hidden behind account creation, the flow is structurally wrong, even if the rest of the system is technically polished.

### 2.2 Solution

This spec creates a standalone `startapp=onboarding` Telegram Mini App that runs an anonymous-first baseline audit flow before any registration requirement. The architecture is deliberately split into three layers:

- `AnonymousAuditSessionManager` for session creation, recording, and persistence without identity
- `BaselineTeaserScoringAdapter` for producing the 60-second benchmark teaser from existing scoring infrastructure
- `PostRevealOfferProjector` for surfacing the Lead Magnet layer only after the teaser is revealed

The flow is fixed:

1. tap Silent Referral link
2. create anonymous Mini App session
3. record 60-second baseline voice audit
4. compute and reveal teaser score immediately
5. show Lead Magnet offer
6. optionally register and link identity
7. optionally route into follow-up or challenge handoff

### 2.3 Scope

**In scope:**

- `startapp=onboarding` Mini App shell
- anonymous session creation with no Telegram identity requirement
- 60-second baseline voice audit flow
- immediate benchmark teaser reveal in-chat or in Mini App
- post-reveal Lead Magnet projection using existing offer-governance logic
- optional anonymous-to-registered transition after reveal
- referral-token preservation across anonymous and registered states
- receipt-chain logging and M-07 enforcement
- explicit state machine and persistence model for the anonymous lifecycle

**Out of scope:**

- re-specifying FR61 scoring internals
- full paid checkout flows after the Lead Magnet
- requiring a Telegram login or email before teaser reveal
- replacing existing conversion or lead-capture systems
- any reaction-mode entry surface beyond the first-touch audit

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object / Schema | Source FR | Pipeline Stage |
|---|---|---|---|
| DEP-ONB-001 | `AnonymousOnboardingSession` | Story 6.1 | Produced by `AnonymousAuditSessionManager` to track state without identity |
| DEP-ONB-002 | `AnonymousAuditAsset` | Story 6.1 | Produced by `BaselineAuditRecorder` representing the 60-second voice action |
| DEP-ONB-003 | `BenchmarkTeaserScore` | Story 6.1 | Produced by `BaselineTeaserScoringAdapter` as a teaser-safe benchmark packet |
| DEP-ONB-004 | `LeadMagnetOfferProjection` | Story 6.1 | Produced by `PostRevealOfferProjector` displaying the Tier 1 Lead Magnet |
| DEP-ONB-005 | `AnonymousRegistrationLink` | Story 6.1 | Produced by `AnonymousRegistrationLinker` bridging anonymous to registered |
| DEP-ONB-006 | `AnonymousReferralToken` | Story 6.1 | Produced by `ReferralTokenResolver` to persist attribution |
| DEP-ONB-007 | `OnboardingLaunchResponse` | FR-ERA3-10 | API response for session start |
| DEP-ONB-008 | `TeaserRevealResponse` | FR-ERA3-10 | API response for benchmark reveal |
| DEP-ONB-009 | `OfferRevealResponse` | FR-ERA3-10 | API response for offer projection |
| DEP-ONB-010 | `RegistrationRequest` | FR-ERA3-10 | API payload for identity linkage |
| DEP-ONB-011 | `RegistrationResponse` | FR-ERA3-10 | API response after successful linkage |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Consumed through `BaselineTeaserScoringAdapter`, which generates a teaser-safe subset of outputs from the existing scoring engine rather than inventing a new score algorithm. |
| `signal_source_loader.py` | `src/ccp/services/signal_source_loader.py` | Provides the real `SignalBundle` contract that the anonymous audit adapter must emulate in memory for baseline scoring. |
| `offer_tier_governor.py` | `src/ccp/services/offer_tier_governor.py` | `evaluate(...)` is called only after the teaser reveal to authorize the Lead Magnet tier surface. |
| `conversion_sequence_router.py` | `src/ccp/services/conversion_sequence_router.py` | Optional follow-up routing once the anonymous session is linked to a real client identifier. |
| `lead_capture_service.py` | `src/ccp/services/lead_capture_service.py` | Existing attribution and new-member capture pattern reused when the user opts into registration or group-based entry. |
| `main.py` | `src/ccp/api/main.py` | Registers the onboarding router and extends `/health` with onboarding readiness. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs session creation, recording completion, teaser reveal, offer display, registration, and auth-wall rule compliance. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Halts risky automated escalation if the anonymous audit contains crisis signals. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends the canonical schema with anonymous sessions, audit assets, teaser results, and registration links. |

**Existing tables consumed:**

- `receipt_chain` - immutable audit records
- `asset_registry` - audio asset IDs for baseline audit uploads
- `person_registry` - eventual person linkage after registration

**New onboarding tables introduced by this spec:**

- `anonymous_onboarding_sessions` - one row per anonymous first-touch audit session
- `anonymous_onboarding_audio_assets` - uploaded 60-second baseline recordings and processing status
- `anonymous_onboarding_teasers` - persisted teaser-score payloads and reveal timestamps
- `anonymous_registration_links` - bridge rows connecting anonymous sessions to registered `person_id` values
- `onboarding_offer_impressions` - post-reveal offer display and acceptance events
- `onboarding_referral_tokens` - tokenized inbound Silent Referral attribution

**Existing API routes extended or called:**

- `GET /health` - extended with onboarding readiness

**New API routes introduced by this spec:**

- `POST /api/onboarding/session/start` - create an anonymous session from a referral link
- `POST /api/onboarding/session/{session_id}/audit-upload` - upload the 60-second baseline recording
- `POST /api/onboarding/session/{session_id}/audit-complete` - finalize recording and start teaser processing
- `GET /api/onboarding/session/{session_id}/teaser` - fetch the teaser benchmark reveal
- `GET /api/onboarding/session/{session_id}/offer` - fetch the Lead Magnet surface after reveal
- `POST /api/onboarding/session/{session_id}/register` - optionally link identity after teaser and offer
- `POST /api/onboarding/session/{session_id}/challenge-handoff` - create the post-registration challenge bridge

**M-07 route-order rule**

The following routes are forbidden before `benchmark_revealed_at` is set:

- `POST /api/onboarding/session/{session_id}/register`
- `GET /api/onboarding/session/{session_id}/offer`
- `POST /api/onboarding/session/{session_id}/challenge-handoff`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-FRC-002` | System 1 to System 2 Escalation | friction_ability | The first move must remain cognitively light: tap, record, receive proof. Only after the teaser does the flow escalate into the higher-commitment ask of Lead Magnet opt-in or registration. |
| `EXP-TRG-002` | Hook Cycle Velocity | trigger_timing | The benchmark reveal must arrive immediately after the audit completes so the emotional momentum from effort becomes a felt result rather than a delayed promise. |

**Naming note**

Epic 6 labels `EXP-FRC-002` as `Friction-Zero Ability`, while the verified YAML canonical name is `System 1 to System 2 Escalation`. This spec uses the YAML canonical name while preserving the Epic 6 quality standard: the first session must feel near-frictionless and only escalate to deeper commitment after value is felt.

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| Auth-Free Benchmark Rule | Phase3-M07 | Story 6.1 | `BenchmarkRevealGuard` makes teaser reveal a mandatory state transition before any registration, email, or commercial route is eligible. Anonymous session state persists independently from `person_registry`, and `PostRevealOfferProjector` is blocked until `benchmark_revealed_at` exists. |

**Formal onboarding state machine**

| State | Entry Condition | Allowed Next State | Hard Rule |
|---|---|---|---|
| `anonymous_session_created` | Silent Referral link opened | `recording_in_progress` | No identity required |
| `recording_in_progress` | Baseline audit started | `audit_uploaded` or `abandoned` | Only one obvious action is presented |
| `audit_uploaded` | Audio file received and stored | `teaser_processing` | No auth or offer step may appear yet |
| `teaser_processing` | Baseline scoring adapter running | `teaser_revealed` or `processing_failed` | System must prioritize low-latency reveal |
| `teaser_revealed` | Benchmark teaser persisted and shown | `offer_revealed` or `registration_optional` | M-07 satisfied; this is the first moment any commercial or identity ask is allowed |
| `offer_revealed` | Lead Magnet layer surfaced | `registration_optional` | Offer exists only after reveal |
| `registration_optional` | User chooses next step | `identity_linked` or `session_closed_anonymous` | Registration remains optional |
| `identity_linked` | Person record or lead linkage completed | `challenge_handoff_ready` | Referral lineage must be preserved |
| `challenge_handoff_ready` | Post-reveal next step accepted | terminal | Downstream flow may now use registered routes |

**Forbidden transitions**

- `anonymous_session_created -> registration_optional`
- `recording_in_progress -> offer_revealed`
- `audit_uploaded -> registration_optional`
- `teaser_processing -> identity_linked`

Any occurrence of those transitions is a direct M-07 violation.

### 3.5 Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Startapp key | `startapp=onboarding` | Clear separation from all post-entry modes |
| Identity model | Anonymous session first, `person_id` optional later | Prompt explicitly requires no Telegram identity for the audit |
| Baseline scoring | Adapter over `TraitScoringEngine`, not a new scoring engine | Reuses real backend logic while keeping spec within scope |
| Teaser result type | Meaningful benchmark teaser, not full diagnostic dump | Story asks for immediate insight, not a heavy report before trust exists |
| Offer timing | `OfferTierGovernor.evaluate(...)` only after `benchmark_revealed_at` | Prevents commercial leakage before value reveal |
| Registration | Optional and post-reveal only | M-07 is absolute |
| Referral persistence | Separate token table linked before identity | Preserves attribution across anonymous-to-registered transition |
| Challenge handoff | Separate final step after identity linkage | Keeps the initial flow narrowly focused on proof before commitment |

## 4. Implementation Plan

### Phase 1 - Anonymous Session Backbone

| Task ID | Task | Output |
|---|---|---|
| P1-T1 | Register `startapp=onboarding` routes in `main.py` | Mini App becomes addressable and health-reportable |
| P1-T2 | Create `anonymous_onboarding_sessions` and `onboarding_referral_tokens` schema | Canonical anonymous session persistence |
| P1-T3 | Implement `ReferralTokenResolver` | Link tokens to coach/program/source metadata |
| P1-T4 | Implement `AnonymousAuditSessionManager` | Session creation (generates a cryptographic `anonymous_device_nonce` via `os.urandom` to map transient client identity), timeout handling, and state transitions |
| P1-T5 | Emit session-start receipt events | M-07 audit trail begins at first tap |
| P1-T6 | Build health/readiness probes for anonymous session storage | Operational confidence |

### Phase 2 - Baseline Audit and Teaser Reveal

| Task ID | Task | Output |
|---|---|---|
| P2-T1 | Create `anonymous_onboarding_audio_assets` and `anonymous_onboarding_teasers` schema | Recording and teaser persistence |
| P2-T2 | Implement `BaselineAuditRecorder` | 60-second recording contract and upload handling |
| P2-T3 | Implement `AnonymousSignalBundleAdapter` | In-memory minimal bundle for `TraitScoringEngine` |
| P2-T4 | Implement `BaselineTeaserScoringAdapter` | Transforms `list[ScoredTrait]` by selecting the highest-confidence trait for `score_label`, calculating an unweighted average for `benchmark_score`, and mapping the primary trait's coping position to `one_line_insight` and `next_move_hint`. |
| P2-T5 | Implement `BenchmarkRevealGuard` | Hard route/state transition enforcement for M-07 |
| P2-T6 | Add `GET /teaser` route and receipt logging | Immediate anonymous reveal path |

### Phase 3 - Post-Reveal Offer and Registration Link

| Task ID | Task | Output |
|---|---|---|
| P3-T1 | Create `onboarding_offer_impressions` and `anonymous_registration_links` schema | Offer and transition persistence |
| P3-T2 | Implement `PostRevealOfferProjector` | Post-reveal Lead Magnet surface using `OfferTierGovernor.evaluate(...)` by passing `session_id` to the `client_id` parameter and an empty list for historical purchases, preserving anonymity. Output `gate_verdict` maps directly from `OfferTierGovernorRow.verdict`. |
| P3-T3 | Implement `AnonymousRegistrationLinker` | Bridges anonymous session to `person_id` or lead record |
| P3-T4 | Preserve referral attribution across registration | No dropped lineage after identity exists |
| P3-T5 | Add `POST /register` route | Optional identity-link path |
| P3-T6 | Add `GET /offer` route guarded by reveal state | Commercial ask always follows value |

### Phase 4 - Handoff, Safety, and Verification

| Task ID | Task | Output |
|---|---|---|
| P4-T1 | Implement `ChallengeHandoffProjector` | Post-registration next-step bridge |
| P4-T2 | Add optional `ConversionSequenceRouter.route(...)` handoff | Follow-up continuity after consented registration |
| P4-T3 | Integrate `lead_capture_service.py` when group/referral contexts require contact capture | Existing attribution reuse |
| P4-T4 | Integrate `circuit_breaker.py` for crisis or unsafe signals in anonymous audits | Safe escalation halt |
| P4-T5 | Write unit and integration tests | Regression safety |
| P4-T6 | Extend `/health` with onboarding-state and teaser-readiness diagnostics | Deployability confidence |

## 5. Output Schema

All contracts below use Pydantic v2 style and avoid `Any`. They define the onboarding Mini App layer, not the underlying scoring engine.

```python
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class OnboardingState(str, Enum):
    anonymous_session_created = "anonymous_session_created"
    recording_in_progress = "recording_in_progress"
    audit_uploaded = "audit_uploaded"
    teaser_processing = "teaser_processing"
    teaser_revealed = "teaser_revealed"
    offer_revealed = "offer_revealed"
    registration_optional = "registration_optional"
    identity_linked = "identity_linked"
    challenge_handoff_ready = "challenge_handoff_ready"
    processing_failed = "processing_failed"
    abandoned = "abandoned"
    session_closed_anonymous = "session_closed_anonymous"


class ReferralChannel(str, Enum):
    telegram_message = "telegram_message"
    debate_share = "debate_share"
    gallery_share = "gallery_share"
    direct_link = "direct_link"


class AuditUploadStatus(str, Enum):
    pending = "pending"
    uploaded = "uploaded"
    processed = "processed"
    failed = "failed"


class LeadMagnetDecision(str, Enum):
    viewed = "viewed"
    accepted = "accepted"
    dismissed = "dismissed"


class RegistrationMode(str, Enum):
    telegram_link = "telegram_link"
    email_capture = "email_capture"
    phone_capture = "phone_capture"
    skipped = "skipped"


class AnonymousReferralToken(BaseModel):
    referral_token_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    source_artifact_id: str | None = Field(default=None)
    channel: ReferralChannel = Field(...)
    created_at_utc: str = Field(..., min_length=1)


class AnonymousOnboardingSession(BaseModel):
    session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    referral_token_id: str | None = Field(default=None)
    anonymous_device_nonce: str = Field(..., min_length=1)
    benchmark_revealed_at: str | None = Field(default=None)
    linked_person_id: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)
    updated_at_utc: str = Field(..., min_length=1)


class AnonymousAuditAsset(BaseModel):
    audit_asset_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    storage_path: str = Field(..., min_length=1)
    duration_seconds: int = Field(..., ge=1, le=120)
    mime_type: str = Field(..., min_length=1)
    upload_status: AuditUploadStatus = Field(...)
    uploaded_at_utc: str = Field(..., min_length=1)


class BenchmarkTeaserScore(BaseModel):
    teaser_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    benchmark_score: int = Field(..., ge=0, le=100)
    score_label: str = Field(..., min_length=1)
    one_line_insight: str = Field(..., min_length=1)
    next_move_hint: str = Field(..., min_length=1)
    confidence_note: str = Field(..., min_length=1)
    revealed_at_utc: str = Field(..., min_length=1)


class LeadMagnetOfferProjection(BaseModel):
    session_id: str = Field(..., min_length=1)
    client_id_for_governor: str = Field(..., min_length=1)
    offer_tier_ceiling: str = Field(..., min_length=1)
    target_campaign_tier: int = Field(..., ge=1)
    gate_verdict: str = Field(..., min_length=1)
    offer_title: str = Field(..., min_length=1)
    offer_summary: str = Field(..., min_length=1)
    decision: LeadMagnetDecision | None = Field(default=None)


class AnonymousRegistrationLink(BaseModel):
    link_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    registration_mode: RegistrationMode = Field(...)
    person_id: str | None = Field(default=None)
    lead_id: str | None = Field(default=None)
    linked_at_utc: str | None = Field(default=None)


class OnboardingLaunchResponse(BaseModel):
    session: AnonymousOnboardingSession = Field(...)
    allowed_next_action: Literal["record_60s_audit"] = Field(default="record_60s_audit")


class TeaserRevealResponse(BaseModel):
    session_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    teaser: BenchmarkTeaserScore = Field(...)
    auth_required_before_next_step: bool = Field(default=False)


class OfferRevealResponse(BaseModel):
    session_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    teaser_already_revealed: bool = Field(default=True)
    offer: LeadMagnetOfferProjection = Field(...)


class RegistrationRequest(BaseModel):
    registration_mode: RegistrationMode = Field(...)
    telegram_user_id: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)
    first_name: str | None = Field(default=None)


class RegistrationResponse(BaseModel):
    session_id: str = Field(..., min_length=1)
    state: OnboardingState = Field(...)
    link: AnonymousRegistrationLink = Field(...)
    next_action: Literal["challenge_handoff_available", "followup_routing_available"] = Field(...)
```

**Schema notes**

- `auth_required_before_next_step` must remain `False` in `TeaserRevealResponse`.
- `BenchmarkTeaserScore` is intentionally compact. It provides the dopamine hit and immediate meaning without exposing a full diagnostic report before trust exists.
- `linked_person_id` remains nullable until the user explicitly opts into registration.

## 6. Fallback and Failure Handling

### 6.1 Fallback States

| Failure Case | Detection | Fallback Behavior |
|---|---|---|
| referral token invalid or expired | token lookup fails | create a coach-default anonymous session with `channel=direct_link`; do not block entry |
| baseline upload fails | upload or validation error | keep anonymous session alive and let the user retry recording without losing the session |
| teaser processing fails | scoring adapter error | surface a retryable processing error and never redirect to registration as a substitute |
| offer projection fails | `OfferTierGovernor.evaluate(...)` error | keep teaser visible and show a non-blocking “next step unavailable” banner; do not invalidate proof already shown |
| registration link fails | write or identity-link error | preserve anonymous session and teaser state, let the user retry later |
| crisis signal detected | `circuit_breaker.py` trigger | halt automated commercial or challenge follow-up; allow coach review path only |

### 6.2 Circuit Breaker Integration

The onboarding flow must integrate with `src/ccp/core/circuit_breaker.py` after the anonymous audit is transcribed or interpreted enough to detect crisis signals. If triggered:

- the teaser may still be withheld if clinically unsafe to auto-reveal
- Lead Magnet and challenge handoff are blocked
- a receipt is written documenting the safety halt
- the anonymous session enters `processing_failed` or a dedicated safe-hold variant rather than progressing to commercial surfaces

### 6.3 M-07 Fail-Closed Rule

If onboarding logic is uncertain about reveal order, it must fail closed against commercialization, not against proof. The only acceptable emergency behavior is:

- show no offer yet
- keep the teaser path prioritized
- preserve the anonymous session

The system may never decide that registration is a required workaround for a teaser-processing issue.

## 7. Tasks

1. Add the onboarding router to [main.py](/D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
2. Extend [setup_supabase.py](/D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with anonymous onboarding session, audio asset, teaser, link, and offer tables.
3. Create onboarding models in `src/ccp/models/`.
4. Implement `ReferralTokenResolver` for Silent Referral link parsing and attribution.
5. Implement `AnonymousAuditSessionManager` and persist anonymous session lifecycle.
6. Implement `BaselineAuditRecorder` for the 60-second voice capture flow.
7. Implement `AnonymousSignalBundleAdapter` to satisfy the real `SignalBundle` contract in memory.
8. Implement `BaselineTeaserScoringAdapter` on top of [trait_scoring_engine.py](/D:/Work/The Conscious Coaching Factory/src/ccp/services/trait_scoring_engine.py).
9. Implement `BenchmarkRevealGuard` and enforce forbidden transition checks.
10. Implement `PostRevealOfferProjector` using [offer_tier_governor.py](/D:/Work/The Conscious Coaching Factory/src/ccp/services/offer_tier_governor.py) (passing `session_id` as the temporary `client_id`).
11. Implement `AnonymousRegistrationLinker` for optional post-reveal identity linkage.
12. Implement optional follow-up routing through `conversion_sequence_router.py` after identity linkage.
13. Reuse `lead_capture_service.py` where a registered lead record must be created.
14. Add receipt-chain events for session start, audit upload, teaser reveal, offer reveal, registration, and rule violations.
15. Add circuit-breaker checks for unsafe anonymous audit outcomes.
16. Write unit and integration tests matching existing typed scenario patterns.

## 8. Acceptance Criteria

### Story 6.1 - The Audit-to-Challenge Conversion

**AC-6.1-A**

- Given a new client taps a Silent Referral link and enters the Telegram Mini App
- When the onboarding flow begins
- Then the system creates an anonymous onboarding session without requiring Telegram identity, email, or account creation
- And the only primary CTA is the 60-second baseline voice audit
- Mandate ref: Story 6.1, `EXP-FRC-002`
- Failure example: the first screen asks for email, Telegram login, or profile details before the user can record the audit

**AC-6.1-B**

- Given the user completes the baseline audit
- When teaser scoring finishes
- Then the system immediately reveals a meaningful benchmark teaser score inside the anonymous Mini App or chat UI
- And no registration, email verification, or authentication gate is triggered before this reveal
- Mandate ref: Phase3-M07, Story 6.1
- Failure example: the app says “Create your account to view your score” after the user records the 60-second audit

**AC-6.1-C**

- Given a benchmark teaser has been revealed
- When the next commercial step is surfaced
- Then the Lead Magnet layer appears as the natural next step
- And the `OfferTierGovernor.evaluate(...)` path runs only after `benchmark_revealed_at` is set
- Mandate ref: Phase3-M07, PRD-01 free-proof ladder
- Failure example: the offer card is shown before the score, or the offer request is evaluated while the session is still pre-reveal

**AC-6.1-D**

- Given a user chooses to continue after seeing the teaser and Lead Magnet
- When they opt into registration
- Then the system links the anonymous session to a real person or lead record without losing referral attribution or teaser history
- And registration remains optional rather than retroactively required to justify the reveal
- Mandate ref: Story 6.1, `EXP-FRC-002`
- Failure example: the system drops the referral lineage, creates a fresh unrelated session, or claims the teaser cannot be kept unless the user signs up immediately

## 9. Dependencies

| Dependency Type | Name | Why It Matters |
|---|---|---|
| Existing service | `TraitScoringEngine.score_all_traits()` | Required to power the teaser through a real backend scoring path |
| Existing contract | `SignalBundle` from `signal_source_loader.py` | Defines the actual input shape that the anonymous audit adapter must satisfy |
| Existing service | `OfferTierGovernor.evaluate(...)` | Required for post-reveal Lead Magnet governance |
| Existing service | `ConversionSequenceRouter.route(...)` | Optional post-registration follow-up continuity |
| Existing service | `LeadCaptureService.capture_new_member(...)` | Optional lead linkage when user identity becomes available |
| Existing core | `receipt_chain.py` | Immutable proof of M-07 compliance and transition order |
| Existing core | `circuit_breaker.py` | Safety halt on risky anonymous audits |
| Existing database | `asset_registry` / `person_registry` | Audit asset IDs and later person linkage |
| Platform | Telegram Mini App runtime | Required anonymous-first execution surface |
| Cross-system strategy | Silent Referral link ecosystem | Primary traffic source for the first-touch experience |

**Dependency constraints**

- `OfferTierGovernor.evaluate(...)` is downstream of reveal, never upstream.
- `person_registry` linkage is optional and post-reveal only.
- Any future checkout or paid conversion path must remain a later-stage dependency, not part of the first proof reveal.

## 10. Testing Strategy

The testing structure must follow the typed, scenario-first style already used in:

- [test_cpsc_fr52_webinar_brief.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_cpsc_fr52_webinar_brief.py)
- [test_ca11_fr16_studio_block.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_ca11_fr16_studio_block.py)

### 10.1 Unit Tests

| Test Name | Purpose |
|---|---|
| `test_benchmark_reveal_guard_blocks_registration_before_reveal` | Verifies forbidden pre-reveal transitions are rejected |
| `test_anonymous_signal_bundle_adapter_builds_minimal_bundle_for_teaser_scoring` | Verifies the adapter satisfies the real `SignalBundle` contract |
| `test_post_reveal_offer_projector_refuses_to_run_without_benchmark_timestamp` | Verifies offer logic is impossible before teaser reveal |
| `test_anonymous_registration_linker_preserves_referral_token` | Verifies attribution continuity through identity linkage |
| `test_referral_token_resolver_falls_back_to_direct_link_channel` | Verifies invalid tokens do not block entry |

### 10.2 Integration Tests

| Test Name | Purpose |
|---|---|
| `test_anonymous_onboarding_flow_reveals_teaser_before_any_auth_prompt` | End-to-end M-07 compliance for anonymous session, recording, and teaser reveal |
| `test_lead_magnet_offer_surfaces_only_after_teaser_reveal` | End-to-end post-reveal offer sequencing |
| `test_registration_after_reveal_links_person_without_resetting_session_history` | End-to-end anonymous-to-registered transition continuity |

### 10.3 Test Data Requirements

- referral token fixture with coach mapping and silent-referral source metadata
- anonymous session fixture with no `person_id`
- baseline audio upload fixture around 60 seconds
- teaser projection fixture with benchmark score and next-step hint
- offer-governor stub or fixture returning Tier 1 Lead Magnet authorization
- receipt-chain assertions for session start, teaser reveal, offer reveal, and registration events

### 10.4 Mandatory Assertions

Every M-07 integration test must assert all of the following:

- no registration or auth prompt appears before teaser reveal
- `benchmark_revealed_at` is populated before any offer or registration route succeeds
- the offer route rejects pre-reveal requests
- anonymous session state persists through teaser reveal
- referral attribution survives post-reveal identity linkage

### 10.5 Non-Goals for Testing

This spec's tests do not need to:

- retest the internals of FR61 scoring
- benchmark full paid conversion flows
- validate Telegram Payments integration
- exercise downstream challenge content generation after handoff

