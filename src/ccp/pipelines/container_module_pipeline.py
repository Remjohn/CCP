"""
CCP Step 6 — Container Module Pipeline Orchestrator

Orchestrates the full Step 6 pipeline:
  FR9 (Audience Empathy Agent) → FR10 (Four-Axis Matching Engine) →
  FR11 (Activation Seed Builder) → FR12 (Failure Prevention Gates)

Receipt chain threading maintained across all stages.
Fallback logic: 3 consecutive Gate 2 failures → system_fallback_invoked.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.container_module_models import (
    ContainerModulePipelineConfig,
    ContainerModulePipelineResult,
    GateDiagnosticCertificate,
)
from src.ccp.services.activation_seed_builder import ActivationSeedBuilder
from src.ccp.services.audience_empathy_agent import AudienceEmpathyAgent
from src.ccp.services.failure_prevention_gates import FailurePreventionGates
from src.ccp.services.four_axis_matching_engine import FourAxisMatchingEngine

logger = logging.getLogger(__name__)


class ContainerModulePipeline:
    """Step 6 Pipeline Orchestrator.

    Runs FR9 → FR10 → FR11 → FR12 in sequence for a given theme,
    threading receipt chain IDs across all stages.
    """

    PIPELINE_AGENT_ID = "container_module_pipeline_v1"

    def __init__(
        self,
        config: ContainerModulePipelineConfig,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.config = config
        self.config.compute_theme_slug()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.config.coach_acronym
        )

        # Initialize sub-agents with shared receipt chain
        self.audience_empathy = AudienceEmpathyAgent(
            coach_acronym=self.config.coach_acronym,
            receipt_chain=self.receipt_chain,
        )
        self.matching_engine = FourAxisMatchingEngine(
            coach_acronym=self.config.coach_acronym,
            receipt_chain=self.receipt_chain,
        )
        self.seed_builder = ActivationSeedBuilder(
            coach_acronym=self.config.coach_acronym,
            receipt_chain=self.receipt_chain,
        )
        self.gates = FailurePreventionGates(
            coach_acronym=self.config.coach_acronym,
            receipt_chain=self.receipt_chain,
        )

    def run(
        self,
        context_premise_map: Optional[dict[str, Any]],
        segments_data: list[dict[str, Any]],
        extraction_data: dict[str, dict[str, list[dict[str, Any]]]],
        tribal_language_data: Optional[dict[str, Any]],
        emotional_dna: Optional[dict[str, Any]],
        trigger_map: Optional[dict[str, Any]],
        coach_soul: Optional[dict[str, Any]] = None,
        output_dir: Optional[Path] = None,
    ) -> ContainerModulePipelineResult:
        """Execute the full Step 6 pipeline.

        Args:
            context_premise_map: DEP-ENG-006 standing audience intelligence.
            segments_data: 6 segment definitions for FR9.
            extraction_data: 6×12 insight extraction data for FR9.
            tribal_language_data: In-group/rejection terms for FR9.
            emotional_dna: DEP-LIB-001 for FR10.
            trigger_map: DEP-LIB-002 for FR10/FR11.
            coach_soul: Optional coach soul document.
            output_dir: Optional output directory.

        Returns:
            ContainerModulePipelineResult with all outputs.
        """
        result = ContainerModulePipelineResult(
            config=self.config,
            pipeline_status="RUNNING",
        )

        try:
            # ── FR9: Audience Empathy Agent ──
            logger.info(
                "Step 6 Pipeline [1/4]: FR9 Audience Empathy Agent — theme=%s",
                self.config.theme,
            )
            context_premise = self.audience_empathy.run(
                theme=self.config.theme,
                context_premise_map=context_premise_map,
                segments_data=segments_data,
                extraction_data=extraction_data,
                tribal_language_data=tribal_language_data,
                coach_soul=coach_soul,
                output_dir=output_dir,
            )
            result.context_premise = context_premise

            # ── FR10: Four-Axis Matching Engine ──
            logger.info(
                "Step 6 Pipeline [2/4]: FR10 Four-Axis Matching Engine — theme=%s",
                self.config.theme,
            )
            match_results = self.matching_engine.run(
                emotional_dna=emotional_dna,
                trigger_map=trigger_map,
                context_premise=context_premise,
            )
            result.match_results = match_results

            # ── FR11: Activation Seed Builder ──
            logger.info(
                "Step 6 Pipeline [3/4]: FR11 Activation Seed Builder — theme=%s",
                self.config.theme,
            )
            activation_seeds = self.seed_builder.run(
                match_results=match_results,
                trigger_map=trigger_map,
                context_premise=context_premise,
            )
            result.activation_seeds = activation_seeds

            # ── FR12: Failure Prevention Gates (Stages 1–4) ──
            logger.info(
                "Step 6 Pipeline [4/4]: FR12 Failure Prevention Gates — theme=%s",
                self.config.theme,
            )
            certificates = self.gates.run(
                match_results=match_results,
                activation_seeds=activation_seeds,
            )
            result.gate_certificates = certificates

            # Check fallback
            if (
                self.gates.gate_2_consecutive_failures
                >= FailurePreventionGates.GATE_2_CONSECUTIVE_FAILURE_LIMIT
            ):
                result.fallback_invoked = True

            result.pipeline_status = "COMPLETE"
            logger.info(
                "Step 6 Pipeline COMPLETE: theme=%s, seeds=%d, certificates=%d, "
                "fallback=%s",
                self.config.theme,
                len(activation_seeds.seeds),
                len(certificates),
                result.fallback_invoked,
            )

        except ValueError as e:
            result.pipeline_status = "HALTED"
            result.errors.append(str(e))
            logger.error("Step 6 Pipeline HALTED: %s", e)

        except Exception as e:
            result.pipeline_status = "ERROR"
            result.errors.append(str(e))
            logger.exception("Step 6 Pipeline ERROR: %s", e)

        return result
