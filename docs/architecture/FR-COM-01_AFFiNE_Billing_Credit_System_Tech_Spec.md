# Tech-Spec: FR-COM-01 — AFFiNE Billing & Credit System

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0
**Architecture Reference:** ADR-01 (Coach Isolation), SPEC-INFRA-001 §5 (Redis)
**Skill Implementation:** `CBCS/backend/billing/billing_middleware.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/other files/active lab archive/temporary lab/affine_billing_architecture.md` — Stripe metered billing, Redis state, jail system
- `docs/other files/active lab archive/temporary lab/pricing_strategy_analysis.md` — Weekly pricing tiers, $4/user CBCS credits
- `docs/architecture/Infrastructure_AWS_NIM_Deployment_Spec.md` — §5 Redis, §8 Cost thresholds
- `CBCS/backend/database/migrations/003_full_schema.sql` — Existing `payments` table

---

## 2. Overview

### Problem Statement
The CCP operates a multi-tenant SaaS where coaches pay a recurring weekly subscription ($25 or $50) plus metered per-client CBCS credits ($4/user). Currently, the `payments` table in migration 003 records transactions but has no middleware enforcement — a coach can add clients, trigger Telegram bots, and consume GPU resources without a valid payment method. There is no mechanism to block pipeline execution when a subscription lapses, no automated usage reporting to Stripe, and no Redis-cached permission state to avoid querying Stripe on every action. The billing architecture exists only as a prose artifact with no database schema, no API contracts, and no integration with the existing pipeline.

### Solution
FR-COM-01 implements the **Billing Middleware** — a "coin-operated" enforcement layer that sits between every billable coach action and the backend. Every action (add client, request video, deploy CBCS bot) passes through `requireCredits()` middleware that checks the coach's cached permission state in Redis, reports usage to Stripe, and blocks execution if the subscription is inactive. Stripe webhooks update Redis in real-time. A "jail" system prevents abuse (instant usage locking, grace period muting, watermarking for free tiers).

### Scope
**In scope:**
- Stripe Subscriptions with Metered Billing (weekly cycle)
- Redis permission state cache (`coach:{uuid}:status`, `coach:{uuid}:active_clients`)
- Billing Middleware (`requireCredits()`) for all billable endpoints
- Stripe Webhook listener (payment success/failure → Redis update)
- AFFiNE Wallet/Billing Block (dashboard showing current cost)
- Abuse prevention ("jail" system: instant usage lock, muting, watermarking)
- Grace period behavior (read-only mode on payment failure)

**Out of scope:**
- Client-side payment collection (coaches handle their own client billing — Model A)
- Stripe Connect (Model B, future premium feature)
- Pricing tier configuration (business decision, not tech spec — see pricing_strategy_analysis.md)
- GPU cost monitoring (FR-INFRA, handled by CloudWatch kill switch)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-COM-001` | Billing Middleware | OUTPUT — `requireCredits()` function wrapping all billable endpoints. |
| `DEP-COM-002` | Stripe Webhook Handler | OUTPUT — Lambda/endpoint consuming Stripe events. |
| `DEP-COM-003` | Redis Permission State | STATE — Cached coach billing status. |
| `DEP-COM-004` | AFFiNE Wallet Block | OUTPUT — Coach-facing billing dashboard. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Billing events hashed into receipt chain. |
| `SPEC-INFRA-001` §5 | Redis (ElastiCache) | INFRASTRUCTURE — Permission state cache. |

### Technical Decisions

1. **Redis-First, Not Stripe-First:** Every billing check reads from Redis, never from Stripe directly. Stripe is the source of truth, but Redis is the enforcement cache. Webhook reconciliation keeps them in sync. This eliminates Stripe API latency from the critical path.
2. **Instant Usage Lock:** The $4 CBCS charge is locked the moment the Telegram bot sends its FIRST message, not when the coach adds the client. This prevents the "add-and-delete-before-billing" exploit.
3. **Muting, Not Deletion:** When payment fails, client data is preserved but all bots are muted (stop sending messages) and the AFFiNE workspace enters read-only mode. Data is never deleted due to billing issues.
4. **Weekly Billing Cycle:** Aligned with the pricing strategy. Stripe calculates: Base Plan + (reported users × $4) at end of each week.

---

## 4. Implementation Plan

### Stage 1: Stripe Product Setup
*Outputs:* Stripe Product IDs, Price IDs

| Stripe Object | ID Pattern | Configuration |
|---|---|---|
| Product: Base Tier | `prod_ccp_base` | Weekly subscription |
| Price: $25/week | `price_ccp_base_25` | Recurring, weekly interval |
| Price: $50/week | `price_ccp_premium_50` | Recurring, weekly interval |
| Product: CBCS Credits | `prod_ccp_cbcs` | Metered billing |
| Price: $4/user | `price_ccp_cbcs_4` | Metered, sum usage, weekly |

### Stage 2: Billing Middleware
*Inputs:* Coach UUID, action type
*Outputs:* ALLOW or BLOCK

```python
async def require_credits(coach_id: UUID, action: str, cost: int = 0):
    """
    Middleware gate for all billable actions.
    1. Check Redis for coach permission state.
    2. If active → report usage to Stripe → allow action.
    3. If inactive → block action → return billing error.
    """
    status = await redis.get(f"coach:{coach_id}:status")
    
    if status != "active":
        raise BillingError(
            code="SUBSCRIPTION_INACTIVE",
            message="Payment method required. Update card in Wallet.",
            redirect="/wallet"
        )
    
    if cost > 0:
        await stripe.usage_records.create(
            subscription_item=await get_metered_item(coach_id),
            quantity=cost,
            action="increment"
        )
    
    # Write Receipt Chain Guard
    await receipt_chain.write({
        "stage": "BILLING_GATE",
        "agent": "billing_middleware",
        "coach_id": str(coach_id),
        "action": action,
        "cost": cost,
        "status": "ALLOWED"
    })
    
    return True
```

### Stage 3: Stripe Webhook Handler
*Inputs:* Stripe webhook events
*Outputs:* Redis state updates

| Stripe Event | Redis Action |
|---|---|
| `invoice.payment_succeeded` | `SET coach:{uuid}:status active` |
| `invoice.payment_failed` | `SET coach:{uuid}:status past_due` |
| `customer.subscription.deleted` | `SET coach:{uuid}:status cancelled` |
| `customer.subscription.updated` | Update tier in `coach:{uuid}:tier` |

### Stage 4: AFFiNE Wallet Block
*Outputs:* Coach-facing billing dashboard

- Current weekly cost breakdown: Base ($25) + CBCS (N clients × $4) = Total
- Payment status indicator (green/amber/red)
- "Update Card" button → Stripe Elements modal (embedded, never leaves AFFiNE)
- Usage history (last 4 weeks)
- Alert banner on payment failure: "Billing failed. Client bots are paused. [Update Card]"

### Stage 5: Jail System (Abuse Prevention)
*Outputs:* Anti-abuse enforcement rules

| Rule | Trigger | Action |
|---|---|---|
| **Instant Usage Lock** | Telegram bot sends first message to new client | Report +1 usage to Stripe immediately. $4 locked for this cycle. |
| **Grace Period Mute** | `invoice.payment_failed` webhook | Bots stop sending messages. AFFiNE → read-only. Data preserved. |
| **Watermark Enforcement** | Free trial tier active | All generated visuals include CCP watermark. Removed only after `status: active`. |
| **Re-activation** | `invoice.payment_succeeded` after `past_due` | Bots resume. AFFiNE → full access. Watermarks removed. |

---

## 5. Data Model

### Table: `coach_subscriptions`

```sql
CREATE TABLE IF NOT EXISTS coach_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_subscription_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_metered_item_id VARCHAR(50),
    tier VARCHAR(20) NOT NULL DEFAULT 'base' CHECK (tier IN ('free_trial', 'base', 'premium', 'concierge')),
    weekly_base_price_cents INTEGER NOT NULL DEFAULT 2500,
    cbcs_unit_price_cents INTEGER NOT NULL DEFAULT 400,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN (
        'active', 'past_due', 'cancelled', 'trialing', 'paused'
    )),
    payment_method_last4 VARCHAR(4),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    active_client_count INTEGER DEFAULT 0,
    total_weekly_cost_cents INTEGER DEFAULT 2500,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sub_coach ON coach_subscriptions(coach_id);
CREATE INDEX idx_sub_status ON coach_subscriptions(status);

ALTER TABLE coach_subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own subscription"
    ON coach_subscriptions FOR SELECT
    USING (auth.uid() = coach_id);
```

### Table: `billing_events`

```sql
CREATE TABLE IF NOT EXISTS billing_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,                -- 'cbcs_credit', 'subscription_payment', 'payment_failed'
    stripe_event_id VARCHAR(100) UNIQUE,
    amount_cents INTEGER,
    client_id UUID,                                  -- For CBCS credit events
    description TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_billing_coach ON billing_events(coach_id);
CREATE INDEX idx_billing_type ON billing_events(event_type);

ALTER TABLE billing_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own billing events"
    ON billing_events FOR SELECT
    USING (auth.uid() = coach_id);
```

---

## 6. Backward Compatibility

The existing `payments` table (migration 003) is a legacy MVP table. It remains for historical records. New billing events flow through `billing_events` + `coach_subscriptions`. A one-time migration script maps any existing `payments.user_id` entries to `coach_subscriptions.coach_id`.

---

## 7. Tasks

- [ ] **Task 1:** Create Stripe Products and Prices (base $25, premium $50, metered CBCS $4).
- [ ] **Task 2:** Implement `billing_middleware.py` with `require_credits()` function.
- [ ] **Task 3:** Build Stripe webhook handler (4 event types → Redis state updates).
- [ ] **Task 4:** Implement Redis permission state schema (`coach:{uuid}:status`, `coach:{uuid}:active_clients`, `coach:{uuid}:tier`).
- [ ] **Task 5:** Build AFFiNE Wallet Block (cost breakdown, payment status, Stripe Elements modal).
- [ ] **Task 6:** Implement Jail System (instant usage lock, grace period mute, watermark enforcement).
- [ ] **Task 7:** Build payment failure → bot muting integration (webhook → Redis → Telegram bot pause).
- [ ] **Task 8:** Register DEP-COM-001 through DEP-COM-004 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Happy Path):** Coach with active subscription adds a client. Assert: Redis status is `active`, Stripe usage record created (+1), client added successfully, bot provisioned.
- [ ] **AC2 (Payment Block):** Coach with `past_due` status attempts to add a client. Assert: `require_credits()` blocks the action. Error returned: `SUBSCRIPTION_INACTIVE`. Bot NOT provisioned.
- [ ] **AC3 (Instant Usage Lock):** Coach adds client → Telegram bot sends first message. Assert: Stripe usage record created at bot-first-message time (not add-client time). Coach deletes client 2 days later. Assert: $4 charge still applies for this cycle.
- [ ] **AC4 (Grace Period Mute):** `invoice.payment_failed` fires. Assert: Redis status → `past_due`. All coach's Telegram bots stop sending. AFFiNE workspace → read-only. Client data preserved (not deleted).
- [ ] **AC5 (Re-activation):** Coach updates card → payment succeeds. Assert: Redis status → `active`. Bots resume sending. AFFiNE → full access.
- [ ] **AC6 (Wallet Display):** Coach with 4 active clients on $25/week. Assert: Wallet shows "$41/week ($25 base + 4 × $4 CBCS)".

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-COM-001 (Billing Middleware) | Output | `require_credits()` wrapping all billable endpoints. |
| DEP-COM-002 (Webhook Handler) | Output | Stripe → Redis state sync. |
| DEP-COM-003 (Redis Permission State) | State | Cached billing status per coach. |
| DEP-COM-004 (AFFiNE Wallet Block) | Output | Coach-facing billing UI. |
| SPEC-INFRA-001 §5 (Redis) | Infrastructure | ElastiCache for permission cache. |
| Stripe API | External | Subscriptions, Metered Billing, Webhooks, Elements. |
| FR-COM-03 (Telegram Onboarding) | Downstream | Onboarding triggers CBCS usage report. |
| FR-COM-04 (Campaign Manager) | Downstream | Program creation requires active subscription. |

---

## 10. Testing Strategy

### Unit Tests
- **Middleware Gate:** Mock Redis with `status: active` → assert allow. Mock Redis with `status: past_due` → assert block.
- **Usage Reporting:** Mock Stripe API. Assert `require_credits(cost=1)` calls `usage_records.create` with `quantity=1`.

### Integration Tests
- **Full Billing Flow:** Create Stripe test subscription → add client → trigger bot → verify usage record → trigger `invoice.payment_succeeded` webhook → verify Redis state.
- **Failure Recovery:** Trigger `invoice.payment_failed` → verify bot muting → update card → trigger `invoice.payment_succeeded` → verify bot resumption.

### Safety Tests
- **Webhook Replay:** Send the same Stripe webhook event twice. Assert idempotent handling (no double charge, no duplicate Redis update).
- **Redis Failure:** Kill Redis connection. Assert middleware falls back to Stripe API direct query (degraded but functional).
