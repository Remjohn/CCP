"""
CCP Pydantic Models — Coach Soul Profile
Task 1.03 — Schema for coach_soul.json with full validation.

The coach soul is the unified identity profile that every downstream
agent reads. Voice DNA, leadership scores, coaching philosophy,
tribe archetype, and content tone parameters all live here.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class VoiceDNA(BaseModel):
    """TTT (Tone, Texture, Timing) baseline extracted from Sacred Audio."""

    sentence_rhythm: list[str] = Field(
        default_factory=list,
        description="Patterns in sentence length, cadence, and structure",
    )
    metaphor_patterns: list[str] = Field(
        default_factory=list,
        description="Recurring metaphor families (animals, nature, warfare, etc.)",
    )
    vocabulary_fingerprint: list[str] = Field(
        default_factory=list,
        description="Signature words/phrases the coach uses repeatedly",
    )
    emotional_peak_markers: list[str] = Field(
        default_factory=list,
        description="How the coach builds to and delivers emotional peaks",
    )
    pause_cadence: Optional[str] = Field(
        default=None,
        description="Pattern of pauses — where the coach breathes, hesitates, emphasizes",
    )
    humor_style: Optional[str] = Field(
        default=None,
        description="Self-deprecating, ironic, absurd, dry, warm — extracted from audio",
    )
    ttt_baseline_hash: Optional[str] = Field(
        default=None,
        description="Hash of the TTT baseline used for drift detection",
    )


class IdealClient(BaseModel):
    """Profile of the coach's ideal client archetype."""

    demographics: str = Field(default="", description="Age range, occupation, life stage")
    psychographics: str = Field(
        default="",
        description="Mindset, values, fears, aspirations",
    )
    pain_points: list[str] = Field(
        default_factory=list,
        description="Specific struggles the ideal client faces",
    )
    aspirations: list[str] = Field(
        default_factory=list,
        description="What the ideal client wants to become/achieve",
    )


class LeadershipScores(BaseModel):
    """12-dimension leadership trait scores.

    Each score is 0-100. Weak traits get exercise formats,
    strong traits get showcase formats in content production.
    """

    deep_empathy: int = Field(default=0, ge=0, le=100)
    authentic_vulnerability: int = Field(default=0, ge=0, le=100)
    embodied_confidence: int = Field(default=0, ge=0, le=100)
    strategic_patience: int = Field(default=0, ge=0, le=100)
    radical_honesty: int = Field(default=0, ge=0, le=100)
    grounded_presence: int = Field(default=0, ge=0, le=100)
    visionary_clarity: int = Field(default=0, ge=0, le=100)
    playful_irreverence: int = Field(default=0, ge=0, le=100)
    fierce_compassion: int = Field(default=0, ge=0, le=100)
    sacred_boundaries: int = Field(default=0, ge=0, le=100)
    intuitive_timing: int = Field(default=0, ge=0, le=100)
    sovereign_authority: int = Field(default=0, ge=0, le=100)

    def get_weak_traits(self, threshold: int = 40) -> list[str]:
        """Return trait names scoring below the threshold (exercise targets)."""
        return [
            name
            for name, score in self.model_dump().items()
            if score < threshold
        ]

    def get_strong_traits(self, threshold: int = 70) -> list[str]:
        """Return trait names scoring above the threshold (showcase targets)."""
        return [
            name
            for name, score in self.model_dump().items()
            if score >= threshold
        ]

    def dominant_trait(self) -> str:
        """Return the highest-scoring trait name."""
        scores = self.model_dump()
        return max(scores, key=scores.get)

    def trait_balance_ratio(self) -> float:
        """Return the ratio of strong to total traits (0.0 to 1.0).

        A high ratio means the coach has many developed traits.
        A low ratio means there's significant room for growth.
        """
        scores = list(self.model_dump().values())
        strong = sum(1 for s in scores if s >= 70)
        return strong / len(scores) if scores else 0.0


class ContentTone(BaseModel):
    """Content tone parameters derived from Voice DNA and onboarding."""

    warmth: float = Field(default=0.0, ge=0.0, le=1.0, description="0=cold/clinical, 1=warm/nurturing")
    directness: float = Field(default=0.0, ge=0.0, le=1.0, description="0=gentle/suggestive, 1=blunt/commanding")
    humor_weight: float = Field(default=0.0, ge=0.0, le=1.0, description="0=serious, 1=humor-heavy")
    formality: float = Field(default=0.0, ge=0.0, le=1.0, description="0=conversational, 1=professional")


class CoachSoul(BaseModel):
    """The complete coach identity profile.

    This is the single source of truth for every downstream agent.
    Voice DNA, leadership scores, coaching philosophy, tribe archetype,
    and content tone parameters all live here.
    """

    version: int = Field(default=1, ge=1, description="Profile version number")
    coach_name: str = Field(..., description="Full name of the coach")
    coach_id: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-0000$",
        description="Coach Person ID (CCC-0000)",
    )

    # Voice DNA
    voice_dna: VoiceDNA = Field(
        default_factory=VoiceDNA,
        description="TTT baseline extracted from Sacred Audio",
    )

    # Identity
    coaching_philosophy: str = Field(
        default="",
        description="Core coaching philosophy in the coach's own words",
    )
    core_message: str = Field(
        default="",
        description="The one-sentence message the coach wants the world to hear",
    )
    tribe_archetype: str = Field(
        default="",
        description="The archetype that best describes the coach's tribe",
    )
    ideal_client: IdealClient = Field(
        default_factory=IdealClient,
        description="Profile of the coach's ideal client",
    )

    # Trait Scores
    leadership_scores: LeadershipScores = Field(
        default_factory=LeadershipScores,
        description="12-dimension leadership trait scores",
    )

    # Content Configuration
    content_tone: ContentTone = Field(
        default_factory=ContentTone,
        description="Tone parameters for content generation",
    )
    signature_frameworks: list[str] = Field(
        default_factory=list,
        description="Coach's named frameworks, methods, or models",
    )
    competitive_positioning: str = Field(
        default="",
        description="How this coach is different from others in their niche",
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def bump_version(self) -> None:
        """Increment version and update timestamp. Called on every profile edit."""
        self.version += 1
        self.updated_at = datetime.now()

    def is_genesis_complete(self) -> bool:
        """Check if all required genesis fields have been populated."""
        return all(
            [
                self.voice_dna.ttt_baseline_hash is not None,
                len(self.voice_dna.vocabulary_fingerprint) > 0,
                self.coaching_philosophy != "",
                self.core_message != "",
                self.tribe_archetype != "",
                any(
                    score > 0
                    for score in self.leadership_scores.model_dump().values()
                ),
            ]
        )

    def get_format_assignment_weights(self) -> dict[str, list[str]]:
        """Return format assignment guidance based on leadership scores.

        Weak traits should get 'exercise' formats (more practice).
        Strong traits should get 'showcase' formats (amplification).
        """
        return {
            "exercise": self.leadership_scores.get_weak_traits(),
            "showcase": self.leadership_scores.get_strong_traits(),
        }
