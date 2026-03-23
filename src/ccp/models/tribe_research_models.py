"""
CCP Pydantic Models — Tribe Soul Research (FR0B)
H11 Tribe Dossier schema + 4-Skill Research Architecture models.

H11 is consumed by:
- FR0C (Character Lexicon Builder — cultural artifacts)
- FR0D (Semiotic Intelligence Library — visual signifiers)
- FR6 (Tribe Profile — Context Premises)
- FR14 (CRAL Research Subsystem)

Spec reference: FR0B_Tribe_Soul_Research_Tech_Spec.md
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class TribeResearchSkill(str, Enum):
    """The 4 specialist skills for Tribe Soul Research."""
    LEXICON = "tribe-lexicon-research"
    HUMOR = "tribe-humor-research"
    EMOTIONAL = "tribe-emotional-research"
    SOCIAL = "tribe-social-research"


class HumorStyle(str, Enum):
    """Humor style classifications (Benign Violation Theory)."""
    SELF_DEPRECATING = "self_deprecating"
    ABSURDIST = "absurdist"
    SATIRICAL = "satirical"
    OBSERVATIONAL = "observational"
    DARK = "dark"
    SARCASTIC = "sarcastic"
    IRONIC = "ironic"
    DEADPAN = "deadpan"


# ──────────────────────────────────────────────────────────────
# Verbatim Entry — the atomic unit
# ──────────────────────────────────────────────────────────────

class VerbatimEntry(BaseModel):
    """A direct quote from a real audience source.

    Core principle: archive, don't analyze.
    Every entry must include the verbatim quote plus its provenance.
    """
    quote: str = Field(..., description="Direct verbatim quote — not paraphrased")
    source_platform: str = Field(default="", description="Platform (Reddit, Discord, Facebook, forum)")
    source_identifier: str = Field(default="", description="Thread/post identifier (e.g., r/solopreneurs, u/user123)")
    timestamp_context: str = Field(default="", description="Temporal context (e.g., '2am post', 'after product launch')")
    category: str = Field(default="", description="Category within the skill's taxonomy")
    context: str = Field(default="", description="Usage context explaining why this quote is significant")


# ──────────────────────────────────────────────────────────────
# Section A: Cultural Artifacts (tribe-lexicon-research)
# ──────────────────────────────────────────────────────────────

class SlangEntry(BaseModel):
    """A tribal slang term with usage context and misuse correction."""
    term: str = Field(...)
    definition: str = Field(default="")
    usage_examples: list[VerbatimEntry] = Field(default_factory=list)
    misuse_correction: str = Field(
        default="",
        description="How tribe members correct misuse of this term",
    )


class HeroEnemyPost(BaseModel):
    """A hero/enemy reference with direct quotes."""
    figure_name: str = Field(...)
    role: str = Field(default="hero", description="'hero' or 'enemy'")
    quotes: list[VerbatimEntry] = Field(default_factory=list)


class InsideJoke(BaseModel):
    """A tribal inside joke with reference examples."""
    joke_reference: str = Field(...)
    context: str = Field(default="")
    examples: list[VerbatimEntry] = Field(default_factory=list)


class CulturalArtifacts(BaseModel):
    """H11 Section A — Cultural Artifacts (tribe-lexicon-research output).

    Volume quotas: 100-150 slang examples, 75-100 hero/enemy posts, 5-7 inside jokes.
    Quality gate: Verbatim ratio ≥70%.
    """
    slang_entries: list[SlangEntry] = Field(default_factory=list)
    hero_enemy_posts: list[HeroEnemyPost] = Field(default_factory=list)
    inside_jokes: list[InsideJoke] = Field(default_factory=list)
    verbatim_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    source_count: int = Field(default=0)
    volume_pages: float = Field(default=0.0)


# ──────────────────────────────────────────────────────────────
# Section B: Humor DNA Profile (tribe-humor-research)
# ──────────────────────────────────────────────────────────────

class HumorPost(BaseModel):
    """A humor post with style classification."""
    content: VerbatimEntry = Field(...)
    style: HumorStyle = Field(...)
    vote_count: int = Field(default=0, description="Community vote/reaction count")


class TabooEntry(BaseModel):
    """A humor taboo with community reaction evidence."""
    topic: str = Field(...)
    community_reaction: str = Field(default="")
    evidence: list[VerbatimEntry] = Field(default_factory=list)


class HumorDNAProfile(BaseModel):
    """H11 Section B — Humor DNA Profile (tribe-humor-research output).

    Volume quotas: 50-100 posts, ≥3 examples per style, 2-3 taboos.
    Quality gate: ≥3 distinct humor styles, ≥2 taboo entries.
    """
    humor_posts: list[HumorPost] = Field(default_factory=list)
    taboo_entries: list[TabooEntry] = Field(default_factory=list)
    styles_identified: list[HumorStyle] = Field(default_factory=list)
    verbatim_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    source_count: int = Field(default=0)
    volume_pages: float = Field(default=0.0)


# ──────────────────────────────────────────────────────────────
# Section C: Emotional Landscape (tribe-emotional-research)
# ──────────────────────────────────────────────────────────────

class EmotionalPost(BaseModel):
    """An emotional post with L3 depth scoring."""
    content: VerbatimEntry = Field(...)
    emotion_type: str = Field(default="", description="aspiration, anxiety, trigger_positive, trigger_negative")
    depth_level: int = Field(default=1, ge=1, le=3, description="L1=surface, L2=personal, L3=visceral")
    authenticity_score: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="LIWC-22 authenticity percentile",
    )


class EmotionalLandscape(BaseModel):
    """H11 Section C — Emotional Landscape (tribe-emotional-research output).

    Volume quotas: 5-7 aspiration quotes, 5-7 anxiety quotes, 3+3 triggers.
    Quality gate: ≥40% of posts above LIWC-22 70th percentile.
    Mind After Midnight methodology: 11pm-4am posts.
    """
    aspiration_quotes: list[EmotionalPost] = Field(default_factory=list)
    anxiety_quotes: list[EmotionalPost] = Field(default_factory=list)
    positive_triggers: list[EmotionalPost] = Field(default_factory=list)
    negative_triggers: list[EmotionalPost] = Field(default_factory=list)
    l3_ratio: float = Field(default=0.0, ge=0.0, le=1.0, description="Percentage of L3 depth posts")
    verbatim_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    source_count: int = Field(default=0)
    volume_pages: float = Field(default=0.0)


# ──────────────────────────────────────────────────────────────
# Section D: Social Architecture (tribe-social-research)
# ──────────────────────────────────────────────────────────────

class UnwrittenRule(BaseModel):
    """A tribal unwritten rule with specificity evidence."""
    rule: str = Field(...)
    violation_consequence: str = Field(
        default="",
        description="Observable community reaction when rule is violated",
    )
    evidence: list[VerbatimEntry] = Field(default_factory=list)


class InGroupSignal(BaseModel):
    """An in-group status signal with context."""
    signal: str = Field(...)
    context: str = Field(default="")
    examples: list[VerbatimEntry] = Field(default_factory=list)


class BoundaryEnforcement(BaseModel):
    """A boundary enforcement example (newcomer correction, moderation)."""
    boundary: str = Field(...)
    enforcement_mechanism: str = Field(default="")
    examples: list[VerbatimEntry] = Field(default_factory=list)


class SocialArchitecture(BaseModel):
    """H11 Section D — Social Architecture (tribe-social-research output).

    Volume quotas: 3-5 rules, 5+ signals, 3+ boundary examples.
    Quality gate: Each rule must be specific enough that violating it
    produces an observable community reaction. Generic rules FAIL.
    """
    unwritten_rules: list[UnwrittenRule] = Field(default_factory=list)
    in_group_signals: list[InGroupSignal] = Field(default_factory=list)
    boundary_enforcements: list[BoundaryEnforcement] = Field(default_factory=list)
    verbatim_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    source_count: int = Field(default=0)
    volume_pages: float = Field(default=0.0)


# ──────────────────────────────────────────────────────────────
# Section E: Cross-Dimensional Convergence Analysis
# ──────────────────────────────────────────────────────────────

class ConvergenceEvent(BaseModel):
    """A cross-dimensional convergence — a figure/concept appearing across multiple skills."""
    entity: str = Field(..., description="The figure, concept, or reference")
    dimensions: list[str] = Field(
        default_factory=list,
        description="Which H11 sections reference this entity",
    )
    tribal_significance: str = Field(
        default="",
        description="Why multi-dimensional appearance makes this entity architecturally valuable",
    )
    evidence: list[VerbatimEntry] = Field(default_factory=list)


class ConvergenceAnalysis(BaseModel):
    """H11 Section E — Cross-Dimensional Convergence Analysis.

    Guardian Agent synthesis step: identifies entities that appear
    across multiple research dimensions (lexicon → humor → emotion → social).
    """
    convergence_events: list[ConvergenceEvent] = Field(default_factory=list)
    category_1_heroes: list[str] = Field(
        default_factory=list,
        description="Aspirational heroes appearing in ≥3 dimensions",
    )
    synthesis_summary: str = Field(default="")


# ──────────────────────────────────────────────────────────────
# Research Execution Plan
# ──────────────────────────────────────────────────────────────

class ResearchExecutionPlan(BaseModel):
    """280-320 word Research Execution Plan generated before skill execution.

    Specifies platform targets, audience segments, and cultural context
    derived from DEP-ENG-050.
    """
    platform_targets: list[str] = Field(
        default_factory=list,
        description="Exact platform targets for this coach's audience",
    )
    audience_segment: str = Field(default="", description="Audience parameters from DEP-ENG-050")
    cultural_context: str = Field(default="", description="Cultural restrictions/directives")
    plan_text: str = Field(default="", description="Full 280-320 word plan")
    dep_eng_050_version: int = Field(default=1)


# ──────────────────────────────────────────────────────────────
# H11 Tribe Dossier — Complete Output
# ──────────────────────────────────────────────────────────────

class TribeDossier(BaseModel):
    """H11 Tribe Dossier — 25-30 page verbatim corpus.

    Primary output of FR0B. 4 sections from specialist skills
    + 1 synthesis section from Guardian Agent.

    Quality Gates:
    - Volume Verification: ≥25 pages combined
    - Verbatim Ratio: ≥70% direct quotes across all sections
    """
    # Metadata
    coach_id: str = Field(...)
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    dep_id: str = Field(default="H11")
    version: int = Field(default=1, ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    # Research plan
    research_plan: Optional[ResearchExecutionPlan] = Field(default=None)

    # 4 specialist sections
    section_a_cultural_artifacts: CulturalArtifacts = Field(default_factory=CulturalArtifacts)
    section_b_humor_dna: HumorDNAProfile = Field(default_factory=HumorDNAProfile)
    section_c_emotional_landscape: EmotionalLandscape = Field(default_factory=EmotionalLandscape)
    section_d_social_architecture: SocialArchitecture = Field(default_factory=SocialArchitecture)

    # Synthesis section
    section_e_convergence: ConvergenceAnalysis = Field(default_factory=ConvergenceAnalysis)

    # Quality gate results
    total_pages: float = Field(default=0.0)
    aggregate_verbatim_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    degradation_flag: bool = Field(
        default=False,
        description="AC3: True if PROVISIONAL verdict — propagates to downstream content",
    )

    # ── Computed Properties ──

    def compute_total_pages(self) -> float:
        """Sum pages across all 4 skill sections."""
        self.total_pages = (
            self.section_a_cultural_artifacts.volume_pages
            + self.section_b_humor_dna.volume_pages
            + self.section_c_emotional_landscape.volume_pages
            + self.section_d_social_architecture.volume_pages
        )
        return self.total_pages

    def compute_aggregate_verbatim_ratio(self) -> float:
        """Weighted average of verbatim ratios across sections."""
        sections = [
            (self.section_a_cultural_artifacts.verbatim_ratio, self.section_a_cultural_artifacts.volume_pages),
            (self.section_b_humor_dna.verbatim_ratio, self.section_b_humor_dna.volume_pages),
            (self.section_c_emotional_landscape.verbatim_ratio, self.section_c_emotional_landscape.volume_pages),
            (self.section_d_social_architecture.verbatim_ratio, self.section_d_social_architecture.volume_pages),
        ]
        total_weight = sum(w for _, w in sections)
        if total_weight == 0:
            self.aggregate_verbatim_ratio = 0.0
            return 0.0
        weighted_sum = sum(r * w for r, w in sections)
        self.aggregate_verbatim_ratio = weighted_sum / total_weight
        return self.aggregate_verbatim_ratio

    def passes_volume_gate(self) -> bool:
        """Volume Verification Test: ≥25 pages. Binary PASS/FAIL."""
        return self.compute_total_pages() >= 25.0

    def passes_verbatim_gate(self) -> bool:
        """Verbatim Ratio Test: ≥70% direct quotes. Binary PASS/FAIL."""
        return self.compute_aggregate_verbatim_ratio() >= 0.70


# ──────────────────────────────────────────────────────────────
# Skill Research Result (individual skill output)
# ──────────────────────────────────────────────────────────────

class SkillResearchResult(BaseModel):
    """Result from a single tribe research skill execution."""
    skill: TribeResearchSkill = Field(...)
    section_name: str = Field(default="")
    verbatim_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    volume_pages: float = Field(default=0.0)
    source_count: int = Field(default=0)
    quality_gates_passed: list[str] = Field(default_factory=list)
    quality_gates_failed: list[str] = Field(default_factory=list)
    receipt_id: str = Field(default="")
