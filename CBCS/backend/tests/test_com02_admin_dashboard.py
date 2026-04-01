"""
FR-COM-02 — Global Admin Dashboard (Factory Floor)

Test Suite: Step 27 Build

Coverage:
- AC1: Review queue — all pending items visible, approve works
- AC2: Rejection with notes — coach sees rejection reason
- AC3: Traffic Control — active renders, failures, retry
- AC4: Treasury — revenue calculation ($500+$800=$1300)
- AC5: Coach isolation — 403 Forbidden on coach access attempt
- AC6: Real-time — new item appears in queue (WebSocket simulated)
- CBAR Q6: LoRA version lock check at approval
- Safety: Concurrent admin, cross-tenant, idempotency
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from core.commercial_models import (
    AdminActionType,
    CoachSubscriptionRow,
    FactoryFloorItem,
    SubscriptionStatus,
    SubscriptionTier,
)
from core.admin_dashboard import (
    AdminAuthGuard,
    AdminDashboardService,
)


# =====================================================
#  Fixtures
# =====================================================

def _make_auth() -> AdminAuthGuard:
    auth = AdminAuthGuard()
    auth.register_admin("admin-001", "admin", "token-admin-001")
    auth.register_admin("admin-002", "operator", "token-admin-002")
    return auth


def _make_dashboard() -> AdminDashboardService:
    auth = _make_auth()
    return AdminDashboardService(auth)


def _make_review_item(
    coach_id: str = "coach-alpha",
    content_id: str | None = None,
    lora_version_id: str | None = None,
) -> FactoryFloorItem:
    return FactoryFloorItem(
        content_id=content_id or str(uuid.uuid4()),
        coach_id=coach_id,
        coach_name=f"Coach {coach_id[-5:]}",
        content_type="video",
        status="pending_review",
        generation_timestamp=datetime.now(timezone.utc),
        pipeline_stage="render_complete",
        lora_version_id=lora_version_id,
    )


def _make_subscription(coach_id: str, **kwargs) -> CoachSubscriptionRow:
    defaults = {
        "coach_id": coach_id,
        "stripe_customer_id": f"cus_{coach_id[:8]}",
        "stripe_subscription_id": f"sub_{coach_id[:8]}",
        "stripe_metered_item_id": f"si_{coach_id[:8]}",
        "tier": SubscriptionTier.BASE,
        "weekly_base_price_cents": 2500,
        "cbcs_unit_price_cents": 400,
        "status": SubscriptionStatus.ACTIVE,
        "active_client_count": 0,
    }
    defaults.update(kwargs)
    return CoachSubscriptionRow(**defaults)


# =====================================================
#  AC1: Review Queue — All Pending Items Visible
# =====================================================

class TestAC1ReviewQueue:

    def test_all_coaches_pending_items_visible(self):
        dashboard = _make_dashboard()

        dashboard.add_to_review_queue(_make_review_item("coach-a"))
        dashboard.add_to_review_queue(_make_review_item("coach-b"))
        dashboard.add_to_review_queue(_make_review_item("coach-c"))

        items = dashboard.get_review_queue("token-admin-001")
        assert len(items) == 3

    def test_approve_changes_status(self):
        dashboard = _make_dashboard()
        item = _make_review_item("coach-a", content_id="vid-001")
        dashboard.add_to_review_queue(item)

        action = dashboard.approve_content("token-admin-001", "vid-001")

        assert item.status == "approved"
        assert action.action_type == AdminActionType.APPROVE

    def test_approve_writes_receipt(self):
        dashboard = _make_dashboard()
        item = _make_review_item("coach-a", content_id="vid-001")
        dashboard.add_to_review_queue(item)

        action = dashboard.approve_content("token-admin-001", "vid-001")

        assert action.receipt_chain_block is not None
        receipts = dashboard.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "ADMIN_ACTION"

    def test_filter_by_coach(self):
        dashboard = _make_dashboard()
        dashboard.add_to_review_queue(_make_review_item("coach-a"))
        dashboard.add_to_review_queue(_make_review_item("coach-b"))

        items = dashboard.get_review_queue("token-admin-001", coach_filter="coach-a")
        assert len(items) == 1
        assert items[0].coach_id == "coach-a"


# =====================================================
#  AC2: Rejection with Notes
# =====================================================

class TestAC2RejectionWithNotes:

    def test_reject_with_notes(self):
        dashboard = _make_dashboard()
        item = _make_review_item("coach-b", content_id="vid-002")
        dashboard.add_to_review_queue(item)

        action = dashboard.reject_content(
            "token-admin-001", "vid-002",
            notes="Audio out of sync at 0:15.",
        )

        assert item.status == "rejected"
        assert action.notes == "Audio out of sync at 0:15."

    def test_rejected_item_leaves_queue(self):
        dashboard = _make_dashboard()
        item = _make_review_item("coach-b", content_id="vid-002")
        dashboard.add_to_review_queue(item)

        dashboard.reject_content("token-admin-001", "vid-002", notes="Bad audio")

        pending = dashboard.get_review_queue("token-admin-001")
        assert len(pending) == 0  # Rejected item no longer pending


# =====================================================
#  AC3: Traffic Control
# =====================================================

class TestAC3TrafficControl:

    def test_health_snapshot(self):
        dashboard = _make_dashboard()

        snapshot = dashboard.record_health_snapshot(
            active_renders=2,
            failed_24h=1,
            failed_by_type={"audio_sync": 1},
            avg_render_time_seconds=45.0,
            gpu_utilization_pct=78.5,
            total_active_coaches=10,
        )

        assert snapshot.active_renders == 2
        assert snapshot.failed_24h == 1
        assert snapshot.failed_by_type == {"audio_sync": 1}

    def test_latest_health(self):
        dashboard = _make_dashboard()
        dashboard.record_health_snapshot(active_renders=1)
        dashboard.record_health_snapshot(active_renders=3)

        latest = dashboard.get_latest_health()
        assert latest.active_renders == 3

    def test_regenerate_content(self):
        dashboard = _make_dashboard()
        item = _make_review_item("coach-a", content_id="vid-003")
        dashboard.add_to_review_queue(item)

        action = dashboard.regenerate_content("token-admin-001", "vid-003")

        assert item.status == "regenerating"
        assert action.action_type == AdminActionType.REGENERATE


# =====================================================
#  AC4: Treasury — Revenue Calculation
# =====================================================

class TestAC4Treasury:

    def test_revenue_10_base_5_premium(self):
        """10 coaches $25/week + 5 coaches $50/week + 200 CBCS users."""
        dashboard = _make_dashboard()

        subs = []
        for i in range(10):
            subs.append(_make_subscription(
                f"coach-base-{i}",
                weekly_base_price_cents=2500,
                active_client_count=10,  # 100 CBCS users from base
            ))
        for i in range(5):
            subs.append(_make_subscription(
                f"coach-prem-{i}",
                tier=SubscriptionTier.PREMIUM,
                weekly_base_price_cents=5000,
                active_client_count=20,  # 100 CBCS users from premium
            ))

        metrics = dashboard.compute_treasury_metrics(
            "token-admin-001", subs, aws_cost_cents=50000,
        )

        # Base revenue: 10 × $25 = $250 → 25000 cents
        assert metrics.revenue_subscriptions_cents == 10 * 2500 + 5 * 5000  # 50000
        # CBCS revenue: 200 × $4 = $800 → 80000 cents
        assert metrics.revenue_cbcs_cents == (100 * 400) + (100 * 400)  # 80000
        assert metrics.revenue_total_cents == 130000
        assert metrics.cbcs_users_this_week == 200
        assert metrics.total_active_coaches == 15

    def test_failed_payments_in_treasury(self):
        dashboard = _make_dashboard()

        subs = [
            _make_subscription("coach-ok", status=SubscriptionStatus.ACTIVE),
            _make_subscription("coach-fail", status=SubscriptionStatus.PAST_DUE),
        ]

        metrics = dashboard.compute_treasury_metrics("token-admin-001", subs)

        assert len(metrics.failed_payments) == 1
        assert metrics.failed_payments[0]["coach_id"] == "coach-fail"

    def test_margin_calculation(self):
        dashboard = _make_dashboard()
        subs = [_make_subscription("coach-1", weekly_base_price_cents=10000)]

        metrics = dashboard.compute_treasury_metrics("token-admin-001", subs, aws_cost_cents=4000)

        # Revenue: 10000, cost: 4000, margin: 60%
        assert metrics.margin_pct == 60.0

    def test_aws_cost_warning(self):
        dashboard = _make_dashboard()
        subs = [_make_subscription("coach-1", weekly_base_price_cents=10000)]

        metrics = dashboard.compute_treasury_metrics("token-admin-001", subs, aws_cost_cents=5000)
        alerts = dashboard.check_treasury_alerts(metrics)

        # Margin 50% → 100-40=60% threshold → 50 < 60 → warning
        assert any(a["type"] == "AWS_COST_WARNING" for a in alerts)


# =====================================================
#  AC5: Coach Isolation — 403 Forbidden
# =====================================================

class TestAC5CoachIsolation:

    def test_coach_token_blocked(self):
        dashboard = _make_dashboard()

        with pytest.raises(PermissionError):
            dashboard.get_review_queue("invalid-token")

    def test_no_token_blocked(self):
        dashboard = _make_dashboard()

        with pytest.raises(PermissionError):
            dashboard.get_review_queue(None)

    def test_admin_token_allowed(self):
        dashboard = _make_dashboard()
        dashboard.add_to_review_queue(_make_review_item("coach-a"))

        items = dashboard.get_review_queue("token-admin-001")
        assert len(items) == 1

    def test_approve_requires_admin(self):
        dashboard = _make_dashboard()
        item = _make_review_item("coach-a", content_id="vid-001")
        dashboard.add_to_review_queue(item)

        with pytest.raises(PermissionError):
            dashboard.approve_content("fake-token", "vid-001")

    def test_treasury_requires_admin(self):
        dashboard = _make_dashboard()

        with pytest.raises(PermissionError):
            dashboard.compute_treasury_metrics("bad-token", [])


# =====================================================
#  AC6: Real-Time — New Item Appears
# =====================================================

class TestAC6RealTime:

    def test_new_item_appears_in_queue(self):
        """Simulates real-time: item added while admin has queue open."""
        dashboard = _make_dashboard()

        # Initial queue
        dashboard.add_to_review_queue(_make_review_item("coach-a"))
        assert len(dashboard.get_review_queue("token-admin-001")) == 1

        # New render completes (WebSocket push simulated)
        dashboard.add_to_review_queue(_make_review_item("coach-b"))
        assert len(dashboard.get_review_queue("token-admin-001")) == 2


# =====================================================
#  CBAR Q6: LoRA Version Lock
# =====================================================

class TestCBARQ6LoRAVersionLock:

    def test_matching_lora_version_approves_cleanly(self):
        dashboard = _make_dashboard()
        dashboard.register_lora_version("coach-a", "v1.0")

        item = _make_review_item("coach-a", content_id="vid-001", lora_version_id="v1.0")
        dashboard.add_to_review_queue(item)

        action = dashboard.approve_content("token-admin-001", "vid-001")

        assert "match" in action.notes

    def test_mismatched_lora_flags_stale(self):
        dashboard = _make_dashboard()
        dashboard.register_lora_version("coach-a", "v2.0")  # Current

        item = _make_review_item("coach-a", content_id="vid-001", lora_version_id="v1.0")
        dashboard.add_to_review_queue(item)

        action = dashboard.approve_content("token-admin-001", "vid-001")

        assert "stale" in action.notes.lower() or "rerender" in action.notes.lower()

    def test_no_lora_version_skips_check(self):
        dashboard = _make_dashboard()

        item = _make_review_item("coach-a", content_id="vid-001")  # No lora_version_id
        dashboard.add_to_review_queue(item)

        action = dashboard.approve_content("token-admin-001", "vid-001")
        assert item.status == "approved"


# =====================================================
#  Safety: Cross-Tenant Actions
# =====================================================

class TestCrossTenantSafety:

    def test_approve_only_affects_target(self):
        dashboard = _make_dashboard()
        item_a = _make_review_item("coach-a", content_id="vid-a")
        item_b = _make_review_item("coach-b", content_id="vid-b")
        dashboard.add_to_review_queue(item_a)
        dashboard.add_to_review_queue(item_b)

        dashboard.approve_content("token-admin-001", "vid-a")

        assert item_a.status == "approved"
        assert item_b.status == "pending_review"

    def test_concurrent_approve_idempotent(self):
        """Two admins approve same video → no double action."""
        dashboard = _make_dashboard()
        item = _make_review_item("coach-a", content_id="vid-001")
        dashboard.add_to_review_queue(item)

        dashboard.approve_content("token-admin-001", "vid-001")
        # Second approve — item already approved, but no crash
        dashboard.approve_content("token-admin-002", "vid-001")

        assert item.status == "approved"
        # Both actions logged
        actions = dashboard.get_action_log()
        assert len(actions) == 2

    def test_nonexistent_content_raises(self):
        dashboard = _make_dashboard()

        with pytest.raises(ValueError):
            dashboard.approve_content("token-admin-001", "nonexistent-id")
