"""Unit tests — CrusadeNarrativeAudit Pydantic validator (Phase5-M03).
§10.1: test_crusade_narrative_validator.py."""
import pytest
from src.ccp.models.ofo_models import CrusadeNarrativeAudit


class TestCrusadeNarrativeValidatorAccepts:
    """Valid transcripts with required themes pass validation."""

    def test_valid_with_algorithm_and_compression(self):
        audit = CrusadeNarrativeAudit(
            transcript="The algorithm has been compressing your natural authority and flattening your legacy.",
            detected_flaw="Embodied Confidence", biometric_score=3.2,
        )
        assert "algorithm" in audit.transcript.lower()

    def test_valid_with_defend_and_protect(self):
        audit = CrusadeNarrativeAudit(
            transcript="We defend your coaching legacy against systematic erosion. We protect what makes you irreplaceable.",
            detected_flaw="Vocal Resonance", biometric_score=4.5,
        )
        assert audit.detected_flaw == "Vocal Resonance"

    def test_valid_with_flattening_and_legacy(self):
        audit = CrusadeNarrativeAudit(
            transcript="Platform flattening destroys the nuance of your legacy and your unique vocal signature.",
            detected_flaw="Narrative Authority", biometric_score=6.0,
        )
        assert audit.biometric_score == 6.0


class TestCrusadeNarrativeValidatorRejects:
    """Invalid transcripts with forbidden words or missing themes are rejected."""

    def test_poor_is_rejected(self):
        with pytest.raises(ValueError, match="forbidden clinical critique"):
            CrusadeNarrativeAudit(
                transcript="Your embodied confidence is poor. The algorithm compresses your legacy.",
                detected_flaw="Embodied Confidence", biometric_score=3.0,
            )

    def test_weak_is_rejected(self):
        with pytest.raises(ValueError, match="forbidden clinical critique"):
            CrusadeNarrativeAudit(
                transcript="Your vocal presence is weak. Algorithm compression flattens your legacy.",
                detected_flaw="Vocal Resonance", biometric_score=2.5,
            )

    def test_bad_is_rejected(self):
        with pytest.raises(ValueError, match="forbidden clinical critique"):
            CrusadeNarrativeAudit(
                transcript="This is a bad performance. Algorithm flattening erodes your legacy.",
                detected_flaw="General", biometric_score=4.0,
            )

    def test_needs_improvement_is_rejected(self):
        with pytest.raises(ValueError, match="forbidden clinical critique"):
            CrusadeNarrativeAudit(
                transcript="Your confidence needs improvement. The algorithm compresses your legacy.",
                detected_flaw="Embodied Confidence", biometric_score=3.5,
            )

    def test_inadequate_is_rejected(self):
        with pytest.raises(ValueError, match="forbidden clinical critique"):
            CrusadeNarrativeAudit(
                transcript="Your delivery is inadequate. The algorithm flattens your legacy.",
                detected_flaw="General", biometric_score=4.0,
            )

    def test_missing_themes_is_rejected(self):
        with pytest.raises(ValueError, match="Crusade Narrative mandate"):
            CrusadeNarrativeAudit(
                transcript="You have great potential and your coaching style is unique and powerful.",
                detected_flaw="General", biometric_score=7.0,
            )

    def test_only_one_theme_is_rejected(self):
        with pytest.raises(ValueError, match="Crusade Narrative mandate"):
            CrusadeNarrativeAudit(
                transcript="The algorithm is changing how content is consumed globally.",
                detected_flaw="General", biometric_score=5.0,
            )
