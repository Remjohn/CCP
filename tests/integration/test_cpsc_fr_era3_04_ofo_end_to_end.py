"""Integration tests — OFO end-to-end pipeline.
§10.4: test_cpsc_fr_era3_04_ofo_end_to_end.py."""
from src.ccp.models.ofo_models import OFOAssetType
from src.ccp.services.ofo_engine_pipeline import OFOEnginePipeline


class TestOFOEndToEndPipeline:
    """AC1: Complete 4-Asset Package Generation."""

    def test_process_target_returns_complete_package(self):
        pipeline = OFOEnginePipeline()
        package = pipeline.process_target(
            target_id="target-e2e-001",
            source_url="https://youtube.com/watch?v=test_stable_video",
        )
        assert package.target_id == "target-e2e-001"
        assert package.carousel is not None
        assert package.storytelling_video is not None
        assert package.reels_explainer is not None
        assert package.animated_audit is not None

    def test_package_has_exactly_4_assets(self):
        pipeline = OFOEnginePipeline()
        package = pipeline.process_target(target_id="target-e2e-002", source_url="https://example.com/v.mp4")
        assets = [package.carousel, package.storytelling_video, package.reels_explainer, package.animated_audit]
        assert len(assets) == 4
        assert all(a is not None for a in assets)

    def test_asset_types_are_correct(self):
        pipeline = OFOEnginePipeline()
        package = pipeline.process_target(target_id="target-e2e-003", source_url="https://example.com/v.mp4")
        assert package.carousel.asset_type == OFOAssetType.CAROUSEL
        assert package.storytelling_video.asset_type == OFOAssetType.STORYTELLING_VIDEO
        assert package.reels_explainer.asset_type == OFOAssetType.REELS_EXPLAINER
        assert package.animated_audit.asset_type == OFOAssetType.ANIMATED_AUDIT

    def test_audit_data_passes_phase5_m03(self):
        """AC2: Audit transcript passes Crusade Narrative validator."""
        pipeline = OFOEnginePipeline()
        package = pipeline.process_target(target_id="target-e2e-004", source_url="https://example.com/v.mp4")
        transcript = package.audit_data.transcript.lower()
        # Must contain at least 2 ideological themes
        themes = ["algorithm", "compression", "flattening", "legacy", "defend", "protect"]
        matches = sum(1 for t in themes if t in transcript)
        assert matches >= 2
        # Must not contain forbidden clinical words
        assert "poor" not in transcript
        assert "weak" not in transcript
        assert "bad" not in transcript
        assert "inadequate" not in transcript

    def test_package_has_valid_asset_urls(self):
        pipeline = OFOEnginePipeline()
        package = pipeline.process_target(target_id="target-e2e-005", source_url="https://example.com/v.mp4")
        assert package.carousel.asset_url.startswith("s3://")
        assert package.animated_audit.asset_url.startswith("s3://")
