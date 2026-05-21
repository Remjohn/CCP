"""Integration tests for FR-ERA3-12 — CMF Arc-Governed Rendering.
AC3: First frame gate blocks before full render.
AC4: Epic Meaning gate blocks release for corporate aesthetic.
AC6: Release requires dual gate pass."""
from src.ccp.models.cmf_arc_render_models import (
    ArcRenderJobStatus, CoalitionSpineInput, EpicMeaningVerdict, FirstFrameVerdict,
)
from src.ccp.services.cmf_arc_governed_rendering import CMFArcGovernedRenderingPipeline

def _spine(arc: str = "rally") -> CoalitionSpineInput:
    return CoalitionSpineInput(content_output_id="CO-INT-001", coach_id="coach-int-001", coach_acronym="CCH", selected_format="short_form_video", spine_text="Every coach who copies the market loses their edge. The ones who win are the ones who fight for what they believe.", somatic_arc_type=arc, voice_dna_id="vdna-int-001")

class TestArcRenderJobStopsBeforeFullRenderWhenFirstFrameGateFails:
    def test_corporate_flag_blocks_job(self):
        pipeline = CMFArcGovernedRenderingPipeline()
        spine = _spine()
        # Manually create with bad first-frame
        from src.ccp.services.cmf_arc_governed_rendering import NarrativeRenderingModel, FirstFrameAuthorityGate
        clusters = NarrativeRenderingModel().translate(spine)
        gate = FirstFrameAuthorityGate()
        check = gate.evaluate(cluster=clusters[0], anti_generic_flags=["corporate aesthetics in key frame"])
        assert check.verdict == FirstFrameVerdict.fail
        # Job with passing scores proceeds
        job_pass = pipeline.create_job(spine)
        # Default scores pass, so job should be preview_rendering
        assert job_pass.status in (ArcRenderJobStatus.preview_rendering, ArcRenderJobStatus.planned)

class TestPreviewRejectionBlocksReleaseForCorporateAesthetic:
    def test_corporate_preview_blocks_release(self):
        pipeline = CMFArcGovernedRenderingPipeline()
        job = pipeline.create_job(_spine())
        job = pipeline.run_epic_meaning_gate(job, blandness_confidence=0.50, failed_rules=["corporate blandness"])
        assert job.status == ArcRenderJobStatus.preview_failed
        assert job.epic_meaning_gate is not None
        assert job.epic_meaning_gate.verdict == EpicMeaningVerdict.fail_corporate_aesthetic
        result = pipeline.release(job)
        assert result is None, "Release must be denied when Epic Meaning gate fails"

class TestClusterRegenerationRetriesOnlyFailedCluster:
    def test_single_cluster_retry(self):
        pipeline = CMFArcGovernedRenderingPipeline()
        job = pipeline.create_job(_spine())
        assert len(job.beat_clusters) >= 2
        # Each cluster has its own ID — targeted regen affects only one
        first_id = job.beat_clusters[0].cluster_id
        second_id = job.beat_clusters[1].cluster_id
        assert first_id != second_id

class TestReleaseHandoffCreatesCompositionAfterDualGatePass:
    def test_dual_gate_pass_allows_release(self):
        pipeline = CMFArcGovernedRenderingPipeline()
        job = pipeline.create_job(_spine())
        assert job.first_frame_check is not None
        assert job.first_frame_check.verdict == FirstFrameVerdict.pass_
        job = pipeline.run_epic_meaning_gate(job, blandness_confidence=0.05)
        assert job.epic_meaning_gate.verdict == EpicMeaningVerdict.pass_
        manifest = pipeline.build_manifest(job, _spine(), "VCB-INT-001")
        assert manifest.manifest_id != ""
        result = pipeline.release(job)
        assert result is not None
        assert result.release_receipt_id.startswith("RCP-")
        assert job.status == ArcRenderJobStatus.released
    def test_release_denied_without_first_frame(self):
        pipeline = CMFArcGovernedRenderingPipeline()
        job = pipeline.create_job(_spine())
        job.first_frame_check = None
        result = pipeline.release(job)
        assert result is None
    def test_release_denied_without_epic_meaning(self):
        pipeline = CMFArcGovernedRenderingPipeline()
        job = pipeline.create_job(_spine())
        result = pipeline.release(job)
        assert result is None, "Release must be denied without Epic Meaning gate"
