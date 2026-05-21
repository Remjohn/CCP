# FR-ERA3-14 — B2B2C Commercial Ladder & Stealth Course Tech Spec

## 1. Files Read

The following foundational documents, modules, and source files were audited and integrated prior to drafting this technical specification:

1. `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` (Format, Execution Order, Mini App Separation, and Pre-Flight Mandates)
2. `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` (Core B2B2C commercial layer definitions, Trojan Horse strategy, and the 4-tier pricing model)
3. `docs/architecture/april_updates/Phase5_Growth_Epics.md` (Full Acceptance Criteria, CBAR Mandates, and Epic/Story breakdowns for Growth Phase 5)
4. `docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` (Adversarial corrections, including the explicit enforcement of the 1-Tap Paywall Rule)
5. `primitives/experience/friction_ability/EXP-FRC-004.yaml` (Friction-Zero Ability - dictates the zero-barrier requirement for core platform actions)
6. `primitives/experience/friction_ability/EXP-FRC-002.yaml` (System 1 to System 2 Escalation - dictates the pacing of cognitive load)
7. `src/ccp/services/offer_tier_governor.py` (Existing Offer Tier routing logic, boundary ceilings, and validation gates)
8. `src/ccp/services/learning_path_builder.py` (Existing DAG-based content journey service for progress tracking and unlock gating)
9. `tests/integration/test_cpsc_fr58_offer_tier.py` (Existing integration testing patterns, assertion structures, and receipt chain mocking strategies)

---

## 2. Overview

### Problem Statement
In Era 3, the Conscious Coaching Platform (CCP) rejects traditional SaaS acquisition tactics. Coaches participating in the free ($0) Proof Layer (Lead Magnet) experience the platform through actionable insights and biometric score validation (e.g., via the OFO Engine or Conscious Reactions). However, as users progress deeper into the platform and approach advanced learning pathways—such as the "Structure" Adaptive Layer containing deep FR61 biometric insights—they must be seamlessly transitioned to the paid Tier 1 continuity subscription ($39.99/mo). Legacy systems relied on abrupt paywalls, external browser redirects, and generic "Upgrade Now" landing pages, creating massive cognitive and physical friction that destroyed Hook Cycle Velocity and decimated conversion rates.

### Solution
This specification implements the **Stealth Course Commercial Ladder (FR-ERA3-14)**. Instead of a hard sales pitch, the platform leverages the "Stealth Course" mechanic. Free users are guided through an automated, frictionless learning progression governed by the `LearningPathBuilder`. When a user reaches a predetermined transition boundary (e.g., an unlock condition requiring Tier 1), the system intercepts the next-content recommendation and surfaces an elegant, inline upgrade gate.

Crucially, this transition enforces the **1-Tap Paywall Rule**. It consumes the existing `OfferTierGovernor` to validate the user's eligibility and routes the upgrade through the FR-ERA3-02 In-Chat Payments module. The entire transaction occurs natively within Telegram using Apple Pay or Google Pay. The cognitive and physical effort required matches that of swiping a flashcard, ensuring zero break in momentum and preserving absolute "Friction-Zero Ability."

### Scope
The scope of this technical specification covers:
1. The **Stealth Course Boundary Detector**, which interfaces with `learning_path_builder.py` to intercept content delivery when an upgrade is required.
2. The **Commercial Ladder Orchestrator**, which delegates tier validation to `offer_tier_governor.py` and delegates payment execution to the FR-ERA3-02 Payment Sheet.
3. The definition of strict Pydantic v2 schemas to govern the transition state machine.
4. The enforcement of CBAR Mandate Phase5-M05.
5. The logging of immutable cryptographic audit receipts into the `receipt_chain`.

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

| DEP-ID | Title | Status | Description |
| :--- | :--- | :--- | :--- |
| **DEP-ENG-041** | Receipt Chain Guard | EXISTING | Mandates immutable cryptographic logging for all state mutations. |
| **DEP-ENG-074** | Learning Path Entry | EXISTING | Defines the DAG-based content progression used for the Stealth Course. |
| **DEP-COM-014** | Stealth Course Transition Boundary | **NEW** | The intercept threshold where free ($0) progression stops and Tier 1 is required. |
| **DEP-COM-015** | 1-Tap Tier Upgrade State | **NEW** | The lifecycle tracking of an inline Telegram payment execution. |

### 3.2 Existing Backend Integration

This specification does not exist in a vacuum; it deeply integrates with the existing Era 3 FastApi backend architecture:

1. **`src/ccp/services/learning_path_builder.py`**
   - **Extension:** This spec consumes the `LearningPathBuilder.recommend_next()` method. We introduce an intercept layer. When `recommend_next()` hits an entry with an `unlock_condition` specifying a minimum tier of `TIER_1_CHALLENGE` or higher, and the user is currently on the $0 Proof Layer, the system halts content delivery and emits a `StealthCourseBoundaryReached` event.
2. **`src/ccp/services/offer_tier_governor.py`**
   - **Consumption:** We invoke `OfferTierGovernor.evaluate(client_id=client_id, coping_position=cp, target_campaign_tier=1)` to ensure the user is mathematically and psychologically eligible for the $39.99/mo Tier 1 subscription before presenting the paywall.
3. **`FR-ERA3-02` (In-Chat Telegram Payments)**
   - **Consumption:** We do *not* implement Stripe logic here. Instead, upon successful tier validation, this service prepares a `TelegramInvoicePayload` and hands it off to the `pay` Mini App / FR-ERA3-02 webhook, which utilizes the Telegram Bot API native invoicing.

### 3.3 Primitives

This specification strictly adheres to the following Experience Primitives (ADR-05):

- **`EXP-FRC-002: Friction-Zero Ability`**
  - *Constraint:* The startup cost of an action must be mathematically zero.
  - *Application:* The payment upgrade process cannot require the user to leave Telegram, enter a password, or manually type a 16-digit credit card number. It must utilize biometric device-level payments (Apple Pay / Google Pay) directly inline.
- **`EXP-FRC-004: System 1 to System 2 Escalation`**
  - *Constraint:* Workflows must begin in fast, emotional 'System 1' thinking and only escalate to 'System 2' after a micro-commitment.
  - *Application:* The transition boundary first delivers the user their score and validation (System 1 dopamine hit) before introducing the analytical decision to subscribe to Tier 1 (System 2).

### 3.4 CBAR Mandate Enforcement

**Phase5-M05: The 1-Tap Paywall Rule (Story 3.1)**
- *Originating Story:* Epic 3, Story 3.1 (Stealth Course Transition).
- *Mandate Definition:* All continuity subscription upgrades within the Stealth Course flow must use native Telegram 1-tap payment infrastructure. The payment action must require the same physical and cognitive effort as swiping a flashcard, preserving Friction-Zero momentum and eliminating cart abandonment. External browser redirects are strictly banned.
- *Enforcement Mechanism:* The `StealthCourseManager` service will throw an immediate `RuntimeError(CbarViolation)` if a generated checkout link attempts to use an external `https://checkout.stripe.com/` URL rather than a Telegram `invoice` payload. The Acceptance Criteria mandates a failure test for this specific violation.

### 3.5 Technical Decisions

1. **State Machine Intercept vs. Pre-Calculation:**
   - *Decision:* Rather than proactively querying payment status on every single learning path interaction, we rely on the existing `learning_path_builder` to evaluate gating. If the user hits a locked node, the builder returns `None` or a restricted node, which the `StealthCourseManager` catches to trigger the commercial ladder.
   - *Rationale:* Reduces database queries and isolates commercial routing logic from pure educational progression logic.
2. **Delegation to FR-ERA3-02:**
   - *Decision:* This service generates a deterministic `StealthCourseUpgradeToken` but delegates the actual fiat transaction handling to the FR-ERA3-02 Payment Sheet.
   - *Rationale:* Maintains the Single Responsibility Principle. If the Stripe integration changes, this Stealth Course progression logic remains unaffected.
3. **Optimistic Pre-Rendering of Next Node:**
   - *Decision:* To preserve momentum, the payload that returns the 1-Tap Invoice also returns a blurred, "locked" preview of the exact content the user will receive upon payment.
   - *Rationale:* Increases conversion by making the reward tangible and immediate.

---

## 4. Implementation Plan

The implementation of the Stealth Course Commercial Ladder is divided into four chronological phases comprising 14 distinct engineering tasks. 

### Phase 1: Core Models, Constants, and Schema Definition
The foundation requires establishing strict Pydantic v2 schemas that enforce the contract between the Learning Path, the Tier Governor, and the Payment module.

1. **Task 1: Define Commercial Ladder Enums**
   - Create `CommercialLadderState` enum (`ACTIVE_FREE`, `BOUNDARY_REACHED`, `PAYMENT_PENDING`, `UPGRADED_TIER_1`).
   - Create `StealthCourseBoundary` enum mapping directly to Context Premise Map dimensions that require paid unlocks.
2. **Task 2: Define `StealthCourseTransitionRequest`**
   - Build a Pydantic model representing the incoming webhook trigger when a user hits a boundary. Must include `client_id`, `coach_id`, `journey_id`, and `current_node_id`.
3. **Task 3: Define `StealthCourseTransitionResponse`**
   - Build the output Pydantic model. Must strictly type the return of the locked payload, containing the Telegram Invoice schema representation and the blurred preview metadata. No `Any` typing allowed.
4. **Task 4: Define `StealthCourseUpgradeReceipt`**
   - Create the internal model used to log the cryptographic receipt when the user successfully transitions tiers. Must include the `governor_evaluation_id` from the `OfferTierGovernor`.

### Phase 2: Stealth Course Boundary Detection
This phase integrates the commercial logic with the existing `learning_path_builder.py` DAG traversal.

5. **Task 5: Implement `StealthCourseBoundaryDetector.check_boundary()`**
   - Create a pure function that evaluates a `NextContentRecommendation` against the user's current subscription level.
   - If the `unlock_condition` of the next node requires `TIER_1_CHALLENGE` and the user is on `$0 Proof Layer`, return a `StealthCourseBoundaryReached` internal state object.
6. **Task 6: Inject Intercept into DAG Traversal**
   - Wrap the standard `LearningPathBuilder.recommend_next()` call within the `StealthCourseManager`.
   - Ensure that if `recommend_next()` returns a boundary, the system gracefully halts delivery and does not mark the node as completed in `learning_progress`.
7. **Task 7: Generate Locked Preview Metadata**
   - Develop a utility to extract the `title`, `topic_cluster`, and `difficulty_level` of the locked node to populate the preview payload, ensuring the user knows exactly what they are buying.

### Phase 3: Offer Tier Validation and 1-Tap Payment Hook
This phase handles the psychological gating and the financial handoff, strictly enforcing Phase5-M05.

8. **Task 8: Integrate `OfferTierGovernor.evaluate()`**
   - Instantiate the `OfferTierGovernor` with the current `coach_id` and the `receipt_chain`.
   - Call `.evaluate()` with `target_campaign_tier=1`.
   - Catch `ValueError(OfferTierError.FAIL_CAPACITY_EXCEEDED)`. If caught, fallback to a graceful error state (e.g., "Account not eligible for upgrade at this time").
9. **Task 9: Construct the Telegram Invoice Payload**
   - Map the successful `OfferTierGovernorRow` into a Telegram `sendInvoice` compatible payload.
   - Define the prices strictly: `price=3999` (cents), `currency="USD"`, `label="Tier 1: Speaking & Learning"`.
10. **Task 10: Enforce the 1-Tap Paywall Rule (Anti-Slop Guard)**
    - Implement a validation step right before returning the invoice payload: `if 'http' in invoice_payload.url: raise CbarViolation("External redirects banned by M05")`. The payload must only be an internal Telegram bot invoice token.
11. **Task 11: Pass to FR-ERA3-02 Payment Sheet**
    - Generate the `stealth_course_upgrade_token` string that the frontend Mini App will use to invoke the `pay` startapp, and embed it in the `StealthCourseTransitionResponse`.

### Phase 4: Upgrade Success Handling and Receipt Logging
The final phase handles the async webhook return from a successful payment, unlocking the content and resuming the user's journey.

12. **Task 12: Implement `handle_successful_upgrade_webhook()`**
    - Create the endpoint/service method to process the success callback from the payment infrastructure.
    - Update the user's canonical subscription record in the database from `$0` to `TIER_1_CHALLENGE`.
13. **Task 13: Resume Learning Path Progression**
    - Automatically push the locked `NextContentRecommendation` to the user via Telegram push, immediately delivering the gratification of the purchase without requiring them to reload the app.
14. **Task 14: Cryptographic Receipt Logging**
    - Write a `receipt_chain` entry with action `stealth-course-upgrade-complete`, hashing the invoice ID, the `governor_evaluation_id`, and the new tier. This guarantees an immutable audit trail for the commercial transition.

---

## 5. Primary Output Schema

All models use Pydantic v2. `Any` is strictly forbidden.

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional

class LockedContentPreview(BaseModel):
    content_id: UUID
    title: str = Field(..., description="Title of the locked Stealth Course node")
    topic_cluster: str
    difficulty_level: str
    blurred_thumbnail_url: str

class TelegramInvoicePayload(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    payload: str = Field(..., description="Internal tracking payload for the bot")
    provider_token: str = Field(..., description="Stripe token via Telegram API")
    currency: str = "USD"
    prices_json: str = Field(..., description="JSON serialized array of LabeledPrice")

    @field_validator('payload')
    def validate_no_external_urls(cls, v):
        if "http://" in v or "https://" in v:
            raise ValueError("CBAR Phase5-M05 Violation: External URLs are strictly banned. Must use native Telegram payment payload.")
        return v

class StealthCourseTransitionResponse(BaseModel):
    client_id: UUID
    journey_id: UUID
    governor_evaluation_id: UUID
    locked_preview: LockedContentPreview
    invoice_payload: TelegramInvoicePayload
    stealth_course_upgrade_token: str = Field(..., description="Token for frontend Mini App to invoke the pay startapp")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StealthCourseUpgradeReceipt(BaseModel):
    client_id: UUID
    previous_tier: str
    new_tier: str
    governor_evaluation_id: UUID
    stripe_invoice_id: str
    unlocked_content_id: UUID
    timestamp: datetime
```

---

## 6. Backward Compatibility Fallback

**Scenario:** A legacy coach or client is traversing a learning path that was constructed before the Stealth Course boundaries were deployed. Their `$0` account hits a node that is suddenly marked as `TIER_1_CHALLENGE` via a retroactive schema migration.

**Fallback Strategy:**
The `StealthCourseBoundaryDetector` inspects the user's creation date. If the `client_id` was created prior to the Epoch Date of Era 3 (defined in constants as `ERA3_EPOCH_DATE`), they are granted a "Legacy Grandfather Pass." The intercept is bypassed, logging a `legacy-grandfather-bypass` receipt, and the user receives the content without hitting the paywall. This prevents abruptly paywalling existing users mid-experience, which violates Trust & Status primitives.

---

## 7. Tasks

1. Define `CommercialLadderState` and `StealthCourseBoundary` enums.
2. Create `StealthCourseTransitionRequest` Pydantic model.
3. Create `StealthCourseTransitionResponse` Pydantic model (with M05 validation).
4. Create `StealthCourseUpgradeReceipt` model for logging.
5. Implement `StealthCourseBoundaryDetector.check_boundary()`.
6. Inject intercept logic into the `LearningPathBuilder` traversal wrapper.
7. Develop metadata extraction for the `LockedContentPreview`.
8. Integrate `OfferTierGovernor.evaluate(target_campaign_tier=1)`.
9. Construct the `TelegramInvoicePayload` mapping.
10. Enforce the Phase5-M05 URL ban in code via Pydantic validators.
11. Expose the handoff to the FR-ERA3-02 `pay` Mini App wrapper.
12. Implement the async `handle_successful_upgrade_webhook()` method.
13. Automate the immediate push delivery of the unlocked content post-purchase.
14. Finalize `receipt_chain` integration for immutable commercial logging.

---

## 8. Acceptance Criteria

### AC1: Transition Boundary Detection via DAG
- **Given** a free ($0) user completes a learning path node,
- **When** the `StealthCourseManager` invokes `recommend_next()` and the underlying `unlock_condition` requires Tier 1,
- **Then** the service correctly intercepts the output, halts content delivery, and returns a `StealthCourseBoundaryReached` internal state mapped to the correct locked preview metadata.
- **FAILURE EXAMPLE:** The intercept logic fails to read the `unlock_condition.min_tier`, and the user is served the premium `course_video` payload for free, bleeding intellectual property.

### AC2: The 1-Tap Paywall Rule (Phase5-M05 Enforcement)
- **Given** the user hits the Stealth Course transition boundary and is presented with the upgrade offer,
- **When** the system generates the checkout payload,
- **Then** the payload exclusively utilizes the `TelegramInvoicePayload` schema, designed for the native Telegram Bot API Apple/Google Pay UI.
- **FAILURE EXAMPLE:** The system returns an `https://checkout.stripe.com/...` link. The Pydantic validator fails to catch it, the user clicks the link, gets kicked out to Safari, sighs at the friction of finding their wallet, and abandons the cart. This is a fatal violation of Phase5-M05.
- **Mandate Enforced:** Phase5-M05 (The 1-Tap Paywall Rule).

### AC3: Governor Capacity Gate Enforcement
- **Given** a user hits the transition boundary,
- **When** the `OfferTierGovernor.evaluate()` method is called to validate the upgrade,
- **Then** if the user's `coping_position` dictates a ceiling lower than Tier 1 (e.g., they have demonstrated extreme negative metrics requiring a different intervention), the upgrade is blocked, returning a graceful fallback instead of the invoice.
- **FAILURE EXAMPLE:** The system bypasses the `OfferTierGovernor`, allowing a severely unqualified lead to purchase a high-level tier, corrupting the platform's social proof architecture.

### AC4: Immediate Fulfillment Momentum
- **Given** the 1-tap payment successfully clears,
- **When** the webhook triggers `handle_successful_upgrade_webhook()`,
- **Then** the system immediately pushes the locked `NextContentRecommendation` to the user's chat interface without requiring a manual refresh or navigation.
- **FAILURE EXAMPLE:** The user pays $39.99, receives a generic "Thank you" receipt, and has to manually click through 3 menus to find the content they just paid for, violating Friction-Zero Ability.

---

## 9. Dependencies

### Internal Services
- **`src/ccp/services/learning_path_builder.py`**: Provider of the content DAG and `recommend_next()` state traversal.
- **`src/ccp/services/offer_tier_governor.py`**: The canonical psychological/financial routing gate that ensures a user is allowed to upgrade to Tier 1.
- **`src/ccp/core/receipt_chain.py`**: The immutable cryptographic ledger required for logging commercial tier changes.

### External Integrations
- **Telegram Bot API (Payments)**: Natively invoked via the FR-ERA3-02 interface. The payload generated in this spec is consumed by the Telegram `sendInvoice` method to trigger Apple Pay/Google Pay.
- **Stripe API**: Functions invisibly in the background, receiving the tokenized fiat transaction from Telegram.

---

## 10. Testing Strategy

The testing strategy mirrors the rigorous patterns established in `tests/integration/test_cpsc_fr58_offer_tier.py`, executing against the actual integrations rather than superficial mocks.

### Unit Tests
1. **`test_stealth_course_boundary_intercept`**:
   Construct an in-memory learning path with a mix of $0 and Tier 1 nodes. Assert that `StealthCourseManager.get_next_step()` returns standard content for $0 nodes and the `StealthCourseTransitionResponse` for the Tier 1 node.
2. **`test_m05_strict_url_ban_validator`**:
   Attempt to instantiate `TelegramInvoicePayload` with a `provider_token` containing `https://checkout.stripe.com`. Assert that it violently raises a `ValueError` containing "CBAR Phase5-M05 Violation".
3. **`test_governor_rejection_graceful_fallback`**:
   Mock `OfferTierGovernor.evaluate()` to raise `ValueError(OfferTierError.FAIL_CAPACITY_EXCEEDED)`. Assert that the Stealth Course manager catches this and returns the appropriate non-commercial fallback message rather than crashing.

### Integration Tests
4. **`test_full_commercial_ladder_progression_integration`**:
   (Integration) Seed a test user in a PostgreSQL test container with `learning_progress` at the boundary. Trigger the progression, capture the generated `TelegramInvoicePayload`, simulate a successful Stripe webhook callback, and assert that `learning_progress` is updated and the user's master tier in the database is elevated to `TIER_1_CHALLENGE`.
5. **`test_cryptographic_receipt_generation_on_upgrade`**:
   (Integration) Following a simulated successful webhook payment, query the local `ReceiptChain` instance on disk. Assert that an entry exists for `stealth-course-upgrade-complete`, and that the parsed `metadata` successfully traces back to the exact `governor_evaluation_id` issued during the gate check.
