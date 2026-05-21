"""
Integration tests for FR58 Offer Tier Architecture.
"""

import pytest

from src.ccp.models.cpsc_models import OfferTierError, UpwardRoutingVerdict
from src.ccp.services.offer_tier_governor import OfferTierGovernor
from src.ccp.core.receipt_chain import ReceiptChain

class MemoryReceiptChain(ReceiptChain):
    def __init__(self):
        self.logs = []
    def log(self, agent_id, action, output_summary, parent_receipt_id=None, metadata=None):
        class Receipt:
            receipt_id = f"test-receipt-{len(self.logs)}"
            
        r = Receipt()
        self.logs.append({
            "id": r.receipt_id,
            "action": action,
            "summary": output_summary
        })
        return r


class TestUUIDBroadcastFilter:
    """Test UUID Broadcast filtering (FR59 simulation) against target Tier 3 campaign."""
    
    def test_tier_3_launch_filters_correctly(self):
        rc = MemoryReceiptChain()
        gov = OfferTierGovernor("coach-integration", rc)
        
        users = [
            {"id": "u1", "coping": 1, "history": []},  # TIER_0 -> Exclude
            {"id": "u2", "coping": 3, "history": [0]}, # TIER_1 -> Exclude
            {"id": "u3", "coping": 4, "history": [1]}, # TIER_2 -> Exclude
            {"id": "u4", "coping": 5, "history": [2]}, # TIER_3 -> Include
            {"id": "u5", "coping": 5, "history": [3]}, # TIER_3 -> Include
        ]
        
        approved_uuids = []
        for u in users:
            try:
                row = gov.evaluate(
                    client_id=u["id"],
                    coping_position=u["coping"],
                    target_campaign_tier=4, # Target Tier 4 Launch (Operator)
                    historical_purchased_tiers=u["history"]
                )
                if row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value:
                    approved_uuids.append(row.client_id)
            except ValueError as e:
                if e.args[0] == OfferTierError.FAIL_CAPACITY_EXCEEDED:
                    pass
                else:
                    raise
                    
        assert approved_uuids == ["u4", "u5"]
        assert any("verdict=FAIL_CAPACITY_EXCEEDED" in log["summary"] for log in rc.logs)


class TestCorruptedStripeLedgerArray:
    """Safety tests: Ensure gateway algorithm cascades gracefully."""
    
    def test_corrupted_history_does_not_crash(self):
        rc = MemoryReceiptChain()
        gov = OfferTierGovernor("coach-safety", rc)
        
        # Corrupt list but high enough coping position to allow Tier 2
        row = gov.evaluate(
            client_id="client-safe",
            coping_position=4,
            target_campaign_tier=2,
            historical_purchased_tiers=[None, float("nan"), -1, "invalid"]
        )
        
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value
        assert row.computed_coping_position == 4
