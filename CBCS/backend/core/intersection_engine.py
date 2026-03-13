"""
Intersection Engine — Coach × Audience Structural Congruence

Computes the "Intersection-First" matching between coach and audience
profiles. This is the core algorithm of Proposal 6's Core Track.

Four matching dimensions:
    1. MFT Cosine Similarity: alignment of moral foundation vectors
    2. Regulatory Fit: same-orientation = full fit (Higgins)
    3. Reconsolidation Potential: coach threshold vs. audience sensitivity
    4. Coping Phase Appropriateness: content depth gating

Architecture: Coach Adapter + Audience Aggregator → Intersection Engine
Research: Proposal 6 (Hybrid Orchestrator), Higgins regulatory fit (1997)
"""

import math
from typing import Optional
from backend.core.audience_trigger_models import (
    CoachMatchVector,
    CohortContextPremise,
    IntersectionResult,
    IntersectionTheme,
    RegulatoryOrientation,
    CopingPhase,
    DataPhase,
)

# ─── Intersection Weights ───────────────────────────────────────────
WEIGHTS = {
    "mft_cosine": 0.35,
    "regulatory_fit": 0.25,
    "reconsolidation_potential": 0.20,
    "coping_appropriateness": 0.20,
}

# ─── Foundation Labels for Theme Generation ─────────────────────────
FOUNDATION_LABELS = {
    "care_harm": "Protection & Nurturing",
    "fairness_cheating": "Justice & Equity",
    "loyalty_betrayal": "Loyalty & Trust",
    "authority_subversion": "Leadership & Order",
    "sanctity_degradation": "Purity & Standards",
    "liberty_oppression": "Freedom & Autonomy",
}

# ─── Emotional Frames (CPM → Content Framing) ───────────────────────
FOUNDATION_TO_FRAME = {
    "care_harm": "compassion_frame",
    "fairness_cheating": "indignation_frame",
    "loyalty_betrayal": "loyalty_frame",
    "authority_subversion": "authority_frame",
    "sanctity_degradation": "purity_frame",
    "liberty_oppression": "liberation_frame",
}

# ─── Coping Phase → Content Depth ───────────────────────────────────
COPING_DEPTH_MAP = {
    CopingPhase.PRE_CONTEMPLATION: "AWARENESS",
    CopingPhase.SEARCH_PHASE: "FULL_DEPTH",
    CopingPhase.ACTIVE_COPING: "ACTION_ORIENTED",
    CopingPhase.MAINTENANCE: "REINFORCEMENT",
}


def _cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """
    Compute cosine similarity between two foundation weight vectors.

    Returns value between 0 and 1 (pre-clamped since all values are non-negative).
    """
    keys = set(vec_a.keys()) | set(vec_b.keys())
    dot = sum(vec_a.get(k, 0.0) * vec_b.get(k, 0.0) for k in keys)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return max(0.0, min(1.0, dot / (mag_a * mag_b)))


def _regulatory_fit_score(
    coach_orient: RegulatoryOrientation,
    audience_orient: RegulatoryOrientation,
) -> float:
    """
    Computes regulatory fit score per Higgins' theory.

    Same orientation = 1.0 (full regulatory fit).
    Cross-orientation = 0.3 (mismatch but still usable).
    Dual-dominant audience = 0.7 for any coach orientation.
    """
    if audience_orient == RegulatoryOrientation.DUAL_DOMINANT:
        return 0.7

    if coach_orient == audience_orient:
        return 1.0

    if coach_orient == RegulatoryOrientation.DUAL_DOMINANT:
        return 0.7

    return 0.3


def _reconsolidation_potential(
    coach_threshold: float,
    audience_sensitivity: float,
) -> float:
    """
    Cross-references coach's prediction error threshold with
    audience's prediction error sensitivity.

    High sensitivity (audience primed for schema revision) +
    low threshold (coach can easily trigger prediction error) =
    high reconsolidation potential.
    """
    # Normalize coach threshold: lower threshold = higher potential
    # Threshold is 1-10 scale, so invert and normalize
    coach_factor = max(0.0, min(1.0, 1.0 - (coach_threshold / 10.0)))

    # Simple product: both need to be high for high potential
    return round(audience_sensitivity * coach_factor, 3)


def _coping_appropriateness(coping_phase: CopingPhase) -> float:
    """
    Scores how appropriate content delivery is for the current coping phase.

    SEARCH_PHASE = highest (1.0) — peak receptivity.
    ACTIVE_COPING = high (0.8) — ready for action content.
    PRE_CONTEMPLATION = moderate (0.4) — only awareness content.
    MAINTENANCE = moderate (0.5) — reinforcement only.
    """
    scores = {
        CopingPhase.SEARCH_PHASE: 1.0,
        CopingPhase.ACTIVE_COPING: 0.8,
        CopingPhase.MAINTENANCE: 0.5,
        CopingPhase.PRE_CONTEMPLATION: 0.4,
    }
    return scores.get(coping_phase, 0.4)


def compute_intersection(
    coach: CoachMatchVector,
    audience: CohortContextPremise,
) -> IntersectionResult:
    """
    Computes structural congruence between coach and audience profiles.

    Produces a ranked list of intersection themes with composite scores
    based on MFT alignment, regulatory fit, reconsolidation potential,
    and coping phase appropriateness.

    Args:
        coach: CoachMatchVector from coach_profile_adapter.
        audience: CohortContextPremise from audience_aggregator.

    Returns:
        IntersectionResult with ranked themes and aggregate metrics.
    """
    # ── Dimension 1: MFT Cosine Similarity ──
    mft_cosine = _cosine_similarity(coach.mft_weights, audience.moral_emotion.foundation_weights)

    # ── Dimension 2: Regulatory Fit ──
    reg_fit = _regulatory_fit_score(
        coach.regulatory_orientation,
        audience.regulatory_focus.dominant_orientation,
    )

    # ── Dimension 3: Reconsolidation Potential ──
    recon_pot = _reconsolidation_potential(
        coach.mean_prediction_error_threshold,
        audience.reconsolidation.prediction_error_sensitivity,
    )

    # ── Dimension 4: Coping Appropriateness ──
    coping_approp = _coping_appropriateness(audience.coping_trajectory.phase)

    # ── Determine content depth from coping phase ──
    recommended_depth = COPING_DEPTH_MAP.get(
        audience.coping_trajectory.phase, "SURFACE"
    )

    # ── Generate Intersection Themes ──
    # Create one theme per foundation that has non-zero weight on BOTH sides
    themes = []
    for foundation_key in FOUNDATION_LABELS:
        coach_weight = coach.mft_weights.get(foundation_key, 0.0)
        audience_weight = audience.moral_emotion.foundation_weights.get(foundation_key, 0.0)

        # Only create theme if both coach and audience have signal
        if coach_weight > 0.05 and audience_weight > 0.05:
            # Theme-specific intersection score
            # Uses foundation-level alignment + global factors
            foundation_alignment = min(coach_weight, audience_weight) * 2  # Reward overlap
            foundation_alignment = min(1.0, foundation_alignment)

            theme_score = (
                WEIGHTS["mft_cosine"] * foundation_alignment +
                WEIGHTS["regulatory_fit"] * reg_fit +
                WEIGHTS["reconsolidation_potential"] * recon_pot +
                WEIGHTS["coping_appropriateness"] * coping_approp
            )

            # Find the coach trigger most aligned with this foundation
            matched_trigger_id = None
            # (In production, this would look up the coach's triggers
            # to find which one maps to this foundation)

            themes.append(IntersectionTheme(
                theme_label=FOUNDATION_LABELS[foundation_key],
                intersection_score=round(theme_score, 3),
                mft_alignment=round(foundation_alignment, 3),
                regulatory_fit=round(reg_fit, 3),
                reconsolidation_potential=round(recon_pot, 3),
                recommended_depth=recommended_depth,
                coach_trigger_id=matched_trigger_id,
            ))

    # Sort by intersection score (highest first)
    themes.sort(key=lambda t: t.intersection_score, reverse=True)

    return IntersectionResult(
        themes=themes,
        overall_mft_cosine=round(mft_cosine, 3),
        overall_regulatory_fit=round(reg_fit, 3),
        audience_coping_phase=audience.coping_trajectory.phase,
        audience_data_phase=audience.data_phase,
    )
