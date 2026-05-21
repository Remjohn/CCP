"""
FR-ERA3-34 Phase-0 Artifact Store
=================================
Artifact lineage, state machine, and manifest assembly.
"""

from __future__ import annotations

from typing import Optional

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_workspace_models import (
    Phase0ArtifactFamily,
    Phase0ArtifactManifest,
    Phase0ArtifactRecord,
    Phase0ArtifactStatus,
    Phase0WorkspaceRecord,
    utc_now_iso,
)
from src.ccp.services.phase0_workspace_service import Phase0WorkspaceService


ARTIFACT_FORWARD_TRANSITIONS: dict[Phase0ArtifactStatus, Phase0ArtifactStatus] = {
    Phase0ArtifactStatus.UPLOADED: Phase0ArtifactStatus.NORMALIZED,
    Phase0ArtifactStatus.NORMALIZED: Phase0ArtifactStatus.AUDIT_READY,
    Phase0ArtifactStatus.AUDIT_READY: Phase0ArtifactStatus.PREVIEW_READY,
    Phase0ArtifactStatus.PREVIEW_READY: Phase0ArtifactStatus.DELIVERED,
    Phase0ArtifactStatus.DELIVERED: Phase0ArtifactStatus.PAYMENT_UNLOCKED,
    Phase0ArtifactStatus.PAYMENT_UNLOCKED: Phase0ArtifactStatus.UPGRADED,
}

PREVIEW_OR_BEYOND = {
    Phase0ArtifactStatus.PREVIEW_READY,
    Phase0ArtifactStatus.DELIVERED,
    Phase0ArtifactStatus.PAYMENT_UNLOCKED,
    Phase0ArtifactStatus.UPGRADED,
}


class Phase0ArtifactStore:
    """Artifact persistence and lineage validation for Phase-0."""

    def __init__(
        self,
        workspace_service: Phase0WorkspaceService,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "P0W",
        asset_id_generator: Optional[AssetIDGenerator] = None,
    ) -> None:
        self._workspace_service = workspace_service
        self._rc = receipt_chain or ReceiptChain(coach_acronym=coach_acronym)
        self._asset_gen = asset_id_generator or AssetIDGenerator(coach_acronym=coach_acronym)
        self.artifacts: dict[str, Phase0ArtifactRecord] = {}
        self._artifact_previous_status: dict[str, Phase0ArtifactStatus] = {}
        self._workspace_service.set_artifact_provider(self.get_artifacts_by_workspace)

    def register_artifact(
        self,
        workspace_id: str,
        family: Phase0ArtifactFamily,
        source_receipt_id: str,
        display_label: str,
        *,
        mime_type: Optional[str] = None,
        file_size_bytes: Optional[int] = None,
        storage_uri: Optional[str] = None,
        checksum_sha256: Optional[str] = None,
        parent_artifact_ids: Optional[list[str]] = None,
        metadata: Optional[dict[str, str]] = None,
    ) -> Phase0ArtifactRecord:
        workspace = self._workspace_service.get_workspace(workspace_id)
        if not source_receipt_id or not source_receipt_id.strip():
            raise ValueError("SOURCE_RECEIPT_REQUIRED")

        parent_artifact_ids = parent_artifact_ids or []
        if family != Phase0ArtifactFamily.INTAKE_SOURCE:
            if not parent_artifact_ids:
                raise ValueError(f"LINEAGE_VIOLATION: {family.value} requires at least one parent artifact ID")
            for parent_id in parent_artifact_ids:
                parent = self.artifacts.get(parent_id)
                if parent is None or parent.workspace_id != workspace_id:
                    raise ValueError("LINEAGE_VIOLATION: parent artifact must exist in same workspace")

        artifact_id = self._asset_gen.generate(AssetType.PHASE0_ARTIFACT)
        receipt = self._rc.log(
            agent_id="phase0_artifact_store",
            action="PHASE0-ARTIFACT-REGISTER",
            asset_id=artifact_id,
            person_id=workspace.prospect_id,
            input_summary=f"Register {family.value} artifact",
            output_summary=display_label,
            decision="approved",
            parent_receipt_id=source_receipt_id,
        )
        record = Phase0ArtifactRecord(
            artifact_id=artifact_id,
            workspace_id=workspace_id,
            prospect_id=workspace.prospect_id,
            family=family,
            display_label=display_label,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            storage_uri=storage_uri,
            checksum_sha256=checksum_sha256,
            parent_artifact_ids=parent_artifact_ids,
            source_receipt_id=source_receipt_id,
            metadata=metadata or {},
            transition_receipt_id=receipt.receipt_id,
        )
        self.artifacts[artifact_id] = record
        workspace.artifact_count += 1
        workspace.updated_at = utc_now_iso()
        return record

    def transition_artifact(
        self,
        artifact_id: str,
        target_status: Phase0ArtifactStatus,
        human_review_note: Optional[str] = None,
    ) -> Phase0ArtifactRecord:
        artifact = self._get_artifact(artifact_id)
        current = artifact.status

        if current == Phase0ArtifactStatus.UPGRADED:
            self._log_transition_fail(artifact, target_status, "upgraded is terminal")
            raise ValueError(f"ILLEGAL_ARTIFACT_TRANSITION: upgraded → {target_status.value}")

        if target_status == Phase0ArtifactStatus.QUARANTINED:
            self._artifact_previous_status[artifact_id] = current
            receipt = self._rc.log(
                agent_id="phase0_artifact_store",
                action="PHASE0-ARTIFACT-TRANSITION",
                asset_id=artifact.artifact_id,
                person_id=artifact.prospect_id,
                input_summary=f"{current.value} -> quarantined",
                output_summary="Artifact quarantined",
                decision="approved",
            )
            artifact.status = target_status
            artifact.updated_at = utc_now_iso()
            artifact.transitioned_at = artifact.updated_at
            artifact.transition_receipt_id = receipt.receipt_id
            return artifact

        if current == Phase0ArtifactStatus.QUARANTINED:
            previous = self._artifact_previous_status.get(artifact_id)
            if previous is None or target_status != previous:
                self._log_transition_fail(artifact, target_status, "quarantined recovery must return to prior state")
                raise ValueError("ILLEGAL_ARTIFACT_TRANSITION: quarantined artifacts can only recover to prior state")
            if not human_review_note or not human_review_note.strip():
                self._log_transition_fail(artifact, target_status, "recovery note missing")
                raise ValueError("RECOVERY_NOTE_REQUIRED")
            receipt = self._rc.log(
                agent_id="phase0_artifact_store",
                action="PHASE0-ARTIFACT-HUMAN-RECOVERY",
                asset_id=artifact.artifact_id,
                person_id=artifact.prospect_id,
                input_summary=f"Recover artifact to {target_status.value}",
                output_summary="Artifact recovered from quarantine",
                decision="approved",
                metadata={"note": human_review_note},
            )
            artifact.status = target_status
            artifact.updated_at = utc_now_iso()
            artifact.transitioned_at = artifact.updated_at
            artifact.transition_receipt_id = receipt.receipt_id
            return artifact

        if target_status == Phase0ArtifactStatus.REJECTED:
            receipt = self._rc.log(
                agent_id="phase0_artifact_store",
                action="PHASE0-ARTIFACT-TRANSITION",
                asset_id=artifact.artifact_id,
                person_id=artifact.prospect_id,
                input_summary=f"{current.value} -> rejected",
                output_summary="Artifact rejected",
                decision="approved",
            )
            artifact.status = target_status
            artifact.updated_at = utc_now_iso()
            artifact.transitioned_at = artifact.updated_at
            artifact.transition_receipt_id = receipt.receipt_id
            return artifact

        expected_next = ARTIFACT_FORWARD_TRANSITIONS.get(current)
        if expected_next != target_status:
            self._log_transition_fail(
                artifact,
                target_status,
                (
                    f"Required path: {current.value} → "
                    f"{expected_next.value if expected_next else 'terminal'}"
                ),
            )
            raise ValueError(
                f"ILLEGAL_ARTIFACT_TRANSITION: {current.value} → {target_status.value}. "
                "Required path: uploaded → normalized → audit_ready → preview_ready → delivered"
                " → payment_unlocked → upgraded"
            )

        receipt = self._rc.log(
            agent_id="phase0_artifact_store",
            action="PHASE0-ARTIFACT-TRANSITION",
            asset_id=artifact.artifact_id,
            person_id=artifact.prospect_id,
            input_summary=f"{current.value} -> {target_status.value}",
            output_summary="Artifact transitioned",
            decision="approved",
        )
        artifact.status = target_status
        artifact.updated_at = utc_now_iso()
        artifact.transitioned_at = artifact.updated_at
        artifact.transition_receipt_id = receipt.receipt_id
        return artifact

    def get_artifacts_by_workspace(self, workspace_id: str) -> list[Phase0ArtifactRecord]:
        workspace = self._workspace_service.get_workspace(workspace_id)
        return [a for a in self.artifacts.values() if a.workspace_id == workspace.workspace_id]

    def get_artifacts_by_family(
        self,
        workspace_id: str,
        family: Phase0ArtifactFamily,
    ) -> list[Phase0ArtifactRecord]:
        return [a for a in self.get_artifacts_by_workspace(workspace_id) if a.family == family]

    def assemble_manifest(self, workspace_id: str) -> Phase0ArtifactManifest:
        workspace = self._workspace_service.get_workspace(workspace_id)
        artifacts = self.get_artifacts_by_workspace(workspace_id)
        grouped: dict[Phase0ArtifactFamily, list[Phase0ArtifactRecord]] = {
            family: [a for a in artifacts if a.family == family]
            for family in Phase0ArtifactFamily
        }

        completeness_summary: dict[str, str] = {}
        for family, records in grouped.items():
            if not records:
                completeness_summary[family.value] = "missing"
            elif any(record.status in PREVIEW_OR_BEYOND for record in records):
                completeness_summary[family.value] = "present"
            else:
                completeness_summary[family.value] = "partial"

        receipt = self._rc.log(
            agent_id="phase0_artifact_store",
            action="PHASE0-MANIFEST-ASSEMBLE",
            asset_id=workspace.workspace_id,
            person_id=workspace.prospect_id,
            input_summary="Assemble workspace artifact manifest",
            output_summary=f"{len(artifacts)} artifacts grouped",
            decision="approved",
        )

        manifest = Phase0ArtifactManifest(
            workspace_id=workspace.workspace_id,
            prospect_id=workspace.prospect_id,
            assembly_receipt_id=receipt.receipt_id,
            intake_sources=[a.artifact_id for a in grouped[Phase0ArtifactFamily.INTAKE_SOURCE]],
            normalized_sources=[a.artifact_id for a in grouped[Phase0ArtifactFamily.NORMALIZED_SOURCE]],
            audit_reports=[a.artifact_id for a in grouped[Phase0ArtifactFamily.AUDIT_REPORT]],
            preview_assets=[a.artifact_id for a in grouped[Phase0ArtifactFamily.PREVIEW_ASSET]],
            produced_proofs=[a.artifact_id for a in grouped[Phase0ArtifactFamily.PRODUCED_PROOF]],
            payment_bridges=[a.artifact_id for a in grouped[Phase0ArtifactFamily.PAYMENT_BRIDGE]],
            upgrade_metadata_refs=[a.artifact_id for a in grouped[Phase0ArtifactFamily.UPGRADE_METADATA]],
            total_artifact_count=len(artifacts),
            completeness_summary=completeness_summary,
            is_delivery_ready=(
                completeness_summary[Phase0ArtifactFamily.AUDIT_REPORT.value] == "present"
                and completeness_summary[Phase0ArtifactFamily.PREVIEW_ASSET.value] == "present"
            ),
            is_payment_bridge_ready=(
                completeness_summary[Phase0ArtifactFamily.PAYMENT_BRIDGE.value] == "present"
            ),
        )
        self._workspace_service.manifests_by_workspace[workspace_id] = manifest
        return manifest

    def _get_artifact(self, artifact_id: str) -> Phase0ArtifactRecord:
        if artifact_id not in self.artifacts:
            raise ValueError(f"Artifact {artifact_id} not found")
        return self.artifacts[artifact_id]

    def _log_transition_fail(
        self,
        artifact: Phase0ArtifactRecord,
        target_status: Phase0ArtifactStatus,
        rationale: str,
    ) -> None:
        self._rc.log(
            agent_id="phase0_artifact_store",
            action="PHASE0-ARTIFACT-TRANSITION-FAIL",
            asset_id=artifact.artifact_id,
            person_id=artifact.prospect_id,
            input_summary=f"{artifact.status.value} -> {target_status.value}",
            output_summary="Artifact transition rejected",
            decision="rejected",
            decision_rationale=rationale,
        )
