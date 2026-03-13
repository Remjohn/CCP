# File System Sync Utility
# Automatically syncs file system changes with database

import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

def sync_projects_with_filesystem(session, inputs_dir: Path) -> dict:
    """
    Sync database with filesystem.
    - Updates existing projects if files changed
    - Returns sync stats
    """
    from db.models import Project, Coach
    
    stats = {"updated": 0, "added": 0, "errors": []}
    
    # Get all projects from database
    projects = session.query(Project).all()
    
    for project in projects:
        folder = Path(project.folder_path)
        
        if not folder.exists():
            continue
        
        # Check for script files
        script_files = list(folder.glob("*final_script*.json"))
        has_script = len(script_files) > 0
        
        # Check for storyboard
        storyboard_files = list(folder.glob("*STORYBOARD*.md")) + list(folder.glob("*storyboard*.md"))
        has_storyboard = len(storyboard_files) > 0
        
        # Check for assets
        assets_dir = folder / "04_assets"
        has_assets = assets_dir.exists() and any(assets_dir.iterdir()) if assets_dir.exists() else False
        
        # Determine correct stage based on file presence
        if project.current_stage == "pending" and has_script:
            project.current_stage = "scripts"
            stats["updated"] += 1
        elif project.current_stage == "scripts" and has_storyboard:
            # Don't auto-advance - user should approve scripts first
            pass
        elif project.current_stage == "assets" and has_assets:
            # Don't auto-advance
            pass
        
        # Update timestamp
        project.updated_at = datetime.now()
    
    return stats


def auto_import_new_folders(session, inputs_dir: Path) -> dict:
    """
    Auto-import any new project folders not in database.
    Creates coach if needed.
    """
    from db.models import Project, Coach
    from utils.auto_import import scan_coach_folders, import_project_to_db
    
    stats = {"imported": 0, "skipped": 0}
    
    # Get existing project paths
    existing_paths = {p.folder_path for p in session.query(Project).all()}
    
    # Scan for all projects
    discovered = scan_coach_folders(inputs_dir)
    
    for proj_data in discovered:
        if proj_data["folder_path"] in existing_paths:
            stats["skipped"] += 1
            continue
        
        # Get or create coach
        coach = session.query(Coach).filter(Coach.name == proj_data["coach_name"]).first()
        if not coach:
            coach = Coach(
                name=proj_data["coach_name"],
                assets_folder=str(inputs_dir / proj_data["coach_name"])
            )
            session.add(coach)
            session.flush()
        
        # Import project
        success = import_project_to_db(session, proj_data, coach.id)
        if success:
            stats["imported"] += 1
    
    return stats


def full_sync(session, inputs_dir: Path) -> dict:
    """
    Full sync: import new + update existing.
    """
    import_stats = auto_import_new_folders(session, inputs_dir)
    sync_stats = sync_projects_with_filesystem(session, inputs_dir)
    
    return {
        "imported": import_stats["imported"],
        "updated": sync_stats["updated"],
        "skipped": import_stats["skipped"]
    }
