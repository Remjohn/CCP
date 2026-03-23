"""
CCP FR7 Leadership Scorecard — Weekly Evolution Engine (Unit 7)
Weekly scorecard evolution: climb/hold/decline logic after ≥3 sessions.

Spec reference: FR7 Tech Spec §Weekly Scorecard Evolution
                §Score Evolution Logic table

Note from spec: 'This is NOT part of Genesis setup. This runs after each weekly production session.'
Trigger: After ccf-validate completes (all 36 scripts pass Sophia + Marcus + Chen).

Evolution logic (spec table):
  CLIMB:   Exercise content passes Sophia ≥85% AND engagement above coach average → score +1 (max 10)
  HOLD:    Passes validation but engagement below average → no change
  DECLINE: Consistently fails Sophia OR Chen detection high → score -1 (min 1)

AC7: 'After 3 consecutive weeks where exercise content for Embodied Confidence passes
      Sophia ≥85% AND audience engagement above coach average → score increases by +1.'
AC8: 'No trait can score below 1 or above 10. A score evolution that would push below 1 →
      stays at 1. Above 10 → stays at 10.'
"""

import json
from pathlib import Path

from src.ccp.models.leadership_scorecard_models import (
    MINIMUM_EVOLUTION_SESSIONS,
    SOPHIA_ALIGNMENT_CLIMB_THRESHOLD,
    TRAIT_SCORE_MAX,
    TRAIT_SCORE_MIN,
    EvolutionAction,
    FormatAssignmentType,
    LeadershipScorecard,
    TraitHistoryEntry,
    TraitName,
    TraitSessionPerformance,
    WeeklySessionData,
)


class WeeklyEvolutionEngine:
    """Applies weekly scorecard evolution logic after production sessions.

    Spec §Weekly Scorecard Evolution — NOT part of Genesis.
    Runs after ccf-validate completes each week.

    The engine reads the existing scorecard, applies the evolution data from the
    completed session, and writes the updated scorecard back.

    AC8 is enforced: scores are clamped to [1, 10] after every evolution step.
    """

    def __init__(self, scorecard_path: Path):
        """Initialize with the path to the coach's leadership_scorecard.json.

        Args:
            scorecard_path: Path to leadership_scorecard.json (DEP-ENG-026).
        """
        self.scorecard_path = scorecard_path

    def load_scorecard(self) -> LeadershipScorecard:
        """Load the current scorecard from disk."""
        data = json.loads(self.scorecard_path.read_text(encoding="utf-8"))
        return LeadershipScorecard.model_validate(data)

    def apply_session(
        self,
        scorecard: LeadershipScorecard,
        session_data: WeeklySessionData,
    ) -> LeadershipScorecard:
        """Apply one week's performance data to the scorecard.

        Spec §Weekly Scorecard Evolution: evolution data added to trait history.
        Evolution score changes only trigger after ≥3 sessions with exercise assignments (AC7).

        Args:
            scorecard: The current scorecard.
            session_data: Performance data from the completed weekly session.

        Returns:
            Updated scorecard with evolution applied.
        """
        updated_traits = list(scorecard.traits)

        for perf in session_data.trait_updates:
            trait_idx = next(
                (i for i, t in enumerate(updated_traits) if t.name == perf.trait_name),
                None,
            )
            if trait_idx is None:
                continue

            trait = updated_traits[trait_idx]

            # Only evolve traits with exercise assignment (develop the weak)
            if perf.assignment_type != FormatAssignmentType.EXERCISE:
                # Add history entry but no score change for non-exercise assignments
                history_entry = TraitHistoryEntry(
                    session_id=session_data.session_id,
                    previous_score=trait.score,
                    new_score=trait.score,
                    action=EvolutionAction.HOLD,
                    formats_assigned=perf.formats_assigned,
                    assignment_type=perf.assignment_type,
                    sophia_alignment=perf.sophia_alignment,
                    chen_detection=perf.chen_detection,
                    audience_engagement_7d=perf.audience_engagement_7d,
                    coach_average_engagement=session_data.coach_average_engagement,
                )
                new_history = list(trait.history) + [history_entry]
                updated_traits[trait_idx] = trait.model_copy(update={"history": new_history})
                continue

            # Determine evolution action
            action, new_score = self._determine_evolution(
                trait=trait,
                perf=perf,
                coach_average=session_data.coach_average_engagement,
            )

            # AC8: clamp to bounds
            new_score = max(TRAIT_SCORE_MIN, min(TRAIT_SCORE_MAX, new_score))

            history_entry = TraitHistoryEntry(
                session_id=session_data.session_id,
                previous_score=trait.score,
                new_score=new_score,
                action=action,
                formats_assigned=perf.formats_assigned,
                assignment_type=perf.assignment_type,
                sophia_alignment=perf.sophia_alignment,
                chen_detection=perf.chen_detection,
                audience_engagement_7d=perf.audience_engagement_7d,
                coach_average_engagement=session_data.coach_average_engagement,
            )

            new_history = list(trait.history) + [history_entry]
            updated_traits[trait_idx] = trait.model_copy(update={
                "score": new_score,
                "history": new_history,
            })

        from datetime import datetime, timezone
        return scorecard.model_copy(update={
            "traits": updated_traits,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        })

    def _determine_evolution(
        self,
        trait: "ScoredTrait",  # type: ignore[name-defined]  # forward ref
        perf: TraitSessionPerformance,
        coach_average: float | None,
    ) -> tuple[EvolutionAction, int]:
        """Determine climb/hold/decline and new score.

        Spec §Score Evolution Logic — requires ≥3 prior exercise sessions:
        CLIMB:   Sophia ≥85% AND engagement above coach average
        HOLD:    Passes but engagement below average
        DECLINE: Consistently fails Sophia OR Chen detection high

        AC7: Evolution only after ≥3 exercise sessions have accumulated in history.

        Returns:
            Tuple of (EvolutionAction, new_score).
        """
        from src.ccp.models.leadership_scorecard_models import ScoredTrait

        # Count prior exercise sessions in history
        exercise_history = [
            h for h in trait.history
            if h.assignment_type == FormatAssignmentType.EXERCISE
        ]

        # AC7: Require ≥3 prior exercise sessions before any evolution triggers
        if len(exercise_history) < MINIMUM_EVOLUTION_SESSIONS:
            return EvolutionAction.HOLD, trait.score

        # DECLINE condition: consistently fails Sophia OR Chen detection high
        # Check last 3 exercise sessions for failure patterns
        recent_exercise = exercise_history[-3:]
        sophia_failures = sum(
            1 for h in recent_exercise
            if h.sophia_alignment < SOPHIA_ALIGNMENT_CLIMB_THRESHOLD
        )
        chen_highs = sum(1 for h in recent_exercise if h.chen_detection > 0.5)

        if sophia_failures >= 3 or chen_highs >= 3:
            return EvolutionAction.DECLINE, trait.score - 1

        # Check current session performance
        sophia_passes = perf.sophia_alignment >= SOPHIA_ALIGNMENT_CLIMB_THRESHOLD
        engagement_above = (
            coach_average is not None
            and perf.audience_engagement_7d is not None
            and perf.audience_engagement_7d > coach_average
        )

        if sophia_passes and engagement_above:
            # CLIMB: AC7 — score increases by +1
            return EvolutionAction.CLIMB, trait.score + 1
        elif perf.sophia_alignment < SOPHIA_ALIGNMENT_CLIMB_THRESHOLD or perf.chen_detection > 0.5:
            return EvolutionAction.DECLINE, trait.score - 1
        else:
            return EvolutionAction.HOLD, trait.score

    def save_scorecard(self, scorecard: LeadershipScorecard) -> None:
        """Write the updated scorecard back to disk."""
        self.scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def run(self, session_data: WeeklySessionData) -> LeadershipScorecard:
        """Load, apply session, save, and return the updated scorecard.

        Spec §Weekly Scorecard Evolution: full weekly evolution cycle.

        Args:
            session_data: Performance data from the completed weekly production session.

        Returns:
            Updated LeadershipScorecard.
        """
        scorecard = self.load_scorecard()
        updated = self.apply_session(scorecard, session_data)
        self.save_scorecard(updated)
        return updated


# Forward reference resolution for type hints
from src.ccp.models.leadership_scorecard_models import ScoredTrait  # noqa: E402
