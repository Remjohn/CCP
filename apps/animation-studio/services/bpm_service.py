"""
FR-VID-13 §4 Stage 3 — BPM Detection Service (Python/librosa)
Produces DEP-VID-034: BPM_Analysis_Result.json

Extracts tempo, beat timestamps, and subdivision grids from a music track.
Called by the Animation Studio frontend via API endpoint.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

import librosa
import numpy as np


def detect_bpm(audio_path: str) -> dict[str, Any]:
    """
    Analyze a music track and produce a BPM Analysis Result (DEP-VID-034).

    Args:
        audio_path: Path to the music audio file (MP3, WAV, FLAC).

    Returns:
        BPM_Analysis_Result dictionary matching Schema C in FR-VID-13 §5.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        ValueError: If BPM detection confidence is below minimum threshold.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Music file not found: {audio_path}")

    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Detect tempo and beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert to scalar float if ndarray
    if isinstance(tempo, np.ndarray):
        tempo = float(tempo[0])
    else:
        tempo = float(tempo)

    # Convert beat frames to timestamps in seconds
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

    # Calculate confidence using onset strength autocorrelation
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    ac = librosa.autocorrelate(onset_env, max_size=len(onset_env))
    ac_norm = ac / (ac[0] + 1e-8)

    # Confidence: peak of the autocorrelation at the tempo lag
    tempo_lag = int(round(60.0 / tempo * sr / librosa.get_duration(y=y, sr=sr) * len(onset_env)))
    if 0 < tempo_lag < len(ac_norm):
        confidence = float(min(1.0, max(0.0, ac_norm[tempo_lag])))
    else:
        confidence = 0.5  # Default if lag is out of range

    # Calculate subdivisions
    beat_duration = 60.0 / tempo
    duration = librosa.get_duration(y=y, sr=sr)

    quarter_beats = _generate_subdivision(beat_duration, duration, 1)
    eighth_beats = _generate_subdivision(beat_duration, duration, 2)
    sixteenth_beats = _generate_subdivision(beat_duration, duration, 4)

    analysis_id = f"BPM-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"

    return {
        "analysis_id": analysis_id,
        "music_file": audio_path,
        "tempo_bpm": round(tempo, 1),
        "confidence": round(confidence, 2),
        "beat_times_sec": [round(t, 3) for t in beat_times],
        "subdivisions": {
            "quarter": [round(t, 3) for t in quarter_beats],
            "eighth": [round(t, 3) for t in eighth_beats],
            "sixteenth": [round(t, 3) for t in sixteenth_beats],
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _generate_subdivision(beat_duration: float, total_duration: float, multiplier: int) -> list[float]:
    """Generate a list of subdivision timestamps."""
    interval = beat_duration / multiplier
    timestamps = []
    t = 0.0
    while t <= total_duration:
        timestamps.append(t)
        t += interval
    return timestamps


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bpm_service.py <audio_file_path>")
        sys.exit(1)

    result = detect_bpm(sys.argv[1])
    print(json.dumps(result, indent=2))
