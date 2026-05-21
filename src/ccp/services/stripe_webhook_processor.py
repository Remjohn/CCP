from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from src.ccp.models.cpsc_models import PaymentStatus, PaymentTier
from src.ccp.services.payment_reward_dispatcher import PaymentRewardDispatcher
from src.ccp.services.coach_os_provisioning import CoachOSProvisioningOrchestrator

class SubscriptionReconciliationHandler:
    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    async def handle_subscription_deleted(self, stripe_subscription_id: str) -> None:
        if self._supabase is not None:
            self._supabase.table("tier_subscriptions").update({"status": "canceled"}).eq("stripe_subscription_id", stripe_subscription_id).execute()
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="subscription-reconciliation", metadata={"stripe_subscription_id": stripe_subscription_id, "new_status": "canceled"})

    async def handle_payment_failed(self, stripe_subscription_id: str) -> None:
        if self._supabase is not None:
            self._supabase.table("tier_subscriptions").update({"status": "past_due"}).eq("stripe_subscription_id", stripe_subscription_id).execute()
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="subscription-reconciliation", metadata={"stripe_subscription_id": stripe_subscription_id, "new_status": "past_due"})

class StripeWebhookProcessor:
    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None, bot_token: str = "") -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._reward_dispatcher = PaymentRewardDispatcher(bot_token=bot_token, receipt_chain=receipt_chain)
        self._provisioning = CoachOSProvisioningOrchestrator(supabase_client=supabase_client, receipt_chain=receipt_chain)
        self._reconciliation = SubscriptionReconciliationHandler(supabase_client=supabase_client, receipt_chain=receipt_chain)

    async def process(self, event_type: str, event_data: dict) -> None:
        if event_type == "invoice.payment_succeeded":
            await self._handle_payment_succeeded(event_data)
        elif event_type == "customer.subscription.deleted":
            stripe_sub_id = event_data.get("id", "")
            await self._reconciliation.handle_subscription_deleted(stripe_sub_id)
        elif event_type == "invoice.payment_failed":
            stripe_sub_id = event_data.get("subscription", "")
            await self._reconciliation.handle_payment_failed(stripe_sub_id)

    async def _handle_payment_succeeded(self, event_data: dict) -> None:
        charge_id = event_data.get("charge", "")
        metadata = event_data.get("metadata", {})
        transaction_id = metadata.get("transaction_id", "")
        chat_id = int(metadata.get("chat_id", 0))
        coach_id = metadata.get("coach_id", "")
        telegram_user_id = int(metadata.get("telegram_user_id", 0))
        tier_str = metadata.get("tier", "SPEAKING_LEARNING")
        tier = PaymentTier(tier_str) if tier_str in PaymentTier.__members__ else PaymentTier.SPEAKING_LEARNING

        # 1. Update payment_transactions to PAYMENT_SUCCESSFUL
        if self._supabase is not None and transaction_id:
            self._supabase.table("payment_transactions").update({"status": PaymentStatus.PAYMENT_SUCCESSFUL.value, "stripe_charge_id": charge_id, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("transaction_id", transaction_id).execute()

        # 2. Create/update tier_subscriptions
        if self._supabase is not None:
            stripe_sub_id = event_data.get("subscription", "")
            self._supabase.table("tier_subscriptions").upsert({"subscription_id": str(uuid4()), "telegram_user_id": telegram_user_id, "coach_id": coach_id, "tier": tier.value, "stripe_subscription_id": stripe_sub_id, "status": "active", "started_at": datetime.now(timezone.utc).isoformat()}).execute()

        # 3. Immediately dispatch reward (M07 — before provisioning)
        reward_result = await self._reward_dispatcher.push_reward(chat_id=chat_id, tier=tier)

        # 4. Mark reward dispatched in DB
        if self._supabase is not None and transaction_id:
            self._supabase.table("payment_transactions").update({"reward_dispatched": True, "status": PaymentStatus.REWARD_DISPATCHED.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("transaction_id", transaction_id).execute()

        # 5. Launch background provisioning via asyncio.create_task
        asyncio.create_task(self._background_provision(coach_id, telegram_user_id, tier, transaction_id))

        # 6. Receipt chain
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="payment-fulfillment", metadata={"transaction_id": transaction_id, "tier": tier.value, "reward_dispatch_id": reward_result.dispatch_id})

    async def _background_provision(self, coach_id: str, telegram_user_id: int, tier: PaymentTier, transaction_id: str) -> None:
        result = await self._provisioning.provision_async(coach_id=coach_id, telegram_user_id=telegram_user_id, tier=tier)
        if self._supabase is not None and transaction_id:
            self._supabase.table("payment_transactions").update({"provisioning_complete": True, "status": PaymentStatus.PROVISIONING_COMPLETE.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("transaction_id", transaction_id).execute()
