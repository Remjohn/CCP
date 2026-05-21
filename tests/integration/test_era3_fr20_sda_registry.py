from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.sda_registry_service import (
    SDARegistryService,
    STAGE_STARTUP_WARM,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SDA_FIXTURE_ROOT = REPO_ROOT / "sda"


def _build_service(tmp_path: Path) -> tuple[SDARegistryService, Path, ReceiptChain]:
    fixture_root = tmp_path / "sda"
    shutil.copytree(SDA_FIXTURE_ROOT, fixture_root)
    receipt_chain = ReceiptChain(coach_acronym="SDA", log_dir=str(tmp_path / "receipt_logs"))
    service = SDARegistryService(
        sda_root=fixture_root,
        manifest_path=fixture_root / "registry_manifest.yaml",
        receipt_chain=receipt_chain,
    )
    return service, fixture_root, receipt_chain


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class TestManifestBoot:
    def test_ac201_warm_loads_all_required_classes(self, tmp_path: Path) -> None:
        service, _, receipt_chain = _build_service(tmp_path)

        report = service.warm()

        assert report.ready is True
        assert report.existential_invariant_count == 3
        assert report.representation_geometry_count == 3
        assert report.archetypal_geometry_count == 3
        assert report.species_composition_rule_count == 2
        assert report.primitive_to_invariant_crosswalk_count == 1
        assert report.archetype_to_geometry_crosswalk_count == 1
        assert report.issues == []

        receipts = receipt_chain.query(action=STAGE_STARTUP_WARM)
        assert receipts, "startup warm receipt must be written"

    def test_manifest_counts_must_match_loaded_counts(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        manifest_path = fixture_root / "registry_manifest.yaml"
        manifest = _read_yaml(manifest_path)
        manifest["expected_counts"]["existential_invariants"] = 4
        _write_yaml(manifest_path, manifest)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "MANIFEST_COUNT_MISMATCH" for issue in report.issues)

    def test_registry_ready_false_when_manifest_missing(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        (fixture_root / "registry_manifest.yaml").unlink()

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "SDA_MANIFEST_MISSING" for issue in report.issues)


class TestArtifactClassGuards:
    def test_false_registry_content_species_rejected(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        forbidden_dir = fixture_root / "ontology" / "content_species"
        forbidden_dir.mkdir(parents=True)
        payload = {
            "artifact_id": "SDA-SPC-001",
            "artifact_class": "canonical_ontology",
            "registry_kind": "content_species",
            "canonical_name": "Derived Species",
            "definition": "This should never live in canonical SDA ontology.",
            "source_documents": [
                "lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md"
            ],
        }
        _write_yaml(forbidden_dir / "SDA-SPC-001.yaml", payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "FALSE_REGISTRY_VIOLATION" for issue in report.issues)

    def test_false_registry_hard_negative_rejected(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        forbidden_dir = fixture_root / "grammar" / "hard_negatives"
        forbidden_dir.mkdir(parents=True)
        payload = {
            "artifact_id": "SDA-HNX-001",
            "artifact_class": "canonical_structural_grammar",
            "registry_kind": "hard_negative",
            "canonical_name": "Bad Negative",
            "definition": "Hard negatives belong to FR-ERA3-24, not FR-ERA3-20.",
            "source_documents": [
                "lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md"
            ],
        }
        _write_yaml(forbidden_dir / "SDA-HNX-001.yaml", payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "FALSE_REGISTRY_VIOLATION" for issue in report.issues)

    def test_runtime_scalar_fields_rejected_on_invariant(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        invariant_path = fixture_root / "ontology" / "existential_invariants" / "SDA-INV-001.yaml"
        payload = _read_yaml(invariant_path)
        payload["invariant_resonance_multiplier"] = 0.91
        _write_yaml(invariant_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "SCALAR_LAYER_VIOLATION" for issue in report.issues)

    def test_wrong_prefix_rejected_for_artifact_kind(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        invariant_path = fixture_root / "ontology" / "existential_invariants" / "SDA-INV-001.yaml"
        payload = _read_yaml(invariant_path)
        payload["artifact_id"] = "SDA-RPG-001"
        _write_yaml(invariant_path, payload)

        report = service.warm()

        assert report.ready is False
        assert any(issue.error_code == "ARTIFACT_ID_PREFIX_VIOLATION" for issue in report.issues)


class TestReloadBehavior:
    def test_single_artifact_reload_updates_only_target(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        initial = service.warm()
        assert initial.ready is True

        target_path = fixture_root / "ontology" / "representation_geometries" / "SDA-RPG-002.yaml"
        payload = _read_yaml(target_path)
        payload["canonical_name"] = "Protective Witness Encoding Updated"
        _write_yaml(target_path, payload)

        result = service.reload_artifact(target_path)

        assert result.success is True
        assert service.get_representation_geometry("SDA-RPG-002") is not None
        assert service.get_representation_geometry("SDA-RPG-002").canonical_name == "Protective Witness Encoding Updated"
        assert service.get_invariant("SDA-INV-001") is not None
        assert service.health().existential_invariant_count == 3

    def test_failed_reload_preserves_previous_good_state(self, tmp_path: Path) -> None:
        service, fixture_root, _ = _build_service(tmp_path)
        initial = service.warm()
        assert initial.ready is True

        target_path = fixture_root / "ontology" / "representation_geometries" / "SDA-RPG-002.yaml"
        old_name = service.get_representation_geometry("SDA-RPG-002").canonical_name
        payload = _read_yaml(target_path)
        payload["artifact_id"] = "SDA-INV-002"
        _write_yaml(target_path, payload)

        result = service.reload_artifact(target_path)

        assert result.success is False
        assert result.error_code == "ARTIFACT_ID_PREFIX_VIOLATION"
        assert service.get_representation_geometry("SDA-RPG-002").canonical_name == old_name

