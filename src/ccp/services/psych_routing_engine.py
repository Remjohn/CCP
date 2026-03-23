"""
CCP FR18 Psychological Routing Brief Generator — Variable Resolution Matrix Engine (Unit 3)
Deterministic 8-variable resolution from DEP-ENG-018 + DEP-ENG-017 inputs.

Spec reference: FR18_Psychological_Routing_Brief_Tech_Spec.md §4 Stage 2
Architecture:   All mapping is matrix lookup — NO LLM inference (spec §3 §Technical Decisions).

Resolution logic (exact spec §4 decision tables):

Variable 1 — mood_state_primary:
  Pass-through from DEP-ENG-018 batch slot assignment.

Variable 2 — arousal_direction (Zillmann 1988, AC1):
  HIGH arousal  → lowers
  LOW arousal   → raises
  Discovery     → maintains (overrides arousal level)

Variable 3 — valence_delivery:
  Escape     → positive
  Discovery  → positive
  Status     → mixed
  Processing → eudaimonic

Variable 4 — regulatory_frame (Higgins 1997):
  gain_seeking    → promotion
  threat_avoidant → prevention

Variable 5 — sdt_need_primary (Deci & Ryan 1985, AC3):
  Escape     → relief
  Discovery  → competence
  Status     → autonomy
  Processing → relatedness

Variable 6 — sequencing_dependency:
  Discovery → requires_positive_prime
  Else      → independent

Variable 7 — comparison_type (Festinger 1954):
  Status + New       → upward_assimilation
  Status + Dev/Loyal → worldview_validation
  Else               → none

Variable 8 — tmt_function (Greenberg et al. 1986, AC2):
  Processing + Loyal      → worldview_construction
  Processing + New/Dev    → insight_delivery
  Else                    → none

Variable 9 — semantic_affinity_risk:
  Pass-through from DEP-ENG-018.
"""

from src.ccp.models.psych_routing_models import (
    ArousalDirection,
    AudienceArousalLevel,
    AudienceMaturityCohort,
    AudienceMaturityProfile,
    ComparisonType,
    MoodContextMap,
    MoodStatePrimary,
    PsychologicalClassification,
    RegulatoryFrame,
    RegulatoryOrientation,
    SDTNeedPrimary,
    SemanticAffinityRisk,
    SequencingDependency,
    TMTFunction,
    ValenceDelivery,
)


class PsychVariableMatrix:
    """Deterministic matrix engine resolving the 8 FR18 psychological variables.

    Implements spec §4 Stage 2 exactly — no inference, no fuzzy logic.
    All decisions are table lookups.
    """

    def resolve(
        self,
        mood_context: MoodContextMap,
        maturity_profile: AudienceMaturityProfile,
    ) -> PsychologicalClassification:
        """Resolve all 8 psychological variables from the input context.

        Args:
            mood_context: DEP-ENG-018 — provides mood state, arousal, valence,
                regulatory orientation, semantic risk.
            maturity_profile: DEP-ENG-017 — provides maturity cohort for
                TMT and comparison_type resolution.

        Returns:
            PsychologicalClassification with all 8 variables resolved.
        """
        mood = mood_context.mood_state_primary

        return PsychologicalClassification(
            mood_state_primary=mood,
            arousal_direction=self._resolve_arousal_direction(
                mood=mood,
                arousal_level=mood_context.audience_arousal_level,
            ),
            valence_delivery=self._resolve_valence_delivery(mood),
            regulatory_frame=self._resolve_regulatory_frame(
                mood_context.regulatory_orientation
            ),
            sdt_need_primary=self._resolve_sdt_need(mood),
            sequencing_dependency=self._resolve_sequencing_dependency(mood),
            comparison_type=self._resolve_comparison_type(
                mood=mood,
                cohort=maturity_profile.maturity_cohort,
            ),
            tmt_function=self._resolve_tmt_function(
                mood=mood,
                cohort=maturity_profile.maturity_cohort,
            ),
            semantic_affinity_risk=mood_context.semantic_affinity_risk,
        )

    # ─── Variable Resolvers ───────────────────────────────────────────────────

    def _resolve_arousal_direction(
        self,
        mood: MoodStatePrimary,
        arousal_level: AudienceArousalLevel,
    ) -> ArousalDirection:
        """Spec §4 Variable 2 — Zillmann Mood Management Theory (AC1).

        Discovery overrides arousal level → maintains.
        Otherwise inversely maps:
          HIGH → lowers
          LOW  → raises
          NEUTRAL → maintains
        """
        if mood == MoodStatePrimary.DISCOVERY:
            return ArousalDirection.MAINTAINS

        if arousal_level == AudienceArousalLevel.HIGH:
            return ArousalDirection.LOWERS
        elif arousal_level == AudienceArousalLevel.LOW:
            return ArousalDirection.RAISES
        else:
            return ArousalDirection.MAINTAINS

    def _resolve_valence_delivery(
        self, mood: MoodStatePrimary
    ) -> ValenceDelivery:
        """Spec §4 Variable 3.

        Escape     → positive  (humor, calming, relief)
        Discovery  → positive  (curiosity, expansive, awe)
        Status     → mixed     (aspirational, comparison-oriented)
        Processing → eudaimonic (heavy, meaningful, contemplative)
        """
        mapping: dict[MoodStatePrimary, ValenceDelivery] = {
            MoodStatePrimary.ESCAPE: ValenceDelivery.POSITIVE,
            MoodStatePrimary.DISCOVERY: ValenceDelivery.POSITIVE,
            MoodStatePrimary.STATUS: ValenceDelivery.MIXED,
            MoodStatePrimary.PROCESSING: ValenceDelivery.EUDAIMONIC,
        }
        return mapping[mood]

    def _resolve_regulatory_frame(
        self, orientation: RegulatoryOrientation
    ) -> RegulatoryFrame:
        """Spec §4 Variable 4 — Higgins 1997 Regulatory Focus Theory.

        gain_seeking    → promotion
        threat_avoidant → prevention
        """
        if orientation == RegulatoryOrientation.GAIN_SEEKING:
            return RegulatoryFrame.PROMOTION
        return RegulatoryFrame.PREVENTION

    def _resolve_sdt_need(self, mood: MoodStatePrimary) -> SDTNeedPrimary:
        """Spec §4 Variable 5 — Self-Determination Theory (Deci & Ryan 1985). AC3.

        1:1 bound to mood state:
        Escape     → relief
        Discovery  → competence
        Status     → autonomy
        Processing → relatedness
        """
        mapping: dict[MoodStatePrimary, SDTNeedPrimary] = {
            MoodStatePrimary.ESCAPE: SDTNeedPrimary.RELIEF,
            MoodStatePrimary.DISCOVERY: SDTNeedPrimary.COMPETENCE,
            MoodStatePrimary.STATUS: SDTNeedPrimary.AUTONOMY,
            MoodStatePrimary.PROCESSING: SDTNeedPrimary.RELATEDNESS,
        }
        return mapping[mood]

    def _resolve_sequencing_dependency(
        self, mood: MoodStatePrimary
    ) -> SequencingDependency:
        """Spec §4 Variable 6.

        Discovery → requires_positive_prime
        Else      → independent
        """
        if mood == MoodStatePrimary.DISCOVERY:
            return SequencingDependency.REQUIRES_POSITIVE_PRIME
        return SequencingDependency.INDEPENDENT

    def _resolve_comparison_type(
        self,
        mood: MoodStatePrimary,
        cohort: AudienceMaturityCohort,
    ) -> ComparisonType:
        """Spec §4 Variable 7 — Social Comparison Theory (Festinger 1954).

        Evaluated only if Mood State == Status.
        Status + New       → upward_assimilation
        Status + Dev/Loyal → worldview_validation
        Else               → none
        """
        if mood != MoodStatePrimary.STATUS:
            return ComparisonType.NONE

        if cohort == AudienceMaturityCohort.NEW:
            return ComparisonType.UPWARD_ASSIMILATION
        return ComparisonType.WORLDVIEW_VALIDATION  # Developing or Loyal

    def _resolve_tmt_function(
        self,
        mood: MoodStatePrimary,
        cohort: AudienceMaturityCohort,
    ) -> TMTFunction:
        """Spec §4 Variable 8 — Terror Management Theory (Greenberg et al. 1986). AC2.

        Evaluated only if Mood == Processing.
        Processing + Loyal      → worldview_construction
        Processing + New/Dev    → insight_delivery
        Else                    → none
        """
        if mood != MoodStatePrimary.PROCESSING:
            return TMTFunction.NONE

        if cohort == AudienceMaturityCohort.LOYAL:
            return TMTFunction.WORLDVIEW_CONSTRUCTION
        return TMTFunction.INSIGHT_DELIVERY  # New or Developing (AC2)
