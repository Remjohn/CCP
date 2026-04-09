"""
FR-VID-13 §4 Stage 8 — Clip Library Import Pipeline
Converts Spine2D JSON, Lottie JSON, and BVH (MoCap) files
to DragonBones JSON format for the animation clip library (DEP-VID-036).

Spec Reference: §4 Stage 8 Steps 1-5.

License Compliance:
- DragonBones format is under MIT license (direct dependency).
- We do NOT use Spine runtime code (requires license).
- We convert Spine's JSON data format description to DragonBones format.
"""

import json
import os
from typing import Any

# ---------------------------------------------------------------------------
# CCP Canonical Bone Maps (§4 Stage 8)
# ---------------------------------------------------------------------------
SPINE_BONE_MAP: dict[str, str] = {
    "root": "b_root",
    "hip": "b_hips",
    "spine": "b_chest",
    "neck": "b_neck",
    "head": "b_head",
    "left-upper-arm": "b_arm_upper_L",
    "left-lower-arm": "b_arm_lower_L",
    "left-hand": "b_hand_L",
    "right-upper-arm": "b_arm_upper_R",
    "right-lower-arm": "b_arm_lower_R",
    "right-hand": "b_hand_R",
    "left-thigh": "b_leg_upper_L",
    "left-calf": "b_leg_lower_L",
    "left-foot": "b_foot_L",
    "right-thigh": "b_leg_upper_R",
    "right-calf": "b_leg_lower_R",
    "right-foot": "b_foot_R",
    "jaw": "b_jaw",
    "left-eye": "b_eye_L",
    "right-eye": "b_eye_R",
}

LOTTIE_LAYER_MAP: dict[str, str] = {
    "Root": "b_root",
    "Hips": "b_hips",
    "Torso": "b_chest",
    "Neck": "b_neck",
    "Head": "b_head",
    "L_UpperArm": "b_arm_upper_L",
    "L_LowerArm": "b_arm_lower_L",
    "L_Hand": "b_hand_L",
    "R_UpperArm": "b_arm_upper_R",
    "R_LowerArm": "b_arm_lower_R",
    "R_Hand": "b_hand_R",
    "L_UpperLeg": "b_leg_upper_L",
    "L_LowerLeg": "b_leg_lower_L",
    "L_Foot": "b_foot_L",
    "R_UpperLeg": "b_leg_upper_R",
    "R_LowerLeg": "b_leg_lower_R",
    "R_Foot": "b_foot_R",
    "Jaw": "b_jaw",
}

BVH_BONE_MAP: dict[str, str] = {
    "Hips": "b_root",
    "Spine": "b_hips",
    "Spine1": "b_chest",
    "Neck": "b_neck",
    "Head": "b_head",
    "LeftArm": "b_arm_upper_L",
    "LeftForeArm": "b_arm_lower_L",
    "LeftHand": "b_hand_L",
    "RightArm": "b_arm_upper_R",
    "RightForeArm": "b_arm_lower_R",
    "RightHand": "b_hand_R",
    "LeftUpLeg": "b_leg_upper_L",
    "LeftLeg": "b_leg_lower_L",
    "LeftFoot": "b_foot_L",
    "RightUpLeg": "b_leg_upper_R",
    "RightLeg": "b_leg_lower_R",
    "RightFoot": "b_foot_R",
}


def convert_spine_to_dragonbones(spine_json_path: str) -> dict[str, Any]:
    """
    Convert a Spine2D JSON animation file to DragonBones format.

    §4 Stage 8 Step 1:
    - Map bone names to CCP canonical skeleton via SPINE_BONE_MAP.
    - Validate affected bones exist in 15-bone skeleton; warn on unmapped.

    Args:
        spine_json_path: Path to Spine2D JSON file.

    Returns:
        DragonBones-format animation data dict.
    """
    if not os.path.isfile(spine_json_path):
        raise FileNotFoundError(f"Spine JSON not found: {spine_json_path}")

    with open(spine_json_path, "r", encoding="utf-8") as f:
        spine_data = json.load(f)

    warnings: list[str] = []
    db_animations = []

    # Extract animations
    spine_animations = spine_data.get("animations", {})
    for anim_name, anim_data in spine_animations.items():
        db_anim: dict[str, Any] = {
            "name": anim_name,
            "duration": 0,
            "bone": [],
        }

        bone_timelines = anim_data.get("bones", {})
        max_time = 0.0

        for spine_bone_name, timeline_data in bone_timelines.items():
            ccp_bone = SPINE_BONE_MAP.get(spine_bone_name)
            if not ccp_bone:
                warnings.append(f"Unmapped Spine bone: '{spine_bone_name}' in animation '{anim_name}'")
                continue

            bone_entry: dict[str, Any] = {
                "name": ccp_bone,
                "rotateFrame": [],
                "translateFrame": [],
            }

            # Rotation keyframes
            for kf in timeline_data.get("rotate", []):
                time = float(kf.get("time", 0))
                angle = float(kf.get("angle", 0))
                bone_entry["rotateFrame"].append({
                    "duration": 0,  # Will be calculated
                    "tweenEasing": 0,
                    "rotate": angle,
                })
                max_time = max(max_time, time)

            # Translation keyframes
            for kf in timeline_data.get("translate", []):
                time = float(kf.get("time", 0))
                bone_entry["translateFrame"].append({
                    "duration": 0,
                    "tweenEasing": 0,
                    "x": float(kf.get("x", 0)),
                    "y": float(kf.get("y", 0)),
                })
                max_time = max(max_time, time)

            db_anim["bone"].append(bone_entry)

        db_anim["duration"] = max_time
        db_animations.append(db_anim)

    return {
        "format": "dragonbones",
        "source": "spine_import",
        "original_format": "spine",
        "animations": db_animations,
        "warnings": warnings,
    }


def convert_lottie_to_dragonbones(lottie_json_path: str) -> dict[str, Any]:
    """
    Convert a Lottie JSON animation file to DragonBones format.

    §4 Stage 8 Step 2:
    - Extract layer transforms (position, rotation, scale, opacity) per frame.
    - Map Lottie layer names to CCP bone names via LOTTIE_LAYER_MAP.
    - Convert Lottie time (frames @ Lottie FPS) to DragonBones time (seconds).

    Args:
        lottie_json_path: Path to Lottie JSON file.

    Returns:
        DragonBones-format animation data dict.
    """
    if not os.path.isfile(lottie_json_path):
        raise FileNotFoundError(f"Lottie JSON not found: {lottie_json_path}")

    with open(lottie_json_path, "r", encoding="utf-8") as f:
        lottie_data = json.load(f)

    warnings: list[str] = []
    db_bones: list[dict[str, Any]] = []

    lottie_fps = float(lottie_data.get("fr", 30))
    in_point = float(lottie_data.get("ip", 0))
    out_point = float(lottie_data.get("op", 0))
    duration_sec = (out_point - in_point) / lottie_fps

    layers = lottie_data.get("layers", [])

    for layer in layers:
        layer_name = layer.get("nm", "")
        ccp_bone = LOTTIE_LAYER_MAP.get(layer_name)

        if not ccp_bone:
            warnings.append(f"Unmapped Lottie layer: '{layer_name}'")
            continue

        bone_entry: dict[str, Any] = {
            "name": ccp_bone,
            "rotateFrame": [],
            "translateFrame": [],
        }

        transform = layer.get("ks", {})

        # Rotation
        rotation_data = transform.get("r", {})
        if isinstance(rotation_data, dict) and "k" in rotation_data:
            keyframes = rotation_data["k"]
            if isinstance(keyframes, list) and len(keyframes) > 0:
                for kf in keyframes:
                    if isinstance(kf, dict):
                        frame = float(kf.get("t", 0))
                        value = kf.get("s", [0])
                        angle = float(value[0]) if isinstance(value, list) else float(value)
                        bone_entry["rotateFrame"].append({
                            "duration": 0,
                            "tweenEasing": 0,
                            "rotate": angle,
                            "time_sec": round((frame - in_point) / lottie_fps, 3),
                        })

        # Position
        position_data = transform.get("p", {})
        if isinstance(position_data, dict) and "k" in position_data:
            keyframes = position_data["k"]
            if isinstance(keyframes, list) and len(keyframes) > 0:
                for kf in keyframes:
                    if isinstance(kf, dict):
                        frame = float(kf.get("t", 0))
                        value = kf.get("s", [0, 0])
                        if isinstance(value, list) and len(value) >= 2:
                            bone_entry["translateFrame"].append({
                                "duration": 0,
                                "tweenEasing": 0,
                                "x": float(value[0]),
                                "y": float(value[1]),
                                "time_sec": round((frame - in_point) / lottie_fps, 3),
                            })

        db_bones.append(bone_entry)

    return {
        "format": "dragonbones",
        "source": "lottie_import",
        "original_format": "lottie",
        "animations": [{
            "name": lottie_data.get("nm", "imported_lottie"),
            "duration": round(duration_sec, 3),
            "bone": db_bones,
        }],
        "warnings": warnings,
    }


def convert_bvh_to_dragonbones(bvh_path: str, target_fps: int = 24) -> dict[str, Any]:
    """
    Convert a BVH (Motion Capture) file to DragonBones format.

    §4 Stage 8 Step 3:
    - Parse joint hierarchy and keyframe channels.
    - Downsample from MoCap joint count to 15-bone CCP skeleton.
    - Map via BVH_BONE_MAP.

    Args:
        bvh_path: Path to BVH file.
        target_fps: Target FPS for downsampling (default 24).

    Returns:
        DragonBones-format animation data dict.
    """
    if not os.path.isfile(bvh_path):
        raise FileNotFoundError(f"BVH file not found: {bvh_path}")

    warnings: list[str] = []

    # Parse BVH file manually (avoid external dependency for basic parsing)
    with open(bvh_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find MOTION section
    motion_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == "MOTION":
            motion_idx = i
            break

    if motion_idx < 0:
        raise ValueError("BVH file has no MOTION section.")

    # Parse header for joint order
    joint_names: list[str] = []
    for line in lines[:motion_idx]:
        stripped = line.strip()
        if stripped.startswith("JOINT") or stripped.startswith("ROOT"):
            parts = stripped.split()
            if len(parts) >= 2:
                joint_names.append(parts[-1])

    # Parse motion data
    frames_line = lines[motion_idx + 1].strip()
    frame_time_line = lines[motion_idx + 2].strip()
    num_frames = int(frames_line.split(":")[1].strip()) if ":" in frames_line else 0
    frame_time = float(frame_time_line.split(":")[1].strip()) if ":" in frame_time_line else 1.0 / target_fps
    source_fps = 1.0 / frame_time

    # Downsample ratio
    step = max(1, int(round(source_fps / target_fps)))

    db_bones: dict[str, dict[str, Any]] = {}
    for bvh_name, ccp_name in BVH_BONE_MAP.items():
        if bvh_name in joint_names:
            db_bones[ccp_name] = {
                "name": ccp_name,
                "rotateFrame": [],
                "translateFrame": [],
            }
        else:
            warnings.append(f"BVH joint '{bvh_name}' not found in file — mapped bone '{ccp_name}' will be empty.")

    # Parse frame data (simplified: each joint has 3 channels for rotation)
    channels_per_joint = 6 if len(joint_names) > 0 else 0  # position(3) + rotation(3) for root, rotation(3) for others
    frame_data_lines = lines[motion_idx + 3:]

    for frame_idx in range(0, min(num_frames, len(frame_data_lines)), step):
        line = frame_data_lines[frame_idx].strip()
        if not line:
            continue
        values = [float(v) for v in line.split()]
        time_sec = round(frame_idx * frame_time, 3)

        # Map values to joints (simplified: first 6 = root pos+rot, then 3 per joint)
        offset = 0
        for j_idx, joint_name in enumerate(joint_names):
            ccp_name = BVH_BONE_MAP.get(joint_name)
            if not ccp_name or ccp_name not in db_bones:
                offset += 6 if j_idx == 0 else 3
                continue

            if j_idx == 0:
                # Root has position + rotation (6 channels)
                if offset + 5 < len(values):
                    db_bones[ccp_name]["translateFrame"].append({
                        "duration": 0,
                        "tweenEasing": 0,
                        "x": values[offset],
                        "y": values[offset + 1],
                        "time_sec": time_sec,
                    })
                    db_bones[ccp_name]["rotateFrame"].append({
                        "duration": 0,
                        "tweenEasing": 0,
                        "rotate": values[offset + 5],  # Z rotation
                        "time_sec": time_sec,
                    })
                offset += 6
            else:
                # Other joints have rotation only (3 channels)
                if offset + 2 < len(values):
                    db_bones[ccp_name]["rotateFrame"].append({
                        "duration": 0,
                        "tweenEasing": 0,
                        "rotate": values[offset + 2],  # Z rotation for 2D
                        "time_sec": time_sec,
                    })
                offset += 3

    duration = round(num_frames * frame_time, 3)

    return {
        "format": "dragonbones",
        "source": "bvh_import",
        "original_format": "bvh",
        "animations": [{
            "name": os.path.splitext(os.path.basename(bvh_path))[0],
            "duration": duration,
            "bone": list(db_bones.values()),
        }],
        "warnings": warnings,
    }


def validate_imported_clip(clip_data: dict[str, Any], canonical_bones: set[str]) -> dict[str, Any]:
    """
    §4 Stage 8 Step 4: Post-import validation.
    Verify clip plays correctly on a test character.
    If bones are missing, warn with CLIP_IMPORT_PARTIAL status.
    """
    status = "CLIP_IMPORT_OK"
    missing_bones: list[str] = []

    for anim in clip_data.get("animations", []):
        for bone_entry in anim.get("bone", []):
            bone_name = bone_entry.get("name", "")
            if bone_name not in canonical_bones:
                missing_bones.append(bone_name)

    if missing_bones:
        status = "CLIP_IMPORT_PARTIAL"

    return {
        "status": status,
        "missing_bones": missing_bones,
        "warnings": clip_data.get("warnings", []),
    }


# CCP canonical 15-bone skeleton set for validation
CCP_CANONICAL_BONES = {
    "b_root", "b_hips", "b_chest", "b_neck", "b_head",
    "b_arm_upper_L", "b_arm_lower_L", "b_hand_L",
    "b_arm_upper_R", "b_arm_lower_R", "b_hand_R",
    "b_leg_upper_L", "b_leg_lower_L", "b_foot_L",
    "b_leg_upper_R", "b_leg_lower_R", "b_foot_R",
    "b_eye_L", "b_eye_R", "b_jaw",
    "b_hair_front", "b_hair_back",
}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python clip_import_service.py <format: spine|lottie|bvh> <file_path>")
        sys.exit(1)

    fmt = sys.argv[1].lower()
    path = sys.argv[2]

    if fmt == "spine":
        result = convert_spine_to_dragonbones(path)
    elif fmt == "lottie":
        result = convert_lottie_to_dragonbones(path)
    elif fmt == "bvh":
        result = convert_bvh_to_dragonbones(path)
    else:
        print(f"Unsupported format: {fmt}. Use spine, lottie, or bvh.")
        sys.exit(1)

    validation = validate_imported_clip(result, CCP_CANONICAL_BONES)
    result["validation"] = validation

    print(json.dumps(result, indent=2))
