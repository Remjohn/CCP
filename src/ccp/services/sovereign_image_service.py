"""
FR50 — Sovereign Image Rule Service (DEP-ENG-044)
NO AI-generated coach faces — ever.

AC1: Metadata intersection (mood + format → Photo Deck query).
AC2: Rotation enforcement (Usage_Count ASC).
AC3: Sovereign guard — blocks prompts containing coach name/headshot/portrait.
AC4: Clean fallback null when no match found.
"""

from __future__ import annotations

import re
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    SelectedPhoto,
    SovereignImageQuery,
    SovereignImageResolution,
    SovereignImageResult,
)


# ── Sovereign Guard Patterns ──────────────────────────
# FR50 §4.3: blocks prompts with coach identity cues
SOVEREIGN_VIOLATION_PATTERNS: list[str] = [
    "coach photo",
    "coach face",
    "coach headshot",
    "coach portrait",
    "headshot",
    "portrait",
    "coach selfie",
    "my face",
    "my photo",
    "generate coach",
    "ai coach image",
    "coach likeness",
]

_SOVEREIGN_REGEX = re.compile(
    "|".join(re.escape(p) for p in SOVEREIGN_VIOLATION_PATTERNS),
    re.IGNORECASE,
)


class SovereignViolationException(Exception):
    """FR50 AC3: Raised when a prompt attempts to generate coach imagery."""
    pass


class SovereignImageService:
    """
    FR50: Sovereign Image Rule — photo retrieval with rotation.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        # In-memory Photo Deck (production: Notion DB)
        self._photo_deck: list[dict] = []

    # ── Photo Deck Management ──────────────────────────

    def register_photo(
        self,
        *,
        notion_page_id: str,
        temporary_s3_url: str,
        mood: str,
        format_tag: str,
        usage_count: int = 0,
    ) -> None:
        """Register a photo in the local Photo Deck."""
        self._photo_deck.append({
            "notion_page_id": notion_page_id,
            "temporary_s3_url": temporary_s3_url,
            "mood": mood.lower(),
            "format_tag": format_tag.lower(),
            "usage_count": usage_count,
        })

    # ── AC3: Sovereign Guard ───────────────────────────

    def check_sovereign_violation(self, prompt_text: str) -> bool:
        """
        FR50 AC3: Check if a prompt violates the sovereign image rule.
        Returns True if violation detected.
        """
        return bool(_SOVEREIGN_REGEX.search(prompt_text))

    def enforce_sovereign_guard(self, prompt_text: str) -> None:
        """
        FR50 AC3: Raise SovereignViolationException on violation.
        """
        if self.check_sovereign_violation(prompt_text):
            self._receipt_chain.log(
                agent_id="SovereignImageService",
                action="SOVEREIGN_VIOLATION_BLOCKED",
                asset_id=f"GUARD-{self._coach}",
                decision="VIOLATION",
                decision_rationale=f"prompt_snippet={prompt_text[:100]}",
            )
            raise SovereignViolationException(
                f"Sovereign Image Rule violated: prompt contains prohibited coach imagery terms"
            )

    # ── AC1: Metadata Intersection Query ───────────────

    def query_photo_deck(
        self,
        query: SovereignImageQuery,
    ) -> SovereignImageResult:
        """
        FR50 AC1/AC2/AC4: Query Photo Deck with mood + format intersection.
        Sort by Usage_Count ASC for rotation enforcement.
        """
        target_mood = query.target_mood.lower()
        target_format = query.target_format.lower()

        # Filter by mood and format
        matches = [
            p for p in self._photo_deck
            if p["mood"] == target_mood and p["format_tag"] == target_format
        ]

        if not matches:
            # AC4: Clean fallback null
            self._receipt_chain.log(
                agent_id="SovereignImageService",
                action="PHOTO_QUERY_NO_MATCH",
                asset_id=f"QUERY-{self._coach}",
                decision="NO_MATCH",
                decision_rationale=f"mood={target_mood}, format={target_format}",
            )
            return SovereignImageResult(
                asset_id=f"SOVEREIGN-{self._coach}",
                resolution_status=SovereignImageResolution.NO_MATCH,
                search_parameters=query,
            )

        # AC2: Sort by usage_count ASC (rotation enforcement)
        matches.sort(key=lambda x: x["usage_count"])
        selected = matches[0]

        # Increment usage count
        selected["usage_count"] += 1

        photo = SelectedPhoto(
            notion_page_id=selected["notion_page_id"],
            temporary_s3_url=selected["temporary_s3_url"],
            usage_count_updated_to=selected["usage_count"],
        )

        self._receipt_chain.log(
            agent_id="SovereignImageService",
            action="PHOTO_SELECTED",
            asset_id=f"SOVEREIGN-{self._coach}",
            decision="SUCCESS",
            decision_rationale=f"page_id={selected['notion_page_id']}, usage={selected['usage_count']}",
        )

        return SovereignImageResult(
            asset_id=f"SOVEREIGN-{self._coach}",
            resolution_status=SovereignImageResolution.SUCCESS,
            search_parameters=query,
            selected_photo=photo,
        )
