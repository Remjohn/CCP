"""
CCP FR6 — Tribe Profile Pipeline Orchestrator (Unit 11)
Full two-stage pipeline: Stage A (Tribe Soul Extraction) → Stage B
(Context Premise Distillation + Neo4j Graph Persistence).

Spec reference: FR6 Tech Spec
  §Stage A — Tribe Soul Extraction (Genesis Setup)
  §Stage B — Context Premise Distillation & Neo4j Graph Persistence
  §Backward Compatibility — Legacy Fallback (AC13)

Pipeline receipt chain writes (4 total):
  1. TRIBE-EXTRACT-INGEST  (Stage A, Phase A1)
  2. TRIBE-EXTRACT-EMIT    (Stage A, Phase A4)
  3. TRIBE-DISTILL-INGEST  (Stage B, Phase B1)
  4. TRIBE-DISTILL-EMIT    (Stage B, Phase B8)

Post-pipeline actions:
  - Update coach_soul.json with tribe_profile_ref + context_premise_ref
  - Update config.yaml status to mark FR6 complete
  - ADR-01: Per-coach isolation enforced at every layer
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul
from src.ccp.models.tribe_profile_models import (
    AuthenticationVerdict,
    ContextPremiseFallbackResult,
    TribeProfile,
    TribeProfileDistilled,
    TribeProfilePipelineSession,
    TribeProfilePipelineStepStatus,
)
from src.ccp.models.tribe_research_models import TribeDossier
from src.ccp.services.context_premise_fallback import ContextPremiseFallback
from src.ccp.services.tribe_profile_distiller import TribeProfileDistiller
from src.ccp.services.tribe_profile_extractor import TribeProfileExtractor

logger = logging.getLogger(__name__)


class TribeProfilePipelineError(Exception):
    """Top-level pipeline error for FR6."""
    pass


class TribeProfilePipeline:
    """Orchestrates the complete FR6 Tribe Profile & Context Premise pipeline.

    This is the main entry point for FR6 execution. It runs both stages
    in sequence, enforces quality gates, writes 4 receipt chain entries,
    and updates coach_soul.json on completion.

    Two-stage architecture:
      Stage A: Tribe Soul Extraction → tribe_profile.json
      Stage B: Context Premise Distillation → tribe_profile_distilled.json + Neo4j

    AC13: When Context Premise Map does not exist, pipeline falls back
    to topic-based prompts from coach_soul.json. All downstream phases
    complete without error.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Optional[Path] = None,
        base_dir: str = "./coaches",
        receipt_chain: Optional[ReceiptChain] = None,
        neo4j_driver: Any = None,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.base_dir = Path(base_dir)
        self.coach_dir = coach_dir or (self.base_dir / self.coach_acronym)
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )

        # Initialize stage-level orchestrators
        self.extractor = TribeProfileExtractor(
            coach_id=coach_id,
            coach_acronym=coach_acronym,
            receipt_chain=self.receipt_chain,
            base_dir=base_dir,
        )
        self.distiller = TribeProfileDistiller(
            coach_id=coach_id,
            coach_acronym=coach_acronym,
            receipt_chain=self.receipt_chain,
            base_dir=base_dir,
            neo4j_driver=neo4j_driver,
        )

    # ══════════════════════════════════════════════════════════════
    # MAIN ENTRY POINT
    # ══════════════════════════════════════════════════════════════

    def execute(
        self,
        tribe_dossier: Optional[TribeDossier] = None,
        audience_raw_data: Optional[list[dict[str, Any]]] = None,
        coach_soul: Optional[CoachSoul] = None,
        coach_soul_dict: Optional[dict[str, Any]] = None,
        coach_philosophy_brief: Optional[str] = None,
        tshala_sentiment_report: Optional[dict[str, Any]] = None,
        engagement_data: Optional[dict[str, float]] = None,
        parent_receipt_id: Optional[str] = None,
    ) -> TribeProfilePipelineSession:
        """Execute the complete FR6 two-stage pipeline.

        Args:
            tribe_dossier: H11 Tribe Dossier from FR0B.
            audience_raw_data: Raw audience research data.
            coach_soul: Parsed CoachSoul model (used for fallback seeds).
            coach_soul_dict: Raw coach_soul dict (passed to sub-services).
            coach_philosophy_brief: Coach philosophy text.
            tshala_sentiment_report: Optional Tshala report.
            engagement_data: Optional engagement metrics for reconsolidation.
            parent_receipt_id: Receipt ID from upstream (chain link).

        Returns:
            TribeProfilePipelineSession with all step statuses and receipt IDs.

        Raises:
            TribeProfilePipelineError: On unrecoverable pipeline failure.
        """
        session = TribeProfilePipelineSession(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )

        # Prepare coach_soul dict for sub-services
        cs_dict = coach_soul_dict
        if cs_dict is None and coach_soul is not None:
            cs_dict = coach_soul.model_dump()

        try:
            # ── STAGE A: Tribe Soul Extraction ──
            self._execute_stage_a(
                session=session,
                tribe_dossier=tribe_dossier,
                audience_raw_data=audience_raw_data,
                coach_soul_dict=cs_dict,
                coach_philosophy_brief=coach_philosophy_brief,
                tshala_sentiment_report=tshala_sentiment_report,
            )

            # ── STAGE B: Context Premise Distillation ──
            self._execute_stage_b(
                session=session,
                coach_soul_dict=cs_dict,
                coach_philosophy_brief=coach_philosophy_brief,
                engagement_data=engagement_data,
            )

            # ── POST-PIPELINE: Coach Soul update + config ──
            self._post_pipeline_update(
                session=session,
                coach_soul=coach_soul,
            )

            session.completed_at = datetime.now(timezone.utc).isoformat()

        except TribeProfilePipelineError:
            raise
        except Exception as e:
            logger.error("FR6 pipeline failed: %s", e, exc_info=True)
            raise TribeProfilePipelineError(
                f"FR6 pipeline failed: {e}"
            ) from e

        return session

    # ══════════════════════════════════════════════════════════════
    # STAGE A: Tribe Soul Extraction
    # ══════════════════════════════════════════════════════════════

    def _execute_stage_a(
        self,
        session: TribeProfilePipelineSession,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: Optional[list[dict[str, Any]]],
        coach_soul_dict: Optional[dict[str, Any]],
        coach_philosophy_brief: Optional[str],
        tshala_sentiment_report: Optional[dict[str, Any]],
    ) -> None:
        """Run Stage A: Phases A1–A6.

        Updates session in-place with step statuses and receipt IDs.
        Populates session.tribe_profile_path on success.
        """
        session.stage_a_ingest = TribeProfilePipelineStepStatus.IN_PROGRESS

        try:
            profile, emit_receipt_id, quota_results = (
                self.extractor.run_stage_a(
                    tribe_dossier=tribe_dossier,
                    audience_raw_data=audience_raw_data,
                    coach_soul=coach_soul_dict,
                    coach_philosophy_brief=coach_philosophy_brief,
                    tshala_sentiment_report=tshala_sentiment_report,
                )
            )

            # Collect receipt IDs from the extractor
            # Stage A writes TRIBE-EXTRACT-INGEST and TRIBE-EXTRACT-EMIT
            # The emit receipt ID is returned directly; ingest is internal
            session.receipt_tribe_emit = emit_receipt_id
            # Ingest receipt is not directly returned — record empty
            # (traceable through receipt chain log files)
            session.receipt_tribe_ingest = ""

            # Mark all Stage A steps complete
            session.stage_a_ingest = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_a_research_planning = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_a_cultural_harvesting = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_a_emit = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_a_validate = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_a_checkpoint = TribeProfilePipelineStepStatus.COMPLETE

            # Store output path
            intelligence_dir = self.coach_dir / "intelligence" / "tribe"
            session.tribe_profile_path = str(
                intelligence_dir / "tribe_profile.json"
            )

            # Store profile for Stage B consumption
            self._stage_a_profile = profile
            self._stage_a_quotas = quota_results

            logger.info(
                "Stage A complete for coach %s. "
                "tribe_profile.json written. Quotas: %d checks.",
                self.coach_acronym,
                len(quota_results),
            )

        except ValueError as e:
            session.stage_a_ingest = TribeProfilePipelineStepStatus.FAILED
            raise TribeProfilePipelineError(
                f"Stage A failed at INGEST: {e}"
            ) from e
        except Exception as e:
            # Mark whatever stage was running as failed
            for step in ["ingest", "research_planning", "cultural_harvesting",
                         "emit", "validate", "checkpoint"]:
                attr = f"stage_a_{step}"
                if getattr(session, attr) == TribeProfilePipelineStepStatus.IN_PROGRESS:
                    setattr(session, attr, TribeProfilePipelineStepStatus.FAILED)
            raise TribeProfilePipelineError(
                f"Stage A failed: {e}"
            ) from e

    # ══════════════════════════════════════════════════════════════
    # STAGE B: Context Premise Distillation
    # ══════════════════════════════════════════════════════════════

    def _execute_stage_b(
        self,
        session: TribeProfilePipelineSession,
        coach_soul_dict: Optional[dict[str, Any]],
        coach_philosophy_brief: Optional[str],
        engagement_data: Optional[dict[str, float]],
    ) -> None:
        """Run Stage B: Phases B1–B10.

        Requires Stage A to have completed (tribe_profile available).
        Updates session in-place with step statuses and receipt IDs.
        """
        session.stage_b_ingest = TribeProfilePipelineStepStatus.IN_PROGRESS

        # Get tribe_profile from Stage A
        tribe_profile = getattr(self, "_stage_a_profile", None)
        if tribe_profile is None:
            session.stage_b_ingest = TribeProfilePipelineStepStatus.FAILED
            raise TribeProfilePipelineError(
                "Stage B cannot start: Stage A did not produce a TribeProfile. "
                "Run Stage A first."
            )

        try:
            distilled, emit_receipt_id = self.distiller.run_stage_b(
                tribe_profile=tribe_profile,
                coach_soul=coach_soul_dict,
                coach_philosophy_brief=coach_philosophy_brief,
                stage_a_receipt_id=session.receipt_tribe_emit,
                engagement_data=engagement_data,
            )

            # Collect receipt IDs from the distiller
            # Stage B writes TRIBE-DISTILL-INGEST and TRIBE-DISTILL-EMIT
            # The emit receipt ID is returned directly; ingest is internal
            session.receipt_distill_emit = emit_receipt_id
            session.receipt_distill_ingest = ""

            # Mark all Stage B steps complete
            session.stage_b_ingest = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_depth_stratification = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_mode_mapping = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_visual_language = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_resonance = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_psychometric = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_neo4j = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_emit = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_validate = TribeProfilePipelineStepStatus.COMPLETE
            session.stage_b_checkpoint = TribeProfilePipelineStepStatus.COMPLETE

            # Store output path
            intelligence_dir = self.coach_dir / "intelligence" / "tribe"
            session.tribe_profile_distilled_path = str(
                intelligence_dir / "tribe_profile_distilled.json"
            )

            # Store distilled profile for post-pipeline actions
            self._stage_b_distilled = distilled

            logger.info(
                "Stage B complete for coach %s. "
                "Authentication: %s.",
                self.coach_acronym,
                distilled.authentication_status.value
                if distilled.authentication_status
                else "NONE",
            )

        except ValueError as e:
            session.stage_b_ingest = TribeProfilePipelineStepStatus.FAILED
            raise TribeProfilePipelineError(
                f"Stage B failed at INGEST: {e}"
            ) from e
        except Exception as e:
            for step in ["ingest", "depth_stratification", "mode_mapping",
                         "visual_language", "resonance", "psychometric",
                         "neo4j", "emit", "validate", "checkpoint"]:
                attr = f"stage_b_{step}"
                if getattr(session, attr) == TribeProfilePipelineStepStatus.IN_PROGRESS:
                    setattr(session, attr, TribeProfilePipelineStepStatus.FAILED)
            raise TribeProfilePipelineError(
                f"Stage B failed: {e}"
            ) from e

    # ══════════════════════════════════════════════════════════════
    # POST-PIPELINE: Coach Soul Update + Config
    # ══════════════════════════════════════════════════════════════

    def _post_pipeline_update(
        self,
        session: TribeProfilePipelineSession,
        coach_soul: Optional[CoachSoul],
    ) -> None:
        """Update coach_soul.json with tribe profile references
        and update config.yaml status.

        Spec §Phase B10 CHECKPOINT:
          - Update coach_soul.json with tribe_profile_ref, context_premise_ref
          - Update config.yaml status
        """
        coach_soul_path = self.coach_dir / "coach_soul.json"

        # Update coach_soul.json with references
        if coach_soul_path.exists():
            try:
                cs_data = json.loads(
                    coach_soul_path.read_text(encoding="utf-8")
                )
                cs_data["tribe_profile_ref"] = session.tribe_profile_path
                cs_data["context_premise_ref"] = (
                    session.tribe_profile_distilled_path
                )
                cs_data["updated_at"] = datetime.now(timezone.utc).isoformat()

                # Bump version if present
                if "version" in cs_data:
                    cs_data["version"] = cs_data.get("version", 0) + 1

                coach_soul_path.write_text(
                    json.dumps(cs_data, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                logger.info(
                    "Updated coach_soul.json with tribe_profile_ref and "
                    "context_premise_ref for coach %s",
                    self.coach_acronym,
                )
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(
                    "Could not update coach_soul.json: %s", e
                )

        # Update config.yaml status (mark FR6 complete)
        self._update_config_status(session)

    def _update_config_status(
        self,
        session: TribeProfilePipelineSession,
    ) -> None:
        """Update config.yaml to mark FR6 pipeline status."""
        config_path = self.coach_dir / "config.yaml"

        status_data = {
            "fr6_tribe_profile": {
                "status": "complete" if session.is_complete() else "partial",
                "stage_a_complete": session.is_stage_a_complete(),
                "stage_b_complete": session.is_stage_b_complete(),
                "tribe_profile_path": session.tribe_profile_path,
                "distilled_profile_path": session.tribe_profile_distilled_path,
                "receipt_tribe_ingest": session.receipt_tribe_ingest,
                "receipt_tribe_emit": session.receipt_tribe_emit,
                "receipt_distill_ingest": session.receipt_distill_ingest,
                "receipt_distill_emit": session.receipt_distill_emit,
                "completed_at": session.completed_at or "",
            },
        }

        try:
            # Write as JSON sidecar since full YAML support is optional
            status_path = self.coach_dir / "fr6_status.json"
            status_path.write_text(
                json.dumps(status_data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            logger.info(
                "FR6 status written to %s for coach %s",
                status_path,
                self.coach_acronym,
            )
        except OSError as e:
            logger.warning("Could not write FR6 status: %s", e)

    # ══════════════════════════════════════════════════════════════
    # FALLBACK EXECUTION (AC13)
    # ══════════════════════════════════════════════════════════════

    def execute_with_fallback(
        self,
        tribe_dossier: Optional[TribeDossier] = None,
        audience_raw_data: Optional[list[dict[str, Any]]] = None,
        coach_soul: Optional[CoachSoul] = None,
        coach_soul_dict: Optional[dict[str, Any]] = None,
        coach_philosophy_brief: Optional[str] = None,
        tshala_sentiment_report: Optional[dict[str, Any]] = None,
        engagement_data: Optional[dict[str, float]] = None,
        parent_receipt_id: Optional[str] = None,
    ) -> tuple[TribeProfilePipelineSession, Optional[ContextPremiseFallbackResult]]:
        """Execute pipeline with AC13 fallback check.

        If audience data is missing and cannot run full pipeline,
        generates fallback seeds from coach_soul.json instead.

        Returns:
            Tuple of (session, fallback_result).
            fallback_result is None if full pipeline executed.
        """
        # Check if we have enough data for full pipeline
        has_dossier = tribe_dossier is not None
        has_raw = audience_raw_data is not None and len(audience_raw_data) > 0

        if not has_dossier and not has_raw:
            # AC13: No audience data → fallback path
            if coach_soul is None:
                raise TribeProfilePipelineError(
                    "AC13 fallback requires coach_soul. Neither audience "
                    "data nor coach_soul provided."
                )

            logger.warning(
                "AC13 FALLBACK: No audience data for coach %s. "
                "Generating topic-based fallback seeds from coach_soul.",
                self.coach_acronym,
            )

            fallback_result = ContextPremiseFallback.resolve(
                coach_soul=coach_soul,
                coach_folder=self.coach_dir,
            )

            # Create a minimal session with fallback status
            session = TribeProfilePipelineSession(
                coach_id=self.coach_id,
                coach_acronym=self.coach_acronym,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )
            # Mark all steps as SKIPPED in fallback mode
            for step in ["ingest", "research_planning", "cultural_harvesting",
                         "emit", "validate", "checkpoint"]:
                setattr(
                    session,
                    f"stage_a_{step}",
                    TribeProfilePipelineStepStatus.SKIPPED,
                )
            for step in ["ingest", "depth_stratification", "mode_mapping",
                         "visual_language", "resonance", "psychometric",
                         "neo4j", "emit", "validate", "checkpoint"]:
                setattr(
                    session,
                    f"stage_b_{step}",
                    TribeProfilePipelineStepStatus.SKIPPED,
                )

            # Write fallback result to disk
            self._write_fallback_result(fallback_result)

            return session, fallback_result

        # Normal execution path
        session = self.execute(
            tribe_dossier=tribe_dossier,
            audience_raw_data=audience_raw_data,
            coach_soul=coach_soul,
            coach_soul_dict=coach_soul_dict,
            coach_philosophy_brief=coach_philosophy_brief,
            tshala_sentiment_report=tshala_sentiment_report,
            engagement_data=engagement_data,
            parent_receipt_id=parent_receipt_id,
        )
        return session, None

    def _write_fallback_result(
        self,
        fallback_result: Optional[ContextPremiseFallbackResult],
    ) -> None:
        """Persist the fallback result to disk for downstream consumers."""
        if fallback_result is None:
            return

        fallback_path = (
            self.coach_dir / "intelligence" / "tribe" / "fallback_status.json"
        )
        fallback_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            fallback_path.write_text(
                json.dumps(
                    fallback_result.model_dump(),
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            logger.info(
                "Fallback status written to %s", fallback_path
            )
        except OSError as e:
            logger.warning("Could not write fallback status: %s", e)

    # ══════════════════════════════════════════════════════════════
    # QUERY INTERFACE
    # ══════════════════════════════════════════════════════════════

    def get_pipeline_summary(self) -> dict[str, Any]:
        """Return a summary of the pipeline state for diagnostics."""
        distilled = getattr(self, "_stage_b_distilled", None)
        profile = getattr(self, "_stage_a_profile", None)

        summary: dict[str, Any] = {
            "coach_id": self.coach_id,
            "coach_acronym": self.coach_acronym,
            "stage_a_complete": profile is not None,
            "stage_b_complete": distilled is not None,
        }

        if distilled is not None:
            summary["authentication_status"] = (
                distilled.authentication_status.value
                if distilled.authentication_status
                else None
            )
            summary["four_laws_passed"] = (
                distilled.four_laws_validation is not None
                and distilled.four_laws_validation.all_passed()
            )

        return summary
