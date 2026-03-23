"""
CCP FR8 TTT Enforcement Rule — TTT Affinity Range Advisor (Unit 5)
Advisory system: checks if authenticated TTT temperature is within archetype's natural range.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md §TTT natural affinity range (advisory system)
                §Technical Decisions: "TTT natural affinity range as ADVISORY, not GATE"

AC8: Outside affinity range → log ttt_outside_affinity_range=True, flag for human review.
     Compilation PROCEEDS — coach's authentic emotional state overrides the affinity range.

This service is ADVISORY ONLY. It never blocks compilation.
"""

from src.ccp.models.ttt_models import AffinityRangeResult, TTTAffinityRange
from src.ccp.services.ttt_pattern_registry import (
    AFFINITY_RANGE_MAP,
    get_affinity_range,
    is_temperature_within_affinity,
)


class TTTAffinityAdvisor:
    """Advisory service for TTT natural affinity range checking.

    Spec §TTT natural affinity range (advisory system):
    "If the coach's authenticated TTT falls outside the archetype's natural affinity range:
      - The Orchestrator logs ttt_outside_affinity_range: true
      - The Orchestrator flags the compilation for human review
      - The compilation PROCEEDS — the coach's authentic emotional state overrides the advisory
      - Content may be unconventional but potentially more powerful than affinity-standard content"

    This service provides the evaluation. The pipeline orchestrator handles the
    logging and human review flagging.
    """

    def evaluate(
        self,
        archetype_id: str,
        coach_temperature: int,
    ) -> AffinityRangeResult:
        """Evaluate whether a coach's temperature is within the archetype's affinity range.

        Args:
            archetype_id: Content archetype identifier (e.g. "story_transformation").
            coach_temperature: Coach's authenticated temperature (1-10).

        Returns:
            AffinityRangeResult with advisory evaluation. compilation_blocked is ALWAYS False.
        """
        affinity = get_affinity_range(archetype_id)

        if affinity is None:
            # Unknown archetype → advisory cannot evaluate → PASS (not gated)
            return AffinityRangeResult(
                archetype_id=archetype_id,
                coach_temperature=coach_temperature,
                affinity_min=1,
                affinity_max=10,
                ttt_outside_affinity_range=False,
                requires_human_review=False,
                compilation_blocked=False,
                advisory_note=(
                    f"Archetype '{archetype_id}' is not registered in AFFINITY_RANGE_MAP. "
                    "No affinity advisory available — proceeding without advisory check."
                ),
            )

        outside_range = not (affinity.min_temperature <= coach_temperature <= affinity.max_temperature)

        requires_review = (
            affinity.human_review_flag_threshold is not None
            and coach_temperature >= affinity.human_review_flag_threshold
        )

        advisory_note: str | None = None
        if outside_range:
            advisory_note = (
                f"Coach authenticated at TTT-{coach_temperature:02d}. "
                f"Archetype '{archetype_id}' natural affinity range: "
                f"TTT-{affinity.min_temperature:02d} to TTT-{affinity.max_temperature:02d}. "
                f"Content may be unconventional but proceeds. "
                f"Rationale: {affinity.rationale}"
            )
        elif requires_review:
            advisory_note = (
                f"Coach at TTT-{coach_temperature:02d} — within affinity range but above "
                f"human review threshold (TTT-{affinity.human_review_flag_threshold}). "
                f"Flagging for human review per archetype advisory."
            )

        return AffinityRangeResult(
            archetype_id=archetype_id,
            coach_temperature=coach_temperature,
            affinity_min=affinity.min_temperature,
            affinity_max=affinity.max_temperature,
            ttt_outside_affinity_range=outside_range,
            requires_human_review=requires_review or outside_range,
            compilation_blocked=False,  # ALWAYS False — advisory only (AC8)
            advisory_note=advisory_note,
        )

    def evaluate_all(
        self,
        coach_temperature: int,
        archetype_ids: list[str],
    ) -> list[AffinityRangeResult]:
        """Evaluate affinity advisory for multiple archetypes at once.

        Args:
            coach_temperature: Coach's authenticated temperature (1-10).
            archetype_ids: List of archetype identifiers to evaluate.

        Returns:
            List of AffinityRangeResult, one per archetype.
        """
        return [self.evaluate(aid, coach_temperature) for aid in archetype_ids]

    def get_affinity_range(self, archetype_id: str) -> TTTAffinityRange | None:
        """Get the registered affinity range for an archetype.

        Args:
            archetype_id: Content archetype identifier.

        Returns:
            TTTAffinityRange if registered, None if archetype is not in the registry.
        """
        return get_affinity_range(archetype_id)

    @property
    def registered_archetypes(self) -> list[str]:
        """List of archetype IDs registered in the affinity range map."""
        return list(AFFINITY_RANGE_MAP.keys())
