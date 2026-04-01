"""FR-CA11-09 — Accountability Check-in System with AFFiNE Visualization.

Extends the CBCS accountability loop with visual feedback:
daily data collection → weekly Excalidraw charts by Benjamin →
milestone badge system → AFFiNE dashboard sync.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    AccountabilityResult,
    AccountabilityVisualPayload,
    DailyDataPoint,
    MilestoneBadge,
    MoodTrajectory,
    WeeklyChart,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_BENJAMIN = "Benjamin"
AGENT_NOEMIE = "Noémie"

MILESTONE_THRESHOLDS: dict[int, str] = {
    7: MilestoneBadge.day_7.value,
    14: MilestoneBadge.day_14.value,
    21: MilestoneBadge.day_21.value,
    30: MilestoneBadge.day_30.value,
    60: MilestoneBadge.day_60.value,
    90: MilestoneBadge.day_90.value,
}

STREAK_BADGE_EMOJIS: dict[str, str] = {
    "7_day": "🥉",
    "14_day": "🥈",
    "21_day": "🥇",
    "30_day": "🏆",
    "60_day": "💎",
    "90_day": "👑",
}

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

ACCOUNTABILITY_DATA_SQL = """
CREATE TABLE IF NOT EXISTS accountability_data (
    id              TEXT PRIMARY KEY,
    client_id       TEXT NOT NULL,
    date            DATE NOT NULL,
    energy_rating   INTEGER NOT NULL CHECK (energy_rating BETWEEN 1 AND 10),
    habits_completed JSONB NOT NULL DEFAULT '[]',
    habits_missed   JSONB NOT NULL DEFAULT '[]',
    mood_state      TEXT NOT NULL DEFAULT 'Processing',
    streak_count    INTEGER NOT NULL DEFAULT 0,
    liwc_markers    JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(client_id, date)
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class AFFiNESyncProtocol(Protocol):
    async def push_content(self, coach_id: str, section: str,
                           title: str, body: str, *,
                           metadata: dict[str, Any] | None = None) -> str: ...


class TelegramProtocol(Protocol):
    async def send_message(self, chat_id: str, text: str) -> None: ...


class AccountabilityStoreProtocol(Protocol):
    async def store_data_point(self, data: DailyDataPoint) -> None: ...
    async def get_week_data(self, client_id: str, week_number: int) -> list[DailyDataPoint]: ...
    async def get_streak(self, client_id: str) -> int: ...


# ---------------------------------------------------------------------------
# Stage 1 — Daily Data Collection
# ---------------------------------------------------------------------------


class DailyDataCollector:
    """Collects and stores daily check-in data."""

    def __init__(self, store: AccountabilityStoreProtocol | None = None) -> None:
        self._store = store

    async def record_checkin(
        self,
        client_id: str,
        energy_rating: int,
        habits_completed: list[str],
        habits_missed: list[str],
        mood_state: str = "Processing",
        streak_count: int = 0,
        date: str | None = None,
    ) -> DailyDataPoint:
        dp = DailyDataPoint(
            client_id=client_id,
            date=date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            energy_rating=energy_rating,
            habits_completed=habits_completed,
            habits_missed=habits_missed,
            mood_state=mood_state,
            streak_count=streak_count,
        )
        if self._store:
            await self._store.store_data_point(dp)
        return dp


# ---------------------------------------------------------------------------
# Stage 2 — Weekly Chart Generation (Benjamin)
# ---------------------------------------------------------------------------


class ProgressChartGenerator:
    """``Benjamin`` — generates weekly Excalidraw progress charts."""

    def generate_chart(
        self,
        week_data: list[DailyDataPoint],
        week_number: int,
        coach_acronym: str = "CCH",
    ) -> WeeklyChart:
        energy_trend = [dp.energy_rating for dp in week_data]
        total_habits = sum(
            len(dp.habits_completed) + len(dp.habits_missed) for dp in week_data
        )
        completed_habits = sum(len(dp.habits_completed) for dp in week_data)
        rate = completed_habits / total_habits if total_habits > 0 else 0.0
        streak = week_data[-1].streak_count if week_data else 0
        badges = self._compute_badges(streak)
        trajectory = self._compute_mood_trajectory(week_data)
        chart_url = (
            f"s3://{coach_acronym}/excalidraw/"
            f"progress_{week_data[0].client_id}_week{week_number}.json"
            if week_data else None
        )

        return WeeklyChart(
            chart_url=chart_url,
            week_number=week_number,
            energy_trend=energy_trend,
            habits_completed_rate=round(rate, 2),
            current_streak=streak,
            milestone_badges=badges,
            mood_trajectory=trajectory,
        )

    def generate_excalidraw_json(
        self,
        chart: WeeklyChart,
    ) -> dict[str, Any]:
        """Produce Excalidraw-compatible JSON structure."""
        elements: list[dict[str, Any]] = []

        # Line graph nodes for energy
        for i, val in enumerate(chart.energy_trend):
            elements.append({
                "type": "ellipse",
                "id": f"energy-{i}",
                "x": 100 + i * 80,
                "y": 300 - val * 25,
                "width": 12,
                "height": 12,
                "label": str(val),
            })

        # Streak counter
        elements.append({
            "type": "text",
            "id": "streak",
            "x": 50,
            "y": 20,
            "text": f"Streak: {chart.current_streak} days",
        })

        # Habit completion rate
        elements.append({
            "type": "text",
            "id": "habit-rate",
            "x": 50,
            "y": 50,
            "text": f"Habits: {chart.habits_completed_rate:.0%}",
        })

        # Milestone badges
        for i, badge in enumerate(chart.milestone_badges):
            emoji = STREAK_BADGE_EMOJIS.get(badge, "⭐")
            elements.append({
                "type": "text",
                "id": f"badge-{i}",
                "x": 350 + i * 40,
                "y": 20,
                "text": emoji,
            })

        return {"type": "excalidraw", "version": 2, "elements": elements}

    @staticmethod
    def _compute_badges(streak: int) -> list[str]:
        return [
            badge for threshold, badge in sorted(MILESTONE_THRESHOLDS.items())
            if streak >= threshold
        ]

    @staticmethod
    def _compute_mood_trajectory(week_data: list[DailyDataPoint]) -> MoodTrajectory:
        if len(week_data) < 2:
            return MoodTrajectory.stable
        first_half = week_data[: len(week_data) // 2]
        second_half = week_data[len(week_data) // 2 :]
        avg_first = sum(dp.energy_rating for dp in first_half) / len(first_half)
        avg_second = sum(dp.energy_rating for dp in second_half) / len(second_half)
        if avg_second - avg_first > 0.5:
            return MoodTrajectory.ascending
        if avg_first - avg_second > 0.5:
            return MoodTrajectory.descending
        return MoodTrajectory.stable


# ---------------------------------------------------------------------------
# Stage 3 — Milestone Badge System (Noémie)
# ---------------------------------------------------------------------------


class MilestoneBadgeSystem:
    """``Noémie`` — tracks streaks and fires milestone celebrations."""

    def check_milestone(self, streak_count: int) -> str | None:
        """Return the milestone badge name if streak hits a threshold."""
        return MILESTONE_THRESHOLDS.get(streak_count)

    def compute_streak(
        self,
        previous_streak: int,
        completed_today: bool,
    ) -> tuple[int, bool]:
        """Return (new_streak, was_reset)."""
        if completed_today:
            return previous_streak + 1, False
        return 0, previous_streak > 0

    def format_celebration(self, badge: str) -> str:
        emoji = STREAK_BADGE_EMOJIS.get(badge, "⭐")
        day_count = badge.replace("_day", "").replace("_", "")
        return f"{emoji} Amazing! You've hit a {day_count}-day streak! Keep going!"

    def format_re_engagement(self) -> str:
        return (
            "No worries — every day is a fresh start. "
            "Your streak may have paused, but your progress hasn't. "
            "Ready to pick back up?"
        )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


class AccountabilityPipeline:
    """End-to-end accountability pipeline: check-in → store → chart → badge."""

    def __init__(
        self,
        store: AccountabilityStoreProtocol | None = None,
        affine_sync: AFFiNESyncProtocol | None = None,
        telegram: TelegramProtocol | None = None,
    ) -> None:
        self._collector = DailyDataCollector(store)
        self._chart_gen = ProgressChartGenerator()
        self._badge_sys = MilestoneBadgeSystem()
        self._affine = affine_sync
        self._telegram = telegram
        self._store = store

    async def process_checkin(
        self,
        client_id: str,
        coach_id: str,
        energy_rating: int,
        habits_completed: list[str],
        habits_missed: list[str],
        mood_state: str = "Processing",
        previous_streak: int = 0,
        chat_id: str | None = None,
        date: str | None = None,
    ) -> AccountabilityResult:
        # Determine if any habit was completed
        completed_today = len(habits_completed) > 0
        new_streak, was_reset = self._badge_sys.compute_streak(
            previous_streak, completed_today
        )

        # Record data
        dp = await self._collector.record_checkin(
            client_id=client_id,
            energy_rating=energy_rating,
            habits_completed=habits_completed,
            habits_missed=habits_missed,
            mood_state=mood_state,
            streak_count=new_streak,
            date=date,
        )

        # AFFiNE dashboard sync
        if self._affine:
            try:
                await self._affine.push_content(
                    coach_id,
                    "dashboard",
                    f"Check-in — {dp.date}",
                    self._format_daily_summary(dp),
                    metadata={"client_id": client_id, "date": dp.date},
                )
            except Exception:
                pass

        # Milestone check
        milestone = self._badge_sys.check_milestone(new_streak)
        if milestone and self._telegram and chat_id:
            try:
                msg = self._badge_sys.format_celebration(milestone)
                await self._telegram.send_message(chat_id, msg)
            except Exception:
                pass

        # Streak reset notification
        if was_reset and self._telegram and chat_id:
            try:
                msg = self._badge_sys.format_re_engagement()
                await self._telegram.send_message(chat_id, msg)
            except Exception:
                pass

        return AccountabilityResult(
            success=True,
            data_point_stored=True,
            milestone_triggered=milestone,
            streak_reset=was_reset,
        )

    async def generate_weekly_chart(
        self,
        week_data: list[DailyDataPoint],
        week_number: int,
        coach_id: str,
        coach_acronym: str = "CCH",
    ) -> AccountabilityResult:
        if not week_data:
            return AccountabilityResult(success=False, error="No data for chart")

        chart = self._chart_gen.generate_chart(week_data, week_number, coach_acronym)
        excalidraw = self._chart_gen.generate_excalidraw_json(chart)

        if self._affine:
            try:
                await self._affine.push_content(
                    coach_id,
                    "progress_board",
                    f"Week {week_number} Progress",
                    str(excalidraw),
                    metadata={
                        "client_id": week_data[0].client_id,
                        "week_number": week_number,
                        "chart_url": chart.chart_url,
                    },
                )
            except Exception:
                pass

        return AccountabilityResult(
            success=True,
            chart_generated=True,
        )

    @staticmethod
    def _format_daily_summary(dp: DailyDataPoint) -> str:
        lines = [
            f"# Daily Check-in — {dp.date}\n",
            f"**Energy:** {dp.energy_rating}/10",
            f"**Mood:** {dp.mood_state}",
            f"**Streak:** {dp.streak_count} days",
            f"**Completed:** {', '.join(dp.habits_completed) or 'None'}",
            f"**Missed:** {', '.join(dp.habits_missed) or 'None'}",
        ]
        return "\n".join(lines)
