"""
CCP FR7 Leadership Scorecard — Category Evaluator (Unit 4)
Phase 3 CATEGORIZE: 5 category coverage evaluation with thresholds.

Spec reference: FR7 Tech Spec §Phase 3: CATEGORIZE — 5 Trait Categories
Architecture reference: §11.6 (Leadership Trait Governance)

After individual scoring, traits are grouped into 5 coverage categories for the
production lock gate. ALL 5 categories must meet their coverage requirement.

Category thresholds from spec:
  Core Philosophy:        At least 1 trait ≥ 4/10
  Audience Understanding: At least 1 trait ≥ 5/10 with L1/L2/L3 depth
  Voice Authenticity:     At least 2 traits ≥ 5/10
  Teaching Method:        At least 1 trait ≥ 5/10 covering all 3 T/V/R modes
  Cultural Grounding:     Minimum 4 of 7 CMM layers populated

AC2: 'A coach with all 12 traits scored but Core Philosophy category failing →
      returns PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: core_philosophy.'
AC11: 'Comic Honesty=2/10 does NOT trigger production lock (Cultural Grounding checks
       CMM layers, not individual trait scores).'
"""

from typing import Any, Optional

from src.ccp.models.leadership_scorecard_models import (
    CATEGORY_TRAIT_MAP,
    CategoryCoverageResult,
    ProductionLockResult,
    ScoredTrait,
    TraitCategory,
    TraitName,
)


class CategoryEvaluator:
    """Evaluates 5 trait categories for production lock gate coverage.

    Spec §Phase 3 CATEGORIZE: traits grouped into 5 categories.
    Production lock gate: ALL 5 must meet their coverage requirement.
    """

    def __init__(
        self,
        scored_traits: list[ScoredTrait],
        cmm_populated_layers: int = 0,
        has_l1_l2_l3_depth: bool = False,
        has_tvr_mode_coverage: bool = False,
    ):
        """Initialize the evaluator.

        Args:
            scored_traits: All 12 scored traits from Phase 2.
            cmm_populated_layers: Number of CMM layers populated (0-7).
                                  Spec Cultural Grounding: 'Minimum 4 of 7 CMM layers populated.'
            has_l1_l2_l3_depth: Whether the tribe soul demonstrates L1/L2/L3 depth coverage.
                                Spec Audience Understanding: 'with L1/L2/L3 depth.'
            has_tvr_mode_coverage: Whether all 3 T/V/R modes are covered.
                                  Spec Teaching Method: 'covering all 3 T/V/R modes.'
        """
        self._traits = {t.name: t for t in scored_traits}
        self._cmm_layers = cmm_populated_layers
        self._has_depth = has_l1_l2_l3_depth
        self._has_tvr = has_tvr_mode_coverage

    def _get_trait_score(self, name: TraitName) -> int:
        """Get the score for a trait by name."""
        trait = self._traits.get(name)
        return trait.score if trait else 0

    def evaluate_all_categories(self) -> list[CategoryCoverageResult]:
        """Evaluate all 5 categories and return results.

        Returns:
            List of 5 CategoryCoverageResult objects.
        """
        return [
            self._evaluate_core_philosophy(),
            self._evaluate_audience_understanding(),
            self._evaluate_voice_authenticity(),
            self._evaluate_teaching_method(),
            self._evaluate_cultural_grounding(),
        ]

    def evaluate_production_lock(self) -> ProductionLockResult:
        """Evaluate the production lock gate across all 5 categories.

        Spec §Phase 6 VALIDATE — Production lock enforcement:
        IF ANY category has coverage_met = false:
          RETURN PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: {category_name}
        ELSE:
          production_lock.all_categories_met = true
          UNLOCK production pipeline

        Returns:
            ProductionLockResult with lock status.
        """
        category_results = self.evaluate_all_categories()
        locked: list[str] = []

        for result in category_results:
            if not result.coverage_met:
                locked.append(result.category.value)

        if locked:
            # AC2: specific category failure message
            first_failure = locked[0]
            return ProductionLockResult(
                all_categories_met=False,
                locked_categories=locked,
                unlock_message=(
                    f"The coach needs additional {first_failure.replace('_', ' ')} evidence "
                    f"before production can begin. Options: (1) Additional Sacred Audio session, "
                    f"(2) Deeper tribe research, (3) Story Archive enrichment"
                ),
                error_code=f"PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: {first_failure}",
            )

        return ProductionLockResult(
            all_categories_met=True,
            locked_categories=[],
            unlock_message="All 5 categories meet coverage requirements. Production unlocked.",
            error_code="",
        )

    # ── Category 1: Core Philosophy ──────────────────────────────
    # Traits: Devotional Passion, Expansion Energy
    # Threshold: At least 1 trait ≥ 4/10

    def _evaluate_core_philosophy(self) -> CategoryCoverageResult:
        """Spec §Phase 3: Core Philosophy — at least 1 trait ≥ 4/10."""
        traits = CATEGORY_TRAIT_MAP[TraitCategory.CORE_PHILOSOPHY]
        scores = {t: self._get_trait_score(t) for t in traits}
        passing = [t for t, s in scores.items() if s >= 4]

        return CategoryCoverageResult(
            category=TraitCategory.CORE_PHILOSOPHY,
            traits=traits,
            coverage_met=len(passing) >= 1,
            threshold_description="At least 1 trait ≥ 4/10",
            details={
                "trait_scores": {t.value: s for t, s in scores.items()},
                "passing_traits": [t.value for t in passing],
                "required_passing": 1,
            },
        )

    # ── Category 2: Audience Understanding ───────────────────────
    # Traits: Deep Empathy, Polarizing Clarity
    # Threshold: At least 1 trait ≥ 5/10 with L1/L2/L3 depth

    def _evaluate_audience_understanding(self) -> CategoryCoverageResult:
        """Spec §Phase 3: Audience Understanding — at least 1 trait ≥ 5/10 with L1/L2/L3 depth."""
        traits = CATEGORY_TRAIT_MAP[TraitCategory.AUDIENCE_UNDERSTANDING]
        scores = {t: self._get_trait_score(t) for t in traits}
        passing_score = [t for t, s in scores.items() if s >= 5]

        # Must have both score threshold AND depth coverage
        coverage_met = len(passing_score) >= 1 and self._has_depth

        return CategoryCoverageResult(
            category=TraitCategory.AUDIENCE_UNDERSTANDING,
            traits=traits,
            coverage_met=coverage_met,
            threshold_description="At least 1 trait ≥ 5/10 with L1/L2/L3 depth",
            details={
                "trait_scores": {t.value: s for t, s in scores.items()},
                "passing_traits_by_score": [t.value for t in passing_score],
                "has_l1_l2_l3_depth": self._has_depth,
                "required_passing": 1,
            },
        )

    # ── Category 3: Voice Authenticity ───────────────────────────
    # Traits: Authentic Vulnerability, Embodied Confidence, Directness
    # Threshold: At least 2 traits ≥ 5/10

    def _evaluate_voice_authenticity(self) -> CategoryCoverageResult:
        """Spec §Phase 3: Voice Authenticity — at least 2 traits ≥ 5/10."""
        traits = CATEGORY_TRAIT_MAP[TraitCategory.VOICE_AUTHENTICITY]
        scores = {t: self._get_trait_score(t) for t in traits}
        passing = [t for t, s in scores.items() if s >= 5]

        return CategoryCoverageResult(
            category=TraitCategory.VOICE_AUTHENTICITY,
            traits=traits,
            coverage_met=len(passing) >= 2,
            threshold_description="At least 2 traits ≥ 5/10",
            details={
                "trait_scores": {t.value: s for t, s in scores.items()},
                "passing_traits": [t.value for t in passing],
                "required_passing": 2,
            },
        )

    # ── Category 4: Teaching Method ──────────────────────────────
    # Traits: Emotional Depth, Archetypal Storytelling, Transformation Proof
    # Threshold: At least 1 trait ≥ 5/10 covering all 3 T/V/R modes

    def _evaluate_teaching_method(self) -> CategoryCoverageResult:
        """Spec §Phase 3: Teaching Method — at least 1 trait ≥ 5/10 covering all 3 T/V/R modes."""
        traits = CATEGORY_TRAIT_MAP[TraitCategory.TEACHING_METHOD]
        scores = {t: self._get_trait_score(t) for t in traits}
        passing_score = [t for t, s in scores.items() if s >= 5]

        # Must have both score threshold AND T/V/R mode coverage
        coverage_met = len(passing_score) >= 1 and self._has_tvr

        return CategoryCoverageResult(
            category=TraitCategory.TEACHING_METHOD,
            traits=traits,
            coverage_met=coverage_met,
            threshold_description="At least 1 trait ≥ 5/10 covering all 3 T/V/R modes",
            details={
                "trait_scores": {t.value: s for t, s in scores.items()},
                "passing_traits_by_score": [t.value for t in passing_score],
                "has_tvr_mode_coverage": self._has_tvr,
                "required_passing": 1,
            },
        )

    # ── Category 5: Cultural Grounding ───────────────────────────
    # Traits: Mystique & Aura, Comic Honesty
    # Threshold: Minimum 4 of 7 CMM layers populated
    # AC11: checks CMM layers, NOT individual trait scores

    def _evaluate_cultural_grounding(self) -> CategoryCoverageResult:
        """Spec §Phase 3: Cultural Grounding — Minimum 4 of 7 CMM layers populated.

        AC11: 'A coach scoring 2/10 on Comic Honesty → this does NOT trigger production lock.
        Cultural Grounding checks CMM layers, not individual trait scores.'
        """
        traits = CATEGORY_TRAIT_MAP[TraitCategory.CULTURAL_GROUNDING]
        scores = {t: self._get_trait_score(t) for t in traits}

        # Coverage is based on CMM layers, NOT trait scores (AC11)
        coverage_met = self._cmm_layers >= 4

        return CategoryCoverageResult(
            category=TraitCategory.CULTURAL_GROUNDING,
            traits=traits,
            coverage_met=coverage_met,
            threshold_description="Minimum 4 of 7 CMM layers populated",
            details={
                "trait_scores": {t.value: s for t, s in scores.items()},
                "cmm_layers_populated": self._cmm_layers,
                "cmm_layers_required": 4,
                "note": "Coverage based on CMM layer population, not individual trait scores (AC11)",
            },
        )
