import asyncio
import pytest
from datetime import datetime, timezone
from src.ccp.models.archetype_container_runtime_models import (
    ArchetypeChoice,
    CoachResponseCapturePacket,
    CoalitionInputs,
    RuntimeStatus,
    SimilarityBand,
    SflBindingStatus,
    CompositionDepthClass,
    CompositionDepthPacket,
    SubliminalFunctionStackPacket,
    VariationProfileBinding,
    SflFunctionBinding,
)
from src.ccp.services.archetype_container_runtime import ArchetypeContainerRuntimeService

# Mock classes for testing
class MockSflHealth:
    def __init__(self, ready: bool = True):
        self.ready = ready

class MockSflLink:
    def __init__(self, archetype_name: str):
        self.archetype_name = archetype_name

class MockSflCrosswalkRecord:
    def __init__(self, artifact_id: str, archetype_name: str, preferred_function_ids: list[str]):
        self.artifact_id = artifact_id
        self.archetype_links = [MockSflLink(archetype_name)]
        self.preferred_function_ids = preferred_function_ids

class MockSflFunctionDefinition:
    def __init__(self, function_id: str, family_id: str, canonical_name: str, polarities: list[str]):
        self.function_id = function_id
        self.family_id = family_id
        self.canonical_name = canonical_name
        self.polarities = polarities

class MockSflRegistry:
    def __init__(self, ready: bool = True, crosswalks: dict = None, functions: dict = None):
        self._ready = ready
        self.crosswalks = crosswalks or {}
        self.functions = functions or {}

    def health(self):
        return MockSflHealth(self._ready)

    def get_crosswalk_bundle(self, name: str) -> dict:
        if name == "archetype_to_function_profile":
            return self.crosswalks
        return {}


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def _build_capture() -> CoachResponseCapturePacket:
    return CoachResponseCapturePacket(
        capture_id="CAP-SFL-TEST",
        coach_id="coach-sfl-999",
        transcript_text="Most coaches copy the market because they are scared to say who they actually disagree with. When I worked with Sarah in 2023, she lost 40 clients by trying to please everyone.",
        transcript_language="en",
        captured_at=datetime.now(timezone.utc),
        source_asset_id="AST-SFL-TEST",
        trigger_guard_session_id="TG-SFL-001",
    )


def _build_coalition() -> CoalitionInputs:
    return CoalitionInputs(
        coalition_id="COL-SFL-42",
        family_mix=["STR"],
        stance_polarity="high_contrast",
        source_count=1,
        evidence_strength=0.85,
        intended_business_job="authority_content",
    )


def test_sfl_bound_successfully_with_registry():
    """Test successful SFL resolution and execution contract assembly when mock SFL registry is online."""
    functions = {
        "SFL-FN-901": MockSflFunctionDefinition("SFL-FN-901", "SFL-FAM-901", "Mock Fun 1", ["positive"]),
        "SFL-FN-902": MockSflFunctionDefinition("SFL-FN-902", "SFL-FAM-902", "Mock Fun 2", ["positive"]),
    }
    crosswalks = {
        "REC-1": MockSflCrosswalkRecord("REC-1", "arc-myth-debunk", ["SFL-FN-901", "SFL-FN-902"])
    }
    mock_registry = MockSflRegistry(ready=True, crosswalks=crosswalks, functions=functions)
    
    # We pass the mock_registry to the runtime constructor
    service = ArchetypeContainerRuntimeService(sfl_registry=mock_registry)
    result = _run(service.compile(
        capture=_build_capture(),
        coalition=_build_coalition(),
        mood_context={"mood_id": "MOOD-001", "primary_vector": "aggressive_certainty", "intensity": 0.85}
    ))
    
    assert result.status == RuntimeStatus.COMPILED
    assert result.sfl_binding_status == SflBindingStatus.SFL_BOUND
    assert result.container_manifest is not None
    assert result.container_manifest.sfl_function_stack is not None
    assert len(result.container_manifest.sfl_function_stack.active_functions) == 2
    assert result.container_manifest.sfl_function_stack.active_functions[0].function_id == "SFL-FN-901"
    
    # Check that execution contract is assembled
    contract = result.container_manifest.execution_contract
    assert contract is not None
    assert contract.runtime_session_id == result.runtime_session_id
    assert contract.skill_execution_mode == "typed_dspy_module"
    assert "input_transcript" in contract.dspy_signature_fields
    assert "output_rendered_blueprint" in contract.dspy_signature_fields


def test_sfl_bound_successfully_with_manual_packets():
    """Test SFL bound status when inputs are passed manually to compile()."""
    service = ArchetypeContainerRuntimeService()
    
    manual_stack = SubliminalFunctionStackPacket(
        stack_id="STK-MANUAL",
        archetype_choice=ArchetypeChoice.ARC_MYTH_DEBUNK,
        active_functions=[
            SflFunctionBinding(
                function_id="SFL-FN-001",
                family_id="SFL-FAM-001",
                canonical_name="Contrast Framing",
                polarity="positive",
                weight=0.45,
                binding_rationale="Manual bind"
            )
        ],
        crosswalk_source_id="XW-MANUAL",
        total_weight=0.45,
        binding_surface="short_form_video",
    )
    manual_depth = CompositionDepthPacket(
        depth_id="DEP-MANUAL",
        depth_class=CompositionDepthClass.LAYERED_INTERPRETATION,
        intensity=0.8,
        governing_rationale="Manual depth"
    )
    manual_variation = VariationProfileBinding(
        variation_id="VAR-MANUAL",
        asymmetry_target=0.7,
        resonance_spacing=0.5,
        predictability_break_threshold=0.6,
        variation_rationale="Manual variation"
    )
    
    result = _run(service.compile(
        capture=_build_capture(),
        coalition=_build_coalition(),
        sfl_function_stack=manual_stack,
        composition_depth=manual_depth,
        variation_profile=manual_variation
    ))
    
    assert result.status == RuntimeStatus.COMPILED
    assert result.sfl_binding_status == SflBindingStatus.SFL_BOUND
    assert result.container_manifest.sfl_function_stack.stack_id == "STK-MANUAL"
    assert result.container_manifest.composition_depth.depth_id == "DEP-MANUAL"
    assert result.container_manifest.variation_binding.variation_id == "VAR-MANUAL"


def test_sfl_partial_binding_status():
    """Test partial binding when only some manual inputs are passed and registry is offline/none."""
    service = ArchetypeContainerRuntimeService()
    
    manual_stack = SubliminalFunctionStackPacket(
        stack_id="STK-MANUAL",
        archetype_choice=ArchetypeChoice.ARC_MYTH_DEBUNK,
        active_functions=[
            SflFunctionBinding(
                function_id="SFL-FN-001",
                family_id="SFL-FAM-001",
                canonical_name="Contrast Framing",
                polarity="positive",
                weight=0.45,
                binding_rationale="Manual bind"
            )
        ],
        crosswalk_source_id="XW-MANUAL",
        total_weight=0.45,
        binding_surface="short_form_video",
    )
    
    result = _run(service.compile(
        capture=_build_capture(),
        coalition=_build_coalition(),
        sfl_function_stack=manual_stack
    ))
    
    assert result.status == RuntimeStatus.COMPILED
    assert result.sfl_binding_status == SflBindingStatus.SFL_PARTIAL


def test_sfl_unavailable_binding_status_when_registry_offline():
    """Test SFL_UNAVAILABLE when registry is passed but is not healthy/ready."""
    mock_registry = MockSflRegistry(ready=False)
    service = ArchetypeContainerRuntimeService(sfl_registry=mock_registry)
    
    result = _run(service.compile(
        capture=_build_capture(),
        coalition=_build_coalition(),
    ))
    
    assert result.status == RuntimeStatus.COMPILED
    assert result.sfl_binding_status == SflBindingStatus.SFL_UNAVAILABLE
    # Manifest fields should still fall back or be None, let's verify no crash
    assert result.container_manifest is not None


def test_sfl_not_bound_status():
    """Test SFL_NOT_BOUND status when no registry is passed and no SFL inputs are provided."""
    service = ArchetypeContainerRuntimeService()
    
    result = _run(service.compile(
        capture=_build_capture(),
        coalition=_build_coalition(),
    ))
    
    assert result.status == RuntimeStatus.COMPILED
    assert result.sfl_binding_status == SflBindingStatus.SFL_NOT_BOUND


def test_invalid_depth_class_validation():
    """Test validation fails if composition_depth has an invalid depth_class value."""
    service = ArchetypeContainerRuntimeService()
    
    # We construct a packet with an invalid string value for depth_class
    invalid_depth = CompositionDepthPacket.model_construct(
        depth_id="DEP-INVALID",
        depth_class="SUPER_DEEP_NONEXISTENT",
    )
    
    with pytest.raises(ValueError, match="Invalid depth_class"):
        _run(service.compile(
            capture=_build_capture(),
            coalition=_build_coalition(),
            composition_depth=invalid_depth
        ))
