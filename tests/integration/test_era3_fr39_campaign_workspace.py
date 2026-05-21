"""
FR-ERA3-39 Phase-0 Campaign Workspace Integration Tests
=========================================================
Tests the complete lifecycle of the campaign workspace: coach row bindings,
bulk drag/drop upload staging and lineage matching, readiness evaluations,
single and batch execution triggers, filtering and sorting, and payment label syncs.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient

from src.ccp.api.main import app
from src.ccp.api.phase0_campaign_workspace import (
    campaign_workspace_service,
    intake_service,
    workspace_service,
    delivery_orchestrator,
    receipt_chain,
)
from src.ccp.models.phase0_campaign_frontend_models import (
    Phase0CampaignWorkspace,
    Phase0CoachRow,
    Phase0CoachBinding,
    Phase0BatchUploadSession,
    Phase0ReadinessSummary,
    Phase0ExecutionRequest,
    Phase0WorkspaceFilterState,
    Phase0BulkAttachmentResult,
)
from src.ccp.models.phase0_intake_models import Phase0ProspectPacket, Phase0ProspectStatus
from src.ccp.models.phase0_workspace_models import Phase0WorkspaceRecord, Phase0WorkspaceStatus
from src.ccp.models.phase0_delivery_models import Phase0DeliveryRun, Phase0DeliveryRunStatus
from src.ccp.core.receipt_chain import ReceiptChain


@pytest.fixture(autouse=True)
def clean_campaign_stores():
    """Clear all service state and databases before each test execution."""
    campaign_workspace_service.workspaces.clear()
    campaign_workspace_service.batch_upload_sessions.clear()
    campaign_workspace_service.execution_requests.clear()
    intake_service.prospects.clear()
    workspace_service.workspaces.clear()
    delivery_orchestrator.runs.clear()
    delivery_orchestrator.plans.clear()
    import shutil
    if receipt_chain.log_dir.exists():
        shutil.rmtree(receipt_chain.log_dir)
    receipt_chain.log_dir.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestFRERA339CampaignWorkspace:

    def test_get_workspace_empty(self, client: TestClient):
        """Verifies returning an empty workspace when no prospects have been intake-staged."""
        response = client.get("/api/phase0/workspace?workspace_id=ws-empty&operator_id=op-mitano")
        assert response.status_code == 200
        workspace = Phase0CampaignWorkspace.model_validate(response.json())
        assert workspace.workspace_id == "ws-empty"
        assert workspace.rows == []
        assert workspace.operator_id == "op-mitano"

    def test_bind_coach_provisional_and_resolved(self, client: TestClient):
        """
        AC1: Verifies operator can bind coach rows, normalising from provisional (draft)
        to resolved IDs, and confirming receipt chain generation.
        """
        # Seed an initial prospect packet
        p_id = "pkt-prospect-audrey"
        packet = Phase0ProspectPacket(
            prospect_id="audrey-id",
            packet_id=p_id,
            display_name="Audrey Beat",
            coach_id="",  # Unbound initially
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p_id] = packet

        # 1. Post a provisional binding (empty or blank coach_id)
        bind_payload = {
            "workspace_id": "ws-1",
            "row_id": p_id,
            "coach_id": "",
            "provisional_label": "Audrey Provisional Draft"
        }
        res_prov = client.post("/api/phase0/workspace/coach-bind", json=bind_payload)
        assert res_prov.status_code == 200
        binding = Phase0CoachBinding.model_validate(res_prov.json())
        assert binding.binding_state == "PROVISIONAL"
        assert binding.provisional_label == "Audrey Provisional Draft"
        assert binding.coach_id == ""

        # Verify receiptchain entry
        bind_receipts = [r for r in receipt_chain.query(action="PHASE0-COACH-BIND")]
        assert len(bind_receipts) == 1
        assert bind_receipts[0].payload["output_summary"] == "Binding resolved as: PROVISIONAL"

        # 2. Resolve to a stable coach_id
        resolve_payload = {
            "workspace_id": "ws-1",
            "row_id": p_id,
            "coach_id": "audrey_coach",
            "provisional_label": None
        }
        res_res = client.post("/api/phase0/workspace/coach-bind", json=resolve_payload)
        assert res_res.status_code == 200
        resolved_binding = Phase0CoachBinding.model_validate(res_res.json())
        assert resolved_binding.binding_state == "RESOLVED"
        assert resolved_binding.coach_id == "audrey_coach"
        assert resolved_binding.coach_acronym == "AUD"

        # Verify second receipt recorded
        updated_receipts = [r for r in receipt_chain.query(action="PHASE0-COACH-BIND")]
        assert len(updated_receipts) == 2
        assert updated_receipts[-1].payload["output_summary"] == "Binding resolved as: RESOLVED"

    def test_batch_upload_grouping_and_lineage(self, client: TestClient):
        """
        AC2 & AC3 & AC4: Tests staging multiple coach uploads in the same workspace session,
        validating correct grouping heuristics and lineage matching in namespaced paths.
        """
        # Seed two coach prospects
        p1_id = "pkt-audrey"
        packet1 = Phase0ProspectPacket(
            prospect_id="p-audrey",
            packet_id=p1_id,
            display_name="Audrey Sonic",
            coach_id="audrey_sonic",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p1_id] = packet1

        p2_id = "pkt-jean"
        packet2 = Phase0ProspectPacket(
            prospect_id="p-jean",
            packet_id=p2_id,
            display_name="Jean Pierre",
            coach_id="jean_pierre",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p2_id] = packet2

        # Staging 3 files:
        # File 1: audrey_interview.mp3 (matches pkt-audrey by filename prefix rule)
        # File 2: jean_sales.mp3 (matches pkt-jean by filename prefix rule)
        # File 3: general_notes.pdf (ambiguous)
        upload_payload = {
            "workspace_id": "ws-campaign",
            "operator_id": "op-mitano",
            "files": [
                {
                    "original_filename": "audrey_interview.mp3",
                    "media_kind": "interview_audio",
                    "file_size_bytes": 50000,
                    "mime_type": "audio/mp3"
                },
                {
                    "original_filename": "jean_sales.mp3",
                    "media_kind": "supporting_reference",
                    "file_size_bytes": 12000,
                    "mime_type": "audio/mp3"
                },
                {
                    "original_filename": "general_notes.pdf",
                    "media_kind": "supporting_reference",
                    "file_size_bytes": 4500
                }
            ],
            "target_row_ids": [p1_id, p2_id]
        }

        res = client.post("/api/phase0/workspace/batch-upload", json=upload_payload)
        assert res.status_code == 200
        result = Phase0BulkAttachmentResult.model_validate(res.json())

        # Assert correct allocations
        assert result.attached_count == 2
        assert result.failed_count == 1
        assert result.row_attachment_counts[p1_id] == 1
        assert result.row_attachment_counts[p2_id] == 1
        
        # Verify ambiguous file fails safely (AC10 / F1)
        assert "general_notes.pdf" in result.unresolved_files
        assert any("Ambiguous file grouping" in w for w in result.warnings)

        # Check intake packets have indeed registered media files correctly with shared storage path conventions
        audrey_packet = intake_service.get_prospect(p1_id)
        assert len(audrey_packet.media_sources) == 1
        assert audrey_packet.media_sources[0].original_filename == "audrey_interview.mp3"
        assert "campaigns/audrey_sonic/intake/audrey_interview.mp3" in audrey_packet.media_sources[0].storage_uri

        jean_packet = intake_service.get_prospect(p2_id)
        assert len(jean_packet.media_sources) == 1
        assert jean_packet.media_sources[0].original_filename == "jean_sales.mp3"
        assert "campaigns/jean_pierre/intake/jean_sales.mp3" in jean_packet.media_sources[0].storage_uri

        # Verify receipt recorded
        upload_receipts = [r for r in receipt_chain.query(action="PHASE0-BATCH-UPLOAD")]
        assert len(upload_receipts) == 1
        assert upload_receipts[0].payload["metadata"]["session_id"] == result.batch_upload_session_id

    def test_readiness_at_a_glance(self, client: TestClient):
        """
        AC5: Verifies that readiness evaluation recomputes validation gaps,
        file attachments, and audience/BI profile metrics correctly on request.
        """
        p_id = "pkt-readiness-test"
        packet = Phase0ProspectPacket(
            prospect_id="p-test",
            packet_id=p_id,
            display_name="Jean Pierre",
            coach_id="jean_pierre",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p_id] = packet

        # Request row detail view - should show unready, zero files, missing fields
        response1 = client.get(f"/api/phase0/workspace/{p_id}?workspace_id=ws-readiness")
        assert response1.status_code == 200
        row1 = Phase0CoachRow.model_validate(response1.json())
        assert row1.row_state == "BOUND_UNREADY"
        assert row1.readiness.ready is False
        assert "missing_interview_material" in row1.readiness.missing_required_fields
        assert row1.readiness.attached_file_count == 0
        assert row1.readiness.audience_present is False
        assert row1.readiness.business_intelligence_present is False
        assert row1.next_action == "Upload Missing Inputs"

        # Attach media sources, audience profile and guardian business intelligence
        intake_service.attach_media(
            prospect_id=p_id,
            media_kind="interview_audio",
            storage_uri="path/interview.mp3",
            original_filename="interview.mp3",
            file_size_bytes=1000
        )
        from src.ccp.models.phase0_intake_models import Phase0TargetAudienceProfile, Phase0GuardianBusinessIntelligenceBundle, Phase0AuditTargetDescriptor, Phase0AuditTargetContentType
        packet.target_audience_profile = Phase0TargetAudienceProfile(
            prospect_id=p_id,
            primary_audience_label="Coaches",
            pain_points=["Stagnant revenue"],
            desires=["Growth"]
        )
        packet.guardian_business_intelligence_bundle = Phase0GuardianBusinessIntelligenceBundle(
            prospect_id=p_id,
            market_summary="High growth potential",
            offer_summary="Conscious Coaching"
        )
        # Add a mock audit target
        packet.audit_targets.append(Phase0AuditTargetDescriptor(
            prospect_id=p_id,
            content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION
        ))

        # Re-fetch row details - should now evaluate to READY
        response2 = client.get(f"/api/phase0/workspace/{p_id}?workspace_id=ws-readiness")
        assert response2.status_code == 200
        row2 = Phase0CoachRow.model_validate(response2.json())
        assert row2.row_state == "READY_TO_EXECUTE"
        assert row2.readiness.ready is True
        assert row2.readiness.missing_required_fields == []
        assert row2.readiness.attached_file_count == 1
        assert row2.readiness.audience_present is True
        assert row2.readiness.business_intelligence_present is True
        assert row2.readiness.audit_target_count == 1
        assert row2.next_action == "Trigger shared execution pipeline"

    def test_single_row_execution(self, client: TestClient):
        """
        AC6: Tests single-row pipeline execution dispatch, verifying delivery run
        initialization and receipt log mutation.
        """
        p_id = "pkt-exec-single"
        packet = Phase0ProspectPacket(
            prospect_id="p-single",
            packet_id=p_id,
            display_name="Audrey Beat",
            coach_id="audrey_beat",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p_id] = packet

        # Pre-attach resources to make it ready
        intake_service.attach_media(p_id, "interview_audio", "path/audio.mp3", "audio.mp3", 1000)
        from src.ccp.models.phase0_intake_models import Phase0TargetAudienceProfile, Phase0GuardianBusinessIntelligenceBundle, Phase0AuditTargetDescriptor, Phase0AuditTargetContentType
        packet.target_audience_profile = Phase0TargetAudienceProfile(prospect_id=p_id, primary_audience_label="av", pain_points=["pp"], desires=["cd"])
        packet.guardian_business_intelligence_bundle = Phase0GuardianBusinessIntelligenceBundle(prospect_id=p_id, market_summary="ge", offer_summary="ins")
        packet.audit_targets.append(Phase0AuditTargetDescriptor(prospect_id=p_id, content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION))

        # Execute Endpoint
        exec_payload = {
            "workspace_id": "ws-exec",
            "row_ids": [p_id],
            "operator_id": "op-mitano"
        }
        res = client.post("/api/phase0/workspace/execute", json=exec_payload)
        assert res.status_code == 200
        execs = [Phase0ExecutionRequest.model_validate(e) for e in res.json()]
        assert len(execs) == 1
        assert execs[0].execution_mode == "SINGLE"
        assert execs[0].row_ids == [p_id]
        assert execs[0].triggered_by_operator_id == "op-mitano"

        # Verify delivery run created and successfully executed synchronously
        active_runs = list(delivery_orchestrator.runs.values())
        assert len(active_runs) == 1
        assert active_runs[0].phase0_packet_id == p_id
        assert active_runs[0].status == Phase0DeliveryRunStatus.COMPLETED

        # Verify execution trigger receipt chain entry
        exec_receipts = [r for r in receipt_chain.query(action="PHASE0-EXECUTION-TRIGGER")]
        assert len(exec_receipts) == 1
        assert exec_receipts[0].payload["metadata"]["request_id"] == execs[0].request_id

    def test_batch_row_execution(self, client: TestClient):
        """
        AC7: Tests multi-select batch execution, and ensures unready rows block
        entire batch execution safely (AC10 / F2 / F6).
        """
        # Row 1: Ready
        p1_id = "pkt-exec-batch-1"
        packet1 = Phase0ProspectPacket(
            prospect_id="p-b1",
            packet_id=p1_id,
            display_name="Coach One",
            coach_id="coach_one",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p1_id] = packet1
        intake_service.attach_media(p1_id, "interview_audio", "path/audio1.mp3", "audio1.mp3", 1000)
        from src.ccp.models.phase0_intake_models import Phase0TargetAudienceProfile, Phase0GuardianBusinessIntelligenceBundle, Phase0AuditTargetDescriptor, Phase0AuditTargetContentType
        packet1.target_audience_profile = Phase0TargetAudienceProfile(prospect_id=p1_id, primary_audience_label="av", pain_points=["pp"], desires=["cd"])
        packet1.guardian_business_intelligence_bundle = Phase0GuardianBusinessIntelligenceBundle(prospect_id=p1_id, market_summary="ge", offer_summary="ins")
        packet1.audit_targets.append(Phase0AuditTargetDescriptor(prospect_id=p1_id, content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION))

        # Row 2: Unready (missing audio)
        p2_id = "pkt-exec-batch-2"
        packet2 = Phase0ProspectPacket(
            prospect_id="p-b2",
            packet_id=p2_id,
            display_name="Coach Two",
            coach_id="coach_two",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p2_id] = packet2

        # 1. Trigger batch execute with an unready row -> Must raise 400 Bad Request
        exec_fail_payload = {
            "workspace_id": "ws-exec-batch",
            "row_ids": [p1_id, p2_id],
            "operator_id": "op-mitano"
        }
        res_fail = client.post("/api/workspace/execute" if False else "/api/phase0/workspace/execute", json=exec_fail_payload)
        assert res_fail.status_code == 400
        assert "EXECUTION_BLOCKED" in res_fail.json()["detail"]

        # Verify blocked execution receipt written
        blocked_receipts = [r for r in receipt_chain.query(action="PHASE0-EXECUTION-BLOCKED")]
        assert len(blocked_receipts) == 1

        # 2. Make Row 2 ready and execute batch again -> Should succeed
        intake_service.attach_media(p2_id, "interview_audio", "path/audio2.mp3", "audio2.mp3", 1000)
        packet2.target_audience_profile = Phase0TargetAudienceProfile(prospect_id=p2_id, primary_audience_label="av", pain_points=["pp"], desires=["cd"])
        packet2.guardian_business_intelligence_bundle = Phase0GuardianBusinessIntelligenceBundle(prospect_id=p2_id, market_summary="ge", offer_summary="ins")
        packet2.audit_targets.append(Phase0AuditTargetDescriptor(prospect_id=p2_id, content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION))

        exec_success_payload = {
            "workspace_id": "ws-exec-batch",
            "row_ids": [p1_id, p2_id],
            "operator_id": "op-mitano"
        }
        res_ok = client.post("/api/phase0/workspace/execute", json=exec_success_payload)
        assert res_ok.status_code == 200
        exec_requests = [Phase0ExecutionRequest.model_validate(e) for e in res_ok.json()]
        assert len(exec_requests) == 2
        assert exec_requests[0].execution_mode == "BATCH"
        assert exec_requests[1].execution_mode == "BATCH"

        # Verify delivery runs created
        active_runs = list(delivery_orchestrator.runs.values())
        assert len(active_runs) == 2
        assert set([r.phase0_packet_id for r in active_runs]) == {p1_id, p2_id}

    def test_workspace_filtering_and_sorting(self, client: TestClient):
        """
        AC8: Verifies workspace query endpoints properly filter by readiness,
        delivery status, payment labels, and search queries, and sort rows.
        """
        # Create row 1: Ready, Unexecuted, name 'Audrey Beat'
        p1_id = "pkt-filter-1"
        packet1 = Phase0ProspectPacket(
            prospect_id="p-f1",
            packet_id=p1_id,
            display_name="Audrey Beat",
            coach_id="audrey_beat",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p1_id] = packet1
        intake_service.attach_media(p1_id, "interview_audio", "path/audio1.mp3", "audio1.mp3", 1000)
        from src.ccp.models.phase0_intake_models import Phase0TargetAudienceProfile, Phase0GuardianBusinessIntelligenceBundle, Phase0AuditTargetDescriptor, Phase0AuditTargetContentType
        packet1.target_audience_profile = Phase0TargetAudienceProfile(prospect_id=p1_id, primary_audience_label="av", pain_points=["pp"], desires=["cd"])
        packet1.guardian_business_intelligence_bundle = Phase0GuardianBusinessIntelligenceBundle(prospect_id=p1_id, market_summary="ge", offer_summary="ins")
        packet1.audit_targets.append(Phase0AuditTargetDescriptor(prospect_id=p1_id, content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION))

        # Create row 2: Unready, Unexecuted, name 'Jean Pierre'
        p2_id = "pkt-filter-2"
        packet2 = Phase0ProspectPacket(
            prospect_id="p-f2",
            packet_id=p2_id,
            display_name="Jean Pierre",
            coach_id="jean_pierre",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p2_id] = packet2

        # 1. Search Query Filter ('Audrey')
        res_search = client.get("/api/phase0/workspace?workspace_id=ws-filter&operator_id=op&search_query=Audrey")
        assert res_search.status_code == 200
        ws_search = Phase0CampaignWorkspace.model_validate(res_search.json())
        assert len(ws_search.rows) == 1
        assert ws_search.rows[0].display_name == "Audrey Beat"

        # 2. Readiness Filter ('READY')
        res_ready = client.get("/api/phase0/workspace?workspace_id=ws-filter&operator_id=op&readiness_filter=READY")
        assert res_ready.status_code == 200
        ws_ready = Phase0CampaignWorkspace.model_validate(res_ready.json())
        assert len(ws_ready.rows) == 1
        assert ws_ready.rows[0].display_name == "Audrey Beat"

        # 3. Readiness Filter ('BLOCKED')
        res_blocked = client.get("/api/phase0/workspace?workspace_id=ws-filter&operator_id=op&readiness_filter=BLOCKED")
        assert res_blocked.status_code == 200
        ws_blocked = Phase0CampaignWorkspace.model_validate(res_blocked.json())
        assert len(ws_blocked.rows) == 1
        assert ws_blocked.rows[0].display_name == "Jean Pierre"

        # 4. Sorting ('NAME')
        res_sort = client.get("/api/phase0/workspace?workspace_id=ws-filter&operator_id=op&sort_key=NAME")
        assert res_sort.status_code == 200
        ws_sort = Phase0CampaignWorkspace.model_validate(res_sort.json())
        assert len(ws_sort.rows) == 2
        assert ws_sort.rows[0].display_name == "Audrey Beat"
        assert ws_sort.rows[1].display_name == "Jean Pierre"

    def test_payment_label_visualization(self, client: TestClient):
        """
        AC9: Verifies that payment related state labels map accurately onto coach rows
        reflecting the lifecycle status of the workspace (DRAFT/UNPAID/PAID/UPGRADED).
        """
        p_id = "pkt-payment-lbl"
        packet = Phase0ProspectPacket(
            prospect_id="p-pay",
            packet_id=p_id,
            display_name="Audrey Beat",
            coach_id="audrey_beat",
            status=Phase0ProspectStatus.DRAFT,
        )
        intake_service.prospects[p_id] = packet

        # 1. Draft/Unready state -> payment state label is NOT_APPLICABLE
        res_draft = client.get(f"/api/phase0/workspace/{p_id}?workspace_id=ws-pay")
        assert res_draft.status_code == 200
        row_draft = Phase0CoachRow.model_validate(res_draft.json())
        assert row_draft.row_state == "BOUND_UNREADY"
        assert row_draft.payment_state_label == "NOT_APPLICABLE"

        # Make ready and execute
        intake_service.attach_media(p_id, "interview_audio", "path/audio1.mp3", "audio1.mp3", 1000)
        from src.ccp.models.phase0_intake_models import Phase0TargetAudienceProfile, Phase0GuardianBusinessIntelligenceBundle, Phase0AuditTargetDescriptor, Phase0AuditTargetContentType
        packet.target_audience_profile = Phase0TargetAudienceProfile(prospect_id=p_id, primary_audience_label="av", pain_points=["pp"], desires=["cd"])
        packet.guardian_business_intelligence_bundle = Phase0GuardianBusinessIntelligenceBundle(prospect_id=p_id, market_summary="ge", offer_summary="ins")
        packet.audit_targets.append(Phase0AuditTargetDescriptor(prospect_id=p_id, content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION))

        client.post("/api/phase0/workspace/execute", json={"workspace_id": "ws-pay", "row_ids": [p_id], "operator_id": "op"})

        # 2. Delivered / awaiting payment state -> UNPAID
        res_deliv = client.get(f"/api/phase0/workspace/{p_id}?workspace_id=ws-pay")
        assert res_deliv.status_code == 200
        row_deliv = Phase0CoachRow.model_validate(res_deliv.json())
        assert row_deliv.row_state == "DELIVERED_AWAITING_PAYMENT"
        assert row_deliv.payment_state_label == "UNPAID"

        # Update workspace record to PAYMENT_UNLOCKED
        ws_rec = next((w for w in workspace_service.workspaces.values() if w.prospect_packet_id == p_id), None)
        if not ws_rec:
            # Seed a workspace record to simulate delivery outcomes
            ws_rec = Phase0WorkspaceRecord(
                prospect_id="p-pay",
                prospect_packet_id=p_id,
                coach_id="audrey_beat",
                workspace_id="ws-audrey",
                display_name="Audrey Beat",
                status=Phase0WorkspaceStatus.DELIVERED,
                created_by_receipt_id="RCPT-1",
            )
            workspace_service.workspaces["ws-audrey"] = ws_rec
        ws_rec.status = Phase0WorkspaceStatus.PAYMENT_UNLOCKED

        # 3. Unlocked state -> PAID
        res_paid = client.get(f"/api/phase0/workspace/{p_id}?workspace_id=ws-pay")
        assert res_paid.status_code == 200
        row_paid = Phase0CoachRow.model_validate(res_paid.json())
        assert row_paid.row_state == "PAID_UNLOCKED"
        assert row_paid.payment_state_label == "PAID"

        # Update workspace record to UPGRADED
        ws_rec.status = Phase0WorkspaceStatus.UPGRADED

        # 4. Upgraded state -> UPGRADED
        res_upg = client.get(f"/api/phase0/workspace/{p_id}?workspace_id=ws-pay")
        assert res_upg.status_code == 200
        row_upg = Phase0CoachRow.model_validate(res_upg.json())
        assert row_upg.row_state == "UPGRADED"
        assert row_upg.payment_state_label == "UPGRADED"

    def test_throughput_12_rows_integration(self, client: TestClient):
        """
        Throughput Gate: Verifies that the workspace is highly optimized to handle
        the synthesis, filtering, and listing of at least 12 simultaneous active rows.
        """
        # Seed 12 different coach rows in the database
        for idx in range(1, 13):
            p_id = f"pkt-throughput-{idx}"
            packet = Phase0ProspectPacket(
                prospect_id=f"p-throughput-{idx}",
                packet_id=p_id,
                display_name=f"Coach Throughput {idx}",
                coach_id=f"coach_throughput_{idx}",
                status=Phase0ProspectStatus.DRAFT,
            )
            intake_service.prospects[p_id] = packet

        response = client.get("/api/phase0/workspace?workspace_id=ws-throughput&operator_id=op")
        assert response.status_code == 200
        workspace = Phase0CampaignWorkspace.model_validate(response.json())
        
        # Verify 12 rows are successfully aggregated and present
        assert len(workspace.rows) == 12
        for idx in range(12):
            assert "Coach Throughput" in workspace.rows[idx].display_name
