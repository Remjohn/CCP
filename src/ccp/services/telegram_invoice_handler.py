from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from src.ccp.models.cpsc_models import (
    EligibilityCheckResult,
    EligibilityVerdict,
    InvoicePayload,
    PaymentTier,
    TIER_PRICE_MAP,
)

TIER_DISPLAY_NAMES: dict[str, str] = {
    "SPEAKING_LEARNING": "Speaking & Learning",
    "COACH_OS": "Coach OS",
}

TIER_DESCRIPTIONS: dict[str, str] = {
    "SPEAKING_LEARNING": "Monthly access to Speaking & Learning tools, biometric score tracking, and community features.",
    "COACH_OS": "Full Coach OS suite with Voice DNA, advanced analytics, content studio, and premium support.",
}

LOYALTY_DESCRIPTIONS: dict[str, str] = {
    "SPEAKING_LEARNING": "You've invested deeply in your growth. Unlock Speaking & Learning and keep your momentum.",
    "COACH_OS": "You've built {assets} assets and trained your Voice DNA. Your Coach OS is ready.",
}


class InvoiceBuilder:
    """Constructs Telegram Bot API sendInvoice JSON payloads.
    No external URLs — native Telegram payment buttons only."""

    def __init__(self, provider_token: str = "") -> None:
        self._provider_token = provider_token

    def build(
        self,
        chat_id: int,
        eligibility: EligibilityCheckResult,
    ) -> InvoicePayload:
        """Build a sendInvoice payload for the given tier and eligibility result."""
        tier = eligibility.target_tier
        amount_cents = TIER_PRICE_MAP.get(tier, 3999)
        display_name = TIER_DISPLAY_NAMES.get(tier, tier)

        # Select description based on offer copy variant (M06 compliance)
        if eligibility.offer_copy_variant == "loyalty_unlock":
            description = LOYALTY_DESCRIPTIONS.get(tier, "").format(
                assets=eligibility.stored_value.cumulative_assets_stored
            )
        else:
            description = TIER_DESCRIPTIONS.get(tier, "")

        return InvoicePayload(
            invoice_id=str(uuid4()),
            chat_id=chat_id,
            title=display_name,
            description=description,
            payload=f"ccp_payment:{eligibility.eligibility_id}:{tier}",
            provider_token=self._provider_token,
            currency="USD",
            prices=[{"label": display_name, "amount": amount_cents}],
            tier=tier,
            sent_at=datetime.now(timezone.utc).isoformat(),
        )


class SCAFrictionMitigator:
    """Sends high-status identity-affirming Telegram message during
    3D Secure / SCA flows so the user doesn't feel abandoned during
    bank verification. No raw Stripe error codes exposed."""

    SCA_REASSURANCE_MESSAGES: dict[str, str] = {
        "SPEAKING_LEARNING": "Your Speaking & Learning credentials are being verified by the banking network. This confirms your access to advanced biometric insights.",
        "COACH_OS": "Your Coach OS credentials are being verified by the banking network. This confirms your elite access.",
    }

    def __init__(self, bot_token: str = "") -> None:
        self._bot_token = bot_token

    async def send_reassurance(self, chat_id: int, tier: str = "COACH_OS") -> None:
        """Send a reassuring message during SCA challenge.
        Uses high-status language, never raw error codes."""
        message = self.SCA_REASSURANCE_MESSAGES.get(tier, self.SCA_REASSURANCE_MESSAGES["COACH_OS"])

        if self._bot_token:
            import httpx
            url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
            async with httpx.AsyncClient() as client:
                await client.post(url, json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                })


class TelegramInvoiceHandler:
    """Orchestrator that generates native Telegram sendInvoice payloads
    and sends them via the Telegram Bot API. No external URLs.
    Enforces EXP-FRC-003 B=MAP Friction Audit — 1-tap checkout."""

    def __init__(
        self,
        provider_token: str = "",
        bot_token: str = "",
        receipt_chain: Any = None,
    ) -> None:
        self._invoice_builder = InvoiceBuilder(provider_token=provider_token)
        self._sca_mitigator = SCAFrictionMitigator(bot_token=bot_token)
        self._bot_token = bot_token
        self._receipt_chain = receipt_chain

    async def generate_and_send(
        self,
        *,
        chat_id: int,
        eligibility: EligibilityCheckResult,
    ) -> InvoicePayload:
        """Generate and send a native Telegram invoice. Returns the InvoicePayload.
        Only sends for PASS_STANDARD or PASS_LOYALTY_UNLOCK verdicts."""

        if eligibility.verdict not in (
            EligibilityVerdict.PASS_STANDARD.value,
            EligibilityVerdict.PASS_LOYALTY_UNLOCK.value,
        ):
            raise ValueError(f"Cannot generate invoice for verdict: {eligibility.verdict}")

        payload = self._invoice_builder.build(chat_id=chat_id, eligibility=eligibility)

        # Send via Telegram Bot API sendInvoice
        if self._bot_token:
            import httpx
            url = f"https://api.telegram.org/bot{self._bot_token}/sendInvoice"
            invoice_data = {
                "chat_id": payload.chat_id,
                "title": payload.title,
                "description": payload.description,
                "payload": payload.payload,
                "provider_token": payload.provider_token,
                "currency": payload.currency,
                "prices": payload.prices,
            }
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=invoice_data)
                    response.raise_for_status()
            except Exception:
                # Graceful degradation — Telegram sendInvoice API failure
                if self._receipt_chain is not None:
                    self._receipt_chain.log(action="invoice-send-failed", metadata={
                        "invoice_id": payload.invoice_id,
                        "chat_id": chat_id,
                    })
                raise

        # Receipt chain logging
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="invoice-sent", metadata={
                "invoice_id": payload.invoice_id,
                "chat_id": chat_id,
                "tier": payload.tier,
                "eligibility_id": eligibility.eligibility_id,
            })

        return payload
