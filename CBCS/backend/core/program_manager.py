"""
FR-COM-04 — Program & Campaign Manager
Build Step 25 · DEP-COM-009 through DEP-COM-011

Program Registry, Campaign Manager, Funnel Page Generator,
Analytics (CBAR Q9 event-sourced funnel analytics).

CBAR Q7: Admin Override Enrollment Protocol — capacity expansion, not bypass.
CBAR Q9: analytics_events + mv_campaign_analytics (signed token validation).
"""

from __future__ import annotations

import hashlib
import random
import string
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from core.commercial_models import (
    ENROLLMENT_CODE_LENGTH,
    RECEIPT_STAGE_CAMPAIGN_LAUNCH,
    RECEIPT_STAGE_CAPACITY_OVERRIDE,
    RECEIPT_STAGE_FUNNEL_DEPLOY,
    RECEIPT_STAGE_PROGRAM_CREATE,
    AnalyticsEventRow,
    AnalyticsEventType,
    CampaignRow,
    CampaignStatus,
    CoachingProgramRow,
    ProgramRegistryError,
    ProgramStatus,
    ProgramValidationResponse,
    build_receipt,
    compute_receipt_hash,
)


# =====================================================
#  DEP-COM-009: Program Registry Service
# =====================================================

class ProgramRegistryService:
    """
    § 4 Stage 1 + Stage 4: Program creation, code management,
    and registry API for FR-COM-03 consumption.
    """

    def __init__(self) -> None:
        self._programs: dict[str, CoachingProgramRow] = {}  # keyed by program_id
        self._codes_index: dict[str, str] = {}  # enrollment_code → program_id
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def _generate_code(self, prefix: str = "") -> str:
        """
        § 4 Stage 1: Auto-generate 8-char alphanumeric enrollment code.
        Guaranteed unique across the platform.
        """
        for _ in range(1000):
            chars = string.ascii_uppercase + string.digits
            suffix_len = ENROLLMENT_CODE_LENGTH - len(prefix)
            if suffix_len <= 0:
                suffix_len = ENROLLMENT_CODE_LENGTH
                prefix = ""
            code = prefix + "".join(random.choices(chars, k=suffix_len))
            code = code[:ENROLLMENT_CODE_LENGTH]
            if code not in self._codes_index:
                return code
        raise ProgramRegistryError(
            code="CODE_GENERATION_EXHAUSTED",
            message="Failed to generate unique code after 1000 attempts.",
        )

    def create_program(
        self,
        coach_id: str,
        program_name: str,
        description: str,
        duration_days: int,
        check_in_schedule: list[str],
        max_clients: int = 30,
        client_price_display: str | None = None,
        custom_code: str | None = None,
        intake_fields: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> CoachingProgramRow:
        """
        § 4 Stage 1: Create a coaching program with auto-generated code.
        Coach can override with a custom code (validated for uniqueness).
        """
        # ADR-01: coach_id scope validation
        if not coach_id or len(coach_id) < 2:
            raise ProgramRegistryError(
                code="INVALID_COACH_ID",
                message="Coach ID must be at least 2 characters.",
            )

        # Code uniqueness validation
        if custom_code:
            if custom_code in self._codes_index:
                raise ProgramRegistryError(
                    code="CODE_ALREADY_EXISTS",
                    message=f"Code '{custom_code}' is already in use.",
                )
            enrollment_code = custom_code
        else:
            # Auto-generate from program name prefix
            prefix = "".join(
                c for c in program_name[:4].upper() if c.isalnum()
            )
            enrollment_code = self._generate_code(prefix)

        program = CoachingProgramRow(
            coach_id=coach_id,
            program_name=program_name,
            description=description,
            duration_days=duration_days,
            check_in_schedule=check_in_schedule,
            max_clients=max_clients,
            client_price_display=client_price_display,
            enrollment_code=enrollment_code,
            intake_fields=intake_fields or ["first_name", "primary_goal"],
            start_date=start_date,
            end_date=end_date,
            status=ProgramStatus.ENROLLING,
        )

        self._programs[program.id] = program
        self._codes_index[enrollment_code] = program.id

        # Receipt Chain Guard (DEP-ENG-041)
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_PROGRAM_CREATE,
            agent_name="program_registry",
            input_payload={
                "coach_id": coach_id,
                "program_name": program_name,
                "enrollment_code": enrollment_code,
            },
            output_payload={
                "program_id": program.id,
                "status": program.status.value,
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        program.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return program

    def validate_code(self, code: str) -> ProgramValidationResponse:
        """
        § 4 Stage 4: Program Registry API — consumed by FR-COM-03.
        POST /api/programs/validate-code
        """
        if code not in self._codes_index:
            return ProgramValidationResponse(
                valid=False,
                reason="CODE_NOT_FOUND",
            )

        program_id = self._codes_index[code]
        program = self._programs.get(program_id)

        if program is None:
            return ProgramValidationResponse(
                valid=False,
                reason="CODE_NOT_FOUND",
            )

        # Check program expiration
        if program.end_date:
            try:
                end = datetime.strptime(program.end_date, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                if datetime.now(timezone.utc) > end:
                    return ProgramValidationResponse(
                        valid=False,
                        reason="PROGRAM_EXPIRED",
                    )
            except ValueError:
                pass

        # Check program status
        if program.status in (ProgramStatus.COMPLETED, ProgramStatus.ARCHIVED):
            return ProgramValidationResponse(
                valid=False,
                reason="PROGRAM_EXPIRED",
            )

        if program.status == ProgramStatus.DRAFT:
            return ProgramValidationResponse(
                valid=False,
                reason="CAMPAIGN_PAUSED",
            )

        # Check capacity
        if program.available_capacity <= 0:
            return ProgramValidationResponse(
                valid=False,
                reason="PROGRAM_FULL",
            )

        return ProgramValidationResponse(
            valid=True,
            coach_id=program.coach_id,
            program_id=program.id,
            program_name=program.program_name,
            available_capacity=program.available_capacity,
            intake_fields=program.intake_fields,
            check_in_schedule=program.check_in_schedule,
            status=program.status.value,
        )

    def increment_enrollment(self, program_id: str) -> int:
        """Increment current_enrolled after successful enrollment."""
        program = self._programs.get(program_id)
        if program is None:
            raise ProgramRegistryError(
                code="PROGRAM_NOT_FOUND",
                message=f"Program {program_id} not found.",
            )
        program.current_enrolled += 1
        program.updated_at = datetime.now(timezone.utc)
        return program.current_enrolled

    def decrement_enrollment(self, program_id: str) -> int:
        """Decrement current_enrolled on client drop."""
        program = self._programs.get(program_id)
        if program is None:
            raise ProgramRegistryError(
                code="PROGRAM_NOT_FOUND",
                message=f"Program {program_id} not found.",
            )
        program.current_enrolled = max(0, program.current_enrolled - 1)
        program.updated_at = datetime.now(timezone.utc)
        return program.current_enrolled

    def apply_capacity_override(
        self,
        program_id: str,
        admin_user_id: str,
    ) -> CoachingProgramRow:
        """
        CBAR Q7: Admin Override Enrollment Protocol.
        NOT a bypass — structured expansion: increment max_clients by 1.
        """
        program = self._programs.get(program_id)
        if program is None:
            raise ProgramRegistryError(
                code="PROGRAM_NOT_FOUND",
                message=f"Program {program_id} not found.",
            )

        program.max_clients += 1
        program.updated_at = datetime.now(timezone.utc)

        # Receipt Chain Guard (DEP-ENG-041)
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_CAPACITY_OVERRIDE,
            agent_name="program_registry",
            input_payload={
                "program_id": program_id,
                "admin_user_id": admin_user_id,
                "previous_max": program.max_clients - 1,
            },
            output_payload={
                "new_max_clients": program.max_clients,
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return program

    def transition_status(
        self,
        program_id: str,
        new_status: ProgramStatus,
    ) -> CoachingProgramRow:
        """
        § 10 Testing: Status transitions validation.
        Valid: draft → enrolling → active → completed → archived.
        """
        program = self._programs.get(program_id)
        if program is None:
            raise ProgramRegistryError(
                code="PROGRAM_NOT_FOUND",
                message=f"Program {program_id} not found.",
            )

        valid_transitions: dict[ProgramStatus, list[ProgramStatus]] = {
            ProgramStatus.DRAFT: [ProgramStatus.ENROLLING],
            ProgramStatus.ENROLLING: [ProgramStatus.ACTIVE, ProgramStatus.ARCHIVED],
            ProgramStatus.ACTIVE: [ProgramStatus.COMPLETED],
            ProgramStatus.COMPLETED: [ProgramStatus.ARCHIVED],
            ProgramStatus.ARCHIVED: [],
        }

        allowed = valid_transitions.get(program.status, [])
        if new_status not in allowed:
            raise ProgramRegistryError(
                code="INVALID_STATUS_TRANSITION",
                message=f"Cannot transition from {program.status.value} to {new_status.value}.",
            )

        program.status = new_status
        program.updated_at = datetime.now(timezone.utc)
        return program

    def get_program(self, program_id: str) -> CoachingProgramRow | None:
        return self._programs.get(program_id)

    def get_programs_by_coach(self, coach_id: str) -> list[CoachingProgramRow]:
        """ADR-01: Coach sees only own programs (RLS equivalent)."""
        return [p for p in self._programs.values() if p.coach_id == coach_id]

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  DEP-COM-010: Campaign Manager
# =====================================================

class CampaignManager:
    """
    § 4 Stage 2 + Stage 3: Campaign creation, funnel URL generation,
    Telegram bot link generation, campaign analytics.
    """

    def __init__(
        self,
        program_registry: ProgramRegistryService,
    ) -> None:
        self._program_registry = program_registry
        self._campaigns: dict[str, CampaignRow] = {}
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def create_campaign(
        self,
        coach_id: str,
        program_id: str,
        campaign_name: str,
        enrollment_code_override: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> CampaignRow:
        """
        § 4 Stage 2: Create campaign linked to a program.
        Auto-generates funnel URL and Telegram bot link.
        """
        # ADR-01: coach_id scope
        if not coach_id or len(coach_id) < 2:
            raise ProgramRegistryError(
                code="INVALID_COACH_ID",
                message="Coach ID must be at least 2 characters.",
            )

        program = self._program_registry.get_program(program_id)
        if program is None:
            raise ProgramRegistryError(
                code="PROGRAM_NOT_FOUND",
                message=f"Program {program_id} not found.",
            )

        # RLS: coach can only create campaigns for own programs
        if program.coach_id != coach_id:
            raise ProgramRegistryError(
                code="CROSS_TENANT_VIOLATION",
                message="Cannot create campaign for another coach's program.",
            )

        # Resolve enrollment code
        code = enrollment_code_override or program.enrollment_code
        if enrollment_code_override:
            # Validate code override uniqueness
            validation = self._program_registry.validate_code(enrollment_code_override)
            if validation.valid and validation.program_id != program_id:
                raise ProgramRegistryError(
                    code="CODE_ALREADY_EXISTS",
                    message=f"Code '{enrollment_code_override}' belongs to another program.",
                )

        # Auto-generate URLs
        slug = campaign_name.lower().replace(" ", "-")[:30]
        funnel_url = f"https://conscious.co/{coach_id[:8]}/{slug}"
        telegram_bot_link = f"https://t.me/ccp_bot?start={code}"
        funnel_s3_path = f"funnels/{coach_id}/{slug}/index.html"

        campaign = CampaignRow(
            coach_id=coach_id,
            program_id=program_id,
            campaign_name=campaign_name,
            enrollment_code_override=enrollment_code_override,
            funnel_url=funnel_url,
            funnel_s3_path=funnel_s3_path,
            telegram_bot_link=telegram_bot_link,
            start_date=start_date,
            end_date=end_date,
            status=CampaignStatus.DRAFT,
        )

        self._campaigns[campaign.id] = campaign

        # Receipt Chain Guard (DEP-ENG-041)
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_CAMPAIGN_LAUNCH,
            agent_name="campaign_manager",
            input_payload={
                "coach_id": coach_id,
                "program_id": program_id,
                "campaign_name": campaign_name,
            },
            output_payload={
                "campaign_id": campaign.id,
                "funnel_url": funnel_url,
                "telegram_bot_link": telegram_bot_link,
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        campaign.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return campaign

    def launch_campaign(self, campaign_id: str) -> CampaignRow:
        """Set campaign status to 'live'."""
        campaign = self._campaigns.get(campaign_id)
        if campaign is None:
            raise ProgramRegistryError(
                code="CAMPAIGN_NOT_FOUND",
                message=f"Campaign {campaign_id} not found.",
            )
        campaign.status = CampaignStatus.LIVE
        campaign.updated_at = datetime.now(timezone.utc)
        return campaign

    def pause_campaign(self, campaign_id: str) -> CampaignRow:
        """Pause a live campaign → registry returns CAMPAIGN_PAUSED."""
        campaign = self._campaigns.get(campaign_id)
        if campaign is None:
            raise ProgramRegistryError(
                code="CAMPAIGN_NOT_FOUND",
                message=f"Campaign {campaign_id} not found.",
            )
        campaign.status = CampaignStatus.PAUSED
        campaign.updated_at = datetime.now(timezone.utc)
        return campaign

    def get_campaign(self, campaign_id: str) -> CampaignRow | None:
        return self._campaigns.get(campaign_id)

    def get_campaigns_by_coach(self, coach_id: str) -> list[CampaignRow]:
        """ADR-01: Coach sees only own campaigns."""
        return [c for c in self._campaigns.values() if c.coach_id == coach_id]

    def check_campaign_paused(self, enrollment_code: str) -> bool:
        """Check if any campaign using this code is paused."""
        for campaign in self._campaigns.values():
            if campaign.enrollment_code_override == enrollment_code:
                if campaign.status == CampaignStatus.PAUSED:
                    return True
        return False

    def record_enrollment(self, campaign_id: str) -> None:
        """Increment enrollment count after successful onboarding."""
        campaign = self._campaigns.get(campaign_id)
        if campaign:
            campaign.total_enrollments += 1
            if campaign.total_funnel_views > 0:
                campaign.conversion_rate = (
                    campaign.total_enrollments / campaign.total_funnel_views
                )
            campaign.updated_at = datetime.now(timezone.utc)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  DEP-COM-011: Funnel Page Generator
# =====================================================

class FunnelPageGenerator:
    """
    § 4 Stage 3: Static HTML page generator for campaigns.
    Generates branded one-pager deployed to S3/CloudFront.
    """

    def __init__(self) -> None:
        self._deployed_funnels: list[dict[str, Any]] = []
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def generate_funnel_html(
        self,
        coach_name: str,
        program_name: str,
        description: str,
        telegram_bot_link: str,
        client_price_display: str | None = None,
        brand_color: str = "#6366f1",
    ) -> str:
        """
        § 4 Stage 3: Generate static HTML for funnel page.
        Mobile-responsive single-page design.
        """
        price_section = ""
        if client_price_display:
            price_section = f'<p class="price">{client_price_display}</p>'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{program_name} — {coach_name}</title>
<style>
  body {{ font-family: 'Inter', sans-serif; max-width: 600px; margin: 0 auto; padding: 2rem; background: #0f172a; color: #e2e8f0; }}
  h1 {{ color: {brand_color}; }}
  .cta {{ display: inline-block; padding: 1rem 2rem; background: {brand_color}; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 1.5rem; }}
</style>
</head>
<body>
  <h1>{program_name}</h1>
  <p>with {coach_name}</p>
  <p>{description}</p>
  {price_section}
  <a href="{telegram_bot_link}" class="cta">Join via Telegram</a>
</body>
</html>"""

    def deploy_funnel(
        self,
        campaign_id: str,
        coach_id: str,
        s3_path: str,
        html_content: str,
    ) -> dict[str, Any]:
        """
        Deploy generated HTML to S3 (simulated).
        In production, uploads to S3 + invalidates CloudFront.
        """
        deployment = {
            "campaign_id": campaign_id,
            "coach_id": coach_id,
            "s3_path": s3_path,
            "content_length": len(html_content),
            "deployed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._deployed_funnels.append(deployment)

        # Receipt Chain Guard (DEP-ENG-041)
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_FUNNEL_DEPLOY,
            agent_name="funnel_page_generator",
            input_payload={"campaign_id": campaign_id, "s3_path": s3_path},
            output_payload=deployment,
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return deployment

    def get_deployed_funnels(self) -> list[dict[str, Any]]:
        return list(self._deployed_funnels)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  CBAR Q9: Analytics Event Service
# =====================================================

class AnalyticsService:
    """
    CBAR Q9: Event-sourced funnel analytics.
    Tracks funnel_view, telegram_click, enrollment_complete
    via analytics_events table with signed token validation.
    """

    def __init__(self, signing_secret: str = "default-secret") -> None:
        self._events: list[AnalyticsEventRow] = []
        self._signing_secret = signing_secret

    def _validate_token(self, campaign_id: str, token_hash: str) -> bool:
        """Validate signed campaign token at edge function level."""
        expected = hashlib.sha256(
            f"{campaign_id}:{self._signing_secret}".encode()
        ).hexdigest()
        return token_hash == expected

    def generate_token(self, campaign_id: str) -> str:
        """Generate signed token for a campaign."""
        return hashlib.sha256(
            f"{campaign_id}:{self._signing_secret}".encode()
        ).hexdigest()

    def record_event(
        self,
        event_type: AnalyticsEventType,
        campaign_id: str,
        coach_id: str,
        signed_token_hash: str,
        metadata: dict[str, Any] | None = None,
    ) -> AnalyticsEventRow | None:
        """
        Record an analytics event. Validates signed token.
        Returns None if token is invalid (anti-abuse).
        """
        if not self._validate_token(campaign_id, signed_token_hash):
            return None

        event = AnalyticsEventRow(
            event_type=event_type,
            campaign_id=campaign_id,
            coach_id=coach_id,
            signed_token_hash=signed_token_hash,
            metadata=metadata,
        )
        self._events.append(event)
        return event

    def get_events_by_campaign(self, campaign_id: str) -> list[AnalyticsEventRow]:
        return [e for e in self._events if e.campaign_id == campaign_id]

    def get_events_by_coach(self, coach_id: str) -> list[AnalyticsEventRow]:
        """ADR-01: Coach sees own analytics events (RLS equivalent)."""
        return [e for e in self._events if e.coach_id == coach_id]

    def get_platform_aggregates(self) -> dict[str, int]:
        """
        CBAR Q9: mv_campaign_analytics equivalent.
        coach_id stripped — only platform-level counts.
        """
        aggregates: dict[str, int] = {
            "total_funnel_views": 0,
            "total_telegram_clicks": 0,
            "total_enrollments": 0,
        }
        for event in self._events:
            if event.event_type == AnalyticsEventType.FUNNEL_VIEW:
                aggregates["total_funnel_views"] += 1
            elif event.event_type == AnalyticsEventType.TELEGRAM_CLICK:
                aggregates["total_telegram_clicks"] += 1
            elif event.event_type == AnalyticsEventType.ENROLLMENT_COMPLETE:
                aggregates["total_enrollments"] += 1
        return aggregates
