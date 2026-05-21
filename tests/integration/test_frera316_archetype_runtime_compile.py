"""Integration tests for FR-ERA3-16 — Archetype Runtime Compile.
AC1: Successful containerization emits concrete archetype manifest.
AC4: Evidence conflicts block container commitment before archetype selection."""
import asyncio
from datetime import datetime, timezone

from src.ccp.models.archetype_container_runtime_models import (
    ArchetypeChoice,
    CoachResponseCapturePacket,
    CoalitionInputs,
    RuntimeStatus,
)
from src.ccp.services.archetype_container_runtime import ArchetypeContainerRuntimeService


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def _build_capture(transcript: str = "Most coaches copy the market because they are scared to say who they actually disagree with. When I worked with Sarah in 2023, she lost 40 clients by trying to please everyone. That failure taught her the exact 3 steps she now teaches.") -> CoachResponseCapturePacket:
    return CoachResponseCapturePacket(
        capture_id="CAP-TEST-001",
        coach_id="coach-test-123",
        transcript_text=transcript,
        transcript_language="en",
        captured_at=datetime.now(timezone.utc),
        source_asset_id="AST-VOICE-TEST",
        trigger_guard_session_id="TG-TEST-001",
    )


def _build_coalition(stance: str = "high_contrast", source_count: int = 1) -> CoalitionInputs:
    return CoalitionInputs(
        coalition_id="COL-TEST-42",
        family_mix=["STR", "PRS", "VOC"],
        stance_polarity=stance,
        source_count=source_count,
        evidence_strength=0.81,
        intended_business_job="authority_content",
    )


class TestAC1SuccessfulContainerization:
    """AC1 — Successful containerization emits a concrete archetype manifest."""

    def test_compiled_status(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(
            capture=_build_capture(),
            coalition=_build_coalition(),
            mood_context={"mood_id": "MOOD-001", "primary_vector": "aggressive_certainty", "intensity": 0.85},
        ))
        assert result.status == RuntimeStatus.COMPILED

    def test_selected_archetype_populated(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_capture(), coalition=_build_coalition()))
        assert result.selected_archetype is not None

    def test_manifest_has_accepted_sentence_ids(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_capture(), coalition=_build_coalition()))
        assert result.container_manifest is not None
        assert len(result.container_manifest.accepted_sentence_ids) > 0

    def test_downstream_targets_cmf(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_capture(), coalition=_build_coalition()))
        assert "cmf_arc_governed_rendering" in result.downstream_system_targets

    def test_manifest_has_structural_invariants(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_capture(), coalition=_build_coalition()))
        assert result.container_manifest is not None
        assert len(result.container_manifest.structural_invariants) > 0

    def test_manifest_has_intensity_profile(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_capture(), coalition=_build_coalition()))
        assert result.container_manifest is not None
        assert result.container_manifest.intensity_profile.narrative_arc != ""

    def test_manifest_has_authorized_render_targets(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(capture=_build_capture(), coalition=_build_coalition()))
        assert result.container_manifest is not None
        assert len(result.container_manifest.authorized_render_targets) > 0


class TestAC4EvidenceConflictBlock:
    """AC4 — Evidence conflicts block container commitment before archetype selection."""

    def test_evidence_conflict_blocks(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(
            capture=_build_capture(),
            coalition=_build_coalition(),
            evidence_bundle={"bundle_id": "EVB-CONFLICT", "authenticity_score": 0.3, "conflict_flags": ["type_3_authenticity_conflict"]},
        ))
        assert result.status == RuntimeStatus.BLOCKED_EVIDENCE_CONFLICT

    def test_no_archetype_selected_on_block(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(
            capture=_build_capture(),
            coalition=_build_coalition(),
            evidence_bundle={"bundle_id": "EVB-CONFLICT", "authenticity_score": 0.3, "conflict_flags": ["type_3_authenticity_conflict"]},
        ))
        assert result.selected_archetype is None

    def test_no_cmf_target_on_block(self):
        service = ArchetypeContainerRuntimeService()
        result = _run(service.compile(
            capture=_build_capture(),
            coalition=_build_coalition(),
            evidence_bundle={"bundle_id": "EVB-CONFLICT", "authenticity_score": 0.3, "conflict_flags": ["type_3_authenticity_conflict"]},
        ))
        assert "cmf_arc_governed_rendering" not in result.downstream_system_targets
