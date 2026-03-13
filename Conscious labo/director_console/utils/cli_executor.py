# CLI Executor for CMF Pipeline Phases
# Triggers Claude Code / Gemini CLI for AI-assisted phases

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# CLI Tools configuration
CLI_TOOLS = {
    "claude": {
        "command": "claude",
        "available": True  # Will be checked at runtime
    },
    "gemini": {
        "command": "gemini",
        "available": True
    }
}

# Command queue file
COMMAND_QUEUE_FILE = Path(__file__).parent.parent / "agent_commands.json"
COMMAND_LOG_FILE = Path(__file__).parent.parent / "agent_command_log.json"


def check_cli_available(tool: str = "claude") -> bool:
    """Check if CLI tool is available on the system."""
    try:
        result = subprocess.run(
            [CLI_TOOLS[tool]["command"], "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def build_prompt(phase: str, data: Dict[str, Any]) -> str:
    """Build the prompt for AI CLI based on phase and data."""
    
    prompts = {
        "premise_hunter": f"""
Execute Premise Hunter V3 Protocol on the following batch:

{json.dumps(data, indent=2, ensure_ascii=False)}

Follow these steps:
1. For each project, read the transcript
2. Use the provided FRAME to guide extraction
3. Build Context Clusters (HOOK, PROBLEM, MECHANISM, PROOF, CLOSE)
4. Score each cluster for viral potential
5. Generate complete script JSON

Save results to: {data.get('output_path', 'generated_scripts/')}
""",

        "scripts": f"""
Process Scripts stage for batch:

{json.dumps(data, indent=2, ensure_ascii=False)}

Follow CMF Sub-Plan 1 - Script Foundation:
1. Read the approved premise analysis
2. Generate final script JSON with scene assignments
3. Map to Sonic Arc and Scene Builder codes
4. Save to project folder as *_final_script.json
""",

        "assets": f"""
Process Assets stage for batch:

{json.dumps(data, indent=2, ensure_ascii=False)}

Follow CMF Sub-Plan 3 - Assets + Assembly:
1. Read the approved script JSON
2. Generate hero frames using visual engine
3. Create kinetic prompts for Wan 2.2
4. Organize assets in 04_assets/ folder
5. Create asset manifest
""",

        "composition": f"""
Process Composition stage for batch:

{json.dumps(data, indent=2, ensure_ascii=False)}

Follow CMF Visual Engine protocol:
1. Read asset manifest
2. Apply Natron effects per scene codes
3. Render composited video segments
4. Create composition_manifest.json
""",

        "audio": f"""
Process Audio stage for batch:

{json.dumps(data, indent=2, ensure_ascii=False)}

Follow Sonic Story Arc protocol:
1. Apply selected Sonic Arc
2. Generate music stems via Suno
3. Mix 10-track audio
4. Create final audio mix
"""
    }
    
    return prompts.get(phase, f"Execute phase: {phase}\nData: {json.dumps(data)}")


def queue_command(
    phase: str,
    projects: List[Dict],
    cli_tool: str = "claude",
    priority: int = 1
) -> str:
    """
    Queue a command for CLI execution.
    Returns the command ID.
    """
    command_id = f"{phase}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Build command data
    command_data = {
        "command_id": command_id,
        "phase": phase,
        "cli_tool": cli_tool,
        "priority": priority,
        "status": "queued",
        "queued_at": datetime.now().isoformat(),
        "projects": projects,
        "prompt": build_prompt(phase, {
            "projects": projects,
            "output_path": str(Path(__file__).parent.parent / "outputs" / command_id)
        })
    }
    
    # Load existing queue
    queue = []
    if COMMAND_QUEUE_FILE.exists():
        with open(COMMAND_QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    
    # Add new command
    queue.append(command_data)
    
    # Save queue
    with open(COMMAND_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    
    return command_id


def execute_command(command_id: str, cli_tool: str = "claude") -> Dict[str, Any]:
    """
    Execute a queued command via CLI.
    Returns execution result.
    """
    # Load queue
    if not COMMAND_QUEUE_FILE.exists():
        return {"success": False, "error": "No command queue found"}
    
    with open(COMMAND_QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    
    # Find command
    command = next((c for c in queue if c["command_id"] == command_id), None)
    if not command:
        return {"success": False, "error": f"Command {command_id} not found"}
    
    # Build CLI command
    prompt = command["prompt"]
    cli_command = [CLI_TOOLS[cli_tool]["command"], prompt]
    
    # Execute
    try:
        result = subprocess.run(
            cli_command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        execution_result = {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "executed_at": datetime.now().isoformat()
        }
        
        # Update command status
        command["status"] = "completed" if result.returncode == 0 else "failed"
        command["result"] = execution_result
        
        # Save updated queue
        with open(COMMAND_QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        
        # Log execution
        log_execution(command_id, execution_result)
        
        return execution_result
        
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def execute_command_async(command_id: str, cli_tool: str = "claude") -> str:
    """
    Execute command asynchronously (background process).
    Returns the process ID or status message.
    """
    # Load command
    if not COMMAND_QUEUE_FILE.exists():
        return "Error: No command queue found"
    
    with open(COMMAND_QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    
    command = next((c for c in queue if c["command_id"] == command_id), None)
    if not command:
        return f"Error: Command {command_id} not found"
    
    # Create a batch file / shell script for execution
    prompt = command["prompt"]
    script_path = Path(__file__).parent.parent / "temp" / f"{command_id}.txt"
    script_path.parent.mkdir(exist_ok=True)
    
    # Save prompt to file
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    # Update command status
    command["status"] = "ready_for_execution"
    command["prompt_file"] = str(script_path)
    
    with open(COMMAND_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    
    return f"Prompt saved to: {script_path}\nRun: {cli_tool} < {script_path}"


def get_queue_status() -> List[Dict]:
    """Get current command queue status."""
    if not COMMAND_QUEUE_FILE.exists():
        return []
    
    with open(COMMAND_QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_completed() -> int:
    """Remove completed commands from queue. Returns count removed."""
    if not COMMAND_QUEUE_FILE.exists():
        return 0
    
    with open(COMMAND_QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    
    original_count = len(queue)
    queue = [c for c in queue if c["status"] not in ["completed", "failed"]]
    
    with open(COMMAND_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    
    return original_count - len(queue)


def log_execution(command_id: str, result: Dict[str, Any]):
    """Log execution result."""
    log = []
    if COMMAND_LOG_FILE.exists():
        with open(COMMAND_LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
    
    log.append({
        "command_id": command_id,
        "timestamp": datetime.now().isoformat(),
        "result": result
    })
    
    # Keep last 100 entries
    log = log[-100:]
    
    with open(COMMAND_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


# Convenience functions for each phase
def trigger_premise_hunter(projects: List[Dict], cli_tool: str = "claude") -> str:
    """Queue Premise Hunter batch execution."""
    return queue_command("premise_hunter", projects, cli_tool)


def trigger_scripts_stage(projects: List[Dict], cli_tool: str = "claude") -> str:
    """Queue Scripts stage execution."""
    return queue_command("scripts", projects, cli_tool)


def trigger_assets_stage(projects: List[Dict], cli_tool: str = "claude") -> str:
    """Queue Assets stage execution."""
    return queue_command("assets", projects, cli_tool)


def trigger_composition_stage(projects: List[Dict], cli_tool: str = "claude") -> str:
    """Queue Composition stage execution."""
    return queue_command("composition", projects, cli_tool)


def trigger_audio_stage(projects: List[Dict], cli_tool: str = "claude") -> str:
    """Queue Audio stage execution."""
    return queue_command("audio", projects, cli_tool)
