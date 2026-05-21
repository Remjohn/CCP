# Tech-Spec: FR-ERA3-19 - Testimonial Builder & User Cards Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 3 - Experience Mini Apps
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new Mini App routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      schema changes extend `src/ccp/scripts/setup_supabase.py`, Section 3 requires cross-spec
                      dependency loading when a feature depends on another Mini App family, and Section 4 requires
                      explicit CBAR enforcement rather than implied compliance.
2. PRD LOADED:        PRD-05 exact brownfield requirement: "Automatically trigger the capture of voice
                      reflections, screenshots, and progress snapshots when benchmark deltas cross success
                      thresholds. Generate public-facing User Cards and branded proof objects from this data."
                      PRD-05 also defines the testimonial trigger events, the real `30-90` second reflection ask,
                      and the User Card tier ladder from Foundation/Bronze through Sovereign/Prismatic.
                      PRD-09 exact brownfield requirement: "Shift all growth loops from explicit 'affiliate links'
                      to Silent Referral: growth happens natively as a byproduct of a coach sharing their scored
                      reaction for votes, debate, or support." PRD-09 also states: "The system should treat
                      fresh-win testimonials as a first-class automation event."
3. EPIC LOADED:       Phase 3 Epic 4 exact FR line: "FR-ERA3-19 (Testimonial Builder & User Cards): The
                      momentum-triggered capture mechanic generating prismatic, status-bearing identity artifacts
                      for the weekly gallery sharing ritual." Story 4.1 first AC: "Given I cross a benchmark
                      threshold or complete a significant challenge layer, When the score is revealed, Then the
                      system initiates the 6-step momentum capture flow, seamlessly extracting my reflection via
                      voice or video."
4. CBAR LOADED:       Phase3-M06 confirmed as a fatal conflict. Exact rewrite demand: "Solo stats can only
                      unlock up to Platinum tier. The Acceptance Criteria must dictate that unlocking the apex
                      'Prismatic' tier strictly requires peer endorsement (e.g., winning a public debate or
                      receiving X votes from the jury)." The audit is explicit that any solo-only Prismatic unlock
                      is a fatal build blocker.
5. PRIMITIVES:        `experience_primitive_id: "EXP-TRG-002"` / `canonical_name: "Hook Cycle Velocity"`
                      `experience_primitive_id: "EXP-SOC-001"` / `canonical_name: "Social Treasures + Group Quests"`
6. BACKEND:           `src/ccp/api/sacred_audio.py` - `async def upload_sacred_audio(file: UploadFile = File(...), coach_acronym: str = "")`
                      `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
                      `src/ccp/services/conversion_sequence_router.py` - `def route(self, *, client_id: str, spt_stage: int | None, hours_since_last_message: float, current_sequence_step: int, next_payload_string: str | None) -> ConversionSequencePayloadRow`
                      `src/ccp/services/lead_capture_service.py` - `def capture_new_member(self, telegram_user_id: int, first_name: str, coach_id: str, stream_id: str, referred_by_user_id: Optional[int] = None) -> LeadCaptureResult`
                      `scorecard_emitter.py` was intentionally excluded because the prompt marks it not relevant.
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, scenario-first
                      class grouping, direct typed assertions, and local async wrappers instead of generic e2e-only
                      smoke tests.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P3_S18_FR-ERA3-19_Testimonial_Builder_User_Cards.md` | 2026-05-11 | Assignment prompt, output target, and fatal M-06 peer-gate constraint |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory stack, route, schema, service, and CBAR requirements |
| 3 | `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | 2026-05-10 | Epic 4 stories, AC, and M-06 enforcement wording |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | 2026-05-10 | Fatal conflict rewrite for Prismatic gating |
| 5 | `docs/prd/modules/PRD_05_CBCS_Law28.md` | v6.0, 2026-05-06 | Testimonial trigger events, capture mechanics, and User Card doctrine |
| 6 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | v6.0, 2026-05-06 | Silent Referral architecture and fresh-win testimonial automation |
| 7 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | Codified registry | Verified timing primitive for immediate capture |
| 8 | `primitives/experience/social_referral/EXP-SOC-001.yaml` | Codified registry | Verified social primitive for Prismatic peer gate |
| 9 | `src/ccp/api/sacred_audio.py` | Existing API | Audio upload pattern and receipt logging boundary |
| 10 | `src/ccp/services/trait_scoring_engine.py` | Existing service | Benchmark scoring and delta-ready evidence source |
| 11 | `src/ccp/services/conversion_sequence_router.py` | Existing service | Silent Referral follow-up routing after consented share |
| 12 | `src/ccp/services/lead_capture_service.py` | Existing service | Downstream attribution pattern when shared artifacts bring in new members |
| 13 | `src/ccp/api/main.py` | 1.0.0 | FastAPI registration and `/health` extension point |
| 14 | `src/ccp/core/receipt_chain.py` | Current | Immutable proof of trigger, capture, consent, gate, and share events |
| 15 | `src/ccp/core/circuit_breaker.py` | Current | Crisis halt and safe fallback rules |
| 16 | `src/ccp/scripts/setup_supabase.py` | Current | Canonical schema extension point |
| 17 | `docs/architecture/april_updates/FR-ERA3-05b_Debate_With_Jury_Tech_Spec.md` | 2026-05-11 draft | Peer-vote and public-debate artifact contract consumed by the Prismatic gate |
| 18 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | 2026-05-11 draft | Reaction artifact and vote-table context for cross-spec endorsement verification |
| 19 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and receipt assertions |
| 20 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async helper pattern and scenario layout |

## 2. Overview

### 2.1 Problem Statement

The product already has the ingredients for transformation proof, but not the orchestration layer that captures it at the right moment and turns it into a socially meaningful artifact. Law28 defines the emotional timing and the identity-bearing User Card. Silent Referral defines why those artifacts matter publicly. The current repo still lacks the Mini App and backend services that make those two ideas operate as one coherent system.

Without that layer, four failures happen:

- testimonials become a separate, manual marketing task instead of a natural byproduct of visible progress
- momentum breaks because capture happens after navigation, delay, or a confirmation step rather than at score reveal
- User Cards can collapse into decorative stat cards with no progression governance
- the apex tier can be incorrectly earned in isolation, which destroys the social physics of Silent Referral

The CBAR audit is explicit that the last failure is fatal. `Prismatic` cannot be the top of a solo grind ladder. It must be conferred by the community through peer-validated proof.

### 2.2 Solution

This spec creates `startapp=testimonial` as a Telegram Mini App for two connected but distinct jobs:

1. momentum-timed capture of breakthrough testimony through a guided voice/video flow
2. weekly projection of public User Cards with a solo progression ladder capped at `Platinum`, plus a separate `PeerEndorsementVerifier` that alone can unlock `Prismatic`

The architecture therefore splits into three cooperating services:

- `MomentumCaptureOrchestrator` for Story 4.1
- `UserCardProgressionEngine` for solo tier calculation through Platinum
- `PeerEndorsementVerifier` for Prismatic eligibility based on debate victories or certified jury votes

Those are intentionally separate. The progression engine is not allowed to introspect raw peer events and silently promote a user. It can only consume a formal peer-verdict output.

### 2.3 Scope

**In scope:**

- `startapp=testimonial` Telegram Mini App shell
- trigger-based capture launches from score reveal or challenge completion
- six-step momentum capture flow with voice/video path
- optional proof attachment support for screenshots or images
- coach/participant permission selection for private, community, or public sharing
- narrative proof assembly for gallery-ready artifacts
- User Card weekly projection with Bronze, Silver, Gold, and Platinum from solo progression
- strict Prismatic lock behind peer verification
- debate/jury endorsement verification as a separate service boundary
- public sharing hooks into Silent Referral routing
- receipt-chain logging and circuit-breaker protections

**Out of scope:**

- rebuilding FR61 biometric scoring internals
- replacing the debate or jury vote mechanics defined in `FR-ERA3-05b`
- using `scorecard_emitter.py` for card progression or capture logic
- generic affiliate dashboards or loud referral mechanics deprecated by PRD-09
- external browser-based checkout or unrelated commercial flows
- a standalone CRM for all gallery recipients

## 3. Context for Development

### 3.1 Architecture Traceability

**Data Exchange Payloads (DEP-IDs)**

| DEP-ID | Schema / Data Object | Source FR | What It Does |
|---|---|---|---|
| DEP-TES-001 | `TestimonialMediaAsset` | FR-ERA3-19 | Normalized asset record for voice, video, or image artifacts |
| DEP-TES-002 | `MomentumTriggerEvent` | Story 4.1 | Event payload describing the win that started the capture flow |
| DEP-TES-003 | `CaptureTagSet` | Story 4.1 | Contextual tags attached to the capture session |
| DEP-TES-004 | `TestimonialCaptureSession` | Story 4.1 | State object for the six-step capture flow |
| DEP-TES-005 | `TransformationProofObject` | Story 4.1 | The final, share-ready narrative artifact |
| DEP-TES-006 | `UserCardMetric` | Story 4.2 | A single stat on the user card |
| DEP-TES-007 | `UserCardSoloProjection` | Story 4.2 | Solo-progression calculation output (capped at Platinum) |
| DEP-TES-008 | `PeerEndorsementEvidence` | Phase3-M06 | The proven debate or vote threshold data |
| DEP-TES-009 | `PeerEndorsementDecision` | Phase3-M06 | The definitive verdict locking or unlocking Prismatic |
| DEP-TES-010 | `UserCardProjection` | Story 4.2 | The fully assembled view state for the card surface |
| DEP-TES-011 | `ShareArtifactRequest` | PRD-09 | Command payload to publish to galleries or feeds |
| DEP-TES-012 | `ShareArtifactResponse` | PRD-09 | Result payload capturing the share receipt and routing status |

**Architectural Components**

| Component | Source FR | What It Does |
|---|---|---|
| `TestimonialMiniAppShell` | FR-ERA3-19 | Standalone Telegram Mini App loaded by `startapp=testimonial` |
| `MomentumTriggerRelay` | Story 4.1 | Receives score-reveal and challenge-completion trigger events without delaying the reveal flow |
| `MomentumCaptureOrchestrator` | Story 4.1 / `EXP-TRG-002` | Starts the six-step capture flow immediately at the win moment |
| `CaptureSessionManager` | Story 4.1 | Manages voice/video capture session lifecycle and resumability |
| `ProofAttachmentCollector` | Story 4.1 | Accepts optional screenshot/image proof objects |
| `ConsentAndVisibilityManager` | Story 4.1 / PRD-05 | Captures private, community, or public sharing permission |
| `TransformationProofAssembler` | Story 4.1 | Assembles voice/video, deltas, proof attachments, and wrapper metadata into a reviewable object |
| `UserCardProgressionEngine` | Story 4.2 | Calculates solo progression tier and card metrics, capped at Platinum |
| `PeerEndorsementVerifier` | Story 4.2 / Phase3-M06 | Separately verifies debate-win or jury-vote eligibility for Prismatic |
| `UserCardProjectionAssembler` | Story 4.2 | Merges solo progression output and peer-verdict output into the final User Card projection |
| `WeeklyCardSnapshotEmitter` | Story 4.2 | Persists weekly card snapshots for gallery and delta comparisons |
| `SilentReferralBridge` | PRD-09 | Routes public-share artifacts into downstream conversion follow-up without changing capture logic |
| `GalleryShareGateway` | Story 4.2 | Publishes consented cards or testimonials into gallery/feed/thread destinations |
| `TestimonialApiBridge` | FR-ERA3-19 | FastAPI routes for trigger intake, capture, consent, card read, and share |
| `TestimonialAuditBridge` | FR-ERA3-19 | Receipt-chain logging for every trigger, upload, consent, gate, and share decision |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | Reuses the existing upload and receipt pattern for voice-capture ingestion. This spec adds a testimonial-specific ingestion layer rather than inventing a separate logging model. |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Consumes `score_all_traits()` and existing score-reveal moments as one class of momentum trigger input. This service is not modified into a card renderer. |
| `conversion_sequence_router.py` | `src/ccp/services/conversion_sequence_router.py` | Consumed only after public/community share to schedule Silent Referral follow-up payloads. It is not the trigger source for the capture flow. |
| `lead_capture_service.py` | `src/ccp/services/lead_capture_service.py` | Used for downstream attribution when testimonial or User Card sharing leads to new member capture; not used for peer endorsement counting. |
| `main.py` | `src/ccp/api/main.py` | Registers the Testimonial Builder router and extends `/health` with Mini App readiness signals. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs trigger issuance, capture completion, consent decisions, peer-gate verdicts, card snapshots, and share publishes. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Halts public publication or live prompt escalation when a capture contains crisis language. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends the canonical schema with testimonial, card, and peer-gate tables. |

**Existing tables consumed:**

- `person_registry` for participant identity and Telegram linkage
- `asset_registry` for capture media, proof attachments, and card asset pointers
- `receipt_chain` for immutable audit logs

**Cross-spec tables consumed when related specs land:**

- `reaction_artifacts` from `FR-ERA3-05-CORE`
- `reaction_votes` from `FR-ERA3-05-CORE` / `FR-ERA3-05b`
- `reaction_debates` from `FR-ERA3-05b`
- `challenge_arena_sessions` and `challenge_arena_weekly_rollups` from `FR-ERA3-11`

**New testimonial tables introduced by this spec:**

- `testimonial_capture_sessions` - one row per triggered or manual capture flow
- `testimonial_media_assets` - normalized rows for uploaded voice/video/image artifacts
- `testimonial_proof_objects` - assembled narrative proof packets plus consent status
- `user_card_snapshots` - weekly user card projections and rendered asset pointers
- `peer_endorsement_verdicts` - separate, authoritative Prismatic gate decisions
- `peer_endorsement_policies` - program/community policy rows with vote thresholds and accepted endorsement pathways
- `community_peer_certifications` - who counts as a certified peer or juror for Prismatic gating
- `testimonial_share_events` - gallery/feed/thread publication records and downstream routing status

**Existing API routes extended or called:**

- `POST /api/sacred-audio/upload` - voice testimony ingestion pattern reused for audio capture
- `GET /health` - extended with testimonial capture and card-readiness state

**New API routes introduced by this spec:**

- `POST /api/testimonial/triggers` - ingest a momentum trigger event
- `GET /api/testimonial/capture/{capture_session_id}` - load current capture state
- `POST /api/testimonial/capture/{capture_session_id}/recording` - submit voice or video reflection metadata
- `POST /api/testimonial/capture/{capture_session_id}/attachments` - upload optional screenshot/image proof
- `POST /api/testimonial/capture/{capture_session_id}/consent` - store private/community/public permission
- `POST /api/testimonial/capture/{capture_session_id}/finalize` - assemble proof object
- `GET /api/testimonial/cards/{person_id}/current` - fetch current User Card projection
- `GET /api/testimonial/cards/{person_id}/history` - fetch historical weekly snapshots
- `POST /api/testimonial/cards/{person_id}/share` - publish card or proof artifact to approved destinations
- `GET /api/testimonial/peer-gate/{person_id}` - fetch the current peer-verdict state

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-TRG-002` | Hook Cycle Velocity | trigger_timing | Capture must begin at the reveal moment, not after a modal, delay, or route change. The score-reveal surface must already hold the session token needed to open the capture flow. |
| `EXP-SOC-001` | Social Treasures + Group Quests | social_referral | The apex User Card tier must be community-conferred. Solo behavior can build status up to Platinum, but social endorsement alone can unlock Prismatic. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| Peer-Gated Apex Rule | Phase3-M06 | Story 4.2 | `UserCardProgressionEngine` is hard-capped at `Platinum`. `PeerEndorsementVerifier` independently evaluates debate wins or certified jury-vote thresholds and emits a separate verdict. `UserCardProjectionAssembler` may render `Prismatic` only if the verifier returns `unlocked`. |

**Formal separation between progression and peer gate**

| Layer | Allowed Inputs | Forbidden Inputs | Output |
|---|---|---|---|
| `UserCardProgressionEngine` | streak count, weekly deltas, primary stats, CBCS layer status, strongest primitive | jury votes, debate win flags, manual coach override to Prismatic | `solo_tier`, stats projection |
| `PeerEndorsementVerifier` | `reaction_debates`, `reaction_votes`, `community_peer_certifications` (requires exactly 3 certified jury votes) | raw streak count, solo scores, local-only practice sessions | `peer_gate_verdict`, `evidence_type`, `evidence_id`, `threshold_progress` |
| `UserCardProjectionAssembler` | outputs from both services | bypassing either service | final render tier and card asset payload |

**Non-negotiable M-06 invariants**

- `Prismatic` can never be set directly by `UserCardProgressionEngine`
- reaching `Sovereign`-level solo metrics still renders `Platinum` until peer verification passes
- uncertified jury votes do not count toward the Prismatic threshold
- a debate artifact counts only if it is published and has a valid winner state under the Debate spec
- if peer verification is unavailable, the system must stay at `PlatinumLocked` rather than fail open

### 3.5 Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Mini App scope | One app with capture flow plus card/gallery surfaces | Both features share the same emotional moment and artifact lineage |
| Capture trigger timing | Pre-issued launch token on score reveal | Satisfies `EXP-TRG-002` by preventing a later navigation delay |
| Capture steps | Six app-facing steps after trigger, with consent embedded in the final review stage | Aligns Epic 4's 6-step wording with PRD-05's more detailed capture mechanics |
| User Card tier mapping | Solo ladder uses Law28 layer semantics mapped to Bronze/Silver/Gold/Platinum; Prismatic remains peer-gated | Source-backed from PRD-05 and avoids arbitrary thresholds |
| Apex gate architecture | Separate verifier service and verdict table | Required by Phase3-M06 and prevents hidden coupling |
| Peer-verification sources | debate victory or certified-juror vote threshold only | Matches Epic 4 and CBAR wording |
| `scorecard_emitter.py` usage | Explicitly excluded | The prompt marks it as not relevant, and it would blur score reflection with identity artifact generation |
| Voice/video ingestion | Reuse sacred-audio patterns for voice and add testimonial-video ingestion alongside it | Preserves asset and receipt consistency |
| Silent Referral bridge | Trigger only after consented share | Prevents referral routing from polluting the capture or progression engines |

## 4. Implementation Plan

### Phase 1 - Trigger and Capture Session Backbone

| Task ID | Task | Output |
|---|---|---|
| P1-T1 | Register `startapp=testimonial` router in `main.py` | Mini App becomes addressable and health-reportable |
| P1-T2 | Create `testimonial_capture_sessions` and `testimonial_media_assets` in `setup_supabase.py` | Canonical session and media persistence |
| P1-T3 | Implement `MomentumTriggerRelay` | Trigger intake from score reveals, challenge completions, streak milestones, and public-recognition events |
| P1-T4 | Implement `CaptureSessionManager` | Session tokens, resumability, and current-step tracking |
| P1-T5 | Implement `MomentumCaptureOrchestrator` | Immediate launch behavior at the reveal moment |
| P1-T6 | Emit trigger and session creation receipts | Audit trail for timing and launch integrity |

### Phase 2 - Proof Assembly and Consent

| Task ID | Task | Output |
|---|---|---|
| P2-T1 | Add voice capture endpoint reusing `sacred_audio.py` patterns | Typed voice-reflection ingestion |
| P2-T2 | Add testimonial video upload path | First-class video selfie support |
| P2-T3 | Implement `ProofAttachmentCollector` | Screenshot/image attachment support |
| P2-T4 | Implement `TransformationProofAssembler` | Reviewable proof object with deltas, trigger context, and assets. Includes an explicit LLM zero-shot prompt contract: "Generate a 1-sentence narrative_summary and a 3-word delta_headline focusing solely on the verified benchmark delta, using no hallucinated praise" |
| P2-T5 | Implement `ConsentAndVisibilityManager` | Private/community/public permission state |
| P2-T6 | Create `testimonial_proof_objects` and `testimonial_share_events` schema | Durable proof-object and sharing ledger |

### Phase 3 - User Card Progression and Peer Verification

| Task ID | Task | Output |
|---|---|---|
| P3-T1 | Create `user_card_snapshots`, `peer_endorsement_policies`, `community_peer_certifications`, and `peer_endorsement_verdicts` tables | Deterministic tiering and policy storage |
| P3-T2 | Implement `UserCardProgressionEngine` | Bronze through Platinum solo projection |
| P3-T3 | Implement `PeerEndorsementVerifier` | Debate/jury-based Prismatic verdict service. Generates `locked_message` using static interpolation (e.g., "Prismatic requires 3 certified peer endorsements. You have {current}.") |
| P3-T4 | Implement `UserCardProjectionAssembler` | Final card view composed from separate service outputs. Sets `prismatic_gate_copy` to static string: "Win a debate or earn 3 jury votes to unlock Prismatic." |
| P3-T5 | Implement `WeeklyCardSnapshotEmitter` | Historical snapshots and weekly delta persistence |
| P3-T6 | Emit peer-gate verdict receipts | Auditable proof of every lock/unlock decision |

### Phase 4 - Sharing, Silent Referral, and Fallbacks

| Task ID | Task | Output |
|---|---|---|
| P4-T1 | Implement `GalleryShareGateway` | Publishes approved artifacts to gallery/feed/thread destinations |
| P4-T2 | Implement `SilentReferralBridge` | Post-share routing into `conversion_sequence_router.py` |
| P4-T3 | Add `lead_capture_service.py` attribution hooks | Tracks referred new members from shared proof objects |
| P4-T4 | Integrate `circuit_breaker.py` checks before public publish | Crisis-safe publication rules |
| P4-T5 | Extend `/health` with capture, card, and peer-gate readiness | Operational visibility |
| P4-T6 | Write unit and integration tests | Regression-safe implementation |

## 5. Output Schema

All new contracts below use Pydantic v2 style and avoid `Any`. File placement may span `src/ccp/models/` plus request/response DTO modules.

```python
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class MomentumTriggerKind(str, Enum):
    benchmark_delta = "benchmark_delta"
    challenge_completion = "challenge_completion"
    streak_milestone = "streak_milestone"
    public_recognition = "public_recognition"
    coach_flagged_breakthrough = "coach_flagged_breakthrough"
    first_win_tier_boundary = "first_win_tier_boundary"


class CaptureMediaMode(str, Enum):
    voice = "voice"
    video = "video"


class CaptureStep(str, Enum):
    warm_prompt = "warm_prompt"
    reflection_record = "reflection_record"
    optional_attachment = "optional_attachment"
    metadata_tagging = "metadata_tagging"
    proof_review = "proof_review"
    consent_decision = "consent_decision"


class ConsentLevel(str, Enum):
    private_archive = "private_archive"
    close_community = "close_community"
    public_share = "public_share"


class UserCardTier(str, Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"
    prismatic = "prismatic"


class PeerGateVerdict(str, Enum):
    locked = "locked"
    pending = "pending"
    unlocked = "unlocked"
    unavailable = "unavailable"


class PeerEvidenceType(str, Enum):
    debate_victory = "debate_victory"
    certified_jury_votes = "certified_jury_votes"


class ShareDestination(str, Enum):
    community_gallery = "community_gallery"
    telegram_feed = "telegram_feed"
    accountability_thread = "accountability_thread"


class CaptureSessionStatus(str, Enum):
    triggered = "triggered"
    in_progress = "in_progress"
    awaiting_review = "awaiting_review"
    awaiting_consent = "awaiting_consent"
    finalized = "finalized"
    shared = "shared"
    blocked = "blocked"


class TestimonialMediaAsset(BaseModel):
    """DEP-TES-001"""
    asset_id: str = Field(..., min_length=1)
    asset_type: Literal["audio", "video", "image"] = Field(...)
    storage_path: str = Field(..., min_length=1)
    duration_seconds: int | None = Field(default=None, ge=1)
    mime_type: str = Field(..., min_length=1)


class MomentumTriggerEvent(BaseModel):
    """DEP-TES-002"""
    trigger_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    trigger_kind: MomentumTriggerKind = Field(...)
    trigger_source: str = Field(..., min_length=1)
    score_before: float | None = Field(default=None, ge=0)
    score_after: float | None = Field(default=None, ge=0)
    delta_value: float | None = Field(default=None)
    streak_count: int | None = Field(default=None, ge=0)
    challenge_layer: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)


class CaptureTagSet(BaseModel):
    """DEP-TES-003"""
    trigger_kind: MomentumTriggerKind = Field(...)
    program_week: int | None = Field(default=None, ge=0)
    emotional_state: str = Field(..., min_length=1)
    strongest_primitive_id: str | None = Field(default=None)
    benchmark_delta_summary: str | None = Field(default=None)
    active_layer_label: str | None = Field(default=None)


class TestimonialCaptureSession(BaseModel):
    """DEP-TES-004"""
    capture_session_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    trigger: MomentumTriggerEvent = Field(...)
    preferred_media_mode: CaptureMediaMode = Field(...)
    status: CaptureSessionStatus = Field(...)
    current_step: CaptureStep = Field(...)
    reflection_text_transcript: str | None = Field(default=None)
    primary_media_asset_id: str | None = Field(default=None)
    attachment_asset_ids: list[str] = Field(default_factory=list)
    tags: CaptureTagSet | None = Field(default=None)
    consent_level: ConsentLevel | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)
    updated_at_utc: str = Field(..., min_length=1)


class TransformationProofObject(BaseModel):
    """DEP-TES-005"""
    proof_object_id: str = Field(..., min_length=1)
    capture_session_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    narrative_summary: str = Field(..., min_length=1)
    primary_media_asset_id: str = Field(..., min_length=1)
    attachment_asset_ids: list[str] = Field(default_factory=list)
    consent_level: ConsentLevel = Field(...)
    trigger_kind: MomentumTriggerKind = Field(...)
    delta_headline: str | None = Field(default=None)
    share_ready: bool = Field(default=False)
    created_at_utc: str = Field(..., min_length=1)


class UserCardMetric(BaseModel):
    """DEP-TES-006"""
    metric_key: str = Field(..., min_length=1)
    current_value: float = Field(..., ge=0)
    delta_value: float = Field(...)
    display_label: str = Field(..., min_length=1)


class UserCardSoloProjection(BaseModel):
    """DEP-TES-007"""
    snapshot_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    weekly_period_key: str = Field(..., min_length=1)
    solo_tier: UserCardTier = Field(...)
    strongest_primitive_id: str | None = Field(default=None)
    streak_count: int = Field(..., ge=0)
    metrics: list[UserCardMetric] = Field(default_factory=list)
    created_at_utc: str = Field(..., min_length=1)


class PeerEndorsementEvidence(BaseModel):
    """DEP-TES-008"""
    evidence_type: PeerEvidenceType = Field(...)
    evidence_id: str = Field(..., min_length=1)
    certified_peer_count: int = Field(..., ge=0)
    threshold_required: int = Field(..., ge=1)
    evidence_summary: str = Field(..., min_length=1)


class PeerEndorsementDecision(BaseModel):
    """DEP-TES-009"""
    verdict_id: str = Field(..., min_length=1)
    person_id: str = Field(..., min_length=1)
    verdict: PeerGateVerdict = Field(...)
    evidence: PeerEndorsementEvidence | None = Field(default=None)
    rationale: str = Field(..., min_length=1)
    locked_message: str | None = Field(default=None)
    decided_at_utc: str = Field(..., min_length=1)


class UserCardProjection(BaseModel):
    """DEP-TES-010"""
    person_id: str = Field(..., min_length=1)
    public_tier: UserCardTier = Field(...)
    solo_projection: UserCardSoloProjection = Field(...)
    peer_decision: PeerEndorsementDecision = Field(...)
    avatar_asset_id: str | None = Field(default=None)
    profile_name: str = Field(..., min_length=1)
    program_identity: str = Field(..., min_length=1)
    card_asset_id: str | None = Field(default=None)
    prismatic_gate_copy: str = Field(..., min_length=1)


class ShareArtifactRequest(BaseModel):
    """DEP-TES-011"""
    artifact_kind: Literal["proof_object", "user_card"] = Field(...)
    artifact_id: str = Field(..., min_length=1)
    destinations: list[ShareDestination] = Field(..., min_length=1)


class ShareArtifactResponse(BaseModel):
    """DEP-TES-012"""
    share_event_id: str = Field(..., min_length=1)
    artifact_kind: Literal["proof_object", "user_card"] = Field(...)
    artifact_id: str = Field(..., min_length=1)
    published_destinations: list[ShareDestination] = Field(default_factory=list)
    silent_referral_routed: bool = Field(default=False)
    receipt_id: str = Field(..., min_length=1)
```

**Schema notes**

- `UserCardSoloProjection.solo_tier` is allowed to be at most `platinum`. The final `public_tier` is the only field that may become `prismatic`, and only through `PeerEndorsementDecision.verdict == unlocked`.
- `threshold_required` is policy-driven but structurally constrained. The Prismatic gate requires exactly 3 certified jury votes (or 1 verified debate victory) per the CBAR exact-numeric mandate.
- `artifact_kind="proof_object"` and `artifact_kind="user_card"` share the same publish ledger so Silent Referral downstream logic can treat them as different surfaces of the same proof economy.

## 6. Fallback and Failure Handling

The Testimonial Builder must integrate with `src/ccp/core/circuit_breaker.py` and fail closed on public-risk or peer-gate ambiguity.

### 6.1 Fallback States

| Failure Case | Detection | Fallback Behavior |
|---|---|---|
| trigger arrives but capture session cannot be created | DB or route failure | reveal surface still shows success state, but a retryable capture banner appears immediately with the same trigger token |
| voice/video upload fails | storage or validation error | keep session alive, preserve prior steps, and allow re-upload without discarding the trigger context |
| optional attachment upload fails | image upload issue | do not block proof assembly; mark attachment optional and continue |
| proof assembly fails | missing primary media or transcript | session remains `awaiting_review`; no share options exposed |
| peer-verification service unavailable | verifier timeout or dependency missing | keep card at `Platinum` or lower with `peer_gate_verdict=unavailable`; never fail open to `Prismatic` |
| public share route fails | Telegram/gallery publish error | keep artifact finalized and consented, mark share event retryable |
| crisis language detected in reflection | `circuit_breaker.py` trip | block public/community share and move session to `blocked` until coach review |

### 6.2 Circuit Breaker Integration

The Circuit Breaker must be checked before:

- converting a finalized proof object from private to community/public
- publishing a User Card to public destinations
- routing a shared artifact into Silent Referral follow-up automation

If the breaker is active, the system must:

- preserve the capture and proof object privately
- block publication and downstream referral routing
- emit a receipt entry documenting the halt reason
- surface coach-review-required messaging instead of an ambiguous publish error

### 6.3 M-06 Fail-Closed Rule

If `PeerEndorsementVerifier` cannot produce a valid verdict, the user remains locked below `Prismatic`. The only acceptable fallback states are:

- `locked`
- `pending`
- `unavailable`

`Prismatic` is never the fallback.

## 7. Tasks

1. Add the `startapp=testimonial` router to [main.py](/D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
2. Extend [setup_supabase.py](/D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with testimonial, card, certification, policy, verdict, and share tables.
3. Create testimonial and user-card domain models in `src/ccp/models/`.
4. Implement `MomentumTriggerRelay` for benchmark, challenge, streak, recognition, and first-win trigger inputs.
5. Implement `CaptureSessionManager` with six-step state tracking and resume support.
6. Implement voice ingestion using the [sacred_audio.py](/D:/Work/The Conscious Coaching Factory/src/ccp/api/sacred_audio.py) asset and receipt pattern.
7. Add testimonial video ingestion and typed metadata validation.
8. Implement `TransformationProofAssembler` and persist `testimonial_proof_objects`.
9. Implement `ConsentAndVisibilityManager` and enforce private/community/public visibility decisions.
10. Implement `UserCardProgressionEngine` with Bronze, Silver, Gold, and Platinum outputs only.
11. Implement `PeerEndorsementVerifier` against `reaction_debates`, `reaction_votes`, and `community_peer_certifications`.
12. Implement `UserCardProjectionAssembler` to merge solo projection and peer verdict into the final card payload.
13. Implement `WeeklyCardSnapshotEmitter` for weekly history and delta arrows.
14. Implement `GalleryShareGateway` for gallery, Telegram feed, and accountability-thread publishing.
15. Implement `SilentReferralBridge` to call `conversion_sequence_router.route(...)` after consented public/community shares.
16. Integrate `lead_capture_service.py` attribution hooks for referred new members.
17. Add receipt-chain events for trigger, upload, consent, verdict, card snapshot, and share.
18. Add circuit-breaker checks before all community/public publish flows.
19. Extend `/health` with testimonial capture readiness, peer-gate readiness, and silent-referral bridge readiness.
20. Write unit and integration tests matching existing typed scenario patterns.

## 8. Acceptance Criteria

### Story 4.1 - Momentum-Triggered Capture Flow

**AC-4.1-A**

- Given a participant crosses a benchmark threshold or completes a significant challenge layer
- When the score is revealed
- Then the system creates or resolves a `testimonial_capture_session` and opens the six-step capture flow immediately from that reveal surface
- And the flow begins without an intermediate confirmation modal, page hop, or delayed background poll
- Mandate ref: Story 4.1, `EXP-TRG-002`
- Failure example: the score reveal closes, the participant returns to a dashboard, and only later receives a generic “leave a testimonial?” prompt after the emotional peak is gone

**AC-4.1-B**

- Given a valid momentum trigger has fired
- When the participant completes the capture flow
- Then the system supports a `30-90` second voice or video reflection
- And it optionally accepts screenshot/image proof
- And it stores trigger type, benchmark delta, week context, emotional state, and active primitive context on the proof object
- Mandate ref: Story 4.1, PRD-05 capture mechanics
- Failure example: the system collects only a bare media blob with no win context, no delta, and no attachment pathway

**AC-4.1-C**

- Given a proof object is assembled
- When the participant reaches the final review stage
- Then they must choose one of `private_archive`, `close_community`, or `public_share`
- And no public/community publication may occur before that explicit consent is stored
- Mandate ref: Story 4.1, PRD-05 permission surface
- Failure example: the system auto-posts a fresh-win video into a gallery just because the capture flow completed

### Story 4.2 - Prismatic User Card Progression

**AC-4.2-A**

- Given a participant has weekly performance stats and streak data
- When their weekly card snapshot is updated
- Then `UserCardProgressionEngine` renders Bronze, Silver, Gold, or Platinum based on solo progression inputs
- And it includes avatar, tier badge, primary stats, weekly delta arrows, streak counter, and strongest primitive when available
- Mandate ref: Story 4.2, PRD-05 User Card doctrine
- Failure example: the card is just a generic badge with a score number and no delta arrows, no streak, and no identity-bearing fields

**AC-4.2-B**

- Given a participant has reached the maximum solo progression state
- When `UserCardProgressionEngine` runs without a verified peer-gate verdict
- Then the highest public tier it may output is `Platinum`
- And `Prismatic` remains locked with explicit gate copy explaining the peer requirement
- Mandate ref: Phase3-M06, `EXP-SOC-001`
- Failure example: a participant grinds solo for enough weeks and silently receives a `Prismatic` card without any debate win or certified jury endorsement

**AC-4.2-C**

- Given a participant has either won a valid public debate judged by peers or reached the configured threshold of certified jury votes
- When `PeerEndorsementVerifier` runs
- Then it emits `verdict=unlocked` with evidence metadata naming the verified debate or vote threshold event
- And only then may `UserCardProjectionAssembler` render `public_tier=prismatic`
- Mandate ref: Phase3-M06, Story 4.2
- Failure example: the frontend flips to `Prismatic` based on an optimistic local flag while the backend has no durable peer-verdict row

**AC-4.2-D**

- Given a participant is below Prismatic
- When they view their current card
- Then the UI clearly communicates the future peer-gate requirement before or at Platinum
- And the copy names the accepted pathways: peer-judged debate victory or threshold certified jury votes
- Mandate ref: Story 4.2, Phase3-M06
- Failure example: the Prismatic gate appears only after the participant expects an upgrade, making the rule feel arbitrary and retroactive

## 9. Dependencies

| Dependency Type | Name | Why It Matters |
|---|---|---|
| Existing API | `POST /api/sacred-audio/upload` | Proven pattern for asset ingest plus receipt logging |
| Existing service | `TraitScoringEngine.score_all_traits()` | One evidence source for benchmark threshold and stat updates |
| Existing service | `ConversionSequenceRouter.route(...)` | Silent Referral follow-up after consented share |
| Existing service | `LeadCaptureService.capture_new_member(...)` | Attribution when shared proof brings in new participants |
| Cross-system core | `receipt_chain.py` | Required for durable trigger, consent, gate, and share audit |
| Cross-system core | `circuit_breaker.py` | Required to block risky publication |
| Cross-spec contract | `FR-ERA3-05-CORE` reaction artifacts and vote tables | Provides juror-vote evidence surface |
| Cross-spec contract | `FR-ERA3-05b` debate winner state and jury vote semantics | Provides debate-victory evidence for Prismatic |
| Cross-spec contract | `FR-ERA3-11` challenge completion and weekly rollups | Provides one trigger source and weekly stat context |
| Existing storage | Supabase buckets and `asset_registry` | Persistent media/card asset addressing |
| Platform | Telegram Mini App runtime | Launches the capture flow and card surfaces inline |

**Dependency constraints**

- `PeerEndorsementVerifier` may consume reaction/debate evidence, but it may not infer endorsement from private practice artifacts.
- `UserCardProgressionEngine` may consume weekly stats and layer state, but it may not query raw jury votes.
- `SilentReferralBridge` runs only after a consented share and may not back-propagate into tier calculation.

## 10. Testing Strategy

The test structure must follow the typed, scenario-first style already used in:

- [test_cpsc_fr52_webinar_brief.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_cpsc_fr52_webinar_brief.py)
- [test_ca11_fr16_studio_block.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_ca11_fr16_studio_block.py)

### 10.1 Unit Tests

| Test Name | Purpose |
|---|---|
| `test_momentum_capture_orchestrator_issues_session_at_score_reveal` | Verifies capture session creation happens on the reveal event, not after a later navigation |
| `test_user_card_progression_engine_caps_solo_tier_at_platinum` | Verifies solo progression never returns `prismatic` under any input combination |
| `test_peer_endorsement_verifier_unlocks_prismatic_from_debate_victory` | Verifies a valid debate-win evidence packet returns `verdict=unlocked` |
| `test_peer_endorsement_verifier_rejects_uncertified_jury_votes` | Verifies uncertified voters cannot satisfy the Prismatic threshold |
| `test_user_card_projection_assembler_requires_peer_verdict_before_prismatic` | Verifies final render tier remains below `prismatic` without a valid verifier result |

### 10.2 Integration Tests

| Test Name | Purpose |
|---|---|
| `test_triggered_capture_flow_launches_from_score_reveal_without_modal_delay` | End-to-end Story 4.1 timing contract for trigger, session creation, and immediate launch |
| `test_testimonial_finalize_respects_consent_before_public_share` | End-to-end proof assembly and visibility enforcement |
| `test_prismatic_unlock_requires_separate_peer_verdict_row` | End-to-end M-06 enforcement proving solo stats alone cannot unlock Prismatic |

### 10.3 Test Data Requirements

- participant fixture with person registry identity and avatar asset
- trigger fixtures for benchmark delta, challenge completion, and first-win tier boundary
- media upload fixtures for one audio and one video path
- reaction/debate fixtures with certified juror identities and both passing/failing vote thresholds
- weekly stats fixture with streak count, delta arrows, and strongest primitive data
- receipt-chain assertions for trigger issuance, consent storage, verdict emission, and share publication

### 10.4 Mandatory Assertions

Every M-06 integration test must assert all of the following:

- `UserCardProgressionEngine` output tier is never `prismatic`
- final `public_tier` becomes `prismatic` only when `PeerEndorsementDecision.verdict == unlocked`
- uncertified votes do not count toward the threshold
- absence of a verdict row or verifier outage leaves the user at `Platinum` or below
- receipt chain contains a gate decision event with the evidence type and rationale

### 10.5 Non-Goals for Testing

This spec's tests do not need to:

- re-test the internal scoring logic of FR61
- re-test debate composition rendering beyond consuming winner/vote outcomes as dependency fixtures
- exercise full commercial checkout flows from PRD-09
- validate manual affiliate or loud referral systems, which are obsolete by architecture

