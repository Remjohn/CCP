"""
DEP-ENG-060: Finding-Linked Source Cache
========================================
Accelerates M2-M6 CRAL Moments by serving converging search results 
from a cache rather than live SearXNG polls. Handles Tier-0 promotion.
"""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime

class DummyRedis:
    def get(self, key): return None
    def set(self, key, val, ex=None): pass

redis_client = DummyRedis()

class FindingSourceCache:
    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym

    def _get_key(self, trigger_category: str, moment_id: str) -> str:
        return f"finding_cache:{trigger_category}:{moment_id}"

    def get_tier0_sources(self, trigger_category: str, moment_id: str) -> Optional[List[str]]:
        """
        Returns cached source URLs if the finding has converged (Tier 0).
        M1 RELEVANT ignores Tier 0 to preserve recency.
        """
        if moment_id == "M1_RELEVANT":
            return None
            
        data_str = redis_client.get(self._get_key(trigger_category, moment_id))
        if data_str:
            data = json.loads(data_str)
            if data.get("tier", 1) == 0:
                # Validate TTL for demotion rule
                # Mock handling
                return data.get("source_urls_used", [])
        return None

    def store_and_compute_convergence(
        self, 
        trigger_category: str, 
        moment_id: str, 
        searxng_raw: dict, 
        finding_text: str, 
        sources_used: List[str]
    ):
        """
        Stores result and computes convergence. Promotes to Tier 0 if 
        3 separate sessions derive identical source utility.
        """
        key = self._get_key(trigger_category, moment_id)
        current_str = redis_client.get(key)
        
        tier = 1
        convergence_count = 0
        now = datetime.utcnow().isoformat()
        first_cached = now

        if current_str:
            current = json.loads(current_str)
            convergence_count = current.get("convergence_count", 0)
            first_cached = current.get("first_cached", now)
            
            # Convergence matching threshold: 2+ shared sources
            prev_sources = set(current.get("source_urls_used", []))
            overlap = set(sources_used).intersection(prev_sources)
            
            if len(overlap) >= 2:
                convergence_count += 1
                
            if convergence_count >= 3:
                tier = 0
                
        payload = {
            "trigger_category": trigger_category,
            "moment_id": moment_id,
            "searxng_raw_json": "compressed_payload_mock",
            "finding_text": finding_text,
            "source_urls_used": sources_used,
            "convergence_count": convergence_count,
            "first_cached": first_cached,
            "last_confirmed": now,
            "ttl_days": 90,
            "tier": tier
        }
        
        redis_client.set(key, json.dumps(payload), ex=86400 * 90)
        return tier
