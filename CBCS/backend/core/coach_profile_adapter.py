"""
Coach Profile Adapter — Coach-Side Vector Generation

Adapts coach-side data (trigger_map.json + emotional_dna.json) into a
CoachMatchVector that is directly comparable with the audience-side
CohortContextPremise for cosine similarity computation.

Three transformations:
    1. MFT Vector: Aggregate moral_foundation fields across all triggers
       into a weighted {foundation: float} vector.
    2. Content Readiness Gate: Only resolved_dual_layer triggers are eligible
       for content activation (per reconsolidation safety protocol).
    3. Regulatory Orientation: Extract from emotional DNA patterns.

Architecture: Coach Data → Adapter → Intersection Engine
Research: Haidt MFQ-2, Tedeschi & Calhoun PTG (2004)
"""

import json
from typing import Optional
from backend.core.audience_trigger_models import (
    CoachMatchVector,
    RegulatoryOrientation,
)

# ─── Foundation options from trigger_map schema ──────────────────────
FOUNDATION_OPTIONS = [
    "care_harm",
    "fairness_cheating",
    "loyalty_betrayal",
    "authority_subversion",
    "sanctity_degradation",
    "liberty_oppression",
]


def adapt_coach_profile(
    trigger_map: dict,
    emotional_dna: Optional[dict] = None,
) -> CoachMatchVector:
    """
    Converts coach trigger_map.json data into a CoachMatchVector
    for comparison with audience CohortContextPremise.

    Args:
        trigger_map: Parsed trigger_map.json content.
        emotional_dna: Parsed emotional_dna.json content (optional).

    Returns:
        CoachMatchVector with MFT weights, orientation, and eligible triggers.
    """
    coach_id = trigger_map.get("coach_id")
    triggers = trigger_map.get("triggers", [])

    # Filter out template entries
    active_triggers = [t for t in triggers if not t.get("_template", False)]

    # ── Step 1: Aggregate MFT Vector ──
    foundation_counts = {f: 0.0 for f in FOUNDATION_OPTIONS}

    for trigger in active_triggers:
        mf = trigger.get("moral_foundation", {})
        primary = mf.get("primary")
        secondary = mf.get("secondary")

        if primary and primary in foundation_counts:
            foundation_counts[primary] += 1.0
        if secondary and secondary in foundation_counts:
            foundation_counts[secondary] += 0.5  # Secondary gets half weight

    # Normalize to sum ≈ 1.0
    total = sum(foundation_counts.values())
    if total > 0:
        mft_weights = {k: round(v / total, 3) for k, v in foundation_counts.items()}
    else:
        mft_weights = {k: 0.0 for k in foundation_counts}

    # ── Step 2: Content Readiness Gate ──
    eligible_ids = []
    prediction_thresholds = []

    for trigger in active_triggers:
        ptg = trigger.get("ptg_status", {})
        ptg_status = ptg.get("status")

        if ptg_status == "resolved_dual_layer":
            trigger_id = trigger.get("trigger_id")
            if trigger_id:
                eligible_ids.append(trigger_id)

            # Collect reconsolidation thresholds
            recon = trigger.get("reconsolidation_sensitivity", {})
            threshold = recon.get("prediction_error_threshold")
            if threshold is not None:
                try:
                    prediction_thresholds.append(float(threshold))
                except (ValueError, TypeError):
                    pass

    mean_threshold = (
        sum(prediction_thresholds) / len(prediction_thresholds)
        if prediction_thresholds
        else 5.0  # Default mid-range
    )

    # ── Step 3: Regulatory Orientation from Emotional DNA ──
    orientation = RegulatoryOrientation.DUAL_DOMINANT

    if emotional_dna:
        # Heuristic: scan emotional patterns for promotion vs. prevention signals
        dna_str = json.dumps(emotional_dna).lower()

        promotion_signals = sum(1 for word in [
            "growth", "aspiration", "ideal", "dream", "build",
            "create", "transform", "advance", "opportunity",
        ] if word in dna_str)

        prevention_signals = sum(1 for word in [
            "protect", "safety", "duty", "obligation", "guard",
            "secure", "maintain", "preserve", "avoid",
        ] if word in dna_str)

        delta = abs(promotion_signals - prevention_signals)
        if delta >= 2:
            if promotion_signals > prevention_signals:
                orientation = RegulatoryOrientation.PROMOTION
            else:
                orientation = RegulatoryOrientation.PREVENTION

    return CoachMatchVector(
        coach_id=coach_id,
        mft_weights=mft_weights,
        regulatory_orientation=orientation,
        eligible_trigger_ids=eligible_ids,
        mean_prediction_error_threshold=round(mean_threshold, 1),
    )
