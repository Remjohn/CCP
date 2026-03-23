"""
CCP Step 5 — Voice DNA Adapter Pipeline Orchestrator (Unit 6)
Orchestrates all 4 Step-5 adapters in Mandate-4-compliant load order.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0
    FR3_Voice_DNA_Extraction_Tech_Spec.md §MANDATE 4 — Negative Space First

Load Order (hardcoded — not a prompt instruction):
    Step 1: NegativeSpaceLoaderAdapter  (Adapter-2) — DEP-ENG-004 → Block A [MUST RUN FIRST]
    Step 2: CoachSoulAdapter            (Adapter-1) — DEP-ENG-003 → Block A [requires Step 1]
    Step 3: IREVCAdapter                (Adapter-5) — DEP-LIB-002 + DEP-ENG-005 → Block A
    Step 4: PsychRoutingAdapter         (Adapter-4) — DEP-LIB-001 + DEP-ENG-016 → Block B

MANDATE 4 enforcement:
    The pipeline raises Mandate4GateError if NegativeSpaceLoaderAdapter fails (Gate PC-03)
    and immediately halts — CoachSoulAdapter is NEVER called in that case.
    This sequencing is enforced at the code level, not via prompts.

ADR-01: coach_id in VoiceDNAPipelineInput scopes all operations.
FR47:   Pipeline emits a top-level orchestration receipt after all adapters complete.
M-02:   No TTT hardcoded values in any adapter output. DEP-ENG-005 provides runtime only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import VoiceDNAAdapterPipelineResult
from src.ccp.models.psych_routing_models import PsychRoutingBrief
from src.ccp.models.ttt_models import TTTBaselineData
from src.ccp.models.trigger_map_models import TriggerMap
from src.ccp.models.voice_dna_models import (
    HumorStyleClassification,
    NegativeSpaceObject,
    PositiveSpaceObject,
)
from src.ccp.models.emotional_dna_models import EmotionalDNAProfile
from src.ccp.services.coach_soul_adapter import CoachSoulAdapter, Mandate4GateError
from src.ccp.services.irevc_adapter import IREVCAdapter
from src.ccp.services.negative_space_loader_adapter import (
    NegativeSpaceLoaderAdapter,
    NegativeSpaceDepthGateError,
)
from src.ccp.services.psych_routing_adapter import PsychRoutingAdapter


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_PIPELINE = "Voice-DNA-Adapter-Pipeline"
STAGE_ORCHESTRATE = "STEP5-ADAPTER-PIPELINE-ORCHESTRATE"


# ─── Pipeline Input ───────────────────────────────────────────────────────────

@dataclass
class VoiceDNAPipelineInput:
    """All inputs required for the Step 5 Voice DNA Adapter Pipeline.

    Required inputs (must be provided):
        coach_id:         ADR-01 tenant isolation identifier.
        negative_space:   DEP-ENG-004 — from NegativeSpaceExcavator (FR3 Step 5).
        positive_space:   DEP-ENG-003 — from PositiveSpaceExtractor (FR3 Steps 6-8).
        emotional_dna:    DEP-LIB-001 — from EmotionalDNAPipeline (FR4).
        trigger_map:      DEP-LIB-002 — from TriggerMapPipeline (FR5).

    Optional inputs:
        humor:            HumorStyleClassification — from FR3 Step 8.
                          If None, Block A will not include the humor style law.
        ttt_baseline:     DEP-ENG-005 — from TTTBaselineExtractor (FR8 Layer 3).
                          If None, IREVC adapter injects a TTT_ABSENT warning.
        routing_brief:    DEP-ENG-016 — from PsychRoutingPipeline (FR18).
                          If None, psych-routing-adapter injects emotional DNA only.
    """
    coach_id: str
    negative_space: NegativeSpaceObject
    positive_space: PositiveSpaceObject
    emotional_dna: EmotionalDNAProfile
    trigger_map: TriggerMap
    humor: Optional[HumorStyleClassification] = None
    ttt_baseline: Optional[TTTBaselineData] = None
    routing_brief: Optional[PsychRoutingBrief] = None


# ─── Pipeline ─────────────────────────────────────────────────────────────────

class VoiceDNAAdapterPipeline:
    """Orchestrates the full Step 5 adapter sequence for JIT SKILL.md compilation.

    Enforces Mandate 4 at the code level:
        - NegativeSpaceLoaderAdapter MUST complete before CoachSoulAdapter.
        - If Gate PC-03 fails (< 15 contrastive strings), the pipeline halts
          immediately. CoachSoulAdapter is never called in this case.

    All 4 adapters write individual receipts. The pipeline writes a top-level
    orchestration receipt on full success (all 4 adapters complete).

    ADR-01: coach_id in VoiceDNAPipelineInput scopes all adapter invocations.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain
        self._neg_space_adapter = NegativeSpaceLoaderAdapter(receipt_chain)
        self._coach_soul_adapter = CoachSoulAdapter(receipt_chain)
        self._irevc_adapter = IREVCAdapter(receipt_chain)
        self._psych_routing_adapter = PsychRoutingAdapter(receipt_chain)

    def run(self, inputs: VoiceDNAPipelineInput) -> VoiceDNAAdapterPipelineResult:
        """Execute all 4 Step 5 adapters in Mandate-4-compliant load order.

        Load order:
            1. negative-space-loader-adapter (DEP-ENG-004) — MUST succeed first
            2. coach-soul-adapter (DEP-ENG-003)            — requires step 1 success
            3. irevc-adapter (DEP-LIB-002 + DEP-ENG-005)
            4. psych-routing-adapter (DEP-LIB-001 + DEP-ENG-016)

        Args:
            inputs: VoiceDNAPipelineInput with all required DEP-IDs.

        Returns:
            VoiceDNAAdapterPipelineResult with all adapter results.
            If NegativeSpaceLoaderAdapter raises NegativeSpaceDepthGateError,
            the result has all_success=False and mandate_4_enforced=False.

        Raises:
            NegativeSpaceDepthGateError: Re-raised from Adapter-2 when Gate PC-03
                fails. Caller should trigger Guardian Agent micro-interview.
            Mandate4GateError: Should not occur — pipeline sets the flag correctly.
                If raised, indicates a pipeline logic bug.
        """
        result = VoiceDNAAdapterPipelineResult(
            coach_id=inputs.coach_id,
            all_success=False,
            mandate_4_enforced=False,
        )

        # ── Step 1: Negative Space Loader (Adapter-2) — MUST RUN FIRST ────────
        # Mandate 4: this step hardcodes the load order. PC-03 gate enforced here.
        # NegativeSpaceDepthGateError is intentionally NOT caught — caller handles it.
        neg_result = self._neg_space_adapter.load(
            negative_space=inputs.negative_space,
            coach_id=inputs.coach_id,
        )
        result.negative_space_result = neg_result

        if not neg_result.success:
            # Adapter returned failure without raising — propagate as pipeline failure
            return result

        # Mandate 4 confirmed: negative space completed successfully
        result.mandate_4_enforced = True

        # ── Step 2: Coach Soul Adapter (Adapter-1) — DEP-ENG-004 confirmed ────
        # negative_space_complete=True because Adapter-2 just succeeded.
        coach_result = self._coach_soul_adapter.load(
            positive_space=inputs.positive_space,
            coach_id=inputs.coach_id,
            negative_space_complete=True,  # Mandate 4 gate — set by pipeline after Step 1
            humor=inputs.humor,
        )
        result.coach_soul_result = coach_result

        # ── Step 3: IREVC Adapter (Adapter-5) ─────────────────────────────────
        irevc_result = self._irevc_adapter.load(
            trigger_map=inputs.trigger_map,
            coach_id=inputs.coach_id,
            ttt_baseline=inputs.ttt_baseline,
        )
        result.irevc_result = irevc_result

        # ── Step 4: Psych Routing Adapter (Adapter-4) ─────────────────────────
        psych_result = self._psych_routing_adapter.load(
            emotional_dna=inputs.emotional_dna,
            coach_id=inputs.coach_id,
            routing_brief=inputs.routing_brief,
        )
        result.psych_routing_result = psych_result

        # ── Determine all_success ──────────────────────────────────────────────
        all_success = all([
            neg_result.success,
            coach_result.success,
            irevc_result.success,
            psych_result.success,
        ])
        result.all_success = all_success

        # ── Pipeline orchestration receipt ────────────────────────────────────
        block_a_count = len(result.get_all_block_a_injections())
        block_b_count = len(result.get_all_block_b_injections())
        total_warnings = sum([
            len(neg_result.warnings),
            len(coach_result.warnings),
            len(irevc_result.warnings),
            len(psych_result.warnings),
        ])

        entry = self._rc.log(
            agent_id=AGENT_PIPELINE,
            action=STAGE_ORCHESTRATE,
            input_summary=(
                f"coach_id={inputs.coach_id} "
                f"has_ttt={'yes' if inputs.ttt_baseline else 'no'} "
                f"has_routing_brief={'yes' if inputs.routing_brief else 'no'} "
                f"has_humor={'yes' if inputs.humor else 'no'}"
            ),
            output_summary=(
                f"all_success={all_success} "
                f"mandate_4_enforced={result.mandate_4_enforced} "
                f"block_a_sections={block_a_count} "
                f"block_b_sections={block_b_count} "
                f"total_warnings={total_warnings}"
            ),
            metadata={
                "stage_name": STAGE_ORCHESTRATE,
                "coach_id": inputs.coach_id,
                "all_success": all_success,
                "mandate_4_enforced": result.mandate_4_enforced,
                "adapters_run": [
                    "negative-space-loader-adapter",
                    "coach-soul-adapter",
                    "irevc-adapter",
                    "psych-routing-adapter",
                ],
                "adapter_receipts": {
                    "negative_space": neg_result.receipt_id,
                    "coach_soul": coach_result.receipt_id,
                    "irevc": irevc_result.receipt_id,
                    "psych_routing": psych_result.receipt_id,
                },
                "block_a_injection_count": block_a_count,
                "block_b_injection_count": block_b_count,
                "total_warnings": total_warnings,
            },
        )
        result.pipeline_receipt_id = entry.receipt_id

        return result

    def format_full_skill_md_injection(
        self,
        inputs: VoiceDNAPipelineInput,
    ) -> dict[str, str]:
        """Run the full pipeline and return formatted SKILL.md section texts.

        Returns:
            Dict with keys 'block_a' and 'block_b' containing the assembled
            section text for SKILL.md injection.

        Raises:
            NegativeSpaceDepthGateError: If Gate PC-03 fails. Caller handles.
        """
        pipeline_result = self.run(inputs)

        block_a_text = ""
        for injection in pipeline_result.get_all_block_a_injections():
            block_a_text += injection.to_block_a_text()

        block_b_text = ""
        for injection in pipeline_result.get_all_block_b_injections():
            block_b_text += injection.to_block_b_text()

        return {
            "block_a": block_a_text,
            "block_b": block_b_text,
        }
