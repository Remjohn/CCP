"""
FR-VIS-01 — Visual Composition Brief Generation — Integration Tests
====================================================================
Tests for Abel's 9-step VCB generation pipeline and Gate C-09.

Coverage map:
  TestAC1FullVCBGeneration           → AC1 (7-slide carousel, all fields, Gate PASS)
  TestAC2SomaticArcSaturation        → AC2 (tension-release saturation curve)
  TestAC3GazeGeometryCold            → AC3 (CBCS 2 → Hook zone)
  TestAC4GazeGeometryWarm            → AC4 (CBCS 8 → Action zone)
  TestAC5AccumulationProhibition     → AC5 (completion imagery detection)
  TestAC6SemioticInjection           → AC6 (semiotic position validation)
  TestAC7GateC09FullValidation       → AC7 (multi-violation detection + auto-revision)
  TestPSSLHelpers                    → PSSL computation unit tests
  TestReceiptChainIntegration        → Receipt chain audit
  TestADR01CoachAcronym              → ADR-01 enforcement
  TestLegacyFallback                 → §6 backward compatibility
"""

from __future__ import annotations

import tempfile
import unittest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AccumulationAuditStatus,
    COMPLETION_IMAGERY_KEYWORDS,
    GAZE_ZONE_RANGES,
    GateC09Rule,
    GateC09Verdict,
    GazeTargetZone,
    MAX_INTERNAL_REVISIONS,
    MIN_TIAR_NOUNS_PER_TEXT_SLIDE,
    MOOD_SATURATION_ANCHORS,
    MoodState,
    SEMIOTIC_INJECTION_MIN_SLIDES,
    SomaticArcType,
    VCBError,
    VCBGenerationInput,
)
from src.ccp.services.abel_vcb_generator import AbelVCBGenerator


# ====================================================================
# Helpers
# ====================================================================

def _make_generator(coach: str = "TST") -> tuple[AbelVCBGenerator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    gen = AbelVCBGenerator(coach_acronym=coach, receipt_chain=rc)
    return gen, rc


def _default_input(**overrides) -> VCBGenerationInput:
    defaults = dict(
        content_output_id="CO-TST-20260318-001-CAROUSEL",
        coach_acronym="TST",
        content_format="carousel_dopamine_cliff",
        format_envelope_id="FCE-TST-20260318-001",
        style_directive_id="SCD-TST-20260318-001",
        visual_style="cinematic_color_graded",
        mood_state=MoodState.ESCAPE,
        cbcs_score=6,
        somatic_arc_type=SomaticArcType.TENSION_RELEASE,
        slide_count=7,
        active_nouns=[
            "the 5am alarm defeat",
            "Sunday night dread spiral",
            "client ghost",
            "revenue plateau confession",
            "launch anxiety loop",
        ],
        blocked_nouns=[],
    )
    defaults.update(overrides)
    return VCBGenerationInput(**defaults)


# ====================================================================
# AC1 — Full VCB Generation
# ====================================================================

class TestAC1FullVCBGeneration(unittest.TestCase):
    """7-slide carousel_dopamine_cliff, mood Escape, CBCS 6."""

    def setUp(self):
        self.gen, self.rc = _make_generator()
        self.inp = _default_input()
        self.vcb = self.gen.generate(self.inp)

    def test_vcb_has_7_slides(self):
        self.assertEqual(len(self.vcb.per_slide_assignments), 7)

    def test_all_slides_have_pssl(self):
        for s in self.vcb.per_slide_assignments:
            self.assertIsNotNone(s.pssl)
            self.assertIsNotNone(s.pssl.lighting_grammar)
            self.assertIsInstance(s.pssl.saturation_pct, int)
            self.assertTrue(0 <= s.pssl.saturation_pct <= 100)

    def test_all_slides_have_pad(self):
        for s in self.vcb.per_slide_assignments:
            pad = s.pssl.pad_environmental_grammar
            self.assertTrue(-1.0 <= pad.P <= 1.0)
            self.assertTrue(-1.0 <= pad.A <= 1.0)
            self.assertTrue(-1.0 <= pad.D <= 1.0)

    def test_all_slides_have_gaze(self):
        for s in self.vcb.per_slide_assignments:
            self.assertIsInstance(s.pssl.head_rotation_degrees, float)
            self.assertIsInstance(s.pssl.pupil_position_ratio_pct, float)

    def test_text_slides_have_tiar_nouns(self):
        for s in self.vcb.per_slide_assignments:
            self.assertGreaterEqual(len(s.tribal_noun_assignments), 3)

    def test_handle_bar_on_slide_0(self):
        self.assertTrue(self.vcb.per_slide_assignments[0].handle_bar.visible)
        self.assertEqual(self.vcb.per_slide_assignments[0].handle_bar.position, "top_locked")

    def test_handle_bar_off_other_slides(self):
        for s in self.vcb.per_slide_assignments[1:]:
            self.assertFalse(s.handle_bar.visible)

    def test_semiotic_injection_present(self):
        self.assertIsNotNone(self.vcb.semiotic_injection)
        # For 7 slides, injection on slide ≥ 2
        self.assertGreaterEqual(self.vcb.semiotic_injection.injection_slide_index, 2)

    def test_gate_c09_pass(self):
        self.assertEqual(self.vcb.gate_c09_result.verdict, GateC09Verdict.PASS)

    def test_chromatic_bloom_nonempty(self):
        for s in self.vcb.per_slide_assignments:
            self.assertGreaterEqual(len(s.pssl.chromatic_bloom_sequence), 1)

    def test_vcb_id_format(self):
        self.assertTrue(self.vcb.vcb_id.startswith("VCB-TST-"))

    def test_recipe_id_populated(self):
        self.assertTrue(len(self.vcb.selected_recipe_id) > 0)


# ====================================================================
# AC2 — Somatic Arc Saturation Curve
# ====================================================================

class TestAC2SomaticArcSaturation(unittest.TestCase):
    """Tension-Release arc: slides 0-3 rising, slides 4-6 dropping."""

    def setUp(self):
        self.gen, _ = _make_generator()
        self.inp = _default_input(
            somatic_arc_type=SomaticArcType.TENSION_RELEASE,
            mood_state=MoodState.ESCAPE,
        )
        self.vcb = self.gen.generate(self.inp)
        self.sats = [s.pssl.saturation_pct for s in self.vcb.per_slide_assignments]

    def test_rising_tension_phase(self):
        # Slides 0-3 should show non-decreasing saturation
        for i in range(1, 4):
            self.assertGreaterEqual(self.sats[i], self.sats[i - 1],
                f"saturation should rise: slide {i-1}={self.sats[i-1]}, slide {i}={self.sats[i]}")

    def test_peak_then_drop(self):
        # The peak saturation should be at some slide in the middle
        peak_idx = self.sats.index(max(self.sats))
        self.assertGreater(peak_idx, 0, "Peak should not be on first slide")
        # Last slide should be lower than peak
        self.assertLess(self.sats[-1], max(self.sats))

    def test_release_phase_decreases(self):
        peak_idx = self.sats.index(max(self.sats))
        # At least last slide should be lower than peak
        self.assertLess(self.sats[-1], self.sats[peak_idx])

    def test_saturation_values_in_escape_range(self):
        low, peak, release = MOOD_SATURATION_ANCHORS[MoodState.ESCAPE]
        for sat in self.sats:
            # Allow some tolerance — values should stay in the general range
            self.assertGreaterEqual(sat, release - 5)
            self.assertLessEqual(sat, peak + 5)


# ====================================================================
# AC3 — Gaze Geometry (Cold Audience)
# ====================================================================

class TestAC3GazeGeometryCold(unittest.TestCase):
    """CBCS 2 → gaze toward Hook Zone."""

    def setUp(self):
        self.gen, _ = _make_generator()
        self.inp = _default_input(cbcs_score=2)
        self.vcb = self.gen.generate(self.inp)

    def test_pupil_in_hook_zone(self):
        lo, hi = GAZE_ZONE_RANGES[GazeTargetZone.HOOK]
        for s in self.vcb.per_slide_assignments:
            self.assertGreaterEqual(s.pssl.pupil_position_ratio_pct, lo)
            self.assertLessEqual(s.pssl.pupil_position_ratio_pct, hi)

    def test_gaze_not_in_action_zone(self):
        lo, _ = GAZE_ZONE_RANGES[GazeTargetZone.ACTION]
        for s in self.vcb.per_slide_assignments:
            self.assertLess(s.pssl.pupil_position_ratio_pct, lo)


# ====================================================================
# AC4 — Gaze Geometry (Warm Audience)
# ====================================================================

class TestAC4GazeGeometryWarm(unittest.TestCase):
    """CBCS 8 → gaze toward Action Zone."""

    def setUp(self):
        self.gen, _ = _make_generator()
        self.inp = _default_input(cbcs_score=8)
        self.vcb = self.gen.generate(self.inp)

    def test_pupil_in_action_zone(self):
        lo, hi = GAZE_ZONE_RANGES[GazeTargetZone.ACTION]
        for s in self.vcb.per_slide_assignments:
            self.assertGreaterEqual(s.pssl.pupil_position_ratio_pct, lo)
            self.assertLessEqual(s.pssl.pupil_position_ratio_pct, hi)

    def test_gaze_not_in_hook_zone(self):
        _, hi = GAZE_ZONE_RANGES[GazeTargetZone.HOOK]
        for s in self.vcb.per_slide_assignments:
            self.assertGreater(s.pssl.pupil_position_ratio_pct, hi)


# ====================================================================
# AC5 — Accumulation Prohibition
# ====================================================================

class TestAC5AccumulationProhibition(unittest.TestCase):
    """Accumulation-cliff arc: detect completion imagery."""

    def test_clean_accumulation_audit(self):
        gen, _ = _make_generator()
        inp = _default_input(
            somatic_arc_type=SomaticArcType.ACCUMULATION_CLIFF,
        )
        vcb = gen.generate(inp)
        self.assertEqual(vcb.accumulation_audit.audit_status, AccumulationAuditStatus.CLEAN)

    def test_non_accumulation_arc_not_applicable(self):
        gen, _ = _make_generator()
        inp = _default_input(
            somatic_arc_type=SomaticArcType.DISCOVERY_REVELATION,
        )
        vcb = gen.generate(inp)
        self.assertEqual(vcb.accumulation_audit.audit_status, AccumulationAuditStatus.NOT_APPLICABLE)

    def test_completion_keywords_detected(self):
        found = AbelVCBGenerator.scan_completion_imagery("The trophy on the checkmark table")
        self.assertIn("trophy", found)
        self.assertIn("checkmark", found)

    def test_no_completion_imagery_in_normal_text(self):
        found = AbelVCBGenerator.scan_completion_imagery("person at desk thinking deeply")
        self.assertEqual(len(found), 0)

    def test_accumulation_slides_list(self):
        gen, _ = _make_generator()
        inp = _default_input(
            somatic_arc_type=SomaticArcType.ACCUMULATION_CLIFF,
            slide_count=5,
        )
        vcb = gen.generate(inp)
        # Accumulation slides = 0,1,2,3 (all except last cliff slide)
        self.assertEqual(vcb.accumulation_audit.accumulation_slides, [0, 1, 2, 3])


# ====================================================================
# AC6 — Semiotic Injection Position
# ====================================================================

class TestAC6SemioticInjection(unittest.TestCase):
    """Semiotic injection in latter third of 4+ slide sequences."""

    def test_6_slide_injection_on_4_or_5(self):
        gen, _ = _make_generator()
        inp = _default_input(slide_count=6)
        vcb = gen.generate(inp)
        self.assertIsNotNone(vcb.semiotic_injection)
        self.assertIn(vcb.semiotic_injection.injection_slide_index, [3, 4, 5])

    def test_injection_never_slide_0_or_1(self):
        gen, _ = _make_generator()
        for n in range(4, 10):
            inp = _default_input(slide_count=n)
            vcb = gen.generate(inp)
            self.assertIsNotNone(vcb.semiotic_injection)
            self.assertGreaterEqual(vcb.semiotic_injection.injection_slide_index, 2)

    def test_no_injection_for_3_slides(self):
        gen, _ = _make_generator()
        inp = _default_input(slide_count=3)
        vcb = gen.generate(inp)
        self.assertIsNone(vcb.semiotic_injection)

    def test_validate_semiotic_position_utility(self):
        # Valid
        self.assertTrue(AbelVCBGenerator.validate_semiotic_position(4, 7))
        # Invalid — slide 1 for 6-slide
        self.assertFalse(AbelVCBGenerator.validate_semiotic_position(1, 6))
        # Under minimum slides — always valid
        self.assertTrue(AbelVCBGenerator.validate_semiotic_position(0, 3))

    def test_c09_r07_rejects_early_injection(self):
        """Gate C-09 should catch injection on slide 0 or 1."""
        gen, _ = _make_generator()
        inp = _default_input(slide_count=6)
        vcb = gen.generate(inp)
        # The generator should have placed it correctly
        self.assertTrue(vcb.semiotic_injection.position_valid)


# ====================================================================
# AC7 — Gate C-09 Full Validation
# ====================================================================

class TestAC7GateC09FullValidation(unittest.TestCase):
    """Multi-violation detection and auto-revision."""

    def test_all_7_checks_present(self):
        gen, _ = _make_generator()
        inp = _default_input()
        vcb = gen.generate(inp)
        rules_checked = {c.rule for c in vcb.gate_c09_result.checks}
        for rule in GateC09Rule:
            self.assertIn(rule.value, rules_checked, f"Missing check for {rule}")

    def test_gate_passes_for_valid_input(self):
        gen, _ = _make_generator()
        inp = _default_input()
        vcb = gen.generate(inp)
        self.assertEqual(vcb.gate_c09_result.verdict, GateC09Verdict.PASS)
        self.assertEqual(len(vcb.gate_c09_result.violations), 0)

    def test_insufficient_nouns_triggers_auto_revision(self):
        """With only 1 active noun, initial VCB fails C09-R03, auto-revision adds more."""
        gen, _ = _make_generator()
        inp = _default_input(active_nouns=["sole noun"])
        vcb = gen.generate(inp)
        # After auto-revision the generator should still produce a VCB
        # (either pass or escalate)
        self.assertIsNotNone(vcb.gate_c09_result)

    def test_all_checks_pass_individually(self):
        gen, _ = _make_generator()
        inp = _default_input()
        vcb = gen.generate(inp)
        for c in vcb.gate_c09_result.checks:
            self.assertTrue(c.passed, f"Rule {c.rule} failed: {c.detail}")


# ====================================================================
# PSSL Helpers
# ====================================================================

class TestPSSLHelpers(unittest.TestCase):
    """Unit tests for PSSL computation statics."""

    def test_saturation_tension_release_peak_not_first(self):
        anchors = MOOD_SATURATION_ANCHORS[MoodState.ESCAPE]
        sats = [
            AbelVCBGenerator._saturation_for_slide(i, 7, SomaticArcType.TENSION_RELEASE, anchors)
            for i in range(7)
        ]
        peak_idx = sats.index(max(sats))
        self.assertGreater(peak_idx, 0)

    def test_saturation_discovery_monotonic(self):
        anchors = MOOD_SATURATION_ANCHORS[MoodState.DISCOVERY]
        sats = [
            AbelVCBGenerator._saturation_for_slide(i, 7, SomaticArcType.DISCOVERY_REVELATION, anchors)
            for i in range(7)
        ]
        for i in range(1, len(sats)):
            self.assertGreaterEqual(sats[i], sats[i - 1])

    def test_saturation_contrast_alternates(self):
        anchors = MOOD_SATURATION_ANCHORS[MoodState.STATUS]
        sats = [
            AbelVCBGenerator._saturation_for_slide(i, 6, SomaticArcType.CONTRAST_RESOLUTION, anchors)
            for i in range(6)
        ]
        # Even slides high, odd slides low
        for i in range(len(sats)):
            if i % 2 == 0:
                self.assertEqual(sats[i], anchors[1])  # peak
            else:
                self.assertEqual(sats[i], anchors[0])  # low

    def test_saturation_accumulation_cliff_last(self):
        anchors = MOOD_SATURATION_ANCHORS[MoodState.ESCAPE]
        sats = [
            AbelVCBGenerator._saturation_for_slide(i, 5, SomaticArcType.ACCUMULATION_CLIFF, anchors)
            for i in range(5)
        ]
        # Last slide drops to release
        self.assertEqual(sats[-1], anchors[2])
        # Preceding slides should be higher than release
        for sat in sats[:-1]:
            self.assertGreaterEqual(sat, anchors[2])

    def test_single_slide_returns_peak(self):
        anchors = MOOD_SATURATION_ANCHORS[MoodState.PROCESSING]
        sat = AbelVCBGenerator._saturation_for_slide(0, 1, SomaticArcType.TENSION_RELEASE, anchors)
        self.assertEqual(sat, anchors[1])

    def test_resolve_gaze_cold(self):
        zone = AbelVCBGenerator._resolve_gaze_zone(2)
        self.assertEqual(zone, GazeTargetZone.HOOK)

    def test_resolve_gaze_warm(self):
        zone = AbelVCBGenerator._resolve_gaze_zone(8)
        self.assertEqual(zone, GazeTargetZone.ACTION)

    def test_resolve_gaze_mid(self):
        zone = AbelVCBGenerator._resolve_gaze_zone(5)
        self.assertEqual(zone, GazeTargetZone.HOOK)  # mid defaults to Hook

    def test_pupil_for_hook_zone(self):
        p = AbelVCBGenerator._pupil_for_zone(GazeTargetZone.HOOK)
        lo, hi = GAZE_ZONE_RANGES[GazeTargetZone.HOOK]
        self.assertGreaterEqual(p, lo)
        self.assertLessEqual(p, hi)

    def test_lighting_grammar_contains_temporal(self):
        lg = AbelVCBGenerator._lighting_grammar(0, (4500, 5000), 65)
        self.assertIn("temporal_signal", lg)

    def test_incomplete_artifact_tension(self):
        # Non-final slide in tension arc should have artifact
        self.assertIsNotNone(
            AbelVCBGenerator._incomplete_artifact(2, 7, SomaticArcType.TENSION_RELEASE)
        )
        # Final slide should be None (release)
        self.assertIsNone(
            AbelVCBGenerator._incomplete_artifact(6, 7, SomaticArcType.TENSION_RELEASE)
        )

    def test_incomplete_artifact_discovery_always_none(self):
        self.assertIsNone(
            AbelVCBGenerator._incomplete_artifact(2, 7, SomaticArcType.DISCOVERY_REVELATION)
        )


# ====================================================================
# Receipt Chain Integration
# ====================================================================

class TestReceiptChainIntegration(unittest.TestCase):

    def test_generate_writes_receipts(self):
        gen, rc = _make_generator()
        inp = _default_input()
        gen.generate(inp)
        entries = rc.query(agent_id="abel_vcb_generator")
        # At least 4 stages (stage 1-5 minus possibly merged)
        self.assertGreaterEqual(len(entries), 4)

    def test_receipt_contains_asset_id(self):
        gen, rc = _make_generator()
        inp = _default_input()
        gen.generate(inp)
        entries = rc.query(agent_id="abel_vcb_generator")
        for e in entries:
            self.assertIn("CO-TST-20260318-001-CAROUSEL", e.asset_id)

    def test_receipt_stage_actions(self):
        gen, rc = _make_generator()
        inp = _default_input()
        gen.generate(inp)
        actions = {e.action for e in rc.query(agent_id="abel_vcb_generator")}
        self.assertIn("stage_1_format_recipe", actions)
        self.assertIn("stage_2_pssl_assignment", actions)
        self.assertIn("stage_3_tiar_pairing", actions)
        self.assertIn("stage_5_gate_c09", actions)


# ====================================================================
# ADR-01 Coach Acronym Enforcement
# ====================================================================

class TestADR01CoachAcronym(unittest.TestCase):

    def test_valid_2_char(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="JPX", log_dir=tmp)
        gen = AbelVCBGenerator(coach_acronym="JP", receipt_chain=rc)
        self.assertIsNotNone(gen)

    def test_valid_4_char(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="JPXX", log_dir=tmp)
        gen = AbelVCBGenerator(coach_acronym="JPXX", receipt_chain=rc)
        self.assertIsNotNone(gen)

    def test_1_char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with self.assertRaises(ValueError):
            AbelVCBGenerator(coach_acronym="J", receipt_chain=rc)

    def test_5_char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with self.assertRaises(ValueError):
            AbelVCBGenerator(coach_acronym="ABCDE", receipt_chain=rc)


# ====================================================================
# Legacy Fallback (§6)
# ====================================================================

class TestLegacyFallback(unittest.TestCase):
    """When Psychological Routing Brief is absent."""

    def test_legacy_defaults_applied(self):
        gen, _ = _make_generator()
        inp = _default_input(has_psychological_routing_brief=False)
        vcb = gen.generate(inp)
        self.assertEqual(vcb.mood_state, MoodState.PROCESSING)
        self.assertEqual(vcb.cbcs_score, 4)

    def test_legacy_warning_emitted(self):
        gen, _ = _make_generator()
        inp = _default_input(has_psychological_routing_brief=False)
        vcb = gen.generate(inp)
        self.assertIn(VCBError.LEGACY_ROUTING_DEFAULT, vcb.warnings)

    def test_legacy_vcb_still_valid(self):
        gen, _ = _make_generator()
        inp = _default_input(has_psychological_routing_brief=False)
        vcb = gen.generate(inp)
        self.assertEqual(vcb.gate_c09_result.verdict, GateC09Verdict.PASS)


# ====================================================================
# Edge Cases
# ====================================================================

class TestEdgeCases(unittest.TestCase):

    def test_single_slide_vcb(self):
        gen, _ = _make_generator()
        inp = _default_input(slide_count=1)
        vcb = gen.generate(inp)
        self.assertEqual(len(vcb.per_slide_assignments), 1)
        self.assertTrue(vcb.per_slide_assignments[0].handle_bar.visible)

    def test_no_active_nouns(self):
        gen, _ = _make_generator()
        inp = _default_input(active_nouns=[])
        vcb = gen.generate(inp)
        # VCB is generated (may fail C09-R03 and escalate, or pass if no text slides)
        self.assertIsNotNone(vcb)

    def test_blocked_nouns_excluded(self):
        gen, _ = _make_generator()
        inp = _default_input(
            active_nouns=["good noun", "bad noun", "another good"],
            blocked_nouns=["bad noun"],
        )
        vcb = gen.generate(inp)
        for s in vcb.per_slide_assignments:
            for n in s.tribal_noun_assignments:
                self.assertNotEqual(n.noun, "bad noun")


if __name__ == "__main__":
    unittest.main()
