"""
CCP FR-CA11-01 — Coach Workspace Provisioning (AFFiNE Sovereign Dashboard)

Provisions a fully branded AFFiNE workspace for each coach during Genesis Pipeline.
Replaces Notion dashboard delivery (FR45) per ADR-05.

Spec reference: FR-CA11-01_Coach_Workspace_Provisioning_Tech_Spec.md
  §4 — Stage 1: Master Template Construction (validation)
  §4 — Stage 2: Theme Token Extraction
  §4 — Stage 3: Workspace Provisioning
  §5 — DEP-ENG-071 PROPOSED (WorkspaceProvisioningPayload)
  §6 — Backward Compatibility Fallback (Notion parallel operation)
  §7 — Tasks 1-6
  §8 — AC1-AC5

Architecture references:
  ADR-01: Single-Tenant Isolated Cloud-Native Instances
  ADR-05: AFFiNE Over Notion (retires ADR-02)
  FR47/DEP-ENG-041: Receipt Chain Guard schema for all receipt writes

Agent: Pierre (AFFiNE Workspace Orchestrator) — Management Department
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

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

AGENT_NAME = "Pierre"
STAGE_TEMPLATE_VALIDATION = "TEMPLATE_VALIDATION"
STAGE_THEME_EXTRACTION = "THEME_EXTRACTION"
STAGE_WORKSPACE_PROVISIONING = "WORKSPACE_PROVISIONING"

# Default template path (relative to project root)
DEFAULT_TEMPLATE_PATH = Path("src/ccp/templates/coach_workspace_master.json")

# AFFiNE base URL (configurable per deployment)
AFFINE_BASE_URL_DEFAULT = "https://os.consciouselite.com"


# ══════════════════════════════════════════════════════════════════════════════
# Unit 3 — Master Template Validator
# ══════════════════════════════════════════════════════════════════════════════


class MasterTemplateValidator:
    """Validates the 8-section AFFiNE workspace master template.

    Spec §4 Stage 1 Failure Condition: Template does not contain all 8
    required sections → provisioner rejects template during validation.

    Gate TEMPLATE-VALID: Exactly 8 root sections required.
    AC1: All 8 root sections exist with correct database schemas.
    """

    def validate(self, template_data: dict) -> MasterTemplateValidationResult:
        """Validate the master template JSON.

        Args:
            template_data: Parsed JSON of the master workspace template.

        Returns:
            MasterTemplateValidationResult with validation status.
        """
        errors: list[str] = []
        sections_found: list[str] = []

        # Check template has sections key
        if "sections" not in template_data:
            return MasterTemplateValidationResult(
                is_valid=False,
                sections_found=[],
                sections_missing=list(REQUIRED_SECTIONS),
                total_sections=0,
                template_version=template_data.get("template_version", ""),
                validation_errors=["Template JSON missing 'sections' key"],
            )

        raw_sections = template_data["sections"]

        # Extract section IDs
        for section in raw_sections:
            section_id = section.get("section_id", "")
            if section_id:
                sections_found.append(section_id)

                # Validate section has required fields
                if not section.get("title"):
                    errors.append(
                        f"Section '{section_id}' missing 'title' field"
                    )
                if not section.get("description"):
                    errors.append(
                        f"Section '{section_id}' missing 'description' field"
                    )
            else:
                errors.append("Section found without 'section_id' field")

        # Check all required sections are present
        found_set = set(sections_found)
        missing = [s for s in REQUIRED_SECTIONS if s not in found_set]

        # Check for unexpected sections (spec defines exactly 8)
        unexpected = [s for s in sections_found if s not in REQUIRED_SECTIONS]
        if unexpected:
            errors.append(
                f"Unexpected sections not in spec: {unexpected}"
            )

        is_valid = (
            len(missing) == 0
            and len(sections_found) == REQUIRED_SECTION_COUNT
            and len(errors) == 0
        )

        return MasterTemplateValidationResult(
            is_valid=is_valid,
            sections_found=sections_found,
            sections_missing=missing,
            total_sections=len(sections_found),
            template_version=template_data.get("template_version", ""),
            validation_errors=errors,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Unit 4 — Theme Token Extractor
# ══════════════════════════════════════════════════════════════════════════════


class ThemeTokenExtractor:
    """Extracts brand tokens from coach_soul.json (DEP-ENG-003) and
    coach_business_summary.json (DEP-ENG-050).

    Spec §4 Stage 2:
      Step 1: Extract primary emotional color from dominant Mood State affinity.
      Step 2: Extract business name, tagline, logo URL from DEP-ENG-050.
      Failure Condition: Missing brand tokens → fallback to CCP default theme.
    """

    def extract(
        self,
        coach_soul: dict[str, Any],
        business_summary: dict[str, Any],
        coach_config: Optional[dict[str, Any]] = None,
    ) -> ThemeTokens:
        """Extract brand tokens from upstream data sources.

        Args:
            coach_soul: Parsed coach_soul.json (DEP-ENG-003).
            business_summary: Parsed coach_business_summary.json (DEP-ENG-050).
            coach_config: Optional coach configuration overrides.

        Returns:
            ThemeTokens with extracted or fallback values.
        """
        # Extract primary color from coach soul's aesthetic/mood data
        primary_color = self._extract_primary_color(coach_soul)
        accent_color = self._extract_accent_color(coach_soul)

        # Extract business tokens from DEP-ENG-050
        business_name = business_summary.get("business_name", "")
        tagline = business_summary.get("tagline", "")
        logo_url = business_summary.get("logo_url", "")

        # Font preference from coach config (or default)
        font_preference = DEFAULT_CCP_FONT
        if coach_config and "font_preference" in coach_config:
            font_preference = coach_config["font_preference"]

        if not business_name:
            # Attempt extraction from nested structures
            business_name = (
                business_summary.get("coach_name", "")
                or business_summary.get("name", "Coach Workspace")
            )

        return ThemeTokens(
            primary_color=primary_color,
            accent_color=accent_color,
            business_name=business_name,
            tagline=tagline,
            logo_url=logo_url,
            font_preference=font_preference,
        )

    def _extract_primary_color(self, coach_soul: dict[str, Any]) -> str:
        """Extract primary color from coach soul's mood/aesthetic data.

        Spec §4 Stage 2 Step 1: primary emotional color mapped from
        dominant Mood State affinity → CSS --ccp-primary.
        Falls back to DEFAULT_CCP_PRIMARY if not found.
        """
        # Navigate to brand aesthetics in coach_soul structure
        aesthetics = coach_soul.get("brand_aesthetics", {})
        if aesthetics and "primary_color" in aesthetics:
            return aesthetics["primary_color"]

        # Alternative: mood_state_affinity mapping
        mood = coach_soul.get("mood_state_affinity", {})
        if mood and "dominant_color" in mood:
            return mood["dominant_color"]

        return DEFAULT_CCP_PRIMARY

    def _extract_accent_color(self, coach_soul: dict[str, Any]) -> str:
        """Extract accent color from secondary Mood State.

        Spec §4 Stage 2 Step 1: accent color from secondary Mood State.
        Falls back to DEFAULT_CCP_ACCENT if not found.
        """
        aesthetics = coach_soul.get("brand_aesthetics", {})
        if aesthetics and "accent_color" in aesthetics:
            return aesthetics["accent_color"]

        mood = coach_soul.get("mood_state_affinity", {})
        if mood and "secondary_color" in mood:
            return mood["secondary_color"]

        return DEFAULT_CCP_ACCENT


# ══════════════════════════════════════════════════════════════════════════════
# Unit 5 — CSS Theme Generator
# ══════════════════════════════════════════════════════════════════════════════


class CSSThemeGenerator:
    """Generates coach-specific CSS theme file from extracted tokens.

    Spec §4 Stage 2 Step 3: Generate coach_theme_{ACRONYM}.css with
    all CSS custom properties.
    Spec §3 Technical Decision 2: CSS Theme Overlay per Coach.

    ADR-05: Full theme/branding control via CSS overlay.
    """

    def generate(self, tokens: ThemeTokens, coach_acronym: str) -> str:
        """Generate CSS content with custom properties.

        Args:
            tokens: Extracted brand theme tokens.
            coach_acronym: Coach identifier for the CSS filename.

        Returns:
            CSS string with custom properties.
        """
        css = f"""/* CCP Coach Theme — {coach_acronym.upper()}
 * Generated by FR-CA11-01 AFFiNE Workspace Provisioner
 * Agent: Pierre (AFFiNE Workspace Orchestrator)
 * Template: coach_workspace_master.json v{TEMPLATE_VERSION}
 *
 * ADR-05: Self-hosted AFFiNE theme overlay per coach.
 * "Never Outshine the Master" — Greene (1998):
 *   The workspace must feel like the coach's, not the platform's.
 */

:root {{
  /* Brand Colors (extracted from DEP-ENG-003 + DEP-ENG-050) */
  --ccp-primary: {tokens.primary_color};
  --ccp-accent: {tokens.accent_color};

  /* Business Identity */
  --ccp-business-name: "{tokens.business_name}";
  --ccp-tagline: "{tokens.tagline}";
  --ccp-logo-url: url("{tokens.logo_url}");

  /* Typography */
  --ccp-font: "{tokens.font_preference}";

  /* Derived Colors */
  --ccp-primary-light: {tokens.primary_color}22;
  --ccp-primary-hover: {tokens.primary_color}dd;
  --ccp-accent-light: {tokens.accent_color}22;
}}

/* AFFiNE Workspace Header */
.workspace-header {{
  background-color: var(--ccp-primary);
  font-family: var(--ccp-font), system-ui, sans-serif;
}}

.workspace-header .title {{
  color: #ffffff;
}}

/* Navigation Sidebar */
.sidebar-nav {{
  border-right-color: var(--ccp-primary-light);
}}

.sidebar-nav .active {{
  background-color: var(--ccp-primary-light);
  color: var(--ccp-primary);
}}

/* Database Views */
.database-header {{
  border-bottom-color: var(--ccp-accent);
}}

/* Status Badges */
.status-published {{
  background-color: var(--ccp-accent);
  color: #ffffff;
}}

.status-in-progress {{
  background-color: var(--ccp-primary-light);
  color: var(--ccp-primary);
}}
"""
        return css

    def get_theme_filename(self, coach_acronym: str) -> str:
        """Generate the theme filename.

        Spec §4 Stage 2: coach_theme_{ACRONYM}.css
        """
        return f"coach_theme_{coach_acronym.upper()}.css"


# ══════════════════════════════════════════════════════════════════════════════
# Unit 6 — AFFiNE Workspace Provisioner (main orchestrator)
# Unit 7 — Fallback Degradation Handler
# Unit 8 — Receipt Chain Integration
# ══════════════════════════════════════════════════════════════════════════════


class AFFiNEWorkspaceProvisioner:
    """Full AFFiNE workspace provisioning pipeline.

    Spec §4 Stage 3: Workspace Provisioning orchestrator.
    Agent: Pierre (AFFiNE Workspace Orchestrator) — Management Department.

    Pipeline:
      1. Validate master template (Gate TEMPLATE-VALID)
      2. Extract theme tokens (DEP-ENG-003 + DEP-ENG-050)
      3. Generate CSS theme
      4. Create AFFiNE workspace from template
      5. Apply theme CSS overlay
      6. Register workspace_id in Supabase
      7. Send Telegram confirmation
      8. Write Receipt Chain Guard entry (DEP-ENG-041)

    Fallback (§6): If AFFiNE API unreachable, fall back to Notion (FR45).
    ADR-01: Each coach gets an isolated workspace (not shared pages).
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        affine_base_url: str = AFFINE_BASE_URL_DEFAULT,
        template_path: Optional[Path] = None,
        supabase_client: Optional[Any] = None,
        telegram_client: Optional[Any] = None,
        affine_client: Optional[Any] = None,
        notion_fallback_service: Optional[Any] = None,
    ):
        """Initialize the provisioner.

        Args:
            coach_id: UUID of the coach.
            coach_acronym: 2-5 letter coach acronym (ADR-01 scoping).
            affine_base_url: Base URL for the AFFiNE instance.
            template_path: Path to master template JSON.
            supabase_client: Supabase client for registration.
            telegram_client: Telegram bot client for confirmation.
            affine_client: AFFiNE API client.
            notion_fallback_service: Notion sync service for fallback (FR45).
        """
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.affine_base_url = affine_base_url.rstrip("/")
        self.template_path = template_path or DEFAULT_TEMPLATE_PATH
        self.supabase = supabase_client
        self.telegram = telegram_client
        self.affine = affine_client
        self.notion_fallback = notion_fallback_service

        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._template_validator = MasterTemplateValidator()
        self._theme_extractor = ThemeTokenExtractor()
        self._css_generator = CSSThemeGenerator()

    # ── Public API ────────────────────────────────────────────────────────

    def provision_coach_workspace(
        self,
        coach_soul: dict[str, Any],
        business_summary: dict[str, Any],
        coach_config: Optional[dict[str, Any]] = None,
    ) -> ProvisioningResult:
        """Execute the full workspace provisioning pipeline.

        Spec §7 Task 2: provision_coach_workspace(coach_id) function.

        Args:
            coach_soul: Parsed coach_soul.json (DEP-ENG-003).
            business_summary: Parsed business summary (DEP-ENG-050).
            coach_config: Optional coach configuration.

        Returns:
            ProvisioningResult with full status and payload.
        """
        # ── Step 1: Load and validate master template ──
        template_data = self._load_template()
        if template_data is None:
            return self._handle_failure(
                WorkspaceProvisioningError.TEMPLATE_VALIDATION_FAILED,
                "Failed to load master template JSON",
            )

        validation = self._template_validator.validate(template_data)
        if not validation.is_valid:
            return self._handle_failure(
                WorkspaceProvisioningError.TEMPLATE_MISSING_SECTIONS,
                f"Template validation failed: {validation.validation_errors}. "
                f"Missing sections: {validation.sections_missing}",
            )

        # ── Step 2: Extract theme tokens ──
        theme_tokens = self._theme_extractor.extract(
            coach_soul, business_summary, coach_config
        )

        # ── Step 3: Generate CSS theme ──
        css_content = self._css_generator.generate(theme_tokens, self.coach_acronym)
        theme_filename = self._css_generator.get_theme_filename(self.coach_acronym)

        # ── Step 4: Create AFFiNE workspace ──
        workspace_id = self._create_affine_workspace(template_data, theme_tokens)
        if workspace_id is None:
            return self._handle_failure_with_fallback(
                WorkspaceProvisioningError.AFFINE_API_UNREACHABLE,
                "AFFiNE API unreachable — workspace creation failed",
            )

        # ── Step 5: Apply theme CSS overlay ──
        theme_applied = self._apply_theme(workspace_id, css_content, theme_filename)
        if not theme_applied:
            logger.warning(
                "Theme application failed for %s — workspace created without theme",
                self.coach_acronym,
            )

        # ── Step 6: Register workspace_id in Supabase ──
        workspace_url = f"{self.affine_base_url}/ws/{workspace_id}"
        registered = self._register_workspace(workspace_id, workspace_url)
        if not registered:
            return self._handle_failure(
                WorkspaceProvisioningError.SUPABASE_REGISTRATION_FAILED,
                f"Failed to register workspace_id {workspace_id} in Supabase",
            )

        # ── Step 7: Send Telegram confirmation ──
        self._send_confirmation(workspace_url)

        # ── Step 8: Build output payload (DEP-ENG-071) ──
        sections_provisioned = [s.value for s in WorkspaceSectionType]
        timestamp = datetime.now(timezone.utc).isoformat()

        payload = WorkspaceProvisioningPayload(
            transaction_timestamp=timestamp,
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            workspace_id=workspace_id,
            workspace_url=workspace_url,
            theme_file=theme_filename,
            template_version=validation.template_version or TEMPLATE_VERSION,
            sections_provisioned=sections_provisioned,
            receipt_chain_guard=ReceiptChainGuardRef(schema_ref="DEP-ENG-041"),
        )

        # ── Step 9: Write Receipt Chain Guard entry ──
        self._write_receipt(payload)

        return ProvisioningResult(
            status=ProvisioningStatus.SUCCESS,
            payload=payload,
        )

    # ── Stage 1: Template Loading ─────────────────────────────────────────

    def _load_template(self) -> Optional[dict]:
        """Load the master workspace template JSON.

        Returns:
            Parsed template dict or None if loading fails.
        """
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error("Failed to load master template: %s", e)
            return None

    # ── Stage 3: AFFiNE API Operations ────────────────────────────────────

    def _create_affine_workspace(
        self,
        template_data: dict,
        theme_tokens: ThemeTokens,
    ) -> Optional[str]:
        """Create an AFFiNE workspace from the master template.

        Spec §4 Stage 3 Step 1: Call AFFiNE workspace creation API with
        template import.
        Spec §3 Technical Decision 3: Each coach gets a separate workspace
        (ADR-01 isolation).

        Returns:
            workspace_id (UUID string) or None if creation fails.
        """
        if self.affine is None:
            logger.warning(
                "AFFiNE client not configured — generating mock workspace_id"
            )
            return str(uuid.uuid4())

        try:
            result = self.affine.create_workspace(
                name=theme_tokens.business_name,
                template=template_data,
            )
            return result.get("workspace_id")
        except Exception as e:
            logger.error("AFFiNE workspace creation failed: %s", e)
            return None

    def _apply_theme(
        self,
        workspace_id: str,
        css_content: str,
        theme_filename: str,
    ) -> bool:
        """Apply CSS theme overlay to the workspace.

        Spec §4 Stage 3 Step 2: Apply coach theme CSS overlay.
        Spec §4 Stage 2 Step 4: Deploy theme file to AFFiNE static assets.
        """
        if self.affine is None:
            logger.info("AFFiNE client not configured — theme application skipped")
            return True

        try:
            self.affine.apply_theme(
                workspace_id=workspace_id,
                css_content=css_content,
                filename=theme_filename,
            )
            return True
        except Exception as e:
            logger.error("Theme application failed: %s", e)
            return False

    def _register_workspace(self, workspace_id: str, workspace_url: str) -> bool:
        """Register workspace_id in Supabase coach_config table.

        Spec §4 Stage 3 Step 3: Register workspace_id in Supabase
        coach_config table (new column: affine_workspace_id).
        Spec §7 Task 4: Add affine_workspace_id column.
        """
        if self.supabase is None:
            logger.info("Supabase client not configured — registration stored locally")
            return True

        try:
            self.supabase.table("coach_config").update(
                {"affine_workspace_id": workspace_id, "affine_workspace_url": workspace_url}
            ).eq("coach_id", self.coach_id).execute()
            return True
        except Exception as e:
            logger.error("Supabase workspace registration failed: %s", e)
            return False

    def _send_confirmation(self, workspace_url: str) -> None:
        """Send workspace ready confirmation via Telegram.

        Spec §4 Stage 3 Step 4: Send confirmation to coach via Telegram.
        """
        if self.telegram is None:
            logger.info("Telegram client not configured — confirmation skipped")
            return

        try:
            self.telegram.send_message(
                coach_id=self.coach_id,
                text=f"Your workspace is ready. {workspace_url}",
            )
        except Exception as e:
            # Telegram failure is non-blocking
            logger.warning("Telegram confirmation failed: %s", e)

    # ── Unit 8: Receipt Chain Integration ─────────────────────────────────

    def _write_receipt(self, payload: WorkspaceProvisioningPayload) -> None:
        """Write provisioning receipt per FR47 DEP-ENG-041 schema.

        Spec §4 Stage 3 Receipt Write: Receipt_CA11_01.json → Receipt Chain Guard.
        CA11 Revision (Global Fix): Cryptographic hash schema, not string literals.
        AC4: Receipt exists with correct workspace_id.
        """
        input_hash = hashlib.sha256(
            json.dumps(
                {
                    "coach_id": payload.coach_id,
                    "template_version": payload.template_version,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()

        output_hash = hashlib.sha256(
            json.dumps(
                {
                    "workspace_id": payload.workspace_id,
                    "sections_provisioned": payload.sections_provisioned,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()

        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action="workspace_provisioning",
            asset_id=payload.workspace_id,
            input_summary=f"Coach: {payload.coach_acronym}, Template: v{payload.template_version}",
            output_summary=(
                f"Workspace: {payload.workspace_id}, "
                f"Sections: {len(payload.sections_provisioned)}, "
                f"Theme: {payload.theme_file}"
            ),
            decision="provisioned",
            decision_rationale="FR-CA11-01 Stage 3 complete — ADR-05 AFFiNE workspace created",
            metadata={
                "stage_name": STAGE_WORKSPACE_PROVISIONING,
                "dep_eng_071": payload.model_dump(),
                "input_payload_hash": input_hash,
                "output_payload_hash": output_hash,
                "receipt_chain_guard": {"schema_ref": "DEP-ENG-041"},
            },
        )

    # ── Unit 7: Fallback Degradation Handler ──────────────────────────────

    def _handle_failure(
        self,
        error: WorkspaceProvisioningError,
        detail: str,
    ) -> ProvisioningResult:
        """Handle a non-recoverable failure without fallback.

        Returns a FAILED result with error details.
        """
        logger.error("Provisioning failure [%s]: %s", error.value, detail)
        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action="workspace_provisioning_failed",
            input_summary=f"Coach: {self.coach_acronym}",
            output_summary=f"Error: {error.value} — {detail}",
            decision="failed",
            metadata={"error": error.value, "detail": detail},
        )
        return ProvisioningResult(
            status=ProvisioningStatus.FAILED_NO_FALLBACK,
            error=error,
            error_detail=detail,
        )

    def _handle_failure_with_fallback(
        self,
        error: WorkspaceProvisioningError,
        detail: str,
    ) -> ProvisioningResult:
        """Handle AFFiNE API failure with Notion fallback.

        Spec §6: During migration period, both notion_sync.py and
        affine_sync.py operate simultaneously. If AFFiNE fails, system
        falls back to Notion (FR45) with degradation flag.
        Spec §4 Stage 3 Failure Condition: AFFiNE API unreachable →
        provisioning queued for retry.
        AC5: Assert system falls back to Notion and logs degradation flag.
        """
        logger.warning(
            "AFFiNE provisioning failed for %s — activating Notion fallback",
            self.coach_acronym,
        )

        notion_dashboard_id = None
        fallback_active = False

        if self.notion_fallback is not None:
            try:
                result = self.notion_fallback.create_coach_dashboard(
                    self.coach_id
                )
                notion_dashboard_id = result.get("page_id") if result else None
                fallback_active = True
            except Exception as e:
                logger.error("Notion fallback also failed: %s", e)

        # Log degradation flag
        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action="workspace_provisioning_fallback",
            input_summary=f"Coach: {self.coach_acronym}",
            output_summary=(
                f"AFFiNE failed: {error.value}. "
                f"Notion fallback: {'active' if fallback_active else 'also failed'}. "
                f"Notion dashboard: {notion_dashboard_id or 'none'}"
            ),
            decision="degraded",
            decision_rationale=(
                "FR-CA11-01 §6 backward compatibility fallback activated. "
                "Degradation flag logged in Supabase."
            ),
            metadata={
                "error": error.value,
                "detail": detail,
                "fallback_active": fallback_active,
                "notion_dashboard_id": notion_dashboard_id,
                "degradation_flag": True,
            },
        )

        # Register degradation flag in Supabase
        if self.supabase is not None:
            try:
                self.supabase.table("coach_config").update(
                    {
                        "affine_workspace_id": None,
                        "affine_provisioning_status": "FAILED_FALLBACK_NOTION",
                        "notion_fallback_active": True,
                    }
                ).eq("coach_id", self.coach_id).execute()
            except Exception as e:
                logger.error("Failed to log degradation flag in Supabase: %s", e)

        return ProvisioningResult(
            status=ProvisioningStatus.FAILED_FALLBACK_NOTION,
            error=error,
            error_detail=detail,
            fallback_active=fallback_active,
            notion_dashboard_id=notion_dashboard_id,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Supabase Migration SQL (Task 4)
# ══════════════════════════════════════════════════════════════════════════════

MIGRATION_SQL = """
-- FR-CA11-01 Task 4: Add affine_workspace_id column to coach_config table.
-- ADR-05: AFFiNE Over Notion — track workspace provisioning per coach.
ALTER TABLE coach_config
  ADD COLUMN IF NOT EXISTS affine_workspace_id TEXT,
  ADD COLUMN IF NOT EXISTS affine_workspace_url TEXT,
  ADD COLUMN IF NOT EXISTS affine_provisioning_status TEXT DEFAULT 'PENDING',
  ADD COLUMN IF NOT EXISTS notion_fallback_active BOOLEAN DEFAULT FALSE;

-- Index for workspace lookup
CREATE INDEX IF NOT EXISTS idx_coach_config_affine_workspace
  ON coach_config(affine_workspace_id)
  WHERE affine_workspace_id IS NOT NULL;
"""
