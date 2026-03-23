"""
FR-VIS-02 — TIAR Integration — Integration Tests
Phase 2B, CVE Visual Engine — spec 4 of 13

Tests cover all 6 Acceptance Criteria (AC1-AC6) plus noun partitioning,
multi-word extraction, decay warning flags, VPO audit completeness,
API timeout resilience, TIAR not-initialized fallback, injection resistance,
and receipt chain integration from FR-VIS-02 §8 and §10.

Every test traces to an explicit AC or test case in the spec.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    DecayStage,
    NounAuditEntry,
    NounDecayAudit,
    SlideNounAudit,
    TIARAdapterError,
    TIARInjectionResult,
    TIARNounEntry,
    TIARValidationResult,
    TIRS_EXPIRED_MAX,
    TIRS_IN_DISTRIBUTION_MIN,
)
from src.ccp.services.tiar_adapter import TIARAdapter


# ─────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────


@pytest.fixture
def tmp_receipt_dir(tmp_path: Path) -> Path:
    receipt_dir = tmp_path / "receipts"
    receipt_dir.mkdir()
    return receipt_dir


@pytest.fixture
def receipt_chain(tmp_receipt_dir: Path) -> ReceiptChain:
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_receipt_dir))


def _make_noun(
    noun: str,
    tirs_score: float,
    decay_stage: DecayStage,
    last_measured_date: str = "2026-03-17",
    expired_since: Optional[str] = None,
) -> TIARNounEntry:
    """Helper: create a TIARNounEntry."""
    return TIARNounEntry(
        noun=noun,
        tirs_score=tirs_score,
        decay_stage=decay_stage,
        last_measured_date=last_measured_date,
        expired_since=expired_since,
    )


def _standard_tiar_data() -> list[TIARNounEntry]:
    """Standard test data: 10 active + 3 expired = 13 nouns per AC1."""
    return [
        # in_distribution (TIRS ≥ 7.0) — 7 nouns
        _make_noun("the 5am alarm defeat", 8.7, DecayStage.IN_DISTRIBUTION),
        _make_noun("Sunday night dread spiral", 9.1, DecayStage.IN_DISTRIBUTION),
        _make_noun("client ghost", 7.4, DecayStage.IN_DISTRIBUTION),
        _make_noun("launch day paralysis", 7.8, DecayStage.IN_DISTRIBUTION),
        _make_noun("inbox zero myth", 7.2, DecayStage.IN_DISTRIBUTION),
        _make_noun("revenue ceiling confession", 8.0, DecayStage.IN_DISTRIBUTION),
        _make_noun("imposter spiral", 7.6, DecayStage.IN_DISTRIBUTION),
        # tribal_potential (5.0-6.9, emerging) — 1 noun
        _make_noun("launch anxiety loop", 5.9, DecayStage.TRIBAL_POTENTIAL),
        # decay_approaching (5.0-6.9, warning) — 2 nouns
        _make_noun("revenue plateau confession", 6.8, DecayStage.DECAY_APPROACHING),
        _make_noun("hustle burnout cycle", 5.2, DecayStage.DECAY_APPROACHING),
        # expired (TIRS < 5.0) — 3 nouns
        _make_noun("alignment", 3.2, DecayStage.EXPIRED, expired_since="2026-03-04"),
        _make_noun("hustle culture", 4.1, DecayStage.EXPIRED, expired_since="2026-03-11"),
        _make_noun("growth mindset", 4.5, DecayStage.EXPIRED, expired_since="2026-03-15"),
    ]


@pytest.fixture
def adapter(receipt_chain: ReceiptChain) -> TIARAdapter:
    return TIARAdapter(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
        tiar_data=_standard_tiar_data(),
    )


@pytest.fixture
def empty_adapter(receipt_chain: ReceiptChain) -> TIARAdapter:
    """Adapter with no TIAR data (new coach)."""
    return TIARAdapter(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
        tiar_data=[],
    )


# ═════════════════════════════════════════════════════
# SECTION 1: NOUN PARTITIONING — FR-VIS-02 §10
# ═════════════════════════════════════════════════════


class TestNounPartitioning:
    """§10: Verify noun partitioning into decay stage buckets."""

    def test_standard_data_partition_counts(self) -> None:
        """13 nouns → 10 active + 3 blocked."""
        data = _standard_tiar_data()
        active, blocked = TIARAdapter.partition_nouns(data)
        assert len(active) == 10
        assert len(blocked) == 3

    def test_in_distribution_nouns_active(self) -> None:
        data = _standard_tiar_data()
        active, _ = TIARAdapter.partition_nouns(data)
        in_dist = [n for n in active if n.decay_stage == DecayStage.IN_DISTRIBUTION]
        assert len(in_dist) == 7
        for n in in_dist:
            assert n.is_emerging is False
            assert n.decay_warning is False

    def test_tribal_potential_flagged_as_emerging(self) -> None:
        data = _standard_tiar_data()
        active, _ = TIARAdapter.partition_nouns(data)
        emerging = [n for n in active if n.is_emerging]
        assert len(emerging) == 1
        assert emerging[0].noun == "launch anxiety loop"
        assert emerging[0].decay_stage == DecayStage.TRIBAL_POTENTIAL

    def test_decay_approaching_flagged_with_warning(self) -> None:
        data = _standard_tiar_data()
        active, _ = TIARAdapter.partition_nouns(data)
        decay_warn = [n for n in active if n.decay_warning]
        assert len(decay_warn) == 2
        noun_names = {n.noun for n in decay_warn}
        assert "revenue plateau confession" in noun_names
        assert "hustle burnout cycle" in noun_names

    def test_expired_nouns_blocked(self) -> None:
        data = _standard_tiar_data()
        _, blocked = TIARAdapter.partition_nouns(data)
        blocked_names = {n.noun for n in blocked}
        assert "alignment" in blocked_names
        assert "hustle culture" in blocked_names
        assert "growth mindset" in blocked_names

    def test_empty_input_returns_empty(self) -> None:
        active, blocked = TIARAdapter.partition_nouns([])
        assert active == []
        assert blocked == []

    def test_all_expired_returns_all_blocked(self) -> None:
        data = [
            _make_noun("dead1", 2.0, DecayStage.EXPIRED),
            _make_noun("dead2", 3.0, DecayStage.EXPIRED),
        ]
        active, blocked = TIARAdapter.partition_nouns(data)
        assert len(active) == 0
        assert len(blocked) == 2


# ═════════════════════════════════════════════════════
# SECTION 2: AC1 — UPSTREAM INJECTION — ACTIVE NOUNS
# FR-VIS-02 §8 AC1
# ═════════════════════════════════════════════════════


class TestAC1UpstreamInjectionActiveNouns:
    """AC1: Query TIAR → 10 active + 3 blocked returned correctly."""

    def test_injection_returns_10_active(self, adapter: TIARAdapter) -> None:
        result = adapter.inject_upstream("coach_tst", "CO-TST-AC1-001")
        assert result.vocabulary_size_active == 10
        assert len(result.active_noun_vocabulary) == 10

    def test_injection_returns_3_blocked(self, adapter: TIARAdapter) -> None:
        result = adapter.inject_upstream("coach_tst", "CO-TST-AC1-002")
        assert result.vocabulary_size_blocked == 3
        assert len(result.blocked_noun_list) == 3

    def test_active_vocabulary_contains_expected_nouns(
        self, adapter: TIARAdapter
    ) -> None:
        result = adapter.inject_upstream("coach_tst", "CO-TST-AC1-003")
        active_names = {n.noun for n in result.active_noun_vocabulary}
        assert "the 5am alarm defeat" in active_names
        assert "Sunday night dread spiral" in active_names
        assert "launch anxiety loop" in active_names
        assert "revenue plateau confession" in active_names

    def test_blocked_list_contains_expired_nouns(
        self, adapter: TIARAdapter
    ) -> None:
        result = adapter.inject_upstream("coach_tst", "CO-TST-AC1-004")
        blocked_names = {n.noun for n in result.blocked_noun_list}
        assert "alignment" in blocked_names
        assert "hustle culture" in blocked_names
        assert "growth mindset" in blocked_names

    def test_injection_cache_status_fresh(self, adapter: TIARAdapter) -> None:
        result = adapter.inject_upstream("coach_tst", "CO-TST-AC1-005")
        assert result.cache_status == "FRESH"

    def test_injection_has_receipt_chain_block(self, adapter: TIARAdapter) -> None:
        result = adapter.inject_upstream("coach_tst", "CO-TST-AC1-006")
        assert result.receipt_chain_block is not None


# ═════════════════════════════════════════════════════
# SECTION 3: AC2 — UPSTREAM INJECTION — EXPIRED NOUN BLOCK
# FR-VIS-02 §8 AC2
# ═════════════════════════════════════════════════════


class TestAC2ExpiredNounBlock:
    """AC2: Text containing expired noun is rejected for rewording."""

    def test_text_with_expired_noun_rejected(self, adapter: TIARAdapter) -> None:
        """AC2 primary: 'hustle culture' in text → rejected."""
        injection = adapter.inject_upstream("coach_tst", "CO-TST-AC2-001")
        ok, found_blocked, replacements = adapter.check_text_for_blocked_nouns(
            "Embrace the hustle culture and grind harder", injection
        )
        assert ok is False
        assert "hustle culture" in found_blocked

    def test_text_with_expired_noun_offers_replacements(
        self, adapter: TIARAdapter
    ) -> None:
        """AC2: replacements offered from in_distribution pool."""
        injection = adapter.inject_upstream("coach_tst", "CO-TST-AC2-002")
        ok, _, replacements = adapter.check_text_for_blocked_nouns(
            "Find your alignment and grow", injection
        )
        assert ok is False
        assert len(replacements) >= 1
        for r in replacements:
            assert r.decay_stage == DecayStage.IN_DISTRIBUTION

    def test_text_without_expired_noun_accepted(
        self, adapter: TIARAdapter
    ) -> None:
        """AC2 inverse: clean text → accepted."""
        injection = adapter.inject_upstream("coach_tst", "CO-TST-AC2-003")
        ok, found_blocked, _ = adapter.check_text_for_blocked_nouns(
            "The 5am alarm defeat is the first sign", injection
        )
        assert ok is True
        assert found_blocked == []

    def test_case_insensitive_detection(self, adapter: TIARAdapter) -> None:
        """Expired noun detection is case insensitive."""
        injection = adapter.inject_upstream("coach_tst", "CO-TST-AC2-004")
        ok, found_blocked, _ = adapter.check_text_for_blocked_nouns(
            "HUSTLE CULTURE is outdated", injection
        )
        assert ok is False
        assert len(found_blocked) == 1


# ═════════════════════════════════════════════════════
# SECTION 4: AC3 — DOWNSTREAM RE-VALIDATION — MID-PIPELINE DECAY
# FR-VIS-02 §8 AC3
# ═════════════════════════════════════════════════════


class TestAC3MidPipelineDecay:
    """AC3: Noun decays between script gen and VCB finalization → detected."""

    def test_mid_pipeline_decay_detected(self, adapter: TIARAdapter) -> None:
        """AC3 primary: 'client ghost' decays from 7.4 to 4.8 → expired → detected."""
        # First, do upstream injection (nouns are fresh)
        adapter.inject_upstream("coach_tst", "CO-TST-AC3-001")

        # Simulate mid-pipeline decay: update 'client ghost' to expired
        updated_data = _standard_tiar_data()
        for i, n in enumerate(updated_data):
            if n.noun == "client ghost":
                updated_data[i] = _make_noun(
                    "client ghost", 4.8, DecayStage.EXPIRED, expired_since="2026-03-18"
                )
                break
        adapter.update_tiar_data(updated_data)

        # Downstream validation
        result = adapter.validate_downstream(
            content_output_id="CO-TST-AC3-001",
            slide_texts=["Watch out for the client ghost in your inbox"],
        )
        assert result.valid is False
        assert "client ghost" in result.expired_nouns
        assert result.tiar_status == "TIAR_DECAY_DETECTED"
        assert result.error_type == TIARAdapterError.NOUN_EXPIRED_SINCE_SCRIPT.value

    def test_mid_pipeline_decay_offers_replacements(
        self, adapter: TIARAdapter
    ) -> None:
        """AC3: replacement nouns offered from active pool."""
        updated_data = _standard_tiar_data()
        for i, n in enumerate(updated_data):
            if n.noun == "client ghost":
                updated_data[i] = _make_noun("client ghost", 4.8, DecayStage.EXPIRED)
                break
        adapter.update_tiar_data(updated_data)

        result = adapter.validate_downstream(
            content_output_id="CO-TST-AC3-002",
            slide_texts=["The client ghost strikes again"],
        )
        assert len(result.replacement_nouns) >= 1
        for r in result.replacement_nouns:
            assert r.decay_stage == DecayStage.IN_DISTRIBUTION

    def test_no_decay_all_active_passes(self, adapter: TIARAdapter) -> None:
        """AC3 inverse: no decay → TIAR_VALID."""
        result = adapter.validate_downstream(
            content_output_id="CO-TST-AC3-003",
            slide_texts=[
                "The 5am alarm defeat is real",
                "Sunday night dread spiral hits hard",
            ],
        )
        assert result.valid is True
        assert result.tiar_status == "TIAR_VALID"
        assert len(result.expired_nouns) == 0


# ═════════════════════════════════════════════════════
# SECTION 5: AC4 — DECAY WARNING — NON-BLOCKING
# FR-VIS-02 §8 AC4
# ═════════════════════════════════════════════════════


class TestAC4DecayWarningNonBlocking:
    """AC4: decay_approaching nouns permitted but warned, no VCB rejection."""

    def test_decay_approaching_noun_permitted(
        self, adapter: TIARAdapter
    ) -> None:
        """AC4 primary: 'revenue plateau confession' (TIRS 6.8, decay_approaching)
        → valid but warns."""
        result = adapter.validate_downstream(
            content_output_id="CO-TST-AC4-001",
            slide_texts=["The revenue plateau confession is your wake-up call"],
        )
        assert result.valid is True
        assert result.tiar_status == "TIAR_VALID"
        assert len(result.warnings) >= 1
        assert any("revenue plateau confession" in w for w in result.warnings)
        assert any("NOUN_DECAY_WARNING" in w for w in result.warnings)

    def test_decay_warning_in_audit(self, adapter: TIARAdapter) -> None:
        """AC4: decay warning appears in VPO audit."""
        result = adapter.validate_downstream(
            content_output_id="CO-TST-AC4-002",
            slide_texts=["The revenue plateau confession keeps you stuck"],
        )
        assert result.noun_decay_audit is not None
        assert result.noun_decay_audit.total_decay_warning >= 1

    def test_no_rejection_for_decay_approaching(
        self, adapter: TIARAdapter
    ) -> None:
        """AC4: no rejection — valid remains True."""
        result = adapter.validate_downstream(
            content_output_id="CO-TST-AC4-003",
            slide_texts=["The hustle burnout cycle is real talk"],
        )
        assert result.valid is True


# ═════════════════════════════════════════════════════
# SECTION 6: AC5 — VPO AUDIT COMPLETENESS
# FR-VIS-02 §8 AC5
# ═════════════════════════════════════════════════════


class TestAC5VPOAuditCompleteness:
    """AC5: 7-slide carousel with TIAR nouns in slides 0, 2, 3, 5.
    Slides 1, 4, 6 are image-only (None)."""

    def test_vpo_audit_7_slides(self, adapter: TIARAdapter) -> None:
        """AC5 primary: audit contains entries for all 7 slides."""
        slide_texts: list[Optional[str]] = [
            "The 5am alarm defeat is the first sign of the Sunday night dread spiral",  # 0: text
            None,  # 1: image-only
            "Watch for the client ghost in your DMs",  # 2: text
            "The revenue plateau confession keeps you stuck",  # 3: text (decay warning)
            None,  # 4: image-only
            "Break the imposter spiral before it breaks you",  # 5: text
            None,  # 6: image-only
        ]
        result = adapter.validate_downstream("CO-TST-AC5-001", slide_texts)
        assert result.noun_decay_audit is not None
        audit = result.noun_decay_audit
        assert len(audit.slide_audits) == 7

    def test_text_slides_have_nouns(self, adapter: TIARAdapter) -> None:
        """AC5: text slides 0, 2, 3, 5 have non-empty nouns_found."""
        slide_texts: list[Optional[str]] = [
            "The 5am alarm defeat is the first sign of the Sunday night dread spiral",
            None,
            "Watch for the client ghost in your DMs",
            "The revenue plateau confession keeps you stuck",
            None,
            "Break the imposter spiral before it breaks you",
            None,
        ]
        result = adapter.validate_downstream("CO-TST-AC5-002", slide_texts)
        audit = result.noun_decay_audit
        assert audit is not None
        # Slide 0: should have "the 5am alarm defeat" and "Sunday night dread spiral"
        assert len(audit.slide_audits[0].nouns_found) >= 2
        # Slide 2: should have "client ghost"
        assert len(audit.slide_audits[2].nouns_found) >= 1
        # Slide 3: should have "revenue plateau confession"
        assert len(audit.slide_audits[3].nouns_found) >= 1
        # Slide 5: should have "imposter spiral"
        assert len(audit.slide_audits[5].nouns_found) >= 1

    def test_image_only_slides_have_empty_nouns(
        self, adapter: TIARAdapter
    ) -> None:
        """AC5: image-only slides 1, 4, 6 have empty nouns_found."""
        slide_texts: list[Optional[str]] = [
            "The 5am alarm defeat",
            None,
            "client ghost",
            "revenue plateau confession",
            None,
            "imposter spiral",
            None,
        ]
        result = adapter.validate_downstream("CO-TST-AC5-003", slide_texts)
        audit = result.noun_decay_audit
        assert audit is not None
        assert len(audit.slide_audits[1].nouns_found) == 0
        assert len(audit.slide_audits[4].nouns_found) == 0
        assert len(audit.slide_audits[6].nouns_found) == 0

    def test_noun_audit_has_position_in_text(
        self, adapter: TIARAdapter
    ) -> None:
        """AC5: per-noun data includes position_in_text."""
        result = adapter.validate_downstream(
            "CO-TST-AC5-004",
            ["The 5am alarm defeat hits hard"],
        )
        audit = result.noun_decay_audit
        assert audit is not None
        nouns = audit.slide_audits[0].nouns_found
        assert len(nouns) >= 1
        for n in nouns:
            assert n.position_in_text is not None
            assert n.position_in_text >= 0

    def test_noun_audit_has_tirs_and_stage(
        self, adapter: TIARAdapter
    ) -> None:
        """AC5: per-noun data includes tirs_score and decay_stage."""
        result = adapter.validate_downstream(
            "CO-TST-AC5-005",
            ["The 5am alarm defeat is legendary"],
        )
        audit = result.noun_decay_audit
        assert audit is not None
        for n in audit.slide_audits[0].nouns_found:
            assert n.tirs_score is not None
            assert n.decay_stage is not None

    def test_vpo_audit_totals_correct(self, adapter: TIARAdapter) -> None:
        """AC5: totals count active + decay_warning correctly."""
        slide_texts: list[Optional[str]] = [
            "The 5am alarm defeat",
            "The revenue plateau confession",
        ]
        result = adapter.validate_downstream("CO-TST-AC5-006", slide_texts)
        audit = result.noun_decay_audit
        assert audit is not None
        assert audit.total_tiar_nouns == 2
        assert audit.total_active == 1  # 5am alarm defeat
        assert audit.total_decay_warning == 1  # revenue plateau confession
        assert audit.total_expired == 0


# ═════════════════════════════════════════════════════
# SECTION 7: AC6 — API TIMEOUT RESILIENCE
# FR-VIS-02 §8 AC6
# ═════════════════════════════════════════════════════


class TestAC6APITimeoutResilience:
    """AC6: Notion API timeout → cached data used, pipeline continues."""

    def test_upstream_timeout_uses_cache(self, adapter: TIARAdapter) -> None:
        """AC6 primary: first call fresh, second call (timeout) uses cache."""
        # First call: populates cache
        fresh_result = adapter.inject_upstream("coach_tst", "CO-TST-AC6-001")
        assert fresh_result.cache_status == "FRESH"
        assert fresh_result.vocabulary_size_active == 10

        # Second call: timeout, uses cache
        stale_result = adapter.inject_upstream(
            "coach_tst", "CO-TST-AC6-002", simulate_timeout=True
        )
        assert stale_result.cache_status == "TIAR_CACHE_STALE"
        assert stale_result.vocabulary_size_active == 10

    def test_downstream_timeout_uses_stale(self, adapter: TIARAdapter) -> None:
        """AC6: downstream timeout → TIAR_STALE_DOWNSTREAM logged."""
        # First, fresh upstream
        adapter.inject_upstream("coach_tst", "CO-TST-AC6-003")

        # Downstream timeout
        result = adapter.validate_downstream(
            "CO-TST-AC6-004",
            ["The 5am alarm defeat"],
            simulate_timeout=True,
        )
        assert result.cache_status == "TIAR_STALE_DOWNSTREAM"
        # Pipeline continues — valid result still returned
        assert result.valid is True

    def test_timeout_without_cache_returns_empty(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """AC6: timeout with no cache → empty results."""
        adapter = TIARAdapter(
            coach_acronym="TST",
            receipt_chain=receipt_chain,
            tiar_data=_standard_tiar_data(),
        )
        # Directly simulate timeout without prior fresh call
        # Need to ensure _cache is None initially
        result = adapter.inject_upstream(
            "coach_tst", "CO-TST-AC6-005", simulate_timeout=True
        )
        assert result.cache_status == "TIAR_CACHE_STALE"
        assert result.vocabulary_size_active == 0

    def test_pipeline_does_not_halt_on_timeout(
        self, adapter: TIARAdapter
    ) -> None:
        """AC6: no exception raised, pipeline continues."""
        adapter.inject_upstream("coach_tst", "CO-TST-AC6-006")
        # Should not raise
        result = adapter.validate_downstream(
            "CO-TST-AC6-007",
            ["Some text here"],
            simulate_timeout=True,
        )
        assert result is not None
        assert result.noun_decay_audit is not None


# ═════════════════════════════════════════════════════
# SECTION 8: TIAR NOT INITIALIZED — FR-VIS-02 §6
# ═════════════════════════════════════════════════════


class TestTIARNotInitialized:
    """§6: New coach with no TIAR data → graceful fallback."""

    def test_upstream_returns_empty_vocabulary(
        self, empty_adapter: TIARAdapter
    ) -> None:
        result = empty_adapter.inject_upstream("coach_new", "CO-TST-INIT-001")
        assert result.vocabulary_size_active == 0
        assert result.vocabulary_size_blocked == 0
        assert result.cache_status == "TIAR_NOT_INITIALIZED"

    def test_downstream_skips_validation(
        self, empty_adapter: TIARAdapter
    ) -> None:
        result = empty_adapter.validate_downstream(
            "CO-TST-INIT-002",
            ["Any text is fine when TIAR is not initialized"],
        )
        assert result.valid is True
        assert result.tiar_status == "TIAR_NOT_INITIALIZED"
        assert any("TIAR_NOT_INITIALIZED" in w for w in result.warnings)

    def test_text_check_passes_with_empty_vocabulary(
        self, empty_adapter: TIARAdapter
    ) -> None:
        injection = empty_adapter.inject_upstream("coach_new", "CO-TST-INIT-003")
        ok, blocked, _ = empty_adapter.check_text_for_blocked_nouns(
            "alignment hustle culture growth mindset", injection
        )
        assert ok is True
        assert blocked == []


# ═════════════════════════════════════════════════════
# SECTION 9: MULTI-WORD NOUN EXTRACTION — FR-VIS-02 §10
# ═════════════════════════════════════════════════════


class TestMultiWordNounExtraction:
    """§10: Multi-word phrase extraction, not individual words."""

    def test_multi_word_phrase_matched(self, adapter: TIARAdapter) -> None:
        """'the 5am alarm defeat' matched as a single phrase."""
        nouns = _standard_tiar_data()
        found, _ = adapter.extract_nouns_from_text(
            "The 5am alarm defeat is the first sign of the Sunday night dread spiral",
            nouns,
        )
        noun_names = {n.noun for n in found}
        assert "the 5am alarm defeat" in noun_names
        assert "Sunday night dread spiral" in noun_names

    def test_position_in_text_correct(self, adapter: TIARAdapter) -> None:
        """Position offset is correct for multi-word phrase."""
        nouns = [_make_noun("client ghost", 7.4, DecayStage.IN_DISTRIBUTION)]
        found, _ = adapter.extract_nouns_from_text(
            "Watch for the client ghost in DMs", nouns
        )
        assert len(found) == 1
        assert found[0].position_in_text == 14  # "Watch for the " = 14 chars

    def test_case_insensitive_matching(self, adapter: TIARAdapter) -> None:
        """Noun matching is case-insensitive."""
        nouns = [_make_noun("Sunday night dread spiral", 9.1, DecayStage.IN_DISTRIBUTION)]
        found, _ = adapter.extract_nouns_from_text(
            "the sunday night dread spiral hits different", nouns
        )
        assert len(found) == 1

    def test_nouns_not_in_registry_returned(self, adapter: TIARAdapter) -> None:
        """Words not matching any TIAR noun returned as not_in_registry."""
        nouns = [_make_noun("client ghost", 7.4, DecayStage.IN_DISTRIBUTION)]
        found, not_in_reg = adapter.extract_nouns_from_text(
            "Watch for the client ghost tomorrow", nouns
        )
        assert len(found) == 1
        # "watch", "for", "tomorrow" — "the" is a stop word
        assert "tomorrow" in not_in_reg


# ═════════════════════════════════════════════════════
# SECTION 10: SAFETY TESTS — FR-VIS-02 §10
# ═════════════════════════════════════════════════════


class TestSafetyInjectionResistance:
    """§10 Safety: Noun injection attack resistance."""

    def test_sql_injection_in_noun(self, receipt_chain: ReceiptChain) -> None:
        """§10: malicious noun treated as literal string."""
        malicious_noun = _make_noun(
            "alignment'; DROP TABLE tiar_registry;",
            3.2, DecayStage.EXPIRED,
        )
        adapter = TIARAdapter(
            coach_acronym="TST",
            receipt_chain=receipt_chain,
            tiar_data=[malicious_noun],
        )
        result = adapter.inject_upstream("coach_tst", "CO-TST-SAFE-001")
        assert result.vocabulary_size_blocked == 1
        assert result.blocked_noun_list[0].noun == "alignment'; DROP TABLE tiar_registry;"

    def test_empty_noun_string_handled(self, receipt_chain: ReceiptChain) -> None:
        """Empty string noun doesn't crash."""
        empty_noun = _make_noun("", 3.0, DecayStage.EXPIRED)
        adapter = TIARAdapter(
            coach_acronym="TST",
            receipt_chain=receipt_chain,
            tiar_data=[empty_noun],
        )
        result = adapter.inject_upstream("coach_tst", "CO-TST-SAFE-002")
        assert result.vocabulary_size_blocked == 1


# ═════════════════════════════════════════════════════
# SECTION 11: RECEIPT CHAIN INTEGRATION
# ═════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """Receipt chain writes per DEP-ENG-041."""

    def test_upstream_writes_receipt(
        self, adapter: TIARAdapter, receipt_chain: ReceiptChain
    ) -> None:
        initial = receipt_chain.chain_length()
        adapter.inject_upstream("coach_tst", "CO-TST-RCH-001")
        assert receipt_chain.chain_length() == initial + 1

    def test_downstream_writes_receipt(
        self, adapter: TIARAdapter, receipt_chain: ReceiptChain
    ) -> None:
        initial = receipt_chain.chain_length()
        adapter.validate_downstream("CO-TST-RCH-002", ["some text"])
        assert receipt_chain.chain_length() == initial + 1

    def test_vpo_audit_writes_receipt(
        self, adapter: TIARAdapter, receipt_chain: ReceiptChain
    ) -> None:
        result = adapter.validate_downstream(
            "CO-TST-RCH-003", ["The 5am alarm defeat"]
        )
        initial = receipt_chain.chain_length()
        adapter.log_vpo_audit(result)
        assert receipt_chain.chain_length() == initial + 1

    def test_receipt_actions_correct(
        self, adapter: TIARAdapter, receipt_chain: ReceiptChain
    ) -> None:
        adapter.inject_upstream("coach_tst", "CO-TST-RCH-004")
        result = adapter.validate_downstream(
            "CO-TST-RCH-004", ["The 5am alarm defeat"]
        )
        adapter.log_vpo_audit(result)
        entries = receipt_chain.query(agent_id="tiar_adapter", limit=100)
        actions = {e.action for e in entries}
        assert "VIS02_UPSTREAM_INJECTION" in actions
        assert "VIS02_DOWNSTREAM_VALIDATION" in actions
        assert "VIS02_VPO_AUDIT" in actions


# ═════════════════════════════════════════════════════
# SECTION 12: ADR-01 COACH ACRONYM ENFORCEMENT
# ═════════════════════════════════════════════════════


class TestADR01CoachAcronym:
    """ADR-01: coach_acronym must be 2-4 characters."""

    def test_valid_2_char(self, receipt_chain: ReceiptChain) -> None:
        a = TIARAdapter(coach_acronym="JP", receipt_chain=receipt_chain)
        assert a.coach_acronym == "JP"

    def test_valid_4_char(self, receipt_chain: ReceiptChain) -> None:
        a = TIARAdapter(coach_acronym="JPGR", receipt_chain=receipt_chain)
        assert a.coach_acronym == "JPGR"

    def test_1_char_rejected(self, receipt_chain: ReceiptChain) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            TIARAdapter(coach_acronym="J", receipt_chain=receipt_chain)

    def test_5_char_rejected(self, receipt_chain: ReceiptChain) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            TIARAdapter(coach_acronym="JPGRS", receipt_chain=receipt_chain)


# ═════════════════════════════════════════════════════
# SECTION 13: DECAY WARNING FLAG TESTS — FR-VIS-02 §10
# ═════════════════════════════════════════════════════


class TestDecayWarningFlagLogic:
    """§10: decay_warning vs is_emerging flag precision."""

    def test_decay_approaching_has_warning_not_emerging(self) -> None:
        noun = _make_noun("test", 6.2, DecayStage.DECAY_APPROACHING)
        _, _ = TIARAdapter.partition_nouns([noun])
        active, _ = TIARAdapter.partition_nouns([noun])
        assert len(active) == 1
        assert active[0].decay_warning is True
        assert active[0].is_emerging is False

    def test_tribal_potential_has_emerging_not_warning(self) -> None:
        noun = _make_noun("test", 6.2, DecayStage.TRIBAL_POTENTIAL)
        active, _ = TIARAdapter.partition_nouns([noun])
        assert len(active) == 1
        assert active[0].is_emerging is True
        assert active[0].decay_warning is False
