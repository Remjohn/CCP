"""
Tests — FR53: Conversion Sequence Generator
=============================================
Covers VulnerabilityModeResolver, DormancyRecoveryGate,
ConversionSequenceRouter, all three ACs, edge cases,
receipt chain, and ADR-01 isolation.
"""

from __future__ import annotations

import shutil
import tempfile
import uuid

import pytest

from src.ccp.models.cpsc_models import (
    ConversionSequencePayloadRow,
    DormancyGateVerdict,
    SequenceError,
    SequenceVulnerabilityMode,
)
from src.ccp.services.conversion_sequence_router import (
    DORMANCY_PASS_MAX_HOURS,
    DORMANCY_PROVISIONAL_MAX_HOURS,
    SPT_AFFECTIVE_THRESHOLD,
    SPT_NULL_FALLBACK,
    ConversionSequenceRouter,
    DormancyRecoveryGate,
    VulnerabilityModeResolver,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rc(tmp_dir: str) -> ReceiptChain:
    return ReceiptChain(coach_acronym="FR3", log_dir=tmp_dir)


def _make_router(tmp_dir: str, coach_id: str = "coach-fr53") -> ConversionSequenceRouter:
    return ConversionSequenceRouter(coach_id=coach_id, receipt_chain=_make_rc(tmp_dir))


def _default_route_kwargs(hours: float = 10.0, spt: int = 2) -> dict:
    return dict(
        client_id="client-001",
        spt_stage=spt,
        hours_since_last_message=hours,
        current_sequence_step=1,
        next_payload_string="Day 1 anchor message text.",
    )


# ---------------------------------------------------------------------------
# VulnerabilityModeResolver Tests
# ---------------------------------------------------------------------------

class TestVulnerabilityModeResolver:

    def test_spt_none_fallback_objective(self):
        """Spec §6: null spt → -1 → OBJECTIVE_REFLECTIVE."""
        assert VulnerabilityModeResolver(None).resolve() == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_negative_1_objective(self):
        assert VulnerabilityModeResolver(-1).resolve() == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_0_objective(self):
        assert VulnerabilityModeResolver(0).resolve() == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_1_objective(self):
        assert VulnerabilityModeResolver(1).resolve() == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_2_objective(self):
        assert VulnerabilityModeResolver(2).resolve() == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_3_affective(self):
        # Threshold: spt_stage >= 3
        assert VulnerabilityModeResolver(3).resolve() == SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT

    # AC3 value
    def test_spt_4_affective(self):
        """AC3: spt_stage=4 → AFFECTIVE_ATTACHMENT."""
        assert VulnerabilityModeResolver(4).resolve() == SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT

    def test_spt_5_affective(self):
        assert VulnerabilityModeResolver(5).resolve() == SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT

    def test_spt_boundary_exactly_threshold(self):
        assert VulnerabilityModeResolver(SPT_AFFECTIVE_THRESHOLD).resolve() == SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT

    def test_spt_one_below_threshold_objective(self):
        assert VulnerabilityModeResolver(SPT_AFFECTIVE_THRESHOLD - 1).resolve() == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE


# ---------------------------------------------------------------------------
# DormancyRecoveryGate Tests
# ---------------------------------------------------------------------------

class TestDormancyRecoveryGate:

    # Spec §10: [12.0, 48.0, 80.0] → [PASS_ACTIVE, PROVISIONAL, FAIL]
    def test_spec_example_floats(self):
        expected = [
            DormancyGateVerdict.PASS_ACTIVE,
            DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY,
            DormancyGateVerdict.FAIL_DORMANT_ABORT,
        ]
        for hours, exp in zip([12.0, 48.0, 80.0], expected):
            assert DormancyRecoveryGate(hours).evaluate() == exp

    def test_zero_hours_pass(self):
        assert DormancyRecoveryGate(0.0).evaluate() == DormancyGateVerdict.PASS_ACTIVE

    def test_just_below_36_pass(self):
        assert DormancyRecoveryGate(35.99).evaluate() == DormancyGateVerdict.PASS_ACTIVE

    def test_exactly_36_provisional(self):
        assert DormancyRecoveryGate(36.0).evaluate() == DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY

    # AC2
    def test_46_hours_provisional(self):
        """AC2: 46 hours → PROVISIONAL_DORMANT_RECOVERY."""
        assert DormancyRecoveryGate(46.0).evaluate() == DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY

    def test_just_below_72_provisional(self):
        assert DormancyRecoveryGate(71.99).evaluate() == DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY

    def test_exactly_72_fail(self):
        assert DormancyRecoveryGate(72.0).evaluate() == DormancyGateVerdict.FAIL_DORMANT_ABORT

    # AC1
    def test_75_hours_fail(self):
        """AC1: 75 hours → FAIL_DORMANT_ABORT."""
        assert DormancyRecoveryGate(75.0).evaluate() == DormancyGateVerdict.FAIL_DORMANT_ABORT

    def test_very_large_hours_fail(self):
        assert DormancyRecoveryGate(10000.0).evaluate() == DormancyGateVerdict.FAIL_DORMANT_ABORT

    def test_pass_boundary_just_under_36(self):
        assert DormancyRecoveryGate(DORMANCY_PASS_MAX_HOURS - 0.01).evaluate() == DormancyGateVerdict.PASS_ACTIVE

    def test_fail_boundary_exactly_72(self):
        assert DormancyRecoveryGate(DORMANCY_PROVISIONAL_MAX_HOURS).evaluate() == DormancyGateVerdict.FAIL_DORMANT_ABORT


# ---------------------------------------------------------------------------
# ConversionSequenceRouter Tests
# ---------------------------------------------------------------------------

class TestConversionSequenceRouter:

    @pytest.fixture(autouse=True)
    def _tmp(self, tmp_path):
        self._tmp_dir = str(tmp_path)
        yield
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def _router(self, coach_id: str = "coach-fr53") -> ConversionSequenceRouter:
        return _make_router(self._tmp_dir, coach_id)

    # ── AC1: Hard dormancy abort ─────────────────────────────────────

    def test_ac1_75_hours_raises_fail_dormant_abort(self):
        """AC1: 75 hours → FAIL_DORMANT_ABORT + ValueError, next_payload=null."""
        router = self._router()
        with pytest.raises(ValueError) as exc:
            router.route(**_default_route_kwargs(hours=75.0))
        assert SequenceError.FAIL_DORMANT_ABORT in str(exc.value)

    def test_ac1_abort_means_no_payload_row(self):
        """AC1: Row is NOT returned on abort."""
        router = self._router()
        with pytest.raises(ValueError):
            result = router.route(**_default_route_kwargs(hours=75.0))
        # If we get here the test should have raised — if it didn't, fail
        # (pytest.raises ensures this block is unreachable on success)

    # ── AC2: Provisional recovery pivot ─────────────────────────────

    def test_ac2_46_hours_provisional_row_returned(self):
        """AC2: 46 hours → PROVISIONAL_DORMANT_RECOVERY, row returned."""
        router = self._router()
        row = router.route(**_default_route_kwargs(hours=46.0, spt=2))
        assert row.gate_verdict == DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY

    def test_ac2_provisional_payload_is_recovery_ping(self):
        router = self._router()
        row = router.route(**_default_route_kwargs(hours=46.0))
        assert row.next_payload_string is not None
        assert "RECOVERY PING" in row.next_payload_string

    # ── AC3: Enum integrity on mode assignment ───────────────────────

    def test_ac3_spt_4_affective_attachment(self):
        """AC3: spt_stage=4 → AFFECTIVE_ATTACHMENT in output."""
        router = self._router()
        row = router.route(**_default_route_kwargs(hours=10.0, spt=4))
        assert row.sequence_vulnerability_mode == SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT

    # ── Output schema correctness ────────────────────────────────────

    def test_output_is_payload_row_instance(self):
        router = self._router()
        row = router.route(**_default_route_kwargs())
        assert isinstance(row, ConversionSequencePayloadRow)

    def test_sequence_execution_id_is_uuid(self):
        router = self._router()
        row = router.route(**_default_route_kwargs())
        parsed = uuid.UUID(row.sequence_execution_id)
        assert str(parsed) == row.sequence_execution_id

    def test_execution_timestamp_iso(self):
        from datetime import datetime
        router = self._router()
        row = router.route(**_default_route_kwargs())
        dt = datetime.fromisoformat(row.execution_timestamp)
        assert dt is not None

    def test_coach_id_in_output(self):
        router = self._router(coach_id="coach-scoped")
        row = router.route(**_default_route_kwargs())
        assert row.coach_id == "coach-scoped"

    def test_client_id_in_output(self):
        router = self._router()
        row = router.route(
            client_id="client-abc",
            spt_stage=2,
            hours_since_last_message=10.0,
            current_sequence_step=2,
            next_payload_string="Hello client.",
        )
        assert row.client_id == "client-abc"

    def test_current_step_stored(self):
        router = self._router()
        row = router.route(**{**_default_route_kwargs(), "current_sequence_step": 3})
        assert row.current_sequence_step_integer == 3

    # ── Vulnerability mode in full pipeline ──────────────────────────

    def test_spt_none_produces_objective_mode(self):
        router = self._router()
        row = router.route(**{**_default_route_kwargs(), "spt_stage": None})
        assert row.sequence_vulnerability_mode == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_2_objective_mode(self):
        router = self._router()
        row = router.route(**_default_route_kwargs(spt=2))
        assert row.sequence_vulnerability_mode == SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE

    def test_spt_3_affective_mode(self):
        router = self._router()
        row = router.route(**_default_route_kwargs(spt=3))
        assert row.sequence_vulnerability_mode == SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT

    # ── PASS_ACTIVE payload passthrough ─────────────────────────────

    def test_pass_active_uses_provided_payload(self):
        router = self._router()
        payload = "Day 1 anchor message — unique text."
        row = router.route(
            client_id="c1",
            spt_stage=2,
            hours_since_last_message=10.0,
            current_sequence_step=1,
            next_payload_string=payload,
        )
        assert row.gate_verdict == DormancyGateVerdict.PASS_ACTIVE
        assert row.next_payload_string == payload

    def test_pass_active_none_payload_allowed(self):
        """PASS_ACTIVE with no payload — should store None."""
        router = self._router()
        row = router.route(
            client_id="c1",
            spt_stage=2,
            hours_since_last_message=5.0,
            current_sequence_step=1,
            next_payload_string=None,
        )
        assert row.gate_verdict == DormancyGateVerdict.PASS_ACTIVE
        assert row.next_payload_string is None

    # ── Receipt chain ────────────────────────────────────────────────

    def test_receipt_logged_on_pass(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR3", log_dir=tmp)
            router = ConversionSequenceRouter(coach_id="rc-test-coach", receipt_chain=rc)
            router.route(**_default_route_kwargs(hours=10.0, spt=3))
            vuln_entries = rc.query(action="sequence-vulnerability-resolve")
            assert len(vuln_entries) >= 1
            gate_entries = rc.query(action="sequence-dormancy-gate")
            assert len(gate_entries) >= 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_receipt_logged_on_fail(self):
        """Receipt written before FAIL_DORMANT_ABORT raise."""
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR3", log_dir=tmp)
            router = ConversionSequenceRouter(coach_id="rc-fail-coach", receipt_chain=rc)
            with pytest.raises(ValueError):
                router.route(**_default_route_kwargs(hours=80.0))
            gate_entries = rc.query(action="sequence-dormancy-gate")
            assert len(gate_entries) >= 1
            assert "FAIL_DORMANT_ABORT" in gate_entries[0].output_summary
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_receipt_vuln_resolve_contains_spt_and_mode(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR3", log_dir=tmp)
            router = ConversionSequenceRouter(coach_id="rc-vuln-check", receipt_chain=rc)
            router.route(**_default_route_kwargs(spt=4))
            entries = rc.query(action="sequence-vulnerability-resolve")
            summary = entries[0].output_summary
            assert "spt_stage=4" in summary
            assert "AFFECTIVE_ATTACHMENT" in summary
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ── Constructor guards ────────────────────────────────────────────

    def test_short_coach_id_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR3", log_dir=tmp)
            with pytest.raises(ValueError):
                ConversionSequenceRouter(coach_id="x", receipt_chain=rc)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_empty_coach_id_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR3", log_dir=tmp)
            with pytest.raises(ValueError):
                ConversionSequenceRouter(coach_id="", receipt_chain=rc)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ── ADR-01 isolation ─────────────────────────────────────────────

    def test_two_coaches_produce_different_execution_ids(self):
        router_a = _make_router(self._tmp_dir + "a", "coach-A")
        router_b = _make_router(self._tmp_dir + "b", "coach-B")
        row_a = router_a.route(**_default_route_kwargs())
        row_b = router_b.route(**_default_route_kwargs())
        assert row_a.sequence_execution_id != row_b.sequence_execution_id
        assert row_a.coach_id != row_b.coach_id

    # ── Boundary edges ───────────────────────────────────────────────

    def test_exactly_36_hours_provisional(self):
        router = self._router()
        row = router.route(**_default_route_kwargs(hours=36.0))
        assert row.gate_verdict == DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY

    def test_exactly_72_hours_abort(self):
        router = self._router()
        with pytest.raises(ValueError):
            router.route(**_default_route_kwargs(hours=72.0))

    def test_35_99_hours_pass(self):
        router = self._router()
        row = router.route(**_default_route_kwargs(hours=35.99))
        assert row.gate_verdict == DormancyGateVerdict.PASS_ACTIVE

    # ── Full row field completeness ──────────────────────────────────

    def test_all_required_fields_populated(self):
        router = self._router()
        row = router.route(**_default_route_kwargs(hours=5.0, spt=2))
        assert row.sequence_execution_id
        assert row.client_id
        assert row.coach_id
        assert row.sequence_vulnerability_mode in (
            SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE,
            SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT,
        )
        assert row.gate_verdict
        assert row.current_sequence_step_integer in (1, 2, 3)
        assert row.execution_timestamp
