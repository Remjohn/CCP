"""FR-ERA3-06 - conflict resolver integration tests."""

from __future__ import annotations

from pathlib import Path
import sys
import textwrap

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.models.primitive_registry_models import PrimitiveQueryRequest
from src.ccp.services.primitive_registry_service import PrimitiveRegistryQueryService


def _run(func, *args, **kwargs):
    return func(*args, **kwargs)


def _write_yaml(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def _build_service(tmp_path: Path) -> PrimitiveRegistryQueryService:
    primitives_root = tmp_path / "primitives"
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
        conflicts_with: ["EXP-SOC-002"]
        experience_stage_fit: {scoring: 1.0, recovery: 1.0}
        surface_fit: {mini_app: 1.0}
        crosswalk_id: "XW-SAF-003"
        """,
    )
    _write_yaml(
        primitives_root / "experience" / "social_referral" / "EXP-SOC-002.yaml",
        """
        experience_primitive_id: "EXP-SOC-002"
        canonical_name: "Share Loop"
        aliases: []
        experience_family: "social_referral"
        mechanic_role: "system"
        moment_role: "share"
        implementation_role: "architectural"
        summary: "Share"
        core_move: "Share"
        why_it_works: "Share"
        synergizes_with: []
        conflicts_with: []
        experience_stage_fit: {scoring: 0.4, social_spread: 1.0}
        surface_fit: {mini_app: 1.0}
        crosswalk_id: "XW-SOC-002"
        """,
    )
    _write_yaml(
        primitives_root / "experience" / "feedback_scoring" / "EXP-FBK-001.yaml",
        """
        experience_primitive_id: "EXP-FBK-001"
        canonical_name: "RIM Feedback Discipline"
        aliases: []
        experience_family: "feedback_scoring"
        mechanic_role: "system"
        moment_role: "feedback_delivery"
        implementation_role: "architectural"
        summary: "RIM"
        core_move: "RIM"
        why_it_works: "RIM"
        synergizes_with: []
        conflicts_with: ["EXP-TRG-001"]
        experience_stage_fit: {scoring: 0.8}
        surface_fit: {mini_app: 1.0}
        crosswalk_id: "XW-FBK-001"
        """,
    )
    _write_yaml(
        primitives_root / "experience" / "trigger_timing" / "EXP-TRG-001.yaml",
        """
        experience_primitive_id: "EXP-TRG-001"
        canonical_name: "Precision Trigger"
        aliases: []
        experience_family: "trigger_timing"
        mechanic_role: "system"
        moment_role: "trigger"
        implementation_role: "architectural"
        summary: "TRG"
        core_move: "TRG"
        why_it_works: "TRG"
        synergizes_with: []
        conflicts_with: ["EXP-FBK-001"]
        experience_stage_fit: {scoring: 0.8}
        surface_fit: {mini_app: 1.0}
        crosswalk_id: "XW-TRG-001"
        """,
    )
    _write_yaml(
        primitives_root / "experience" / "personalization_identity" / "EXP-PER-001.yaml",
        """
        experience_primitive_id: "EXP-PER-001"
        canonical_name: "Identity Match"
        aliases: []
        experience_family: "personalization_identity"
        mechanic_role: "system"
        moment_role: "identity"
        implementation_role: "architectural"
        summary: "PER"
        core_move: "PER"
        why_it_works: "PER"
        synergizes_with: []
        conflicts_with: ["None"]
        experience_stage_fit: {scoring: 0.8}
        surface_fit: {mini_app: 1.0}
        crosswalk_id: "XW-PER-001"
        """,
    )
    _write_yaml(
        primitives_root / "meaning" / "design_business" / "PRM-BUS-001.yaml",
        """
        primitive_id: "PRM-BUS-001"
        canonical_name: "Guidance Stack"
        aliases: []
        family: "design_business"
        implementation_role: "core"
        summary: "BUS"
        core_move: "BUS"
        why_it_works: "BUS"
        synergizes_with: []
        conflicts_with: []
        coalition_partners_antagonistic: ["PRM-HUM-001"]
        phase_fit: {generation: 0.9}
        surface_fit: {visual: 1.0}
        goal_bias: {clarity: 1.0}
        crosswalk_id: "XW-BUS-001"
        """,
    )
    _write_yaml(
        primitives_root / "meaning" / "humor_distortion" / "PRM-HUM-001.yaml",
        """
        primitive_id: "PRM-HUM-001"
        canonical_name: "Comedy Distortion"
        aliases: []
        family: "humor_distortion"
        implementation_role: "core"
        summary: "HUM"
        core_move: "HUM"
        why_it_works: "HUM"
        synergizes_with: []
        conflicts_with: []
        phase_fit: {generation: 0.4}
        surface_fit: {visual: 0.8}
        goal_bias: {surprise: 1.0}
        crosswalk_id: "XW-HUM-001"
        """,
    )
    service = PrimitiveRegistryQueryService(primitives_root=primitives_root)
    _run(service.warm_registry)
    return service


class TestAC221ConflictFilteringBeforePayloadReturn:
    def test_unilateral_conflict_removes_lower_scoring_primitive(self, tmp_path: Path):
        service = _build_service(tmp_path)

        response = service.query_batch(
            PrimitiveQueryRequest(
                requested_ids=["EXP-SAF-003", "EXP-SOC-002"],
                context="scoring",
            )
        )

        assert response.conflict_resolution.resolution_applied is True
        assert response.conflict_resolution.removed_ids == ["EXP-SOC-002"]
        assert [record.experience_primitive_id for record in response.resolved_primitives] == ["EXP-SAF-003"]

    def test_meaning_plane_antagonistic_field_is_honored(self, tmp_path: Path):
        service = _build_service(tmp_path)

        response = service.query_batch(
            PrimitiveQueryRequest(
                requested_ids=["PRM-BUS-001", "PRM-HUM-001"],
                context="generation",
            )
        )

        assert response.conflict_resolution.removed_ids == ["PRM-HUM-001"]
        assert [record.primitive_id for record in response.resolved_primitives] == ["PRM-BUS-001"]


class TestAC222DeterministicTiebreakingOrder:
    def test_family_order_tiebreak_is_stable_over_repeated_replays(self, tmp_path: Path):
        service = _build_service(tmp_path)

        winners = []
        for _ in range(100):
            response = service.query_batch(
                PrimitiveQueryRequest(
                    requested_ids=["EXP-FBK-001", "EXP-TRG-001"],
                    context="scoring",
                )
            )
            winners.append(response.resolved_primitives[0].experience_primitive_id)

        assert set(winners) == {"EXP-TRG-001"}


class TestAC223QuerySurfaceCoverageAndNormalization:
    def test_none_conflict_normalization_does_not_strip_valid_primitives(self, tmp_path: Path):
        service = _build_service(tmp_path)

        response = service.query_batch(
            PrimitiveQueryRequest(
                requested_ids=["EXP-PER-001", "EXP-SAF-003"],
                context="scoring",
            )
        )

        resolved_ids = [record.experience_primitive_id for record in response.resolved_primitives]
        assert resolved_ids == ["EXP-PER-001", "EXP-SAF-003"]
        assert response.conflict_resolution.resolution_applied is False
