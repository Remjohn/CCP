"""
CCP Step 5 — Voice DNA Adapter Integration Tests (Unit 7)
Tests all 4 Step-5 adapters and the pipeline orchestrator.

Spec coverage:
    Gate PC-03 (≥15 contrastive strings) — negative_space_loader_adapter
    Mandate 4 enforcement — coach_soul_adapter cannot run without Adapter-2 success
    C-08 rhythm whitelist — all RhythmInstruction.bypass_c08 = True
    ADR-01 coach_id isolation — all adapters scope by coach_id
    Pipeline load order — negative space FIRST, coach soul SECOND
    TTT runtime context injection — DEP-ENG-005 factual report (M-02 compliant)
    PTG safety gate — raw_unresolved HARD EXCLUDED from IREVC trigger pre-load
    Minimum viable map advisory warning — non-blocking
    V1-V5 appraisal constraint generation
    Moral foundation activation thresholds
    Routing brief injection (DEP-ENG-016)
"""

from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import (
    AdapterSlot,
    BlockTarget,
    RhythmInstruction,
)
from src.ccp.models.emotional_dna_models import (
    AgencyAttributionType,
    AppraisalSequenceType,
    AppraisalVariables,
    CSIPv3Extensions,
    EmotionalDNAProfile,
    ExtractionStatus,
    MoralFoundationWeight,
    MoralFoundations,
    V1TriggerSpecificityThreshold,
    V2AppraisalSequenceOrdering,
    V3CopingPotentialPattern,
    V4NormCompatibilityThreshold,
    V5AgencyAttributionBias,
)
from src.ccp.models.psych_routing_models import (
    ArousalDirection,
    AudienceMaturityCohort,
    AudienceMaturityProfile,
    ComparisonType,
    MoodStatePrimary,
    PsychologicalClassification,
    PsychRoutingBrief,
    RegulatoryFrame,
    SDTNeedPrimary,
    SemanticAffinityRisk,
    SequencingDependency,
    TMTFunction,
    ValenceDelivery,
)
from src.ccp.models.ttt_models import (
    TextureQuality,
    ToneRegister,
    TTTBaselineData,
)
from src.ccp.models.trigger_map_models import (
    AKBLevel,
    ArchetypeMapping,
    OriginClassification,
    PTGAssessment,
    PTGStatus,
    ReconsolidationSensitivity,
    TriggerEntry,
    TriggerMap,
)
from src.ccp.models.voice_dna_models import (
    ClusterProseDescription,
    HumorStyleClassification,
    HumorType,
    LexicalBlacklist,
    NegativeSpaceObject,
    PositiveSpaceObject,
    StylometryProfile,
    StructuralExclusions,
)
from src.ccp.services.coach_soul_adapter import (
    CoachSoulAdapter,
    IncompletePositiveSpaceError,
    Mandate4GateError,
)
from src.ccp.services.irevc_adapter import IREVCAdapter
from src.ccp.services.negative_space_loader_adapter import (
    NegativeSpaceDepthGateError,
    NegativeSpaceLoaderAdapter,
)
from src.ccp.services.psych_routing_adapter import PsychRoutingAdapter
from src.ccp.pipelines.voice_dna_adapter_pipeline import (
    VoiceDNAAdapterPipeline,
    VoiceDNAPipelineInput,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture()
def receipt_chain(tmp_path: Path) -> ReceiptChain:
    return ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "receipts"),
    )


COACH_ID = "coach-TST-001"


def _make_valid_negative_space(contrastive_count: int = 20) -> NegativeSpaceObject:
    """Build a NegativeSpaceObject with enough contrastive strings to pass PC-03."""
    # Each academic/spiritual/intensifier word counts as one contrastive string
    # Use contrastive_count to control total
    n_academic = min(contrastive_count, 10)
    n_spiritual = max(0, min(contrastive_count - n_academic, 10))
    n_intensifiers = max(0, contrastive_count - n_academic - n_spiritual)

    return NegativeSpaceObject(
        lexical_blacklist=LexicalBlacklist(
            academic=[f"academic_word_{i}" for i in range(n_academic)],
            spiritual=[f"spiritual_word_{i}" for i in range(n_spiritual)],
            banned_intensifiers=[f"intensifier_{i}" for i in range(n_intensifiers)],
        ),
        syntactic_impossibilities=[],
        structural_exclusions=StructuralExclusions(
            forbidden_openings=["Opens with a rhetorical question"],
            forbidden_closings=["Ends with a generic call to action"],
        ),
    )


def _make_positive_space_complete() -> PositiveSpaceObject:
    """Build a complete DEP-ENG-003 with 5 clusters all having prose descriptions."""
    clusters = [
        ClusterProseDescription(
            cluster_id=f"CLUSTER-{i}",
            cluster_name=f"Test Cluster {i}",
            prose_description=f"This coach uses pattern {i} — a distinct voice signature.",
        )
        for i in range(1, 6)
    ]
    return PositiveSpaceObject(
        clusters=clusters,
        stylometry_profile=StylometryProfile(
            average_sentence_length_words=14.5,
        ),
    )


def _make_positive_space_incomplete() -> PositiveSpaceObject:
    """Build an incomplete DEP-ENG-003 — 3 of 5 clusters missing prose."""
    clusters = [
        ClusterProseDescription(
            cluster_id=f"CLUSTER-{i}",
            cluster_name=f"Test Cluster {i}",
            prose_description=f"Prose for cluster {i}" if i <= 2 else "",
        )
        for i in range(1, 6)
    ]
    return PositiveSpaceObject(clusters=clusters)


def _make_emotional_dna(
    v1_score: int = 7,
    v2_type: AppraisalSequenceType = AppraisalSequenceType.MECHANISM_FIRST,
    v3_ratio: float = 0.8,
    v4_score: int = 5,
    v5_bias: AgencyAttributionType = AgencyAttributionType.INDIVIDUAL,
    care_harm_weight: float = 0.8,
) -> EmotionalDNAProfile:
    """Build a minimal EmotionalDNAProfile for testing adapter constraints."""
    return EmotionalDNAProfile(
        extraction_status=ExtractionStatus(confidence=0.9),
        appraisal_variables=AppraisalVariables(
            v1_trigger_specificity_threshold=V1TriggerSpecificityThreshold(
                score=v1_score
            ),
            v2_appraisal_sequence_ordering=V2AppraisalSequenceOrdering(
                type=v2_type
            ),
            v3_coping_potential_pattern=V3CopingPotentialPattern(
                ratio=v3_ratio
            ),
            v4_norm_compatibility_threshold=V4NormCompatibilityThreshold(
                score=v4_score
            ),
            v5_agency_attribution_bias=V5AgencyAttributionBias(
                dominant=v5_bias
            ),
        ),
        moral_foundations=MoralFoundations(
            v6_care_harm=MoralFoundationWeight(weight=care_harm_weight),
        ),
        csip_v3_extensions=CSIPv3Extensions(),
    )


def _make_routing_brief() -> PsychRoutingBrief:
    """Build a minimal PsychRoutingBrief (DEP-ENG-016) for testing."""
    return PsychRoutingBrief(
        routing_id="PRB-TEST-001",
        coach_id=COACH_ID,
        psychological_classification=PsychologicalClassification(
            mood_state_primary=MoodStatePrimary.PROCESSING,
            arousal_direction=ArousalDirection.LOWERS,
            valence_delivery=ValenceDelivery.EUDAIMONIC,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            sdt_need_primary=SDTNeedPrimary.RELATEDNESS,
            sequencing_dependency=SequencingDependency.INDEPENDENT,
            comparison_type=ComparisonType.NONE,
            tmt_function=TMTFunction.WORLDVIEW_CONSTRUCTION,
            semantic_affinity_risk=SemanticAffinityRisk.LOW,
        ),
        payload_masking_instruction=(
            "MASKING: Structure this content so its function as grief processing "
            "is not visible to the audience. Lead with a surface-level question."
        ),
    )


def _make_trigger_map(
    n_resolved: int = 3,
    n_raw_unresolved: int = 1,
) -> TriggerMap:
    """Build a TriggerMap with resolved and optionally raw_unresolved triggers."""
    triggers: list[TriggerEntry] = []

    for i in range(n_resolved):
        entry = TriggerEntry(
            trigger_id=f"TRG-{i:03d}",
            label=f"Test Trigger {i}",
            description="A test trigger for the test suite.",
            ptg_status=PTGAssessment(status=PTGStatus.RESOLVED_DUAL_LAYER),
            originating_experience=OriginClassification(
                akb_level=AKBLevel.GENERAL_EVENT
            ),
            reconsolidation_sensitivity=ReconsolidationSensitivity(score=5),
        )
        triggers.append(entry)

    # Raw unresolved — HARD EXCLUDED by PTG gate
    for i in range(n_raw_unresolved):
        entry = TriggerEntry(
            trigger_id=f"TRG-RAW-{i:03d}",
            label=f"Raw Unresolved Trigger {i}",
            ptg_status=PTGAssessment(status=PTGStatus.RAW_UNRESOLVED),
        )
        triggers.append(entry)

    tm = TriggerMap(coach_id=COACH_ID, triggers=triggers)
    tm.compute_status()
    return tm


def _make_ttt_baseline(authenticated: bool = True) -> TTTBaselineData:
    """Build a TTTBaselineData (DEP-ENG-005) for testing."""
    return TTTBaselineData(
        temperature=6,
        texture=TextureQuality.COLLOQUIAL,
        tone=ToneRegister.REFLECTIVE,
        liwc_authenticity_score=8.5 if authenticated else 5.0,
        session_id="SESSION-TST-001",
        coach_id=COACH_ID,
        extraction_timestamp="2026-03-19T10:00:00Z",
        voice_note_hash="abc123def456",
        liwc_authenticated=authenticated,
    )


# ─── Adapter-2: NegativeSpaceLoaderAdapter ───────────────────────────────────


class TestNegativeSpaceLoaderAdapter:
    """Gate PC-03 enforcement + Block A injection."""

    def test_gate_pc03_pass_with_sufficient_strings(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Gate PC-03: ≥15 contrastive strings → PASS and Block A injection succeeds."""
        neg_space = _make_valid_negative_space(contrastive_count=20)
        adapter = NegativeSpaceLoaderAdapter(receipt_chain)

        result = adapter.load(neg_space, COACH_ID)

        assert result.success is True
        assert result.adapter_slot == AdapterSlot.NEGATIVE_SPACE_LOADER
        assert result.block_a is not None
        assert result.block_a.target == BlockTarget.BLOCK_A
        assert len(result.block_a.structural_laws) > 0
        assert result.receipt_id != ""

    def test_gate_pc03_fail_below_threshold(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Gate PC-03: < 15 contrastive strings → NegativeSpaceDepthGateError raised.

        Spec §Stress Test Q1: 'mathematically less than 15 validated contrastive
        strings → L3_INSUFFICIENT_DEPTH halt'
        """
        neg_space = _make_valid_negative_space(contrastive_count=10)
        adapter = NegativeSpaceLoaderAdapter(receipt_chain)

        with pytest.raises(NegativeSpaceDepthGateError) as exc_info:
            adapter.load(neg_space, COACH_ID)

        assert exc_info.value.found == 10
        assert exc_info.value.required == 15

    def test_gate_pc03_exact_threshold_passes(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Gate PC-03: exactly 15 contrastive strings → PASS (≥15, not >15)."""
        neg_space = _make_valid_negative_space(contrastive_count=15)
        adapter = NegativeSpaceLoaderAdapter(receipt_chain)

        result = adapter.load(neg_space, COACH_ID)

        assert result.success is True
        assert result.block_a is not None
        assert result.block_a.metadata["total_contrastive_strings"] == 15
        assert result.block_a.metadata["gate_pc03"] == "PASS"

    def test_block_a_contains_lexical_prohibition_law(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Block A must contain at least one LEXICAL PROHIBITION law string."""
        neg_space = _make_valid_negative_space(contrastive_count=20)
        adapter = NegativeSpaceLoaderAdapter(receipt_chain)

        result = adapter.load(neg_space, COACH_ID)

        assert result.block_a is not None
        laws = result.block_a.structural_laws
        lexical_laws = [l for l in laws if "LEXICAL PROHIBITION" in l]
        assert len(lexical_laws) > 0

    def test_adr01_coach_id_in_output(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """ADR-01: coach_id must be present in result and block_a."""
        neg_space = _make_valid_negative_space(contrastive_count=20)
        adapter = NegativeSpaceLoaderAdapter(receipt_chain)

        result = adapter.load(neg_space, "coach-ADR-TEST-001")

        assert result.coach_id == "coach-ADR-TEST-001"
        assert result.block_a is not None
        assert result.block_a.coach_id == "coach-ADR-TEST-001"


# ─── Adapter-1: CoachSoulAdapter ─────────────────────────────────────────────


class TestCoachSoulAdapter:
    """Mandate 4 enforcement + Block A cluster prose injection."""

    def test_mandate4_gate_blocks_without_negative_space_complete(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Mandate 4: negative_space_complete=False → Mandate4GateError raised.

        Spec §Step 6 AC2: 'the pipeline halts with a DEP-ENG-004_NOT_FOUND error
        (not a prompt failure — a code-level gate)'
        """
        positive_space = _make_positive_space_complete()
        adapter = CoachSoulAdapter(receipt_chain)

        with pytest.raises(Mandate4GateError):
            adapter.load(positive_space, COACH_ID, negative_space_complete=False)

    def test_mandate4_gate_passes_with_flag_true(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Mandate 4: negative_space_complete=True → succeeds."""
        positive_space = _make_positive_space_complete()
        adapter = CoachSoulAdapter(receipt_chain)

        result = adapter.load(
            positive_space, COACH_ID, negative_space_complete=True
        )

        assert result.success is True
        assert result.block_a is not None
        assert result.block_a.metadata["mandate_4_gate"] == "PASSED"
    def test_incomplete_positive_space_raises_error(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """AC3: Not all 5 clusters populated → IncompletePositiveSpaceError."""
        positive_space = _make_positive_space_incomplete()
        adapter = CoachSoulAdapter(receipt_chain)

        with pytest.raises(IncompletePositiveSpaceError):
            adapter.load(positive_space, COACH_ID, negative_space_complete=True)

    def test_block_a_contains_5_cluster_laws(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Block A must contain reference to all 5 stylometry clusters."""
        positive_space = _make_positive_space_complete()
        adapter = CoachSoulAdapter(receipt_chain)

        result = adapter.load(
            positive_space, COACH_ID, negative_space_complete=True
        )

        assert result.block_a is not None
        laws_text = " ".join(result.block_a.structural_laws)
        # Check that all 5 cluster IDs are referenced
        for i in range(1, 6):
            assert f"Cluster {i}" in laws_text

    def test_humor_style_law_injected_when_provided(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """If humor classification is provided, Block A must include a humor law."""
        positive_space = _make_positive_space_complete()
        humor = HumorStyleClassification(
            primary_style=HumorType.AFFILIATIVE,
            secondary_style=HumorType.SELF_ENHANCING,
        )
        adapter = CoachSoulAdapter(receipt_chain)

        result = adapter.load(
            positive_space, COACH_ID, negative_space_complete=True, humor=humor
        )

        assert result.block_a is not None
        laws_text = " ".join(result.block_a.structural_laws)
        assert "HUMOR STYLE LAW" in laws_text
        assert "AFFILIATIVE" in laws_text

    def test_no_ttt_value_in_block_a_output(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """M-02: No TTT-NN values in Block A output strings."""
        import re
        positive_space = _make_positive_space_complete()
        adapter = CoachSoulAdapter(receipt_chain)

        result = adapter.load(
            positive_space, COACH_ID, negative_space_complete=True
        )

        assert result.block_a is not None
        laws_text = " ".join(result.block_a.structural_laws)
        ttt_pattern = re.compile(r"TTT-\d{1,2}")
        assert not ttt_pattern.search(laws_text), (
            "M-02 VIOLATION: TTT-NN value found in Block A coach_soul_adapter output"
        )


# ─── Adapter-4: PsychRoutingAdapter ──────────────────────────────────────────


class TestPsychRoutingAdapter:
    """C-08 rhythm whitelist + V1-V5 constraint generation + routing brief injection."""

    def test_all_rhythm_instructions_bypass_c08(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """FR8 C-08 mandate: ALL RhythmInstruction objects must have bypass_c08=True.

        Spec §Layer 2 §C-08 exception:
        'Sentence Rhythm generated by the Psychological Routing Adapter
        is computationally classified as a Structural Mechanic.
        Gate C-08 MUST whitelist rhythm instructions.'
        """
        emotional_dna = _make_emotional_dna(
            v2_type=AppraisalSequenceType.MECHANISM_FIRST,
            v3_ratio=0.8,
        )
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID)

        assert result.success is True
        assert result.block_b is not None

        for rhythm in result.block_b.rhythm_instructions:
            assert rhythm.bypass_c08 is True, (
                f"C-08 WHITELIST VIOLATION: RhythmInstruction '{rhythm.instruction_text[:50]}' "
                f"has bypass_c08={rhythm.bypass_c08} — must be True"
            )

    def test_v1_high_specificity_constraint_generated(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """V1 score=9 (HIGH SPECIFICITY) → constraint includes 'HIGH SPECIFICITY'."""
        emotional_dna = _make_emotional_dna(v1_score=9)
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID)

        assert result.block_b is not None
        constraints_text = " ".join(result.block_b.constraint_strings)
        assert "V1" in constraints_text
        assert "HIGH SPECIFICITY" in constraints_text

    def test_v5_agency_constraint_individual_generated(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """V5 bias=individual → constraint includes 'INDIVIDUAL agency bias'."""
        emotional_dna = _make_emotional_dna(v5_bias=AgencyAttributionType.INDIVIDUAL)
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID)

        assert result.block_b is not None
        constraints_text = " ".join(result.block_b.constraint_strings)
        assert "V5" in constraints_text
        assert "individual" in constraints_text.lower()

    def test_moral_foundation_high_weight_generates_constraint(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Moral foundation weight > 0.6 → active constraint generated."""
        emotional_dna = _make_emotional_dna(care_harm_weight=0.85)
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID)

        assert result.block_b is not None
        constraints_text = " ".join(result.block_b.constraint_strings)
        assert "V6 — Care/Harm" in constraints_text

    def test_moral_foundation_low_weight_no_constraint(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Moral foundation weight ≤ 0.6 → no constraint generated (inactive axis)."""
        emotional_dna = _make_emotional_dna(care_harm_weight=0.4)
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID)

        assert result.block_b is not None
        constraints_text = " ".join(result.block_b.constraint_strings)
        assert "V6 — Care/Harm" not in constraints_text

    def test_routing_brief_injected_when_provided(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """When routing_brief (DEP-ENG-016) is provided, its variables are injected."""
        emotional_dna = _make_emotional_dna()
        routing_brief = _make_routing_brief()
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID, routing_brief=routing_brief)

        assert result.block_b is not None
        constraints_text = " ".join(result.block_b.constraint_strings)
        assert "PSYCH ROUTING" in constraints_text
        assert "PRB-TEST-001" in constraints_text
        assert "PAYLOAD MASKING" in constraints_text

    def test_no_ttt_hardcoded_in_block_b_constraints(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """M-02: No TTT-NN values in Block B constraint strings."""
        import re
        emotional_dna = _make_emotional_dna()
        routing_brief = _make_routing_brief()
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID, routing_brief=routing_brief)

        assert result.block_b is not None
        constraints_text = " ".join(result.block_b.constraint_strings)
        ttt_pattern = re.compile(r"TTT-\d{1,2}")
        assert not ttt_pattern.search(constraints_text), (
            "M-02 VIOLATION: TTT-NN value found in psych_routing_adapter Block B output"
        )

    def test_metadata_flags_all_rhythm_whitelisted(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Metadata field 'all_rhythm_bypass_c08' must be True."""
        emotional_dna = _make_emotional_dna()
        adapter = PsychRoutingAdapter(receipt_chain)

        result = adapter.load(emotional_dna, COACH_ID)

        assert result.block_b is not None
        assert result.block_b.metadata.get("all_rhythm_bypass_c08") is True


# ─── Adapter-5: IREVCAdapter ─────────────────────────────────────────────────


class TestIREVCAdapter:
    """PTG safety gate + TTT runtime context injection + minimum viable warning."""

    def test_ptg_raw_unresolved_excluded_from_block_a(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """PTG safety gate: raw_unresolved triggers MUST NOT appear in Block A.

        Spec §Phase 4: 'raw_unresolved = HARD EXCLUDE from content activation.'
        """
        trigger_map = _make_trigger_map(n_resolved=3, n_raw_unresolved=2)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID)

        assert result.success is True
        assert result.block_a is not None
        laws_text = " ".join(result.block_a.structural_laws)
        # Raw unresolved trigger labels should NOT appear
        assert "Raw Unresolved Trigger 0" not in laws_text
        assert "Raw Unresolved Trigger 1" not in laws_text
        # Resolved triggers SHOULD appear
        assert "Test Trigger 0" in laws_text

    def test_ptg_gate_metadata_counts_correctly(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Metadata must report correct content_safe_triggers and raw_unresolved_excluded."""
        trigger_map = _make_trigger_map(n_resolved=3, n_raw_unresolved=2)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID)

        assert result.block_a is not None
        metadata = result.block_a.metadata
        assert metadata["content_safe_triggers"] == 3
        assert metadata["raw_unresolved_excluded"] == 2
        assert metadata["ptg_gate_status"] == "ENFORCED"

    def test_ttt_authenticated_context_injected(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """DEP-ENG-005 authenticated TTT → AUTHENTICATED context string injected."""
        trigger_map = _make_trigger_map(n_resolved=3)
        ttt_baseline = _make_ttt_baseline(authenticated=True)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID, ttt_baseline=ttt_baseline)

        assert result.block_a is not None
        laws_text = " ".join(result.block_a.structural_laws)
        assert "AUTHENTICATED TTT CONTEXT" in laws_text
        assert "SESSION-TST-001" in laws_text
        # Should be a factual state report — no TTT-NN assignment directive
        import re
        # The format is "Temperature=6/10" — no "TTT-06" directive
        assert not re.search(r"TTT-\d{1,2}", laws_text)

    def test_ttt_not_authenticated_produces_warning(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """LIWC < 7.0 → warning added, not a blocking failure."""
        trigger_map = _make_trigger_map(n_resolved=3)
        ttt_baseline = _make_ttt_baseline(authenticated=False)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID, ttt_baseline=ttt_baseline)

        assert result.success is True  # Not a blocking failure
        assert any("TTT_NOT_AUTHENTICATED" in w for w in result.warnings)

    def test_no_ttt_baseline_produces_warning(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """No ttt_baseline provided → DEP-ENG-005_ABSENT warning (non-blocking)."""
        trigger_map = _make_trigger_map(n_resolved=3)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID, ttt_baseline=None)

        assert result.success is True
        assert any("DEP-ENG-005_ABSENT" in w for w in result.warnings)

    def test_minimum_viable_map_warning_when_below_threshold(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """TriggerMap with < 2 resolved triggers → DEGRADED_MAP warning (non-blocking)."""
        trigger_map = _make_trigger_map(n_resolved=1)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID)

        assert result.success is True  # advisory only — does not halt
        assert any("DEGRADED_MAP" in w for w in result.warnings)

    def test_sufficient_triggers_no_degraded_warning(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """TriggerMap with ≥ 2 resolved triggers → no DEGRADED_MAP warning."""
        trigger_map = _make_trigger_map(n_resolved=3)
        adapter = IREVCAdapter(receipt_chain)

        result = adapter.load(trigger_map, COACH_ID)

        assert not any("DEGRADED_MAP" in w for w in result.warnings)


# ─── Pipeline: VoiceDNAAdapterPipeline ───────────────────────────────────────


class TestVoiceDNAAdapterPipeline:
    """Pipeline load order + Mandate 4 enforcement + full pipeline success."""

    def _make_pipeline_inputs(
        self,
        neg_space: NegativeSpaceObject | None = None,
        pos_space: PositiveSpaceObject | None = None,
        emotional_dna: EmotionalDNAProfile | None = None,
        trigger_map: TriggerMap | None = None,
        ttt_baseline: TTTBaselineData | None = None,
        routing_brief: PsychRoutingBrief | None = None,
    ) -> VoiceDNAPipelineInput:
        return VoiceDNAPipelineInput(
            coach_id=COACH_ID,
            negative_space=neg_space or _make_valid_negative_space(20),
            positive_space=pos_space or _make_positive_space_complete(),
            emotional_dna=emotional_dna or _make_emotional_dna(),
            trigger_map=trigger_map or _make_trigger_map(n_resolved=3),
            ttt_baseline=ttt_baseline,
            routing_brief=routing_brief,
        )

    def test_full_pipeline_success_all_4_adapters(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Full pipeline run with all valid inputs → all_success=True, 4 adapters."""
        inputs = self._make_pipeline_inputs(
            ttt_baseline=_make_ttt_baseline(authenticated=True),
            routing_brief=_make_routing_brief(),
        )
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        result = pipeline.run(inputs)

        assert result.all_success is True
        assert result.mandate_4_enforced is True
        assert result.negative_space_result is not None
        assert result.coach_soul_result is not None
        assert result.irevc_result is not None
        assert result.psych_routing_result is not None
        assert result.pipeline_receipt_id != ""

    def test_mandate4_load_order_enforced(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Mandate 4: negative_space_result must complete before coach_soul_result.

        Verifies mandate_4_enforced=True only after Adapter-2 succeeds.
        """
        inputs = self._make_pipeline_inputs()
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        result = pipeline.run(inputs)

        assert result.mandate_4_enforced is True
        # Adapter-2 completed (negative_space_result.success=True) before
        # Adapter-1 (coach_soul_result.success=True)
        assert result.negative_space_result is not None
        assert result.coach_soul_result is not None
        assert result.negative_space_result.success is True
        assert result.coach_soul_result.success is True

    def test_gate_pc03_fail_halts_pipeline_before_coach_soul(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Gate PC-03 fail → NegativeSpaceDepthGateError raised, coach_soul never called.

        Mandate 4: the pipeline MUST NOT proceed to Adapter-1 if Adapter-2 fails.
        """
        bad_neg_space = _make_valid_negative_space(contrastive_count=5)
        inputs = self._make_pipeline_inputs(neg_space=bad_neg_space)
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        with pytest.raises(NegativeSpaceDepthGateError):
            pipeline.run(inputs)

    def test_pipeline_block_a_injections_include_all_3_adapters(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Block A must include negative space, coach soul, and IREVC injections."""
        inputs = self._make_pipeline_inputs()
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        result = pipeline.run(inputs)

        block_a_sections = result.get_all_block_a_injections()
        slot_names = {inj.adapter_slot for inj in block_a_sections}
        assert AdapterSlot.NEGATIVE_SPACE_LOADER in slot_names
        assert AdapterSlot.COACH_SOUL in slot_names
        assert AdapterSlot.IREVC in slot_names

    def test_pipeline_block_b_injections_include_psych_routing(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Block B must include psych routing injection."""
        inputs = self._make_pipeline_inputs(routing_brief=_make_routing_brief())
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        result = pipeline.run(inputs)

        block_b_sections = result.get_all_block_b_injections()
        slot_names = {inj.adapter_slot for inj in block_b_sections}
        assert AdapterSlot.PSYCH_ROUTING in slot_names

    def test_format_full_skill_md_injection_returns_both_blocks(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """format_full_skill_md_injection returns non-empty block_a and block_b."""
        inputs = self._make_pipeline_inputs(
            ttt_baseline=_make_ttt_baseline(authenticated=True),
            routing_brief=_make_routing_brief(),
        )
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        blocks = pipeline.format_full_skill_md_injection(inputs)

        assert "block_a" in blocks
        assert "block_b" in blocks
        assert len(blocks["block_a"]) > 100
        assert len(blocks["block_b"]) > 50

    def test_adr01_coach_id_propagated_to_all_results(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """ADR-01: coach_id in inputs must propagate to all 4 adapter results."""
        specific_coach_id = "coach-SPECIFIC-999"
        inputs = VoiceDNAPipelineInput(
            coach_id=specific_coach_id,
            negative_space=_make_valid_negative_space(20),
            positive_space=_make_positive_space_complete(),
            emotional_dna=_make_emotional_dna(),
            trigger_map=_make_trigger_map(n_resolved=3),
        )
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        result = pipeline.run(inputs)

        assert result.coach_id == specific_coach_id
        assert result.negative_space_result is not None
        assert result.coach_soul_result is not None
        assert result.irevc_result is not None
        assert result.psych_routing_result is not None
        assert result.negative_space_result.coach_id == specific_coach_id
        assert result.coach_soul_result.coach_id == specific_coach_id
        assert result.irevc_result.coach_id == specific_coach_id
        assert result.psych_routing_result.coach_id == specific_coach_id

    def test_all_adapters_write_individual_receipts(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """FR47: Each adapter must write an individual receipt (non-empty receipt_id)."""
        inputs = self._make_pipeline_inputs()
        pipeline = VoiceDNAAdapterPipeline(receipt_chain)

        result = pipeline.run(inputs)

        assert result.negative_space_result is not None
        assert result.coach_soul_result is not None
        assert result.irevc_result is not None
        assert result.psych_routing_result is not None
        assert result.negative_space_result.receipt_id != ""
        assert result.coach_soul_result.receipt_id != ""
        assert result.irevc_result.receipt_id != ""
        assert result.psych_routing_result.receipt_id != ""
        # Pipeline also writes its own orchestration receipt
        assert result.pipeline_receipt_id != ""
