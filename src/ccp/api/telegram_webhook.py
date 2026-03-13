"""
CCP Telegram Webhook Handler
Task 3.01 — FastAPI endpoint receiving Telegram updates.

Handles:
- Text messages from clients
- Voice notes from clients
- Commands from coaches
- Deduplication via Redis
- < 2s P95 response time target
"""

import hashlib
import json
import os
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain

router = APIRouter()


class TelegramUser(BaseModel):
    """Telegram user info from an update."""
    id: int
    first_name: str = ""
    last_name: str = ""
    username: str = ""


class TelegramMessage(BaseModel):
    """Parsed Telegram message."""
    message_id: int
    chat_id: int
    user: TelegramUser
    text: Optional[str] = None
    voice: Optional[dict] = None
    audio: Optional[dict] = None
    date: int = 0


class WebhookResponse(BaseModel):
    """Response sent back after processing."""
    status: str
    message_id: int
    processing_time_ms: float


# In-memory dedup set (replace with Redis in production)
_recent_message_ids: set[str] = set()
_MAX_DEDUP_SIZE = 10000


def _dedup_key(chat_id: int, message_id: int) -> str:
    return f"{chat_id}:{message_id}"


def _is_duplicate(chat_id: int, message_id: int) -> bool:
    key = _dedup_key(chat_id, message_id)
    if key in _recent_message_ids:
        return True
    _recent_message_ids.add(key)
    if len(_recent_message_ids) > _MAX_DEDUP_SIZE:
        # Evict oldest (in production, use Redis with TTL)
        _recent_message_ids.pop()
    return False


def _verify_secret(request: Request) -> bool:
    """Verify the Telegram webhook secret token."""
    secret = os.getenv("TELEGRAM_SECRET_TOKEN", "")
    if not secret:
        return True  # No secret configured, allow (dev mode)
    header = request.headers.get("x-telegram-bot-api-secret-token", "")
    return header == secret


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Receive and process Telegram webhook updates.

    This endpoint is called by Telegram whenever a message arrives.
    Target: < 2s P95 response time.
    """
    start_time = time.monotonic()

    # Verify secret token
    if not _verify_secret(request):
        raise HTTPException(status_code=403, detail="Invalid secret token")

    # Parse the update
    body = await request.json()
    message_data = body.get("message", {})
    if not message_data:
        return {"status": "no_message"}

    # Extract message info
    chat_id = message_data.get("chat", {}).get("id", 0)
    message_id = message_data.get("message_id", 0)
    user_data = message_data.get("from", {})

    # Deduplication
    if _is_duplicate(chat_id, message_id):
        return {"status": "duplicate", "message_id": message_id}

    # Build parsed message
    msg = TelegramMessage(
        message_id=message_id,
        chat_id=chat_id,
        user=TelegramUser(
            id=user_data.get("id", 0),
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            username=user_data.get("username", ""),
        ),
        text=message_data.get("text"),
        voice=message_data.get("voice"),
        audio=message_data.get("audio"),
        date=message_data.get("date", 0),
    )

    # Determine message type and route
    coach_acronym = os.getenv("COACH_ACRONYM", "UNK")
    message_type = _classify_message(msg)

    # Route to the appropriate handler
    from src.ccp.agents.vidye_router import VidyeRouter

    vidye = VidyeRouter(coach_acronym=coach_acronym)
    response_text = await vidye.route(msg, message_type)

    # Send response back via Telegram
    if response_text:
        await _send_telegram_response(chat_id, response_text)

    elapsed_ms = (time.monotonic() - start_time) * 1000

    return WebhookResponse(
        status="processed",
        message_id=message_id,
        processing_time_ms=round(elapsed_ms, 1),
    )


def _classify_message(msg: TelegramMessage) -> str:
    """Classify the incoming message type."""
    if msg.voice or msg.audio:
        return "voice"
    if msg.text and msg.text.startswith("/"):
        return "command"
    if msg.text:
        return "text"
    return "unknown"


async def _send_telegram_response(chat_id: int, text: str) -> None:
    """Send a text response to a Telegram chat."""
    import httpx

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not bot_token:
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})
