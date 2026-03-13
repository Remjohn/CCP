"""
CCP Embedded Governance Ministers
Tasks 2.08, 2.09, 2.10 — Three inline validation checks during generation.

Minister of Identity (2.08): Checks voice DNA drift (TTT < 15%)
Minister of Relevance (2.09): Checks tribe archetype alignment
Minister of Timing (2.10): Checks seasonal appropriateness

These run INLINE during generation, not as a separate validation gate.
They catch issues early before the content reaches the Validation Team.
"""

import json
import os
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.models.coach_soul import CoachSoul


class MinisterVerdict(BaseModel):
    """Result from an inline minister check."""

    minister: str
    passed: bool
    score: float = Field(ge=0.0, le=1.0, description="0=complete failure, 1=perfect")
    issues: list[str] = Field(default_factory=list)
    corrections: list[str] = Field(default_factory=list)


IDENTITY_CHECK_PROMPT = """You are the Minister of Identity. Evaluate this script for voice authenticity.

COACH VOICE DNA:
- Rhythm patterns: {rhythm}
- Metaphor families: {metaphors}
- Signature vocabulary: {vocabulary}
- Humor style: {humor_style}
- Tone: warmth={warmth}, directness={directness}

SCRIPT TO EVALUATE:
{script}

Score this script on TTT (Tone, Texture, Timing) alignment with the coach's voice.
Identify ANY moment that sounds generic, AI-generated, or unlike the coach.

Return JSON:
{{
  "alignment_score": 0.0-1.0,
  "drift_detected": true/false,
  "issues": ["specific issue 1", "..."],
  "corrections": ["correction instruction 1", "..."],
  "ai_tells": ["phrases that sound AI-generated"]
}}
"""

RELEVANCE_CHECK_PROMPT = """You are the Minister of Relevance. Evaluate this script for tribe alignment.

COACH TRIBE:
- Archetype: {tribe}
- Ideal client pain points: {pain_points}
- Ideal client aspirations: {aspirations}
- Core message: {core_message}

SCRIPT TO EVALUATE:
{script}

Does this content resonate with the coach's tribe? Would the ideal client
feel spoken to, or would they scroll past?

Return JSON:
{{
  "relevance_score": 0.0-1.0,
  "tribe_aligned": true/false,
  "issues": ["specific issue 1", "..."],
  "corrections": ["correction instruction 1", "..."]
}}
"""

TIMING_CHECK_PROMPT = """You are the Minister of Timing. Evaluate this script for seasonal appropriateness.

CURRENT CONTEXT:
- Month: {month}
- Season (Macro): {macro_season}
- Cultural moments: Consider major holidays, back-to-school, new year energy, etc.
- Content topic: {topic}

SCRIPT TO EVALUATE:
{script}

Is this content seasonally appropriate? Would it feel timely or tone-deaf?

Return JSON:
{{
  "timing_score": 0.0-1.0,
  "seasonally_appropriate": true/false,
  "issues": ["specific issue 1", "..."],
  "corrections": ["correction instruction 1", "..."]
}}
"""

SEASONS = {
    1: "New Beginnings / Resolution Energy",
    2: "Winter Depth / Valentine's Love/Self-Love",
    3: "Spring Awakening / Renewal",
    4: "Spring Growth / Easter Rebirth",
    5: "Momentum / Pre-Summer Drive",
    6: "Summer Expansion / Freedom",
    7: "Mid-Year Reflection / Summer Peak",
    8: "Late Summer / Back-to-School Prep",
    9: "Autumn Reset / New Season Energy",
    10: "Harvest / Gratitude / Pre-Holiday",
    11: "Depth / Thanksgiving / Year-End Prep",
    12: "Reflection / Closure / Holiday Spirit",
}


class GovernanceMinisters:
    """Three inline governance checks for content quality."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    async def check_identity(self, soul: CoachSoul, script: str) -> MinisterVerdict:
        """Minister of Identity — check voice DNA alignment."""
        from google import genai

        client = genai.Client(api_key=self.api_key)
        prompt = IDENTITY_CHECK_PROMPT.format(
            rhythm=", ".join(soul.voice_dna.sentence_rhythm),
            metaphors=", ".join(soul.voice_dna.metaphor_patterns),
            vocabulary=", ".join(soul.voice_dna.vocabulary_fingerprint[:10]),
            humor_style=soul.voice_dna.humor_style or "unknown",
            warmth=soul.content_tone.warmth,
            directness=soul.content_tone.directness,
            script=script,
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        data = self._parse_json(response.text)

        score = float(data.get("alignment_score", 0.5))
        passed = score >= 0.85  # 15% drift threshold = 85% alignment

        return MinisterVerdict(
            minister="identity",
            passed=passed,
            score=score,
            issues=data.get("issues", []) + data.get("ai_tells", []),
            corrections=data.get("corrections", []),
        )

    async def check_relevance(self, soul: CoachSoul, script: str) -> MinisterVerdict:
        """Minister of Relevance — check tribe alignment."""
        from google import genai

        client = genai.Client(api_key=self.api_key)
        prompt = RELEVANCE_CHECK_PROMPT.format(
            tribe=soul.tribe_archetype,
            pain_points=", ".join(soul.ideal_client.pain_points),
            aspirations=", ".join(soul.ideal_client.aspirations),
            core_message=soul.core_message,
            script=script,
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        data = self._parse_json(response.text)

        return MinisterVerdict(
            minister="relevance",
            passed=data.get("tribe_aligned", False),
            score=float(data.get("relevance_score", 0.5)),
            issues=data.get("issues", []),
            corrections=data.get("corrections", []),
        )

    async def check_timing(
        self, script: str, topic: str, month: Optional[int] = None
    ) -> MinisterVerdict:
        """Minister of Timing — check seasonal appropriateness."""
        from datetime import datetime
        from google import genai

        if month is None:
            month = datetime.now().month

        client = genai.Client(api_key=self.api_key)
        prompt = TIMING_CHECK_PROMPT.format(
            month=month,
            macro_season=SEASONS.get(month, ""),
            topic=topic,
            script=script,
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        data = self._parse_json(response.text)

        return MinisterVerdict(
            minister="timing",
            passed=data.get("seasonally_appropriate", True),
            score=float(data.get("timing_score", 0.8)),
            issues=data.get("issues", []),
            corrections=data.get("corrections", []),
        )

    async def run_all(
        self, soul: CoachSoul, script: str, topic: str = ""
    ) -> list[MinisterVerdict]:
        """Run all three minister checks in parallel."""
        import asyncio

        results = await asyncio.gather(
            self.check_identity(soul, script),
            self.check_relevance(soul, script),
            self.check_timing(script, topic),
        )
        return list(results)

    @staticmethod
    def _parse_json(text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {}
