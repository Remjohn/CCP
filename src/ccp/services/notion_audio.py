"""
CCP Audio Block Handler
Task 4.04 — Handles audio embedding in Notion pages.

Takes a Supabase Storage URL for voice/Sacred Audio clips:
- Creates a Notion audio embed block
- Handles OGG/MP3/M4A formats
- Adds transcript as a toggle block below the audio
"""

from typing import Optional

from src.ccp.services.notion_sync import NotionSync


class NotionAudioHandler:
    """Handle audio blocks in Notion pages."""

    SUPPORTED_FORMATS = {"ogg", "mp3", "m4a", "wav", "webm"}

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.notion = NotionSync(coach_acronym=self.coach_acronym)

    async def embed_audio_with_transcript(
        self,
        page_id: str,
        audio_url: str,
        transcript: str = "",
        label: str = "Audio",
        duration_seconds: float = 0,
    ) -> dict:
        """Embed an audio file with an optional transcript toggle.

        Args:
            page_id: Notion page ID to append to
            audio_url: Supabase Storage URL for the audio file
            transcript: Optional transcript text
            label: Display label for the audio
            duration_seconds: Duration in seconds

        Returns:
            Notion API response
        """
        blocks = []

        # Audio embed
        blocks.append(self.notion.audio_block(audio_url))

        # Metadata callout
        duration_str = f"{duration_seconds:.0f}s" if duration_seconds else "unknown"
        file_format = audio_url.rsplit(".", 1)[-1].lower() if "." in audio_url else "audio"
        blocks.append(self.notion.paragraph(
            f"🎧 {label} · {file_format.upper()} · {duration_str}",
            color="gray",
        ))

        # Transcript toggle
        if transcript:
            blocks.append(self.notion.toggle(
                "📝 View transcript",
                children=[self.notion.paragraph(transcript)]
            ))

        return await self.notion.append_blocks(page_id, blocks)

    async def embed_sacred_audio(
        self,
        page_id: str,
        audio_url: str,
        transcript: str,
        asset_id: str = "",
    ) -> dict:
        """Embed a Sacred Audio clip with full context.

        Sacred Audio gets special treatment:
        - Framed as the coach's authentic voice
        - Transcript in a toggle
        - Asset ID reference
        """
        blocks = [
            self.notion.callout(
                f"🎙️ Sacred Audio · {asset_id}" if asset_id else "🎙️ Sacred Audio",
                emoji="🎙️",
                color="purple_background",
            ),
            self.notion.audio_block(audio_url),
        ]

        if transcript:
            blocks.append(self.notion.toggle(
                "📝 Full transcript",
                children=[self.notion.paragraph(transcript)]
            ))

        return await self.notion.append_blocks(page_id, blocks)

    @staticmethod
    def validate_format(url: str) -> bool:
        """Check if the audio URL has a supported format."""
        ext = url.rsplit(".", 1)[-1].lower() if "." in url else ""
        return ext in NotionAudioHandler.SUPPORTED_FORMATS
