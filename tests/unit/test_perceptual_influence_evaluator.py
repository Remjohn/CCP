"""
Unit and Integration Tests for FR-ERA3-27 Perceptual Influence Evaluator.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ca11_models import ValidationStatus
from src.ccp.models.directional_integrity_models import (
    ArchetypalGeometryPacket,
    DirectionalIntegrityDecision,
    DirectionalIntegrityDecisionSummary,
    DirectionalIntegrityDimension,
    DirectionalIntegrityDimensionScore,
    DirectionalIntegrityDomain as DIDom,
    DirectionalIntegrityEngineResult,
    DirectionalIntegrityReport,
    DirectionalIntegrityRequest,
    DirectionalIntegrityResolutionPath,
    DirectionalIntegritySeverity as DISev,
    DirectionalIntegritySurfaceClass as DISurf,
    InvariantFieldPacket,
    RepresentationGeometryPacket,
)
from src.ccp.models.perceptual_influence_models import (
    BrandPostureContext,
    FalseDepthClass,
    PerceptualInfluenceDecision,
    PerceptualInfluenceDimension,
    PerceptualInfluenceDomain,
    PerceptualInfluenceFallbackReason,
    PerceptualInfluencePolicyBundle,
    PerceptualInfluenceRequest,
    PerceptualInfluenceResolutionPath,
    PerceptualInfluenceSeverity,
    PerceptualInfluenceSurface,
    SFLFunctionStackSnapshot,
)
from src.ccp.services.content_machine import ContentMachinePipeline
from src.ccp.services.directional_integrity_engine import DirectionalIntegrityEngine
from src.ccp.services.perceptual_influence_evaluator import (
    CognitiveImprintAnalyzer,
    ContrastClarityAnalyzer,
    FalseDepthDetector,
    HumanCongruenceAnalyzer,
    InfluenceAlignmentAnalyzer,
    MemorabilityPressureAnalyzer,
    OverexplanationRiskAnalyzer,
    PerceptualInfluenceDecisionRouter,
    PerceptualInfluenceEvaluator,
    SymbolicDensityAnalyzer,
    SyntheticSmoothnessAnalyzer,
)
from src.ccp.services.perceptual_influence_policy_registry import (
    PerceptualInfluencePolicyRegistry,
)


# ── Mocks / Muted Dependencies ───────────────────────────────────────────

class MockReceiptChain:
    """Mock append-only receipt chain."""
    def __init__(self):
        self.entries = []
    def log(self, **kwargs):
        class Entry:
            def __init__(self, rid):
                self.receipt_id = rid
        e = Entry(f"REC-{len(self.entries)+1}")
        self.entries.append(kwargs)
        return e


class MockSFLRegistryService:
    """Mock SFL Registry service."""
    pass


class MockDirectionalIntegrityEngine:
    """Muted DI Engine for testing verification flow."""
    def __init__(self, decision: str = "PASS"):
        self.decision = decision

    def evaluate(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
        def dummy_score(dim: DirectionalIntegrityDimension) -> DirectionalIntegrityDimensionScore:
            return DirectionalIntegrityDimensionScore(
                dimension=dim,
                score=1.0,
                severity=DISev.INFO,
                threshold_warning=0.5,
                threshold_block=0.8,
                rationale="Mock passed",
            )

        report = DirectionalIntegrityReport(
            report_id="DIR-MOCK-1",
            request_id=request.request_id,
            domain=request.domain,
            surface_class=request.surface_class,
            policy_id="POLICY-MOCK",
            evaluated_at_utc=datetime.utcnow(),
            decision_summary=DirectionalIntegrityDecisionSummary(
                decision=DirectionalIntegrityDecision(self.decision),
                resolution_path=DirectionalIntegrityResolutionPath.CONTINUE,
                blocking=False,
                advisory_only=False,
                summary="Mocked report summary",
            ),
            invariant_preservation_score=dummy_score(DirectionalIntegrityDimension.INVARIANT_PRESERVATION),
            representation_drift_score=dummy_score(DirectionalIntegrityDimension.REPRESENTATION_DRIFT),
            hard_negative_adjacency_score=dummy_score(DirectionalIntegrityDimension.HARD_NEGATIVE_ADJACENCY),
            trajectory_risk_score=dummy_score(DirectionalIntegrityDimension.TRAJECTORY_RISK),
            overall_confidence=1.0,
        )
        return DirectionalIntegrityEngineResult(
            report=report,
            should_continue_automation=True,
            should_queue_operator_review=False,
            should_trigger_regeneration=False,
            should_trip_circuit_break=False,
        )


# ── Test Suite ───────────────────────────────────────────────────────────

def test_policy_registry_lookup():
    """Policy resolution matching specific and domain-wide fallback."""
    registry = PerceptualInfluencePolicyRegistry()
    
    # Specific lookup
    policy = registry.resolve(PerceptualInfluenceDomain.CCF, PerceptualInfluenceSurface.RENDER_RELEASE)
    assert policy is not None
    assert policy.domain == PerceptualInfluenceDomain.CMF
    assert policy.surface_class == PerceptualInfluenceSurface.RENDER_RELEASE
    assert policy.pass_thresholds["COGNITIVE_IMPRINT"] == 0.55
    assert policy.risk_ceilings["SYNTHETIC_SMOOTHNESS"] == 0.45
    
    # General lookup fallback
    policy_gen = registry.resolve(PerceptualInfluenceDomain.WEBINAR, PerceptualInfluenceSurface.INTERNAL_REVIEW)
    assert policy_gen is not None
    assert policy_gen.domain == PerceptualInfluenceDomain.CCF  # fell back to CCF base policy
    assert policy_gen.policy_id == "PI-POL-INTERNAL_REVIEW"


def test_analyzer_cognitive_imprint():
    """CognitiveImprint analyzer score drop on generic motivational language."""
    analyzer = CognitiveImprintAnalyzer()
    
    # Good text with anchor concept
    good_text = "The Tension Engine is a crucial framework for managing client cognitive breakthroughs."
    res_good = analyzer.analyze(good_text)
    assert res_good.score >= 0.5
    
    # Generic motivational text
    bad_text = "Unlock your potential! Achieve success and be your best today! Go high!"
    res_bad = analyzer.analyze(bad_text)
    assert res_bad.score < 0.5


def test_analyzer_symbolic_density():
    """SymbolicDensity analyzer score changes based on metaphors and gravity words."""
    analyzer = SymbolicDensityAnalyzer()
    
    # High density text
    high_text = "This bridge acts as a mirror, acting as a manifesto for transformation."
    res_high = analyzer.analyze(high_text)
    assert res_high.score >= 0.5
    
    # Sparse density text
    low_text = "just simple normal words here."
    res_low = analyzer.analyze(low_text)
    assert res_low.score < 0.5


def test_analyzer_human_congruence():
    """HumanCongruence analyzer drop on uniform lengths/predictable pacing."""
    analyzer = HumanCongruenceAnalyzer()
    
    # High variance and pronoun presence (human-like)
    human_text = "Honestly, I had to stop. I looked back, and there it was - a simple choice. Let's make it together."
    res_human = analyzer.analyze(human_text)
    assert res_human.score >= 0.6
    
    # Uniform sentence length, no pronouns (robotic/polished)
    robotic_text = "The project commences tomorrow. The team executes the deployment. The operations continue smoothly."
    res_robotic = analyzer.analyze(robotic_text)
    assert res_robotic.score < 0.45


def test_analyzer_contrast_clarity():
    """ContrastClarity score rises on tension, drops on compromise."""
    analyzer = ContrastClarityAnalyzer()
    
    # Clear tension/contrast
    contrast_text = "You want authority, but you seek comfort. Tension versus relief."
    res_contrast = analyzer.analyze(contrast_text)
    assert res_contrast.score >= 0.6
    
    # Compromise
    compromise_text = "We should explore both sides and find a middle ground, a polite compromise."
    res_compromise = analyzer.analyze(compromise_text)
    assert res_compromise.score < 0.45


def test_analyzer_memorability_pressure():
    """MemorabilityPressure score drops on lack of hooks or rhythm anchors."""
    analyzer = MemorabilityPressureAnalyzer()
    
    # Strong hook and repetition
    hook_text = "Never look back. Let's talk about power. Power is focus. Power is everything."
    res_hook = analyzer.analyze(hook_text)
    assert res_hook.score >= 0.6
    
    # Flat text without hooks
    flat_text = "The following documentation outlines the system properties and directory layout."
    res_flat = analyzer.analyze(flat_text)
    assert res_flat.score < 0.45


def test_analyzer_overexplanation_risk():
    """OverexplanationRisk rises when redundant explanations or long paragraphs exist."""
    analyzer = OverexplanationRiskAnalyzer()
    
    # Clean, concise text
    clean_text = "Embrace the tension. It is the boundary of growth."
    res_clean = analyzer.analyze(clean_text)
    assert res_clean.score < 0.4
    
    # Overexplained text
    over_text = "This means that you must change. In other words, to explain further, this is essentially a change."
    res_over = analyzer.analyze(over_text)
    assert res_over.score >= 0.5


def test_analyzer_synthetic_smoothness():
    """SyntheticSmoothness rises on low variance sentence templates and heavy transitions."""
    analyzer = SyntheticSmoothnessAnalyzer()
    
    # Rough human dialogue (highly varied sentence lengths to avoid low-variance block)
    rough_text = "Wait... you really think that's the absolute best way to handle this situation? No. I strongly doubt it, and we must reconsider immediately. Exactly."
    res_rough = analyzer.analyze(rough_text)
    assert res_rough.score < 0.4
    
    # Highly transitioned and uniform sentences
    smooth_text = "Furthermore, the system will execute. Consequently, the user is notified. Therefore, the pipeline finishes."
    res_smooth = analyzer.analyze(smooth_text)
    assert res_smooth.score >= 0.5


def test_false_depth_detector():
    """FalseDepthDetector correctly maps performative, authority, and polish classes."""
    detector = FalseDepthDetector()
    
    # Mock metric bundle
    class DummyScore:
        def __init__(self, score):
            self.score = score
            
    metrics = type("Metrics", (), {
        "cognitive_imprint_score": DummyScore(0.2),
        "synthetic_smoothness_score": DummyScore(0.7),
        "overexplanation_risk_score": DummyScore(0.6)
    })()
    
    # Performative Profundity
    text_profundity = "We transcend the limitless quantum vibrations of infinite cosmic transformation."
    res1 = detector.evaluate(text_profundity, metrics)
    assert res1.detected
    assert FalseDepthClass.PERFORMATIVE_PROFUNDITY in res1.detected_classes

    # Dead Polish (pristine, high smoothness, no emotion/pronouns)
    text_polish = "The protocol ensures consistent operational capabilities. The deployment pipeline runs continuously. The execution completes successfully."
    res2 = detector.evaluate(text_polish, metrics)
    assert res2.detected
    assert FalseDepthClass.DEAD_POLISH in res2.detected_classes

    # Synthetic Authority
    text_auth = "As an expert with a proven methodology and scientific proof of guaranteed success."
    res3 = detector.evaluate(text_auth, metrics)
    assert res3.detected
    assert FalseDepthClass.SYNTHETIC_AUTHORITY in res3.detected_classes

    # Empty Motivational Smoothness
    text_motive = "Believe in yourself and take action today to reach your goals!"
    res4 = detector.evaluate(text_motive, metrics)
    assert res4.detected
    assert FalseDepthClass.EMPTY_MOTIVATIONAL_SMOOTHNESS in res4.detected_classes


def test_influence_alignment_sfl_stack():
    """SFL stack matches/mismatches checked against brand posture."""
    analyzer = InfluenceAlignmentAnalyzer()
    policy = PerceptualInfluencePolicyBundle(
        policy_id="TEST",
        domain=PerceptualInfluenceDomain.CCF,
        surface_class=PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
        pass_thresholds={},
        risk_ceilings={},
        influence_alignment_required=True,
    )
    
    # Missing stack triggers misalignment
    req_missing_stack = PerceptualInfluenceRequest(
        request_id="REQ-1",
        domain=PerceptualInfluenceDomain.CCF,
        surface_class=PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
        actor_id="user1",
        coach_id="coach1",
        candidate_text="Buy this now",
        sfl_function_stack=None,
    )
    res_missing = analyzer.evaluate(req_missing_stack, policy)
    assert not res_missing.aligned
    assert "missing" in res_missing.misalignment_details[0]

    # Forbidden pattern matching
    stack = SFLFunctionStackSnapshot(
        stack_id="ST-1",
        active_families=["covert_suggestion"],
        active_functions=["covert_anchor"],
    )
    brand = BrandPostureContext(
        brand_posture_id="BP-1",
        authority_source="earned",
        belonging_mode="invitational",
        identity_frame="sovereign",
        forbidden_influence_patterns=["covert"],
    )
    req_forbidden = PerceptualInfluenceRequest(
        request_id="REQ-2",
        domain=PerceptualInfluenceDomain.CCF,
        surface_class=PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
        actor_id="user1",
        coach_id="coach1",
        candidate_text="Buy this now",
        sfl_function_stack=stack,
        brand_posture=brand,
    )
    res_forbidden = analyzer.evaluate(req_forbidden, policy)
    assert not res_forbidden.aligned
    assert any("forbidden" in det.lower() for det in res_forbidden.misalignment_details)


def test_decision_router():
    """Decision router maps thresholds, false depth block, and DI inputs correctly."""
    router = PerceptualInfluenceDecisionRouter()
    
    policy = PerceptualInfluencePolicyBundle(
        policy_id="P-1",
        domain=PerceptualInfluenceDomain.CCF,
        surface_class=PerceptualInfluenceSurface.SEMANTIC_PLANNING,
        pass_thresholds={"COGNITIVE_IMPRINT": 0.5},
        risk_ceilings={"SYNTHETIC_SMOOTHNESS": 0.4},
        false_depth_blocks=True,
    )
    
    # DI = FAIL triggers immediate Downgrade
    res_di_fail = router.route(
        metrics=None,
        alignment=None,
        false_depth=None,
        policy=policy,
        fallback_reason=None,
        di_decision="FAIL",
    )
    assert res_di_fail.decision == PerceptualInfluenceDecision.DOWNGRADE
    
    # Policy threshold violation
    class Score:
        def __init__(self, val):
            self.score = val
    metrics_fail = type("Metrics", (), {
        "cognitive_imprint_score": Score(0.3),  # below threshold 0.5
        "symbolic_density_score": Score(0.5),
        "human_congruence_score": Score(0.5),
        "contrast_clarity_score": Score(0.5),
        "memorability_pressure": Score(0.5),
        "overexplanation_risk_score": Score(0.2),
        "synthetic_smoothness_score": Score(0.2),
    })()
    
    align_ok = type("Align", (), {"aligned": True, "misalignment_details": []})()
    fd_ok = type("FD", (), {"detected": False, "detected_classes": []})()
    
    res_threshold_fail = router.route(
        metrics=metrics_fail,
        alignment=align_ok,
        false_depth=fd_ok,
        policy=policy,
        fallback_reason=None,
        di_decision="PASS",
    )
    assert res_threshold_fail.decision == PerceptualInfluenceDecision.REVIEW
    assert res_threshold_fail.resolution_path == PerceptualInfluenceResolutionPath.OPERATOR_REVIEW


def test_evaluator_e2e_mock_di():
    """End-to-end evaluation using mocked DI engine in ContentMachinePipeline."""
    di_engine = MockDirectionalIntegrityEngine(decision="PASS")
    pi_evaluator = PerceptualInfluenceEvaluator(
        policy_registry=PerceptualInfluencePolicyRegistry(),
        sfl_registry=None,
        receipt_chain=MockReceiptChain(),
    )
    
    # Process session content through pipeline
    pipeline = ContentMachinePipeline(
        affine_sync=None,
        ccf_batch=None,
        voice_dna=None,
        di_engine=di_engine,
        pi_evaluator=pi_evaluator,
    )
    
    report = {
        "session_id": "session-e2e-test-1",
        "key_insights": ["The Tension Engine framework is useful."],
        "breakthrough_moments": ["First insight breakthrough."],
        "emotional_beats": [{"description": "Deep session moment", "intensity": 0.9}],
    }
    
    loop = asyncio.new_event_loop()
    try:
        res = loop.run_until_complete(pipeline.process_session(report, "coach-1", "JPR"))
        assert res.success
        # Validated piece check
        for p in res.output.content_pieces:
            # Short-form video script got filtered out due to short text failure,
            # or passed if it satisfies length (video script candidate gets prepended [VIDEO SCRIPT])
            # Let's ensure if it passes, validation_status is PASSED
            if p.validation_status == ValidationStatus.passed:
                assert p.fingerprint_id is not None
    finally:
        loop.close()
