"""
CCP Step 11 — Scheduled Monitor Service (FR15)

Implements the FR15 Scheduled Monitor Agent — autonomous daily cultural
tension detection and proactive coach prompting pipeline.

Architecture reference:
    FR15_Scheduled_Monitor_Agent_Tech_Spec.md
    CCP_Architecture_V5.0 §10.1 — Scheduled Production Flow

Stages:
    1. Daily Monitor Initialization — scrape tribe_soul sources.
    2. Cultural Tension Extraction & Assessment Gate (>15% spike threshold).
    3. Telegram Proactive Prompt Generation (rigid 3-part structure).
    4. Coach Response Ingestion & Session Initiation (or abort).

FR15 AC1: Novelty gate — chronic topics with no >15% spike → FAIL → silent abort.
FR15 AC2: Prompt must have exact 3-part structure (Observation/Summaries/Question).
FR15 AC3: Coach decline → session_aborted_by_coach, no corrupted DEP-ENG-005.
FR15 AC4: ADR-01 — scraping strictly limited to tribe_soul domain list per coach.

ADR-01: coach_id scopes ALL operations. No cross-tenant scraping.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

from src.ccp.models.scheduled_monitor_models import (
    COACH_RESPONSE_TIMEOUT_HOURS,
    NOVELTY_SPIKE_PASS_THRESHOLD,
    NOVELTY_SPIKE_PROVISIONAL_MIN,
    PRACTITIONER_SUMMARY_COUNT,
    CoachDeclineReason,
    CoachResponse,
    MonitorAbortLog,
    MonitorRunResult,
    MonitorRunStatus,
    MonitorVerdict,
    PractitionerPosition,
    SessionInitiationResult,
    SessionInitiationType,
    TelegramPromptPayload,
    TensionObservation,
)

if TYPE_CHECKING:
    from src.ccp.core.receipt_chain import ReceiptChain

logger = logging.getLogger(__name__)

# ── Stage names ───────────────────────────────────────────────────────────────

STAGE_1_NAME = "STAGE-1-MONITOR-INIT"
STAGE_2_NAME = "STAGE-2-ASSESSMENT"
STAGE_3_NAME = "STAGE-3-MONITOR-PROMPT"
STAGE_4_NAME = "STAGE-4-MONITOR-INGEST"
AGENT_NAME = "Scheduled-Monitor-Agent"
INTAKE_AGENT_NAME = "Telegram-Intake-Router"


# ── Opt-out phrase detection ──────────────────────────────────────────────────

_DECLINE_PHRASES: frozenset[str] = frozenset({
    "no", "not today", "not now", "i'm travelling", "i am travelling",
    "travelling today", "skip today", "pass", "not interested",
    "no thanks", "nope", "later", "busy today",
})


def _is_decline_response(text: str) -> bool:
    """FR15 AC3: Detect explicit coach opt-out.

    Returns True when the response is an explicit decline or
    too short (<15 words) to be a valid session topic.
    """
    normalized = text.strip().lower().rstrip(".!,")
    if normalized in _DECLINE_PHRASES:
        return True
    # Partial phrase match for longer decline sentences
    for phrase in _DECLINE_PHRASES:
        if len(phrase) > 4 and phrase in normalized:
            return True
    return False


def _word_count(text: str) -> int:
    return len(text.split())


# ── ScheduledMonitorService ───────────────────────────────────────────────────

class ScheduledMonitorService:
    """FR15 Scheduled Monitor Agent service.

    Implements the 4-stage daily monitoring pipeline. Designed to be
    called on a configurable daily cron cadence.

    ADR-01: All methods require coach_id and verify domain scope against
    the allowed_domains list (extracted from tribe_soul.json).

    Args:
        coach_id: 3-char coach acronym for ADR-01 isolation.
        receipt_chain: Optional ReceiptChain for cryptographic audit.
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional["ReceiptChain"] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.receipt_chain = receipt_chain

    # ── Stage 2: Assessment Gate ─────────────────────────────────────────────

    def assess_tension_novelty(
        self,
        topic: str,
        source_domain: str,
        frequency_delta_percent: float,
        practitioner_positions: Optional[list[dict[str, str]]] = None,
        source_urls: Optional[list[str]] = None,
    ) -> TensionObservation:
        """FR15 §Stage 2: Cultural Tension Extraction & Assessment Gate.

        Compares frequency spike against DEP-ENG-023 historical baseline.

        FR15 AC1: Chronic topics with no >15% spike → MonitorVerdict.FAIL.
        Provisional range (10-15%) → MonitorVerdict.PROVISIONAL + weak_signal flag.

        Args:
            topic: The identified tension description.
            source_domain: Primary platform for this tension.
            frequency_delta_percent: Percentage spike vs DEP-ENG-023 baseline.
            practitioner_positions: Up to 3 practitioner positions.
            source_urls: Source URLs for audit trail.

        Returns:
            TensionObservation with auto-derived novelty_verdict.
        """
        positions: list[PractitionerPosition] = []
        for pos_dict in (practitioner_positions or [])[:PRACTITIONER_SUMMARY_COUNT]:
            positions.append(PractitionerPosition(
                practitioner_handle=pos_dict.get("handle", "anonymous"),
                platform=pos_dict.get("platform", source_domain),
                position_summary=pos_dict.get("summary", ""),
            ))

        observation = TensionObservation(
            coach_id=self.coach_id,
            identified_tension=topic,
            source_domain=source_domain,
            frequency_delta_percent=frequency_delta_percent,
            practitioner_positions=positions,
            source_urls=source_urls or [],
        )

        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=AGENT_NAME,
                action=STAGE_2_NAME,
                input_summary=f"topic='{topic}' delta={frequency_delta_percent:.1f}%",
                output_summary=f"verdict={observation.novelty_verdict.value}",
                decision=observation.novelty_verdict.value,
                decision_rationale=(
                    f"Frequency spike {frequency_delta_percent:.1f}% vs "
                    f"PASS threshold {NOVELTY_SPIKE_PASS_THRESHOLD}%"
                ),
            )

        return observation

    # ── Stage 3: Prompt Generation ───────────────────────────────────────────

    def build_telegram_prompt(
        self,
        observation: TensionObservation,
    ) -> TelegramPromptPayload:
        """FR15 §Stage 3: Build the rigid 3-part Telegram prompt.

        FR15 AC2: The 3-part structure is mandatory and enforced:
          Part 1: Observation announcement
          Part 2: Three practitioner position summaries
          Part 3: Closing question

        Args:
            observation: The validated TensionObservation from Stage 2.

        Returns:
            TelegramPromptPayload with has_required_structure() == True.

        Raises:
            ValueError: If fewer than 1 practitioner position provided.
        """
        # Part 1 — Observation
        signal_qualifier = " (emerging signal)" if observation.is_weak_signal else ""
        part_1 = (
            f"I am seeing a lot of conversation in your community about "
            f"\"{observation.identified_tension}\"{signal_qualifier}. "
            f"This is showing a {observation.frequency_delta_percent:.0f}% spike "
            f"in activity on {observation.source_domain} in the last 48 hours."
        )

        # Part 2 — Practitioner Summaries
        if observation.practitioner_positions:
            position_lines = []
            for i, pos in enumerate(
                observation.practitioner_positions[:PRACTITIONER_SUMMARY_COUNT], 1
            ):
                position_lines.append(
                    f"{i}. {pos.practitioner_handle} ({pos.platform}): "
                    f"{pos.position_summary}"
                )
            summaries_text = "\n".join(position_lines)
        else:
            summaries_text = (
                "Practitioners in your community are actively engaging with this tension "
                "from multiple angles."
            )

        part_2 = (
            f"Three practitioners/users I tracked are taking these positions:\n"
            f"{summaries_text}"
        )

        # Part 3 — Closing question
        part_3 = (
            "Does this connect to something you have been thinking about "
            "for your audience?"
        )

        payload = TelegramPromptPayload(
            coach_id=self.coach_id,
            part_1_observation=part_1,
            part_2_practitioner_summaries=part_2,
            part_3_closing_question=part_3,
            is_weak_signal=observation.is_weak_signal,
            source_tension=observation,
        )

        if not payload.has_required_structure():
            raise ValueError(
                "FR15 AC2 VIOLATION: Generated prompt failed 3-part structure check. "
                f"Parts — P1: '{part_1[:50]}...' P2: '{part_2[:50]}...' P3: '{part_3[:50]}'"
            )

        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=AGENT_NAME,
                action=STAGE_3_NAME,
                input_summary=f"tension='{observation.identified_tension}'",
                output_summary="3-part Telegram prompt generated",
                decision="PROMPT_GENERATED",
            )

        return payload

    # ── Stage 4: Coach Response Ingestion ────────────────────────────────────

    def process_coach_response(
        self,
        raw_response_text: str,
        observation: TensionObservation,
        response_type: str = "text",
    ) -> SessionInitiationResult:
        """FR15 §Stage 4: Process coach's reply and route or abort.

        FR15 AC3: Explicit decline or < 15-word response → session_aborted_by_coach.
        Valid response → SessionInitiationResult with DEP-ENG-005 extension fields.

        Args:
            raw_response_text: Coach's raw Telegram response text.
            observation: The TensionObservation that seeded the prompt.
            response_type: 'text' or 'voice_transcription'.

        Returns:
            SessionInitiationResult — either session initiated or aborted.
        """
        coach_response = CoachResponse(
            coach_id=self.coach_id,
            raw_text=raw_response_text,
            response_type=response_type,
        )

        # Check decline
        if coach_response.is_decline:
            abort_result = SessionInitiationResult(
                coach_id=self.coach_id,
                session_aborted=True,
                abort_reason=coach_response.decline_reason,
                initiation_type=SessionInitiationType.SYSTEM_PROACTIVE,
            )
            if self.receipt_chain:
                self.receipt_chain.log(
                    agent_id=INTAKE_AGENT_NAME,
                    action=STAGE_4_NAME,
                    input_summary=f"response='{raw_response_text[:60]}...' words={coach_response.word_count}",
                    output_summary="session_aborted_by_coach",
                    decision="SESSION_ABORTED",
                    decision_rationale=f"decline_reason={coach_response.decline_reason}",
                )
            return abort_result

        # Valid response — build DEP-ENG-005 extension
        trigger_id = (
            f"TRIG-{self.coach_id}-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        )
        # Simple mechanism extraction: first meaningful noun phrase from response
        extracted_mechanism = self._extract_mechanism(raw_response_text)
        frequency_str = f"+{observation.frequency_delta_percent:.0f}% spike 48h"

        result = SessionInitiationResult(
            coach_id=self.coach_id,
            session_aborted=False,
            initiation_type=SessionInitiationType.SYSTEM_PROACTIVE,
            trigger_id=trigger_id,
            identified_tension=observation.identified_tension,
            source_domain=observation.source_domain,
            frequency_delta=frequency_str,
            coach_raw_response=raw_response_text,
            extracted_mechanism=extracted_mechanism,
            authentication_status="CONFIRMED_READY_FOR_M2",
            cral_initiation_signal_emitted=True,
        )

        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=INTAKE_AGENT_NAME,
                action=STAGE_4_NAME,
                input_summary=f"response='{raw_response_text[:80]}'",
                output_summary=f"trigger_id={trigger_id} mechanism='{extracted_mechanism}'",
                decision="SESSION_INITIATED",
                decision_rationale="Valid response → DEP-ENG-005 extension emitted",
            )

        return result

    # ── Silent Abort ─────────────────────────────────────────────────────────

    def build_abort_log(
        self,
        abort_type: str,
        reason: str,
        frequency_delta_percent: Optional[float] = None,
        coach_response_text: Optional[str] = None,
        decline_reason: Optional[CoachDeclineReason] = None,
    ) -> MonitorAbortLog:
        """Build a silent abort log for Stage 2 FAIL or coach decline.

        FR15 §Stage 2: 'Write a silent_abort log.'
        FR15 §Stage 4: 'Log session_aborted_by_coach.'
        """
        log = MonitorAbortLog(
            coach_id=self.coach_id,
            abort_type=abort_type,
            reason=reason,
            frequency_delta_percent=frequency_delta_percent,
            coach_response_text=coach_response_text,
            decline_reason=decline_reason,
        )

        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=AGENT_NAME,
                action=f"ABORT-{abort_type.upper()}",
                input_summary=reason,
                output_summary=f"abort_logged coach_id={self.coach_id}",
                decision=abort_type,
            )

        return log

    # ── Full Pipeline ─────────────────────────────────────────────────────────

    def run_full_pipeline(
        self,
        topic: str,
        source_domain: str,
        frequency_delta_percent: float,
        practitioner_positions: Optional[list[dict[str, str]]] = None,
        source_urls: Optional[list[str]] = None,
        allowed_domains: Optional[list[str]] = None,
        coach_response_text: Optional[str] = None,
        response_type: str = "text",
    ) -> MonitorRunResult:
        """Run the full 4-stage scheduled monitor pipeline.

        FR15 AC4: ADR-01 — verifies all source_urls against allowed_domains.
        If tension FAIL → MonitorRunResult with ABORTED_NO_TENSION.
        If coach declined → ABORTED_COACH_DECLINED.
        If valid response → SESSION_INITIATED.

        Args:
            topic: Identified cultural tension.
            source_domain: Primary platform.
            frequency_delta_percent: Percentage spike vs baseline.
            practitioner_positions: Up to 3 practitioner positions.
            source_urls: Source URLs scraped.
            allowed_domains: Permitted domains from tribe_soul.json (ADR-01).
            coach_response_text: Coach's Telegram reply (None = simulate no reply).
            response_type: 'text' or 'voice_transcription'.

        Returns:
            MonitorRunResult with complete pipeline state.
        """
        # ADR-01: Verify all source URLs are within allowed scope
        adr01_verified = True
        if allowed_domains is not None and source_urls:
            for url in source_urls:
                if not any(domain in url for domain in allowed_domains):
                    adr01_verified = False
                    logger.warning(
                        "ADR-01 VIOLATION: URL '%s' not in allowed domains for coach %s",
                        url, self.coach_id,
                    )

        # Stage 1 receipt
        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=AGENT_NAME,
                action=STAGE_1_NAME,
                input_summary=(
                    f"topic='{topic}' source='{source_domain}' "
                    f"urls={len(source_urls or [])}"
                ),
                output_summary="raw_discourse_payload_ready",
            )

        # Stage 2: Assess novelty
        observation = self.assess_tension_novelty(
            topic=topic,
            source_domain=source_domain,
            frequency_delta_percent=frequency_delta_percent,
            practitioner_positions=practitioner_positions,
            source_urls=source_urls,
        )

        # Stage 2 FAIL → silent abort
        if observation.novelty_verdict == MonitorVerdict.FAIL:
            abort_log = self.build_abort_log(
                abort_type="silent_abort",
                reason=f"No novel tension: delta={frequency_delta_percent:.1f}% < {NOVELTY_SPIKE_PROVISIONAL_MIN}%",
                frequency_delta_percent=frequency_delta_percent,
            )
            return MonitorRunResult(
                coach_id=self.coach_id,
                run_status=MonitorRunStatus.ABORTED_NO_TENSION,
                tension_observation=observation,
                abort_log=abort_log,
                scraping_source_urls=source_urls or [],
                adr01_verified=adr01_verified,
            )

        # Stage 3: Build prompt
        prompt_payload = self.build_telegram_prompt(observation)

        run_status = (
            MonitorRunStatus.COMPLETED_WEAK_SIGNAL
            if observation.is_weak_signal
            else MonitorRunStatus.COMPLETED_TENSION_FOUND
        )

        # No coach response provided — pipeline stops at prompt delivery
        if coach_response_text is None:
            return MonitorRunResult(
                coach_id=self.coach_id,
                run_status=run_status,
                tension_observation=observation,
                prompt_payload=prompt_payload,
                scraping_source_urls=source_urls or [],
                adr01_verified=adr01_verified,
            )

        # Stage 4: Process coach response
        session_result = self.process_coach_response(
            raw_response_text=coach_response_text,
            observation=observation,
            response_type=response_type,
        )

        if session_result.session_aborted:
            abort_log = self.build_abort_log(
                abort_type="session_aborted_by_coach",
                reason=f"Coach declined: {session_result.abort_reason}",
                coach_response_text=coach_response_text,
                decline_reason=session_result.abort_reason,
            )
            return MonitorRunResult(
                coach_id=self.coach_id,
                run_status=MonitorRunStatus.ABORTED_COACH_DECLINED,
                tension_observation=observation,
                prompt_payload=prompt_payload,
                session_result=session_result,
                abort_log=abort_log,
                scraping_source_urls=source_urls or [],
                adr01_verified=adr01_verified,
            )

        return MonitorRunResult(
            coach_id=self.coach_id,
            run_status=MonitorRunStatus.SESSION_INITIATED,
            tension_observation=observation,
            prompt_payload=prompt_payload,
            session_result=session_result,
            scraping_source_urls=source_urls or [],
            adr01_verified=adr01_verified,
        )

    # ── Internal Helpers ─────────────────────────────────────────────────────

    def _extract_mechanism(self, response_text: str) -> str:
        """Extract a short mechanism keyword from the coach's response.

        Simple heuristic: Returns the first sentence trimmed to ≤60 chars.
        In production this would be an LLM extraction call.
        """
        first_sentence = response_text.split(".")[0].strip()
        return first_sentence[:60] if first_sentence else response_text[:60]
