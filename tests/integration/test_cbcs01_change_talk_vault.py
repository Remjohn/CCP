"""
FR-CBCS-01 — Change Talk Vault — Integration Tests
====================================================
Covers: DARN-CAT extraction, priority ordering, intensity scoring,
vault quality gate, and acceptance criteria AC1-AC3.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    DARN_CAT_PATTERNS,
    VAULT_PASS_THRESHOLD,
    VAULT_PROVISIONAL_MIN,
    ChangeTalkArchiveRow,
    ChangeTalkError,
    DarnCatDimension,
    VaultGateVerdict,
    VaultQueryResult,
)
from src.ccp.services.change_talk_vault import ChangeTalkTagger, ChangeTalkVault


# ── Helpers ─────────────────────────────────────────────────────────────

def _make_tagger(coach: str = "TST") -> tuple[ChangeTalkTagger, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    tagger = ChangeTalkTagger(coach_acronym=coach, receipt_chain=rc)
    return tagger, rc


def _make_vault(coach: str = "TST") -> tuple[ChangeTalkVault, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    vault = ChangeTalkVault(coach_acronym=coach, receipt_chain=rc)
    return vault, rc


def _extract(tagger: ChangeTalkTagger, text: str, coping: int = 2, mood: str = "Processing") -> list[ChangeTalkArchiveRow]:
    return tagger.extract("c1", "coach1", text, coping, mood)


def _make_entry(
    dim: str = "Commitment",
    intensity: float = 50.0,
    client_id: str = "c1",
    coach_id: str = "coach1",
) -> ChangeTalkArchiveRow:
    import uuid
    return ChangeTalkArchiveRow(
        entry_id=str(uuid.uuid4()),
        client_id=client_id,
        coach_id=coach_id,
        statement_text="I will do this.",
        darn_cat_dimension=dim,
        liwc_intensity_score=intensity,
        coping_stage_at_time=3,
        emotional_mode="Processing",
        timestamp="2026-03-18T00:00:00Z",
    )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1 — DARN-CAT Extraction
# ═══════════════════════════════════════════════════════════════════════

class TestDarnCatExtraction:
    """§4 Stage 1 + Stage 3 — regex-based extraction."""

    def test_desire_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I want to change my life.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Desire"

    def test_ability_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I can do this easily.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Ability"

    def test_reasons_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I exercise because it makes me feel good.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Reasons"

    def test_need_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I must change my habits now.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Need"

    def test_commitment_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I promise to follow through.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Commitment"

    def test_activation_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I am ready for the challenge.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Activation"

    def test_taking_steps_detected(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I started going to the gym.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Taking_Steps"

    def test_no_match_returns_empty(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "The weather is nice today.")
        assert len(entries) == 0

    def test_empty_text_returns_empty(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "")
        assert len(entries) == 0

    def test_whitespace_only_returns_empty(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "   ")
        assert len(entries) == 0

    def test_multiple_sentences_multiple_dimensions(self) -> None:
        t, _ = _make_tagger()
        text = "I want to improve. I must try harder. I started journaling."
        entries = _extract(t, text)
        dims = {e.darn_cat_dimension for e in entries}
        assert "Desire" in dims
        assert "Need" in dims
        assert "Taking_Steps" in dims


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2 — Priority Ordering
# ═══════════════════════════════════════════════════════════════════════

class TestPriorityOrder:
    """Need takes priority over Commitment, Commitment over Reasons, etc."""

    def test_need_over_commitment(self) -> None:
        """'must' (Need) + 'promise' (Commitment) → Need wins."""
        t, _ = _make_tagger()
        entries = _extract(t, "I must promise to finish.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Need"

    def test_need_over_reasons(self) -> None:
        """'must' (Need) + 'because' (Reasons) → Need wins."""
        t, _ = _make_tagger()
        entries = _extract(t, "I must do this because of my family.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Need"

    def test_commitment_over_desire(self) -> None:
        """'will' (Commitment) + 'want' (Desire) → Commitment wins."""
        t, _ = _make_tagger()
        entries = _extract(t, "I will get what I want.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Commitment"

    def test_taking_steps_over_ability(self) -> None:
        """'started' (Taking_Steps) + 'can' (Ability) → Taking_Steps wins."""
        t, _ = _make_tagger()
        entries = _extract(t, "I started and I can see progress.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Taking_Steps"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3 — Intensity Score
# ═══════════════════════════════════════════════════════════════════════

class TestIntensityScore:
    """liwc_intensity_score = (matched_words / total_words) * 100."""

    def test_single_match_in_5_words(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I must change my life.")
        assert len(entries) == 1
        # "must" → 1 match in 5 words → 20.0
        assert entries[0].liwc_intensity_score == pytest.approx(20.0)

    def test_zero_intensity_not_possible_when_matched(self) -> None:
        """If a dimension was matched, intensity > 0."""
        t, _ = _make_tagger()
        entries = _extract(t, "I want to succeed.")
        assert len(entries) == 1
        assert entries[0].liwc_intensity_score > 0.0

    def test_intensity_capped_at_100(self) -> None:
        """Single word sentences can't exceed 100.0."""
        t, _ = _make_tagger()
        # "must" alone — but sentence splitting might keep the period
        entries = _extract(t, "must.")
        if entries:
            assert entries[0].liwc_intensity_score <= 100.0


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4 — Output Schema Validation
# ═══════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    """§5 schema compliance."""

    def test_entry_has_all_fields(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I must change.", coping=3, mood="Discovery")
        assert len(entries) == 1
        e = entries[0]
        assert e.entry_id  # UUID
        assert e.client_id == "c1"
        assert e.coach_id == "coach1"
        assert len(e.statement_text) > 0
        assert e.darn_cat_dimension in [d.value for d in DarnCatDimension]
        assert 0.0 <= e.liwc_intensity_score <= 100.0
        assert e.coping_stage_at_time == 3
        assert e.emotional_mode == "Discovery"
        assert e.timestamp  # ISO8601

    def test_coping_stage_clamped_low(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I must go.", coping=0)
        assert entries[0].coping_stage_at_time == 1

    def test_coping_stage_clamped_high(self) -> None:
        t, _ = _make_tagger()
        entries = _extract(t, "I must go.", coping=9)
        assert entries[0].coping_stage_at_time == 5


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5 — Vault Quality Gate
# ═══════════════════════════════════════════════════════════════════════

class TestVaultQualityGate:
    """§4 Stage 5 — Minimum Vault Threshold Gate."""

    def test_pass_verdict_ge3_commitment_entries(self) -> None:
        v, _ = _make_vault()
        archive = [
            _make_entry("Commitment", 80.0),
            _make_entry("Taking_Steps", 70.0),
            _make_entry("Commitment", 60.0),
        ]
        result = v.query_vault("c1", "coach1", archive)
        assert result.verdict == "PASS"
        assert result.top_statement is not None
        assert result.top_statement.liwc_intensity_score == 80.0
        assert result.confidence_flag is None

    def test_provisional_verdict_1_or_2_entries(self) -> None:
        v, _ = _make_vault()
        archive = [
            _make_entry("Commitment", 50.0),
            _make_entry("Commitment", 40.0),
        ]
        result = v.query_vault("c1", "coach1", archive)
        assert result.verdict == "PROVISIONAL"
        assert result.confidence_flag == "PROVISIONAL"
        assert result.top_statement is not None

    def test_fail_verdict_zero_commitment(self) -> None:
        v, _ = _make_vault()
        archive = [
            _make_entry("Desire", 50.0),
            _make_entry("Reasons", 40.0),
        ]
        result = v.query_vault("c1", "coach1", archive)
        assert result.verdict == "FAIL"
        assert result.top_statement is None

    def test_fail_verdict_empty_archive(self) -> None:
        v, _ = _make_vault()
        result = v.query_vault("c1", "coach1", [])
        assert result.verdict == "FAIL"
        assert result.total_entries == 0
        assert result.commitment_count == 0

    def test_pass_returns_highest_intensity(self) -> None:
        v, _ = _make_vault()
        archive = [
            _make_entry("Commitment", 30.0),
            _make_entry("Taking_Steps", 90.0),
            _make_entry("Commitment", 50.0),
        ]
        result = v.query_vault("c1", "coach1", archive)
        assert result.verdict == "PASS"
        assert result.top_statement is not None
        assert result.top_statement.liwc_intensity_score == 90.0

    def test_provisional_single_entry(self) -> None:
        v, _ = _make_vault()
        archive = [_make_entry("Taking_Steps", 45.0)]
        result = v.query_vault("c1", "coach1", archive)
        assert result.verdict == "PROVISIONAL"
        assert result.commitment_count == 1


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6 — ADR-01 Coach Scope
# ═══════════════════════════════════════════════════════════════════════

class TestCoachScope:
    """ADR-01 enforcement — coach isolation."""

    def test_tagger_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ChangeTalkTagger(coach_acronym="X", receipt_chain=rc)

    def test_tagger_rejects_5char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ChangeTalkTagger(coach_acronym="ABCDE", receipt_chain=rc)

    def test_vault_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ChangeTalkVault(coach_acronym="X", receipt_chain=rc)

    def test_vault_rejects_5char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ChangeTalkVault(coach_acronym="ABCDE", receipt_chain=rc)

    def test_vault_filters_by_coach_scope(self) -> None:
        """AC3: Cross-coach query returns 0 rows."""
        v, _ = _make_vault()
        archive = [
            _make_entry("Commitment", 80.0, client_id="c1", coach_id="coachA"),
            _make_entry("Commitment", 70.0, client_id="c1", coach_id="coachA"),
            _make_entry("Commitment", 60.0, client_id="c1", coach_id="coachA"),
        ]
        # Query as coachB → should see 0
        result = v.query_vault("c1", "coachB", archive)
        assert result.commitment_count == 0
        assert result.verdict == "FAIL"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7 — Receipt Chain
# ═══════════════════════════════════════════════════════════════════════

class TestReceiptChain:
    """Receipt chain integration."""

    def test_tagger_emits_receipt(self) -> None:
        t, rc = _make_tagger()
        _extract(t, "I must change.")
        entries = rc.query(action="change-talk-extract")
        assert len(entries) >= 1
        assert entries[0].agent_id == "change-talk-tagger"

    def test_vault_emits_receipt(self) -> None:
        v, rc = _make_vault()
        v.query_vault("c1", "coach1", [])
        entries = rc.query(action="vault-query")
        assert len(entries) >= 1
        assert entries[0].agent_id == "change-talk-vault"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 8 — Acceptance Criteria
# ═══════════════════════════════════════════════════════════════════════

class TestAcceptanceCriteria:
    """Verbatim AC1-AC3 from the spec."""

    def test_ac1_must_maps_to_need(self) -> None:
        """AC1: 'I must do this because I was promised a raise.' → Need.
        'must' (Need) takes priority over 'because' (Reasons) and 'promised' (Commitment).
        """
        t, _ = _make_tagger()
        entries = _extract(t, "I must do this because I was promised a raise.")
        assert len(entries) == 1
        assert entries[0].darn_cat_dimension == "Need"

    def test_ac2_two_entries_provisional(self) -> None:
        """AC2: Exactly 2 commitment entries → PROVISIONAL verdict."""
        v, _ = _make_vault()
        archive = [
            _make_entry("Commitment", 50.0),
            _make_entry("Taking_Steps", 40.0),
        ]
        result = v.query_vault("c1", "coach1", archive)
        assert result.verdict == "PROVISIONAL"
        assert result.confidence_flag == "PROVISIONAL"

    def test_ac3_cross_coach_returns_zero(self) -> None:
        """AC3: Coach A querying Client B (assigned to Coach B) → 0 rows."""
        v, _ = _make_vault()
        archive = [
            _make_entry("Commitment", 80.0, client_id="clientB", coach_id="coachB"),
            _make_entry("Commitment", 70.0, client_id="clientB", coach_id="coachB"),
            _make_entry("Commitment", 60.0, client_id="clientB", coach_id="coachB"),
        ]
        result = v.query_vault("clientB", "coachA", archive)
        assert result.total_entries == 0
        assert result.commitment_count == 0
        assert result.verdict == "FAIL"
