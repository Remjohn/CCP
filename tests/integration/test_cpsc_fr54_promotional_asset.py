"""
Tests — FR54: Promotional Asset Compiler
==========================================
Covers PayloadCompletenessGate, PromotionalAssetCompiler,
all three ACs, Z-Pattern node correctness, VOICE_SCRIPT path,
receipt chain, and ADR-01 isolation.
"""

from __future__ import annotations

import shutil
import tempfile
import uuid

import pytest

from src.ccp.models.cpsc_models import (
    AssetCompilerError,
    AssetTypeGenerated,
    PayloadCompletenessVerdict,
    StructuredAssetPayloadRow,
    ZPatternNodes,
)
from src.ccp.services.promotional_asset_compiler import (
    FLYER_HOOK_MAX_WORDS,
    PLACEHOLDER_PHOTO_SENTINEL,
    PayloadCompletenessGate,
    PromotionalAssetCompiler,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_IMAGE_URL = "https://assets.ccp.io/photos/coach123.jpg"
FAKE_SOURCE_ID = str(uuid.uuid4())


def _make_rc(tmp_dir: str) -> ReceiptChain:
    return ReceiptChain(coach_acronym="FR4", log_dir=tmp_dir)


def _make_compiler(tmp_dir: str, coach_id: str = "coach-fr54") -> PromotionalAssetCompiler:
    return PromotionalAssetCompiler(coach_id=coach_id, receipt_chain=_make_rc(tmp_dir))


# ---------------------------------------------------------------------------
# PayloadCompletenessGate Tests
# ---------------------------------------------------------------------------

class TestPayloadCompletenessGate:

    # ── FAIL cases ────────────────────────────────────────────────────

    def test_none_node_1_fail(self):
        gate = PayloadCompletenessGate(None, VALID_IMAGE_URL)
        assert gate.evaluate() == PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION

    def test_7_word_hook_fail(self):
        gate = PayloadCompletenessGate("one two three four five six seven", VALID_IMAGE_URL)
        assert gate.evaluate() == PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION

    def test_15_word_hook_fail(self):
        # AC1: 15-word headline
        long_hook = "the quick brown fox jumps over the lazy dog and then some more"
        gate = PayloadCompletenessGate(long_hook, VALID_IMAGE_URL)
        assert gate.evaluate() == PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION

    # ── PROVISIONAL cases ─────────────────────────────────────────────

    def test_none_image_provisional(self):
        # AC2: coach photo missing
        gate = PayloadCompletenessGate("Short hook here", None)
        assert gate.evaluate() == PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

    def test_placeholder_image_provisional(self):
        # AC2: exact sentinel
        gate = PayloadCompletenessGate("Short hook", PLACEHOLDER_PHOTO_SENTINEL)
        assert gate.evaluate() == PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

    def test_placeholder_in_url_provisional(self):
        gate = PayloadCompletenessGate("Hook text", f"https://example.com/{PLACEHOLDER_PHOTO_SENTINEL}/img.jpg")
        assert gate.evaluate() == PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

    # ── PASS cases ───────────────────────────────────────────────────

    def test_6_word_hook_valid_image_pass(self):
        gate = PayloadCompletenessGate("one two three four five six", VALID_IMAGE_URL)
        assert gate.evaluate() == PayloadCompletenessVerdict.PASS

    def test_1_word_hook_valid_image_pass(self):
        gate = PayloadCompletenessGate("Transform", VALID_IMAGE_URL)
        assert gate.evaluate() == PayloadCompletenessVerdict.PASS

    def test_exactly_6_words_pass(self):
        gate = PayloadCompletenessGate("a b c d e f", VALID_IMAGE_URL)
        assert gate.evaluate() == PayloadCompletenessVerdict.PASS

    # ── Priority: fail before provisional ────────────────────────────

    def test_long_hook_with_missing_image_still_fails(self):
        """Boundary violation takes priority over missing asset."""
        gate = PayloadCompletenessGate("word " * 10, None)
        assert gate.evaluate() == PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION

    # Spec §10: [3, 6, 7] → [PASS, PASS, FAIL]
    def test_spec_length_map(self):
        hooks = [
            "a b c",
            "a b c d e f",
            "a b c d e f g",
        ]
        expected = [
            PayloadCompletenessVerdict.PASS,
            PayloadCompletenessVerdict.PASS,
            PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION,
        ]
        for hook, exp in zip(hooks, expected):
            verdict = PayloadCompletenessGate(hook, VALID_IMAGE_URL).evaluate()
            assert verdict == exp


# ---------------------------------------------------------------------------
# PromotionalAssetCompiler — Flyer Tests
# ---------------------------------------------------------------------------

class TestPromotionalAssetCompilerFlyer:

    @pytest.fixture(autouse=True)
    def _tmp(self, tmp_path):
        self._tmp_dir = str(tmp_path)
        yield
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def _compiler(self, coach_id: str = "coach-fr54") -> PromotionalAssetCompiler:
        return _make_compiler(self._tmp_dir, coach_id)

    def _flyer_kwargs(
        self,
        hook: str = "Transform your tribe today",
        price: float = 9.0,
        image: str | None = VALID_IMAGE_URL,
    ) -> dict:
        return dict(
            generator_source_id=FAKE_SOURCE_ID,
            hook_text=hook,
            commitment_price=price,
            enemy_contrast_noun="The Hustle Culture",
            coach_verified_image_url=image,
        )

    # ── AC1: Hard boundary enforcement ──────────────────────────────

    def test_ac1_15_word_hook_raises(self):
        """AC1: 15-word headline → FAIL_BOUNDARY_VIOLATION + ValueError."""
        compiler = self._compiler()
        long_hook = "the quick brown fox jumps over the lazy dog and then some more extra"
        with pytest.raises(ValueError) as exc:
            compiler.compile_flyer(**self._flyer_kwargs(hook=long_hook))
        assert AssetCompilerError.FAIL_BOUNDARY_VIOLATION in str(exc.value)

    def test_ac1_7_word_hook_raises(self):
        compiler = self._compiler()
        with pytest.raises(ValueError):
            compiler.compile_flyer(**self._flyer_kwargs(hook="one two three four five six seven"))

    # ── AC2: Provisional photo halt ──────────────────────────────────

    def test_ac2_missing_photo_provisional(self):
        """AC2: missing coach photo → PROVISIONAL_MISSING_ASSET, row returned."""
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs(image=None))
        assert row.gate_verdict == PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

    def test_ac2_placeholder_photo_provisional(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs(image=PLACEHOLDER_PHOTO_SENTINEL))
        assert row.gate_verdict == PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

    # ── AC3: Z-Pattern schema verification ──────────────────────────

    def test_ac3_z_pattern_flyer_type(self):
        """AC3: FR51 brief → asset_type_generated=Z_PATTERN_FLYER."""
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        assert row.asset_type_generated == AssetTypeGenerated.Z_PATTERN_FLYER

    def test_ac3_bottom_right_cta_is_price(self):
        """AC3: z_pattern_nodes.bottom_right_cta = "$9.0" (str of price)."""
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs(price=9.0))
        assert row.z_pattern_nodes is not None
        assert "9.0" in row.z_pattern_nodes.bottom_right_cta

    def test_ac3_top_left_hook_stored(self):
        compiler = self._compiler()
        hook = "Break free from hustle now"
        row = compiler.compile_flyer(**self._flyer_kwargs(hook=hook))
        assert row.z_pattern_nodes is not None
        assert row.z_pattern_nodes.top_left_hook == hook

    # ── Output schema correctness ────────────────────────────────────

    def test_output_is_structured_asset_row(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        assert isinstance(row, StructuredAssetPayloadRow)

    def test_asset_payload_id_is_uuid(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        parsed = uuid.UUID(row.asset_payload_id)
        assert str(parsed) == row.asset_payload_id

    def test_generator_source_id_preserved(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        assert row.generator_source_id == FAKE_SOURCE_ID

    def test_compiled_at_iso(self):
        from datetime import datetime
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        dt = datetime.fromisoformat(row.compiled_at)
        assert dt is not None

    def test_tts_script_body_null_for_flyer(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        assert row.tts_script_body is None

    def test_gate_verdict_pass_on_valid_flyer(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs())
        assert row.gate_verdict == PayloadCompletenessVerdict.PASS

    # ── Receipt chain ────────────────────────────────────────────────

    def test_receipt_logged_on_pass(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR4", log_dir=tmp)
            compiler = PromotionalAssetCompiler(coach_id="coach-rctest", receipt_chain=rc)
            compiler.compile_flyer(
                generator_source_id=FAKE_SOURCE_ID,
                hook_text="Build your tribe fast",
                commitment_price=9.0,
                enemy_contrast_noun="The Hustle",
                coach_verified_image_url=VALID_IMAGE_URL,
            )
            type_entries = rc.query(action="asset-type-resolve")
            assert len(type_entries) >= 1
            gate_entries = rc.query(action="asset-completeness-gate")
            assert len(gate_entries) >= 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_receipt_logged_on_fail(self):
        """Receipt written before FAIL_BOUNDARY_VIOLATION raise."""
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR4", log_dir=tmp)
            compiler = PromotionalAssetCompiler(coach_id="coach-failtest", receipt_chain=rc)
            with pytest.raises(ValueError):
                compiler.compile_flyer(
                    generator_source_id=FAKE_SOURCE_ID,
                    hook_text="this hook is far too long for z pattern",
                    commitment_price=9.0,
                    enemy_contrast_noun="Enemy",
                    coach_verified_image_url=VALID_IMAGE_URL,
                )
            gate_entries = rc.query(action="asset-completeness-gate")
            assert len(gate_entries) >= 1
            assert "FAIL_BOUNDARY_VIOLATION" in gate_entries[0].output_summary
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ── ADR-01 ───────────────────────────────────────────────────────

    def test_two_coaches_different_asset_ids(self):
        compiler_a = _make_compiler(self._tmp_dir + "a", "coach-A")
        compiler_b = _make_compiler(self._tmp_dir + "b", "coach-B")
        row_a = compiler_a.compile_flyer(**self._flyer_kwargs())
        row_b = compiler_b.compile_flyer(**self._flyer_kwargs())
        assert row_a.asset_payload_id != row_b.asset_payload_id

    # ── Boundary edge cases ──────────────────────────────────────────

    def test_exactly_6_word_hook_passes(self):
        compiler = self._compiler()
        row = compiler.compile_flyer(**self._flyer_kwargs(hook="one two three four five six"))
        assert row.gate_verdict == PayloadCompletenessVerdict.PASS

    def test_constructor_short_coach_id_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            rc = ReceiptChain(coach_acronym="FR4", log_dir=tmp)
            with pytest.raises(ValueError):
                PromotionalAssetCompiler(coach_id="x", receipt_chain=rc)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# PromotionalAssetCompiler — Voice Script Tests
# ---------------------------------------------------------------------------

class TestPromotionalAssetCompilerVoiceScript:

    @pytest.fixture(autouse=True)
    def _tmp(self, tmp_path):
        self._tmp_dir = str(tmp_path)
        yield
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def _compiler(self) -> PromotionalAssetCompiler:
        return _make_compiler(self._tmp_dir)

    # Spec §10: origin=FR52 → VOICE_SCRIPT
    def test_voice_script_type_from_webinar_source(self):
        compiler = self._compiler()
        row = compiler.compile_voice_script(
            generator_source_id=FAKE_SOURCE_ID,
            tts_script_body="I know you're ready to make a change.",
            coach_verified_image_url=VALID_IMAGE_URL,
        )
        assert row.asset_type_generated == AssetTypeGenerated.VOICE_SCRIPT

    def test_voice_script_tts_body_stored(self):
        compiler = self._compiler()
        script = "Change Talk phrase verbatim here."
        row = compiler.compile_voice_script(
            generator_source_id=FAKE_SOURCE_ID,
            tts_script_body=script,
            coach_verified_image_url=VALID_IMAGE_URL,
        )
        assert row.tts_script_body == script

    def test_voice_script_z_nodes_null(self):
        compiler = self._compiler()
        row = compiler.compile_voice_script(
            generator_source_id=FAKE_SOURCE_ID,
            tts_script_body="Short script.",
            coach_verified_image_url=VALID_IMAGE_URL,
        )
        assert row.z_pattern_nodes is None

    def test_voice_script_missing_photo_provisional(self):
        compiler = self._compiler()
        row = compiler.compile_voice_script(
            generator_source_id=FAKE_SOURCE_ID,
            tts_script_body="Script text here.",
            coach_verified_image_url=None,
        )
        assert row.gate_verdict == PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

    def test_voice_script_valid_photo_pass(self):
        compiler = self._compiler()
        row = compiler.compile_voice_script(
            generator_source_id=FAKE_SOURCE_ID,
            tts_script_body="Motivating script body text.",
            coach_verified_image_url=VALID_IMAGE_URL,
        )
        assert row.gate_verdict == PayloadCompletenessVerdict.PASS
