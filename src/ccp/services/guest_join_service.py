"""FR-CA11-21 — Studio Guest Join (WebRTC Multi-Party).

DEP-ENG-117: WebRTC Signaling Endpoint
DEP-ENG-118: Guest Join Page
DEP-ENG-119: Canvas Compositing (Guest)
DEP-ENG-120: Guest Audio Merge
DEP-ENG-121: Invite Link Generator

Agent: Diego (Studio Guest Join Operator)
"""
from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    DEFAULT_ICE_SERVERS,
    GUEST_JOIN_AGENT_NAME,
    INVITE_TOKEN_LENGTH,
    PIP_SIZE_DEFAULT,
    PIP_SIZE_MAX,
    PIP_SIZE_MIN,
    TOKEN_EXPIRY_MINUTES,
    GuestAudioConfig,
    GuestCanvasRect,
    GuestInvite,
    GuestJoinError,
    GuestJoinResult,
    GuestLayoutConfig,
    GuestLayoutMode,
    GuestSessionRecord,
    GuestSessionStatus,
)

# ---------------------------------------------------------------------------
# SQL (§5 Data Model)
# ---------------------------------------------------------------------------

GUEST_SESSIONS_SQL = """
CREATE TABLE IF NOT EXISTS studio_guest_sessions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id          UUID NOT NULL REFERENCES studio_sessions(id),
    guest_name          VARCHAR(255) NOT NULL,
    join_token          VARCHAR(64) NOT NULL UNIQUE,
    token_expires_at    TIMESTAMPTZ NOT NULL,
    layout_mode         VARCHAR(20) DEFAULT 'pip',
    status              VARCHAR(20) DEFAULT 'pending',
    connected_at        TIMESTAMPTZ,
    disconnected_at     TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_guest_sessions_token ON studio_guest_sessions(join_token);
CREATE INDEX IF NOT EXISTS idx_guest_sessions_session ON studio_guest_sessions(session_id);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class GuestDatabaseProtocol(Protocol):
    async def insert_guest_session(self, record: dict[str, Any]) -> str: ...
    async def get_guest_by_token(self, token: str) -> Optional[dict[str, Any]]: ...
    async def update_guest_session(self, record_id: str, updates: dict[str, Any]) -> None: ...


# ---------------------------------------------------------------------------
# Receipt utilities (FR47 DEP-ENG-041)
# ---------------------------------------------------------------------------


def _sha256(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _build_receipt(
    stage_name: str, agent_name: str,
    input_payload: Any, output_payload: Any,
    previous_receipt_hash: str = "",
) -> dict[str, Any]:
    return {
        "receipt_id": str(uuid.uuid4()),
        "previous_receipt_hash": previous_receipt_hash,
        "input_payload_hash": _sha256(input_payload),
        "output_payload_hash": _sha256(output_payload),
        "stage_name": stage_name,
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Pure functions
# ---------------------------------------------------------------------------


def generate_invite_token() -> str:
    """§4 Stage 2 Step 1: Generate 64-char hex token. AC1: unique, 30-min expiry."""
    return secrets.token_hex(INVITE_TOKEN_LENGTH // 2)


def create_guest_invite(
    session_id: str,
    coach_name: str = "",
    base_url: str = "https://studio.consciouselite.com/join",
) -> GuestInvite:
    """§4 Stage 2 Step 1: POST /studio/guest-invite."""
    token = generate_invite_token()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    invite_url = f"{base_url}/{token}"

    return GuestInvite(
        session_id=session_id,
        coach_name=coach_name,
        token=token,
        invite_url=invite_url,
        expires_at=expires_at,
        created_at=now,
    )


def validate_token(invite: GuestInvite, now: Optional[datetime] = None) -> Optional[str]:
    """Check if token is still valid. Returns error string or None."""
    current = now or datetime.now(timezone.utc)
    expires = invite.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if current > expires:
        return GuestJoinError.TOKEN_EXPIRED.value
    return None


def compute_pip_rect(
    canvas_width: float,
    canvas_height: float,
    pip_size: float = PIP_SIZE_DEFAULT,
) -> GuestCanvasRect:
    """§4 Stage 3 Step 3: PiP layout — guest 25% in bottom-right corner.

    AC3: Guest renders as pip_size fraction of canvas in bottom-right.
    """
    clamped = max(PIP_SIZE_MIN, min(PIP_SIZE_MAX, pip_size))
    guest_w = canvas_width * clamped
    guest_h = canvas_height * clamped
    x = canvas_width - guest_w
    y = canvas_height - guest_h
    return GuestCanvasRect(x=x, y=y, width=guest_w, height=guest_h)


def compute_side_by_side_rects(
    canvas_width: float,
    canvas_height: float,
) -> tuple[GuestCanvasRect, GuestCanvasRect]:
    """§4 Stage 3 Step 4: Side-by-side — 50/50 split.

    AC4: Coach left, guest right.
    Returns (coach_rect, guest_rect).
    """
    half_w = canvas_width / 2.0
    coach = GuestCanvasRect(x=0, y=0, width=half_w, height=canvas_height)
    guest = GuestCanvasRect(x=half_w, y=0, width=half_w, height=canvas_height)
    return coach, guest


def compute_guest_rect(
    canvas_width: float,
    canvas_height: float,
    layout_mode: str = GuestLayoutMode.PIP.value,
    pip_size: float = PIP_SIZE_DEFAULT,
) -> GuestCanvasRect:
    """Unified rect computation based on layout mode."""
    if layout_mode == GuestLayoutMode.SIDE_BY_SIDE.value:
        _, guest = compute_side_by_side_rects(canvas_width, canvas_height)
        return guest
    return compute_pip_rect(canvas_width, canvas_height, pip_size)


def mute_guest_audio(config: GuestAudioConfig) -> GuestAudioConfig:
    """AC6: Mute guest — gain → 0, muted flag."""
    return GuestAudioConfig(gain=0.0, muted=True)


def unmute_guest_audio(
    config: GuestAudioConfig, restore_gain: float = 1.0,
) -> GuestAudioConfig:
    """Unmute guest — restore gain."""
    return GuestAudioConfig(gain=restore_gain, muted=False)


# ---------------------------------------------------------------------------
# Guest Join Service
# ---------------------------------------------------------------------------


class GuestJoinService:
    """FR-CA11-21 — Studio Guest Join.

    Stateless invite/layout logic + receipt chain.
    """

    def __init__(self, db: GuestDatabaseProtocol | None = None) -> None:
        self._db = db
        self._receipt_chain: list[dict[str, Any]] = []

    @property
    def receipt_chain(self) -> list[dict[str, Any]]:
        return list(self._receipt_chain)

    def _emit_receipt(
        self, stage_name: str, input_payload: Any, output_payload: Any,
    ) -> dict[str, Any]:
        prev_hash = ""
        if self._receipt_chain:
            prev_hash = _sha256(self._receipt_chain[-1])
        receipt = _build_receipt(
            stage_name=stage_name,
            agent_name=GUEST_JOIN_AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Stage 2: Invite Link --

    def create_invite(
        self, session_id: str, coach_name: str = "",
    ) -> GuestJoinResult:
        """AC1: Generate invite link with unique token and 30-min expiry."""
        invite = create_guest_invite(session_id, coach_name)

        self._emit_receipt(
            stage_name="guest-invite",
            input_payload={"session_id": session_id},
            output_payload={"token": invite.token, "expires_at": invite.expires_at.isoformat()},
        )

        return GuestJoinResult(success=True, invite=invite)

    # -- Token validation --

    def validate_invite(self, invite: GuestInvite) -> GuestJoinResult:
        """AC8: Validate token hasn't expired."""
        error = validate_token(invite)
        if error:
            return GuestJoinResult(success=False, error=error)
        return GuestJoinResult(success=True, invite=invite)

    # -- Guest connection --

    def connect_guest(
        self, invite: GuestInvite, guest_name: str,
    ) -> GuestJoinResult:
        """AC2: Guest connects via token → session record created."""
        error = validate_token(invite)
        if error:
            return GuestJoinResult(success=False, error=error)

        now = datetime.now(timezone.utc)
        session = GuestSessionRecord(
            session_id=invite.session_id,
            guest_name=guest_name,
            join_token=invite.token,
            token_expires_at=invite.expires_at,
            status=GuestSessionStatus.CONNECTED.value,
            connected_at=now,
        )

        layout = GuestLayoutConfig(
            layout_mode=GuestLayoutMode.PIP.value,
            pip_size=PIP_SIZE_DEFAULT,
        )

        self._emit_receipt(
            stage_name="guest-connect",
            input_payload={"token": invite.token, "guest_name": guest_name},
            output_payload={"session_id": session.session_id, "status": session.status},
        )

        return GuestJoinResult(success=True, session=session, layout=layout)

    # -- Disconnect --

    def disconnect_guest(
        self, session: GuestSessionRecord,
    ) -> GuestJoinResult:
        """AC7: Disconnect guest — close WebRTC, remove from canvas."""
        data = session.model_dump()
        data["status"] = GuestSessionStatus.DISCONNECTED.value
        data["disconnected_at"] = datetime.now(timezone.utc)
        updated = GuestSessionRecord(**data)

        self._emit_receipt(
            stage_name="guest-disconnect",
            input_payload={"record_id": session.record_id},
            output_payload={"status": updated.status},
        )

        return GuestJoinResult(success=True, session=updated)

    # -- Layout switch --

    def switch_layout(
        self,
        current: GuestLayoutConfig,
        canvas_width: float,
        canvas_height: float,
    ) -> GuestLayoutConfig:
        """AC3/AC4: Toggle PiP ↔ Side-by-Side."""
        new_mode = (
            GuestLayoutMode.SIDE_BY_SIDE.value
            if current.layout_mode == GuestLayoutMode.PIP.value
            else GuestLayoutMode.PIP.value
        )
        guest_rect = compute_guest_rect(canvas_width, canvas_height, new_mode, current.pip_size)
        return GuestLayoutConfig(
            layout_mode=new_mode,
            pip_size=current.pip_size,
            guest_rect=guest_rect,
        )

    # -- Receipt chain verification --

    def verify_receipt_chain(self) -> bool:
        if not self._receipt_chain:
            return True
        if self._receipt_chain[0]["previous_receipt_hash"] != "":
            return False
        for i in range(1, len(self._receipt_chain)):
            expected = _sha256(self._receipt_chain[i - 1])
            if self._receipt_chain[i]["previous_receipt_hash"] != expected:
                return False
        return True
