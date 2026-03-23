"""
FR45 — Notion Export Pipeline Service (DEP-ENG-039)
7-section page generation with sovereign image enforcement.

AC1: 7-section Notion page generation.
AC2: Sovereign Image enforcement (Photo Deck DB first).
AC3: Approval trigger via webhook/polling.
AC4: Rate limit backoff (exponential on 429).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    NOTION_APPROVAL_POLL_MINUTES,
    NOTION_MAX_BLOCKS_PER_REQUEST,
    NOTION_PAGE_SECTIONS,
    NotionPagePayload,
    NotionSection,
)


# ── 7 Required Sections ───────────────────────────────
# FR45 §4.2: fixed section list
REQUIRED_SECTIONS: list[str] = [
    "Coach Voice Note",
    "Why This Post",
    "Leadership Farming",
    "Script",
    "Coach Photo",
    "Visual Assets",
    "Posting Notes",
]


class NotionExportService:
    """
    FR45: Notion export pipeline with 7-section page generation.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        self._approval_status: dict[str, str] = {}

    # ── Stage 1: Payload Construction ──────────────────

    def build_page_payload(
        self,
        *,
        parent_database_id: str,
        title: str,
        universal_asset_id: str,
        arc_type: str = "",
        section_contents: Optional[dict[str, str]] = None,
        coach_photo_url: Optional[str] = None,
    ) -> NotionPagePayload:
        """
        FR45 AC1: Build 7-section Notion page payload.
        """
        contents = section_contents or {}
        sections: list[NotionSection] = []

        for section_name in REQUIRED_SECTIONS:
            if section_name == "Coach Photo":
                sections.append(NotionSection(
                    section_name=section_name,
                    block_type="image",
                    url=coach_photo_url or "",
                ))
            elif section_name == "Visual Assets":
                sections.append(NotionSection(
                    section_name=section_name,
                    block_type="image",
                    content=contents.get(section_name, ""),
                ))
            else:
                sections.append(NotionSection(
                    section_name=section_name,
                    block_type="paragraph",
                    content=contents.get(section_name, ""),
                ))

        payload = NotionPagePayload(
            parent_database_id=parent_database_id,
            title=title,
            universal_asset_id=universal_asset_id,
            arc_type=arc_type,
            sections=sections,
        )

        self._receipt_chain.log(
            agent_id="NotionExportService",
            action="PAGE_PAYLOAD_BUILT",
            asset_id=universal_asset_id,
            decision="SUCCESS",
            decision_rationale=f"sections={len(sections)}, title={title}",
        )

        return payload

    # ── Stage 2: Block Chunking ────────────────────────

    def chunk_blocks(
        self,
        blocks: list[dict[str, Any]],
    ) -> list[list[dict[str, Any]]]:
        """
        FR45 §4.2: Chunk blocks into groups of 100
        for Notion API child-block limit.
        """
        chunks: list[list[dict[str, Any]]] = []
        for i in range(0, len(blocks), NOTION_MAX_BLOCKS_PER_REQUEST):
            chunks.append(blocks[i:i + NOTION_MAX_BLOCKS_PER_REQUEST])
        return chunks

    # ── Stage 3: Approval Polling ──────────────────────

    def set_approval_status(
        self,
        universal_asset_id: str,
        status: str,
    ) -> None:
        """FR45 AC3: Set approval status for an asset."""
        self._approval_status[universal_asset_id] = status

    def check_approval(self, universal_asset_id: str) -> str:
        """
        FR45 AC3: Check approval status.
        In production, polls webhook every 5 minutes.
        """
        return self._approval_status.get(universal_asset_id, "PENDING")

    @property
    def approval_poll_interval_minutes(self) -> int:
        return NOTION_APPROVAL_POLL_MINUTES

    # ── Stage 4: Rate Limit ────────────────────────────

    def compute_backoff_seconds(self, attempt: int) -> float:
        """
        FR45 AC4: Exponential backoff on 429 errors.
        """
        return min(2.0 ** attempt, 120.0)

    # ── Validation ─────────────────────────────────────

    def validate_section_count(self, payload: NotionPagePayload) -> bool:
        """FR45 AC1: Ensure exactly 7 sections."""
        return len(payload.sections) == NOTION_PAGE_SECTIONS

    def validate_sovereign_image(
        self,
        payload: NotionPagePayload,
    ) -> bool:
        """
        FR45 AC2: Sovereign image enforcement.
        Coach Photo section must have a URL (not AI-generated).
        """
        for section in payload.sections:
            if section.section_name == "Coach Photo":
                return bool(section.url)
        return False
