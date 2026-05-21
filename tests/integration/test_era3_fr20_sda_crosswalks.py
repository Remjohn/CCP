from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.sda_registry_service import SDARegistryService


REPO_ROOT = Path(__file__).resolve().parents[2]
SDA_FIXTURE_ROOT = REPO_ROOT / "sda"


def _build_service(tmp_path: Path) -> tuple[SDARegistryService, Path]:
    fixture_root = tmp_path / "sda"
    shutil.copytree(SDA_FIXTURE_ROOT, fixture_root)
    receipt_chain = ReceiptChain(coach_acronym="SDA", log_dir=str(tmp_path / "receipt_logs"))
    service = SDARegistryService(
        sda_root=fixture_root,
        manifest_path=fixture_root / "registry_manifest.yaml",
        receipt_chain=receipt_chain,
    )
    return service, fixture_root


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class TestPrimitiveInvariantCrosswalks:
    def test_ac204_primitive_reference_must_exist(self, tmp_path: Path) -> None:
        service, fixture_root = _build_service(tmp_path)
        crosswalk_path = fixture_root / "crosswalks" / "primitive_to_invariant" / "SDA-XW-PI-001.yaml"
        payload = _read_yaml(crosswalk_path)
        payload["primitive_id"] = "EXP-TRS-999"
        _write_yaml(crosswalk_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "CROSSWALK_REFERENCE_MISSING" for issue in report.issues)

    def test_invariant_reference_must_exist(self, tmp_path: Path) -> None:
        service, fixture_root = _build_service(tmp_path)
        crosswalk_path = fixture_root / "crosswalks" / "primitive_to_invariant" / "SDA-XW-PI-001.yaml"
        payload = _read_yaml(crosswalk_path)
        payload["linked_invariants"][0]["target_id"] = "SDA-INV-999"
        _write_yaml(crosswalk_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any("Invariant reference not found" in issue.message for issue in report.issues)

    def test_crosswalk_weights_within_zero_to_one(self, tmp_path: Path) -> None:
        service, fixture_root = _build_service(tmp_path)
        crosswalk_path = fixture_root / "crosswalks" / "primitive_to_invariant" / "SDA-XW-PI-001.yaml"
        payload = _read_yaml(crosswalk_path)
        payload["linked_invariants"][0]["weight"] = 1.5
        _write_yaml(crosswalk_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "MODEL_VALIDATION_ERROR" for issue in report.issues)


class TestArchetypeGeometryCrosswalks:
    def test_content_archetype_must_belong_to_retained_prd02_inventory(self, tmp_path: Path) -> None:
        service, fixture_root = _build_service(tmp_path)
        crosswalk_path = fixture_root / "crosswalks" / "archetype_to_geometry" / "SDA-XW-AG-001.yaml"
        payload = _read_yaml(crosswalk_path)
        payload["content_archetype"] = "Made Up Archetype"
        _write_yaml(crosswalk_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "ARCHETYPE_INVENTORY_VIOLATION" for issue in report.issues)

    def test_geometry_reference_must_exist(self, tmp_path: Path) -> None:
        service, fixture_root = _build_service(tmp_path)
        crosswalk_path = fixture_root / "crosswalks" / "archetype_to_geometry" / "SDA-XW-AG-001.yaml"
        payload = _read_yaml(crosswalk_path)
        payload["linked_geometries"][0]["target_id"] = "SDA-ARG-999"
        _write_yaml(crosswalk_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any("Archetypal geometry reference not found" in issue.message for issue in report.issues)

