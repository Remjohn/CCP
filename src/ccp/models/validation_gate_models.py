"""
CCP FR26 — Validation Team Gate Models (DEP-PROTO-016)

Pydantic models for the triple-pass Validation Gate protocol.
Sophia (Soul), Marcus (Protocol), Chen (Mimicry) — all three must PASS.
Any single FAIL rejects the draft entirely.

Spec reference: FR26_Validation_Gate_Tech_Spec.md
  §4 — Stage 1: Sophia Soul Validation (TTT Drift <15%)
  §4 — Stage 2: Marcus Protocol Validation (100% Season Compliance)
  §4 — Stage 3: Chen Mimicry Validation (AI Artifacts <5%)
  §4 — Stage 4: Orchestration Routing (TillDone Loop, max 3)
  §5 — validation_report.json schema
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Enumerations ─────────────────────────────────────────────────────────────

class ValidatorType(str, Enum):
    """The three validators in the Validation Team Gate."""

    SOPHIA_SOUL = "sophia_soul"
    MARCUS_PROTOCOL = "marcus_protocol"
    CHEN_MIMICRY = "chen_mimicry"


class SeasonMandate(str, Enum):
    """30-Day Movement Season states.

    Spec §4 Stage 2: Marcus enforces the active season.
    """

    DECONSTRUCTION = "DECONSTRUCTION"
    THE_FORGE = "THE_FORGE"
    THE_MIRROR = "THE_MIRROR"
    THE_TRIBE = "THE_TRIBE"


class ValidationFinalVerdict(str, Enum):
    """Final verdict for a script through the validation gate."""

    APPROVED = "APPROVED"
    FAIL_TRIGGER_REWRITE = "FAIL_TRIGGER_REWRITE"
    FAIL_MAX_ITERATIONS = "FAIL_MAX_ITERATIONS"
    REFERENCE_FALLBACK = "REFERENCE_FALLBACK"


# ─── Sophia Models ────────────────────────────────────────────────────────────

class SophiaSoulResult(BaseModel):
    """Sophia's TTT drift validation result.

    Spec §4 Stage 1: Calculates TTT score of generated draft using
    the same extraction algorithm from Genesis. Delta >15% → FAIL.

    Stress Test Decision: Rolling 4-Week Sophia Baseline governs validation.
    Stress Test Decision: Model Offset Coefficient Registry applied before drift calc.
    """

    status: str = Field(
        ...,
        description="PASS or FAIL",
    )
    ttt_drift_percentage: float = Field(
        ..., ge=0.0, le=1.0,
        description="Absolute TTT drift from baseline (0.0-1.0 scale, 0.15 = 15%)",
    )
    drift_threshold: float = Field(
        default=0.15,
        description="Maximum allowed drift: 15%",
    )
    feedback: Optional[str] = Field(
        default=None,
        description="Sophia's precisely worded negative constraints for rewrite",
    )
    baseline_source: str = Field(
        default="rolling_4_week",
        description="Always 'rolling_4_week' per stress test decision",
    )
    model_offset_applied: float = Field(
        default=0.0,
        description="Model-specific TTT offset coefficient from Global Model Offset Registry",
    )

    DRIFT_THRESHOLD: float = 0.15

    def model_post_init(self, __context: Any) -> None:
        """Auto-set status based on drift percentage."""
        self.status = "PASS" if self.ttt_drift_percentage <= self.DRIFT_THRESHOLD else "FAIL"


class SophiaProvisionalPass(BaseModel):
    """Sophia provisional pass when coach_soul.json is missing/corrupted.

    Spec §6: Sophia's pass is PROVISIONAL_PASS, high-priority alert sent.
    Does not block Marcus or Chen.
    """

    provisional: bool = Field(default=True)
    reason: str = Field(default="SOPHIA_BASELINE_MISSING")
    alert_sent: bool = Field(default=False)


# ─── Marcus Models ────────────────────────────────────────────────────────────

class MarcusProtocolResult(BaseModel):
    """Marcus's 30-Day Movement Season compliance result.

    Spec §4 Stage 2: Compliance must be 100%.
    A script using wrong season rhetoric → FAIL.
    """

    status: str = Field(
        ...,
        description="PASS or FAIL",
    )
    active_season: SeasonMandate = Field(
        ...,
        description="The currently active 30-Day Movement Season",
    )
    compliance: float = Field(
        ..., ge=0.0, le=1.0,
        description="1.0 = 100% compliance required for PASS",
    )
    feedback: Optional[str] = Field(
        default=None,
        description="Marcus's structural rewrite constraints",
    )

    def model_post_init(self, __context: Any) -> None:
        """Auto-set status based on compliance."""
        self.status = "PASS" if self.compliance >= 1.0 else "FAIL"


# ─── Chen Models ──────────────────────────────────────────────────────────────

class ChenMimicryResult(BaseModel):
    """Chen's zero-shot AI artifact detection result.

    Spec §4 Stage 3: Artifact score >5% → FAIL.
    Scans for: 'crucial', 'vital', 'navigating', 'in today's busy world',
    symmetrical transitions, unnaturally balanced paragraph lengths.
    """

    status: str = Field(
        ...,
        description="PASS or FAIL",
    )
    artifact_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Detected AI artifact likelihood (0.0-1.0 scale)",
    )
    artifact_threshold: float = Field(
        default=0.05,
        description="Maximum allowed: 5%",
    )
    feedback: Optional[str] = Field(
        default=None,
        description="Chen's flagged AI phrasing responsible for failure",
    )
    ai_tells_found: list[str] = Field(
        default_factory=list,
        description="Specific AI phrases/patterns detected",
    )

    ARTIFACT_THRESHOLD: float = 0.05

    def model_post_init(self, __context: Any) -> None:
        """Auto-set status based on artifact score."""
        self.status = "PASS" if self.artifact_score <= self.ARTIFACT_THRESHOLD else "FAIL"


# ─── Combined Validation Report ───────────────────────────────────────────────

class TriplePassResult(BaseModel):
    """Combined result from the Validation Team Gate.

    Spec §4 Stage 4: ALL three must PASS. Any single FAIL rejects entirely.
    No averaging, no "best 2 out of 3" (AC1).
    """

    script_id: str = Field(
        ...,
        description="Script identifier",
    )
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01: Coach acronym scoping this validation",
    )
    validation_timestamp: str = Field(
        ...,
        description="ISO 8601 UTC timestamp",
    )
    final_verdict: ValidationFinalVerdict
    iteration_count: int = Field(
        default=1, ge=1, le=4,
        description="Current iteration (1 = first attempt, max 3 + 1 final fail)",
    )
    sophia_soul: SophiaSoulResult
    marcus_protocol: MarcusProtocolResult
    chen_mimicry: ChenMimicryResult
    sophia_provisional: Optional[SophiaProvisionalPass] = Field(
        default=None,
        description="Present only when Sophia baseline was missing",
    )


# ─── TillDone Payload ─────────────────────────────────────────────────────────

class TillDonePayload(BaseModel):
    """Payload for the TillDone rewrite cycle.

    Spec §4 Stage 4: Alex merges all Negative Constraints from failed
    checks into a single prompt injection for ccf-generate rewrite.
    """

    script_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    iteration: int = Field(ge=1, le=3)
    max_iterations: int = Field(default=3)
    failed_validators: list[ValidatorType] = Field(
        ...,
        description="Which validators failed this pass",
    )
    merged_negative_constraints: str = Field(
        ...,
        description="Combined rewrite instructions from all failed validators",
    )
    sophia_feedback: Optional[str] = Field(default=None)
    marcus_feedback: Optional[str] = Field(default=None)
    chen_feedback: Optional[str] = Field(default=None)
    is_final_attempt: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        """Auto-set is_final_attempt."""
        self.is_final_attempt = self.iteration >= self.max_iterations


# ─── Validation Report (Output Schema) ────────────────────────────────────────

class ValidationReport(BaseModel):
    """validation_report.json — Spec §5 Primary Output Schema.

    Written per-script after the triple-pass gate.
    """

    script_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    validation_timestamp: str
    final_verdict: ValidationFinalVerdict
    iteration_count: int = Field(default=1, ge=1)
    validators: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Keyed by validator name: sophia_soul, marcus_protocol, chen_mimicry",
    )
    till_done_payload: Optional[str] = Field(
        default=None,
        description="Rewrite instructions when verdict is FAIL_TRIGGER_REWRITE",
    )
    receipt_chain_hash: Optional[str] = Field(
        default=None,
        description="Receipt hash for this validation run",
    )
