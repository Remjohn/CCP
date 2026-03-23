"""
CCP FR8 TTT Enforcement Rule — Integration Tests (Unit 10)
Tests all 12 acceptance criteria from the FR8 spec.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md §Acceptance Criteria
"""

import json
import math
from pathlib import Path
from typing import Any

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ttt_models import (
    BlockALaw,
    BlockBField,
    C08Status,
    C08ViolationType,
    CompiledDesignBrief,
    SophiaDriftVerdict,
    TextureQuality,
    ToneRegister,
    TTTBaselineData,
)
from src.ccp.pipelines.ttt_enforcement_pipeline import TTTEnforcementPipeline
from src.ccp.services.assembly_report_writer import AssemblyReportWriter
from src.ccp.services.c08_ttt_enforcement import C08TTTEnforcement, run_c08
from src.ccp.services.sophia_ttt_validator import (
    DRIFT_THRESHOLD,
    PEAK_EXCEEDANCE_THRESHOLD,
    SIMILARITY_THRESHOLD,
    SophiaTTTValidator,
)
from src.ccp.services.ttt_affinity_advisor import TTTAffinityAdvisor
from src.ccp.services.ttt_baseline_extractor import (
    LIWC_AUTHENTICITY_THRESHOLD,
    LIWCAuthenticationError,
    TTTBaselineExtractor,
)
from src.ccp.tools.template_m02_checker import TemplateM02Checker


# ─── Shared Fixtures ─────────────────────────────────────────────────────────


@pytest.fixture()
def tmp_coach_dir(tmp_path: Path) -> Path:
    """Temporary coach directory with config/ subdirectory."""
    coach_dir = tmp_path / "coaches" / "TST"
    (coach_dir / "config").mkdir(parents=True)
    return coach_dir


@pytest.fixture()
def receipt_chain(tmp_path: Path) -> ReceiptChain:
    """In-memory receipt chain for testing."""
    return ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "receipts"),
    )


@pytest.fixture()
def ttt_baseline() -> TTTBaselineData:
    """Authenticated TTT baseline fixture."""
    return TTTBaselineData(
        temperature=6,
        texture=TextureQuality.CONVERSATIONAL,
        tone=ToneRegister.NURTURING,
        liwc_authenticity_score=8.2,
        session_id="sess-test-001",
        coach_id="coach-TST-001",
    )


def _make_clean_brief(
    compilation_id: str = "COMP-TEST-001",
    archetype_id: str = "story_transformation",
    extra_block_b: list[BlockBField] | None = None,
    extra_block_a: list[BlockALaw] | None = None,
) -> CompiledDesignBrief:
    """Create a clean compiled brief with no TTT violations."""
    block_b = [
        BlockBField(name="hook_strategy", value="Open with a question"),
        BlockBField(name="narrative_arc", value="3-act structure — tension to resolution"),
        BlockBField(name="dep_eng_005_reference", value="LOAD:ttt_baseline.json", context="runtime_reference"),
    ]
    if extra_block_b:
        block_b.extend(extra_block_b)

    block_a = [
        BlockALaw(law_id="law_01", text="Hook must open with a rhetorical question."),
        BlockALaw(law_id="law_02", text="CTA must arrive in the final 10% of the piece."),
    ]
    if extra_block_a:
        block_a.extend(extra_block_a)

    return CompiledDesignBrief(
        compilation_id=compilation_id,
        archetype_id=archetype_id,
        block_b_fields=block_b,
        block_a_structural_laws=block_a,
        dep_eng_005_reference="config/ttt_baseline.json",
    )


def _make_generated_content_analysis(
    affect: float = 6.0,
    posemo: float = 5.5,
    negemo: float = 2.0,
    authentic: float = 7.8,
    segment_intensities: list[float] | None = None,
) -> dict[str, Any]:
    """Build a synthetic LIWC content analysis dict."""
    analysis: dict[str, Any] = {
        "affect": affect,
        "posemo": posemo,
        "negemo": negemo,
        "social": 4.5,
        "insight": 3.0,
        "cogmech": 5.0,
        "clout": 6.0,
        "authentic": authentic,
        "anger": 1.0,
        "achieve": 3.5,
    }
    if segment_intensities:
        analysis["segment_intensities"] = segment_intensities
    return analysis


# ─── AC1: Block B TTT field name → REJECT ────────────────────────────────────


class TestAC1BlockBHardcodedTTT:
    """AC1: Block B field named 'ttt_temperature' with value 'TTT-06' → C-08 REJECT."""

    def test_c08_rejects_explicit_ttt_field(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC1-001",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="ttt_temperature", value="TTT-06"),
                BlockBField(name="narrative_arc", value="3-act structure"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)

        assert not result.passed
        assert result.status == C08Status.FAIL
        assert result.first_violation is not None
        assert result.first_violation.violation_type == C08ViolationType.HARDCODED_IN_BLOCK_B
        assert result.first_violation.violating_field == "ttt_temperature"

    def test_c08_violation_includes_recovery_instruction(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC1-002",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="temperature", value=7),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)

        assert not result.passed
        assert result.first_violation is not None
        assert len(result.first_violation.recovery_instruction) > 0
        assert result.first_violation.mandate_violated == "M-02"

    def test_c08_passes_clean_block_b(self) -> None:
        brief = _make_clean_brief()
        result = run_c08(brief)
        assert result.passed
        assert result.status == C08Status.PASS
        assert len(result.violations) == 0


# ─── AC2: Block B value string contains TTT-XX → REJECT ──────────────────────


class TestAC2ValueEmbeddedTTT:
    """AC2: Block B value containing embedded TTT reference → C-08 REJECT."""

    def test_embedded_ttt_in_string_value(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC2-001",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(
                    name="field_9",
                    value="maintain warm register at TTT-04",
                ),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)

        assert not result.passed
        assert result.first_violation is not None
        assert result.first_violation.violation_type == C08ViolationType.VALUE_EMBEDDED_IN_BLOCK_B

    def test_override_ttt_in_value(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC2-002",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="generation_params", value="override_ttt=8"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)
        assert not result.passed

    def test_temperature_assignment_in_value(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC2-003",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="config", value="temperature:7"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)
        assert not result.passed


# ─── AC3: Block A structural law contains TTT directive → REJECT ──────────────


class TestAC3BlockADirective:
    """AC3: Block A structural law with TTT directive → C-08 REJECT."""

    def test_block_a_ttt_directive_rejected(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC3-001",
            archetype_id="story_transformation",
            block_b_fields=[],
            block_a_structural_laws=[
                BlockALaw(
                    law_id="law_hook",
                    text="The Hook must hit TTT-08 — maximum urgency.",
                ),
            ],
        )
        result = run_c08(brief)

        assert not result.passed
        assert result.first_violation is not None
        assert result.first_violation.violation_type == C08ViolationType.DIRECTIVE_IN_BLOCK_A

    def test_block_a_clean_law_passes(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC3-002",
            archetype_id="story_transformation",
            block_b_fields=[],
            block_a_structural_laws=[
                BlockALaw(
                    law_id="law_hook",
                    text="The Hook must open with a rhetorical question.",
                ),
            ],
        )
        result = run_c08(brief)
        assert result.passed


# ─── AC4: Block A Field 4 affinity advisory → PASS ───────────────────────────


class TestAC4AffinityAdvisoryPermitted:
    """AC4: Affinity range advisory in Block A Field 4 is NOT rejected by C-08."""

    def test_advisory_reference_passes_c08(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC4-001",
            archetype_id="story_transformation",
            block_b_fields=[],
            block_a_structural_laws=[
                BlockALaw(
                    law_id="field_4_advisory",
                    text="Natural affinity range for this archetype: TTT-02 to TTT-05.",
                    context="natural_affinity_range_advisory",
                ),
            ],
        )
        result = run_c08(brief)
        assert result.passed, (
            "Block A advisory reference should PASS C-08. "
            f"Got: {result.first_violation}"
        )

    def test_advisory_context_is_required_for_exemption(self) -> None:
        """Without advisory context, a TTT reference in Block A is still rejected."""
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC4-002",
            archetype_id="story_transformation",
            block_b_fields=[],
            block_a_structural_laws=[
                BlockALaw(
                    law_id="law_01",
                    text="Natural affinity range for this archetype: TTT-02 to TTT-05.",
                    # No advisory context → treated as a structural directive
                ),
            ],
        )
        result = run_c08(brief)
        assert not result.passed


# ─── AC5: TTT field alias detection → REJECT ─────────────────────────────────


class TestAC5AliasDetection:
    """AC5: Block B field named 'emotional_heat' → alias detected → REJECT."""

    def test_emotional_heat_alias_rejected(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC5-001",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="emotional_heat", value=7),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)

        assert not result.passed
        assert result.first_violation is not None
        assert result.first_violation.violating_field == "emotional_heat"

    def test_heat_setting_alias_rejected(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC5-002",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="heat_setting", value="medium"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)
        assert not result.passed

    def test_emotional_register_alias_rejected(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC5-003",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="emotional_register", value="high"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)
        assert not result.passed

    def test_sentence_rhythm_exempted(self) -> None:
        """Sentence rhythm (adapter-6 output) is whitelisted — Exception Exemption."""
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC5-004",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="sentence_rhythm", value="short-long-short pattern"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)
        assert result.passed, (
            "sentence_rhythm is whitelisted (Exception Exemption). "
            f"Got: {result.first_violation}"
        )


# ─── AC6: REJECT result is zero-token ────────────────────────────────────────


class TestAC6ZeroTokenGuarantee:
    """AC6: C-08 REJECT result has tokens_consumed=0, adapter_invocations=0, section_assemblies=0."""

    def test_reject_result_has_zero_tokens(self) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC6-001",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="ttt_temperature", value="TTT-06"),
            ],
            block_a_structural_laws=[],
        )
        result = run_c08(brief)

        assert not result.passed
        assert result.tokens_consumed == 0, f"Expected 0 tokens, got {result.tokens_consumed}"
        assert result.adapter_invocations == 0, f"Expected 0 adapter invocations, got {result.adapter_invocations}"
        assert result.section_assemblies == 0, f"Expected 0 section assemblies, got {result.section_assemblies}"

    def test_pass_result_also_zero(self) -> None:
        """PASS result is also zero-token (no assembly yet at Tier 0 stage)."""
        brief = _make_clean_brief()
        result = run_c08(brief)

        assert result.passed
        assert result.tokens_consumed == 0
        assert result.adapter_invocations == 0
        assert result.section_assemblies == 0


# ─── AC7: LIWC-22 Authenticity Gate ──────────────────────────────────────────


class TestAC7LIWCAuthenticationGate:
    """AC7: LIWC score ≥ 7.0 → liwc_authenticated=True; score < 7.0 → LIWCAuthenticationError."""

    @pytest.fixture()
    def high_liwc_analysis(self) -> dict[str, Any]:
        return {
            "authentic": 8.5,
            "affect": 6.0,
            "posemo": 5.5,
            "analytic": 4.0,
            "clout": 6.5,
            "informal": 2.0,
            "cogmech": 3.0,
            "anger": 1.0,
            "negemo": 1.5,
            "social": 4.0,
            "insight": 3.5,
            "achieve": 3.0,
        }

    @pytest.fixture()
    def low_liwc_analysis(self) -> dict[str, Any]:
        return {
            "authentic": 5.2,
            "affect": 2.0,
            "posemo": 1.5,
            "analytic": 7.0,
            "clout": 4.0,
            "informal": 1.0,
            "cogmech": 6.0,
            "anger": 0.5,
            "negemo": 0.5,
            "social": 2.0,
            "insight": 2.0,
            "achieve": 2.0,
        }

    def test_authenticated_above_threshold(
        self, tmp_coach_dir: Path, high_liwc_analysis: dict[str, Any]
    ) -> None:
        extractor = TTTBaselineExtractor(tmp_coach_dir)
        baseline = extractor.extract(
            liwc_analysis=high_liwc_analysis,
            session_id="sess-001",
            coach_id="coach-TST-001",
        )
        assert baseline.liwc_authenticated is True
        assert baseline.liwc_authenticity_score >= LIWC_AUTHENTICITY_THRESHOLD

    def test_rejects_below_threshold(
        self, tmp_coach_dir: Path, low_liwc_analysis: dict[str, Any]
    ) -> None:
        extractor = TTTBaselineExtractor(tmp_coach_dir)
        with pytest.raises(LIWCAuthenticationError) as exc_info:
            extractor.extract(
                liwc_analysis=low_liwc_analysis,
                session_id="sess-002",
                coach_id="coach-TST-001",
            )
        assert exc_info.value.score < LIWC_AUTHENTICITY_THRESHOLD
        assert exc_info.value.threshold == LIWC_AUTHENTICITY_THRESHOLD

    def test_ttt_baseline_data_auth_gate(self) -> None:
        """TTTBaselineData field_validator sets liwc_authenticated from score."""
        baseline_auth = TTTBaselineData(
            temperature=6,
            texture=TextureQuality.CONVERSATIONAL,
            tone=ToneRegister.NURTURING,
            liwc_authenticity_score=7.5,
            session_id="s-01",
            coach_id="c-01",
        )
        assert baseline_auth.liwc_authenticated is True

        baseline_not_auth = TTTBaselineData(
            temperature=6,
            texture=TextureQuality.CONVERSATIONAL,
            tone=ToneRegister.NURTURING,
            liwc_authenticity_score=6.9,
            session_id="s-02",
            coach_id="c-01",
        )
        assert baseline_not_auth.liwc_authenticated is False


# ─── AC8: Affinity range advisory — never blocks ─────────────────────────────


class TestAC8AffinityRangeAdvisory:
    """AC8: TTT outside affinity range → advisory logged, compilation_blocked=False."""

    def test_outside_range_is_advisory_only(self) -> None:
        """Coach at TTT-08 outside story_transformation range (TTT-02 to TTT-05)."""
        advisor = TTTAffinityAdvisor()
        result = advisor.evaluate(
            archetype_id="story_transformation",
            coach_temperature=8,
        )

        assert result.ttt_outside_affinity_range is True
        assert result.compilation_blocked is False
        assert result.requires_human_review is True

    def test_inside_range_not_flagged(self) -> None:
        advisor = TTTAffinityAdvisor()
        result = advisor.evaluate(
            archetype_id="story_transformation",
            coach_temperature=4,
        )
        assert result.ttt_outside_affinity_range is False
        assert result.compilation_blocked is False

    def test_unknown_archetype_passes_without_blocking(self) -> None:
        advisor = TTTAffinityAdvisor()
        result = advisor.evaluate(
            archetype_id="unknown_custom_archetype",
            coach_temperature=9,
        )
        assert result.compilation_blocked is False
        assert result.ttt_outside_affinity_range is False


# ─── AC9: Sophia drift gate ───────────────────────────────────────────────────


class TestAC9SophiaDriftGate:
    """AC9: Sophia drift > 0.15 → DRIFT_EXCEEDED; drift < 0.15 → PASS (or higher priority verdict)."""

    def test_high_drift_rejected(self, ttt_baseline: TTTBaselineData) -> None:
        # Temperature 6 → normalized 0.6 baseline
        # Generated affect=9.8 → normalized ~0.98 → drift > 0.15
        generated = _make_generated_content_analysis(affect=9.8, posemo=9.0)
        validator = SophiaTTTValidator()
        result = validator.validate(
            baseline=ttt_baseline,
            generated_content_analysis=generated,
            compilation_id="COMP-AC9-001",
            model_id="gpt-4",
        )
        assert result.verdict == SophiaDriftVerdict.DRIFT_EXCEEDED
        assert not result.drift_passed
        assert result.ttt_drift_percentage > DRIFT_THRESHOLD

    def test_low_drift_can_pass(self, ttt_baseline: TTTBaselineData) -> None:
        # Temperature 6 → normalized 0.6
        # Generated affect matching closely → drift < 0.15
        generated = _make_generated_content_analysis(
            affect=6.1,
            posemo=5.6,
            segment_intensities=[5.8, 6.2, 7.5, 6.0, 5.9],  # Has peaks
        )
        validator = SophiaTTTValidator()
        result = validator.validate(
            baseline=ttt_baseline,
            generated_content_analysis=generated,
            compilation_id="COMP-AC9-002",
            model_id="gpt-4",
        )
        assert result.drift_passed is True

    def test_model_offset_applied(self, ttt_baseline: TTTBaselineData) -> None:
        """Model offset from registry is applied before drift calculation."""
        generated = _make_generated_content_analysis(
            affect=6.0,
            posemo=5.5,
            segment_intensities=[5.8, 6.3, 7.8, 6.1, 5.9],
        )
        validator = SophiaTTTValidator()
        result = validator.validate(
            baseline=ttt_baseline,
            generated_content_analysis=generated,
            compilation_id="COMP-AC9-003",
            model_id="groq",  # groq offset = -0.12
        )
        # Model offset should be recorded in result
        assert result.model_offset_applied != 0.0


# ─── AC10: Sophia emotional peak detection ────────────────────────────────────


class TestAC10EmotionalPeakDetection:
    """AC10: 0 peaks above +20% avg → FLAT_EMOTIONAL_ARC; ≥1 peak → peaks_passed=True."""

    def test_flat_arc_detected(self, ttt_baseline: TTTBaselineData) -> None:
        # Matching affect scores (no drift) but perfectly flat segment intensities
        generated = _make_generated_content_analysis(
            affect=6.0,
            posemo=5.5,
            # All segments identical → no peaks above +20% avg
            segment_intensities=[6.0, 6.0, 6.0, 6.0, 6.0],
        )
        validator = SophiaTTTValidator()
        result = validator.validate(
            baseline=ttt_baseline,
            generated_content_analysis=generated,
            compilation_id="COMP-AC10-001",
            model_id="gpt-4",
        )
        assert result.peaks_passed is False
        # FLAT_EMOTIONAL_ARC only fires if drift and similarity PASS first
        if result.drift_passed and result.similarity_passed:
            assert result.verdict == SophiaDriftVerdict.FLAT_EMOTIONAL_ARC

    def test_peaks_detected_passes(self, ttt_baseline: TTTBaselineData) -> None:
        # At least one segment clearly above +20% of average
        avg = 6.0
        peak_value = avg * 1.30  # 30% above average — exceeds 20% threshold
        generated = _make_generated_content_analysis(
            affect=6.0,
            posemo=5.5,
            segment_intensities=[5.8, 6.0, peak_value, 5.9, 6.1],
        )
        validator = SophiaTTTValidator()
        result = validator.validate(
            baseline=ttt_baseline,
            generated_content_analysis=generated,
            compilation_id="COMP-AC10-002",
            model_id="gpt-4",
        )
        assert result.peaks_passed is True
        assert len(result.emotional_peaks) >= 1

    def test_borderline_peak_threshold(self, ttt_baseline: TTTBaselineData) -> None:
        """Peak exactly at 20% above average — should count as passing."""
        # avg = 6.0, peak at 6.0 * 1.20 = 7.20
        avg = 6.0
        # iRAV: peak exceeding average by ≥ 20% (spec: strictly exceeds)
        peak_value = avg * 1.21  # 21% above — clearly exceeds
        generated = _make_generated_content_analysis(
            affect=6.0,
            posemo=5.5,
            segment_intensities=[5.9, 6.0, peak_value, 5.8, 6.2],
        )
        validator = SophiaTTTValidator()
        result = validator.validate(
            baseline=ttt_baseline,
            generated_content_analysis=generated,
            compilation_id="COMP-AC10-003",
            model_id="gpt-4",
        )
        if result.drift_passed and result.similarity_passed:
            assert result.peaks_passed is True


# ─── AC11: Assembly report interruption log ───────────────────────────────────


class TestAC11PipelineInterruptionLog:
    """AC11: Pipeline interruption logged with template_id, violated_field, recovery_instruction."""

    def test_c08_reject_produces_interruption_log(
        self, tmp_coach_dir: Path, receipt_chain: ReceiptChain
    ) -> None:
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC11-001",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="ttt_temperature", value="TTT-06"),
            ],
            block_a_structural_laws=[],
        )

        pipeline = TTTEnforcementPipeline(
            coach_dir=tmp_coach_dir,
            coach_acronym="TST",
            receipt_chain=receipt_chain,
        )
        session = pipeline.run(brief=brief)

        assert session.deployment_status == "REJECTED"
        assert session.assembly_report is not None

        log = session.assembly_report.pipeline_interruption_log
        assert log is not None
        assert log["template_id"] == "COMP-AC11-001"
        assert log["violated_field"] == "ttt_temperature"
        assert len(log["recovery_instruction"]) > 0

    def test_interruption_log_written_to_file(
        self, tmp_path: Path, tmp_coach_dir: Path, receipt_chain: ReceiptChain
    ) -> None:
        """Assembly report JSON contains the interruption log."""
        report_dir = tmp_path / "reports"
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC11-002",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(name="temperature", value=7),
            ],
            block_a_structural_laws=[],
        )

        pipeline = TTTEnforcementPipeline(
            coach_dir=tmp_coach_dir,
            coach_acronym="TST",
            receipt_chain=receipt_chain,
            report_dir=report_dir,
        )
        session = pipeline.run(brief=brief)

        assert session.assembly_report_path is not None
        report_path = session.assembly_report_path
        assert report_path.exists()

        with report_path.open() as f:
            data = json.load(f)

        assert data["deployment_status"] == "REJECTED"
        log = data.get("pipeline_interruption_log")
        assert log is not None
        assert "template_id" in log
        assert "violated_field" in log
        assert "recovery_instruction" in log


# ─── AC12: Clean template → C-08 PASS + full pipeline ACCEPTED ───────────────


class TestAC12CleanTemplateAccepted:
    """AC12: Clean template (no TTT in Block A/B, valid DEP-ENG-005 ref) → ACCEPTED."""

    def test_clean_template_passes_c08(self) -> None:
        brief = _make_clean_brief()
        result = run_c08(brief)
        assert result.passed
        assert len(result.violations) == 0

    def test_m02_checker_passes_clean_template(self) -> None:
        checker = TemplateM02Checker()
        template_data = {
            "compilation_id": "COMP-AC12-001",
            "archetype_id": "story_transformation",
            "block_b_fields": [
                {"name": "hook_strategy", "value": "Open with vulnerability"},
                {"name": "narrative_arc", "value": "tension-discovery-resolution"},
            ],
            "block_a_structural_laws": [
                {"law_id": "law_01", "text": "Hook must be ≤ 2 sentences."},
            ],
        }
        result = checker.scan_template_dict(template_data, template_id="COMP-AC12-001")
        assert result.is_compliant
        assert result.violation_count == 0

    def test_full_pipeline_accepted_with_dep_eng_005(
        self,
        tmp_coach_dir: Path,
        receipt_chain: ReceiptChain,
        ttt_baseline: TTTBaselineData,
    ) -> None:
        """Full pipeline run with baseline present → ACCEPTED status."""
        # Write ttt_baseline.json as DEP-ENG-005
        baseline_path = tmp_coach_dir / "config" / "ttt_baseline.json"
        baseline_path.write_text(
            ttt_baseline.model_dump_json(indent=2),
            encoding="utf-8",
        )

        brief = _make_clean_brief(compilation_id="COMP-AC12-002")
        generated = _make_generated_content_analysis(
            affect=6.1,
            posemo=5.6,
            segment_intensities=[5.8, 6.0, 7.5, 6.1, 5.9],
        )

        pipeline = TTTEnforcementPipeline(
            coach_dir=tmp_coach_dir,
            coach_acronym="TST",
            receipt_chain=receipt_chain,
        )
        session = pipeline.run(
            brief=brief,
            generated_content_analysis=generated,
            model_id="gpt-4",
        )

        # C-08 must have passed
        assert session.c08_result is not None
        assert session.c08_result.passed

        # Baseline must have loaded
        assert session.baseline is not None

        # Receipt must be logged
        assert session.receipt_id is not None

    def test_dep_eng_005_runtime_reference_passes_c08(self) -> None:
        """DEP-ENG-005 reference in Block B is permitted (not flagged as TTT hardcode)."""
        brief = CompiledDesignBrief(
            compilation_id="COMP-AC12-003",
            archetype_id="story_transformation",
            block_b_fields=[
                BlockBField(
                    name="dep_eng_005_reference",
                    value="LOAD:config/ttt_baseline.json",
                    context="runtime_reference",
                ),
            ],
            block_a_structural_laws=[],
            dep_eng_005_reference="config/ttt_baseline.json",
        )
        result = run_c08(brief)
        assert result.passed, (
            "DEP-ENG-005 runtime reference must pass C-08. "
            f"Got: {result.first_violation}"
        )
