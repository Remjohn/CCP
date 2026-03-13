import redis.asyncio as redis
from backend.config import get_settings
import json
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        self.silence_duration = 90  # seconds
        self.buffer_limit = 5       # messages

    async def close(self):
        await self.redis.aclose()

    async def buffer_message(self, user_id: int, message_payload: dict) -> dict:
        """
        Buffers a message and checks if the pipeline should be triggered.
        Returns a dict indicating if trigger is needed: {'trigger': bool, 'reason': str}
        """
        buffer_key = f"buffer:{user_id}"
        timer_key = f"timer:{user_id}"

        # 1. Push message to buffer
        # We store the whole payload or just the text? Story says "message payload".
        # Let's store JSON string.
        await self.redis.rpush(buffer_key, json.dumps(message_payload))
        
        # 2. Check Buffer Size (Hard Limit)
        buffer_len = await self.redis.llen(buffer_key)
        if buffer_len >= self.buffer_limit:
            logger.info(f"Buffer limit hit for {user_id}. Triggering pipeline.")
            # Reset timer to avoid double trigger? Or just let it expire?
            # Better to delete timer if we trigger now.
            await self.redis.delete(timer_key)
            return {"trigger": True, "reason": "limit_reached"}

        # 3. Set/Reset Silence Timer
        # We set a key that expires. 
        # Ideally, we want an event when it expires. 
        # For MVP without external worker, we might just rely on the next message check 
        # OR we assume a separate worker listens to keyspace notifications.
        # For this story, we just set the timer.
        await self.redis.setex(timer_key, self.silence_duration, "active")
        
        return {"trigger": False, "reason": "buffering"}

    async def get_and_clear_buffer(self, user_id: int) -> list[dict]:
        """
        Retrieves all messages from the buffer and clears it.
        """
        buffer_key = f"buffer:{user_id}"
        # Transactional retrieval and delete would be better (LPOP count or MULTI/EXEC)
        # For simplicity: LRANGE then DEL
        messages_raw = await self.redis.lrange(buffer_key, 0, -1)
        if not messages_raw:
            return []
        
        await self.redis.delete(buffer_key)
        return [json.loads(m) for m in messages_raw]

# Global instance
redis_client = RedisClient()
