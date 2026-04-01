"""
FR-VIS-15 — ConsciousPose Body Language Library Tests (Step 29)

Coverage:
- AC1: Deterministic reproduction (same CP-ID → same path)
- AC2: Composition resolution (7-layer decomposition)
- AC3: Layer independence
- AC4: Mood-state query filtering
- AC6: Manifest integrity validation
- Safety: CP-ID validation, path traversal, framing mismatch
"""

import pytest

from core.conscious_pose_library import (
    CompositionRegistry,
    CompositionValidator,
    ControlNetMapResolver,
    PoseAtomRegistry,
)
from core.visual_models import (
    CompositionType,
    ManifestEntry,
    PoseAtom,
    PoseComposition,
    PoseLayer,
    PoseSpec,
    SourceLibrary,
    VisualPipelineError,
)


def _seed_registry() -> PoseAtomRegistry:
    """Seed a registry with representative atoms from each layer."""
    registry = PoseAtomRegistry()
    atoms = [
        PoseAtom(cp_id="CP-B-001", layer=PoseLayer.BODY, position_name="standing_square_shoulders_back",
                 signal="Full authority", mood_fit=["Status", "Processing"], archetype_fit=["The Educator"]),
        PoseAtom(cp_id="CP-B-002", layer=PoseLayer.BODY, position_name="standing_hip_shift",
                 signal="Relaxed confidence", mood_fit=["Escape"], archetype_fit=["The Storyteller"]),
        PoseAtom(cp_id="CP-B-014", layer=PoseLayer.BODY, position_name="forward_lean_engaged",
                 signal="Active engagement", mood_fit=["Processing", "Discovery"],
                 archetype_fit=["The Educator", "The Guide"]),
        PoseAtom(cp_id="CP-B-034", layer=PoseLayer.BODY, position_name="victory_arms",
                 signal="Celebration", mood_fit=["Status", "Escape"]),
        PoseAtom(cp_id="CP-H-001", layer=PoseLayer.HANDS, position_name="index_point_camera_firm",
                 signal="Direct authority", mood_fit=["Status"]),
        PoseAtom(cp_id="CP-H-009", layer=PoseLayer.HANDS, position_name="open_palm_gesture",
                 signal="Invitation", mood_fit=["Escape", "Discovery"]),
        PoseAtom(cp_id="CP-H-031", layer=PoseLayer.HANDS, position_name="relaxed_neutral",
                 signal="Neutral baseline", mood_fit=["Processing", "Escape", "Discovery", "Status"]),
        PoseAtom(cp_id="CP-G-001", layer=PoseLayer.GAZE, position_name="direct_camera",
                 signal="Parasocial lock", mood_fit=["Escape", "Status"]),
        PoseAtom(cp_id="CP-G-005", layer=PoseLayer.GAZE, position_name="averted_contemplative",
                 signal="Curiosity cue", mood_fit=["Processing"]),
        PoseAtom(cp_id="CP-S-001", layer=PoseLayer.SCENE, position_name="extreme_closeup",
                 signal="Intimacy", mood_fit=["Processing"]),
        PoseAtom(cp_id="CP-S-002", layer=PoseLayer.SCENE, position_name="medium_shot",
                 signal="Conversational", mood_fit=["Escape", "Processing"]),
        PoseAtom(cp_id="CP-S-005", layer=PoseLayer.SCENE, position_name="wide_shot",
                 signal="Context + authority", mood_fit=["Status"]),
        PoseAtom(cp_id="CP-MV-001", layer=PoseLayer.MOOD_VISUAL, position_name="warm_intimate",
                 signal="Warmth", mood_fit=["Processing", "Escape"]),
        PoseAtom(cp_id="CP-MV-014", layer=PoseLayer.MOOD_VISUAL, position_name="lab_clinical",
                 signal="Clinical", mood_fit=["Processing"]),
        PoseAtom(cp_id="CP-P-024", layer=PoseLayer.PROPS, position_name="coffee_mug_hold",
                 signal="Casual authority", mood_fit=["Escape"]),
    ]
    registry.register_atoms(atoms)
    return registry


class TestPoseAtomRegistry:

    def test_register_and_count(self):
        registry = _seed_registry()
        assert registry.count() == 15

    def test_get_valid_atom(self):
        registry = _seed_registry()
        atom = registry.get_atom("CP-B-001")
        assert atom.position_name == "standing_square_shoulders_back"

    def test_get_invalid_atom_raises(self):
        registry = _seed_registry()
        with pytest.raises(VisualPipelineError) as exc:
            registry.get_atom("CP-B-037")
        assert exc.value.code == "INVALID_CP_ID"

    def test_query_by_layer(self):
        registry = _seed_registry()
        body = registry.get_atoms_by_layer(PoseLayer.BODY)
        assert len(body) == 4

    def test_mood_state_query_processing(self):
        """AC4: Mood-state query returns correct atoms."""
        registry = _seed_registry()
        processing = registry.get_atoms_by_mood("Processing")

        cp_ids = [a.cp_id for a in processing]
        assert "CP-B-001" in cp_ids     # Status + Processing
        assert "CP-B-014" in cp_ids     # Processing + Discovery
        assert "CP-MV-001" in cp_ids    # Processing + Escape
        assert "CP-B-034" not in cp_ids  # Status + Escape only

    def test_archetype_query(self):
        registry = _seed_registry()
        educator = registry.get_atoms_by_archetype("The Educator")
        assert len(educator) >= 2

    def test_count_by_layer(self):
        registry = _seed_registry()
        counts = registry.count_by_layer()
        assert counts["body"] == 4
        assert counts["hands"] == 3
        assert counts["gaze"] == 2


class TestCompositionRegistry:

    def test_composition_resolution(self):
        """AC2: Composition resolves to 7-layer decomposition."""
        registry = _seed_registry()
        comp_registry = CompositionRegistry(registry)

        comp = PoseComposition(
            composition_id="COMP-EDUCATOR-DEFAULT-001",
            composition_name="Educator Default - Teaching Authority",
            composition_type=CompositionType.ARCHETYPE_DEFAULT,
            body_cp_id="CP-B-001",
            hands_cp_id="CP-H-001",
            gaze_cp_id="CP-G-001",
            scene_cp_id="CP-S-002",
            mood_visual_cp_id="CP-MV-001",
            props_cp_id=None,
            archetype_family="The Educator",
        )
        comp_registry.register_composition(comp)

        resolved = comp_registry.resolve("COMP-EDUCATOR-DEFAULT-001")
        assert resolved.body_cp_id == "CP-B-001"
        assert resolved.hands_cp_id == "CP-H-001"
        assert resolved.gaze_cp_id == "CP-G-001"
        assert resolved.scene_cp_id == "CP-S-002"

    def test_nonexistent_composition_raises(self):
        registry = _seed_registry()
        comp_registry = CompositionRegistry(registry)

        with pytest.raises(VisualPipelineError) as exc:
            comp_registry.resolve("COMP-NONEXISTENT")
        assert exc.value.code == "COMPOSITION_NOT_FOUND"

    def test_composition_type_query(self):
        registry = _seed_registry()
        comp_registry = CompositionRegistry(registry)

        comp_registry.register_composition(PoseComposition(
            composition_id="COMP-ARCH-001", composition_type=CompositionType.ARCHETYPE_DEFAULT,
        ))
        comp_registry.register_composition(PoseComposition(
            composition_id="COMP-MEME-001", composition_type=CompositionType.MEMETIC_RECIPE,
        ))

        archetypes = comp_registry.get_compositions_by_type(CompositionType.ARCHETYPE_DEFAULT)
        assert len(archetypes) == 1


class TestControlNetMapResolver:

    def test_deterministic_path_resolution(self):
        """AC1: Same CP-ID → same path across multiple calls."""
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        path1 = resolver.resolve_depth_path("CP-B-001")
        path2 = resolver.resolve_depth_path("CP-B-001")
        assert path1 == path2

    def test_depth_and_openpose_different(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        depth = resolver.resolve_depth_path("CP-B-001")
        openpose = resolver.resolve_openpose_path("CP-B-001")
        assert depth != openpose
        assert "depth" in depth
        assert "openpose" in openpose

    def test_path_traversal_blocked(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        with pytest.raises(VisualPipelineError) as exc:
            resolver.sanitize_path("../../../../etc/passwd")
        assert exc.value.code == "PATH_TRAVERSAL_BLOCKED"

    def test_non_efs_path_blocked(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        with pytest.raises(VisualPipelineError) as exc:
            resolver.sanitize_path("/tmp/evil/depth.png")
        assert exc.value.code == "INVALID_PATH"

    def test_valid_efs_path_passes(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        result = resolver.sanitize_path("/efs/ccp-models/controlnet/body/CP-B-001_depth.png")
        assert result.startswith("/efs/ccp-models/controlnet/")

    def test_manifest_integrity_all_match(self):
        """AC6: Manifest matches disk files."""
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        entries = [
            ManifestEntry(cp_id="CP-B-001", file_path="/efs/a.png", file_type="depth"),
            ManifestEntry(cp_id="CP-B-002", file_path="/efs/b.png", file_type="depth"),
        ]
        resolver.build_manifest(entries)

        result = resolver.validate_manifest(["/efs/a.png", "/efs/b.png"])
        assert result["valid"] is True
        assert len(result["missing_on_disk"]) == 0
        assert len(result["orphans_on_disk"]) == 0

    def test_manifest_missing_file(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        entries = [
            ManifestEntry(cp_id="CP-B-001", file_path="/efs/a.png", file_type="depth"),
            ManifestEntry(cp_id="CP-B-002", file_path="/efs/b.png", file_type="depth"),
        ]
        resolver.build_manifest(entries)

        result = resolver.validate_manifest(["/efs/a.png"])  # b.png missing
        assert result["valid"] is False
        assert "/efs/b.png" in result["missing_on_disk"]

    def test_manifest_orphan_file(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        entries = [ManifestEntry(cp_id="CP-B-001", file_path="/efs/a.png", file_type="depth")]
        resolver.build_manifest(entries)

        result = resolver.validate_manifest(["/efs/a.png", "/efs/orphan.png"])
        assert result["valid"] is False
        assert "/efs/orphan.png" in result["orphans_on_disk"]

    def test_receipt_chain_on_resolve(self):
        registry = _seed_registry()
        resolver = ControlNetMapResolver(registry)

        spec = PoseSpec(body="CP-B-001", scene="CP-S-002")
        resolver.resolve_pose_spec(spec)

        receipts = resolver.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "POSE_RESOLVE"


class TestCompositionValidator:

    def test_framing_mismatch_detected(self):
        validator = CompositionValidator()
        result = validator.validate_composition(
            body_cp_id="CP-B-001",   # Full body
            scene_cp_id="CP-S-001",  # Extreme closeup
        )
        assert result["has_warnings"] is True
        assert "FRAMING_MISMATCH" in result["warnings"][0]

    def test_compatible_framing_no_warning(self):
        validator = CompositionValidator()
        result = validator.validate_composition(
            body_cp_id="CP-B-001",
            scene_cp_id="CP-S-005",  # Wide shot — compatible
        )
        assert result["has_warnings"] is False

    def test_non_body_atoms_no_framing_check(self):
        validator = CompositionValidator()
        result = validator.validate_composition(
            body_cp_id="CP-B-014",  # Not in FULL_BODY_ATOMS set
            scene_cp_id="CP-S-001",
        )
        assert result["has_warnings"] is False
