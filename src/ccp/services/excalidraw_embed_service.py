"""FR-CA11-10 — Excalidraw Embedded Workspace (BlockSuite Custom Block).

Python-side service for registering and injecting Excalidraw embed
blocks into AFFiNE pages via the sync service.  The actual React/
TypeScript component lives in ``ccp-blocks/excalidraw-embed/``; this
module handles the programmatic injection API and block lifecycle.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    EmbedInjectionRequest,
    EmbedInjectionResult,
    EmbedMode,
    ExcalidrawEmbedBlock,
    ExcalidrawState,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BLOCK_TYPE = "excalidraw-embed"
DEFAULT_WIDTH = "100%"
DEFAULT_HEIGHT = "600px"
SUPPORTED_MODES = {"view", "edit"}

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

EMBED_BLOCKS_SQL = """
CREATE TABLE IF NOT EXISTS excalidraw_embed_blocks (
    block_id        TEXT PRIMARY KEY,
    workspace_id    TEXT NOT NULL,
    page_id         TEXT NOT NULL,
    mode            TEXT NOT NULL DEFAULT 'view',
    source_asset_id TEXT,
    fallback_png_url TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class AFFiNEBlockAPIProtocol(Protocol):
    async def create_block(self, workspace_id: str, page_id: str,
                           block_type: str, props: dict[str, Any],
                           position: int) -> str: ...


class FallbackRendererProtocol(Protocol):
    async def render_png(self, excalidraw_json: dict[str, Any]) -> str: ...


# ---------------------------------------------------------------------------
# Block Builder
# ---------------------------------------------------------------------------


class ExcalidrawBlockBuilder:
    """Constructs an ``ExcalidrawEmbedBlock`` from raw Excalidraw JSON."""

    @staticmethod
    def build(
        excalidraw_json: dict[str, Any],
        mode: EmbedMode = EmbedMode.view,
        source_asset_id: str | None = None,
        width: str = DEFAULT_WIDTH,
        height: str = DEFAULT_HEIGHT,
    ) -> ExcalidrawEmbedBlock:
        state = ExcalidrawState(
            type=excalidraw_json.get("type", "excalidraw"),
            version=excalidraw_json.get("version", 2),
            elements=excalidraw_json.get("elements", []),
            app_state=excalidraw_json.get("appState", {}),
            files=excalidraw_json.get("files", {}),
        )
        return ExcalidrawEmbedBlock(
            excalidraw_state=state,
            mode=mode,
            width=width,
            height=height,
            source_asset_id=source_asset_id,
        )

    @staticmethod
    def to_block_props(block: ExcalidrawEmbedBlock) -> dict[str, Any]:
        """Serialise block to AFFiNE BlockSuite props format."""
        return {
            "excalidraw_state": block.excalidraw_state.model_dump(),
            "mode": block.mode.value,
            "width": block.width,
            "height": block.height,
            "source_asset_id": block.source_asset_id,
            "fallback_png_url": block.fallback_png_url,
        }


# ---------------------------------------------------------------------------
# Mode Enforcer
# ---------------------------------------------------------------------------


class ModeEnforcer:
    """Enforces edit / view mode constraints."""

    @staticmethod
    def is_toolbar_visible(mode: EmbedMode) -> bool:
        return mode == EmbedMode.edit

    @staticmethod
    def is_drawing_enabled(mode: EmbedMode) -> bool:
        return mode == EmbedMode.edit

    @staticmethod
    def validate_mode(mode: str) -> EmbedMode:
        if mode not in SUPPORTED_MODES:
            return EmbedMode.view
        return EmbedMode(mode)


# ---------------------------------------------------------------------------
# Injection Service
# ---------------------------------------------------------------------------


class ExcalidrawEmbedService:
    """Programmatic injection of Excalidraw embed blocks into AFFiNE pages."""

    def __init__(
        self,
        block_api: AFFiNEBlockAPIProtocol,
        fallback_renderer: FallbackRendererProtocol | None = None,
    ) -> None:
        self._api = block_api
        self._fallback = fallback_renderer
        self._builder = ExcalidrawBlockBuilder()

    async def inject(
        self,
        request: EmbedInjectionRequest,
    ) -> EmbedInjectionResult:
        block = self._builder.build(
            request.excalidraw_json,
            mode=request.mode,
            source_asset_id=request.source_asset_id,
        )

        # Generate fallback PNG if renderer available
        if self._fallback:
            try:
                png_url = await self._fallback.render_png(request.excalidraw_json)
                block.fallback_png_url = png_url
            except Exception:
                pass

        props = self._builder.to_block_props(block)

        try:
            block_id = await self._api.create_block(
                request.workspace_id,
                request.page_id,
                BLOCK_TYPE,
                props,
                request.position,
            )
        except Exception as exc:
            return EmbedInjectionResult(
                success=False,
                page_id=request.page_id,
                error=f"Block creation failed: {exc}",
            )

        return EmbedInjectionResult(
            success=True,
            block_id=block_id,
            page_id=request.page_id,
            fallback_used=block.fallback_png_url is not None,
        )

    async def inject_from_json(
        self,
        workspace_id: str,
        page_id: str,
        excalidraw_json: dict[str, Any],
        mode: str = "view",
        position: int = 0,
        source_asset_id: str | None = None,
    ) -> EmbedInjectionResult:
        """Convenience wrapper for simple injection calls."""
        req = EmbedInjectionRequest(
            workspace_id=workspace_id,
            page_id=page_id,
            excalidraw_json=excalidraw_json,
            mode=ModeEnforcer.validate_mode(mode),
            position=position,
            source_asset_id=source_asset_id,
        )
        return await self.inject(req)
