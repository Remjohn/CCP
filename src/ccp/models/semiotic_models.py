"""
CCP Pydantic Models — Semiotic Intelligence Library (FR0D)
4-Category Visual Signifier Lexicon + DEP-PROTO-018 Composition Decision Protocol V2.

Consumed by:
- FR35/FR36 Content Composition
- FR-VIS-01+ Visual Pipeline
- Semiotic Composer Agent
- Stewardship Mode (8-week freshness tracking)

Spec reference: FR0D_Semiotic_Intelligence_Tech_Spec.md
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class SemioticCategory(str, Enum):
    """4 semiotic categories for the visual signifier lexicon."""
    CELEBRITY_MEME_FORMATS = "celebrity_meme_formats"  # Layer 2 — H11 Sec B
    UNIVERSAL_ARCHETYPES = "universal_archetypes"       # Layer 1 — Baseline + FR0C
    CULTURAL_SYMBOLS = "cultural_symbols"               # Layer 3 — H11 Sec A + D
    COLOR_TYPOGRAPHY = "color_typography"                # Layer 4 — V2 Spec


class AudienceMaturity(str, Enum):
    """Audience maturity level for DEP-PROTO-018 Q1."""
    NEW = "new"             # L2 primary
    DEVELOPING = "developing"  # L2 + L3
    LOYAL = "loyal"         # L1 primary


class EmotionalMode(str, Enum):
    """Content emotional mode for DEP-PROTO-018 Q2."""
    TENSION = "T"          # L3 + Cat 4/5
    VULNERABILITY = "V"   # L1 + Cat 1/2
    RECOGNITION = "R"     # L2 + Cat 2


class ColorProfile(str, Enum):
    """4 pre-defined color psychology profiles."""
    ESCAPE = "escape"               # Warm Neutral — comfort, gentle invitation
    PROCESSING = "processing"       # High Contrast Deep — depth, serious invitation
    DISCOVERY = "discovery"         # Mid-Warmth Energetic — possibility, active invitation
    STATUS = "status"               # Premium Dark — exclusivity, insider signal


# ──────────────────────────────────────────────────────────────
# Signifier Entry — atomic unit
# ──────────────────────────────────────────────────────────────

class VisualSignifierEntry(BaseModel):
    """A single entry in the visual signifier lexicon."""
    signifier_id: str = Field(default="")
    coach_id: str = Field(default="")
    category: SemioticCategory = Field(...)
    name: str = Field(...)
    description: str = Field(default="")
    deployment_mechanism: str = Field(
        default="",
        description="How this signifier is deployed in content — must be documented",
    )
    cognitive_mechanism: str = Field(
        default="",
        description="Cognitive mechanism this triggers (e.g., pattern recognition)",
    )
    tribal_resonance: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Tribal relevance score — 0 = universal baseline, 1 = deeply tribal",
    )
    source_section: str = Field(
        default="",
        description="H11 section source (e.g., 'Section B', 'Section A+D')",
    )
    is_baseline: bool = Field(
        default=False,
        description="True if from baseline JSON (read-only shared), False if tribal SQL",
    )


# ──────────────────────────────────────────────────────────────
# Color Psychology Profile
# ──────────────────────────────────────────────────────────────

class ColorPsychologyProfile(BaseModel):
    """A pre-defined color psychology profile mapped to a mood state."""
    profile: ColorProfile = Field(...)
    label: str = Field(default="")
    description: str = Field(default="")
    primary_colors: list[str] = Field(default_factory=list)
    typography_style: str = Field(default="")
    mood_state: str = Field(default="")
    invitation_type: str = Field(default="")
    deployment_mechanism: str = Field(default="")


# ──────────────────────────────────────────────────────────────
# Semiotic Combination Registry
# ──────────────────────────────────────────────────────────────

class SemioticCombinationRecord(BaseModel):
    """8-week freshness tracking for compositions."""
    combination_id: str = Field(default="")
    coach_id: str = Field(default="")
    signifier_ids: list[str] = Field(default_factory=list)
    content_format: str = Field(default="")
    deployed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    rotation_count: int = Field(default=0, description="≥3 triggers fatigue signal")


# ──────────────────────────────────────────────────────────────
# DEP-PROTO-018: Composition Decision Protocol V2
# ──────────────────────────────────────────────────────────────

class CompositionQuery(BaseModel):
    """DEP-PROTO-018 — 4-question sequential algorithm input."""
    audience_maturity: AudienceMaturity = Field(...)
    emotional_mode: EmotionalMode = Field(...)
    cral_moment: str = Field(..., description="CRAL moment ID (M1-M7)")
    freshness_check: bool = Field(
        default=True,
        description="If True, check 8-week freshness registry",
    )


class CompositionDecision(BaseModel):
    """DEP-PROTO-018 — deterministic visual decision output."""
    recommended_signifiers: list[VisualSignifierEntry] = Field(default_factory=list)
    color_profile: Optional[ColorPsychologyProfile] = Field(default=None)
    decision_rationale: str = Field(default="")
    freshness_status: str = Field(default="fresh")
    fatigue_signal: bool = Field(
        default=False,
        description="True if ≥3 rotations on the same combination",
    )
    jungian_anchor_required: bool = Field(default=False)
    jungian_anchor_error: str = Field(default="")


# ──────────────────────────────────────────────────────────────
# Semiotic Coverage Test
# ──────────────────────────────────────────────────────────────

class CategoryCoverageResult(BaseModel):
    """Coverage test result for one category."""
    category: SemioticCategory = Field(...)
    tribe_specific_count: int = Field(default=0)
    has_deployment_mechanism: bool = Field(default=False)
    passed: bool = Field(default=False)
    reason: str = Field(default="")


class SemioticCoverageTestResult(BaseModel):
    """Aggregate result of the Semiotic Coverage Test."""
    category_results: list[CategoryCoverageResult] = Field(default_factory=list)
    all_passed: bool = Field(default=False)
    total_tribe_specific: int = Field(default=0)


# ──────────────────────────────────────────────────────────────
# Visual Signifier Lexicon — Complete output
# ──────────────────────────────────────────────────────────────

class VisualSignifierLexicon(BaseModel):
    """The complete Semiotic Intelligence Library (FR0D output).

    Split storage:
    - baseline.json (read-only shared)
    - Supabase SQL (per-coach tribal enrichment)

    Governed by DEP-PROTO-018 for deterministic composition decisions.
    """
    coach_id: str = Field(...)
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    dep_id: str = Field(default="VISUAL-SIGNIFIER-LEXICON")
    protocol_id: str = Field(default="DEP-PROTO-018")
    version: int = Field(default=1, ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    # Entries by category
    entries: list[VisualSignifierEntry] = Field(default_factory=list)

    # Color psychology profiles
    color_profiles: list[ColorPsychologyProfile] = Field(default_factory=list)

    # Combination registry (initialized empty)
    combination_registry: list[SemioticCombinationRecord] = Field(default_factory=list)

    # Coverage test result
    coverage_test: Optional[SemioticCoverageTestResult] = Field(default=None)

    def entries_by_category(self, category: SemioticCategory) -> list[VisualSignifierEntry]:
        return [e for e in self.entries if e.category == category]

    def count_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for cat in SemioticCategory:
            counts[cat.value] = len(self.entries_by_category(cat))
        return counts

    def tribe_specific_entries(self) -> list[VisualSignifierEntry]:
        return [e for e in self.entries if not e.is_baseline and e.tribal_resonance > 0]

    def run_coverage_test(self) -> SemioticCoverageTestResult:
        """Semiotic Coverage Test: ≥3 tribe-specific entries per category with deployment mechanism."""
        results: list[CategoryCoverageResult] = []

        for cat in SemioticCategory:
            cat_entries = self.entries_by_category(cat)
            tribe_entries = [e for e in cat_entries if not e.is_baseline and e.tribal_resonance > 0]
            with_mechanism = [e for e in tribe_entries if e.deployment_mechanism.strip()]

            passed = len(with_mechanism) >= 3
            results.append(CategoryCoverageResult(
                category=cat,
                tribe_specific_count=len(tribe_entries),
                has_deployment_mechanism=len(with_mechanism) >= 3,
                passed=passed,
                reason=(
                    f"{len(with_mechanism)} tribe-specific w/ mechanism (threshold: ≥3)"
                    if passed else
                    f"Only {len(with_mechanism)} tribe-specific w/ mechanism (need ≥3)"
                ),
            ))

        all_passed = all(r.passed for r in results)
        total = sum(r.tribe_specific_count for r in results)

        test_result = SemioticCoverageTestResult(
            category_results=results,
            all_passed=all_passed,
            total_tribe_specific=total,
        )
        self.coverage_test = test_result
        return test_result
