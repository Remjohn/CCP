"""
CCP Guardian Agent — Stewardship Mode (DEP-PROTO-020)
FR-GA Task 4 — Weekly Signal Monitoring Protocol + Stewardship Reports.

Post-genesis, the Guardian Agent monitors 3 signal categories weekly:
1. Lexicon Drift — unmapped vocabulary in CBCS data
2. Cultural Evolution — character relevance drops below 0.4
3. Campaign Fatigue — declining conversions, character repeats

Spec references:
- FR_GA_Guardian_Agent_Tech_Spec.md §Stewardship Mode
- FR_GA_Guardian_Agent_Tech_Spec.md §Authenticity Floor Calibration
- FR_GA_Guardian_Agent_Tech_Spec.md §Evolutionary Recalibration Handshake
- FR_GA_Guardian_Agent_Tech_Spec.md §Data Promotion Timeout Deadlock

AC2: When 5+ character_lexicon entries drop below relevance_score 0.4,
     Stewardship Mode generates a Cultural Evolution Signal.
AC3: Refresh recommendation NOT executed until /ccf-guardian approve [id] issued.

Usage:
    from src.ccp.services.stewardship_monitor import StewardshipMonitor

    monitor = StewardshipMonitor(coach_id="NDL-0000", coach_acronym="NDL")
    signals = await monitor.run_weekly_sweep()
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.stewardship_models import (
    DataPromotionTimeout,
    EvolutionaryRecalibration,
    RecommendationStatus,
    RefreshRecommendation,
    SignalDetection,
    SignalType,
    StewardshipReport,
)


class StewardshipMonitor:
    """Weekly Signal Monitoring Protocol (DEP-PROTO-020).

    Runs three signal checks and generates RefreshRecommendations
    that require operator approval before execution.
    """

    # Thresholds from spec
    CHARACTER_RELEVANCE_THRESHOLD = 0.4  # AC2: below this triggers Cultural Evolution signal
    CHARACTER_DROP_COUNT_THRESHOLD = 5   # AC2: 5+ entries below threshold
    CHARACTER_REPEAT_THRESHOLD = 3       # Campaign Fatigue: >3 repeats in 8 weeks
    UNMAPPED_TERM_THRESHOLD = 3          # Lexicon Drift: 3+ occurrences of unmapped terms
    TTT_DRIFT_THRESHOLD = 0.15          # 15% drift threshold for recalibration
    TTT_CONSECUTIVE_WEEKS = 4           # 4 consecutive weeks for re-extraction trigger
    PROMOTION_TIMEOUT_DAYS = 21         # Data promotion timeout deadlock

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        base_dir: str = "./coaches",
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.base_dir = Path(base_dir)
        self.coach_dir = self.base_dir / self.coach_acronym

        self.receipt_chain = ReceiptChain(
            coach_acronym=self.coach_acronym,
            log_dir=str(self.coach_dir / "logs" / "receipt_chain"),
        )

        # State persistence
        self.state_dir = self.coach_dir / "config" / "guardian"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    async def run_weekly_sweep(self) -> list[SignalDetection]:
        """Execute all 3 signal monitoring checks.

        Returns:
            List of detected signals. Each signal with sufficient severity
            generates a RefreshRecommendation requiring operator approval.
        """
        print(f"\n  🔍 STEWARDSHIP SWEEP — {self.coach_acronym}")
        print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

        all_signals: list[SignalDetection] = []

        # Log sweep initiation
        sweep_receipt = self.receipt_chain.log(
            agent_id="guardian_agent",
            action="stewardship_sweep_started",
            input_summary=f"Weekly signal monitoring for {self.coach_id}",
            output_summary="Starting 3-signal sweep",
            decision="started",
        )

        # Signal 1: Lexicon Drift
        print("\n  📖 Signal 1/3: Lexicon Drift...")
        lexicon_signals = await self._check_lexicon_drift()
        all_signals.extend(lexicon_signals)
        if lexicon_signals:
            print(f"     ⚠️  {len(lexicon_signals)} drift signals detected")
        else:
            print("     ✅ No drift detected")

        # Signal 2: Cultural Evolution
        print("\n  🎭 Signal 2/3: Cultural Evolution...")
        cultural_signals = await self._check_cultural_evolution()
        all_signals.extend(cultural_signals)
        if cultural_signals:
            print(f"     ⚠️  {len(cultural_signals)} evolution signals detected")
        else:
            print("     ✅ No evolution signals")

        # Signal 3: Campaign Fatigue
        print("\n  📊 Signal 3/3: Campaign Fatigue...")
        fatigue_signals = await self._check_campaign_fatigue()
        all_signals.extend(fatigue_signals)
        if fatigue_signals:
            print(f"     ⚠️  {len(fatigue_signals)} fatigue signals detected")
        else:
            print("     ✅ No fatigue signals")

        # Check Evolutionary Recalibration
        print("\n  🧬 Checking TTT Drift Recalibration...")
        recalibration = await self._check_evolutionary_recalibration()

        # Check Data Promotion Timeouts
        print("  ⏱️  Checking Data Promotion Timeouts...")
        blocking = await self._check_promotion_timeouts()

        # Generate recommendations for detected signals
        recommendations = self._generate_recommendations(all_signals)
        if recommendations:
            self._save_recommendations(recommendations)
            print(f"\n  📋 {len(recommendations)} new recommendations generated (require operator approval)")

        # Log sweep completion
        self.receipt_chain.log(
            agent_id="guardian_agent",
            action="stewardship_sweep_complete",
            input_summary=f"Weekly sweep for {self.coach_id}",
            output_summary=f"Signals: {len(all_signals)}, Recommendations: {len(recommendations)}",
            decision="completed",
            parent_receipt_id=sweep_receipt.receipt_id,
            metadata={
                "total_signals": len(all_signals),
                "lexicon_drift_count": len(lexicon_signals),
                "cultural_evolution_count": len(cultural_signals),
                "campaign_fatigue_count": len(fatigue_signals),
                "recommendations_generated": len(recommendations),
                "recalibration_triggered": recalibration is not None and recalibration.re_extraction_triggered,
                "blocking_promotions": len(blocking),
            },
        )

        # Save sweep history
        self._save_sweep_history(all_signals)

        return all_signals

    # ──────────────────────────────────────────────────────────
    # Signal 1: Lexicon Drift
    # ──────────────────────────────────────────────────────────

    async def _check_lexicon_drift(self) -> list[SignalDetection]:
        """Detect unmapped vocabulary in CBCS interaction data.

        Spec: Triggers recommendation for Tribe Lexicon addition when
        3+ occurrences of unmapped terms detected.
        """
        signals: list[SignalDetection] = []

        # Load tribe lexicon and recent CBCS data
        unmapped_terms = await self._find_unmapped_terms()

        if unmapped_terms:
            signals.append(
                SignalDetection(
                    signal_type=SignalType.LEXICON_DRIFT,
                    evidence=[
                        f"Unmapped term: '{term}' ({count} occurrences)"
                        for term, count in unmapped_terms.items()
                    ],
                    severity=min(len(unmapped_terms) / 10.0, 1.0),
                    affected_dep_ids=["DEP-ENG-007", "DEP-ENG-023"],
                    metrics={
                        "unmapped_term_count": len(unmapped_terms),
                        "terms": unmapped_terms,
                    },
                )
            )

        return signals

    async def _find_unmapped_terms(self) -> dict[str, int]:
        """Find terms in CBCS data not present in tribe lexicon.

        Stub: returns empty dict. Will query Supabase/Neo4j when
        CBCS and tribe lexicon infrastructure is built.
        """
        # Stub — will be populated when CBCS and tribe data are available
        return {}

    # ──────────────────────────────────────────────────────────
    # Signal 2: Cultural Evolution
    # ──────────────────────────────────────────────────────────

    async def _check_cultural_evolution(self) -> list[SignalDetection]:
        """Detect character relevance drops and emerging figures.

        AC2: When 5+ character_lexicon entries drop below relevance_score 0.4,
        generate a Cultural Evolution Signal.
        """
        signals: list[SignalDetection] = []

        # Load character lexicon
        low_relevance = await self._find_low_relevance_characters()

        if len(low_relevance) >= self.CHARACTER_DROP_COUNT_THRESHOLD:
            signals.append(
                SignalDetection(
                    signal_type=SignalType.CULTURAL_EVOLUTION,
                    evidence=[
                        f"Character '{char['name']}' relevance dropped to {char['relevance_score']:.2f}"
                        for char in low_relevance
                    ],
                    severity=min(len(low_relevance) / 15.0, 1.0),
                    affected_dep_ids=["CHARACTER-LEXICON", "DEP-PROTO-017"],
                    metrics={
                        "low_relevance_count": len(low_relevance),
                        "threshold": self.CHARACTER_RELEVANCE_THRESHOLD,
                        "characters": low_relevance,
                    },
                )
            )

        return signals

    async def _find_low_relevance_characters(self) -> list[dict[str, Any]]:
        """Find character lexicon entries below relevance threshold.

        Stub: returns empty list. Will query character lexicon data when
        FR0C infrastructure is built.
        """
        # Stub — will be populated when Character Lexicon data is available
        return []

    # ──────────────────────────────────────────────────────────
    # Signal 3: Campaign Fatigue
    # ──────────────────────────────────────────────────────────

    async def _check_campaign_fatigue(self) -> list[SignalDetection]:
        """Detect declining semiotic combo conversions and character over-use.

        Spec: Semiotic combo conversions drop or character repeats >3 times
        in 8 weeks → adjust deployment weights.
        """
        signals: list[SignalDetection] = []

        # Check character repetition
        repeated_chars = await self._find_overused_characters()
        # Check semiotic conversion decline
        declining_combos = await self._find_declining_combos()

        evidence = []
        if repeated_chars:
            evidence.extend([
                f"Character '{char}' used {count} times in 8 weeks (limit: {self.CHARACTER_REPEAT_THRESHOLD})"
                for char, count in repeated_chars.items()
            ])
        if declining_combos:
            evidence.extend([
                f"Semiotic combo '{combo}' conversion declined by {drop:.0%}"
                for combo, drop in declining_combos.items()
            ])

        if evidence:
            signals.append(
                SignalDetection(
                    signal_type=SignalType.CAMPAIGN_FATIGUE,
                    evidence=evidence,
                    severity=min((len(repeated_chars) + len(declining_combos)) / 10.0, 1.0),
                    affected_dep_ids=["DEP-ENG-025", "CHARACTER-LEXICON"],
                    metrics={
                        "overused_characters": repeated_chars,
                        "declining_combos": declining_combos,
                    },
                )
            )

        return signals

    async def _find_overused_characters(self) -> dict[str, int]:
        """Find characters used more than threshold times in 8-week window.

        Stub: returns empty dict.
        """
        return {}

    async def _find_declining_combos(self) -> dict[str, float]:
        """Find semiotic combos with declining conversion rates.

        Stub: returns empty dict.
        """
        return {}

    # ──────────────────────────────────────────────────────────
    # Evolutionary Recalibration Handshake
    # ──────────────────────────────────────────────────────────

    async def _check_evolutionary_recalibration(self) -> Optional[EvolutionaryRecalibration]:
        """Check if sustained TTT drift should trigger DEP-ENG-005 re-extraction.

        Spec: If >15% drift towards a NEW authentic vector for 4 consecutive
        weeks, trigger re-extraction. Sophia's baseline permanently updated.
        """
        recal = self._load_recalibration_state()
        if recal is None:
            return None

        if recal.should_trigger():
            recal.re_extraction_triggered = True
            recal.triggered_at = datetime.now(timezone.utc).isoformat()
            self._save_recalibration_state(recal)

            self.receipt_chain.log(
                agent_id="guardian_agent",
                action="evolutionary_recalibration_triggered",
                input_summary=f"TTT drift >{self.TTT_DRIFT_THRESHOLD:.0%} for {recal.consecutive_weeks} consecutive weeks",
                output_summary="DEP-ENG-005 Re-Extraction Event triggered — Sophia baseline will be updated",
                decision="triggered",
                metadata={
                    "consecutive_weeks": recal.consecutive_weeks,
                    "drift_percentages": recal.drift_percentages,
                    "drift_direction": recal.drift_direction,
                },
            )

            print(f"     🔄 RECALIBRATION TRIGGERED: {recal.consecutive_weeks} weeks of >{self.TTT_DRIFT_THRESHOLD:.0%} drift")
        else:
            print(f"     ✅ No recalibration needed (weeks: {recal.consecutive_weeks}/{self.TTT_CONSECUTIVE_WEEKS})")

        return recal

    # ──────────────────────────────────────────────────────────
    # Data Promotion Timeout Deadlock
    # ──────────────────────────────────────────────────────────

    async def _check_promotion_timeouts(self) -> list[DataPromotionTimeout]:
        """Check for patterns blocked by unreviewed promotions.

        Spec: 14-consecutive-session threshold + 21-day unreviewed →
        CRITICAL_BLOCKING → pipeline halt. NO auto-promotion bypass.
        """
        promotions = self._load_promotion_queue()
        blocking: list[DataPromotionTimeout] = []

        for promo in promotions:
            if promo.status == "PENDING" and promo.check_timeout():
                promo.status = "CRITICAL_BLOCKING"
                blocking.append(promo)

                self.receipt_chain.log(
                    agent_id="guardian_agent",
                    action="promotion_timeout_blocking",
                    input_summary=f"Pattern '{promo.pattern_description}' pending for >{self.PROMOTION_TIMEOUT_DAYS} days",
                    output_summary="CRITICAL_BLOCKING — pipeline execution halted until operator resolves",
                    decision="blocked",
                    metadata={
                        "pattern_id": promo.pattern_id,
                        "queued_at": promo.queued_at,
                        "consecutive_sessions": promo.consecutive_sessions,
                    },
                )

                print(f"     🚫 BLOCKING: Pattern '{promo.pattern_description}' — {self.PROMOTION_TIMEOUT_DAYS}+ days unreviewed")

        if blocking:
            self._save_promotion_queue(promotions)

        if not blocking:
            print("     ✅ No timeout deadlocks")

        return blocking

    # ──────────────────────────────────────────────────────────
    # Recommendation Generation
    # ──────────────────────────────────────────────────────────

    def _generate_recommendations(
        self,
        signals: list[SignalDetection],
    ) -> list[RefreshRecommendation]:
        """Generate refresh recommendations from detected signals.

        AC3: Recommendations are NOT executed until operator approves.
        """
        recommendations: list[RefreshRecommendation] = []

        for signal in signals:
            action = self._signal_to_action(signal)
            if action:
                rec = RefreshRecommendation(
                    recommendation_id=str(uuid.uuid4())[:8],
                    coach_id=self.coach_id,
                    signal_type=signal.signal_type,
                    signal_detections=[signal],
                    recommended_action=action,
                    affected_components=self._signal_to_components(signal),
                    status=RecommendationStatus.PENDING,
                )
                recommendations.append(rec)

        return recommendations

    def _signal_to_action(self, signal: SignalDetection) -> str:
        """Convert a signal to a recommended action string."""
        action_map = {
            SignalType.LEXICON_DRIFT: "Add unmapped terms to Tribe Lexicon (DEP-ENG-007) and update Cultural Memory Map (DEP-ENG-023)",
            SignalType.CULTURAL_EVOLUTION: "Refresh Character Lexicon entries with low relevance scores. Consider partial dossier refresh or character rescore.",
            SignalType.CAMPAIGN_FATIGUE: "Adjust character deployment weights and semiotic combo rotation to reduce repetition.",
        }
        return action_map.get(signal.signal_type, "")

    def _signal_to_components(self, signal: SignalDetection) -> list[str]:
        """Map a signal type to affected component names."""
        component_map = {
            SignalType.LEXICON_DRIFT: ["tribe_lexicon", "cultural_memory_map"],
            SignalType.CULTURAL_EVOLUTION: ["character_lexicon", "character_invocation_protocol"],
            SignalType.CAMPAIGN_FATIGUE: ["content_performance_registry", "character_deployment"],
        }
        return component_map.get(signal.signal_type, [])

    # ──────────────────────────────────────────────────────────
    # Recommendation Approval (for slash command handler)
    # ──────────────────────────────────────────────────────────

    def approve_recommendation(
        self,
        recommendation_id: str,
        approved_by: str,
    ) -> Optional[RefreshRecommendation]:
        """Approve a pending recommendation.

        AC3: Recommendation NOT executed until this is called via
        /ccf-guardian approve [recommendation_id].
        """
        recommendations = self._load_recommendations()

        for rec in recommendations:
            if rec.recommendation_id == recommendation_id:
                if rec.status != RecommendationStatus.PENDING:
                    return None  # Already approved/rejected

                rec.status = RecommendationStatus.APPROVED
                rec.approved_at = datetime.now(timezone.utc).isoformat()
                rec.approved_by = approved_by

                # Log approval
                receipt = self.receipt_chain.log(
                    agent_id="guardian_agent",
                    action="stewardship_recommendation_approved",
                    input_summary=f"Recommendation {recommendation_id} approved by {approved_by}",
                    output_summary=f"Action: {rec.recommended_action}",
                    decision="approved",
                    metadata={
                        "recommendation_id": recommendation_id,
                        "signal_type": rec.signal_type.value,
                        "affected_components": rec.affected_components,
                    },
                )
                rec.receipt_id = receipt.receipt_id

                self._save_recommendations(recommendations)
                return rec

        return None

    def reject_recommendation(
        self,
        recommendation_id: str,
        rejected_by: str,
    ) -> Optional[RefreshRecommendation]:
        """Reject a pending recommendation."""
        recommendations = self._load_recommendations()

        for rec in recommendations:
            if rec.recommendation_id == recommendation_id:
                if rec.status != RecommendationStatus.PENDING:
                    return None

                rec.status = RecommendationStatus.REJECTED
                rec.approved_by = rejected_by  # Reusing field for actor
                rec.approved_at = datetime.now(timezone.utc).isoformat()

                self.receipt_chain.log(
                    agent_id="guardian_agent",
                    action="stewardship_recommendation_rejected",
                    input_summary=f"Recommendation {recommendation_id} rejected by {rejected_by}",
                    output_summary=f"Action: {rec.recommended_action}",
                    decision="rejected",
                    metadata={"recommendation_id": recommendation_id},
                )

                self._save_recommendations(recommendations)
                return rec

        return None

    def get_pending_recommendations(self) -> list[RefreshRecommendation]:
        """Get all PENDING recommendations."""
        recommendations = self._load_recommendations()
        return [r for r in recommendations if r.status == RecommendationStatus.PENDING]

    # ──────────────────────────────────────────────────────────
    # Quarterly Report Generation (DEP-ENG-053)
    # ──────────────────────────────────────────────────────────

    def generate_quarterly_report(self, quarter: str) -> StewardshipReport:
        """Generate the quarterly Stewardship Report (DEP-ENG-053)."""
        recommendations = self._load_recommendations()
        sweep_history = self._load_sweep_history()

        report = StewardshipReport(
            report_id=str(uuid.uuid4())[:8],
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            quarter=quarter,
            total_signals_detected=len(sweep_history),
            signals_by_type={
                SignalType.LEXICON_DRIFT.value: sum(
                    1 for s in sweep_history if s.signal_type == SignalType.LEXICON_DRIFT
                ),
                SignalType.CULTURAL_EVOLUTION.value: sum(
                    1 for s in sweep_history if s.signal_type == SignalType.CULTURAL_EVOLUTION
                ),
                SignalType.CAMPAIGN_FATIGUE.value: sum(
                    1 for s in sweep_history if s.signal_type == SignalType.CAMPAIGN_FATIGUE
                ),
            },
            signal_detections=sweep_history,
            total_recommendations=len(recommendations),
            approved_recommendations=[
                r for r in recommendations if r.status == RecommendationStatus.APPROVED
            ],
            pending_recommendations=[
                r for r in recommendations if r.status == RecommendationStatus.PENDING
            ],
            rejected_recommendations=[
                r for r in recommendations if r.status == RecommendationStatus.REJECTED
            ],
            ttt_drift_status=self._load_recalibration_state(),
            data_promotion_queue=self._load_promotion_queue(),
        )

        # Save report
        report_path = self.state_dir / f"stewardship_report_{quarter}.json"
        report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")

        self.receipt_chain.log(
            agent_id="guardian_agent",
            action="stewardship_report_generated",
            input_summary=f"Quarterly report for {quarter}",
            output_summary=f"Signals: {report.total_signals_detected}, Recommendations: {report.total_recommendations}",
            decision="completed",
            metadata={
                "report_id": report.report_id,
                "quarter": quarter,
            },
        )

        return report

    # ──────────────────────────────────────────────────────────
    # State Persistence Helpers
    # ──────────────────────────────────────────────────────────

    def _save_recommendations(self, recs: list[RefreshRecommendation]) -> None:
        path = self.state_dir / "recommendations.json"
        data = [r.model_dump() for r in recs]
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    def _load_recommendations(self) -> list[RefreshRecommendation]:
        path = self.state_dir / "recommendations.json"
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return [RefreshRecommendation.model_validate(item) for item in data]

    def _save_sweep_history(self, signals: list[SignalDetection]) -> None:
        path = self.state_dir / "sweep_history.json"
        existing = self._load_sweep_history()
        existing.extend(signals)
        data = [s.model_dump() for s in existing]
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    def _load_sweep_history(self) -> list[SignalDetection]:
        path = self.state_dir / "sweep_history.json"
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return [SignalDetection.model_validate(item) for item in data]

    def _load_recalibration_state(self) -> Optional[EvolutionaryRecalibration]:
        path = self.state_dir / "recalibration_state.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return EvolutionaryRecalibration.model_validate(data)

    def _save_recalibration_state(self, state: EvolutionaryRecalibration) -> None:
        path = self.state_dir / "recalibration_state.json"
        path.write_text(state.model_dump_json(indent=2), encoding="utf-8")

    def _load_promotion_queue(self) -> list[DataPromotionTimeout]:
        path = self.state_dir / "promotion_queue.json"
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return [DataPromotionTimeout.model_validate(item) for item in data]

    def _save_promotion_queue(self, queue: list[DataPromotionTimeout]) -> None:
        path = self.state_dir / "promotion_queue.json"
        data = [p.model_dump() for p in queue]
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
