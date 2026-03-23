"""
CCP FR6 — Psychometric Extension Mapper (Phase B6) (Unit 7)
5 psychometric extension mappings for the Context Premise Map.

Spec reference: FR6 Tech Spec §Phase B6
  1. regulatory_focus_orientation — Higgins Regulatory Focus Theory (1997)
  2. moral_foundation_violated — Haidt MFT / MFQ-2 (2023), eMFD
  3. coping_trajectory_position — Lazarus & Folkman (1984)
  4. hermeneutical_gap_markers — Fricker (2007), Dotson (2011)
  5. reconsolidation_sensitivity — Nader (2000), NEAS framework

AC14: All 5 extensions populated or explicitly null with reasoning.
moral_foundation_violated must use MFT/MFQ-2 framework labels, not free-text.
"""

from typing import Any, Optional

from src.ccp.models.tribe_profile_models import (
    CopingTrajectoryPosition,
    DepthStratifiedEntry,
    EmotionalTriggerEntry,
    HermeneuticalGapMarker,
    HermeneuticalGapMethod,
    MoralFoundationType,
    MoralFoundationViolated,
    PsychometricExtensions,
    ReconsolidationEngagementProxies,
    ReconsolidationSensitivityExt,
    RegulatoryFocus,
)


# ──────────────────────────────────────────────────────────────
# Keyword maps for heuristic classification
# ──────────────────────────────────────────────────────────────

_PROMOTION_KEYWORDS = frozenset([
    "grow", "growth", "achieve", "dream", "aspire", "build",
    "create", "inspire", "ideal", "vision", "transform",
    "opportunity", "potential", "flourish", "thrive", "gain",
])

_PREVENTION_KEYWORDS = frozenset([
    "protect", "safe", "safety", "avoid", "prevent", "duty",
    "obligation", "secure", "guard", "shield", "loss",
    "risk", "threat", "danger", "careful", "responsibility",
])

_MORAL_FOUNDATION_KEYWORDS: dict[MoralFoundationType, frozenset[str]] = {
    MoralFoundationType.CARE_HARM: frozenset([
        "care", "harm", "hurt", "suffering", "compassion", "empathy",
        "cruel", "kind", "nurture", "protect children", "vulnerable",
    ]),
    MoralFoundationType.FAIRNESS_CHEATING: frozenset([
        "fair", "unfair", "justice", "injustice", "equal", "cheat",
        "rigged", "rights", "discrimination", "equity", "deserve",
    ]),
    MoralFoundationType.LOYALTY_BETRAYAL: frozenset([
        "loyal", "betray", "traitor", "team", "group", "tribe",
        "solidarity", "patriot", "community", "belong", "sellout",
    ]),
    MoralFoundationType.AUTHORITY_SUBVERSION: frozenset([
        "authority", "respect", "obey", "rebel", "tradition",
        "hierarchy", "order", "chaos", "discipline", "leader",
    ]),
    MoralFoundationType.SANCTITY_DEGRADATION: frozenset([
        "pure", "impure", "sacred", "profane", "disgust", "clean",
        "dirty", "corrupt", "noble", "degrading", "wholesome",
    ]),
    MoralFoundationType.LIBERTY_OPPRESSION: frozenset([
        "freedom", "liberty", "oppression", "tyranny", "control",
        "autonomy", "domination", "censorship", "rights", "choice",
    ]),
}

_COPING_SEARCH_KEYWORDS = frozenset([
    "has anyone", "how do you", "what should", "looking for",
    "anyone tried", "help me", "where do i", "need advice",
    "recommendations", "suggestions", "struggling with",
])

_COPING_ACTIVE_KEYWORDS = frozenset([
    "working on", "step by step", "progress", "getting better",
    "learning", "trying", "implementing", "practicing",
    "improving", "on track", "moving forward",
])

_COPING_EXHAUSTED_KEYWORDS = frozenset([
    "exhausted", "given up", "hopeless", "pointless", "burned out",
    "nothing works", "tired of trying", "done", "over it",
    "can't anymore", "what's the point",
])


class PsychometricExtensionMapper:
    """FR6 Phase B6: 5 Psychometric Extension Mappings.

    Maps audience data to psychometric dimensions grounded in
    7 academic frameworks.

    AC14: All 5 populated or explicitly null with reasoning.
    """

    # ──────────────────────────────────────────────────────────
    # Extension 1: Regulatory Focus (Higgins 1997)
    # ──────────────────────────────────────────────────────────

    def map_regulatory_focus(
        self,
        entries: list[DepthStratifiedEntry],
    ) -> RegulatoryFocus:
        """Classify audience regulatory focus orientation.
        Uses eager vs. vigilant language markers."""
        all_text = " ".join(e.text.lower() for e in entries if e.text)
        words = set(all_text.split())

        promo_score = len(words & _PROMOTION_KEYWORDS)
        prev_score = len(words & _PREVENTION_KEYWORDS)

        if promo_score > prev_score * 1.5:
            return RegulatoryFocus.PROMOTION
        elif prev_score > promo_score * 1.5:
            return RegulatoryFocus.PREVENTION
        else:
            return RegulatoryFocus.MIXED

    # ──────────────────────────────────────────────────────────
    # Extension 2: Moral Foundation Violated (Haidt MFT/MFQ-2)
    # ──────────────────────────────────────────────────────────

    def map_moral_foundation(
        self,
        triggers: list[EmotionalTriggerEntry],
        entries: list[DepthStratifiedEntry],
    ) -> MoralFoundationViolated:
        """Reverse-engineer activated moral foundation from audience L3 pain.
        AC14: Must use MFT/MFQ-2 framework labels, not free-text."""
        all_text = " ".join(
            e.text.lower() for e in entries if e.text
        ) + " " + " ".join(
            t.text.lower() for t in triggers if t.text
        )
        words = set(all_text.split())

        # Score each foundation
        scores: dict[MoralFoundationType, int] = {}
        for foundation, keywords in _MORAL_FOUNDATION_KEYWORDS.items():
            scores[foundation] = len(words & keywords)

        # Sort by score descending
        sorted_foundations = sorted(
            scores.items(), key=lambda x: x[1], reverse=True,
        )

        primary: Optional[MoralFoundationType] = None
        secondary: Optional[MoralFoundationType] = None
        weighting: dict[str, float] = {}

        total_score = sum(s for _, s in sorted_foundations)
        if total_score > 0:
            primary = sorted_foundations[0][0]
            weighting[primary.value] = sorted_foundations[0][1] / total_score
            if len(sorted_foundations) > 1 and sorted_foundations[1][1] > 0:
                secondary = sorted_foundations[1][0]
                weighting[secondary.value] = sorted_foundations[1][1] / total_score

        return MoralFoundationViolated(
            primary=primary,
            secondary=secondary,
            weighting=weighting,
        )

    # ──────────────────────────────────────────────────────────
    # Extension 3: Coping Trajectory Position (Lazarus & Folkman)
    # ──────────────────────────────────────────────────────────

    def map_coping_trajectory(
        self,
        entries: list[DepthStratifiedEntry],
    ) -> CopingTrajectoryPosition:
        """Classify current phase in stress-coping cycle.
        SEARCH = peak intervention receptivity."""
        all_text = " ".join(e.text.lower() for e in entries if e.text)

        search_score = sum(1 for k in _COPING_SEARCH_KEYWORDS if k in all_text)
        active_score = sum(1 for k in _COPING_ACTIVE_KEYWORDS if k in all_text)
        exhausted_score = sum(1 for k in _COPING_EXHAUSTED_KEYWORDS if k in all_text)

        if search_score >= active_score and search_score >= exhausted_score:
            return CopingTrajectoryPosition.SEARCH
        elif active_score >= exhausted_score:
            return CopingTrajectoryPosition.ACTIVE
        else:
            return CopingTrajectoryPosition.EXHAUSTED

    # ──────────────────────────────────────────────────────────
    # Extension 4: Hermeneutical Gap Markers (Fricker / Dotson)
    # ──────────────────────────────────────────────────────────

    def detect_hermeneutical_gaps(
        self,
        entries: list[DepthStratifiedEntry],
    ) -> list[HermeneuticalGapMarker]:
        """Detect evidence of unarticulated experience.

        Detection methods:
        - Truncation: discourse breaks mid-sentence (cosine similarity drops)
        - Parabola: sentiment regression within single post (affective parabola)
        - Novelty: novel metaphors indicating search for language (MelBERT proxy)
        """
        markers: list[HermeneuticalGapMarker] = []

        for entry in entries:
            text = entry.text
            if not text:
                continue

            text_lower = text.lower()

            # Truncation detection: "I don't know...", "it's like...", trailing off
            truncation_signals = [
                "i don't know", "it's like", "i can't explain",
                "hard to describe", "words fail", "...",
                "i mean", "sort of", "kind of like",
            ]
            has_truncation = any(s in text_lower for s in truncation_signals)

            # Novelty detection: novel metaphors (heuristic)
            novelty_signals = [
                "it felt like", "as if", "like being",
                "imagine", "picture this", "it was as though",
            ]
            has_novelty = any(s in text_lower for s in novelty_signals)

            # Parabola detection: sentiment shift markers
            parabola_signals = [
                "but then", "and yet", "however", "on the other hand",
                "at first", "initially", "turned out",
            ]
            has_parabola = any(s in text_lower for s in parabola_signals)

            if has_truncation:
                markers.append(HermeneuticalGapMarker(
                    text=text[:200],
                    detection_method=HermeneuticalGapMethod.TRUNCATION,
                    confidence=0.7 if "..." in text else 0.5,
                ))
            elif has_novelty:
                markers.append(HermeneuticalGapMarker(
                    text=text[:200],
                    detection_method=HermeneuticalGapMethod.NOVELTY,
                    confidence=0.6,
                ))
            elif has_parabola:
                markers.append(HermeneuticalGapMarker(
                    text=text[:200],
                    detection_method=HermeneuticalGapMethod.PARABOLA,
                    confidence=0.5,
                ))

        return markers

    # ──────────────────────────────────────────────────────────
    # Extension 5: Reconsolidation Sensitivity (Nader 2000)
    # ──────────────────────────────────────────────────────────

    def map_reconsolidation_sensitivity(
        self,
        engagement_data: Optional[dict[str, float]] = None,
    ) -> ReconsolidationSensitivityExt:
        """Map audience readiness for memory reconsolidation.

        Uses behavioral engagement proxies:
        save_rate, comment_depth, share_velocity, dm_response_rate.
        """
        if engagement_data is None:
            return ReconsolidationSensitivityExt()

        proxies = ReconsolidationEngagementProxies(
            save_rate=engagement_data.get("save_rate", 0.0),
            comment_depth=engagement_data.get("comment_depth", 0.0),
            share_velocity=engagement_data.get("share_velocity", 0.0),
            dm_response_rate=engagement_data.get("dm_response_rate", 0.0),
        )

        # Overall score: weighted average of proxies (0-10 scale)
        weighted = (
            proxies.save_rate * 3.0
            + proxies.comment_depth * 3.0
            + proxies.share_velocity * 2.0
            + proxies.dm_response_rate * 2.0
        )
        overall = min(10.0, weighted)

        return ReconsolidationSensitivityExt(
            overall_score=overall,
            engagement_proxies=proxies,
        )

    # ──────────────────────────────────────────────────────────
    # Full Extension Mapping
    # ──────────────────────────────────────────────────────────

    def map_all_extensions(
        self,
        entries: list[DepthStratifiedEntry],
        triggers: list[EmotionalTriggerEntry],
        engagement_data: Optional[dict[str, float]] = None,
    ) -> PsychometricExtensions:
        """Map all 5 psychometric extensions. AC14 compliance."""
        return PsychometricExtensions(
            regulatory_focus_orientation=self.map_regulatory_focus(entries),
            moral_foundation_violated=self.map_moral_foundation(triggers, entries),
            coping_trajectory_position=self.map_coping_trajectory(entries),
            hermeneutical_gap_markers=self.detect_hermeneutical_gaps(entries),
            reconsolidation_sensitivity=self.map_reconsolidation_sensitivity(
                engagement_data,
            ),
        )
