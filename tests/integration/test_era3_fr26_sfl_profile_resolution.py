from __future__ import annotations

import shutil
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.sfl_query_models import DeliverySurfaceKind, FunctionProfileAssemblyRequest
from src.ccp.services.primitive_registry_service import PrimitiveRegistryQueryService
from src.ccp.services.sda_registry_service import SDARegistryService
from src.ccp.services.sfl_query_service import SubliminalFunctionQueryService
from src.ccp.services.sfl_registry_service import SFLRegistryService


def _build_services(tmp_path: Path) -> SubliminalFunctionQueryService:
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
    return query_service


class TestAssemblyDeterminism:
    def test_ac264_same_inputs_produce_same_stack(self, tmp_path: Path) -> None:
        service = _build_services(tmp_path)
        request = FunctionProfileAssemblyRequest(
            coach_id="coach-001",
            content_archetype="Transformation Story",
            delivery_surface=DeliverySurfaceKind.SHORT_FORM_VIDEO,
            representation_geometry_id="SDA-RPG-001",
            primitive_ids=["PRM-BUS-001", "PRM-BUS-002"],
        )

        first = service.assemble_profile(request)
        second = service.assemble_profile(request)

        assert first.status == second.status
        assert first.stack_packet is not None
        assert second.stack_packet is not None
        assert first.stack_packet.active_function_ids == second.stack_packet.active_function_ids
        assert [record.source_artifact_id for record in first.stack_packet.evidence_trace] == [
            record.source_artifact_id for record in second.stack_packet.evidence_trace
        ]


class TestFallbacks:
    def test_ac265_partial_evidence_degrades_to_family_only_with_warning(self, tmp_path: Path) -> None:
        service = _build_services(tmp_path)
        request = FunctionProfileAssemblyRequest(
            coach_id="coach-002",
            delivery_surface=DeliverySurfaceKind.COMMERCIAL,
            primitive_ids=["EXP-FBK-001"],
            allow_family_only_fallback=True,
        )

        result = service.assemble_profile(request)

        assert result.status.value == "family_only"
        assert result.stack_packet is not None
        assert result.stack_packet.active_function_ids == ["SFL-FN-001", "SFL-FN-002"]
        assert any(warning.code.value == "family_only_fallback" for warning in result.warnings)
        assert all(
            record.selection_source.value == "fallback_from_family"
            for record in result.profile.resolved_functions
        )


class TestConflictHandling:
    def test_ac266_conflicting_profiles_do_not_union_into_centroid_stack(self, tmp_path: Path) -> None:
        service = _build_services(tmp_path)
        request = FunctionProfileAssemblyRequest(
            coach_id="coach-003",
            content_archetype="Transformation Story",
            delivery_surface=DeliverySurfaceKind.TELEGRAM,
        )

        result = service.assemble_profile(request)

        assert result.status.value == "partial"
        assert result.stack_packet is not None
        assert "SFL-FN-004" not in result.stack_packet.active_function_ids
        assert "SFL-FN-004" in result.stack_packet.suppressed_function_ids
        assert any(conflict.resolution == "suppressed_lower_priority" for conflict in result.conflicts)
        assert len(result.stack_packet.active_function_ids) <= 4
