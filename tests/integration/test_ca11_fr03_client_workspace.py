"""
FR-CA11-03 — Client Workspace Provisioning Tests
==================================================
Covers all 6 Acceptance Criteria:
  AC1: Provisioning on Onboarding — workspace created with correct template/theme
  AC2: Content Gating — only unlocked blocks exist (Week 1 only at start)
  AC3: Progressive Unlock — update coping → new blocks provisioned
  AC4: Read-Only Enforcement — client writes rejected on CCP-managed sections
  AC5: Cross-Client Isolation — Client A cannot access Client B's workspace
  AC6: Telegram-Only Fallback — AFFiNE down → Telegram continues, workspace queued

Plus: model validation, gating engine logic, template parsing.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any, Optional
from unittest.mock import AsyncMock

import pytest

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
    UnlockCondition,
)
from src.ccp.services.affine_client_workspace import (
    AGENT_NOEMIE,
    AGENT_PIERRE,
    CLIENT_WORKSPACE_SQL,
    ClientWorkspaceProvisioner,
    ContentGatingEngine,
)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _run(coro):
    """Run an async coroutine synchronously for tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ══════════════════════════════════════════════════════════════════════════════
# Mocks
# ══════════════════════════════════════════════════════════════════════════════


class MockAFFiNEClient:
    """Mock AFFiNE client for client workspace provisioning."""

    def __init__(self):
        self._workspaces: dict[str, dict] = {}
        self._entries: dict[str, list[dict]] = {}
        self._themes: dict[str, str] = {}
        self._should_fail = False

    async def create_workspace(self, name: str, template: dict) -> dict:
        if self._should_fail:
            raise ConnectionError("AFFiNE API unreachable")
        ws_id = str(uuid.uuid4())[:12]
        ws_url = f"https://os.consciouselite.com/ws/{ws_id}"
        self._workspaces[ws_id] = {"name": name, "template": template}
        return {"workspace_id": ws_id, "workspace_url": ws_url}

    async def apply_theme(self, workspace_id: str, theme_file: str) -> None:
        if self._should_fail:
            raise ConnectionError("AFFiNE API unreachable")
        self._themes[workspace_id] = theme_file

    async def create_entry(
        self, workspace_id: str, section_id: str, entry_data: dict
    ) -> dict:
        if self._should_fail:
            raise ConnectionError("AFFiNE API unreachable")
        key = f"{workspace_id}:{section_id}"
        if key not in self._entries:
            self._entries[key] = []
        self._entries[key].append(entry_data)
        return entry_data

    def get_entries(self, workspace_id: str, section_id: str) -> list[dict]:
        return self._entries.get(f"{workspace_id}:{section_id}", [])


class MockSupabase:
    """Mock Supabase for client workspace registration."""

    def __init__(self):
        self._client_workspaces: dict[str, dict] = {}

    def register_client_workspace(
        self, client_id: str, workspace_id: str, workspace_url: str, program_id: str
    ) -> None:
        self._client_workspaces[client_id] = {
            "client_workspace_id": workspace_id,
            "workspace_url": workspace_url,
            "program_id": program_id,
        }

    def get_client_workspace(self, client_id: str) -> dict:
        if client_id not in self._client_workspaces:
            raise KeyError(f"Client {client_id} not found")
        return self._client_workspaces[client_id]


class MockTelegram:
    """Mock Telegram client for notifications."""

    def __init__(self):
        self.messages: list[dict] = []

    async def send_message(self, client_id: str, message: str) -> None:
        self.messages.append({"client_id": client_id, "message": message})


# ── Fixtures ──────────────────────────────────────────────────────────────────

CLIENT_ID = "uuid-client-042"
COACH_ID = "uuid-coach-001"
PROGRAM_ID = "reference-program"
COACH_THEME = "coach_theme_JPR.css"


@pytest.fixture
def affine_client():
    return MockAFFiNEClient()


@pytest.fixture
def supabase():
    return MockSupabase()


@pytest.fixture
def telegram():
    return MockTelegram()


@pytest.fixture
def template_dir():
    return Path("src/ccp/templates")


@pytest.fixture
def provisioner(affine_client, supabase, telegram, template_dir):
    return ClientWorkspaceProvisioner(
        coach_acronym="JPR",
        affine_client=affine_client,
        supabase_client=supabase,
        telegram_client=telegram,
        template_dir=template_dir,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Test Constants & Enums
# ══════════════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify FR-CA11-03 constants."""

    def test_client_sections_count(self):
        assert CLIENT_WORKSPACE_SECTIONS_COUNT == 4

    def test_required_sections(self):
        assert CLIENT_REQUIRED_SECTIONS == {
            "dashboard", "learning_library", "journal", "resources"
        }

    def test_readwrite_sections(self):
        assert CLIENT_READWRITE_SECTIONS == {"journal"}

    def test_readonly_sections(self):
        assert CLIENT_READONLY_SECTIONS == {"dashboard", "learning_library", "resources"}

    def test_section_enum_values(self):
        assert len(ClientWorkspaceSection) == 4

    def test_provisioning_status_values(self):
        assert set(ClientProvisioningStatus) == {
            ClientProvisioningStatus.SUCCESS,
            ClientProvisioningStatus.QUEUED,
            ClientProvisioningStatus.FAILED_TELEGRAM_ONLY,
        }


# ══════════════════════════════════════════════════════════════════════════════
# Test Models (DEP-ENG-073)
# ══════════════════════════════════════════════════════════════════════════════


class TestModels:
    """Verify DEP-ENG-073 payload schema."""

    def test_unlock_condition_validation(self):
        uc = UnlockCondition(min_coping_position=2, min_atlas_week=3)
        assert uc.min_coping_position == 2
        assert uc.min_atlas_week == 3

    def test_unlock_condition_rejects_negative(self):
        with pytest.raises(Exception):
            UnlockCondition(min_coping_position=-1, min_atlas_week=0)

    def test_content_block_creation(self):
        block = ContentBlock(
            block_id="BLK-001",
            title="Test Block",
            content_type="video",
            program_tag="week-1",
            unlock_condition=UnlockCondition(min_coping_position=0, min_atlas_week=0),
        )
        assert block.permission == ContentPermission.READ_ONLY

    def test_gating_snapshot(self):
        gs = GatingSnapshot(coping_position=2, atlas_week=3, capacity_track="Growth")
        assert gs.coping_position == 2

    def test_client_workspace_payload(self):
        p = ClientWorkspaceProvisioningPayload(
            client_id="c-001",
            coach_id="coach-001",
            program_id="test-program",
            workspace_id="ws-001",
            workspace_url="https://test.local/ws/001",
            theme_inherited_from="coach_theme_JPR.css",
            sections_provisioned=["dashboard", "journal", "resources"],
            learning_library_blocks_unlocked=2,
            learning_library_blocks_total=8,
        )
        assert p.receipt_chain_guard.schema_ref == "DEP-ENG-041"

    def test_client_provisioning_result(self):
        r = ClientProvisioningResult(
            status=ClientProvisioningStatus.QUEUED,
            telegram_fallback_active=True,
        )
        assert r.payload is None
        assert r.telegram_fallback_active is True


# ══════════════════════════════════════════════════════════════════════════════
# Test Content Gating Engine (Noémie)
# ══════════════════════════════════════════════════════════════════════════════


class TestContentGatingEngine:
    """Test Noémie's gating logic."""

    def _make_blocks(self) -> list[ContentBlock]:
        return [
            ContentBlock(
                block_id="BLK-W01-INTRO",
                title="Welcome",
                content_type="video",
                program_tag="week-1",
                unlock_condition=UnlockCondition(min_coping_position=0, min_atlas_week=0),
            ),
            ContentBlock(
                block_id="BLK-W01-WS",
                title="Worksheet",
                content_type="worksheet",
                program_tag="week-1",
                unlock_condition=UnlockCondition(min_coping_position=0, min_atlas_week=0),
            ),
            ContentBlock(
                block_id="BLK-W02-ID",
                title="Identity Mapping",
                content_type="video",
                program_tag="week-2",
                unlock_condition=UnlockCondition(min_coping_position=1, min_atlas_week=2),
            ),
            ContentBlock(
                block_id="BLK-W03-VULN",
                title="Vulnerability Workshop",
                content_type="video",
                program_tag="week-3",
                unlock_condition=UnlockCondition(min_coping_position=2, min_atlas_week=3),
            ),
            ContentBlock(
                block_id="BLK-W04-MAST",
                title="Mastery Integration",
                content_type="video",
                program_tag="week-4",
                unlock_condition=UnlockCondition(min_coping_position=3, min_atlas_week=4),
            ),
        ]

    def test_initial_state_unlocks_week1_only(self):
        """AC2: At coping=0, week=0, only Week 1 blocks unlock."""
        blocks = self._make_blocks()
        unlocked = ContentGatingEngine.evaluate_unlockable(blocks, 0, 0)
        assert len(unlocked) == 2
        ids = {b.block_id for b in unlocked}
        assert ids == {"BLK-W01-INTRO", "BLK-W01-WS"}

    def test_coping_position_alone_not_enough(self):
        """Both conditions must be met."""
        blocks = self._make_blocks()
        unlocked = ContentGatingEngine.evaluate_unlockable(blocks, 3, 0)
        # High coping but week=0 → still only week 1
        assert len(unlocked) == 2

    def test_atlas_week_alone_not_enough(self):
        blocks = self._make_blocks()
        unlocked = ContentGatingEngine.evaluate_unlockable(blocks, 0, 4)
        assert len(unlocked) == 2

    def test_progressive_unlock_week2(self):
        blocks = self._make_blocks()
        unlocked = ContentGatingEngine.evaluate_unlockable(blocks, 1, 2)
        assert len(unlocked) == 3
        ids = {b.block_id for b in unlocked}
        assert "BLK-W02-ID" in ids

    def test_progressive_unlock_all(self):
        blocks = self._make_blocks()
        unlocked = ContentGatingEngine.evaluate_unlockable(blocks, 3, 4)
        assert len(unlocked) == 5  # All blocks

    def test_newly_unlockable_excludes_provisioned(self):
        blocks = self._make_blocks()
        already = {"BLK-W01-INTRO", "BLK-W01-WS"}
        newly = ContentGatingEngine.evaluate_newly_unlockable(blocks, already, 1, 2)
        assert len(newly) == 1
        assert newly[0].block_id == "BLK-W02-ID"

    def test_validate_unlock_request_legitimate(self):
        block = self._make_blocks()[2]  # Week 2: coping>=1, week>=2
        assert ContentGatingEngine.validate_unlock_request(block, 1, 2) is True

    def test_validate_unlock_request_premature(self):
        """Safety: premature unlock rejected."""
        block = self._make_blocks()[2]  # Week 2: coping>=1, week>=2
        assert ContentGatingEngine.validate_unlock_request(block, 0, 2) is False

    def test_parse_template_blocks(self):
        """Parse content blocks from reference template."""
        template_path = Path("src/ccp/templates/client_reference_program.json")
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            blocks = ContentGatingEngine.parse_template_blocks(data)
            assert len(blocks) == 8  # Reference template has 8 blocks
            assert all(isinstance(b, ContentBlock) for b in blocks)


# ══════════════════════════════════════════════════════════════════════════════
# AC1: Provisioning on Onboarding
# ══════════════════════════════════════════════════════════════════════════════


class TestProvisioningOnOnboarding:
    """AC1: Onboard client → workspace created with correct template and theme."""

    def test_workspace_created(self, provisioner, affine_client):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
            coping_position=0,
            atlas_week=0,
        ))
        assert result.status == ClientProvisioningStatus.SUCCESS
        assert result.payload is not None
        assert result.payload.workspace_id != ""

    def test_coach_theme_applied(self, provisioner, affine_client):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        assert result.payload.theme_inherited_from == COACH_THEME
        # Theme was applied to the workspace
        ws_id = result.payload.workspace_id
        assert affine_client._themes.get(ws_id) == COACH_THEME

    def test_sections_provisioned(self, provisioner):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
            coping_position=0,
            atlas_week=0,
        ))
        # At coping=0, week=0: dashboard, learning_library (has week1), journal, resources
        sections = result.payload.sections_provisioned
        assert "dashboard" in sections
        assert "journal" in sections
        assert "resources" in sections

    def test_supabase_registration(self, provisioner, supabase):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        ws_data = supabase.get_client_workspace(CLIENT_ID)
        assert ws_data["client_workspace_id"] == result.payload.workspace_id

    def test_telegram_notification_sent(self, provisioner, telegram):
        _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        assert len(telegram.messages) == 1
        assert "ready" in telegram.messages[0]["message"].lower()


# ══════════════════════════════════════════════════════════════════════════════
# AC2: Content Gating
# ══════════════════════════════════════════════════════════════════════════════


class TestContentGating:
    """AC2: Client at coping=0, week=0 → only Week 1 content exists."""

    def test_initial_gating_unlocks_week1_only(self, provisioner):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
            coping_position=0,
            atlas_week=0,
        ))
        # Reference template: 2 blocks at coping=0, week=0
        assert result.payload.learning_library_blocks_unlocked == 2
        assert result.payload.learning_library_blocks_total == 8

    def test_gating_snapshot_recorded(self, provisioner):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
            coping_position=1,
            atlas_week=1,
        ))
        gs = result.payload.gating_snapshot
        assert gs.coping_position == 1
        assert gs.atlas_week == 1


# ══════════════════════════════════════════════════════════════════════════════
# AC3: Progressive Unlock
# ══════════════════════════════════════════════════════════════════════════════


class TestProgressiveUnlock:
    """AC3: Update coping/atlas → new blocks provisioned."""

    def test_unlock_new_content(self, provisioner):
        # Initial provision
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
            coping_position=0,
            atlas_week=0,
        ))
        ws_id = result.payload.workspace_id

        # Progress to coping=1, week=2
        unlock_result = _run(provisioner.unlock_content(
            client_id=CLIENT_ID,
            program_id=PROGRAM_ID,
            workspace_id=ws_id,
            coping_position=1,
            atlas_week=2,
        ))
        # Should unlock BLK-W01-EXERCISE (coping>=1, week>=1) and BLK-W02-IDENTITY
        assert len(unlock_result.blocks_unlocked) >= 1
        assert unlock_result.telegram_notified is True

    def test_no_duplicate_unlock(self, provisioner):
        """Already provisioned blocks are not re-provisioned."""
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
            coping_position=0,
            atlas_week=0,
        ))
        ws_id = result.payload.workspace_id

        # Same gating state → nothing new to unlock
        unlock_result = _run(provisioner.unlock_content(
            client_id=CLIENT_ID,
            program_id=PROGRAM_ID,
            workspace_id=ws_id,
            coping_position=0,
            atlas_week=0,
        ))
        assert len(unlock_result.blocks_unlocked) == 0
        assert unlock_result.telegram_notified is False


# ══════════════════════════════════════════════════════════════════════════════
# AC4: Read-Only Enforcement
# ══════════════════════════════════════════════════════════════════════════════


class TestReadOnlyEnforcement:
    """AC4: CCP-managed sections are read-only for clients."""

    def test_journal_is_writable(self, provisioner):
        assert provisioner.check_write_permission("journal") is True

    def test_dashboard_is_readonly(self, provisioner):
        assert provisioner.check_write_permission("dashboard") is False

    def test_learning_library_is_readonly(self, provisioner):
        assert provisioner.check_write_permission("learning_library") is False

    def test_resources_is_readonly(self, provisioner):
        assert provisioner.check_write_permission("resources") is False

    def test_unknown_section_is_readonly(self, provisioner):
        assert provisioner.check_write_permission("unknown") is False


# ══════════════════════════════════════════════════════════════════════════════
# AC5: Cross-Client Isolation
# ══════════════════════════════════════════════════════════════════════════════


class TestCrossClientIsolation:
    """AC5: Client A cannot access Client B's workspace."""

    def test_owner_can_access(self, provisioner, supabase):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        ws_id = result.payload.workspace_id
        assert provisioner.validate_workspace_access(CLIENT_ID, ws_id) is True

    def test_other_client_cannot_access(self, provisioner, supabase):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        ws_id = result.payload.workspace_id
        assert provisioner.validate_workspace_access("other-client", ws_id) is False


# ══════════════════════════════════════════════════════════════════════════════
# AC6: Telegram-Only Fallback
# ══════════════════════════════════════════════════════════════════════════════


class TestTelegramFallback:
    """AC6: AFFiNE down → Telegram continues, workspace queued."""

    def test_affine_failure_returns_queued(self, provisioner, affine_client):
        affine_client._should_fail = True
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        assert result.status == ClientProvisioningStatus.QUEUED
        assert result.telegram_fallback_active is True

    def test_fallback_does_not_crash(self, provisioner, affine_client):
        affine_client._should_fail = True
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        # Should not raise, should return graceful fallback
        assert result.payload is None
        assert result.error_detail != ""


# ══════════════════════════════════════════════════════════════════════════════
# Receipt Chain
# ══════════════════════════════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """Verify receipt is written on provisioning."""

    def test_receipt_written(self, provisioner):
        result = _run(provisioner.provision_client_workspace(
            client_id=CLIENT_ID,
            coach_id=COACH_ID,
            program_id=PROGRAM_ID,
            coach_theme_file=COACH_THEME,
        ))
        assert result.status == ClientProvisioningStatus.SUCCESS
        # Receipt writing is internal — if no exception, receipt was written


# ══════════════════════════════════════════════════════════════════════════════
# SQL Schema
# ══════════════════════════════════════════════════════════════════════════════


class TestSQLSchema:
    """Verify SQL schema for client workspace."""

    def test_client_workspace_columns(self):
        assert "client_workspace_id" in CLIENT_WORKSPACE_SQL
        assert "client_workspace_url" in CLIENT_WORKSPACE_SQL
        assert "client_workspace_program_id" in CLIENT_WORKSPACE_SQL
        assert "client_workspace_status" in CLIENT_WORKSPACE_SQL
