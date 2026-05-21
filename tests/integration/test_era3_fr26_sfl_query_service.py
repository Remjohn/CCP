from __future__ import annotations

import shutil
from pathlib import Path
import sys

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.sfl_query_models import SFLQueryMode, SubliminalFunctionQueryRequest
from src.ccp.services.primitive_registry_service import PrimitiveRegistryQueryService
from src.ccp.services.sda_registry_service import SDARegistryService
from src.ccp.services.sfl_query_service import SubliminalFunctionQueryService
from src.ccp.services.sfl_registry_service import SFLRegistryService


def _build_services(tmp_path: Path) -> tuple[SubliminalFunctionQueryService, Path]:
    fixture_root = tmp_path / "fixture_root"
    shutil.copytree(REPO_ROOT / "sfl", fixture_root / "sfl")
    shutil.copytree(REPO_ROOT / "sda", fixture_root / "sda")
    shutil.copytree(REPO_ROOT / "primitives", fixture_root / "primitives")

    receipt_chain = ReceiptChain(coach_acronym="SFL", log_dir=str(tmp_path / "receipt_logs"))
    primitive_service = PrimitiveRegistryQueryService(
        primitives_root=fixture_root / "primitives",
        receipt_chain=receipt_chain,
    )
    sda_service = SDARegistryService(
        sda_root=fixture_root / "sda",
        manifest_path=fixture_root / "sda" / "registry_manifest.yaml",
        receipt_chain=receipt_chain,
    )
    sfl_registry_service = SFLRegistryService(
        sfl_root=fixture_root / "sfl",
        manifest_path=fixture_root / "sfl" / "registry_manifest.yaml",
        primitives_root=fixture_root / "primitives",
        sda_root=fixture_root / "sda",
        receipt_chain=receipt_chain,
        primitive_registry_service=primitive_service,
        sda_registry_service=sda_service,
    )
    query_service = SubliminalFunctionQueryService(
        sfl_registry_service=sfl_registry_service,
        primitive_registry_service=primitive_service,
        sda_registry_service=sda_service,
        receipt_chain=receipt_chain,
    )
    assert query_service.warm() is True
    return query_service, fixture_root


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class TestWarmAndLookup:
    def test_ac261_query_by_family_returns_only_canonical_functions(self, tmp_path: Path) -> None:
        service, _ = _build_services(tmp_path)

        response = service.query(
            SubliminalFunctionQueryRequest(
                query_mode=SFLQueryMode.BY_FAMILY,
                family_id="SFL-FAM-001",
            )
        )

        assert response.ready is True
        assert response.resolved_families
        assert response.resolved_functions
        assert all(record.function_id.startswith("SFL-FN-") for record in response.resolved_functions)
        dumped = response.model_dump(mode="json")
        assert "cognitive_imprint_score" not in str(dumped)
        assert "FalseDepthContrastCase" not in str(dumped)

    def test_ac262_query_by_primitive_uses_crosswalk_evidence_only(self, tmp_path: Path) -> None:
        service, _ = _build_services(tmp_path)

        response = service.query(
            SubliminalFunctionQueryRequest(
                query_mode=SFLQueryMode.BY_PRIMITIVE_CROSSWALK,
                primitive_id="PRM-BUS-001",
            )
        )

        assert response.ready is True
        assert response.evidence_trace
        assert all(record.evidence_kind.value == "primitive_crosswalk" for record in response.evidence_trace)
        returned_function_ids = {record.function_id for record in response.resolved_functions}
        assert returned_function_ids == {"SFL-FN-002", "SFL-FN-003", "SFL-FN-004"}


class TestBoundaryEnforcement:
    def test_ac263_geometry_lookup_does_not_emit_sda_runtime_metrics(self, tmp_path: Path) -> None:
        service, _ = _build_services(tmp_path)

        response = service.query(
            SubliminalFunctionQueryRequest(
                query_mode=SFLQueryMode.BY_REPRESENTATION_GEOMETRY,
                representation_geometry_id="SDA-RPG-001",
            )
        )

        dumped = response.model_dump(mode="json")
        dump_text = str(dumped)
        assert "invariant_gravity" not in dump_text
        assert "invariant_activation_intensity" not in dump_text
        assert "directional_integrity" not in dump_text
        assert response.resolved_functions


class TestHotPathBehavior:
    def test_ac267_repeated_queries_use_warmed_indexes(self, tmp_path: Path) -> None:
        service, _ = _build_services(tmp_path)

        initial_build_count = service.cache_manager.index_build_count
        for _ in range(100):
            response = service.query(
                SubliminalFunctionQueryRequest(
                    query_mode=SFLQueryMode.BY_FAMILY,
                    family_id="SFL-FAM-002",
                )
            )
            assert response.cache_hit is True

        assert service.cache_manager.index_build_count == initial_build_count

    def test_ac268_failed_rebuild_preserves_previous_good_state(self, tmp_path: Path) -> None:
        service, fixture_root = _build_services(tmp_path)

        baseline = service.query(
            SubliminalFunctionQueryRequest(
                query_mode=SFLQueryMode.BY_PRIMITIVE_CROSSWALK,
                primitive_id="EXP-FBK-001",
            )
        )
        baseline_family_ids = [family.family_id for family in baseline.resolved_families]
        baseline_registry_hash = service.cache_manager.version_stamp.registry_hash

        target_path = fixture_root / "sfl" / "crosswalks" / "primitive_to_function_family" / "SFL-XW-PF-001.yaml"
        payload = _read_yaml(target_path)
        payload["target_family_ids"] = ["SFL-FAM-999"]
        _write_yaml(target_path, payload)

        assert service.rebuild_after_registry_reload(target_path) is False

        after = service.query(
            SubliminalFunctionQueryRequest(
                query_mode=SFLQueryMode.BY_PRIMITIVE_CROSSWALK,
                primitive_id="EXP-FBK-001",
            )
        )
        assert [family.family_id for family in after.resolved_families] == baseline_family_ids
        assert service.cache_manager.version_stamp.registry_hash == baseline_registry_hash
