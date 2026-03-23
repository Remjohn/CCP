"""
FR-CBCS-09 — Habit Architecture Module
========================================
Enforces Implementation Intentions (Gollwitzer, 1999) via If/Then syntax
parsing, concrete action verification, and habit lifecycle state machine.

Spec ref: FR_CBCS_09_Habit_Architecture_Module_Tech_Spec.md
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    ABSTRACT_VERBS,
    HABIT_ABANDONMENT_DAYS,
    HabitArchitectureError,
    HabitArchitectureTrackerRow,
    HabitStatus,
    HabitVerificationVerdict,
)

# ── Compiled regex patterns ────────────────────────────────────────────

# If/When … Then/I will/I'm going to syntax (§4 Stage 2)
_IF_THEN_RE = re.compile(
    r"\b(if|when)\b\s+(.+?)\s*[,.]?\s*\b(then|i will|i'm going to)\b\s+(.+)",
    re.IGNORECASE | re.DOTALL,
)

# Abstract verb detector (§4 Stage 2)
_ABSTRACT_VERB_RE = re.compile(
    r"\b(" + "|".join(re.escape(v) for v in ABSTRACT_VERBS) + r")\b",
    re.IGNORECASE,
)

# Broken-habit self-report patterns (§4 Stage 4)
_BROKEN_RE = re.compile(
    r"\b(i didn't do it|i missed my habit|i skipped|i failed|didn't follow through)\b",
    re.IGNORECASE,
)


class ImplementationIntentionParser:
    """Parses client goal messages for Implementation Intention structure.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(HabitArchitectureError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 1 + 2: Intention Parsing ─────────────────────────────────

    @staticmethod
    def detect_if_then_syntax(text: str) -> bool:
        """Return ``True`` if *text* contains If/When…Then/I will syntax."""
        return _IF_THEN_RE.search(text) is not None

    @staticmethod
    def extract_components(text: str) -> tuple[Optional[str], Optional[str]]:
        """Extract (environmental_cue, concrete_action) from *text*.

        Returns ``(None, None)`` if If/Then syntax is absent.
        """
        m = _IF_THEN_RE.search(text)
        if m is None:
            return None, None
        cue = m.group(2).strip().rstrip(",.")
        action = m.group(4).strip().rstrip(".,!?")
        return cue, action

    @staticmethod
    def is_concrete_action(action_text: Optional[str]) -> bool:
        """Return ``True`` if *action_text* contains a concrete (non-abstract) verb."""
        if not action_text or not action_text.strip():
            return False
        words = action_text.lower().split()
        if not words:
            return False
        # Skip auxiliary/pronoun/common function words to find the core verb
        _skip = {
            "i", "you", "he", "she", "we", "they", "it", "my", "me",
            "will", "would", "shall", "should", "can", "could", "may",
            "might", "must", "am", "is", "are", "was", "were",
            "a", "an", "the", "to", "of", "in", "on", "at",
            "and", "or", "but", "for", "with", "out", "not",
            "do", "does", "did", "have", "has", "had",
            "going", "gonna", "just", "also", "more", "very",
            "i'm", "i'll",
        }
        for w in words:
            w_clean = w.strip(".,!?;:'\"")
            if w_clean in _skip or len(w_clean) <= 1:
                continue
            # First meaningful word: check if it's abstract
            if w_clean in ABSTRACT_VERBS:
                return False
            return True
        return False

    # ── Stage 3: Verification Gate ─────────────────────────────────────

    def parse_and_verify(
        self,
        client_id: str,
        raw_client_message_text: str,
    ) -> HabitArchitectureTrackerRow:
        """Parse client message and produce a verified habit tracker row.

        Parameters
        ----------
        client_id:
            Unique client identifier.
        raw_client_message_text:
            The raw text of the client's goal/habit message.

        Returns
        -------
        HabitArchitectureTrackerRow
            Tracker row with verification verdict and habit status.
        """
        now_iso = datetime.now(timezone.utc).isoformat()

        # Empty message guard
        if not raw_client_message_text or not raw_client_message_text.strip():
            row = HabitArchitectureTrackerRow(
                tracker_id=str(uuid.uuid4()),
                client_id=client_id,
                coach_id=self._coach,
                environmental_cue=None,
                concrete_action=None,
                habit_status=HabitStatus.FORMING.value,
                verification_verdict=HabitVerificationVerdict.FAIL.value,
                last_checked_date=now_iso,
            )
            self._log_receipt(row)
            return row

        # Stage 2 — Variable resolution
        if_then_found = self.detect_if_then_syntax(raw_client_message_text)
        cue, action = self.extract_components(raw_client_message_text)
        concrete_found = self.is_concrete_action(action) if if_then_found else False

        # Stage 3 — Gate evaluation
        if if_then_found and concrete_found:
            verdict = HabitVerificationVerdict.PASS
            status = HabitStatus.VERIFIED
        elif if_then_found and not concrete_found:
            verdict = HabitVerificationVerdict.PROVISIONAL
            status = HabitStatus.FORMING
        else:
            verdict = HabitVerificationVerdict.FAIL
            status = HabitStatus.FORMING

        row = HabitArchitectureTrackerRow(
            tracker_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach,
            environmental_cue=cue,
            concrete_action=action if concrete_found else None,
            habit_status=status.value,
            verification_verdict=verdict.value,
            last_checked_date=now_iso,
        )
        self._log_receipt(row)
        return row

    # ── Stage 4: Broken habit detection ────────────────────────────────

    def check_broken_report(
        self,
        client_id: str,
        message: str,
        existing_row: HabitArchitectureTrackerRow,
    ) -> HabitArchitectureTrackerRow:
        """Check if client reports a broken habit. Returns updated row."""
        if _BROKEN_RE.search(message):
            updated = existing_row.model_copy(update={
                "habit_status": HabitStatus.BROKEN.value,
                "last_checked_date": datetime.now(timezone.utc).isoformat(),
            })
            self._rc.log(
                agent_id="implementation-intention-parser",
                action="habit-broken-detected",
                input_summary=f"client={client_id}",
                output_summary=f"status=BROKEN",
                decision="BROKEN",
                decision_rationale="Client self-reported habit failure",
            )
            return updated
        return existing_row


class HabitAbandonmentChecker:
    """Cron-style checker that auto-prunes stale habits to ABANDONED.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(HabitArchitectureError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    def check_abandonment(
        self,
        row: HabitArchitectureTrackerRow,
        reference_time: Optional[datetime] = None,
    ) -> HabitArchitectureTrackerRow:
        """If *row* is stale (>14 days with no updates), mark ABANDONED.

        Parameters
        ----------
        row:
            The existing tracker row to evaluate.
        reference_time:
            Optional reference datetime (UTC). Defaults to now.

        Returns
        -------
        HabitArchitectureTrackerRow
            Original row or updated with ABANDONED status.
        """
        if row.habit_status == HabitStatus.ABANDONED.value:
            return row  # Already abandoned

        ref = reference_time or datetime.now(timezone.utc)
        last_checked = datetime.fromisoformat(row.last_checked_date)
        # Make timezone-aware if naive
        if last_checked.tzinfo is None:
            last_checked = last_checked.replace(tzinfo=timezone.utc)

        days_since = (ref - last_checked).days

        if days_since > HABIT_ABANDONMENT_DAYS:
            updated = row.model_copy(update={
                "habit_status": HabitStatus.ABANDONED.value,
                "last_checked_date": ref.isoformat(),
            })
            self._rc.log(
                agent_id="habit-abandonment-checker",
                action="habit-auto-abandon",
                input_summary=f"tracker={row.tracker_id}, days_since={days_since}",
                output_summary="status=ABANDONED",
                decision="ABANDONED",
                decision_rationale=f"No activity for {days_since} days (threshold={HABIT_ABANDONMENT_DAYS})",
            )
            return updated

        return row

    # ── Receipt Chain ──────────────────────────────────────────────────

    def _log_receipt(self, row: HabitArchitectureTrackerRow) -> None:
        self._rc.log(
            agent_id="habit-abandonment-checker",
            action="habit-abandonment-check",
            input_summary=f"tracker={row.tracker_id}",
            output_summary=f"status={row.habit_status}",
            decision=row.habit_status,
        )


# ── Shared receipt logging for ImplementationIntentionParser ───────────

def _log_receipt_impl(self: ImplementationIntentionParser, row: HabitArchitectureTrackerRow) -> None:
    self._rc.log(
        agent_id="implementation-intention-parser",
        action="habit-intention-parse",
        input_summary=f"client={row.client_id}",
        output_summary=f"verdict={row.verification_verdict}, status={row.habit_status}",
        decision=row.verification_verdict,
        decision_rationale=f"cue={'present' if row.environmental_cue else 'absent'}, action={'concrete' if row.concrete_action else 'abstract/absent'}",
        metadata={
            "tracker_id": row.tracker_id,
            "habit_status": row.habit_status,
        },
    )

# Attach receipt method
ImplementationIntentionParser._log_receipt = _log_receipt_impl  # type: ignore[attr-defined]
