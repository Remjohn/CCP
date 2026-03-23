"""
FR-CBCS-04 — Information Coping Trajectory Mapper
===================================================
Individual 5-position classification from LIWC-22 markers + tribe-level
aggregation with minimum-sample quality gate.

Spec ref: FR_CBCS_04_Information_Coping_Trajectory_Mapper_Tech_Spec.md
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from statistics import median

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    CONTENT_ARCHETYPE_MAP,
    ICT_ANXIETY_THRESHOLD,
    ICT_COGNITIVE_PROCESSES_THRESHOLD_HIGH,
    ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW,
    ICT_FUTURE_FOCUS_THRESHOLD,
    ICT_INFORMATION_SEEKING_THRESHOLD,
    ICT_INSIGHT_THRESHOLD_HIGH,
    ICT_INSIGHT_THRESHOLD_LOW,
    ICT_INTERACTION_FREQ_THRESHOLD,
    ICT_NEGATIVE_EMOTION_THRESHOLD,
    ICT_POSITION_4_SUSTAINED_DAYS,
    ICT_POSITIVE_EMOTION_THRESHOLD,
    ICT_SOCIAL_WORDS_THRESHOLD,
    ICTError,
    ICTLiwcScores,
    InformationCopingTrajectoryRow,
    POSITION_LABEL_MAP,
    PositionDistribution,
    TRIBE_DEFAULT_POSITION,
    TRIBE_SAMPLE_PASS_THRESHOLD,
    TribeGateVerdict,
    TribeIctSnapshotRow,
)


class ICTMapper:
    """Classifies individual clients into 5 Information Coping positions.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(ICTError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Individual Classification ──────────────────────────────────────

    def classify_client(
        self,
        client_id: str,
        coach_id: str,
        liwc_scores: ICTLiwcScores,
        interaction_freq_per_week: float = 2.0,
        days_at_position_4: int = 0,
    ) -> InformationCopingTrajectoryRow:
        """Classify a single client into position 1-5 (§4 Stage 1-2).

        Parameters
        ----------
        client_id : str
            Unique client identifier.
        coach_id : str
            Coach boundary (ADR-01).
        liwc_scores : ICTLiwcScores
            LIWC-22 marker set for trailing 7-day window.
        interaction_freq_per_week : float
            Average CBCS interactions per week. Defaults to 2.0 (safe).
        days_at_position_4 : int
            Consecutive days client has sustained Position 4.
        """
        position, conditions_met, conditions_total = self._evaluate_position(
            liwc_scores, interaction_freq_per_week, days_at_position_4
        )
        confidence = conditions_met / conditions_total if conditions_total > 0 else 0.0

        row = InformationCopingTrajectoryRow(
            ict_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=coach_id,
            position=position,
            position_label=POSITION_LABEL_MAP[position],
            liwc_markers_snapshot=liwc_scores.model_dump(),
            classification_confidence=round(confidence, 4),
            last_updated=datetime.now(timezone.utc).isoformat(),
        )

        self._rc.log(
            agent_id="ict-mapper",
            action="ict-classify",
            asset_id=row.ict_id,
            person_id=client_id,
            input_summary=f"liwc:{len(liwc_scores.model_dump())} fields",
            output_summary=f"position={position} ({POSITION_LABEL_MAP[position]}), confidence={confidence:.4f}",
        )
        return row

    # ── Position Evaluation (§4 Stage 2) ──────────────────────────────

    @staticmethod
    def _evaluate_position(
        s: ICTLiwcScores,
        interaction_freq: float,
        days_at_p4: int,
    ) -> tuple[int, int, int]:
        """Top-down sequential evaluation, highest match takes priority.

        Returns (position, conditions_met, total_conditions_for_position).
        """
        # Position 5 — Information Donor (3 conditions)
        p5_conds = [
            s.social_words > ICT_SOCIAL_WORDS_THRESHOLD,
            s.insight > ICT_INSIGHT_THRESHOLD_HIGH,
            days_at_p4 > ICT_POSITION_4_SUSTAINED_DAYS,
        ]
        if all(p5_conds):
            return 5, sum(p5_conds), len(p5_conds)

        # Position 4 — Information Health (3 conditions)
        p4_conds = [
            s.cognitive_processes > ICT_COGNITIVE_PROCESSES_THRESHOLD_HIGH,
            s.positive_emotion > ICT_POSITIVE_EMOTION_THRESHOLD,
            s.insight > ICT_INSIGHT_THRESHOLD_LOW,
        ]
        if all(p4_conds):
            return 4, sum(p4_conds), len(p4_conds)

        # Position 3 — Needs Injection (2 conditions)
        p3_conds = [
            s.information_seeking > ICT_INFORMATION_SEEKING_THRESHOLD,
            s.future_focus > ICT_FUTURE_FOCUS_THRESHOLD,
        ]
        if all(p3_conds):
            return 3, sum(p3_conds), len(p3_conds)

        # Position 2 — Ill-Informed (2 conditions)
        p2_conds = [
            s.cognitive_processes < ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW,
            s.anxiety > ICT_ANXIETY_THRESHOLD,
        ]
        if all(p2_conds):
            return 2, sum(p2_conds), len(p2_conds)

        # Position 1 — Deficiency (3 conditions)
        p1_conds = [
            s.cognitive_processes < ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW,
            s.negative_emotion > ICT_NEGATIVE_EMOTION_THRESHOLD,
            interaction_freq < ICT_INTERACTION_FREQ_THRESHOLD,
        ]
        if all(p1_conds):
            return 1, sum(p1_conds), len(p1_conds)

        # Fallback → Position 2 (§4 Stage 2, safest default)
        # Confidence for fallback: count how many P2 conditions were met
        return 2, sum(p2_conds), len(p2_conds)

    # ── Batch Classification ──────────────────────────────────────────

    def classify_batch(
        self,
        clients: list[
            tuple[str, str, ICTLiwcScores, float, int]
        ],
    ) -> list[InformationCopingTrajectoryRow]:
        """Classify a list of (client_id, coach_id, liwc, freq, days_at_p4)."""
        return [
            self.classify_client(cid, coid, liwc, freq, days)
            for cid, coid, liwc, freq, days in clients
        ]


class TribeICTAggregator:
    """Aggregates individual ICT positions into a tribe snapshot.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(ICTError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Tribe Aggregation (§4 Stage 3) ─────────────────────────────────

    def aggregate(
        self,
        coach_id: str,
        individual_rows: list[InformationCopingTrajectoryRow],
    ) -> tuple[TribeIctSnapshotRow, TribeGateVerdict]:
        """Compute tribe snapshot from individual classifications.

        Returns
        -------
        tuple[TribeIctSnapshotRow, TribeGateVerdict]
            The snapshot row and the quality gate verdict.
        """
        active_count = len(individual_rows)

        # ── Gate evaluation ────────────────────────────────────────────
        if active_count == 0:
            verdict = TribeGateVerdict.FAIL
            agg_position = TRIBE_DEFAULT_POSITION
            dist = PositionDistribution()
        elif active_count < TRIBE_SAMPLE_PASS_THRESHOLD:
            verdict = TribeGateVerdict.PROVISIONAL
            positions = [r.position for r in individual_rows]
            agg_position = int(median(positions))
            dist = self._compute_distribution(positions)
        else:
            verdict = TribeGateVerdict.PASS
            positions = [r.position for r in individual_rows]
            dist = self._compute_distribution(positions)
            agg_position = self._majority_position(dist)

        archetype = self._resolve_archetype(agg_position)

        snapshot = TribeIctSnapshotRow(
            snapshot_id=str(uuid.uuid4()),
            coach_id=coach_id,
            aggregate_position=agg_position,
            position_distribution=dist,
            recommended_content_archetype=archetype,
            computed_date=datetime.now(timezone.utc).isoformat(),
        )

        self._rc.log(
            agent_id="tribe-ict-aggregator",
            action="tribe-ict-aggregate",
            asset_id=snapshot.snapshot_id,
            input_summary=f"active_clients={active_count}",
            output_summary=(
                f"verdict={verdict.value}, agg_position={agg_position}, "
                f"archetype={archetype}"
            ),
        )
        return snapshot, verdict

    # ── Distribution Computation ───────────────────────────────────────

    @staticmethod
    def _compute_distribution(positions: list[int]) -> PositionDistribution:
        """Compute COUNT(position=X) / TOTAL_COUNT for each bucket."""
        total = len(positions)
        if total == 0:
            return PositionDistribution()
        counts = {i: 0 for i in range(1, 6)}
        for p in positions:
            counts[p] = counts.get(p, 0) + 1
        return PositionDistribution(
            p1=round(counts[1] / total, 4),
            p2=round(counts[2] / total, 4),
            p3=round(counts[3] / total, 4),
            p4=round(counts[4] / total, 4),
            p5=round(counts[5] / total, 4),
        )

    @staticmethod
    def _majority_position(dist: PositionDistribution) -> int:
        """Return position with largest share; tie-break → lower number."""
        shares = {
            1: dist.p1,
            2: dist.p2,
            3: dist.p3,
            4: dist.p4,
            5: dist.p5,
        }
        max_share = max(shares.values())
        # Tie-break: lowest position wins (conservative bias per §4 Stage 4)
        for pos in sorted(shares):
            if shares[pos] == max_share:
                return pos
        return TRIBE_DEFAULT_POSITION  # pragma: no cover — unreachable

    @staticmethod
    def _resolve_archetype(agg_position: int) -> str:
        """Map aggregate position to content archetype string (§4 Stage 4)."""
        if agg_position <= 2:
            return CONTENT_ARCHETYPE_MAP["low"]
        if agg_position == 3:
            return CONTENT_ARCHETYPE_MAP["mid"]
        return CONTENT_ARCHETYPE_MAP["high"]
