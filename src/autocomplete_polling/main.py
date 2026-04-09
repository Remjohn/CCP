from fastapi import FastAPI
import httpx
import json
from datetime import datetime
import asyncio

app = FastAPI(title="CCP Autocomplete Polling Engine", version="1.0")

SEARXNG_URL = "http://ccp-searxng:8080/autocomplete"

class DummyAsyncRedis:
    async def get(self, key): return None
    async def set(self, key, val, ex=None): pass
    async def lpush(self, key, val): pass
    async def lrange(self, key, start, stop): return []

redis_client = DummyAsyncRedis()

class AutocompletePoller:
    async def poll_tribe(self, coach_id: str, seed_phrases: list[str]):
        current_snapshot = {}
        
        for phrase in seed_phrases:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(SEARXNG_URL, params={"q": phrase})
                    if response.status_code == 200:
                        current_snapshot[phrase] = response.json()
                except Exception:
                    pass
        
        previous_snapshot_str = await redis_client.get(f"autocomplete:{coach_id}")
        previous_snapshot = json.loads(previous_snapshot_str) if previous_snapshot_str else {}
        
        emerging_signals = []
        for phrase, current_suggestions in current_snapshot.items():
            prev_sugg = previous_snapshot.get(phrase, [])
            new_sugg = [s for s in current_suggestions if s not in prev_sugg]
            if new_sugg:
                emerging_signals.append({
                    "seed_phrase": phrase,
                    "new_autocomplete": new_sugg,
                    "signal_type": "zero_to_one_spike",
                    "detected_at": datetime.utcnow().isoformat(),
                    "coach_id": coach_id
                })
        
        await redis_client.set(f"autocomplete:{coach_id}", json.dumps(current_snapshot), ex=86400)
        
        if emerging_signals:
            await redis_client.lpush(f"signals:{coach_id}", json.dumps(emerging_signals))
            
        return emerging_signals

@app.get("/api/tribe_signals/{coach_id}")
async def get_tribe_signals(coach_id: str):
    signals = await redis_client.lrange(f"signals:{coach_id}", 0, -1)
    return {
        "coach_id": coach_id,
        "emerging_signals": [json.loads(s) for s in signals],
        "last_polled": await redis_client.get(f"last_poll:{coach_id}")
    }
