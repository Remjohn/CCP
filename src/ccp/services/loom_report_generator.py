"""
FR60 — Loom Report Generation
================================
Translates FR56 campaign performance arrays into coach-facing narrative
documents. Enforces the Actionable Threshold Gate to prevent hallucinated
advice and vague summaries.

Classes
-------
ConversionSignalDetector
    Computes boolean signals (spike / crash) from group vs baseline rates.

ActionableThresholdGate
    Validates the recommendation_block against hallucination blacklist and
    vague-summary heuristics.

LoomIntelligenceTranslator
    Orchestrates both stages, assembles LoomNarrativeReportRow, and writes
    receipt chain entries (DEP-ENG-041).
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

from src.ccp.models.cpsc_models import (
    LoomGateVerdict,
    LoomNarrativeReportRow,
    LoomReportError,
    LoomSections,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants — Stage 1 conversion signal thresholds
# ---------------------------------------------------------------------------

# conversion_spike: group_conversion > baseline * SPIKE_MULTIPLIER
SPIKE_MULTIPLIER: float = 1.5

# conversion_crash: group_conversion < baseline / CRASH_DIVISOR
CRASH_DIVISOR: float = 2.0

# ---------------------------------------------------------------------------
# Constants — Stage 2 Actionable Threshold Gate
# ---------------------------------------------------------------------------

# Blacklisted terms that indicate hallucinated external-platform advice (§7 Task 2)
_HALLUCINATION_BLACKLIST_PATTERNS: list[str] = [
    r"\bfacebook\s+ads?\b",
    r"\binstagram\s+(ads?|traffic)\b",
    r"\btiktok\s+(ads?|campaigns?)\b",
    r"\bgoogle\s+ads?\b",
    r"\bclickfunnels?\b",
    r"\byoutube\s+ads?\b",
    r"\bpaid\s+(social|media)\b",
    r"\brun\s+ads?\b",
    r"\bbuy\s+traffic\b",
    r"\bseo\s+campaign\b",
]

_HALLUCINATION_REGEX = re.compile(
    "|".join(_HALLUCINATION_BLACKLIST_PATTERNS),
    re.IGNORECASE,
)

# Vague-summary patterns: strings devoid of numbers (§4 Stage 2 PROVISIONAL condition)
_VAGUE_SUMMARY_PATTERN = re.compile(r"\d")   # must contain at least one digit

# Minimum word count for a non-vague recommendation block
RECOMMENDATION_MIN_WORDS: int = 5


# ---------------------------------------------------------------------------
# ConversionSignalDetector — Stage 1
# ---------------------------------------------------------------------------

class ConversionSignalDetector:
    """
    Detects conversion spike / crash signals from performance data.

    Parameters
    ----------
    baseline_conversion : float
        Baseline campaign conversion rate (e.g. 0.10 for 10%).
    group_a_conversion : float
        Conversion rate for Group A (high coping tier cohort).
    group_b_conversion : float
        Conversion rate for Group B (low coping tier cohort).
    """

    def __init__(
        self,
        baseline_conversion: float,
        group_a_conversion: float,
        group_b_conversion: float,
    ) -> None:
        self._baseline = baseline_conversion
        self._group_a = group_a_conversion
        self._group_b = group_b_conversion

    def spike_detected(self) -> bool:
        """True if Group A conversion > baseline * SPIKE_MULTIPLIER."""
        if self._baseline <= 0:
            return False
        return self._group_a > self._baseline * SPIKE_MULTIPLIER

    def crash_detected(self) -> bool:
        """True if Group B conversion < baseline / CRASH_DIVISOR."""
        if self._baseline <= 0:
            return False
        return self._group_b < self._baseline / CRASH_DIVISOR

    def build_signal_text(self, conversion_counts: dict[str, int] | None = None) -> str:
        """
        Build a human-readable psychological_signal_block string.
        Includes at least one numeric reference per spec §4.
        """
        parts: list[str] = []
        if self.spike_detected():
            parts.append(
                f"SPIKE detected: Group A conversion {self._group_a:.0%} "
                f"exceeds baseline {self._baseline:.0%} × {SPIKE_MULTIPLIER}. "
                "Identity anchor messaging drove above-threshold response."
            )
        if self.crash_detected():
            parts.append(
                f"CRASH detected: Group B conversion {self._group_b:.0%} "
                f"fell below baseline {self._baseline:.0%} ÷ {CRASH_DIVISOR}. "
                "Commitment price misaligned with Coping Tier B."
            )
        if not parts:
            parts.append(
                f"No anomalous signals. Baseline: {self._baseline:.0%}. "
                f"Group A: {self._group_a:.0%}. Group B: {self._group_b:.0%}."
            )
        return " | ".join(parts)


# ---------------------------------------------------------------------------
# ActionableThresholdGate — Stage 2
# ---------------------------------------------------------------------------

class ActionableThresholdGate:
    """
    Validates a recommendation_block string against the spec's two-tier gate:

    FAIL_HALLUCINATED_ADVICE
        The block contains blacklisted platform terms (§7 Task 2, AC1).

    PROVISIONAL_VAGUE_SUMMARY
        The block contains no numeric data (no digits) — treated as vague
        and lacking statistical grounding (§4 Stage 2, AC2).

    PASS
        Block cites real numbers, no blacklisted terms (§4 Stage 2, AC3).
    """

    def __init__(self, recommendation_block: str) -> None:
        self._rec = recommendation_block

    def evaluate(self) -> LoomGateVerdict:
        # FAIL takes precedence (AC1)
        if _HALLUCINATION_REGEX.search(self._rec):
            return LoomGateVerdict.FAIL_HALLUCINATED_ADVICE

        # PROVISIONAL: no numeric content (AC2)
        if not _VAGUE_SUMMARY_PATTERN.search(self._rec):
            return LoomGateVerdict.PROVISIONAL_VAGUE_SUMMARY

        return LoomGateVerdict.PASS


# ---------------------------------------------------------------------------
# LoomIntelligenceTranslator
# ---------------------------------------------------------------------------

class LoomIntelligenceTranslator:
    """
    Orchestrates FR60: resolves narrative signals, evaluates the
    Actionable Threshold Gate, and returns a LoomNarrativeReportRow.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain (DEP-ENG-041).
    """

    _AGENT_ID = "loom-intelligence-translator"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        *,
        campaign_execution_id: str,
        baseline_conversion: float,
        group_a_conversion: float,
        group_b_conversion: float,
        summary_block: str,
        actionable_recommendation_block: str,
    ) -> LoomNarrativeReportRow:
        """
        Generate a Loom Narrative Report Row.

        Parameters
        ----------
        campaign_execution_id : str
            FR59 execution log UUID this report belongs to.
        baseline_conversion : float
            Baseline conversion rate (e.g. 0.10 = 10%).
        group_a_conversion : float
            Group A conversion rate.
        group_b_conversion : float
            Group B conversion rate.
        summary_block : str
            High-level summary text (operator-authored or pre-computed).
        actionable_recommendation_block : str
            Recommendation text to pass through the Actionable Threshold Gate.

        Returns
        -------
        LoomNarrativeReportRow

        Raises
        ------
        ValueError(LoomReportError.FAIL_HALLUCINATED_ADVICE)
            If hallucinated advice is detected (receipt logged before raising).
        """
        # ── Stage 1: Signal Detection ─────────────────────────────────
        detector = ConversionSignalDetector(
            baseline_conversion, group_a_conversion, group_b_conversion
        )
        signal_text = detector.build_signal_text()

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="loom-narrative-resolve",
            output_summary=(
                f"coach={self._coach_id} campaign={campaign_execution_id} "
                f"spike={detector.spike_detected()} crash={detector.crash_detected()}"
            ),
        )

        # ── Stage 2: Actionable Threshold Gate ───────────────────────
        gate = ActionableThresholdGate(actionable_recommendation_block)
        verdict = gate.evaluate()

        if verdict == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE:
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="loom-threshold-gate",
                output_summary=(
                    f"coach={self._coach_id} campaign={campaign_execution_id} "
                    "verdict=FAIL_HALLUCINATED_ADVICE — blacklisted platform term detected"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(LoomReportError.FAIL_HALLUCINATED_ADVICE)

        self._rc.log(
            agent_id=self._AGENT_ID,
            action="loom-threshold-gate",
            output_summary=(
                f"coach={self._coach_id} campaign={campaign_execution_id} "
                f"verdict={verdict.value}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        return LoomNarrativeReportRow(
            report_id=str(uuid.uuid4()),
            campaign_execution_id=campaign_execution_id,
            coach_id=self._coach_id,
            gate_verdict=verdict.value,
            loom_sections=LoomSections(
                summary_block=summary_block,
                psychological_signal_block=signal_text,
                actionable_recommendation_block=actionable_recommendation_block,
            ),
            computation_timestamp=datetime.now(timezone.utc).isoformat(),
        )
