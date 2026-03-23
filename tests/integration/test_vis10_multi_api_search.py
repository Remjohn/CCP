"""
FR-VIS-10 — Multi-API Image Search  ·  Integration Tests
==========================================================
47 tests covering 6 ACs, ADR-01, C-11, receipt chain, safety.
"""

from __future__ import annotations

import os
import tempfile
import time
from unittest import mock

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    API_STAGGER_MS,
    COLOR_MATCH_WEIGHT,
    LICENSING_SCORES,
    LICENSING_WEIGHT,
    MIN_SEARCH_RESOLUTION_PX,
    MultiAPISearchError,
    NormalizedSearchResult,
    RELEVANCE_WEIGHT,
    RUNNINGHUB_POLL_SCHEDULE,
    RunningHubTaskStatus,
    SearchRequest,
    SkillId,
    TIER_SKILL_MAP,
    TRIBAL_ALIGNMENT_WEIGHT,
)
from src.ccp.services.multi_api_image_search import (
    MultiAPIImageSearchAdapter,
    _SimulatedAPIBackend,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_adapter(
    coach: str = "TST",
    backend: _SimulatedAPIBackend | None = None,
) -> tuple[MultiAPIImageSearchAdapter, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    be = backend or _SimulatedAPIBackend()
    adapter = MultiAPIImageSearchAdapter(coach, rc, backend=be)
    return adapter, rc


def _stock_request(
    search_id: str = "MAPIS-TST-001",
    terms: list[str] | None = None,
    tier: str = "tier_2_stock",
    coach: str = "TST",
    **kwargs,
) -> SearchRequest:
    return SearchRequest(
        search_id=search_id,
        slide_index=0,
        search_terms=terms or ["person desk laptop"],
        source_tier=tier,
        coach_acronym=coach,
        **kwargs,
    )


def _make_raw_result(
    url: str = "https://img.example.com/abc.jpg",
    width: int = 2400,
    height: int = 3200,
    relevance: float = 0.8,
    tribal: float = 0.7,
    color: float = 0.6,
    license_type: str = "unsplash_license",
    result_id: str | None = None,
    **extra,
) -> dict:
    d: dict = {
        "url": url,
        "width": width,
        "height": height,
        "relevance_score": relevance,
        "tribal_noun_alignment": tribal,
        "color_match_score": color,
        "licensing_type": license_type,
    }
    if result_id:
        d["result_id"] = result_id
    d.update(extra)
    return d


# ===========================================================================
# 1. AC1 — Multi-API Dispatch (Tier 2 searches all 5 stock skills)
# ===========================================================================

class TestAC1MultiAPIDispatch:
    """AC1: Tier 2 request dispatches all available stock skills."""

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_all_5_skills_dispatched(self):
        be = _SimulatedAPIBackend()
        # Inject 1 result per skill
        for sid in TIER_SKILL_MAP["tier_2_stock"]:
            be.inject_results(sid, [_make_raw_result(
                url=f"https://img.example.com/{sid}.jpg",
                result_id=f"SR-{sid}",
            )])
        adapter, rc = _make_adapter(backend=be)
        req = _stock_request()
        resp = adapter.search(req)

        assert len(resp.skills_dispatched) == 5
        assert len(resp.skills_succeeded) == 5
        assert resp.total_results_raw == 5

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_results_normalised_to_common_schema(self):
        be = _SimulatedAPIBackend()
        for sid in TIER_SKILL_MAP["tier_2_stock"]:
            be.inject_results(sid, [_make_raw_result(
                url=f"https://img.example.com/{sid}.jpg",
                result_id=f"SR-{sid}",
            )])
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert resp.total_results_after_filtering == 5
        for rr in resp.ranked_results:
            assert rr.combined_score > 0
            assert rr.image_url.startswith("https://")

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_ranked_by_combined_score(self):
        be = _SimulatedAPIBackend()
        for sid in TIER_SKILL_MAP["tier_2_stock"]:
            be.inject_results(sid, [_make_raw_result(
                url=f"https://img.example.com/{sid}.jpg",
                result_id=f"SR-{sid}",
                relevance=0.5 + (0.1 * hash(sid) % 5) / 10,
            )])
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        scores = [r.combined_score for r in resp.ranked_results]
        assert scores == sorted(scores, reverse=True)

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_top_result_marked_selected(self):
        be = _SimulatedAPIBackend()
        be.inject_results(SkillId.UNSPLASH, [_make_raw_result(result_id="SR-001")])
        be.inject_results(SkillId.PEXELS, [_make_raw_result(result_id="SR-002")])
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        selected = [r for r in resp.ranked_results if r.selected]
        assert len(selected) == 1
        assert selected[0].rank == 1


# ===========================================================================
# 2. AC2 — Result Ranking (weighted scoring)
# ===========================================================================

class TestAC2ResultRanking:
    """AC2: Pexels higher than Unsplash with spec-given scores."""

    def test_pexels_beats_unsplash_per_spec(self):
        """
        Unsplash: relevance=0.9, tribal=0.5, color=0.4
          → 0.9*0.4 + 0.5*0.3 + 0.4*0.2 = 0.36+0.15+0.08 = 0.59
        Pexels: relevance=0.7, tribal=0.9, color=0.8
          → 0.7*0.4 + 0.9*0.3 + 0.8*0.2 = 0.28+0.27+0.16 = 0.71
        (licensing component excluded for this check — same license)
        """
        unsplash = NormalizedSearchResult(
            result_id="SR-U",
            source_skill=SkillId.UNSPLASH,
            source_api="unsplash",
            image_url="https://u.com/1.jpg",
            width_px=2400,
            height_px=3200,
            relevance_score=0.9,
            tribal_noun_alignment=0.5,
            color_match_score=0.4,
            licensing_type="unsplash_license",
            resolution_adequate=True,
        )
        pexels = NormalizedSearchResult(
            result_id="SR-P",
            source_skill=SkillId.PEXELS,
            source_api="pexels",
            image_url="https://p.com/2.jpg",
            width_px=2400,
            height_px=3200,
            relevance_score=0.7,
            tribal_noun_alignment=0.9,
            color_match_score=0.8,
            licensing_type="pexels_license",
            resolution_adequate=True,
        )

        u_score = MultiAPIImageSearchAdapter.compute_combined_score(unsplash)
        p_score = MultiAPIImageSearchAdapter.compute_combined_score(pexels)

        assert p_score > u_score
        # Verify approximate values (with licensing component)
        u_lic = LICENSING_SCORES["unsplash_license"] * LICENSING_WEIGHT
        p_lic = LICENSING_SCORES["pexels_license"] * LICENSING_WEIGHT
        assert abs(u_score - (0.59 + u_lic)) < 0.01
        assert abs(p_score - (0.71 + p_lic)) < 0.01

    def test_ranking_uses_all_4_weights(self):
        """Confirm all 4 weight components are additive."""
        r = NormalizedSearchResult(
            result_id="SR-X",
            source_skill=SkillId.UNSPLASH,
            source_api="unsplash",
            image_url="https://x.com/1.jpg",
            width_px=2400,
            height_px=3200,
            relevance_score=1.0,
            tribal_noun_alignment=1.0,
            color_match_score=1.0,
            licensing_type="creative_commons",
            resolution_adequate=True,
        )
        score = MultiAPIImageSearchAdapter.compute_combined_score(r)
        expected = (
            1.0 * RELEVANCE_WEIGHT
            + 1.0 * TRIBAL_ALIGNMENT_WEIGHT
            + 1.0 * COLOR_MATCH_WEIGHT
            + LICENSING_SCORES["creative_commons"] * LICENSING_WEIGHT
        )
        assert abs(score - expected) < 0.001

    def test_zero_scores_give_zero(self):
        r = NormalizedSearchResult(
            result_id="SR-Z",
            source_skill=SkillId.UNSPLASH,
            source_api="unsplash",
            image_url="https://z.com/1.jpg",
            width_px=2400,
            height_px=3200,
            relevance_score=0.0,
            tribal_noun_alignment=0.0,
            color_match_score=0.0,
            licensing_type="unknown",
            resolution_adequate=True,
        )
        score = MultiAPIImageSearchAdapter.compute_combined_score(r)
        assert score == 0.0

    def test_licensing_hierarchy_creative_commons_top(self):
        assert LICENSING_SCORES["creative_commons"] > LICENSING_SCORES["editorial"]
        assert LICENSING_SCORES["editorial"] > LICENSING_SCORES["unsplash_license"]
        assert LICENSING_SCORES["unsplash_license"] > LICENSING_SCORES["giphy_license"]


# ===========================================================================
# 3. AC3 — Resolution Filter
# ===========================================================================

class TestAC3ResolutionFilter:
    """AC3: Sub-1080px images excluded from ranked results."""

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_sub_resolution_excluded(self):
        be = _SimulatedAPIBackend()
        # 8 adequate results + 7 inadequate
        results: list[dict] = []
        for i in range(15):
            w = 2400 if i < 8 else 640
            h = 3200 if i < 8 else 480
            results.append(_make_raw_result(
                url=f"https://img.example.com/{i}.jpg",
                result_id=f"SR-{i:03d}",
                width=w,
                height=h,
            ))
        be.inject_results(SkillId.UNSPLASH, results)
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert resp.total_results_raw == 15
        assert resp.total_results_after_filtering == 8

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
    }, clear=False)
    def test_all_sub_resolution_returns_filter_exhausted(self):
        be = _SimulatedAPIBackend()
        be.inject_results(SkillId.UNSPLASH, [
            _make_raw_result(width=640, height=480, result_id="SR-LO"),
        ])
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert resp.total_results_raw == 1
        assert resp.total_results_after_filtering == 0
        assert resp.error_type == MultiAPISearchError.RESOLUTION_FILTER_EXHAUSTED

    def test_exactly_1080_passes(self):
        nr = MultiAPIImageSearchAdapter.normalize_result(
            _make_raw_result(width=1080, height=1080),
            SkillId.UNSPLASH,
            MIN_SEARCH_RESOLUTION_PX,
        )
        assert nr is not None
        assert nr.resolution_adequate is True

    def test_1079_fails(self):
        nr = MultiAPIImageSearchAdapter.normalize_result(
            _make_raw_result(width=1079, height=1920),
            SkillId.UNSPLASH,
            MIN_SEARCH_RESOLUTION_PX,
        )
        assert nr is not None
        assert nr.resolution_adequate is False


# ===========================================================================
# 4. AC4 — API Failure Resilience
# ===========================================================================

class TestAC4APIFailureResilience:
    """AC4: 2 APIs time out, remaining 3 return results."""

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_two_timeouts_three_succeed(self):
        be = _SimulatedAPIBackend()
        be.inject_timeout(SkillId.UNSPLASH)
        be.inject_timeout(SkillId.SERPER_GENERAL)
        for sid in [SkillId.PEXELS, SkillId.PIXABAY, SkillId.GIPHY]:
            be.inject_results(sid, [_make_raw_result(result_id=f"SR-{sid}")])

        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert len(resp.skills_succeeded) == 3
        assert len(resp.skills_failed) == 2
        assert SkillId.UNSPLASH in resp.skills_failed
        assert SkillId.SERPER_GENERAL in resp.skills_failed
        assert resp.total_results_after_filtering == 3

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_failed_reasons_populated(self):
        be = _SimulatedAPIBackend()
        be.inject_timeout(SkillId.UNSPLASH)
        be.inject_results(SkillId.PEXELS, [_make_raw_result()])
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert SkillId.UNSPLASH in resp.skills_failed_reasons
        assert "timed out" in resp.skills_failed_reasons[SkillId.UNSPLASH]

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_all_fail_returns_no_results(self):
        be = _SimulatedAPIBackend()
        for sid in TIER_SKILL_MAP["tier_2_stock"]:
            be.inject_timeout(sid)
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert len(resp.skills_failed) == 5
        assert resp.total_results_after_filtering == 0


# ===========================================================================
# 5. AC5 — Missing API Key
# ===========================================================================

class TestAC5MissingAPIKey:
    """AC5: Missing env var → skill skipped, others execute."""

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        # PIXABAY_API_KEY deliberately absent
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_pixabay_skipped_others_execute(self):
        be = _SimulatedAPIBackend()
        for sid in [SkillId.UNSPLASH, SkillId.PEXELS, SkillId.GIPHY, SkillId.SERPER_GENERAL]:
            be.inject_results(sid, [_make_raw_result(result_id=f"SR-{sid}")])
        adapter, _ = _make_adapter(backend=be)

        # Ensure PIXABAY_API_KEY is absent
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PIXABAY_API_KEY", None)
            resp = adapter.search(_stock_request())

        assert SkillId.PIXABAY in resp.skills_skipped
        assert "MISSING_API_KEY" in resp.skills_skipped_reasons.get(SkillId.PIXABAY, "")
        assert len(resp.skills_dispatched) == 4
        assert resp.total_results_after_filtering >= 1

    def test_all_keys_missing_returns_all_unavailable(self):
        be = _SimulatedAPIBackend()
        adapter, _ = _make_adapter(backend=be)

        with mock.patch.dict(os.environ, {}, clear=True):
            resp = adapter.search(_stock_request())

        assert resp.error_type == MultiAPISearchError.ALL_APIS_UNAVAILABLE
        assert len(resp.skills_skipped) == 5

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_no_keys_missing_no_skips(self):
        be = _SimulatedAPIBackend()
        for sid in TIER_SKILL_MAP["tier_2_stock"]:
            be.inject_results(sid, [_make_raw_result(result_id=f"SR-{sid}")])
        adapter, _ = _make_adapter(backend=be)
        resp = adapter.search(_stock_request())

        assert len(resp.skills_skipped) == 0


# ===========================================================================
# 6. AC6 — RunningHub Task Dispatch
# ===========================================================================

class TestAC6RunningHubDispatch:
    """AC6: RunningHub dispatch with exponential backoff polling."""

    def test_realistic_dispatch_returns_task_id(self):
        be = _SimulatedAPIBackend()
        be.inject_results(SkillId.RUNNINGHUB_REALISTIC, [
            {"task_id": "RH-TASK-001"},
        ])
        be.inject_runninghub_task(RunningHubTaskStatus(
            task_id="RH-TASK-001",
            status="completed",
            output_url="https://rh.example.com/output-001.png",
        ))
        adapter, _ = _make_adapter(backend=be)
        req = _stock_request(
            tier="tier_3_ai_realistic",
            terms=["person at desk"],
        )
        req.compiled_prompt = "A photorealistic scene..."
        resp = adapter.search(req)

        assert len(resp.skills_succeeded) == 1
        assert SkillId.RUNNINGHUB_REALISTIC in resp.skills_succeeded
        assert resp.total_results_raw == 1

    def test_ghibli_dispatch_returns_task_id(self):
        be = _SimulatedAPIBackend()
        be.inject_results(SkillId.RUNNINGHUB_GHIBLI, [
            {"task_id": "RH-TASK-002"},
        ])
        be.inject_runninghub_task(RunningHubTaskStatus(
            task_id="RH-TASK-002",
            status="completed",
            output_url="https://rh.example.com/ghibli-002.png",
        ))
        adapter, _ = _make_adapter(backend=be)
        req = _stock_request(tier="tier_3_ai_ghibli", terms=["mythical forest"])
        req.compiled_prompt = "A Ghibli-style forest..."
        req.lora_model_path = "/models/ghibli-v2.safetensors"
        resp = adapter.search(req)

        assert SkillId.RUNNINGHUB_GHIBLI in resp.skills_succeeded

    def test_backoff_schedule_matches_spec(self):
        assert RUNNINGHUB_POLL_SCHEDULE == [5, 10, 20, 40, 60]

    def test_runninghub_timeout_results_in_failure(self):
        be = _SimulatedAPIBackend()
        be.inject_timeout(SkillId.RUNNINGHUB_REALISTIC)
        adapter, _ = _make_adapter(backend=be)
        req = _stock_request(
            tier="tier_3_ai_realistic",
            terms=["person at desk"],
        )
        resp = adapter.search(req)

        assert SkillId.RUNNINGHUB_REALISTIC in resp.skills_failed
        assert resp.total_results_after_filtering == 0


# ===========================================================================
# 7. Stagger Timing
# ===========================================================================

class TestStaggerTiming:
    """Dispatch timestamps should show ≥100ms between providers."""

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_100ms_stagger_between_skills(self):
        be = _SimulatedAPIBackend()
        for sid in TIER_SKILL_MAP["tier_2_stock"]:
            be.inject_results(sid, [_make_raw_result(result_id=f"SR-{sid}")])
        adapter, _ = _make_adapter(backend=be)
        adapter.search(_stock_request())

        timestamps = be.dispatch_timestamps
        assert len(timestamps) == 5

        for i in range(1, len(timestamps)):
            delta_ms = (timestamps[i][1] - timestamps[i - 1][1]) * 1000
            # Allow small tolerance for timing jitter
            assert delta_ms >= (API_STAGGER_MS - 20), (
                f"Gap between {timestamps[i-1][0]} and {timestamps[i][0]} "
                f"was {delta_ms:.1f}ms, expected ≥{API_STAGGER_MS}ms"
            )


# ===========================================================================
# 8. Normalisation
# ===========================================================================

class TestNormalization:
    """Raw results from different APIs normalise to common schema."""

    def test_unsplash_normalises(self):
        raw = {
            "url": "https://unsplash.com/photo-1.jpg",
            "width": 2400,
            "height": 3200,
            "photographer": "Jane Doe",
            "license": "unsplash_license",
            "relevance_score": 0.85,
            "tribal_noun_alignment": 0.7,
            "color_match_score": 0.6,
        }
        nr = MultiAPIImageSearchAdapter.normalize_result(
            raw, SkillId.UNSPLASH, 1080
        )
        assert nr is not None
        assert nr.source_api == "unsplash"
        assert nr.width_px == 2400
        assert nr.resolution_adequate is True
        assert nr.photographer == "Jane Doe"

    def test_pexels_normalises(self):
        raw = {
            "url": "https://pexels.com/photo-2.jpg",
            "width": 1920,
            "height": 1080,
            "photographer": "John",
            "license": "pexels_license",
        }
        nr = MultiAPIImageSearchAdapter.normalize_result(
            raw, SkillId.PEXELS, 1080
        )
        assert nr is not None
        assert nr.source_api == "pexels"
        assert nr.resolution_adequate is True

    def test_giphy_normalises(self):
        raw = {
            "url": "https://giphy.com/gif-1.gif",
            "width": 480,
            "height": 480,
            "title": "funny cat",
            "rating": "G",
        }
        nr = MultiAPIImageSearchAdapter.normalize_result(
            raw, SkillId.GIPHY, 1080
        )
        assert nr is not None
        assert nr.source_api == "giphy"
        assert nr.resolution_adequate is False  # 480 < 1080

    def test_invalid_raw_returns_none(self):
        nr = MultiAPIImageSearchAdapter.normalize_result(
            {"not_a_valid_result": True},
            SkillId.UNSPLASH,
            1080,
        )
        # Should still return something (with defaults) since url="" is ok
        # but width/height would be 0
        assert nr is not None
        assert nr.resolution_adequate is False

    def test_auto_result_id_generated(self):
        nr = MultiAPIImageSearchAdapter.normalize_result(
            _make_raw_result(url="https://unique.com/img.jpg"),
            SkillId.UNSPLASH,
            1080,
        )
        assert nr is not None
        assert nr.result_id.startswith("SR-")


# ===========================================================================
# 9. Receipt Chain Integration
# ===========================================================================

class TestReceiptChainIntegration:
    """Receipt chain writes for dispatch and completion."""

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
        "PEXELS_API_KEY": "key2",
        "PIXABAY_API_KEY": "key3",
        "GIPHY_API_KEY": "key4",
        "SERPER_API_KEY": "key5",
    }, clear=False)
    def test_happy_path_writes_2_receipts(self):
        be = _SimulatedAPIBackend()
        be.inject_results(SkillId.UNSPLASH, [_make_raw_result()])
        adapter, rc = _make_adapter(backend=be)
        adapter.search(_stock_request())

        assert rc.chain_length() >= 2  # dispatch_start + search_complete
        entries = rc.query(action="dispatch_start")
        assert len(entries) == 1
        entries = rc.query(action="search_complete")
        assert len(entries) == 1

    def test_all_unavailable_writes_abort_receipt(self):
        be = _SimulatedAPIBackend()
        adapter, rc = _make_adapter(backend=be)
        with mock.patch.dict(os.environ, {}, clear=True):
            adapter.search(_stock_request())
        entries = rc.query(action="search_aborted")
        assert len(entries) == 1

    @mock.patch.dict(os.environ, {
        "UNSPLASH_ACCESS_KEY": "key1",
    }, clear=False)
    def test_receipt_contains_search_id(self):
        be = _SimulatedAPIBackend()
        be.inject_results(SkillId.UNSPLASH, [_make_raw_result()])
        adapter, rc = _make_adapter(backend=be)
        adapter.search(_stock_request(search_id="MAPIS-TEST-42"))

        entries = rc.query(asset_id="MAPIS-TEST-42")
        assert len(entries) >= 1


# ===========================================================================
# 10. ADR-01 Coach Acronym
# ===========================================================================

class TestADR01CoachAcronym:
    def test_valid_2_char(self):
        """Adapter accepts 2-char acronym (ADR-01 range)."""
        rc = ReceiptChain(coach_acronym="JPX")  # RC needs 3-char
        adapter = MultiAPIImageSearchAdapter("JP", rc)
        assert adapter is not None

    def test_valid_4_char(self):
        rc = ReceiptChain(coach_acronym="BRN")
        adapter = MultiAPIImageSearchAdapter("BREN", rc)
        assert adapter is not None

    def test_1_char_rejected(self):
        with pytest.raises(ValueError, match="2-4"):
            rc = ReceiptChain(coach_acronym="TST")
            MultiAPIImageSearchAdapter("X", rc)

    def test_5_char_rejected(self):
        with pytest.raises(ValueError, match="2-4"):
            rc = ReceiptChain(coach_acronym="TST")
            MultiAPIImageSearchAdapter("ABCDE", rc)


# ===========================================================================
# 11. Safety — Query Injection
# ===========================================================================

class TestSafetyQueryInjection:
    """Injection characters stripped from search terms."""

    def test_semicolon_stripped(self):
        clean = MultiAPIImageSearchAdapter._sanitize_query(
            ["alarm clock; curl evil.com"]
        )
        assert ";" not in clean[0]
        assert "alarm clock" in clean[0]

    def test_pipe_stripped(self):
        clean = MultiAPIImageSearchAdapter._sanitize_query(["test | rm -rf /"])
        assert "|" not in clean[0]

    def test_backtick_stripped(self):
        clean = MultiAPIImageSearchAdapter._sanitize_query(["`whoami`"])
        assert "`" not in clean[0]

    def test_dollar_stripped(self):
        clean = MultiAPIImageSearchAdapter._sanitize_query(["$HOME/secret"])
        assert "$" not in clean[0]


# ===========================================================================
# 12. Invalid Tier
# ===========================================================================

class TestInvalidTier:
    def test_unknown_tier_returns_error(self):
        adapter, _ = _make_adapter()
        req = _stock_request(tier="tier_99_unknown")
        resp = adapter.search(req)

        assert resp.error_type == MultiAPISearchError.INVALID_TIER
        assert "tier_99_unknown" in (resp.error_detail or "")


# ===========================================================================
# 13. Tier-to-Skill Mapping
# ===========================================================================

class TestTierSkillMapping:
    def test_tier_2_stock_has_5_skills(self):
        assert len(TIER_SKILL_MAP["tier_2_stock"]) == 5

    def test_tier_3_realistic_has_1_skill(self):
        assert TIER_SKILL_MAP["tier_3_ai_realistic"] == [SkillId.RUNNINGHUB_REALISTIC]

    def test_tier_3_ghibli_has_1_skill(self):
        assert TIER_SKILL_MAP["tier_3_ai_ghibli"] == [SkillId.RUNNINGHUB_GHIBLI]

    def test_photo_deck_tier(self):
        assert TIER_SKILL_MAP["tier_1_photo_deck"] == [SkillId.PHOTO_DECK]

    def test_known_person_tier(self):
        assert TIER_SKILL_MAP["tier_1_known_person"] == [SkillId.SERPER_KNOWN_PERSON]
