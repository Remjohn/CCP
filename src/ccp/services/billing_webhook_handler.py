from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from src.ccp.models.billing_models import BillingStatus, REDIS_KEY_STATUS, REDIS_KEY_TIER


class BillingWebhookHandler:
    """Handles Stripe webhook events and syncs state to Redis + PostgreSQL.
    Processes: invoice.payment_succeeded, invoice.payment_failed,
    customer.subscription.deleted, customer.subscription.updated.
    Enforces Phase 1 M-07 Payment Masking Rule on payment_succeeded."""

    def __init__(self, redis_client: Any = None, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._redis = redis_client
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    async def handle_event(self, event_type: str, event_data: dict, stripe_event_id: str = "") -> None:
        if event_type == "invoice.payment_succeeded":
            await self._handle_payment_succeeded(event_data, stripe_event_id)
        elif event_type == "invoice.payment_failed":
            await self._handle_payment_failed(event_data, stripe_event_id)
        elif event_type == "customer.subscription.deleted":
            await self._handle_subscription_deleted(event_data, stripe_event_id)
        elif event_type == "customer.subscription.updated":
            await self._handle_subscription_updated(event_data, stripe_event_id)

    async def _handle_payment_succeeded(self, event_data: dict, stripe_event_id: str) -> None:
        coach_id = event_data.get("metadata", {}).get("coach_id", "")
        # 1. SET coach:{uuid}:status active
        if self._redis is not None and coach_id:
            await self._redis.set(REDIS_KEY_STATUS.format(coach_id=coach_id), BillingStatus.ACTIVE.value)
        # 2. INSERT INTO billing_events
        if self._supabase is not None and coach_id:
            self._supabase.table("billing_events").insert({"id": str(uuid4()), "coach_id": coach_id, "event_type": "subscription_payment", "stripe_event_id": stripe_event_id, "amount_cents": event_data.get("amount_paid", 0), "description": "Subscription payment succeeded", "created_at": datetime.now(timezone.utc).isoformat()}).execute()
            # Update subscription status
            self._supabase.table("coach_subscriptions").update({"status": BillingStatus.ACTIVE.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("coach_id", coach_id).execute()
        # 3. Receipt chain
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="billing-webhook-success", metadata={"coach_id": coach_id, "stripe_event_id": stripe_event_id})

    async def _handle_payment_failed(self, event_data: dict, stripe_event_id: str) -> None:
        coach_id = event_data.get("metadata", {}).get("coach_id", "")
        # 1. SET coach:{uuid}:status past_due
        if self._redis is not None and coach_id:
            await self._redis.set(REDIS_KEY_STATUS.format(coach_id=coach_id), BillingStatus.PAST_DUE.value)
        # 2. INSERT INTO billing_events
        if self._supabase is not None and coach_id:
            self._supabase.table("billing_events").insert({"id": str(uuid4()), "coach_id": coach_id, "event_type": "payment_failed", "stripe_event_id": stripe_event_id, "description": "Payment failed", "created_at": datetime.now(timezone.utc).isoformat()}).execute()
            self._supabase.table("coach_subscriptions").update({"status": BillingStatus.PAST_DUE.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("coach_id", coach_id).execute()
        # 3. Receipt chain
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="billing-webhook-failed", metadata={"coach_id": coach_id, "stripe_event_id": stripe_event_id})

    async def _handle_subscription_deleted(self, event_data: dict, stripe_event_id: str) -> None:
        coach_id = event_data.get("metadata", {}).get("coach_id", "")
        # 1. SET coach:{uuid}:status cancelled
        if self._redis is not None and coach_id:
            await self._redis.set(REDIS_KEY_STATUS.format(coach_id=coach_id), BillingStatus.CANCELLED.value)
        # 2. Update DB
        if self._supabase is not None and coach_id:
            self._supabase.table("coach_subscriptions").update({"status": BillingStatus.CANCELLED.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("coach_id", coach_id).execute()
        # 3. Receipt chain
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="billing-webhook-cancelled", metadata={"coach_id": coach_id, "stripe_event_id": stripe_event_id})

    async def _handle_subscription_updated(self, event_data: dict, stripe_event_id: str) -> None:
        coach_id = event_data.get("metadata", {}).get("coach_id", "")
        new_tier = event_data.get("metadata", {}).get("tier", "")
        # Update tier in Redis
        if self._redis is not None and coach_id and new_tier:
            await self._redis.set(REDIS_KEY_TIER.format(coach_id=coach_id), new_tier)
        # Update DB
        if self._supabase is not None and coach_id and new_tier:
            self._supabase.table("coach_subscriptions").update({"tier": new_tier, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("coach_id", coach_id).execute()
