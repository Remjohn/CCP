import httpx
from groq import AsyncGroq
from backend.config import get_settings
import logging
import os

logger = logging.getLogger(__name__)
settings = get_settings()

class GroqTranscriber:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.telegram_api_base = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

    async def get_file_path(self, file_id: str) -> str:
        """
        Queries Telegram API to get the file path for a given file_id.
        """
        url = f"{self.telegram_api_base}/getFile"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"file_id": file_id})
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                raise ValueError(f"Telegram API Error: {data}")
            return data["result"]["file_path"]

    async def download_file(self, file_path: str) -> bytes:
        """
        Downloads the file bytes from Telegram.
        """
        url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content

    async def transcribe(self, audio_bytes: bytes, filename: str = "voice.ogg") -> str:
        """
        Sends audio bytes to Groq for transcription.
        """
        try:
            # Groq expects a file-like object with a name
            transcription = await self.client.audio.transcriptions.create(
                file=(filename, audio_bytes),
                model="distil-whisper-large-v3-en",
                response_format="json",
                language="en",
                temperature=0.0
            )
            return transcription.text
        except Exception as e:
            logger.error(f"Groq Transcription Failed: {e}")
            raise

# Global instance
transcriber = GroqTranscriber()
