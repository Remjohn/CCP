"""
CCP Humor Agent + Tweet Meteorologist
Tasks 2.06 & 2.07 — Humor content generation and digital weather forecasting.

The Humor Agent generates tweets, memes, and humor-angle scripts.
The Tweet Meteorologist reads the digital conversation climate to
inform timely humor angles.
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul


HUMOR_PROMPT = """You are the Humor Agent for coach {coach_name}.

COACH HUMOR PROFILE:
- Style: {humor_style}
- Tone warmth: {warmth}
- Signature vocabulary: {vocabulary}

DIGITAL WEATHER (current conversation climate):
{weather_report}

CONTENT BRIEF:
- Format: {format_label}
- Topic: {topic}
- Angle: {angle}

Generate a humor piece. Rules:
1. Match the coach's humor style exactly ({humor_style}).
2. NO puns, dad jokes, or corporate "funny". This must feel like something a real human would share.
3. For memes: provide setup, punchline, AND image description.
4. For tweets: maximum impact in minimum words. Every word earns its place.
5. The humor must serve the coach's message — never just jokes for laughs.
6. Acceptable humor methods: irony, absurdity, awkwardly relatable moments, unexpected truth, contrast with expectations.
7. VIBE CHECK: If you wouldn't screenshot this and send it to a friend, rewrite it.

Write the humor piece:
"""

WEATHER_PROMPT = """You are the Tweet Meteorologist. Scan the current digital conversation landscape
for coaching/personal development audiences and report:

1. SENTIMENT CLIMATE: Overall mood (anxious, optimistic, frustrated, reflective)
2. VIRAL TRENDS: What formats/topics are spreading right now
3. MEME EXPLOSIONS: Current meme formats that could be adapted
4. NARRATIVE SHIFTS: New conversations emerging in the coaching space
5. COUNTER-NARRATIVE OPPORTUNITIES: Things everyone says that could be gently challenged

Focus area: coaching, personal development, entrepreneurship, mental health.

Return as JSON:
{{
  "sentiment": "one-word mood",
  "sentiment_detail": "2-sentence explanation",
  "trending_topics": ["topic1", "topic2", "topic3"],
  "meme_formats": ["format description 1", "format description 2"],
  "counter_narratives": ["thing everyone says that's worth questioning"],
  "best_timing": "when to post for maximum resonance",
  "weather_emoji": "single emoji that captures the digital mood"
}}
"""


class TweetMeteorologist:
    """Forecasts digital conversation weather for humor timing."""

    async def forecast(self) -> dict:
        """Generate a digital weather report."""
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=WEATHER_PROMPT,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"sentiment": "neutral", "trending_topics": [], "meme_formats": []}


class HumorAgent:
    """Generate humor content in the coach's voice."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self.meteorologist = TweetMeteorologist()

    async def generate(
        self,
        soul: CoachSoul,
        idea: dict,
        weather: Optional[dict] = None,
    ) -> dict:
        """Generate a humor piece.

        Args:
            soul: Coach soul profile
            idea: ContentIdea dict
            weather: Optional weather forecast (auto-fetched if missing)

        Returns:
            Dict with humor script and metadata
        """
        from google import genai

        if weather is None:
            weather = await self.meteorologist.forecast()

        weather_report = "\n".join([
            f"Mood: {weather.get('sentiment', 'neutral')} {weather.get('weather_emoji', '')}",
            f"Detail: {weather.get('sentiment_detail', '')}",
            f"Trending: {', '.join(weather.get('trending_topics', []))}",
            f"Meme formats: {', '.join(weather.get('meme_formats', []))}",
            f"Counter-narratives: {', '.join(weather.get('counter_narratives', []))}",
        ])

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = HUMOR_PROMPT.format(
            coach_name=soul.coach_name,
            humor_style=soul.voice_dna.humor_style or "warm_ironic",
            warmth=soul.content_tone.warmth,
            vocabulary=", ".join(soul.voice_dna.vocabulary_fingerprint[:8]),
            weather_report=weather_report,
            format_label=idea.get("format_label", "Tweet"),
            topic=idea.get("topic", ""),
            angle=idea.get("angle", ""),
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        script = response.text.strip()

        self.receipt_chain.log(
            agent_id="humor_agent",
            action="generate_humor",
            asset_id=idea.get("asset_id", ""),
            input_summary=f"Humor {idea.get('format_label', '')}: {idea.get('topic', '')[:60]}",
            output_summary=f"Generated: {len(script.split())} words, weather={weather.get('sentiment', '')}",
            decision="completed",
        )

        return {
            "asset_id": idea.get("asset_id", ""),
            "script": script,
            "word_count": len(script.split()),
            "weather_context": weather,
            "stage": "humor_draft",
        }
