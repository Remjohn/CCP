"""FR-CA11-14 — Excalidraw Live OBS Annotation Overlay.

Injects an Excalidraw canvas as OBS browser source for live annotation
during recording sessions.  Transparent background ensures only drawn
elements appear over the video feed.
"""
from __future__ import annotations

from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    OBSOverlayPayload,
    OverlayActivationResult,
    OverlayStatus,
    OverlayTheme,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_OVERLAY_URL = "http://localhost:9876/overlay"
DEFAULT_SOURCE_NAME = "CCP_Overlay"
DEFAULT_RESOLUTION = "1920x1080"
TRANSPARENT_CSS = "body { background-color: rgba(0,0,0,0); }"
BLANK_URL = "about:blank"

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class OBSControllerProtocol(Protocol):
    async def set_browser_source(self, source_name: str, url: str) -> Any: ...


class OverlayServerProtocol(Protocol):
    async def health_check(self) -> bool: ...


# ---------------------------------------------------------------------------
# Overlay Configuration
# ---------------------------------------------------------------------------


class OverlayConfig:
    """Configuration for the Excalidraw overlay."""

    def __init__(
        self,
        url: str = DEFAULT_OVERLAY_URL,
        source_name: str = DEFAULT_SOURCE_NAME,
        resolution: str = DEFAULT_RESOLUTION,
        theme: OverlayTheme = OverlayTheme.dark,
        brand_colors: list[str] | None = None,
    ) -> None:
        self.url = url
        self.source_name = source_name
        self.resolution = resolution
        self.theme = theme
        self.brand_colors = brand_colors or ["#2E86AB", "#F18F01", "#FFFFFF"]

    def to_payload(self, status: OverlayStatus) -> OBSOverlayPayload:
        return OBSOverlayPayload(
            overlay_status=status,
            excalidraw_url=self.url,
            obs_source_name=self.source_name,
            resolution=self.resolution,
            theme=self.theme,
            brand_colors=self.brand_colors,
        )


# ---------------------------------------------------------------------------
# Overlay Manager
# ---------------------------------------------------------------------------


class ExcalidrawOverlayManager:
    """Manages the Excalidraw overlay in OBS via browser source."""

    def __init__(
        self,
        obs_controller: OBSControllerProtocol | None = None,
        overlay_server: OverlayServerProtocol | None = None,
        config: OverlayConfig | None = None,
    ) -> None:
        self._obs = obs_controller
        self._server = overlay_server
        self._config = config or OverlayConfig()
        self._status = OverlayStatus.inactive

    @property
    def status(self) -> OverlayStatus:
        return self._status

    @property
    def config(self) -> OverlayConfig:
        return self._config

    async def activate(self) -> OverlayActivationResult:
        """AC1 — Activate the Excalidraw overlay in OBS."""
        # Check if overlay server is reachable
        if self._server:
            try:
                healthy = await self._server.health_check()
                if not healthy:
                    return OverlayActivationResult(
                        success=False,
                        error="Overlay server not running. Recording continues without overlay.",
                    )
            except Exception:
                return OverlayActivationResult(
                    success=False,
                    error="Overlay server not running. Recording continues without overlay.",
                )

        if not self._obs:
            return OverlayActivationResult(
                success=False,
                error="OBS controller not available",
            )

        try:
            result = await self._obs.set_browser_source(
                self._config.source_name, self._config.url,
            )
            # Check if the OBS command succeeded
            if hasattr(result, "success") and not result.success:
                return OverlayActivationResult(
                    success=False,
                    error="Failed to set OBS browser source",
                )
            self._status = OverlayStatus.active
            return OverlayActivationResult(
                success=True,
                overlay_status=OverlayStatus.active,
                message="Excalidraw overlay activated 🎨",
            )
        except Exception as exc:
            return OverlayActivationResult(
                success=False,
                error=f"Overlay activation failed: {exc}",
            )

    async def deactivate(self) -> OverlayActivationResult:
        """AC4 — Deactivate the overlay."""
        if not self._obs:
            return OverlayActivationResult(
                success=False, error="OBS controller not available")

        try:
            await self._obs.set_browser_source(self._config.source_name, BLANK_URL)
            self._status = OverlayStatus.inactive
            return OverlayActivationResult(
                success=True,
                overlay_status=OverlayStatus.inactive,
                message="Overlay deactivated",
            )
        except Exception as exc:
            return OverlayActivationResult(
                success=False,
                error=f"Overlay deactivation failed: {exc}",
            )

    def get_payload(self) -> OBSOverlayPayload:
        return self._config.to_payload(self._status)


# ---------------------------------------------------------------------------
# Telegram Command Handler
# ---------------------------------------------------------------------------


class OverlayTelegramHandler:
    """Handles /overlay on and /overlay off commands."""

    def __init__(self, manager: ExcalidrawOverlayManager) -> None:
        self._manager = manager

    async def handle(self, args: str) -> OverlayActivationResult:
        arg = args.strip().lower()
        if arg == "on":
            return await self._manager.activate()
        elif arg == "off":
            return await self._manager.deactivate()
        return OverlayActivationResult(
            success=False,
            error="Usage: /overlay on | /overlay off",
        )
