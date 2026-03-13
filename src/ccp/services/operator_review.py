"""
CCP Operator Review Queue
Task 2.12 — Post-validation review queue for operator approval.

After the Validation Team passes content, it enters this queue.
The Operator can approve, reject (with reason), or edit each piece.
Edits preserve the Receipt Chain with both original and edited versions.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class ReviewItem(BaseModel):
    """A single item in the operator review queue."""

    asset_id: str
    format_type: str
    format_label: str
    topic: str
    script: str
    word_count: int
    validation_scores: dict = Field(default_factory=dict)
    status: str = Field(default="pending")  # pending, approved, rejected, edited
    rejection_reason: str = ""
    edited_script: str = ""
    reviewed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OperatorReviewQueue:
    """Manages the operator content review process."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self.queue_dir = Path(f"coaches/{self.coach_acronym}/production/scripts")
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self._queue_file = self.queue_dir / "review_queue.jsonl"

    def add(
        self,
        asset_id: str,
        format_type: str,
        format_label: str,
        topic: str,
        script: str,
        validation_scores: dict,
    ) -> ReviewItem:
        """Add a validated piece to the review queue."""
        item = ReviewItem(
            asset_id=asset_id,
            format_type=format_type,
            format_label=format_label,
            topic=topic,
            script=script,
            word_count=len(script.split()),
            validation_scores=validation_scores,
        )
        with open(self._queue_file, "a", encoding="utf-8") as f:
            f.write(item.model_dump_json() + "\n")
        return item

    def get_pending(self) -> list[ReviewItem]:
        """Get all pending items in the queue."""
        return self._load_by_status("pending")

    def approve(self, asset_id: str) -> ReviewItem:
        """Approve a content piece for delivery."""
        item = self._update_status(asset_id, "approved")
        self.receipt_chain.log(
            agent_id="operator",
            action="approve_content",
            asset_id=asset_id,
            input_summary=f"Reviewed: {item.format_label} — {item.topic[:60]}",
            output_summary="Approved for Notion delivery",
            decision="approved",
        )
        return item

    def reject(self, asset_id: str, reason: str) -> ReviewItem:
        """Reject a content piece with a reason for rewrite."""
        item = self._update_status(asset_id, "rejected", rejection_reason=reason)
        self.receipt_chain.log(
            agent_id="operator",
            action="reject_content",
            asset_id=asset_id,
            input_summary=f"Reviewed: {item.format_label} — {item.topic[:60]}",
            output_summary=f"Rejected: {reason}",
            decision="rejected",
            decision_rationale=reason,
        )
        return item

    def edit(self, asset_id: str, new_script: str) -> ReviewItem:
        """Edit a content piece (preserves original in Receipt Chain)."""
        item = self._update_status(asset_id, "edited", edited_script=new_script)
        self.receipt_chain.log(
            agent_id="operator",
            action="edit_content",
            asset_id=asset_id,
            input_summary=f"Original: {item.word_count} words",
            output_summary=f"Edited: {len(new_script.split())} words",
            decision="edited",
            metadata={
                "original_word_count": item.word_count,
                "edited_word_count": len(new_script.split()),
            },
        )
        return item

    def _load_by_status(self, status: str) -> list[ReviewItem]:
        if not self._queue_file.exists():
            return []
        items = []
        with open(self._queue_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = ReviewItem.model_validate_json(line)
                if item.status == status:
                    items.append(item)
        return items

    def _update_status(self, asset_id: str, new_status: str, **kwargs) -> ReviewItem:
        if not self._queue_file.exists():
            raise ValueError(f"No queue file found")

        lines = self._queue_file.read_text(encoding="utf-8").splitlines()
        updated = []
        target_item = None
        for line in lines:
            if not line.strip():
                continue
            item = ReviewItem.model_validate_json(line)
            if item.asset_id == asset_id:
                item.status = new_status
                item.reviewed_at = datetime.now(timezone.utc)
                for k, v in kwargs.items():
                    if hasattr(item, k):
                        setattr(item, k, v)
                target_item = item
            updated.append(item.model_dump_json())

        self._queue_file.write_text("\n".join(updated) + "\n", encoding="utf-8")

        if target_item is None:
            raise ValueError(f"Asset ID {asset_id} not found in queue")
        return target_item
