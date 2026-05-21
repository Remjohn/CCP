import pytest
from datetime import datetime, timezone
from uuid import uuid4
from src.ccp.models.cbcs_models import (
    CBCSSubmissionKind, CapacityTrack, CbcsPerceptualIntakeEnvelope,
    CardEvidenceSnapshot, AuditPrescriptionItem, AuditIntelligenceSummaryInput,
    VisibleScoreCarryover, ScoreBand, PerceptualSeverity, PerceptualEffectSummary,
    PerceptualSourceReference, SourceSystem, RecommendationClass, CoachingSurfaceType,
    VisibleScoreName, CbcsPerceptualRecommendation, VoiceNotePerceptualGuidance,
    AccountabilityPerceptualPrescription, RelationshipFramedCoachingMessage,
    CbcsPerceptualRuntimeReceipt,
)
from src.ccp.models.perceptual_influence_models import (
    PerceptualInfluenceReport, PerceptualInfluenceMetricBundle, PerceptualDimensionScore,
    PerceptualInfluenceDimension, PerceptualInfluenceSeverity, InfluenceAlignmentResult,
    FalseDepthDetectionResult, PerceptualInfluenceDecisionSummary, PerceptualInfluenceDecision,
)
from src.ccp.services.cbcs_evidence_engine import CBCSEvidenceEngineService
from src.ccp.services.cbcs_diagnostic_engine import CBCSDiagnosticEngineService
from src.ccp.services.cbcs_ritual_engine import CBCSRitualEngineService
from src.ccp.services.cbcs_relationship_engine import CBCSRelationshipEngineService
from src.ccp.services.cbcs_four_engine_runtime import CBCSFourEngineRuntimeService
from src.ccp.services.cbcs_sfl_adapters import CbcsSflAdapter


class MockReceiptChain:
    def __init__(self):
        self.logs = []

    def log(self, action, metadata):
        self.logs.append({"action": action, "metadata": metadata})


def make_dummy_report(
    cognitive=0.8,
    symbolic=0.8,
    human=0.8,
    clarity=0.8,
    pressure=0.8,
    overexplanation=0.1,
    smoothness=0.1,
    report_id="PIR-123",
    request_id="REQ-123",
    false_depth_detected=False,
):
    def make_score(dim, score):
        return PerceptualDimensionScore(
            dimension=dim,
            score=score,
            severity=PerceptualInfluenceSeverity.NONE,
            explanation=f"Valid score of {score} for {dim.value}",
        )

    bundle = PerceptualInfluenceMetricBundle(
        cognitive_imprint_score=make_score(PerceptualInfluenceDimension.COGNITIVE_IMPRINT, cognitive),
        symbolic_density_score=make_score(PerceptualInfluenceDimension.SYMBOLIC_DENSITY, symbolic),
        human_congruence_score=make_score(PerceptualInfluenceDimension.HUMAN_CONGRUENCE, human),
        contrast_clarity_score=make_score(PerceptualInfluenceDimension.CONTRAST_CLARITY, clarity),
        memorability_pressure=make_score(PerceptualInfluenceDimension.MEMORABILITY_PRESSURE, pressure),
        overexplanation_risk_score=make_score(PerceptualInfluenceDimension.OVEREXPLANATION_RISK, overexplanation),
        synthetic_smoothness_score=make_score(PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS, smoothness),
    )

    align = InfluenceAlignmentResult(
        aligned=True,
        alignment_score=0.9,
        brand_posture_match=True,
        representation_geometry_match=True,
        archetype_match=True,
        surface_sensitivity_match=True,
    )

    false_depth = FalseDepthDetectionResult(
        detected=false_depth_detected,
    )

    dec = PerceptualInfluenceDecisionSummary(
        decision=PerceptualInfluenceDecision.PASS,
        rationale="Passes evaluation",
    )

    return PerceptualInfluenceReport(
        report_id=report_id,
        request_id=request_id,
        metric_bundle=bundle,
        influence_alignment=align,
        false_depth_result=false_depth,
        decision_summary=dec,
        evaluated_at_utc=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_end_to_end_sfl_flow():
    # 1. End-to-end integration flow via CbcsSflAdapter using a dummy PerceptualInfluenceReport
    receipt_chain = MockReceiptChain()
    evidence_service = CBCSEvidenceEngineService(receipt_chain=receipt_chain)
    diagnostic_service = CBCSDiagnosticEngineService(receipt_chain=receipt_chain)
    ritual_service = CBCSRitualEngineService(receipt_chain=receipt_chain)
    relationship_service = CBCSRelationshipEngineService(receipt_chain=receipt_chain)
    runtime = CBCSFourEngineRuntimeService(
        evidence_engine=evidence_service,
        diagnostic_engine=diagnostic_service,
        ritual_engine=ritual_service,
        relationship_engine=relationship_service,
        receipt_chain=receipt_chain,
    )

    report = make_dummy_report()
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    session = await runtime.process_submission(
        client_id="client-1",
        coach_id="coach-1",
        submission_kind=CBCSSubmissionKind.VOICE_NOTE,
        perceptual_intake=intake,
    )

    assert session.evidence_packet.perceptual_intake is not None
    assert session.perceptual_recommendation is not None
    assert session.user_notification is not None
    assert session.user_notification.safe_headline is not None

    # Check receipt chain log action final-dispatch exists
    actions = [l["action"] for l in receipt_chain.logs]
    assert "final-dispatch" in actions


@pytest.mark.asyncio
async def test_low_trust_resolves_to_proof_ground():
    # 2. Low trust score (severe failure) resolves to PROOF_GROUND recommendation class
    receipt_chain = MockReceiptChain()
    diagnostic_service = CBCSDiagnosticEngineService(receipt_chain=receipt_chain)
    ritual_service = CBCSRitualEngineService(receipt_chain=receipt_chain)

    report = make_dummy_report(clarity=0.1)  # Low clarity maps to low trust
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    evidence_packet = await CBCSEvidenceEngineService().extract_evidence(
        client_id="client-1",
        coach_id="coach-1",
        submission_kind=CBCSSubmissionKind.VOICE_NOTE,
        perceptual_intake=intake,
    )

    rec = await diagnostic_service.diagnose_perceptual(evidence=evidence_packet)
    assert rec.recommendation_class == RecommendationClass.PROOF_GROUND
    assert rec.target_surface == CoachingSurfaceType.ACCOUNTABILITY_MESSAGE

    vn_guidance, acc_prescription = await ritual_service.generate_perceptual_plans(
        recommendation=rec, intake=intake
    )
    assert acc_prescription is not None
    assert acc_prescription.repetition_window_days == 3  # Tighter check-in window


@pytest.mark.asyncio
async def test_fallback_mode_visible_scores_only():
    # 3. Fallback mode verification: source contract 'FALLBACK_SFL_EVAL'
    receipt_chain = MockReceiptChain()
    diagnostic_service = CBCSDiagnosticEngineService(receipt_chain=receipt_chain)
    relationship_service = CBCSRelationshipEngineService(receipt_chain=receipt_chain)
    runtime = CBCSFourEngineRuntimeService(
        evidence_engine=CBCSEvidenceEngineService(receipt_chain=receipt_chain),
        diagnostic_engine=diagnostic_service,
        ritual_engine=CBCSRitualEngineService(receipt_chain=receipt_chain),
        relationship_engine=relationship_service,
        receipt_chain=receipt_chain,
    )

    # Construct fallback report with specific contract ID
    report = make_dummy_report(report_id="FALLBACK_SFL_EVAL")
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    session = await runtime.process_submission(
        client_id="client-1",
        coach_id="coach-1",
        submission_kind=CBCSSubmissionKind.VOICE_NOTE,
        perceptual_intake=intake,
    )

    assert "[LOWER CONFIDENCE: Running in visible-scores-only fallback mode.]" in session.perceptual_recommendation.explanation_for_operator

    # Check if receipt registered fallback mode
    dispatch_logs = [l for l in receipt_chain.logs if l["action"] == "final-dispatch"]
    assert len(dispatch_logs) > 0
    assert dispatch_logs[0]["metadata"]["fallback_mode"] == "visible_scores_only"


@pytest.mark.asyncio
async def test_no_raw_card_or_board_ids_exposed():
    # 4. No raw Card or Board IDs are exposed in the final message
    relationship_service = CBCSRelationshipEngineService()

    card_snapshot = CardEvidenceSnapshot(
        board_id="board-xyz-777",
        card_ids=["card-abc-111", "card-def-222"],
        thumbnail_asset_ids=[],
        primary_card_labels=["Write introduction"],
    )

    report = make_dummy_report()
    intake = CbcsSflAdapter.from_fr27_report(
        report, client_id="client-1", coach_id="coach-1", card_snapshot=card_snapshot
    )

    rec = CbcsPerceptualRecommendation(
        recommendation_id="rec-1",
        recommendation_class=RecommendationClass.PROOF_GROUND,
        target_surface=CoachingSurfaceType.ACCOUNTABILITY_MESSAGE,
        primary_score_target=VisibleScoreName.TRUST,
        plain_language_goal="Review card-abc-111 on board-xyz-777.",
        recommended_behavior="Look at tasks.",
        prohibited_behavior="Ignore cards.",
        explanation_for_operator="Goal contains raw card references.",
    )

    trend_context = await relationship_service.build_trend_context(client_id="client-1", coach_id="coach-1")
    coaching_msg = await relationship_service.frame_coaching_message(
        recommendation=rec, intake=intake, trend_context=trend_context
    )

    assert "card-abc-111" not in coaching_msg.safe_headline
    assert "card-abc-111" not in coaching_msg.safe_body
    assert "board-xyz-777" not in coaching_msg.safe_body
    assert "your tasks" in coaching_msg.safe_body or "your task" in coaching_msg.safe_body


@pytest.mark.asyncio
async def test_receipt_writes_registered_at_each_stage():
    # 5. Receipt writes registered in the receipt chain at each stage
    receipt_chain = MockReceiptChain()
    evidence_service = CBCSEvidenceEngineService(receipt_chain=receipt_chain)
    diagnostic_service = CBCSDiagnosticEngineService(receipt_chain=receipt_chain)
    ritual_service = CBCSRitualEngineService(receipt_chain=receipt_chain)
    relationship_service = CBCSRelationshipEngineService(receipt_chain=receipt_chain)
    runtime = CBCSFourEngineRuntimeService(
        evidence_engine=evidence_service,
        diagnostic_engine=diagnostic_service,
        ritual_engine=ritual_service,
        relationship_engine=relationship_service,
        receipt_chain=receipt_chain,
    )

    report = make_dummy_report()
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    await runtime.process_submission(
        client_id="client-1",
        coach_id="coach-1",
        submission_kind=CBCSSubmissionKind.VOICE_NOTE,
        perceptual_intake=intake,
    )

    actions = [l["action"] for l in receipt_chain.logs]
    assert "evidence-extraction" in actions
    assert "diagnostic-decision" in actions
    assert "ritual-mutation" in actions
    assert "final-dispatch" in actions


@pytest.mark.asyncio
async def test_cbar_limits_conformance():
    # 6. Target duration and repetition windows conform strictly to CBAR limits
    ritual_service = CBCSRitualEngineService()

    # Create recommendation demanding extreme values
    rec_voice = CbcsPerceptualRecommendation(
        recommendation_id="rec-vn",
        recommendation_class=RecommendationClass.HUMANIZE,
        target_surface=CoachingSurfaceType.VOICE_NOTE,
        primary_score_target=VisibleScoreName.HUMANITY,
        plain_language_goal="Humanize communication",
        recommended_behavior="Be human",
        prohibited_behavior="Be robotic",
        explanation_for_operator="Preserve humanity",
    )

    report = make_dummy_report()
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    vn_guidance, _ = await ritual_service.generate_perceptual_plans(
        recommendation=rec_voice, intake=intake
    )
    assert vn_guidance is not None
    # 10 <= duration <= 600
    assert 10 <= vn_guidance.target_duration_seconds <= 600

    rec_acc = CbcsPerceptualRecommendation(
        recommendation_id="rec-acc",
        recommendation_class=RecommendationClass.PROOF_GROUND,
        target_surface=CoachingSurfaceType.ACCOUNTABILITY_MESSAGE,
        primary_score_target=VisibleScoreName.TRUST,
        plain_language_goal="Build trust",
        recommended_behavior="Review tasks",
        prohibited_behavior="Ignore cards",
        explanation_for_operator="Building trust",
    )
    _, acc_prescription = await ritual_service.generate_perceptual_plans(
        recommendation=rec_acc, intake=intake
    )
    assert acc_prescription is not None
    # 1 <= window <= 30
    assert 1 <= acc_prescription.repetition_window_days <= 30


@pytest.mark.asyncio
async def test_dignity_preservation_on_downgrade():
    # 7. Down-track/downgrade scenarios verify long-loop context and dignity preservation
    relationship_service = CBCSRelationshipEngineService()

    report = make_dummy_report()
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    # Set up trend context with positive 14-day trajectory
    trend_context = await relationship_service.build_trend_context(client_id="client-1", coach_id="coach-1")
    # Manually populate trend for testing downgrade interception
    trend_context.fourteen_day.status = "positive"
    trend_context.fourteen_day.headline_metric = "+15.0% improvement"
    trend_context.fourteen_day.supporting_sentence = "Your 14-day trajectory shows consistent progress."

    # Downgrade class recommendation
    rec = CbcsPerceptualRecommendation(
        recommendation_id="rec-down",
        recommendation_class=RecommendationClass.SLOW_DOWN,
        target_surface=CoachingSurfaceType.VOICE_NOTE,
        primary_score_target=VisibleScoreName.HUMANITY,
        plain_language_goal="Slow down pace",
        recommended_behavior="Breathe between sentences",
        prohibited_behavior="Rushing",
        explanation_for_operator="Intervention required",
    )

    coaching_msg = await relationship_service.frame_coaching_message(
        recommendation=rec, intake=intake, trend_context=trend_context
    )

    # Assert no regression language
    banned = ["going backward", "you failed", "you struggled", "score dropped", "score fell", "downgraded"]
    for word in banned:
        assert word not in coaching_msg.safe_headline.lower()
        assert word not in coaching_msg.safe_body.lower()

    # Assert long-loop context is highlighted
    assert "+15.0% improvement" in coaching_msg.long_loop_reference


@pytest.mark.asyncio
async def test_anti_slop_rewrites_final_output():
    # 8. Anti-slop / synthetic tone active warning modifies instructions and de-smooths output
    relationship_service = CBCSRelationshipEngineService()

    # High smoothness maps to high slop risk
    report = make_dummy_report(smoothness=0.9)
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    assert intake.effect_summary.anti_slop_warning_active is True

    # Delve, tapestry, and moreover are fluffy words that must be de-smoothed
    rec = CbcsPerceptualRecommendation(
        recommendation_id="rec-slop",
        recommendation_class=RecommendationClass.HUMANIZE,
        target_surface=CoachingSurfaceType.VOICE_NOTE,
        primary_score_target=VisibleScoreName.HUMANITY,
        plain_language_goal="Delve into the tapestry of your goals, moreover maintain pacing.",
        recommended_behavior="Be direct",
        prohibited_behavior="Do not use slop",
        explanation_for_operator="High slop risk detected",
    )

    trend_context = await relationship_service.build_trend_context(client_id="client-1", coach_id="coach-1")
    coaching_msg = await relationship_service.frame_coaching_message(
        recommendation=rec, intake=intake, trend_context=trend_context
    )

    # De-smoothing replacement checks: "delve" -> "focus", "tapestry" -> "journey", "moreover" -> "also"
    assert "delve" not in coaching_msg.safe_body.lower()
    assert "tapestry" not in coaching_msg.safe_body.lower()
    assert "Conversational focus:" in coaching_msg.safe_body


@pytest.mark.asyncio
async def test_humanity_and_resonance_strengths_preserved():
    # 9. Humanity and resonance strength flags preserve strength profiles without flattening
    relationship_service = CBCSRelationshipEngineService()

    # High human congruence maps to high humanity score
    report = make_dummy_report(human=0.9, symbolic=0.9)
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")

    assert any(s.score_name == VisibleScoreName.HUMANITY for s in intake.effect_summary.primary_strengths)

    rec = CbcsPerceptualRecommendation(
        recommendation_id="rec-str",
        recommendation_class=RecommendationClass.REINFORCE,
        target_surface=CoachingSurfaceType.VOICE_NOTE,
        primary_score_target=VisibleScoreName.HUMANITY,
        plain_language_goal="Keep expressing yourself",
        recommended_behavior="Share personal anecdotes",
        prohibited_behavior="Sounding too corporate",
        explanation_for_operator="Reinforce humanity",
    )

    trend_context = await relationship_service.build_trend_context(client_id="client-1", coach_id="coach-1")
    coaching_msg = await relationship_service.frame_coaching_message(
        recommendation=rec, intake=intake, trend_context=trend_context
    )

    # Verify that warm strength reinforcement is added to headline/body
    assert "Your voice brings unique clarity here" in coaching_msg.safe_headline
    assert "I really appreciate how real you have been in these notes." in coaching_msg.safe_body


@pytest.mark.asyncio
async def test_reactance_guard_fails_commanding_phrases():
    # 10. Reactance Guard validation fails for bossy/commanding phrases
    relationship_service = CBCSRelationshipEngineService()

    # Test the reactance guard directly
    assert relationship_service._validate_reactance_guard("You must do this task today.") is False
    assert relationship_service._validate_reactance_guard("Please consider this simple next step.") is True

    # Check integration fallback when recommendation triggers reactance
    rec = CbcsPerceptualRecommendation(
        recommendation_id="rec-react",
        recommendation_class=RecommendationClass.SLOW_DOWN,
        target_surface=CoachingSurfaceType.VOICE_NOTE,
        primary_score_target=VisibleScoreName.HUMANITY,
        plain_language_goal="Obey the command.",
        recommended_behavior="Be cooperative",
        prohibited_behavior="Reactance triggers",
        explanation_for_operator="Check reactance",
    )

    # Let's force recommendation text to fail guard by having a bossy plain language goal that gets translated
    # Let's craft the recommendation class to be proof ground, which maps the plain language goal to body
    rec_bossy = CbcsPerceptualRecommendation(
        recommendation_id="rec-bossy",
        recommendation_class=RecommendationClass.PROOF_GROUND,
        target_surface=CoachingSurfaceType.ACCOUNTABILITY_MESSAGE,
        primary_score_target=VisibleScoreName.TRUST,
        plain_language_goal="You must obey and fail to complete this.",
        recommended_behavior="Follow instructions",
        prohibited_behavior="Rebellion",
        explanation_for_operator="Should trigger reactance guard",
    )

    report = make_dummy_report()
    intake = CbcsSflAdapter.from_fr27_report(report, client_id="client-1", coach_id="coach-1")
    trend_context = await relationship_service.build_trend_context(client_id="client-1", coach_id="coach-1")

    coaching_msg = await relationship_service.frame_coaching_message(
        recommendation=rec_bossy, intake=intake, trend_context=trend_context
    )

    # Should fall back to extremely safe default
    assert coaching_msg.safe_body == "Tomorrow's session is ready. Feel free to explore it when you can."
