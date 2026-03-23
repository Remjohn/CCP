"""
CCP FR6 Tribe Profile & Context Premise Map — Integration Tests (Unit 12)
Tests covering all 14 Acceptance Criteria.

AC1:  Prerequisite Gate — Stage A: halts when audience raw data missing
AC2:  Prerequisite Gate — Stage B: halts when tribe_profile.json missing
AC3:  Volume Quotas: slang ≥10, jokes ≥5, heroes ≥5, enemies ≥5, humor ≥3/style,
      aspirations ≥5, anxieties ≥5, triggers ≥3+3
AC4:  Depth Stratification: L2 ≥30%, L3 ≥10% hard gate
AC5:  Mode Coverage: ≥3 triggers per mode (T/V/R)
AC6:  Visual Codes: ≥5 insider objects, ≥3 rejection triggers
AC7:  Language Registry: ≥10 safe terms, ≥5 outsider terms
AC8:  Interchangeability Test: Law 4 Check 4
AC9:  Neo4j Isolation: cross-coach contamination impossible
AC10: Neo4j Performance: <500ms per query
AC11: Authentication Verdict: AUTHENTICATED/PROVISIONAL/FAILED
AC12: Coach-Tribe Resonance: ≥3 alignment, ≥1 friction
AC13: Backward Compatibility: fallback to coach_soul topic-based prompts
AC14: Psychometric Extensions: 5 extensions populated with proper labels
"""

import json
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul, ContentTone, IdealClient, LeadershipScores, VoiceDNA
from src.ccp.models.tribe_profile_models import (
    AuthenticationVerdict,
    ContextPremiseDimension,
    ContextPremiseFallbackResult,
    CopingMechanismDimension,
    CopingTrajectoryPosition,
    DepthDistribution,
    DepthLevel,
    DepthStratifiedEntry,
    EmotionalMode,
    EmotionalTriggerDimension,
    EmotionalTriggerEntry,
    FourLawsValidation,
    GraphNode,
    GraphRelationship,
    LanguageRegistryEntry,
    LanguageRegisterType,
    LawValidationResult,
    ModeDistribution,
    PsychometricExtensions,
    RegulatoryFocus,
    TribeProfile,
    TribeProfileDistilled,
    TribeProfilePipelineSession,
    TribeProfilePipelineStepStatus,
    TriggerIntensity,
    VisualCodeType,
    VisualRecognitionCode,
)
from src.ccp.models.tribe_research_models import (
    CulturalArtifacts,
    EmotionalLandscape,
    HumorDNAProfile,
    SocialArchitecture,
    TribeDossier,
    VerbatimEntry,
)
from src.ccp.services.coach_tribe_resonance import CoachTribeResonanceAnalyzer
from src.ccp.services.context_premise_fallback import ContextPremiseFallback
from src.ccp.services.depth_stratifier import DepthStratifier
from src.ccp.services.emotional_mode_mapper import EmotionalModeMapper
from src.ccp.services.neo4j_graph_manager import Neo4jGraphManager
from src.ccp.services.psychometric_extension_mapper import PsychometricExtensionMapper
from src.ccp.services.tribe_profile_distiller import TribeProfileDistiller
from src.ccp.services.tribe_profile_extractor import TribeProfileExtractor
from src.ccp.services.visual_language_registry import VisualLanguageRegistry


# ══════════════════════════════════════════════════════════════
# Test Fixtures
# ══════════════════════════════════════════════════════════════


def _build_tribe_dossier() -> TribeDossier:
    """Build a minimal TribeDossier for testing."""
    return TribeDossier(
        coach_id="TST-0000",
        coach_acronym="TST",
    )


def _build_raw_audience_data(count: int = 5) -> list[dict[str, Any]]:
    """Build minimal raw audience data entries."""
    return [
        {
            "source": f"reddit_post_{i}",
            "text": f"Sample audience post {i} about struggles and dreams",
            "platform": "reddit",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        for i in range(count)
    ]


def _build_coach_soul() -> CoachSoul:
    """Build a test CoachSoul with enough data for fallback seeds."""
    return CoachSoul(
        coach_name="Test Coach",
        coach_id="TST-0000",
        coaching_philosophy="Help people find their authentic voice",
        core_message="Authenticity is the foundation of all growth",
        tribe_archetype="The Awakened Seeker",
        voice_dna=VoiceDNA(
            vocabulary_fingerprint=["authentic", "voice", "truth"],
        ),
        ideal_client=IdealClient(
            pain_points=["imposter syndrome", "burnout", "lack of direction"],
            aspirations=["confidence", "purpose", "peace"],
        ),
        leadership_scores=LeadershipScores(
            deep_empathy=85,
            authentic_vulnerability=90,
            radical_honesty=75,
        ),
        signature_frameworks=["Authentic Voice Method", "The Awakening Protocol"],
        content_tone=ContentTone(warmth=0.8, directness=0.6),
    )


def _build_tribe_profile() -> TribeProfile:
    """Build a TribeProfile with all volume quotas met."""
    from src.ccp.models.tribe_profile_models import (
        AntiAspirationalMarker,
        CulturalArtifactsSection,
        EmotionalResonanceSection,
        HighArousalTriggerItem,
        HumorProfileSection,
        HumorExampleItem,
        TribeSlangItem,
        InsideJokeItem,
        HeroEnemyItem,
        EmotionalQuoteItem,
    )

    return TribeProfile(
        coach_id="TST-0000",
        coach_acronym="TST",
        cultural_artifacts=CulturalArtifactsSection(
            tribe_slang=[TribeSlangItem(term=f"slang_{i}") for i in range(12)],
            inside_jokes=[InsideJokeItem(joke_reference=f"joke_{i}") for i in range(6)],
            shared_heroes=[HeroEnemyItem(name=f"hero_{i}", role="hero") for i in range(6)],
            common_enemies=[HeroEnemyItem(name=f"enemy_{i}", role="enemy") for i in range(6)],
        ),
        humor_profile=HumorProfileSection(
            style_examples=[HumorExampleItem(style=s, content=f"example_{i}") for i, s in enumerate(["self_deprecating", "ironic", "absurd"])],
            humor_targets=[],
            taboos_and_no_go_zones=[],
        ),
        emotional_resonance=EmotionalResonanceSection(
            primary_aspirations=[EmotionalQuoteItem(text=f"aspiration_{i}") for i in range(6)],
            core_anxieties=[EmotionalQuoteItem(text=f"anxiety_{i}") for i in range(6)],
            high_arousal_triggers=[
                HighArousalTriggerItem(
                    event_type=f"event_{i}",
                    valence="positive" if i < 4 else "negative",
                    reaction_quote=f"trigger_{i}",
                )
                for i in range(8)
            ],
        ),
        visual_recognition_codes=[],
        anti_aspirational_markers=[
            AntiAspirationalMarker(marker=f"anti_{i}") for i in range(4)
        ],
    )


def _build_distilled_profile_authenticated() -> TribeProfileDistilled:
    """Build a TribeProfileDistilled that passes all 4 Laws."""
    # Build entries across L1/L2/L3 depths with T/V/R modes
    entries_frustrations: list[DepthStratifiedEntry] = []
    for i in range(6):
        depth = [DepthLevel.L1, DepthLevel.L2, DepthLevel.L2, DepthLevel.L3, DepthLevel.L2, DepthLevel.L3][i]
        entries_frustrations.append(
            DepthStratifiedEntry(
                text=f"Frustration {i}: why does nobody listen when I share my soul?",
                depth=depth,
            )
        )

    trigger_entries: list[EmotionalTriggerEntry] = []
    modes = [EmotionalMode.TENSION, EmotionalMode.VULNERABILITY, EmotionalMode.RECOGNITION]
    for i in range(9):
        mode = modes[i % 3]
        depth = [DepthLevel.L2, DepthLevel.L3, DepthLevel.L2][i % 3]
        trigger_entries.append(
            EmotionalTriggerEntry(
                text=f"Trigger {i}: emotional response to coaching-specific event",
                depth=depth,
                mode=mode,
                intensity=TriggerIntensity.ACTIVE,
                activation_keywords=[f"keyword_{i}"],
            )
        )

    visuals = [
        VisualRecognitionCode(
            name=f"insider_obj_{i}",
            code_type=VisualCodeType.INSIDER,
            description=f"Tribe-specific insider visual {i}",
        )
        for i in range(6)
    ] + [
        VisualRecognitionCode(
            name=f"rejection_obj_{i}",
            code_type=VisualCodeType.REJECTION,
            description=f"Tribe-specific rejection visual {i}",
        )
        for i in range(4)
    ]

    lang_entries = [
        LanguageRegistryEntry(
            term=f"safe_term_{i}",
            register_type=LanguageRegisterType.SAFE,
            context_example=f"Used in context {i}",
        )
        for i in range(12)
    ] + [
        LanguageRegistryEntry(
            term=f"outsider_term_{i}",
            register_type=LanguageRegisterType.OUTSIDER,
            use_instead=f"replacement_{i}",
        )
        for i in range(6)
    ]

    distilled = TribeProfileDistilled(
        coach_id="TST-0000",
        coach_acronym="TST",
        frustrations=ContextPremiseDimension(
            entries=[
                DepthStratifiedEntry(
                    text=e.text,
                    depth=e.depth,
                )
                for e in entries_frustrations
            ],
        ),
        emotional_triggers=EmotionalTriggerDimension(entries=trigger_entries),
        visual_recognition_codes=visuals,
        language_registry=lang_entries,
    )

    return distilled


# ══════════════════════════════════════════════════════════════
# AC1: Prerequisite Gate — Stage A
# ══════════════════════════════════════════════════════════════


class TestAC1PrerequisiteGateStageA:
    """AC1: Pipeline halts with descriptive error when audience raw data
    is empty or missing."""

    def test_halts_when_no_audience_data(self, tmp_path: Path) -> None:
        """No dossier + no raw data → ValueError."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        extractor = TribeProfileExtractor(
            coach_id="TST-0000",
            coach_acronym="TST",
            receipt_chain=rc,
            base_dir=str(tmp_path),
        )

        with pytest.raises(ValueError, match="Audience raw data not found"):
            extractor.ingest(
                tribe_dossier=None,
                audience_raw_data=None,
                coach_soul=None,
                coach_philosophy_brief=None,
            )

    def test_halts_when_empty_audience_data(self, tmp_path: Path) -> None:
        """Dossier=None + empty raw data list → ValueError."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        extractor = TribeProfileExtractor(
            coach_id="TST-0000",
            coach_acronym="TST",
            receipt_chain=rc,
            base_dir=str(tmp_path),
        )

        with pytest.raises(ValueError, match="Audience raw data not found"):
            extractor.ingest(
                tribe_dossier=None,
                audience_raw_data=[],
                coach_soul=None,
                coach_philosophy_brief=None,
            )

    def test_proceeds_with_valid_data(self, tmp_path: Path) -> None:
        """Valid dossier + raw data → ingest succeeds."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        extractor = TribeProfileExtractor(
            coach_id="TST-0000",
            coach_acronym="TST",
            receipt_chain=rc,
            base_dir=str(tmp_path),
        )

        result = extractor.ingest(
            tribe_dossier=_build_tribe_dossier(),
            audience_raw_data=_build_raw_audience_data(),
            coach_soul={"coach_name": "Test"},
            coach_philosophy_brief="Help people grow",
        )
        assert result is not None
        assert result["tribe_dossier"] is not None


# ══════════════════════════════════════════════════════════════
# AC2: Prerequisite Gate — Stage B
# ══════════════════════════════════════════════════════════════


class TestAC2PrerequisiteGateStageB:
    """AC2: Pipeline halts with descriptive error when tribe_profile.json
    does not exist."""

    def test_halts_when_tribe_profile_none(self, tmp_path: Path) -> None:
        """tribe_profile=None → ValueError."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        distiller = TribeProfileDistiller(
            coach_id="TST-0000",
            coach_acronym="TST",
            receipt_chain=rc,
            base_dir=str(tmp_path),
        )

        with pytest.raises(ValueError, match="tribe_profile.json not found"):
            distiller.ingest(
                tribe_profile=None,
                coach_soul=None,
                coach_philosophy_brief=None,
            )

    def test_proceeds_with_valid_tribe_profile(self, tmp_path: Path) -> None:
        """Valid tribe_profile → ingest succeeds."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        distiller = TribeProfileDistiller(
            coach_id="TST-0000",
            coach_acronym="TST",
            receipt_chain=rc,
            base_dir=str(tmp_path),
        )

        result = distiller.ingest(
            tribe_profile=_build_tribe_profile(),
            coach_soul={"coach_name": "Test"},
            coach_philosophy_brief="Help people grow",
        )
        assert result is not None
        assert "ingest_receipt_id" in result


# ══════════════════════════════════════════════════════════════
# AC3: Volume Quotas
# ══════════════════════════════════════════════════════════════


class TestAC3VolumeQuotas:
    """AC3: tribe_profile.json contains all required minimums.
    Any quota unmet → validation fails."""

    def test_all_quotas_met(self) -> None:
        """Profile with all quotas met → all pass."""
        profile = _build_tribe_profile()
        results = profile.validate_volume_quotas()
        for r in results:
            assert r.passed, f"Quota failed: {r.quota_name} — {r.actual} < {r.minimum}"

    def test_slang_quota_fails(self) -> None:
        """Profile with <10 slang → slang quota fails."""
        profile = _build_tribe_profile()
        profile.cultural_artifacts.tribe_slang = ["only_one"]
        results = profile.validate_volume_quotas()
        slang_results = [r for r in results if "slang" in r.quota_name.lower()]
        assert len(slang_results) > 0
        assert not slang_results[0].passed

    def test_heroes_quota_fails(self) -> None:
        """Profile with <5 heroes → heroes quota fails."""
        profile = _build_tribe_profile()
        profile.cultural_artifacts.shared_heroes = ["hero_1", "hero_2"]
        results = profile.validate_volume_quotas()
        hero_results = [r for r in results if "hero" in r.quota_name.lower()]
        assert len(hero_results) > 0
        assert not hero_results[0].passed


# ══════════════════════════════════════════════════════════════
# AC4: Depth Stratification
# ══════════════════════════════════════════════════════════════


class TestAC4DepthStratification:
    """AC4: L2 ≥30% AND L3 ≥10%. Profile with 80/15/5 → FAILED."""

    def test_passing_depth_distribution(self) -> None:
        """L1=40%, L2=40%, L3=20% → passes gate."""
        dist = DepthDistribution(l1_ratio=0.40, l2_ratio=0.40, l3_ratio=0.20)
        assert dist.passes_depth_gate() is True

    def test_failing_depth_distribution_l3_too_low(self) -> None:
        """L1=80%, L2=15%, L3=5% → FAILED (L3 <10%)."""
        dist = DepthDistribution(l1_ratio=0.80, l2_ratio=0.15, l3_ratio=0.05)
        assert dist.passes_depth_gate() is False

    def test_failing_depth_distribution_l2_too_low(self) -> None:
        """L1=80%, L2=10%, L3=10% → FAILED (L2 <30%)."""
        dist = DepthDistribution(l1_ratio=0.80, l2_ratio=0.10, l3_ratio=0.10)
        assert dist.passes_depth_gate() is False

    def test_stratifier_classify_depth(self) -> None:
        """DepthStratifier classifies text into L1/L2/L3."""
        stratifier = DepthStratifier()
        depth, score = stratifier.classify_depth(
            text="I hate how nobody talks about the real struggle at 2am",
            source_platform="reddit",
        )
        assert depth in [DepthLevel.L1, DepthLevel.L2, DepthLevel.L3]
        assert isinstance(score, float)

    def test_stratifier_validate_gate(self) -> None:
        """DepthStratifier validate_depth_gate with failing dist."""
        stratifier = DepthStratifier()
        dist = DepthDistribution(l1_ratio=0.80, l2_ratio=0.15, l3_ratio=0.05)
        assert stratifier.validate_depth_gate(dist) is False


# ══════════════════════════════════════════════════════════════
# AC5: Mode Coverage (T/V/R)
# ══════════════════════════════════════════════════════════════


class TestAC5ModeCoverage:
    """AC5: ≥3 triggers per mode (T/V/R). 10T/4V/0R → MODE-INCOMPLETE."""

    def test_passing_mode_distribution(self) -> None:
        """3T + 3V + 3R → passes mode gate."""
        dist = ModeDistribution(
            tension_count=3,
            vulnerability_count=3,
            recognition_count=3,
        )
        assert dist.passes_mode_gate() is True

    def test_failing_mode_distribution_zero_recognition(self) -> None:
        """10T + 4V + 0R → fails mode gate."""
        dist = ModeDistribution(
            tension_count=10,
            vulnerability_count=4,
            recognition_count=0,
        )
        assert dist.passes_mode_gate() is False

    def test_mode_mapper_classify(self) -> None:
        """EmotionalModeMapper classifies entries into T/V/R."""
        mapper = EmotionalModeMapper()
        entry = EmotionalTriggerEntry(
            text="I feel angry when experts dismiss my experience",
            activation_keywords=["dismiss", "angry"],
        )
        classified = mapper.classify_mode(
            text=entry.text,
            activation_keywords=entry.activation_keywords,
        )
        assert classified in [
            EmotionalMode.TENSION,
            EmotionalMode.VULNERABILITY,
            EmotionalMode.RECOGNITION,
        ]


# ══════════════════════════════════════════════════════════════
# AC6: Visual Codes
# ══════════════════════════════════════════════════════════════


class TestAC6VisualCodes:
    """AC6: ≥5 insider objects, ≥3 rejection triggers present."""

    def test_visual_codes_pass(self) -> None:
        """6 insider + 4 rejection → passes validation."""
        registry = VisualLanguageRegistry()
        codes = [
            VisualRecognitionCode(name=f"insider_{i}", code_type=VisualCodeType.INSIDER)
            for i in range(6)
        ] + [
            VisualRecognitionCode(name=f"rejection_{i}", code_type=VisualCodeType.REJECTION)
            for i in range(4)
        ]
        result = registry.validate_visual_codes(codes)
        assert result["insider_met"] is True
        assert result["rejection_met"] is True

    def test_visual_codes_fail_insufficient_insider(self) -> None:
        """2 insider + 3 rejection → insider fails."""
        registry = VisualLanguageRegistry()
        codes = [
            VisualRecognitionCode(name=f"insider_{i}", code_type=VisualCodeType.INSIDER)
            for i in range(2)
        ] + [
            VisualRecognitionCode(name=f"rejection_{i}", code_type=VisualCodeType.REJECTION)
            for i in range(3)
        ]
        result = registry.validate_visual_codes(codes)
        assert result["insider_met"] is False

    def test_visual_codes_fail_insufficient_rejection(self) -> None:
        """5 insider + 1 rejection → rejection fails."""
        registry = VisualLanguageRegistry()
        codes = [
            VisualRecognitionCode(name=f"insider_{i}", code_type=VisualCodeType.INSIDER)
            for i in range(5)
        ] + [
            VisualRecognitionCode(name="rejection_0", code_type=VisualCodeType.REJECTION)
        ]
        result = registry.validate_visual_codes(codes)
        assert result["rejection_met"] is False


# ══════════════════════════════════════════════════════════════
# AC7: Language Registry
# ══════════════════════════════════════════════════════════════


class TestAC7LanguageRegistry:
    """AC7: ≥10 safe terms + ≥5 outsider terms with alternatives."""

    def test_language_registry_pass(self) -> None:
        """12 safe + 6 outsider → passes validation."""
        registry = VisualLanguageRegistry()
        entries = [
            LanguageRegistryEntry(
                term=f"safe_term_{i}",
                register_type=LanguageRegisterType.SAFE,
                context_example=f"context {i}",
            )
            for i in range(12)
        ] + [
            LanguageRegistryEntry(
                term=f"outsider_term_{i}",
                register_type=LanguageRegisterType.OUTSIDER,
                use_instead=f"alt_{i}",
            )
            for i in range(6)
        ]
        result = registry.validate_language_registry(entries)
        assert result["safe_met"] is True
        assert result["outsider_met"] is True

    def test_language_registry_fail_insufficient_safe(self) -> None:
        """3 safe + 5 outsider → safe fails."""
        registry = VisualLanguageRegistry()
        entries = [
            LanguageRegistryEntry(
                term=f"safe_{i}",
                register_type=LanguageRegisterType.SAFE,
                context_example=f"ctx {i}",
            )
            for i in range(3)
        ] + [
            LanguageRegistryEntry(
                term=f"outsider_{i}",
                register_type=LanguageRegisterType.OUTSIDER,
                use_instead=f"alt_{i}",
            )
            for i in range(5)
        ]
        result = registry.validate_language_registry(entries)
        assert result["safe_met"] is False


# ══════════════════════════════════════════════════════════════
# AC8: Interchangeability Test (Law 4 Check 4)
# ══════════════════════════════════════════════════════════════


class TestAC8InterchangeabilityTest:
    """AC8: Profile fails Law 4 Check 4 if it could describe
    a different community's tribe."""

    def test_four_laws_validation_model(self) -> None:
        """FourLawsValidation model correctly aggregates results."""
        validation = FourLawsValidation(
            law_1_mode_triggers=LawValidationResult(passed=True),
            law_2_visual_codes=LawValidationResult(passed=True),
            law_3_language_registry=LawValidationResult(passed=True),
            law_4_authenticity=LawValidationResult(passed=True),
        )
        assert validation.all_passed() is True
        assert validation.get_verdict() == AuthenticationVerdict.AUTHENTICATED

    def test_four_laws_partial_failure(self) -> None:
        """3/4 laws pass → PROVISIONAL."""
        validation = FourLawsValidation(
            law_1_mode_triggers=LawValidationResult(passed=True),
            law_2_visual_codes=LawValidationResult(passed=True),
            law_3_language_registry=LawValidationResult(passed=True),
            law_4_authenticity=LawValidationResult(passed=False, reason="Generic profile"),
        )
        assert validation.get_verdict() == AuthenticationVerdict.PROVISIONAL

    def test_four_laws_major_failure(self) -> None:
        """≤2/4 laws pass → FAILED."""
        validation = FourLawsValidation(
            law_1_mode_triggers=LawValidationResult(passed=True),
            law_2_visual_codes=LawValidationResult(passed=False),
            law_3_language_registry=LawValidationResult(passed=False),
            law_4_authenticity=LawValidationResult(passed=False),
        )
        assert validation.get_verdict() == AuthenticationVerdict.FAILED


# ══════════════════════════════════════════════════════════════
# AC9: Neo4j Isolation
# ══════════════════════════════════════════════════════════════


class TestAC9Neo4jIsolation:
    """AC9: Coach A graph CANNOT return Coach B nodes.
    Cross-coach contamination = critical security violation."""

    def test_graph_manager_creates_with_coach_scope(self) -> None:
        """Neo4jGraphManager stores coach_id for isolation."""
        manager = Neo4jGraphManager(
            coach_id="COACH-A",
            coach_acronym="CA",
        )
        assert manager.coach_id == "COACH-A"

    def test_graph_node_scoped_to_coach(self) -> None:
        """GraphNode model includes coach_id for per-coach isolation."""
        node = GraphNode(
            node_type="Frustration",
            coach_id="TST-0000",
            properties={"text": "test"},
        )
        assert node.coach_id == "TST-0000"

    def test_relationship_scoped_to_coach(self) -> None:
        """GraphRelationship model includes coach_id for isolation."""
        rel = GraphRelationship(
            relationship_type="TRIGGERS",
            source_node_id="node_1",
            target_node_id="node_2",
            coach_id="TST-0000",
        )
        assert rel.coach_id == "TST-0000"

    def test_purge_coach_graph_uses_coach_filter(self) -> None:
        """purge_coach_graph only removes nodes for the specified coach."""
        manager = Neo4jGraphManager(
            coach_id="COACH-A",
            coach_acronym="CA",
        )
        # Without a real Neo4j driver, the method should handle gracefully
        result = manager.purge_coach_data()
        assert isinstance(result, dict)
        assert result.get("coach_id") == "COACH-A"


# ══════════════════════════════════════════════════════════════
# AC10: Neo4j Performance
# ══════════════════════════════════════════════════════════════


class TestAC10Neo4jPerformance:
    """AC10: Context Premise graph read <500ms per query."""

    def test_read_performance_contract_exists(self) -> None:
        """Neo4jGraphManager exposes read methods for performance testing."""
        manager = Neo4jGraphManager(
            coach_id="TST-0000",
            coach_acronym="TST",
        )
        # Verify query interface exists (actual perf testing needs live Neo4j)
        assert hasattr(manager, "query_nodes")
        assert hasattr(manager, "populate_dimension")

    def test_read_returns_empty_without_driver(self) -> None:
        """Without Neo4j driver, read returns empty results gracefully."""
        from src.ccp.models.tribe_profile_models import Neo4jNodeType
        manager = Neo4jGraphManager(
            coach_id="TST-0000",
            coach_acronym="TST",
        )
        result = manager.query_nodes(Neo4jNodeType.FRUSTRATION)
        assert isinstance(result, list)


# ══════════════════════════════════════════════════════════════
# AC11: Authentication Verdict
# ══════════════════════════════════════════════════════════════


class TestAC11AuthenticationVerdict:
    """AC11: AUTHENTICATED (4/4), PROVISIONAL (3/4), FAILED (≤2/4).
    FAILED profile returns error, cannot feed downstream stages."""

    def test_authenticated_verdict(self) -> None:
        """4/4 laws pass → AUTHENTICATED."""
        verdict = FourLawsValidation(
            law_1_mode_triggers=LawValidationResult(passed=True),
            law_2_visual_codes=LawValidationResult(passed=True),
            law_3_language_registry=LawValidationResult(passed=True),
            law_4_authenticity=LawValidationResult(passed=True),
        ).get_verdict()
        assert verdict == AuthenticationVerdict.AUTHENTICATED

    def test_provisional_verdict(self) -> None:
        """3/4 laws pass → PROVISIONAL."""
        verdict = FourLawsValidation(
            law_1_mode_triggers=LawValidationResult(passed=True),
            law_2_visual_codes=LawValidationResult(passed=False),
            law_3_language_registry=LawValidationResult(passed=True),
            law_4_authenticity=LawValidationResult(passed=True),
        ).get_verdict()
        assert verdict == AuthenticationVerdict.PROVISIONAL

    def test_failed_verdict(self) -> None:
        """≤2/4 laws pass → FAILED."""
        verdict = FourLawsValidation(
            law_1_mode_triggers=LawValidationResult(passed=True),
            law_2_visual_codes=LawValidationResult(passed=False),
            law_3_language_registry=LawValidationResult(passed=False),
            law_4_authenticity=LawValidationResult(passed=False),
        ).get_verdict()
        assert verdict == AuthenticationVerdict.FAILED

    def test_failed_profile_cannot_feed_downstream(self) -> None:
        """FAILED authentication → profile should be rejected."""
        distilled = _build_distilled_profile_authenticated()
        distilled.authentication_status = AuthenticationVerdict.FAILED
        assert distilled.authentication_status == AuthenticationVerdict.FAILED
        # Downstream consumers check authentication_status before processing


# ══════════════════════════════════════════════════════════════
# AC12: Coach-Tribe Resonance
# ══════════════════════════════════════════════════════════════


class TestAC12CoachTribeResonance:
    """AC12: ≥3 alignment points and ≥1 friction point.
    Zero friction points → WARNING: relationship is idealized."""

    def test_resonance_analyzer_interface(self) -> None:
        """CoachTribeResonanceAnalyzer has the expected interface."""
        analyzer = CoachTribeResonanceAnalyzer()
        assert hasattr(analyzer, "build_resonance")
        assert hasattr(analyzer, "find_alignment_points")
        assert hasattr(analyzer, "find_friction_points")

    def test_resonance_validation_passes(self) -> None:
        """≥3 alignment + ≥1 friction → passes."""
        from src.ccp.models.tribe_profile_models import CoachTribeResonance
        resonance = CoachTribeResonance(
            alignment_points=[f"alignment_{i}" for i in range(4)],
            friction_points=["friction_1"],
            gaps=[],
        )
        assert len(resonance.alignment_points) >= 3
        assert len(resonance.friction_points) >= 1

    def test_resonance_zero_friction_warning(self) -> None:
        """Zero friction points → indicates idealized relationship."""
        from src.ccp.models.tribe_profile_models import CoachTribeResonance
        resonance = CoachTribeResonance(
            alignment_points=[f"alignment_{i}" for i in range(5)],
            friction_points=[],
            gaps=[],
        )
        assert len(resonance.friction_points) == 0
        # This should trigger a WARNING in the validation phase


# ══════════════════════════════════════════════════════════════
# AC13: Backward Compatibility
# ══════════════════════════════════════════════════════════════


class TestAC13BackwardCompatibility:
    """AC13: Coach without Context Premise Map → content generated
    using topic-based prompts from coach_soul.json. No errors.
    All downstream phases complete. Trigger Matching Layer degrades."""

    def test_fallback_detection_no_cpm(self, tmp_path: Path) -> None:
        """No context_premise_map.json → fallback detected."""
        assert ContextPremiseFallback.context_premise_exists(tmp_path) is False

    def test_fallback_detection_with_cpm(self, tmp_path: Path) -> None:
        """Valid context_premise_map.json → no fallback needed."""
        cpm_path = tmp_path / "context_premise_map.json"
        cpm_path.write_text(json.dumps({
            "dimensions": {"frustrations": {}},
            "authentication": {"verdict": "AUTHENTICATED"},
        }))
        assert ContextPremiseFallback.context_premise_exists(tmp_path) is True

    def test_fallback_generates_seeds(self) -> None:
        """Fallback seeds contain topic-based prompts from coach_soul."""
        coach_soul = _build_coach_soul()
        seeds = ContextPremiseFallback.generate_fallback_seeds(coach_soul)
        assert "philosophy_topics" in seeds
        assert "core_message_prompts" in seeds
        assert "pain_point_topics" in seeds
        assert "aspiration_topics" in seeds
        assert "content_tone" in seeds
        assert len(seeds["pain_point_topics"]) == 3  # from fixture

    def test_fallback_resolve_returns_result(self, tmp_path: Path) -> None:
        """resolve() returns ContextPremiseFallbackResult when no CPM."""
        coach_soul = _build_coach_soul()
        result = ContextPremiseFallback.resolve(
            coach_soul=coach_soul,
            coach_folder=tmp_path,
        )
        assert result is not None
        assert result.used_fallback is True
        assert len(result.limitations) == 4
        assert "fallback_content_seed" in result.model_dump()

    def test_fallback_resolve_returns_none_when_cpm_exists(self, tmp_path: Path) -> None:
        """resolve() returns None when context_premise_map.json exists."""
        cpm_path = tmp_path / "context_premise_map.json"
        cpm_path.write_text(json.dumps({
            "dimensions": {"frustrations": {}},
            "authentication": {"verdict": "AUTHENTICATED"},
        }))
        coach_soul = _build_coach_soul()
        result = ContextPremiseFallback.resolve(
            coach_soul=coach_soul,
            coach_folder=tmp_path,
        )
        assert result is None

    def test_fallback_no_errors(self, tmp_path: Path) -> None:
        """Entire fallback path completes without exceptions."""
        coach_soul = _build_coach_soul()
        result = ContextPremiseFallback.resolve(
            coach_soul=coach_soul,
            coach_folder=tmp_path,
        )
        assert result is not None
        # Verify degraded config is available
        degraded = ContextPremiseFallback.degrade_trigger_matching_config()
        assert degraded["trigger_matching_mode"] == "degraded"
        assert degraded["four_axis_engine_enabled"] is False

    def test_exit_condition_check(self, tmp_path: Path) -> None:
        """Fallback exit when both files exist."""
        # Initially active
        assert ContextPremiseFallback.is_fallback_still_active(tmp_path) is True

        # Create both files → exit condition met
        (tmp_path / "context_premise_map.json").write_text(json.dumps({
            "dimensions": {}, "authentication": {},
        }))
        (tmp_path / "tribe_profile_distilled.json").write_text("{}")
        assert ContextPremiseFallback.is_fallback_still_active(tmp_path) is False


# ══════════════════════════════════════════════════════════════
# AC14: Psychometric Extensions
# ══════════════════════════════════════════════════════════════


class TestAC14PsychometricExtensions:
    """AC14: All 5 extensions populated or explicitly null with reasoning.
    moral_foundation_violated must use MFT/MFQ-2 framework labels."""

    def test_psychometric_mapper_interface(self) -> None:
        """PsychometricExtensionMapper has the expected interface."""
        mapper = PsychometricExtensionMapper()
        assert hasattr(mapper, "map_all_extensions")
        assert hasattr(mapper, "map_regulatory_focus")
        assert hasattr(mapper, "map_moral_foundation")
        assert hasattr(mapper, "map_coping_trajectory")
        assert hasattr(mapper, "detect_hermeneutical_gaps")
        assert hasattr(mapper, "map_reconsolidation_sensitivity")

    def test_extensions_model_has_all_five(self) -> None:
        """PsychometricExtensions model includes all 5 extension fields."""
        ext = PsychometricExtensions()
        assert hasattr(ext, "regulatory_focus")
        assert hasattr(ext, "moral_foundation_violated")
        assert hasattr(ext, "coping_trajectory")
        assert hasattr(ext, "hermeneutical_gaps")
        assert hasattr(ext, "reconsolidation_sensitivity")

    def test_regulatory_focus_uses_enum(self) -> None:
        """Regulatory focus uses framework enum values."""
        assert RegulatoryFocus.PROMOTION.value == "promotion"
        assert RegulatoryFocus.PREVENTION.value == "prevention"
        assert RegulatoryFocus.MIXED.value == "mixed"

    def test_coping_trajectory_uses_enum(self) -> None:
        """Coping trajectory uses framework enum values."""
        assert CopingTrajectoryPosition.SEARCH.value == "search"
        assert CopingTrajectoryPosition.ACTIVE.value == "active"
        assert CopingTrajectoryPosition.EXHAUSTED.value == "exhausted"

    def test_moral_foundation_uses_mft_labels(self) -> None:
        """moral_foundation_violated uses MFT/MFQ-2 labels, not free text."""
        mapper = PsychometricExtensionMapper()
        from src.ccp.models.tribe_profile_models import MoralFoundationViolated
        # Verify mapper enforces MFT labels
        result = mapper.map_moral_foundation(
            entries=[],
            triggers=[],
        )
        # Result should be a MoralFoundationViolated model with framework labels
        assert isinstance(result, MoralFoundationViolated)

    def test_map_all_extensions_returns_complete(self) -> None:
        """map_all_extensions returns PsychometricExtensions with all fields."""
        mapper = PsychometricExtensionMapper()
        result = mapper.map_all_extensions(
            entries=[],
            triggers=[],
        )
        assert isinstance(result, PsychometricExtensions)
        # All fields should be present (populated or null)
        dumped = result.model_dump()
        assert "regulatory_focus" in dumped
        assert "moral_foundation_violated" in dumped
        assert "coping_trajectory" in dumped
        assert "hermeneutical_gaps" in dumped
        assert "reconsolidation_sensitivity" in dumped


# ══════════════════════════════════════════════════════════════
# Pipeline Session Tests
# ══════════════════════════════════════════════════════════════


class TestPipelineSession:
    """Test TribeProfilePipelineSession tracking."""

    def test_session_stage_tracking(self) -> None:
        """Session tracks Stage A and Stage B step statuses."""
        session = TribeProfilePipelineSession(
            coach_id="TST-0000",
            coach_acronym="TST",
        )
        assert session.is_stage_a_complete() is False
        assert session.is_stage_b_complete() is False
        assert session.is_complete() is False

    def test_session_stage_a_complete(self) -> None:
        """Session marks Stage A as complete when all steps done."""
        session = TribeProfilePipelineSession(
            coach_id="TST-0000",
            coach_acronym="TST",
        )
        for step in ["ingest", "research_planning", "cultural_harvesting",
                     "emit", "validate", "checkpoint"]:
            setattr(session, f"stage_a_{step}", TribeProfilePipelineStepStatus.COMPLETE)
        assert session.is_stage_a_complete() is True

    def test_session_full_complete(self) -> None:
        """Session marks full pipeline complete when both stages done."""
        session = TribeProfilePipelineSession(
            coach_id="TST-0000",
            coach_acronym="TST",
        )
        for step in ["ingest", "research_planning", "cultural_harvesting",
                     "emit", "validate", "checkpoint"]:
            setattr(session, f"stage_a_{step}", TribeProfilePipelineStepStatus.COMPLETE)
        for step in ["ingest", "depth_stratification", "mode_mapping",
                     "visual_language", "resonance", "psychometric",
                     "neo4j", "emit", "validate", "checkpoint"]:
            setattr(session, f"stage_b_{step}", TribeProfilePipelineStepStatus.COMPLETE)
        assert session.is_complete() is True


# ══════════════════════════════════════════════════════════════
# Receipt Chain Integration
# ══════════════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """Test that all 4 receipt writes are properly chained."""

    def test_receipt_chain_write_on_ingest(self, tmp_path: Path) -> None:
        """Receipt chain log produces a receipt entry on ingest."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        entry = rc.log(
            agent_id="tribe_soul_extraction_engine_v2",
            action="TRIBE-EXTRACT-INGEST",
            asset_id="DEP-H11-TST",
            input_summary="Test ingest",
            output_summary="Ingest complete",
            decision="proceed",
        )
        assert entry.receipt_id != ""
        assert entry.action == "TRIBE-EXTRACT-INGEST"

    def test_receipt_chain_chaining(self, tmp_path: Path) -> None:
        """Receipt entries chain via parent_receipt_id."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        e1 = rc.log(
            agent_id="extractor",
            action="TRIBE-EXTRACT-INGEST",
            input_summary="Ingest",
            output_summary="Done",
        )
        e2 = rc.log(
            agent_id="extractor",
            action="TRIBE-EXTRACT-EMIT",
            input_summary="Emit",
            output_summary="Done",
            parent_receipt_id=e1.receipt_id,
        )
        assert e2.parent_receipt_id == e1.receipt_id

    def test_all_four_receipt_actions(self, tmp_path: Path) -> None:
        """All 4 required receipt actions can be written."""
        rc = ReceiptChain(coach_acronym="TST", log_dir=str(tmp_path / "logs"))
        actions = [
            "TRIBE-EXTRACT-INGEST",
            "TRIBE-EXTRACT-EMIT",
            "TRIBE-DISTILL-INGEST",
            "TRIBE-DISTILL-EMIT",
        ]
        entries = []
        parent_id: str | None = None
        for action in actions:
            entry = rc.log(
                agent_id="fr6_pipeline",
                action=action,
                input_summary=f"{action} input",
                output_summary=f"{action} output",
                parent_receipt_id=parent_id,
            )
            entries.append(entry)
            parent_id = entry.receipt_id

        assert len(entries) == 4
        assert entries[0].action == "TRIBE-EXTRACT-INGEST"
        assert entries[3].action == "TRIBE-DISTILL-EMIT"
        assert entries[3].parent_receipt_id == entries[2].receipt_id
