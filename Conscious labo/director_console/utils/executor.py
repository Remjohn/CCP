# Executor utility for CMF Director's Console
# Writes commands to file for Claude Code Agent to process

import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

# File where commands are written for agent to read
COMMANDS_FILE = Path(__file__).parent.parent / "agent_commands.json"
COMMENTS_FILE = Path(__file__).parent.parent / "agent_comments.txt"


def queue_command(
    project_id: int,
    project_code: str,
    command_type: str,
    args: dict = None
) -> dict:
    """
    Queue a command for the agent to execute.
    
    Args:
        project_id: Database ID of the project
        project_code: Full project code (e.g., "009-220-12-Adele")
        command_type: Type of command (run_scripts, run_assets, etc.)
        args: Optional additional arguments
    
    Returns:
        The command dict that was queued
    """
    command = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "project_id": project_id,
        "project_code": project_code,
        "command_type": command_type,
        "args": args or {},
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # Load existing commands
    commands = load_commands()
    
    # Add new command
    commands.append(command)
    
    # Save
    save_commands(commands)
    
    return command


def load_commands() -> list:
    """Load pending commands from file."""
    if not COMMANDS_FILE.exists():
        return []
    
    try:
        with open(COMMANDS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_commands(commands: list):
    """Save commands to file."""
    with open(COMMANDS_FILE, "w") as f:
        json.dump(commands, f, indent=2)


def get_pending_commands() -> list:
    """Get all pending commands."""
    commands = load_commands()
    return [c for c in commands if c.get("status") == "pending"]


def mark_command_complete(command_id: str, success: bool = True, error: str = None):
    """Mark a command as completed or failed."""
    commands = load_commands()
    
    for cmd in commands:
        if cmd.get("id") == command_id:
            cmd["status"] = "completed" if success else "failed"
            cmd["executed_at"] = datetime.now().isoformat()
            if error:
                cmd["error"] = error
            break
    
    save_commands(commands)


def write_comment_for_agent(
    project_code: str,
    stage: str,
    comment: str,
    is_rerun: bool = False
):
    """
    Write a comment to file for Claude Code Agent to read.
    
    Args:
        project_code: Project identifier
        stage: Which stage this relates to
        comment: The actual comment/instruction
        is_rerun: Whether this is a re-run instruction
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "project_code": project_code,
        "stage": stage,
        "comment": comment,
        "is_rerun": is_rerun
    }
    
    # Append to comments file
    with open(COMMENTS_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Project: {project_code}\n")
        f.write(f"Stage: {stage}\n")
        f.write(f"Time: {entry['timestamp']}\n")
        if is_rerun:
            f.write(">>> RE-RUN INSTRUCTION <<<\n")
        f.write(f"\n{comment}\n")


def clear_comments():
    """Clear the comments file."""
    if COMMENTS_FILE.exists():
        COMMENTS_FILE.unlink()


# Command types
COMMAND_TYPES = {
    "run_scripts": "Execute Phase 1: Script generation",
    "run_assets": "Execute Phase 2-4: Assets generation",
    "run_composition": "Execute Phase 5: VFX composition",
    "run_audio": "Execute Phase 6: Audio assembly",
    "run_export": "Execute Phase 7-8: Final export",
    "run_full": "Execute full pipeline",
    "rerun_stage": "Re-run a specific stage with modifications",
}
