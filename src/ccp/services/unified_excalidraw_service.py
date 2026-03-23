"""
FR35 — Unified Excalidraw Pipeline Service (DEP-ENG-030)
Consumer of DEP-ENG-031 (Transparent Collage).
Handles horizontal (webinars) and vertical (tierlists) layouts.

AC1: Transparent collage integration from DEP-ENG-031.
AC2: Unified cross-format layout engine.
AC3: Brand consistency (stroke/fill enforcement).
AC4: Native editable text (no rasterized text).
"""

from __future__ import annotations

from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    ExcalidrawLayoutStrategy,
    SpatialLayoutEntry,
    TransparentCollageOutput,
    UnifiedExcalidrawPayload,
    YOLO_SLIDE_HEIGHT,
    YOLO_SLIDE_WIDTH,
)


# ── Layout Constants ───────────────────────────────────
HORIZONTAL_SLIDE_GAP: int = 100
VERTICAL_SECTION_GAP: int = 80
BRAND_STROKE_COLOR: str = "#111827"
BRAND_BACKGROUND_COLOR: str = "#ffffff"
TEXT_FONT_FAMILY: int = 1  # Virgil (hand-drawn)


class UnifiedExcalidrawService:
    """
    FR35: Unified Excalidraw pipeline — consumes DEP-ENG-031 images
    and assembles cross-format .excalidraw JSON.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)

    # ── Stage 1: Layout Parsing ────────────────────────

    def compute_layout(
        self,
        *,
        strategy: ExcalidrawLayoutStrategy,
        num_sections: int,
        section_width: int = YOLO_SLIDE_WIDTH,
        section_height: int = YOLO_SLIDE_HEIGHT,
    ) -> list[SpatialLayoutEntry]:
        """
        FR35 AC2: Compute spatial coordinates per strategy.
        """
        entries: list[SpatialLayoutEntry] = []

        for i in range(num_sections):
            if strategy == ExcalidrawLayoutStrategy.HORIZONTAL_SLIDE_SEQUENCE:
                x = i * (section_width + HORIZONTAL_SLIDE_GAP)
                y = 0
            else:  # VERTICAL_SCROLLING
                x = 0
                y = i * (section_height + VERTICAL_SECTION_GAP)

            entries.append(SpatialLayoutEntry(
                x=x,
                y=y,
                width=section_width,
                height=section_height,
                element_type="rectangle",
                stroke_color=BRAND_STROKE_COLOR,
                background_color=BRAND_BACKGROUND_COLOR,
            ))

        self._receipt_chain.log(
            agent_id="UnifiedExcalidrawService",
            action="LAYOUT_COMPUTED",
            asset_id=f"LAYOUT-{self._coach}",
            decision="SUCCESS",
            decision_rationale=f"strategy={strategy.value}, sections={num_sections}",
        )

        return entries

    # ── Stage 2: Element Assembly ──────────────────────

    def assemble_elements(
        self,
        *,
        layout: list[SpatialLayoutEntry],
        titles: list[str],
        body_texts: list[str],
        images: Optional[list[TransparentCollageOutput]] = None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """
        FR35 AC1/AC3/AC4: Assemble elements with brand consistency
        and native editable text.
        """
        elements: list[dict[str, Any]] = []
        files: dict[str, Any] = {}

        for i, entry in enumerate(layout):
            group_id = str(uuid4())

            # Background rectangle
            elements.append({
                "id": str(uuid4()),
                "type": "rectangle",
                "x": entry.x,
                "y": entry.y,
                "width": entry.width,
                "height": entry.height,
                "strokeColor": BRAND_STROKE_COLOR,
                "backgroundColor": BRAND_BACKGROUND_COLOR,
                "fillStyle": "solid",
                "groupIds": [group_id],
            })

            # FR35 AC4: Native editable text — title
            if i < len(titles):
                elements.append({
                    "id": str(uuid4()),
                    "type": "text",
                    "x": entry.x + 40,
                    "y": entry.y + 30,
                    "width": entry.width - 80,
                    "height": 40,
                    "text": titles[i],
                    "fontSize": 28,
                    "fontFamily": TEXT_FONT_FAMILY,
                    "groupIds": [group_id],
                })

            # Body text
            if i < len(body_texts):
                elements.append({
                    "id": str(uuid4()),
                    "type": "text",
                    "x": entry.x + 40,
                    "y": entry.y + 90,
                    "width": entry.width - 80,
                    "height": entry.height - 140,
                    "text": body_texts[i],
                    "fontSize": 16,
                    "fontFamily": TEXT_FONT_FAMILY,
                    "groupIds": [group_id],
                })

            # FR35 AC1: Transparent collage image from DEP-ENG-031
            if images and i < len(images):
                img = images[i]
                file_id = str(uuid4())
                files[file_id] = {
                    "mimeType": "image/png",
                    "id": file_id,
                    "dataURL": f"data:image/png;base64,{img.base64_png}",
                }
                elements.append({
                    "id": str(uuid4()),
                    "type": "image",
                    "x": entry.x + entry.width - 300,
                    "y": entry.y + entry.height - 300,
                    "width": 260,
                    "height": 260,
                    "fileId": file_id,
                    "groupIds": [group_id],
                })

        return elements, files

    # ── Full Pipeline ──────────────────────────────────

    def compile_payload(
        self,
        *,
        strategy: ExcalidrawLayoutStrategy,
        titles: list[str],
        body_texts: list[str],
        images: Optional[list[TransparentCollageOutput]] = None,
    ) -> UnifiedExcalidrawPayload:
        """
        FR35 §5: Full DEP-ENG-030 compilation.
        """
        num_sections = max(len(titles), len(body_texts))
        layout = self.compute_layout(
            strategy=strategy,
            num_sections=num_sections,
        )
        elements, files = self.assemble_elements(
            layout=layout,
            titles=titles,
            body_texts=body_texts,
            images=images,
        )

        payload = UnifiedExcalidrawPayload(
            elements=elements,
            files=files,
        )

        self._receipt_chain.log(
            agent_id="UnifiedExcalidrawService",
            action="EXCALIDRAW_PAYLOAD_COMPILED",
            asset_id=f"EXC-{self._coach}",
            decision="SUCCESS",
            decision_rationale=f"elements={len(elements)}, files={len(files)}",
        )

        return payload
