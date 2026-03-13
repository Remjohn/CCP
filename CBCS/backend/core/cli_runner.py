"""
CLI Session Runner — Story 20.1
================================
Spawns Gemini CLI sessions to execute CCF/CMF commands.
CBCS is the coordinator/scheduler. Gemini CLI is the creative executor.

Architecture:
    CBCS (Telegram bot) → cli_runner.spawn_session() → Gemini CLI → Output files
    CBCS (Telegram bot) ← cli_runner.wait_for_output()  ← File system

Design Principles:
    1. CCF/CMF commands run UNCHANGED — 300+ prompt files stay as-is
    2. Each command = one fresh CLI session (no context bleed)
    3. State lives in file system (strategy_brief.json, Quote_Manifest.md, etc.)
    4. The runner monitors output files to determine completion
    5. Timeout + retry logic prevents zombie sessions
"""

import asyncio
import json
import os
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class CLISessionConfig:
    """Configuration for a single CLI session."""
    command: str               # e.g., 'cmf-diagnose', 'ccf-weekly'
    project_id: str            # e.g., '01_50-12 Matthis'
    workspace_root: str        # e.g., 'd:/Work/The Conscious Movie Factory December'
    expected_outputs: List[str]  # Relative paths to expected output files
    timeout_seconds: int = 600   # 10 minutes default
    env_overrides: Dict[str, str] = field(default_factory=dict)


@dataclass
class CLISessionResult:
    """Result of a CLI session execution."""
    success: bool
    command: str
    project_id: str
    duration_seconds: float
    output_files: Dict[str, str]   # filename → contents (for small files) or path
    error: Optional[str] = None
    return_code: Optional[int] = None


# ──────────────────────────────────────────────
# The CLI Session Runner
# ──────────────────────────────────────────────

class CLISessionRunner:
    """
    Spawns and manages Gemini CLI sessions for CCF/CMF pipeline execution.

    Usage:
        runner = CLISessionRunner()

        # Run a single command
        result = await runner.run_session(CLISessionConfig(
            command='cmf-diagnose',
            project_id='01_50-12 Matthis',
            workspace_root='d:/Work/The Conscious Movie Factory December',
            expected_outputs=['production/Coach Adele/01_50-12 Matthis/01_50-12 Matthis_strategy_brief.json']
        ))

        # Run a pipeline (commands in sequence)
        results = await runner.run_pipeline([
            CLISessionConfig(command='cmf-diagnose', ...),
            CLISessionConfig(command='cmf-hunt', ...),
            CLISessionConfig(command='cmf-compose', ...),
        ])
    """

    def __init__(self, gemini_executable: str = "gemini"):
        self.gemini_executable = gemini_executable
        self._active_sessions: Dict[str, subprocess.Popen] = {}

    async def run_session(self, config: CLISessionConfig) -> CLISessionResult:
        """
        Spawn a single Gemini CLI session and wait for completion.

        The session runs in the workspace_root directory and executes a command like:
            gemini -p "Read commands/{command}.md and execute for project \"{project_id}\""

        Args:
            config: Session configuration

        Returns:
            CLISessionResult with success/failure, duration, and output file contents
        """
        session_id = f"{config.command}_{config.project_id}_{datetime.now().strftime('%H%M%S')}"
        start_time = datetime.now()

        logger.info(f"[CLI Runner] Starting session: {session_id}")
        logger.info(f"[CLI Runner] Command: {config.command} for {config.project_id}")

        # Build the prompt that tells Gemini CLI what to do
        prompt = self._build_prompt(config.command, config.project_id)

        # Build environment
        env = os.environ.copy()
        env.update(config.env_overrides)

        try:
            # Spawn the CLI process
            process = await asyncio.create_subprocess_exec(
                self.gemini_executable,
                "-p", prompt,
                cwd=config.workspace_root,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            logger.info(f"[CLI Runner] Session {session_id} spawned (PID: {process.pid})")

            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=config.timeout_seconds
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                duration = (datetime.now() - start_time).total_seconds()
                logger.error(f"[CLI Runner] Session {session_id} timed out after {config.timeout_seconds}s")
                return CLISessionResult(
                    success=False,
                    command=config.command,
                    project_id=config.project_id,
                    duration_seconds=duration,
                    output_files={},
                    error=f"Session timed out after {config.timeout_seconds} seconds",
                    return_code=-1
                )

            duration = (datetime.now() - start_time).total_seconds()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='replace') if stderr else "Unknown error"
                logger.error(f"[CLI Runner] Session {session_id} failed (code {process.returncode}): {error_msg[:500]}")
                return CLISessionResult(
                    success=False,
                    command=config.command,
                    project_id=config.project_id,
                    duration_seconds=duration,
                    output_files={},
                    error=error_msg[:1000],
                    return_code=process.returncode
                )

            # Check for expected output files
            output_files = self._collect_outputs(config)

            missing = [f for f in config.expected_outputs
                       if os.path.basename(f) not in output_files]

            if missing:
                logger.warning(f"[CLI Runner] Session {session_id} completed but missing outputs: {missing}")

            logger.info(f"[CLI Runner] Session {session_id} completed in {duration:.1f}s "
                        f"({len(output_files)} output files)")

            return CLISessionResult(
                success=True,
                command=config.command,
                project_id=config.project_id,
                duration_seconds=duration,
                output_files=output_files,
                return_code=0
            )

        except FileNotFoundError:
            duration = (datetime.now() - start_time).total_seconds()
            error = f"Gemini CLI executable not found: {self.gemini_executable}"
            logger.error(f"[CLI Runner] {error}")
            return CLISessionResult(
                success=False,
                command=config.command,
                project_id=config.project_id,
                duration_seconds=duration,
                output_files={},
                error=error,
                return_code=-1
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[CLI Runner] Session {session_id} error: {e}")
            return CLISessionResult(
                success=False,
                command=config.command,
                project_id=config.project_id,
                duration_seconds=duration,
                output_files={},
                error=str(e),
                return_code=-1
            )

    async def run_pipeline(
        self,
        configs: List[CLISessionConfig],
        stop_on_failure: bool = True
    ) -> List[CLISessionResult]:
        """
        Run multiple CLI sessions in sequence (pipeline execution).

        Each session runs in a fresh context. State passes through the file system:
            cmf-diagnose → strategy_brief.json → cmf-hunt → Quote_Manifest.md → cmf-compose → ...

        Args:
            configs: List of session configurations to run in order
            stop_on_failure: If True, stop the pipeline when a session fails

        Returns:
            List of CLISessionResults
        """
        results = []
        logger.info(f"[CLI Runner] Starting pipeline with {len(configs)} sessions")

        for i, config in enumerate(configs, 1):
            logger.info(f"[CLI Runner] Pipeline step {i}/{len(configs)}: {config.command}")

            result = await self.run_session(config)
            results.append(result)

            if not result.success and stop_on_failure:
                logger.error(f"[CLI Runner] Pipeline stopped at step {i} due to failure")
                break

            # Brief pause between sessions to avoid resource contention
            if i < len(configs):
                await asyncio.sleep(2)

        total_duration = sum(r.duration_seconds for r in results)
        successes = sum(1 for r in results if r.success)
        logger.info(f"[CLI Runner] Pipeline completed: {successes}/{len(results)} successful, "
                     f"total duration: {total_duration:.1f}s")

        return results

    def _build_prompt(self, command: str, project_id: str) -> str:
        """
        Build the prompt string for Gemini CLI.

        Maps command names to their file paths and constructs the execution prompt.
        """
        # Command routing table — maps short names to command file paths
        command_map = {
            # CCF Commands
            "ccf-weekly": "ccf-26/commands/ccf-weekly.md",
            "ccf-tierlist": "commands/ccf-tierlist.md",
            "ccf-deep-research": "ccf-26/commands/ccf-deep-research.md",

            # CMF Phase 1A Commands
            "cmf-diagnose": "commands/cmf-diagnose.md",
            "cmf-hunt": "commands/cmf-hunt.md",
            "cmf-analyze": "commands/cmf-analyze.md",
            "cmf-compose": "commands/cmf-compose.md",
            "cmf-authorize": "commands/cmf-authorize.md",

            # CMF Phase 1B Commands
            "cmf-storyboard": "commands/cmf-storyboard.md",
            "cmf-sonic": "commands/cmf-sonic.md",
            "cmf-motion": "commands/cmf-motion.md",

            # CMF Narrative Commands
            "cmf-narrative": "commands/cmf-narrative.md",
            "cmf-script": "commands/cmf-script.md",
        }

        command_path = command_map.get(command)
        if not command_path:
            # Fallback: try direct path
            command_path = f"commands/{command}.md"

        prompt = f'Read {command_path} and execute for project "{project_id}"'

        return prompt

    def _collect_outputs(self, config: CLISessionConfig) -> Dict[str, str]:
        """
        Collect output files generated by the CLI session.

        For each expected output, check if it exists and read its contents
        (for JSON/small files) or return its path (for large files).
        """
        output_files = {}

        for expected in config.expected_outputs:
            full_path = os.path.join(config.workspace_root, expected)

            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                basename = os.path.basename(full_path)

                if file_size < 50_000 and full_path.endswith(('.json', '.md', '.txt', '.yaml')):
                    # Read small text files
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            output_files[basename] = f.read()
                    except Exception as e:
                        output_files[basename] = f"[READ ERROR: {e}]"
                else:
                    # Large files: return path only
                    output_files[basename] = full_path

        return output_files


# ──────────────────────────────────────────────
# Pipeline Presets
# ──────────────────────────────────────────────

def build_cmf_phase1a_pipeline(
    project_id: str,
    coach_name: str = "Coach Adele",
    workspace_root: str = "d:/Work/The Conscious Movie Factory December"
) -> List[CLISessionConfig]:
    """
    Build the CMF Phase 1A pipeline configuration.

    This produces 4 sequential sessions:
        1. cmf-diagnose → strategy_brief.json
        2. cmf-hunt → Quote_Manifest.md
        3. cmf-analyze → Quote_Manifest_Enriched.md
        4. cmf-compose → premise_analysis.json
    """
    project_dir = f"production/{coach_name}/{project_id}"

    return [
        CLISessionConfig(
            command="cmf-diagnose",
            project_id=project_id,
            workspace_root=workspace_root,
            expected_outputs=[f"{project_dir}/{project_id}_strategy_brief.json"],
            timeout_seconds=300,
        ),
        CLISessionConfig(
            command="cmf-hunt",
            project_id=project_id,
            workspace_root=workspace_root,
            expected_outputs=[f"{project_dir}/{project_id}_Quote_Manifest.md"],
            timeout_seconds=600,
        ),
        CLISessionConfig(
            command="cmf-analyze",
            project_id=project_id,
            workspace_root=workspace_root,
            expected_outputs=[f"{project_dir}/{project_id}_Quote_Manifest_Enriched.md"],
            timeout_seconds=600,
        ),
        CLISessionConfig(
            command="cmf-compose",
            project_id=project_id,
            workspace_root=workspace_root,
            expected_outputs=[f"{project_dir}/{project_id}_premise_analysis.json"],
            timeout_seconds=600,
        ),
    ]


def build_ccf_weekly_pipeline(
    project_id: str,
    workspace_root: str = "d:/Work/The Conscious Movie Factory December"
) -> List[CLISessionConfig]:
    """
    Build the CCF Weekly pipeline configuration.

    Single session that runs the full weekly pipeline:
        ccf-weekly → dynamic_content_themes.json + content outputs
    """
    return [
        CLISessionConfig(
            command="ccf-weekly",
            project_id=project_id,
            workspace_root=workspace_root,
            expected_outputs=[
                f"ccf-26/Production/{project_id}/dynamic_content_themes.json",
            ],
            timeout_seconds=900,  # 15 min — weekly pipeline is long
        ),
    ]


# ──────────────────────────────────────────────
# Global Instance
# ──────────────────────────────────────────────

cli_runner = CLISessionRunner()
