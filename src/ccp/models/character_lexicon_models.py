"""
CCP Pydantic Models — Character Lexicon (FR0C)
65-Character Schema + DEP-PROTO-017 Character Invocation Protocol.

Consumed by:
- FR14 CRAL Research Subsystem (M2-M5)
- FR35/FR36 Content Composition
- Semiotic Composer
- Stewardship Mode (relevance scoring)

Spec reference: FR0C_Character_Lexicon_Tech_Spec.md
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class CharacterCategory(int, Enum):
    """5 functional categories per V2 schema."""
    ASPIRATIONAL_HERO = 1       # 20 entries — figures the tribe wants to become
    NOSTALGIC_ICON = 2          # 15 entries — formative period references
    CREDIBILITY_VALIDATOR = 3   # 10 entries — currently active respected voices
    CAUTIONARY_ENEMY = 4        # 10 entries — wrong path figures
    IDEOLOGICAL_OPPOSITION = 5  # 10 entries — opposing worldview figures


class GazeDirection(str, Enum):
    """Gaze direction for visual deployment."""
    HOOK_ZONE = "hook_zone"
    ACTION_ZONE = "action_zone"


class MoralFoundation(str, Enum):
    """Moral Foundations Theory (MFT) — 6 foundations."""
    CARE_HARM = "care_harm"
    FAIRNESS_CHEATING = "fairness_cheating"
    LOYALTY_BETRAYAL = "loyalty_betrayal"
    AUTHORITY_SUBVERSION = "authority_subversion"
    SANCTITY_DEGRADATION = "sanctity_degradation"
    LIBERTY_OPPRESSION = "liberty_oppression"


class JungianArchetype(str, Enum):
    """Jungian archetypes with Character Lexicon anchors."""
    HERO = "hero"           # → Category 1 Aspirational Hero
    SAGE = "sage"           # → Category 3 Credibility Validator
    SHADOW = "shadow"       # → Category 4 Cautionary Enemy
    TRICKSTER = "trickster" # → Category 2 Nostalgic Icon


# Jungian Specificity Rule mapping
JUNGIAN_ANCHOR_MAP = {
    JungianArchetype.HERO: CharacterCategory.ASPIRATIONAL_HERO,
    JungianArchetype.SAGE: CharacterCategory.CREDIBILITY_VALIDATOR,
    JungianArchetype.SHADOW: CharacterCategory.CAUTIONARY_ENEMY,
    JungianArchetype.TRICKSTER: CharacterCategory.NOSTALGIC_ICON,
}


# ──────────────────────────────────────────────────────────────
# Character Entry
# ──────────────────────────────────────────────────────────────

class CharacterEntry(BaseModel):
    """A single character in the 65-character lexicon.

    Each entry represents a figure's significance TO THIS TRIBE,
    not a biographical summary (Psychological Specificity Test).
    """
    character_id: str = Field(default="")
    coach_id: str = Field(default="")
    name: str = Field(...)
    category: CharacterCategory = Field(...)
    role_definition: str = Field(
        ...,
        description="Why this figure matters TO THIS TRIBE — not biography",
    )
    cral_moments: list[str] = Field(
        default_factory=list,
        description="CRAL moment IDs where this character is deployable",
    )
    moral_foundation_activated: MoralFoundation = Field(
        default=MoralFoundation.CARE_HARM,
    )
    content_mode_fit: list[str] = Field(
        default_factory=list,
        description="Emotional modes: status, processing, escape, recognition, discovery, tension",
    )
    character_prompt: str = Field(
        default="",
        description="Image generation prompt for visual deployment",
    )
    last_deployed_date: Optional[str] = Field(default=None)
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0)
    gaze_direction: GazeDirection = Field(default=GazeDirection.HOOK_ZONE)


# ──────────────────────────────────────────────────────────────
# Character Usage Registry
# ──────────────────────────────────────────────────────────────

class CharacterUsageRecord(BaseModel):
    """Usage log for non-repetition enforcement."""
    character_id: str = Field(...)
    content_format: str = Field(..., description="Format type (carousel, reel, story, etc.)")
    deployed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    context: str = Field(default="")


# ──────────────────────────────────────────────────────────────
# DEP-PROTO-017: Character Invocation Protocol
# ──────────────────────────────────────────────────────────────

class CharacterInvocationQuery(BaseModel):
    """DEP-PROTO-017 structured query: 5 parameters."""
    cral_moment: str = Field(..., description="CRAL moment ID (M2, M3, M4, M5, M7)")
    moral_foundation: MoralFoundation = Field(...)
    content_mode: str = Field(..., description="Emotional mode for content")
    audience_maturity: str = Field(default="established")
    exclusion_window_weeks: int = Field(
        default=8,
        description="Non-repetition window per format type",
    )


class CharacterInvocationResult(BaseModel):
    """Response from DEP-PROTO-017 invocation."""
    ranked_characters: list[CharacterEntry] = Field(default_factory=list)
    selection_justification: str = Field(default="")
    excluded_characters: list[str] = Field(
        default_factory=list,
        description="Character IDs excluded by non-repetition rule",
    )
    query_parameters: Optional[CharacterInvocationQuery] = Field(default=None)


# ──────────────────────────────────────────────────────────────
# Psychological Specificity Test
# ──────────────────────────────────────────────────────────────

class SpecificityTestResult(BaseModel):
    """Result of the Psychological Specificity Test for one character."""
    character_name: str = Field(...)
    passed: bool = Field(...)
    reason: str = Field(default="")


class LexiconSpecificityTestResult(BaseModel):
    """Aggregate result of the Psychological Specificity Test for all 65 characters."""
    total_tested: int = Field(default=0)
    total_passed: int = Field(default=0)
    total_failed: int = Field(default=0)
    pass_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    failures: list[SpecificityTestResult] = Field(default_factory=list)
    passed: bool = Field(default=False)


# ──────────────────────────────────────────────────────────────
# Jungian Anchor Validation
# ──────────────────────────────────────────────────────────────

class JungianAnchorValidation(BaseModel):
    """Result of Jungian Specificity Rule check (AC3)."""
    archetype: JungianArchetype = Field(...)
    required_category: CharacterCategory = Field(...)
    anchor_character: Optional[CharacterEntry] = Field(default=None)
    validated: bool = Field(default=False)
    error: str = Field(default="")


# ──────────────────────────────────────────────────────────────
# Character Lexicon — Complete output
# ──────────────────────────────────────────────────────────────

# Category count requirements
CATEGORY_COUNTS = {
    CharacterCategory.ASPIRATIONAL_HERO: 20,
    CharacterCategory.NOSTALGIC_ICON: 15,
    CharacterCategory.CREDIBILITY_VALIDATOR: 10,
    CharacterCategory.CAUTIONARY_ENEMY: 10,
    CharacterCategory.IDEOLOGICAL_OPPOSITION: 10,
}


class CharacterLexicon(BaseModel):
    """The complete 65-character lexicon (FR0C output).

    Governed by DEP-PROTO-017 for deterministic runtime selection.
    """
    coach_id: str = Field(...)
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    dep_id: str = Field(default="CHARACTER-LEXICON")
    protocol_id: str = Field(default="DEP-PROTO-017")
    version: int = Field(default=1, ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    entries: list[CharacterEntry] = Field(default_factory=list)
    usage_registry: list[CharacterUsageRecord] = Field(default_factory=list)
    specificity_test: Optional[LexiconSpecificityTestResult] = Field(default=None)

    def count_by_category(self) -> dict[int, int]:
        """Count entries per category."""
        counts: dict[int, int] = {}
        for entry in self.entries:
            cat = entry.category.value
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def total_entries(self) -> int:
        return len(self.entries)

    def meets_count_requirements(self) -> bool:
        """Check if each category has the required count of entries."""
        counts = self.count_by_category()
        for cat, required in CATEGORY_COUNTS.items():
            if counts.get(cat.value, 0) < required:
                return False
        return True

    def get_by_category(self, category: CharacterCategory) -> list[CharacterEntry]:
        return [e for e in self.entries if e.category == category]

    def invoke(
        self,
        query: CharacterInvocationQuery,
    ) -> CharacterInvocationResult:
        """DEP-PROTO-017: Structured character invocation.

        5-parameter query → ranked list of eligible characters.
        Non-repetition enforced per format type (not globally).
        """
        from datetime import timedelta

        # Map CRAL moments to categories
        cral_category_map = {
            "M2": [CharacterCategory.CREDIBILITY_VALIDATOR],
            "M3": [CharacterCategory.CAUTIONARY_ENEMY, CharacterCategory.IDEOLOGICAL_OPPOSITION],
            "M4": [CharacterCategory.ASPIRATIONAL_HERO, CharacterCategory.NOSTALGIC_ICON],
            "M5": [CharacterCategory.IDEOLOGICAL_OPPOSITION],
            "M7": [CharacterCategory.NOSTALGIC_ICON],
        }

        eligible_categories = cral_category_map.get(query.cral_moment, list(CharacterCategory))

        # Filter by category and moral foundation
        candidates = [
            e for e in self.entries
            if e.category in eligible_categories
            and e.moral_foundation_activated == query.moral_foundation
        ]

        # If no exact moral foundation match, relax to all in category
        if not candidates:
            candidates = [
                e for e in self.entries
                if e.category in eligible_categories
            ]

        # Non-repetition: exclude characters used in same format within window
        cutoff = datetime.now(timezone.utc) - timedelta(weeks=query.exclusion_window_weeks)
        recently_used_ids = set()
        for usage in self.usage_registry:
            try:
                deployed = datetime.fromisoformat(usage.deployed_at)
                if deployed > cutoff and usage.content_format == query.content_mode:
                    recently_used_ids.add(usage.character_id)
            except (ValueError, TypeError):
                continue

        excluded = [c.character_id for c in candidates if c.character_id in recently_used_ids]
        ranked = [c for c in candidates if c.character_id not in recently_used_ids]

        # Sort by relevance score
        ranked.sort(key=lambda c: c.relevance_score, reverse=True)

        return CharacterInvocationResult(
            ranked_characters=ranked,
            selection_justification=(
                f"Query: {query.cral_moment} + {query.moral_foundation.value} + {query.content_mode}. "
                f"Eligible: {len(candidates)}, Excluded (non-rep): {len(excluded)}, Ranked: {len(ranked)}."
            ),
            excluded_characters=excluded,
            query_parameters=query,
        )

    def validate_jungian_anchor(
        self,
        archetype: JungianArchetype,
    ) -> JungianAnchorValidation:
        """AC3: Validate Jungian archetype has a character anchor."""
        required_category = JUNGIAN_ANCHOR_MAP[archetype]
        candidates = self.get_by_category(required_category)

        if candidates:
            return JungianAnchorValidation(
                archetype=archetype,
                required_category=required_category,
                anchor_character=candidates[0],
                validated=True,
            )
        return JungianAnchorValidation(
            archetype=archetype,
            required_category=required_category,
            validated=False,
            error=f"JUNGIAN_ANCHOR_REQUIRED: No {required_category.name} found for archetype {archetype.value}",
        )
