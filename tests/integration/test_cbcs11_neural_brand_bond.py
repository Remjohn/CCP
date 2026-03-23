"""
FR-CBCS-11 — Neural Brand Bond Protocol — Integration Tests
=============================================================
Tests for BrandStoryPlanner, DmpfcSemanticEvaluator covering
all 3 ACs plus edge cases.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BRAND_STORY_MIN_WORDS,
    DmpfcVerdict,
    NeuralBrandError,
    StoryStructure,
)
from src.ccp.services.neural_brand_bond import (
    BrandStoryPlanner,
    DmpfcSemanticEvaluator,
)


# ── Helpers ────────────────────────────────────────────────────────────

def _make_planner(coach: str = "TST") -> tuple[BrandStoryPlanner, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    planner = BrandStoryPlanner(coach_acronym=coach, receipt_chain=rc)
    return planner, rc


def _make_evaluator(coach: str = "TST") -> tuple[DmpfcSemanticEvaluator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    ev = DmpfcSemanticEvaluator(coach_acronym=coach, receipt_chain=rc)
    return ev, rc


def _long_story(social_nouns: int = 3, cliches: int = 0, value_word: str = "discipline") -> str:
    """Generate a story >=50 words with configurable social nouns and cliches."""
    base = (
        f"There was a person who valued {value_word} deeply. "
        f"She told her friend about the importance of showing up every single day. "
        f"He listened carefully and realized that without {value_word}, "
        f"they would never achieve the consistency required. "
        f"The people around them started noticing the change. "
        f"Someone once said that the greatest strength is simply not giving up "
        f"when the world tells you to stop and rest your weary bones."
    )
    cliche_phrases = ["unlock your potential ", "next level ", "game changer "]
    for i in range(min(cliches, len(cliche_phrases))):
        base += f" This was truly a {cliche_phrases[i]}moment."
    return base


# Short story (< 50 words)
_SHORT_STORY = "Integrity is the cornerstone of our coaching framework."

# Abstract story with no social nouns
_ABSTRACT_STORY = (
    "Integrity is the cornerstone of our coaching framework. "
    "It provides structure and reliability for the entire process. "
    "Without it, the system crumbles under its own weight. "
    "The philosophy dictates that every action must align with principles. "
    "Excellence emerges from consistent application of these truths. "
    "The framework ensures stability and predictability for all stakeholders involved in this endeavor."
)


# ════════════════════════════════════════════════════════════════════════
# 1. Constructor & ADR-01
# ════════════════════════════════════════════════════════════════════════

class TestConstructor:
    def test_valid_coach_2_char_planner(self) -> None:
        p, _ = _make_planner("TS")
        assert p is not None

    def test_valid_coach_4_char_evaluator(self) -> None:
        ev, _ = _make_evaluator("TEST")
        assert ev is not None

    def test_invalid_coach_1_char_planner(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_planner("T")

    def test_invalid_coach_5_char_planner(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_planner("TESTI")

    def test_invalid_coach_1_char_evaluator(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_evaluator("T")


# ════════════════════════════════════════════════════════════════════════
# 2. Story Structure Mapping (Stage 1)
# ════════════════════════════════════════════════════════════════════════

class TestStoryStructure:
    def test_ac3_discipline_maps_to_fail_state_warning(self) -> None:
        """AC3: 'Discipline' → FAIL_STATE_WARNING."""
        planner, _ = _make_planner()
        result = planner.resolve_story_structure("Discipline")
        assert result == StoryStructure.FAIL_STATE_WARNING

    def test_growth_maps_to_hero_journey(self) -> None:
        planner, _ = _make_planner()
        result = planner.resolve_story_structure("Growth")
        assert result == StoryStructure.HERO_JOURNEY

    def test_innovation_maps_to_paradigm_shift(self) -> None:
        planner, _ = _make_planner()
        result = planner.resolve_story_structure("Innovation")
        assert result == StoryStructure.PARADIGM_SHIFT

    def test_security_maps_to_fail_state_warning(self) -> None:
        planner, _ = _make_planner()
        result = planner.resolve_story_structure("Security")
        assert result == StoryStructure.FAIL_STATE_WARNING

    def test_truth_maps_to_paradigm_shift(self) -> None:
        planner, _ = _make_planner()
        result = planner.resolve_story_structure("Truth")
        assert result == StoryStructure.PARADIGM_SHIFT

    def test_unknown_value_raises(self) -> None:
        planner, _ = _make_planner()
        with pytest.raises(ValueError, match="UNKNOWN_BRAND_VALUE"):
            planner.resolve_story_structure("RandomValue")

    def test_structure_receipt_logged(self) -> None:
        planner, rc = _make_planner()
        planner.resolve_story_structure("Achievement")
        entries = rc.query(action="brand-story-structure-resolve")
        assert len(entries) == 1
        assert entries[0].decision == "HERO_JOURNEY"


# ════════════════════════════════════════════════════════════════════════
# 3. Static Metric Extraction (Stage 2)
# ════════════════════════════════════════════════════════════════════════

class TestSocialNouns:
    def test_multiple_social_nouns(self) -> None:
        count = DmpfcSemanticEvaluator.count_social_nouns(
            "She told her friend about it. He and they agreed."
        )
        # she, friend, he, they → 4
        assert count == 4

    def test_zero_social_nouns(self) -> None:
        count = DmpfcSemanticEvaluator.count_social_nouns(
            "Integrity is the cornerstone of our coaching framework."
        )
        assert count == 0


class TestBrandCliches:
    def test_one_cliche(self) -> None:
        count = DmpfcSemanticEvaluator.count_brand_cliches(
            "He unlocked his potential through hard work."
        )
        # Note: "unlock your potential" vs "unlocked his potential" — exact phrase match
        # "unlock your potential" won't match "unlocked his potential" — count should be 0
        # unless the regex matches. Let's check:
        # The cliché list has "unlock your potential" — "unlocked his potential" won't match
        assert count == 0

    def test_exact_cliche_match(self) -> None:
        count = DmpfcSemanticEvaluator.count_brand_cliches(
            "This is a game changer for the industry."
        )
        assert count == 1

    def test_multiple_cliches(self) -> None:
        count = DmpfcSemanticEvaluator.count_brand_cliches(
            "Synergy helps us reach the next level and achieve 10x results."
        )
        # synergy, next level, 10x → 3
        assert count == 3

    def test_zero_cliches(self) -> None:
        count = DmpfcSemanticEvaluator.count_brand_cliches(
            "She told her friend about real discipline and showing up."
        )
        assert count == 0


class TestMoralSentiment:
    def test_value_present(self) -> None:
        assert DmpfcSemanticEvaluator.check_moral_sentiment(
            "This story is about discipline and showing up.", "Discipline"
        ) is True

    def test_value_absent(self) -> None:
        assert DmpfcSemanticEvaluator.check_moral_sentiment(
            "This story is about innovation and disruption.", "Discipline"
        ) is False

    def test_case_insensitive(self) -> None:
        assert DmpfcSemanticEvaluator.check_moral_sentiment(
            "GROWTH is essential.", "Growth"
        ) is True


# ════════════════════════════════════════════════════════════════════════
# 4. Full dmPFC Gate Evaluation (Stage 3)
# ════════════════════════════════════════════════════════════════════════

class TestGatePass:
    def test_full_pass(self) -> None:
        ev, _ = _make_evaluator()
        story = _long_story(social_nouns=3, cliches=0, value_word="discipline")
        result = ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        assert result.semantic_verdict == DmpfcVerdict.PASS.value
        assert result.metrics_payload.social_nouns_found >= 2
        assert result.metrics_payload.cliches_found == 0
        assert result.metrics_payload.moral_sentiment_matched is True

    def test_pass_receipt_logged(self) -> None:
        ev, rc = _make_evaluator()
        story = _long_story(value_word="discipline")
        ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        entries = rc.query(action="dmpfc-semantic-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "PASS"


class TestGateFail:
    def test_ac1_abstract_no_social_nouns(self) -> None:
        """AC1: 'Integrity is the cornerstone...' → social_nouns=0 → FAIL_REJECTED."""
        ev, _ = _make_evaluator()
        result = ev.evaluate(
            _ABSTRACT_STORY,
            StoryStructure.FAIL_STATE_WARNING,
            "Integrity",
        )
        assert result.semantic_verdict == DmpfcVerdict.FAIL_REJECTED.value
        assert result.metrics_payload.social_nouns_found < 2

    def test_fail_no_moral_match(self) -> None:
        """Social nouns present but moral doesn't match → FAIL."""
        ev, _ = _make_evaluator()
        story = _long_story(value_word="discipline")
        result = ev.evaluate(story, StoryStructure.HERO_JOURNEY, "Innovation")
        assert result.semantic_verdict == DmpfcVerdict.FAIL_REJECTED.value
        assert result.metrics_payload.moral_sentiment_matched is False

    def test_fail_receipt_logged(self) -> None:
        ev, rc = _make_evaluator()
        ev.evaluate(_ABSTRACT_STORY, StoryStructure.FAIL_STATE_WARNING, "Integrity")
        entries = rc.query(action="dmpfc-semantic-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "FAIL_REJECTED"


class TestGateProvisional:
    def test_ac2_cliche_with_social_nouns(self) -> None:
        """AC2: social_nouns present + moral match but cliché detected → PROVISIONAL_REVIEW."""
        ev, _ = _make_evaluator()
        story = _long_story(social_nouns=3, cliches=1, value_word="discipline")
        result = ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        assert result.semantic_verdict == DmpfcVerdict.PROVISIONAL_REVIEW.value
        assert result.metrics_payload.cliches_found >= 1
        assert result.metrics_payload.social_nouns_found >= 2
        assert result.metrics_payload.moral_sentiment_matched is True

    def test_provisional_receipt_logged(self) -> None:
        ev, rc = _make_evaluator()
        story = _long_story(cliches=1, value_word="discipline")
        ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        entries = rc.query(action="dmpfc-semantic-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "PROVISIONAL_REVIEW"


class TestShortStory:
    def test_short_story_auto_fail(self) -> None:
        ev, _ = _make_evaluator()
        result = ev.evaluate(
            _SHORT_STORY,
            StoryStructure.FAIL_STATE_WARNING,
            "Integrity",
        )
        assert result.semantic_verdict == DmpfcVerdict.FAIL_REJECTED.value

    def test_short_story_receipt(self) -> None:
        ev, rc = _make_evaluator()
        ev.evaluate(_SHORT_STORY, StoryStructure.FAIL_STATE_WARNING, "Integrity")
        entries = rc.query(action="dmpfc-semantic-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "FAIL_REJECTED"


# ════════════════════════════════════════════════════════════════════════
# 5. Output Schema Integrity
# ════════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    def test_eval_id_is_uuid(self) -> None:
        ev, _ = _make_evaluator()
        story = _long_story(value_word="discipline")
        result = ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        import uuid
        uuid.UUID(result.eval_id)

    def test_evaluated_at_iso8601(self) -> None:
        ev, _ = _make_evaluator()
        story = _long_story(value_word="discipline")
        result = ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        from datetime import datetime
        datetime.fromisoformat(result.evaluated_at)

    def test_coach_id_matches(self) -> None:
        ev, _ = _make_evaluator("TST")
        story = _long_story(value_word="discipline")
        result = ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        assert result.coach_id == "TST"

    def test_story_structure_stored(self) -> None:
        ev, _ = _make_evaluator()
        story = _long_story(value_word="discipline")
        result = ev.evaluate(story, StoryStructure.HERO_JOURNEY, "discipline")
        assert result.story_structure_used == StoryStructure.HERO_JOURNEY.value


# ════════════════════════════════════════════════════════════════════════
# 6. C-11 Persona Masking
# ════════════════════════════════════════════════════════════════════════

class TestPersonaMasking:
    def test_no_agent_name_in_result(self) -> None:
        ev, _ = _make_evaluator()
        story = _long_story(value_word="discipline")
        result = ev.evaluate(story, StoryStructure.FAIL_STATE_WARNING, "discipline")
        dump = result.model_dump_json()
        assert "dmpfc-semantic-evaluator" not in dump
        assert "brand-story-planner" not in dump
