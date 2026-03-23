"""
CCP FR6 — Depth Stratifier (Phase B2) (Unit 3)
L1/L2/L3 depth classification with LIWC-22 authenticity scoring.

Spec reference: FR6 Tech Spec §Phase B2
  L1 = Public Statements (performative broadcast, high self-monitoring)
  L2 = Private Struggles (communal in-group disclosure, guarded)
  L3 = Unspoken Feelings (authentic anonymous disinhibition, 2am test)

Hard gate: L2 ≥30% AND L3 ≥10%. L1-dominant profile CANNOT feed
the Trigger Matching Layer.

Research basis:
  Clark & Brennan Common Ground Theory (1991)
  Tubbs et al. Mind After Midnight (2022)
  Suler Online Disinhibition (2004)
  Pennebaker LIWC-22 (2015)
  Newman et al. Lying Words (2003)
"""

from collections.abc import Sequence
from typing import Any, Optional, Protocol

from src.ccp.models.tribe_profile_models import (
    DepthDistribution,
    DepthLevel,
    DepthStratifiedEntry,
)


class LiwcScorerProtocol(Protocol):
    """Protocol for LIWC-22 authenticity scoring.
    External dependency — injected at runtime."""

    def score_authenticity(self, text: str) -> float:
        """Return LIWC-22 authenticity percentile (0.0–1.0)."""
        ...


class DefaultLiwcScorer:
    """Default LIWC-22 scorer using heuristic markers.

    In production, replaced by actual LIWC-22 library.
    Uses Pennebaker (2015) and Newman et al. (2003) marker heuristics:
    - L3 markers: high personal pronouns (I/me/my), lower cognitive complexity,
      increased negative emotion words, narrative style
    - L1 markers: low personal pronouns, managed emotions, polished/formal style,
      high social monitoring
    """

    # LIWC-22 L3 markers (Mind After Midnight)
    L3_MARKERS = [
        "i ", "i'm", "i've", "i'd", "my ", "me ", "myself",
        "feel", "hurt", "scared", "afraid", "ashamed", "broken",
        "can't sleep", "3am", "2am", "late night", "nobody knows",
        "never told", "honestly", "truth is", "real talk",
    ]

    # L1 markers (performative/polished)
    L1_MARKERS = [
        "one should", "it is important", "we must", "society",
        "in my opinion", "I believe that", "research shows",
        "furthermore", "moreover", "consequently",
    ]

    # L3 authenticity threshold (spec: ≥70th percentile)
    L3_AUTHENTICITY_THRESHOLD = 0.70

    def score_authenticity(self, text: str) -> float:
        """Heuristic LIWC-22 authenticity scoring.
        Returns a 0.0–1.0 percentile estimate."""
        if not text:
            return 0.0

        text_lower = text.lower()
        text_len = max(len(text_lower.split()), 1)

        # Count L3 markers
        l3_count = sum(1 for m in self.L3_MARKERS if m in text_lower)
        # Count L1 markers (subtract from authenticity)
        l1_count = sum(1 for m in self.L1_MARKERS if m in text_lower)

        # Pronoun density (I/me/my per word) — L3 signal
        pronoun_count = sum(
            1 for w in text_lower.split()
            if w in {"i", "i'm", "i've", "i'd", "my", "me", "myself"}
        )
        pronoun_density = pronoun_count / text_len

        # Composite score: higher L3 markers + pronouns → higher authenticity
        raw_score = (
            (l3_count * 0.15)
            + (pronoun_density * 2.0)
            - (l1_count * 0.10)
        )

        # Clamp to 0.0–1.0
        return max(0.0, min(1.0, raw_score))


class DepthStratifier:
    """FR6 Phase B2: L1/L2/L3 Depth Stratification.

    For each entry across all 12 dimensions, classifies depth level
    using LIWC-22 authenticity scoring and source context.

    Neuroscience grounding (Mind After Midnight hypothesis):
    - Amygdala-PFC decoupling during circadian nadir → reduced self-regulation
    - Spontaneous disclosure patterns measurable via LIWC-22 markers
    """

    L3_AUTHENTICITY_THRESHOLD = 0.70
    L2_MIN_RATIO = 0.30
    L3_MIN_RATIO = 0.10

    def __init__(self, liwc_scorer: Optional[LiwcScorerProtocol] = None):
        self.liwc_scorer: LiwcScorerProtocol = liwc_scorer or DefaultLiwcScorer()

    def classify_depth(
        self,
        text: str,
        source_platform: str = "",
        timestamp_context: str = "",
    ) -> tuple[DepthLevel, float]:
        """Classify a single text entry to L1/L2/L3.

        Returns (depth_level, authenticity_score).

        Classification logic (spec §Phase B2):
        - L3: LIWC-22 authenticity ≥70th percentile + anonymous/late-night sources
        - L2: In-group disclosure context (closed groups, moderated channels)
        - L1: Default — public, polished, professional
        """
        authenticity_score = self.liwc_scorer.score_authenticity(text)

        # L3 check: authenticity threshold + source signals
        is_anonymous_source = any(
            s in source_platform.lower()
            for s in ["anonymous", "throwaway", "burner", "vent", "confess"]
        )
        is_late_night = any(
            t in timestamp_context.lower()
            for t in ["2am", "3am", "4am", "1am", "late night", "midnight", "can't sleep"]
        )

        if authenticity_score >= self.L3_AUTHENTICITY_THRESHOLD:
            return DepthLevel.L3, authenticity_score

        if is_anonymous_source or is_late_night:
            # Boost: anonymous/late-night sources get L3 if near threshold
            if authenticity_score >= (self.L3_AUTHENTICITY_THRESHOLD - 0.15):
                return DepthLevel.L3, authenticity_score

        # L2 check: in-group disclosure signals
        l2_platforms = [
            "closed group", "private", "discord", "slack",
            "member", "subscriber", "dm", "closed facebook",
        ]
        is_l2_source = any(s in source_platform.lower() for s in l2_platforms)

        if is_l2_source or authenticity_score >= 0.40:
            return DepthLevel.L2, authenticity_score

        # Default: L1
        return DepthLevel.L1, authenticity_score

    def stratify_entries(
        self,
        entries: list[DepthStratifiedEntry] | Sequence[DepthStratifiedEntry],
    ) -> list[DepthStratifiedEntry] | Sequence[DepthStratifiedEntry]:
        """Classify depth for a list of entries in-place."""
        for entry in entries:
            depth, score = self.classify_depth(
                text=entry.text,
                source_platform=entry.source_platform,
                timestamp_context="",
            )
            entry.depth = depth
            entry.liwc_authenticity_score = score
        return entries

    def compute_distribution(
        self,
        entries: Sequence[DepthStratifiedEntry],
    ) -> DepthDistribution:
        """Compute L1/L2/L3 distribution ratios.
        AC4: L2 ≥30% AND L3 ≥10%."""
        total = len(entries)
        if total == 0:
            return DepthDistribution()

        l1_count = sum(1 for e in entries if e.depth == DepthLevel.L1)
        l2_count = sum(1 for e in entries if e.depth == DepthLevel.L2)
        l3_count = sum(1 for e in entries if e.depth == DepthLevel.L3)

        return DepthDistribution(
            l1_ratio=l1_count / total,
            l2_ratio=l2_count / total,
            l3_ratio=l3_count / total,
        )

    def validate_depth_gate(
        self,
        distribution: DepthDistribution,
    ) -> bool:
        """Spec §Phase B2 Hard Gate: L2 ≥30% AND L3 ≥10%.
        AC4: Profile with 80% L1 / 15% L2 / 5% L3 → FAILED."""
        return distribution.passes_depth_gate()
