"""
FR-VIS-12 — Known Persons Registry — Integration Tests
Phase 2B, CVE Visual Engine — spec 6 of 13

Tests cover all 6 Acceptance Criteria (AC1-AC6) plus context routing matrix,
repetition window calculations, registry query, SERPER fallback,
AI generation prohibition, safety tests, and receipt chain integration
from FR-VIS-12 §8 and §10.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    REPETITION_WINDOW_DAYS,
    CanonicalImage,
    ContextValidationResult,
    ImageUsageLogEntry,
    KnownPersonRegistryEntry,
    KnownPersonsError,
    PersonRole,
    RepetitionCheckResult,
    ResolvedPersonImage,
)
from src.ccp.services.known_persons_registry_adapter import (
    KnownPersonsRegistryAdapter,
)


# ─────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────

NOW = datetime(2026, 3, 18, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def tmp_receipt_dir(tmp_path: Path) -> Path:
    d = tmp_path / "receipts"
    d.mkdir()
    return d


@pytest.fixture
def receipt_chain(tmp_receipt_dir: Path) -> ReceiptChain:
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_receipt_dir))


def _img(image_id: str, url: str = "https://r2.ccf-assets.com/test.jpg") -> CanonicalImage:
    return CanonicalImage(
        image_id=image_id,
        r2_cached_url=url,
        licensing_type="Editorial",
        licensing_source="Getty",
        resolution_px="2400x3600",
    )


def _usage(image_id: str, days_ago: int) -> ImageUsageLogEntry:
    used = NOW - timedelta(days=days_ago)
    return ImageUsageLogEntry(
        image_id=image_id,
        used_date=used.isoformat(),
        content_output_id=f"CO-TST-{days_ago}",
    )


def _brene_entry(
    images: list[CanonicalImage] | None = None,
    usage_log: list[ImageUsageLogEntry] | None = None,
    role: PersonRole = PersonRole.HERO,
) -> KnownPersonRegistryEntry:
    return KnownPersonRegistryEntry(
        registry_entry_id="KPR-001-BRENE-BROWN",
        person_name="Brené Brown",
        person_role=role,
        coach_id="coach_tst",
        canonical_images=images or [
            _img("KPR-IMG-001"),
            _img("KPR-IMG-002"),
        ],
        usage_log=usage_log or [],
        registry_status="ACTIVE",
    )


def _sinek_entry() -> KnownPersonRegistryEntry:
    return KnownPersonRegistryEntry(
        registry_entry_id="KPR-002-SIMON-SINEK",
        person_name="Simon Sinek",
        person_role=PersonRole.HERO,
        coach_id="coach_tst",
        canonical_images=[_img("KPR-IMG-010")],
        registry_status="ACTIVE",
    )


def _enemy_entry() -> KnownPersonRegistryEntry:
    return KnownPersonRegistryEntry(
        registry_entry_id="KPR-003-ENEMY",
        person_name="Gary Vee",
        person_role=PersonRole.ENEMY,
        coach_id="coach_tst",
        canonical_images=[_img("KPR-IMG-020")],
        registry_status="ACTIVE",
    )


@pytest.fixture
def adapter(receipt_chain: ReceiptChain) -> KnownPersonsRegistryAdapter:
    return KnownPersonsRegistryAdapter(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
        registry_data=[
            _brene_entry(
                usage_log=[
                    _usage("KPR-IMG-001", days_ago=21),  # 3 weeks ago (in window)
                    _usage("KPR-IMG-002", days_ago=63),  # 9 weeks ago (outside window)
                ],
            ),
            _sinek_entry(),
            _enemy_entry(),
        ],
    )


# ═════════════════════════════════════════════════════
# SECTION 1: CONTEXT ROUTING MATRIX — §4 Stage 2 / §10
# ═════════════════════════════════════════════════════


class TestContextRoutingMatrix:
    """§10 Unit: 4-role routing rules — all permitted/prohibited combos."""

    # ── Hero ──
    def test_hero_aspirational_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.HERO, "aspirational"
        )
        assert r.valid is True

    def test_hero_wisdom_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.HERO, "wisdom"
        )
        assert r.valid is True

    def test_hero_cautionary_negative_prohibited(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.HERO, "cautionary_negative"
        )
        assert r.valid is False
        assert "Permitted contexts" in (r.violation_detail or "")

    def test_hero_failure_prohibited(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.HERO, "failure"
        )
        assert r.valid is False

    # ── Enemy ──
    def test_enemy_cautionary_tale_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.ENEMY, "cautionary_tale"
        )
        assert r.valid is True

    def test_enemy_aspirational_prohibited(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.ENEMY, "aspirational"
        )
        assert r.valid is False

    def test_enemy_heroic_prohibited(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.ENEMY, "heroic"
        )
        assert r.valid is False

    # ── Mentor ──
    def test_mentor_wisdom_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.MENTOR, "wisdom"
        )
        assert r.valid is True

    def test_mentor_teaching_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.MENTOR, "teaching"
        )
        assert r.valid is True

    def test_mentor_negative_example_prohibited(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.MENTOR, "negative_example"
        )
        assert r.valid is False

    def test_mentor_competition_prohibited(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.MENTOR, "competition"
        )
        assert r.valid is False

    # ── Wildcard ──
    def test_wildcard_aspirational_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.WILDCARD, "aspirational"
        )
        assert r.valid is True

    def test_wildcard_negative_example_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.WILDCARD, "negative_example"
        )
        assert r.valid is True

    def test_wildcard_any_context_permitted(self) -> None:
        r = KnownPersonsRegistryAdapter.validate_context(
            "Test", PersonRole.WILDCARD, "random_custom_context"
        )
        assert r.valid is True


# ═════════════════════════════════════════════════════
# SECTION 2: REPETITION WINDOW — §4 Stage 3 / §10
# ═════════════════════════════════════════════════════


class TestRepetitionWindow:
    """§10 Unit: 56-day repetition window calculations."""

    def test_55_days_ago_in_window(self) -> None:
        """55 days < 56 → REPETITION_VIOLATION (still in window)."""
        images = [_img("IMG-1")]
        usage = [_usage("IMG-1", 55)]
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            images, usage, reference_date=NOW
        )
        assert r.clear is False
        assert r.all_in_window is True

    def test_57_days_ago_outside_window(self) -> None:
        """57 days > 56 → REPETITION_CLEAR."""
        images = [_img("IMG-1")]
        usage = [_usage("IMG-1", 57)]
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            images, usage, reference_date=NOW
        )
        assert r.clear is True
        assert r.selected_image_id == "IMG-1"

    def test_56_days_exactly_clears(self) -> None:
        """56 days exactly → CLEAR (window is ≥ 56 days, not >)."""
        images = [_img("IMG-1")]
        usage = [_usage("IMG-1", 56)]
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            images, usage, reference_date=NOW
        )
        assert r.clear is True

    def test_never_used_image_selected(self) -> None:
        """Image never used → ideal candidate."""
        images = [_img("IMG-1"), _img("IMG-2")]
        usage = [_usage("IMG-1", 10)]  # IMG-2 never used
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            images, usage, reference_date=NOW
        )
        assert r.clear is True
        assert r.selected_image_id == "IMG-2"

    def test_select_least_recently_used(self) -> None:
        """Multiple outside window → select most stale (least recently used)."""
        images = [_img("IMG-1"), _img("IMG-2"), _img("IMG-3")]
        usage = [
            _usage("IMG-1", 60),
            _usage("IMG-2", 90),
            _usage("IMG-3", 120),
        ]
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            images, usage, reference_date=NOW
        )
        assert r.clear is True
        assert r.selected_image_id == "IMG-3"  # 120 days = most stale

    def test_5_images_priority_selection(self) -> None:
        """§10: 5 images [10, 30, 60, 90, 120] → select 60 (first outside, but LRU among viable)."""
        images = [_img(f"IMG-{i}") for i in range(5)]
        usage = [
            _usage("IMG-0", 10),
            _usage("IMG-1", 30),
            _usage("IMG-2", 60),
            _usage("IMG-3", 90),
            _usage("IMG-4", 120),
        ]
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            images, usage, reference_date=NOW
        )
        assert r.clear is True
        # Should prefer IMG-4 (most stale = 120 days)
        assert r.selected_image_id == "IMG-4"

    def test_no_images_returns_all_in_window(self) -> None:
        r = KnownPersonsRegistryAdapter.check_repetition_window(
            [], [], reference_date=NOW
        )
        assert r.clear is False
        assert r.all_in_window is True


# ═════════════════════════════════════════════════════
# SECTION 3: AC1 — REGISTRY MATCH HAPPY PATH
# FR-VIS-12 §8 AC1
# ═════════════════════════════════════════════════════


class TestAC1RegistryMatchHappyPath:
    """AC1: Brené Brown, 2 images. Image 1 used 3 weeks ago (in window).
    Image 2 used 9 weeks ago (outside window). → selects Image 2."""

    def test_selects_image_2(self, adapter: KnownPersonsRegistryAdapter) -> None:
        result = adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational_transformation",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC1-001",
            reference_date=NOW,
        )
        assert result.selected_image is not None
        assert result.selected_image.image_id == "KPR-IMG-002"
        assert result.error_type is None

    def test_repetition_clear(self, adapter: KnownPersonsRegistryAdapter) -> None:
        result = adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC1-002",
            reference_date=NOW,
        )
        assert result.repetition_check is not None
        assert result.repetition_check.clear is True

    def test_context_validated(self, adapter: KnownPersonsRegistryAdapter) -> None:
        result = adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC1-003",
            reference_date=NOW,
        )
        assert result.context_validation is not None
        assert result.context_validation.valid is True

    def test_source_type_registry(self, adapter: KnownPersonsRegistryAdapter) -> None:
        result = adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC1-004",
            reference_date=NOW,
        )
        assert result.source_type == "known_persons_registry"
        assert result.sourcing_tier == "tier_1_real_person"


# ═════════════════════════════════════════════════════
# SECTION 4: AC2 — HERO IN NEGATIVE CONTEXT
# FR-VIS-12 §8 AC2
# ═════════════════════════════════════════════════════


class TestAC2HeroInNegativeContext:
    """AC2: Simon Sinek (Hero) in cautionary_negative → CONTEXT_VIOLATION."""

    def test_context_violation_returned(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        result = adapter.resolve_person(
            person_name="Simon Sinek",
            person_role=PersonRole.HERO,
            slide_index=3,
            slide_context="cautionary_negative",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC2-001",
            reference_date=NOW,
        )
        assert result.error_type == KnownPersonsError.CONTEXT_VIOLATION.value
        assert "cautionary_negative" in (result.error_detail or "")
        assert "Permitted contexts" in (result.error_detail or "")

    def test_no_image_selected_on_violation(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        result = adapter.resolve_person(
            person_name="Simon Sinek",
            person_role=PersonRole.HERO,
            slide_index=3,
            slide_context="cautionary_negative",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC2-002",
            reference_date=NOW,
        )
        assert result.selected_image is None


# ═════════════════════════════════════════════════════
# SECTION 5: AC3 — ENEMY IN ASPIRATIONAL CONTEXT
# FR-VIS-12 §8 AC3
# ═════════════════════════════════════════════════════


class TestAC3EnemyInAspirationalContext:
    """AC3: Enemy in aspirational_transformation → CONTEXT_VIOLATION."""

    def test_enemy_aspirational_violation(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        result = adapter.resolve_person(
            person_name="Gary Vee",
            person_role=PersonRole.ENEMY,
            slide_index=1,
            slide_context="aspirational_transformation",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC3-001",
            reference_date=NOW,
        )
        assert result.error_type == KnownPersonsError.CONTEXT_VIOLATION.value

    def test_enemy_cautionary_permitted(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        result = adapter.resolve_person(
            person_name="Gary Vee",
            person_role=PersonRole.ENEMY,
            slide_index=1,
            slide_context="cautionary_tale",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC3-002",
            reference_date=NOW,
        )
        assert result.error_type is None
        assert result.selected_image is not None


# ═════════════════════════════════════════════════════
# SECTION 6: AC4 — ALL IMAGES IN WINDOW
# FR-VIS-12 §8 AC4
# ═════════════════════════════════════════════════════


class TestAC4AllImagesInWindow:
    """AC4: 3 images all used within 8 weeks → ALL_IMAGES_IN_WINDOW → SERPER."""

    def test_all_in_window_triggers_serper(
        self, receipt_chain: ReceiptChain
    ) -> None:
        entry = _brene_entry(
            images=[_img("IMG-A"), _img("IMG-B"), _img("IMG-C")],
            usage_log=[
                _usage("IMG-A", 10),
                _usage("IMG-B", 20),
                _usage("IMG-C", 40),
            ],
        )
        adapter = KnownPersonsRegistryAdapter(
            coach_acronym="TST",
            receipt_chain=receipt_chain,
            registry_data=[entry],
        )
        result = adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC4-001",
            reference_date=NOW,
        )
        assert result.error_type == KnownPersonsError.ALL_IMAGES_IN_WINDOW.value
        assert result.source_type == "serper_fallback"
        assert result.pending_registry_addition is True


# ═════════════════════════════════════════════════════
# SECTION 7: AC5 — PERSON NOT IN REGISTRY
# FR-VIS-12 §8 AC5
# ═════════════════════════════════════════════════════


class TestAC5PersonNotInRegistry:
    """AC5: Adam Grant not in registry → PERSON_NOT_IN_REGISTRY + SERPER fallback."""

    def test_not_in_registry_serper_fallback(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        result = adapter.resolve_person(
            person_name="Adam Grant",
            person_role=PersonRole.HERO,
            slide_index=4,
            slide_context="wisdom",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC5-001",
            reference_date=NOW,
        )
        assert result.error_type == KnownPersonsError.PERSON_NOT_IN_REGISTRY.value
        assert result.pending_registry_addition is True
        assert result.source_type == "serper_fallback"

    def test_not_in_registry_has_receipt(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        result = adapter.resolve_person(
            person_name="Adam Grant",
            person_role=PersonRole.HERO,
            slide_index=4,
            slide_context="wisdom",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC5-002",
            reference_date=NOW,
        )
        assert result.receipt_chain_block is not None


# ═════════════════════════════════════════════════════
# SECTION 8: AC6 — AI GENERATION PROHIBITION
# FR-VIS-12 §8 AC6
# ═════════════════════════════════════════════════════


class TestAC6AIGenerationProhibition:
    """AC6: Named person NEVER routes to AI generation (Tier 3/4)."""

    def test_assert_no_ai_generation_raises(self) -> None:
        with pytest.raises(RuntimeError, match="AI_GENERATION_PROHIBITED"):
            KnownPersonsRegistryAdapter.assert_no_ai_generation("Elon Musk")

    def test_assert_includes_person_name(self) -> None:
        with pytest.raises(RuntimeError, match="Elon Musk"):
            KnownPersonsRegistryAdapter.assert_no_ai_generation("Elon Musk")

    def test_resolved_person_never_has_ai_tier(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        """Even when registry fails, result never has Tier 3/4."""
        result = adapter.resolve_person(
            person_name="Unknown Person",
            person_role=PersonRole.HERO,
            slide_index=0,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-AC6-001",
            reference_date=NOW,
        )
        assert result.sourcing_tier == "tier_1_real_person"
        # Even on failure, never routes to AI
        assert "tier_3" not in result.sourcing_tier
        assert "tier_4" not in result.sourcing_tier


# ═════════════════════════════════════════════════════
# SECTION 9: REGISTRY QUERY — §4 Stage 1
# ═════════════════════════════════════════════════════


class TestRegistryQuery:
    """§4 Stage 1: Query and lookup logic."""

    def test_case_insensitive_lookup(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        entry = adapter.query_registry("brené brown", "coach_tst")
        assert entry is not None
        assert entry.person_name == "Brené Brown"

    def test_unknown_person_returns_none(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        entry = adapter.query_registry("Unknown Person", "coach_tst")
        assert entry is None

    def test_timeout_returns_none(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        entry = adapter.query_registry(
            "Brené Brown", "coach_tst", simulate_timeout=True
        )
        assert entry is None


# ═════════════════════════════════════════════════════
# SECTION 10: SAFETY TESTS — §10
# ═════════════════════════════════════════════════════


class TestSafetyInjectionResistance:
    """§10: Registry injection attack resistance."""

    def test_sql_injection_in_person_name(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        """Injected SQL treated as literal string → no match."""
        entry = adapter.query_registry(
            "Brené Brown'; DROP DATABASE known_persons;", "coach_tst"
        )
        assert entry is None

    def test_xss_in_person_name(
        self, adapter: KnownPersonsRegistryAdapter
    ) -> None:
        entry = adapter.query_registry(
            '<script>alert("xss")</script>', "coach_tst"
        )
        assert entry is None


# ═════════════════════════════════════════════════════
# SECTION 11: RECEIPT CHAIN INTEGRATION
# ═════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """DEP-ENG-041: Receipt writes at every stage."""

    def test_happy_path_writes_4_receipts(
        self, adapter: KnownPersonsRegistryAdapter, receipt_chain: ReceiptChain
    ) -> None:
        """4 stages → 4 receipt writes."""
        initial = receipt_chain.chain_length()
        adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-RCH-001",
            reference_date=NOW,
        )
        assert receipt_chain.chain_length() == initial + 4

    def test_not_found_writes_1_receipt(
        self, adapter: KnownPersonsRegistryAdapter, receipt_chain: ReceiptChain
    ) -> None:
        initial = receipt_chain.chain_length()
        adapter.resolve_person(
            person_name="Adam Grant",
            person_role=PersonRole.HERO,
            slide_index=4,
            slide_context="wisdom",
            coach_id="coach_tst",
            content_output_id="CO-TST-RCH-002",
            reference_date=NOW,
        )
        assert receipt_chain.chain_length() == initial + 1

    def test_receipt_actions_present(
        self, adapter: KnownPersonsRegistryAdapter, receipt_chain: ReceiptChain
    ) -> None:
        adapter.resolve_person(
            person_name="Brené Brown",
            person_role=PersonRole.HERO,
            slide_index=2,
            slide_context="aspirational",
            coach_id="coach_tst",
            content_output_id="CO-TST-RCH-003",
            reference_date=NOW,
        )
        entries = receipt_chain.query(agent_id="known_persons_registry", limit=100)
        actions = {e.action for e in entries}
        assert "VIS12_REGISTRY_QUERY" in actions
        assert "VIS12_CONTEXT_VALIDATION" in actions
        assert "VIS12_REPETITION_CHECK" in actions
        assert "VIS12_IMAGE_RESOLUTION" in actions


# ═════════════════════════════════════════════════════
# SECTION 12: ADR-01 COACH ACRONYM
# ═════════════════════════════════════════════════════


class TestADR01CoachAcronym:
    """ADR-01: 2-4 character coach acronym enforcement."""

    def test_valid_2_char(self, receipt_chain: ReceiptChain) -> None:
        a = KnownPersonsRegistryAdapter(coach_acronym="JP", receipt_chain=receipt_chain)
        assert a.coach_acronym == "JP"

    def test_valid_4_char(self, receipt_chain: ReceiptChain) -> None:
        a = KnownPersonsRegistryAdapter(coach_acronym="JPGR", receipt_chain=receipt_chain)
        assert a.coach_acronym == "JPGR"

    def test_1_char_rejected(self, receipt_chain: ReceiptChain) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            KnownPersonsRegistryAdapter(coach_acronym="J", receipt_chain=receipt_chain)

    def test_5_char_rejected(self, receipt_chain: ReceiptChain) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            KnownPersonsRegistryAdapter(coach_acronym="JPGRS", receipt_chain=receipt_chain)
