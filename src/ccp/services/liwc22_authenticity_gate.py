"""
CCP LIWC-22 7-Factor Authenticity Gate — FR2 Unit 2
Implements the 7-marker authenticity scoring per FR2 Tech Spec §Stage D.

Spec reference: FR2 Tech Spec §Stage D — 7-Factor LIWC-22 Authenticity Gate
Architecture reference: §11.5 (Quality Gates), §10.6 (Audio Pipeline)
Stress test reference: Q32 — Authenticity Floor Calibration (authentic_multiplier)

Each Thought_Unit is independently scored on 7 markers:
1. First-Person Singular (elevated I/me/my)
2. Exclusive Words (but/except/without density)
3. Absence of Hedging (zero maybe/perhaps/I think)
4. Sentence Compression (reduced WPS ratio)
5. Verb Tense Distribution (Simple Present spike)
6. Filler Frequency (natural um/uh distribution)
7. Discourse Marker Position (mid-sentence, not sentence-opening)

Score = count of markers in-range / 7.
All 7 markers must be within authentic range for AUTHENTIC status.
Per-coach calibration via authentic_multiplier (Q32).
"""

import re
from typing import Optional

from src.ccp.models.sacred_audio_models import (
    AuthenticityMarker,
    AuthenticityScore,
    AuthenticityStatus,
    MarkerResult,
    ThoughtUnit,
)


# ──────────────────────────────────────────────────────────────
# Word lists for marker evaluation
# Spec: §Stage D marker table — exact word categories
# ──────────────────────────────────────────────────────────────

# Marker 1: First-Person Singular
FPS_WORDS = {"i", "me", "my", "mine", "myself", "i'm", "i've", "i'd", "i'll"}

# Marker 2: Exclusive Words
EXCLUSIVE_WORDS = {"but", "except", "without", "however", "although", "though", "unless", "yet", "nevertheless"}

# Marker 3: Hedging Words (inverse: high hedging = OUT of range)
HEDGING_WORDS = {"maybe", "perhaps", "i think", "i believe", "kind of", "sort of", "i guess", "probably", "possibly", "might"}

# Marker 5: Present tense indicators
PRESENT_TENSE_MARKERS = {"is", "are", "am", "do", "does", "have", "has", "feel", "see", "know", "want", "need", "get"}
PAST_TENSE_MARKERS = {"was", "were", "did", "had", "felt", "saw", "knew", "wanted", "needed", "got", "went", "said", "told", "made", "came"}

# Marker 6: Filler words
FILLER_WORDS = {"um", "uh", "hmm", "uhh", "umm", "eh", "er", "ah"}

# Marker 7: Discourse markers
DISCOURSE_MARKERS = {"actually", "so", "look", "well", "you know", "i mean", "basically", "honestly", "right", "like", "okay"}


# ──────────────────────────────────────────────────────────────
# Default thresholds (calibrated by authentic_multiplier)
# ──────────────────────────────────────────────────────────────

# These are the baseline thresholds for a "typical" coach.
# The authentic_multiplier from Q32 scales these downward for stoic coaches.

DEFAULT_THRESHOLDS = {
    # Marker 1: FPS ratio (proportion of FPS words to total words)
    # Authentic: elevated FPS. Threshold: ≥5% of words are FPS.
    AuthenticityMarker.FIRST_PERSON_SINGULAR: {"min": 0.05, "max": 1.0},

    # Marker 2: Exclusive word density
    # Authentic: high density. Threshold: ≥1.5% of words are exclusive.
    AuthenticityMarker.EXCLUSIVE_WORDS: {"min": 0.015, "max": 1.0},

    # Marker 3: Hedging ratio (INVERSE — low is good)
    # Authentic: near-zero. Threshold: ≤2% of words are hedging.
    AuthenticityMarker.ABSENCE_OF_HEDGING: {"min": 0.0, "max": 0.02},

    # Marker 4: Words per sentence (WPS) — lower = more compressed
    # Authentic: reduced WPS. Threshold: ≤18 WPS.
    AuthenticityMarker.SENTENCE_COMPRESSION: {"min": 0.0, "max": 18.0},

    # Marker 5: Present tense ratio (present / (present + past))
    # Authentic: spike in present. Threshold: ≥55% present tense.
    AuthenticityMarker.VERB_TENSE_DISTRIBUTION: {"min": 0.55, "max": 1.0},

    # Marker 6: Filler frequency (fillers per 100 words)
    # Authentic: natural distribution (0.5 - 8.0 per 100 words).
    # Zero = scripted. Extreme = anxiety.
    AuthenticityMarker.FILLER_FREQUENCY: {"min": 0.5, "max": 8.0},

    # Marker 7: Discourse marker position ratio (mid-sentence / total discourse markers)
    # Authentic: mid-sentence. Threshold: ≥40% mid-sentence.
    AuthenticityMarker.DISCOURSE_MARKER_POSITION: {"min": 0.40, "max": 1.0},
}


class LIWC22AuthenticityGate:
    """7-Factor LIWC-22 Authenticity Gate for Sacred Audio Thought Units.

    Spec: 'Each Thought_Unit is independently scored on 7 markers.
    Score = count of markers in-range / 7. Minimum passing score:
    ≥7/10 (i.e., all 7 markers must be within authentic range).'

    Stress test Q32: Per-coach authentic_multiplier calibration.
    If a stoic coach's authentic_multiplier is 0.7, thresholds are
    scaled to accommodate their natural expression level.
    """

    def __init__(
        self,
        authentic_multiplier: float = 1.0,
        coach_filler_baseline: Optional[float] = None,
    ):
        """Initialize the gate with per-coach calibration.

        Args:
            authentic_multiplier: From genesis_certificate.authentic_multiplier.
                Scales minimum thresholds downward for stoic coaches (Q32).
                Default 1.0 = standard thresholds apply.
            coach_filler_baseline: Optional per-coach filler frequency baseline.
                If provided, Marker 6 uses this as the center of the acceptable range.
        """
        self.authentic_multiplier = authentic_multiplier
        self.coach_filler_baseline = coach_filler_baseline
        self.thresholds = self._calibrate_thresholds()

    def _calibrate_thresholds(self) -> dict[AuthenticityMarker, dict[str, float]]:
        """Apply authentic_multiplier to default thresholds.

        Stress test Q32: 'the orchestration pipeline algorithmic floor
        dynamically and permanently adjusts downward.'

        The multiplier scales the MINIMUM requirements for markers where
        higher values indicate authenticity (FPS, exclusive words, present tense,
        discourse position). For inverted markers (hedging, WPS), the multiplier
        scales the MAXIMUM upward (more lenient).
        """
        calibrated = {}

        for marker, bounds in DEFAULT_THRESHOLDS.items():
            new_bounds = dict(bounds)

            if marker == AuthenticityMarker.ABSENCE_OF_HEDGING:
                # Inverted: max threshold scales up (more lenient) with lower multiplier
                new_bounds["max"] = bounds["max"] / self.authentic_multiplier
            elif marker == AuthenticityMarker.SENTENCE_COMPRESSION:
                # Inverted: max WPS scales up (more lenient) with lower multiplier
                new_bounds["max"] = bounds["max"] / self.authentic_multiplier
            elif marker == AuthenticityMarker.FILLER_FREQUENCY:
                # Special: if coach baseline exists, center around it
                if self.coach_filler_baseline is not None:
                    half_range = 3.0
                    new_bounds["min"] = max(0.0, self.coach_filler_baseline - half_range)
                    new_bounds["max"] = self.coach_filler_baseline + half_range
                else:
                    # Scale minimum down for stoic coaches
                    new_bounds["min"] = bounds["min"] * self.authentic_multiplier
            else:
                # Standard: minimum scales down with lower multiplier (more lenient)
                new_bounds["min"] = bounds["min"] * self.authentic_multiplier

            calibrated[marker] = new_bounds

        return calibrated

    def evaluate(self, unit: ThoughtUnit) -> AuthenticityScore:
        """Score a ThoughtUnit on all 7 markers.

        Spec: 'FOR EACH Thought_Unit: score = evaluate_7_markers(unit.text)
        IF score.pass_count >= 7: unit.status = "AUTHENTIC"
        ELSE: unit.status = "SYNTHETIC_CANDIDATE"'

        Returns:
            AuthenticityScore with all 7 marker results and final status.
        """
        text = unit.text
        words = text.lower().split()
        total_words = len(words)

        if total_words == 0:
            # Empty unit fails all markers
            return self._empty_score(unit.unit_id)

        marker_results = [
            self._evaluate_fps(words, total_words),
            self._evaluate_exclusive(words, total_words),
            self._evaluate_hedging(text, total_words),
            self._evaluate_sentence_compression(text, total_words),
            self._evaluate_verb_tense(words),
            self._evaluate_filler_frequency(words, total_words),
            self._evaluate_discourse_position(text),
        ]

        return AuthenticityScore(
            unit_id=unit.unit_id,
            marker_results=marker_results,
            authentic_multiplier=self.authentic_multiplier,
        )

    # ──────────────────────────────────────────────────────────
    # Marker 1: First-Person Singular
    # Spec: "Elevated I/me/my — demonstrated ownership of experience"
    # ──────────────────────────────────────────────────────────

    def _evaluate_fps(self, words: list[str], total_words: int) -> MarkerResult:
        fps_count = sum(1 for w in words if w in FPS_WORDS)
        ratio = fps_count / total_words
        bounds = self.thresholds[AuthenticityMarker.FIRST_PERSON_SINGULAR]

        return MarkerResult(
            marker=AuthenticityMarker.FIRST_PERSON_SINGULAR,
            in_range=ratio >= bounds["min"],
            value=round(ratio, 4),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{fps_count} FPS words in {total_words} total ({ratio:.2%})",
        )

    # ──────────────────────────────────────────────────────────
    # Marker 2: Exclusive Words
    # Spec: "High density of but/except/without"
    # ──────────────────────────────────────────────────────────

    def _evaluate_exclusive(self, words: list[str], total_words: int) -> MarkerResult:
        exc_count = sum(1 for w in words if w in EXCLUSIVE_WORDS)
        ratio = exc_count / total_words
        bounds = self.thresholds[AuthenticityMarker.EXCLUSIVE_WORDS]

        return MarkerResult(
            marker=AuthenticityMarker.EXCLUSIVE_WORDS,
            in_range=ratio >= bounds["min"],
            value=round(ratio, 4),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{exc_count} exclusive words in {total_words} total ({ratio:.2%})",
        )

    # ──────────────────────────────────────────────────────────
    # Marker 3: Absence of Hedging
    # Spec: "Zero or near-zero maybe/perhaps/I think/I believe/kind of"
    # INVERSE marker: low hedging = authentic
    # ──────────────────────────────────────────────────────────

    def _evaluate_hedging(self, text: str, total_words: int) -> MarkerResult:
        text_lower = text.lower()
        hedge_count = 0
        for phrase in HEDGING_WORDS:
            # Count multi-word phrases properly
            if " " in phrase:
                hedge_count += text_lower.count(phrase)
            else:
                hedge_count += text_lower.split().count(phrase)

        ratio = hedge_count / total_words if total_words > 0 else 0.0
        bounds = self.thresholds[AuthenticityMarker.ABSENCE_OF_HEDGING]

        return MarkerResult(
            marker=AuthenticityMarker.ABSENCE_OF_HEDGING,
            in_range=ratio <= bounds["max"],
            value=round(ratio, 4),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{hedge_count} hedging instances in {total_words} words ({ratio:.2%})",
        )

    # ──────────────────────────────────────────────────────────
    # Marker 4: Sentence Compression
    # Spec: "Reduced WPS ratio — short burst sentences indicating emotional urgency"
    # INVERSE marker: lower WPS = authentic
    # ──────────────────────────────────────────────────────────

    def _evaluate_sentence_compression(self, text: str, total_words: int) -> MarkerResult:
        # Split on sentence-ending punctuation
        sentences = re.split(r'[.!?]+', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = max(len(sentences), 1)

        wps = total_words / sentence_count
        bounds = self.thresholds[AuthenticityMarker.SENTENCE_COMPRESSION]

        return MarkerResult(
            marker=AuthenticityMarker.SENTENCE_COMPRESSION,
            in_range=wps <= bounds["max"],
            value=round(wps, 2),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{total_words} words / {sentence_count} sentences = {wps:.1f} WPS",
        )

    # ──────────────────────────────────────────────────────────
    # Marker 5: Verb Tense Distribution
    # Spec: "Spike in Simple Present ('it IS' not 'it WAS') — Figural Deictic Present"
    # ──────────────────────────────────────────────────────────

    def _evaluate_verb_tense(self, words: list[str]) -> MarkerResult:
        present_count = sum(1 for w in words if w in PRESENT_TENSE_MARKERS)
        past_count = sum(1 for w in words if w in PAST_TENSE_MARKERS)
        total_tense = present_count + past_count

        if total_tense == 0:
            # No tense markers found — cannot evaluate, pass by default
            return MarkerResult(
                marker=AuthenticityMarker.VERB_TENSE_DISTRIBUTION,
                in_range=True,
                value=0.5,
                detail="No tense markers detected — default pass",
            )

        present_ratio = present_count / total_tense
        bounds = self.thresholds[AuthenticityMarker.VERB_TENSE_DISTRIBUTION]

        return MarkerResult(
            marker=AuthenticityMarker.VERB_TENSE_DISTRIBUTION,
            in_range=present_ratio >= bounds["min"],
            value=round(present_ratio, 4),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{present_count} present / {past_count} past = {present_ratio:.2%} present",
        )

    # ──────────────────────────────────────────────────────────
    # Marker 6: Filler Frequency
    # Spec: "Natural distribution of um/uh matching coach's established baseline"
    # "Zero fillers → scripted/curated; extreme fillers → anxiety"
    # ──────────────────────────────────────────────────────────

    def _evaluate_filler_frequency(self, words: list[str], total_words: int) -> MarkerResult:
        filler_count = sum(1 for w in words if w in FILLER_WORDS)
        fillers_per_100 = (filler_count / total_words) * 100 if total_words > 0 else 0.0
        bounds = self.thresholds[AuthenticityMarker.FILLER_FREQUENCY]

        return MarkerResult(
            marker=AuthenticityMarker.FILLER_FREQUENCY,
            in_range=bounds["min"] <= fillers_per_100 <= bounds["max"],
            value=round(fillers_per_100, 2),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{filler_count} fillers in {total_words} words = {fillers_per_100:.1f} per 100",
        )

    # ──────────────────────────────────────────────────────────
    # Marker 7: Discourse Marker Position
    # Spec: "Transitions (actually, so, look) at mid-sentence, not sentence-opening"
    # ──────────────────────────────────────────────────────────

    def _evaluate_discourse_position(self, text: str) -> MarkerResult:
        # Split into sentences
        sentences = re.split(r'[.!?]+', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]

        total_markers = 0
        mid_sentence_markers = 0

        for sentence in sentences:
            words_in_sentence = sentence.lower().split()
            if len(words_in_sentence) < 2:
                continue

            for marker_phrase in DISCOURSE_MARKERS:
                marker_words = marker_phrase.split()
                marker_len = len(marker_words)

                for idx in range(len(words_in_sentence) - marker_len + 1):
                    window = words_in_sentence[idx:idx + marker_len]
                    # Strip punctuation for comparison
                    window_clean = [re.sub(r'[,;:]', '', w) for w in window]
                    if window_clean == marker_words:
                        total_markers += 1
                        # Mid-sentence = not at position 0
                        if idx > 0:
                            mid_sentence_markers += 1

        if total_markers == 0:
            # No discourse markers — cannot evaluate, pass by default
            return MarkerResult(
                marker=AuthenticityMarker.DISCOURSE_MARKER_POSITION,
                in_range=True,
                value=0.5,
                detail="No discourse markers detected — default pass",
            )

        mid_ratio = mid_sentence_markers / total_markers
        bounds = self.thresholds[AuthenticityMarker.DISCOURSE_MARKER_POSITION]

        return MarkerResult(
            marker=AuthenticityMarker.DISCOURSE_MARKER_POSITION,
            in_range=mid_ratio >= bounds["min"],
            value=round(mid_ratio, 4),
            threshold_low=bounds["min"],
            threshold_high=bounds["max"],
            detail=f"{mid_sentence_markers}/{total_markers} markers mid-sentence ({mid_ratio:.2%})",
        )

    # ──────────────────────────────────────────────────────────
    # Helper: empty unit score (all fail)
    # ──────────────────────────────────────────────────────────

    def _empty_score(self, unit_id: str) -> AuthenticityScore:
        """Generate a failing score for an empty thought unit."""
        results = []
        for marker in AuthenticityMarker:
            results.append(MarkerResult(
                marker=marker,
                in_range=False,
                value=0.0,
                detail="Empty unit — automatic fail",
            ))
        return AuthenticityScore(
            unit_id=unit_id,
            marker_results=results,
            authentic_multiplier=self.authentic_multiplier,
        )
