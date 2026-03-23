"""
CCP Sacred Audio Data Models — FR2 Unit 1
ThoughtUnit, AuthenticityScore, SacredAudioSession, ExtractionReadiness

Spec reference: FR2 Tech Spec
  §Stage C — ThoughtUnit schema (unit_id, text, word_count, whisper_timestamps)
  §Stage D — 7-Factor LIWC-22 Authenticity Gate (7 markers, status enum)
  §Stage E — Storage targets (extraction_readiness.authenticated_word_count)
  §Dependencies — coach_soul.json schema v4.0

Architecture reference: CCP_Technical_Architecture.md §3.1 (Supabase Schemas)
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────────────────────
# Thought Unit Schema
# Spec: §Stage C — "Output: array of Thought_Units, each with:
# unit_id, text, word_count, whisper_timestamps"
# ──────────────────────────────────────────────────────────────

class ThoughtUnit(BaseModel):
    """A single logic-bounded segment of coach speech.

    Spec: 'A Thought_Unit is a complete logical move:
    [claim → mechanism → emotional assertion].'
    """

    unit_id: str = Field(
        ...,
        description="Unique identifier for this thought unit within the session",
    )
    text: str = Field(
        ...,
        min_length=1,
        description="Full text content of the thought unit",
    )
    word_count: int = Field(
        ...,
        ge=0,
        description="Word count of this unit (must be ≥30 after merge)",
    )
    whisper_timestamps: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Word-level timestamps from Whisper for boundary detection",
    )
    hard_boundary: bool = Field(
        default=False,
        description=(
            "True if this unit was force-segmented at the 300-word mark "
            "(long continuous stream >500 words without root return). "
            "Spec: §Stage C Edge cases"
        ),
    )
    multilingual_flag: bool = Field(
        default=False,
        description=(
            "True if multilingual code-switching detected. "
            "Spec: 'flag for manual review — do not segment cross-language units'"
        ),
    )

    @field_validator("word_count", mode="before")
    @classmethod
    def validate_word_count(cls, v: int, info: Any) -> int:
        """Auto-compute word count from text if not provided or zero."""
        if v == 0 and info.data.get("text"):
            return len(info.data["text"].split())
        return v


# ──────────────────────────────────────────────────────────────
# Authenticity Status Enum
# Spec: §Stage D Gate Logic — "unit.status = 'AUTHENTIC'" or
# "unit.status = 'SYNTHETIC_CANDIDATE'"
# ──────────────────────────────────────────────────────────────

class AuthenticityStatus(str, Enum):
    """Status of a thought unit after LIWC-22 scoring."""
    AUTHENTIC = "AUTHENTIC"
    SYNTHETIC_CANDIDATE = "SYNTHETIC_CANDIDATE"
    DROPPED = "DROPPED"  # After persistent gate failure (≥2 re-elicitation attempts)


# ──────────────────────────────────────────────────────────────
# Session Status Enum
# Spec: §Stage D — "session is marked INSUFFICIENT"
# §Stage E — "Session contains ≥3 AUTHENTIC Thought_Units"
# ──────────────────────────────────────────────────────────────

class SessionStatus(str, Enum):
    """Status of a Sacred Audio session."""
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    INSUFFICIENT = "INSUFFICIENT"  # <3 AUTHENTIC units after all attempts


# ──────────────────────────────────────────────────────────────
# 7-Factor LIWC-22 Authenticity Markers
# Spec: §Stage D — The 7 Authenticity Markers table
# ──────────────────────────────────────────────────────────────

class AuthenticityMarker(str, Enum):
    """The 7 LIWC-22 authenticity markers from FR2 spec."""
    FIRST_PERSON_SINGULAR = "first_person_singular"
    EXCLUSIVE_WORDS = "exclusive_words"
    ABSENCE_OF_HEDGING = "absence_of_hedging"
    SENTENCE_COMPRESSION = "sentence_compression"
    VERB_TENSE_DISTRIBUTION = "verb_tense_distribution"
    FILLER_FREQUENCY = "filler_frequency"
    DISCOURSE_MARKER_POSITION = "discourse_marker_position"


class MarkerResult(BaseModel):
    """Result of evaluating a single LIWC-22 marker on a ThoughtUnit."""

    marker: AuthenticityMarker = Field(..., description="Which of the 7 markers")
    in_range: bool = Field(..., description="Whether the marker value falls within the authentic range")
    value: float = Field(..., description="Computed metric value for this marker")
    threshold_low: float = Field(
        default=0.0,
        description="Lower bound of the authentic range (adjusted by authentic_multiplier)",
    )
    threshold_high: float = Field(
        default=1.0,
        description="Upper bound of the authentic range",
    )
    detail: str = Field(
        default="",
        description="Human-readable explanation of the scoring",
    )


class AuthenticityScore(BaseModel):
    """Complete LIWC-22 authenticity scoring result for a ThoughtUnit.

    Spec: 'Score = count of markers in-range / 7.
    Minimum passing score: ≥7/10 (i.e., all 7 markers must be within
    authentic range — the ≥7/10 means the composite indicator, not a ratio).'
    """

    unit_id: str = Field(..., description="ThoughtUnit this score belongs to")
    marker_results: list[MarkerResult] = Field(
        ...,
        min_length=7,
        max_length=7,
        description="Results for all 7 markers",
    )
    pass_count: int = Field(
        default=0,
        description="Count of markers that are in-range",
    )
    status: AuthenticityStatus = Field(
        default=AuthenticityStatus.SYNTHETIC_CANDIDATE,
        description="AUTHENTIC if all 7 pass, SYNTHETIC_CANDIDATE otherwise",
    )
    failed_markers: list[AuthenticityMarker] = Field(
        default_factory=list,
        description="List of markers that failed (for re-elicitation targeting)",
    )
    authentic_multiplier: float = Field(
        default=1.0,
        description=(
            "Per-coach calibration from genesis_certificate.authentic_multiplier. "
            "Stress test Q32: adjusts per-marker thresholds for stoic coaches."
        ),
    )
    re_elicitation_attempts: int = Field(
        default=0,
        description="Number of re-elicitation attempts on this unit",
    )

    def model_post_init(self, __context: Any) -> None:
        """Compute pass_count, status, and failed_markers from marker_results."""
        self.pass_count = sum(1 for m in self.marker_results if m.in_range)
        self.failed_markers = [
            m.marker for m in self.marker_results if not m.in_range
        ]
        # Spec: all 7 markers must be within authentic range
        if self.pass_count == 7:
            self.status = AuthenticityStatus.AUTHENTIC
        else:
            self.status = AuthenticityStatus.SYNTHETIC_CANDIDATE


# ──────────────────────────────────────────────────────────────
# Scored Thought Unit (ThoughtUnit + score combined)
# ──────────────────────────────────────────────────────────────

class ScoredThoughtUnit(BaseModel):
    """A ThoughtUnit with its authenticity score attached."""

    unit: ThoughtUnit
    score: AuthenticityScore
    status: AuthenticityStatus = Field(
        default=AuthenticityStatus.SYNTHETIC_CANDIDATE,
    )

    def model_post_init(self, __context: Any) -> None:
        """Sync status from score."""
        self.status = self.score.status


# ──────────────────────────────────────────────────────────────
# Sacred Audio Session
# Spec: §Stage E — session metadata (session_id, date, unit_count,
# authenticity_scores)
# ──────────────────────────────────────────────────────────────

class SacredAudioSession(BaseModel):
    """A complete Sacred Audio ingestion session.

    Tracks the full pipeline from ingestion through storage.
    """

    session_id: str = Field(
        ...,
        description="Unique session identifier",
    )
    coach_id: str = Field(..., description="Coach identifier")
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        description="Session date (ISO date)",
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Session start timestamp (ISO 8601)",
    )
    status: SessionStatus = Field(
        default=SessionStatus.PROCESSING,
        description="Current session status",
    )

    # Stage A outputs
    audio_format: str = Field(default="", description="File format (.ogg, .mp3, .m4a)")
    audio_duration_seconds: float = Field(default=0.0, description="Audio duration in seconds")
    audio_hash: str = Field(default="", description="SHA-256 hash of raw audio bytes")

    # Stage B outputs
    raw_transcript: str = Field(default="", description="Full Groq Whisper transcript (non-verbals preserved)")
    transcription_model: str = Field(default="", description="Model used (groq-whisper or gemini-flash)")

    # Stage C outputs
    thought_units: list[ThoughtUnit] = Field(
        default_factory=list,
        description="Segmented thought units from Stage C",
    )

    # Stage D outputs
    scored_units: list[ScoredThoughtUnit] = Field(
        default_factory=list,
        description="Thought units with authenticity scores from Stage D",
    )
    authentic_units: list[ScoredThoughtUnit] = Field(
        default_factory=list,
        description="Only AUTHENTIC units (for Stage E storage)",
    )
    synthetic_candidates: list[ScoredThoughtUnit] = Field(
        default_factory=list,
        description="SYNTHETIC_CANDIDATE units awaiting re-elicitation",
    )
    dropped_units: list[ScoredThoughtUnit] = Field(
        default_factory=list,
        description="Permanently dropped units (persistent gate failure)",
    )

    # Stage E outputs
    authenticated_word_count: int = Field(
        default=0,
        description="Total word count of AUTHENTIC units in this session",
    )

    # Receipt chain tracking
    receipt_ids: dict[str, str] = Field(
        default_factory=dict,
        description="Map of stage_name → receipt_id for chain integrity verification",
    )

    def total_authentic_units(self) -> int:
        """Count of AUTHENTIC units in this session."""
        return len(self.authentic_units)

    def passes_sufficiency_gate(self) -> bool:
        """Spec: 'a session with ≥3 AUTHENTIC units proceeds to Stage E'."""
        return self.total_authentic_units() >= 3


# ──────────────────────────────────────────────────────────────
# Extraction Readiness Tracker
# Spec: §Stage E — "Word count is tracked in coach_soul.json →
# extraction_readiness.authenticated_word_count"
# "When count crosses 3,000: system notifies Morgan"
# ──────────────────────────────────────────────────────────────

MINIMUM_CORPUS_WORDS: int = 3000
"""Spec: 'Minimum of 3,000 validated words (Post-LIWC-22 gate) across
all sessions before FR3 pipeline can be triggered'."""


class ExtractionReadiness(BaseModel):
    """Tracks accumulated authenticated word count across sessions.

    Stored in coach_soul.json → extraction_readiness field.
    """

    authenticated_word_count: int = Field(
        default=0,
        description="Running total of validated words across all sessions",
    )
    session_count: int = Field(
        default=0,
        description="Number of completed Sacred Audio sessions",
    )
    sessions: list[str] = Field(
        default_factory=list,
        description="List of session_ids that contributed to the word count",
    )
    fr3_ready: bool = Field(
        default=False,
        description="True when authenticated_word_count ≥ 3,000",
    )
    fr3_notification_sent: bool = Field(
        default=False,
        description="True after Morgan has been notified of FR3 readiness",
    )

    def add_session(self, session_id: str, word_count: int) -> bool:
        """Add a session's word count. Returns True if FR3 threshold is newly crossed.

        Spec: 'When count crosses 3,000: system notifies Morgan (Setup Orchestrator)
        to initiate FR3.'
        """
        self.authenticated_word_count += word_count
        self.session_count += 1
        self.sessions.append(session_id)

        was_ready = self.fr3_ready
        self.fr3_ready = self.authenticated_word_count >= MINIMUM_CORPUS_WORDS

        # Return True only on the transition from not-ready to ready
        return self.fr3_ready and not was_ready
