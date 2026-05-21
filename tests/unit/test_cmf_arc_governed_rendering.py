"""Unit tests for FR-ERA3-12 — CMF Arc-Governed Rendering."""
from src.ccp.models.cmf_arc_render_models import (
    ArcRenderJobStatus, BeatClusterType, CoalitionSpineInput, EpicMeaningVerdict,
    FirstFrameVerdict, ShotGrammarProfile,
)
from src.ccp.services.cmf_arc_governed_rendering import (
    BeatClusterPlanner, CMFArcGovernedRenderingPipeline, EpicMeaningGate,
    FirstFrameAuthorityGate, NarrativeRenderingModel, SkiaRenderManifestBuilder,
)

def _spine(arc: str = "rally") -> CoalitionSpineInput:
    return CoalitionSpineInput(content_output_id="CO-001", coach_id="coach-001", coach_acronym="CCH", selected_format="short_form_video", spine_text="Every coach who copies the market loses their edge. The ones who win are the ones who fight for what they believe.", somatic_arc_type=arc, voice_dna_id="vdna-001")

class TestBeatClusterPlannerAssignsDistinctShotGrammarPerArc:
    def test_rally_gets_kinetic(self):
        clusters = NarrativeRenderingModel().translate(_spine("rally"))
        assert all(c.shot_grammar == ShotGrammarProfile.kinetic_escalation for c in clusters)
    def test_witness_gets_intimate(self):
        clusters = NarrativeRenderingModel().translate(_spine("witness"))
        assert all(c.shot_grammar == ShotGrammarProfile.intimate_observation for c in clusters)
    def test_reflection_gets_contemplative(self):
        clusters = NarrativeRenderingModel().translate(_spine("reflection"))
        assert all(c.shot_grammar == ShotGrammarProfile.contemplative_pause for c in clusters)
    def test_confrontation_gets_pressure(self):
        clusters = NarrativeRenderingModel().translate(_spine("confrontation"))
        assert all(c.shot_grammar == ShotGrammarProfile.pressure_lock for c in clusters)
    def test_arcs_are_distinct(self):
        grammars = set()
        for arc in ["rally", "witness", "reflection", "confrontation"]:
            clusters = NarrativeRenderingModel().translate(_spine(arc))
            grammars.add(clusters[0].shot_grammar)
        assert len(grammars) == 4

class TestFirstFrameAuthorityGateBlocksCorporateAesthetic:
    def test_corporate_flag_blocks(self):
        clusters = NarrativeRenderingModel().translate(_spine())
        gate = FirstFrameAuthorityGate()
        check = gate.evaluate(cluster=clusters[0], anti_generic_flags=["corporate aesthetics detected"])
        assert check.verdict == FirstFrameVerdict.fail
    def test_sterile_lighting_blocks(self):
        clusters = NarrativeRenderingModel().translate(_spine())
        gate = FirstFrameAuthorityGate()
        check = gate.evaluate(cluster=clusters[0], anti_generic_flags=["sterile lighting in key frame"])
        assert check.verdict == FirstFrameVerdict.fail
    def test_good_scores_pass(self):
        clusters = NarrativeRenderingModel().translate(_spine())
        gate = FirstFrameAuthorityGate()
        check = gate.evaluate(cluster=clusters[0], authority_score=0.85, contrast_score=0.80, recognizability_score=0.82)
        assert check.verdict == FirstFrameVerdict.pass_
    def test_low_scores_block(self):
        clusters = NarrativeRenderingModel().translate(_spine())
        gate = FirstFrameAuthorityGate()
        check = gate.evaluate(cluster=clusters[0], authority_score=0.50, contrast_score=0.40, recognizability_score=0.55)
        assert check.verdict == FirstFrameVerdict.fail

class TestEpicMeaningGateRejectsFlatPreview:
    def test_high_blandness_fails(self):
        gate = EpicMeaningGate()
        result = gate.evaluate(job_id="J1", blandness_confidence=0.45, failed_rules=["corporate blandness"])
        assert result.verdict == EpicMeaningVerdict.fail_corporate_aesthetic
    def test_low_blandness_passes(self):
        gate = EpicMeaningGate()
        result = gate.evaluate(job_id="J2", blandness_confidence=0.05)
        assert result.verdict == EpicMeaningVerdict.pass_
    def test_borderline_escalates(self):
        gate = EpicMeaningGate()
        result = gate.evaluate(job_id="J3", blandness_confidence=0.22)
        assert result.verdict == EpicMeaningVerdict.escalate
    def test_no_cluster_tempo_fails(self):
        gate = EpicMeaningGate()
        result = gate.evaluate(job_id="J4", has_cluster_tempo=False)
        assert result.verdict == EpicMeaningVerdict.fail_generic_sonic_bed

class TestManifestBuilderPreservesClusterOrder:
    def test_cluster_order_preserved(self):
        clusters = NarrativeRenderingModel().translate(_spine())
        builder = SkiaRenderManifestBuilder()
        manifest = builder.build(job_id="J1", spine=_spine(), vcb_id="VCB-001", clusters=clusters)
        for i, c in enumerate(manifest.beat_clusters):
            assert c.order_index == i
        assert len(manifest.beat_clusters) == len(clusters)
    def test_controls_present(self):
        clusters = NarrativeRenderingModel().translate(_spine())
        builder = SkiaRenderManifestBuilder()
        manifest = builder.build(job_id="J1", spine=_spine(), vcb_id="VCB-001", clusters=clusters)
        for c in manifest.beat_clusters:
            assert c.deterministic_controls.identity_lora_path != ""
            assert c.deterministic_controls.conscious_pose_id != ""
