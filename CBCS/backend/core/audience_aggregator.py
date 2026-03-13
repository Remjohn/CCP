"""
Audience Aggregator — Cohort-Level Context Premise Builder

Aggregates individual AudienceTriggerProfile objects into a single
CohortContextPremise for a segment/cohort. This is the bridge between
per-text scoring (Step 2) and the Intersection Engine (Step 5).

Key Design Decision: L-depth weighted averaging.
    L3 (authentic) texts get 3x weight.
    L2 (communal) texts get 1.5x weight.
    L1 (performative) texts get 1x weight.
This ensures raw, unpolished disclosures have disproportionate influence
on the aggregate profile, per the L-depth provenance chain.

Architecture: Scorers → Aggregator → Intersection Engine
Research: Audience Data Sourcing Analysis (3-phase lifecycle),
          Verified L3 Data Through Digital Ethnography
"""

from typing import Optional
from collections import Counter
from backend.core.audience_trigger_models import (
    AudienceTriggerProfile,
    CohortContextPremise,
    RegulatoryFocusProfile,
    RegulatoryOrientation,
    MoralEmotionProfile,
    CopingTrajectoryPosition,
    CopingPhase,
    HermeneuticalGapProfile,
    ReconsolidationMarkers,
    LDepth,
    DataPhase,
)

# ─── L-Depth Weights ────────────────────────────────────────────────
L_DEPTH_WEIGHTS = {
    LDepth.L1_PERFORMATIVE: 1.0,
    LDepth.L2_COMMUNAL: 1.5,
    LDepth.L3_AUTHENTIC: 3.0,
}

# ─── Data Phase Thresholds ───────────────────────────────────────────
COLD_THRESHOLD = 10
WARM_THRESHOLD = 50


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    """Compute weighted mean, handling empty/zero-weight cases."""
    total_weight = sum(weights)
    if total_weight == 0 or len(values) == 0:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def aggregate_profiles(
    profiles: list[AudienceTriggerProfile],
    segment_id: Optional[str] = None,
    segment_label: Optional[str] = None,
) -> CohortContextPremise:
    """
    Aggregates individual AudienceTriggerProfiles into a CohortContextPremise.

    Uses L-depth weighted averaging: L3 texts get 3x weight, L2 gets 1.5x,
    L1 gets 1x. This privileges raw, unpolished disclosures over performative
    content per the provenance chain methodology.

    Args:
        profiles: List of individual AudienceTriggerProfile objects.
        segment_id: Optional segment identifier.
        segment_label: Optional human-readable label.

    Returns:
        CohortContextPremise with aggregated scores.
    """
    n = len(profiles)
    if n == 0:
        return CohortContextPremise(
            segment_id=segment_id,
            segment_label=segment_label,
        )

    # Compute per-profile weights based on L-depth
    weights = [
        L_DEPTH_WEIGHTS.get(p.authenticity.l_depth, 1.0)
        for p in profiles
    ]

    # ── Regulatory Focus Aggregation ──
    eagerness_agg = _weighted_mean(
        [p.regulatory_focus.eagerness_score for p in profiles], weights
    )
    vigilance_agg = _weighted_mean(
        [p.regulatory_focus.vigilance_score for p in profiles], weights
    )
    delta = abs(eagerness_agg - vigilance_agg)
    if delta < 0.15:
        orientation = RegulatoryOrientation.DUAL_DOMINANT
    elif eagerness_agg > vigilance_agg:
        orientation = RegulatoryOrientation.PROMOTION
    else:
        orientation = RegulatoryOrientation.PREVENTION

    # ── Moral Emotion Aggregation ──
    foundation_keys = [
        "care_harm", "fairness_cheating", "loyalty_betrayal",
        "authority_subversion", "sanctity_degradation", "liberty_oppression",
    ]
    agg_foundations = {}
    for key in foundation_keys:
        values = [p.moral_emotion.foundation_weights.get(key, 0.0) for p in profiles]
        agg_foundations[key] = round(_weighted_mean(values, weights), 3)

    # Re-normalize to sum ≈ 1.0
    total = sum(agg_foundations.values())
    if total > 0:
        agg_foundations = {k: round(v / total, 3) for k, v in agg_foundations.items()}

    # Dominant emotion: mode across profiles
    emotions = [p.moral_emotion.dominant_emotion for p in profiles if p.moral_emotion.dominant_emotion]
    dominant_emotion = Counter(emotions).most_common(1)[0][0] if emotions else None

    # ── Coping Trajectory Aggregation ──
    temporal_shift_agg = _weighted_mean(
        [p.coping_trajectory.temporal_language_shift for p in profiles], weights
    )
    agency_delta_agg = _weighted_mean(
        [p.coping_trajectory.agency_attribution_delta for p in profiles], weights
    )
    search_conf_agg = _weighted_mean(
        [p.coping_trajectory.search_phase_confidence for p in profiles], weights
    )
    # Modal phase
    phases = [p.coping_trajectory.phase for p in profiles]
    modal_phase = Counter(phases).most_common(1)[0][0] if phases else CopingPhase.PRE_CONTEMPLATION

    # ── Hermeneutical Gap Aggregation ──
    trunc_agg = _weighted_mean(
        [p.hermeneutical_gap.discourse_truncation_score for p in profiles], weights
    )
    parab_agg = _weighted_mean(
        [p.hermeneutical_gap.affective_parabola_score for p in profiles], weights
    )
    novel_agg = _weighted_mean(
        [p.hermeneutical_gap.metaphor_novelty_score for p in profiles], weights
    )
    composite_agg = _weighted_mean(
        [p.hermeneutical_gap.composite_gap_score for p in profiles], weights
    )

    # ── Reconsolidation Aggregation ──
    pe_agg = _weighted_mean(
        [p.reconsolidation.prediction_error_sensitivity for p in profiles], weights
    )
    ss_agg = _weighted_mean(
        [p.reconsolidation.save_share_ratio for p in profiles], weights
    )
    coupling_agg = _weighted_mean(
        [p.reconsolidation.neural_coupling_proxy for p in profiles], weights
    )
    parasocial_agg = _weighted_mean(
        [p.reconsolidation.parasocial_engagement for p in profiles], weights
    )

    # ── Authenticity Meta ──
    auth_mean = _weighted_mean(
        [p.authenticity.liwc_authenticity_proxy for p in profiles],
        [1.0] * n,  # Unweighted for the meta score itself
    )
    depth_counts = Counter(p.authenticity.l_depth for p in profiles)
    l_depth_dist = {
        "L1_PERFORMATIVE": round(depth_counts.get(LDepth.L1_PERFORMATIVE, 0) / n, 3),
        "L2_COMMUNAL": round(depth_counts.get(LDepth.L2_COMMUNAL, 0) / n, 3),
        "L3_AUTHENTIC": round(depth_counts.get(LDepth.L3_AUTHENTIC, 0) / n, 3),
    }

    # ── Data Phase ──
    if n < COLD_THRESHOLD:
        data_phase = DataPhase.COLD
    elif n < WARM_THRESHOLD:
        data_phase = DataPhase.WARM
    else:
        data_phase = DataPhase.HOT

    return CohortContextPremise(
        segment_id=segment_id,
        segment_label=segment_label,
        sample_size=n,
        regulatory_focus=RegulatoryFocusProfile(
            eagerness_score=round(eagerness_agg, 3),
            vigilance_score=round(vigilance_agg, 3),
            dominant_orientation=orientation,
        ),
        moral_emotion=MoralEmotionProfile(
            foundation_weights=agg_foundations,
            dominant_emotion=dominant_emotion,
        ),
        coping_trajectory=CopingTrajectoryPosition(
            phase=modal_phase,
            temporal_language_shift=round(temporal_shift_agg, 3),
            agency_attribution_delta=round(agency_delta_agg, 3),
            search_phase_confidence=round(search_conf_agg, 3),
        ),
        hermeneutical_gap=HermeneuticalGapProfile(
            discourse_truncation_score=round(trunc_agg, 3),
            affective_parabola_score=round(parab_agg, 3),
            metaphor_novelty_score=round(novel_agg, 3),
            composite_gap_score=round(composite_agg, 3),
        ),
        reconsolidation=ReconsolidationMarkers(
            prediction_error_sensitivity=round(pe_agg, 3),
            save_share_ratio=round(ss_agg, 3),
            neural_coupling_proxy=round(coupling_agg, 3),
            parasocial_engagement=round(parasocial_agg, 3),
        ),
        data_phase=data_phase,
        mean_authenticity=round(auth_mean, 3),
        l_depth_distribution=l_depth_dist,
    )
