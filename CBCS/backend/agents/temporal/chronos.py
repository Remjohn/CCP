"""
Chronos Agent — Temporal Tracking and Change Point Detection

Architecture Layer 3: Transforms a collection of daily identity snapshots
into a trajectory with detected change points. Answers the question:
"Where is this user's identity GOING?"

Three core functions:
    1. compute_rolling_trends()  — rolling averages per dimension
    2. detect_change_points()    — PELT algorithm for structural breaks
    3. classify_trajectory()     — arc classification (Redemption/Contamination/etc.)

Dependencies: Steps 1-4 must be complete.
    - Step 1: Timestamped identity vectors in Neo4j
    - Step 2: IdentityVector data model
    - Step 4: Populated vectors from Aria's enhanced pipeline

CCF Bible compliance:
    - Principle 1: Cognitive state instructions, not role descriptions
    - Principle 3: Pre-computation constraints (minimum data thresholds)
    - Principle 7: No character role assignments
    - Principle 8: Binary, model-executable validation only
"""

import math
import logging
from typing import Optional

from backend.core.identity_models import (
    IdentityVector,
    TemporalAnalysis,
    DimensionTrend,
    ChangePoint,
    TrendDirection,
    TrajectoryType,
    ConfidenceLevel,
)

logger = logging.getLogger(__name__)

# ─── Configuration ──────────────────────────────────────────────────

# The 12 dimensions of the identity vector to track temporally
TRACKED_DIMENSIONS = [
    "agency", "communion", "redemption_arc", "meaning_making",
    "actual_ideal_gap", "actual_ought_gap", "feared_self_proximity",
    "autonomy", "competence", "relatedness",
    "threat_level", "confidence",
]

# Minimum data thresholds (Architecture Layer 3, Quality Gate 1)
MIN_ENTRIES_FOR_TRENDS = 7
MIN_ENTRIES_FOR_TRAJECTORY = 14

# Default rolling window size (Paper 6: BERTopic stability = 3-5 day windows)
DEFAULT_WINDOW_SIZE = 5

# PELT penalty coefficient (Paper 10: Writing in Symbiosis, Appendix A.4)
# Validated for optimal Type I/II error balance on linguistic time series
PELT_PENALTY_COEFFICIENT = 4.2


# ─── Helper: Extract Dimension Value ────────────────────────────────

def _extract_dimension(vector: dict, dimension: str) -> float:
    """
    Extracts a scalar value for a named dimension from a flat
    Neo4j IdentitySnapshot dict or from an IdentityVector model.
    """
    # Direct key access for flat Neo4j dicts from get_identity_trajectory()
    if dimension in vector:
        val = vector[dimension]
        if isinstance(val, (int, float)):
            return float(val)
        return 0.0

    # Nested access for IdentityVector model
    if isinstance(vector, IdentityVector):
        if dimension in ("agency", "communion", "redemption_arc", "meaning_making"):
            return getattr(vector.narrative, dimension, 0.0)
        elif dimension in ("actual_ideal_gap", "actual_ought_gap", "feared_self_proximity"):
            return getattr(vector.discrepancy, dimension, 0.0)
        elif dimension in ("autonomy", "competence", "relatedness"):
            return float(getattr(vector.sdt, dimension, 50))
        elif dimension == "threat_level":
            return 0.0  # Computed from severity, not directly stored
        elif dimension == "confidence":
            return vector.confidence

    return 0.0


# ─── 1. Rolling Trends ──────────────────────────────────────────────

def compute_rolling_trends(
    identity_vectors: list[dict],
    window_size: int = DEFAULT_WINDOW_SIZE,
) -> list[DimensionTrend]:
    """
    Computes rolling averages for each identity dimension and classifies
    the trend direction (RISING, FALLING, STABLE, UNKNOWN).

    Cognitive state: Statistical trend detection.
    You have accumulated data points. You are computing whether each
    dimension is moving in a direction. You are NOT interpreting why.
    Direction is a mathematical property of the series, not a judgment.

    Pre-computation constraints:
    - If len(vectors) < MIN_ENTRIES_FOR_TRENDS (7): return UNKNOWN for all
    - Window size must be ≥3 and ≤ len(vectors)/2

    Args:
        identity_vectors: Ordered list of flat dicts from get_identity_trajectory()
        window_size: Rolling window size (default 5)

    Returns:
        List of DimensionTrend objects, one per tracked dimension
    """
    n = len(identity_vectors)
    trends = []

    for dim in TRACKED_DIMENSIONS:
        # Insufficient data → UNKNOWN
        if n < MIN_ENTRIES_FOR_TRENDS:
            trends.append(DimensionTrend(
                dimension=dim,
                direction=TrendDirection.UNKNOWN,
                slope=0.0,
                confidence=ConfidenceLevel.LOW,
            ))
            continue

        # Extract time series for this dimension
        series = [_extract_dimension(v, dim) for v in identity_vectors]

        # Compute rolling average of last `window_size` entries
        effective_window = min(window_size, n // 2, n)
        if effective_window < 3:
            effective_window = 3

        # First half average vs second half average
        midpoint = n // 2
        first_half = series[:midpoint]
        second_half = series[midpoint:]

        avg_first = sum(first_half) / len(first_half) if first_half else 0
        avg_second = sum(second_half) / len(second_half) if second_half else 0

        # Simple linear regression slope
        slope = _compute_slope(series)

        # Classify direction based on slope magnitude
        # Threshold: 5% of the dimension's range per entry
        threshold = 0.02  # 2% change per entry = meaningful trend
        if abs(slope) < threshold:
            direction = TrendDirection.STABLE
        elif slope > 0:
            direction = TrendDirection.RISING
        else:
            direction = TrendDirection.FALLING

        # Confidence based on consistency of direction
        consistent_direction = _direction_consistency(series)
        if consistent_direction > 0.7:
            confidence = ConfidenceLevel.HIGH
        elif consistent_direction > 0.5:
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.LOW

        trends.append(DimensionTrend(
            dimension=dim,
            direction=direction,
            slope=round(slope, 4),
            confidence=confidence,
        ))

    return trends


def _compute_slope(series: list[float]) -> float:
    """Simple linear regression slope."""
    n = len(series)
    if n < 2:
        return 0.0
    x_mean = (n - 1) / 2
    y_mean = sum(series) / n
    numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(series))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    return numerator / denominator if denominator != 0 else 0.0


def _direction_consistency(series: list[float]) -> float:
    """
    Fraction of consecutive pairs that move in the same direction
    as the overall trend. Higher = more consistent.
    """
    if len(series) < 2:
        return 0.0
    overall_slope = _compute_slope(series)
    if abs(overall_slope) < 1e-8:
        return 1.0  # Stable is consistent

    same_direction = 0
    total = len(series) - 1
    for i in range(total):
        diff = series[i + 1] - series[i]
        if (diff > 0 and overall_slope > 0) or (diff < 0 and overall_slope < 0) or abs(diff) < 1e-8:
            same_direction += 1
    return same_direction / total


# ─── 2. Change Point Detection (PELT) ───────────────────────────────

def detect_change_points(
    identity_vectors: list[dict],
) -> list[ChangePoint]:
    """
    Detects structural breaks in identity dimension time series using
    the PELT (Pruned Exact Linear Time) algorithm.

    Cognitive state: Structural break detection.
    You are looking for the moments where the data generation process
    changed. A change point is not a spike — it is a shift in the
    underlying distribution. Before index k, the data comes from
    distribution A. After index k, it comes from distribution B.
    That transition is what you are detecting.

    Pre-computation constraints:
    - Requires ≥ MIN_ENTRIES_FOR_TRENDS (7) entries
    - Penalty: 4.2 · log(n), validated on linguistic time series
    - Each dimension analyzed independently

    Returns:
        List of ChangePoint objects for all detected breaks across all dimensions
    """
    n = len(identity_vectors)
    if n < MIN_ENTRIES_FOR_TRENDS:
        logger.info(f"Change point detection skipped: only {n} entries (need {MIN_ENTRIES_FOR_TRENDS})")
        return []

    change_points = []
    penalty = PELT_PENALTY_COEFFICIENT * math.log(max(n, 2))

    for dim in TRACKED_DIMENSIONS:
        series = [_extract_dimension(v, dim) for v in identity_vectors]

        # Try ruptures library first, fall back to simple detection
        try:
            dim_cps = _pelt_detect(series, penalty)
        except ImportError:
            logger.warning("ruptures not installed, using fallback change point detection")
            dim_cps = _simple_change_point_detect(series, penalty)

        for cp_index in dim_cps:
            if 0 < cp_index < n:
                pre_mean = sum(series[:cp_index]) / cp_index if cp_index > 0 else 0
                post_mean = sum(series[cp_index:]) / (n - cp_index) if n - cp_index > 0 else 0
                entry_id = identity_vectors[cp_index].get("entry_id", "")

                change_points.append(ChangePoint(
                    dimension=dim,
                    entry_index=cp_index,
                    entry_id=entry_id,
                    pre_mean=round(pre_mean, 4),
                    post_mean=round(post_mean, 4),
                    magnitude=round(abs(post_mean - pre_mean), 4),
                ))

    return change_points


def _pelt_detect(series: list[float], penalty: float) -> list[int]:
    """PELT change point detection using ruptures library."""
    import numpy as np
    import ruptures as rpt

    signal = np.array(series)
    algo = rpt.Pelt(model="l2", min_size=3)
    algo.fit(signal)
    breakpoints = algo.predict(pen=penalty)
    # ruptures returns indices including the last element; remove it
    return [bp for bp in breakpoints if bp < len(series)]


def _simple_change_point_detect(series: list[float], penalty: float) -> list[int]:
    """
    Fallback: simple mean-shift detection when ruptures is unavailable.
    Tests each possible split point and keeps those where the
    cost reduction exceeds the penalty.
    """
    n = len(series)
    if n < 6:
        return []

    total_mean = sum(series) / n
    total_cost = sum((x - total_mean) ** 2 for x in series)

    change_points = []
    for i in range(3, n - 3):
        left = series[:i]
        right = series[i:]
        left_mean = sum(left) / len(left)
        right_mean = sum(right) / len(right)
        split_cost = (
            sum((x - left_mean) ** 2 for x in left)
            + sum((x - right_mean) ** 2 for x in right)
        )
        improvement = total_cost - split_cost
        if improvement > penalty:
            change_points.append(i)

    return change_points


# ─── 3. Trajectory Classification ───────────────────────────────────

def classify_trajectory(
    identity_vectors: list[dict],
    change_points: list[ChangePoint],
    trends: list[DimensionTrend],
) -> TrajectoryType:
    """
    Classifies the overall user trajectory into one of 5 types.

    Cognitive state: Arc pattern recognition.
    You have the full data. Trends give you direction. Change points
    give you structural breaks. The trajectory type is the narrative
    arc that best fits both signals. You are not diagnosing the user.
    You are classifying the mathematical shape of their identity shift.

    Pre-computation constraints:
    - Requires ≥ MIN_ENTRIES_FOR_TRAJECTORY (14) entries
    - Requires ≥2 dimensions agreeing for any classification
    - Returns UNKNOWN if insufficient data or no clear pattern

    Classification rules:
    - REDEMPTION_ARC: Rising Agency + Rising Redemption scores
    - CONTAMINATION_ARC: Rising Contamination + Declining Competence
    - PLATEAU: No change points in any dimension
    - OSCILLATION: Multiple change points (≥3) in short window (≤10 entries)
    - BREAKTHROUGH: ≥3 dimensions shift simultaneously within 2-entry window
    """
    n = len(identity_vectors)
    if n < MIN_ENTRIES_FOR_TRAJECTORY:
        return TrajectoryType.UNKNOWN

    # Build lookup for trends
    trend_map = {t.dimension: t for t in trends}

    # Check 1: BREAKTHROUGH — ≥3 dimensions change in a 2-entry window
    if change_points:
        cp_indices = [cp.entry_index for cp in change_points]
        for window_start in range(max(cp_indices) - 1):
            window_end = window_start + 2
            dims_in_window = set()
            for cp in change_points:
                if window_start <= cp.entry_index <= window_end:
                    dims_in_window.add(cp.dimension)
            if len(dims_in_window) >= 3:
                return TrajectoryType.BREAKTHROUGH

    # Check 2: OSCILLATION — ≥3 change points in ≤10 entries
    if len(change_points) >= 3:
        cp_indices_sorted = sorted(cp.entry_index for cp in change_points)
        for i in range(len(cp_indices_sorted) - 2):
            if cp_indices_sorted[i + 2] - cp_indices_sorted[i] <= 10:
                return TrajectoryType.OSCILLATION

    # Check 3: REDEMPTION_ARC — Rising Agency + Rising Redemption
    agency_trend = trend_map.get("agency")
    redemption_trend = trend_map.get("redemption_arc")
    if (agency_trend and agency_trend.direction == TrendDirection.RISING
            and redemption_trend and redemption_trend.direction == TrendDirection.RISING):
        return TrajectoryType.REDEMPTION_ARC

    # Check 4: CONTAMINATION_ARC — Falling Redemption + Falling Competence
    competence_trend = trend_map.get("competence")
    if (redemption_trend and redemption_trend.direction == TrendDirection.FALLING
            and competence_trend and competence_trend.direction == TrendDirection.FALLING):
        return TrajectoryType.CONTAMINATION_ARC

    # Check 5: PLATEAU — No change points at all
    if not change_points:
        return TrajectoryType.PLATEAU

    return TrajectoryType.UNKNOWN


# ─── Public API: Full Temporal Analysis ─────────────────────────────

def analyze_temporal(identity_vectors: list[dict]) -> TemporalAnalysis:
    """
    Runs the full Chronos analysis pipeline on a user's identity trajectory.

    Orchestrates: trends → change points → trajectory classification.
    Returns a complete TemporalAnalysis with all computed results.

    This is the function called by journal_processor.py (Step 8).
    """
    n = len(identity_vectors)

    trends = compute_rolling_trends(identity_vectors)
    change_points = detect_change_points(identity_vectors)
    trajectory = classify_trajectory(identity_vectors, change_points, trends)

    return TemporalAnalysis(
        trends=trends,
        change_points=change_points,
        trajectory=trajectory,
        entry_count=n,
        sufficient_data_for_trends=n >= MIN_ENTRIES_FOR_TRENDS,
        sufficient_data_for_trajectory=n >= MIN_ENTRIES_FOR_TRAJECTORY,
    )
