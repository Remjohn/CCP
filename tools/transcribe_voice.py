"""
Voice Note Transcription Tool (CCP L1: Perception — Sacred Audio Pipeline)
Pattern: firecrawl_wrapper.py
CCP Integration: Used by coach-elicitation for Sacred Audio Mode
TODO: Add Sacred Audio metadata extraction (emotional_tone, energy_level, pause_pattern)

Usage:
  python transcribe_voice.py transcribe "path/to/audio.m4a"
  python transcribe_voice.py batch "path/to/voice_notes_dir/"

Requires: GROQ_API_KEY environment variable (for Groq Whisper)
Fallback: Uses local whisper if GROQ_API_KEY not set (requires `pip install openai-whisper`)
"""

import os
import argparse
import json
import sys
from pathlib import Path

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
SUPPORTED_EXTENSIONS = {".m4a", ".ogg", ".mp3", ".wav", ".webm", ".mp4"}


def transcribe_groq(file_path: str):
    """Transcribe audio using Groq Whisper API (fast, cloud-based)."""
    try:
        import requests

        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }

        with open(file_path, "rb") as audio_file:
            files = {
                "file": (os.path.basename(file_path), audio_file),
            }
            data = {
                "model": "whisper-large-v3",
                "response_format": "verbose_json",
                "language": "auto"
            }

            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()

    except Exception as e:
        return {"error": f"Groq transcription failed: {str(e)}"}


def transcribe_local(file_path: str):
    """Transcribe audio using local Whisper model (slower, offline)."""
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return {
            "text": result["text"],
            "segments": result.get("segments", []),
            "language": result.get("language", "unknown"),
            "duration": result.get("duration", 0)
        }
    except ImportError:
        return {"error": "Local whisper not installed. Run: pip install openai-whisper"}
    except Exception as e:
        return {"error": f"Local transcription failed: {str(e)}"}


def transcribe_file(file_path: str):
    """Transcribe a single audio file."""
    path = Path(file_path)

    if not path.exists():
        print(json.dumps({"error": f"File not found: {file_path}"}))
        return

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(json.dumps({"error": f"Unsupported format: {path.suffix}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"}))
        return

    # Try Groq first (fast), fall back to local
    if GROQ_API_KEY:
        result = transcribe_groq(file_path)
    else:
        print(json.dumps({"warning": "GROQ_API_KEY not set, using local whisper (slower)"}), file=sys.stderr)
        result = transcribe_local(file_path)

    output = {
        "file": str(path.name),
        "file_path": str(path.absolute()),
        "file_size_mb": round(path.stat().st_size / (1024 * 1024), 2),
        "backend": "groq" if GROQ_API_KEY else "local_whisper",
        "transcription": result
    }

    print(json.dumps(output, indent=2))


def batch_transcribe(directory: str):
    """Transcribe all audio files in a directory."""
    dir_path = Path(directory)

    if not dir_path.exists():
        print(json.dumps({"error": f"Directory not found: {directory}"}))
        return

    audio_files = [f for f in dir_path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]

    if not audio_files:
        print(json.dumps({"error": f"No audio files found in {directory}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"}))
        return

    results = []
    for audio_file in sorted(audio_files):
        print(json.dumps({"status": f"Transcribing: {audio_file.name}"}), file=sys.stderr)

        if GROQ_API_KEY:
            transcription = transcribe_groq(str(audio_file))
        else:
            transcription = transcribe_local(str(audio_file))

        results.append({
            "file": audio_file.name,
            "file_path": str(audio_file.absolute()),
            "file_size_mb": round(audio_file.stat().st_size / (1024 * 1024), 2),
            "transcription": transcription
        })

    output = {
        "directory": str(dir_path.absolute()),
        "total_files": len(audio_files),
        "backend": "groq" if GROQ_API_KEY else "local_whisper",
        "results": results
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice Note Transcription Tool (CCF v2.5)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Single file transcription
    transcribe_parser = subparsers.add_parser("transcribe", help="Transcribe a single audio file")
    transcribe_parser.add_argument("file", help="Path to audio file")

    # Batch transcription
    batch_parser = subparsers.add_parser("batch", help="Transcribe all audio files in a directory")
    batch_parser.add_argument("directory", help="Path to directory containing audio files")

    args = parser.parse_args()

    if args.command == "transcribe":
        transcribe_file(args.file)
    elif args.command == "batch":
        batch_transcribe(args.directory)
