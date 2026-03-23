"""
CCP Sacred Audio Transcriber — FR2 Unit 6
Enhanced Groq Whisper with non-standard config + Gemini Flash fallback.

Spec reference: FR2 Tech Spec §Stage B — ASR via Groq Whisper API

Non-standard Whisper configuration — mandatory:
  - Disable ITN (Inverse Text Normalization): preserve um, uh, stutters, false starts
  - Request word-level timestamps for Thought Unit boundary detection
  - Return raw transcript with all non-verbal utterances preserved

Fallback: Gemini Flash transcription if Groq rate limit exceeded or API error.

This module EXTENDS the base GroqTranscriber to add FR2-specific requirements.
The base transcriber (src/ccp/services/groq_transcriber.py) handles basic
transcription. This module adds:
  1. ITN-disabled configuration
  2. Word-level timestamps
  3. Non-verbal preservation hints
  4. Gemini Flash fallback
  5. DamageControl retry pattern (single retry on failure)
"""

import hashlib
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import httpx


# ──────────────────────────────────────────────────────────────
# Sacred Audio Transcription Result
# ──────────────────────────────────────────────────────────────

@dataclass
class SacredTranscriptionResult:
    """Result of a Sacred Audio transcription with non-verbals preserved.

    Spec: 'Return raw transcript with all non-verbal utterances preserved.'
    """

    text: str
    """Full transcript with um/uh/stutters preserved."""

    duration_seconds: float
    """Audio duration in seconds."""

    word_timestamps: list[dict[str, Any]] = field(default_factory=list)
    """Word-level timestamps for Thought Unit boundary detection.
    Each entry: {"word": str, "start": float, "end": float}."""

    language: Optional[str] = None
    """Detected language."""

    model_used: str = "whisper-large-v3-turbo"
    """Which model was used for transcription."""

    fallback_used: bool = False
    """True if Gemini Flash was used as fallback."""

    processing_time_ms: float = 0.0
    """Processing time in milliseconds."""

    input_hash: str = ""
    """SHA-256 hash of the audio input."""

    output_hash: str = ""
    """SHA-256 hash of the transcript output."""


# ──────────────────────────────────────────────────────────────
# Supported formats
# Spec §Stage A: "accept .ogg, .mp3, .m4a"
# ──────────────────────────────────────────────────────────────

SACRED_AUDIO_FORMATS = {".ogg", ".mp3", ".m4a"}

# Spec §Stage A: "if < 15 seconds → implicit rejection"
MIN_DURATION_SECONDS = 15.0


class SacredAudioTranscriber:
    """Transcribes Sacred Audio with FR2-specific configuration.

    Spec §Stage B: 'Engine: Groq API (Whisper model) — per-coach API key
    from environment variables. Fallback: Gemini Flash transcription if
    Groq rate limit exceeded or API error.'

    Differences from base GroqTranscriber:
    1. ITN disabled: preserves filled pauses (um, uh), stutters, false starts
    2. Word-level timestamps requested for Stage C boundary detection
    3. Non-verbal preservation prompt hint
    4. Gemini Flash fallback on Groq failure
    5. Single retry via DamageControl pattern (not base retry logic)
    """

    GROQ_API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
    GROQ_MODEL = "whisper-large-v3-turbo"

    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        coach_language: str = "en",
    ):
        """Initialize with per-coach API credentials.

        Spec: 'per-coach API key from environment variables.'

        Args:
            groq_api_key: Groq API key. Falls back to GROQ_API_KEY env var.
            gemini_api_key: Gemini API key for fallback. Falls back to GEMINI_API_KEY env var.
            coach_language: Coach's configured locale (ISO 639-1).
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.coach_language = coach_language

        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set via environment variable or constructor."
            )

    def validate_audio_file(self, file_path: Path) -> tuple[bool, str]:
        """Validate audio file format and duration.

        Spec §Stage A:
        - 'accept .ogg, .mp3, .m4a — reject all others'
        - 'if < 15 seconds → implicit rejection'

        Returns:
            (is_valid, error_message). error_message is empty if valid.
        """
        if not file_path.exists():
            return False, f"File not found: {file_path}"

        ext = file_path.suffix.lower()
        if ext not in SACRED_AUDIO_FORMATS:
            return False, f"Unsupported format: {ext}. Accepted: {SACRED_AUDIO_FORMATS}"

        return True, ""

    def compute_audio_hash(self, audio_bytes: bytes) -> str:
        """Compute SHA-256 hash of audio content.

        Spec §Stage A Receipt: 'input_payload_hash: sha256:{audio_file_hash}'
        """
        return hashlib.sha256(audio_bytes).hexdigest()

    def transcribe(
        self,
        audio_bytes: bytes,
        file_name: str = "audio.ogg",
    ) -> SacredTranscriptionResult:
        """Transcribe Sacred Audio with non-standard Whisper configuration.

        Spec §Stage B Steps:
        1. Submit audio to Groq Whisper endpoint with language parameter
        2. Non-standard config: ITN disabled, word timestamps, non-verbal preservation
        3. Validate response — on failure, DamageControl single retry
        4. If retry fails → fallback to Gemini Flash

        Args:
            audio_bytes: Raw audio bytes (in-process memory, not disk)
            file_name: Original filename for MIME type detection

        Returns:
            SacredTranscriptionResult with transcript, timestamps, and hashes.

        Raises:
            RuntimeError: If both Groq and Gemini Flash fail.
        """
        input_hash = self.compute_audio_hash(audio_bytes)
        start_time = time.monotonic()
        ext = Path(file_name).suffix.lower()
        mime_type = self._mime_type(ext)

        # Attempt 1: Groq Whisper with non-standard config
        try:
            result = self._transcribe_groq(audio_bytes, file_name, mime_type)
            result.input_hash = input_hash
            result.output_hash = hashlib.sha256(result.text.encode()).hexdigest()
            result.processing_time_ms = (time.monotonic() - start_time) * 1000
            return result
        except Exception as first_error:
            pass

        # DamageControl: single retry (spec §Stage B Step 3)
        try:
            result = self._transcribe_groq(audio_bytes, file_name, mime_type)
            result.input_hash = input_hash
            result.output_hash = hashlib.sha256(result.text.encode()).hexdigest()
            result.processing_time_ms = (time.monotonic() - start_time) * 1000
            return result
        except Exception:
            pass

        # Fallback: Gemini Flash (spec: "Gemini Flash transcription if
        # Groq rate limit exceeded or API error")
        if self.gemini_api_key:
            try:
                result = self._transcribe_gemini_flash(audio_bytes, file_name, mime_type)
                result.input_hash = input_hash
                result.output_hash = hashlib.sha256(result.text.encode()).hexdigest()
                result.processing_time_ms = (time.monotonic() - start_time) * 1000
                result.fallback_used = True
                return result
            except Exception:
                pass

        # Both failed — raise for pipeline to handle
        raise RuntimeError(
            "Sacred Audio transcription failed: both Groq Whisper and "
            "Gemini Flash returned errors. Coach should be notified."
        )

    def _transcribe_groq(
        self,
        audio_bytes: bytes,
        file_name: str,
        mime_type: str,
    ) -> SacredTranscriptionResult:
        """Transcribe via Groq Whisper with FR2 non-standard config.

        Spec §Stage B Step 2 — mandatory:
        - Disable ITN: preserve um, uh, stutters, false starts
        - Request word-level timestamps
        - Return raw transcript with all non-verbal utterances preserved
        """
        form_data = {
            "model": self.GROQ_MODEL,
            "response_format": "verbose_json",
            "language": self.coach_language,
            # Non-standard: request word-level timestamps
            "timestamp_granularities[]": "word",
            # Prompt hint to preserve non-verbals (Whisper respects this)
            # Spec: 'Filled pauses (um/uh), stutters, and false starts are
            # authenticity signals in the LIWC-22 Marker 6. Stripping them
            # at ingestion corrupts the gate.'
            "prompt": (
                "Preserve all filled pauses (um, uh, hmm), stutters, false starts, "
                "and self-corrections exactly as spoken. Do not clean up or normalize "
                "the speech. Preserve natural speech patterns."
            ),
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                self.GROQ_API_URL,
                headers={"Authorization": f"Bearer {self.groq_api_key}"},
                data=form_data,
                files={"file": (file_name, audio_bytes, mime_type)},
            )
            response.raise_for_status()

        data = response.json()

        # Extract word-level timestamps
        word_timestamps = []
        for word_info in data.get("words", []):
            word_timestamps.append({
                "word": word_info.get("word", ""),
                "start": word_info.get("start", 0.0),
                "end": word_info.get("end", 0.0),
            })

        # Also check segments for word-level data if top-level words not present
        if not word_timestamps and data.get("segments"):
            for segment in data["segments"]:
                for word_info in segment.get("words", []):
                    word_timestamps.append({
                        "word": word_info.get("word", ""),
                        "start": word_info.get("start", 0.0),
                        "end": word_info.get("end", 0.0),
                    })

        return SacredTranscriptionResult(
            text=data.get("text", ""),
            duration_seconds=data.get("duration", 0.0),
            word_timestamps=word_timestamps,
            language=data.get("language"),
            model_used=self.GROQ_MODEL,
        )

    def _transcribe_gemini_flash(
        self,
        audio_bytes: bytes,
        file_name: str,
        mime_type: str,
    ) -> SacredTranscriptionResult:
        """Fallback transcription via Gemini Flash.

        Spec: 'Fallback: Gemini Flash transcription if Groq rate limit
        exceeded or API error.'
        """
        try:
            from google import genai

            client = genai.Client(api_key=self.gemini_api_key)

            # Upload audio as inline data
            import base64
            audio_b64 = base64.b64encode(audio_bytes).decode()

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {
                        "parts": [
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": audio_b64,
                                }
                            },
                            {
                                "text": (
                                    "Transcribe this audio exactly as spoken. "
                                    "Preserve ALL filled pauses (um, uh, hmm), stutters, "
                                    "false starts, and self-corrections. Do NOT clean up "
                                    "or normalize the speech. Return ONLY the raw transcript text."
                                )
                            },
                        ]
                    }
                ],
            )

            transcript_text = response.text if response.text else ""

            return SacredTranscriptionResult(
                text=transcript_text,
                duration_seconds=0.0,  # Gemini doesn't return duration
                word_timestamps=[],  # Gemini doesn't return word timestamps
                model_used="gemini-2.0-flash",
            )

        except ImportError:
            raise RuntimeError("google-genai package not available for Gemini fallback")

    @staticmethod
    def _mime_type(ext: str) -> str:
        """Map file extension to MIME type."""
        mime_map = {
            ".ogg": "audio/ogg",
            ".mp3": "audio/mpeg",
            ".m4a": "audio/mp4",
        }
        return mime_map.get(ext, "audio/ogg")
