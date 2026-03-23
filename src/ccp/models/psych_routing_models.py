"""
CCP FR18 Psychological Routing Brief Generator — Data Models (Unit 1)
Pydantic v2 models for DEP-ENG-016, DEP-ENG-017 (input), DEP-ENG-018 (input).

Spec reference: FR18_Psychological_Routing_Brief_Tech_Spec.md
Architecture reference: Mood_State_Architecture_Documentation, CCP_Evolution_Architecture_Report_V3 §Stage 3

DEP-ENG-016: Psychological Routing Brief — PRIMARY OUTPUT of this engine.
             Injected into Block B (field_3_context) of the compilation template.
DEP-ENG-017: Audience Maturity Profile — INPUT from batch sequencer (Step 4).
DEP-ENG-018: Mood Context Map — INPUT from live psychometric feed (Step 4).

Academic grounding (spec §3):
  Uses & Gratifications Theory (Katz & Blumler 1973)   → mood_state_primary / mood_state_secondary
  Mood Management Theory (Zillmann 1988)                → arousal_direction / valence_delivery
  Self-Determination Theory (Deci & Ryan 1985)          → sdt_need_primary
  Social Comparison Theory (Festinger 1954)             → comparison_type
  Regulatory Focus Theory (Higgins 1997)                → regulatory_frame
  Terror Management Theory (Greenberg et al. 1986)      → tmt_function

All variable resolution is DETERMINISTIC — matrix lookup only, no LLM inference (spec §3 §Technical Decisions).
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Input Enums ─────────────────────────────────────────────────────────────


class MoodStatePrimary(str, Enum):
    """Four primary mood states from Uses & Gratifications Theory (Katz & Blumler 1973).

    Spec §4 Stage 2 Variable 1:
    Fetched directly from the batch composer allocation slot assigned to this run.
    """
    PROCESSING = "Processing"
    ESCAPE = "Escape"
    DISCOVERY = "Discovery"
    STATUS = "Status"


class AudienceArousalLevel(str, Enum):
    """Current audience arousal level — input from DEP-ENG-018.

    Used by Zillmann Mood Management Theory to compute arousal_direction (AC1).
    """
    HIGH = "HIGH"
    LOW = "LOW"
    NEUTRAL = "NEUTRAL"


class AudienceValencePolarity(str, Enum):
    """Current audience valence polarity — input from DEP-ENG-018.

    Used together with arousal to identify the Mood State quadrant.
    """
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class AudienceMaturityCohort(str, Enum):
    """Audience maturity cohort from DEP-ENG-017 — binding for TMT function.

    Spec §4 Stage 2 Variable 7 (tmt_function):
    - Loyal (long-term) → worldview_construction
    - New / Developing → insight_delivery
    """
    NEW = "New"           # 0–4 weeks (spec AC2 citation: "New (0-4wk)")
    DEVELOPING = "Developing"
    LOYAL = "Loyal"


class RegulatoryOrientation(str, Enum):
    """Audience language marker orientation — from DEP-ENG-018 LIWC-22 analysis.

    Drives regulatory_frame resolution (Higgins 1997 Regulatory Focus Theory).
    """
    GAIN_SEEKING = "gain_seeking"
    THREAT_AVOIDANT = "threat_avoidant"


class SemanticAffinityRisk(str, Enum):
    """Pain Map collision risk — passed through from DEP-ENG-018.

    Spec §5 Output Schema: provided as pass-through <low/medium/high>.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ─── Output Enums ─────────────────────────────────────────────────────────────


class ArousalDirection(str, Enum):
    """Resolved arousal direction — Mood Management Theory output.

    Spec §4 Variable 2:
      HIGH audience arousal → <lowers>
      LOW audience arousal  → <raises>
      Discovery mood        → <maintains>
    """
    LOWERS = "lowers"
    RAISES = "raises"
    MAINTAINS = "maintains"


class ValenceDelivery(str, Enum):
    """Resolved valence/atmosphere — mood state dependent.

    Spec §4 Variable 3:
      Escape     → positive
      Discovery  → positive
      Status     → mixed
      Processing → eudaimonic
    """
    POSITIVE = "positive"
    MIXED = "mixed"
    EUDAIMONIC = "eudaimonic"


class RegulatoryFrame(str, Enum):
    """Resolved regulatory frame — Higgins 1997.

    Spec §4 Variable 4:
      gain-seeking    → promotion
      threat-avoidant → prevention
    """
    PROMOTION = "promotion"
    PREVENTION = "prevention"


class SDTNeedPrimary(str, Enum):
    """Self-Determination Theory primary need — 1:1 bound to mood state.

    Spec §4 Variable 5 (second item 4, actually Variable 5):
      Escape     → relief
      Discovery  → competence
      Status     → autonomy
      Processing → relatedness
    """
    RELIEF = "relief"
    COMPETENCE = "competence"
    AUTONOMY = "autonomy"
    RELATEDNESS = "relatedness"


class SequencingDependency(str, Enum):
    """Sequencing constraint — Discovery mode requires positive prime.

    Spec §4 Variable 6:
      Discovery → requires_positive_prime
      Else      → independent
    """
    REQUIRES_POSITIVE_PRIME = "requires_positive_prime"
    INDEPENDENT = "independent"


class ComparisonType(str, Enum):
    """Social comparison type — Social Comparison Theory (Festinger 1954).

    Spec §4 Variable 7:
      Evaluated only if Mood State == Status.
      Status + New     → upward_assimilation
      Status + Dev/Loyal → worldview_validation
      Else             → none
    """
    UPWARD_ASSIMILATION = "upward_assimilation"
    WORLDVIEW_VALIDATION = "worldview_validation"
    NONE = "none"


class TMTFunction(str, Enum):
    """Terror Management Theory function — Greenberg et al. 1986.

    Spec §4 Variable 8:
      Evaluated only if Mood == Processing.
      Processing + Loyal       → worldview_construction
      Processing + New/Dev     → insight_delivery
      Else                     → none
    """
    WORLDVIEW_CONSTRUCTION = "worldview_construction"
    INSIGHT_DELIVERY = "insight_delivery"
    NONE = "none"


# ─── Input Models ─────────────────────────────────────────────────────────────


class MoodContextMap(BaseModel):
    """DEP-ENG-018 — Live psychometric feed summary for the active batch slot.

    FR18 input. Produced by the Smart Batch Sequencer / Audience Monitor Agent (Step 4).
    When unavailable, the engine falls back to NeutralProcessingProxyState.
    """
    mood_state_primary: MoodStatePrimary = Field(
        description="Primary mood state allocation for this batch slot."
    )
    mood_state_secondary: Optional[MoodStatePrimary] = Field(
        default=None,
        description="Secondary mood state (if dual-mode batch slot).",
    )
    audience_arousal_level: AudienceArousalLevel = Field(
        description="Current audience arousal level from psychometric feed."
    )
    audience_valence_polarity: AudienceValencePolarity = Field(
        description="Current audience valence polarity."
    )
    regulatory_orientation: RegulatoryOrientation = Field(
        description="Audience language orientation — LIWC-22 inferred."
    )
    semantic_affinity_risk: SemanticAffinityRisk = Field(
        default=SemanticAffinityRisk.LOW,
        description="Pain Map collision risk — pass-through from batch sequencer.",
    )
    batch_slot_id: Optional[str] = Field(
        default=None,
        description="Batch slot identifier for receipt chaining.",
    )
    coach_id: Optional[str] = Field(
        default=None,
        description="Coach ID — enforces ADR-01 single-tenant isolation (AC4).",
    )


class AudienceMaturityProfile(BaseModel):
    """DEP-ENG-017 — Audience maturity cohort profile for the active coach.

    FR18 input. Produced by Audience Maturity Lifecycle (FR20, Step 4).
    When unavailable, defaults to NEW cohort in the fallback path.
    """
    maturity_cohort: AudienceMaturityCohort = Field(
        description="Audience maturity cohort classification."
    )
    coach_id: str = Field(
        description="Coach ID — enforces ADR-01 single-tenant isolation (AC4)."
    )
    cohort_age_weeks: Optional[int] = Field(
        default=None,
        description="Average cohort age in weeks (informational).",
    )
    profile_version: str = Field(
        default="1.0",
        description="Schema version for forward-compatibility.",
    )


# ─── Output Models ────────────────────────────────────────────────────────────


class PsychologicalClassification(BaseModel):
    """The 8-variable psychological classification block — core of DEP-ENG-016.

    All 8 variables resolved deterministically by the matrix engine (spec §4).
    """
    mood_state_primary: MoodStatePrimary = Field(
        description="Primary mood state (pass-through from DEP-ENG-018 or default)."
    )
    arousal_direction: ArousalDirection = Field(
        description="Inversely mapped arousal modulation directive (Zillmann 1988)."
    )
    valence_delivery: ValenceDelivery = Field(
        description="Emotional polarity/atmosphere directive."
    )
    regulatory_frame: RegulatoryFrame = Field(
        description="Regulatory orientation directive (Higgins 1997)."
    )
    sdt_need_primary: SDTNeedPrimary = Field(
        description="Self-Determination Theory primary need (Deci & Ryan 1985)."
    )
    sequencing_dependency: SequencingDependency = Field(
        description="Sequencing constraint for Discovery mode."
    )
    comparison_type: ComparisonType = Field(
        description="Social comparison type (Festinger 1954) — Status mode only."
    )
    tmt_function: TMTFunction = Field(
        description="Terror Management Theory function (Greenberg 1986) — Processing mode only."
    )
    semantic_affinity_risk: SemanticAffinityRisk = Field(
        default=SemanticAffinityRisk.LOW,
        description="Pain Map collision risk — pass-through from DEP-ENG-018.",
    )


class PsychRoutingBrief(BaseModel):
    """DEP-ENG-016 — Psychological Routing Brief.

    Primary output of the FR18 engine. Injected into Block B (field_3_context)
    of the JIT compilation template.

    Spec §5 Output Schema: psych_routing_brief.json
    """
    routing_id: str = Field(
        description="Unique routing brief identifier (e.g. PRB-20260313-001)."
    )
    receipt_chain_hash: str = Field(
        default="",
        description="Hash from the final receipt write (Stage 3).",
    )
    coach_id: Optional[str] = Field(
        default=None,
        description="Coach ID — ADR-01 single-tenant isolation (AC4).",
    )
    psychological_classification: PsychologicalClassification = Field(
        description="8-variable resolved classification block."
    )
    payload_masking_instruction: str = Field(
        description=(
            "Literal instruction string injected into the Emilio prompt. "
            "Keyed to mood_state_primary. Forces Trojan Horse structural behavior."
        )
    )
    is_fallback: bool = Field(
        default=False,
        description="True if DEP-ENG-018 was unavailable and Neutral Processing Proxy State was used.",
    )
    operator_warning: Optional[str] = Field(
        default=None,
        description="OPERATOR_WARNING message when is_fallback=True (spec §6).",
    )


# ─── Fallback State ───────────────────────────────────────────────────────────


NEUTRAL_PROCESSING_PROXY_STATE = MoodContextMap(
    mood_state_primary=MoodStatePrimary.PROCESSING,
    audience_arousal_level=AudienceArousalLevel.NEUTRAL,
    audience_valence_polarity=AudienceValencePolarity.NEUTRAL,
    regulatory_orientation=RegulatoryOrientation.GAIN_SEEKING,
    semantic_affinity_risk=SemanticAffinityRisk.LOW,
)
"""
Spec §6 Fallback:
  Arousal = 'maintains', Regulatory = 'promotion', Semantic Risk = 'lowered_by_default'.
  Used when DEP-ENG-018 is unavailable.
"""

NEUTRAL_PROCESSING_PROXY_MATURITY = AudienceMaturityProfile(
    maturity_cohort=AudienceMaturityCohort.NEW,
    coach_id="fallback",
)
"""Default maturity profile for fallback path — NEW cohort ensures conservative TMT routing."""

OPERATOR_WARNING_FALLBACK = (
    "OPERATOR_WARNING: Psychological Routing Brief generated via Neutral Processing Proxy State "
    "because DEP-ENG-018 (Mood Context Map) was unavailable. "
    "Brief relies on static defaults rather than live psychometric reading. "
    "Compilation continues normally, relying on DEP-ENG-005 TTT profile."
)
