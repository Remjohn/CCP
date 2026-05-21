"""Integration tests for FR-ERA3-03 — Silent Referral Architecture.
Full Vote-Then-React loop and cooldown routing."""
import pytest
from datetime import datetime, timezone
from src.ccp.models.referral_models import (
    EarnedEscalationViolation, SignatureMismatchError, UserCardPayload,
)
from src.ccp.services.cryptographic_signer import CryptographicCardSigner
from src.ccp.services.referral_escalation_engine import ReferralEscalationEngine


def _payload(score=85):
    return UserCardPayload(
        session_id="sess-int-001", coach_id="coach-int-001",
        timestamp=datetime(2026, 5, 15, 14, 0, 0, tzinfo=timezone.utc),
        biometric_hash="b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        score_value=score,
    )


class TestFullVoteThenReactLoopSuccess:
    """§10 integration test 1: Full deep-link → vote → win-state → escalation → lead capture."""

    def test_full_loop(self):
        signer = CryptographicCardSigner(secret="integration-test-secret")
        engine = ReferralEscalationEngine()

        # Step 1: Coach generates signed card
        signed_card = signer.sign(_payload(92))
        assert signed_card.signature

        # Step 2: Peer receives deep link, backend verifies card
        verified = signer.verify(signed_card)
        assert verified.session_id == "sess-int-001"
        assert verified.score_value == 92

        # Step 3: Initialize peer in escalation engine
        state = engine.initialize_peer(peer_telegram_id=99001, coach_source_id="coach-int-001")
        assert state.vote_submitted is False
        assert state.win_state_delivered is False

        # Step 4: Peer submits vote → receives Ephemeral Win-State
        result = engine.submit_vote(peer_telegram_id=99001, vote_value=90, consensus_value=92)
        assert result.expansion_trigger_unlocked is True
        assert result.win_state_message  # Non-empty message

        # Verify state transition
        state = engine.get_state(99001)
        assert state.vote_submitted is True
        assert state.win_state_delivered is True

        # Step 5: Escalation now allowed
        esc = engine.request_escalation(peer_telegram_id=99001)
        assert esc["escalation_presented"] is True

        # Step 6: Lead capture after escalation
        lead = engine.capture_lead(peer_telegram_id=99001, peer_data={"name": "Test Peer"})
        assert lead["offer_tier"] == 1  # Tier 1 / $0 provisional access
        assert lead["peer_telegram_id"] == 99001

    def test_tampered_card_rejected(self):
        """AC1 failure: Tampered card does not pass verification."""
        signer = CryptographicCardSigner(secret="integration-test-secret")
        signed = signer.sign(_payload(85))
        # Tamper score
        tampered_payload = _payload(99)
        from src.ccp.models.referral_models import SignedUserCard
        tampered = SignedUserCard(payload=tampered_payload, signature=signed.signature)
        with pytest.raises(SignatureMismatchError):
            signer.verify(tampered)

    def test_premature_escalation_blocked(self):
        """AC2 failure: Escalation before win-state raises EarnedEscalationViolation."""
        engine = ReferralEscalationEngine()
        engine.initialize_peer(peer_telegram_id=99002, coach_source_id="coach-int-001")
        with pytest.raises(EarnedEscalationViolation):
            engine.request_escalation(peer_telegram_id=99002)

    def test_premature_lead_capture_blocked(self):
        """AC3 failure: Lead capture before escalation is presented."""
        engine = ReferralEscalationEngine()
        engine.initialize_peer(peer_telegram_id=99003, coach_source_id="coach-int-001")
        engine.submit_vote(peer_telegram_id=99003, vote_value=80, consensus_value=85)
        # Skip request_escalation
        with pytest.raises(EarnedEscalationViolation):
            engine.capture_lead(peer_telegram_id=99003, peer_data={})


class TestReferralPeerCooldownRouting:
    """§10 integration test 2: Peer on commercial cooldown can vote but not aggressively escalated."""

    def test_peer_can_vote_regardless_of_cooldown(self):
        engine = ReferralEscalationEngine()
        engine.initialize_peer(peer_telegram_id=99010, coach_source_id="coach-int-002")
        # Peer votes — cooldown does not block voting
        result = engine.submit_vote(peer_telegram_id=99010, vote_value=75, consensus_value=80)
        assert result.expansion_trigger_unlocked is True

    def test_vote_miss_still_delivers_win_state(self):
        """Even a miss vote delivers win-state (encouragement), unlocking escalation."""
        engine = ReferralEscalationEngine()
        engine.initialize_peer(peer_telegram_id=99011, coach_source_id="coach-int-002")
        result = engine.submit_vote(peer_telegram_id=99011, vote_value=10, consensus_value=90)
        assert result.win_state_message  # Always provides a message
        assert result.expansion_trigger_unlocked is True
        state = engine.get_state(99011)
        assert state.win_state_delivered is True
