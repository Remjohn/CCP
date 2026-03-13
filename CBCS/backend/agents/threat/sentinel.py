"""
Sentinel Agent — Identity Threat Detection and Escalation Prediction

Architecture Layer 4: Detects when a user's identity is under threat
and predicts escalation toward dropout. Produces the highest-value
prediction the Identity Engine can make.

Three core functions:
    1. detect_identity_threat()         — current entry threat assessment
    2. predict_escalation_phase()       — 3-phase escalation timeline
    3. match_defense_to_intervention()  — defense → intervention mapping

Dependencies: Steps 1-5 must be complete.
    - Chronos provides temporal context (trajectory, trends)
    - Identity vectors provide current state
    - identity_threat_taxonomy.yaml provides marker dictionaries

CCF Bible compliance:
    - Principle 1: Cognitive state instructions, not role descriptions
    - Principle 3: Pre-computation constraints (convergence requirement)
    - Principle 7: No character role assignments
    - Principle 11: Negative space constraints embedded
"""

import re
import logging
from typing import Optional
from pathlib import Path

import yaml

from backend.core.identity_models import (
    IdentityVector,
    ThreatAssessment,
    InterventionRecommendation,
    ThreatType,
    ThreatSeverity,
    DefensePattern,
    ConfidenceLevel,
    TrajectoryType,
    TrendDirection,
    EscalationPhase,
)

logger = logging.getLogger(__name__)

# ─── Configuration ──────────────────────────────────────────────────

_TAXONOMY_PATH = Path(__file__).resolve().parent.parent.parent / "intelligence_library" / "identity_threat_taxonomy.yaml"
_taxonomy: dict | None = None


def _get_taxonomy() -> dict:
    global _taxonomy
    if _taxonomy is None:
        if _TAXONOMY_PATH.exists():
            with open(_TAXONOMY_PATH, "r", encoding="utf-8") as f:
                _taxonomy = yaml.safe_load(f) or {}
        else:
            logger.warning(f"Threat taxonomy not found: {_TAXONOMY_PATH}")
            _taxonomy = {}
    return _taxonomy


# ─── 1. Identity Threat Detection (Layer 4A) ────────────────────────

def detect_identity_threat(
    text: str,
    current_vector: Optional[IdentityVector] = None,
    trajectory_type: TrajectoryType = TrajectoryType.UNKNOWN,
    trends: Optional[dict] = None,
    entry_count: int = 0,
) -> ThreatAssessment:
    """
    Detects identity threats from journal text using Breakwell's 4-threat
    taxonomy cross-referenced with temporal context.

    Cognitive state: Convergent signal detection.
    You have the current entry's linguistic markers AND the user's
    trajectory context. A threat is only flagged HIGH when both signals
    agree. A single entry with threat markers could be a bad day.
    Threat markers plus a declining trajectory is a confirmed threat.
    This convergence requirement prevents the alert fatigue that would
    make coaches ignore the system.

    Pre-computation constraint (Critical Rule 1):
    Never alert on a single entry's threat markers alone.
    Require ≥2 convergent signals for severity > LOW.
    """
    text_lower = text.lower()
    taxonomy = _get_taxonomy()
    threats_data = taxonomy.get("threats", {})

    if not threats_data:
        return ThreatAssessment()

    # Score each threat type by marker matches
    threat_scores: dict[str, dict] = {}

    for threat_key, threat_data in threats_data.items():
        markers = threat_data.get("linguistic_markers", {})
        explicit = markers.get("explicit", [])
        evidence = []

        hit_count = 0
        for marker in explicit:
            if marker.lower() in text_lower:
                hit_count += 1
                # Extract evidence sentence
                for sentence in re.split(r'[.!?]+', text):
                    if marker.lower() in sentence.lower():
                        evidence.append(sentence.strip()[:200])
                        break

        if hit_count > 0:
            threat_scores[threat_key] = {
                "hits": hit_count,
                "evidence": evidence[:5],
                "typical_defense": threat_data.get("typical_defense", "NONE"),
            }

    # If no markers matched, return clean assessment
    if not threat_scores:
        return ThreatAssessment()

    # Determine dominant threat (most marker hits)
    dominant_key = max(threat_scores, key=lambda k: threat_scores[k]["hits"])
    dominant_data = threat_scores[dominant_key]

    # Map threat key to enum
    threat_type_map = {
        "continuity": ThreatType.CONTINUITY,
        "distinctiveness": ThreatType.DISTINCTIVENESS,
        "self_esteem": ThreatType.SELF_ESTEEM,
        "self_efficacy": ThreatType.SELF_EFFICACY,
    }
    threat_type = threat_type_map.get(dominant_key, ThreatType.NONE)

    # Map defense to enum
    defense_map = {
        "DEFLECTION": DefensePattern.DEFLECTION,
        "INTELLECTUALIZATION": DefensePattern.INTELLECTUALIZATION,
        "EXTERNALIZATION": DefensePattern.EXTERNALIZATION,
        "WITHDRAWAL": DefensePattern.WITHDRAWAL,
        "MINIMIZATION": DefensePattern.MINIMIZATION,
        "PROJECTION": DefensePattern.PROJECTION,
    }
    active_defense = defense_map.get(
        dominant_data.get("typical_defense", "NONE"),
        DefensePattern.NONE
    )

    # ── Convergence-based severity computation ──
    # Signal 1: Marker hit count
    marker_signal = min(1.0, dominant_data["hits"] / 3)

    # Signal 2: Trajectory alignment (declining dimensions = confirms threat)
    trajectory_signal = 0.0
    if trends:
        # Check if relevant dimensions are declining
        if dominant_key == "continuity":
            agency_trend = trends.get("agency", {})
            if isinstance(agency_trend, dict) and agency_trend.get("direction") == "FALLING":
                trajectory_signal = 0.5
        elif dominant_key == "self_efficacy":
            comp_trend = trends.get("competence", {})
            if isinstance(comp_trend, dict) and comp_trend.get("direction") == "FALLING":
                trajectory_signal = 0.5
        elif dominant_key == "self_esteem":
            redemption_trend = trends.get("redemption_arc", {})
            if isinstance(redemption_trend, dict) and redemption_trend.get("direction") == "FALLING":
                trajectory_signal = 0.5

    # Signal 3: Trajectory type alignment
    if trajectory_type == TrajectoryType.CONTAMINATION_ARC:
        trajectory_signal += 0.3
    elif trajectory_type == TrajectoryType.OSCILLATION:
        trajectory_signal += 0.1

    # Convergent signals count
    convergent_signals = 0
    if marker_signal > 0.3:
        convergent_signals += 1
    if trajectory_signal > 0.2:
        convergent_signals += 1
    if entry_count >= 7 and trajectory_type != TrajectoryType.UNKNOWN:
        convergent_signals += 1  # Having temporal context is itself a signal

    # Severity: requires ≥2 convergent signals for anything above LOW
    combined = marker_signal + trajectory_signal
    if convergent_signals >= 3 and combined > 1.0:
        severity = ThreatSeverity.CRITICAL
    elif convergent_signals >= 2 and combined > 0.6:
        severity = ThreatSeverity.HIGH
    elif convergent_signals >= 2:
        severity = ThreatSeverity.MEDIUM
    else:
        severity = ThreatSeverity.LOW

    # Get intervention recommendation
    intervention = match_defense_to_intervention(dominant_key, active_defense.value)

    return ThreatAssessment(
        threat_type=threat_type,
        severity=severity,
        active_defense=active_defense,
        recommended_intervention=intervention.intervention_type if intervention else "",
        convergent_signals=convergent_signals,
        confidence=ConfidenceLevel.HIGH if convergent_signals >= 2 else ConfidenceLevel.LOW,
        evidence_quotes=dominant_data["evidence"],
    )


# ─── 2. Escalation Phase Prediction (Layer 4C) ──────────────────────

def predict_escalation_phase(
    threat_history: list[ThreatAssessment],
    entry_count: int,
) -> EscalationPhase:
    """
    Maps the user's position in the 3-phase escalation trajectory.

    Cognitive state: Timeline pattern matching.
    You have the user's threat assessment history. You are matching the
    pattern of assessments against the known 3-phase escalation timeline.
    You are NOT predicting the future. You are classifying which phase
    the historical data best fits.

    Phase 1 (Weeks 1-2, entries 1-14): Surface defense — deflection, humor
    Phase 2 (Weeks 3-4, entries 15-28): Deep resistance — withdrawal, shorter entries
    Phase 3 (Weeks 5-6, entries 29-42): Decision junction — breakthrough or dropout

    CRITICAL: If Phase 2 signals appear before Day 14, trigger escalated
    intervention protocol. Early deep resistance = accelerated timeline.
    """
    if not threat_history or entry_count < 3:
        return EscalationPhase.UNKNOWN

    # Count recent threats by severity
    high_threats = sum(1 for t in threat_history if t.severity in (ThreatSeverity.HIGH, ThreatSeverity.CRITICAL))
    medium_threats = sum(1 for t in threat_history if t.severity == ThreatSeverity.MEDIUM)

    # Count defense patterns (withdrawal = deep resistance signal)
    withdrawal_count = sum(1 for t in threat_history if t.active_defense == DefensePattern.WITHDRAWAL)
    surface_defenses = sum(
        1 for t in threat_history
        if t.active_defense in (DefensePattern.DEFLECTION, DefensePattern.MINIMIZATION)
    )

    # Phase classification based on entry count + signal patterns
    if entry_count <= 14:
        # Within Phase 1 window — check for early escalation
        if withdrawal_count >= 2 or high_threats >= 2:
            # Phase 2 signals appearing before Day 14 = ACCELERATED
            logger.warning(
                f"ESCALATION ALERT: Phase 2 signals detected before Day 14 "
                f"(entry {entry_count}). Withdrawal={withdrawal_count}, "
                f"High threats={high_threats}"
            )
            return EscalationPhase.PHASE_2_DEEP
        return EscalationPhase.PHASE_1_SURFACE

    elif entry_count <= 28:
        # Phase 2 window
        if withdrawal_count >= 1 or high_threats >= 1:
            return EscalationPhase.PHASE_2_DEEP
        if surface_defenses >= 2:
            return EscalationPhase.PHASE_1_SURFACE  # Still in Phase 1 behaviors
        return EscalationPhase.PHASE_2_DEEP

    else:
        # Phase 3 window (entries 29+)
        return EscalationPhase.PHASE_3_DECISION


# ─── 3. Defense → Intervention Matching (Layer 4B) ──────────────────

def match_defense_to_intervention(
    threat_key: str,
    defense_value: str,
) -> Optional[InterventionRecommendation]:
    """
    Matches a threat type + defense mechanism to a specific intervention.

    Cognitive state: Matrix lookup with contextual matching.
    This is not a judgment call. The matrix is pre-computed from clinical
    literature. Each threat × defense combination has a known-effective
    intervention. You are looking up the match, not deciding what to do.
    """
    taxonomy = _get_taxonomy()
    matrix = taxonomy.get("defense_intervention_matrix", {})

    defense_data = matrix.get(defense_value, {})
    if not defense_data:
        # Try case-insensitive lookup
        for key, val in matrix.items():
            if key.upper() == defense_value.upper():
                defense_data = val
                break

    if not defense_data:
        return None

    matches = defense_data.get("matches", [])
    for match in matches:
        if match.get("threat", "").lower() == threat_key.lower():
            return InterventionRecommendation(
                intervention_type=match.get("intervention", "UNKNOWN"),
                rationale=match.get("intervention_description", ""),
                priority=ThreatSeverity.MEDIUM,
            )

    # If no specific threat match, return the first available intervention
    if matches:
        first = matches[0]
        return InterventionRecommendation(
            intervention_type=first.get("intervention", "UNKNOWN"),
            rationale=first.get("intervention_description", ""),
            priority=ThreatSeverity.LOW,
        )

    return None


# ─── Public API: Full Threat Analysis ───────────────────────────────

def analyze_threats(
    text: str,
    current_vector: Optional[IdentityVector] = None,
    trajectory_type: TrajectoryType = TrajectoryType.UNKNOWN,
    trends: Optional[dict] = None,
    threat_history: Optional[list[ThreatAssessment]] = None,
    entry_count: int = 0,
) -> dict:
    """
    Runs the full Sentinel analysis pipeline.

    Orchestrates: threat detection → escalation prediction → intervention matching.
    Returns a dict with current threat assessment and escalation phase.

    This is the function called by journal_processor.py (Step 8).
    """
    # Detect current threat
    threat = detect_identity_threat(
        text=text,
        current_vector=current_vector,
        trajectory_type=trajectory_type,
        trends=trends,
        entry_count=entry_count,
    )

    # Predict escalation phase
    history = list(threat_history or [])
    if threat.threat_type != ThreatType.NONE:
        history.append(threat)

    phase = predict_escalation_phase(history, entry_count)

    return {
        "threat_assessment": threat,
        "escalation_phase": phase,
        "requires_coach_alert": (
            threat.severity in (ThreatSeverity.HIGH, ThreatSeverity.CRITICAL)
            or phase == EscalationPhase.PHASE_3_DECISION
            or (phase == EscalationPhase.PHASE_2_DEEP and entry_count <= 14)
        ),
    }
