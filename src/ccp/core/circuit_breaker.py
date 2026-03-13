"""
CCP Circuit Breaker
Task 3.08 — Crisis detection and automated response halt.

First-pass keyword detection runs on EVERY incoming message
BEFORE any other processing. On trigger:
1. All automated responses halt for this client
2. Coach is notified via Telegram within 10s
3. Receipt Chain logs the activation
4. Resumes only when coach explicitly resets
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


# Crisis keywords and patterns — configurable per coach
DEFAULT_CRISIS_PATTERNS = [
    # Self-harm indicators
    "want to die", "kill myself", "end it all", "not worth living",
    "better off dead", "no reason to live", "can't go on",
    "hurt myself", "cutting myself", "self harm", "self-harm",
    # Severe distress
    "i can't breathe", "panic attack", "please help me",
    "i'm scared", "i'm terrified", "i don't feel safe",
    "nobody cares", "completely alone", "no one understands",
    # Suicidal ideation markers
    "suicide", "suicidal", "overdose", "jump off",
    "pills", "end my life", "last goodbye",
]


class CircuitBreaker:
    """Crisis detection and automated response halt system."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._state_dir = Path(f"coaches/{self.coach_acronym}/clients")
        self._state_dir.mkdir(parents=True, exist_ok=True)
        self._patterns = self._load_patterns()

    def _load_patterns(self) -> list[str]:
        """Load crisis patterns (custom per coach or defaults)."""
        custom_path = Path(
            f"coaches/{self.coach_acronym}/config/crisis_patterns.json"
        )
        if custom_path.exists():
            return json.loads(custom_path.read_text(encoding="utf-8"))
        return DEFAULT_CRISIS_PATTERNS

    def scan_for_crisis(self, text: str) -> bool:
        """First-pass crisis keyword scan. Runs before ANY other processing.

        Args:
            text: The raw message text

        Returns:
            True if crisis signals detected
        """
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in self._patterns)

    def is_active(self, client_telegram_id: str) -> bool:
        """Check if the Circuit Breaker is active for a client."""
        state_file = self._state_dir / f"cb_{client_telegram_id}.json"
        if not state_file.exists():
            return False
        state = json.loads(state_file.read_text(encoding="utf-8"))
        return state.get("active", False)

    async def activate(
        self,
        client_telegram_id: str,
        trigger_message: str,
    ) -> None:
        """Activate the Circuit Breaker for a client.

        1. Halt all automated responses
        2. Notify coach via Telegram
        3. Log to Receipt Chain
        """
        # Save state
        state = {
            "active": True,
            "client_telegram_id": client_telegram_id,
            "trigger_message": trigger_message[:500],
            "activated_at": datetime.now(timezone.utc).isoformat(),
            "activated_by": "auto_detection",
        }
        state_file = self._state_dir / f"cb_{client_telegram_id}.json"
        state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")

        # Log to Receipt Chain
        self.receipt_chain.log(
            agent_id="circuit_breaker",
            action="activate",
            person_id=f"telegram:{client_telegram_id}",
            input_summary=f"Crisis trigger: {trigger_message[:100]}",
            output_summary="Circuit Breaker ACTIVATED — all automation halted",
            decision="crisis_halt",
            metadata={"trigger_patterns_matched": True},
        )

        # Notify coach via Telegram
        await self._notify_coach(client_telegram_id, trigger_message)

    async def _notify_coach(
        self, client_telegram_id: str, trigger_message: str
    ) -> None:
        """Send a crisis alert to the coach via Telegram."""
        import httpx

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        coach_chat_id = os.getenv("COACH_TELEGRAM_CHAT_ID", "")
        if not bot_token or not coach_chat_id:
            return

        alert_text = (
            f"🔴 CIRCUIT BREAKER ACTIVATED\n\n"
            f"Client: {client_telegram_id}\n"
            f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
            f"Trigger message:\n\"{trigger_message[:300]}\"\n\n"
            f"⚠️ All automated responses for this client have been halted.\n"
            f"Please reach out to them directly.\n\n"
            f"To resume automation, use: /reset_cb {client_telegram_id}"
        )

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                url,
                json={"chat_id": coach_chat_id, "text": alert_text},
            )

    def reset(self, client_telegram_id: str, reset_by: str = "coach") -> None:
        """Reset the Circuit Breaker — coach explicitly allows automation to resume."""
        state_file = self._state_dir / f"cb_{client_telegram_id}.json"
        if state_file.exists():
            state = json.loads(state_file.read_text(encoding="utf-8"))
            state["active"] = False
            state["reset_at"] = datetime.now(timezone.utc).isoformat()
            state["reset_by"] = reset_by
            state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")

        self.receipt_chain.log(
            agent_id="circuit_breaker",
            action="reset",
            person_id=f"telegram:{client_telegram_id}",
            input_summary=f"Reset by: {reset_by}",
            output_summary="Circuit Breaker RESET — automation resumed",
            decision="crisis_cleared",
        )
