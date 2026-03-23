"""
CCP FR5 Trigger Map Builder — Trigger Archetype Mapper (Unit 7)
Phase 7: Emotional state → archetype candidates + TTT eligibility.

Spec reference: FR5 Tech Spec §Phase 7
  - Maps the emotional state produced by trigger activation to
    archetype candidates from the Trigger-First Engine Architecture
  - Checks TTT eligibility: coach's ttt_baseline must meet the
    archetype's ttt_minimum to be eligible
  - Uses the trigger_archetype_map table from trigger_map.json template

Research basis:
  Trigger-First Engine Architecture v3.0 — Stage 5 specification
  TTT (Temperature, Texture, Tone) Authentication System
"""

from typing import Optional

from src.ccp.models.trigger_map_models import (
    ArchetypeMapping,
    MoralFoundationType,
    TriggerEntry,
)


# Default archetype mappings from trigger_map.json template
# These map emotional_state + moral_foundation → archetype candidates
DEFAULT_ARCHETYPE_MAPPINGS: list[dict[str, str]] = [
    {
        "emotional_state": "disgust_protective_fury",
        "moral_foundation": "sanctity_degradation",
        "primary_archetype": "myth_indignation",
        "secondary_archetype": "reaction_outrage",
        "ttt_minimum": "TTT-07",
    },
    {
        "emotional_state": "betrayal_anger",
        "moral_foundation": "loyalty_betrayal",
        "primary_archetype": "myth_indignation",
        "secondary_archetype": "comparison_outrageous",
        "ttt_minimum": "TTT-07",
    },
    {
        "emotional_state": "outrage_mechanism_opacity",
        "moral_foundation": "fairness_cheating",
        "primary_archetype": "listicle_shocking",
        "secondary_archetype": "comparison_shocking",
        "ttt_minimum": "TTT-05",
    },
    {
        "emotional_state": "protective_urgency",
        "moral_foundation": "care_harm_liberty_oppression",
        "primary_archetype": "myth_fear_anxiety",
        "secondary_archetype": "tweet_warning",
        "ttt_minimum": "TTT-05",
    },
    {
        "emotional_state": "righteous_authority",
        "moral_foundation": "fairness_authority",
        "primary_archetype": "tier_list_controversial",
        "secondary_archetype": "myth_empowering",
        "ttt_minimum": "TTT-05",
    },
    {
        "emotional_state": "grief_tinged_outrage",
        "moral_foundation": "care_harm",
        "primary_archetype": "story_transformation",
        "secondary_archetype": "story_recognition",
        "ttt_minimum": "TTT-03",
    },
]


class TriggerArchetypeMapper:
    """Phase 7 service: Maps triggers to archetype candidates.

    Maps each trigger's emotional state (derived from moral foundation
    + PTG status + narrative identity) to archetype candidates from
    the Trigger-First Engine Architecture.

    TTT Eligibility: The coach's ttt_baseline must meet the archetype's
    ttt_minimum threshold. If the coach's natural TTT ceiling is below
    the archetype's minimum, coach_eligible = False.
    """

    def __init__(
        self,
        archetype_table: Optional[list[dict[str, str]]] = None,
    ):
        """Initialize with archetype mapping table.

        Args:
            archetype_table: Custom archetype mapping table. If None,
                uses the default table from trigger_map.json template.
        """
        self.archetype_table = archetype_table or DEFAULT_ARCHETYPE_MAPPINGS

    def map_triggers(
        self,
        triggers: list[TriggerEntry],
        ttt_baseline: Optional[dict[str, object]] = None,
        session_id: str = "",
    ) -> tuple[list[TriggerEntry], list[ArchetypeMapping]]:
        """Map triggers to archetype candidates and check TTT eligibility.

        Args:
            triggers: Classified triggers from Phases 2-6.
            ttt_baseline: Coach's TTT baseline (from ttt_baseline.json).
                Expected key: 'overall_ttt' with int value 1-10.
            session_id: Pipeline session identifier.

        Returns:
            Tuple of (triggers, archetype_mappings).
            Triggers are returned with archetype info in description.
            archetype_mappings is the full mapping table with eligibility.
        """
        coach_ttt = self._extract_coach_ttt(ttt_baseline)

        # Build archetype mapping table with eligibility
        archetype_mappings: list[ArchetypeMapping] = []
        for entry in self.archetype_table:
            mapping = ArchetypeMapping(
                emotional_state=entry.get("emotional_state", ""),
                moral_foundation=entry.get("moral_foundation", ""),
                primary_archetype=entry.get("primary_archetype", ""),
                secondary_archetype=entry.get("secondary_archetype", ""),
                ttt_minimum=entry.get("ttt_minimum", ""),
                coach_eligible=self._check_ttt_eligibility(
                    entry.get("ttt_minimum", ""), coach_ttt
                ),
            )
            archetype_mappings.append(mapping)

        # Annotate triggers with best matching archetype
        for trigger in triggers:
            best_match = self._find_best_archetype_match(
                trigger, archetype_mappings
            )
            if best_match and best_match.is_populated():
                # Add archetype info to trigger's activation mechanisms
                mechanism = (
                    f"archetype:{best_match.primary_archetype}"
                    f"|secondary:{best_match.secondary_archetype}"
                    f"|eligible:{best_match.coach_eligible}"
                )
                if mechanism not in trigger.activation_mechanisms:
                    trigger.activation_mechanisms.append(mechanism)

        return triggers, archetype_mappings

    def _extract_coach_ttt(
        self, ttt_baseline: Optional[dict[str, object]]
    ) -> Optional[int]:
        """Extract the coach's overall TTT score from ttt_baseline.json."""
        if not ttt_baseline:
            return None

        overall = ttt_baseline.get("overall_ttt")
        if overall is not None:
            try:
                return int(overall)  # type: ignore[arg-type]
            except (ValueError, TypeError):
                pass

        # Try alternative key formats
        for key in ["ttt_score", "temperature", "overall"]:
            val = ttt_baseline.get(key)
            if val is not None:
                try:
                    return int(val)  # type: ignore[arg-type]
                except (ValueError, TypeError):
                    continue

        return None

    def _check_ttt_eligibility(
        self, ttt_minimum_str: str, coach_ttt: Optional[int]
    ) -> Optional[bool]:
        """Check if coach's TTT meets the archetype's minimum.

        TTT format: 'TTT-07' → numeric value 7.
        Coach eligible if coach_ttt >= archetype minimum.
        Returns None if coach TTT is unknown.
        """
        if coach_ttt is None:
            return None

        # Parse TTT-XX format
        try:
            min_value = int(ttt_minimum_str.replace("TTT-", "").strip())
        except (ValueError, AttributeError):
            return None

        return coach_ttt >= min_value

    def _find_best_archetype_match(
        self,
        trigger: TriggerEntry,
        mappings: list[ArchetypeMapping],
    ) -> Optional[ArchetypeMapping]:
        """Find the best archetype mapping for a trigger.

        Matches based on moral foundation alignment between the trigger's
        primary moral foundation and the archetype mapping table.
        """
        if not trigger.moral_foundation.primary:
            return None

        trigger_foundation = trigger.moral_foundation.primary.value
        best_match: Optional[ArchetypeMapping] = None
        best_score = 0.0

        for mapping in mappings:
            # Check if moral foundation matches
            mapping_foundation = mapping.moral_foundation.lower()

            score = 0.0
            if trigger_foundation in mapping_foundation:
                score = 1.0
            elif any(
                part in mapping_foundation
                for part in trigger_foundation.split("_")
            ):
                score = 0.5

            # Prefer eligible archetypes
            if mapping.coach_eligible is True:
                score += 0.2
            elif mapping.coach_eligible is None:
                score += 0.1

            if score > best_score:
                best_score = score
                best_match = mapping

        return best_match
