"""
CCP Stream of Consciousness Capture
Task 2.01 — Processes coach topic suggestions into structured idea seeds.

Coaches send voice notes or text via Telegram with raw topic ideas.
This service transcribes, structures, and queues them for the
content analysis pipeline (ccf-analyze).
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain


class TopicSeed(BaseModel):
    """A structured topic suggestion from the coach."""

    asset_id: str = Field(description="SUGG Asset ID")
    raw_input: str = Field(description="Original coach input (text or transcript)")
    topic_summary: str = Field(description="Cleaned 1-2 sentence topic summary")
    keywords: list[str] = Field(default_factory=list, description="Extracted keywords")
    suggested_formats: list[str] = Field(
        default_factory=list,
        description="Formats this topic could suit (thread, carousel, reel, etc.)",
    )
    source: str = Field(default="telegram", description="Where the suggestion came from")
    status: str = Field(default="queued", description="queued, scheduled, used, archived")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SOCCapture:
    """Process Stream of Consciousness inputs from coaches."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.asset_gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self.queue_dir = Path(f"coaches/{self.coach_acronym}/intelligence/research")
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self._queue_file = self.queue_dir / "topic_queue.jsonl"

    async def capture_text(self, text: str, source: str = "telegram") -> TopicSeed:
        """Capture a text topic suggestion from the coach.

        Args:
            text: The coach's raw topic suggestion
            source: Where it came from (telegram, operator, etc.)

        Returns:
            Structured TopicSeed
        """
        asset_id = self.asset_gen.generate(AssetType.SUGGESTION)

        # Use Gemini Flash for fast structuring
        structured = await self._structure_topic(text)

        seed = TopicSeed(
            asset_id=asset_id,
            raw_input=text,
            topic_summary=structured.get("summary", text[:200]),
            keywords=structured.get("keywords", []),
            suggested_formats=structured.get("formats", []),
            source=source,
        )

        # Save to queue
        self._enqueue(seed)

        # Log
        self.receipt_chain.log(
            agent_id="soc_capture",
            action="capture_topic",
            asset_id=asset_id,
            input_summary=f"Topic from {source}: {text[:100]}...",
            output_summary=f"Seed: {seed.topic_summary}",
            decision="queued",
            metadata={"keywords": seed.keywords, "formats": seed.suggested_formats},
        )

        return seed

    async def capture_voice(
        self,
        audio_path: str,
        source: str = "telegram",
    ) -> TopicSeed:
        """Capture a voice note topic suggestion — transcribe then structure."""
        from src.ccp.services.groq_transcriber import GroqTranscriber

        transcriber = GroqTranscriber()
        result = transcriber.transcribe_file(audio_path)
        return await self.capture_text(result.text, source=source)

    def get_queue(self, status: str = "queued") -> list[TopicSeed]:
        """Get all topic seeds with a given status."""
        if not self._queue_file.exists():
            return []

        seeds = []
        with open(self._queue_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                seed = TopicSeed.model_validate_json(line)
                if seed.status == status:
                    seeds.append(seed)
        return seeds

    def mark_used(self, asset_id: str) -> None:
        """Mark a topic seed as used in content production."""
        self._update_status(asset_id, "used")

    def _enqueue(self, seed: TopicSeed) -> None:
        """Add a topic seed to the queue."""
        with open(self._queue_file, "a", encoding="utf-8") as f:
            f.write(seed.model_dump_json() + "\n")

    def _update_status(self, asset_id: str, new_status: str) -> None:
        """Update the status of a topic seed in the queue file."""
        if not self._queue_file.exists():
            return

        lines = self._queue_file.read_text(encoding="utf-8").splitlines()
        updated = []
        for line in lines:
            if not line.strip():
                continue
            seed = TopicSeed.model_validate_json(line)
            if seed.asset_id == asset_id:
                seed.status = new_status
            updated.append(seed.model_dump_json())

        self._queue_file.write_text("\n".join(updated) + "\n", encoding="utf-8")

    async def _structure_topic(self, raw_text: str) -> dict:
        """Use Gemini Flash to structure a raw topic into keywords and format suggestions."""
        import os
        try:
            from google import genai

            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            response = await client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""Extract from this coach's topic suggestion:
1. A clean 1-2 sentence summary
2. 3-5 keywords
3. Which content formats would suit this topic best (thread, carousel, reel, meme, story, article, quote, case_study)

Topic: "{raw_text}"

Return ONLY JSON: {{"summary": "...", "keywords": [...], "formats": [...]}}""",
            )
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(text)
        except Exception:
            # Fallback: use the raw text as-is
            return {
                "summary": raw_text[:200],
                "keywords": [],
                "formats": ["thread", "carousel"],
            }
