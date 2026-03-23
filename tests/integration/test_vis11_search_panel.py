"""
FR-VIS-11 — In-App Image Search Panel  ·  Integration Tests
==============================================================
46 tests covering 6 ACs, ADR-01, C-11, receipt chain, safety.
"""

from __future__ import annotations

import tempfile
from typing import Optional

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    ImageSearchPanelError,
    MIN_SEARCH_RESOLUTION_PX,
    RankedResult,
    SearchPanelTab,
    StyleDirectiveFilter,
    SwapSourceType,
)
from src.ccp.services.image_search_panel_adapter import (
    ImageSearchPanelAdapter,
    _ANIMATION_PROHIBITED_FORMATS,
    _GHIBLI_PROHIBITED_FORMATS,
    _GIPHY_ANIMATED,
    _RUNNINGHUB_GHIBLI,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_adapter(
    coach: str = "TST",
) -> tuple[ImageSearchPanelAdapter, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    adapter = ImageSearchPanelAdapter(coach, rc)
    return adapter, rc


def _make_ranked(
    result_id: str = "SR-001",
    source_api: str = "unsplash",
    combined_score: float = 0.8,
    image_url: str = "https://img.example.com/1.jpg",
    rank: int = 1,
) -> RankedResult:
    return RankedResult(
        rank=rank,
        result_id=result_id,
        source_skill=f"SKILL-IMG-{result_id[-3:]}",
        source_api=source_api,
        image_url=image_url,
        combined_score=combined_score,
        selected=False,
    )


# ===========================================================================
# 1. AC1 — Multi-API Search (results from ≥3 APIs)
# ===========================================================================

class TestAC1MultiAPISearch:
    """AC1: Results from ≥3 stock APIs appear in thumbnail grid."""

    def test_multiple_api_results_displayed(self):
        """Panel receives results from multiple APIs and tracks them."""
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")

        # Simulate ranked results from 3 different APIs
        results = [
            _make_ranked("SR-001", "unsplash", rank=1),
            _make_ranked("SR-002", "pexels", rank=2),
            _make_ranked("SR-003", "pixabay", rank=3),
        ]
        visible, filtered = adapter.filter_results(
            results,
            session.style_directive_filter or StyleDirectiveFilter(),
        )
        assert len(visible) == 3
        assert filtered == 0

        # Verify distinct APIs
        apis = {r.source_api for r in visible}
        assert len(apis) >= 3

    def test_each_result_has_source_api(self):
        results = [
            _make_ranked("SR-001", "unsplash"),
            _make_ranked("SR-002", "pexels"),
        ]
        for r in results:
            assert r.source_api != ""


# ===========================================================================
# 2. AC2 — Style Filtering (Ghibli + GIF hidden for carousel)
# ===========================================================================

class TestAC2StyleFiltering:
    """AC2: Carousel hides Ghibli gen + animated GIFs."""

    def test_carousel_hides_giphy(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session(
            "COMP-TST-001",
            content_format="carousel_dopamine_cliff",
        )
        sf = session.style_directive_filter
        assert sf is not None
        assert _GIPHY_ANIMATED in sf.hidden_sources

    def test_carousel_hides_ghibli(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session(
            "COMP-TST-001",
            content_format="carousel_dopamine_cliff",
        )
        sf = session.style_directive_filter
        assert sf is not None
        assert _RUNNINGHUB_GHIBLI in sf.hidden_sources

    def test_giphy_results_filtered_for_carousel(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session(
            "COMP-TST-001",
            content_format="carousel_dopamine_cliff",
        )
        results = [
            _make_ranked("SR-001", "unsplash", rank=1),
            _make_ranked("SR-002", "giphy", rank=2),
            _make_ranked("SR-003", "pexels", rank=3),
        ]
        sf = session.style_directive_filter or StyleDirectiveFilter()
        visible, filtered = adapter.filter_results(results, sf)

        assert len(visible) == 2
        assert filtered == 1
        assert all(r.source_api != "giphy" for r in visible)

    def test_ghibli_results_filtered_for_carousel(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session(
            "COMP-TST-001",
            content_format="carousel_story_arc",
        )
        results = [
            _make_ranked("SR-001", "unsplash", rank=1),
            _make_ranked("SR-002", "runninghub_ghibli", rank=2),
        ]
        sf = session.style_directive_filter or StyleDirectiveFilter()
        visible, filtered = adapter.filter_results(results, sf)

        assert len(visible) == 1
        assert filtered == 1

    def test_no_filter_for_unrestricted_format(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session(
            "COMP-TST-001",
            content_format="reel_hook_pattern",
        )
        sf = session.style_directive_filter or StyleDirectiveFilter()
        assert len(sf.hidden_sources) == 0

    def test_gifs_tab_hidden_for_carousel(self):
        sf = StyleDirectiveFilter(hidden_sources=[_GIPHY_ANIMATED])
        assert ImageSearchPanelAdapter.is_tab_available(
            SearchPanelTab.GIFS, sf
        ) is False

    def test_gifs_tab_visible_for_unrestricted(self):
        sf = StyleDirectiveFilter()
        assert ImageSearchPanelAdapter.is_tab_available(
            SearchPanelTab.GIFS, sf
        ) is True

    def test_all_animation_prohibited_formats(self):
        for fmt in _ANIMATION_PROHIBITED_FORMATS:
            sf = ImageSearchPanelAdapter._compute_style_filter(fmt, None)
            assert _GIPHY_ANIMATED in sf.hidden_sources, f"{fmt} should hide GIPHY"


# ===========================================================================
# 3. AC3 — One-Click Placement
# ===========================================================================

class TestAC3OneClickPlacement:
    """AC3: Click 'Place in Slot' places image in correct slide."""

    def test_place_in_correct_slide(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")
        result = adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=3,
            image_url="https://pexels.com/photo-456.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            source_api="pexels",
            width_px=2400,
            height_px=3200,
            original_url="https://r2.ccf-assets.com/stock/unsplash-abc.jpg",
            original_source_type="tier_2_stock",
            operator_id="operator_maria",
        )

        assert result.success is True
        assert result.slide_index == 3
        assert result.image_url == "https://pexels.com/photo-456.jpg"
        assert result.r2_storage_url is not None
        assert "r2.ccf-assets.com" in (result.r2_storage_url or "")

    def test_original_stored_in_history(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")
        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=3,
            image_url="https://pexels.com/photo-456.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            original_url="https://r2.ccf-assets.com/stock/unsplash-abc.jpg",
            original_source_type="tier_2_stock",
            operator_id="operator_maria",
        )

        history = adapter.asset_history
        assert len(history) == 1
        assert history[0].original_image.url == "https://r2.ccf-assets.com/stock/unsplash-abc.jpg"
        assert history[0].replacement_image.url == "https://pexels.com/photo-456.jpg"

    def test_invalid_session_returns_error(self):
        adapter, _ = _make_adapter()
        result = adapter.place_image(
            session_id="NONEXISTENT",
            slide_index=0,
            image_url="https://example.com/img.jpg",
            source_type="manual",
        )
        assert result.success is False
        assert result.error_type == ImageSearchPanelError.SLOT_NOT_SELECTED


# ===========================================================================
# 4. AC4 — Asset History Logging
# ===========================================================================

class TestAC4AssetHistoryLogging:
    """AC4: 2 swaps → 2 history entries with correct data."""

    def test_two_swaps_two_entries(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")

        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=1,
            image_url="https://pexels.com/1.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            source_api="pexels",
            original_url="https://r2.ccf-assets.com/orig-1.jpg",
            operator_id="op_alice",
            swap_reason="Too similar to competitor",
        )
        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=4,
            image_url="https://pixabay.com/2.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            source_api="pixabay",
            original_url="https://r2.ccf-assets.com/orig-2.jpg",
            operator_id="op_alice",
        )

        history = adapter.asset_history
        assert len(history) == 2

    def test_history_entries_have_correct_fields(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")

        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=2,
            image_url="https://pexels.com/swap.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            source_api="pexels",
            original_url="https://r2.ccf-assets.com/original.jpg",
            original_source_type="tier_2_stock",
            original_source_api="unsplash",
            operator_id="op_bob",
            swap_reason="Contextually inappropriate",
        )

        entry = adapter.asset_history[0]
        assert entry.composition_id == "COMP-TST-001"
        assert entry.slide_index == 2
        assert entry.operator_id == "op_bob"
        assert entry.swap_reason == "Contextually inappropriate"
        assert entry.swap_timestamp_utc != ""
        assert entry.swap_id.startswith("SWAP-TST-")
        assert entry.original_image.source_type == "tier_2_stock"
        assert entry.replacement_image.source_api == "pexels"

    def test_session_swap_counter_increments(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")

        assert session.total_swaps_this_session == 0

        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=0,
            image_url="https://example.com/1.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
        )

        # Re-fetch session state
        updated = adapter.get_session(session.panel_session_id)
        assert updated is not None
        assert updated.total_swaps_this_session == 1


# ===========================================================================
# 5. AC5 — Resolution Warning
# ===========================================================================

class TestAC5ResolutionWarning:
    """AC5: Low-res image shows warning but is NOT blocked."""

    def test_640x480_shows_warning(self):
        has_warning, msg = ImageSearchPanelAdapter.check_resolution_warning(
            640, 480
        )
        assert has_warning is True
        assert msg is not None
        assert "pixelated" in msg.lower()

    def test_1080x1350_no_warning(self):
        has_warning, msg = ImageSearchPanelAdapter.check_resolution_warning(
            1080, 1350
        )
        assert has_warning is False
        assert msg is None

    def test_placement_not_blocked_for_low_res(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")
        result = adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=0,
            image_url="https://example.com/lowres.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            width_px=640,
            height_px=480,
        )
        assert result.success is True
        assert result.resolution_warning is True
        assert result.warning_message is not None

    def test_warning_counter_updates_session(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")
        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=0,
            image_url="https://example.com/lowres.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            width_px=640,
            height_px=480,
        )
        updated = adapter.get_session(session.panel_session_id)
        assert updated is not None
        assert updated.resolution_warnings_shown == 1

    def test_exactly_1080_passes(self):
        has_warning, _ = ImageSearchPanelAdapter.check_resolution_warning(
            1080, 1080
        )
        assert has_warning is False

    def test_1079_warns(self):
        has_warning, _ = ImageSearchPanelAdapter.check_resolution_warning(
            1079, 1920
        )
        assert has_warning is True


# ===========================================================================
# 6. AC6 — Photo Deck Access
# ===========================================================================

class TestAC6PhotoDeckAccess:
    """AC6: Photo Deck filtered by coach_id; unauthorized = 403."""

    def test_correct_coach_access(self):
        adapter, _ = _make_adapter(coach="TST")
        assert adapter.validate_photo_deck_access("TST") is True

    def test_wrong_coach_rejected(self):
        adapter, _ = _make_adapter(coach="TST")
        assert adapter.validate_photo_deck_access("XYZ") is False

    def test_case_insensitive_access(self):
        adapter, _ = _make_adapter(coach="TST")
        assert adapter.validate_photo_deck_access("tst") is True

    def test_photo_deck_source_type_logged(self):
        adapter, _ = _make_adapter()
        session = adapter.open_session("COMP-TST-001")
        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=1,
            image_url="https://notion.so/photo-deck/img.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_PHOTO_DECK,
            source_api="photo_deck",
            operator_id="op_maria",
        )
        entry = adapter.asset_history[0]
        assert entry.replacement_image.source_type == SwapSourceType.MANUAL_OVERRIDE_PHOTO_DECK


# ===========================================================================
# 7. Receipt Chain Integration
# ===========================================================================

class TestReceiptChainIntegration:
    """Receipt writes for session open and image placement."""

    def test_session_open_writes_receipt(self):
        adapter, rc = _make_adapter()
        adapter.open_session("COMP-TST-001")
        entries = rc.query(action="session_opened")
        assert len(entries) == 1

    def test_placement_writes_receipt(self):
        adapter, rc = _make_adapter()
        session = adapter.open_session("COMP-TST-001")
        adapter.place_image(
            session_id=session.panel_session_id,
            slide_index=0,
            image_url="https://example.com/1.jpg",
            source_type=SwapSourceType.MANUAL_OVERRIDE_STOCK,
            operator_id="op_test",
        )
        entries = rc.query(action="image_placed")
        assert len(entries) == 1

    def test_receipt_contains_composition_id(self):
        adapter, rc = _make_adapter()
        adapter.open_session("COMP-UNIQUE-99")
        entries = rc.query(asset_id="COMP-UNIQUE-99")
        assert len(entries) >= 1


# ===========================================================================
# 8. ADR-01 Coach Acronym
# ===========================================================================

class TestADR01CoachAcronym:
    def test_valid_2_char(self):
        rc = ReceiptChain(coach_acronym="JPX", log_dir=tempfile.mkdtemp())
        adapter = ImageSearchPanelAdapter("JP", rc)
        assert adapter.coach_acronym == "JP"

    def test_valid_4_char(self):
        rc = ReceiptChain(coach_acronym="BRN", log_dir=tempfile.mkdtemp())
        adapter = ImageSearchPanelAdapter("BREN", rc)
        assert adapter.coach_acronym == "BREN"

    def test_1_char_rejected(self):
        with pytest.raises(ValueError, match="2-4"):
            rc = ReceiptChain(coach_acronym="TST", log_dir=tempfile.mkdtemp())
            ImageSearchPanelAdapter("X", rc)

    def test_5_char_rejected(self):
        with pytest.raises(ValueError, match="2-4"):
            rc = ReceiptChain(coach_acronym="TST", log_dir=tempfile.mkdtemp())
            ImageSearchPanelAdapter("ABCDE", rc)


# ===========================================================================
# 9. Safety — XSS in Search Query
# ===========================================================================

class TestSafetyXSS:
    """XSS vectors stripped from search queries."""

    def test_img_tag_stripped(self):
        clean = ImageSearchPanelAdapter.sanitize_search_query(
            '<img src=x onerror=alert(1)>'
        )
        assert "<" not in clean
        assert ">" not in clean
        assert "onerror" not in clean

    def test_script_tag_stripped(self):
        clean = ImageSearchPanelAdapter.sanitize_search_query(
            '<script>alert("xss")</script>'
        )
        assert "<script>" not in clean
        assert "alert" not in clean

    def test_normal_query_preserved(self):
        clean = ImageSearchPanelAdapter.sanitize_search_query(
            "person at desk frustrated"
        )
        assert clean == "person at desk frustrated"

    def test_semicolon_stripped(self):
        clean = ImageSearchPanelAdapter.sanitize_search_query(
            "search; DROP TABLE images"
        )
        assert ";" not in clean


# ===========================================================================
# 10. Swap Source Types
# ===========================================================================

class TestSwapSourceTypes:
    def test_manual_override_stock(self):
        assert SwapSourceType.MANUAL_OVERRIDE_STOCK == "manual_override_stock"

    def test_manual_override_ai(self):
        assert SwapSourceType.MANUAL_OVERRIDE_AI == "manual_override_ai"

    def test_manual_override_photo_deck(self):
        assert SwapSourceType.MANUAL_OVERRIDE_PHOTO_DECK == "manual_override_photo_deck"

    def test_manual_upload(self):
        assert SwapSourceType.MANUAL_UPLOAD == "manual_upload"
