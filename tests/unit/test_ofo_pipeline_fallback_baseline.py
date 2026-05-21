"""Unit tests — OFO Pipeline Baseline Discovery fallback.
§10.3: test_ofo_pipeline_fallback_baseline.py."""
from src.ccp.models.ofo_models import InsufficientSignalError
from src.ccp.services.ofo_engine_pipeline import OFOEnginePipeline


class MockTraitEngineFails:
    """TraitScoringEngine that always raises InsufficientSignalError."""
    def score_all_traits(self, audio_path=None):
        raise InsufficientSignalError("Audio quality too poor for trait scoring")


class TestOFOPipelineBaselineDiscoveryFallback:
    """When TraitScoringEngine throws InsufficientSignalError, pipeline generates Baseline Discovery."""

    def test_insufficient_signal_generates_baseline_package(self):
        pipeline = OFOEnginePipeline(trait_engine=MockTraitEngineFails())
        package = pipeline.process_target(target_id="target-fallback-001", source_url="https://example.com/video.mp4")
        assert package.target_id == "target-fallback-001"
        assert package.audit_data.detected_flaw == "Insufficient Audio Signal"
        assert package.audit_data.biometric_score == 0.0
        assert "compression" in package.audit_data.transcript.lower()
        assert "baseline" in package.audit_data.transcript.lower()
        # Still generates all 4 assets
        assert package.carousel is not None
        assert package.storytelling_video is not None
        assert package.reels_explainer is not None
        assert package.animated_audit is not None

    def test_baseline_package_has_correct_asset_types(self):
        pipeline = OFOEnginePipeline(trait_engine=MockTraitEngineFails())
        package = pipeline.process_target(target_id="target-fallback-002", source_url="https://example.com/v2.mp4")
        assert package.carousel.asset_type.value == "carousel"
        assert package.storytelling_video.asset_type.value == "storytelling_video"
        assert package.reels_explainer.asset_type.value == "reels_explainer"
        assert package.animated_audit.asset_type.value == "animated_audit"
