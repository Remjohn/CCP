"""
FR59 — Campaign Orchestration Agent: Integration Tests
=======================================================
Covers:
- CampaignStateResolver (all 4 state transitions, boundary conditions)
- CampaignInitializationGate (all 3 verdicts, boundary conditions)
- strip_commercial_urls / payload_contains_commercial_url
- CampaignOrchestrator.launch (happy-path, provisional, hard-fail, receipts)
- Acceptance Criteria AC1-AC3 (verbatim from spec)
- coach_id ADR-01 guard
"""

from __future__ import annotations

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    CampaignExecutionLogRow,
    CampaignGateVerdict,
    CampaignOrchestrationError,
    MasterCampaignState,
)
from src.ccp.services.campaign_orchestrator import (
    ADMIN_ROLES,
    LEGACY_BRIEF_SENTINEL,
    CampaignInitializationGate,
    CampaignOrchestrator,
    CampaignStateResolver,
    payload_contains_commercial_url,
    strip_commercial_urls,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="TST", log_dir=tmp_path)


@pytest.fixture()
def orchestrator(rc):
    return CampaignOrchestrator(coach_id="coachA", receipt_chain=rc)


BLUEPRINT_ID = "bp-0001-0000-0000-000000000001"
OPERATOR_ID = "operator-human-01"
ROSTER = ["client-a", "client-b", "client-c"]
BRIEF_ID = "brief-0001"


# ---------------------------------------------------------------------------
# CampaignStateResolver — all 4 states
# ---------------------------------------------------------------------------

class TestCampaignStateResolver:

    def test_queued_before_launch(self):
        """days = -1 (future launch date) → QUEUED_PENDING_LAUNCH."""
        state = CampaignStateResolver(-1.0).resolve()
        assert state == MasterCampaignState.QUEUED_PENDING_LAUNCH

    def test_queued_on_negative_boundary(self):
        state = CampaignStateResolver(-0.001).resolve()
        assert state == MasterCampaignState.QUEUED_PENDING_LAUNCH

    def test_anchoring_day_0(self):
        """days = 0 → ANCHORING_DAY_1_TO_3."""
        state = CampaignStateResolver(0.0).resolve()
        assert state == MasterCampaignState.ANCHORING_DAY_1_TO_3

    def test_anchoring_day_1(self):
        state = CampaignStateResolver(1.0).resolve()
        assert state == MasterCampaignState.ANCHORING_DAY_1_TO_3

    def test_anchoring_day_3(self):
        """days = 3 exactly → ANCHORING_DAY_1_TO_3 (inclusive boundary)."""
        state = CampaignStateResolver(3.0).resolve()
        assert state == MasterCampaignState.ANCHORING_DAY_1_TO_3

    def test_conversion_day_4(self):
        """days = 4 → CONVERSION_WINDOW_ACTIVE."""
        state = CampaignStateResolver(4.0).resolve()
        assert state == MasterCampaignState.CONVERSION_WINDOW_ACTIVE

    def test_conversion_day_5(self):
        state = CampaignStateResolver(5.0).resolve()
        assert state == MasterCampaignState.CONVERSION_WINDOW_ACTIVE

    def test_conversion_day_7(self):
        """days = 7 exactly → CONVERSION_WINDOW_ACTIVE (inclusive boundary)."""
        state = CampaignStateResolver(7.0).resolve()
        assert state == MasterCampaignState.CONVERSION_WINDOW_ACTIVE

    def test_cooldown_day_8(self):
        """AC3: days = 8 → COOLDOWN_RESOLVED."""
        state = CampaignStateResolver(8.0).resolve()
        assert state == MasterCampaignState.COOLDOWN_RESOLVED

    def test_cooldown_large_days(self):
        state = CampaignStateResolver(100.0).resolve()
        assert state == MasterCampaignState.COOLDOWN_RESOLVED

    @pytest.mark.parametrize("days,expected", [
        (-5,   MasterCampaignState.QUEUED_PENDING_LAUNCH),
        (0,    MasterCampaignState.ANCHORING_DAY_1_TO_3),
        (2,    MasterCampaignState.ANCHORING_DAY_1_TO_3),
        (3,    MasterCampaignState.ANCHORING_DAY_1_TO_3),
        (3.01, MasterCampaignState.CONVERSION_WINDOW_ACTIVE),
        (7,    MasterCampaignState.CONVERSION_WINDOW_ACTIVE),
        (7.01, MasterCampaignState.COOLDOWN_RESOLVED),
        (30,   MasterCampaignState.COOLDOWN_RESOLVED),
    ])
    def test_state_table(self, days, expected):
        assert CampaignStateResolver(days).resolve() == expected


# ---------------------------------------------------------------------------
# CampaignInitializationGate — all 3 verdicts
# ---------------------------------------------------------------------------

class TestCampaignInitializationGate:

    def test_pass_all_conditions(self):
        verdict = CampaignInitializationGate("admin", 3, BRIEF_ID).evaluate()
        assert verdict == CampaignGateVerdict.PASS_AUTHORIZED

    def test_pass_operator_role(self):
        verdict = CampaignInitializationGate("operator", 1, BRIEF_ID).evaluate()
        assert verdict == CampaignGateVerdict.PASS_AUTHORIZED

    def test_pass_coach_admin_role(self):
        verdict = CampaignInitializationGate("coach_admin", 5, BRIEF_ID).evaluate()
        assert verdict == CampaignGateVerdict.PASS_AUTHORIZED

    def test_provisional_legacy_mode(self):
        """Conditions 1&2 pass, brief_id = LEGACY_BRIEF_SENTINEL → PROVISIONAL."""
        verdict = CampaignInitializationGate("admin", 3, LEGACY_BRIEF_SENTINEL).evaluate()
        assert verdict == CampaignGateVerdict.PROVISIONAL_LEGACY_MODE

    def test_provisional_brief_id_negative_one(self):
        verdict = CampaignInitializationGate("admin", 5, -1).evaluate()
        assert verdict == CampaignGateVerdict.PROVISIONAL_LEGACY_MODE

    def test_fail_non_admin_role(self):
        """AC1: caller_role = 'discord_bot' → FAIL_ABORTED."""
        verdict = CampaignInitializationGate("discord_bot", 3, BRIEF_ID).evaluate()
        assert verdict == CampaignGateVerdict.FAIL_ABORTED

    def test_fail_assistant_role(self):
        verdict = CampaignInitializationGate("Assistant", 3, BRIEF_ID).evaluate()
        assert verdict == CampaignGateVerdict.FAIL_ABORTED

    def test_fail_zero_roster(self):
        """roster_size = 0 → FAIL_ABORTED."""
        verdict = CampaignInitializationGate("admin", 0, BRIEF_ID).evaluate()
        assert verdict == CampaignGateVerdict.FAIL_ABORTED

    def test_fail_takes_precedence_over_provisional(self):
        """
        Even if brief_id is legacy sentinel, if role is wrong → FAIL_ABORTED.
        FAIL check (cond_1 / cond_2) is evaluated first.
        """
        verdict = CampaignInitializationGate("discord_bot", 0, LEGACY_BRIEF_SENTINEL).evaluate()
        assert verdict == CampaignGateVerdict.FAIL_ABORTED

    def test_fail_zero_roster_admin_role_legacy(self):
        """Zero roster → FAIL regardless of brief_id."""
        verdict = CampaignInitializationGate("admin", 0, LEGACY_BRIEF_SENTINEL).evaluate()
        assert verdict == CampaignGateVerdict.FAIL_ABORTED


# ---------------------------------------------------------------------------
# Commercial URL detection / stripping (§7 Task 3 / §10 safety test)
# ---------------------------------------------------------------------------

class TestCommercialUrlSafety:

    def test_detects_https_url(self):
        assert payload_contains_commercial_url("Buy here https://stripe.com/pay") is True

    def test_detects_http_url(self):
        assert payload_contains_commercial_url("Click http://offer.co") is True

    def test_detects_www_url(self):
        assert payload_contains_commercial_url("Visit www.stripe.com") is True

    def test_clean_payload_no_url(self):
        assert payload_contains_commercial_url("Hello, your next session begins soon.") is False

    def test_strip_https_url(self):
        result = strip_commercial_urls("Buy now https://checkout.stripe.com/pay/abc123")
        assert "https" not in result
        assert "stripe" not in result

    def test_strip_www_url(self):
        result = strip_commercial_urls("Go to www.stripe.com today!")
        assert "www.stripe.com" not in result

    def test_strip_preserves_non_url_text(self):
        result = strip_commercial_urls("Hello world. No links here.")
        assert "Hello world" in result

    def test_strip_multiple_urls(self):
        result = strip_commercial_urls("See https://a.com and also www.b.com for details.")
        assert "https://a.com" not in result
        assert "www.b.com" not in result


# ---------------------------------------------------------------------------
# Acceptance Criteria (verbatim from spec §8)
# ---------------------------------------------------------------------------

class TestAcceptanceCriteria:

    def test_ac1_discord_bot_role_fail_aborted(self, orchestrator):
        """AC1: caller_role='discord_bot' → FAIL_ABORTED (hard automation lockdown)."""
        with pytest.raises(ValueError) as exc_info:
            orchestrator.launch(
                campaign_blueprint_id=BLUEPRINT_ID,
                operator_auth_id="bot-scheduler",
                caller_role="discord_bot",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )
        assert CampaignOrchestrationError.FAIL_ABORTED in str(exc_info.value)

    def test_ac2_csv_broadcast_provisional_legacy(self, orchestrator):
        """AC2: brief_id=-1 (legacy CSV) → PROVISIONAL_LEGACY_MODE."""
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=-1,
        )
        assert row.gate_verdict == CampaignGateVerdict.PROVISIONAL_LEGACY_MODE.value

    def test_ac3_day_8_state_cooldown(self, orchestrator):
        """AC3: days_since_launch=8 → master_campaign_state=COOLDOWN_RESOLVED."""
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
            days_since_launch=8.0,
        )
        assert row.master_campaign_state == MasterCampaignState.COOLDOWN_RESOLVED.value


# ---------------------------------------------------------------------------
# CampaignOrchestrator — row structure & receipt chain
# ---------------------------------------------------------------------------

class TestCampaignOrchestratorRow:

    def test_pass_row_fields(self, orchestrator):
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
            days_since_launch=0.0,
        )
        assert isinstance(row, CampaignExecutionLogRow)
        assert row.campaign_blueprint_id == BLUEPRINT_ID
        assert row.coach_id == "coachA"
        assert row.operator_auth_id == OPERATOR_ID
        assert row.roster_size_at_launch == 3
        assert row.gate_verdict == CampaignGateVerdict.PASS_AUTHORIZED.value
        assert row.master_campaign_state == MasterCampaignState.ANCHORING_DAY_1_TO_3.value
        assert row.execution_run_id  # non-empty UUID
        assert row.started_at  # non-empty ISO string

    def test_execution_run_id_is_uuid(self, orchestrator):
        import uuid as _uuid
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
        )
        _uuid.UUID(row.execution_run_id)

    def test_started_at_is_iso_with_tz(self, orchestrator):
        from datetime import datetime
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
        )
        dt = datetime.fromisoformat(row.started_at)
        assert dt.tzinfo is not None

    def test_roster_size_counts_list_length(self, orchestrator):
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=["a", "b"],
            brief_id=BRIEF_ID,
        )
        assert row.roster_size_at_launch == 2

    def test_empty_roster_fails(self, orchestrator):
        with pytest.raises(ValueError):
            orchestrator.launch(
                campaign_blueprint_id=BLUEPRINT_ID,
                operator_auth_id=OPERATOR_ID,
                caller_role="admin",
                roster=[],
                brief_id=BRIEF_ID,
            )


# ---------------------------------------------------------------------------
# CampaignOrchestrator — receipt chain entries
# ---------------------------------------------------------------------------

class TestCampaignOrchestratorReceipts:

    def test_pass_logs_two_receipts(self, rc, orchestrator):
        orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
        )
        state_entries = rc.query(action="campaign-state-resolve")
        gate_entries = rc.query(action="campaign-init-gate")
        assert len(state_entries) >= 1
        assert len(gate_entries) >= 1

    def test_fail_logs_receipts_before_raising(self, rc, orchestrator):
        with pytest.raises(ValueError):
            orchestrator.launch(
                campaign_blueprint_id=BLUEPRINT_ID,
                operator_auth_id="bot",
                caller_role="discord_bot",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )
        state_entries = rc.query(action="campaign-state-resolve")
        gate_entries = rc.query(action="campaign-init-gate")
        assert len(state_entries) >= 1
        assert len(gate_entries) >= 1
        assert any("FAIL_ABORTED" in e.output_summary for e in gate_entries)

    def test_provisional_logs_two_receipts(self, rc, orchestrator):
        orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=-1,
        )
        assert len(rc.query(action="campaign-state-resolve")) >= 1
        assert len(rc.query(action="campaign-init-gate")) >= 1

    def test_receipt_contains_coach_id(self, rc, orchestrator):
        orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
        )
        entries = rc.query(action="campaign-state-resolve")
        assert any("coachA" in e.output_summary for e in entries)

    def test_gate_receipt_has_parent_id(self, rc, orchestrator):
        orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
        )
        gate_entries = rc.query(action="campaign-init-gate")
        assert all(e.parent_receipt_id is not None for e in gate_entries)


# ---------------------------------------------------------------------------
# CampaignOrchestrator — FAIL hard-abort behaviour
# ---------------------------------------------------------------------------

class TestHardAbortBehaviour:

    def test_raises_value_error_on_fail(self, orchestrator):
        with pytest.raises(ValueError):
            orchestrator.launch(
                campaign_blueprint_id=BLUEPRINT_ID,
                operator_auth_id="bot",
                caller_role="bot",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )

    def test_error_message_contains_fail_aborted(self, orchestrator):
        with pytest.raises(ValueError) as exc_info:
            orchestrator.launch(
                campaign_blueprint_id=BLUEPRINT_ID,
                operator_auth_id="bot",
                caller_role="anonymous",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )
        assert "FAIL_ABORTED" in str(exc_info.value)

    def test_no_row_returned_on_fail(self, orchestrator):
        result = None
        try:
            result = orchestrator.launch(
                campaign_blueprint_id=BLUEPRINT_ID,
                operator_auth_id="bot",
                caller_role="anonymous",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )
        except ValueError:
            pass
        assert result is None


# ---------------------------------------------------------------------------
# CampaignOrchestrator — ADR-01 coach_id guard
# ---------------------------------------------------------------------------

class TestCoachIdGuard:

    def test_short_coach_id_raises(self, rc):
        with pytest.raises(ValueError):
            CampaignOrchestrator(coach_id="X", receipt_chain=rc)

    def test_empty_coach_id_raises(self, rc):
        with pytest.raises(ValueError):
            CampaignOrchestrator(coach_id="", receipt_chain=rc)

    def test_valid_min_coach_id(self, rc):
        orch = CampaignOrchestrator(coach_id="AB", receipt_chain=rc)
        assert orch is not None


# ---------------------------------------------------------------------------
# CampaignOrchestrator — multiple launches (receipt accumulation)
# ---------------------------------------------------------------------------

class TestMultipleLaunches:

    def test_each_launch_unique_execution_id(self, orchestrator):
        ids = set()
        for i in range(4):
            row = orchestrator.launch(
                campaign_blueprint_id=f"bp-{i:04d}",
                operator_auth_id=OPERATOR_ID,
                caller_role="admin",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )
            ids.add(row.execution_run_id)
        assert len(ids) == 4

    def test_receipts_accumulate_over_launches(self, rc, orchestrator):
        for i in range(3):
            orchestrator.launch(
                campaign_blueprint_id=f"bp-{i:04d}",
                operator_auth_id=OPERATOR_ID,
                caller_role="admin",
                roster=ROSTER,
                brief_id=BRIEF_ID,
            )
        assert len(rc.query(action="campaign-state-resolve")) == 3


# ---------------------------------------------------------------------------
# State progression integration — spec §10 Test_State_Progression_Timing
# ---------------------------------------------------------------------------

class TestStateProgressionTiming:

    def test_day_5_is_conversion_active(self, orchestrator):
        """Spec §10: days=5 → CONVERSION_WINDOW_ACTIVE."""
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
            days_since_launch=5.0,
        )
        assert row.master_campaign_state == MasterCampaignState.CONVERSION_WINDOW_ACTIVE.value

    def test_day_0_is_anchoring(self, orchestrator):
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=ROSTER,
            brief_id=BRIEF_ID,
            days_since_launch=0.0,
        )
        assert row.master_campaign_state == MasterCampaignState.ANCHORING_DAY_1_TO_3.value


# ---------------------------------------------------------------------------
# Roster size integration — spec §10 Test_Roster_Size_Count_Array
# ---------------------------------------------------------------------------

class TestRosterSizeCount:

    def test_three_element_roster(self, orchestrator):
        """Spec §10: roster=['A','B','C'] → roster_size_at_launch=3."""
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=["A", "B", "C"],
            brief_id=BRIEF_ID,
        )
        assert row.roster_size_at_launch == 3

    def test_single_client_roster(self, orchestrator):
        row = orchestrator.launch(
            campaign_blueprint_id=BLUEPRINT_ID,
            operator_auth_id=OPERATOR_ID,
            caller_role="admin",
            roster=["only-one"],
            brief_id=BRIEF_ID,
        )
        assert row.roster_size_at_launch == 1
