"""
FR-CBCS-05 — 72-Hour Identity Anchor Protocol
================================================
BehavioralScienceGuard  — reactance prevention gate (§4 Stage 2)
IdentityAnchorOrchestrator — sequence builder + state machine (§4 Stages 1, 3, 4)

Academic grounding:
  - Freedman & Fraser (1966) Foot-in-the-Door
  - Cialdini (1984) Commitment & Consistency
  - Brehm (1966) Psychological Reactance
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    COMMERCIAL_KEYWORDS,
    IDENTITY_ANCHOR_COOLDOWN_DAYS,
    IDENTITY_ANCHOR_MAX_RETRIES,
    URGENT_PUNCTUATION_PATTERN,
    IdentityAnchorError,
    ProtocolSequencePayload,
    ProtocolStatus,
    ReactanceGateResult,
    ReactanceVerdict,
)

# ── Compiled pattern cache ─────────────────────────────────────────────

# Commercial keyword pattern — whole-word matches (e.g., "buy" not "buyer")
_COMMERCIAL_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in COMMERCIAL_KEYWORDS) + r")\b",
    re.IGNORECASE,
)

# Urgent punctuation: 2+ "!" OR 3+-letter all-caps word
_URGENT_RE = re.compile(URGENT_PUNCTUATION_PATTERN)


# ═══════════════════════════════════════════════════════════════════════
# Stage 2 — BehavioralScienceGuard (Reactance Prevention Gate)
# ═══════════════════════════════════════════════════════════════════════


class BehavioralScienceGuard:
    """
    Analyzes a combined sequence text for anti-reactance compliance.

    Gate rules (§4 Stage 2 exact thresholds):
      - commercial_flag_count = REGEX_COUNT(text, COMMERCIAL_KEYWORDS)
      - urgent_punctuation_count = REGEX_COUNT(text, URGENT_PUNCTUATION_PATTERN)

    Verdict:
      PASS         — commercial=0 AND urgent=0
      PROVISIONAL  — commercial=0 AND urgent>0  →  REVIEW_REQUIRED flag
      FAIL         — commercial>0               →  rewind_generation()
    """

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain | None = None) -> None:
        if not (2 <= len(coach_id) <= 4):
            raise ValueError(
                f"coach_id must be 2–4 characters (ADR-01). Got: {coach_id!r}"
            )
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ── Public API ────────────────────────────────────────────────────

    def evaluate(self, sequence_text: str) -> ReactanceGateResult:
        """
        Evaluate sequence_text for reactance risk.

        Args:
            sequence_text: Combined text of all three day scripts.

        Returns:
            ReactanceGateResult with verdict, counts, and flagged phrases.
        """
        commercial_matches = _COMMERCIAL_RE.findall(sequence_text)
        urgent_matches = _URGENT_RE.findall(sequence_text)

        commercial_count = len(commercial_matches)
        urgent_count = len(urgent_matches)
        flagged: list[str] = list(dict.fromkeys(commercial_matches))  # deduplicated

        if commercial_count > 0:
            verdict = ReactanceVerdict.FAIL
        elif urgent_count > 0:
            verdict = ReactanceVerdict.PROVISIONAL
        else:
            verdict = ReactanceVerdict.PASS

        result = ReactanceGateResult(
            verdict=verdict.value,
            commercial_flag_count=commercial_count,
            urgent_punctuation_count=urgent_count,
            flagged_phrases=flagged,
        )

        if self._rc is not None:
            self._rc.log(
                agent_id=self._coach_id,
                action="reactance-gate-evaluate",
                output_summary=(
                    f"verdict={verdict.value} commercial={commercial_count} "
                    f"urgent={urgent_count}"
                ),
            )

        return result

    # ── Static helpers ────────────────────────────────────────────────

    @staticmethod
    def count_commercial_flags(text: str) -> int:
        """Return the count of banned commercial keyword occurrences."""
        return len(_COMMERCIAL_RE.findall(text))

    @staticmethod
    def count_urgent_punctuation(text: str) -> int:
        """Return the count of urgent punctuation / ALL-CAPS occurrences."""
        return len(_URGENT_RE.findall(text))


# ═══════════════════════════════════════════════════════════════════════
# Stages 1, 3, 4 — IdentityAnchorOrchestrator
# ═══════════════════════════════════════════════════════════════════════


class IdentityAnchorOrchestrator:
    """
    Orchestrates the 72-Hour Identity Anchor Protocol.

    Responsibilities:
      Stage 1 — Build the three-day script array (d3, d2, d1).
      Stage 2 — Route through BehavioralScienceGuard.
      Stage 3 — Apply early-abort on client resistance signals.
      Stage 4 — Resolve output schema (ProtocolSequencePayload).
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        if not (2 <= len(coach_id) <= 4):
            raise ValueError(
                f"coach_id must be 2–4 characters (ADR-01). Got: {coach_id!r}"
            )
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._guard = BehavioralScienceGuard(coach_id=coach_id, receipt_chain=None)

    # ── Public API ────────────────────────────────────────────────────

    def build_sequence(
        self,
        client_id: str,
        day_minus_3_script: str,
        day_minus_2_script: str,
        day_minus_1_script: str,
        attempt: int = 1,
    ) -> ProtocolSequencePayload:
        """
        Build and gate a 72-hour sequence payload.

        Args:
            client_id: Target client identifier.
            day_minus_3_script: Observation Prompt (Day -3).
            day_minus_2_script: Competence Mirror (Day -2).
            day_minus_1_script: Anticipation Signal (Day -1).
            attempt: Current generation attempt number (1-indexed).

        Returns:
            ProtocolSequencePayload with status GENERATED or REVIEW_REQUIRED.

        Raises:
            ValueError: If attempt > IDENTITY_ANCHOR_MAX_RETRIES (hard abort).
            ValueError: If any script is empty.
        """
        if attempt > IDENTITY_ANCHOR_MAX_RETRIES:
            raise ValueError(
                f"{IdentityAnchorError.MAX_RETRIES_EXCEEDED.value}: "
                f"Exceeded {IDENTITY_ANCHOR_MAX_RETRIES} generation attempts."
            )

        for label, script in [
            ("day_minus_3_script", day_minus_3_script),
            ("day_minus_2_script", day_minus_2_script),
            ("day_minus_1_script", day_minus_1_script),
        ]:
            if not script or not script.strip():
                raise ValueError(
                    f"{IdentityAnchorError.SCRIPT_EMPTY.value}: "
                    f"{label} must not be empty."
                )

        combined = " ".join(
            [day_minus_3_script, day_minus_2_script, day_minus_1_script]
        )
        gate_result = self._guard.evaluate(combined)

        if gate_result.verdict == ReactanceVerdict.FAIL.value:
            raise ValueError(
                f"{IdentityAnchorError.MAX_RETRIES_EXCEEDED.value}: "
                f"Reactance gate FAIL — commercial_flag_count="
                f"{gate_result.commercial_flag_count}, "
                f"flagged={gate_result.flagged_phrases}. "
                f"Rewind generation and retry. "
                f"(attempt {attempt}/{IDENTITY_ANCHOR_MAX_RETRIES})"
            )

        if gate_result.verdict == ReactanceVerdict.PROVISIONAL.value:
            status = ProtocolStatus.REVIEW_REQUIRED
        else:
            status = ProtocolStatus.GENERATED

        payload = ProtocolSequencePayload(
            sequence_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            day_minus_3_script=day_minus_3_script,
            day_minus_2_script=day_minus_2_script,
            day_minus_1_script=day_minus_1_script,
            status=status.value,
            abort_reason=None,
            last_updated=datetime.now(timezone.utc).isoformat(),
        )

        if self._rc is not None:
            self._rc.log(
                agent_id=self._coach_id,
                action="identity-anchor-build",
                asset_id=payload.sequence_id,
                output_summary=(
                    f"status={status.value} attempt={attempt}"
                ),
            )

        return payload

    def apply_abort(
        self,
        payload: ProtocolSequencePayload,
        liwc_scores: dict[str, Any],
    ) -> ProtocolSequencePayload:
        """
        Apply Stage 3 Anti-Reactance Abort rule.

        Triggers ABORTED when:
          - Current status is D3_SENT or D2_SENT
          - AND (liwc_scores.negative_emotion > 0.05 OR
                 liwc_scores.anger > 0.02 OR
                 sentiment == 'hostile')

        Returns:
            Updated ProtocolSequencePayload (new object with mutated fields).
        """
        active_states = {ProtocolStatus.D3_SENT.value, ProtocolStatus.D2_SENT.value}
        if payload.status not in active_states:
            return payload

        neg_emotion: float = float(liwc_scores.get("negative_emotion", 0.0))
        anger: float = float(liwc_scores.get("anger", 0.0))
        sentiment: str = str(liwc_scores.get("sentiment", "")).lower()

        should_abort = (
            neg_emotion > 0.05
            or anger > 0.02
            or sentiment == "hostile"
        )

        if not should_abort:
            return payload

        aborted = ProtocolSequencePayload(
            sequence_id=payload.sequence_id,
            client_id=payload.client_id,
            coach_id=payload.coach_id,
            day_minus_3_script=payload.day_minus_3_script,
            day_minus_2_script=payload.day_minus_2_script,
            day_minus_1_script=payload.day_minus_1_script,
            status=ProtocolStatus.ABORTED.value,
            abort_reason="Client Resistance Detected",
            last_updated=datetime.now(timezone.utc).isoformat(),
        )

        if self._rc is not None:
            self._rc.log(
                agent_id=self._coach_id,
                action="identity-anchor-abort",
                asset_id=payload.sequence_id,
                output_summary=(
                    f"ABORTED — neg_emotion={neg_emotion:.3f} "
                    f"anger={anger:.3f} sentiment={sentiment}"
                ),
            )

        return aborted
