"""
FR-VIS-11 — In-App Image Search Panel (Backend Adapter)
=========================================================
Manages search panel state, style-directive filtering of results,
image slot placement, and Asset History Table logging.

Pipeline stages:
  Stage 1 — Search dispatch via FR-VIS-10 multi_api_image_search
  Stage 2 — Style directive filtering & resolution warnings
  Stage 3 — Slot placement + Asset History logging
"""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    MIN_SEARCH_RESOLUTION_PX,
    AssetHistoryEntry,
    ImageSearchPanelError,
    ImageSlotPlacement,
    MultiAPISearchResponse,
    NormalizedSearchResult,
    OriginalImageInfo,
    RankedResult,
    ReplacementImageInfo,
    SearchPanelState,
    SearchPanelTab,
    StyleDirectiveFilter,
    SwapSourceType,
)


# ---------------------------------------------------------------------------
# Style-to-hidden-sources mapping
# ---------------------------------------------------------------------------

# GIPHY animated content hidden source key
_GIPHY_ANIMATED = "giphy_animated"
_RUNNINGHUB_GHIBLI = "runninghub_ghibli"

# Formats that prohibit animated GIFs
_ANIMATION_PROHIBITED_FORMATS: frozenset[str] = frozenset({
    "carousel_dopamine_cliff",
    "carousel_story_arc",
    "carousel_authority_stack",
    "single_image_hero_moment",
    "single_image_text_overlay",
    "infographic_comparison",
    "infographic_process",
})

# Formats that prohibit Ghibli illustration style
_GHIBLI_PROHIBITED_FORMATS: frozenset[str] = frozenset({
    "carousel_dopamine_cliff",
    "carousel_story_arc",
    "carousel_authority_stack",
})


# ---------------------------------------------------------------------------
# Image Search Panel Adapter
# ---------------------------------------------------------------------------

class ImageSearchPanelAdapter:
    """
    Backend adapter for the In-App Image Search Panel.
    Manages panel state, style filtering, placement, and history logging.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got '{coach_acronym}'"
            )
        self._coach = coach_acronym
        self._rc = receipt_chain
        self._asset_history: list[AssetHistoryEntry] = []
        self._sessions: dict[str, SearchPanelState] = {}

    @property
    def coach_acronym(self) -> str:
        return self._coach

    @property
    def asset_history(self) -> list[AssetHistoryEntry]:
        return list(self._asset_history)

    # ====================================================================
    # Session Management
    # ====================================================================

    def open_session(
        self,
        composition_id: str,
        content_format: Optional[str] = None,
        permitted_styles: Optional[list[str]] = None,
    ) -> SearchPanelState:
        """
        Open a new panel session for a composition.
        Computes the style directive filter based on format constraints.
        """
        session_id = f"ISP-{self._coach}-{uuid.uuid4().hex[:8]}"

        style_filter = self._compute_style_filter(
            content_format, permitted_styles
        )

        state = SearchPanelState(
            panel_session_id=session_id,
            composition_id=composition_id,
            coach_acronym=self._coach,
            style_directive_filter=style_filter,
        )
        self._sessions[session_id] = state

        self._rc.log(
            agent_id="image_search_panel",
            action="session_opened",
            asset_id=composition_id,
            input_summary=f"format={content_format or 'unspecified'}",
            output_summary=f"session={session_id}",
        )

        return state

    def get_session(self, session_id: str) -> SearchPanelState | None:
        return self._sessions.get(session_id)

    # ====================================================================
    # Style Directive Filtering
    # ====================================================================

    @staticmethod
    def _compute_style_filter(
        content_format: Optional[str],
        permitted_styles: Optional[list[str]],
    ) -> StyleDirectiveFilter:
        """Build the style filter for hiding incompatible sources."""
        hidden: list[str] = []

        if content_format:
            if content_format in _ANIMATION_PROHIBITED_FORMATS:
                hidden.append(_GIPHY_ANIMATED)
            if content_format in _GHIBLI_PROHIBITED_FORMATS:
                hidden.append(_RUNNINGHUB_GHIBLI)

        return StyleDirectiveFilter(
            permitted_styles=permitted_styles or [],
            hidden_sources=hidden,
        )

    @staticmethod
    def filter_results(
        results: list[RankedResult],
        style_filter: StyleDirectiveFilter,
    ) -> tuple[list[RankedResult], int]:
        """
        Filter ranked results by style directive.
        Returns (visible_results, count_filtered_out).
        """
        if not style_filter.hidden_sources:
            return results, 0

        visible: list[RankedResult] = []
        filtered_count = 0

        for r in results:
            source_api = r.source_api.lower()

            # Check if this result's source is hidden
            hidden = False
            if _GIPHY_ANIMATED in style_filter.hidden_sources:
                if source_api == "giphy":
                    hidden = True
            if _RUNNINGHUB_GHIBLI in style_filter.hidden_sources:
                if source_api == "runninghub_ghibli":
                    hidden = True

            if hidden:
                filtered_count += 1
            else:
                visible.append(r)

        return visible, filtered_count

    @staticmethod
    def is_tab_available(
        tab: str,
        style_filter: StyleDirectiveFilter,
    ) -> bool:
        """Check if a tab should be available given style constraints."""
        if tab == SearchPanelTab.GIFS:
            return _GIPHY_ANIMATED not in style_filter.hidden_sources
        if tab == SearchPanelTab.AI_GENERATE:
            # AI generate tab shows if at least one AI source is visible
            return _RUNNINGHUB_GHIBLI not in style_filter.hidden_sources
        return True

    # ====================================================================
    # Resolution Warning
    # ====================================================================

    @staticmethod
    def check_resolution_warning(
        width_px: int,
        height_px: int,
        minimum_px: int = MIN_SEARCH_RESOLUTION_PX,
    ) -> tuple[bool, str | None]:
        """
        Returns (is_warning, message).
        Warning if shortest edge < minimum_px.
        Does NOT block placement — operator override.
        """
        shortest = min(width_px, height_px)
        if shortest < minimum_px:
            return True, (
                f"Low resolution ({width_px}×{height_px}) — "
                f"may appear pixelated at export"
            )
        return False, None

    # ====================================================================
    # Image Slot Placement
    # ====================================================================

    def place_image(
        self,
        session_id: str,
        slide_index: int,
        image_url: str,
        source_type: str,
        source_api: str = "",
        width_px: int = 0,
        height_px: int = 0,
        *,
        original_url: str = "",
        original_source_type: str = "",
        original_source_api: str = "",
        operator_id: str = "",
        swap_reason: Optional[str] = None,
    ) -> ImageSlotPlacement:
        """
        Place an image into a canvas slot.
        Logs an AssetHistoryEntry and writes a receipt.
        """
        session = self._sessions.get(session_id)
        if not session:
            return ImageSlotPlacement(
                placement_id="",
                slide_index=slide_index,
                image_url=image_url,
                source_type=source_type,
                success=False,
                error_type=ImageSearchPanelError.SLOT_NOT_SELECTED,
            )

        # Compute resolution warning
        has_warning, warning_msg = self.check_resolution_warning(
            width_px, height_px
        )

        # Simulate R2 upload (in production: download → upload to R2)
        r2_url = f"https://r2.ccf-assets.com/manual/{hashlib.sha256(image_url.encode()).hexdigest()[:16]}.jpg"

        placement_id = f"PLC-{self._coach}-{uuid.uuid4().hex[:8]}"
        placement = ImageSlotPlacement(
            placement_id=placement_id,
            slide_index=slide_index,
            image_url=image_url,
            source_type=source_type,
            r2_storage_url=r2_url,
            resolution_warning=has_warning,
            warning_message=warning_msg,
            success=True,
        )

        # Log asset history
        ts = datetime.now(timezone.utc).isoformat()
        swap_id = f"SWAP-{self._coach}-{uuid.uuid4().hex[:8]}"

        history_entry = AssetHistoryEntry(
            swap_id=swap_id,
            composition_id=session.composition_id,
            slide_index=slide_index,
            original_image=OriginalImageInfo(
                url=original_url or "unknown",
                source_type=original_source_type,
                source_api=original_source_api or None,
            ),
            replacement_image=ReplacementImageInfo(
                url=image_url,
                source_type=source_type,
                source_api=source_api or None,
            ),
            operator_id=operator_id or "unknown",
            swap_reason=swap_reason,
            swap_timestamp_utc=ts,
            receipt_chain_block=f"RCB-SWAP-{swap_id}",
        )
        self._asset_history.append(history_entry)

        # Update session state
        session.total_swaps_this_session += 1
        if has_warning:
            session.resolution_warnings_shown += 1

        # Receipt write
        self._rc.log(
            agent_id="image_search_panel",
            action="image_placed",
            asset_id=session.composition_id,
            input_summary=(
                f"slide={slide_index}, source={source_type}, "
                f"operator={operator_id}"
            ),
            output_summary=f"swap_id={swap_id}, r2={r2_url}",
        )

        return placement

    # ====================================================================
    # Sanitisation
    # ====================================================================

    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """
        Strip XSS / injection vectors from search queries.
        Panel renders escaped text only.
        """
        # Strip script blocks (tag + content)
        cleaned = re.sub(r"<script[^>]*>.*?</script>", "", query, flags=re.IGNORECASE | re.DOTALL)
        # Strip remaining HTML tags
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        # Strip script-injection chars
        cleaned = re.sub(r"[<>&\"';]", "", cleaned)
        return cleaned.strip()

    # ====================================================================
    # Photo Deck Access Control
    # ====================================================================

    def validate_photo_deck_access(
        self,
        requesting_coach: str,
    ) -> bool:
        """
        Validates that the requesting coach matches the panel's coach scope.
        Returns False (403-equivalent) for unauthorized access.
        """
        return requesting_coach.upper() == self._coach.upper()
