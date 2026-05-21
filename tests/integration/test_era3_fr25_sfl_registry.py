from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.sfl_registry_service import (
    SFLRegistryService,
    STAGE_STARTUP_WARM,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SFL_FIXTURE_ROOT = REPO_ROOT / "sfl"


def _build_service(tmp_path: Path) -> tuple[SFLRegistryService, Path, ReceiptChain]:
    fixture_root = tmp_path / "sfl"
    shutil.copytree(SFL_FIXTURE_ROOT, fixture_root)
    receipt_chain = ReceiptChain(coach_acronym="SFL", log_dir=str(tmp_path / "receipt_logs"))
    service = SFLRegistryService(
        sfl_root=fixture_root,
        manifest_path=fixture_root / "registry_manifest.yaml",
        receipt_chain=receipt_chain,
    )
    return service, fixture_root, receipt_chain


def _read_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class TestManifestBoot:
    def test_ac251_warm_loads_all_required_sfl_classes(self, tmp_path: Path) -> None:
        service, _, receipt_chain = _build_service(tmp_path)

        report = service.warm()

        assert report.ready is True
        assert report.family_count == 4
        assert report.function_count == 4
        assert report.compression_rule_count == 4
        assert report.primitive_to_function_family_crosswalk_count == 2
        assert report.representation_geometry_crosswalk_count == 1
        assert report.archetype_profile_crosswalk_count == 1
        assert report.surface_constraint_profile_count == 2
        assert report.issues == []

        receipts = receipt_chain.query(action=STAGE_STARTUP_WARM)
        assert receipts, "startup warm receipt must be written"


class TestArtifactClassGuards:
    def test_flat_120_rows_are_rejected(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        forbidden_dir = fixture_root / "associations"
        forbidden_dir.mkdir(parents=True)
        payload = {
            "artifact_id": "SFL-FAM-998",
            "artifact_class": "canonical_function_family",
            "canonical_name": "Framing",
            "family_kind": "framing_and_contrast",
            "definition": "A long enough definition that still attempts to flatten one association into canon.",
            "purpose": "A long enough purpose that still represents a forbidden flat-120 design.",
            "positive_space_role": "A long enough positive role that still reflects a single-term family row.",
            "negative_space_boundary": "A long enough negative role that still reflects a forbidden one-row canonization.",
            "anti_bloat_guidance": "A long enough anti-bloat note that does not rescue the flat-row violation.",
            "related_raw_terms": [{"raw_term": "framing", "normalization_note": "single row"}],
            "source_documents": [{"path": "lab/120 subliminal associations Chat.md", "note": "test"}],
        }
        _write_yaml(forbidden_dir / "framing.yaml", payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "FLAT_120_VIOLATION" for issue in report.issues)

    def test_metric_payload_in_functions_dir_is_rejected(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        function_path = fixture_root / "functions" / "SFL-FN-001.yaml"
        payload = _read_yaml(function_path)
        payload["cognitive_imprint_score"] = 0.92
        _write_yaml(function_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "FUNCTION_METRIC_SEPARATION_VIOLATION" for issue in report.issues)

    def test_sda_owned_fields_on_sfl_artifact_are_rejected(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        function_path = fixture_root / "functions" / "SFL-FN-002.yaml"
        payload = _read_yaml(function_path)
        payload["invariant_gravity"] = 0.88
        _write_yaml(function_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "SDA_OWNERSHIP_VIOLATION" for issue in report.issues)


class TestReloadBehavior:
    def test_single_artifact_reload_updates_only_target(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        initial = service.warm()
        assert initial.ready is True

        target_path = fixture_root / "functions" / "SFL-FN-004.yaml"
        payload = _read_yaml(target_path)
        payload["canonical_name"] = "MysteryRetentionFunctionUpdated"
        _write_yaml(target_path, payload)

        result = service.reload_artifact(target_path)

        assert result.success is True
        assert service.get_function("SFL-FN-004") is not None
        assert service.get_function("SFL-FN-004").canonical_name == "MysteryRetentionFunctionUpdated"
        assert service.get_family("SFL-FAM-001") is not None
        assert service.health().family_count == 4

    def test_failed_reload_preserves_previous_good_state(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        initial = service.warm()
        assert initial.ready is True

        target_path = fixture_root / "functions" / "SFL-FN-004.yaml"
        old_name = service.get_function("SFL-FN-004").canonical_name
        payload = _read_yaml(target_path)
        payload["cognitive_imprint_score"] = 0.99
        _write_yaml(target_path, payload)

        result = service.reload_artifact(target_path)

        assert result.success is False
        assert result.previous_state_restored is True
        assert result.error_code == "FUNCTION_METRIC_SEPARATION_VIOLATION"
        assert service.get_function("SFL-FN-004").canonical_name == old_name
