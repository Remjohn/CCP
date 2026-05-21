"""Unit tests — CrusadeNarrativeFitter deterministic fallback (Phase5-M03).
§10.2: test_crusade_narrative_fitter.py."""
from src.ccp.services.crusade_narrative_fitter import CrusadeNarrativeFitter
from src.ccp.models.ofo_models import CRUSADE_FALLBACK_TEMPLATES


class MockLLMBadOutput:
    """LLM that always returns Phase5-M03 violating text."""
    def generate(self, prompt):
        return "Your coaching is poor and weak. You need improvement badly."


class MockLLMGoodOutput:
    """LLM that returns valid Crusade Narrative text."""
    def generate(self, prompt):
        return (
            "The algorithm has been compressing your natural authority and flattening "
            "the qualities that define your coaching legacy. We defend your presence "
            "against this systematic erosion and protect what makes you irreplaceable."
        )


class TestFitterDeterministicFallback:
    """When LLM fails Phase5-M03, deterministic templates engage."""

    def test_bad_llm_falls_back_to_deterministic(self):
        fitter = CrusadeNarrativeFitter(llm_client=MockLLMBadOutput())
        audit = fitter.apply_framing(detected_flaw="Embodied Confidence", biometric_score=3.2)
        assert "algorithm" in audit.transcript.lower() or "compression" in audit.transcript.lower()
        assert "poor" not in audit.transcript.lower()
        assert "weak" not in audit.transcript.lower()

    def test_good_llm_passes_directly(self):
        fitter = CrusadeNarrativeFitter(llm_client=MockLLMGoodOutput())
        audit = fitter.apply_framing(detected_flaw="Vocal Resonance", biometric_score=4.5)
        assert "algorithm" in audit.transcript.lower()
        assert audit.detected_flaw == "Vocal Resonance"

    def test_no_llm_uses_deterministic(self):
        fitter = CrusadeNarrativeFitter(llm_client=None)
        audit = fitter.apply_framing(detected_flaw="Embodied Confidence", biometric_score=3.0)
        assert audit.transcript == CRUSADE_FALLBACK_TEMPLATES["embodied_confidence"]

    def test_unknown_flaw_uses_default_template(self):
        fitter = CrusadeNarrativeFitter(llm_client=None)
        audit = fitter.apply_framing(detected_flaw="Unknown Metric XYZ", biometric_score=5.0)
        assert audit.transcript == CRUSADE_FALLBACK_TEMPLATES["default"]


class TestFitterBaselineDiscovery:
    """When audio quality is too poor, Baseline Discovery path activates."""

    def test_baseline_discovery_transcript(self):
        fitter = CrusadeNarrativeFitter()
        audit = fitter.apply_baseline_discovery()
        assert "compression" in audit.transcript.lower()
        assert "baseline" in audit.transcript.lower()
        assert audit.detected_flaw == "Insufficient Audio Signal"
        assert audit.biometric_score == 0.0
