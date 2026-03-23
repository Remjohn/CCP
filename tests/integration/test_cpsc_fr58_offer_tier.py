"""
FR58 — Offer Tier Architecture: Integration Tests
==================================================
Covers:
- TierCeilingResolver (coping→ceiling mapping, null/boundary cases)
- _safe_tier_history_max (corrupt history sanitisation)
- UpwardOnlyRoutingGate (all three verdicts)
- OfferTierGovernor.evaluate (happy-path, provisional, hard-fail, receipt chain)
- Acceptance Criteria AC1-AC3 (verbatim from spec)
- coach_id guard (ADR-01)
"""

from __future__ import annotations

import math
import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    OfferTierCeiling,
    OfferTierError,
    OfferTierGovernorRow,
    UpwardRoutingVerdict,
)
from src.ccp.services.offer_tier_governor import (
    OfferTierGovernor,
    TierCeilingResolver,
    UpwardOnlyRoutingGate,
    _safe_tier_history_max,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="TST", log_dir=tmp_path)


@pytest.fixture()
def governor(rc):
    return OfferTierGovernor(coach_id="coachA", receipt_chain=rc)


# ---------------------------------------------------------------------------
# TierCeilingResolver — coping-to-ceiling mapping
# ---------------------------------------------------------------------------

class TestTierCeilingResolver:

    @pytest.mark.parametrize("coping,expected_ceiling", [
        (1, OfferTierCeiling.TIER_1_CHALLENGE),
        (2, OfferTierCeiling.TIER_1_CHALLENGE),
        (3, OfferTierCeiling.TIER_1_CHALLENGE),
        (4, OfferTierCeiling.TIER_2_CORE),
        (5, OfferTierCeiling.TIER_3_PREMIUM),
    ])
    def test_tier_matrix_from_spec(self, coping, expected_ceiling):
        """§10 unit test table: coping=[1,3,4,5] → [TIER_1,TIER_1,TIER_2,TIER_3]."""
        cp, ceiling = TierCeilingResolver(coping).resolve()
        assert ceiling == expected_ceiling
        assert cp == coping

    def test_null_coping_maps_to_tier1(self):
        """Null coping → TIER_1_CHALLENGE baseline (§6 backward compat)."""
        cp, ceiling = TierCeilingResolver(None).resolve()
        assert ceiling == OfferTierCeiling.TIER_1_CHALLENGE
        assert cp == 1  # COPING_NULL_FALLBACK

    def test_coping_above_5_clamps_to_tier3(self):
        """coping > 5 → TIER_3_PREMIUM (graceful ceiling)."""
        _, ceiling = TierCeilingResolver(9).resolve()
        assert ceiling == OfferTierCeiling.TIER_3_PREMIUM

    def test_coping_zero_maps_to_tier1(self):
        """coping=0 ≤ 3 → TIER_1_CHALLENGE."""
        _, ceiling = TierCeilingResolver(0).resolve()
        assert ceiling == OfferTierCeiling.TIER_1_CHALLENGE


# ---------------------------------------------------------------------------
# _safe_tier_history_max — corrupt history sanitisation
# ---------------------------------------------------------------------------

class TestSafeTierHistoryMax:

    def test_normal_list(self):
        assert _safe_tier_history_max([1, 2, 3]) == 3

    def test_single_value(self):
        assert _safe_tier_history_max([2]) == 2

    def test_empty_list(self):
        assert _safe_tier_history_max([]) == 0

    def test_none_list(self):
        assert _safe_tier_history_max(None) == 0

    def test_all_none_values(self):
        assert _safe_tier_history_max([None, None]) == 0

    def test_nan_values(self):
        assert _safe_tier_history_max([math.nan, math.nan]) == 0

    def test_negative_values(self):
        """Negative tier values are invalid → excluded → fallback 0."""
        assert _safe_tier_history_max([-1, -2]) == 0

    def test_mixed_corrupt_and_valid(self):
        """Mix of None, NaN, -1, and valid → max of valid ones."""
        assert _safe_tier_history_max([None, math.nan, -1, 2, 3]) == 3

    def test_float_valid_tier(self):
        """Floats like 2.0 should be treated as 2."""
        assert _safe_tier_history_max([1.0, 2.0, 3.0]) == 3

    def test_string_corrupt_value(self):
        """Non-numeric strings are silently excluded."""
        assert _safe_tier_history_max(["bad", 2]) == 2


# ---------------------------------------------------------------------------
# UpwardOnlyRoutingGate — all three verdicts
# ---------------------------------------------------------------------------

class TestUpwardOnlyRoutingGate:

    def test_pass_authorized_no_history(self):
        """target=1, ceiling=TIER_2, history=[] → PASS."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=1,
            ceiling=OfferTierCeiling.TIER_2_CORE,
            historical_tiers=[],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.PASS_AUTHORIZED

    def test_pass_authorized_target_equals_ceiling(self):
        """target=3, ceiling=TIER_3 → PASS (target ≤ ceiling, ≥ history)."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=3,
            ceiling=OfferTierCeiling.TIER_3_PREMIUM,
            historical_tiers=[1, 2],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.PASS_AUTHORIZED

    def test_pass_authorized_target_equals_history_max(self):
        """target == history_max and target ≤ ceiling → PASS."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=2,
            ceiling=OfferTierCeiling.TIER_3_PREMIUM,
            historical_tiers=[2],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.PASS_AUTHORIZED

    def test_fail_capacity_exceeded_basic(self):
        """target=2, ceiling=TIER_1 → FAIL_CAPACITY_EXCEEDED."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=2,
            ceiling=OfferTierCeiling.TIER_1_CHALLENGE,
            historical_tiers=[],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.FAIL_CAPACITY_EXCEEDED

    def test_fail_capacity_exceeded_target_above_tier3(self):
        """target=3, ceiling=TIER_2 → FAIL_CAPACITY_EXCEEDED."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=3,
            ceiling=OfferTierCeiling.TIER_2_CORE,
            historical_tiers=[],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.FAIL_CAPACITY_EXCEEDED

    def test_provisional_downsell_basic(self):
        """target=1, history=[3], ceiling=TIER_3 → PROVISIONAL_DOWNSELL."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=1,
            ceiling=OfferTierCeiling.TIER_3_PREMIUM,
            historical_tiers=[3],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT

    def test_provisional_downsell_from_2_to_1(self):
        """target=1, history=[2], ceiling=TIER_3 → PROVISIONAL_DOWNSELL."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=1,
            ceiling=OfferTierCeiling.TIER_3_PREMIUM,
            historical_tiers=[2],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT

    def test_provisional_downsell_corrupt_history_ignored(self):
        """History [None,-1,3]: max valid=3; target=1 → PROVISIONAL_DOWNSELL."""
        verdict = UpwardOnlyRoutingGate(
            target_tier=1,
            ceiling=OfferTierCeiling.TIER_3_PREMIUM,
            historical_tiers=[None, -1, 3],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT

    def test_fail_takes_precedence_over_downsell(self):
        """
        target=3 > ceiling_int=1 even though history is high.
        FAIL_CAPACITY_EXCEEDED checked first.
        """
        verdict = UpwardOnlyRoutingGate(
            target_tier=3,
            ceiling=OfferTierCeiling.TIER_1_CHALLENGE,
            historical_tiers=[3],
        ).evaluate()
        assert verdict == UpwardRoutingVerdict.FAIL_CAPACITY_EXCEEDED


# ---------------------------------------------------------------------------
# Acceptance Criteria (verbatim from spec §8)
# ---------------------------------------------------------------------------

class TestAcceptanceCriteria:

    def test_ac1_coping2_target_tier3_fail(self, governor):
        """AC1: coping=2 + target=3 → FAIL_CAPACITY_EXCEEDED."""
        with pytest.raises(ValueError) as exc_info:
            governor.evaluate(
                client_id="client-ac1",
                coping_position=2,
                target_campaign_tier=3,
                historical_purchased_tiers=[],
            )
        assert OfferTierError.FAIL_CAPACITY_EXCEEDED in str(exc_info.value)

    def test_ac2_tier3_history_target_tier1_provisional(self, governor):
        """AC2: client has Tier 3 history + target Tier 1 → PROVISIONAL_DOWNSELL."""
        row = governor.evaluate(
            client_id="client-ac2",
            coping_position=5,
            target_campaign_tier=1,
            historical_purchased_tiers=[3],
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT.value

    def test_ac3_coping4_ceiling_tier2(self, governor):
        """AC3: coping=4 → eligible_tier_ceiling='TIER_2_CORE'."""
        row = governor.evaluate(
            client_id="client-ac3",
            coping_position=4,
            target_campaign_tier=2,
            historical_purchased_tiers=[],
        )
        assert row.eligible_tier_ceiling == OfferTierCeiling.TIER_2_CORE.value


# ---------------------------------------------------------------------------
# OfferTierGovernor — row structure & receipt chain
# ---------------------------------------------------------------------------

class TestOfferTierGovernorRow:

    def test_pass_row_fields(self, governor):
        row = governor.evaluate(
            client_id="cli-01",
            coping_position=3,
            target_campaign_tier=1,
            historical_purchased_tiers=[],
        )
        assert isinstance(row, OfferTierGovernorRow)
        assert row.client_id == "cli-01"
        assert row.coach_id == "coachA"
        assert row.computed_coping_position == 3
        assert row.eligible_tier_ceiling == OfferTierCeiling.TIER_1_CHALLENGE.value
        assert row.target_campaign_tier == 1
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value
        assert row.governor_evaluation_id  # non-empty UUID
        assert row.timestamp  # non-empty ISO string

    def test_provisional_row_fields(self, governor):
        row = governor.evaluate(
            client_id="cli-02",
            coping_position=5,
            target_campaign_tier=2,
            historical_purchased_tiers=[3],
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT.value
        assert row.eligible_tier_ceiling == OfferTierCeiling.TIER_3_PREMIUM.value

    def test_governor_evaluation_id_is_uuid(self, governor):
        import uuid
        row = governor.evaluate(
            client_id="cli-uuid",
            coping_position=4,
            target_campaign_tier=2,
        )
        # Should not raise
        uuid.UUID(row.governor_evaluation_id)

    def test_timestamp_is_iso_format(self, governor):
        from datetime import datetime
        row = governor.evaluate(
            client_id="cli-ts",
            coping_position=5,
            target_campaign_tier=3,
        )
        dt = datetime.fromisoformat(row.timestamp)
        assert dt.tzinfo is not None  # timezone-aware

    def test_null_coping_produces_tier1_ceiling(self, governor):
        row = governor.evaluate(
            client_id="cli-null",
            coping_position=None,
            target_campaign_tier=1,
        )
        assert row.eligible_tier_ceiling == OfferTierCeiling.TIER_1_CHALLENGE.value
        assert row.computed_coping_position == 1

    def test_no_history_argument_defaults_to_empty(self, governor):
        """historical_purchased_tiers defaults to None → treated as []."""
        row = governor.evaluate(
            client_id="cli-nohist",
            coping_position=4,
            target_campaign_tier=2,
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value


# ---------------------------------------------------------------------------
# OfferTierGovernor — receipt chain entries
# ---------------------------------------------------------------------------

class TestOfferTierGovernorReceipts:

    def test_pass_logs_two_receipts(self, rc, governor):
        governor.evaluate(
            client_id="cli-rc1",
            coping_position=3,
            target_campaign_tier=1,
        )
        ceiling_entries = rc.query(action="tier-ceiling-resolve")
        gate_entries = rc.query(action="offer-routing-gate")
        assert len(ceiling_entries) >= 1
        assert len(gate_entries) >= 1

    def test_fail_logs_two_receipts_before_raising(self, rc, governor):
        with pytest.raises(ValueError):
            governor.evaluate(
                client_id="cli-rc2",
                coping_position=1,
                target_campaign_tier=3,
            )
        ceiling_entries = rc.query(action="tier-ceiling-resolve")
        gate_entries = rc.query(action="offer-routing-gate")
        assert len(ceiling_entries) >= 1
        assert len(gate_entries) >= 1
        # Confirm gate receipt mentions FAIL
        assert any("FAIL_CAPACITY_EXCEEDED" in e.output_summary for e in gate_entries)

    def test_provisional_logs_two_receipts(self, rc, governor):
        governor.evaluate(
            client_id="cli-rc3",
            coping_position=5,
            target_campaign_tier=1,
            historical_purchased_tiers=[3],
        )
        assert len(rc.query(action="tier-ceiling-resolve")) >= 1
        assert len(rc.query(action="offer-routing-gate")) >= 1

    def test_receipt_contains_coach_id(self, rc, governor):
        governor.evaluate(
            client_id="cli-rc4",
            coping_position=4,
            target_campaign_tier=2,
        )
        entries = rc.query(action="tier-ceiling-resolve")
        assert any("coachA" in e.output_summary for e in entries)

    def test_gate_receipt_has_parent_id(self, rc, governor):
        governor.evaluate(
            client_id="cli-rc5",
            coping_position=4,
            target_campaign_tier=2,
        )
        gate_entries = rc.query(action="offer-routing-gate")
        assert all(e.parent_receipt_id is not None for e in gate_entries)


# ---------------------------------------------------------------------------
# OfferTierGovernor — FAIL_CAPACITY_EXCEEDED hard-abort behaviour
# ---------------------------------------------------------------------------

class TestHardAbortBehaviour:

    def test_raises_value_error(self, governor):
        with pytest.raises(ValueError):
            governor.evaluate(
                client_id="cli-abort1",
                coping_position=2,
                target_campaign_tier=2,
            )

    def test_error_contains_fail_capacity_exceeded(self, governor):
        with pytest.raises(ValueError) as exc_info:
            governor.evaluate(
                client_id="cli-abort2",
                coping_position=3,
                target_campaign_tier=2,
            )
        assert "FAIL_CAPACITY_EXCEEDED" in str(exc_info.value)

    def test_tier1_ceiling_blocks_tier2(self, governor):
        with pytest.raises(ValueError):
            governor.evaluate(
                client_id="cli-abort3",
                coping_position=1,
                target_campaign_tier=2,
            )

    def test_tier1_ceiling_blocks_tier3(self, governor):
        with pytest.raises(ValueError):
            governor.evaluate(
                client_id="cli-abort4",
                coping_position=2,
                target_campaign_tier=3,
            )

    def test_tier2_ceiling_blocks_tier3(self, governor):
        with pytest.raises(ValueError):
            governor.evaluate(
                client_id="cli-abort5",
                coping_position=4,
                target_campaign_tier=3,
            )

    def test_tier3_ceiling_does_not_block_tier3(self, governor):
        """coping=5 → TIER_3; target=3 → should PASS (no abort)."""
        row = governor.evaluate(
            client_id="cli-pass3",
            coping_position=5,
            target_campaign_tier=3,
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value


# ---------------------------------------------------------------------------
# OfferTierGovernor — ADR-01 coach_id guard
# ---------------------------------------------------------------------------

class TestCoachIdGuard:

    def test_short_coach_id_raises(self, rc):
        with pytest.raises(ValueError):
            OfferTierGovernor(coach_id="X", receipt_chain=rc)

    def test_empty_coach_id_raises(self, rc):
        with pytest.raises(ValueError):
            OfferTierGovernor(coach_id="", receipt_chain=rc)

    def test_valid_min_coach_id(self, rc):
        gov = OfferTierGovernor(coach_id="AB", receipt_chain=rc)
        assert gov is not None


# ---------------------------------------------------------------------------
# OfferTierGovernor — multiple evaluations (receipt accumulation)
# ---------------------------------------------------------------------------

class TestMultipleEvaluations:

    def test_each_evaluation_unique_id(self, governor):
        ids = set()
        for i in range(5):
            row = governor.evaluate(
                client_id=f"cli-{i}",
                coping_position=4,
                target_campaign_tier=2,
            )
            ids.add(row.governor_evaluation_id)
        assert len(ids) == 5

    def test_receipts_accumulate(self, rc, governor):
        for i in range(3):
            governor.evaluate(
                client_id=f"cli-{i}",
                coping_position=3,
                target_campaign_tier=1,
            )
        entries = rc.query(action="tier-ceiling-resolve")
        assert len(entries) == 3

    def test_multi_client_different_ceilings(self, governor):
        r1 = governor.evaluate(
            client_id="c1", coping_position=2, target_campaign_tier=1
        )
        r2 = governor.evaluate(
            client_id="c2", coping_position=4, target_campaign_tier=2
        )
        r3 = governor.evaluate(
            client_id="c3", coping_position=5, target_campaign_tier=3
        )
        assert r1.eligible_tier_ceiling == "TIER_1_CHALLENGE"
        assert r2.eligible_tier_ceiling == "TIER_2_CORE"
        assert r3.eligible_tier_ceiling == "TIER_3_PREMIUM"


# ---------------------------------------------------------------------------
# Spec §10 unit test matrix
# ---------------------------------------------------------------------------

class TestSpecUnitTestMatrix:
    """
    §10 example: coping=[1,3,4,5] → ceiling=[TIER_1,TIER_1,TIER_2,TIER_3]
    """

    @pytest.mark.parametrize("coping,expected", [
        (1, "TIER_1_CHALLENGE"),
        (3, "TIER_1_CHALLENGE"),
        (4, "TIER_2_CORE"),
        (5, "TIER_3_PREMIUM"),
    ])
    def test_matrix_row(self, governor, coping, expected):
        row = governor.evaluate(
            client_id=f"matrix-{coping}",
            coping_position=coping,
            target_campaign_tier=1,  # always valid (never exceeds ceiling)
        )
        assert row.eligible_tier_ceiling == expected


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_all_corrupt_history_treated_as_no_history(self, governor):
        """
        If all history values are corrupt (None, -1, NaN), max_hist=0,
        so any target ≤ ceiling → PASS.
        """
        row = governor.evaluate(
            client_id="cli-corrupt",
            coping_position=5,
            target_campaign_tier=2,
            historical_purchased_tiers=[None, -1],
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value

    def test_target_equals_ceiling_and_history_max(self, governor):
        """
        target == ceiling_int == history_max → PASS (not a downsell).
        """
        row = governor.evaluate(
            client_id="cli-edge1",
            coping_position=5,
            target_campaign_tier=3,
            historical_purchased_tiers=[3],
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value

    def test_null_history_list_same_as_empty(self, governor):
        row = governor.evaluate(
            client_id="cli-null-hist",
            coping_position=4,
            target_campaign_tier=2,
            historical_purchased_tiers=None,
        )
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value

    def test_large_coping_clamps_to_tier3(self, governor):
        row = governor.evaluate(
            client_id="cli-large-cp",
            coping_position=100,
            target_campaign_tier=3,
        )
        assert row.eligible_tier_ceiling == "TIER_3_PREMIUM"
        assert row.gate_verdict == UpwardRoutingVerdict.PASS_AUTHORIZED.value
