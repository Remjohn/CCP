"""
Integration tests — FR-CBCS-14: Conscious Relationship Nurturing Architecture
==============================================================================
Tests cover:
  - CycleStateRouter (active cycle resolution)
  - ConsciousNurturingOrchestrator (cooldown gate + queue lock)
  - ADR-01 constructor enforcement
  - C-11 persona masking
  - Schema validation
  - Acceptance Criteria AC1, AC2, AC3
"""

from __future__ import annotations

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    ActiveCycle,
    COMMERCIAL_COOLDOWN_DAYS,
    COMMERCIAL_COOLDOWN_INFO_SEEKING_THRESHOLD,
    COMMERCIAL_COOLDOWN_PROVISIONAL_MIN_DAYS,
    CooldownGateVerdict,
    NurturingArchError,
    RelationshipCycleLog,
    WEEKLY_CYCLE_WEEKDAY,
)
from src.ccp.services.conscious_nurturing_orchestrator import (
    ConsciousNurturingOrchestrator,
    CycleStateRouter,
)

COACH_ID = "TST"
CLIENT_ID = "CLIENT-Z"


# ── Fixtures ───────────────────────────────────────────────────────────


@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "receipts"))


@pytest.fixture()
def router():
    return CycleStateRouter(coach_id=COACH_ID)


@pytest.fixture()
def orchestrator(rc):
    return ConsciousNurturingOrchestrator(coach_id=COACH_ID, receipt_chain=rc)


# ═══════════════════════════════════════════════════════════════════════
# TestConstants
# ═══════════════════════════════════════════════════════════════════════


class TestConstants:
    def test_commercial_cooldown_days_is_21(self):
        assert COMMERCIAL_COOLDOWN_DAYS == 21.0

    def test_provisional_min_days_is_14(self):
        assert COMMERCIAL_COOLDOWN_PROVISIONAL_MIN_DAYS == 14.0

    def test_info_seeking_threshold_is_0_1(self):
        assert COMMERCIAL_COOLDOWN_INFO_SEEKING_THRESHOLD == 0.1

    def test_weekly_cycle_weekday_is_sunday(self):
        assert WEEKLY_CYCLE_WEEKDAY == 6

    def test_active_cycle_enum_has_3_values(self):
        assert len(ActiveCycle) == 3

    def test_cooldown_gate_verdict_has_3_values(self):
        assert len(CooldownGateVerdict) == 3

    def test_active_cycle_daily_value(self):
        assert ActiveCycle.DAILY.value == "DAILY"

    def test_active_cycle_weekly_value(self):
        assert ActiveCycle.WEEKLY.value == "WEEKLY"

    def test_active_cycle_campaign_value(self):
        assert ActiveCycle.CAMPAIGN.value == "CAMPAIGN"


# ═══════════════════════════════════════════════════════════════════════
# TestADR01Constructor
# ═══════════════════════════════════════════════════════════════════════


class TestADR01Constructor:
    def test_router_accepts_2_char(self):
        assert CycleStateRouter(coach_id="AB") is not None

    def test_router_accepts_3_char(self):
        assert CycleStateRouter(coach_id="TST") is not None

    def test_router_accepts_4_char(self):
        assert CycleStateRouter(coach_id="ABCD") is not None

    def test_router_rejects_1_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CycleStateRouter(coach_id="X")

    def test_router_rejects_5_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            CycleStateRouter(coach_id="ABCDE")

    def test_orchestrator_rejects_1_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            ConsciousNurturingOrchestrator(coach_id="X")

    def test_orchestrator_rejects_5_char(self):
        with pytest.raises(ValueError, match="ADR-01"):
            ConsciousNurturingOrchestrator(coach_id="ABCDE")


# ═══════════════════════════════════════════════════════════════════════
# TestCycleStateRouter — active cycle resolution
# ═══════════════════════════════════════════════════════════════════════


class TestCycleStateRouter:
    def test_campaign_when_search_phase_confirmed(self, router):
        assert router.resolve_cycle(search_phase_confirmed=True) == ActiveCycle.CAMPAIGN

    def test_campaign_when_operator_trigger(self, router):
        assert router.resolve_cycle(operator_manual_trigger=True) == ActiveCycle.CAMPAIGN

    def test_campaign_overrides_sunday(self, router):
        """CAMPAIGN wins even if it's Sunday."""
        assert router.resolve_cycle(search_phase_confirmed=True, current_weekday=6) == ActiveCycle.CAMPAIGN

    def test_weekly_on_sunday(self, router):
        """Sunday (weekday=6) with no campaign → WEEKLY."""
        assert router.resolve_cycle(current_weekday=6) == ActiveCycle.WEEKLY

    def test_daily_on_monday(self, router):
        assert router.resolve_cycle(current_weekday=0) == ActiveCycle.DAILY

    def test_daily_on_saturday(self, router):
        assert router.resolve_cycle(current_weekday=5) == ActiveCycle.DAILY

    @pytest.mark.parametrize("day", [0, 1, 2, 3, 4, 5])
    def test_daily_on_all_non_sunday_weekdays(self, router, day):
        assert router.resolve_cycle(current_weekday=day) == ActiveCycle.DAILY

    def test_returns_active_cycle_instance(self, router):
        result = router.resolve_cycle(current_weekday=0)
        assert isinstance(result, ActiveCycle)


# ═══════════════════════════════════════════════════════════════════════
# TestCooldownGate — PASS verdicts
# ═══════════════════════════════════════════════════════════════════════


class TestCooldownGatePass:
    def test_pass_no_offer(self, orchestrator):
        """No offer in payload → always PASS regardless of days."""
        result = orchestrator.orchestrate(CLIENT_ID, 5.0, contains_offer=False)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PASS.value

    def test_pass_21_days_exactly(self, orchestrator):
        """21 days but NOT > 21 → still FAIL."""
        # 21.0 is NOT > 21.0 → FAIL (strict >)
        result = orchestrator.orchestrate(CLIENT_ID, 21.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value

    def test_pass_above_21_days(self, orchestrator):
        """22 days since offer → PASS."""
        result = orchestrator.orchestrate(CLIENT_ID, 22.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PASS.value

    def test_pass_30_days(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 30.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PASS.value

    def test_pass_no_offer_zero_days(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 0.0, contains_offer=False)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PASS.value


# ═══════════════════════════════════════════════════════════════════════
# TestCooldownGate — PROVISIONAL_OVERRIDE verdicts
# ═══════════════════════════════════════════════════════════════════════


class TestCooldownGateProvisional:
    def test_provisional_days15_high_info_seeking(self, orchestrator):
        """AC2: 15 days, offer=True, info_seeking=0.15 → PROVISIONAL_OVERRIDE."""
        result = orchestrator.orchestrate(CLIENT_ID, 15.0, contains_offer=True,
                                          liwc_info_seeking=0.15)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PROVISIONAL_OVERRIDE.value

    def test_provisional_days14_01_high_seeking(self, orchestrator):
        """14.01 days > 14 threshold + info_seeking=0.11 → PROVISIONAL."""
        result = orchestrator.orchestrate(CLIENT_ID, 14.01, contains_offer=True,
                                          liwc_info_seeking=0.11)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PROVISIONAL_OVERRIDE.value

    def test_provisional_days20_high_seeking(self, orchestrator):
        """20 days (within 21-day window) + high seeking → PROVISIONAL."""
        result = orchestrator.orchestrate(CLIENT_ID, 20.0, contains_offer=True,
                                          liwc_info_seeking=0.2)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PROVISIONAL_OVERRIDE.value


# ═══════════════════════════════════════════════════════════════════════
# TestCooldownGate — FAIL_COOLDOWN_ACTIVE verdicts
# ═══════════════════════════════════════════════════════════════════════


class TestCooldownGateFail:
    def test_fail_ac1_days18_offer(self, orchestrator):
        """AC1: 18 days, offer=True → FAIL_COOLDOWN_ACTIVE."""
        result = orchestrator.orchestrate(CLIENT_ID, 18.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value

    def test_fail_days1_offer(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 1.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value

    def test_fail_days14_exactly(self, orchestrator):
        """14 days exactly is NOT > 14 → FAIL (strict >)."""
        result = orchestrator.orchestrate(CLIENT_ID, 14.0, contains_offer=True,
                                          liwc_info_seeking=0.15)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value

    def test_fail_days15_low_seeking(self, orchestrator):
        """Days 15 but info_seeking <= 0.1 → FAIL."""
        result = orchestrator.orchestrate(CLIENT_ID, 15.0, contains_offer=True,
                                          liwc_info_seeking=0.1)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value

    def test_fail_days0_offer(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 0.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value


# ═══════════════════════════════════════════════════════════════════════
# TestQueueLock — CAMPAIGN cycle enforcement
# ═══════════════════════════════════════════════════════════════════════


class TestQueueLock:
    def test_campaign_sets_queue_lock_true(self, orchestrator):
        """AC3: CAMPAIGN mode → queue_lock_active=True."""
        result = orchestrator.orchestrate(CLIENT_ID, 100.0, search_phase_confirmed=True)
        assert result.queue_lock_active is True
        assert result.active_cycle == ActiveCycle.CAMPAIGN.value

    def test_daily_queue_lock_false(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 100.0, current_weekday=0)
        assert result.queue_lock_active is False

    def test_weekly_queue_lock_false(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 100.0, current_weekday=6)
        assert result.queue_lock_active is False

    def test_operator_trigger_sets_campaign_and_lock(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 100.0, operator_manual_trigger=True)
        assert result.active_cycle == ActiveCycle.CAMPAIGN.value
        assert result.queue_lock_active is True


# ═══════════════════════════════════════════════════════════════════════
# TestOutputSchema
# ═══════════════════════════════════════════════════════════════════════


class TestOutputSchema:
    def test_result_is_relationship_cycle_log(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        assert isinstance(result, RelationshipCycleLog)

    def test_orchestration_id_is_uuid4(self, orchestrator):
        import uuid
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        parsed = uuid.UUID(result.orchestration_id, version=4)
        assert str(parsed) == result.orchestration_id

    def test_two_calls_unique_orchestration_ids(self, orchestrator):
        r1 = orchestrator.orchestrate(CLIENT_ID, 30.0)
        r2 = orchestrator.orchestrate(CLIENT_ID, 30.0)
        assert r1.orchestration_id != r2.orchestration_id

    def test_computation_timestamp_is_iso8601(self, orchestrator):
        from datetime import datetime
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        dt = datetime.fromisoformat(result.computation_timestamp)
        assert dt is not None

    def test_cooldown_expiry_timestamp_is_iso8601(self, orchestrator):
        from datetime import datetime
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        dt = datetime.fromisoformat(result.cooldown_expiry_timestamp)
        assert dt is not None

    def test_coach_id_persisted(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        assert result.coach_id == COACH_ID

    def test_client_id_persisted(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        assert result.client_id == CLIENT_ID

    def test_last_executed_node_persisted(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 30.0, last_executed_node="FR-CBCS-05")
        assert result.last_executed_node == "FR-CBCS-05"

    def test_negative_days_raises(self, orchestrator):
        with pytest.raises(ValueError, match="INVALID_DAYS_ELAPSED"):
            orchestrator.orchestrate(CLIENT_ID, -1.0)


# ═══════════════════════════════════════════════════════════════════════
# TestReceiptChain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    def test_receipt_logged_on_orchestrate(self, orchestrator, rc):
        orchestrator.orchestrate(CLIENT_ID, 30.0)
        entries = rc.query(action="relationship-cycle-orchestrate")
        assert len(entries) >= 1

    def test_multiple_orchestrations_all_logged(self, orchestrator, rc):
        orchestrator.orchestrate(CLIENT_ID, 30.0)
        orchestrator.orchestrate(CLIENT_ID, 15.0, contains_offer=True, liwc_info_seeking=0.15)
        entries = rc.query(action="relationship-cycle-orchestrate")
        assert len(entries) >= 2


# ═══════════════════════════════════════════════════════════════════════
# TestAcceptanceCriteria — explicit spec ACs
# ═══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """
    AC1 — days=18, offer=True → FAIL_COOLDOWN_ACTIVE
    AC2 — days=15, offer=True, info_seeking=0.15 → PROVISIONAL_OVERRIDE
    AC3 — search_phase_confirmed=True → active_cycle=CAMPAIGN, queue_lock=True
    """

    def test_ac1_18_days_fail(self, orchestrator):
        """AC1: 18-day broadcast → FAIL_COOLDOWN_ACTIVE."""
        result = orchestrator.orchestrate(CLIENT_ID, 18.0, contains_offer=True)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE.value

    def test_ac2_15_days_provisional(self, orchestrator):
        """AC2: 15-day + client query info_seeking=0.15 → PROVISIONAL_OVERRIDE."""
        result = orchestrator.orchestrate(CLIENT_ID, 15.0, contains_offer=True,
                                          liwc_info_seeking=0.15)
        assert result.cooldown_gate_verdict == CooldownGateVerdict.PROVISIONAL_OVERRIDE.value

    def test_ac3_campaign_locks_queue(self, orchestrator):
        """AC3: CAMPAIGN mode → queue_lock_active=True."""
        result = orchestrator.orchestrate(CLIENT_ID, 100.0, search_phase_confirmed=True,
                                          contains_offer=False)
        assert result.active_cycle == ActiveCycle.CAMPAIGN.value
        assert result.queue_lock_active is True

    def test_ac3_daily_payload_blocked_in_campaign(self, orchestrator):
        """AC3: CAMPAIGN cycle produces queue_lock=True — daily cycle would be suppressed."""
        result = orchestrator.orchestrate(CLIENT_ID, 100.0, search_phase_confirmed=True,
                                          last_executed_node="FR10-Daily-Ritual")
        assert result.queue_lock_active is True


# ═══════════════════════════════════════════════════════════════════════
# TestPersonaMasking — C-11: no agent names in output JSON
# ═══════════════════════════════════════════════════════════════════════


class TestPersonaMasking:
    AGENT_NAMES = [
        "CycleStateRouter",
        "ConsciousNurturingOrchestrator",
        "conscious-nurturing-orchestrator",
    ]

    def test_no_agent_name_in_result_json(self, orchestrator):
        result = orchestrator.orchestrate(CLIENT_ID, 30.0)
        result_json = result.model_dump_json()
        for name in self.AGENT_NAMES:
            assert name not in result_json, f"Agent name {name!r} leaked into JSON"
