"""
FR-VID-13 — Animation Studio API (FastAPI)
Provides endpoints for BPM detection, lip sync generation, frame export,
clip import, and health checks.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.bpm_service import detect_bpm
from services.lip_sync_service import generate_lip_sync
from services.frame_export_service import (
    create_export_job,
    create_carousel_pose_job,
    validate_character_package_safety,
    verify_frame_naming,
)
from services.clip_import_service import (
    convert_spine_to_dragonbones,
    convert_lottie_to_dragonbones,
    convert_bvh_to_dragonbones,
    validate_imported_clip,
    CCP_CANONICAL_BONES,
)

app = FastAPI(
    title="CCP Animation Studio API",
    description="Backend services for FR-VID-13 Animation Studio",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health Check (Gate O Q6: Export Pipeline Ready) ---
@app.get("/api/export/health")
async def export_health():
    """Health check endpoint consumed by Gate O Q6."""
    return {"status": "healthy", "service": "animation-render-service", "timestamp": datetime.now(timezone.utc).isoformat()}


# --- BPM Detection (Stage 3) ---
class BPMRequest(BaseModel):
    audio_path: str


@app.post("/api/bpm/detect")
async def api_detect_bpm(request: BPMRequest):
    """Detect BPM from a music track. Produces DEP-VID-034."""
    try:
        result = detect_bpm(request.audio_path)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BPM detection failed: {e}")


# --- Lip Sync (Stage 4) ---
class LipSyncRequest(BaseModel):
    audio_path: str
    fps: int = 24
    beat_start_sec: float
    beat_duration_sec: float


@app.post("/api/lip-sync/generate")
async def api_generate_lip_sync(request: LipSyncRequest):
    """Generate b_jaw rotation keyframes from voiceover amplitude."""
    try:
        keyframes = generate_lip_sync(
            request.audio_path,
            request.fps,
            request.beat_start_sec,
            request.beat_duration_sec,
        )
        return {"keyframes": keyframes, "bone": "b_jaw", "frame_count": len(keyframes)}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lip sync generation failed: {e}")


# --- Frame Export (Stage 6) ---
class FrameExportRequest(BaseModel):
    character_id: str
    manifest: dict[str, Any]
    beat_index: int
    target_format: str
    scene_id: str
    output_dir: str
    patch: dict[str, Any] | None = None


@app.post("/api/export/frames")
async def api_create_frame_export_job(request: FrameExportRequest):
    """Create a frame export job. Produces DEP-VID-038."""
    try:
        job = create_export_job(
            request.character_id,
            request.manifest,
            request.beat_index,
            request.target_format,
            request.scene_id,
            request.output_dir,
            request.patch,
        )
        return job
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=400, detail=str(e))


class PoseExportRequest(BaseModel):
    character_id: str
    clip_id: str
    target_format: str
    output_dir: str


@app.post("/api/export/pose")
async def api_create_pose_export_job(request: PoseExportRequest):
    """Create a carousel pose export job. Produces DEP-VID-032."""
    job = create_carousel_pose_job(
        request.character_id,
        request.clip_id,
        request.target_format,
        request.output_dir,
    )
    return job


# --- Clip Import (Stage 8) ---
class ClipImportRequest(BaseModel):
    format: str  # "spine", "lottie", "bvh"
    file_path: str


@app.post("/api/clips/import")
async def api_import_clip(request: ClipImportRequest):
    """Import an animation clip from external format. Updates DEP-VID-036."""
    try:
        if request.format == "spine":
            result = convert_spine_to_dragonbones(request.file_path)
        elif request.format == "lottie":
            result = convert_lottie_to_dragonbones(request.file_path)
        elif request.format == "bvh":
            result = convert_bvh_to_dragonbones(request.file_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {request.format}")

        validation = validate_imported_clip(result, CCP_CANONICAL_BONES)
        result["validation"] = validation
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clip import failed: {e}")


# --- Safety Validation ---
@app.post("/api/safety/validate-package")
async def api_validate_package_safety(package: dict[str, Any]):
    """Validate character package against safety limits (§11)."""
    return validate_character_package_safety(package)
