"""
CCP Transparent Collage Pipeline
Task 5.07 — Generates transparent PNG visuals for webinar slides.

Pipeline:
  1. Visual Reasoning Protocol → Extract visual brief from slide context
  2. Generate T2I prompt (white background, clean composition)
  3. Background removal → transparent PNG
  4. Inject as image node in Excalidraw JSON

Uses the coach's brand aesthetic preferences for visual consistency.
"""

import json
import os
from pathlib import Path
from typing import Optional

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain


VISUAL_BRIEF_PROMPT = """You are generating a visual brief for a webinar slide.

SLIDE CONTEXT:
- Headline: {headline}
- Teaching point: {teaching_point}
- Visual suggestion from generator: {visual_suggestion}

Generate a T2I (text-to-image) prompt for this slide visual. Rules:
1. WHITE BACKGROUND MANDATORY (for transparent extraction)
2. Clean, modern illustration style — not stock photography
3. No text in the image (text will be overlaid in Excalidraw)
4. Single focal element, centered composition
5. Professional, premium aesthetic

Return JSON:
{{
  "t2i_prompt": "detailed prompt for image generation...",
  "style_notes": "illustration style details",
  "focal_element": "what the main visual element is",
  "composition": "centered/left/right"
}}
"""


class TransparentCollagePipeline:
    """Generate transparent PNG visuals for webinar slides."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.asset_gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate_visual_brief(
        self,
        headline: str,
        teaching_point: str,
        visual_suggestion: str = "",
    ) -> dict:
        """Generate a T2I prompt from slide context.

        Args:
            headline: The slide headline
            teaching_point: The teaching content
            visual_suggestion: Optional suggestion from module generator

        Returns:
            Visual brief with T2I prompt, style notes, and composition
        """
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=VISUAL_BRIEF_PROMPT.format(
                headline=headline,
                teaching_point=teaching_point[:200],
                visual_suggestion=visual_suggestion or "No specific suggestion",
            ),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            brief = json.loads(text)
        except json.JSONDecodeError:
            brief = {
                "t2i_prompt": f"Clean modern illustration of {headline}, white background, centered",
                "style_notes": "minimal modern illustration",
                "focal_element": headline,
                "composition": "centered",
            }

        return brief

    async def process_webinar_visuals(
        self,
        webinar_json_path: str,
    ) -> list[dict]:
        """Generate visual briefs for all slides in a webinar.

        Args:
            webinar_json_path: Path to the webinar script JSON

        Returns:
            List of visual brief dicts, one per module
        """
        webinar = json.loads(Path(webinar_json_path).read_text(encoding="utf-8"))
        briefs = []

        for module in webinar.get("modules", []):
            slides = module.get("slides", [])
            for slide in slides:
                brief = await self.generate_visual_brief(
                    headline=slide.get("headline", ""),
                    teaching_point=slide.get("body", ""),
                    visual_suggestion=slide.get("visual_suggestion", ""),
                )
                brief["module_number"] = module.get("module_number", 0)
                brief["slide_number"] = slide.get("slide_number", 0)
                brief["asset_id"] = self.asset_gen.generate(AssetType.VISUAL_ASSET)
                briefs.append(brief)

        # Save briefs
        output_dir = Path(f"coaches/{self.coach_acronym}/production/webinars")
        output_dir.mkdir(parents=True, exist_ok=True)
        asset_id = webinar.get("asset_id", "webinar")
        briefs_path = output_dir / f"{asset_id}_visual_briefs.json"
        briefs_path.write_text(json.dumps(briefs, indent=2), encoding="utf-8")

        self.receipt_chain.log(
            agent_id="transparent_collage",
            action="generate_visual_briefs",
            asset_id=webinar.get("asset_id", ""),
            output_summary=f"Generated {len(briefs)} visual briefs",
            decision="completed",
            metadata={"brief_count": len(briefs)},
        )

        return briefs

    def inject_image_to_excalidraw(
        self,
        excalidraw_path: str,
        image_path: str,
        x: float,
        y: float,
        width: float = 400,
        height: float = 300,
    ) -> None:
        """Inject a transparent PNG as an image node in an Excalidraw file.

        Args:
            excalidraw_path: Path to the .excalidraw file
            image_path: Path to the transparent PNG
            x, y: Position on canvas
            width, height: Image dimensions
        """
        import base64
        import uuid

        excalidraw = json.loads(Path(excalidraw_path).read_text(encoding="utf-8"))

        # Read and base64 encode the image
        image_data = Path(image_path).read_bytes()
        b64_data = base64.b64encode(image_data).decode("utf-8")

        file_id = uuid.uuid4().hex[:20]

        # Add to files dict
        excalidraw.setdefault("files", {})[file_id] = {
            "mimeType": "image/png",
            "id": file_id,
            "dataURL": f"data:image/png;base64,{b64_data}",
            "created": 1,
        }

        # Add image element
        element = {
            "id": uuid.uuid4().hex[:20],
            "type": "image",
            "x": x, "y": y,
            "width": width, "height": height,
            "fileId": file_id,
            "status": "saved",
            "strokeColor": "transparent",
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 0,
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "seed": hash(file_id) % 2**31,
            "version": 1,
            "versionNonce": hash(file_id + "v") % 2**31,
            "isDeleted": False,
            "boundElements": None,
            "updated": 1,
            "link": None,
            "locked": False,
        }
        excalidraw["elements"].append(element)

        Path(excalidraw_path).write_text(json.dumps(excalidraw, indent=2), encoding="utf-8")
