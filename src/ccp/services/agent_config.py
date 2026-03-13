"""
CCP Agent Config Manager
Task 5.09 — Version-controlled agent configuration with rollback.

Operators can modify:
- Agent SKILL.md files
- Prompt templates
- Tool configurations
- Model selections

All changes are versioned, logged, and take effect on next pipeline run.
Rollback support via version history.
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class ConfigVersion(BaseModel):
    """A versioned configuration snapshot."""

    version: int
    config_path: str
    snapshot_path: str
    changed_by: str
    changed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    change_description: str = ""
    is_current: bool = True


class AgentConfigManager:
    """Manage and version agent configurations."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._config_dir = Path(f"coaches/{self.coach_acronym}/config/agents")
        self._versions_dir = self._config_dir / "_versions"
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._versions_dir.mkdir(parents=True, exist_ok=True)
        self._registry_file = self._config_dir / "version_registry.json"

    def update_config(
        self,
        agent_name: str,
        config_content: str,
        changed_by: str = "operator",
        description: str = "",
    ) -> ConfigVersion:
        """Update an agent's configuration with versioning.

        Args:
            agent_name: Name of the agent (e.g., "humor_agent", "script_generator")
            config_content: New configuration content
            changed_by: Who made the change
            description: What was changed and why

        Returns:
            The new ConfigVersion
        """
        config_path = self._config_dir / f"{agent_name}.json"
        registry = self._load_registry()

        # Get next version
        agent_versions = registry.get(agent_name, [])
        next_version = len(agent_versions) + 1

        # Snapshot current config if it exists
        snapshot_name = f"{agent_name}_v{next_version}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        snapshot_path = self._versions_dir / f"{snapshot_name}.json"

        if config_path.exists():
            shutil.copy2(config_path, snapshot_path)

        # Write new config
        config_path.write_text(config_content, encoding="utf-8")

        # Create version record
        version = ConfigVersion(
            version=next_version,
            config_path=str(config_path),
            snapshot_path=str(snapshot_path),
            changed_by=changed_by,
            change_description=description,
        )

        # Mark previous versions as not current
        for v in agent_versions:
            v["is_current"] = False

        agent_versions.append(version.model_dump(mode="json"))
        registry[agent_name] = agent_versions
        self._save_registry(registry)

        # Log
        self.receipt_chain.log(
            agent_id="config_manager",
            action="update_config",
            input_summary=f"Agent: {agent_name}, by: {changed_by}",
            output_summary=f"Version {next_version}: {description}",
            decision="updated",
            metadata={"agent": agent_name, "version": next_version},
        )

        return version

    def rollback(self, agent_name: str, target_version: int) -> ConfigVersion:
        """Rollback an agent's config to a previous version.

        Args:
            agent_name: Agent to rollback
            target_version: Version number to restore

        Returns:
            The restored ConfigVersion
        """
        registry = self._load_registry()
        agent_versions = registry.get(agent_name, [])

        target = None
        for v in agent_versions:
            if v["version"] == target_version:
                target = v
                break

        if not target:
            raise ValueError(
                f"Version {target_version} not found for agent {agent_name}"
            )

        snapshot_path = Path(target["snapshot_path"])
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")

        # Restore from snapshot
        config_path = self._config_dir / f"{agent_name}.json"
        restored_content = snapshot_path.read_text(encoding="utf-8")

        # Create a new version (rollback is itself a versioned change)
        return self.update_config(
            agent_name=agent_name,
            config_content=restored_content,
            changed_by="operator_rollback",
            description=f"Rolled back to version {target_version}",
        )

    def get_history(self, agent_name: str) -> list[dict]:
        """Get version history for an agent."""
        registry = self._load_registry()
        return registry.get(agent_name, [])

    def get_current_config(self, agent_name: str) -> Optional[str]:
        """Get the current config for an agent."""
        config_path = self._config_dir / f"{agent_name}.json"
        if config_path.exists():
            return config_path.read_text(encoding="utf-8")
        return None

    def list_agents(self) -> list[str]:
        """List all configured agents."""
        registry = self._load_registry()
        return list(registry.keys())

    def _load_registry(self) -> dict:
        if self._registry_file.exists():
            return json.loads(self._registry_file.read_text(encoding="utf-8"))
        return {}

    def _save_registry(self, registry: dict) -> None:
        self._registry_file.write_text(
            json.dumps(registry, indent=2, default=str), encoding="utf-8"
        )
