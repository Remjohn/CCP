"""
CCP FR7 Leadership Scorecard & Coach Development Engine — Data Models (Unit 1)
Pydantic v2 models for DEP-ENG-026 (leadership_scorecard.json).

Spec reference: FR7 Tech Spec §The 12 Leadership Traits, §Phase 3 CATEGORIZE,
                §Phase 4 FORMAT GOVERNANCE, §Phase 5 EMIT, §Weekly Scorecard Evolution
Architecture reference: §6.3 (Minister of Identity), §11.6 (Leadership Trait Governance)

Primary output:
  - DEP-ENG-026: LeadershipScorecard (12-trait map with categories, format governance, evolution)

Scale: 1–10 per trait (distinct from coach_soul.py LeadershipScores which uses 0-100 for genesis quick-scoring).
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ──────────────────────────────────────────────────────────────
# Constants from spec
# ──────────────────────────────────────────────────────────────

# Spec §Phase 2: Score bounds
TRAIT_SCORE_MIN: int = 1
TRAIT_SCORE_MAX: int = 10

# Spec §Phase 4: Format governance ratios
SHOWCASE_RATIO: float = 0.6
EXERCISE_RATIO: float = 0.4

# Spec §Phase 4: Weak/strong thresholds
WEAK_TRAIT_THRESHOLD: int = 5   # score ≤ 5 → exercise
STRONG_TRAIT_THRESHOLD: int = 7  # score ≥ 7 → showcase

# Spec §Weekly Evolution: minimum sessions before evolution applies
MINIMUM_EVOLUTION_SESSIONS: int = 3

# Spec §Weekly Evolution: Sophia alignment threshold for climb
SOPHIA_ALIGNMENT_CLIMB_THRESHOLD: float = 0.85

# Spec §Quarterly Rescoring: weeks between rescores
QUARTERLY_RESCORE_WEEKS: int = 12


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class TraitName(str, Enum):
    """The 12 irreducible leadership traits from MCDA first-principles decomposition.
    Spec §The 12 Leadership Traits table.
    """
    DEEP_EMPATHY = "deep_empathy"
    AUTHENTIC_VULNERABILITY = "authentic_vulnerability"
    EMBODIED_CONFIDENCE = "embodied_confidence"
    EMOTIONAL_DEPTH = "emotional_depth"
    DEVOTIONAL_PASSION = "devotional_passion"
    MYSTIQUE_AND_AURA = "mystique_and_aura"
    ARCHETYPAL_STORYTELLING = "archetypal_storytelling"
    TRANSFORMATION_PROOF = "transformation_proof"
    POLARIZING_CLARITY = "polarizing_clarity"
    EXPANSION_ENERGY = "expansion_energy"
    COMIC_HONESTY = "comic_honesty"
    DIRECTNESS = "directness"


class TraitCategory(str, Enum):
    """5 trait categories for the production lock gate.
    Spec §Phase 3 CATEGORIZE table.
    """
    CORE_PHILOSOPHY = "core_philosophy"
    AUDIENCE_UNDERSTANDING = "audience_understanding"
    VOICE_AUTHENTICITY = "voice_authenticity"
    TEACHING_METHOD = "teaching_method"
    CULTURAL_GROUNDING = "cultural_grounding"


class FormatAssignmentType(str, Enum):
    """Assignment type for a trait's content formats.
    Spec §Phase 4 FORMAT GOVERNANCE.
    """
    EXERCISE = "exercise"
    SHOWCASE = "showcase"
    NEUTRAL = "neutral"


class EvolutionAction(str, Enum):
    """Weekly evolution score actions.
    Spec §Weekly Scorecard Evolution — Score Evolution Logic table.
    """
    CLIMB = "climb"
    HOLD = "hold"
    DECLINE = "decline"


class LeadershipPipelineStepStatus(str, Enum):
    """Pipeline step statuses for FR7."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# ──────────────────────────────────────────────────────────────
# Trait Category → Trait Mapping (from spec §Phase 3)
# ──────────────────────────────────────────────────────────────

CATEGORY_TRAIT_MAP: dict[TraitCategory, list[TraitName]] = {
    TraitCategory.CORE_PHILOSOPHY: [
        TraitName.DEVOTIONAL_PASSION,
        TraitName.EXPANSION_ENERGY,
    ],
    TraitCategory.AUDIENCE_UNDERSTANDING: [
        TraitName.DEEP_EMPATHY,
        TraitName.POLARIZING_CLARITY,
    ],
    TraitCategory.VOICE_AUTHENTICITY: [
        TraitName.AUTHENTIC_VULNERABILITY,
        TraitName.EMBODIED_CONFIDENCE,
        TraitName.DIRECTNESS,
    ],
    TraitCategory.TEACHING_METHOD: [
        TraitName.EMOTIONAL_DEPTH,
        TraitName.ARCHETYPAL_STORYTELLING,
        TraitName.TRANSFORMATION_PROOF,
    ],
    TraitCategory.CULTURAL_GROUNDING: [
        TraitName.MYSTIQUE_AND_AURA,
        TraitName.COMIC_HONESTY,
    ],
}


# ──────────────────────────────────────────────────────────────
# Exercise/Showcase Archetype Mapping (from spec §Phase 4 tables)
# ──────────────────────────────────────────────────────────────

EXERCISE_ARCHETYPE_MAP: dict[TraitName, list[str]] = {
    TraitName.DEEP_EMPATHY: ["story_recognition", "tweet_recognition"],
    TraitName.AUTHENTIC_VULNERABILITY: ["story_transformation", "myth_fear_anxiety"],
    TraitName.EMBODIED_CONFIDENCE: ["tier_list_controversial", "myth_indignation"],
    TraitName.EMOTIONAL_DEPTH: ["comparison_profound", "story_transformation"],
    TraitName.DEVOTIONAL_PASSION: ["myth_empowering", "tweet_conviction"],
    TraitName.MYSTIQUE_AND_AURA: ["reaction_surprising", "comparison_conceptual"],
    TraitName.ARCHETYPAL_STORYTELLING: ["story_transformation", "story_recognition"],
    TraitName.TRANSFORMATION_PROOF: ["listicle_helpful", "comparison_outrageous"],
    TraitName.POLARIZING_CLARITY: ["myth_indignation", "tier_list_controversial"],
    TraitName.EXPANSION_ENERGY: ["listicle_helpful", "tweet_wisdom"],
    TraitName.COMIC_HONESTY: ["reaction_funny", "tweet_recognition"],
    TraitName.DIRECTNESS: ["tweet_warning", "myth_indignation"],
}

SHOWCASE_ARCHETYPE_MAP: dict[TraitName, list[str]] = {
    TraitName.DEEP_EMPATHY: ["story_recognition", "myth_fear_anxiety"],
    TraitName.AUTHENTIC_VULNERABILITY: ["story_transformation"],
    TraitName.EMBODIED_CONFIDENCE: ["myth_indignation", "tier_list_controversial"],
    TraitName.EMOTIONAL_DEPTH: ["comparison_profound", "story_transformation"],
    TraitName.DEVOTIONAL_PASSION: ["myth_empowering", "tweet_conviction"],
    TraitName.MYSTIQUE_AND_AURA: ["reaction_surprising", "comparison_shocking"],
    TraitName.ARCHETYPAL_STORYTELLING: [
        "story_transformation", "story_recognition",
        "story_fear_anxiety", "story_empowering",
    ],
    TraitName.TRANSFORMATION_PROOF: ["listicle_shocking", "comparison_outrageous"],
    TraitName.POLARIZING_CLARITY: ["myth_indignation", "tier_list_controversial"],
    TraitName.EXPANSION_ENERGY: ["listicle_helpful", "tweet_wisdom"],
    TraitName.COMIC_HONESTY: ["reaction_funny", "tweet_recognition"],
    TraitName.DIRECTNESS: ["tweet_warning", "myth_indignation"],
}


# ──────────────────────────────────────────────────────────────
# Evidence Model
# ──────────────────────────────────────────────────────────────

class TraitEvidence(BaseModel):
    """A single evidence citation supporting a trait score.
    Spec §Phase 2: 'Every score MUST have a specific evidence quote.'
    """
    signal_source: str = Field(
        ...,
        description="DEP-ID or source name that the evidence came from",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Evidence description or quote from the signal source",
    )
    rubric_points: int = Field(
        default=0,
        ge=0,
        description="Points contributed by this evidence per rubric table",
    )


# ──────────────────────────────────────────────────────────────
# Trait History Entry (for weekly evolution)
# ──────────────────────────────────────────────────────────────

class TraitHistoryEntry(BaseModel):
    """A single entry in a trait's evolution history.
    Spec §Weekly Scorecard Evolution — Evolution Data.
    """
    session_id: str = Field(..., description="Weekly session identifier (e.g. weekly_session_2026-W12)")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    previous_score: int = Field(..., ge=TRAIT_SCORE_MIN, le=TRAIT_SCORE_MAX)
    new_score: int = Field(..., ge=TRAIT_SCORE_MIN, le=TRAIT_SCORE_MAX)
    action: EvolutionAction = Field(..., description="climb/hold/decline")
    formats_assigned: list[str] = Field(default_factory=list)
    assignment_type: FormatAssignmentType = Field(default=FormatAssignmentType.NEUTRAL)
    sophia_alignment: float = Field(default=0.0, ge=0.0, le=1.0)
    chen_detection: float = Field(default=0.0, ge=0.0, le=1.0)
    audience_engagement_7d: Optional[float] = Field(default=None)
    coach_average_engagement: Optional[float] = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def preprocess_history_entry(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Default previous_score and new_score to 5 if missing or None
            if "previous_score" not in data or data["previous_score"] is None:
                data["previous_score"] = 5
            if "new_score" not in data or data["new_score"] is None:
                data["new_score"] = 5
                
            # Handle boolean to float conversion for chen_detection
            chen = data.get("chen_detection")
            if isinstance(chen, bool):
                data["chen_detection"] = 1.0 if chen else 0.0
                
            # Handle boolean to float conversion for sophia_alignment
            sophia = data.get("sophia_alignment")
            if isinstance(sophia, bool):
                data["sophia_alignment"] = 1.0 if sophia else 0.0
        return data


# ──────────────────────────────────────────────────────────────
# Scored Trait
# ──────────────────────────────────────────────────────────────

class ScoredTrait(BaseModel):
    """A single scored leadership trait for DEP-ENG-026.
    Spec §Phase 5 EMIT — traits array schema.
    """
    trait_id: int = Field(..., ge=1, le=12)
    name: TraitName = Field(...)
    label: str = Field(..., description="Human-readable trait label")
    score: int = Field(..., ge=TRAIT_SCORE_MIN, le=TRAIT_SCORE_MAX)
    max_score: int = Field(default=TRAIT_SCORE_MAX)
    evidence: list[TraitEvidence] = Field(default_factory=list)
    category: TraitCategory = Field(...)
    format_assignment: FormatAssignmentType = Field(default=FormatAssignmentType.NEUTRAL)
    exercise_archetypes: list[str] = Field(default_factory=list)
    showcase_archetypes: list[str] = Field(default_factory=list)
    history: list[TraitHistoryEntry] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def resolve_trait_id(cls, data: Any) -> Any:
        if isinstance(data, dict):
            trait_id = data.get("trait_id")
            name = data.get("name")
            
            # Simple direct name-to-id mapping inside the validator to prevent forward reference issues
            name_to_id = {
                "deep_empathy": 1,
                "authentic_vulnerability": 2,
                "embodied_confidence": 3,
                "emotional_depth": 4,
                "devotional_passion": 5,
                "mystique_and_aura": 6,
                "archetypal_storytelling": 7,
                "transformation_proof": 8,
                "polarizing_clarity": 9,
                "expansion_energy": 10,
                "comic_honesty": 11,
                "directness": 12,
            }
            
            if trait_id is not None:
                if isinstance(trait_id, str):
                    if trait_id.isdigit():
                        data["trait_id"] = int(trait_id)
                    else:
                        val = trait_id.lower()
                        if val in name_to_id:
                            data["trait_id"] = name_to_id[val]
                elif hasattr(trait_id, "value") and isinstance(trait_id.value, str):
                    val = trait_id.value.lower()
                    if val in name_to_id:
                        data["trait_id"] = name_to_id[val]
            
            if (data.get("trait_id") is None or not isinstance(data.get("trait_id"), int)) and name is not None:
                val = None
                if isinstance(name, str):
                    val = name.lower()
                elif hasattr(name, "value") and isinstance(name.value, str):
                    val = name.value.lower()
                if val and val in name_to_id:
                    data["trait_id"] = name_to_id[val]
        return data

    @field_validator("evidence")
    @classmethod
    def evidence_not_empty(cls, v: list[TraitEvidence]) -> list[TraitEvidence]:
        """Spec §Phase 6 VALIDATE: 'Every score has ≥1 evidence citation.'
        AC3: 'A trait scored 7/10 with zero evidence citations → validation error.'
        """
        if len(v) < 1:
            raise ValueError(
                "Every trait score must have ≥1 evidence citation (AC3)"
            )
        return v


# ──────────────────────────────────────────────────────────────
# Category Coverage Result
# ──────────────────────────────────────────────────────────────

class CategoryCoverageResult(BaseModel):
    """Coverage evaluation for a single trait category.
    Spec §Phase 3 CATEGORIZE table.
    """
    category: TraitCategory = Field(...)
    traits: list[TraitName] = Field(default_factory=list)
    coverage_met: bool = Field(default=False)
    threshold_description: str = Field(
        default="",
        description="Human-readable description of the coverage requirement",
    )
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional evaluation details (trait scores, CMM layer count, etc.)",
    )

    @model_validator(mode="before")
    @classmethod
    def preprocess_coverage_result(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. Handle traits list containing ScoredTrait or similar objects
            traits = data.get("traits")
            if isinstance(traits, list):
                new_traits = []
                for t in traits:
                    if isinstance(t, str):
                        new_traits.append(t)
                    elif hasattr(t, "name"):
                        new_traits.append(t.name)
                    elif isinstance(t, dict) and "name" in t:
                        new_traits.append(t["name"])
                    else:
                        new_traits.append(t)
                data["traits"] = new_traits
            
            # 2. Handle details field if it is passed as a string or empty/None
            details = data.get("details")
            if isinstance(details, str):
                if details:
                    data["details"] = {"info": details}
                else:
                    data["details"] = {}
            elif details is None:
                data["details"] = {}
        return data


# ──────────────────────────────────────────────────────────────
# Production Lock Result
# ──────────────────────────────────────────────────────────────

class ProductionLockResult(BaseModel):
    """Production lock gate evaluation result.
    Spec §Phase 6 VALIDATE — Production lock enforcement.
    """
    all_categories_met: bool = Field(default=False)
    locked_categories: list[str] = Field(
        default_factory=list,
        description="Category names that failed coverage",
    )
    unlock_message: str = Field(default="")
    error_code: str = Field(
        default="",
        description="PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD or PRODUCTION_LOCKED_CATEGORY_INCOMPLETE",
    )


# ──────────────────────────────────────────────────────────────
# Format Governance
# ──────────────────────────────────────────────────────────────

class FormatGovernance(BaseModel):
    """Format governance configuration for the scorecard.
    Spec §Phase 4 FORMAT GOVERNANCE.
    """
    showcase_ratio: float = Field(default=SHOWCASE_RATIO)
    exercise_ratio: float = Field(default=EXERCISE_RATIO)
    assignments_written_to: str = Field(default="02_content_strategy.md")


# ──────────────────────────────────────────────────────────────
# Signal Source Availability
# ──────────────────────────────────────────────────────────────

class SignalSourceAvailability(BaseModel):
    """Tracks which signal sources were available during scoring.
    Spec §Phase 5 EMIT — signal_sources field.
    """
    coach_soul: bool = Field(default=False)
    ttt_baseline: bool = Field(default=False)
    tribe_soul: bool = Field(default=False)
    cultural_memory_map: bool = Field(default=False)
    coach_story_archive: bool = Field(default=False)
    philosophy_brief: bool = Field(default=False)


# ──────────────────────────────────────────────────────────────
# Weekly Session Performance Data (input for evolution)
# ──────────────────────────────────────────────────────────────

class TraitSessionPerformance(BaseModel):
    """Performance data for a single trait in a weekly session.
    Spec §Weekly Scorecard Evolution — Evolution Data.
    """
    trait_name: TraitName = Field(...)
    formats_assigned: list[str] = Field(default_factory=list)
    assignment_type: FormatAssignmentType = Field(default=FormatAssignmentType.NEUTRAL)
    sophia_alignment: float = Field(default=0.0, ge=0.0, le=1.0)
    chen_detection: float = Field(default=0.0, ge=0.0, le=1.0)
    audience_engagement_7d: Optional[float] = Field(default=None)


class WeeklySessionData(BaseModel):
    """Complete weekly session performance data.
    Spec §Weekly Scorecard Evolution — Evolution Data.
    """
    session_id: str = Field(..., description="e.g. weekly_session_2026-W12")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    trait_updates: list[TraitSessionPerformance] = Field(default_factory=list)
    coach_average_engagement: Optional[float] = Field(
        default=None,
        description="Coach's average engagement metric across all content",
    )


# ──────────────────────────────────────────────────────────────
# DEP-ENG-026: Leadership Scorecard (PRIMARY OUTPUT)
# ──────────────────────────────────────────────────────────────

class LeadershipScorecard(BaseModel):
    """The complete Leadership Scorecard — DEP-ENG-026.
    Spec §Phase 5 EMIT — full JSON schema.

    This is the primary output of FR7: the 12-trait leadership map that
    governs content format assignment in the production pipeline.
    """
    dep_id: str = Field(default="DEP-ENG-026")
    version: str = Field(default="1.0")
    coach_id: str = Field(default="", description="Coach person ID (CCC-0000)")
    scored_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 timestamp of initial scoring",
    )
    last_updated: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 timestamp of last update",
    )
    created_at: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp of creation (optional)",
    )
    signal_sources: SignalSourceAvailability = Field(
        default_factory=SignalSourceAvailability,
    )
    traits: list[ScoredTrait] = Field(
        default_factory=list,
        description="All 12 scored traits",
    )
    categories: dict[str, CategoryCoverageResult] = Field(
        default_factory=dict,
        description="5 category coverage evaluations keyed by category name",
    )
    production_lock: ProductionLockResult = Field(
        default_factory=ProductionLockResult,
    )
    format_governance: FormatGovernance = Field(
        default_factory=FormatGovernance,
    )

    @field_validator("traits")
    @classmethod
    def validate_trait_count(cls, v: list[ScoredTrait]) -> list[ScoredTrait]:
        """Spec §Phase 6: 'All 12 traits have a score between 1 and 10.'"""
        if len(v) != 0 and len(v) != 12:
            raise ValueError(
                f"Scorecard must contain exactly 12 traits, got {len(v)}"
            )
        return v

    def get_trait_by_name(self, name: TraitName) -> Optional[ScoredTrait]:
        """Look up a scored trait by its enum name."""
        for trait in self.traits:
            if trait.name == name:
                return trait
        return None

    def get_weak_traits(self, threshold: int = WEAK_TRAIT_THRESHOLD) -> list[ScoredTrait]:
        """Return traits scoring at or below the threshold (exercise targets)."""
        return [t for t in self.traits if t.score <= threshold]

    def get_strong_traits(self, threshold: int = STRONG_TRAIT_THRESHOLD) -> list[ScoredTrait]:
        """Return traits scoring at or above the threshold (showcase targets)."""
        return [t for t in self.traits if t.score >= threshold]

    def dominant_trait(self) -> Optional[ScoredTrait]:
        """Return the highest-scoring trait."""
        if not self.traits:
            return None
        return max(self.traits, key=lambda t: t.score)


# ──────────────────────────────────────────────────────────────
# Trait ID → Metadata Mapping
# ──────────────────────────────────────────────────────────────

TRAIT_REGISTRY: list[dict[str, Any]] = [
    {"trait_id": 1, "name": TraitName.DEEP_EMPATHY, "label": "Deep Empathy", "category": TraitCategory.AUDIENCE_UNDERSTANDING},
    {"trait_id": 2, "name": TraitName.AUTHENTIC_VULNERABILITY, "label": "Authentic Vulnerability", "category": TraitCategory.VOICE_AUTHENTICITY},
    {"trait_id": 3, "name": TraitName.EMBODIED_CONFIDENCE, "label": "Embodied Confidence", "category": TraitCategory.VOICE_AUTHENTICITY},
    {"trait_id": 4, "name": TraitName.EMOTIONAL_DEPTH, "label": "Emotional Depth", "category": TraitCategory.TEACHING_METHOD},
    {"trait_id": 5, "name": TraitName.DEVOTIONAL_PASSION, "label": "Devotional Passion", "category": TraitCategory.CORE_PHILOSOPHY},
    {"trait_id": 6, "name": TraitName.MYSTIQUE_AND_AURA, "label": "Mystique & Aura", "category": TraitCategory.CULTURAL_GROUNDING},
    {"trait_id": 7, "name": TraitName.ARCHETYPAL_STORYTELLING, "label": "Archetypal Storytelling", "category": TraitCategory.TEACHING_METHOD},
    {"trait_id": 8, "name": TraitName.TRANSFORMATION_PROOF, "label": "Transformation Proof", "category": TraitCategory.TEACHING_METHOD},
    {"trait_id": 9, "name": TraitName.POLARIZING_CLARITY, "label": "Polarizing Clarity", "category": TraitCategory.AUDIENCE_UNDERSTANDING},
    {"trait_id": 10, "name": TraitName.EXPANSION_ENERGY, "label": "Expansion Energy", "category": TraitCategory.CORE_PHILOSOPHY},
    {"trait_id": 11, "name": TraitName.COMIC_HONESTY, "label": "Comic Honesty", "category": TraitCategory.CULTURAL_GROUNDING},
    {"trait_id": 12, "name": TraitName.DIRECTNESS, "label": "Directness", "category": TraitCategory.VOICE_AUTHENTICITY},
]


# ──────────────────────────────────────────────────────────────
# Pipeline Session Model
# ──────────────────────────────────────────────────────────────

class LeadershipScorecardPipelineSession(BaseModel):
    """Tracks the state of a complete FR7 pipeline execution."""
    coach_id: str = Field(default="")
    coach_acronym: str = Field(default="", min_length=3, max_length=3)
    started_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    completed_at: Optional[str] = Field(default=None)
    step_statuses: dict[str, LeadershipPipelineStepStatus] = Field(
        default_factory=lambda: {
            "ingest": LeadershipPipelineStepStatus.PENDING,
            "score": LeadershipPipelineStepStatus.PENDING,
            "categorize": LeadershipPipelineStepStatus.PENDING,
            "format_governance": LeadershipPipelineStepStatus.PENDING,
            "emit": LeadershipPipelineStepStatus.PENDING,
            "validate": LeadershipPipelineStepStatus.PENDING,
        },
    )
    ingest_receipt_id: Optional[str] = Field(default=None)
    complete_receipt_id: Optional[str] = Field(default=None)
    scorecard: Optional[LeadershipScorecard] = Field(default=None)
    error: Optional[str] = Field(default=None)
