"""
FR-ERA3-39 Phase-0 Campaign Workspace Service
=============================================
Orchestrates coach rows, bindings, bulk uploads, readiness recomputation,
and execution triggers for the shared trial phase outreach board.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional, Literal, Any

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_campaign_frontend_models import (
    Phase0CampaignWorkspace,
    Phase0CoachRow,
    Phase0CoachBinding,
    Phase0BatchUploadSession,
    Phase0ReadinessSummary,
    Phase0ExecutionRequest,
    Phase0WorkspaceFilterState,
    Phase0BulkAttachmentResult,
    Phase0WorkspaceHealth,
)
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0ProspectStatus,
    Phase0DeliveryReadiness,
)
from src.ccp.models.phase0_workspace_models import (
    Phase0WorkspaceRecord,
    Phase0WorkspaceStatus,
)
from src.ccp.models.phase0_delivery_models import (
    Phase0DeliveryRun,
    Phase0DeliveryRunStatus,
)

from src.ccp.services.phase0_intake_service import Phase0IntakeService
from src.ccp.services.phase0_workspace_service import Phase0WorkspaceService
from src.ccp.services.phase0_delivery_orchestrator import Phase0DeliveryOrchestrator


class Phase0CampaignWorkspaceService:
    """
    Coordinates Campaign Workspace actions: bindings, bulk uploads, readiness gating,
    and triggering executions without dedicated containers (Shared Namespace Law).
    """

    def __init__(
        self,
        intake_service: Optional[Phase0IntakeService] = None,
        workspace_service: Optional[Phase0WorkspaceService] = None,
        delivery_orchestrator: Optional[Phase0DeliveryOrchestrator] = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        self.intake_service = intake_service or Phase0IntakeService()
        self.workspace_service = workspace_service or Phase0WorkspaceService()
        self.delivery_orchestrator = delivery_orchestrator or Phase0DeliveryOrchestrator()
        self._rc = receipt_chain or ReceiptChain(coach_acronym="CMW")

        # In-memory session stores
        self.workspaces: Dict[str, Phase0CampaignWorkspace] = {}
        self.batch_upload_sessions: Dict[str, Phase0BatchUploadSession] = {}
        self.execution_requests: Dict[str, Phase0ExecutionRequest] = {}

    def get_or_create_campaign_workspace(
        self,
        workspace_id: str,
        operator_id: str,
        title: str = "Phase-0 Outreach Control Board",
    ) -> Phase0CampaignWorkspace:
        """Fetch or initialize a Campaign Workspace."""
        if workspace_id not in self.workspaces:
            filter_state = Phase0WorkspaceFilterState()
            self.workspaces[workspace_id] = Phase0CampaignWorkspace(
                workspace_id=workspace_id,
                title=title,
                operator_id=operator_id,
                rows=[],
                filter_state=filter_state,
                selected_row_ids=[],
                generated_at_utc=datetime.now(timezone.utc),
            )
        elif operator_id != "system":
            self.workspaces[workspace_id].operator_id = operator_id
        return self.workspaces[workspace_id]

    def update_filter_state(
        self,
        workspace_id: str,
        filter_state: Phase0WorkspaceFilterState,
    ) -> Phase0CampaignWorkspace:
        """Update filter state on the workspace."""
        workspace = self.get_or_create_campaign_workspace(workspace_id, "system")
        workspace.filter_state = filter_state
        return workspace

    def bind_coach(
        self,
        workspace_id: str,
        row_id: str,
        coach_id: str,
        provisional_label: Optional[str] = None,
    ) -> Phase0CoachBinding:
        """
        AC1: Bind/map an internal prospect packet record to a stable coach_id.
        Logs a 'PHASE0-COACH-BIND' receipt.
        """
        packet = self.intake_service.get_prospect(row_id)
        if not packet:
            raise ValueError(f"Prospect record {row_id} not found")

        # Set or update the coach_id in the intake packet
        packet.coach_id = coach_id
        packet.updated_at = datetime.now(timezone.utc).isoformat()

        # Determine binding state
        binding_state: Literal["PROVISIONAL", "RESOLVED", "INVALID"] = "RESOLVED"
        if not coach_id or not coach_id.strip():
            binding_state = "PROVISIONAL"
        elif len(coach_id) < 3:
            binding_state = "INVALID"

        coach_acronym = coach_id[:3].upper() if len(coach_id) >= 3 else None

        binding = Phase0CoachBinding(
            binding_id=f"BND-{uuid.uuid4().hex[:8].upper()}",
            provisional_label=provisional_label,
            coach_id=coach_id,
            coach_acronym=coach_acronym,
            binding_state=binding_state,
            created_at_utc=datetime.now(timezone.utc),
            resolved_at_utc=datetime.now(timezone.utc) if binding_state == "RESOLVED" else None,
        )

        # Log receipt stage mutations
        self._rc.log(
            agent_id="phase0_campaign_workspace_service",
            action="PHASE0-COACH-BIND",
            asset_id=row_id,
            person_id=row_id,
            input_summary=f"Bind coach ID '{coach_id}' to row '{row_id}'",
            output_summary=f"Binding resolved as: {binding_state}",
            decision="approved",
            metadata={"binding_id": binding.binding_id, "coach_acronym": coach_acronym},
        )

        return binding

    def evaluate_readiness(self, row_id: str) -> Phase0ReadinessSummary:
        """
        AC5: Synthesize and check validation gaps for intake rows.
        Uses Rule-based quality gates.
        """
        packet = self.intake_service.get_prospect(row_id)
        if not packet:
            raise ValueError(f"Prospect record {row_id} not found")

        # Run intake validation to update missing input states
        readiness_state = self.intake_service.validate_readiness(row_id)

        # Map details to Campaign readiness summary format
        ready = (
            readiness_state.delivery_readiness
            in {
                Phase0DeliveryReadiness.READY,
                Phase0DeliveryReadiness.READY_HIGH_CONFIDENCE,
                Phase0DeliveryReadiness.CONDITIONALLY_READY,
            }
        )

        missing_fields = [m.missing_code for m in readiness_state.blocking_missing_inputs]

        attached_count = len(packet.media_sources) + len(packet.transcript_sources)
        grouped_count = len(packet.media_sources)

        return Phase0ReadinessSummary(
            phase0_packet_id=packet.packet_id,
            ready=ready,
            missing_required_fields=missing_fields,
            attached_file_count=attached_count,
            grouped_file_count=grouped_count,
            audit_target_count=len(packet.audit_targets),
            audience_present=packet.target_audience_profile is not None,
            business_intelligence_present=packet.guardian_business_intelligence_bundle is not None,
            last_checked_at_utc=datetime.now(timezone.utc),
        )

    def bulk_stage_upload(
        self,
        workspace_id: str,
        operator_id: str,
        files: List[Dict[str, Any]],
        target_row_ids: List[str],
    ) -> Phase0BulkAttachmentResult:
        """
        AC2: Bulk upload / attach source files.
        AC3: Staging and multi-coach intake grouping in namespaced folders.
        Logs a 'PHASE0-BATCH-UPLOAD' receipt.
        """
        session_id = f"BUS-{uuid.uuid4().hex[:8].upper()}"

        attached_file_names = [f.get("original_filename", "unnamed") for f in files]
        session = Phase0BatchUploadSession(
            batch_upload_session_id=session_id,
            workspace_id=workspace_id,
            initiated_by_operator_id=operator_id,
            attached_file_names=attached_file_names,
            target_row_ids=target_row_ids,
            total_file_count=len(files),
            created_at_utc=datetime.now(timezone.utc),
        )
        self.batch_upload_sessions[session_id] = session

        attached_count = 0
        failed_count = 0
        row_attachment_counts: Dict[str, int] = {rid: 0 for rid in target_row_ids}
        unresolved_files: List[str] = []
        warnings: List[str] = []

        # Shared Namespace Law: organize directories under a structured path
        # Let's say d:\Work\The Conscious Coaching Factory\shared_workspace\campaigns\{coach_id}\intake\
        shared_workspace_root = os.path.join(
            "d:\\Work\\The Conscious Coaching Factory", "shared_workspace", "campaigns"
        )

        for file_info in files:
            filename = file_info.get("original_filename", "")
            media_kind = file_info.get("media_kind", "supporting_reference")
            size_bytes = file_info.get("file_size_bytes", 1024)

            # Heuristically determine which row gets the file (using targeted row IDs or filename prefix match)
            matched_row_id: Optional[str] = None

            # Look for explicit row target mapping, or prefix match (e.g. 'audrey_interview.mp3' matches row 'audrey')
            for rid in target_row_ids:
                packet = self.intake_service.get_prospect(rid)
                if packet:
                    clean_rid = rid.replace("pkt-", "").lower()
                    clean_prospect_id = packet.prospect_id.replace("p-", "").lower()
                    coach_id_sub = packet.coach_id.lower() if packet.coach_id else ""
                    display_sub = packet.display_name.lower().split()[0] if packet.display_name else ""
                    
                    if (
                        rid.lower() in filename.lower()
                        or clean_rid in filename.lower()
                        or (clean_prospect_id and clean_prospect_id in filename.lower())
                        or (coach_id_sub and coach_id_sub in filename.lower())
                        or (display_sub and display_sub in filename.lower())
                    ):
                        matched_row_id = rid
                        break

            if not matched_row_id and len(target_row_ids) == 1:
                matched_row_id = target_row_ids[0]

            if not matched_row_id:
                # F1. Upload Grouping Ambiguity: keep unresolved, do not guess silently
                unresolved_files.append(filename)
                warnings.append(f"Ambiguous file grouping for file: {filename}")
                failed_count += 1
                continue

            packet = self.intake_service.get_prospect(matched_row_id)
            if not packet:
                warnings.append(f"Target row record {matched_row_id} not found in intake")
                unresolved_files.append(filename)
                failed_count += 1
                continue

            # Compute namespaced storage path
            coach_folder = packet.coach_id or "unbound_coach"
            namespaced_path = os.path.join(
                shared_workspace_root, coach_folder, "intake", filename
            )

            # Stage / Register the media via Intake Service
            try:
                self.intake_service.attach_media(
                    prospect_id=matched_row_id,
                    media_kind=media_kind,
                    storage_uri=namespaced_path.replace("\\", "/"),
                    original_filename=filename,
                    file_size_bytes=size_bytes,
                    mime_type=file_info.get("mime_type"),
                    duration_seconds=file_info.get("duration_seconds"),
                )
                attached_count += 1
                row_attachment_counts[matched_row_id] += 1
            except Exception as exc:
                failed_count += 1
                warnings.append(f"Persistence error for {filename} on row {matched_row_id}: {str(exc)}")

        # Log Batch Upload Receipt Chain Stage
        self._rc.log(
            agent_id="phase0_campaign_workspace_service",
            action="PHASE0-BATCH-UPLOAD",
            asset_id=session_id,
            input_summary=f"Staged {len(files)} files for rows: {target_row_ids}",
            output_summary=f"Attached: {attached_count} | Failed/Unresolved: {failed_count}",
            decision="approved" if attached_count > 0 else "flagged",
            metadata={
                "session_id": session_id,
                "unresolved": unresolved_files,
                "warnings": warnings,
            },
        )

        session.completed_at_utc = datetime.now(timezone.utc)

        return Phase0BulkAttachmentResult(
            batch_upload_session_id=session_id,
            attached_count=attached_count,
            failed_count=failed_count,
            row_attachment_counts=row_attachment_counts,
            unresolved_files=unresolved_files,
            warnings=warnings,
        )

    def trigger_pipeline_execution(
        self,
        workspace_id: str,
        row_ids: List[str],
        operator_id: str,
    ) -> List[Phase0ExecutionRequest]:
        """
        AC6: Trigger the shared Phase-0 backend pipeline.
        AC7: Multi-select batch execution trigger.
        Logs a 'PHASE0-EXECUTION-TRIGGER' receipt.
        """
        if not row_ids:
            raise ValueError("Must select at least one row for execution trigger")

        # 1. Pre-validate ALL rows for readiness before starting any execution (Fail-closed)
        for row_id in row_ids:
            packet = self.intake_service.get_prospect(row_id)
            if not packet:
                raise ValueError(f"Prospect record {row_id} not found")

            # Validate readiness before trigger (F2/F6 constraints)
            readiness_summary = self.evaluate_readiness(row_id)
            if not readiness_summary.ready:
                # F2 / F6: block execution if unready
                self._rc.log(
                    agent_id="phase0_campaign_workspace_service",
                    action="PHASE0-EXECUTION-BLOCKED",
                    asset_id=row_id,
                    person_id=row_id,
                    input_summary=f"Attempt to execute row '{row_id}'",
                    output_summary="Blocked due to unready validation gates",
                    decision="rejected",
                )
                raise ValueError(f"EXECUTION_BLOCKED: Row {row_id} is not ready for pipeline trigger")

        execution_requests: List[Phase0ExecutionRequest] = []
        mode: Literal["SINGLE", "BATCH"] = "SINGLE" if len(row_ids) == 1 else "BATCH"

        for row_id in row_ids:
            packet = self.intake_service.get_prospect(row_id)
            # Packet and readiness are guaranteed valid by pre-validation loop

            # Create standard request object
            req_id = f"ERQ-{uuid.uuid4().hex[:8].upper()}"
            exec_req = Phase0ExecutionRequest(
                request_id=req_id,
                workspace_id=workspace_id,
                row_ids=[row_id],
                phase0_packet_ids=[packet.packet_id],
                triggered_by_operator_id=operator_id,
                execution_mode=mode,
                created_at_utc=datetime.now(timezone.utc),
            )
            self.execution_requests[req_id] = exec_req
            execution_requests.append(exec_req)

            # Generate Delivery Plan & Start run (reusing existing orchestrator)
            plan = self.delivery_orchestrator.create_plan(packet)
            run = self.delivery_orchestrator.start_run(plan)

            # Auto-run steps synchronously for Phase-0 pipeline trial
            # In real system, this runs async; here we simulate full step transitions until run is finalized/completed
            try:
                while True:
                    nxt = self.delivery_orchestrator.execute_next_step(run, packet)
                    if nxt is None:
                        break

                # Initialize local workspace state if workspace service has it
                try:
                    self.workspace_service.create_workspace(packet)
                except Exception:
                    pass  # Workspace record might already exist or be registered

            except Exception as exc:
                # F4. Backend Execution Trigger Failure: move to FAILED
                run.status = Phase0DeliveryRunStatus.FAILED
                run.failure_state = str(exc)

            # Log execution trigger receipt stage
            self._rc.log(
                agent_id="phase0_campaign_workspace_service",
                action="PHASE0-EXECUTION-TRIGGER",
                asset_id=run.delivery_run_id,
                person_id=row_id,
                input_summary=f"Trigger delivery pipeline for coach ID '{packet.coach_id}'",
                output_summary=f"Pipeline initialized: plan_id={plan.plan_id}, run_id={run.delivery_run_id}",
                decision="approved" if run.status != Phase0DeliveryRunStatus.FAILED else "rejected",
                metadata={"request_id": req_id, "mode": mode, "run_status": run.status.value},
            )

        return execution_requests

    def synthesize_rows(
        self,
        workspace_id: str,
        filter_state: Optional[Phase0WorkspaceFilterState] = None,
    ) -> List[Phase0CoachRow]:
        """Aggregate and synthesize dense rows from backend data sources."""
        rows: List[Phase0CoachRow] = []

        # Iterate over all prospects currently staged in intake
        for prospect_id, packet in self.intake_service.prospects.items():
            # Create binding object
            binding_state: Literal["PROVISIONAL", "RESOLVED", "INVALID"] = "RESOLVED"
            if not packet.coach_id or not packet.coach_id.strip():
                binding_state = "PROVISIONAL"
            elif len(packet.coach_id) < 3:
                binding_state = "INVALID"

            coach_acronym = packet.coach_id[:3].upper() if len(packet.coach_id) >= 3 else None

            coach_binding = Phase0CoachBinding(
                binding_id=f"BND-{prospect_id[:4].upper()}",
                provisional_label="Draft Row" if binding_state == "PROVISIONAL" else None,
                coach_id=packet.coach_id or "",
                coach_acronym=coach_acronym,
                binding_state=binding_state,
                created_at_utc=datetime.now(timezone.utc),
            )

            # Evaluate readiness
            readiness = self.evaluate_readiness(prospect_id)

            # Look up any active delivery runs
            active_run: Optional[Phase0DeliveryRun] = None
            for run in self.delivery_orchestrator.runs.values():
                plan = self.delivery_orchestrator.plans.get(run.plan_id)
                if plan and plan.phase0_packet_id == packet.packet_id:
                    active_run = run
                    break

            # Resolve Row State
            row_state: Literal[
                "DRAFT",
                "BOUND_UNREADY",
                "READY_TO_EXECUTE",
                "RUNNING",
                "REVIEW_REQUIRED",
                "DELIVERED_AWAITING_PAYMENT",
                "PAID_UNLOCKED",
                "UPGRADED",
                "FAILED",
            ] = "DRAFT"

            if binding_state == "PROVISIONAL":
                row_state = "DRAFT"
            elif not readiness.ready:
                row_state = "BOUND_UNREADY"
            elif not active_run:
                row_state = "READY_TO_EXECUTE"
            else:
                if active_run.status == Phase0DeliveryRunStatus.RUNNING:
                    row_state = "RUNNING"
                elif active_run.status in {
                    Phase0DeliveryRunStatus.COMPLETED,
                    Phase0DeliveryRunStatus.DEGRADED_READY,
                }:
                    ws_rec = next(
                        (
                            w
                            for w in self.workspace_service.workspaces.values()
                            if w.prospect_packet_id == packet.packet_id or w.prospect_id == packet.prospect_id
                        ),
                        None,
                    )
                    if ws_rec:
                        if ws_rec.status == Phase0WorkspaceStatus.PAYMENT_UNLOCKED:
                            row_state = "PAID_UNLOCKED"
                        elif ws_rec.status == Phase0WorkspaceStatus.UPGRADED:
                            row_state = "UPGRADED"
                        else:
                            row_state = "DELIVERED_AWAITING_PAYMENT"
                    else:
                        row_state = "DELIVERED_AWAITING_PAYMENT"
                elif active_run.status == Phase0DeliveryRunStatus.FAILED:
                    row_state = "FAILED"

            # F7. Payment State Not Yet Known
            payment_state_label = "PAYMENT_STATE_PENDING_SYNC"
            if row_state in {"DRAFT", "BOUND_UNREADY", "READY_TO_EXECUTE"}:
                payment_state_label = "NOT_APPLICABLE"
            elif row_state == "DELIVERED_AWAITING_PAYMENT":
                payment_state_label = "UNPAID"
            elif row_state == "PAID_UNLOCKED":
                payment_state_label = "PAID"
            elif row_state == "UPGRADED":
                payment_state_label = "UPGRADED"

            # One Primary Action Per Row State rule
            next_action = "Bind Coach ID"
            if row_state == "DRAFT":
                next_action = "Bind Coach ID"
            elif row_state == "BOUND_UNREADY":
                next_action = "Upload Missing Inputs"
            elif row_state == "READY_TO_EXECUTE":
                next_action = "Trigger shared execution pipeline"
            elif row_state == "RUNNING":
                next_action = "View running logs"
            elif row_state == "REVIEW_REQUIRED":
                next_action = "Operator review board"
            elif row_state == "DELIVERED_AWAITING_PAYMENT":
                next_action = "Send payment link"
            elif row_state == "PAID_UNLOCKED":
                next_action = "Initiate upgrade migration"
            elif row_state == "UPGRADED":
                next_action = "Archive workspace"
            elif row_state == "FAILED":
                next_action = "Retry execution pipeline"

            row = Phase0CoachRow(
                row_id=prospect_id,
                display_name=packet.display_name,
                coach_binding=coach_binding,
                row_state=row_state,
                readiness=readiness,
                phase0_packet_id=packet.packet_id,
                delivery_run_id=active_run.delivery_run_id if active_run else None,
                payment_state_label=payment_state_label,
                next_action=next_action,
                updated_at_utc=datetime.now(timezone.utc),
            )

            # Apply filters
            if filter_state:
                # 1. Readiness filter
                if filter_state.readiness_filter == "READY" and not readiness.ready:
                    continue
                if filter_state.readiness_filter == "BLOCKED" and readiness.ready:
                    continue

                # 2. Delivery filter
                if filter_state.delivery_filter == "RUNNING" and row_state != "RUNNING":
                    continue
                if filter_state.delivery_filter == "REVIEW" and row_state != "REVIEW_REQUIRED":
                    continue
                if filter_state.delivery_filter == "DELIVERED" and row_state not in {
                    "DELIVERED_AWAITING_PAYMENT",
                    "PAID_UNLOCKED",
                    "UPGRADED",
                }:
                    continue

                # 3. Payment filter
                if filter_state.payment_filter == "UNPAID" and payment_state_label != "UNPAID":
                    continue
                if filter_state.payment_filter == "PAID" and payment_state_label != "PAID":
                    continue
                if filter_state.payment_filter == "UPGRADED" and payment_state_label != "UPGRADED":
                    continue

                # 4. Search Query
                if filter_state.search_query.strip():
                    query = filter_state.search_query.lower()
                    if (
                        query not in row.display_name.lower()
                        and query not in coach_binding.coach_id.lower()
                    ):
                        continue

            rows.append(row)

        # Apply Sort Key
        if filter_state:
            if filter_state.sort_key == "NAME":
                rows.sort(key=lambda r: r.display_name)
            elif filter_state.sort_key == "READY_FIRST":
                rows.sort(key=lambda r: not r.readiness.ready)

        return rows

    def get_workspace_view(
        self,
        workspace_id: str,
        operator_id: str,
    ) -> Phase0CampaignWorkspace:
        """Fetch full campaign workspace payload."""
        workspace = self.get_or_create_campaign_workspace(workspace_id, operator_id)
        workspace.rows = self.synthesize_rows(workspace_id, workspace.filter_state)
        workspace.generated_at_utc = datetime.now(timezone.utc)
        return workspace

    def check_health(self, workspace_id: str) -> Phase0WorkspaceHealth:
        """Evaluate dependencies health status for operator visibility."""
        # Simple probe mocks
        return Phase0WorkspaceHealth(
            workspace_id=workspace_id,
            intake_api_ready=True,
            delivery_api_ready=True,
            commercial_api_ready=True,
            receipt_chain_ready=True,
            shared_storage_ready=True,
            checked_at_utc=datetime.now(timezone.utc),
        )
