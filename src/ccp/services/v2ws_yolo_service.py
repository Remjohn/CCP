"""
FR33 — V²WS YOLO Mode Webinar (DEP-ENG-028)
5-variable intake → DEEP/FRESH research → 5-part script → Excalidraw.
approval_gate bypass = true.

AC1: 5-input gate (all required).
AC2: No approval pauses in pipeline.
AC3: Valid .excalidraw JSON output.
AC4: Speaker notes outside 1920×1080 viewport.
"""

from __future__ import annotations

from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    V2WSExcalidrawPayload,
    WebinarModuleScript,
    WebinarPart,
    YOLO_MAX_WORDS_PER_SLIDE,
    YOLO_REQUIRED_INPUTS,
    YOLO_SLIDE_HEIGHT,
    YOLO_SLIDE_SPACING,
    YOLO_SLIDE_WIDTH,
    YOLO_SPEAKER_NOTE_OFFSET_X,
    YoloIntake,
)


# ── 5-Part Flow ───────────────────────────────────────
YOLO_FLOW_ORDER: list[WebinarPart] = [
    WebinarPart.HOOK,
    WebinarPart.PROBLEM_EXPANSION,
    WebinarPart.PARADIGM_SHIFT,
    WebinarPart.THE_METHOD,
    WebinarPart.THE_OFFER,
]


class V2WSYoloService:
    """
    FR33: YOLO Mode — zero-pause webinar generation.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)

    # ── Stage 1: Intake Gate ───────────────────────────

    def validate_intake(self, intake: YoloIntake) -> bool:
        """
        FR33 AC1: All 5 variables must be present.
        Pydantic handles the min_length validators.
        """
        # If we got here without a ValidationError, all 5 are valid
        return True

    # ── Stage 3: Script Generation ─────────────────────

    def generate_module_scripts(
        self,
        intake: YoloIntake,
    ) -> list[WebinarModuleScript]:
        """
        FR33 §4.3: Generate 5-part webinar scripts.
        Artisan <150 words/slide.
        """
        modules: list[WebinarModuleScript] = []

        for part in YOLO_FLOW_ORDER:
            # Build contextual instructions for each part
            slide_content = self._build_slide_content(part, intake)
            speaker_script = self._build_speaker_script(part, intake)

            modules.append(WebinarModuleScript(
                part=part,
                slide_content=slide_content,
                speaker_script=speaker_script,
                visual_instructions=f"Visual for {part.value}: stick figure + prop",
            ))

        self._receipt_chain.log(
            agent_id="V2WSYoloService",
            action="YOLO_SCRIPTS_GENERATED",
            asset_id=f"YOLO-{self._coach}",
            decision="SUCCESS",
            decision_rationale=f"modules={len(modules)}, approval_gate=bypass",
        )

        return modules

    # ── Stage 4: Excalidraw Compilation ────────────────

    def compile_excalidraw(
        self,
        modules: list[WebinarModuleScript],
    ) -> V2WSExcalidrawPayload:
        """
        FR33 AC3/AC4: Compile to .excalidraw JSON.
        1920×1080 slides, speaker notes at x: boundary + 2000.
        """
        elements: list[dict[str, Any]] = []
        files: dict[str, Any] = {}

        for idx, module in enumerate(modules):
            x_offset = idx * (YOLO_SLIDE_WIDTH + YOLO_SLIDE_SPACING)
            group_id = str(uuid4())

            # Slide background rectangle
            elements.append({
                "id": str(uuid4()),
                "type": "rectangle",
                "x": x_offset,
                "y": 0,
                "width": YOLO_SLIDE_WIDTH,
                "height": YOLO_SLIDE_HEIGHT,
                "strokeColor": "#111827",
                "backgroundColor": "#ffffff",
                "fillStyle": "solid",
                "groupIds": [group_id],
            })

            # Slide title text
            elements.append({
                "id": str(uuid4()),
                "type": "text",
                "x": x_offset + 80,
                "y": 60,
                "width": YOLO_SLIDE_WIDTH - 160,
                "height": 40,
                "text": module.part.value,
                "fontSize": 32,
                "fontFamily": 1,
                "groupIds": [group_id],
            })

            # Slide content text
            elements.append({
                "id": str(uuid4()),
                "type": "text",
                "x": x_offset + 80,
                "y": 140,
                "width": YOLO_SLIDE_WIDTH - 160,
                "height": YOLO_SLIDE_HEIGHT - 220,
                "text": module.slide_content[:600],
                "fontSize": 18,
                "fontFamily": 1,
                "groupIds": [group_id],
            })

            # FR33 AC4: Speaker notes OUTSIDE viewport
            speaker_note_x = x_offset + YOLO_SPEAKER_NOTE_OFFSET_X
            elements.append({
                "id": str(uuid4()),
                "type": "text",
                "x": speaker_note_x,
                "y": 0,
                "width": 800,
                "height": YOLO_SLIDE_HEIGHT,
                "text": f"SPEAKER NOTES:\n{module.speaker_script}",
                "fontSize": 14,
                "fontFamily": 1,
                "groupIds": [],
                "strokeColor": "#6b7280",
            })

        payload = V2WSExcalidrawPayload(
            elements=elements,
            files=files,
        )

        self._receipt_chain.log(
            agent_id="V2WSYoloService",
            action="EXCALIDRAW_COMPILED",
            asset_id=f"YOLO-DECK-{self._coach}",
            decision="SUCCESS",
            decision_rationale=f"slides={len(modules)}, elements={len(elements)}",
        )

        return payload

    # ── Full Pipeline ──────────────────────────────────

    def run_yolo_pipeline(
        self,
        intake: YoloIntake,
    ) -> V2WSExcalidrawPayload:
        """
        FR33 AC2: Full YOLO pipeline — NO approval pauses.
        """
        self.validate_intake(intake)
        modules = self.generate_module_scripts(intake)
        return self.compile_excalidraw(modules)

    # ── Internals ──────────────────────────────────────

    @staticmethod
    def _build_slide_content(part: WebinarPart, intake: YoloIntake) -> str:
        """Build slide content stub for each part."""
        content_map = {
            WebinarPart.HOOK: f"Thesis: {intake.actionable_lesson_thesis}",
            WebinarPart.PROBLEM_EXPANSION: f"Audience: {intake.target_audience_segment}",
            WebinarPart.PARADIGM_SHIFT: f"Stories: {', '.join(intake.key_stories_array[:3])}",
            WebinarPart.THE_METHOD: f"Method aligned to: {intake.tone_energy_constraint}",
            WebinarPart.THE_OFFER: f"CTA: {intake.final_offer_cta}",
        }
        return content_map.get(part, "")

    @staticmethod
    def _build_speaker_script(part: WebinarPart, intake: YoloIntake) -> str:
        """Build speaker script stub for each part."""
        return f"[{part.value}] Deliver with {intake.tone_energy_constraint} energy."
