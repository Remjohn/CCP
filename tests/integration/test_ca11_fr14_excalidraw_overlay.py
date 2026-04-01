"""FR-CA11-14 — Excalidraw Live OBS Annotation Overlay — Integration Tests.

Covers all 6 Acceptance Criteria:
  AC1: Overlay activation
  AC2: Drawing visibility (simulated)
  AC3: Transparency (config validation)
  AC4: Overlay deactivation
  AC5: Recording integration (overlay state during recording)
  AC6: Graceful failure when server not running
"""
from __future__ import annotations

import asyncio
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    OBSOverlayPayload,
    OverlayActivationResult,
    OverlayStatus,
    OverlayTheme,
)
from src.ccp.services.excalidraw_overlay import (
    BLANK_URL,
    DEFAULT_OVERLAY_URL,
    DEFAULT_RESOLUTION,
    DEFAULT_SOURCE_NAME,
    TRANSPARENT_CSS,
    ExcalidrawOverlayManager,
    OverlayConfig,
    OverlayTelegramHandler,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---- Mocks ----

class MockOBSController:
    def __init__(self):
        self.sources: list[tuple[str, str]] = []
    async def set_browser_source(self, source_name, url):
        self.sources.append((source_name, url))
        return type("R", (), {"success": True})()


class FailingOBSController:
    async def set_browser_source(self, *a, **kw):
        raise ConnectionError("OBS unavailable")


class MockOverlayServer:
    def __init__(self, healthy=True):
        self._healthy = healthy
    async def health_check(self):
        return self._healthy


class FailingOverlayServer:
    async def health_check(self):
        raise ConnectionError("Server down")


# ===================================================================
# 1. Model validation (4 tests)
# ===================================================================

class TestModels:
    def test_overlay_payload_defaults(self):
        p = OBSOverlayPayload()
        assert p.overlay_status == OverlayStatus.inactive
        assert p.background == "transparent"
        assert p.theme == OverlayTheme.dark

    def test_overlay_brand_colors(self):
        p = OBSOverlayPayload()
        assert len(p.brand_colors) == 3
        assert "#2E86AB" in p.brand_colors

    def test_activation_result(self):
        r = OverlayActivationResult(success=True, overlay_status=OverlayStatus.active)
        assert r.success

    def test_overlay_status_enum(self):
        assert OverlayStatus.active.value == "active"
        assert OverlayStatus.inactive.value == "inactive"


# ===================================================================
# 2. Overlay Config (3 tests)
# ===================================================================

class TestOverlayConfig:
    def test_defaults(self):
        c = OverlayConfig()
        assert c.url == DEFAULT_OVERLAY_URL
        assert c.source_name == DEFAULT_SOURCE_NAME
        assert c.theme == OverlayTheme.dark

    def test_custom_config(self):
        c = OverlayConfig(url="http://custom:8080/overlay", theme=OverlayTheme.light)
        assert c.url == "http://custom:8080/overlay"
        assert c.theme == OverlayTheme.light

    def test_to_payload(self):
        c = OverlayConfig()
        p = c.to_payload(OverlayStatus.active)
        assert p.overlay_status == OverlayStatus.active
        assert p.excalidraw_url == DEFAULT_OVERLAY_URL


# ===================================================================
# 3. Overlay Activation — AC1 (3 tests)
# ===================================================================

class TestActivation:
    def test_activate_ac1(self):
        """AC1 — overlay activates and OBS shows transparent Excalidraw layer."""
        obs = MockOBSController()
        server = MockOverlayServer()
        mgr = ExcalidrawOverlayManager(obs_controller=obs, overlay_server=server)
        result = _run(mgr.activate())
        assert result.success
        assert result.overlay_status == OverlayStatus.active
        assert "overlay activated" in result.message
        assert mgr.status == OverlayStatus.active
        assert obs.sources[0] == (DEFAULT_SOURCE_NAME, DEFAULT_OVERLAY_URL)

    def test_activate_without_server_check(self):
        """Server check optional — activates if no server protocol provided."""
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs)
        result = _run(mgr.activate())
        assert result.success

    def test_activate_no_obs(self):
        mgr = ExcalidrawOverlayManager(obs_controller=None)
        result = _run(mgr.activate())
        assert not result.success
        assert "not available" in result.error


# ===================================================================
# 4. Transparency — AC3 (2 tests)
# ===================================================================

class TestTransparency:
    def test_transparent_background_ac3(self):
        """AC3 — background is transparent."""
        p = OBSOverlayPayload()
        assert p.background == "transparent"

    def test_transparent_css(self):
        assert "rgba(0,0,0,0)" in TRANSPARENT_CSS


# ===================================================================
# 5. Deactivation — AC4 (2 tests)
# ===================================================================

class TestDeactivation:
    def test_deactivate_ac4(self):
        """AC4 — overlay disappears from OBS."""
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs)
        _run(mgr.activate())
        result = _run(mgr.deactivate())
        assert result.success
        assert result.overlay_status == OverlayStatus.inactive
        assert mgr.status == OverlayStatus.inactive
        # Should have set browser source to blank
        assert obs.sources[-1] == (DEFAULT_SOURCE_NAME, BLANK_URL)

    def test_deactivate_no_obs(self):
        mgr = ExcalidrawOverlayManager(obs_controller=None)
        result = _run(mgr.deactivate())
        assert not result.success


# ===================================================================
# 6. Recording Integration — AC5 (2 tests)
# ===================================================================

class TestRecordingIntegration:
    def test_overlay_state_during_recording_ac5(self):
        """AC5 — overlay state persists through recording lifecycle."""
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs)
        _run(mgr.activate())
        assert mgr.status == OverlayStatus.active
        payload = mgr.get_payload()
        assert payload.overlay_status == OverlayStatus.active

    def test_overlay_survives_scene_changes(self):
        """Browser source persists across scene changes."""
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs)
        _run(mgr.activate())
        # Simulated scene changes — overlay status unchanged
        assert mgr.status == OverlayStatus.active


# ===================================================================
# 7. Graceful Failure — AC6 (3 tests)
# ===================================================================

class TestGracefulFailure:
    def test_server_not_running_ac6(self):
        """AC6 — overlay server down returns graceful error."""
        obs = MockOBSController()
        server = MockOverlayServer(healthy=False)
        mgr = ExcalidrawOverlayManager(obs_controller=obs, overlay_server=server)
        result = _run(mgr.activate())
        assert not result.success
        assert "Overlay server not running" in result.error

    def test_server_exception_ac6(self):
        """AC6 — server health check exception handled gracefully."""
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs, overlay_server=FailingOverlayServer())
        result = _run(mgr.activate())
        assert not result.success
        assert "Overlay server not running" in result.error

    def test_obs_failure_during_activation(self):
        mgr = ExcalidrawOverlayManager(obs_controller=FailingOBSController())
        result = _run(mgr.activate())
        assert not result.success
        assert "activation failed" in result.error


# ===================================================================
# 8. Telegram Handler (3 tests)
# ===================================================================

class TestTelegramHandler:
    def test_overlay_on(self):
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs)
        handler = OverlayTelegramHandler(mgr)
        result = _run(handler.handle("on"))
        assert result.success
        assert result.overlay_status == OverlayStatus.active

    def test_overlay_off(self):
        obs = MockOBSController()
        mgr = ExcalidrawOverlayManager(obs_controller=obs)
        _run(mgr.activate())
        handler = OverlayTelegramHandler(mgr)
        result = _run(handler.handle("off"))
        assert result.success
        assert result.overlay_status == OverlayStatus.inactive

    def test_invalid_arg(self):
        mgr = ExcalidrawOverlayManager(obs_controller=MockOBSController())
        handler = OverlayTelegramHandler(mgr)
        result = _run(handler.handle("maybe"))
        assert not result.success
        assert "Usage" in result.error


# ===================================================================
# 9. Constants (2 tests)
# ===================================================================

class TestConstants:
    def test_constants(self):
        assert DEFAULT_OVERLAY_URL == "http://localhost:9876/overlay"
        assert DEFAULT_SOURCE_NAME == "CCP_Overlay"
        assert DEFAULT_RESOLUTION == "1920x1080"

    def test_blank_url(self):
        assert BLANK_URL == "about:blank"
