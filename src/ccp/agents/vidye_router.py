"""
CCP Vidye Router (CBCS Mode)
Task 3.02 — Routes incoming client messages to the correct handler.

Uses Gemini Flash for fast classification into:
- ritual_response: Daily accountability ritual reply
- journal_entry: Journaling prompt response
- voice_note: Voice note needing transcription + context extraction
- crisis_signal: Requires immediate Circuit Breaker activation
- general: General coaching question or conversation
- greeting: First-time or returning client greeting
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


ROUTE_CLASSIFICATIONS = [
    "ritual_response",
    "journal_entry",
    "voice_note",
    "crisis_signal",
    "general",
    "greeting",
]

CLASSIFICATION_PROMPT = """Classify this client message into exactly ONE category:

MESSAGE: "{message}"
CONTEXT: Last interaction type was "{last_interaction}". Client has been active for {days_active} days.

Categories:
- ritual_response: Replying to a daily accountability check-in
- journal_entry: Responding to a journaling prompt or sharing a reflection
- voice_note: Audio message (always classify audio as voice_note)
- crisis_signal: Shows signs of severe distress, self-harm, or crisis language
- general: General question, conversation, or coaching request
- greeting: Saying hello, checking in, or returning after silence

Return ONLY the category name, nothing else.
"""


class VidyeRouter:
    """Route client messages to the appropriate CBCS handler."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def route(self, message, message_type: str) -> Optional[str]:
        """Route a message to the appropriate handler.

        Args:
            message: TelegramMessage object
            message_type: Pre-classified type (text, voice, command)

        Returns:
            Response text to send back, or None if no response needed
        """
        # Voice notes always go to Aria
        if message_type == "voice":
            return await self._handle_voice(message)

        # Commands are handled separately
        if message_type == "command":
            return await self._handle_command(message)

        # Text messages need classification
        classification = await self._classify(message.text or "")

        # Log the routing decision
        self.receipt_chain.log(
            agent_id="vidye_router",
            action="classify_message",
            person_id=f"{self.coach_acronym}-{message.user.id}",
            input_summary=f"Text: {(message.text or '')[:80]}",
            output_summary=f"Route: {classification}",
            decision=classification,
        )

        # Route to handler
        handlers = {
            "crisis_signal": self._handle_crisis,
            "ritual_response": self._handle_ritual_response,
            "journal_entry": self._handle_journal_response,
            "greeting": self._handle_greeting,
            "general": self._handle_general,
        }

        handler = handlers.get(classification, self._handle_general)
        return await handler(message)

    async def _classify(self, text: str) -> str:
        """Classify message intent using Gemini Flash."""
        # First-pass: check for crisis keywords (no LLM needed)
        from src.ccp.core.circuit_breaker import CircuitBreaker
        cb = CircuitBreaker(coach_acronym=self.coach_acronym)
        if cb.scan_for_crisis(text):
            return "crisis_signal"

        try:
            from google import genai
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            response = await client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents=CLASSIFICATION_PROMPT.format(
                    message=text[:500],
                    last_interaction="unknown",
                    days_active=0,
                ),
            )
            result = response.text.strip().lower()
            if result in ROUTE_CLASSIFICATIONS:
                return result
        except Exception:
            pass
        return "general"

    async def _handle_voice(self, message) -> Optional[str]:
        """Route voice notes to Aria."""
        from src.ccp.agents.aria_processor import AriaProcessor
        aria = AriaProcessor(coach_acronym=self.coach_acronym)
        return await aria.process_voice_note(message)

    async def _handle_crisis(self, message) -> Optional[str]:
        """Activate Circuit Breaker on crisis detection."""
        from src.ccp.core.circuit_breaker import CircuitBreaker
        cb = CircuitBreaker(coach_acronym=self.coach_acronym)
        await cb.activate(
            client_telegram_id=str(message.user.id),
            trigger_message=message.text or "",
        )
        return (
            "I hear you, and what you're feeling matters. "
            "Your coach has been notified and will reach out to you personally very soon. "
            "You're not alone in this."
        )

    async def _handle_ritual_response(self, message) -> Optional[str]:
        """Process a reply to a daily accountability ritual."""
        from src.ccp.services.soul_resonance import SoulResonance
        resonance = SoulResonance(coach_acronym=self.coach_acronym)
        return await resonance.generate_response(
            client_id=str(message.user.id),
            message_text=message.text or "",
            interaction_type="ritual_response",
        )

    async def _handle_journal_response(self, message) -> Optional[str]:
        """Process a journaling prompt response."""
        from src.ccp.services.soul_resonance import SoulResonance
        resonance = SoulResonance(coach_acronym=self.coach_acronym)
        return await resonance.generate_response(
            client_id=str(message.user.id),
            message_text=message.text or "",
            interaction_type="journal_response",
        )

    async def _handle_greeting(self, message) -> Optional[str]:
        """Handle a greeting or check-in."""
        from src.ccp.services.soul_resonance import SoulResonance
        resonance = SoulResonance(coach_acronym=self.coach_acronym)
        return await resonance.generate_response(
            client_id=str(message.user.id),
            message_text=message.text or "",
            interaction_type="greeting",
        )

    async def _handle_general(self, message) -> Optional[str]:
        """Handle a general coaching question."""
        from src.ccp.services.soul_resonance import SoulResonance
        resonance = SoulResonance(coach_acronym=self.coach_acronym)
        return await resonance.generate_response(
            client_id=str(message.user.id),
            message_text=message.text or "",
            interaction_type="general",
        )

    async def _handle_command(self, message) -> Optional[str]:
        """Handle Telegram bot commands."""
        text = message.text or ""
        if text.startswith("/start"):
            # New client onboarding
            from src.ccp.services.client_onboarding import ClientOnboarding
            onboarding = ClientOnboarding(coach_acronym=self.coach_acronym)
            return await onboarding.onboard(message.user)
        return None
