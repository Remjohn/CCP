"""Domain policy tests for FR-ERA3-22 — per §10.2.D."""
from src.ccp.models.directional_integrity_models import (
    ArchetypalGeometryPacket, DirectionalIntegrityDecision as DID,
    DirectionalIntegrityDomain as Dom, DirectionalIntegrityRequest,
    DirectionalIntegritySurfaceClass as Surf, InvariantFieldPacket,
    RepresentationGeometryPacket,
)
from src.ccp.services.directional_integrity_engine import DirectionalIntegrityEngine

def _inv(): return InvariantFieldPacket(packet_id="IFP-DP", primary_invariant_ids=["earned_authority"], invariant_activation_intensity={"earned_authority": 0.75})
def _arch(): return ArchetypalGeometryPacket(packet_id="AGP-DP", geometry_id="GEOM-RALLY", confidence=0.85, required_preservations=["conviction"], forbidden_drifts=["prestige theater"])
def _rep(): return RepresentationGeometryPacket(packet_id="RGP-DP", representation_geometry_id="REPG-EARNED", authority_source="earned", belonging_mode="invitational", identity_frame="sovereign", coercion_risk_budget=0.4)
def _req(d, s, t):
    return DirectionalIntegrityRequest(request_id="DIR-DP-001", domain=d, surface_class=s, actor_id="act", coach_id="c", candidate_text=t, invariant_field=_inv(), archetypal_geometry=_arch(), representation_geometry=_rep())

class TestSameArtifactPassesPlanningFailsCommercial:
    def test(self):
        engine = DirectionalIntegrityEngine()
        mild = "some prestige theater elements but mostly clean earned authority content"
        r_plan = engine.evaluate(_req(Dom.CCF, Surf.SEMANTIC_PLANNING, mild))
        r_comm = engine.evaluate(_req(Dom.COMMERCIAL, Surf.COMMERCIAL_TRUST_TRANSFER, mild))
        # Commercial uses tighter thresholds so drift is more likely to block
        comm_drift = r_comm.report.representation_drift_score.threshold_block
        plan_drift = r_plan.report.representation_drift_score.threshold_block
        assert comm_drift <= plan_drift

class TestReactionReviewsButBlocksPublicShare:
    def test_social_reaction_reviews_or_blocks(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req(Dom.REACTIONS, Surf.SOCIAL_REACTION, "vanity display with prestige theater of coercive urgency"))
        assert result.report.decision_summary.decision in (DID.REVIEW, DID.FAIL)

class TestWebinarCTABlocksOnCoerciveAuthority:
    def test(self):
        engine = DirectionalIntegrityEngine()
        result = engine.evaluate(_req(Dom.WEBINAR, Surf.LONG_FORM_AUTHORITY, "manipulation shame coercive urgency prestige theater vanity"))
        assert result.report.decision_summary.decision == DID.FAIL
