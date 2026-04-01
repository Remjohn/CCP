"""
CCP FR-CA11-03 — Client Workspace Provisioning (Gated Learning Environment)
DEP-ENG-073 PROPOSED

Provisions client-facing AFFiNE workspaces with content gating.
Triggered by CBCS Telegram onboarding (FR27). Content blocks are
provisioned by absence (not hidden — absent) based on coping_trajectory
and atlas_roadmap gating conditions.

Spec reference: FR-CA11-03_Client_Workspace_Provisioning_Tech_Spec.md
  §4 — Stage 1: Client Template Construction
  §4 — Stage 2: Provisioning Engine (Pierre)
  §4 — Stage 3: Content Gating Engine (Noémie)
  §5 — DEP-ENG-073 PROPOSED (ClientWorkspaceProvisioningPayload)
  §6 — Backward Compatibility: Telegram-only fallback
  §7 — Tasks 1-7
  §8 — AC1-AC6

Architecture references:
  ADR-01: Single-Tenant Isolated Cloud-Native Instances
  ADR-05: AFFiNE Over Notion
  FR-CA11-01/DEP-ENG-071: Coach workspace (theme inheritance)
  FR47/DEP-ENG-041: Receipt Chain Guard schema

Agent Roles:
  Pierre — AFFiNE Workspace Orchestrator (provisioning)
  Noémie — Content Gating Agent (unlock logic)
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ca11_models import (
    CLIENT_READONLY_SECTIONS,
    CLIENT_READWRITE_SECTIONS,
    CLIENT_REQUIRED_SECTIONS,
    CLIENT_WORKSPACE_SECTIONS_COUNT,
    ClientProvisioningResult,
    ClientProvisioningStatus,
    ClientWorkspaceProvisioningPayload,
    ClientWorkspaceSection,
    ContentBlock,
    ContentPermission,
    ContentUnlockResult,
    GatingSnapshot,
    ReceiptChainGuardRef,
    UnlockCondition,
)

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

AGENT_PIERRE = "Pierre"
AGENT_NOEMIE = "Noémie"

# Default template directory
DEFAULT_TEMPLATE_DIR = Path("src/ccp/templates")

# AFFiNE base URL
AFFINE_BASE_URL_DEFAULT = "https://os.consciouselite.com"


# ── SQL Schema ────────────────────────────────────────────────────────────────
# Task 4: Add client_workspace_id to cbcs_clients table

CLIENT_WORKSPACE_SQL = """
ALTER TABLE cbcs_clients
    ADD COLUMN IF NOT EXISTS client_workspace_id UUID,
    ADD COLUMN IF NOT EXISTS client_workspace_url TEXT,
    ADD COLUMN IF NOT EXISTS client_workspace_program_id TEXT,
    ADD COLUMN IF NOT EXISTS client_workspace_status TEXT DEFAULT 'QUEUED'
        CHECK (client_workspace_status IN ('SUCCESS', 'QUEUED', 'FAILED_TELEGRAM_ONLY'));
"""


# ══════════════════════════════════════════════════════════════════════════════
# Unit 3 — Content Gating Engine (Agent: Noémie)
# ══════════════════════════════════════════════════════════════════════════════


class ContentGatingEngine:
    """Noémie — Content Gating Agent.

    Evaluates which content blocks should be unlocked for a client
    based on their coping_trajectory position and atlas_roadmap week.

    Key design decision (§4 Technical Decisions #1): Gating by Absence.
    Content blocks that are not yet unlocked do not exist in the workspace.
    They are provisioned only when the unlock condition is met.
    """

    @staticmethod
    def parse_template_blocks(template_data: dict) -> list[ContentBlock]:
        """Extract content blocks from a client template JSON."""
        blocks: list[ContentBlock] = []
        for section in template_data.get("sections", []):
            if section.get("section_type") != "learning_library":
                continue
            for block_data in section.get("content_blocks", []):
                blocks.append(ContentBlock(
                    block_id=block_data["block_id"],
                    title=block_data["title"],
                    content_type=block_data["content_type"],
                    program_tag=block_data["program_tag"],
                    unlock_condition=UnlockCondition(**block_data["unlock_condition"]),
                    permission=ContentPermission.READ_ONLY,
                ))
        return blocks

    @staticmethod
    def evaluate_unlockable(
        blocks: list[ContentBlock],
        coping_position: int,
        atlas_week: int,
    ) -> list[ContentBlock]:
        """Determine which blocks are unlockable given current gating state.

        A block is unlockable if BOTH conditions are met:
          coping_position >= min_coping_position AND
          atlas_week >= min_atlas_week

        Returns only blocks whose conditions are satisfied.
        """
        unlockable: list[ContentBlock] = []
        for block in blocks:
            cond = block.unlock_condition
            if (
                coping_position >= cond.min_coping_position
                and atlas_week >= cond.min_atlas_week
            ):
                unlockable.append(block)
        return unlockable

    @staticmethod
    def evaluate_newly_unlockable(
        blocks: list[ContentBlock],
        already_provisioned_ids: set[str],
        coping_position: int,
        atlas_week: int,
    ) -> list[ContentBlock]:
        """Find blocks that are now unlockable but not yet provisioned.

        Used for progressive unlock (AC3).
        """
        all_unlockable = ContentGatingEngine.evaluate_unlockable(
            blocks, coping_position, atlas_week
        )
        return [b for b in all_unlockable if b.block_id not in already_provisioned_ids]

    @staticmethod
    def validate_unlock_request(
        block: ContentBlock,
        actual_coping_position: int,
        actual_atlas_week: int,
    ) -> bool:
        """Validate that a client has actually achieved the unlock threshold.

        Safety test: §10 Premature Unlock Prevention.
        Reject if the client hasn't actually reached the required position.
        """
        cond = block.unlock_condition
        return (
            actual_coping_position >= cond.min_coping_position
            and actual_atlas_week >= cond.min_atlas_week
        )


# ══════════════════════════════════════════════════════════════════════════════
# Unit 4 — Client Workspace Provisioner (Agent: Pierre)
# ══════════════════════════════════════════════════════════════════════════════


class ClientWorkspaceProvisioner:
    """Pierre — provisions client AFFiNE workspaces.

    Triggered by CBCS onboarding (FR27) via Vidye.
    Creates workspace from program template, applies coach theme,
    provisions only unlocked content blocks, registers in Supabase.

    AC1: Provisioning on Onboarding
    AC2: Content Gating (only unlocked content exists)
    AC4: Read-Only Enforcement
    AC5: Cross-Client Isolation
    AC6: Telegram-Only Fallback
    """

    def __init__(
        self,
        coach_acronym: str,
        affine_client: Any = None,
        supabase_client: Any = None,
        telegram_client: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
        template_dir: Optional[Path] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self._affine = affine_client
        self._supabase = supabase_client
        self._telegram = telegram_client
        self._receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )
        self._template_dir = template_dir or DEFAULT_TEMPLATE_DIR
        self._gating = ContentGatingEngine()
        # Track provisioned blocks per client (in-memory for service lifetime)
        self._client_blocks: dict[str, set[str]] = {}

    def load_program_template(self, program_id: str) -> dict:
        """Load a program-specific client template JSON."""
        template_path = self._template_dir / f"client_{program_id.replace('-', '_')}.json"
        if not template_path.exists():
            raise FileNotFoundError(
                f"Client template not found: {template_path}"
            )
        with open(template_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_section_permission(self, section_type: str) -> ContentPermission:
        """Determine permission level for a section (AC4 Read-Only Enforcement)."""
        if section_type in CLIENT_READWRITE_SECTIONS:
            return ContentPermission.READ_WRITE
        return ContentPermission.READ_ONLY

    async def provision_client_workspace(
        self,
        client_id: str,
        coach_id: str,
        program_id: str,
        coach_theme_file: str,
        coping_position: int = 0,
        atlas_week: int = 0,
        capacity_track: str = "Foundation",
    ) -> ClientProvisioningResult:
        """Full client workspace provisioning pipeline.

        Steps (§4 Stage 2):
        1. Load program template
        2. Create AFFiNE workspace
        3. Apply coach theme (inherited from FR-CA11-01)
        4. Evaluate content gating → provision only unlocked blocks
        5. Register in Supabase
        6. Send Telegram notification
        7. Write receipt
        """
        gating_snapshot = GatingSnapshot(
            coping_position=coping_position,
            atlas_week=atlas_week,
            capacity_track=capacity_track,
        )

        try:
            # Step 1: Load template
            template_data = self.load_program_template(program_id)

            # Step 2: Create workspace via AFFiNE
            workspace_id, workspace_url = await self._create_workspace(
                client_id, program_id, template_data
            )

            # Step 3: Apply coach theme
            await self._apply_theme(workspace_id, coach_theme_file)

            # Step 4: Content gating
            all_blocks = self._gating.parse_template_blocks(template_data)
            unlocked = self._gating.evaluate_unlockable(
                all_blocks, coping_position, atlas_week
            )

            # Provision unlocked blocks
            provisioned_ids = set()
            for block in unlocked:
                await self._provision_block(workspace_id, block)
                provisioned_ids.add(block.block_id)
            self._client_blocks[client_id] = provisioned_ids

            # Determine provisioned sections
            sections_provisioned = self._get_provisioned_sections(
                template_data, unlocked
            )

            # Step 5: Register in Supabase
            await self._register_client_workspace(
                client_id, workspace_id, workspace_url, program_id
            )

            # Step 6: Telegram notification
            await self._send_telegram_notification(
                client_id, workspace_url, "created"
            )

            # Step 7: Write receipt
            payload = ClientWorkspaceProvisioningPayload(
                client_id=client_id,
                coach_id=coach_id,
                program_id=program_id,
                workspace_id=workspace_id,
                workspace_url=workspace_url,
                theme_inherited_from=coach_theme_file,
                sections_provisioned=sections_provisioned,
                learning_library_blocks_unlocked=len(unlocked),
                learning_library_blocks_total=len(all_blocks),
                gating_snapshot=gating_snapshot,
            )
            self._write_receipt(
                action="provision_client_workspace",
                asset_id=f"CLIENT-WS-{client_id[:8]}",
                payload=payload,
            )

            return ClientProvisioningResult(
                status=ClientProvisioningStatus.SUCCESS,
                payload=payload,
            )

        except Exception as exc:
            logger.error(
                "Client workspace provisioning failed for %s: %s",
                client_id,
                exc,
            )
            return self._handle_fallback(client_id, str(exc))

    async def unlock_content(
        self,
        client_id: str,
        program_id: str,
        workspace_id: str,
        coping_position: int,
        atlas_week: int,
    ) -> ContentUnlockResult:
        """Progressive content unlock — triggered by coping/atlas changes (AC3).

        Agent: Noémie evaluates newly unlockable blocks and provisions them.
        """
        template_data = self.load_program_template(program_id)
        all_blocks = self._gating.parse_template_blocks(template_data)
        already_provisioned = self._client_blocks.get(client_id, set())

        newly_unlockable = self._gating.evaluate_newly_unlockable(
            all_blocks, already_provisioned, coping_position, atlas_week
        )

        unlocked_ids: list[str] = []
        for block in newly_unlockable:
            # Safety: Validate the unlock is legitimate
            if not self._gating.validate_unlock_request(
                block, coping_position, atlas_week
            ):
                logger.warning(
                    "Premature unlock rejected for client %s block %s",
                    client_id,
                    block.block_id,
                )
                continue

            await self._provision_block(workspace_id, block)
            unlocked_ids.append(block.block_id)
            already_provisioned.add(block.block_id)

        self._client_blocks[client_id] = already_provisioned

        # Telegram notification if new content was unlocked
        telegram_notified = False
        if unlocked_ids:
            await self._send_telegram_notification(
                client_id, "", "unlocked"
            )
            telegram_notified = True

        new_snapshot = GatingSnapshot(
            coping_position=coping_position,
            atlas_week=atlas_week,
        )

        return ContentUnlockResult(
            client_id=client_id,
            blocks_unlocked=unlocked_ids,
            blocks_already_provisioned=list(already_provisioned - set(unlocked_ids)),
            new_gating_snapshot=new_snapshot,
            telegram_notified=telegram_notified,
        )

    def validate_workspace_access(
        self, client_id: str, workspace_id: str
    ) -> bool:
        """Cross-client isolation check (AC5).

        Verifies that the requesting client owns the workspace.
        """
        if self._supabase is not None:
            try:
                result = self._supabase.get_client_workspace(client_id)
                return result.get("client_workspace_id") == workspace_id
            except Exception:
                return False
        return False

    def check_write_permission(
        self, section_type: str
    ) -> bool:
        """Read-only enforcement check (AC4).

        Only journal section allows client writes.
        """
        return section_type in CLIENT_READWRITE_SECTIONS

    # ── Internal Helpers ──────────────────────────────────────────────────

    async def _create_workspace(
        self, client_id: str, program_id: str, template_data: dict
    ) -> tuple[str, str]:
        """Create AFFiNE workspace from template."""
        if self._affine is not None:
            result = await self._affine.create_workspace(
                name=f"Client-{client_id[:8]}-{program_id}",
                template=template_data,
            )
            ws_id = result.get("workspace_id", str(uuid.uuid4()))
            ws_url = result.get(
                "workspace_url",
                f"{AFFINE_BASE_URL_DEFAULT}/ws/{ws_id}",
            )
            return ws_id, ws_url

        # Mock/fallback: generate IDs
        ws_id = str(uuid.uuid4())
        return ws_id, f"{AFFINE_BASE_URL_DEFAULT}/ws/{ws_id}"

    async def _apply_theme(self, workspace_id: str, theme_file: str) -> None:
        """Apply coach CSS theme to client workspace."""
        if self._affine is not None:
            await self._affine.apply_theme(workspace_id, theme_file)

    async def _provision_block(
        self, workspace_id: str, block: ContentBlock
    ) -> None:
        """Provision a single content block in the client workspace."""
        if self._affine is not None:
            await self._affine.create_entry(
                workspace_id=workspace_id,
                section_id="learning_library",
                entry_data=block.model_dump(mode="json"),
            )

    async def _register_client_workspace(
        self,
        client_id: str,
        workspace_id: str,
        workspace_url: str,
        program_id: str,
    ) -> None:
        """Register client workspace in Supabase cbcs_clients table."""
        if self._supabase is not None:
            self._supabase.register_client_workspace(
                client_id=client_id,
                workspace_id=workspace_id,
                workspace_url=workspace_url,
                program_id=program_id,
            )

    async def _send_telegram_notification(
        self, client_id: str, workspace_url: str, event_type: str
    ) -> None:
        """Send Telegram message about workspace event."""
        if self._telegram is not None:
            if event_type == "created":
                msg = (
                    f"Your personal coaching space is ready! "
                    f"Access it here: {workspace_url}"
                )
            else:
                msg = "New content unlocked in your coaching space! 🎉"
            await self._telegram.send_message(client_id, msg)

    def _get_provisioned_sections(
        self, template_data: dict, unlocked_blocks: list[ContentBlock]
    ) -> list[str]:
        """Determine which root sections are provisioned."""
        sections = []
        for section in template_data.get("sections", []):
            st = section.get("section_type", "")
            if st == "learning_library":
                # Only include if any blocks are unlocked
                if unlocked_blocks:
                    sections.append(st)
            else:
                sections.append(st)
        return sections

    def _handle_fallback(
        self, client_id: str, error_detail: str
    ) -> ClientProvisioningResult:
        """Telegram-only fallback (AC6).

        If AFFiNE is unreachable, client continues on Telegram.
        Workspace creation is queued for retry.
        """
        return ClientProvisioningResult(
            status=ClientProvisioningStatus.QUEUED,
            error_detail=error_detail,
            telegram_fallback_active=True,
        )

    def _write_receipt(
        self, action: str, asset_id: str, payload: Any
    ) -> str:
        """Write provisioning receipt to Receipt Chain Guard."""
        if hasattr(payload, "model_dump"):
            data = payload.model_dump(mode="json")
        else:
            data = str(payload)
        payload_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True, default=str).encode()
        ).hexdigest()

        entry = self._receipt_chain.log(
            agent_id=AGENT_PIERRE,
            action=action,
            asset_id=asset_id,
            input_summary=f"Client workspace payload hash: {payload_hash}",
            output_summary=f"Client workspace provisioned",
            decision="provisioned",
            metadata={"schema_ref": "DEP-ENG-041"},
        )
        return entry.receipt_id
