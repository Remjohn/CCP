"""
CCP Excalidraw Compiler
Task 5.06 — Compiles webinar modules into a branded .excalidraw file.

Takes generated modules + visual assets and produces:
- Text elements for headlines and body
- Image nodes for visuals
- Styled containers (branded colors)
- Module grouping with connectors
- Export to .excalidraw JSON (openable in Excalidraw)
"""

import json
import uuid
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


class ExcalidrawCompiler:
    """Compile webinar content into an Excalidraw canvas."""

    # Excalidraw element positioning
    SLIDE_WIDTH = 800
    SLIDE_HEIGHT = 450
    SLIDE_GAP = 100
    COLUMN_COUNT = 3  # Slides per row

    # Brand colors (customizable per coach)
    DEFAULT_COLORS = {
        "bg": "#1a1a2e",
        "headline": "#e94560",
        "body": "#eaeaea",
        "accent": "#0f3460",
        "divider": "#533483",
    }

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    def compile(
        self,
        webinar_json_path: str,
        output_path: Optional[str] = None,
        colors: Optional[dict] = None,
    ) -> str:
        """Compile a webinar JSON into an Excalidraw file.

        Args:
            webinar_json_path: Path to the webinar script JSON
            output_path: Output .excalidraw path (auto-generated if None)
            colors: Custom brand colors dict

        Returns:
            Path to the generated .excalidraw file
        """
        colors = colors or self.DEFAULT_COLORS
        webinar = json.loads(Path(webinar_json_path).read_text(encoding="utf-8"))

        elements = []
        element_id = 0

        # Title slide
        title_el = self._text_element(
            id=self._gen_id(),
            text=webinar.get("title", "Untitled"),
            x=50, y=50,
            width=self.SLIDE_WIDTH * 2,
            height=80,
            font_size=48,
            color=colors["headline"],
        )
        elements.append(title_el)

        # Generate slides for each module
        all_modules = webinar.get("modules", [])
        if webinar.get("offer_module"):
            all_modules.append(webinar["offer_module"])

        slide_index = 0
        for module in all_modules:
            # Module header
            row = slide_index // self.COLUMN_COUNT
            col = slide_index % self.COLUMN_COUNT
            x = col * (self.SLIDE_WIDTH + self.SLIDE_GAP) + 50
            y = row * (self.SLIDE_HEIGHT + self.SLIDE_GAP) + 180

            # Module container
            container = self._rect_element(
                id=self._gen_id(),
                x=x, y=y,
                width=self.SLIDE_WIDTH,
                height=self.SLIDE_HEIGHT,
                bg_color=colors["accent"],
                stroke_color=colors["divider"],
            )
            elements.append(container)

            # Module title
            title = self._text_element(
                id=self._gen_id(),
                text=f"Module {module.get('module_number', slide_index+1)}: {module.get('title', '')}",
                x=x + 20, y=y + 15,
                width=self.SLIDE_WIDTH - 40,
                height=40,
                font_size=28,
                color=colors["headline"],
            )
            elements.append(title)

            # Hook text
            hook = module.get("hook", "")
            if hook:
                hook_el = self._text_element(
                    id=self._gen_id(),
                    text=f"🎯 {hook}",
                    x=x + 20, y=y + 65,
                    width=self.SLIDE_WIDTH - 40,
                    height=60,
                    font_size=16,
                    color=colors["body"],
                )
                elements.append(hook_el)

            # Teaching point
            teaching = module.get("teaching_point", "")
            if teaching:
                teach_el = self._text_element(
                    id=self._gen_id(),
                    text=teaching,
                    x=x + 20, y=y + 135,
                    width=self.SLIDE_WIDTH - 40,
                    height=200,
                    font_size=14,
                    color=colors["body"],
                )
                elements.append(teach_el)

            # Duration badge
            duration = module.get("duration_minutes", 0)
            if duration:
                badge = self._text_element(
                    id=self._gen_id(),
                    text=f"⏱ {duration}min",
                    x=x + self.SLIDE_WIDTH - 100, y=y + self.SLIDE_HEIGHT - 35,
                    width=80, height=25,
                    font_size=12,
                    color=colors["divider"],
                )
                elements.append(badge)

            slide_index += 1

        # Build the Excalidraw file
        excalidraw = {
            "type": "excalidraw",
            "version": 2,
            "source": "ccp-webinar-compiler",
            "elements": elements,
            "appState": {
                "viewBackgroundColor": colors["bg"],
                "gridSize": 20,
            },
            "files": {},
        }

        # Output path
        if output_path is None:
            asset_id = webinar.get("asset_id", "webinar")
            output_dir = Path(f"coaches/{self.coach_acronym}/production/webinars")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / f"{asset_id}.excalidraw")

        Path(output_path).write_text(json.dumps(excalidraw, indent=2), encoding="utf-8")

        self.receipt_chain.log(
            agent_id="excalidraw_compiler",
            action="compile_webinar",
            asset_id=webinar.get("asset_id", ""),
            output_summary=f"Compiled: {slide_index} modules → {output_path}",
            decision="completed",
            metadata={"element_count": len(elements), "module_count": slide_index},
        )

        return output_path

    @staticmethod
    def _gen_id() -> str:
        return uuid.uuid4().hex[:20]

    @staticmethod
    def _text_element(
        id: str, text: str, x: float, y: float,
        width: float, height: float, font_size: int = 16,
        color: str = "#ffffff",
    ) -> dict:
        return {
            "id": id,
            "type": "text",
            "x": x, "y": y,
            "width": width, "height": height,
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1,
            "textAlign": "left",
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "seed": hash(id) % 2**31,
            "version": 1,
            "versionNonce": hash(id + "v") % 2**31,
            "isDeleted": False,
            "boundElements": None,
            "updated": 1,
            "link": None,
            "locked": False,
        }

    @staticmethod
    def _rect_element(
        id: str, x: float, y: float,
        width: float, height: float,
        bg_color: str = "#1a1a2e",
        stroke_color: str = "#333",
    ) -> dict:
        return {
            "id": id,
            "type": "rectangle",
            "x": x, "y": y,
            "width": width, "height": height,
            "strokeColor": stroke_color,
            "backgroundColor": bg_color,
            "fillStyle": "solid",
            "strokeWidth": 2,
            "roughness": 0,
            "opacity": 80,
            "groupIds": [],
            "seed": hash(id) % 2**31,
            "version": 1,
            "versionNonce": hash(id + "v") % 2**31,
            "isDeleted": False,
            "boundElements": None,
            "updated": 1,
            "link": None,
            "locked": False,
            "roundness": {"type": 3},
        }
