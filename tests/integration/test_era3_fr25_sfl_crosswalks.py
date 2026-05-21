from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.sfl_registry_service import SFLRegistryService


REPO_ROOT = Path(__file__).resolve().parents[2]
SFL_FIXTURE_ROOT = REPO_ROOT / "sfl"


def _build_service(tmp_path: Path) -> tuple[SFLRegistryService, Path]:
    fixture_root = tmp_path / "sfl"
    shutil.copytree(SFL_FIXTURE_ROOT, fixture_root)
    receipt_chain = ReceiptChain(coach_acronym="SFL", log_dir=str(tmp_path / "receipt_logs"))
    service = SFLRegistryService(
        sfl_root=fixture_root,
        manifest_path=fixture_root / "registry_manifest.yaml",
        receipt_chain=receipt_chain,
    )
    return service, fixture_root


def _read_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class TestCrosswalkIntegrity:
    def test_primitive_crosswalk_rejects_unknown_primitive_id(self, tmp_path: Path) -> None:
        service, fixture_root = _build_service(tmp_path)
        crosswalk_path = fixture_root / "crosswalks" / "primitive_to_function_family" / "SFL-XW-PF-001.yaml"
        payload = _read_yaml(crosswalk_path)
        primitive_links = payload["primitive_links"]
        primitive_links[0]["primitive_id"] = "EXP-TRB-001"
        _write_yaml(crosswalk_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "PRIMITIVE_REFERENCE_MISSING" for issue in report.issues)

    def test_geometry_crosswalk_resolves_known_sda_geometry(self, tmp_path: Path) -> None:
        service, _ = _build_service(tmp_path)

        report = service.warm()

        assert report.ready is True
        bundle = service.get_crosswalk_bundle("representation_geometry_to_function_profile")
        assert "SFL-XW-RG-001" in bundle
