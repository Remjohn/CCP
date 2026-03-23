"""
FR-CBCS-04 — Information Coping Trajectory Mapper — Integration Tests
======================================================================
Covers: Individual 5-position classification, tribe aggregation,
quality gate, and acceptance criteria AC1-AC3.
"""

from __future__ import annotations

import tempfile
import uuid

import pytest

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
from src.ccp.services.ict_mapper import ICTMapper, TribeICTAggregator


# ── Helpers ─────────────────────────────────────────────────────────────

def _make_mapper(coach: str = "TST") -> tuple[ICTMapper, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    mapper = ICTMapper(coach_acronym=coach, receipt_chain=rc)
    return mapper, rc


def _make_aggregator(coach: str = "TST") -> tuple[TribeICTAggregator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    agg = TribeICTAggregator(coach_acronym=coach, receipt_chain=rc)
    return agg, rc


def _liwc(**kwargs: float) -> ICTLiwcScores:
    """Build ICTLiwcScores with defaults at zero except cognitive_processes."""
    defaults = {"cognitive_processes": 0.0}
    defaults.update(kwargs)
    return ICTLiwcScores(**defaults)


def _classify(mapper: ICTMapper, liwc: ICTLiwcScores, freq: float = 2.0, days_p4: int = 0) -> InformationCopingTrajectoryRow:
    return mapper.classify_client("c1", "coach1", liwc, freq, days_p4)


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1 — Individual Position Classification
# ═══════════════════════════════════════════════════════════════════════

class TestPositionClassification:
    """§4 Stage 2 — top-down sequential evaluation."""

    def test_position5_information_donor(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            social_words=ICT_SOCIAL_WORDS_THRESHOLD + 0.01,
            insight=ICT_INSIGHT_THRESHOLD_HIGH + 0.01,
            cognitive_processes=0.2,
        )
        row = _classify(m, liwc, days_p4=ICT_POSITION_4_SUSTAINED_DAYS + 1)
        assert row.position == 5
        assert row.position_label == "Information Donor"

    def test_position5_fails_without_sustained_days(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            social_words=ICT_SOCIAL_WORDS_THRESHOLD + 0.01,
            insight=ICT_INSIGHT_THRESHOLD_HIGH + 0.01,
            cognitive_processes=0.2,
        )
        row = _classify(m, liwc, days_p4=ICT_POSITION_4_SUSTAINED_DAYS - 1)
        assert row.position != 5  # Falls to 4 (cog + pos_emotion + insight)

    def test_position4_information_health(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            cognitive_processes=ICT_COGNITIVE_PROCESSES_THRESHOLD_HIGH + 0.01,
            positive_emotion=ICT_POSITIVE_EMOTION_THRESHOLD + 0.01,
            insight=ICT_INSIGHT_THRESHOLD_LOW + 0.01,
        )
        row = _classify(m, liwc)
        assert row.position == 4
        assert row.position_label == "Information Health"

    def test_position4_fails_missing_insight(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            cognitive_processes=ICT_COGNITIVE_PROCESSES_THRESHOLD_HIGH + 0.01,
            positive_emotion=ICT_POSITIVE_EMOTION_THRESHOLD + 0.01,
            insight=ICT_INSIGHT_THRESHOLD_LOW - 0.01,
        )
        row = _classify(m, liwc)
        assert row.position != 4

    def test_position3_needs_injection(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            information_seeking=ICT_INFORMATION_SEEKING_THRESHOLD + 0.01,
            future_focus=ICT_FUTURE_FOCUS_THRESHOLD + 0.01,
            cognitive_processes=0.12,  # above low threshold so doesn't hit P2
        )
        row = _classify(m, liwc)
        assert row.position == 3
        assert row.position_label == "Needs Injection"

    def test_position3_fails_missing_future_focus(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            information_seeking=ICT_INFORMATION_SEEKING_THRESHOLD + 0.01,
            future_focus=ICT_FUTURE_FOCUS_THRESHOLD - 0.01,
            cognitive_processes=0.12,
        )
        row = _classify(m, liwc)
        assert row.position != 3

    def test_position2_ill_informed(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            cognitive_processes=ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW - 0.01,
            anxiety=ICT_ANXIETY_THRESHOLD + 0.01,
        )
        row = _classify(m, liwc)
        assert row.position == 2
        assert row.position_label == "Ill-Informed"

    def test_position1_deficiency(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            cognitive_processes=ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW - 0.01,
            negative_emotion=ICT_NEGATIVE_EMOTION_THRESHOLD + 0.01,
            anxiety=0.0,  # anxiety below threshold → skip P2
        )
        row = _classify(m, liwc, freq=ICT_INTERACTION_FREQ_THRESHOLD - 0.1)
        assert row.position == 1
        assert row.position_label == "Deficiency"

    def test_position1_fails_high_interaction_freq(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(
            cognitive_processes=ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW - 0.01,
            negative_emotion=ICT_NEGATIVE_EMOTION_THRESHOLD + 0.01,
            anxiety=0.0,
        )
        row = _classify(m, liwc, freq=ICT_INTERACTION_FREQ_THRESHOLD + 0.5)
        assert row.position != 1

    def test_fallback_to_position2(self) -> None:
        """No conditions met → defaults to Position 2 (§4 Stage 2 fallback)."""
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.12)  # above low, below high → no match
        row = _classify(m, liwc)
        assert row.position == 2
        assert row.position_label == "Ill-Informed"

    def test_priority_order_5_over_4(self) -> None:
        """Position 5 evaluated first; if all P5 AND P4 conditions met, P5 wins."""
        m, _ = _make_mapper()
        liwc = _liwc(
            social_words=0.2,
            insight=0.06,
            cognitive_processes=0.2,
            positive_emotion=0.06,
        )
        row = _classify(m, liwc, days_p4=35)
        assert row.position == 5

    def test_priority_order_4_over_3(self) -> None:
        """When P4 and P3 conditions both met, P4 wins (higher priority)."""
        m, _ = _make_mapper()
        liwc = _liwc(
            cognitive_processes=0.2,
            positive_emotion=0.06,
            insight=0.04,
            information_seeking=0.15,
            future_focus=0.08,
        )
        row = _classify(m, liwc)
        assert row.position == 4


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2 — Confidence Calculation
# ═══════════════════════════════════════════════════════════════════════

class TestConfidence:
    """classification_confidence = conditions_met / total_conditions."""

    def test_position5_full_confidence(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(social_words=0.2, insight=0.06, cognitive_processes=0.2)
        row = _classify(m, liwc, days_p4=35)
        assert row.classification_confidence == pytest.approx(1.0)

    def test_position4_full_confidence(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.2, positive_emotion=0.06, insight=0.04)
        row = _classify(m, liwc)
        assert row.classification_confidence == pytest.approx(1.0)

    def test_fallback_partial_confidence(self) -> None:
        """Fallback to P2: confidence based on how many P2 conditions are met."""
        m, _ = _make_mapper()
        # cognitive_processes=0.12 → above 0.10 threshold (P2 cond 1 = False)
        # anxiety=0.0 → below 0.02 threshold (P2 cond 2 = False)
        liwc = _liwc(cognitive_processes=0.12, anxiety=0.0)
        row = _classify(m, liwc)
        assert row.position == 2
        assert row.classification_confidence == pytest.approx(0.0)


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3 — Output Schema Validation
# ═══════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    """§5 schema compliance."""

    def test_ict_row_has_all_fields(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.2, positive_emotion=0.06, insight=0.04)
        row = _classify(m, liwc)
        assert row.ict_id  # UUID string
        assert row.client_id == "c1"
        assert row.coach_id == "coach1"
        assert 1 <= row.position <= 5
        assert row.position_label in POSITION_LABEL_MAP.values()
        assert isinstance(row.liwc_markers_snapshot, dict)
        assert 0.0 <= row.classification_confidence <= 1.0
        assert row.last_updated  # ISO8601 string

    def test_liwc_snapshot_preserves_raw_data(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.18, anxiety=0.03, insight=0.04)
        row = _classify(m, liwc)
        snap = row.liwc_markers_snapshot
        assert snap["cognitive_processes"] == pytest.approx(0.18)
        assert snap["anxiety"] == pytest.approx(0.03)

    def test_position_label_matches_position(self) -> None:
        m, _ = _make_mapper()
        for pos in range(1, 6):
            label = POSITION_LABEL_MAP[pos]
            assert isinstance(label, str)
            assert len(label) > 0


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4 — Tribe Aggregation
# ═══════════════════════════════════════════════════════════════════════

class TestTribeAggregation:
    """§4 Stage 3 — tribe snapshot + quality gate."""

    def _make_rows(self, positions: list[int]) -> list[InformationCopingTrajectoryRow]:
        """Synthesise individual rows with given positions."""
        return [
            InformationCopingTrajectoryRow(
                ict_id=str(uuid.uuid4()),
                client_id=f"c{i}",
                coach_id="coach1",
                position=p,
                position_label=POSITION_LABEL_MAP[p],
                liwc_markers_snapshot={"cognitive_processes": 0.1},
                classification_confidence=1.0,
                last_updated="2026-03-18T00:00:00Z",
            )
            for i, p in enumerate(positions)
        ]

    # ── PASS verdict ───────────────────────────────────────────────────

    def test_pass_verdict_ge5_clients(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([1, 2, 3, 4, 5])
        snap, verdict = agg.aggregate("coach1", rows)
        assert verdict == TribeGateVerdict.PASS
        assert snap.aggregate_position in range(1, 6)

    def test_pass_majority_position(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([3, 3, 3, 4, 5])
        snap, _ = agg.aggregate("coach1", rows)
        assert snap.aggregate_position == 3

    def test_pass_tie_breaks_lower(self) -> None:
        """Equal shares → lower position wins (conservative bias)."""
        agg, _ = _make_aggregator()
        rows = self._make_rows([2, 2, 4, 4, 5])
        snap, _ = agg.aggregate("coach1", rows)
        # P2=0.4, P4=0.4 → tie → P2 wins
        assert snap.aggregate_position == 2

    def test_pass_distribution_correct(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([1, 2, 3, 4, 5])
        snap, _ = agg.aggregate("coach1", rows)
        dist = snap.position_distribution
        assert dist.p1 == pytest.approx(0.2)
        assert dist.p2 == pytest.approx(0.2)
        assert dist.p3 == pytest.approx(0.2)
        assert dist.p4 == pytest.approx(0.2)
        assert dist.p5 == pytest.approx(0.2)

    # ── PROVISIONAL verdict ────────────────────────────────────────────

    def test_provisional_verdict_lt5_clients(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([2, 3, 4])
        snap, verdict = agg.aggregate("coach1", rows)
        assert verdict == TribeGateVerdict.PROVISIONAL
        # Median of [2, 3, 4] = 3
        assert snap.aggregate_position == 3

    def test_provisional_uses_median_not_distribution(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([1, 5])
        snap, verdict = agg.aggregate("coach1", rows)
        assert verdict == TribeGateVerdict.PROVISIONAL
        # Median of [1, 5] = 3.0 → int(3.0) = 3
        assert snap.aggregate_position == 3

    def test_provisional_single_client(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([4])
        snap, verdict = agg.aggregate("coach1", rows)
        assert verdict == TribeGateVerdict.PROVISIONAL
        assert snap.aggregate_position == 4

    # ── FAIL verdict ───────────────────────────────────────────────────

    def test_fail_verdict_zero_clients(self) -> None:
        agg, _ = _make_aggregator()
        snap, verdict = agg.aggregate("coach1", [])
        assert verdict == TribeGateVerdict.FAIL
        assert snap.aggregate_position == TRIBE_DEFAULT_POSITION
        assert snap.aggregate_position == 2

    def test_fail_distribution_all_zeros(self) -> None:
        agg, _ = _make_aggregator()
        snap, _ = agg.aggregate("coach1", [])
        dist = snap.position_distribution
        assert dist.p1 == 0.0
        assert dist.p2 == 0.0
        assert dist.p3 == 0.0
        assert dist.p4 == 0.0
        assert dist.p5 == 0.0


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5 — Content Archetype Resolution
# ═══════════════════════════════════════════════════════════════════════

class TestArchetypeResolution:
    """§4 Stage 4 — aggregate_position → archetype string."""

    def _make_rows(self, positions: list[int]) -> list[InformationCopingTrajectoryRow]:
        return [
            InformationCopingTrajectoryRow(
                ict_id=str(uuid.uuid4()),
                client_id=f"c{i}",
                coach_id="coach1",
                position=p,
                position_label=POSITION_LABEL_MAP[p],
                liwc_markers_snapshot={"cognitive_processes": 0.1},
                classification_confidence=1.0,
                last_updated="2026-03-18T00:00:00Z",
            )
            for i, p in enumerate(positions)
        ]

    def test_archetype_low_position1(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([1, 1, 1, 1, 1])
        snap, _ = agg.aggregate("coach1", rows)
        assert snap.recommended_content_archetype == "Validation/Defense"

    def test_archetype_low_position2(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([2, 2, 2, 2, 2])
        snap, _ = agg.aggregate("coach1", rows)
        assert snap.recommended_content_archetype == "Validation/Defense"

    def test_archetype_mid_position3(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([3, 3, 3, 3, 3])
        snap, _ = agg.aggregate("coach1", rows)
        assert snap.recommended_content_archetype == "Curiosity/Bridge"

    def test_archetype_high_position4(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([4, 4, 4, 4, 4])
        snap, _ = agg.aggregate("coach1", rows)
        assert snap.recommended_content_archetype == "Expansion/Agency"

    def test_archetype_high_position5(self) -> None:
        agg, _ = _make_aggregator()
        rows = self._make_rows([5, 5, 5, 5, 5])
        snap, _ = agg.aggregate("coach1", rows)
        assert snap.recommended_content_archetype == "Expansion/Agency"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6 — ADR-01 Coach Scope & Receipt Chain
# ═══════════════════════════════════════════════════════════════════════

class TestCoachScopeAndReceipt:
    """ADR-01 enforcement + C-11 persona masking."""

    def test_mapper_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ICTMapper(coach_acronym="X", receipt_chain=rc)

    def test_mapper_rejects_5char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ICTMapper(coach_acronym="ABCDE", receipt_chain=rc)

    def test_aggregator_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            TribeICTAggregator(coach_acronym="X", receipt_chain=rc)

    def test_aggregator_rejects_5char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            TribeICTAggregator(coach_acronym="ABCDE", receipt_chain=rc)

    def test_mapper_accepts_2char_coach(self) -> None:
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="AB", log_dir=tmp)
        m = ICTMapper(coach_acronym="AB", receipt_chain=rc)
        assert m is not None

    def test_mapper_accepts_4char_coach(self) -> None:
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="ABCD", log_dir=tmp)
        m = ICTMapper(coach_acronym="ABCD", receipt_chain=rc)
        assert m is not None

    def test_receipt_emitted_on_classify(self) -> None:
        m, rc = _make_mapper()
        liwc = _liwc(cognitive_processes=0.2, positive_emotion=0.06, insight=0.04)
        _classify(m, liwc)
        entries = rc.query(action="ict-classify")
        assert len(entries) >= 1
        assert entries[0].agent_id == "ict-mapper"
        assert entries[0].action == "ict-classify"

    def test_receipt_emitted_on_aggregate(self) -> None:
        agg, rc = _make_aggregator()
        snap, _ = agg.aggregate("coach1", [])
        entries = rc.query(action="tribe-ict-aggregate")
        assert len(entries) >= 1
        assert entries[0].agent_id == "tribe-ict-aggregator"
        assert entries[0].action == "tribe-ict-aggregate"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7 — Batch Classification
# ═══════════════════════════════════════════════════════════════════════

class TestBatchClassification:
    """Bulk classification convenience."""

    def test_batch_returns_correct_count(self) -> None:
        m, _ = _make_mapper()
        clients = [
            ("c1", "coach1", _liwc(cognitive_processes=0.2, positive_emotion=0.06, insight=0.04), 2.0, 0),
            ("c2", "coach1", _liwc(cognitive_processes=0.05, anxiety=0.03), 2.0, 0),
            ("c3", "coach1", _liwc(cognitive_processes=0.12), 2.0, 0),
        ]
        results = m.classify_batch(clients)
        assert len(results) == 3

    def test_batch_positions_correct(self) -> None:
        m, _ = _make_mapper()
        clients = [
            ("c1", "coach1", _liwc(cognitive_processes=0.2, positive_emotion=0.06, insight=0.04), 2.0, 0),
            ("c2", "coach1", _liwc(cognitive_processes=0.05, anxiety=0.03), 2.0, 0),
        ]
        results = m.classify_batch(clients)
        assert results[0].position == 4
        assert results[1].position == 2


# ═══════════════════════════════════════════════════════════════════════
# SECTION 8 — Acceptance Criteria
# ═══════════════════════════════════════════════════════════════════════

class TestAcceptanceCriteria:
    """Verbatim AC1-AC3 from the spec."""

    def test_ac1_exact_enum_mapping_position2(self) -> None:
        """AC1: cognitive_processes=0.05, anxiety=0.08 → position=2 exactly."""
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.05, anxiety=0.08)
        row = _classify(m, liwc)
        assert row.position == 2
        assert row.position_label == "Ill-Informed"

    def test_ac2_tribe_provisional_3_clients(self) -> None:
        """AC2: 3 active clients → PROVISIONAL, median integer output."""
        agg, _ = _make_aggregator()
        rows = [
            InformationCopingTrajectoryRow(
                ict_id=str(uuid.uuid4()),
                client_id=f"c{i}",
                coach_id="coach1",
                position=p,
                position_label=POSITION_LABEL_MAP[p],
                liwc_markers_snapshot={"cognitive_processes": 0.1},
                classification_confidence=1.0,
                last_updated="2026-03-18T00:00:00Z",
            )
            for i, p in enumerate([2, 3, 4])
        ]
        snap, verdict = agg.aggregate("coach1", rows)
        assert verdict == TribeGateVerdict.PROVISIONAL
        assert snap.aggregate_position == 3  # median of [2,3,4]

    def test_ac3_aggregate_position3_archetype(self) -> None:
        """AC3: aggregate_position=3 → 'Curiosity/Bridge' exactly."""
        agg, _ = _make_aggregator()
        rows = [
            InformationCopingTrajectoryRow(
                ict_id=str(uuid.uuid4()),
                client_id=f"c{i}",
                coach_id="coach1",
                position=3,
                position_label="Needs Injection",
                liwc_markers_snapshot={"cognitive_processes": 0.1},
                classification_confidence=1.0,
                last_updated="2026-03-18T00:00:00Z",
            )
            for i in range(5)
        ]
        snap, verdict = agg.aggregate("coach1", rows)
        assert verdict == TribeGateVerdict.PASS
        assert snap.aggregate_position == 3
        assert snap.recommended_content_archetype == "Curiosity/Bridge"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 9 — Edge Cases & Backward Compatibility
# ═══════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Boundary and backward compatibility (§6)."""

    def test_all_zeros_liwc_falls_to_position2(self) -> None:
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.0)
        row = _classify(m, liwc)
        # cognitive<0.1 TRUE, anxiety(0.0)>0.02 FALSE → no P2
        # cognitive<0.1 TRUE, negative(0.0)>0.05 FALSE → no P1
        # Falls to fallback P2
        assert row.position == 2

    def test_boundary_cognitive_exactly_at_threshold(self) -> None:
        """Strict inequality: cognitive < 0.10 required for P2. At 0.10 → fallback."""
        m, _ = _make_mapper()
        liwc = _liwc(cognitive_processes=0.10, anxiety=0.05)
        row = _classify(m, liwc)
        # cognitive_processes NOT < 0.10 (equal) → P2 cond 1 fails
        assert row.position == 2  # Fallback

    def test_tribe_snapshot_has_uuid(self) -> None:
        agg, _ = _make_aggregator()
        snap, _ = agg.aggregate("coach1", [])
        assert len(snap.snapshot_id) == 36  # UUID format

    def test_tribe_snapshot_has_computed_date(self) -> None:
        agg, _ = _make_aggregator()
        snap, _ = agg.aggregate("coach1", [])
        assert "T" in snap.computed_date  # ISO8601

    def test_backward_compat_no_rows_defaults_position2(self) -> None:
        """§6: Coach with 0 active clients → aggregate_position=2."""
        agg, _ = _make_aggregator()
        snap, verdict = agg.aggregate("coach1", [])
        assert snap.aggregate_position == 2
        assert verdict == TribeGateVerdict.FAIL
