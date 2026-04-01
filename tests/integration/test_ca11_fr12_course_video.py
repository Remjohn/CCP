"""FR-CA11-12 — Course Video Generation via CMF Pipeline — Integration Tests.

Covers all 5 Acceptance Criteria:
  AC1: Course video generation (5-10 min .mp4)
  AC2: Editorial template adherence (no rapid cuts, clean captions, no B-roll)
  AC3: Excalidraw visual aids (≥2 diagrams)
  AC4: Learning path tagged
  AC5: Client delivery (program-tagged)
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    AmbientMoodProfile,
    CaptionStyle,
    CourseVideoEditorialTemplate,
    CourseVideoManifest,
    CourseVideoResult,
    LearningPathRegistration,
    VisualAid,
    VisualAidType,
)
from src.ccp.services.course_video_cmf import (
    ALLOWED_MOOD_PROFILES,
    COURSE_VIDEO_COMMAND,
    COURSE_VIDEO_SQL,
    MAX_DURATION_SECONDS,
    MIN_DIAGRAMS,
    MIN_DURATION_SECONDS,
    MIN_SCENE_CHANGE_SECONDS,
    CourseVideoCommandHandler,
    CourseVideoPipeline,
    EditorialTemplateValidator,
    VisualAidAssembler,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "coach-jpr-001"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---- Mocks ----

class MockTranscriber:
    async def transcribe(self, voice_note_url):
        return "Breaking the approval trap means recognizing external validation patterns."


class MockDiagramGenerator:
    def __init__(self, count=3):
        self._count = count
    async def generate_diagrams(self, topics, count):
        return [{"url": f"s3://diagrams/d{i}.png"} for i in range(min(count, self._count))]


class MockImageSourcer:
    async def source_images(self, themes, count):
        return [{"url": f"s3://images/img{i}.jpg", "source": "unsplash",
                 "query": themes[0] if themes else "coaching"} for i in range(count)]


class MockRenderEngine:
    async def render_course_video(self, narration, visual_aids, template, audio_mood):
        return {"video_url": f"s3://rendered/{uuid.uuid4().hex[:8]}.mp4",
                "duration_seconds": 420}


class FailingRenderEngine:
    async def render_course_video(self, *a, **kw):
        raise RuntimeError("GPU unavailable")


class MockLearningPathAgent:
    def __init__(self):
        self.registered: list[dict] = []
    async def categorize_and_register(self, manifest):
        self.registered.append(manifest)
        return {"topic_cluster": "external_validation",
                "difficulty_level": "developing",
                "program_tag": "90day-leadership-mastery"}


# ===================================================================
# 1. Model validation (7 tests)
# ===================================================================

class TestModels:
    def test_editorial_template_defaults(self):
        t = CourseVideoEditorialTemplate()
        assert t.template_name == "course_video"
        assert t.duration_range_seconds == (300, 600)
        assert t.caption_style == CaptionStyle.clean_centered
        assert not t.broll_allowed

    def test_scene_change_interval(self):
        t = CourseVideoEditorialTemplate()
        lo, hi = t.scene_change_interval_seconds
        assert lo >= MIN_SCENE_CHANGE_SECONDS
        assert hi >= lo

    def test_allowed_mood_profiles(self):
        t = CourseVideoEditorialTemplate()
        for m in t.audio_mood_profiles:
            assert m in ALLOWED_MOOD_PROFILES

    def test_visual_aid(self):
        aid = VisualAid(type=VisualAidType.excalidraw_diagram, url="s3://d.png")
        assert aid.type == VisualAidType.excalidraw_diagram

    def test_manifest(self):
        m = CourseVideoManifest(
            asset_id="JPR-CMF-001", coach_id=COACH_ID,
            title="Test", duration_seconds=420,
            video_url="s3://v.mp4",
        )
        assert m.editorial_template == "course_video"
        assert m.ambient_audio_mood == AmbientMoodProfile.contemplation

    def test_learning_path_registration(self):
        r = LearningPathRegistration(topic_cluster="external_validation")
        assert r.content_type == "course_video"
        assert r.difficulty_level == "developing"

    def test_course_video_result(self):
        r = CourseVideoResult(success=True)
        assert not r.fallback_text_delivered


# ===================================================================
# 2. Editorial Template Validator — AC2 (5 tests)
# ===================================================================

class TestEditorialValidator:
    def test_default_passes_ac2(self):
        """AC2 — default template adheres to course video rules."""
        t = EditorialTemplateValidator.default_template()
        errors = EditorialTemplateValidator.validate(t)
        assert errors == []

    def test_broll_rejected(self):
        """AC2 — B-roll retention edits forbidden."""
        t = CourseVideoEditorialTemplate(broll_allowed=True)
        errors = EditorialTemplateValidator.validate(t)
        assert any("B-roll" in e for e in errors)

    def test_rapid_fire_rejected(self):
        t = CourseVideoEditorialTemplate(caption_style=CaptionStyle.rapid_fire)
        errors = EditorialTemplateValidator.validate(t)
        assert any("clean_centered" in e for e in errors)

    def test_short_scene_change_rejected(self):
        t = CourseVideoEditorialTemplate(scene_change_interval_seconds=(5, 10))
        errors = EditorialTemplateValidator.validate(t)
        assert any("scene change" in e for e in errors)

    def test_duration_out_of_range(self):
        t = CourseVideoEditorialTemplate(duration_range_seconds=(100, 900))
        errors = EditorialTemplateValidator.validate(t)
        assert len(errors) == 2  # too short min + too long max


# ===================================================================
# 3. Command Handler (3 tests)
# ===================================================================

class TestCommandHandler:
    def test_parse_topic(self):
        r = CourseVideoCommandHandler.parse_command('/course-video "Breaking Approval Seeking"')
        assert r["topic"] == "Breaking Approval Seeking"

    def test_parse_empty(self):
        r = CourseVideoCommandHandler.parse_command("/course-video")
        assert r["topic"] == "Untitled Course Video"

    def test_parse_no_quotes(self):
        r = CourseVideoCommandHandler.parse_command("/course-video My Topic")
        assert "My Topic" in r["topic"]


# ===================================================================
# 4. Visual Aid Assembler — AC3 (3 tests)
# ===================================================================

class TestVisualAidAssembler:
    def test_assembles_diagrams_and_images_ac3(self):
        """AC3 — at least 2 diagrams appear."""
        assembler = VisualAidAssembler(
            diagram_generator=MockDiagramGenerator(count=3),
            image_sourcer=MockImageSourcer(),
        )
        aids = _run(assembler.assemble(["external_validation"], diagram_count=3, image_count=4))
        diagrams = [a for a in aids if a.type == VisualAidType.excalidraw_diagram]
        images = [a for a in aids if a.type == VisualAidType.stock_image]
        assert len(diagrams) >= MIN_DIAGRAMS
        assert len(images) >= 1

    def test_no_generators(self):
        assembler = VisualAidAssembler()
        aids = _run(assembler.assemble(["topic"]))
        assert aids == []

    def test_diagram_only(self):
        assembler = VisualAidAssembler(diagram_generator=MockDiagramGenerator(count=2))
        aids = _run(assembler.assemble(["topic"], diagram_count=2))
        assert len(aids) == 2
        assert all(a.type == VisualAidType.excalidraw_diagram for a in aids)


# ===================================================================
# 5. Full Pipeline — AC1 + AC4 + AC5 (7 tests)
# ===================================================================

class TestPipeline:
    def test_full_pipeline_ac1(self):
        """AC1 — 5-10 min video generated from /course-video command."""
        learning = MockLearningPathAgent()
        pipeline = CourseVideoPipeline(
            transcriber=MockTranscriber(),
            diagram_generator=MockDiagramGenerator(),
            image_sourcer=MockImageSourcer(),
            render_engine=MockRenderEngine(),
            learning_path_agent=learning,
        )
        result = _run(pipeline.execute(
            COACH_ID,
            '/course-video "Breaking Approval Seeking"',
            voice_note_url="s3://voice/note.ogg",
            topics=["external_validation", "approval_seeking"],
        ))
        assert result.success
        assert result.manifest is not None
        assert MIN_DURATION_SECONDS <= result.manifest.duration_seconds <= MAX_DURATION_SECONDS
        assert result.manifest.video_url.endswith(".mp4")

    def test_text_brief_mode(self):
        pipeline = CourseVideoPipeline(
            diagram_generator=MockDiagramGenerator(),
            image_sourcer=MockImageSourcer(),
        )
        result = _run(pipeline.execute(COACH_ID, '/course-video "My Topic"'))
        assert result.success
        assert result.manifest.title == "My Topic"

    def test_learning_path_tagged_ac4(self):
        """AC4 — video registered in learning_path_registry."""
        learning = MockLearningPathAgent()
        pipeline = CourseVideoPipeline(
            diagram_generator=MockDiagramGenerator(),
            learning_path_agent=learning,
        )
        result = _run(pipeline.execute(COACH_ID, '/course-video "Topic"'))
        assert result.manifest.learning_path_registration is not None
        assert result.manifest.learning_path_registration.content_type == "course_video"
        assert len(learning.registered) == 1

    def test_program_tag_for_client_delivery_ac5(self):
        """AC5 — program-tagged videos available for client delivery."""
        learning = MockLearningPathAgent()
        pipeline = CourseVideoPipeline(
            diagram_generator=MockDiagramGenerator(),
            learning_path_agent=learning,
        )
        result = _run(pipeline.execute(COACH_ID, '/course-video "Topic"'))
        reg = result.manifest.learning_path_registration
        assert reg.program_tag == "90day-leadership-mastery"

    def test_editorial_template_name(self):
        pipeline = CourseVideoPipeline()
        result = _run(pipeline.execute(COACH_ID, '/course-video "Topic"'))
        assert result.manifest.editorial_template == "course_video"

    def test_ambient_mood(self):
        pipeline = CourseVideoPipeline()
        result = _run(pipeline.execute(COACH_ID, '/course-video "Topic"'))
        assert result.manifest.ambient_audio_mood in ALLOWED_MOOD_PROFILES

    def test_gpu_failure_fallback(self):
        """Fallback: text lesson delivered when GPU render fails."""
        pipeline = CourseVideoPipeline(
            diagram_generator=MockDiagramGenerator(),
            render_engine=FailingRenderEngine(),
        )
        result = _run(pipeline.execute(COACH_ID, '/course-video "Topic"'))
        assert result.success
        assert result.fallback_text_delivered


# ===================================================================
# 6. Constants & SQL (2 tests)
# ===================================================================

class TestConstants:
    def test_constants(self):
        assert COURSE_VIDEO_COMMAND == "/course-video"
        assert MIN_DURATION_SECONDS == 300
        assert MAX_DURATION_SECONDS == 600

    def test_sql_schema(self):
        assert "course_videos" in COURSE_VIDEO_SQL
        assert "video_id" in COURSE_VIDEO_SQL
