"""
CCP FR28 — Dynamic Journaling Engine (DEP-ENG-024)

Spec: FR28_Dynamic_Journaling_Tech_Spec.md
Produces: DEP-ENG-024 Dynamic Journaling Directive

§4 Stage 1: Async Scheduled Trigger (cron check)
§4 Stage 2: Strategic Trajectory Mapping (Atlas anti-escalation logic)
§4 Stage 3: Generative Assembly (Artisan constraint builder)

§3 Tech Decision 1: 4+1+2 weekly structure — Active(4) + Reflection(1) + Rest(2)
§3 Tech Decision 2: Anti-Escalation — cannot go above Foundation before day 14
§8 AC1: Day 6 + "Motivated" → stays at Foundation (anti-escalation enforced)
§8 AC2: Rest Day → blocks generation, shifts to next active day
§8 AC3: Momentum + Complacent → <75 word friction challenge
§8 AC4: ADR-01 — Cron mounts coach-specific PantryConfig only
"""

from __future__ import annotations

from datetime import datetime, date, timezone
from typing import Optional

from src.ccp.models.onboarding_prerequisite_models import (
    ANTI_ESCALATION_MIN_DAYS,
    JOURNALING_MAX_WORDS,
    ArtisanDirective,
    CapacityTrack,
    DynamicJournalingDirective,
    MoodState,
    PsychologicalContext,
    RoadmapContext,
    StructuralDay,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ══════════════════════════════════════════════════════════════════════════════
# Mapping Tables (FR28 §4 Stage 2)
# ══════════════════════════════════════════════════════════════════════════════

# Track × Mood → (prompt_category, emotional_target, required_constraint)
_DIRECTIVE_MAP: dict[
    tuple[CapacityTrack, MoodState], tuple[str, str, str]
] = {
    (CapacityTrack.RECOVERY, MoodState.DISTRESSED): (
        "grounding_sensory",
        "safety_establishment",
        "Must not ask the user for a new commitment today. "
        "Must only ask them to pause and label the anxiety.",
    ),
    (CapacityTrack.RECOVERY, MoodState.ANXIOUS_AVOIDANT): (
        "grounding_sensory",
        "safety_establishment",
        "Must not ask the user for a new commitment today. "
        "Invite them to name one safe, simple thing in their environment.",
    ),
    (CapacityTrack.RECOVERY, MoodState.APATHETIC): (
        "curiosity_activation",
        "gentle_re_engagement",
        "Avoid performance language. Ask about something they have noticed "
        "or found interesting recently.",
    ),
    (CapacityTrack.FOUNDATION, MoodState.STABLE): (
        "identity_anchoring",
        "value_alignment",
        "Ground the prompt in the coach's foundational principle. "
        "Keep challenge level at 0.",
    ),
    (CapacityTrack.FOUNDATION, MoodState.MOTIVATED): (
        "identity_anchoring",
        "value_alignment",
        "High motivation acknowledged but do not escalate intensity. "
        "Foundation track requires consolidation, not acceleration.",
    ),
    (CapacityTrack.GROWTH, MoodState.STABLE): (
        "friction_challenge",
        "growth_edge_activation",
        "Include one direct challenge that pushes slightly past the comfortable.",
    ),
    (CapacityTrack.GROWTH, MoodState.MOTIVATED): (
        "friction_challenge",
        "growth_edge_activation",
        "Increase challenge 10% above last session. User is ready to be pushed.",
    ),
    (CapacityTrack.MOMENTUM, MoodState.MOTIVATED): (
        "friction_challenge",
        "performance_reinforcement",
        "Direct tone. Intensity 10% higher than last week. "
        "Name a specific behavior to test today.",
    ),
    (CapacityTrack.MOMENTUM, MoodState.COMPLACENT): (
        "friction_challenge",
        "pattern_interruption",
        "Name the complacency directly without shaming. "
        "Propose a specific contrarian action. Friction required.",
    ),
    (CapacityTrack.PEAK, MoodState.MOTIVATED): (
        "mastery_refinement",
        "precision_excellence",
        "At Peak, focus on nuance and mastery details the user may be "
        "skating over in pursuit of speed.",
    ),
}

# Default fallback by track
_DEFAULT_DIRECTIVE: dict[CapacityTrack, tuple[str, str, str]] = {
    CapacityTrack.RECOVERY: (
        "grounding_sensory",
        "safety_establishment",
        "Default Recovery baseline — no new commitments.",
    ),
    CapacityTrack.FOUNDATION: (
        "identity_anchoring",
        "value_alignment",
        "Default Foundation baseline — consolidate, no acceleration.",
    ),
    CapacityTrack.GROWTH: (
        "friction_challenge",
        "growth_edge_activation",
        "Default Growth baseline — light challenge.",
    ),
    CapacityTrack.MOMENTUM: (
        "friction_challenge",
        "performance_reinforcement",
        "Default Momentum baseline — maintain cadence.",
    ),
    CapacityTrack.PEAK: (
        "mastery_refinement",
        "precision_excellence",
        "Default Peak baseline — refinement focus.",
    ),
}

# 7-day rolling Rest Day indices (1-based): default positions 3 and 7
DEFAULT_REST_DAYS: frozenset[int] = frozenset({3, 7})


# ══════════════════════════════════════════════════════════════════════════════
# PantryConfig (ADR-01 per-coach settings)
# ══════════════════════════════════════════════════════════════════════════════

class PantryConfig:
    """FR28 §4 Stage 1 / AC4: Per-coach configuration.

    ADR-01: Each cron invocation must mount THIS coach's config — never shared.
    """

    def __init__(
        self,
        coach_id: str,
        journaling_frequency_per_week: int = 2,
        rest_day_indices: frozenset[int] = DEFAULT_REST_DAYS,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError("coach_id must be 3 characters (ADR-01).")
        self.coach_id = coach_id
        # Capped to max meaningful 5 journaling days (7 - 2 rest days)
        self.journaling_frequency = min(journaling_frequency_per_week, 5)
        self.rest_day_indices = rest_day_indices  # 1-7 where 1=Mon

    def is_rest_day(self, day_of_week: int) -> bool:
        """AC2: Return True if this weekday (1=Mon…7=Sun) is a designated Rest Day."""
        return day_of_week in self.rest_day_indices


# ══════════════════════════════════════════════════════════════════════════════
# Stage 1: Cron Trigger Check
# ══════════════════════════════════════════════════════════════════════════════

class JournalingCronCheck:
    """FR28 §4 Stage 1: Determine whether to invoke Atlas for this user today.

    Checks:
        - Is today a Rest Day? → block
        - Has the user hit their weekly quota? → skip
        - Is Dormancy Timer active? → route to dormancy recovery instead
    """

    def __init__(self, pantry: PantryConfig) -> None:
        self.pantry = pantry

    def should_trigger(
        self,
        current_day_of_week: int,
        prompts_sent_this_week: int,
        dormancy_active: bool = False,
    ) -> tuple[bool, str]:
        """Return (should_trigger, reason).

        AC2: Rest Day → blocked ('REST_DAY_BLOCKED').
        """
        if dormancy_active:
            return False, "DORMANCY_ACTIVE"
        if self.pantry.is_rest_day(current_day_of_week):
            return False, "REST_DAY_BLOCKED"
        if prompts_sent_this_week >= self.pantry.journaling_frequency:
            return False, "WEEKLY_QUOTA_MET"
        return True, "TRIGGER_APPROVED"


# ══════════════════════════════════════════════════════════════════════════════
# Stage 2: Strategic Trajectory Mapping (Atlas)
# ══════════════════════════════════════════════════════════════════════════════

class AtlasTrajectoryMapper:
    """FR28 §4 Stage 2: Map Capacity Track × Mood → ArtisanDirective.

    AC1 (Anti-Escalation): If current_day < 14 AND track ∈ {Growth, Momentum, Peak}
    → demote to Foundation and set escalation_blocked=True.
    """

    def map(
        self,
        current_day: int,
        capacity_track: CapacityTrack,
        last_mood: MoodState = MoodState.STABLE,
        context_extraction_available: bool = True,
    ) -> tuple[CapacityTrack, ArtisanDirective, bool]:
        """Return (effective_track, artisan_directive, escalation_blocked).

        If Aria context_extraction is unavailable, fall back to static baseline
        for the active Capacity Track (§6 fallback).
        """
        high_intensity = {CapacityTrack.GROWTH, CapacityTrack.MOMENTUM, CapacityTrack.PEAK}
        escalation_blocked = False

        # Anti-escalation gate
        if current_day < ANTI_ESCALATION_MIN_DAYS and capacity_track in high_intensity:
            capacity_track = CapacityTrack.FOUNDATION
            escalation_blocked = True
            last_mood = MoodState.STABLE  # reset modifier

        # Lookup directive
        if context_extraction_available:
            cat, target, constraint = _DIRECTIVE_MAP.get(
                (capacity_track, last_mood),
                _DEFAULT_DIRECTIVE[capacity_track],
            )
        else:
            # §6 fallback: static baseline without behavioral modifier
            cat, target, constraint = _DEFAULT_DIRECTIVE[capacity_track]

        directive = ArtisanDirective(
            prompt_category=cat,
            emotional_target=target,
            required_constraint=constraint,
            max_words=JOURNALING_MAX_WORDS,
        )
        return capacity_track, directive, escalation_blocked


# ══════════════════════════════════════════════════════════════════════════════
# Stage 3: Artisan Prompt Word-Count Validator
# ══════════════════════════════════════════════════════════════════════════════

class ArtisanOutputValidator:
    """FR28 §4 Stage 3 / AC3: Enforce ≤ 75-word output length."""

    MAX_WORDS = JOURNALING_MAX_WORDS

    def validate(self, generated_text: str) -> tuple[bool, int]:
        """Return (valid, word_count). valid=True if word_count ≤ 75."""
        words = generated_text.split()
        count = len(words)
        return count <= self.MAX_WORDS, count

    def truncate(self, text: str) -> str:
        """Truncate to 75 words as hard enforcement."""
        words = text.split()
        return " ".join(words[: self.MAX_WORDS])


# ══════════════════════════════════════════════════════════════════════════════
# Full Journaling Engine
# ══════════════════════════════════════════════════════════════════════════════

class DynamicJournalingEngine:
    """FR28 full pipeline orchestrator.

    Usage:
        engine = DynamicJournalingEngine(pantry=PantryConfig("EMI", 3))
        directive = engine.generate(
            user_id="USR-001",
            current_day=10,
            capacity_track=CapacityTrack.FOUNDATION,
            last_mood=MoodState.MOTIVATED,
            current_day_of_week=5,
            prompts_sent_this_week=1,
        )
    """

    def __init__(
        self,
        pantry: PantryConfig,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        self.pantry = pantry
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=pantry.coach_id
        )
        self.cron_check = JournalingCronCheck(pantry)
        self.trajectory_mapper = AtlasTrajectoryMapper()
        self.output_validator = ArtisanOutputValidator()

    def generate(
        self,
        user_id: str,
        current_day: int,
        capacity_track: CapacityTrack,
        last_mood: MoodState = MoodState.STABLE,
        current_day_of_week: int = 1,
        prompts_sent_this_week: int = 0,
        dormancy_active: bool = False,
        context_extraction_available: bool = True,
        scheduled_date: Optional[str] = None,
    ) -> Optional[DynamicJournalingDirective]:
        """Generate a DEP-ENG-024 Journaling Directive or None if blocked.

        Returns None when: Rest Day blocked, quota met, or dormancy active.
        """
        # Stage 1: Cron check
        should_trigger, reason = self.cron_check.should_trigger(
            current_day_of_week=current_day_of_week,
            prompts_sent_this_week=prompts_sent_this_week,
            dormancy_active=dormancy_active,
        )
        if not should_trigger:
            self.receipt_chain.log(
                agent_id="Master-Cron-Job",
                action="journaling_trigger_check",
                input_summary=f"user={user_id} day_of_week={current_day_of_week}",
                output_summary=f"Blocked: {reason}",
                metadata={"stage_name": "ASYNCHRONOUS-TRIGGER", "reason": reason},
            )
            return None

        # Stage 2: Trajectory mapping
        structural_day = self._determine_structural_day(current_day_of_week)
        effective_track, directive, escalation_blocked = self.trajectory_mapper.map(
            current_day=current_day,
            capacity_track=capacity_track,
            last_mood=last_mood,
            context_extraction_available=context_extraction_available,
        )

        self.receipt_chain.log(
            agent_id="Atlas",
            action="trajectory_mapping",
            input_summary=f"user={user_id} day={current_day} track={capacity_track.value} mood={last_mood.value}",
            output_summary=(
                f"effective_track={effective_track.value} "
                f"category={directive.prompt_category} "
                f"escalation_blocked={escalation_blocked}"
            ),
            metadata={"stage_name": "STRATEGIC-TRAJECTORY-MAPPING"},
        )

        today_str = scheduled_date or date.today().isoformat()

        journaling_directive = DynamicJournalingDirective(
            user_id=user_id,
            coach_id=self.pantry.coach_id,
            scheduled_date=today_str,
            roadmap_context=RoadmapContext(
                current_day=current_day,
                capacity_track=effective_track,
                structural_day=structural_day,
            ),
            psychological_context=PsychologicalContext(
                last_interaction_mood=last_mood,
                intensity_override=(
                    "decrease_10_percent"
                    if last_mood == MoodState.DISTRESSED
                    else None
                ),
            ),
            artisan_directive=directive,
            escalation_blocked=escalation_blocked,
        )

        # Stage 3 receipt
        self.receipt_chain.log(
            agent_id="Artisan",
            action="journaling_directive_assembly",
            input_summary=f"user={user_id} category={directive.prompt_category}",
            output_summary=f"max_words={directive.max_words} rest_day_blocked=False",
            metadata={"stage_name": "GENERATIVE-ASSEMBLY-DELIVERY"},
        )

        return journaling_directive

    @staticmethod
    def _determine_structural_day(day_of_week: int) -> StructuralDay:
        """FR28 §3 Tech Decision 1: 4 Active, 1 Reflection, 2 Rest in a 7-day cycle.

        Default mapping: Mon-Thu=Active, Fri=Reflection, Sat-Sun=Rest.
        """
        if day_of_week in {6, 7}:  # Sat, Sun
            return StructuralDay.REST_DAY
        if day_of_week == 5:  # Fri
            return StructuralDay.REFLECTION_POINT
        return StructuralDay.ACTIVE_RITUAL
