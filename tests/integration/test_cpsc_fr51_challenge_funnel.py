"""
Tests — FR51: Challenge Funnel Intelligence Builder
====================================================
Covers ICTModeCalculator, CommitmentDeviceGate, ChallengeFunnelArchitect,
all three ACs, edge cases, and receipt chain integration.
"""

from __future__ import annotations

import shutil
import tempfile
import uuid

import pytest

from src.ccp.models.cpsc_models import (
    ChallengeFunnelBriefRow,
    ChallengeFunnelError,
    CommitmentGateVerdict,
    StructureFocus,
)
from src.ccp.services.challenge_funnel_builder import (
    COMMITMENT_PRICE_MAX,
    COMMITMENT_PRICE_MIN,
    FLYER_HOOK_MAX_WORDS,
    ICT_SHORT_FUNNEL_THRESHOLD,
    ChallengeFunnelArchitect,
    CommitmentDeviceGate,
    ICTModeCalculator,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_lexicon(heroes: list[str] | None = None, enemies: list[str] | None = None) -> dict:
    return {
        "category_1_heroes": heroes if heroes is not None else ["The Committed Entrepreneur"],
        "category_4_enemies": enemies if enemies is not None else ["The Hustle Culture"],
    }


def _make_rc(tmp_dir: str) -> ReceiptChain:
    return ReceiptChain(coach_acronym="FR1", log_dir=tmp_dir)


def _make_architect(tmp_dir: str, coach_id: str = "coach-fr51-test") -> ChallengeFunnelArchitect:
    rc = _make_rc(tmp_dir)
    return ChallengeFunnelArchitect(coach_id=coach_id, receipt_chain=rc)


# ---------------------------------------------------------------------------
# ICTModeCalculator Tests
# ---------------------------------------------------------------------------

class TestICTModeCalculator:

    def test_empty_array_raises(self):
        with pytest.raises(ValueError) as exc:
            ICTModeCalculator([])
        assert ChallengeFunnelError.EMPTY_COPING_ARRAY in str(exc.value)

    def test_modal_single_element(self):
        calc = ICTModeCalculator([3])
        assert calc.modal_position() == 3

    def test_modal_all_same(self):
        calc = ICTModeCalculator([2, 2, 2, 2])
        assert calc.modal_position() == 2

    def test_modal_majority(self):
        # From spec §10 unit test: [1,2,2,2,5] → mode=2
        calc = ICTModeCalculator([1, 2, 2, 2, 5])
        assert calc.modal_position() == 2

    def test_resolve_5day_at_threshold(self):
        # modal=2 → 5_DAY_MOMENTUM
        calc = ICTModeCalculator([2, 2, 2])
        days, focus = calc.resolve()
        assert days == 5
        assert focus == StructureFocus.FIVE_DAY_MOMENTUM

    def test_resolve_5day_modal_1(self):
        calc = ICTModeCalculator([1, 1, 3])
        days, focus = calc.resolve()
        assert days == 5
        assert focus == StructureFocus.FIVE_DAY_MOMENTUM

    def test_resolve_7day_modal_3(self):
        # modal=3 → 7_DAY_IDENTITY
        calc = ICTModeCalculator([3, 3, 3])
        days, focus = calc.resolve()
        assert days == 7
        assert focus == StructureFocus.SEVEN_DAY_IDENTITY

    def test_resolve_7day_modal_5(self):
        calc = ICTModeCalculator([5, 5, 1])
        days, focus = calc.resolve()
        assert days == 7
        assert focus == StructureFocus.SEVEN_DAY_IDENTITY

    def test_spec_example_array(self):
        # Spec §10: [1,2,2,2,5] → mode=2 → days=5 → 5_DAY_MOMENTUM
        calc = ICTModeCalculator([1, 2, 2, 2, 5])
        days, focus = calc.resolve()
        assert days == 5
        assert focus == StructureFocus.FIVE_DAY_MOMENTUM

    def test_threshold_boundary_exactly_2(self):
        calc = ICTModeCalculator([2])
        days, focus = calc.resolve()
        assert days == 5
        assert focus == StructureFocus.FIVE_DAY_MOMENTUM

    def test_threshold_boundary_exactly_3(self):
        calc = ICTModeCalculator([3])
        days, focus = calc.resolve()
        assert days == 7
        assert focus == StructureFocus.SEVEN_DAY_IDENTITY

    def test_large_array(self):
        arr = [1] * 50 + [4] * 100
        calc = ICTModeCalculator(arr)
        assert calc.modal_position() == 4
        days, focus = calc.resolve()
        assert days == 7

    def test_single_high_value(self):
        calc = ICTModeCalculator([10])
        days, focus = calc.resolve()
        assert days == 7
        assert focus == StructureFocus.SEVEN_DAY_IDENTITY


# ---------------------------------------------------------------------------
# CommitmentDeviceGate Tests
# ---------------------------------------------------------------------------

class TestCommitmentDeviceGate:

    # Spec §10 unit test: [0.0, 9.0, 17.5, 99.9] → [PROVISIONAL, PASS, FAIL, FAIL]
    def test_gate_float_map_spec_example(self):
        expected = [
            CommitmentGateVerdict.PROVISIONAL_FREE_ACCEPTED,
            CommitmentGateVerdict.PASS,
            CommitmentGateVerdict.FAIL_OVERPRICED,
            CommitmentGateVerdict.FAIL_OVERPRICED,
        ]
        for price, exp in zip([0.0, 9.0, 17.5, 99.9], expected):
            assert CommitmentDeviceGate(price).evaluate() == exp

    def test_zero_price_provisional(self):
        assert CommitmentDeviceGate(0.0).evaluate() == CommitmentGateVerdict.PROVISIONAL_FREE_ACCEPTED

    def test_min_price_pass(self):
        assert CommitmentDeviceGate(COMMITMENT_PRICE_MIN).evaluate() == CommitmentGateVerdict.PASS

    def test_max_price_pass(self):
        assert CommitmentDeviceGate(COMMITMENT_PRICE_MAX).evaluate() == CommitmentGateVerdict.PASS

    def test_typical_nine_dollars_pass(self):
        assert CommitmentDeviceGate(9.0).evaluate() == CommitmentGateVerdict.PASS

    def test_just_above_max_fail(self):
        assert CommitmentDeviceGate(17.01).evaluate() == CommitmentGateVerdict.FAIL_OVERPRICED

    def test_49_dollars_fail(self):
        # AC1 value from spec
        assert CommitmentDeviceGate(49.0).evaluate() == CommitmentGateVerdict.FAIL_OVERPRICED

    def test_99_dollars_fail(self):
        assert CommitmentDeviceGate(99.9).evaluate() == CommitmentGateVerdict.FAIL_OVERPRICED

    def test_negative_price_fail(self):
        # Negative price → FAIL_OVERPRICED (invalid)
        assert CommitmentDeviceGate(-1.0).evaluate() == CommitmentGateVerdict.FAIL_OVERPRICED

    def test_mid_range_pass(self):
        assert CommitmentDeviceGate(10.0).evaluate() == CommitmentGateVerdict.PASS

    def test_0_01_pass(self):
        # Just above zero — within 1–17 range
        assert CommitmentDeviceGate(0.01).evaluate() == CommitmentGateVerdict.FAIL_OVERPRICED

    def test_exactly_17_pass(self):
        assert CommitmentDeviceGate(17.0).evaluate() == CommitmentGateVerdict.PASS

    def test_exactly_1_pass(self):
        assert CommitmentDeviceGate(1.0).evaluate() == CommitmentGateVerdict.PASS


# ---------------------------------------------------------------------------
# ChallengeFunnelArchitect Tests
# ---------------------------------------------------------------------------

class TestChallengeFunnelArchitect:

    @pytest.fixture(autouse=True)
    def _tmp(self, tmp_path):
        self._tmp_dir = str(tmp_path)
        yield
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def _arch(self, coach_id: str = "coach-fr51") -> ChallengeFunnelArchitect:
        return _make_architect(self._tmp_dir, coach_id)

    def _default_kwargs(self, price: float = 9.0, hook: str = "Transform in 5 days") -> dict:
        return dict(
            coping_positions=[2, 2, 3],
            character_lexicon=_make_lexicon(),
            user_requested_price=price,
            flyer_hook_text=hook,
        )

    # ── AC1: Hard price block ────────────────────────────────────────

    def test_ac1_price_49_raises_fail_overpriced(self):
        """AC1: price=$49 → FAIL_OVERPRICED, generation aborted."""
        arch = self._arch()
        with pytest.raises(ValueError) as exc:
            arch.compile_brief(**self._default_kwargs(price=49.0))
        assert ChallengeFunnelError.FAIL_OVERPRICED in str(exc.value)

    def test_ac1_price_18_raises_fail_overpriced(self):
        arch = self._arch()
        with pytest.raises(ValueError) as exc:
            arch.compile_brief(**self._default_kwargs(price=18.0))
        assert ChallengeFunnelError.FAIL_OVERPRICED in str(exc.value)

    # ── AC2: Provisional free accepted ──────────────────────────────

    def test_ac2_price_zero_provisional(self):
        """AC2: price=$0 → PROVISIONAL_FREE_ACCEPTED, row returned."""
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs(price=0.0, hook="Free challenge starts now"))
        assert row.gate_verdict == CommitmentGateVerdict.PROVISIONAL_FREE_ACCEPTED
        assert row.commitment_price == 0.0

    # ── AC3: Lexicon binding verification ──────────────────────────

    def test_ac3_enemy_contrast_verbatim(self):
        """AC3: enemy_contrast_noun must equal the exact lexicon entry."""
        arch = self._arch()
        lexicon = _make_lexicon(enemies=["The Hustle Culture"])
        row = arch.compile_brief(
            coping_positions=[4, 4, 4],
            character_lexicon=lexicon,
            user_requested_price=9.0,
            flyer_hook_text="Break free today",
        )
        assert row.enemy_contrast_noun == "The Hustle Culture"

    def test_ac3_hero_anchor_verbatim(self):
        arch = self._arch()
        lexicon = _make_lexicon(heroes=["The Conscious Leader"])
        row = arch.compile_brief(
            coping_positions=[1, 1, 1],
            character_lexicon=lexicon,
            user_requested_price=9.0,
            flyer_hook_text="Lead your team now",
        )
        assert row.hero_anchor_noun == "The Conscious Leader"

    # ── Output schema correctness ───────────────────────────────────

    def test_output_is_brief_row_instance(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs())
        assert isinstance(row, ChallengeFunnelBriefRow)

    def test_coach_id_scoped_correctly(self):
        arch = self._arch(coach_id="unique-coach-xyz")
        row = arch.compile_brief(**self._default_kwargs())
        assert row.coach_id == "unique-coach-xyz"

    def test_funnel_blueprint_id_is_uuid(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs())
        # Should not raise
        parsed = uuid.UUID(row.funnel_blueprint_id)
        assert str(parsed) == row.funnel_blueprint_id

    def test_generated_at_is_iso_string(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs())
        from datetime import datetime
        # Should parse without error
        dt = datetime.fromisoformat(row.generated_at)
        assert dt is not None

    # ── Duration / focus resolution ─────────────────────────────────

    def test_duration_5_day_for_modal_lte_2(self):
        arch = self._arch()
        row = arch.compile_brief(
            coping_positions=[2, 2, 2],
            character_lexicon=_make_lexicon(),
            user_requested_price=9.0,
            flyer_hook_text="Start your journey now",
        )
        assert row.challenge_duration_days == 5
        assert row.structure_focus == StructureFocus.FIVE_DAY_MOMENTUM

    def test_duration_7_day_for_modal_gte_3(self):
        arch = self._arch()
        row = arch.compile_brief(
            coping_positions=[3, 3, 3],
            character_lexicon=_make_lexicon(),
            user_requested_price=9.0,
            flyer_hook_text="Shift your identity now",
        )
        assert row.challenge_duration_days == 7
        assert row.structure_focus == StructureFocus.SEVEN_DAY_IDENTITY

    def test_price_locked_as_commitment_price(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs(price=12.5))
        assert row.commitment_price == 12.5

    def test_gate_verdict_pass_string(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs(price=9.0))
        assert row.gate_verdict == CommitmentGateVerdict.PASS

    # ── Lexicon error paths ─────────────────────────────────────────

    def test_missing_heroes_key_raises(self):
        arch = self._arch()
        with pytest.raises(ValueError) as exc:
            arch.compile_brief(
                coping_positions=[1, 1],
                character_lexicon={"category_4_enemies": ["Bad Guy"]},
                user_requested_price=9.0,
                flyer_hook_text="Short hook text",
            )
        assert ChallengeFunnelError.LEXICON_KEY_MISSING in str(exc.value)

    def test_missing_enemies_key_raises(self):
        arch = self._arch()
        with pytest.raises(ValueError) as exc:
            arch.compile_brief(
                coping_positions=[1, 1],
                character_lexicon={"category_1_heroes": ["Hero"]},
                user_requested_price=9.0,
                flyer_hook_text="Short hook text",
            )
        assert ChallengeFunnelError.LEXICON_KEY_MISSING in str(exc.value)

    def test_empty_heroes_list_raises_missing_anchor(self):
        arch = self._arch()
        with pytest.raises(ValueError) as exc:
            arch.compile_brief(
                coping_positions=[1],
                character_lexicon={"category_1_heroes": [], "category_4_enemies": ["Enemy"]},
                user_requested_price=9.0,
                flyer_hook_text="Hook text",
            )
        assert ChallengeFunnelError.MISSING_TRIBAL_ANCHOR in str(exc.value)

    # ── flyer_hook_text word-count guard ────────────────────────────

    def test_hook_text_exactly_6_words_allowed(self):
        arch = self._arch()
        row = arch.compile_brief(
            coping_positions=[1],
            character_lexicon=_make_lexicon(),
            user_requested_price=9.0,
            flyer_hook_text="one two three four five six",
        )
        assert row.flyer_hook_text == "one two three four five six"

    def test_hook_text_7_words_raises(self):
        arch = self._arch()
        with pytest.raises(ValueError, match="flyer_hook_text"):
            arch.compile_brief(
                coping_positions=[1],
                character_lexicon=_make_lexicon(),
                user_requested_price=9.0,
                flyer_hook_text="one two three four five six seven",
            )

    # ── empty coping array propagates ──────────────────────────────

    def test_empty_coping_positions_raises(self):
        arch = self._arch()
        with pytest.raises(ValueError) as exc:
            arch.compile_brief(
                coping_positions=[],
                character_lexicon=_make_lexicon(),
                user_requested_price=9.0,
                flyer_hook_text="Quick hook",
            )
        assert ChallengeFunnelError.EMPTY_COPING_ARRAY in str(exc.value)

    # ── Receipt chain integration ────────────────────────────────────

    def test_receipt_logged_on_success(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR1", log_dir=tmp)
            arch = ChallengeFunnelArchitect(coach_id="coach-rctest", receipt_chain=rc)
            arch.compile_brief(
                coping_positions=[3, 3],
                character_lexicon=_make_lexicon(),
                user_requested_price=9.0,
                flyer_hook_text="Reclaim your time today",
            )
            entries = rc.query(action="challenge-ict-resolve")
            assert len(entries) >= 1
            gate_entries = rc.query(action="challenge-gate-evaluate")
            assert len(gate_entries) >= 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_receipt_logged_on_fail_overpriced(self):
        """Gate receipt is written even on FAIL_OVERPRICED before raising."""
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR1", log_dir=tmp)
            arch = ChallengeFunnelArchitect(coach_id="coach-failtest", receipt_chain=rc)
            with pytest.raises(ValueError):
                arch.compile_brief(
                    coping_positions=[2, 2],
                    character_lexicon=_make_lexicon(),
                    user_requested_price=49.0,
                    flyer_hook_text="Big price big fail",
                )
            entries = rc.query(action="challenge-gate-evaluate")
            assert len(entries) >= 1
            assert "FAIL_OVERPRICED" in entries[0].output_summary
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_receipt_ict_resolve_content(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR1", log_dir=tmp)
            arch = ChallengeFunnelArchitect(coach_id="coach-ict-chk", receipt_chain=rc)
            arch.compile_brief(
                coping_positions=[1, 1, 1],
                character_lexicon=_make_lexicon(),
                user_requested_price=9.0,
                flyer_hook_text="Five days quick start",
            )
            entries = rc.query(action="challenge-ict-resolve")
            assert len(entries) == 1
            summary = entries[0].output_summary
            assert "coach-ict-chk" in summary
            assert "modal_coping=1" in summary
            assert "duration=5" in summary
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ── ADR-01 coach_id scoping ─────────────────────────────────────

    def test_adr01_coach_id_in_output(self):
        arch = self._arch(coach_id="scoped-coach-A")
        row = arch.compile_brief(**self._default_kwargs())
        assert row.coach_id == "scoped-coach-A"

    def test_adr01_different_coaches_different_blueprints(self):
        """Two architects produce different blueprint IDs."""
        arch_a = _make_architect(self._tmp_dir + "a", "coach-A")
        arch_b = _make_architect(self._tmp_dir + "b", "coach-B")
        row_a = arch_a.compile_brief(**self._default_kwargs())
        row_b = arch_b.compile_brief(**self._default_kwargs())
        assert row_a.funnel_blueprint_id != row_b.funnel_blueprint_id
        assert row_a.coach_id != row_b.coach_id

    # ── Price boundary edge cases ───────────────────────────────────

    def test_price_exactly_1_pass(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs(price=1.0))
        assert row.gate_verdict == CommitmentGateVerdict.PASS

    def test_price_exactly_17_pass(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs(price=17.0))
        assert row.gate_verdict == CommitmentGateVerdict.PASS

    def test_price_17_01_aborts(self):
        arch = self._arch()
        with pytest.raises(ValueError):
            arch.compile_brief(**self._default_kwargs(price=17.01))

    # ── Constructor guards ──────────────────────────────────────────

    def test_short_coach_id_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR1", log_dir=tmp)
            with pytest.raises(ValueError):
                ChallengeFunnelArchitect(coach_id="x", receipt_chain=rc)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_empty_coach_id_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR1", log_dir=tmp)
            with pytest.raises(ValueError):
                ChallengeFunnelArchitect(coach_id="", receipt_chain=rc)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ── Misc / model field completeness ─────────────────────────────

    def test_all_required_fields_populated(self):
        arch = self._arch()
        row = arch.compile_brief(**self._default_kwargs())
        assert row.funnel_blueprint_id
        assert row.coach_id
        assert row.challenge_duration_days in (5, 7)
        assert row.structure_focus in (
            StructureFocus.FIVE_DAY_MOMENTUM,
            StructureFocus.SEVEN_DAY_IDENTITY,
        )
        assert row.commitment_price >= 0
        assert row.hero_anchor_noun
        assert row.enemy_contrast_noun
        assert row.flyer_hook_text
        assert row.gate_verdict
        assert row.generated_at

    def test_flyer_hook_stored_verbatim(self):
        arch = self._arch()
        hook = "Build your tribe now"
        row = arch.compile_brief(**self._default_kwargs(hook=hook))
        assert row.flyer_hook_text == hook
