"""
CCP FR7 Leadership Scorecard & Coach Development Engine — Pipeline Orchestrator (Unit 9)
Full pipeline: Phase 1 (INGEST) → Phase 6 (VALIDATE), with receipt chain.

Spec reference: FR7 Tech Spec §Phase 1-6, §Receipt Writes
Architecture reference: §6.3 (Minister of Identity — inference-time, read-only)
                        §5.3 (Genesis Pipeline Phase 0.5)

Receipt writes:
  Phase 1 INGEST:  stage_name = LEADERSHIP-SCORECARD-INGEST,  agent = minister_identity
  Phase 6 COMPLETE: stage_name = LEADERSHIP-SCORECARD-COMPLETE, agent = minister_identity

AC9:  Missing required dep → CANNOT_SCORE_MISSING_DEPENDENCIES
AC10: Minister of Identity is read-only — never writes to source DEP objects
AC1:  Production lock → PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD (enforced in Morgan, checked here)
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain, ReceiptEntry
from src.ccp.models.leadership_scorecard_models import (
    LeadershipScorecard,
    LeadershipScorecardPipelineSession,
    LeadershipPipelineStepStatus,
)
from src.ccp.services.category_evaluator import CategoryEvaluator
from src.ccp.services.format_governance_engine import FormatGovernanceEngine
from src.ccp.services.scorecard_emitter import ScorecardEmitter, ScorecardValidationError
from src.ccp.services.signal_source_loader import MissingDependencyError, SignalBundle, SignalSourceLoader
from src.ccp.services.trait_scoring_engine import TraitScoringEngine


def _hash_dict(data: dict) -> str:
    """Compute a SHA-256 hash of a dict for receipt chain."""
    serialized = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()[:16]


class LeadershipScorecardPipeline:
    """Orchestrates the complete FR7 Leadership Scorecard pipeline.

    Phases:
      1. INGEST — Load + verify signal sources, write INGEST receipt
      2. SCORE — 12-trait evaluation from signal sources
      3. CATEGORIZE — 5-category coverage evaluation
      4. FORMAT GOVERNANCE — Exercise/showcase assignment
      5. EMIT — Assemble and write leadership_scorecard.json
      6. VALIDATE — Validate all checks, enforce production lock, write COMPLETE receipt

    The Minister of Identity is READ-ONLY — it scores and annotates, never rewrites
    source DEP objects (AC10).
    """

    AGENT_ID = "minister_identity"  # C-11: internal routing ID only, never in API payloads

    def __init__(
        self,
        coach_dir: Path,
        coach_acronym: str,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        """Initialize the pipeline.

        Args:
            coach_dir: Root directory for this coach instance.
            coach_acronym: 3-letter coach acronym (e.g. "NDL").
            coach_id: Full coach person ID (e.g. "NDL-0000").
            receipt_chain: Optional ReceiptChain instance. If None, a new one is created.
        """
        self.coach_dir = coach_dir
        self.coach_acronym = coach_acronym.upper()
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=self.coach_acronym)

        self._loader = SignalSourceLoader(coach_dir)
        self._emitter = ScorecardEmitter(coach_dir)
        self._governance = FormatGovernanceEngine()

    def run(self) -> LeadershipScorecardPipelineSession:
        """Execute the complete FR7 pipeline from Phase 1 to Phase 6.

        Returns:
            LeadershipScorecardPipelineSession with final scorecard and receipt IDs.
        """
        session = LeadershipScorecardPipelineSession(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )

        try:
            # ── Phase 1: INGEST ──────────────────────────────────
            session.step_statuses["ingest"] = LeadershipPipelineStepStatus.RUNNING
            bundle = self._run_ingest()
            ingest_entry = self._write_ingest_receipt(bundle)
            session.ingest_receipt_id = ingest_entry.receipt_id
            session.step_statuses["ingest"] = LeadershipPipelineStepStatus.COMPLETED

            # ── Phase 2: SCORE ───────────────────────────────────
            session.step_statuses["score"] = LeadershipPipelineStepStatus.RUNNING
            scoring_engine = TraitScoringEngine(bundle)
            scored_traits = scoring_engine.score_all_traits()
            session.step_statuses["score"] = LeadershipPipelineStepStatus.COMPLETED

            # ── Phase 3: CATEGORIZE ──────────────────────────────
            session.step_statuses["categorize"] = LeadershipPipelineStepStatus.RUNNING
            cmm_layers, has_depth, has_tvr = self._extract_context_flags(bundle)
            evaluator = CategoryEvaluator(
                scored_traits=scored_traits,
                cmm_populated_layers=cmm_layers,
                has_l1_l2_l3_depth=has_depth,
                has_tvr_mode_coverage=has_tvr,
            )
            category_results = evaluator.evaluate_all_categories()
            production_lock = evaluator.evaluate_production_lock()
            session.step_statuses["categorize"] = LeadershipPipelineStepStatus.COMPLETED

            # ── Phase 4: FORMAT GOVERNANCE ───────────────────────
            session.step_statuses["format_governance"] = LeadershipPipelineStepStatus.RUNNING
            scored_traits = self._governance.apply_format_governance(scored_traits)
            session.step_statuses["format_governance"] = LeadershipPipelineStepStatus.COMPLETED

            # ── Phase 5: EMIT ────────────────────────────────────
            session.step_statuses["emit"] = LeadershipPipelineStepStatus.RUNNING
            scorecard = self._emitter.assemble_scorecard(
                coach_id=self.coach_id,
                scored_traits=scored_traits,
                category_results=category_results,
                production_lock_result=production_lock,
                signal_sources=bundle.source_availability,
            )
            session.step_statuses["emit"] = LeadershipPipelineStepStatus.COMPLETED

            # ── Phase 6: VALIDATE & EMIT ─────────────────────────
            session.step_statuses["validate"] = LeadershipPipelineStepStatus.RUNNING
            final_scorecard, validation_errors = self._emitter.emit(
                scorecard,
                raise_on_validation_failure=True,
            )

            # Write format governance to 02_content_strategy.md
            strategy_path = self.coach_dir / "config" / "02_content_strategy.md"
            self._governance.write_to_content_strategy(
                scored_traits=scored_traits,
                scorecard_id=f"DEP-ENG-026-{self.coach_acronym}",
                output_path=strategy_path,
            )

            # Update pipeline status in coach_soul.json (status field only — not DEP data)
            self._emitter.update_pipeline_status(scored=True)

            # Write COMPLETE receipt
            complete_entry = self._write_complete_receipt(
                final_scorecard,
                ingest_receipt_id=session.ingest_receipt_id or "",
            )
            session.complete_receipt_id = complete_entry.receipt_id
            session.step_statuses["validate"] = LeadershipPipelineStepStatus.COMPLETED
            session.scorecard = final_scorecard

        except MissingDependencyError as exc:
            # AC9: propagate as pipeline failure
            session.error = str(exc)
            for step in session.step_statuses:
                if session.step_statuses[step] == LeadershipPipelineStepStatus.RUNNING:
                    session.step_statuses[step] = LeadershipPipelineStepStatus.FAILED

        except ScorecardValidationError as exc:
            session.error = f"Scorecard validation failed: {exc.errors}"
            session.step_statuses["validate"] = LeadershipPipelineStepStatus.FAILED

        except Exception as exc:
            session.error = f"Pipeline error: {type(exc).__name__}: {exc}"
            for step in session.step_statuses:
                if session.step_statuses[step] == LeadershipPipelineStepStatus.RUNNING:
                    session.step_statuses[step] = LeadershipPipelineStepStatus.FAILED

        finally:
            session.completed_at = datetime.now(timezone.utc).isoformat()

        return session

    def _run_ingest(self) -> SignalBundle:
        """Phase 1: Load and verify all signal sources.

        Spec §Phase 1 INGEST — Steps 1-6.
        Raises MissingDependencyError (AC9) if required deps are absent.
        """
        return self._loader.load()

    def _write_ingest_receipt(self, bundle: SignalBundle) -> ReceiptEntry:
        """Write Phase 1 INGEST receipt per FR47 DEP-ENG-041 schema.

        Spec §Phase 1 — Receipt Write:
        stage_name: LEADERSHIP-SCORECARD-INGEST
        agent_name: Minister of Identity (internal id: minister_identity)
        """
        gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        asset_id = gen.generate(AssetType.LEADERSHIP_CARD)

        input_hash = _hash_dict({
            "coach_soul_loaded": bundle.source_availability.coach_soul,
            "ttt_baseline_loaded": bundle.source_availability.ttt_baseline,
            "tribe_soul_loaded": bundle.source_availability.tribe_soul,
        })

        source_summary = (
            f"Required: coach_soul={'✓' if bundle.source_availability.coach_soul else '✗'}, "
            f"ttt_baseline={'✓' if bundle.source_availability.ttt_baseline else '✗'}, "
            f"tribe_soul={'✓' if bundle.source_availability.tribe_soul else '✗'}. "
            f"Optional: cmm={'✓' if bundle.source_availability.cultural_memory_map else '✗'}, "
            f"stories={'✓' if bundle.source_availability.coach_story_archive else '✗'}, "
            f"philosophy={'✓' if bundle.source_availability.philosophy_brief else '✗'}"
        )

        return self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="LEADERSHIP-SCORECARD-INGEST",
            asset_id=asset_id,
            input_summary=source_summary,
            output_summary=f"Signal bundle loaded. 3 required + {sum([bundle.source_availability.cultural_memory_map, bundle.source_availability.coach_story_archive, bundle.source_availability.philosophy_brief])} optional sources.",
            decision="completed",
            metadata={
                "stage_name": "LEADERSHIP-SCORECARD-INGEST",
                "agent_name": "Minister of Identity",
                "dep_id": "DEP-ENG-026",
                "input_payload_hash": input_hash,
                "source_availability": bundle.source_availability.model_dump(),
            },
        )

    def _write_complete_receipt(
        self,
        scorecard: LeadershipScorecard,
        ingest_receipt_id: str,
    ) -> ReceiptEntry:
        """Write Phase 6 COMPLETE receipt per FR47 DEP-ENG-041 schema.

        Spec §Phase 6 — Receipt Write:
        stage_name: LEADERSHIP-SCORECARD-COMPLETE
        previous_receipt_hash: Phase 1 INGEST receipt ID
        """
        gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        asset_id = gen.generate(AssetType.LEADERSHIP_CARD)

        output_hash = _hash_dict({
            "trait_count": len(scorecard.traits),
            "all_categories_met": scorecard.production_lock.all_categories_met,
            "coach_id": scorecard.coach_id,
        })

        dominant = scorecard.dominant_trait()
        lock_status = "UNLOCKED" if scorecard.production_lock.all_categories_met else "LOCKED"

        return self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="LEADERSHIP-SCORECARD-COMPLETE",
            asset_id=asset_id,
            input_summary=f"Scored 12 traits. Production lock: {lock_status}.",
            output_summary=(
                f"DEP-ENG-026 emitted. "
                f"Dominant trait: {dominant.name.value if dominant else 'N/A'} "
                f"(score={dominant.score if dominant else 0}). "
                f"Production {'unlocked' if scorecard.production_lock.all_categories_met else 'LOCKED: ' + scorecard.production_lock.error_code}."
            ),
            decision="completed" if scorecard.production_lock.all_categories_met else "production_locked",
            parent_receipt_id=ingest_receipt_id,
            metadata={
                "stage_name": "LEADERSHIP-SCORECARD-COMPLETE",
                "agent_name": "Minister of Identity",
                "dep_id": "DEP-ENG-026",
                "output_payload_hash": output_hash,
                "previous_receipt_hash": ingest_receipt_id,
                "trait_count": len(scorecard.traits),
                "production_lock": scorecard.production_lock.model_dump(),
                "dominant_trait": dominant.name.value if dominant else None,
                "weak_traits": [t.name.value for t in scorecard.get_weak_traits()],
                "strong_traits": [t.name.value for t in scorecard.get_strong_traits()],
            },
        )

    def _extract_context_flags(
        self, bundle: SignalBundle
    ) -> tuple[int, bool, bool]:
        """Extract CMM layer count, L1/L2/L3 depth flag, and T/V/R mode flag from bundle.

        Returns:
            Tuple of (cmm_layers: int, has_l1_l2_l3_depth: bool, has_tvr_coverage: bool).
        """
        # CMM layer count
        cmm_layers = 0
        if bundle.cultural_memory_map_data:
            layers = bundle.cultural_memory_map_data.get("populated_layers", [])
            cmm_layers = len(layers) if isinstance(layers, list) else 0

        # L1/L2/L3 depth from tribe_soul
        depth_dist = bundle.tribe_soul_data.get("depth_distribution", {})
        l3_pct = depth_dist.get("l3_percentage", 0) if isinstance(depth_dist, dict) else 0
        l2_pct = depth_dist.get("l2_percentage", 0) if isinstance(depth_dist, dict) else 0
        has_depth = (l3_pct >= 10) or (l2_pct >= 30)

        # T/V/R mode coverage from tribe_soul
        mode_dist = bundle.tribe_soul_data.get("mode_distribution", {})
        modes_covered = sum(
            1 for mk in ["thought", "visceral", "reflective"]
            if isinstance(mode_dist, dict) and mode_dist.get(mk, 0) >= 3
        )
        has_tvr = modes_covered >= 3

        return cmm_layers, has_depth, has_tvr
