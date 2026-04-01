"""FR-CA11-22 — Studio Stream Overlay & Trivianar Display.

DEP-ENG-122: Overlay React Component (state machine)
DEP-ENG-123: Question Display Module
DEP-ENG-124: Answer Distribution Renderer
DEP-ENG-125: Leaderboard Panel
DEP-ENG-126: Winner Reveal Animation

Agent: Diego (Studio Overlay Operator)
Stress Test Q38: OffscreenCanvas Web Worker (canvas rendering)
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any

from src.ccp.models.ca11_models import (
    CONFETTI_DURATION_SECONDS,
    COUNTDOWN_BAR_TOLERANCE_MS,
    LEADERBOARD_AUTO_DISMISS_SECONDS,
    LEADERBOARD_DISPLAY_SIZE,
    OVERLAY_AGENT_NAME,
    OVERLAY_CARD_BG,
    WINNER_HOLD_1ST_SECONDS,
    WINNER_HOLD_2ND_SECONDS,
    WINNER_HOLD_3RD_SECONDS,
    WINNER_TOTAL_SECONDS,
    AnswerDistributionEntry,
    OverlayBrandConfig,
    OverlayDistributionEvent,
    OverlayError,
    OverlayEventType,
    OverlayLeaderboardEntry,
    OverlayLeaderboardEvent,
    OverlayQuestionEvent,
    OverlayQuestionOption,
    OverlayResult,
    OverlayState,
    OverlayWinnerEvent,
    WinnerEntry,
)

# ---------------------------------------------------------------------------
# Valid state transitions (§4 Stage 1 Step 2)
# ---------------------------------------------------------------------------

VALID_TRANSITIONS: dict[str, set[str]] = {
    OverlayState.IDLE.value: {
        OverlayState.QUESTION.value,
    },
    OverlayState.QUESTION.value: {
        OverlayState.DISTRIBUTION.value,
        OverlayState.IDLE.value,
    },
    OverlayState.DISTRIBUTION.value: {
        OverlayState.LEADERBOARD.value,
        OverlayState.QUESTION.value,
        OverlayState.IDLE.value,
    },
    OverlayState.LEADERBOARD.value: {
        OverlayState.WINNER.value,
        OverlayState.QUESTION.value,
        OverlayState.IDLE.value,
    },
    OverlayState.WINNER.value: {
        OverlayState.IDLE.value,
    },
}

# ---------------------------------------------------------------------------
# Event-to-state mapping (§4 Stage 1 Step 3)
# ---------------------------------------------------------------------------

EVENT_STATE_MAP: dict[str, str] = {
    OverlayEventType.QUESTION_SENT.value: OverlayState.QUESTION.value,
    OverlayEventType.ANSWER_DISTRIBUTION.value: OverlayState.DISTRIBUTION.value,
    OverlayEventType.LEADERBOARD_UPDATED.value: OverlayState.LEADERBOARD.value,
    OverlayEventType.WINNER_REVEAL.value: OverlayState.WINNER.value,
    OverlayEventType.CLEAR.value: OverlayState.IDLE.value,
}


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


def is_valid_transition(current: str, target: str) -> bool:
    """Check if state transition is allowed."""
    allowed = VALID_TRANSITIONS.get(current, set())
    return target in allowed


def resolve_target_state(event_type: str) -> str | None:
    """Map event type to target overlay state."""
    return EVENT_STATE_MAP.get(event_type)


def compute_countdown_progress(
    elapsed_ms: int, total_ms: int,
) -> float:
    """§4 Stage 2 Step 3: Countdown bar progress (1.0 → 0.0).

    AC2: Animates from full to empty over time_limit_seconds.
    """
    if total_ms <= 0:
        return 0.0
    progress = 1.0 - (elapsed_ms / total_ms)
    return max(0.0, min(1.0, progress))


def compute_bar_widths(
    distribution: dict[str, AnswerDistributionEntry],
    canvas_width: float,
) -> dict[str, float]:
    """§4 Stage 3 Step 3: Bar width proportional to vote percentage.

    AC3: Higher percentage → wider bar.
    """
    return {
        key: (entry.percentage / 100.0) * canvas_width
        for key, entry in distribution.items()
    }


def select_leaderboard_top(
    entries: list[OverlayLeaderboardEntry],
    limit: int = LEADERBOARD_DISPLAY_SIZE,
) -> list[OverlayLeaderboardEntry]:
    """§4 Stage 4 Step 3: Display top 5 participants."""
    sorted_entries = sorted(entries, key=lambda e: e.score, reverse=True)
    return sorted_entries[:limit]


def compute_winner_timing() -> dict[str, int]:
    """§4 Stage 5 Step 2: Winner reveal timing (seconds)."""
    return {
        "3rd": WINNER_HOLD_3RD_SECONDS,
        "2nd": WINNER_HOLD_2ND_SECONDS,
        "1st": WINNER_HOLD_1ST_SECONDS,
        "confetti": CONFETTI_DURATION_SECONDS,
        "total": WINNER_TOTAL_SECONDS,
    }


def apply_brand_to_card_style(brand: OverlayBrandConfig) -> dict[str, str]:
    """§4 Stage 2 Step 2: Apply DPA branding.

    AC6: overlay backgrounds, borders, and accent colors use brand color.
    """
    return {
        "background": brand.card_bg,
        "border_color": brand.primary_color,
        "accent_color": brand.accent_color,
        "font_family": brand.font_family,
    }


# ---------------------------------------------------------------------------
# Overlay State Machine Service
# ---------------------------------------------------------------------------


class StreamOverlayService:
    """FR-CA11-22 — Stream Overlay & Trivianar Display.

    State machine + overlay rendering logic.
    """

    def __init__(self, brand: OverlayBrandConfig | None = None) -> None:
        self._state: str = OverlayState.IDLE.value
        self._brand = brand or OverlayBrandConfig()
        self._receipt_chain: list[dict[str, Any]] = []

    @property
    def state(self) -> str:
        return self._state

    @property
    def brand(self) -> OverlayBrandConfig:
        return self._brand

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
            agent_name=OVERLAY_AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Event handling --

    def handle_event(self, event_type: str) -> OverlayResult:
        """Process a WebSocket event and transition state."""
        target = resolve_target_state(event_type)
        if target is None:
            return OverlayResult(
                success=False,
                state=self._state,
                error=OverlayError.UNKNOWN_EVENT.value,
            )

        if not is_valid_transition(self._state, target):
            return OverlayResult(
                success=False,
                state=self._state,
                error=OverlayError.INVALID_TRANSITION.value,
            )

        old_state = self._state
        self._state = target

        self._emit_receipt(
            stage_name="overlay-transition",
            input_payload={"event": event_type, "from": old_state},
            output_payload={"to": self._state},
        )

        return OverlayResult(success=True, state=self._state)

    # -- Layout helpers --

    def get_card_style(self) -> dict[str, str]:
        """Get branded card style for overlay rendering."""
        return apply_brand_to_card_style(self._brand)

    def get_countdown_progress(self, elapsed_ms: int, total_ms: int) -> float:
        """Get current countdown bar progress."""
        return compute_countdown_progress(elapsed_ms, total_ms)

    def get_bar_widths(
        self, distribution: dict[str, AnswerDistributionEntry], canvas_width: float,
    ) -> dict[str, float]:
        """Get distribution bar widths."""
        return compute_bar_widths(distribution, canvas_width)

    def get_winner_timing(self) -> dict[str, int]:
        """Get winner reveal timing."""
        return compute_winner_timing()

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
