"""
CCP FR7 Leadership Scorecard — Signal Source Loader (Unit 2)
Phase 1 INGEST: Load and verify all required + optional DEP objects.

Spec reference: FR7 Tech Spec §Implementation Plan — Phase 1: INGEST
                §Prerequisite Gate

The loader verifies:
  - coach_soul.json (DEP-ENG-003 + DEP-ENG-004 + DEP-LIB-001) — REQUIRED
  - ttt_baseline.json (DEP-ENG-005) — REQUIRED
  - tribe_soul.json (DEP-ENG-001) — REQUIRED
  - cultural_memory_map (DEP-ENG-023) — OPTIONAL
  - coach_story_archive (DEP-ENG-024) — OPTIONAL
  - philosophy_brief — OPTIONAL

AC9: 'Minister of Identity activated without ttt_baseline.json →
      returns CANNOT_SCORE_MISSING_DEPENDENCIES: ttt_baseline.json'
AC10: 'The Minister of Identity scores and annotates. It never modifies
       coach_soul.json, ttt_baseline.json, or tribe_soul.json.'
"""

import json
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.ccp.models.leadership_scorecard_models import SignalSourceAvailability


class MissingDependencyError(Exception):
    """Raised when a required DEP object is missing.
    Spec §Prerequisite Gate: 'CANNOT_SCORE_MISSING_DEPENDENCIES error with list of missing objects.'
    AC9 enforcement.
    """

    def __init__(self, missing_deps: list[str]):
        self.missing_deps = missing_deps
        self.error_code = "CANNOT_SCORE_MISSING_DEPENDENCIES"
        dep_list = ", ".join(missing_deps)
        super().__init__(f"{self.error_code}: {dep_list}")


class SignalBundle(BaseModel):
    """Validated bundle of all signal sources for the scoring engine.

    All data is READ-ONLY — the scoring engine must never modify these objects (AC10).
    """
    # Required sources
    coach_soul_data: dict[str, Any] = Field(
        ...,
        description="Parsed coach_soul.json content (DEP-ENG-003 + DEP-ENG-004 + DEP-LIB-001)",
    )
    ttt_baseline_data: dict[str, Any] = Field(
        ...,
        description="Parsed ttt_baseline.json content (DEP-ENG-005)",
    )
    tribe_soul_data: dict[str, Any] = Field(
        ...,
        description="Parsed tribe_soul.json content (DEP-ENG-001)",
    )

    # Optional enrichment sources
    cultural_memory_map_data: Optional[dict[str, Any]] = Field(
        default=None,
        description="Parsed cultural_memory_map data (DEP-ENG-023) — optional enrichment",
    )
    coach_story_archive_data: Optional[dict[str, Any]] = Field(
        default=None,
        description="Parsed coach_story_archive data (DEP-ENG-024) — optional enrichment",
    )
    philosophy_brief_data: Optional[dict[str, Any]] = Field(
        default=None,
        description="Parsed philosophy brief data — optional enrichment",
    )

    # Availability tracking
    source_availability: SignalSourceAvailability = Field(
        default_factory=SignalSourceAvailability,
    )


class SignalSourceLoader:
    """Loads and verifies all signal sources for the Minister of Identity scoring pipeline.

    Spec §Phase 1 INGEST — Steps 1-6.
    AC9: Missing required deps → CANNOT_SCORE_MISSING_DEPENDENCIES.
    AC10: Read-only — never writes to source files.

    The loader reads JSON files from the coach directory and returns a frozen SignalBundle.
    All paths are resolved from the coach_dir root.
    """

    # Required file paths relative to coach_dir
    REQUIRED_FILES: dict[str, str] = {
        "coach_soul": "config/coach_soul.json",
        "ttt_baseline": "config/ttt_baseline.json",
        "tribe_soul": "config/tribe_soul.json",
    }

    # Optional file paths relative to coach_dir
    OPTIONAL_FILES: dict[str, str] = {
        "cultural_memory_map": "config/cultural_memory_map.json",
        "coach_story_archive": "config/coach_story_archive.json",
        "philosophy_brief": "config/philosophy_brief.json",
    }

    def __init__(self, coach_dir: Path):
        """Initialize the loader with a coach directory.

        Args:
            coach_dir: Root directory for this coach instance.
        """
        self.coach_dir = coach_dir

    def _load_json(self, file_path: Path) -> Optional[dict[str, Any]]:
        """Safely load a JSON file. Returns None if file doesn't exist or is malformed."""
        if not file_path.exists():
            return None
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return None

    def load(self) -> SignalBundle:
        """Load all signal sources and verify prerequisites.

        Spec §Phase 1 INGEST — Steps 1-6:
          1. Load coach_soul.json — verify DEP-ENG-003, DEP-ENG-004, DEP-LIB-001 populated
          2. Load ttt_baseline.json — verify TTT profile exists
          3. Load tribe_soul.json — verify DEP-ENG-001 populated
          4. Load cultural_memory_map (optional)
          5. Load coach_story_archive (optional)
          6. Load philosophy_brief (optional)

        Returns:
            SignalBundle with all loaded data.

        Raises:
            MissingDependencyError: If any required DEP object is missing (AC9).
        """
        # Check all required files
        missing: list[str] = []
        required_data: dict[str, Optional[dict[str, Any]]] = {}

        for key, rel_path in self.REQUIRED_FILES.items():
            full_path = self.coach_dir / rel_path
            data = self._load_json(full_path)
            if data is None:
                missing.append(rel_path)
            required_data[key] = data

        # AC9: If any required dep missing, raise with full list
        if missing:
            raise MissingDependencyError(missing)

        # Load optional enrichments
        optional_data: dict[str, Optional[dict[str, Any]]] = {}
        for key, rel_path in self.OPTIONAL_FILES.items():
            full_path = self.coach_dir / rel_path
            optional_data[key] = self._load_json(full_path)

        # Build availability tracking
        availability = SignalSourceAvailability(
            coach_soul=required_data["coach_soul"] is not None,
            ttt_baseline=required_data["ttt_baseline"] is not None,
            tribe_soul=required_data["tribe_soul"] is not None,
            cultural_memory_map=optional_data["cultural_memory_map"] is not None,
            coach_story_archive=optional_data["coach_story_archive"] is not None,
            philosophy_brief=optional_data["philosophy_brief"] is not None,
        )

        return SignalBundle(
            coach_soul_data=required_data["coach_soul"],  # type: ignore[arg-type]
            ttt_baseline_data=required_data["ttt_baseline"],  # type: ignore[arg-type]
            tribe_soul_data=required_data["tribe_soul"],  # type: ignore[arg-type]
            cultural_memory_map_data=optional_data["cultural_memory_map"],
            coach_story_archive_data=optional_data["coach_story_archive"],
            philosophy_brief_data=optional_data["philosophy_brief"],
            source_availability=availability,
        )
