"""
FR-VIS-03 — PSSL Prompt Compilation — Integration Tests
========================================================
Tests for Paradoxe's deterministic PSSL-to-prompt translation pipeline.

Coverage map:
  TestAC1PSSLTranslationFidelity     → AC1 (lighting grammar translation)
  TestAC2SaturationTranslation       → AC2 (numeric → descriptive mapping)
  TestAC3GazeGeometryCompilation     → AC3 (negative head rotation, left gaze)
  TestAC4AntiGenericFromEnemy        → AC4 (enemy typology → anti-patterns)
  TestAC5ReferenceImageStrength      → AC5 (0.85 default, 0.95 drift retry)
  TestAC6ExponentialBackoff          → AC6 (5→10→20→40→60→60 schedule)
  TestTranslationDeterminism         → 5x identical compilation
  TestFullCompilationPipeline        → End-to-end VCB → payloads
  TestReceiptChainIntegration        → Receipt audit
  TestADR01CoachAcronym              → ADR-01 enforcement
  TestLegacyPSSLFallback             → §6 backward compat
"""

from __future__ import annotations

import tempfile
import unittest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AccumulationAudit,
    AccumulationAuditStatus,
    DEFAULT_IMPERFECTION_SPEC,
    ENEMY_ANTI_PATTERNS,
    GateC09Result,
    GateC09Verdict,
    GrammarSystem,
    HandleBarConfig,
    MoodState,
    PADVector,
    PSSLBlock,
    PerSlideAssignment,
    PollingStatus,
    REFERENCE_IMAGE_STRENGTH_DEFAULT,
    REFERENCE_IMAGE_STRENGTH_HIGH,
    RUNNINGHUB_INITIAL_BACKOFF_S,
    RUNNINGHUB_MAX_BACKOFF_S,
    RUNNINGHUB_TIMEOUT_TOTAL_S,
    SATURATION_RANGES,
    SomaticArcType,
    UNIVERSAL_ANTI_GENERIC,
    VisualCompositionBrief,
)
from src.ccp.services.paradoxe_pssl_compiler import ParadoxePSSLCompiler


# ====================================================================
# Helpers
# ====================================================================

def _make_compiler(coach: str = "TST") -> tuple[ParadoxePSSLCompiler, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    compiler = ParadoxePSSLCompiler(coach_acronym=coach, receipt_chain=rc)
    return compiler, rc


def _make_pssl(**overrides) -> PSSLBlock:
    defaults = dict(
        lighting_grammar=(
            "overcast diffused, temporal_signal: 5200K-5600K neutral hold, "
            "shadow: 45° key angle, fill ratio 3:1"
        ),
        saturation_pct=72,
        head_rotation_degrees=15.0,
        pupil_position_ratio_pct=65.0,
        pad_environmental_grammar=PADVector(P=0.4, A=0.7, D=0.3),
        chromatic_bloom_sequence=["#2D1B69→#FF6B35 ease 2s"],
        incomplete_tribal_artifact="half-drawn circle",
    )
    defaults.update(overrides)
    return PSSLBlock(**defaults)


def _make_slide(index: int = 0, **pssl_overrides) -> PerSlideAssignment:
    return PerSlideAssignment(
        slide_index=index,
        slide_type="hook_cover",
        image_type="tier_3_ai_realistic",
        pssl=_make_pssl(**pssl_overrides),
        tribal_noun_assignments=[],
        handle_bar=HandleBarConfig(visible=True, position="top_locked"),
        semantic_conflicts=[],
    )


def _make_vcb(slides: list[PerSlideAssignment] | None = None) -> VisualCompositionBrief:
    if slides is None:
        slides = [_make_slide(i) for i in range(3)]
    return VisualCompositionBrief(
        vcb_id="VCB-TST-20260318-001",
        content_output_id="CO-TST-20260318-001-CAROUSEL",
        coach_acronym="TST",
        content_format="carousel_dopamine_cliff",
        selected_recipe_id="RCP-001",
        somatic_arc_type=SomaticArcType.TENSION_RELEASE,
        slide_count=len(slides),
        format_envelope_id="FCE-TST-001",
        style_directive_id="SCD-TST-001",
        visual_style="cinematic_color_graded",
        mood_state=MoodState.ESCAPE,
        cbcs_score=6,
        per_slide_assignments=slides,
        accumulation_audit=AccumulationAudit(
            arc_type=SomaticArcType.TENSION_RELEASE,
            audit_status=AccumulationAuditStatus.NOT_APPLICABLE,
        ),
        gate_c09_result=GateC09Result(verdict=GateC09Verdict.PASS),
        timestamp_utc="2026-03-18T01:36:30Z",
    )


# ====================================================================
# AC1 — PSSL Translation Fidelity
# ====================================================================

class TestAC1PSSLTranslationFidelity(unittest.TestCase):
    """Overcast diffused lighting — correct terms present, wrong terms absent."""

    def setUp(self):
        self.compiler, _ = _make_compiler()
        self.pssl = _make_pssl()
        self.prompt = self.compiler.compile_pssl_text(self.pssl)

    def test_overcast_diffused_present(self):
        self.assertIn("overcast diffused", self.prompt.lower())

    def test_temporal_signal_present(self):
        self.assertIn("5200K", self.prompt)
        self.assertIn("5600K", self.prompt)

    def test_shadow_angle_present(self):
        self.assertIn("45", self.prompt)

    def test_fill_ratio_present(self):
        self.assertIn("3:1", self.prompt)

    def test_no_golden_or_warm(self):
        # "overcast diffused" should NOT produce "golden" or "warm"
        lighting = ParadoxePSSLCompiler.translate_lighting(self.pssl.lighting_grammar).lower()
        self.assertNotIn("golden", lighting)
        self.assertNotIn("warm", lighting)


# ====================================================================
# AC2 — Saturation Numeric Translation
# ====================================================================

class TestAC2SaturationTranslation(unittest.TestCase):

    def test_28_is_muted(self):
        t = ParadoxePSSLCompiler.translate_saturation(28)
        self.assertIn("muted", t.descriptor)
        self.assertIn("28%", t.full_text)

    def test_85_is_hyper(self):
        t = ParadoxePSSLCompiler.translate_saturation(85)
        self.assertIn("hyper-saturated", t.descriptor)
        self.assertIn("85%", t.full_text)

    def test_0_is_desaturated(self):
        t = ParadoxePSSLCompiler.translate_saturation(0)
        self.assertIn("desaturated", t.descriptor)

    def test_50_is_moderate(self):
        t = ParadoxePSSLCompiler.translate_saturation(50)
        self.assertIn("moderate", t.descriptor)

    def test_65_is_vivid(self):
        t = ParadoxePSSLCompiler.translate_saturation(65)
        self.assertIn("vivid", t.descriptor)

    def test_boundary_20(self):
        t = ParadoxePSSLCompiler.translate_saturation(20)
        self.assertIn("desaturated", t.descriptor)

    def test_boundary_21(self):
        t = ParadoxePSSLCompiler.translate_saturation(21)
        self.assertIn("muted", t.descriptor)

    def test_boundary_100(self):
        t = ParadoxePSSLCompiler.translate_saturation(100)
        self.assertIn("hyper-saturated", t.descriptor)


# ====================================================================
# AC3 — Gaze Geometry Compilation
# ====================================================================

class TestAC3GazeGeometryCompilation(unittest.TestCase):
    """Negative head rotation → left, low pupil → leftward."""

    def test_negative_rotation_left(self):
        g = ParadoxePSSLCompiler.translate_gaze(-20.0, 30.0)
        self.assertEqual(g.head_direction_text, "left")
        self.assertIn("20", g.compiled_text)
        self.assertIn("left", g.compiled_text.lower())

    def test_positive_rotation_right(self):
        g = ParadoxePSSLCompiler.translate_gaze(15.0, 65.0)
        self.assertEqual(g.head_direction_text, "right")
        self.assertIn("right", g.compiled_text.lower())

    def test_zero_rotation_center(self):
        g = ParadoxePSSLCompiler.translate_gaze(0.0, 50.0)
        self.assertEqual(g.head_direction_text, "center")

    def test_low_pupil_leftward(self):
        g = ParadoxePSSLCompiler.translate_gaze(-20.0, 30.0)
        self.assertEqual(g.pupil_direction_text, "leftward")

    def test_high_pupil_rightward(self):
        g = ParadoxePSSLCompiler.translate_gaze(15.0, 75.0)
        self.assertEqual(g.pupil_direction_text, "rightward")

    def test_mid_pupil_forward(self):
        g = ParadoxePSSLCompiler.translate_gaze(0.0, 50.0)
        self.assertEqual(g.pupil_direction_text, "forward")

    def test_pupil_percentage_in_text(self):
        g = ParadoxePSSLCompiler.translate_gaze(-20.0, 30.0)
        self.assertIn("30%", g.compiled_text)


# ====================================================================
# AC4 — Anti-Generic from Enemy
# ====================================================================

class TestAC4AntiGenericFromEnemy(unittest.TestCase):

    def test_toxic_positivity_patterns(self):
        ag = ParadoxePSSLCompiler.assemble_anti_generic("toxic positivity")
        self.assertIn("forced smiles", ag.compiled_text)
        self.assertIn("just be happy", ag.compiled_text)
        self.assertIn("neon color palettes", ag.compiled_text)

    def test_hustle_culture_patterns(self):
        ag = ParadoxePSSLCompiler.assemble_anti_generic("hustle culture")
        self.assertIn("glorified overwork", ag.compiled_text)

    def test_universal_always_present(self):
        ag = ParadoxePSSLCompiler.assemble_anti_generic("toxic positivity")
        self.assertIn("generic stock photography", ag.compiled_text)

    def test_no_enemy_uses_defaults(self):
        ag = ParadoxePSSLCompiler.assemble_anti_generic(None)
        self.assertIsNone(ag.enemy_anti_pattern)
        self.assertIn("generic stock photography", ag.compiled_text)

    def test_unknown_enemy_uses_defaults(self):
        ag = ParadoxePSSLCompiler.assemble_anti_generic("unknown enemy xyz")
        self.assertIsNone(ag.enemy_anti_pattern)
        self.assertIn(UNIVERSAL_ANTI_GENERIC, ag.compiled_text)


# ====================================================================
# AC5 — Reference Image Strength
# ====================================================================

class TestAC5ReferenceImageStrength(unittest.TestCase):

    def test_tier_3_default_strength(self):
        ref = ParadoxePSSLCompiler.build_reference_config(
            image_type="tier_3_ai_realistic",
            char_ref_id="CHAR-JP-001",
        )
        self.assertEqual(ref.strength, REFERENCE_IMAGE_STRENGTH_DEFAULT)
        self.assertTrue(ref.has_reference)

    def test_drift_retry_strength(self):
        ref = ParadoxePSSLCompiler.build_reference_config(
            image_type="tier_3_ai_realistic",
            char_ref_id="CHAR-JP-001",
            strength=REFERENCE_IMAGE_STRENGTH_HIGH,
        )
        self.assertEqual(ref.strength, 0.95)

    def test_ghibli_no_reference(self):
        ref = ParadoxePSSLCompiler.build_reference_config(
            image_type="tier_4_ghibli",
            lora_path="loras/ghibli_v3.safetensors",
        )
        self.assertFalse(ref.has_reference)
        self.assertTrue(ref.is_ghibli)
        self.assertIsNotNone(ref.lora_model_path)

    def test_no_char_ref_no_reference(self):
        ref = ParadoxePSSLCompiler.build_reference_config(
            image_type="tier_3_ai_realistic",
        )
        self.assertFalse(ref.has_reference)


# ====================================================================
# AC6 — Exponential Backoff
# ====================================================================

class TestAC6ExponentialBackoff(unittest.TestCase):

    def test_initial_is_5(self):
        self.assertEqual(RUNNINGHUB_INITIAL_BACKOFF_S, 5)

    def test_sequence_starts_5_10_20_40_60(self):
        seq = ParadoxePSSLCompiler.backoff_sequence()
        self.assertEqual(seq[0], 5)
        self.assertEqual(seq[1], 10)
        self.assertEqual(seq[2], 20)
        self.assertEqual(seq[3], 40)
        self.assertEqual(seq[4], 60)
        # After 60, stays at 60
        if len(seq) > 5:
            self.assertEqual(seq[5], 60)

    def test_does_not_exceed_timeout(self):
        seq = ParadoxePSSLCompiler.backoff_sequence()
        self.assertLessEqual(sum(seq), RUNNINGHUB_TIMEOUT_TOTAL_S + RUNNINGHUB_MAX_BACKOFF_S)

    def test_max_backoff_capped(self):
        nxt = ParadoxePSSLCompiler.compute_next_backoff(40)
        self.assertEqual(nxt, 60)
        nxt = ParadoxePSSLCompiler.compute_next_backoff(60)
        self.assertEqual(nxt, 60)

    def test_compute_doubling(self):
        self.assertEqual(ParadoxePSSLCompiler.compute_next_backoff(5), 10)
        self.assertEqual(ParadoxePSSLCompiler.compute_next_backoff(10), 20)
        self.assertEqual(ParadoxePSSLCompiler.compute_next_backoff(20), 40)


# ====================================================================
# Translation Determinism
# ====================================================================

class TestTranslationDeterminism(unittest.TestCase):
    """Same PSSL → same prompt text, every time."""

    def test_5x_identical(self):
        compiler, _ = _make_compiler()
        pssl = _make_pssl()
        self.assertTrue(compiler.compile_pssl_text_deterministic(pssl, n=5))

    def test_different_pssl_different_output(self):
        compiler, _ = _make_compiler()
        p1 = _make_pssl(saturation_pct=28)
        p2 = _make_pssl(saturation_pct=85)
        t1 = compiler.compile_pssl_text(p1)
        t2 = compiler.compile_pssl_text(p2)
        self.assertNotEqual(t1, t2)


# ====================================================================
# Full Compilation Pipeline
# ====================================================================

class TestFullCompilationPipeline(unittest.TestCase):

    def setUp(self):
        self.compiler, self.rc = _make_compiler()
        self.vcb = _make_vcb()
        self.payloads = self.compiler.compile_vcb(
            self.vcb,
            enemy_typology="toxic positivity",
            grammar_system=GrammarSystem.CINEMATIC,
        )

    def test_one_payload_per_slide(self):
        self.assertEqual(len(self.payloads), 3)

    def test_payloads_have_prompt_text(self):
        for p in self.payloads:
            self.assertGreater(len(p.compiled_prompt_text), 50)

    def test_payloads_have_anti_generic(self):
        for p in self.payloads:
            self.assertIn("forced smiles", p.anti_generic_constraints.compiled_text)

    def test_payloads_have_imperfection(self):
        for p in self.payloads:
            self.assertEqual(p.imperfection_spec, DEFAULT_IMPERFECTION_SPEC)

    def test_runninghub_payload_workflow(self):
        for p in self.payloads:
            self.assertTrue(p.runninghub_payload.workflow_id.startswith("WF-"))

    def test_compilation_id_format(self):
        for p in self.payloads:
            self.assertTrue(p.compilation_id.startswith("CPL-TST-"))

    def test_slide_indices_sequential(self):
        indices = [p.slide_index for p in self.payloads]
        self.assertEqual(indices, [0, 1, 2])


# ====================================================================
# Receipt Chain Integration
# ====================================================================

class TestReceiptChainIntegration(unittest.TestCase):

    def test_compile_vcb_writes_receipt(self):
        compiler, rc = _make_compiler()
        vcb = _make_vcb()
        compiler.compile_vcb(vcb)
        entries = rc.query(agent_id="paradoxe_pssl_compiler")
        # 1 per slide + 1 for compile_vcb
        self.assertGreaterEqual(len(entries), 4)  # 3 slides + 1 aggregate

    def test_receipt_contains_vcb_id(self):
        compiler, rc = _make_compiler()
        vcb = _make_vcb()
        compiler.compile_vcb(vcb)
        entries = rc.query(agent_id="paradoxe_pssl_compiler")
        for e in entries:
            self.assertIn("VCB-TST", e.asset_id)

    def test_receipt_actions(self):
        compiler, rc = _make_compiler()
        vcb = _make_vcb()
        compiler.compile_vcb(vcb)
        actions = {e.action for e in rc.query(agent_id="paradoxe_pssl_compiler")}
        self.assertIn("compile_slide", actions)
        self.assertIn("compile_vcb", actions)


# ====================================================================
# ADR-01 Coach Acronym Enforcement
# ====================================================================

class TestADR01CoachAcronym(unittest.TestCase):

    def test_valid_2_char(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="JPX", log_dir=tmp)
        c = ParadoxePSSLCompiler(coach_acronym="JP", receipt_chain=rc)
        self.assertIsNotNone(c)

    def test_valid_4_char(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="JPXX", log_dir=tmp)
        c = ParadoxePSSLCompiler(coach_acronym="JPXX", receipt_chain=rc)
        self.assertIsNotNone(c)

    def test_1_char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with self.assertRaises(ValueError):
            ParadoxePSSLCompiler(coach_acronym="J", receipt_chain=rc)

    def test_5_char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with self.assertRaises(ValueError):
            ParadoxePSSLCompiler(coach_acronym="ABCDE", receipt_chain=rc)


# ====================================================================
# PAD Translation
# ====================================================================

class TestPADTranslation(unittest.TestCase):

    def test_high_pleasure_warm(self):
        text = ParadoxePSSLCompiler.translate_pad(PADVector(P=0.8, A=0.3, D=0.0))
        self.assertIn("warm", text.lower())

    def test_low_pleasure_cold(self):
        text = ParadoxePSSLCompiler.translate_pad(PADVector(P=-0.7, A=0.5, D=0.0))
        self.assertIn("cold", text.lower())

    def test_high_arousal_tense(self):
        text = ParadoxePSSLCompiler.translate_pad(PADVector(P=0.0, A=0.8, D=0.0))
        self.assertIn("tense", text.lower())

    def test_high_dominance_expansive(self):
        text = ParadoxePSSLCompiler.translate_pad(PADVector(P=0.0, A=0.3, D=0.8))
        self.assertIn("expansive", text.lower())

    def test_low_dominance_confined(self):
        text = ParadoxePSSLCompiler.translate_pad(PADVector(P=0.0, A=0.3, D=-0.5))
        self.assertIn("confined", text.lower())


# ====================================================================
# Chromatic Bloom & Artifact
# ====================================================================

class TestChromaticAndArtifact(unittest.TestCase):

    def test_bloom_translation(self):
        text = ParadoxePSSLCompiler.translate_chromatic_bloom(
            ["#2D1B69→#FF6B35 ease 2s"]
        )
        self.assertIn("#2D1B69", text)
        self.assertIn("#FF6B35", text)

    def test_artifact_translation(self):
        text = ParadoxePSSLCompiler.translate_artifact("half-drawn circle")
        self.assertIn("half-drawn circle", text)
        self.assertIn("incomplete", text)

    def test_null_artifact_empty(self):
        text = ParadoxePSSLCompiler.translate_artifact(None)
        self.assertEqual(text, "")


# ====================================================================
# Ghibli Pipeline
# ====================================================================

class TestGhibliPipeline(unittest.TestCase):

    def test_ghibli_workflow(self):
        compiler, _ = _make_compiler()
        slide = _make_slide(0, **{})
        slide = slide.model_copy(update={"image_type": "tier_4_ghibli"})
        vcb = _make_vcb([slide])
        payloads = compiler.compile_vcb(
            vcb,
            lora_paths={0: "loras/ghibli_v3.safetensors"},
        )
        self.assertEqual(payloads[0].runninghub_payload.workflow_id, "WF-GHIBLI-V1-001")
        self.assertTrue(payloads[0].reference_image.is_ghibli)
        self.assertFalse(payloads[0].reference_image.has_reference)


if __name__ == "__main__":
    unittest.main()
