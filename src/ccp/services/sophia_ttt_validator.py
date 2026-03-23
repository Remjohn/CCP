"""
CCP FR8 TTT Enforcement Rule — Sophia TTT Validator (Unit 6)
Post-generation TTT drift validation by Sophia (Minister of Identity).

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md §Layer 4: Post-Generation Verification
                §Sophia Validation checks:
                  - TTT Drift < 15% from DEP-ENG-005 baseline (after model offset)
                  - Cosine similarity ≥ 0.85 against ttt_baseline.json
                  - iRAV-inspired ≥1 emotional peak exceeding average by ≥20% per script

Model Offset Calibration:
  Sophia applies the global model offset BEFORE calculating drift threshold.
  E.g., Groq: -0.12 → baseline shifted -0.12 before drift check.
  Prevents false-positive rejections from LLM architecture temperature variance.

AC9:  TTT drift > 15% → Sophia DRIFT_EXCEEDED. Drift ≤ 15% → PASS.
AC10: ≥1 emotional peak exceeds average by ≥20% per script → PASS. Zero peaks → FLAT_EMOTIONAL_ARC.
"""

import math
from typing import Any, Optional

from src.ccp.models.ttt_models import (
    EmotionalPeak,
    SophiaDriftVerdict,
    SophiaTTTValidationResult,
    TTTBaselineData,
)
from src.ccp.services.ttt_pattern_registry import get_model_offset

# ─── Sophia Validation Constants ──────────────────────────────────────────────

DRIFT_THRESHOLD: float = 0.15          # < 15% — AC9
SIMILARITY_THRESHOLD: float = 0.85     # ≥ 0.85 cosine similarity
PEAK_EXCEEDANCE_THRESHOLD: float = 0.20  # ≥ 20% above average — AC10


class SophiaTTTValidator:
    """Sophia (Minister of Identity) post-generation TTT drift validation.

    Spec §Layer 4 Post-Generation Verification:
    After content is generated, Sophia validates the produced content's
    emotional register is consistent with the DEP-ENG-005 authentication.

    This validator:
    1. Applies model offset calibration (Spec §Model Offset Calibration Registry)
    2. Calculates TTT drift from authenticated baseline (AC9)
    3. Computes cosine similarity of emotional markers
    4. Detects iRAV-inspired emotional peaks (AC10)
    5. Returns a SophiaTTTValidationResult

    Note: The "generated_content_analysis" dict is expected to contain LIWC-22-style
    emotional markers extracted from the generated content — the same format as the
    voice note analysis used to produce the TTT baseline.
    """

    def validate(
        self,
        baseline: TTTBaselineData,
        generated_content_analysis: dict[str, Any],
        compilation_id: str,
        model_id: Optional[str] = None,
    ) -> SophiaTTTValidationResult:
        """Validate generated content against the TTT baseline.

        Args:
            baseline: The DEP-ENG-005 TTT baseline from the production session.
            generated_content_analysis: LIWC-22 analysis of the generated content.
            compilation_id: The JIT compilation ID.
            model_id: The executing LLM model ID for offset calibration.

        Returns:
            SophiaTTTValidationResult with verdict and all check details.
        """
        # Step 1: Model offset calibration (Spec §Layer 4)
        model_offset = get_model_offset(model_id or "gpt-4")

        # Step 2: TTT drift check (AC9)
        drift_pct, drift_passed = self._check_drift(
            baseline=baseline,
            content_analysis=generated_content_analysis,
            model_offset=model_offset,
        )

        # Step 3: Cosine similarity check
        cosine_sim, similarity_passed = self._check_cosine_similarity(
            baseline=baseline,
            content_analysis=generated_content_analysis,
        )

        # Step 4: iRAV emotional peak detection (AC10)
        peaks, avg_intensity, peaks_passed = self._check_emotional_peaks(
            content_analysis=generated_content_analysis,
        )

        # Step 5: Determine overall verdict
        verdict = self._determine_verdict(drift_passed, similarity_passed, peaks_passed)

        return SophiaTTTValidationResult(
            verdict=verdict,
            compilation_id=compilation_id,
            session_id=baseline.session_id,
            ttt_drift_percentage=drift_pct,
            drift_threshold=DRIFT_THRESHOLD,
            drift_passed=drift_passed,
            cosine_similarity=cosine_sim,
            similarity_threshold=SIMILARITY_THRESHOLD,
            similarity_passed=similarity_passed,
            emotional_peaks=peaks,
            average_intensity=avg_intensity,
            peaks_passed=peaks_passed,
            peak_threshold_pct=PEAK_EXCEEDANCE_THRESHOLD,
            model_id=model_id,
            model_offset_applied=model_offset,
        )

    def _check_drift(
        self,
        baseline: TTTBaselineData,
        content_analysis: dict[str, Any],
        model_offset: float,
    ) -> tuple[float, bool]:
        """Calculate TTT drift from baseline after applying model offset.

        Spec §Layer 4: "Sophia mathematically shifts the coach's TTT baseline by
        this offset *before* calculating the <15% drift threshold."

        Args:
            baseline: DEP-ENG-005 TTT baseline (Temperature 1-10).
            content_analysis: LIWC-22 analysis of generated content.
            model_offset: LLM architecture temperature offset (-0.12 for Groq, etc.)

        Returns:
            Tuple of (drift_percentage: float, passed: bool).
        """
        # Normalized baseline temperature (1-10 → 0.0-1.0)
        baseline_normalized = (baseline.temperature - 1) / 9.0

        # Apply model offset to baseline (Spec §Layer 4)
        adjusted_baseline = max(0.0, min(1.0, baseline_normalized + model_offset))

        # Extract content temperature from LIWC analysis
        content_affect = float(content_analysis.get("affect", 0.0))
        content_clout = float(content_analysis.get("clout", 50.0))
        content_temperature = (
            min(content_affect / 15.0, 1.0) * 0.6 +
            (content_clout / 100.0) * 0.4
        )

        # Calculate drift as absolute difference from adjusted baseline
        drift = abs(content_temperature - adjusted_baseline)

        return drift, drift < DRIFT_THRESHOLD

    def _check_cosine_similarity(
        self,
        baseline: TTTBaselineData,
        content_analysis: dict[str, Any],
    ) -> tuple[float, bool]:
        """Compute cosine similarity of content emotional markers vs TTT baseline.

        Spec §Layer 4: "Register Consistency: TTT cosine similarity against ttt_baseline.json"
        Threshold: ≥ 0.85

        Args:
            baseline: DEP-ENG-005 TTT baseline.
            content_analysis: LIWC-22 analysis of generated content.

        Returns:
            Tuple of (cosine_similarity: float [0.0-1.0], passed: bool).
        """
        # Build feature vectors from LIWC markers
        # Use consistent set of emotional marker dimensions
        LIWC_DIMENSIONS = [
            "affect", "posemo", "negemo", "social", "insight",
            "cogmech", "clout", "authentic", "anger", "achieve"
        ]

        # Baseline vector: constructed from baseline data
        baseline_vector = self._baseline_to_vector(baseline, LIWC_DIMENSIONS)

        # Content vector: extracted from content LIWC analysis
        content_vector = [
            float(content_analysis.get(dim, 0.0)) for dim in LIWC_DIMENSIONS
        ]

        cosine_sim = self._cosine_similarity(baseline_vector, content_vector)
        return cosine_sim, cosine_sim >= SIMILARITY_THRESHOLD

    def _check_emotional_peaks(
        self,
        content_analysis: dict[str, Any],
    ) -> tuple[list[EmotionalPeak], float, bool]:
        """Detect iRAV-inspired emotional peaks in generated content.

        Spec §Layer 4 iRAV-inspired peak detection:
        "≥1 emotional peak exceeding the average by ≥20% in each script"

        Args:
            content_analysis: LIWC-22 analysis of generated content. Should contain
                              either a 'segment_intensities' list or per-paragraph
                              LIWC scores.

        Returns:
            Tuple of (peaks: list[EmotionalPeak], avg_intensity: float, passed: bool).
        """
        # Extract segment-level intensities if available
        # FR2 processes voice note by paragraph/segment, producing per-segment affect
        segment_intensities = content_analysis.get("segment_intensities", [])

        if not segment_intensities:
            # Fallback: single overall intensity from top-level affect score
            overall_affect = float(content_analysis.get("affect", 0.0))
            overall_intensity = min(overall_affect / 15.0, 1.0)
            segment_intensities = [overall_intensity]

        # Normalize to [0.0, 1.0]
        normalized = [min(max(float(v), 0.0), 1.0) for v in segment_intensities]

        avg_intensity = sum(normalized) / len(normalized) if normalized else 0.0
        peak_threshold = avg_intensity * (1.0 + PEAK_EXCEEDANCE_THRESHOLD)

        peaks: list[EmotionalPeak] = []
        for idx, intensity in enumerate(normalized):
            if intensity >= peak_threshold:
                peaks.append(EmotionalPeak(
                    position_index=idx,
                    intensity=intensity,
                ))

        # AC10: ≥1 peak must exceed average by ≥20%
        peaks_passed = len(peaks) >= 1

        return peaks, avg_intensity, peaks_passed

    def _determine_verdict(
        self,
        drift_passed: bool,
        similarity_passed: bool,
        peaks_passed: bool,
    ) -> SophiaDriftVerdict:
        """Determine the overall Sophia validation verdict.

        Priority order (first failure wins):
        1. Drift exceeded → DRIFT_EXCEEDED (AC9)
        2. Similarity failed → SIMILARITY_FAILED
        3. Flat emotional arc → FLAT_EMOTIONAL_ARC (AC10)
        4. All passed → PASS
        """
        if not drift_passed:
            return SophiaDriftVerdict.DRIFT_EXCEEDED
        if not similarity_passed:
            return SophiaDriftVerdict.SIMILARITY_FAILED
        if not peaks_passed:
            return SophiaDriftVerdict.FLAT_EMOTIONAL_ARC
        return SophiaDriftVerdict.PASS

    # ─── Vector Helpers ────────────────────────────────────────────────────────

    def _baseline_to_vector(
        self, baseline: TTTBaselineData, dimensions: list[str]
    ) -> list[float]:
        """Convert TTT baseline to a LIWC-comparable feature vector.

        Maps TTTBaselineData fields to approximate LIWC dimension values
        for cosine similarity computation.
        """
        # Map temperature (1-10) to approximate affect score (0-30)
        approx_affect = (baseline.temperature - 1) * (30 / 9)

        # Map texture to analytic score (RAW→20, LITERARY→80)
        texture_map = {
            "raw": 20.0,
            "colloquial": 35.0,
            "conversational": 50.0,
            "polished": 65.0,
            "literary": 80.0,
        }
        approx_analytic = texture_map.get(baseline.texture.value, 50.0)

        # Map tone to posemo/negemo/clout split
        tone_posemo: dict[str, float] = {
            "nurturing": 8.0, "instructional": 4.0,
            "reflective": 3.0, "confrontational": 1.0,
            "declarative": 3.5, "questioning": 3.0,
            "celebratory": 9.0, "grieving": 2.0,
        }
        tone_negemo: dict[str, float] = {
            "nurturing": 1.0, "instructional": 1.5,
            "reflective": 2.0, "confrontational": 6.0,
            "declarative": 2.0, "questioning": 2.5,
            "celebratory": 0.5, "grieving": 5.0,
        }
        approx_posemo = tone_posemo.get(baseline.tone.value, 4.0)
        approx_negemo = tone_negemo.get(baseline.tone.value, 2.0)
        approx_clout = 50.0 + (baseline.temperature - 5) * 4.0  # Higher temp = higher clout

        vector_map: dict[str, float] = {
            "affect": approx_affect,
            "posemo": approx_posemo,
            "negemo": approx_negemo,
            "social": 5.0,
            "insight": 3.0 if baseline.tone.value == "reflective" else 1.5,
            "cogmech": 4.0 if baseline.tone.value in ("reflective", "instructional") else 2.0,
            "clout": approx_clout,
            "authentic": baseline.liwc_authenticity_score,
            "anger": 3.0 if baseline.tone.value == "confrontational" else 0.5,
            "achieve": 4.0 if baseline.tone.value == "instructional" else 1.5,
        }

        return [vector_map.get(dim, 0.0) for dim in dimensions]

    @staticmethod
    def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
        """Compute cosine similarity between two equal-length vectors.

        Returns 0.0 if either vector has zero magnitude.
        """
        if len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = math.sqrt(sum(a * a for a in vec_a))
        magnitude_b = math.sqrt(sum(b * b for b in vec_b))

        if magnitude_a == 0.0 or magnitude_b == 0.0:
            return 0.0

        # Clamp to [0.0, 1.0] for numerical stability
        return max(0.0, min(1.0, dot_product / (magnitude_a * magnitude_b)))
