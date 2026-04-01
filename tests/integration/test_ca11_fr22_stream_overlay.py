"""FR-CA11-22 — Studio Stream Overlay & Trivianar Display — Integration Tests.

Target: 8 ACs + state machine + transitions + branding + timing + receipt chain + constants.
"""
from __future__ import annotations

import pytest

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
from src.ccp.services.stream_overlay_service import (
    EVENT_STATE_MAP,
    VALID_TRANSITIONS,
    StreamOverlayService,
    apply_brand_to_card_style,
    compute_bar_widths,
    compute_countdown_progress,
    compute_winner_timing,
    is_valid_transition,
    resolve_target_state,
    select_leaderboard_top,
)


# ═══════════════════════════════════════════════════════════════════════
# AC1: Question Display
# ═══════════════════════════════════════════════════════════════════════


class TestQuestionDisplay:
    """AC1: question_sent → overlay renders question + options + countdown."""

    def test_question_event_model(self):
        event = OverlayQuestionEvent(
            question_id="q-1",
            text="What year was CBT developed?",
            options=[
                OverlayQuestionOption(key="A", text="1952", color="#E74C3C"),
                OverlayQuestionOption(key="B", text="1960", color="#3498DB"),
            ],
        )
        assert event.text == "What year was CBT developed?"
        assert len(event.options) == 2

    def test_question_sent_transitions_to_question(self):
        svc = StreamOverlayService()
        result = svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        assert result.success is True
        assert svc.state == OverlayState.QUESTION.value

    def test_question_has_time_limit(self):
        event = OverlayQuestionEvent(
            question_id="q-1",
            text="Test?",
            options=[
                OverlayQuestionOption(key="A", text="Yes"),
                OverlayQuestionOption(key="B", text="No"),
            ],
            time_limit_seconds=15,
        )
        assert event.time_limit_seconds == 15


# ═══════════════════════════════════════════════════════════════════════
# AC2: Countdown Bar
# ═══════════════════════════════════════════════════════════════════════


class TestCountdownBar:
    """AC2: Countdown bar full → empty over time_limit_seconds."""

    def test_progress_starts_at_full(self):
        progress = compute_countdown_progress(0, 15000)
        assert progress == pytest.approx(1.0)

    def test_progress_at_half(self):
        progress = compute_countdown_progress(7500, 15000)
        assert progress == pytest.approx(0.5)

    def test_progress_at_end(self):
        progress = compute_countdown_progress(15000, 15000)
        assert progress == pytest.approx(0.0)

    def test_progress_clamped_above_total(self):
        progress = compute_countdown_progress(20000, 15000)
        assert progress == 0.0

    def test_progress_zero_total(self):
        progress = compute_countdown_progress(1000, 0)
        assert progress == 0.0

    def test_via_service(self):
        svc = StreamOverlayService()
        progress = svc.get_countdown_progress(3000, 15000)
        assert progress == pytest.approx(0.8)


# ═══════════════════════════════════════════════════════════════════════
# AC3: Answer Distribution
# ═══════════════════════════════════════════════════════════════════════


class TestAnswerDistribution:
    """AC3: Bar widths proportional to percentage. Correct answer glows."""

    def test_distribution_event_model(self):
        event = OverlayDistributionEvent(
            question_id="q-1",
            correct_answer="B",
            distribution={
                "A": AnswerDistributionEntry(count=12, percentage=24),
                "B": AnswerDistributionEntry(count=28, percentage=56),
                "C": AnswerDistributionEntry(count=5, percentage=10),
                "D": AnswerDistributionEntry(count=5, percentage=10),
            },
        )
        assert event.correct_answer == "B"
        assert event.distribution["B"].percentage == 56

    def test_bar_widths_proportional(self):
        dist = {
            "A": AnswerDistributionEntry(percentage=25),
            "B": AnswerDistributionEntry(percentage=50),
            "C": AnswerDistributionEntry(percentage=15),
            "D": AnswerDistributionEntry(percentage=10),
        }
        widths = compute_bar_widths(dist, 1000)
        assert widths["B"] == pytest.approx(500)
        assert widths["A"] == pytest.approx(250)

    def test_correct_answer_wider(self):
        dist = {
            "A": AnswerDistributionEntry(percentage=24),
            "B": AnswerDistributionEntry(percentage=56),
        }
        widths = compute_bar_widths(dist, 1000)
        assert widths["B"] > widths["A"]

    def test_distribution_transitions(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        result = svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value)
        assert result.success is True
        assert svc.state == OverlayState.DISTRIBUTION.value


# ═══════════════════════════════════════════════════════════════════════
# AC4: Leaderboard Slide-In
# ═══════════════════════════════════════════════════════════════════════


class TestLeaderboardPanel:
    """AC4: Slides in from right, top 5, auto-dismiss at 5s."""

    def test_leaderboard_event_model(self):
        event = OverlayLeaderboardEvent(
            top_5=[
                OverlayLeaderboardEntry(rank=1, name="Sarah", score=2450, change="+150"),
                OverlayLeaderboardEntry(rank=2, name="Mike", score=2100, change="+80"),
            ],
        )
        assert len(event.top_5) == 2
        assert event.top_5[0].name == "Sarah"

    def test_top_5_selection(self):
        entries = [
            OverlayLeaderboardEntry(rank=i, name=f"P{i}", score=100 * (10 - i))
            for i in range(1, 10)
        ]
        top = select_leaderboard_top(entries)
        assert len(top) == LEADERBOARD_DISPLAY_SIZE
        assert top[0].score >= top[1].score

    def test_leaderboard_transition(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value)
        result = svc.handle_event(OverlayEventType.LEADERBOARD_UPDATED.value)
        assert result.success is True
        assert svc.state == OverlayState.LEADERBOARD.value

    def test_auto_dismiss_constant(self):
        assert LEADERBOARD_AUTO_DISMISS_SECONDS == 5


# ═══════════════════════════════════════════════════════════════════════
# AC5: Winner Reveal
# ═══════════════════════════════════════════════════════════════════════


class TestWinnerReveal:
    """AC5: 3rd→2nd→1st reveal + confetti."""

    def test_winner_event_model(self):
        event = OverlayWinnerEvent(
            winners=[
                WinnerEntry(rank=3, name="Lisa", score=1900),
                WinnerEntry(rank=2, name="Mike", score=2100),
                WinnerEntry(rank=1, name="Sarah", score=2450),
            ],
        )
        assert len(event.winners) == 3
        assert event.winners[0].rank == 3  # 3rd first

    def test_winner_timing(self):
        timing = compute_winner_timing()
        assert timing["3rd"] == WINNER_HOLD_3RD_SECONDS
        assert timing["2nd"] == WINNER_HOLD_2ND_SECONDS
        assert timing["1st"] == WINNER_HOLD_1ST_SECONDS
        assert timing["confetti"] == CONFETTI_DURATION_SECONDS
        assert timing["total"] == WINNER_TOTAL_SECONDS

    def test_winner_transition(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value)
        svc.handle_event(OverlayEventType.LEADERBOARD_UPDATED.value)
        result = svc.handle_event(OverlayEventType.WINNER_REVEAL.value)
        assert result.success is True
        assert svc.state == OverlayState.WINNER.value

    def test_winner_to_idle(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value)
        svc.handle_event(OverlayEventType.LEADERBOARD_UPDATED.value)
        svc.handle_event(OverlayEventType.WINNER_REVEAL.value)
        result = svc.handle_event(OverlayEventType.CLEAR.value)
        assert result.success is True
        assert svc.state == OverlayState.IDLE.value


# ═══════════════════════════════════════════════════════════════════════
# AC6: DPA Branding
# ═══════════════════════════════════════════════════════════════════════


class TestDPABranding:
    """AC6: Overlay uses coach brand colors."""

    def test_brand_config_default(self):
        brand = OverlayBrandConfig()
        assert brand.primary_color == "#2E86AB"

    def test_custom_brand_color(self):
        brand = OverlayBrandConfig(primary_color="#FF5733")
        style = apply_brand_to_card_style(brand)
        assert style["border_color"] == "#FF5733"

    def test_card_bg(self):
        brand = OverlayBrandConfig()
        style = apply_brand_to_card_style(brand)
        assert style["background"] == OVERLAY_CARD_BG

    def test_service_uses_brand(self):
        brand = OverlayBrandConfig(primary_color="#2E86AB")
        svc = StreamOverlayService(brand=brand)
        style = svc.get_card_style()
        assert style["border_color"] == "#2E86AB"


# ═══════════════════════════════════════════════════════════════════════
# AC7: Recording Capture (model-level)
# ═══════════════════════════════════════════════════════════════════════


class TestRecordingCapture:
    """AC7: Output video contains overlay composited with webcam."""

    def test_full_cycle_state_machine(self):
        svc = StreamOverlayService()
        # idle → question → distribution → leaderboard → winner → idle
        assert svc.handle_event(OverlayEventType.QUESTION_SENT.value).success is True
        assert svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value).success is True
        assert svc.handle_event(OverlayEventType.LEADERBOARD_UPDATED.value).success is True
        assert svc.handle_event(OverlayEventType.WINNER_REVEAL.value).success is True
        assert svc.handle_event(OverlayEventType.CLEAR.value).success is True
        assert svc.state == OverlayState.IDLE.value


# ═══════════════════════════════════════════════════════════════════════
# AC8: Idle State
# ═══════════════════════════════════════════════════════════════════════


class TestIdleState:
    """AC8: No events → idle, renders nothing."""

    def test_initial_state_is_idle(self):
        svc = StreamOverlayService()
        assert svc.state == OverlayState.IDLE.value

    def test_clear_returns_to_idle(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        svc.handle_event(OverlayEventType.CLEAR.value)
        assert svc.state == OverlayState.IDLE.value


# ═══════════════════════════════════════════════════════════════════════
# State Machine Transitions
# ═══════════════════════════════════════════════════════════════════════


class TestStateMachine:
    """State machine transition validation."""

    def test_invalid_transition_rejected(self):
        svc = StreamOverlayService()
        # idle → distribution is not valid
        result = svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value)
        assert result.success is False
        assert result.error == OverlayError.INVALID_TRANSITION.value

    def test_unknown_event(self):
        svc = StreamOverlayService()
        result = svc.handle_event("nonexistent_event")
        assert result.success is False
        assert result.error == OverlayError.UNKNOWN_EVENT.value

    def test_valid_transitions_defined(self):
        for state in OverlayState:
            assert state.value in VALID_TRANSITIONS

    def test_event_state_map_complete(self):
        for event in OverlayEventType:
            assert event.value in EVENT_STATE_MAP

    def test_question_can_go_to_idle(self):
        assert is_valid_transition(OverlayState.QUESTION.value, OverlayState.IDLE.value)

    def test_distribution_can_skip_to_question(self):
        assert is_valid_transition(OverlayState.DISTRIBUTION.value, OverlayState.QUESTION.value)


# ═══════════════════════════════════════════════════════════════════════
# Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """Receipt chain integrity."""

    def test_full_cycle_chain(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        svc.handle_event(OverlayEventType.ANSWER_DISTRIBUTION.value)
        svc.handle_event(OverlayEventType.LEADERBOARD_UPDATED.value)
        svc.handle_event(OverlayEventType.WINNER_REVEAL.value)
        svc.handle_event(OverlayEventType.CLEAR.value)
        assert len(svc.receipt_chain) == 5
        assert svc.verify_receipt_chain() is True

    def test_empty_chain_valid(self):
        svc = StreamOverlayService()
        assert svc.verify_receipt_chain() is True

    def test_agent_name(self):
        svc = StreamOverlayService()
        svc.handle_event(OverlayEventType.QUESTION_SENT.value)
        assert svc.receipt_chain[0]["agent_name"] == OVERLAY_AGENT_NAME


# ═══════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify constants."""

    def test_countdown_tolerance(self):
        assert COUNTDOWN_BAR_TOLERANCE_MS == 500

    def test_leaderboard_size(self):
        assert LEADERBOARD_DISPLAY_SIZE == 5

    def test_leaderboard_dismiss(self):
        assert LEADERBOARD_AUTO_DISMISS_SECONDS == 5

    def test_winner_timing(self):
        assert WINNER_HOLD_3RD_SECONDS == 2
        assert WINNER_HOLD_2ND_SECONDS == 2
        assert WINNER_HOLD_1ST_SECONDS == 3
        assert WINNER_TOTAL_SECONDS == 8
        assert CONFETTI_DURATION_SECONDS == 3

    def test_card_bg(self):
        assert OVERLAY_CARD_BG == "rgba(0,0,0,0.75)"

    def test_agent_name(self):
        assert OVERLAY_AGENT_NAME == "Diego"

    def test_overlay_states(self):
        states = [s.value for s in OverlayState]
        assert len(states) == 5
        assert "idle" in states
        assert "winner" in states

    def test_event_types(self):
        events = [e.value for e in OverlayEventType]
        assert len(events) == 5
        assert "question_sent" in events
        assert "clear" in events
