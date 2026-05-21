"""
Integration tests for FR-ERA3-34 Phase-0 Workspace and Artifact Store.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_intake_models import Phase0ProspectPacket
from src.ccp.models.phase0_workspace_models import (
    Phase0ArtifactFamily,
    Phase0ArtifactStatus,
    Phase0DeliveryWindowStatus,
    Phase0WorkspaceStatus,
)
from src.ccp.services.phase0_artifact_store import Phase0ArtifactStore
from src.ccp.services.phase0_migration_service import Phase0MigrationService
from src.ccp.services.phase0_workspace_service import Phase0WorkspaceService


def make_packet(prospect_id: str = "P1", packet_id: str = "PKT-P1") -> Phase0ProspectPacket:
    return Phase0ProspectPacket(
        prospect_id=prospect_id,
        packet_id=packet_id,
        display_name=f"Prospect {prospect_id}",
        coach_id="P0W",
    )


@pytest.fixture
def services(tmp_path):
    receipt_dir = tmp_path / "receipt_chain"
    rc = ReceiptChain(coach_acronym="P0W", log_dir=str(receipt_dir))
    workspace_service = Phase0WorkspaceService(receipt_chain=rc)
    artifact_store = Phase0ArtifactStore(workspace_service=workspace_service, receipt_chain=rc)
    migration_service = Phase0MigrationService(
        workspace_service=workspace_service,
        artifact_store=artifact_store,
        receipt_chain=rc,
        scaffold_root=tmp_path / "coaches",
    )
    return rc, workspace_service, artifact_store, migration_service


class TestPhase0WorkspaceCreation:
    def test_valid_packet_creates_workspace(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        assert workspace.status == Phase0WorkspaceStatus.INTAKE_RECEIVED

    def test_status_is_intake_received(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        assert workspace.status == Phase0WorkspaceStatus.INTAKE_RECEIVED

    def test_sla_deadline_is_24h_from_now(self, services):
        _, workspace_service, _, _ = services
        before = datetime.now(timezone.utc)
        workspace = workspace_service.create_workspace(make_packet())
        deadline = datetime.fromisoformat(workspace.delivery_sla_deadline_utc)
        diff_hours = (deadline - before).total_seconds() / 3600.0
        assert 23.9 <= diff_hours <= 24.1

    def test_empty_prospect_id_rejected(self, services):
        _, workspace_service, _, _ = services
        with pytest.raises(ValueError):
            workspace_service.create_workspace(make_packet(prospect_id="", packet_id="PKT-X"))

    def test_empty_packet_id_rejected(self, services):
        _, workspace_service, _, _ = services
        with pytest.raises(ValueError):
            workspace_service.create_workspace(make_packet(prospect_id="P1", packet_id=""))

    def test_receipt_logged_on_create(self, services):
        rc, workspace_service, _, _ = services
        workspace_service.create_workspace(make_packet())
        assert len(rc.query(action="PHASE0-WORKSPACE-CREATE")) >= 1


class TestPhase0WorkspaceTransition:
    def test_valid_transition_succeeds(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        workspace = workspace_service.transition_workspace(
            workspace.workspace_id, Phase0WorkspaceStatus.ARTIFACTS_COLLECTING
        )
        assert workspace.status == Phase0WorkspaceStatus.ARTIFACTS_COLLECTING

    def test_illegal_transition_raises_value_error(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        with pytest.raises(ValueError):
            workspace_service.transition_workspace(workspace.workspace_id, Phase0WorkspaceStatus.DELIVERED)

    def test_illegal_transition_leaves_status_unchanged(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        with pytest.raises(ValueError):
            workspace_service.transition_workspace(workspace.workspace_id, Phase0WorkspaceStatus.DELIVERED)
        assert workspace_service.get_workspace(workspace.workspace_id).status == Phase0WorkspaceStatus.INTAKE_RECEIVED

    def test_transition_logs_receipt(self, services):
        rc, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        workspace_service.transition_workspace(workspace.workspace_id, Phase0WorkspaceStatus.ARTIFACTS_COLLECTING)
        assert len(rc.query(action="PHASE0-WORKSPACE-TRANSITION")) >= 1

    def test_blocked_requires_human_recovery(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        workspace_service.transition_workspace(workspace.workspace_id, Phase0WorkspaceStatus.BLOCKED)
        with pytest.raises(ValueError):
            workspace_service.transition_workspace(
                workspace.workspace_id,
                Phase0WorkspaceStatus.INTAKE_RECEIVED,
            )


class TestPhase0ArtifactRegistration:
    def test_intake_source_registered_without_parent(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        assert artifact.family == Phase0ArtifactFamily.INTAKE_SOURCE

    def test_audit_report_requires_parent_artifact(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        with pytest.raises(ValueError):
            artifact_store.register_artifact(
                workspace_id=workspace.workspace_id,
                family=Phase0ArtifactFamily.AUDIT_REPORT,
                source_receipt_id="rcpt-audit",
                display_label="audit pdf",
            )

    def test_empty_source_receipt_id_rejected(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        with pytest.raises(ValueError):
            artifact_store.register_artifact(
                workspace_id=workspace.workspace_id,
                family=Phase0ArtifactFamily.INTAKE_SOURCE,
                source_receipt_id="",
                display_label="interview audio",
            )

    def test_artifact_id_follows_p0af_format(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        assert artifact.artifact_id.startswith("P0AF-P0W-")

    def test_receipt_logged_on_register(self, services):
        rc, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        assert len(rc.query(action="PHASE0-ARTIFACT-REGISTER")) >= 1


class TestPhase0ArtifactStateMachine:
    def test_uploaded_to_normalized_allowed(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        artifact = artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.NORMALIZED)
        assert artifact.status == Phase0ArtifactStatus.NORMALIZED

    def test_uploaded_to_delivered_raises(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        with pytest.raises(ValueError):
            artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.DELIVERED)

    def test_normalized_to_audit_ready_allowed(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.NORMALIZED)
        artifact = artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.AUDIT_READY)
        assert artifact.status == Phase0ArtifactStatus.AUDIT_READY

    def test_any_state_to_quarantined_allowed(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        artifact = artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.QUARANTINED)
        assert artifact.status == Phase0ArtifactStatus.QUARANTINED

    def test_quarantine_recovery_requires_human_note(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.QUARANTINED)
        with pytest.raises(ValueError):
            artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.UPLOADED)

    def test_upgraded_is_terminal_state(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        for status in (
            Phase0ArtifactStatus.NORMALIZED,
            Phase0ArtifactStatus.AUDIT_READY,
            Phase0ArtifactStatus.PREVIEW_READY,
            Phase0ArtifactStatus.DELIVERED,
            Phase0ArtifactStatus.PAYMENT_UNLOCKED,
            Phase0ArtifactStatus.UPGRADED,
        ):
            artifact = artifact_store.transition_artifact(artifact.artifact_id, status)
        with pytest.raises(ValueError):
            artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.NORMALIZED)

    def test_transition_logs_receipt(self, services):
        rc, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.NORMALIZED)
        assert len(rc.query(action="PHASE0-ARTIFACT-TRANSITION")) >= 1


class TestPhase0ManifestAssembly:
    def test_empty_workspace_all_families_missing(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        manifest = artifact_store.assemble_manifest(workspace.workspace_id)
        assert manifest.completeness_summary["audit_report"] == "missing"
        assert manifest.completeness_summary["preview_asset"] == "missing"

    def test_intake_source_present_marks_family_partial(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        manifest = artifact_store.assemble_manifest(workspace.workspace_id)
        assert manifest.completeness_summary["intake_source"] == "partial"

    def test_preview_ready_artifact_marks_family_present(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        source = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        audit = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.AUDIT_REPORT,
            source_receipt_id="rcpt-audit",
            display_label="audit pdf",
            parent_artifact_ids=[source.artifact_id],
        )
        for status in (
            Phase0ArtifactStatus.NORMALIZED,
            Phase0ArtifactStatus.AUDIT_READY,
            Phase0ArtifactStatus.PREVIEW_READY,
        ):
            artifact_store.transition_artifact(audit.artifact_id, status)
        manifest = artifact_store.assemble_manifest(workspace.workspace_id)
        assert manifest.completeness_summary["audit_report"] == "present"

    def test_delivery_ready_requires_audit_and_preview(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        source = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        audit = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.AUDIT_REPORT,
            source_receipt_id="rcpt-audit",
            display_label="audit pdf",
            parent_artifact_ids=[source.artifact_id],
        )
        preview = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.PREVIEW_ASSET,
            source_receipt_id="rcpt-preview",
            display_label="preview mp4",
            parent_artifact_ids=[source.artifact_id],
        )
        for artifact in (audit, preview):
            for status in (
                Phase0ArtifactStatus.NORMALIZED,
                Phase0ArtifactStatus.AUDIT_READY,
                Phase0ArtifactStatus.PREVIEW_READY,
            ):
                artifact_store.transition_artifact(artifact.artifact_id, status)
        manifest = artifact_store.assemble_manifest(workspace.workspace_id)
        assert manifest.is_delivery_ready is True

    def test_manifest_receipt_logged(self, services):
        rc, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact_store.assemble_manifest(workspace.workspace_id)
        assert len(rc.query(action="PHASE0-MANIFEST-ASSEMBLE")) >= 1


class TestPhase0ReadinessComputation:
    def test_on_track_when_hours_remaining_gt_6(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        readiness = workspace_service.compute_readiness(workspace.workspace_id)
        assert readiness.delivery_window_status == Phase0DeliveryWindowStatus.ON_TRACK

    def test_at_risk_when_hours_remaining_lte_6(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        workspace.delivery_sla_deadline_utc = (datetime.now(timezone.utc) + timedelta(hours=5)).isoformat()
        readiness = workspace_service.compute_readiness(workspace.workspace_id)
        assert readiness.delivery_window_status == Phase0DeliveryWindowStatus.AT_RISK

    def test_breached_when_hours_remaining_lte_0(self, services):
        _, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        workspace.delivery_sla_deadline_utc = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        readiness = workspace_service.compute_readiness(workspace.workspace_id)
        assert readiness.delivery_window_status == Phase0DeliveryWindowStatus.BREACHED

    def test_quarantined_artifact_sets_human_review_required(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        artifact_store.transition_artifact(artifact.artifact_id, Phase0ArtifactStatus.QUARANTINED)
        readiness = workspace_service.compute_readiness(workspace.workspace_id)
        assert readiness.human_review_required is True

    def test_readiness_receipt_logged(self, services):
        rc, workspace_service, _, _ = services
        workspace = workspace_service.create_workspace(make_packet())
        workspace_service.compute_readiness(workspace.workspace_id)
        assert len(rc.query(action="PHASE0-READINESS-COMPUTE")) >= 1


class TestPhase0UpgradeBridge:
    def test_initiate_bridge_creates_pending_record(self, services):
        _, workspace_service, _, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        assert bridge.migration_status == "pending"

    def test_payment_confirmed_sets_flag(self, services):
        _, workspace_service, _, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        bridge = migration_service.confirm_payment(bridge.bridge_id, "payment-rcpt")
        assert bridge.payment_confirmed is True

    def test_migration_blocked_without_payment(self, services):
        _, workspace_service, _, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        with pytest.raises(PermissionError):
            migration_service.migrate_to_container(workspace.workspace_id, "NDL")

    def test_migration_blocked_logs_receipt(self, services):
        rc, workspace_service, _, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        with pytest.raises(PermissionError):
            migration_service.migrate_to_container(workspace.workspace_id, "NDL")
        assert len(rc.query(action="PHASE0-MIGRATION-BLOCKED")) >= 1

    def test_abort_sets_abort_reason(self, services):
        _, workspace_service, _, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        bridge = migration_service.abort_upgrade(bridge.bridge_id, "operator cancelled")
        assert bridge.abort_reason == "operator cancelled"


class TestPhase0Migration:
    def test_migration_archives_workspace(self, services):
        _, workspace_service, artifact_store, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        source = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        migration_service.confirm_payment(bridge.bridge_id, "payment-rcpt")
        result = migration_service.migrate_to_container(workspace.workspace_id, "NDL")
        assert result.archived_workspace_status == Phase0WorkspaceStatus.ARCHIVED

    def test_migration_marks_artifacts_upgraded(self, services):
        _, workspace_service, artifact_store, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        source = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        migration_service.confirm_payment(bridge.bridge_id, "payment-rcpt")
        migration_service.migrate_to_container(workspace.workspace_id, "NDL")
        artifacts = artifact_store.get_artifacts_by_workspace(workspace.workspace_id)
        assert all(a.status == Phase0ArtifactStatus.UPGRADED for a in artifacts)

    def test_migration_receipt_chain_complete(self, services):
        rc, workspace_service, artifact_store, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        migration_service.confirm_payment(bridge.bridge_id, "payment-rcpt")
        migration_service.migrate_to_container(workspace.workspace_id, "NDL")
        assert len(rc.query(action="PHASE0-MIGRATION-EXECUTE")) >= 1

    def test_migration_preserves_artifact_lineage(self, services):
        _, workspace_service, artifact_store, migration_service = services
        workspace = workspace_service.create_workspace(make_packet())
        source = artifact_store.register_artifact(
            workspace_id=workspace.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-source",
            display_label="interview audio",
        )
        bridge = migration_service.initiate_upgrade_bridge(workspace.workspace_id, "coach_os")
        migration_service.confirm_payment(bridge.bridge_id, "payment-rcpt")
        result = migration_service.migrate_to_container(workspace.workspace_id, "NDL")
        assert source.metadata["migrated_to_asset_id"] == result.remapped_asset_ids[source.artifact_id]


class TestPhase0Isolation:
    def test_two_prospects_artifacts_never_cross(self, services):
        _, workspace_service, artifact_store, _ = services
        workspace_1 = workspace_service.create_workspace(make_packet("P1", "PKT-P1"))
        workspace_2 = workspace_service.create_workspace(make_packet("P2", "PKT-P2"))
        artifact_store.register_artifact(
            workspace_id=workspace_1.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-1",
            display_label="p1 audio",
        )
        artifact_store.register_artifact(
            workspace_id=workspace_2.workspace_id,
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            source_receipt_id="rcpt-2",
            display_label="p2 audio",
        )
        artifacts_p1 = artifact_store.get_artifacts_by_workspace(workspace_1.workspace_id)
        assert all(a.prospect_id == "P1" for a in artifacts_p1)

    def test_workspace_ids_unique_across_prospects(self, services):
        _, workspace_service, _, _ = services
        workspace_1 = workspace_service.create_workspace(make_packet("P1", "PKT-P1"))
        workspace_2 = workspace_service.create_workspace(make_packet("P2", "PKT-P2"))
        assert workspace_1.workspace_id != workspace_2.workspace_id
