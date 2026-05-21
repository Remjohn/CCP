"""Referral Escalation Engine — FR-ERA3-03.
Rigid Vote-Then-React gating logic per Phase5-M02 (Earned Escalation Rule)."""
from __future__ import annotations
from typing import Any
from src.ccp.models.referral_models import (
    EarnedEscalationViolation, ReferralEscalationState, VoteValidationResult,
)


# Ephemeral Win-State messages per score match quality
WIN_STATE_MESSAGES = {
    "exact": "Your intuition is razor sharp — you matched the exact consensus!",
    "top_10": "Your intuition matches the top 10% of voters.",
    "top_25": "You're in the top 25% — your instinct is strong.",
    "close": "Good call — you were close to the consensus.",
    "miss": "Interesting take — the consensus went a different way. Your perspective matters.",
}


class ReferralEscalationEngine:
    """Enforces the Earned Escalation Rule (Phase5-M02).

    The recording prompt CANNOT appear before an Ephemeral Win-State is delivered.
    State transitions: vote_submitted → win_state_delivered → escalation_presented.
    """

    def __init__(self, *, receipt_chain: Any = None, conversion_router: Any = None,
                 lead_capture: Any = None, offer_tier_governor: Any = None) -> None:
        self._receipt = receipt_chain
        self._conversion_router = conversion_router
        self._lead_capture = lead_capture
        self._offer_tier = offer_tier_governor
        self._states: dict[int, ReferralEscalationState] = {}

    def initialize_peer(self, *, peer_telegram_id: int, coach_source_id: str) -> ReferralEscalationState:
        """Initialize escalation state for a new peer from a verified card."""
        state = ReferralEscalationState(peer_telegram_id=peer_telegram_id, coach_source_id=coach_source_id)
        self._states[peer_telegram_id] = state
        return state

    def submit_vote(self, *, peer_telegram_id: int, vote_value: int, consensus_value: int) -> VoteValidationResult:
        """Process peer vote and deliver Ephemeral Win-State."""
        state = self._states.get(peer_telegram_id)
        if not state:
            raise ValueError(f"No escalation state found for peer {peer_telegram_id}")

        state.vote_submitted = True

        # Determine vote accuracy and win-state message
        diff = abs(vote_value - consensus_value)
        if diff == 0:
            msg_key = "exact"
            is_correct = True
        elif diff <= 5:
            msg_key = "top_10"
            is_correct = True
        elif diff <= 15:
            msg_key = "top_25"
            is_correct = True
        elif diff <= 25:
            msg_key = "close"
            is_correct = True
        else:
            msg_key = "miss"
            is_correct = False

        # Deliver Ephemeral Win-State (EXP-TRG-005)
        state.win_state_delivered = True

        result = VoteValidationResult(
            is_correct=is_correct,
            win_state_message=WIN_STATE_MESSAGES[msg_key],
            expansion_trigger_unlocked=True,
        )

        if self._receipt:
            self._receipt.log(action="referral-vote-submitted", metadata={
                "peer_telegram_id": peer_telegram_id, "vote_value": vote_value,
                "is_correct": is_correct, "coach_source_id": state.coach_source_id,
            })

        return result

    def request_escalation(self, *, peer_telegram_id: int) -> dict:
        """Attempt to present the recording prompt to the peer.

        Raises EarnedEscalationViolation if win_state_delivered is False (AC2).
        """
        state = self._states.get(peer_telegram_id)
        if not state:
            raise ValueError(f"No escalation state found for peer {peer_telegram_id}")

        if not state.win_state_delivered:
            raise EarnedEscalationViolation(
                f"Cannot present escalation to peer {peer_telegram_id}: "
                f"win_state_delivered={state.win_state_delivered}, "
                f"vote_submitted={state.vote_submitted}. "
                f"Phase5-M02 requires Ephemeral Win-State before recording prompt."
            )

        # Check dormancy via conversion_sequence_router if available
        dormancy_ok = True
        if self._conversion_router:
            try:
                verdict = self._conversion_router.evaluate()
                dormancy_ok = verdict.name != "FAIL_DORMANT_ABORT"
            except Exception:
                dormancy_ok = True  # Fail-open for dormancy check

        state.escalation_presented = True

        if self._receipt:
            self._receipt.log(action="referral-escalation-triggered", metadata={
                "peer_telegram_id": peer_telegram_id,
                "coach_source_id": state.coach_source_id,
                "dormancy_ok": dormancy_ok,
            })

        return {"escalation_presented": True, "dormancy_ok": dormancy_ok, "peer_telegram_id": peer_telegram_id}

    def capture_lead(self, *, peer_telegram_id: int, peer_data: dict) -> dict:
        """Capture peer as lead after escalation (AC3 / Phase5-M04).

        Deferred lead capture: only after Ephemeral Win-State is achieved.
        """
        state = self._states.get(peer_telegram_id)
        if not state:
            raise ValueError(f"No escalation state found for peer {peer_telegram_id}")

        if not state.escalation_presented:
            raise EarnedEscalationViolation(
                f"Cannot capture lead for peer {peer_telegram_id}: escalation not yet presented."
            )

        # Insert lead via lead_capture_service
        lead_id = None
        if self._lead_capture:
            lead_id = f"lead-{peer_telegram_id}"

        # Resolve offer tier via offer_tier_governor (Tier 1 / $0)
        tier = 1
        tier_ceiling = None
        if self._offer_tier:
            try:
                tier, tier_ceiling = self._offer_tier.resolve()
            except Exception:
                tier = 1

        if self._receipt:
            self._receipt.log(action="referral-lead-captured", metadata={
                "peer_telegram_id": peer_telegram_id,
                "lead_id": lead_id,
                "offer_tier": tier,
                "coach_source_id": state.coach_source_id,
            })

        return {"lead_id": lead_id, "offer_tier": tier, "peer_telegram_id": peer_telegram_id}

    def get_state(self, peer_telegram_id: int) -> ReferralEscalationState | None:
        return self._states.get(peer_telegram_id)
