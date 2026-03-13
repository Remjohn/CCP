"""
Blueprint Orchestrator — Proposal 6 Hybrid (Core + Satellite)

The master content orchestrator that consumes intersection results and
generates a dual-track content blueprint.

Dual-Track Architecture:
    CORE Track (default 60%): Intersection-First Adaptive
        - Takes top-N intersection themes from IntersectionResult
        - Combines coach's resolved trigger narrative with audience's
          moral foundation violation
        - Applies Scherer CPM emotional framing

    SATELLITE Track (default 40%): Audience-First Sequential
        - Covers audience signals that don't intersect with coach triggers
        - Generates awareness-level content validating unarticulated experience
        - Prevents "echo chamber" effect

    Progressive Enrichment (by data phase):
        COLD (Mode C):  Core 40% / Satellite 60% (broad, surface-level)
        WARM (Mode B):  Core 60% / Satellite 40% (balanced)
        HOT  (Mode A):  Core 70% / Satellite 30% (deep intersection)

Architecture: Intersection Engine → Blueprint Orchestrator → Content Pipeline
Research: MCDA Blueprint Orchestrator (Proposal 6),
          Structural Congruence Theory, Authentic Activation,
          Neural Coupling, Content Diversity Research
"""

import uuid
from backend.core.audience_trigger_models import (
    IntersectionResult,
    CohortContextPremise,
    CoachMatchVector,
    ContentBlueprint,
    BlueprintItem,
    BlueprintTrack,
    DataPhase,
    ConfidenceLevel,
)

# ─── Progressive Enrichment Ratios ───────────────────────────────────
PHASE_RATIOS = {
    DataPhase.COLD: {"core": 0.40, "satellite": 0.60},
    DataPhase.WARM: {"core": 0.60, "satellite": 0.40},
    DataPhase.HOT:  {"core": 0.70, "satellite": 0.30},
}

# ─── Foundation → Emotional Frame Mapping ────────────────────────────
FOUNDATION_FRAMES = {
    "care_harm": "compassion_frame",
    "fairness_cheating": "indignation_frame",
    "loyalty_betrayal": "loyalty_frame",
    "authority_subversion": "authority_frame",
    "sanctity_degradation": "purity_frame",
    "liberty_oppression": "liberation_frame",
}

# ─── Foundation → Narrative Arc Mapping ──────────────────────────────
FOUNDATION_ARCS = {
    "care_harm": "protection_narrative",
    "fairness_cheating": "whistleblower_narrative",
    "loyalty_betrayal": "betrayal_to_redemption",
    "authority_subversion": "maverick_narrative",
    "sanctity_degradation": "purification_narrative",
    "liberty_oppression": "liberation_narrative",
}

# ─── Satellite Theme Templates ──────────────────────────────────────
# For audience signals that don't intersect with coach triggers
SATELLITE_THEMES = {
    "hermeneutical_gap": {
        "label": "Naming the Unnamed",
        "frame": "validation_frame",
        "arc": "discovery_narrative",
        "description": "Content that provides new interpretive frameworks for experiences the audience cannot yet articulate",
    },
    "reconsolidation_high": {
        "label": "Schema Challenge",
        "frame": "surprise_frame",
        "arc": "paradigm_shift_narrative",
        "description": "Content that deliberately violates audience expectations to trigger reconsolidation",
    },
    "search_phase": {
        "label": "The First Step",
        "frame": "guidance_frame",
        "arc": "journey_beginning_narrative",
        "description": "Content calibrated for people in the search phase — maximum receptivity",
    },
    "prevention_care": {
        "label": "Safe Harbor",
        "frame": "reassurance_frame",
        "arc": "stability_narrative",
        "description": "Content for prevention-focused audiences who need safety signals before action",
    },
}


def _determine_confidence(data_phase: DataPhase, intersection_score: float) -> ConfidenceLevel:
    """Determines confidence level based on data phase and score strength."""
    if data_phase == DataPhase.HOT and intersection_score > 0.6:
        return ConfidenceLevel.HIGH
    elif data_phase == DataPhase.WARM or intersection_score > 0.4:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.LOW


def _generate_satellite_items(
    audience: CohortContextPremise,
    intersection: IntersectionResult,
    target_count: int,
) -> list[BlueprintItem]:
    """
    Generates satellite items from audience-only signals.

    These cover dimensions where the audience has strong signals
    but no corresponding coach trigger was found.
    """
    items = []
    item_count = 0

    # Satellite 1: Hermeneutical Gap (if high composite score)
    if audience.hermeneutical_gap.composite_gap_score > 0.3 and item_count < target_count:
        theme = SATELLITE_THEMES["hermeneutical_gap"]
        items.append(BlueprintItem(
            item_id=f"sat_{uuid.uuid4().hex[:8]}",
            track=BlueprintTrack.SATELLITE,
            theme_label=theme["label"],
            emotional_frame=theme["frame"],
            narrative_arc_type=theme["arc"],
            content_depth="AWARENESS" if audience.data_phase == DataPhase.COLD else "MEDIUM",
            intersection_score=round(audience.hermeneutical_gap.composite_gap_score * 0.7, 3),
            data_confidence=_determine_confidence(audience.data_phase, 0.3),
        ))
        item_count += 1

    # Satellite 2: High Reconsolidation Sensitivity (without coach match)
    if audience.reconsolidation.prediction_error_sensitivity > 0.4 and item_count < target_count:
        theme = SATELLITE_THEMES["reconsolidation_high"]
        items.append(BlueprintItem(
            item_id=f"sat_{uuid.uuid4().hex[:8]}",
            track=BlueprintTrack.SATELLITE,
            theme_label=theme["label"],
            emotional_frame=theme["frame"],
            narrative_arc_type=theme["arc"],
            content_depth="MEDIUM",
            intersection_score=round(audience.reconsolidation.prediction_error_sensitivity * 0.6, 3),
            data_confidence=_determine_confidence(audience.data_phase, 0.4),
        ))
        item_count += 1

    # Satellite 3: Search Phase Content (peak receptivity)
    from backend.core.audience_trigger_models import CopingPhase
    if audience.coping_trajectory.phase == CopingPhase.SEARCH_PHASE and item_count < target_count:
        theme = SATELLITE_THEMES["search_phase"]
        items.append(BlueprintItem(
            item_id=f"sat_{uuid.uuid4().hex[:8]}",
            track=BlueprintTrack.SATELLITE,
            theme_label=theme["label"],
            emotional_frame=theme["frame"],
            narrative_arc_type=theme["arc"],
            content_depth="FULL_DEPTH",
            intersection_score=round(audience.coping_trajectory.search_phase_confidence * 0.8, 3),
            data_confidence=ConfidenceLevel.MEDIUM,
        ))
        item_count += 1

    # Satellite 4: Prevention orientation care content
    from backend.core.audience_trigger_models import RegulatoryOrientation
    if audience.regulatory_focus.dominant_orientation == RegulatoryOrientation.PREVENTION and item_count < target_count:
        theme = SATELLITE_THEMES["prevention_care"]
        items.append(BlueprintItem(
            item_id=f"sat_{uuid.uuid4().hex[:8]}",
            track=BlueprintTrack.SATELLITE,
            theme_label=theme["label"],
            emotional_frame=theme["frame"],
            narrative_arc_type=theme["arc"],
            content_depth="AWARENESS",
            intersection_score=round(audience.regulatory_focus.vigilance_score * 0.5, 3),
            data_confidence=_determine_confidence(audience.data_phase, 0.3),
        ))
        item_count += 1

    return items


def generate_blueprint(
    intersection: IntersectionResult,
    audience: CohortContextPremise,
    coach: CoachMatchVector,
    max_items: int = 10,
) -> ContentBlueprint:
    """
    Generates a dual-track content blueprint from intersection results.

    Core Track: Intersection-first content (coach trigger × audience foundation)
    Satellite Track: Audience-first content (signals without coach match)

    Ratios adapt to data phase:
        COLD: 40% core / 60% satellite
        WARM: 60% core / 40% satellite
        HOT:  70% core / 30% satellite

    Args:
        intersection: IntersectionResult from compute_intersection().
        audience: CohortContextPremise from aggregate_profiles().
        coach: CoachMatchVector from adapt_coach_profile().
        max_items: Maximum total blueprint items.

    Returns:
        ContentBlueprint with ordered, tagged items.
    """
    data_phase = intersection.audience_data_phase
    ratios = PHASE_RATIOS.get(data_phase, PHASE_RATIOS[DataPhase.WARM])

    core_count = max(1, int(max_items * ratios["core"]))
    satellite_count = max(1, max_items - core_count)

    # ── Core Track: Intersection Themes ──
    core_items = []
    for i, theme in enumerate(intersection.themes[:core_count]):
        # Find the dominant foundation for this theme
        foundation_key = None
        for fk, label in {
            "care_harm": "Protection & Nurturing",
            "fairness_cheating": "Justice & Equity",
            "loyalty_betrayal": "Loyalty & Trust",
            "authority_subversion": "Leadership & Order",
            "sanctity_degradation": "Purity & Standards",
            "liberty_oppression": "Freedom & Autonomy",
        }.items():
            if label == theme.theme_label:
                foundation_key = fk
                break

        emotional_frame = FOUNDATION_FRAMES.get(foundation_key, "neutral_frame")
        narrative_arc = FOUNDATION_ARCS.get(foundation_key, "general_narrative")

        core_items.append(BlueprintItem(
            item_id=f"core_{uuid.uuid4().hex[:8]}",
            track=BlueprintTrack.CORE,
            theme_label=theme.theme_label,
            coach_trigger_id=theme.coach_trigger_id,
            audience_foundation=foundation_key,
            emotional_frame=emotional_frame,
            content_depth=theme.recommended_depth,
            narrative_arc_type=narrative_arc,
            intersection_score=theme.intersection_score,
            data_confidence=_determine_confidence(data_phase, theme.intersection_score),
        ))

    # ── Satellite Track: Audience-Only Signals ──
    satellite_items = _generate_satellite_items(audience, intersection, satellite_count)

    # ── Combine and build blueprint ──
    all_items = core_items + satellite_items

    # Final sort: core items first (by score), then satellite items (by score)
    core_sorted = sorted(
        [i for i in all_items if i.track == BlueprintTrack.CORE],
        key=lambda x: x.intersection_score, reverse=True,
    )
    satellite_sorted = sorted(
        [i for i in all_items if i.track == BlueprintTrack.SATELLITE],
        key=lambda x: x.intersection_score, reverse=True,
    )

    final_items = core_sorted + satellite_sorted

    return ContentBlueprint(
        blueprint_id=str(uuid.uuid4()),
        coach_id=coach.coach_id,
        segment_id=audience.segment_id,
        items=final_items,
        core_ratio=ratios["core"],
        satellite_ratio=ratios["satellite"],
        data_phase=data_phase,
    )
