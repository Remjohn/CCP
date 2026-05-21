from __future__ import annotations

from typing import Any

from src.ccp.models.cpsc_models import (
    EligibilityCheckResult,
    EligibilityVerdict,
    LOYALTY_ASSET_THRESHOLD,
    PaymentTier,
    StoredValueSnapshot,
)


class StoredValueResolver:
    """Queries asset_registry for cumulative_assets_stored count,
    checks Voice DNA status for voice_dna_trained, and counts
    archive/reaction DB entries to populate content_archive_count
    and reaction_count."""

    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    async def resolve(self, telegram_user_id: int) -> StoredValueSnapshot:
        """Resolve the stored value snapshot for a given user.
        Falls back to zero-value snapshot if asset_registry query fails."""
        try:
            cumulative_assets_stored = 0
            voice_dna_trained = False
            content_archive_count = 0
            reaction_count = 0

            if self._supabase is not None:
                # Query asset_registry for cumulative_assets_stored
                asset_result = self._supabase.table("asset_registry").select("id").eq(
                    "telegram_user_id", telegram_user_id
                ).execute()
                if asset_result and hasattr(asset_result, "data"):
                    cumulative_assets_stored = len(asset_result.data)

                # Check Voice DNA training status
                vdna_result = self._supabase.table("voice_dna_profiles").select("trained").eq(
                    "telegram_user_id", telegram_user_id
                ).execute()
                if vdna_result and hasattr(vdna_result, "data") and vdna_result.data:
                    voice_dna_trained = bool(vdna_result.data[0].get("trained", False))

                # Count content archive entries
                archive_result = self._supabase.table("content_archive").select("id").eq(
                    "telegram_user_id", telegram_user_id
                ).execute()
                if archive_result and hasattr(archive_result, "data"):
                    content_archive_count = len(archive_result.data)

                # Count reaction entries
                reaction_result = self._supabase.table("reactions").select("id").eq(
                    "telegram_user_id", telegram_user_id
                ).execute()
                if reaction_result and hasattr(reaction_result, "data"):
                    reaction_count = len(reaction_result.data)

            return StoredValueSnapshot(
                cumulative_assets_stored=cumulative_assets_stored,
                voice_dna_trained=voice_dna_trained,
                content_archive_count=content_archive_count,
                reaction_count=reaction_count,
            )
        except Exception:
            # Fallback: stored-value-fallback — return zero-value snapshot
            return StoredValueSnapshot(
                cumulative_assets_stored=0,
                voice_dna_trained=False,
                content_archive_count=0,
                reaction_count=0,
            )


class EligibilityGate:
    """Combines OfferTierGovernor.evaluate() output with StoredValueResolver
    output to produce EligibilityCheckResult. Resolves PROVISIONAL_PENDING_PAYMENT
    if an incomplete payment is active."""

    def __init__(
        self,
        offer_tier_governor: Any = None,
        supabase_client: Any = None,
    ) -> None:
        self._governor = offer_tier_governor
        self._supabase = supabase_client

    async def evaluate(
        self,
        telegram_user_id: int,
        coach_id: str,
        target_tier: PaymentTier,
        stored_value: StoredValueSnapshot,
    ) -> tuple[str, str]:
        """Returns (verdict, offer_copy_variant) tuple.
        Checks: already-subscribed, in-flight payment, tier ceiling, loyalty threshold."""

        current_stripe_status = "free"

        # Check for existing active subscription (AC-3.5)
        if self._supabase is not None:
            sub_result = self._supabase.table("tier_subscriptions").select("*").eq(
                "telegram_user_id", telegram_user_id
            ).eq("tier", target_tier.value).eq("status", "active").execute()
            if sub_result and hasattr(sub_result, "data") and sub_result.data:
                return EligibilityVerdict.FAIL_ALREADY_SUBSCRIBED.value, "standard"
            # Resolve current stripe status
            any_sub = self._supabase.table("tier_subscriptions").select("*").eq(
                "telegram_user_id", telegram_user_id
            ).eq("status", "active").execute()
            if any_sub and hasattr(any_sub, "data") and any_sub.data:
                current_stripe_status = "active"

        # Check for in-flight payment (AC-3.7)
        if self._supabase is not None:
            pending_result = self._supabase.table("payment_transactions").select("*").eq(
                "telegram_user_id", telegram_user_id
            ).eq("tier", target_tier.value).in_(
                "status", ["INVOICE_SENT", "PRE_CHECKOUT_CONFIRMED", "REQUIRES_ACTION"]
            ).execute()
            if pending_result and hasattr(pending_result, "data") and pending_result.data:
                return EligibilityVerdict.PROVISIONAL_PENDING_PAYMENT.value, "standard"

        # Check tier ceiling via OfferTierGovernor
        if self._governor is not None:
            try:
                target_campaign_tier = 1 if target_tier == PaymentTier.SPEAKING_LEARNING else 2
                self._governor.evaluate(
                    client_id=str(telegram_user_id),
                    coping_position=None,
                    target_campaign_tier=target_campaign_tier,
                )
            except ValueError as e:
                if "FAIL_CAPACITY_EXCEEDED" in str(e):
                    return EligibilityVerdict.FAIL_TIER_EXCEEDED.value, "standard"
                raise

        # Determine loyalty unlock vs standard (AC-3.1 / M06)
        if (
            stored_value.cumulative_assets_stored >= LOYALTY_ASSET_THRESHOLD
            and current_stripe_status == "free"
        ):
            return EligibilityVerdict.PASS_LOYALTY_UNLOCK.value, "loyalty_unlock"

        return EligibilityVerdict.PASS_STANDARD.value, "standard"


class PaymentEligibilityService:
    """Orchestrator class that wires StoredValueResolver + EligibilityGate
    into a single check_eligibility call. Includes Loyalty Unlock logic
    and receipt chain logging."""

    def __init__(
        self,
        supabase_client: Any = None,
        receipt_chain: Any = None,
        offer_tier_governor: Any = None,
        lead_capture_service: Any = None,
    ) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._stored_value_resolver = StoredValueResolver(supabase_client=supabase_client)
        self._eligibility_gate = EligibilityGate(
            offer_tier_governor=offer_tier_governor,
            supabase_client=supabase_client,
        )
        self._lead_capture_service = lead_capture_service

    async def check_eligibility(
        self,
        *,
        telegram_user_id: int,
        coach_id: str,
        target_tier: PaymentTier,
    ) -> EligibilityCheckResult:
        """Primary entrypoint: check eligibility combining stripe_status
        + cumulative_assets_stored. Enforces Phase1-M06 Stored Value Rule."""
        from datetime import datetime, timezone
        from uuid import uuid4

        # Check commercial cooldown via lead_capture_service
        if self._lead_capture_service is not None:
            try:
                cooldown = self._lead_capture_service.check_cooldown(telegram_user_id)
                if cooldown and getattr(cooldown, "is_active", False):
                    stored_value = StoredValueSnapshot(
                        cumulative_assets_stored=0,
                        voice_dna_trained=False,
                        content_archive_count=0,
                        reaction_count=0,
                    )
                    result = EligibilityCheckResult(
                        eligibility_id=str(uuid4()),
                        telegram_user_id=telegram_user_id,
                        coach_id=coach_id,
                        target_tier=target_tier.value,
                        current_stripe_status="free",
                        stored_value=stored_value,
                        verdict=EligibilityVerdict.FAIL_COOLDOWN_ACTIVE.value,
                        offer_copy_variant="standard",
                        evaluated_at=datetime.now(timezone.utc).isoformat(),
                    )
                    if self._receipt_chain is not None:
                        self._receipt_chain.log(action="eligibility-check", metadata={
                            "eligibility_id": result.eligibility_id,
                            "verdict": result.verdict,
                        })
                    return result
            except Exception:
                pass

        # Resolve stored value
        stored_value = await self._stored_value_resolver.resolve(telegram_user_id)

        # Evaluate eligibility gate
        verdict, offer_copy_variant = await self._eligibility_gate.evaluate(
            telegram_user_id=telegram_user_id,
            coach_id=coach_id,
            target_tier=target_tier,
            stored_value=stored_value,
        )

        # Determine current stripe status
        current_stripe_status = "free"
        if self._supabase is not None:
            any_sub = self._supabase.table("tier_subscriptions").select("*").eq(
                "telegram_user_id", telegram_user_id
            ).eq("status", "active").execute()
            if any_sub and hasattr(any_sub, "data") and any_sub.data:
                current_stripe_status = "active"

        result = EligibilityCheckResult(
            eligibility_id=str(uuid4()),
            telegram_user_id=telegram_user_id,
            coach_id=coach_id,
            target_tier=target_tier.value,
            current_stripe_status=current_stripe_status,
            stored_value=stored_value,
            verdict=verdict,
            offer_copy_variant=offer_copy_variant,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

        # Receipt chain logging
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="eligibility-check", metadata={
                "eligibility_id": result.eligibility_id,
                "verdict": result.verdict,
                "offer_copy_variant": result.offer_copy_variant,
                "cumulative_assets_stored": stored_value.cumulative_assets_stored,
            })

        return result
