"""
FR-CBCS-07 — Telegram Intimacy Index Calculator
================================================
Weekly cron-job computation of the 6-component Telegram Intimacy Index
(TII) and Parasocial Relationship (PSR) stage classification.

Stages 1 + 3 + 4 of the FR-CBCS-07 spec.

C-11 Persona Masking: agent names MUST NOT appear in external payloads.
ADR-01: All operations scoped to coach_id.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    MAX_EXPECTED_FREQUENCY,
    MAX_LATENCY_HOURS,
    PSR_BORDERLINE_THRESHOLD,
    PSR_INTENSE_PERSONAL_THRESHOLD,
    PSRStage,
    TII_PASS_THRESHOLD,
    TII_PROVISIONAL_CONSISTENCY,
    TII_PROVISIONAL_FLOOR,
    TII_WEIGHT_CONSISTENCY,
    TII_WEIGHT_DISCLOSURE,
    TII_WEIGHT_FREQUENCY,
    TII_WEIGHT_INITIATIVE,
    TII_WEIGHT_LATENCY,
    TII_WEIGHT_VOICE,
    TII_WINDOW_DAYS,
    TIIComponentScores,
    TIIError,
    TIIGateResult,
    TIIVerdict,
    TelegramIntimacyIndexRow,
    VOICE_RATIO_MULTIPLIER,
    ClientMessageStats,
)


class TIICalculator:
    """Computes the 6-component Telegram Intimacy Index.

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
                f"{TIIError.INVALID_COACH_ACRONYM.value}: "
                f"'{coach_acronym}' length must be 2-4."
            )
        self._coach = coach_acronym
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ── public — calculate single client ────────────────────────────

    def calculate(
        self, stats: ClientMessageStats
    ) -> TelegramIntimacyIndexRow:
        """Calculate TII for a single client from message stats.

        If stats contain zero activity, all scores resolve to 0.0
        (no ZeroDivisionError) per spec §6 backward compatibility.
        """
        scores = self._compute_components(stats)
        composite = self._composite(scores)
        psr = self._classify_psr(composite)
        now = datetime.now(timezone.utc).isoformat()
        tii_id = str(uuid.uuid4())

        row = TelegramIntimacyIndexRow(
            tii_id=tii_id,
            client_id=stats.client_id,
            coach_id=self._coach_id,
            interaction_frequency_score=scores.interaction_frequency_score,
            consistency_score=scores.consistency_score,
            disclosure_depth_score=scores.disclosure_depth_score,
            response_latency_score=scores.response_latency_score,
            voice_note_ratio_score=scores.voice_note_ratio_score,
            initiative_frequency_score=scores.initiative_frequency_score,
            composite_tii=composite,
            psr_stage=psr,
            last_computed=now,
        )

        self._rc.log(
            agent_id="telegram-intimacy-calculator",
            action="tii-calculate",
            asset_id=tii_id,
            person_id=stats.client_id,
            input_summary=f"msgs={stats.message_count} days_active={stats.days_active_in_last_30}",
            output_summary=f"composite_tii={composite:.4f} psr={psr}",
            metadata={
                "coach": self._coach,
                "client_id": stats.client_id,
                "composite_tii": round(composite, 4),
                "psr_stage": psr,
            },
        )

        return row

    # ── public — batch calculate ────────────────────────────────────

    def calculate_batch(
        self, clients: list[ClientMessageStats]
    ) -> list[TelegramIntimacyIndexRow]:
        """Calculate TII for a batch of clients."""
        return [self.calculate(c) for c in clients]

    # ── public — TII gate evaluation (§4 Stage 2) ──────────────────

    def evaluate_gate(
        self, client_id: str, composite_tii: float, consistency_score: float
    ) -> TIIGateResult:
        """Evaluate the TII Delivery Threshold Gate.

        Verdicts:
          PASS:        composite_tii >= 0.4
          PROVISIONAL: 0.3 <= composite_tii < 0.4 AND consistency > 0.8
          FAIL:        composite_tii < 0.3
        """
        now = datetime.now(timezone.utc).isoformat()

        if composite_tii >= TII_PASS_THRESHOLD:
            verdict = TIIVerdict.PASS.value
            alert = None
        elif (
            composite_tii >= TII_PROVISIONAL_FLOOR
            and composite_tii < TII_PASS_THRESHOLD
            and consistency_score > TII_PROVISIONAL_CONSISTENCY
        ):
            verdict = TIIVerdict.PROVISIONAL.value
            alert = (
                "Ready for manual Deep Disclosure / Voice Note connection "
                "rather than automated funnel block."
            )
        else:
            verdict = TIIVerdict.FAIL.value
            alert = None

        return TIIGateResult(
            client_id=client_id,
            coach_id=self._coach_id,
            composite_tii=round(composite_tii, 4),
            consistency_score=round(consistency_score, 4),
            verdict=verdict,
            operator_alert=alert,
            last_evaluated=now,
        )

    # ── internal — component calculations (§4 Stage 4) ─────────────

    def _compute_components(
        self, stats: ClientMessageStats
    ) -> TIIComponentScores:
        """Compute the 6 individual TII component scores.

        All scores clamped to [0.0, 1.0].
        All division-by-zero cases safely resolve to 0.0.
        """
        # interaction_frequency_score = (Message_Count / 30) / Max_Expected_Frequency
        freq_raw = (stats.message_count / TII_WINDOW_DAYS) / MAX_EXPECTED_FREQUENCY
        freq = min(freq_raw, 1.0)

        # consistency_score = Days_Active_In_Last_30 / 30
        consistency = stats.days_active_in_last_30 / TII_WINDOW_DAYS

        # disclosure_depth_score = spt_stage / 4.0
        disclosure = stats.spt_stage / 4.0

        # response_latency_score = (24h - min(24h, avg_response_time)) / 24h
        clamped_latency = min(MAX_LATENCY_HOURS, stats.avg_response_time_hours)
        latency = (MAX_LATENCY_HOURS - clamped_latency) / MAX_LATENCY_HOURS

        # voice_note_ratio_score = (Voice_Message_Count / Total_Client_Messages) * 2.0
        if stats.total_client_messages > 0:
            voice_raw = (stats.voice_message_count / stats.total_client_messages) * VOICE_RATIO_MULTIPLIER
        else:
            voice_raw = 0.0
        voice = min(voice_raw, 1.0)

        # initiative_frequency_score = Days_Client_Initiated / Days_Active_In_Last_30
        if stats.days_active_in_last_30 > 0:
            init_raw = stats.days_client_initiated / stats.days_active_in_last_30
        else:
            init_raw = 0.0
        initiative = min(init_raw, 1.0)

        return TIIComponentScores(
            interaction_frequency_score=round(freq, 4),
            consistency_score=round(consistency, 4),
            disclosure_depth_score=round(disclosure, 4),
            response_latency_score=round(latency, 4),
            voice_note_ratio_score=round(voice, 4),
            initiative_frequency_score=round(initiative, 4),
        )

    # ── internal — composite weighted average ──────────────────────

    def _composite(self, scores: TIIComponentScores) -> float:
        """Weighted average per §4 Stage 4."""
        composite = (
            TII_WEIGHT_FREQUENCY * scores.interaction_frequency_score
            + TII_WEIGHT_CONSISTENCY * scores.consistency_score
            + TII_WEIGHT_DISCLOSURE * scores.disclosure_depth_score
            + TII_WEIGHT_LATENCY * scores.response_latency_score
            + TII_WEIGHT_VOICE * scores.voice_note_ratio_score
            + TII_WEIGHT_INITIATIVE * scores.initiative_frequency_score
        )
        return round(min(composite, 1.0), 4)

    # ── internal — PSR stage classification (§4 Stage 3) ───────────

    def _classify_psr(self, composite_tii: float) -> str:
        """Map composite TII to Parasocial Relationship stage."""
        if composite_tii >= PSR_BORDERLINE_THRESHOLD:
            return PSRStage.BORDERLINE.value
        elif composite_tii >= PSR_INTENSE_PERSONAL_THRESHOLD:
            return PSRStage.INTENSE_PERSONAL.value
        else:
            return PSRStage.ENTERTAINMENT_SOCIAL.value
