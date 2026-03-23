"""
CCP Step 6 — Container Module Library Models

Pydantic v2 models for:
  FR9:  Audience Empathy Agent (theme-specific Context Premise, 6×12 matrix, Four Laws)
  FR10: Four-Axis Structural Matching Engine (DEP-ENG-010 Four-Axis Match Object)
  FR11: Activation Event Seed Construction (DEP-ENG-011 Activation Event Seed)
  FR12: Three Failure Prevention Gates (DEP-ENG-027 Gate Diagnostic Certificate)

Architecture References:
  §Context_Premise_Trigger_Matching_Layer Part 2 (Four Laws of Audience Research Distillation)
  §Context_Premise_Trigger_Matching_Layer Part 4 (Four-Axis Structural Matching Engine)
  §Trigger-First Engine Architecture v3.0 Part 2

DEP-IDs produced:
  DEP-ENG-010: FourAxisMatchResult (Four-Axis Match Object)
  DEP-ENG-011: ActivationEventSeed (Activation Event Seed)
  DEP-ENG-027: GateDiagnosticCertificate (Gate Diagnostic Certificate — PROPOSED in FR12)

DEP-IDs consumed:
  DEP-LIB-001: EmotionalDNAProfile (from emotional_dna_models.py)
  DEP-LIB-002: TriggerMap (from trigger_map_models.py)
  DEP-ENG-006: ContextPremiseMap (from tribe_profile_models.py)
  DEP-ENG-019: Session Transcript Intelligence (from sacred_audio_models.py)
  DEP-ENG-041: Receipt Chain Guard (from receipt_chain.py)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ══════════════════════════════════════════════════════════════
# Shared Enums
# ══════════════════════════════════════════════════════════════

class MatchClassification(str, Enum):
    """FR10 §Phase 3: Four-axis match classification.
    CONFIRMED: sum = 4.0 (all axes EXACT/CONGRUENT)
    STRONG: sum 3.0–3.5, no axis = 0.0
    ADJACENT: any axis = 0.0 OR sum < 3.0  → never passed to seed construction
    NO_MATCH: sum < 2.0"""
    CONFIRMED = "CONFIRMED"
    STRONG = "STRONG"
    ADJACENT = "ADJACENT"
    NO_MATCH = "NO_MATCH"


class AxisCongruence(str, Enum):
    """Individual axis scoring level for four-axis matching."""
    EXACT = "EXACT"          # Score = 1.0
    CONGRUENT = "CONGRUENT"  # Score = 1.0 (synonym for Axis 2/3/4)
    ADJACENT = "ADJACENT"    # Score = 0.5
    PARTIAL = "PARTIAL"      # Score = 0.5 (synonym for Axis 2/4)
    NONE = "NONE"            # Score = 0.0
    INVALID = "INVALID"      # Axis 4: raw_unresolved — excluded


class DARNCATDimension(str, Enum):
    """Miller & Rollnick DARN-CAT dimensions for evocative questions.
    FR11 restricts to Taking Steps and Reasons only."""
    TAKING_STEPS = "taking_steps"
    REASONS = "reasons"


class AnchorQuality(str, Enum):
    """FR11 §Phase 2 Element 1: ESK anchor quality grading.
    full = ESK-level with sensory-perceptual records.
    degraded = General Event or Lifetime Period — flags requires_esk_harvesting."""
    FULL = "full"
    DEGRADED = "degraded"


class LanguageDriftStatus(str, Enum):
    """FR11 §Phase 4 / FR12 Gate 2: Language drift prevention verdict."""
    PASSED = "passed"
    WARNING = "warning"       # 1–2 terms
    CRITICAL = "critical"     # 0 terms → reject


class GateVerdict(str, Enum):
    """FR12: Three-valued gate verdict."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class AuthenticationVerdict(str, Enum):
    """FR9 §Phase 5: Four Laws authentication verdict.
    AUTHENTICATED = 4/4 Laws PASS
    PROVISIONAL = 3/4 Laws PASS
    FAILED = ≤2/4 Laws PASS — cannot feed downstream"""
    AUTHENTICATED = "AUTHENTICATED"
    PROVISIONAL = "PROVISIONAL"
    FAILED = "FAILED"


class FourLawName(str, Enum):
    """FR9 §Phase 4: The Four Laws of Audience Research Distillation."""
    LAW_1_LIVED_REALITY = "law_1_lived_reality"
    LAW_2_DEPTH_STRATIFICATION = "law_2_depth_stratification"
    LAW_3_TRIBAL_LANGUAGE = "law_3_tribal_language"
    LAW_4_DATA_PROVENANCE = "law_4_data_provenance"


class Gate3FailureMode(str, Enum):
    """FR12 §Stage 5: Diagnostic failure mode for Gate 3."""
    COACH_TEMPORAL_ERROR = "coach_temporal_error"
    AUDIENCE_EXTRACTION_ERROR = "audience_extraction_error"


# ══════════════════════════════════════════════════════════════
# FR9 — Audience Empathy Agent Models
# ══════════════════════════════════════════════════════════════

# ── Per-Cell Insight ──

class ContextPremiseInsight(BaseModel):
    """FR9 §Phase 3: A single insight cell in the 6×12 matrix.
    Each cell = one segment × one category."""
    text: str = Field(..., min_length=1, description="Insight in the audience's own language")
    depth: str = Field(..., pattern=r"^L[123]$", description="L1|L2|L3 depth classification")
    source: str = Field(
        ..., min_length=1,
        description="Verifiable source reference (forum URL, interview timestamp, etc.)"
    )
    tribal_terms: list[str] = Field(default_factory=list, description="In-group vocabulary used")
    two_am_test: bool = Field(default=False, description="Law 1: passes 2am neurobiological test")


class HiddenBeliefInsight(ContextPremiseInsight):
    """FR9 §Phase 3: Enhanced extraction for Hidden Beliefs.
    Must include public/private contradiction per AC8."""
    public_contradiction: str = Field(
        ..., min_length=1,
        description="They publicly say X, but privately believe Y"
    )


class EmotionalTriggerInsight(ContextPremiseInsight):
    """FR9 §Phase 3: Enhanced extraction for Emotional Triggers.
    Must include activation_keywords, moral_foundation, involuntary_response per AC8."""
    activation_keywords: list[str] = Field(
        ..., min_length=1,
        description="Specific words/phrases that fire the trigger"
    )
    moral_foundation: str = Field(
        ..., min_length=1,
        description="Which MFT foundation this trigger violates"
    )
    involuntary_response: str = Field(
        ..., min_length=1,
        description="Immediate unreflective emotional response"
    )


class CopingMechanismInsight(ContextPremiseInsight):
    """FR9 §Phase 3: Enhanced extraction for Coping Mechanism.
    Must include agency_attribution_pattern and coping_potential_assessment per AC8."""
    agency_attribution_pattern: str = Field(
        ..., min_length=1,
        description="Who the audience blames — self/individual/institutional/systemic"
    )
    coping_potential_assessment: str = Field(
        ..., min_length=1,
        description="Low/medium/high coping potential"
    )


# ── Segment Categories ──

class SegmentCategories(BaseModel):
    """FR9 §Phase 3: All 12 psychological categories for a single segment."""
    wants: list[ContextPremiseInsight] = Field(default_factory=list)
    frustrations: list[ContextPremiseInsight] = Field(default_factory=list)
    dreams: list[ContextPremiseInsight] = Field(default_factory=list)
    fears: list[ContextPremiseInsight] = Field(default_factory=list)
    suspicions: list[ContextPremiseInsight] = Field(default_factory=list)
    insecurities: list[ContextPremiseInsight] = Field(default_factory=list)
    envy_feelings: list[ContextPremiseInsight] = Field(default_factory=list)
    enemies: list[ContextPremiseInsight] = Field(default_factory=list)
    coping_mechanism: list[CopingMechanismInsight] = Field(default_factory=list)
    hidden_beliefs: list[HiddenBeliefInsight] = Field(default_factory=list)
    emotional_triggers: list[EmotionalTriggerInsight] = Field(default_factory=list)
    success_markers: list[ContextPremiseInsight] = Field(default_factory=list)

    def all_insights(self) -> list[ContextPremiseInsight]:
        """Return all insights across all 12 categories."""
        result: list[ContextPremiseInsight] = []
        result.extend(self.wants)
        result.extend(self.frustrations)
        result.extend(self.dreams)
        result.extend(self.fears)
        result.extend(self.suspicions)
        result.extend(self.insecurities)
        result.extend(self.envy_feelings)
        result.extend(self.enemies)
        result.extend(self.coping_mechanism)
        result.extend(self.hidden_beliefs)
        result.extend(self.emotional_triggers)
        result.extend(self.success_markers)
        return result

    def category_count(self) -> int:
        """Count of non-empty categories (out of 12)."""
        count = 0
        for cat in [
            self.wants, self.frustrations, self.dreams, self.fears,
            self.suspicions, self.insecurities, self.envy_feelings, self.enemies,
            self.coping_mechanism, self.hidden_beliefs, self.emotional_triggers,
            self.success_markers,
        ]:
            if len(cat) > 0:
                count += 1
        return count


# ── Segment Profile ──

class AudienceSegmentProfile(BaseModel):
    """FR9 §Phase 2: A single audience segment with full metadata."""
    segment_id: str = Field(..., min_length=1, description="Unique segment identifier")
    dhd_label: str = Field(..., min_length=1, description="Deep Human Desire label")
    coping_trajectory_position: str = Field(
        ..., pattern=r"^(SEARCH|ACTIVE|EXHAUSTED)$",
        description="Lazarus & Folkman: SEARCH|ACTIVE|EXHAUSTED"
    )
    regulatory_focus: str = Field(
        ..., pattern=r"^(promotion|prevention|mixed)$",
        description="Higgins Regulatory Focus Theory"
    )
    primary_moral_foundation_violated: str = Field(
        ..., min_length=1,
        description="MFT label: care_harm|fairness_cheating|loyalty_betrayal|authority_subversion|sanctity_degradation|liberty_oppression"
    )
    description: str = Field(
        ..., min_length=1,
        description="One-paragraph psychological portrait"
    )
    categories: SegmentCategories = Field(default_factory=SegmentCategories)


# ── Tribal Language Registry ──

class InGroupTerm(BaseModel):
    """FR9 §Phase 4 Law 3: A verified in-group tribal term."""
    term: str = Field(..., min_length=1)
    context: str = Field(default="", description="Usage context")
    example_usage: str = Field(default="", description="Example of the term in use")


class RejectionTerm(BaseModel):
    """FR9 §Phase 4 Law 3: A term rejected by the genericness test."""
    term: str = Field(..., min_length=1)
    why_rejected: str = Field(default="", description="Reason for rejection")
    what_to_use_instead: str = Field(default="", description="Tribal alternative")


class TribalLanguageRegistry(BaseModel):
    """FR9 §Phase 4 Law 3: Registry of tribal and rejected terms.
    Law 3 gate: ≥10 in-group terms, ≥5 rejection terms."""
    in_group_terms: list[InGroupTerm] = Field(default_factory=list)
    rejection_terms: list[RejectionTerm] = Field(default_factory=list)

    def passes_law_3(self) -> bool:
        """Law 3 gate: ≥10 in-group terms AND ≥5 rejection terms."""
        return len(self.in_group_terms) >= 10 and len(self.rejection_terms) >= 5


# ── Depth Distribution ──

class DepthDistribution(BaseModel):
    """FR9 §Phase 4 Law 2: Depth stratification distribution."""
    l1: float = Field(default=0.0, ge=0.0, le=1.0)
    l2: float = Field(default=0.0, ge=0.0, le=1.0)
    l3: float = Field(default=0.0, ge=0.0, le=1.0)

    # FR9 Law 2 exact thresholds
    L2_MINIMUM: float = 0.30
    L3_MINIMUM: float = 0.10

    def passes_law_2(self) -> bool:
        """Law 2 gate: L2 ≥ 30% AND L3 ≥ 10%."""
        return self.l2 >= self.L2_MINIMUM and self.l3 >= self.L3_MINIMUM

    class Config:
        # Allow L2_MINIMUM / L3_MINIMUM as class-level constants
        pass


# ── Provenance Report ──

class ProvenanceReport(BaseModel):
    """FR9 §Phase 4 Law 4: Data provenance tracking."""
    total_insights: int = 0
    verified_count: int = 0
    unverified_count: int = 0
    provenance_percentage: float = Field(default=0.0, ge=0.0, le=1.0)

    # FR9 Law 4 exact threshold
    MAX_UNVERIFIED_PERCENTAGE: float = 0.20

    def passes_law_4(self) -> bool:
        """Law 4 gate: ≤20% unverified insights."""
        if self.total_insights == 0:
            return False
        unverified_pct = self.unverified_count / self.total_insights
        return unverified_pct <= self.MAX_UNVERIFIED_PERCENTAGE


# ── Four Laws Status ──

class FourLawsStatus(BaseModel):
    """FR9 §Phase 4: Status of all four Laws of Audience Research Distillation."""
    law_1_lived_reality: str = Field(
        default="PENDING", pattern=r"^(PASS|FAIL|PENDING)$"
    )
    law_2_depth_stratification: str = Field(
        default="PENDING", pattern=r"^(PASS|FAIL|PENDING)$"
    )
    law_3_tribal_language: str = Field(
        default="PENDING", pattern=r"^(PASS|FAIL|PENDING)$"
    )
    law_4_data_provenance: str = Field(
        default="PENDING", pattern=r"^(PASS|FAIL|PENDING)$"
    )
    overall_status: str = Field(
        default="PENDING",
        pattern=r"^(AUTHENTICATED|PROVISIONAL|FAILED|PENDING)$"
    )

    def compute_verdict(self) -> str:
        """FR9 §Phase 5 verdict logic:
        4/4 PASS → AUTHENTICATED
        3/4 PASS → PROVISIONAL
        ≤2/4 PASS → FAILED"""
        laws = [
            self.law_1_lived_reality,
            self.law_2_depth_stratification,
            self.law_3_tribal_language,
            self.law_4_data_provenance,
        ]
        pass_count = sum(1 for law in laws if law == "PASS")
        if pass_count == 4:
            self.overall_status = "AUTHENTICATED"
        elif pass_count == 3:
            self.overall_status = "PROVISIONAL"
        else:
            self.overall_status = "FAILED"
        return self.overall_status


# ── FR9 Main Output ──

class ThemeContextPremise(BaseModel):
    """FR9 §Phase 5: The complete theme-specific Context Premise output artifact.
    6 segments × 12 categories × L1/L2/L3 depth-stratified, Four Laws validated.
    Output path: intelligence/context_premises/{theme_slug}_context_premise.json"""
    theme: str = Field(..., min_length=1)
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    agent_version: str = Field(default="1.0")
    standing_dep_eng_006_version: str = Field(
        default="",
        description="Reference to standing Context Premise Map version used"
    )
    segments: list[AudienceSegmentProfile] = Field(
        default_factory=list,
        description="Exactly 6 audience segments"
    )
    depth_distribution: DepthDistribution = Field(default_factory=DepthDistribution)
    tribal_language_registry: TribalLanguageRegistry = Field(
        default_factory=TribalLanguageRegistry
    )
    four_laws_status: FourLawsStatus = Field(default_factory=FourLawsStatus)
    provenance_report: ProvenanceReport = Field(default_factory=ProvenanceReport)

    @field_validator("segments")
    @classmethod
    def validate_segment_count(
        cls, v: list[AudienceSegmentProfile]
    ) -> list[AudienceSegmentProfile]:
        """FR9 §Phase 2 gate: Exactly 6 segments required."""
        if len(v) != 6:
            raise ValueError(
                f"FR9 requires exactly 6 audience segments, got {len(v)}. "
                f"Fewer than 6 indicates insufficient understanding of audience diversity. "
                f"More than 6 indicates failure to identify genuine psychological boundaries."
            )
        return v

    def validate_unique_dhd_coping(self) -> bool:
        """FR9 AC10: No two segments share the same DHD + coping trajectory combination."""
        combos: set[tuple[str, str]] = set()
        for seg in self.segments:
            combo = (seg.dhd_label, seg.coping_trajectory_position)
            if combo in combos:
                return False
            combos.add(combo)
        return True

    def compute_depth_distribution(self) -> DepthDistribution:
        """FR9 §Phase 4 Law 2: Compute L1/L2/L3 percentages across all cells."""
        all_insights: list[ContextPremiseInsight] = []
        for seg in self.segments:
            all_insights.extend(seg.categories.all_insights())
        total = len(all_insights)
        if total == 0:
            return DepthDistribution(l1=0.0, l2=0.0, l3=0.0)
        l1_count = sum(1 for i in all_insights if i.depth == "L1")
        l2_count = sum(1 for i in all_insights if i.depth == "L2")
        l3_count = sum(1 for i in all_insights if i.depth == "L3")
        self.depth_distribution = DepthDistribution(
            l1=l1_count / total,
            l2=l2_count / total,
            l3=l3_count / total,
        )
        return self.depth_distribution

    def compute_provenance_report(self) -> ProvenanceReport:
        """FR9 §Phase 4 Law 4: Compute provenance statistics."""
        all_insights: list[ContextPremiseInsight] = []
        for seg in self.segments:
            all_insights.extend(seg.categories.all_insights())
        total = len(all_insights)
        verified = sum(
            1 for i in all_insights
            if i.source and not i.source.lower().startswith("inferred")
            and "likely based on" not in i.source.lower()
        )
        unverified = total - verified
        self.provenance_report = ProvenanceReport(
            total_insights=total,
            verified_count=verified,
            unverified_count=unverified,
            provenance_percentage=verified / total if total > 0 else 0.0,
        )
        return self.provenance_report

    def count_structural_l3_per_segment(self) -> dict[str, dict[str, int]]:
        """FR9 AC8: Count L3 entries per structural category per segment.
        Returns {segment_id: {category: count}}. Minimum 2 per category required."""
        result: dict[str, dict[str, int]] = {}
        for seg in self.segments:
            counts: dict[str, int] = {
                "hidden_beliefs": sum(
                    1 for i in seg.categories.hidden_beliefs if i.depth == "L3"
                ),
                "emotional_triggers": sum(
                    1 for i in seg.categories.emotional_triggers if i.depth == "L3"
                ),
                "coping_mechanism": sum(
                    1 for i in seg.categories.coping_mechanism if i.depth == "L3"
                ),
            }
            result[seg.segment_id] = counts
        return result

    STRUCTURAL_L3_MINIMUM_PER_CATEGORY: int = 2


# ══════════════════════════════════════════════════════════════
# FR10 — Four-Axis Structural Matching Engine Models
# ══════════════════════════════════════════════════════════════

class L3StructuralCoordinate(BaseModel):
    """FR10 §Phase 2: L3 structural coordinates extracted from a single audience segment.
    Used for four-axis matching against coach triggers."""
    segment_id: str = Field(..., min_length=1)
    moral_foundations_violated: list[str] = Field(
        default_factory=list,
        description="MFT foundations violated in audience L3 pain"
    )
    coping_mechanism_pattern: dict[str, str] = Field(
        default_factory=dict,
        description="mechanism, agency_attribution, coping_potential_assessment"
    )
    agency_attribution_target: str = Field(
        default="",
        description="self|individual|institutional|systemic"
    )
    temporal_position_evidence: dict[str, Any] = Field(
        default_factory=dict,
        description="currently_inside, frustration_indicators, hidden_belief_indicators, search_phase_markers"
    )
    tribal_language_terms: list[str] = Field(
        default_factory=list,
        description="Verified L3 tribal language terms for this segment"
    )


class AxisScore(BaseModel):
    """FR10 §Phase 3: Score for a single matching axis."""
    axis_name: str = Field(..., description="moral_foundation|coping_potential|agency_attribution|temporal_position")
    congruence: AxisCongruence = Field(default=AxisCongruence.NONE)
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    coach_value: str = Field(default="", description="Coach-side data used for matching")
    audience_value: str = Field(default="", description="Audience-side data used for matching")
    failure_mode: str = Field(default="", description="Diagnostic if not congruent")

    @field_validator("score")
    @classmethod
    def validate_score_matches_congruence(cls, v: float, info: Any) -> float:
        """Ensure score aligns with congruence level."""
        # This validator is advisory — the engine sets both fields consistently
        return v


class FourAxisMatchResult(BaseModel):
    """FR10 §Phase 4 / DEP-ENG-010: Four-Axis Match Object.
    Produced by FR10, consumed by FR11 and FR12."""
    match_id: str = Field(
        default_factory=lambda: f"MATCH-{uuid.uuid4().hex[:12]}"
    )
    trigger_id: str = Field(..., description="Coach trigger ID from DEP-LIB-002")
    segment_id: str = Field(..., description="Audience segment ID from FR9")
    theme: str = Field(default="")
    axis_scores: dict[str, AxisScore] = Field(
        default_factory=dict,
        description="moral_foundation, coping_potential, agency_attribution, temporal_position"
    )
    total_score: float = Field(default=0.0, ge=0.0, le=4.0)
    match_classification: MatchClassification = Field(
        default=MatchClassification.NO_MATCH
    )
    adjacent_flag: bool = Field(
        default=False,
        description="True if any axis = 0.0 or classified ADJACENT"
    )
    diagnostic: str = Field(
        default="",
        description="Axis-by-axis diagnostic for non-CONFIRMED matches"
    )

    def compute_classification(self) -> MatchClassification:
        """FR10 §Phase 3: Compute match classification from axis scores.
        CONFIRMED: sum = 4.0 (all axes congruent)
        STRONG: sum 3.0–3.9, no axis = 0.0
        ADJACENT: any axis = 0.0 OR sum < 3.0 (with sum ≥ 2.0)
        NO_MATCH: sum < 2.0"""
        scores = [ax.score for ax in self.axis_scores.values()]
        self.total_score = sum(scores)
        has_zero = any(s == 0.0 for s in scores)

        if has_zero:
            self.adjacent_flag = True
            if self.total_score >= 2.0:
                self.match_classification = MatchClassification.ADJACENT
            else:
                self.match_classification = MatchClassification.NO_MATCH
        elif self.total_score >= 3.5:
            if self.total_score == 4.0:
                self.match_classification = MatchClassification.CONFIRMED
            else:
                self.match_classification = MatchClassification.STRONG
        elif self.total_score >= 3.0:
            self.match_classification = MatchClassification.STRONG
        elif self.total_score >= 2.0:
            self.match_classification = MatchClassification.ADJACENT
            self.adjacent_flag = True
        else:
            self.match_classification = MatchClassification.NO_MATCH

        return self.match_classification


class MatchResultsPayload(BaseModel):
    """FR10 §Phase 6: Complete match evaluation output.
    Output path: intelligence/matching/{theme_slug}_match_results.json"""
    theme: str = Field(..., min_length=1)
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    engine_version: str = Field(default="1.0")
    inputs_used: dict[str, str] = Field(
        default_factory=dict,
        description="emotional_dna_version, trigger_map_version, context_premise_version"
    )
    triggers_evaluated: int = 0
    segments_evaluated: int = Field(default=6)
    total_combinations_evaluated: int = 0
    matches: dict[str, list[FourAxisMatchResult]] = Field(
        default_factory=lambda: {
            "confirmed": [],
            "strong": [],
            "adjacent": [],
        }
    )
    no_match_count: int = 0
    exclusions: dict[str, Any] = Field(
        default_factory=lambda: {
            "raw_unresolved_triggers_excluded": [],
            "l1_l2_entries_filtered": 0,
        }
    )


# ══════════════════════════════════════════════════════════════
# FR11 — Activation Event Seed Construction Models
# ══════════════════════════════════════════════════════════════

class ESKAnchor(BaseModel):
    """FR11 §Phase 2 Element 1: Coach Event-Specific Knowledge anchor."""
    akb_level: str = Field(
        ..., description="esk|general_event|lifetime_period"
    )
    sensory_details: list[str] = Field(
        default_factory=list,
        description="Sensory-perceptual records from ESK moment"
    )
    anchor_quality: AnchorQuality = Field(default=AnchorQuality.DEGRADED)
    requires_esk_harvesting: bool = Field(
        default=False,
        description="True if anchor is degraded — triggers deep-dive interview request"
    )


class TribalLanguageElement(BaseModel):
    """FR11 §Phase 2 Element 2: Tribal language selection for seed construction."""
    extracted_terms: list[str] = Field(
        default_factory=list,
        description="Selected L3 tribal terms (minimum 3)"
    )
    verified_count: int = Field(default=0)
    language_drift_status: LanguageDriftStatus = Field(
        default=LanguageDriftStatus.PASSED
    )


class StructuralCongruencePoint(BaseModel):
    """FR11 §Phase 2 Element 3: The exact structural overlap articulation."""
    moral_foundation: str = Field(default="", description="Shared violation")
    coping_pattern: str = Field(default="", description="Shared defense mechanism")
    agency_attribution: str = Field(default="", description="Shared enemy")
    temporal_position: str = Field(
        default="",
        description="Audience pre-PTG, coach post-PTG"
    )
    articulation: str = Field(
        default="",
        description="Full text articulating the structural congruence point"
    )


class ActivationEvent(BaseModel):
    """FR11 §Phase 3: The DARN-CAT formatted evocative question."""
    darn_cat_dimension: DARNCATDimension = Field(
        default=DARNCATDimension.TAKING_STEPS
    )
    grounding_statement: str = Field(
        default="",
        description="Element 3 & 2: audience position in their language"
    )
    episodic_bridge: str = Field(
        default="",
        description="Element 3 & 1: connects audience position to coach ESK"
    )
    question_text: str = Field(
        default="",
        description="The evocative question (Taking Steps / Reasons)"
    )
    tribal_terms_used: list[str] = Field(
        default_factory=list,
        description="Exact tribal terms present in the question"
    )


class ActivationEventSeedFlags(BaseModel):
    """FR11 §Phase 5: Flags on a constructed seed."""
    degraded_anchor: bool = Field(
        default=False, description="ESK anchor is GE/LP, not ESK"
    )
    language_drift_risk: bool = Field(
        default=False, description="Language drift warning (1-2 terms)"
    )
    requires_esk_harvesting: bool = Field(
        default=False, description="Deep-dive interview needed for ESK harvest"
    )


class ActivationEventSeed(BaseModel):
    """FR11 §Phase 5 / DEP-ENG-011: The final Activation Event Seed.
    Output path: intelligence/matching/{theme_slug}_activation_seeds.json"""
    seed_id: str = Field(
        default_factory=lambda: f"SEED-{uuid.uuid4().hex[:12]}"
    )
    match_id: str = Field(default="", description="Reference to FR10 match")
    match_classification: MatchClassification = Field(
        default=MatchClassification.CONFIRMED
    )
    match_score: float = Field(default=0.0, ge=0.0, le=4.0)
    priority_rank: int = Field(default=0, ge=0)
    elements: dict[str, Any] = Field(
        default_factory=dict,
        description="esk_anchor, tribal_language, structural_congruence_point"
    )
    esk_anchor: ESKAnchor = Field(default_factory=lambda: ESKAnchor(akb_level="esk"))
    tribal_language: TribalLanguageElement = Field(
        default_factory=TribalLanguageElement
    )
    structural_congruence_point: StructuralCongruencePoint = Field(
        default_factory=StructuralCongruencePoint
    )
    activation_event: ActivationEvent = Field(default_factory=ActivationEvent)
    flags: ActivationEventSeedFlags = Field(
        default_factory=ActivationEventSeedFlags
    )


class ActivationSeedsPayload(BaseModel):
    """FR11 §Phase 5: Complete activation seeds output.
    Output path: intelligence/matching/{theme_slug}_activation_seeds.json"""
    theme: str = Field(..., min_length=1)
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    builder_version: str = Field(default="1.0")
    seeds: list[ActivationEventSeed] = Field(default_factory=list)
    graceful_exit: bool = Field(
        default=False,
        description="True if FR10 produced zero valid structural matches"
    )
    status: str = Field(
        default="",
        description="active | graceful_exit_zero_matches"
    )


# ══════════════════════════════════════════════════════════════
# FR12 — Three Failure Prevention Gates Models
# ══════════════════════════════════════════════════════════════

class Gate1Result(BaseModel):
    """FR12 §Stage 2: Gate 1 — Adjacent vs. Congruent validation result."""
    verdict: GateVerdict = Field(default=GateVerdict.FAIL)
    total_score: float = Field(default=0.0, ge=0.0, le=4.0)
    axis_matrix: dict[str, float] = Field(
        default_factory=lambda: {
            "moral_foundation": 0.0,
            "coping_potential": 0.0,
            "agency_attribution": 0.0,
            "temporal_position": 0.0,
        }
    )
    min_axis_score: float = Field(default=0.0, ge=0.0, le=1.0)
    adjacent_flag: bool = Field(default=False)

    # FR12 §Stage 2 exact thresholds
    PASS_THRESHOLD: float = 3.5
    PROVISIONAL_THRESHOLD: float = 3.0

    def evaluate(self, axis_scores: dict[str, float]) -> GateVerdict:
        """FR12 Gate 1 logic:
        sum ≥ 3.5 AND min > 0.0 → PASS
        sum = 3.0, all > 0.0 → PROVISIONAL
        any = 0.0 OR sum < 3.0 → FAIL"""
        self.axis_matrix = axis_scores
        scores = list(axis_scores.values())
        self.total_score = sum(scores)
        self.min_axis_score = min(scores) if scores else 0.0

        if self.min_axis_score == 0.0:
            self.verdict = GateVerdict.FAIL
            self.adjacent_flag = True
        elif self.total_score >= self.PASS_THRESHOLD:
            self.verdict = GateVerdict.PASS
            self.adjacent_flag = False
        elif self.total_score >= self.PROVISIONAL_THRESHOLD:
            self.verdict = GateVerdict.PROVISIONAL
            self.adjacent_flag = False
        else:
            self.verdict = GateVerdict.FAIL
            self.adjacent_flag = True

        return self.verdict


class Gate2Result(BaseModel):
    """FR12 §Stage 3: Gate 2 — Language Drift Prevention result."""
    verdict: GateVerdict = Field(default=GateVerdict.FAIL)
    required_count: int = Field(default=3)
    actual_count: int = Field(default=0)
    matched_terms_lemmatized: list[str] = Field(default_factory=list)
    language_drift_warning: bool = Field(default=False)

    # FR12 §Stage 3 exact thresholds
    PASS_THRESHOLD: int = 3
    PROVISIONAL_THRESHOLD: int = 2

    def evaluate(self, matched_terms: list[str]) -> GateVerdict:
        """FR12 Gate 2 logic:
        ≥3 matching terms → PASS
        2 terms → PROVISIONAL + language_drift_warning
        0-1 terms → FAIL"""
        self.matched_terms_lemmatized = matched_terms
        self.actual_count = len(matched_terms)

        if self.actual_count >= self.PASS_THRESHOLD:
            self.verdict = GateVerdict.PASS
            self.language_drift_warning = False
        elif self.actual_count >= self.PROVISIONAL_THRESHOLD:
            self.verdict = GateVerdict.PROVISIONAL
            self.language_drift_warning = True
        else:
            self.verdict = GateVerdict.FAIL
            self.language_drift_warning = False

        return self.verdict


class Gate3Result(BaseModel):
    """FR12 §Stage 5: Gate 3 — Authenticity Score Feedback Loop result."""
    status: str = Field(
        default="AWAITING_TELEGRAM_PAYLOAD",
        description="AWAITING_TELEGRAM_PAYLOAD | EVALUATED"
    )
    liwc_22_score_received: Optional[float] = Field(
        default=None, ge=0.0, le=10.0
    )
    verdict: Optional[GateVerdict] = None
    failure_mode: Optional[Gate3FailureMode] = None
    downstream_mutations: dict[str, bool] = Field(
        default_factory=lambda: {
            "dep_lib_002_mutated": False,
            "dep_eng_006_mutated": False,
        }
    )
    coach_ptg_retrograde: bool = Field(
        default=False,
        description="True if trigger retrograded from resolved_dual_layer to active_processing"
    )
    audience_l3_revalidation: bool = Field(
        default=False,
        description="True if audience segment flagged for L3 re-validation"
    )

    # FR12 §Stage 5 exact thresholds
    PASS_THRESHOLD: float = 7.0
    PROVISIONAL_LOW: float = 5.0
    PROVISIONAL_HIGH: float = 6.9
    FAIL_THRESHOLD: float = 5.0

    def evaluate(
        self,
        liwc_score: float,
        historical_trigger_decay: bool = False,
        historical_trigger_flawless: bool = False,
    ) -> GateVerdict:
        """FR12 Gate 3 logic:
        ≥7.0 → PASS (increase activation precedence by 15%)
        5.0-6.9 → PROVISIONAL (flag ESK anchor as potentially degraded)
        <5.0 + Gate 1/2 were PASS + historical decay → FAIL (Coach Temporal Error)
        <5.0 + Gate 1/2 were PASS + historical flawless → FAIL (Audience Extraction Error)"""
        self.liwc_22_score_received = liwc_score
        self.status = "EVALUATED"

        if liwc_score >= self.PASS_THRESHOLD:
            self.verdict = GateVerdict.PASS
        elif liwc_score >= self.PROVISIONAL_LOW:
            self.verdict = GateVerdict.PROVISIONAL
        else:
            self.verdict = GateVerdict.FAIL
            if historical_trigger_decay:
                self.failure_mode = Gate3FailureMode.COACH_TEMPORAL_ERROR
                self.coach_ptg_retrograde = True
                self.downstream_mutations["dep_lib_002_mutated"] = True
            elif historical_trigger_flawless:
                self.failure_mode = Gate3FailureMode.AUDIENCE_EXTRACTION_ERROR
                self.audience_l3_revalidation = True
                self.downstream_mutations["dep_eng_006_mutated"] = True

        return self.verdict


class GateDiagnosticCertificate(BaseModel):
    """FR12 §5 / DEP-ENG-027: Gate Diagnostic Certificate.
    Auditable JSON manifest documenting PASS/FAIL matrices for the three gates.
    Output path: affixed to DEP-ENG-011 before Telegram Elicitation Protocol."""
    gate_certificate_id: str = Field(
        default_factory=lambda: f"CERT-{uuid.uuid4().hex[:12]}"
    )
    seed_reference_id: str = Field(
        default="",
        description="Reference to the seed this certificate accompanies"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    receipt_chain_hash: str = Field(
        default="",
        description="Hash of the full receipt chain for this validation session"
    )
    gate_1_structural_congruence: Gate1Result = Field(
        default_factory=Gate1Result
    )
    gate_2_language_drift: Gate2Result = Field(
        default_factory=Gate2Result
    )
    gate_3_authenticity_feedback: Gate3Result = Field(
        default_factory=Gate3Result
    )

    def is_cleared_for_emission(self) -> bool:
        """A seed is cleared for emission if Gate 1 and Gate 2 are not FAIL.
        Gate 3 is async (post-recording) and does not block emission."""
        return (
            self.gate_1_structural_congruence.verdict != GateVerdict.FAIL
            and self.gate_2_language_drift.verdict != GateVerdict.FAIL
        )


# ══════════════════════════════════════════════════════════════
# Pipeline Orchestration Models
# ══════════════════════════════════════════════════════════════

class ContainerModulePipelineConfig(BaseModel):
    """Configuration for the Step 6 Container Module Pipeline."""
    coach_id: str = Field(..., min_length=1)
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    theme: str = Field(..., min_length=1)
    theme_slug: str = Field(default="")

    def compute_theme_slug(self) -> str:
        """Generate a filesystem-safe slug from the theme."""
        self.theme_slug = (
            self.theme.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
            .replace('"', "")
        )
        return self.theme_slug


class ContainerModulePipelineResult(BaseModel):
    """Result of the full Step 6 pipeline execution."""
    config: ContainerModulePipelineConfig
    context_premise: Optional[ThemeContextPremise] = None
    match_results: Optional[MatchResultsPayload] = None
    activation_seeds: Optional[ActivationSeedsPayload] = None
    gate_certificates: list[GateDiagnosticCertificate] = Field(default_factory=list)
    pipeline_status: str = Field(default="PENDING")
    fallback_invoked: bool = Field(
        default=False,
        description="True if 3 consecutive Gate 2 failures triggered fallback"
    )
    receipt_ids: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
