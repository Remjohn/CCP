"""
CCP FR-CA11-02 — AFFiNE Sync Service (DEP-ENG-072 PROPOSED)

FastAPI-based webhook-driven sync service that replaces notion_sync.py (FR45)
as the delivery pipeline. Pushes CCP backend intelligence to coach and client
AFFiNE workspaces with idempotent writes, event logging, and receipt chain
integration.

Spec reference: FR-CA11-02_AFFiNE_Sync_Service_Tech_Spec.md
  §4 — Stage 1: FastAPI Service Scaffold
  §4 — Stage 2: Content Push Implementation
  §4 — Stage 3: Telemetry Push Implementation
  §5 — DEP-ENG-072 PROPOSED (ContentPushPayload)
  §6 — Backward Compatibility Fallback (dual delivery)
  §7 — Tasks 1-8
  §8 — AC1-AC6

Architecture references:
  ADR-05: AFFiNE Over Notion (retires ADR-02)
  FR47/DEP-ENG-041: Receipt Chain Guard schema for all receipt writes
  FR-CA11-01/DEP-ENG-071: Workspace provisioning (workspace must exist)

Agent: Pierre (AFFiNE Workspace Orchestrator) — Management Department
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ca11_models import (
    SYNC_BACKOFF_SCHEDULE,
    SYNC_MAX_RETRIES,
    CanvaApprovePayload,
    ContentPushPayload,
    LearningPathPushPayload,
    SessionPushPayload,
    SyncErrorType,
    SyncEvent,
    SyncEventStatus,
    SyncEventType,
    SyncResult,
    TelemetryPushPayload,
)

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

AGENT_NAME = "Pierre"
SERVICE_NAME = "affine_sync"

# ── SQL Schema ────────────────────────────────────────────────────────────────
# Task 3: Supabase affine_sync_events table + DELIVERY_TARGET column (Task 6)

SYNC_EVENTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS affine_sync_events (
    event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type      TEXT NOT NULL CHECK (event_type IN (
                        'CONTENT_PUSH', 'TELEMETRY_PUSH', 'SESSION_PUSH',
                        'LEARNING_PATH_PUSH', 'CANVA_APPROVE')),
    target_workspace_id UUID NOT NULL,
    payload_hash    TEXT NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('SUCCESS', 'RETRY', 'FAILED')),
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT now(),
    receipt_chain_id TEXT,
    error_detail    TEXT DEFAULT '',
    retry_count     INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sync_events_workspace
    ON affine_sync_events (target_workspace_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_sync_events_status
    ON affine_sync_events (status) WHERE status != 'SUCCESS';

-- Task 6: Delivery target feature flag on coach_config
ALTER TABLE coach_config
    ADD COLUMN IF NOT EXISTS delivery_target TEXT DEFAULT 'BOTH'
    CHECK (delivery_target IN ('AFFINE_ONLY', 'NOTION_ONLY', 'BOTH'));
"""


# ══════════════════════════════════════════════════════════════════════════════
# Unit 3 — AFFiNE API Client
# ══════════════════════════════════════════════════════════════════════════════


class AFFiNEClient:
    """Thin wrapper around AFFiNE's GraphQL/REST API for database operations.

    For the self-hosted instance, this client handles:
    - Database entry creation (create blocks in AFFiNE pages)
    - Database entry lookup (query by Asset ID for idempotency)
    - Database entry update (overwrite existing entry on retry)
    """

    def __init__(
        self,
        base_url: str = "https://os.consciouselite.com",
        api_token: str = "",
    ):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token

    async def query_by_asset_id(
        self,
        workspace_id: str,
        section_id: str,
        asset_id: str,
    ) -> Optional[dict[str, Any]]:
        """Query AFFiNE database for an existing entry by Universal Asset ID.

        Returns the entry dict if found, None if not found.
        This enables idempotency: same asset_id → update instead of duplicate.
        """
        # Implementation will use AFFiNE GraphQL API
        # Placeholder for external API call
        raise NotImplementedError("AFFiNE API integration pending deployment")

    async def create_entry(
        self,
        workspace_id: str,
        section_id: str,
        entry_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a new database entry in an AFFiNE workspace section.

        Returns the created entry with its AFFiNE block ID.
        """
        raise NotImplementedError("AFFiNE API integration pending deployment")

    async def update_entry(
        self,
        workspace_id: str,
        section_id: str,
        block_id: str,
        entry_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Update an existing database entry in an AFFiNE workspace section.

        Returns the updated entry.
        """
        raise NotImplementedError("AFFiNE API integration pending deployment")

    async def health_check(self) -> bool:
        """Check if the AFFiNE instance is responsive."""
        raise NotImplementedError("AFFiNE API integration pending deployment")


# ══════════════════════════════════════════════════════════════════════════════
# Unit 4 — Idempotency Engine
# ══════════════════════════════════════════════════════════════════════════════


class IdempotencyEngine:
    """Ensures duplicate pushes do not create duplicates (AC2).

    Uses Universal Asset ID (DEP-ENG-040) as the idempotency key.
    If an entry with the same Asset ID already exists, it is updated
    rather than duplicated.
    """

    def __init__(self, affine_client: AFFiNEClient):
        self._client = affine_client

    async def create_or_update(
        self,
        workspace_id: str,
        section_id: str,
        asset_id: str,
        entry_data: dict[str, Any],
    ) -> tuple[dict[str, Any], bool]:
        """Create a new entry or update existing one.

        Returns:
            Tuple of (entry_dict, was_update).
            was_update is True if an existing entry was updated.
        """
        existing = await self._client.query_by_asset_id(
            workspace_id=workspace_id,
            section_id=section_id,
            asset_id=asset_id,
        )

        if existing is not None:
            block_id = existing.get("block_id", "")
            result = await self._client.update_entry(
                workspace_id=workspace_id,
                section_id=section_id,
                block_id=block_id,
                entry_data=entry_data,
            )
            return result, True

        result = await self._client.create_entry(
            workspace_id=workspace_id,
            section_id=section_id,
            entry_data=entry_data,
        )
        return result, False


# ══════════════════════════════════════════════════════════════════════════════
# Unit 5 — Retry / Backoff Engine
# ══════════════════════════════════════════════════════════════════════════════


class RetryEngine:
    """Exponential backoff retry logic for AFFiNE API calls (AC4).

    Schedule: 5s, 10s, 20s, 40s, 80s — max 5 retries.
    After 5 failures → FAILED status, System Operator notified.

    Spec §4 Stage 2 Failure Condition: AFFiNE API unreachable →
    event logged as RETRY, DamageControl queues for exponential backoff.
    """

    def __init__(
        self,
        max_retries: int = SYNC_MAX_RETRIES,
        backoff_schedule: tuple[float, ...] = SYNC_BACKOFF_SCHEDULE,
        sleep_fn: Any = None,
    ):
        self.max_retries = max_retries
        self.backoff_schedule = backoff_schedule
        # Injectable sleep function for testing (default: asyncio.sleep)
        self._sleep_fn = sleep_fn

    async def _sleep(self, seconds: float) -> None:
        """Sleep for the given duration. Uses injected sleep_fn if provided."""
        if self._sleep_fn is not None:
            await self._sleep_fn(seconds)
        else:
            import asyncio
            await asyncio.sleep(seconds)

    def get_backoff_delay(self, attempt: int) -> float:
        """Get the backoff delay for a given attempt number (0-indexed)."""
        if attempt < len(self.backoff_schedule):
            return self.backoff_schedule[attempt]
        return self.backoff_schedule[-1]

    async def execute_with_retry(
        self,
        operation: Any,
        *args: Any,
        on_retry: Any = None,
        **kwargs: Any,
    ) -> tuple[Any, int]:
        """Execute an async operation with retry logic.

        Args:
            operation: Async callable to execute.
            on_retry: Optional callback(attempt, error) called on each retry.

        Returns:
            Tuple of (result, retry_count).

        Raises:
            The last exception if all retries are exhausted.
        """
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                result = await operation(*args, **kwargs)
                return result, attempt
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries:
                    delay = self.get_backoff_delay(attempt)
                    logger.warning(
                        "Sync retry attempt %d/%d after %.1fs: %s",
                        attempt + 1,
                        self.max_retries,
                        delay,
                        str(exc),
                    )
                    if on_retry is not None:
                        await on_retry(attempt, exc)
                    await self._sleep(delay)

        raise last_error  # type: ignore[misc]


# ══════════════════════════════════════════════════════════════════════════════
# Unit 6 — Event Logger
# ══════════════════════════════════════════════════════════════════════════════


class SyncEventLogger:
    """Writes sync events to the affine_sync_events Supabase table (AC3).

    Every sync operation writes an event with: event_type, target workspace,
    payload hash (SHA-256), status, timestamp, and receipt_chain_id.
    """

    def __init__(self, supabase_client: Any = None):
        self._supabase = supabase_client
        self._events: list[SyncEvent] = []  # In-memory log for testing

    @staticmethod
    def compute_payload_hash(payload: Any) -> str:
        """Compute SHA-256 hash of a payload for audit trail."""
        if hasattr(payload, "model_dump"):
            data = payload.model_dump(mode="json")
        elif isinstance(payload, dict):
            data = payload
        else:
            data = str(payload)
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def log_event(
        self,
        event_type: SyncEventType,
        target_workspace_id: str,
        payload_hash: str,
        status: SyncEventStatus,
        receipt_chain_id: str = "",
        error_detail: str = "",
        retry_count: int = 0,
    ) -> SyncEvent:
        """Record a sync event."""
        event = SyncEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            target_workspace_id=target_workspace_id,
            payload_hash=payload_hash,
            status=status,
            timestamp=datetime.now(timezone.utc).isoformat(),
            receipt_chain_id=receipt_chain_id,
            error_detail=error_detail,
            retry_count=retry_count,
        )
        self._events.append(event)

        # Persist to Supabase if available
        if self._supabase is not None:
            try:
                self._supabase.table("affine_sync_events").insert(
                    event.model_dump(mode="json")
                ).execute()
            except Exception as exc:
                logger.error("Failed to persist sync event to Supabase: %s", exc)

        return event

    def get_events(
        self,
        workspace_id: Optional[str] = None,
        event_type: Optional[SyncEventType] = None,
        status: Optional[SyncEventStatus] = None,
    ) -> list[SyncEvent]:
        """Query in-memory events with optional filters."""
        results = self._events
        if workspace_id is not None:
            results = [e for e in results if e.target_workspace_id == workspace_id]
        if event_type is not None:
            results = [e for e in results if e.event_type == event_type]
        if status is not None:
            results = [e for e in results if e.status == status]
        return results


# ══════════════════════════════════════════════════════════════════════════════
# Dual Delivery Router Removed (Obsolete Notion integration)
# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# Main Service — AFFiNE Sync Service
# ══════════════════════════════════════════════════════════════════════════════


class AFFiNESyncService:
    """AFFiNE Sync Service — the main orchestrator (Tasks 1-7).

    Replaces notion_sync.py (FR45) as the CCP delivery pipeline.
    Handles content push, telemetry push, session push, learning path push,
    and Canva approval webhook with idempotent writes, event logging,
    exponential retry, and receipt chain integration.
    """

    def __init__(
        self,
        coach_acronym: str,
        affine_client: AFFiNEClient,
        supabase_client: Any = None,
        config_provider: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
        retry_engine: Optional[RetryEngine] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self._affine = affine_client
        self._idempotency = IdempotencyEngine(affine_client)
        self._event_logger = SyncEventLogger(supabase_client)
        self._config_provider = config_provider
        self._receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )
        self._retry = retry_engine or RetryEngine()

    @property
    def event_logger(self) -> SyncEventLogger:
        """Expose event logger for test inspection."""
        return self._event_logger

    # ── Receipt Chain Integration (AC6) ──────────────────────────────────

    def _write_receipt(
        self,
        action: str,
        asset_id: str,
        input_payload: Any,
        output_summary: str,
        event_id: str,
    ) -> str:
        """Write a receipt to the Receipt Chain Guard (DEP-ENG-041)."""
        payload_hash = SyncEventLogger.compute_payload_hash(input_payload)
        entry = self._receipt_chain.log(
            agent_id=AGENT_NAME,
            action=action,
            asset_id=asset_id,
            input_summary=f"Sync payload hash: {payload_hash}",
            output_summary=output_summary,
            decision="delivered",
            metadata={
                "sync_event_id": event_id,
                "service": SERVICE_NAME,
                "schema_ref": "DEP-ENG-041",
            },
        )
        return entry.receipt_id

    # ── Workspace Resolution ─────────────────────────────────────────────

    def _resolve_workspace_id(self, coach_id: str) -> str:
        """Resolve coach_config.affine_workspace_id for a coach.

        In production, this queries Supabase coach_config table.
        Here we use the config_provider if available.
        """
        if self._config_provider is not None:
            config = self._config_provider.get_coach_config(coach_id)
            ws_id = config.get("affine_workspace_id", "")
            if ws_id:
                return ws_id
        raise ValueError(f"No AFFiNE workspace found for coach {coach_id}")

    def _validate_coach_workspace_ownership(
        self, coach_id: str, workspace_id: str
    ) -> bool:
        """Validate that the coach owns the target workspace (cross-tenant safety).

        Spec §10 Safety Tests: Cross-Tenant Push Rejection.
        """
        if self._config_provider is not None:
            config = self._config_provider.get_coach_config(coach_id)
            return config.get("affine_workspace_id") == workspace_id
        return True  # No config provider = no validation possible

    # ── Content Push (AC1, AC2, AC3, AC6) ─────────────────────────────────

    async def push_content(
        self,
        payload: ContentPushPayload,
        workspace_id: Optional[str] = None,
    ) -> SyncResult:
        """Push content to the coach's AFFiNE Content Calendar.

        Implements: AC1 (content push), AC2 (idempotency), AC3 (event logging),
        AC6 (receipt chain).
        """
        target_ws = workspace_id or self._resolve_workspace_id(payload.coach_id)
        payload_hash = SyncEventLogger.compute_payload_hash(payload)
        targets_completed: list[str] = []

        # Cross-tenant validation
        if not self._validate_coach_workspace_ownership(payload.coach_id, target_ws):
            event = self._event_logger.log_event(
                event_type=SyncEventType.CONTENT_PUSH,
                target_workspace_id=target_ws,
                payload_hash=payload_hash,
                status=SyncEventStatus.FAILED,
                error_detail="Cross-tenant push rejected: coach does not own workspace",
            )
            return SyncResult(
                success=False,
                event=event,
                error_type=SyncErrorType.COACH_WORKSPACE_MISMATCH,
            )

        # AFFiNE delivery
        try:
            entry_data = payload.model_dump(mode="json")
            result, retry_count = await self._retry.execute_with_retry(
                self._idempotency.create_or_update,
                target_ws,
                "content_calendar",
                payload.asset_id,
                entry_data,
                on_retry=lambda attempt, exc: self._log_retry_event(
                    SyncEventType.CONTENT_PUSH, target_ws, payload_hash, attempt, str(exc)
                ),
            )
            affine_entry, was_update = result
            targets_completed.append("AFFINE")
        except Exception as exc:
            event = self._event_logger.log_event(
                event_type=SyncEventType.CONTENT_PUSH,
                target_workspace_id=target_ws,
                payload_hash=payload_hash,
                status=SyncEventStatus.FAILED,
                error_detail=str(exc),
                retry_count=self._retry.max_retries,
                )
            return SyncResult(
                success=False,
                event=event,
                error_type=SyncErrorType.MAX_RETRIES_EXCEEDED,
                delivery_targets_completed=targets_completed,
            )

        # Log success event
        receipt_id = self._write_receipt(
            action="content_push",
            asset_id=payload.asset_id,
            input_payload=payload,
            output_summary=f"Content pushed to {', '.join(targets_completed)}",
            event_id="",
        )
        event = self._event_logger.log_event(
            event_type=SyncEventType.CONTENT_PUSH,
            target_workspace_id=target_ws,
            payload_hash=payload_hash,
            status=SyncEventStatus.SUCCESS,
            receipt_chain_id=receipt_id,
        )

        return SyncResult(
            success=True,
            event=event,
            was_update=was_update,
            delivery_targets_completed=targets_completed,
        )

    # ── Telemetry Push ────────────────────────────────────────────────────

    async def push_telemetry(
        self,
        payload: TelemetryPushPayload,
        workspace_id: Optional[str] = None,
    ) -> SyncResult:
        """Push CBCS aggregated telemetry to Client Intelligence Hub."""
        target_ws = workspace_id or self._resolve_workspace_id(payload.coach_id)
        payload_hash = SyncEventLogger.compute_payload_hash(payload)

        try:
            entry_data = payload.model_dump(mode="json")
            result, retry_count = await self._retry.execute_with_retry(
                self._affine.create_entry,
                target_ws,
                "client_intelligence_hub",
                entry_data,
            )
        except Exception as exc:
            event = self._event_logger.log_event(
                event_type=SyncEventType.TELEMETRY_PUSH,
                target_workspace_id=target_ws,
                payload_hash=payload_hash,
                status=SyncEventStatus.FAILED,
                error_detail=str(exc),
            )
            return SyncResult(
                success=False,
                event=event,
                error_type=SyncErrorType.MAX_RETRIES_EXCEEDED,
            )

        receipt_id = self._write_receipt(
            action="telemetry_push",
            asset_id=f"TELEM-{payload.period}",
            input_payload=payload,
            output_summary=f"Telemetry pushed for period {payload.period}",
            event_id="",
        )
        event = self._event_logger.log_event(
            event_type=SyncEventType.TELEMETRY_PUSH,
            target_workspace_id=target_ws,
            payload_hash=payload_hash,
            status=SyncEventStatus.SUCCESS,
            receipt_chain_id=receipt_id,
        )
        return SyncResult(success=True, event=event, delivery_targets_completed=["AFFINE"])

    # ── Session Push ──────────────────────────────────────────────────────

    async def push_session(
        self,
        payload: SessionPushPayload,
        workspace_id: Optional[str] = None,
    ) -> SyncResult:
        """Push session intelligence reports to Session Archive."""
        target_ws = workspace_id or self._resolve_workspace_id(payload.coach_id)
        payload_hash = SyncEventLogger.compute_payload_hash(payload)

        try:
            entry_data = payload.model_dump(mode="json")
            result, retry_count = await self._retry.execute_with_retry(
                self._affine.create_entry,
                target_ws,
                "session_archive",
                entry_data,
            )
        except Exception as exc:
            event = self._event_logger.log_event(
                event_type=SyncEventType.SESSION_PUSH,
                target_workspace_id=target_ws,
                payload_hash=payload_hash,
                status=SyncEventStatus.FAILED,
                error_detail=str(exc),
            )
            return SyncResult(
                success=False,
                event=event,
                error_type=SyncErrorType.MAX_RETRIES_EXCEEDED,
            )

        receipt_id = self._write_receipt(
            action="session_push",
            asset_id=payload.session_id,
            input_payload=payload,
            output_summary=f"Session {payload.session_id} pushed",
            event_id="",
        )
        event = self._event_logger.log_event(
            event_type=SyncEventType.SESSION_PUSH,
            target_workspace_id=target_ws,
            payload_hash=payload_hash,
            status=SyncEventStatus.SUCCESS,
            receipt_chain_id=receipt_id,
        )
        return SyncResult(success=True, event=event, delivery_targets_completed=["AFFINE"])

    # ── Learning Path Push ────────────────────────────────────────────────

    async def push_learning_path(
        self,
        payload: LearningPathPushPayload,
        workspace_id: Optional[str] = None,
    ) -> SyncResult:
        """Push categorized content to Program Content Library."""
        target_ws = workspace_id or self._resolve_workspace_id(payload.coach_id)
        payload_hash = SyncEventLogger.compute_payload_hash(payload)

        try:
            entry_data = payload.model_dump(mode="json")
            result, retry_count = await self._retry.execute_with_retry(
                self._affine.create_entry,
                target_ws,
                "program_content_library",
                entry_data,
            )
        except Exception as exc:
            event = self._event_logger.log_event(
                event_type=SyncEventType.LEARNING_PATH_PUSH,
                target_workspace_id=target_ws,
                payload_hash=payload_hash,
                status=SyncEventStatus.FAILED,
                error_detail=str(exc),
            )
            return SyncResult(
                success=False,
                event=event,
                error_type=SyncErrorType.MAX_RETRIES_EXCEEDED,
            )

        receipt_id = self._write_receipt(
            action="learning_path_push",
            asset_id=f"LP-{payload.content_category}",
            input_payload=payload,
            output_summary=f"Learning path pushed: {payload.content_category}",
            event_id="",
        )
        event = self._event_logger.log_event(
            event_type=SyncEventType.LEARNING_PATH_PUSH,
            target_workspace_id=target_ws,
            payload_hash=payload_hash,
            status=SyncEventStatus.SUCCESS,
            receipt_chain_id=receipt_id,
        )
        return SyncResult(success=True, event=event, delivery_targets_completed=["AFFINE"])

    # ── Canva Approve Webhook ─────────────────────────────────────────────

    async def handle_canva_approve(
        self,
        payload: CanvaApprovePayload,
        workspace_id: Optional[str] = None,
    ) -> SyncResult:
        """Handle CVE Canva App approval event, push VPO to Visual Production Console."""
        target_ws = workspace_id or self._resolve_workspace_id(payload.coach_id)
        payload_hash = SyncEventLogger.compute_payload_hash(payload)

        try:
            entry_data = payload.model_dump(mode="json")
            result, retry_count = await self._retry.execute_with_retry(
                self._affine.create_entry,
                target_ws,
                "visual_production_console",
                entry_data,
            )
        except Exception as exc:
            event = self._event_logger.log_event(
                event_type=SyncEventType.CANVA_APPROVE,
                target_workspace_id=target_ws,
                payload_hash=payload_hash,
                status=SyncEventStatus.FAILED,
                error_detail=str(exc),
            )
            return SyncResult(
                success=False,
                event=event,
                error_type=SyncErrorType.MAX_RETRIES_EXCEEDED,
            )

        receipt_id = self._write_receipt(
            action="canva_approve",
            asset_id=payload.asset_id,
            input_payload=payload,
            output_summary=f"Canva design {payload.design_id} approved and pushed",
            event_id="",
        )
        event = self._event_logger.log_event(
            event_type=SyncEventType.CANVA_APPROVE,
            target_workspace_id=target_ws,
            payload_hash=payload_hash,
            status=SyncEventStatus.SUCCESS,
            receipt_chain_id=receipt_id,
        )
        return SyncResult(success=True, event=event, delivery_targets_completed=["AFFINE"])

    # ── Notion Fallback Push Removed ──────────────────────────────────────

    # ── Retry Event Logging Helper ────────────────────────────────────────

    async def _log_retry_event(
        self,
        event_type: SyncEventType,
        workspace_id: str,
        payload_hash: str,
        attempt: int,
        error_detail: str,
    ) -> None:
        """Log a RETRY event during backoff."""
        self._event_logger.log_event(
            event_type=event_type,
            target_workspace_id=workspace_id,
            payload_hash=payload_hash,
            status=SyncEventStatus.RETRY,
            error_detail=error_detail,
            retry_count=attempt + 1,
        )

    # ── Health Check ──────────────────────────────────────────────────────

    async def health_check(self) -> dict[str, Any]:
        """Service health check endpoint data."""
        affine_ok = False
        try:
            affine_ok = await self._affine.health_check()
        except Exception:
            pass
        return {
            "service": SERVICE_NAME,
            "status": "healthy" if affine_ok else "degraded",
            "affine_connected": affine_ok,
            "coach_acronym": self.coach_acronym,
        }
