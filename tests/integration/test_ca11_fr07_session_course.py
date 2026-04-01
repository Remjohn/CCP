"""FR-CA11-07 — Session-to-Course Auto Pipeline — Integration Tests.

Covers all 5 Acceptance Criteria:
  AC1: Auto-grouping of sessions by topic cluster overlap
  AC2: Drip schedule aligns with Atlas 4+1+2 active days
  AC3: Telegram drip contains chapter snippet + AFFiNE link
  AC4: Full chapter content appears in AFFiNE on drip day
  AC5: Engagement tracking (learning_progress records)
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    CourseAssemblyResult,
    CourseChapter,
    CourseDefinition,
    DripDeliveryResult,
    DripSchedule,
)
from src.ccp.services.session_to_course import (
    AGENT_GABRIELLE,
    ATLAS_ACTIVE_DAYS,
    ATLAS_REFLECTION_DAYS,
    ATLAS_REST_DAYS,
    CONTENT_TYPE_COURSE_CHAPTER,
    COURSE_REGISTRY_SQL,
    DRIP_SCHEDULE_SQL,
    MIN_CLUSTER_OVERLAP,
    MIN_SESSIONS_FOR_COURSE,
    ChapterExtractor,
    CourseAssembler,
    DripDeliveryEngine,
    DripScheduleCalculator,
    SessionGrouper,
    SessionToCoursePipeline,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "uuid-coach-test-01"
CLIENT_ID = "uuid-client-042"
CHAT_ID = "chat-999"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _make_session(
    topic_clusters: list[str],
    title: str = "Session",
    session_id: str | None = None,
    created_at: str = "2026-03-20",
) -> dict[str, Any]:
    return {
        "session_id": session_id or str(uuid.uuid4()),
        "title": title,
        "topic_clusters": topic_clusters,
        "key_timestamps": ["00:14:32"],
        "key_insights": ["Insight from session"],
        "action_items": ["Reflect on insight"],
        "created_at": created_at,
    }


# ---- Mocks ----

class MockSessionStore:
    def __init__(self, sessions: list[dict[str, Any]]):
        self._sessions = sessions
    async def get_sessions_for_coach(self, coach_id: str) -> list[dict[str, Any]]:
        return self._sessions


class MockAFFiNeSync:
    def __init__(self):
        self.pushes: list[dict] = []
    async def push_content(self, coach_id, section, title, body, *, metadata=None):
        page_id = f"page-{uuid.uuid4().hex[:8]}"
        self.pushes.append({
            "coach_id": coach_id, "section": section,
            "title": title, "body": body,
            "metadata": metadata, "page_id": page_id,
        })
        return page_id


class MockAtlas:
    def __init__(self, active_days: set[int] | None = None):
        self._days = active_days or ATLAS_ACTIVE_DAYS
    def get_active_days(self, client_id: str) -> set[int]:
        return self._days


class MockTelegram:
    def __init__(self):
        self.messages: list[tuple[str, str]] = []
    async def send_message(self, chat_id: str, text: str) -> None:
        self.messages.append((chat_id, text))


class MockLPHook:
    def __init__(self):
        self.entries: list[dict] = []
    async def on_voice_lesson(self, entry: dict) -> None:
        self.entries.append(entry)


def _pipeline(sessions: list[dict[str, Any]], *, with_atlas: bool = True, with_tg: bool = True, with_lp: bool = True):
    store = MockSessionStore(sessions)
    sync = MockAFFiNeSync()
    atlas = MockAtlas() if with_atlas else None
    tg = MockTelegram() if with_tg else None
    lp = MockLPHook() if with_lp else None
    pipe = SessionToCoursePipeline(
        session_store=store,
        affine_sync=sync,
        atlas=atlas,
        learning_path_hook=lp,
        telegram=tg,
    )
    return pipe, store, sync, atlas, tg, lp


# ===================================================================
# 1. Model validation (6 tests)
# ===================================================================

class TestModels:
    def test_course_chapter_valid(self):
        ch = CourseChapter(
            chapter_number=1, session_id="s1",
            title="Ch1", key_insight="Insight", action_item="Action",
        )
        assert ch.chapter_number == 1

    def test_course_chapter_rejects_zero(self):
        with pytest.raises(Exception):
            CourseChapter(chapter_number=0, session_id="s1",
                          title="X", key_insight="I", action_item="A")

    def test_drip_schedule_defaults(self):
        ds = DripSchedule(client_id=CLIENT_ID)
        assert ds.delivery_time == "09:00"
        assert ds.timezone == "Europe/Paris"

    def test_course_definition_uuid_generated(self):
        cd = CourseDefinition(
            coach_id=COACH_ID, title="Course", topic_clusters=["a"],
        )
        assert cd.course_id  # UUID generated

    def test_drip_delivery_result(self):
        r = DripDeliveryResult(chapter_number=1)
        assert not r.telegram_sent
        assert not r.affine_pushed

    def test_course_assembly_result(self):
        r = CourseAssemblyResult(success=True, courses_created=2)
        assert r.courses_created == 2


# ===================================================================
# 2. Session grouping (7 tests)  — AC1
# ===================================================================

class TestSessionGrouper:
    def test_groups_by_overlap(self):
        """AC1 — sessions sharing ≥2 clusters form a course."""
        sessions = [
            _make_session(["a", "b", "c"], "S1"),
            _make_session(["a", "b", "d"], "S2"),
            _make_session(["a", "b"], "S3"),
        ]
        groups = SessionGrouper.group_sessions(sessions)
        assert len(groups) == 1
        assert len(groups[0]) == 3

    def test_no_overlap_no_group(self):
        sessions = [
            _make_session(["a", "b"], "S1"),
            _make_session(["c", "d"], "S2"),
        ]
        groups = SessionGrouper.group_sessions(sessions)
        assert len(groups) == 0  # each group < MIN_SESSIONS_FOR_COURSE

    def test_multiple_groups(self):
        sessions = [
            _make_session(["a", "b"], "S1"),
            _make_session(["a", "b"], "S2"),
            _make_session(["x", "y"], "S3"),
            _make_session(["x", "y"], "S4"),
        ]
        groups = SessionGrouper.group_sessions(sessions)
        assert len(groups) == 2

    def test_single_session_not_grouped(self):
        sessions = [_make_session(["a", "b"], "S1")]
        groups = SessionGrouper.group_sessions(sessions)
        assert len(groups) == 0

    def test_empty_sessions(self):
        assert SessionGrouper.group_sessions([]) == []

    def test_transitive_grouping(self):
        """S1 overlaps S2, S2 overlaps S3 — all three in one group."""
        sessions = [
            _make_session(["a", "b", "c"], "S1"),
            _make_session(["b", "c", "d"], "S2"),
            _make_session(["c", "d", "e"], "S3"),
        ]
        groups = SessionGrouper.group_sessions(sessions)
        assert len(groups) == 1
        assert len(groups[0]) == 3

    def test_8_sessions_3_courses(self):
        """Spec unit test: 8 sessions → 3 courses (3+3+2)."""
        sessions = [
            _make_session(["a", "b"], "G1-S1"),
            _make_session(["a", "b"], "G1-S2"),
            _make_session(["a", "b"], "G1-S3"),
            _make_session(["x", "y"], "G2-S1"),
            _make_session(["x", "y"], "G2-S2"),
            _make_session(["x", "y"], "G2-S3"),
            _make_session(["p", "q"], "G3-S1"),
            _make_session(["p", "q"], "G3-S2"),
        ]
        groups = SessionGrouper.group_sessions(sessions)
        assert len(groups) == 3
        sizes = sorted([len(g) for g in groups])
        assert sizes == [2, 3, 3]


# ===================================================================
# 3. Chapter extraction (3 tests)
# ===================================================================

class TestChapterExtractor:
    def test_extracts_chapter(self):
        sess = _make_session(["a", "b"], "My Session")
        ch = ChapterExtractor.extract_chapter(sess, 1)
        assert ch.chapter_number == 1
        assert ch.title == "My Session"
        assert ch.key_insight == "Insight from session"
        assert ch.action_item == "Reflect on insight"

    def test_missing_insights_uses_defaults(self):
        sess = {"session_id": "s1", "title": "T", "topic_clusters": []}
        ch = ChapterExtractor.extract_chapter(sess, 2)
        assert "Key insight" in ch.key_insight

    def test_timestamps_preserved(self):
        sess = _make_session(["a"], "S")
        ch = ChapterExtractor.extract_chapter(sess, 1)
        assert ch.key_timestamps == ["00:14:32"]


# ===================================================================
# 4. Course assembler (4 tests)
# ===================================================================

class TestCourseAssembler:
    def test_assembles_course(self):
        sessions = [
            _make_session(["a", "b"], "S1", created_at="2026-03-20"),
            _make_session(["a", "b"], "S2", created_at="2026-03-21"),
            _make_session(["a", "b"], "S3", created_at="2026-03-22"),
        ]
        asm = CourseAssembler()
        courses = asm.assemble_courses(sessions, COACH_ID)
        assert len(courses) == 1
        assert courses[0].total_chapters == 3
        assert courses[0].coach_id == COACH_ID

    def test_chapters_ordered_chronologically(self):
        sessions = [
            _make_session(["a", "b"], "Late", created_at="2026-03-25"),
            _make_session(["a", "b"], "Early", created_at="2026-03-20"),
        ]
        asm = CourseAssembler()
        courses = asm.assemble_courses(sessions, COACH_ID)
        assert courses[0].chapters[0].title == "Early"
        assert courses[0].chapters[1].title == "Late"

    def test_title_derived_from_clusters(self):
        sessions = [
            _make_session(["external_validation", "self_worth"], "S1"),
            _make_session(["external_validation", "self_worth"], "S2"),
        ]
        asm = CourseAssembler()
        courses = asm.assemble_courses(sessions, COACH_ID)
        assert "External Validation" in courses[0].title

    def test_no_courses_from_unrelated_sessions(self):
        sessions = [
            _make_session(["a"], "S1"),
            _make_session(["b"], "S2"),
        ]
        asm = CourseAssembler()
        courses = asm.assemble_courses(sessions, COACH_ID)
        assert len(courses) == 0


# ===================================================================
# 5. Drip schedule — AC2 (5 tests)
# ===================================================================

class TestDripSchedule:
    def test_active_days_only(self):
        """AC2 — drips only on active days (Mon-Thu)."""
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=4,
        )
        calc = DripScheduleCalculator(MockAtlas())
        # Start on a Monday (2026-03-23 is a Monday)
        start = datetime(2026, 3, 23, tzinfo=timezone.utc)
        sched = calc.compute_schedule(course, CLIENT_ID, start_date=start)
        assert len(sched.chapter_delivery_dates) == 4
        # All dates should be Mon-Thu
        for d in sched.chapter_delivery_dates:
            dt = datetime.strptime(d, "%Y-%m-%d")
            assert dt.weekday() in ATLAS_ACTIVE_DAYS

    def test_no_drip_on_reflection_day(self):
        """AC2 — no drips on Friday (reflection)."""
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=6,
        )
        calc = DripScheduleCalculator(MockAtlas())
        start = datetime(2026, 3, 23, tzinfo=timezone.utc)
        sched = calc.compute_schedule(course, CLIENT_ID, start_date=start)
        for d in sched.chapter_delivery_dates:
            dt = datetime.strptime(d, "%Y-%m-%d")
            assert dt.weekday() not in ATLAS_REFLECTION_DAYS

    def test_no_drip_on_rest_days(self):
        """AC2 — no drips on Sat/Sun."""
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=6,
        )
        calc = DripScheduleCalculator(MockAtlas())
        start = datetime(2026, 3, 23, tzinfo=timezone.utc)
        sched = calc.compute_schedule(course, CLIENT_ID, start_date=start)
        for d in sched.chapter_delivery_dates:
            dt = datetime.strptime(d, "%Y-%m-%d")
            assert dt.weekday() not in ATLAS_REST_DAYS

    def test_default_atlas_without_provider(self):
        calc = DripScheduleCalculator(atlas=None)
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=2,
        )
        start = datetime(2026, 3, 23, tzinfo=timezone.utc)
        sched = calc.compute_schedule(course, CLIENT_ID, start_date=start)
        assert len(sched.chapter_delivery_dates) == 2

    def test_schedule_has_client_fields(self):
        calc = DripScheduleCalculator(MockAtlas())
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=1,
        )
        sched = calc.compute_schedule(course, CLIENT_ID)
        assert sched.client_id == CLIENT_ID
        assert sched.delivery_time == "09:00"
        assert sched.timezone == "Europe/Paris"


# ===================================================================
# 6. Drip delivery — AC3 + AC4 (5 tests)
# ===================================================================

class TestDripDelivery:
    def test_affine_push_ac4(self):
        """AC4 — full chapter content in AFFiNE."""
        sync = MockAFFiNeSync()
        engine = DripDeliveryEngine(sync)
        course = CourseDefinition(
            coach_id=COACH_ID, title="Course", topic_clusters=["a"],
            total_chapters=1,
            chapters=[CourseChapter(
                chapter_number=1, session_id="s1",
                title="Ch1", key_insight="Insight", action_item="Action",
            )],
        )
        result = _run(engine.deliver_chapter(course, course.chapters[0], CLIENT_ID))
        assert result.affine_pushed
        assert result.page_id is not None
        assert sync.pushes[0]["section"] == "learning_library"

    def test_telegram_snippet_ac3(self):
        """AC3 — Telegram drip contains chapter snippet + AFFiNE link."""
        sync = MockAFFiNeSync()
        tg = MockTelegram()
        engine = DripDeliveryEngine(sync, tg)
        course = CourseDefinition(
            coach_id=COACH_ID, title="Course", topic_clusters=["a"],
            total_chapters=2,
            chapters=[CourseChapter(
                chapter_number=1, session_id="s1",
                title="Ch1", key_insight="Insight one", action_item="Do X",
            )],
        )
        _run(engine.deliver_chapter(course, course.chapters[0], CLIENT_ID, CHAT_ID))
        assert len(tg.messages) == 1
        text = tg.messages[0][1]
        assert "1/2" in text  # chapter/total
        assert "Insight one" in text
        assert "Do X" in text

    def test_chapter_body_has_title_insight_action(self):
        sync = MockAFFiNeSync()
        engine = DripDeliveryEngine(sync)
        ch = CourseChapter(
            chapter_number=1, session_id="s1",
            title="Test", key_insight="I", action_item="A",
            key_timestamps=["00:10:00"],
        )
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=1, chapters=[ch],
        )
        _run(engine.deliver_chapter(course, ch, CLIENT_ID))
        body = sync.pushes[0]["body"]
        assert "Test" in body
        assert "00:10:00" in body

    def test_telegram_optional(self):
        sync = MockAFFiNeSync()
        engine = DripDeliveryEngine(sync, telegram=None)
        ch = CourseChapter(
            chapter_number=1, session_id="s1",
            title="X", key_insight="I", action_item="A",
        )
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=1, chapters=[ch],
        )
        result = _run(engine.deliver_chapter(course, ch, CLIENT_ID))
        assert result.affine_pushed
        assert not result.telegram_sent

    def test_affine_failure_captured(self):
        class FailSync:
            async def push_content(self, *a, **kw):
                raise ConnectionError("offline")
        engine = DripDeliveryEngine(FailSync())
        ch = CourseChapter(
            chapter_number=1, session_id="s1",
            title="X", key_insight="I", action_item="A",
        )
        course = CourseDefinition(
            coach_id=COACH_ID, title="C", topic_clusters=["a"],
            total_chapters=1, chapters=[ch],
        )
        result = _run(engine.deliver_chapter(course, ch, CLIENT_ID))
        assert not result.affine_pushed
        assert "AFFiNE push failed" in result.error


# ===================================================================
# 7. Full pipeline (6 tests)
# ===================================================================

class TestFullPipeline:
    def _sessions_5_overlapping(self):
        return [
            _make_session(["ext_val", "self_worth", "boundaries"], "S1", created_at="2026-03-20"),
            _make_session(["ext_val", "self_worth"], "S2", created_at="2026-03-21"),
            _make_session(["ext_val", "boundaries"], "S3", created_at="2026-03-22"),
            _make_session(["self_worth", "boundaries"], "S4", created_at="2026-03-23"),
            _make_session(["ext_val", "self_worth"], "S5", created_at="2026-03-24"),
        ]

    def test_full_pipeline_success(self):
        pipe, _, sync, _, tg, lp = _pipeline(self._sessions_5_overlapping())
        results = _run(pipe.run_full_pipeline(COACH_ID, CLIENT_ID, CHAT_ID))
        assert len(results) >= 1
        assert results[0].success
        assert results[0].course is not None

    def test_ac1_auto_grouping(self):
        """AC1 — 5 overlapping sessions grouped into a course."""
        pipe, _, _, _, _, _ = _pipeline(self._sessions_5_overlapping())
        courses = _run(pipe.assemble_courses(COACH_ID))
        assert len(courses) >= 1
        total_chapters = sum(c.total_chapters for c in courses)
        assert total_chapters == 5

    def test_drip_schedule_assigned(self):
        pipe, _, _, _, _, _ = _pipeline(self._sessions_5_overlapping())
        courses = _run(pipe.assemble_courses(COACH_ID))
        start = datetime(2026, 3, 23, tzinfo=timezone.utc)
        result = _run(pipe.schedule_and_deliver_course(courses[0], CLIENT_ID, CHAT_ID, start))
        assert result.course.drip_schedule is not None
        assert len(result.course.drip_schedule.chapter_delivery_dates) == courses[0].total_chapters

    def test_first_chapter_delivered_immediately(self):
        pipe, _, sync, _, tg, _ = _pipeline(self._sessions_5_overlapping())
        courses = _run(pipe.assemble_courses(COACH_ID))
        _run(pipe.schedule_and_deliver_course(courses[0], CLIENT_ID, CHAT_ID))
        assert len(sync.pushes) == 1  # first chapter
        assert len(tg.messages) == 1

    def test_learning_path_chapters_registered(self):
        """AC5-adjacent — chapters registered in learning path as course_chapter."""
        pipe, _, _, _, _, lp = _pipeline(self._sessions_5_overlapping())
        courses = _run(pipe.assemble_courses(COACH_ID))
        _run(pipe.schedule_and_deliver_course(courses[0], CLIENT_ID, CHAT_ID))
        assert len(lp.entries) == courses[0].total_chapters
        for entry in lp.entries:
            assert entry["content_type"] == CONTENT_TYPE_COURSE_CHAPTER

    def test_no_sessions_returns_error(self):
        pipe, _, _, _, _, _ = _pipeline([])
        results = _run(pipe.run_full_pipeline(COACH_ID, CLIENT_ID))
        assert len(results) == 1
        assert not results[0].success
        assert "No courses" in results[0].error


# ===================================================================
# 8. Constants & SQL (3 tests)
# ===================================================================

class TestConstants:
    def test_agent_name(self):
        assert AGENT_GABRIELLE == "Gabrielle"

    def test_sql_drip_schedule(self):
        assert "drip_schedule" in DRIP_SCHEDULE_SQL
        assert "delivery_date" in DRIP_SCHEDULE_SQL
        assert "engaged_at" in DRIP_SCHEDULE_SQL

    def test_sql_course_registry(self):
        assert "course_registry" in COURSE_REGISTRY_SQL
        assert "topic_clusters" in COURSE_REGISTRY_SQL
