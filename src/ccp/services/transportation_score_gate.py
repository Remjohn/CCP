"""
FR-CBCS-08 — Transportation Score Gate
========================================
Strict algorithmic quality filter for voice delivery drafts.
Grades against four Transportation Theory components:
  1. Sensory Detail count
  2. Distancing Language count (zero tolerance)
  3. Prosodic Match (cosine similarity vs Voice DNA)
  4. Narrative Arc (past→present/future tense shift)

Spec ref: FR_CBCS_08_Transportation_Score_Gate_Tech_Spec.md
"""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    DISTANCING_WORDS,
    PROSODIC_MATCH_THRESHOLD,
    SENSORY_WORDS,
    TransportationGateResult,
    TransportGateError,
    TransportGateVerdict,
    TransportMetricsPayload,
)

# ── Compiled regex patterns ────────────────────────────────────────────
_SENSORY_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in SENSORY_WORDS) + r")\b",
    re.IGNORECASE,
)

_DISTANCING_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in DISTANCING_WORDS) + r")\b",
    re.IGNORECASE,
)

# Past-tense indicators → present/future-tense indicators
_PAST_RE = re.compile(r"\b(was|were|had|did|used to|went|felt|thought|remembered)\b", re.IGNORECASE)
_PRESENT_FUTURE_RE = re.compile(r"\b(is|am|are|will|now|today|going to|can|shall)\b", re.IGNORECASE)


def _sha256(text: str) -> str:
    """Return hex SHA-256 digest of *text*."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Pure-Python cosine similarity — no NumPy dependency."""
    if len(vec_a) != len(vec_b) or len(vec_a) == 0:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = sum(a * a for a in vec_a) ** 0.5
    mag_b = sum(b * b for b in vec_b) ** 0.5
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot / (mag_a * mag_b)


class TransportationScoreEvaluator:
    """Evaluates voice-delivery script drafts against Transportation Theory.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(TransportGateError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 1 + 2: Component Analysis ────────────────────────────────

    @staticmethod
    def count_sensory_details(draft: str) -> int:
        """Count sensory detail words in *draft* (§4 Stage 2)."""
        return len(_SENSORY_RE.findall(draft))

    @staticmethod
    def count_distancing_language(draft: str) -> int:
        """Count distancing language occurrences in *draft* (§4 Stage 2)."""
        return len(_DISTANCING_RE.findall(draft))

    @staticmethod
    def compute_prosodic_match(
        draft_syntax_frequencies: list[float],
        coach_syntax_baseline: list[float],
    ) -> float:
        """Cosine similarity between draft syntax and Voice DNA baseline (§4 Stage 2)."""
        return _cosine_similarity(draft_syntax_frequencies, coach_syntax_baseline)

    @staticmethod
    def detect_narrative_arc(draft: str) -> bool:
        """Detect past→present/future tense shift indicating story arc (§4 Stage 2).

        Returns ``True`` if the draft contains *both* past-tense and
        present/future-tense markers with the first past-tense marker
        appearing *before* the first present/future-tense marker (indicating
        narrative movement from past into the present).
        """
        past_match = _PAST_RE.search(draft)
        future_match = _PRESENT_FUTURE_RE.search(draft)
        if past_match is None or future_match is None:
            return False
        # Past must precede present/future to constitute an arc
        return past_match.start() < future_match.start()

    # ── Stage 3: Quality Gate ──────────────────────────────────────────

    def evaluate(
        self,
        voice_message_script_draft: str,
        draft_syntax_frequencies: Optional[list[float]] = None,
        coach_syntax_baseline: Optional[list[float]] = None,
    ) -> TransportationGateResult:
        """Run the full Transportation Score Gate evaluation.

        Parameters
        ----------
        voice_message_script_draft:
            The raw text of the voice script to evaluate.
        draft_syntax_frequencies:
            Frequency vector derived from the draft. If ``None``, prosodic
            match defaults to ``0.0``.
        coach_syntax_baseline:
            Voice DNA syntax baseline vector. If ``None``, prosodic match
            defaults to ``0.0``.

        Returns
        -------
        TransportationGateResult
            Complete evaluation with verdict, metrics, and failure details.
        """
        evaluation_id = str(uuid.uuid4())
        evaluated_at = datetime.now(timezone.utc).isoformat()

        # Empty-script guard (§4 Stage 1)
        if not voice_message_script_draft or not voice_message_script_draft.strip():
            result = TransportationGateResult(
                evaluation_id=evaluation_id,
                script_hash=_sha256(""),
                gate_verdict=TransportGateVerdict.FAIL.value,
                metrics_payload=TransportMetricsPayload(
                    sensory_count=0,
                    distancing_count=0,
                    prosodic_match_score=0.0,
                    narrative_arc_found=False,
                ),
                failure_details=[TransportGateError.SCRIPT_EMPTY.value],
                evaluated_at=evaluated_at,
            )
            self._log_receipt(result)
            return result

        # Stage 2 — Metric computation
        sensory_count = self.count_sensory_details(voice_message_script_draft)
        distancing_count = self.count_distancing_language(voice_message_script_draft)

        prosodic_match = 0.0
        if draft_syntax_frequencies is not None and coach_syntax_baseline is not None:
            prosodic_match = self.compute_prosodic_match(
                draft_syntax_frequencies, coach_syntax_baseline,
            )

        narrative_arc = self.detect_narrative_arc(voice_message_script_draft)

        # Stage 3 — Gate evaluation
        cond1 = sensory_count > 0
        cond2 = distancing_count == 0
        cond3 = prosodic_match >= PROSODIC_MATCH_THRESHOLD
        cond4 = narrative_arc is True

        failure_details: list[str] = []

        if cond2 and cond3 and cond4:
            if cond1:
                verdict = TransportGateVerdict.PASS
            else:
                verdict = TransportGateVerdict.PROVISIONAL_REVIEW
        else:
            verdict = TransportGateVerdict.FAIL
            if not cond2:
                failure_details.append(
                    "Failed Condition 2: Remove distancing language."
                )
            if not cond3:
                failure_details.append(
                    "Failed Condition 3: Prosodic match below threshold."
                )
            if not cond4:
                failure_details.append(
                    "Failed Condition 4: No narrative structure detected."
                )

        result = TransportationGateResult(
            evaluation_id=evaluation_id,
            script_hash=_sha256(voice_message_script_draft),
            gate_verdict=verdict.value,
            metrics_payload=TransportMetricsPayload(
                sensory_count=sensory_count,
                distancing_count=distancing_count,
                prosodic_match_score=round(prosodic_match, 4),
                narrative_arc_found=narrative_arc,
            ),
            failure_details=failure_details,
            evaluated_at=evaluated_at,
        )
        self._log_receipt(result)
        return result

    # ── Receipt Chain ──────────────────────────────────────────────────

    def _log_receipt(self, result: TransportationGateResult) -> None:
        self._rc.log(
            agent_id="transportation-score-evaluator",
            action="transportation-gate-evaluate",
            input_summary=f"script_hash={result.script_hash[:12]}…",
            output_summary=f"verdict={result.gate_verdict}",
            decision=result.gate_verdict,
            decision_rationale=(
                "; ".join(result.failure_details) if result.failure_details
                else "All conditions met"
            ),
            metadata={
                "evaluation_id": result.evaluation_id,
                "sensory_count": result.metrics_payload.sensory_count,
                "distancing_count": result.metrics_payload.distancing_count,
                "prosodic_match_score": result.metrics_payload.prosodic_match_score,
                "narrative_arc_found": result.metrics_payload.narrative_arc_found,
            },
        )
