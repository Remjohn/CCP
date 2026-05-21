"""Cryptographic Card Signer — FR-ERA3-03 / DEP-SEC-011.
HMAC-SHA256 signing and verification for User Cards (Phase5-M01)."""
from __future__ import annotations
import hashlib
import hmac
import json
import os
from src.ccp.models.referral_models import SignatureMismatchError, SignedUserCard, UserCardPayload


SIGNING_SECRET: str = os.environ.get("CCP_REFERRAL_HMAC_SECRET", "ccp-default-referral-hmac-secret-change-in-prod")


class CryptographicCardSigner:
    """HMAC-SHA256 signer/verifier for UserCardPayload.

    Phase5-M01 enforcement: All shareable score objects MUST include a backend
    cryptographic hash binding session_id, timestamp, and biometric_hash.
    """

    def __init__(self, secret: str | None = None) -> None:
        self._secret = (secret or SIGNING_SECRET).encode("utf-8")

    def _canonical_payload(self, payload: UserCardPayload) -> str:
        """Deterministic JSON serialization for HMAC input."""
        canonical = {
            "session_id": payload.session_id,
            "coach_id": payload.coach_id,
            "timestamp": payload.timestamp.isoformat(),
            "biometric_hash": payload.biometric_hash,
            "score_value": payload.score_value,
        }
        return json.dumps(canonical, sort_keys=True, separators=(",", ":"))

    def sign(self, payload: UserCardPayload) -> SignedUserCard:
        """Generate HMAC-SHA256 signature over the canonical payload."""
        canonical = self._canonical_payload(payload)
        signature = hmac.new(self._secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
        return SignedUserCard(payload=payload, signature=signature)

    def verify(self, signed_card: SignedUserCard) -> UserCardPayload:
        """Verify HMAC-SHA256 signature. Raises SignatureMismatchError on failure."""
        canonical = self._canonical_payload(signed_card.payload)
        expected = hmac.new(self._secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signed_card.signature):
            raise SignatureMismatchError(
                f"Signature mismatch: payload has been tampered with. "
                f"session_id={signed_card.payload.session_id}"
            )
        return signed_card.payload

    def generate_deep_link(self, signed_card: SignedUserCard, bot_username: str = "ccp_bot") -> str:
        """Generate Telegram deep link with ref_ prefix for the signed card."""
        compact = f"{signed_card.payload.session_id}:{signed_card.payload.score_value}:{signed_card.signature[:16]}"
        return f"https://t.me/{bot_username}/app?startapp=ref_{compact}"
