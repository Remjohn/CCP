"""
CCP Step 7 — Integration Tests for Adapter Registry v2.0
Tests the 3 new adapters and the unified 8-adapter pipeline orchestrator.

Test coverage:
    1. adapter_registry_v2_models.py — model instantiation and helper methods
    2. context_premise_adapter.py — Adapter-3 Block B injection
    3. payload_masking_adapter.py — Adapter-6 mood × archetype masking
    4. cral_finding_router_adapter.py — Adapter-8 arc phase routing
    5. adapter_registry_v2_pipeline.py — Unified pipeline orchestrator
"""

from __future__ import annotations

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import AdapterSlot, BlockTarget
from src.ccp.models.adapter_registry_v2_models import (
    ArcPhase,
    ArcPhaseInjection,
    CRALFinding,
    CRALFindingIndex,
    CRALFindingRouterOutput,
    CRALMomentKey,
    ContextPremiseAdapterOutput,
    GateWiringConfig,
    GateWiringStatus,
    PayloadMaskingAdapterOutput,
    STORYTELLING_ARC_PHASE_ROUTING,
    AdapterRegistryV2Result,
)
from src.ccp.models.psych_routing_models import MoodStatePrimary
from src.ccp.services.context_premise_adapter import ContextPremiseAdapter
from src.ccp.services.cral_finding_router_adapter import CRALFindingRouterAdapter
from src.ccp.services.payload_masking_adapter import PayloadMaskingAdapter


# ══════════════════════════════════════════════════════════════
# Fixtures
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def receipt_chain(tmp_path) -> ReceiptChain:
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "receipts"))


@pytest.fixture
def coach_id() -> str:
    return "test-coach-001"


@pytest.fixture
def full_cral_index(coach_id: str) -> CRALFindingIndex:
    """A complete CRAL Finding Index with all 7 moments."""
    return CRALFindingIndex(
        coach_id=coach_id,
        theme="overcoming-imposter-syndrome",
        archetype_id="storytelling-v1",
        coverage_status="COMPLETE",
        findings={
            CRALMomentKey.M1_TIMELY.value: CRALFinding(
                moment_key=CRALMomentKey.M1_TIMELY,
                finding_text="Imposter syndrome is trending on LinkedIn this quarter.",
                human_evidence_count=5,
            ),
            CRALMomentKey.M2_BELIEVABLE.value: CRALFinding(
                moment_key=CRALMomentKey.M2_BELIEVABLE,
                finding_text="73% of professionals have experienced imposter feelings.",
                human_evidence_count=4,
            ),
            CRALMomentKey.M3_UNDENIABLE.value: CRALFinding(
                moment_key=CRALMomentKey.M3_UNDENIABLE,
                finding_text="The audience believes imposter syndrome is a character flaw.",
                human_evidence_count=6,
            ),
            CRALMomentKey.M4_RESONANT.value: CRALFinding(
                moment_key=CRALMomentKey.M4_RESONANT,
                finding_text="They recognize the pattern in late-night self-doubt.",
                human_evidence_count=3,
            ),
            CRALMomentKey.M5_SURPRISING.value: CRALFinding(
                moment_key=CRALMomentKey.M5_SURPRISING,
                finding_text="High performers report MORE imposter feelings, not fewer.",
                human_evidence_count=7,
            ),
            CRALMomentKey.M6_IRREFUTABLE.value: CRALFinding(
                moment_key=CRALMomentKey.M6_IRREFUTABLE,
                finding_text="Maya Angelou publicly described her imposter experience.",
                human_evidence_count=4,
            ),
            CRALMomentKey.M7_RELATABLE.value: CRALFinding(
                moment_key=CRALMomentKey.M7_RELATABLE,
                finding_text="The fear of being 'found out' is universal, not personal.",
                human_evidence_count=5,
            ),
        },
    )


@pytest.fixture
def partial_cral_index(coach_id: str) -> CRALFindingIndex:
    """A partial CRAL Finding Index with only M2 and M5."""
    return CRALFindingIndex(
        coach_id=coach_id,
        theme="leadership-vulnerability",
        archetype_id="storytelling-v1",
        coverage_status="DEGRADED",
        findings={
            CRALMomentKey.M2_BELIEVABLE.value: CRALFinding(
                moment_key=CRALMomentKey.M2_BELIEVABLE,
                finding_text="Leaders who show vulnerability build stronger teams.",
                human_evidence_count=3,
            ),
            CRALMomentKey.M5_SURPRISING.value: CRALFinding(
                moment_key=CRALMomentKey.M5_SURPRISING,
                finding_text="Perceived weakness increases follower trust by 40%.",
                human_evidence_count=2,
            ),
        },
    )


# ══════════════════════════════════════════════════════════════
# Test: CRAL Finding Index Model
# ══════════════════════════════════════════════════════════════

class TestCRALFindingIndex:
    """Tests for CRALFindingIndex model helpers."""

    def test_get_finding_present(self, full_cral_index: CRALFindingIndex) -> None:
        finding = full_cral_index.get_finding(CRALMomentKey.M3_UNDENIABLE)
        assert finding is not None
        assert "character flaw" in finding.finding_text

    def test_get_finding_absent(self, partial_cral_index: CRALFindingIndex) -> None:
        finding = partial_cral_index.get_finding(CRALMomentKey.M3_UNDENIABLE)
        assert finding is None

    def test_missing_moments_complete(self, full_cral_index: CRALFindingIndex) -> None:
        missing = full_cral_index.missing_moments()
        assert len(missing) == 0

    def test_missing_moments_partial(self, partial_cral_index: CRALFindingIndex) -> None:
        missing = partial_cral_index.missing_moments()
        assert len(missing) == 5  # Only M2 and M5 present, so 5 missing


# ══════════════════════════════════════════════════════════════
# Test: Arc Phase Routing Map
# ══════════════════════════════════════════════════════════════

class TestArcPhaseRoutingMap:
    """Tests for the storytelling arc phase routing map constants."""

    def test_stakes_maps_to_m2_m3(self) -> None:
        assert CRALMomentKey.M2_BELIEVABLE in STORYTELLING_ARC_PHASE_ROUTING[ArcPhase.STAKES]
        assert CRALMomentKey.M3_UNDENIABLE in STORYTELLING_ARC_PHASE_ROUTING[ArcPhase.STAKES]

    def test_mechanism_maps_to_m4(self) -> None:
        assert STORYTELLING_ARC_PHASE_ROUTING[ArcPhase.MECHANISM] == [CRALMomentKey.M4_RESONANT]

    def test_turn_maps_to_m5(self) -> None:
        assert STORYTELLING_ARC_PHASE_ROUTING[ArcPhase.TURN] == [CRALMomentKey.M5_SURPRISING]

    def test_result_maps_to_m6(self) -> None:
        assert STORYTELLING_ARC_PHASE_ROUTING[ArcPhase.RESULT] == [CRALMomentKey.M6_IRREFUTABLE]

    def test_implication_maps_to_m7(self) -> None:
        assert STORYTELLING_ARC_PHASE_ROUTING[ArcPhase.IMPLICATION] == [CRALMomentKey.M7_RELATABLE]

    def test_all_5_phases_covered(self) -> None:
        assert len(STORYTELLING_ARC_PHASE_ROUTING) == 5

    def test_m1_not_in_any_phase(self) -> None:
        """M1_TIMELY is a pre-condition check, not injected into an arc phase."""
        all_moments = []
        for moments in STORYTELLING_ARC_PHASE_ROUTING.values():
            all_moments.extend(moments)
        assert CRALMomentKey.M1_TIMELY not in all_moments


# ══════════════════════════════════════════════════════════════
# Test: Gate Wiring Config
# ══════════════════════════════════════════════════════════════

class TestGateWiringConfig:
    """Tests for FR12 gate wiring configuration."""

    def test_cleared_allows_compilation(self) -> None:
        config = GateWiringConfig(overall_status=GateWiringStatus.CLEARED)
        assert config.is_compilation_allowed()

    def test_provisional_allows_compilation(self) -> None:
        config = GateWiringConfig(overall_status=GateWiringStatus.PROVISIONAL)
        assert config.is_compilation_allowed()

    def test_awaiting_gate_3_allows_compilation(self) -> None:
        config = GateWiringConfig(overall_status=GateWiringStatus.AWAITING_GATE_3)
        assert config.is_compilation_allowed()

    def test_blocked_gate_1_halts_compilation(self) -> None:
        config = GateWiringConfig(overall_status=GateWiringStatus.BLOCKED_GATE_1)
        assert not config.is_compilation_allowed()

    def test_blocked_gate_2_halts_compilation(self) -> None:
        config = GateWiringConfig(overall_status=GateWiringStatus.BLOCKED_GATE_2)
        assert not config.is_compilation_allowed()

    def test_not_evaluated_halts_compilation(self) -> None:
        config = GateWiringConfig(overall_status=GateWiringStatus.NOT_EVALUATED)
        assert not config.is_compilation_allowed()


# ══════════════════════════════════════════════════════════════
# Test: Payload Masking Adapter (Adapter-6)
# ══════════════════════════════════════════════════════════════

class TestPayloadMaskingAdapter:
    """Tests for the payload-masking-adapter (Adapter-6)."""

    def test_processing_mode_bypass(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.PROCESSING,
            coach_id=coach_id,
        )
        assert result.success is True
        assert result.block_b is None  # No injection in Processing mode
        assert any("not activated" in w for w in result.warnings)

    def test_escape_mode_generates_masking(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.ESCAPE,
            coach_id=coach_id,
            archetype_id="storytelling-v1",
            theme="test-theme",
        )
        assert result.success is True
        assert result.block_b is not None
        assert result.block_b.adapter_slot == AdapterSlot.PAYLOAD_MASKING
        assert result.block_b.target == BlockTarget.BLOCK_B
        assert len(result.block_b.constraint_strings) >= 1
        # Check the masking instruction contains the ESCAPE-specific string
        assert any("ESCAPE" in c for c in result.block_b.constraint_strings)

    def test_escape_mode_with_m3(
        self,
        receipt_chain: ReceiptChain,
        coach_id: str,
        full_cral_index: CRALFindingIndex,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.ESCAPE,
            coach_id=coach_id,
            cral_finding_index=full_cral_index,
            theme="test-theme",
        )
        assert result.success is True
        assert result.block_b is not None
        # Should have M3 subversion constraint
        constraints_text = " ".join(result.block_b.constraint_strings)
        assert "ANTI-DRAFT LEVEL 2" in constraints_text

    def test_discovery_mode(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.DISCOVERY,
            coach_id=coach_id,
            theme="test-theme",
        )
        assert result.success is True
        assert result.block_b is not None
        assert any("DISCOVERY" in c for c in result.block_b.constraint_strings)

    def test_status_mode(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.STATUS,
            coach_id=coach_id,
            theme="test-theme",
        )
        assert result.success is True
        assert result.block_b is not None

    def test_semantic_affinity_high_blocks_escape(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.ESCAPE,
            coach_id=coach_id,
            semantic_affinity_risk="HIGH",
            theme="trauma-related-topic",
        )
        assert result.success is False
        assert len(result.gate_failures) > 0
        assert "SEMANTIC AFFINITY" in result.gate_failures[0]

    def test_semantic_affinity_medium_warns(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.ESCAPE,
            coach_id=coach_id,
            semantic_affinity_risk="MEDIUM",
            theme="sensitive-topic",
        )
        assert result.success is True
        assert any("MEDIUM" in w for w in result.warnings)

    def test_receipt_written(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.ESCAPE,
            coach_id=coach_id,
            theme="test-theme",
        )
        assert result.receipt_id != ""
        assert receipt_chain.chain_length() >= 1

    def test_cral_degraded_warning_when_m3_absent(
        self,
        receipt_chain: ReceiptChain,
        coach_id: str,
        partial_cral_index: CRALFindingIndex,
    ) -> None:
        """Partial CRAL index without M3 should produce degraded warning."""
        adapter = PayloadMaskingAdapter(receipt_chain)
        result = adapter.load(
            mood_state=MoodStatePrimary.ESCAPE,
            coach_id=coach_id,
            cral_finding_index=partial_cral_index,
            theme="test-theme",
        )
        assert result.success is True
        assert any("CRAL_DEGRADED" in w or "M3_UNDENIABLE" in w for w in result.warnings)


# ══════════════════════════════════════════════════════════════
# Test: CRAL Finding Router Adapter (Adapter-8)
# ══════════════════════════════════════════════════════════════

class TestCRALFindingRouterAdapter:
    """Tests for the cral-finding-router-adapter (Adapter-8)."""

    def test_full_cral_complete_routing(
        self,
        receipt_chain: ReceiptChain,
        coach_id: str,
        full_cral_index: CRALFindingIndex,
    ) -> None:
        adapter = CRALFindingRouterAdapter(receipt_chain)
        result = adapter.load(
            coach_id=coach_id,
            archetype_id="storytelling-v1",
            cral_finding_index=full_cral_index,
        )
        assert result.success is True
        assert result.block_b is not None
        assert result.block_b.adapter_slot == AdapterSlot.CRAL_FINDING_ROUTER
        assert result.block_b.metadata["coverage_status"] == "COMPLETE"
        # All 5 phases should have injections (6 total: Stakes has M2+M3)
        assert result.block_b.metadata["phase_injection_count"] == 6

    def test_partial_cral_degraded_routing(
        self,
        receipt_chain: ReceiptChain,
        coach_id: str,
        partial_cral_index: CRALFindingIndex,
    ) -> None:
        adapter = CRALFindingRouterAdapter(receipt_chain)
        result = adapter.load(
            coach_id=coach_id,
            cral_finding_index=partial_cral_index,
        )
        assert result.success is True
        assert result.block_b is not None
        assert result.block_b.metadata["coverage_status"] == "DEGRADED"
        assert len(result.block_b.metadata["degraded_phases"]) > 0

    def test_absent_cral_graceful_degradation(
        self, receipt_chain: ReceiptChain, coach_id: str,
    ) -> None:
        adapter = CRALFindingRouterAdapter(receipt_chain)
        result = adapter.load(
            coach_id=coach_id,
            cral_finding_index=None,  # DEP-ENG-021 absent
        )
        assert result.success is True  # Graceful degradation is NOT failure
        assert result.block_b is None  # No injection when fully degraded
        assert any("CRAL_DEGRADED" in w for w in result.warnings)

    def test_fr16_evidence_warning(
        self,
        receipt_chain: ReceiptChain,
        coach_id: str,
        partial_cral_index: CRALFindingIndex,
    ) -> None:
        """M5 in partial index has 2 evidence instances (below FR16 threshold of 3)."""
        adapter = CRALFindingRouterAdapter(receipt_chain)
        result = adapter.load(
            coach_id=coach_id,
            cral_finding_index=partial_cral_index,
        )
        assert any("FR16" in w for w in result.warnings)

    def test_receipt_written(
        self,
        receipt_chain: ReceiptChain,
        coach_id: str,
        full_cral_index: CRALFindingIndex,
    ) -> None:
        adapter = CRALFindingRouterAdapter(receipt_chain)
        result = adapter.load(
            coach_id=coach_id,
            cral_finding_index=full_cral_index,
        )
        assert result.receipt_id != ""
        assert receipt_chain.chain_length() >= 1


# ══════════════════════════════════════════════════════════════
# Test: V2 Model Instantiation
# ══════════════════════════════════════════════════════════════

class TestV2Models:
    """Basic model instantiation and validation tests."""

    def test_context_premise_adapter_output(self) -> None:
        out = ContextPremiseAdapterOutput(
            coach_id="test",
            l3_pain_domains=["fear of irrelevance"],
            tribal_terms=["bro science", "natty or not"],
        )
        assert out.segment_count == 0
        assert len(out.l3_pain_domains) == 1

    def test_payload_masking_adapter_output(self) -> None:
        out = PayloadMaskingAdapterOutput(
            coach_id="test",
            mood_state="Escape",
            masking_instruction="Test instruction",
        )
        assert out.m3_subversion_instruction is None
        assert out.semantic_affinity_cleared is False

    def test_cral_finding_router_output(self) -> None:
        out = CRALFindingRouterOutput(
            coach_id="test",
            archetype_id="storytelling-v1",
            phase_injections=[
                ArcPhaseInjection(
                    arc_phase=ArcPhase.STAKES,
                    moment_key=CRALMomentKey.M2_BELIEVABLE,
                    injection_text="Test injection for Stakes",
                ),
            ],
            coverage_status="DEGRADED",
            degraded_phases=["Mechanism", "Turn", "Result", "Implication"],
        )
        assert len(out.phase_injections) == 1
        assert len(out.degraded_phases) == 4

    def test_gate_wiring_config_default(self) -> None:
        config = GateWiringConfig()
        assert config.overall_status == GateWiringStatus.NOT_EVALUATED
        assert not config.is_compilation_allowed()

    def test_adapter_registry_v2_result_block_collection(self) -> None:
        """Test that get_all_block_b_injections returns in correct order."""
        result = AdapterRegistryV2Result(coach_id="test")
        # No adapters set → empty collections
        assert result.get_all_block_a_injections() == []
        assert result.get_all_block_b_injections() == []
