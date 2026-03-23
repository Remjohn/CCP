"""
CCP Step 11 — Scheduled Monitor Agent Models (FR15)

Pydantic v2 models for the FR15 Scheduled Monitor Agent.

FR15 implements the autonomous daily cultural tension monitor that proactively
messages the coach via Telegram, shifting the CCP from reactive to proactive.

Architecture reference:
    FR15_Scheduled_Monitor_Agent_Tech_Spec.md
    CCP_Architecture_V5.0 §10.1 — Scheduled Production Flow
    CRAL_Documentation_V1 §Integration Point 1

Models defined:
    MonitorVerdict — Stage 2 assessment gate outcomes
    TensionObservation — Extracted cultural tension with frequency delta
    TelegramPromptPayload — The rigid 3-part structured message
    CoachResponse — Coach's reply to the proactive prompt
    CoachDeclineReason — Opt-out classification
    SessionInitiationResult — Stage 4 routing outcome (DEP-ENG-005 or abort)
    MonitorAbortLog — Silent abort log for Stage 2 FAIL / coach decline
    MonitorRunResult — Full run container for one daily cycle

Critical constraints:
    - FR15 §Stage 2: >15% frequency spike → PASS; 10-15% → PROVISIONAL; <10% → FAIL silent abort.
    - FR15 §Stage 3: 3-part prompt structure: Observation, Practitioner Summaries, Question.
    - FR15 §Stage 4: Coach decline OR < 15 words → session_aborted_by_coach.
    - FR15 §Stage 4: Timeout = 12 hours.
    - ADR-01: coach_id scopes all operations — no cross-tenant scraping.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Constants ────────────────────────────────────────────────────────────────

NOVELTY_SPIKE_PASS_THRESHOLD: float = 15.0
"""FR15 §Stage 2 PASS threshold: >15% frequency spike vs DEP-ENG-023 baseline."""

NOVELTY_SPIKE_PROVISIONAL_MIN: float = 10.0
"""FR15 §Stage 2 PROVISIONAL lower bound: 10-15% spike."""

MINIMUM_COACH_RESPONSE_WORDS: int = 15
"""FR15 §Stage 4: Coach response must be >= 15 words to be treated as valid."""

COACH_RESPONSE_TIMEOUT_HOURS: int = 12
"""FR15 §Stage 4: Await coach reply. Timeout after 12 hours."""

PRACTITIONER_SUMMARY_COUNT: int = 3
"""FR15 §Stage 3: 'Three practitioners/users I tracked are taking these positions.'"""


# ─── Enumerations ─────────────────────────────────────────────────────────────

class MonitorVerdict(str, Enum):
    """FR15 §Stage 2 Logic Gate verdict.

    PASS: >15% frequency spike → novel tension → proceed to Stage 3.
    PROVISIONAL: 10-15% spike → weak signal → proceed with weak_signal flag.
    FAIL: No novel tension → silent_abort, do not message coach.
    """
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class CoachDeclineReason(str, Enum):
    """Classification of coach opt-out responses.

    FR15 §Stage 4: 'Not today', 'No', 'I'm travelling today' → OPT_OUT.
    Short response < 15 words → INSUFFICIENT_CONTENT.
    Timeout → TIMEOUT.
    """
    OPT_OUT = "OPT_OUT"
    INSUFFICIENT_CONTENT = "INSUFFICIENT_CONTENT"
    TIMEOUT = "TIMEOUT"


class SessionInitiationType(str, Enum):
    """FR15 §Stage 4: Whether the session was proactively initiated.

    Matches DEP-ENG-005 extension field `initiation_type`.
    """
    SYSTEM_PROACTIVE = "system_proactive"
    USER_REACTIVE_FALLBACK = "user_reactive_fallback"


class MonitorRunStatus(str, Enum):
    """Overall status of a full daily monitor cycle."""
    COMPLETED_TENSION_FOUND = "COMPLETED_TENSION_FOUND"
    COMPLETED_WEAK_SIGNAL = "COMPLETED_WEAK_SIGNAL"
    ABORTED_NO_TENSION = "ABORTED_NO_TENSION"
    ABORTED_COACH_DECLINED = "ABORTED_COACH_DECLINED"
    ABORTED_SCRAPING_FAILURE = "ABORTED_SCRAPING_FAILURE"
    SESSION_INITIATED = "SESSION_INITIATED"


# ─── Tension Observation ──────────────────────────────────────────────────────

class PractitionerPosition(BaseModel):
    """A single practitioner/user position on the cultural tension.

    FR15 §Stage 3: 'Three practitioners/users I tracked are taking these positions.'
    """
    practitioner_handle: str = Field(
        ...,
        description="Community handle or anonymized identifier (e.g., '@BuilderDev').",
    )
    platform: str = Field(
        ...,
        description="Source platform (e.g., 'HustleCulture subreddit', 'TikTok').",
    )
    position_summary: str = Field(
        ...,
        description="1-2 sentence summary of this practitioner's stance on the tension.",
    )


class TensionObservation(BaseModel):
    """Extracted cultural tension from Stage 2 discourse analysis.

    FR15 §Stage 2: The result of detecting a >15% frequency spike
    in the coach's community vs DEP-ENG-023 baseline.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation — 3-char coach acronym.",
    )
    identified_tension: str = Field(
        ...,
        description="Human-readable description of the cultural tension detected.",
    )
    source_domain: str = Field(
        ...,
        description="Primary platform/community where the tension was observed.",
    )
    frequency_delta_percent: float = Field(
        ...,
        description="Percentage spike vs DEP-ENG-023 historical baseline.",
    )
    is_weak_signal: bool = Field(
        default=False,
        description="True if frequency_delta is in PROVISIONAL range (10-15%).",
    )
    novelty_verdict: MonitorVerdict = Field(
        default=MonitorVerdict.FAIL,
        description="Stage 2 gate verdict for this tension.",
    )
    practitioner_positions: list[PractitionerPosition] = Field(
        default_factory=list,
        description="3 practitioner positions for Stage 3 prompt.",
    )
    source_urls: list[str] = Field(
        default_factory=list,
        description="Source URLs for audit trail.",
    )
    observed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 timestamp of observation.",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive novelty_verdict and is_weak_signal from frequency_delta."""
        if self.frequency_delta_percent > NOVELTY_SPIKE_PASS_THRESHOLD:
            self.novelty_verdict = MonitorVerdict.PASS
            self.is_weak_signal = False
        elif self.frequency_delta_percent >= NOVELTY_SPIKE_PROVISIONAL_MIN:
            self.novelty_verdict = MonitorVerdict.PROVISIONAL
            self.is_weak_signal = True
        else:
            self.novelty_verdict = MonitorVerdict.FAIL
            self.is_weak_signal = False


# ─── Telegram Prompt ──────────────────────────────────────────────────────────

class TelegramPromptPayload(BaseModel):
    """The rigidly structured 3-part Telegram message.

    FR15 §Stage 3: Strict 3-part structure mandatory:
      Part 1: 'I am seeing a lot of conversation in your community about [tension].'
      Part 2: 'Three practitioners/users I tracked are taking these positions: [Summary].'
      Part 3: 'Does this connect to something you have been thinking about for your audience?'

    FR15 AC2: The exact phrased structure must be present — not a generic question.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    part_1_observation: str = Field(
        ...,
        description="'I am seeing a lot of conversation in your community about [tension].'",
    )
    part_2_practitioner_summaries: str = Field(
        ...,
        description="'Three practitioners/users I tracked are taking these positions: [...]'",
    )
    part_3_closing_question: str = Field(
        ...,
        description="'Does this connect to something you have been thinking about for your audience?'",
    )
    is_weak_signal: bool = Field(
        default=False,
        description="If True, phrasing reflects provisional/weak signal.",
    )
    full_message: str = Field(
        default="",
        description="Auto-assembled full message text.",
    )
    source_tension: Optional[TensionObservation] = Field(
        default=None,
        description="The tension observation that triggered this prompt.",
    )
    sent_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    def model_post_init(self, __context: Any) -> None:
        """Auto-assemble the full_message from the 3 parts."""
        self.full_message = (
            f"{self.part_1_observation}\n\n"
            f"{self.part_2_practitioner_summaries}\n\n"
            f"{self.part_3_closing_question}"
        )

    def has_required_structure(self) -> bool:
        """FR15 AC2: Validate that all 3 structural parts are non-empty.

        Each part must:
        - Part 1: mention 'community' or 'conversation'
        - Part 2: mention 'practitioner' or 'position' or 'tracked'
        - Part 3: end with '?'
        """
        p1_ok = bool(self.part_1_observation.strip()) and any(
            kw in self.part_1_observation.lower()
            for kw in ("community", "conversation", "seeing")
        )
        p2_ok = bool(self.part_2_practitioner_summaries.strip()) and any(
            kw in self.part_2_practitioner_summaries.lower()
            for kw in ("practitioner", "position", "tracked", "user")
        )
        p3_ok = bool(self.part_3_closing_question.strip()) and (
            "?" in self.part_3_closing_question
        )
        return p1_ok and p2_ok and p3_ok


# ─── Coach Response ───────────────────────────────────────────────────────────

# Decline phrases as per FR15 spec
DECLINE_PHRASES: frozenset[str] = frozenset({
    "no", "not today", "not now", "i'm travelling", "i am travelling",
    "travelling today", "skip today", "pass", "not interested",
    "no thanks", "nope", "later", "busy today",
})


class CoachResponse(BaseModel):
    """Coach's reply to the Scheduled Monitor's proactive Telegram prompt.

    FR15 §Stage 4: Router evaluates word count and decline phrases.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    raw_text: str = Field(
        ...,
        description="Raw text of the coach's Telegram response.",
    )
    response_type: str = Field(
        default="text",
        description="'text' or 'voice_transcription'.",
    )
    received_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    word_count: int = Field(default=0)
    is_decline: bool = Field(
        default=False,
        description="True if response matches a decline phrase.",
    )
    decline_reason: Optional[CoachDeclineReason] = Field(default=None)

    def model_post_init(self, __context: Any) -> None:
        """Auto-evaluate decline status and word count."""
        self.word_count = len(self.raw_text.split())
        normalized = self.raw_text.strip().lower().rstrip(".!,")
        if normalized in DECLINE_PHRASES or any(
            phrase in normalized for phrase in DECLINE_PHRASES if len(phrase) > 4
        ):
            self.is_decline = True
            self.decline_reason = CoachDeclineReason.OPT_OUT
        elif self.word_count < MINIMUM_COACH_RESPONSE_WORDS:
            self.is_decline = True
            self.decline_reason = CoachDeclineReason.INSUFFICIENT_CONTENT


# ─── Session Initiation Result ────────────────────────────────────────────────

class SessionInitiationResult(BaseModel):
    """Result of Stage 4: Coach Response Ingestion.

    FR15 §Stage 4: If valid response → DEP-ENG-005 extension emitted.
    If decline → session_aborted_by_coach logged.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    session_aborted: bool = Field(
        default=False,
        description="True if coach declined or response was insufficient.",
    )
    abort_reason: Optional[CoachDeclineReason] = Field(default=None)
    initiation_type: SessionInitiationType = Field(
        default=SessionInitiationType.SYSTEM_PROACTIVE,
    )
    # DEP-ENG-005 extension fields (when session proceeds)
    trigger_id: str = Field(
        default="",
        description="Generated trigger ID for the DEP-ENG-005 output.",
    )
    identified_tension: str = Field(
        default="",
        description="The tension that seeded the session.",
    )
    source_domain: str = Field(default="")
    frequency_delta: str = Field(
        default="",
        description="Human-readable frequency spike string (e.g. '+22% spike 48h').",
    )
    coach_raw_response: str = Field(
        default="",
        description="Coach's raw text response.",
    )
    extracted_mechanism: str = Field(
        default="",
        description="Extracted mechanism keyword from the coach's response.",
    )
    authentication_status: str = Field(
        default="CONFIRMED_READY_FOR_M2",
        description="DEP-ENG-005 extension authentication_status.",
    )
    receipt_hash: str = Field(default="")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    cral_initiation_signal_emitted: bool = Field(
        default=False,
        description="True when CRAL Orchestrator was signalled to commence M2-M7.",
    )


# ─── Monitor Abort Log ────────────────────────────────────────────────────────

class MonitorAbortLog(BaseModel):
    """Silent abort log for Stage 2 FAIL or coach decline.

    FR15 §Stage 2: 'Abort the daily prompt. Do not message the coach.
    Write a silent_abort log.'
    FR15 §Stage 4: 'Log session_aborted_by_coach, terminate flow.'
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    abort_type: str = Field(
        ...,
        description="'silent_abort' (Stage 2 FAIL) or 'session_aborted_by_coach' (Stage 4).",
    )
    reason: str = Field(
        default="",
        description="Human-readable abort reason.",
    )
    frequency_delta_percent: Optional[float] = Field(
        default=None,
        description="Set for Stage 2 FAIL aborts.",
    )
    coach_response_text: Optional[str] = Field(
        default=None,
        description="Set for Stage 4 coach-declined aborts.",
    )
    decline_reason: Optional[CoachDeclineReason] = Field(default=None)
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    receipt_hash: str = Field(default="")


# ─── Full Run Result ──────────────────────────────────────────────────────────

class MonitorRunResult(BaseModel):
    """Full container for one complete daily scheduled monitor cycle.

    Holds the tension observation, prompt payload, and session initiation
    (or abort) result. Used for audit trail and receipt chain.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    run_status: MonitorRunStatus = Field(
        default=MonitorRunStatus.ABORTED_NO_TENSION,
    )
    tension_observation: Optional[TensionObservation] = Field(default=None)
    prompt_payload: Optional[TelegramPromptPayload] = Field(default=None)
    coach_response: Optional[CoachResponse] = Field(default=None)
    session_result: Optional[SessionInitiationResult] = Field(default=None)
    abort_log: Optional[MonitorAbortLog] = Field(default=None)
    run_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    scraping_source_urls: list[str] = Field(default_factory=list)
    adr01_verified: bool = Field(
        default=True,
        description="True when all scraped domains are within coach's tribe_soul scope.",
    )
    receipt_chain_hash: str = Field(default="")
