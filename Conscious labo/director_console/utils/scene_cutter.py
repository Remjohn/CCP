"""
FFmpeg Scene Cutter for CMF V13
Cuts video clips based on script timecodes
"""
import subprocess
import os
import json
from pathlib import Path


def parse_timecode(tc: str) -> float:
    """Convert MM:SS or HH:MM:SS to seconds."""
    parts = tc.strip().split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return 0.0


def cut_scene(input_video: str, start_tc: str, end_tc: str, output_path: str) -> bool:
    """
    Cut a single scene from video using FFmpeg.
    
    Args:
        input_video: Path to source video
        start_tc: Start timecode (MM:SS or HH:MM:SS)
        end_tc: End timecode (MM:SS or HH:MM:SS)
        output_path: Output file path
    
    Returns:
        bool: True if successful
    """
    start_sec = parse_timecode(start_tc)
    end_sec = parse_timecode(end_tc)
    duration = end_sec - start_sec
    
    if duration <= 0:
        print(f"Invalid duration: {start_tc} to {end_tc}")
        return False
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", input_video,
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "fast",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Cut: {output_path}")
            return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found. Please install FFmpeg.")
        return False


def cut_all_scenes(input_video: str, scenes: list, output_dir: str, project_code: str) -> dict:
    """
    Cut all scenes from a video based on scene list.
    
    Args:
        input_video: Path to source video
        scenes: List of dicts with 'scene_id', 'start', 'end' keys
        output_dir: Output directory for clips
        project_code: Project code for naming
    
    Returns:
        dict: Results with success/failure counts
    """
    results = {"success": 0, "failed": 0, "outputs": []}
    
    a_roll_dir = os.path.join(output_dir, "04_assets", "a_roll")
    os.makedirs(a_roll_dir, exist_ok=True)
    
    for scene in scenes:
        scene_id = scene.get("scene_id", "UNKNOWN")
        start = scene.get("start", "0:00")
        end = scene.get("end", "0:00")
        
        output_path = os.path.join(a_roll_dir, f"{project_code}_{scene_id}.mp4")
        
        if cut_scene(input_video, start, end, output_path):
            results["success"] += 1
            results["outputs"].append(output_path)
        else:
            results["failed"] += 1
    
    return results


def extract_scenes_from_script(script_path: str) -> list:
    """
    Extract scene timecodes from a script JSON file.
    Expected format: {"scenes": [{"id": "SC_01", "start": "0:00", "end": "0:15"}, ...]}
    """
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        scenes = []
        for scene in data.get("scenes", []):
            scenes.append({
                "scene_id": scene.get("id", scene.get("scene_id", "UNKNOWN")),
                "start": scene.get("start", scene.get("start_time", "0:00")),
                "end": scene.get("end", scene.get("end_time", "0:00"))
            })
        return scenes
    except Exception as e:
        print(f"Error reading script: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    print("FFmpeg Scene Cutter - CMF V13")
    print("Usage: Import this module and use cut_all_scenes()")
