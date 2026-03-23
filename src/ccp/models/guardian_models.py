"""
CCP Pydantic Models — Guardian Agent
FR-GA Task 1/3 — Models for Genesis Mode verdicts, stage results,
and Guardian Agent state management.

These models are consumed by the Guardian Agent orchestrator
(src/ccp/agents/guardian_agent.py) and persisted to the coach's
config directory as JSON.
"""

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class GenesisVerdict(str, Enum):
    """Deterministic verdict for each FR0x stage.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Verdict Logic
    - AUTHENTICATED: All quality gates pass. Full production clearance.
    - PROVISIONAL: Minimum viable quality met. Specific gaps flagged.
    - FAILED: Quality gate not met. Pipeline HALTS.
    """

    AUTHENTICATED = "AUTHENTICATED"
    PROVISIONAL = "PROVISIONAL"
    FAILED = "FAILED"


class GenesisStage(str, Enum):
    """The 5 FR0x stages plus interview and certificate phases.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Genesis Flow
    Strict sequential order: INTERVIEW → FR0A → FR0B → FR0C → FR0D → FR0E → CERTIFICATE
    """

    IDLE = "IDLE"
    INTERVIEW = "INTERVIEW"
    FR0A = "FR0A"  # Business Intelligence Summary
    FR0B = "FR0B"  # Tribe Soul Research
    FR0C = "FR0C"  # Character Lexicon Builder
    FR0D = "FR0D"  # Semiotic Intelligence Library
    FR0E = "FR0E"  # Brand Avatar Generation
    CERTIFICATE = "CERTIFICATE"
    COMPLETE = "COMPLETE"


# Strict sequential order enforced by the orchestrator
GENESIS_STAGE_ORDER: list[GenesisStage] = [
    GenesisStage.INTERVIEW,
    GenesisStage.FR0A,
    GenesisStage.FR0B,
    GenesisStage.FR0C,
    GenesisStage.FR0D,
    GenesisStage.FR0E,
    GenesisStage.CERTIFICATE,
]


class QualityGateResult(BaseModel):
    """Result of a single quality gate check within a stage."""

    gate_name: str = Field(..., description="Name of the quality gate")
    passed: bool = Field(..., description="Whether the gate passed")
    score: Optional[float] = Field(
        default=None,
        description="Numeric score if applicable (e.g., authenticity score)",
    )
    threshold: Optional[float] = Field(
        default=None,
        description="Required threshold for this gate",
    )
    evidence: str = Field(
        default="",
        description="Evidence supporting the pass/fail determination",
    )
    is_provisional_eligible: bool = Field(
        default=False,
        description="If failed, can this gate allow PROVISIONAL status?",
    )


class StageResult(BaseModel):
    """Result of executing a single FR0x stage.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Verdict Logic
    """

    stage_name: GenesisStage = Field(..., description="Which FR0x stage this result is for")
    verdict: GenesisVerdict = Field(..., description="AUTHENTICATED, PROVISIONAL, or FAILED")
    quality_gates_passed: list[str] = Field(
        default_factory=list,
        description="Names of quality gates that passed",
    )
    quality_gates_failed: list[str] = Field(
        default_factory=list,
        description="Names of quality gates that failed",
    )
    provisional_gaps: list[str] = Field(
        default_factory=list,
        description="Specific gaps flagged for PROVISIONAL verdicts",
    )
    quality_gate_results: list[QualityGateResult] = Field(
        default_factory=list,
        description="Detailed results for each quality gate",
    )
    dep_ids_produced: list[str] = Field(
        default_factory=list,
        description="DEP-IDs produced by this stage (e.g., DEP-ENG-050)",
    )
    receipt_id: str = Field(
        default="",
        description="Receipt chain ID for this stage's execution",
    )
    executed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of execution",
    )
    execution_duration_ms: float = Field(
        default=0.0,
        description="Duration of stage execution in milliseconds",
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if stage failed with an exception",
    )


class StageConfig(BaseModel):
    """Configuration for a single Genesis stage.

    Used by the Guardian Agent to know how to execute each FR0x stage.
    """

    stage_name: GenesisStage = Field(..., description="Which stage this config is for")
    description: str = Field(default="", description="Human-readable stage description")
    quality_gates: list[str] = Field(
        default_factory=list,
        description="Names of quality gates to evaluate",
    )
    dep_ids_produced: list[str] = Field(
        default_factory=list,
        description="DEP-IDs this stage produces on success",
    )
    dep_ids_required: list[str] = Field(
        default_factory=list,
        description="DEP-IDs required before this stage can execute",
    )
    skill_path: Optional[str] = Field(
        default=None,
        description="Path to the SKILL.md file for this stage",
    )


class GenesisState(BaseModel):
    """Persistent state of the Guardian Agent's Genesis Mode execution.

    Saved to the coach's config directory for resume capability.
    """

    coach_id: str = Field(..., description="Coach Person ID (CCC-0000)")
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    current_stage: GenesisStage = Field(
        default=GenesisStage.IDLE,
        description="Current position in the genesis pipeline",
    )
    stage_results: dict[str, StageResult] = Field(
        default_factory=dict,
        description="Results keyed by stage name (e.g., 'FR0A' → StageResult)",
    )
    is_halted: bool = Field(
        default=False,
        description="True if pipeline halted due to FAILED verdict",
    )
    halt_reason: Optional[str] = Field(
        default=None,
        description="Stage name that caused the halt",
    )
    started_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="When Genesis Mode was initiated",
    )
    completed_at: Optional[str] = Field(
        default=None,
        description="When Genesis Mode completed (None if still running)",
    )

    def get_next_stage(self) -> Optional[GenesisStage]:
        """Return the next stage to execute, or None if complete/halted."""
        if self.is_halted:
            return None

        try:
            current_idx = GENESIS_STAGE_ORDER.index(self.current_stage)
            if current_idx + 1 < len(GENESIS_STAGE_ORDER):
                return GENESIS_STAGE_ORDER[current_idx + 1]
        except ValueError:
            # IDLE → first stage
            if self.current_stage == GenesisStage.IDLE:
                return GENESIS_STAGE_ORDER[0]
        return None

    def has_any_failed(self) -> bool:
        """Check if any stage resulted in FAILED verdict."""
        return any(
            r.verdict == GenesisVerdict.FAILED
            for r in self.stage_results.values()
        )

    def has_any_provisional(self) -> bool:
        """Check if any stage resulted in PROVISIONAL verdict."""
        return any(
            r.verdict == GenesisVerdict.PROVISIONAL
            for r in self.stage_results.values()
        )

    def all_stages_passed(self) -> bool:
        """Check if all 5 FR0x stages have AUTHENTICATED or PROVISIONAL verdicts."""
        fr_stages = [
            GenesisStage.FR0A.value,
            GenesisStage.FR0B.value,
            GenesisStage.FR0C.value,
            GenesisStage.FR0D.value,
            GenesisStage.FR0E.value,
        ]
        for stage in fr_stages:
            result = self.stage_results.get(stage)
            if result is None:
                return False
            if result.verdict == GenesisVerdict.FAILED:
                return False
        return True
