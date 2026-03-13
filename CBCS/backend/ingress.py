from fastapi import APIRouter, Header, Request, HTTPException, BackgroundTasks, status
from typing import Annotated
import logging
from .config import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)

from .core.redis_client import redis_client


# ──────────────────────────────────────────────
# Role Registry (Story 18.1 / 18.2)
# ──────────────────────────────────────────────

class RoleRegistry:
    """
    Resolves Telegram chat_id → role (coach/user/unknown).

    Architecture:
        1. Check in-memory cache first (fast path)
        2. Fall back to Supabase lookup (cold path)
        3. Default to 'user' for unknown chat_ids

    Per-coach cloning: Each instance has its own registry.
    In a single-coach deployment, there's typically 1 coach + N users.
    """

    def __init__(self):
        # In-memory cache: {chat_id: {"role": "coach"|"user", "coach_id": uuid, ...}}
        self._cache: dict[int, dict] = {}

    def register_coach(self, chat_id: int, coach_id: str, coach_name: str) -> None:
        """Register a coach in the local cache."""
        self._cache[chat_id] = {
            "role": "coach",
            "coach_id": coach_id,
            "coach_name": coach_name,
        }
        logger.info(f"[RoleRegistry] Registered coach: {coach_name} (chat_id={chat_id})")

    def register_user(self, chat_id: int, user_id: str, coach_id: str) -> None:
        """Register a user in the local cache."""
        self._cache[chat_id] = {
            "role": "user",
            "user_id": user_id,
            "coach_id": coach_id,
        }
        logger.info(f"[RoleRegistry] Registered user: {user_id} (chat_id={chat_id})")

    async def resolve_role(self, chat_id: int) -> dict:
        """
        Resolve the role for a given Telegram chat_id.

        Returns:
            dict with 'role' key ('coach', 'user', or 'unknown')
        """
        # 1. Check cache
        if chat_id in self._cache:
            return self._cache[chat_id]

        # 2. TODO: Supabase lookup (Story 18.1)
        # try:
        #     from .tools.supabase_tools import supabase_client
        #     profile = await supabase_client.get_profile_by_chat_id(chat_id)
        #     if profile:
        #         self._cache[chat_id] = profile
        #         return profile
        # except Exception as e:
        #     logger.warning(f"[RoleRegistry] Supabase lookup failed: {e}")

        # 3. Default: unknown (treat as user)
        logger.info(f"[RoleRegistry] Unknown chat_id={chat_id}, defaulting to 'user'")
        return {"role": "user", "user_id": str(chat_id)}


# Global instance
role_registry = RoleRegistry()


# ──────────────────────────────────────────────
# Telegram Update Processor
# ──────────────────────────────────────────────

async def process_telegram_update(payload: dict):
    """
    Background task to process the Telegram update.

    Role-based routing:
        1. Resolve role (coach vs user)
        2. Coach messages → coach_graph (content ideation, pipeline triggers, monitoring)
        3. User messages → user_graph (existing CBCS flow: perception → strategy → expression)
    """
    try:
        message = payload.get("message", {})
        user_id = message.get("from", {}).get("id")
        text = message.get("text")

        if not user_id:
            logger.warning("Received update without user_id")
            return

        # ── Step 1: Resolve Role ──
        role_info = await role_registry.resolve_role(user_id)
        role = role_info.get("role", "user")
        logger.info(f"[Ingress] chat_id={user_id} resolved as role='{role}'")

        # ── Step 2: Handle Voice Messages ──
        if "voice" in message or "audio" in message:
            try:
                file_id = message.get("voice", {}).get("file_id") or message.get("audio", {}).get("file_id")
                if file_id:
                    logger.info(f"Detected audio message {file_id}. Transcribing...")
                    from .core.transcription import transcriber

                    # 1. Get Path
                    file_path = await transcriber.get_file_path(file_id)

                    # 2. Download
                    audio_bytes = await transcriber.download_file(file_path)

                    # 3. Transcribe
                    transcribed_text = await transcriber.transcribe(audio_bytes)
                    logger.info(f"Transcription: {transcribed_text}")

                    # 4. Update Message Payload
                    message["text"] = f"[TRANSCRIPTION]: {transcribed_text}"
                    text = message["text"]

                    # 5. Process journal (user flow only)
                    if role == "user":
                        from .core.journal_processor import journal_processor
                        await journal_processor.process_journal(str(user_id), transcribed_text)

            except Exception as e:
                logger.error(f"Transcription/Processing failed: {e}")
                message["text"] = "[ERROR]: Audio processing failed."

        if not text and not message.get("text"):
            logger.warning(f"Received update from {user_id} without text or audio.")
            return

        logger.info(f"Processing message from {user_id} (role={role}): {text}")

        # ── Step 3: Buffer Messages ──
        result = await redis_client.buffer_message(user_id, payload)

        if result["trigger"]:
            logger.info(f"Pipeline triggered for {user_id} due to {result['reason']}")

            # Fetch buffer
            messages = await redis_client.get_and_clear_buffer(user_id)
            logger.info(f"Flushed {len(messages)} messages for processing.")

            # ── Step 4: Route to Correct Graph ──
            if role == "coach":
                await _route_to_coach_graph(user_id, messages, role_info)
            else:
                await _route_to_user_graph(user_id, messages)

        else:
            logger.info(f"Message buffered for {user_id}. Waiting for silence...")

    except Exception as e:
        logger.error(f"Error processing update: {e}")


async def _route_to_coach_graph(user_id: int, messages: list, role_info: dict):
    """
    Route buffered messages to the coach LangGraph subgraph.

    Coach flow nodes:
        coach_listening → content_ideation | pipeline_trigger | user_monitor
    """
    try:
        from .core.coach_graph import get_coach_graph

        initial_state = {
            "user_id": user_id,
            "role": "coach",
            "coach_config": role_info,
            "buffer": messages,
            "messages": [],
            "is_processing": True,
        }

        config = {"configurable": {"thread_id": f"coach_{user_id}"}}
        graph = get_coach_graph()
        await graph.ainvoke(initial_state, config=config)
        logger.info(f"[Coach Graph] Execution completed for coach {user_id}")

    except Exception as e:
        logger.error(f"[Coach Graph] Failed for coach {user_id}: {e}")


async def _route_to_user_graph(user_id: int, messages: list):
    """
    Route buffered messages to the existing user LangGraph.

    User flow: listening → processing → END (existing CBCS pipeline)
    """
    try:
        from .core.graph import get_graph

        initial_state = {
            "user_id": user_id,
            "role": "user",
            "buffer": messages,
            "messages": [],
            "is_processing": True,
        }

        config = {"configurable": {"thread_id": str(user_id)}}
        graph = get_graph()
        await graph.ainvoke(initial_state, config=config)
        logger.info(f"[User Graph] Execution completed for user {user_id}")

    except Exception as e:
        logger.error(f"[User Graph] Failed for user {user_id}: {e}")


# ──────────────────────────────────────────────
# Webhook Endpoint
# ──────────────────────────────────────────────

@router.post("/webhooks/telegram", status_code=status.HTTP_200_OK)
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None
):
    """
    High-concurrency webhook endpoint for Telegram.
    Validates secret token and offloads processing to background task.
    """
    # 1. Security Check
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        logger.warning("Invalid Telegram Secret Token")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Secret Token"
        )

    # 2. Parse Payload
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON"
        )

    # 3. Offload to Background Task (The "200ms Rule")
    background_tasks.add_task(process_telegram_update, payload)

    # 4. Immediate Ack
    return {"status": "ok"}

