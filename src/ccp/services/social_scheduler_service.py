"""FR-CA11-18 — Conscious Social Scheduling & Performance Analysis.

DEP-ENG-099: Scheduler Deployment (Docker on AWS)
DEP-ENG-100: Post Queuing Integration (CMF → scheduler)
DEP-ENG-101: Performance Ingestion (6h/24h/48h/168h polling)
DEP-ENG-102: Social Media OS Template (AFFiNE dashboard)
DEP-ENG-103: CRAL Feedback Loop (performance → content strategy)

Agent: Sofia (Social Performance Analyst)
Stress Test Q39: ±4h temporal mutex, DAG_VIOLATION_COLLISION, human priority
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    COLLECTION_CYCLES,
    ENGAGEMENT_WEIGHTS,
    ROLLING_AVERAGE_WINDOW_DAYS,
    SOCIAL_AGENT_NAME,
    TEMPORAL_MUTEX_HOURS,
    TOP_PERFORMER_THRESHOLD,
    CollectionCycle,
    EngagementMetrics,
    QueuePostRequest,
    SocialPerformanceRecord,
    SocialPlatform,
    SocialPostRecord,
    SocialPostStatus,
    SocialSchedulingError,
    SocialSchedulingResult,
    TemporalMutexResult,
)

# ---------------------------------------------------------------------------
# SQL — social_posts + social_performance tables (§5 Data Model)
# ---------------------------------------------------------------------------

SOCIAL_POSTS_SQL = """
CREATE TABLE IF NOT EXISTS social_posts (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id            UUID NOT NULL REFERENCES coaches(id),
    content_id          UUID,
    platform            VARCHAR(30) NOT NULL,
    caption             TEXT,
    media_urls          JSONB,
    hashtags            JSONB,
    scheduler_post_id   VARCHAR(255),
    scheduled_at        TIMESTAMPTZ,
    published_at        TIMESTAMPTZ,
    status              VARCHAR(20) DEFAULT 'draft',
    is_human_scheduled  BOOLEAN DEFAULT FALSE,
    receipt_chain_id    UUID REFERENCES receipt_chain(id),
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_social_posts_coach ON social_posts(coach_id);
CREATE INDEX IF NOT EXISTS idx_social_posts_status ON social_posts(status);
"""

SOCIAL_PERFORMANCE_SQL = """
CREATE TABLE IF NOT EXISTS social_performance (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id             UUID NOT NULL REFERENCES social_posts(id),
    views               INTEGER DEFAULT 0,
    likes               INTEGER DEFAULT 0,
    shares              INTEGER DEFAULT 0,
    comments            INTEGER DEFAULT 0,
    saves               INTEGER DEFAULT 0,
    ctr                 DECIMAL(5,4) DEFAULT 0,
    engagement_score    DECIMAL(8,2) DEFAULT 0,
    collection_cycle    VARCHAR(10) NOT NULL,
    is_top_performer    BOOLEAN DEFAULT FALSE,
    collected_at        TIMESTAMPTZ NOT NULL,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_social_performance_post ON social_performance(post_id);
CREATE INDEX IF NOT EXISTS idx_social_performance_top
    ON social_performance(is_top_performer) WHERE is_top_performer = TRUE;
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class SchedulerAPIProtocol(Protocol):
    async def create_post(self, platform: str, content: dict[str, Any]) -> str: ...
    async def get_metrics(self, scheduler_post_id: str) -> dict[str, Any]: ...


class SocialDatabaseProtocol(Protocol):
    async def insert_post(self, record: dict[str, Any]) -> str: ...
    async def update_post(self, post_id: str, fields: dict[str, Any]) -> None: ...
    async def insert_performance(self, record: dict[str, Any]) -> str: ...
    async def get_posts_in_window(
        self, coach_id: str, platform: str, start: datetime, end: datetime,
    ) -> list[dict[str, Any]]: ...
    async def get_rolling_average(
        self, coach_id: str, platform: str, window_days: int,
    ) -> float: ...


# ---------------------------------------------------------------------------
# Receipt utilities (FR47 DEP-ENG-041)
# ---------------------------------------------------------------------------


def _sha256(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _build_receipt(
    stage_name: str, agent_name: str,
    input_payload: Any, output_payload: Any,
    previous_receipt_hash: str = "",
) -> dict[str, Any]:
    return {
        "receipt_id": str(uuid.uuid4()),
        "previous_receipt_hash": previous_receipt_hash,
        "input_payload_hash": _sha256(input_payload),
        "output_payload_hash": _sha256(output_payload),
        "stage_name": stage_name,
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Pure functions
# ---------------------------------------------------------------------------


def calculate_engagement_score(metrics: EngagementMetrics) -> float:
    """Weighted composite engagement score.

    Formula: Σ(metric × weight) for views, likes, shares, comments, saves.
    """
    return round(
        metrics.views * ENGAGEMENT_WEIGHTS["views"]
        + metrics.likes * ENGAGEMENT_WEIGHTS["likes"]
        + metrics.shares * ENGAGEMENT_WEIGHTS["shares"]
        + metrics.comments * ENGAGEMENT_WEIGHTS["comments"]
        + metrics.saves * ENGAGEMENT_WEIGHTS["saves"],
        2,
    )


def is_top_performer(engagement_score: float, rolling_average: float) -> bool:
    """§4 Stage 3 Step 5: Flag if engagement exceeds 2x rolling average."""
    if rolling_average <= 0:
        return False
    return engagement_score >= (rolling_average * TOP_PERFORMER_THRESHOLD)


def check_temporal_mutex(
    scheduled_time: datetime,
    existing_posts: list[SocialPostRecord],
    is_human_scheduled: bool = False,
) -> TemporalMutexResult:
    """Stress Test Q39: ±4h temporal mutex check.

    If a post already exists within ±4h on the same platform,
    raises DAG_VIOLATION_COLLISION — unless the new post is human-scheduled
    (human posts always have priority).
    """
    window = timedelta(hours=TEMPORAL_MUTEX_HOURS)
    for post in existing_posts:
        if post.scheduled_at is None:
            continue
        diff = abs(scheduled_time - post.scheduled_at)
        if diff <= window:
            # Human-scheduled posts override auto-scheduled ones
            if is_human_scheduled and not post.is_human_scheduled:
                return TemporalMutexResult(
                    is_clear=True,
                    human_priority_override=True,
                    conflicting_post_id=post.post_id,
                )
            return TemporalMutexResult(
                is_clear=False,
                conflicting_post_id=post.post_id,
                conflict_platform=post.platform,
                conflict_time=post.scheduled_at,
            )

    return TemporalMutexResult(is_clear=True)


# ---------------------------------------------------------------------------
# Social Scheduling Service
# ---------------------------------------------------------------------------


class SocialSchedulerService:
    """FR-CA11-18 — Social Scheduling & Performance Analysis.

    Orchestrates post queuing, publish tracking, metric ingestion,
    top performer detection. All state mutations emit FR47 receipts.
    """

    def __init__(
        self,
        scheduler_api: SchedulerAPIProtocol | None = None,
        db: SocialDatabaseProtocol | None = None,
    ) -> None:
        self._scheduler = scheduler_api
        self._db = db
        self._receipt_chain: list[dict[str, Any]] = []

    @property
    def receipt_chain(self) -> list[dict[str, Any]]:
        return list(self._receipt_chain)

    def _emit_receipt(
        self, stage_name: str, input_payload: Any, output_payload: Any,
    ) -> dict[str, Any]:
        prev_hash = ""
        if self._receipt_chain:
            prev_hash = _sha256(self._receipt_chain[-1])
        receipt = _build_receipt(
            stage_name=stage_name,
            agent_name=SOCIAL_AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Stage 2: Post Queuing (DEP-ENG-100) --

    async def queue_post(self, request: QueuePostRequest) -> SocialSchedulingResult:
        """Queue content for social media publishing.

        AC1: auto-queue from CMF. AC2: multi-platform.
        Stress Test Q39: temporal mutex check per platform.
        """
        valid_platforms = [p.value for p in SocialPlatform]
        for p in request.platforms:
            if p not in valid_platforms:
                return SocialSchedulingResult(
                    success=False,
                    error=f"{SocialSchedulingError.INVALID_PLATFORM.value}: '{p}'",
                )

        posts: list[SocialPostRecord] = []
        for platform in request.platforms:
            # Q39: temporal mutex check
            existing = []
            if self._db:
                window = timedelta(hours=TEMPORAL_MUTEX_HOURS)
                raw = await self._db.get_posts_in_window(
                    request.coach_id, platform,
                    request.scheduled_time - window,
                    request.scheduled_time + window,
                )
                existing = [SocialPostRecord(**r) for r in raw]

            mutex_result = check_temporal_mutex(
                request.scheduled_time, existing, request.is_human_scheduled,
            )
            if not mutex_result.is_clear:
                return SocialSchedulingResult(
                    success=False,
                    error=(
                        f"{SocialSchedulingError.TEMPORAL_MUTEX_VIOLATION.value}: "
                        f"Post on {platform} conflicts with {mutex_result.conflicting_post_id} "
                        f"at {mutex_result.conflict_time}"
                    ),
                )

            # Create post record
            scheduler_post_id = None
            if self._scheduler:
                scheduler_post_id = await self._scheduler.create_post(platform, {
                    "caption": request.caption,
                    "media_urls": request.media_urls,
                    "hashtags": request.hashtags,
                    "scheduled_time": request.scheduled_time.isoformat(),
                })

            post = SocialPostRecord(
                coach_id=request.coach_id,
                content_id=request.content_id,
                platform=platform,
                caption=request.caption,
                media_urls=request.media_urls,
                hashtags=request.hashtags,
                scheduler_post_id=scheduler_post_id,
                scheduled_at=request.scheduled_time,
                status=SocialPostStatus.SCHEDULED.value,
                is_human_scheduled=request.is_human_scheduled,
            )

            if self._db:
                await self._db.insert_post(post.model_dump(mode="json"))

            posts.append(post)

        # Receipt: post-queue (state mutation: INSERT social_posts)
        self._emit_receipt(
            stage_name="post-queue",
            input_payload={
                "coach_id": request.coach_id,
                "platforms": request.platforms,
                "scheduled_time": request.scheduled_time.isoformat(),
            },
            output_payload={
                "post_ids": [p.post_id for p in posts],
                "status": SocialPostStatus.SCHEDULED.value,
            },
        )

        return SocialSchedulingResult(success=True, posts=posts)

    # -- Publish status update (AC3, AC7) --

    async def mark_published(
        self, post_id: str, published_at: datetime,
    ) -> SocialPostRecord:
        """Update post status to published. AC3 + AC7 receipt."""
        post = SocialPostRecord(
            post_id=post_id,
            coach_id="system",
            platform="pending",
            status=SocialPostStatus.PUBLISHED.value,
            published_at=published_at,
        )

        if self._db:
            await self._db.update_post(post_id, {
                "status": SocialPostStatus.PUBLISHED.value,
                "published_at": published_at.isoformat(),
            })

        # Receipt: post-publish (state mutation: UPDATE social_posts)
        self._emit_receipt(
            stage_name="post-publish",
            input_payload={"post_id": post_id},
            output_payload={
                "post_id": post_id,
                "status": SocialPostStatus.PUBLISHED.value,
                "published_at": published_at.isoformat(),
            },
        )

        return post

    # -- Stage 3: Performance Ingestion (DEP-ENG-101) --

    async def ingest_performance(
        self,
        post_id: str,
        metrics: EngagementMetrics,
        collection_cycle: str,
        rolling_average: float = 0.0,
    ) -> SocialPerformanceRecord:
        """Ingest performance metrics for a published post.

        AC4: metric row with collection_cycle.
        AC5: top performer detection.
        """
        score = calculate_engagement_score(metrics)
        top = is_top_performer(score, rolling_average)

        record = SocialPerformanceRecord(
            post_id=post_id,
            views=metrics.views,
            likes=metrics.likes,
            shares=metrics.shares,
            comments=metrics.comments,
            saves=metrics.saves,
            ctr=metrics.ctr,
            engagement_score=score,
            collection_cycle=collection_cycle,
            is_top_performer=top,
        )

        if self._db:
            await self._db.insert_performance(record.model_dump(mode="json"))

        return record

    # -- Receipt chain verification --

    def verify_receipt_chain(self) -> bool:
        if not self._receipt_chain:
            return True
        if self._receipt_chain[0]["previous_receipt_hash"] != "":
            return False
        for i in range(1, len(self._receipt_chain)):
            expected = _sha256(self._receipt_chain[i - 1])
            if self._receipt_chain[i]["previous_receipt_hash"] != expected:
                return False
        return True
