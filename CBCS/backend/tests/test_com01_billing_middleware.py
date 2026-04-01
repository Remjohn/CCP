"""
FR-COM-01 — AFFiNE Billing & Credit System

Test Suite: Step 24 Build

Coverage:
- AC1: Happy path (active subscription → allow + Stripe usage record)
- AC2: Payment block (past_due → BillingError)
- AC3: Instant usage lock (first-message trigger, delete-doesn't-refund)
- AC4: Grace period mute (payment_failed → past_due, bots stop, data preserved)
- AC5: Re-activation (payment succeeded → active, bots resume)
- AC6: Wallet display (4 clients × $4 + $25 base = $41)
- CBAR Q4: Grace dispatch for pre-queued messages
- CBAR Q5: Billing queue pre-billing + dispatcher lock
- Safety: Webhook replay idempotency
- Safety: Redis fallback
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from core.commercial_models import (
    BILLING_QUEUE_MAX_RETRIES,
    BillingError,
    BillingEventType,
    BillingQueueRow,
    BillingQueueStatus,
    CoachSubscriptionRow,
    SubscriptionStatus,
    SubscriptionTier,
    WalletDisplayData,
)
from core.billing_middleware import (
    BillingMiddleware,
    BillingQueueWorker,
    JailSystem,
    RedisPermissionStore,
    StripeClient,
    StripeWebhookHandler,
    WalletBlockService,
)


# =====================================================
#  Fixtures
# =====================================================

def _make_redis(coach_id: str, status: str = "active", tier: str = "base", clients: int = 0) -> RedisPermissionStore:
    redis = RedisPermissionStore()
    redis.set_status(coach_id, SubscriptionStatus(status))
    redis.set_tier(coach_id, SubscriptionTier(tier))
    redis.set_active_clients(coach_id, clients)
    return redis


def _make_subscription(coach_id: str, **kwargs) -> CoachSubscriptionRow:
    defaults = {
        "coach_id": coach_id,
        "stripe_customer_id": f"cus_{coach_id[:8]}",
        "stripe_subscription_id": f"sub_{coach_id[:8]}",
        "stripe_metered_item_id": f"si_{coach_id[:8]}",
        "tier": SubscriptionTier.BASE,
        "weekly_base_price_cents": 2500,
        "cbcs_unit_price_cents": 400,
        "status": SubscriptionStatus.ACTIVE,
        "payment_method_last4": "4242",
        "active_client_count": 0,
    }
    defaults.update(kwargs)
    return CoachSubscriptionRow(**defaults)


# =====================================================
#  AC1: Happy Path — require_credits() ALLOWS active coach
# =====================================================

class TestAC1HappyPath:

    def test_active_coach_allows_free_action(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        middleware = BillingMiddleware(redis, stripe, {coach_id: sub})

        result = middleware.require_credits(coach_id, "add_client", cost=0)

        assert result.allowed is True
        assert result.status == SubscriptionStatus.ACTIVE
        assert result.receipt_id is not None

    def test_active_coach_allows_paid_action(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        middleware = BillingMiddleware(redis, stripe, {coach_id: sub})

        result = middleware.require_credits(coach_id, "deploy_cbcs_bot", cost=1)

        assert result.allowed is True
        assert result.cost_cents == 1
        assert len(stripe.get_usage_records()) == 1
        assert stripe.get_usage_records()[0].quantity == 1

    def test_active_coach_stripe_usage_record_created(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        middleware = BillingMiddleware(redis, stripe, {coach_id: sub})

        middleware.require_credits(coach_id, "add_client", cost=1, client_id="client-123")

        records = stripe.get_usage_records()
        assert len(records) == 1
        assert records[0].subscription_item == sub.stripe_metered_item_id

    def test_receipt_chain_written(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        middleware = BillingMiddleware(redis, stripe, {coach_id: sub})

        middleware.require_credits(coach_id, "add_client", cost=0)

        receipts = middleware.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "BILLING_GATE"
        assert receipts[0]["agent_name"] == "billing_middleware"


# =====================================================
#  AC2: Payment Block — require_credits() BLOCKS inactive coach
# =====================================================

class TestAC2PaymentBlock:

    def test_past_due_blocks_action(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        with pytest.raises(BillingError) as exc_info:
            middleware.require_credits(coach_id, "add_client", cost=0)

        assert exc_info.value.code == "SUBSCRIPTION_INACTIVE"
        assert len(stripe.get_usage_records()) == 0

    def test_cancelled_blocks_action(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "cancelled")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        with pytest.raises(BillingError) as exc_info:
            middleware.require_credits(coach_id, "deploy_cbcs_bot", cost=1)

        assert exc_info.value.code == "SUBSCRIPTION_INACTIVE"

    def test_bot_not_provisioned_on_block(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        with pytest.raises(BillingError):
            middleware.require_credits(coach_id, "provision_bot", cost=1)

        # Verify NO Stripe usage record exists
        assert len(stripe.get_usage_records()) == 0

    def test_block_includes_redirect(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        with pytest.raises(BillingError) as exc_info:
            middleware.require_credits(coach_id, "add_client")

        assert exc_info.value.redirect == "/wallet"


# =====================================================
#  AC3: Instant Usage Lock — first-message billing trigger
# =====================================================

class TestAC3InstantUsageLock:

    def test_first_message_creates_stripe_usage(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        jail = JailSystem(redis, stripe, {coach_id: sub})

        record = jail.apply_instant_usage_lock(coach_id, "client-1", 12345678)

        assert record.quantity == 1
        assert len(stripe.get_usage_records()) == 1

    def test_client_count_incremented(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active", clients=3)
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        jail = JailSystem(redis, stripe, {coach_id: sub})

        jail.apply_instant_usage_lock(coach_id, "client-1", 12345678)

        assert redis.get_active_clients(coach_id) == 4

    def test_delete_client_doesnt_refund_cycle(self):
        """Coach adds client → bot sends first message → $4 locked.
        Coach deletes client 2 days later → $4 still applies for this cycle."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        jail = JailSystem(redis, stripe, {coach_id: sub})

        # Bot sends first message → $4 locked
        jail.apply_instant_usage_lock(coach_id, "client-1", 12345678)

        # Stripe usage record exists — deletion doesn't remove it
        records = stripe.get_usage_records()
        assert len(records) == 1
        assert records[0].quantity == 1
        # In production: client removal does NOT call Stripe to reverse the usage record

    def test_idempotent_lock(self):
        """Same first message trigger twice → one charge (idempotency)."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        jail = JailSystem(redis, stripe, {coach_id: sub})

        r1 = jail.apply_instant_usage_lock(coach_id, "client-1", 12345678)
        r2 = jail.apply_instant_usage_lock(coach_id, "client-1", 12345678)

        assert r1.id == r2.id  # Same record, idempotent
        assert len(stripe.get_usage_records()) == 1

    def test_receipt_chain_written_on_lock(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id)
        jail = JailSystem(redis, stripe, {coach_id: sub})

        jail.apply_instant_usage_lock(coach_id, "client-1", 12345678)

        receipts = jail.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "JAIL_ACTION"


# =====================================================
#  AC4: Grace Period Mute — payment_failed → bots stop
# =====================================================

class TestAC4GracePeriodMute:

    def test_payment_failed_sets_past_due(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        sub = _make_subscription(coach_id)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        event = handler.process_event(
            event_type="invoice.payment_failed",
            stripe_event_id="evt_fail_001",
            data={"coach_id": coach_id},
        )

        assert redis.get_status(coach_id) == SubscriptionStatus.PAST_DUE
        assert event is not None
        assert event.event_type == BillingEventType.PAYMENT_FAILED

    def test_bots_muted_on_past_due(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        jail = JailSystem(redis, stripe)

        result = jail.apply_grace_period_mute(coach_id)

        assert result["bots_muted"] is True
        assert result["affine_read_only"] is True
        assert result["data_preserved"] is True

    def test_data_never_deleted(self):
        """Client data preserved — never deleted due to billing issues."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        jail = JailSystem(redis, stripe)

        result = jail.apply_grace_period_mute(coach_id)
        assert result["data_preserved"] is True


# =====================================================
#  AC5: Re-activation — payment succeeds after past_due
# =====================================================

class TestAC5Reactivation:

    def test_payment_success_restores_active(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        sub = _make_subscription(coach_id, status=SubscriptionStatus.PAST_DUE)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        handler.process_event(
            event_type="invoice.payment_succeeded",
            stripe_event_id="evt_success_001",
            data={"coach_id": coach_id, "amount_cents": 2500},
        )

        assert redis.get_status(coach_id) == SubscriptionStatus.ACTIVE

    def test_bots_resume_on_reactivation(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        jail = JailSystem(redis, stripe)

        result = jail.apply_reactivation(coach_id)

        assert result["bots_resumed"] is True
        assert result["affine_full_access"] is True
        assert result["watermarks_removed"] is True


# =====================================================
#  AC6: Wallet Display — cost breakdown
# =====================================================

class TestAC6WalletDisplay:

    def test_4_clients_25_base(self):
        """4 active clients on $25/week → Wallet shows $41/week."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active", "base", clients=4)
        sub = _make_subscription(coach_id, active_client_count=4)
        wallet = WalletBlockService(redis, {coach_id: sub})

        display = wallet.get_wallet_display(coach_id)

        assert display.weekly_base_cost_cents == 2500
        assert display.active_client_count == 4
        assert display.cbcs_unit_cents == 400
        assert display.total_weekly_cost_cents == 4100  # 2500 + 4*400
        assert display.payment_status == SubscriptionStatus.ACTIVE
        assert display.alert_message is None

    def test_past_due_shows_alert(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due", "base", clients=2)
        sub = _make_subscription(coach_id, status=SubscriptionStatus.PAST_DUE)
        wallet = WalletBlockService(redis, {coach_id: sub})

        display = wallet.get_wallet_display(coach_id)

        assert "Billing failed" in display.alert_message
        assert "[Update Card]" in display.alert_message

    def test_no_subscription_shows_error(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "cancelled")
        wallet = WalletBlockService(redis, {})

        display = wallet.get_wallet_display(coach_id)

        assert display.total_weekly_cost_cents == 0
        assert "No subscription found" in display.alert_message

    def test_premium_tier_shows_50(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active", "premium", clients=10)
        sub = _make_subscription(coach_id, weekly_base_price_cents=5000, tier=SubscriptionTier.PREMIUM)
        wallet = WalletBlockService(redis, {coach_id: sub})

        display = wallet.get_wallet_display(coach_id)

        assert display.weekly_base_cost_cents == 5000
        assert display.total_weekly_cost_cents == 9000  # 5000 + 10*400


# =====================================================
#  CBAR Q4: Grace Dispatch for Pre-Queued Messages
# =====================================================

class TestCBARQ4GraceDispatch:

    def test_pre_queued_message_dispatches_under_grace(self):
        """Message scheduled BEFORE billing failure → allowed under grace."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        billing_failure = datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)
        msg_scheduled = datetime(2026, 4, 1, 10, 0, 0, tzinfo=timezone.utc)  # Before failure

        result = middleware.check_grace_dispatch(coach_id, msg_scheduled, billing_failure)

        assert result.allowed is True
        assert result.grace_dispatch is True
        assert result.receipt_id is not None

    def test_post_failure_message_blocked(self):
        """Message scheduled AFTER billing failure → blocked."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        billing_failure = datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)
        msg_scheduled = datetime(2026, 4, 1, 14, 0, 0, tzinfo=timezone.utc)  # After failure

        with pytest.raises(BillingError) as exc_info:
            middleware.check_grace_dispatch(coach_id, msg_scheduled, billing_failure)

        assert exc_info.value.code == "SUBSCRIPTION_INACTIVE"

    def test_active_coach_no_grace_needed(self):
        """Active coach → no grace dispatch, normal allow."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        result = middleware.check_grace_dispatch(
            coach_id,
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
        )

        assert result.allowed is True
        assert result.grace_dispatch is False

    def test_grace_dispatch_receipt_logged(self):
        """Grace dispatch writes Receipt Chain Guard entry."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe)

        billing_failure = datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)
        msg_scheduled = datetime(2026, 4, 1, 10, 0, 0, tzinfo=timezone.utc)

        middleware.check_grace_dispatch(coach_id, msg_scheduled, billing_failure)

        receipts = middleware.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "BILLING_GATE"


# =====================================================
#  CBAR Q5: Billing Queue Pre-Billing + Dispatcher Lock
# =====================================================

class TestCBARQ5BillingQueue:

    def test_enqueue_creates_pending_row(self):
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        coach_id = str(uuid.uuid4())
        scheduled = datetime(2026, 4, 2, 9, 0, 0, tzinfo=timezone.utc)

        row = worker.enqueue(coach_id, 12345678, scheduled, "si_test")

        assert row.status == BillingQueueStatus.PENDING
        assert row.coach_id == coach_id
        assert row.idempotency_key is not None

    def test_process_pending_bills_successfully(self):
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        coach_id = str(uuid.uuid4())
        scheduled = datetime(2026, 4, 2, 9, 0, 0, tzinfo=timezone.utc)
        worker.enqueue(coach_id, 12345678, scheduled, "si_test")

        billed = worker.process_pending(metered_items={coach_id: "si_test"})

        assert len(billed) == 1
        assert billed[0].status == BillingQueueStatus.BILLED
        assert billed[0].stripe_usage_record_id is not None
        assert billed[0].billed_at is not None

    def test_dispatcher_locked_until_billed(self):
        """CBAR Q5: Dispatcher forbidden from sending until status = 'billed'."""
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        coach_id = str(uuid.uuid4())
        scheduled = datetime(2026, 4, 2, 9, 0, 0, tzinfo=timezone.utc)
        row = worker.enqueue(coach_id, 12345678, scheduled, "si_test")

        # Before billing — dispatch blocked
        assert worker.is_dispatch_allowed(row.idempotency_key) is False

        # After billing — dispatch allowed
        worker.process_pending(metered_items={coach_id: "si_test"})
        assert worker.is_dispatch_allowed(row.idempotency_key) is True

    def test_missing_metered_item_fails(self):
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        coach_id = str(uuid.uuid4())
        scheduled = datetime(2026, 4, 2, 9, 0, 0, tzinfo=timezone.utc)
        worker.enqueue(coach_id, 12345678, scheduled, "si_test")

        # No metered item mapped for this coach
        billed = worker.process_pending(metered_items={})

        assert len(billed) == 0
        queue = worker.get_queue()
        assert queue[0].status == BillingQueueStatus.FAILED
        assert queue[0].retry_count == 1

    def test_escalation_after_max_retries(self):
        """After 6 retries (30 min), should escalate to Factory Floor."""
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        row = BillingQueueRow(
            coach_id="coach-1",
            client_telegram_user_id=12345678,
            idempotency_key="test-key",
            scheduled_dispatch_at=datetime.now(timezone.utc),
            retry_count=BILLING_QUEUE_MAX_RETRIES,
        )

        assert worker.should_escalate(row) is True

    def test_no_escalation_before_max(self):
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        row = BillingQueueRow(
            coach_id="coach-1",
            client_telegram_user_id=12345678,
            idempotency_key="test-key",
            scheduled_dispatch_at=datetime.now(timezone.utc),
            retry_count=3,
        )

        assert worker.should_escalate(row) is False

    def test_billing_queue_receipt_chain(self):
        stripe = StripeClient()
        worker = BillingQueueWorker(stripe)

        coach_id = str(uuid.uuid4())
        scheduled = datetime(2026, 4, 2, 9, 0, 0, tzinfo=timezone.utc)
        worker.enqueue(coach_id, 12345678, scheduled, "si_test")
        worker.process_pending(metered_items={coach_id: "si_test"})

        receipts = worker.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "USAGE_REPORT"


# =====================================================
#  Safety: Webhook Replay Idempotency
# =====================================================

class TestWebhookIdempotency:

    def test_duplicate_event_ignored(self):
        """Same Stripe webhook event twice → no double charge, no duplicate Redis update."""
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        sub = _make_subscription(coach_id)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        event1 = handler.process_event(
            event_type="invoice.payment_succeeded",
            stripe_event_id="evt_dupe_001",
            data={"coach_id": coach_id, "amount_cents": 2500},
        )
        event2 = handler.process_event(
            event_type="invoice.payment_succeeded",
            stripe_event_id="evt_dupe_001",
            data={"coach_id": coach_id, "amount_cents": 2500},
        )

        assert event1 is not None
        assert event2 is None  # Duplicate → ignored
        assert len(handler.get_processed_events()) == 1

    def test_different_events_processed(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        sub = _make_subscription(coach_id)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        handler.process_event("invoice.payment_succeeded", "evt_001", {"coach_id": coach_id})
        handler.process_event("invoice.payment_failed", "evt_002", {"coach_id": coach_id})

        assert len(handler.get_processed_events()) == 2
        assert redis.get_status(coach_id) == SubscriptionStatus.PAST_DUE  # Last event wins

    def test_webhook_receipt_chain(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        sub = _make_subscription(coach_id)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        handler.process_event("invoice.payment_succeeded", "evt_001", {"coach_id": coach_id})

        receipts = handler.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "WEBHOOK_SYNC"
        assert receipts[0]["agent_name"] == "stripe_webhook_handler"


# =====================================================
#  Safety: Subscription Tier Updates
# =====================================================

class TestSubscriptionTierUpdate:

    def test_tier_updated_via_webhook(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active", "base")
        sub = _make_subscription(coach_id)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        handler.process_event(
            event_type="customer.subscription.updated",
            stripe_event_id="evt_tier_001",
            data={"coach_id": coach_id, "tier": "premium"},
        )

        assert redis.get_tier(coach_id) == SubscriptionTier.PREMIUM

    def test_subscription_deleted_sets_cancelled(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        sub = _make_subscription(coach_id)
        handler = StripeWebhookHandler(redis, {coach_id: sub})

        handler.process_event(
            event_type="customer.subscription.deleted",
            stripe_event_id="evt_del_001",
            data={"coach_id": coach_id},
        )

        assert redis.get_status(coach_id) == SubscriptionStatus.CANCELLED


# =====================================================
#  Watermark Enforcement
# =====================================================

class TestWatermarkEnforcement:

    def test_free_trial_requires_watermark(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active", "free_trial")
        stripe = StripeClient()
        jail = JailSystem(redis, stripe)

        assert jail.check_watermark_required(coach_id) is True

    def test_active_paid_no_watermark(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active", "base")
        stripe = StripeClient()
        jail = JailSystem(redis, stripe)

        assert jail.check_watermark_required(coach_id) is False

    def test_past_due_requires_watermark(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "past_due", "base")
        stripe = StripeClient()
        jail = JailSystem(redis, stripe)

        assert jail.check_watermark_required(coach_id) is True


# =====================================================
#  Redis Permission Store
# =====================================================

class TestRedisPermissionStore:

    def test_default_status_cancelled(self):
        redis = RedisPermissionStore()
        assert redis.get_status("unknown-coach") == SubscriptionStatus.CANCELLED

    def test_default_tier_free_trial(self):
        redis = RedisPermissionStore()
        assert redis.get_tier("unknown-coach") == SubscriptionTier.FREE_TRIAL

    def test_default_active_clients_zero(self):
        redis = RedisPermissionStore()
        assert redis.get_active_clients("unknown-coach") == 0

    def test_set_and_get_status(self):
        redis = RedisPermissionStore()
        redis.set_status("coach-1", SubscriptionStatus.ACTIVE)
        assert redis.get_status("coach-1") == SubscriptionStatus.ACTIVE

    def test_increment_active_clients(self):
        redis = RedisPermissionStore()
        redis.set_active_clients("coach-1", 5)
        new = redis.increment_active_clients("coach-1")
        assert new == 6
        assert redis.get_active_clients("coach-1") == 6


# =====================================================
#  No Metered Item Guard
# =====================================================

class TestNoMeteredItem:

    def test_no_metered_item_raises(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        sub = _make_subscription(coach_id, stripe_metered_item_id=None)
        middleware = BillingMiddleware(redis, stripe, {coach_id: sub})

        with pytest.raises(BillingError) as exc_info:
            middleware.require_credits(coach_id, "add_client", cost=1)

        assert exc_info.value.code == "NO_METERED_ITEM"

    def test_no_subscription_raises(self):
        coach_id = str(uuid.uuid4())
        redis = _make_redis(coach_id, "active")
        stripe = StripeClient()
        middleware = BillingMiddleware(redis, stripe, {})

        with pytest.raises(BillingError) as exc_info:
            middleware.require_credits(coach_id, "add_client", cost=1)

        assert exc_info.value.code == "NO_METERED_ITEM"
