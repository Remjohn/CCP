"""Integration tests for FR-ERA3-12 CMF SFL-Aware Realization Layer."""
import pytest
from datetime import datetime, timezone

from src.ccp.models.cmf_arc_render_models import CoalitionSpineInput, ArcRenderJobStatus
from src.ccp.models.cmf_sfl_render_models import RenderSurfaceType, RenderFallbackDecision
from src.ccp.models.sfl_query_models import SubliminalFunctionStackPacket, SFLAssemblyStatus, DeliverySurfaceKind, SFLVersionStamp
from src.ccp.models.perceptual_influence_models import (
    PerceptualInfluenceReport, PerceptualInfluenceDecision, PerceptualInfluenceMetricBundle,
    PerceptualDimensionScore, PerceptualInfluenceDimension, PerceptualInfluenceSeverity,
    InfluenceAlignmentResult, FalseDepthDetectionResult, PerceptualInfluenceDecisionSummary
)
from src.ccp.services.cmf_arc_governed_rendering import CMFArcGovernedRenderingPipeline
from src.ccp.services.course_video_cmf import CourseVideoPipeline, CourseVideoResult
from src.ccp.core.receipt_chain import ReceiptChain

def _spine() -> CoalitionSpineInput:
    return CoalitionSpineInput(
        content_output_id="CO-SFL-001",
        coach_id="coach-sfl-001",
        coach_acronym="ADR",
        selected_format="1:1",
        spine_text="Do not seek followers. Fight for the truth of the coaching craft.",
        somatic_arc_type="witness",
        voice_dna_id="vdna-sfl-001"
    )

def _sfl_packet() -> SubliminalFunctionStackPacket:
    return SubliminalFunctionStackPacket(
        packet_id="PKT-SFL-001",
        delivery_surface=DeliverySurfaceKind.CAROUSEL,
        status=SFLAssemblyStatus.RESOLVED,
        active_family_ids=["SFL-FAM-001"],
        active_function_ids=["SFL-FN-001", "SFL-FN-002"],
        version_stamp=SFLVersionStamp(manifest_version="1.0.0", manifest_hash="hash12345678")
    )

def _dim_score(dim: PerceptualInfluenceDimension, score: float) -> PerceptualDimensionScore:
    return PerceptualDimensionScore(
        dimension=dim,
        score=score,
        severity=PerceptualInfluenceSeverity.NONE,
        explanation=f"{dim.value} evaluation"
    )

def _perceptual_report(synthetic_smoothness: float = 0.1) -> PerceptualInfluenceReport:
    metrics = PerceptualInfluenceMetricBundle(
        cognitive_imprint_score=_dim_score(PerceptualInfluenceDimension.COGNITIVE_IMPRINT, 0.85),
        symbolic_density_score=_dim_score(PerceptualInfluenceDimension.SYMBOLIC_DENSITY, 0.75),
        human_congruence_score=_dim_score(PerceptualInfluenceDimension.HUMAN_CONGRUENCE, 0.90),
        contrast_clarity_score=_dim_score(PerceptualInfluenceDimension.CONTRAST_CLARITY, 0.80),
        memorability_pressure=_dim_score(PerceptualInfluenceDimension.MEMORABILITY_PRESSURE, 0.70),
        overexplanation_risk_score=_dim_score(PerceptualInfluenceDimension.OVEREXPLANATION_RISK, 0.20),
        synthetic_smoothness_score=_dim_score(PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS, synthetic_smoothness)
    )
    alignment = InfluenceAlignmentResult(
        aligned=True,
        alignment_score=0.88,
        brand_posture_match=True,
        representation_geometry_match=True,
        archetype_match=True,
        surface_sensitivity_match=True
    )
    false_depth = FalseDepthDetectionResult(detected=False)
    decision = PerceptualInfluenceDecisionSummary(
        decision=PerceptualInfluenceDecision.PASS,
        rationale="Clear intensity alignment verified"
    )
    return PerceptualInfluenceReport(
        report_id="PIR-SFL-001",
        request_id="REQ-SFL-001",
        metric_bundle=metrics,
        influence_alignment=alignment,
        false_depth_result=false_depth,
        decision_summary=decision
    )

def test_sfl_render_planning_success():
    rc = ReceiptChain("ADR")
    pipeline = CMFArcGovernedRenderingPipeline(receipt_chain=rc)
    spine = _spine()
    packet = _sfl_packet()
    report = _perceptual_report()

    # Create job with SFL structures
    job = pipeline.create_job(
        spine=spine,
        surface_type=RenderSurfaceType.AUDIT_CARD,
        sfl_stack=packet,
        perceptual_report=report
    )

    assert job.perceptual_plan is not None
    assert job.perceptual_plan.surface_type == RenderSurfaceType.AUDIT_CARD
    assert job.perceptual_plan.function_stack_packet_id == packet.packet_id
    assert job.perceptual_plan.card_safe is True

    # Generate bundles
    card_bundle, board_bundle = pipeline.generate_audit_bundles(job, job.perceptual_plan, report)
    assert card_bundle.overall_score_0_99 == 87
    assert card_bundle.ai_slop_risk_0_99 == 9
    assert len(card_bundle.visible_scores) == 6

    # Build manifest and verify preservation report
    manifest = pipeline.build_manifest(job, spine, "VCB-SFL-TEST")
    assert job.preservation_report is not None
    assert job.preservation_report.fallback_decision == RenderFallbackDecision.PASS
    assert len(job.preservation_report.dimensions) == 5
    assert all(d.preserved for d in job.preservation_report.dimensions)

def test_sfl_render_planning_missing_report_raises():
    pipeline = CMFArcGovernedRenderingPipeline()
    spine = _spine()
    packet = _sfl_packet()

    with pytest.raises(ValueError, match="Missing PerceptualInfluenceReport"):
        pipeline.create_job(
            spine=spine,
            surface_type=RenderSurfaceType.AUDIT_CARD,
            sfl_stack=packet,
            perceptual_report=None
        )

def test_sfl_render_preservation_downgrade():
    pipeline = CMFArcGovernedRenderingPipeline()
    spine = _spine()
    packet = _sfl_packet()
    # High synthetic smoothness should trigger downgrade decision
    report = _perceptual_report(synthetic_smoothness=0.55)

    job = pipeline.create_job(
        spine=spine,
        surface_type=RenderSurfaceType.REEL,
        sfl_stack=packet,
        perceptual_report=report
    )
    manifest = pipeline.build_manifest(job, spine, "VCB-SFL-TEST-2")

    assert job.preservation_report is not None
    assert job.preservation_report.fallback_decision == RenderFallbackDecision.DOWNGRADE
    assert len(job.preservation_report.lost_intents) > 0
    assert "reel" in job.preservation_report.downgraded_surfaces

def test_course_video_temporal_hints_success():
    class MockRenderEngine:
        async def render_course_video(self, narration, visual_aids, template, audio_mood):
            return {"video_url": "s3://mock/video.mp4", "duration_seconds": 320}

    rc = ReceiptChain("ADR")
    pipeline = CMFArcGovernedRenderingPipeline(receipt_chain=rc)
    job = pipeline.create_job(
        spine=_spine(),
        surface_type=RenderSurfaceType.COURSE_VIDEO,
        sfl_stack=_sfl_packet(),
        perceptual_report=_perceptual_report()
    )

    video_pipeline = CourseVideoPipeline(render_engine=MockRenderEngine())
    import asyncio
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(video_pipeline.execute(
        coach_id="coach-sfl-001",
        command_text="/course-video 'SFL Pacing Lesson'",
        perceptual_plan=job.perceptual_plan
    ))
    assert res.success is True
    assert res.manifest.duration_seconds == 320

def test_course_video_temporal_hints_downgrade():
    rc = ReceiptChain("ADR")
    pipeline = CMFArcGovernedRenderingPipeline(receipt_chain=rc)
    # Create plan with empty/missing temporal hints to trigger downgrade
    plan = pipeline.build_render_perceptual_plan(
        content_output_id="CO-SFL-001",
        coach_id="coach-sfl-001",
        surface_type=RenderSurfaceType.COURSE_VIDEO,
        sfl_stack=SubliminalFunctionStackPacket(
            packet_id="PKT-EMPTY",
            delivery_surface=DeliverySurfaceKind.LONG_FORM_VIDEO,
            status=SFLAssemblyStatus.UNRESOLVED,
            version_stamp=SFLVersionStamp(manifest_version="1.0.0", manifest_hash="hash12345678")
        ),
        directional_report_id="DIR-1",
        perceptual_report=_perceptual_report()
    )
    # Clear hints manually
    plan.temporal_hints.hints = []

    video_pipeline = CourseVideoPipeline(render_engine=None)
    
    import asyncio
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(video_pipeline.execute(
        coach_id="coach-sfl-001",
        command_text="/course-video 'SFL Fallback Lesson'",
        perceptual_plan=plan
    ))
    
    assert res.success is True
    assert "[Low-Motion Downgraded]" in res.manifest.title
