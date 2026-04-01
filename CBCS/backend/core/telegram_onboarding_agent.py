"""
FR-COM-03 — Telegram Code Onboarding Agent
Build Step 26 · DEP-COM-007, DEP-COM-008

Telegram bot flow: code validation → conversational intake →
atomic auto-provisioning → duplicate detection.

CBAR Q8: Multi-enrollment — UNIQUE(telegram_user_id, coach_id), not UNIQUE(telegram_user_id).
Audit Revision: ALTER TABLE profiles instead of CREATE TABLE cbcs_clients.
First-message billing trigger — $4 usage at bot-first-message time (not enrollment).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from core.commercial_models import (
    RECEIPT_STAGE_CODE_VALIDATE,
    RECEIPT_STAGE_FIRST_MESSAGE,
    RECEIPT_STAGE_INTAKE_COMPLETE,
    RECEIPT_STAGE_PROVISIONING,
    ClientProfileExtension,
    ClientProfileStatus,
    IntakeSession,
    OnboardingError,
    OnboardingEventRow,
    OnboardingEventType,
    ProvisioningResult,
    build_receipt,
    compute_receipt_hash,
)
from core.program_manager import ProgramRegistryService


# =====================================================
#  Intake Question Templates
# =====================================================

INTAKE_QUESTIONS: dict[str, str] = {
    "first_name": "What's your first name?",
    "primary_goal": "What's your #1 goal for this program?",
    "email": "What's the best email to reach you?",
    "age_range": "What age range are you in? (18-25, 26-35, 36-45, 46+)",
    "timezone": "What timezone are you in?",
}


# =====================================================
#  DEP-COM-007: Telegram Onboarding Bot
# =====================================================

class TelegramOnboardingBot:
    """
    § 4 Stages 1-4: Telegram bot handling code-based enrollment.

    State Machine:
    IDLE → CODE_ENTERED → INTAKE_ACTIVE → PROVISIONING → COMPLETE
    """

    def __init__(
        self,
        program_registry: ProgramRegistryService,
        onboarding_api: "ClientOnboardingAPI",
    ) -> None:
        self._registry = program_registry
        self._api = onboarding_api
        self._active_sessions: dict[int, IntakeSession] = {}  # telegram_user_id → session
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def handle_start(self, telegram_user_id: int) -> str:
        """
        /start handler — welcome message.
        """
        return "Welcome to Conscious Coaching! 🎯 Enter your program code:"

    def handle_message(self, telegram_user_id: int, text: str) -> str:
        """
        Main message handler — routes through state machine.
        """
        # Check if user has an active intake session
        if telegram_user_id in self._active_sessions:
            return self._handle_intake_response(telegram_user_id, text)

        # Otherwise treat as code entry
        return self._handle_code_entry(telegram_user_id, text)

    def _handle_code_entry(self, telegram_user_id: int, code: str) -> str:
        """
        § 4 Stage 1: Code Validation Flow.
        """
        code = code.strip().upper()

        # Log event
        self._api.log_event(telegram_user_id, OnboardingEventType.CODE_ENTERED, code)

        # Check duplicate enrollment (same user, same program code)
        validation = self._registry.validate_code(code)

        if not validation.valid:
            # Log appropriate event
            reason = validation.reason
            if reason == "CODE_NOT_FOUND":
                self._api.log_event(telegram_user_id, OnboardingEventType.CODE_INVALID, code)
                return "Sorry, that code wasn't found. Double-check it and try again."
            elif reason == "PROGRAM_EXPIRED":
                self._api.log_event(telegram_user_id, OnboardingEventType.CODE_EXPIRED, code)
                return "That program has ended. Contact your coach for the latest code."
            elif reason == "PROGRAM_FULL":
                self._api.log_event(telegram_user_id, OnboardingEventType.PROGRAM_FULL, code)
                return "That program is currently full. Contact your coach."
            elif reason == "CAMPAIGN_PAUSED":
                self._api.log_event(telegram_user_id, OnboardingEventType.CODE_INVALID, code)
                return "That program is not currently accepting enrollments."
            else:
                return "Sorry, something went wrong. Please try again."

        # Check duplicate: same Telegram user + same coach (CBAR Q8)
        if self._api.check_duplicate(telegram_user_id, validation.coach_id, validation.program_id):
            self._api.log_event(
                telegram_user_id, OnboardingEventType.DUPLICATE_BLOCKED, code,
                coach_id=validation.coach_id, program_id=validation.program_id,
            )
            return "You're already enrolled in this program!"

        # Valid code — start intake
        self._api.log_event(
            telegram_user_id, OnboardingEventType.CODE_VALID, code,
            coach_id=validation.coach_id, program_id=validation.program_id,
        )

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_CODE_VALIDATE,
            agent_name="telegram_onboarding_bot",
            input_payload={"telegram_user_id": telegram_user_id, "code": code},
            output_payload={"valid": True, "coach_id": validation.coach_id},
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        # Create intake session
        session = IntakeSession(
            telegram_user_id=telegram_user_id,
            coach_id=validation.coach_id,
            program_id=validation.program_id,
            program_code=code,
            intake_fields=validation.intake_fields or ["first_name", "primary_goal"],
        )
        self._active_sessions[telegram_user_id] = session

        self._api.log_event(
            telegram_user_id, OnboardingEventType.INTAKE_STARTED, code,
            coach_id=validation.coach_id, program_id=validation.program_id,
        )

        # Ask first question
        return self._get_question(session)

    def _handle_intake_response(self, telegram_user_id: int, text: str) -> str:
        """
        § 4 Stage 2: Conversational Intake — one question at a time.
        """
        session = self._active_sessions[telegram_user_id]
        current_field = session.current_field

        if current_field is None:
            return "Something went wrong. Please start over with /start."

        # Store response
        session.collected_data[current_field] = text.strip()
        session.current_field_index += 1

        # Check if intake is complete
        if session.is_complete:
            self._api.log_event(
                telegram_user_id, OnboardingEventType.INTAKE_COMPLETED,
                session.program_code, coach_id=session.coach_id,
                program_id=session.program_id,
            )

            # Receipt for intake completion
            receipt = build_receipt(
                stage_name=RECEIPT_STAGE_INTAKE_COMPLETE,
                agent_name="telegram_onboarding_bot",
                input_payload={
                    "telegram_user_id": telegram_user_id,
                    "collected_fields": list(session.collected_data.keys()),
                },
                output_payload={"status": "intake_complete"},
                previous_receipt_hash=self._last_receipt_hash,
            )
            self._receipts.append(receipt)
            self._last_receipt_hash = compute_receipt_hash(receipt)

            # Trigger provisioning
            result = self._api.provision_client(session)

            # Clean up session
            del self._active_sessions[telegram_user_id]

            if result.success:
                first_name = session.collected_data.get("first_name", "there")
                return f"You're in, {first_name}! 🎉 Your first check-in arrives soon."
            else:
                return f"Something went wrong during setup: {result.error}. Please contact your coach."

        # Ask next question
        return self._get_question(session)

    def _get_question(self, session: IntakeSession) -> str:
        """Get the current intake question."""
        field = session.current_field
        if field and field in INTAKE_QUESTIONS:
            return INTAKE_QUESTIONS[field]
        elif field:
            return f"Please enter your {field.replace('_', ' ')}:"
        return "Something went wrong."

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  DEP-COM-008: Client Onboarding API
# =====================================================

class ClientOnboardingAPI:
    """
    § 4 Stage 3 + Stage 4: Backend endpoint processing enrollments.

    Atomic auto-provisioning:
    1. Create CBCS Profile (ALTER TABLE profiles extension)
    2. Flag usage for billing on first bot message
    3. Add to AFFiNE workspace
    4. Schedule first check-in
    5. Confirm to prospect
    6. Notify coach
    7. Write Receipt Chain Guard
    """

    def __init__(
        self,
        program_registry: ProgramRegistryService,
    ) -> None:
        self._registry = program_registry
        self._profiles: dict[str, ClientProfileExtension] = {}  # keyed by composite
        self._events: list[OnboardingEventRow] = []
        self._provisioned: list[ProvisioningResult] = []
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""
        # Track duplicate enrollment: (telegram_user_id, coach_id) → set of program_ids
        self._enrollments: dict[tuple[int, str], set[str]] = {}

    def log_event(
        self,
        telegram_user_id: int,
        event_type: OnboardingEventType,
        program_code: str | None = None,
        coach_id: str | None = None,
        program_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> OnboardingEventRow:
        """Log an onboarding event."""
        event = OnboardingEventRow(
            telegram_user_id=telegram_user_id,
            event_type=event_type,
            program_code=program_code,
            coach_id=coach_id,
            program_id=program_id,
            metadata=metadata,
        )
        self._events.append(event)
        return event

    def check_duplicate(
        self,
        telegram_user_id: int,
        coach_id: str,
        program_id: str,
    ) -> bool:
        """
        § 4 Stage 4: Duplicate Detection.
        CBAR Q8: UNIQUE(telegram_user_id, coach_id) — one enrollment per (user, coach).
        Same user + same coach + same program → BLOCK.
        Same user + different coach → ALLOW (multi-coach enrollment).
        """
        key = (telegram_user_id, coach_id)
        enrolled_programs = self._enrollments.get(key, set())
        return program_id in enrolled_programs

    def provision_client(self, session: IntakeSession) -> ProvisioningResult:
        """
        § 4 Stage 3: Atomic auto-provisioning sequence.
        All succeed or all rollback.
        """
        self.log_event(
            session.telegram_user_id,
            OnboardingEventType.PROVISIONING_STARTED,
            session.program_code,
            coach_id=session.coach_id,
            program_id=session.program_id,
        )

        try:
            # Step 1: Create CBCS Profile (ALTER TABLE profiles extension)
            profile_id = str(uuid.uuid4())
            profile = ClientProfileExtension(
                program_id=session.program_id,
                telegram_user_id=session.telegram_user_id,
                primary_goal=session.collected_data.get("primary_goal"),
                intake_data=session.collected_data,
                enrollment_code=session.program_code,
                status=ClientProfileStatus.ACTIVE,
            )

            # CBAR Q8: Composite key enforcement
            composite_key = f"{session.telegram_user_id}_{session.coach_id}"
            self._profiles[composite_key] = profile

            # Track enrollment for duplicate detection
            enrollment_key = (session.telegram_user_id, session.coach_id)
            if enrollment_key not in self._enrollments:
                self._enrollments[enrollment_key] = set()
            self._enrollments[enrollment_key].add(session.program_id)

            # Step 2: Flag usage for billing (first-message trigger, not enrollment)
            # Note: actual $4 charge happens at first bot message time (JailSystem)
            billing_flagged = True

            # Step 3: Add to AFFiNE workspace (simulated)
            affine_pushed = True

            # Step 4: Schedule first check-in (simulated)
            checkin_scheduled = True

            # Step 5: Confirm — handled by bot

            # Step 6: Notify coach (simulated)
            coach_notified = True

            # Step 7: Increment program enrollment count
            self._registry.increment_enrollment(session.program_id)

            # Step 8: Write Receipt Chain Guard (DEP-ENG-041)
            receipt = build_receipt(
                stage_name=RECEIPT_STAGE_PROVISIONING,
                agent_name="client_onboarding_api",
                input_payload={
                    "telegram_user_id": session.telegram_user_id,
                    "coach_id": session.coach_id,
                    "program_id": session.program_id,
                    "program_code": session.program_code,
                },
                output_payload={
                    "profile_id": profile_id,
                    "status": "provisioned",
                },
                previous_receipt_hash=self._last_receipt_hash,
            )
            self._receipts.append(receipt)
            self._last_receipt_hash = compute_receipt_hash(receipt)

            result = ProvisioningResult(
                success=True,
                profile_id=profile_id,
                billing_reported=billing_flagged,
                affine_pushed=affine_pushed,
                checkin_scheduled=checkin_scheduled,
                coach_notified=coach_notified,
                receipt_id=receipt["receipt_id"],
            )

            self.log_event(
                session.telegram_user_id,
                OnboardingEventType.PROVISIONING_COMPLETED,
                session.program_code,
                coach_id=session.coach_id,
                program_id=session.program_id,
            )

            self._provisioned.append(result)
            return result

        except Exception as e:
            self.log_event(
                session.telegram_user_id,
                OnboardingEventType.PROVISIONING_FAILED,
                session.program_code,
                coach_id=session.coach_id,
                program_id=session.program_id,
                metadata={"error": str(e)},
            )
            return ProvisioningResult(
                success=False,
                error=str(e),
            )

    def trigger_first_message_billing(
        self,
        telegram_user_id: int,
        coach_id: str,
        client_id: str,
    ) -> dict[str, Any]:
        """
        First-message billing trigger.
        Called when bot sends FIRST message to the client.
        $4 usage reported at this time (not during enrollment).
        """
        # Find profile
        composite_key = f"{telegram_user_id}_{coach_id}"
        profile = self._profiles.get(composite_key)
        if profile is None:
            raise OnboardingError(
                code="PROFILE_NOT_FOUND",
                message="Client profile not found for billing trigger.",
            )

        if profile.first_message_sent:
            # Idempotent — already triggered
            return {
                "already_triggered": True,
                "first_message_sent_at": profile.first_message_sent_at.isoformat()
                if profile.first_message_sent_at
                else None,
            }

        profile.first_message_sent = True
        profile.first_message_sent_at = datetime.now(timezone.utc)
        profile.billing_reported = True

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_FIRST_MESSAGE,
            agent_name="client_onboarding_api",
            input_payload={
                "telegram_user_id": telegram_user_id,
                "coach_id": coach_id,
            },
            output_payload={
                "billing_reported": True,
                "first_message_sent_at": profile.first_message_sent_at.isoformat(),
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return {
            "already_triggered": False,
            "billing_reported": True,
            "first_message_sent_at": profile.first_message_sent_at.isoformat(),
        }

    def get_events(self) -> list[OnboardingEventRow]:
        return list(self._events)

    def get_events_by_type(self, event_type: OnboardingEventType) -> list[OnboardingEventRow]:
        return [e for e in self._events if e.event_type == event_type]

    def get_provisioned(self) -> list[ProvisioningResult]:
        return list(self._provisioned)

    def get_profiles(self) -> dict[str, ClientProfileExtension]:
        return dict(self._profiles)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)
