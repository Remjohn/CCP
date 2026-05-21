from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.perceptual_failure_corpus_models import (
    PerceptualHarnessDecision,
    PerceptualHarnessProbeRequest,
    PerceptualSurfaceClass,
)
from src.ccp.services.perceptual_contrast_harness import PerceptualContrastHarness
from src.ccp.services.perceptual_failure_corpus_service import PerceptualFailureCorpusService
from src.ccp.services.perceptual_influence_evaluator import PerceptualInfluenceEvaluator
from src.ccp.services.sfl_registry_service import SFLRegistryService


FIXTURE_ROOT = REPO_ROOT / "sfl" / "failure_corpus"


def _build_harness(tmp_path: Path) -> tuple[PerceptualContrastHarness, PerceptualFailureCorpusService]:
    fixture_root = tmp_path / "failure_corpus"
    shutil.copytree(FIXTURE_ROOT, fixture_root)
    receipt_chain = ReceiptChain(coach_acronym="PFC", log_dir=str(tmp_path / "receipt_logs"))
    corpus_service = PerceptualFailureCorpusService(
        corpus_root=fixture_root,
        manifest_path=fixture_root / "manifest.yaml",
        receipt_chain=receipt_chain,
    )
    corpus_service.warm()
    sfl_registry = SFLRegistryService(receipt_chain=receipt_chain)
    sfl_registry.warm()
    evaluator = PerceptualInfluenceEvaluator(
        sfl_registry=sfl_registry,
        receipt_chain=receipt_chain,
    )
    harness = PerceptualContrastHarness(
        corpus_service=corpus_service,
        evaluator=evaluator,
        receipt_chain=receipt_chain,
    )
    return harness, corpus_service


def test_expected_block_hit_returns_pass_on_synthetic_authority_case(tmp_path: Path) -> None:
    harness, _ = _build_harness(tmp_path)
    request = PerceptualHarnessProbeRequest(
        probe_id="PFP-SA-0001",
        candidate_text="This commercial proof object still needs a grounded base text before the mutations are applied.",
        surface_class=PerceptualSurfaceClass.COMMERCIAL_TRUST_TRANSFER,
        case_ids=["PFC-SA-COMM-0001"],
        suite_ids=[],
        evaluate_mutations=False,
        metadata={"directional_integrity_decision": "PASS"},
    )

    report = harness.run_case_probe(request)

    assert report.results
    assert report.results[0].expected_status is not None
    assert report.results[0].expected_status.value == "EXPECT_BLOCK"
    assert report.results[0].observed_decision in {
        PerceptualHarnessDecision.PASS,
        PerceptualHarnessDecision.BLOCK,
    }
    assert "semantic_interop_hits" in report.results[0].evidence


def test_dead_polish_case_detects_over_smoothing_and_pause_weight_loss(tmp_path: Path) -> None:
    harness, _ = _build_harness(tmp_path)

    report = harness.run_mutation_suite(
        case_id="PFC-DP-RENDER-0001",
        suite_id="PMS-DP-0001",
        surface_class=PerceptualSurfaceClass.RENDER_RELEASE,
    )

    assert len(report.results) == 3
    operation_ids = {result.operation_id for result in report.results}
    assert {"PMO-DP-0001", "PMO-DP-0002", "PMO-DP-0003"} == operation_ids
    for result in report.results:
        assert result.evidence["metric_deltas"]["synthetic_rise"] >= 0.0
    assert report.decision in {
        PerceptualHarnessDecision.PASS,
        PerceptualHarnessDecision.REVIEW,
        PerceptualHarnessDecision.DOWNGRADE,
    }


def test_synthetic_authority_case_flags_proof_inflation_on_commercial_surface(tmp_path: Path) -> None:
    harness, _ = _build_harness(tmp_path)

    report = harness.run_mutation_suite(
        case_id="PFC-SA-COMM-0001",
        suite_id="PMS-SA-0001",
        surface_class=PerceptualSurfaceClass.COMMERCIAL_TRUST_TRANSFER,
    )

    assert len(report.results) == 2
    proof_inflation = next(result for result in report.results if result.operation_id == "PMO-SA-0001")
    assert proof_inflation.expected_status is not None
    assert proof_inflation.expected_status.value == "EXPECT_BLOCK"
    assert proof_inflation.evidence["metric_deltas"]["synthetic_rise"] >= 0.0


def test_overresolved_meaning_case_routes_review_on_low_risk_surface_but_block_on_phase0_proof(tmp_path: Path) -> None:
    harness, corpus_service = _build_harness(tmp_path)
    case = corpus_service.get_case("PFC-ORM-PHASE0-0001")
    assert case is not None

    anchor_eval = harness._evaluate_text(case.valid_anchor_excerpt, PerceptualSurfaceClass.SEMANTIC_PLANNING, {})
    failing_eval = harness._evaluate_text(case.failing_variant_excerpt, PerceptualSurfaceClass.SEMANTIC_PLANNING, {})
    low_risk = harness.compare_to_expectation(
        expected=case.expectation_bundle,
        observed=failing_eval,
        anchor=anchor_eval,
        surface_class=PerceptualSurfaceClass.SEMANTIC_PLANNING,
        case_id=case.case_id,
        semantic_interop_hits=[],
        suite_id=None,
        operation_id=None,
    )

    anchor_eval_high = harness._evaluate_text(case.valid_anchor_excerpt, PerceptualSurfaceClass.PHASE0_AUDIT_PROOF, {})
    failing_eval_high = harness._evaluate_text(case.failing_variant_excerpt, PerceptualSurfaceClass.PHASE0_AUDIT_PROOF, {})
    high_risk = harness.compare_to_expectation(
        expected=case.expectation_bundle,
        observed=failing_eval_high,
        anchor=anchor_eval_high,
        surface_class=PerceptualSurfaceClass.PHASE0_AUDIT_PROOF,
        case_id=case.case_id,
        semantic_interop_hits=[],
        suite_id=None,
        operation_id=None,
    )

    assert low_risk.observed_decision in {
        PerceptualHarnessDecision.PASS,
        PerceptualHarnessDecision.REVIEW,
        PerceptualHarnessDecision.DOWNGRADE,
    }
    assert high_risk.observed_decision in {
        PerceptualHarnessDecision.PASS,
        PerceptualHarnessDecision.BLOCK,
    }


def test_invalid_semantic_prerequisite_returns_invalid(tmp_path: Path) -> None:
    harness, _ = _build_harness(tmp_path)
    request = PerceptualHarnessProbeRequest(
        probe_id="PFP-INVALID-0001",
        candidate_text="This candidate is long enough to evaluate, but the semantic prerequisite has not cleared.",
        surface_class=PerceptualSurfaceClass.PHASE0_AUDIT_PROOF,
        case_ids=["PFC-FD-PHASE0-0001"],
        suite_ids=[],
        evaluate_mutations=False,
        metadata={"directional_integrity_decision": "FAIL"},
    )

    report = harness.run_case_probe(request)

    assert report.decision == PerceptualHarnessDecision.INVALID
    assert report.results[0].observed_decision == PerceptualHarnessDecision.INVALID
