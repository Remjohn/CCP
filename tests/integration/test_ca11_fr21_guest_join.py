"""FR-CA11-21 — Studio Guest Join (WebRTC Multi-Party) — Integration Tests.

Target: 10 ACs + token logic + layout computation + receipt chain + SQL + constants.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

import pytest

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
from src.ccp.services.guest_join_service import (
    GUEST_SESSIONS_SQL,
    GuestJoinService,
    compute_guest_rect,
    compute_pip_rect,
    compute_side_by_side_rects,
    create_guest_invite,
    generate_invite_token,
    mute_guest_audio,
    unmute_guest_audio,
    validate_token,
)


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ═══════════════════════════════════════════════════════════════════════
# AC1: Invite Link (Token Generation)
# ═══════════════════════════════════════════════════════════════════════


class TestInviteLink:
    """AC1: Generate invite link — unique token, 30-min expiry."""

    def test_token_length(self):
        token = generate_invite_token()
        assert len(token) == INVITE_TOKEN_LENGTH

    def test_token_uniqueness(self):
        tokens = {generate_invite_token() for _ in range(100)}
        assert len(tokens) == 100

    def test_invite_has_url(self):
        invite = create_guest_invite("session-1", "Coach Amy")
        assert invite.invite_url.endswith(invite.token)

    def test_invite_expires_in_30_min(self):
        invite = create_guest_invite("session-1")
        delta = invite.expires_at - invite.created_at
        assert abs(delta.total_seconds() - TOKEN_EXPIRY_MINUTES * 60) < 2

    def test_invite_via_service(self):
        svc = GuestJoinService()
        result = svc.create_invite("session-1", "Coach Amy")
        assert result.success is True
        assert result.invite is not None
        assert len(result.invite.token) == INVITE_TOKEN_LENGTH

    def test_invite_emits_receipt(self):
        svc = GuestJoinService()
        svc.create_invite("session-1")
        assert len(svc.receipt_chain) == 1
        assert svc.receipt_chain[0]["stage_name"] == "guest-invite"


# ═══════════════════════════════════════════════════════════════════════
# AC2: Guest Connect
# ═══════════════════════════════════════════════════════════════════════


class TestGuestConnect:
    """AC2: Guest opens link → connects → session created."""

    def test_connect_creates_session(self):
        svc = GuestJoinService()
        invite_result = svc.create_invite("session-1")
        invite = invite_result.invite
        result = svc.connect_guest(invite, "Guest Bob")
        assert result.success is True
        assert result.session is not None
        assert result.session.status == GuestSessionStatus.CONNECTED.value
        assert result.session.guest_name == "Guest Bob"

    def test_connect_sets_layout(self):
        svc = GuestJoinService()
        invite = svc.create_invite("session-1").invite
        result = svc.connect_guest(invite, "Guest Bob")
        assert result.layout is not None
        assert result.layout.layout_mode == GuestLayoutMode.PIP.value

    def test_connect_emits_receipt(self):
        svc = GuestJoinService()
        invite = svc.create_invite("session-1").invite
        svc.connect_guest(invite, "Guest Bob")
        assert len(svc.receipt_chain) == 2  # invite + connect


# ═══════════════════════════════════════════════════════════════════════
# AC3: PiP Layout
# ═══════════════════════════════════════════════════════════════════════


class TestPiPLayout:
    """AC3: Guest video renders as 25% overlay in bottom-right."""

    def test_pip_default_25pct(self):
        rect = compute_pip_rect(1920, 1080)
        assert rect.width == pytest.approx(1920 * PIP_SIZE_DEFAULT, abs=1)
        assert rect.height == pytest.approx(1080 * PIP_SIZE_DEFAULT, abs=1)

    def test_pip_bottom_right(self):
        rect = compute_pip_rect(1920, 1080)
        assert rect.x == pytest.approx(1920 - rect.width, abs=1)
        assert rect.y == pytest.approx(1080 - rect.height, abs=1)

    def test_pip_custom_size(self):
        rect = compute_pip_rect(1920, 1080, pip_size=0.30)
        assert rect.width == pytest.approx(1920 * 0.30, abs=1)

    def test_pip_clamped_min(self):
        rect = compute_pip_rect(1920, 1080, pip_size=0.05)
        assert rect.width == pytest.approx(1920 * PIP_SIZE_MIN, abs=1)

    def test_pip_clamped_max(self):
        rect = compute_pip_rect(1920, 1080, pip_size=0.50)
        assert rect.width == pytest.approx(1920 * PIP_SIZE_MAX, abs=1)

    def test_pip_9_16_canvas(self):
        rect = compute_pip_rect(1080, 1920)
        assert rect.width == pytest.approx(1080 * PIP_SIZE_DEFAULT, abs=1)
        assert rect.height == pytest.approx(1920 * PIP_SIZE_DEFAULT, abs=1)


# ═══════════════════════════════════════════════════════════════════════
# AC4: Side-by-Side Layout
# ═══════════════════════════════════════════════════════════════════════


class TestSideBySideLayout:
    """AC4: 50/50 split — coach left, guest right."""

    def test_side_by_side_50_50(self):
        coach, guest = compute_side_by_side_rects(1920, 1080)
        assert coach.width == pytest.approx(960, abs=1)
        assert guest.width == pytest.approx(960, abs=1)

    def test_coach_left_guest_right(self):
        coach, guest = compute_side_by_side_rects(1920, 1080)
        assert coach.x == 0
        assert guest.x == pytest.approx(960, abs=1)

    def test_full_height(self):
        coach, guest = compute_side_by_side_rects(1920, 1080)
        assert coach.height == 1080
        assert guest.height == 1080


# ═══════════════════════════════════════════════════════════════════════
# AC5: Audio Merge (model-level)
# ═══════════════════════════════════════════════════════════════════════


class TestAudioMerge:
    """AC5: Guest audio present in recording output."""

    def test_default_audio_config(self):
        config = GuestAudioConfig()
        assert config.gain == 1.0
        assert config.muted is False

    def test_audio_gain_range(self):
        config = GuestAudioConfig(gain=0.5)
        assert config.gain == 0.5


# ═══════════════════════════════════════════════════════════════════════
# AC6: Mute Guest
# ═══════════════════════════════════════════════════════════════════════


class TestMuteGuest:
    """AC6: Mute silences audio, video stays visible."""

    def test_mute_sets_zero_gain(self):
        config = GuestAudioConfig(gain=1.0)
        muted = mute_guest_audio(config)
        assert muted.gain == 0.0
        assert muted.muted is True

    def test_unmute_restores_gain(self):
        muted = GuestAudioConfig(gain=0.0, muted=True)
        restored = unmute_guest_audio(muted, restore_gain=0.8)
        assert restored.gain == 0.8
        assert restored.muted is False


# ═══════════════════════════════════════════════════════════════════════
# AC7: Disconnect Guest
# ═══════════════════════════════════════════════════════════════════════


class TestDisconnectGuest:
    """AC7: Disconnect closes WebRTC, removes guest from canvas."""

    def test_disconnect_updates_status(self):
        svc = GuestJoinService()
        invite = svc.create_invite("session-1").invite
        conn = svc.connect_guest(invite, "Guest Bob")
        result = svc.disconnect_guest(conn.session)
        assert result.session.status == GuestSessionStatus.DISCONNECTED.value
        assert result.session.disconnected_at is not None

    def test_disconnect_emits_receipt(self):
        svc = GuestJoinService()
        invite = svc.create_invite("session-1").invite
        conn = svc.connect_guest(invite, "Guest Bob")
        svc.disconnect_guest(conn.session)
        assert len(svc.receipt_chain) == 3  # invite + connect + disconnect


# ═══════════════════════════════════════════════════════════════════════
# AC8: Token Expiry
# ═══════════════════════════════════════════════════════════════════════


class TestTokenExpiry:
    """AC8: Expired token → error."""

    def test_valid_token(self):
        invite = create_guest_invite("session-1")
        error = validate_token(invite)
        assert error is None

    def test_expired_token(self):
        invite = create_guest_invite("session-1")
        future = datetime.now(timezone.utc) + timedelta(minutes=31)
        error = validate_token(invite, now=future)
        assert error == GuestJoinError.TOKEN_EXPIRED.value

    def test_expired_via_service(self):
        svc = GuestJoinService()
        invite = create_guest_invite("session-1")
        # Manually expire
        data = invite.model_dump()
        data["expires_at"] = datetime.now(timezone.utc) - timedelta(minutes=1)
        expired_invite = GuestInvite(**data)
        result = svc.validate_invite(expired_invite)
        assert result.success is False
        assert result.error == GuestJoinError.TOKEN_EXPIRED.value

    def test_connect_with_expired_fails(self):
        svc = GuestJoinService()
        invite = create_guest_invite("session-1")
        data = invite.model_dump()
        data["expires_at"] = datetime.now(timezone.utc) - timedelta(minutes=1)
        expired_invite = GuestInvite(**data)
        result = svc.connect_guest(expired_invite, "Guest Bob")
        assert result.success is False


# ═══════════════════════════════════════════════════════════════════════
# AC9: TURN Fallback (ICE config)
# ═══════════════════════════════════════════════════════════════════════


class TestTURNFallback:
    """AC9: STUN blocked → TURN relay. Check ICE server config."""

    def test_ice_servers_include_stun(self):
        stun_urls = [s["urls"] for s in DEFAULT_ICE_SERVERS if "stun" in s["urls"]]
        assert len(stun_urls) >= 1

    def test_ice_servers_include_turn(self):
        turn_urls = [s["urls"] for s in DEFAULT_ICE_SERVERS if "turn" in s["urls"]]
        assert len(turn_urls) >= 1

    def test_turn_has_credentials(self):
        turn_servers = [s for s in DEFAULT_ICE_SERVERS if "turn" in s["urls"]]
        for srv in turn_servers:
            assert "username" in srv
            assert "credential" in srv


# ═══════════════════════════════════════════════════════════════════════
# AC10: Recording Integrity (model-level)
# ═══════════════════════════════════════════════════════════════════════


class TestRecordingIntegrity:
    """AC10: Output video contains both coach and guest video/audio."""

    def test_guest_rect_computed_for_pip(self):
        rect = compute_guest_rect(1920, 1080, GuestLayoutMode.PIP.value)
        assert rect.width > 0
        assert rect.height > 0

    def test_guest_rect_computed_for_sbs(self):
        rect = compute_guest_rect(1920, 1080, GuestLayoutMode.SIDE_BY_SIDE.value)
        assert rect.x == pytest.approx(960, abs=1)
        assert rect.width == pytest.approx(960, abs=1)


# ═══════════════════════════════════════════════════════════════════════
# Layout Switch
# ═══════════════════════════════════════════════════════════════════════


class TestLayoutSwitch:
    """Toggle between PiP and Side-by-Side."""

    def test_pip_to_sbs(self):
        svc = GuestJoinService()
        config = GuestLayoutConfig(layout_mode=GuestLayoutMode.PIP.value)
        new = svc.switch_layout(config, 1920, 1080)
        assert new.layout_mode == GuestLayoutMode.SIDE_BY_SIDE.value
        assert new.guest_rect is not None

    def test_sbs_to_pip(self):
        svc = GuestJoinService()
        config = GuestLayoutConfig(layout_mode=GuestLayoutMode.SIDE_BY_SIDE.value)
        new = svc.switch_layout(config, 1920, 1080)
        assert new.layout_mode == GuestLayoutMode.PIP.value
        assert new.guest_rect is not None


# ═══════════════════════════════════════════════════════════════════════
# Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """Receipt chain integrity for guest join operations."""

    def test_full_flow_chain(self):
        svc = GuestJoinService()
        invite = svc.create_invite("session-1").invite
        conn = svc.connect_guest(invite, "Guest Bob")
        svc.disconnect_guest(conn.session)
        assert len(svc.receipt_chain) == 3
        assert svc.verify_receipt_chain() is True

    def test_empty_chain_valid(self):
        svc = GuestJoinService()
        assert svc.verify_receipt_chain() is True

    def test_agent_name(self):
        svc = GuestJoinService()
        svc.create_invite("session-1")
        assert svc.receipt_chain[0]["agent_name"] == GUEST_JOIN_AGENT_NAME


# ═══════════════════════════════════════════════════════════════════════
# SQL + Constants
# ═══════════════════════════════════════════════════════════════════════


class TestSQLAndConstants:
    """Verify SQL schema and constants."""

    def test_guest_sessions_sql(self):
        assert "studio_guest_sessions" in GUEST_SESSIONS_SQL
        assert "join_token" in GUEST_SESSIONS_SQL
        assert "layout_mode" in GUEST_SESSIONS_SQL
        assert "studio_sessions" in GUEST_SESSIONS_SQL  # FK

    def test_token_length(self):
        assert INVITE_TOKEN_LENGTH == 64

    def test_token_expiry(self):
        assert TOKEN_EXPIRY_MINUTES == 30

    def test_pip_sizes(self):
        assert PIP_SIZE_DEFAULT == 0.25
        assert PIP_SIZE_MIN == 0.15
        assert PIP_SIZE_MAX == 0.35

    def test_agent_name(self):
        assert GUEST_JOIN_AGENT_NAME == "Diego"

    def test_ice_servers(self):
        assert len(DEFAULT_ICE_SERVERS) >= 2

    def test_layout_modes(self):
        modes = [m.value for m in GuestLayoutMode]
        assert "pip" in modes
        assert "side_by_side" in modes

    def test_session_statuses(self):
        statuses = [s.value for s in GuestSessionStatus]
        assert "pending" in statuses
        assert "connected" in statuses
        assert "disconnected" in statuses
