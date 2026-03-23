"""
FR-VIS-06 — Notion Visual Content Card
=======================================
Assembles the Visual Production Output (VPO) Notion page containing
6 sections:

  1. Card Header (identification & status)
  2. Preview (visual assets + downloads)
  3. Content Ready to Copy (hook, caption, hashtags, schedule)
  4. Why This Visual Was Built This Way (rationale)
  5. Leadership Farming Note (trait development)
  6. Technical Audit (collapsed — TIAR, AGSS, authenticity, receipt)

C-11 Persona Masking: agent names MUST NOT appear in external payloads.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AGSSAuditEntry,
    AuthenticityAuditEntry,
    CardHeader,
    ContentReadyToCopy,
    LeadershipFarmingNote,
    LeadershipTrait,
    NotionCardError,
    PostingRecommendation,
    PreviewAssets,
    SlidePreview,
    TechnicalAudit,
    TIARDecayEntry,
    VPONotionCard,
    VPOSyncStatus,
    WhyThisVisual,
)


# ── XSS sanitiser ─────────────────────────────────────────────────────

_SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def _sanitise(text: str) -> str:
    text = _SCRIPT_RE.sub("", text)
    return _TAG_RE.sub("", text).strip()


# ── protocol for Notion sync tool (dependency-injected) ────────────────

class NotionSyncClient(Protocol):
    """Structural typing for the Notion API sync tool (FR45)."""

    def create_page(
        self, database_id: str, properties: dict[str, Any], children: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Create a Notion page. Returns dict with 'id' key."""
        ...


# ── rationale template library ─────────────────────────────────────────

# Keyed by (recipe_type, visual_style). In production this would be a
# much larger registry loaded from config.

_RATIONALE_TEMPLATES: dict[str, dict[str, str]] = {}
_DATA_UNAVAILABLE = "DATA_UNAVAILABLE"


def register_rationale_template(
    recipe_type: str,
    arc_type_explanation: str,
    style_rationale: str,
    tribal_function: str,
) -> None:
    """Register a rationale template for a recipe type."""
    _RATIONALE_TEMPLATES[recipe_type] = {
        "arc_type_explanation": arc_type_explanation,
        "style_rationale": style_rationale,
        "tribal_function": tribal_function,
    }


def get_rationale_template(recipe_type: str) -> dict[str, str] | None:
    return _RATIONALE_TEMPLATES.get(recipe_type)


# ── leadership trait mapping ───────────────────────────────────────────

_LEADERSHIP_TRAIT_MAP: dict[str, tuple[str, str]] = {
    "dopamine_cliff": (
        LeadershipTrait.OBSERVER.value,
        "Publishing this visual positions you as someone who notices what "
        "others suppress. Your audience will recognise themselves in the "
        "observation, building the 'I'm not the only one' resonance.",
    ),
    "listicle": (
        LeadershipTrait.ARCHITECT.value,
        "This visual exercises the Architect trait — structuring chaotic "
        "experiences into a navigable framework your audience can hold onto.",
    ),
    "timeline": (
        LeadershipTrait.SHEPHERD.value,
        "This visual exercises the Shepherd trait — guiding your audience "
        "through a temporal sequence that normalises their journey.",
    ),
    "comparison": (
        LeadershipTrait.PROVOCATEUR.value,
        "This visual exercises the Provocateur trait — placing two realities "
        "side-by-side and letting the contrast speak for itself.",
    ),
    "single_image": (
        LeadershipTrait.MIRROR.value,
        "This visual exercises the Mirror trait — reflecting a single moment "
        "so precisely that the viewer sees their own experience in it.",
    ),
}


def register_leadership_mapping(
    recipe_type: str, trait: str, context: str
) -> None:
    _LEADERSHIP_TRAIT_MAP[recipe_type] = (trait, context)


# ── fingerprint ────────────────────────────────────────────────────────

def compute_fingerprint(data: dict[str, Any]) -> str:
    """SHA-256 of the canonical JSON representation."""
    canonical = json.dumps(data, sort_keys=True, default=str)
    return f"SHA256:{hashlib.sha256(canonical.encode()).hexdigest()}"


# ── main service ───────────────────────────────────────────────────────

class NotionVisualContentCardService:
    """Orchestrates VPO assembly and Notion sync.

    Parameters
    ----------
    coach_acronym : str
        2-4 char coach scope (ADR-01).
    coach_id : str
        Human-readable coach identifier.
    receipt_chain : ReceiptChain
        Audit log.
    notion_client : NotionSyncClient | None
        If None, all VPOs go to R2 fallback.
    notion_database_id : str
        Target Notion database.
    """

    def __init__(
        self,
        coach_acronym: str,
        coach_id: str,
        receipt_chain: ReceiptChain,
        notion_client: Optional[NotionSyncClient] = None,
        notion_database_id: str = "",
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"{NotionCardError.INVALID_COACH_ACRONYM.value}: "
                f"'{coach_acronym}' length must be 2-4."
            )
        self._coach = coach_acronym
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._notion = notion_client
        self._db_id = notion_database_id

    # ── public — assemble VPO ─────────────────────────────────────

    def assemble_vpo(
        self,
        composition_id: str,
        vcb_data: dict[str, Any],
        validation_results: list[dict[str, Any]] | None = None,
        tiar_audit: list[dict[str, Any]] | None = None,
        export_assets: dict[str, Any] | None = None,
        content_output: dict[str, Any] | None = None,
        receipt_block_ids: list[str] | None = None,
    ) -> VPONotionCard:
        """Assemble a VPO card from upstream data and optionally sync."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        date_str = now[:10]
        vpo_id = f"VPO-{self._coach}-{date_str.replace('-', '')}-{uuid.uuid4().hex[:6]}"
        ua_id = f"{self._coach}-VIS-{date_str.replace('-', '')}-{uuid.uuid4().hex[:4]}"
        warnings: list[str] = []

        # ── Section 1 — Card Header ────────────────────────────────
        header = self._build_header(vcb_data, ua_id, date_str, warnings)

        # ── Section 2 — Preview ────────────────────────────────────
        preview = self._build_preview(export_assets, warnings)

        # ── Section 3 — Content Ready to Copy ──────────────────────
        content = self._build_content(content_output, warnings)

        # ── Section 4 — Why This Visual ────────────────────────────
        why = self._build_rationale(vcb_data, tiar_audit, warnings)

        # ── Section 5 — Leadership Farming Note ────────────────────
        farming = self._build_farming_note(vcb_data, warnings)

        # ── Section 6 — Technical Audit ────────────────────────────
        audit = self._build_audit(
            validation_results, tiar_audit, receipt_block_ids, warnings
        )

        # ── Fingerprint ───────────────────────────────────────────
        fingerprint_data = {
            "vpo_id": vpo_id,
            "composition_id": composition_id,
            "header": header.model_dump(),
            "audit": audit.model_dump(),
        }
        audit.fingerprint_id = compute_fingerprint(fingerprint_data)

        # ── Sync ──────────────────────────────────────────────────
        notion_page_id: str | None = None
        sync_status = VPOSyncStatus.QUEUED.value
        r2_fallback: str | None = None

        if self._notion is not None:
            try:
                result = self._notion.create_page(
                    database_id=self._db_id,
                    properties={"title": vpo_id},
                    children=[],  # production builds full Notion blocks
                )
                notion_page_id = result.get("id")
                sync_status = VPOSyncStatus.SYNCED.value
            except Exception as exc:
                warnings.append(f"Notion sync failed: {exc}")
                sync_status = VPOSyncStatus.SYNC_FAILED.value
                r2_fallback = f"https://r2.ccf-assets.com/vpo-fallback/{vpo_id}.json"
        else:
            sync_status = VPOSyncStatus.R2_FALLBACK.value
            r2_fallback = f"https://r2.ccf-assets.com/vpo-fallback/{vpo_id}.json"
            warnings.append("Notion client unavailable — VPO stored in R2 fallback")

        # ── Receipt ───────────────────────────────────────────────
        entry = self._rc.log(
            agent_id="notion-visual-content-card",
            action="vpo-assemble",
            asset_id=vpo_id,
            input_summary=f"composition={composition_id}",
            output_summary=f"sync_status={sync_status}",
            metadata={"coach": self._coach, "fingerprint": audit.fingerprint_id},
        )

        return VPONotionCard(
            vpo_id=vpo_id,
            universal_asset_id=ua_id,
            notion_page_id=notion_page_id,
            coach_id=self._coach_id,
            coach_acronym=self._coach,
            card_header=header,
            preview_assets=preview,
            content_ready_to_copy=content,
            why_this_visual=why,
            leadership_farming_note=farming,
            technical_audit=audit,
            sync_status=sync_status,
            r2_fallback_url=r2_fallback,
            receipt_chain_block=entry.receipt_id,
            timestamp_utc=now,
            warnings=warnings,
        )

    # ── public — retry sync ───────────────────────────────────────

    def retry_sync(self, card: VPONotionCard) -> VPONotionCard:
        """Retry a failed Notion sync.  Returns updated card."""
        if self._notion is None:
            card.warnings.append("Notion client still unavailable")
            return card
        try:
            result = self._notion.create_page(
                database_id=self._db_id,
                properties={"title": card.vpo_id},
                children=[],
            )
            card.notion_page_id = result.get("id")
            card.sync_status = VPOSyncStatus.DELAYED_SYNC.value
            self._rc.log(
                agent_id="notion-visual-content-card",
                action="vpo-retry-sync",
                asset_id=card.vpo_id,
                output_summary="DELAYED_SYNC",
            )
        except Exception as exc:
            card.warnings.append(f"Retry failed: {exc}")
        return card

    # ── internal — section builders ───────────────────────────────

    def _build_header(
        self, vcb: dict[str, Any], ua_id: str, date: str, w: list[str]
    ) -> CardHeader:
        return CardHeader(
            universal_asset_id=ua_id,
            recipe_name=_sanitise(vcb.get("recipe_name", _DATA_UNAVAILABLE)),
            production_status=vcb.get("production_status", _DATA_UNAVAILABLE),
            date=date,
            visual_style=_sanitise(vcb.get("visual_style", _DATA_UNAVAILABLE)),
        )

    def _build_preview(
        self, assets: dict[str, Any] | None, w: list[str]
    ) -> PreviewAssets:
        if assets is None:
            w.append("MISSING_UPSTREAM_DATA: export_assets")
            return PreviewAssets(content_type="carousel")
        slides = [
            SlidePreview(slide_index=s["slide_index"], url=s["url"])
            for s in assets.get("slide_previews", [])
        ]
        return PreviewAssets(
            content_type=assets.get("type", "carousel"),
            horizontal_stitch_url=assets.get("horizontal_stitch_url"),
            slide_previews=slides,
            zip_download_url=assets.get("zip_download_url"),
        )

    def _build_content(
        self, co: dict[str, Any] | None, w: list[str]
    ) -> ContentReadyToCopy:
        if co is None:
            w.append("MISSING_UPSTREAM_DATA: content_output")
            return ContentReadyToCopy(hook_text=_DATA_UNAVAILABLE)
        pr = co.get("posting_recommendation")
        posting: PostingRecommendation | None = None
        if pr:
            posting = PostingRecommendation(
                day=pr.get("day", ""),
                time=pr.get("time", ""),
                rationale=pr.get("rationale", ""),
            )
        return ContentReadyToCopy(
            hook_text=_sanitise(co.get("hook_text", _DATA_UNAVAILABLE)),
            full_caption=_sanitise(co.get("full_caption", "")),
            hashtags=_sanitise(co.get("hashtags", "")),
            posting_recommendation=posting,
        )

    def _build_rationale(
        self,
        vcb: dict[str, Any],
        tiar: list[dict[str, Any]] | None,
        w: list[str],
    ) -> WhyThisVisual:
        recipe_type = vcb.get("recipe_type", "")
        tpl = get_rationale_template(recipe_type)
        if tpl is None:
            w.append(
                f"{NotionCardError.TEMPLATE_RATIONALE_MISSING.value}: "
                f"recipe_type='{recipe_type}'"
            )
            return WhyThisVisual(
                arc_type_explanation=_DATA_UNAVAILABLE,
                tiar_noun_rationale=_DATA_UNAVAILABLE,
                style_rationale=_DATA_UNAVAILABLE,
                tribal_function=_DATA_UNAVAILABLE,
            )

        # build TIAR noun rationale from audit data
        noun_parts: list[str] = []
        if tiar:
            for entry in tiar[:3]:  # top 3 nouns
                noun_parts.append(
                    f"'{entry.get('noun', '?')}' (TIRS {entry.get('tirs_score', '?')})"
                )
        tiar_rationale = (
            f"We used {', '.join(noun_parts)} because these phrases trigger "
            f"immediate identity recognition in your audience."
            if noun_parts
            else _DATA_UNAVAILABLE
        )

        return WhyThisVisual(
            arc_type_explanation=tpl["arc_type_explanation"],
            tiar_noun_rationale=tiar_rationale,
            style_rationale=tpl["style_rationale"],
            tribal_function=tpl["tribal_function"],
        )

    def _build_farming_note(
        self, vcb: dict[str, Any], w: list[str]
    ) -> LeadershipFarmingNote:
        recipe_type = vcb.get("recipe_type", "")
        mapping = _LEADERSHIP_TRAIT_MAP.get(recipe_type)
        if mapping is None:
            w.append(f"No leadership mapping for recipe_type='{recipe_type}'")
            return LeadershipFarmingNote(
                trait=_DATA_UNAVAILABLE,
                development_context=_DATA_UNAVAILABLE,
            )
        return LeadershipFarmingNote(trait=mapping[0], development_context=mapping[1])

    def _build_audit(
        self,
        validations: list[dict[str, Any]] | None,
        tiar: list[dict[str, Any]] | None,
        receipt_ids: list[str] | None,
        w: list[str],
    ) -> TechnicalAudit:
        tiar_entries: list[TIARDecayEntry] = []
        if tiar:
            for t in tiar:
                tiar_entries.append(
                    TIARDecayEntry(
                        noun=t.get("noun", ""),
                        tirs_score=float(t.get("tirs_score", 0.0)),
                        decay_stage=t.get("decay_stage", "unknown"),
                        last_measured=t.get("last_measured", ""),
                    )
                )
        else:
            w.append("MISSING_UPSTREAM_DATA: tiar_audit")

        agss_entries: list[AGSSAuditEntry] = []
        auth_entries: list[AuthenticityAuditEntry] = []
        if validations:
            for v in validations:
                agss = v.get("agss", {})
                agss_entries.append(
                    AGSSAuditEntry(
                        slide_index=v.get("slide_index", 0),
                        composite=float(agss.get("composite_score", 0.0)),
                        lighting=float(agss.get("lighting_naturalism", 0.0)),
                        texture=float(agss.get("texture_authenticity", 0.0)),
                        composition=float(agss.get("compositional_coherence", 0.0)),
                        emotion=float(agss.get("emotional_believability", 0.0)),
                    )
                )
                auth = v.get("authenticity", {})
                auth_entries.append(
                    AuthenticityAuditEntry(
                        slide_index=v.get("slide_index", 0),
                        expression=auth.get("expression_naturalness", "UNAVAILABLE"),
                        proportion=auth.get("facial_proportion", "UNAVAILABLE"),
                        skin_texture=auth.get("skin_texture", "UNAVAILABLE"),
                    )
                )
        else:
            w.append("MISSING_UPSTREAM_DATA: validation_results")

        return TechnicalAudit(
            collapsed=True,
            tiar_decay_status=tiar_entries,
            agss_scores=agss_entries,
            authenticity_checks=auth_entries,
            receipt_chain_status="VALID" if receipt_ids else "NO_RECEIPTS",
            receipt_chain_blocks=receipt_ids or [],
            fingerprint_id=None,  # computed after assembly
            asset_history=[],
        )
