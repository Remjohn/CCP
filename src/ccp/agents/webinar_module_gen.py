"""
CCP Webinar Module Generator
Task 5.05 — Generates individual webinar modules with TTT calibration.

Used by both YOLO mode and Interactive mode. Each module follows
the Jason Fladlien principle: every slide is a HOOK.
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


MODULE_GENERATION_PROMPT = """You are generating a single webinar module for coach {coach_name}.

MODULE BRIEF:
- Module #{module_number}: {module_title}
- Teaching point: {teaching_point}
- Target duration: {duration} minutes
- Story to include: {story}

COACH VOICE: warmth={warmth}, directness={directness}, humor={humor}
BOREDOM BAN: {avoidance}

Generate the module with 4-8 slides. Each slide must have:
1. headline: The HOOK (what makes them pay attention)
2. body: The teaching content (2-3 short paragraphs max)
3. speaker_notes: Delivery instructions (pauses, emphasis, audience interaction)
4. visual_suggestion: What visual should appear on this slide

Return only JSON:
{{
  "slides": [
    {{
      "slide_number": 1,
      "headline": "...",
      "body": "...",
      "speaker_notes": "...",
      "visual_suggestion": "..."
    }}
  ],
  "audience_interaction": "One engagement prompt for this module",
  "key_takeaway": "One sentence the audience should remember"
}}

Rules:
1. First slide must open with a promise or provocative question
2. No slide should feel like "filler" — every one earns its spot
3. Speaker notes should include: [PAUSE], [EMPHASIS], [SCAN ROOM], [ASK AUDIENCE]
4. Visual suggestions should be specific enough for image generation
5. Sound like {coach_name} on stage, not reading from slides
"""


class WebinarModuleGenerator:
    """Generate individual webinar modules with TTT calibration."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate_module(
        self,
        module_number: int,
        module_title: str,
        teaching_point: str,
        story: str = "",
        duration: int = 12,
        avoidance: str = "None",
    ) -> dict:
        """Generate a single webinar module.

        Returns:
            Module dict with slides, interaction prompts, and key takeaway
        """
        from google import genai

        soul_data = self._load_soul()
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=MODULE_GENERATION_PROMPT.format(
                coach_name=soul_data.get("coach_name", "Coach"),
                module_number=module_number,
                module_title=module_title,
                teaching_point=teaching_point,
                story=story or "No specific story provided.",
                duration=duration,
                warmth=soul_data.get("content_tone", {}).get("warmth", 0.7),
                directness=soul_data.get("content_tone", {}).get("directness", 0.5),
                humor=soul_data.get("content_tone", {}).get("humor_weight", 0.3),
                avoidance=avoidance,
            ),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        result = json.loads(text)

        self.receipt_chain.log(
            agent_id="webinar_module_gen",
            action="generate_module",
            output_summary=f"Module {module_number}: {module_title} — {len(result.get('slides', []))} slides",
            decision="completed",
        )

        return result

    def _load_soul(self) -> dict:
        from pathlib import Path
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        if soul_path.exists():
            return json.loads(soul_path.read_text(encoding="utf-8"))
        return {}
