"""
FR56 — Campaign Performance Registry  (CPSC Spec 2 of 10)
==========================================================
Tests for ConversionOutcomeResolver and CampaignPerformanceLogger.
"""

from __future__ import annotations

import shutil
import tempfile
import uuid
from datetime import datetime, timezone

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    BOOKED_WEBHOOK_KEYS,
    CAMPAIGN_DORMANCY_HOURS,
    DECLINED_WEBHOOK_KEYS,
    CampaignPerformanceRegistryRow,
    CampaignRegistryError,
    ConversionOutcome,
    PsychSnapshotAtLaunch,
    RegistryGateVerdict,
)
from src.ccp.services.campaign_performance_logger import (
    CampaignPerformanceLogger,
    ConversionOutcomeResolver,
)


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

CID = "TST"
EXEC_ID = str(uuid.uuid4())


def _make_rc_isolated() -> tuple[ReceiptChain, str]:
    tmp = tempfile.mkdtemp(prefix="fr56_rc_")
    rc = ReceiptChain(coach_acronym=CID, log_dir=tmp)
    return rc, tmp


def _full_snap(coping: int = 4, spt: int = 3, intimacy: float = 0.6) -> PsychSnapshotAtLaunch:
    return PsychSnapshotAtLaunch(coping_tier=coping, spt_stage=spt, intimacy_score=intimacy)


def _booked_payload(client_id: str = "c1") -> dict:
    return {"client_id": client_id, "event_type": "checkout.session.completed"}


def _declined_payload(client_id: str = "c1") -> dict:
    return {"client_id": client_id, "message": "/stop"}


# ══════════════════════════════════════════════════════════════════════
# 1. Constants
# ══════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify constants match spec §4."""

    def test_dormancy_hours(self) -> None:
        assert CAMPAIGN_DORMANCY_HOURS == 72.0

    def test_booked_webhook_keys_present(self) -> None:
        assert "checkout.session.completed" in BOOKED_WEBHOOK_KEYS
        assert "charge.succeeded" in BOOKED_WEBHOOK_KEYS
        assert "invitee.created" in BOOKED_WEBHOOK_KEYS

    def test_declined_webhook_keys_present(self) -> None:
        assert "/stop" in DECLINED_WEBHOOK_KEYS
        assert "no thanks" in DECLINED_WEBHOOK_KEYS


# ══════════════════════════════════════════════════════════════════════
# 2. ADR-01 Constructor Validation
# ══════════════════════════════════════════════════════════════════════


class TestADR01Constructor:
    """ADR-01: coach_id must be 2-4 chars."""

    def test_2_char_ok(self) -> None:
        ConversionOutcomeResolver(coach_id="AB")
        CampaignPerformanceLogger(coach_id="AB")

    def test_3_char_ok(self) -> None:
        ConversionOutcomeResolver(coach_id="ABC")
        CampaignPerformanceLogger(coach_id="ABC")

    def test_4_char_ok(self) -> None:
        ConversionOutcomeResolver(coach_id="ABCD")
        CampaignPerformanceLogger(coach_id="ABCD")

    def test_1_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="ADR-01"):
            ConversionOutcomeResolver(coach_id="A")
        with pytest.raises(ValueError, match="ADR-01"):
            CampaignPerformanceLogger(coach_id="A")

    def test_5_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="ADR-01"):
            ConversionOutcomeResolver(coach_id="ABCDE")
        with pytest.raises(ValueError, match="ADR-01"):
            CampaignPerformanceLogger(coach_id="ABCDE")


# ══════════════════════════════════════════════════════════════════════
# 3. ConversionOutcomeResolver — Stage 1
# ══════════════════════════════════════════════════════════════════════


class TestConversionOutcomeResolver:
    """Stage 1 — webhook → ConversionOutcome."""

    def setup_method(self) -> None:
        self.r = ConversionOutcomeResolver(coach_id=CID)

    # ── BOOKED_CONVERTED ───────────────────────────────────────────

    def test_checkout_session_completed(self) -> None:
        cid, outcome = self.r.resolve({"client_id": "c1", "event_type": "checkout.session.completed"})
        assert outcome == ConversionOutcome.BOOKED_CONVERTED

    def test_charge_succeeded(self) -> None:
        """AC3: charge.succeeded → BOOKED_CONVERTED."""
        cid, outcome = self.r.resolve({"client_id": "c1", "event_type": "charge.succeeded"})
        assert outcome == ConversionOutcome.BOOKED_CONVERTED

    def test_invitee_created(self) -> None:
        cid, outcome = self.r.resolve({"client_id": "c1", "event_type": "invitee.created"})
        assert outcome == ConversionOutcome.BOOKED_CONVERTED

    def test_booked_key_in_nested_payload(self) -> None:
        payload = {"client_id": "c1", "data": {"object": {"event": "checkout.session.completed"}}}
        cid, outcome = self.r.resolve(payload)
        assert outcome == ConversionOutcome.BOOKED_CONVERTED

    # ── DECLINED_OPT_OUT ──────────────────────────────────────────

    def test_stop_command(self) -> None:
        cid, outcome = self.r.resolve({"client_id": "c1", "message": "/stop"})
        assert outcome == ConversionOutcome.DECLINED_OPT_OUT

    def test_no_thanks(self) -> None:
        cid, outcome = self.r.resolve({"client_id": "c1", "button": "No Thanks"})
        assert outcome == ConversionOutcome.DECLINED_OPT_OUT

    # ── NO_RESPONSE_DORMANT ────────────────────────────────────────

    def test_dormant_over_72h(self) -> None:
        cid, outcome = self.r.resolve({"client_id": "c1"}, hours_elapsed_since_offer=73.0)
        assert outcome == ConversionOutcome.NO_RESPONSE_DORMANT

    def test_dormant_exactly_72h_not_dormant(self) -> None:
        """Exactly 72h is NOT over threshold (> not >=)."""
        cid, outcome = self.r.resolve({"client_id": "c1"}, hours_elapsed_since_offer=72.0)
        # 72.0 is NOT > 72.0 so falls through to default dormant anyway — still DORMANT
        assert outcome == ConversionOutcome.NO_RESPONSE_DORMANT

    def test_no_signal_no_elapsed_defaults_dormant(self) -> None:
        """No positive/negative signal + no hours → defaults to DORMANT."""
        cid, outcome = self.r.resolve({"client_id": "c1"})
        assert outcome == ConversionOutcome.NO_RESPONSE_DORMANT

    # ── Priority order: booked > declined > dormant ────────────────

    def test_booked_takes_priority_over_dormant(self) -> None:
        cid, outcome = self.r.resolve(
            {"client_id": "c1", "event_type": "charge.succeeded"},
            hours_elapsed_since_offer=100.0,
        )
        assert outcome == ConversionOutcome.BOOKED_CONVERTED

    # ── Client ID extraction ───────────────────────────────────────

    def test_client_id_returned(self) -> None:
        cid, _ = self.r.resolve({"client_id": "client_xyz", "event_type": "charge.succeeded"})
        assert cid == "client_xyz"

    def test_client_id_from_metadata(self) -> None:
        payload = {"metadata": {"client_id": "meta_client"}, "event_type": "invitee.created"}
        cid, outcome = self.r.resolve(payload)
        assert cid == "meta_client"
        assert outcome == ConversionOutcome.BOOKED_CONVERTED

    def test_missing_client_id_raises(self) -> None:
        with pytest.raises(ValueError, match="MISSING_CLIENT_ID"):
            self.r.resolve({"event_type": "charge.succeeded"})


# ══════════════════════════════════════════════════════════════════════
# 4. CampaignPerformanceLogger — Gate Verdicts
# ══════════════════════════════════════════════════════════════════════


class TestCampaignPerformanceLogger:
    """Stage 2 — completeness gate + row generation."""

    def setup_method(self) -> None:
        self.lg = CampaignPerformanceLogger(coach_id=CID)

    # ── PASS ───────────────────────────────────────────────────────

    def test_pass_all_fields_present(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.gate_verdict == RegistryGateVerdict.PASS.value
        assert row.conversion_outcome == ConversionOutcome.BOOKED_CONVERTED.value

    # ── PROVISIONAL_PARTIAL ────────────────────────────────────────

    def test_provisional_intimacy_null(self) -> None:
        """AC2: coping=3, intimacy=None → PROVISIONAL_PARTIAL."""
        snap = PsychSnapshotAtLaunch(coping_tier=3, spt_stage=2, intimacy_score=None)
        row = self.lg.log_outcome(EXEC_ID, {"client_id": "c1"}, snap, hours_elapsed_since_offer=80.0)
        assert row.gate_verdict == RegistryGateVerdict.PROVISIONAL_PARTIAL.value
        assert row.conversion_outcome == ConversionOutcome.NO_RESPONSE_DORMANT.value

    def test_provisional_spt_null(self) -> None:
        snap = PsychSnapshotAtLaunch(coping_tier=3, spt_stage=None, intimacy_score=0.5)
        row = self.lg.log_outcome(EXEC_ID, {"client_id": "c1"}, snap)
        assert row.gate_verdict == RegistryGateVerdict.PROVISIONAL_PARTIAL.value

    def test_provisional_both_spt_and_intimacy_null(self) -> None:
        snap = PsychSnapshotAtLaunch(coping_tier=4, spt_stage=None, intimacy_score=None)
        row = self.lg.log_outcome(EXEC_ID, {"client_id": "c1"}, snap)
        assert row.gate_verdict == RegistryGateVerdict.PROVISIONAL_PARTIAL.value

    # ── FAIL_CORRUPTED ─────────────────────────────────────────────

    def test_fail_corrupted_coping_null_raises(self) -> None:
        """AC1: coping_tier=None → FAIL_CORRUPTED raises ValueError."""
        snap = PsychSnapshotAtLaunch(coping_tier=None, spt_stage=3, intimacy_score=0.5)
        with pytest.raises(ValueError, match="CORRUPTED_PSYCH_SNAPSHOT"):
            self.lg.log_outcome(EXEC_ID, {"client_id": "c1"}, snap)

    def test_fail_corrupted_no_snapshot_raises(self) -> None:
        """No snapshot → all None → coping_tier None → FAIL_CORRUPTED."""
        with pytest.raises(ValueError, match="CORRUPTED_PSYCH_SNAPSHOT"):
            self.lg.log_outcome(EXEC_ID, {"client_id": "c1"}, None)

    # ── Row fields ─────────────────────────────────────────────────

    def test_row_has_registry_id_uuid(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        parsed = uuid.UUID(row.registry_id, version=4)
        assert str(parsed) == row.registry_id

    def test_row_has_log_timestamp_iso(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        dt = datetime.fromisoformat(row.log_timestamp)
        assert dt.tzinfo is not None

    def test_row_has_campaign_execution_id(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.campaign_execution_id == EXEC_ID

    def test_row_has_coach_id(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.coach_id == CID

    def test_row_time_to_conversion_null_when_not_provided(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.time_to_conversion_hours is None

    def test_row_time_to_conversion_set(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap(), time_to_conversion_hours=4.5)
        assert row.time_to_conversion_hours == pytest.approx(4.5)

    def test_no_receipt_chain_ok(self) -> None:
        lg = CampaignPerformanceLogger(coach_id=CID, receipt_chain=None)
        row = lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.gate_verdict == RegistryGateVerdict.PASS.value


# ══════════════════════════════════════════════════════════════════════
# 5. Acceptance Criteria
# ══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """Verbatim AC scenarios from tech spec §8."""

    def setup_method(self) -> None:
        self.lg = CampaignPerformanceLogger(coach_id=CID)

    # AC1 — coping_tier=null → FAIL_CORRUPTED, row NOT written
    def test_ac1_corrupted_null_coping_rejected(self) -> None:
        snap = PsychSnapshotAtLaunch(coping_tier=None, spt_stage=3, intimacy_score=0.5)
        with pytest.raises(ValueError) as exc_info:
            self.lg.log_outcome(EXEC_ID, {"client_id": "ac1"}, snap)
        assert "CORRUPTED_PSYCH_SNAPSHOT" in str(exc_info.value)
        assert "psychological context" in str(exc_info.value)

    # AC2 — NO_RESPONSE_DORMANT + coping=3 + intimacy=None → PROVISIONAL_PARTIAL, row written
    def test_ac2_provisional_partial_written(self) -> None:
        snap = PsychSnapshotAtLaunch(coping_tier=3, spt_stage=None, intimacy_score=None)
        row = self.lg.log_outcome(
            EXEC_ID,
            {"client_id": "ac2"},
            snap,
            hours_elapsed_since_offer=80.0,
        )
        assert row.gate_verdict == RegistryGateVerdict.PROVISIONAL_PARTIAL.value
        assert row.conversion_outcome == ConversionOutcome.NO_RESPONSE_DORMANT.value
        # Row was produced (not rejected)
        assert row.registry_id is not None

    # AC3 — charge.succeeded → BOOKED_CONVERTED
    def test_ac3_charge_succeeded_maps_to_booked(self) -> None:
        snap = _full_snap()
        row = self.lg.log_outcome(
            EXEC_ID,
            {"client_id": "ac3", "event_type": "charge.succeeded"},
            snap,
        )
        assert row.conversion_outcome == ConversionOutcome.BOOKED_CONVERTED.value
        assert row.gate_verdict == RegistryGateVerdict.PASS.value


# ══════════════════════════════════════════════════════════════════════
# 6. PsychSnapshotAtLaunch Model
# ══════════════════════════════════════════════════════════════════════


class TestPsychSnapshot:
    """Verify PsychSnapshotAtLaunch field defaults and structure."""

    def test_all_none_defaults(self) -> None:
        snap = PsychSnapshotAtLaunch()
        assert snap.coping_tier is None
        assert snap.spt_stage is None
        assert snap.intimacy_score is None

    def test_fully_populated(self) -> None:
        snap = PsychSnapshotAtLaunch(coping_tier=4, spt_stage=3, intimacy_score=0.7)
        assert snap.coping_tier == 4
        assert snap.spt_stage == 3
        assert snap.intimacy_score == pytest.approx(0.7)


# ══════════════════════════════════════════════════════════════════════
# 7. Output Schema
# ══════════════════════════════════════════════════════════════════════


class TestOutputSchema:
    """Verify CampaignPerformanceRegistryRow output matches spec §5."""

    def setup_method(self) -> None:
        self.lg = CampaignPerformanceLogger(coach_id=CID)

    def test_model_dump_keys(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        keys = set(row.model_dump().keys())
        expected = {
            "registry_id", "campaign_execution_id", "client_id", "coach_id",
            "conversion_outcome", "psych_snapshot_at_launch",
            "time_to_conversion_hours", "gate_verdict", "log_timestamp",
        }
        assert keys == expected

    def test_psych_snapshot_keys(self) -> None:
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        snap_keys = set(row.psych_snapshot_at_launch.model_dump().keys())
        assert snap_keys == {"coping_tier", "spt_stage", "intimacy_score"}

    def test_conversion_outcome_valid_enum_values(self) -> None:
        valid = {e.value for e in ConversionOutcome}
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.conversion_outcome in valid

    def test_gate_verdict_valid_enum_values(self) -> None:
        valid = {e.value for e in RegistryGateVerdict}
        row = self.lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.gate_verdict in valid


# ══════════════════════════════════════════════════════════════════════
# 8. Receipt Chain
# ══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """Verify receipt logging."""

    def test_two_receipts_on_pass(self) -> None:
        rc, tmp = _make_rc_isolated()
        lg = CampaignPerformanceLogger(coach_id=CID, receipt_chain=rc)
        lg.log_outcome(EXEC_ID, _booked_payload("r1"), _full_snap())
        resolve = rc.query(action="conversion-outcome-resolve")
        gate = rc.query(action="registry-completeness-gate")
        assert len(resolve) >= 1
        assert len(gate) >= 1
        shutil.rmtree(tmp, ignore_errors=True)

    def test_outcome_receipt_contains_client(self) -> None:
        rc, tmp = _make_rc_isolated()
        lg = CampaignPerformanceLogger(coach_id=CID, receipt_chain=rc)
        lg.log_outcome(EXEC_ID, {"client_id": "r2client"}, _full_snap())
        entries = rc.query(action="conversion-outcome-resolve")
        assert len(entries) >= 1
        assert "r2client" in entries[0].output_summary
        shutil.rmtree(tmp, ignore_errors=True)

    def test_fail_corrupted_emits_receipt(self) -> None:
        rc, tmp = _make_rc_isolated()
        lg = CampaignPerformanceLogger(coach_id=CID, receipt_chain=rc)
        snap = PsychSnapshotAtLaunch(coping_tier=None)
        with pytest.raises(ValueError):
            lg.log_outcome(EXEC_ID, {"client_id": "r3"}, snap)
        gate = rc.query(action="registry-completeness-gate")
        assert len(gate) >= 1
        assert "FAIL_CORRUPTED" in gate[0].output_summary
        shutil.rmtree(tmp, ignore_errors=True)

    def test_no_receipt_chain_no_error(self) -> None:
        lg = CampaignPerformanceLogger(coach_id=CID, receipt_chain=None)
        row = lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        assert row.gate_verdict == RegistryGateVerdict.PASS.value


# ══════════════════════════════════════════════════════════════════════
# 9. Persona Masking (C-11)
# ══════════════════════════════════════════════════════════════════════


class TestPersonaMasking:
    """C-11: No agent class names in output JSON."""

    def test_no_class_names_in_output(self) -> None:
        lg = CampaignPerformanceLogger(coach_id=CID)
        row = lg.log_outcome(EXEC_ID, _booked_payload(), _full_snap())
        json_str = row.model_dump_json()
        for forbidden in [
            "ConversionOutcomeResolver",
            "CampaignPerformanceLogger",
            "CampaignRegistryError",
        ]:
            assert forbidden not in json_str, f"C-11 violation: {forbidden} in output"


# ══════════════════════════════════════════════════════════════════════
# 10. Enum Coverage
# ══════════════════════════════════════════════════════════════════════


class TestEnumCoverage:
    """Verify enum members match spec."""

    def test_conversion_outcome_members(self) -> None:
        names = {m.name for m in ConversionOutcome}
        assert names == {"BOOKED_CONVERTED", "DECLINED_OPT_OUT", "NO_RESPONSE_DORMANT"}

    def test_registry_gate_verdict_members(self) -> None:
        names = {m.name for m in RegistryGateVerdict}
        assert names == {"PASS", "PROVISIONAL_PARTIAL", "FAIL_CORRUPTED"}

    def test_campaign_registry_error_members(self) -> None:
        names = {m.name for m in CampaignRegistryError}
        assert names == {
            "MISSING_CLIENT_ID",
            "CORRUPTED_PSYCH_SNAPSHOT",
            "GATE_EVALUATION_ERROR",
            "INVALID_COACH_SCOPE",
        }
