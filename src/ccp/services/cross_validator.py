"""
CCP FR4 Emotional DNA — Cross-Validation Service (Unit 6)
Phase 6: VALIDATE — Apply constraints A through D.

Spec reference: FR4 Tech Spec §Phase 6 VALIDATE

Constraint A — Provenance Check:
    Every non-null variable must have ≥1 evidence passage.
    Violation: force variable to null.

Constraint B — Triage Depth Enforcement:
    Variables blocked at LOW tier (V2, V4) must remain null.
    Violation: force variable to null.

Constraint C — Appraisal-MFT Coherence Rules:
    (1) High Care/Harm + system-level agency → expect low V1 for institutional triggers
    (2) High Liberty → expect institutional/systemic V5
    (3) High Loyalty → expect low V4 for betrayal-themed content
    (4) High Sanctity → expect moral_verdict_first V2
    "On any incoherence: flag for operator review. Do NOT auto-correct."

Constraint D — No Fabrication Gate:
    No variable may be invented without corpus evidence.
    Verify profile_hash matches re-computed hash.
"""

from src.ccp.models.emotional_dna_models import (
    CROSS_VALIDATION_MFT_DIVERGENCE_PCT,
    AgencyAttributionType,
    AppraisalSequenceType,
    CrossValidationResult,
    EmotionalDNAProfile,
    GranularityTriageResult,
    IncoherenceFlag,
    IncoherenceType,
    TriageTier,
)


class CrossValidator:
    """Validates the complete EmotionalDNAProfile against spec constraints.

    Spec §Phase 6: Four constraint checks. Returns a CrossValidationResult
    with pass/fail per constraint, incoherence flags, and nullified variables.
    """

    def validate(
        self,
        profile: EmotionalDNAProfile,
        triage_result: GranularityTriageResult,
    ) -> CrossValidationResult:
        """Run all four constraint checks.

        Args:
            profile: The fully extracted EmotionalDNAProfile.
            triage_result: The Phase 2 granularity triage result.

        Returns:
            CrossValidationResult with constraint outcomes.
        """
        result = CrossValidationResult()

        # Constraint A: Provenance
        self._check_constraint_a(profile, result)

        # Constraint B: Triage depth
        self._check_constraint_b(profile, triage_result, result)

        # Constraint C: Appraisal-MFT coherence
        self._check_constraint_c(profile, result)

        # Constraint D: No fabrication
        self._check_constraint_d(profile, result)

        # Set operator review flag if any incoherence
        if result.incoherence_flags:
            result.operator_review_required = True

        return result

    def _check_constraint_a(
        self,
        profile: EmotionalDNAProfile,
        result: CrossValidationResult,
    ) -> None:
        """Constraint A: Provenance Check.

        Every non-null variable must have ≥1 evidence passage.
        Violation: force variable to null.
        """
        nullified: list[str] = []
        appraisal = profile.appraisal_variables

        # V1
        v1 = appraisal.v1_trigger_specificity_threshold
        if v1.score is not None and len(v1.evidence_passages) < 1:
            appraisal.v1_trigger_specificity_threshold.score = None
            nullified.append("V1")

        # V2
        v2 = appraisal.v2_appraisal_sequence_ordering
        if v2.type is not None and len(v2.evidence_passages) < 1:
            appraisal.v2_appraisal_sequence_ordering.type = None
            nullified.append("V2")

        # V3
        v3 = appraisal.v3_coping_potential_pattern
        if v3.ratio is not None and len(v3.evidence_passages) < 1:
            appraisal.v3_coping_potential_pattern.ratio = None
            nullified.append("V3")

        # V4
        v4 = appraisal.v4_norm_compatibility_threshold
        if v4.score is not None and len(v4.evidence_passages) < 1:
            appraisal.v4_norm_compatibility_threshold.score = None
            nullified.append("V4")

        # V5
        v5 = appraisal.v5_agency_attribution_bias
        if v5.dominant is not None and len(v5.evidence_passages) < 1:
            appraisal.v5_agency_attribution_bias.dominant = None
            nullified.append("V5")

        # V6-V10b moral foundations
        mft = profile.moral_foundations
        foundation_vars = [
            ("V6", mft.v6_care_harm),
            ("V7", mft.v7_fairness_cheating),
            ("V8", mft.v8_loyalty_betrayal),
            ("V9", mft.v9_authority_subversion),
            ("V10", mft.v10_sanctity_degradation),
            ("V10b", mft.v10b_liberty_oppression),
        ]
        for name, fvar in foundation_vars:
            if fvar.weight is not None and len(fvar.evidence_passages) < 1:
                fvar.weight = None
                nullified.append(name)

        result.variables_forced_to_null.extend(nullified)
        result.constraint_a_passed = len(nullified) == 0

    def _check_constraint_b(
        self,
        profile: EmotionalDNAProfile,
        triage_result: GranularityTriageResult,
        result: CrossValidationResult,
    ) -> None:
        """Constraint B: Triage Depth Enforcement.

        At LOW tier: V2 and V4 must remain null.
        """
        nullified: list[str] = []
        tier = triage_result.tier

        if tier == TriageTier.LOW:
            appraisal = profile.appraisal_variables

            # V2 must be null at LOW
            if appraisal.v2_appraisal_sequence_ordering.type is not None:
                appraisal.v2_appraisal_sequence_ordering.type = None
                appraisal.v2_appraisal_sequence_ordering.percentage_breakdown = {}
                nullified.append("V2_triage_blocked")

            # V4 must be null at LOW
            if appraisal.v4_norm_compatibility_threshold.score is not None:
                appraisal.v4_norm_compatibility_threshold.score = None
                nullified.append("V4_triage_blocked")

        result.variables_forced_to_null.extend(nullified)
        result.constraint_b_passed = len(nullified) == 0

    def _check_constraint_c(
        self,
        profile: EmotionalDNAProfile,
        result: CrossValidationResult,
    ) -> None:
        """Constraint C: Appraisal-MFT Coherence Rules.

        4 rules checking cross-variable consistency.
        'On any incoherence: flag for operator review. Do NOT auto-correct.'
        """
        appraisal = profile.appraisal_variables
        mft = profile.moral_foundations
        flags: list[IncoherenceFlag] = []

        # Rule 1: High Care/Harm + system agency → expect low V1 for
        # institutional triggers
        care_weight = mft.v6_care_harm.weight
        v1_score = appraisal.v1_trigger_specificity_threshold.score
        v5_dominant = appraisal.v5_agency_attribution_bias.dominant

        if (
            care_weight is not None
            and care_weight > 0.3
            and v5_dominant in (
                AgencyAttributionType.INSTITUTIONAL,
                AgencyAttributionType.SYSTEMIC,
            )
            and v1_score is not None
            and v1_score > 7
        ):
            flags.append(IncoherenceFlag(
                incoherence_type=IncoherenceType.HIGH_CARE_SELF_AGENCY,
                description=(
                    "High Care/Harm weight with system-level agency attribution "
                    "but high trigger specificity — expected low V1 for "
                    "institutional triggers."
                ),
                conflicting_variables=["V1", "V5", "V6"],
                evidence_summary=(
                    f"V6 care_harm={care_weight}, V5={v5_dominant}, V1={v1_score}"
                ),
            ))

        # Rule 2: High Liberty → expect institutional/systemic V5
        liberty_weight = mft.v10b_liberty_oppression.weight
        if (
            liberty_weight is not None
            and liberty_weight > 0.25
            and v5_dominant is not None
            and v5_dominant not in (
                AgencyAttributionType.INSTITUTIONAL,
                AgencyAttributionType.SYSTEMIC,
            )
        ):
            flags.append(IncoherenceFlag(
                incoherence_type=IncoherenceType.HIGH_LIBERTY_SELF_AGENCY,
                description=(
                    "High Liberty/Oppression weight but V5 agency attribution "
                    "is not institutional/systemic as expected."
                ),
                conflicting_variables=["V5", "V10b"],
                evidence_summary=(
                    f"V10b liberty={liberty_weight}, V5={v5_dominant}"
                ),
            ))

        # Rule 3: High Loyalty → expect low V4 for betrayal-themed content
        loyalty_weight = mft.v8_loyalty_betrayal.weight
        v4_score = appraisal.v4_norm_compatibility_threshold.score
        if (
            loyalty_weight is not None
            and loyalty_weight > 0.25
            and v4_score is not None
            and v4_score > 6
        ):
            flags.append(IncoherenceFlag(
                incoherence_type=IncoherenceType.HIGH_LOYALTY_HIGH_NORM,
                description=(
                    "High Loyalty/Betrayal weight but high norm compatibility "
                    "threshold — expected low V4 for betrayal-themed content."
                ),
                conflicting_variables=["V4", "V8"],
                evidence_summary=(
                    f"V8 loyalty={loyalty_weight}, V4={v4_score}"
                ),
            ))

        # Rule 4: High Sanctity → expect moral_verdict_first V2
        sanctity_weight = mft.v10_sanctity_degradation.weight
        v2_type = appraisal.v2_appraisal_sequence_ordering.type
        if (
            sanctity_weight is not None
            and sanctity_weight > 0.25
            and v2_type is not None
            and v2_type != AppraisalSequenceType.MORAL_VERDICT_FIRST
        ):
            flags.append(IncoherenceFlag(
                incoherence_type=IncoherenceType.HIGH_SANCTITY_COPING_FIRST,
                description=(
                    "High Sanctity/Degradation weight but V2 appraisal sequence "
                    "is not moral_verdict_first as expected."
                ),
                conflicting_variables=["V2", "V10"],
                evidence_summary=(
                    f"V10 sanctity={sanctity_weight}, V2={v2_type}"
                ),
            ))

        result.incoherence_flags.extend(flags)
        result.constraint_c_passed = len(flags) == 0

    def _check_constraint_d(
        self,
        profile: EmotionalDNAProfile,
        result: CrossValidationResult,
    ) -> None:
        """Constraint D: No Fabrication Gate.

        Verify that every populated variable has genuine evidence,
        not just a default/empty value masquerading as populated.
        Verify profile hash integrity.
        """
        issues: list[str] = []

        # Check appraisal variables for fabrication
        appraisal = profile.appraisal_variables

        if (
            appraisal.v1_trigger_specificity_threshold.score is not None
            and not appraisal.v1_trigger_specificity_threshold.evidence_passages
        ):
            issues.append("V1 has score but no evidence — fabrication suspected")

        if (
            appraisal.v2_appraisal_sequence_ordering.type is not None
            and not appraisal.v2_appraisal_sequence_ordering.evidence_passages
        ):
            issues.append("V2 has type but no evidence — fabrication suspected")

        if (
            appraisal.v3_coping_potential_pattern.ratio is not None
            and not appraisal.v3_coping_potential_pattern.evidence_passages
        ):
            issues.append("V3 has ratio but no evidence — fabrication suspected")

        if (
            appraisal.v4_norm_compatibility_threshold.score is not None
            and not appraisal.v4_norm_compatibility_threshold.evidence_passages
        ):
            issues.append("V4 has score but no evidence — fabrication suspected")

        if (
            appraisal.v5_agency_attribution_bias.dominant is not None
            and not appraisal.v5_agency_attribution_bias.evidence_passages
        ):
            issues.append("V5 has dominant but no evidence — fabrication suspected")

        # Check MFT variables
        mft = profile.moral_foundations
        foundation_vars = [
            ("V6", mft.v6_care_harm),
            ("V7", mft.v7_fairness_cheating),
            ("V8", mft.v8_loyalty_betrayal),
            ("V9", mft.v9_authority_subversion),
            ("V10", mft.v10_sanctity_degradation),
            ("V10b", mft.v10b_liberty_oppression),
        ]
        for name, fvar in foundation_vars:
            if fvar.weight is not None and fvar.weight > 0 and not fvar.evidence_passages:
                issues.append(f"{name} has weight but no evidence — fabrication suspected")

        # Profile hash verification (re-compute and compare)
        if profile.profile_hash:
            original_hash = profile.profile_hash
            recomputed_hash = profile.compute_hash()
            if original_hash != recomputed_hash:
                issues.append(
                    f"Profile hash mismatch: original={original_hash[:16]}... "
                    f"recomputed={recomputed_hash[:16]}..."
                )

        result.constraint_d_passed = len(issues) == 0
        if issues:
            # Create incoherence flags for fabrication issues
            for issue in issues:
                result.incoherence_flags.append(IncoherenceFlag(
                    incoherence_type=IncoherenceType.HIGH_CARE_SELF_AGENCY,
                    description=f"Constraint D Fabrication: {issue}",
                    conflicting_variables=[],
                    evidence_summary=issue,
                ))
