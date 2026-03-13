# Naming utility for CMF Director's Console
# Generates project codes in format: CVN-TVN-MM-CoachName

from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def get_current_month() -> int:
    """Get current month (1-12)."""
    return datetime.now().month


def get_next_video_number(session, month: int, total_videos: int = 220) -> int:
    """
    Get the next available video number for a month.
    Resets to 001 at the start of each month.
    """
    from db.models import Project
    
    # Count existing projects for this month
    count = session.query(Project).filter(
        Project.month == month,
        Project.video_number.isnot(None)
    ).count()
    
    return min(count + 1, total_videos)


def generate_project_code(
    video_number: int,
    total_videos: int,
    month: int,
    coach_name: str
) -> str:
    """
    Generate project code in format: CVN-TVN-MM-CoachName
    
    Args:
        video_number: Current video number (1-220)
        total_videos: Total videos per month (220)
        month: Month number (1-12)
        coach_name: Coach/brand name
    
    Returns:
        Project code like "009-220-12-Adele"
    """
    cvn = f"{video_number:03d}"
    tvn = f"{total_videos:03d}"
    mm = f"{month:02d}"
    
    # Clean coach name (remove special chars, spaces to underscores)
    clean_name = coach_name.strip().replace(" ", "_")
    
    return f"{cvn}-{tvn}-{mm}-{clean_name}"


def parse_project_code(code: str) -> dict:
    """
    Parse a project code back into components.
    
    Args:
        code: Project code like "009-220-12-Adele"
    
    Returns:
        Dict with video_number, total_videos, month, coach_name
    """
    parts = code.split("-", 3)
    if len(parts) != 4:
        raise ValueError(f"Invalid project code format: {code}")
    
    return {
        "video_number": int(parts[0]),
        "total_videos": int(parts[1]),
        "month": int(parts[2]),
        "coach_name": parts[3]
    }


def generate_folder_path(
    inputs_dir: Path,
    coach_name: str,
    project_code: str
) -> Path:
    """
    Generate the folder path for a project.
    
    Expected structure:
    production/
    └── Coach_Adele/
        └── 009-220-12-Adele/
            └── TRANSCRIPT.md
    """
    # Clean coach name for folder
    coach_folder = f"Coach_{coach_name.replace(' ', '_')}"
    
    return inputs_dir / coach_folder / project_code


def create_project_folder(
    inputs_dir: Path,
    coach_name: str,
    project_code: str
) -> Path:
    """Create the project folder structure."""
    folder = generate_folder_path(inputs_dir, coach_name, project_code)
    folder.mkdir(parents=True, exist_ok=True)
    return folder
