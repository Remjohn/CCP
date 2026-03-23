"""
CCP FR5 Trigger Map Builder — Trigger Feedback Loop (Unit 8)
Weekly feedback loop: activation_history + LIWC-22 scoring → precedence update.

Spec reference: FR5 Tech Spec §Weekly Feedback Loop
  - Records when triggers are activated in content production
  - Scores activation using LIWC-22 markers
  - After ≥3 activation_history entries per trigger, calculates precedence:
      * climb — increasing engagement/activation trend
      * hold — stable engagement/activation trend
      * fall — declining engagement/activation trend
      * dormant — no activation in ≥4 weeks
  - Writes TMAP-WEEKLY-UPDATE receipt

Research basis:
  LIWC-22 (Pennebaker) — linguistic marker scoring
  Haidt MFT foundation stability — foundations shift with major life events
"""

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.models.trigger_map_models import (
    LIWC_22_TRIGGER_MARKERS,
    MINIMUM_ACTIVATION_ENTRIES_FOR_PRECEDENCE,
    ActivationHistoryEntry,
    PrecedenceCalculation,
    TriggerMap,
    TriggerPrecedence,
)


class TriggerFeedbackLoop:
    """Weekly feedback loop service for trigger map maintenance.

    After content production activates triggers, this service:
    1. Records activation events with LIWC-22 scores
    2. After ≥3 entries per trigger, calculates precedence
    3. Updates trigger precedence: climb/hold/fall/dormant

    Spec: 'The weekly feedback loop runs after each content batch
    to track which triggers are being activated and how effectively.'
    """

    # Weeks without activation before marking dormant
    DORMANT_THRESHOLD_WEEKS: int = 4

    # Trend thresholds for precedence calculation
    CLIMB_THRESHOLD: float = 0.1  # positive trend > 10%
    FALL_THRESHOLD: float = -0.1  # negative trend < -10%

    def record_activation(
        self,
        trigger_map: TriggerMap,
        trigger_id: str,
        content_asset_id: str,
        liwc_scores: Optional[dict[str, float]] = None,
        engagement_metrics: Optional[dict[str, Any]] = None,
        notes: str = "",
    ) -> ActivationHistoryEntry:
        """Record a trigger activation event.

        Args:
            trigger_map: The trigger map to update.
            trigger_id: ID of the activated trigger.
            content_asset_id: Asset ID of the content that activated it.
            liwc_scores: LIWC-22 marker scores from the activation content.
            engagement_metrics: Engagement data from content performance.
            notes: Additional notes about the activation.

        Returns:
            The created ActivationHistoryEntry.
        """
        entry = ActivationHistoryEntry(
            activation_id=f"act_{trigger_id}_{len(trigger_map.activation_history) + 1:04d}",
            trigger_id=trigger_id,
            activation_date=datetime.now(timezone.utc).isoformat(),
            content_asset_id=content_asset_id,
            liwc_22_scores=liwc_scores or {},
            engagement_metrics=engagement_metrics or {},
            notes=notes,
        )

        trigger_map.activation_history.append(entry)
        return entry

    def calculate_precedence(
        self, trigger_map: TriggerMap
    ) -> list[PrecedenceCalculation]:
        """Calculate precedence for all triggers with sufficient activation data.

        Spec: 'Precedence recalculation requires ≥3 activation_history entries.
        climb = increasing trend, hold = stable, fall = declining, dormant = ≥4 weeks inactive.'

        Args:
            trigger_map: The trigger map with activation history.

        Returns:
            List of PrecedenceCalculation results.
        """
        calculations: list[PrecedenceCalculation] = []

        # Collect all unique trigger IDs
        all_triggers = trigger_map.triggers + trigger_map.candidate_triggers
        trigger_ids = {t.trigger_id for t in all_triggers}

        for trigger_id in trigger_ids:
            # Get activation entries for this trigger
            entries = [
                e
                for e in trigger_map.activation_history
                if e.trigger_id == trigger_id
            ]

            calc = self._calculate_single_trigger_precedence(
                trigger_id=trigger_id,
                entries=entries,
            )
            calculations.append(calc)

            # Update the trigger's precedence in the map
            self._apply_precedence_to_trigger(trigger_map, trigger_id, calc)

        return calculations

    def _calculate_single_trigger_precedence(
        self,
        trigger_id: str,
        entries: list[ActivationHistoryEntry],
    ) -> PrecedenceCalculation:
        """Calculate precedence for a single trigger.

        Requirements:
        - ≥3 entries to calculate trend
        - dormant if no activation in ≥4 weeks
        """
        now = datetime.now(timezone.utc)

        if not entries:
            return PrecedenceCalculation(
                trigger_id=trigger_id,
                precedence=TriggerPrecedence.DORMANT,
                activation_count=0,
                trend_direction=0.0,
                evidence_summary="No activation entries — dormant",
            )

        activation_count = len(entries)

        # Check dormancy: no activation in ≥4 weeks
        try:
            latest_date = max(
                datetime.fromisoformat(e.activation_date.replace("Z", "+00:00"))
                for e in entries
            )
            weeks_since_last = (now - latest_date).days / 7.0
        except (ValueError, TypeError):
            weeks_since_last = float(self.DORMANT_THRESHOLD_WEEKS + 1)

        if weeks_since_last >= self.DORMANT_THRESHOLD_WEEKS:
            return PrecedenceCalculation(
                trigger_id=trigger_id,
                precedence=TriggerPrecedence.DORMANT,
                activation_count=activation_count,
                trend_direction=0.0,
                evidence_summary=(
                    f"No activation in {weeks_since_last:.1f} weeks — dormant"
                ),
            )

        # Need ≥3 entries for trend calculation
        if activation_count < MINIMUM_ACTIVATION_ENTRIES_FOR_PRECEDENCE:
            return PrecedenceCalculation(
                trigger_id=trigger_id,
                precedence=TriggerPrecedence.HOLD,
                activation_count=activation_count,
                trend_direction=0.0,
                evidence_summary=(
                    f"Insufficient entries ({activation_count}/"
                    f"{MINIMUM_ACTIVATION_ENTRIES_FOR_PRECEDENCE}) — hold"
                ),
            )

        # Calculate trend from engagement metrics
        trend = self._calculate_trend(entries)

        if trend > self.CLIMB_THRESHOLD:
            precedence = TriggerPrecedence.CLIMB
            summary = f"Positive trend ({trend:+.2f}) — climbing"
        elif trend < self.FALL_THRESHOLD:
            precedence = TriggerPrecedence.FALL
            summary = f"Negative trend ({trend:+.2f}) — falling"
        else:
            precedence = TriggerPrecedence.HOLD
            summary = f"Stable trend ({trend:+.2f}) — hold"

        return PrecedenceCalculation(
            trigger_id=trigger_id,
            precedence=precedence,
            activation_count=activation_count,
            trend_direction=trend,
            evidence_summary=summary,
        )

    def _calculate_trend(self, entries: list[ActivationHistoryEntry]) -> float:
        """Calculate engagement trend from activation entries.

        Uses a simple linear trend over the last N entries.
        Trend is computed from engagement metrics if available,
        falls back to LIWC-22 score averages.
        """
        if len(entries) < 2:
            return 0.0

        # Sort by activation date
        sorted_entries = sorted(entries, key=lambda e: e.activation_date)

        # Try engagement metrics first
        engagement_values = []
        for entry in sorted_entries:
            if entry.engagement_metrics:
                # Use a composite engagement score if available
                score = entry.engagement_metrics.get(
                    "engagement_score",
                    entry.engagement_metrics.get(
                        "likes", entry.engagement_metrics.get("views", 0)
                    ),
                )
                try:
                    engagement_values.append(float(score))
                except (ValueError, TypeError):
                    pass

        if len(engagement_values) >= 2:
            return self._linear_trend(engagement_values)

        # Fall back to LIWC-22 score averages
        liwc_values = []
        for entry in sorted_entries:
            if entry.liwc_22_scores:
                avg_score = sum(entry.liwc_22_scores.values()) / len(
                    entry.liwc_22_scores
                )
                liwc_values.append(avg_score)

        if len(liwc_values) >= 2:
            return self._linear_trend(liwc_values)

        return 0.0

    def _linear_trend(self, values: list[float]) -> float:
        """Calculate a simple linear trend.
        Returns the normalized slope: positive = climbing, negative = falling."""
        if len(values) < 2:
            return 0.0

        n = len(values)
        x_mean = (n - 1) / 2.0
        y_mean = sum(values) / n

        numerator = sum(
            (i - x_mean) * (v - y_mean) for i, v in enumerate(values)
        )
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        slope = numerator / denominator

        # Normalize by y_mean to get relative trend
        if y_mean != 0:
            return slope / abs(y_mean)
        return slope

    def _apply_precedence_to_trigger(
        self,
        trigger_map: TriggerMap,
        trigger_id: str,
        calc: PrecedenceCalculation,
    ) -> None:
        """Apply the calculated precedence to the trigger in the map."""
        for trigger in trigger_map.triggers + trigger_map.candidate_triggers:
            if trigger.trigger_id == trigger_id:
                trigger.precedence = calc.precedence
                break

    def check_staleness(self, trigger_map: TriggerMap) -> bool:
        """Check if the trigger map needs recalibration.

        Spec: 'Monitors whether life events have shifted MFT weightings.
        Triggers recalibration when drift detected.'

        Returns True if recalibration is recommended.
        """
        # Check if map has enough history for drift detection
        if not trigger_map.activation_history:
            return False

        # Count dormant triggers
        all_triggers = trigger_map.triggers + trigger_map.candidate_triggers
        dormant_count = sum(
            1
            for t in all_triggers
            if t.precedence == TriggerPrecedence.DORMANT
        )
        total = len(all_triggers)

        if total == 0:
            return False

        # If >50% of triggers are dormant, recommend recalibration
        dormant_ratio = dormant_count / total
        if dormant_ratio > 0.5:
            trigger_map.staleness_tracking.drift_detected = True
            trigger_map.staleness_tracking.recalibration_recommended = True
            return True

        # Check for foundation weight drift via activation patterns
        # (simplified: flag if engagement trend is consistently falling)
        fall_count = sum(
            1
            for t in all_triggers
            if t.precedence == TriggerPrecedence.FALL
        )
        if total > 0 and fall_count / total > 0.4:
            trigger_map.staleness_tracking.drift_detected = True
            trigger_map.staleness_tracking.recalibration_recommended = True
            return True

        trigger_map.staleness_tracking.drift_detected = False
        trigger_map.staleness_tracking.recalibration_recommended = False
        return False
