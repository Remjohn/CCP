"""
CCP Step 8 — Research Synthesis Protocol Models (Unit 2)
Pydantic v2 models for FR17 Builder Engine Step 3.5 conflict detection.

Architecture reference:
    FR17_Research_Synthesis_Protocol_Tech_Spec.md
    CCP_Evolution_Architecture_Report_V4 §4.2

Models defined:
    ConflictType: Type 1 (Proximity), Type 2 (Structural), Type 3 (Authenticity)
    ConflictResolutionStatus: AUTO_RESOLVED, FLAGGED_FOR_OPERATOR, TERMINAL_BLOCK
    ConflictResolution: Individual conflict resolution record
    AssemblyReportExtension: The cral_conflict_resolution[] array
    Step35Result: Full Step 3.5 execution result

Technical Decisions (FR17 §3):
    1. Type 1 (Source Proximity) = deterministic auto-resolve (M6 > M2)
    2. Type 2 (Structural Mismatch) = halt + operator flag (non-destructive)
    3. Type 3 (Authenticity Conflict) = terminal block back to Phase 1
    4. Step 3.5 only executes if cral_coverage_status ≠ ABSENT

ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════
# Conflict Types & Resolution Status
# ══════════════════════════════════════════════════════════════

class ConflictType(str, Enum):
    """Three defined conflict types from FR17 §4."""
    TYPE_1_PROXIMITY = "TYPE_1_PROXIMITY"
    TYPE_2_STRUCTURAL = "TYPE_2_STRUCTURAL"
    TYPE_3_AUTHENTICITY = "TYPE_3_AUTHENTICITY"


class ConflictResolutionStatus(str, Enum):
    """Resolution outcome for each conflict pass."""
    NO_CONFLICT = "NO_CONFLICT"
    AUTO_RESOLVED = "AUTO_RESOLVED"
    FLAGGED_FOR_OPERATOR = "FLAGGED_FOR_OPERATOR"
    RESOLVED_BY_OPERATOR = "RESOLVED_BY_OPERATOR"
    TERMINAL_BLOCK = "TERMINAL_BLOCK"
    SKIPPED = "SKIPPED"


class Step35Status(str, Enum):
    """Overall Step 3.5 execution status."""
    CLEAR = "CLEAR"
    RESOLVED = "RESOLVED"
    PENDING_OPERATOR_CLEARANCE = "PENDING_OPERATOR_CLEARANCE"
    TERMINAL_BLOCK = "TERMINAL_BLOCK"
    SKIPPED_CRAL_ABSENT = "SKIPPED_CRAL_ABSENT"
    ERROR = "ERROR"


# ══════════════════════════════════════════════════════════════
# Conflict Resolution Record
# ══════════════════════════════════════════════════════════════

class ConflictResolution(BaseModel):
    """A single conflict resolution record for the assembly report.

    FR17 §5 Output Schema: Each entry in cral_conflict_resolution[]
    contains conflict_type, status, details, action_taken, receipt_hash.
    """
    conflict_type: ConflictType = Field(
        description="Which conflict type was detected."
    )
    status: ConflictResolutionStatus = Field(
        description="Resolution outcome."
    )
    details: str = Field(
        description=(
            "Human-readable description of the conflict. "
            "E.g., 'M2 (News Article) asserted mechanism A; "
            "M6 (Whistleblower Memo) asserted derivative mechanism A1.'"
        ),
    )
    action_taken: str = Field(
        description=(
            "What the protocol did. E.g., 'M6 forced as primary evidentiary anchor' "
            "or 'Placed in Operator Resolution Queue ID: REQ-XXXX'."
        ),
    )
    receipt_hash: str = Field(
        default="",
        description="Receipt chain hash for this specific resolution action."
    )
    operator_queue_id: Optional[str] = Field(
        default=None,
        description="Operator Resolution Queue ID if FLAGGED_FOR_OPERATOR."
    )
    source_a: str = Field(
        default="",
        description="First source in the conflict (e.g., 'DEP-ENG-021[M2_BELIEVABLE]')."
    )
    source_b: str = Field(
        default="",
        description="Second source in the conflict (e.g., 'DEP-ENG-021[M6_IRREFUTABLE]')."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional resolution metadata."
    )


# ══════════════════════════════════════════════════════════════
# Assembly Report Extension
# ══════════════════════════════════════════════════════════════

class AssemblyReportExtension(BaseModel):
    """The cral_conflict_resolution[] array for the assembly_report.json.

    FR17 §5: All Step 3.5 decisions are logged in assembly_report.json
    under key: cral_conflict_resolution[].
    """
    cral_conflict_resolution: list[ConflictResolution] = Field(
        default_factory=list,
        description="Ordered list of conflict resolution records."
    )
    step_35_status: Step35Status = Field(
        default=Step35Status.CLEAR,
        description="Overall Step 3.5 outcome."
    )
    type_1_count: int = Field(default=0, description="Number of Type 1 conflicts detected.")
    type_2_count: int = Field(default=0, description="Number of Type 2 conflicts detected.")
    type_3_count: int = Field(default=0, description="Number of Type 3 conflicts detected.")
    auto_resolved_count: int = Field(
        default=0,
        description="Number of conflicts auto-resolved deterministically."
    )
    operator_flags_count: int = Field(
        default=0,
        description="Number of conflicts flagged for operator review."
    )
    terminal_blocks_count: int = Field(
        default=0,
        description="Number of terminal blocks issued."
    )

    def has_blocking_conflicts(self) -> bool:
        """True if any conflicts require operator clearance or are terminal."""
        return self.operator_flags_count > 0 or self.terminal_blocks_count > 0


# ══════════════════════════════════════════════════════════════
# Step 3.5 Full Result
# ══════════════════════════════════════════════════════════════

class Step35Input(BaseModel):
    """Inputs for the Research Synthesis Protocol (Step 3.5).

    FR17 §4 Stage 1: Load DEP-ENG-021, DEP-ENG-010, DEP-ENG-005.
    """
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    cral_coverage_status: str = Field(
        default="ABSENT",
        description="COMPLETE | PARTIAL | DEGRADED | ABSENT"
    )
    cral_finding_index: Optional[Any] = Field(
        default=None,
        description="DEP-ENG-021 CRALFindingIndex (typed loosely to avoid circular imports)."
    )
    soc_batch: Optional[Any] = Field(
        default=None,
        description="DEP-ENG-010 FourAxisMatchResult / Source of Context batch."
    )
    auth_certificate: Optional[Any] = Field(
        default=None,
        description="DEP-ENG-005 TTTBaselineData / Authentication Certificate."
    )


class Step35Result(BaseModel):
    """Full result from the Research Synthesis Protocol.

    Contains the assembly report extension and execution metadata.
    """
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    step_35_status: Step35Status = Field(
        default=Step35Status.CLEAR,
        description="Overall Step 3.5 outcome."
    )
    assembly_report: AssemblyReportExtension = Field(
        default_factory=AssemblyReportExtension,
        description="The cral_conflict_resolution[] output."
    )
    compilation_allowed: bool = Field(
        default=True,
        description=(
            "True if compilation may proceed to Step 4 (Template Selection). "
            "False if operator clearance needed or terminal block issued."
        ),
    )
    receipt_id: str = Field(
        default="",
        description="Top-level receipt ID for the Step 3.5 pass."
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-blocking advisory messages."
    )
    execution_time_ms: float = Field(
        default=0.0,
        description="Execution time in milliseconds (AC4: < 20ms for skip)."
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
