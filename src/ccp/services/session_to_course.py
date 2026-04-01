"""FR-CA11-07 — Session-to-Course Auto Pipeline.

Converts a series of OBS-recorded coaching sessions (via Session
Intelligence Reports from FR-CA11-05) into a structured, drip-fed
course delivered through AFFiNE + Telegram.

Pipeline: Session grouping by topic cluster → Chapter extraction →
          Drip schedule (Atlas 4+1+2) → Delivery via Telegram + AFFiNE.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    CourseAssemblyResult,
    CourseChapter,
    CourseDefinition,
    DripDeliveryResult,
    DripSchedule,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_GABRIELLE = "Gabrielle"
MIN_CLUSTER_OVERLAP = 2          # sessions sharing ≥2 topic clusters → same course
MIN_SESSIONS_FOR_COURSE = 2      # at least 2 sessions needed to create a course
CONTENT_TYPE_COURSE_CHAPTER = "course_chapter"

# Atlas 4+1+2 — default active days (Mon=0 .. Sun=6)
ATLAS_ACTIVE_DAYS = {0, 1, 2, 3}      # Mon-Thu
ATLAS_REFLECTION_DAYS = {4}            # Fri
ATLAS_REST_DAYS = {5, 6}               # Sat-Sun

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

DRIP_SCHEDULE_SQL = """
CREATE TABLE IF NOT EXISTS drip_schedule (
    drip_id         TEXT PRIMARY KEY,
    course_id       TEXT NOT NULL,
    client_id       TEXT NOT NULL,
    chapter_number  INTEGER NOT NULL,
    delivery_date   DATE NOT NULL,
    delivery_time   TEXT NOT NULL DEFAULT '09:00',
    timezone        TEXT NOT NULL DEFAULT 'Europe/Paris',
    delivered_at    TIMESTAMPTZ,
    engaged_at      TIMESTAMPTZ
);
"""

COURSE_REGISTRY_SQL = """
CREATE TABLE IF NOT EXISTS course_registry (
    course_id       TEXT PRIMARY KEY,
    coach_id        TEXT NOT NULL,
    title           TEXT NOT NULL,
    topic_clusters  JSONB NOT NULL,
    total_chapters  INTEGER NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class SessionIntelligenceStoreProtocol(Protocol):
    async def get_sessions_for_coach(self, coach_id: str) -> list[dict[str, Any]]: ...


class AtlasRoadmapProtocol(Protocol):
    def get_active_days(self, client_id: str) -> set[int]: ...


class AFFiNESyncProtocol(Protocol):
    async def push_content(self, coach_id: str, section: str,
                           title: str, body: str, *,
                           metadata: dict[str, Any] | None = None) -> str: ...


class TelegramProtocol(Protocol):
    async def send_message(self, chat_id: str, text: str) -> None: ...


class LearningPathHookProtocol(Protocol):
    async def on_voice_lesson(self, entry: dict[str, Any]) -> None: ...


# ---------------------------------------------------------------------------
# Stage 1 — Course Assembly (Gabrielle)
# ---------------------------------------------------------------------------


class SessionGrouper:
    """Groups sessions by overlapping topic clusters.

    Two sessions belong to the same course if they share
    ≥ ``MIN_CLUSTER_OVERLAP`` topic clusters.
    """

    @staticmethod
    def group_sessions(
        sessions: list[dict[str, Any]],
    ) -> list[list[dict[str, Any]]]:
        if not sessions:
            return []

        used: set[int] = set()
        groups: list[list[dict[str, Any]]] = []

        for i, sess_a in enumerate(sessions):
            if i in used:
                continue
            group = [sess_a]
            used.add(i)
            clusters_a = set(sess_a.get("topic_clusters", []))
            for j, sess_b in enumerate(sessions):
                if j in used:
                    continue
                clusters_b = set(sess_b.get("topic_clusters", []))
                if len(clusters_a & clusters_b) >= MIN_CLUSTER_OVERLAP:
                    group.append(sess_b)
                    used.add(j)
                    clusters_a = clusters_a | clusters_b  # widen for transitive grouping
            if len(group) >= MIN_SESSIONS_FOR_COURSE:
                groups.append(group)

        return groups


class ChapterExtractor:
    """Extracts chapter content from a session intelligence report."""

    @staticmethod
    def extract_chapter(
        session: dict[str, Any],
        chapter_number: int,
    ) -> CourseChapter:
        title = session.get("title") or session.get("primary_topic", "Untitled Session")
        timestamps = session.get("key_timestamps", [])
        insights = session.get("key_insights", [])
        actions = session.get("action_items", [])
        return CourseChapter(
            chapter_number=chapter_number,
            session_id=session.get("session_id", str(uuid.uuid4())),
            title=title,
            key_timestamps=timestamps,
            key_insight=insights[0] if insights else "Key insight from this session",
            action_item=actions[0] if actions else "Reflect on the key insight from this chapter",
        )


class CourseAssembler:
    """Gabrielle — assembles grouped sessions into course definitions."""

    def __init__(self) -> None:
        self._grouper = SessionGrouper()
        self._extractor = ChapterExtractor()

    def assemble_courses(
        self,
        sessions: list[dict[str, Any]],
        coach_id: str,
    ) -> list[CourseDefinition]:
        # Sort sessions chronologically
        sorted_sessions = sorted(
            sessions,
            key=lambda s: s.get("created_at", ""),
        )
        groups = self._grouper.group_sessions(sorted_sessions)
        courses: list[CourseDefinition] = []

        for group in groups:
            all_clusters: set[str] = set()
            chapters: list[CourseChapter] = []
            for idx, sess in enumerate(group, 1):
                all_clusters.update(sess.get("topic_clusters", []))
                chapters.append(self._extractor.extract_chapter(sess, idx))
            cluster_list = sorted(all_clusters)
            title = self._derive_title(cluster_list, len(chapters))
            course = CourseDefinition(
                coach_id=coach_id,
                title=title,
                topic_clusters=cluster_list,
                chapters=chapters,
                total_chapters=len(chapters),
            )
            courses.append(course)

        return courses

    @staticmethod
    def _derive_title(clusters: list[str], chapter_count: int) -> str:
        topic = clusters[0].replace("_", " ").title() if clusters else "Coaching"
        return f"{topic} — A {chapter_count}-Session Journey"


# ---------------------------------------------------------------------------
# Stage 2 — Drip Schedule (Atlas 4+1+2)
# ---------------------------------------------------------------------------


class DripScheduleCalculator:
    """Calculates drip delivery dates aligned to Atlas roadmap active days."""

    def __init__(self, atlas: AtlasRoadmapProtocol | None = None) -> None:
        self._atlas = atlas

    def compute_schedule(
        self,
        course: CourseDefinition,
        client_id: str,
        start_date: datetime | None = None,
        delivery_time: str = "09:00",
        tz: str = "Europe/Paris",
    ) -> DripSchedule:
        active_days = self._get_active_days(client_id)
        start = start_date or datetime.now(timezone.utc)
        dates: list[str] = []
        current = start
        assigned = 0
        max_scan = 60  # safety cap

        while assigned < course.total_chapters and max_scan > 0:
            if current.weekday() in active_days:
                dates.append(current.strftime("%Y-%m-%d"))
                assigned += 1
            current += timedelta(days=1)
            max_scan -= 1

        return DripSchedule(
            client_id=client_id,
            chapter_delivery_dates=dates,
            delivery_time=delivery_time,
            timezone=tz,
        )

    def _get_active_days(self, client_id: str) -> set[int]:
        if self._atlas:
            return self._atlas.get_active_days(client_id)
        return ATLAS_ACTIVE_DAYS


# ---------------------------------------------------------------------------
# Stage 3 — Drip Delivery
# ---------------------------------------------------------------------------


class DripDeliveryEngine:
    """Delivers chapter drips via Telegram + AFFiNE."""

    def __init__(
        self,
        affine_sync: AFFiNESyncProtocol,
        telegram: TelegramProtocol | None = None,
    ) -> None:
        self._affine = affine_sync
        self._telegram = telegram

    async def deliver_chapter(
        self,
        course: CourseDefinition,
        chapter: CourseChapter,
        client_id: str,
        chat_id: str | None = None,
    ) -> DripDeliveryResult:
        result = DripDeliveryResult(chapter_number=chapter.chapter_number)

        # AFFiNE push — full chapter content
        try:
            body = self._format_chapter_body(chapter)
            page_id = await self._affine.push_content(
                course.coach_id,
                "learning_library",
                chapter.title,
                body,
                metadata={
                    "course_id": course.course_id,
                    "chapter_number": chapter.chapter_number,
                    "session_id": chapter.session_id,
                },
            )
            result.affine_pushed = True
            result.page_id = page_id
        except Exception as exc:
            result.error = f"AFFiNE push failed: {exc}"

        # Telegram drip — snippet
        if self._telegram and chat_id:
            try:
                snippet = self._format_telegram_snippet(course, chapter, result.page_id)
                await self._telegram.send_message(chat_id, snippet)
                result.telegram_sent = True
            except Exception:
                pass  # non-blocking

        return result

    @staticmethod
    def _format_chapter_body(chapter: CourseChapter) -> str:
        lines = [
            f"# Chapter {chapter.chapter_number}: {chapter.title}\n",
            f"**Key Insight:** {chapter.key_insight}\n",
            f"**Action Item:** {chapter.action_item}\n",
        ]
        if chapter.key_timestamps:
            lines.append("**Key Moments:** " + ", ".join(chapter.key_timestamps) + "\n")
        return "\n".join(lines)

    @staticmethod
    def _format_telegram_snippet(
        course: CourseDefinition,
        chapter: CourseChapter,
        page_id: str | None,
    ) -> str:
        link = f"[Open in AFFiNE]({page_id})" if page_id else ""
        return (
            f"Chapter {chapter.chapter_number}/{course.total_chapters}: "
            f"{chapter.title}\n\n"
            f"Key insight: {chapter.key_insight}\n\n"
            f"Action: {chapter.action_item}\n\n"
            f"{link}"
        )


# ---------------------------------------------------------------------------
# Orchestrator — SessionToCoursePipeline
# ---------------------------------------------------------------------------


class SessionToCoursePipeline:
    """End-to-end pipeline: session intelligence reports → drip-fed course."""

    def __init__(
        self,
        session_store: SessionIntelligenceStoreProtocol,
        affine_sync: AFFiNESyncProtocol,
        atlas: AtlasRoadmapProtocol | None = None,
        learning_path_hook: LearningPathHookProtocol | None = None,
        telegram: TelegramProtocol | None = None,
    ) -> None:
        self._session_store = session_store
        self._assembler = CourseAssembler()
        self._scheduler = DripScheduleCalculator(atlas)
        self._delivery = DripDeliveryEngine(affine_sync, telegram)
        self._lp_hook = learning_path_hook

    async def assemble_courses(
        self,
        coach_id: str,
    ) -> list[CourseDefinition]:
        sessions = await self._session_store.get_sessions_for_coach(coach_id)
        return self._assembler.assemble_courses(sessions, coach_id)

    async def schedule_and_deliver_course(
        self,
        course: CourseDefinition,
        client_id: str,
        chat_id: str | None = None,
        start_date: datetime | None = None,
    ) -> CourseAssemblyResult:
        # Schedule drips
        schedule = self._scheduler.compute_schedule(
            course, client_id, start_date=start_date
        )
        course.drip_schedule = schedule

        # Register chapters in learning path
        if self._lp_hook:
            for ch in course.chapters:
                try:
                    await self._lp_hook.on_voice_lesson({
                        "lesson_id": ch.session_id,
                        "coach_id": course.coach_id,
                        "topic_cluster": course.topic_clusters[0] if course.topic_clusters else "general",
                        "difficulty_level": "developing",
                        "content_type": CONTENT_TYPE_COURSE_CHAPTER,
                    })
                except Exception:
                    pass

        # Deliver first chapter immediately (Day 1 drip)
        if course.chapters:
            await self._delivery.deliver_chapter(
                course, course.chapters[0], client_id, chat_id
            )

        return CourseAssemblyResult(
            success=True,
            course=course,
            courses_created=1,
        )

    async def run_full_pipeline(
        self,
        coach_id: str,
        client_id: str,
        chat_id: str | None = None,
        start_date: datetime | None = None,
    ) -> list[CourseAssemblyResult]:
        courses = await self.assemble_courses(coach_id)
        if not courses:
            return [CourseAssemblyResult(success=False, error="No courses could be assembled")]
        results: list[CourseAssemblyResult] = []
        for course in courses:
            r = await self.schedule_and_deliver_course(
                course, client_id, chat_id, start_date
            )
            results.append(r)
        return results
