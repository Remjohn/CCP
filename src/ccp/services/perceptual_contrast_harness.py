"""
FR-ERA3-28 - Perceptual Contrast Harness.

Deterministic mutation and adversarial probe execution over the typed
perceptual failure corpus, with FR-27 evaluator interop and receipt logging.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.perceptual_failure_corpus_models import (
    EvaluatorExpectationBundle,
    MutationOperatorKind,
    PerceptualContrastCaseRecord,
    PerceptualFailureClass,
    PerceptualFailureHarnessReport,
    PerceptualHarnessDecision,
    PerceptualHarnessProbeRequest,
    PerceptualHarnessProbeResult,
    PerceptualMutationOperation,
    PerceptualMutationSuite,
    PerceptualExpectationStatus,
    PerceptualSurfaceClass,
)
from src.ccp.models.perceptual_influence_models import (
    FalseDepthClass,
    PerceptualInfluenceDecision,
    PerceptualInfluenceDomain,
    PerceptualInfluenceEvaluatorResult,
    PerceptualInfluenceRequest,
    PerceptualInfluenceSurface,
)
from src.ccp.services.hard_negative_adapter import HardNegativeAdapter
from src.ccp.services.perceptual_failure_corpus_service import PerceptualFailureCorpusService
from src.ccp.services.perceptual_influence_evaluator import PerceptualInfluenceEvaluator
from src.ccp.services.sfl_registry_service import SFLRegistryService


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


class PerceptualFailureDecisionRouter:
    """Translates expectation/evaluator mismatch into harness-level decisions."""

    PRIORITY = {
        PerceptualHarnessDecision.ERROR: 6,
        PerceptualHarnessDecision.INVALID: 5,
        PerceptualHarnessDecision.BLOCK: 4,
        PerceptualHarnessDecision.DOWNGRADE: 3,
        PerceptualHarnessDecision.REVIEW: 2,
        PerceptualHarnessDecision.PASS: 1,
    }

    def combine(self, results: list[PerceptualHarnessProbeResult]) -> PerceptualHarnessDecision:
        if not results:
            return PerceptualHarnessDecision.INVALID
        return max(results, key=lambda item: self.PRIORITY[item.observed_decision]).observed_decision

    def route(
        self,
        *,
        expectation: EvaluatorExpectationBundle,
        surface_class: PerceptualSurfaceClass,
        evaluator_decision: PerceptualInfluenceDecision,
        thresholds_met: bool,
    ) -> tuple[PerceptualHarnessDecision, bool, list[str]]:
        warnings: list[str] = []
        expected = expectation.expected_status

        if expected == PerceptualExpectationStatus.EXPECT_BLOCK:
            if surface_class in expectation.route_block_surfaces:
                if evaluator_decision == PerceptualInfluenceDecision.DOWNGRADE:
                    if thresholds_met:
                        return PerceptualHarnessDecision.PASS, True, warnings
                    warnings.append("Evaluator downgraded a block-surface failure but did not produce the required metric shifts.")
                    return PerceptualHarnessDecision.BLOCK, False, warnings
                warnings.append("Evaluator under-reacted on a block-surface perceptual failure.")
                return PerceptualHarnessDecision.BLOCK, False, warnings
            if evaluator_decision == PerceptualInfluenceDecision.DOWNGRADE:
                if thresholds_met:
                    return PerceptualHarnessDecision.PASS, True, warnings
                warnings.append("Evaluator downgraded the failure but did not reach the expected metric deltas.")
                return PerceptualHarnessDecision.DOWNGRADE, False, warnings
            warnings.append("Evaluator missed downgrade behavior for block-class failure outside strict block surfaces.")
            return PerceptualHarnessDecision.DOWNGRADE, False, warnings

        if expected == PerceptualExpectationStatus.EXPECT_DOWNGRADE:
            if evaluator_decision == PerceptualInfluenceDecision.DOWNGRADE:
                if thresholds_met:
                    return PerceptualHarnessDecision.PASS, True, warnings
                warnings.append("Evaluator downgraded the probe but did not meet the expected metric-delta floor.")
                return PerceptualHarnessDecision.DOWNGRADE, False, warnings
            if evaluator_decision == PerceptualInfluenceDecision.REVIEW:
                warnings.append("Evaluator returned REVIEW where downgrade pressure was expected.")
                return PerceptualHarnessDecision.DOWNGRADE, False, warnings
            if evaluator_decision == PerceptualInfluenceDecision.PASS:
                warnings.append("Evaluator passed a probe that should at least downgrade.")
                return PerceptualHarnessDecision.DOWNGRADE, False, warnings

        if expected == PerceptualExpectationStatus.EXPECT_REVIEW:
            if evaluator_decision == PerceptualInfluenceDecision.REVIEW:
                if thresholds_met:
                    return PerceptualHarnessDecision.PASS, True, warnings
                warnings.append("Evaluator surfaced review pressure but did not reach the expected metric-delta floor.")
                return PerceptualHarnessDecision.REVIEW, False, warnings
            if evaluator_decision == PerceptualInfluenceDecision.DOWNGRADE:
                warnings.append("Evaluator over-reacted by downgrading a review-target failure.")
                return PerceptualHarnessDecision.REVIEW, False, warnings
            warnings.append("Evaluator passed a probe that should have surfaced review pressure.")
            return PerceptualHarnessDecision.DOWNGRADE, False, warnings

        if expected == PerceptualExpectationStatus.EXPECT_WARNING:
            if evaluator_decision in {PerceptualInfluenceDecision.REVIEW, PerceptualInfluenceDecision.DOWNGRADE}:
                warnings.append("Evaluator reacted more strongly than the warning-tier expectation.")
                return PerceptualHarnessDecision.REVIEW, False, warnings
            return PerceptualHarnessDecision.PASS, True, warnings

        warnings.append("Unknown expectation state encountered.")
        return PerceptualHarnessDecision.ERROR, False, warnings


class PerceptualContrastHarness:
    """Runs FR-28 corpus probes against the FR-27 perceptual evaluator."""

    def __init__(
        self,
        *,
        corpus_service: PerceptualFailureCorpusService | None = None,
        evaluator: PerceptualInfluenceEvaluator | None = None,
        receipt_chain: ReceiptChain | None = None,
        hard_negative_adapter: HardNegativeAdapter | None = None,
    ) -> None:
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym="PFC")
        self.corpus_service = corpus_service or PerceptualFailureCorpusService(receipt_chain=self.receipt_chain)
        if evaluator is None:
            sfl_registry = SFLRegistryService(receipt_chain=self.receipt_chain)
            sfl_registry.warm(allow_degraded_dev_mode=False)
            evaluator = PerceptualInfluenceEvaluator(
                sfl_registry=sfl_registry,
                receipt_chain=self.receipt_chain,
            )
        self.evaluator = evaluator
        self.hard_negative_adapter = hard_negative_adapter or HardNegativeAdapter()
        self.router = PerceptualFailureDecisionRouter()

    def run_case_probe(self, request: PerceptualHarnessProbeRequest) -> PerceptualFailureHarnessReport:
        receipt_ids: list[str] = []
        results: list[PerceptualHarnessProbeResult] = []

        if not self.corpus_service.cases:
            self.corpus_service.warm()

        invalid_decision = self._validate_semantic_prerequisite(request)
        if invalid_decision is not None:
            report = self._invalid_report(request, invalid_decision)
            receipt_ids.extend(self._log_report_receipt(report, action="perceptual-failure-probe-run"))
            report.receipt_ids = receipt_ids
            return report

        cases = self._resolve_cases(request)
        suites = self._resolve_suites(request, cases)

        for case in cases:
            result = self._probe_case(case=case, request=request)
            results.append(result)

        if request.evaluate_mutations:
            for suite in suites:
                for operation in suite.operations:
                    result = self._probe_operation(
                        request=request,
                        suite=suite,
                        operation=operation,
                        anchor_text=request.candidate_text,
                    )
                    results.append(result)

        overall_decision = self.router.combine(results)
        report = PerceptualFailureHarnessReport(
            report_id=_id("PFR"),
            evaluated_at=datetime.now(timezone.utc),
            request=request,
            resolved_case_ids=[case.case_id for case in cases],
            resolved_suite_ids=[suite.suite_id for suite in suites],
            decision=overall_decision,
            results=results,
            summary=self._build_summary(results, overall_decision),
            metadata={
                "surface_class": request.surface_class.value,
                "resolved_case_ids": [case.case_id for case in cases],
                "resolved_suite_ids": [suite.suite_id for suite in suites],
                "expected_statuses": [result.expected_status.value for result in results if result.expected_status is not None],
                "observed_decisions": [result.observed_decision.value for result in results],
                "semantic_interop_hits": sorted(
                    {
                        hit
                        for case in cases
                        for hit in case.semantic_interop.linked_hard_negative_ids
                    }
                ),
                "mismatch_count": sum(1 for result in results if not result.decision_match),
                "rolled_back": False,
            },
        )
        receipt_ids.extend(self._log_report_receipt(report, action="perceptual-failure-probe-run"))
        report.receipt_ids = receipt_ids
        return report

    def run_mutation_suite(
        self,
        case_id: str,
        suite_id: str,
        surface_class: PerceptualSurfaceClass,
    ) -> PerceptualFailureHarnessReport:
        case = self.corpus_service.get_case(case_id)
        suite = self.corpus_service.get_suite(suite_id)
        if case is None or suite is None:
            request = PerceptualHarnessProbeRequest(
                probe_id=_id("PFP"),
                candidate_text=case.failing_variant_excerpt if case else "missing case or suite prevents mutation execution.",
                surface_class=surface_class,
                case_ids=[case_id] if case else [],
                suite_ids=[suite_id] if suite else [],
                evaluate_mutations=True,
                metadata={},
            )
            report = self._invalid_report(request, "Missing case or suite for mutation execution.")
            report.receipt_ids.extend(self._log_report_receipt(report, action="perceptual-failure-suite-run"))
            return report

        request = PerceptualHarnessProbeRequest(
            probe_id=_id("PFP"),
            candidate_text=case.valid_anchor_excerpt,
            surface_class=surface_class,
            case_ids=[case_id],
            suite_ids=[suite_id],
            evaluate_mutations=True,
            metadata={},
        )
        results = [
            self._probe_operation(
                request=request,
                suite=suite,
                operation=operation,
                anchor_text=case.valid_anchor_excerpt,
            )
            for operation in suite.operations
        ]
        decision = self.router.combine(results)
        report = PerceptualFailureHarnessReport(
            report_id=_id("PFR"),
            evaluated_at=datetime.now(timezone.utc),
            request=request,
            resolved_case_ids=[case.case_id],
            resolved_suite_ids=[suite.suite_id],
            decision=decision,
            results=results,
            summary=self._build_summary(results, decision),
            metadata={
                "surface_class": surface_class.value,
                "resolved_case_ids": [case.case_id],
                "resolved_suite_ids": [suite.suite_id],
                "expected_statuses": [suite.expectation_bundle.expected_status.value] * len(results),
                "observed_decisions": [result.observed_decision.value for result in results],
                "semantic_interop_hits": case.semantic_interop.linked_hard_negative_ids,
                "mismatch_count": sum(1 for result in results if not result.decision_match),
                "rolled_back": False,
            },
        )
        report.receipt_ids.extend(self._log_report_receipt(report, action="perceptual-failure-suite-run"))
        return report

    def materialize_mutation(self, base_text: str, operation: PerceptualMutationOperation) -> str:
        mutated = base_text.strip()
        if operation.kind == MutationOperatorKind.OVER_SMOOTHING:
            mutated = re.sub(r"[!?]+", ".", mutated)
            mutated = mutated.replace("—", ", ").replace("...", ". ")
            mutated = f"It is important to remember that {mutated[0].lower() + mutated[1:]}" if mutated else mutated
        elif operation.kind == MutationOperatorKind.IMPLICATION_STRIPPING:
            mutated = self._flatten_symbolic_terms(mutated)
            mutated = (
                f"{mutated} This means that the point is fully explicit. "
                "In other words, there is no implied layer left for the audience to discover."
            )
        elif operation.kind == MutationOperatorKind.SYMBOLIC_FLATTENING:
            mutated = self._flatten_symbolic_terms(mutated)
        elif operation.kind == MutationOperatorKind.RHYTHM_NORMALIZATION:
            sentences = [segment.strip() for segment in re.split(r"[.!?]+", mutated) if segment.strip()]
            normalized = []
            for sentence in sentences:
                words = sentence.split()
                if len(words) > 12:
                    words = words[:12]
                normalized.append(" ".join(words))
            mutated = ". ".join(normalized) + "."
        elif operation.kind == MutationOperatorKind.PROOF_INFLATION:
            mutated = (
                f"{mutated} Hundreds of elite clients, premium founders, and top-tier operators already validate this proven methodology with scientific proof and guaranteed success."
            )
        elif operation.kind == MutationOperatorKind.PRESTIGE_THEATER_INJECTION:
            mutated = (
                f"{mutated} As an expert, I can say the result is world-class, premium, iconic, and worthy of cinematic admiration."
            )
        elif operation.kind == MutationOperatorKind.MOTIVATIONAL_SOFTENING:
            mutated = mutated.replace("must", "can").replace("truth", "possibility").replace("need to", "might want to")
            mutated = (
                f"{mutated} Everyone is on their own journey, so the main thing is to believe in yourself, keep going, and never give up."
            )
        elif operation.kind == MutationOperatorKind.PAUSE_WEIGHT_REMOVAL:
            mutated = re.sub(r"\s+", " ", mutated.replace("...", " ").replace("—", " ").replace("\n", " ")).strip()
        return mutated

    def _probe_case(
        self,
        *,
        case: PerceptualContrastCaseRecord,
        request: PerceptualHarnessProbeRequest,
    ) -> PerceptualHarnessProbeResult:
        anchor_eval = self._evaluate_text(case.valid_anchor_excerpt, request.surface_class, request.metadata)
        failing_eval = self._evaluate_text(case.failing_variant_excerpt, request.surface_class, request.metadata)
        semantic_hits = self._evaluate_semantic_interop(case)
        return self.compare_to_expectation(
            expected=case.expectation_bundle,
            observed=failing_eval,
            anchor=anchor_eval,
            surface_class=request.surface_class,
            case_id=case.case_id,
            semantic_interop_hits=semantic_hits,
            suite_id=None,
            operation_id=None,
        )

    def _probe_operation(
        self,
        *,
        request: PerceptualHarnessProbeRequest,
        suite: PerceptualMutationSuite,
        operation: PerceptualMutationOperation,
        anchor_text: str,
    ) -> PerceptualHarnessProbeResult:
        mutated_text = self.materialize_mutation(anchor_text, operation)
        anchor_eval = self._evaluate_text(anchor_text, request.surface_class, request.metadata)
        mutated_eval = self._evaluate_text(mutated_text, request.surface_class, request.metadata)
        return self.compare_to_expectation(
            expected=suite.expectation_bundle,
            observed=mutated_eval,
            anchor=anchor_eval,
            surface_class=request.surface_class,
            case_id=None,
            semantic_interop_hits=[],
            suite_id=suite.suite_id,
            operation_id=operation.operation_id,
        )

    def compare_to_expectation(
        self,
        *,
        expected: EvaluatorExpectationBundle,
        observed: PerceptualInfluenceEvaluatorResult,
        anchor: PerceptualInfluenceEvaluatorResult,
        surface_class: PerceptualSurfaceClass,
        case_id: str | None,
        semantic_interop_hits: list[str],
        suite_id: str | None,
        operation_id: str | None,
    ) -> PerceptualHarnessProbeResult:
        deltas = self._metric_deltas(anchor, observed)
        thresholds_met = (
            deltas["human_drop"] >= expected.minimum_human_congruence_drop
            and deltas["memorability_drop"] >= expected.minimum_memorability_drop
            and deltas["symbolic_drop"] >= expected.minimum_symbolic_density_drop
            and deltas["contrast_drop"] >= expected.minimum_contrast_clarity_drop
            and deltas["overexplanation_rise"] >= expected.minimum_overexplanation_risk_rise
            and deltas["synthetic_rise"] >= expected.minimum_synthetic_smoothness_rise
        )
        decision, decision_match, warnings = self.router.route(
            expectation=expected,
            surface_class=surface_class,
            evaluator_decision=observed.report.decision_summary.decision,
            thresholds_met=thresholds_met,
        )

        false_depth_classes = [detected.value for detected in observed.report.false_depth_result.detected_classes]
        evidence = {
            "anchor_report_id": anchor.report.report_id,
            "observed_report_id": observed.report.report_id,
            "evaluator_decision": observed.report.decision_summary.decision.value,
            "false_depth_classes": false_depth_classes,
            "metric_deltas": deltas,
            "thresholds_met": thresholds_met,
            "semantic_interop_hits": semantic_interop_hits,
        }
        remediation = list(observed.report.decision_summary.required_corrections)
        if not decision_match and not remediation:
            remediation.append("Tighten evaluator policy or mutation thresholds for this perceptual failure class.")

        return PerceptualHarnessProbeResult(
            probe_id=_id("PFP"),
            case_id=case_id,
            suite_id=suite_id,
            operation_id=operation_id,
            expected_status=expected.expected_status,
            observed_decision=decision,
            decision_match=decision_match,
            evidence=evidence,
            warnings=warnings,
            remediation=remediation,
        )

    def _evaluate_text(
        self,
        text: str,
        surface_class: PerceptualSurfaceClass,
        metadata: dict[str, Any],
    ) -> PerceptualInfluenceEvaluatorResult:
        domain, mapped_surface = self._map_surface(surface_class)
        request = PerceptualInfluenceRequest(
            request_id=_id("PIR"),
            domain=domain,
            surface_class=mapped_surface,
            actor_id=str(metadata.get("actor_id", "fr28-harness")),
            coach_id=str(metadata.get("coach_id", "FR28")),
            candidate_text=text,
            directional_integrity_report_id=metadata.get("directional_integrity_report_id"),
            directional_integrity_decision=metadata.get("directional_integrity_decision", "PASS"),
            content_archetype_id=metadata.get("content_archetype_id"),
            representation_geometry_id=metadata.get("representation_geometry_id"),
        )
        return self.evaluator.evaluate(request)

    def _metric_deltas(
        self,
        anchor: PerceptualInfluenceEvaluatorResult,
        observed: PerceptualInfluenceEvaluatorResult,
    ) -> dict[str, float]:
        anchor_metrics = anchor.report.metric_bundle
        observed_metrics = observed.report.metric_bundle
        return {
            "human_drop": max(0.0, anchor_metrics.human_congruence_score.score - observed_metrics.human_congruence_score.score),
            "memorability_drop": max(0.0, anchor_metrics.memorability_pressure.score - observed_metrics.memorability_pressure.score),
            "symbolic_drop": max(0.0, anchor_metrics.symbolic_density_score.score - observed_metrics.symbolic_density_score.score),
            "contrast_drop": max(0.0, anchor_metrics.contrast_clarity_score.score - observed_metrics.contrast_clarity_score.score),
            "overexplanation_rise": max(0.0, observed_metrics.overexplanation_risk_score.score - anchor_metrics.overexplanation_risk_score.score),
            "synthetic_rise": max(0.0, observed_metrics.synthetic_smoothness_score.score - anchor_metrics.synthetic_smoothness_score.score),
        }

    def _evaluate_semantic_interop(self, case: PerceptualContrastCaseRecord) -> list[str]:
        if not case.semantic_interop.linked_hard_negative_ids:
            return []
        geometry_id = case.semantic_interop.linked_geometry_ids[0] if case.semantic_interop.linked_geometry_ids else "SDA-RPG-001"
        report = self.hard_negative_adapter.evaluate(
            candidate_text=case.failing_variant_excerpt,
            representation_geometry_id=geometry_id,
        )
        hits = set(case.semantic_interop.linked_hard_negative_ids)
        hits.update(match.hard_negative_id for match in report.top_matches)
        return sorted(hits)

    def _resolve_cases(self, request: PerceptualHarnessProbeRequest) -> list[PerceptualContrastCaseRecord]:
        if request.case_ids:
            cases = [self.corpus_service.get_case(case_id) for case_id in request.case_ids]
            return [case for case in cases if case is not None]
        failure_classes = None
        if request.metadata.get("failure_classes"):
            failure_classes = [PerceptualFailureClass(value) for value in request.metadata["failure_classes"]]
        return self.corpus_service.find_cases(
            surface_class=request.surface_class,
            function_family_ids=request.metadata.get("function_family_ids"),
            archetype_ids=request.metadata.get("archetype_ids"),
            failure_classes=failure_classes,
        )

    def _resolve_suites(
        self,
        request: PerceptualHarnessProbeRequest,
        cases: list[PerceptualContrastCaseRecord],
    ) -> list[PerceptualMutationSuite]:
        if request.suite_ids:
            suites = [self.corpus_service.get_suite(suite_id) for suite_id in request.suite_ids]
            return [suite for suite in suites if suite is not None]
        suite_ids = {suite_id for case in cases for suite_id in case.mutation_suite_ids}
        return [suite for suite_id in sorted(suite_ids) if (suite := self.corpus_service.get_suite(suite_id)) is not None]

    def _validate_semantic_prerequisite(self, request: PerceptualHarnessProbeRequest) -> str | None:
        di_decision = str(request.metadata.get("directional_integrity_decision", "PASS")).upper()
        if di_decision not in {"PASS", "REVIEW"}:
            return f"Invalid directional integrity prerequisite for FR-28 probe: {di_decision}"
        return None

    def _invalid_report(self, request: PerceptualHarnessProbeRequest, reason: str) -> PerceptualFailureHarnessReport:
        return PerceptualFailureHarnessReport(
            report_id=_id("PFR"),
            evaluated_at=datetime.now(timezone.utc),
            request=request,
            resolved_case_ids=[],
            resolved_suite_ids=[],
            decision=PerceptualHarnessDecision.INVALID,
            results=[
                PerceptualHarnessProbeResult(
                    probe_id=request.probe_id,
                    expected_status=None,
                    observed_decision=PerceptualHarnessDecision.INVALID,
                    decision_match=False,
                    evidence={"reason": reason},
                    warnings=[reason],
                    remediation=["Provide a PASS or REVIEW directional integrity prerequisite before running the perceptual harness."],
                )
            ],
            summary=reason,
            metadata={
                "surface_class": request.surface_class.value,
                "resolved_case_ids": [],
                "resolved_suite_ids": [],
                "expected_statuses": [],
                "observed_decisions": [PerceptualHarnessDecision.INVALID.value],
                "semantic_interop_hits": [],
                "mismatch_count": 1,
                "rolled_back": False,
            },
        )

    def _map_surface(
        self,
        surface_class: PerceptualSurfaceClass,
    ) -> tuple[PerceptualInfluenceDomain, PerceptualInfluenceSurface]:
        mapping = {
            PerceptualSurfaceClass.SEMANTIC_PLANNING: (
                PerceptualInfluenceDomain.CCF,
                PerceptualInfluenceSurface.SEMANTIC_PLANNING,
            ),
            PerceptualSurfaceClass.RENDER_RELEASE: (
                PerceptualInfluenceDomain.CMF,
                PerceptualInfluenceSurface.RENDER_RELEASE,
            ),
            PerceptualSurfaceClass.COACHING_INTERVENTION: (
                PerceptualInfluenceDomain.CBCS,
                PerceptualInfluenceSurface.COACHING_INTERVENTION,
            ),
            PerceptualSurfaceClass.SOCIAL_REACTION: (
                PerceptualInfluenceDomain.REACTIONS,
                PerceptualInfluenceSurface.SOCIAL_SHARE,
            ),
            PerceptualSurfaceClass.LONG_FORM_AUTHORITY: (
                PerceptualInfluenceDomain.WEBINAR,
                PerceptualInfluenceSurface.RENDER_RELEASE,
            ),
            PerceptualSurfaceClass.COMMERCIAL_TRUST_TRANSFER: (
                PerceptualInfluenceDomain.COMMERCIAL,
                PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
            ),
            PerceptualSurfaceClass.PHASE0_AUDIT_PROOF: (
                PerceptualInfluenceDomain.COMMERCIAL,
                PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
            ),
        }
        return mapping[surface_class]

    def _build_summary(
        self,
        results: list[PerceptualHarnessProbeResult],
        decision: PerceptualHarnessDecision,
    ) -> str:
        mismatches = sum(1 for result in results if not result.decision_match)
        return (
            f"FR-ERA3-28 probe completed with {len(results)} result(s), "
            f"{mismatches} mismatch(es), and final harness decision {decision.value}."
        )

    def _log_report_receipt(
        self,
        report: PerceptualFailureHarnessReport,
        *,
        action: str,
    ) -> list[str]:
        entry = self.receipt_chain.log(
            agent_id="perceptual-contrast-harness",
            action=action,
            asset_id=report.report_id,
            input_summary=f"FR-ERA3-28 probe on {report.request.surface_class.value}",
            output_summary=report.summary,
            decision=report.decision.value.lower(),
            metadata=report.metadata,
        )
        return [entry.receipt_id]

    def _flatten_symbolic_terms(self, text: str) -> str:
        replacements = {
            "bridge": "idea",
            "mirror": "example",
            "lens": "perspective",
            "resonance": "consistency",
            "rhythm": "pattern",
            "anchor": "point",
            "symbol": "detail",
            "metaphor": "comparison",
            "crusade": "plan",
            "manifesto": "message",
        }
        flattened = text
        for original, replacement in replacements.items():
            flattened = re.sub(rf"\b{re.escape(original)}\b", replacement, flattened, flags=re.IGNORECASE)
        return flattened
