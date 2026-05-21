"""
src/ccp/services/phase0_review_board_service.py
================================================
Core service implementing FR-ERA3-40 Phase-0 Batch Execution Review and Approval Board.
Manages run aggregation, operator decisions, rerun provenance, and release state gating.
"""

from __future__ import annotations
import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_review_board_models import (
    Phase0BatchExecutionBoard,
    Phase0ReviewRow,
    Phase0ArtifactReviewSet,
    Phase0ApprovalDecision,
    Phase0RerunRequest,
    Phase0RevisionRequest,
    Phase0ReleaseState,
    Phase0PaymentReadyState,
)
from src.ccp.models.phase0_delivery_models import (
    Phase0DeliveryRun,
    Phase0DeliveryRunStatus,
    Phase0SequenceStepResult,
    Phase0SequenceStepType,
)
from src.ccp.services.phase0_delivery_orchestrator import Phase0DeliveryOrchestrator
from src.ccp.services.phase0_commercial_bridge import Phase0CommercialBridgeService
from src.ccp.models.phase0_commercial_models import Phase0CommercialStage

logger = logging.getLogger(__name__)


class Phase0ReviewBoardService:
    """
    Coordinates operators' review decisions, aggregates run outputs, evaluates
    release readiness rules, and manages payment readiness integration.
    """

    def __init__(
        self,
        orchestrator: Phase0DeliveryOrchestrator,
        commercial_bridge: Phase0CommercialBridgeService,
        log_dir: Optional[str] = None,
    ):
        self.orchestrator = orchestrator
        self.commercial_bridge = commercial_bridge
        self.log_dir = log_dir

        # In-memory storage mirroring DB tables
        self.decisions: Dict[str, List[Phase0ApprovalDecision]] = {}
        self.rerun_requests: Dict[str, Phase0RerunRequest] = {}
        self.revision_requests: Dict[str, Phase0RevisionRequest] = {}
        self.run_lineage: Dict[str, str] = {}

    def _get_acronym(self, coach_id: str) -> str:
        """Extract acronym from coach ID or return default."""
        if coach_id and len(coach_id) >= 3:
            return coach_id[:3].upper()
        return "P0B"

    def _get_receipt_chain(self, coach_id: str) -> ReceiptChain:
        """Helper to fetch coach-specific ReceiptChain."""
        return ReceiptChain(coach_acronym=self._get_acronym(coach_id), log_dir=self.log_dir)

    def aggregate_board(self, coach_id: Optional[str] = None) -> Phase0BatchExecutionBoard:
        """
        Assembles all runs into a high-level review board filtered optionally by coach_id.
        Evaluates blockers, release state, and payment state for each run.
        """
        rows: List[Phase0ReviewRow] = []

        # Find all runs
        target_runs = list(self.orchestrator.runs.values())
        if coach_id:
            target_runs = [r for r in target_runs if r.coach_id == coach_id]

        for run in target_runs:
            row = self.load_row(run.delivery_run_id)
            rows.append(row)

        # Compute board metrics
        generated_at = datetime.now(timezone.utc)
        total_rows = len(rows)
        ready_rows = sum(1 for r in rows if r.review_status == "approved" or r.release_state.status in ["release_ready", "released"])
        blocked_rows = sum(1 for r in rows if r.release_state.status == "blocked")
        payment_ready_rows = sum(1 for r in rows if r.payment_ready_state.status == "payment_ready")
        release_ready_rows = sum(1 for r in rows if r.release_state.status == "release_ready")

        board = Phase0BatchExecutionBoard(
            board_id=f"BRD-{uuid.uuid4().hex[:8].upper()}",
            generated_at=generated_at,
            filter_state={"coach_id": coach_id} if coach_id else {},
            total_rows=total_rows,
            ready_rows=ready_rows,
            blocked_rows=blocked_rows,
            payment_ready_rows=payment_ready_rows,
            release_ready_rows=release_ready_rows,
            rows=rows,
        )
        return board

    def load_row(self, run_id: str) -> Phase0ReviewRow:
        """
        Fetches detailed review row state for a target delivery run.
        Populates artifacts, release state, payment state, and latest decision.
        """
        run = self.orchestrator.runs.get(run_id)
        if not run:
            raise ValueError(f"Delivery run {run_id} not found")

        plan = self.orchestrator.plans.get(run.plan_id)
        if not plan:
            raise ValueError(f"Plan {run.plan_id} associated with run {run_id} not found")

        bundle = self.orchestrator.bundles.get(run.output_bundle_id)
        if not bundle:
            raise ValueError(f"Bundle {run.output_bundle_id} associated with run {run_id} not found")

        # Resolve latest decision
        run_decisions = self.decisions.get(run_id, [])
        latest_decision = run_decisions[-1] if run_decisions else None

        # Resolve prior runs for side-by-side compare
        compare_targets = []
        prior_run_id = self.run_lineage.get(run_id)
        curr_prior_id = prior_run_id
        while curr_prior_id:
            compare_targets.append(curr_prior_id)
            curr_prior_id = self.run_lineage.get(curr_prior_id)

        # Assemble review artifacts set
        artifact_review_set = self._assemble_artifact_review_set(run, plan, bundle)

        # Compute release and payment ready states
        release_state = self._compute_release_state(
            run, plan, bundle, latest_decision, artifact_review_set
        )
        payment_ready_state = self._compute_payment_ready_state(
            run, bundle, release_state
        )

        review_status = "not_started"
        if latest_decision:
            review_status = latest_decision.decision_type

        blocking_reason_codes = list(bundle.release_blockers)
        if release_state.status == "blocked":
            blocking_reason_codes.extend(release_state.release_blockers)
            # Dedup
            blocking_reason_codes = list(set(blocking_reason_codes))

        row = Phase0ReviewRow(
            coach_id=run.coach_id,
            prospect_packet_id=plan.phase0_packet_id,
            run_id=run_id,
            prior_run_id=prior_run_id,
            artifact_set_id=bundle.output_bundle_id,
            coach_display_name=f"Coach {run.coach_id.upper()}",
            content_type_mix=plan.requested_outputs,
            execution_status=run.status.value,
            review_status=review_status,
            blocking_reason_codes=blocking_reason_codes,
            artifact_review_set=artifact_review_set,
            release_state=release_state,
            payment_ready_state=payment_ready_state,
            latest_decision=latest_decision,
            compare_targets=compare_targets,
            updated_at=datetime.now(timezone.utc),
        )
        return row

    def approve(self, run_id: str, operator_id: str, note: Optional[str] = None) -> Phase0ApprovalDecision:
        """
        Operator decision to approve the run.
        Emits canonical decision to ReceiptChain and transitions review state.
        """
        run = self.orchestrator.runs.get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")

        bundle = self.orchestrator.bundles.get(run.output_bundle_id)
        if not bundle:
            raise ValueError(f"Bundle for run {run_id} not found")

        # Validate that we have core artifacts before allowing approval
        plan = self.orchestrator.plans.get(run.plan_id)
        if not bundle.pdf_audit_payload_id:
            raise ValueError("Cannot approve: PDF audit payload is missing")
        if not bundle.score_card_board_ids:
            raise ValueError("Cannot approve: Score card board is missing")

        # Collect produced artifact IDs
        target_artifact_ids = []
        if bundle.pdf_audit_payload_id:
            target_artifact_ids.append(bundle.pdf_audit_payload_id)
        if bundle.score_card_board_ids:
            target_artifact_ids.extend(bundle.score_card_board_ids)
        if bundle.audit_explainer_video_payload_id:
            target_artifact_ids.append(bundle.audit_explainer_video_payload_id)
        if bundle.explainer_video_1_asset_id:
            target_artifact_ids.append(bundle.explainer_video_1_asset_id)
        if bundle.explainer_video_2_asset_id:
            target_artifact_ids.append(bundle.explainer_video_2_asset_id)
        if bundle.cinematic_video_asset_id:
            target_artifact_ids.append(bundle.cinematic_video_asset_id)

        decision = Phase0ApprovalDecision(
            decision_id=f"DEC-APP-{uuid.uuid4().hex[:8].upper()}",
            coach_id=run.coach_id,
            run_id=run_id,
            artifact_set_id=bundle.output_bundle_id,
            decision_type="approve",
            operator_id=operator_id,
            reason_code="OPERATOR_APPROVED",
            note=note,
            target_artifact_ids=target_artifact_ids,
            created_at=datetime.now(timezone.utc),
        )

        self.decisions.setdefault(run_id, []).append(decision)

        # Log decision to receipt chain
        rc = self._get_receipt_chain(run.coach_id)
        rc.log(
            agent_id="phase0_review_board",
            action="approve",
            asset_id=run_id,
            person_id=plan.phase0_packet_id if plan else None,
            input_summary=f"Operator {operator_id} approves run {run_id}",
            output_summary=f"Approved with decision ID: {decision.decision_id}",
            decision="approved",
            decision_rationale=note,
            metadata={
                "decision_id": decision.decision_id,
                "operator_id": operator_id,
                "run_id": run_id,
                "artifact_set_id": bundle.output_bundle_id,
            },
        )

        # Update run's review status
        run.review_state = "APPROVED"
        return decision

    def reject(self, run_id: str, operator_id: str, note: Optional[str] = None) -> Phase0ApprovalDecision:
        """
        Operator decision to reject the run.
        Emits canonical decision to ReceiptChain and transitions review state.
        """
        run = self.orchestrator.runs.get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")

        bundle = self.orchestrator.bundles.get(run.output_bundle_id)
        if not bundle:
            raise ValueError(f"Bundle for run {run_id} not found")

        plan = self.orchestrator.plans.get(run.plan_id)

        decision = Phase0ApprovalDecision(
            decision_id=f"DEC-REJ-{uuid.uuid4().hex[:8].upper()}",
            coach_id=run.coach_id,
            run_id=run_id,
            artifact_set_id=bundle.output_bundle_id,
            decision_type="reject",
            operator_id=operator_id,
            reason_code="OPERATOR_REJECTED",
            note=note,
            target_artifact_ids=[],
            created_at=datetime.now(timezone.utc),
        )

        self.decisions.setdefault(run_id, []).append(decision)

        # Log decision to receipt chain
        rc = self._get_receipt_chain(run.coach_id)
        rc.log(
            agent_id="phase0_review_board",
            action="reject",
            asset_id=run_id,
            person_id=plan.phase0_packet_id if plan else None,
            input_summary=f"Operator {operator_id} rejects run {run_id}",
            output_summary=f"Rejected with decision ID: {decision.decision_id}",
            decision="rejected",
            decision_rationale=note,
            metadata={
                "decision_id": decision.decision_id,
                "operator_id": operator_id,
                "run_id": run_id,
            },
        )

        run.review_state = "DENIED"
        run.status = Phase0DeliveryRunStatus.BLOCKED
        return decision

    def rerun(
        self,
        run_id: str,
        target_scope: Literal[
            "full_package",
            "audit_only",
            "audit_video_only",
            "explainer_1_only",
            "explainer_2_only",
            "cinematic_only",
            "optional_assets_only",
        ],
        operator_id: str,
        reason_code: str,
        note: Optional[str] = None,
    ) -> Phase0RerunRequest:
        """
        Requests a scoped rerun of a delivery run.
        Generates a new run record pointing back to the prior run_id to preserve lineage,
        copying over unaffected successful step results so they are not re-executed.
        """
        run = self.orchestrator.runs.get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")

        plan = self.orchestrator.plans.get(run.plan_id)
        if not plan:
            raise ValueError(f"Plan associated with run {run_id} not found")

        rerun_request_id = f"REQ-RRN-{uuid.uuid4().hex[:8].upper()}"
        rerun_request = Phase0RerunRequest(
            rerun_request_id=rerun_request_id,
            coach_id=run.coach_id,
            source_run_id=run_id,
            source_artifact_set_id=run.output_bundle_id,
            target_scope=target_scope,
            requested_by=operator_id,
            reason_code=reason_code,
            note=note,
            created_at=datetime.now(timezone.utc),
        )

        self.rerun_requests[rerun_request_id] = rerun_request

        # Log rerun request to receipt chain
        rc = self._get_receipt_chain(run.coach_id)
        rc.log(
            agent_id="phase0_review_board",
            action="rerun_requested",
            asset_id=run_id,
            person_id=plan.phase0_packet_id,
            input_summary=f"Operator {operator_id} requests rerun of scope {target_scope} on run {run_id}",
            output_summary=f"Rerun requested under request ID: {rerun_request_id}",
            decision="approved",
            metadata={
                "rerun_request_id": rerun_request_id,
                "source_run_id": run_id,
                "target_scope": target_scope,
                "reason_code": reason_code,
            },
        )

        # ── Trigger the new run on the orchestrator ──
        new_run = self.orchestrator.start_run(plan)
        self.run_lineage[new_run.delivery_run_id] = run_id  # Preserve rerun lineage!

        # Copy successful unaffected step results from prior run
        new_bundle = self.orchestrator.bundles[new_run.output_bundle_id]
        prior_bundle = self.orchestrator.bundles[run.output_bundle_id]

        for step in plan.generation_order:
            # Check if this step is targeted by the rerun scope
            is_targeted = False
            if target_scope == "full_package":
                is_targeted = True
            elif target_scope == "audit_only" and step.step_key == "audit_core":
                is_targeted = True
            elif target_scope == "audit_video_only" and step.step_key == "audit_explainer_video":
                is_targeted = True
            elif target_scope == "explainer_1_only" and step.step_key == "explainer_video_1":
                is_targeted = True
            elif target_scope == "explainer_2_only" and step.step_key == "explainer_video_2":
                is_targeted = True
            elif target_scope == "cinematic_only" and step.step_key == "cinematic_video":
                is_targeted = True
            elif target_scope == "optional_assets_only" and step.step_key in ["carousel_spread", "meme_layer"]:
                is_targeted = True

            if not is_targeted:
                # Find prior step result and copy if SUCCEEDED
                prior_res = next((res for res in run.step_results if res.step_id == step.step_id), None)
                if prior_res and prior_res.status == "SUCCEEDED":
                    new_res = Phase0SequenceStepResult(
                        step_id=step.step_id,
                        status="SUCCEEDED",
                        produced_artifact_ids=list(prior_res.produced_artifact_ids),
                        started_at_utc=prior_res.started_at_utc,
                        completed_at_utc=prior_res.completed_at_utc,
                    )
                    new_run.step_results.append(new_res)

                    # Also copy the produced artifact reference to the new bundle
                    if step.step_key == "audit_core":
                        new_bundle.audit_report_id = prior_bundle.audit_report_id
                    elif step.step_key == "pdf_assembly":
                        new_bundle.pdf_audit_payload_id = prior_bundle.pdf_audit_payload_id
                    elif step.step_key == "audit_explainer_video":
                        new_bundle.audit_explainer_video_payload_id = prior_bundle.audit_explainer_video_payload_id
                    elif step.step_key == "explainer_video_1":
                        new_bundle.explainer_video_1_asset_id = prior_bundle.explainer_video_1_asset_id
                    elif step.step_key == "explainer_video_2":
                        new_bundle.explainer_video_2_asset_id = prior_bundle.explainer_video_2_asset_id
                    elif step.step_key == "cinematic_video":
                        new_bundle.cinematic_video_asset_id = prior_bundle.cinematic_video_asset_id
                    elif step.step_key == "carousel_spread":
                        new_bundle.carousel_asset_ids = list(prior_bundle.carousel_asset_ids)
                    elif step.step_key == "meme_layer":
                        new_bundle.meme_asset_ids = list(prior_bundle.meme_asset_ids)
                    elif step.step_key == "preview_assembly":
                        new_bundle.preview_bundle_ids = list(prior_bundle.preview_bundle_ids)
                    elif step.step_key == "payment_handoff":
                        new_bundle.payment_handoff_ready = prior_bundle.payment_handoff_ready

        # Save an approval decision of type rerun to keep row state correct
        decision = Phase0ApprovalDecision(
            decision_id=f"DEC-RRN-{uuid.uuid4().hex[:8].upper()}",
            coach_id=run.coach_id,
            run_id=run_id,
            artifact_set_id=run.output_bundle_id,
            decision_type="rerun",
            operator_id=operator_id,
            reason_code=reason_code,
            note=note,
            target_artifact_ids=[],
            created_at=datetime.now(timezone.utc),
        )
        self.decisions.setdefault(run_id, []).append(decision)

        # Mark prior run review state
        run.review_state = "RERUN"
        return rerun_request

    def revise(
        self,
        run_id: str,
        severity: Literal["minor", "major", "blocking"],
        issue_code: str,
        note: str,
        operator_id: str,
    ) -> Phase0RevisionRequest:
        """
        Submits a manual revision request against a run.
        Transitions the run's review state and records the decision.
        """
        run = self.orchestrator.runs.get(run_id)
        if not run:
            raise ValueError(f"Run {run_id} not found")

        bundle = self.orchestrator.bundles.get(run.output_bundle_id)
        if not bundle:
            raise ValueError(f"Bundle for run {run_id} not found")

        plan = self.orchestrator.plans.get(run.plan_id)

        revision_request_id = f"REQ-REV-{uuid.uuid4().hex[:8].upper()}"
        revision_request = Phase0RevisionRequest(
            revision_request_id=revision_request_id,
            coach_id=run.coach_id,
            run_id=run_id,
            artifact_set_id=bundle.output_bundle_id,
            severity=severity,
            issue_code=issue_code,
            note=note,
            requested_by=operator_id,
            created_at=datetime.now(timezone.utc),
        )

        self.revision_requests[revision_request_id] = revision_request

        decision = Phase0ApprovalDecision(
            decision_id=f"DEC-REV-{uuid.uuid4().hex[:8].upper()}",
            coach_id=run.coach_id,
            run_id=run_id,
            artifact_set_id=bundle.output_bundle_id,
            decision_type="revise",
            operator_id=operator_id,
            reason_code=issue_code,
            note=note,
            target_artifact_ids=[],
            created_at=datetime.now(timezone.utc),
        )
        self.decisions.setdefault(run_id, []).append(decision)

        # Log to receipt chain
        rc = self._get_receipt_chain(run.coach_id)
        rc.log(
            agent_id="phase0_review_board",
            action="revision_requested",
            asset_id=run_id,
            person_id=plan.phase0_packet_id if plan else None,
            input_summary=f"Operator {operator_id} requests revision on run {run_id}",
            output_summary=f"Revision request {revision_request_id} created with severity {severity}",
            decision="rejected" if severity == "blocking" else "approved",
            decision_rationale=note,
            metadata={
                "revision_request_id": revision_request_id,
                "severity": severity,
                "issue_code": issue_code,
            },
        )

        run.review_state = "REVISE"
        if severity == "blocking":
            run.status = Phase0DeliveryRunStatus.BLOCKED

        return revision_request

    def _assemble_artifact_review_set(
        self,
        run: Phase0DeliveryRun,
        plan: Any,
        bundle: Any,
    ) -> Phase0ArtifactReviewSet:
        """Helper to group produced bundle artifacts and categorize them by required vs optional."""
        missing_req = []
        failed_opt = []
        auto_passed = []
        human_review_required = []

        # Audit PDF, Audit cards, and Explainer video are core human-review primitives
        human_review_required.append("audit_pdf")
        human_review_required.append("audit_card_board")
        human_review_required.append("audit_explainer_video")

        # Map step execution results to missing / failed status lists
        for step in plan.generation_order:
            step_res = next((res for res in run.step_results if res.step_id == step.step_id), None)
            is_failed = step_res and step_res.status == "FAILED"
            is_missing = not step_res or step_res.status in ["PENDING", "RUNNING"]

            is_required = step.required and step.step_key not in ["carousel_spread", "meme_layer"]
            if is_required:
                if is_failed or is_missing:
                    missing_req.append(step.step_key)
                if step.execution_mode == "AUTOMATIC":
                    auto_passed.append(step.step_key)
                else:
                    human_review_required.append(step.step_key)
            else:
                if is_failed or (step_res and step_res.degraded):
                    failed_opt.append(step.step_key)
                auto_passed.append(step.step_key)

        # Assemble and resolve paths honestly (AC-8)
        # Previews are resolved to /previews/<id>.<ext> only if the source artifact exists!
        # If the preview path is manually cleared or unavailable, we show artifact ID but path remains None.
        pdf_path = f"/previews/{bundle.pdf_audit_payload_id}.pdf" if bundle.pdf_audit_payload_id else None
        card_path = f"/previews/{bundle.score_card_board_ids[0]}.png" if bundle.score_card_board_ids else None
        audit_vid_path = f"/previews/{bundle.audit_explainer_video_payload_id}.mp4" if bundle.audit_explainer_video_payload_id else None
        exp1_path = f"/previews/{bundle.explainer_video_1_asset_id}.mp4" if bundle.explainer_video_1_asset_id else None
        exp2_path = f"/previews/{bundle.explainer_video_2_asset_id}.mp4" if bundle.explainer_video_2_asset_id else None
        cin_path = f"/previews/{bundle.cinematic_video_asset_id}.mp4" if bundle.cinematic_video_asset_id else None

        review_set = Phase0ArtifactReviewSet(
            audit_pdf_artifact_id=bundle.pdf_audit_payload_id,
            audit_pdf_preview_path=pdf_path,
            audit_card_board_artifact_id=bundle.score_card_board_ids[0] if bundle.score_card_board_ids else None,
            audit_card_board_preview_path=card_path,
            audit_explainer_video_artifact_id=bundle.audit_explainer_video_payload_id,
            audit_explainer_video_preview_path=audit_vid_path,
            explainer_video_1_artifact_id=bundle.explainer_video_1_asset_id,
            explainer_video_1_preview_path=exp1_path,
            explainer_video_2_artifact_id=bundle.explainer_video_2_asset_id,
            explainer_video_2_preview_path=exp2_path,
            cinematic_video_artifact_id=bundle.cinematic_video_asset_id,
            cinematic_video_preview_path=cin_path,
            carousel_artifact_id=bundle.carousel_asset_ids[0] if bundle.carousel_asset_ids else None,
            meme_artifact_id=bundle.meme_asset_ids[0] if bundle.meme_asset_ids else None,
            preview_bundle_path=bundle.preview_bundle_ids[0] if bundle.preview_bundle_ids else None,
            missing_required_artifacts=list(set(missing_req)),
            failed_optional_artifacts=list(set(failed_opt)),
            auto_passed_artifacts=list(set(auto_passed)),
            human_review_required_artifacts=list(set(human_review_required)),
        )
        return review_set

    def _compute_release_state(
        self,
        run: Phase0DeliveryRun,
        plan: Any,
        bundle: Any,
        latest_decision: Optional[Phase0ApprovalDecision],
        artifact_review_set: Phase0ArtifactReviewSet,
    ) -> Phase0ReleaseState:
        """
        GC-1 & GC-2 & GC-3 Gating logic:
        Calculates the Phase0ReleaseState from artifacts and Operator approval state.
        """
        # Hard block if core components are missing
        blockers = []
        if not bundle.pdf_audit_payload_id:
            blockers.append("missing_core_audit_pdf")
        if not bundle.score_card_board_ids:
            blockers.append("missing_score_card_board")
        if not bundle.audit_explainer_video_payload_id:
            blockers.append("missing_audit_explainer_video")

        # Map plan's required outputs to verify presence
        for step in plan.generation_order:
            is_step_required = step.required and step.step_key not in ["preview_assembly", "payment_handoff", "carousel_spread", "meme_layer"]
            if is_step_required:
                step_res = next((res for res in run.step_results if res.step_id == step.step_id), None)
                if not step_res or step_res.status != "SUCCEEDED":
                    blockers.append(f"missing_{step.step_key}")

        # Dedup blockers
        blockers = list(set(blockers))

        # Check approval state
        is_approved = latest_decision and latest_decision.decision_type == "approve"
        is_rejected = latest_decision and latest_decision.decision_type == "reject"
        is_revised = latest_decision and latest_decision.decision_type == "revise"

        # Determine release status
        if len(blockers) > 0 or is_rejected or is_revised or run.status == Phase0DeliveryRunStatus.FAILED:
            status = "blocked"
        elif not is_approved:
            status = "review_in_progress"
        else:
            # All core approved. Check optional outputs for honest degradation (GC-3)
            if artifact_review_set.failed_optional_artifacts:
                status = "core_ready_optional_failed"
            else:
                # Check if optional outputs are defined in the plan but missing in the bundle
                has_missing_optional = False
                for opt_out in plan.optional_outputs_enabled:
                    if opt_out == "carousel_spread" and not bundle.carousel_asset_ids:
                        has_missing_optional = True
                    elif opt_out == "meme_layer" and not bundle.meme_asset_ids:
                        has_missing_optional = True

                if has_missing_optional:
                    status = "core_ready_optional_missing"
                else:
                    status = "release_ready"

        # Collect approved and pending lists
        approved_req = []
        pending_req = []
        for r_out in plan.requested_outputs:
            if is_approved:
                approved_req.append(r_out)
            else:
                pending_req.append(r_out)

        released_at = None
        if run.status == Phase0DeliveryRunStatus.COMPLETED and is_approved:
            released_at = latest_decision.created_at

        return Phase0ReleaseState(
            status=status,
            release_blockers=blockers,
            approved_required_artifacts=approved_req,
            pending_required_artifacts=pending_req,
            released_at=released_at,
        )

    def _compute_payment_ready_state(
        self,
        run: Phase0DeliveryRun,
        bundle: Any,
        release_state: Phase0ReleaseState,
    ) -> Phase0PaymentReadyState:
        """
        GC-5 Commercial Separation logic:
        Calculates payment readiness, separating review approval from payment confirm.
        """
        blockers = []
        # If release is blocked or review is in progress, payment handoff is NOT ready
        if release_state.status in ["blocked", "review_in_progress"]:
            blockers.append("review_not_approved_or_blocked")

        # Resolve or create commercial state via Commercial Bridge
        comm_state = self.commercial_bridge.get_or_create_commercial_state(
            packet_id=run.phase0_packet_id,  # Actually packet_id maps to packet_id parameter in commercial bridge get_or_create
            delivery_run_id=run.delivery_run_id,
        )

        # Check if the commercial stage is blocked
        if not comm_state:
            blockers.append("missing_commercial_bridge_state")

        # Resolve payment readiness status
        if len(blockers) > 0:
            status = "not_ready"
        else:
            # We are ready from review standpoint.
            # Check commercial paid state
            if comm_state.phase0_unlock_paid:
                status = "unlock_confirmed"
            elif comm_state.stage == Phase0CommercialStage.UNLOCK_OFFER_READY:
                status = "payment_ready"
            elif comm_state.stage == Phase0CommercialStage.PROOF_VISIBLE:
                # Update stage to offer ready as review passed
                comm_state.stage = Phase0CommercialStage.UNLOCK_OFFER_READY
                status = "payment_ready"
            else:
                status = "unlock_initiated"

        return Phase0PaymentReadyState(
            status=status,
            bridge_compatible=True,
            commercial_state_ref=comm_state.commercial_state_id if comm_state else None,
            blockers=blockers,
            updated_at=datetime.now(timezone.utc),
        )
