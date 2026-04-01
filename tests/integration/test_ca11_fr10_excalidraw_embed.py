"""FR-CA11-10 — Excalidraw Embedded Workspace — Integration Tests.

Covers all 6 Acceptance Criteria:
  AC1: Block registration (correct initial state)
  AC2: Edit mode (toolbar + drawing enabled)
  AC3: View mode (toolbar hidden, drawing disabled)
  AC4: CRDT sync (state persistence via YJS — simulated)
  AC5: Programmatic injection via API
  AC6: Fallback PNG on failure
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    EmbedInjectionRequest,
    EmbedInjectionResult,
    EmbedMode,
    ExcalidrawEmbedBlock,
    ExcalidrawState,
)
from src.ccp.services.excalidraw_embed_service import (
    BLOCK_TYPE,
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    EMBED_BLOCKS_SQL,
    SUPPORTED_MODES,
    ExcalidrawBlockBuilder,
    ExcalidrawEmbedService,
    ModeEnforcer,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WORKSPACE_ID = "ws-001"
PAGE_ID = "page-001"

SAMPLE_EXCALIDRAW = {
    "type": "excalidraw",
    "version": 2,
    "elements": [
        {"type": "rectangle", "id": "r1", "x": 10, "y": 10, "width": 100, "height": 50},
        {"type": "text", "id": "t1", "x": 20, "y": 20, "text": "Hello"},
    ],
    "appState": {"zoom": {"value": 1}},
    "files": {},
}


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---- Mocks ----

class MockBlockAPI:
    def __init__(self):
        self.blocks: list[dict] = []
    async def create_block(self, workspace_id, page_id, block_type, props, position):
        block_id = f"block-{uuid.uuid4().hex[:8]}"
        self.blocks.append({
            "workspace_id": workspace_id, "page_id": page_id,
            "block_type": block_type, "props": props, "position": position,
            "block_id": block_id,
        })
        return block_id


class FailingBlockAPI:
    async def create_block(self, *a, **kw):
        raise ConnectionError("AFFiNE unavailable")


class MockFallbackRenderer:
    def __init__(self):
        self.rendered = False
    async def render_png(self, excalidraw_json):
        self.rendered = True
        return f"s3://fallback/png-{uuid.uuid4().hex[:6]}.png"


# ===================================================================
# 1. Model validation (6 tests)
# ===================================================================

class TestModels:
    def test_excalidraw_state_defaults(self):
        s = ExcalidrawState()
        assert s.type == "excalidraw"
        assert s.version == 2
        assert s.elements == []

    def test_embed_block_defaults(self):
        b = ExcalidrawEmbedBlock()
        assert b.block_type == "excalidraw-embed"
        assert b.mode == EmbedMode.view
        assert b.width == "100%"
        assert b.height == "600px"

    def test_embed_mode_enum(self):
        assert EmbedMode.view.value == "view"
        assert EmbedMode.edit.value == "edit"

    def test_injection_request(self):
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW,
        )
        assert req.mode == EmbedMode.view
        assert req.position == 0

    def test_injection_result(self):
        r = EmbedInjectionResult(success=True, block_id="b1", page_id="p1")
        assert r.success
        assert not r.fallback_used

    def test_block_id_generated(self):
        b = ExcalidrawEmbedBlock()
        assert b.block_id.startswith("block-")


# ===================================================================
# 2. Block builder — AC1 (4 tests)
# ===================================================================

class TestBlockBuilder:
    def test_builds_from_json_ac1(self):
        """AC1 — block renders with correct initial state."""
        builder = ExcalidrawBlockBuilder()
        block = builder.build(SAMPLE_EXCALIDRAW)
        assert len(block.excalidraw_state.elements) == 2
        assert block.excalidraw_state.version == 2

    def test_mode_applied(self):
        builder = ExcalidrawBlockBuilder()
        block = builder.build(SAMPLE_EXCALIDRAW, mode=EmbedMode.edit)
        assert block.mode == EmbedMode.edit

    def test_source_asset_id(self):
        builder = ExcalidrawBlockBuilder()
        block = builder.build(SAMPLE_EXCALIDRAW, source_asset_id="JP-001")
        assert block.source_asset_id == "JP-001"

    def test_to_block_props(self):
        builder = ExcalidrawBlockBuilder()
        block = builder.build(SAMPLE_EXCALIDRAW)
        props = builder.to_block_props(block)
        assert props["mode"] == "view"
        assert "excalidraw_state" in props


# ===================================================================
# 3. Mode enforcer — AC2 + AC3 (5 tests)
# ===================================================================

class TestModeEnforcer:
    def test_edit_mode_toolbar_visible_ac2(self):
        """AC2 — edit mode shows toolbar."""
        assert ModeEnforcer.is_toolbar_visible(EmbedMode.edit)

    def test_edit_mode_drawing_enabled_ac2(self):
        """AC2 — edit mode enables drawing."""
        assert ModeEnforcer.is_drawing_enabled(EmbedMode.edit)

    def test_view_mode_toolbar_hidden_ac3(self):
        """AC3 — view mode hides toolbar."""
        assert not ModeEnforcer.is_toolbar_visible(EmbedMode.view)

    def test_view_mode_drawing_disabled_ac3(self):
        """AC3 — view mode disables drawing."""
        assert not ModeEnforcer.is_drawing_enabled(EmbedMode.view)

    def test_validate_invalid_mode(self):
        assert ModeEnforcer.validate_mode("bogus") == EmbedMode.view


# ===================================================================
# 4. CRDT sync — AC4 (simulated, 2 tests)
# ===================================================================

class TestCRDTSync:
    def test_state_roundtrip_ac4(self):
        """AC4 — state persists through serialisation."""
        builder = ExcalidrawBlockBuilder()
        block = builder.build(SAMPLE_EXCALIDRAW, mode=EmbedMode.edit)
        props = builder.to_block_props(block)
        # Simulate YJS restore
        restored = ExcalidrawState(**props["excalidraw_state"])
        assert len(restored.elements) == 2
        assert restored.elements[0]["type"] == "rectangle"

    def test_elements_preserved_after_edit(self):
        """AC4 — edited elements appear in state."""
        builder = ExcalidrawBlockBuilder()
        block = builder.build(SAMPLE_EXCALIDRAW, mode=EmbedMode.edit)
        # Simulate user adding a shape
        block.excalidraw_state.elements.append(
            {"type": "ellipse", "id": "e1", "x": 50, "y": 50}
        )
        assert len(block.excalidraw_state.elements) == 3


# ===================================================================
# 5. Programmatic injection — AC5 (4 tests)
# ===================================================================

class TestInjection:
    def test_inject_success_ac5(self):
        """AC5 — inject block via API."""
        api = MockBlockAPI()
        svc = ExcalidrawEmbedService(api)
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW,
        )
        result = _run(svc.inject(req))
        assert result.success
        assert result.block_id is not None
        assert result.page_id == PAGE_ID
        assert len(api.blocks) == 1
        assert api.blocks[0]["block_type"] == BLOCK_TYPE

    def test_inject_from_json_convenience(self):
        api = MockBlockAPI()
        svc = ExcalidrawEmbedService(api)
        result = _run(svc.inject_from_json(
            WORKSPACE_ID, PAGE_ID, SAMPLE_EXCALIDRAW,
            mode="edit", source_asset_id="JP-001",
        ))
        assert result.success
        assert api.blocks[0]["props"]["mode"] == "edit"

    def test_position_respected(self):
        api = MockBlockAPI()
        svc = ExcalidrawEmbedService(api)
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW, position=5,
        )
        _run(svc.inject(req))
        assert api.blocks[0]["position"] == 5

    def test_api_failure(self):
        svc = ExcalidrawEmbedService(FailingBlockAPI())
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW,
        )
        result = _run(svc.inject(req))
        assert not result.success
        assert "Block creation failed" in result.error


# ===================================================================
# 6. Fallback — AC6 (3 tests)
# ===================================================================

class TestFallback:
    def test_fallback_png_generated_ac6(self):
        """AC6 — fallback PNG is generated when renderer available."""
        api = MockBlockAPI()
        renderer = MockFallbackRenderer()
        svc = ExcalidrawEmbedService(api, fallback_renderer=renderer)
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW,
        )
        result = _run(svc.inject(req))
        assert result.success
        assert result.fallback_used
        assert renderer.rendered

    def test_no_fallback_renderer(self):
        api = MockBlockAPI()
        svc = ExcalidrawEmbedService(api, fallback_renderer=None)
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW,
        )
        result = _run(svc.inject(req))
        assert result.success
        assert not result.fallback_used

    def test_fallback_props_in_block(self):
        api = MockBlockAPI()
        renderer = MockFallbackRenderer()
        svc = ExcalidrawEmbedService(api, fallback_renderer=renderer)
        req = EmbedInjectionRequest(
            workspace_id=WORKSPACE_ID, page_id=PAGE_ID,
            excalidraw_json=SAMPLE_EXCALIDRAW,
        )
        _run(svc.inject(req))
        props = api.blocks[0]["props"]
        assert props["fallback_png_url"] is not None


# ===================================================================
# 7. Constants & SQL (2 tests)
# ===================================================================

class TestConstants:
    def test_block_type(self):
        assert BLOCK_TYPE == "excalidraw-embed"
        assert SUPPORTED_MODES == {"view", "edit"}

    def test_sql_schema(self):
        assert "excalidraw_embed_blocks" in EMBED_BLOCKS_SQL
        assert "block_id" in EMBED_BLOCKS_SQL
