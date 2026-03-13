"""
CCP Client Onboarding Flow
Task 3.09 — Handles new client registration via Telegram /start command.

Onboarding steps:
  1. Welcome message in coach's voice
  2. Assign Person ID (CCC-NNNN)
  3. Create Neo4j User node
  4. Initialize ritual configuration
  5. Initial journaling prompt
  6. Update Notion Client Intelligence DB
"""

import json
import os
from pathlib import Path
from typing import Optional

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_registry import CoachRegistry


class ClientOnboarding:
    """Handle new client registration and initial setup."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def onboard(self, telegram_user) -> str:
        """Register a new client and return the welcome message.

        Args:
            telegram_user: TelegramUser object with id, first_name, username

        Returns:
            Welcome message text
        """
        # Step 1: Generate Person ID
        person_id = self._assign_person_id(telegram_user)

        # Step 2: Create Neo4j user node
        try:
            from src.ccp.scripts.setup_neo4j import ContextPremiseGraph
            graph = ContextPremiseGraph(coach_acronym=self.coach_acronym)
            graph.create_user(
                person_id=person_id,
                name=f"{telegram_user.first_name} {telegram_user.last_name}".strip(),
                telegram_id=str(telegram_user.id),
            )
            graph.close()
        except Exception:
            pass  # Neo4j unavailable — continue without graph

        # Step 3: Initialize ritual config
        from src.ccp.services.ritual_scheduler import RitualConfig, RitualScheduler
        scheduler = RitualScheduler(coach_acronym=self.coach_acronym)
        config = RitualConfig(
            person_id=person_id,
            telegram_id=str(telegram_user.id),
        )
        scheduler.save_config(config)

        # Step 4: Initialize dormancy tracking
        from src.ccp.services.dormancy_engine import DormancyEngine
        dormancy = DormancyEngine(coach_acronym=self.coach_acronym)
        dormancy.record_activity(person_id, str(telegram_user.id))

        # Step 5: Generate welcome message
        welcome = await self._generate_welcome(telegram_user.first_name, person_id)

        # Log
        self.receipt_chain.log(
            agent_id="client_onboarding",
            action="register_client",
            person_id=person_id,
            input_summary=f"New client: {telegram_user.first_name} (@{telegram_user.username})",
            output_summary=f"Registered as {person_id}",
            decision="completed",
            metadata={
                "telegram_id": telegram_user.id,
                "username": telegram_user.username,
            },
        )

        return welcome

    def _assign_person_id(self, telegram_user) -> str:
        """Assign a Person ID to a new client."""
        registry_path = Path(
            f"coaches/{self.coach_acronym}/config/coach_registry.json"
        )
        if registry_path.exists():
            data = json.loads(registry_path.read_text(encoding="utf-8"))
            registry = CoachRegistry.model_validate(data)
        else:
            registry = CoachRegistry(
                coach_name="Coach",
                coach_acronym=self.coach_acronym,
                coach_id=f"{self.coach_acronym}-0000",
            )

        person_id = registry.next_person_id()

        # Save updated registry
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(
            registry.model_dump_json(indent=2), encoding="utf-8"
        )

        return person_id.full_id

    async def _generate_welcome(self, first_name: str, person_id: str) -> str:
        """Generate a personalized welcome message in the coach's voice."""
        from google import genai

        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        coach_name = "Coach"
        philosophy = ""
        warmth = 0.7

        if soul_path.exists():
            soul_data = json.loads(soul_path.read_text(encoding="utf-8"))
            coach_name = soul_data.get("coach_name", "Coach")
            philosophy = soul_data.get("coaching_philosophy", "")
            warmth = soul_data.get("content_tone", {}).get("warmth", 0.7)

        prompt = f"""You are {coach_name}. A new client named {first_name} just joined your coaching space.

Your philosophy: {philosophy}
Your warmth level: {warmth}

Write a welcome message. Rules:
1. Maximum 4 sentences
2. Use their first name
3. Make them feel seen and safe
4. Set the expectation: you'll check in daily, they can talk anytime
5. End with one simple question to start the relationship
6. Sound warm and human, NOT corporate or AI-like
7. No bullet points, no lists — this is a personal message

Write the welcome:"""

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text.strip()
