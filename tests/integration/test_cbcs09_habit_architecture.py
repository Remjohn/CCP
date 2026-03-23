"""
FR-CBCS-09 — Habit Architecture Module — Integration Tests
============================================================
Tests for ImplementationIntentionParser, HabitAbandonmentChecker,
covering all 3 ACs plus edge cases.
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timezone, timedelta

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    HABIT_ABANDONMENT_DAYS,
    HabitArchitectureError,
    HabitArchitectureTrackerRow,
    HabitStatus,
    HabitVerificationVerdict,
)
from src.ccp.services.habit_architecture import (
    HabitAbandonmentChecker,
    ImplementationIntentionParser,
)


# ── Helpers ────────────────────────────────────────────────────────────

def _make_parser(coach: str = "TST") -> tuple[ImplementationIntentionParser, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    parser = ImplementationIntentionParser(coach_acronym=coach, receipt_chain=rc)
    return parser, rc


def _make_checker(coach: str = "TST") -> tuple[HabitAbandonmentChecker, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    chk = HabitAbandonmentChecker(coach_acronym=coach, receipt_chain=rc)
    return chk, rc


def _make_row(
    status: str = "VERIFIED",
    days_ago: int = 0,
) -> HabitArchitectureTrackerRow:
    """Create a tracker row with last_checked_date *days_ago* days in the past."""
    checked = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return HabitArchitectureTrackerRow(
        tracker_id="test-tracker-001",
        client_id="client-001",
        coach_id="TST",
        environmental_cue="I wake up",
        concrete_action="drink a glass of water",
        habit_status=status,
        verification_verdict=HabitVerificationVerdict.PASS.value,
        last_checked_date=checked.isoformat(),
    )


# ════════════════════════════════════════════════════════════════════════
# 1. Constructor & ADR-01
# ════════════════════════════════════════════════════════════════════════

class TestConstructor:
    """ADR-01 coach scope enforcement."""

    def test_valid_coach_2_char(self) -> None:
        p, _ = _make_parser("TS")
        assert p is not None

    def test_valid_coach_4_char(self) -> None:
        p, _ = _make_parser("TEST")
        assert p is not None

    def test_invalid_coach_1_char_parser(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_parser("T")

    def test_invalid_coach_5_char_parser(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_parser("TESTI")

    def test_invalid_coach_1_char_checker(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_checker("T")

    def test_invalid_coach_5_char_checker(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_checker("TESTI")


# ════════════════════════════════════════════════════════════════════════
# 2. Static Parsing (Stage 1 + 2)
# ════════════════════════════════════════════════════════════════════════

class TestIfThenSyntax:
    """If/When … Then/I will detection."""

    def test_classic_if_then(self) -> None:
        assert ImplementationIntentionParser.detect_if_then_syntax(
            "If it is 8 AM, then I will run for 20 minutes."
        ) is True

    def test_when_i_will(self) -> None:
        assert ImplementationIntentionParser.detect_if_then_syntax(
            "When I wake up, I will drink a glass of water."
        ) is True

    def test_when_im_going_to(self) -> None:
        assert ImplementationIntentionParser.detect_if_then_syntax(
            "When I get home, I'm going to write in my journal."
        ) is True

    def test_no_syntax(self) -> None:
        assert ImplementationIntentionParser.detect_if_then_syntax(
            "I will go to the gym tomorrow"
        ) is False

    def test_empty_string(self) -> None:
        assert ImplementationIntentionParser.detect_if_then_syntax("") is False


class TestComponentExtraction:
    """Environmental cue and concrete action extraction."""

    def test_extract_if_then(self) -> None:
        cue, action = ImplementationIntentionParser.extract_components(
            "If it is 8 AM, then I will run for 20 minutes."
        )
        assert cue is not None
        assert "8 AM" in cue
        assert action is not None
        assert "run" in action.lower()

    def test_extract_when_i_will(self) -> None:
        cue, action = ImplementationIntentionParser.extract_components(
            "When I wake up, I will drink a glass of water."
        )
        assert cue is not None
        assert "wake up" in cue.lower()
        assert action is not None
        assert "drink" in action.lower()

    def test_no_match_returns_none(self) -> None:
        cue, action = ImplementationIntentionParser.extract_components(
            "I want to exercise more."
        )
        assert cue is None
        assert action is None


class TestConcreteAction:
    """Concrete vs abstract verb detection."""

    def test_concrete_drink(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("drink a glass of water") is True

    def test_concrete_run(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("run for 20 minutes") is True

    def test_concrete_write(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("write in my journal") is True

    def test_abstract_focus(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("focus") is False

    def test_abstract_be_better(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("be better") is False

    def test_abstract_feel_good(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("feel good") is False

    def test_none_action(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action(None) is False

    def test_empty_action(self) -> None:
        assert ImplementationIntentionParser.is_concrete_action("") is False


# ════════════════════════════════════════════════════════════════════════
# 3. Full Verification Gate (Stage 3)
# ════════════════════════════════════════════════════════════════════════

class TestVerifyPass:
    """PASS — both If/Then syntax and concrete action present."""

    def test_full_pass(self) -> None:
        parser, rc = _make_parser()
        row = parser.parse_and_verify(
            "client-001",
            "If it is 8 AM, then I will run for 20 minutes.",
        )
        assert row.verification_verdict == HabitVerificationVerdict.PASS.value
        assert row.habit_status == HabitStatus.VERIFIED.value
        assert row.environmental_cue is not None
        assert row.concrete_action is not None

    def test_pass_receipt_logged(self) -> None:
        parser, rc = _make_parser()
        parser.parse_and_verify("c1", "When I wake up, I will drink water.")
        entries = rc.query(action="habit-intention-parse")
        assert len(entries) == 1
        assert entries[0].decision == "PASS"


class TestVerifyFail:
    """FAIL — no If/Then syntax found."""

    def test_ac1_no_if_then_syntax(self) -> None:
        """AC1: 'I will go to the gym tomorrow' → if_then_syntax_found=False → FAIL → FORMING."""
        parser, _ = _make_parser()
        row = parser.parse_and_verify(
            "client-001",
            "I will go to the gym tomorrow",
        )
        assert row.verification_verdict == HabitVerificationVerdict.FAIL.value
        assert row.habit_status == HabitStatus.FORMING.value
        assert row.environmental_cue is None
        assert row.concrete_action is None

    def test_fail_receipt_logged(self) -> None:
        parser, rc = _make_parser()
        parser.parse_and_verify("c1", "I want to exercise more.")
        entries = rc.query(action="habit-intention-parse")
        assert len(entries) == 1
        assert entries[0].decision == "FAIL"


class TestVerifyProvisional:
    """PROVISIONAL — If/Then present but action is abstract."""

    def test_ac2_abstract_verb_provisional(self) -> None:
        """AC2: 'When I wake up, then I will focus.' → abstract verb → PROVISIONAL."""
        parser, _ = _make_parser()
        row = parser.parse_and_verify(
            "client-001",
            "When I wake up, then I will focus.",
        )
        assert row.verification_verdict == HabitVerificationVerdict.PROVISIONAL.value
        assert row.habit_status == HabitStatus.FORMING.value
        assert row.environmental_cue is not None
        assert row.concrete_action is None  # Abstract action not stored

    def test_provisional_be_better(self) -> None:
        parser, _ = _make_parser()
        row = parser.parse_and_verify(
            "client-001",
            "If I feel sad, then I will be better.",
        )
        assert row.verification_verdict == HabitVerificationVerdict.PROVISIONAL.value
        assert row.habit_status == HabitStatus.FORMING.value

    def test_provisional_receipt_logged(self) -> None:
        parser, rc = _make_parser()
        parser.parse_and_verify("c1", "When I wake up, then I will focus.")
        entries = rc.query(action="habit-intention-parse")
        assert len(entries) == 1
        assert entries[0].decision == "PROVISIONAL"


class TestEmptyMessage:
    """Empty/whitespace message → FAIL + FORMING."""

    def test_empty_string(self) -> None:
        parser, _ = _make_parser()
        row = parser.parse_and_verify("c1", "")
        assert row.verification_verdict == HabitVerificationVerdict.FAIL.value
        assert row.habit_status == HabitStatus.FORMING.value

    def test_whitespace_only(self) -> None:
        parser, _ = _make_parser()
        row = parser.parse_and_verify("c1", "   \n  ")
        assert row.verification_verdict == HabitVerificationVerdict.FAIL.value
        assert row.habit_status == HabitStatus.FORMING.value


# ════════════════════════════════════════════════════════════════════════
# 4. Broken Habit Detection (Stage 4)
# ════════════════════════════════════════════════════════════════════════

class TestBrokenReport:
    """Client self-reports habit failure."""

    def test_missed_habit_broken(self) -> None:
        parser, rc = _make_parser()
        existing = _make_row(status="VERIFIED")
        updated = parser.check_broken_report("c1", "I missed my habit this week.", existing)
        assert updated.habit_status == HabitStatus.BROKEN.value

    def test_didnt_do_it_broken(self) -> None:
        parser, _ = _make_parser()
        existing = _make_row(status="VERIFIED")
        updated = parser.check_broken_report("c1", "I didn't do it today.", existing)
        assert updated.habit_status == HabitStatus.BROKEN.value

    def test_no_broken_signal_unchanged(self) -> None:
        parser, _ = _make_parser()
        existing = _make_row(status="VERIFIED")
        updated = parser.check_broken_report("c1", "I had a great day!", existing)
        assert updated.habit_status == HabitStatus.VERIFIED.value

    def test_broken_receipt_logged(self) -> None:
        parser, rc = _make_parser()
        existing = _make_row(status="VERIFIED")
        parser.check_broken_report("c1", "I missed my habit.", existing)
        entries = rc.query(action="habit-broken-detected")
        assert len(entries) == 1
        assert entries[0].decision == "BROKEN"


# ════════════════════════════════════════════════════════════════════════
# 5. Abandonment Auto-Prune (Stage 4 — Cron)
# ════════════════════════════════════════════════════════════════════════

class TestAbandonmentChecker:
    """Auto-prune stale habits after 14 days."""

    def test_ac3_15_days_abandoned(self) -> None:
        """AC3: last_checked=15 days ago, status=VERIFIED → ABANDONED."""
        checker, _ = _make_checker()
        row = _make_row(status="VERIFIED", days_ago=15)
        updated = checker.check_abandonment(row)
        assert updated.habit_status == HabitStatus.ABANDONED.value

    def test_exactly_14_days_not_abandoned(self) -> None:
        """14 days is the threshold — NOT exceeded (> 14 required)."""
        checker, _ = _make_checker()
        row = _make_row(status="VERIFIED", days_ago=14)
        updated = checker.check_abandonment(row)
        assert updated.habit_status == HabitStatus.VERIFIED.value

    def test_13_days_not_abandoned(self) -> None:
        checker, _ = _make_checker()
        row = _make_row(status="VERIFIED", days_ago=13)
        updated = checker.check_abandonment(row)
        assert updated.habit_status == HabitStatus.VERIFIED.value

    def test_30_days_abandoned(self) -> None:
        checker, _ = _make_checker()
        row = _make_row(status="VERIFIED", days_ago=30)
        updated = checker.check_abandonment(row)
        assert updated.habit_status == HabitStatus.ABANDONED.value

    def test_already_abandoned_unchanged(self) -> None:
        checker, _ = _make_checker()
        row = _make_row(status="ABANDONED", days_ago=30)
        updated = checker.check_abandonment(row)
        assert updated.habit_status == HabitStatus.ABANDONED.value

    def test_forming_stale_abandoned(self) -> None:
        checker, _ = _make_checker()
        row = _make_row(status="FORMING", days_ago=20)
        updated = checker.check_abandonment(row)
        assert updated.habit_status == HabitStatus.ABANDONED.value

    def test_abandonment_receipt_logged(self) -> None:
        checker, rc = _make_checker()
        row = _make_row(status="VERIFIED", days_ago=15)
        checker.check_abandonment(row)
        entries = rc.query(action="habit-auto-abandon")
        assert len(entries) == 1
        assert entries[0].decision == "ABANDONED"

    def test_reference_time_override(self) -> None:
        """Test with explicit reference time."""
        checker, _ = _make_checker()
        # Row checked 10 days ago from now
        row = _make_row(status="VERIFIED", days_ago=10)
        # But reference time is 20 days in the future → 30 days gap
        future_ref = datetime.now(timezone.utc) + timedelta(days=20)
        updated = checker.check_abandonment(row, reference_time=future_ref)
        assert updated.habit_status == HabitStatus.ABANDONED.value


# ════════════════════════════════════════════════════════════════════════
# 6. Output Schema Integrity
# ════════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    """Verify output field resolution (§4 Stage 4)."""

    def test_tracker_id_is_uuid(self) -> None:
        parser, _ = _make_parser()
        row = parser.parse_and_verify("c1", "If I wake up, then I will run.")
        import uuid
        uuid.UUID(row.tracker_id)  # raises if invalid

    def test_last_checked_date_iso8601(self) -> None:
        parser, _ = _make_parser()
        row = parser.parse_and_verify("c1", "If I wake up, then I will run.")
        datetime.fromisoformat(row.last_checked_date)

    def test_coach_id_matches_constructor(self) -> None:
        parser, _ = _make_parser("TST")
        row = parser.parse_and_verify("c1", "Hello world")
        assert row.coach_id == "TST"


# ════════════════════════════════════════════════════════════════════════
# 7. C-11 Persona Masking
# ════════════════════════════════════════════════════════════════════════

class TestPersonaMasking:
    """Agent names must NOT leak into external payloads."""

    def test_no_agent_name_in_result(self) -> None:
        parser, _ = _make_parser()
        row = parser.parse_and_verify("c1", "If I wake up, then I will run.")
        dump = row.model_dump_json()
        assert "implementation-intention-parser" not in dump
        assert "habit-abandonment-checker" not in dump
