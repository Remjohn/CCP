"""Unit tests for FR-ERA3-03 — Cryptographic Card Signer.
Tests: valid payload, tampered score, altered biometric, premature escalation."""
import pytest
from datetime import datetime, timezone
from src.ccp.models.referral_models import (
    EarnedEscalationViolation, ReferralEscalationState, SignatureMismatchError,
    SignedUserCard, UserCardPayload,
)
from src.ccp.services.cryptographic_signer import CryptographicCardSigner
from src.ccp.services.referral_escalation_engine import ReferralEscalationEngine


def _payload(score=85):
    return UserCardPayload(
        session_id="sess-001", coach_id="coach-001",
        timestamp=datetime(2026, 5, 15, 12, 0, 0, tzinfo=timezone.utc),
        biometric_hash="a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        score_value=score,
    )


class TestSignerValidPayloadPasses:
    """§10 test 1: Correctly signed payload passes validation."""
    def test(self):
        signer = CryptographicCardSigner(secret="test-secret")
        signed = signer.sign(_payload())
        verified = signer.verify(signed)
        assert verified.session_id == "sess-001"
        assert verified.score_value == 85


class TestSignerTamperedScoreFails:
    """§10 test 2: Modified score_value after signing raises SignatureMismatchError."""
    def test(self):
        signer = CryptographicCardSigner(secret="test-secret")
        signed = signer.sign(_payload(85))
        # Tamper with score_value
        tampered_payload = _payload(99)
        tampered_card = SignedUserCard(payload=tampered_payload, signature=signed.signature)
        with pytest.raises(SignatureMismatchError):
            signer.verify(tampered_card)


class TestSignerAlteredBiometricHashFails:
    """§10 test 3: Altered biometric_hash confirms failure."""
    def test(self):
        signer = CryptographicCardSigner(secret="test-secret")
        signed = signer.sign(_payload())
        # Alter biometric_hash
        altered = UserCardPayload(
            session_id="sess-001", coach_id="coach-001",
            timestamp=datetime(2026, 5, 15, 12, 0, 0, tzinfo=timezone.utc),
            biometric_hash="FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            score_value=85,
        )
        tampered_card = SignedUserCard(payload=altered, signature=signed.signature)
        with pytest.raises(SignatureMismatchError):
            signer.verify(tampered_card)


class TestEscalationEnginePrematureEscalationRaises:
    """§10 test 4: Premature escalation raises EarnedEscalationViolation."""
    def test(self):
        engine = ReferralEscalationEngine()
        engine.initialize_peer(peer_telegram_id=12345, coach_source_id="coach-001")
        # Attempt escalation before vote/win-state
        with pytest.raises(EarnedEscalationViolation):
            engine.request_escalation(peer_telegram_id=12345)


class TestDeepLinkGeneration:
    """Verify deep link contains ref_ prefix and session_id."""
    def test(self):
        signer = CryptographicCardSigner(secret="test-secret")
        signed = signer.sign(_payload())
        link = signer.generate_deep_link(signed)
        assert "startapp=ref_" in link
        assert "sess-001" in link
