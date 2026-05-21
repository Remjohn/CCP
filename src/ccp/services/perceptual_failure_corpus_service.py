"""
FR-ERA3-28 - Perceptual Failure Corpus Service.

Manifest-driven loader for typed perceptual failure cases and mutation suites,
with failure-closed reload behavior and explicit receipt-chain logging.
"""

from __future__ import annotations

import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.perceptual_failure_corpus_models import (
    CASE_CLASS_BY_FAILURE,
    CASE_DIRECTORY_BY_FAILURE,
    PerceptualContrastCaseRecord,
    PerceptualFailureClass,
    PerceptualFailureCorpusManifest,
    PerceptualMutationSuite,
    PerceptualSurfaceClass,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CORPUS_ROOT = REPO_ROOT / "sfl" / "failure_corpus"
DEFAULT_MANIFEST_PATH = DEFAULT_CORPUS_ROOT / "manifest.yaml"

CASE_DIRECTORIES = frozenset(CASE_DIRECTORY_BY_FAILURE.values())
SUITE_DIRECTORY = "mutation_suites"


class PerceptualFailureCorpusService:
    """Typed corpus loader for FR-ERA3-28 perceptual failure assets."""

    def __init__(
        self,
        *,
        corpus_root: Path | None = None,
        manifest_path: Path | None = None,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        coach_acronym = os.getenv("COACH_ACRONYM", "PFC")[:3].upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=coach_acronym,
            log_dir=str(REPO_ROOT / "coaches" / coach_acronym / "logs" / "receipt_chain"),
        )
        self.corpus_root = corpus_root or DEFAULT_CORPUS_ROOT
        self.manifest_path = manifest_path or DEFAULT_MANIFEST_PATH

        self.manifest: PerceptualFailureCorpusManifest | None = None
        self.cases: dict[str, PerceptualContrastCaseRecord] = {}
        self.suites: dict[str, PerceptualMutationSuite] = {}

    def warm(self) -> PerceptualFailureCorpusManifest:
        snapshot = self._snapshot()
        try:
            manifest, cases, suites = self._load_all()
        except Exception as exc:
            self._restore(snapshot)
            self._log_receipt(
                action="perceptual-failure-corpus-warm",
                decision="rejected",
                metadata={
                    "surface_class": "N/A",
                    "resolved_case_ids": [],
                    "resolved_suite_ids": [],
                    "expected_statuses": [],
                    "observed_decisions": [],
                    "semantic_interop_hits": [],
                    "mismatch_count": 0,
                    "rolled_back": snapshot is not None,
                    "error": str(exc),
                },
            )
            raise

        self.manifest = manifest
        self.cases = cases
        self.suites = suites
        self._log_receipt(
            action="perceptual-failure-corpus-warm",
            decision="approved",
            metadata={
                "surface_class": "N/A",
                "resolved_case_ids": sorted(cases.keys()),
                "resolved_suite_ids": sorted(suites.keys()),
                "expected_statuses": [],
                "observed_decisions": [],
                "semantic_interop_hits": self._semantic_interop_hits(cases),
                "mismatch_count": 0,
                "rolled_back": False,
            },
        )
        return manifest

    def reload(
        self,
        case_ids: list[str] | None = None,
        suite_ids: list[str] | None = None,
    ) -> PerceptualFailureCorpusManifest:
        snapshot = self._snapshot()
        if snapshot is None:
            return self.warm()

        try:
            manifest, loaded_cases, loaded_suites = self._load_all()
            next_cases = deepcopy(self.cases)
            next_suites = deepcopy(self.suites)

            requested_case_ids = sorted(set(case_ids or loaded_cases.keys()))
            requested_suite_ids = sorted(set(suite_ids or loaded_suites.keys()))

            for case_id in requested_case_ids:
                if case_id not in loaded_cases:
                    raise ValueError(f"Requested reload case missing from corpus: {case_id}")
                next_cases[case_id] = loaded_cases[case_id]

            for suite_id in requested_suite_ids:
                if suite_id not in loaded_suites:
                    raise ValueError(f"Requested reload suite missing from corpus: {suite_id}")
                next_suites[suite_id] = loaded_suites[suite_id]

            self._validate_case_suite_links(next_cases, next_suites)
            self._validate_manifest_counts(manifest, next_cases, next_suites)

            self.manifest = manifest
            self.cases = next_cases
            self.suites = next_suites
        except Exception as exc:
            self._restore(snapshot)
            self._log_receipt(
                action="perceptual-failure-reload",
                decision="rolled_back",
                metadata={
                    "surface_class": "N/A",
                    "resolved_case_ids": sorted((case_ids or [])),
                    "resolved_suite_ids": sorted((suite_ids or [])),
                    "expected_statuses": [],
                    "observed_decisions": [],
                    "semantic_interop_hits": self._semantic_interop_hits(self.cases),
                    "mismatch_count": 1,
                    "rolled_back": True,
                    "error": str(exc),
                },
            )
            raise

        self._log_receipt(
            action="perceptual-failure-reload",
            decision="approved",
            metadata={
                "surface_class": "N/A",
                "resolved_case_ids": sorted((case_ids or loaded_cases.keys())),
                "resolved_suite_ids": sorted((suite_ids or loaded_suites.keys())),
                "expected_statuses": [],
                "observed_decisions": [],
                "semantic_interop_hits": self._semantic_interop_hits(self.cases),
                "mismatch_count": 0,
                "rolled_back": False,
            },
        )
        return self.manifest

    def get_case(self, case_id: str) -> Optional[PerceptualContrastCaseRecord]:
        case = self.cases.get(case_id)
        self._log_receipt(
            action="perceptual-failure-case-resolve",
            decision="resolved" if case is not None else "missing",
            metadata={
                "surface_class": case.source_surface.value if case else "N/A",
                "resolved_case_ids": [case_id] if case else [],
                "resolved_suite_ids": [],
                "expected_statuses": [case.expectation_bundle.expected_status.value] if case else [],
                "observed_decisions": [],
                "semantic_interop_hits": case.semantic_interop.linked_hard_negative_ids if case else [],
                "mismatch_count": 0,
                "rolled_back": False,
            },
        )
        return case

    def find_cases(
        self,
        surface_class: PerceptualSurfaceClass | None = None,
        function_family_ids: list[str] | None = None,
        archetype_ids: list[str] | None = None,
        failure_classes: list[PerceptualFailureClass] | None = None,
    ) -> list[PerceptualContrastCaseRecord]:
        family_filter = set(function_family_ids or [])
        archetype_filter = set(archetype_ids or [])
        class_filter = set(failure_classes or [])
        found: list[PerceptualContrastCaseRecord] = []
        for case in self.cases.values():
            if surface_class and case.source_surface != surface_class:
                continue
            if class_filter and case.failure_class not in class_filter:
                continue
            if family_filter and not family_filter.intersection(case.source_function_family_ids):
                continue
            if archetype_filter and not archetype_filter.intersection(case.source_archetype_ids):
                continue
            found.append(case)
        return sorted(found, key=lambda item: item.case_id)

    def get_suite(self, suite_id: str) -> Optional[PerceptualMutationSuite]:
        suite = self.suites.get(suite_id)
        self._log_receipt(
            action="perceptual-failure-suite-resolve",
            decision="resolved" if suite is not None else "missing",
            metadata={
                "surface_class": "N/A",
                "resolved_case_ids": [],
                "resolved_suite_ids": [suite_id] if suite else [],
                "expected_statuses": [suite.expectation_bundle.expected_status.value] if suite else [],
                "observed_decisions": [],
                "semantic_interop_hits": [],
                "mismatch_count": 0,
                "rolled_back": False,
            },
        )
        return suite

    def find_suites(
        self,
        target_failure_class: PerceptualFailureClass,
        target_surface: PerceptualSurfaceClass | None = None,
    ) -> list[PerceptualMutationSuite]:
        suites = [
            suite
            for suite in self.suites.values()
            if suite.target_failure_class == target_failure_class
            and (
                not suite.target_surfaces
                or target_surface is None
                or target_surface in suite.target_surfaces
            )
        ]
        return sorted(suites, key=lambda item: item.suite_id)

    def _load_all(
        self,
    ) -> tuple[PerceptualFailureCorpusManifest, dict[str, PerceptualContrastCaseRecord], dict[str, PerceptualMutationSuite]]:
        manifest_payload = self._read_yaml(self.manifest_path)
        if not manifest_payload:
            raise ValueError("Perceptual failure corpus manifest is missing or empty.")

        manifest = PerceptualFailureCorpusManifest.model_validate(manifest_payload)

        resolved_root = (self.corpus_root if self.corpus_root.is_absolute() else (REPO_ROOT / self.corpus_root)).resolve()
        if resolved_root != self.corpus_root.resolve():
            self.corpus_root = resolved_root

        cases: dict[str, PerceptualContrastCaseRecord] = {}
        for failure_class, dirname in CASE_DIRECTORY_BY_FAILURE.items():
            case_dir = self.corpus_root / dirname
            if not case_dir.exists():
                raise ValueError(f"Required case directory missing: {case_dir}")
            for path in sorted(case_dir.glob("*.yaml")):
                case = self._load_case(path, failure_class)
                cases[case.case_id] = case

        suite_dir = self.corpus_root / SUITE_DIRECTORY
        if not suite_dir.exists():
            raise ValueError(f"Required suite directory missing: {suite_dir}")
        suites: dict[str, PerceptualMutationSuite] = {}
        for path in sorted(suite_dir.glob("*.yaml")):
            suite = PerceptualMutationSuite.model_validate(self._read_yaml(path))
            suites[suite.suite_id] = suite

        self._validate_case_suite_links(cases, suites)
        self._validate_manifest_counts(manifest, cases, suites)
        return manifest, cases, suites

    def _load_case(
        self,
        path: Path,
        expected_failure_class: PerceptualFailureClass,
    ) -> PerceptualContrastCaseRecord:
        payload = self._read_yaml(path)
        if not payload:
            raise ValueError(f"Case payload is empty: {path}")
        model_type = CASE_CLASS_BY_FAILURE[expected_failure_class]
        case = model_type.model_validate(payload)
        expected_dir = CASE_DIRECTORY_BY_FAILURE[case.failure_class]
        if path.parent.name != expected_dir:
            raise ValueError(
                f"Case directory/class mismatch for {path.name}: expected directory {expected_dir}, got {path.parent.name}"
            )
        if case.failure_class != expected_failure_class:
            raise ValueError(
                f"Case {case.case_id} declared {case.failure_class.value} but was loaded from {expected_failure_class.value}"
            )
        return case

    def _validate_case_suite_links(
        self,
        cases: dict[str, PerceptualContrastCaseRecord],
        suites: dict[str, PerceptualMutationSuite],
    ) -> None:
        for case in cases.values():
            for suite_id in case.mutation_suite_ids:
                suite = suites.get(suite_id)
                if suite is None:
                    raise ValueError(f"Case {case.case_id} references missing suite {suite_id}")
                if suite.target_failure_class != case.failure_class:
                    raise ValueError(
                        f"Suite {suite_id} targets {suite.target_failure_class.value} but case {case.case_id} is {case.failure_class.value}"
                    )
        for suite in suites.values():
            if not suite.operations:
                raise ValueError(f"Suite {suite.suite_id} must contain at least one mutation operation.")

    def _validate_manifest_counts(
        self,
        manifest: PerceptualFailureCorpusManifest,
        cases: dict[str, PerceptualContrastCaseRecord],
        suites: dict[str, PerceptualMutationSuite],
    ) -> None:
        actual_case_counts = {failure.value: 0 for failure in PerceptualFailureClass}
        for case in cases.values():
            actual_case_counts[case.failure_class.value] += 1
        if manifest.case_counts != actual_case_counts:
            raise ValueError(
                f"Manifest case_counts mismatch. expected={manifest.case_counts} actual={actual_case_counts}"
            )

        actual_suite_counts = {failure.value: 0 for failure in PerceptualFailureClass}
        for suite in suites.values():
            actual_suite_counts[suite.target_failure_class.value] += 1
        if manifest.suite_counts != actual_suite_counts:
            raise ValueError(
                f"Manifest suite_counts mismatch. expected={manifest.suite_counts} actual={actual_suite_counts}"
            )

        maintained_case_ids = sorted(case.case_id for case in cases.values() if case.maintained)
        deprecated_case_ids = sorted(case.case_id for case in cases.values() if not case.maintained)
        if sorted(manifest.maintained_case_ids) != maintained_case_ids:
            raise ValueError("Manifest maintained_case_ids do not match corpus cases.")
        if sorted(manifest.deprecated_case_ids) != deprecated_case_ids:
            raise ValueError("Manifest deprecated_case_ids do not match corpus cases.")

        maintained_suite_ids = sorted(suite.suite_id for suite in suites.values())
        if sorted(manifest.maintained_suite_ids) != maintained_suite_ids:
            raise ValueError("Manifest maintained_suite_ids do not match corpus suites.")
        if manifest.deprecated_suite_ids:
            raise ValueError("Wave-1 corpus does not support deprecated suites yet; manifest.deprecated_suite_ids must be empty.")

    def _read_yaml(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise ValueError(f"Required YAML path missing: {path}")
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle) or {}
        if not isinstance(payload, dict):
            raise ValueError(f"YAML payload must be a mapping: {path}")
        return payload

    def _snapshot(
        self,
    ) -> tuple[
        PerceptualFailureCorpusManifest | None,
        dict[str, PerceptualContrastCaseRecord],
        dict[str, PerceptualMutationSuite],
    ] | None:
        if self.manifest is None and not self.cases and not self.suites:
            return None
        return (
            deepcopy(self.manifest),
            deepcopy(self.cases),
            deepcopy(self.suites),
        )

    def _restore(
        self,
        snapshot: tuple[
            PerceptualFailureCorpusManifest | None,
            dict[str, PerceptualContrastCaseRecord],
            dict[str, PerceptualMutationSuite],
        ]
        | None,
    ) -> None:
        if snapshot is None:
            self.manifest = None
            self.cases = {}
            self.suites = {}
            return
        self.manifest = snapshot[0]
        self.cases = snapshot[1]
        self.suites = snapshot[2]

    def _semantic_interop_hits(self, cases: dict[str, PerceptualContrastCaseRecord]) -> list[str]:
        hits: set[str] = set()
        for case in cases.values():
            hits.update(case.semantic_interop.linked_hard_negative_ids)
        return sorted(hits)

    def _log_receipt(self, *, action: str, decision: str, metadata: dict[str, Any]) -> None:
        self.receipt_chain.log(
            agent_id="perceptual-failure-corpus-service",
            action=action,
            input_summary=f"FR-ERA3-28 corpus action: {action}",
            output_summary=f"Decision: {decision}",
            decision=decision,
            metadata=metadata,
        )

