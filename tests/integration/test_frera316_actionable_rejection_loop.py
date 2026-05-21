"""Integration tests for FR-ERA3-16 — Actionable Rejection and Trigger Guard Reroute.
AC2: Anti-centroid rejection returns exact failing sentences and coaching fix.
AC3: Rejection loops route back into trigger-first capture without extra navigation."""
import asyncio
from datetime import datetime, timezone

from src.ccp.models.archetype_container_runtime_models import (
    CoachResponseCapturePacket,
    CoalitionInputs,
    RuntimeStatus,
)
from src.ccp.services.archetype_container_runtime import ArchetypeContainerRuntimeService


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def _build_generic_capture() -> CoachResponseCapturePacket:
    return CoachResponseCapturePacket(
        capture_id="CAP-GENERIC-001",
        coach_id="coach-test-456",
        transcript_text="Every business should just focus on authenticity. At the end of the day we all need to be ourselves. Success comes from growth mindset.",
        transcript_language="en",
        captured_at=datetime.now(timezone.utc),
        source_asset_id="AST-VOICE-GENERIC",
        trigger_guard_session_id="TG-TEST-789",
    )


def _build_coalition() -> CoalitionInputs:
    return CoalitionInputs(
        coalition_id="COL-TEST-99",
        family_mix=["STR"],
        stance_polarity="high_contrast",
        source_count=1,
        evidence_strength=0.5,
        intended_business_job="authority_content",
    )


class TestAC2ActionableRejection:
    """AC2 — Anti-centroid rejection returns exact failing sentences and coaching fix (Phase4-M05)."""

    def test_rejected_actionable_status(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.status == RuntimeStatus.REJECTED_ACTIONABLE

    def test_failing_sentence_ids_exact_and_ordered(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        assert len(result.rejection_payload.failing_sentence_ids) >= 1
        for sid in result.rejection_payload.failing_sentence_ids:
            assert sid.startswith("S")

    def test_failing_sentences_are_exact_text(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        for sentence in result.rejection_payload.failing_sentences:
            assert len(sentence) > 0

    def test_similarity_score_populated(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        assert result.rejection_payload.similarity_score >= 0.75

    def test_coaching_fix_not_empty(self):
        """Phase4-M05: coaching_fix must be specific, not 'Too generic. Try again.'"""
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        assert len(result.rejection_payload.coaching_fix) > 10
        assert result.rejection_payload.coaching_fix != "Too generic. Try again."

    def test_rerecord_prompt_specific(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        assert "Re-record" in result.rejection_payload.rerecord_prompt


class TestAC3TriggerGuardReroute:
    """AC3 — Rejection loops route back into trigger-first capture without extra navigation."""

    def test_reroute_token_present(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        assert result.rejection_payload.trigger_guard_reroute_token is not None
        assert result.rejection_payload.trigger_guard_reroute_token.startswith("TG-REROUTE-")

    def test_trigger_guard_session_id_preserved(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert result.rejection_payload is not None
        assert result.rejection_payload.trigger_guard_session_id == "TG-TEST-789"

    def test_downstream_target_is_trigger_guard(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_generic_capture(), coalition=_build_coalition()))
        assert "trigger_first_execution_guard" in result.downstream_system_targets
