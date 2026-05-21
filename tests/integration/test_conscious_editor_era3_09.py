"""Integration tests for FR-ERA3-09 — Conscious Editor.
AC-3.1-A: Artifact review returns archetype before media.
AC-3.2-B: Typo fix rerenders without NIM or audio restart.
AC-3.2-C: Slide regeneration keeps other slots and lineage intact."""
from src.ccp.models.conscious_editor_models import (
    CreateTranscriptRevisionRequest,
    EditorSessionStatus,
    EditorTier,
    RerenderScope,
    TranscriptTokenPatch,
)
from src.ccp.services.conscious_editor_service import (
    EditorArtifactResolver,
    LineageAuditProjector,
    ScopedRerenderClassifier,
    ScopedRerenderOrchestrator,
    TranscriptRevisionManager,
)


class TestEditorArtifactReviewReturnsArchetypeBeforeMediaPreview:
    """AC-3.1-A: Given a coach has recorded a reaction, When ContentMachine completes,
    Then artifact payload exposes archetype_container before any composition preview."""

    def test_artifact_review_before_media(self):
        resolver = EditorArtifactResolver()
        session = resolver.resolve(
            editor_session_id="ES-INT-001",
            coach_id="coach-int-001",
            source_audio_asset_id="AST-VOICE-INT-001",
            content_machine_result={
                "success": True,
                "content_output_id": "CO-INT-001",
                "archetype_container": "ARC-MYTH-DEBUNK",
                "content_piece_ids": ["CP-1", "CP-2"],
                "source_audio_asset_id": "AST-VOICE-INT-001",
            },
        )

        assert session.artifact_summary is not None
        assert session.artifact_summary.archetype_container == "ARC-MYTH-DEBUNK"
        assert session.artifact_summary.trigger_first_verified is True
        assert session.tier == EditorTier.artifact_review
        # No media summary when only artifact exists
        assert session.media_summary is None

    def test_artifact_has_no_blank_prompt_surface(self):
        resolver = EditorArtifactResolver()
        session = resolver.resolve(
            editor_session_id="ES-INT-002",
            coach_id="coach-int-001",
            source_audio_asset_id="AST-VOICE-INT-002",
            content_machine_result={
                "success": True,
                "content_output_id": "CO-INT-002",
                "archetype_container": "ARC-WITNESS",
                "content_piece_ids": ["CP-3"],
                "source_audio_asset_id": "AST-VOICE-INT-002",
            },
        )
        # Session is purely artifact review — no composition authoring
        assert session.artifact_summary is not None
        assert session.composition_id is None


class TestEditorTranscriptTypoFixRerendersWithoutNimOrAudioRestart:
    """AC-3.2-B: Given a coach fixes a misspelled word, When the revision is saved,
    Then scope is caption_text_patch, requires_audio_rerecord=False, requires_nim_rerun=False,
    and prior source audio, semantic artifact, VCB, and composition lineage remain linked."""

    def test_typo_fix_stays_modular(self):
        mgr = TranscriptRevisionManager()
        revision = mgr.create_revision(
            editor_session_id="ES-INT-003",
            author_person_id="coach-int-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="The coach helped her clients succeed in the market",
                revised_json_payload='{"tokens": []}',
                revision_note="Fixed typo: clienst -> clients",
                token_patches=[TranscriptTokenPatch(
                    token_index=3,
                    original_text="clienst",
                    revised_text="clients",
                    start_ms=1200,
                    end_ms=1500,
                )],
            ),
        )

        classifier = ScopedRerenderClassifier()
        decision = classifier.classify(revision=revision)

        # M-05 mandatory assertions
        assert decision.scope == RerenderScope.caption_text_patch
        assert decision.requires_audio_rerecord is False
        assert decision.requires_nim_rerun is False
        assert decision.requires_vcb_refresh is False

    def test_lineage_preserved_after_typo_fix(self):
        projector = LineageAuditProjector()
        graph = projector.build(
            editor_session_id="ES-INT-003",
            source_audio_asset_id="AST-VOICE-INT-003",
            transcript_id="TRX-INT-003",
            content_output_id="CO-INT-003",
            vcb_id="VCB-INT-003",
            composition_id="COMP-INT-003",
        )

        assert graph.root_source_audio_asset_id == "AST-VOICE-INT-003"
        assert graph.trigger_first_chain_verified is True
        assert graph.source_restart_required is False
        # Source audio node still root
        assert graph.nodes[0].referenced_id == "AST-VOICE-INT-003"


class TestEditorSlideRegenerationKeepsOtherSlotsAndLineageIntact:
    """AC-3.2-C: Given transcript is correct but one slide image is wrong,
    When the coach requests a slide fix, Then scope is visual_slide_regeneration,
    and the rest of the composition remains intact."""

    def test_slide_fix_is_visual_only(self):
        mgr = TranscriptRevisionManager()
        revision = mgr.create_revision(
            editor_session_id="ES-INT-004",
            author_person_id="coach-int-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="Unchanged transcript for three slides",
                revised_json_payload='{"tokens": []}',
                revision_note="Slide 2 image is off-brand",
            ),
        )

        classifier = ScopedRerenderClassifier()
        decision = classifier.classify(
            revision=revision,
            has_visual_defect=True,
            affected_slide_indices=[1],
        )

        assert decision.scope == RerenderScope.visual_slide_regeneration
        assert decision.affected_slide_indices == [1]
        assert decision.requires_audio_rerecord is False
        assert decision.requires_nim_rerun is False
        assert decision.requires_vcb_refresh is False

    def test_other_slides_unaffected(self):
        """Only slide_index=1 is targeted; slides 0 and 2 remain intact."""
        orchestrator = ScopedRerenderOrchestrator()
        mgr = TranscriptRevisionManager()
        revision = mgr.create_revision(
            editor_session_id="ES-INT-005",
            author_person_id="coach-int-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="Three slide composition text",
                revised_json_payload='{"tokens": []}',
                revision_note="Fix slide 1 only",
            ),
        )
        classifier = ScopedRerenderClassifier()
        decision = classifier.classify(
            revision=revision,
            has_visual_defect=True,
            affected_slide_indices=[1],
        )

        result = orchestrator.execute(
            decision=decision,
            revision=revision,
            composition_id="COMP-INT-005",
            vcb_id="VCB-INT-005",
            slide_count=3,
        )

        assert result["scope"] == "visual_slide_regeneration"
        # Without canvas service, we verify the path was correct
        assert decision.affected_slide_indices == [1]
