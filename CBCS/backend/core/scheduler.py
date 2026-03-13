"""
CCP Task Scheduler — Epic 10 (Stories 10.1, 10.2, 10.3)
=========================================================
Replaces the original keep-warm-only scheduler with APScheduler.

Architecture:
    FastAPI lifespan → scheduler.start() → APScheduler AsyncIOScheduler
                    ↓
    ┌─────────────────────────────────────────────────────┐
    │  Built-in Jobs:                                     │
    │    • keep_warm     — ping voice engine during peak  │
    │    • sync_coaches  — reload coach configs from DB   │
    │                                                     │
    │  Per-Coach Cron Jobs (dynamic):                     │
    │    • interview_prompt_{coach_id}                     │
    │    • ideas_delivery_{coach_id}                       │
    │    • recording_prep_{coach_id}                       │
    └─────────────────────────────────────────────────────┘

Coach schedules are read from the `coach_configs` table and converted
to APScheduler CronTriggers. When configs change, the sync job
removes stale triggers and adds new ones.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from backend.config import get_settings
from backend.core.telegram import send_telegram_message
from backend.core.output_watcher import output_watcher

logger = logging.getLogger(__name__)
settings = get_settings()


# ──────────────────────────────────────────────
# Day name → cron day_of_week mapping
# ──────────────────────────────────────────────
DAY_MAP = {
    "monday": "mon",
    "tuesday": "tue",
    "wednesday": "wed",
    "thursday": "thu",
    "friday": "fri",
    "saturday": "sat",
    "sunday": "sun",
}


# ──────────────────────────────────────────────
# Heartbeat Messages (Story 10.3)
# ──────────────────────────────────────────────

HEARTBEAT_MESSAGES = {
    "interview": (
        "🎤 *It's Interview Day!*\n\n"
        "Time to record your weekly voice note.\n\n"
        "Share what's on your mind this week — a client win, "
        "a framework you've been thinking about, or a topic "
        "your audience has been asking about.\n\n"
        "Just hit record and send it here when you're ready. "
        "I'll extract the themes and start generating content ideas."
    ),
    "ideas": (
        "📊 *Your Weekly Content Ideas Are Ready!*\n\n"
        "Based on this week's themes, I've prepared 3 content ideas "
        "for you.\n\n"
        "_Generating now... stand by._"
    ),
    "recording": (
        "🎬 *Recording Prep Day!*\n\n"
        "Your recording package is ready for the selected idea.\n\n"
        "I'm assembling:\n"
        "• 📝 Script with talking points\n"
        "• 🎨 Visual prompt suggestions\n"
        "• ⏱️ Estimated duration\n\n"
        "_Preparing now..._"
    ),
}


# ──────────────────────────────────────────────
# Scheduler Class
# ──────────────────────────────────────────────

class CoachScheduler:
    """
    APScheduler-based scheduler for the Conscious Coach Platform.

    Replaces the original keep-warm-only asyncio loop with proper
    cron-based job scheduling. Supports per-coach timezone-aware
    triggers loaded from Supabase coach_configs table.
    """

    def __init__(self):
        self._scheduler: Optional[AsyncIOScheduler] = None
        self._coach_configs: Dict[str, Dict[str, Any]] = {}  # coach_id → config

    def start(self):
        """Initialize and start the APScheduler."""
        self._scheduler = AsyncIOScheduler(
            job_defaults={
                "coalesce": True,       # If missed, run once instead of N times
                "max_instances": 1,     # Never overlap same job
                "misfire_grace_time": 3600,  # 1 hour grace for missed jobs
            }
        )

        # ── Built-in Jobs ──

        # Keep-warm: ping voice engine every 4 min during peak hours
        self._scheduler.add_job(
            _keep_warm_job,
            trigger=IntervalTrigger(minutes=4),
            id="keep_warm",
            name="Keep-Warm Voice Engine Ping",
            replace_existing=True,
        )

        # Sync coach configs from DB every 15 minutes
        self._scheduler.add_job(
            self._sync_coach_schedules,
            trigger=IntervalTrigger(minutes=15),
            id="sync_coaches",
            name="Sync Coach Schedules",
            replace_existing=True,
        )

        self._scheduler.start()
        logger.info("[Scheduler] APScheduler started with built-in jobs")

        # Initial coach config sync (fire-and-forget)
        asyncio.ensure_future(self._sync_coach_schedules())

    async def stop(self):
        """Shutdown the scheduler gracefully."""
        if self._scheduler and self._scheduler.running:
            self._scheduler.shutdown(wait=False)
            logger.info("[Scheduler] APScheduler stopped")

        # Stop all output watchers
        output_watcher.stop_all()

    # ──────────────────────────────────────────────
    # Coach Schedule Sync (Story 10.2)
    # ──────────────────────────────────────────────

    async def _sync_coach_schedules(self):
        """
        Read coach_configs from Supabase and create/update cron jobs.

        Called:
            - Once on startup
            - Every 15 minutes to pick up config changes
        """
        try:
            configs = await _fetch_coach_configs()
            logger.info(f"[Scheduler] Synced {len(configs)} coach configs")

            # Track which coaches we've seen to remove stale jobs
            active_coach_ids = set()

            for config in configs:
                coach_id = config["coach_id"]
                chat_id = config.get("telegram_chat_id")
                active_coach_ids.add(coach_id)

                if not chat_id:
                    logger.warning(f"[Scheduler] Coach {coach_id} has no chat_id, skipping")
                    continue

                # Check if config changed (skip re-registration if identical)
                old_config = self._coach_configs.get(coach_id)
                if old_config == config:
                    continue

                self._coach_configs[coach_id] = config
                tz = config.get("timezone", "Europe/Paris")

                # Register/update the 3 weekly jobs for this coach
                self._register_coach_job(
                    coach_id=coach_id,
                    chat_id=chat_id,
                    job_type="interview",
                    day=config.get("interview_day", "monday"),
                    time_str=config.get("interview_time", "09:00"),
                    timezone=tz,
                )
                self._register_coach_job(
                    coach_id=coach_id,
                    chat_id=chat_id,
                    job_type="ideas",
                    day=config.get("ideas_day", "thursday"),
                    time_str=config.get("ideas_time", "09:00"),
                    timezone=tz,
                )
                self._register_coach_job(
                    coach_id=coach_id,
                    chat_id=chat_id,
                    job_type="recording",
                    day=config.get("recording_day", "saturday"),
                    time_str=config.get("recording_time", "09:00"),
                    timezone=tz,
                )

                # Start output file watcher for this coach (Story 20.4)
                project_root = config.get("project_root")
                if project_root:
                    output_watcher.start_watching(coach_id, chat_id, project_root)

            # Remove jobs for coaches no longer in the database
            self._cleanup_stale_jobs(active_coach_ids)

        except Exception as e:
            logger.error(f"[Scheduler] Coach sync failed: {e}", exc_info=True)

    def _register_coach_job(
        self,
        coach_id: str,
        chat_id: int,
        job_type: str,
        day: str,
        time_str: str,
        timezone: str,
    ):
        """
        Register a single cron job for a coach.

        Example: interview_prompt_abc123 runs every Monday 09:00 Europe/Paris
        """
        job_id = f"{job_type}_{coach_id}"
        cron_day = DAY_MAP.get(day.lower(), "mon")

        # Parse time "09:00" → hour=9, minute=0
        parts = time_str.split(":")
        hour = int(parts[0]) if len(parts) >= 1 else 9
        minute = int(parts[1]) if len(parts) >= 2 else 0

        trigger = CronTrigger(
            day_of_week=cron_day,
            hour=hour,
            minute=minute,
            timezone=timezone,
        )

        self._scheduler.add_job(
            _coach_heartbeat_job,
            trigger=trigger,
            id=job_id,
            name=f"{job_type.title()} for coach {coach_id[:8]}",
            replace_existing=True,
            kwargs={
                "coach_id": coach_id,
                "chat_id": chat_id,
                "job_type": job_type,
            },
        )

        logger.info(
            f"[Scheduler] Registered {job_type} job for coach {coach_id[:8]}... "
            f"→ {cron_day} {hour:02d}:{minute:02d} ({timezone})"
        )

    def _cleanup_stale_jobs(self, active_coach_ids: set):
        """Remove scheduler jobs for coaches no longer in the database."""
        if not self._scheduler:
            return

        for job in self._scheduler.get_jobs():
            # Skip built-in jobs
            if job.id in ("keep_warm", "sync_coaches"):
                continue

            # Extract coach_id from job_id pattern: "{type}_{coach_id}"
            parts = job.id.split("_", 1)
            if len(parts) == 2:
                coach_id = parts[1]
                if coach_id not in active_coach_ids:
                    logger.info(f"[Scheduler] Removing stale job: {job.id}")
                    job.remove()

        # Also clean up cached configs and output watchers
        stale_ids = set(self._coach_configs.keys()) - active_coach_ids
        for sid in stale_ids:
            del self._coach_configs[sid]
            output_watcher.stop_watching(sid)

    # ──────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────

    def get_coach_schedule(self, coach_id: str) -> List[Dict[str, Any]]:
        """Return the scheduled jobs for a specific coach."""
        jobs = []
        if not self._scheduler:
            return jobs

        for job in self._scheduler.get_jobs():
            if coach_id in job.id:
                jobs.append({
                    "id": job.id,
                    "name": job.name,
                    "next_run": str(job.next_run_time) if job.next_run_time else None,
                })
        return jobs

    def get_all_jobs_summary(self) -> List[Dict[str, Any]]:
        """Return summary of all scheduled jobs (for debugging)."""
        if not self._scheduler:
            return []

        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run": str(job.next_run_time) if job.next_run_time else None,
            }
            for job in self._scheduler.get_jobs()
        ]


# ──────────────────────────────────────────────
# Job Functions (run by APScheduler)
# ──────────────────────────────────────────────

async def _keep_warm_job():
    """
    Ping the voice engine during peak hours to prevent GPU cold starts.

    Preserved from the original scheduler.py — only runs during
    the 07:00–10:00 window to keep IndexTTS-2 warm on Runpod.
    """
    from datetime import time

    now = datetime.now()
    start_time = time(7, 0)
    end_time = time(10, 0)

    if start_time <= now.time() <= end_time:
        try:
            from backend.core.voice import voice_engine
            logger.info("[Scheduler] Keep-Warm: pinging voice engine")
            await voice_engine.generate_audio("warmup", style="Standard")
        except Exception as e:
            logger.error(f"[Scheduler] Keep-warm ping failed: {e}")


async def _coach_heartbeat_job(
    coach_id: str,
    chat_id: int,
    job_type: str,
):
    """
    Send a scheduled heartbeat message to a coach via Telegram.

    For 'ideas' type, this also triggers the content ideation flow
    in the coach graph.
    """
    logger.info(f"[Scheduler] Firing {job_type} heartbeat for coach {coach_id[:8]}...")

    message = HEARTBEAT_MESSAGES.get(job_type)
    if not message:
        logger.error(f"[Scheduler] Unknown job_type: {job_type}")
        return

    # Send the heartbeat message
    success = await send_telegram_message(chat_id, message)

    if success:
        logger.info(f"[Scheduler] Sent {job_type} heartbeat to chat_id={chat_id}")
    else:
        logger.error(f"[Scheduler] Failed to send {job_type} heartbeat to chat_id={chat_id}")

    # For 'ideas' type, trigger the content ideation pipeline
    if job_type == "ideas" and success:
        await _trigger_content_ideation(coach_id, chat_id)

    # For 'recording' type, trigger recording prep
    if job_type == "recording" and success:
        await _trigger_recording_prep(coach_id, chat_id)


async def _trigger_content_ideation(coach_id: str, chat_id: int):
    """
    Trigger the content ideation flow after sending ideas heartbeat.

    Pipeline (Story 11.3 + 10.3):
        1. Run CCF weekly CLI command to generate fresh themes
        2. Read dynamic_content_themes.json
        3. Invoke coach graph's content_ideation node with themes
        4. Send 3 generated ideas to coach via Telegram
    """
    try:
        # Step 1: Run CCF weekly pipeline (Story 11.3)
        from backend.core.cli_runner import cli_runner, build_ccf_weekly_pipeline

        coach_config = scheduler._coach_configs.get(coach_id, {})
        project_root = coach_config.get("project_root")

        if project_root:
            import os
            project_id = os.path.basename(project_root)
            workspace_root = os.path.dirname(os.path.dirname(project_root))

            logger.info(f"[Scheduler] Running CCF weekly pipeline for {project_id}")
            await send_telegram_message(
                chat_id,
                "🔄 Running weekly content research pipeline... (1-2 min)"
            )

            ccf_configs = build_ccf_weekly_pipeline(
                project_id=project_id,
                workspace_root=workspace_root,
            )

            ccf_results = await cli_runner.run_pipeline(
                configs=ccf_configs,
                stop_on_failure=False,
            )

            if ccf_results and ccf_results[0].success:
                logger.info("[Scheduler] CCF weekly pipeline completed successfully")
            else:
                logger.warning("[Scheduler] CCF weekly pipeline had issues, proceeding with ideation anyway")

        # Step 2: Trigger coach graph content ideation
        from backend.core.coach_graph import get_coach_graph
        from langchain_core.messages import HumanMessage

        graph = get_coach_graph()
        result = await graph.ainvoke({
            "user_id": chat_id,
            "role": "coach",
            "buffer": [{"message": {"text": "generate ideas"}}],
            "messages": [HumanMessage(content="[Scheduled] Generate weekly content ideas")],
            "is_processing": False,
        })

        # Send the generated ideas via Telegram
        if result.get("messages"):
            last_msg = result["messages"][-1]
            if hasattr(last_msg, "content") and last_msg.content:
                await send_telegram_message(chat_id, last_msg.content)

    except Exception as e:
        logger.error(f"[Scheduler] Content ideation trigger failed: {e}", exc_info=True)


async def _trigger_recording_prep(coach_id: str, chat_id: int):
    """
    Trigger recording preparation after sending recording heartbeat.

    This is a placeholder — will be wired to generate the actual
    recording package (script + visual prompts) once Epic 11.4 is complete.
    """
    logger.info(f"[Scheduler] Recording prep trigger for coach {coach_id[:8]} — pending Epic 11.4")


# ──────────────────────────────────────────────
# Supabase Integration
# ──────────────────────────────────────────────

async def _fetch_coach_configs() -> List[Dict[str, Any]]:
    """
    Fetch all coach configurations from Supabase.

    Joins coach_configs with profiles to get the telegram_chat_id
    for each coach, which is needed for sending heartbeat messages.
    """
    try:
        import httpx

        url = f"{settings.SUPABASE_URL}/rest/v1/coach_configs"
        select = (
            "coach_id,coach_name,interview_day,interview_time,"
            "ideas_day,ideas_time,recording_day,recording_time,"
            "timezone,content_format,ideas_per_week,preferred_archetypes,"
            "project_root,current_week,"
            "profiles!coach_configs_coach_id_fkey(telegram_chat_id)"
        )

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                url,
                headers={
                    "apikey": settings.SUPABASE_KEY,
                    "Authorization": f"Bearer {settings.SUPABASE_KEY}",
                },
                params={"select": select},
            )

            if resp.status_code != 200:
                logger.error(f"[Scheduler] Supabase fetch failed: {resp.status_code} {resp.text[:200]}")
                return []

            rows = resp.json()

            # Flatten the join: extract telegram_chat_id from nested profiles
            configs = []
            for row in rows:
                profile = row.pop("profiles", {})
                if isinstance(profile, dict):
                    row["telegram_chat_id"] = profile.get("telegram_chat_id")
                elif isinstance(profile, list) and profile:
                    row["telegram_chat_id"] = profile[0].get("telegram_chat_id")
                else:
                    row["telegram_chat_id"] = None
                configs.append(row)

            return configs

    except Exception as e:
        logger.error(f"[Scheduler] Failed to fetch coach configs: {e}", exc_info=True)
        return []


# ──────────────────────────────────────────────
# Global Instance (maintains API contract with main.py)
# ──────────────────────────────────────────────

scheduler = CoachScheduler()
