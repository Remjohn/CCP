"""
SKILL.md Loader — Story 21.1
==============================
Runtime loader for SKILL.md protocol files.

Reads SKILL.md from the intelligence_library/protocols/ directory,
extracts YAML frontmatter for metadata, and converts the markdown body
to a system prompt string for Pydantic AI agents.

Architecture:
    intelligence_library/protocols/aria_SKILL.md
                     ↓
    skill_loader.load_skill("aria") → SkillSpec
                     ↓
    SkillSpec.system_prompt → Pydantic AI Agent(system_prompt=...)
"""

import logging
import os
import re
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, field

import yaml

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Default protocols directory
PROTOCOLS_DIR = Path(__file__).parent.parent / "intelligence_library" / "protocols"


@dataclass
class SkillSpec:
    """Parsed SKILL.md file ready for injection into a Pydantic AI agent."""

    name: str
    description: str
    version: str
    agent_role: str
    input_type: str
    output_type: str
    system_prompt: str  # Full markdown body (after frontmatter)
    raw_content: str  # Original file content
    file_path: str  # Source file path

    # Extra metadata fields from frontmatter
    metadata: Dict[str, Any] = field(default_factory=dict)

    def inject_variables(self, **kwargs) -> str:
        """
        Replace dynamic variables in the system prompt.

        Example variables:
            {user_identity} → "Challenger"
            {user_ttt} → "TTT-07"
            {context_premise} → "Fear: Financial Instability, Dream: Legacy"
        """
        prompt = self.system_prompt
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        return prompt


# ──────────────────────────────────────────────
# YAML Frontmatter Parser
# ──────────────────────────────────────────────

FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n",
    re.DOTALL,
)


def _parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """
    Extract YAML frontmatter and markdown body from a SKILL.md file.

    Returns (metadata_dict, markdown_body).
    """
    match = FRONTMATTER_RE.match(content)
    if match:
        frontmatter_str = match.group(1)
        body = content[match.end():]
        try:
            metadata = yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError as e:
            logger.warning(f"[SkillLoader] Failed to parse YAML frontmatter: {e}")
            metadata = {}
        return metadata, body
    else:
        # No frontmatter — treat entire content as body
        return {}, content


# ──────────────────────────────────────────────
# Skill Loader
# ──────────────────────────────────────────────

class SkillLoader:
    """
    Loads and caches SKILL.md files from the protocols directory.

    Usage:
        loader = SkillLoader()
        aria_spec = loader.load_skill("aria")
        prompt = aria_spec.inject_variables(user_identity="Challenger")
    """

    def __init__(self, protocols_dir: Optional[Path] = None):
        self.protocols_dir = protocols_dir or PROTOCOLS_DIR
        self._cache: Dict[str, SkillSpec] = {}

    def load_skill(self, agent_name: str) -> Optional[SkillSpec]:
        """
        Load a SKILL.md file for the given agent name.

        Looks for: {protocols_dir}/{agent_name}_SKILL.md

        Returns SkillSpec or None if file not found.
        Results are cached — reload_skill() to refresh.
        """
        # Return cached version
        if agent_name in self._cache:
            return self._cache[agent_name]

        skill_path = self.protocols_dir / f"{agent_name}_SKILL.md"
        if not skill_path.exists():
            logger.warning(
                f"[SkillLoader] SKILL.md not found for agent '{agent_name}': {skill_path}"
            )
            return None

        try:
            content = skill_path.read_text(encoding="utf-8")
            metadata, body = _parse_frontmatter(content)

            spec = SkillSpec(
                name=metadata.get("name", agent_name),
                description=metadata.get("description", ""),
                version=metadata.get("version", "1.0"),
                agent_role=metadata.get("agent_role", ""),
                input_type=metadata.get("input_type", ""),
                output_type=metadata.get("output_type", ""),
                system_prompt=body.strip(),
                raw_content=content,
                file_path=str(skill_path),
                metadata=metadata,
            )

            self._cache[agent_name] = spec
            logger.info(
                f"[SkillLoader] Loaded SKILL.md: {agent_name} "
                f"v{spec.version} ({len(body)} chars)"
            )
            return spec

        except Exception as e:
            logger.error(f"[SkillLoader] Failed to load {skill_path}: {e}")
            return None

    def reload_skill(self, agent_name: str) -> Optional[SkillSpec]:
        """Force reload a skill (clear cache and re-read file)."""
        self._cache.pop(agent_name, None)
        return self.load_skill(agent_name)

    def reload_all(self):
        """Clear entire cache. Skills will be re-loaded on next access."""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"[SkillLoader] Cleared cache ({count} skills)")

    def list_available_skills(self) -> list[str]:
        """List all available SKILL.md files in the protocols directory."""
        skills = []
        for path in self.protocols_dir.glob("*_SKILL.md"):
            name = path.stem.replace("_SKILL", "")
            skills.append(name)
        return sorted(skills)

    def get_cached_count(self) -> int:
        """Number of skills currently cached."""
        return len(self._cache)


# ──────────────────────────────────────────────
# Global Instance
# ──────────────────────────────────────────────

skill_loader = SkillLoader()
