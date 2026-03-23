"""
CCP FR24 — Autonomous Weekly CCF Pipeline v3.1 Models (DEP-PROTO-014)

Pydantic models for the Weekly Pipeline protocol layer.
Governs the Master Orchestrator (Alex) coordinating 65 agents across
5 phases of the Trigger-First Architecture.

Spec reference: FR24_Weekly_Pipeline_Tech_Spec.md
  §4 — Stage 1: Phase A (Discovery & Trigger Matching)
  §4 — Stage 2: Phase B (Authenticity Gate & Research Synthesis)
  §4 — Stage 3: Phase C (JIT Compilation Mass-Assembly)
  §4 — Stage 3B: Novelty Validation (Agent Grâce)
  §4 — Stage 3C: Reference Template Fallback
  §4 — Stage 4: Phase D (Visual Routing & Critic Validation)
  §5 — weekly_production_batch_v3.json schema
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Enumerations ─────────────────────────────────────────────────────────────

class PipelinePhase(str, Enum):
    """The 5 phases of the Trigger-First weekly pipeline."""

    PHASE_A_DISCOVERY = "PHASE_A_DISCOVERY"
    PHASE_B_RESEARCH = "PHASE_B_RESEARCH"
    PHASE_C_GENERATION = "PHASE_C_GENERATION"
    PHASE_C_NOVELTY = "PHASE_C_NOVELTY"
    PHASE_D_VALIDATION = "PHASE_D_VALIDATION"


class PipelineStatus(str, Enum):
    """Overall pipeline execution status."""

    RUNNING = "RUNNING"
    WAITING_COACH_AUDIO = "WAITING_COACH_AUDIO"
    COMPLETED = "COMPLETED"
    HALTED = "HALTED"
    FAILED_UNRECOVERABLE = "FAILED_UNRECOVERABLE"
    PENDING_UPGRADE = "PENDING_UPGRADE"
    PIPELINE_V30_DEGRADATION = "PIPELINE_V30_DEGRADATION"


class GenerationStatus(str, Enum):
    """Status for an individual script generation slot."""

    GENERATED = "GENERATED"
    REFERENCE_FALLBACK = "REFERENCE_FALLBACK"
    FAILED = "FAILED"
    NOVELTY_FAIL = "NOVELTY_FAIL"
    REWRITE_IN_PROGRESS = "REWRITE_IN_PROGRESS"


class NoveltyVerdict(str, Enum):
    """Agent Grâce novelty check verdict."""

    NOVELTY_PASS = "NOVELTY_PASS"
    NOVELTY_FAIL = "NOVELTY_FAIL"


# ─── Phase Receipt Models ─────────────────────────────────────────────────────

class PhaseReceipt(BaseModel):
    """Receipt record for a single pipeline phase.

    Every phase writes a receipt per FR47 DEP-ENG-041 schema.
    """

    phase: PipelinePhase
    receipt_hash: str = Field(
        ...,
        description="SHA-256 hash for this phase's execution",
    )
    agent_names: str = Field(
        ...,
        description="Agents involved (e.g., 'Alex-Adele-Divine')",
    )
    stage_name: str = Field(
        ...,
        description="Receipt stage name (e.g., 'DISCOVERY-AND-TRIGGER-MATCHING')",
    )
    timestamp: str
    input_payload_hash: str = Field(default="")
    output_payload_hash: str = Field(default="")
    previous_receipt_hash: Optional[str] = Field(default=None)


# ─── Phase A Models ───────────────────────────────────────────────────────────

class TriggerMatchCandidate(BaseModel):
    """A candidate from Phase A trigger matching.

    Spec §4 Stage 1: 2-axis structural mapping (MFT + Temporal)
    between trend vectors and coach's trigger_map.json.
    """

    trigger_key: str = Field(
        ..., description="Key from trigger_map.json"
    )
    trend_topic: str = Field(
        ..., description="Extracted trend from ccf-radar"
    )
    mft_axis_score: float = Field(
        ge=0.0, le=1.0,
        description="Moral Foundations Theory alignment score",
    )
    temporal_axis_score: float = Field(
        ge=0.0, le=1.0,
        description="Temporal relevance score",
    )
    combined_score: float = Field(
        ge=0.0, le=1.0,
        description="Weighted combination of MFT + Temporal",
    )


class PhaseAResult(BaseModel):
    """Output of Phase A: Discovery & Trigger Matching.

    Spec §4 Stage 1: Outputs final_theme_selection.md and
    trigger_matching_candidates.json.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    trigger_match_candidates: list[TriggerMatchCandidate] = Field(
        default_factory=list,
    )
    final_theme_selection: str = Field(
        default="",
        description="The selected theme for this week's content",
    )
    trigger_match_score: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Best trigger match score",
    )
    provocation_text: str = Field(
        default="",
        description="80-word Telegram Provocation sent to coach",
    )
    phase_receipt: Optional[PhaseReceipt] = None


# ─── Phase B Models ───────────────────────────────────────────────────────────

class LIWCAuthenticityResult(BaseModel):
    """Result of the LIWC-22 Authenticity Gate.

    Spec §4 Stage 2: Coach audio must score ≥0.6 on 7 authenticity markers.
    Below threshold → reject + Telegram re-record request.
    """

    composite_score: float = Field(
        ge=0.0, le=1.0,
        description="LIWC-22 composite authenticity score",
    )
    passed: bool = Field(
        ...,
        description="True if composite_score ≥ 0.6",
    )
    rejection_reason: Optional[str] = Field(
        default=None,
        description="Set to 'LIWC_BELOW_THRESHOLD' on failure",
    )
    markers_evaluated: int = Field(
        default=7,
        description="Number of LIWC-22 authenticity markers checked",
    )

    THRESHOLD: float = 0.6

    def model_post_init(self, __context: Any) -> None:
        """Auto-set passed and rejection_reason based on score."""
        self.passed = self.composite_score >= self.THRESHOLD
        if not self.passed:
            self.rejection_reason = "LIWC_BELOW_THRESHOLD"


class PhaseBResult(BaseModel):
    """Output of Phase B: Authenticity Gate & Research Synthesis.

    Spec §4 Stage 2: LIWC-22 gate + ccf-raw-research + ccf-research-deep.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    liwc_result: LIWCAuthenticityResult
    transcript_available: bool = Field(default=False)
    research_pages_generated: int = Field(default=0)
    phase_receipt: Optional[PhaseReceipt] = None


# ─── Phase C Models ───────────────────────────────────────────────────────────

class ScriptSlot(BaseModel):
    """A single slot in the 36-script batch.

    Spec §4 Stage 3: 36 finalized SKILL.md variations across 14 archetypes.
    Stage 3C: If TillDone fails 3 iterations → REFERENCE_FALLBACK.
    """

    slot_id: str = Field(
        ...,
        description="Unique slot identifier (e.g., 'STORY01')",
    )
    skill_id: str = Field(
        default="",
        description="Full Skill Fingerprint ID",
    )
    archetype: str = Field(
        default="",
        description="Archetype assignment for this slot",
    )
    generation_status: GenerationStatus = Field(
        default=GenerationStatus.GENERATED,
    )
    till_done_iterations: int = Field(
        default=0, ge=0, le=3,
        description="Number of TillDone rewrite attempts",
    )
    fallback_fingerprint_id: Optional[str] = Field(
        default=None,
        description="Fingerprint ID of the reference template used in REFERENCE_FALLBACK",
    )
    file_path: str = Field(
        default="",
        description="Path to the generated SKILL.md file",
    )
    validation_scores: Optional[dict[str, float]] = Field(
        default=None,
        description="Sophia/Marcus/Chen scores after validation",
    )


class NoveltyCheckResult(BaseModel):
    """Result from Agent Grâce (Boredom Ban Enforcer).

    Spec §4 Stage 3B: 8-week rolling window novelty check.
    FAIL → TillDone. 3 failures → Reference Template Fallback.
    """

    slot_id: str
    verdict: NoveltyVerdict
    thematic_similarity: float = Field(
        default=0.0, ge=0.0, le=1.0,
    )
    structural_similarity: float = Field(
        default=0.0, ge=0.0, le=1.0,
    )
    semantic_similarity: float = Field(
        default=0.0, ge=0.0, le=1.0,
    )
    rolling_window_weeks: int = Field(default=8)


class PhaseCResult(BaseModel):
    """Output of Phase C: JIT Compilation Mass-Assembly.

    Includes novelty validation and reference fallback results.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    total_slots: int = Field(default=36)
    slots: list[ScriptSlot] = Field(default_factory=list)
    novelty_results: list[NoveltyCheckResult] = Field(default_factory=list)
    c11_persona_masking_passed: bool = Field(
        default=True,
        description="C-11 gate: all 65 agent names scrubbed from API payloads",
    )
    epsilon_greedy_floor: float = Field(
        default=0.05,
        description="5% random-chance selection rate for underperforming structures",
    )
    phase_receipt: Optional[PhaseReceipt] = None


# ─── Phase D Models ───────────────────────────────────────────────────────────

class PhaseDResult(BaseModel):
    """Output of Phase D: Visual Routing & Critic Validation.

    Spec §4 Stage 4: Visual asset generation + Validation Triad.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    total_validated: int = Field(default=0)
    total_approved: int = Field(default=0)
    total_rewritten: int = Field(default=0)
    total_fallback: int = Field(default=0)
    visual_prompts_generated: int = Field(default=0)
    phase_receipt: Optional[PhaseReceipt] = None


# ─── Weekly Batch Payload ─────────────────────────────────────────────────────

class WeeklyBatchPayload(BaseModel):
    """weekly_production_batch_v3.json — the final output.

    Spec §5: Primary Output Schema.
    """

    production_week: str = Field(
        ...,
        description="ISO week format (e.g., '2026-W11')",
    )
    coach_id: str = Field(..., min_length=3, max_length=3)
    pipeline_status: PipelineStatus = Field(
        default=PipelineStatus.COMPLETED,
    )
    trigger_match_score: float = Field(
        default=0.0, ge=0.0, le=1.0,
    )
    authenticity_liwc_composite: float = Field(
        default=0.0, ge=0.0, le=1.0,
    )
    season_mandate: str = Field(
        default="",
        description="Active 30-Day Movement Season (e.g., 'THE_FORGE')",
    )
    receipt_chain_ledger: dict[str, str] = Field(
        default_factory=dict,
        description="Phase-level receipt hash mapping",
    )
    total_generated: int = Field(default=0)
    formats_utilized: int = Field(default=0)
    scripts: list[ScriptSlot] = Field(default_factory=list)
    phase_a: Optional[PhaseAResult] = None
    phase_b: Optional[PhaseBResult] = None
    phase_c: Optional[PhaseCResult] = None
    phase_d: Optional[PhaseDResult] = None


# ─── DamageControl Models ─────────────────────────────────────────────────────

class DamageControlStatus(BaseModel):
    """DamageControl infinite loop breaker status.

    Spec §3 Technical Decision 2: Max retry depth = 3.
    Fourth retry → FAILED_UNRECOVERABLE.
    """

    current_retry: int = Field(default=0, ge=0)
    max_retry_depth: int = Field(default=3)
    is_exhausted: bool = Field(default=False)
    failure_reason: Optional[str] = Field(default=None)

    def increment(self) -> None:
        """Increment retry counter. If exceeds max, mark exhausted."""
        self.current_retry += 1
        if self.current_retry >= self.max_retry_depth:
            self.is_exhausted = True
            self.failure_reason = "FAILED_UNRECOVERABLE"
