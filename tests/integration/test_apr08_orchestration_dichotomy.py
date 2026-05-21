import pytest
from pydantic import ValidationError
from src.ccp.core.primitive_schemas import PrimitiveCandidate, PrimitiveFamily, CoalitionSignature, EdgeProduct


class TestSchemaRejection:
    """AC1: Pydantic field_validator raises ValueError on generic evidence."""

    def test_ac1_generic_evidence_quote_rejected(self):
        with pytest.raises(ValidationError):
            PrimitiveCandidate(
                primitive_id="PRM-STR-008",
                primitive_name="Narrative Arc Builder",
                family=PrimitiveFamily.STRUCTURAL,
                evidence_quote="Most people agree that storytelling matters",
                evidence_fidelity=0.7,
                emotional_charge=0.5,
                tribal_density=0.4,
                speakability=0.6,
            )

    def test_ac1_valid_evidence_quote_accepted(self):
        c = PrimitiveCandidate(
            primitive_id="PRM-STR-008",
            primitive_name="Narrative Arc Builder",
            family=PrimitiveFamily.STRUCTURAL,
            evidence_quote="When my client told me she finally stood up to her boss after our session",
            evidence_fidelity=0.7,
            emotional_charge=0.5,
            tribal_density=0.4,
            speakability=0.6,
        )
        assert c.primitive_id == "PRM-STR-008"

    def test_ac8_invalid_primitive_id_format_rejected(self):
        with pytest.raises(ValidationError):
            PrimitiveCandidate(
                primitive_id="STR",
                primitive_name="Narrative Arc Builder",
                family=PrimitiveFamily.STRUCTURAL,
                evidence_quote="When my client told me she finally stood up to her boss after our session",
                evidence_fidelity=0.7,
                emotional_charge=0.5,
                tribal_density=0.4,
                speakability=0.6,
            )


class TestAntiCentroidGate:
    """AC2: All candidates with low emotional_charge rejected."""

    def test_ac2_all_low_emotional_charge_rejected(self):
        from src.ccp.core.orchestration_dichotomy import DichotomyGate, DichotomyGateRejection
        candidates = [
            PrimitiveCandidate(primitive_id="PRM-TNS-001", primitive_name="Tension Builder", family=PrimitiveFamily.TENSION, evidence_quote="My client said she felt trapped between two identities", evidence_fidelity=0.8, emotional_charge=0.2, tribal_density=0.5, speakability=0.6),
            PrimitiveCandidate(primitive_id="PRM-STR-002", primitive_name="Structure Anchor", family=PrimitiveFamily.STRUCTURAL, evidence_quote="He described his routine as a prison of his own making", evidence_fidelity=0.7, emotional_charge=0.2, tribal_density=0.4, speakability=0.5),
            PrimitiveCandidate(primitive_id="PRM-IDN-003", primitive_name="Identity Forge", family=PrimitiveFamily.IDENTITY, evidence_quote="She told me she doesn't know who she is anymore", evidence_fidelity=0.6, emotional_charge=0.1, tribal_density=0.3, speakability=0.4),
            PrimitiveCandidate(primitive_id="PRM-EMO-004", primitive_name="Emotional Charge", family=PrimitiveFamily.EMOTIONAL, evidence_quote="He wept as he recounted his father's last words to him", evidence_fidelity=0.9, emotional_charge=0.2, tribal_density=0.6, speakability=0.7),
        ]
        gate = DichotomyGate()
        with pytest.raises(DichotomyGateRejection, match="CENTROID_DRIFT_DETECTED"):
            gate.validate(candidates, "coach-001")


class TestCoalitionMinimum:
    """AC5: Only 1 candidate after filtering -> coalition rejected."""

    def test_ac5_single_candidate_rejected(self):
        from src.ccp.core.coalition_engine import CoalitionEngine
        candidates = [
            PrimitiveCandidate(primitive_id="PRM-TNS-001", primitive_name="Tension Builder", family=PrimitiveFamily.TENSION, evidence_quote="My client said she felt trapped between two identities", evidence_fidelity=0.8, emotional_charge=0.5, tribal_density=0.5, speakability=0.6),
        ]
        engine = CoalitionEngine()
        with pytest.raises(ValueError, match="Coalition minimum not met"):
            engine.assemble(candidates, "coach-001")


class TestEdgeProductRouting:
    """AC7: Dominant PRM-TNS-001 -> transformation-pressure-edge."""

    def test_ac7_dominant_tension_routes_correctly(self):
        from src.ccp.core.coalition_engine import CoalitionEngine
        candidates = [
            PrimitiveCandidate(primitive_id="PRM-TNS-001", primitive_name="Tension Builder", family=PrimitiveFamily.TENSION, evidence_quote="My client said she felt trapped between two identities", evidence_fidelity=0.9, emotional_charge=0.8, tribal_density=0.7, speakability=0.6),
            PrimitiveCandidate(primitive_id="PRM-STR-002", primitive_name="Structure Anchor", family=PrimitiveFamily.STRUCTURAL, evidence_quote="He described his routine as a prison of his own making", evidence_fidelity=0.6, emotional_charge=0.4, tribal_density=0.3, speakability=0.5),
        ]
        engine = CoalitionEngine()
        coalition, edge = engine.assemble(candidates, "coach-001")
        assert edge.ccf_routing_target == "transformation-pressure-edge"
        assert coalition.dominant_primitive_id == "PRM-TNS-001"
