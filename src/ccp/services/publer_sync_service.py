"""
FR42 — Publer Automated Sync Service (DEP-ENG-037)
4-trigger content performance pipeline: Schedule → Publish → 48h → 7/30d snapshots.

AC1: Scheduling handshake with Publer API.
AC2: Engagement rate = (saves + shares + comments + likes) / reach.
AC3: Notion page genesis on publication.
AC4: Idempotent DB updates (upsert by universal_asset_id).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    ContentPerformanceRow,
)


class PublerSyncService:
    """
    FR42: Automated content performance sync from Publer.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        # In-memory store for idempotent updates (production: Supabase)
        self._performance_store: dict[str, ContentPerformanceRow] = {}

    # ── Trigger 1: Content Scheduling ──────────────────

    def schedule_content(
        self,
        *,
        universal_asset_id: str,
        publer_post_id: str,
        platform: str,
    ) -> ContentPerformanceRow:
        """
        FR42 AC1: Register a scheduled post.
        """
        row = ContentPerformanceRow(
            universal_asset_id=universal_asset_id,
            publer_post_id=publer_post_id,
            platform=platform,
        )

        self._upsert(row)

        self._receipt_chain.log(
            agent_id="PublerSyncService",
            action="CONTENT_SCHEDULED",
            asset_id=universal_asset_id,
            decision="SUCCESS",
            decision_rationale=f"platform={platform}, publer_id={publer_post_id}",
        )

        return row

    # ── Trigger 2: Publication Confirmation ────────────

    def confirm_publication(
        self,
        *,
        universal_asset_id: str,
        platform_post_url: str,
    ) -> ContentPerformanceRow:
        """
        FR42 §4.2: Confirm publication and record URL.
        """
        row = self._get_or_create(universal_asset_id)
        row.platform_post_url = platform_post_url
        row.published_at = datetime.now(timezone.utc).isoformat()

        self._upsert(row)

        self._receipt_chain.log(
            agent_id="PublerSyncService",
            action="PUBLICATION_CONFIRMED",
            asset_id=universal_asset_id,
            decision="SUCCESS",
        )

        return row

    # ── Trigger 3: 48h Performance Retrieval ───────────

    def ingest_48h_metrics(
        self,
        *,
        universal_asset_id: str,
        reach: int = 0,
        impressions: int = 0,
        saves: int = 0,
        shares: int = 0,
        comments: int = 0,
        likes: int = 0,
        video_views: int = 0,
    ) -> ContentPerformanceRow:
        """
        FR42 AC2: Ingest 48-hour metrics and compute engagement rate.
        engagement_rate = (saves + shares + comments + likes) / reach
        """
        row = self._get_or_create(universal_asset_id)
        row.reach = reach
        row.impressions = impressions
        row.saves = saves
        row.shares = shares
        row.comments = comments
        row.likes = likes
        row.video_views = video_views
        row.engagement_rate = row.computed_engagement_rate
        row.first_insights_at = datetime.now(timezone.utc).isoformat()

        self._upsert(row)

        self._receipt_chain.log(
            agent_id="PublerSyncService",
            action="48H_METRICS_INGESTED",
            asset_id=universal_asset_id,
            decision="SUCCESS",
            decision_rationale=f"reach={reach}, engagement={row.engagement_rate:.4f}",
        )

        return row

    # ── Trigger 4: 7/30-day Snapshots ──────────────────

    def ingest_snapshot(
        self,
        *,
        universal_asset_id: str,
        snapshot_day: int,
        snapshot_data: dict[str, Any],
    ) -> ContentPerformanceRow:
        """
        FR42 §4.4: Record 7-day or 30-day snapshot.
        """
        row = self._get_or_create(universal_asset_id)

        if snapshot_day == 7:
            row.day_7_snapshot = snapshot_data
        elif snapshot_day == 30:
            row.day_30_snapshot = snapshot_data
        else:
            raise ValueError(f"Unsupported snapshot day: {snapshot_day}. Must be 7 or 30.")

        self._upsert(row)

        self._receipt_chain.log(
            agent_id="PublerSyncService",
            action=f"DAY_{snapshot_day}_SNAPSHOT",
            asset_id=universal_asset_id,
            decision="SUCCESS",
        )

        return row

    # ── Accessors ──────────────────────────────────────

    def get_performance(self, universal_asset_id: str) -> Optional[ContentPerformanceRow]:
        return self._performance_store.get(universal_asset_id)

    @property
    def store_size(self) -> int:
        return len(self._performance_store)

    # ── Internals ──────────────────────────────────────

    def _upsert(self, row: ContentPerformanceRow) -> None:
        """FR42 AC4: Idempotent upsert by universal_asset_id."""
        self._performance_store[row.universal_asset_id] = row

    def _get_or_create(self, universal_asset_id: str) -> ContentPerformanceRow:
        if universal_asset_id not in self._performance_store:
            self._performance_store[universal_asset_id] = ContentPerformanceRow(
                universal_asset_id=universal_asset_id,
            )
        return self._performance_store[universal_asset_id]
