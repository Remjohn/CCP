"""
CCP FR25 — Boredom Ban Novelty Enforcement Models (DEP-PROTO-015)

Pydantic v2 models for the Boredom Ban (Novelty Enforcement) Protocol.
Prevents LLM drift toward safe, repetitive analogies and structures
across the 36-script weekly production batch.

Spec reference: FR25_Boredom_Ban_Tech_Spec.md
  §4 — Stage 1: Theme Discovery Novelty Check (Agent Divine)
  §4 — Stage 2: Wisdom Forge Metaphor Extraction (Lionel/Jordan)
  §4 — Stage 3: Draft Testing Validation (Agent Grâce)
  §5 — Primary Output Schema (Novelty Check Ledger / assembly_report.json)

Three-vector comparison (Spec §3 Technical Decision 1):
  1. Thematic Payload    — cosine similarity > 0.80 → REJECT: BOREDOM_BAN
  2. Structural Pattern  — LIST02 > 3 uses in 14 days → REJECT: STRUCTURAL_FATIGUE
  3. Metaphorical Vehicle — exact/synonym match → REJECT: TILL_DONE_TRIGGERED

Fatigue Override Circuit Breaker (Spec §4 Stage 1):
  3 consecutive theme collisions → FATIGUE_OVERRIDE_GRANTED: true
  → bypass collision check for this batch slot only, log to operator dashboard.

Cold Start (Spec §6 Backward Compatibility):
  MemoryFolder returns null / [] → PASS + MEMORY_ABSENT_ASSUMED_NOVEL.
  Does NOT halt pipeline.

ADR-01: coach_id scopes ALL episodic memory lookups — Coach A's memory
MUST NEVER be accessible to Coach B's compilation.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

# ─── Constants ────────────────────────────────────────────────────────────────

BOREDOM_BAN_WINDOW_DAYS: int = 56
"""8-week sliding window (56 days). Spec §4 AC1: 'past 56 days', NOT 30 days."""

THEME_COSINE_REJECT_THRESHOLD: float = 0.80
"""Spec §4 Stage 1 Step 3: cosine > 0.80 → flag [REJECT: BOREDOM_BAN]."""

STRUCTURAL_FATIGUE_MAX_USES: int = 3
"""Spec §4 Stage 3 Step 3: Archetype used > 3 times in 14 days → STRUCTURAL_FATIGUE."""

STRUCTURAL_FATIGUE_DAYS: int = 14
"""Spec §4 Stage 3: Structural fatigue check window is 14 days."""

FATIGUE_OVERRIDE_COLLISION_COUNT: int = 3
"""Spec §4 Stage 1 Failure Condition: 3 consecutive collisions → FATIGUE_OVERRIDE_GRANTED."""


# ─── Enumerations ─────────────────────────────────────────────────────────────

class BoredomBanVectorStatus(str, Enum):
    """Per-vector novelty verdict.

    Spec §5 Output Schema: each of the 3 vectors has a status field.
    """
    PASS = "PASS"
    REJECT_BOREDOM_BAN = "REJECT_BOREDOM_BAN"
    REJECT_TILL_DONE_TRIGGERED = "REJECT_TILL_DONE_TRIGGERED"
    REJECT_STRUCTURAL_FATIGUE = "REJECT_STRUCTURAL_FATIGUE"
    MEMORY_ABSENT_ASSUMED_NOVEL = "MEMORY_ABSENT_ASSUMED_NOVEL"


class OverallNoveltyVerdict(str, Enum):
    """Final clearance verdict for the Boredom Ban protocol.

    Spec §5 Schema: 'final_clearance': true/false.
    """
    CLEAR = "CLEAR"
    BLOCKED = "BLOCKED"
    FATIGUE_OVERRIDE = "FATIGUE_OVERRIDE"
    MEMORY_ABSENT = "MEMORY_ABSENT"


class BoredomBanStage(str, Enum):
    """Which pipeline stage the check ran in.

    Spec §4: Early = Theme Discovery (Stage 1),
             Mid = Wisdom Forge (Stage 2),
             Late = Draft Testing (Stage 3).
    """
    EARLY_THEME_DISCOVERY = "EARLY_THEME_DISCOVERY"
    MID_METAPHOR_EXTRACTION = "MID_METAPHOR_EXTRACTION"
    LATE_DRAFT_TESTING = "LATE_DRAFT_TESTING"


class TillDoneRewriteType(str, Enum):
    """What the TillDone extension is commanded to mutate.

    Spec §4 Stage 3 Step 4: commanded to mutate script archetype.
    Spec §4 Stage 2 Step 3: commanded to generate new metaphorical vehicle.
    """
    MUTATE_METAPHOR_VEHICLE = "MUTATE_METAPHOR_VEHICLE"
    MUTATE_ARCHETYPE_STRUCTURE = "MUTATE_ARCHETYPE_STRUCTURE"
    MUTATE_THEMATIC_PAYLOAD = "MUTATE_THEMATIC_PAYLOAD"


# ─── Memory Folder (Episodic Memory) ──────────────────────────────────────────

class MemoryFolderEntry(BaseModel):
    """A single entry in the MemoryFolder episodic memory store.

    Spec §4: MemoryFolder tracks Fingerprint IDs and extracted semantic/
    structural payloads of all content over the 8-week rolling window.
    """

    skill_id: str = Field(
        ...,
        description="Fingerprint ID of the compiled skill this entry represents.",
    )
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant key — STRICTLY isolated per coach.",
    )
    thematic_payload: str = Field(
        default="",
        description="Extracted thematic core of this skill's content.",
    )
    metaphor_vehicle: str = Field(
        default="",
        description="The metaphorical vehicle used in this output.",
    )
    archetype_format: str = Field(
        default="",
        description="Archetype format code (e.g., 'STORY01', 'LIST02').",
    )
    published_date: date = Field(
        ...,
        description="Date this content was published / cleared compilation.",
    )

    def is_within_window(self, reference_date: Optional[date] = None) -> bool:
        """True if this entry falls within the BOREDOM_BAN_WINDOW_DAYS window.

        Spec §4 Stage 1: 'past 56 days' rolling window.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()
        delta = (reference_date - self.published_date).days
        return 0 <= delta <= BOREDOM_BAN_WINDOW_DAYS

    def is_within_structural_window(self, reference_date: Optional[date] = None) -> bool:
        """True if within the 14-day structural fatigue window.

        Spec §4 Stage 3: Structural fatigue check is 14-day, NOT 56-day.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()
        delta = (reference_date - self.published_date).days
        return 0 <= delta <= STRUCTURAL_FATIGUE_DAYS


class MemoryFolderQuery(BaseModel):
    """Query parameters for the Episodic-Memory-Query-API.

    Spec §7 Task 1: 'accepts a date range (Now - 56 days) and a target
    specific slice (theme, structure, metaphor).'
    """

    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01: MUST only return this coach's memory.",
    )
    window_days: int = Field(
        default=BOREDOM_BAN_WINDOW_DAYS,
        description="Rolling window in days. Default 56.",
    )
    fetch_themes: bool = Field(default=True)
    fetch_metaphors: bool = Field(default=True)
    fetch_structures: bool = Field(default=True)
    reference_date: Optional[date] = Field(
        default=None,
        description="Reference date for window calculation. None → today UTC.",
    )


# ─── Per-Vector Check Results ─────────────────────────────────────────────────

class ThematicSimilarityResult(BaseModel):
    """Result of the cosine similarity check on thematic payload.

    Spec §4 Stage 1: cosine > 0.80 → REJECT: BOREDOM_BAN.
    AC2: Cosine 0.85 → Divine drops theme and replaces it.
    """

    proposed_theme: str = Field(default="")
    similarity_score: float = Field(
        default=0.0, ge=0.0, le=1.0,
    )
    status: BoredomBanVectorStatus = Field(
        default=BoredomBanVectorStatus.PASS,
    )
    closest_match_id: Optional[str] = Field(
        default=None,
        description="Fingerprint ID of the closest prior theme.",
    )
    closest_match_theme: Optional[str] = Field(
        default=None,
    )
    memory_absent: bool = Field(
        default=False,
        description="True when MemoryFolder returned null/[] (cold start).",
    )
    collision_count: int = Field(
        default=0,
        description="Consecutive collision count for fatigue override tracking.",
    )

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive status from score and memory state."""
        if self.memory_absent:
            self.status = BoredomBanVectorStatus.MEMORY_ABSENT_ASSUMED_NOVEL
        elif self.similarity_score > THEME_COSINE_REJECT_THRESHOLD:
            self.status = BoredomBanVectorStatus.REJECT_BOREDOM_BAN
        else:
            self.status = BoredomBanVectorStatus.PASS


class MetaphorCollisionResult(BaseModel):
    """Result of the metaphor vehicle overlap check.

    Spec §4 Stage 2: direct exact-match/synonym overlap check.
    AC1: 'house foundation' metaphor used 32 days ago → Grâce rejects it.
    Spec AC1 failure: system allows it because hardcoded 30-day limit (NOT 56).
    """

    proposed_metaphor: str = Field(default="")
    status: BoredomBanVectorStatus = Field(
        default=BoredomBanVectorStatus.PASS,
    )
    offending_vehicle: Optional[str] = Field(
        default=None,
        description="The prior metaphor that collided.",
    )
    closest_match_id: Optional[str] = Field(
        default=None,
    )
    days_since_last_use: Optional[int] = Field(
        default=None,
    )
    memory_absent: bool = Field(default=False)
    till_done_rewrite_command: Optional[str] = Field(
        default=None,
        description=(
            "Spec §4 Stage 2 Step 3: 'Metaphor [X] was used N days ago. "
            "Generate a new conceptual vehicle from an unrelated domain.'"
        ),
    )


class StructuralFatigueResult(BaseModel):
    """Result of the structural fatigue check for an archetype format.

    Spec §4 Stage 3: LIST02 used > 3 times in 14 days → STRUCTURAL_FATIGUE.
    AC3: 4th Shocking Listicle in same week → reject, force reshape to Case Study.
    """

    archetype_format: str = Field(
        default="",
        description="Archetype format being checked (e.g., 'LIST02').",
    )
    frequency_14_days: int = Field(
        default=0,
        description="Number of times this archetype was used in last 14 days.",
    )
    status: BoredomBanVectorStatus = Field(
        default=BoredomBanVectorStatus.PASS,
    )
    memory_absent: bool = Field(default=False)
    suggested_alternative: Optional[str] = Field(
        default=None,
        description="Alternative archetype suggested when structural fatigue fires.",
    )

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive status from frequency."""
        if self.memory_absent:
            self.status = BoredomBanVectorStatus.MEMORY_ABSENT_ASSUMED_NOVEL
        elif self.frequency_14_days > STRUCTURAL_FATIGUE_MAX_USES:
            self.status = BoredomBanVectorStatus.REJECT_STRUCTURAL_FATIGUE
        else:
            self.status = BoredomBanVectorStatus.PASS


# ─── TillDone Rewrite Payload ─────────────────────────────────────────────────

class BoredomBanTillDonePayload(BaseModel):
    """Payload dispatched to the TillDone extension when novelty fails.

    Spec §4 Stage 3 Step 4: 'generation agent is commanded via TillDone to
    mutate the script into STORY01 or another assigned, non-fatigued Archetype.'
    """

    rewrite_type: TillDoneRewriteType
    original_value: str = Field(
        default="",
        description="The rejected metaphor, theme, or archetype.",
    )
    rejection_reason: BoredomBanVectorStatus
    rejection_detail: str = Field(default="")
    mutation_command: str = Field(
        default="",
        description=(
            "The explicit LLM command to mutate. "
            "E.g., 'Generate a new conceptual vehicle from an unrelated domain "
            "(biology, architecture, thermodynamics).'."
        ),
    )
    till_done_iteration: int = Field(
        default=1, ge=1,
        description="Which TillDone iteration this is (max 3 per spec FR24).",
    )


# ─── Fatigue Override Record ──────────────────────────────────────────────────

class FatigueOverrideRecord(BaseModel):
    """Records when the fatigue override circuit breaker fires.

    Spec §4 Stage 1 Failure Condition:
      3 consecutive theme collisions → FATIGUE_OVERRIDE_GRANTED: true.
      Bypass collision check for this batch slot only.
      Log override to operator dashboard with collision details for manual review.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    slot_id: str = Field(default="")
    stage_name: str = Field(default="FATIGUE-OVERRIDE")
    agent_name: str = Field(default="Divine")
    collision_count: int = Field(
        default=FATIGUE_OVERRIDE_COLLISION_COUNT,
        description="Always 3 when override fires.",
    )
    override_granted: bool = Field(default=True)
    colliding_themes: list[str] = Field(
        default_factory=list,
        description="The 3 themes that collided — for operator manual review.",
    )
    timestamp: str = Field(default="")
    receipt_hash: str = Field(default="")


# ─── Boredom Ban Result ────────────────────────────────────────────────────────

class BoredomBanResult(BaseModel):
    """Full output of the DEP-PROTO-015 Boredom Ban Protocol check.

    Spec §5 Output Schema — attached to assembly_report.json.
    AC4: Coach A's check MUST NOT read Coach B's memory.
    """

    protocol_invocation: str = Field(
        default="DEP-PROTO-015_BOREDOM_BAN",
    )
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 strict isolation — all memory reads scoped to this coach.",
    )
    stage: BoredomBanStage = Field(
        ...,
        description="Which pipeline stage this check ran in.",
    )
    eight_week_window_start: Optional[str] = Field(
        default=None,
        description="ISO date of the 8-week window start (today - 56 days).",
    )
    vectors_checked: dict[str, Any] = Field(
        default_factory=dict,
        description="Spec §5: {thematic_similarity, metaphor_collision, structural_fatigue}.",
    )
    thematic_similarity: Optional[ThematicSimilarityResult] = Field(default=None)
    metaphor_collision: Optional[MetaphorCollisionResult] = Field(default=None)
    structural_fatigue: Optional[StructuralFatigueResult] = Field(default=None)
    till_done_payloads: list[BoredomBanTillDonePayload] = Field(
        default_factory=list,
    )
    fatigue_override: Optional[FatigueOverrideRecord] = Field(
        default=None,
        description="Set when the circuit breaker fires after 3 collisions.",
    )
    till_done_iterations_required: int = Field(
        default=0,
        description="Total TillDone iterations used across all vectors.",
    )
    final_clearance: bool = Field(
        default=False,
    )
    overall_verdict: OverallNoveltyVerdict = Field(
        default=OverallNoveltyVerdict.BLOCKED,
    )
    memory_absent_log: Optional[str] = Field(
        default=None,
        description=(
            "Spec §6: Set to '[MEMORY_ABSENT_ASSUMED_NOVEL]' on cold start. "
            "Pipeline proceeds without halting."
        ),
    )
    receipt_hash: str = Field(default="")

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive overall_verdict and final_clearance from vector results."""
        # Cold start: all vectors absent
        theme_absent = (
            self.thematic_similarity is not None
            and self.thematic_similarity.memory_absent
        )
        meta_absent = (
            self.metaphor_collision is not None
            and self.metaphor_collision.memory_absent
        )
        struct_absent = (
            self.structural_fatigue is not None
            and self.structural_fatigue.memory_absent
        )

        # All absent = cold start
        checked = [
            self.thematic_similarity,
            self.metaphor_collision,
            self.structural_fatigue,
        ]
        present = [c for c in checked if c is not None]
        all_absent = all(
            getattr(c, "memory_absent", False) for c in present
        ) if present else True

        if all_absent and present:
            self.overall_verdict = OverallNoveltyVerdict.MEMORY_ABSENT
            self.final_clearance = True
            self.memory_absent_log = "[MEMORY_ABSENT_ASSUMED_NOVEL]"
            return

        # Fatigue override
        if self.fatigue_override and self.fatigue_override.override_granted:
            self.overall_verdict = OverallNoveltyVerdict.FATIGUE_OVERRIDE
            self.final_clearance = True
            return

        # Check for any blocking vectors
        blocking_statuses = {
            BoredomBanVectorStatus.REJECT_BOREDOM_BAN,
            BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED,
            BoredomBanVectorStatus.REJECT_STRUCTURAL_FATIGUE,
        }
        blocked = False
        if self.thematic_similarity and self.thematic_similarity.status in blocking_statuses:
            blocked = True
        if self.metaphor_collision and self.metaphor_collision.status in blocking_statuses:
            blocked = True
        if self.structural_fatigue and self.structural_fatigue.status in blocking_statuses:
            blocked = True

        if blocked:
            self.overall_verdict = OverallNoveltyVerdict.BLOCKED
            self.final_clearance = False
        else:
            self.overall_verdict = OverallNoveltyVerdict.CLEAR
            self.final_clearance = True
