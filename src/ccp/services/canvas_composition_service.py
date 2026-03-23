"""
FR-VIS-05 — Canvas Composition & Delivery
==========================================
Orchestrates VCB-to-composition assembly, RunningHub asset
reception, edge-bleed validation, carousel export, and operator
approval controls.

Pipeline stages:
  Stage 1 — VCB Intake & Template Loading
  Stage 2 — RunningHub Asset Reception
  Stage 3 — Seamless Carousel Export
  Stage 4 — Approval Controls

C-11 Persona Masking: agent names MUST NOT appear in external payloads.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    ApprovalAction,
    CanvasComposition,
    CanvasCompositionError,
    CIEDE2000_MAX_DISTANCE,
    CompositionDimensions,
    CompositionHandleBar,
    CompositionSlot,
    CompositionStatus,
    EDGE_BLEED_PX,
    EdgeBleedResult,
    ExportAssets,
    HANDLE_BAR_POSITION,
    RegenerationRequest,
)


# ── XSS sanitiser ─────────────────────────────────────────────────────

_SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def _sanitise(text: str) -> str:
    """Strip script blocks and all HTML tags from user/VCB text."""
    text = _SCRIPT_RE.sub("", text)
    return _TAG_RE.sub("", text).strip()


# ── template registry (stub) ──────────────────────────────────────────

# In production, templates are loaded from the file system or a DB.
# Here we keep a minimal registry for test/validation purposes.

_TEMPLATE_REGISTRY: dict[str, dict[str, Any]] = {}


def register_template(template_id: str, metadata: dict[str, Any]) -> None:
    """Register a Fabric.js template for the composition engine."""
    _TEMPLATE_REGISTRY[template_id] = metadata


def get_template(template_id: str) -> dict[str, Any] | None:
    return _TEMPLATE_REGISTRY.get(template_id)


# ── main service ───────────────────────────────────────────────────────

class CanvasCompositionService:
    """Orchestrates composition lifecycle (VCB intake → export → approval).

    Parameters
    ----------
    coach_acronym : str
        2-4 char coach scope (ADR-01).
    receipt_chain : ReceiptChain
        Audit log.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"{CanvasCompositionError.INVALID_COACH_ACRONYM.value}: "
                f"'{coach_acronym}' length must be 2-4."
            )
        self._coach = coach_acronym
        self._rc = receipt_chain
        # In-memory composition store (production uses DB)
        self._compositions: dict[str, CanvasComposition] = {}

    # ── Stage 1 — VCB Intake & Template Loading ───────────────────

    def create_composition(
        self,
        vcb_id: str,
        template_id: str,
        slide_count: int,
        dimensions: dict[str, Any],
        handle_bar: dict[str, Any],
        text_content: dict[int, dict[str, str]] | None = None,
        content_output_id: str | None = None,
    ) -> CanvasComposition:
        """Create a composition from a VCB.

        Parameters
        ----------
        vcb_id : str
        template_id : str — must resolve to a registered template.
        slide_count : int — number of slides (≥ 1).
        dimensions : dict with width_px, height_px, aspect_ratio.
        handle_bar : dict with coach_name, coach_handle, etc.
        text_content : optional {slide_index: {zone: text}} mapping.
        content_output_id : optional content output ID.
        """
        # template validation
        tpl = get_template(template_id)
        if tpl is None:
            raise ValueError(
                f"{CanvasCompositionError.TEMPLATE_NOT_FOUND.value}: "
                f"'{template_id}'"
            )

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        comp_id = f"COMP-{self._coach}-{now[:10].replace('-', '')}-{uuid.uuid4().hex[:6]}"

        # sanitise text content
        sanitised_text: dict[int, dict[str, str]] = {}
        warnings: list[str] = []
        if text_content:
            for si, zones in text_content.items():
                sanitised_text[si] = {}
                for zone, raw in zones.items():
                    clean = _sanitise(raw)
                    if clean != raw:
                        warnings.append(
                            f"XSS content sanitised in slide {si}, zone '{zone}'"
                        )
                    sanitised_text[si][zone] = clean

        # build slots
        slots: list[CompositionSlot] = []
        for i in range(slide_count):
            text_pop = i in sanitised_text and bool(sanitised_text[i])
            slots.append(
                CompositionSlot(
                    slide_index=i,
                    text_populated=text_pop,
                    image_populated=False,
                    image_source=None,
                    image_r2_url=None,
                    validation_verdict=None,
                )
            )

        # sanitise handle bar text
        hb_name = _sanitise(handle_bar.get("coach_name", ""))
        hb_handle = _sanitise(handle_bar.get("coach_handle", ""))
        hb = CompositionHandleBar(
            visible=handle_bar.get("visible", True),
            position=HANDLE_BAR_POSITION,
            coach_name=hb_name,
            coach_handle=hb_handle,
            profile_picture_url=handle_bar.get("profile_picture_url"),
            logo_url=handle_bar.get("logo_url"),
        )

        dims = CompositionDimensions(
            width_px=dimensions["width_px"],
            height_px=dimensions["height_px"],
            aspect_ratio=dimensions["aspect_ratio"],
        )

        comp = CanvasComposition(
            composition_id=comp_id,
            vcb_id=vcb_id,
            content_output_id=content_output_id,
            template_id=template_id,
            coach_acronym=self._coach,
            status=CompositionStatus.ASSEMBLING.value,
            dimensions=dims,
            slide_count=slide_count,
            handle_bar=hb,
            slots=slots,
            export_assets=ExportAssets(),
            approval_action=None,
            receipt_chain_block=None,
            timestamp_utc=now,
            warnings=warnings,
        )

        # receipt
        entry = self._rc.log(
            agent_id="canvas-composition-service",
            action="composition-create",
            asset_id=comp_id,
            input_summary=f"vcb={vcb_id} template={template_id}",
            output_summary=f"status=ASSEMBLING slides={slide_count}",
            metadata={"coach": self._coach},
        )
        comp.receipt_chain_block = entry.receipt_id

        self._compositions[comp_id] = comp
        return comp

    # ── Stage 2 — RunningHub Asset Reception ──────────────────────

    def receive_asset(
        self,
        composition_id: str,
        slide_index: int,
        image_url: str,
        image_source: str = "runninghub_tier_3",
        validation_verdict: str | None = None,
    ) -> CanvasComposition:
        """Populate an image slot in an existing composition."""
        comp = self._compositions.get(composition_id)
        if comp is None:
            raise ValueError(
                f"{CanvasCompositionError.WEBHOOK_TASK_MISMATCH.value}: "
                f"'{composition_id}' not found."
            )

        # find slot
        slot_found = False
        for slot in comp.slots:
            if slot.slide_index == slide_index:
                slot.image_populated = True
                slot.image_r2_url = image_url
                slot.image_source = image_source
                slot.validation_verdict = validation_verdict
                slot_found = True
                break

        if not slot_found:
            raise ValueError(
                f"{CanvasCompositionError.WEBHOOK_TASK_MISMATCH.value}: "
                f"slide_index {slide_index} not found in composition."
            )

        # check if all slots populated → READY_FOR_REVIEW
        if all(s.image_populated for s in comp.slots):
            comp.status = CompositionStatus.READY_FOR_REVIEW.value

        # receipt
        self._rc.log(
            agent_id="canvas-composition-service",
            action="asset-receive",
            asset_id=composition_id,
            input_summary=f"slide={slide_index} source={image_source}",
            output_summary=f"status={comp.status}",
        )

        return comp

    # ── Stage 3 — Edge Bleed Validation ───────────────────────────

    @staticmethod
    def validate_edge_bleeds(
        slide_colors: list[tuple[float, float, float]],
    ) -> list[EdgeBleedResult]:
        """Validate CIEDE2000 color distance between adjacent slides.

        Parameters
        ----------
        slide_colors : list of (L*, a*, b*) tuples — one per slide,
            representing the average colour of the bleed zone on the
            right edge of slide *i* and the left edge of slide *i+1*.

        Returns list of EdgeBleedResult (one per boundary).
        """
        results: list[EdgeBleedResult] = []
        for i in range(len(slide_colors) - 1):
            # simplified CIEDE2000 (Euclidean in Lab space — production
            # uses full CIEDE2000)
            l1, a1, b1 = slide_colors[i]
            l2, a2, b2 = slide_colors[i + 1]
            dist = ((l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5
            dist = round(dist, 2)
            result_label = "PASS" if dist <= CIEDE2000_MAX_DISTANCE else "FAIL"
            results.append(
                EdgeBleedResult(
                    left_slide_index=i,
                    right_slide_index=i + 1,
                    ciede2000_distance=dist,
                    threshold=CIEDE2000_MAX_DISTANCE,
                    result=result_label,
                )
            )
        return results

    # ── Stage 3 — Export ──────────────────────────────────────────

    def export_composition(
        self,
        composition_id: str,
        slide_urls: list[str] | None = None,
        stitch_url: str | None = None,
        zip_url: str | None = None,
    ) -> CanvasComposition:
        """Record export assets for a composition."""
        comp = self._compositions.get(composition_id)
        if comp is None:
            raise ValueError(
                f"{CanvasCompositionError.WEBHOOK_TASK_MISMATCH.value}: "
                f"'{composition_id}' not found."
            )

        comp.export_assets = ExportAssets(
            individual_slides=slide_urls or [],
            horizontal_stitch=stitch_url,
            zip_archive=zip_url,
        )

        self._rc.log(
            agent_id="canvas-composition-service",
            action="composition-export",
            asset_id=composition_id,
            output_summary=f"slides={len(comp.export_assets.individual_slides)}",
        )

        return comp

    # ── Stage 4 — Approval Controls ──────────────────────────────

    def approve(
        self,
        composition_id: str,
    ) -> CanvasComposition:
        """Approve & Publish — triggers downstream Notion sync."""
        comp = self._get_comp(composition_id)
        comp.status = CompositionStatus.APPROVED.value
        comp.approval_action = ApprovalAction.APPROVE_AND_PUBLISH.value

        entry = self._rc.log(
            agent_id="canvas-composition-service",
            action="composition-approve",
            asset_id=composition_id,
            output_summary="APPROVED → Notion sync triggered",
        )
        comp.receipt_chain_block = entry.receipt_id
        return comp

    def request_regeneration(
        self,
        composition_id: str,
        slide_index: int,
        revision_note: str,
    ) -> tuple[CanvasComposition, RegenerationRequest]:
        """Request regeneration for a specific slide."""
        comp = self._get_comp(composition_id)
        comp.status = CompositionStatus.REGENERATION_REQUESTED.value
        comp.approval_action = ApprovalAction.REQUEST_REGENERATION.value

        req = RegenerationRequest(
            slide_index=slide_index,
            revision_note=revision_note,
            vcb_id=comp.vcb_id,
        )

        # mark slot as not populated
        for slot in comp.slots:
            if slot.slide_index == slide_index:
                slot.image_populated = False
                slot.image_r2_url = None
                slot.image_source = None
                break

        self._rc.log(
            agent_id="canvas-composition-service",
            action="composition-request-regen",
            asset_id=composition_id,
            input_summary=f"slide={slide_index}",
            output_summary=f"revision_note={revision_note[:80]}",
        )
        return comp, req

    def edit_and_approve(
        self,
        composition_id: str,
    ) -> CanvasComposition:
        """Save operator edits then approve."""
        comp = self._get_comp(composition_id)
        comp.status = CompositionStatus.MANUALLY_EDITED_APPROVED.value
        comp.approval_action = ApprovalAction.EDIT_AND_APPROVE.value

        entry = self._rc.log(
            agent_id="canvas-composition-service",
            action="composition-edit-approve",
            asset_id=composition_id,
            output_summary="MANUALLY_EDITED_APPROVED → Notion sync triggered",
        )
        comp.receipt_chain_block = entry.receipt_id
        return comp

    # ── helpers ───────────────────────────────────────────────────

    def _get_comp(self, composition_id: str) -> CanvasComposition:
        comp = self._compositions.get(composition_id)
        if comp is None:
            raise ValueError(
                f"{CanvasCompositionError.WEBHOOK_TASK_MISMATCH.value}: "
                f"'{composition_id}' not found."
            )
        return comp

    def get_composition(self, composition_id: str) -> CanvasComposition | None:
        return self._compositions.get(composition_id)
