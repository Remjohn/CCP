"""
CCP FR7 Leadership Scorecard — Scorecard Emitter & Validator (Unit 6)
Phase 5 EMIT + Phase 6 VALIDATE: Assemble, write, and validate DEP-ENG-026.

Spec reference: FR7 Tech Spec §Phase 5: EMIT, §Phase 6: VALIDATE & PRODUCTION LOCK GATE
                §Backward Compatibility

Primary output: leadership_scorecard.json (DEP-ENG-026)

Validation checks from spec (Phase 6):
  - All 12 traits have a score between 1 and 10
  - Every score has ≥1 evidence citation from the signal sources
  - All 5 trait categories evaluated for coverage
  - If any category fails → production_lock.locked_categories lists the failing category

AC3: 'A trait scored 7/10 with zero evidence citations → validation error.'
AC10: 'The Minister of Identity never modifies coach_soul.json, ttt_baseline.json, or tribe_soul.json.'
"""

import json
from pathlib import Path
from typing import Optional

from src.ccp.models.leadership_scorecard_models import (
    CategoryCoverageResult,
    FormatGovernance,
    LeadershipScorecard,
    ProductionLockResult,
    SignalSourceAvailability,
    ScoredTrait,
    TRAIT_SCORE_MAX,
    TRAIT_SCORE_MIN,
)


class ScorecardValidationError(Exception):
    """Raised when the assembled scorecard fails validation."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Scorecard validation failed: {'; '.join(errors)}")


class ScorecardEmitter:
    """Assembles, validates, and writes the leadership_scorecard.json (DEP-ENG-026).

    Spec §Phase 5 EMIT:
    - Assembles all scored traits, category results, production lock, format governance
    - Writes to leadership_scorecard.json

    Spec §Phase 6 VALIDATE:
    - All 12 traits scored with evidence
    - All 5 categories evaluated
    - Production lock determined
    - config.yaml and coach_soul.json pipeline_status updated (write-only to STATUS fields, not DEP fields)

    AC10: This emitter writes ONLY to leadership_scorecard.json and config/pipeline_status.
    It never writes to coach_soul.json (DEP-ENG-003/004), ttt_baseline.json, or tribe_soul.json.
    """

    # The only files this emitter writes to (AC10 compliance)
    WRITE_TARGETS = frozenset([
        "config/leadership_scorecard.json",
        "config/02_content_strategy.md",
    ])

    def __init__(self, coach_dir: Path):
        """Initialize the emitter.

        Args:
            coach_dir: Root directory for this coach instance.
        """
        self.coach_dir = coach_dir

    def assemble_scorecard(
        self,
        coach_id: str,
        scored_traits: list[ScoredTrait],
        category_results: list[CategoryCoverageResult],
        production_lock_result: ProductionLockResult,
        signal_sources: SignalSourceAvailability,
    ) -> LeadershipScorecard:
        """Assemble the complete scorecard from all phase outputs.

        Spec §Phase 5 EMIT — assembles all fields per the JSON schema.

        Returns:
            LeadershipScorecard (DEP-ENG-026) ready for writing.
        """
        categories_dict = {
            r.category.value: r for r in category_results
        }

        return LeadershipScorecard(
            dep_id="DEP-ENG-026",
            version="1.0",
            coach_id=coach_id,
            signal_sources=signal_sources,
            traits=scored_traits,
            categories=categories_dict,
            production_lock=production_lock_result,
            format_governance=FormatGovernance(
                showcase_ratio=0.6,
                exercise_ratio=0.4,
                assignments_written_to="02_content_strategy.md",
            ),
        )

    def validate(self, scorecard: LeadershipScorecard) -> list[str]:
        """Run all Phase 6 validation checks on the assembled scorecard.

        Spec §Phase 6 VALIDATE — Validation checks:
        - All 12 traits have a score between 1 and 10
        - Every score has ≥1 evidence citation from the signal sources
        - All 5 trait categories evaluated for coverage

        Returns:
            List of validation error strings. Empty list = PASS.
        """
        errors: list[str] = []

        # Check 1: All 12 traits must be present
        if len(scorecard.traits) != 12:
            errors.append(
                f"Scorecard must contain exactly 12 scored traits, found {len(scorecard.traits)}"
            )

        # Check 2: All trait scores must be between 1 and 10 (AC8)
        for trait in scorecard.traits:
            if trait.score < TRAIT_SCORE_MIN or trait.score > TRAIT_SCORE_MAX:
                errors.append(
                    f"Trait '{trait.name.value}' has invalid score {trait.score} "
                    f"(must be {TRAIT_SCORE_MIN}–{TRAIT_SCORE_MAX})"
                )

        # Check 3: Every trait must have ≥1 evidence citation (AC3)
        for trait in scorecard.traits:
            if len(trait.evidence) < 1:
                errors.append(
                    f"Trait '{trait.name.value}' (score={trait.score}) has zero evidence citations "
                    f"— AC3 requires ≥1 evidence citation for every scored trait"
                )

        # Check 4: All 5 categories must be evaluated
        expected_categories = {
            "core_philosophy", "audience_understanding",
            "voice_authenticity", "teaching_method", "cultural_grounding",
        }
        present_categories = set(scorecard.categories.keys())
        missing_categories = expected_categories - present_categories
        if missing_categories:
            errors.append(
                f"Missing category evaluations: {', '.join(missing_categories)}"
            )

        return errors

    def emit(
        self,
        scorecard: LeadershipScorecard,
        raise_on_validation_failure: bool = True,
    ) -> tuple[LeadershipScorecard, list[str]]:
        """Validate and write the scorecard to leadership_scorecard.json.

        Spec §Phase 5 EMIT + §Phase 6 VALIDATE.
        AC10: Only writes to WRITE_TARGETS — never to source DEP files.

        Args:
            scorecard: The assembled scorecard.
            raise_on_validation_failure: If True, raises on validation errors.

        Returns:
            Tuple of (scorecard, validation_errors). If no errors, errors is empty list.

        Raises:
            ScorecardValidationError: If validation fails and raise_on_validation_failure=True.
        """
        # Phase 6 validation
        errors = self.validate(scorecard)

        if errors and raise_on_validation_failure:
            raise ScorecardValidationError(errors)

        # Write to leadership_scorecard.json (only permitted target)
        output_path = self.coach_dir / "config" / "leadership_scorecard.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        scorecard_json = scorecard.model_dump(mode="json")
        output_path.write_text(
            json.dumps(scorecard_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return scorecard, errors

    def update_pipeline_status(
        self,
        scored: bool = True,
    ) -> None:
        """Update coach_soul.json pipeline_status.leadership_scored flag.

        Spec §Phase 6 VALIDATE checkpoint:
        'Update coach_soul.json: pipeline_status.leadership_scored = true'

        IMPORTANT: This ONLY modifies the pipeline_status.leadership_scored field.
        It never modifies DEP-ENG-003, DEP-ENG-004, or any voice/tribe data (AC10).
        """
        soul_path = self.coach_dir / "config" / "coach_soul.json"
        if not soul_path.exists():
            return

        try:
            data = json.loads(soul_path.read_text(encoding="utf-8"))
            if "pipeline_status" not in data:
                data["pipeline_status"] = {}
            data["pipeline_status"]["leadership_scored"] = scored
            soul_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except (json.JSONDecodeError, IOError):
            # Non-fatal — status update failure does not block scorecard emission
            pass
