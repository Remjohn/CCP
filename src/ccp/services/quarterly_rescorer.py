"""
CCP FR7 Leadership Scorecard — Quarterly Rescorer (Unit 8)
Quarterly full rescore from updated DEP objects.

Spec reference: FR7 Tech Spec §Quarterly Rescoring

'Every 12 weeks, the Minister of Identity performs a full rescore using the LATEST
coach_soul.json (which may have been updated if the coach submitted new Sacred Audio).
This catches genuine coach development that occurred outside the content pipeline
(e.g., new testimonials, deeper tribe understanding from CBCS interactions, public
speaking growth).'

AC12: 'After 12 weeks, a rescore using updated coach_soul.json (new Sacred Audio)
produces different scores than the Genesis baseline for at least 1 trait.'
"""

import json
from pathlib import Path
from typing import Optional

from src.ccp.models.leadership_scorecard_models import (
    LeadershipScorecard,
    QUARTERLY_RESCORE_WEEKS,
)
from src.ccp.services.signal_source_loader import SignalSourceLoader


class QuarterlyRescorerTriggerError(Exception):
    """Raised when rescore is triggered before the minimum interval."""
    pass


class QuarterlyRescorer:
    """Performs a full 12-trait rescore every QUARTERLY_RESCORE_WEEKS weeks.

    Spec §Quarterly Rescoring:
    'Every 12 weeks, the Minister of Identity performs a full rescore using the LATEST
    coach_soul.json (new Sacred Audio submitted).'

    The rescorer:
    1. Loads the current scorecard to read baseline scores
    2. Loads fresh signal sources (latest DEP objects)
    3. Runs the full scoring pipeline
    4. Emits an updated scorecard with new scores
    5. Preserves history from the pre-rescore scorecard

    AC12: Produces different scores for at least 1 trait when DEP objects have been updated.
    """

    def __init__(self, coach_dir: Path):
        """Initialize the quarterly rescorer.

        Args:
            coach_dir: Root directory for the coach instance.
        """
        self.coach_dir = coach_dir
        self.scorecard_path = coach_dir / "config" / "leadership_scorecard.json"

    def load_current_scorecard(self) -> Optional[LeadershipScorecard]:
        """Load the current scorecard, if it exists."""
        if not self.scorecard_path.exists():
            return None
        data = json.loads(self.scorecard_path.read_text(encoding="utf-8"))
        return LeadershipScorecard.model_validate(data)

    def is_rescore_due(self, current_scorecard: LeadershipScorecard) -> tuple[bool, int]:
        """Check if 12 weeks have elapsed since last scoring.

        Spec: 'Every 12 weeks, the Minister of Identity performs a full rescore.'

        Returns:
            Tuple of (is_due: bool, weeks_since_last: int).
        """
        from datetime import datetime, timezone

        last_updated = current_scorecard.last_updated
        created_at = getattr(current_scorecard, "created_at", None)

        dates = []
        for d_str in [last_updated, created_at]:
            if d_str:
                try:
                    dt = datetime.fromisoformat(d_str)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    dates.append(dt)
                except (ValueError, TypeError):
                    pass

        if not dates:
            return True, QUARTERLY_RESCORE_WEEKS

        last_dt = min(dates)
        now = datetime.now(timezone.utc)
        elapsed_days = (now - last_dt).days
        weeks_elapsed = elapsed_days // 7

        return weeks_elapsed >= QUARTERLY_RESCORE_WEEKS, weeks_elapsed

    def rescore(
        self,
        current_scorecard: LeadershipScorecard,
        force: bool = False,
    ) -> LeadershipScorecard:
        """Perform a full rescore from updated DEP objects.

        Spec §Quarterly Rescoring: full 12-trait rescore using latest DEP objects.
        AC12: Must produce at least 1 different score when DEP objects have been updated.

        Args:
            current_scorecard: The existing scorecard (used to preserve history).
            force: If True, bypass the 12-week interval check.

        Returns:
            Newly scored LeadershipScorecard with preserved history from current.

        Raises:
            QuarterlyRescorerTriggerError: If rescore is triggered too early and force=False.
        """
        from src.ccp.services.signal_source_loader import SignalSourceLoader
        from src.ccp.services.trait_scoring_engine import TraitScoringEngine
        from src.ccp.services.category_evaluator import CategoryEvaluator
        from src.ccp.services.format_governance_engine import FormatGovernanceEngine
        from src.ccp.services.scorecard_emitter import ScorecardEmitter
        from datetime import datetime, timezone

        if not force:
            is_due, weeks_elapsed = self.is_rescore_due(current_scorecard)
            if not is_due:
                raise QuarterlyRescorerTriggerError(
                    f"Rescore triggered after {weeks_elapsed} weeks. "
                    f"Minimum interval is {QUARTERLY_RESCORE_WEEKS} weeks. "
                    f"Use force=True to override."
                )

        # Load fresh signal sources
        loader = SignalSourceLoader(self.coach_dir)
        bundle = loader.load()

        # Score all 12 traits from fresh data
        scoring_engine = TraitScoringEngine(bundle)
        new_scored_traits = scoring_engine.score_all_traits()

        # Merge history from current scorecard into new traits
        new_scored_traits = self._merge_history(current_scorecard, new_scored_traits)

        # Detect CMM layer count and mode coverage from bundle
        cmm_layers = 0
        if bundle.cultural_memory_map_data:
            layers = bundle.cultural_memory_map_data.get("populated_layers", [])
            cmm_layers = len(layers) if isinstance(layers, list) else 0

        # Determine L1/L2/L3 depth and T/V/R coverage from tribe_soul
        depth_dist = bundle.tribe_soul_data.get("depth_distribution", {})
        l3_pct = depth_dist.get("l3_percentage", 0) if isinstance(depth_dist, dict) else 0
        l2_pct = depth_dist.get("l2_percentage", 0) if isinstance(depth_dist, dict) else 0
        has_depth = (l3_pct >= 10) or (l2_pct >= 30)

        mode_dist = bundle.tribe_soul_data.get("mode_distribution", {})
        modes_with_3 = sum(
            1 for mk in ["thought", "visceral", "reflective"]
            if isinstance(mode_dist, dict) and mode_dist.get(mk, 0) >= 3
        )
        has_tvr = modes_with_3 >= 3

        # Evaluate categories
        evaluator = CategoryEvaluator(
            scored_traits=new_scored_traits,
            cmm_populated_layers=cmm_layers,
            has_l1_l2_l3_depth=has_depth,
            has_tvr_mode_coverage=has_tvr,
        )
        category_results = evaluator.evaluate_all_categories()
        production_lock = evaluator.evaluate_production_lock()

        # Apply format governance
        governance_engine = FormatGovernanceEngine()
        new_scored_traits = governance_engine.apply_format_governance(new_scored_traits)

        # Assemble new scorecard
        emitter = ScorecardEmitter(self.coach_dir)
        new_scorecard = emitter.assemble_scorecard(
            coach_id=current_scorecard.coach_id,
            scored_traits=new_scored_traits,
            category_results=category_results,
            production_lock_result=production_lock,
            signal_sources=bundle.source_availability,
        )

        # Update version
        new_scorecard = new_scorecard.model_copy(update={
            "version": str(round(float(current_scorecard.version) + 0.1, 1)),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        })

        return new_scorecard

    def _merge_history(
        self,
        current_scorecard: LeadershipScorecard,
        new_traits: list,
    ) -> list:
        """Merge trait history from current scorecard into newly scored traits.

        Spec: Quarterly rescore preserves all prior evolution history.
        The new scores replace the current scores, but the history from weekly evolution
        is preserved in the new trait objects.
        """
        history_map = {t.name: t.history for t in current_scorecard.traits}

        merged = []
        for trait in new_traits:
            existing_history = history_map.get(trait.name, [])
            merged.append(trait.model_copy(update={"history": existing_history}))

        return merged

    def count_changed_traits(
        self,
        old_scorecard: LeadershipScorecard,
        new_scorecard: LeadershipScorecard,
    ) -> int:
        """Count how many trait scores changed between old and new scorecard.

        Used to verify AC12: 'produces different scores for at least 1 trait.'

        Returns:
            Number of traits with changed scores.
        """
        old_scores = {t.name: t.score for t in old_scorecard.traits}
        new_scores = {t.name: t.score for t in new_scorecard.traits}

        changed = sum(
            1 for name in old_scores
            if name in new_scores and old_scores[name] != new_scores[name]
        )
        return changed

    def save_rescored_scorecard(self, scorecard: LeadershipScorecard) -> None:
        """Write the rescored scorecard to disk."""
        self.scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
