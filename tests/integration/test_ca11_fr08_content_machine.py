"""FR-CA11-08 — Content Machine Pipeline — Integration Tests.

Covers all 6 Acceptance Criteria:
  AC1: Content Multiplication (≥5 pieces from 5 insights)
  AC2: Batch Inclusion (matching theme → included)
  AC3: Queue Routing (non-matching → queued)
  AC4: Triple-Pass Validation (all content validated before delivery)
  AC5: Fingerprint Traceability (source_type = SESSION)
  AC6: Non-Interference (no disruption to standard CCF)
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    ContentMachineArray,
    ContentMachineResult,
    QueueStatus,
    SessionContentPiece,
    SessionContentType,
    ValidationStatus,
)
from src.ccp.services.content_machine import (
    AGENT_CESARE,
    AGENT_CHEN,
    AGENT_JULIO,
    AGENT_MARCUS,
    AGENT_SOPHIA,
    AI_DETECTION_MAX,
    EMOTIONAL_INTENSITY_VIDEO_THRESHOLD,
    MIN_EXTRACTION_PIECES,
    PIPELINE_SESSION,
    SESSION_CONTENT_SQL,
    TTT_DRIFT_MAX,
    BatchEvaluator,
    ContentMachinePipeline,
    MicroContentExtractor,
    TriplePassValidator,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "uuid-coach-test-01"
COACH_ACRONYM = "JPR"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _make_report(
    num_insights: int = 5,
    num_breakthroughs: int = 2,
    num_beats: int = 3,
    beat_intensity: float = 0.8,
) -> dict[str, Any]:
    return {
        "session_id": str(uuid.uuid4()),
        "key_insights": [
            {"text": f"Insight number {i+1} about transformation and growth", "timestamp": f"00:{10+i}:00"}
            for i in range(num_insights)
        ],
        "breakthrough_moments": [
            {"description": f"Breakthrough {i+1}: client discovers inner authority"}
            for i in range(num_breakthroughs)
        ],
        "emotional_beats": [
            {"description": f"Emotional beat {i+1}: vulnerability moment", "intensity": beat_intensity, "timestamp": f"00:{20+i}:00"}
            for i in range(num_beats)
        ],
    }


# ---- Mocks ----

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


class MockCCFBatch:
    def __init__(self, keywords: list[str] | None = None, boredom: list[str] | None = None):
        self._keywords = keywords or []
        self._boredom = boredom or []
    def get_current_batch_theme(self, coach_id: str) -> dict[str, Any]:
        return {"keywords": self._keywords}
    def get_boredom_ban_window(self, coach_id: str) -> list[str]:
        return self._boredom


class MockVoiceDNA:
    def __init__(self, drift: float = 0.05):
        self._drift = drift
    def compute_ttt_drift(self, text: str, coach_id: str) -> float:
        return self._drift


def _pipeline(
    *,
    keywords: list[str] | None = None,
    boredom: list[str] | None = None,
    drift: float = 0.05,
    with_sync: bool = True,
    with_batch: bool = True,
):
    sync = MockAFFiNeSync() if with_sync else None
    batch = MockCCFBatch(keywords or [], boredom or []) if with_batch else None
    vdna = MockVoiceDNA(drift)
    pipe = ContentMachinePipeline(
        affine_sync=sync,
        ccf_batch=batch,
        voice_dna=vdna,
    )
    return pipe, sync, batch, vdna


# ===================================================================
# 1. Model validation (5 tests)
# ===================================================================

class TestModels:
    def test_session_content_piece_defaults(self):
        p = SessionContentPiece(
            asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
            text="Some insight",
        )
        assert p.validation_status == ValidationStatus.pending
        assert p.source_type == "SESSION"
        assert p.queue_status == QueueStatus.session_content_queue

    def test_content_machine_array(self):
        arr = ContentMachineArray(session_id="s1", total_extracted=5)
        assert arr.batch_included_count == 0
        assert arr.queued_count == 0

    def test_content_machine_result(self):
        r = ContentMachineResult(success=True)
        assert r.output is None

    def test_session_content_types(self):
        assert SessionContentType.telegram_insight_card.value == "telegram_insight_card"
        assert SessionContentType.instagram_caption.value == "instagram_caption"
        assert SessionContentType.short_form_video_script.value == "short_form_video_script"

    def test_validation_status_values(self):
        assert ValidationStatus.pending.value == "PENDING"
        assert ValidationStatus.passed.value == "PASSED"
        assert ValidationStatus.failed.value == "FAILED"


# ===================================================================
# 2. Micro-content extraction — AC1 (5 tests)
# ===================================================================

class TestMicroContentExtraction:
    def test_extracts_from_5_insights(self):
        """AC1 — 5 insights → ≥5 micro-content pieces."""
        extractor = MicroContentExtractor()
        report = _make_report(num_insights=5, num_breakthroughs=2, num_beats=2)
        pieces = extractor.extract(report, COACH_ID, COACH_ACRONYM)
        assert len(pieces) >= 5

    def test_insight_cards_created(self):
        extractor = MicroContentExtractor()
        report = _make_report(num_insights=3)
        pieces = extractor.extract(report, COACH_ID, COACH_ACRONYM)
        cards = [p for p in pieces if p.content_type == SessionContentType.telegram_insight_card]
        assert len(cards) == 3

    def test_instagram_captions_from_breakthroughs(self):
        extractor = MicroContentExtractor()
        report = _make_report(num_breakthroughs=2)
        pieces = extractor.extract(report, COACH_ID, COACH_ACRONYM)
        captions = [p for p in pieces if p.content_type == SessionContentType.instagram_caption]
        assert len(captions) == 2

    def test_video_scripts_from_high_intensity(self):
        extractor = MicroContentExtractor()
        report = _make_report(num_beats=3, beat_intensity=0.9)
        pieces = extractor.extract(report, COACH_ID, COACH_ACRONYM)
        videos = [p for p in pieces if p.content_type == SessionContentType.short_form_video_script]
        assert len(videos) == 3

    def test_low_intensity_beats_not_video(self):
        extractor = MicroContentExtractor()
        report = _make_report(num_beats=3, beat_intensity=0.3)
        pieces = extractor.extract(report, COACH_ID, COACH_ACRONYM)
        videos = [p for p in pieces if p.content_type == SessionContentType.short_form_video_script]
        assert len(videos) == 0


# ===================================================================
# 3. Batch evaluation — AC2 + AC3 (5 tests)
# ===================================================================

class TestBatchEvaluation:
    def test_matching_theme_included_ac2(self):
        """AC2 — insight matching batch theme → batch_included."""
        evaluator = BatchEvaluator(MockCCFBatch(keywords=["transformation"]))
        report = _make_report(num_insights=3)
        pieces = MicroContentExtractor().extract(report, COACH_ID, COACH_ACRONYM)
        evaluated = evaluator.evaluate(pieces, COACH_ID)
        included = [p for p in evaluated if p.batch_included]
        assert len(included) > 0

    def test_non_matching_queued_ac3(self):
        """AC3 — insight not matching → session_content_queue."""
        evaluator = BatchEvaluator(MockCCFBatch(keywords=["astrophysics"]))
        report = _make_report(num_insights=3)
        pieces = MicroContentExtractor().extract(report, COACH_ID, COACH_ACRONYM)
        evaluated = evaluator.evaluate(pieces, COACH_ID)
        queued = [p for p in evaluated if p.queue_status == QueueStatus.session_content_queue]
        assert len(queued) == len(pieces)

    def test_boredom_ban_overrides(self):
        evaluator = BatchEvaluator(MockCCFBatch(
            keywords=["transformation"],
            boredom=["transformation"],
        ))
        report = _make_report(num_insights=2)
        pieces = MicroContentExtractor().extract(report, COACH_ID, COACH_ACRONYM)
        evaluated = evaluator.evaluate(pieces, COACH_ID)
        included = [p for p in evaluated if p.batch_included]
        assert len(included) == 0  # boredom ban wins

    def test_no_batch_context_all_queued(self):
        evaluator = BatchEvaluator(ccf_batch=None)
        pieces = [SessionContentPiece(
            asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
            text="Some text",
        )]
        result = evaluator.evaluate(pieces, COACH_ID)
        assert all(not p.batch_included for p in result)

    def test_mixed_batch_and_queue(self):
        evaluator = BatchEvaluator(MockCCFBatch(keywords=["growth"]))
        pieces = [
            SessionContentPiece(
                asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
                text="Content about growth and learning",
            ),
            SessionContentPiece(
                asset_id="A-2", content_type=SessionContentType.telegram_insight_card,
                text="Something about astrophysics",
            ),
        ]
        evaluated = evaluator.evaluate(pieces, COACH_ID)
        assert evaluated[0].batch_included
        assert not evaluated[1].batch_included


# ===================================================================
# 4. Triple-Pass Validation — AC4 (4 tests)
# ===================================================================

class TestTriplePassValidation:
    def test_all_validated_ac4(self):
        """AC4 — all content passes validation before delivery."""
        validator = TriplePassValidator(MockVoiceDNA(0.05))
        pieces = [
            SessionContentPiece(
                asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
                text="A meaningful insight about coaching transformation",
            ),
        ]
        result = validator.validate(pieces, COACH_ID)
        assert result[0].validation_status == ValidationStatus.passed

    def test_high_drift_fails(self):
        validator = TriplePassValidator(MockVoiceDNA(0.25))
        pieces = [
            SessionContentPiece(
                asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
                text="Some text that drifts from voice DNA",
            ),
        ]
        result = validator.validate(pieces, COACH_ID)
        assert result[0].validation_status == ValidationStatus.failed

    def test_short_text_fails(self):
        validator = TriplePassValidator(MockVoiceDNA(0.05))
        pieces = [
            SessionContentPiece(
                asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
                text="Short",
            ),
        ]
        result = validator.validate(pieces, COACH_ID)
        assert result[0].validation_status == ValidationStatus.failed

    def test_fingerprint_assigned_on_pass(self):
        validator = TriplePassValidator(MockVoiceDNA(0.05))
        pieces = [
            SessionContentPiece(
                asset_id="A-1", content_type=SessionContentType.telegram_insight_card,
                text="A meaningful insight about genuine transformation",
            ),
        ]
        result = validator.validate(pieces, COACH_ID)
        assert result[0].fingerprint_id is not None
        assert "SESSION" in result[0].fingerprint_id


# ===================================================================
# 5. Fingerprint traceability — AC5 (2 tests)
# ===================================================================

class TestFingerprintTraceability:
    def test_source_type_session_ac5(self):
        """AC5 — source_type = SESSION in all content pieces."""
        pipe, _, _, _ = _pipeline()
        report = _make_report()
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        for piece in result.output.content_pieces:
            assert piece.source_type == "SESSION"

    def test_fingerprint_on_passed_pieces(self):
        pipe, _, _, _ = _pipeline()
        report = _make_report()
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        passed = [p for p in result.output.content_pieces if p.validation_status == ValidationStatus.passed]
        for p in passed:
            assert p.fingerprint_id is not None


# ===================================================================
# 6. Non-interference — AC6 (2 tests)
# ===================================================================

class TestNonInterference:
    def test_pipeline_is_additive_ac6(self):
        """AC6 — pipeline produces output without side effects on CCF."""
        pipe, sync, _, _ = _pipeline()
        report = _make_report()
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        assert result.success
        # AFFiNE push is to content_calendar, not to CCF batch
        if sync.pushes:
            assert sync.pushes[0]["section"] == "content_calendar"

    def test_no_sync_still_succeeds(self):
        pipe, _, _, _ = _pipeline(with_sync=False)
        report = _make_report()
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        assert result.success


# ===================================================================
# 7. Full pipeline (5 tests)
# ===================================================================

class TestFullPipeline:
    def test_success(self):
        pipe, _, _, _ = _pipeline(keywords=["transformation"])
        report = _make_report()
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        assert result.success
        assert result.output is not None
        assert result.output.total_extracted >= 5

    def test_batch_counts(self):
        pipe, _, _, _ = _pipeline(keywords=["transformation"])
        report = _make_report()
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        out = result.output
        assert out.batch_included_count + out.queued_count == out.total_extracted

    def test_affine_push(self):
        pipe, sync, _, _ = _pipeline()
        report = _make_report()
        _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        assert len(sync.pushes) >= 1
        assert sync.pushes[0]["metadata"]["source_type"] == "SESSION"

    def test_session_id_in_output(self):
        pipe, _, _, _ = _pipeline()
        report = _make_report()
        report["session_id"] = "test-session-abc"
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        assert result.output.session_id == "test-session-abc"

    def test_low_density_still_succeeds(self):
        pipe, _, _, _ = _pipeline()
        report = _make_report(num_insights=1, num_breakthroughs=0, num_beats=0)
        result = _run(pipe.process_session(report, COACH_ID, COACH_ACRONYM))
        assert result.success
        assert result.output.total_extracted == 1


# ===================================================================
# 8. Constants & SQL (3 tests)
# ===================================================================

class TestConstants:
    def test_agent_names(self):
        assert AGENT_JULIO == "Julio"
        assert AGENT_CESARE == "Cesare"
        assert AGENT_SOPHIA == "Sophia"
        assert AGENT_MARCUS == "Marcus"
        assert AGENT_CHEN == "Chen"

    def test_pipeline_session(self):
        assert PIPELINE_SESSION == "SESSION"

    def test_sql_schema(self):
        assert "session_content" in SESSION_CONTENT_SQL
        assert "fingerprint_id" in SESSION_CONTENT_SQL
        assert "source_type" in SESSION_CONTENT_SQL
