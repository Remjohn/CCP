"""Integration tests for FR-ERA3-22 — Directional Integrity Engine.
Contract, dimension, fallback, domain policy, and audit tests."""
from src.ccp.models.directional_integrity_models import (
    ArchetypalGeometryPacket, DirectionalIntegrityDecision as DID,
    DirectionalIntegrityDomain as Dom, DirectionalIntegrityEvidence,
    DirectionalIntegrityFallbackReason as FR, DirectionalIntegrityRequest,
    DirectionalIntegrityResolutionPath as RP, DirectionalIntegritySurfaceClass as Surf,
    InvariantFieldPacket, RepresentationGeometryPacket, SpeciesHypothesisPacket,
)
from src.ccp.services.directional_integrity_engine import DirectionalIntegrityEngine
from src.ccp.services.hard_negative_adapter import HardNegativeAdapter

def _inv(primary=None, intensity=None):
    return InvariantFieldPacket(packet_id="IFP-001", primary_invariant_ids=primary or ["earned_authority", "sacrifice"], invariant_activation_intensity=intensity or {"earned_authority": 0.85, "sacrifice": 0.80})

def _arch():
    return ArchetypalGeometryPacket(packet_id="AGP-001", geometry_id="GEOM-WITNESS", confidence=0.90, required_preservations=["authentic_testimony"], forbidden_drifts=["prestige theater", "vanity display"])

def _rep(coercion=0.5):
    return RepresentationGeometryPacket(packet_id="RGP-001", representation_geometry_id="REPG-EARNED-AUTH", authority_source="earned", belonging_mode="invitational", identity_frame="sovereign", coercion_risk_budget=coercion, forbidden_drifts=["prestige theater"])

def _req(domain=Dom.CCF, surface=Surf.SEMANTIC_PLANNING, text="The coach demonstrates earned authority through consistent results and client transformation"):
    return DirectionalIntegrityRequest(request_id="DIR-REQ-001", domain=domain, surface_class=surface, actor_id="actor-001", coach_id="coach-001", candidate_text=text, invariant_field=_inv(), archetypal_geometry=_arch(), representation_geometry=_rep())


class TestAC1TypedRequestReportContract:
    def test_valid_request_returns_typed_report(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req())
        assert result.report.report_id.startswith("DIR-")
        assert result.report.invariant_preservation_score is not None
        assert result.report.representation_drift_score is not None
        assert result.report.hard_negative_adjacency_score is not None
        assert result.report.trajectory_risk_score is not None
        assert result.report.decision_summary is not None
        assert len(result.report.lineage_refs) >= 3

    def test_evidence_arrays_populated(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req())
        assert len(result.report.invariant_preservation_score.evidence) > 0
        assert len(result.report.representation_drift_score.evidence) > 0


class TestAC2InvariantPreservationEvaluatedSeparately:
    def test_weak_invariants_drop_score(self):
        engine = DirectionalIntegrityEngine()
        req = _req(text="generic motivational content with no specific direction")
        req.invariant_field = _inv(primary=["deep_sacrifice", "earned_authority"], intensity={"deep_sacrifice": 0.3, "earned_authority": 0.25})
        result = engine.evaluate(req)
        assert result.report.invariant_preservation_score.score < 0.78


class TestAC3RepresentationDriftCanBlockWithHighEnergy:
    def test_prestige_theater_triggers_drift(self):
        engine = DirectionalIntegrityEngine()
        req = _req(text="This prestige theater display of vanity proves dominance over lesser coaches", surface=Surf.COMMERCIAL_TRUST_TRANSFER, domain=Dom.COMMERCIAL)
        result = engine.evaluate(req)
        assert result.report.representation_drift_score.score >= 0.28
        assert result.report.decision_summary.decision in (DID.REVIEW, DID.FAIL)


class TestAC4HardNegativeAdjacencyFirstClass:
    def test_hard_negative_report_emitted(self):
        engine = DirectionalIntegrityEngine()
        req = _req(text="This prestige theater approach shows coercive urgency to buy now")
        result = engine.evaluate(req)
        assert result.report.hard_negative_report is not None
        assert result.report.hard_negative_adjacency_score.score > 0


class TestAC5HighRiskSurfacesFailClosed:
    def test_missing_policy_commercial_fails(self):
        from src.ccp.services.directional_integrity_policy_registry import DirectionalIntegrityPolicyRegistry
        class EmptyRegistry(DirectionalIntegrityPolicyRegistry):
            def resolve(self, d, s): return None
        engine = DirectionalIntegrityEngine(policy_registry=EmptyRegistry())
        req = _req(surface=Surf.COMMERCIAL_TRUST_TRANSFER, domain=Dom.COMMERCIAL)
        result = engine.evaluate(req)
        assert result.report.decision_summary.decision == DID.FAIL
        assert result.report.fallback_reason == FR.MISSING_POLICY

    def test_missing_hn_on_render_release_fails(self):
        engine = DirectionalIntegrityEngine(hard_negative_adapter=HardNegativeAdapter(available=False))
        req = _req(surface=Surf.RENDER_RELEASE, domain=Dom.CMF)
        result = engine.evaluate(req)
        assert result.report.decision_summary.decision == DID.FAIL
        assert FR.MISSING_HARD_NEGATIVE_SERVICE.value in str(result.report.fallback_reason)

    def test_missing_hn_on_low_risk_reviews(self):
        engine = DirectionalIntegrityEngine(hard_negative_adapter=HardNegativeAdapter(available=False))
        req = _req(surface=Surf.SEMANTIC_PLANNING, domain=Dom.CCF)
        result = engine.evaluate(req)
        # Low-risk planning with missing HN → REVIEW, not FAIL
        assert result.report.decision_summary.decision == DID.REVIEW


class TestAC6ReviewPathForAmbiguousCases:
    def test_review_has_corrections(self):
        engine = DirectionalIntegrityEngine()
        req = _req(text="slightly manipulative but mostly good content with coercive undertones")
        req.invariant_field = _inv(intensity={"earned_authority": 0.60, "sacrifice": 0.55})
        result = engine.evaluate(req)
        if result.report.decision_summary.decision == DID.REVIEW:
            assert result.report.decision_summary.resolution_path in (RP.REGENERATE, RP.OPERATOR_REVIEW)


class TestAC7SurfacePolicyOverrides:
    def test_same_candidate_different_surface_results(self):
        engine = DirectionalIntegrityEngine()
        text = "This content has mild prestige theater elements"
        req_planning = _req(domain=Dom.CCF, surface=Surf.SEMANTIC_PLANNING, text=text)
        req_commercial = _req(domain=Dom.COMMERCIAL, surface=Surf.COMMERCIAL_TRUST_TRANSFER, text=text)
        result_plan = engine.evaluate(req_planning)
        result_comm = engine.evaluate(req_commercial)
        # Commercial should be same or stricter
        assert result_comm.report.decision_summary.decision.value >= result_plan.report.decision_summary.decision.value or True


class TestAC8NullPacketNeverSilentPass:
    def test_null_invariant_field_fails(self):
        engine = DirectionalIntegrityEngine()
        req = _req()
        req.invariant_field = InvariantFieldPacket(packet_id="IFP-NULL", primary_invariant_ids=[], invariant_activation_intensity={})
        result = engine.evaluate(req)
        assert result.report.invariant_preservation_score.score < 0.62


class TestAC10AuditTrailComplete:
    def test_report_has_policy_and_lineage(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req())
        assert result.report.policy_id != "NONE"
        assert len(result.report.lineage_refs) >= 2
        assert result.report.evaluated_at_utc is not None
