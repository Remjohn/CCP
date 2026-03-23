"""
FR-VIS-09 — Image Sourcing Hierarchy — Integration Tests
Phase 2B, CVE Visual Engine — spec 5 of 13

Tests cover all 6 Acceptance Criteria (AC1-AC6) plus tier routing,
adequacy threshold, search term derivation, cascade logic, batch
escalation, legacy fallback, safety tests, and receipt chain integration
from FR-VIS-09 §8 and §10.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    ADEQUACY_RELEVANCE_THRESHOLD,
    BATCH_ESCALATION_THRESHOLD,
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
from src.ccp.services.aurore_image_sourcing import AuroreImageSourcing


# ─────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────


@pytest.fixture
def tmp_receipt_dir(tmp_path: Path) -> Path:
    receipt_dir = tmp_path / "receipts"
    receipt_dir.mkdir()
    return receipt_dir


@pytest.fixture
def receipt_chain(tmp_receipt_dir: Path) -> ReceiptChain:
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_receipt_dir))


@pytest.fixture
def aurore(receipt_chain: ReceiptChain) -> AuroreImageSourcing:
    return AuroreImageSourcing(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
    )


def _stock_hit(
    score: float = 0.85,
    resolution: str = "2400x3200",
    license_type: str = "unsplash_license",
    api: str = "unsplash",
) -> StockSearchResult:
    """Helper: create an adequate stock search result."""
    return StockSearchResult(
        attempted=True,
        best_relevance_score=score,
        resolution_px=resolution,
        licensing_type=license_type,
        reason_accepted=f"relevance ≥0.7, resolution ≥1080px, license compatible",
        source_api=api,
    )


def _stock_miss(
    score: float = 0.48,
    resolution: str = "2400x3200",
    license_type: str = "unsplash_license",
) -> StockSearchResult:
    """Helper: create a below-threshold stock search result."""
    return StockSearchResult(
        attempted=True,
        best_relevance_score=score,
        resolution_px=resolution,
        licensing_type=license_type,
        reason_rejected=f"relevance below {ADEQUACY_RELEVANCE_THRESHOLD} threshold",
        source_api="unsplash",
    )


# ═════════════════════════════════════════════════════
# SECTION 1: TIER ROUTING — FR-VIS-09 §4 Stage 1
# ═════════════════════════════════════════════════════


class TestTierRouting:
    """§4 Stage 1: Per-slide tier routing logic."""

    def test_named_person_routes_to_tier1(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual",
                    "named_person_reference": "Brené Brown"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_1_REAL_PERSON
        assert routes[0].named_person_reference == "Brené Brown"

    def test_tier2_stock_routing(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_2_STOCK
        assert SourceTier.TIER_3_AI_REALISTIC in routes[0].fallback_tiers

    def test_tier3_ai_routing(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_3_ai_realistic"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_3_AI_REALISTIC
        assert routes[0].fallback_tiers == []

    def test_tier4_ghibli_permitted_format(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_4_ai_ghibli"}]
        routes = aurore.route_slides(slides, content_format="carousel_conceptual_contrast")
        assert routes[0].initial_tier == SourceTier.TIER_4_AI_GHIBLI
        assert routes[0].format_permits_tier4 is True

    def test_tier4_ghibli_non_permitted_format(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_4_ai_ghibli"}]
        routes = aurore.route_slides(slides, content_format="carousel_dopamine_cliff")
        assert routes[0].initial_tier == SourceTier.TIER_4_AI_GHIBLI
        assert routes[0].format_permits_tier4 is False

    def test_unknown_image_type_defaults_tier2(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "some_unknown_type"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_2_STOCK

    def test_animated_gif_routes_tier2(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "animated_gif"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_2_STOCK

    def test_graphic_vector_routes_tier2(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "graphic_vector"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_2_STOCK

    def test_named_person_overrides_image_type(self, aurore: AuroreImageSourcing) -> None:
        """Named person always takes precedence over image_type."""
        slides = [{"slide_index": 0, "image_type": "tier_3_ai_realistic",
                    "named_person_reference": "Simon Sinek"}]
        routes = aurore.route_slides(slides)
        assert routes[0].initial_tier == SourceTier.TIER_1_REAL_PERSON

    def test_multiple_slides_routed(self, aurore: AuroreImageSourcing) -> None:
        slides = [
            {"slide_index": 0, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 1, "image_type": "tier_3_ai_realistic"},
            {"slide_index": 2, "image_type": "tier_2_stock_environmental"},
        ]
        routes = aurore.route_slides(slides)
        assert len(routes) == 3
        assert routes[0].initial_tier == SourceTier.TIER_2_STOCK
        assert routes[1].initial_tier == SourceTier.TIER_3_AI_REALISTIC
        assert routes[2].initial_tier == SourceTier.TIER_2_STOCK

    def test_named_person_no_fallback_tiers(self, aurore: AuroreImageSourcing) -> None:
        """AC4: Named person NEVER has AI fallback tiers."""
        slides = [{"slide_index": 0, "image_type": "real_person_photo",
                    "named_person_reference": "Brené Brown"}]
        routes = aurore.route_slides(slides)
        assert routes[0].fallback_tiers == []


# ═════════════════════════════════════════════════════
# SECTION 2: AC1 — TIER 1 NAMED PERSON RESOLUTION
# FR-VIS-09 §8 AC1
# ═════════════════════════════════════════════════════


class TestAC1NamedPersonResolution:
    """AC1: Named person → Tier 1 → Known Persons Registry → RESOLVED."""

    def test_named_person_resolves_tier1(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 2, "image_type": "real_person_photo",
                    "named_person_reference": "Brené Brown"}]
        routes = aurore.route_slides(slides)
        known = {2: {"image_url": "https://registry.ccf/brene-brown.jpg",
                      "source_api": "known_persons_registry",
                      "relevance_score": 1.0,
                      "resolution_px": "1200x1600",
                      "licensing_type": "editorial"}}
        resolutions = aurore.resolve_slides(routes, known_person_results=known)
        assert resolutions[0].resolved_tier == 1
        assert resolutions[0].status == SlideResolutionStatus.RESOLVED
        assert resolutions[0].image_url == "https://registry.ccf/brene-brown.jpg"

    def test_named_person_not_found_pending_operator(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """AC1: Named person not in registry → PENDING_OPERATOR_REVIEW."""
        slides = [{"slide_index": 2, "image_type": "real_person_photo",
                    "named_person_reference": "Brené Brown"}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes)  # No known person result
        assert resolutions[0].status == SlideResolutionStatus.PENDING_OPERATOR_REVIEW
        assert resolutions[0].error_type == ImageSourcingError.NAMED_PERSON_NOT_FOUND.value


# ═════════════════════════════════════════════════════
# SECTION 3: AC2 — TIER 2 → TIER 3 CASCADE
# FR-VIS-09 §8 AC2
# ═════════════════════════════════════════════════════


class TestAC2Tier2Tier3Cascade:
    """AC2: Stock score < 0.7 → cascade to Tier 3; score ≥ 0.7 → RESOLVED."""

    def test_adequate_stock_resolves_tier2(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: _stock_hit(score=0.84)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 2
        assert resolutions[0].status == SlideResolutionStatus.RESOLVED

    def test_inadequate_stock_cascades_to_tier3(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """AC2 primary: relevance 0.48 < 0.7 → cascade to Tier 3."""
        slides = [{"slide_index": 4, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {4: _stock_miss(score=0.48)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 3
        assert resolutions[0].status == SlideResolutionStatus.PENDING_AI_GENERATION
        assert resolutions[0].ai_generation_queued is True

    def test_mixed_slides_correct_tiers(self, aurore: AuroreImageSourcing) -> None:
        """AC2: multiple slides — adequate stays Tier 2, inadequate cascades."""
        slides = [
            {"slide_index": 0, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 1, "image_type": "tier_2_stock_environmental"},
            {"slide_index": 2, "image_type": "tier_2_stock_abstract"},
        ]
        routes = aurore.route_slides(slides)
        stock = {
            0: _stock_hit(score=0.84),
            1: _stock_miss(score=0.52),
            2: _stock_hit(score=0.71),
        }
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 2  # 0.84 ≥ 0.7
        assert resolutions[1].resolved_tier == 3  # 0.52 < 0.7 → cascade
        assert resolutions[2].resolved_tier == 2  # 0.71 ≥ 0.7

    def test_borderline_score_exact_threshold(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """Relevance exactly 0.7 is adequate."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: _stock_hit(score=0.7)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 2
        assert resolutions[0].status == SlideResolutionStatus.RESOLVED


# ═════════════════════════════════════════════════════
# SECTION 4: AC3 — PARALLEL PROCESSING
# FR-VIS-09 §8 AC3
# ═════════════════════════════════════════════════════


class TestAC3ParallelProcessing:
    """AC3: All slides processed concurrently (simulated — verify all resolved)."""

    def test_7_slide_carousel_all_processed(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """AC3: 7 slides — all produce a resolution (no silent drops)."""
        slides = [
            {"slide_index": i, "image_type": "tier_2_stock_contextual"}
            for i in range(7)
        ]
        routes = aurore.route_slides(slides)
        stock = {i: _stock_hit() for i in range(7)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert len(resolutions) == 7
        for r in resolutions:
            assert r.status == SlideResolutionStatus.RESOLVED

    def test_mixed_tiers_all_processed(self, aurore: AuroreImageSourcing) -> None:
        """AC3: Mixed tier slides — all processed."""
        slides = [
            {"slide_index": 0, "image_type": "real_person_photo",
             "named_person_reference": "Brené Brown"},
            {"slide_index": 1, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 2, "image_type": "tier_3_ai_realistic"},
            {"slide_index": 3, "image_type": "tier_2_stock_environmental"},
            {"slide_index": 4, "image_type": "tier_3_ai_realistic"},
            {"slide_index": 5, "image_type": "tier_4_ai_ghibli"},
            {"slide_index": 6, "image_type": "tier_2_stock_contextual"},
        ]
        routes = aurore.route_slides(slides, content_format="carousel_conceptual_contrast")
        known = {0: {"image_url": "https://reg/brene.jpg"}}
        stock = {1: _stock_hit(), 3: _stock_miss(), 6: _stock_hit()}
        resolutions = aurore.resolve_slides(
            routes, stock_results=stock, known_person_results=known
        )
        assert len(resolutions) == 7
        # Verify each slide got some status
        for r in resolutions:
            assert r.status in {
                SlideResolutionStatus.RESOLVED,
                SlideResolutionStatus.PENDING_AI_GENERATION,
                SlideResolutionStatus.PENDING_HUMAN_REVIEW,
                SlideResolutionStatus.PENDING_OPERATOR_REVIEW,
            }


# ═════════════════════════════════════════════════════
# SECTION 5: AC4 — NAMED PERSON NEVER ROUTES TO AI
# FR-VIS-09 §8 AC4
# ═════════════════════════════════════════════════════


class TestAC4NamedPersonNeverAI:
    """AC4: Named person w/ no registry + no SERPER → PENDING_OPERATOR_REVIEW.
    NEVER cascades to Tier 3 or 4."""

    def test_named_person_no_sources_pending_operator(
        self, aurore: AuroreImageSourcing
    ) -> None:
        slides = [{"slide_index": 0, "image_type": "real_person_photo",
                    "named_person_reference": "Simon Sinek"}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes)
        assert resolutions[0].status == SlideResolutionStatus.PENDING_OPERATOR_REVIEW
        assert resolutions[0].resolved_tier is None
        # Verify NOT Tier 3 or 4
        assert resolutions[0].ai_generation_queued is False

    def test_named_person_fallback_never_contains_ai(
        self, aurore: AuroreImageSourcing
    ) -> None:
        slides = [{"slide_index": 0, "image_type": "real_person_photo",
                    "named_person_reference": "Simon Sinek"}]
        routes = aurore.route_slides(slides)
        assert SourceTier.TIER_3_AI_REALISTIC not in routes[0].fallback_tiers
        assert SourceTier.TIER_4_AI_GHIBLI not in routes[0].fallback_tiers


# ═════════════════════════════════════════════════════
# SECTION 6: AC5 — TIER 4 FORMAT RESTRICTION
# FR-VIS-09 §8 AC5
# ═════════════════════════════════════════════════════


class TestAC5Tier4FormatRestriction:
    """AC5: Tier 4 only for permitted formats (conceptual_contrast, supervisual)."""

    def test_tier4_allowed_on_conceptual_contrast(
        self, aurore: AuroreImageSourcing
    ) -> None:
        slides = [{"slide_index": 3, "image_type": "tier_4_ai_ghibli"}]
        routes = aurore.route_slides(slides, content_format="carousel_conceptual_contrast")
        resolutions = aurore.resolve_slides(routes)
        assert resolutions[0].resolved_tier == 4
        assert resolutions[0].status == SlideResolutionStatus.PENDING_AI_GENERATION

    def test_tier4_rejected_on_dopamine_cliff(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """AC5 primary: carousel_dopamine_cliff does NOT permit Tier 4."""
        slides = [{"slide_index": 3, "image_type": "tier_4_ai_ghibli"}]
        routes = aurore.route_slides(slides, content_format="carousel_dopamine_cliff")
        resolutions = aurore.resolve_slides(routes)
        assert resolutions[0].status == SlideResolutionStatus.PENDING_HUMAN_REVIEW
        assert resolutions[0].error_type == ImageSourcingError.TIER4_FORMAT_NOT_PERMITTED.value

    def test_tier4_allowed_on_supervisual(
        self, aurore: AuroreImageSourcing
    ) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_4_ai_ghibli"}]
        routes = aurore.route_slides(slides, content_format="supervisual")
        resolutions = aurore.resolve_slides(routes)
        assert resolutions[0].resolved_tier == 4
        assert resolutions[0].status == SlideResolutionStatus.PENDING_AI_GENERATION

    def test_tier4_rejected_on_empty_format(
        self, aurore: AuroreImageSourcing
    ) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_4_ai_ghibli"}]
        routes = aurore.route_slides(slides, content_format=None)
        resolutions = aurore.resolve_slides(routes)
        assert resolutions[0].status == SlideResolutionStatus.PENDING_HUMAN_REVIEW


# ═════════════════════════════════════════════════════
# SECTION 7: AC6 — BATCH ESCALATION
# FR-VIS-09 §8 AC6
# ═════════════════════════════════════════════════════


class TestAC6BatchEscalation:
    """AC6: >50% slides PENDING_HUMAN_REVIEW → batch escalation."""

    def test_4_of_6_pending_escalates(self, aurore: AuroreImageSourcing) -> None:
        """AC6 primary: 4/6 slides fail → >50% → batch_escalated=True."""
        slides = [
            {"slide_index": i, "image_type": "tier_2_stock_contextual"}
            for i in range(6)
        ]
        routes = aurore.route_slides(slides)
        # 2 adequate, 4 will have no stock → cascade to Tier 3 (not pending review)
        # Need to force PENDING_HUMAN_REVIEW: use animated_gif with no fallback
        slides_no_fallback = [
            {"slide_index": i, "image_type": "animated_gif"} for i in range(6)
        ]
        routes = aurore.route_slides(slides_no_fallback)
        # animated_gif routes to Tier 2 with Tier 3 fallback — that would cascade.
        # Let's use the full pipeline with stock results that fail for 4 slides.
        # Actually, Tier 2 with fallback to Tier 3 won't produce PENDING_HUMAN_REVIEW.
        # Need named persons with no results for 4 slides.
        slides_mixed = [
            {"slide_index": 0, "image_type": "real_person_photo",
             "named_person_reference": "Person A"},
            {"slide_index": 1, "image_type": "real_person_photo",
             "named_person_reference": "Person B"},
            {"slide_index": 2, "image_type": "real_person_photo",
             "named_person_reference": "Person C"},
            {"slide_index": 3, "image_type": "real_person_photo",
             "named_person_reference": "Person D"},
            {"slide_index": 4, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 5, "image_type": "tier_2_stock_contextual"},
        ]
        routes = aurore.route_slides(slides_mixed)
        stock = {4: _stock_hit(), 5: _stock_hit()}
        # 4 named persons with no results → PENDING_OPERATOR_REVIEW
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        irm = aurore.assemble_resolution_map(
            "VCB-TST-AC6", "CO-TST-AC6", resolutions
        )
        assert irm.batch_escalated is True
        assert irm.resolution_summary.pending_operator_review == 4

    def test_1_of_6_pending_no_escalation(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """1/6 pending → 16.7% → not escalated."""
        slides = [
            {"slide_index": 0, "image_type": "real_person_photo",
             "named_person_reference": "Person A"},  # Will be pending
            {"slide_index": 1, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 2, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 3, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 4, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 5, "image_type": "tier_2_stock_contextual"},
        ]
        routes = aurore.route_slides(slides)
        stock = {i: _stock_hit() for i in range(1, 6)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        irm = aurore.assemble_resolution_map(
            "VCB-TST-AC6-NO", "CO-TST-AC6-NO", resolutions
        )
        assert irm.batch_escalated is False

    def test_3_of_6_pending_exact_50_not_escalated(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """3/6 = 50% exactly → NOT escalated (>50% required, not ≥50%)."""
        slides = [
            {"slide_index": 0, "image_type": "real_person_photo",
             "named_person_reference": "A"},
            {"slide_index": 1, "image_type": "real_person_photo",
             "named_person_reference": "B"},
            {"slide_index": 2, "image_type": "real_person_photo",
             "named_person_reference": "C"},
            {"slide_index": 3, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 4, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 5, "image_type": "tier_2_stock_contextual"},
        ]
        routes = aurore.route_slides(slides)
        stock = {i: _stock_hit() for i in range(3, 6)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        irm = aurore.assemble_resolution_map(
            "VCB-TST-AC6-50", "CO-TST-AC6-50", resolutions
        )
        assert irm.batch_escalated is False  # 50% is not >50%


# ═════════════════════════════════════════════════════
# SECTION 8: ADEQUACY THRESHOLD — §3 / §10
# ═════════════════════════════════════════════════════


class TestAdequacyThreshold:
    """§3: Stock image adequacy — relevance, resolution, license."""

    def test_relevance_065_cascades(self, aurore: AuroreImageSourcing) -> None:
        """0.65 < 0.7 → cascades to Tier 3."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: _stock_miss(score=0.65)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 3

    def test_relevance_071_resolves(self, aurore: AuroreImageSourcing) -> None:
        """0.71 ≥ 0.7 → resolves at Tier 2."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: _stock_hit(score=0.71)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 2

    def test_relevance_088_resolves(self, aurore: AuroreImageSourcing) -> None:
        """0.88 ≥ 0.7 → resolves at Tier 2."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: _stock_hit(score=0.88)}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 2

    def test_low_resolution_cascades(self, aurore: AuroreImageSourcing) -> None:
        """Resolution < 1080px → cascades even if relevance is high."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: StockSearchResult(
            attempted=True, best_relevance_score=0.92,
            resolution_px="800x600", licensing_type="unsplash_license",
        )}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 3

    def test_incompatible_license_cascades(
        self, aurore: AuroreImageSourcing
    ) -> None:
        """Incompatible license → cascades."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: StockSearchResult(
            attempted=True, best_relevance_score=0.85,
            resolution_px="2400x3200", licensing_type="rights_managed_exclusive",
        )}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        assert resolutions[0].resolved_tier == 3


# ═════════════════════════════════════════════════════
# SECTION 9: SEARCH TERM DERIVATION — §10
# ═════════════════════════════════════════════════════


class TestSearchTermDerivation:
    """§10: Specific, non-generic search terms from VCB params."""

    def test_visual_descriptors_included(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        params = [{"visual_descriptors": [
            "person reaching for alarm clock dark bedroom",
            "dimly lit bedroom morning dread",
        ]}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes, slide_params=params)
        terms = resolutions[0].search_terms_used
        assert "person reaching for alarm clock dark bedroom" in terms

    def test_pad_negative_pleasure_dark(self, aurore: AuroreImageSourcing) -> None:
        """Negative pleasure → dark/tense mood modifier."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        params = [{"pssl_mood": {"P": -0.5, "A": 0.7, "D": 0.2}}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes, slide_params=params)
        terms = resolutions[0].search_terms_used
        mood_terms = [t for t in terms if "dark" in t.lower() or "tense" in t.lower()]
        assert len(mood_terms) >= 1

    def test_search_injection_sanitized(self, aurore: AuroreImageSourcing) -> None:
        """§10 Safety: Injected 'site:malicious.com' is stripped."""
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        params = [{"visual_descriptors": [
            '"alarm clock" site:malicious.com'
        ]}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes, slide_params=params)
        terms = resolutions[0].search_terms_used
        for t in terms:
            assert "site:" not in t
            assert "malicious.com" not in t


# ═════════════════════════════════════════════════════
# SECTION 10: RESOLUTION MAP ASSEMBLY — §4 Stage 3
# ═════════════════════════════════════════════════════


class TestResolutionMapAssembly:
    """§4 Stage 3: Full resolution map assembly."""

    def test_resolution_summary_counts(self, aurore: AuroreImageSourcing) -> None:
        slides = [
            {"slide_index": 0, "image_type": "real_person_photo",
             "named_person_reference": "Brené Brown"},
            {"slide_index": 1, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 2, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 3, "image_type": "tier_3_ai_realistic"},
            {"slide_index": 4, "image_type": "tier_4_ai_ghibli"},
        ]
        routes = aurore.route_slides(slides, content_format="carousel_conceptual_contrast")
        known = {0: {"image_url": "https://reg/brene.jpg"}}
        stock = {1: _stock_hit(), 2: _stock_miss()}
        resolutions = aurore.resolve_slides(routes, stock_results=stock,
                                            known_person_results=known)
        irm = aurore.assemble_resolution_map(
            "VCB-TST-MAP", "CO-TST-MAP", resolutions, "carousel_conceptual_contrast"
        )
        assert irm.total_slides == 5
        assert irm.resolution_summary.tier_1_resolved == 1
        assert irm.resolution_summary.tier_2_resolved == 1
        assert irm.resolution_summary.tier_3_pending_generation == 2  # cascade + direct
        assert irm.resolution_summary.tier_4_pending_generation == 1
        assert irm.resolution_summary.pending_human_review == 0

    def test_resolution_map_has_receipt(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        stock = {0: _stock_hit()}
        resolutions = aurore.resolve_slides(routes, stock_results=stock)
        irm = aurore.assemble_resolution_map("VCB-1", "CO-1", resolutions)
        assert irm.receipt_chain_block is not None

    def test_resolution_map_id_format(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes, stock_results={0: _stock_hit()})
        irm = aurore.assemble_resolution_map("VCB-1", "CO-1", resolutions)
        assert irm.resolution_map_id.startswith("IRM-TST-")

    def test_timestamp_utc_present(self, aurore: AuroreImageSourcing) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        routes = aurore.route_slides(slides)
        resolutions = aurore.resolve_slides(routes, stock_results={0: _stock_hit()})
        irm = aurore.assemble_resolution_map("VCB-1", "CO-1", resolutions)
        assert irm.timestamp_utc is not None


# ═════════════════════════════════════════════════════
# SECTION 11: FULL PIPELINE (resolve_vcb) — §4
# ═════════════════════════════════════════════════════


class TestFullPipeline:
    """Full 3-stage pipeline via resolve_vcb()."""

    def test_full_pipeline_7_slides(self, aurore: AuroreImageSourcing) -> None:
        """Full cascade: 1 T1, 3 T2 (1 inadequate), 2 T3, 1 T4."""
        slides = [
            {"slide_index": 0, "image_type": "real_person_photo",
             "named_person_reference": "Brené Brown"},
            {"slide_index": 1, "image_type": "tier_2_stock_contextual"},
            {"slide_index": 2, "image_type": "tier_2_stock_environmental"},
            {"slide_index": 3, "image_type": "tier_2_stock_abstract"},
            {"slide_index": 4, "image_type": "tier_3_ai_realistic"},
            {"slide_index": 5, "image_type": "tier_3_ai_realistic"},
            {"slide_index": 6, "image_type": "tier_4_ai_ghibli"},
        ]
        known = {0: {"image_url": "https://reg/brene.jpg"}}
        stock = {
            1: _stock_hit(score=0.84),
            2: _stock_miss(score=0.52),  # Will cascade
            3: _stock_hit(score=0.78),
        }
        irm = aurore.resolve_vcb(
            vcb_id="VCB-TST-FULL",
            content_output_id="CO-TST-FULL",
            slides=slides,
            content_format="carousel_conceptual_contrast",
            stock_results=stock,
            known_person_results=known,
        )
        assert irm.total_slides == 7
        assert irm.resolution_summary.tier_1_resolved == 1
        assert irm.resolution_summary.tier_2_resolved == 2
        # Tier 3: 2 direct + 1 cascade = 3
        assert irm.resolution_summary.tier_3_pending_generation == 3
        assert irm.resolution_summary.tier_4_pending_generation == 1
        assert irm.batch_escalated is False


# ═════════════════════════════════════════════════════
# SECTION 12: LEGACY FALLBACK — §6
# ═════════════════════════════════════════════════════


class TestLegacyFallback:
    """§6: VCB without per-slide image_type fields."""

    def test_legacy_defaults_to_tier2(self, aurore: AuroreImageSourcing) -> None:
        stock = {i: _stock_hit() for i in range(3)}
        irm = aurore.resolve_legacy_vcb(
            "VCB-LEGACY", "CO-LEGACY", total_slides=3, stock_results=stock
        )
        assert irm.legacy_sourcing_warning is True
        assert irm.resolution_summary.tier_2_resolved == 3

    def test_legacy_cascade_to_tier3(self, aurore: AuroreImageSourcing) -> None:
        stock = {0: _stock_hit(), 1: _stock_miss()}
        irm = aurore.resolve_legacy_vcb(
            "VCB-LEGACY2", "CO-LEGACY2", total_slides=2, stock_results=stock
        )
        assert irm.resolution_summary.tier_2_resolved == 1
        assert irm.resolution_summary.tier_3_pending_generation == 1

    def test_legacy_never_assigns_tier4(self, aurore: AuroreImageSourcing) -> None:
        stock = {0: _stock_miss(), 1: _stock_miss()}
        irm = aurore.resolve_legacy_vcb(
            "VCB-LEGACY3", "CO-LEGACY3", total_slides=2, stock_results=stock
        )
        assert irm.resolution_summary.tier_4_pending_generation == 0


# ═════════════════════════════════════════════════════
# SECTION 13: RECEIPT CHAIN INTEGRATION
# ═════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """DEP-ENG-041: Receipt writes at every stage."""

    def test_full_pipeline_writes_3_receipts(
        self, aurore: AuroreImageSourcing, receipt_chain: ReceiptChain
    ) -> None:
        """3 stages → 3 receipt writes."""
        initial = receipt_chain.chain_length()
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        aurore.resolve_vcb("VCB-RCH", "CO-RCH", slides, stock_results={0: _stock_hit()})
        assert receipt_chain.chain_length() == initial + 3

    def test_receipt_actions_correct(
        self, aurore: AuroreImageSourcing, receipt_chain: ReceiptChain
    ) -> None:
        slides = [{"slide_index": 0, "image_type": "tier_2_stock_contextual"}]
        aurore.resolve_vcb("VCB-RCH2", "CO-RCH2", slides, stock_results={0: _stock_hit()})
        entries = receipt_chain.query(agent_id="aurore_image_sourcing", limit=100)
        actions = {e.action for e in entries}
        assert "VIS09_TIER_ROUTING" in actions
        assert "VIS09_PARALLEL_RESOLUTION" in actions
        assert "VIS09_RESOLUTION_MAP_ASSEMBLY" in actions

    def test_assembly_only_writes_1_receipt(
        self, aurore: AuroreImageSourcing, receipt_chain: ReceiptChain
    ) -> None:
        resolutions = [SlideResolution(
            slide_index=0, image_type="tier_2_stock_contextual",
            resolved_tier=2, status=SlideResolutionStatus.RESOLVED,
        )]
        initial = receipt_chain.chain_length()
        aurore.assemble_resolution_map("VCB-A", "CO-A", resolutions)
        assert receipt_chain.chain_length() == initial + 1


# ═════════════════════════════════════════════════════
# SECTION 14: ADR-01 COACH ACRONYM
# ═════════════════════════════════════════════════════


class TestADR01CoachAcronym:
    """ADR-01: 2-4 character coach acronym enforcement."""

    def test_valid_2_char(self, receipt_chain: ReceiptChain) -> None:
        a = AuroreImageSourcing(coach_acronym="JP", receipt_chain=receipt_chain)
        assert a.coach_acronym == "JP"

    def test_valid_4_char(self, receipt_chain: ReceiptChain) -> None:
        a = AuroreImageSourcing(coach_acronym="JPGR", receipt_chain=receipt_chain)
        assert a.coach_acronym == "JPGR"

    def test_1_char_rejected(self, receipt_chain: ReceiptChain) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            AuroreImageSourcing(coach_acronym="J", receipt_chain=receipt_chain)

    def test_5_char_rejected(self, receipt_chain: ReceiptChain) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            AuroreImageSourcing(coach_acronym="JPGRS", receipt_chain=receipt_chain)
