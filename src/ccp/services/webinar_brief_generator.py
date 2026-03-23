"""
FR52 — Webinar Brief Generator
================================
Cross-references CBCS client intelligence to produce a segmented
WebinarConversionBriefRow (DEP-ENG-073) consumed by FR33.

Classes
-------
ChangeTalkSubstringGate
    Validates that injected change-talk quotes are verbatim substrings
    of the original archive using exact match + Levenshtein fallback.

WebinarBriefArchitect
    Orchestrates ICT mode resolution, instruction-string mapping,
    Change Talk injection, gate evaluation, and receipt logging.
"""

from __future__ import annotations

import statistics
import uuid
from datetime import datetime, timezone

from src.ccp.models.cpsc_models import (
    AlignmentGateVerdict,
    WebinarBriefError,
    WebinarConversionBriefRow,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# ICT mode threshold for segment routing (§4 Stage 1)
WEBINAR_ICT_LOW_THRESHOLD: int = 3   # modal ≤ 3 → intro validation path
WEBINAR_ICT_HIGH_THRESHOLD: int = 4  # modal ≥ 4 → close offer-heavy path

# Gate thresholds (§4 Stage 2)
PASS_EXACT_MATCH_MIN: int = 2      # ≥ 2 exact substrings → PASS
PROVISIONAL_LEVENSHTEIN_MAX: int = 3  # 1 exact OR levenshtein < 3 → PROVISIONAL

# Instruction strings (§4 Stage 1)
INTRO_INSTRUCTION_LOW: str = (
    "Instruct V2WS: Spend 15% of slide count validating the pain state. "
    "Do not mention solutions."
)
CLOSE_INSTRUCTION_LOW: str = (
    "Instruct V2WS: Spend 20% of slide count on offer parameters."
)
INTRO_INSTRUCTION_HIGH: str = (
    "Instruct V2WS: Spend 10% of slide count on pain validation. "
    "Move to solution framing by slide 3."
)
CLOSE_INSTRUCTION_HIGH: str = (
    "Instruct V2WS: Spend 35% of slide count on offer parameters. "
    "Inject exact Change Talk phrases here."
)


# ---------------------------------------------------------------------------
# Levenshtein distance (pure Python — no external dep)
# ---------------------------------------------------------------------------

def _levenshtein(a: str, b: str) -> int:
    """Standard dynamic-programming Levenshtein edit distance."""
    if a == b:
        return 0
    len_a, len_b = len(a), len(b)
    if len_a == 0:
        return len_b
    if len_b == 0:
        return len_a
    prev = list(range(len_b + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * len_b
        for j, cb in enumerate(b, 1):
            curr[j] = min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + (0 if ca == cb else 1),
            )
        prev = curr
    return prev[len_b]


# ---------------------------------------------------------------------------
# ChangeTalkSubstringGate
# ---------------------------------------------------------------------------

class ChangeTalkSubstringGate:
    """
    Validates change-talk injected quotes against the source archive.

    Parameters
    ----------
    archive_strings : list[str]
        The raw Change Talk Vault strings from FR-CBCS-01 (DEP-ENG-016).
    injected_quotes : list[str]
        Quotes placed by the LLM (or caller) into the brief.

    Gate logic (§4 Stage 2)
    -----------------------
    - PASS_FALLBACK : archive is empty → bypass evaluation entirely
    - PASS            : ≥ 2 injected quotes are exact substrings of any archive string
    - PROVISIONAL_PARAPHRASED : 1 exact match OR any Levenshtein distance < 3
    - FAIL_HALLUCINATED : 0 exact matches
    """

    def __init__(
        self,
        archive_strings: list[str],
        injected_quotes: list[str],
    ) -> None:
        self._archive = archive_strings
        self._injected = injected_quotes

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(self) -> tuple[AlignmentGateVerdict, list[str]]:
        """
        Return ``(verdict, validated_quotes)``.

        ``validated_quotes`` contains only the injected quotes that pass
        the exact-substring check (empty on FAIL/FALLBACK).
        """
        if not self._archive:
            return AlignmentGateVerdict.PASS_FALLBACK, []

        exact_matches: list[str] = []
        near_matches: int = 0

        for quote in self._injected:
            if self._is_exact_substring(quote):
                exact_matches.append(quote)
            elif self._has_near_match(quote):
                near_matches += 1

        if len(exact_matches) >= PASS_EXACT_MATCH_MIN:
            return AlignmentGateVerdict.PASS, exact_matches

        if len(exact_matches) == 1 or near_matches > 0:
            return AlignmentGateVerdict.PROVISIONAL_PARAPHRASED, exact_matches

        return AlignmentGateVerdict.FAIL_HALLUCINATED, []

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_exact_substring(self, quote: str) -> bool:
        """True if ``quote`` is an exact character-for-character substring
        of any string in the archive."""
        return any(quote in archive_str for archive_str in self._archive)

    def _has_near_match(self, quote: str) -> bool:
        """True if Levenshtein distance to any archive string is < threshold."""
        for archive_str in self._archive:
            if _levenshtein(quote, archive_str) < PROVISIONAL_LEVENSHTEIN_MAX:
                return True
        return False


# ---------------------------------------------------------------------------
# WebinarBriefArchitect
# ---------------------------------------------------------------------------

class WebinarBriefArchitect:
    """
    Orchestrates FR52: resolves dominant coping target, maps instruction
    strings, applies the Structural Coping Alignment Gate, and returns
    a ``WebinarConversionBriefRow``.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain for DEP-ENG-041 cryptographic logging.
    """

    _AGENT_ID = "webinar-brief-architect"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compile_brief(
        self,
        *,
        coping_positions: list[int],
        change_talk_archive: list[str],
        injected_quotes: list[str],
    ) -> WebinarConversionBriefRow:
        """
        Compile and return a ``WebinarConversionBriefRow``.

        Parameters
        ----------
        coping_positions : list[int]
            Tribe ICT aggregate coping_position array (DEP-ENG-058).
            Must be non-empty.
        change_talk_archive : list[str]
            Raw Change Talk Vault strings (DEP-ENG-016).
            Empty list → PASS_FALLBACK path.
        injected_quotes : list[str]
            Quotes to inject into the brief (validated by gate).

        Returns
        -------
        WebinarConversionBriefRow

        Raises
        ------
        ValueError(WebinarBriefError.EMPTY_COPING_AGGREGATE)
            If coping_positions is empty.
        ValueError(WebinarBriefError.FAIL_HALLUCINATED)
            If gate returns FAIL_HALLUCINATED (hard abort, receipt logged).
        """
        if not coping_positions:
            raise ValueError(WebinarBriefError.EMPTY_COPING_AGGREGATE)

        # ── Stage 1: ICT Mode Resolution ──────────────────────────────
        dominant = statistics.mode(coping_positions)
        intro_str, close_str = self._resolve_instructions(dominant)

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="webinar-ict-resolve",
            output_summary=(
                f"coach={self._coach_id} dominant_coping={dominant} "
                f"archive_len={len(change_talk_archive)}"
            ),
        )

        # ── Stage 2: Structural Coping Alignment Gate ─────────────────
        gate = ChangeTalkSubstringGate(change_talk_archive, injected_quotes)
        verdict, validated_quotes = gate.evaluate()

        if verdict == AlignmentGateVerdict.FAIL_HALLUCINATED:
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="webinar-gate-evaluate",
                output_summary=(
                    f"coach={self._coach_id} verdict=FAIL_HALLUCINATED — "
                    "rewind_generation triggered"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(WebinarBriefError.FAIL_HALLUCINATED)

        # Fallback path: use all injected_quotes as-is
        final_quotes = validated_quotes if validated_quotes else injected_quotes

        self._rc.log(
            agent_id=self._AGENT_ID,
            action="webinar-gate-evaluate",
            output_summary=(
                f"coach={self._coach_id} verdict={verdict.value} "
                f"validated_quotes_count={len(final_quotes)}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        return WebinarConversionBriefRow(
            webinar_brief_id=str(uuid.uuid4()),
            coach_id=self._coach_id,
            dominant_coping_target=dominant,
            change_talk_injected_quotes=final_quotes,
            gate_verdict=verdict.value,
            intro_instruction_string=intro_str,
            close_instruction_string=close_str,
            computation_timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resolve_instructions(self, dominant: int) -> tuple[str, str]:
        """Map dominant coping position to (intro_instruction, close_instruction)."""
        if dominant <= WEBINAR_ICT_LOW_THRESHOLD:
            return INTRO_INSTRUCTION_LOW, CLOSE_INSTRUCTION_LOW
        return INTRO_INSTRUCTION_HIGH, CLOSE_INSTRUCTION_HIGH
