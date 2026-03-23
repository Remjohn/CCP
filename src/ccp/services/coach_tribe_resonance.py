"""
CCP FR6 — Coach-Tribe Resonance Cross-Reference (Phase B5) (Unit 6)
Alignment points, friction points, and gap analysis.

Spec reference: FR6 Tech Spec §Phase B5
  Alignment Points: ≥3 — where coach's philosophy ADDRESSES tribe's pain
  Friction Points: ≥1 — where coach's belief CONTRADICTS tribe's experience
  Gaps: free count — tribe pains the coach's philosophy doesn't address yet

"Missing friction is a red flag. If coach and tribe are in perfect agreement
on everything, the relationship is idealized, not real."

AC12: ≥3 alignment points and ≥1 friction point documented.
Zero friction points → WARNING: relationship is idealized.
"""

from typing import Any, Optional

from src.ccp.models.tribe_profile_models import (
    AlignmentPoint,
    CoachTribeResonance,
    DepthStratifiedEntry,
    EmotionalTriggerEntry,
    FrictionPoint,
    GapAnalysis,
)


class CoachTribeResonanceAnalyzer:
    """FR6 Phase B5: Coach-Tribe Resonance Cross-Reference.

    Uses coach_philosophy_brief (H10) and coach_soul.json (H8) to
    find alignment points, friction points, and gaps with the tribe.

    AC12: ≥3 alignment points AND ≥1 friction point.
    Zero friction → WARNING: idealized relationship.
    """

    def analyze_alignment(
        self,
        coach_philosophy: str,
        coach_beliefs: list[str],
        tribe_pains: list[str],
    ) -> list[AlignmentPoint]:
        """Find where coach's philosophy addresses tribe's pain.

        Uses keyword overlap between coach beliefs and tribe pain descriptions.
        Minimum: ≥3 alignment points (AC12).
        """
        points: list[AlignmentPoint] = []

        for belief in coach_beliefs:
            belief_words = set(belief.lower().split())
            for pain in tribe_pains:
                pain_words = set(pain.lower().split())
                overlap = belief_words & pain_words
                # Require meaningful overlap (>2 content words)
                content_overlap = overlap - {
                    "the", "a", "an", "is", "are", "was", "were", "be",
                    "to", "of", "in", "for", "on", "with", "and", "or",
                    "that", "this", "it", "not", "but", "they", "their",
                }
                if len(content_overlap) >= 2:
                    points.append(AlignmentPoint(
                        coach_belief=belief,
                        tribe_pain=pain,
                        leverage_description=(
                            f"Coach addresses tribe pain through: "
                            f"{', '.join(sorted(content_overlap))}"
                        ),
                    ))

        return points

    def analyze_friction(
        self,
        coach_beliefs: list[str],
        tribe_experiences: list[str],
    ) -> list[FrictionPoint]:
        """Find where coach's belief contradicts tribe's experience.

        Looks for semantic opposition between beliefs and experiences.
        Minimum: ≥1 friction point (AC12).
        """
        points: list[FrictionPoint] = []

        # Opposition word pairs for friction detection
        opposition_pairs = [
            ("should", "can't"), ("must", "impossible"),
            ("always", "never"), ("easy", "hard"),
            ("simple", "complex"), ("positive", "negative"),
            ("strength", "weakness"), ("success", "failure"),
            ("growth", "stuck"), ("change", "same"),
            ("forward", "backward"), ("rise", "fall"),
        ]

        for belief in coach_beliefs:
            belief_lower = belief.lower()
            for experience in tribe_experiences:
                exp_lower = experience.lower()
                for b_word, e_word in opposition_pairs:
                    if b_word in belief_lower and e_word in exp_lower:
                        points.append(FrictionPoint(
                            coach_belief=belief,
                            tribe_experience=experience,
                            risk_description=(
                                f"Coach says '{b_word}' but tribe experiences "
                                f"'{e_word}' — authenticity risk zone"
                            ),
                        ))
                        break  # One friction point per pair

        return points

    def analyze_gaps(
        self,
        coach_beliefs: list[str],
        tribe_pains: list[str],
        alignment_points: list[AlignmentPoint],
    ) -> list[GapAnalysis]:
        """Find tribe pains the coach's philosophy doesn't address.

        Any tribe pain not matched in alignment points = gap.
        """
        addressed_pains = {ap.tribe_pain for ap in alignment_points}
        gaps: list[GapAnalysis] = []

        for pain in tribe_pains:
            if pain not in addressed_pains:
                gaps.append(GapAnalysis(
                    tribe_pain=pain,
                    opportunity_description=(
                        f"Tribe pain not addressed by current coaching philosophy. "
                        f"Content opportunity: develop perspective on '{pain[:50]}...'"
                    ),
                ))

        return gaps

    def build_resonance(
        self,
        coach_soul: dict[str, Any],
        coach_philosophy_brief: str,
        tribe_entries: list[DepthStratifiedEntry],
        tribe_triggers: list[EmotionalTriggerEntry],
    ) -> CoachTribeResonance:
        """Full Phase B5 analysis: alignment + friction + gaps.

        Extracts coach beliefs from coach_soul and philosophy brief.
        Extracts tribe pains from depth-stratified entries.
        """
        # Extract coach beliefs
        coach_beliefs: list[str] = []
        if coach_philosophy_brief:
            # Split philosophy into belief statements
            for sentence in coach_philosophy_brief.replace(". ", ".\n").split("\n"):
                sentence = sentence.strip()
                if sentence and len(sentence) > 10:
                    coach_beliefs.append(sentence)

        # Add from coach_soul
        philosophy = coach_soul.get("coaching_philosophy", "")
        if philosophy:
            coach_beliefs.append(philosophy)
        core_msg = coach_soul.get("core_message", "")
        if core_msg:
            coach_beliefs.append(core_msg)

        # Extract tribe pains (all entries as text)
        tribe_pains = [e.text for e in tribe_entries if e.text]
        tribe_pains.extend(t.text for t in tribe_triggers if t.text)

        # Analyze
        alignment = self.analyze_alignment(
            coach_philosophy=coach_philosophy_brief,
            coach_beliefs=coach_beliefs,
            tribe_pains=tribe_pains,
        )
        friction = self.analyze_friction(
            coach_beliefs=coach_beliefs,
            tribe_experiences=[e.text for e in tribe_entries if e.text],
        )
        gaps = self.analyze_gaps(
            coach_beliefs=coach_beliefs,
            tribe_pains=tribe_pains,
            alignment_points=alignment,
        )

        return CoachTribeResonance(
            alignment_points=alignment,
            friction_points=friction,
            gaps=gaps,
        )

    def validate_resonance(
        self,
        resonance: CoachTribeResonance,
    ) -> dict[str, Any]:
        """AC12: ≥3 alignment + ≥1 friction. Zero friction → WARNING."""
        return {
            "alignment_count": len(resonance.alignment_points),
            "friction_count": len(resonance.friction_points),
            "gap_count": len(resonance.gaps),
            "passes_gate": resonance.passes_resonance_gate(),
            "zero_friction_warning": resonance.has_zero_friction_warning(),
        }
