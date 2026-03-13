"""
CCP Posting Notes Generator
Task 4.12 — Generates platform-specific posting instructions.

For each approved piece generates:
  - Optimal posting time
  - Hashtag suggestions
  - Caption variants
  - Engagement prompts
  - Platform-specific formatting notes
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


POSTING_NOTES_PROMPT = """Generate platform-specific posting notes for this content piece.

CONTENT:
- Title: {title}
- Format: {format_label}
- Asset ID: {asset_id}

COACH VOICE: {voice_context}

Generate posting instructions for each platform. Return JSON:
{{
  "summary": "2-sentence overview of posting strategy",
  "optimal_time": "Best time to post (e.g., 'Tuesday 9:00 AM EST')",
  "platforms": {{
    "Instagram": "Format-specific instructions, caption approach, hashtag strategy, story teasers",
    "LinkedIn": "Professional angle, headline approach, engagement prompt",
    "Twitter/X": "Thread structure or standalone, hook approach",
    "TikTok": "If applicable — hook, pacing, trending audio suggestions"
  }},
  "hashtags": {{
    "primary": ["5 core hashtags"],
    "secondary": ["5 niche hashtags"],
    "trending": ["3 currently trending relevant hashtags"]
  }},
  "caption_variants": {{
    "short": "Under 100 characters — punchy",
    "medium": "100-300 characters — engaging",
    "long": "300+ characters — storytelling"
  }},
  "engagement_prompt": "A question or CTA to drive comments",
  "cross_post_notes": "How to adapt this piece for different platforms"
}}
"""


class PostingNotesGenerator:
    """Generate platform-specific posting instructions."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate(
        self,
        format_label: str,
        title: str,
        asset_id: str = "",
    ) -> dict:
        """Generate posting notes for an approved content piece.

        Args:
            format_label: Content format (Thread, Carousel, etc.)
            title: Content title
            asset_id: Optional Asset ID

        Returns:
            Posting notes dict with platform-specific instructions
        """
        from google import genai
        from pathlib import Path

        voice_context = self._load_voice_context()

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=POSTING_NOTES_PROMPT.format(
                title=title,
                format_label=format_label,
                asset_id=asset_id,
                voice_context=voice_context,
            ),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            notes = json.loads(text)
        except json.JSONDecodeError:
            notes = {
                "summary": f"Post {title} as a {format_label}.",
                "platforms": {},
                "hashtags": {"primary": [], "secondary": [], "trending": []},
                "caption_variants": {"short": title, "medium": title, "long": title},
                "engagement_prompt": "What do you think?",
            }

        self.receipt_chain.log(
            agent_id="posting_notes",
            action="generate_notes",
            asset_id=asset_id,
            output_summary=f"Notes for {format_label}: {title}",
            decision="completed",
            metadata={"platforms": list(notes.get("platforms", {}).keys())},
        )

        return notes

    def _load_voice_context(self) -> str:
        from pathlib import Path
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        if soul_path.exists():
            soul = json.loads(soul_path.read_text(encoding="utf-8"))
            return f"Coach: {soul.get('coach_name', 'Coach')}, Tone: warmth={soul.get('content_tone', {}).get('warmth', 0.7)}"
        return "No voice profile."
