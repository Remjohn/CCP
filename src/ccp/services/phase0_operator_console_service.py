"""
FR-ERA3-38 Phase-0 Operator Console and SLA Tracker Orchestration Service
==========================================================================
Aggregates downstream state trackers and registers operational receipt chains.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Literal

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_intake_models import Phase0ProspectPacket, Phase0ProspectStatus
from src.ccp.models.phase0_workspace_models import Phase0WorkspaceRecord, Phase0WorkspaceStatus
from src.ccp.models.phase0_delivery_models import Phase0DeliveryRun, Phase0DeliveryRunStatus, Phase0SequenceStepType
from src.ccp.models.phase0_commercial_models import Phase0CommercialState, FirstProofUnlockReceipt
from src.ccp.models.phase0_operator_console_models import (
    Phase0TopLevelState,
    Phase0AlertSeverity,
    Phase0EscalationLevel,
    Phase0RunStatus,
    Phase0SlaState,
    Phase0Alert,
    Phase0MissingInputState,
    Phase0EscalationState,
    Phase0OperatorQueueItem,
    Phase0OperatorQueueView,
    Phase0PackageDetailView,
)
from src.ccp.services.phase0_sla_tracker import Phase0SlaTracker


class Phase0OperatorConsoleService:
    """Consolidated state aggregator and recovery management service for Trial Phase-0."""

    def __init__(
        self,
        workspace_service: Optional[object] = None,
        delivery_orchestrator: Optional[object] = None,
        receipt_chain: Optional[ReceiptChain] = None,
        sla_tracker: Optional[Phase0SlaTracker] = None,
    ):
        self.workspace_service = workspace_service
        self.delivery_orchestrator = delivery_orchestrator
        self.receipt_chain = receipt_chain
        self.sla_tracker = sla_tracker or Phase0SlaTracker(receipt_chain=receipt_chain)

        # In-memory persistence stores for console-specific states
        self.missing_inputs: Dict[str, Phase0MissingInputState] = {}
        self.escalations: Dict[str, Phase0EscalationState] = {}
        self.alerts: Dict[str, Phase0Alert] = {}

    def resolve_top_level_state(
        self,
        workspace: Optional[Phase0WorkspaceRecord],
        delivery_run: Optional[Phase0DeliveryRun],
        commercial_state: Optional[Phase0CommercialState],
        unlock_receipt: Optional[FirstProofUnlockReceipt],
        prospect_packet: Optional[Phase0ProspectPacket],
    ) -> Phase0TopLevelState:
        """Translates low-level runtime statuses into a unified operator-ready state."""
        # 1. UPGRADED / HANDED OFF
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.UPGRADED:
            return Phase0TopLevelState.UPGRADED_HANDED_OFF
        
        # 2. PAID / UNLOCKED
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.PAYMENT_UNLOCKED:
            return Phase0TopLevelState.PAID_UNLOCKED
        if commercial_state is not None and commercial_state.phase0_unlock_paid:
            if unlock_receipt is not None and unlock_receipt.unlock_propagated:
                return Phase0TopLevelState.PAID_UNLOCKED

        # 3. DELIVERED / AWAITING PAYMENT
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.DELIVERED:
            return Phase0TopLevelState.DELIVERED_AWAITING_PAYMENT
        if delivery_run is not None and delivery_run.status == Phase0DeliveryRunStatus.COMPLETED:
            if commercial_state is None or not commercial_state.phase0_unlock_paid:
                return Phase0TopLevelState.DELIVERED_AWAITING_PAYMENT

        # 4. FAILED RUNS
        if delivery_run is not None and delivery_run.status in [
            Phase0DeliveryRunStatus.FAILED,
            Phase0DeliveryRunStatus.PARTIAL_FAILURE,
        ]:
            return Phase0TopLevelState.FAILED

        # 5. READY TO DELIVER
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.PREVIEW_READY:
            return Phase0TopLevelState.READY_TO_DELIVER
        if delivery_run is not None and delivery_run.status in [
            Phase0DeliveryRunStatus.READY,
            Phase0DeliveryRunStatus.DEGRADED_READY,
            Phase0DeliveryRunStatus.AWAITING_REVIEW,
        ]:
            return Phase0TopLevelState.READY_TO_DELIVER

        # 6. AUDIT IN PROGRESS
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.AUDIT_IN_PROGRESS:
            return Phase0TopLevelState.AUDIT_IN_PROGRESS
        if delivery_run is not None and delivery_run.current_step_id is not None:
            # Check if active step is audit_core or pdf_assembly
            for res in delivery_run.step_results:
                if res.step_id == delivery_run.current_step_id and res.status in ["PENDING", "RUNNING"]:
                    if "AUDIT" in res.step_id or "PDF" in res.step_id:
                        return Phase0TopLevelState.AUDIT_IN_PROGRESS

        # 7. ASSETS RENDERING
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.ARTIFACTS_COLLECTING:
            return Phase0TopLevelState.ASSETS_RENDERING
        if delivery_run is not None and delivery_run.status == Phase0DeliveryRunStatus.RUNNING:
            return Phase0TopLevelState.ASSETS_RENDERING

        # 8. BLOCKED ON VITAL INPUTS
        if workspace is not None and workspace.status == Phase0WorkspaceStatus.BLOCKED:
            return Phase0TopLevelState.BLOCKED_MISSING_INPUTS
        if prospect_packet is not None and prospect_packet.status == Phase0ProspectStatus.BLOCKED_MISSING_INPUTS:
            return Phase0TopLevelState.BLOCKED_MISSING_INPUTS

        # 9. NEW INTAKE / PLANNED DEFAULT
        return Phase0TopLevelState.NEW_INTAKE

    def resolve_next_action(self, top_state: Phase0TopLevelState) -> str:
        """Determines the single most urgent cognitive action for this package."""
        if top_state == Phase0TopLevelState.NEW_INTAKE:
            return "Initiate workspace audit run"
        elif top_state == Phase0TopLevelState.BLOCKED_MISSING_INPUTS:
            return "Request missing fields from prospect"
        elif top_state == Phase0TopLevelState.AUDIT_IN_PROGRESS:
            return "Monitor audit intelligence engine progress"
        elif top_state == Phase0TopLevelState.ASSETS_RENDERING:
            return "Monitor creative rendering queue"
        elif top_state == Phase0TopLevelState.READY_TO_DELIVER:
            return "Execute outreach package delivery handoff"
        elif top_state == Phase0TopLevelState.DELIVERED_AWAITING_PAYMENT:
            return "Awaiting Stripe/Telegram payment confirmation"
        elif top_state == Phase0TopLevelState.PAID_UNLOCKED:
            return "Execute container migration to target tier"
        elif top_state == Phase0TopLevelState.UPGRADED_HANDED_OFF:
            return "Workspace successfully upgraded and closed"
        elif top_state == Phase0TopLevelState.FAILED:
            return "Review run logs and trigger override retry"
        return "Review pipeline status"

    def synthesize_alerts_and_escalations(
        self,
        coach_id: str,
        packet_id: str,
        top_state: Phase0TopLevelState,
        sla_state: Phase0SlaState,
        delivery_run: Optional[Phase0DeliveryRun],
        unlock_receipt: Optional[FirstProofUnlockReceipt],
        prospect_packet: Optional[Phase0ProspectPacket],
    ) -> List[Phase0Alert]:
        """Scans current runtime packets to dynamically compile alerts and escalations."""
        synthesized: List[Phase0Alert] = []
        current_time = datetime.now(timezone.utc)

        def register_alert(alert: Phase0Alert):
            # Seek a matching existing alert to reuse the ID and keep its acknowledged status
            existing = next(
                (a for a in self.alerts.values()
                 if a.phase0_packet_id == alert.phase0_packet_id and a.alert_type == alert.alert_type),
                None
            )
            if existing:
                alert.alert_id = existing.alert_id
                if existing.acknowledged_at_utc is not None:
                    alert.acknowledged_at_utc = existing.acknowledged_at_utc
            self.alerts[alert.alert_id] = alert
            synthesized.append(alert)

        # 1. SLA Breach Alert
        if sla_state.breached:
            alert = Phase0Alert(
                alert_id=f"ALT-SLA-{packet_id}-{uuid.uuid4().hex[:4].upper()}",
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                severity=Phase0AlertSeverity.CRITICAL,
                alert_type="SLA_BREACH",
                title="SLA Deadline Breached",
                summary=f"SLA deadline was crossed by {abs(sla_state.minutes_remaining)} minutes.",
                recommended_action="Engage immediate emergency recovery",
                source_state_ref="sla_state",
                created_at_utc=current_time,
            )
            register_alert(alert)
            
            # Automatically scale escalation
            esc = Phase0EscalationState(
                escalation_id=f"ESC-SLA-{packet_id}",
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                escalation_level=Phase0EscalationLevel.MANAGER_ATTENTION,
                escalation_reason="24h delivery SLA completely breached.",
                linked_alert_ids=[alert.alert_id],
                active=True,
                created_at_utc=current_time,
            )
            self.escalations[esc.escalation_id] = esc

        # 2. SLA Risk Alert
        elif sla_state.risk_band in ["RED", "ORANGE"]:
            alert = Phase0Alert(
                alert_id=f"ALT-RISK-{packet_id}-{uuid.uuid4().hex[:4].upper()}",
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                severity=Phase0AlertSeverity.HIGH,
                alert_type="SLA_RISK",
                title="SLA At High Risk",
                summary=f"Package is in {sla_state.risk_band} band with only {sla_state.minutes_remaining} minutes left.",
                recommended_action="Expedite pipeline execution and review",
                source_state_ref="sla_state",
                created_at_utc=current_time,
            )
            register_alert(alert)
            
            esc = Phase0EscalationState(
                escalation_id=f"ESC-RISK-{packet_id}",
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                escalation_level=Phase0EscalationLevel.SAME_DAY_RECOVERY if sla_state.risk_band == "RED" else Phase0EscalationLevel.OPERATOR_REVIEW,
                escalation_reason="SLA window entering high risk zone.",
                linked_alert_ids=[alert.alert_id],
                active=True,
                created_at_utc=current_time,
            )
            self.escalations[esc.escalation_id] = esc

        # 3. Missing Inputs Alert
        if top_state == Phase0TopLevelState.BLOCKED_MISSING_INPUTS:
            missing_state = self.missing_inputs.get(packet_id)
            if missing_state is None:
                # Compile from packet or defaults
                missing_fields = []
                if prospect_packet and prospect_packet.missing_input_states:
                    missing_fields = [m.missing_code for m in prospect_packet.missing_input_states]
                else:
                    missing_fields = ["interview_audio", "target_audience_profile"]

                missing_state = Phase0MissingInputState(
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    missing_fields=missing_fields,
                    blocking=True,
                    last_request_sent_at_utc=None,
                    operator_note="Intake validation identified missing required parameters",
                    updated_at_utc=current_time,
                )
                self.missing_inputs[packet_id] = missing_state

            if missing_state.last_request_sent_at_utc is None:
                alert = Phase0Alert(
                    alert_id=f"ALT-MIA-NEW-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    severity=Phase0AlertSeverity.WARNING,
                    alert_type="MISSING_INPUT_NO_REQUEST",
                    title="Missing Vital Prospect Inputs",
                    summary=f"Blockers identified: {', '.join(missing_state.missing_fields)}. No request sent yet.",
                    recommended_action="Trigger immediate in-chat input request to prospect",
                    source_state_ref="missing_input_state",
                    created_at_utc=current_time,
                )
                register_alert(alert)
            else:
                elapsed_hours = (current_time - missing_state.last_request_sent_at_utc).total_seconds() / 3600.0
                if elapsed_hours >= 4.0:
                    alert = Phase0Alert(
                        alert_id=f"ALT-MIA-STALE-{packet_id}",
                        coach_id=coach_id,
                        phase0_packet_id=packet_id,
                        severity=Phase0AlertSeverity.HIGH,
                        alert_type="MISSING_INPUT_STALE",
                        title="Stale Input Request",
                        summary=f"Handoff blocked on inputs for {elapsed_hours:.1f} hours since request.",
                        recommended_action="Trigger telephone/escalated manual outreach",
                        source_state_ref="missing_input_state",
                        created_at_utc=current_time,
                    )
                    register_alert(alert)

                    esc = Phase0EscalationState(
                        escalation_id=f"ESC-MIA-{packet_id}",
                        coach_id=coach_id,
                        phase0_packet_id=packet_id,
                        escalation_level=Phase0EscalationLevel.OPERATOR_REVIEW,
                        escalation_reason="Prospect has not responded to vital input request within 4h.",
                        linked_alert_ids=[alert.alert_id],
                        active=True,
                        created_at_utc=current_time,
                    )
                    self.escalations[esc.escalation_id] = esc

        # 4. Stuck Run Alert (stale in RUNNING/ASSETS_RENDERING > 2 hours)
        if delivery_run is not None and delivery_run.status == Phase0DeliveryRunStatus.RUNNING:
            started_at = delivery_run.started_at_utc or current_time
            # Try to get the last step updated_at or receipt time
            last_activity = started_at
            if delivery_run.receipts:
                last_activity = max(r.completed_at_utc or started_at for r in delivery_run.receipts)
            
            # If no activity in > 2 hours, flag as stuck run
            stale_seconds = (current_time - last_activity).total_seconds()
            if stale_seconds > 7200.0:
                alert = Phase0Alert(
                    alert_id=f"ALT-STUCK-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    severity=Phase0AlertSeverity.HIGH,
                    alert_type="STUCK_RUN",
                    title="Stuck Generation Pipeline",
                    summary=f"No run progress or receipt events updated for {stale_seconds/3600:.1f} hours.",
                    recommended_action="Trigger manual force-retry or override pipeline",
                    source_state_ref="delivery_run",
                    created_at_utc=current_time,
                )
                register_alert(alert)

                esc = Phase0EscalationState(
                    escalation_id=f"ESC-STUCK-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    escalation_level=Phase0EscalationLevel.SAME_DAY_RECOVERY,
                    escalation_reason="Stuck active render or audit step exceeded 2h latency barrier.",
                    linked_alert_ids=[alert.alert_id],
                    active=True,
                    created_at_utc=current_time,
                )
                self.escalations[esc.escalation_id] = esc

        # 5. Unlock Propagation Failure
        if unlock_receipt is not None and unlock_receipt.payment_status == "PAYMENT_SUCCESSFUL":
            if not unlock_receipt.unlock_propagated:
                alert = Phase0Alert(
                    alert_id=f"ALT-PROP-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    severity=Phase0AlertSeverity.CRITICAL,
                    alert_type="UNLOCK_PROPAGATION_FAILURE",
                    title="Unlock Propagation Failure",
                    summary="Stripe payment successful but downstream artifact lock release failed.",
                    recommended_action="Manually unlock artifacts and clear delivery gates",
                    source_state_ref="unlock_receipt",
                    created_at_utc=current_time,
                )
                register_alert(alert)

                esc = Phase0EscalationState(
                    escalation_id=f"ESC-PROP-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    escalation_level=Phase0EscalationLevel.MANUAL_OVERRIDE_REQUIRED,
                    escalation_reason="Payment unlock failed to auto-propagate to workspace state.",
                    linked_alert_ids=[alert.alert_id],
                    active=True,
                    created_at_utc=current_time,
                )
                self.escalations[esc.escalation_id] = esc

        return synthesized

    def get_operator_queue_view(
        self,
        workspace_id: str,
        packets: List[Phase0ProspectPacket],
    ) -> Phase0OperatorQueueView:
        """Sweeps and aggregates a collection of packets into a single console matrix view."""
        current_time = datetime.now(timezone.utc)
        items: List[Phase0OperatorQueueItem] = []

        green = yellow = orange = red = breached = 0

        # Build list of active targets
        for pkt in packets:
            coach_id = pkt.coach_id or "P0W"
            packet_id = pkt.packet_id

            # Query downstream systems
            workspace = None
            if self.workspace_service is not None:
                # Attempt lookup in service workspaces
                workspace = next((w for w in getattr(self.workspace_service, "workspaces", {}).values() if w.prospect_packet_id == packet_id), None)
            
            delivery_run = None
            if self.delivery_orchestrator is not None:
                delivery_run = next((r for r in getattr(self.delivery_orchestrator, "runs", {}).values() if r.phase0_packet_id == packet_id), None)

            commercial_state = None
            # Retrieve or build a commercial state lookup
            if workspace is not None and self.workspace_service is not None:
                bridges = getattr(self.workspace_service, "upgrade_bridges", {})
                matching_bridge = next((b for b in bridges.values() if b.workspace_id == workspace.workspace_id), None)
                if matching_bridge:
                    commercial_state = Phase0CommercialState(
                        commercial_state_id=f"CS-{packet_id}",
                        coach_id=coach_id,
                        phase0_packet_id=packet_id,
                        delivery_run_id=delivery_run.delivery_run_id if delivery_run else "RUN-NONE",
                        phase0_unlock_paid=matching_bridge.payment_confirmed,
                        upgrade_credit_available=matching_bridge.payment_confirmed,
                        updated_at_utc=current_time,
                    )

            unlock_receipt = None
            if commercial_state is not None and commercial_state.phase0_unlock_paid:
                unlock_receipt = FirstProofUnlockReceipt(
                    receipt_id=f"RCPT-UNLOCK-{packet_id}",
                    request_id=f"REQ-UNLOCK-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    payment_status="PAYMENT_SUCCESSFUL",
                    unlock_propagated=(workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED]),
                    created_at_utc=current_time,
                    completed_at_utc=current_time,
                )

            # SLA Timeline status
            started_at = current_time - timezone_offset_hours(2.0)
            if workspace is not None:
                started_at = datetime.fromisoformat(workspace.created_at)

            # Retrieve active or generate new SLA tracking state
            sla_state = self.sla_tracker.start_tracking(
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                sla_started_at_utc=started_at,
                based_on_run_id=delivery_run.delivery_run_id if delivery_run else None,
            )
            # Update values
            sla_state = self.sla_tracker.update_sla_status(sla_state, current_time=current_time)

            # Resolve state enums
            top_level_state = self.resolve_top_level_state(
                workspace, delivery_run, commercial_state, unlock_receipt, pkt
            )

            next_action = self.resolve_next_action(top_level_state)

            # Synthesize alerts
            alerts_list = self.synthesize_alerts_and_escalations(
                coach_id, packet_id, top_level_state, sla_state, delivery_run, unlock_receipt, pkt
            )
            
            # Count alerts
            active_alerts = [a for a in alerts_list if a.acknowledged_at_utc is None]
            alert_count = len(active_alerts)
            highest_sev = None
            if active_alerts:
                severities_ord = {"INFO": 0, "WARNING": 1, "HIGH": 2, "CRITICAL": 3}
                sorted_alerts = sorted(active_alerts, key=lambda a: severities_ord[a.severity.value], reverse=True)
                highest_sev = sorted_alerts[0].severity

            # Tally color bands
            risk = sla_state.risk_band
            if risk == "GREEN":
                green += 1
            elif risk == "YELLOW":
                yellow += 1
            elif risk == "ORANGE":
                orange += 1
            elif risk == "RED":
                red += 1
            elif risk == "BREACHED":
                breached += 1

            # Compile payment labels (Surfacing $29.99, $39.99, $99.99 tier parameters)
            payment_label = "Unpaid (Pending $29.99 Proof Unlock)"
            if commercial_state and commercial_state.phase0_unlock_paid:
                payment_label = "Paid ($29.99 Phase-0 Proof Unlocked)"
            elif workspace and workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED]:
                payment_label = "Paid ($29.99 Phase-0 Proof Unlocked)"

            upgrade_label = "Eligible for upgrade credits"
            if workspace and workspace.status == Phase0WorkspaceStatus.UPGRADED:
                if commercial_state and commercial_state.upgrade_credit_consumed:
                    tier_str = "Coach OS ($99.99/mo)"
                    if workspace.display_name.find("Speaking") != -1:
                        tier_str = "Speaking & Learning ($39.99/mo)"
                    upgrade_label = f"Upgraded to {tier_str}"
                else:
                    upgrade_label = "Upgraded to Speaking & Learning ($39.99/mo)"

            run_status = Phase0RunStatus(
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                delivery_run_id=delivery_run.delivery_run_id if delivery_run else None,
                top_level_state=top_level_state,
                intake_ready=(pkt.status != Phase0ProspectStatus.BLOCKED_MISSING_INPUTS),
                audit_ready=(workspace.status not in [Phase0WorkspaceStatus.CREATED, Phase0WorkspaceStatus.INTAKE_RECEIVED] if workspace else False),
                render_ready=(delivery_run.status == Phase0DeliveryRunStatus.COMPLETED if delivery_run else False),
                review_required=(delivery_run.review_state == "REQUIRED" if delivery_run else False),
                delivered=(workspace.status in [Phase0WorkspaceStatus.DELIVERED, Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED] if workspace else False),
                payment_completed=(workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED] if workspace else False),
                unlock_propagated=(workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED] if workspace else False),
                updated_at_utc=current_time,
            )

            item = Phase0OperatorQueueItem(
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                display_name=pkt.display_name,
                run_status=run_status,
                sla_state=sla_state,
                active_alert_count=alert_count,
                highest_alert_severity=highest_sev,
                next_action=next_action,
                payment_state_label=payment_label,
                upgrade_state_label=upgrade_label,
            )
            items.append(item)

        # Sort queue: breached and critical items float above green / on-time ones
        def sort_priority(item: Phase0OperatorQueueItem) -> int:
            sla_ord = {"BREACHED": 0, "RED": 1, "ORANGE": 2, "YELLOW": 3, "GREEN": 4}
            return sla_ord[item.sla_state.risk_band]

        items.sort(key=sort_priority)

        view = Phase0OperatorQueueView(
            workspace_id=workspace_id,
            generated_at_utc=current_time,
            total_active_packages=len(items),
            green_count=green,
            yellow_count=yellow,
            orange_count=orange,
            red_count=red,
            breached_count=breached,
            items=items,
        )

        if self.receipt_chain is not None:
            self.receipt_chain.log(
                action="PHASE0-CONSOLE-AGGREGATE",
                coach_acronym="P0W",
                payload={
                    "total_active": len(items),
                    "green": green,
                    "yellow": yellow,
                    "orange": orange,
                    "red": red,
                    "breached": breached,
                },
            )

        return view

    def get_package_detail_view(
        self,
        coach_id: str,
        packet_id: str,
        packet: Phase0ProspectPacket,
    ) -> Phase0PackageDetailView:
        """Assembles a deep-dive operational inspection perspective for a package."""
        current_time = datetime.now(timezone.utc)

        workspace = None
        if self.workspace_service is not None:
            workspace = next((w for w in getattr(self.workspace_service, "workspaces", {}).values() if w.prospect_packet_id == packet_id), None)
        
        delivery_run = None
        if self.delivery_orchestrator is not None:
            delivery_run = next((r for r in getattr(self.delivery_orchestrator, "runs", {}).values() if r.phase0_packet_id == packet_id), None)

        commercial_state = None
        if workspace is not None and self.workspace_service is not None:
            bridges = getattr(self.workspace_service, "upgrade_bridges", {})
            matching_bridge = next((b for b in bridges.values() if b.workspace_id == workspace.workspace_id), None)
            if matching_bridge:
                commercial_state = Phase0CommercialState(
                    commercial_state_id=f"CS-{packet_id}",
                    coach_id=coach_id,
                    phase0_packet_id=packet_id,
                    delivery_run_id=delivery_run.delivery_run_id if delivery_run else "RUN-NONE",
                    phase0_unlock_paid=matching_bridge.payment_confirmed,
                    upgrade_credit_available=matching_bridge.payment_confirmed,
                    updated_at_utc=current_time,
                )

        unlock_receipt = None
        if commercial_state is not None and commercial_state.phase0_unlock_paid:
            unlock_receipt = FirstProofUnlockReceipt(
                receipt_id=f"RCPT-UNLOCK-{packet_id}",
                request_id=f"REQ-UNLOCK-{packet_id}",
                coach_id=coach_id,
                phase0_packet_id=packet_id,
                payment_status="PAYMENT_SUCCESSFUL",
                unlock_propagated=(workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED]),
                created_at_utc=current_time,
                completed_at_utc=current_time,
            )

        started_at = current_time - timezone_offset_hours(2.0)
        if workspace is not None:
            started_at = datetime.fromisoformat(workspace.created_at)

        sla_state = self.sla_tracker.start_tracking(
            coach_id=coach_id,
            phase0_packet_id=packet_id,
            sla_started_at_utc=started_at,
            based_on_run_id=delivery_run.delivery_run_id if delivery_run else None,
        )
        sla_state = self.sla_tracker.update_sla_status(sla_state, current_time=current_time)

        top_level_state = self.resolve_top_level_state(
            workspace, delivery_run, commercial_state, unlock_receipt, packet
        )

        run_status = Phase0RunStatus(
            coach_id=coach_id,
            phase0_packet_id=packet_id,
            delivery_run_id=delivery_run.delivery_run_id if delivery_run else None,
            top_level_state=top_level_state,
            intake_ready=(packet.status != Phase0ProspectStatus.BLOCKED_MISSING_INPUTS),
            audit_ready=(workspace.status not in [Phase0WorkspaceStatus.CREATED, Phase0WorkspaceStatus.INTAKE_RECEIVED] if workspace else False),
            render_ready=(delivery_run.status == Phase0DeliveryRunStatus.COMPLETED if delivery_run else False),
            review_required=(delivery_run.review_state == "REQUIRED" if delivery_run else False),
            delivered=(workspace.status in [Phase0WorkspaceStatus.DELIVERED, Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED] if workspace else False),
            payment_completed=(workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED] if workspace else False),
            unlock_propagated=(workspace.status in [Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.UPGRADED] if workspace else False),
            updated_at_utc=current_time,
        )

        # Synthesize fresh alerts and escalations for this package
        self.synthesize_alerts_and_escalations(
            coach_id=coach_id,
            packet_id=packet_id,
            top_state=top_level_state,
            sla_state=sla_state,
            delivery_run=delivery_run,
            unlock_receipt=unlock_receipt,
            prospect_packet=packet,
        )

        missing_state = self.missing_inputs.get(packet_id)
        esc_state = self.escalations.get(f"ESC-SLA-{packet_id}") or self.escalations.get(f"ESC-RISK-{packet_id}") or self.escalations.get(f"ESC-MIA-{packet_id}") or self.escalations.get(f"ESC-STUCK-{packet_id}") or self.escalations.get(f"ESC-PROP-{packet_id}")

        alerts_list = [a for a in self.alerts.values() if a.phase0_packet_id == packet_id and a.acknowledged_at_utc is None]

        # Gather receipt IDs
        receipt_ids = []
        if delivery_run and delivery_run.receipts:
            receipt_ids = [r.receipt_id for r in delivery_run.receipts]

        primary_action = None
        if top_level_state == Phase0TopLevelState.READY_TO_DELIVER:
            primary_action = "DELIVER_NOW"
        elif top_level_state == Phase0TopLevelState.PAID_UNLOCKED:
            primary_action = "MIGRATE_CONTAINER"

        return Phase0PackageDetailView(
            coach_id=coach_id,
            phase0_packet_id=packet_id,
            run_status=run_status,
            sla_state=sla_state,
            missing_input_state=missing_state,
            escalation_state=esc_state,
            alerts=alerts_list,
            receipt_ids=receipt_ids,
            primary_review_action=primary_action,
        )

    def acknowledge_alert(self, alert_id: str, operator_id: str) -> bool:
        """Marks an alert as acknowledged by the active console operator."""
        alert = self.alerts.get(alert_id)
        if not alert:
            return False

        current_time = datetime.now(timezone.utc)
        alert.acknowledged_at_utc = current_time

        if self.receipt_chain is not None:
            self.receipt_chain.log(
                action="PHASE0-CONSOLE-ACTION-EXEC",
                coach_acronym=alert.coach_id[:3].upper() if len(alert.coach_id) >= 3 else "P0W",
                payload={
                    "action_type": "acknowledge_alert",
                    "alert_id": alert_id,
                    "operator_id": operator_id,
                    "timestamp": current_time.isoformat(),
                },
            )

        return True

    def trigger_retry(self, coach_id: str, packet_id: str, operator_id: str) -> bool:
        """Initiates an operational pipeline override/retry after recovery from a failed state."""
        current_time = datetime.now(timezone.utc)
        
        # In reality, this endpoint talks to DeliveryOrchestrator to start a new execution plan
        if self.receipt_chain is not None:
            self.receipt_chain.log(
                action="PHASE0-CONSOLE-ACTION-EXEC",
                coach_acronym=coach_id[:3].upper() if len(coach_id) >= 3 else "P0W",
                payload={
                    "action_type": "pipeline_force_retry",
                    "phase0_packet_id": packet_id,
                    "operator_id": operator_id,
                    "timestamp": current_time.isoformat(),
                },
            )
        
        # Clear stuck runs or failed state markers
        stuck_esc_key = f"ESC-STUCK-{packet_id}"
        if stuck_esc_key in self.escalations:
            self.escalations[stuck_esc_key].active = False
            self.escalations[stuck_esc_key].resolved_at_utc = current_time

        return True

    def trigger_escalation(
        self,
        coach_id: str,
        packet_id: str,
        level: Phase0EscalationLevel,
        reason: str,
        operator_id: str,
    ) -> Phase0EscalationState:
        """Manually raises the escalation severity profile of a package."""
        current_time = datetime.now(timezone.utc)
        esc_id = f"ESC-MAN-{packet_id}-{uuid.uuid4().hex[:4].upper()}"
        
        esc = Phase0EscalationState(
            escalation_id=esc_id,
            coach_id=coach_id,
            phase0_packet_id=packet_id,
            escalation_level=level,
            escalation_reason=reason,
            linked_alert_ids=[],
            active=True,
            created_at_utc=current_time,
        )
        self.escalations[esc_id] = esc

        if self.receipt_chain is not None:
            self.receipt_chain.log(
                action="PHASE0-CONSOLE-ACTION-EXEC",
                coach_acronym=coach_id[:3].upper() if len(coach_id) >= 3 else "P0W",
                payload={
                    "action_type": "manual_escalation_raise",
                    "escalation_id": esc_id,
                    "level": level.value,
                    "reason": reason,
                    "operator_id": operator_id,
                    "timestamp": current_time.isoformat(),
                },
            )

        return esc


def timezone_offset_hours(hours: float) -> timezone | datetime.timedelta:
    """Helper to return time offsets cleanly."""
    import datetime as dt
    return dt.timedelta(hours=hours)
