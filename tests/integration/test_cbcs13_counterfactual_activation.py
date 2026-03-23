"""
Integration tests — FR-CBCS-13: Counterfactual Activation Window
=================================================================
Tests cover:
  - CounterfactualTriggerRouter (activation mode resolution)
  - EpistemicDeliveryGuard (temporal gate + provisional edge-case)
  - ADR-01 constructor enforcement
  - C-11 persona masking
  - Schema validation
  - All gate verdict permutations
"""

from __future__ import annotations

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    ActivationMode,
    COUNTERFACTUAL_GATE_HOURS,
    COUNTERFACTUAL_PROVISIONAL_COGNITIVE_THRESHOLD,
    COUNTERFACTUAL_PROVISIONAL_MIN_HOURS,
    DOWNWARD_DRIVERS,
    EpistemicActivationRow,
    EpistemicGateVerdict,
    UPWARD_DRIVERS,
)
from src.ccp.services.counterfactual_activation import (
    CounterfactualTriggerRouter,
    EpistemicDeliveryGuard,
)

COACH_ID = "TST"
CLIENT_ID = "CLIENT-X"


# ── Fixtures ───────────────────────────────────────────────────────────


@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "receipts"))


@pytest.fixture()
def router():
    return CounterfactualTriggerRouter(coach_id=COACH_ID)


@pytest.fixture()
def guard(rc):
    return EpistemicDeliveryGuard(coach_id=COACH_ID, receipt_chain=rc)


# ═══════════════════════════════════════════════════════════════════════
# TestConstants
# ═══════════════════════════════════════════════════════════════════════


class TestConstants:
    def test_gate_hours_is_72(self):
        assert COUNTERFACTUAL_GATE_HOURS == 72.0

    def test_provisional_min_hours_is_48(self):
        assert COUNTERFACTUAL_PROVISIONAL_MIN_HOURS == 48.0

    def test_provisional_cog_threshold_is_0_1(self):
        assert COUNTERFACTUAL_PROVISIONAL_COGNITIVE_THRESHOLD == 0.1

    def test_upward_drivers_contains_expansion(self):
        assert "Expansion" in UPWARD_DRIVERS

    def test_upward_drivers_contains_autonomy(self):
        assert "Autonomy" in UPWARD_DRIVERS

    def test_upward_drivers_contains_growth(self):
        assert "Growth" in UPWARD_DRIVERS

    def test_upward_drivers_contains_achievement(self):
        assert "Achievement" in UPWARD_DRIVERS

    def test_downward_drivers_contains_security(self):
        assert "Security" in DOWNWARD_DRIVERS

    def test_downward_drivers_contains_belonging(self):
        assert "Belonging" in DOWNWARD_DRIVERS

    def test_downward_drivers_contains_safety(self):
        assert "Safety" in DOWNWARD_DRIVERS

    def test_downward_drivers_contains_connection(self):
        assert "Connection" in DOWNWARD_DRIVERS

    def test_activation_mode_enum_has_2_values(self):
        assert len(ActivationMode) == 2

    def test_epistemic_gate_verdict_has_3_values(self):
        assert len(EpistemicGateVerdict) == 3


# ═══════════════════════════════════════════════════════════════════════
# TestADR01Constructor
# ═══════════════════════════════════════════════════════════════════════


class TestADR01Constructor:
    def test_router_accepts_2_char(self):
        assert CounterfactualTriggerRouter(coach_id="AB") is not None

    def test_router_accepts_3_char(self):
        assert CounterfactualTriggerRouter(coach_id="TST") is not None

    def test_router_accepts_4_char(self):
        assert CounterfactualTriggerRouter(coach_id="ABCD") is not None

    def test_router_rejects_1_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CounterfactualTriggerRouter(coach_id="X")

    def test_router_rejects_5_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CounterfactualTriggerRouter(coach_id="ABCDE")

    def test_guard_rejects_1_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            EpistemicDeliveryGuard(coach_id="X")

    def test_guard_rejects_5_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            EpistemicDeliveryGuard(coach_id="ABCDE")


# ═══════════════════════════════════════════════════════════════════════
# TestCounterfactualTriggerRouter — activation mode resolution
# ═══════════════════════════════════════════════════════════════════════


class TestCounterfactualTriggerRouter:
    @pytest.mark.parametrize("driver", ["Expansion", "Autonomy", "Growth", "Achievement"])
    def test_upward_drivers_resolve_to_upward(self, router, driver):
        assert router.resolve_activation_mode(driver) == ActivationMode.UPWARD_COUNTERFACTUAL

    @pytest.mark.parametrize("driver", ["Security", "Belonging", "Safety", "Connection"])
    def test_downward_drivers_resolve_to_downward(self, router, driver):
        assert router.resolve_activation_mode(driver) == ActivationMode.DOWNWARD_COUNTERFACTUAL

    def test_unknown_driver_raises(self, router):
        with pytest.raises(ValueError, match="ROUTING_ERROR"):
            router.resolve_activation_mode("Ambition")

    def test_case_sensitive_unknown(self, router):
        """Lowercase 'expansion' does not match 'Expansion'."""
        with pytest.raises(ValueError, match="ROUTING_ERROR"):
            router.resolve_activation_mode("expansion")

    def test_returns_activation_mode_instance(self, router):
        result = router.resolve_activation_mode("Security")
        assert isinstance(result, ActivationMode)


# ═══════════════════════════════════════════════════════════════════════
# TestEpistemicDeliveryGuard — PASS verdicts
# ═══════════════════════════════════════════════════════════════════════


class TestEpistemicDeliveryGuardPass:
    def test_pass_exactly_72_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Expansion", 72.0, False)
        assert result.gate_verdict == EpistemicGateVerdict.PASS.value

    def test_pass_80_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Autonomy", 80.0, False)
        assert result.gate_verdict == EpistemicGateVerdict.PASS.value

    def test_pass_120_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Growth", 120.0, False)
        assert result.gate_verdict == EpistemicGateVerdict.PASS.value

    def test_pass_dispatched_text_preserved(self, guard):
        result = guard.evaluate(CLIENT_ID, "Achievement", 75.0, False, dispatched_text="Your script here.")
        assert result.dispatched_text == "Your script here."
        assert result.gate_verdict == EpistemicGateVerdict.PASS.value


# ═══════════════════════════════════════════════════════════════════════
# TestEpistemicDeliveryGuard — PROVISIONAL verdicts
# ═══════════════════════════════════════════════════════════════════════


class TestEpistemicDeliveryGuardProvisional:
    def test_provisional_48_to_72_high_cog(self, guard):
        """48 ≤ hours < 72, not replied, cog > 0.1 → PROVISIONAL_EARLY_FIRE."""
        result = guard.evaluate(CLIENT_ID, "Security", 50.0, False, liwc_cog_processes=0.12)
        assert result.gate_verdict == EpistemicGateVerdict.PROVISIONAL_EARLY_FIRE.value

    def test_provisional_exactly_48_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Belonging", 48.0, False, liwc_cog_processes=0.15)
        assert result.gate_verdict == EpistemicGateVerdict.PROVISIONAL_EARLY_FIRE.value

    def test_provisional_71_99_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Safety", 71.99, False, liwc_cog_processes=0.2)
        assert result.gate_verdict == EpistemicGateVerdict.PROVISIONAL_EARLY_FIRE.value

    def test_provisional_dispatched_text_preserved(self, guard):
        result = guard.evaluate(CLIENT_ID, "Connection", 55.0, False,
                                liwc_cog_processes=0.11, dispatched_text="Draft script.")
        assert result.dispatched_text == "Draft script."


# ═══════════════════════════════════════════════════════════════════════
# TestEpistemicDeliveryGuard — FAIL_BLOCKED verdicts
# ═══════════════════════════════════════════════════════════════════════


class TestEpistemicDeliveryGuardFail:
    def test_fail_client_replied(self, guard):
        """client_replied=True always FAIL regardless of hours."""
        result = guard.evaluate(CLIENT_ID, "Growth", 100.0, True)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value

    def test_fail_under_48_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Belonging", 30.0, False, liwc_cog_processes=0.05)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value

    def test_fail_48_72_low_cog(self, guard):
        """48-72 range but cog ≤ 0.1 → FAIL (not provisional)."""
        result = guard.evaluate(CLIENT_ID, "Security", 60.0, False, liwc_cog_processes=0.05)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value

    def test_fail_exactly_0_hours(self, guard):
        result = guard.evaluate(CLIENT_ID, "Expansion", 0.0, False)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value

    def test_fail_replied_overrides_high_hours(self, guard):
        """Even at 200h, if client replied → FAIL_BLOCKED."""
        result = guard.evaluate(CLIENT_ID, "Achievement", 200.0, True)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value

    def test_fail_dispatched_text_cleared(self, guard):
        """FAIL_BLOCKED must null out dispatched_text."""
        result = guard.evaluate(CLIENT_ID, "Autonomy", 10.0, False, dispatched_text="Sneak text")
        assert result.dispatched_text is None

    def test_fail_48_exactly_at_threshold_cog(self, guard):
        """cog == 0.1 exactly → not > 0.1 → FAIL_BLOCKED."""
        result = guard.evaluate(CLIENT_ID, "Safety", 55.0, False, liwc_cog_processes=0.1)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value


# ═══════════════════════════════════════════════════════════════════════
# TestOutputSchema
# ═══════════════════════════════════════════════════════════════════════


class TestOutputSchema:
    def test_result_is_epistemic_activation_row(self, guard):
        result = guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        assert isinstance(result, EpistemicActivationRow)

    def test_eval_id_is_uuid4(self, guard):
        import uuid
        result = guard.evaluate(CLIENT_ID, "Expansion", 75.0, False)
        parsed = uuid.UUID(result.eval_id, version=4)
        assert str(parsed) == result.eval_id

    def test_two_calls_have_unique_eval_ids(self, guard):
        r1 = guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        r2 = guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        assert r1.eval_id != r2.eval_id

    def test_last_evaluated_is_iso8601(self, guard):
        from datetime import datetime
        result = guard.evaluate(CLIENT_ID, "Security", 80.0, False)
        dt = datetime.fromisoformat(result.last_evaluated)
        assert dt is not None

    def test_hours_elapsed_persisted(self, guard):
        result = guard.evaluate(CLIENT_ID, "Autonomy", 55.5, False, liwc_cog_processes=0.2)
        assert result.hours_elapsed_since_offer == 55.5

    def test_coach_id_persisted(self, guard):
        result = guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        assert result.coach_id == COACH_ID

    def test_client_id_persisted(self, guard):
        result = guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        assert result.client_id == CLIENT_ID

    def test_negative_hours_raises(self, guard):
        with pytest.raises(ValueError, match="INVALID_HOURS_ELAPSED"):
            guard.evaluate(CLIENT_ID, "Growth", -1.0, False)


# ═══════════════════════════════════════════════════════════════════════
# TestReceiptChain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    def test_receipt_logged_on_evaluate(self, guard, rc):
        guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        entries = rc.query(action="epistemic-gate-evaluate")
        assert len(entries) >= 1

    def test_multiple_evaluations_all_logged(self, guard, rc):
        guard.evaluate(CLIENT_ID, "Security", 80.0, False)
        guard.evaluate(CLIENT_ID, "Safety", 50.0, False, liwc_cog_processes=0.15)
        entries = rc.query(action="epistemic-gate-evaluate")
        assert len(entries) >= 2


# ═══════════════════════════════════════════════════════════════════════
# TestAcceptanceCriteria — explicit spec ACs
# ═══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """
    AC1 — primary_driver="Expansion" → activation_mode="UPWARD_COUNTERFACTUAL"
    AC2 — hours=80, not replied → gate_verdict="PASS"
    AC3 — hours=50, not replied, cog=0.12 → gate_verdict="PROVISIONAL_EARLY_FIRE"
    AC4 — client_replied=True → gate_verdict="FAIL_BLOCKED"
    AC5 — hours=30, low cog → gate_verdict="FAIL_BLOCKED"
    """

    def test_ac1_expansion_maps_to_upward(self, router):
        """AC1: Expansion → UPWARD_COUNTERFACTUAL."""
        mode = router.resolve_activation_mode("Expansion")
        assert mode == ActivationMode.UPWARD_COUNTERFACTUAL

    def test_ac1_activation_mode_in_row(self, guard):
        """AC1: activation_mode_assigned field reflects UPWARD_COUNTERFACTUAL."""
        result = guard.evaluate(CLIENT_ID, "Expansion", 80.0, False)
        assert result.activation_mode_assigned == ActivationMode.UPWARD_COUNTERFACTUAL.value

    def test_ac2_80h_not_replied_is_pass(self, guard):
        """AC2: 80h, not replied → PASS."""
        result = guard.evaluate(CLIENT_ID, "Autonomy", 80.0, False)
        assert result.gate_verdict == EpistemicGateVerdict.PASS.value

    def test_ac3_50h_cog_high_is_provisional(self, guard):
        """AC3: 50h, cog=0.12 → PROVISIONAL_EARLY_FIRE."""
        result = guard.evaluate(CLIENT_ID, "Security", 50.0, False, liwc_cog_processes=0.12)
        assert result.gate_verdict == EpistemicGateVerdict.PROVISIONAL_EARLY_FIRE.value

    def test_ac4_replied_true_is_fail(self, guard):
        """AC4: client_replied=True → FAIL_BLOCKED."""
        result = guard.evaluate(CLIENT_ID, "Growth", 100.0, True)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value

    def test_ac5_30h_low_cog_is_fail(self, guard):
        """AC5: 30h, low cog → FAIL_BLOCKED."""
        result = guard.evaluate(CLIENT_ID, "Belonging", 30.0, False, liwc_cog_processes=0.05)
        assert result.gate_verdict == EpistemicGateVerdict.FAIL_BLOCKED.value


# ═══════════════════════════════════════════════════════════════════════
# TestPersonaMasking — C-11: no agent names in output JSON
# ═══════════════════════════════════════════════════════════════════════


class TestPersonaMasking:
    AGENT_NAMES = [
        "CounterfactualTriggerRouter",
        "EpistemicDeliveryGuard",
        "epistemic-delivery-guard",
        "counterfactual-generator-agent",
    ]

    def test_no_agent_name_in_result_json(self, guard):
        result = guard.evaluate(CLIENT_ID, "Growth", 80.0, False)
        result_json = result.model_dump_json()
        for name in self.AGENT_NAMES:
            assert name not in result_json, f"Agent name {name!r} leaked into JSON"
