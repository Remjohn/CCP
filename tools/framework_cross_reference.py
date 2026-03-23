"""
Framework Cross-Reference Tool — FR40 §4 Stage 4

Spec: FR40_Intuition_Extensions_Tech_Spec.md §4 Stage 4
Agent: The Philosopher
Purpose: Maps coach statements against CMA principles, philosophical lexicons.

Inputs: draft_text, Knowledge Base frameworks.
Output: FrameworkCrossReferenceToolResult — matched principle, lens, reframing.

§8 AC4: Inject AncestralWisdom spark using "Stoic Lens."
        Run output against Flesch-Kincaid scorer.
        Assert Grade 8-10 (accessible, not academic).
        Failure: "reads like a 19th-century academic thesis."

ADR-01: All operations scoped to coach_id.
"""

from __future__ import annotations

import math
import re
from typing import Any, Optional

from src.ccp.models.intuition_extension_models import (
    ANCESTRAL_WISDOM_READABILITY_MAX,
    ANCESTRAL_WISDOM_READABILITY_MIN,
    FrameworkCrossReferenceToolResult,
    PhilosophicalLens,
)


# ══════════════════════════════════════════════════════════════════════════════
# CMA Principles (14 Principles of Conscious Movement Alchemy)
# ══════════════════════════════════════════════════════════════════════════════

CMA_PRINCIPLES: list[dict[str, str]] = [
    {"id": "CMA-01", "name": "Radical Transparency", "description": "Truth before comfort."},
    {"id": "CMA-02", "name": "Embodied Practice", "description": "Knowledge without practice is entertainment."},
    {"id": "CMA-03", "name": "Paradox Integration", "description": "Hold two opposing truths simultaneously."},
    {"id": "CMA-04", "name": "Shadow Acknowledgment", "description": "What you refuse to see controls you."},
    {"id": "CMA-05", "name": "Temporal Awareness", "description": "The right message at the wrong time is the wrong message."},
    {"id": "CMA-06", "name": "Structural Humility", "description": "Your framework is a lens, not the truth."},
    {"id": "CMA-07", "name": "Audience Sovereignty", "description": "The audience decides relevance. You provide the invitation."},
    {"id": "CMA-08", "name": "Productive Discomfort", "description": "Growth happens at the edge of your comfort zone."},
    {"id": "CMA-09", "name": "Contextual Integrity", "description": "Every piece of advice must acknowledge its limitations."},
    {"id": "CMA-10", "name": "Emotional Precision", "description": "Name the exact emotion. Vague feelings create vague content."},
    {"id": "CMA-11", "name": "Iterative Refinement", "description": "First drafts capture intent. Third drafts capture truth."},
    {"id": "CMA-12", "name": "Cultural Sensitivity", "description": "Universal advice is universally shallow."},
    {"id": "CMA-13", "name": "Narrative Honesty", "description": "If the story only has a hero, it's a lie."},
    {"id": "CMA-14", "name": "Legacy Thinking", "description": "Write for the person they'll be in 5 years, not who they are today."},
]


# ══════════════════════════════════════════════════════════════════════════════
# Philosophical Lens Frameworks
# ══════════════════════════════════════════════════════════════════════════════

_LENS_FRAMEWORKS: dict[PhilosophicalLens, dict[str, str]] = {
    PhilosophicalLens.STOICISM: {
        "core_question": "What is within your control, and what is not?",
        "reframing_template": (
            "The Stoics would call this the dichotomy of control. "
            "{topic} is not about changing the external — it is about "
            "changing your response to the external."
        ),
        "reference_thinker": "Marcus Aurelius wrote in Meditations",
    },
    PhilosophicalLens.BEHAVIORAL_ECONOMICS: {
        "core_question": "What hidden incentive structure is driving this behaviour?",
        "reframing_template": (
            "Kahneman would call this a System 1 trap. "
            "{topic} feels intuitive but the data says otherwise. "
            "The question is not whether people want to change, "
            "but whether the environment is designed for it."
        ),
        "reference_thinker": "Kahneman and Tversky showed in Prospect Theory",
    },
    PhilosophicalLens.EXISTENTIALISM: {
        "core_question": "What meaning are you choosing to create from this?",
        "reframing_template": (
            "Frankl survived Auschwitz and concluded that the last human "
            "freedom is choosing your attitude. {topic} is not happening "
            "to you — you are happening to it."
        ),
        "reference_thinker": "Viktor Frankl wrote in Man's Search for Meaning",
    },
    PhilosophicalLens.SYSTEMS_THINKING: {
        "core_question": "Where is the leverage point in this system?",
        "reframing_template": (
            "Meadows would say you are pushing on the wrong lever. "
            "{topic} is a symptom of the system, not a problem to solve. "
            "Change the feedback loop, not the output."
        ),
        "reference_thinker": "Donella Meadows identified in Thinking in Systems",
    },
    PhilosophicalLens.GAME_THEORY: {
        "core_question": "What game are you actually playing — and is it the right one?",
        "reframing_template": (
            "Nash showed that rational individual choices can produce "
            "collectively irrational outcomes. {topic} is not a competition — "
            "it is a coordination problem disguised as one."
        ),
        "reference_thinker": "What you are describing is what Nash called",
    },
    PhilosophicalLens.NARRATIVE_PSYCHOLOGY: {
        "core_question": "What story are you telling yourself about this?",
        "reframing_template": (
            "McAdams showed that identity is a story we tell. "
            "{topic} is not what happened — it is how you narrate "
            "what happened. Change the narrative, change the identity."
        ),
        "reference_thinker": "Dan McAdams demonstrated in The Redemptive Self",
    },
}


def cross_reference_framework(
    coach_id: str,
    draft_text: str,
    philosophical_lens: Optional[PhilosophicalLens] = None,
    target_grade_min: int = ANCESTRAL_WISDOM_READABILITY_MIN,
    target_grade_max: int = ANCESTRAL_WISDOM_READABILITY_MAX,
) -> FrameworkCrossReferenceToolResult:
    """Map coach statements against CMA principles and philosophical lexicons.

    §4 Stage 4 Tool: 'tools/framework_cross_reference.py'
    (Maps coach statements against CMA principles, philosophical lexicons.)

    §8 AC4: Output must remain Flesch-Kincaid Grade 8-10.

    Args:
        coach_id: 3-char coach identifier (ADR-01 scope).
        draft_text: The current draft text to reframe.
        philosophical_lens: Which lens to apply. If None, auto-selects.
        target_grade_min: Minimum FK grade (8).
        target_grade_max: Maximum FK grade (10).

    Returns:
        FrameworkCrossReferenceToolResult with matched principle,
        reframing directive, and readability score.
    """
    if len(coach_id) != 3:
        raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")

    # Match to CMA principle
    matched_principle = _match_cma_principle(draft_text)

    # Select or auto-detect philosophical lens
    lens = philosophical_lens or _auto_select_lens(draft_text)

    # Build reframing directive
    reframing = _build_reframing(draft_text, lens)

    # Legacy pattern
    legacy = _find_legacy_pattern(lens)

    # Compute readability of the reframing
    fk_grade = compute_flesch_kincaid_grade(reframing)

    return FrameworkCrossReferenceToolResult(
        coach_id=coach_id.upper(),
        matched_principle=matched_principle,
        philosophical_lens=lens,
        reframing_directive=reframing,
        legacy_pattern=legacy,
        flesch_kincaid_grade=fk_grade,
    )


def compute_flesch_kincaid_grade(text: str) -> float:
    """Compute the Flesch-Kincaid Grade Level of a text.

    §8 AC4: Score must be Grade 8-10. Below 8 = too simple.
    Above 10 = too academic.

    Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
    """
    if not text.strip():
        return 0.0

    # Count sentences
    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]
    num_sentences = max(len(sentences), 1)

    # Count words
    words = text.split()
    num_words = max(len(words), 1)

    # Count syllables
    num_syllables = sum(_count_syllables(w) for w in words)

    grade = (
        0.39 * (num_words / num_sentences)
        + 11.8 * (num_syllables / num_words)
        - 15.59
    )

    return round(max(0.0, grade), 1)


def _count_syllables(word: str) -> int:
    """Estimate syllable count for a word."""
    word = word.lower().strip(".,!?;:'\"()-")
    if not word:
        return 1

    # Special cases
    if len(word) <= 3:
        return 1

    # Count vowel groups
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    # Adjust for silent 'e'
    if word.endswith("e") and count > 1:
        count -= 1

    # Adjust for common endings
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1

    return max(count, 1)


def _match_cma_principle(text: str) -> Optional[str]:
    """Match draft text to the most relevant CMA principle."""
    text_lower = text.lower()
    best_match: Optional[str] = None
    best_score = 0

    keyword_map: dict[str, list[str]] = {
        "CMA-01 Radical Transparency": ["truth", "honest", "transparent", "authentic"],
        "CMA-03 Paradox Integration": ["paradox", "contradiction", "opposing", "tension"],
        "CMA-04 Shadow Acknowledgment": ["shadow", "dark", "hidden", "unconscious"],
        "CMA-06 Structural Humility": ["humble", "framework", "lens", "perspective"],
        "CMA-08 Productive Discomfort": ["comfort zone", "growth", "edge", "discomfort"],
        "CMA-10 Emotional Precision": ["emotion", "feel", "specific", "precise"],
        "CMA-13 Narrative Honesty": ["story", "narrative", "hero", "honest"],
        "CMA-14 Legacy Thinking": ["future", "legacy", "long-term", "5 years"],
    }

    for principle, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > best_score:
            best_score = score
            best_match = principle

    return best_match


def _auto_select_lens(text: str) -> PhilosophicalLens:
    """Auto-select the most appropriate philosophical lens."""
    text_lower = text.lower()

    lens_keywords: dict[PhilosophicalLens, list[str]] = {
        PhilosophicalLens.STOICISM: ["control", "accept", "endure", "discipline", "virtue"],
        PhilosophicalLens.BEHAVIORAL_ECONOMICS: ["incentive", "bias", "rational", "decision", "system"],
        PhilosophicalLens.EXISTENTIALISM: ["meaning", "purpose", "freedom", "choose", "authentic"],
        PhilosophicalLens.SYSTEMS_THINKING: ["system", "feedback", "loop", "leverage", "emergent"],
        PhilosophicalLens.GAME_THEORY: ["competition", "strategy", "player", "equilibrium", "game"],
        PhilosophicalLens.NARRATIVE_PSYCHOLOGY: ["story", "identity", "narrative", "self", "tell"],
    }

    best_lens = PhilosophicalLens.STOICISM
    best_score = 0

    for lens, keywords in lens_keywords.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > best_score:
            best_score = score
            best_lens = lens

    return best_lens


def _build_reframing(text: str, lens: PhilosophicalLens) -> str:
    """Build the reframing directive using the selected lens."""
    framework = _LENS_FRAMEWORKS.get(lens, _LENS_FRAMEWORKS[PhilosophicalLens.STOICISM])

    # Extract a rough topic from the text (first meaningful clause)
    sentences = re.split(r"[.!?]+", text)
    topic_hint = sentences[0].strip()[:60] if sentences else "this topic"

    template = framework["reframing_template"]
    reframing = template.format(topic=topic_hint)

    return reframing


def _find_legacy_pattern(lens: PhilosophicalLens) -> Optional[str]:
    """Find a timeless wisdom link for this lens."""
    framework = _LENS_FRAMEWORKS.get(lens)
    if framework:
        return framework.get("reference_thinker")
    return None
