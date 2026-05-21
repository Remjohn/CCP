from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.perceptual_failure_corpus_models import (
    DeadPolishContrastCase,
    EmptyMotivationalSmoothnessCase,
    FalseDepthContrastCase,
    OverresolvedMeaningCase,
    SyntheticAuthorityContrastCase,
)
from src.ccp.services.perceptual_failure_corpus_service import PerceptualFailureCorpusService


FIXTURE_ROOT = REPO_ROOT / "sfl" / "failure_corpus"


def _build_service(tmp_path: Path) -> tuple[PerceptualFailureCorpusService, Path, ReceiptChain]:
    fixture_root = tmp_path / "failure_corpus"
    shutil.copytree(FIXTURE_ROOT, fixture_root)
    receipt_chain = ReceiptChain(coach_acronym="PFC", log_dir=str(tmp_path / "receipt_logs"))
    service = PerceptualFailureCorpusService(
        corpus_root=fixture_root,
        manifest_path=fixture_root / "manifest.yaml",
        receipt_chain=receipt_chain,
    )
    return service, fixture_root, receipt_chain


def _read_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_ac281_warm_loads_typed_perceptual_failure_corpus(tmp_path: Path) -> None:
    service, _, receipt_chain = _build_service(tmp_path)

    manifest = service.warm()

    assert manifest.case_counts["false_depth"] == 1
    assert manifest.case_counts["dead_polish"] == 1
    assert manifest.case_counts["synthetic_authority"] == 1
    assert manifest.case_counts["overresolved_meaning"] == 1
    assert manifest.case_counts["empty_motivational_smoothness"] == 1
    assert manifest.suite_counts["false_depth"] == 1
    assert manifest.suite_counts["synthetic_authority"] == 1

    assert isinstance(service.get_case("PFC-FD-PHASE0-0001"), FalseDepthContrastCase)
    assert isinstance(service.get_case("PFC-DP-RENDER-0001"), DeadPolishContrastCase)
    assert isinstance(service.get_case("PFC-SA-COMM-0001"), SyntheticAuthorityContrastCase)
    assert isinstance(service.get_case("PFC-ORM-PHASE0-0001"), OverresolvedMeaningCase)
    assert isinstance(service.get_case("PFC-EMS-REACT-0001"), EmptyMotivationalSmoothnessCase)

    receipts = receipt_chain.query(action="perceptual-failure-corpus-warm")
    assert receipts, "warm load must emit a perceptual-failure-corpus-warm receipt"


def test_directory_class_mismatch_is_rejected(tmp_path: Path) -> None:
    service, fixture_root, _ = _build_service(tmp_path)
    bad_case_path = fixture_root / "false_depth" / "PFC-FD-PHASE0-0001.yaml"
    payload = _read_yaml(bad_case_path)
    payload["failure_class"] = "dead_polish"
    payload["labels"]["failure_class"] = "dead_polish"
    _write_yaml(bad_case_path, payload)

    with pytest.raises(ValueError):
        service.warm()


def test_semantic_interop_reference_does_not_inline_hard_negative_ownership(tmp_path: Path) -> None:
    service, fixture_root, _ = _build_service(tmp_path)
    case_path = fixture_root / "synthetic_authority" / "PFC-SA-COMM-0001.yaml"
    payload = _read_yaml(case_path)
    payload["semantic_interop"]["linked_hard_negative_ids"] = [
        {"hard_negative_id": "HN-PRESTIGE-THEATER", "owned_definition": "forbidden"}
    ]
    _write_yaml(case_path, payload)

    with pytest.raises(ValueError):
        service.warm()


def test_failed_reload_keeps_previous_validated_manifest_active(tmp_path: Path) -> None:
    service, fixture_root, _ = _build_service(tmp_path)
    service.warm()
    original_case = service.get_case("PFC-SA-COMM-0001")
    assert original_case is not None

    manifest_path = fixture_root / "manifest.yaml"
    manifest_payload = _read_yaml(manifest_path)
    manifest_payload["case_counts"]["synthetic_authority"] = 2
    _write_yaml(manifest_path, manifest_payload)

    with pytest.raises(ValueError):
        service.reload(case_ids=["PFC-SA-COMM-0001"])

    restored_case = service.get_case("PFC-SA-COMM-0001")
    assert restored_case is not None
    assert restored_case.title == original_case.title
    assert service.manifest is not None
    assert service.manifest.case_counts["synthetic_authority"] == 1
