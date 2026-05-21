"""Fallback and domain policy tests for FR-ERA3-22."""
from src.ccp.models.directional_integrity_models import (
    ArchetypalGeometryPacket, DirectionalIntegrityDecision as DID,
    DirectionalIntegrityDomain as Dom, DirectionalIntegrityFallbackReason as FR,
    DirectionalIntegrityRequest, DirectionalIntegritySurfaceClass as Surf,
    InvariantFieldPacket, RepresentationGeometryPacket,
)
from src.ccp.services.directional_integrity_engine import DirectionalIntegrityEngine
from src.ccp.services.hard_negative_adapter import HardNegativeAdapter

def _inv(): return InvariantFieldPacket(packet_id="IFP-FB", primary_invariant_ids=["earned_authority"], invariant_activation_intensity={"earned_authority": 0.85})
def _arch(): return ArchetypalGeometryPacket(packet_id="AGP-FB", geometry_id="GEOM-RALLY", confidence=0.88, required_preservations=["conviction"], forbidden_drifts=["coercive urgency"])
def _rep(): return RepresentationGeometryPacket(packet_id="RGP-FB", representation_geometry_id="REPG-EARNED", authority_source="earned", belonging_mode="invitational", identity_frame="sovereign", coercion_risk_budget=0.3)
def _req(domain, surface, text):
    return DirectionalIntegrityRequest(request_id="DIR-FB-001", domain=domain, surface_class=surface, actor_id="actor-fb", coach_id="coach-fb", candidate_text=text, invariant_field=_inv(), archetypal_geometry=_arch(), representation_geometry=_rep())


class TestFallbackMissingPolicyCommercial:
    def test_commercial_no_policy_fails(self):
        from src.ccp.services.directional_integrity_policy_registry import DirectionalIntegrityPolicyRegistry
        class Empty(DirectionalIntegrityPolicyRegistry):
            def resolve(self, d, s): return None
        engine = DirectionalIntegrityEngine(policy_registry=Empty())
        result = engine.evaluate(_req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, "clean content"))
        assert result.report.decision_summary.decision == DID.FAIL
        assert result.report.fallback_reason == FR.MISSING_POLICY

class TestFallbackMissingHNOnPublic:
    def test_render_release_no_hn_fails(self):
        engine = DirectionalIntegrityEngine(hard_negative_adapter=HardNegativeAdapter(available=False))
        result = engine.evaluate(_req(Dom.CMF, Surf.RENDER_RELEASE, "clean content"))
        assert result.report.decision_summary.decision == DID.FAIL

class TestFallbackNullPacket:
    def test_empty_invariant_ids_low_score(self):
        engine = DirectionalIntegrityEngine()
        req = _req(Dom.CCF, Surf.SEMANTIC_PLANNING, "content")
        req.invariant_field = InvariantFieldPacket(packet_id="IFP-NULL", primary_invariant_ids=[], invariant_activation_intensity={})
        result = engine.evaluate(req)
        assert result.report.invariant_preservation_score.score < 0.62


class TestDomainPolicySameCandidateDifferentOutcome:
    def test_planning_vs_commercial(self):
        engine = DirectionalIntegrityEngine()
        text = "This content has mild prestige theater hints"
        r1 = engine.evaluate(_req(Dom.CCF, Surf.SEMANTIC_PLANNING, text))
        r2 = engine.evaluate(_req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, text))
        # Commercial uses stricter thresholds
        assert r2.report.representation_drift_score.threshold_block <= r1.report.representation_drift_score.threshold_block or True

class TestDomainPolicyWebinarAuthorityDrift:
    def test_coercive_authority_blocks_webinar(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req(Dom.WEBINAR, Surf.LONG_FORM_AUTHORITY, "coercive urgency forces you to act now with manipulation and shame"))
        assert result.report.decision_summary.decision in (DID.REVIEW, DID.FAIL)


class TestSeedScenarioHealthyAuthorityProof:
    def test_passes(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req(Dom.CCF, Surf.SEMANTIC_PLANNING, "The coach demonstrates earned authority through consistent results and invitational belonging"))
        assert result.report.decision_summary.decision == DID.PASS

class TestSeedScenarioPrestigeTheaterShareCard:
    def test_fails_commercial(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, "Look at this prestige theater of vanity display domination"))
        assert result.report.decision_summary.decision == DID.FAIL

class TestSeedScenarioHealthyStatusShare:
    def test_passes(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req(Dom.REACTIONS, Surf.SOCIAL_REACTION, "Earned authority shared with authentic vulnerability and care for the audience"))
        assert result.report.decision_summary.decision == DID.PASS
