"""
CCP Groq Transcription Service
Task 1.09 — Fast voice-to-text transcription for Sacred Audio and client voice notes.

Handles:
- Sacred Audio recordings (coach onboarding) — higher quality, longer
- Client voice notes (CBCS interactions) — fast, < 5s target
- Retry logic with exponential backoff
- Format detection (OGG, MP3, M4A)

Usage:
    from src.ccp.services.groq_transcriber import GroqTranscriber

    transcriber = GroqTranscriber()
    result = transcriber.transcribe_file("path/to/audio.ogg")
    print(result.text)
    print(result.duration_seconds)
"""

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx


@dataclass
class TranscriptionResult:
    """Result of a transcription operation."""

    text: str
    duration_seconds: float
    language: Optional[str] = None
    model_used: str = "whisper-large-v3-turbo"
    processing_time_ms: float = 0.0
    segments: list[dict] = field(default_factory=list)


class GroqTranscriber:
    """Transcribe audio files using Groq's Whisper endpoint.

    Groq provides ultra-fast inference for Whisper models,
    making it ideal for real-time coaching interactions where
    transcription must complete in < 5 seconds.
    """

    API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
    DEFAULT_MODEL = "whisper-large-v3-turbo"
    MAX_RETRIES = 3
    SUPPORTED_FORMATS = {".ogg", ".mp3", ".m4a", ".wav", ".webm", ".mp4"}

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set it via environment variable "
                "or pass it to GroqTranscriber(api_key=...)"
            )

    def transcribe_file(
        self,
        file_path: str | Path,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> TranscriptionResult:
        """Transcribe an audio file.

        Args:
            file_path: Path to the audio file
            language: Optional language hint (ISO 639-1, e.g. 'en', 'fr')
            prompt: Optional prompt to guide the transcription style

        Returns:
            TranscriptionResult with text, duration, and metadata

        Raises:
            FileNotFoundError: If the audio file doesn't exist
            ValueError: If the file format is not supported
            httpx.HTTPStatusError: If the API returns an error after retries
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {path.suffix}. "
                f"Supported: {self.SUPPORTED_FORMATS}"
            )

        start_time = time.monotonic()

        # Build the multipart form data
        form_data = {"model": self.DEFAULT_MODEL, "response_format": "verbose_json"}
        if language:
            form_data["language"] = language
        if prompt:
            form_data["prompt"] = prompt

        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                with open(path, "rb") as audio_file:
                    with httpx.Client(timeout=30.0) as client:
                        response = client.post(
                            self.API_URL,
                            headers={"Authorization": f"Bearer {self.api_key}"},
                            data=form_data,
                            files={"file": (path.name, audio_file, self._mime_type(path))},
                        )
                        response.raise_for_status()

                data = response.json()
                elapsed = (time.monotonic() - start_time) * 1000

                return TranscriptionResult(
                    text=data.get("text", ""),
                    duration_seconds=data.get("duration", 0.0),
                    language=data.get("language"),
                    model_used=self.DEFAULT_MODEL,
                    processing_time_ms=elapsed,
                    segments=data.get("segments", []),
                )

            except (httpx.HTTPStatusError, httpx.ConnectError) as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    wait = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    time.sleep(wait)

        raise last_error

    def transcribe_url(
        self,
        audio_url: str,
        download_dir: str = "/tmp/ccp_audio",
        language: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> TranscriptionResult:
        """Download an audio file from a URL and transcribe it.

        Useful for transcribing files hosted on Supabase Storage.

        Args:
            audio_url: URL of the audio file
            download_dir: Temporary directory for the download
            language: Optional language hint
            prompt: Optional transcription prompt

        Returns:
            TranscriptionResult
        """
        download_path = Path(download_dir)
        download_path.mkdir(parents=True, exist_ok=True)

        # Extract filename from URL
        filename = audio_url.split("/")[-1].split("?")[0]
        local_path = download_path / filename

        # Download
        with httpx.Client(timeout=60.0) as client:
            response = client.get(audio_url)
            response.raise_for_status()
            local_path.write_bytes(response.content)

        try:
            result = self.transcribe_file(local_path, language=language, prompt=prompt)
        finally:
            # Clean up the downloaded file
            if local_path.exists():
                local_path.unlink()

        return result

    @staticmethod
    def _mime_type(path: Path) -> str:
        """Map file extension to MIME type."""
        mime_map = {
            ".ogg": "audio/ogg",
            ".mp3": "audio/mpeg",
            ".m4a": "audio/mp4",
            ".wav": "audio/wav",
            ".webm": "audio/webm",
            ".mp4": "audio/mp4",
        }
        return mime_map.get(path.suffix.lower(), "audio/ogg")
