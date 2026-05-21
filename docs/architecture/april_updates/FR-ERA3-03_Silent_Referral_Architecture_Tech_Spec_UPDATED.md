# PRE-WORK LOG

<!-- UPDATED: Added Wave 0/1 SDA source validation and proof of the original share/proof governance gap. -->

1. **Protocol (`ERA3_Tech_Spec_Writing_Protocol.md`)**: Read §2 (backend architecture), §3 (Pre-Flight), §4 (Format).
2. **PRD Modules (`PRD_09_CPSC_Silent_Referral.md`)**: "Silent Referral is not 'affiliate without the word affiliate.' It is a product architecture where value creates participation, participation creates shareable objects, shareable objects create social invitations, and social invitations create new product entry." (PRD-09 §5.1)
3. **Phase Epic (`Phase5_Growth_Epics.md`)**: First AC Quoted: "*Given* a user achieves a high score, completes a challenge layer, or records a powerful Conscious Reaction, *When* the artifact is processed, *Then* the system generates a branded, status-bearing link (e.g., a Prismatic User Card) that: Includes a backend-verifiable cryptographic hash binding the specific session ID, timestamp, and biometric data that generated the score."
4. **CBAR Audit (`CBAR_Audit_Phase5_Growth.md`)**: Confirmed mandates "The Verifiable Artifact Rule" and "The Earned Escalation Rule" and applied corrections for the hallucinated primitive EXP-TRG-005.
5. **Primitives (`primitives/experience/`)**: 
   - `id: "EXP-SOC-001"`, `name: "Social Treasures + Group Quests"`
   - `id: "EXP-TRG-005"`, `name: "First Major Win-State"`
6. **Backend Python Files**: 
   - `conversion_sequence_router.py`: `def evaluate(self) -> DormancyGateVerdict:`
   - `lead_capture_service.py`: `async def insert_lead(self, lead: dict[str, Any]) -> str:`
   - `offer_tier_governor.py`: `def resolve(self) -> tuple[int, OfferTierCeiling]:`
7. **Test Files (`tests/integration/`)**: Read `test_cpsc_fr51_challenge_funnel.py`. Noted class-based grouping (`TestCommitmentDeviceGate`), `ReceiptChain` integration, and `pytest.raises` for testing failure modes and boundary edge cases. Section 10 tests match this established pattern exactly.
8. **Exact Gap Proof from the Existing Spec**: Re-read the baseline `FR-ERA3-03_Silent_Referral_Architecture_Tech_Spec.md` and confirmed that Section 2 currently packages user successes into "cryptographically verifiable social objects" and the Phase 5 story excerpt names a "branded, status-bearing link (e.g., a Prismatic User Card)." Those lines correctly govern proof authenticity and earned escalation, but they do not yet distinguish healthy trust transfer from prestige theater or define SDA controls for status-bearing proof objects.
9. **Wave 0 PRD Alignment**:
   - `PRD_09_CPSC_Silent_Referral.md`: Re-read the new `5.3A Relationship to the Semantic Discernment Architecture` and `1.4 SDA-Aware Trust Transfer and Commercial Integrity` sections. These now require the system to distinguish healthy authority from prestige theater, proof from vanity, belonging from social capture, and urgency from coercion.
   - `PRD_06_Conscious_Reactions.md`: Re-read the new `5.3A Relationship to the Semantic Discernment Architecture` section because many referral artifacts originate from reaction outcomes and therefore inherit status / belonging / authority / shame / redemption risks.
10. **Mandatory SDA Source Set**:
   - `lab/semantic_discernment_architecture_content_engine_v_1.md`
   - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
   - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
   - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`
11. **Wave 1 SDA Tech Specs**:
   - `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
   - `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
   - `FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`
   These were read to keep ontology ownership, crosswalk access, and directional-integrity decisions outside Silent Referral itself.

---

# Tech Spec: FR-ERA3-03 — Silent Referral Architecture

## 1. Files Read
- `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
- `docs/architecture/april_updates/Phase5_Growth_Epics.md`
- `docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md`
- `primitives/experience/social_referral/EXP-SOC-001.yaml`
- `primitives/experience/trigger_timing/EXP-TRG-005.yaml`
- `src/ccp/services/conversion_sequence_router.py`
- `src/ccp/services/lead_capture_service.py`
- `src/ccp/services/offer_tier_governor.py`
- `tests/integration/test_cpsc_fr51_challenge_funnel.py`
- `docs/architecture/april_updates/FR-ERA3-03_Silent_Referral_Architecture_Tech_Spec.md`
- `docs/prd/modules/PRD_06_Conscious_Reactions.md`
- `lab/semantic_discernment_architecture_content_engine_v_1.md`
- `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`
- `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`

## 2. Overview
<!-- UPDATED: Added explicit trust-transfer vs prestige-theater governance for status-bearing referral artifacts. -->
The Silent Referral Architecture (FR-ERA3-03) defines the mechanism that turns authentic user participation into a powerful, frictionless acquisition channel. Rather than relying on transactional "refer-a-friend" affiliate requests that deplete social capital, this architecture packages user successes (e.g., Debate victories, High Reaction scores) into cryptographically verifiable social objects (User Cards). These objects act as organic invitations. 

When peers engage with a shared User Card to vote or offer feedback, they are subsequently introduced to the CCP ecosystem through an Ephemeral Win-State, earning their progression to their own recording actions. This guarantees that all platform growth is a byproduct of high-fidelity social verification, firmly protected against spoofing and spam.

This revised specification preserves that architecture but adds the missing SDA governance layer. Silent Referral now treats every shareable proof object as a **status-bearing semantic artifact**, not merely a conversion asset. A card can therefore be factually valid and still be directionally wrong if it drifts into prestige theater, vanity proof, coercive urgency, manipulative belonging, or superiority signaling.

The governing distinction is now explicit:
- **Healthy trust transfer**: a proof surface communicates earned authority, truthful transformation, invitational belonging, and authentic performance without coercive social pressure.
- **Prestige theater**: a proof surface still looks premium and credible, but its semantic force comes mainly from vanity display, exclusionary status extraction, synthetic superiority, or compulsive comparison.

As a result, this updated architecture adds representation-geometry governance, directional-integrity release gates, hard-negative rejection, and referral-loop feedback controls before a status-bearing artifact can be rendered, signed, escalated, or amplified.

## 3. Context for Development

### 3.1 DEP-IDs Traceability
| Dependency ID | Description | Resolution Strategy |
| --- | --- | --- |
| DEP-ENG-023 | 7-layer Cultural Memory Map | Captured leads inherit relevant CMM layers for immediate personalization. |
| DEP-ENG-045 | Context Performance Registry | Silent referral outcomes are tracked for context performance metrics. |
| DEP-SEC-011 | Cryptographic Object Binding | SHA-256 HMAC of biometric data + session_id for all generated User Cards. |
| DEP-SLA-004 | Sub-second Mini App Load | Pre-generated sharing states injected directly into Telegram Mini App SDK. |
| DEP-SDA-020 | SDA Ontology + Registry | Canonical existential invariants, representation geometries, archetypal geometries, and grammar references are resolved through `FR-ERA3-20`. |
| DEP-SDA-021 | SDA Query + Crosswalk Service | Primitive-to-invariant and archetype-to-geometry lookups are resolved through `FR-ERA3-21` instead of local heuristics. |
| DEP-SDA-022 | Directional Integrity Engine | Every status-bearing proof candidate must pass `FR-ERA3-22` before public release or escalation. |

### 3.2 Existing Backend Integration
This specification builds heavily upon the existing CCP FastAPI architecture to enforce routing, validation, and commercial evaluation:
- **`src/ccp/services/conversion_sequence_router.py`**: Consumed to evaluate `DormancyGateVerdict`. Referral entries must calibrate their timing based on the recipient's dormancy state before presenting new triggers.
- **`src/ccp/services/lead_capture_service.py`**: Reads `check_commercial_cooldown` to ensure that peers clicking referral links are not bombarded with commercial offers if they are on an active cooldown.
- **`src/ccp/services/offer_tier_governor.py`**: Consumes `resolve()` to determine the tier ceiling and appropriate routing pathways for new peers converted via silent referral links.
- **`src/ccp/api/telegram_webhook.py`**: The entry point that intercepts shared deep links (`startapp=reaction_vote_xyz`), passing control to the Mini App routing handlers.
- **Database (`receipt_chain`)**: All User Card generations and peer votes will be immutably recorded in the ADR-compliant audit log.
- **`FR-ERA3-21 SDA Query and Crosswalk Service`**: Resolves canonical `representation_geometry_id` references for the referral surface and keeps crosswalk ownership outside this feature.
- **`FR-ERA3-22 Directional Integrity Engine`**: Evaluates whether a candidate proof object preserves the intended authority, belonging, proof, and aspiration direction or has drifted into prestige theater.

### 3.3 ADR-05 Primitives
This feature is heavily governed by the following experience primitives:
- **`EXP-SOC-001` (Social Treasures + Group Quests)**: The User Card is the ultimate Social Treasure. It has no value if it can be falsified. The primitive mandates that the reward is earned in collaboration or high-threshold solo success, driving intrinsic motivation to share.
- **`EXP-TRG-005` (First Major Win-State)**: Explicitly governs the escalation path for the invited peer. The system MUST NOT prompt the invited peer to record their own Voice DNA until an Ephemeral Win-State (Fiero moment) is achieved by correctly voting or providing feedback.

### 3.4 CBAR Mandate Enforcement
The following canonical mandates from Phase 5 are enforced:
- **Phase5-M01: The Verifiable Artifact Rule**: Governed by Story 1.1. All shareable score objects (User Cards) MUST include a backend cryptographic hash binding the session ID, timestamp, and biometric data. **Enforcement:** A new service `CryptographicCardSigner` will generate a SHA-256 HMAC for the payload. The Mini App frontend will pass this hash back to the server upon load to verify authenticity before rendering the peer's score.
- **Phase5-M02: The Earned Escalation Rule**: Governed by Story 1.2. The recording prompt CANNOT appear before an Ephemeral Win-State is delivered. **Enforcement:** The `ReferralEscalationEngine` blocks all outbound recording prompts to the peer. The peer MUST complete a `vote_submit` action, receive a `VoteValidationResult` (the Ephemeral Win-State), and only then does the engine unlock the `expansion_trigger_unlocked` state.
- **Wave0-SDA Commercial Integrity Rule**: Status-bearing growth artifacts MUST preserve semantic direction. **Enforcement:** a new `ReferralDirectionalIntegrityBridge` calls `FR-ERA3-22` before release, and a new `ReferralRepresentationGeometryGuard` resolves / persists the artifact's representation geometry so factual proof cannot be rendered as prestige theater.

### 3.5 Technical Decisions
- **HMAC over JWT**: To enforce the Verifiable Artifact Rule, HMAC-SHA256 was chosen over heavy JWTs to keep the referral deep links short and performant for the Telegram `startapp` parameter constraints.
- **Deferred Lead Capture**: `lead_capture_service` is only engaged AFTER the Ephemeral Win-State is achieved to honor Friction-Zero. Pre-mature lead capture destroys the Vote-Then-React escalation loop.
- **Stateless Verification**: The verification of the User Card happens on the backend during the initial Telegram Mini App `initData` payload exchange, preventing any frontend tampering of scores.
- **Trust Transfer over Prestige Theater**: Silent Referral is now formally optimized for earned trust transfer rather than raw status extraction. A share artifact may convert well and still be rejected if it encodes vanity proof, superiority signaling, manipulative belonging, or coercive urgency.
- **Representation Geometry Is Mandatory for Status-Bearing Artifacts**: Cryptographic truth is necessary but not sufficient. Each public proof surface must carry a canonical `representation_geometry_id` so its framing can be validated against SDA doctrine.
- **Hard-Negative and Feedback-Loop Safety**: Deceptively-close prestige-bearing proof variants must be blocked before publication, and repeated share / reward loops must be monitored for drift into compulsive comparison or social capture.

## 4. Implementation Plan
<!-- UPDATED: Added SDA instrumentation, release-gating, and loop-safety phases without replacing the baseline architecture. -->

### Phase 1: Core Cryptographic Binding
- **Task 1.1**: Define the Pydantic schema for `UserCardPayload` containing `session_id`, `biometric_hash`, `timestamp`, `coach_id`, and `score_value`.
- **Task 1.2**: Implement `CryptographicCardSigner` service in `src/ccp/services/cryptographic_signer.py` using HMAC-SHA256 with an environment secret.
- **Task 1.3**: Update `content_machine.py` to intercept high-score events and automatically append the signed hash to the generated sharing payload.
- **Task 1.4**: Add `representation_geometry_id`, `directional_integrity_status`, and `hard_negative_status` fields to the referral payload models so status-bearing proof surfaces can carry SDA state without duplicating ontology.

### Phase 2: Deep Link Generation & Routing
- **Task 2.1**: Implement the Telegram deep link generator that constructs `https://t.me/ccp_bot/app?startapp=ref_...` incorporating the encrypted payload.
- **Task 2.2**: Update `src/ccp/api/telegram_webhook.py` to parse the `ref_` prefix from the `startapp` payload.
- **Task 2.3**: Create a new API endpoint `GET /api/referral/verify-card` that accepts the deep link payload and validates the signature, returning the verified `UserCardPayload` to the frontend.
- **Task 2.4**: Implement `ReferralRepresentationGeometryGuard` to resolve the correct canonical geometry through `FR-ERA3-21` before the card is rendered or signed for public distribution.

### Phase 3: The Earned Escalation Engine
- **Task 3.1**: Define the Pydantic state model `ReferralEscalationState` to track `vote_submitted`, `win_state_delivered`, and `expansion_unlocked`.
- **Task 3.2**: Implement `ReferralEscalationEngine` in `src/ccp/services/referral_escalation_engine.py` to evaluate the user's state. It must throw an error if an expansion request is made before `win_state_delivered == True`. Upon successful delivery of the Ephemeral Win-State, the system must execute an immutable log write (`referral-win-state-delivered`) to the `ReceiptChain` prior to enabling escalation.
- **Task 3.3**: Integrate with `conversion_sequence_router.py` to ensure that peers who have been dormant are not immediately thrown into aggressive escalation.
- **Task 3.4**: Implement `ReferralDirectionalIntegrityBridge` so every status-bearing artifact candidate is screened by `FR-ERA3-22` before `SignedUserCard` issuance or escalation unlock. Extract the evaluation ID from the `FR-ERA3-22` response and assign it to the `directional_integrity_report_id` field in the `SignedUserCard`.
- **Task 3.5**: Define downgrade paths for cards that are factually true but directionally unsafe, falling back to neutral invitation surfaces instead of prestige-bearing proof.
- **Task 3.6**: Implement a resolution rule to populate the `trust_transfer_class` field in `VoteValidationResult`. If the peer's validated vote aligns with the canonical representation geometry resolved by the `ReferralRepresentationGeometryGuard`, map the field to `earned_authority`; otherwise, fall back to `neutral_invitation`.

### Phase 4: Integration with Commercial Gates
- **Task 4.1**: Connect the successful escalation event to the `lead_capture_service.py` to transition the peer from an anonymous voter to an identified lead.
- **Task 4.2**: Use `offer_tier_governor.py` to grant the new peer provisional access to the Lead Magnet ($0) layer for their first Reaction recording.
- **Task 4.3**: Integrate Immutable Audit Logging: write `referral-card-generated`, `referral-card-verified`, and `referral-escalation-triggered` actions to the `ReceiptChain`.
- **Task 4.4**: Persist `ReferralIntegrityEnvelope` audit records that capture geometry selection, directional-integrity decision, hard-negative status, and loop-safety state for every status-bearing proof surface. The `blocked_reason` field MUST be populated using the explicit rejection message returned by `FR-ERA3-22` if the decision is FAIL or REVIEW.
- **Task 4.5**: Implement `ReferralLoopSafetyMonitor` to cool automated escalation when repeated share / reward cycles show prestige addiction, manipulative comparison, or social capture patterns. A cycle violation is strictly defined as generating >5 status-bearing share/reward cycles within a 24-hour window, which automatically degrades `loop_safety_status` to 'cooling' and pauses automatic escalation.

## 5. Primary Output Schema
<!-- UPDATED: Added SDA references and runtime integrity state while keeping canonical ontology ownership outside this feature. -->
<!-- REVISION: Added registered DEP-IDs for all data objects. -->

```python
from pydantic import BaseModel, Field
from datetime import datetime

class UserCardPayload(BaseModel):
    """DEP-ID: DEP-SOC-010"""
    session_id: str = Field(..., description="Unique session ID where the score was achieved")
    coach_id: str = Field(..., description="The ID of the coach who achieved the score")
    timestamp: datetime = Field(..., description="The exact time the score was calculated")
    biometric_hash: str = Field(..., description="SHA-256 hash of the biometric data points")
    score_value: int = Field(..., ge=0, le=100, description="The validated biometric score")
    representation_geometry_id: str = Field(..., description="Canonical SDA representation geometry resolved for this share surface")
    directional_integrity_status: str = Field("pending", description="Runtime release state returned by FR-ERA3-22")
    hard_negative_status: str = Field("pending", description="Whether known prestige-theater or vanity-proof patterns were detected")

class SignedUserCard(BaseModel):
    """DEP-ID: DEP-SOC-011"""
    payload: UserCardPayload
    signature: str = Field(..., description="HMAC-SHA256 signature of the payload")
    directional_integrity_report_id: str = Field(..., description="Reference to the FR-ERA3-22 evaluation used to approve release")

class VoteValidationResult(BaseModel):
    """DEP-ID: DEP-SOC-012"""
    is_correct: bool = Field(..., description="Whether the peer's vote matched the consensus")
    win_state_message: str = Field(..., description="The Ephemeral Win-State message (e.g., 'Your intuition matches the top 10%')")
    expansion_trigger_unlocked: bool = Field(..., description="MUST be True before prompting the peer to record")
    trust_transfer_class: str = Field("earned_authority", description="Commercial-semantic interpretation of the proof surface presented to the peer")

class ReferralEscalationState(BaseModel):
    """DEP-ID: DEP-SOC-013"""
    peer_telegram_id: int
    coach_source_id: str
    vote_submitted: bool = False
    win_state_delivered: bool = False
    escalation_presented: bool = False
    loop_safety_status: str = Field("healthy", description="Longitudinal status for prestige-addiction / social-capture monitoring")

class ReferralIntegrityEnvelope(BaseModel):
    """DEP-ID: DEP-SOC-014"""
    source_session_id: str
    representation_geometry_id: str
    directional_integrity_decision: str
    hard_negative_status: str
    loop_safety_status: str = "healthy"
    blocked_reason: str | None = None
```

## 6. Backward Compatibility Fallback
<!-- UPDATED: Status-bearing release now fails closed when SDA governance is missing or negative. -->
For older legacy deep links that do not contain the `ref_` prefix or the cryptographic signature, the system will fall back to rendering a generic "Reaction Request" screen rather than a verified "User Card". Legacy users will not see the specific score or biometric data of the sender, preserving the rule that ONLY cryptographically verified data can be presented as status-bearing proof. Existing `trivianar_engine_service.py` interactions will route to standard default flows until fully deprecated.

If SDA query / crosswalk resolution is unavailable, or if `FR-ERA3-22` returns `REVIEW` / `FAIL` for a prestige-bearing proof surface, the system MUST fail closed on the status-bearing version and fall back to a neutral invitation artifact. This preserves access to the product loop without teaching the wrong status logic.

## 7. Tasks
<!-- UPDATED: Added concrete work items for SDA representation geometry, directional-integrity, and loop governance. -->

1. Create `src/ccp/models/referral_models.py` containing the schemas defined in Section 5.
2. Implement `src/ccp/services/cryptographic_signer.py` for HMAC-SHA256 operations.
3. Add `generate_signed_card()` to the post-reaction scoring pipeline.
4. Add `verify_signed_card(payload, signature)` service function.
5. Implement FastAPI route: `POST /api/referral/verify` mapped to `verify_signed_card`.
6. Implement `src/ccp/services/referral_escalation_engine.py` with the rigid gating logic.
7. Write `ReceiptChain` loggers for all referral generation and validation events.
8. Wire the `ReferralEscalationEngine` to `lead_capture_service.py` for post-win lead capture.
9. Write unit tests for `CryptographicCardSigner` (Valid, Tampered, Expired cases).
10. Write integration tests for the full Vote-Then-React escalation pathway.
11. Update Telegram Mini App manifest configuration to accept the new `startapp` payload length.
12. Execute CBAR QA validation against the Phase5 mandates before deployment.
13. Implement `ReferralRepresentationGeometryGuard` against `FR-ERA3-21`.
14. Implement `ReferralDirectionalIntegrityBridge` against `FR-ERA3-22`.
15. Persist `ReferralIntegrityEnvelope` state and audit records.
16. Add downgrade rendering for directionally unsafe prestige-bearing proof artifacts.
17. Implement `ReferralLoopSafetyMonitor` cooling rules for repeated share / reward cycles.

## 8. Acceptance Criteria
<!-- UPDATED: Added explicit criteria for trust-transfer semantics, hard-negative rejection, and loop-safety. -->

### AC 1: Cryptographic Binding Validation
- **Given** a high-performing coach finishes a Debate reaction,
- **When** the system generates the shareable User Card link,
- **Then** the link payload must contain a signature generated via HMAC-SHA256 over the `session_id`, `timestamp`, and `biometric_hash`.
- **FAILURE EXAMPLE:** A user manually alters the `score_value` in the deep link payload from 85 to 99. The `verify_signed_card()` function must raise a `SignatureMismatchError` and refuse to render the User Card, falling back to an error state.
- **Mandate Enforced:** Phase5-M01 (The Verifiable Artifact Rule).
- **SDA EXTENSION:** The same payload must also carry a canonical `representation_geometry_id`, and the status-bearing version of the card may only be published if `FR-ERA3-22` approves the directional-integrity decision.

### AC 2: Gated Escalation Pathway
- **Given** an invited peer clicks a valid User Card deep link and views the Debate,
- **When** the peer submits their vote,
- **Then** the system MUST return a `VoteValidationResult` with an Ephemeral Win-State message and transition the state to `win_state_delivered = True`. Only then can the recording prompt be rendered.
- **FAILURE EXAMPLE:** The UI attempts to render the recording prompt *before* the vote is cast or simultaneously with the vote button. The backend `ReferralEscalationEngine` must reject any state transition to `escalation_presented` if `win_state_delivered` is False, throwing an `EarnedEscalationViolation`.
- **Mandate Enforced:** Phase5-M02 (The Earned Escalation Rule).
- **SDA EXTENSION:** The win-state copy, preview framing, and escalation pathway must preserve healthy trust transfer. A proof surface that slides into vanity proof, superiority theater, coercive urgency, or manipulative belonging MUST be blocked or downgraded before escalation even if the underlying event is authentic.

### AC 3: Silent Lead Capture Integration
- **Given** a peer has successfully achieved their Ephemeral Win-State and clicks "Record my own take,"
- **When** the peer proceeds to the recording step,
- **Then** the system MUST call `lead_capture_service.insert_lead()` seamlessly in the background, utilizing the `offer_tier_governor.py` to assign Tier 1 ($0) provisional access without interrupting the flow with heavy login forms.
- **FAILURE EXAMPLE:** The peer is redirected to a standard web browser form asking for email and password before they can record, completely destroying Friction-Zero and causing a bounce.
- **Mandate Enforced:** Phase5-M04 (The Inline Capture Hook).

### AC 4: Prestige-Theater Rejection
- **Given** a coach's artifact is cryptographically valid but the public proof framing increases status pressure by teaching superiority, vanity proof, or exclusionary belonging,
- **When** `ReferralDirectionalIntegrityBridge` evaluates the candidate through `FR-ERA3-22`,
- **Then** the system MUST refuse to release the prestige-bearing version and either downgrade to a neutral invitation surface or require manual review according to policy.
- **FAILURE EXAMPLE:** A Prismatic-style card highlights "Top 1%" dominance copy and tribal exclusion cues despite the underlying score being real. The system publishes it anyway because the signature is valid. This is a failure of Silent Referral's SDA governance.

### AC 5: Feedback-Loop Cooling
- **Given** a user repeatedly triggers status-bearing referral artifacts (>5 share/reward cycles within a 24-hour window) forming compulsive proving or social-capture loops,
- **When** the `ReferralLoopSafetyMonitor` detects a degraded `loop_safety_status` (cooling),
- **Then** automatic escalation and amplification MUST cool or pause without revoking the factual proof lineage of the original achievements.
- **FAILURE EXAMPLE:** The same actor repeatedly farms high-status proof cards and the system keeps escalating them unchanged despite unhealthy comparison loops becoming visible in the telemetry.

## 9. Dependencies
<!-- UPDATED: Added mandatory SDA and upstream reaction dependencies. -->

### Internal Dependencies
- `src/ccp/services/lead_capture_service.py`: For registering new peers seamlessly.
- `src/ccp/services/offer_tier_governor.py`: For assigning the initial offer tier to incoming referral peers.
- `src/ccp/services/conversion_sequence_router.py`: To check dormancy and cadence for follow-up notifications.
- `src/ccp/core/receipt_chain.py`: Immutable logging of referral actions.
- `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`: Canonical ontology / grammar ownership.
- `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`: Canonical SDA lookup and crosswalk access.
- `FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`: Directional-integrity decisioning for status-bearing proof release.
- `PRD_06_Conscious_Reactions.md`: Upstream reaction artifacts are a major source of referral proof objects and therefore share the same status / belonging / authority risks.

### External Dependencies
- `Telegram Bot API`: Specifically the `startapp` parameter of the Mini App deep link functionality.
- `hmac` and `hashlib`: Python standard libraries for cryptographic signing.

## 10. Testing Strategy
<!-- UPDATED: Added semantic-direction tests for prestige-theater rejection and loop-safety cooling. -->

All tests will follow the established `pytest` pattern in `tests/integration/`, specifically mirroring the class-based grouping and failure-case assertions seen in `test_cpsc_fr51_challenge_funnel.py`.

### Unit Tests (`tests/unit/test_referral_crypto.py`)
1. `test_signer_valid_payload_passes`: Verifies that a correctly signed payload passes validation.
2. `test_signer_tampered_score_fails`: Modifies the `score_value` after signing and verifies `SignatureMismatchError` is raised.
3. `test_signer_altered_biometric_hash_fails`: Alters the `biometric_hash` and confirms failure.
4. `test_escalation_engine_premature_escalation_raises`: Attempts to set `escalation_presented = True` while `win_state_delivered = False`, ensuring an `EarnedEscalationViolation` is raised.
5. `test_status_bearing_card_without_geometry_fails_closed`: Verifies that a prestige-bearing referral card cannot publish if `representation_geometry_id` cannot be resolved.
6. `test_prestige_theater_hard_negative_blocks_release`: Verifies that a factually valid card is blocked or downgraded when `FR-ERA3-22` flags superiority theater or vanity proof.

### Integration Tests (`tests/integration/test_cpsc_frera3_03_referral.py`)
1. `test_full_vote_then_react_loop_success`: Simulates a full deep-link intercept -> vote submission -> win-state delivery -> escalation prompt -> lead capture insertion. Ensures `ReceiptChain` logs `referral-card-verified` and `referral-escalation-triggered`.
2. `test_referral_peer_cooldown_routing`: Simulates a peer who has previously interacted and is on a commercial cooldown (via `lead_capture_service.check_commercial_cooldown`). Validates that the peer is allowed to vote but is NOT aggressively pushed to a paid challenge immediately, deferring to `conversion_sequence_router.py`.
3. `test_directionally_unsafe_card_downgrades_to_neutral_invitation`: Confirms a real score can still route to a non-prestige invitation surface when SDA release criteria fail.
4. `test_referral_loop_cooling_pauses_escalation`: Simulates repeated status-bearing share cycles that degrade `loop_safety_status` and verifies escalation is cooled while factual proof lineage is preserved.
