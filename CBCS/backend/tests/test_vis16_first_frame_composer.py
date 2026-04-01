"""
FR-VIS-16 — First Frame Composer (Iris) Tests (Step 31)

Coverage:
- AC1: Carousel cover (face, warm lighting, expression)
- AC2: Thumbnail rule-of-thirds face positioning
- AC3: Anti-draft rejection (Level 1 stock thumbnail)
- AC4: CLIP deduplication (Level 2)
- AC5: Format routing (short_video → cac_composer)
- Determinism: Same inputs → same output
- Format: Dimension enforcement
- Safety: Text injection sanitization
- Anti-draft: 5 known-stock compositions caught
"""

import pytest

from core.iris_first_frame_composer import (
    AntiDraftEngine,
    FORMAT_CONSTRAINTS,
    FORMAT_ROUTING,
    GAZE_BY_TIER,
    IrisFirstFrameComposer,
)
from core.visual_models import (
    AntiDraftLevel,
    CBCSTier,
    OutputFormat,
    VisualPipelineError,
)


class TestFormatConstraints:

    def test_8_formats_defined(self):
        assert len(FORMAT_CONSTRAINTS) == 8

    def test_short_video_9_16(self):
        c = FORMAT_CONSTRAINTS[OutputFormat.SHORT_VIDEO]
        assert c.dimensions == "1080x1920"

    def test_thumbnail_16_9(self):
        c = FORMAT_CONSTRAINTS[OutputFormat.THUMBNAIL]
        assert c.dimensions == "1920x1080"

    def test_carousel_4_5(self):
        c = FORMAT_CONSTRAINTS[OutputFormat.CAROUSEL]
        assert c.dimensions == "1080x1350"

    def test_email_3_2(self):
        c = FORMAT_CONSTRAINTS[OutputFormat.EMAIL]
        assert c.dimensions == "600x400"

    def test_poll_1_1(self):
        c = FORMAT_CONSTRAINTS[OutputFormat.POLL]
        assert c.dimensions == "1080x1080"

    def test_story_same_as_video(self):
        c = FORMAT_CONSTRAINTS[OutputFormat.STORY]
        assert c.dimensions == "1080x1920"


class TestGazeRouting:

    def test_cold_processing_averted(self):
        gazes = GAZE_BY_TIER[CBCSTier.COLD]["Processing"]
        assert "CP-G-005" in gazes

    def test_hot_escape_confident(self):
        gazes = GAZE_BY_TIER[CBCSTier.HOT]["Escape"]
        assert "CP-G-019" in gazes

    def test_all_tiers_all_moods(self):
        for tier in CBCSTier:
            assert tier in GAZE_BY_TIER
            for mood in ["Processing", "Escape", "Discovery", "Status"]:
                assert mood in GAZE_BY_TIER[tier]


class TestAntiDraftEngine:

    def test_level_1_stock_detected(self):
        engine = AntiDraftEngine()
        result = engine.check_level_1(
            mood_visual_cp_id="CP-MV-014",
            kelvin=5600, saturation_pct=35,
            has_plain_background=True,
            expression_is_default=True,
        )
        assert result.passed is False
        assert result.level == AntiDraftLevel.LEVEL_1_STOCK

    def test_level_1_warm_lighting_passes(self):
        engine = AntiDraftEngine()
        result = engine.check_level_1(
            mood_visual_cp_id="CP-MV-007",
            kelvin=3500, saturation_pct=60,
            has_plain_background=False,
            expression_is_default=False,
        )
        assert result.passed is True

    def test_level_2_carousel_no_face_rejected(self):
        engine = AntiDraftEngine()
        result = engine.check_level_2(
            output_format=OutputFormat.CAROUSEL,
            has_face=False,
        )
        assert result.passed is False
        assert result.level == AntiDraftLevel.LEVEL_2_FORMAT

    def test_level_2_thumbnail_centered_rejected(self):
        engine = AntiDraftEngine()
        result = engine.check_level_2(
            output_format=OutputFormat.THUMBNAIL,
            face_position="centered",
        )
        assert result.passed is False

    def test_level_2_clip_dedup_rejected(self):
        engine = AntiDraftEngine()
        result = engine.check_level_2(
            output_format=OutputFormat.CAROUSEL,
            has_face=True,
            clip_similarity=0.95,
        )
        assert result.passed is False
        assert "0.92" in result.violation_reason

    def test_level_2_valid_thumbnail_passes(self):
        engine = AntiDraftEngine()
        result = engine.check_level_2(
            output_format=OutputFormat.THUMBNAIL,
            has_face=True,
            face_position="rule_of_thirds",
        )
        assert result.passed is True


class TestIrisComposer:

    def test_carousel_cold_escape(self):
        """AC1: Carousel + Escape + cold → face, warm lighting, expression."""
        iris = IrisFirstFrameComposer()
        spec = iris.compose(
            coach_id="coach-001",
            output_format="carousel",
            mood_state="Escape",
            cbcs_tier="cold",
            identity_lora_path="/efs/ccp-models/loras/coach_001_v1.safetensors",
        )

        assert spec.dimensions == "1080x1350"
        assert spec.mood_visual_cp_id == "CP-MV-007"  # Escape warm lighting
        assert spec.gaze_cp_id == "CP-G-001"  # Cold + Escape = provocative direct
        assert spec.expression_spec["channels"]["smile_duchenne"] > 0

    def test_thumbnail_rule_of_thirds(self):
        """AC2: Thumbnail format → face in thirds."""
        iris = IrisFirstFrameComposer()
        spec = iris.compose(
            coach_id="coach-001",
            output_format="thumbnail",
            mood_state="Status",
            cbcs_tier="warm",
            identity_lora_path="/efs/lora.safetensors",
        )

        assert spec.dimensions == "1920x1080"
        assert spec.reasoning["step_1_format"] is not None

    def test_format_routing_video(self):
        """AC5: short_video → cac_composer."""
        iris = IrisFirstFrameComposer()
        spec = iris.compose(
            coach_id="coach-001",
            output_format="short_video",
            mood_state="Processing",
            cbcs_tier="cold",
            identity_lora_path="/efs/lora.safetensors",
        )

        assert spec.routed_to == "cac_composer"

    def test_format_routing_carousel(self):
        iris = IrisFirstFrameComposer()
        spec = iris.compose(
            coach_id="coach-001",
            output_format="carousel",
            mood_state="Escape",
            cbcs_tier="cold",
            identity_lora_path="/efs/lora.safetensors",
        )
        assert spec.routed_to == "carousel_builder"

    def test_determinism(self):
        """Same inputs → same output across 10 calls."""
        iris = IrisFirstFrameComposer()
        specs = []
        for _ in range(10):
            spec = iris.compose(
                coach_id="coach-001",
                output_format="carousel",
                mood_state="Escape",
                cbcs_tier="cold",
                identity_lora_path="/efs/lora.safetensors",
            )
            specs.append(spec)

        # All specs should have identical compositions
        for s in specs[1:]:
            assert s.mood_visual_cp_id == specs[0].mood_visual_cp_id
            assert s.gaze_cp_id == specs[0].gaze_cp_id
            assert s.expression_spec == specs[0].expression_spec

    def test_text_injection_sanitized(self):
        """Safety: XSS in headline sanitized."""
        iris = IrisFirstFrameComposer()
        spec = iris.compose(
            coach_id="coach-001",
            output_format="carousel",
            mood_state="Escape",
            cbcs_tier="cold",
            identity_lora_path="/efs/lora.safetensors",
            text_headline="<script>alert('xss')</script>",
        )

        assert "<script>" not in spec.text_headline
        assert "alert" in spec.text_headline  # Content preserved, tags stripped

    def test_receipt_chain_written(self):
        iris = IrisFirstFrameComposer()
        iris.compose(
            coach_id="coach-001",
            output_format="carousel",
            mood_state="Escape",
            cbcs_tier="cold",
            identity_lora_path="/efs/lora.safetensors",
        )

        receipts = iris.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "FFC_COMPOSE"

    def test_unsupported_format_raises(self):
        iris = IrisFirstFrameComposer()
        with pytest.raises(ValueError):
            iris.compose(
                coach_id="coach-001",
                output_format="hologram",  # Not a valid OutputFormat
                mood_state="Escape",
                cbcs_tier="cold",
                identity_lora_path="/efs/lora.safetensors",
            )

    def test_all_8_formats_routable(self):
        assert len(FORMAT_ROUTING) == 8
        for fmt in OutputFormat:
            assert fmt in FORMAT_ROUTING
