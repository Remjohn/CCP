"""
FR-VIS-16 — First Frame Composer (Iris)
Build Step 31 · DEP-VIS-012

6-step deterministic decision engine (no LLM), 8-format routing table,
2-level anti-draft constraint system, CLIP deduplication.

§10 Testing: Determinism, format dimensions, anti-draft rule matching,
text injection safety, non-existent CP-ID fallback.
"""

from __future__ import annotations

import hashlib
import html
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from core.commercial_models import build_receipt, compute_receipt_hash
from core.visual_models import (
    ANTI_DRAFT_KELVIN_THRESHOLD,
    ANTI_DRAFT_SATURATION_THRESHOLD,
    CLIP_DEDUP_THRESHOLD,
    CONSCIOUS_SMILE_DEFAULT_WEIGHT,
    CONTROLNET_DEFAULT_STRENGTH,
    IDENTITY_LORA_DEFAULT_WEIGHT,
    RECEIPT_STAGE_ANTI_DRAFT_CHECK,
    RECEIPT_STAGE_FFC_COMPOSE,
    AntiDraftLevel,
    AntiDraftResult,
    CBCSTier,
    FirstFrameSpec,
    FormatConstraints,
    OutputFormat,
    VisualPipelineError,
)


# =====================================================
#  Format Routing Table (§4 Stage 2)
# =====================================================

FORMAT_CONSTRAINTS: dict[OutputFormat, FormatConstraints] = {
    OutputFormat.SHORT_VIDEO: FormatConstraints(
        dimensions="1080x1920", face_position_rule="top_40_pct",
        text_zone="bottom_30_pct", face_required=True,
    ),
    OutputFormat.CAROUSEL: FormatConstraints(
        dimensions="1080x1350", face_position_rule="centered",
        text_zone="bottom_30_pct", face_required=True,
    ),
    OutputFormat.THUMBNAIL: FormatConstraints(
        dimensions="1920x1080", face_position_rule="rule_of_thirds",
        text_zone="opposite_third", face_required=True,
    ),
    OutputFormat.FLYER: FormatConstraints(
        dimensions="1080x1920", face_position_rule="flexible",
        text_zone="bottom_40_pct", face_required=False,
    ),
    OutputFormat.WEBINAR: FormatConstraints(
        dimensions="1920x1080", face_position_rule="professional_framing",
        text_zone="bottom_20_pct", face_required=True,
    ),
    OutputFormat.STORY: FormatConstraints(
        dimensions="1080x1920", face_position_rule="top_center",
        text_zone="bottom_30_pct", face_required=True,
    ),
    OutputFormat.POLL: FormatConstraints(
        dimensions="1080x1080", face_position_rule="split_screen",
        text_zone="right_half", face_required=False,
    ),
    OutputFormat.EMAIL: FormatConstraints(
        dimensions="600x400", face_position_rule="centered",
        text_zone="below_face", face_required=True,
    ),
}


# =====================================================
#  Gaze Routing Table (§4 Stage 1, Step 3)
# =====================================================

GAZE_BY_TIER: dict[CBCSTier, dict[str, list[str]]] = {
    CBCSTier.COLD: {
        "Processing": ["CP-G-005", "CP-G-006"],   # Averted contemplative
        "Escape": ["CP-G-001", "CP-G-002"],        # Provocative direct
        "Discovery": ["CP-G-003", "CP-G-004"],     # Curious lateral
        "Status": ["CP-G-007", "CP-G-008"],        # Challenging direct
    },
    CBCSTier.WARM: {
        "Processing": ["CP-G-009", "CP-G-010"],   # Near-direct engaged
        "Escape": ["CP-G-011", "CP-G-012"],        # Warm direct
        "Discovery": ["CP-G-013", "CP-G-014"],     # Inviting gaze
        "Status": ["CP-G-015", "CP-G-016"],        # Confident steady
    },
    CBCSTier.HOT: {
        "Processing": ["CP-G-017", "CP-G-018"],   # Intimate direct
        "Escape": ["CP-G-019", "CP-G-020"],        # Confident invitation
        "Discovery": ["CP-G-021", "CP-G-022"],     # Knowing look
        "Status": ["CP-G-023", "CP-G-024"],        # Authority direct
    },
}


# =====================================================
#  Expression Presets by Mood (§4 Stage 1, Step 5)
# =====================================================

EXPRESSION_BY_MOOD: dict[str, dict[str, float]] = {
    "Processing": {"brow_furrow": 0.5, "eye_squint": 0.3, "smile_duchenne": 0.2},
    "Escape": {"smile_duchenne": 0.6, "eye_squint": 0.4, "smirk": 0.2},
    "Discovery": {"brow_raise": 0.6, "eye_wide": 0.4, "smile_duchenne": 0.3},
    "Status": {"brow_furrow": 0.4, "lip_press": 0.3, "chin_raise": 0.3},
}


# =====================================================
#  Mood Visual Routing (§4 Stage 1, Step 2)
# =====================================================

MOOD_VISUAL_BY_STATE: dict[str, list[str]] = {
    "Processing": ["CP-MV-001", "CP-MV-002", "CP-MV-003"],
    "Escape": ["CP-MV-007", "CP-MV-008", "CP-MV-009"],
    "Discovery": ["CP-MV-013", "CP-MV-014", "CP-MV-015"],
    "Status": ["CP-MV-019", "CP-MV-020", "CP-MV-021"],
}


# =====================================================
#  Format Routing (§4 Stage 2)
# =====================================================

FORMAT_ROUTING: dict[OutputFormat, str] = {
    OutputFormat.SHORT_VIDEO: "cac_composer",
    OutputFormat.CAROUSEL: "carousel_builder",
    OutputFormat.THUMBNAIL: "thumbnail_renderer",
    OutputFormat.FLYER: "static_composition",
    OutputFormat.WEBINAR: "event_page_builder",
    OutputFormat.STORY: "story_renderer",
    OutputFormat.POLL: "crowdpurr_template",
    OutputFormat.EMAIL: "email_hero_renderer",
}


# =====================================================
#  Anti-Draft Constraint System (§4 Stage 3)
# =====================================================

class AntiDraftEngine:
    """
    §4 Stage 3: 2-Level Anti-Draft Constraint System.
    Level 1: Stock thumbnail detection.
    Level 2: Format-specific rejection patterns.
    """

    def check_level_1(
        self,
        mood_visual_cp_id: str | None,
        kelvin: float | None = None,
        saturation_pct: float | None = None,
        has_plain_background: bool = False,
        expression_is_default: bool = False,
    ) -> AntiDraftResult:
        """
        Level 1 — Stock Thumbnail Anti-Draft.
        Studio lighting (>5500K, <40% sat) + plain bg + generic expression → REJECT.
        """
        is_studio = False
        if kelvin is not None and saturation_pct is not None:
            is_studio = kelvin > ANTI_DRAFT_KELVIN_THRESHOLD and saturation_pct < ANTI_DRAFT_SATURATION_THRESHOLD

        if is_studio and has_plain_background and expression_is_default:
            return AntiDraftResult(
                passed=False,
                level=AntiDraftLevel.LEVEL_1_STOCK,
                violation_reason=(
                    "Stock thumbnail detected: studio lighting + plain background + "
                    "generic expression. This looks like every other coach's content."
                ),
                suggestion="Use warmer lighting (CP-MV-007+), textured background, and a specific expression preset.",
            )

        return AntiDraftResult(passed=True)

    def check_level_2(
        self,
        output_format: OutputFormat,
        has_face: bool = True,
        face_position: str = "centered",
        clip_similarity: float | None = None,
    ) -> AntiDraftResult:
        """
        Level 2 — Format-Specific Anti-Draft.
        """
        # Carousel cover with no face
        if output_format == OutputFormat.CAROUSEL and not has_face:
            return AntiDraftResult(
                passed=False,
                level=AntiDraftLevel.LEVEL_2_FORMAT,
                violation_reason="Carousel cover must include a face for emotional contagion.",
                suggestion="Add coach face to carousel cover.",
            )

        # Thumbnail with centered face (no rule-of-thirds)
        if output_format == OutputFormat.THUMBNAIL and face_position == "centered":
            return AntiDraftResult(
                passed=False,
                level=AntiDraftLevel.LEVEL_2_FORMAT,
                violation_reason="Thumbnail face must follow rule-of-thirds, not center.",
                suggestion="Position face in left or right third.",
            )

        # CLIP deduplication
        if clip_similarity is not None and clip_similarity > CLIP_DEDUP_THRESHOLD:
            return AntiDraftResult(
                passed=False,
                level=AntiDraftLevel.LEVEL_2_FORMAT,
                violation_reason=(
                    f"Too similar to recent content (CLIP: {clip_similarity:.2f} > {CLIP_DEDUP_THRESHOLD}). "
                    f"Coach's feed will look repetitive."
                ),
                suggestion="Vary body position, expression, or scene.",
            )

        return AntiDraftResult(passed=True)


# =====================================================
#  First Frame Composer — Iris (§4 Stage 1)
# =====================================================

class IrisFirstFrameComposer:
    """
    §4 Stage 1: 6-Step Deterministic Decision Engine.
    No LLM reasoning — pure rule-based composition.

    Step 1: Format Constraints → dimensions, face rule, text zone
    Step 2: Mood Visual → CP-MV selection
    Step 3: Gaze Vector → CP-G selection
    Step 4: Text Hook → headline, position, font treatment
    Step 5: Expression → ConsciousSmile channel values
    Step 6: Compose & Audit → complete first_frame_spec + Receipt Chain Guard
    """

    def __init__(self) -> None:
        self._anti_draft = AntiDraftEngine()
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""
        self._recent_specs: list[FirstFrameSpec] = []

    def compose(
        self,
        coach_id: str,
        output_format: OutputFormat | str,
        mood_state: str,
        cbcs_tier: CBCSTier | str,
        identity_lora_path: str,
        body_cp_id: str | None = None,
        hands_cp_id: str | None = None,
        text_headline: str | None = None,
        beat_cluster_id: str | None = None,
        props_cp_id: str | None = None,
    ) -> FirstFrameSpec:
        """
        Execute the 6-step decision engine.
        Returns a complete FirstFrameSpec.
        """
        # Normalize enums
        if isinstance(output_format, str):
            output_format = OutputFormat(output_format)
        if isinstance(cbcs_tier, str):
            cbcs_tier = CBCSTier(cbcs_tier)

        reasoning: dict[str, str] = {}

        # === Step 1: Format Constraints ===
        constraints = FORMAT_CONSTRAINTS.get(output_format)
        if constraints is None:
            raise VisualPipelineError(
                code="UNSUPPORTED_FORMAT",
                message=f"Output format '{output_format}' is not supported.",
            )
        reasoning["step_1_format"] = f"Format={output_format.value}, dims={constraints.dimensions}"

        # === Step 2: Mood Visual ===
        mood_visuals = MOOD_VISUAL_BY_STATE.get(mood_state, ["CP-MV-001"])
        mood_visual_cp_id = mood_visuals[0]  # Deterministic: always first match
        reasoning["step_2_mood_visual"] = f"Mood={mood_state} → {mood_visual_cp_id}"

        # === Step 3: Gaze Vector ===
        tier_gazes = GAZE_BY_TIER.get(cbcs_tier, {})
        mood_gazes = tier_gazes.get(mood_state, ["CP-G-001"])
        gaze_cp_id = mood_gazes[0]  # Deterministic
        reasoning["step_3_gaze"] = f"CBCS={cbcs_tier.value}, Mood={mood_state} → {gaze_cp_id}"

        # === Step 4: Text Hook ===
        sanitized_headline = None
        text_position = None
        text_font_treatment = None
        if text_headline:
            # §10 Safety: Text injection sanitization
            sanitized_headline = html.escape(text_headline)
            sanitized_headline = re.sub(r"<[^>]+>", "", sanitized_headline)
            text_position = constraints.text_zone
            text_font_treatment = "bold_sans_serif"
        reasoning["step_4_text"] = f"Headline={'set' if sanitized_headline else 'none'}, pos={text_position}"

        # === Step 5: Expression ===
        expression_channels = EXPRESSION_BY_MOOD.get(mood_state, {})
        reasoning["step_5_expression"] = f"Mood={mood_state} → {len(expression_channels)} channels"

        # === Step 6: Compose & Audit ===
        face_position = constraints.face_position_rule

        # Anti-draft Level 1
        l1_result = self._anti_draft.check_level_1(
            mood_visual_cp_id=mood_visual_cp_id,
            expression_is_default=len(expression_channels) == 0,
        )

        # Anti-draft Level 2
        l2_result = self._anti_draft.check_level_2(
            output_format=output_format,
            has_face=constraints.face_required,
            face_position=face_position,
        )

        anti_draft_passed = l1_result.passed and l2_result.passed
        reasoning["step_6_anti_draft"] = (
            f"L1={'PASS' if l1_result.passed else 'FAIL'}, "
            f"L2={'PASS' if l2_result.passed else 'FAIL'}"
        )

        # Route to downstream pipeline
        routed_to = FORMAT_ROUTING.get(output_format, "unknown")

        spec = FirstFrameSpec(
            coach_id=coach_id,
            output_format=output_format,
            dimensions=constraints.dimensions,
            mood_state=mood_state,
            cbcs_tier=cbcs_tier,
            body_cp_id=body_cp_id,
            hands_cp_id=hands_cp_id,
            gaze_cp_id=gaze_cp_id,
            scene_cp_id=None,
            mood_visual_cp_id=mood_visual_cp_id,
            props_cp_id=props_cp_id,
            expression_spec={"channels": expression_channels, "mode": "mood_derived"},
            text_headline=sanitized_headline,
            text_position=text_position,
            text_font_treatment=text_font_treatment,
            identity_lora_path=identity_lora_path,
            reasoning=reasoning,
            anti_draft_passed=anti_draft_passed,
            routed_to=routed_to,
        )

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_FFC_COMPOSE,
            agent_name="iris_first_frame_composer",
            input_payload={
                "coach_id": coach_id,
                "format": output_format.value,
                "mood_state": mood_state,
                "cbcs_tier": cbcs_tier.value,
            },
            output_payload={
                "spec_id": spec.spec_id,
                "routed_to": routed_to,
                "anti_draft_passed": anti_draft_passed,
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        spec.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        self._recent_specs.append(spec)
        return spec

    def get_format_constraints(self, output_format: OutputFormat) -> FormatConstraints | None:
        return FORMAT_CONSTRAINTS.get(output_format)

    def get_anti_draft_engine(self) -> AntiDraftEngine:
        return self._anti_draft

    def get_recent_specs(self) -> list[FirstFrameSpec]:
        return list(self._recent_specs)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)
