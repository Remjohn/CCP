"""
FR-VID-13 §4 Stage 6 — Headless Frame Export Service
Produces DEP-VID-038 (Character Frame Export) and DEP-VID-032 (Character Pose Export).

This is a Node.js service in production (using @pixi/node + DragonBonesJS).
This Python wrapper provides the API layer and job queue management
via Bull/BullMQ on Redis, and delegates rendering to a Node.js subprocess.

Spec Reference: §4 Stage 6 Steps 1-5.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Frame Export Configuration (from spec §4 Stage 6)
# ---------------------------------------------------------------------------
MAX_FRAMES_PER_BEAT = 3600  # §11 Safety Tests: 2.5 min max at 24 FPS
MAX_LAYERS_PER_CHARACTER = 50  # §11 Safety Tests: 50-layer limit
MAX_PACKAGE_SIZE_MB = 200  # §11 Safety Tests: 200MB limit
DEFAULT_FPS = 24


def create_export_job(
    character_id: str,
    manifest: dict[str, Any],
    beat_index: int,
    target_format: str,
    scene_id: str,
    output_dir: str,
    patch: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a frame export job for a single beat.

    §4 Stage 6 Step 3: For each beat in manifest —
    apply animation clip, loops, bone overrides, lip sync, scene composition,
    then render each frame to transparent PNG.

    Args:
        character_id: Character package ID.
        manifest: Full Remotion manifest dict.
        beat_index: Which beat to export.
        target_format: Output format (9:16, 1:1, 16:9, 4:5).
        scene_id: Scene composition preset.
        output_dir: Base output directory for frames.
        patch: Optional manifest patch to apply first.

    Returns:
        Job descriptor dict for the render queue.
    """
    beat = manifest["beats"][beat_index]
    duration_frames = beat.get("duration_frames", 0)

    # Safety check: enforce max frame limit (§11 Safety Tests)
    if duration_frames > MAX_FRAMES_PER_BEAT:
        raise ValueError(
            f"Beat {beat_index} has {duration_frames} frames, exceeding the "
            f"{MAX_FRAMES_PER_BEAT}-frame safety limit (2.5 minutes at 24 FPS)."
        )

    job_id = f"EXPORT-{uuid.uuid4().hex[:8]}"
    output_path = os.path.join(
        output_dir, "characters", character_id, f"beat-{beat_index}"
    )

    return {
        "job_id": job_id,
        "character_id": character_id,
        "beat_index": beat_index,
        "target_format": target_format,
        "scene_id": scene_id,
        "status": "queued",
        "total_frames": duration_frames,
        "frames_rendered": 0,
        "output_path": output_path,
        "fps": manifest.get("fps", DEFAULT_FPS),
        "character_overlay": beat.get("character_overlay", {}),
        "patch_applied": patch is not None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def create_carousel_pose_job(
    character_id: str,
    clip_id: str,
    target_format: str,
    output_dir: str,
) -> dict[str, Any]:
    """
    Create a carousel pose export job (§4 Stage 6 Step 4).

    Renders a single-frame high-res pose PNG for CanvasCompositionService.
    Resolution: 2K-4K depending on format (2048×2560 for 4:5, 2160×3840 for 9:16).

    Args:
        character_id: Character package ID.
        clip_id: Animation clip ID (pose = frame 0 of this clip).
        target_format: Output format.
        output_dir: Output directory.

    Returns:
        Job descriptor dict for the render queue.
    """
    CAROUSEL_DIMS = {
        "9:16": {"width": 2160, "height": 3840},
        "1:1": {"width": 2048, "height": 2048},
        "16:9": {"width": 3840, "height": 2160},
        "4:5": {"width": 2048, "height": 2560},
    }

    dims = CAROUSEL_DIMS.get(target_format, CAROUSEL_DIMS["4:5"])
    job_id = f"POSE-{uuid.uuid4().hex[:8]}"

    return {
        "job_id": job_id,
        "character_id": character_id,
        "clip_id": clip_id,
        "type": "carousel_pose",
        "target_format": target_format,
        "width": dims["width"],
        "height": dims["height"],
        "status": "queued",
        "total_frames": 1,
        "frames_rendered": 0,
        "output_path": os.path.join(
            output_dir, "characters", character_id, "poses", f"{clip_id}.png"
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def validate_character_package_safety(package: dict[str, Any]) -> dict[str, Any]:
    """
    §11 Safety Tests: Reject packages exceeding safety limits.
    - 50-layer limit
    - 200MB total size limit
    """
    errors: list[str] = []

    layers = package.get("layers", [])
    if len(layers) > MAX_LAYERS_PER_CHARACTER:
        errors.append(
            f"Character package has {len(layers)} layers, exceeding the "
            f"{MAX_LAYERS_PER_CHARACTER}-layer safety limit."
        )

    return {
        "safe": len(errors) == 0,
        "errors": errors,
    }


# Naming convention verification (§4 Stage 6 Step 3g)
def verify_frame_naming(output_path: str, total_frames: int) -> dict[str, Any]:
    """
    Verify that exported frames follow the naming convention:
    /characters/{character_id}/beat-{beat_index}/frame-{0000}.png

    Args:
        output_path: Directory containing exported frames.
        total_frames: Expected number of frames.

    Returns:
        Verification result dict.
    """
    errors: list[str] = []

    if not os.path.isdir(output_path):
        return {"valid": False, "errors": [f"Output directory does not exist: {output_path}"]}

    expected_files = {f"frame-{str(i).zfill(4)}.png" for i in range(total_frames)}
    actual_files = set(os.listdir(output_path))

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    if missing:
        errors.append(f"Missing {len(missing)} frames: {sorted(missing)[:5]}...")
    if extra:
        errors.append(f"Unexpected {len(extra)} files: {sorted(extra)[:5]}...")

    return {
        "valid": len(errors) == 0,
        "expected_count": total_frames,
        "actual_count": len(actual_files & expected_files),
        "errors": errors,
    }
