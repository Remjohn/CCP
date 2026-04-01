"""FR-CA11-20 — Trivianar Lead Generation Viral Loop — Integration Tests.

Target: 6 ACs + cooldown logic + receipt chain + SQL + constants.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

import pytest

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
from src.ccp.services.lead_capture_service import (
    TRIVIA_LEADS_SQL,
    LeadCaptureService,
    apply_contact_update,
    check_commercial_cooldown,
    compute_cbcs_warm_start,
    detect_new_member,
)


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_lead(**overrides) -> TriviaLead:
    now = datetime.now(timezone.utc)
    defaults = dict(
        telegram_user_id=12345,
        first_name="Alice",
        coach_id="coach-1",
        stream_id="stream-1",
        nurture_status=NurtureStatus.NEW.value,
        commercial_cooldown_until=now + timedelta(days=COMMERCIAL_COOLDOWN_DAYS),
    )
    defaults.update(overrides)
    return TriviaLead(**defaults)


# ═══════════════════════════════════════════════════════════════════════
# AC1: Auto-Detect New Member
# ═══════════════════════════════════════════════════════════════════════


class TestAutoDetect:
    """AC1: new_chat_members → trivia_leads row with telegram_user_id + first_name."""

    def test_detect_creates_lead(self):
        lead = detect_new_member(
            telegram_user_id=12345,
            first_name="Alice",
            coach_id="coach-1",
            stream_id="stream-1",
        )
        assert lead.telegram_user_id == 12345
        assert lead.first_name == "Alice"
        assert lead.nurture_status == NurtureStatus.NEW.value

    def test_detect_sets_cooldown(self):
        lead = detect_new_member(
            telegram_user_id=12345,
            first_name="Alice",
            coach_id="coach-1",
            stream_id="stream-1",
        )
        assert lead.commercial_cooldown_until is not None
        delta = lead.commercial_cooldown_until - lead.created_at
        assert delta.days == COMMERCIAL_COOLDOWN_DAYS

    def test_detect_via_service(self):
        svc = LeadCaptureService()
        result = svc.capture_new_member(
            telegram_user_id=12345,
            first_name="Bob",
            coach_id="coach-1",
            stream_id="stream-1",
        )
        assert result.success is True
        assert result.lead is not None
        assert result.lead.first_name == "Bob"

    def test_detect_emits_receipt(self):
        svc = LeadCaptureService()
        svc.capture_new_member(
            telegram_user_id=12345,
            first_name="Bob",
            coach_id="coach-1",
            stream_id="stream-1",
        )
        assert len(svc.receipt_chain) == 1
        assert svc.receipt_chain[0]["stage_name"] == "lead-capture"


# ═══════════════════════════════════════════════════════════════════════
# AC2: Phone Capture
# ═══════════════════════════════════════════════════════════════════════


class TestPhoneCapture:
    """AC2: Bot DM → user shares contact → phone_number stored."""

    def test_phone_stored(self):
        lead = _make_lead()
        update = LeadContactUpdate(
            telegram_user_id=12345,
            coach_id="coach-1",
            phone_number="+1234567890",
        )
        updated = apply_contact_update(lead, update)
        assert updated.phone_number == "+1234567890"

    def test_status_becomes_active(self):
        lead = _make_lead()
        update = LeadContactUpdate(
            telegram_user_id=12345,
            coach_id="coach-1",
            phone_number="+1234567890",
        )
        updated = apply_contact_update(lead, update)
        assert updated.nurture_status == NurtureStatus.ACTIVE.value

    def test_phone_via_service(self):
        svc = LeadCaptureService()
        lead = _make_lead()
        update = LeadContactUpdate(
            telegram_user_id=12345,
            coach_id="coach-1",
            phone_number="+1234567890",
        )
        result = svc.update_contact(lead, update)
        assert result.success is True
        assert result.lead.phone_number == "+1234567890"


# ═══════════════════════════════════════════════════════════════════════
# AC3: Email Capture
# ═══════════════════════════════════════════════════════════════════════


class TestEmailCapture:
    """AC3: 24h later → bot sends email prompt → email stored."""

    def test_email_stored(self):
        lead = _make_lead(phone_number="+1234567890")
        update = LeadContactUpdate(
            telegram_user_id=12345,
            coach_id="coach-1",
            email="alice@example.com",
        )
        updated = apply_contact_update(lead, update)
        assert updated.email == "alice@example.com"

    def test_email_preserves_phone(self):
        lead = _make_lead(phone_number="+1234567890")
        update = LeadContactUpdate(
            telegram_user_id=12345,
            coach_id="coach-1",
            email="alice@example.com",
        )
        updated = apply_contact_update(lead, update)
        assert updated.phone_number == "+1234567890"

    def test_pii_receipt_emitted(self):
        svc = LeadCaptureService()
        lead = _make_lead()
        update = LeadContactUpdate(
            telegram_user_id=12345,
            coach_id="coach-1",
            email="alice@example.com",
        )
        svc.update_contact(lead, update)
        assert len(svc.receipt_chain) == 1
        assert svc.receipt_chain[0]["stage_name"] == "contact-capture-pii"


# ═══════════════════════════════════════════════════════════════════════
# AC4: CBCS Warm Start
# ═══════════════════════════════════════════════════════════════════════


class TestCBCSWarmStart:
    """AC4: ≥3 qualifying responses → cbcs_initial_assessment."""

    def test_warm_start_with_5_responses(self):
        lead = _make_lead()
        mappings = [
            {"social": 0.20},
            {"social": 0.10, "analytical": 0.30},
            {"social": 0.15, "analytical": 0.25},
            {"creative": 0.40},
            {"social": 0.05, "creative": 0.60},
        ]
        payload = compute_cbcs_warm_start(lead, mappings)
        assert payload is not None
        assert payload.warm_start is True
        assert "social" in payload.cbcs_initial_assessment
        assert payload.qualifying_responses == 5

    def test_insufficient_responses_returns_none(self):
        lead = _make_lead()
        mappings = [{"social": 0.20}, {"analytical": 0.30}]
        payload = compute_cbcs_warm_start(lead, mappings)
        assert payload is None

    def test_exactly_min_responses(self):
        lead = _make_lead()
        mappings = [{"social": 0.10}] * MIN_QUALIFYING_RESPONSES
        payload = compute_cbcs_warm_start(lead, mappings)
        assert payload is not None
        assert payload.qualifying_responses == MIN_QUALIFYING_RESPONSES

    def test_aggregation_averages(self):
        lead = _make_lead()
        mappings = [
            {"social": 0.20},
            {"social": 0.40},
            {"social": 0.60},
        ]
        payload = compute_cbcs_warm_start(lead, mappings)
        assert payload.cbcs_initial_assessment["social"] == 0.4

    def test_warm_start_via_service(self):
        svc = LeadCaptureService()
        lead = _make_lead()
        mappings = [{"social": 0.20}, {"analytical": 0.30}, {"social": 0.10}]
        result = svc.generate_warm_start(lead, mappings)
        assert result.success is True
        assert result.warm_start is not None

    def test_insufficient_via_service(self):
        svc = LeadCaptureService()
        lead = _make_lead()
        mappings = [{"social": 0.20}]
        result = svc.generate_warm_start(lead, mappings)
        assert result.success is False
        assert result.error == LeadCaptureError.INSUFFICIENT_RESPONSES.value


# ═══════════════════════════════════════════════════════════════════════
# AC5: 21-Day Commercial Cooldown
# ═══════════════════════════════════════════════════════════════════════


class TestCooldown:
    """AC5: No CPSC conversion within 21 days of capture."""

    def test_cooldown_active_on_day_1(self):
        lead = _make_lead()
        check = check_commercial_cooldown(lead)
        assert check.is_active is True
        assert check.days_remaining > 0

    def test_cooldown_expired_after_22_days(self):
        now = datetime.now(timezone.utc)
        lead = _make_lead(
            commercial_cooldown_until=now - timedelta(days=1),
        )
        check = check_commercial_cooldown(lead, now=now)
        assert check.is_active is False
        assert check.days_remaining == 0

    def test_cooldown_exactly_21_days(self):
        now = datetime.now(timezone.utc)
        lead = _make_lead(
            commercial_cooldown_until=now + timedelta(hours=1),
        )
        check = check_commercial_cooldown(lead, now=now)
        assert check.is_active is True

    def test_no_cooldown_set(self):
        lead = _make_lead(commercial_cooldown_until=None)
        check = check_commercial_cooldown(lead)
        assert check.is_active is False

    def test_cooldown_via_service(self):
        svc = LeadCaptureService()
        lead = _make_lead()
        check = svc.check_cooldown(lead)
        assert check.is_active is True


# ═══════════════════════════════════════════════════════════════════════
# AC6: Referral Attribution
# ═══════════════════════════════════════════════════════════════════════


class TestReferralAttribution:
    """AC6: User A invites User B → referred_by_user_id = User A."""

    def test_referral_tracked(self):
        lead = detect_new_member(
            telegram_user_id=99999,
            first_name="Bob",
            coach_id="coach-1",
            stream_id="stream-1",
            referred_by_user_id=12345,
        )
        assert lead.referred_by_user_id == 12345

    def test_no_referral(self):
        lead = detect_new_member(
            telegram_user_id=99999,
            first_name="Bob",
            coach_id="coach-1",
            stream_id="stream-1",
        )
        assert lead.referred_by_user_id is None

    def test_referral_via_service(self):
        svc = LeadCaptureService()
        result = svc.capture_new_member(
            telegram_user_id=99999,
            first_name="Charlie",
            coach_id="coach-1",
            stream_id="stream-1",
            referred_by_user_id=12345,
        )
        assert result.lead.referred_by_user_id == 12345


# ═══════════════════════════════════════════════════════════════════════
# Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """Receipt chain integrity for lead capture operations."""

    def test_chain_valid_after_multi_ops(self):
        svc = LeadCaptureService()
        svc.capture_new_member(12345, "Alice", "coach-1", "stream-1")
        lead = _make_lead()
        update = LeadContactUpdate(
            telegram_user_id=12345, coach_id="coach-1", phone_number="+1234567890",
        )
        svc.update_contact(lead, update)
        mappings = [{"social": 0.20}] * 3
        svc.generate_warm_start(lead, mappings)
        assert len(svc.receipt_chain) == 3
        assert svc.verify_receipt_chain() is True

    def test_empty_chain_valid(self):
        svc = LeadCaptureService()
        assert svc.verify_receipt_chain() is True

    def test_agent_name(self):
        svc = LeadCaptureService()
        svc.capture_new_member(12345, "Alice", "coach-1", "stream-1")
        assert svc.receipt_chain[0]["agent_name"] == LEAD_CAPTURE_AGENT_NAME


# ═══════════════════════════════════════════════════════════════════════
# SQL + Constants
# ═══════════════════════════════════════════════════════════════════════


class TestSQLAndConstants:
    """Verify SQL schema and constants."""

    def test_trivia_leads_sql(self):
        assert "trivia_leads" in TRIVIA_LEADS_SQL
        assert "telegram_user_id" in TRIVIA_LEADS_SQL
        assert "phone_number" in TRIVIA_LEADS_SQL
        assert "cbcs_initial_assessment" in TRIVIA_LEADS_SQL
        assert "nurture_status" in TRIVIA_LEADS_SQL
        assert "commercial_cooldown_until" in TRIVIA_LEADS_SQL

    def test_unique_index(self):
        assert "idx_trivia_leads_unique_user" in TRIVIA_LEADS_SQL

    def test_cooldown_days(self):
        assert COMMERCIAL_COOLDOWN_DAYS == 21

    def test_min_qualifying(self):
        assert MIN_QUALIFYING_RESPONSES == 3

    def test_agent_name(self):
        assert LEAD_CAPTURE_AGENT_NAME == "Marco"

    def test_nurture_statuses(self):
        statuses = [s.value for s in NurtureStatus]
        assert "new" in statuses
        assert "active" in statuses
        assert "passive" in statuses
        assert "converted" in statuses
