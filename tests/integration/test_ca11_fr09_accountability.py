"""FR-CA11-09 — Accountability Visualization — Integration Tests.

Covers all 5 Acceptance Criteria:
  AC1: Daily data capture (energy, habits, mood)
  AC2: Weekly chart generation (line graph, habit grid, streak, mood trend)
  AC3: Milestone badge on 7-day streak
  AC4: Streak reset + re-engagement prompt
  AC5: AFFiNE dashboard sync
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    AccountabilityResult,
    AccountabilityVisualPayload,
    DailyDataPoint,
    MilestoneBadge,
    MoodTrajectory,
    WeeklyChart,
)
from src.ccp.services.accountability_visualizer import (
    ACCOUNTABILITY_DATA_SQL,
    AGENT_BENJAMIN,
    AGENT_NOEMIE,
    MILESTONE_THRESHOLDS,
    STREAK_BADGE_EMOJIS,
    AccountabilityPipeline,
    DailyDataCollector,
    MilestoneBadgeSystem,
    ProgressChartGenerator,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CLIENT_ID = "uuid-client-042"
COACH_ID = "uuid-coach-test-01"
COACH_ACRONYM = "JPR"
CHAT_ID = "chat-111"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _make_dp(
    day: int = 1,
    energy: int = 7,
    completed: list[str] | None = None,
    missed: list[str] | None = None,
    streak: int = 1,
    mood: str = "Discovery",
) -> DailyDataPoint:
    return DailyDataPoint(
        client_id=CLIENT_ID,
        date=f"2026-03-{day:02d}",
        energy_rating=energy,
        habits_completed=completed or ["meditation", "journaling"],
        habits_missed=missed or [],
        mood_state=mood,
        streak_count=streak,
    )


def _week_data(
    energies: list[int] | None = None,
    streak_end: int = 7,
) -> list[DailyDataPoint]:
    energies = energies or [7, 6, 8, 7, 9, 8, 7]
    return [
        _make_dp(day=i + 1, energy=e, streak=i + 1)
        for i, e in enumerate(energies)
    ]


# ---- Mocks ----

class MockStore:
    def __init__(self):
        self.points: list[DailyDataPoint] = []
        self._streak = 0
    async def store_data_point(self, data: DailyDataPoint) -> None:
        self.points.append(data)
    async def get_week_data(self, client_id: str, week_number: int) -> list[DailyDataPoint]:
        return self.points[:7]
    async def get_streak(self, client_id: str) -> int:
        return self._streak


class MockAFFiNeSync:
    def __init__(self):
        self.pushes: list[dict] = []
    async def push_content(self, coach_id, section, title, body, *, metadata=None):
        page_id = f"page-{uuid.uuid4().hex[:8]}"
        self.pushes.append({
            "coach_id": coach_id, "section": section,
            "title": title, "body": body, "metadata": metadata,
        })
        return page_id


class MockTelegram:
    def __init__(self):
        self.messages: list[tuple[str, str]] = []
    async def send_message(self, chat_id: str, text: str) -> None:
        self.messages.append((chat_id, text))


def _pipeline(*, with_store=True, with_sync=True, with_tg=True):
    store = MockStore() if with_store else None
    sync = MockAFFiNeSync() if with_sync else None
    tg = MockTelegram() if with_tg else None
    pipe = AccountabilityPipeline(store=store, affine_sync=sync, telegram=tg)
    return pipe, store, sync, tg


# ===================================================================
# 1. Model validation (6 tests)
# ===================================================================

class TestModels:
    def test_daily_data_point(self):
        dp = _make_dp()
        assert dp.energy_rating == 7
        assert dp.client_id == CLIENT_ID

    def test_energy_bounds(self):
        with pytest.raises(Exception):
            DailyDataPoint(client_id="c", date="2026-01-01", energy_rating=0)
        with pytest.raises(Exception):
            DailyDataPoint(client_id="c", date="2026-01-01", energy_rating=11)

    def test_weekly_chart_defaults(self):
        wc = WeeklyChart(week_number=1)
        assert wc.habits_completed_rate == 0.0
        assert wc.mood_trajectory == MoodTrajectory.stable

    def test_milestone_badges_enum(self):
        assert MilestoneBadge.day_7.value == "7_day"
        assert MilestoneBadge.day_30.value == "30_day"

    def test_mood_trajectory_enum(self):
        assert MoodTrajectory.ascending.value == "ascending"

    def test_accountability_result(self):
        r = AccountabilityResult(success=True, milestone_triggered="7_day")
        assert r.milestone_triggered == "7_day"


# ===================================================================
# 2. Daily data collector — AC1 (3 tests)
# ===================================================================

class TestDailyDataCollector:
    def test_records_checkin_ac1(self):
        """AC1 — check-in creates data point with correct fields."""
        store = MockStore()
        collector = DailyDataCollector(store)
        dp = _run(collector.record_checkin(
            CLIENT_ID, energy_rating=8,
            habits_completed=["meditation"], habits_missed=["exercise"],
            mood_state="Discovery", streak_count=5,
        ))
        assert dp.energy_rating == 8
        assert dp.habits_completed == ["meditation"]
        assert dp.habits_missed == ["exercise"]
        assert dp.mood_state == "Discovery"
        assert len(store.points) == 1

    def test_no_store_still_returns(self):
        collector = DailyDataCollector(store=None)
        dp = _run(collector.record_checkin(CLIENT_ID, 7, ["med"], []))
        assert dp.energy_rating == 7

    def test_streak_count_stored(self):
        store = MockStore()
        collector = DailyDataCollector(store)
        dp = _run(collector.record_checkin(CLIENT_ID, 6, ["x"], [], streak_count=14))
        assert dp.streak_count == 14


# ===================================================================
# 3. Chart generation — AC2 (6 tests)
# ===================================================================

class TestChartGeneration:
    def test_weekly_chart_generated_ac2(self):
        """AC2 — chart contains energy trend, habit rate, streak, mood."""
        gen = ProgressChartGenerator()
        data = _week_data()
        chart = gen.generate_chart(data, week_number=12, coach_acronym=COACH_ACRONYM)
        assert chart.week_number == 12
        assert len(chart.energy_trend) == 7
        assert chart.habits_completed_rate > 0
        assert chart.current_streak > 0

    def test_chart_url_format(self):
        gen = ProgressChartGenerator()
        data = _week_data()
        chart = gen.generate_chart(data, 1, COACH_ACRONYM)
        assert COACH_ACRONYM in chart.chart_url
        assert "excalidraw" in chart.chart_url

    def test_excalidraw_json_structure(self):
        gen = ProgressChartGenerator()
        data = _week_data()
        chart = gen.generate_chart(data, 1)
        ej = gen.generate_excalidraw_json(chart)
        assert ej["type"] == "excalidraw"
        assert len(ej["elements"]) > 0

    def test_excalidraw_has_streak_and_rate(self):
        gen = ProgressChartGenerator()
        data = _week_data()
        chart = gen.generate_chart(data, 1)
        ej = gen.generate_excalidraw_json(chart)
        texts = [e["text"] for e in ej["elements"] if e["type"] == "text"]
        assert any("Streak" in t for t in texts)
        assert any("Habits" in t for t in texts)

    def test_mood_ascending(self):
        gen = ProgressChartGenerator()
        data = _week_data(energies=[3, 3, 3, 8, 9, 9, 9])
        chart = gen.generate_chart(data, 1)
        assert chart.mood_trajectory == MoodTrajectory.ascending

    def test_mood_descending(self):
        gen = ProgressChartGenerator()
        data = _week_data(energies=[9, 9, 9, 3, 3, 3, 3])
        chart = gen.generate_chart(data, 1)
        assert chart.mood_trajectory == MoodTrajectory.descending


# ===================================================================
# 4. Milestone badges — AC3 (5 tests)
# ===================================================================

class TestMilestoneBadges:
    def test_7_day_milestone_ac3(self):
        """AC3 — 7-day streak triggers milestone."""
        sys = MilestoneBadgeSystem()
        assert sys.check_milestone(7) == "7_day"

    def test_14_day_milestone(self):
        sys = MilestoneBadgeSystem()
        assert sys.check_milestone(14) == "14_day"

    def test_non_milestone_day(self):
        sys = MilestoneBadgeSystem()
        assert sys.check_milestone(5) is None

    def test_celebration_message(self):
        sys = MilestoneBadgeSystem()
        msg = sys.format_celebration("7_day")
        assert "7" in msg
        assert "🥉" in msg

    def test_badges_computed_for_chart(self):
        gen = ProgressChartGenerator()
        data = _week_data()
        # Streak of 7 → should include 7_day badge
        data[-1] = _make_dp(day=7, streak=7)
        chart = gen.generate_chart(data, 1)
        assert "7_day" in chart.milestone_badges


# ===================================================================
# 5. Streak reset — AC4 (4 tests)
# ===================================================================

class TestStreakReset:
    def test_streak_continues(self):
        sys = MilestoneBadgeSystem()
        new_streak, reset = sys.compute_streak(5, completed_today=True)
        assert new_streak == 6
        assert not reset

    def test_streak_resets_ac4(self):
        """AC4 — missed day resets streak."""
        sys = MilestoneBadgeSystem()
        new_streak, reset = sys.compute_streak(10, completed_today=False)
        assert new_streak == 0
        assert reset

    def test_re_engagement_message(self):
        sys = MilestoneBadgeSystem()
        msg = sys.format_re_engagement()
        assert "fresh start" in msg
        assert "progress" in msg.lower()

    def test_reset_from_zero_not_flagged(self):
        sys = MilestoneBadgeSystem()
        new_streak, reset = sys.compute_streak(0, completed_today=False)
        assert new_streak == 0
        assert not reset  # can't reset from 0


# ===================================================================
# 6. Full pipeline — AC5 + integration (6 tests)
# ===================================================================

class TestFullPipeline:
    def test_checkin_success(self):
        pipe, store, sync, tg = _pipeline()
        result = _run(pipe.process_checkin(
            CLIENT_ID, COACH_ID, energy_rating=8,
            habits_completed=["meditation"], habits_missed=["exercise"],
            previous_streak=5, chat_id=CHAT_ID,
        ))
        assert result.success
        assert result.data_point_stored

    def test_affine_dashboard_sync_ac5(self):
        """AC5 — daily data appears in AFFiNE dashboard."""
        pipe, _, sync, _ = _pipeline()
        _run(pipe.process_checkin(
            CLIENT_ID, COACH_ID, energy_rating=7,
            habits_completed=["x"], habits_missed=[],
            previous_streak=3,
        ))
        assert len(sync.pushes) == 1
        assert sync.pushes[0]["section"] == "dashboard"

    def test_milestone_fires_telegram(self):
        pipe, _, _, tg = _pipeline()
        result = _run(pipe.process_checkin(
            CLIENT_ID, COACH_ID, energy_rating=8,
            habits_completed=["x"], habits_missed=[],
            previous_streak=6, chat_id=CHAT_ID,  # will become 7
        ))
        assert result.milestone_triggered == "7_day"
        assert len(tg.messages) == 1
        assert "7" in tg.messages[0][1]

    def test_streak_reset_fires_telegram(self):
        pipe, _, _, tg = _pipeline()
        result = _run(pipe.process_checkin(
            CLIENT_ID, COACH_ID, energy_rating=5,
            habits_completed=[], habits_missed=["all"],
            previous_streak=10, chat_id=CHAT_ID,
        ))
        assert result.streak_reset
        assert len(tg.messages) == 1
        assert "fresh start" in tg.messages[0][1]

    def test_weekly_chart_generation(self):
        pipe, _, sync, _ = _pipeline()
        data = _week_data()
        result = _run(pipe.generate_weekly_chart(data, 12, COACH_ID, COACH_ACRONYM))
        assert result.success
        assert result.chart_generated
        assert len(sync.pushes) == 1
        assert sync.pushes[0]["section"] == "progress_board"

    def test_empty_week_data(self):
        pipe, _, _, _ = _pipeline()
        result = _run(pipe.generate_weekly_chart([], 1, COACH_ID))
        assert not result.success


# ===================================================================
# 7. Constants & SQL (3 tests)
# ===================================================================

class TestConstants:
    def test_agent_names(self):
        assert AGENT_BENJAMIN == "Benjamin"
        assert AGENT_NOEMIE == "Noémie"

    def test_milestone_thresholds(self):
        assert 7 in MILESTONE_THRESHOLDS
        assert 30 in MILESTONE_THRESHOLDS
        assert 90 in MILESTONE_THRESHOLDS

    def test_sql_schema(self):
        assert "accountability_data" in ACCOUNTABILITY_DATA_SQL
        assert "energy_rating" in ACCOUNTABILITY_DATA_SQL
        assert "streak_count" in ACCOUNTABILITY_DATA_SQL
