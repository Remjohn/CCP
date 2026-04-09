"""
FR-VID-13 §4 Stage 4 — Lip Sync Engine (Python Backend)
Extracts audio amplitude envelope and converts to b_jaw rotation keyframes.
Spec Reference: §4 Stage 4 Steps 1-5 — exact algorithm from spec.

This module is the EXACT code from the spec with production hardening.
Maximum jaw rotation: -20.0° (fully open).
Rest position: 0° rotation.
"""

import json
import os
from typing import Any

import librosa
import numpy as np


def generate_lip_sync(
    audio_path: str,
    fps: int,
    beat_start_sec: float,
    beat_duration_sec: float,
) -> list[dict[str, Any]]:
    """
    Generate b_jaw rotation keyframes from voiceover audio amplitude.

    This is the exact algorithm from FR-VID-13 §4 Stage 4 Step 1:
    - Extract audio amplitude envelope per frame using librosa RMS.
    - Map amplitude to jaw rotation: -20.0 * min(1.0, amplitude / max_amplitude).
    - Open during speech (negative rotation), closed during silence (0°).

    Args:
        audio_path: Path to the voiceover audio file.
        fps: Frames per second (typically 24).
        beat_start_sec: Start time of the beat in the audio (seconds).
        beat_duration_sec: Duration of the beat (seconds).

    Returns:
        List of keyframes: [{"frame": int, "bone": "b_jaw", "rotation": float}, ...]

    Raises:
        FileNotFoundError: If the audio file does not exist.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Voiceover audio not found: {audio_path}")

    # Load the specific beat segment
    y, sr = librosa.load(audio_path, offset=beat_start_sec, duration=beat_duration_sec)

    # Calculate hop length to get one RMS value per frame
    hop_length = sr // fps

    # Extract RMS (Root Mean Square) amplitude envelope
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]

    # Generate jaw keyframes — exact spec algorithm
    jaw_keyframes: list[dict[str, Any]] = []
    for i, amplitude in enumerate(rms):
        # Map amplitude to rotation: 0° (closed) to -20° (fully open)
        rotation = -20.0 * min(1.0, float(amplitude) / (float(rms.max()) + 1e-8))
        jaw_keyframes.append({
            "frame": i,
            "bone": "b_jaw",
            "rotation": round(rotation, 2),
        })

    return jaw_keyframes


def lip_sync_to_json(keyframes: list[dict[str, Any]]) -> str:
    """Serialize lip sync keyframes to JSON."""
    return json.dumps(keyframes, indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print("Usage: python lip_sync_service.py <audio_path> <fps> <beat_start_sec> <beat_duration_sec>")
        sys.exit(1)

    kf = generate_lip_sync(
        audio_path=sys.argv[1],
        fps=int(sys.argv[2]),
        beat_start_sec=float(sys.argv[3]),
        beat_duration_sec=float(sys.argv[4]),
    )
    print(lip_sync_to_json(kf))
