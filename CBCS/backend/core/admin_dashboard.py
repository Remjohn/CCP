"""
FR-COM-02 — Global Admin Dashboard (Factory Floor)
Build Step 27 · DEP-COM-005, DEP-COM-006

Factory Floor (review queue), Traffic Control (pipeline health),
Treasury (billing & revenue), admin-only authentication.

CBAR Q6: LoRA Version Lock at Factory Floor approval.
CBAR Q9: mv_campaign_analytics materialized view (coach_id stripped).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from core.commercial_models import (
    HEALTH_SNAPSHOT_INTERVAL_MINUTES,
    RECEIPT_STAGE_ADMIN_ACTION,
    RECEIPT_STAGE_HEALTH_SNAPSHOT,
    TREASURY_AWS_COST_WARNING_PCT,
    TREASURY_CBCS_CHURN_WEEKLY_THRESHOLD,
    TREASURY_PAYMENT_FAILURE_ESCALATION_HOURS,
    AdminActionRow,
    AdminActionType,
    CoachSubscriptionRow,
    FactoryFloorItem,
    LoRAVersionCheckResult,
    PipelineHealthSnapshotRow,
    SubscriptionStatus,
    SubscriptionTier,
    TreasuryMetrics,
    build_receipt,
    compute_receipt_hash,
)


# =====================================================
#  Authentication Guard
# =====================================================

ADMIN_ROLES = {"admin", "operator", "system_admin"}


class AdminAuthGuard:
    """
    § 3: Admin-only authentication.
    Coaches do NOT have accounts on the admin dashboard.
    """

    def __init__(self) -> None:
        self._admin_tokens: dict[str, dict[str, str]] = {}

    def register_admin(self, user_id: str, role: str, token: str) -> None:
        """Register an admin user."""
        self._admin_tokens[token] = {"user_id": user_id, "role": role}

    def authenticate(self, token: str | None) -> dict[str, str] | None:
        """
        Returns admin user dict if valid, None if invalid.
        """
        if token is None:
            return None
        return self._admin_tokens.get(token)

    def is_admin(self, token: str | None) -> bool:
        admin = self.authenticate(token)
        if admin is None:
            return False
        return admin.get("role", "") in ADMIN_ROLES


# =====================================================
#  DEP-COM-005: Admin Dashboard Service
# =====================================================

class AdminDashboardService:
    """
    Global Admin Dashboard — Factory Floor, Traffic Control, Treasury.
    Uses service-role key (bypasses RLS) for global aggregation.
    """

    def __init__(self, auth_guard: AdminAuthGuard) -> None:
        self._auth_guard = auth_guard
        self._review_queue: list[FactoryFloorItem] = []
        self._action_log: list[AdminActionRow] = []
        self._health_snapshots: list[PipelineHealthSnapshotRow] = []
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

        # LoRA version registry (CBAR Q6)
        self._lora_versions: dict[str, str] = {}  # coach_id → current lora version

    # -------------------------------------------------
    #  Factory Floor: Review Queue
    # -------------------------------------------------

    def add_to_review_queue(self, item: FactoryFloorItem) -> None:
        """Add content to the review queue (called by CMF pipeline on render complete)."""
        self._review_queue.append(item)

    def get_review_queue(
        self,
        token: str,
        coach_filter: str | None = None,
        content_type_filter: str | None = None,
    ) -> list[FactoryFloorItem]:
        """
        § 4 Stage 1: Factory Floor — unified review queue.
        Filters: By coach, by content type.
        """
        if not self._auth_guard.is_admin(token):
            raise PermissionError("403 Forbidden — admin access required.")

        items = [i for i in self._review_queue if i.status == "pending_review"]

        if coach_filter:
            items = [i for i in items if i.coach_id == coach_filter]
        if content_type_filter:
            items = [i for i in items if i.content_type == content_type_filter]

        return items

    def approve_content(
        self,
        token: str,
        content_id: str,
    ) -> AdminActionRow:
        """
        § 4 Stage 1: Approve → status: approved.
        CBAR Q6: LoRA Version Lock check before delivery.
        """
        admin = self._auth_guard.authenticate(token)
        if admin is None or admin.get("role") not in ADMIN_ROLES:
            raise PermissionError("403 Forbidden — admin access required.")

        item = self._find_item(content_id)
        if item is None:
            raise ValueError(f"Content {content_id} not found in review queue.")

        # CBAR Q6: LoRA Version Lock check
        lora_check = self._check_lora_version(item)

        item.status = "approved"

        action = AdminActionRow(
            admin_user_id=admin["user_id"],
            action_type=AdminActionType.APPROVE,
            target_coach_id=item.coach_id,
            target_content_id=content_id,
            notes=f"LoRA check: {'match' if lora_check.match else lora_check.action_required}",
        )
        self._action_log.append(action)

        # Receipt Chain Guard (DEP-ENG-041)
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_ADMIN_ACTION,
            agent_name="admin_dashboard",
            input_payload={"content_id": content_id, "action": "approve"},
            output_payload={
                "status": "approved",
                "lora_match": lora_check.match,
                "admin_user_id": admin["user_id"],
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        action.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return action

    def reject_content(
        self,
        token: str,
        content_id: str,
        notes: str = "",
    ) -> AdminActionRow:
        """§ 4 Stage 1: Reject → status: rejected + notes."""
        admin = self._auth_guard.authenticate(token)
        if admin is None or admin.get("role") not in ADMIN_ROLES:
            raise PermissionError("403 Forbidden — admin access required.")

        item = self._find_item(content_id)
        if item is None:
            raise ValueError(f"Content {content_id} not found in review queue.")

        item.status = "rejected"

        action = AdminActionRow(
            admin_user_id=admin["user_id"],
            action_type=AdminActionType.REJECT,
            target_coach_id=item.coach_id,
            target_content_id=content_id,
            notes=notes,
        )
        self._action_log.append(action)

        # Receipt
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_ADMIN_ACTION,
            agent_name="admin_dashboard",
            input_payload={"content_id": content_id, "action": "reject", "notes": notes},
            output_payload={"status": "rejected"},
            previous_receipt_hash=self._last_receipt_hash,
        )
        action.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return action

    def regenerate_content(
        self,
        token: str,
        content_id: str,
    ) -> AdminActionRow:
        """§ 4 Stage 1: Regenerate → status: regenerating → re-trigger CMF pipeline."""
        admin = self._auth_guard.authenticate(token)
        if admin is None or admin.get("role") not in ADMIN_ROLES:
            raise PermissionError("403 Forbidden — admin access required.")

        item = self._find_item(content_id)
        if item is None:
            raise ValueError(f"Content {content_id} not found in review queue.")

        item.status = "regenerating"

        action = AdminActionRow(
            admin_user_id=admin["user_id"],
            action_type=AdminActionType.REGENERATE,
            target_coach_id=item.coach_id,
            target_content_id=content_id,
        )
        self._action_log.append(action)

        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_ADMIN_ACTION,
            agent_name="admin_dashboard",
            input_payload={"content_id": content_id, "action": "regenerate"},
            output_payload={"status": "regenerating"},
            previous_receipt_hash=self._last_receipt_hash,
        )
        action.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return action

    # -------------------------------------------------
    #  CBAR Q6: LoRA Version Lock
    # -------------------------------------------------

    def register_lora_version(self, coach_id: str, version_id: str) -> None:
        """Register current LoRA version for a coach."""
        self._lora_versions[coach_id] = version_id

    def _check_lora_version(self, item: FactoryFloorItem) -> LoRAVersionCheckResult:
        """
        CBAR Q6: Check if asset's LoRA version matches current registry.
        Mismatch → operator dialog (stale-approve or re-render).
        """
        current_version = self._lora_versions.get(item.coach_id)

        if item.lora_version_id is None or current_version is None:
            return LoRAVersionCheckResult(match=True)

        if item.lora_version_id == current_version:
            return LoRAVersionCheckResult(
                match=True,
                asset_lora_version=item.lora_version_id,
                current_lora_version=current_version,
            )

        return LoRAVersionCheckResult(
            match=False,
            asset_lora_version=item.lora_version_id,
            current_lora_version=current_version,
            action_required="stale_approve_or_rerender",
        )

    # -------------------------------------------------
    #  Traffic Control: Pipeline Health
    # -------------------------------------------------

    def record_health_snapshot(
        self,
        active_renders: int = 0,
        failed_24h: int = 0,
        failed_by_type: dict[str, int] | None = None,
        avg_render_time_seconds: float | None = None,
        gpu_utilization_pct: float | None = None,
        total_active_coaches: int = 0,
        revenue_week_cents: int = 0,
        aws_cost_week_cents: int = 0,
    ) -> PipelineHealthSnapshotRow:
        """§ 4 Stage 2: Record 15-minute health snapshot."""
        pending = len([i for i in self._review_queue if i.status == "pending_review"])
        margin = 0.0
        if revenue_week_cents > 0:
            margin = ((revenue_week_cents - aws_cost_week_cents) / revenue_week_cents) * 100

        snapshot = PipelineHealthSnapshotRow(
            active_renders=active_renders,
            failed_24h=failed_24h,
            failed_by_type=failed_by_type,
            avg_render_time_seconds=avg_render_time_seconds,
            gpu_utilization_pct=gpu_utilization_pct,
            total_active_coaches=total_active_coaches,
            total_pending_review=pending,
            revenue_week_cents=revenue_week_cents,
            aws_cost_week_cents=aws_cost_week_cents,
            margin_pct=margin,
        )
        self._health_snapshots.append(snapshot)
        return snapshot

    def get_latest_health(self) -> PipelineHealthSnapshotRow | None:
        if not self._health_snapshots:
            return None
        return self._health_snapshots[-1]

    # -------------------------------------------------
    #  Treasury: Revenue & Billing
    # -------------------------------------------------

    def compute_treasury_metrics(
        self,
        token: str,
        subscriptions: list[CoachSubscriptionRow],
        aws_cost_cents: int = 0,
    ) -> TreasuryMetrics:
        """
        § 4 Stage 3: Treasury — global billing status, revenue.
        Requires admin token.
        """
        if not self._auth_guard.is_admin(token):
            raise PermissionError("403 Forbidden — admin access required.")

        active_coaches = [s for s in subscriptions if s.status == SubscriptionStatus.ACTIVE]
        coaches_by_tier: dict[str, int] = {}
        revenue_subs = 0
        revenue_cbcs = 0
        total_cbcs_users = 0
        failed_payments: list[dict[str, Any]] = []

        for sub in subscriptions:
            tier_key = sub.tier.value
            coaches_by_tier[tier_key] = coaches_by_tier.get(tier_key, 0) + 1

            if sub.status == SubscriptionStatus.ACTIVE:
                revenue_subs += sub.weekly_base_price_cents
                cbcs_revenue = sub.active_client_count * sub.cbcs_unit_price_cents
                revenue_cbcs += cbcs_revenue
                total_cbcs_users += sub.active_client_count
            elif sub.status == SubscriptionStatus.PAST_DUE:
                failed_payments.append({
                    "coach_id": sub.coach_id,
                    "status": sub.status.value,
                    "last4": sub.payment_method_last4,
                })

        total_revenue = revenue_subs + revenue_cbcs
        margin = 0.0
        if total_revenue > 0:
            margin = ((total_revenue - aws_cost_cents) / total_revenue) * 100

        return TreasuryMetrics(
            total_active_coaches=len(active_coaches),
            coaches_by_tier=coaches_by_tier,
            cbcs_users_this_week=total_cbcs_users,
            revenue_subscriptions_cents=revenue_subs,
            revenue_cbcs_cents=revenue_cbcs,
            revenue_total_cents=total_revenue,
            aws_cost_cents=aws_cost_cents,
            margin_pct=round(margin, 1),
            failed_payments=failed_payments,
        )

    def check_treasury_alerts(
        self,
        metrics: TreasuryMetrics,
    ) -> list[dict[str, str]]:
        """Treasury alert generation."""
        alerts: list[dict[str, str]] = []

        if metrics.margin_pct < (100 - TREASURY_AWS_COST_WARNING_PCT):
            alerts.append({
                "type": "AWS_COST_WARNING",
                "message": f"AWS cost exceeding {TREASURY_AWS_COST_WARNING_PCT}% of revenue (margin: {metrics.margin_pct}%).",
            })

        if metrics.failed_payments:
            alerts.append({
                "type": "PAYMENT_FAILURES",
                "message": f"{len(metrics.failed_payments)} coach(es) with failed payments.",
            })

        return alerts

    # -------------------------------------------------
    #  Helpers
    # -------------------------------------------------

    def _find_item(self, content_id: str) -> FactoryFloorItem | None:
        for item in self._review_queue:
            if item.content_id == content_id:
                return item
        return None

    def get_action_log(self) -> list[AdminActionRow]:
        return list(self._action_log)

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)
