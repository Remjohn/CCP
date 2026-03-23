"""
FR57 — Social Proof Intelligence Engine  (CPSC Spec 3 of 10)
=============================================================
Tests for SocialProofRetriever and RelevanceStringencyGate.
"""

from __future__ import annotations

import shutil
import tempfile
import uuid
from datetime import datetime, timezone

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    MatchTierRating,
    MatchedTestimonialPayloadRow,
    SocialProofError,
    SocialProofGateVerdict,
    TestimonialArchiveEntry,
)
from src.ccp.services.social_proof_retriever import (
    RelevanceStringencyGate,
    SocialProofRetriever,
)


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

CID = "TST"


def _make_rc_isolated() -> tuple[ReceiptChain, str]:
    tmp = tempfile.mkdtemp(prefix="fr57_rc_")
    rc = ReceiptChain(coach_acronym=CID, log_dir=tmp)
    return rc, tmp


def _entry(record_id: str, coping: int, spt: int, text: str = "Great coach!") -> TestimonialArchiveEntry:
    return TestimonialArchiveEntry(
        record_id=record_id,
        coach_id=CID,
        coping_tier=coping,
        spt_stage=spt,
        testimonial_text=text,
    )


def _archive(*entries: TestimonialArchiveEntry) -> list[TestimonialArchiveEntry]:
    return list(entries)


def _gate() -> RelevanceStringencyGate:
    return RelevanceStringencyGate(coach_id=CID)


# ══════════════════════════════════════════════════════════════════════
# 1. ADR-01 Constructor Validation
# ══════════════════════════════════════════════════════════════════════


class TestADR01Constructor:
    """ADR-01: coach_id must be 2-4 chars."""

    def test_2_char_ok(self) -> None:
        SocialProofRetriever(coach_id="AB")
        RelevanceStringencyGate(coach_id="AB")

    def test_3_char_ok(self) -> None:
        SocialProofRetriever(coach_id="ABC")
        RelevanceStringencyGate(coach_id="ABC")

    def test_4_char_ok(self) -> None:
        SocialProofRetriever(coach_id="ABCD")
        RelevanceStringencyGate(coach_id="ABCD")

    def test_1_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="ADR-01"):
            SocialProofRetriever(coach_id="A")
        with pytest.raises(ValueError, match="ADR-01"):
            RelevanceStringencyGate(coach_id="A")

    def test_5_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="ADR-01"):
            SocialProofRetriever(coach_id="ABCDE")
        with pytest.raises(ValueError, match="ADR-01"):
            RelevanceStringencyGate(coach_id="ABCDE")


# ══════════════════════════════════════════════════════════════════════
# 2. SocialProofRetriever — Stage 1 Segment Filtering
# ══════════════════════════════════════════════════════════════════════


class TestSocialProofRetriever:
    """Stage 1 — 3-point segment filtering."""

    def setup_method(self) -> None:
        self.r = SocialProofRetriever(coach_id=CID)

    # ── PERFECT_MATCH ──────────────────────────────────────────────

    def test_perfect_match_exact_coping_and_spt(self) -> None:
        arc = _archive(_entry("r1", 3, 3))
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.PERFECT_MATCH
        assert entry is not None
        assert entry.record_id == "r1"

    def test_perfect_match_returns_first_exact(self) -> None:
        arc = _archive(_entry("r1", 3, 3, "First"), _entry("r2", 3, 3, "Second"))
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.PERFECT_MATCH
        assert entry.record_id == "r1"

    def test_perfect_match_not_polluted_by_adjacent(self) -> None:
        """Adjacent entry present but exact match wins."""
        arc = _archive(_entry("r_adj", 4, 3), _entry("r_exact", 3, 3))
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.PERFECT_MATCH
        assert entry.record_id == "r_exact"

    # ── ADJACENT_MATCH ─────────────────────────────────────────────

    def test_adjacent_match_coping_plus_1(self) -> None:
        arc = _archive(_entry("r1", 4, 3))  # prospect coping=3, archive coping=4
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.ADJACENT_MATCH
        assert entry.record_id == "r1"

    def test_adjacent_match_coping_minus_1(self) -> None:
        arc = _archive(_entry("r1", 2, 3))  # prospect coping=3, archive coping=2
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.ADJACENT_MATCH
        assert entry.record_id == "r1"

    def test_adjacent_requires_exact_spt(self) -> None:
        """Adjacent coping but different SPT → not an adjacent match."""
        arc = _archive(_entry("r1", 4, 2))  # prospect spt=3, archive spt=2
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.BASELINE_DEFAULT
        assert entry is None

    def test_adjacent_coping_2_apart_is_baseline(self) -> None:
        """Coping differs by 2 → BASELINE."""
        arc = _archive(_entry("r1", 5, 3))  # prospect coping=3, archive coping=5
        tier, entry = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.BASELINE_DEFAULT

    # ── BASELINE_DEFAULT ───────────────────────────────────────────

    def test_baseline_empty_archive(self) -> None:
        tier, entry = self.r.retrieve("c1", 3, 3, [])
        assert tier == MatchTierRating.BASELINE_DEFAULT
        assert entry is None

    def test_baseline_no_match_at_all(self) -> None:
        arc = _archive(_entry("r1", 5, 5))  # way off
        tier, entry = self.r.retrieve("c1", 2, 2, arc)
        assert tier == MatchTierRating.BASELINE_DEFAULT
        assert entry is None

    # ── AC1 setup: coping=2, archive only coping=5 ─────────────────

    def test_ac1_prospect_coping2_archive_coping5_baseline(self) -> None:
        """AC1: coping=2, archive only coping=5 → BASELINE_DEFAULT."""
        arc = _archive(_entry("r1", 5, 3))
        tier, _ = self.r.retrieve("c1", 2, 3, arc)
        assert tier == MatchTierRating.BASELINE_DEFAULT

    # ── ADR-01 scoping ─────────────────────────────────────────────

    def test_adr01_other_coach_entries_excluded(self) -> None:
        """Archive entry belonging to a different coach is ignored."""
        other_entry = TestimonialArchiveEntry(
            record_id="rx", coach_id="OTH", coping_tier=3, spt_stage=3,
            testimonial_text="Other coach"
        )
        arc = [other_entry]
        tier, _ = self.r.retrieve("c1", 3, 3, arc)
        assert tier == MatchTierRating.BASELINE_DEFAULT


# ══════════════════════════════════════════════════════════════════════
# 3. RelevanceStringencyGate — Gate Verdicts
# ══════════════════════════════════════════════════════════════════════


class TestRelevanceStringencyGate:
    """Stage 2 — gate verdict + payload row generation."""

    def setup_method(self) -> None:
        self.g = _gate()

    # ── PASS ───────────────────────────────────────────────────────

    def test_pass_perfect_match(self) -> None:
        arc = _archive(_entry("r1", 3, 3, "Transformed my life"))
        row = self.g.evaluate("c1", 3, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.PASS.value
        assert row.match_tier_rating == MatchTierRating.PERFECT_MATCH.value
        assert row.testimonial_text_raw == "Transformed my life"
        assert row.matched_historical_record_id == "r1"

    # ── PROVISIONAL ────────────────────────────────────────────────

    def test_provisional_adjacent_match(self) -> None:
        """AC2: coping=3, archive has coping=4 → ADJACENT → PROVISIONAL."""
        arc = _archive(_entry("r1", 4, 3, "Adjacent proof"))
        row = self.g.evaluate("c1", 3, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.PROVISIONAL.value
        assert row.match_tier_rating == MatchTierRating.ADJACENT_MATCH.value
        assert row.testimonial_text_raw == "Adjacent proof"
        assert row.matched_historical_record_id == "r1"

    # ── FAIL_OMIT_REQUIRED ─────────────────────────────────────────

    def test_fail_omit_baseline(self) -> None:
        """AC1: BASELINE_DEFAULT → FAIL_OMIT_REQUIRED, text=null."""
        arc = _archive(_entry("r1", 5, 3))  # far off
        row = self.g.evaluate("c1", 2, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.FAIL_OMIT_REQUIRED.value
        assert row.testimonial_text_raw is None
        assert row.matched_historical_record_id is None

    def test_fail_omit_empty_archive(self) -> None:
        row = self.g.evaluate("c1", 3, 3, [])
        assert row.gate_verdict == SocialProofGateVerdict.FAIL_OMIT_REQUIRED.value
        assert row.testimonial_text_raw is None

    # ── Row fields ─────────────────────────────────────────────────

    def test_row_has_retrieval_id_uuid(self) -> None:
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("c1", 3, 3, arc)
        parsed = uuid.UUID(row.retrieval_id, version=4)
        assert str(parsed) == row.retrieval_id

    def test_row_has_target_client_id(self) -> None:
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("client_xyz", 3, 3, arc)
        assert row.target_client_id_linked == "client_xyz"

    def test_row_has_coach_id(self) -> None:
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("c1", 3, 3, arc)
        assert row.coach_id == CID

    def test_row_has_computation_timestamp_iso(self) -> None:
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("c1", 3, 3, arc)
        dt = datetime.fromisoformat(row.computation_timestamp)
        assert dt.tzinfo is not None

    def test_no_receipt_chain_ok(self) -> None:
        g = RelevanceStringencyGate(coach_id=CID, receipt_chain=None)
        arc = _archive(_entry("r1", 3, 3))
        row = g.evaluate("c1", 3, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.PASS.value


# ══════════════════════════════════════════════════════════════════════
# 4. Acceptance Criteria
# ══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """Verbatim AC scenarios from tech spec §8."""

    def setup_method(self) -> None:
        self.g = _gate()

    # AC1 — prospect coping=2, only coping=5 in archive → FAIL_OMIT_REQUIRED, text=null
    def test_ac1_advanced_testimonial_withheld_from_beginner(self) -> None:
        arc = _archive(
            _entry("r_adv", 5, 3, "Made $100k after years of work!"),
        )
        row = self.g.evaluate("ac1_client", 2, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.FAIL_OMIT_REQUIRED.value
        assert row.testimonial_text_raw is None
        assert row.matched_historical_record_id is None
        assert row.match_tier_rating == MatchTierRating.BASELINE_DEFAULT.value

    # AC2 — coping=3, archive has coping=4, spt=3 → ADJACENT → PROVISIONAL, text returned
    def test_ac2_adjacent_match_provisional_returned(self) -> None:
        arc = _archive(
            _entry("r_adj", 4, 3, "Slightly ahead but still relatable"),
        )
        row = self.g.evaluate("ac2_client", 3, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.PROVISIONAL.value
        assert row.match_tier_rating == MatchTierRating.ADJACENT_MATCH.value
        assert row.testimonial_text_raw == "Slightly ahead but still relatable"
        assert row.matched_historical_record_id == "r_adj"

    # AC3 — PERFECT_MATCH → matched_historical_record_id populated from archive row
    def test_ac3_perfect_match_record_id_populated(self) -> None:
        record_uuid = str(uuid.uuid4())
        arc = _archive(
            _entry(record_uuid, 4, 3, "Exact match testimonial"),
        )
        row = self.g.evaluate("ac3_client", 4, 3, arc)
        assert row.gate_verdict == SocialProofGateVerdict.PASS.value
        assert row.match_tier_rating == MatchTierRating.PERFECT_MATCH.value
        assert row.matched_historical_record_id == record_uuid
        assert row.testimonial_text_raw == "Exact match testimonial"


# ══════════════════════════════════════════════════════════════════════
# 5. Anti-Fabrication Rule
# ══════════════════════════════════════════════════════════════════════


class TestAntiFabricationRule:
    """Testimonial text must be returned verbatim — no modification."""

    def test_long_testimonial_passed_verbatim(self) -> None:
        long_text = "A" * 5000
        g = _gate()
        arc = _archive(_entry("r1", 3, 3, long_text))
        row = g.evaluate("c1", 3, 3, arc)
        assert row.testimonial_text_raw == long_text

    def test_text_with_special_chars_verbatim(self) -> None:
        special = "I can't believe it! $0→$5000 in 90 days. \"Best decision ever.\""
        g = _gate()
        arc = _archive(_entry("r1", 3, 3, special))
        row = g.evaluate("c1", 3, 3, arc)
        assert row.testimonial_text_raw == special


# ══════════════════════════════════════════════════════════════════════
# 6. Output Schema
# ══════════════════════════════════════════════════════════════════════


class TestOutputSchema:
    """Verify MatchedTestimonialPayloadRow output matches spec §5."""

    def setup_method(self) -> None:
        self.g = _gate()

    def test_model_dump_keys(self) -> None:
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("s1", 3, 3, arc)
        keys = set(row.model_dump().keys())
        expected = {
            "retrieval_id", "target_client_id_linked", "coach_id",
            "match_tier_rating", "gate_verdict", "testimonial_text_raw",
            "matched_historical_record_id", "computation_timestamp",
        }
        assert keys == expected

    def test_match_tier_rating_valid_values(self) -> None:
        valid = {e.value for e in MatchTierRating}
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("s1", 3, 3, arc)
        assert row.match_tier_rating in valid

    def test_gate_verdict_valid_values(self) -> None:
        valid = {e.value for e in SocialProofGateVerdict}
        arc = _archive(_entry("r1", 3, 3))
        row = self.g.evaluate("s1", 3, 3, arc)
        assert row.gate_verdict in valid


# ══════════════════════════════════════════════════════════════════════
# 7. Receipt Chain
# ══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """Verify receipt logging."""

    def test_two_receipts_logged(self) -> None:
        rc, tmp = _make_rc_isolated()
        g = RelevanceStringencyGate(coach_id=CID, receipt_chain=rc)
        arc = _archive(_entry("r1", 3, 3))
        g.evaluate("c1", 3, 3, arc)
        retrieve = rc.query(action="social-proof-retrieve")
        gate = rc.query(action="social-proof-gate")
        assert len(retrieve) >= 1
        assert len(gate) >= 1
        shutil.rmtree(tmp, ignore_errors=True)

    def test_retrieve_receipt_contains_client(self) -> None:
        rc, tmp = _make_rc_isolated()
        g = RelevanceStringencyGate(coach_id=CID, receipt_chain=rc)
        g.evaluate("r2client", 3, 3, _archive(_entry("r1", 3, 3)))
        entries = rc.query(action="social-proof-retrieve")
        assert len(entries) >= 1
        assert "r2client" in entries[0].output_summary
        shutil.rmtree(tmp, ignore_errors=True)

    def test_gate_receipt_contains_verdict(self) -> None:
        rc, tmp = _make_rc_isolated()
        g = RelevanceStringencyGate(coach_id=CID, receipt_chain=rc)
        g.evaluate("c1", 3, 3, _archive(_entry("r1", 3, 3)))
        gate = rc.query(action="social-proof-gate")
        assert len(gate) >= 1
        assert "PASS" in gate[0].output_summary
        shutil.rmtree(tmp, ignore_errors=True)

    def test_no_receipt_chain_no_error(self) -> None:
        g = RelevanceStringencyGate(coach_id=CID, receipt_chain=None)
        row = g.evaluate("c1", 3, 3, _archive(_entry("r1", 3, 3)))
        assert row.gate_verdict == SocialProofGateVerdict.PASS.value


# ══════════════════════════════════════════════════════════════════════
# 8. Persona Masking (C-11)
# ══════════════════════════════════════════════════════════════════════


class TestPersonaMasking:
    """C-11: No agent class names in output JSON."""

    def test_no_class_names_in_output(self) -> None:
        g = _gate()
        arc = _archive(_entry("r1", 3, 3))
        row = g.evaluate("pm1", 3, 3, arc)
        json_str = row.model_dump_json()
        for forbidden in [
            "SocialProofRetriever",
            "RelevanceStringencyGate",
            "SocialProofError",
        ]:
            assert forbidden not in json_str, f"C-11 violation: {forbidden} in output"


# ══════════════════════════════════════════════════════════════════════
# 9. Enum Coverage
# ══════════════════════════════════════════════════════════════════════


class TestEnumCoverage:
    """Verify enum members match spec."""

    def test_match_tier_rating_members(self) -> None:
        names = {m.name for m in MatchTierRating}
        assert names == {"PERFECT_MATCH", "ADJACENT_MATCH", "BASELINE_DEFAULT"}

    def test_social_proof_gate_verdict_members(self) -> None:
        names = {m.name for m in SocialProofGateVerdict}
        assert names == {"PASS", "PROVISIONAL", "FAIL_OMIT_REQUIRED"}

    def test_social_proof_error_members(self) -> None:
        names = {m.name for m in SocialProofError}
        assert names == {
            "EMPTY_ARCHIVE",
            "FILTER_ERROR",
            "GATE_EVALUATION_ERROR",
            "INVALID_COACH_SCOPE",
        }
