"""
CCP Ritual Delivery Scheduler
Task 3.04 — Schedule and send personalized daily accountability rituals.

Rituals include:
- Morning intention prompt
- Midday check-in
- Evening reflection
- Weekly synthesis (Fridays)

Timing adapts to client timezone and engagement patterns.
"""

import json
import os
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class RitualConfig(BaseModel):
    """Per-client ritual configuration."""

    person_id: str
    telegram_id: str
    timezone_offset: int = Field(default=0, description="Hours from UTC")
    morning_time: str = Field(default="08:00", description="HH:MM local")
    midday_time: str = Field(default="13:00")
    evening_time: str = Field(default="20:00")
    active: bool = True
    engagement_streak: int = 0
    last_response_date: str = ""


RITUAL_PROMPTS = {
    "morning": """You are coaching as {coach_name}. Write a morning intention prompt for your client.

CLIENT CONTEXT: {client_context}
COACH VOICE: warmth={warmth}, directness={directness}

Rules:
1. Maximum 3 sentences
2. Reference something specific from their recent context if available
3. Ask ONE specific question they can answer in 30 seconds
4. Sound like {coach_name}, not a generic bot
5. No emojis except ONE at the start

Write the morning prompt:""",

    "midday": """You are coaching as {coach_name}. Write a midday check-in for your client.

CLIENT CONTEXT: {client_context}
LAST MORNING RESPONSE: {last_response}

Rules:
1. Maximum 2 sentences
2. Acknowledge their morning intention
3. One gentle redirect or encouragement
4. Sound casual and real, like a text from a friend who happens to be a coach

Write the midday check-in:""",

    "evening": """You are coaching as {coach_name}. Write an evening reflection prompt for your client.

CLIENT CONTEXT: {client_context}
TODAY'S INTERACTIONS: {today_summary}

Rules:
1. Maximum 3 sentences
2. Invite them to notice what went well AND what surprised them
3. The question should provoke genuine reflection, not just "how was your day"
4. Warm close, no pressure

Write the evening prompt:""",

    "weekly_synthesis": """You are coaching as {coach_name}. Write a weekly synthesis for your client.

THIS WEEK'S HIGHLIGHTS:
{weekly_highlights}

CLIENT CONTEXT: {client_context}

Rules:
1. 4-6 sentences maximum
2. Name ONE specific pattern you noticed this week
3. Name ONE specific victory (even small)
4. Ask a forward-looking question for next week
5. Celebrate their consistency (they showed up {streak} days this week)

Write the weekly synthesis:""",
}


class RitualScheduler:
    """Schedule and generate personalized daily rituals."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._config_dir = Path(f"coaches/{self.coach_acronym}/clients")
        self._config_dir.mkdir(parents=True, exist_ok=True)

    def get_config(self, person_id: str) -> Optional[RitualConfig]:
        """Load ritual config for a client."""
        config_path = self._config_dir / f"ritual_{person_id}.json"
        if config_path.exists():
            data = json.loads(config_path.read_text(encoding="utf-8"))
            return RitualConfig.model_validate(data)
        return None

    def save_config(self, config: RitualConfig) -> None:
        """Save ritual config."""
        config_path = self._config_dir / f"ritual_{config.person_id}.json"
        config_path.write_text(config.model_dump_json(indent=2), encoding="utf-8")

    async def generate_ritual(
        self,
        ritual_type: str,
        person_id: str,
        client_context: str = "",
        last_response: str = "",
        today_summary: str = "",
        weekly_highlights: str = "",
    ) -> str:
        """Generate a ritual message.

        Args:
            ritual_type: morning, midday, evening, or weekly_synthesis
            person_id: Client Person ID
            client_context: Context Premise narrative
            last_response: Their last response (for midday follow-up)
            today_summary: Today's interactions summary (for evening)
            weekly_highlights: Week's highlights (for weekly synthesis)

        Returns:
            Generated ritual message text
        """
        from google import genai

        template = RITUAL_PROMPTS.get(ritual_type)
        if not template:
            return ""

        # Load coach soul for voice
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        soul_data = {}
        if soul_path.exists():
            soul_data = json.loads(soul_path.read_text(encoding="utf-8"))

        config = self.get_config(person_id)
        streak = config.engagement_streak if config else 0

        prompt = template.format(
            coach_name=soul_data.get("coach_name", "Coach"),
            client_context=client_context or "New client, no context yet.",
            warmth=soul_data.get("content_tone", {}).get("warmth", 0.7),
            directness=soul_data.get("content_tone", {}).get("directness", 0.5),
            last_response=last_response or "No response yet today.",
            today_summary=today_summary or "No interactions today.",
            weekly_highlights=weekly_highlights or "First week.",
            streak=streak,
        )

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        ritual_text = response.text.strip()

        self.receipt_chain.log(
            agent_id="ritual_scheduler",
            action=f"generate_{ritual_type}",
            person_id=person_id,
            output_summary=f"{ritual_type}: {len(ritual_text)} chars",
            decision="sent",
        )

        return ritual_text

    async def send_ritual(
        self, telegram_id: str, ritual_text: str
    ) -> None:
        """Send a ritual message via Telegram."""
        import httpx

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not bot_token:
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, json={"chat_id": telegram_id, "text": ritual_text})

    def record_response(self, person_id: str) -> None:
        """Record that a client responded to a ritual (streak tracking)."""
        config = self.get_config(person_id)
        if config:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if config.last_response_date != today:
                config.engagement_streak += 1
                config.last_response_date = today
                self.save_config(config)
