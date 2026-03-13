"""
Telegram Messaging Utility
===========================
Shared utility for sending messages from any backend component
(scheduler, coach_graph, ingress) to Telegram chats.

Extracted because multiple components need outbound messaging:
- Scheduler → heartbeat messages
- Coach graph → idea delivery
- Ingress → typing indicators
"""

import httpx
import logging
from typing import Optional

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"


async def send_telegram_message(
    chat_id: int,
    text: str,
    parse_mode: str = "Markdown",
    reply_markup: Optional[dict] = None,
) -> bool:
    """
    Send a text message to a Telegram chat.

    Returns True on success, False on failure.
    Logs errors but never raises — callers should not crash on send failure.
    """
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{TELEGRAM_API_BASE}/sendMessage", json=payload)
            if resp.status_code == 200:
                return True
            else:
                logger.error(
                    f"[Telegram] sendMessage failed: status={resp.status_code} "
                    f"body={resp.text[:200]} chat_id={chat_id}"
                )
                return False
    except Exception as e:
        logger.error(f"[Telegram] sendMessage error for chat_id={chat_id}: {e}")
        return False


async def send_typing_action(chat_id: int) -> None:
    """Send 'typing...' action indicator to a chat."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"{TELEGRAM_API_BASE}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"},
            )
    except Exception:
        pass  # Best-effort, never crash on typing indicator
