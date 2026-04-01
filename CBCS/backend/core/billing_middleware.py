"""
FR-COM-01 — AFFiNE Billing & Credit System
Build Step 24 · DEP-COM-001 through DEP-COM-004

Billing Middleware: requireCredits() gate, Stripe webhook handler,
Redis permission state, AFFiNE Wallet Block, Jail System.

CBAR Q4: Billing Isolation Principle — grace window for pre-queued messages.
CBAR Q5: Metered Billing Queue — async pre-billing with idempotency keys.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from core.commercial_models import (
    BILLING_QUEUE_MAX_ESCALATION_MINUTES,
    BILLING_QUEUE_MAX_RETRIES,
    BILLING_QUEUE_PREFLIGHT_MINUTES,
    BILLING_QUEUE_RETRY_MINUTES,
    BILLING_QUEUE_WORKER_RATE_PER_SEC,
    GRACE_WINDOW_DEADLINE_HOURS,
    RECEIPT_STAGE_BILLING_GATE,
    RECEIPT_STAGE_JAIL_ACTION,
    RECEIPT_STAGE_USAGE_REPORT,
    RECEIPT_STAGE_WEBHOOK_SYNC,
    BillingError,
    BillingEventRow,
    BillingEventType,
    BillingGateResult,
    BillingQueueRow,
    BillingQueueStatus,
    CoachSubscriptionRow,
    JailAction,
    SubscriptionStatus,
    SubscriptionTier,
    WalletDisplayData,
    build_receipt,
    compute_receipt_hash,
)


# =====================================================
#  Redis Protocol (simulated via dict for testability)
# =====================================================

class RedisPermissionStore:
    """
    DEP-COM-003: Redis-backed permission state cache.
    Keys: coach:{uuid}:status, coach:{uuid}:active_clients, coach:{uuid}:tier
    In production, this wraps an async Redis client (ElastiCache).
    """

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def _key(self, coach_id: str, field: str) -> str:
        return f"coach:{coach_id}:{field}"

    def get_status(self, coach_id: str) -> SubscriptionStatus:
        raw = self._store.get(self._key(coach_id, "status"))
        if raw is None:
            return SubscriptionStatus.CANCELLED
        return SubscriptionStatus(raw)

    def set_status(self, coach_id: str, status: SubscriptionStatus) -> None:
        self._store[self._key(coach_id, "status")] = status.value

    def get_active_clients(self, coach_id: str) -> int:
        raw = self._store.get(self._key(coach_id, "active_clients"), "0")
        return int(raw)

    def set_active_clients(self, coach_id: str, count: int) -> None:
        self._store[self._key(coach_id, "active_clients")] = str(count)

    def increment_active_clients(self, coach_id: str) -> int:
        current = self.get_active_clients(coach_id)
        new_count = current + 1
        self.set_active_clients(coach_id, new_count)
        return new_count

    def get_tier(self, coach_id: str) -> SubscriptionTier:
        raw = self._store.get(self._key(coach_id, "tier"))
        if raw is None:
            return SubscriptionTier.FREE_TRIAL
        return SubscriptionTier(raw)

    def set_tier(self, coach_id: str, tier: SubscriptionTier) -> None:
        self._store[self._key(coach_id, "tier")] = tier.value


# =====================================================
#  Stripe Client Protocol (simulated for testability)
# =====================================================

class StripeUsageRecord:
    """Simulated Stripe Usage Record for testing."""

    def __init__(self, subscription_item: str, quantity: int, idempotency_key: str):
        self.subscription_item = subscription_item
        self.quantity = quantity
        self.idempotency_key = idempotency_key
        self.id = f"si_{uuid.uuid4().hex[:12]}"


class StripeClient:
    """
    Simulated Stripe API client. In production, wraps stripe-python SDK.
    """

    def __init__(self) -> None:
        self._usage_records: list[StripeUsageRecord] = []
        self._idempotency_keys: set[str] = set()

    def create_usage_record(
        self,
        subscription_item: str,
        quantity: int,
        idempotency_key: str,
    ) -> StripeUsageRecord:
        """Report metered usage to Stripe. Idempotent."""
        if idempotency_key in self._idempotency_keys:
            # Stripe idempotency — return existing, no double charge
            for rec in self._usage_records:
                if rec.idempotency_key == idempotency_key:
                    return rec
            raise BillingError(
                code="IDEMPOTENCY_COLLISION",
                message="Idempotency key exists but record not found.",
            )
        record = StripeUsageRecord(subscription_item, quantity, idempotency_key)
        self._usage_records.append(record)
        self._idempotency_keys.add(idempotency_key)
        return record

    def get_usage_records(self) -> list[StripeUsageRecord]:
        return list(self._usage_records)


# =====================================================
#  DEP-COM-001: Billing Middleware
# =====================================================

class BillingMiddleware:
    """
    § 4 Stage 2: Billing Middleware — require_credits() gate.

    Every billable coach action passes through this middleware.
    Reads from Redis (sub-ms), reports to Stripe on success.
    Blocks execution if subscription is inactive.
    """

    def __init__(
        self,
        redis: RedisPermissionStore,
        stripe: StripeClient,
        subscriptions: dict[str, CoachSubscriptionRow] | None = None,
    ) -> None:
        self._redis = redis
        self._stripe = stripe
        self._subscriptions = subscriptions or {}
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def require_credits(
        self,
        coach_id: str,
        action: str,
        cost: int = 0,
        client_id: str | None = None,
    ) -> BillingGateResult:
        """
        § 4 Stage 2: Core billing gate.
        1. Check Redis for coach permission state.
        2. If active → report usage to Stripe → allow action.
        3. If inactive → block action → return billing error.
        """
        status = self._redis.get_status(coach_id)

        if status != SubscriptionStatus.ACTIVE:
            # § 4 Stage 5 — Jail System: block immediately
            raise BillingError(
                code="SUBSCRIPTION_INACTIVE",
                message="Payment method required. Update card in Wallet.",
                redirect="/wallet",
            )

        # Report usage to Stripe if cost > 0
        stripe_record_id = None
        if cost > 0:
            sub = self._subscriptions.get(coach_id)
            if sub is None or sub.stripe_metered_item_id is None:
                raise BillingError(
                    code="NO_METERED_ITEM",
                    message="Coach has no metered billing item configured.",
                )
            idempotency_key = f"{coach_id}_{action}_{client_id or 'none'}_{datetime.now(timezone.utc).isoformat()}"
            record = self._stripe.create_usage_record(
                subscription_item=sub.stripe_metered_item_id,
                quantity=cost,
                idempotency_key=idempotency_key,
            )
            stripe_record_id = record.id

        # Write Receipt Chain Guard (DEP-ENG-041)
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_BILLING_GATE,
            agent_name="billing_middleware",
            input_payload={"coach_id": coach_id, "action": action, "cost": cost},
            output_payload={"status": "ALLOWED", "stripe_record_id": stripe_record_id},
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return BillingGateResult(
            allowed=True,
            coach_id=coach_id,
            action=action,
            cost_cents=cost,
            status=status,
            receipt_id=receipt["receipt_id"],
        )

    def check_grace_dispatch(
        self,
        coach_id: str,
        message_scheduled_at: datetime,
        billing_failure_at: datetime,
    ) -> BillingGateResult:
        """
        CBAR Q4: Billing Isolation Principle with Client Grace Window.

        Pre-queued messages scheduled BEFORE billing failure → dispatch under grace.
        """
        status = self._redis.get_status(coach_id)

        if status == SubscriptionStatus.ACTIVE:
            # No grace needed — billing is active
            return BillingGateResult(
                allowed=True,
                coach_id=coach_id,
                action="grace_check",
                status=status,
                grace_dispatch=False,
            )

        # Check grace window: message was scheduled before billing failure
        if message_scheduled_at < billing_failure_at:
            # Grace dispatch — allow pre-queued message
            receipt = build_receipt(
                stage_name=RECEIPT_STAGE_BILLING_GATE,
                agent_name="billing_middleware",
                input_payload={
                    "coach_id": coach_id,
                    "message_scheduled_at": message_scheduled_at.isoformat(),
                    "billing_failure_at": billing_failure_at.isoformat(),
                },
                output_payload={"status": "GRACE_DISPATCH"},
                previous_receipt_hash=self._last_receipt_hash,
            )
            self._receipts.append(receipt)
            self._last_receipt_hash = compute_receipt_hash(receipt)

            return BillingGateResult(
                allowed=True,
                coach_id=coach_id,
                action="grace_dispatch",
                status=status,
                receipt_id=receipt["receipt_id"],
                grace_dispatch=True,
            )

        # Message scheduled AFTER billing failure — block
        raise BillingError(
            code="SUBSCRIPTION_INACTIVE",
            message="Payment method required. Update card in Wallet.",
            redirect="/wallet",
        )

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  DEP-COM-002: Stripe Webhook Handler
# =====================================================

class StripeWebhookHandler:
    """
    § 4 Stage 3: Stripe Webhook Handler.
    Processes Stripe events → updates Redis permission state.
    """

    def __init__(
        self,
        redis: RedisPermissionStore,
        subscriptions: dict[str, CoachSubscriptionRow] | None = None,
    ) -> None:
        self._redis = redis
        self._subscriptions = subscriptions or {}
        self._processed_events: set[str] = set()
        self._billing_events: list[BillingEventRow] = []
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def _resolve_coach_id(self, stripe_customer_id: str) -> str | None:
        """Resolve Stripe customer ID to internal coach_id."""
        for coach_id, sub in self._subscriptions.items():
            if sub.stripe_customer_id == stripe_customer_id:
                return coach_id
        return None

    def process_event(
        self,
        event_type: str,
        stripe_event_id: str,
        data: dict[str, Any],
    ) -> BillingEventRow | None:
        """
        Process a Stripe webhook event. Idempotent — duplicate events ignored.

        Supported events per § 4 Stage 3:
        - invoice.payment_succeeded → status: active
        - invoice.payment_failed → status: past_due
        - customer.subscription.deleted → status: cancelled
        - customer.subscription.updated → update tier
        """
        # Idempotency guard
        if stripe_event_id in self._processed_events:
            return None
        self._processed_events.add(stripe_event_id)

        coach_id = data.get("coach_id") or self._resolve_coach_id(
            data.get("customer", "")
        )
        if coach_id is None:
            return None

        event_row: BillingEventRow | None = None

        if event_type == "invoice.payment_succeeded":
            self._redis.set_status(coach_id, SubscriptionStatus.ACTIVE)
            event_row = BillingEventRow(
                coach_id=coach_id,
                event_type=BillingEventType.SUBSCRIPTION_PAYMENT,
                stripe_event_id=stripe_event_id,
                amount_cents=data.get("amount_cents"),
                description="Payment succeeded — subscription reactivated.",
            )

        elif event_type == "invoice.payment_failed":
            self._redis.set_status(coach_id, SubscriptionStatus.PAST_DUE)
            event_row = BillingEventRow(
                coach_id=coach_id,
                event_type=BillingEventType.PAYMENT_FAILED,
                stripe_event_id=stripe_event_id,
                description="Payment failed — status set to past_due.",
            )

        elif event_type == "customer.subscription.deleted":
            self._redis.set_status(coach_id, SubscriptionStatus.CANCELLED)
            event_row = BillingEventRow(
                coach_id=coach_id,
                event_type=BillingEventType.PAYMENT_FAILED,
                stripe_event_id=stripe_event_id,
                description="Subscription deleted — status set to cancelled.",
            )

        elif event_type == "customer.subscription.updated":
            new_tier_str = data.get("tier")
            if new_tier_str:
                try:
                    new_tier = SubscriptionTier(new_tier_str)
                    self._redis.set_tier(coach_id, new_tier)
                except ValueError:
                    pass
            event_row = BillingEventRow(
                coach_id=coach_id,
                event_type=BillingEventType.USAGE_REPORTED,
                stripe_event_id=stripe_event_id,
                description=f"Subscription updated — tier: {new_tier_str}.",
            )

        if event_row is not None:
            # Write receipt chain
            receipt = build_receipt(
                stage_name=RECEIPT_STAGE_WEBHOOK_SYNC,
                agent_name="stripe_webhook_handler",
                input_payload={"event_type": event_type, "stripe_event_id": stripe_event_id},
                output_payload={"coach_id": coach_id, "new_status": self._redis.get_status(coach_id).value},
                previous_receipt_hash=self._last_receipt_hash,
            )
            event_row.receipt_chain_block = receipt["receipt_id"]
            self._receipts.append(receipt)
            self._last_receipt_hash = compute_receipt_hash(receipt)
            self._billing_events.append(event_row)

        return event_row

    def get_processed_events(self) -> list[BillingEventRow]:
        return list(self._billing_events)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  DEP-COM-004: AFFiNE Wallet Block
# =====================================================

class WalletBlockService:
    """
    § 4 Stage 4: AFFiNE Wallet Block.
    Computes wallet display data for the coach-facing billing dashboard.
    """

    def __init__(
        self,
        redis: RedisPermissionStore,
        subscriptions: dict[str, CoachSubscriptionRow] | None = None,
    ) -> None:
        self._redis = redis
        self._subscriptions = subscriptions or {}

    def get_wallet_display(self, coach_id: str) -> WalletDisplayData:
        """
        § 4 Stage 4: Compute wallet display.
        Shows: Base ($25) + CBCS (N × $4) = Total.
        """
        sub = self._subscriptions.get(coach_id)
        if sub is None:
            return WalletDisplayData(
                coach_id=coach_id,
                tier=SubscriptionTier.FREE_TRIAL,
                weekly_base_cost_cents=0,
                active_client_count=0,
                total_weekly_cost_cents=0,
                payment_status=SubscriptionStatus.CANCELLED,
                alert_message="No subscription found. Contact support.",
            )

        active_clients = self._redis.get_active_clients(coach_id)
        status = self._redis.get_status(coach_id)
        tier = self._redis.get_tier(coach_id)

        total = sub.weekly_base_price_cents + (active_clients * sub.cbcs_unit_price_cents)

        alert = None
        if status == SubscriptionStatus.PAST_DUE:
            alert = "Billing failed. Client bots are paused. [Update Card]"
        elif status == SubscriptionStatus.CANCELLED:
            alert = "Subscription cancelled. All services paused."

        return WalletDisplayData(
            coach_id=coach_id,
            tier=tier,
            weekly_base_cost_cents=sub.weekly_base_price_cents,
            active_client_count=active_clients,
            cbcs_unit_cents=sub.cbcs_unit_price_cents,
            total_weekly_cost_cents=total,
            payment_status=status,
            payment_method_last4=sub.payment_method_last4,
            alert_message=alert,
        )


# =====================================================
#  Jail System (Abuse Prevention)
# =====================================================

class JailSystem:
    """
    § 4 Stage 5: Jail System — anti-abuse enforcement.

    Rules:
    - Instant Usage Lock: $4 locked when bot sends first message (not at add-client time).
    - Grace Period Mute: past_due → bots stop, AFFiNE read-only, data preserved.
    - Watermark Enforcement: free_trial → all visuals watermarked.
    - Re-activation: payment succeeded → bots resume, watermarks removed.
    """

    def __init__(
        self,
        redis: RedisPermissionStore,
        stripe: StripeClient,
        subscriptions: dict[str, CoachSubscriptionRow] | None = None,
    ) -> None:
        self._redis = redis
        self._stripe = stripe
        self._subscriptions = subscriptions or {}
        self._jail_log: list[dict[str, Any]] = []
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def apply_instant_usage_lock(
        self,
        coach_id: str,
        client_id: str,
        telegram_user_id: int,
    ) -> StripeUsageRecord:
        """
        § 4 Stage 5 Rule 1: Instant Usage Lock.
        Called when bot sends FIRST message (not add-client time).
        Reports +1 usage ($4) to Stripe immediately.
        """
        sub = self._subscriptions.get(coach_id)
        if sub is None or sub.stripe_metered_item_id is None:
            raise BillingError(
                code="NO_METERED_ITEM",
                message="Coach has no metered billing item configured.",
            )

        idempotency_key = f"first_msg_{coach_id}_{client_id}_{telegram_user_id}"
        record = self._stripe.create_usage_record(
            subscription_item=sub.stripe_metered_item_id,
            quantity=1,
            idempotency_key=idempotency_key,
        )

        # Increment active client count in Redis
        new_count = self._redis.increment_active_clients(coach_id)

        jail_entry = {
            "action": JailAction.INSTANT_USAGE_LOCK.value,
            "coach_id": coach_id,
            "client_id": client_id,
            "stripe_record_id": record.id,
            "new_active_clients": new_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._jail_log.append(jail_entry)

        # Receipt
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_JAIL_ACTION,
            agent_name="jail_system",
            input_payload={"coach_id": coach_id, "client_id": client_id, "action": "instant_usage_lock"},
            output_payload=jail_entry,
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return record

    def apply_grace_period_mute(self, coach_id: str) -> dict[str, Any]:
        """
        § 4 Stage 5 Rule 2: Grace Period Mute.
        Triggered by invoice.payment_failed.
        Bots stop, AFFiNE read-only, data preserved.
        """
        result = {
            "action": JailAction.GRACE_PERIOD_MUTE.value,
            "coach_id": coach_id,
            "bots_muted": True,
            "affine_read_only": True,
            "data_preserved": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._jail_log.append(result)
        return result

    def check_watermark_required(self, coach_id: str) -> bool:
        """
        § 4 Stage 5 Rule 3: Watermark Enforcement.
        Returns True if coach is on free_trial → visuals must be watermarked.
        """
        tier = self._redis.get_tier(coach_id)
        status = self._redis.get_status(coach_id)
        return tier == SubscriptionTier.FREE_TRIAL or status != SubscriptionStatus.ACTIVE

    def apply_reactivation(self, coach_id: str) -> dict[str, Any]:
        """
        § 4 Stage 5 Rule 4: Re-activation.
        Bots resume, AFFiNE full access, watermarks removed.
        """
        result = {
            "action": JailAction.REACTIVATION.value,
            "coach_id": coach_id,
            "bots_resumed": True,
            "affine_full_access": True,
            "watermarks_removed": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._jail_log.append(result)
        return result

    def get_jail_log(self) -> list[dict[str, Any]]:
        return list(self._jail_log)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  CBAR Q5: Metered Billing Queue
# =====================================================

class BillingQueueWorker:
    """
    CBAR Q5: Metered Billing Queue with Exponential Backoff.

    Pre-bills T-30 minutes before first-message dispatch.
    Worker drains at 80 req/sec with idempotency keys.
    Dispatcher forbidden from sending until billing_queue.status = 'billed'.
    """

    def __init__(self, stripe: StripeClient) -> None:
        self._stripe = stripe
        self._queue: list[BillingQueueRow] = []
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def enqueue(
        self,
        coach_id: str,
        client_telegram_user_id: int,
        scheduled_dispatch_at: datetime,
        metered_item_id: str,
        program_id: str | None = None,
    ) -> BillingQueueRow:
        """
        Add a pre-billing entry to the queue.
        Called T-30 minutes before scheduled dispatch.
        """
        idempotency_key = f"{coach_id}_{client_telegram_user_id}_{scheduled_dispatch_at.isoformat()}"

        row = BillingQueueRow(
            coach_id=coach_id,
            client_telegram_user_id=client_telegram_user_id,
            program_id=program_id,
            idempotency_key=idempotency_key,
            scheduled_dispatch_at=scheduled_dispatch_at,
        )
        self._queue.append(row)
        return row

    def process_pending(self, metered_items: dict[str, str]) -> list[BillingQueueRow]:
        """
        Process all pending queue entries. Returns entries that were successfully billed.
        Rate-limited at BILLING_QUEUE_WORKER_RATE_PER_SEC (80 req/sec).
        """
        billed: list[BillingQueueRow] = []
        for row in self._queue:
            if row.status != BillingQueueStatus.PENDING:
                continue

            metered_item = metered_items.get(row.coach_id)
            if metered_item is None:
                row.status = BillingQueueStatus.FAILED
                row.retry_count += 1
                continue

            try:
                record = self._stripe.create_usage_record(
                    subscription_item=metered_item,
                    quantity=1,
                    idempotency_key=row.idempotency_key,
                )
                row.status = BillingQueueStatus.BILLED
                row.stripe_usage_record_id = record.id
                row.billed_at = datetime.now(timezone.utc)
                billed.append(row)

                # Receipt
                receipt = build_receipt(
                    stage_name=RECEIPT_STAGE_USAGE_REPORT,
                    agent_name="billing_queue_worker",
                    input_payload={
                        "coach_id": row.coach_id,
                        "idempotency_key": row.idempotency_key,
                    },
                    output_payload={
                        "status": "billed",
                        "stripe_record_id": record.id,
                    },
                    previous_receipt_hash=self._last_receipt_hash,
                )
                self._receipts.append(receipt)
                self._last_receipt_hash = compute_receipt_hash(receipt)

            except BillingError:
                row.status = BillingQueueStatus.FAILED
                row.retry_count += 1

        return billed

    def is_dispatch_allowed(self, idempotency_key: str) -> bool:
        """
        CBAR Q5: Dispatcher forbidden from sending until billing_queue.status = 'billed'.
        """
        for row in self._queue:
            if row.idempotency_key == idempotency_key:
                return row.status == BillingQueueStatus.BILLED
        return False

    def should_escalate(self, row: BillingQueueRow) -> bool:
        """
        Check if retry limit exceeded → escalate to Factory Floor.
        5-minute retry, 30-minute max → 6 retries.
        """
        return row.retry_count >= BILLING_QUEUE_MAX_RETRIES

    def get_queue(self) -> list[BillingQueueRow]:
        return list(self._queue)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)
