"""
CCP Kimya Elicitation Processor
Task 1.12 — Processes the onboarding interview to populate coach_soul.json.

Kimya (Elicitation Architect) is the agent that transforms a raw
onboarding interview transcript into structured identity data:
- Coaching philosophy
- Core message  
- Ideal client profile
- Signature frameworks
- Competitive positioning
- Content tone parameters

Uses Gemini Pro for deep reasoning about the coach's identity.
"""

import json
import os
from typing import Optional

from src.ccp.models.coach_soul import (
    CoachSoul,
    ContentTone,
    IdealClient,
)


# Structured extraction prompt for Gemini
KIMYA_EXTRACTION_PROMPT = """You are Kimya, the Elicitation Architect for the Conscious Coaching Platform.

Your task: Extract a structured identity profile from this coach's onboarding interview transcript.

TRANSCRIPT:
{transcript}

{research_context}

Extract the following and return as valid JSON:

{{
  "coaching_philosophy": "A 2-3 sentence summary of the coach's core philosophy, in their voice",
  "core_message": "The single most important thing this coach wants the world to understand (1 sentence)",
  "tribe_archetype": "The archetype that best describes who this coach serves (e.g. 'The Wounded Healer', 'The Ambitious Introvert', 'The Corporate Escapee')",
  "ideal_client": {{
    "demographics": "Age range, typical occupation, life stage",
    "psychographics": "Mindset, values, inner conflicts",
    "pain_points": ["List of 3-5 specific pain points"],
    "aspirations": ["List of 3-5 specific aspirations"]
  }},
  "signature_frameworks": ["List any named methods, models, or frameworks the coach uses"],
  "competitive_positioning": "What makes this coach different from others in their niche (1-2 sentences)",
  "content_tone": {{
    "warmth": 0.0-1.0,
    "directness": 0.0-1.0,
    "humor_weight": 0.0-1.0,
    "formality": 0.0-1.0
  }}
}}

Rules:
1. Preserve the coach's exact language and metaphors where possible.
2. The coaching_philosophy should sound like the coach, not like an AI summary.
3. For content_tone, score based on how the coach actually speaks, not what they say they want.
4. For tribe_archetype, create a specific label that captures the coach's unique audience.
5. Return ONLY the JSON, no markdown, no explanation.
"""


class KimyaProcessor:
    """Process onboarding interview transcripts to extract coach identity."""

    def __init__(self, gemini_api_key: Optional[str] = None):
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for Kimya processing")

    async def process_interview(
        self,
        transcript: str,
        research_brief: Optional[str] = None,
    ) -> dict:
        """Extract structured identity data from an interview transcript.

        Args:
            transcript: The full interview transcript text
            research_brief: Optional pre-meeting research about the coach

        Returns:
            Dictionary matching the extraction schema
        """
        from google import genai

        client = genai.Client(api_key=self.api_key)

        research_context = ""
        if research_brief:
            research_context = f"\nPRE-MEETING RESEARCH:\n{research_brief}\n"

        prompt = KIMYA_EXTRACTION_PROMPT.format(
            transcript=transcript,
            research_context=research_context,
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        # Parse the JSON response
        response_text = response.text.strip()
        # Strip markdown code fences if present
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        return json.loads(response_text)

    def apply_to_soul(self, soul: CoachSoul, extracted: dict) -> CoachSoul:
        """Apply extracted identity data to an existing CoachSoul profile.

        Args:
            soul: The CoachSoul to update
            extracted: Dictionary from process_interview()

        Returns:
            Updated CoachSoul with new identity data
        """
        soul.coaching_philosophy = extracted.get("coaching_philosophy", soul.coaching_philosophy)
        soul.core_message = extracted.get("core_message", soul.core_message)
        soul.tribe_archetype = extracted.get("tribe_archetype", soul.tribe_archetype)

        if "ideal_client" in extracted:
            ic = extracted["ideal_client"]
            soul.ideal_client = IdealClient(
                demographics=ic.get("demographics", ""),
                psychographics=ic.get("psychographics", ""),
                pain_points=ic.get("pain_points", []),
                aspirations=ic.get("aspirations", []),
            )

        if "signature_frameworks" in extracted:
            soul.signature_frameworks = extracted["signature_frameworks"]

        if "competitive_positioning" in extracted:
            soul.competitive_positioning = extracted["competitive_positioning"]

        if "content_tone" in extracted:
            ct = extracted["content_tone"]
            soul.content_tone = ContentTone(
                warmth=float(ct.get("warmth", 0.5)),
                directness=float(ct.get("directness", 0.5)),
                humor_weight=float(ct.get("humor_weight", 0.3)),
                formality=float(ct.get("formality", 0.3)),
            )

        soul.bump_version()
        return soul
