"""
FR-VIS-09 — Image Sourcing Hierarchy — Aurore Image Research Planner
Phase 2B, CVE Visual Engine — spec 5 of 13

Four-tier cascade sourcing orchestrator:
  Tier 1 — Named person → Known Persons Registry + SERPER fallback
  Tier 2 — Stock imagery  → Unsplash / Pexels / Pixabay / GIPHY / SERPER
  Tier 3 — AI realistic   → RunningHub semi-realistic (fallback from Tier 2)
  Tier 4 — AI Ghibli      → RunningHub Ghibli LoRA (format-restricted)

Cascade rule: tiers are a cascade, NOT a menu.
Named persons NEVER route to AI generation (AC4).
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    ADEQUACY_RELEVANCE_THRESHOLD,
    BATCH_ESCALATION_THRESHOLD,
    COMPATIBLE_LICENSES,
    MIN_RESOLUTION_PX,
    TIER4_PERMITTED_FORMATS,
    ImageResolutionMap,
    ImageSourcingError,
    ResolutionSummary,
    SlideResolution,
    SlideResolutionStatus,
    SourceTier,
    StockSearchResult,
    TierRoutingEntry,
)


# ── image-type → initial tier routing table (§4 Stage 1) ──

_IMAGE_TYPE_TIER_MAP: dict[str, SourceTier] = {
    # Tier 1
    "real_person_photo": SourceTier.TIER_1_REAL_PERSON,
    # Tier 2 variants
    "tier_2_stock_contextual": SourceTier.TIER_2_STOCK,
    "tier_2_stock_environmental": SourceTier.TIER_2_STOCK,
    "tier_2_stock_abstract": SourceTier.TIER_2_STOCK,
    "tier_2_stock_documentary": SourceTier.TIER_2_STOCK,
    "graphic_vector": SourceTier.TIER_2_STOCK,
    "animated_gif": SourceTier.TIER_2_STOCK,
    # Tier 3
    "tier_3_ai_realistic": SourceTier.TIER_3_AI_REALISTIC,
    # Tier 4
    "tier_4_ai_ghibli": SourceTier.TIER_4_AI_GHIBLI,
}

_TIER_FALLBACK_MAP: dict[SourceTier, list[SourceTier]] = {
    SourceTier.TIER_1_REAL_PERSON: [],  # Named person NEVER falls to AI
    SourceTier.TIER_2_STOCK: [SourceTier.TIER_3_AI_REALISTIC],
    SourceTier.TIER_3_AI_REALISTIC: [],  # Tier 3 failure → PENDING_HUMAN_REVIEW
    SourceTier.TIER_4_AI_GHIBLI: [],    # Tier 4 failure → PENDING_HUMAN_REVIEW
}


def _sanitize_search_query(query: str) -> str:
    """Remove embedded API params / injection attempts from search terms."""
    # Strip site:, filetype:, inurl:, and similar operators
    return re.sub(r'\b(site|filetype|inurl|intext|intitle|link):[^\s]+', '', query).strip()


def _parse_resolution(resolution_str: str | None) -> int:
    """Extract shortest edge from 'WxH' resolution string."""
    if not resolution_str:
        return 0
    parts = resolution_str.lower().split("x")
    if len(parts) != 2:
        return 0
    try:
        return min(int(parts[0]), int(parts[1]))
    except ValueError:
        return 0


class AuroreImageSourcing:
    """Parallel image resolution orchestrator (Aurore agent).

    Processes all VCB slides concurrently through the 4-tier cascade.
    External API calls are simulated via injectable providers for testing.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
        *,
        known_persons_provider: Any | None = None,
        stock_search_provider: Any | None = None,
        ai_generation_provider: Any | None = None,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got '{coach_acronym}'"
            )
        self.coach_acronym = coach_acronym
        self.receipt_chain = receipt_chain
        # Injectable providers for external API simulation
        self._known_persons = known_persons_provider
        self._stock_search = stock_search_provider
        self._ai_generation = ai_generation_provider

    # ── Stage 1: Per-Slide Tier Routing ──────────────────

    def route_slides(
        self,
        slides: list[dict[str, Any]],
        content_format: str | None = None,
    ) -> list[TierRoutingEntry]:
        """Route each slide to its initial tier based on image_type + named person.

        Args:
            slides: List of slide dicts. Required keys: 'slide_index', 'image_type'.
                    Optional: 'named_person_reference'.
            content_format: The VCB content format (for Tier 4 gating).

        Returns:
            List of TierRoutingEntry — one per slide.
        """
        format_permits_tier4 = (content_format or "").lower() in TIER4_PERMITTED_FORMATS
        entries: list[TierRoutingEntry] = []

        for slide in slides:
            slide_index = slide.get("slide_index", 0)
            image_type = slide.get("image_type", "")
            named_person = slide.get("named_person_reference")

            # Named person always routes to Tier 1 regardless of image_type
            if named_person:
                entries.append(TierRoutingEntry(
                    slide_index=slide_index,
                    image_type=image_type or "real_person_photo",
                    named_person_reference=named_person,
                    initial_tier=SourceTier.TIER_1_REAL_PERSON,
                    fallback_tiers=[],  # Never to AI
                    format_permits_tier4=format_permits_tier4,
                ))
                continue

            # Map image_type to tier
            tier = _IMAGE_TYPE_TIER_MAP.get(image_type)

            # Tier 4 format gating (AC5)
            if tier == SourceTier.TIER_4_AI_GHIBLI and not format_permits_tier4:
                # Reject: format doesn't permit Tier 4
                entries.append(TierRoutingEntry(
                    slide_index=slide_index,
                    image_type=image_type,
                    initial_tier=SourceTier.TIER_4_AI_GHIBLI,
                    fallback_tiers=[],
                    format_permits_tier4=False,
                ))
                continue

            # Legacy fallback: unknown image_type → Tier 2 default
            if tier is None:
                tier = SourceTier.TIER_2_STOCK

            fallback = list(_TIER_FALLBACK_MAP.get(tier, []))

            entries.append(TierRoutingEntry(
                slide_index=slide_index,
                image_type=image_type or "unknown",
                initial_tier=tier,
                fallback_tiers=fallback,
                format_permits_tier4=format_permits_tier4,
            ))

        return entries

    # ── Stage 2: Parallel Source Resolution ──────────────

    def resolve_slides(
        self,
        routing_entries: list[TierRoutingEntry],
        slide_params: list[dict[str, Any]] | None = None,
        stock_results: dict[int, StockSearchResult] | None = None,
        known_person_results: dict[int, dict[str, Any]] | None = None,
    ) -> list[SlideResolution]:
        """Resolve images for all slides (simulated parallel).

        Args:
            routing_entries: Output from route_slides().
            slide_params: Optional per-slide search parameters (tribal nouns, PAD).
            stock_results: Injectable Tier 2 results keyed by slide_index.
            known_person_results: Injectable Tier 1 results keyed by slide_index.

        Returns:
            List of SlideResolution — one per slide.
        """
        stock_results = stock_results or {}
        known_person_results = known_person_results or {}
        slide_params = slide_params or [{} for _ in routing_entries]
        resolutions: list[SlideResolution] = []

        for i, entry in enumerate(routing_entries):
            params = slide_params[i] if i < len(slide_params) else {}
            search_terms = self._derive_search_terms(params)
            provenance = self._build_provenance(params)

            resolution = self._resolve_single_slide(
                entry=entry,
                search_terms=search_terms,
                provenance=provenance,
                stock_result=stock_results.get(entry.slide_index),
                known_person_result=known_person_results.get(entry.slide_index),
            )
            resolutions.append(resolution)

        return resolutions

    def _resolve_single_slide(
        self,
        entry: TierRoutingEntry,
        search_terms: list[str],
        provenance: dict,
        stock_result: StockSearchResult | None = None,
        known_person_result: dict[str, Any] | None = None,
    ) -> SlideResolution:
        """Resolve a single slide through the tier cascade."""

        # ── Tier 4 format gating (AC5) ──
        if entry.initial_tier == SourceTier.TIER_4_AI_GHIBLI and not entry.format_permits_tier4:
            return SlideResolution(
                slide_index=entry.slide_index,
                image_type=entry.image_type,
                resolved_tier=None,
                status=SlideResolutionStatus.PENDING_HUMAN_REVIEW,
                search_terms_used=search_terms,
                provenance=provenance,
                error_type=ImageSourcingError.TIER4_FORMAT_NOT_PERMITTED.value,
                error_detail=f"Tier 4 Ghibli not permitted for this format",
            )

        # ── Tier 1: Named Person ──
        if entry.initial_tier == SourceTier.TIER_1_REAL_PERSON:
            return self._resolve_tier1(entry, search_terms, provenance, known_person_result)

        # ── Tier 3: Direct AI (no stock attempt) ──
        if entry.initial_tier == SourceTier.TIER_3_AI_REALISTIC:
            return self._resolve_tier3(entry, search_terms, provenance)

        # ── Tier 4: Direct Ghibli AI ──
        if entry.initial_tier == SourceTier.TIER_4_AI_GHIBLI:
            return self._resolve_tier4(entry, search_terms, provenance)

        # ── Tier 2: Stock → optional Tier 3 cascade ──
        return self._resolve_tier2(entry, search_terms, provenance, stock_result)

    def _resolve_tier1(
        self,
        entry: TierRoutingEntry,
        search_terms: list[str],
        provenance: dict,
        known_person_result: dict[str, Any] | None,
    ) -> SlideResolution:
        """Tier 1: Named person — Known Persons Registry → SERPER → PENDING_OPERATOR_REVIEW.
        NEVER routes to Tier 3 or 4 (AC4)."""

        if known_person_result and known_person_result.get("image_url"):
            return SlideResolution(
                slide_index=entry.slide_index,
                image_type=entry.image_type,
                resolved_tier=1,
                status=SlideResolutionStatus.RESOLVED,
                image_url=known_person_result["image_url"],
                source_api=known_person_result.get("source_api", "known_persons_registry"),
                relevance_score=known_person_result.get("relevance_score", 1.0),
                resolution_px=known_person_result.get("resolution_px"),
                licensing_type=known_person_result.get("licensing_type"),
                search_terms_used=search_terms,
                provenance=provenance,
            )

        # Named person not found → PENDING_OPERATOR_REVIEW (NEVER AI)
        return SlideResolution(
            slide_index=entry.slide_index,
            image_type=entry.image_type,
            resolved_tier=None,
            status=SlideResolutionStatus.PENDING_OPERATOR_REVIEW,
            search_terms_used=search_terms,
            provenance=provenance,
            error_type=ImageSourcingError.NAMED_PERSON_NOT_FOUND.value,
            error_detail=f"Named person '{entry.named_person_reference}' not resolved",
        )

    def _resolve_tier2(
        self,
        entry: TierRoutingEntry,
        search_terms: list[str],
        provenance: dict,
        stock_result: StockSearchResult | None,
    ) -> SlideResolution:
        """Tier 2: Stock imagery with adequacy check → Tier 3 cascade if fails."""

        if stock_result and stock_result.attempted:
            # Check adequacy threshold
            if self._is_stock_adequate(stock_result):
                return SlideResolution(
                    slide_index=entry.slide_index,
                    image_type=entry.image_type,
                    resolved_tier=2,
                    status=SlideResolutionStatus.RESOLVED,
                    image_url=f"https://r2.ccf-assets.com/stock/{stock_result.source_api or 'unknown'}-resolved.jpg",
                    source_api=stock_result.source_api,
                    relevance_score=stock_result.best_relevance_score,
                    resolution_px=stock_result.resolution_px,
                    licensing_type=stock_result.licensing_type,
                    search_terms_used=search_terms,
                    stock_search_result=stock_result,
                    provenance=provenance,
                )
            else:
                # Cascade to Tier 3
                if SourceTier.TIER_3_AI_REALISTIC in entry.fallback_tiers:
                    return SlideResolution(
                        slide_index=entry.slide_index,
                        image_type=entry.image_type,
                        resolved_tier=3,
                        status=SlideResolutionStatus.PENDING_AI_GENERATION,
                        search_terms_used=search_terms,
                        stock_search_result=stock_result,
                        ai_generation_queued=True,
                        provenance=provenance,
                    )

        # No stock result at all — cascade to Tier 3 if available
        if SourceTier.TIER_3_AI_REALISTIC in entry.fallback_tiers:
            return SlideResolution(
                slide_index=entry.slide_index,
                image_type=entry.image_type,
                resolved_tier=3,
                status=SlideResolutionStatus.PENDING_AI_GENERATION,
                search_terms_used=search_terms,
                stock_search_result=StockSearchResult(
                    attempted=False,
                    reason_rejected="No stock search result provided",
                ),
                ai_generation_queued=True,
                provenance=provenance,
            )

        # No fallback available
        return SlideResolution(
            slide_index=entry.slide_index,
            image_type=entry.image_type,
            resolved_tier=None,
            status=SlideResolutionStatus.PENDING_HUMAN_REVIEW,
            search_terms_used=search_terms,
            provenance=provenance,
            error_type=ImageSourcingError.STOCK_SEARCH_FAILED.value,
            error_detail="Stock search failed with no fallback tier",
        )

    def _resolve_tier3(
        self,
        entry: TierRoutingEntry,
        search_terms: list[str],
        provenance: dict,
    ) -> SlideResolution:
        """Tier 3: AI realistic — queued for Paradoxe PSSL compilation."""
        return SlideResolution(
            slide_index=entry.slide_index,
            image_type=entry.image_type,
            resolved_tier=3,
            status=SlideResolutionStatus.PENDING_AI_GENERATION,
            search_terms_used=search_terms,
            ai_generation_queued=True,
            provenance=provenance,
        )

    def _resolve_tier4(
        self,
        entry: TierRoutingEntry,
        search_terms: list[str],
        provenance: dict,
    ) -> SlideResolution:
        """Tier 4: AI Ghibli — queued for Paradoxe PSSL + LoRA compilation."""
        return SlideResolution(
            slide_index=entry.slide_index,
            image_type=entry.image_type,
            resolved_tier=4,
            status=SlideResolutionStatus.PENDING_AI_GENERATION,
            search_terms_used=search_terms,
            ai_generation_queued=True,
            provenance=provenance,
        )

    # ── Adequacy Check ───────────────────────────────

    def _is_stock_adequate(self, result: StockSearchResult) -> bool:
        """Check if stock search result meets adequacy threshold (§3).

        Three conditions — all must pass:
        1. Relevance score ≥ ADEQUACY_RELEVANCE_THRESHOLD (0.7)
        2. Resolution ≥ MIN_RESOLUTION_PX (1080) on shortest edge
        3. Compatible license
        """
        if result.best_relevance_score < ADEQUACY_RELEVANCE_THRESHOLD:
            return False

        shortest_edge = _parse_resolution(result.resolution_px)
        if shortest_edge > 0 and shortest_edge < MIN_RESOLUTION_PX:
            return False

        if result.licensing_type:
            if result.licensing_type.lower().replace(" ", "_") not in COMPATIBLE_LICENSES:
                return False

        return True

    # ── Search Term Derivation ───────────────────────

    def _derive_search_terms(self, params: dict[str, Any]) -> list[str]:
        """Derive search terms from VCB tribal nouns + PAD modifiers (§4 Stage 2).

        Produces specific, non-generic terms. NOT "morning" — instead
        "person reaching for alarm clock dark bedroom."
        """
        terms: list[str] = []

        # Tribal noun visual descriptors
        tribal_nouns: list[str] = params.get("tribal_nouns", [])
        visual_descriptors: list[str] = params.get("visual_descriptors", [])
        for desc in visual_descriptors:
            terms.append(_sanitize_search_query(desc))

        # PAD-based mood modifiers
        pad: dict[str, float] = params.get("pssl_mood", {})
        if pad:
            mood_term = self._pad_to_search_modifier(pad)
            if mood_term:
                terms.append(mood_term)

        # Slide description
        slide_desc: str = params.get("slide_description", "")
        if slide_desc:
            terms.append(_sanitize_search_query(slide_desc))

        return [t for t in terms if t]

    @staticmethod
    def _pad_to_search_modifier(pad: dict[str, float]) -> str:
        """Translate PAD vector to search modifiers.

        P (Pleasure): negative → dark/tense, positive → warm/bright
        A (Arousal): high → dramatic/dynamic, low → calm/still
        D (Dominance): low → constrained/tight, high → expansive/open
        """
        parts: list[str] = []
        p = pad.get("P", 0.0)
        a = pad.get("A", 0.0)
        d = pad.get("D", 0.0)

        if p < -0.3:
            parts.append("dark tense atmosphere")
        elif p > 0.3:
            parts.append("warm bright atmosphere")

        if a > 0.5:
            parts.append("dramatic dynamic lighting")
        elif a < -0.3:
            parts.append("calm still composition")

        if d < 0.3:
            parts.append("tight framing constrained")
        elif d > 0.6:
            parts.append("expansive open wide angle")

        return " ".join(parts) if parts else ""

    def _build_provenance(self, params: dict[str, Any]) -> dict:
        """Build provenance metadata from slide parameters."""
        prov: dict[str, Any] = {}
        if "pssl_mood" in params:
            prov["pssl_mood"] = params["pssl_mood"]
        if "tribal_nouns" in params:
            prov["tribal_nouns"] = params["tribal_nouns"]
        return prov

    # ── Stage 3: Image Resolution Map Assembly ───────

    def assemble_resolution_map(
        self,
        vcb_id: str,
        content_output_id: str,
        resolutions: list[SlideResolution],
        content_format: str | None = None,
    ) -> ImageResolutionMap:
        """Assemble the final ImageResolutionMap from all resolved slides.

        Applies batch escalation logic: >50% PENDING_HUMAN_REVIEW → escalate.
        Writes receipt chain block for audit.
        """
        total = len(resolutions)
        summary = ResolutionSummary()
        for r in resolutions:
            if r.status == SlideResolutionStatus.RESOLVED:
                if r.resolved_tier == 1:
                    summary.tier_1_resolved += 1
                elif r.resolved_tier == 2:
                    summary.tier_2_resolved += 1
            elif r.status == SlideResolutionStatus.PENDING_AI_GENERATION:
                if r.resolved_tier == 4:
                    summary.tier_4_pending_generation += 1
                else:
                    summary.tier_3_pending_generation += 1
            elif r.status == SlideResolutionStatus.PENDING_HUMAN_REVIEW:
                summary.pending_human_review += 1
            elif r.status == SlideResolutionStatus.PENDING_OPERATOR_REVIEW:
                summary.pending_operator_review += 1

        # Batch escalation check
        review_count = summary.pending_human_review + summary.pending_operator_review
        batch_escalated = (total > 0 and review_count / total > BATCH_ESCALATION_THRESHOLD)

        now = datetime.now(timezone.utc).isoformat()
        map_id = f"IRM-{self.coach_acronym}-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"

        # Receipt chain write
        receipt = self.receipt_chain.log(
            agent_id="aurore_image_sourcing",
            action="VIS09_RESOLUTION_MAP_ASSEMBLY",
            asset_id=content_output_id,
            input_summary=f"vcb_id={vcb_id}, slides={total}",
            output_summary=(
                f"t1={summary.tier_1_resolved}, t2={summary.tier_2_resolved}, "
                f"t3={summary.tier_3_pending_generation}, t4={summary.tier_4_pending_generation}, "
                f"review={review_count}, escalated={batch_escalated}"
            ),
            decision="BATCH_ESCALATED" if batch_escalated else "MAP_ASSEMBLED",
            decision_rationale=f"review_ratio={review_count}/{total}",
        )

        return ImageResolutionMap(
            resolution_map_id=map_id,
            vcb_id=vcb_id,
            content_output_id=content_output_id,
            content_format=content_format,
            total_slides=total,
            resolution_summary=summary,
            per_slide_resolution=resolutions,
            batch_escalated=batch_escalated,
            receipt_chain_block=receipt.receipt_id,
            timestamp_utc=now,
        )

    # ── Full Pipeline Orchestration ──────────────────

    def resolve_vcb(
        self,
        vcb_id: str,
        content_output_id: str,
        slides: list[dict[str, Any]],
        content_format: str | None = None,
        slide_params: list[dict[str, Any]] | None = None,
        stock_results: dict[int, StockSearchResult] | None = None,
        known_person_results: dict[int, dict[str, Any]] | None = None,
    ) -> ImageResolutionMap:
        """Full 3-stage pipeline: route → resolve → assemble.

        This is the main entry point for Aurore.
        """
        # Stage 1: Route
        routing = self.route_slides(slides, content_format)

        # Stage 1 receipt
        self.receipt_chain.log(
            agent_id="aurore_image_sourcing",
            action="VIS09_TIER_ROUTING",
            asset_id=content_output_id,
            input_summary=f"vcb_id={vcb_id}, slides={len(slides)}",
            output_summary=f"routing_entries={len(routing)}",
            decision="ROUTES_ASSIGNED",
        )

        # Stage 2: Resolve
        resolutions = self.resolve_slides(
            routing, slide_params, stock_results, known_person_results,
        )

        # Stage 2 receipt
        resolved_count = sum(
            1 for r in resolutions if r.status == SlideResolutionStatus.RESOLVED
        )
        self.receipt_chain.log(
            agent_id="aurore_image_sourcing",
            action="VIS09_PARALLEL_RESOLUTION",
            asset_id=content_output_id,
            input_summary=f"routing_entries={len(routing)}",
            output_summary=f"resolved={resolved_count}/{len(resolutions)}",
            decision="RESOLUTION_COMPLETE",
        )

        # Stage 3: Assemble
        return self.assemble_resolution_map(
            vcb_id, content_output_id, resolutions, content_format,
        )

    # ── Legacy Fallback ──────────────────────────────

    def resolve_legacy_vcb(
        self,
        vcb_id: str,
        content_output_id: str,
        total_slides: int,
        slide_texts: list[str | None] | None = None,
        stock_results: dict[int, StockSearchResult] | None = None,
    ) -> ImageResolutionMap:
        """§6: Legacy VCB without per-slide image_type fields.

        All slides default to Tier 2; stock failure cascades to Tier 3.
        Tier 4 never auto-assigned. LEGACY_SOURCING_DEFAULT warning logged.
        """
        slides: list[dict[str, Any]] = []
        for i in range(total_slides):
            slides.append({
                "slide_index": i,
                "image_type": "tier_2_stock_contextual",
            })

        irm = self.resolve_vcb(
            vcb_id=vcb_id,
            content_output_id=content_output_id,
            slides=slides,
            stock_results=stock_results,
        )
        irm.legacy_sourcing_warning = True
        return irm
