"""
FR-VIS-14 — ConsciousSmile Expression Adapter
Build Step 28 · DEP-VIS-008, DEP-VIS-013

28-channel FACS-based expression system with continuous 0.0–1.0 per channel.
Named emotion presets, LoRA weight budget enforcement, confusion pair management.

§10 Testing: Channel parsing, preset resolution, weight budget, legacy fallback.
"""

from __future__ import annotations

import re
from typing import Any

from core.commercial_models import build_receipt, compute_receipt_hash
from core.visual_models import (
    CONSCIOUS_SMILE_DEFAULT_WEIGHT,
    EXPRESSION_CHANNEL_COUNT,
    IDENTITY_LORA_DEFAULT_WEIGHT,
    LORA_WEIGHT_BUDGET_MAX,
    RECEIPT_STAGE_EXPRESSION_PARSE,
    RECEIPT_STAGE_PRESET_RESOLVE,
    ChannelStatus,
    ExpressionChannel,
    ExpressionPreset,
    ExpressionSpec,
    TrainingPhase,
    TrainingRunRow,
    VisualPipelineError,
    WeightBudgetResult,
)


# =====================================================
#  28-Channel Registry (from §4 Stage 1 + MCDA audit)
# =====================================================

# Phase 1: Core (5 channels)
CORE_CHANNELS = [
    ExpressionChannel(channel_id="CH01", channel_name="smile_duchenne", facs_action_units="AU6 + AU12",
                      arkit_blendshapes=["mouthSmileL", "mouthSmileR", "cheekSquintL", "cheekSquintR"],
                      somatic_target="Zygomaticus + Orbicularis → viewer warmth/trust",
                      mood_state_affinity={"Escape": 0.8, "Discovery": 0.5},
                      training_phase=1, confusion_pairs=["CH14_dimpler"]),
    ExpressionChannel(channel_id="CH02", channel_name="gaze_vertical", facs_action_units="AU61/AU62",
                      arkit_blendshapes=["eyeLookUpL", "eyeLookUpR", "eyeLookDownL", "eyeLookDownR"],
                      somatic_target="Superior rectus → viewer curiosity/submission",
                      mood_state_affinity={"Processing": 0.7, "Discovery": 0.6},
                      training_phase=1, confusion_pairs=["CH04_brow_raise"]),
    ExpressionChannel(channel_id="CH03", channel_name="brow_raise", facs_action_units="AU1 + AU2",
                      arkit_blendshapes=["browInnerUp", "browOuterUpL", "browOuterUpR"],
                      somatic_target="Frontalis → viewer surprise/openness",
                      mood_state_affinity={"Discovery": 0.8, "Processing": 0.3},
                      training_phase=1, confusion_pairs=["CH09_eye_wide"]),
    ExpressionChannel(channel_id="CH04", channel_name="brow_furrow", facs_action_units="AU4",
                      arkit_blendshapes=["browDownL", "browDownR"],
                      somatic_target="Corrugator → viewer concern/empathy",
                      mood_state_affinity={"Processing": 0.9, "Status": 0.2},
                      training_phase=1, confusion_pairs=["CH05_eye_squint"]),
    ExpressionChannel(channel_id="CH05", channel_name="eye_squint", facs_action_units="AU7",
                      arkit_blendshapes=["eyeSquintL", "eyeSquintR"],
                      somatic_target="Orbicularis oculi → viewer trust activation",
                      mood_state_affinity={"Escape": 0.6, "Processing": 0.4},
                      training_phase=1, confusion_pairs=["CH01_smile_duchenne"]),
]

# Phase 2: Extended (11 channels)
EXTENDED_CHANNELS = [
    ExpressionChannel(channel_id="CH06", channel_name="gaze_horizontal", facs_action_units="AU63/AU64",
                      arkit_blendshapes=["eyeLookInL", "eyeLookInR", "eyeLookOutL", "eyeLookOutR"],
                      somatic_target="Lateral rectus → viewer attention direction",
                      training_phase=2),
    ExpressionChannel(channel_id="CH07", channel_name="lip_press", facs_action_units="AU24",
                      arkit_blendshapes=["mouthPressL", "mouthPressR"],
                      somatic_target="Orbicularis oris → viewer determination",
                      training_phase=2, confusion_pairs=["CH19_chin_raise"]),
    ExpressionChannel(channel_id="CH08", channel_name="mouth_frown", facs_action_units="AU15",
                      arkit_blendshapes=["mouthFrownL", "mouthFrownR"],
                      somatic_target="Depressor anguli oris → viewer sadness/concern",
                      training_phase=2),
    ExpressionChannel(channel_id="CH09", channel_name="eye_wide", facs_action_units="AU5",
                      arkit_blendshapes=["eyeWideL", "eyeWideR"],
                      somatic_target="Levator palpebrae → viewer surprise/alarm",
                      training_phase=2),
    ExpressionChannel(channel_id="CH10", channel_name="jaw_open", facs_action_units="AU26",
                      arkit_blendshapes=["jawOpen"],
                      somatic_target="Masseter release → viewer shock/awe",
                      training_phase=2),
    ExpressionChannel(channel_id="CH11", channel_name="chin_raise", facs_action_units="AU17",
                      arkit_blendshapes=["chinRaiser"],
                      somatic_target="Mentalis → viewer defiance/resolve",
                      training_phase=2),
    ExpressionChannel(channel_id="CH12", channel_name="smirk", facs_action_units="AU12L",
                      arkit_blendshapes=["mouthSmileL"],
                      somatic_target="Unilateral zygomaticus → viewer irony/knowing",
                      training_phase=2),
    ExpressionChannel(channel_id="CH13", channel_name="lip_bite", facs_action_units="AU25 + AU28",
                      arkit_blendshapes=["mouthRollLower"],
                      somatic_target="Orbicularis + incisors → viewer vulnerability",
                      training_phase=2),
    ExpressionChannel(channel_id="CH14", channel_name="wink_left", facs_action_units="AU46L",
                      arkit_blendshapes=["eyeBlinkL"],
                      somatic_target="Orbicularis oculi unilateral → viewer complicity",
                      training_phase=2),
    ExpressionChannel(channel_id="CH15", channel_name="wink_right", facs_action_units="AU46R",
                      arkit_blendshapes=["eyeBlinkR"],
                      somatic_target="Orbicularis oculi unilateral → viewer complicity",
                      training_phase=2),
    ExpressionChannel(channel_id="CH16", channel_name="nostril_flare", facs_action_units="AU38",
                      arkit_blendshapes=["noseSneerL", "noseSneerR"],
                      somatic_target="Nasalis → viewer intensity/effort",
                      training_phase=2),
]

# Phase 3: Refinement (12 channels)
REFINEMENT_CHANNELS = [
    ExpressionChannel(channel_id="CH17", channel_name="dimpler", facs_action_units="AU14",
                      arkit_blendshapes=["mouthDimpleL", "mouthDimpleR"],
                      somatic_target="Buccinator → viewer charm/appeal",
                      training_phase=3, confusion_pairs=["CH01_smile_duchenne"]),
    ExpressionChannel(channel_id="CH18", channel_name="head_tilt", facs_action_units="AU55/AU56",
                      arkit_blendshapes=["headRoll"],
                      somatic_target="SCM muscle → viewer engagement/curiosity",
                      training_phase=3),
    ExpressionChannel(channel_id="CH19", channel_name="lip_pucker", facs_action_units="AU18",
                      arkit_blendshapes=["mouthPucker"],
                      somatic_target="Orbicularis oris → viewer thoughtfulness",
                      training_phase=3, confusion_pairs=["CH24_nose_wrinkle"]),
    ExpressionChannel(channel_id="CH20", channel_name="nose_wrinkle", facs_action_units="AU9",
                      arkit_blendshapes=["noseSneerL", "noseSneerR"],
                      somatic_target="Levator labii → viewer disgust/playful rejection",
                      training_phase=3),
    ExpressionChannel(channel_id="CH21", channel_name="eye_moisture", facs_action_units="AU-custom",
                      arkit_blendshapes=["eyeSquintL", "eyeSquintR"],
                      somatic_target="Lacrimal response → viewer empathy/connection",
                      training_phase=3),
    ExpressionChannel(channel_id="CH22", channel_name="pout", facs_action_units="AU22 + AU25",
                      arkit_blendshapes=["mouthFunnel", "mouthPucker"],
                      somatic_target="Orbicularis + mentalis → viewer playfulness",
                      training_phase=3),
    ExpressionChannel(channel_id="CH23", channel_name="teeth_clench", facs_action_units="AU-custom",
                      arkit_blendshapes=["jawForward", "mouthClose"],
                      somatic_target="Masseter contraction → viewer tension/effort",
                      training_phase=3),
    ExpressionChannel(channel_id="CH24", channel_name="tongue_peek", facs_action_units="AU19",
                      arkit_blendshapes=["tongueOut"],
                      somatic_target="Genioglossus → viewer playful rebellion",
                      training_phase=3),
    ExpressionChannel(channel_id="CH25", channel_name="lip_purse", facs_action_units="AU28",
                      arkit_blendshapes=["mouthShrugUpper", "mouthShrugLower"],
                      somatic_target="Orbicularis tight → viewer withholding/control",
                      training_phase=3),
    ExpressionChannel(channel_id="CH26", channel_name="cheek_dimple", facs_action_units="AU14 deep",
                      arkit_blendshapes=["mouthDimpleL", "mouthDimpleR"],
                      somatic_target="Deep buccinator → viewer warmth/charm",
                      training_phase=3),
    ExpressionChannel(channel_id="CH27", channel_name="crow_feet_activation", facs_action_units="AU-custom",
                      arkit_blendshapes=["eyeSquintL", "eyeSquintR"],
                      somatic_target="Periorbital wrinkle → Duchenne authenticity signal",
                      training_phase=3),
    ExpressionChannel(channel_id="CH28", channel_name="micro_contempt", facs_action_units="AU14L",
                      arkit_blendshapes=["mouthDimpleL"],
                      somatic_target="Unilateral buccinator → viewer detection of insincerity",
                      training_phase=3),
]

ALL_CHANNELS = CORE_CHANNELS + EXTENDED_CHANNELS + REFINEMENT_CHANNELS


# =====================================================
#  Default Presets (from §4 Stage 6)
# =====================================================

DEFAULT_PRESETS = [
    ExpressionPreset(
        preset_name="warm_confidence",
        display_name="Warm Confidence",
        channel_values={"smile_duchenne": 0.6, "eye_squint": 0.4, "brow_raise": 0.1},
        mood_state_affinity="Escape",
        prompt_string="expression: smile_duchenne 0.6, eye_squint 0.4, brow_raise 0.1",
    ),
    ExpressionPreset(
        preset_name="empathic_concern",
        display_name="Empathic Concern",
        channel_values={"brow_furrow": 0.5, "eye_squint": 0.3, "smile_duchenne": 0.2, "head_tilt": 0.3},
        mood_state_affinity="Processing",
        prompt_string="expression: brow_furrow 0.5, eye_squint 0.3, smile_duchenne 0.2, head_tilt 0.3",
    ),
    ExpressionPreset(
        preset_name="determined_resolve",
        display_name="Determined Resolve",
        channel_values={"brow_furrow": 0.6, "lip_press": 0.4, "eye_squint": 0.2, "chin_raise": 0.3},
        mood_state_affinity="Status",
        prompt_string="expression: brow_furrow 0.6, lip_press 0.4, eye_squint 0.2, chin_raise 0.3",
    ),
    ExpressionPreset(
        preset_name="playful_mischief",
        display_name="Playful Mischief",
        channel_values={"smirk": 0.7, "brow_raise": 0.4, "eye_squint": 0.2, "wink_left": 0.3},
        mood_state_affinity="Escape",
        prompt_string="expression: smirk 0.7, brow_raise 0.4, eye_squint 0.2, wink_left 0.3",
    ),
    ExpressionPreset(
        preset_name="genuine_surprise",
        display_name="Genuine Surprise",
        channel_values={"brow_raise": 0.8, "eye_wide": 0.7, "jaw_open": 0.3},
        mood_state_affinity="Discovery",
        prompt_string="expression: brow_raise 0.8, eye_wide 0.7, jaw_open 0.3",
    ),
    ExpressionPreset(
        preset_name="thoughtful_processing",
        display_name="Thoughtful Processing",
        channel_values={"gaze_vertical": 0.4, "lip_purse": 0.3, "brow_furrow": 0.2},
        mood_state_affinity="Processing",
        prompt_string="expression: gaze_vertical 0.4, lip_purse 0.3, brow_furrow 0.2",
    ),
    ExpressionPreset(
        preset_name="vulnerable_openness",
        display_name="Vulnerable Openness",
        channel_values={"eye_moisture": 0.3, "brow_raise": 0.2, "smile_duchenne": 0.15, "lip_bite": 0.2},
        mood_state_affinity="Processing",
        prompt_string="expression: eye_moisture 0.3, brow_raise 0.2, smile_duchenne 0.15, lip_bite 0.2",
    ),
    ExpressionPreset(
        preset_name="neutral",
        display_name="Neutral",
        channel_values={},
        mood_state_affinity=None,
        prompt_string="expression: neutral",
    ),
]


# =====================================================
#  Expression Prompt Parser (§10 Unit Tests)
# =====================================================

class ExpressionPromptParser:
    """
    §10 Unit Test: Channel Prompt Parsing.
    Parses 'expression: smile 0.6, brow_furrow 0.3' into channel dict.
    """

    def __init__(self, channels: list[ExpressionChannel] | None = None):
        self._channels = {ch.channel_name: ch for ch in (channels or ALL_CHANNELS)}

    def parse(self, prompt_string: str) -> dict[str, float]:
        """
        Parse expression prompt string into channel:value dict.
        Format: 'expression: channel_name value, channel_name value, ...'
        Unmentioned channels default to 0.0.
        """
        result: dict[str, float] = {}

        # Remove 'expression:' prefix
        text = prompt_string.strip()
        if text.lower().startswith("expression:"):
            text = text[len("expression:"):].strip()

        if not text or text.lower() == "neutral":
            return result

        # Parse channel:value pairs
        # Supports: "smile 0.6, brow_furrow 0.3" and "smile_duchenne 0.6, eye_squint 0.4"
        pairs = [p.strip() for p in text.split(",") if p.strip()]
        for pair in pairs:
            parts = pair.strip().split()
            if len(parts) == 2:
                channel_name = parts[0].strip()
                try:
                    value = float(parts[1].strip())
                except ValueError:
                    continue

                # Clamp to [0.0, 1.0] — §10 Safety: expression injection protection
                value = max(0.0, min(1.0, value))

                # Validate channel exists
                if channel_name in self._channels:
                    result[channel_name] = value
                else:
                    # Try partial match (e.g., 'smile' → 'smile_duchenne')
                    for ch_name in self._channels:
                        if ch_name.startswith(channel_name):
                            result[ch_name] = value
                            break

        return result

    def get_unset_channels(self, active: dict[str, float]) -> list[str]:
        """Return channels not set in the active dict (default 0.0)."""
        return [name for name in self._channels if name not in active]


# =====================================================
#  Preset Resolver (§10 Unit Tests)
# =====================================================

class PresetResolver:
    """
    §10 Unit Test: Preset Resolution.
    Resolves named presets to multi-channel vectors.
    """

    def __init__(self, presets: list[ExpressionPreset] | None = None):
        self._presets = {p.preset_name: p for p in (presets or DEFAULT_PRESETS)}

    def resolve(self, preset_name: str) -> ExpressionPreset | None:
        return self._presets.get(preset_name)

    def resolve_with_overrides(
        self, preset_name: str, overrides: dict[str, float] | None = None,
    ) -> dict[str, float]:
        """Resolve preset + apply per-channel overrides."""
        preset = self._presets.get(preset_name)
        if preset is None:
            raise VisualPipelineError(
                code="PRESET_NOT_FOUND",
                message=f"Expression preset '{preset_name}' not found.",
            )
        values = dict(preset.channel_values)
        if overrides:
            for ch, val in overrides.items():
                values[ch] = max(0.0, min(1.0, val))
        return values

    def get_presets_by_mood(self, mood_state: str) -> list[ExpressionPreset]:
        """Return presets with matching mood state affinity."""
        return [p for p in self._presets.values() if p.mood_state_affinity == mood_state]

    def list_presets(self) -> list[str]:
        return list(self._presets.keys())


# =====================================================
#  LoRA Weight Budget Validator (§10 Unit Tests)
# =====================================================

class WeightBudgetValidator:
    """
    §10 Unit Test: Weight Budget Validation.
    Identity LoRA + ConsciousSmile ≤ 1.50.
    """

    def __init__(self, max_budget: float = LORA_WEIGHT_BUDGET_MAX):
        self._max_budget = max_budget

    def validate(
        self,
        identity_weight: float = IDENTITY_LORA_DEFAULT_WEIGHT,
        adapter_weight: float = CONSCIOUS_SMILE_DEFAULT_WEIGHT,
    ) -> WeightBudgetResult:
        total = identity_weight + adapter_weight
        within_budget = total <= self._max_budget
        warning = None
        if not within_budget:
            warning = (
                f"LoRA weight budget exceeded: {total:.2f} > {self._max_budget:.2f}. "
                f"Risk of burn/artifact/deep-fry on output images."
            )
        return WeightBudgetResult(
            total_weight=round(total, 2),
            identity_weight=identity_weight,
            adapter_weight=adapter_weight,
            within_budget=within_budget,
            warning=warning,
        )


# =====================================================
#  Expression Spec Builder (VCB integration)
# =====================================================

class ExpressionSpecBuilder:
    """
    Builds the expression_spec for VCB embedding.
    Integrates parser + preset resolver + weight budget.
    """

    def __init__(self):
        self._parser = ExpressionPromptParser()
        self._resolver = PresetResolver()
        self._budget = WeightBudgetValidator()
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def build_from_preset(
        self,
        preset_name: str,
        overrides: dict[str, float] | None = None,
        identity_weight: float = IDENTITY_LORA_DEFAULT_WEIGHT,
        adapter_weight: float = CONSCIOUS_SMILE_DEFAULT_WEIGHT,
    ) -> ExpressionSpec:
        """Build expression spec from a named preset with optional overrides."""
        channel_values = self._resolver.resolve_with_overrides(preset_name, overrides)

        budget = self._budget.validate(identity_weight, adapter_weight)
        if not budget.within_budget:
            raise VisualPipelineError(
                code="WEIGHT_BUDGET_EXCEEDED",
                message=budget.warning or "Weight budget exceeded.",
            )

        spec = ExpressionSpec(
            mode="preset",
            preset_name=preset_name,
            channel_overrides=overrides or {},
            adapter_weight=adapter_weight,
        )

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_PRESET_RESOLVE,
            agent_name="expression_spec_builder",
            input_payload={"preset_name": preset_name, "overrides": overrides},
            output_payload={"channel_values": channel_values, "budget": budget.model_dump()},
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return spec

    def build_from_prompt(
        self,
        prompt_string: str,
        identity_weight: float = IDENTITY_LORA_DEFAULT_WEIGHT,
        adapter_weight: float = CONSCIOUS_SMILE_DEFAULT_WEIGHT,
    ) -> ExpressionSpec:
        """Build expression spec from a raw prompt string."""
        channel_values = self._parser.parse(prompt_string)

        budget = self._budget.validate(identity_weight, adapter_weight)
        if not budget.within_budget:
            raise VisualPipelineError(
                code="WEIGHT_BUDGET_EXCEEDED",
                message=budget.warning or "Weight budget exceeded.",
            )

        spec = ExpressionSpec(
            mode="manual",
            channel_overrides=channel_values,
            adapter_weight=adapter_weight,
        )

        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_EXPRESSION_PARSE,
            agent_name="expression_spec_builder",
            input_payload={"prompt_string": prompt_string},
            output_payload={"channel_values": channel_values},
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return spec

    def check_legacy_fallback(self, vcb: dict[str, Any]) -> bool:
        """
        §6 Backward Compatibility: If VCB has no expression_spec,
        return True → Paradoxe falls back to prompt-only.
        """
        return "expression_spec" not in vcb or vcb.get("expression_spec") is None

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)
