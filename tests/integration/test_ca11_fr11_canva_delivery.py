"""FR-CA11-11 — CVE Canva Clone → AFFiNE Delivery — Integration Tests.

Covers all 4 Acceptance Criteria:
  AC1: Delivery Redirect (AFFINE_ONLY)
  AC2: Dual Delivery (BOTH)
  AC3: Metadata Integrity
  AC4: Deep Link
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    CanvaApproveWebhookPayload,
    DeliveryTargetFlag,
    SlideEntry,
    VisualProductionOutput,
    VPODeliveryResult,
)
from src.ccp.services.canva_affine_delivery import (
    COLLAPSIBLE_AUDIT_KEYS,
    VPC_SECTION,
    VPO_ENTRIES_SQL,
    CanvaApproveHandler,
    DeliveryRouter,
    VPOConsoleEntryBuilder,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WORKSPACE_ID = "ws-coach-001"


def _make_vpo(**overrides) -> VisualProductionOutput:
    defaults = dict(
        asset_id="JP-CCF-20260324-001-CAROUSEL",
        slides=[
            SlideEntry(slide_number=1, png_url="https://r2.cdn/s1.png", agss_score=7.8),
            SlideEntry(slide_number=2, png_url="https://r2.cdn/s2.png", agss_score=8.1),
        ],
        horizontal_stitch_url="https://r2.cdn/stitch.png",
        zip_download_url="https://r2.cdn/comp.zip",
        recipe_name="Dopamine Cliff Carousel",
        visual_style="cinematic_color_graded",
        why_this_visual="Built from Trigger Map activation event.",
        leadership_farming_note="Exercises Deep Empathy (score: 7.4)",
        tiar_decay_audit={"inner compass": "in_distribution", "sovereign leader": "tribal_potential"},
        receipt_chain_status="CONFIRMED",
        fingerprint_id="SKILL-DOP-JP-DISC-PROM-DEV-20260324-001",
    )
    defaults.update(overrides)
    return VisualProductionOutput(**defaults)


def _make_payload(**overrides) -> CanvaApproveWebhookPayload:
    defaults = dict(
        vpo=_make_vpo(),
        coach_workspace_id=WORKSPACE_ID,
        delivery_target=DeliveryTargetFlag.affine_only,
        canva_app_deep_link="https://canva.ccp/edit/comp-001",
    )
    defaults.update(overrides)
    return CanvaApproveWebhookPayload(**defaults)


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---- Mocks ----

class MockAFFiNeSync:
    def __init__(self):
        self.entries: list[dict] = []
    async def push_content(self, workspace_id, section, payload):
        page_id = f"page-{uuid.uuid4().hex[:8]}"
        self.entries.append({"workspace_id": workspace_id, "section": section,
                             "payload": payload, "page_id": page_id})
        return page_id


class MockNotionSync:
    def __init__(self):
        self.entries: list[dict] = []
    async def push_content(self, workspace_id, section, payload):
        self.entries.append({"workspace_id": workspace_id, "section": section,
                             "payload": payload})
        return "notion-page-001"


class FailingSync:
    async def push_content(self, *a, **kw):
        raise ConnectionError("sync unavailable")


# ===================================================================
# 1. Model validation (6 tests)
# ===================================================================

class TestModels:
    def test_vpo_required_fields(self):
        vpo = _make_vpo()
        assert vpo.asset_id == "JP-CCF-20260324-001-CAROUSEL"
        assert len(vpo.slides) == 2

    def test_slide_entry(self):
        s = SlideEntry(slide_number=1, png_url="https://cdn/s.png", agss_score=9.0)
        assert s.agss_score == 9.0

    def test_delivery_target_flag_values(self):
        assert DeliveryTargetFlag.affine_only.value == "AFFINE_ONLY"
        assert DeliveryTargetFlag.both.value == "BOTH"
        assert DeliveryTargetFlag.notion_only.value == "NOTION_ONLY"

    def test_payload(self):
        p = _make_payload()
        assert p.coach_workspace_id == WORKSPACE_ID
        assert p.delivery_target == DeliveryTargetFlag.affine_only

    def test_vpo_delivery_result_defaults(self):
        r = VPODeliveryResult(success=True)
        assert not r.affine_delivered
        assert not r.notion_delivered

    def test_composition_id_generated(self):
        vpo = _make_vpo()
        assert len(vpo.composition_id) == 36  # UUID


# ===================================================================
# 2. Console Entry Builder (5 tests)
# ===================================================================

class TestConsoleEntryBuilder:
    def test_builds_entry(self):
        vpo = _make_vpo()
        entry = VPOConsoleEntryBuilder.build_entry(vpo, "https://link")
        assert entry["asset_id"] == vpo.asset_id
        assert len(entry["slides"]) == 2
        assert entry["deep_link"] == "https://link"

    def test_audit_section(self):
        vpo = _make_vpo()
        entry = VPOConsoleEntryBuilder.build_entry(vpo)
        assert "tiar_decay_audit" in entry["audit"]
        assert entry["audit"]["fingerprint_id"] == vpo.fingerprint_id

    def test_entry_id_generated(self):
        vpo = _make_vpo()
        entry = VPOConsoleEntryBuilder.build_entry(vpo)
        assert entry["entry_id"].startswith("vpo-")

    def test_metadata_integrity_ac3(self):
        """AC3 — TIAR, AGSS, fingerprint match."""
        vpo = _make_vpo()
        entry = VPOConsoleEntryBuilder.build_entry(vpo)
        assert VPOConsoleEntryBuilder.validate_metadata_integrity(vpo, entry)

    def test_metadata_integrity_mismatch(self):
        vpo = _make_vpo()
        entry = VPOConsoleEntryBuilder.build_entry(vpo)
        entry["audit"]["fingerprint_id"] = "WRONG"
        assert not VPOConsoleEntryBuilder.validate_metadata_integrity(vpo, entry)


# ===================================================================
# 3. Delivery Router — AC1 (5 tests)
# ===================================================================

class TestDeliveryRedirect:
    def test_affine_only_ac1(self):
        """AC1 — VPO delivered to AFFiNE only."""
        affine = MockAFFiNeSync()
        notion = MockNotionSync()
        router = DeliveryRouter(affine_sync=affine, notion_sync=notion)
        payload = _make_payload(delivery_target=DeliveryTargetFlag.affine_only)
        result = _run(router.deliver(payload))
        assert result.success
        assert result.affine_delivered
        assert not result.notion_delivered
        assert len(affine.entries) == 1
        assert len(notion.entries) == 0

    def test_affine_section_is_vpc(self):
        affine = MockAFFiNeSync()
        router = DeliveryRouter(affine_sync=affine)
        payload = _make_payload()
        _run(router.deliver(payload))
        assert affine.entries[0]["section"] == VPC_SECTION

    def test_affine_page_id_returned(self):
        affine = MockAFFiNeSync()
        router = DeliveryRouter(affine_sync=affine)
        result = _run(router.deliver(_make_payload()))
        assert result.affine_page_id is not None

    def test_affine_failure(self):
        router = DeliveryRouter(affine_sync=FailingSync())
        result = _run(router.deliver(_make_payload()))
        assert not result.success
        assert "AFFiNE delivery failed" in result.error

    def test_no_affine_sync_configured(self):
        router = DeliveryRouter(affine_sync=None)
        result = _run(router.deliver(_make_payload()))
        assert not result.success
        assert "not configured" in result.error


# ===================================================================
# 4. Dual Delivery — AC2 (4 tests)
# ===================================================================

class TestDualDelivery:
    def test_both_target_ac2(self):
        """AC2 — VPO appears in both AFFiNE and Notion."""
        affine = MockAFFiNeSync()
        notion = MockNotionSync()
        router = DeliveryRouter(affine_sync=affine, notion_sync=notion)
        payload = _make_payload(delivery_target=DeliveryTargetFlag.both)
        result = _run(router.deliver(payload))
        assert result.success
        assert result.affine_delivered
        assert result.notion_delivered
        assert len(affine.entries) == 1
        assert len(notion.entries) == 1

    def test_both_affine_fails(self):
        notion = MockNotionSync()
        router = DeliveryRouter(affine_sync=FailingSync(), notion_sync=notion)
        payload = _make_payload(delivery_target=DeliveryTargetFlag.both)
        result = _run(router.deliver(payload))
        assert not result.success  # both required
        assert result.notion_delivered

    def test_notion_only(self):
        notion = MockNotionSync()
        router = DeliveryRouter(notion_sync=notion)
        payload = _make_payload(delivery_target=DeliveryTargetFlag.notion_only)
        result = _run(router.deliver(payload))
        assert result.success
        assert result.notion_delivered
        assert not result.affine_delivered

    def test_notion_only_not_configured(self):
        router = DeliveryRouter()  # Nothing configured
        payload = _make_payload(delivery_target=DeliveryTargetFlag.notion_only)
        result = _run(router.deliver(payload))
        assert not result.success


# ===================================================================
# 5. Deep Link — AC4 (2 tests)
# ===================================================================

class TestDeepLink:
    def test_deep_link_in_entry_ac4(self):
        """AC4 — Deep link propagated to console entry."""
        affine = MockAFFiNeSync()
        router = DeliveryRouter(affine_sync=affine)
        payload = _make_payload(canva_app_deep_link="https://canva.ccp/edit/comp-001")
        _run(router.deliver(payload))
        entry = affine.entries[0]["payload"]
        assert entry["deep_link"] == "https://canva.ccp/edit/comp-001"

    def test_deep_link_none_handled(self):
        affine = MockAFFiNeSync()
        router = DeliveryRouter(affine_sync=affine)
        payload = _make_payload(canva_app_deep_link=None)
        _run(router.deliver(payload))
        entry = affine.entries[0]["payload"]
        assert entry["deep_link"] is None


# ===================================================================
# 6. Webhook Handler (3 tests)
# ===================================================================

class TestWebhookHandler:
    def test_handle_raw_payload(self):
        affine = MockAFFiNeSync()
        router = DeliveryRouter(affine_sync=affine)
        handler = CanvaApproveHandler(router)
        raw = _make_payload().model_dump()
        result = _run(handler.handle(raw))
        assert result.success
        assert result.affine_delivered

    def test_handle_with_both(self):
        affine = MockAFFiNeSync()
        notion = MockNotionSync()
        router = DeliveryRouter(affine_sync=affine, notion_sync=notion)
        handler = CanvaApproveHandler(router)
        raw = _make_payload(delivery_target=DeliveryTargetFlag.both).model_dump()
        result = _run(handler.handle(raw))
        assert result.success
        assert result.affine_delivered and result.notion_delivered

    def test_handle_invalid_payload(self):
        router = DeliveryRouter(affine_sync=MockAFFiNeSync())
        handler = CanvaApproveHandler(router)
        with pytest.raises(Exception):
            _run(handler.handle({"bad": "data"}))


# ===================================================================
# 7. Constants & SQL (2 tests)
# ===================================================================

class TestConstants:
    def test_vpc_section(self):
        assert VPC_SECTION == "visual-production-console"
        assert "tiar_decay_audit" in COLLAPSIBLE_AUDIT_KEYS

    def test_sql_schema(self):
        assert "vpo_entries" in VPO_ENTRIES_SQL
        assert "asset_id" in VPO_ENTRIES_SQL
