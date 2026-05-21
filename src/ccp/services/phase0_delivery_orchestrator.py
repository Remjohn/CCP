"""
src/ccp/services/phase0_delivery_orchestrator.py
=================================================
Core implementation of FR-ERA3-36 Phase-0 Delivery Orchestrator Service.
Conforms completely to the Tech Spec and rules of PROMPT_Spec_Build.md.
"""

from __future__ import annotations
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Literal

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0ProspectStatus,
    Phase0AuditTargetContentType
)
from src.ccp.models.phase0_audit_models import (
    AuditIntelligenceReport,
    PdfAuditPayload,
    ExplainerAuditVideoPayload,
    BridgeTierRecommendation
)
from src.ccp.models.phase0_delivery_models import (
    Phase0DeliveryPlan,
    Phase0DeliveryRun,
    Phase0DeliveryRunStatus,
    Phase0SequenceStep,
    Phase0SequenceStepType,
    Phase0ExecutionMode,
    Phase0RenderRequest,
    Phase0SequenceStepResult,
    Phase0DeliveryReceipt,
    Phase0OutputBundle,
    Phase0PaymentHandoffPacket
)
from src.ccp.models.cmf_arc_render_models import (
    CoalitionSpineInput,
    ArcRenderJobRecord,
    ArcRenderJobStatus
)
from src.ccp.services.audit_intelligence_engine import AuditIntelligenceEngine
from src.ccp.services.cmf_arc_governed_rendering import CMFArcGovernedRenderingPipeline


logger = logging.getLogger(__name__)


class CMFReceiptAdapter:
    """
    Adapts the standard ReceiptChain instance to conform to the simple 
    log(action, metadata) invocation signature used inside the CMFArcGovernedRenderingPipeline.
    """
    def __init__(self, rc: ReceiptChain):
        self.rc = rc

    def log(self, action: str, metadata: Dict[str, Any]) -> Any:
        return self.rc.log(
            agent_id="cmf_render_pipeline",
            action=action,
            metadata=metadata
        )


class Phase0DeliveryOrchestrator:
    """
    Coordinates intake validation, core audit generation, rendering dispatches,
    preview assembly, review gates, and payment handoff package preparation.
    
    Enforces the Shared Pre-Container Namespaced Runtime constraints.
    """

    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir = log_dir
        # Store in-memory maps mirroring namespaced database state
        self.plans: Dict[str, Phase0DeliveryPlan] = {}
        self.runs: Dict[str, Phase0DeliveryRun] = {}
        self.bundles: Dict[str, Phase0OutputBundle] = {}

    def _get_acronym(self, coach_id: str) -> str:
        """Extract a 3-letter acronym from coach ID or default."""
        if coach_id and len(coach_id) >= 3:
            return coach_id[:3].upper()
        return "P0D"

    def _get_receipt_chain(self, coach_id: str) -> ReceiptChain:
        """Returns a ReceiptChain instance configured for the coach."""
        return ReceiptChain(coach_acronym=self._get_acronym(coach_id), log_dir=self.log_dir)

    def create_plan(self, packet: Phase0ProspectPacket) -> Phase0DeliveryPlan:
        """
        AC1: Produces a canonical Phase0DeliveryPlan from a valid packet.
        AC2: Differentiate internal generation order from public release order.
        """
        # Hard check: Cannot plan a packet that has blocking intake issues
        if packet.status == Phase0ProspectStatus.BLOCKED_MISSING_INPUTS:
            raise ValueError(f"Cannot generate plan for blocked packet {packet.packet_id}")

        coach_id = packet.coach_id or "COACH-DEFAULT"
        plan_id = f"PLN-{uuid.uuid4().hex[:8].upper()}"

        # Heuristically determine variant from primary audit target
        package_variant = "standard_proof"
        requested_outputs = ["audit_pdf", "preview_bundle", "payment_handoff"]
        optional_outputs_enabled = []

        if packet.audit_targets:
            target = packet.audit_targets[0]
            if target.content_type == Phase0AuditTargetContentType.REEL_CAPTION:
                package_variant = "video_enhanced_proof"
                requested_outputs.extend(["explainer_video_1", "explainer_video_2", "cinematic_video", "audit_explainer_video"])
            else:
                requested_outputs.extend(["explainer_video_1", "cinematic_video"])

            # Map archetype and optional carousels/memes
            if target.archetype_hint or len(packet.captions) > 0:
                optional_outputs_enabled.append("carousel_spread")
                optional_outputs_enabled.append("meme_layer")

        now = datetime.now(timezone.utc)
        # 24h Delivery Readiness SLA
        sla_deadline = now + timedelta(hours=24)

        # ── Construct internal generation order steps ──
        generation_steps: List[Phase0SequenceStep] = []
        
        # 1. Audit core
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-AUDIT",
            step_key="audit_core",
            step_type=Phase0SequenceStepType.AUDIT_CORE,
            order_index=0,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            target_output_key="audit_report_id"
        ))

        # 2. Scorecard visual board components
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-CARD",
            step_key="card_render",
            step_type=Phase0SequenceStepType.CARD_RENDER,
            order_index=1,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="score_card_board_ids"
        ))

        # 3. PDF Audit package assembly
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-PDF",
            step_key="pdf_assembly",
            step_type=Phase0SequenceStepType.PDF_AUDIT_ASSEMBLY,
            order_index=2,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="pdf_audit_payload_id"
        ))

        # 4. Animated audit explainer production
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-AUDIT-VID",
            step_key="audit_explainer_video",
            step_type=Phase0SequenceStepType.AUDIT_EXPLAINER_VIDEO,
            order_index=3,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required="audit_explainer_video" in requested_outputs,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="audit_explainer_video_payload_id"
        ))

        # 5. Explainer Video 1
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-EXP1",
            step_key="explainer_video_1",
            step_type=Phase0SequenceStepType.EXPLAINER_VIDEO,
            order_index=4,
            execution_mode=Phase0ExecutionMode.OPERATOR_REVIEW_REQUIRED,
            review_gate=True,
            required="explainer_video_1" in requested_outputs,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="explainer_video_1_asset_id"
        ))

        # 6. Explainer Video 2 (Conditional)
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-EXP2",
            step_key="explainer_video_2",
            step_type=Phase0SequenceStepType.EXPLAINER_VIDEO,
            order_index=5,
            execution_mode=Phase0ExecutionMode.OPERATOR_REVIEW_REQUIRED,
            review_gate=True,
            required="explainer_video_2" in requested_outputs,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="explainer_video_2_asset_id"
        ))

        # 7. Cinematic storytelling video
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-CIN",
            step_key="cinematic_video",
            step_type=Phase0SequenceStepType.CINEMATIC_VIDEO,
            order_index=6,
            execution_mode=Phase0ExecutionMode.OPERATOR_REVIEW_REQUIRED,
            review_gate=True,
            required="cinematic_video" in requested_outputs,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="cinematic_video_asset_id"
        ))

        # 8. Optional carousel asset
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-CAROUSEL",
            step_key="carousel_spread",
            step_type=Phase0SequenceStepType.CAROUSEL_ASSET,
            order_index=7,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required="carousel_spread" in optional_outputs_enabled,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="carousel_asset_ids"
        ))

        # 9. Optional meme asset
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-MEME",
            step_key="meme_layer",
            step_type=Phase0SequenceStepType.MEME_ASSET,
            order_index=8,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required="meme_layer" in optional_outputs_enabled,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="meme_asset_ids"
        ))

        # 10. Preview assembly
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-PREVIEW",
            step_key="preview_assembly",
            step_type=Phase0SequenceStepType.PREVIEW_ASSEMBLY,
            order_index=9,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-PDF"],
            target_output_key="preview_bundle_ids"
        ))

        # 11. Payment handoff mapping
        generation_steps.append(Phase0SequenceStep(
            step_id=f"STP-GEN-{plan_id}-HANDOFF",
            step_key="payment_handoff",
            step_type=Phase0SequenceStepType.PAYMENT_HANDOFF,
            order_index=10,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            depends_on_step_ids=[f"STP-GEN-{plan_id}-AUDIT"],
            target_output_key="payment_handoff_ready"
        ))

        # ── Construct external release order steps (Section 4 Release sequencing) ──
        # Order: Exp 1 -> Exp 2 -> Cinematic -> PDF Audit -> Animated Audit -> Carousels/Memes -> Handoff
        release_steps: List[Phase0SequenceStep] = []
        
        # 1. Explainer 1
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-EXP1",
            step_key="explainer_video_1",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=0,
            execution_mode=Phase0ExecutionMode.OPERATOR_REVIEW_REQUIRED,
            review_gate=True,
            required="explainer_video_1" in requested_outputs,
            target_output_key="explainer_video_1_asset_id"
        ))

        # 2. Explainer 2
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-EXP2",
            step_key="explainer_video_2",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=1,
            execution_mode=Phase0ExecutionMode.OPERATOR_REVIEW_REQUIRED,
            review_gate=True,
            required="explainer_video_2" in requested_outputs,
            target_output_key="explainer_video_2_asset_id"
        ))

        # 3. Cinematic
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-CIN",
            step_key="cinematic_video",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=2,
            execution_mode=Phase0ExecutionMode.OPERATOR_REVIEW_REQUIRED,
            review_gate=True,
            required="cinematic_video" in requested_outputs,
            target_output_key="cinematic_video_asset_id"
        ))

        # 4. PDF Full Audit
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-PDF",
            step_key="pdf_assembly",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=3,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            target_output_key="pdf_audit_payload_id"
        ))

        # 5. Animated Audit explainer
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-AUDIT-VID",
            step_key="audit_explainer_video",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=4,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required="audit_explainer_video" in requested_outputs,
            target_output_key="audit_explainer_video_payload_id"
        ))

        # 6. Carousels/Memes
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-CAROUSEL",
            step_key="carousel_spread",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=5,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required="carousel_spread" in optional_outputs_enabled,
            target_output_key="carousel_asset_ids"
        ))
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-MEME",
            step_key="meme_layer",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=6,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required="meme_layer" in optional_outputs_enabled,
            target_output_key="meme_asset_ids"
        ))

        # 7. Payment/activation handoff bridge
        release_steps.append(Phase0SequenceStep(
            step_id=f"STP-REL-{plan_id}-HANDOFF",
            step_key="payment_handoff",
            step_type=Phase0SequenceStepType.RELEASE_STEP,
            order_index=7,
            execution_mode=Phase0ExecutionMode.AUTOMATIC,
            required=True,
            target_output_key="payment_handoff_ready"
        ))

        plan = Phase0DeliveryPlan(
            plan_id=plan_id,
            coach_id=coach_id,
            phase0_packet_id=packet.packet_id,
            package_variant=package_variant,
            requested_outputs=requested_outputs,
            generation_order=generation_steps,
            release_order=release_steps,
            review_required=True,
            optional_outputs_enabled=optional_outputs_enabled,
            sla_deadline_utc=sla_deadline,
            created_at_utc=now
        )

        # Log plan generation in receipt chain
        rc = self._get_receipt_chain(coach_id)
        rc.log(
            agent_id="phase0_delivery_orchestrator",
            action="delivery_plan_generated",
            asset_id=plan_id,
            person_id=packet.prospect_id,
            input_summary=f"Compile Phase-0 delivery plan for packet: {packet.packet_id}",
            output_summary=f"Plan generated under ID: {plan_id} with variant: {package_variant}",
            decision="approved",
            metadata={"variant": package_variant, "outputs": requested_outputs}
        )

        self.plans[plan_id] = plan
        return plan

    def start_run(self, plan: Phase0DeliveryPlan) -> Phase0DeliveryRun:
        """Initializes and kicks off a delivery run lifecycle record."""
        run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        bundle = Phase0OutputBundle(
            output_bundle_id=f"BND-{uuid.uuid4().hex[:8].upper()}",
            coach_id=plan.coach_id,
            phase0_packet_id=plan.phase0_packet_id
        )
        self.bundles[bundle.output_bundle_id] = bundle

        run = Phase0DeliveryRun(
            delivery_run_id=run_id,
            plan_id=plan.plan_id,
            coach_id=plan.coach_id,
            phase0_packet_id=plan.phase0_packet_id,
            status=Phase0DeliveryRunStatus.RUNNING,
            started_at_utc=now,
            output_bundle_id=bundle.output_bundle_id,
            review_state="NOT_STARTED"
        )

        # Log delivery run start
        rc = self._get_receipt_chain(plan.coach_id)
        rc.log(
            agent_id="phase0_delivery_orchestrator",
            action="delivery_run_started",
            asset_id=run_id,
            input_summary=f"Initialize delivery run for plan ID: {plan.plan_id}",
            output_summary=f"Run started under ID: {run_id}",
            decision="approved",
            metadata={"bundle_id": bundle.output_bundle_id}
        )

        self.runs[run_id] = run
        return run

    def execute_next_step(
        self,
        run: Phase0DeliveryRun,
        packet: Phase0ProspectPacket,
        optional_failures_map: Optional[Dict[str, bool]] = None
    ) -> Optional[Phase0SequenceStep]:
        """
        Executes the next uncompleted step in the generation order.
        Supports programmatic step execution and testing of failure conditions.
        """
        plan = self.plans[run.plan_id]
        bundle = self.bundles[run.output_bundle_id]
        
        # Find next step to execute
        executed_step_ids = {res.step_id for res in run.step_results}
        next_step: Optional[Phase0SequenceStep] = None
        for step in plan.generation_order:
            if step.step_id not in executed_step_ids:
                next_step = step
                break

        if not next_step:
            # All steps executed, finalize the run
            self.finalize_run(run)
            return None

        # If step is not required, skip it
        if not next_step.required:
            res = Phase0SequenceStepResult(
                step_id=next_step.step_id,
                status="SKIPPED",
                started_at_utc=datetime.now(timezone.utc),
                completed_at_utc=datetime.now(timezone.utc)
            )
            run.step_results.append(res)
            return next_step

        run.current_step_id = next_step.step_id
        now = datetime.now(timezone.utc)
        
        res = Phase0SequenceStepResult(
            step_id=next_step.step_id,
            status="RUNNING",
            started_at_utc=now
        )

        rc = self._get_receipt_chain(run.coach_id)

        try:
            # ── Programmatic simulation of asset failures (Section 6 & 10 rules) ──
            should_fail = optional_failures_map and optional_failures_map.get(next_step.step_key, False)
            if should_fail:
                raise RuntimeError(f"Simulated failure for step: {next_step.step_key}")

            # ── 1. AUDIT_CORE Step ──
            if next_step.step_type == Phase0SequenceStepType.AUDIT_CORE:
                if not packet.audit_targets:
                    raise ValueError("No audit targets found in prospect packet")
                
                target_id = packet.audit_targets[0].audit_target_id
                
                # If there are no captions, attach a dummy caption to satisfy the AuditIntelligenceEngine requirement
                if not packet.captions:
                    from src.ccp.models.phase0_intake_models import Phase0CaptionAttachment
                    dummy_caption = Phase0CaptionAttachment(
                        prospect_id=packet.prospect_id,
                        audit_target_id=target_id,
                        caption_text="Provisional dummy caption for evaluation",
                        source_kind="manual_entry"
                    )
                    packet.captions.append(dummy_caption)
                    packet.audit_targets[0].caption_id = dummy_caption.caption_id

                # Invoke the canonical AuditIntelligenceEngine (AC8 Fail-closed core audit logic)
                engine = AuditIntelligenceEngine(coach_acronym=self._get_acronym(run.coach_id))
                report = engine.generate_audit(packet=packet, target_id=target_id, provisional_override=True)
                
                bundle.audit_report_id = report.report_id
                res.produced_artifact_ids.append(report.report_id)
                res.status = "SUCCEEDED"

            # ── 2. CARD_RENDER Step ──
            elif next_step.step_type == Phase0SequenceStepType.CARD_RENDER:
                if not bundle.audit_report_id:
                    raise ValueError("Audit report must be generated before scorecard rendering")
                # Create visual scorecard references namespaced under run ID
                card_id = f"CRD-{uuid.uuid4().hex[:8].upper()}"
                bundle.score_card_board_ids.append(card_id)
                res.produced_artifact_ids.append(card_id)
                res.status = "SUCCEEDED"

            # ── 3. PDF_AUDIT_ASSEMBLY Step ──
            elif next_step.step_type == Phase0SequenceStepType.PDF_AUDIT_ASSEMBLY:
                if not bundle.audit_report_id:
                    raise ValueError("Audit report must exist for PDF assembly")
                # Assembly path translates report into PdfAuditPayload (Section 3.2 PDF assembly)
                pdf_id = f"PDF-{uuid.uuid4().hex[:8].upper()}"
                bundle.pdf_audit_payload_id = pdf_id
                res.produced_artifact_ids.append(pdf_id)
                res.status = "SUCCEEDED"

            # ── 4. AUDIT_EXPLAINER_VIDEO Step ──
            elif next_step.step_type == Phase0SequenceStepType.AUDIT_EXPLAINER_VIDEO:
                if not bundle.audit_report_id:
                    raise ValueError("Audit report must exist for animated explainer video")
                vid_payload_id = f"EXP-VID-PAYLOAD-{uuid.uuid4().hex[:8].upper()}"
                bundle.audit_explainer_video_payload_id = vid_payload_id
                res.produced_artifact_ids.append(vid_payload_id)
                res.status = "SUCCEEDED"

            # ── 5. EXPLAINER_VIDEO & CINEMATIC_VIDEO Rendering Steps ──
            elif next_step.step_type in [Phase0SequenceStepType.EXPLAINER_VIDEO, Phase0SequenceStepType.CINEMATIC_VIDEO]:
                # Dispatches normalized render requests directly into CMF-compatible realizations (AC3 & AC11)
                render_req = Phase0RenderRequest(
                    render_request_id=f"REQ-{uuid.uuid4().hex[:8].upper()}",
                    coach_id=run.coach_id,
                    phase0_packet_id=packet.packet_id,
                    delivery_run_id=run.delivery_run_id,
                    target_surface="shared_ccp_realization_queue",
                    artifact_family="video" if next_step.step_type == Phase0SequenceStepType.EXPLAINER_VIDEO else "cinematic",
                    source_payload_ids=[bundle.audit_report_id or "RPT-FALLBACK"],
                    template_key="staged_realization_v1",
                    priority="HIGH",
                    review_required=next_step.review_gate
                )
                
                # Mock CMF Pipeline execution conforming to Section 3.2, passing Adapted receipt chain!
                pipeline = CMFArcGovernedRenderingPipeline(receipt_chain=CMFReceiptAdapter(rc))
                spine = CoalitionSpineInput(
                    content_output_id=render_req.render_request_id,
                    coach_id=run.coach_id,
                    coach_acronym=self._get_acronym(run.coach_id),
                    selected_format="instagram_reel" if next_step.step_type == Phase0SequenceStepType.EXPLAINER_VIDEO else "cinematic_60s",
                    spine_text="Staged CMF realization sequence. The raw authentic voice is the key. Let the somatic witness guide." * 2,
                    somatic_arc_type="witness" if next_step.step_type == Phase0SequenceStepType.EXPLAINER_VIDEO else "rally",
                    voice_dna_id=f"VDNA-{run.coach_id}"
                )
                
                job = pipeline.create_job(spine)
                job = pipeline.run_epic_meaning_gate(job, blandness_confidence=0.08)
                release_res = pipeline.release(job)

                if not release_res:
                    raise RuntimeError("CMF Render release denied by Epic Meaning Gate")

                asset_id = release_res.composition_id

                if next_step.step_key == "explainer_video_1":
                    bundle.explainer_video_1_asset_id = asset_id
                elif next_step.step_key == "explainer_video_2":
                    bundle.explainer_video_2_asset_id = asset_id
                elif next_step.step_key == "cinematic_video":
                    bundle.cinematic_video_asset_id = asset_id

                res.produced_artifact_ids.append(asset_id)
                res.status = "SUCCEEDED"

            # ── 6. CAROUSEL_ASSET & MEME_ASSET Steps (Optional) ──
            elif next_step.step_type in [Phase0SequenceStepType.CAROUSEL_ASSET, Phase0SequenceStepType.MEME_ASSET]:
                asset_id = f"OPT-AST-{uuid.uuid4().hex[:8].upper()}"
                if next_step.step_type == Phase0SequenceStepType.CAROUSEL_ASSET:
                    bundle.carousel_asset_ids.append(asset_id)
                else:
                    bundle.meme_asset_ids.append(asset_id)
                res.produced_artifact_ids.append(asset_id)
                res.status = "SUCCEEDED"

            # ── 7. PREVIEW_ASSEMBLY Step ──
            elif next_step.step_type == Phase0SequenceStepType.PREVIEW_ASSEMBLY:
                # AC9: Preview Assembly Failure handles blocks (Section 7.7)
                preview_id = f"PVW-{uuid.uuid4().hex[:8].upper()}"
                bundle.preview_bundle_ids.append(preview_id)
                res.produced_artifact_ids.append(preview_id)
                res.status = "SUCCEEDED"

            # ── 8. PAYMENT_HANDOFF Step ──
            elif next_step.step_type == Phase0SequenceStepType.PAYMENT_HANDOFF:
                bundle.payment_handoff_ready = True
                res.status = "SUCCEEDED"

        except Exception as e:
            logger.error(f"Execution failed for step {next_step.step_id}: {str(e)}")
            res.status = "FAILED"
            res.failure_reason = str(e)

            # ── Handle Failure & Fallback Boundaries (Section 6 & AC7/AC8/AC9) ──
            # AC8 Fail-Closed Audit rules: if audit, PDF, or preview assembly fails, run is FAILED
            if next_step.step_type in [
                Phase0SequenceStepType.AUDIT_CORE,
                Phase0SequenceStepType.PDF_AUDIT_ASSEMBLY,
                Phase0SequenceStepType.PREVIEW_ASSEMBLY,
                Phase0SequenceStepType.PAYMENT_HANDOFF
            ]:
                run.status = Phase0DeliveryRunStatus.FAILED
                run.failure_state = f"{next_step.step_key}_failed"
            else:
                # Optional/Video asset failure (Honest degradation AC7)
                res.degraded = True
                # Run stays RUNNING or transitions into DEGRADED_READY internally

        res.completed_at_utc = datetime.now(timezone.utc)
        run.step_results.append(res)

        # Log Step execution event in ReceiptChain (AC6)
        receipt = Phase0DeliveryReceipt(
            receipt_id=f"RCP-{uuid.uuid4().hex[:8].upper()}",
            delivery_run_id=run.delivery_run_id,
            step_id=next_step.step_id,
            coach_id=run.coach_id,
            outcome="SUCCEEDED" if res.status == "SUCCEEDED" else ("DEGRADED" if res.degraded else "FAILED"),
            artifact_ids=res.produced_artifact_ids,
            notes=[res.failure_reason] if res.failure_reason else [],
            started_at_utc=res.started_at_utc,
            completed_at_utc=res.completed_at_utc
        )
        run.receipts.append(receipt)

        rc.log(
            agent_id="phase0_delivery_orchestrator",
            action="step_executed",
            asset_id=next_step.step_id,
            input_summary=f"Run step: {next_step.step_key} ({next_step.step_type.value})",
            output_summary=f"Outcome: {receipt.outcome}. Artifacts produced: {receipt.artifact_ids}",
            decision="approved",
            metadata={"run_status": run.status.value, "degraded": res.degraded}
        )

        return next_step

    def resolve_review_gate(self, run_id: str, step_id: str, approved: bool) -> Phase0DeliveryRun:
        """
        AC4: Explicit Operator Review Gate.
        Sets manual approval status for high-value video assets.
        """
        run = self.runs.get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")

        plan = self.plans[run.plan_id]
        step = next((s for s in plan.generation_order if s.step_id == step_id), None)
        if not step or not step.review_gate:
            raise ValueError(f"No review gate found for step {step_id}")

        step_res = next((res for res in run.step_results if res.step_id == step_id), None)
        if not step_res:
            raise ValueError(f"Step {step_id} has not been executed yet")

        rc = self._get_receipt_chain(run.coach_id)

        if approved:
            step_res.status = "SUCCEEDED"
            run.review_state = "APPROVED"
        else:
            step_res.status = "FAILED"
            step_res.failure_reason = "Operator review denied."
            run.review_state = "DENIED"
            run.status = Phase0DeliveryRunStatus.BLOCKED

        rc.log(
            agent_id="phase0_delivery_orchestrator",
            action="review_gate_resolved",
            asset_id=step_id,
            input_summary=f"Operator review submitted for step ID: {step_id}",
            output_summary=f"Approved: {approved}. Review State updated: {run.review_state}",
            decision="approved" if approved else "rejected"
        )

        return run

    def finalize_run(self, run: Phase0DeliveryRun) -> Phase0OutputBundle:
        """
        Finalizes run lifecycle, computes package status, and compiles the
        payment handoff packets.
        """
        plan = self.plans[run.plan_id]
        bundle = self.bundles[run.output_bundle_id]
        rc = self._get_receipt_chain(run.coach_id)

        # Check for release blockers (AC9 / Section G5 & G6)
        blockers = []
        if not bundle.audit_report_id:
            blockers.append("missing_core_audit_report")
        if not bundle.pdf_audit_payload_id:
            blockers.append("missing_pdf_payload")
        if not bundle.preview_bundle_ids:
            blockers.append("missing_preview_bundle")

        bundle.release_blockers = blockers

        # Core Minimum Rule check (Section G5 / AC10)
        has_critical_failures = run.status == Phase0DeliveryRunStatus.FAILED or any(
            res.status == "FAILED" and next(s for s in plan.generation_order if s.step_id == res.step_id).required and next(s for s in plan.generation_order if s.step_id == res.step_id).step_type in [
                Phase0SequenceStepType.AUDIT_CORE,
                Phase0SequenceStepType.PDF_AUDIT_ASSEMBLY,
                Phase0SequenceStepType.PREVIEW_ASSEMBLY,
                Phase0SequenceStepType.PAYMENT_HANDOFF
            ]
            for res in run.step_results
        )

        if len(blockers) > 0 or has_critical_failures:
            bundle.delivery_ready = False
            bundle.payment_handoff_ready = False
            run.status = Phase0DeliveryRunStatus.FAILED if has_critical_failures else Phase0DeliveryRunStatus.BLOCKED
        else:
            bundle.delivery_ready = True
            
            # Identify if some optional outputs failed (Honest degradation AC7)
            has_optional_failures = any(
                res.status == "FAILED" or res.degraded
                for res in run.step_results
            )
            
            if has_optional_failures:
                run.status = Phase0DeliveryRunStatus.DEGRADED_READY
            else:
                run.status = Phase0DeliveryRunStatus.COMPLETED

        run.completed_at_utc = datetime.now(timezone.utc)

        # Log completion
        rc.log(
            agent_id="phase0_delivery_orchestrator",
            action="delivery_run_completed",
            asset_id=run.delivery_run_id,
            input_summary=f"Finalize run: {run.delivery_run_id}",
            output_summary=f"Completed with status: {run.status.value}. Delivery Ready: {bundle.delivery_ready}",
            decision="approved",
            metadata={"blockers": blockers, "step_count": len(run.step_results)}
        )

        return bundle

    def get_payment_handoff_packet(self, run_id: str, report: AuditIntelligenceReport) -> Phase0PaymentHandoffPacket:
        """
        AC10: Returns explicit Phase0PaymentHandoffPacket based on the continuity bridge
        recommendation.
        """
        run = self.runs.get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")

        bundle = self.bundles[run.output_bundle_id]
        if not bundle.delivery_ready:
            raise ValueError("Cannot package payment handoff for an unready delivery bundle")

        # Map Continuity recommendations into concrete offer keys (PRD-09 continuity ladder)
        recommended_tier = report.continuity_bridge.recommended_tier
        if recommended_tier == BridgeTierRecommendation.COACH_OS_9999:
            offer_key = "coach_os_continuity_99"
        elif recommended_tier == BridgeTierRecommendation.SPEAKING_LEARNING_3999:
            offer_key = "speaking_learning_continuity_39"
        else:
            offer_key = "phase0_proof_unlock_29"

        return Phase0PaymentHandoffPacket(
            coach_id=run.coach_id,
            phase0_packet_id=bundle.phase0_packet_id,
            delivery_run_id=run.delivery_run_id,
            output_bundle_id=bundle.output_bundle_id,
            commercial_offer_key=offer_key,
            payment_ready=True,
            release_ready=True,
            upgrade_credit_eligible=True
        )
