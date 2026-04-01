"""FR-CA11-20 — Trivianar Lead Generation Viral Loop.

DEP-ENG-114: New Member Detection (Telegram new_chat_members)
DEP-ENG-115: Contact Capture DM Flow (request_contact + email)
DEP-ENG-116: CBCS Warm Start Entry (qualifying → partial coping trajectory)

Agent: Marco (Lead Capture Operator)
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    COMMERCIAL_COOLDOWN_DAYS,
    LEAD_CAPTURE_AGENT_NAME,
    MIN_QUALIFYING_RESPONSES,
    CBCSWarmStartPayload,
    CooldownCheck,
    LeadCaptureError,
    LeadCaptureResult,
    LeadContactUpdate,
    NurtureStatus,
    TriviaLead,
)

# ---------------------------------------------------------------------------
# SQL (§5 Data Model)
# ---------------------------------------------------------------------------

TRIVIA_LEADS_SQL = """
CREATE TABLE IF NOT EXISTS trivia_leads (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_user_id            BIGINT NOT NULL,
    first_name                  VARCHAR(255),
    phone_number                VARCHAR(30),
    email                       VARCHAR(255),
    referred_by_user_id         BIGINT,
    coach_id                    UUID NOT NULL REFERENCES coaches(id),
    stream_id                   UUID,
    cbcs_initial_assessment     JSONB,
    nurture_status              VARCHAR(20) DEFAULT 'new',
    commercial_cooldown_until   TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trivia_leads_coach ON trivia_leads(coach_id);
CREATE INDEX IF NOT EXISTS idx_trivia_leads_status ON trivia_leads(nurture_status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_trivia_leads_unique_user
    ON trivia_leads(telegram_user_id, coach_id);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class LeadDatabaseProtocol(Protocol):
    async def insert_lead(self, lead: dict[str, Any]) -> str: ...
    async def get_lead(self, telegram_user_id: int, coach_id: str) -> Optional[dict[str, Any]]: ...
    async def update_lead(self, lead_id: str, updates: dict[str, Any]) -> None: ...


class TelegramBotProtocol(Protocol):
    async def send_contact_request(self, chat_id: int, message: str) -> None: ...
    async def send_message(self, chat_id: int, message: str) -> None: ...


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


def detect_new_member(
    telegram_user_id: int,
    first_name: str,
    coach_id: str,
    stream_id: str,
    referred_by_user_id: Optional[int] = None,
) -> TriviaLead:
    """§4 Stage 1: Detect new_chat_members → create TriviaLead.

    AC1: telegram_user_id + first_name captured.
    AC6: referred_by_user_id links referral.
    """
    now = datetime.now(timezone.utc)
    return TriviaLead(
        telegram_user_id=telegram_user_id,
        first_name=first_name,
        coach_id=coach_id,
        stream_id=stream_id,
        referred_by_user_id=referred_by_user_id,
        nurture_status=NurtureStatus.NEW.value,
        commercial_cooldown_until=now + timedelta(days=COMMERCIAL_COOLDOWN_DAYS),
        created_at=now,
        updated_at=now,
    )


def apply_contact_update(
    lead: TriviaLead, update: LeadContactUpdate,
) -> TriviaLead:
    """§4 Stage 2: Apply phone/email from DM flow.

    AC2: phone_number stored.
    AC3: email stored.
    """
    data = lead.model_dump()
    if update.phone_number is not None:
        data["phone_number"] = update.phone_number
    if update.email is not None:
        data["email"] = update.email
    if update.phone_number or update.email:
        data["nurture_status"] = NurtureStatus.ACTIVE.value
    data["updated_at"] = datetime.now(timezone.utc)
    return TriviaLead(**data)


def compute_cbcs_warm_start(
    lead: TriviaLead,
    qualifying_mappings: list[dict[str, Any]],
) -> Optional[CBCSWarmStartPayload]:
    """§4 Stage 3 Step 1: Aggregate qualifying question CBCS mappings.

    AC4: ≥ MIN_QUALIFYING_RESPONSES → cbcs_initial_assessment produced.
    """
    if len(qualifying_mappings) < MIN_QUALIFYING_RESPONSES:
        return None

    # Aggregate: average each dimension across all responses
    dimension_sums: dict[str, float] = {}
    dimension_counts: dict[str, int] = {}
    for mapping in qualifying_mappings:
        for dim, value in mapping.items():
            dimension_sums[dim] = dimension_sums.get(dim, 0.0) + float(value)
            dimension_counts[dim] = dimension_counts.get(dim, 0) + 1

    assessment = {
        dim: round(dimension_sums[dim] / dimension_counts[dim], 4)
        for dim in dimension_sums
    }

    return CBCSWarmStartPayload(
        lead_id=lead.lead_id,
        telegram_user_id=lead.telegram_user_id,
        coach_id=lead.coach_id,
        qualifying_responses=len(qualifying_mappings),
        cbcs_initial_assessment=assessment,
        warm_start=True,
    )


def check_commercial_cooldown(
    lead: TriviaLead,
    now: Optional[datetime] = None,
) -> CooldownCheck:
    """§4 Stage 3 Step 4: 21-day commercial cooldown enforcement.

    AC5: No CPSC conversion evaluation within 21 days.
    """
    current = now or datetime.now(timezone.utc)

    if lead.commercial_cooldown_until is None:
        return CooldownCheck(is_active=False)

    cooldown_end = lead.commercial_cooldown_until
    if cooldown_end.tzinfo is None:
        cooldown_end = cooldown_end.replace(tzinfo=timezone.utc)

    if current < cooldown_end:
        remaining = (cooldown_end - current).days + 1
        return CooldownCheck(
            is_active=True,
            cooldown_until=cooldown_end,
            days_remaining=remaining,
        )

    return CooldownCheck(is_active=False, cooldown_until=cooldown_end, days_remaining=0)


# ---------------------------------------------------------------------------
# Lead Capture Service
# ---------------------------------------------------------------------------


class LeadCaptureService:
    """FR-CA11-20 — Trivianar Lead Capture.

    Stateless pure logic + receipt chain.
    """

    def __init__(self, db: LeadDatabaseProtocol | None = None) -> None:
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
            agent_name=LEAD_CAPTURE_AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Stage 1: New Member Detection --

    def capture_new_member(
        self,
        telegram_user_id: int,
        first_name: str,
        coach_id: str,
        stream_id: str,
        referred_by_user_id: Optional[int] = None,
    ) -> LeadCaptureResult:
        """AC1 + AC6: Detect new member, create lead, set cooldown."""
        lead = detect_new_member(
            telegram_user_id=telegram_user_id,
            first_name=first_name,
            coach_id=coach_id,
            stream_id=stream_id,
            referred_by_user_id=referred_by_user_id,
        )

        self._emit_receipt(
            stage_name="lead-capture",
            input_payload={"telegram_user_id": telegram_user_id, "stream_id": stream_id},
            output_payload={"lead_id": lead.lead_id, "nurture_status": lead.nurture_status},
        )

        return LeadCaptureResult(success=True, lead=lead)

    # -- Stage 2: Contact Update --

    def update_contact(
        self, lead: TriviaLead, update: LeadContactUpdate,
    ) -> LeadCaptureResult:
        """AC2 + AC3: Apply phone/email from DM flow, receipt PII event."""
        updated = apply_contact_update(lead, update)

        # PII capture receipt (§4 Stage 2 Step 7)
        self._emit_receipt(
            stage_name="contact-capture-pii",
            input_payload={
                "telegram_user_id": update.telegram_user_id,
                "has_phone": update.phone_number is not None,
                "has_email": update.email is not None,
            },
            output_payload={"lead_id": lead.lead_id, "nurture_status": updated.nurture_status},
        )

        return LeadCaptureResult(success=True, lead=updated)

    # -- Stage 3: CBCS Warm Start --

    def generate_warm_start(
        self, lead: TriviaLead, qualifying_mappings: list[dict[str, Any]],
    ) -> LeadCaptureResult:
        """AC4: Produce CBCS warm start payload from qualifying responses."""
        payload = compute_cbcs_warm_start(lead, qualifying_mappings)
        if payload is None:
            return LeadCaptureResult(
                success=False,
                error=LeadCaptureError.INSUFFICIENT_RESPONSES.value,
            )

        self._emit_receipt(
            stage_name="cbcs-warm-start",
            input_payload={"lead_id": lead.lead_id, "qualifying_count": len(qualifying_mappings)},
            output_payload=payload.model_dump(),
        )

        return LeadCaptureResult(success=True, lead=lead, warm_start=payload)

    # -- Cooldown check --

    def check_cooldown(self, lead: TriviaLead) -> CooldownCheck:
        """AC5: Check 21-day commercial cooldown."""
        return check_commercial_cooldown(lead)

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
