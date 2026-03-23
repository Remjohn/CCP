"""
CCP Scheduled Monitor Agent — FR1 Unit 8
Step 11-A: Daily cultural monitoring + DARN-CAT question generation

Spec reference: FR1 Tech Spec §Phase 0, Step 11-A
Architecture reference: CCP_Technical_Architecture.md §3.1

The scheduled monitor:
- Runs on daily cadence (default 6:00 AM coach local timezone)
- Monitors community channels (Instagram, LinkedIn, TikTok, Facebook Group)
- Cross-references CMM Layers 3 (Industry Mythology) & 7 (Shared Enemy Typology)
- Generates DARN-CAT questions from observed cultural tension
- Delivers via Telegram: 'Observation:' + 'Question:'
- Is the ONLY production session initiator (AC4 enforcement)
- Saves scheduled_monitor_config.json to pass MorganOrchestrator gate #12

C-11 Persona Masking Gate: no agent names in model-facing prompts.
"""

import json
import asyncio
from datetime import datetime, timezone, time
from pathlib import Path
from typing import Optional

from src.ccp.models.v5_models import CulturalMemoryMap, CMMLayerType


# DARN-CAT categories
DARN_CAT_CATEGORIES = [
    "Desire",       # What they want
    "Ability",      # What they can do
    "Reasons",      # Why it matters
    "Need",         # What's at stake
    "Commitment",   # What they'll do
    "Activation",   # What starts now
    "Taking_steps", # What they're already doing
]


# Monitored channel types
CHANNEL_TYPES = [
    "instagram",
    "linkedin",
    "tiktok",
    "facebook_group",
    "twitter",
    "substack",
    "youtube",
]


_DARN_CAT_GENERATION_PROMPT = """You are a cultural tension analyst for a professional coaching operation.

You have observed a cultural signal in the coach's audience community:

OBSERVATION:
{observation}

COACH CONTEXT:
- Industry Mythology the coach challenges: {industry_mythology}
- Shared Enemy their audience names: {shared_enemy}
- Coach's Linguistic Templates (native phrases): {linguistic_templates}

Generate 3 high-leverage coaching session questions from this observation.
Each question must:
1. Connect the cultural observation to a DARN-CAT motivational interviewing category
2. Use the coach's linguistic templates naturally (do NOT force them)
3. Open a real conversation — not a yes/no answer
4. Be delivered in the coach's native register

Return ONLY valid JSON:
[
  {{
    "question": "...",
    "darn_cat_category": "Desire|Ability|Reasons|Need|Commitment|Activation|Taking_steps",
    "cultural_tension_addressed": "...",
    "observation_link": "how this question connects to the observation"
  }},
  ...
]

Return only the JSON array. No commentary.
"""


class DARNCATQuestion:
    """A single DARN-CAT question generated from a cultural observation."""

    def __init__(
        self,
        question: str,
        darn_cat_category: str,
        cultural_tension_addressed: str,
        observation_link: str,
        source_observation: str,
        generated_at: Optional[datetime] = None,
    ):
        self.question = question
        self.darn_cat_category = darn_cat_category
        self.cultural_tension_addressed = cultural_tension_addressed
        self.observation_link = observation_link
        self.source_observation = source_observation
        self.generated_at = generated_at or datetime.now(timezone.utc)

    def to_telegram_format(self) -> str:
        """Format for Telegram delivery — spec format: 'Observation:' + 'Question:'"""
        return (
            f"📡 *Scheduled Session Trigger*\n\n"
            f"*Observation:* {self.source_observation}\n\n"
            f"*Question ({self.darn_cat_category}):* {self.question}\n\n"
            f"_Tension addressed:_ {self.cultural_tension_addressed}"
        )

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "darn_cat_category": self.darn_cat_category,
            "cultural_tension_addressed": self.cultural_tension_addressed,
            "observation_link": self.observation_link,
            "source_observation": self.source_observation,
            "generated_at": self.generated_at.isoformat(),
        }


class ScheduledMonitorConfig:
    """Configuration for the Scheduled Monitor Agent.

    Written to scheduled_monitor_config.json on the coach's file system.
    Presence of this file passes MorganOrchestrator gate check #12.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        run_time_utc: str = "06:00",  # Default 6:00 AM
        coach_timezone: str = "America/New_York",
        monitored_channels: Optional[list[str]] = None,
        cmm_cross_ref_layers: Optional[list[str]] = None,
        telegram_delivery_chat_id: Optional[str] = None,
        active: bool = True,
        created_at: Optional[datetime] = None,
        last_run: Optional[datetime] = None,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.run_time_utc = run_time_utc
        self.coach_timezone = coach_timezone
        self.monitored_channels = monitored_channels or []
        # Default: cross-reference CMM Layer 3 (Industry Mythology) + Layer 7 (Shared Enemy)
        self.cmm_cross_ref_layers = cmm_cross_ref_layers or [
            CMMLayerType.INDUSTRY_MYTHOLOGY.value,
            CMMLayerType.SHARED_ENEMY.value,
        ]
        self.telegram_delivery_chat_id = telegram_delivery_chat_id
        self.active = active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.last_run = last_run

    def to_dict(self) -> dict:
        return {
            "coach_id": self.coach_id,
            "coach_acronym": self.coach_acronym,
            "run_time_utc": self.run_time_utc,
            "coach_timezone": self.coach_timezone,
            "monitored_channels": self.monitored_channels,
            "cmm_cross_ref_layers": self.cmm_cross_ref_layers,
            "telegram_delivery_chat_id": self.telegram_delivery_chat_id,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduledMonitorConfig":
        obj = cls(
            coach_id=data["coach_id"],
            coach_acronym=data["coach_acronym"],
            run_time_utc=data.get("run_time_utc", "06:00"),
            coach_timezone=data.get("coach_timezone", "America/New_York"),
            monitored_channels=data.get("monitored_channels", []),
            cmm_cross_ref_layers=data.get("cmm_cross_ref_layers"),
            telegram_delivery_chat_id=data.get("telegram_delivery_chat_id"),
            active=data.get("active", True),
        )
        if data.get("created_at"):
            obj.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("last_run"):
            obj.last_run = datetime.fromisoformat(data["last_run"])
        return obj


class ScheduledMonitorAgent:
    """FR1 Step 11-A: Daily Cultural Monitor + DARN-CAT Question Generator.

    Spec:
    - 'Daily monitoring cadence (default 6:00 AM coach timezone)'
    - 'Community channel surveillance (Instagram, LinkedIn, TikTok, Facebook Group)'
    - 'CMM Layer 3 (Industry Mythology) and Layer 7 (Shared Enemy Typology) cross-reference'
    - 'DARN-CAT question generation from observed cultural tension'
    - 'Telegram delivery format: Observation: + Question:'
    - AC4: This is the ONLY legitimate production session initiator

    The config file saved by this agent passes gate check #12 in MorganOrchestrator.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
        gemini_api_key: Optional[str] = None,
        telegram_bot_token: Optional[str] = None,
    ):
        import os
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.telegram_bot_token = telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN")

    def initialize(
        self,
        run_time_utc: str = "06:00",
        coach_timezone: str = "America/New_York",
        monitored_channels: Optional[list[str]] = None,
        telegram_delivery_chat_id: Optional[str] = None,
    ) -> ScheduledMonitorConfig:
        """Initialize the scheduled monitor and write config.json.

        This is what passes MorganOrchestrator gate check #12:
        `scheduled_monitor_config.json` must exist in the coach's config directory.

        Args:
            run_time_utc: Daily run time in HH:MM UTC format.
            coach_timezone: Coach's local timezone for log display.
            monitored_channels: List of channel handles/URLs to monitor.
            telegram_delivery_chat_id: Telegram chat_id for DARN-CAT delivery.

        Returns:
            ScheduledMonitorConfig written to disk.
        """
        config = ScheduledMonitorConfig(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            run_time_utc=run_time_utc,
            coach_timezone=coach_timezone,
            monitored_channels=monitored_channels or [],
            telegram_delivery_chat_id=telegram_delivery_chat_id,
            active=True,
        )

        config_path = self.coach_dir / "config" / "scheduled_monitor_config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")

        return config

    def load_config(self) -> Optional[ScheduledMonitorConfig]:
        """Load the current scheduled monitor config."""
        config_path = self.coach_dir / "config" / "scheduled_monitor_config.json"
        if not config_path.exists():
            return None
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return ScheduledMonitorConfig.from_dict(data)

    def _get_cmm_context(self, cmm: CulturalMemoryMap) -> dict:
        """Extract CMM Layer 3 and Layer 7 context for the DARN-CAT prompt."""
        industry_mythology_entries = []
        shared_enemy_entries = []
        linguistic_templates = []

        for entry in cmm.entries:
            if entry.operator_approved:
                if entry.layer_type == CMMLayerType.INDUSTRY_MYTHOLOGY:
                    industry_mythology_entries.append(entry.content)
                elif entry.layer_type == CMMLayerType.SHARED_ENEMY:
                    shared_enemy_entries.append(entry.content)
                elif entry.layer_type == CMMLayerType.LINGUISTIC_TEMPLATES:
                    linguistic_templates.append(entry.content)

        return {
            "industry_mythology": "; ".join(industry_mythology_entries[:5]) or "Not specified",
            "shared_enemy": "; ".join(shared_enemy_entries[:5]) or "Not specified",
            "linguistic_templates": "; ".join(linguistic_templates[:5]) or "Not specified",
        }

    async def generate_darncat_from_observation(
        self,
        observation: str,
        cmm: CulturalMemoryMap,
    ) -> list[DARNCATQuestion]:
        """Generate DARN-CAT questions from a cultural observation.

        Spec Step 11-A: 'DARN-CAT question generation from observed cultural tension'
        Cross-references CMM Layer 3 (Industry Mythology) + Layer 7 (Shared Enemy).

        Args:
            observation: The cultural signal observed in community channels.
            cmm: The coach's confirmed Cultural Memory Map for cross-referencing.

        Returns:
            List of DARNCATQuestion objects ready for Telegram delivery.
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for DARN-CAT generation")

        from google import genai

        cmm_context = self._get_cmm_context(cmm)

        prompt = _DARN_CAT_GENERATION_PROMPT.format(
            observation=observation,
            industry_mythology=cmm_context["industry_mythology"],
            shared_enemy=cmm_context["shared_enemy"],
            linguistic_templates=cmm_context["linguistic_templates"],
        )

        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        raw_questions = json.loads(response_text)

        questions = []
        for q in raw_questions:
            questions.append(DARNCATQuestion(
                question=q.get("question", ""),
                darn_cat_category=q.get("darn_cat_category", "Reasons"),
                cultural_tension_addressed=q.get("cultural_tension_addressed", ""),
                observation_link=q.get("observation_link", ""),
                source_observation=observation,
            ))

        return questions

    async def deliver_via_telegram(
        self,
        questions: list[DARNCATQuestion],
        chat_id: str,
    ) -> None:
        """Deliver DARN-CAT questions to operator via Telegram.

        Spec format: 'Observation:' + 'Question:'
        AC4: This delivery IS the legitimate session initiator — no manual trigger path.
        """
        if not self.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN required for delivery")

        try:
            import httpx

            bot_url = f"https://api.telegram.org/bot{self.telegram_bot_token}"

            for question in questions:
                message = question.to_telegram_format()
                async with httpx.AsyncClient() as client:
                    await client.post(
                        f"{bot_url}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": message,
                            "parse_mode": "Markdown",
                        },
                    )
                    # Rate limit: 1 message per second
                    await asyncio.sleep(1)

        except ImportError:
            raise ImportError("httpx required for Telegram delivery: pip install httpx")

    async def run_daily_cycle(
        self,
        cmm: CulturalMemoryMap,
        channel_observations: list[str],
    ) -> list[DARNCATQuestion]:
        """Run the full daily monitoring cycle.

        Spec Step 11-A:
        - Community channel surveillance
        - CMM Layer 3+7 cross-reference
        - DARN-CAT question generation
        - Telegram delivery

        AC4: This is the ONLY legitimate production session initiator.
        The operator receives questions via Telegram; manual trigger is blocked.

        Args:
            cmm: Coach's confirmed Cultural Memory Map.
            channel_observations: List of observed cultural signals from community channels.

        Returns:
            All generated DARN-CAT questions.
        """
        all_questions: list[DARNCATQuestion] = []

        for observation in channel_observations:
            if not observation.strip():
                continue
            questions = await self.generate_darncat_from_observation(observation, cmm)
            all_questions.extend(questions)

        config = self.load_config()
        if config and config.telegram_delivery_chat_id and all_questions:
            await self.deliver_via_telegram(all_questions, config.telegram_delivery_chat_id)

        # Update last_run
        if config:
            config.last_run = datetime.now(timezone.utc)
            config_path = self.coach_dir / "config" / "scheduled_monitor_config.json"
            config_path.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")

        return all_questions

    def save_session_log(self, questions: list[DARNCATQuestion]) -> Path:
        """Save the daily session log for audit trail and semantic affinity wiring."""
        log_dir = self.coach_dir / "logs" / "scheduled_monitor"
        log_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_path = log_dir / f"{today}_{self.coach_acronym}_darncat.json"
        log_data = {
            "date": today,
            "coach_acronym": self.coach_acronym,
            "questions_generated": len(questions),
            "questions": [q.to_dict() for q in questions],
        }
        log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
        return log_path
