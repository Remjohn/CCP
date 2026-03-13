"""
CCP Validation Team Gate
Task 2.11 — Triple-pass validation: Sophia → Marcus → Chen.

Sophia (Content Strategist): Strategic value and audience resonance
Marcus (Protocol Validator): Format compliance and structural integrity
Chen (Soul Validator): Voice authenticity and coach-soul alignment

Failed pieces enter a TillDone rewrite loop (max 3 retries).
"""

import json
import os
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul


class ValidatorVerdict(BaseModel):
    """Result from a single validator pass."""

    validator: str
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    feedback: list[str] = Field(default_factory=list)
    rewrite_instructions: list[str] = Field(default_factory=list)


class ValidationResult(BaseModel):
    """Combined result from all three validators."""

    passed: bool
    sophia: ValidatorVerdict
    marcus: ValidatorVerdict
    chen: ValidatorVerdict
    overall_score: float
    requires_rewrite: bool
    combined_rewrite_instructions: list[str] = Field(default_factory=list)


SOPHIA_PROMPT = """You are Sophia, the Content Strategist. Evaluate this script for strategic value.

COACH PROFILE:
- Core message: {core_message}
- Tribe: {tribe}
- Ideal client pain points: {pain_points}

SCRIPT:
{script}

Evaluate:
1. Does this content teach something ACTIONABLE? (Not just motivational fluff)
2. Would the ideal client save or share this? Why?
3. Does it advance the coach's positioning?
4. Is the angle fresh and specific?

Return JSON: {{"score": 0.0-1.0, "passed": true/false, "feedback": ["..."], "rewrite_instructions": ["..."]}}
Threshold: 0.7 to pass.
"""

MARCUS_PROMPT = """You are Marcus, the Protocol Validator. Check this script for structural integrity.

FORMAT: {format_label}
SCRIPT:
{script}

Check:
1. Does it match the format requirements?
   - Thread: 5-8 connected posts
   - Carousel: clear slide-by-slide structure
   - Reel: timing notes, spoken-word cadence
   - Quote: single powerful sentence
   - Meme: setup + punchline + image description
   - Article: 600-800 words with sections
2. Does it have a strong opening hook (first 2 lines)?
3. Does it end with engagement (question/challenge), NOT a summary?
4. Is it the right length for the format?

Return JSON: {{"score": 0.0-1.0, "passed": true/false, "feedback": ["..."], "rewrite_instructions": ["..."]}}
Threshold: 0.75 to pass.
"""

CHEN_PROMPT = """You are Chen, the Soul Validator. Final voice authenticity check.

VOICE DNA:
- Rhythm: {rhythm}
- Metaphors: {metaphors}
- Vocabulary: {vocabulary}
- Humor: {humor_style}
- Tone: warmth={warmth}, directness={directness}

SCRIPT:
{script}

This is the LAST check before content reaches the coach. You are the guardian.

Evaluate:
1. Does EVERY sentence sound like the coach? Flag any that don't.
2. Are there any AI-tells? (passive voice, "let's dive in", hedging words, excessive emojis)
3. Does the emotional arc feel human? (real build, not manufactured)
4. Would you be comfortable sending this as-is to the coach for publishing?

Return JSON: {{"score": 0.0-1.0, "passed": true/false, "feedback": ["..."], "rewrite_instructions": ["..."], "ai_tells_found": ["..."]}}
Threshold: 0.85 to pass (highest bar).
"""


class ValidationTeam:
    """Triple-pass validation gate for content quality."""

    MAX_RETRIES = 3

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def validate(
        self, soul: CoachSoul, script: str, format_label: str, asset_id: str = ""
    ) -> ValidationResult:
        """Run all three validator passes sequentially.

        Sequential because Marcus needs to know if Sophia passed,
        and Chen needs to know about prior issues.
        """
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Sophia (Strategy)
        sophia = await self._run_validator(
            client, "sophia",
            SOPHIA_PROMPT.format(
                core_message=soul.core_message,
                tribe=soul.tribe_archetype,
                pain_points=", ".join(soul.ideal_client.pain_points),
                script=script,
            ),
        )

        # Marcus (Protocol)
        marcus = await self._run_validator(
            client, "marcus",
            MARCUS_PROMPT.format(format_label=format_label, script=script),
        )

        # Chen (Soul) — highest bar
        chen = await self._run_validator(
            client, "chen",
            CHEN_PROMPT.format(
                rhythm=", ".join(soul.voice_dna.sentence_rhythm),
                metaphors=", ".join(soul.voice_dna.metaphor_patterns),
                vocabulary=", ".join(soul.voice_dna.vocabulary_fingerprint[:10]),
                humor_style=soul.voice_dna.humor_style or "unknown",
                warmth=soul.content_tone.warmth,
                directness=soul.content_tone.directness,
                script=script,
            ),
        )

        all_passed = sophia.passed and marcus.passed and chen.passed
        avg_score = (sophia.score + marcus.score + chen.score) / 3

        combined_instructions = (
            sophia.rewrite_instructions
            + marcus.rewrite_instructions
            + chen.rewrite_instructions
        )

        result = ValidationResult(
            passed=all_passed,
            sophia=sophia,
            marcus=marcus,
            chen=chen,
            overall_score=round(avg_score, 3),
            requires_rewrite=not all_passed,
            combined_rewrite_instructions=combined_instructions,
        )

        # Log
        self.receipt_chain.log(
            agent_id="validation_team",
            action="validate_content",
            asset_id=asset_id,
            input_summary=f"Script: {len(script.split())} words",
            output_summary=(
                f"{'PASSED' if all_passed else 'FAILED'} — "
                f"Sophia={sophia.score:.2f} Marcus={marcus.score:.2f} Chen={chen.score:.2f} "
                f"Avg={avg_score:.2f}"
            ),
            decision="approved" if all_passed else "requires_rewrite",
            metadata={
                "sophia_score": sophia.score,
                "marcus_score": marcus.score,
                "chen_score": chen.score,
                "overall": avg_score,
                "rewrite_count": len(combined_instructions),
            },
        )

        return result

    async def _run_validator(self, client, name: str, prompt: str) -> ValidatorVerdict:
        """Run a single validator and parse its response."""
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {"score": 0.5, "passed": False, "feedback": ["Parse error"]}

        return ValidatorVerdict(
            validator=name,
            passed=data.get("passed", False),
            score=float(data.get("score", 0.5)),
            feedback=data.get("feedback", []),
            rewrite_instructions=data.get("rewrite_instructions", []),
        )
