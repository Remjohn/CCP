"""
CCP FR20 — Audience Maturity Lifecycle Models (DEP-ENG-017)

Canonical schema for the Audience Maturity Profile produced by
the Maturity-Lifecycle-Engine.

Academic grounding:
    Fredrickson & Joiner 2002 — Broaden-and-Build Theory (Upward Spiral)
    Greenberg et al. 1986 / Burke 2010 — Terror Management Theory

Architecture reference:
    Mood_State_Architecture_Documentation §06
    JIT_Skill_Compiler_Architecture — Adapter 8
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

# Re-export the canonical cohort enum already defined in FR18
from src.ccp.models.psych_routing_models import AudienceMaturityCohort

__all__ = [
    "AudienceMaturityCohort",
    "DepthPermission",
    "TMTFunctionAllowed",
    "BroadenAndBuildStatus",
    "ClassificationMethod",
    "EngagementSignals",
    "BatchAllocation",
    "AudienceMaturityProfile",
    "BATCH_ALLOCATION_MATRIX",
    "DEPTH_PERMISSION_MATRIX",
    "TMT_FUNCTION_MATRIX",
    "BROADEN_BUILD_MATRIX",
]


# ─── Enums ────────────────────────────────────────────────────────────────────


class DepthPermission(str, Enum):
    """Implication phase depth control — spec §4 Stage 2 Variable 2.

    Surface → actionable / immediate only
    Mid     → broader systemic issues
    Full    → deep psychological / existential roots
    """
    SURFACE = "Surface"
    MID = "Mid"
    FULL = "Full"


class TMTFunctionAllowed(str, Enum):
    """Terror Management Theory execution gate — spec §4 Stage 2 Variable 3.

    Greenberg et al. 1986.
    Worldview construction restricted to Loyal; prevents startling New cohorts.
    """
    INSIGHT_DELIVERY_ONLY = "insight_delivery_only"
    WORLDVIEW_CONSTRUCTION_PERMITTED = "worldview_construction_permitted"


class BroadenAndBuildStatus(str, Enum):
    """Fredrickson Upward Spiral lifecycle tracking — spec §4 Stage 2 Variable 4.

    Not_yet_seeded → Escape prime pending before Discovery reward
    Active         → Cognitive scope broadening in progress
    Mature         → Ready for high Processing load without burnout
    """
    NOT_YET_SEEDED = "Not_yet_seeded"
    ACTIVE = "Active"
    MATURE = "Mature"


class ClassificationMethod(str, Enum):
    """How the cohort was determined — spec §4 Stage 1 + §6 Fallback."""
    BEHAVIORAL_OVERRIDE = "BEHAVIORAL_OVERRIDE"
    CALENDAR_FALLBACK = "CALENDAR_FALLBACK"
    CALENDAR_FALLBACK_DEFAULT = "CALENDAR_FALLBACK_DEFAULT"


# ─── Input Models ─────────────────────────────────────────────────────────────


class EngagementSignals(BaseModel):
    """DEP-ENG-042 — Upstream engagement signal feed from FR43 Data Analyst Agent.

    Provides behavioral depth indicators on a rolling 7-day window.
    When entirely unavailable, the engine falls back to calendar age only
    with classification_method = CALENDAR_FALLBACK_DEFAULT.
    """
    coach_id: str = Field(
        ..., min_length=1, description="ADR-01 tenant isolation key."
    )
    save_to_share_ratio: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Saves ÷ shares over rolling 7-day window.",
    )
    dm_vulnerability_ratio: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Fraction of DMs containing vulnerable language markers.",
    )
    account_age_weeks: float = Field(
        ...,
        ge=0.0,
        description="Coach account age in fractional weeks.",
    )


# ─── Batch Allocation ────────────────────────────────────────────────────────


class BatchAllocation(BaseModel):
    """Percentage allocation across the 4 mood states — must total 100.

    Spec §4 Stage 2 Variable 1.
    """
    processing: int = Field(..., ge=0, le=100)
    escape: int = Field(..., ge=0, le=100)
    discovery: int = Field(..., ge=0, le=100)
    status: int = Field(..., ge=0, le=100)

    @field_validator("status")
    @classmethod
    def _total_must_be_100(cls, v: int, info: object) -> int:
        data = info.data if hasattr(info, "data") else {}  # type: ignore[union-attr]
        total = data.get("processing", 0) + data.get("escape", 0) + data.get("discovery", 0) + v
        if total != 100:
            msg = f"Batch allocation must total 100, got {total}"
            raise ValueError(msg)
        return v


# ─── Output Model ─────────────────────────────────────────────────────────────


class AudienceMaturityProfile(BaseModel):
    """DEP-ENG-017 — Master output produced by the Maturity-Lifecycle-Engine.

    Spec §5 Primary Output Schema.
    """
    profile_id: str = Field(
        ..., min_length=1, description="Unique profile evaluation identifier."
    )
    receipt_chain_hash: str = Field(
        ..., min_length=1, description="Cryptographic receipt chain hash."
    )
    tenant_id: str = Field(
        ..., min_length=1, description="ADR-01 coach-scoped tenant key."
    )
    last_evaluation_epoch: int = Field(
        ..., description="UNIX epoch of evaluation timestamp."
    )
    cohort_classification: AudienceMaturityCohort = Field(
        ..., description="Resolved cohort tier (New / Developing / Loyal)."
    )
    classification_method: ClassificationMethod = Field(
        ..., description="How the cohort was determined."
    )
    batch_allocation: BatchAllocation = Field(
        ..., description="Mood-state percentage allocation for batch composition."
    )
    depth_permission: DepthPermission = Field(
        ..., description="Implication phase depth constraint."
    )
    tmt_function_allowed: TMTFunctionAllowed = Field(
        ..., description="TMT gate — worldview construction vs insight only."
    )
    broaden_and_build_status: BroadenAndBuildStatus = Field(
        ..., description="Fredrickson Upward Spiral lifecycle stage."
    )


# ─── Deterministic Expansion Matrices ─────────────────────────────────────────


BATCH_ALLOCATION_MATRIX: dict[AudienceMaturityCohort, BatchAllocation] = {
    AudienceMaturityCohort.NEW: BatchAllocation(
        processing=10, escape=40, discovery=30, status=20,
    ),
    AudienceMaturityCohort.DEVELOPING: BatchAllocation(
        processing=25, escape=35, discovery=20, status=20,
    ),
    AudienceMaturityCohort.LOYAL: BatchAllocation(
        processing=50, escape=20, discovery=15, status=15,
    ),
}

DEPTH_PERMISSION_MATRIX: dict[AudienceMaturityCohort, DepthPermission] = {
    AudienceMaturityCohort.NEW: DepthPermission.SURFACE,
    AudienceMaturityCohort.DEVELOPING: DepthPermission.MID,
    AudienceMaturityCohort.LOYAL: DepthPermission.FULL,
}

TMT_FUNCTION_MATRIX: dict[AudienceMaturityCohort, TMTFunctionAllowed] = {
    AudienceMaturityCohort.NEW: TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY,
    AudienceMaturityCohort.DEVELOPING: TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY,
    AudienceMaturityCohort.LOYAL: TMTFunctionAllowed.WORLDVIEW_CONSTRUCTION_PERMITTED,
}

BROADEN_BUILD_MATRIX: dict[AudienceMaturityCohort, BroadenAndBuildStatus] = {
    AudienceMaturityCohort.NEW: BroadenAndBuildStatus.NOT_YET_SEEDED,
    AudienceMaturityCohort.DEVELOPING: BroadenAndBuildStatus.ACTIVE,
    AudienceMaturityCohort.LOYAL: BroadenAndBuildStatus.MATURE,
}
