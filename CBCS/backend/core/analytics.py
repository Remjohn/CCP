from pydantic import BaseModel
from typing import List, Dict
from backend.config import get_settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

class Vibe(BaseModel):
    word: str
    count: int
    sentiment: str # "Positive", "Negative", "Neutral"

class AnalyticsService:
    def __init__(self):
        self.settings = get_settings()
        self.supabase: Client = create_client(self.settings.SUPABASE_URL, self.settings.SUPABASE_KEY)
        
        # Define the vibes we track (same as seed data)
        self.tracked_vibes = {
            "Anxious": "Negative", "Stuck": "Negative", "Overwhelmed": "Negative", 
            "Tired": "Negative", "Guilty": "Negative", "Lonely": "Negative", 
            "Determined": "Positive", "Hopeful": "Positive", "Proud": "Positive", 
            "Curious": "Neutral"
        }

    def get_cohort_vibes(self) -> List[Vibe]:
        """
        Returns aggregated emotional data from the cohort by analyzing journal transcripts.
        """
        try:
            # Fetch all journals (for MVP, we fetch all. In prod, use SQL aggregation or limit)
            response = self.supabase.table("daily_journals").select("transcript").execute()
            journals = response.data
            
            vibe_counts = {word: 0 for word in self.tracked_vibes.keys()}
            
            for entry in journals:
                text = entry.get("transcript", "").lower()
                for word in self.tracked_vibes.keys():
                    if word.lower() in text:
                        vibe_counts[word] += 1
            
            # Convert to List[Vibe]
            result = []
            for word, count in vibe_counts.items():
                if count > 0:
                    result.append(Vibe(
                        word=word,
                        count=count,
                        sentiment=self.tracked_vibes[word]
                    ))
            
            # Sort by count desc
            result.sort(key=lambda x: x.count, reverse=True)
            return result
            
        except Exception as e:
            logger.error(f"Error fetching cohort vibes: {e}")
            return []

# Global Instance
analytics = AnalyticsService()
