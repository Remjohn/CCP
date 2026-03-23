"""
FR60 — Loom Report Generation: Integration Tests
=================================================
Covers:
- ConversionSignalDetector (spike / crash math, §10 unit test table)
- ActionableThresholdGate (all 3 verdicts, blacklist, vague detection)
- LoomIntelligenceTranslator.generate (happy-path, provisional, hard-fail, receipts)
- Acceptance Criteria AC1-AC3 (verbatim from spec)
- LoomSections / LoomNarrativeReportRow field structure
- coach_id ADR-01 guard
"""

from __future__ import annotations

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    LoomGateVerdict,
    LoomNarrativeReportRow,
    LoomReportError,
    LoomSections,
)
from src.ccp.services.loom_report_generator import (
    CRASH_DIVISOR,
    SPIKE_MULTIPLIER,
    ActionableThresholdGate,
    ConversionSignalDetector,
    LoomIntelligenceTranslator,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def rc(tmp_path):
    return ReceiptChain(coach_acronym="TST", log_dir=tmp_path)


@pytest.fixture()
def translator(rc):
    return LoomIntelligenceTranslator(coach_id="coachA", receipt_chain=rc)


CAMPAIGN_ID = "exec-0001-0000-0000-000000000001"
GOOD_REC = "Group A showed 30% conversion vs 10% baseline — recommend replicating identity anchor at Day 1."
VAGUE_REC = "Some clients did well this cycle."
HALLU_REC = "Try running Facebook ads to boost reach."


# ---------------------------------------------------------------------------
# ConversionSignalDetector — spike / crash math
# ---------------------------------------------------------------------------

class TestConversionSignalDetector:

    def test_spike_detected_above_threshold(self):
        """§10: baseline=1.0, group_a=3.5 → spike_detected=True."""
        det = ConversionSignalDetector(1.0, 3.5, 0.5)
        assert det.spike_detected() is True

    def test_spike_not_detected_at_threshold(self):
        """group_a == baseline * 1.5 is NOT > so no spike."""
        det = ConversionSignalDetector(1.0, 1.5, 0.8)
        assert det.spike_detected() is False

    def test_spike_not_detected_below_threshold(self):
        det = ConversionSignalDetector(0.10, 0.12, 0.08)
        assert det.spike_detected() is False

    def test_crash_detected_below_threshold(self):
        """baseline=1.0, group_b=0.3 < 1.0/2.0=0.5 → crash_detected=True."""
        det = ConversionSignalDetector(1.0, 0.5, 0.3)
        assert det.crash_detected() is True

    def test_crash_not_detected_at_half_baseline(self):
        """group_b == baseline / 2.0 is NOT < so no crash."""
        det = ConversionSignalDetector(1.0, 1.0, 0.5)
        assert det.crash_detected() is False

    def test_crash_not_detected_above_half_baseline(self):
        det = ConversionSignalDetector(0.10, 0.10, 0.06)
        assert det.crash_detected() is False

    def test_zero_baseline_no_spike(self):
        """Zero baseline → no spike (guard against division by zero)."""
        det = ConversionSignalDetector(0.0, 999.0, 0.0)
        assert det.spike_detected() is False

    def test_zero_baseline_no_crash(self):
        det = ConversionSignalDetector(0.0, 0.0, 0.0)
        assert det.crash_detected() is False

    def test_spike_and_crash_simultaneously(self):
        """Group A spikes, Group B crashes — both can be True."""
        det = ConversionSignalDetector(0.10, 0.20, 0.02)
        assert det.spike_detected() is True
        assert det.crash_detected() is True

    def test_build_signal_text_contains_numbers(self):
        det = ConversionSignalDetector(0.10, 0.20, 0.02)
        text = det.build_signal_text()
        import re
        assert re.search(r"\d", text), "Signal text must contain numeric data"

    def test_build_signal_text_no_anomaly_mentions_baseline(self):
        """No spike, no crash → neutral text still includes baseline numbers."""
        det = ConversionSignalDetector(0.10, 0.11, 0.08)
        text = det.build_signal_text()
        assert "10%" in text or "0.10" in text or "10" in text

    def test_spec_unit_test_math_ratio(self):
        """
        §10 Test_Conversion_Math_Ratio_Detection:
        baseline=1.0, group_a=3.5 → spike_detected=True.
        """
        det = ConversionSignalDetector(baseline_conversion=1.0, group_a_conversion=3.5, group_b_conversion=0.5)
        assert det.spike_detected() is True


# ---------------------------------------------------------------------------
# ActionableThresholdGate — all 3 verdicts
# ---------------------------------------------------------------------------

class TestActionableThresholdGate:

    def test_pass_with_numeric_recommendation(self):
        rec = "30% of Tier 2 clients converted — replicate Day 1 anchor sequence."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.PASS

    def test_pass_with_percentage_reference(self):
        rec = "Group A achieved 45% vs 10% baseline. Recommend identity anchoring."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.PASS

    def test_provisional_vague_no_numbers(self):
        """AC2: No digits → PROVISIONAL_VAGUE_SUMMARY."""
        assert ActionableThresholdGate(VAGUE_REC).evaluate() == LoomGateVerdict.PROVISIONAL_VAGUE_SUMMARY

    def test_provisional_all_words_no_digits(self):
        rec = "Clients appeared to respond well to identity messaging overall."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.PROVISIONAL_VAGUE_SUMMARY

    def test_fail_facebook_ads(self):
        """AC1: 'Facebook ads' → FAIL_HALLUCINATED_ADVICE."""
        rec = "Try running Facebook ads to boost reach."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE

    def test_fail_instagram_traffic(self):
        rec = "You really need more Instagram traffic to convert."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE

    def test_fail_tiktok_campaigns(self):
        rec = "Launch TikTok campaigns to reach under-25 segment."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE

    def test_fail_clickfunnels(self):
        rec = "Move funnels to Clickfunnels for a better conversion rate."
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE

    def test_fail_takes_precedence_over_provisional(self):
        """Blacklisted term even with no numbers → FAIL (not PROVISIONAL)."""
        rec = "Run Facebook ads for better reach."  # no digits
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE

    def test_spec_regex_sanitization(self):
        """
        §10 Test_Regex_Dictionary_Sanitization:
        'You really need more Instagram traffic' → FAIL_HALLUCINATED_ADVICE.
        """
        rec = "You really need more Instagram traffic"
        assert ActionableThresholdGate(rec).evaluate() == LoomGateVerdict.FAIL_HALLUCINATED_ADVICE


# ---------------------------------------------------------------------------
# Acceptance Criteria (verbatim from spec §8)
# ---------------------------------------------------------------------------

class TestAcceptanceCriteria:

    def test_ac1_hallucination_rejection(self, translator):
        """AC1: 'Try running TikTok ad campaigns' → FAIL_HALLUCINATED_ADVICE."""
        with pytest.raises(ValueError) as exc_info:
            translator.generate(
                campaign_execution_id=CAMPAIGN_ID,
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.08,
                summary_block="Campaign summary.",
                actionable_recommendation_block="Try running TikTok ad campaigns.",
            )
        assert LoomReportError.FAIL_HALLUCINATED_ADVICE in str(exc_info.value)

    def test_ac2_provisional_vague_summary(self, translator):
        """AC2: No numeric data → PROVISIONAL_VAGUE_SUMMARY."""
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.11,
            group_b_conversion=0.09,
            summary_block="Campaign completed.",
            actionable_recommendation_block=VAGUE_REC,
        )
        assert row.gate_verdict == LoomGateVerdict.PROVISIONAL_VAGUE_SUMMARY.value

    def test_ac3_three_sections_in_report(self, translator):
        """AC3: All 3 loom_sections populated (psychological_signal_block not empty)."""
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.25,
            group_b_conversion=0.03,
            summary_block="Campaign achieved above-baseline results.",
            actionable_recommendation_block=GOOD_REC,
        )
        assert isinstance(row.loom_sections, LoomSections)
        assert row.loom_sections.summary_block
        assert row.loom_sections.psychological_signal_block
        assert row.loom_sections.actionable_recommendation_block


# ---------------------------------------------------------------------------
# LoomIntelligenceTranslator — row structure
# ---------------------------------------------------------------------------

class TestLoomNarrativeReportRow:

    def test_pass_row_fields(self, translator):
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary text.",
            actionable_recommendation_block=GOOD_REC,
        )
        assert isinstance(row, LoomNarrativeReportRow)
        assert row.campaign_execution_id == CAMPAIGN_ID
        assert row.coach_id == "coachA"
        assert row.gate_verdict == LoomGateVerdict.PASS.value
        assert row.report_id  # non-empty UUID
        assert row.computation_timestamp  # non-empty ISO

    def test_report_id_is_uuid(self, translator):
        import uuid as _uuid
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary.",
            actionable_recommendation_block=GOOD_REC,
        )
        _uuid.UUID(row.report_id)

    def test_timestamp_is_iso_with_tz(self, translator):
        from datetime import datetime
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary.",
            actionable_recommendation_block=GOOD_REC,
        )
        dt = datetime.fromisoformat(row.computation_timestamp)
        assert dt.tzinfo is not None

    def test_provisional_row_gate_verdict(self, translator):
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.11,
            group_b_conversion=0.09,
            summary_block="Flat campaign.",
            actionable_recommendation_block=VAGUE_REC,
        )
        assert row.gate_verdict == LoomGateVerdict.PROVISIONAL_VAGUE_SUMMARY.value

    def test_psychological_signal_block_contains_numbers(self, translator):
        """Signal block must contain numeric evidence (spec §4 anti-hallucination)."""
        import re
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary.",
            actionable_recommendation_block=GOOD_REC,
        )
        assert re.search(r"\d", row.loom_sections.psychological_signal_block)

    def test_spike_signal_reflected_in_report(self, translator):
        """When spike detected, signal block should mention spike."""
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.25,
            group_b_conversion=0.08,
            summary_block="S",
            actionable_recommendation_block=GOOD_REC,
        )
        assert "SPIKE" in row.loom_sections.psychological_signal_block.upper() or \
               "spike" in row.loom_sections.psychological_signal_block.lower()

    def test_crash_signal_reflected_in_report(self, translator):
        row = translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.11,
            group_b_conversion=0.02,
            summary_block="S",
            actionable_recommendation_block=GOOD_REC,
        )
        assert "CRASH" in row.loom_sections.psychological_signal_block.upper() or \
               "crash" in row.loom_sections.psychological_signal_block.lower()


# ---------------------------------------------------------------------------
# Receipt chain entries
# ---------------------------------------------------------------------------

class TestLoomReportReceipts:

    def test_pass_logs_two_receipts(self, rc, translator):
        translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary.",
            actionable_recommendation_block=GOOD_REC,
        )
        assert len(rc.query(action="loom-narrative-resolve")) >= 1
        assert len(rc.query(action="loom-threshold-gate")) >= 1

    def test_fail_logs_receipts_before_raising(self, rc, translator):
        with pytest.raises(ValueError):
            translator.generate(
                campaign_execution_id=CAMPAIGN_ID,
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.04,
                summary_block="Summary.",
                actionable_recommendation_block=HALLU_REC,
            )
        assert len(rc.query(action="loom-narrative-resolve")) >= 1
        gate_entries = rc.query(action="loom-threshold-gate")
        assert any("FAIL_HALLUCINATED_ADVICE" in e.output_summary for e in gate_entries)

    def test_provisional_logs_two_receipts(self, rc, translator):
        translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.11,
            group_b_conversion=0.09,
            summary_block="Summary.",
            actionable_recommendation_block=VAGUE_REC,
        )
        assert len(rc.query(action="loom-narrative-resolve")) >= 1
        assert len(rc.query(action="loom-threshold-gate")) >= 1

    def test_receipt_contains_coach_id(self, rc, translator):
        translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary.",
            actionable_recommendation_block=GOOD_REC,
        )
        entries = rc.query(action="loom-narrative-resolve")
        assert any("coachA" in e.output_summary for e in entries)

    def test_gate_receipt_has_parent_id(self, rc, translator):
        translator.generate(
            campaign_execution_id=CAMPAIGN_ID,
            baseline_conversion=0.10,
            group_a_conversion=0.20,
            group_b_conversion=0.04,
            summary_block="Summary.",
            actionable_recommendation_block=GOOD_REC,
        )
        gate_entries = rc.query(action="loom-threshold-gate")
        assert all(e.parent_receipt_id is not None for e in gate_entries)


# ---------------------------------------------------------------------------
# Hard-abort behaviour
# ---------------------------------------------------------------------------

class TestHardAbortBehaviour:

    def test_raises_value_error_on_hallucination(self, translator):
        with pytest.raises(ValueError):
            translator.generate(
                campaign_execution_id=CAMPAIGN_ID,
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.04,
                summary_block="Summary.",
                actionable_recommendation_block="Use Google Ads for maximum ROI.",
            )

    def test_error_contains_fail_hallucinated_advice(self, translator):
        with pytest.raises(ValueError) as exc_info:
            translator.generate(
                campaign_execution_id=CAMPAIGN_ID,
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.04,
                summary_block="S.",
                actionable_recommendation_block="Run paid social campaigns now.",
            )
        assert "FAIL_HALLUCINATED_ADVICE" in str(exc_info.value)

    def test_no_row_on_hallucination(self, translator):
        result = None
        try:
            result = translator.generate(
                campaign_execution_id=CAMPAIGN_ID,
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.04,
                summary_block="S.",
                actionable_recommendation_block=HALLU_REC,
            )
        except ValueError:
            pass
        assert result is None


# ---------------------------------------------------------------------------
# ADR-01 coach_id guard
# ---------------------------------------------------------------------------

class TestCoachIdGuard:

    def test_short_coach_id_raises(self, rc):
        with pytest.raises(ValueError):
            LoomIntelligenceTranslator(coach_id="X", receipt_chain=rc)

    def test_empty_coach_id_raises(self, rc):
        with pytest.raises(ValueError):
            LoomIntelligenceTranslator(coach_id="", receipt_chain=rc)

    def test_valid_min_coach_id(self, rc):
        t = LoomIntelligenceTranslator(coach_id="AB", receipt_chain=rc)
        assert t is not None


# ---------------------------------------------------------------------------
# Multiple generations (receipt accumulation, unique IDs)
# ---------------------------------------------------------------------------

class TestMultipleGenerations:

    def test_unique_report_ids(self, translator):
        ids = set()
        for i in range(4):
            row = translator.generate(
                campaign_execution_id=f"exec-{i:04d}",
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.04,
                summary_block="S.",
                actionable_recommendation_block=GOOD_REC,
            )
            ids.add(row.report_id)
        assert len(ids) == 4

    def test_receipts_accumulate(self, rc, translator):
        for i in range(3):
            translator.generate(
                campaign_execution_id=f"exec-{i}",
                baseline_conversion=0.10,
                group_a_conversion=0.20,
                group_b_conversion=0.04,
                summary_block="S.",
                actionable_recommendation_block=GOOD_REC,
            )
        assert len(rc.query(action="loom-narrative-resolve")) == 3


# ---------------------------------------------------------------------------
# Backward compatibility — legacy mode produces PROVISIONAL_VAGUE_SUMMARY
# ---------------------------------------------------------------------------

class TestLegacyCompatibility:

    def test_legacy_mode_flat_data_produces_provisional(self, translator):
        """
        FR59 PROVISIONAL_LEGACY_MODE campaigns have no deep intelligence arrays.
        The recommendation will be vague → PROVISIONAL_VAGUE_SUMMARY.
        """
        row = translator.generate(
            campaign_execution_id="legacy-exec-001",
            baseline_conversion=0.0,  # no data
            group_a_conversion=0.0,
            group_b_conversion=0.0,
            summary_block="Legacy broadcast campaign completed.",
            actionable_recommendation_block="No significant patterns observed this cycle.",
        )
        assert row.gate_verdict == LoomGateVerdict.PROVISIONAL_VAGUE_SUMMARY.value
