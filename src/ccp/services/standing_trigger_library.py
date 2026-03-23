"""
CCP Standing Trigger Library — FR1 Unit 10
Phase 2: Trigger Library Seeding, Gate G-LIB, Gate G-LIB-IDX

Spec reference: FR1 Tech Spec §Phase 2, Standing Trigger Library
Architecture reference: CCP_Technical_Architecture.md §3.3

Gate G-LIB: quality_score ≥ 0.65 (AC7 — 0.60 discarded, 0.65 accepted)
Gate G-LIB-IDX: primary key MUST be trigger_category_id (NOT archetype_id) (AC6)
Human evidence gate: ≥3 verified real-person examples (DEP-ENG-021)

7 trigger categories:
    Worth, Transformation, Certainty, Belonging, Authority, Resistance, Legacy

ADR-01 Single-Tenant: all entries scoped to coach_id.
C-11 Persona Masking Gate: no agent names in model-facing prompts.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# AC6 trigger categories — the ONLY valid primary key domain
VALID_TRIGGER_CATEGORIES = [
    "Worth",
    "Transformation",
    "Certainty",
    "Belonging",
    "Authority",
    "Resistance",
    "Legacy",
]

# Gate G-LIB quality threshold (AC7)
QUALITY_GATE_THRESHOLD: float = 0.65

# Human evidence gate (DEP-ENG-021)
HUMAN_EVIDENCE_MINIMUM: int = 3


class ArchetypeIndexRejected(Exception):
    """Raised when a library entry uses archetype_id as primary key.

    AC6: 'The standing trigger library must index by trigger_category_id,
    not archetype_id. Attempting to index by archetype raises ArchetypeIndexRejected.'
    """
    def __init__(self, attempted_key: str):
        self.attempted_key = attempted_key
        super().__init__(
            f"ARCHETYPE_INDEX_REJECTED: Standing trigger library entries must use "
            f"trigger_category_id as primary key. Received key: '{attempted_key}'. "
            f"Valid trigger categories: {', '.join(VALID_TRIGGER_CATEGORIES)}"
        )


class QualityGateRejected(Exception):
    """Raised when a library entry fails the G-LIB quality gate.

    AC7: 'Library entry with quality_score 0.60 is discarded;
    entry with quality_score 0.65 is saved.'
    """
    def __init__(self, quality_score: float, threshold: float = QUALITY_GATE_THRESHOLD):
        self.quality_score = quality_score
        self.threshold = threshold
        super().__init__(
            f"QUALITY_GATE_REJECTED: Entry quality_score {quality_score:.2f} is below "
            f"threshold {threshold:.2f}. Entry discarded."
        )


class HumanEvidenceGateRejected(Exception):
    """Raised when an entry lacks sufficient human evidence (DEP-ENG-021)."""
    def __init__(self, human_count: int, required: int = HUMAN_EVIDENCE_MINIMUM):
        self.human_count = human_count
        self.required = required
        super().__init__(
            f"HUMAN_EVIDENCE_GATE_REJECTED: Entry has {human_count} verified human examples. "
            f"Required: ≥{required} (DEP-ENG-021)."
        )


class TriggerLibraryEntry(BaseModel):
    """A single Standing Trigger Library entry.

    Spec fields:
    - trigger_category_id: MUST be one of 7 valid categories (AC6)
    - quality_score: MUST be ≥ 0.65 to persist (AC7, G-LIB)
    - human_evidence_count: MUST be ≥ 3 verified real-person examples (DEP-ENG-021)

    The DB CHECK constraint enforces quality_score >= 0.65 and
    human_evidence_count >= 3 at the Supabase layer as well.
    """
    entry_id: str = Field(default_factory=lambda: f"STL-{uuid.uuid4().hex[:12].upper()}")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")

    # AC6: primary key domain — MUST be trigger_category_id, NOT archetype_id
    trigger_category_id: str = Field(
        ...,
        description="Primary index key — MUST be one of 7 trigger categories (AC6)"
    )

    trigger_phrase: str = Field(..., description="The trigger phrase or pattern")
    context_description: str = Field(..., description="When/how this trigger fires")
    human_evidence: list[str] = Field(
        default_factory=list,
        description="≥3 verified real-person examples (DEP-ENG-021)"
    )
    quality_score: float = Field(
        ...,
        description="Quality score 0.0–1.0. Must be ≥0.65 to persist (AC7, G-LIB)"
    )
    evidence_sources: list[str] = Field(
        default_factory=list,
        description="Source references for human evidence"
    )
    operator_approved: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("trigger_category_id")
    @classmethod
    def validate_trigger_category(cls, v: str) -> str:
        """AC6: Reject archetype_id; only trigger_category_id is valid."""
        if v not in VALID_TRIGGER_CATEGORIES:
            raise ValueError(
                f"trigger_category_id must be one of {VALID_TRIGGER_CATEGORIES}. "
                f"Received: '{v}'. "
                f"If you passed an archetype_id, use ArchetypeIndexRejected path instead."
            )
        return v

    @property
    def human_evidence_count(self) -> int:
        return len(self.human_evidence)


class StandingTriggerLibrary(BaseModel):
    """The full standing trigger library for a coach.

    AC6: all entries indexed by trigger_category_id (NOT archetype_id).
    AC7: entries with quality_score < 0.65 are never persisted.
    DEP-ENG-021: all entries require ≥3 verified human examples.
    """
    library_id: str = Field(default_factory=lambda: f"STL-LIB-{uuid.uuid4().hex[:8].upper()}")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    entries: list[TriggerLibraryEntry] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_by_category(self, trigger_category_id: str) -> list[TriggerLibraryEntry]:
        """Get all approved entries for a given trigger category."""
        return [
            e for e in self.entries
            if e.trigger_category_id == trigger_category_id and e.operator_approved
        ]

    def category_count(self) -> int:
        """Number of categories with at least one approved entry."""
        return len({
            e.trigger_category_id for e in self.entries if e.operator_approved
        })


class StandingTriggerLibraryService:
    """Service for seeding and managing the Standing Trigger Library.

    Spec Phase 2: 'Standing Trigger Library seeded with 7 trigger categories'
    Gate G-LIB: quality_score ≥ 0.65
    Gate G-LIB-IDX: primary key must be trigger_category_id

    The library is seeded AFTER Phase 1 completion (FR2 and FR3 complete).
    It provides the stable trigger backbone for context-aware content generation.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir

    def ingest_entry(
        self,
        trigger_category_id: str,
        trigger_phrase: str,
        context_description: str,
        human_evidence: list[str],
        quality_score: float,
        evidence_sources: Optional[list[str]] = None,
        entry_id_key_type: str = "trigger_category_id",
    ) -> TriggerLibraryEntry:
        """Ingest a single trigger library entry through all gates.

        Gate G-LIB-IDX (AC6): entry_id_key_type must be 'trigger_category_id'.
        Gate G-LIB (AC7): quality_score must be ≥ 0.65.
        DEP-ENG-021: human_evidence must have ≥ 3 entries.

        Args:
            trigger_category_id: One of the 7 valid trigger categories.
            trigger_phrase: The trigger pattern to store.
            context_description: Context/conditions for this trigger.
            human_evidence: List of real-person examples (min 3).
            quality_score: Quality score 0.0–1.0.
            evidence_sources: Source references for evidence.
            entry_id_key_type: Must be 'trigger_category_id' — passing
                               'archetype_id' raises ArchetypeIndexRejected (AC6).

        Returns:
            TriggerLibraryEntry if all gates pass.

        Raises:
            ArchetypeIndexRejected: If entry_id_key_type == 'archetype_id' (AC6).
            QualityGateRejected: If quality_score < 0.65 (AC7).
            HumanEvidenceGateRejected: If human_evidence count < 3 (DEP-ENG-021).
        """
        # Gate G-LIB-IDX (AC6): reject archetype-indexed entries
        if entry_id_key_type == "archetype_id":
            raise ArchetypeIndexRejected(attempted_key=entry_id_key_type)

        # Gate G-LIB (AC7): quality threshold
        if quality_score < QUALITY_GATE_THRESHOLD:
            raise QualityGateRejected(quality_score=quality_score)

        # Human evidence gate (DEP-ENG-021)
        if len(human_evidence) < HUMAN_EVIDENCE_MINIMUM:
            raise HumanEvidenceGateRejected(human_count=len(human_evidence))

        # Category validation (Pydantic field_validator handles this)
        entry = TriggerLibraryEntry(
            coach_id=self.coach_id,
            trigger_category_id=trigger_category_id,
            trigger_phrase=trigger_phrase,
            context_description=context_description,
            human_evidence=human_evidence,
            quality_score=quality_score,
            evidence_sources=evidence_sources or [],
        )

        return entry

    def batch_ingest(
        self,
        raw_entries: list[dict],
    ) -> tuple[list[TriggerLibraryEntry], list[dict]]:
        """Batch ingest entries, collecting passes and rejections.

        AC7 spec test: '0.60 discarded; 0.65 saved'

        Args:
            raw_entries: List of entry dicts with keys:
                trigger_category_id, trigger_phrase, context_description,
                human_evidence, quality_score, evidence_sources (optional),
                entry_id_key_type (optional, default 'trigger_category_id')

        Returns:
            Tuple of (accepted_entries, rejected_entries_with_reasons).
        """
        accepted: list[TriggerLibraryEntry] = []
        rejected: list[dict] = []

        for raw in raw_entries:
            try:
                entry = self.ingest_entry(
                    trigger_category_id=raw["trigger_category_id"],
                    trigger_phrase=raw["trigger_phrase"],
                    context_description=raw["context_description"],
                    human_evidence=raw.get("human_evidence", []),
                    quality_score=raw["quality_score"],
                    evidence_sources=raw.get("evidence_sources", []),
                    entry_id_key_type=raw.get("entry_id_key_type", "trigger_category_id"),
                )
                accepted.append(entry)
            except (ArchetypeIndexRejected, QualityGateRejected, HumanEvidenceGateRejected) as e:
                rejected.append({
                    "entry": raw,
                    "rejection_reason": str(e),
                    "rejection_type": type(e).__name__,
                })

        return accepted, rejected

    def save_library(self, entries: list[TriggerLibraryEntry]) -> StandingTriggerLibrary:
        """Save accepted entries to the standing trigger library config file.

        Args:
            entries: List of entries that have passed all gates.

        Returns:
            The full StandingTriggerLibrary.
        """
        # Load existing or create new
        library = self.load_library() or StandingTriggerLibrary(
            coach_id=self.coach_id,
        )

        # Append new entries (no duplicates by trigger_phrase + category)
        existing_signatures = {
            (e.trigger_category_id, e.trigger_phrase) for e in library.entries
        }
        for entry in entries:
            sig = (entry.trigger_category_id, entry.trigger_phrase)
            if sig not in existing_signatures:
                library.entries.append(entry)
                existing_signatures.add(sig)

        library.updated_at = datetime.now(timezone.utc)

        # Persist
        lib_path = self.coach_dir / "config" / "standing_trigger_library.json"
        lib_path.parent.mkdir(parents=True, exist_ok=True)
        lib_path.write_text(library.model_dump_json(indent=2), encoding="utf-8")

        return library

    def load_library(self) -> Optional[StandingTriggerLibrary]:
        """Load standing trigger library from local config."""
        lib_path = self.coach_dir / "config" / "standing_trigger_library.json"
        if not lib_path.exists():
            return None
        data = json.loads(lib_path.read_text(encoding="utf-8"))
        return StandingTriggerLibrary.model_validate(data)

    def get_triggers_for_generation(
        self,
        categories: Optional[list[str]] = None,
    ) -> dict[str, list[TriggerLibraryEntry]]:
        """Retrieve approved triggers grouped by category for content generation.

        Args:
            categories: Optional list of category names to filter by.
                        If None, returns all 7 categories.

        Returns:
            Dict mapping trigger_category_id → list of approved entries.
        """
        library = self.load_library()
        if library is None:
            return {}

        target_categories = categories or VALID_TRIGGER_CATEGORIES
        result: dict[str, list[TriggerLibraryEntry]] = {}

        for category in target_categories:
            category_entries = library.get_by_category(category)
            if category_entries:
                result[category] = category_entries

        return result
