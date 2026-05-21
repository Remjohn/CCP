from __future__ import annotations
from typing import Any
from src.ccp.models.cpsc_models import EligibilityCheckResult, InvoicePayload, PaymentTier
from src.ccp.services.payment_eligibility_service import PaymentEligibilityService
from src.ccp.services.telegram_invoice_handler import TelegramInvoiceHandler

class PaymentFlowOrchestrator:
    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None, offer_tier_governor: Any = None, lead_capture_service: Any = None, provider_token: str = "", bot_token: str = "") -> None:
        self._eligibility_service = PaymentEligibilityService(supabase_client=supabase_client, receipt_chain=receipt_chain, offer_tier_governor=offer_tier_governor, lead_capture_service=lead_capture_service)
        self._invoice_handler = TelegramInvoiceHandler(provider_token=provider_token, bot_token=bot_token, receipt_chain=receipt_chain)

    async def initiate_upgrade(self, *, telegram_user_id: int, chat_id: int, coach_id: str, target_tier: PaymentTier) -> tuple[EligibilityCheckResult, InvoicePayload | None]:
        eligibility = await self._eligibility_service.check_eligibility(telegram_user_id=telegram_user_id, coach_id=coach_id, target_tier=target_tier)
        if eligibility.verdict in ("PASS_STANDARD", "PASS_LOYALTY_UNLOCK"):
            invoice = await self._invoice_handler.generate_and_send(chat_id=chat_id, eligibility=eligibility)
            return eligibility, invoice
        return eligibility, None
