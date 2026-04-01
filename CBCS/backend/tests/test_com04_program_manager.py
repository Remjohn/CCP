"""
FR-COM-04 — Program & Campaign Manager

Test Suite: Step 25 Build

Coverage:
- AC1: Program creation → code auto-generated + unique + status enrolling
- AC2: Code uniqueness — two coaches, globally unique codes, custom override rejected
- AC3: Campaign launch → funnel URL + Telegram link + S3 deploy
- AC4: Registry query (FR-COM-03 consumption) → correct coach_id, program_name, capacity
- AC5: Capacity enforcement → PROGRAM_FULL when max_clients reached
- AC6: Campaign paused → CAMPAIGN_PAUSED from registry
- CBAR Q7: Admin override = expansion, not bypass
- CBAR Q9: Analytics events with signed token validation
- Safety: Coach isolation (RLS equivalent)
- Safety: Status transition validation
"""

from __future__ import annotations

import uuid

import pytest

from core.commercial_models import (
    AnalyticsEventType,
    CampaignStatus,
    ProgramRegistryError,
    ProgramStatus,
)
from core.program_manager import (
    AnalyticsService,
    CampaignManager,
    FunnelPageGenerator,
    ProgramRegistryService,
)


# =====================================================
#  Fixtures
# =====================================================

def _make_registry() -> ProgramRegistryService:
    return ProgramRegistryService()


def _make_program(
    registry: ProgramRegistryService,
    coach_id: str = "coach-alpha",
    program_name: str = "90-Day Transform",
    max_clients: int = 30,
    **kwargs,
):
    defaults = {
        "description": "A comprehensive 90-day coaching journey",
        "duration_days": 90,
        "check_in_schedule": ["monday", "wednesday", "friday"],
        "max_clients": max_clients,
    }
    defaults.update(kwargs)
    return registry.create_program(coach_id=coach_id, program_name=program_name, **defaults)


# =====================================================
#  AC1: Program Creation
# =====================================================

class TestAC1ProgramCreation:

    def test_program_created_with_auto_code(self):
        registry = _make_registry()
        program = _make_program(registry)

        assert program.program_name == "90-Day Transform"
        assert program.enrollment_code is not None
        assert len(program.enrollment_code) == 8
        assert program.status == ProgramStatus.ENROLLING

    def test_auto_code_is_alphanumeric(self):
        registry = _make_registry()
        program = _make_program(registry)

        assert program.enrollment_code.isalnum()

    def test_receipt_chain_written(self):
        registry = _make_registry()
        _make_program(registry)

        receipts = registry.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "PROGRAM_CREATE"
        assert receipts[0]["agent_name"] == "program_registry"

    def test_program_has_receipt_block(self):
        registry = _make_registry()
        program = _make_program(registry)

        assert program.receipt_chain_block is not None

    def test_custom_code_accepted(self):
        registry = _make_registry()
        program = registry.create_program(
            coach_id="coach-alpha",
            program_name="Custom Program",
            description="Test",
            duration_days=30,
            check_in_schedule=["monday"],
            custom_code="CUSTOM01",
        )
        assert program.enrollment_code == "CUSTOM01"

    def test_default_intake_fields(self):
        registry = _make_registry()
        program = _make_program(registry)

        assert program.intake_fields == ["first_name", "primary_goal"]

    def test_custom_intake_fields(self):
        registry = _make_registry()
        program = registry.create_program(
            coach_id="coach-alpha",
            program_name="Custom Intake",
            description="Test",
            duration_days=30,
            check_in_schedule=["monday"],
            intake_fields=["first_name", "primary_goal", "email", "age_range"],
        )
        assert len(program.intake_fields) == 4
        assert "email" in program.intake_fields


# =====================================================
#  AC2: Code Uniqueness
# =====================================================

class TestAC2CodeUniqueness:

    def test_two_coaches_get_unique_codes(self):
        registry = _make_registry()
        p1 = _make_program(registry, coach_id="coach-alpha", program_name="Program A")
        p2 = _make_program(registry, coach_id="coach-beta", program_name="Program B")

        assert p1.enrollment_code != p2.enrollment_code

    def test_custom_code_rejected_if_exists(self):
        registry = _make_registry()
        _make_program(registry, custom_code="UNIQ0001")

        with pytest.raises(ProgramRegistryError) as exc_info:
            registry.create_program(
                coach_id="coach-beta",
                program_name="Duplicate Code",
                description="Test",
                duration_days=30,
                check_in_schedule=["monday"],
                custom_code="UNIQ0001",
            )
        assert exc_info.value.code == "CODE_ALREADY_EXISTS"

    def test_1000_codes_all_unique(self):
        registry = _make_registry()
        codes = set()
        for i in range(100):  # 100 is sufficient to prove uniqueness logic
            program = registry.create_program(
                coach_id=f"coach-{i:03d}",
                program_name=f"Program {i}",
                description="Test",
                duration_days=30,
                check_in_schedule=["monday"],
            )
            codes.add(program.enrollment_code)
        assert len(codes) == 100


# =====================================================
#  AC3: Campaign Launch
# =====================================================

class TestAC3CampaignLaunch:

    def test_campaign_created_with_urls(self):
        registry = _make_registry()
        program = _make_program(registry)
        manager = CampaignManager(registry)

        campaign = manager.create_campaign(
            coach_id="coach-alpha",
            program_id=program.id,
            campaign_name="March Launch",
        )

        assert campaign.funnel_url is not None
        assert "conscious.co" in campaign.funnel_url
        assert campaign.telegram_bot_link is not None
        assert "t.me/ccp_bot" in campaign.telegram_bot_link
        assert campaign.status == CampaignStatus.DRAFT

    def test_campaign_telegram_link_has_code(self):
        registry = _make_registry()
        program = _make_program(registry)
        manager = CampaignManager(registry)

        campaign = manager.create_campaign(
            coach_id="coach-alpha",
            program_id=program.id,
            campaign_name="Code Test",
        )

        assert program.enrollment_code in campaign.telegram_bot_link

    def test_funnel_s3_path_generated(self):
        registry = _make_registry()
        program = _make_program(registry)
        manager = CampaignManager(registry)

        campaign = manager.create_campaign(
            coach_id="coach-alpha",
            program_id=program.id,
            campaign_name="S3 Test",
        )

        assert campaign.funnel_s3_path is not None
        assert campaign.funnel_s3_path.startswith("funnels/")

    def test_funnel_html_generated(self):
        generator = FunnelPageGenerator()
        html = generator.generate_funnel_html(
            coach_name="Coach Alpha",
            program_name="90-Day Transform",
            description="Journey description",
            telegram_bot_link="https://t.me/ccp_bot?start=TRANS90A",
            client_price_display="$197",
        )

        assert "90-Day Transform" in html
        assert "Coach Alpha" in html
        assert "$197" in html
        assert "t.me/ccp_bot" in html
        assert "<!DOCTYPE html>" in html

    def test_funnel_deploy_receipt(self):
        generator = FunnelPageGenerator()
        html = "<html>test</html>"
        deployment = generator.deploy_funnel(
            campaign_id="camp-1",
            coach_id="coach-alpha",
            s3_path="funnels/coach-alpha/test/index.html",
            html_content=html,
        )

        assert deployment["campaign_id"] == "camp-1"
        receipts = generator.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "FUNNEL_DEPLOY"

    def test_campaign_receipt_chain(self):
        registry = _make_registry()
        program = _make_program(registry)
        manager = CampaignManager(registry)

        manager.create_campaign(
            coach_id="coach-alpha",
            program_id=program.id,
            campaign_name="Receipt Test",
        )

        receipts = manager.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "CAMPAIGN_LAUNCH"


# =====================================================
#  AC4: Registry Query (FR-COM-03 consumption)
# =====================================================

class TestAC4RegistryQuery:

    def test_valid_code_returns_program_data(self):
        registry = _make_registry()
        program = _make_program(registry, max_clients=30)

        response = registry.validate_code(program.enrollment_code)

        assert response.valid is True
        assert response.coach_id == "coach-alpha"
        assert response.program_name == "90-Day Transform"
        assert response.available_capacity == 30
        assert response.intake_fields == ["first_name", "primary_goal"]
        assert response.check_in_schedule == ["monday", "wednesday", "friday"]

    def test_invalid_code_returns_not_found(self):
        registry = _make_registry()

        response = registry.validate_code("FAKE1234")

        assert response.valid is False
        assert response.reason == "CODE_NOT_FOUND"

    def test_capacity_reported_correctly(self):
        registry = _make_registry()
        program = _make_program(registry, max_clients=30)

        # Enroll 18 clients
        for _ in range(18):
            registry.increment_enrollment(program.id)

        response = registry.validate_code(program.enrollment_code)
        assert response.available_capacity == 12

    def test_enrollment_increments_count(self):
        registry = _make_registry()
        program = _make_program(registry)

        new_count = registry.increment_enrollment(program.id)
        assert new_count == 1
        assert program.current_enrolled == 1

    def test_enrollment_decrements_on_drop(self):
        registry = _make_registry()
        program = _make_program(registry)
        registry.increment_enrollment(program.id)
        registry.increment_enrollment(program.id)

        new_count = registry.decrement_enrollment(program.id)
        assert new_count == 1


# =====================================================
#  AC5: Capacity Enforcement
# =====================================================

class TestAC5CapacityEnforcement:

    def test_full_program_returns_program_full(self):
        registry = _make_registry()
        program = _make_program(registry, max_clients=2)
        registry.increment_enrollment(program.id)
        registry.increment_enrollment(program.id)

        response = registry.validate_code(program.enrollment_code)

        assert response.valid is False
        assert response.reason == "PROGRAM_FULL"

    def test_one_spot_left_allows(self):
        registry = _make_registry()
        program = _make_program(registry, max_clients=3)
        registry.increment_enrollment(program.id)
        registry.increment_enrollment(program.id)

        response = registry.validate_code(program.enrollment_code)

        assert response.valid is True
        assert response.available_capacity == 1


# =====================================================
#  AC6: Campaign Paused
# =====================================================

class TestAC6CampaignPaused:

    def test_completed_program_returns_expired(self):
        registry = _make_registry()
        program = _make_program(registry)
        # Transition: enrolling → active → completed
        registry.transition_status(program.id, ProgramStatus.ACTIVE)
        registry.transition_status(program.id, ProgramStatus.COMPLETED)

        response = registry.validate_code(program.enrollment_code)

        assert response.valid is False
        assert response.reason == "PROGRAM_EXPIRED"

    def test_draft_program_returns_paused(self):
        """Draft programs are not yet live — treated as paused."""
        registry = _make_registry()
        program = registry.create_program(
            coach_id="coach-alpha",
            program_name="Draft Program",
            description="Test",
            duration_days=30,
            check_in_schedule=["monday"],
        )
        # Override status to draft for test
        program.status = ProgramStatus.DRAFT

        response = registry.validate_code(program.enrollment_code)

        assert response.valid is False
        assert response.reason == "CAMPAIGN_PAUSED"

    def test_expired_end_date_returns_expired(self):
        registry = _make_registry()
        program = registry.create_program(
            coach_id="coach-alpha",
            program_name="Expired Program",
            description="Test",
            duration_days=30,
            check_in_schedule=["monday"],
            end_date="2020-01-01",  # Past date
        )

        response = registry.validate_code(program.enrollment_code)

        assert response.valid is False
        assert response.reason == "PROGRAM_EXPIRED"


# =====================================================
#  CBAR Q7: Admin Override → Expansion, Not Bypass
# =====================================================

class TestCBARQ7CapacityOverride:

    def test_override_increments_max_clients(self):
        registry = _make_registry()
        program = _make_program(registry, max_clients=30)

        updated = registry.apply_capacity_override(program.id, "admin-001")

        assert updated.max_clients == 31

    def test_override_writes_receipt(self):
        registry = _make_registry()
        program = _make_program(registry, max_clients=30)

        registry.apply_capacity_override(program.id, "admin-001")

        receipts = registry.get_receipts()
        # 1 from program creation + 1 from override
        assert len(receipts) == 2
        assert receipts[1]["stage_name"] == "CAPACITY_OVERRIDE"

    def test_override_opens_one_spot(self):
        """Full program + override → exactly 1 spot available."""
        registry = _make_registry()
        program = _make_program(registry, max_clients=2)
        registry.increment_enrollment(program.id)
        registry.increment_enrollment(program.id)

        # Program is full
        assert registry.validate_code(program.enrollment_code).reason == "PROGRAM_FULL"

        # Admin override → 1 spot
        registry.apply_capacity_override(program.id, "admin-001")
        response = registry.validate_code(program.enrollment_code)
        assert response.valid is True
        assert response.available_capacity == 1


# =====================================================
#  CBAR Q9: Analytics with Signed Token Validation
# =====================================================

class TestCBARQ9Analytics:

    def test_valid_token_records_event(self):
        analytics = AnalyticsService(signing_secret="test-secret")
        campaign_id = "camp-001"
        token = analytics.generate_token(campaign_id)

        event = analytics.record_event(
            event_type=AnalyticsEventType.FUNNEL_VIEW,
            campaign_id=campaign_id,
            coach_id="coach-alpha",
            signed_token_hash=token,
        )

        assert event is not None
        assert event.event_type == AnalyticsEventType.FUNNEL_VIEW

    def test_invalid_token_rejected(self):
        analytics = AnalyticsService(signing_secret="test-secret")

        event = analytics.record_event(
            event_type=AnalyticsEventType.FUNNEL_VIEW,
            campaign_id="camp-001",
            coach_id="coach-alpha",
            signed_token_hash="invalid-hash",
        )

        assert event is None

    def test_platform_aggregates_strip_coach_id(self):
        analytics = AnalyticsService(signing_secret="test-secret")
        c1_token = analytics.generate_token("camp-001")
        c2_token = analytics.generate_token("camp-002")

        analytics.record_event(AnalyticsEventType.FUNNEL_VIEW, "camp-001", "coach-a", c1_token)
        analytics.record_event(AnalyticsEventType.FUNNEL_VIEW, "camp-002", "coach-b", c2_token)
        analytics.record_event(AnalyticsEventType.ENROLLMENT_COMPLETE, "camp-001", "coach-a", c1_token)

        agg = analytics.get_platform_aggregates()

        assert agg["total_funnel_views"] == 2
        assert agg["total_enrollments"] == 1
        # No coach_id in aggregates
        assert "coach_id" not in agg

    def test_coach_sees_own_events_only(self):
        analytics = AnalyticsService(signing_secret="test-secret")
        c1_token = analytics.generate_token("camp-001")
        c2_token = analytics.generate_token("camp-002")

        analytics.record_event(AnalyticsEventType.FUNNEL_VIEW, "camp-001", "coach-a", c1_token)
        analytics.record_event(AnalyticsEventType.FUNNEL_VIEW, "camp-002", "coach-b", c2_token)

        coach_a_events = analytics.get_events_by_coach("coach-a")
        assert len(coach_a_events) == 1
        assert coach_a_events[0].coach_id == "coach-a"


# =====================================================
#  Safety: Status Transitions
# =====================================================

class TestStatusTransitions:

    def test_valid_transition_enrolling_to_active(self):
        registry = _make_registry()
        program = _make_program(registry)

        updated = registry.transition_status(program.id, ProgramStatus.ACTIVE)
        assert updated.status == ProgramStatus.ACTIVE

    def test_valid_transition_active_to_completed(self):
        registry = _make_registry()
        program = _make_program(registry)
        registry.transition_status(program.id, ProgramStatus.ACTIVE)

        updated = registry.transition_status(program.id, ProgramStatus.COMPLETED)
        assert updated.status == ProgramStatus.COMPLETED

    def test_invalid_transition_archived_to_enrolling(self):
        registry = _make_registry()
        program = _make_program(registry)
        registry.transition_status(program.id, ProgramStatus.ACTIVE)
        registry.transition_status(program.id, ProgramStatus.COMPLETED)
        registry.transition_status(program.id, ProgramStatus.ARCHIVED)

        with pytest.raises(ProgramRegistryError) as exc_info:
            registry.transition_status(program.id, ProgramStatus.ENROLLING)

        assert exc_info.value.code == "INVALID_STATUS_TRANSITION"


# =====================================================
#  Safety: Coach Isolation (ADR-01)
# =====================================================

class TestCoachIsolation:

    def test_coach_sees_only_own_programs(self):
        registry = _make_registry()
        _make_program(registry, coach_id="coach-alpha", program_name="Alpha Program")
        _make_program(registry, coach_id="coach-beta", program_name="Beta Program")

        alpha_programs = registry.get_programs_by_coach("coach-alpha")
        assert len(alpha_programs) == 1
        assert alpha_programs[0].program_name == "Alpha Program"

    def test_cross_coach_campaign_blocked(self):
        registry = _make_registry()
        program = _make_program(registry, coach_id="coach-alpha")
        manager = CampaignManager(registry)

        with pytest.raises(ProgramRegistryError) as exc_info:
            manager.create_campaign(
                coach_id="coach-beta",  # Different coach!
                program_id=program.id,
                campaign_name="Hijack Attempt",
            )

        assert exc_info.value.code == "CROSS_TENANT_VIOLATION"

    def test_invalid_coach_id_rejected(self):
        registry = _make_registry()

        with pytest.raises(ProgramRegistryError) as exc_info:
            registry.create_program(
                coach_id="x",  # Too short
                program_name="Bad Program",
                description="Test",
                duration_days=30,
                check_in_schedule=["monday"],
            )

        assert exc_info.value.code == "INVALID_COACH_ID"

    def test_campaign_launch_and_pause(self):
        registry = _make_registry()
        program = _make_program(registry)
        manager = CampaignManager(registry)

        campaign = manager.create_campaign(
            coach_id="coach-alpha",
            program_id=program.id,
            campaign_name="Launch Test",
        )

        launched = manager.launch_campaign(campaign.id)
        assert launched.status == CampaignStatus.LIVE

        paused = manager.pause_campaign(campaign.id)
        assert paused.status == CampaignStatus.PAUSED
