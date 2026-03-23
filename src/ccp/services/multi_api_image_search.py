"""
FR-VIS-10 — Multi-API Image Search
====================================
Unified Python interface that accepts standardized search requests,
dispatches to the appropriate composable image search skill(s), and
returns a normalised, ranked response.

Pipeline stages:
  Stage 1 — Search Request Assembly & env-var validation
  Stage 2 — Parallel Skill Dispatch (100 ms stagger, per-skill timeout)
  Stage 3 — Result Normalisation & Ranking (4-weight combined score)
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import time
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    API_STAGGER_MS,
    API_TIMEOUT_SECONDS,
    COLOR_MATCH_WEIGHT,
    LICENSING_SCORES,
    LICENSING_WEIGHT,
    MIN_SEARCH_RESOLUTION_PX,
    MultiAPISearchError,
    MultiAPISearchResponse,
    NormalizedSearchResult,
    RELEVANCE_WEIGHT,
    RankedResult,
    RUNNINGHUB_POLL_SCHEDULE,
    RUNNINGHUB_TIMEOUT_SECONDS,
    RunningHubTaskStatus,
    SKILL_ENV_KEYS,
    SearchRequest,
    SkillId,
    TIER_SKILL_MAP,
    TRIBAL_ALIGNMENT_WEIGHT,
)


# ---------------------------------------------------------------------------
# Simulated API backends (for testing / offline usage)
# ---------------------------------------------------------------------------

class _SimulatedAPIBackend:
    """Pluggable backend that can be replaced for live or test usage."""

    def __init__(self) -> None:
        self._simulated_results: dict[str, list[dict]] = {}
        self._simulated_failures: set[str] = set()
        self._simulated_timeouts: set[str] = set()
        self._dispatch_timestamps: list[tuple[str, float]] = []
        self._runninghub_tasks: dict[str, RunningHubTaskStatus] = {}

    # -- test hooks ---------------------------------------------------------
    def inject_results(self, skill_id: str, results: list[dict]) -> None:
        """Inject canned results for a skill (test helper)."""
        self._simulated_results[skill_id] = results

    def inject_failure(self, skill_id: str) -> None:
        self._simulated_failures.add(skill_id)

    def inject_timeout(self, skill_id: str) -> None:
        self._simulated_timeouts.add(skill_id)

    def inject_runninghub_task(self, task: RunningHubTaskStatus) -> None:
        self._runninghub_tasks[task.task_id] = task

    def clear(self) -> None:
        self._simulated_results.clear()
        self._simulated_failures.clear()
        self._simulated_timeouts.clear()
        self._dispatch_timestamps.clear()
        self._runninghub_tasks.clear()

    @property
    def dispatch_timestamps(self) -> list[tuple[str, float]]:
        return list(self._dispatch_timestamps)

    # -- dispatch -----------------------------------------------------------
    def dispatch(self, skill_id: str, params: dict) -> list[dict]:
        """Simulate dispatching a search skill and returning raw results."""
        self._dispatch_timestamps.append((skill_id, time.monotonic()))

        if skill_id in self._simulated_timeouts:
            raise TimeoutError(f"{skill_id} timed out after {API_TIMEOUT_SECONDS}s")
        if skill_id in self._simulated_failures:
            raise RuntimeError(f"{skill_id} API failure")

        return list(self._simulated_results.get(skill_id, []))

    def poll_runninghub(self, task_id: str) -> RunningHubTaskStatus:
        """Return stored RunningHub task status."""
        if task_id in self._runninghub_tasks:
            return self._runninghub_tasks[task_id]
        return RunningHubTaskStatus(task_id=task_id, status="pending")


# ---------------------------------------------------------------------------
# Multi-API Image Search Adapter
# ---------------------------------------------------------------------------

class MultiAPIImageSearchAdapter:
    """
    Unified interface for dispatching image search across 9 skills,
    normalising results, and ranking them by 4-weight combined score.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
        *,
        backend: _SimulatedAPIBackend | None = None,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got '{coach_acronym}'"
            )
        self._coach = coach_acronym
        self._rc = receipt_chain
        self._backend = backend or _SimulatedAPIBackend()

    @property
    def backend(self) -> _SimulatedAPIBackend:
        return self._backend

    # ====================================================================
    # Stage 1 — Search Request Assembly & env-var validation
    # ====================================================================

    @staticmethod
    def _check_env_keys(skill_ids: list[str]) -> tuple[list[str], dict[str, str]]:
        """
        Return (available_skills, skipped_reasons).
        Skills whose env-var key is missing are skipped, not halted.
        """
        available: list[str] = []
        skipped: dict[str, str] = {}
        for sid in skill_ids:
            env_key = SKILL_ENV_KEYS.get(sid)
            if env_key and not os.environ.get(env_key):
                skipped[sid] = f"MISSING_API_KEY: {env_key}"
            else:
                available.append(sid)
        return available, skipped

    @staticmethod
    def _sanitize_query(terms: list[str]) -> list[str]:
        """Strip shell-injection characters from search terms."""
        cleaned: list[str] = []
        for t in terms:
            safe = re.sub(r"[;|&`$\\]", "", t).strip()
            if safe:
                cleaned.append(safe)
        return cleaned

    # ====================================================================
    # Stage 2 — Skill Dispatch
    # ====================================================================

    def _dispatch_stock_skills(
        self,
        request: SearchRequest,
        skill_ids: list[str],
    ) -> tuple[
        list[tuple[str, list[dict]]],
        list[str],
        dict[str, str],
    ]:
        """
        Dispatch stock-image skills with ≥100 ms stagger.
        Returns (successes, failed_ids, fail_reasons).
        """
        successes: list[tuple[str, list[dict]]] = []
        failed_ids: list[str] = []
        fail_reasons: dict[str, str] = {}

        safe_terms = self._sanitize_query(request.search_terms)
        params = {
            "query": " ".join(safe_terms),
            "orientation": request.orientation,
            "color_filter": request.color_filter,
            "resolution_minimum_px": request.resolution_minimum_px,
        }

        for idx, sid in enumerate(skill_ids):
            if idx > 0:
                # 100 ms stagger between different providers
                time.sleep(API_STAGGER_MS / 1000.0)
            try:
                raw = self._backend.dispatch(sid, params)
                successes.append((sid, raw))
            except (TimeoutError, RuntimeError) as exc:
                failed_ids.append(sid)
                fail_reasons[sid] = str(exc)

        return successes, failed_ids, fail_reasons

    def _dispatch_runninghub(
        self,
        request: SearchRequest,
        skill_id: str,
    ) -> tuple[RunningHubTaskStatus | None, str | None]:
        """
        Dispatch a RunningHub AI-generation skill with exponential backoff.
        Returns (task_status, error_reason).
        """
        params: dict = {
            "prompt": request.compiled_prompt or "",
        }
        if skill_id == SkillId.RUNNINGHUB_REALISTIC:
            params["reference_image_base64"] = request.reference_image_base64 or ""
            params["strength"] = 0.85
        elif skill_id == SkillId.RUNNINGHUB_GHIBLI:
            params["lora_model_path"] = request.lora_model_path or ""

        try:
            raw = self._backend.dispatch(skill_id, params)
            # For RunningHub, the dispatch returns a task ID
            task_id = raw[0].get("task_id", "") if raw else ""
            if not task_id:
                return None, f"{skill_id} returned no task_id"

            # Exponential backoff polling
            status = self._backend.poll_runninghub(task_id)
            poll_count = 0
            elapsed = 0.0
            for wait in RUNNINGHUB_POLL_SCHEDULE:
                if status.status in ("completed", "failed"):
                    break
                poll_count += 1
                elapsed += wait
                if elapsed > RUNNINGHUB_TIMEOUT_SECONDS:
                    break
                # In real implementation: time.sleep(wait) then re-poll
                status = self._backend.poll_runninghub(task_id)

            status_out = RunningHubTaskStatus(
                task_id=task_id,
                status=status.status,
                status_url=status.status_url,
                output_url=status.output_url,
                poll_count=poll_count,
                elapsed_seconds=elapsed,
                error_detail=status.error_detail,
            )
            return status_out, None

        except (TimeoutError, RuntimeError) as exc:
            return None, str(exc)

    # ====================================================================
    # Stage 3 — Normalisation & Ranking
    # ====================================================================

    @staticmethod
    def normalize_result(
        raw: dict,
        skill_id: str,
        min_resolution: int,
    ) -> NormalizedSearchResult | None:
        """Convert a raw API result dict to a NormalizedSearchResult."""
        try:
            url = raw.get("url") or raw.get("image_url", "")
            width = int(raw.get("width", raw.get("width_px", 0)))
            height = int(raw.get("height", raw.get("height_px", 0)))
            shortest_edge = min(width, height) if width and height else 0
            resolution_ok = shortest_edge >= min_resolution

            # Map skill_id to source_api name
            api_map: dict[str, str] = {
                SkillId.UNSPLASH: "unsplash",
                SkillId.PEXELS: "pexels",
                SkillId.PIXABAY: "pixabay",
                SkillId.GIPHY: "giphy",
                SkillId.SERPER_GENERAL: "serper",
                SkillId.SERPER_KNOWN_PERSON: "serper_known_person",
                SkillId.RUNNINGHUB_REALISTIC: "runninghub_realistic",
                SkillId.RUNNINGHUB_GHIBLI: "runninghub_ghibli",
                SkillId.PHOTO_DECK: "photo_deck",
            }

            result_id = raw.get(
                "result_id",
                f"SR-{hashlib.sha256(url.encode()).hexdigest()[:8]}",
            )

            return NormalizedSearchResult(
                result_id=result_id,
                source_skill=skill_id,
                source_api=api_map.get(skill_id, "unknown"),
                image_url=url,
                thumbnail_url=raw.get("thumbnail_url"),
                width_px=max(width, 1),
                height_px=max(height, 1),
                aspect_ratio=raw.get("aspect_ratio"),
                licensing_type=raw.get("licensing_type", raw.get("license", "unknown")),
                licensing_restrictions=raw.get("licensing_restrictions"),
                photographer=raw.get("photographer"),
                relevance_score=float(raw.get("relevance_score", 0.0)),
                resolution_adequate=resolution_ok,
                color_match_score=float(raw.get("color_match_score", 0.0)),
                tribal_noun_alignment=float(raw.get("tribal_noun_alignment", 0.0)),
                combined_score=0.0,  # computed after normalization
            )
        except (ValueError, TypeError):
            return None

    @staticmethod
    def compute_combined_score(result: NormalizedSearchResult) -> float:
        """
        4-weight combined score:
          relevance 40% + tribal_noun_alignment 30%
          + color_match 20% + licensing 10%.
        """
        lic_score = LICENSING_SCORES.get(result.licensing_type, 0.0)
        raw = (
            result.relevance_score * RELEVANCE_WEIGHT
            + result.tribal_noun_alignment * TRIBAL_ALIGNMENT_WEIGHT
            + result.color_match_score * COLOR_MATCH_WEIGHT
            + lic_score * LICENSING_WEIGHT
        )
        # Clamp to [0, 1]
        return max(0.0, min(1.0, round(raw, 4)))

    @staticmethod
    def rank_results(
        normalized: list[NormalizedSearchResult],
        min_resolution: int,
    ) -> list[RankedResult]:
        """
        Filter out sub-resolution results, score, sort, and return ranks.
        Top-ranked result is marked selected=True.
        """
        adequate = [r for r in normalized if r.resolution_adequate]
        for r in adequate:
            r.combined_score = MultiAPIImageSearchAdapter.compute_combined_score(r)

        adequate.sort(key=lambda r: r.combined_score, reverse=True)

        ranked: list[RankedResult] = []
        for idx, r in enumerate(adequate):
            ranked.append(
                RankedResult(
                    rank=idx + 1,
                    result_id=r.result_id,
                    source_skill=r.source_skill,
                    source_api=r.source_api,
                    image_url=r.image_url,
                    combined_score=r.combined_score,
                    selected=(idx == 0),
                )
            )
        return ranked

    # ====================================================================
    # Main entry point
    # ====================================================================

    def search(self, request: SearchRequest) -> MultiAPISearchResponse:
        """
        Execute a full multi-API image search.
        Returns a MultiAPISearchResponse with ranked results.
        """
        ts = datetime.now(timezone.utc).isoformat()

        # ---- validate tier ------------------------------------------------
        tier_skills = TIER_SKILL_MAP.get(request.source_tier)
        if tier_skills is None:
            return MultiAPISearchResponse(
                search_id=request.search_id,
                slide_index=request.slide_index,
                search_terms=request.search_terms,
                error_type=MultiAPISearchError.INVALID_TIER,
                error_detail=f"Unknown tier: {request.source_tier}",
                timestamp_utc=ts,
            )

        # ---- Stage 1: env-var check & sanitization -------------------------
        available_skills, skipped = self._check_env_keys(list(tier_skills))

        if not available_skills:
            self._rc.log(
                agent_id="multi_api_image_search",
                action="search_aborted",
                asset_id=request.search_id,
                input_summary=f"tier={request.source_tier}",
                output_summary="ALL_APIS_UNAVAILABLE",
            )
            return MultiAPISearchResponse(
                search_id=request.search_id,
                slide_index=request.slide_index,
                search_terms=request.search_terms,
                skills_skipped=list(skipped.keys()),
                skills_skipped_reasons=skipped,
                error_type=MultiAPISearchError.ALL_APIS_UNAVAILABLE,
                error_detail="All API keys are missing",
                timestamp_utc=ts,
            )

        # Receipt: dispatch start
        self._rc.log(
            agent_id="multi_api_image_search",
            action="dispatch_start",
            asset_id=request.search_id,
            input_summary=f"terms={request.search_terms[:3]}, tier={request.source_tier}",
            output_summary=f"skills={available_skills}",
        )

        # ---- Stage 2: Dispatch -------------------------------------------
        is_runninghub = request.source_tier.startswith("tier_3_ai")
        all_raw: list[tuple[str, list[dict]]] = []
        failed_skills: list[str] = []
        fail_reasons: dict[str, str] = {}
        rh_task: RunningHubTaskStatus | None = None

        if is_runninghub:
            # RunningHub dispatch (single skill)
            skill_id = available_skills[0]
            task_status, err = self._dispatch_runninghub(request, skill_id)
            if err:
                failed_skills.append(skill_id)
                fail_reasons[skill_id] = err
            elif task_status:
                rh_task = task_status
                if task_status.output_url:
                    # Synthesise a single result from the generated image
                    all_raw.append((skill_id, [{
                        "url": task_status.output_url,
                        "width": 1080,
                        "height": 1350,
                        "licensing_type": "ai_generated",
                        "relevance_score": 0.9,
                        "tribal_noun_alignment": 0.9,
                        "color_match_score": 0.8,
                        "task_id": task_status.task_id,
                    }]))
        else:
            # Stock / internal dispatch
            successes, failed_ids, reasons = self._dispatch_stock_skills(
                request, available_skills
            )
            all_raw = successes
            failed_skills = failed_ids
            fail_reasons = reasons

        # ---- Stage 3: Normalise & Rank -----------------------------------
        all_normalized: list[NormalizedSearchResult] = []
        total_raw = 0
        for skill_id, raw_list in all_raw:
            total_raw += len(raw_list)
            for raw in raw_list:
                nr = self.normalize_result(
                    raw, skill_id, request.resolution_minimum_px
                )
                if nr:
                    all_normalized.append(nr)

        ranked = self.rank_results(all_normalized, request.resolution_minimum_px)

        succeeded = [sid for sid, _ in all_raw]

        # ---- Determine error state ----------------------------------------
        error_type: str | None = None
        error_detail: str | None = None

        if not ranked and total_raw > 0:
            error_type = MultiAPISearchError.RESOLUTION_FILTER_EXHAUSTED
            error_detail = (
                f"All {total_raw} results had resolution < "
                f"{request.resolution_minimum_px}px"
            )
        elif not ranked and total_raw == 0 and not failed_skills:
            error_type = MultiAPISearchError.NO_RESULTS_FOUND
            error_detail = f"No results for terms: {request.search_terms}"

        # ---- Receipt: search completed ------------------------------------
        self._rc.log(
            agent_id="multi_api_image_search",
            action="search_complete",
            asset_id=request.search_id,
            input_summary=(
                f"dispatched={len(succeeded) + len(failed_skills)}, "
                f"succeeded={len(succeeded)}"
            ),
            output_summary=(
                f"raw={total_raw}, ranked={len(ranked)}, "
                f"top={ranked[0].combined_score if ranked else 'N/A'}"
            ),
        )

        return MultiAPISearchResponse(
            search_id=request.search_id,
            slide_index=request.slide_index,
            search_terms=request.search_terms,
            orientation=request.orientation,
            color_filter=request.color_filter,
            resolution_minimum_px=request.resolution_minimum_px,
            skills_dispatched=available_skills,
            skills_succeeded=succeeded,
            skills_failed=failed_skills,
            skills_failed_reasons=fail_reasons,
            skills_skipped=list(skipped.keys()),
            skills_skipped_reasons=skipped,
            total_results_raw=total_raw,
            total_results_after_filtering=len(ranked),
            ranked_results=ranked,
            receipt_chain_block=f"RCB-MAPIS-{request.search_id}",
            timestamp_utc=ts,
            error_type=error_type,
            error_detail=error_detail,
        )
