"""
FR-CA11-01 — Coach Workspace Provisioning (AFFiNE Sovereign Dashboard)
======================================================================
Tests for MasterTemplateValidator, ThemeTokenExtractor, CSSThemeGenerator,
AFFiNEWorkspaceProvisioner, and fallback degradation.

Spec reference: FR-CA11-01_Coach_Workspace_Provisioning_Tech_Spec.md
  §8 — AC1 (Template Integrity), AC2 (Theme Application),
        AC3 (Isolation Enforcement), AC4 (Receipt Chain Integration),
        AC5 (Fallback Graceful Degradation)
  §10 — Testing Strategy
"""

from __future__ import annotations

import json
import tempfile
import uuid
from pathlib import Path
from typing import Any, Optional
from unittest.mock import MagicMock, patch

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ca11_models import (
    DEFAULT_CCP_ACCENT,
    DEFAULT_CCP_FONT,
    DEFAULT_CCP_PRIMARY,
    REQUIRED_SECTION_COUNT,
    REQUIRED_SECTIONS,
    TEMPLATE_VERSION,
    MasterTemplateValidationResult,
    ProvisioningResult,
    ProvisioningStatus,
    ReceiptChainGuardRef,
    ThemeTokens,
    WorkspaceProvisioningError,
    WorkspaceProvisioningPayload,
    WorkspaceSectionType,
)
from src.ccp.services.affine_workspace_provisioner import (
    AGENT_NAME,
    AFFiNEWorkspaceProvisioner,
    CSSThemeGenerator,
    MasterTemplateValidator,
    ThemeTokenExtractor,
)


# ══════════════════════════════════════════════════════════════════════
# Helpers & Fixtures
# ══════════════════════════════════════════════════════════════════════

CID = "TST"
COACH_UUID = "uuid-coach-test-001"


def _load_master_template() -> dict:
    """Load the actual master workspace template."""
    template_path = Path("src/ccp/templates/coach_workspace_master.json")
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _make_coach_soul(
    primary: str = "#2E86AB",
    accent: str = "#F18F01",
) -> dict:
    """Create a mock coach_soul.json (DEP-ENG-003) with brand aesthetics."""
    return {
        "coach_id": COACH_UUID,
        "brand_aesthetics": {
            "primary_color": primary,
            "accent_color": accent,
        },
        "positive_space": {"clusters": []},
        "negative_space": {"forbidden_strings": []},
    }


def _make_business_summary(
    name: str = "Test Coach Academy",
    tagline: str = "Transform your life",
    logo: str = "https://example.com/logo.png",
) -> dict:
    """Create a mock coach_business_summary.json (DEP-ENG-050)."""
    return {
        "business_name": name,
        "tagline": tagline,
        "logo_url": logo,
    }


def _make_rc_isolated() -> tuple[ReceiptChain, str]:
    """Create a receipt chain with an isolated temp log dir."""
    tmp = tempfile.mkdtemp(prefix="fr_ca11_01_rc_")
    rc = ReceiptChain(coach_acronym=CID, log_dir=tmp)
    return rc, tmp


class MockAFFiNEClient:
    """Mock AFFiNE API client for testing."""

    def __init__(self, fail_create: bool = False, fail_theme: bool = False):
        self._fail_create = fail_create
        self._fail_theme = fail_theme
        self._workspaces: dict[str, dict] = {}

    def create_workspace(self, name: str, template: dict) -> dict:
        if self._fail_create:
            raise ConnectionError("AFFiNE API unreachable")
        ws_id = str(uuid.uuid4())
        self._workspaces[ws_id] = {"name": name, "template": template}
        return {"workspace_id": ws_id}

    def apply_theme(self, workspace_id: str, css_content: str, filename: str) -> None:
        if self._fail_theme:
            raise ConnectionError("Theme application failed")
        if workspace_id in self._workspaces:
            self._workspaces[workspace_id]["theme"] = filename


class MockSupabaseClient:
    """Mock Supabase client for testing."""

    def __init__(self):
        self._data: dict[str, list[dict]] = {}
        self._last_update: Optional[dict] = None

    def table(self, name: str):
        self._current_table = name
        return self

    def update(self, data: dict):
        self._last_update = data
        return self

    def eq(self, field: str, value: str):
        return self

    def execute(self):
        return {"data": [self._last_update], "count": 1}


class MockNotionFallback:
    """Mock Notion fallback service for testing AC5."""

    def __init__(self, fail: bool = False):
        self._fail = fail
        self.called = False

    def create_coach_dashboard(self, coach_id: str) -> dict:
        self.called = True
        if self._fail:
            raise ConnectionError("Notion also unreachable")
        return {"page_id": f"notion-{coach_id}"}


class MockTelegramClient:
    """Mock Telegram client for testing."""

    def __init__(self):
        self.messages: list[dict] = []

    def send_message(self, coach_id: str, text: str) -> None:
        self.messages.append({"coach_id": coach_id, "text": text})


# ══════════════════════════════════════════════════════════════════════
# 1. Constants & Enums
# ══════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify constants match spec values."""

    def test_required_section_count(self) -> None:
        """Spec §4 Stage 1: Exactly 8 root sections."""
        assert REQUIRED_SECTION_COUNT == 8

    def test_required_sections_all_present(self) -> None:
        """Spec §4 Stage 1: All 8 section IDs defined."""
        assert len(REQUIRED_SECTIONS) == 8
        expected = {
            "command_center",
            "content_calendar",
            "client_intelligence_hub",
            "cpsc_campaign_console",
            "cral_evidence_vault",
            "guardian_agent_console",
            "visual_production_console",
            "program_content_library",
        }
        assert REQUIRED_SECTIONS == expected

    def test_workspace_section_enum_values(self) -> None:
        """All 8 WorkspaceSectionType enum values match REQUIRED_SECTIONS."""
        enum_values = {s.value for s in WorkspaceSectionType}
        assert enum_values == REQUIRED_SECTIONS

    def test_template_version(self) -> None:
        assert TEMPLATE_VERSION == "1.0.0"

    def test_agent_name(self) -> None:
        """Spec §4 Stage 2-3: Agent is Pierre."""
        assert AGENT_NAME == "Pierre"


# ══════════════════════════════════════════════════════════════════════
# 2. Master Template Validation (AC1, Gate TEMPLATE-VALID)
# ══════════════════════════════════════════════════════════════════════


class TestMasterTemplateValidation:
    """Spec §4 Stage 1, §8 AC1, §10 Unit Tests — Template Validation."""

    def test_valid_template_passes(self) -> None:
        """AC1: Provision from master template → all 8 sections exist."""
        template = _load_master_template()
        validator = MasterTemplateValidator()
        result = validator.validate(template)

        assert result.is_valid is True
        assert result.total_sections == 8
        assert len(result.sections_missing) == 0
        assert set(result.sections_found) == REQUIRED_SECTIONS

    def test_template_has_correct_version(self) -> None:
        template = _load_master_template()
        assert template["template_version"] == TEMPLATE_VERSION

    def test_template_sections_have_titles(self) -> None:
        """Each section has a non-empty title."""
        template = _load_master_template()
        for section in template["sections"]:
            assert "title" in section
            assert len(section["title"]) > 0

    def test_template_sections_have_descriptions(self) -> None:
        """Each section has a non-empty description."""
        template = _load_master_template()
        for section in template["sections"]:
            assert "description" in section
            assert len(section["description"]) > 0

    def test_content_calendar_has_all_columns(self) -> None:
        """AC1: Content Calendar database schema matches spec §4 Stage 1."""
        template = _load_master_template()
        cc = next(s for s in template["sections"] if s["section_id"] == "content_calendar")
        col_names = [c["name"] for c in cc["database_schema"]["columns"]]
        expected = [
            "Asset ID", "Script Preview", "Visual Assets", "Posting Notes",
            "Voice Note", "Why This Post", "Leadership Farming", "Fingerprint ID", "Status",
        ]
        assert col_names == expected

    def test_missing_sections_key_fails(self) -> None:
        """Template without 'sections' key fails validation."""
        validator = MasterTemplateValidator()
        result = validator.validate({"template_version": "1.0.0"})
        assert result.is_valid is False
        assert len(result.sections_missing) == 8

    def test_incomplete_template_fails(self) -> None:
        """Template with only 5 sections fails (needs exactly 8)."""
        validator = MasterTemplateValidator()
        template = {
            "template_version": "1.0.0",
            "sections": [
                {"section_id": "command_center", "title": "CC", "description": "d"},
                {"section_id": "content_calendar", "title": "CAL", "description": "d"},
                {"section_id": "client_intelligence_hub", "title": "CIH", "description": "d"},
                {"section_id": "cpsc_campaign_console", "title": "CPC", "description": "d"},
                {"section_id": "cral_evidence_vault", "title": "CEV", "description": "d"},
            ],
        }
        result = validator.validate(template)
        assert result.is_valid is False
        assert result.total_sections == 5
        assert len(result.sections_missing) == 3

    def test_section_without_title_fails(self) -> None:
        """Section missing title produces validation error."""
        validator = MasterTemplateValidator()
        sections = [
            {"section_id": s.value, "title": s.value, "description": "d"}
            for s in WorkspaceSectionType
        ]
        sections[0]["title"] = ""  # Remove title from first section
        template = {"template_version": "1.0.0", "sections": sections}
        result = validator.validate(template)
        assert result.is_valid is False
        assert any("missing 'title'" in e for e in result.validation_errors)


# ══════════════════════════════════════════════════════════════════════
# 3. Theme Token Extraction (AC2)
# ══════════════════════════════════════════════════════════════════════


class TestThemeTokenExtraction:
    """Spec §4 Stage 2, §8 AC2, §10 Unit Tests — Theme Generation."""

    def test_extract_brand_colors(self) -> None:
        """AC2: Extract primary=#2E86AB, accent=#F18F01 from coach_soul."""
        extractor = ThemeTokenExtractor()
        tokens = extractor.extract(
            _make_coach_soul(primary="#2E86AB", accent="#F18F01"),
            _make_business_summary(),
        )
        assert tokens.primary_color == "#2E86AB"
        assert tokens.accent_color == "#F18F01"

    def test_extract_business_tokens(self) -> None:
        """Business name, tagline, logo extracted from DEP-ENG-050."""
        extractor = ThemeTokenExtractor()
        tokens = extractor.extract(
            _make_coach_soul(),
            _make_business_summary(
                name="Elite Academy",
                tagline="Your journey starts here",
                logo="https://cdn.example.com/logo.png",
            ),
        )
        assert tokens.business_name == "Elite Academy"
        assert tokens.tagline == "Your journey starts here"
        assert tokens.logo_url == "https://cdn.example.com/logo.png"

    def test_fallback_to_defaults_on_missing_colors(self) -> None:
        """Spec §4 Stage 2 Failure Condition: Missing → CCP defaults."""
        extractor = ThemeTokenExtractor()
        tokens = extractor.extract(
            {"coach_id": "test"},  # No brand_aesthetics
            _make_business_summary(),
        )
        assert tokens.primary_color == DEFAULT_CCP_PRIMARY
        assert tokens.accent_color == DEFAULT_CCP_ACCENT

    def test_default_font_preference(self) -> None:
        extractor = ThemeTokenExtractor()
        tokens = extractor.extract(_make_coach_soul(), _make_business_summary())
        assert tokens.font_preference == DEFAULT_CCP_FONT

    def test_custom_font_from_config(self) -> None:
        extractor = ThemeTokenExtractor()
        tokens = extractor.extract(
            _make_coach_soul(),
            _make_business_summary(),
            coach_config={"font_preference": "Playfair Display"},
        )
        assert tokens.font_preference == "Playfair Display"

    def test_mood_state_affinity_color_extraction(self) -> None:
        """Alternative extraction path: mood_state_affinity."""
        extractor = ThemeTokenExtractor()
        soul = {
            "mood_state_affinity": {
                "dominant_color": "#FF5733",
                "secondary_color": "#33FF57",
            }
        }
        tokens = extractor.extract(soul, _make_business_summary())
        assert tokens.primary_color == "#FF5733"
        assert tokens.accent_color == "#33FF57"


# ══════════════════════════════════════════════════════════════════════
# 4. CSS Theme Generation (AC2)
# ══════════════════════════════════════════════════════════════════════


class TestCSSThemeGeneration:
    """Spec §4 Stage 2 Step 3, §3 Technical Decision 2."""

    def test_css_contains_primary_color(self) -> None:
        """AC2: Generated CSS has correct --ccp-primary."""
        generator = CSSThemeGenerator()
        tokens = ThemeTokens(
            primary_color="#2E86AB",
            accent_color="#F18F01",
            business_name="Test",
            tagline="",
            logo_url="",
        )
        css = generator.generate(tokens, "JP")
        assert "--ccp-primary: #2E86AB;" in css

    def test_css_contains_accent_color(self) -> None:
        """AC2: Generated CSS has correct --ccp-accent."""
        generator = CSSThemeGenerator()
        tokens = ThemeTokens(
            primary_color="#2E86AB",
            accent_color="#F18F01",
            business_name="Test",
            tagline="",
            logo_url="",
        )
        css = generator.generate(tokens, "JP")
        assert "--ccp-accent: #F18F01;" in css

    def test_css_contains_business_name(self) -> None:
        generator = CSSThemeGenerator()
        tokens = ThemeTokens(
            primary_color="#000",
            accent_color="#FFF",
            business_name="Elite Coaching",
            tagline="Transform",
            logo_url="https://example.com/logo.png",
        )
        css = generator.generate(tokens, "EC")
        assert '--ccp-business-name: "Elite Coaching"' in css

    def test_css_contains_logo_url(self) -> None:
        generator = CSSThemeGenerator()
        tokens = ThemeTokens(
            primary_color="#000",
            accent_color="#FFF",
            business_name="Test",
            logo_url="https://example.com/logo.png",
        )
        css = generator.generate(tokens, "TST")
        assert "https://example.com/logo.png" in css

    def test_theme_filename_format(self) -> None:
        """Spec §4 Stage 2: coach_theme_{ACRONYM}.css"""
        generator = CSSThemeGenerator()
        assert generator.get_theme_filename("jp") == "coach_theme_JP.css"
        assert generator.get_theme_filename("TST") == "coach_theme_TST.css"

    def test_css_contains_font(self) -> None:
        generator = CSSThemeGenerator()
        tokens = ThemeTokens(
            primary_color="#000",
            accent_color="#FFF",
            business_name="Test",
            font_preference="Montserrat",
        )
        css = generator.generate(tokens, "TST")
        assert '--ccp-font: "Montserrat"' in css


# ══════════════════════════════════════════════════════════════════════
# 5. Full Provisioning Pipeline (AC1-AC4)
# ══════════════════════════════════════════════════════════════════════


class TestFullProvisioningPipeline:
    """Spec §4 Stage 3, §8 AC1-AC4, §10 Integration Tests."""

    def _make_provisioner(
        self,
        affine_client: Optional[MockAFFiNEClient] = None,
        supabase_client: Optional[MockSupabaseClient] = None,
        telegram_client: Optional[MockTelegramClient] = None,
        notion_fallback: Optional[MockNotionFallback] = None,
    ) -> AFFiNEWorkspaceProvisioner:
        return AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            template_path=Path("src/ccp/templates/coach_workspace_master.json"),
            affine_client=affine_client or MockAFFiNEClient(),
            supabase_client=supabase_client or MockSupabaseClient(),
            telegram_client=telegram_client or MockTelegramClient(),
            notion_fallback_service=notion_fallback,
        )

    def test_successful_provisioning(self) -> None:
        """Full pipeline: template → theme → workspace → receipt."""
        provisioner = self._make_provisioner()
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.SUCCESS
        assert result.payload is not None
        assert result.payload.coach_id == COACH_UUID
        assert result.payload.coach_acronym == CID

    def test_payload_has_8_sections(self) -> None:
        """AC1: All 8 sections provisioned."""
        provisioner = self._make_provisioner()
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.payload is not None
        assert len(result.payload.sections_provisioned) == 8
        assert set(result.payload.sections_provisioned) == REQUIRED_SECTIONS

    def test_payload_has_correct_theme_file(self) -> None:
        """Theme file matches coach_theme_{ACRONYM}.css pattern."""
        provisioner = self._make_provisioner()
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.payload is not None
        assert result.payload.theme_file == f"coach_theme_{CID}.css"

    def test_payload_has_workspace_url(self) -> None:
        """Workspace URL contains the workspace_id."""
        provisioner = self._make_provisioner()
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.payload is not None
        assert result.payload.workspace_id in result.payload.workspace_url

    def test_payload_receipt_chain_guard_ref(self) -> None:
        """CA11 Revision Fix 2: receipt_chain_guard uses schema_ref, not string literal."""
        provisioner = self._make_provisioner()
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.payload is not None
        assert result.payload.receipt_chain_guard.schema_ref == "DEP-ENG-041"

    def test_telegram_confirmation_sent(self) -> None:
        """Spec §4 Stage 3 Step 4: Telegram confirmation."""
        telegram = MockTelegramClient()
        provisioner = self._make_provisioner(telegram_client=telegram)
        provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert len(telegram.messages) == 1
        assert "workspace is ready" in telegram.messages[0]["text"]

    def test_supabase_registration(self) -> None:
        """Spec §4 Stage 3 Step 3: workspace_id registered in Supabase."""
        supabase = MockSupabaseClient()
        provisioner = self._make_provisioner(supabase_client=supabase)
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.SUCCESS
        assert supabase._last_update is not None
        assert "affine_workspace_id" in supabase._last_update


# ══════════════════════════════════════════════════════════════════════
# 6. Isolation Enforcement (AC3)
# ══════════════════════════════════════════════════════════════════════


class TestIsolationEnforcement:
    """Spec §8 AC3, §10 Safety Tests — ADR-01 Isolation."""

    def test_two_coaches_get_different_workspace_ids(self) -> None:
        """AC3: Coach A and Coach B get separate workspace_ids."""
        provisioner_a = AFFiNEWorkspaceProvisioner(
            coach_id="uuid-coach-A",
            coach_acronym="CHA",
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        provisioner_b = AFFiNEWorkspaceProvisioner(
            coach_id="uuid-coach-B",
            coach_acronym="CHB",
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        result_a = provisioner_a.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(name="Coach A Academy"),
        )
        result_b = provisioner_b.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(name="Coach B Academy"),
        )
        assert result_a.payload is not None
        assert result_b.payload is not None
        assert result_a.payload.workspace_id != result_b.payload.workspace_id
        assert result_a.payload.coach_acronym == "CHA"
        assert result_b.payload.coach_acronym == "CHB"

    def test_workspace_urls_are_unique(self) -> None:
        """Each coach's workspace URL is unique."""
        provisioner_a = AFFiNEWorkspaceProvisioner(
            coach_id="uuid-A",
            coach_acronym="AAA",
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        provisioner_b = AFFiNEWorkspaceProvisioner(
            coach_id="uuid-B",
            coach_acronym="BBB",
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        r_a = provisioner_a.provision_coach_workspace(
            _make_coach_soul(), _make_business_summary()
        )
        r_b = provisioner_b.provision_coach_workspace(
            _make_coach_soul(), _make_business_summary()
        )
        assert r_a.payload is not None and r_b.payload is not None
        assert r_a.payload.workspace_url != r_b.payload.workspace_url


# ══════════════════════════════════════════════════════════════════════
# 7. Receipt Chain Integration (AC4)
# ══════════════════════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """Spec §8 AC4 — Receipt_CA11_01.json exists with correct workspace_id."""

    def test_receipt_written_on_success(self) -> None:
        """AC4: Successful provisioning writes receipt to chain."""
        rc, tmp_dir = _make_rc_isolated()
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        # Inject isolated receipt chain
        provisioner.receipt_chain = rc

        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.SUCCESS

        # Verify receipt was written
        log_files = list(Path(tmp_dir).glob("receipt_*.jsonl"))
        assert len(log_files) > 0

        # Read receipt entries
        entries = []
        for log_file in log_files:
            with open(log_file, "r") as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))

        # Find the provisioning receipt
        prov_receipts = [
            e for e in entries if e.get("action") == "workspace_provisioning"
        ]
        assert len(prov_receipts) >= 1

        receipt = prov_receipts[0]
        assert receipt["agent_id"] == "Pierre"
        assert receipt["decision"] == "provisioned"
        assert result.payload is not None
        assert receipt["asset_id"] == result.payload.workspace_id

        # Verify DEP-ENG-041 schema fields in metadata
        meta = receipt.get("metadata", {})
        assert "input_payload_hash" in meta
        assert "output_payload_hash" in meta
        assert meta["receipt_chain_guard"]["schema_ref"] == "DEP-ENG-041"
        assert meta["stage_name"] == "WORKSPACE_PROVISIONING"

    def test_receipt_contains_dep_eng_071_payload(self) -> None:
        """Receipt metadata includes full DEP-ENG-071 payload."""
        rc, tmp_dir = _make_rc_isolated()
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        provisioner.receipt_chain = rc

        provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )

        log_files = list(Path(tmp_dir).glob("receipt_*.jsonl"))
        entries = []
        for log_file in log_files:
            with open(log_file, "r") as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))

        prov = [e for e in entries if e.get("action") == "workspace_provisioning"][0]
        dep_071 = prov["metadata"]["dep_eng_071"]
        assert dep_071["coach_id"] == COACH_UUID
        assert len(dep_071["sections_provisioned"]) == 8


# ══════════════════════════════════════════════════════════════════════
# 8. Fallback Graceful Degradation (AC5)
# ══════════════════════════════════════════════════════════════════════


class TestFallbackDegradation:
    """Spec §6, §8 AC5 — Fallback to Notion on AFFiNE failure."""

    def test_affine_failure_triggers_notion_fallback(self) -> None:
        """AC5: Block AFFiNE → system falls back to Notion with degradation flag."""
        notion = MockNotionFallback()
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            affine_client=MockAFFiNEClient(fail_create=True),
            supabase_client=MockSupabaseClient(),
            notion_fallback_service=notion,
        )
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.FAILED_FALLBACK_NOTION
        assert result.fallback_active is True
        assert notion.called is True
        assert result.notion_dashboard_id is not None

    def test_fallback_logs_degradation_flag(self) -> None:
        """AC5: Degradation flag logged in receipt chain."""
        rc, tmp_dir = _make_rc_isolated()
        notion = MockNotionFallback()
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            affine_client=MockAFFiNEClient(fail_create=True),
            supabase_client=MockSupabaseClient(),
            notion_fallback_service=notion,
        )
        provisioner.receipt_chain = rc

        provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )

        log_files = list(Path(tmp_dir).glob("receipt_*.jsonl"))
        entries = []
        for log_file in log_files:
            with open(log_file, "r") as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))

        fallback_entries = [
            e for e in entries if e.get("action") == "workspace_provisioning_fallback"
        ]
        assert len(fallback_entries) >= 1
        assert fallback_entries[0]["decision"] == "degraded"
        assert fallback_entries[0]["metadata"]["degradation_flag"] is True

    def test_both_fallback_and_affine_fail(self) -> None:
        """Both AFFiNE and Notion fail — fallback_active is False."""
        notion = MockNotionFallback(fail=True)
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            affine_client=MockAFFiNEClient(fail_create=True),
            supabase_client=MockSupabaseClient(),
            notion_fallback_service=notion,
        )
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.FAILED_FALLBACK_NOTION
        assert result.fallback_active is False
        assert result.notion_dashboard_id is None

    def test_no_notion_fallback_configured(self) -> None:
        """Without Notion fallback service, no fallback occurs."""
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            affine_client=MockAFFiNEClient(fail_create=True),
            supabase_client=MockSupabaseClient(),
            notion_fallback_service=None,
        )
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.FAILED_FALLBACK_NOTION
        assert result.fallback_active is False


# ══════════════════════════════════════════════════════════════════════
# 9. DEP-ENG-071 Schema Validation
# ══════════════════════════════════════════════════════════════════════


class TestDEPENG071Schema:
    """Verify DEP-ENG-071 output schema matches spec §5."""

    def test_payload_serialization(self) -> None:
        """Payload serializes correctly with all required fields."""
        payload = WorkspaceProvisioningPayload(
            transaction_timestamp="2026-03-25T18:00:00Z",
            coach_id="uuid-coach-001",
            coach_acronym="JP",
            workspace_id="affine-ws-uuid-001",
            workspace_url="https://os.consciouselite.com/ws/affine-ws-uuid-001",
            theme_file="coach_theme_JP.css",
            template_version="1.0.0",
            sections_provisioned=[s.value for s in WorkspaceSectionType],
            receipt_chain_guard=ReceiptChainGuardRef(schema_ref="DEP-ENG-041"),
        )
        data = payload.model_dump()
        assert data["coach_id"] == "uuid-coach-001"
        assert data["workspace_id"] == "affine-ws-uuid-001"
        assert len(data["sections_provisioned"]) == 8
        assert data["receipt_chain_guard"]["schema_ref"] == "DEP-ENG-041"

    def test_payload_rejects_wrong_section_count(self) -> None:
        """DEP-ENG-071 enforces exactly 8 sections."""
        with pytest.raises(Exception):
            WorkspaceProvisioningPayload(
                transaction_timestamp="2026-03-25T18:00:00Z",
                coach_id="uuid-coach-001",
                coach_acronym="JP",
                workspace_id="affine-ws-uuid-001",
                workspace_url="https://os.consciouselite.com/ws/affine-ws-uuid-001",
                theme_file="coach_theme_JP.css",
                sections_provisioned=["command_center", "content_calendar"],  # Only 2
            )

    def test_payload_template_version_default(self) -> None:
        """Template version defaults to TEMPLATE_VERSION."""
        payload = WorkspaceProvisioningPayload(
            transaction_timestamp="2026-03-25T18:00:00Z",
            coach_id="uuid-001",
            coach_acronym="JP",
            workspace_id="ws-001",
            workspace_url="https://os.consciouselite.com/ws/ws-001",
            theme_file="coach_theme_JP.css",
            sections_provisioned=[s.value for s in WorkspaceSectionType],
        )
        assert payload.template_version == TEMPLATE_VERSION


# ══════════════════════════════════════════════════════════════════════
# 10. Template Load Error Handling
# ══════════════════════════════════════════════════════════════════════


class TestTemplateLoadErrors:
    """Edge cases for template loading failures."""

    def test_missing_template_file(self) -> None:
        """Non-existent template path fails gracefully."""
        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            template_path=Path("/nonexistent/template.json"),
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.FAILED_NO_FALLBACK
        assert result.error == WorkspaceProvisioningError.TEMPLATE_VALIDATION_FAILED

    def test_invalid_json_template(self) -> None:
        """Malformed JSON template fails gracefully."""
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        tmp.write("{invalid json")
        tmp.close()

        provisioner = AFFiNEWorkspaceProvisioner(
            coach_id=COACH_UUID,
            coach_acronym=CID,
            template_path=Path(tmp.name),
            affine_client=MockAFFiNEClient(),
            supabase_client=MockSupabaseClient(),
        )
        result = provisioner.provision_coach_workspace(
            coach_soul=_make_coach_soul(),
            business_summary=_make_business_summary(),
        )
        assert result.status == ProvisioningStatus.FAILED_NO_FALLBACK
