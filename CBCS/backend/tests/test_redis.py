import pytest
from backend.core.redis_client import RedisClient
import json
import asyncio

@pytest.mark.asyncio
async def test_redis_buffer_flow():
    # Instantiate a fresh client for this test to match the current event loop
    client = RedisClient()
    user_id = 999999
    
    try:
        # Ensure clean state
        await client.redis.delete(f"buffer:{user_id}")
        await client.redis.delete(f"timer:{user_id}")

        # 1. Push first message
        payload1 = {"message": {"text": "msg1"}}
        result = await client.buffer_message(user_id, payload1)
        assert result["trigger"] is False
        assert result["reason"] == "buffering"
        
        # Check buffer size
        buffer_len = await client.redis.llen(f"buffer:{user_id}")
        assert buffer_len == 1

        # Check timer
        ttl = await client.redis.ttl(f"timer:{user_id}")
        assert ttl > 0

        # 2. Push up to limit (limit is 5)
        for i in range(3):
            await client.buffer_message(user_id, {"message": {"text": f"msg{i+2}"}})
        
        # Buffer should be 4 now
        buffer_len = await client.redis.llen(f"buffer:{user_id}")
        assert buffer_len == 4

        # 3. Push 5th message (Trigger)
        payload5 = {"message": {"text": "msg5"}}
        result = await client.buffer_message(user_id, payload5)
        assert result["trigger"] is True
        assert result["reason"] == "limit_reached"

        # 4. Clear buffer
        messages = await client.get_and_clear_buffer(user_id)
        assert len(messages) == 5
        assert messages[0]["message"]["text"] == "msg1"
        assert messages[4]["message"]["text"] == "msg5"

        # Verify buffer is empty
        buffer_len = await client.redis.llen(f"buffer:{user_id}")
        assert buffer_len == 0

    finally:
        await client.close()
