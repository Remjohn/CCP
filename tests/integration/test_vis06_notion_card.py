"""
FR-VIS-06 — Notion Visual Content Card — Integration Tests
===========================================================
60 tests covering 6 ACs × 6 sections + ADR-01 + receipt + edge cases.
"""

from __future__ import annotations

import tempfile
from typing import Any
from unittest.mock import MagicMock

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AGSSAuditEntry,
    AuthenticityAuditEntry,
    CardHeader,
    ContentReadyToCopy,
    LeadershipFarmingNote,
    LeadershipTrait,
    NotionCardError,
    PostingRecommendation,
    PreviewAssets,
    SlidePreview,
    TechnicalAudit,
    TIARDecayEntry,
    VPONotionCard,
    VPOSyncStatus,
    WhyThisVisual,
)
from src.ccp.services.notion_visual_content_card import (
    NotionVisualContentCardService,
    compute_fingerprint,
    register_rationale_template,
    register_leadership_mapping,
    _sanitise,
)


# ═══════════════════════════════════════════════════════════════════════
# Fixtures & Helpers
# ═══════════════════════════════════════════════════════════════════════

_DEFAULT_RECIPE = "dopamine_cliff"


def _ensure_templates() -> None:
    register_rationale_template(
        recipe_type="dopamine_cliff",
        arc_type_explanation=(
            "This carousel follows a Tension-Release arc — the first 4 "
            "slides build frustrated stagnation using progressively tighter "
            "framing and cooler colors, then slide 5 releases with warm, "
            "expansive composition."
        ),
        style_rationale=(
            "Cinematic color grading was selected because your audience's "
            "CBCS (6) is at the trust-authentication stage."
        ),
        tribal_function=(
            "This visual exercises the Observer leadership trait — naming "
            "a shared experience without prescribing a solution."
        ),
    )


def _make_service(
    coach: str = "TST",
    notion: Any = "DEFAULT",
) -> tuple[NotionVisualContentCardService, ReceiptChain]:
    _ensure_templates()
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    if notion == "DEFAULT":
        notion = _good_notion()
    svc = NotionVisualContentCardService(
        coach_acronym=coach,
        coach_id="coach_test",
        receipt_chain=rc,
        notion_client=notion,
        notion_database_id="db-123",
    )
    return svc, rc


def _good_notion() -> MagicMock:
    mock = MagicMock()
    mock.create_page.return_value = {"id": "notion-page-abc-123"}
    return mock


def _default_vcb() -> dict[str, Any]:
    return {
        "recipe_name": "Dopamine Cliff Carousel — Tension-Release Arc",
        "recipe_type": "dopamine_cliff",
        "production_status": "APPROVED",
        "visual_style": "Cinematic Color Graded",
    }


def _default_validations() -> list[dict[str, Any]]:
    return [
        {
            "slide_index": 0,
            "agss": {
                "composite_score": 7.8,
                "lighting_naturalism": 8.2,
                "texture_authenticity": 7.5,
                "compositional_coherence": 7.9,
                "emotional_believability": 7.6,
            },
            "authenticity": {
                "expression_naturalness": "PASS",
                "facial_proportion": "PASS",
                "skin_texture": "PASS",
            },
        }
    ]


def _default_tiar() -> list[dict[str, Any]]:
    return [
        {"noun": "the 5am alarm defeat", "tirs_score": 8.7, "decay_stage": "in_distribution", "last_measured": "2026-03-17"},
        {"noun": "Sunday night dread spiral", "tirs_score": 9.1, "decay_stage": "in_distribution", "last_measured": "2026-03-17"},
        {"noun": "revenue plateau confession", "tirs_score": 6.8, "decay_stage": "decay_approaching", "last_measured": "2026-03-17"},
    ]


def _default_export_assets() -> dict[str, Any]:
    return {
        "type": "carousel",
        "horizontal_stitch_url": "https://r2.ccf-assets.com/stitch.png",
        "slide_previews": [
            {"slide_index": 0, "url": "https://r2.ccf-assets.com/s0.png"},
            {"slide_index": 1, "url": "https://r2.ccf-assets.com/s1.png"},
        ],
        "zip_download_url": "https://r2.ccf-assets.com/all.zip",
    }


def _default_content_output() -> dict[str, Any]:
    return {
        "hook_text": "The 5am alarm goes off. You don't hit snooze.",
        "full_caption": "The Sunday night dread spiral isn't about Monday...",
        "hashtags": "#consciouscoaching, #leadershipdevelopment",
        "posting_recommendation": {
            "day": "Thursday",
            "time": "09:30",
            "rationale": "Peak engagement window",
        },
    }


def _assemble_full(svc: NotionVisualContentCardService) -> VPONotionCard:
    return svc.assemble_vpo(
        composition_id="COMP-TST-001",
        vcb_data=_default_vcb(),
        validation_results=_default_validations(),
        tiar_audit=_default_tiar(),
        export_assets=_default_export_assets(),
        content_output=_default_content_output(),
        receipt_block_ids=["RCB-001", "RCB-002"],
    )


# ═══════════════════════════════════════════════════════════════════════
# § Enums
# ═══════════════════════════════════════════════════════════════════════


class TestEnums:
    def test_vpo_sync_status_members(self):
        assert set(VPOSyncStatus.__members__.keys()) == {
            "SYNCED", "DELAYED_SYNC", "SYNC_FAILED", "QUEUED", "R2_FALLBACK",
        }

    def test_notion_card_error_members(self):
        assert set(NotionCardError.__members__.keys()) == {
            "MISSING_UPSTREAM_DATA",
            "NOTION_API_FAILURE",
            "R2_UPLOAD_FAILURE",
            "INVALID_COACH_ACRONYM",
            "FINGERPRINT_MISMATCH",
            "TEMPLATE_RATIONALE_MISSING",
        }

    def test_leadership_trait_members(self):
        assert set(LeadershipTrait.__members__.keys()) == {
            "OBSERVER", "PROVOCATEUR", "SHEPHERD", "ARCHITECT", "MIRROR",
        }


# ═══════════════════════════════════════════════════════════════════════
# § AC1: Complete VPO Card (all 6 sections)
# ═══════════════════════════════════════════════════════════════════════


class TestAC1_CompleteCard:
    def test_card_has_header(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.card_header.recipe_name != ""
        assert card.card_header.universal_asset_id != ""

    def test_card_has_preview(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert len(card.preview_assets.slide_previews) == 2
        assert card.preview_assets.zip_download_url is not None

    def test_card_has_content(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "5am alarm" in card.content_ready_to_copy.hook_text

    def test_card_has_rationale(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "Tension-Release" in card.why_this_visual.arc_type_explanation

    def test_card_has_farming_note(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.leadership_farming_note.trait == LeadershipTrait.OBSERVER.value

    def test_card_has_audit(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.technical_audit.collapsed is True
        assert len(card.technical_audit.tiar_decay_status) == 3
        assert len(card.technical_audit.agss_scores) == 1

    def test_vpo_id_contains_coach(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "TST" in card.vpo_id

    def test_notion_page_id_set(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.notion_page_id == "notion-page-abc-123"

    def test_sync_status_synced(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.sync_status == VPOSyncStatus.SYNCED.value


# ═══════════════════════════════════════════════════════════════════════
# § AC2: Rationale Content (non-generic)
# ═══════════════════════════════════════════════════════════════════════


class TestAC2_Rationale:
    def test_arc_type_contains_recipe_specific_text(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "Tension-Release" in card.why_this_visual.arc_type_explanation
        assert len(card.why_this_visual.arc_type_explanation) > 50

    def test_tiar_noun_rationale_contains_nouns(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "5am alarm defeat" in card.why_this_visual.tiar_noun_rationale
        assert "8.7" in card.why_this_visual.tiar_noun_rationale

    def test_style_rationale_not_generic(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "Cinematic" in card.why_this_visual.style_rationale or "CBCS" in card.why_this_visual.style_rationale

    def test_tribal_function_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert len(card.why_this_visual.tribal_function) > 20

    def test_missing_recipe_type_uses_placeholder(self):
        svc, _ = _make_service()
        vcb = _default_vcb()
        vcb["recipe_type"] = "nonexistent_recipe"
        card = svc.assemble_vpo(
            composition_id="COMP-TST-001",
            vcb_data=vcb,
        )
        assert "DATA_UNAVAILABLE" in card.why_this_visual.arc_type_explanation
        assert any("TEMPLATE_RATIONALE_MISSING" in w for w in card.warnings)


# ═══════════════════════════════════════════════════════════════════════
# § AC3: Technical Audit Collapsed
# ═══════════════════════════════════════════════════════════════════════


class TestAC3_TechAudit:
    def test_audit_collapsed_by_default(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.technical_audit.collapsed is True

    def test_tiar_decay_table_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert len(card.technical_audit.tiar_decay_status) == 3

    def test_agss_scores_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert len(card.technical_audit.agss_scores) == 1
        assert card.technical_audit.agss_scores[0].composite == 7.8

    def test_authenticity_checks_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert len(card.technical_audit.authenticity_checks) == 1
        assert card.technical_audit.authenticity_checks[0].expression == "PASS"

    def test_receipt_chain_status(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.technical_audit.receipt_chain_status == "VALID"
        assert len(card.technical_audit.receipt_chain_blocks) == 2

    def test_fingerprint_id_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert card.technical_audit.fingerprint_id is not None
        assert card.technical_audit.fingerprint_id.startswith("SHA256:")


# ═══════════════════════════════════════════════════════════════════════
# § AC4: TIAR Decay Visibility
# ═══════════════════════════════════════════════════════════════════════


class TestAC4_TIARDecay:
    def test_all_nouns_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        nouns = [e.noun for e in card.technical_audit.tiar_decay_status]
        assert "the 5am alarm defeat" in nouns
        assert "revenue plateau confession" in nouns

    def test_decay_approaching_noun_flagged(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        decay_entries = [
            e for e in card.technical_audit.tiar_decay_status
            if e.decay_stage == "decay_approaching"
        ]
        assert len(decay_entries) >= 1
        assert decay_entries[0].noun == "revenue plateau confession"

    def test_tirs_scores_preserved(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        by_noun = {e.noun: e for e in card.technical_audit.tiar_decay_status}
        assert by_noun["the 5am alarm defeat"].tirs_score == 8.7
        assert by_noun["Sunday night dread spiral"].tirs_score == 9.1


# ═══════════════════════════════════════════════════════════════════════
# § AC5: Content Ready to Copy
# ═══════════════════════════════════════════════════════════════════════


class TestAC5_ContentCopy:
    def test_hook_text_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "5am alarm" in card.content_ready_to_copy.hook_text

    def test_hashtags_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "#consciouscoaching" in card.content_ready_to_copy.hashtags

    def test_posting_recommendation_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        pr = card.content_ready_to_copy.posting_recommendation
        assert pr is not None
        assert pr.day == "Thursday"
        assert pr.time == "09:30"

    def test_full_caption_present(self):
        svc, _ = _make_service()
        card = _assemble_full(svc)
        assert "Sunday night" in card.content_ready_to_copy.full_caption


# ═══════════════════════════════════════════════════════════════════════
# § AC6: Sync Failure Fallback
# ═══════════════════════════════════════════════════════════════════════


class TestAC6_SyncFallback:
    def test_notion_failure_stores_r2(self):
        mock = MagicMock()
        mock.create_page.side_effect = RuntimeError("Notion API down")
        svc, _ = _make_service(notion=mock)
        card = _assemble_full(svc)
        assert card.sync_status == VPOSyncStatus.SYNC_FAILED.value
        assert card.r2_fallback_url is not None
        assert "vpo-fallback" in card.r2_fallback_url

    def test_notion_failure_warning_present(self):
        mock = MagicMock()
        mock.create_page.side_effect = RuntimeError("API down")
        svc, _ = _make_service(notion=mock)
        card = _assemble_full(svc)
        assert any("Notion sync failed" in w for w in card.warnings)

    def test_no_notion_client_uses_r2(self):
        svc, _ = _make_service(notion=None)
        card = _assemble_full(svc)
        assert card.sync_status == VPOSyncStatus.R2_FALLBACK.value
        assert card.r2_fallback_url is not None

    def test_retry_sync_succeeds(self):
        # First assemble fails
        failing = MagicMock()
        failing.create_page.side_effect = RuntimeError("down")
        svc, _ = _make_service(notion=failing)
        card = _assemble_full(svc)
        assert card.sync_status == VPOSyncStatus.SYNC_FAILED.value

        # Now retry with working client
        svc._notion = _good_notion()
        card = svc.retry_sync(card)
        assert card.sync_status == VPOSyncStatus.DELAYED_SYNC.value
        assert card.notion_page_id is not None

    def test_retry_without_client_warns(self):
        svc, _ = _make_service(notion=None)
        card = _assemble_full(svc)
        svc._notion = None
        card = svc.retry_sync(card)
        assert any("still unavailable" in w for w in card.warnings)


# ═══════════════════════════════════════════════════════════════════════
# § Missing Upstream Data
# ═══════════════════════════════════════════════════════════════════════


class TestMissingData:
    def test_missing_export_assets_warning(self):
        svc, _ = _make_service()
        card = svc.assemble_vpo(
            composition_id="COMP-TST-001",
            vcb_data=_default_vcb(),
            export_assets=None,
        )
        assert any("MISSING_UPSTREAM_DATA: export_assets" in w for w in card.warnings)

    def test_missing_content_output_warning(self):
        svc, _ = _make_service()
        card = svc.assemble_vpo(
            composition_id="COMP-TST-001",
            vcb_data=_default_vcb(),
            content_output=None,
        )
        assert any("MISSING_UPSTREAM_DATA: content_output" in w for w in card.warnings)
        assert card.content_ready_to_copy.hook_text == "DATA_UNAVAILABLE"

    def test_missing_validations_warning(self):
        svc, _ = _make_service()
        card = svc.assemble_vpo(
            composition_id="COMP-TST-001",
            vcb_data=_default_vcb(),
            validation_results=None,
        )
        assert any("MISSING_UPSTREAM_DATA: validation_results" in w for w in card.warnings)

    def test_missing_tiar_warning(self):
        svc, _ = _make_service()
        card = svc.assemble_vpo(
            composition_id="COMP-TST-001",
            vcb_data=_default_vcb(),
            tiar_audit=None,
        )
        assert any("MISSING_UPSTREAM_DATA: tiar_audit" in w for w in card.warnings)

    def test_no_silent_omission(self):
        """Even with all upstreams missing, card has all 6 sections (with placeholders)."""
        svc, _ = _make_service()
        card = svc.assemble_vpo(
            composition_id="COMP-TST-001",
            vcb_data={"recipe_type": "dopamine_cliff", "recipe_name": "X", "production_status": "A", "visual_style": "Y"},
        )
        assert card.card_header is not None
        assert card.preview_assets is not None
        assert card.content_ready_to_copy is not None
        assert card.why_this_visual is not None
        assert card.leadership_farming_note is not None
        assert card.technical_audit is not None


# ═══════════════════════════════════════════════════════════════════════
# § XSS Sanitisation
# ═══════════════════════════════════════════════════════════════════════


class TestXSS:
    def test_script_stripped(self):
        assert _sanitise('<script>alert("xss")</script>Hello') == "Hello"

    def test_html_tags_stripped(self):
        assert _sanitise("<b>Bold</b>") == "Bold"

    def test_clean_text_unchanged(self):
        assert _sanitise("Normal text") == "Normal text"


# ═══════════════════════════════════════════════════════════════════════
# § ADR-01
# ═══════════════════════════════════════════════════════════════════════


class TestADR01:
    def test_valid_3char_coach(self):
        svc, _ = _make_service(coach="TST")
        card = _assemble_full(svc)
        assert card.coach_acronym == "TST"

    def test_alt_3char_coach(self):
        svc, _ = _make_service(coach="ABC")
        card = _assemble_full(svc)
        assert card.coach_acronym == "ABC"
        assert "ABC" in card.vpo_id

    def test_1char_rejected_by_service(self):
        """1-char coach should be rejected at the service level."""
        tmp = tempfile.mkdtemp()
        # ReceiptChain also rejects <3, but we test the service validation path
        with pytest.raises((ValueError,)):
            NotionVisualContentCardService(
                coach_acronym="X",
                coach_id="test",
                receipt_chain=ReceiptChain(coach_acronym="TST", log_dir=tmp),
                notion_database_id="db",
            )

    def test_5char_rejected_by_service(self):
        tmp = tempfile.mkdtemp()
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            NotionVisualContentCardService(
                coach_acronym="ABCDE",
                coach_id="test",
                receipt_chain=ReceiptChain(coach_acronym="TST", log_dir=tmp),
                notion_database_id="db",
            )

    def test_empty_rejected(self):
        """Empty coach string rejected by service."""
        tmp = tempfile.mkdtemp()
        with pytest.raises((ValueError,)):
            NotionVisualContentCardService(
                coach_acronym="",
                coach_id="test",
                receipt_chain=ReceiptChain(coach_acronym="TST", log_dir=tmp),
                notion_database_id="db",
            )


# ═══════════════════════════════════════════════════════════════════════
# § Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    def test_receipt_logged_on_assemble(self):
        svc, rc = _make_service()
        _assemble_full(svc)
        entries = rc.query(action="vpo-assemble")
        assert len(entries) >= 1

    def test_receipt_metadata_has_fingerprint(self):
        svc, rc = _make_service()
        _assemble_full(svc)
        entries = rc.query(action="vpo-assemble")
        assert "fingerprint" in entries[0].metadata

    def test_retry_receipt_logged(self):
        failing = MagicMock()
        failing.create_page.side_effect = RuntimeError("down")
        svc, rc = _make_service(notion=failing)
        card = _assemble_full(svc)
        svc._notion = _good_notion()
        svc.retry_sync(card)
        entries = rc.query(action="vpo-retry-sync")
        assert len(entries) >= 1


# ═══════════════════════════════════════════════════════════════════════
# § Fingerprint
# ═══════════════════════════════════════════════════════════════════════


class TestFingerprint:
    def test_deterministic(self):
        data = {"a": 1, "b": "hello"}
        assert compute_fingerprint(data) == compute_fingerprint(data)

    def test_different_data_different_hash(self):
        assert compute_fingerprint({"a": 1}) != compute_fingerprint({"a": 2})

    def test_starts_with_sha256(self):
        fp = compute_fingerprint({"x": "y"})
        assert fp.startswith("SHA256:")
        assert len(fp) > 70  # SHA256: + 64 hex chars


# ═══════════════════════════════════════════════════════════════════════
# § Model Validation
# ═══════════════════════════════════════════════════════════════════════


class TestModelValidation:
    def test_tiar_score_clamped(self):
        with pytest.raises(Exception):
            TIARDecayEntry(noun="test", tirs_score=11.0, decay_stage="x", last_measured="d")

    def test_agss_audit_score_clamped(self):
        with pytest.raises(Exception):
            AGSSAuditEntry(
                slide_index=0, composite=11.0,
                lighting=0, texture=0, composition=0, emotion=0,
            )
