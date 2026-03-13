# Auto-import utility for discovering and importing existing projects
# Scans input folders and imports projects into database

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import re

def detect_stage(folder: Path) -> str:
    """
    Detect the current stage of a project based on existing files.
    Conservative approach: prioritize scripts stage for review workflow.
    """
    files = list(folder.glob("*"))
    file_names = [f.name.lower() for f in files]
    
    # Check for final_script.json - this is the key indicator
    has_script = any("final_script" in n for n in file_names)
    has_transcript = any("transcript" in n for n in file_names)
    
    # Check for completion markers (has final video in name)
    has_final_video = any("final" in n and n.endswith(".mp4") for n in file_names)
    has_draft = any("draft" in n and n.endswith(".mp4") for n in file_names)
    
    if has_final_video:
        return "completed"
    
    # Check for audio stage (has actual audio files for the project)
    has_song = any("song" in n and (n.endswith(".mp3") or n.endswith(".wav")) for n in file_names)
    if has_draft and has_song:
        return "audio"
    
    # For most cases with a script, start at SCRIPTS stage for review
    # This ensures scripts go through approval workflow
    if has_script:
        return "scripts"
    
    # Has transcript but no script - pending
    if has_transcript:
        return "pending"
    
    return "pending"


def parse_project_folder_name(folder_name: str) -> Dict:
    """
    Parse project folder name to extract project code and name.
    Expected formats:
    - "01_50-12 Matthis" → video_number=1, total=50, month=12, name=Matthis
    - "02_50-12 Audrey" → video_number=2, total=50, month=12, name=Audrey
    """
    # Pattern: XX_YY-ZZ Name where XX=video#, YY=total, ZZ=month
    pattern = r"(\d+)_(\d+)-(\d+)\s+(.+)"
    match = re.match(pattern, folder_name)
    
    if match:
        return {
            "video_number": int(match.group(1)),
            "total_videos": int(match.group(2)),
            "month": int(match.group(3)),
            "name": match.group(4).strip()
        }
    
    # Fallback: just use folder name
    return {
        "video_number": 1,
        "total_videos": 1,
        "month": 12,
        "name": folder_name
    }


def scan_coach_folders(inputs_dir: Path) -> List[Dict]:
    """
    Scan inputs directory for coach folders and projects.
    Returns list of discovered projects with metadata.
    """
    discovered = []
    
    if not inputs_dir.exists():
        return discovered
    
    # Find coach folders (folders that start with "Coach " or contain coach indicator)
    for coach_folder in inputs_dir.iterdir():
        if not coach_folder.is_dir():
            continue
        
        coach_name = coach_folder.name
        
        # Skip if it's not a coach folder (could add more sophisticated detection)
        if coach_name.startswith(".") or coach_name.startswith("_"):
            continue
        
        # Scan for project subfolders
        for project_folder in coach_folder.iterdir():
            if not project_folder.is_dir():
                continue
            
            # Skip special folders
            if project_folder.name.startswith(".") or project_folder.name == "assets":
                continue
            
            # Parse project info
            project_info = parse_project_folder_name(project_folder.name)
            
            # Detect stage
            stage = detect_stage(project_folder)
            
            # Check for key files
            files = {f.name: str(f) for f in project_folder.glob("*")}
            
            has_transcript = any("transcript" in k.lower() for k in files.keys())
            has_script = any("final_script" in k.lower() for k in files.keys())
            has_premise = any("premise" in k.lower() for k in files.keys())
            has_storyboard = any("storyboard" in k.lower() for k in files.keys())
            
            # Build full code
            full_code = f"{project_info['video_number']:02d}_{project_info['total_videos']}-{project_info['month']:02d}"
            
            discovered.append({
                "folder_path": str(project_folder),
                "folder_name": project_folder.name,
                "coach_name": coach_name,
                "project_name": project_info["name"],
                "video_number": project_info["video_number"],
                "total_videos": project_info["total_videos"],
                "month": project_info["month"],
                "full_code": full_code,
                "detected_stage": stage,
                "has_transcript": has_transcript,
                "has_script": has_script,
                "has_premise": has_premise,
                "has_storyboard": has_storyboard,
            })
    
    return discovered


def import_project_to_db(session, project_data: Dict, coach_id: int) -> bool:
    """
    Import a discovered project into the database.
    Returns True if successful, False if already exists.
    """
    from db.models import Project, StageApproval
    
    # Check if already exists
    existing = session.query(Project).filter(
        Project.folder_path == project_data["folder_path"]
    ).first()
    
    if existing:
        return False
    
    # Create project
    project = Project(
        project_id=project_data["full_code"],
        name=project_data["project_name"],
        video_number=project_data["video_number"],
        month=project_data["month"],
        total_videos=project_data["total_videos"],
        full_code=project_data["full_code"],
        coach_id=coach_id,
        folder_path=project_data["folder_path"],
        current_stage=project_data["detected_stage"]
    )
    session.add(project)
    session.flush()
    
    # Create stage approvals
    for stage in ["scripts", "assets", "composition", "audio"]:
        # Mark earlier stages as approved if we're past them
        stage_order = {"pending": 0, "scripts": 1, "assets": 2, "composition": 3, "audio": 4, "completed": 5}
        current_order = stage_order.get(project_data["detected_stage"], 0)
        stage_idx = stage_order.get(stage, 0)
        
        status = "approved" if stage_idx < current_order else "pending"
        
        approval = StageApproval(
            project_id=project.id,
            stage=stage,
            status=status
        )
        session.add(approval)
    
    return True
