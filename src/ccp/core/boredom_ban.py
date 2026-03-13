"""
CCP Boredom Ban Checker
Task 2.03 — Prevents thematic repetition over an 8-week rolling window.

Tracks published themes, angles, metaphors, and story structures.
New content is checked against the window before validation.
Matches trigger redirect instructions for the generator.

The window is per-coach, per-format — a metaphor used in a thread
CAN be used in a reel, but not in another thread within 8 weeks.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class ContentFingerprint(BaseModel):
    """Fingerprint of a published content piece for repetition detection."""

    asset_id: str
    format_type: str  # SCRP, THRD, CRSL, REEL, MEME, etc.
    published_date: datetime
    theme: str = Field(description="Primary theme or topic")
    angle: str = Field(description="Specific angle or argument")
    metaphors: list[str] = Field(default_factory=list, description="Key metaphors used")
    story_structure: str = Field(default="", description="Narrative arc type")
    hook_type: str = Field(default="", description="Opening hook classification")
    keywords: list[str] = Field(default_factory=list, description="Top 5 keywords")


class BoredomBanResult(BaseModel):
    """Result of a boredom ban check."""

    passed: bool
    conflicts: list[dict] = Field(default_factory=list)
    avoidance_instructions: list[str] = Field(default_factory=list)


class BoredomBan:
    """8-week rolling window repetition checker.

    Stores fingerprints of all published content and checks new
    proposed content against the window for thematic overlap.
    """

    WINDOW_WEEKS = 8
    SIMILARITY_THRESHOLD = 0.6  # 60% keyword/metaphor overlap = too similar

    def __init__(self, coach_acronym: str, data_dir: Optional[str] = None):
        self.coach_acronym = coach_acronym.upper()
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path(f"coaches/{self.coach_acronym}/intelligence/memory/episodic")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._window_file = self.data_dir / "boredom_ban_window.jsonl"

    def register(self, fingerprint: ContentFingerprint) -> None:
        """Register a published piece in the rolling window."""
        with open(self._window_file, "a", encoding="utf-8") as f:
            f.write(fingerprint.model_dump_json() + "\n")

    def check(
        self,
        proposed_theme: str,
        proposed_angle: str,
        proposed_metaphors: list[str],
        proposed_format: str,
        proposed_keywords: list[str],
        proposed_hook: str = "",
        proposed_structure: str = "",
    ) -> BoredomBanResult:
        """Check proposed content against the 8-week window.

        Args:
            proposed_theme: The theme of the proposed content
            proposed_angle: The specific angle
            proposed_metaphors: Key metaphors to be used
            proposed_format: Format type code (SCRP, THRD, etc.)
            proposed_keywords: Top keywords
            proposed_hook: Opening hook type
            proposed_structure: Narrative structure type

        Returns:
            BoredomBanResult with pass/fail and avoidance instructions
        """
        window = self._load_window()
        same_format = [fp for fp in window if fp.format_type == proposed_format]

        conflicts = []
        avoidance = []

        for fp in same_format:
            # Check theme similarity
            if self._normalize(proposed_theme) == self._normalize(fp.theme):
                conflicts.append({
                    "type": "theme_repeat",
                    "asset_id": fp.asset_id,
                    "published": fp.published_date.isoformat(),
                    "detail": f"Same theme '{fp.theme}' used in {fp.format_type}",
                })
                avoidance.append(f"AVOID theme: '{fp.theme}' (used {fp.published_date.strftime('%b %d')})")

            # Check angle similarity
            if self._normalize(proposed_angle) == self._normalize(fp.angle):
                conflicts.append({
                    "type": "angle_repeat",
                    "asset_id": fp.asset_id,
                    "published": fp.published_date.isoformat(),
                    "detail": f"Same angle '{fp.angle}'",
                })
                avoidance.append(f"AVOID angle: '{fp.angle}'")

            # Check metaphor overlap
            overlap = set(self._normalize_list(proposed_metaphors)) & set(
                self._normalize_list(fp.metaphors)
            )
            if overlap:
                conflicts.append({
                    "type": "metaphor_overlap",
                    "asset_id": fp.asset_id,
                    "overlapping": list(overlap),
                    "detail": f"Metaphors {overlap} already used",
                })
                for m in overlap:
                    avoidance.append(f"AVOID metaphor: '{m}'")

            # Check keyword overlap ratio
            kw_overlap = set(self._normalize_list(proposed_keywords)) & set(
                self._normalize_list(fp.keywords)
            )
            if len(proposed_keywords) > 0:
                overlap_ratio = len(kw_overlap) / len(proposed_keywords)
                if overlap_ratio >= self.SIMILARITY_THRESHOLD:
                    conflicts.append({
                        "type": "keyword_saturation",
                        "asset_id": fp.asset_id,
                        "overlap_ratio": round(overlap_ratio, 2),
                        "overlapping": list(kw_overlap),
                    })
                    avoidance.append(
                        f"AVOID keywords: {list(kw_overlap)} ({overlap_ratio:.0%} overlap with {fp.asset_id})"
                    )

            # Check hook type repetition (same hook in 3+ recent pieces)
            if proposed_hook and proposed_hook == fp.hook_type:
                hook_count = sum(
                    1 for x in same_format[-10:] if x.hook_type == proposed_hook
                )
                if hook_count >= 3:
                    conflicts.append({
                        "type": "hook_fatigue",
                        "hook_type": proposed_hook,
                        "count": hook_count,
                    })
                    avoidance.append(
                        f"AVOID hook type '{proposed_hook}' (used {hook_count}x in last 10 pieces)"
                    )

        passed = len(conflicts) == 0
        return BoredomBanResult(
            passed=passed,
            conflicts=conflicts,
            avoidance_instructions=list(set(avoidance)),
        )

    def get_window_summary(self, format_type: Optional[str] = None) -> dict:
        """Get a summary of the current 8-week window for planning."""
        window = self._load_window()
        if format_type:
            window = [fp for fp in window if fp.format_type == format_type]

        themes = [fp.theme for fp in window]
        all_metaphors = [m for fp in window for m in fp.metaphors]
        all_keywords = [k for fp in window for k in fp.keywords]

        return {
            "window_size": len(window),
            "unique_themes": list(set(themes)),
            "theme_count": len(set(themes)),
            "used_metaphors": list(set(all_metaphors)),
            "top_keywords": list(set(all_keywords)),
            "format_filter": format_type,
        }

    def _load_window(self) -> list[ContentFingerprint]:
        """Load fingerprints from the last 8 weeks."""
        cutoff = datetime.now(timezone.utc) - timedelta(weeks=self.WINDOW_WEEKS)
        entries = []

        if not self._window_file.exists():
            return entries

        with open(self._window_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fp = ContentFingerprint.model_validate_json(line)
                if fp.published_date.replace(tzinfo=timezone.utc) >= cutoff:
                    entries.append(fp)

        return entries

    @staticmethod
    def _normalize(text: str) -> str:
        return text.strip().lower()

    @staticmethod
    def _normalize_list(items: list[str]) -> list[str]:
        return [i.strip().lower() for i in items]
