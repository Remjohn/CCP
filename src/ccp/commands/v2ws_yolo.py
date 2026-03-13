"""
CCP YOLO Mode Webinar Intake
Task 5.04 — Receives 5 coach answers and generates a full webinar script.

The 5 YOLO questions:
  1. What do you want to teach?
  2. Who is your audience?
  3. What's your offer at the end?
  4. What stories do you have?
  5. What's the tone?

From these, generates a module-by-module webinar using the
Jason Fladlien method: every slide is a HOOK.
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain


class YoloInput(BaseModel):
    """The 5 YOLO mode inputs from the coach."""

    teach_what: str = Field(description="What do you want to teach?")
    audience: str = Field(description="Who is your audience?")
    offer: str = Field(description="What's your offer at the end?")
    stories: str = Field(description="What stories do you have?")
    tone: str = Field(description="What's the tone?")


class WebinarModule(BaseModel):
    """A single webinar module."""

    module_number: int
    title: str
    hook: str = Field(description="Opening hook for this module")
    teaching_point: str
    story_beat: str = Field(default="", description="Story to illustrate the point")
    slides: list[dict] = Field(default_factory=list, description="Slide-by-slide content")
    transition: str = Field(default="", description="Bridge to next module")
    duration_minutes: int = 0


class WebinarScript(BaseModel):
    """Complete webinar script."""

    asset_id: str
    coach_acronym: str
    title: str
    modules: list[WebinarModule]
    total_duration_minutes: int
    offer_module: WebinarModule
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


YOLO_GENERATION_PROMPT = """You are generating a high-converting webinar script using the Jason Fladlien method.

COACH INPUT:
- Teaching: {teach_what}
- Audience: {audience}
- Offer: {offer}
- Stories: {stories}
- Tone: {tone}

COACH VOICE:
{voice_context}

METHOD: Every slide is a HOOK. Each module opens with a promise, delivers on it, then hooks into the next.

Generate a complete webinar script with 5-7 modules. Return JSON:
{{
  "title": "Webinar title",
  "modules": [
    {{
      "module_number": 1,
      "title": "Module title",
      "hook": "Opening hook that makes them NEED to hear this module",
      "teaching_point": "The core teaching of this module",
      "story_beat": "Story that illustrates the teaching",
      "slides": [
        {{"slide_number": 1, "headline": "...", "body": "...", "speaker_notes": "..."}},
        {{"slide_number": 2, "headline": "...", "body": "...", "speaker_notes": "..."}}
      ],
      "transition": "Bridge to next module",
      "duration_minutes": N
    }}
  ],
  "offer_module": {{
    "module_number": 99,
    "title": "The Offer",
    "hook": "The transition from teaching to offering",
    "teaching_point": "What they get",
    "story_beat": "Social proof story",
    "slides": [...],
    "transition": "",
    "duration_minutes": N
  }}
}}

Rules:
1. Module 1 must IMMEDIATELY deliver value — no "welcome" or "about me" fluff
2. Each module hook must create genuine curiosity or urgency
3. Stories should come from the coach's real experiences (use their stories input)
4. The offer module should feel like a natural next step, not a pitch
5. Speaker notes should include delivery cues (pause, emphasis, gesture)
6. Target total duration: 60-90 minutes
7. Sound like the coach, not a generic presenter
"""


class V2WSYoloMode:
    """Generate a complete webinar from 5 quick inputs."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.asset_gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate(self, inputs: YoloInput) -> WebinarScript:
        """Generate a full webinar script from YOLO inputs.

        Args:
            inputs: The 5 YOLO mode answers

        Returns:
            Complete WebinarScript with modules
        """
        from google import genai

        # Load coach voice context
        voice_context = self._load_voice_context()

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=YOLO_GENERATION_PROMPT.format(
                teach_what=inputs.teach_what,
                audience=inputs.audience,
                offer=inputs.offer,
                stories=inputs.stories,
                tone=inputs.tone,
                voice_context=voice_context,
            ),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        raw = json.loads(text)

        # Build WebinarScript
        asset_id = self.asset_gen.generate(AssetType.WEBINAR)
        modules = [WebinarModule(**m) for m in raw.get("modules", [])]
        offer = WebinarModule(**raw.get("offer_module", {"module_number": 99, "title": "Offer", "hook": "", "teaching_point": ""}))
        total_duration = sum(m.duration_minutes for m in modules) + offer.duration_minutes

        script = WebinarScript(
            asset_id=asset_id,
            coach_acronym=self.coach_acronym,
            title=raw.get("title", "Untitled Webinar"),
            modules=modules,
            total_duration_minutes=total_duration,
            offer_module=offer,
        )

        # Save
        output_dir = Path(f"coaches/{self.coach_acronym}/production/webinars")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{asset_id}.json"
        output_file.write_text(script.model_dump_json(indent=2), encoding="utf-8")

        self.receipt_chain.log(
            agent_id="v2ws_yolo",
            action="generate_webinar",
            asset_id=asset_id,
            input_summary=f"YOLO: {inputs.teach_what[:60]}",
            output_summary=f"{len(modules)} modules, {total_duration}min",
            decision="completed",
            metadata={"module_count": len(modules), "duration": total_duration},
        )

        return script

    def _load_voice_context(self) -> str:
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        if soul_path.exists():
            soul = json.loads(soul_path.read_text(encoding="utf-8"))
            return (
                f"Coach: {soul.get('coach_name', 'Coach')}\n"
                f"Warmth: {soul.get('content_tone', {}).get('warmth', 0.7)}\n"
                f"Directness: {soul.get('content_tone', {}).get('directness', 0.5)}\n"
                f"Humor: {soul.get('voice_dna', {}).get('humor_style', 'balanced')}"
            )
        return "No voice profile available."
