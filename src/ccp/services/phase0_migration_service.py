"""
FR-ERA3-34 Phase-0 Migration Service
====================================
Upgrade bridge state and guarded migration into coach tenancy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_workspace_models import (
    Phase0ArtifactFamily,
    Phase0ArtifactStatus,
    Phase0MigrationResult,
    Phase0UpgradeBridgeState,
    Phase0WorkspaceStatus,
    utc_now_iso,
)
from src.ccp.scripts.scaffold_coach import scaffold_coach
from src.ccp.services.phase0_artifact_store import Phase0ArtifactStore
from src.ccp.services.phase0_workspace_service import Phase0WorkspaceService


VALID_TARGET_TIERS = {"speaking_learning", "coach_os", "operator"}


class Phase0MigrationService:
    """Upgrade bridge manager and copy-then-archive migration executor."""

    def __init__(
        self,
        workspace_service: Phase0WorkspaceService,
        artifact_store: Phase0ArtifactStore,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "P0W",
        scaffold_root: Optional[Path] = None,
    ) -> None:
        self._workspace_service = workspace_service
        self._artifact_store = artifact_store
        self._rc = receipt_chain or ReceiptChain(coach_acronym=coach_acronym)
        self._scaffold_root = Path(scaffold_root) if scaffold_root else Path("coaches")

    def initiate_upgrade_bridge(
        self,
        workspace_id: str,
        target_tier: str,
        *,
        payment_amount_cents: Optional[int] = None,
        credit_applied_cents: Optional[int] = None,
    ) -> Phase0UpgradeBridgeState:
        if target_tier not in VALID_TARGET_TIERS:
            raise ValueError(f"INVALID_TARGET_TIER: {target_tier}")
        workspace = self._workspace_service.get_workspace(workspace_id)
        receipt = self._rc.log(
            agent_id="phase0_migration_service",
            action="PHASE0-UPGRADE-INITIATE",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary=f"Initiate upgrade bridge to {target_tier}",
            output_summary="Upgrade bridge pending",
            decision="approved",
        )
        bridge = Phase0UpgradeBridgeState(
            workspace_id=workspace.workspace_id,
            prospect_id=workspace.prospect_id,
            target_tier=target_tier,
            payment_amount_cents=payment_amount_cents,
            credit_applied_cents=credit_applied_cents,
            migration_receipt_id=receipt.receipt_id,
        )
        self._workspace_service.upgrade_bridges[bridge.bridge_id] = bridge
        return bridge

    def confirm_payment(
        self,
        bridge_id: str,
        payment_receipt_id: str,
        *,
        payment_amount_cents: Optional[int] = None,
        credit_applied_cents: Optional[int] = None,
    ) -> Phase0UpgradeBridgeState:
        bridge = self._get_bridge(bridge_id)
        workspace = self._workspace_service.get_workspace(bridge.workspace_id)
        receipt = self._rc.log(
            agent_id="phase0_migration_service",
            action="PHASE0-PAYMENT-CONFIRM",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary=f"Confirm payment for {bridge.target_tier}",
            output_summary="Payment confirmed",
            decision="approved",
            parent_receipt_id=payment_receipt_id,
        )
        bridge.payment_confirmed = True
        bridge.payment_receipt_id = payment_receipt_id
        if payment_amount_cents is not None:
            bridge.payment_amount_cents = payment_amount_cents
        if credit_applied_cents is not None:
            bridge.credit_applied_cents = credit_applied_cents
        bridge.confirmed_at = utc_now_iso()
        bridge.migration_receipt_id = receipt.receipt_id
        if workspace.status == Phase0WorkspaceStatus.DELIVERED:
            self._workspace_service.transition_workspace(workspace.workspace_id, Phase0WorkspaceStatus.PAYMENT_UNLOCKED)
        return bridge

    def abort_upgrade(self, bridge_id: str, reason: str) -> Phase0UpgradeBridgeState:
        bridge = self._get_bridge(bridge_id)
        workspace = self._workspace_service.get_workspace(bridge.workspace_id)
        receipt = self._rc.log(
            agent_id="phase0_migration_service",
            action="PHASE0-UPGRADE-ABORT",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary=f"Abort upgrade bridge {bridge_id}",
            output_summary="Upgrade aborted",
            decision="approved",
            decision_rationale=reason,
        )
        bridge.migration_status = "aborted"
        bridge.abort_reason = reason
        bridge.migration_receipt_id = receipt.receipt_id
        return bridge

    def migrate_to_container(self, workspace_id: str, coach_acronym: str) -> Phase0MigrationResult:
        workspace = self._workspace_service.get_workspace(workspace_id)
        bridge = self._find_bridge_for_workspace(workspace_id)
        if bridge is None or not bridge.payment_confirmed:
            self._rc.log(
                agent_id="phase0_migration_service",
                action="PHASE0-MIGRATION-BLOCKED",
                asset_id=workspace.workspace_id,
                person_id=workspace.prospect_id,
                input_summary=f"Migrate workspace to {coach_acronym}",
                output_summary="Migration rejected",
                decision="rejected",
                decision_rationale="payment_confirmed=False",
            )
            raise PermissionError(f"MIGRATION_BLOCKED: payment_confirmed=False for workspace_id={workspace_id}")
        if bridge.migration_status != "pending":
            raise ValueError(f"MIGRATION_BLOCKED: bridge migration_status={bridge.migration_status}")

        coach_acronym = coach_acronym.upper()
        coach_dir = self._scaffold_root / coach_acronym
        scaffold_path = scaffold_coach(
            coach_name=workspace.display_name,
            acronym=coach_acronym,
            output_dir=str(coach_dir),
            phase0_source_workspace_id=workspace.workspace_id,
        )

        target_gen = AssetIDGenerator(coach_acronym=coach_acronym)
        artifacts = self._artifact_store.get_artifacts_by_workspace(workspace_id)
        remapped_ids: dict[str, str] = {}
        for artifact in artifacts:
            new_asset_id = target_gen.generate(AssetType.PHASE0_ARTIFACT)
            remapped_ids[artifact.artifact_id] = new_asset_id
            artifact.metadata["migrated_to_asset_id"] = new_asset_id
            artifact.metadata["target_coach_acronym"] = coach_acronym
            artifact.status = Phase0ArtifactStatus.UPGRADED
            artifact.updated_at = utc_now_iso()
            artifact.transitioned_at = artifact.updated_at

        receipt = self._rc.log(
            agent_id="phase0_migration_service",
            action="PHASE0-MIGRATION-EXECUTE",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary=f"Migrate workspace to coach {coach_acronym}",
            output_summary=f"Migrated {len(artifacts)} artifacts and archived source workspace",
            decision="approved",
        )

        bridge.target_coach_acronym = coach_acronym
        bridge.migration_status = "completed"
        bridge.completed_at = utc_now_iso()
        bridge.migration_receipt_id = receipt.receipt_id

        upgrade_meta = self._artifact_store.register_artifact(
            workspace_id=workspace_id,
            family=Phase0ArtifactFamily.UPGRADE_METADATA,
            source_receipt_id=receipt.receipt_id,
            display_label=f"Migration manifest for {coach_acronym}",
            parent_artifact_ids=[a.artifact_id for a in artifacts] if artifacts else [],
            metadata={"scaffold_path": str(scaffold_path), "target_coach_acronym": coach_acronym},
        ) if artifacts else None
        if upgrade_meta is not None:
            upgrade_meta.status = Phase0ArtifactStatus.UPGRADED

        workspace.status = Phase0WorkspaceStatus.ARCHIVED
        workspace.updated_at = utc_now_iso()
        workspace.last_transition_receipt_id = receipt.receipt_id

        return Phase0MigrationResult(
            workspace_id=workspace.workspace_id,
            prospect_id=workspace.prospect_id,
            target_coach_acronym=coach_acronym,
            scaffold_path=str(scaffold_path),
            migrated_artifact_count=len(artifacts),
            remapped_asset_ids=remapped_ids,
            archived_workspace_status=workspace.status,
            migration_receipt_id=receipt.receipt_id,
        )

    def _get_bridge(self, bridge_id: str) -> Phase0UpgradeBridgeState:
        if bridge_id not in self._workspace_service.upgrade_bridges:
            raise ValueError(f"Bridge {bridge_id} not found")
        return self._workspace_service.upgrade_bridges[bridge_id]

    def _find_bridge_for_workspace(self, workspace_id: str) -> Optional[Phase0UpgradeBridgeState]:
        for bridge in self._workspace_service.upgrade_bridges.values():
            if bridge.workspace_id == workspace_id:
                return bridge
        return None
