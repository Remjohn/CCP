# FR-ERA3-37 — Phase-0 Commercial Bridge and Payment Runtime Tech Spec

## §1 Files Read

### Core Prompt
- `docs/architecture/april_updates/spec_prompts/P0_S05_FR-ERA3-37_Phase0_Commercial_Bridge_And_Payment_Runtime.md`

### Source PRD Modules
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`

### Mandatory Phase-0 Source Set
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/CCP APRIL Updates/05_Core_Experience/Pricing_Silent_Referral_CoCreation_Architecture.md`
- `lab/ccp_biological_orchestration_model_v_1.md`

### Existing Phase-0 Runtime Specs
- `docs/architecture/april_updates/FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md`
- `docs/architecture/april_updates/FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md`

### Existing Billing / Payment / Offer Files
- `src/ccp/api/billing_api.py`
- `src/ccp/models/billing_models.py`
- `src/ccp/models/cpsc_models.py`
- `src/ccp/services/payment_flow_orchestrator.py`
- `src/ccp/services/payment_eligibility_service.py`
- `src/ccp/services/telegram_invoice_handler.py`
- `src/ccp/services/billing_webhook_handler.py`
- `src/ccp/services/billing_middleware.py`
- `src/ccp/services/offer_tier_governor.py`
- `src/ccp/services/post_reveal_offer_projector.py`

### Existing Integration Test Files
- `tests/integration/test_era3_fr02_payment_flow.py`
- `tests/integration/test_era3_fr02_payment_eligibility.py`
- `tests/integration/test_com01_billing_integration.py`
- `tests/integration/test_com01_billing_middleware.py`

### Pre-Work Log

#### Protocol and Structural Read
This spec was written after following the Era-3 spec-writing protocol structure already used throughout this wave:
- explicit pre-work log
- dependency honesty
- typed runtime ownership
- no detached architecture invention

#### Proof from `PRD-09`
The pricing ladder and credit bridge are explicitly defined in the source PRD:

- `PRD-09`, line 125:
  - `1. **$29.99 First Proof Unlock**`
- `PRD-09`, line 129:
  - `The initial $29.99 is applied toward the first $39.99/mo or $99.99/mo upgrade so the next yes feels like continuation, not a second unrelated spend.`
- `PRD-09`, line 133:
  - `free proof → $29.99 activation → $39.99 continuity or $99.99 Coach OS`
- `PRD-09`, line 151:
  - `### 2.6 Telegram-Native Continuity`
- `PRD-09`, line 248:
  - `proof is visible, but activation, download, and usable ownership are gated.`
- `PRD-09`, line 1201:
  - `Frictionless checkout for the $29.99 First Proof Unlock, the $39.99/mo Speaking & Learning tier, and the $99.99/mo Coach OS tier natively inside the Telegram chat or Telegram Mini App using the Telegram Payments API`

#### Proof from `PRD-01`
The platform strategy confirms that the commercial ladder and payment surface are already Telegram-centered:

- `PRD-01`, line 284:
  - `### 4.3 The $0 → $39.99 → $99.99 Conversion Ladder`
- `PRD-01`, line 291:
  - `| **Speaking & Learning** | $39.99/mo |`
- `PRD-01`, line 292:
  - `| **Coach OS** | $99.99/mo |`
- `PRD-01`, line 347:
  - `| **Telegram** | Voice notes coaching sessions, reactions, challenges, content drops, accountability nudges, payments | DSPy pipelines, Pydantic validation, biometric scoring, NIM inference, Stripe webhooks, CMF rendering |`
- `PRD-01`, line 585:
  - `Invisible App continuity ... Telegram Mini App`

#### Proof from the Mandatory Phase-0 Source Set

From `Fladlien_Sales_Insights.md`:
- `the messaging is embedded inside the audit parameters`
- `the initial $29.99 is applied toward the first upgrade`
- commercial sequence is:
  - free proof
  - `$29.99`
  - continuity / Coach OS

From `Pricing_Silent_Referral_CoCreation_Architecture.md`:
- the stronger architecture is:
  - `free proof is delivered first`
  - `the prospect is pulled inside Telegram immediately`
  - `the 29$/month layer becomes the continuity and accountability engine`
  - `the 99$/month layer becomes the full operating system`

From `ccp_biological_orchestration_model_v_1.md`:
- CCP separates:
  - runtime organism
  - outer learning loop
  - optimization infrastructure
- this matters here because the commercial bridge belongs to the runtime organism:
  - specifically between phenotype delivery and commercial evaluation / unlock propagation

#### Existing Backend Signatures Verified

From `payment_flow_orchestrator.py`:
- `async def initiate_upgrade(self, *, telegram_user_id: int, chat_id: int, coach_id: str, target_tier: PaymentTier) -> tuple[EligibilityCheckResult, InvoicePayload | None]`

From `payment_eligibility_service.py`:
- `async def check_eligibility(self, *, telegram_user_id: int, coach_id: str, target_tier: PaymentTier) -> EligibilityCheckResult`

From `telegram_invoice_handler.py`:
- `async def generate_and_send(self, *, chat_id: int, eligibility: EligibilityCheckResult) -> InvoicePayload`

From `billing_webhook_handler.py`:
- `async def handle_event(self, event_type: str, event_data: dict, stripe_event_id: str = "") -> None`

From `billing_middleware.py`:
- `async def require_credits(self, coach_id: str, action: str, cost: int = 0) -> bool`

From `offer_tier_governor.py`:
- `def evaluate(self, *, client_id: str, coping_position: int | None, target_campaign_tier: int, historical_purchased_tiers: list[Any] | None = None) -> OfferTierGovernorRow`

#### Existing Models Verified
Relevant current model structures already exist for:
- `PaymentTier`
- `PaymentStatus`
- `EligibilityVerdict`
- `StoredValueSnapshot`
- `EligibilityCheckResult`
- `InvoicePayload`
- `PaymentTransactionRow`
- billing tiers and statuses

Important gap:
- there is **no current canonical Phase-0 $29.99 activation model**
- there is **no current canonical upgrade-credit state model**
- there is **no current entitlement state for free-proof vs unlock ownership**

This spec must add those missing contracts while interoperating with the existing `$39.99/$99.99` payment rails.

#### Existing Test Patterns Verified
Payment and entitlement-related integration tests already expect:
- standard upgrade flow
- loyalty unlock flow
- already-subscribed blocking
- receipt completeness
- billing integration safety
- middleware gate behavior

That gives us a real baseline for how this new runtime should be tested.

#### Continuity Boundary Confirmed
What remains Phase-0 only:
- first proof unlock
- proof-asset activation
- preview / download / ownership gating
- `$29.99` credit creation and bridge handoff

What becomes continuity / Coach OS concern:
- recurring `$39.99/mo` billing
- recurring `$99.99/mo` billing
- longer-lived entitlement state
- monthly operating privileges
- deeper container / deployment rights

This spec therefore owns the bridge, not the entire subscription engine.

---

## §2 Overview

`FR-ERA3-37` defines the commercial runtime that turns visible free proof into:
- a `$29.99` first proof activation
- a Telegram-native payment handoff
- an immediate unlock-state propagation
- a clean upgrade bridge into `$39.99/mo` or `$99.99/mo`
- and a credit state that makes the next purchase feel like continuation rather than coupon clutter

This runtime sits downstream of the Phase-0 delivery orchestrator and upstream of the existing continuity billing rails.

Its responsibilities are:
- determine what is visible but still locked
- determine what becomes owned and usable after the first payment
- project the correct first unlock offer inside Telegram
- initiate Telegram-native payment flow
- record the first proof unlock state
- create and persist upgrade credit state
- apply that credit to the first qualifying `$39.99` or `$99.99` upgrade
- propagate entitlements after payment events complete

### Core Commercial Law
The runtime must enforce:

> proof is visible for belief, activation is paid for ownership, and the first paid step counts toward continuity.

### What This Spec Is Not
This is not:
- a generic web checkout spec
- a detached Stripe-only commerce layer
- a replacement for current billing tiers
- a full recurring subscription system rewrite

Instead this is:
- a **bridge runtime**
- specialized to the Phase-0 proof lane
- attached to Telegram-native flow
- interoperating with existing eligibility, invoice, and webhook machinery

### Runtime Position
The order across Phase 0 should become:

1. proof is generated and reviewable
2. proof is visible in teaser / preview form
3. activation offer is projected
4. Telegram-native payment is initiated
5. unlock state is propagated after successful payment
6. upgrade credit is stored
7. later continuity upgrade consumes that credit cleanly

### External Framing Rule
The system must frame this commercially as:
- unlocking the first proof package
- applying what they already paid toward the next meaningful step

It must **not** frame it as:
- coupon stacking
- discount gimmicks
- random checkout branching

---

## §3.1 DEP-IDs

### Primary Dependencies
- `DEP-FR-ERA3-36`
  - `FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md`
  - supplies `Phase0OutputBundle`, review completion, and payment-handoff readiness

- `DEP-FR-ERA3-35`
  - `FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
  - defines proof objects whose visibility and ownership states matter commercially

- `DEP-FR-ERA3-33`
  - validated prospect identity and packet context

### Existing Payment / Continuity Dependencies
- `DEP-PAY-001`
  - `PaymentEligibilityService`

- `DEP-PAY-002`
  - `TelegramInvoiceHandler`

- `DEP-PAY-003`
  - `PaymentTransactionRow`

- `DEP-BILL-001`
  - `BillingWebhookHandler`

- `DEP-OFFER-001`
  - `OfferTierGovernor`

### Source Doctrine Dependencies
- `DEP-PRD-09`
- `DEP-PRD-01`
- `DEP-FLADLIEN-PHASE0`

### Future Dependency
- `DEP-FR-ERA3-38`
  - operator console / SLA tracker should display commercial bridge state

### Dependency Boundary Rule
`FR-ERA3-37` may:
- reuse existing billing/payment rails
- create new Phase-0 state models
- call existing invoice / eligibility / webhook logic

`FR-ERA3-37` may not:
- duplicate recurring billing ownership
- bypass existing payment verification flow
- invent a detached “Phase-0 checkout portal”

---

## §3.2 Backend

### Runtime Position
The commercial bridge runtime sits between:
- `Phase0OutputBundle.payment_handoff_ready`
- Telegram-native invoice initiation
- payment confirmation
- unlock propagation
- continuity upgrade routing

### Existing Backend Files to Reuse

#### 1. `payment_flow_orchestrator.py`
Already provides:
- upgrade initiation
- eligibility checking
- Telegram invoice generation

This should be extended or wrapped, not replaced.

#### 2. `payment_eligibility_service.py`
Already provides:
- verdict logic
- in-flight payment detection
- loyalty-based copy variation
- receipt logging

Phase-0 should reuse the shape of this service while adding first-proof-specific state.

#### 3. `telegram_invoice_handler.py`
Already provides:
- native Telegram `sendInvoice` flow
- description selection
- no external URL dependency

This should be reused for:
- first proof unlock invoices
- upgrade invoices after credit application

#### 4. `billing_webhook_handler.py`
Already provides:
- post-payment state propagation
- billing event persistence
- Redis / DB sync

Phase-0 unlock propagation should attach to the same confirmation pathway or a closely aligned adapter.

#### 5. `billing_middleware.py`
Already provides:
- entitlement-style action gating
- status and tier lookups

The new commercial runtime should introduce Phase-0 entitlement semantics that this layer can later honor without confusion.

### Recommended Implementation Roots
- `src/ccp/models/phase0_commercial_models.py`
- `src/ccp/services/phase0_commercial_bridge.py`
- `src/ccp/services/phase0_unlock_propagator.py`
- `src/ccp/api/routes/phase0_commercial.py`
- `tests/services/test_phase0_commercial_bridge.py`

### Recommended Collaborators
- `Phase0DeliveryOrchestrator`
- `PaymentEligibilityService`
- `TelegramInvoiceHandler`
- `BillingWebhookHandler`
- `OfferTierGovernor`
- `post_reveal_offer_projector.py` or successor runtime

### Backend Ownership Law
The commercial bridge runtime owns:
- free vs locked vs unlocked state for Phase-0 proof assets
- first proof unlock offer projection
- upgrade credit state
- post-payment Phase-0 entitlement propagation

It does not own:
- full recurring subscription bookkeeping
- monthly quota enforcement
- Coach OS deployment entitlements

---

## §3.3 Commercial States / Unlocks

This section defines the canonical commercial state machine for Phase 0.

### Surface-State Categories

#### 1. `VISIBLE_FREE`
The asset or proof object can be seen in teaser or preview form.

Examples:
- audit teaser
- score cards
- preview board
- limited proof snippets

#### 2. `LOCKED_ACTIVATION_REQUIRED`
The asset exists but download, ownership, or full release requires the `$29.99` first unlock.

Examples:
- full PDF audit
- downloadable proof package
- full-resolution delivered assets
- final explainer package release

#### 3. `UNLOCKED_PHASE0`
The first proof unlock has been paid and the asset is now owned/released under Phase-0 entitlement.

#### 4. `UPGRADE_CREDIT_ELIGIBLE`
A user has completed the first proof unlock and has credit that can be applied to the first qualifying upgrade.

#### 5. `CREDIT_CONSUMED`
The user’s `$29.99` bridge has already been applied to one qualifying upgrade.

#### 6. `CONTINUITY_ACTIVE`
The user has transitioned to `$39.99/mo` or `$99.99/mo`.

### What Remains Free
The following remain free by doctrine:
- audit teaser / damage reveal
- preview of produced assets
- visible proof that the system understands the coach
- visible score-card surfaces needed to create belief

### What Becomes Paid / Activated
The following require the `$29.99` first unlock:
- full package activation
- full download ownership
- full PDF audit delivery
- full audit explainer video release
- final release of produced proof assets under the package scope

### What the `$29.99` Creates
The first proof unlock creates:
- a payment record
- a Phase-0 entitlement state
- a release permission
- an upgrade credit state

### Credit Bridge Rule
The first qualifying upgrade to:
- `$39.99/mo`
- or `$99.99/mo`

must apply the full `$29.99` once.

### Suggested Credit Validity
Default recommendation:
- valid for `7 days`
- one-time use
- only first qualifying upgrade

This keeps urgency without UI clutter.

### Telegram-Native Flow Rule
Commercial transitions must feel like:
- visible proof in chat / mini app
- one-tap invoice in Telegram
- post-payment unlock message in Telegram
- continuity invite in the same relational surface

Not:
- browser detour
- email checkout chain
- portal-first commerce

---

## §3.4 Governance Constraints

### G1. Proof-Before-Payment Rule
The runtime may not present the first paid activation before visible proof exists.

### G2. Clean-Credit-Bridge Rule
Credit must be modeled as continuation credit, not coupon clutter.

### G3. Telegram-Native Commercial Flow Rule
Default payment and unlock flow must stay inside Telegram or Telegram Mini App surfaces.

### G4. No-Random-Upsell Rule
The first proof unlock must map to a concrete released package, not a vague upgrade offer.

### G5. Continuity-Bridge Rule
The `$29.99` state must naturally lead to `$39.99` or `$99.99` without detached logic branches.

### G6. No Detached Checkout Architecture
This runtime must reuse existing invoice / eligibility / webhook rails where possible.

### G7. Unlock Propagation Must Be Verifiable
Post-payment entitlement changes must emit receipts and persisted state.

### G8. One Credit, One Consumption
The `$29.99` bridge may only be applied once.

### G9. Free Visibility Must Not Accidentally Become Full Ownership
The runtime must clearly separate preview from download / activation / ownership.

### G10. Phase-0 Is Not Continuity
The `$29.99` first unlock must not be represented as a monthly tier itself.

---

## §3.5 Technical Decisions

### TD1. Keep `$29.99` Outside Existing `PaymentTier`
Decision:
- do not overload current `PaymentTier` enum with a fake recurring tier

Reason:
- current enum models continuity tiers
- `$29.99` is a one-time activation, not a subscription tier

### TD2. Introduce Phase-0 Commercial Models
Decision:
- add dedicated Phase-0 commercial state models rather than forcing them into legacy billing rows

Reason:
- clean ownership
- avoids semantic confusion

### TD3. Reuse Telegram Invoice Flow
Decision:
- use native Telegram invoice generation as the default payment transport

Reason:
- already present
- aligned with PRD doctrine

### TD4. Upgrade Credit Is Stored State, Not Pure Copy
Decision:
- the credit bridge must be represented as real state

Reason:
- needed for accurate application
- required for testing
- required to avoid ambiguous operator handling

### TD5. Payment Success and Unlock Propagation Must Be Decoupled But Linked
Decision:
- payment confirmation and entitlement propagation are separate steps with their own receipts

Reason:
- clearer failure handling
- safer retries
- cleaner webhook interop

### TD6. Keep Credit Application Server-Side
Decision:
- do not trust client-side calculation for upgrade credit

Reason:
- billing integrity
- avoids front-end drift

### TD7. Preserve Offer-Copy Variants
Decision:
- the runtime should still support standard vs loyalty-oriented copy variants

Reason:
- current payment eligibility stack already encodes this pattern

---

## §4 Plan

### Phase 1. Model and State Foundations
1. Create `Phase0CommercialState`
2. Create `FirstProofUnlockRequest`
3. Create `FirstProofUnlockReceipt`
4. Create `UpgradeCreditState`
5. Create `UpgradeOfferBridge`
6. Create `Phase0EntitlementState`

### Phase 2. Payment Initiation and Offer Projection
7. Implement `Phase0CommercialBridgeService`
8. Implement free-vs-locked asset surface resolution from `Phase0OutputBundle`
9. Implement first-proof unlock offer projection
10. Implement Telegram invoice payload builder for `$29.99`
11. Implement upgrade offer projection for `$39.99` and `$99.99`

### Phase 3. Post-Payment Propagation
12. Implement first-proof unlock transaction persistence
13. Implement post-payment unlock propagator
14. Implement upgrade credit state creation
15. Implement Telegram-native unlock confirmation messaging
16. Implement release-ready entitlement propagation back into Phase-0 bundle state

### Phase 4. Upgrade Credit Consumption
17. Implement first qualifying upgrade credit calculation
18. Implement one-time credit consumption tracking
19. Implement continuity handoff adapter to existing upgrade flow
20. Implement failure-safe logic for expired or already-consumed credit

### Phase 5. Observability and Safety
21. Add receipt-chain logs for all major transitions
22. Add API routes
23. Add Redis / DB sync strategy
24. Add integration tests for standard, failure, and credit-consumption paths

---

## §5 Schema

### Enum: `Phase0CommercialStage`
- `PROOF_VISIBLE`
- `UNLOCK_OFFER_READY`
- `INVOICE_SENT`
- `PAYMENT_PENDING`
- `PHASE0_UNLOCKED`
- `UPGRADE_BRIDGE_READY`
- `CREDIT_CONSUMED`
- `FAILED`

### Enum: `Phase0EntitlementLevel`
- `PREVIEW_ONLY`
- `PHASE0_UNLOCKED`
- `CONTINUITY_UNLOCKED`
- `COACH_OS_UNLOCKED`

### Pydantic Model: `Phase0CommercialState`
```python
class Phase0CommercialState(BaseModel):
    commercial_state_id: str
    coach_id: str
    phase0_packet_id: str
    delivery_run_id: str
    stage: Literal[
        "PROOF_VISIBLE",
        "UNLOCK_OFFER_READY",
        "INVOICE_SENT",
        "PAYMENT_PENDING",
        "PHASE0_UNLOCKED",
        "UPGRADE_BRIDGE_READY",
        "CREDIT_CONSUMED",
        "FAILED",
    ]
    current_offer_key: str
    phase0_unlock_paid: bool = False
    upgrade_credit_available: bool = False
    upgrade_credit_consumed: bool = False
    telegram_chat_id: int | None = None
    last_invoice_id: str | None = None
    updated_at_utc: datetime
```

### Pydantic Model: `FirstProofUnlockRequest`
```python
class FirstProofUnlockRequest(BaseModel):
    request_id: str
    coach_id: str
    phase0_packet_id: str
    delivery_run_id: str
    telegram_user_id: int
    chat_id: int
    amount_cents: int = Field(default=2999, ge=2999, le=2999)
    currency: str = Field(default="USD")
    offer_copy_variant: Literal["standard", "loyalty_unlock", "phase0_unlock"]
    output_bundle_id: str
    created_at_utc: datetime
```

### Pydantic Model: `FirstProofUnlockReceipt`
```python
class FirstProofUnlockReceipt(BaseModel):
    receipt_id: str
    request_id: str
    coach_id: str
    phase0_packet_id: str
    invoice_id: str | None = None
    transaction_id: str | None = None
    amount_cents: int = Field(default=2999, ge=2999)
    payment_status: Literal[
        "INVOICE_SENT",
        "PRE_CHECKOUT_CONFIRMED",
        "REQUIRES_ACTION",
        "PAYMENT_SUCCESSFUL",
        "PAYMENT_FAILED",
        "REWARD_DISPATCHED",
        "PROVISIONING_COMPLETE",
    ]
    unlock_propagated: bool = False
    created_at_utc: datetime
    completed_at_utc: datetime | None = None
```

### Pydantic Model: `UpgradeCreditState`
```python
class UpgradeCreditState(BaseModel):
    credit_state_id: str
    coach_id: str
    phase0_packet_id: str
    source_unlock_receipt_id: str
    original_amount_cents: int = Field(default=2999, ge=2999)
    remaining_amount_cents: int = Field(default=2999, ge=0, le=2999)
    eligible_target_tiers: tuple[Literal["SPEAKING_LEARNING", "COACH_OS"], Literal["SPEAKING_LEARNING", "COACH_OS"]]
    valid_until_utc: datetime
    consumed: bool = False
    consumed_at_utc: datetime | None = None
    consumed_by_target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"] | None = None
```

### Pydantic Model: `UpgradeOfferBridge`
```python
class UpgradeOfferBridge(BaseModel):
    bridge_id: str
    coach_id: str
    phase0_packet_id: str
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"]
    base_amount_cents: int = Field(ge=0)
    applied_credit_cents: int = Field(ge=0)
    final_amount_cents: int = Field(ge=0)
    bridge_copy: str
    credit_state_id: str | None = None
    expires_at_utc: datetime | None = None
```

### Pydantic Model: `Phase0EntitlementState`
```python
class Phase0EntitlementState(BaseModel):
    entitlement_state_id: str
    coach_id: str
    phase0_packet_id: str
    output_bundle_id: str
    entitlement_level: Literal[
        "PREVIEW_ONLY",
        "PHASE0_UNLOCKED",
        "CONTINUITY_UNLOCKED",
        "COACH_OS_UNLOCKED",
    ]
    visible_asset_keys: list[str]
    downloadable_asset_keys: list[str]
    ownership_granted: bool = False
    audit_pdf_unlocked: bool = False
    audit_video_unlocked: bool = False
    proof_package_unlocked: bool = False
    updated_at_utc: datetime
```

### Auxiliary Model: `Phase0UpgradeInvoiceRequest`
```python
class Phase0UpgradeInvoiceRequest(BaseModel):
    telegram_user_id: int
    chat_id: int
    coach_id: str
    phase0_packet_id: str
    target_tier: Literal["SPEAKING_LEARNING", "COACH_OS"]
    credit_state_id: str | None = None
    applied_credit_cents: int = Field(default=0, ge=0)
```

### Auxiliary Model: `Phase0UnlockProjection`
```python
class Phase0UnlockProjection(BaseModel):
    coach_id: str
    phase0_packet_id: str
    current_stage: str
    free_visible_assets: list[str]
    locked_assets: list[str]
    unlock_offer_title: str
    unlock_offer_summary: str
    amount_cents: int = Field(default=2999)
    telegram_native: bool = True
```

---

## §6 Fallback

### F1. Delivery Bundle Not Ready
If `Phase0OutputBundle.payment_handoff_ready` is false:
- no unlock offer may be projected
- commercial state remains upstream-blocked

### F2. Invoice Send Failure
If Telegram invoice send fails:
- commercial stage moves to `FAILED`
- no unlock propagation occurs
- operator retry allowed

### F3. Payment Pending / In-Flight
If a matching pending transaction exists:
- return pending state
- do not generate duplicate first-proof invoices

### F4. Payment Failed
If payment fails:
- keep assets in preview-only state
- preserve retryable unlock offer
- no ownership grant

### F5. Unlock Propagation Failure After Payment Success
If payment succeeds but entitlement propagation fails:
- mark `PAYMENT_SUCCESSFUL` but `unlock_propagated=False`
- create operator-visible repair state
- do not silently claim success

### F6. Credit State Missing on Upgrade Attempt
If a user should have credit but no `UpgradeCreditState` exists:
- fail closed
- require operator repair
- do not silently charge full continuity amount without explicit design approval

### F7. Credit Expired
If credit validity has expired:
- allow upgrade
- do not apply credit
- surface clear “continuation window expired” copy

### F8. Credit Already Consumed
If credit was already consumed:
- no second application
- standard upgrade invoice flow resumes

---

## §7 Tasks

### T1. Create `phase0_commercial_models.py`
Define all canonical models in this spec.

### T2. Create `phase0_commercial_bridge.py`
Implement:
- offer projection
- first unlock initiation
- unlock-state management
- credit-state creation

### T3. Create first-proof unlock invoice adapter
Use Telegram-native invoice transport for `$29.99`.

### T4. Create `phase0_unlock_propagator.py`
Implement post-payment state transitions:
- entitlement update
- bundle release state
- credit state creation

### T5. Add persistence contracts
Recommended storage families:
- `phase0_commercial_states`
- `phase0_unlock_receipts`
- `phase0_upgrade_credit_states`
- `phase0_entitlement_states`

### T6. Add bridge projection API
Suggested routes:
- `GET /api/phase0/commercial/{phase0_packet_id}/projection`
- `POST /api/phase0/commercial/{phase0_packet_id}/unlock`

### T7. Add payment callback adapter
Link successful payment events to unlock propagation.

### T8. Add continuity upgrade bridge adapter
Allow `$39.99` / `$99.99` invoice requests to consume valid credit.

### T9. Add receipt-chain logging
Log:
- unlock projected
- invoice sent
- payment confirmed
- unlock propagated
- credit created
- credit consumed

### T10. Add operator-repair pathways
Support:
- resend invoice
- retry unlock propagation
- repair credit state

### T11. Add Telegram-native copy templates
Separate:
- proof unlock invitation
- unlock success
- continuity bridge invitation

### T12. Add tests
Cover:
- standard proof unlock
- payment failure
- unlock propagation failure
- upgrade credit application
- expired credit

---

## §8 AC

### AC1
When visible proof exists and the bundle is payment-handoff-ready, the system can project a `$29.99` first proof unlock offer.

### AC2
The system distinguishes preview visibility from owned unlocked state.

### AC3
The first proof unlock is represented as a one-time activation, not as a fake monthly tier.

### AC4
The system can generate and send a Telegram-native invoice for the `$29.99` unlock.

### AC5
After successful payment, the system propagates a Phase-0 entitlement state and marks the proof package unlocked.

### AC6
After successful first proof unlock, the system creates an `UpgradeCreditState` worth `2999` cents.

### AC7
The first qualifying upgrade to `$39.99` or `$99.99` consumes the credit exactly once.

### AC8
The system can produce a clean bridge offer showing:
- target tier
- base amount
- applied credit
- final amount

### AC9
If the unlock payment fails, the user remains preview-only and no ownership is granted.

### AC10
If unlock propagation fails after payment success, the system records a repairable inconsistent state instead of silently marking completion.

### AC11
The runtime interoperates with existing Telegram invoice flow rather than inventing a browser checkout path.

### FAILURE EXAMPLE
Bad behavior that must be rejected:
- user pays `$29.99`
- payment succeeds
- full package is still locked
- no credit state is created
- operator has no receipt trail

This is a hard failure because it violates:
- proof-to-activation trust
- clean bridge continuity
- Telegram-native commercial reliability

---

## §9 Dependencies

### Confirmed Present in Workspace
- `PaymentFlowOrchestrator`
- `PaymentEligibilityService`
- `TelegramInvoiceHandler`
- `BillingWebhookHandler`
- `BillingMiddleware`
- `OfferTierGovernor`
- `PaymentTier`
- `EligibilityCheckResult`
- `InvoicePayload`

### Required New Models / Services
- `Phase0CommercialState`
- `FirstProofUnlockRequest`
- `FirstProofUnlockReceipt`
- `UpgradeCreditState`
- `UpgradeOfferBridge`
- `Phase0EntitlementState`
- `Phase0CommercialBridgeService`
- `Phase0UnlockPropagator`

### Dependency Rule
This spec depends on `FR-ERA3-36` for package-readiness truth.
It must not independently decide that assets are releasable without consulting delivery/orchestration state.

### Future Integration Touchpoints
- `FR-ERA3-38` Operator Console and SLA Tracker
- `FR-ERA3-39` Campaign Frontend
- `FR-ERA3-40` Batch Review Board

---

## §10 Testing

### Unit Tests
- project unlock offer when bundle is ready
- reject unlock offer when bundle is not ready
- create first-proof unlock request
- create upgrade credit state after successful unlock
- compute upgrade bridge final price correctly
- reject double credit consumption

### Integration Tests
- visible proof -> `$29.99` invoice -> payment success -> entitlement unlock
- visible proof -> `$29.99` invoice -> payment failure -> preview-only preserved
- `$29.99` unlock -> `$39.99` upgrade -> credit applied
- `$29.99` unlock -> `$99.99` upgrade -> credit applied

### Failure Tests
- pending payment blocks duplicate invoice
- unlock propagation failure creates repair state
- missing credit state blocks incorrect discounted upgrade
- expired credit no longer applies

### Telegram-Native Tests
- invoice payload uses Telegram-native fields
- no external checkout URL is required
- unlock confirmation is emitted through Telegram-facing path

### Regression Tests
- free assets remain visible before payment
- paid assets remain locked before payment
- continuity credit remains one-time only
- post-payment propagation never bypasses receipt logging

### Build Notes and Future Integration
This spec intentionally bridges into current `$39.99/$99.99` machinery without mutating their core enum semantics.

That means the first implementation should:
- keep `$29.99` as Phase-0 commercial state
- leave recurring `PaymentTier` focused on continuity tiers
- connect Phase-0 unlock completion to the existing continuity invoice runtime through adapters

This preserves speed now and avoids a messy commercial state collapse later.
