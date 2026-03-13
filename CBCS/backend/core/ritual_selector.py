"""
Ritual Selector — Architecture Layer 5

Multi-factor scoring algorithm that selects the optimal ritual
for each user based on the full Identity Engine output.

Replaces the old identity_pillar-based selection with a weighted
multi-factor formula:

    RitualScore(r) = Σ (wᵢ · factorᵢ)

    Factors:
    1. SDT Need Match (w=0.30)     — ritual targets the most frustrated need
    2. Threat Mitigation (w=0.25)  — ritual's intervention matches active threat
    3. Trajectory Alignment (w=0.20) — ritual supports current arc direction
    4. Discrepancy Reduction (w=0.15) — ritual addresses dominant self-gap
    5. Distortion Counter (w=0.10)  — ritual includes cognitive reframe

This selector is consumed by Atlas (schedule generator) to produce
the daily ritual assignment.
"""

import logging
from typing import Optional

from backend.core.identity_models import (
    IdentityVector,
    TemporalAnalysis,
    ThreatAssessment,
    ThreatType,
    ThreatSeverity,
    DominantNeed,
    DominantGapType,
    TrajectoryType,
    TrendDirection,
    DefensePattern,
)

logger = logging.getLogger(__name__)

# ─── Ritual Registry ────────────────────────────────────────────────
# Each ritual has metadata describing which identity dimensions it targets.
# In production, this comes from Supabase. For now, hardcoded reference set.

RITUAL_REGISTRY = {
    "morning_reflection": {
        "name": "Morning Reflection",
        "targets_need": "AUTONOMY",
        "targets_gap": "IDEAL",
        "targets_threat": None,
        "intervention_type": None,
        "supports_trajectory": ["REDEMPTION_ARC", "PLATEAU"],
        "counters_distortion": ["SHOULD_STATEMENTS", "ALL_OR_NOTHING"],
        "intensity": "LOW",
    },
    "gratitude_journal": {
        "name": "Gratitude Journal",
        "targets_need": "RELATEDNESS",
        "targets_gap": "IDEAL",
        "targets_threat": "SELF_ESTEEM",
        "intervention_type": "SELF_AFFIRMATION",
        "supports_trajectory": ["REDEMPTION_ARC", "PLATEAU"],
        "counters_distortion": ["MENTAL_FILTER", "DISQUALIFYING_POSITIVE"],
        "intensity": "LOW",
    },
    "micro_mastery": {
        "name": "Micro Mastery Challenge",
        "targets_need": "COMPETENCE",
        "targets_gap": "IDEAL",
        "targets_threat": "SELF_EFFICACY",
        "intervention_type": "MICRO_MASTERY",
        "supports_trajectory": ["CONTAMINATION_ARC", "PLATEAU"],
        "counters_distortion": ["OVERGENERALIZATION", "JUMPING_TO_CONCLUSIONS"],
        "intensity": "MEDIUM",
    },
    "warrior_ritual": {
        "name": "Warrior Activation",
        "targets_need": "AUTONOMY",
        "targets_gap": "OUGHT",
        "targets_threat": "SELF_EFFICACY",
        "intervention_type": "SOMATIC_GROUNDING",
        "supports_trajectory": ["CONTAMINATION_ARC", "OSCILLATION"],
        "counters_distortion": ["EMOTIONAL_REASONING", "MAGNIFICATION"],
        "intensity": "HIGH",
    },
    "connection_call": {
        "name": "Connection Call",
        "targets_need": "RELATEDNESS",
        "targets_gap": "OUGHT",
        "targets_threat": "DISTINCTIVENESS",
        "intervention_type": "RADICAL_INDIVIDUALIZATION",
        "supports_trajectory": ["PLATEAU", "OSCILLATION"],
        "counters_distortion": ["PERSONALIZATION", "JUMPING_TO_CONCLUSIONS"],
        "intensity": "MEDIUM",
    },
    "identity_letter": {
        "name": "Letter to Future Self",
        "targets_need": "AUTONOMY",
        "targets_gap": "IDEAL",
        "targets_threat": "CONTINUITY",
        "intervention_type": "NARRATIVE_REMOORING",
        "supports_trajectory": ["CONTAMINATION_ARC", "OSCILLATION"],
        "counters_distortion": ["LABELLING", "OVERGENERALIZATION"],
        "intensity": "MEDIUM",
    },
    "fear_facing": {
        "name": "Fear Facing Exercise",
        "targets_need": "COMPETENCE",
        "targets_gap": "FEARED",
        "targets_threat": "SELF_EFFICACY",
        "intervention_type": "SOMATIC_GROUNDING",
        "supports_trajectory": ["REDEMPTION_ARC"],
        "counters_distortion": ["MAGNIFICATION", "EMOTIONAL_REASONING"],
        "intensity": "HIGH",
    },
    "temporal_bridge": {
        "name": "Temporal Bridging",
        "targets_need": "AUTONOMY",
        "targets_gap": "IDEAL",
        "targets_threat": "CONTINUITY",
        "intervention_type": "TEMPORAL_BRIDGING",
        "supports_trajectory": ["CONTAMINATION_ARC", "OSCILLATION"],
        "counters_distortion": ["ALL_OR_NOTHING", "LABELLING"],
        "intensity": "MEDIUM",
    },
}


# ─── Scoring Weights ────────────────────────────────────────────────

WEIGHTS = {
    "sdt_need_match": 0.30,
    "threat_mitigation": 0.25,
    "trajectory_alignment": 0.20,
    "discrepancy_reduction": 0.15,
    "distortion_counter": 0.10,
}


# ─── Multi-Factor Scoring ───────────────────────────────────────────

def score_ritual(
    ritual_id: str,
    ritual_meta: dict,
    identity_vector: IdentityVector,
    temporal_analysis: Optional[TemporalAnalysis] = None,
    threat_assessment: Optional[ThreatAssessment] = None,
) -> float:
    """
    Computes a weighted composite score for a single ritual.

    Each factor is scored 0.0 to 1.0, then multiplied by its weight.
    The final score is the sum of all weighted factors.
    """
    scores = {}

    # ── Factor 1: SDT Need Match (w=0.30) ──
    # Does this ritual target the user's most frustrated need?
    dominant_need = identity_vector.sdt.dominant_need.value
    ritual_targets = ritual_meta.get("targets_need", "")
    if ritual_targets == dominant_need:
        scores["sdt_need_match"] = 1.0
    elif _needs_adjacent(ritual_targets, dominant_need):
        scores["sdt_need_match"] = 0.5
    else:
        scores["sdt_need_match"] = 0.1

    # ── Factor 2: Threat Mitigation (w=0.25) ──
    # Does this ritual's intervention match the active threat?
    if threat_assessment and threat_assessment.threat_type != ThreatType.NONE:
        ritual_intervention = ritual_meta.get("intervention_type")
        recommended = threat_assessment.recommended_intervention
        if ritual_intervention and ritual_intervention == recommended:
            scores["threat_mitigation"] = 1.0
        elif ritual_meta.get("targets_threat") == threat_assessment.threat_type.value:
            scores["threat_mitigation"] = 0.7
        else:
            scores["threat_mitigation"] = 0.1
    else:
        scores["threat_mitigation"] = 0.3  # No active threat = neutral

    # ── Factor 3: Trajectory Alignment (w=0.20) ──
    # Does this ritual support the user's current trajectory direction?
    if temporal_analysis and temporal_analysis.sufficient_data_for_trajectory:
        trajectory = temporal_analysis.trajectory.value
        supported = ritual_meta.get("supports_trajectory", [])
        if trajectory in supported:
            scores["trajectory_alignment"] = 1.0
        elif trajectory == "UNKNOWN":
            scores["trajectory_alignment"] = 0.5
        else:
            scores["trajectory_alignment"] = 0.2
    else:
        scores["trajectory_alignment"] = 0.5  # Insufficient data = neutral

    # ── Factor 4: Discrepancy Reduction (w=0.15) ──
    # Does this ritual address the dominant self-discrepancy gap?
    dominant_gap = identity_vector.discrepancy.dominant_gap_type.value
    ritual_gap = ritual_meta.get("targets_gap", "")
    if ritual_gap == dominant_gap:
        scores["discrepancy_reduction"] = 1.0
    else:
        scores["discrepancy_reduction"] = 0.3

    # ── Factor 5: Distortion Counter (w=0.10) ──
    # Does this ritual include a cognitive reframe for detected distortions?
    if identity_vector.distortions.dominant_distortion:
        dominant_distortion = identity_vector.distortions.dominant_distortion.value
        counters = ritual_meta.get("counters_distortion", [])
        if dominant_distortion in counters:
            scores["distortion_counter"] = 1.0
        else:
            scores["distortion_counter"] = 0.2
    else:
        scores["distortion_counter"] = 0.5  # No distortions = neutral

    # ── Compute Weighted Sum ──
    total = sum(
        scores.get(factor, 0) * weight
        for factor, weight in WEIGHTS.items()
    )

    return round(total, 4)


def _needs_adjacent(need_a: str, need_b: str) -> bool:
    """
    Returns True if two needs are 'adjacent' — meaning targeting one
    often indirectly supports the other (SDT literature).
    """
    adjacency = {
        ("AUTONOMY", "COMPETENCE"): True,
        ("COMPETENCE", "AUTONOMY"): True,
        ("RELATEDNESS", "AUTONOMY"): False,
        ("AUTONOMY", "RELATEDNESS"): False,
        ("COMPETENCE", "RELATEDNESS"): True,
        ("RELATEDNESS", "COMPETENCE"): True,
    }
    return adjacency.get((need_a, need_b), False)


# ─── Public API: Select Best Ritual ─────────────────────────────────

def select_ritual(
    identity_vector: IdentityVector,
    temporal_analysis: Optional[TemporalAnalysis] = None,
    threat_assessment: Optional[ThreatAssessment] = None,
    excluded_rituals: Optional[list[str]] = None,
    intensity_cap: Optional[str] = None,
) -> dict:
    """
    Scores all available rituals and returns the best match.

    Args:
        identity_vector: Current 12-dimensional identity vector
        temporal_analysis: Chronos output (if available)
        threat_assessment: Sentinel output (if available)
        excluded_rituals: IDs to exclude (recently assigned)
        intensity_cap: "LOW", "MEDIUM", or "HIGH" max intensity

    Returns:
        Dict with: ritual_id, ritual_name, score, factor_scores, reasoning
    """
    excluded = set(excluded_rituals or [])
    intensity_order = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    max_intensity = intensity_order.get(intensity_cap, 3)

    scored_rituals = []
    for ritual_id, ritual_meta in RITUAL_REGISTRY.items():
        if ritual_id in excluded:
            continue

        ritual_intensity = intensity_order.get(ritual_meta.get("intensity", "LOW"), 1)
        if ritual_intensity > max_intensity:
            continue

        score = score_ritual(
            ritual_id, ritual_meta, identity_vector,
            temporal_analysis, threat_assessment
        )
        scored_rituals.append({
            "ritual_id": ritual_id,
            "ritual_name": ritual_meta["name"],
            "score": score,
            "intensity": ritual_meta.get("intensity", "LOW"),
        })

    # Sort by score descending
    scored_rituals.sort(key=lambda r: r["score"], reverse=True)

    if not scored_rituals:
        return {
            "ritual_id": "morning_reflection",
            "ritual_name": "Morning Reflection",
            "score": 0.0,
            "reasoning": "No rituals available — returning default",
        }

    best = scored_rituals[0]
    logger.info(
        f"Ritual selected: {best['ritual_name']} "
        f"(score={best['score']}, intensity={best['intensity']})"
    )

    return {
        "ritual_id": best["ritual_id"],
        "ritual_name": best["ritual_name"],
        "score": best["score"],
        "intensity": best["intensity"],
        "reasoning": _build_reasoning(best, identity_vector, threat_assessment),
        "alternatives": scored_rituals[1:3],  # Top 2 alternatives
    }


def _build_reasoning(
    selected: dict,
    identity_vector: IdentityVector,
    threat: Optional[ThreatAssessment],
) -> str:
    """Builds a human-readable reasoning string for the coach dashboard."""
    parts = [f"Selected '{selected['ritual_name']}' (score: {selected['score']})."]
    parts.append(f"Dominant need: {identity_vector.sdt.dominant_need.value}.")
    parts.append(f"Dominant gap: {identity_vector.discrepancy.dominant_gap_type.value}.")

    if identity_vector.distortions.dominant_distortion:
        parts.append(f"Active distortion: {identity_vector.distortions.dominant_distortion.value}.")

    if threat and threat.threat_type != ThreatType.NONE:
        parts.append(f"Active threat: {threat.threat_type.value} ({threat.severity.value}).")

    return " ".join(parts)
