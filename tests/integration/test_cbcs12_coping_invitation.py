"""
Integration tests — FR-CBCS-12: Coping-Diagnostic Invitation Engine
=====================================================================
Tests cover:
  - CommercialMatrixRouter (tier mapping)
  - CommercialMatrixGate (price ceiling enforcement)
  - ADR-01 constructor enforcement
  - C-11 persona masking
  - Schema validation
  - Acceptance Criteria AC1, AC2, AC3
"""

from __future__ import annotations

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    INVITATION_TIER_CEILINGS,
    INVITATION_TIER_MAP,
    CommercialRoutingVerdict,
    CommercialRoutingVerdictRow,
    CopingInvitationError,
    InvitationTier,
)
from src.ccp.services.coping_invitation_engine import (
    CommercialMatrixGate,
    CommercialMatrixRouter,
)

COACH_ID = "TST"
CLIENT_ID = "CLIENT-001"


# ── Fixtures ───────────────────────────────────────────────────────────


@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "receipts"))


@pytest.fixture()
def router():
    return CommercialMatrixRouter(coach_id=COACH_ID)


@pytest.fixture()
def gate(rc):
    return CommercialMatrixGate(coach_id=COACH_ID, receipt_chain=rc)


# ═══════════════════════════════════════════════════════════════════════
# TestConstants — model-level constants
# ═══════════════════════════════════════════════════════════════════════


class TestConstants:
    def test_tier_map_has_5_positions(self):
        assert len(INVITATION_TIER_MAP) == 5

    def test_tier_ceilings_has_5_positions(self):
        assert len(INVITATION_TIER_CEILINGS) == 5

    def test_position1_ceiling_is_zero(self):
        assert INVITATION_TIER_CEILINGS[1] == 0.0

    def test_position2_ceiling_is_49(self):
        assert INVITATION_TIER_CEILINGS[2] == 49.0

    def test_position3_ceiling_is_399(self):
        assert INVITATION_TIER_CEILINGS[3] == 399.0

    def test_position4_ceiling_is_5000(self):
        assert INVITATION_TIER_CEILINGS[4] == 5000.0

    def test_position5_ceiling_is_none(self):
        assert INVITATION_TIER_CEILINGS[5] is None

    def test_position1_maps_to_deficiency(self):
        assert INVITATION_TIER_MAP[1] == "DEFICIENCY_ESCAPE_ROUTE"

    def test_position2_maps_to_ill_informed(self):
        assert INVITATION_TIER_MAP[2] == "ILL_INFORMED_BRIDGE"

    def test_position3_maps_to_catalyst(self):
        assert INVITATION_TIER_MAP[3] == "NEEDS_INJECTION_CATALYST"

    def test_position4_maps_to_partnership(self):
        assert INVITATION_TIER_MAP[4] == "INFORMATION_HEALTH_PARTNERSHIP"

    def test_position5_maps_to_donor(self):
        assert INVITATION_TIER_MAP[5] == "DONOR_MASTERY_PATH"

    def test_invitation_tier_enum_has_5_values(self):
        assert len(InvitationTier) == 5

    def test_commercial_routing_verdict_has_3_values(self):
        assert len(CommercialRoutingVerdict) == 3


# ═══════════════════════════════════════════════════════════════════════
# TestADR01Constructor — 2-4 char coach_id enforcement
# ═══════════════════════════════════════════════════════════════════════


class TestADR01Constructor:
    def test_router_accepts_2_char(self):
        r = CommercialMatrixRouter(coach_id="AB")
        assert r is not None

    def test_router_accepts_3_char(self):
        r = CommercialMatrixRouter(coach_id="TST")
        assert r is not None

    def test_router_accepts_4_char(self):
        r = CommercialMatrixRouter(coach_id="ABCD")
        assert r is not None

    def test_router_rejects_1_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CommercialMatrixRouter(coach_id="X")

    def test_router_rejects_5_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CommercialMatrixRouter(coach_id="ABCDE")

    def test_gate_rejects_1_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CommercialMatrixGate(coach_id="X")

    def test_gate_rejects_5_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CommercialMatrixGate(coach_id="ABCDE")


# ═══════════════════════════════════════════════════════════════════════
# TestCommercialMatrixRouter — tier resolution
# ═══════════════════════════════════════════════════════════════════════


class TestCommercialMatrixRouter:
    @pytest.mark.parametrize("pos,expected_tier", [
        (1, InvitationTier.DEFICIENCY_ESCAPE_ROUTE),
        (2, InvitationTier.ILL_INFORMED_BRIDGE),
        (3, InvitationTier.NEEDS_INJECTION_CATALYST),
        (4, InvitationTier.INFORMATION_HEALTH_PARTNERSHIP),
        (5, InvitationTier.DONOR_MASTERY_PATH),
    ])
    def test_resolve_tier_all_positions(self, router, pos, expected_tier):
        assert router.resolve_tier(pos) == expected_tier

    def test_resolve_tier_invalid_0(self, router):
        with pytest.raises(ValueError, match="INVALID_COPING_POSITION"):
            router.resolve_tier(0)

    def test_resolve_tier_invalid_6(self, router):
        with pytest.raises(ValueError, match="INVALID_COPING_POSITION"):
            router.resolve_tier(6)

    def test_get_price_ceiling_position1(self, router):
        assert router.get_price_ceiling(1) == 0.0

    def test_get_price_ceiling_position5_none(self, router):
        assert router.get_price_ceiling(5) is None

    def test_resolve_tier_returns_invitation_tier_instance(self, router):
        result = router.resolve_tier(3)
        assert isinstance(result, InvitationTier)


# ═══════════════════════════════════════════════════════════════════════
# TestCommercialMatrixGate — verdict logic
# ═══════════════════════════════════════════════════════════════════════


class TestCommercialMatrixGate:
    # ── PASS cases ───────────────────────────────────────────────────

    def test_pass_position1_free_offer(self, gate):
        result = gate.evaluate(CLIENT_ID, 1, 0.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    def test_pass_position2_at_ceiling(self, gate):
        result = gate.evaluate(CLIENT_ID, 2, 49.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    def test_pass_position2_below_ceiling(self, gate):
        result = gate.evaluate(CLIENT_ID, 2, 25.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    def test_pass_position3_at_ceiling(self, gate):
        result = gate.evaluate(CLIENT_ID, 3, 399.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    def test_pass_position4_at_ceiling(self, gate):
        result = gate.evaluate(CLIENT_ID, 4, 5000.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    def test_pass_position5_any_price(self, gate):
        """Position 5 has no ceiling — always PASS."""
        result = gate.evaluate(CLIENT_ID, 5, 100_000.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    def test_pass_position4_below_ceiling(self, gate):
        result = gate.evaluate(CLIENT_ID, 4, 4999.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value

    # ── PROVISIONAL cases ────────────────────────────────────────────

    def test_provisional_position2_at_99(self, gate):
        """$99 > P2 ceiling ($49) but ≤ P3 ceiling ($399) → 1 tier → PROVISIONAL."""
        result = gate.evaluate(CLIENT_ID, 2, 99.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PROVISIONAL.value

    def test_provisional_position2_below_p3(self, gate):
        result = gate.evaluate(CLIENT_ID, 2, 199.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PROVISIONAL.value

    def test_provisional_position1_below_p2_ceiling(self, gate):
        """$25 > P1 ceiling ($0) but ≤ P2 ceiling ($49) → 1 tier → PROVISIONAL."""
        result = gate.evaluate(CLIENT_ID, 1, 25.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PROVISIONAL.value

    def test_provisional_position3_below_p4(self, gate):
        """$500 > P3 ceiling ($399) but ≤ P4 ceiling ($5000) → 1 tier → PROVISIONAL."""
        result = gate.evaluate(CLIENT_ID, 3, 500.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PROVISIONAL.value

    # ── FAIL_VIOLATION cases ─────────────────────────────────────────

    def test_fail_position1_at_997(self, gate):
        """AC1: $997 to Position 1 → exceeds P2 ($49) and P3 ($399) → 2+ tiers → FAIL."""
        result = gate.evaluate(CLIENT_ID, 1, 997.0)
        assert result.gate_verdict == CommercialRoutingVerdict.FAIL_VIOLATION.value

    def test_fail_position2_mastermind(self, gate):
        """$5000 to Position 2 → exceeds P3 ($399) and P4 ($5000) → FAIL."""
        result = gate.evaluate(CLIENT_ID, 2, 5000.0)
        assert result.gate_verdict == CommercialRoutingVerdict.FAIL_VIOLATION.value

    def test_fail_position1_high_ticket(self, gate):
        result = gate.evaluate(CLIENT_ID, 1, 5000.0)
        assert result.gate_verdict == CommercialRoutingVerdict.FAIL_VIOLATION.value

    def test_fail_position1_very_high(self, gate):
        result = gate.evaluate(CLIENT_ID, 1, 10000.0)
        assert result.gate_verdict == CommercialRoutingVerdict.FAIL_VIOLATION.value

    # ── Schema ───────────────────────────────────────────────────────

    def test_result_has_routing_id(self, gate):
        import uuid
        result = gate.evaluate(CLIENT_ID, 3, 100.0)
        parsed = uuid.UUID(result.routing_id, version=4)
        assert str(parsed) == result.routing_id

    def test_result_has_correct_tier(self, gate):
        result = gate.evaluate(CLIENT_ID, 4, 1000.0)
        assert result.invitation_tier == InvitationTier.INFORMATION_HEALTH_PARTNERSHIP.value

    def test_result_has_correct_coping_position(self, gate):
        result = gate.evaluate(CLIENT_ID, 2, 30.0)
        assert result.computed_coping_position == 2

    def test_result_has_iso8601_timestamp(self, gate):
        from datetime import datetime
        result = gate.evaluate(CLIENT_ID, 3, 200.0)
        dt = datetime.fromisoformat(result.timestamp)
        assert dt is not None

    def test_result_is_commercial_routing_verdict_row(self, gate):
        result = gate.evaluate(CLIENT_ID, 2, 30.0)
        assert isinstance(result, CommercialRoutingVerdictRow)

    def test_receipt_logged_on_evaluate(self, gate, rc):
        gate.evaluate(CLIENT_ID, 3, 200.0)
        entries = rc.query(action="commercial-matrix-gate")
        assert len(entries) >= 1

    def test_invalid_position_raises(self, gate):
        with pytest.raises(ValueError, match="INVALID_COPING_POSITION"):
            gate.evaluate(CLIENT_ID, 0, 100.0)

    def test_two_evaluations_have_unique_routing_ids(self, gate):
        r1 = gate.evaluate(CLIENT_ID, 3, 100.0)
        r2 = gate.evaluate(CLIENT_ID, 3, 100.0)
        assert r1.routing_id != r2.routing_id


# ═══════════════════════════════════════════════════════════════════════
# TestAcceptanceCriteria — explicit spec AC checks
# ═══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """
    AC1 — $997 offer to Position 1 → FAIL_VIOLATION (exceeds ceiling by 2+ tiers)
    AC2 — $99 offer to Position 2 → PROVISIONAL (exceeds by exactly 1 tier)
    AC3 — coping_position=4 → invitation_tier="INFORMATION_HEALTH_PARTNERSHIP"
    """

    def test_ac1_997_to_position1_is_fail_violation(self, gate):
        """AC1: $997 to coping_position=1 must return FAIL_VIOLATION."""
        result = gate.evaluate(CLIENT_ID, 1, 997.0)
        assert result.gate_verdict == CommercialRoutingVerdict.FAIL_VIOLATION.value

    def test_ac1_invitation_tier_is_deficiency(self, gate):
        """AC1: invitation_tier for position 1 is DEFICIENCY_ESCAPE_ROUTE."""
        result = gate.evaluate(CLIENT_ID, 1, 997.0)
        assert result.invitation_tier == InvitationTier.DEFICIENCY_ESCAPE_ROUTE.value

    def test_ac2_99_to_position2_is_provisional(self, gate):
        """AC2: $99 to coping_position=2 must return PROVISIONAL."""
        result = gate.evaluate(CLIENT_ID, 2, 99.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PROVISIONAL.value

    def test_ac2_invitation_tier_is_ill_informed(self, gate):
        """AC2: invitation_tier for position 2 is ILL_INFORMED_BRIDGE."""
        result = gate.evaluate(CLIENT_ID, 2, 99.0)
        assert result.invitation_tier == InvitationTier.ILL_INFORMED_BRIDGE.value

    def test_ac3_position4_maps_to_information_health_partnership(self, router):
        """AC3: coping_position=4 → INFORMATION_HEALTH_PARTNERSHIP."""
        tier = router.resolve_tier(4)
        assert tier == InvitationTier.INFORMATION_HEALTH_PARTNERSHIP
        assert tier.value == "INFORMATION_HEALTH_PARTNERSHIP"

    def test_ac3_gate_position4_pass_below_ceiling(self, gate):
        """AC3: $4999 to position 4 → PASS."""
        result = gate.evaluate(CLIENT_ID, 4, 4999.0)
        assert result.gate_verdict == CommercialRoutingVerdict.PASS.value
        assert result.invitation_tier == InvitationTier.INFORMATION_HEALTH_PARTNERSHIP.value


# ═══════════════════════════════════════════════════════════════════════
# TestPersonaMasking — C-11: no agent name in output JSON
# ═══════════════════════════════════════════════════════════════════════


class TestPersonaMasking:
    AGENT_NAMES = [
        "CommercialMatrixRouter",
        "CommercialMatrixGate",
        "commercial-matrix-gating-engine",
    ]

    def test_no_agent_name_in_result_json(self, gate):
        result = gate.evaluate(CLIENT_ID, 3, 100.0)
        result_json = result.model_dump_json()
        for name in self.AGENT_NAMES:
            assert name not in result_json, f"Agent name {name!r} leaked into JSON"
