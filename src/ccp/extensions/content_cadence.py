"""
CCP ContentCadence Extension
Task 2.14 — Enforces monthly content generation limits per coach.

Tracks production count and auto-pauses ccf-weekly when the
configured limit is reached.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class CadenceConfig(BaseModel):
    """Monthly cadence limits for a coach."""

    monthly_limit: int = Field(default=144, description="Max pieces per month (4 batches × 36)")
    current_month: str = Field(default="")
    current_count: int = Field(default=0)
    paused: bool = Field(default=False)


class ContentCadence:
    """Track and enforce monthly content production limits."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.config_path = Path(
            f"coaches/{self.coach_acronym}/config/cadence.json"
        )
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> CadenceConfig:
        if self.config_path.exists():
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
            return CadenceConfig.model_validate(data)
        return CadenceConfig()

    def _save(self, config: CadenceConfig) -> None:
        self.config_path.write_text(config.model_dump_json(indent=2), encoding="utf-8")

    def can_produce(self, batch_size: int = 36) -> tuple[bool, str]:
        """Check if a batch can be produced within the monthly limit.

        Returns:
            (can_proceed, message) tuple
        """
        config = self._load()
        current_month = datetime.now(timezone.utc).strftime("%Y-%m")

        # Reset counter if new month
        if config.current_month != current_month:
            config.current_month = current_month
            config.current_count = 0
            config.paused = False
            self._save(config)

        if config.paused:
            return False, f"Production paused. {config.current_count}/{config.monthly_limit} used this month."

        remaining = config.monthly_limit - config.current_count
        if remaining < batch_size:
            return False, (
                f"Insufficient quota: {remaining} remaining, {batch_size} needed. "
                f"({config.current_count}/{config.monthly_limit} used this month)"
            )

        return True, f"OK: {remaining} remaining after this batch."

    def record_batch(self, count: int) -> None:
        """Record that a batch was produced."""
        config = self._load()
        current_month = datetime.now(timezone.utc).strftime("%Y-%m")
        if config.current_month != current_month:
            config.current_month = current_month
            config.current_count = 0
        config.current_count += count
        if config.current_count >= config.monthly_limit:
            config.paused = True
        self._save(config)

    def set_limit(self, monthly_limit: int) -> None:
        """Set the monthly production limit."""
        config = self._load()
        config.monthly_limit = monthly_limit
        self._save(config)

    def get_status(self) -> dict:
        """Get current cadence status."""
        config = self._load()
        return {
            "coach": self.coach_acronym,
            "month": config.current_month,
            "produced": config.current_count,
            "limit": config.monthly_limit,
            "remaining": max(0, config.monthly_limit - config.current_count),
            "paused": config.paused,
        }
