from src.ccp.models.onboarding_models import LeadMagnetOfferProjection
from src.ccp.services.benchmark_reveal_guard import BenchmarkRevealGuard

class PostRevealOfferProjector:
    async def project(self, session) -> LeadMagnetOfferProjection:
        BenchmarkRevealGuard.assert_reveal_completed(session)
        # Would call OfferTierGovernor.evaluate
        return LeadMagnetOfferProjection(
            session_id=session.session_id,
            client_id_for_governor=session.session_id,
            offer_tier_ceiling="tier_1",
            target_campaign_tier=1,
            gate_verdict="authorized",
            offer_title="Free Benchmark Package",
            offer_summary="Unlock 4 free assets.",
            decision=None
        )
