"""
Unit tests for FR-ERA3-34 Phase-0 Workspace models.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.ccp.models.phase0_workspace_models import (
    Phase0ArtifactFamily,
    Phase0ArtifactRecord,
    Phase0UpgradeBridgeState,
    Phase0WorkspaceRecord,
    Phase0WorkspaceStatus,
)


class TestPhase0WorkspaceRecord:
    def test_status_default_is_created(self):
        workspace = Phase0WorkspaceRecord(
            prospect_id="P-100",
            prospect_packet_id="PKT-100",
            display_name="Jane Doe",
            created_by_receipt_id="rcpt-1",
        )
        assert workspace.status == Phase0WorkspaceStatus.CREATED

    def test_artifact_count_cannot_be_negative(self):
        with pytest.raises(ValidationError):
            Phase0WorkspaceRecord(
                prospect_id="P-100",
                prospect_packet_id="PKT-100",
                display_name="Jane Doe",
                created_by_receipt_id="rcpt-1",
                artifact_count=-1,
            )

    def test_created_by_receipt_id_required(self):
        with pytest.raises(ValidationError):
            Phase0WorkspaceRecord(
                prospect_id="P-100",
                prospect_packet_id="PKT-100",
                display_name="Jane Doe",
                created_by_receipt_id="",
            )


class TestPhase0ArtifactRecord:
    def test_parent_artifact_ids_defaults_empty(self):
        artifact = Phase0ArtifactRecord(
            artifact_id="P0AF-P0W-05-26-ABCD",
            workspace_id="ws-1",
            prospect_id="P-1",
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            display_label="raw clip",
            source_receipt_id="rcpt-1",
        )
        assert artifact.parent_artifact_ids == []

    def test_metadata_values_cast_to_strings(self):
        artifact = Phase0ArtifactRecord(
            artifact_id="P0AF-P0W-05-26-ABCD",
            workspace_id="ws-1",
            prospect_id="P-1",
            family=Phase0ArtifactFamily.INTAKE_SOURCE,
            display_label="raw clip",
            source_receipt_id="rcpt-1",
            metadata={"count": 3, "flag": True},
        )
        assert artifact.metadata == {"count": "3", "flag": "True"}

    def test_file_size_bytes_cannot_be_negative(self):
        with pytest.raises(ValidationError):
            Phase0ArtifactRecord(
                artifact_id="P0AF-P0W-05-26-ABCD",
                workspace_id="ws-1",
                prospect_id="P-1",
                family=Phase0ArtifactFamily.INTAKE_SOURCE,
                display_label="raw clip",
                source_receipt_id="rcpt-1",
                file_size_bytes=-10,
            )


class TestPhase0UpgradeBridgeState:
    def test_payment_confirmed_defaults_false(self):
        bridge = Phase0UpgradeBridgeState(
            workspace_id="ws-1",
            prospect_id="P-1",
            target_tier="coach_os",
        )
        assert bridge.payment_confirmed is False

    def test_target_coach_acronym_enforces_3_char(self):
        with pytest.raises(ValidationError):
            Phase0UpgradeBridgeState(
                workspace_id="ws-1",
                prospect_id="P-1",
                target_tier="coach_os",
                target_coach_acronym="TOOLONG",
            )

    def test_credit_applied_cannot_be_negative(self):
        with pytest.raises(ValidationError):
            Phase0UpgradeBridgeState(
                workspace_id="ws-1",
                prospect_id="P-1",
                target_tier="coach_os",
                credit_applied_cents=-1,
            )
