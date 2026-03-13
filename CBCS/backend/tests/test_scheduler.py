"""
Tests for the CCP Task Scheduler (Epic 10).

Tests the scheduler's core functionality without requiring
a running Supabase instance or Telegram API access.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, time

from backend.core.scheduler import (
    CoachScheduler,
    _keep_warm_job,
    _coach_heartbeat_job,
    DAY_MAP,
    HEARTBEAT_MESSAGES,
)


# ──────────────────────────────────────────────
# Unit Tests
# ──────────────────────────────────────────────


class TestDayMapping:
    """Test day name to cron day_of_week mapping."""

    def test_all_days_mapped(self):
        expected = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        assert set(DAY_MAP.keys()) == expected

    def test_monday_maps_to_mon(self):
        assert DAY_MAP["monday"] == "mon"

    def test_saturday_maps_to_sat(self):
        assert DAY_MAP["saturday"] == "sat"


class TestHeartbeatMessages:
    """Test heartbeat message templates exist for all job types."""

    def test_interview_message_exists(self):
        assert "interview" in HEARTBEAT_MESSAGES
        assert "Interview Day" in HEARTBEAT_MESSAGES["interview"]

    def test_ideas_message_exists(self):
        assert "ideas" in HEARTBEAT_MESSAGES
        assert "Content Ideas" in HEARTBEAT_MESSAGES["ideas"]

    def test_recording_message_exists(self):
        assert "recording" in HEARTBEAT_MESSAGES
        assert "Recording Prep" in HEARTBEAT_MESSAGES["recording"]


class TestCoachSchedulerInit:
    """Test scheduler initialization."""

    def test_scheduler_creates_without_starting(self):
        sched = CoachScheduler()
        assert sched._scheduler is None
        assert sched._coach_configs == {}

    def test_get_all_jobs_empty_when_not_started(self):
        sched = CoachScheduler()
        assert sched.get_all_jobs_summary() == []


class TestCoachSchedulerJobs:
    """Test job registration logic."""

    def test_register_coach_job(self):
        sched = CoachScheduler()
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        sched._scheduler = AsyncIOScheduler()
        sched._scheduler.start()

        sched._register_coach_job(
            coach_id="test-123",
            chat_id=999,
            job_type="interview",
            day="monday",
            time_str="09:00",
            timezone="Europe/Paris",
        )

        jobs = sched.get_all_jobs_summary()
        assert len(jobs) == 1
        assert jobs[0]["id"] == "interview_test-123"

        sched._scheduler.shutdown(wait=False)

    def test_register_replaces_existing_job(self):
        sched = CoachScheduler()
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        sched._scheduler = AsyncIOScheduler()
        sched._scheduler.start()

        # Register same job twice
        for _ in range(2):
            sched._register_coach_job(
                coach_id="test-123",
                chat_id=999,
                job_type="ideas",
                day="thursday",
                time_str="10:30",
                timezone="Europe/Paris",
            )

        jobs = sched.get_all_jobs_summary()
        assert len(jobs) == 1  # Should not duplicate

        sched._scheduler.shutdown(wait=False)

    def test_cleanup_stale_jobs(self):
        sched = CoachScheduler()
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        sched._scheduler = AsyncIOScheduler()
        sched._scheduler.start()

        # Register jobs for two coaches
        for coach_id in ["coach-a", "coach-b"]:
            sched._register_coach_job(
                coach_id=coach_id,
                chat_id=999,
                job_type="interview",
                day="monday",
                time_str="09:00",
                timezone="UTC",
            )

        assert len(sched.get_all_jobs_summary()) == 2

        # Only coach-a is active now
        sched._cleanup_stale_jobs({"coach-a"})

        jobs = sched.get_all_jobs_summary()
        assert len(jobs) == 1
        assert jobs[0]["id"] == "interview_coach-a"

        sched._scheduler.shutdown(wait=False)


# ──────────────────────────────────────────────
# Async Tests (heartbeat job)
# ──────────────────────────────────────────────


@pytest.mark.asyncio
@patch("backend.core.scheduler.send_telegram_message", new_callable=AsyncMock)
async def test_coach_heartbeat_sends_message(mock_send):
    """Test that heartbeat job sends the correct message type."""
    mock_send.return_value = True

    await _coach_heartbeat_job(
        coach_id="test-coach-123",
        chat_id=42,
        job_type="interview",
    )

    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert call_args[0][0] == 42  # chat_id
    assert "Interview Day" in call_args[0][1]  # message content


@pytest.mark.asyncio
@patch("backend.core.scheduler.send_telegram_message", new_callable=AsyncMock)
async def test_heartbeat_unknown_type_logs_error(mock_send):
    """Test that unknown job types are handled gracefully."""
    await _coach_heartbeat_job(
        coach_id="test-coach-123",
        chat_id=42,
        job_type="nonexistent",
    )

    mock_send.assert_not_called()


@pytest.mark.asyncio
@patch("backend.core.scheduler.send_telegram_message", new_callable=AsyncMock)
@patch("backend.core.scheduler._trigger_content_ideation", new_callable=AsyncMock)
async def test_ideas_heartbeat_triggers_ideation(mock_ideation, mock_send):
    """Test that ideas heartbeat also triggers content ideation."""
    mock_send.return_value = True

    await _coach_heartbeat_job(
        coach_id="test-coach-123",
        chat_id=42,
        job_type="ideas",
    )

    mock_send.assert_called_once()
    mock_ideation.assert_called_once_with("test-coach-123", 42)


# ──────────────────────────────────────────────
# Keep-warm tests (preserved from original)
# ──────────────────────────────────────────────


@pytest.mark.asyncio
@patch("backend.core.scheduler.datetime")
@patch("backend.core.voice.voice_engine.generate_audio", new_callable=AsyncMock)
async def test_keep_warm_during_peak(mock_audio, mock_dt):
    """Test keep-warm pings during peak hours."""
    mock_dt.now.return_value = datetime(2026, 2, 18, 8, 30)  # 08:30 — peak
    mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

    await _keep_warm_job()

    mock_audio.assert_called_once_with("warmup", style="Standard")


@pytest.mark.asyncio
@patch("backend.core.scheduler.datetime")
@patch("backend.core.voice.voice_engine.generate_audio", new_callable=AsyncMock)
async def test_keep_warm_outside_peak(mock_audio, mock_dt):
    """Test keep-warm does NOT ping outside peak hours."""
    mock_dt.now.return_value = datetime(2026, 2, 18, 14, 0)  # 14:00 — not peak
    mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

    await _keep_warm_job()

    mock_audio.assert_not_called()
