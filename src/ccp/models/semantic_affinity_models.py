"""
CCP FR19 Semantic Affinity Guard Protocol — Data Models (Unit 1)
Pydantic v2 models for DEP-PROTO-011 (Semantic Affinity Guard execution log).

Spec reference: FR19_Semantic_Affinity_Guard_Tech_Spec.md
Architecture reference: Mood_State_Architecture_Documentation §Section 05

DEP-PROTO-011: Semantic Affinity Guard — ENFORCER protocol.
               Gate C-06: Escape Mode + HIGH affinity = FAIL_TERMINAL.
               Processing Mode + HIGH affinity = PASS (faces pain directly).
               MEDIUM affinity = Operator Review queue.
               LOW affinity = PASS.

Academic grounding:
  Mood Management Theory / Semantic Affinity (Zillmann 1988):
  HIGH semantic affinity between content domain and active stress domain
  prevents mood repair and heightens anxiety during Escape content.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Enums ────────────────────────────────────────────────────────────────────


class AffinityRating(str, Enum):
    """Semantic affinity rating between content domain and L3 pain domain.

    Spec §4 Stage 2 verdicts:
      LOW    — entirely separate domains → Proceed
      MEDIUM — adjacent but distinct → Flag for Operator Review
      HIGH   — exact L3 semantic vocabulary overlap → Hard Block (Escape only)
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class C06Clearance(str, Enum):
    """Gate C-06 clearance status per batch slot.

    Spec §4 Stage 3:
      PASS          — slot cleared for compilation
      FAIL_TERMINAL — Escape + HIGH → compilation halted, no bypass possible
      OPERATOR_REVIEW — MEDIUM → sent to operator queue for manual validation
    """
    PASS = "PASS"
    FAIL_TERMINAL = "FAIL_TERMINAL"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"


class BatchClearanceStatus(str, Enum):
    """Overall batch clearance status from the Semantic Affinity Guard.

    Spec §5 Output Schema: batch_clearance_status.
    """
    CLEARED = "CLEARED"
    BLOCKED = "BLOCKED"
    PENDING_REVIEW = "PENDING_REVIEW"


class MoodMode(str, Enum):
    """Content mood mode classification for batch slots.

    Spec §3 Technical Decisions:
      Escape     — HIGH affinity → FAIL_TERMINAL (C-06 kill switch)
      Processing — HIGH affinity → PASS (faces pain directly, productive)
      Status     — MEDIUM tolerated → Operator Review
      Discovery  — MEDIUM tolerated → Operator Review
    """
    ESCAPE = "Escape"
    PROCESSING = "Processing"
    STATUS = "Status"
    DISCOVERY = "Discovery"


class C06ResolutionPath(str, Enum):
    """Mandated resolution paths when C-06 triggers a terminal block.

    Spec §4 Stage 3 Step 3:
      Resolution A: Mutate template (domain swap to distant semantic field)
      Resolution B: Reclassify as Processing Mode (FR18 re-executes automatically)
    """
    DOMAIN_SWAP = "RESOLUTION_A_DOMAIN_SWAP"
    RECLASSIFY_PROCESSING = "RESOLUTION_B_RECLASSIFY_PROCESSING"


# ─── Input Models ─────────────────────────────────────────────────────────────


class BatchSlot(BaseModel):
    """A single content slot in the batch composition.

    Represents one item tagged with a mood_state for the semantic affinity check.
    """
    slot_id: int = Field(description="Batch slot sequential identifier.")
    intended_mode: MoodMode = Field(description="Mood mode assigned by the batch composer.")
    content_domain: str = Field(
        description="Textual description of the content's conceptual domain."
    )
    archetype_id: Optional[str] = Field(
        default=None,
        description="Content archetype identifier (optional context).",
    )


class BatchMetadata(BaseModel):
    """Batch composition metadata — input for the Semantic Affinity Guard.

    Contains all slots to be evaluated by the guard protocol.
    """
    batch_id: str = Field(description="Unique batch identifier.")
    coach_id: str = Field(description="Coach ID — ADR-01 single-tenant isolation (AC4).")
    slots: list[BatchSlot] = Field(
        description="All content slots in the batch for evaluation."
    )


class PainMapInput(BaseModel):
    """Simplified pain map input derived from DEP-ENG-006 (Context Premise Map).

    The guard needs the active L3 pain domain narrative for distance calculation.
    """
    coach_id: str = Field(description="Coach ID — ADR-01 isolation (AC4).")
    active_l3_pain_domain: str = Field(
        description=(
            "Active L3 pain domain narrative text from DEP-ENG-006. "
            "This is the domain the audience is currently suffering in."
        )
    )
    l2_pain_domains: list[str] = Field(
        default_factory=list,
        description="L2 pain domain list for adjacency checks (MEDIUM detection).",
    )
    l1_pain_domains: list[str] = Field(
        default_factory=list,
        description="L1 broad pain categories.",
    )


# ─── Output Models ────────────────────────────────────────────────────────────


class SlotEvaluation(BaseModel):
    """Evaluation result for a single batch slot.

    Spec §5 Output Schema: batch_evaluation array item.
    """
    slot_id: int = Field(description="Batch slot identifier.")
    intended_mode: MoodMode = Field(description="Mood mode of the slot.")
    content_domain: str = Field(description="Content domain text.")
    affinity_rating: AffinityRating = Field(
        description="Computed semantic affinity rating."
    )
    c06_clearance: C06Clearance = Field(
        description="Gate C-06 clearance verdict for this slot."
    )
    affinity_score: float = Field(
        default=0.0,
        description="Raw affinity score (0.0–1.0) before enum bucketing.",
    )
    resolution_paths: list[C06ResolutionPath] = Field(
        default_factory=list,
        description="Available resolution paths if FAIL_TERMINAL.",
    )


class SemanticAffinityClearance(BaseModel):
    """DEP-PROTO-011 — Semantic Affinity Guard execution log.

    Spec §5 Output Schema: semantic_affinity_clearance.json.
    """
    protocol_id: str = Field(
        default="DEP-PROTO-011",
        description="Protocol identifier.",
    )
    receipt_chain_hash: str = Field(
        default="",
        description="Hash from the final receipt write.",
    )
    tenant_id: str = Field(
        description="Coach/tenant identifier — ADR-01 isolation.",
    )
    active_l3_pain_domain: str = Field(
        description="Active L3 pain domain used for evaluation.",
    )
    batch_evaluation: list[SlotEvaluation] = Field(
        default_factory=list,
        description="Per-slot evaluation results.",
    )
    batch_clearance_status: BatchClearanceStatus = Field(
        description="Overall batch clearance: CLEARED, BLOCKED, or PENDING_REVIEW.",
    )
    is_fallback: bool = Field(
        default=False,
        description="True if NLP module was unavailable and PROVISIONAL_MEDIUM was used.",
    )
    operator_warning: Optional[str] = Field(
        default=None,
        description="Warning message if fallback state was triggered.",
    )


# ─── Constants ─────────────────────────────────────────────────────────────────

# Affinity score thresholds for enum bucketing
AFFINITY_THRESHOLD_HIGH = 0.75
"""Score ≥ 0.75 → HIGH affinity (exact L3 vocabulary overlap)."""

AFFINITY_THRESHOLD_MEDIUM = 0.40
"""Score ≥ 0.40 and < 0.75 → MEDIUM affinity (adjacent but distinct)."""

# Below 0.40 → LOW affinity (entirely separate domains)

# Fallback state when NLP module crashes (spec §6)
PROVISIONAL_MEDIUM_WARNING = (
    "OPERATOR_WARNING: NLP Domain Mapping module unavailable. "
    "All Escape slots degraded to PROVISIONAL_MEDIUM and sent to Operator Queue. "
    "No Escape slot will auto-pass until NLP is restored."
)
