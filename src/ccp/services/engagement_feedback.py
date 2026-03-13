"""
CCP Engagement Feedback Ingestion
Task 5.02 — Captures content engagement metrics and tags resonance markers.

Tracks per content piece:
- Save count, share count, comment count
- Engagement rate relative to coach's baseline
- Theme correlation with high-performing content

High-performing themes are tagged as "resonance markers" in the
coach profile and feed into the next ccf-analyze cycle.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class EngagementMetrics(BaseModel):
    """Engagement data for a single content piece."""

    asset_id: str
    format_type: str
    topic: str
    published_date: Optional[datetime] = None
    saves: int = 0
    shares: int = 0
    comments: int = 0
    impressions: int = 0
    engagement_rate: float = Field(default=0.0, description="(saves+shares+comments)/impressions")
    is_resonance_marker: bool = False
    resonance_reason: str = ""


class EngagementFeedback:
    """Ingest and analyze content engagement metrics."""

    RESONANCE_THRESHOLD = 2.0  # 2x above rolling average = resonance marker

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._data_dir = Path(
            f"coaches/{self.coach_acronym}/intelligence/memory/semantic"
        )
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._metrics_file = self._data_dir / "engagement_metrics.jsonl"

    def ingest(self, metrics: EngagementMetrics) -> EngagementMetrics:
        """Ingest engagement data for a content piece.

        Automatically checks if the piece qualifies as a resonance marker.
        """
        # Calculate engagement rate
        if metrics.impressions > 0:
            metrics.engagement_rate = (
                (metrics.saves + metrics.shares + metrics.comments) / metrics.impressions
            )

        # Check against rolling average
        avg_rate = self._get_rolling_average()
        if avg_rate > 0 and metrics.engagement_rate >= avg_rate * self.RESONANCE_THRESHOLD:
            metrics.is_resonance_marker = True
            metrics.resonance_reason = (
                f"Engagement rate {metrics.engagement_rate:.2%} is "
                f"{metrics.engagement_rate / avg_rate:.1f}x above average ({avg_rate:.2%})"
            )

        # Save
        with open(self._metrics_file, "a", encoding="utf-8") as f:
            f.write(metrics.model_dump_json() + "\n")

        # If resonance marker, save to coach profile
        if metrics.is_resonance_marker:
            self._save_resonance_marker(metrics)

        self.receipt_chain.log(
            agent_id="engagement_feedback",
            action="ingest_metrics",
            asset_id=metrics.asset_id,
            output_summary=(
                f"{'🟣 RESONANCE HIT' if metrics.is_resonance_marker else 'Normal'}: "
                f"rate={metrics.engagement_rate:.2%}, saves={metrics.saves}, shares={metrics.shares}"
            ),
            decision="resonance_marker" if metrics.is_resonance_marker else "normal",
        )

        return metrics

    def get_resonance_markers(self) -> list[dict]:
        """Get all resonance markers for content planning."""
        markers_file = self._data_dir / "resonance_markers.json"
        if markers_file.exists():
            return json.loads(markers_file.read_text(encoding="utf-8"))
        return []

    def get_top_performing(self, limit: int = 10) -> list[EngagementMetrics]:
        """Get top performing content by engagement rate."""
        all_metrics = self._load_all()
        sorted_metrics = sorted(all_metrics, key=lambda m: m.engagement_rate, reverse=True)
        return sorted_metrics[:limit]

    def _get_rolling_average(self, window: int = 20) -> float:
        """Get rolling average engagement rate from last N pieces."""
        all_metrics = self._load_all()
        if not all_metrics:
            return 0.0
        recent = all_metrics[-window:]
        rates = [m.engagement_rate for m in recent if m.engagement_rate > 0]
        return sum(rates) / len(rates) if rates else 0.0

    def _save_resonance_marker(self, metrics: EngagementMetrics) -> None:
        """Save a resonance marker to the dedicated file."""
        markers_file = self._data_dir / "resonance_markers.json"
        markers = []
        if markers_file.exists():
            markers = json.loads(markers_file.read_text(encoding="utf-8"))
        markers.append({
            "asset_id": metrics.asset_id,
            "format_type": metrics.format_type,
            "topic": metrics.topic,
            "engagement_rate": metrics.engagement_rate,
            "reason": metrics.resonance_reason,
            "tagged_at": datetime.now(timezone.utc).isoformat(),
        })
        markers_file.write_text(json.dumps(markers, indent=2), encoding="utf-8")

    def _load_all(self) -> list[EngagementMetrics]:
        if not self._metrics_file.exists():
            return []
        metrics = []
        with open(self._metrics_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    metrics.append(EngagementMetrics.model_validate_json(line))
        return metrics
