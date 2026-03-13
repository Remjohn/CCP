"""
CCP Notion Webhook Receiver
Task 4.09 — Receives Notion automation webhooks on status changes.

When a coach changes a content page Status from Draft → Approved,
this triggers the distribution pipeline for that Asset ID.
"""

import json
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Request

from src.ccp.core.receipt_chain import ReceiptChain

router = APIRouter()


@router.post("/notion/webhook")
async def notion_webhook(request: Request):
    """Receive webhook from Notion automation.

    Expected payload (from Notion automation via Make/Zapier):
    {
        "page_id": "...",
        "asset_id": "...",
        "old_status": "Draft",
        "new_status": "Approved",
        "coach_acronym": "NDL"
    }
    """
    body = await request.json()
    page_id = body.get("page_id", "")
    asset_id = body.get("asset_id", "")
    old_status = body.get("old_status", "")
    new_status = body.get("new_status", "")
    coach_acronym = body.get("coach_acronym", os.getenv("COACH_ACRONYM", "UNK"))

    if not page_id or not new_status:
        raise HTTPException(status_code=400, detail="Missing page_id or new_status")

    receipt_chain = ReceiptChain(coach_acronym=coach_acronym)

    # Draft → Approved triggers distribution
    if new_status == "Approved" and old_status in ("Draft", "In Review"):
        from src.ccp.services.distribution import DistributionPipeline
        pipeline = DistributionPipeline(coach_acronym=coach_acronym)
        result = await pipeline.distribute(page_id=page_id, asset_id=asset_id)

        receipt_chain.log(
            agent_id="notion_webhook",
            action="status_change_trigger",
            asset_id=asset_id,
            input_summary=f"Status: {old_status} → {new_status}",
            output_summary=f"Distribution triggered: {result.get('status', '')}",
            decision="distribution_triggered",
        )

        return {
            "status": "distribution_triggered",
            "asset_id": asset_id,
            "distribution": result,
        }

    # Log other status changes
    receipt_chain.log(
        agent_id="notion_webhook",
        action="status_change",
        asset_id=asset_id,
        input_summary=f"Status: {old_status} → {new_status}",
        output_summary="Logged, no action triggered",
        decision="logged",
    )

    return {"status": "logged", "asset_id": asset_id}
