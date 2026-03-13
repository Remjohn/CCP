"""
CCP Sacred Audio Ingestion API
Task 1.08 — FastAPI endpoint for uploading coach Sacred Audio recordings.

Receives audio files (OGG, MP3, M4A), validates format, stores in
Supabase Storage with SAUD Asset ID, and returns confirmation.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain

router = APIRouter()

SUPPORTED_FORMATS = {".ogg", ".mp3", ".m4a", ".wav", ".webm"}
MAX_FILE_SIZE_MB = 50
MIN_TOTAL_MINUTES = 10


@router.post("/sacred-audio/upload")
async def upload_sacred_audio(
    file: UploadFile = File(...),
    coach_acronym: str = "",
):
    """Upload a Sacred Audio recording for voice DNA extraction.

    Args:
        file: Audio file (OGG, MP3, M4A, WAV, or WebM)
        coach_acronym: 3-letter coach code (e.g. NDL)

    Returns:
        Confirmation with Asset ID and storage location.
    """
    # Validate coach acronym
    if not coach_acronym or len(coach_acronym) != 3:
        raise HTTPException(
            status_code=400,
            detail="coach_acronym must be exactly 3 letters",
        )

    coach_acronym = coach_acronym.upper()

    # Validate file format
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format: {ext}. Supported: {SUPPORTED_FORMATS}",
        )

    # Read file content
    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {file_size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB)",
        )

    # Generate Asset ID
    generator = AssetIDGenerator(coach_acronym=coach_acronym)
    asset_id = generator.generate(AssetType.SACRED_AUDIO)

    # Save locally (Supabase upload happens in a follow-up service)
    coach_dir = Path(f"coaches/{coach_acronym}/production/audio")
    coach_dir.mkdir(parents=True, exist_ok=True)
    local_path = coach_dir / f"{asset_id}{ext}"
    local_path.write_bytes(content)

    # Log to Receipt Chain
    receipt = ReceiptChain(coach_acronym=coach_acronym)
    entry = receipt.log(
        agent_id="sacred_audio_api",
        action="upload_sacred_audio",
        asset_id=asset_id,
        input_summary=f"Audio upload: {file.filename} ({file_size_mb:.1f}MB, {ext})",
        output_summary=f"Stored at {local_path}",
        decision="accepted",
        metadata={
            "original_filename": file.filename,
            "file_size_mb": round(file_size_mb, 2),
            "format": ext,
        },
    )

    return {
        "status": "uploaded",
        "asset_id": asset_id,
        "file_size_mb": round(file_size_mb, 2),
        "format": ext,
        "receipt_id": entry.receipt_id,
        "local_path": str(local_path),
        "next_step": "Run Genesis Pipeline (ccf-init) to extract Voice DNA",
    }


@router.get("/sacred-audio/list/{coach_acronym}")
async def list_sacred_audio(coach_acronym: str):
    """List all Sacred Audio files for a coach."""
    coach_acronym = coach_acronym.upper()
    audio_dir = Path(f"coaches/{coach_acronym}/production/audio")

    if not audio_dir.exists():
        return {"coach_acronym": coach_acronym, "files": []}

    files = []
    for f in sorted(audio_dir.glob("SAUD-*")):
        files.append(
            {
                "filename": f.name,
                "asset_id": f.stem,
                "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                "format": f.suffix,
            }
        )

    return {"coach_acronym": coach_acronym, "file_count": len(files), "files": files}
