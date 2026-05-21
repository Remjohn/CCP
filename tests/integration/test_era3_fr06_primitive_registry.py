"""FR-ERA3-06 - Primitive Registry Query Service - integration tests."""

from __future__ import annotations

import time
from pathlib import Path
import sys
import textwrap

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.models.primitive_registry_models import PrimitivePlane
from src.ccp.services.primitive_registry_service import PrimitiveRegistryQueryService


def _run(func, *args, **kwargs):
    return func(*args, **kwargs)


def _write_yaml(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


class TestAC211StartupRegistryWarmAndInMemoryServing:
    def test_warm_cache_counts_and_hot_path_avoids_disk_reads(self):
        service = PrimitiveRegistryQueryService()
        warm_stats = _run(service.warm_registry)

        assert warm_stats.total_cached >= 243
        assert service.health().total_cached >= 243

        yaml_reads_before = service.loader.yaml_reads
        timings_ms: list[float] = []
        for _ in range(100):
            start = time.perf_counter()
            lookup = service.cache.get("EXP-FBK-001")
            timings_ms.append((time.perf_counter() - start) * 1000)
            assert lookup.record is not None
            assert lookup.cache_hit is True

        assert service.loader.yaml_reads == yaml_reads_before
        p95 = sorted(timings_ms)[94]
        assert p95 < 3.0

    def test_plane_and_family_queries_preserve_boundaries(self):
        service = PrimitiveRegistryQueryService()
        _run(service.warm_registry)

        family_response = service.query_by_family("feedback_scoring")
        assert family_response.experience_records
        assert family_response.meaning_records == []

        plane_response = service.query_by_plane(PrimitivePlane.MEANING)
        assert plane_response.plane == PrimitivePlane.MEANING
        assert plane_response.primitives
        assert all(hasattr(record, "primitive_id") for record in plane_response.primitives)


class TestAC212TargetedPrimitiveHotReload:
    def test_targeted_invalidation_reloads_only_the_affected_yaml(self, tmp_path: Path):
        primitives_root = tmp_path / "primitives"
        _write_yaml(
            primitives_root / "experience" / "feedback_scoring" / "EXP-FBK-001.yaml",
            """
            experience_primitive_id: "EXP-FBK-001"
            canonical_name: "Original RIM"
            aliases: ["RIM"]
            experience_family: "feedback_scoring"
            mechanic_role: "system"
            moment_role: "feedback_delivery"
            implementation_role: "architectural"
            summary: "Original"
            core_move: "Original"
            why_it_works: "Original"
            synergizes_with: []
            conflicts_with: []
            experience_stage_fit: {scoring: 1.0}
            surface_fit: {mini_app: 1.0}
            crosswalk_id: "XW-FBK-RIM"
            """,
        )
        _write_yaml(
            primitives_root / "experience" / "safe_failure_recovery" / "EXP-SAF-003.yaml",
            """
            experience_primitive_id: "EXP-SAF-003"
            canonical_name: "Recovery Anchor"
            aliases: []
            experience_family: "safe_failure_recovery"
            mechanic_role: "system"
            moment_role: "recovery"
            implementation_role: "architectural"
            summary: "Stable"
            core_move: "Stable"
            why_it_works: "Stable"
            synergizes_with: []
            conflicts_with: []
            experience_stage_fit: {recovery: 1.0}
            surface_fit: {mini_app: 1.0}
            crosswalk_id: "XW-SAF-003"
            """,
        )
        _write_yaml(
            primitives_root / "meaning" / "design_business" / "PRM-BUS-001.yaml",
            """
            primitive_id: "PRM-BUS-001"
            canonical_name: "Perception and Guidance Stack"
            aliases: []
            family: "design_business"
            implementation_role: "core"
            summary: "Meaning primitive"
            core_move: "Meaning primitive"
            why_it_works: "Meaning primitive"
            synergizes_with: []
            conflicts_with: []
            phase_fit: {generation: 1.0}
            surface_fit: {visual: 1.0}
            goal_bias: {clarity: 1.0}
            crosswalk_id: "XW-BUS-001"
            """,
        )

        service = PrimitiveRegistryQueryService(primitives_root=primitives_root)
        _run(service.warm_registry)
        yaml_reads_before_hot_reload = service.loader.yaml_reads

        record_before = service.query_by_id("EXP-FBK-001", PrimitivePlane.EXPERIENCE)
        assert record_before is not None
        assert record_before.canonical_name == "Original RIM"

        _write_yaml(
            primitives_root / "experience" / "feedback_scoring" / "EXP-FBK-001.yaml",
            """
            experience_primitive_id: "EXP-FBK-001"
            canonical_name: "Updated RIM"
            aliases: ["RIM"]
            experience_family: "feedback_scoring"
            mechanic_role: "system"
            moment_role: "feedback_delivery"
            implementation_role: "architectural"
            summary: "Updated"
            core_move: "Updated"
            why_it_works: "Updated"
            synergizes_with: []
            conflicts_with: []
            experience_stage_fit: {scoring: 1.0}
            surface_fit: {mini_app: 1.0}
            crosswalk_id: "XW-FBK-RIM"
            """,
        )

        invalidation = service.invalidate_primitive("EXP-FBK-001")
        assert invalidation.deleted_keys == 1

        unrelated_before = service.loader.yaml_reads
        unrelated_record = service.query_by_id("EXP-SAF-003", PrimitivePlane.EXPERIENCE)
        assert unrelated_record is not None
        assert service.loader.yaml_reads == unrelated_before

        reloaded_record = service.query_by_id("EXP-FBK-001", PrimitivePlane.EXPERIENCE)
        assert reloaded_record is not None
        assert reloaded_record.canonical_name == "Updated RIM"
        assert service.loader.yaml_reads == yaml_reads_before_hot_reload + 1
