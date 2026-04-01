"""
FR-VIS-15 — ConsciousPose Body Language Library
Build Step 29 · DEP-VIS-010

298 composable atoms across 9 layers, composition resolver,
ControlNet map resolver, manifest system, mood-state queries.

§10 Testing: CP-ID validation, composition validation, manifest checksum,
framing mismatch, path traversal safety.
"""

from __future__ import annotations

import hashlib
import os
import re
from typing import Any

from core.commercial_models import build_receipt, compute_receipt_hash
from core.visual_models import (
    CONTROLNET_DEFAULT_STRENGTH,
    RECEIPT_STAGE_COMPOSITION_RESOLVE,
    RECEIPT_STAGE_POSE_RESOLVE,
    CompositionType,
    ManifestEntry,
    PoseAtom,
    PoseComposition,
    PoseLayer,
    PoseSpec,
    RenderStatus,
    SourceLibrary,
    VisualPipelineError,
)


# =====================================================
#  Pose Atom Registry
# =====================================================

class PoseAtomRegistry:
    """
    §4 Stage 1: Atom Registry — 298 composable atoms across 9 layers.
    Provides mood-state query, archetype query, layer-based filtering.
    """

    def __init__(self) -> None:
        self._atoms: dict[str, PoseAtom] = {}  # keyed by cp_id

    def register_atom(self, atom: PoseAtom) -> None:
        """Register a single pose atom."""
        self._atoms[atom.cp_id] = atom

    def register_atoms(self, atoms: list[PoseAtom]) -> int:
        """Bulk register atoms. Returns count registered."""
        for atom in atoms:
            self._atoms[atom.cp_id] = atom
        return len(atoms)

    def get_atom(self, cp_id: str) -> PoseAtom:
        """
        §10 Unit Test: CP-ID Validation.
        Raises INVALID_CP_ID for non-existent atoms.
        """
        atom = self._atoms.get(cp_id)
        if atom is None:
            raise VisualPipelineError(
                code="INVALID_CP_ID",
                message=f"Pose atom '{cp_id}' does not exist in the registry.",
            )
        return atom

    def get_atoms_by_layer(self, layer: PoseLayer) -> list[PoseAtom]:
        """Get all atoms for a specific layer."""
        return [a for a in self._atoms.values() if a.layer == layer]

    def get_atoms_by_mood(self, mood_state: str) -> list[PoseAtom]:
        """
        §8 AC4: Mood-State Query.
        Uses GIN-equivalent filtering on mood_fit list.
        """
        return [a for a in self._atoms.values() if mood_state in a.mood_fit]

    def get_atoms_by_archetype(self, archetype: str) -> list[PoseAtom]:
        """Query atoms by archetype fit."""
        return [a for a in self._atoms.values() if archetype in a.archetype_fit]

    def get_rendered_atoms(self) -> list[PoseAtom]:
        """Get atoms with rendered ControlNet assets."""
        return [a for a in self._atoms.values() if a.has_rendered_assets]

    def count(self) -> int:
        return len(self._atoms)

    def count_by_layer(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for atom in self._atoms.values():
            key = atom.layer.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    def count_by_source(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for atom in self._atoms.values():
            key = atom.source_library.value
            counts[key] = counts.get(key, 0) + 1
        return counts


# =====================================================
#  Composition Resolver
# =====================================================

class CompositionRegistry:
    """
    §4 Stage 1: Composition Registry — archetype defaults + memetic recipes.
    Resolves composition_id → 7-layer CP-ID decomposition.
    """

    def __init__(self, atom_registry: PoseAtomRegistry) -> None:
        self._atom_registry = atom_registry
        self._compositions: dict[str, PoseComposition] = {}

    def register_composition(self, comp: PoseComposition) -> None:
        self._compositions[comp.composition_id] = comp

    def resolve(self, composition_id: str) -> PoseComposition:
        """
        §8 AC2: Composition Resolution.
        Returns the correct 7-layer CP-ID decomposition.
        """
        comp = self._compositions.get(composition_id)
        if comp is None:
            raise VisualPipelineError(
                code="COMPOSITION_NOT_FOUND",
                message=f"Composition '{composition_id}' not found.",
            )
        return comp

    def get_compositions_by_type(self, comp_type: CompositionType) -> list[PoseComposition]:
        return [c for c in self._compositions.values() if c.composition_type == comp_type]

    def get_compositions_by_archetype(self, archetype: str) -> list[PoseComposition]:
        return [c for c in self._compositions.values() if c.archetype_family == archetype]

    def count(self) -> int:
        return len(self._compositions)


# =====================================================
#  ControlNet Map Resolver
# =====================================================

class ControlNetMapResolver:
    """
    §4 Stage 6: Resolves CP-IDs to EFS file paths.
    Validates paths, prevents path traversal, checks manifest.
    """

    EFS_BASE = "/efs/ccp-models/controlnet"
    ALLOWED_PREFIXES = ("/efs/ccp-models/controlnet/",)

    def __init__(self, atom_registry: PoseAtomRegistry) -> None:
        self._atom_registry = atom_registry
        self._manifest: dict[str, ManifestEntry] = {}  # file_path → entry
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def build_manifest(self, entries: list[ManifestEntry]) -> int:
        """Build manifest from list of entries. Returns count."""
        for entry in entries:
            self._manifest[entry.file_path] = entry
        return len(entries)

    def resolve_depth_path(self, cp_id: str, scene_cp_id: str | None = None) -> str:
        """Resolve CP-ID to depth map path."""
        atom = self._atom_registry.get_atom(cp_id)
        if atom.controlnet_depth_path:
            return atom.controlnet_depth_path
        # Build default path
        scene_suffix = f"_{scene_cp_id}" if scene_cp_id else ""
        return f"{self.EFS_BASE}/{atom.layer.value}/{cp_id}{scene_suffix}_depth.png"

    def resolve_openpose_path(self, cp_id: str, scene_cp_id: str | None = None) -> str:
        """Resolve CP-ID to openpose map path."""
        atom = self._atom_registry.get_atom(cp_id)
        if atom.controlnet_openpose_path:
            return atom.controlnet_openpose_path
        scene_suffix = f"_{scene_cp_id}" if scene_cp_id else ""
        return f"{self.EFS_BASE}/{atom.layer.value}/{cp_id}{scene_suffix}_openpose.png"

    def resolve_pose_spec(self, spec: PoseSpec) -> dict[str, str | None]:
        """
        Resolve a full PoseSpec to file paths.
        Returns dict with depth/openpose paths.
        """
        paths: dict[str, str | None] = {
            "controlnet_depth": None,
            "controlnet_openpose": None,
        }

        body_id = spec.body or spec.composition_id
        if spec.composition_id:
            # Resolve from composition
            pass  # Composition provides composed paths

        if spec.body:
            paths["controlnet_depth"] = self.resolve_depth_path(spec.body, spec.scene)
            paths["controlnet_openpose"] = self.resolve_openpose_path(spec.body, spec.scene)

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_POSE_RESOLVE,
            agent_name="controlnet_map_resolver",
            input_payload={"pose_spec": spec.model_dump()},
            output_payload=paths,
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return paths

    def sanitize_path(self, path: str) -> str:
        """
        §10 Safety: Path Traversal Prevention.
        Rejects non-EFS paths, normalizes traversal attempts.
        """
        # Normalize
        normalized = os.path.normpath(path).replace("\\", "/")

        # Check for traversal attempts
        if ".." in normalized:
            raise VisualPipelineError(
                code="PATH_TRAVERSAL_BLOCKED",
                message=f"Path traversal attempt detected: {path}",
            )

        # Check prefix
        if not any(normalized.startswith(prefix) for prefix in self.ALLOWED_PREFIXES):
            raise VisualPipelineError(
                code="INVALID_PATH",
                message=f"Path not in allowed EFS directory: {path}",
            )

        return normalized

    def validate_manifest(self, file_paths_on_disk: list[str]) -> dict[str, Any]:
        """
        §8 AC6: Manifest Integrity.
        Cross-check manifest against actual files.
        """
        manifest_paths = set(self._manifest.keys())
        disk_paths = set(file_paths_on_disk)

        missing_on_disk = manifest_paths - disk_paths
        orphans_on_disk = disk_paths - manifest_paths

        return {
            "valid": len(missing_on_disk) == 0 and len(orphans_on_disk) == 0,
            "total_manifest_entries": len(manifest_paths),
            "total_files_on_disk": len(disk_paths),
            "missing_on_disk": list(missing_on_disk),
            "orphans_on_disk": list(orphans_on_disk),
        }

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  Composition Validator
# =====================================================

class CompositionValidator:
    """
    §10 Unit Test: Composition Validation.
    Validates framing compatibility between layers.
    """

    # Scene atoms defining extreme close-ups (incompatible with full body)
    CLOSEUP_SCENES = {"CP-S-001", "CP-S-002", "CP-S-003"}
    # Body atoms requiring wide framing
    FULL_BODY_ATOMS = {"CP-B-001", "CP-B-002", "CP-B-003", "CP-B-004", "CP-B-005", "CP-B-006"}

    def validate_composition(
        self,
        body_cp_id: str | None,
        scene_cp_id: str | None,
        hands_cp_id: str | None = None,
        gaze_cp_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Check composition compatibility.
        Returns validation result with warnings.
        """
        warnings: list[str] = []
        valid = True

        # Framing mismatch: extreme closeup + full body
        if scene_cp_id in self.CLOSEUP_SCENES and body_cp_id in self.FULL_BODY_ATOMS:
            warnings.append(
                f"FRAMING_MISMATCH: {scene_cp_id} (extreme closeup) is incompatible "
                f"with {body_cp_id} (full body standing). Use a wider framing."
            )

        return {
            "valid": valid,
            "warnings": warnings,
            "has_warnings": len(warnings) > 0,
        }
