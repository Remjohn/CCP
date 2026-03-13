import httpx
from backend.config import get_settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)
settings = get_settings()

class VoiceEngine:
    def __init__(self):
        self.api_key = settings.RUNPOD_API_KEY
        self.endpoint_id = settings.RUNPOD_ENDPOINT_ID
        self.base_url = f"https://api.runpod.ai/v2/{self.endpoint_id}/runsync" if self.endpoint_id else None

    async def generate_audio(self, text: str, style: str = "Standard") -> Optional[str]:
        """
        Generates audio from text using the configured TTS engine.
        Returns the URL of the generated audio file.
        """
        if not self.api_key or not self.endpoint_id:
            logger.warning("Runpod credentials not configured. Returning mock audio URL.")
            return "https://mock.audio/output.mp3"

        # Map Style to TTS Parameters
        # TTT-02 (Compassionate) -> Speed 0.85x, Breathiness High
        # TTT-08 (Challenger) -> Speed 1.1x, Breathiness Low
        
        params = {
            "speed": 1.0,
            "breathiness": 0.5
        }
        
        if style == "Compassionate":
            params = {"speed": 0.85, "breathiness": 0.8}
        elif style == "Challenger":
            params = {"speed": 1.1, "breathiness": 0.2}

        payload = {
            "input": {
                "text": text,
                "speed": params["speed"],
                "breathiness": params["breathiness"]
            }
        }

        logger.info(f"Generating audio via Runpod (Style: {style})...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Assuming Runpod returns { "output": { "audio_url": "..." } }
                # Adjust based on actual IndexTTS-2 API contract
                audio_url = data.get("output", {}).get("audio_url")
                
                if not audio_url:
                    logger.error(f"Runpod response missing audio_url: {data}")
                    return None
                    
                return audio_url

        except Exception as e:
            logger.error(f"Voice generation failed: {e}")
            return None

# Global Instance
voice_engine = VoiceEngine()
