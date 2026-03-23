"""
CCP FR23 — Skill Fingerprint ID & Archive Engine Models (DEP-ENG-020)

Pydantic v2 models for the Fingerprint Archive Engine.
Every successfully compiled SKILL.md receives a cryptographically unique
Fingerprint ID linking its exact dependency state to downstream performance.

Spec reference: FR23_Skill_Fingerprint_ID_Tech_Spec.md
  §4 — Stage 1: Fingerprint String Synthesis
  §4 — Stage 2: Archive Engine Registration
  §4 — Stage 3: Output Linkage API (Telemetry Listener)
  §4 — Stage 4: Promotion Tier Protocol (DEP-PROTO-012)
  §5 — Primary Output Schema (fingerprint_archive.json)

Skill ID format (Spec §4 Stage 1 Step 4):
  SKILL-{ARCH_ID}-{COACH_ID}-{MOOD}-{REG_FRAME}-{COHORT}-{YYYYMMDD}-{SEQ}
  Example: SKILL-STORY01-EMI-P-PRV-L-20260315-001

Promotion Tiers (DEP-PROTO-012):
  Draft    → default on registration.
  Tested   → outputs.length >= 3 with assembly_failure == false.
  Stable   → outputs.length >= 10 + saves > 2x category average.
  Reference→ Stable + manual Architecture Review approval.

ADR-01: coach_id isolates all fingerprint records per tenant.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

# ─── Constants ────────────────────────────────────────────────────────────────

SKILL_ID_SEQ_FORMAT: str = "03d"
"""Sequence number zero-padded to 3 digits per spec example: '001'."""

TESTED_MINIMUM_OUTPUTS: int = 3
"""Spec §4 Stage 4: Tested requires outputs.length >= 3 (assembly_failure==false)."""

STABLE_MINIMUM_OUTPUTS: int = 10
"""Spec §4 Stage 4: Stable requires outputs.length >= 10 across diverse inputs."""

STABLE_SAVE_MULTIPLIER: float = 2.0
"""Spec §4 Stage 4: Stable requires saves > 2x category average."""


# ─── Enumerations ─────────────────────────────────────────────────────────────

class SkillMaturity(str, Enum):
    """Promotion Tier states per DEP-PROTO-012.

    Spec §4 Stage 4:
      Draft     → default, high plasticity.
      Tested    → >= 3 successful outputs, medium plasticity.
      Stable    → >= 10 diverse outputs + 2x saves, low plasticity.
      Reference → Stable + Architecture Review approval.
    """
    DRAFT = "draft"
    TESTED = "tested"
    STABLE = "stable"
    REFERENCE = "reference"


class MoodCode(str, Enum):
    """Single-character mood codes used in Skill ID synthesis.

    Spec §4 Stage 1 Step 1: MOOD = P, E, D, S.
    """
    PROCESSING = "P"
    ESCAPE = "E"
    DISCOVERY = "D"
    SOCIAL = "S"


class RegulatoryFrame(str, Enum):
    """Regulatory frame codes for Skill ID.

    Spec §4 Stage 1 Step 1: REG_FRAME = PRO (promotion) | PRV (prevention).
    """
    PROMOTION = "PRO"
    PREVENTION = "PRV"


class AudienceCohort(str, Enum):
    """Audience cohort codes for Skill ID.

    Spec §4 Stage 1 Step 1: COHORT = N (new) | DEV (developing) | L (loyal).
    """
    NEW = "N"
    DEVELOPING = "DEV"
    LOYAL = "L"


class ArchiveWriteError(str, Enum):
    """Error codes for archive write operations.

    Spec §4 Stage 3 Failure Condition: API receives payload with no skill_id
    association → UNLINKED_ORPHAN_OUTPUT.
    """
    UNLINKED_ORPHAN_OUTPUT = "UNLINKED_ORPHAN_OUTPUT"
    IO_COLLISION = "IO_COLLISION"
    SKILL_ID_NOT_FOUND = "SKILL_ID_NOT_FOUND"


# ─── Fingerprint ID Components ────────────────────────────────────────────────

class SkillIDComponents(BaseModel):
    """Input components for Skill ID synthesis.

    Spec §4 Stage 1 Steps 1-4: Extract 6 routing variables + date + sequence.
    AC1: Null pointers break the hyphenated formatting.
    """

    arch_id: str = Field(
        ...,
        description="Archetype identifier (e.g., 'STORY01', 'LIST02').",
    )
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="3-char coach acronym for ADR-01 isolation.",
    )
    mood: MoodCode = Field(
        ...,
        description="Spec: MOOD = P|E|D|S.",
    )
    regulatory_frame: RegulatoryFrame = Field(
        ...,
        description="Spec: REG_FRAME = PRO|PRV.",
    )
    cohort: AudienceCohort = Field(
        ...,
        description="Spec: COHORT = N|DEV|L.",
    )
    compilation_date: date = Field(
        ...,
        description="UTC compilation date — YYYYMMDD for ID synthesis.",
    )
    sequence_number: int = Field(
        default=1, ge=1,
        description="Spec §4 Stage 1 Step 3: Same-day sequence, starting at 001.",
    )

    def synthesize(self) -> str:
        """Build the human-readable Skill ID string.

        Spec §4 Stage 1 Step 4:
          SKILL-{ARCH_ID}-{COACH_ID}-{MOOD}-{REG_FRAME}-{COHORT}-{YYYYMMDD}-{SEQ}
        AC1 Example: SKILL-LIST02-ANA-E-PRO-N-20260315-001
        """
        date_str = self.compilation_date.strftime("%Y%m%d")
        seq_str = format(self.sequence_number, SKILL_ID_SEQ_FORMAT)
        return (
            f"SKILL-{self.arch_id}-{self.coach_id}-"
            f"{self.mood.value}-{self.regulatory_frame.value}-"
            f"{self.cohort.value}-{date_str}-{seq_str}"
        )


# ─── Dependency Snapshot ──────────────────────────────────────────────────────

class DependencySnapshot(BaseModel):
    """SHA-256 hashes of the dependency state at compilation time.

    Spec §4 Stage 2 Step 1: Generate SHA-256 hashes for current state of
    DEP-ENG-003, DEP-ENG-006, DEP-ENG-016.

    AC2: Running the same hashing algorithm on the same file at same timestamp
    must produce the exact same hash. Empty strings are invalid.
    """

    dep_eng_003: str = Field(
        default="",
        description="SHA-256 hash of Voice DNA (Positive Space Object).",
    )
    dep_eng_006: str = Field(
        default="",
        description="SHA-256 hash of the Emotional DNA baseline.",
    )
    dep_eng_016: str = Field(
        default="",
        description="SHA-256 hash of the Psychological Brief Mode.",
    )
    additional_deps: dict[str, str] = Field(
        default_factory=dict,
        description="Any additional dependency hashes for this compilation.",
    )

    def is_populated(self) -> bool:
        """AC2 guard: All core hashes must be non-empty strings."""
        return all([
            len(self.dep_eng_003) > 0,
            len(self.dep_eng_006) > 0,
            len(self.dep_eng_016) > 0,
        ])


# ─── Performance Telemetry ─────────────────────────────────────────────────────

class ContentPerformanceMetrics(BaseModel):
    """Platform performance metrics for a single output.

    Spec §5 Schema: saves, shares, comments, viral_quartet_score.
    """

    saves: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    viral_quartet_score: float = Field(
        default=0.0, ge=0.0,
        description="0.0-5.0 composite virality score.",
    )


class AudienceSignals(BaseModel):
    """Behavioural signals beyond raw engagement counts.

    Spec §5 Schema: dm_vulnerability_ratio, comment_depth_score,
    save_to_share_ratio.
    """

    dm_vulnerability_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    comment_depth_score: float = Field(default=0.0, ge=0.0)
    save_to_share_ratio: float = Field(default=0.0, ge=0.0)


class OutputTelemetryPayload(BaseModel):
    """A single telemetry record appended to the outputs array.

    Spec §4 Stage 3: Listener receives structured analytics payload,
    finds target skill_id, appends to outputs array, triggers Stage 4.

    Spec §6 Backward Compatibility: If skill_id is absent →
    UNLINKED_ORPHAN_OUTPUT warning; write is safely ignored.
    """

    output_id: str = Field(
        ...,
        description="Unique output identifier (e.g., 'OUT-STORY01-EMI-20260316-001').",
    )
    skill_id: str = Field(
        ...,
        description="Parent skill_id this output belongs to.",
    )
    content_title: str = Field(default="")
    platform: str = Field(default="instagram")
    published_date: Optional[str] = Field(default=None)
    performance: ContentPerformanceMetrics = Field(
        default_factory=ContentPerformanceMetrics,
    )
    audience_signals: AudienceSignals = Field(
        default_factory=AudienceSignals,
    )
    assembly_failure: bool = Field(
        default=False,
        description=(
            "Spec §4 Stage 4 AC3: Error-flagged assembly must NOT count toward "
            "Tested threshold. assembly_failure==true → excluded from promotion math."
        ),
    )
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01: tenant isolation. Payload locked to this coach's archive.",
    )


# ─── Archive Record ────────────────────────────────────────────────────────────

class FingerprintArchiveRecord(BaseModel):
    """A single record in DEP-ENG-020 fingerprint_archive.json.

    Spec §4 Stage 2 Step 2: Appended to fingerprint_archive.json on registration.

    AC4: Emilio's telemetry payload must ONLY write to Emilio's isolated
    fingerprint_archive.json bucket (ADR-01 strict isolation).
    """

    skill_id: str = Field(
        ...,
        description="Human-readable Skill Fingerprint ID.",
    )
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant partition key.",
    )
    archetype_template_id: str = Field(default="")
    archetype_template_version: str = Field(default="")
    compilation_date: str = Field(
        default="",
        description="ISO date string YYYY-MM-DD.",
    )
    maturity: SkillMaturity = Field(
        default=SkillMaturity.DRAFT,
        description="Spec §4 Stage 4: Default state upon Stage 2 registration.",
    )
    assembly_status: str = Field(
        default="COMPLETE",
        description="Assembly status from FR21 (FR21's AssemblyStatus enum value).",
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Spec §5: {coach_id, mood_state, regulatory_frame, audience_cohort, "
            "tmt_function, sdt_need_primary}."
        ),
    )
    dep_snapshot: DependencySnapshot = Field(
        default_factory=DependencySnapshot,
        description="SHA-256 hashes of dependencies at compilation time.",
    )
    outputs: list[OutputTelemetryPayload] = Field(
        default_factory=list,
        description="Empty on registration. Appended via Stage 3 Telemetry Listener.",
    )
    performance_scores: dict[str, float] = Field(
        default_factory=dict,
    )
    promoted_to_stable: bool = Field(
        default=False,
    )
    promoted_to_reference: bool = Field(
        default=False,
    )
    reference_review_approved: bool = Field(
        default=False,
        description="Spec §4 Stage 4: Reference requires manual Architecture Review approval.",
    )

    def successful_output_count(self) -> int:
        """Count outputs where assembly_failure == false.

        Spec §4 Stage 4 AC3: Error-flagged assembly must NOT count toward
        Tested threshold.
        """
        return sum(1 for o in self.outputs if not o.assembly_failure)

    def average_saves(self) -> float:
        """Average saves across all successful outputs."""
        successful = [o for o in self.outputs if not o.assembly_failure]
        if not successful:
            return 0.0
        return sum(o.performance.saves for o in successful) / len(successful)

    def evaluate_maturity(
        self,
        category_average_saves: float = 0.0,
    ) -> SkillMaturity:
        """DEP-PROTO-012 promotion logic.

        Spec §4 Stage 4:
          Draft   → always default.
          Tested  → successful_outputs >= 3.
          Stable  → successful_outputs >= 10 AND saves > 2x category average.
          Reference → Stable AND reference_review_approved.
        """
        success_count = self.successful_output_count()
        avg_saves = self.average_saves()

        if (
            self.reference_review_approved
            and success_count >= STABLE_MINIMUM_OUTPUTS
            and category_average_saves > 0
            and avg_saves > STABLE_SAVE_MULTIPLIER * category_average_saves
        ):
            return SkillMaturity.REFERENCE

        if (
            success_count >= STABLE_MINIMUM_OUTPUTS
            and category_average_saves > 0
            and avg_saves > STABLE_SAVE_MULTIPLIER * category_average_saves
        ):
            return SkillMaturity.STABLE

        if success_count >= TESTED_MINIMUM_OUTPUTS:
            return SkillMaturity.TESTED

        return SkillMaturity.DRAFT


# ─── Promotion Evaluation Result ──────────────────────────────────────────────

class PromotionEvaluationResult(BaseModel):
    """Result from the Archive-Promotion-Monitor.

    Spec §4 Stage 4: Runs asynchronously every time Telemetry Listener fires.
    AC3: 'asynchronous monitor immediately changes maturity to Tested.'
    """

    skill_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    previous_maturity: SkillMaturity
    new_maturity: SkillMaturity
    promoted: bool
    successful_output_count: int
    average_saves: float
    category_average_saves: float
    promotion_reason: str = Field(default="")
    receipt_hash: str = Field(default="")

    def model_post_init(self, __context: Any) -> None:
        self.promoted = self.new_maturity != self.previous_maturity
        if self.promoted:
            self.promotion_reason = (
                f"Promoted {self.previous_maturity.value} → {self.new_maturity.value}: "
                f"{self.successful_output_count} successful outputs, "
                f"avg_saves={self.average_saves:.0f} "
                f"(category_avg={self.category_average_saves:.0f})"
            )


# ─── Telemetry Listener Response ──────────────────────────────────────────────

class TelemetryListenerResponse(BaseModel):
    """Response from the Archive-Telemetry-Listener endpoint.

    Spec §4 Stage 3: Listener validates schema, appends to outputs array.
    Spec §6: skill_id absent → UNLINKED_ORPHAN_OUTPUT (safe ignore, log warning).
    """

    accepted: bool = Field(
        ...,
        description="True if payload was successfully appended.",
    )
    skill_id: str = Field(default="")
    output_id: str = Field(default="")
    error: Optional[ArchiveWriteError] = Field(
        default=None,
        description="Set when write fails (orphan, IO collision, not found).",
    )
    promotion_result: Optional[PromotionEvaluationResult] = Field(
        default=None,
        description="Set when Stage 4 check runs post-append.",
    )
    receipt_hash: str = Field(default="")


# ─── Archive Query Models ──────────────────────────────────────────────────────

class ArchiveRegistrationResult(BaseModel):
    """Result of registering a new skill in DEP-ENG-020.

    Spec §4 Stage 2: On successful registration:
      - dep_snapshot populated
      - outputs array is []
      - maturity is 'draft'
    """

    success: bool
    skill_id: str = Field(default="")
    coach_id: str = Field(default="")
    maturity: SkillMaturity = Field(default=SkillMaturity.DRAFT)
    dep_snapshot_populated: bool = Field(default=False)
    error: Optional[ArchiveWriteError] = Field(default=None)
    receipt_hash: str = Field(default="")
