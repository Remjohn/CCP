# Tech-Spec: FR-ERA3-02 — In-Chat Telegram Payments
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — CBAR-Hardened)
**Phase:** 1 — Infrastructure
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md §7

---

## Pre-Work Log

```
1. PROTOCOL LOADED:   §2.1 Stack Summary confirms FastAPI (Python) at src/ccp/api/main.py,
                      Supabase (PostgreSQL) with RLS, Redis cache, Telegram Webhook → VidyeRouter.
2. PRD LOADED:        PRD-09 §1.2 FR definition: "Frictionless checkout for the $39.99/mo Speaking
                      & Learning and $99.99/mo Coach OS tiers natively inside the Telegram chat or
                      Telegram Mini App using the Telegram Payments API (e.g., Stripe integration
                      inside TMA)."
3. EPIC LOADED:       Story 3.1 AC: "Given I trigger an upgrade intent, When the system generates
                      the invoice, Then it queries both stripe_status and cumulative_assets_stored
                      from the asset_manager, And it triggers a tailored 'Loyalty Unlock' offer flow
                      if I have high stored value but low billing status."
4. CBAR AUDIT LOADED: Phase1-M06 (The Stored Value Rule) and Phase1-M07 (The Payment Masking Rule)
                      confirmed in CBAR_Audit_Phase1_Infrastructure.md §3.1 and §3.3.
5. PRIMITIVES LOADED: EXP-PER-003 id:"EXP-PER-003" name:"Cumulative Investment"
                      EXP-FBK-001 id:"EXP-FBK-001" name:"RIM Feedback Discipline"
                      EXP-FRC-003 id:"EXP-FRC-003" name:"The B=MAP Friction Audit"
6. BACKEND FILES READ:offer_tier_governor.py — OfferTierGovernor.evaluate(*, client_id: str,
                        coping_position: int | None, target_campaign_tier: int,
                        historical_purchased_tiers: list[Any] | None = None) -> OfferTierGovernorRow
                      conversion_sequence_router.py — ConversionSequenceRouter.route(*, client_id: str,
                        spt_stage: int | None, hours_since_last_message: float,
                        current_sequence_step: int, next_payload_string: str | None)
                        -> ConversionSequencePayloadRow
                      lead_capture_service.py — LeadCaptureService.check_cooldown(lead: TriviaLead)
                        -> CooldownCheck
                      telegram_webhook.py — router.post("/telegram/webhook") async def
                        telegram_webhook(request: Request)
                      circuit_breaker.py — CircuitBreaker.scan_for_crisis(text: str) -> bool
7. TEST PATTERN:      test_cpsc_fr58_offer_tier.py + test_cpsc_fr53_conversion_sequence.py read.
                      Pattern: pytest classes per component, @pytest.fixture for ReceiptChain(tmp_path),
                      parametrized boundary tests, explicit AC test class, receipt chain verification,
                      ADR-01 isolation tests, edge case classes.
```

---

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|------|-------------|---------|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | 2026-05-11 | Master protocol — stack, routes, DB, format |
| 2 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | v7.0 2026-05-09 | Source PRD — pricing, billing, payments FR |
| 3 | `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md` | 2026-05-10 | Epic 3 stories 3.1–3.3, 7 CBAR mandates |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase1_Infrastructure.md` | 2026-05-10 | Adversarial audit — M06/M07 resolutions |
| 5 | `primitives/experience/personalization_identity/EXP-PER-003.yaml` | Codified | Cumulative Investment — stored value |
| 6 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified | RIM Feedback Discipline |
| 7 | `primitives/experience/friction_ability/EXP-FRC-003.yaml` | Codified | B=MAP Friction Audit |
| 8 | `src/ccp/services/offer_tier_governor.py` | FR58 | Tier ceiling + upward-only gate |
| 9 | `src/ccp/services/lead_capture_service.py` | FR-CA11-20 | Cooldown check, lead state |
| 10 | `src/ccp/services/conversion_sequence_router.py` | FR53 | Dormancy gate pattern |
| 11 | `src/ccp/api/telegram_webhook.py` | Task 3.01 | Existing webhook handler |
| 12 | `src/ccp/api/main.py` | 1.0.0 | FastAPI app — router registration |
| 13 | `src/ccp/core/circuit_breaker.py` | Task 3.08 | Graceful degradation pattern |
| 14 | `src/ccp/models/cpsc_models.py` | CPSC | Existing Pydantic models |
| 15 | `tests/integration/test_cpsc_fr58_offer_tier.py` | FR58 | Test pattern reference |
| 16 | `tests/integration/test_cpsc_fr53_conversion_sequence.py` | FR53 | Test pattern reference |

---

## 2. Overview

### 2.1 Problem Statement — What breaks without this spec?

Without in-chat payments, a user who reaches peak emotional momentum (e.g., after a high biometric score or a debate win) must leave Telegram, open an external browser, navigate a checkout portal, and enter credit card details. This context-switch destroys the System 1 emotional state, causing conversion abandonment. PRD-09 §1.2 explicitly marks external web checkout portals as `[OBSOLETE]`. Additionally, without stored-value-aware eligibility checks, the system sends generic beginner upgrade pitches to high-investment free users — violating their trust and causing churn.

### 2.2 Solution

This spec builds three net-new components: (1) a **Payment Eligibility Service** that consumes `offer_tier_governor.py` and enriches it with `cumulative_assets_stored` to produce investment-aware offer flows, (2) a **Telegram Invoice Handler** that generates native `sendInvoice` payloads via the Telegram Bot API with Stripe as the payment provider, and (3) a **Stripe Webhook Processor** that handles `successful_payment` events, updates tenant records, and immediately pushes a pre-rendered experiential reward asset via the Telegram bot to mask backend provisioning latency. All three components integrate into the existing FastAPI app at `src/ccp/api/main.py`.

### 2.3 Scope

**In scope:**
- Payment eligibility check combining `stripe_status` + `cumulative_assets_stored`
- Loyalty Unlock flow for high-investment free users
- Native Telegram `sendInvoice` generation for $39.99 / $99.99 tiers
- SCA (`requires_action`) friction mitigation via reassuring bot messages
- Stripe webhook handler for `invoice.payment_succeeded`
- Instant experiential reward delivery (pre-rendered asset push) on payment success
- Background Coach OS provisioning orchestration
- Receipt chain logging for all payment events
- Pydantic v2 models extending `src/ccp/models/cpsc_models.py`

**Out of scope:**
- $199.99 Operator tier (unadvertised, manual onboarding)
- $9.99 à la carte video purchases (separate spec)
- Stripe merchant account setup (assumed existing)
- Church/B2B2C institutional billing
- Refund processing
- Subscription management portal
- Mini App payment surface (this spec covers in-chat bot payments only)

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|--------|-----------|----------|--------------|
| DEP-PAY-001 | `PaymentEligibilityService` | FR-ERA3-02, Story 3.1 | Combines billing state + stored value for eligibility |
| DEP-PAY-002 | `TelegramInvoiceHandler` | FR-ERA3-02, Story 3.2 | Generates native Telegram `sendInvoice` payloads |
| DEP-PAY-003 | `StripeWebhookProcessor` | FR-ERA3-02, Story 3.3 | Handles `invoice.payment_succeeded`, triggers reward + provisioning |
| DEP-PAY-004 | `PaymentRewardDispatcher` | FR-ERA3-02, Story 3.3 | Pushes pre-rendered experiential reward via Telegram bot |
| DEP-PAY-005 | `CoachOSProvisioningResult` | FR-ERA3-02, Story 3.3 | Payload of background provisioning (vector namespace, Voice DNA) |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `offer_tier_governor.py` | `src/ccp/services/` | **CONSUMED** — `OfferTierGovernor.evaluate()` called to resolve tier ceiling before invoice generation. This spec adds a wrapper that enriches the evaluation with `cumulative_assets_stored`. |
| `telegram_webhook.py` | `src/ccp/api/` | **EXTENDED** — New `pre_checkout_query` and `successful_payment` message types added to `_classify_message()`. The Stripe webhook is a separate endpoint but the Telegram payment callbacks flow through the existing webhook. |
| `lead_capture_service.py` | `src/ccp/services/` | **READ** — `LeadCaptureService.check_cooldown()` consulted to ensure commercial cooldown is respected before showing upgrade offers. |
| `main.py` | `src/ccp/api/` | **EXTENDED** — New `payment_router` registered via `app.include_router()`. |
| `circuit_breaker.py` | `src/ccp/core/` | **PATTERN REFERENCE** — Graceful degradation pattern for Stripe API failures follows `CircuitBreaker` state machine approach. |
| `cpsc_models.py` | `src/ccp/models/` | **EXTENDED** — New payment enums and Pydantic models appended. |
| `receipt_chain.py` | `src/ccp/core/` | **CONSUMED** — All payment events logged to immutable audit trail. |

**Database tables consumed:**
- `receipt_chain` — immutable audit log for payment events
- `person_registry` — `telegram_user_id` → `person_id` resolution
- `asset_registry` — `cumulative_assets_stored` count query

**Database tables created:**
- `payment_transactions` — payment state machine (NEW)
- `tier_subscriptions` — active subscription tracking (NEW)

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|-------------|------|--------|-------------------|
| `EXP-PER-003` | Cumulative Investment | PER | Eligibility must combine `stripe_status` with `cumulative_assets_stored`. Generic beginner pitches to high-investment free users are banned. High stored value triggers Loyalty Unlock flow. |
| `EXP-FBK-001` | RIM Feedback Discipline | FBK | Payment confirmation must be Relevant (tier-specific), Immediate (millisecond of webhook), Meaningful (experiential reward, not text). Pre-rendered asset masks provisioning latency. |
| `EXP-FRC-003` | The B=MAP Friction Audit | FRC | Checkout must use native Telegram payment (1 tap). External browser redirects are banned. SCA friction mitigated with reassuring in-chat messages. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---------|----------|-------------|------------------------|
| **The Stored Value Rule** | Phase1-M06 | Story 3.1 | `PaymentEligibilityService` queries both `stripe_status` (from `tier_subscriptions` table) AND `cumulative_assets_stored` (from `asset_registry` count). If `assets_stored >= LOYALTY_THRESHOLD` AND `stripe_status == 'free'`, the service returns a `LOYALTY_UNLOCK` offer type with tailored copy acknowledging the user's investment history. Generic upgrade copy is never served to high-investment users. |
| **The Payment Masking Rule** | Phase1-M07 | Story 3.3 | `StripeWebhookProcessor` immediately calls `PaymentRewardDispatcher.push_reward()` which sends a pre-built video/audio asset via `sendVideo`/`sendAudio` Telegram Bot API. This asset is pre-rendered and stored in the `visual-assets` Supabase bucket — NOT generated at payment time. `CoachOSProvisioningOrchestrator` runs asynchronously in background. The user consumes the 30-60s reward asset while provisioning completes. "Not ready" errors are impossible because the reward is the immediate response. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|---------------------|-------------|
| Use Telegram Bot API `sendInvoice` (not Mini App payments) | PRD-09 §8.1 specifies in-chat payment. Bot API `sendInvoice` creates native payment buttons directly in the chat. | Telegram Mini App `WebApp.openInvoice()` | Out of scope — Mini App payment surface is a separate concern. In-chat payment maximizes System 1 momentum. |
| Stripe as sole payment provider | Telegram Payments API requires a payment provider. Stripe is the most mature provider with SCA support. | LiqPay, Sberbank, other Telegram-supported providers | Stripe has the strongest SCA handling, webhook infrastructure, and is already referenced in PRD-09 §1.2. |
| Pre-rendered reward assets (not real-time generated) | Spec-specific context mandates pre-built media. Eliminates generation latency risk entirely. | Real-time generated welcome video | Generation latency (10-30s) would create the exact "Not ready" state that M07 bans. Pre-rendered assets guarantee sub-second delivery. |
| Separate `/api/stripe/webhook` endpoint | Stripe webhooks are server-to-server with signature verification. Mixing with Telegram webhook adds complexity. | Route Stripe events through existing Telegram webhook | Different authentication models (Telegram secret token vs Stripe signature). Separation enforces clean security boundaries. |
| `asyncio.create_task()` for background provisioning | Non-blocking provisioning allows instant reward dispatch. | Sequential provisioning before reward | Would violate M07 — user waits 30-60s staring at "processing". |

---

## 4. Implementation Plan

### Phase 1: Data Models & Schema (Tasks 1-3)

- [ ] **Task 1:** Create payment enums (`PaymentTier`, `PaymentStatus`, `EligibilityVerdict`, `PaymentError`) in `src/ccp/models/cpsc_models.py`
- [ ] **Task 2:** Create Pydantic models (`EligibilityCheckResult`, `InvoicePayload`, `PaymentTransactionRow`, `TierSubscriptionRow`, `RewardDispatchResult`) in `src/ccp/models/cpsc_models.py`
- [ ] **Task 3:** Add `payment_transactions` and `tier_subscriptions` table DDL to `src/ccp/scripts/setup_supabase.py`

### Phase 2: Payment Eligibility Service (Tasks 4-6)

- [ ] **Task 4:** Create `src/ccp/services/payment_eligibility_service.py` with `StoredValueResolver` class that queries `asset_registry` for `cumulative_assets_stored` count, checks Voice DNA status for `voice_dna_trained`, and counts archive/reaction DB entries to populate `content_archive_count` and `reaction_count`.
- [ ] **Task 5:** Create `EligibilityGate` class that combines `OfferTierGovernor.evaluate()` output with `StoredValueResolver` output to produce `EligibilityCheckResult`, including resolving a `PROVISIONAL_PENDING_PAYMENT` verdict if an incomplete payment is active.
- [ ] **Task 6:** Create `PaymentEligibilityService` orchestrator class with `check_eligibility(*, telegram_user_id: int, coach_id: str, target_tier: PaymentTier) -> EligibilityCheckResult` method, including Loyalty Unlock logic and receipt chain logging

### Phase 3: Telegram Invoice Handler (Tasks 7-9)

- [ ] **Task 7:** Create `src/ccp/services/telegram_invoice_handler.py` with `InvoiceBuilder` class that constructs `sendInvoice` JSON payloads per Telegram Bot API spec
- [ ] **Task 8:** Create `SCAFrictionMitigator` class with `send_reassurance(chat_id: int) -> None` that sends high-status identity-affirming Telegram message during 3D Secure flows
- [ ] **Task 9:** Create `TelegramInvoiceHandler` orchestrator with `generate_and_send(*, chat_id: int, eligibility: EligibilityCheckResult) -> InvoicePayload` method

### Phase 4: Stripe Webhook & Fulfillment (Tasks 10-14)

- [ ] **Task 10:** Create `src/ccp/api/stripe_webhook.py` with FastAPI router, Stripe signature verification, and `POST /api/stripe/webhook` endpoint
- [ ] **Task 11:** Create `src/ccp/services/payment_reward_dispatcher.py` with `push_reward(chat_id: int, tier: PaymentTier) -> RewardDispatchResult` that sends pre-rendered video/audio asset via Telegram Bot API `sendVideo`
- [ ] **Task 12:** Create `src/ccp/services/coach_os_provisioning.py` with `provision_async(coach_id: str, telegram_user_id: int, tier: PaymentTier) -> CoachOSProvisioningResult` that runs vector namespace creation + Voice DNA init as background task, and explicitly writes a receipt chain entry upon completion.
- [ ] **Task 13:** Create `StripeWebhookProcessor` in `src/ccp/services/stripe_webhook_processor.py` that orchestrates: DB update → reward dispatch → background provisioning → receipt chain
- [ ] **Task 13.5:** Create `SubscriptionReconciliationHandler` to process `customer.subscription.deleted` and `invoice.payment_failed` webhooks to keep `tier_subscriptions` table synchronized with Stripe.
- [ ] **Task 14:** Register `stripe_router` in `src/ccp/api/main.py` via `app.include_router()`

### Phase 5: Integration & Telegram Webhook Extension (Tasks 15-16)

- [ ] **Task 15:** Extend `_classify_message()` in `src/ccp/api/telegram_webhook.py` to handle `pre_checkout_query` and `successful_payment` update types (for Telegram-side checkout acknowledgement only; fulfillment is driven by Stripe webhook).
- [ ] **Task 16:** Create `src/ccp/services/payment_flow_orchestrator.py` that wires eligibility check → invoice generation → webhook processing into a single coherent flow callable by `VidyeRouter`

---

## 5. Primary Output Schema

```python
# Appended to src/ccp/models/cpsc_models.py

# ══════════════════════════════════════════════════════════════════════
# FR-ERA3-02 — In-Chat Telegram Payments
# ══════════════════════════════════════════════════════════════════════

class PaymentTier(str, Enum):
    """Pricing tiers from PRD-09 §3."""
    SPEAKING_LEARNING = "SPEAKING_LEARNING"     # $39.99/mo
    COACH_OS = "COACH_OS"                       # $99.99/mo

class PaymentStatus(str, Enum):
    """Payment transaction lifecycle states."""
    INVOICE_SENT = "INVOICE_SENT"
    PRE_CHECKOUT_CONFIRMED = "PRE_CHECKOUT_CONFIRMED"
    REQUIRES_ACTION = "REQUIRES_ACTION"         # SCA/3D Secure
    PAYMENT_SUCCESSFUL = "PAYMENT_SUCCESSFUL"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    REWARD_DISPATCHED = "REWARD_DISPATCHED"
    PROVISIONING_COMPLETE = "PROVISIONING_COMPLETE"

class EligibilityVerdict(str, Enum):
    """Eligibility check outcomes."""
    PASS_STANDARD = "PASS_STANDARD"
    PASS_LOYALTY_UNLOCK = "PASS_LOYALTY_UNLOCK"
    PROVISIONAL_PENDING_PAYMENT = "PROVISIONAL_PENDING_PAYMENT"
    FAIL_ALREADY_SUBSCRIBED = "FAIL_ALREADY_SUBSCRIBED"
    FAIL_TIER_EXCEEDED = "FAIL_TIER_EXCEEDED"
    FAIL_COOLDOWN_ACTIVE = "FAIL_COOLDOWN_ACTIVE"

class PaymentError(str, Enum):
    """Hard-abort error codes for FR-ERA3-02."""
    FAIL_ALREADY_SUBSCRIBED = "FAIL_ALREADY_SUBSCRIBED"
    FAIL_TIER_EXCEEDED = "FAIL_TIER_EXCEEDED"
    FAIL_STRIPE_ERROR = "FAIL_STRIPE_ERROR"
    FAIL_SIGNATURE_INVALID = "FAIL_SIGNATURE_INVALID"

# ── Constants ──────────────────────────────────────────────────────────

LOYALTY_ASSET_THRESHOLD: int = 50        # cumulative_assets_stored >= 50 triggers Loyalty Unlock
TIER_PRICE_MAP: dict[str, int] = {
    "SPEAKING_LEARNING": 3999,           # cents
    "COACH_OS": 9999,                    # cents
}

# ── Models ─────────────────────────────────────────────────────────────

class StoredValueSnapshot(BaseModel):
    """Snapshot of user's cumulative platform investment."""
    cumulative_assets_stored: int = Field(..., ge=0)
    voice_dna_trained: bool = Field(default=False)
    content_archive_count: int = Field(default=0, ge=0)
    reaction_count: int = Field(default=0, ge=0)

class EligibilityCheckResult(BaseModel):
    """Primary output — eligibility evaluation (DEP-PAY-001)."""
    eligibility_id: str = Field(...)
    telegram_user_id: int = Field(...)
    coach_id: str = Field(...)
    target_tier: str = Field(...)
    current_stripe_status: str = Field(...)
    stored_value: StoredValueSnapshot = Field(...)
    verdict: str = Field(...)
    offer_copy_variant: str = Field(...)    # "standard" | "loyalty_unlock"
    evaluated_at: str = Field(...)

class InvoicePayload(BaseModel):
    """Telegram sendInvoice payload (DEP-PAY-002)."""
    invoice_id: str = Field(...)
    chat_id: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    payload: str = Field(...)               # internal tracking payload
    provider_token: str = Field(...)
    currency: str = Field(default="USD")
    prices: list[dict[str, int | str]] = Field(...)
    tier: str = Field(...)
    sent_at: str = Field(...)

class PaymentTransactionRow(BaseModel):
    """Payment transaction record (DEP-PAY-003)."""
    transaction_id: str = Field(...)
    telegram_user_id: int = Field(...)
    coach_id: str = Field(...)
    tier: str = Field(...)
    amount_cents: int = Field(..., gt=0)
    status: str = Field(...)
    stripe_charge_id: str = Field(default="")
    eligibility_id: str = Field(...)
    reward_dispatched: bool = Field(default=False)
    provisioning_complete: bool = Field(default=False)
    created_at: str = Field(...)
    updated_at: str = Field(...)

class TierSubscriptionRow(BaseModel):
    """Active subscription tracking record."""
    subscription_id: str = Field(...)
    telegram_user_id: int = Field(...)
    coach_id: str = Field(...)
    tier: str = Field(...)
    stripe_subscription_id: str = Field(default="")
    status: str = Field(default="active")
    started_at: str = Field(...)

class RewardDispatchResult(BaseModel):
    """Result of experiential reward push (DEP-PAY-004)."""
    dispatch_id: str = Field(...)
    chat_id: int = Field(...)
    tier: str = Field(...)
    asset_type: str = Field(...)            # "video" | "audio"
    asset_url: str = Field(...)
    telegram_message_id: int = Field(default=0)
    dispatched_at: str = Field(...)

class CoachOSProvisioningResult(BaseModel):
    """Result of background provisioning (DEP-PAY-005)."""
    provisioning_id: str = Field(...)
    telegram_user_id: int = Field(...)
    tier: str = Field(...)
    vector_namespace_created: bool = Field(...)
    voice_dna_initialized: bool = Field(...)
    completed_at: str = Field(...)
```

---

## 6. Backward Compatibility Fallback

Following the `circuit_breaker.py` pattern from `src/ccp/core/`:

| Failure Mode | Degradation Strategy |
|-------------|---------------------|
| **Stripe API unreachable** | `PaymentCircuitBreaker` trips after 3 consecutive failures within 60s. System falls back to sending a deep-link URL to a Stripe checkout session (external browser). Receipt chain logs the fallback with `action="payment-circuit-breaker-fallback"`. Circuit auto-resets after 300s. |
| **`asset_registry` query fails** | `StoredValueResolver` returns `StoredValueSnapshot(cumulative_assets_stored=0, ...)` — eligibility proceeds with standard (non-loyalty) flow. Receipt logs `action="stored-value-fallback"`. |
| **`offer_tier_governor.py` raises `ValueError`** | `PaymentEligibilityService` catches `FAIL_CAPACITY_EXCEEDED`, returns `EligibilityCheckResult` with `verdict=FAIL_TIER_EXCEEDED`. No invoice sent. User receives a Telegram message explaining they need to progress further. |
| **Pre-rendered reward asset missing from bucket** | `PaymentRewardDispatcher` falls back to a text-based congratulation message with a rich Telegram `sendPhoto` using a static branded image. Receipt logs `action="reward-asset-fallback"`. |
| **Background provisioning fails** | `CoachOSProvisioningOrchestrator` retries 3 times with exponential backoff (2s, 4s, 8s). On final failure, logs to receipt chain and notifies operator via the existing `scheduled_monitor_service.py` alerting pattern. User still has the reward asset; provisioning is retried by cron. |
| **Telegram `sendInvoice` API fails** | Returns graceful error message to user: "Payment is temporarily unavailable. Please try again in a few minutes." Receipt logs the Telegram API error. |

---

## 7. Tasks

### Sprint 1: Models & Schema
- [ ] Create `PaymentTier`, `PaymentStatus`, `EligibilityVerdict`, `PaymentError` enums in `src/ccp/models/cpsc_models.py`
- [ ] Create `StoredValueSnapshot`, `EligibilityCheckResult`, `InvoicePayload`, `PaymentTransactionRow`, `TierSubscriptionRow`, `RewardDispatchResult` models in `src/ccp/models/cpsc_models.py`
- [ ] Add `payment_transactions` table DDL in `src/ccp/scripts/setup_supabase.py`
- [ ] Add `tier_subscriptions` table DDL in `src/ccp/scripts/setup_supabase.py`

### Sprint 2: Eligibility Service
- [ ] Create `StoredValueResolver` class in `src/ccp/services/payment_eligibility_service.py`
- [ ] Create `EligibilityGate` class in `src/ccp/services/payment_eligibility_service.py`
- [ ] Create `PaymentEligibilityService` orchestrator in `src/ccp/services/payment_eligibility_service.py`
- [ ] Write unit tests in `tests/integration/test_era3_fr02_payment_eligibility.py`

### Sprint 3: Invoice & SCA
- [ ] Create `InvoiceBuilder` class in `src/ccp/services/telegram_invoice_handler.py`
- [ ] Create `SCAFrictionMitigator` class in `src/ccp/services/telegram_invoice_handler.py`
- [ ] Create `TelegramInvoiceHandler` orchestrator in `src/ccp/services/telegram_invoice_handler.py`
- [ ] Write unit tests in `tests/integration/test_era3_fr02_invoice_handler.py`

### Sprint 4: Webhook & Fulfillment
- [ ] Create `POST /api/stripe/webhook` endpoint in `src/ccp/api/stripe_webhook.py`
- [ ] Create `PaymentRewardDispatcher` in `src/ccp/services/payment_reward_dispatcher.py`
- [ ] Create `CoachOSProvisioningOrchestrator` in `src/ccp/services/coach_os_provisioning.py`
- [ ] Create `StripeWebhookProcessor` in `src/ccp/services/stripe_webhook_processor.py`
- [ ] Register `stripe_router` in `src/ccp/api/main.py`
- [ ] Extend `_classify_message()` in `src/ccp/api/telegram_webhook.py` for `pre_checkout_query` and `successful_payment`
- [ ] Write integration tests in `tests/integration/test_era3_fr02_stripe_webhook.py`

### Sprint 5: Integration & Flow
- [ ] Create `PaymentFlowOrchestrator` in `src/ccp/services/payment_flow_orchestrator.py`
- [ ] Wire `PaymentFlowOrchestrator` into `VidyeRouter` in `src/ccp/agents/vidye_router.py`
- [ ] Write end-to-end integration tests in `tests/integration/test_era3_fr02_payment_flow.py`

---

## 8. Acceptance Criteria

### AC-3.1: Stored Value Eligibility Check (Story 3.1)

**CBAR Mandate Enforced:** Phase1-M06 — The Stored Value Rule

**Given** a Free Tier user with `cumulative_assets_stored >= 50` triggers an upgrade intent,
**When** the `PaymentEligibilityService.check_eligibility()` is called,
**Then** it queries both `stripe_status` (from `tier_subscriptions`) AND `cumulative_assets_stored` (from `asset_registry`),
**And** it returns `EligibilityCheckResult` with `verdict=PASS_LOYALTY_UNLOCK` and `offer_copy_variant="loyalty_unlock"`,
**And** the Loyalty Unlock copy explicitly acknowledges the user's stored value (e.g., "You've built 73 assets and trained your Voice DNA. Your Coach OS is ready.").

**FAILURE EXAMPLE:** A Free Tier user with 150 stored assets and a trained Voice DNA model triggers an upgrade. The system checks only `stripe_status`, sees "free", and sends: "Start your journey with Coach OS for $99.99/mo!" — a generic beginner pitch that ignores their 4-month investment history. The user feels unrecognized and churns. **This is a spec violation.**

**Measurable pass condition:** `verdict == "PASS_LOYALTY_UNLOCK"` when `cumulative_assets_stored >= LOYALTY_ASSET_THRESHOLD (50)` AND `stripe_status == "free"`.

---

### AC-3.2: Native Invoice Generation (Story 3.2)

**CBAR Mandate Enforced:** None directly (inherits from M06 via tailored payload)

**Given** the user is eligible for the $99.99 Coach OS tier (verdict is `PASS_STANDARD` or `PASS_LOYALTY_UNLOCK`),
**When** the `TelegramInvoiceHandler.generate_and_send()` is called,
**Then** it sends a Telegram `sendInvoice` API call with `provider_token` (Stripe), `currency="USD"`, `prices=[{"label": "Coach OS", "amount": 9999}]`,
**And** the invoice renders as a native payment button inside the Telegram chat (not an external link),
**And** if Stripe returns a `requires_action` state, the `SCAFrictionMitigator` sends a reassuring Telegram message: "Your Coach OS credentials are being verified by the banking network. This confirms your elite access."

**FAILURE EXAMPLE:** User taps "Pay $99.99". Instead of a native Telegram payment button, they receive a URL linking to `https://checkout.stripe.com/...`. They must open a browser, wait for the page to load, re-enter card details. Conversion drops 60%. **This is a spec violation.**

**Measurable pass condition:** `InvoicePayload.chat_id` matches the user's Telegram chat. Telegram Bot API `sendInvoice` returns HTTP 200. No external URLs are sent.

---

### AC-3.3: Post-Payment Fulfillment with Masking (Story 3.3)

**CBAR Mandate Enforced:** Phase1-M07 — The Payment Masking Rule

**Given** a successful Stripe webhook fires (`invoice.payment_succeeded`),
**When** the `StripeWebhookProcessor.process()` is called,
**Then** it updates the `payment_transactions` record to `status=PAYMENT_SUCCESSFUL`,
**And** it immediately calls `PaymentRewardDispatcher.push_reward()` which sends a pre-rendered video/audio asset via `sendVideo` / `sendAudio` Telegram Bot API within 2 seconds of webhook receipt,
**And** it launches `CoachOSProvisioningOrchestrator.provision_async()` as a background task (vector namespace creation, Voice DNA profile init),
**And** the user never encounters a "Not ready", "Still provisioning", or empty dashboard state,
**And** a receipt chain entry is logged with `action="payment-fulfillment"` linking the transaction_id,
**And** upon completion of the background task, a separate receipt chain entry is logged with `action="provisioning-complete"`.

**FAILURE EXAMPLE:** Payment succeeds. The system updates the DB and begins a 45-second provisioning script. The user taps the Coach OS button and sees: "Your account is being set up. Please wait..." They feel buyer's remorse. After 60 seconds, they close Telegram. **This is a spec violation.**

**Measurable pass condition:** `RewardDispatchResult.dispatched_at` timestamp is within 2000ms of `PaymentTransactionRow.updated_at` (payment success timestamp). `reward_dispatched == True` before `provisioning_complete == True`.

---

### AC-3.4: Stripe Webhook Signature Verification

**Given** a POST request arrives at `/api/stripe/webhook`,
**When** the endpoint verifies the `Stripe-Signature` header against the webhook signing secret,
**Then** requests with invalid signatures are rejected with HTTP 400,
**And** a receipt chain entry is logged with `action="stripe-signature-rejected"`.

**FAILURE EXAMPLE:** An attacker sends a forged `successful_payment` payload to `/api/stripe/webhook`. The system processes it without signature verification, upgrading a non-paying user to Coach OS. **This is a security violation.**

**Measurable pass condition:** Invalid signature → HTTP 400. Valid signature → HTTP 200.

---

### AC-3.5: Already-Subscribed Guard

**Given** a user who already has an active `COACH_OS` subscription triggers an upgrade intent for `COACH_OS`,
**When** `PaymentEligibilityService.check_eligibility()` is called,
**Then** it returns `verdict=FAIL_ALREADY_SUBSCRIBED`,
**And** no invoice is generated,
**And** the user receives a contextual message: "You already have Coach OS. Your next billing cycle is [date]."

**FAILURE EXAMPLE:** A paying Coach OS user receives another $99.99 invoice prompt. They accidentally pay again, creating a double charge. **This is a spec violation.**

**Measurable pass condition:** `verdict == "FAIL_ALREADY_SUBSCRIBED"` when active subscription exists for requested tier. Zero `sendInvoice` calls made.

---

### AC-3.6: Subscription State Reconciliation

**Given** a user cancels their subscription or a recurring payment fails,
**When** the Stripe `customer.subscription.deleted` or `invoice.payment_failed` webhook arrives,
**Then** the `SubscriptionReconciliationHandler` updates the `tier_subscriptions` table `status` to `canceled` or `past_due`,
**And** logs a receipt chain entry with `action="subscription-reconciliation"`.

**Measurable pass condition:** Stripe cancellation event correctly mirrors into `tier_subscriptions` without manual intervention.

---

### AC-3.7: Provisional State for In-Flight Payments

**Given** a user initiates a checkout but does not immediately complete it (SCA challenge or abandoned cart),
**When** they attempt to trigger another upgrade intent within the timeout window,
**Then** `PaymentEligibilityService.check_eligibility()` returns `verdict=PROVISIONAL_PENDING_PAYMENT`,
**And** the system instructs the user to complete their pending checkout rather than generating a new invoice.

**Measurable pass condition:** In-flight transactions return `PROVISIONAL_PENDING_PAYMENT` and prevent duplicate `sendInvoice` generation.

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|-------------|----------------|------------------------------|
| `offer_tier_governor.py` (FR58) | Runtime consumption | `OfferTierGovernor.evaluate()` for tier ceiling resolution |
| `receipt_chain.py` (Core) | Runtime consumption | `ReceiptChain.log()` for immutable audit trail |
| `lead_capture_service.py` (FR-CA11-20) | Runtime read | `check_cooldown()` to respect 21-day commercial cooldown |
| `telegram_webhook.py` (Task 3.01) | Code extension | `_classify_message()` extended for payment update types |
| `main.py` (Core) | Code extension | New `stripe_router` registered |
| `circuit_breaker.py` (Task 3.08) | Pattern reference | Graceful degradation state machine pattern |
| `cpsc_models.py` (CPSC) | Code extension | New enums and models appended |
| `setup_supabase.py` (Core) | Code extension | New table DDL appended |
| FR-ERA3-08 (Mini App Host Shell) | Deployment dependency | Host shell provides the `startapp=pay` routing for Mini App payment surface (future scope) |

### External

| API/Library | Version | Purpose |
|------------|---------|---------|
| `stripe` (Python SDK) | `>=7.0.0` | Webhook signature verification, charge object parsing |
| Telegram Bot API | v7.x | `sendInvoice`, `answerPreCheckoutQuery`, `sendVideo`, `sendAudio` |
| `httpx` | `>=0.27.0` | Async HTTP client for Telegram Bot API calls (already in use) |
| Supabase PostgreSQL | Existing | `payment_transactions`, `tier_subscriptions` tables |

---

## 10. Testing Strategy

### Unit Tests

**File:** `tests/integration/test_era3_fr02_payment_eligibility.py`

```
class TestStoredValueResolver:
    def test_assets_above_threshold_returns_high_investment()
    def test_assets_below_threshold_returns_standard()
    def test_zero_assets_returns_standard()
    def test_voice_dna_trained_flag_set_correctly()

class TestEligibilityGate:
    def test_free_user_high_assets_loyalty_unlock()
    def test_free_user_low_assets_standard()
    def test_subscribed_user_same_tier_already_subscribed()
    def test_cooldown_active_blocks_eligibility()
    def test_tier_exceeded_from_governor_propagated()

class TestPaymentEligibilityService:
    def test_ac31_stored_value_combined_with_stripe_status()
    def test_loyalty_unlock_copy_variant()
    def test_receipt_logged_on_eligibility_check()
```

**File:** `tests/integration/test_era3_fr02_invoice_handler.py`

```
class TestInvoiceBuilder:
    def test_coach_os_invoice_amount_9999_cents()
    def test_speaking_learning_invoice_amount_3999_cents()
    def test_invoice_currency_usd()
    def test_payload_contains_eligibility_id()

class TestSCAFrictionMitigator:
    def test_reassurance_message_sent_on_requires_action()
    def test_no_raw_stripe_error_codes_in_message()

class TestTelegramInvoiceHandler:
    def test_ac32_native_invoice_no_external_urls()
    def test_invoice_not_sent_for_fail_verdicts()
```

**File:** `tests/integration/test_era3_fr02_stripe_webhook.py`

```
class TestStripeSignatureVerification:
    def test_valid_signature_returns_200()
    def test_invalid_signature_returns_400()
    def test_missing_signature_returns_400()

class TestStripeWebhookProcessor:
    def test_ac33_reward_dispatched_before_provisioning()
    def test_payment_transaction_status_updated()
    def test_receipt_chain_logged_on_success()
    def test_duplicate_webhook_idempotent()
```

### Integration Tests

**File:** `tests/integration/test_era3_fr02_payment_flow.py`

Modeled on `test_cpsc_fr58_offer_tier.py` pattern:

```python
@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="PAY", log_dir=tmp_path)

class TestPaymentFlowEndToEnd:
    """Full eligibility → invoice → webhook → reward → provisioning flow."""

    def test_free_user_standard_upgrade_flow(self, rc):
        """Standard user: eligibility PASS → invoice sent → webhook → reward dispatched."""
        # 1. Check eligibility (low stored value)
        # 2. Verify InvoicePayload generated
        # 3. Simulate successful_payment webhook
        # 4. Assert reward dispatched
        # 5. Assert provisioning triggered
        # 6. Assert receipt chain has 4+ entries

    def test_free_user_loyalty_unlock_flow(self, rc):
        """High-investment free user: PASS_LOYALTY_UNLOCK → tailored invoice → reward."""
        # 1. Set cumulative_assets_stored = 75
        # 2. Check eligibility
        # 3. Assert verdict == PASS_LOYALTY_UNLOCK
        # 4. Assert offer_copy_variant == "loyalty_unlock"
        # 5. Simulate payment + verify reward

    def test_already_subscribed_blocked(self, rc):
        """Coach OS subscriber requesting Coach OS → FAIL_ALREADY_SUBSCRIBED, no invoice."""
        # 1. Create active COACH_OS subscription
        # 2. Check eligibility
        # 3. Assert verdict == FAIL_ALREADY_SUBSCRIBED
        # 4. Assert no sendInvoice call

    def test_receipt_chain_completeness(self, rc):
        """Every payment stage logs to receipt chain."""
        # Verify actions: eligibility-check, invoice-sent, payment-received,
        # reward-dispatched, provisioning-started

class TestCBARMandateEnforcement:
    """Explicit mandate violation detection tests."""

    def test_m06_stored_value_rule_no_generic_pitch_to_invested_user(self, rc):
        """Phase1-M06: User with 100 assets must NOT get generic copy."""
        # Assert offer_copy_variant != "standard" when assets >= 50

    def test_m07_payment_masking_rule_reward_before_provisioning(self, rc):
        """Phase1-M07: Reward timestamp must precede provisioning start."""
        # Assert reward_dispatched_at < provisioning_started_at
```

### Manual Verification

1. **Telegram Bot Test:** Using BotFather test credentials, trigger an upgrade intent in a test chat. Verify the native payment button renders inline (not as a URL).
2. **Stripe Test Mode:** Process a test payment using Stripe test card `4242 4242 4242 4242`. Verify the `successful_payment` webhook fires and the reward video is delivered to the chat within 2 seconds.
3. **SCA Flow Test:** Use Stripe test card `4000 0027 6000 3184` (requires 3D Secure). Verify the reassuring bot message appears during the SCA challenge.
4. **Loyalty Unlock Visual QA:** Create a test user with 75+ assets on the Free tier. Trigger upgrade. Verify the offer copy explicitly references their stored value count.
5. **Double-Subscribe Guard:** With an active Coach OS subscription, trigger another upgrade. Verify no invoice is generated and the contextual "already subscribed" message appears.
6. **Provisioning Latency Test:** After successful payment, time the gap between reward delivery and Coach OS availability. Reward must arrive within 2s; Coach OS must be ready within 60s.
