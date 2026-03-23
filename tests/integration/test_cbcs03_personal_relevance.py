"""
FR-CBCS-03 — Personal Relevance Trigger — Integration Tests
=============================================================
Covers: Identity profile synthesis, variable resolution, trigger gate
validation, and acceptance criteria AC1-AC3.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BEHAVIORAL_PATTERNS,
    DEFENSE_FALLBACK,
    DEFENSE_MECHANISM_MAP,
    IDENTITY_PATTERNS,
    PRIMARY_DRIVER_FALLBACK,
    EmotionalArchitecture,
    IdentityTargetingVerdict,
    IdentityTriggerVerdict,
    PersonalRelevanceError,
    UnifiedIdentityProfile,
)
from src.ccp.services.personal_relevance_trigger import (
    CentralRouteTriggerValidator,
    IdentityProfileBuilder,
)


# ── Helpers ─────────────────────────────────────────────────────────────

def _make_builder(coach: str = "TST") -> tuple[IdentityProfileBuilder, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    builder = IdentityProfileBuilder(coach_acronym=coach, receipt_chain=rc)
    return builder, rc


def _make_validator(coach: str = "TST") -> tuple[CentralRouteTriggerValidator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    val = CentralRouteTriggerValidator(coach_acronym=coach, receipt_chain=rc)
    return val, rc


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1 — Identity Profile Synthesis
# ═══════════════════════════════════════════════════════════════════════

class TestIdentityProfileSynthesis:
    """§4 Stage 1 + 2 — profile building with variable resolution."""

    def test_full_profile_with_all_inputs(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize(
            client_id="c1", coach_id="coach1",
            emotional_dna_dominant_theme="Connection",
            coping_primary_defense="Intellectualization",
            moral_primary="fairness",
            highest_intensity_score=85.5,
        )
        assert profile.client_id == "c1"
        assert profile.coach_id == "coach1"
        assert "fairness" in profile.core_identity_statement
        assert "Retreats into logic" in profile.emotional_architecture.defense_mechanism
        assert profile.emotional_architecture.primary_driver == "Connection"
        assert profile.highest_intensity_change_talk == "85.50"

    def test_null_emotional_dna_fallback(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", emotional_dna_dominant_theme=None)
        assert profile.emotional_architecture.primary_driver == PRIMARY_DRIVER_FALLBACK
        assert profile.emotional_architecture.primary_driver == "Autonomy"

    def test_null_coping_fallback_general_resistance(self) -> None:
        """AC2: Null coping → 'General Resistance'."""
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", coping_primary_defense=None)
        assert profile.emotional_architecture.defense_mechanism == DEFENSE_FALLBACK
        assert profile.emotional_architecture.defense_mechanism == "General Resistance"

    def test_avoidance_maps_correctly(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", coping_primary_defense="Avoidance")
        assert "Deflects attention" in profile.emotional_architecture.defense_mechanism

    def test_intellectualization_maps_correctly(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", coping_primary_defense="Intellectualization")
        assert "Retreats into logic" in profile.emotional_architecture.defense_mechanism

    def test_unknown_coping_fallback(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", coping_primary_defense="Projection")
        assert profile.emotional_architecture.defense_mechanism == "General Resistance"

    def test_null_moral_fallback(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", moral_primary=None)
        assert "growth" in profile.core_identity_statement

    def test_null_intensity_fallback(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", highest_intensity_score=None)
        assert profile.highest_intensity_change_talk == "0.00"

    def test_core_identity_statement_template(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize(
            "c1", "coach1",
            emotional_dna_dominant_theme="Freedom",
            coping_primary_defense="Avoidance",
            moral_primary="loyalty",
        )
        expected_parts = [
            "Someone who values loyalty",
            "struggles with",
            "Deflects attention away from the core emotional wound",
            "Freedom is threatened",
        ]
        for part in expected_parts:
            assert part in profile.core_identity_statement

    def test_all_nulls_still_generates_profile(self) -> None:
        """Safety test: all inputs null → no crash, all fallbacks engaged."""
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1")
        assert profile.emotional_architecture.primary_driver == "Autonomy"
        assert profile.emotional_architecture.defense_mechanism == "General Resistance"
        assert "growth" in profile.core_identity_statement
        assert profile.highest_intensity_change_talk == "0.00"

    def test_last_synthesized_is_iso8601(self) -> None:
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1")
        assert "T" in profile.last_synthesized


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2 — Trigger Gate Validation
# ═══════════════════════════════════════════════════════════════════════

class TestTriggerGateValidation:
    """§4 Stage 3 — Identity-First Trigger Gate."""

    def test_pass_no_behavioral_with_identity(self) -> None:
        v, _ = _make_validator()
        text = "Think about who you are and the values you hold."
        result = v.validate(text)
        assert result.verdict == "PASS"
        assert result.is_valid is True
        assert result.rewrite_instruction is None
        assert len(result.rejected_behavioral_phrases) == 0

    def test_fail_behavioral_no_identity(self) -> None:
        v, _ = _make_validator()
        text = "You missed 3 workouts this week."
        result = v.validate(text)
        assert result.verdict == "FAIL"
        assert result.is_valid is False
        assert result.rewrite_instruction is not None
        assert "missed" in result.rejected_behavioral_phrases

    def test_provisional_mixed_message(self) -> None:
        v, _ = _make_validator()
        text = "You missed your session, but think about who you are."
        result = v.validate(text)
        assert result.verdict == "PROVISIONAL"
        assert result.is_valid is False
        assert len(result.rejected_behavioral_phrases) > 0

    def test_fail_no_behavioral_no_identity(self) -> None:
        """No behavioral, no identity → FAIL (no identity engagement)."""
        v, _ = _make_validator()
        text = "Here is a nice sunset picture."
        result = v.validate(text)
        assert result.verdict == "FAIL"
        assert result.is_valid is False

    def test_multiple_behavioral_matches(self) -> None:
        v, _ = _make_validator()
        text = "You missed workouts, stopped journaling, and failed to meditate."
        result = v.validate(text)
        assert result.verdict == "FAIL"
        assert len(result.rejected_behavioral_phrases) >= 3

    def test_behavioral_stopped(self) -> None:
        v, _ = _make_validator()
        result = v.validate("You stopped your routine.")
        assert "stopped" in result.rejected_behavioral_phrases

    def test_behavioral_failed_to(self) -> None:
        v, _ = _make_validator()
        result = v.validate("You failed to complete the challenge.")
        assert len(result.rejected_behavioral_phrases) >= 1

    def test_behavioral_last_time_you(self) -> None:
        v, _ = _make_validator()
        result = v.validate("Last time you tried this approach.")
        assert len(result.rejected_behavioral_phrases) >= 1

    def test_behavioral_habit_tracking(self) -> None:
        v, _ = _make_validator()
        result = v.validate("Your habit tracking shows gaps.")
        assert len(result.rejected_behavioral_phrases) >= 1

    def test_behavioral_days_in_a_row(self) -> None:
        v, _ = _make_validator()
        result = v.validate("You achieved 5 days in a row last month.")
        assert len(result.rejected_behavioral_phrases) >= 1

    def test_identity_who_you_are(self) -> None:
        v, _ = _make_validator()
        text = "Remember who you are at your core."
        result = v.validate(text)
        assert result.verdict == "PASS"

    def test_identity_values(self) -> None:
        v, _ = _make_validator()
        text = "This aligns with your deepest values."
        result = v.validate(text)
        assert result.verdict == "PASS"

    def test_identity_belief(self) -> None:
        v, _ = _make_validator()
        text = "Your belief system drives this change."
        result = v.validate(text)
        assert result.verdict == "PASS"

    def test_identity_kind_of_person(self) -> None:
        v, _ = _make_validator()
        text = "You're the kind of person who perseveres."
        result = v.validate(text)
        assert result.verdict == "PASS"

    def test_rewrite_instruction_includes_driver(self) -> None:
        v, _ = _make_validator()
        result = v.validate("You missed your goal.", primary_driver="Growth")
        assert result.rewrite_instruction is not None
        assert "Growth" in result.rewrite_instruction


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3 — ADR-01 Coach Scope & Receipt Chain
# ═══════════════════════════════════════════════════════════════════════

class TestCoachScopeAndReceipt:
    """ADR-01 enforcement + receipt chain."""

    def test_builder_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            IdentityProfileBuilder(coach_acronym="X", receipt_chain=rc)

    def test_builder_rejects_5char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            IdentityProfileBuilder(coach_acronym="ABCDE", receipt_chain=rc)

    def test_validator_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            CentralRouteTriggerValidator(coach_acronym="X", receipt_chain=rc)

    def test_receipt_emitted_on_synthesize(self) -> None:
        b, rc = _make_builder()
        b.synthesize("c1", "coach1")
        entries = rc.query(action="identity-synthesize")
        assert len(entries) >= 1
        assert entries[0].agent_id == "identity-profile-builder"

    def test_receipt_emitted_on_validate(self) -> None:
        v, rc = _make_validator()
        v.validate("Think about who you are.")
        entries = rc.query(action="identity-trigger-validate")
        assert len(entries) >= 1
        assert entries[0].agent_id == "central-route-trigger-validator"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4 — Acceptance Criteria
# ═══════════════════════════════════════════════════════════════════════

class TestAcceptanceCriteria:
    """Verbatim AC1-AC3 from the spec."""

    def test_ac1_missed_3_journal_entries_fail(self) -> None:
        """AC1: 'You've missed 3 Journal entries' → behavioral_count=1 → FAIL."""
        v, _ = _make_validator()
        result = v.validate("You've missed 3 Journal entries")
        assert result.verdict == "FAIL"
        assert result.is_valid is False
        assert "missed" in result.rejected_behavioral_phrases
        assert result.rewrite_instruction is not None

    def test_ac2_null_coping_still_generates_profile(self) -> None:
        """AC2: coping_mechanisms=Null → defense_mechanism='General Resistance'."""
        b, _ = _make_builder()
        profile = b.synthesize("c1", "coach1", coping_primary_defense=None)
        assert profile.emotional_architecture.defense_mechanism == "General Resistance"
        assert profile.client_id == "c1"  # No crash

    def test_ac3_cross_coach_profile_isolation(self) -> None:
        """AC3: Coach A cannot access Coach B's client profiles.
        We verify ADR-01 enforcement at the service level (2-4 char constraint).
        Cross-coach RLS is enforced at the database layer; here we verify
        that the profile always tags the correct coach_id.
        """
        b, _ = _make_builder()
        profile = b.synthesize("clientB", "coachB")
        assert profile.coach_id == "coachB"
        # A different builder instance for coachA cannot create coachB's profile
        # without explicitly passing coachB's ID — the profile always binds to
        # the coach_id passed, and DB RLS prevents cross-coach reads.
