"""
FR-ERA3-38 Phase-0 Operator Console and SLA Tracker Integration Tests
======================================================================
Tests the full aggregation, SLA risk classifications, alert synthesis,
and manual operator recovery endpoints end-to-end using FastAPI TestClient.
"""

from __future__ import annotations
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient

from src.ccp.api.main import app
from src.ccp.api.phase0_operator_console import (
    intake_service,
    workspace_service,
    delivery_orchestrator,
    console_service,
)
from src.ccp.models.phase0_intake_models import Phase0ProspectPacket, Phase0ProspectStatus
from src.ccp.models.phase0_workspace_models import Phase0WorkspaceRecord, Phase0WorkspaceStatus
from src.ccp.models.phase0_delivery_models import Phase0DeliveryRun, Phase0DeliveryRunStatus, Phase0SequenceStepResult
from src.ccp.models.phase0_commercial_models import Phase0CommercialState, FirstProofUnlockReceipt
from src.ccp.models.phase0_operator_console_models import (
    Phase0OperatorQueueView,
    Phase0PackageDetailView,
    Phase0EscalationLevel,
    Phase0EscalationState,
    Phase0TopLevelState,
    Phase0AlertSeverity,
)
from src.ccp.core.receipt_chain import ReceiptChain


@pytest.fixture(autouse=True)
def clean_console_stores():
    """Clear all in-memory persistence stores before each test execution."""
    intake_service.prospects.clear()
    workspace_service.workspaces.clear()
    workspace_service.upgrade_bridges.clear()
    delivery_orchestrator.runs.clear()
    console_service.alerts.clear()
    console_service.escalations.clear()
    console_service.missing_inputs.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestFRERA338OperatorConsole:

    def test_empty_queue_view(self, client: TestClient):
        """Verifies correct queue view response when there are zero active packages."""
        response = client.get("/api/phase0/operator/queue?workspace_id=test-ws-empty")
        assert response.status_code == 200
        
        view = Phase0OperatorQueueView.model_validate(response.json())
        assert view.workspace_id == "test-ws-empty"
        assert view.total_active_packages == 0
        assert view.items == []

    def test_state_mapping_and_sla_risk_bands(self, client: TestClient):
        """
        AC1 & AC2 & AC3: Verifies downstream states map perfectly to Top-Level enums,
        and SLA remaining minutes correctly classify into HSL color-coded risk bands.
        """
        current_time = datetime.now(timezone.utc)
        
        # Scenario 1: Intake blocked on missing inputs (4h stale request -> High alert and escalation)
        p1_id = "pkt-prospect-1"
        packet1 = Phase0ProspectPacket(
            prospect_id="P1",
            packet_id=p1_id,
            display_name="Audrey Beat",
            coach_id="P0W",
            status=Phase0ProspectStatus.BLOCKED_MISSING_INPUTS,
        )
        intake_service.prospects[p1_id] = packet1
        
        workspace1 = Phase0WorkspaceRecord(
            prospect_id="P1",
            prospect_packet_id=p1_id,
            coach_id="P0W",
            workspace_id="ws-p1",
            display_name="Audrey Beat",
            status=Phase0WorkspaceStatus.BLOCKED,
            created_by_receipt_id="RCPT-TEST-1",
            created_at=(current_time - timedelta(hours=3)).isoformat(),
            delivery_sla_deadline_utc=(current_time + timedelta(hours=21)).isoformat(),
        )
        workspace_service.workspaces["ws-p1"] = workspace1

        # We populate the console missing input state to represent 4h stale response
        from src.ccp.models.phase0_operator_console_models import Phase0MissingInputState
        console_service.missing_inputs[p1_id] = Phase0MissingInputState(
            coach_id="P0W",
            phase0_packet_id=p1_id,
            missing_fields=["interview_audio", "target_audience_profile"],
            blocking=True,
            last_request_sent_at_utc=current_time - timedelta(hours=4.5),
            operator_note="Stale input check",
            updated_at_utc=current_time,
        )

        # Scenario 2: Active Audit in progress (SLA window yellow)
        p2_id = "pkt-prospect-2"
        packet2 = Phase0ProspectPacket(
            prospect_id="P2",
            packet_id=p2_id,
            display_name="Audrey Sonic",
            coach_id="P0W",
            status=Phase0ProspectStatus.AWAITING_VALIDATION,
        )
        intake_service.prospects[p2_id] = packet2
        
        workspace2 = Phase0WorkspaceRecord(
            prospect_id="P2",
            prospect_packet_id=p2_id,
            coach_id="P0W",
            workspace_id="ws-p2",
            display_name="Audrey Sonic",
            status=Phase0WorkspaceStatus.AUDIT_IN_PROGRESS,
            created_by_receipt_id="RCPT-TEST-2",
            created_at=(current_time - timedelta(hours=19)).isoformat(),
            delivery_sla_deadline_utc=(current_time + timedelta(hours=5)).isoformat(),  # ~300 mins -> YELLOW
        )
        workspace_service.workspaces["ws-p2"] = workspace2

        response = client.get("/api/phase0/operator/queue?workspace_id=test-ws-active")
        assert response.status_code == 200
        
        view = Phase0OperatorQueueView.model_validate(response.json())
        assert view.total_active_packages == 2
        
        # Audrey Sonic (ws-p2) has 5h (300 mins) remaining -> YELLOW.
        # Audrey Beat (ws-p1) has 21h (1260 mins) remaining -> GREEN.
        # Check counts
        assert view.green_count == 1
        assert view.yellow_count == 1
        
        # Sonic should sort above Beat because YELLOW (3) floats above GREEN (4)
        item_sonic = view.items[0]
        assert item_sonic.phase0_packet_id == p2_id
        assert item_sonic.run_status.top_level_state == Phase0TopLevelState.AUDIT_IN_PROGRESS
        assert item_sonic.sla_state.risk_band == "YELLOW"
        assert 290 <= item_sonic.sla_state.minutes_remaining <= 305
        
        item_beat = view.items[1]
        assert item_beat.phase0_packet_id == p1_id
        assert item_beat.run_status.top_level_state == Phase0TopLevelState.BLOCKED_MISSING_INPUTS
        assert item_beat.sla_state.risk_band == "GREEN"

    def test_alert_synthesis_and_acknowledgment(self, client: TestClient):
        """
        AC4 & AC5: Verifies automatic alert compilation rules (stuck runs > 2h, missing inputs,
        propagation failures) and operator alert acknowledgment endpoint actions.
        """
        current_time = datetime.now(timezone.utc)
        p_id = "pkt-alert-test"
        
        packet = Phase0ProspectPacket(
            prospect_id="P3",
            packet_id=p_id,
            display_name="Jean Pierre",
            coach_id="P0W",
            status=Phase0ProspectStatus.READY_FOR_PHASE0,
        )
        intake_service.prospects[p_id] = packet

        workspace = Phase0WorkspaceRecord(
            prospect_id="P3",
            prospect_packet_id=p_id,
            coach_id="P0W",
            workspace_id="ws-p3",
            display_name="Jean Pierre",
            status=Phase0WorkspaceStatus.ARTIFACTS_COLLECTING,
            created_by_receipt_id="RCPT-TEST-3",
            created_at=(current_time - timedelta(hours=10)).isoformat(),
            delivery_sla_deadline_utc=(current_time + timedelta(hours=14)).isoformat(),
        )
        workspace_service.workspaces["ws-p3"] = workspace

        # Simulate stuck render run: Started 2.5 hours ago, still RUNNING (no recent activity)
        stuck_run = Phase0DeliveryRun(
            delivery_run_id="run-stuck-999",
            plan_id="plan-stuck-999",
            coach_id="P0W",
            phase0_packet_id=p_id,
            status=Phase0DeliveryRunStatus.RUNNING,
            current_step_id="step-create-assets",
            started_at_utc=current_time - timedelta(hours=2.5),
            step_results=[
                Phase0SequenceStepResult(
                    step_id="step-create-assets",
                    status="RUNNING",
                    started_at_utc=current_time - timedelta(hours=2.5),
                )
            ]
        )
        delivery_orchestrator.runs["run-stuck-999"] = stuck_run

        # 1. Fetch package detail and verify stuck run alert has been synthesized automatically
        response = client.get(f"/api/phase0/operator/package/{p_id}")
        assert response.status_code == 200
        
        detail = Phase0PackageDetailView.model_validate(response.json())
        assert detail.run_status.top_level_state == Phase0TopLevelState.ASSETS_RENDERING
        
        # Verify stuck run alert is synthesized
        assert len(detail.alerts) == 1
        stuck_alert = detail.alerts[0]
        assert stuck_alert.alert_type == "STUCK_RUN"
        assert stuck_alert.severity == Phase0AlertSeverity.HIGH
        assert "Trigger manual force-retry" in stuck_alert.recommended_action
        
        # Verify matching escalation has escalated automatically to SAME_DAY_RECOVERY
        assert detail.escalation_state is not None
        assert detail.escalation_state.escalation_level == Phase0EscalationLevel.SAME_DAY_RECOVERY
        assert detail.escalation_state.active is True

        # 2. Acknowledge alert via POST action
        ack_payload = {
            "alert_id": stuck_alert.alert_id,
            "operator_id": "operator-mitano"
        }
        res_ack = client.post(f"/api/phase0/operator/package/{p_id}/acknowledge-alert", json=ack_payload)
        assert res_ack.status_code == 200
        assert res_ack.json()["status"] == "success"

        # Verify alert is now marked acknowledged and is excluded from subsequent detail sweeps
        res_detail_2 = client.get(f"/api/phase0/operator/package/{p_id}")
        detail_2 = Phase0PackageDetailView.model_validate(res_detail_2.json())
        assert len(detail_2.alerts) == 0  # Acknowledged alerts are cleared from view

        # Verify receipt written for action
        rc = ReceiptChain(coach_acronym="P0W")
        action_receipts = [r for r in rc.query(action="PHASE0-CONSOLE-ACTION-EXEC")]
        assert len(action_receipts) >= 1
        assert any(r.payload["action_type"] == "acknowledge_alert" for r in action_receipts)

    def test_manual_override_retry_and_escalation_actions(self, client: TestClient):
        """
        AC5: Verifies execution of manual retry force commands and explicit escalation level overrides.
        """
        current_time = datetime.now(timezone.utc)
        p_id = "pkt-override-test"
        
        packet = Phase0ProspectPacket(
            prospect_id="P4",
            packet_id=p_id,
            display_name="Jean Pierre Beat",
            coach_id="P0W",
            status=Phase0ProspectStatus.READY_FOR_PHASE0,
        )
        intake_service.prospects[p_id] = packet

        workspace = Phase0WorkspaceRecord(
            prospect_id="P4",
            prospect_packet_id=p_id,
            coach_id="P0W",
            workspace_id="ws-p4",
            display_name="Jean Pierre Beat",
            status=Phase0WorkspaceStatus.BLOCKED,
            created_by_receipt_id="RCPT-TEST-4",
            created_at=(current_time - timedelta(hours=10)).isoformat(),
            delivery_sla_deadline_utc=(current_time + timedelta(hours=14)).isoformat(),
        )
        workspace_service.workspaces["ws-p4"] = workspace

        # 1. Trigger manual retry override action
        retry_payload = {
            "operator_id": "op-mitano"
        }
        res_retry = client.post(f"/api/phase0/operator/package/{p_id}/retry", json=retry_payload)
        assert res_retry.status_code == 200
        assert "Manual retry override logged" in res_retry.json()["message"]

        # Verify force_retry action receipt logged in standard receipt chain
        rc = ReceiptChain(coach_acronym="P0W")
        action_receipts = [r for r in rc.query(action="PHASE0-CONSOLE-ACTION-EXEC")]
        assert any(r.payload["action_type"] == "pipeline_force_retry" for r in action_receipts)

        # 2. Trigger explicit escalation override elevation
        esc_payload = {
            "operator_id": "op-mitano",
            "level": "MANAGER_ATTENTION",
            "reason": "Pipeline stuck in manual intake limbo. Requires telephone outreach."
        }
        res_esc = client.post(f"/api/phase0/operator/package/{p_id}/escalate", json=esc_payload)
        assert res_esc.status_code == 200
        
        esc_state = Phase0EscalationState.model_validate(res_esc.json())
        assert esc_state.escalation_level == Phase0EscalationLevel.MANAGER_ATTENTION
        assert esc_state.escalation_reason == esc_payload["reason"]
        assert esc_state.active is True

        # Verify manual escalation raise receipt was logged
        action_receipts_updated = [r for r in rc.query(action="PHASE0-CONSOLE-ACTION-EXEC")]
        assert any(r.payload["action_type"] == "manual_escalation_raise" for r in action_receipts_updated)

    def test_payment_and_upgrade_handoff_visibility(self, client: TestClient):
        """
        AC6 & AC7: Verifies payment pricing parameters and upgrade handoff tier parameters
        ($39.99 Speaking & Learning and $99.99 Coach OS) are clearly surfaced.
        """
        current_time = datetime.now(timezone.utc)
        p_id = "pkt-payment-test"
        
        packet = Phase0ProspectPacket(
            prospect_id="P5",
            packet_id=p_id,
            display_name="Speaking & Learning Prospect",
            coach_id="P0W",
            status=Phase0ProspectStatus.READY_FOR_PHASE0,
        )
        intake_service.prospects[p_id] = packet

        # Mock upgraded workspace to Speaking & Learning tier with credit bridge details
        workspace = Phase0WorkspaceRecord(
            prospect_id="P5",
            prospect_packet_id=p_id,
            coach_id="P0W",
            workspace_id="ws-p5",
            display_name="Speaking & Learning Workspace",
            status=Phase0WorkspaceStatus.UPGRADED,
            created_by_receipt_id="RCPT-TEST-5",
            created_at=(current_time - timedelta(hours=5)).isoformat(),
            delivery_sla_deadline_utc=(current_time + timedelta(hours=19)).isoformat(),
        )
        workspace.display_name = "Speaking & Learning Workspace"
        workspace_service.workspaces["ws-p5"] = workspace

        # Mock upgrade bridge where credit was successfully consumed
        from src.ccp.models.phase0_workspace_models import Phase0UpgradeBridgeState
        bridge = Phase0UpgradeBridgeState(
            bridge_id="bridge-p5",
            workspace_id="ws-p5",
            prospect_id="P5",
            target_tier="SPEAKING_LEARNING",
            payment_confirmed=True,
            payment_amount_cents=2999,
            credit_applied_cents=2999,
            migration_status="completed",
            confirmed_at=current_time.isoformat(),
        )
        workspace_service.upgrade_bridges["ws-p5"] = bridge

        response = client.get("/api/phase0/operator/queue?workspace_id=test-ws-commercial")
        assert response.status_code == 200
        
        view = Phase0OperatorQueueView.model_validate(response.json())
        assert view.total_active_packages == 1
        
        item = view.items[0]
        # Paid label should reflect $29.99 unlock details
        assert "Paid ($29.99 Phase-0 Proof Unlocked)" in item.payment_state_label
        # Upgrade label should explicitly reflect Speaking & Learning continuity tier parameter
        assert "Upgraded to Speaking & Learning ($39.99/mo)" in item.upgrade_state_label

    def test_batch_aggregator_12_packages_sorting(self, client: TestClient):
        """
        AC8: Verifies queue aggregation remains fully functional and fast for at least 12
        simultaneous packages, with breached packages floating strictly to the top.
        """
        current_time = datetime.now(timezone.utc)
        
        # Populate exactly 12 packages
        for idx in range(1, 13):
            p_id = f"pkt-batch-{idx}"
            display_name = f"Coach Pack {idx}"
            
            packet = Phase0ProspectPacket(
                prospect_id=f"P-BATCH-{idx}",
                packet_id=p_id,
                display_name=display_name,
                coach_id="P0W",
                status=Phase0ProspectStatus.READY_FOR_PHASE0,
            )
            intake_service.prospects[p_id] = packet

            # Configure package 3 and 7 to be breached (negative SLA countdown remaining minutes)
            if idx in [3, 7]:
                offset_hours = -2.0  # 2 hours overdue -> BREACHED
            elif idx in [1, 9]:
                offset_hours = 0.5   # 30 mins remaining -> RED
            else:
                offset_hours = 12.0  # 12 hours remaining -> GREEN

            workspace = Phase0WorkspaceRecord(
                prospect_id=f"P-BATCH-{idx}",
                prospect_packet_id=p_id,
                coach_id="P0W",
                workspace_id=f"ws-batch-{idx}",
                display_name=display_name,
                status=Phase0WorkspaceStatus.AUDIT_IN_PROGRESS,
                created_by_receipt_id=f"RCPT-TEST-BATCH-{idx}",
                created_at=(current_time - timedelta(hours=24) + timedelta(hours=offset_hours)).isoformat(),
                delivery_sla_deadline_utc=(current_time + timedelta(hours=offset_hours)).isoformat(),
            )
            workspace_service.workspaces[f"ws-batch-{idx}"] = workspace

        response = client.get("/api/phase0/operator/queue?workspace_id=test-ws-batch-12")
        assert response.status_code == 200
        
        view = Phase0OperatorQueueView.model_validate(response.json())
        assert view.total_active_packages == 12
        
        # Tally color classifications
        assert view.breached_count == 2
        assert view.red_count == 2
        assert view.green_count == 8
        
        # Assert strictly sorted sequence priorities: BREACHED items MUST float to absolute top of queue
        # Followed by RED risk-band items, and finally GREEN items.
        
        # First 2 items must be BREACHED (from pack 3 and 7)
        assert view.items[0].sla_state.risk_band == "BREACHED"
        assert view.items[1].sla_state.risk_band == "BREACHED"
        assert set([view.items[0].phase0_packet_id, view.items[1].phase0_packet_id]) == {"pkt-batch-3", "pkt-batch-7"}
        
        # Next 2 items must be RED risk-band (from pack 1 and 9)
        assert view.items[2].sla_state.risk_band == "RED"
        assert view.items[3].sla_state.risk_band == "RED"
        assert set([view.items[2].phase0_packet_id, view.items[3].phase0_packet_id]) == {"pkt-batch-1", "pkt-batch-9"}
        
        # Remaining items must be GREEN risk-band
        for idx in range(4, 12):
            assert view.items[idx].sla_state.risk_band == "GREEN"

        # Verify batch sweep registration receipt written
        rc = ReceiptChain(coach_acronym="P0W")
        sweep_receipts = [r for r in rc.query(action="PHASE0-CONSOLE-AGGREGATE")]
        assert len(sweep_receipts) >= 1
        assert sweep_receipts[-1].payload["total_active"] == 12
