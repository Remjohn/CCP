"""
FR-ERA3-34 Phase-0 Workspace Service
====================================
Shared workspace lifecycle and readiness computation.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_intake_models import Phase0ProspectPacket
from src.ccp.models.phase0_workspace_models import (
    Phase0ArtifactFamily,
    Phase0ArtifactRecord,
    Phase0ArtifactStatus,
    Phase0DeliveryWindowStatus,
    Phase0ReadinessState,
    Phase0UpgradeBridgeState,
    Phase0WorkspaceRecord,
    Phase0WorkspaceStatus,
    utc_now_iso,
)


WORKSPACE_ALLOWED_TRANSITIONS: dict[Phase0WorkspaceStatus, set[Phase0WorkspaceStatus]] = {
    Phase0WorkspaceStatus.CREATED: {Phase0WorkspaceStatus.INTAKE_RECEIVED, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.INTAKE_RECEIVED: {Phase0WorkspaceStatus.ARTIFACTS_COLLECTING, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.ARTIFACTS_COLLECTING: {Phase0WorkspaceStatus.AUDIT_IN_PROGRESS, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.AUDIT_IN_PROGRESS: {Phase0WorkspaceStatus.PREVIEW_READY, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.PREVIEW_READY: {Phase0WorkspaceStatus.DELIVERED, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.DELIVERED: {Phase0WorkspaceStatus.PAYMENT_UNLOCKED, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.PAYMENT_UNLOCKED: {Phase0WorkspaceStatus.UPGRADED, Phase0WorkspaceStatus.BLOCKED},
    Phase0WorkspaceStatus.UPGRADED: {Phase0WorkspaceStatus.ARCHIVED},
    Phase0WorkspaceStatus.ARCHIVED: set(),
    Phase0WorkspaceStatus.BLOCKED: set(),
}


class Phase0WorkspaceService:
    """Workspace lifecycle manager for shared pre-container Phase-0 records."""

    def __init__(
        self,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "P0W",
    ) -> None:
        self._rc = receipt_chain or ReceiptChain(coach_acronym=coach_acronym)
        self.workspaces: dict[str, Phase0WorkspaceRecord] = {}
        self.manifests_by_workspace: dict[str, object] = {}
        self.upgrade_bridges: dict[str, Phase0UpgradeBridgeState] = {}
        self._previous_status_by_workspace: dict[str, Phase0WorkspaceStatus] = {}
        self._artifact_provider: Optional[Callable[[str], list[Phase0ArtifactRecord]]] = None

    def set_artifact_provider(self, provider: Callable[[str], list[Phase0ArtifactRecord]]) -> None:
        self._artifact_provider = provider

    def create_workspace(self, prospect_packet: Phase0ProspectPacket) -> Phase0WorkspaceRecord:
        if not prospect_packet.prospect_id.strip():
            entry = self._rc.log(
                agent_id="phase0_workspace_service",
                action="PHASE0-WORKSPACE-CREATE-FAIL",
                asset_id=prospect_packet.packet_id,
                person_id=prospect_packet.prospect_id or None,
                input_summary="Create Phase-0 workspace",
                output_summary="Workspace rejected",
                decision="rejected",
                decision_rationale="prospect_id is empty",
            )
            raise ValueError(f"WORKSPACE_CREATE_REJECTED: prospect_id is empty ({entry.receipt_id})")

        if not prospect_packet.packet_id.strip():
            entry = self._rc.log(
                agent_id="phase0_workspace_service",
                action="PHASE0-WORKSPACE-CREATE-FAIL",
                asset_id=None,
                person_id=prospect_packet.prospect_id,
                input_summary="Create Phase-0 workspace",
                output_summary="Workspace rejected",
                decision="rejected",
                decision_rationale="prospect_packet_id is empty",
            )
            raise ValueError(f"WORKSPACE_CREATE_REJECTED: prospect_packet_id is empty ({entry.receipt_id})")

        deadline = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        create_receipt = self._rc.log(
            agent_id="phase0_workspace_service",
            action="PHASE0-WORKSPACE-CREATE",
            asset_id=prospect_packet.packet_id,
            person_id=prospect_packet.prospect_id,
            input_summary=f"Create workspace for {prospect_packet.display_name}",
            output_summary="Workspace created and intake received",
            decision="approved",
            metadata={"coach_id": prospect_packet.coach_id or "", "campaign_metadata": prospect_packet.campaign_metadata},
        )
        record = Phase0WorkspaceRecord(
            prospect_id=prospect_packet.prospect_id,
            prospect_packet_id=prospect_packet.packet_id,
            coach_id=prospect_packet.coach_id,
            display_name=prospect_packet.display_name,
            status=Phase0WorkspaceStatus.INTAKE_RECEIVED,
            campaign_id=str(prospect_packet.campaign_metadata.get("campaign_id", "")) or None,
            delivery_sla_deadline_utc=deadline,
            created_by_receipt_id=create_receipt.receipt_id,
            last_transition_receipt_id=create_receipt.receipt_id,
        )
        self.workspaces[record.workspace_id] = record
        return record

    def get_workspace(self, workspace_id: str) -> Phase0WorkspaceRecord:
        if workspace_id not in self.workspaces:
            raise ValueError(f"Workspace {workspace_id} not found")
        return self.workspaces[workspace_id]

    def transition_workspace(
        self,
        workspace_id: str,
        target_status: Phase0WorkspaceStatus,
        human_review_note: Optional[str] = None,
    ) -> Phase0WorkspaceRecord:
        workspace = self.get_workspace(workspace_id)
        current = workspace.status

        if current == Phase0WorkspaceStatus.BLOCKED:
            previous = self._previous_status_by_workspace.get(workspace_id)
            if previous is None or target_status != previous:
                raise ValueError("ILLEGAL_WORKSPACE_TRANSITION: blocked workspaces can only recover to prior state")
            if not human_review_note or not human_review_note.strip():
                raise ValueError("RECOVERY_NOTE_REQUIRED")
            receipt = self._rc.log(
                agent_id="phase0_workspace_service",
                action="PHASE0-WORKSPACE-HUMAN-RECOVERY",
                asset_id=workspace.workspace_id,
                person_id=workspace.prospect_id,
                input_summary=f"Recover workspace from blocked to {target_status.value}",
                output_summary="Workspace recovered",
                decision="approved",
                metadata={"note": human_review_note},
            )
            workspace.status = target_status
            workspace.updated_at = utc_now_iso()
            workspace.last_transition_receipt_id = receipt.receipt_id
            return workspace

        if target_status == Phase0WorkspaceStatus.BLOCKED:
            if current in {Phase0WorkspaceStatus.UPGRADED, Phase0WorkspaceStatus.ARCHIVED}:
                raise ValueError(f"ILLEGAL_WORKSPACE_TRANSITION: {current.value} -> blocked")
            self._previous_status_by_workspace[workspace_id] = current
        elif target_status not in WORKSPACE_ALLOWED_TRANSITIONS[current]:
            raise ValueError(f"ILLEGAL_WORKSPACE_TRANSITION: {current.value} -> {target_status.value}")

        if target_status == Phase0WorkspaceStatus.DELIVERED:
            readiness = self.compute_readiness(workspace_id)
            if readiness.blocking_families:
                raise ValueError(
                    f"WORKSPACE_DELIVERY_BLOCKED: blocking families={','.join(readiness.blocking_families)}"
                )
        if target_status == Phase0WorkspaceStatus.UPGRADED:
            matching_bridges = [b for b in self.upgrade_bridges.values() if b.workspace_id == workspace_id]
            if not matching_bridges or not any(b.payment_confirmed for b in matching_bridges):
                raise PermissionError("MIGRATION_BLOCKED: payment_confirmed=False")

        receipt = self._rc.log(
            agent_id="phase0_workspace_service",
            action="PHASE0-WORKSPACE-TRANSITION",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary=f"{current.value} -> {target_status.value}",
            output_summary="Workspace transitioned",
            decision="approved",
        )
        workspace.status = target_status
        workspace.updated_at = utc_now_iso()
        workspace.last_transition_receipt_id = receipt.receipt_id
        return workspace

    def compute_readiness(self, workspace_id: str) -> Phase0ReadinessState:
        workspace = self.get_workspace(workspace_id)
        artifacts = self._artifact_provider(workspace_id) if self._artifact_provider else []
        now = datetime.now(timezone.utc)
        deadline = (
            datetime.fromisoformat(workspace.delivery_sla_deadline_utc)
            if workspace.delivery_sla_deadline_utc
            else None
        )

        blocking_families: list[str] = []
        warning_families: list[str] = []
        quarantined = [a.artifact_id for a in artifacts if a.status == Phase0ArtifactStatus.QUARANTINED]
        rejected = [a.artifact_id for a in artifacts if a.status == Phase0ArtifactStatus.REJECTED]

        required_families = {Phase0ArtifactFamily.AUDIT_REPORT.value, Phase0ArtifactFamily.PREVIEW_ASSET.value}
        for family in required_families:
            family_records = [a for a in artifacts if a.family.value == family]
            if not family_records:
                blocking_families.append(family)
                continue
            if not any(
                a.status
                in {
                    Phase0ArtifactStatus.PREVIEW_READY,
                    Phase0ArtifactStatus.DELIVERED,
                    Phase0ArtifactStatus.PAYMENT_UNLOCKED,
                    Phase0ArtifactStatus.UPGRADED,
                }
                for a in family_records
            ):
                blocking_families.append(family)
            elif not all(
                a.status
                in {
                    Phase0ArtifactStatus.PREVIEW_READY,
                    Phase0ArtifactStatus.DELIVERED,
                    Phase0ArtifactStatus.PAYMENT_UNLOCKED,
                    Phase0ArtifactStatus.UPGRADED,
                }
                for a in family_records
            ):
                warning_families.append(family)

        human_review_required = bool(quarantined or rejected)

        if workspace.status in {
            Phase0WorkspaceStatus.DELIVERED,
            Phase0WorkspaceStatus.PAYMENT_UNLOCKED,
            Phase0WorkspaceStatus.UPGRADED,
            Phase0WorkspaceStatus.ARCHIVED,
        }:
            delivery_window_status = Phase0DeliveryWindowStatus.DELIVERED
            hours_remaining = 0.0
        elif deadline is None:
            delivery_window_status = Phase0DeliveryWindowStatus.NOT_STARTED
            hours_remaining = None
        else:
            hours_raw = (deadline - now).total_seconds() / 3600.0
            hours_remaining = max(hours_raw, 0.0)
            if hours_raw <= 0:
                delivery_window_status = Phase0DeliveryWindowStatus.BREACHED
                human_review_required = True
                self._rc.log(
                    agent_id="phase0_workspace_service",
                    action="PHASE0-SLA-BREACH",
                    asset_id=workspace.workspace_id,
                    person_id=workspace.prospect_id,
                    input_summary="Compute Phase-0 readiness",
                    output_summary="Workspace breached 24h SLA",
                    decision="flagged",
                )
            elif hours_raw <= 6:
                delivery_window_status = Phase0DeliveryWindowStatus.AT_RISK
            else:
                delivery_window_status = Phase0DeliveryWindowStatus.ON_TRACK

        if human_review_required:
            summary = "Workspace requires human review due to quarantined or rejected artifacts."
        elif blocking_families:
            summary = f"Workspace blocked by missing delivery families: {', '.join(blocking_families)}."
        elif warning_families:
            summary = f"Workspace conditionally ready with partial families: {', '.join(warning_families)}."
        else:
            summary = "Workspace is ready and on track."

        receipt = self._rc.log(
            agent_id="phase0_workspace_service",
            action="PHASE0-READINESS-COMPUTE",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary="Compute readiness from artifact state machine",
            output_summary=f"{delivery_window_status.value} / blockers={len(blocking_families)}",
            decision="approved",
        )

        return Phase0ReadinessState(
            workspace_id=workspace.workspace_id,
            prospect_id=workspace.prospect_id,
            workspace_status=workspace.status,
            delivery_window_status=delivery_window_status,
            sla_deadline_utc=workspace.delivery_sla_deadline_utc,
            hours_remaining=hours_remaining,
            blocking_families=blocking_families,
            warning_families=warning_families,
            quarantined_artifact_ids=quarantined,
            rejected_artifact_ids=rejected,
            human_review_required=human_review_required,
            readiness_summary=summary,
            computation_receipt_id=receipt.receipt_id,
        )
