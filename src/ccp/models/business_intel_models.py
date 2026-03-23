"""
CCP Pydantic Models — Business Intelligence Summary (DEP-ENG-050)
FR0A — Schema for coach_business_summary.json.

DEP-ENG-050 is the seed for all downstream extraction. It is consumed by:
- FR0B (Tribe Soul Research — audience parameters)
- FR1 (Genesis Pipeline — positioning context)
- FR7 (Leadership Scorecard — business context)
- FR51–FR60 (CPSC Campaign Layer — campaign positioning)

Spec reference: FR0A_Business_Intelligence_Tech_Spec.md §Output
"""

from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class TransformationStory(BaseModel):
    """A verified real-person transformation story with verbatim language.

    Spec: ≥3 required for Value Proposition CRAL depth pass.
    Human Evidence Bias gate (per CRAL_Documentation_V1).
    """

    client_identifier: str = Field(
        default="",
        description="Anonymized client reference (e.g., 'Client A', 'Sarah, corporate exec')",
    )
    before_state: str = Field(
        ...,
        description="Client's state before working with the coach — verbatim language preferred",
    )
    after_state: str = Field(
        ...,
        description="Client's state after the transformation — verbatim language preferred",
    )
    verbatim_quotes: list[str] = Field(
        default_factory=list,
        description="Direct quotes from the client or coach describing the transformation",
    )
    transformation_mechanism: str = Field(
        default="",
        description="What specifically caused the change (method, process, intervention)",
    )
    source: str = Field(
        default="",
        description="Where this story was sourced from (testimonial, case study, interview)",
    )


class ValueProposition(BaseModel):
    """Dimension 1: What the coach delivers and why it matters.

    CRAL depth pass REQUIRED — minimum 3 verified real-person transformation stories.
    """

    core_transformation: str = Field(
        default="",
        description="The specific before→after journey the coach delivers",
    )
    unique_mechanism: str = Field(
        default="",
        description="The coach's proprietary method, process, or framework",
    )
    transformation_stories: list[TransformationStory] = Field(
        default_factory=list,
        description="≥3 verified real-person transformation stories with verbatim language",
    )
    cral_depth_passed: bool = Field(
        default=False,
        description="True if CRAL depth pass confirmed (≥3 stories verified)",
    )

    @field_validator("transformation_stories")
    @classmethod
    def validate_min_stories(cls, v: list) -> list:
        """Warn if fewer than 3 stories — gate enforced at pipeline level."""
        return v


class RevenueArchitecture(BaseModel):
    """Dimension 2: Offer structure, pricing, and delivery.

    No CRAL depth pass required — structural analysis sufficient.
    """

    offer_tiers: list[str] = Field(
        default_factory=list,
        description="Distinct offer levels (e.g., '1:1 coaching', 'group program', 'course')",
    )
    price_range: str = Field(
        default="",
        description="Price range or pricing model description",
    )
    delivery_method: str = Field(
        default="",
        description="How the coaching is delivered (online, in-person, hybrid, async)",
    )
    revenue_model: str = Field(
        default="",
        description="Business model type (service-based, product-based, hybrid)",
    )


class AudiencePrecision(BaseModel):
    """Dimension 3: Who buys, who doesn't, and why.

    No CRAL depth pass required — Interview Phase 5 provides deeper seed.
    """

    who_buys: str = Field(
        default="",
        description="Profile of people who actually purchase (not aspirational)",
    )
    who_doesnt: str = Field(
        default="",
        description="Profile of people who engage but don't convert",
    )
    why_they_buy: str = Field(
        default="",
        description="The trigger or moment that causes the purchase decision",
    )
    audience_language: list[str] = Field(
        default_factory=list,
        description="Exact phrases the audience uses to describe their problem",
    )


class MarketPositioning(BaseModel):
    """Dimension 4: What competitors cannot claim.

    CRAL depth pass REQUIRED — differentiation claim with competitor evidence.
    """

    primary_differentiator: str = Field(
        default="",
        description="The one thing competitors cannot credibly claim",
    )
    competitor_landscape: list[str] = Field(
        default_factory=list,
        description="Named or described competitors in the same niche",
    )
    positioning_gap: str = Field(
        default="",
        description="The gap between marketing language and actual transformation",
    )
    cral_depth_passed: bool = Field(
        default=False,
        description="True if CRAL depth pass confirmed with competitor evidence",
    )


class ContentPhilosophy(BaseModel):
    """Dimension 5: Coach's beliefs about content's role in the business.

    No CRAL depth pass required — authenticated coach voice is the authority.
    """

    content_role: str = Field(
        default="",
        description="What the coach believes content should do for their business",
    )
    content_fears: str = Field(
        default="",
        description="What the coach is afraid of in content creation",
    )
    content_strengths: str = Field(
        default="",
        description="What the coach does naturally well in content",
    )
    platform_preferences: list[str] = Field(
        default_factory=list,
        description="Preferred platforms and why",
    )


class PositioningPrecisionTestResult(BaseModel):
    """Result of the Positioning Precision Test quality gate.

    Spec: Replace coach name with competitor name. If summary still
    accurately describes the competitor, extraction FAILED.
    """

    passed: bool = Field(..., description="True if substitution BREAKS the description")
    competitor_name_used: str = Field(
        default="",
        description="The competitor name used for substitution testing",
    )
    substitution_analysis: str = Field(
        default="",
        description="Explanation of why substitution breaks/doesn't break the summary",
    )
    generic_dimensions: list[str] = Field(
        default_factory=list,
        description="Dimensions flagged as generic (on failure)",
    )


class SourceIngestionResult(BaseModel):
    """Metadata from source folder ingestion."""

    source_document_count: int = Field(default=0, description="Total documents ingested")
    document_types: dict[str, int] = Field(
        default_factory=dict,
        description="Count by type (website, transcript, positioning_doc, recording)",
    )
    total_content_length: int = Field(default=0, description="Total character count across all sources")
    interview_response_count: int = Field(default=0, description="Number of interview Phase 1 responses")
    ingested_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


class BusinessIntelSummary(BaseModel):
    """DEP-ENG-050: Business Intelligence Summary.

    Primary output of FR0A. Stored as coach_business_summary.json.
    Consumed by FR0B, FR1, FR7, FR51-FR60.

    Spec reference: FR0A_Business_Intelligence_Tech_Spec.md §Output
    """

    # Metadata
    coach_id: str = Field(..., description="Coach Person ID (CCC-0000)")
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    version: int = Field(default=1, ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    dep_id: str = Field(
        default="DEP-ENG-050",
        description="Dependency Registry ID",
    )

    # Primary output: 60-80 word positioning summary
    positioning_summary: str = Field(
        ...,
        description=(
            "60-80 word positioning summary in 3rd person: "
            "expertise → audience → pain → solution"
        ),
    )

    # 5 dimensions
    value_proposition: ValueProposition = Field(default_factory=ValueProposition)
    revenue_architecture: RevenueArchitecture = Field(default_factory=RevenueArchitecture)
    audience_precision: AudiencePrecision = Field(default_factory=AudiencePrecision)
    market_positioning: MarketPositioning = Field(default_factory=MarketPositioning)
    content_philosophy: ContentPhilosophy = Field(default_factory=ContentPhilosophy)

    # Transformation evidence corpus
    transformation_evidence_corpus: list[TransformationStory] = Field(
        default_factory=list,
        description="≥3 verified real-person transformation stories with verbatim language",
    )

    # Quality gate result
    positioning_precision_test: Optional[PositioningPrecisionTestResult] = Field(
        default=None,
        description="Result of the Positioning Precision Test",
    )

    # Ingestion metadata
    source_ingestion: Optional[SourceIngestionResult] = Field(
        default=None,
        description="Metadata from source folder ingestion",
    )

    def word_count(self) -> int:
        """Count words in positioning summary."""
        return len(self.positioning_summary.split())

    def has_minimum_stories(self, minimum: int = 3) -> bool:
        """Check if transformation evidence corpus meets minimum threshold."""
        return len(self.transformation_evidence_corpus) >= minimum

    def is_cral_complete(self) -> bool:
        """Check if both CRAL depth passes are complete."""
        return (
            self.value_proposition.cral_depth_passed
            and self.market_positioning.cral_depth_passed
        )
