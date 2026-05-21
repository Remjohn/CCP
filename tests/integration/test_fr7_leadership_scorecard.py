"""
FR7 Leadership Scorecard & Coach Development Engine — Integration Test Suite
Unit 10: All 12 Acceptance Criteria

Spec reference: FR7_Leadership_Scorecard_Tech_Spec.md §Acceptance Criteria

Test coverage:
  AC1  — ProductionLockGate: missing scorecard → PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD
  AC2  — CategoryEvaluator: failing Core Philosophy → PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: core_philosophy
  AC3  — ScoredTrait: empty evidence list raises ValueError
  AC4  — FormatGovernance: deep_empathy score=3 → ≥2 empathy-exercise archetypes assigned
  AC5  — FormatGovernance: archetypal_storytelling score=9 → showcase formats assigned
  AC6  — FormatGovernance: all-exercise or all-showcase → FormatRatioError raised
  AC7  — WeeklyEvolution: ≥3 sessions, sophia≥0.85, engagement>avg → score climbs by +1
  AC8  — Score clamping: push to 11 → stays 10; push to 0 → stays 1
  AC9  — SignalSourceLoader: missing ttt_baseline.json → MissingDependencyError
  AC10 — ScorecardEmitter.WRITE_TARGETS: only approved output paths
  AC11 — CategoryEvaluator: ComicHonesty=2 + cmm_layers=4 → Cultural Grounding coverage_met=True
  AC12 — QuarterlyRescorer.count_changed_traits: detects trait score changes
"""

import json
import uuid
from pathlib import Path

import pytest

# ─── Model imports ────────────────────────────────────────────────────────────
from src.ccp.models.leadership_scorecard_models import (
    CategoryCoverageResult,
    EvolutionAction,
    FormatAssignmentType,
    LeadershipScorecard,
    LeadershipScorecardPipelineSession,
    ProductionLockResult,
    ScoredTrait,
    SignalSourceAvailability,
    TraitCategory,
    TraitEvidence,
    TraitHistoryEntry,
    TraitName,
    WeeklySessionData,
    TraitSessionPerformance,
    MINIMUM_EVOLUTION_SESSIONS,
    SOPHIA_ALIGNMENT_CLIMB_THRESHOLD,
    STRONG_TRAIT_THRESHOLD,
    TRAIT_SCORE_MAX,
    TRAIT_SCORE_MIN,
    WEAK_TRAIT_THRESHOLD,
    EXERCISE_ARCHETYPE_MAP,
    SHOWCASE_ARCHETYPE_MAP,
)

# ─── Service imports ──────────────────────────────────────────────────────────
from src.ccp.services.category_evaluator import CategoryEvaluator
from src.ccp.services.format_governance_engine import FormatGovernanceEngine, FormatRatioError
from src.ccp.services.scorecard_emitter import ScorecardEmitter, ScorecardValidationError
from src.ccp.services.signal_source_loader import MissingDependencyError, SignalSourceLoader
from src.ccp.services.weekly_evolution_engine import WeeklyEvolutionEngine
from src.ccp.services.quarterly_rescorer import QuarterlyRescorer

# ─── Morgan gate imports ──────────────────────────────────────────────────────
from src.ccp.agents.morgan_orchestrator import ProductionLockGate


# ─── Shared helpers ───────────────────────────────────────────────────────────

def _make_evidence(n: int = 1) -> list[TraitEvidence]:
    """Create n TraitEvidence objects with minimal required fields."""
    return [
        TraitEvidence(
            signal_source=f"source_{i}",
            description=f"Test evidence item {i}",
            rubric_points=1,
        )
        for i in range(n)
    ]


def _make_scored_trait(
    name: TraitName,
    score: int,
    category: TraitCategory = TraitCategory.CORE_PHILOSOPHY,
    format_assignment: FormatAssignmentType = FormatAssignmentType.NEUTRAL,
    history: list[TraitHistoryEntry] | None = None,
) -> ScoredTrait:
    return ScoredTrait(
        trait_id=name.value,
        name=name,
        label=name.value.replace("_", " ").title(),
        score=score,
        category=category,
        evidence=_make_evidence(1),
        format_assignment=format_assignment,
        exercise_archetypes=EXERCISE_ARCHETYPE_MAP.get(name, []),
        showcase_archetypes=SHOWCASE_ARCHETYPE_MAP.get(name, []),
        history=history or [],
    )


def _make_all_12_traits(base_score: int = 6) -> list[ScoredTrait]:
    """Create all 12 required traits with a single base score."""
    trait_categories = {
        TraitName.DEEP_EMPATHY: TraitCategory.AUDIENCE_UNDERSTANDING,
        TraitName.AUTHENTIC_VULNERABILITY: TraitCategory.VOICE_AUTHENTICITY,
        TraitName.EMBODIED_CONFIDENCE: TraitCategory.VOICE_AUTHENTICITY,
        TraitName.EMOTIONAL_DEPTH: TraitCategory.CORE_PHILOSOPHY,
        TraitName.DEVOTIONAL_PASSION: TraitCategory.CORE_PHILOSOPHY,
        TraitName.MYSTIQUE_AND_AURA: TraitCategory.CULTURAL_GROUNDING,
        TraitName.ARCHETYPAL_STORYTELLING: TraitCategory.TEACHING_METHOD,
        TraitName.TRANSFORMATION_PROOF: TraitCategory.TEACHING_METHOD,
        TraitName.POLARIZING_CLARITY: TraitCategory.CORE_PHILOSOPHY,
        TraitName.EXPANSION_ENERGY: TraitCategory.AUDIENCE_UNDERSTANDING,
        TraitName.COMIC_HONESTY: TraitCategory.CULTURAL_GROUNDING,
        TraitName.DIRECTNESS: TraitCategory.VOICE_AUTHENTICITY,
    }
    return [
        _make_scored_trait(name, base_score, category=category)
        for name, category in trait_categories.items()
    ]


def _make_minimal_scorecard(
    coach_id: str = "TST-0000",
    base_score: int = 7,
    all_categories_met: bool = True,
) -> LeadershipScorecard:
    traits = _make_all_12_traits(base_score=base_score)
    all_cats = [cat for cat in TraitCategory]
    category_results = [
        CategoryCoverageResult(
            category=cat,
            traits=[t for t in traits if t.category == cat],
            coverage_met=True,
            threshold_description="test",
            details="",
        )
        for cat in all_cats
    ]
    production_lock = ProductionLockResult(
        all_categories_met=all_categories_met,
        locked_categories=[] if all_categories_met else [TraitCategory.CORE_PHILOSOPHY],
        unlock_message="All categories met." if all_categories_met else "",
        error_code="" if all_categories_met else "PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: core_philosophy",
    )
    signal_sources = SignalSourceAvailability(
        coach_soul=True,
        ttt_baseline=True,
        tribe_soul=True,
    )
    return LeadershipScorecard(
        coach_id=coach_id,
        traits=traits,
        category_coverage=category_results,
        production_lock=production_lock,
        signal_sources=signal_sources,
        version="7.0.0",
    )


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def coach_acronym() -> str:
    return "TST"


@pytest.fixture
def coach_id() -> str:
    return f"TST-{uuid.uuid4().hex[:4].upper()}"


@pytest.fixture
def tmp_coach_dir(tmp_path: Path, coach_acronym: str) -> Path:
    coach_dir = tmp_path / "coaches" / coach_acronym.lower()
    (coach_dir / "config").mkdir(parents=True)
    (coach_dir / "logs").mkdir(parents=True)
    return coach_dir


@pytest.fixture
def required_signal_files(tmp_coach_dir: Path) -> Path:
    """Write minimal required signal source JSON files for loader tests."""
    (tmp_coach_dir / "config" / "coach_soul.json").write_text(
        json.dumps({"coach_id": "TST-0001", "voice_profile": {}, "tribe_alignment": {}}),
        encoding="utf-8",
    )
    (tmp_coach_dir / "config" / "ttt_baseline.json").write_text(
        json.dumps({"tone_scores": {}, "tribe_match": {}}),
        encoding="utf-8",
    )
    (tmp_coach_dir / "config" / "tribe_soul.json").write_text(
        json.dumps({
            "tribe_name": "Test Tribe",
            "depth_distribution": {"l3_percentage": 15, "l2_percentage": 35},
            "mode_distribution": {"thought": 5, "visceral": 4, "reflective": 4},
        }),
        encoding="utf-8",
    )
    return tmp_coach_dir


# ══════════════════════════════════════════════════════════════════════════════
# AC1 — Production Lock Gate: missing scorecard
# ══════════════════════════════════════════════════════════════════════════════

class TestAC1ProductionLockGate:
    """AC1: 'Without a complete leadership_scorecard.json, triggering ccf-batch returns
    PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD from Morgan's gate — not a prompt failure.'
    """

    def test_missing_scorecard_returns_locked(self, tmp_coach_dir: Path) -> None:
        """Missing leadership_scorecard.json → passes=False."""
        gate = ProductionLockGate(tmp_coach_dir)
        passes, error_code, details = gate.check()
        assert passes is False

    def test_missing_scorecard_error_code_exact(self, tmp_coach_dir: Path) -> None:
        """Error code must be exactly PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD."""
        gate = ProductionLockGate(tmp_coach_dir)
        _, error_code, _ = gate.check()
        assert error_code == "PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD"

    def test_missing_scorecard_details_contains_path(self, tmp_coach_dir: Path) -> None:
        """Details dict must reference the expected path."""
        gate = ProductionLockGate(tmp_coach_dir)
        _, _, details = gate.check()
        assert "leadership_scorecard.json" in str(details)

    def test_valid_scorecard_unlocks_gate(self, tmp_coach_dir: Path) -> None:
        """With all 12 traits scored ≥1, gate passes."""
        scorecard_data = {
            "scores": {name.value: 5 for name in TraitName},
        }
        (tmp_coach_dir / "config" / "leadership_scorecard.json").write_text(
            json.dumps(scorecard_data), encoding="utf-8"
        )
        gate = ProductionLockGate(tmp_coach_dir)
        passes, error_code, _ = gate.check()
        assert passes is True
        assert error_code == ""


# ══════════════════════════════════════════════════════════════════════════════
# AC2 — CategoryEvaluator: Core Philosophy failure → production lock
# ══════════════════════════════════════════════════════════════════════════════

class TestAC2CategoryProductionLock:
    """AC2: 'A coach with all Core Philosophy traits scored below 4/10 cannot be produced —
    the system returns PRODUCTION_LOCKED_CATEGORY_INCOMPLETE: core_philosophy.'
    """

    def test_all_core_philosophy_below_4_locks_production(self) -> None:
        """All Core Philosophy traits at score=3 → CategoryEvaluator locks production."""
        core_philosophy_names = [
            TraitName.EMOTIONAL_DEPTH,
            TraitName.DEVOTIONAL_PASSION,
            TraitName.POLARIZING_CLARITY,
        ]
        traits = []
        for name in core_philosophy_names:
            traits.append(_make_scored_trait(name, score=3, category=TraitCategory.CORE_PHILOSOPHY))
        # Fill remaining 9 with passing scores across other categories
        other_names = [
            (TraitName.DEEP_EMPATHY, TraitCategory.AUDIENCE_UNDERSTANDING),
            (TraitName.AUTHENTIC_VULNERABILITY, TraitCategory.VOICE_AUTHENTICITY),
            (TraitName.EMBODIED_CONFIDENCE, TraitCategory.VOICE_AUTHENTICITY),
            (TraitName.MYSTIQUE_AND_AURA, TraitCategory.CULTURAL_GROUNDING),
            (TraitName.ARCHETYPAL_STORYTELLING, TraitCategory.TEACHING_METHOD),
            (TraitName.TRANSFORMATION_PROOF, TraitCategory.TEACHING_METHOD),
            (TraitName.EXPANSION_ENERGY, TraitCategory.AUDIENCE_UNDERSTANDING),
            (TraitName.COMIC_HONESTY, TraitCategory.CULTURAL_GROUNDING),
            (TraitName.DIRECTNESS, TraitCategory.VOICE_AUTHENTICITY),
        ]
        for name, cat in other_names:
            traits.append(_make_scored_trait(name, score=7, category=cat))

        evaluator = CategoryEvaluator(
            scored_traits=traits,
            cmm_populated_layers=7,
            has_l1_l2_l3_depth=True,
            has_tvr_mode_coverage=True,
        )
        lock = evaluator.evaluate_production_lock()
        assert lock.all_categories_met is False

    def test_production_lock_error_code_contains_core_philosophy(self) -> None:
        """Error code must name the failing category: core_philosophy."""
        core_philosophy_names = [
            TraitName.EMOTIONAL_DEPTH,
            TraitName.DEVOTIONAL_PASSION,
            TraitName.POLARIZING_CLARITY,
        ]
        traits = [_make_scored_trait(n, score=2, category=TraitCategory.CORE_PHILOSOPHY) for n in core_philosophy_names]
        other_names = [
            (TraitName.DEEP_EMPATHY, TraitCategory.AUDIENCE_UNDERSTANDING),
            (TraitName.AUTHENTIC_VULNERABILITY, TraitCategory.VOICE_AUTHENTICITY),
            (TraitName.EMBODIED_CONFIDENCE, TraitCategory.VOICE_AUTHENTICITY),
            (TraitName.MYSTIQUE_AND_AURA, TraitCategory.CULTURAL_GROUNDING),
            (TraitName.ARCHETYPAL_STORYTELLING, TraitCategory.TEACHING_METHOD),
            (TraitName.TRANSFORMATION_PROOF, TraitCategory.TEACHING_METHOD),
            (TraitName.EXPANSION_ENERGY, TraitCategory.AUDIENCE_UNDERSTANDING),
            (TraitName.COMIC_HONESTY, TraitCategory.CULTURAL_GROUNDING),
            (TraitName.DIRECTNESS, TraitCategory.VOICE_AUTHENTICITY),
        ]
        for name, cat in other_names:
            traits.append(_make_scored_trait(name, score=7, category=cat))

        evaluator = CategoryEvaluator(
            scored_traits=traits,
            cmm_populated_layers=7,
            has_l1_l2_l3_depth=True,
            has_tvr_mode_coverage=True,
        )
        lock = evaluator.evaluate_production_lock()
        assert "core_philosophy" in (lock.error_code or "").lower()

    def test_at_least_one_core_philosophy_at_4_passes(self) -> None:
        """One Core Philosophy trait at score=4 satisfies the category threshold."""
        traits = []
        core_names_scores = [
            (TraitName.EMOTIONAL_DEPTH, 4),  # exactly at threshold
            (TraitName.DEVOTIONAL_PASSION, 3),
            (TraitName.POLARIZING_CLARITY, 3),
        ]
        for name, score in core_names_scores:
            traits.append(_make_scored_trait(name, score=score, category=TraitCategory.CORE_PHILOSOPHY))
        other_names = [
            (TraitName.DEEP_EMPATHY, TraitCategory.AUDIENCE_UNDERSTANDING),
            (TraitName.AUTHENTIC_VULNERABILITY, TraitCategory.VOICE_AUTHENTICITY),
            (TraitName.EMBODIED_CONFIDENCE, TraitCategory.VOICE_AUTHENTICITY),
            (TraitName.MYSTIQUE_AND_AURA, TraitCategory.CULTURAL_GROUNDING),
            (TraitName.ARCHETYPAL_STORYTELLING, TraitCategory.TEACHING_METHOD),
            (TraitName.TRANSFORMATION_PROOF, TraitCategory.TEACHING_METHOD),
            (TraitName.EXPANSION_ENERGY, TraitCategory.AUDIENCE_UNDERSTANDING),
            (TraitName.COMIC_HONESTY, TraitCategory.CULTURAL_GROUNDING),
            (TraitName.DIRECTNESS, TraitCategory.VOICE_AUTHENTICITY),
        ]
        for name, cat in other_names:
            traits.append(_make_scored_trait(name, score=7, category=cat))

        evaluator = CategoryEvaluator(
            scored_traits=traits,
            cmm_populated_layers=7,
            has_l1_l2_l3_depth=True,
            has_tvr_mode_coverage=True,
        )
        core_result = evaluator._evaluate_core_philosophy()
        assert core_result.coverage_met is True


# ══════════════════════════════════════════════════════════════════════════════
# AC3 — ScoredTrait: empty evidence raises ValueError
# ══════════════════════════════════════════════════════════════════════════════

class TestAC3EvidenceRequired:
    """AC3: 'Every scored trait must carry ≥1 piece of supporting evidence.
    Attempting to create a ScoredTrait with an empty evidence list raises a ValidationError.'
    """

    def test_empty_evidence_raises_validation_error(self) -> None:
        """Empty evidence list must be rejected at Pydantic validation time."""
        with pytest.raises(Exception) as exc_info:  # Pydantic ValidationError is a subclass of ValueError
            ScoredTrait(
                trait_id="deep_empathy",
                name=TraitName.DEEP_EMPATHY,
                label="Deep Empathy",
                score=5,
                category=TraitCategory.AUDIENCE_UNDERSTANDING,
                evidence=[],  # AC3 violation
                format_assignment=FormatAssignmentType.NEUTRAL,
                exercise_archetypes=[],
                showcase_archetypes=[],
                history=[],
            )
        assert "evidence" in str(exc_info.value).lower() or "at least" in str(exc_info.value).lower()

    def test_single_evidence_accepted(self) -> None:
        """A single evidence item is sufficient."""
        trait = ScoredTrait(
            trait_id="deep_empathy",
            name=TraitName.DEEP_EMPATHY,
            label="Deep Empathy",
            score=5,
            category=TraitCategory.AUDIENCE_UNDERSTANDING,
            evidence=_make_evidence(1),
            format_assignment=FormatAssignmentType.NEUTRAL,
            exercise_archetypes=[],
            showcase_archetypes=[],
            history=[],
        )
        assert len(trait.evidence) == 1

    def test_multiple_evidence_accepted(self) -> None:
        """Multiple evidence items are accepted without error."""
        trait = ScoredTrait(
            trait_id="deep_empathy",
            name=TraitName.DEEP_EMPATHY,
            label="Deep Empathy",
            score=5,
            category=TraitCategory.AUDIENCE_UNDERSTANDING,
            evidence=_make_evidence(3),
            format_assignment=FormatAssignmentType.NEUTRAL,
            exercise_archetypes=[],
            showcase_archetypes=[],
            history=[],
        )
        assert len(trait.evidence) == 3


# ══════════════════════════════════════════════════════════════════════════════
# AC4 — FormatGovernance: deep_empathy weak → empathy-exercise archetypes
# ══════════════════════════════════════════════════════════════════════════════

class TestAC4DeepEmpathyExerciseAssignment:
    """AC4: 'A coach with deep_empathy = 3 receives ≥2 empathy-exercise archetypes in the
    exercise assignment (e.g. story_recognition, tweet_recognition).'
    """

    def test_deep_empathy_score_3_gets_exercise_assignment(self) -> None:
        """score=3 ≤ WEAK_TRAIT_THRESHOLD(5) → EXERCISE assignment."""
        traits = _make_all_12_traits(base_score=7)
        # Override deep_empathy to score=3
        traits = [
            _make_scored_trait(TraitName.DEEP_EMPATHY, score=3, category=TraitCategory.AUDIENCE_UNDERSTANDING)
            if t.name == TraitName.DEEP_EMPATHY else t
            for t in traits
        ]

        engine = FormatGovernanceEngine()
        result = engine.apply_format_governance(traits)
        empathy_trait = next(t for t in result if t.name == TraitName.DEEP_EMPATHY)

        assert empathy_trait.format_assignment == FormatAssignmentType.EXERCISE

    def test_deep_empathy_score_3_has_2_or_more_exercise_archetypes(self) -> None:
        """Exercise archetypes for deep_empathy must include ≥2 entries."""
        archetypes = EXERCISE_ARCHETYPE_MAP.get(TraitName.DEEP_EMPATHY, [])
        assert len(archetypes) >= 2, (
            f"deep_empathy EXERCISE_ARCHETYPE_MAP has only {len(archetypes)} archetype(s); expected ≥2"
        )

    def test_deep_empathy_exercise_archetypes_contain_recognition_types(self) -> None:
        """Exercise archetypes should include empathy-targeting formats."""
        archetypes = EXERCISE_ARCHETYPE_MAP.get(TraitName.DEEP_EMPATHY, [])
        archetype_str = " ".join(archetypes).lower()
        # At least one recognition-type format must appear (story_recognition or tweet_recognition)
        assert any(kw in archetype_str for kw in ["recognition", "empathy", "story", "tweet"]), (
            f"deep_empathy exercise archetypes do not contain recognition formats: {archetypes}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# AC5 — FormatGovernance: archetypal_storytelling score=9 → showcase
# ══════════════════════════════════════════════════════════════════════════════

class TestAC5ArchetypalStorytellingScoredHigh:
    """AC5: 'A coach with archetypal_storytelling = 9 receives story-based showcase formats
    in the weekly allocation.'
    """

    def test_score_9_gets_showcase_assignment(self) -> None:
        """score=9 ≥ STRONG_TRAIT_THRESHOLD(7) → SHOWCASE assignment."""
        traits = _make_all_12_traits(base_score=5)
        traits = [
            _make_scored_trait(TraitName.ARCHETYPAL_STORYTELLING, score=9, category=TraitCategory.TEACHING_METHOD)
            if t.name == TraitName.ARCHETYPAL_STORYTELLING else t
            for t in traits
        ]

        engine = FormatGovernanceEngine()
        result = engine.apply_format_governance(traits)
        storytelling_trait = next(t for t in result if t.name == TraitName.ARCHETYPAL_STORYTELLING)

        assert storytelling_trait.format_assignment == FormatAssignmentType.SHOWCASE

    def test_archetypal_storytelling_showcase_archetypes_populated(self) -> None:
        """archetypal_storytelling SHOWCASE_ARCHETYPE_MAP must have at least 1 archetype."""
        archetypes = SHOWCASE_ARCHETYPE_MAP.get(TraitName.ARCHETYPAL_STORYTELLING, [])
        assert len(archetypes) >= 1, (
            f"archetypal_storytelling SHOWCASE_ARCHETYPE_MAP is empty"
        )

    def test_archetypal_storytelling_showcase_contains_story_format(self) -> None:
        """Showcase archetypes should include story-format identifiers."""
        archetypes = SHOWCASE_ARCHETYPE_MAP.get(TraitName.ARCHETYPAL_STORYTELLING, [])
        archetype_str = " ".join(archetypes).lower()
        assert any(kw in archetype_str for kw in ["story", "thread", "narrative", "teaching"]), (
            f"archetypal_storytelling showcase archetypes don't include story formats: {archetypes}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# AC6 — FormatGovernance: 100% exercise or showcase → FormatRatioError
# ══════════════════════════════════════════════════════════════════════════════

class TestAC6FormatRatioGuard:
    """AC6: 'Weekly allocation is approximately 60% showcase / 40% exercise.
    If all assigned formats are 100% showcase or 100% exercise, the format governance
    validator rejects the assignment.'
    """

    def test_all_exercise_traits_raises_format_ratio_error(self) -> None:
        """12 traits all at score=1 → all EXERCISE → FormatRatioError."""
        traits = _make_all_12_traits(base_score=1)  # score=1 ≤ WEAK_TRAIT_THRESHOLD=5 → EXERCISE
        engine = FormatGovernanceEngine()
        with pytest.raises(FormatRatioError):
            engine.apply_format_governance(traits)

    def test_all_showcase_traits_raises_format_ratio_error(self) -> None:
        """12 traits all at score=10 → all SHOWCASE → FormatRatioError."""
        traits = _make_all_12_traits(base_score=10)  # score=10 ≥ STRONG_TRAIT_THRESHOLD=7 → SHOWCASE
        engine = FormatGovernanceEngine()
        with pytest.raises(FormatRatioError):
            engine.apply_format_governance(traits)

    def test_mixed_traits_pass_ratio_guard(self) -> None:
        """Mixed weak and strong traits must not raise FormatRatioError."""
        traits = []
        # 6 weak, 6 strong — guaranteed mixed
        names = list(TraitName)
        categories = [
            TraitCategory.AUDIENCE_UNDERSTANDING,
            TraitCategory.VOICE_AUTHENTICITY,
            TraitCategory.CORE_PHILOSOPHY,
            TraitCategory.TEACHING_METHOD,
            TraitCategory.CULTURAL_GROUNDING,
        ]
        for i, name in enumerate(names):
            score = 3 if i < 6 else 8
            cat = categories[i % len(categories)]
            traits.append(_make_scored_trait(name, score=score, category=cat))

        engine = FormatGovernanceEngine()
        result = engine.apply_format_governance(traits)
        assert len(result) == 12


# ══════════════════════════════════════════════════════════════════════════════
# AC7 — WeeklyEvolution: ≥3 sessions, criteria met → score climbs
# ══════════════════════════════════════════════════════════════════════════════

class TestAC7WeeklyEvolution:
    """AC7: 'A trait with 3+ exercise sessions, sophia_alignment ≥ 85%, and audience
    engagement above the weekly average climbs by +1 on next weekly evolution.'
    """

    def _make_scorecard_file(self, path: Path, trait_score: int = 5) -> None:
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=trait_score)
        path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _make_trait_with_3_sessions(self, base_score: int = 5) -> ScoredTrait:
        """Create a trait with exactly 3 prior exercise history entries (MINIMUM_EVOLUTION_SESSIONS)."""
        history = [
            TraitHistoryEntry(
                session_id=f"session_{i}",
                action=EvolutionAction.HOLD,
                sophia_alignment=0.90,
                chen_detection=False,
                audience_engagement_7d=0.70,
            )
            for i in range(MINIMUM_EVOLUTION_SESSIONS)
        ]
        return _make_scored_trait(
            TraitName.DEEP_EMPATHY,
            score=base_score,
            category=TraitCategory.AUDIENCE_UNDERSTANDING,
            history=history,
        )

    def test_trait_climbs_when_all_criteria_met(self, tmp_path: Path) -> None:
        """≥3 sessions + sophia ≥ 0.85 + engagement > avg → score +1."""
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=5)
        # Give deep_empathy 3 prior sessions so evolution can trigger
        history = [
            TraitHistoryEntry(
                session_id=f"session_{i}",
                action=EvolutionAction.HOLD,
                sophia_alignment=0.91,
                chen_detection=False,
                audience_engagement_7d=0.80,
                assignment_type=FormatAssignmentType.EXERCISE,
            )
            for i in range(MINIMUM_EVOLUTION_SESSIONS)
        ]
        # Replace deep_empathy trait with one that has history
        updated_traits = []
        for t in scorecard.traits:
            if t.name == TraitName.DEEP_EMPATHY:
                updated_traits.append(ScoredTrait(
                    trait_id=t.trait_id,
                    name=t.name,
                    label=t.label,
                    score=5,
                    category=t.category,
                    evidence=t.evidence,
                    format_assignment=t.format_assignment,
                    exercise_archetypes=t.exercise_archetypes,
                    showcase_archetypes=t.showcase_archetypes,
                    history=history,
                ))
            else:
                updated_traits.append(t)

        scorecard = scorecard.model_copy(update={"traits": updated_traits})

        scorecard_path = tmp_path / "leadership_scorecard.json"
        scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        session_data = WeeklySessionData(
            session_id="session_evolve",
            trait_updates=[
                TraitSessionPerformance(
                    trait_name=TraitName.DEEP_EMPATHY,
                    sophia_alignment=SOPHIA_ALIGNMENT_CLIMB_THRESHOLD,  # exactly 0.85
                    chen_detection=False,
                    audience_engagement_7d=0.85,  # above avg
                    assignment_type=FormatAssignmentType.EXERCISE,
                )
            ],
            coach_average_engagement=0.70,  # deep_empathy engagement (0.85) > avg (0.70)
        )

        engine = WeeklyEvolutionEngine(scorecard_path)
        updated_scorecard = engine.run(session_data)

        deep_empathy = next(t for t in updated_scorecard.traits if t.name == TraitName.DEEP_EMPATHY)
        assert deep_empathy.score == 6, (
            f"Expected score to climb from 5 → 6, got {deep_empathy.score}"
        )

    def test_trait_does_not_climb_without_minimum_sessions(self, tmp_path: Path) -> None:
        """Fewer than 3 sessions → NO evolution, score unchanged."""
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=5)
        scorecard_path = tmp_path / "leadership_scorecard.json"
        scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # 2 sessions on deep_empathy (below minimum)
        updated_traits = []
        for t in scorecard.traits:
            if t.name == TraitName.DEEP_EMPATHY:
                history = [
                    TraitHistoryEntry(
                        session_id=f"s{i}",
                        action=EvolutionAction.HOLD,
                        sophia_alignment=0.92,
                        chen_detection=False,
                        audience_engagement_7d=0.80,
                        assignment_type=FormatAssignmentType.EXERCISE,
                    )
                    for i in range(MINIMUM_EVOLUTION_SESSIONS - 1)  # only 2
                ]
                updated_traits.append(ScoredTrait(
                    trait_id=t.trait_id, name=t.name, label=t.label,
                    score=5, category=t.category, evidence=t.evidence,
                    format_assignment=t.format_assignment,
                    exercise_archetypes=t.exercise_archetypes,
                    showcase_archetypes=t.showcase_archetypes,
                    history=history,
                ))
            else:
                updated_traits.append(t)

        scorecard = scorecard.model_copy(update={"traits": updated_traits})
        scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        session_data = WeeklySessionData(
            session_id="session_no_evolve",
            trait_updates=[
                TraitSessionPerformance(
                    trait_name=TraitName.DEEP_EMPATHY,
                    sophia_alignment=0.95,
                    chen_detection=False,
                    audience_engagement_7d=0.90,
                    assignment_type=FormatAssignmentType.EXERCISE,
                )
            ],
            coach_average_engagement=0.50,
        )

        engine = WeeklyEvolutionEngine(scorecard_path)
        result_scorecard = engine.run(session_data)
        deep_empathy = next(t for t in result_scorecard.traits if t.name == TraitName.DEEP_EMPATHY)
        assert deep_empathy.score == 5, (
            f"Score should not change without minimum sessions, got {deep_empathy.score}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# AC8 — Score Clamping: never exceeds [1, 10]
# ══════════════════════════════════════════════════════════════════════════════

class TestAC8ScoreClamping:
    """AC8: 'Trait scores are clamped to the 1–10 range. A score that would be 11 stays
    10; a score that would be 0 stays 1.'
    """

    def test_score_cannot_exceed_10(self, tmp_path: Path) -> None:
        """A trait at score=10 that meets all climb criteria stays at 10."""
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=6)

        # Give deep_empathy score=10 with 3 sessions
        history = [
            TraitHistoryEntry(
                session_id=f"s{i}",
                action=EvolutionAction.CLIMB,
                sophia_alignment=0.95,
                chen_detection=False,
                audience_engagement_7d=0.90,
                assignment_type=FormatAssignmentType.EXERCISE,
            )
            for i in range(MINIMUM_EVOLUTION_SESSIONS)
        ]
        updated_traits = []
        for t in scorecard.traits:
            if t.name == TraitName.DEEP_EMPATHY:
                updated_traits.append(ScoredTrait(
                    trait_id=t.trait_id, name=t.name, label=t.label,
                    score=TRAIT_SCORE_MAX,  # already at ceiling
                    category=t.category, evidence=t.evidence,
                    format_assignment=t.format_assignment,
                    exercise_archetypes=t.exercise_archetypes,
                    showcase_archetypes=t.showcase_archetypes,
                    history=history,
                ))
            else:
                updated_traits.append(t)

        scorecard = scorecard.model_copy(update={"traits": updated_traits})
        scorecard_path = tmp_path / "leadership_scorecard.json"
        scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        session_data = WeeklySessionData(
            session_id="session_ceiling",
            trait_updates=[
                TraitSessionPerformance(
                    trait_name=TraitName.DEEP_EMPATHY,
                    sophia_alignment=0.95,
                    chen_detection=False,
                    audience_engagement_7d=0.90,
                    assignment_type=FormatAssignmentType.EXERCISE,
                )
            ],
            coach_average_engagement=0.50,
        )

        engine = WeeklyEvolutionEngine(scorecard_path)
        result_scorecard = engine.run(session_data)
        deep_empathy = next(t for t in result_scorecard.traits if t.name == TraitName.DEEP_EMPATHY)
        assert deep_empathy.score == TRAIT_SCORE_MAX, (
            f"Score at ceiling {TRAIT_SCORE_MAX} must not exceed it. Got {deep_empathy.score}"
        )

    def test_score_cannot_fall_below_1(self, tmp_path: Path) -> None:
        """A trait at score=1 that meets all decline criteria stays at 1."""
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=6)

        # deep_empathy at score=1 with 3 sophia failures
        history = [
            TraitHistoryEntry(
                session_id=f"s{i}",
                action=EvolutionAction.DECLINE,
                sophia_alignment=0.50,  # below climb threshold
                chen_detection=True,    # chen detected
                audience_engagement_7d=0.30,
                assignment_type=FormatAssignmentType.EXERCISE,
            )
            for i in range(MINIMUM_EVOLUTION_SESSIONS)
        ]
        updated_traits = []
        for t in scorecard.traits:
            if t.name == TraitName.DEEP_EMPATHY:
                updated_traits.append(ScoredTrait(
                    trait_id=t.trait_id, name=t.name, label=t.label,
                    score=TRAIT_SCORE_MIN,  # already at floor
                    category=t.category, evidence=t.evidence,
                    format_assignment=t.format_assignment,
                    exercise_archetypes=t.exercise_archetypes,
                    showcase_archetypes=t.showcase_archetypes,
                    history=history,
                ))
            else:
                updated_traits.append(t)

        scorecard = scorecard.model_copy(update={"traits": updated_traits})
        scorecard_path = tmp_path / "leadership_scorecard.json"
        scorecard_path.write_text(
            json.dumps(scorecard.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        session_data = WeeklySessionData(
            session_id="session_floor",
            trait_updates=[
                TraitSessionPerformance(
                    trait_name=TraitName.DEEP_EMPATHY,
                    sophia_alignment=0.40,  # below threshold
                    chen_detection=True,
                    audience_engagement_7d=0.20,
                    assignment_type=FormatAssignmentType.EXERCISE,
                )
            ],
            coach_average_engagement=0.50,
        )

        engine = WeeklyEvolutionEngine(scorecard_path)
        result_scorecard = engine.run(session_data)
        deep_empathy = next(t for t in result_scorecard.traits if t.name == TraitName.DEEP_EMPATHY)
        assert deep_empathy.score == TRAIT_SCORE_MIN, (
            f"Score at floor {TRAIT_SCORE_MIN} must not fall below it. Got {deep_empathy.score}"
        )

    def test_trait_score_constant_bounds(self) -> None:
        """Model constants must reflect the [1, 10] spec range."""
        assert TRAIT_SCORE_MIN == 1
        assert TRAIT_SCORE_MAX == 10
        assert TRAIT_SCORE_MIN < TRAIT_SCORE_MAX


# ══════════════════════════════════════════════════════════════════════════════
# AC9 — SignalSourceLoader: missing required dep → MissingDependencyError
# ══════════════════════════════════════════════════════════════════════════════

class TestAC9MissingDependency:
    """AC9: 'If ttt_baseline.json (DEP-ENG-005) is missing, the system raises
    CANNOT_SCORE_MISSING_DEPENDENCIES rather than scoring with incomplete data.'
    """

    def test_missing_ttt_baseline_raises_missing_dependency_error(
        self, tmp_coach_dir: Path
    ) -> None:
        """Only coach_soul.json and tribe_soul.json present — ttt_baseline.json absent."""
        (tmp_coach_dir / "config" / "coach_soul.json").write_text(
            json.dumps({"coach_id": "TST-0001"}), encoding="utf-8"
        )
        (tmp_coach_dir / "config" / "tribe_soul.json").write_text(
            json.dumps({"tribe_name": "Test"}), encoding="utf-8"
        )
        # ttt_baseline.json intentionally NOT written

        loader = SignalSourceLoader(tmp_coach_dir)
        with pytest.raises(MissingDependencyError) as exc_info:
            loader.load()

        assert "ttt_baseline" in str(exc_info.value).lower() or \
               "CANNOT_SCORE_MISSING_DEPENDENCIES" in str(exc_info.value)

    def test_error_code_is_cannot_score_missing_dependencies(
        self, tmp_coach_dir: Path
    ) -> None:
        """MissingDependencyError must carry the exact error code from spec."""
        (tmp_coach_dir / "config" / "coach_soul.json").write_text(
            json.dumps({}), encoding="utf-8"
        )
        # Both ttt_baseline and tribe_soul missing

        loader = SignalSourceLoader(tmp_coach_dir)
        with pytest.raises(MissingDependencyError) as exc_info:
            loader.load()

        exc = exc_info.value
        assert exc.error_code == "CANNOT_SCORE_MISSING_DEPENDENCIES"

    def test_all_required_present_no_error(self, required_signal_files: Path) -> None:
        """All 3 required files present → load() succeeds without exception."""
        loader = SignalSourceLoader(required_signal_files)
        bundle = loader.load()
        assert bundle.source_availability.coach_soul is True
        assert bundle.source_availability.ttt_baseline is True
        assert bundle.source_availability.tribe_soul is True


# ══════════════════════════════════════════════════════════════════════════════
# AC10 — ScorecardEmitter.WRITE_TARGETS: only approved output paths
# ══════════════════════════════════════════════════════════════════════════════

class TestAC10WriteTargetRestriction:
    """AC10: 'The Minister of Identity is read-only — it reads existing DEP objects and
    writes ONLY to leadership_scorecard.json and 02_content_strategy.md.'
    """

    def test_write_targets_is_frozenset(self) -> None:
        """WRITE_TARGETS must be immutable (frozenset)."""
        assert isinstance(ScorecardEmitter.WRITE_TARGETS, frozenset)

    def test_write_targets_contains_leadership_scorecard(self) -> None:
        """leadership_scorecard.json must be a permitted write target."""
        assert any("leadership_scorecard.json" in t for t in ScorecardEmitter.WRITE_TARGETS)

    def test_write_targets_contains_content_strategy(self) -> None:
        """02_content_strategy.md must be a permitted write target."""
        assert any("02_content_strategy" in t for t in ScorecardEmitter.WRITE_TARGETS)

    def test_write_targets_does_not_contain_coach_soul(self) -> None:
        """coach_soul.json is a source DEP — must NOT be in WRITE_TARGETS."""
        for target in ScorecardEmitter.WRITE_TARGETS:
            assert "coach_soul" not in target, (
                f"WRITE_TARGETS must not include coach_soul.json, found: {target}"
            )

    def test_write_targets_does_not_contain_ttt_baseline(self) -> None:
        """ttt_baseline.json is a source DEP — must NOT be in WRITE_TARGETS."""
        for target in ScorecardEmitter.WRITE_TARGETS:
            assert "ttt_baseline" not in target

    def test_write_targets_does_not_contain_tribe_soul(self) -> None:
        """tribe_soul.json is a source DEP — must NOT be in WRITE_TARGETS."""
        for target in ScorecardEmitter.WRITE_TARGETS:
            assert "tribe_soul" not in target

    def test_write_targets_has_exactly_2_entries(self) -> None:
        """WRITE_TARGETS should have exactly 2 permitted outputs per spec."""
        assert len(ScorecardEmitter.WRITE_TARGETS) == 2


# ══════════════════════════════════════════════════════════════════════════════
# AC11 — CategoryEvaluator: ComicHonesty=2, cmm_layers=4 → Cultural Grounding passes
# ══════════════════════════════════════════════════════════════════════════════

class TestAC11CulturalGroundingCMMLayerGate:
    """AC11: 'Cultural Grounding evaluates CMM layer completeness (7 layers), NOT individual
    trait scores. A coach with comic_honesty = 2 but a fully populated CMM passes Cultural Grounding.'
    """

    def test_comic_honesty_2_with_cmm_4_layers_passes_cultural_grounding(self) -> None:
        """Low comic_honesty score does NOT block Cultural Grounding when cmm_layers ≥ 4."""
        traits = _make_all_12_traits(base_score=7)
        # Explicitly set both cultural traits to low scores
        traits = [
            _make_scored_trait(t.name, score=2, category=TraitCategory.CULTURAL_GROUNDING)
            if t.name in (TraitName.COMIC_HONESTY, TraitName.MYSTIQUE_AND_AURA)
            else t
            for t in traits
        ]

        evaluator = CategoryEvaluator(
            scored_traits=traits,
            cmm_populated_layers=4,  # ≥ 4 → threshold met
            has_l1_l2_l3_depth=True,
            has_tvr_mode_coverage=True,
        )
        cultural_result = evaluator._evaluate_cultural_grounding()
        assert cultural_result.coverage_met is True, (
            f"Cultural Grounding should pass with cmm_layers=4, "
            f"even with comic_honesty=2. coverage_met={cultural_result.coverage_met}"
        )

    def test_cmm_3_layers_fails_cultural_grounding(self) -> None:
        """cmm_layers=3 (< 4) → Cultural Grounding coverage_met=False, regardless of trait scores."""
        traits = _make_all_12_traits(base_score=9)  # All traits at max score

        evaluator = CategoryEvaluator(
            scored_traits=traits,
            cmm_populated_layers=3,  # below threshold
            has_l1_l2_l3_depth=True,
            has_tvr_mode_coverage=True,
        )
        cultural_result = evaluator._evaluate_cultural_grounding()
        assert cultural_result.coverage_met is False, (
            f"Cultural Grounding should FAIL with cmm_layers=3 even if trait scores are all 9."
        )

    def test_full_production_lock_with_comic_honesty_2_and_cmm_4(self) -> None:
        """Full production lock eval: comic_honesty=2 does NOT cause CATEGORY_INCOMPLETE."""
        traits = _make_all_12_traits(base_score=7)
        traits = [
            _make_scored_trait(t.name, score=2, category=TraitCategory.CULTURAL_GROUNDING)
            if t.name == TraitName.COMIC_HONESTY
            else t
            for t in traits
        ]

        evaluator = CategoryEvaluator(
            scored_traits=traits,
            cmm_populated_layers=4,
            has_l1_l2_l3_depth=True,
            has_tvr_mode_coverage=True,
        )
        lock = evaluator.evaluate_production_lock()
        # Production lock must not fail due to Cultural Grounding when CMM has ≥4 layers
        assert "cultural_grounding" not in (lock.error_code or "").lower()


# ══════════════════════════════════════════════════════════════════════════════
# AC12 — QuarterlyRescorer: count_changed_traits detects score changes
# ══════════════════════════════════════════════════════════════════════════════

class TestAC12QuarterlyRescore:
    """AC12: 'Quarterly rescore runs every 12 weeks. A full re-evaluation against current
    signals updates each of the 12 traits to the new signal-derived score, and the system
    logs how many traits changed score versus the prior quarter.'
    """

    def test_count_changed_traits_detects_differences(self, tmp_coach_dir: Path) -> None:
        """count_changed_traits() returns correct count when scores differ."""
        old_scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=5)
        new_scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=7)

        rescorer = QuarterlyRescorer(tmp_coach_dir)
        changed = rescorer.count_changed_traits(old_scorecard, new_scorecard)
        # All 12 traits changed from score 5 → 7
        assert changed == 12

    def test_count_changed_traits_zero_when_identical(self, tmp_coach_dir: Path) -> None:
        """count_changed_traits() returns 0 when both scorecards have identical scores."""
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=6)
        rescorer = QuarterlyRescorer(tmp_coach_dir)
        changed = rescorer.count_changed_traits(scorecard, scorecard)
        assert changed == 0

    def test_count_changed_traits_partial_change(self, tmp_coach_dir: Path) -> None:
        """count_changed_traits() returns partial count when only some traits change."""
        old_scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=5)

        # Modify only deep_empathy in new scorecard
        new_traits = [
            ScoredTrait(
                trait_id=t.trait_id, name=t.name, label=t.label,
                score=8 if t.name == TraitName.DEEP_EMPATHY else t.score,  # only 1 changes
                category=t.category, evidence=t.evidence,
                format_assignment=t.format_assignment,
                exercise_archetypes=t.exercise_archetypes,
                showcase_archetypes=t.showcase_archetypes,
                history=t.history,
            )
            for t in old_scorecard.traits
        ]
        new_scorecard = old_scorecard.model_copy(update={"traits": new_traits})

        rescorer = QuarterlyRescorer(tmp_coach_dir)
        changed = rescorer.count_changed_traits(old_scorecard, new_scorecard)
        assert changed == 1

    def test_is_rescore_due_before_12_weeks_returns_false(self, tmp_coach_dir: Path) -> None:
        """is_rescore_due() returns False when fewer than 12 weeks have elapsed."""
        from datetime import datetime, timezone, timedelta
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=6)

        # Set created_at to 6 weeks ago
        six_weeks_ago = (datetime.now(timezone.utc) - timedelta(weeks=6)).isoformat()
        scorecard = scorecard.model_copy(update={"created_at": six_weeks_ago})

        rescorer = QuarterlyRescorer(tmp_coach_dir)
        is_due, weeks_elapsed = rescorer.is_rescore_due(scorecard)
        assert is_due is False
        assert weeks_elapsed < 12

    def test_is_rescore_due_after_12_weeks_returns_true(self, tmp_coach_dir: Path) -> None:
        """is_rescore_due() returns True when ≥12 weeks have elapsed."""
        from datetime import datetime, timezone, timedelta
        scorecard = _make_minimal_scorecard(coach_id="TST-0001", base_score=6)

        # Set created_at to 13 weeks ago
        thirteen_weeks_ago = (datetime.now(timezone.utc) - timedelta(weeks=13)).isoformat()
        scorecard = scorecard.model_copy(update={"created_at": thirteen_weeks_ago})

        rescorer = QuarterlyRescorer(tmp_coach_dir)
        is_due, weeks_elapsed = rescorer.is_rescore_due(scorecard)
        assert is_due is True
        assert weeks_elapsed >= 12
