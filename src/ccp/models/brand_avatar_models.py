"""
CCP Pydantic Models — Brand Avatar Architecture (FR0E)
Avatar Schema + Content-Context Routing.

Consumed by:
- FR50 (Visual Composition)
- FR-VIS-03
- FR54
- Semiotic Composer (routing integration)

Spec reference: FR0E_Brand_Avatar_Tech_Spec.md
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class SituationCategory(str, Enum):
    """Avatar situation categories — stages of professional evolution."""
    MENTOR = "mentor"
    STRUGGLER = "struggler"
    REBEL = "rebel"
    ORIGIN = "origin"


class CopingStage(str, Enum):
    """Audience coping trajectory position."""
    SEARCH = "search"        # Peak receptivity
    ACTIVE = "active"        # Executing
    EXHAUSTED = "exhausted"  # Depleted


class AvatarEmotionalMode(str, Enum):
    """Content emotional modes for routing."""
    TENSION = "T"
    VULNERABILITY = "V"
    RECOGNITION = "R"
    PROCESSING = "processing"
    DISCOVERY = "discovery"
    STATUS = "status"
    ESCAPE = "escape"


# ──────────────────────────────────────────────────────────────
# Brand Avatar Entry
# ──────────────────────────────────────────────────────────────

class BrandAvatarEntry(BaseModel):
    """A single brand avatar — a narrative situation from the coach's Hero's Journey."""
    avatar_id: str = Field(default="")
    coach_id: str = Field(default="")
    situation_category: SituationCategory = Field(...)
    emotional_state: str = Field(
        ...,
        description="Precise situational description — not generic 'stressed' but contextual",
    )
    wardrobe_and_styling: str = Field(
        default="",
        description="Context-appropriate appearance for image generation",
    )
    contextual_setting: str = Field(
        default="",
        description="Environment reflecting the narrative situation",
    )
    coping_trajectory_routing: list[str] = Field(
        default_factory=list,
        description="Audience coping stages where this avatar is contextually appropriate",
    )
    emotional_mode_routing: list[str] = Field(
        default_factory=list,
        description="Content emotional modes where this avatar activates",
    )
    source_transcript: str = Field(
        default="",
        description="Reference to authenticated story corpus source",
    )
    source_timestamp: str = Field(
        default="",
        description="Timestamp in source transcript where this moment is traced",
    )


# ──────────────────────────────────────────────────────────────
# Content-Context Routing
# ──────────────────────────────────────────────────────────────

class RoutingQuery(BaseModel):
    """Content-Context Routing query."""
    coping_stage: CopingStage = Field(...)
    emotional_mode: str = Field(...)


class RoutingResult(BaseModel):
    """Content-Context Routing result."""
    recommended_avatar: Optional[BrandAvatarEntry] = Field(default=None)
    situation_category: SituationCategory = Field(...)
    rationale: str = Field(default="")
    all_candidates: list[BrandAvatarEntry] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Content-Context Routing Table (from spec §Content-Context Routing V2)
# ──────────────────────────────────────────────────────────────

ROUTING_TABLE: list[dict[str, Any]] = [
    {
        "coping_stage": CopingStage.SEARCH,
        "emotional_modes": ["processing", "discovery"],
        "avatar": SituationCategory.MENTOR,
        "rationale": "Authority figure — wisdom receiver frame",
    },
    {
        "coping_stage": CopingStage.SEARCH,
        "emotional_modes": ["T"],
        "avatar": SituationCategory.REBEL,
        "rationale": "Defiance resonance — fight validation",
    },
    {
        "coping_stage": CopingStage.ACTIVE,
        "emotional_modes": ["discovery", "status"],
        "avatar": SituationCategory.MENTOR,
        "rationale": "Path confirmation — authority validates current action",
    },
    {
        "coping_stage": CopingStage.ACTIVE,
        "emotional_modes": ["R"],
        "avatar": SituationCategory.ORIGIN,  # Nostalgic equivalent → peer-level
        "rationale": "Peer-level celebration rather than authority validation",
    },
    {
        "coping_stage": CopingStage.EXHAUSTED,
        "emotional_modes": ["V"],
        "avatar": SituationCategory.STRUGGLER,
        "rationale": "Depth-match — someone has been exactly here",
    },
    {
        "coping_stage": CopingStage.EXHAUSTED,
        "emotional_modes": ["escape"],
        "avatar": SituationCategory.ORIGIN,
        "rationale": "Lightness — return to before the weight accumulated",
    },
    {
        # Any stage + Tension (tribal) → Rebel
        "coping_stage": None,  # Any
        "emotional_modes": ["T"],
        "avatar": SituationCategory.REBEL,
        "rationale": "Righteous indignation validation",
    },
]


def route_avatar(coping_stage: CopingStage, emotional_mode: str) -> tuple[SituationCategory, str]:
    """Content-Context Routing function.

    Deterministic: given coping stage + emotional mode → recommended avatar.
    """
    # Try specific match first
    for rule in ROUTING_TABLE:
        if rule["coping_stage"] is not None and rule["coping_stage"] != coping_stage:
            continue
        if emotional_mode in rule["emotional_modes"]:
            return rule["avatar"], rule["rationale"]

    # Fallback to any-stage rules
    for rule in ROUTING_TABLE:
        if rule["coping_stage"] is None and emotional_mode in rule["emotional_modes"]:
            return rule["avatar"], rule["rationale"]

    # Default fallback
    return SituationCategory.MENTOR, "Default — mentor is safe fallback"


# ──────────────────────────────────────────────────────────────
# Narrative Authenticity Test
# ──────────────────────────────────────────────────────────────

class AuthenticityTestResult(BaseModel):
    """Result of the Narrative Authenticity Test for one avatar."""
    avatar_category: SituationCategory = Field(...)
    passed: bool = Field(...)
    reason: str = Field(default="")


class NarrativeAuthenticityTestResult(BaseModel):
    """Aggregate Narrative Authenticity Test result."""
    total_tested: int = Field(default=0)
    total_passed: int = Field(default=0)
    total_failed: int = Field(default=0)
    failures: list[AuthenticityTestResult] = Field(default_factory=list)
    passed: bool = Field(default=False)


# Generic emotional state phrases that fail the Narrative Authenticity Test
GENERIC_EMOTIONAL_PHRASES = [
    "feeling overwhelmed",
    "feeling stressed",
    "under pressure",
    "burned out",
    "working hard",
    "trying to succeed",
    "dealing with challenges",
    "facing difficulties",
    "struggling with",
    "feeling anxious",
]


# ──────────────────────────────────────────────────────────────
# Brand Avatar Collection — Complete output
# ──────────────────────────────────────────────────────────────

class BrandAvatarCollection(BaseModel):
    """Complete Brand Avatar collection (FR0E output).

    Stored as entries in character_lexicon with routing metadata.
    """
    coach_id: str = Field(...)
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    dep_id: str = Field(default="BRAND-AVATARS")
    version: int = Field(default=1, ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    avatars: list[BrandAvatarEntry] = Field(default_factory=list)
    authenticity_test: Optional[NarrativeAuthenticityTestResult] = Field(default=None)
    routing_function_registered: bool = Field(default=False)

    def get_by_category(self, category: SituationCategory) -> list[BrandAvatarEntry]:
        return [a for a in self.avatars if a.situation_category == category]

    def all_categories_present(self) -> bool:
        """Check all 4 situation categories have at least one avatar."""
        return all(
            len(self.get_by_category(cat)) > 0
            for cat in SituationCategory
        )
