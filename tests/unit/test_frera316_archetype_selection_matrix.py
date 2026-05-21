"""Unit tests for ArchetypeSelectionMatrix — FR-ERA3-16."""
from src.ccp.models.archetype_container_runtime_models import ArchetypeChoice, CoalitionInputs
from src.ccp.services.archetype_container_runtime import ArchetypeSelectionMatrix


def _coalition(stance: str, source_count: int = 1) -> CoalitionInputs:
    return CoalitionInputs(
        coalition_id="COL-TEST",
        family_mix=["STR", "PRS"],
        stance_polarity=stance,
        source_count=source_count,
        evidence_strength=0.8,
        intended_business_job="authority_content",
    )


class TestHighContrastSelectsMythDebunk:
    """test_high_contrast_single_take_selects_arc_myth_debunk"""

    def test_high_contrast_maps_to_myth_debunk(self):
        matrix = ArchetypeSelectionMatrix()
        result = matrix.select(_coalition("high_contrast"))
        assert result == ArchetypeChoice.ARC_MYTH_DEBUNK

    def test_aggressive_certainty_maps_to_myth_debunk(self):
        matrix = ArchetypeSelectionMatrix()
        result = matrix.select(_coalition("aggressive_certainty"))
        assert result == ArchetypeChoice.ARC_MYTH_DEBUNK


class TestMultiSourceCanSelectArcComp:
    """test_multi_source_three_or_more_sources_can_select_arc_comp"""

    def test_three_sources_with_compilation_stance(self):
        matrix = ArchetypeSelectionMatrix()
        result = matrix.select(_coalition("compilation", source_count=3))
        assert result == ArchetypeChoice.ARC_COMP

    def test_four_sources_with_synthesis_stance(self):
        matrix = ArchetypeSelectionMatrix()
        result = matrix.select(_coalition("synthesis", source_count=4))
        assert result == ArchetypeChoice.ARC_COMP


class TestArcCompRejectedBelowThree:
    """test_arc_comp_rejected_when_source_count_below_three (AC5)"""

    def test_single_source_cannot_be_comp(self):
        matrix = ArchetypeSelectionMatrix()
        result = matrix.select(_coalition("compilation", source_count=1))
        assert result != ArchetypeChoice.ARC_COMP

    def test_two_sources_cannot_be_comp(self):
        matrix = ArchetypeSelectionMatrix()
        result = matrix.select(_coalition("synthesis", source_count=2))
        assert result != ArchetypeChoice.ARC_COMP
