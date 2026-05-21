"""Integration tests for FR-ERA3-22 SFL Interop extension."""
from __future__ import annotations
from src.ccp.models.directional_integrity_models import (
    ArchetypalGeometryPacket, DirectionalIntegrityDecision as DID,
    DirectionalIntegrityDomain as Dom, DirectionalIntegrityRequest,
    DirectionalIntegritySurfaceClass as Surf, InvariantFieldPacket,
    RepresentationGeometryPacket, PerceptualInteropDecision,
    SemanticVsPerceptualDecisionState, JointRoutingAction, JointFailureClass,
    PerceptualAttachmentSummary,
)
from src.ccp.services.directional_integrity_engine import DirectionalIntegrityEngine

def _inv(intensity=0.85):
    return InvariantFieldPacket(
        packet_id="IFP-INT",
        primary_invariant_ids=["earned_authority"],
        invariant_activation_intensity={"earned_authority": intensity}
    )

def _arch():
    return ArchetypalGeometryPacket(
        packet_id="AGP-INT",
        geometry_id="GEOM-RALLY",
        confidence=0.88,
        required_preservations=["conviction"],
        forbidden_drifts=["coercive urgency"]
    )

def _rep(drifts=None):
    return RepresentationGeometryPacket(
        packet_id="RGP-INT",
        representation_geometry_id="REPG-EARNED",
        authority_source="earned",
        belonging_mode="invitational",
        identity_frame="sovereign",
        coercion_risk_budget=0.3,
        forbidden_drifts=drifts or []
    )

def _req(domain, surface, text, drifts=None, intensity=0.85):
    return DirectionalIntegrityRequest(
        request_id="DIR-INT-REQ-001",
        domain=domain,
        surface_class=surface,
        actor_id="actor-int",
        coach_id="coach-int",
        candidate_text=text,
        invariant_field=_inv(intensity),
        archetypal_geometry=_arch(),
        representation_geometry=_rep(drifts)
    )


class TestSFLInteropRouting:
    def test_semantic_fail_perceptual_pass_hard_block(self):
        # AC-22-SFL-1: Semantic FAIL + Perceptual PASS => Hard Block
        engine = DirectionalIntegrityEngine()
        # Trigger semantic fail via extreme drift text
        req = _req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, "This is prestige theater of vanity display")
        perceptual = PerceptualAttachmentSummary(
            perceptual_report_id="PIR-001",
            perceptual_decision=PerceptualInteropDecision.PASS,
            human_congruence_score=0.9,
            cognitive_imprint_score=0.9,
            lineage_refs=["PI-LINEAGE-1"]
        )
        report = engine.evaluate_interop(req, perceptual)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_FAIL__PERCEPTUAL_PASS
        assert report.failure_surface.failure_class == JointFailureClass.SEMANTIC_FAILURE
        assert report.routing_decision.action == JointRoutingAction.HARD_BLOCK
        assert not report.routing_decision.should_continue_automation
        assert not report.routing_decision.should_queue_operator_review

    def test_semantic_pass_perceptual_downgrade_commercial(self):
        # AC-22-SFL-2: Semantic PASS + Perceptual DOWNGRADE => Block on Commercial Trust Transfer
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, "Earned authority clean content")
        perceptual = PerceptualAttachmentSummary(
            perceptual_report_id="PIR-002",
            perceptual_decision=PerceptualInteropDecision.DOWNGRADE,
            lineage_refs=["PI-LINEAGE-2"]
        )
        report = engine.evaluate_interop(req, perceptual)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE
        assert report.failure_surface.failure_class == JointFailureClass.PERCEPTUAL_FAILURE
        assert report.routing_decision.action == JointRoutingAction.HARD_BLOCK
        assert not report.routing_decision.should_continue_automation

    def test_semantic_pass_perceptual_downgrade_render(self):
        # AC-22-SFL-2: Semantic PASS + Perceptual DOWNGRADE => Downgrade on Render Release
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.CMF, Surf.RENDER_RELEASE, "Earned authority clean content")
        perceptual = PerceptualAttachmentSummary(
            perceptual_report_id="PIR-003",
            perceptual_decision=PerceptualInteropDecision.DOWNGRADE,
            lineage_refs=["PI-LINEAGE-3"]
        )
        report = engine.evaluate_interop(req, perceptual)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE
        assert report.routing_decision.action == JointRoutingAction.DOWNGRADE_SURFACE
        assert not report.routing_decision.should_continue_automation

    def test_missing_perceptual_prerequisite_high_risk(self):
        # AC-22-SFL-3: Missing perceptual attachment on high-risk surface => Hold
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.CMF, Surf.RENDER_RELEASE, "Earned authority clean content")
        report = engine.evaluate_interop(req, None)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_PASS__PERCEPTUAL_MISSING
        assert report.failure_surface.failure_class == JointFailureClass.MISSING_PERCEPTUAL_PREREQUISITE
        assert report.routing_decision.action == JointRoutingAction.HOLD_FOR_PERCEPTUAL_PREREQUISITE
        assert report.routing_decision.should_queue_operator_review
        assert not report.routing_decision.should_continue_automation

    def test_semantic_review_perceptual_pass_operator_review(self):
        # AC-22-SFL-4: Semantic REVIEW + Perceptual PASS => Operator Review
        engine = DirectionalIntegrityEngine()
        # Trigger semantic review via lower intensity
        req = _req(Dom.CCF, Surf.SEMANTIC_PLANNING, "Earned authority clean content", intensity=0.45)
        perceptual = PerceptualAttachmentSummary(
            perceptual_report_id="PIR-004",
            perceptual_decision=PerceptualInteropDecision.PASS
        )
        report = engine.evaluate_interop(req, perceptual)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_REVIEW__PERCEPTUAL_PASS
        assert report.routing_decision.action == JointRoutingAction.OPERATOR_REVIEW
        assert report.routing_decision.should_queue_operator_review
        assert not report.routing_decision.should_continue_automation

    def test_joint_report_preservation_and_lineages(self):
        # AC-22-SFL-5: Verify field preservation, warning aggregation, and lineage merging
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.CCF, Surf.SEMANTIC_PLANNING, "Earned authority clean content")
        perceptual = PerceptualAttachmentSummary(
            perceptual_report_id="PIR-005",
            perceptual_decision=PerceptualInteropDecision.PASS,
            dependency_warnings=["Perceptual database lagging"],
            lineage_refs=["PI-CANONICAL-REF"]
        )
        report = engine.evaluate_interop(req, perceptual)
        assert report.semantic_report_id is not None
        assert report.perceptual_attachment is not None
        assert report.perceptual_attachment.perceptual_report_id == "PIR-005"
        # Lineages should merge req.invariant_field, req.archetypal_geometry, rep, and PI lineages
        assert "IFP-INT" in report.lineage_refs
        assert "AGP-INT" in report.lineage_refs
        assert "REPG-EARNED" in report.lineage_refs
        assert "PI-CANONICAL-REF" in report.lineage_refs
        assert "Perceptual database lagging" in report.dependency_warnings

    def test_high_risk_surface_hard_negative_block(self):
        # AC-22-SFL-6: Hard-negative block wins on high-risk surface
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, "Earned authority with prestige theater")
        perceptual = PerceptualAttachmentSummary(
            perceptual_report_id="PIR-006",
            perceptual_decision=PerceptualInteropDecision.PASS
        )
        report = engine.evaluate_interop(req, perceptual)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_FAIL__PERCEPTUAL_PASS
        assert report.routing_decision.action == JointRoutingAction.HARD_BLOCK
        assert any("hard-negative" in reason.lower() for reason in report.failure_surface.blocking_reasons)


    def test_low_risk_planning_no_perceptual_allows_legacy_pass(self):
        # AC-22-SFL-7: Low-risk planning allows legacy pass even if SFL is missing
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.CCF, Surf.SEMANTIC_PLANNING, "Earned authority clean content")
        report = engine.evaluate_interop(req, None)
        assert report.combined_state == SemanticVsPerceptualDecisionState.SEMANTIC_PASS__PERCEPTUAL_MISSING
        assert report.routing_decision.action == JointRoutingAction.CONTINUE
        assert report.routing_decision.should_continue_automation
        assert not report.routing_decision.should_queue_operator_review
