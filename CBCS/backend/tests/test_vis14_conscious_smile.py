"""
FR-VIS-14 — ConsciousSmile Expression Adapter Tests (Step 28)

Coverage:
- AC1: Channel activation precision (prompt parsing accuracy)
- AC2: Channel isolation (unmentioned channels default 0.0)
- AC5: LoRA weight budget enforcement
- AC6: Monotonic intensity (parsing preserves ordering)
- AC7: Named preset resolution
- Safety: Expression injection clamping (9999.0 → 1.0)
- Legacy: VCB backward compatibility fallback
"""

import pytest

from core.conscious_smile_adapter import (
    ALL_CHANNELS,
    DEFAULT_PRESETS,
    ExpressionPromptParser,
    ExpressionSpecBuilder,
    PresetResolver,
    WeightBudgetValidator,
)
from core.visual_models import VisualPipelineError


class TestChannelRegistry:

    def test_28_channels_registered(self):
        assert len(ALL_CHANNELS) == 28

    def test_channel_ids_unique(self):
        ids = [ch.channel_id for ch in ALL_CHANNELS]
        assert len(ids) == len(set(ids))

    def test_channel_names_unique(self):
        names = [ch.channel_name for ch in ALL_CHANNELS]
        assert len(names) == len(set(names))

    def test_core_channels_phase_1(self):
        core = [ch for ch in ALL_CHANNELS if ch.training_phase == 1]
        assert len(core) == 5

    def test_extended_channels_phase_2(self):
        extended = [ch for ch in ALL_CHANNELS if ch.training_phase == 2]
        assert len(extended) == 11

    def test_refinement_channels_phase_3(self):
        refinement = [ch for ch in ALL_CHANNELS if ch.training_phase == 3]
        assert len(refinement) == 12

    def test_confusion_pairs_defined(self):
        pairs = [ch for ch in ALL_CHANNELS if ch.confusion_pairs]
        assert len(pairs) >= 5  # At least 5 channels have confusion pairs


class TestExpressionPromptParser:

    def test_parse_three_channels(self):
        parser = ExpressionPromptParser()
        result = parser.parse("expression: smile_duchenne 0.6, brow_furrow 0.3, eye_squint 0.2")

        assert result["smile_duchenne"] == 0.6
        assert result["brow_furrow"] == 0.3
        assert result["eye_squint"] == 0.2

    def test_unmentioned_channels_default_zero(self):
        parser = ExpressionPromptParser()
        result = parser.parse("expression: smile_duchenne 0.6")

        assert result.get("smile_duchenne") == 0.6
        unset = parser.get_unset_channels(result)
        assert "brow_furrow" in unset
        assert "eye_squint" in unset

    def test_neutral_returns_empty(self):
        parser = ExpressionPromptParser()
        result = parser.parse("expression: neutral")
        assert result == {}

    def test_empty_string_returns_empty(self):
        parser = ExpressionPromptParser()
        result = parser.parse("")
        assert result == {}

    def test_clamp_to_max_1(self):
        """Safety: expression injection — 9999 clamped to 1.0."""
        parser = ExpressionPromptParser()
        result = parser.parse("expression: smile_duchenne 9999.0")
        assert result["smile_duchenne"] == 1.0

    def test_clamp_to_min_0(self):
        parser = ExpressionPromptParser()
        result = parser.parse("expression: smile_duchenne -5.0")
        assert result["smile_duchenne"] == 0.0

    def test_partial_channel_name_match(self):
        """'smile' should match 'smile_duchenne'."""
        parser = ExpressionPromptParser()
        result = parser.parse("expression: smile 0.7")
        assert "smile_duchenne" in result
        assert result["smile_duchenne"] == 0.7

    def test_invalid_channel_ignored(self):
        parser = ExpressionPromptParser()
        result = parser.parse("expression: nonexistent_channel 0.5, smile_duchenne 0.3")
        assert "smile_duchenne" in result
        assert "nonexistent_channel" not in result

    def test_monotonic_values_preserved(self):
        """AC6: Intensity values are preserved in order."""
        parser = ExpressionPromptParser()
        r1 = parser.parse("expression: smile_duchenne 0.2")
        r2 = parser.parse("expression: smile_duchenne 0.4")
        r3 = parser.parse("expression: smile_duchenne 0.6")
        r4 = parser.parse("expression: smile_duchenne 0.8")

        assert r1["smile_duchenne"] < r2["smile_duchenne"]
        assert r2["smile_duchenne"] < r3["smile_duchenne"]
        assert r3["smile_duchenne"] < r4["smile_duchenne"]


class TestPresetResolver:

    def test_warm_confidence_resolves(self):
        resolver = PresetResolver()
        preset = resolver.resolve("warm_confidence")

        assert preset is not None
        assert preset.channel_values["smile_duchenne"] == 0.6
        assert preset.channel_values["eye_squint"] == 0.4

    def test_empathic_concern_resolves(self):
        resolver = PresetResolver()
        preset = resolver.resolve("empathic_concern")

        assert preset is not None
        assert "brow_furrow" in preset.channel_values
        assert "head_tilt" in preset.channel_values

    def test_nonexistent_preset_returns_none(self):
        resolver = PresetResolver()
        assert resolver.resolve("nonexistent") is None

    def test_resolve_with_overrides(self):
        resolver = PresetResolver()
        values = resolver.resolve_with_overrides("warm_confidence", {"smile_duchenne": 0.9})

        assert values["smile_duchenne"] == 0.9  # Override applied
        assert values["eye_squint"] == 0.4  # Original preserved

    def test_resolve_nonexistent_raises(self):
        resolver = PresetResolver()
        with pytest.raises(VisualPipelineError) as exc:
            resolver.resolve_with_overrides("fake_preset")
        assert exc.value.code == "PRESET_NOT_FOUND"

    def test_mood_state_query(self):
        resolver = PresetResolver()
        processing = resolver.get_presets_by_mood("Processing")
        assert len(processing) >= 2  # empathic_concern + thoughtful_processing

    def test_all_presets_listed(self):
        resolver = PresetResolver()
        assert len(resolver.list_presets()) == 8

    def test_neutral_preset_empty_channels(self):
        resolver = PresetResolver()
        preset = resolver.resolve("neutral")
        assert preset is not None
        assert preset.channel_values == {}


class TestWeightBudgetValidator:

    def test_default_weights_pass(self):
        validator = WeightBudgetValidator()
        result = validator.validate(0.65, 0.80)

        assert result.within_budget is True
        assert result.total_weight == 1.45
        assert result.warning is None

    def test_overweight_fails(self):
        validator = WeightBudgetValidator()
        result = validator.validate(0.90, 0.80)

        assert result.within_budget is False
        assert result.total_weight == 1.70
        assert result.warning is not None
        assert "exceeded" in result.warning.lower()

    def test_exact_budget_passes(self):
        validator = WeightBudgetValidator()
        result = validator.validate(0.70, 0.80)

        assert result.within_budget is True
        assert result.total_weight == 1.50


class TestExpressionSpecBuilder:

    def test_build_from_preset(self):
        builder = ExpressionSpecBuilder()
        spec = builder.build_from_preset("warm_confidence")

        assert spec.mode == "preset"
        assert spec.preset_name == "warm_confidence"
        assert spec.adapter_weight == 0.80

    def test_build_from_prompt(self):
        builder = ExpressionSpecBuilder()
        spec = builder.build_from_prompt("expression: smile_duchenne 0.7, brow_furrow 0.3")

        assert spec.mode == "manual"
        assert spec.channel_overrides["smile_duchenne"] == 0.7

    def test_overweight_spec_raises(self):
        builder = ExpressionSpecBuilder()
        with pytest.raises(VisualPipelineError) as exc:
            builder.build_from_preset("warm_confidence", identity_weight=0.90, adapter_weight=0.80)
        assert exc.value.code == "WEIGHT_BUDGET_EXCEEDED"

    def test_receipt_chain_written(self):
        builder = ExpressionSpecBuilder()
        builder.build_from_preset("warm_confidence")

        receipts = builder.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "PRESET_RESOLVE"

    def test_legacy_fallback_no_expression_spec(self):
        builder = ExpressionSpecBuilder()
        vcb = {"concept": "test", "mood_state": "Escape"}
        assert builder.check_legacy_fallback(vcb) is True

    def test_legacy_fallback_with_expression_spec(self):
        builder = ExpressionSpecBuilder()
        vcb = {"expression_spec": {"mode": "preset", "preset_name": "warm_confidence"}}
        assert builder.check_legacy_fallback(vcb) is False
