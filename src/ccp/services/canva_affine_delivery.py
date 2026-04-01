"""FR-CA11-11 — CVE Canva Clone → AFFiNE Delivery.

Rewires the Conscious Canva App's composition-approve flow to deliver
Visual Production Output (VPO) to the coach's AFFiNE Visual Production
Console instead of (or alongside) Notion.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    CanvaApproveWebhookPayload,
    DeliveryTargetFlag,
    VisualProductionOutput,
    VPODeliveryResult,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VPC_SECTION = "visual-production-console"
DEFAULT_DELIVERY_TARGET = DeliveryTargetFlag.affine_only
COLLAPSIBLE_AUDIT_KEYS = {"tiar_decay_audit", "receipt_chain_status", "fingerprint_id"}

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

VPO_ENTRIES_SQL = """
CREATE TABLE IF NOT EXISTS vpo_entries (
    entry_id        TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL,
    asset_id        TEXT NOT NULL,
    composition_id  TEXT NOT NULL,
    recipe_name     TEXT NOT NULL,
    visual_style    TEXT NOT NULL,
    slide_count     INTEGER NOT NULL,
    stitch_url      TEXT NOT NULL,
    zip_url         TEXT NOT NULL,
    fingerprint_id  TEXT,
    receipt_status  TEXT NOT NULL DEFAULT 'PENDING',
    deep_link       TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class AFFiNESyncProtocol(Protocol):
    async def push_content(self, workspace_id: str, section: str,
                           payload: dict[str, Any]) -> str: ...


class NotionSyncProtocol(Protocol):
    async def push_content(self, workspace_id: str, section: str,
                           payload: dict[str, Any]) -> str: ...


# ---------------------------------------------------------------------------
# Console Entry Builder
# ---------------------------------------------------------------------------


class VPOConsoleEntryBuilder:
    """Builds the AFFiNE Visual Production Console database entry layout."""

    @staticmethod
    def build_entry(vpo: VisualProductionOutput,
                    deep_link: str | None = None) -> dict[str, Any]:
        """Transform VPO into the AFFiNE console entry format."""
        slides_preview = [
            {
                "slide_number": s.slide_number,
                "png_url": s.png_url,
                "agss_score": s.agss_score,
            }
            for s in vpo.slides
        ]

        entry: dict[str, Any] = {
            "entry_id": f"vpo-{uuid.uuid4().hex[:12]}",
            "asset_id": vpo.asset_id,
            "composition_id": vpo.composition_id,
            "recipe_name": vpo.recipe_name,
            "visual_style": vpo.visual_style,
            "slides": slides_preview,
            "horizontal_stitch_url": vpo.horizontal_stitch_url,
            "zip_download_url": vpo.zip_download_url,
            "why_this_visual": vpo.why_this_visual,
            "leadership_farming_note": vpo.leadership_farming_note,
            # Collapsed-by-default audit section
            "audit": {
                "tiar_decay_audit": vpo.tiar_decay_audit,
                "receipt_chain_status": vpo.receipt_chain_status,
                "fingerprint_id": vpo.fingerprint_id,
            },
            "deep_link": deep_link,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        return entry

    @staticmethod
    def validate_metadata_integrity(vpo: VisualProductionOutput,
                                    entry: dict[str, Any]) -> bool:
        """AC3 — Verify TIAR, AGSS, fingerprint match between VPO and entry."""
        if entry["audit"]["tiar_decay_audit"] != vpo.tiar_decay_audit:
            return False
        if entry["audit"]["fingerprint_id"] != vpo.fingerprint_id:
            return False
        if entry["audit"]["receipt_chain_status"] != vpo.receipt_chain_status:
            return False
        # AGSS per slide
        for slide, entry_slide in zip(vpo.slides, entry["slides"]):
            if slide.agss_score != entry_slide["agss_score"]:
                return False
        return True


# ---------------------------------------------------------------------------
# Delivery Router
# ---------------------------------------------------------------------------


class DeliveryRouter:
    """Routes VPO to AFFiNE, Notion, or both based on feature flag."""

    def __init__(
        self,
        affine_sync: AFFiNESyncProtocol | None = None,
        notion_sync: NotionSyncProtocol | None = None,
    ) -> None:
        self._affine = affine_sync
        self._notion = notion_sync
        self._builder = VPOConsoleEntryBuilder()

    async def deliver(
        self, payload: CanvaApproveWebhookPayload,
    ) -> VPODeliveryResult:
        target = payload.delivery_target
        vpo = payload.vpo

        affine_ok = False
        notion_ok = False
        affine_page_id: str | None = None
        errors: list[str] = []

        # AFFiNE delivery
        if target in (DeliveryTargetFlag.affine_only, DeliveryTargetFlag.both):
            if self._affine is None:
                errors.append("AFFiNE sync not configured")
            else:
                try:
                    entry = self._builder.build_entry(vpo, payload.canva_app_deep_link)
                    affine_page_id = await self._affine.push_content(
                        payload.coach_workspace_id, VPC_SECTION, entry,
                    )
                    affine_ok = True
                except Exception as exc:
                    errors.append(f"AFFiNE delivery failed: {exc}")

        # Notion delivery (legacy / dual)
        if target in (DeliveryTargetFlag.notion_only, DeliveryTargetFlag.both):
            if self._notion is None:
                errors.append("Notion sync not configured")
            else:
                try:
                    entry = self._builder.build_entry(vpo, payload.canva_app_deep_link)
                    await self._notion.push_content(
                        payload.coach_workspace_id, VPC_SECTION, entry,
                    )
                    notion_ok = True
                except Exception as exc:
                    errors.append(f"Notion delivery failed: {exc}")

        success = (
            (target == DeliveryTargetFlag.affine_only and affine_ok)
            or (target == DeliveryTargetFlag.notion_only and notion_ok)
            or (target == DeliveryTargetFlag.both and affine_ok and notion_ok)
        )

        return VPODeliveryResult(
            success=success,
            affine_delivered=affine_ok,
            notion_delivered=notion_ok,
            affine_page_id=affine_page_id,
            error="; ".join(errors) if errors else None,
        )


# ---------------------------------------------------------------------------
# Webhook Handler (entry point)
# ---------------------------------------------------------------------------


class CanvaApproveHandler:
    """Handles incoming Canva App approve webhooks."""

    def __init__(self, router: DeliveryRouter) -> None:
        self._router = router

    async def handle(self, raw_payload: dict[str, Any]) -> VPODeliveryResult:
        payload = CanvaApproveWebhookPayload(**raw_payload)
        return await self._router.deliver(payload)
