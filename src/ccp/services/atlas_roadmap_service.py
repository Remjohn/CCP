"""
FR32 — Dynamic Capacity Tracks & 4-Week Roadmap (DEP-ENG-027)
5 Capacity Tracks + 4+1+2 matrix + 10% progressive overload + 14-day lock.

AC1: Track designation from psychological profile.
AC2: 4+1+2 matrix (16 Active / 4 Reflection / 8 Rest per 28 days).
AC3: +10% intensity per week (REST always 0.00).
AC4: 14-day anti-escalation lock for Recovery track.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    ANTI_ESCALATION_LOCK_DAYS,
    AntiPatternLock,
    AtlasRoadmap,
    CapacityTrack,
    FOUNDATION_FEAR_RANGE,
    GROWTH_AGENCY_MIN,
    GROWTH_FEAR_RANGE,
    MILESTONE_INDICES,
    MOMENTUM_AGENCY_MIN,
    MOMENTUM_FEAR_RANGE,
    PEAK_AGENCY_MIN,
    PEAK_FEAR_MAX,
    RECOVERY_COPING_THRESHOLD,
    RECOVERY_FEAR_THRESHOLD,
    ROADMAP_DAYS,
    RoadmapDay,
    RoadmapDayType,
    WEEKLY_OVERLOAD_MULTIPLIER,
)


# ── 4+1+2 weekly template ─────────────────────────────
# FR32 §4.2: [Active, Active, Rest, Active, Active, Reflection, Rest]
WEEKLY_TEMPLATE: list[RoadmapDayType] = [
    RoadmapDayType.ACTIVE,
    RoadmapDayType.ACTIVE,
    RoadmapDayType.REST,
    RoadmapDayType.ACTIVE,
    RoadmapDayType.ACTIVE,
    RoadmapDayType.REFLECTION,
    RoadmapDayType.REST,
]


class AtlasRoadmapService:
    """
    FR32: Capacity track classification + 28-day roadmap generation.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)

    # ── Track Classification ───────────────────────────

    def classify_track(
        self,
        *,
        fear_score: float,
        agency_score: float,
        coping_exhaustion: float = 0.0,
    ) -> CapacityTrack:
        """
        FR32 AC1: Classify capacity track from psychological profile.
        Recovery: fear >= 0.8 OR coping_exhaustion >= 0.75
        Foundation: 0.6 <= fear <= 0.79
        Growth: 0.4 <= fear <= 0.59 AND agency >= 0.5
        Momentum: 0.2 <= fear <= 0.39 AND agency >= 0.65
        Peak: fear < 0.2 AND agency >= 0.8
        """
        if fear_score >= RECOVERY_FEAR_THRESHOLD or coping_exhaustion >= RECOVERY_COPING_THRESHOLD:
            return CapacityTrack.RECOVERY
        if FOUNDATION_FEAR_RANGE[0] <= fear_score <= FOUNDATION_FEAR_RANGE[1]:
            return CapacityTrack.FOUNDATION
        if (GROWTH_FEAR_RANGE[0] <= fear_score <= GROWTH_FEAR_RANGE[1]
                and agency_score >= GROWTH_AGENCY_MIN):
            return CapacityTrack.GROWTH
        if (MOMENTUM_FEAR_RANGE[0] <= fear_score <= MOMENTUM_FEAR_RANGE[1]
                and agency_score >= MOMENTUM_AGENCY_MIN):
            return CapacityTrack.MOMENTUM
        if fear_score < PEAK_FEAR_MAX and agency_score >= PEAK_AGENCY_MIN:
            return CapacityTrack.PEAK
        # Default to Foundation if no specific match
        return CapacityTrack.FOUNDATION

    # ── Roadmap Generation ─────────────────────────────

    def generate_roadmap(
        self,
        *,
        user_id: str,
        track: CapacityTrack,
        base_intensity: float = 0.5,
    ) -> AtlasRoadmap:
        """
        FR32 AC2/AC3: Generate 28-day roadmap with 4+1+2 template
        and +10% progressive overload per week.
        """
        days: list[RoadmapDay] = []

        for week_num in range(1, 5):
            # FR32 AC3: +10% per week (week 1 = base × 1.0, week 2 = base × 1.10, etc.)
            week_multiplier = WEEKLY_OVERLOAD_MULTIPLIER ** (week_num - 1)
            week_intensity = round(base_intensity * week_multiplier, 4)

            for day_in_week, day_type in enumerate(WEEKLY_TEMPLATE):
                day_number = (week_num - 1) * 7 + day_in_week + 1

                # FR32 §4.3: REST days always 0.00
                if day_type == RoadmapDayType.REST:
                    intensity = 0.0
                elif day_type == RoadmapDayType.REFLECTION:
                    intensity = round(week_intensity * 0.5, 4)  # Reflection = half load
                else:
                    intensity = week_intensity

                days.append(RoadmapDay(
                    day=day_number,
                    week_number=week_num,
                    type=day_type,
                    assigned_intensity_load=intensity,
                ))

        roadmap = AtlasRoadmap(
            user_id=user_id,
            coach_id=self._coach,
            capacity_track=track,
            roadmap_architecture=days,
        )

        self._receipt_chain.log(
            agent_id="AtlasRoadmapService",
            action="ROADMAP_GENERATED",
            asset_id=f"ROADMAP-{user_id}",
            person_id=user_id,
            decision=track.value,
            decision_rationale=f"base_intensity={base_intensity}, days={ROADMAP_DAYS}",
        )

        return roadmap

    # ── Anti-Escalation Lock ───────────────────────────

    def check_anti_escalation_lock(
        self,
        *,
        current_track: CapacityTrack,
        days_in_current_track: int,
    ) -> bool:
        """
        FR32 AC4: Recovery track cannot escalate before Day 15.
        Returns True if escalation is BLOCKED.
        """
        if current_track == CapacityTrack.RECOVERY:
            return days_in_current_track < (ANTI_ESCALATION_LOCK_DAYS + 1)
        return False

    def can_escalate(
        self,
        *,
        current_track: CapacityTrack,
        target_track: CapacityTrack,
        days_in_current_track: int,
    ) -> bool:
        """Check if track escalation is allowed."""
        if self.check_anti_escalation_lock(
            current_track=current_track,
            days_in_current_track=days_in_current_track,
        ):
            return False

        # Validate escalation order
        track_order = [
            CapacityTrack.RECOVERY,
            CapacityTrack.FOUNDATION,
            CapacityTrack.GROWTH,
            CapacityTrack.MOMENTUM,
            CapacityTrack.PEAK,
        ]
        current_idx = track_order.index(current_track)
        target_idx = track_order.index(target_track)

        # Can only escalate one level at a time
        return target_idx == current_idx + 1
