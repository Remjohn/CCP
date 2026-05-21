"""
FR-CA11-02 — AFFiNE Sync Service Tests
=======================================
Covers all 6 Acceptance Criteria:
  AC1: Content Push — entry appears in AFFiNE Content Calendar
  AC2: Idempotency — same payload twice → one entry (update, not duplicate)
  AC3: Event Logging — affine_sync_events contains correct entry
  AC4: Retry Logic — 5 retries with exponential backoff
  AC5: Dual Delivery — BOTH mode pushes to AFFiNE + Notion
  AC6: Receipt Chain — valid receipt with sync event's receipt_chain_id

Plus: cross-tenant rejection, model validation, hash computation, payload schemas.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ccp.models.ca11_models import (
    SYNC_BACKOFF_SCHEDULE,
    SYNC_MAX_RETRIES,
    CanvaApprovePayload,
    ContentPayloadBody,
    ContentPushPayload,
    LearningPathPushPayload,
    SessionPushPayload,
    SyncErrorType,
    SyncEvent,
    SyncEventStatus,
    SyncEventType,
    SyncResult,
    TelemetryPushPayload,
    VisualAssetRef,
)
from src.ccp.services.affine_sync import (
    AGENT_NAME,
    SERVICE_NAME,
    SYNC_EVENTS_TABLE_SQL,
    AFFiNEClient,
    AFFiNESyncService,
    IdempotencyEngine,
    RetryEngine,
    SyncEventLogger,
)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _run(coro):
    """Run an async coroutine synchronously for tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ══════════════════════════════════════════════════════════════════════════════
# Test Fixtures & Mocks
# ══════════════════════════════════════════════════════════════════════════════


class MockAFFiNEClient(AFFiNEClient):
    """Mock AFFiNE client that stores entries in memory."""

    def __init__(self):
        super().__init__(base_url="https://test.local", api_token="test-token")
        self._databases: dict[str, dict[str, dict]] = {}
        self._healthy = True
        self._fail_count = 0
        self._fail_until = 0

    async def query_by_asset_id(
        self, workspace_id: str, section_id: str, asset_id: str
    ) -> Optional[dict[str, Any]]:
        self._maybe_fail()
        db_key = f"{workspace_id}:{section_id}"
        db = self._databases.get(db_key, {})
        return db.get(asset_id)

    async def create_entry(
        self, workspace_id: str, section_id: str, entry_data: dict[str, Any]
    ) -> dict[str, Any]:
        self._maybe_fail()
        db_key = f"{workspace_id}:{section_id}"
        if db_key not in self._databases:
            self._databases[db_key] = {}
        block_id = str(uuid.uuid4())[:8]
        asset_id = entry_data.get("asset_id", block_id)
        record = {**entry_data, "block_id": block_id}
        self._databases[db_key][asset_id] = record
        return record

    async def update_entry(
        self,
        workspace_id: str,
        section_id: str,
        block_id: str,
        entry_data: dict[str, Any],
    ) -> dict[str, Any]:
        self._maybe_fail()
        db_key = f"{workspace_id}:{section_id}"
        asset_id = entry_data.get("asset_id", "")
        if db_key in self._databases and asset_id in self._databases[db_key]:
            self._databases[db_key][asset_id].update(entry_data)
            return self._databases[db_key][asset_id]
        return {**entry_data, "block_id": block_id}

    async def health_check(self) -> bool:
        return self._healthy

    def _maybe_fail(self):
        if self._fail_until > 0:
            self._fail_until -= 1
            self._fail_count += 1
            raise ConnectionError("AFFiNE API unreachable (mock)")

    def set_fail_until(self, count: int):
        self._fail_until = count
        self._fail_count = 0

    def get_entry_count(self, workspace_id: str, section_id: str) -> int:
        db_key = f"{workspace_id}:{section_id}"
        return len(self._databases.get(db_key, {}))

    def get_entry(
        self, workspace_id: str, section_id: str, asset_id: str
    ) -> Optional[dict]:
        db_key = f"{workspace_id}:{section_id}"
        return self._databases.get(db_key, {}).get(asset_id)


# MockNotionSync Removed (Obsolete)


class MockConfigProvider:
    """Mock coach_config provider."""

    def __init__(self, configs: dict[str, dict] = None):
        self._configs = configs or {}

    def get_coach_config(self, coach_id: str) -> dict:
        if coach_id not in self._configs:
            raise KeyError(f"Coach {coach_id} not found")
        return self._configs[coach_id]


def make_content_payload(
    asset_id: str = "JP-CCF-20260324-001-CAROUSEL",
    coach_id: str = "uuid-coach-001",
) -> ContentPushPayload:
    """Factory for test content payloads."""
    return ContentPushPayload(
        asset_id=asset_id,
        coach_id=coach_id,
        fingerprint_id="SKILL-ACH-JP-PROC-PROM-DEV-20260324-001",
        content=ContentPayloadBody(
            script_markdown="## The Mirror Effect\nYour reflection reveals...",
            posting_notes="Best posted Tuesday 9AM.",
            why_this_post="Built from voice note about identity.",
            leadership_farming="Authentic Vulnerability (score: 7.2).",
        ),
        visual_assets=[
            VisualAssetRef(
                slide_number=1,
                image_url="https://r2.consciouselite.com/JP/assets/slide_001.png",
                agss_score=7.8,
                tiar_nouns=["inner compass", "sovereign leader"],
            )
        ],
        voice_note_url="https://r2.consciouselite.com/JP/audio/trigger_20260324.mp3",
    )


COACH_ID = "uuid-coach-001"
WORKSPACE_ID = "ws-affine-001"


@pytest.fixture
def affine_client():
    return MockAFFiNEClient()


# notion_sync fixture removed


@pytest.fixture
def config_provider():
    return MockConfigProvider(
        configs={
            COACH_ID: {
                "affine_workspace_id": WORKSPACE_ID,
                "delivery_target": "BOTH",
            },
            "uuid-coach-002": {
                "affine_workspace_id": "ws-affine-002",
                "delivery_target": "AFFINE_ONLY",
            },
        }
    )


@pytest.fixture
def sync_service(affine_client, config_provider, tmp_path):
    return AFFiNESyncService(
        coach_acronym="JPR",
        affine_client=affine_client,
        config_provider=config_provider,
        retry_engine=RetryEngine(
            sleep_fn=AsyncMock(),  # no-op sleep for tests
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Test Constants & Enums
# ══════════════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify FR-CA11-02 constants are correctly defined."""

    def test_sync_max_retries(self):
        assert SYNC_MAX_RETRIES == 5

    def test_backoff_schedule(self):
        assert SYNC_BACKOFF_SCHEDULE == (5.0, 10.0, 20.0, 40.0, 80.0)

    # test_default_delivery_target, test_delivery_target_values removed (obsolete)

    def test_sync_event_types(self):
        assert len(SyncEventType) == 5
        assert SyncEventType.CONTENT_PUSH.value == "CONTENT_PUSH"

    def test_sync_event_status_values(self):
        assert set(s.value for s in SyncEventStatus) == {"SUCCESS", "RETRY", "FAILED"}


# ══════════════════════════════════════════════════════════════════════════════
# Test Models (DEP-ENG-072)
# ══════════════════════════════════════════════════════════════════════════════


class TestContentPushPayloadSchema:
    """Verify DEP-ENG-072 ContentPushPayload schema."""

    def test_valid_payload_creates(self):
        p = make_content_payload()
        assert p.asset_id == "JP-CCF-20260324-001-CAROUSEL"
        assert p.receipt_chain_guard.schema_ref == "DEP-ENG-041"

    def test_receipt_chain_guard_ref_not_string_literal(self):
        """CA11 Revision Fix 2: schema_ref, not string literal."""
        p = make_content_payload()
        assert hasattr(p.receipt_chain_guard, "schema_ref")
        assert p.receipt_chain_guard.schema_ref == "DEP-ENG-041"

    def test_visual_asset_validation(self):
        v = VisualAssetRef(
            slide_number=1,
            image_url="https://example.com/img.png",
            agss_score=7.8,
            tiar_nouns=["word"],
        )
        assert v.agss_score == 7.8

    def test_visual_asset_score_bounds(self):
        with pytest.raises(Exception):
            VisualAssetRef(
                slide_number=1,
                image_url="https://example.com/img.png",
                agss_score=11.0,  # Out of bounds
                tiar_nouns=[],
            )

    def test_missing_asset_id_rejected(self):
        with pytest.raises(Exception):
            ContentPushPayload(
                coach_id="test",
                fingerprint_id="test",
                content=ContentPayloadBody(script_markdown="test"),
            )

    def test_telemetry_payload_validation(self):
        p = TelemetryPushPayload(
            coach_id="uuid-001",
            period="2026-W13",
            spt_distribution={"Stage1": 5, "Stage2": 3},
            avg_intimacy_index=6.5,
        )
        assert p.period == "2026-W13"

    def test_session_payload_validation(self):
        p = SessionPushPayload(
            coach_id="uuid-001",
            session_id="sess-001",
            session_date="2026-03-24",
            session_summary="Great session",
        )
        assert p.session_id == "sess-001"

    def test_sync_event_model(self):
        e = SyncEvent(
            event_id=str(uuid.uuid4()),
            event_type=SyncEventType.CONTENT_PUSH,
            target_workspace_id="ws-001",
            payload_hash="abc123",
            status=SyncEventStatus.SUCCESS,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        assert e.retry_count == 0


# ══════════════════════════════════════════════════════════════════════════════
# AC1: Content Push
# ══════════════════════════════════════════════════════════════════════════════


class TestContentPush:
    """AC1: Push content → entry appears in AFFiNE Content Calendar."""

    def test_content_push_creates_entry(self, sync_service, affine_client):
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        assert result.success is True
        assert "AFFINE" in result.delivery_targets_completed

        entry = affine_client.get_entry(WORKSPACE_ID, "content_calendar", payload.asset_id)
        assert entry is not None
        assert entry["asset_id"] == payload.asset_id
        assert entry["fingerprint_id"] == payload.fingerprint_id

    def test_content_push_correct_metadata(self, sync_service, affine_client):
        payload = make_content_payload()
        _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        entry = affine_client.get_entry(WORKSPACE_ID, "content_calendar", payload.asset_id)
        assert entry["content"]["script_markdown"].startswith("## The Mirror Effect")
        assert len(entry["visual_assets"]) == 1
        assert entry["visual_assets"][0]["agss_score"] == 7.8

    def test_content_push_returns_sync_result(self, sync_service):
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        assert isinstance(result, SyncResult)
        assert isinstance(result.event, SyncEvent)
        assert result.event.event_type == SyncEventType.CONTENT_PUSH
        assert result.event.status == SyncEventStatus.SUCCESS


# ══════════════════════════════════════════════════════════════════════════════
# AC2: Idempotency
# ══════════════════════════════════════════════════════════════════════════════


class TestIdempotency:
    """AC2: Push same payload twice → only one entry (update, not duplicate)."""

    def test_duplicate_push_does_not_create_duplicate(
        self, sync_service, affine_client
    ):
        payload = make_content_payload()
        _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        count = affine_client.get_entry_count(WORKSPACE_ID, "content_calendar")
        assert count == 1, f"Expected 1 entry, got {count} — idempotency violation"

    def test_duplicate_push_returns_was_update(self, sync_service):
        payload = make_content_payload()
        result1 = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        result2 = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        assert result1.was_update is False
        assert result2.was_update is True

    def test_different_assets_create_separate_entries(
        self, sync_service, affine_client
    ):
        p1 = make_content_payload(asset_id="ASSET-001")
        p2 = make_content_payload(asset_id="ASSET-002")
        _run(sync_service.push_content(p1, workspace_id=WORKSPACE_ID))
        _run(sync_service.push_content(p2, workspace_id=WORKSPACE_ID))

        count = affine_client.get_entry_count(WORKSPACE_ID, "content_calendar")
        assert count == 2

    def test_idempotency_engine_standalone(self, affine_client):
        engine = IdempotencyEngine(affine_client)
        data = {"asset_id": "ASSET-X", "content": "test"}

        result1, was_update1 = _run(engine.create_or_update(
            "ws-1", "section-1", "ASSET-X", data
        ))
        assert was_update1 is False

        result2, was_update2 = _run(engine.create_or_update(
            "ws-1", "section-1", "ASSET-X", data
        ))
        assert was_update2 is True


# ══════════════════════════════════════════════════════════════════════════════
# AC3: Event Logging
# ══════════════════════════════════════════════════════════════════════════════


class TestEventLogging:
    """AC3: Push payload → affine_sync_events contains correct entry."""

    def test_event_logged_on_success(self, sync_service):
        payload = make_content_payload()
        _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        events = sync_service.event_logger.get_events(
            event_type=SyncEventType.CONTENT_PUSH,
            status=SyncEventStatus.SUCCESS,
        )
        assert len(events) >= 1
        event = events[-1]
        assert event.event_type == SyncEventType.CONTENT_PUSH
        assert event.status == SyncEventStatus.SUCCESS

    def test_event_payload_hash_matches(self, sync_service):
        payload = make_content_payload()
        expected_hash = SyncEventLogger.compute_payload_hash(payload)
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        assert result.event.payload_hash == expected_hash

    def test_event_has_receipt_chain_id(self, sync_service):
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        assert result.event.receipt_chain_id != ""

    def test_payload_hash_deterministic(self):
        payload = make_content_payload()
        h1 = SyncEventLogger.compute_payload_hash(payload)
        h2 = SyncEventLogger.compute_payload_hash(payload)
        assert h1 == h2
        assert len(h1) == 64  # SHA-256 hex

    def test_different_payloads_different_hashes(self):
        p1 = make_content_payload(asset_id="A1")
        p2 = make_content_payload(asset_id="A2")
        assert SyncEventLogger.compute_payload_hash(p1) != SyncEventLogger.compute_payload_hash(p2)


# ══════════════════════════════════════════════════════════════════════════════
# AC4: Retry Logic
# ══════════════════════════════════════════════════════════════════════════════


class TestRetryLogic:
    """AC4: AFFiNE API blocked → 5 retries with exponential backoff."""

    def test_retry_succeeds_after_failures(self, sync_service, affine_client):
        affine_client.set_fail_until(3)  # Fail 3 times, then succeed
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        assert result.success is True

    def test_retry_logs_retry_events(self, sync_service, affine_client):
        affine_client.set_fail_until(2)  # Fail 2 times
        payload = make_content_payload()
        _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        retry_events = sync_service.event_logger.get_events(
            status=SyncEventStatus.RETRY
        )
        assert len(retry_events) >= 1

    def test_max_retries_exceeded_returns_failed(
        self, sync_service, affine_client
    ):
        affine_client.set_fail_until(100)  # Always fail
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))
        assert result.success is False
        assert result.error_type == SyncErrorType.MAX_RETRIES_EXCEEDED
        assert result.event.status == SyncEventStatus.FAILED

    def test_backoff_schedule(self):
        engine = RetryEngine()
        assert engine.get_backoff_delay(0) == 5.0
        assert engine.get_backoff_delay(1) == 10.0
        assert engine.get_backoff_delay(2) == 20.0
        assert engine.get_backoff_delay(3) == 40.0
        assert engine.get_backoff_delay(4) == 80.0
        assert engine.get_backoff_delay(99) == 80.0  # Clamp to last

    def test_retry_engine_returns_attempt_count(self):
        call_count = 0

        async def failing_then_ok():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise ConnectionError("fail")
            return "ok"

        engine = RetryEngine(sleep_fn=AsyncMock())
        result, retries = _run(engine.execute_with_retry(failing_then_ok))
        assert result == "ok"
        assert retries == 2  # Succeeded on attempt index 2 (3rd attempt)


# ══════════════════════════════════════════════════════════════════════════════
# AC5: Dual Delivery
# ══════════════════════════════════════════════════════════════════════════════


class TestDualDelivery:
    """AC5: Notion delivery is retired. Verify only AFFiNE is delivered."""

    def test_only_affine_target_delivered(
        self, sync_service, affine_client
    ):
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        assert "AFFINE" in result.delivery_targets_completed
        assert "NOTION" not in result.delivery_targets_completed
        assert affine_client.get_entry_count(WORKSPACE_ID, "content_calendar") == 1


# ══════════════════════════════════════════════════════════════════════════════
# AC6: Receipt Chain
# ══════════════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """AC6: Push payload → Receipt Chain Guard contains valid receipt."""

    def test_receipt_written_on_push(self, sync_service):
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        assert result.event.receipt_chain_id != ""
        assert len(result.event.receipt_chain_id) > 0

    def test_receipt_chain_id_in_event(self, sync_service):
        payload = make_content_payload()
        result = _run(sync_service.push_content(payload, workspace_id=WORKSPACE_ID))

        events = sync_service.event_logger.get_events(
            status=SyncEventStatus.SUCCESS
        )
        assert len(events) >= 1
        assert events[-1].receipt_chain_id == result.event.receipt_chain_id


# ══════════════════════════════════════════════════════════════════════════════
# Cross-Tenant Safety
# ══════════════════════════════════════════════════════════════════════════════


class TestCrossTenantSafety:
    """§10 Safety: Cross-tenant push rejection."""

    def test_cross_tenant_push_rejected(self, affine_client):
        config = MockConfigProvider(
            configs={
                COACH_ID: {
                    "affine_workspace_id": WORKSPACE_ID,
                    "delivery_target": "AFFINE_ONLY",
                }
            }
        )
        service = AFFiNESyncService(
            coach_acronym="JPR",
            affine_client=affine_client,
            config_provider=config,
            retry_engine=RetryEngine(sleep_fn=AsyncMock()),
        )
        payload = make_content_payload(coach_id=COACH_ID)
        # Push to a workspace NOT owned by this coach
        result = _run(service.push_content(payload, workspace_id="ws-OTHER-COACH"))

        assert result.success is False
        assert result.error_type == SyncErrorType.COACH_WORKSPACE_MISMATCH


# ══════════════════════════════════════════════════════════════════════════════
# Other Endpoints
# ══════════════════════════════════════════════════════════════════════════════


class TestOtherEndpoints:
    """Telemetry, session, learning path, canva approve endpoints."""

    def test_telemetry_push(self, sync_service):
        payload = TelemetryPushPayload(
            coach_id=COACH_ID,
            period="2026-W13",
            spt_distribution={"Stage1": 5},
            avg_intimacy_index=6.5,
        )
        result = _run(sync_service.push_telemetry(payload, workspace_id=WORKSPACE_ID))
        assert result.success is True
        assert result.event.event_type == SyncEventType.TELEMETRY_PUSH

    def test_session_push(self, sync_service):
        payload = SessionPushPayload(
            coach_id=COACH_ID,
            session_id="sess-001",
            session_date="2026-03-24",
            session_summary="Client breakthrough on vulnerability.",
        )
        result = _run(sync_service.push_session(payload, workspace_id=WORKSPACE_ID))
        assert result.success is True
        assert result.event.event_type == SyncEventType.SESSION_PUSH

    def test_learning_path_push(self, sync_service):
        payload = LearningPathPushPayload(
            coach_id=COACH_ID,
            content_category="Module 3 — Identity",
            content_items=[{"title": "Voice DNA Intro", "type": "video"}],
        )
        result = _run(sync_service.push_learning_path(
            payload, workspace_id=WORKSPACE_ID
        ))
        assert result.success is True
        assert result.event.event_type == SyncEventType.LEARNING_PATH_PUSH

    def test_canva_approve(self, sync_service):
        payload = CanvaApprovePayload(
            coach_id=COACH_ID,
            design_id="canva-design-001",
            asset_id="JP-VPO-20260324-001",
        )
        result = _run(sync_service.handle_canva_approve(
            payload, workspace_id=WORKSPACE_ID
        ))
        assert result.success is True
        assert result.event.event_type == SyncEventType.CANVA_APPROVE

    def test_health_check(self, sync_service):
        health = _run(sync_service.health_check())
        assert health["service"] == SERVICE_NAME
        assert health["coach_acronym"] == "JPR"


# ══════════════════════════════════════════════════════════════════════════════
# SQL Schema Validation
# ══════════════════════════════════════════════════════════════════════════════


class TestSQLSchema:
    """Verify SQL schema contains required elements."""

    def test_sync_events_table_defined(self):
        assert "affine_sync_events" in SYNC_EVENTS_TABLE_SQL
        assert "event_id" in SYNC_EVENTS_TABLE_SQL
        assert "event_type" in SYNC_EVENTS_TABLE_SQL
        assert "payload_hash" in SYNC_EVENTS_TABLE_SQL
        assert "receipt_chain_id" in SYNC_EVENTS_TABLE_SQL

    def test_delivery_target_column_defined(self):
        assert "delivery_target" in SYNC_EVENTS_TABLE_SQL
        assert "AFFINE_ONLY" in SYNC_EVENTS_TABLE_SQL
        assert "NOTION_ONLY" in SYNC_EVENTS_TABLE_SQL
        assert "BOTH" in SYNC_EVENTS_TABLE_SQL
