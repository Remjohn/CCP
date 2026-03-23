"""
CCP FR6 — Context Premise Fallback (Unit 10)
AC13 backward compatibility when Context Premise Map (DEP-ENG-006)
does not exist for this coach.

Spec reference: FR6 Tech Spec §Backward Compatibility — Legacy Fallback
  Condition: Context Premise Map (DEP-ENG-006) does not exist for this coach.

Fallback behavior (from spec):
  1. Content generation uses coach_soul.json values and topic-based prompts
     instead of audience-matched structural seeds
  2. Trigger Matching Layer 4-axis engine cannot execute — content generated
     from coach triggers without audience structural matching
  3. Archetype selection uses coach emotional state only, not audience mode routing
  4. DARN-CAT questions are topic-generic, not L3-vocabulary-anchored

Limitation: Content without Context Premise Map delivers professional empathy
(comprehension without coupling). Expected neural coupling quality significantly
lower. Audience feels informed but not recognized.

Exit from fallback: When Stage A + Stage B complete →
tribe_profile_distilled.json exists + Neo4j populated → weekly pipeline
automatically reads DEP-ENG-006 for Trigger Matching.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

from src.ccp.models.coach_soul import CoachSoul
from src.ccp.models.tribe_profile_models import ContextPremiseFallbackResult

logger = logging.getLogger(__name__)


class ContextPremiseFallback:
    """AC13: Generates fallback content seeds from coach_soul.json
    when Context Premise Map is absent.

    All downstream phases complete without error. Trigger Matching
    Layer gracefully degrades — it receives topic-based prompts
    instead of audience-matched structural seeds.
    """

    # ──────────────────────────────────────────────────────────
    # DETECTION
    # ──────────────────────────────────────────────────────────

    @staticmethod
    def context_premise_exists(coach_folder: Path) -> bool:
        """Check whether DEP-ENG-006 (context_premise_map.json) exists
        for the given coach folder.

        Returns True if the file exists AND is valid JSON with
        at least the required top-level fields.
        """
        cpm_path = coach_folder / "context_premise_map.json"
        if not cpm_path.exists():
            return False

        try:
            data = json.loads(cpm_path.read_text(encoding="utf-8"))
            # Minimal structural check — must have dimensions + authentication
            if not isinstance(data, dict):
                return False
            if "dimensions" not in data and "authentication" not in data:
                return False
            return True
        except (json.JSONDecodeError, OSError):
            return False

    @staticmethod
    def distilled_profile_exists(coach_folder: Path) -> bool:
        """Check whether tribe_profile_distilled.json exists.
        When this file exists, the fallback is no longer needed."""
        distilled_path = coach_folder / "tribe_profile_distilled.json"
        return distilled_path.exists()

    # ──────────────────────────────────────────────────────────
    # FALLBACK SEED GENERATION
    # ──────────────────────────────────────────────────────────

    @staticmethod
    def generate_fallback_seeds(
        coach_soul: CoachSoul,
    ) -> dict[str, Any]:
        """Generate topic-based content prompts from coach_soul.json.

        These seeds allow content generation to proceed without
        audience-matched structural seeds. Quality will be lower
        (professional empathy vs. neural coupling) but all downstream
        phases complete without error.

        Returns a dict of topic-based prompts organized by content area.
        """
        seeds: dict[str, Any] = {}

        # Topic seeds from coaching philosophy
        if coach_soul.coaching_philosophy:
            seeds["philosophy_topics"] = [
                coach_soul.coaching_philosophy,
            ]

        # Topic seeds from core message
        if coach_soul.core_message:
            seeds["core_message_prompts"] = [
                coach_soul.core_message,
            ]

        # Topic seeds from ideal client pain points
        if coach_soul.ideal_client.pain_points:
            seeds["pain_point_topics"] = list(
                coach_soul.ideal_client.pain_points
            )

        # Topic seeds from ideal client aspirations
        if coach_soul.ideal_client.aspirations:
            seeds["aspiration_topics"] = list(
                coach_soul.ideal_client.aspirations
            )

        # Trait-based format guidance (exercise/showcase)
        format_weights = coach_soul.get_format_assignment_weights()
        if format_weights.get("exercise") or format_weights.get("showcase"):
            seeds["trait_format_guidance"] = format_weights

        # Tribe archetype (generic, not mode-routed)
        if coach_soul.tribe_archetype:
            seeds["tribe_archetype"] = coach_soul.tribe_archetype

        # Signature frameworks as generic content scaffolds
        if coach_soul.signature_frameworks:
            seeds["framework_topics"] = list(
                coach_soul.signature_frameworks
            )

        # Voice DNA hooks — vocabulary fingerprint for basic tone matching
        if coach_soul.voice_dna.vocabulary_fingerprint:
            seeds["vocabulary_hooks"] = list(
                coach_soul.voice_dna.vocabulary_fingerprint
            )

        # Content tone parameters (warmth, directness, humor, formality)
        seeds["content_tone"] = coach_soul.content_tone.model_dump()

        return seeds

    # ──────────────────────────────────────────────────────────
    # FULL FALLBACK RESOLUTION
    # ──────────────────────────────────────────────────────────

    @classmethod
    def resolve(
        cls,
        coach_soul: CoachSoul,
        coach_folder: Path,
        coach_soul_path: Optional[str] = None,
    ) -> Optional[ContextPremiseFallbackResult]:
        """Resolve fallback status for a coach.

        Returns:
            ContextPremiseFallbackResult if fallback is active (no CPM).
            None if Context Premise Map exists (normal pipeline path).
        """
        if cls.context_premise_exists(coach_folder):
            return None

        # AC13: Coach without Context Premise Map → content generated
        # using topic-based prompts from coach_soul.json. No errors.
        logger.warning(
            "AC13 FALLBACK: Context Premise Map not found for coach %s. "
            "Using topic-based prompts from coach_soul.json. "
            "Content quality limited to professional empathy.",
            coach_soul.coach_id,
        )

        fallback_seeds = cls.generate_fallback_seeds(coach_soul)

        return ContextPremiseFallbackResult(
            used_fallback=True,
            reason=(
                f"Context Premise Map (DEP-ENG-006) not found for "
                f"coach {coach_soul.coach_id} in {coach_folder}"
            ),
            coach_soul_path=coach_soul_path or str(coach_folder / "coach_soul.json"),
            fallback_content_seed=fallback_seeds,
        )

    # ──────────────────────────────────────────────────────────
    # EXIT CONDITION CHECK
    # ──────────────────────────────────────────────────────────

    @classmethod
    def is_fallback_still_active(cls, coach_folder: Path) -> bool:
        """Check whether fallback is still active.

        Exit condition: When Stage A + Stage B complete →
        tribe_profile_distilled.json exists + context_premise_map.json exists.

        Returns True if fallback is still needed (files missing).
        Returns False if pipeline has completed (files exist).
        """
        cpm_exists = cls.context_premise_exists(coach_folder)
        distilled_exists = cls.distilled_profile_exists(coach_folder)

        if cpm_exists and distilled_exists:
            logger.info(
                "Fallback exit condition met: both "
                "context_premise_map.json and tribe_profile_distilled.json "
                "exist in %s",
                coach_folder,
            )
            return False

        return True

    # ──────────────────────────────────────────────────────────
    # GRACEFUL DEGRADATION INTERFACE
    # ──────────────────────────────────────────────────────────

    @staticmethod
    def degrade_trigger_matching_config() -> dict[str, Any]:
        """Return degraded configuration for Trigger Matching Layer.

        Spec §Backward Compatibility:
          - 4-axis engine cannot execute
          - Archetype selection uses coach emotional state only
          - DARN-CAT questions are topic-generic
        """
        return {
            "trigger_matching_mode": "degraded",
            "four_axis_engine_enabled": False,
            "archetype_routing": "coach_emotional_state_only",
            "darn_cat_mode": "topic_generic",
            "audience_mode_routing": False,
            "l3_vocabulary_anchoring": False,
            "neural_coupling_expected": False,
            "quality_level": "professional_empathy",
        }
