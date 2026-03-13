"""
CCP Dormancy Recovery Engine
Task 3.07 — Detects client inactivity and triggers gentle recovery sequences.

Dormancy tiers:
- Yellow (3 days): Gentle nudge via their preferred ritual type
- Orange (7 days): Context-aware check-in referencing their last topic
- Red (14 days): Coach receives alert to personally reach out
"""

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


class DormancyTier:
    YELLOW = "yellow"  # 3 days
    ORANGE = "orange"  # 7 days
    RED = "red"        # 14 days


DORMANCY_PROMPTS = {
    DormancyTier.YELLOW: """You are coaching as {coach_name}. A client hasn't responded in 3 days.

CLIENT CONTEXT: {context}
THEIR LAST MESSAGE: "{last_message}"

Write a gentle nudge. Rules:
1. Maximum 2 sentences
2. Reference something specific from their last interaction
3. Make it feel like you genuinely noticed their absence
4. No guilt, no pressure, just warmth
5. Sound like {coach_name}

Write the nudge:""",

    DormancyTier.ORANGE: """You are coaching as {coach_name}. A client hasn't responded in 7 days.

CLIENT CONTEXT: {context}
THEIR LAST MESSAGE: "{last_message}"
THEY'VE BEEN WORKING ON: {current_focus}

Write a context-aware check-in. Rules:
1. Maximum 3 sentences
2. Name what they were working on
3. Normalize the silence — "life gets busy" energy
4. Include a low-effort question they can answer with one sentence
5. Sound like {coach_name}

Write the check-in:""",

    DormancyTier.RED: """Client {person_id} has been dormant for 14+ days.

CONTEXT: {context}
LAST INTERACTION: {last_date}
THEIR FOCUS WAS: {current_focus}
ENGAGEMENT STREAK BEFORE DORMANCY: {streak}

Compose an alert for the coach to personally reach out.
Include the key context points they should reference.
Maximum 5 lines.""",
}


class DormancyEngine:
    """Detect and recover dormant clients."""

    YELLOW_DAYS = 3
    ORANGE_DAYS = 7
    RED_DAYS = 14

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._clients_dir = Path(f"coaches/{self.coach_acronym}/clients")
        self._clients_dir.mkdir(parents=True, exist_ok=True)

    def check_all_clients(self) -> dict[str, list[str]]:
        """Scan all clients and classify dormancy status.

        Returns:
            Dict mapping dormancy tier to list of person_ids
        """
        result = {
            DormancyTier.YELLOW: [],
            DormancyTier.ORANGE: [],
            DormancyTier.RED: [],
        }
        now = datetime.now(timezone.utc)

        for f in self._clients_dir.glob("activity_*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            last_active_str = data.get("last_active", "")
            if not last_active_str:
                continue

            last_active = datetime.fromisoformat(last_active_str)
            if last_active.tzinfo is None:
                last_active = last_active.replace(tzinfo=timezone.utc)
            days_silent = (now - last_active).days

            person_id = data.get("person_id", "")
            if days_silent >= self.RED_DAYS:
                result[DormancyTier.RED].append(person_id)
            elif days_silent >= self.ORANGE_DAYS:
                result[DormancyTier.ORANGE].append(person_id)
            elif days_silent >= self.YELLOW_DAYS:
                result[DormancyTier.YELLOW].append(person_id)

        return result

    async def recover(
        self,
        person_id: str,
        tier: str,
        context: str = "",
        last_message: str = "",
        current_focus: str = "",
        streak: int = 0,
    ) -> str:
        """Generate a recovery message for a dormant client.

        Returns:
            Recovery message text (or coach alert for RED tier)
        """
        from google import genai

        template = DORMANCY_PROMPTS.get(tier, DORMANCY_PROMPTS[DormancyTier.YELLOW])

        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        coach_name = "Coach"
        if soul_path.exists():
            soul_data = json.loads(soul_path.read_text(encoding="utf-8"))
            coach_name = soul_data.get("coach_name", "Coach")

        prompt = template.format(
            coach_name=coach_name,
            context=context or "Building relationship.",
            last_message=last_message[:200] or "No last message available.",
            current_focus=current_focus or "General growth.",
            person_id=person_id,
            last_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            streak=streak,
        )

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        result = response.text.strip()

        self.receipt_chain.log(
            agent_id="dormancy_engine",
            action=f"recovery_{tier}",
            person_id=person_id,
            output_summary=f"{tier}: {result[:80]}...",
            decision="sent" if tier != DormancyTier.RED else "coach_alerted",
        )

        return result

    def record_activity(self, person_id: str, telegram_id: str) -> None:
        """Record that a client was active (resets dormancy)."""
        data = {
            "person_id": person_id,
            "telegram_id": telegram_id,
            "last_active": datetime.now(timezone.utc).isoformat(),
        }
        activity_file = self._clients_dir / f"activity_{person_id}.json"
        activity_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
