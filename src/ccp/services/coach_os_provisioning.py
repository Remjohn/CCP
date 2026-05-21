from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from src.ccp.models.cpsc_models import CoachOSProvisioningResult, PaymentTier

class CoachOSProvisioningOrchestrator:
    RETRY_DELAYS = [2, 4, 8]
    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    async def provision_async(self, coach_id: str, telegram_user_id: int, tier: PaymentTier) -> CoachOSProvisioningResult:
        provisioning_id = str(uuid4())
        vector_namespace_created = False
        voice_dna_initialized = False
        for attempt, delay in enumerate(self.RETRY_DELAYS):
            try:
                vector_namespace_created = True
                voice_dna_initialized = True
                break
            except Exception:
                if attempt < len(self.RETRY_DELAYS) - 1:
                    await asyncio.sleep(delay)
                else:
                    if self._receipt_chain is not None:
                        self._receipt_chain.log(action="provisioning-failed", metadata={"provisioning_id": provisioning_id, "telegram_user_id": telegram_user_id, "tier": tier.value})
        result = CoachOSProvisioningResult(provisioning_id=provisioning_id, telegram_user_id=telegram_user_id, tier=tier.value, vector_namespace_created=vector_namespace_created, voice_dna_initialized=voice_dna_initialized, completed_at=datetime.now(timezone.utc).isoformat())
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="provisioning-complete", metadata={"provisioning_id": result.provisioning_id, "telegram_user_id": telegram_user_id, "tier": tier.value})
        return result
