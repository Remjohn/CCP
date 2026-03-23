"""
CCP FR7 Leadership Scorecard — Format Governance Engine (Unit 5)
Phase 4 FORMAT GOVERNANCE: Exercise/showcase assignment, 60/40 weighting.

Spec reference: FR7 Tech Spec §Phase 4: FORMAT GOVERNANCE — Exercise/Showcase Assignment
                §Exercise Assignment table, §Showcase Assignment table, §Weighting formula

Governs the ccf-eroll-plan format assignment for Emmanuel's 36-format weekly allocation:
  - 60% showcase (strong traits drive content authority)
  - 40% exercise (weak traits receive development reps)
  - Within exercise: lowest-scored traits get highest format weight

AC4: 'A coach with Deep Empathy = 3/10 → weekly format allocation contains
      ≥2 empathy-exercise archetypes (story_recognition or tweet_recognition).'
AC5: 'A coach with Archetypal Storytelling = 9/10 → weekly format allocation
      contains high-weight story formats.'
AC6: 'Weekly allocation is approximately 60% showcase / 40% exercise.
      100% showcase or 100% exercise → rejected by format governance validator.'
"""

from pathlib import Path
from typing import Optional, TypedDict

from src.ccp.models.leadership_scorecard_models import (
    EXERCISE_ARCHETYPE_MAP,
    EXERCISE_RATIO,
    SHOWCASE_ARCHETYPE_MAP,
    SHOWCASE_RATIO,
    STRONG_TRAIT_THRESHOLD,
    WEAK_TRAIT_THRESHOLD,
    FormatAssignmentType,
    FormatGovernance,
    LeadershipScorecard,
    ScoredTrait,
    TraitName,
)


class WeeklyAllocation(TypedDict):
    """Return type for FormatGovernanceEngine.compute_weekly_allocation()."""
    showcase_formats: list[str]
    exercise_formats: list[str]
    showcase_count: int
    exercise_count: int
    showcase_ratio: float
    exercise_ratio: float


class FormatRatioError(Exception):
    """Raised when format governance produces an invalid ratio.
    AC6: '100% showcase or 100% exercise → rejected by format governance validator.'
    """
    pass


class FormatGovernanceEngine:
    """Applies exercise/showcase format assignments to scored traits.

    Spec §Phase 4 FORMAT GOVERNANCE:
    - Weak traits (score ≤ 5/10) → exercise assignment
    - Strong traits (score ≥ 7/10) → showcase assignment
    - Middle range (6/10) → neutral (system defaults)
    - 60% showcase / 40% exercise ratio enforced
    - Within exercise: lowest-scored traits receive highest format weight
    """

    TOTAL_WEEKLY_FORMATS: int = 36  # Emmanuel's 36-format weekly allocation

    def apply_format_governance(self, scored_traits: list[ScoredTrait]) -> list[ScoredTrait]:
        """Apply exercise/showcase assignments to all scored traits.

        Args:
            scored_traits: The 12 scored traits from Phase 2.

        Returns:
            Traits with format_assignment, exercise_archetypes, and showcase_archetypes set.

        Raises:
            FormatRatioError: If the resulting assignment would be 100% showcase or 100% exercise (AC6).
        """
        updated: list[ScoredTrait] = []

        for trait in scored_traits:
            assignment = self._determine_assignment(trait)
            exercise_archetypes = EXERCISE_ARCHETYPE_MAP.get(trait.name, [])
            showcase_archetypes = SHOWCASE_ARCHETYPE_MAP.get(trait.name, [])

            updated.append(ScoredTrait(
                trait_id=trait.trait_id,
                name=trait.name,
                label=trait.label,
                score=trait.score,
                category=trait.category,
                evidence=trait.evidence,
                format_assignment=assignment,
                exercise_archetypes=exercise_archetypes,
                showcase_archetypes=showcase_archetypes,
                history=trait.history,
            ))

        # Validate ratio (AC6)
        self._validate_ratio(updated)

        return updated

    def _determine_assignment(self, trait: ScoredTrait) -> FormatAssignmentType:
        """Determine exercise/showcase/neutral assignment for a trait.

        Spec: Weak traits (≤5) → exercise. Strong traits (≥7) → showcase.
        """
        if trait.score <= WEAK_TRAIT_THRESHOLD:
            return FormatAssignmentType.EXERCISE
        elif trait.score >= STRONG_TRAIT_THRESHOLD:
            return FormatAssignmentType.SHOWCASE
        else:
            return FormatAssignmentType.NEUTRAL

    def _validate_ratio(self, traits: list[ScoredTrait]) -> None:
        """Validate that the 60/40 ratio constraint is not violated.

        AC6: '100% showcase or 100% exercise → rejected by format governance validator.'
        """
        exercise_count = sum(1 for t in traits if t.format_assignment == FormatAssignmentType.EXERCISE)
        showcase_count = sum(1 for t in traits if t.format_assignment == FormatAssignmentType.SHOWCASE)
        total = len(traits)

        if total == 0:
            return

        if exercise_count == total:
            raise FormatRatioError(
                f"Format governance rejected: 100% exercise allocation ({exercise_count}/{total} traits). "
                f"A coach with all weak traits still needs showcase exploration to avoid stagnation."
            )

        if showcase_count == total:
            raise FormatRatioError(
                f"Format governance rejected: 100% showcase allocation ({showcase_count}/{total} traits). "
                f"A coach with all strong traits still needs exercise reps to prevent complacency."
            )

    def compute_weekly_allocation(self, scored_traits: list[ScoredTrait]) -> WeeklyAllocation:
        """Compute the weekly 36-format allocation with exercise/showcase weighting.

        Spec §Weighting formula:
        - 60% showcase (strong traits drive content authority)
        - 40% exercise (weak traits receive development reps)
        - Within exercise: traits with lowest scores get highest format weight

        Returns:
            Dict with 'showcase_formats' and 'exercise_formats' lists.
        """
        exercise_traits = sorted(
            [t for t in scored_traits if t.format_assignment == FormatAssignmentType.EXERCISE],
            key=lambda t: t.score,  # Lowest scores first = highest weight
        )
        showcase_traits = sorted(
            [t for t in scored_traits if t.format_assignment == FormatAssignmentType.SHOWCASE],
            key=lambda t: t.score, reverse=True,  # Highest scores first
        )
        neutral_traits = [t for t in scored_traits if t.format_assignment == FormatAssignmentType.NEUTRAL]

        showcase_slots = round(self.TOTAL_WEEKLY_FORMATS * SHOWCASE_RATIO)  # 22 slots
        exercise_slots = self.TOTAL_WEEKLY_FORMATS - showcase_slots           # 14 slots

        # Build showcase format list (highest-scoring showcase traits get more slots)
        showcase_formats: list[str] = []
        if showcase_traits:
            per_trait_slots = max(1, showcase_slots // len(showcase_traits))
            for trait in showcase_traits:
                archetypes = trait.showcase_archetypes
                for i in range(per_trait_slots):
                    if archetypes:
                        showcase_formats.append(archetypes[i % len(archetypes)])

        # Fill remaining showcase slots with neutral traits if available
        while len(showcase_formats) < showcase_slots and neutral_traits:
            for trait in neutral_traits:
                if len(showcase_formats) >= showcase_slots:
                    break
                if trait.showcase_archetypes:
                    showcase_formats.append(trait.showcase_archetypes[0])

        # Trim to showcase_slots
        showcase_formats = showcase_formats[:showcase_slots]

        # Build exercise format list (lowest-scoring exercise traits get highest weight)
        exercise_formats: list[str] = []
        if exercise_traits:
            # Lower-scored traits get more slots
            total_weight = sum(range(1, len(exercise_traits) + 1))
            for rank, trait in enumerate(exercise_traits):
                weight = len(exercise_traits) - rank  # lowest score → highest weight
                slots = max(1, round((weight / total_weight) * exercise_slots))
                archetypes = trait.exercise_archetypes
                for i in range(slots):
                    if archetypes:
                        exercise_formats.append(archetypes[i % len(archetypes)])

        exercise_formats = exercise_formats[:exercise_slots]

        return {
            "showcase_formats": showcase_formats,
            "exercise_formats": exercise_formats,
            "showcase_count": len(showcase_formats),
            "exercise_count": len(exercise_formats),
            "showcase_ratio": len(showcase_formats) / self.TOTAL_WEEKLY_FORMATS if self.TOTAL_WEEKLY_FORMATS else 0,
            "exercise_ratio": len(exercise_formats) / self.TOTAL_WEEKLY_FORMATS if self.TOTAL_WEEKLY_FORMATS else 0,
        }

    def write_to_content_strategy(
        self,
        scored_traits: list[ScoredTrait],
        scorecard_id: str,
        output_path: Optional[Path] = None,
    ) -> str:
        """Write format governance assignments to 02_content_strategy.md.

        Spec §Phase 4: 'Format assignments written to 02_content_strategy.md
        with trait-to-format mapping.'
        Also §Phase 6: 'Write format governance to 02_content_strategy.md'

        Returns:
            Formatted markdown content.
        """
        allocation = self.compute_weekly_allocation(scored_traits)
        lines = [
            "# Content Strategy — Format Governance",
            f"",
            f"**Scorecard ID:** {scorecard_id}",
            f"**Format ratio:** {allocation['showcase_ratio']:.0%} showcase / {allocation['exercise_ratio']:.0%} exercise",
            f"",
            "## Showcase Assignments (Strong Traits — Score ≥ 7/10)",
            "",
        ]

        showcase_traits = [t for t in scored_traits if t.format_assignment == FormatAssignmentType.SHOWCASE]
        for trait in showcase_traits:
            lines.append(f"### {trait.label} (Score: {trait.score}/10)")
            lines.append(f"- **Assignment type:** Showcase")
            lines.append(f"- **Assigned formats:** {', '.join(trait.showcase_archetypes)}")
            lines.append(f"")

        lines.extend([
            "## Exercise Assignments (Weak Traits — Score ≤ 5/10)",
            "",
        ])

        exercise_traits = sorted(
            [t for t in scored_traits if t.format_assignment == FormatAssignmentType.EXERCISE],
            key=lambda t: t.score,
        )
        for trait in exercise_traits:
            lines.append(f"### {trait.label} (Score: {trait.score}/10)")
            lines.append(f"- **Assignment type:** Exercise")
            lines.append(f"- **Assigned formats:** {', '.join(trait.exercise_archetypes)}")
            lines.append(f"")

        lines.extend([
            "## Weekly Format Allocation (36 formats total)",
            "",
            f"### Showcase formats ({allocation['showcase_count']} slots):",
            *[f"- {f}" for f in allocation["showcase_formats"]],
            "",
            f"### Exercise formats ({allocation['exercise_count']} slots):",
            *[f"- {f}" for f in allocation["exercise_formats"]],
        ])

        content = "\n".join(lines)

        if output_path:
            output_path.write_text(content, encoding="utf-8")

        return content
