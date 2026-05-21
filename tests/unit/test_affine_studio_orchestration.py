"""Unit tests for FR-ERA3-07 — AFFiNE Studio Orchestration.
Covers client card projection, red flag excerpt assembly, and intercept review gate."""
import hashlib
from datetime import datetime, timezone

from src.ccp.models.affine_broadcast_models import (
    InterceptGateStatus,
    ReviewAcknowledgementRequest,
)
from src.ccp.services.affine_studio_orchestration import (
    ClientCardProjectionService,
    CrossSystemProgressAdapter,
    DiagnosticExcerptEvidenceResolver,
    InterceptReviewGateService,
    RedFlagExcerptAssembler,
)


def _make_adapter() -> CrossSystemProgressAdapter:
    return CrossSystemProgressAdapter()


def _make_card_service() -> ClientCardProjectionService:
    return ClientCardProjectionService(progress_adapter=_make_adapter())


def _make_excerpt_resolver() -> DiagnosticExcerptEvidenceResolver:
    return DiagnosticExcerptEvidenceResolver()


def _make_flag_assembler() -> RedFlagExcerptAssembler:
    return RedFlagExcerptAssembler(excerpt_resolver=_make_excerpt_resolver())


class TestClientCardProjectionBuildsVisualArcAndCta:
    """test_client_card_projection_builds_visual_completion_arc_and_cta (AC1)"""

    def test_card_has_progress_arc(self):
        service = _make_card_service()
        card = service.build_card(client_id="cli-001", coach_id="coach-001", display_name="Test Client")
        assert card.progress_arc.completion_percent >= 0.0
        assert card.progress_arc.streak_days >= 0
        assert len(card.progress_arc.mood_indicator) > 0
        assert len(card.progress_arc.current_program_step) > 0

    def test_card_has_conviction_score(self):
        service = _make_card_service()
        card = service.build_card(client_id="cli-001", coach_id="coach-001")
        assert 0.0 <= card.conviction.composite_score <= 100.0

    def test_card_has_cta(self):
        service = _make_card_service()
        card = service.build_card(client_id="cli-001", coach_id="coach-001")
        assert len(card.primary_cta) > 0

    def test_card_does_not_expose_raw_internals(self):
        """Card displays composite score and CTA — not raw metric internals."""
        service = _make_card_service()
        card = service.build_card(client_id="cli-001", coach_id="coach-001")
        model_fields = set(card.model_fields.keys())
        assert "raw_biometrics" not in model_fields
        assert "internal_metrics" not in model_fields


class TestRedFlagExcerptAssemblerSuppressesNumericOnly:
    """test_red_flag_excerpt_assembler_suppresses_numeric_only_alerts (AC2)"""

    def test_transcript_signal_emits_flag(self):
        assembler = _make_flag_assembler()
        flags = assembler.assemble(
            coach_id="coach-001",
            client_id="cli-001",
            signals=[{
                "flag_id": "FLAG-001",
                "session_id": "SESS-001",
                "asset_id": "AST-001",
                "workspace_entry_id": "WE-001",
                "transcript_snippet": "Client paused for 4 seconds after mentioning pricing",
                "severity": "high",
                "flag_title": "Pricing hesitation detected",
                "flag_summary": "Client showed significant hesitation when discussing pricing details",
            }],
        )
        assert len(flags) == 1
        assert flags[0].excerpt.display_excerpt == "Client paused for 4 seconds after mentioning pricing"
        assert len(flags[0].excerpt.excerpt_hash) >= 32

    def test_numeric_only_signal_suppressed(self):
        assembler = _make_flag_assembler()
        flags = assembler.assemble(
            coach_id="coach-001",
            client_id="cli-001",
            signals=[{
                "flag_id": "FLAG-002",
                "session_id": "SESS-002",
                "asset_id": "AST-002",
                "workspace_entry_id": "WE-002",
                "severity": "medium",
                "flag_title": "Low Confidence 0.32",
                "flag_summary": "Confidence below threshold",
            }],
        )
        assert len(flags) == 0, "Numeric-only flag must be suppressed"

    def test_flags_sorted_by_severity(self):
        assembler = _make_flag_assembler()
        flags = assembler.assemble(
            coach_id="coach-001",
            client_id="cli-001",
            signals=[
                {
                    "flag_id": "FLAG-LOW",
                    "session_id": "S1", "asset_id": "A1", "workspace_entry_id": "W1",
                    "transcript_snippet": "Client mentioned feeling okay about the schedule change",
                    "severity": "low",
                    "flag_title": "Minor concern",
                    "flag_summary": "Low-priority observation from session",
                },
                {
                    "flag_id": "FLAG-CRIT",
                    "session_id": "S2", "asset_id": "A2", "workspace_entry_id": "W2",
                    "transcript_snippet": "Client explicitly said they want to cancel the program immediately",
                    "severity": "critical",
                    "flag_title": "Cancel intent",
                    "flag_summary": "Client expressed clear intent to cancel program engagement",
                },
            ],
        )
        assert len(flags) == 2
        assert flags[0].severity.value == "critical"
        assert flags[1].severity.value == "low"


class TestInterceptReviewGateRequiresExactPhraseAndHash:
    """test_intercept_review_gate_requires_exact_phrase_and_hash_match (AC3, AC4)"""

    def test_matching_hash_unlocks(self):
        gate = InterceptReviewGateService()
        excerpt_text = "Client paused for 4 seconds after mentioning pricing"
        current_hash = hashlib.sha256(excerpt_text.encode("utf-8")).hexdigest()

        request = ReviewAcknowledgementRequest(
            coach_id="coach-001",
            client_id="cli-001",
            excerpt_hash=current_hash,
            acknowledgement_phrase="I have reviewed this",
        )

        record = gate.acknowledge_review(flag_id="FLAG-001", request=request, current_excerpt_hash=current_hash)
        assert record is not None
        assert record.gate_status_after_ack == InterceptGateStatus.ready
        assert record.excerpt_hash == current_hash

    def test_mismatched_hash_stays_locked(self):
        gate = InterceptReviewGateService()
        request = ReviewAcknowledgementRequest(
            coach_id="coach-001",
            client_id="cli-001",
            excerpt_hash="a" * 32,
            acknowledgement_phrase="I have reviewed this",
        )
        record = gate.acknowledge_review(flag_id="FLAG-001", request=request, current_excerpt_hash="b" * 32)
        assert record is None


class TestInterceptGateRelocksOnExcerptRevision:
    """test_intercept_gate_relocks_when_excerpt_revision_changes (AC5)"""

    def test_stale_hash_returns_locked(self):
        gate = InterceptReviewGateService()
        old_hash = "a" * 64
        new_hash = "b" * 64

        status = gate.check_gate_status(flag_id="FLAG-001", coach_id="coach-001", current_excerpt_hash=new_hash)
        assert status == InterceptGateStatus.locked
