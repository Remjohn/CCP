"""Unit tests for FR-ERA3-09 — Conscious Editor.
Covers ScopedRerenderClassifier, TranscriptRevisionManager, and LineageAuditProjector."""
from src.ccp.models.conscious_editor_models import (
    CreateTranscriptRevisionRequest,
    LineageNodeType,
    RerenderScope,
    TranscriptTokenPatch,
)
from src.ccp.services.conscious_editor_service import (
    LineageAuditProjector,
    ScopedRerenderClassifier,
    TranscriptRevisionManager,
)


def _make_revision_manager() -> TranscriptRevisionManager:
    return TranscriptRevisionManager()


def _make_classifier() -> ScopedRerenderClassifier:
    return ScopedRerenderClassifier()


class TestScopedRerenderClassifierReturnsCaptionPatchForSingleWordFix:
    """Verifies that typo-class revisions stay in caption_text_patch
    and explicitly set both rerun flags to False."""

    def test_single_word_typo_is_caption_patch(self):
        mgr = _make_revision_manager()
        revision = mgr.create_revision(
            editor_session_id="ES-001",
            author_person_id="coach-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="The coach helped her clients succeed",
                revised_json_payload='{"tokens": []}',
                revision_note="Fixed typo",
                token_patches=[TranscriptTokenPatch(
                    token_index=3,
                    original_text="clienst",
                    revised_text="clients",
                    start_ms=1200,
                    end_ms=1500,
                )],
            ),
        )

        classifier = _make_classifier()
        decision = classifier.classify(revision=revision)

        assert decision.scope == RerenderScope.caption_text_patch
        assert decision.requires_audio_rerecord is False
        assert decision.requires_nim_rerun is False
        assert decision.requires_vcb_refresh is False


class TestScopedRerenderClassifierReturnsCompositionReflowForWrapChange:
    """Verifies that longer subtitle text causing layout overflow
    upgrades only to composition_reflow."""

    def test_long_text_replacement_triggers_reflow(self):
        mgr = _make_revision_manager()
        revision = mgr.create_revision(
            editor_session_id="ES-002",
            author_person_id="coach-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="A much longer replacement text that will definitely cause caption overflow issues in the rendering",
                revised_json_payload='{"tokens": []}',
                token_patches=[TranscriptTokenPatch(
                    token_index=0,
                    original_text="Short",
                    revised_text="A much longer replacement text that will definitely overflow",
                    start_ms=0,
                    end_ms=500,
                )],
            ),
        )

        classifier = _make_classifier()
        decision = classifier.classify(revision=revision)

        assert decision.scope == RerenderScope.composition_reflow
        assert decision.requires_audio_rerecord is False
        assert decision.requires_nim_rerun is False


class TestScopedRerenderClassifierReturnsVisualRegenForSlideDefect:
    """Verifies that a visual complaint with unchanged transcript
    routes to visual_slide_regeneration."""

    def test_visual_defect_without_token_patches(self):
        mgr = _make_revision_manager()
        revision = mgr.create_revision(
            editor_session_id="ES-003",
            author_person_id="coach-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="Original transcript unchanged",
                revised_json_payload='{"tokens": []}',
            ),
        )

        classifier = _make_classifier()
        decision = classifier.classify(
            revision=revision,
            has_visual_defect=True,
            affected_slide_indices=[2],
        )

        assert decision.scope == RerenderScope.visual_slide_regeneration
        assert decision.affected_slide_indices == [2]
        assert decision.requires_audio_rerecord is False
        assert decision.requires_nim_rerun is False


class TestTranscriptRevisionManagerPreservesOriginalSourcePayload:
    """Verifies append-only revision storage and original transcript immutability."""

    def test_revision_is_new_record_not_overwrite(self):
        mgr = _make_revision_manager()
        rev1 = mgr.create_revision(
            editor_session_id="ES-004",
            author_person_id="coach-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="First revision text",
                revised_json_payload='{"v": 1}',
            ),
        )
        rev2 = mgr.create_revision(
            editor_session_id="ES-004",
            author_person_id="coach-001",
            request=CreateTranscriptRevisionRequest(
                revised_plaintext="Second revision text",
                revised_json_payload='{"v": 2}',
            ),
        )
        assert rev1.revision_id != rev2.revision_id
        assert rev1.revised_plaintext == "First revision text"
        assert rev2.revised_plaintext == "Second revision text"


class TestLineageAuditProjectorEmitsSourceToExportChain:
    """Verifies node ordering and parent references for audit display."""

    def test_full_chain_in_order(self):
        projector = LineageAuditProjector()
        graph = projector.build(
            editor_session_id="ES-005",
            source_audio_asset_id="AST-VOICE-001",
            transcript_id="TRX-001",
            content_output_id="CO-001",
            vcb_id="VCB-001",
            composition_id="COMP-001",
            export_bundle_id="EXP-001",
        )

        assert graph.root_source_audio_asset_id == "AST-VOICE-001"
        assert len(graph.nodes) == 6
        assert graph.nodes[0].node_type == LineageNodeType.source_audio
        assert graph.nodes[1].node_type == LineageNodeType.transcript
        assert graph.nodes[2].node_type == LineageNodeType.semantic_artifact
        assert graph.nodes[3].node_type == LineageNodeType.visual_composition_brief
        assert graph.nodes[4].node_type == LineageNodeType.canvas_composition
        assert graph.nodes[5].node_type == LineageNodeType.export_bundle

        # Parent chain is linear
        assert graph.nodes[0].parent_node_id is None
        for i in range(1, len(graph.nodes)):
            assert graph.nodes[i].parent_node_id == graph.nodes[i - 1].node_id

        assert graph.trigger_first_chain_verified is True
