"""FR-CA11-08 — Live Coaching → Content Machine Pipeline.

Bridges Session Intelligence (FR-CA11-05) with the CCF Expression
Department.  After Lena produces a Session Intelligence Report, this
pipeline routes insights to Julio (micro-content) and Cesare (batch
evaluation), then through Triple-Pass Validation before delivery.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    ContentMachineArray,
    ContentMachineResult,
    QueueStatus,
    SessionContentPiece,
    SessionContentType,
    ValidationStatus,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_JULIO = "Julio"
AGENT_CESARE = "Cesare"
AGENT_SOPHIA = "Sophia"
AGENT_MARCUS = "Marcus"
AGENT_CHEN = "Chen"
PIPELINE_SESSION = "SESSION"
MIN_EXTRACTION_PIECES = 3
EMOTIONAL_INTENSITY_VIDEO_THRESHOLD = 0.7
TTT_DRIFT_MAX = 0.15
AI_DETECTION_MAX = 0.05

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

SESSION_CONTENT_SQL = """
CREATE TABLE IF NOT EXISTS session_content (
    asset_id            TEXT PRIMARY KEY,
    session_id          TEXT NOT NULL,
    content_type        TEXT NOT NULL,
    text                TEXT NOT NULL,
    validation_status   TEXT NOT NULL DEFAULT 'PENDING',
    fingerprint_id      TEXT,
    source_type         TEXT NOT NULL DEFAULT 'SESSION',
    batch_included      BOOLEAN NOT NULL DEFAULT FALSE,
    queue_status        TEXT NOT NULL DEFAULT 'session_content_queue',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class VoiceDNAProtocol(Protocol):
    def compute_ttt_drift(self, text: str, coach_id: str) -> float: ...


class AFFiNESyncProtocol(Protocol):
    async def push_content(self, coach_id: str, section: str,
                           title: str, body: str, *,
                           metadata: dict[str, Any] | None = None) -> str: ...


class CCFBatchProtocol(Protocol):
    def get_current_batch_theme(self, coach_id: str) -> dict[str, Any]: ...
    def get_boredom_ban_window(self, coach_id: str) -> list[str]: ...


# ---------------------------------------------------------------------------
# Stage 1 — Julio: Micro-Content Extraction
# ---------------------------------------------------------------------------


class MicroContentExtractor:
    """``Julio`` — extracts 5-8 micro-content pieces from session insights."""

    def extract(
        self,
        session_report: dict[str, Any],
        coach_id: str,
        coach_acronym: str = "CCH",
    ) -> list[SessionContentPiece]:
        pieces: list[SessionContentPiece] = []
        insights = session_report.get("key_insights", [])
        breakthroughs = session_report.get("breakthrough_moments", [])
        emotional_beats = session_report.get("emotional_beats", [])

        # Telegram insight cards — one per insight
        for i, insight in enumerate(insights):
            text = insight if isinstance(insight, str) else insight.get("text", str(insight))
            pieces.append(SessionContentPiece(
                asset_id=self._mint_asset_id(coach_acronym, "CARD", i),
                content_type=SessionContentType.telegram_insight_card,
                text=text,
                source_insight_timestamp=self._get_timestamp(insight),
            ))

        # Instagram caption drafts — one per breakthrough
        for i, bt in enumerate(breakthroughs):
            text = bt if isinstance(bt, str) else bt.get("description", str(bt))
            caption = self._build_caption(text)
            pieces.append(SessionContentPiece(
                asset_id=self._mint_asset_id(coach_acronym, "CAPTION", i),
                content_type=SessionContentType.instagram_caption,
                text=caption,
            ))

        # Short-form video script candidates — high-intensity beats
        for i, beat in enumerate(emotional_beats):
            intensity = beat.get("intensity", 0) if isinstance(beat, dict) else 0
            if intensity > EMOTIONAL_INTENSITY_VIDEO_THRESHOLD:
                text = beat.get("description", str(beat)) if isinstance(beat, dict) else str(beat)
                pieces.append(SessionContentPiece(
                    asset_id=self._mint_asset_id(coach_acronym, "VIDEO", i),
                    content_type=SessionContentType.short_form_video_script,
                    text=f"[VIDEO SCRIPT] {text}",
                    source_insight_timestamp=beat.get("timestamp") if isinstance(beat, dict) else None,
                ))

        return pieces

    @staticmethod
    def _mint_asset_id(acronym: str, suffix: str, idx: int) -> str:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        uid = uuid.uuid4().hex[:6]
        return f"{acronym}-SESSION-{date_str}-{uid}-{suffix}"

    @staticmethod
    def _get_timestamp(insight: Any) -> Optional[str]:
        if isinstance(insight, dict):
            return insight.get("timestamp")
        return None

    @staticmethod
    def _build_caption(text: str) -> str:
        if len(text) < 150:
            return f"{text}\n\n#coaching #transformation #growth"
        return text[:300]


# ---------------------------------------------------------------------------
# Stage 2 — Cesare: CCF Batch Evaluation
# ---------------------------------------------------------------------------


class BatchEvaluator:
    """``Cesare`` — evaluates session insights against the current CCF batch."""

    def __init__(self, ccf_batch: CCFBatchProtocol | None = None) -> None:
        self._ccf_batch = ccf_batch

    def evaluate(
        self,
        pieces: list[SessionContentPiece],
        coach_id: str,
    ) -> list[SessionContentPiece]:
        if not self._ccf_batch:
            return pieces  # no batch context → all go to queue

        theme = self._ccf_batch.get_current_batch_theme(coach_id)
        boredom_window = set(self._ccf_batch.get_boredom_ban_window(coach_id))
        batch_keywords = set(theme.get("keywords", []))

        for piece in pieces:
            text_lower = piece.text.lower()
            # Check boredom ban — semantic overlap
            if any(banned.lower() in text_lower for banned in boredom_window):
                piece.queue_status = QueueStatus.session_content_queue
                piece.batch_included = False
                continue
            # Check theme alignment
            if batch_keywords and any(kw.lower() in text_lower for kw in batch_keywords):
                piece.batch_included = True
                piece.queue_status = QueueStatus.batch_included
            else:
                piece.queue_status = QueueStatus.session_content_queue
                piece.batch_included = False

        return pieces


# ---------------------------------------------------------------------------
# Stage 3 — Triple-Pass Validation (Sophia / Marcus / Chen)
# ---------------------------------------------------------------------------


class TriplePassValidator:
    """Simulates Sophia/Marcus/Chen validation gate."""

    def __init__(self, voice_dna: VoiceDNAProtocol | None = None) -> None:
        self._voice_dna = voice_dna

    def validate(
        self,
        pieces: list[SessionContentPiece],
        coach_id: str,
    ) -> list[SessionContentPiece]:
        for piece in pieces:
            # TTT drift check
            drift = self._check_ttt_drift(piece.text, coach_id)
            if drift > TTT_DRIFT_MAX:
                piece.validation_status = ValidationStatus.failed
                continue
            # Structural compliance (minimum text length)
            if len(piece.text.strip()) < 10:
                piece.validation_status = ValidationStatus.failed
                continue
            piece.validation_status = ValidationStatus.passed
            piece.fingerprint_id = self._mint_fingerprint(coach_id, piece)

        return pieces

    def _check_ttt_drift(self, text: str, coach_id: str) -> float:
        if self._voice_dna:
            return self._voice_dna.compute_ttt_drift(text, coach_id)
        return 0.0

    @staticmethod
    def _mint_fingerprint(coach_id: str, piece: SessionContentPiece) -> str:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        uid = uuid.uuid4().hex[:6]
        return f"SKILL-SESSION-{coach_id[:4].upper()}-{date_str}-{uid}"


# ---------------------------------------------------------------------------
# Orchestrator — ContentMachinePipeline
# ---------------------------------------------------------------------------


class ContentMachinePipeline:
    """End-to-end: Session Intelligence Report → validated micro-content."""

    def __init__(
        self,
        affine_sync: AFFiNESyncProtocol | None = None,
        ccf_batch: CCFBatchProtocol | None = None,
        voice_dna: VoiceDNAProtocol | None = None,
    ) -> None:
        self._extractor = MicroContentExtractor()
        self._evaluator = BatchEvaluator(ccf_batch)
        self._validator = TriplePassValidator(voice_dna)
        self._affine_sync = affine_sync

    async def process_session(
        self,
        session_report: dict[str, Any],
        coach_id: str,
        coach_acronym: str = "CCH",
    ) -> ContentMachineResult:
        session_id = session_report.get("session_id", str(uuid.uuid4()))

        # Stage 1: Julio extraction
        pieces = self._extractor.extract(session_report, coach_id, coach_acronym)
        if len(pieces) < MIN_EXTRACTION_PIECES:
            # Low content density — not an error, just metadata
            pass

        # Stage 2: Cesare batch evaluation
        pieces = self._evaluator.evaluate(pieces, coach_id)

        # Stage 3: Triple-Pass Validation
        pieces = self._validator.validate(pieces, coach_id)

        # Filter to validated only for delivery
        passed_pieces = [p for p in pieces if p.validation_status == ValidationStatus.passed]

        # Deliver to AFFiNE
        if self._affine_sync and passed_pieces:
            try:
                body = self._format_content_calendar(passed_pieces)
                await self._affine_sync.push_content(
                    coach_id,
                    "content_calendar",
                    f"Session Content — {session_id[:8]}",
                    body,
                    metadata={"session_id": session_id, "source_type": PIPELINE_SESSION},
                )
            except Exception:
                pass  # non-blocking

        batch_count = sum(1 for p in pieces if p.batch_included)
        output = ContentMachineArray(
            session_id=session_id,
            content_pieces=pieces,
            total_extracted=len(pieces),
            batch_included_count=batch_count,
            queued_count=len(pieces) - batch_count,
        )

        return ContentMachineResult(success=True, output=output)

    @staticmethod
    def _format_content_calendar(pieces: list[SessionContentPiece]) -> str:
        lines = ["# Session-Derived Content\n"]
        for p in pieces:
            lines.append(f"## [{p.content_type.value}] {p.asset_id}")
            lines.append(p.text)
            lines.append("")
        return "\n".join(lines)
