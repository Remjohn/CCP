"""
FR-CBCS-02 — SPT Stage Engine
==============================
Weekly classification engine computing Social Penetration Theory stage
(1-4) from trailing LIWC-22 marker windows.

Stage 1 + Stage 2 of the FR-CBCS-02 spec.

C-11 Persona Masking: agent names MUST NOT appear in external payloads.
ADR-01: All operations scoped to coach_id.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BLOCKED_MOOD_STATES,
    COGNITIVE_PROCESSES_THRESHOLD,
    EMOTIONAL_COMPLEXITY_THRESHOLD,
    EXCLUSIVE_WORDS_THRESHOLD,
    FIRST_PERSON_FREQ_THRESHOLD,
    HEDGING_WORDS_THRESHOLD,
    SPTError,
    SPTStage,
    TRAILING_WINDOW_14_DAYS,
    TRAILING_WINDOW_30_DAYS,
    LIWCScores,
    SPTClassificationResult,
    SPTDepthGaugeRow,
)


class SPTStageEngine:
    """Computes Social Penetration Theory stage from LIWC-22 markers.

    Parameters
    ----------
    coach_acronym : str
        2-4 char coach scope (ADR-01).
    coach_id : str
        Coach UUID for DB scoping.
    receipt_chain : ReceiptChain
        Audit trail.
    """

    def __init__(
        self,
        coach_acronym: str,
        coach_id: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"{SPTError.INVALID_COACH_ACRONYM.value}: "
                f"'{coach_acronym}' length must be 2-4."
            )
        self._coach = coach_acronym
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ── public — classify single client ─────────────────────────────

    def classify_client(
        self,
        client_id: str,
        liwc_scores_14d: LIWCScores | None = None,
        liwc_scores_30d: LIWCScores | None = None,
    ) -> SPTClassificationResult:
        """Classify a client's SPT stage from trailing LIWC windows.

        If no LIWC data is available, safely defaults to Stage 1
        (Orientation) per spec §4 Stage 1 failure condition.
        """
        now = datetime.now(timezone.utc).isoformat()
        warnings: list[str] = []

        # ── Fallback: no voice profile data → Orientation ──────────
        if liwc_scores_14d is None:
            warnings.append(
                f"{SPTError.MISSING_VOICE_PROFILE.value}: "
                f"client_id={client_id} — defaulting to ORIENTATION"
            )
            result = SPTClassificationResult(
                client_id=client_id,
                coach_id=self._coach_id,
                spt_stage=SPTStage.ORIENTATION.value,
                spt_stage_name=SPTStage.ORIENTATION.name,
                trailing_window_days=TRAILING_WINDOW_14_DAYS,
                liwc_snapshot=LIWCScores(
                    first_person_freq=0.0,
                    emotional_complexity=0.0,
                ),
                classification_warnings=warnings,
                timestamp_utc=now,
            )
            self._emit_receipt(client_id, result)
            return result

        # ── Stage evaluation (highest matching wins) ───────────────
        stage, window = self._resolve_stage(
            liwc_scores_14d, liwc_scores_30d, warnings
        )

        result = SPTClassificationResult(
            client_id=client_id,
            coach_id=self._coach_id,
            spt_stage=stage.value,
            spt_stage_name=stage.name,
            trailing_window_days=window,
            liwc_snapshot=liwc_scores_14d,
            classification_warnings=warnings,
            timestamp_utc=now,
        )
        self._emit_receipt(client_id, result)
        return result

    # ── public — batch classify ─────────────────────────────────────

    def classify_batch(
        self,
        clients: list[dict[str, Any]],
    ) -> list[SPTClassificationResult]:
        """Classify a batch of clients.

        Each dict must have 'client_id' and optionally 'liwc_14d' and
        'liwc_30d' as LIWCScores instances or None.
        """
        results: list[SPTClassificationResult] = []
        for c in clients:
            result = self.classify_client(
                client_id=c["client_id"],
                liwc_scores_14d=c.get("liwc_14d"),
                liwc_scores_30d=c.get("liwc_30d"),
            )
            results.append(result)
        return results

    # ── public — build DB row ───────────────────────────────────────

    def to_depth_gauge_row(
        self,
        result: SPTClassificationResult,
        previous_stage: int = 1,
    ) -> SPTDepthGaugeRow:
        """Convert a classification result to a persistence row."""
        return SPTDepthGaugeRow(
            client_id=result.client_id,
            coach_id=result.coach_id,
            spt_stage=result.spt_stage,
            spt_stage_name=result.spt_stage_name,
            previous_stage=previous_stage,
            trailing_window_days=result.trailing_window_days,
            last_computed_utc=result.timestamp_utc,
        )

    # ── internal — stage resolution rules (§4 Stage 2) ─────────────

    def _resolve_stage(
        self,
        liwc_14d: LIWCScores,
        liwc_30d: LIWCScores | None,
        warnings: list[str],
    ) -> tuple[SPTStage, int]:
        """Apply the exact variable resolution rules from the spec.

        Evaluation is top-down (highest stage first); first match wins.
        Each higher stage must also meet its predecessor's baseline.
        """

        # ── Check Orientation baseline ────────────────────────────
        orientation_baseline = (
            liwc_14d.first_person_freq < FIRST_PERSON_FREQ_THRESHOLD
            and liwc_14d.emotional_complexity < EMOTIONAL_COMPLEXITY_THRESHOLD
        )

        # ── Check Exploratory Affective baseline ──────────────────
        exploratory_baseline = (
            liwc_14d.first_person_freq >= FIRST_PERSON_FREQ_THRESHOLD
            and liwc_14d.emotional_complexity >= EMOTIONAL_COMPLEXITY_THRESHOLD
        )

        # ── Check Affective Exchange ──────────────────────────────
        affective_exchange = (
            exploratory_baseline
            and liwc_14d.exclusive_words > EXCLUSIVE_WORDS_THRESHOLD
            and liwc_14d.hedging_words < HEDGING_WORDS_THRESHOLD
        )

        # ── Check Stable Exchange (requires 30-day window) ────────
        if liwc_30d is not None and affective_exchange:
            stable_exchange = (
                liwc_30d.cognitive_processes > COGNITIVE_PROCESSES_THRESHOLD
                and liwc_30d.exclusive_words > EXCLUSIVE_WORDS_THRESHOLD
                and liwc_30d.hedging_words < HEDGING_WORDS_THRESHOLD
                and liwc_30d.first_person_freq >= FIRST_PERSON_FREQ_THRESHOLD
                and liwc_30d.emotional_complexity >= EMOTIONAL_COMPLEXITY_THRESHOLD
            )
            if stable_exchange:
                return SPTStage.STABLE_EXCHANGE, TRAILING_WINDOW_30_DAYS

        if affective_exchange:
            return SPTStage.AFFECTIVE_EXCHANGE, TRAILING_WINDOW_14_DAYS

        if exploratory_baseline:
            return SPTStage.EXPLORATORY_AFFECTIVE, TRAILING_WINDOW_14_DAYS

        # ── Default: Orientation ──────────────────────────────────
        return SPTStage.ORIENTATION, TRAILING_WINDOW_14_DAYS

    # ── internal — receipt ─────────────────────────────────────────

    def _emit_receipt(
        self,
        client_id: str,
        result: SPTClassificationResult,
    ) -> None:
        self._rc.log(
            agent_id="spt-stage-classifier",
            action="spt-classify",
            asset_id=client_id,
            input_summary=f"liwc_window={result.trailing_window_days}d",
            output_summary=f"spt_stage={result.spt_stage} ({result.spt_stage_name})",
            metadata={
                "coach": self._coach,
                "client_id": client_id,
                "spt_stage": result.spt_stage,
            },
        )
