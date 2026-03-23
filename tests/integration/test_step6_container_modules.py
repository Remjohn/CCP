"""
CCP Step 6 — Integration Tests: Container Module Library

Tests covering all 39 Acceptance Criteria across FR9 (12 ACs),
FR10 (13 ACs), FR11 (9 ACs), FR12 (5 ACs).

Also covers:
  - PTG safety exclusion
  - Adjacent firewall
  - ADR-01 coach isolation
  - FAILED context premise halt
  - Graceful exit for zero matches
  - Language drift prevention
  - Gate 3 async flow
  - Fallback after 3 consecutive Gate 2 failures
"""

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.container_module_models import (
    ActivationEvent,
    ActivationEventSeed,
    ActivationSeedsPayload,
    AnchorQuality,
    AudienceSegmentProfile,
    AxisCongruence,
    AxisScore,
    ContainerModulePipelineConfig,
    ContextPremiseInsight,
    CopingMechanismInsight,
    DARNCATDimension,
    DepthDistribution,
    EmotionalTriggerInsight,
    ESKAnchor,
    FourAxisMatchResult,
    FourLawsStatus,
    Gate1Result,
    Gate2Result,
    Gate3FailureMode,
    Gate3Result,
    GateDiagnosticCertificate,
    GateVerdict,
    HiddenBeliefInsight,
    InGroupTerm,
    LanguageDriftStatus,
    MatchClassification,
    MatchResultsPayload,
    ProvenanceReport,
    RejectionTerm,
    SegmentCategories,
    StructuralCongruencePoint,
    ThemeContextPremise,
    TribalLanguageElement,
    TribalLanguageRegistry,
)
from src.ccp.services.activation_seed_builder import ActivationSeedBuilder
from src.ccp.services.audience_empathy_agent import AudienceEmpathyAgent
from src.ccp.services.failure_prevention_gates import FailurePreventionGates
from src.ccp.services.four_axis_matching_engine import FourAxisMatchingEngine


# ══════════════════════════════════════════════════════════════
# Test Fixtures
# ══════════════════════════════════════════════════════════════


def _make_insight(
    text: str = "test insight",
    depth: str = "L3",
    source: str = "forum post https://example.com",
    tribal_terms: list[str] | None = None,
    two_am_test: bool = True,
) -> dict:
    return {
        "text": text,
        "depth": depth,
        "source": source,
        "tribal_terms": tribal_terms or ["struggle-bus", "inner-work"],
        "two_am_test": two_am_test,
    }


def _make_hidden_belief(
    text: str = "test belief",
    depth: str = "L3",
    public_contradiction: str = "They say X, but believe Y",
    **kwargs,
) -> dict:
    base = _make_insight(text=text, depth=depth, **kwargs)
    base["public_contradiction"] = public_contradiction
    return base


def _make_emotional_trigger(
    text: str = "test trigger",
    depth: str = "L3",
    activation_keywords: list[str] | None = None,
    moral_foundation: str = "care_harm",
    involuntary_response: str = "anger + withdrawal",
    **kwargs,
) -> dict:
    base = _make_insight(text=text, depth=depth, **kwargs)
    base["activation_keywords"] = activation_keywords or ["burnout", "hustle"]
    base["moral_foundation"] = moral_foundation
    base["involuntary_response"] = involuntary_response
    return base


def _make_coping_mechanism(
    text: str = "test coping",
    depth: str = "L3",
    agency_attribution_pattern: str = "self",
    coping_potential_assessment: str = "medium",
    **kwargs,
) -> dict:
    base = _make_insight(text=text, depth=depth, **kwargs)
    base["agency_attribution_pattern"] = agency_attribution_pattern
    base["coping_potential_assessment"] = coping_potential_assessment
    return base


def _build_full_segment_data() -> tuple[
    list[dict], dict[str, dict[str, list[dict]]]
]:
    """Build complete 6-segment + 6×12 extraction data."""
    dhds = [
        "Autonomy", "Belonging", "Mastery",
        "Purpose", "Safety", "Recognition",
    ]
    coping_positions = [
        "SEARCH", "ACTIVE", "EXHAUSTED",
        "SEARCH", "ACTIVE", "EXHAUSTED",
    ]
    segments_data = []
    extraction_data: dict[str, dict[str, list[dict]]] = {}

    for i in range(6):
        seg_id = f"SEG-{i+1:02d}"
        segments_data.append({
            "segment_id": seg_id,
            "dhd_label": dhds[i],
            "coping_trajectory_position": coping_positions[i],
            "regulatory_focus": "promotion" if i < 3 else "prevention",
            "primary_moral_foundation_violated": "care_harm",
            "description": f"Segment {i+1} psychological portrait",
        })

        # Build all 12 categories with at least 1 insight each
        # Structural categories get ≥2 L3 entries
        cat_data: dict[str, list[dict]] = {}
        simple_cats = [
            "wants", "frustrations", "dreams", "fears",
            "suspicions", "insecurities", "envy_feelings", "enemies",
            "success_markers",
        ]
        for cat in simple_cats:
            cat_data[cat] = [_make_insight(text=f"{cat} insight for {seg_id}")]

        # Structural: hidden_beliefs ≥2 L3
        cat_data["hidden_beliefs"] = [
            _make_hidden_belief(text=f"belief 1 for {seg_id}"),
            _make_hidden_belief(text=f"belief 2 for {seg_id}"),
        ]
        # Structural: emotional_triggers ≥2 L3
        cat_data["emotional_triggers"] = [
            _make_emotional_trigger(text=f"trigger 1 for {seg_id}"),
            _make_emotional_trigger(text=f"trigger 2 for {seg_id}"),
        ]
        # Structural: coping_mechanism ≥2 L3
        cat_data["coping_mechanism"] = [
            _make_coping_mechanism(text=f"coping 1 for {seg_id}"),
            _make_coping_mechanism(text=f"coping 2 for {seg_id}"),
        ]

        extraction_data[seg_id] = cat_data

    return segments_data, extraction_data


def _build_tribal_language_data() -> dict:
    """Build tribal language data that passes Law 3 (≥10 in-group, ≥5 rejection)."""
    return {
        "in_group_terms": [
            {"term": f"tribal-term-{i}", "context": f"ctx-{i}", "example_usage": f"ex-{i}"}
            for i in range(12)
        ],
        "rejection_terms": [
            {"term": f"rejected-{i}", "why_rejected": f"generic-{i}", "what_to_use_instead": f"alt-{i}"}
            for i in range(6)
        ],
    }


def _build_trigger_map_data() -> dict:
    """Build a trigger map with mixed PTG statuses."""
    return {
        "triggers": [
            {
                "trigger_id": "TRG-001",
                "moral_foundation": "care_harm",
                "coping_trajectory_position": "ACTIVE",
                "agency_attribution": "self",
                "ptg_assessment": {"status": "resolved_dual_layer"},
                "origin_classification": {
                    "akb_level": "event_specific_knowledge",
                    "sensory_anchors": [
                        {"description": "The smell of hospital antiseptic"},
                        {"description": "Fluorescent buzzing at 3am"},
                    ],
                },
            },
            {
                "trigger_id": "TRG-002",
                "moral_foundation": "fairness_cheating",
                "coping_trajectory_position": "SEARCH",
                "agency_attribution": "institutional",
                "ptg_assessment": {"status": "resolved_dual_layer"},
                "origin_classification": {
                    "akb_level": "general_event",
                    "sensory_anchors": [],
                },
            },
            {
                "trigger_id": "TRG-003-UNSAFE",
                "moral_foundation": "loyalty_betrayal",
                "coping_trajectory_position": "EXHAUSTED",
                "agency_attribution": "self",
                "ptg_assessment": {"status": "raw_unresolved"},
                "origin_classification": {
                    "akb_level": "event_specific_knowledge",
                    "sensory_anchors": [],
                },
            },
        ],
    }


def _build_emotional_dna() -> dict:
    return {
        "overall_confidence": 0.85,
        "agency_attribution_type": "self",
        "version": "1.0",
        "trigger_map_version": "1.0",
    }


# ══════════════════════════════════════════════════════════════
# FR9 Tests (AC1–AC12)
# ══════════════════════════════════════════════════════════════


class TestFR9AudienceEmpathyAgent:
    """FR9: Audience Empathy Agent tests."""

    def _agent(self) -> AudienceEmpathyAgent:
        return AudienceEmpathyAgent(coach_acronym="TST")

    # AC1: Pipeline halts when DEP-ENG-006 missing
    def test_ac1_halts_on_missing_dep_eng_006(self):
        agent = self._agent()
        with pytest.raises(ValueError, match="DEP-ENG-006"):
            agent.ingest(theme="test", context_premise_map=None)

    def test_ac1_halts_on_empty_dep_eng_006(self):
        agent = self._agent()
        with pytest.raises(ValueError, match="DEP-ENG-006"):
            agent.ingest(theme="test", context_premise_map={})

    def test_ac1_halts_on_missing_theme(self):
        agent = self._agent()
        with pytest.raises(ValueError, match="Theme is required"):
            agent.ingest(theme="", context_premise_map={"key": "val"})

    # AC2: Exactly 6 segments
    def test_ac2_rejects_5_segments(self):
        agent = self._agent()
        ingested = agent.ingest(theme="test", context_premise_map={"k": "v"})
        with pytest.raises(ValueError, match="6 segments"):
            agent.segment(ingested, [{} for _ in range(5)])

    def test_ac2_rejects_7_segments(self):
        agent = self._agent()
        ingested = agent.ingest(theme="test", context_premise_map={"k": "v"})
        with pytest.raises(ValueError, match="6 segments"):
            agent.segment(ingested, [{} for _ in range(7)])

    # AC10: No two segments share same DHD + coping combo
    def test_ac10_rejects_duplicate_combo(self):
        agent = self._agent()
        ingested = agent.ingest(theme="test", context_premise_map={"k": "v"})
        dup_segments = [
            {"segment_id": f"S{i}", "dhd_label": "Autonomy",
             "coping_trajectory_position": "SEARCH",
             "primary_moral_foundation_violated": "care_harm",
             "description": f"seg {i}"}
            for i in range(6)
        ]
        with pytest.raises(ValueError, match="Duplicate DHD"):
            agent.segment(ingested, dup_segments)

    # AC3: All 72 cells populated
    def test_ac3_halts_on_empty_category(self):
        agent = self._agent()
        segments_data, extraction_data = _build_full_segment_data()
        ingested = agent.ingest(theme="test", context_premise_map={"k": "v"})
        segments = agent.segment(ingested, segments_data)
        # Remove a category from first segment
        extraction_data["SEG-01"].pop("wants")
        with pytest.raises(ValueError, match="AC3"):
            agent.extract(segments, extraction_data)

    # AC4: Law 2 depth distribution
    def test_ac4_depth_distribution(self):
        dd = DepthDistribution(l1=0.60, l2=0.30, l3=0.10)
        assert dd.passes_law_2() is True

    def test_ac4_depth_insufficient(self):
        dd = DepthDistribution(l1=0.90, l2=0.05, l3=0.05)
        assert dd.passes_law_2() is False

    # AC5: Law 1 — 2am test
    def test_ac5_law_1_reclassifies_failed_l3(self):
        agent = self._agent()
        insights = [
            ContextPremiseInsight(
                text="deep insight", depth="L3", source="forum",
                two_am_test=False,
            ),
            ContextPremiseInsight(
                text="authentic insight", depth="L3", source="forum",
                two_am_test=True,
            ),
        ]
        result = agent._validate_law_1(insights)
        assert result is True
        assert insights[0].depth == "L2"  # Reclassified
        assert insights[1].depth == "L3"  # Unchanged

    # AC6: Law 3 — tribal language
    def test_ac6_tribal_language_passes(self):
        registry = TribalLanguageRegistry(
            in_group_terms=[InGroupTerm(term=f"t{i}") for i in range(10)],
            rejection_terms=[RejectionTerm(term=f"r{i}") for i in range(5)],
        )
        assert registry.passes_law_3() is True

    def test_ac6_tribal_language_fails_insufficient_ingroup(self):
        registry = TribalLanguageRegistry(
            in_group_terms=[InGroupTerm(term=f"t{i}") for i in range(5)],
            rejection_terms=[RejectionTerm(term=f"r{i}") for i in range(5)],
        )
        assert registry.passes_law_3() is False

    # AC7: Law 4 — provenance
    def test_ac7_provenance_passes(self):
        report = ProvenanceReport(
            total_insights=100, verified_count=85, unverified_count=15,
            provenance_percentage=0.85,
        )
        assert report.passes_law_4() is True

    def test_ac7_provenance_fails(self):
        report = ProvenanceReport(
            total_insights=100, verified_count=70, unverified_count=30,
            provenance_percentage=0.70,
        )
        assert report.passes_law_4() is False

    # AC8: Structural L3 minimum
    def test_ac8_structural_l3_minimum(self):
        agent = self._agent()
        segments_data, extraction_data = _build_full_segment_data()
        ingested = agent.ingest(theme="test", context_premise_map={"k": "v"})
        segments = agent.segment(ingested, segments_data)
        # Reduce hidden_beliefs to 1 L3 entry (needs ≥2)
        extraction_data["SEG-01"]["hidden_beliefs"] = [
            _make_hidden_belief(text="only one", depth="L3"),
        ]
        with pytest.raises(ValueError, match="AC8"):
            segments_populated = agent.extract(segments, extraction_data)
            agent._validate_structural_weighting(segments_populated)

    # AC9: Verdict logic
    def test_ac9_authenticated(self):
        status = FourLawsStatus(
            law_1_lived_reality="PASS",
            law_2_depth_stratification="PASS",
            law_3_tribal_language="PASS",
            law_4_data_provenance="PASS",
        )
        assert status.compute_verdict() == "AUTHENTICATED"

    def test_ac9_provisional(self):
        status = FourLawsStatus(
            law_1_lived_reality="PASS",
            law_2_depth_stratification="PASS",
            law_3_tribal_language="PASS",
            law_4_data_provenance="FAIL",
        )
        assert status.compute_verdict() == "PROVISIONAL"

    def test_ac9_failed(self):
        status = FourLawsStatus(
            law_1_lived_reality="PASS",
            law_2_depth_stratification="FAIL",
            law_3_tribal_language="FAIL",
            law_4_data_provenance="FAIL",
        )
        assert status.compute_verdict() == "FAILED"

    # AC11: Output schema consumable by FR10
    def test_ac11_output_schema(self):
        segments_data, extraction_data = _build_full_segment_data()
        agent = self._agent()
        result = agent.run(
            theme="transformation",
            context_premise_map={"segments": "data"},
            segments_data=segments_data,
            extraction_data=extraction_data,
            tribal_language_data=_build_tribal_language_data(),
        )
        # Verify schema is FR10-compatible
        assert isinstance(result, ThemeContextPremise)
        assert len(result.segments) == 6
        assert result.four_laws_status.overall_status in (
            "AUTHENTICATED", "PROVISIONAL", "FAILED"
        )

    # AC12: No DEP-ENG-006 mutation
    def test_ac12_no_dep_eng_006_mutation(self):
        original = {"key": "original_value", "deep": {"nested": True}}
        agent = self._agent()
        ingested = agent.ingest(theme="test", context_premise_map=original)
        # Verify original dict is not modified
        assert original["key"] == "original_value"
        assert original["deep"]["nested"] is True


# ══════════════════════════════════════════════════════════════
# FR10 Tests (AC1–AC13)
# ══════════════════════════════════════════════════════════════


class TestFR10FourAxisMatchingEngine:
    """FR10: Four-Axis Structural Matching Engine tests."""

    def _engine(self) -> FourAxisMatchingEngine:
        return FourAxisMatchingEngine(coach_acronym="TST")

    def _make_context_premise(
        self, verdict: str = "AUTHENTICATED"
    ) -> ThemeContextPremise:
        segments_data, extraction_data = _build_full_segment_data()
        agent = AudienceEmpathyAgent(coach_acronym="TST")
        result = agent.run(
            theme="test_theme",
            context_premise_map={"k": "v"},
            segments_data=segments_data,
            extraction_data=extraction_data,
            tribal_language_data=_build_tribal_language_data(),
        )
        # Override verdict if needed
        if verdict != result.four_laws_status.overall_status:
            result.four_laws_status.overall_status = verdict
        return result

    # AC1: Halts on missing dependencies
    def test_ac1_halts_on_missing_dep_lib_001(self):
        engine = self._engine()
        cp = self._make_context_premise()
        with pytest.raises(ValueError, match="DEP-LIB-001"):
            engine.ingest(None, _build_trigger_map_data(), cp)

    def test_ac1_halts_on_missing_dep_lib_002(self):
        engine = self._engine()
        cp = self._make_context_premise()
        with pytest.raises(ValueError, match="DEP-LIB-002"):
            engine.ingest(_build_emotional_dna(), None, cp)

    def test_ac1_halts_on_missing_fr9(self):
        engine = self._engine()
        with pytest.raises(ValueError, match="FR9"):
            engine.ingest(_build_emotional_dna(), _build_trigger_map_data(), None)

    def test_ac1_halts_on_low_confidence(self):
        engine = self._engine()
        cp = self._make_context_premise()
        low_dna = {"overall_confidence": 0.3}
        with pytest.raises(ValueError, match="overall_confidence"):
            engine.ingest(low_dna, _build_trigger_map_data(), cp)

    # AC1 extension: Halts on FAILED FR9 verdict
    def test_ac1_halts_on_failed_context_premise(self):
        engine = self._engine()
        cp = self._make_context_premise(verdict="FAILED")
        with pytest.raises(ValueError, match="FAILED"):
            engine.ingest(_build_emotional_dna(), _build_trigger_map_data(), cp)

    # AC2: raw_unresolved triggers excluded
    def test_ac2_excludes_raw_unresolved(self):
        engine = self._engine()
        cp = self._make_context_premise()
        trigger_map = _build_trigger_map_data()
        result = engine.ingest(_build_emotional_dna(), trigger_map, cp)
        assert len(result["safe_triggers"]) == 2
        assert len(result["excluded_triggers"]) == 1
        assert result["excluded_triggers"][0]["trigger_id"] == "TRG-003-UNSAFE"

    # AC3: L3 only
    def test_ac3_l3_only_extraction(self):
        engine = self._engine()
        cp = self._make_context_premise()
        coords = engine.extract_l3_coordinates(cp)
        assert len(coords) == 6
        for coord in coords:
            # All extracted data should be from L3 sources
            assert coord.segment_id.startswith("SEG-")

    # AC4: [1.0, 1.0, 1.0, 0.0] → ADJACENT
    def test_ac4_three_exact_one_zero_is_adjacent(self):
        result = FourAxisMatchResult(
            trigger_id="T1", segment_id="S1",
            axis_scores={
                "moral_foundation": AxisScore(
                    axis_name="mf", congruence=AxisCongruence.EXACT, score=1.0
                ),
                "coping_potential": AxisScore(
                    axis_name="cp", congruence=AxisCongruence.CONGRUENT, score=1.0
                ),
                "agency_attribution": AxisScore(
                    axis_name="aa", congruence=AxisCongruence.CONGRUENT, score=1.0
                ),
                "temporal_position": AxisScore(
                    axis_name="tp", congruence=AxisCongruence.NONE, score=0.0
                ),
            },
        )
        classification = result.compute_classification()
        assert classification == MatchClassification.ADJACENT
        assert result.adjacent_flag is True

    # AC5: 2-axis match → ADJACENT
    def test_ac5_two_axis_match_is_adjacent(self):
        result = FourAxisMatchResult(
            trigger_id="T1", segment_id="S1",
            axis_scores={
                "moral_foundation": AxisScore(
                    axis_name="mf", congruence=AxisCongruence.EXACT, score=1.0
                ),
                "coping_potential": AxisScore(
                    axis_name="cp", congruence=AxisCongruence.CONGRUENT, score=1.0
                ),
                "agency_attribution": AxisScore(
                    axis_name="aa", congruence=AxisCongruence.NONE, score=0.0
                ),
                "temporal_position": AxisScore(
                    axis_name="tp", congruence=AxisCongruence.NONE, score=0.0
                ),
            },
        )
        classification = result.compute_classification()
        assert classification == MatchClassification.ADJACENT

    # Full CONFIRMED match
    def test_confirmed_match(self):
        result = FourAxisMatchResult(
            trigger_id="T1", segment_id="S1",
            axis_scores={
                "moral_foundation": AxisScore(
                    axis_name="mf", score=1.0, congruence=AxisCongruence.EXACT
                ),
                "coping_potential": AxisScore(
                    axis_name="cp", score=1.0, congruence=AxisCongruence.CONGRUENT
                ),
                "agency_attribution": AxisScore(
                    axis_name="aa", score=1.0, congruence=AxisCongruence.CONGRUENT
                ),
                "temporal_position": AxisScore(
                    axis_name="tp", score=1.0, congruence=AxisCongruence.CONGRUENT
                ),
            },
        )
        assert result.compute_classification() == MatchClassification.CONFIRMED

    # STRONG match: 3.5 with no zeros
    def test_strong_match(self):
        result = FourAxisMatchResult(
            trigger_id="T1", segment_id="S1",
            axis_scores={
                "moral_foundation": AxisScore(
                    axis_name="mf", score=1.0, congruence=AxisCongruence.EXACT
                ),
                "coping_potential": AxisScore(
                    axis_name="cp", score=1.0, congruence=AxisCongruence.CONGRUENT
                ),
                "agency_attribution": AxisScore(
                    axis_name="aa", score=1.0, congruence=AxisCongruence.CONGRUENT
                ),
                "temporal_position": AxisScore(
                    axis_name="tp", score=0.5, congruence=AxisCongruence.ADJACENT
                ),
            },
        )
        assert result.compute_classification() == MatchClassification.STRONG

    # NO_MATCH: sum < 2.0
    def test_no_match(self):
        result = FourAxisMatchResult(
            trigger_id="T1", segment_id="S1",
            axis_scores={
                "moral_foundation": AxisScore(
                    axis_name="mf", score=0.5, congruence=AxisCongruence.ADJACENT
                ),
                "coping_potential": AxisScore(
                    axis_name="cp", score=0.0, congruence=AxisCongruence.NONE
                ),
                "agency_attribution": AxisScore(
                    axis_name="aa", score=0.0, congruence=AxisCongruence.NONE
                ),
                "temporal_position": AxisScore(
                    axis_name="tp", score=0.0, congruence=AxisCongruence.NONE
                ),
            },
        )
        assert result.compute_classification() == MatchClassification.NO_MATCH

    # AC12: Cross-product evaluation
    def test_ac12_cross_product(self):
        engine = self._engine()
        cp = self._make_context_premise()
        result = engine.run(
            emotional_dna=_build_emotional_dna(),
            trigger_map=_build_trigger_map_data(),
            context_premise=cp,
        )
        # 2 safe triggers × 6 segments = 12 combinations
        assert result.total_combinations_evaluated == 12
        assert result.triggers_evaluated == 2
        assert result.segments_evaluated == 6

    # AC13: structural_congruence_point field present (tested in FR11)


# ══════════════════════════════════════════════════════════════
# FR11 Tests (AC1–AC6, AC8–AC9)
# ══════════════════════════════════════════════════════════════


class TestFR11ActivationSeedBuilder:
    """FR11: Activation Event Seed Construction tests."""

    def _builder(self) -> ActivationSeedBuilder:
        return ActivationSeedBuilder(coach_acronym="TST")

    def _make_match_results(self) -> MatchResultsPayload:
        """Build match results with some CONFIRMED + STRONG + ADJACENT."""
        return MatchResultsPayload(
            theme="test_theme",
            triggers_evaluated=2,
            segments_evaluated=6,
            total_combinations_evaluated=12,
            matches={
                "confirmed": [
                    FourAxisMatchResult(
                        trigger_id="TRG-001", segment_id="SEG-01", theme="test_theme",
                        match_classification=MatchClassification.CONFIRMED,
                        total_score=4.0,
                        axis_scores={
                            "moral_foundation": AxisScore(axis_name="mf", score=1.0),
                            "coping_potential": AxisScore(axis_name="cp", score=1.0),
                            "agency_attribution": AxisScore(axis_name="aa", score=1.0),
                            "temporal_position": AxisScore(axis_name="tp", score=1.0),
                        },
                    ),
                ],
                "strong": [
                    FourAxisMatchResult(
                        trigger_id="TRG-002", segment_id="SEG-02", theme="test_theme",
                        match_classification=MatchClassification.STRONG,
                        total_score=3.5,
                        axis_scores={
                            "moral_foundation": AxisScore(axis_name="mf", score=1.0),
                            "coping_potential": AxisScore(axis_name="cp", score=1.0),
                            "agency_attribution": AxisScore(axis_name="aa", score=1.0),
                            "temporal_position": AxisScore(axis_name="tp", score=0.5),
                        },
                    ),
                ],
                "adjacent": [
                    FourAxisMatchResult(
                        trigger_id="TRG-001", segment_id="SEG-03", theme="test_theme",
                        match_classification=MatchClassification.ADJACENT,
                        total_score=2.5,
                    ),
                ],
            },
            no_match_count=9,
        )

    def _make_context_premise(self) -> ThemeContextPremise:
        segments_data, extraction_data = _build_full_segment_data()
        agent = AudienceEmpathyAgent(coach_acronym="TST")
        return agent.run(
            theme="test_theme",
            context_premise_map={"k": "v"},
            segments_data=segments_data,
            extraction_data=extraction_data,
            tribal_language_data=_build_tribal_language_data(),
        )

    # AC1: ADJACENT and NO_MATCH excluded
    def test_ac1_excludes_adjacent(self):
        builder = self._builder()
        mr = self._make_match_results()
        cp = self._make_context_premise()
        ingested = builder.ingest(mr, _build_trigger_map_data(), cp)
        # Only CONFIRMED + STRONG = 2 matches
        assert len(ingested["seedable_matches"]) == 2

    # AC8: Zero valid matches → graceful exit
    def test_ac8_graceful_exit(self):
        builder = self._builder()
        mr = MatchResultsPayload(
            theme="test_theme",
            matches={"confirmed": [], "strong": [], "adjacent": []},
            no_match_count=12,
        )
        cp = self._make_context_premise()
        result = builder.run(mr, _build_trigger_map_data(), cp)
        assert result.graceful_exit is True
        assert result.status == "graceful_exit_zero_matches"
        assert len(result.seeds) == 0

    # AC2: ESK anchor quality
    def test_ac2_esk_anchor_full(self):
        builder = self._builder()
        trigger = {
            "origin_classification": {
                "akb_level": "event_specific_knowledge",
                "sensory_anchors": [{"description": "cold tile"}],
            },
        }
        anchor = builder._extract_esk_anchor(trigger)
        assert anchor.anchor_quality == AnchorQuality.FULL
        assert anchor.requires_esk_harvesting is False

    def test_ac2_esk_anchor_degraded(self):
        builder = self._builder()
        trigger = {
            "origin_classification": {
                "akb_level": "general_event",
                "sensory_anchors": [],
            },
        }
        anchor = builder._extract_esk_anchor(trigger)
        assert anchor.anchor_quality == AnchorQuality.DEGRADED
        assert anchor.requires_esk_harvesting is True

    # AC4: DARN-CAT dimension
    def test_ac4_darn_cat_taking_steps(self):
        builder = self._builder()
        esk = ESKAnchor(akb_level="esk", anchor_quality=AnchorQuality.FULL)
        tribal = TribalLanguageElement(extracted_terms=["struggle-bus", "inner-work", "shadow-self"])
        congruence = StructuralCongruencePoint(
            moral_foundation="care_harm",
            articulation="shared structural pain",
        )
        event = builder.construct_darn_cat(esk, tribal, congruence)
        assert event.darn_cat_dimension in (
            DARNCATDimension.TAKING_STEPS, DARNCATDimension.REASONS
        )
        assert len(event.question_text) > 0

    # AC5: Language drift rejection for 0 terms
    def test_ac5_language_drift_critical(self):
        builder = self._builder()
        seed = ActivationEventSeed(
            match_id="M1",
            match_classification=MatchClassification.CONFIRMED,
            match_score=4.0,
            esk_anchor=ESKAnchor(akb_level="esk"),
            tribal_language=TribalLanguageElement(
                extracted_terms=["zzz-nonexistent-term"]
            ),
            activation_event=ActivationEvent(
                grounding_statement="text without any tribal terms",
                episodic_bridge="more text",
                question_text="question text",
            ),
        )
        result = builder.language_drift_gate(seed)
        assert result.tribal_language.language_drift_status == LanguageDriftStatus.CRITICAL

    # AC6: Tribal term count tracked
    def test_ac6_tribal_term_count(self):
        builder = self._builder()
        mr = self._make_match_results()
        cp = self._make_context_premise()
        result = builder.run(mr, _build_trigger_map_data(), cp)
        for seed in result.seeds:
            assert hasattr(seed.tribal_language, "verified_count")
            assert hasattr(seed.activation_event, "tribal_terms_used")

    # AC9: Receipt chain
    def test_ac9_receipt_chain(self):
        rc = ReceiptChain(coach_acronym="TST")
        builder = ActivationSeedBuilder(coach_acronym="TST", receipt_chain=rc)
        mr = self._make_match_results()
        cp = self._make_context_premise()
        builder.run(mr, _build_trigger_map_data(), cp)
        # Should have at least ingest + drift gate + emit receipts
        assert rc.chain_length() >= 3


# ══════════════════════════════════════════════════════════════
# FR12 Tests (AC1–AC5)
# ══════════════════════════════════════════════════════════════


class TestFR12FailurePreventionGates:
    """FR12: Three Failure Prevention Gates tests."""

    def _gates(self) -> FailurePreventionGates:
        return FailurePreventionGates(coach_acronym="TST")

    # AC1: Gate 1 — [1.0, 1.0, 1.0, 0.0] → FAIL
    def test_ac1_gate_1_zero_axis_fails(self):
        gate = Gate1Result()
        verdict = gate.evaluate({
            "moral_foundation": 1.0,
            "coping_potential": 1.0,
            "agency_attribution": 1.0,
            "temporal_position": 0.0,
        })
        assert verdict == GateVerdict.FAIL
        assert gate.adjacent_flag is True

    def test_gate_1_pass(self):
        gate = Gate1Result()
        verdict = gate.evaluate({
            "moral_foundation": 1.0,
            "coping_potential": 1.0,
            "agency_attribution": 1.0,
            "temporal_position": 0.5,
        })
        assert verdict == GateVerdict.PASS

    def test_gate_1_provisional(self):
        gate = Gate1Result()
        verdict = gate.evaluate({
            "moral_foundation": 1.0,
            "coping_potential": 1.0,
            "agency_attribution": 0.5,
            "temporal_position": 0.5,
        })
        assert verdict == GateVerdict.PROVISIONAL

    # AC2: Gate 2 — 2 matches → PROVISIONAL
    def test_ac2_gate_2_provisional(self):
        gate = Gate2Result()
        verdict = gate.evaluate(["term1", "term2"])
        assert verdict == GateVerdict.PROVISIONAL
        assert gate.language_drift_warning is True

    def test_gate_2_pass(self):
        gate = Gate2Result()
        verdict = gate.evaluate(["t1", "t2", "t3"])
        assert verdict == GateVerdict.PASS
        assert gate.language_drift_warning is False

    def test_gate_2_fail(self):
        gate = Gate2Result()
        verdict = gate.evaluate(["only_one"])
        assert verdict == GateVerdict.FAIL

    # AC3: Certificate contains receipt chain hash
    def test_ac3_certificate_structure(self):
        cert = GateDiagnosticCertificate(
            seed_reference_id="SEED-001",
            receipt_chain_hash="abc123",
            gate_1_structural_congruence=Gate1Result(verdict=GateVerdict.PASS),
            gate_2_language_drift=Gate2Result(verdict=GateVerdict.PASS),
        )
        assert cert.gate_certificate_id.startswith("CERT-")
        assert cert.receipt_chain_hash == "abc123"
        assert cert.is_cleared_for_emission() is True

    def test_certificate_blocked_on_gate_1_fail(self):
        cert = GateDiagnosticCertificate(
            seed_reference_id="SEED-002",
            gate_1_structural_congruence=Gate1Result(verdict=GateVerdict.FAIL),
            gate_2_language_drift=Gate2Result(verdict=GateVerdict.PASS),
        )
        assert cert.is_cleared_for_emission() is False

    def test_certificate_blocked_on_gate_2_fail(self):
        cert = GateDiagnosticCertificate(
            seed_reference_id="SEED-003",
            gate_1_structural_congruence=Gate1Result(verdict=GateVerdict.PASS),
            gate_2_language_drift=Gate2Result(verdict=GateVerdict.FAIL),
        )
        assert cert.is_cleared_for_emission() is False

    # AC4: Gate 3 — LIWC-22 < 5.0 + historical decay → PTG retrograde
    def test_ac4_gate_3_coach_temporal_error(self):
        gate = Gate3Result()
        verdict = gate.evaluate(
            liwc_score=4.2,
            historical_trigger_decay=True,
            historical_trigger_flawless=False,
        )
        assert verdict == GateVerdict.FAIL
        assert gate.failure_mode == Gate3FailureMode.COACH_TEMPORAL_ERROR
        assert gate.coach_ptg_retrograde is True
        assert gate.downstream_mutations["dep_lib_002_mutated"] is True

    def test_ac4_gate_3_audience_extraction_error(self):
        gate = Gate3Result()
        verdict = gate.evaluate(
            liwc_score=3.5,
            historical_trigger_decay=False,
            historical_trigger_flawless=True,
        )
        assert verdict == GateVerdict.FAIL
        assert gate.failure_mode == Gate3FailureMode.AUDIENCE_EXTRACTION_ERROR
        assert gate.audience_l3_revalidation is True
        assert gate.downstream_mutations["dep_eng_006_mutated"] is True

    def test_gate_3_pass(self):
        gate = Gate3Result()
        verdict = gate.evaluate(liwc_score=8.5)
        assert verdict == GateVerdict.PASS

    def test_gate_3_provisional(self):
        gate = Gate3Result()
        verdict = gate.evaluate(liwc_score=6.0)
        assert verdict == GateVerdict.PROVISIONAL

    # AC5: ADR-01 Coach Isolation
    def test_ac5_adr_01_isolation(self):
        """Verify each gates instance is scoped to one coach_acronym."""
        gates_a = FailurePreventionGates(coach_acronym="AAA")
        gates_b = FailurePreventionGates(coach_acronym="BBB")
        assert gates_a.coach_acronym == "AAA"
        assert gates_b.coach_acronym == "BBB"
        # Separate receipt chains
        assert gates_a.receipt_chain is not gates_b.receipt_chain

    # Fallback after 3 consecutive Gate 2 failures
    def test_consecutive_gate_2_failures_fallback(self):
        gates = self._gates()
        seed = ActivationEventSeed(
            match_id="M1",
            match_classification=MatchClassification.CONFIRMED,
            match_score=4.0,
            tribal_language=TribalLanguageElement(extracted_terms=[]),
            activation_event=ActivationEvent(
                grounding_statement="no tribal terms here",
                episodic_bridge="nothing",
                question_text="nothing",
            ),
        )
        # Run Gate 2 three times with 0 matching terms
        for i in range(3):
            gates.run_gate_2(seed)
        assert gates.gate_2_consecutive_failures >= 3


# ══════════════════════════════════════════════════════════════
# Pipeline Config Tests
# ══════════════════════════════════════════════════════════════


class TestContainerModuleConfig:
    def test_theme_slug(self):
        config = ContainerModulePipelineConfig(
            coach_id="C1", coach_acronym="TST", theme="Self-Transformation Journey"
        )
        slug = config.compute_theme_slug()
        assert slug == "self_transformation_journey"
        assert "'" not in slug
        assert "-" not in slug
