"""
Unit tests for FR58 Offer Tier Architecture (5-Layer Model).
"""

import pytest

from src.ccp.models.cpsc_models import OfferTierCeiling, UpwardRoutingVerdict, OfferTierError
from src.ccp.services.offer_tier_governor import (
    TierCeilingResolver,
    UpwardOnlyRoutingGate,
    OfferTierGovernor,
    _safe_tier_history_max,
)


class MockReceiptChain:
    def log(self, **kwargs):
        class Receipt:
            receipt_id = "test-receipt-id"
        return Receipt()


class MockEngagementFeedback:
    def __init__(self, metrics):
        self.metrics = metrics

    def get_svi_metrics(self, client_id):
        if self.metrics is None:
            raise Exception("Service unavailable")
        return self.metrics


class TestCeilingMapper:
    """Test resolution of Coping Position into the 5-Layer Model."""
    
    def test_coping_null_fallback_tier_a(self):
        cp, ceiling = TierCeilingResolver(None).resolve()
        assert cp == 0
        assert ceiling == OfferTierCeiling.TIER_A_PROOF
        
    def test_coping_1_tier_a(self):
        cp, ceiling = TierCeilingResolver(1).resolve()
        assert cp == 1
        assert ceiling == OfferTierCeiling.TIER_A_PROOF

    def test_coping_2_without_bridge_tier_a(self):
        cp, ceiling = TierCeilingResolver(2, []).resolve()
        assert cp == 2
        assert ceiling == OfferTierCeiling.TIER_A_PROOF

    def test_coping_2_with_bridge_tier_b(self):
        cp, ceiling = TierCeilingResolver(2, [1]).resolve()
        assert cp == 2
        assert ceiling == OfferTierCeiling.TIER_B_FIRST_PROOF_UNLOCK
        
    def test_coping_3_tier_c(self):
        cp, ceiling = TierCeilingResolver(3).resolve()
        assert cp == 3
        assert ceiling == OfferTierCeiling.TIER_C_SPEAKING_LEARNING
        
    def test_coping_4_tier_d(self):
        cp, ceiling = TierCeilingResolver(4).resolve()
        assert cp == 4
        assert ceiling == OfferTierCeiling.TIER_D_COACH_OS
        
    def test_coping_5_tier_e(self):
        cp, ceiling = TierCeilingResolver(5).resolve()
        assert cp == 5
        assert ceiling == OfferTierCeiling.TIER_E_OPERATOR


class TestDiscountDownSellGate:
    """Test Upward-Only routing rules preventing brand devaluation in 5-layer model."""
    
    def test_safe_tier_history_max_ignores_corrupt(self):
        assert _safe_tier_history_max(None) == 0
        assert _safe_tier_history_max([None, float("nan"), -1, "invalid"]) == 0
        assert _safe_tier_history_max([0, 1, 3, "2"]) == 3
        
    def test_provisional_downsell_attempt(self):
        # Ceiling is Tier E (Operator=4), Target is Tier C (Speaking/Learning=2), History Max is Tier D (Coach OS=3)
        gate = UpwardOnlyRoutingGate(
            target_tier=2,
            ceiling=OfferTierCeiling.TIER_E_OPERATOR,
            historical_tiers=[3]
        )
        assert gate.evaluate() == UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT
        
    def test_fail_capacity_exceeded(self):
        # Target Tier E (Operator=4) but Ceiling is Tier C (Speaking/Learning=2)
        gate = UpwardOnlyRoutingGate(
            target_tier=4,
            ceiling=OfferTierCeiling.TIER_C_SPEAKING_LEARNING,
            historical_tiers=[0]
        )
        assert gate.evaluate() == UpwardRoutingVerdict.FAIL_CAPACITY_EXCEEDED
        
    def test_pass_authorized(self):
        # Target Tier D (Coach OS=3), Ceiling is Tier D (Coach OS=3), History Max is Tier C (Speaking/Learning=2)
        gate = UpwardOnlyRoutingGate(
            target_tier=3,
            ceiling=OfferTierCeiling.TIER_D_COACH_OS,
            historical_tiers=[2]
        )
        assert gate.evaluate() == UpwardRoutingVerdict.PASS_AUTHORIZED


class TestLoyaltyUnlockThreshold:
    """Test Phase1-M06 The Stored Value Rule implementation for 5-layer model."""
    
    def test_svi_meets_threshold_unlocks_tier_c(self):
        engagement = MockEngagementFeedback({"streak_days": 35, "peer_helpfulness_score": 0.90})
        gov = OfferTierGovernor("coach-123", MockReceiptChain(), engagement)
        
        # User is Coping 2 -> TIER_A_PROOF, but meets SVI threshold unlocking TIER_C (tier integer 2)
        row = gov.evaluate(
            client_id="client-456",
            coping_position=2,
            target_campaign_tier=2,  # Target Tier C Speaking & Learning campaign
            historical_purchased_tiers=[]
        )
        assert row.eligible_tier_ceiling == OfferTierCeiling.TIER_C_SPEAKING_LEARNING.value
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value
        
    def test_svi_below_threshold_retains_tier_a(self):
        engagement = MockEngagementFeedback({"streak_days": 10, "peer_helpfulness_score": 0.90})
        gov = OfferTierGovernor("coach-123", MockReceiptChain(), engagement)
        
        with pytest.raises(ValueError) as exc:
            gov.evaluate(
                client_id="client-456",
                coping_position=2,
                target_campaign_tier=2,
                historical_purchased_tiers=[]
            )
        assert exc.value.args[0] == OfferTierError.FAIL_CAPACITY_EXCEEDED
        
    def test_service_unavailable_fails_closed(self):
        engagement = MockEngagementFeedback(None)
        gov = OfferTierGovernor("coach-123", MockReceiptChain(), engagement)
        
        with pytest.raises(ValueError):
            gov.evaluate(
                client_id="client-456",
                coping_position=2,
                target_campaign_tier=2,
                historical_purchased_tiers=[]
            )
