"""
CCP DARN-CAT Re-Elicitation Engine — FR2 Unit 4
Marker-specific prompt generation for failed LIWC-22 Thought Units.

Spec reference: FR2 Tech Spec §Stage D — On Gate Failure (SYNTHETIC_CANDIDATE)
  'The system does NOT tell the coach they failed. It deepens the session
   using a DARN-CAT framework prompt dispatched via Telegram.'

Architecture reference: §10.6 (Audio Pipeline), §5.2 (Corrected Intake Flow)

DARN-CAT = Desire, Ability, Reasons, Need, Commitment, Activation, Taking_steps
(Motivational Interviewing framework)

OARS = Open questions, Affirmations, Reflections, Summaries
(Therapeutic interview framework governing re-elicitation phrasing)
"""

from typing import Optional

from src.ccp.models.sacred_audio_models import (
    AuthenticityMarker,
    AuthenticityScore,
)


# ──────────────────────────────────────────────────────────────
# Marker-Specific Re-Elicitation Prompts
# Spec: §Stage D — "Examples calibrated to the failed marker" table
# ──────────────────────────────────────────────────────────────

# Primary prompts: taken directly from the spec
MARKER_PRIMARY_PROMPTS: dict[AuthenticityMarker, str] = {
    AuthenticityMarker.ABSENCE_OF_HEDGING: (
        "I understood the idea, but I want to get closer to the actual moment. "
        "Tell me specifically: when did you first feel this? What were you doing?"
    ),
    AuthenticityMarker.VERB_TENSE_DISTRIBUTION: (
        "Walk me through it as if you're there right now. "
        "Not what happened — what is actually happening?"
    ),
    AuthenticityMarker.FIRST_PERSON_SINGULAR: (
        "Tell me about a time when this personally affected YOU — "
        "not a client, not the industry. You."
    ),
    AuthenticityMarker.FILLER_FREQUENCY: (
        "That came through clearly — but I want the version you'd say "
        "to a close friend at 11pm. Less polished, more real."
    ),
}

# Secondary prompts: for markers not explicitly in the spec table
# but following the same DARN-CAT / OARS framework principles
MARKER_SECONDARY_PROMPTS: dict[AuthenticityMarker, str] = {
    AuthenticityMarker.EXCLUSIVE_WORDS: (
        "I hear the main idea — but what's the tension? What's the 'but' "
        "in this story? Where does it get complicated?"
    ),
    AuthenticityMarker.SENTENCE_COMPRESSION: (
        "That's a full picture — now give me just the gut punch. "
        "If you had 10 seconds to tell someone the realest part, what would you say?"
    ),
    AuthenticityMarker.DISCOURSE_MARKER_POSITION: (
        "I can feel you thinking about how to say this. "
        "Stop organizing it. Just react — what's the first thing that comes up?"
    ),
}

# Generic fallback for cases where no specific prompt exists
GENERIC_DEEPENING_PROMPT: str = (
    "That's helpful — but I want to go deeper. "
    "What's the part of this you don't usually say out loud?"
)

# Spec: "session is marked INSUFFICIENT and coach is notified to continue
# the conversation over the week"
INSUFFICIENT_SESSION_MESSAGE: str = (
    "This is a great start. Let's continue this conversation over the week — "
    "there's more depth here and I want to make sure we capture it properly."
)


class ReElicitationEngine:
    """Generates marker-specific DARN-CAT re-elicitation prompts.

    Spec: 'The system does NOT tell the coach they failed. It deepens
    the session using a DARN-CAT framework prompt dispatched via Telegram.'

    This engine:
    1. Analyzes which markers failed on a SYNTHETIC_CANDIDATE unit
    2. Selects the most appropriate re-elicitation prompt
    3. Formats it for Telegram delivery
    """

    def generate_prompt(self, score: AuthenticityScore) -> str:
        """Generate a re-elicitation prompt for a SYNTHETIC_CANDIDATE unit.

        Spec: 'Examples calibrated to the failed marker.'
        Priority: select prompt for the most significant failed marker.

        Args:
            score: The AuthenticityScore with failed_markers populated.

        Returns:
            A DARN-CAT formatted re-elicitation prompt string.
        """
        if not score.failed_markers:
            return GENERIC_DEEPENING_PROMPT

        # Priority order for prompt selection:
        # 1. Hedging (most actionable — spec explicitly lists this)
        # 2. Past-tense dominant (spec explicitly lists this)
        # 3. Low FPS (spec explicitly lists this)
        # 4. Zero fillers / scripted (spec explicitly lists this)
        # 5. Other markers (secondary prompts)
        priority_order = [
            AuthenticityMarker.ABSENCE_OF_HEDGING,
            AuthenticityMarker.VERB_TENSE_DISTRIBUTION,
            AuthenticityMarker.FIRST_PERSON_SINGULAR,
            AuthenticityMarker.FILLER_FREQUENCY,
            AuthenticityMarker.EXCLUSIVE_WORDS,
            AuthenticityMarker.SENTENCE_COMPRESSION,
            AuthenticityMarker.DISCOURSE_MARKER_POSITION,
        ]

        for marker in priority_order:
            if marker in score.failed_markers:
                if marker in MARKER_PRIMARY_PROMPTS:
                    return MARKER_PRIMARY_PROMPTS[marker]
                elif marker in MARKER_SECONDARY_PROMPTS:
                    return MARKER_SECONDARY_PROMPTS[marker]

        return GENERIC_DEEPENING_PROMPT

    def generate_combined_prompt(self, score: AuthenticityScore) -> str:
        """Generate a prompt addressing multiple failed markers when possible.

        If 2+ markers fail, combines the primary prompt with a secondary
        element to address the second most significant failure.
        """
        if not score.failed_markers or len(score.failed_markers) == 1:
            return self.generate_prompt(score)

        primary = self.generate_prompt(score)

        # Find a secondary failed marker
        primary_marker = self._get_primary_marker(score.failed_markers)
        secondary_markers = [m for m in score.failed_markers if m != primary_marker]

        if secondary_markers:
            secondary_marker = secondary_markers[0]
            secondary_hint = self._get_secondary_hint(secondary_marker)
            if secondary_hint:
                return f"{primary} {secondary_hint}"

        return primary

    def get_insufficient_session_message(self) -> str:
        """Return the message for sessions with <3 AUTHENTIC units.

        Spec: 'session is marked INSUFFICIENT and coach is notified to
        continue the conversation over the week.'
        """
        return INSUFFICIENT_SESSION_MESSAGE

    def get_duration_rejection_message(self) -> str:
        """Return the message for voice notes <15 seconds.

        Spec §Stage A: 'if < 15 seconds → implicit rejection. System responds:
        "Could you share a bit more? I want to make sure I can really work
        with what you're giving me."'
        """
        return (
            "Could you share a bit more? I want to make sure I can "
            "really work with what you're giving me."
        )

    def get_api_error_message(self) -> str:
        """Return the message for Groq API failures.

        Spec §Stage B: 'halt and alert coach: "I'm having trouble processing
        your audio right now. Please try again in a few minutes."'
        """
        return (
            "I'm having trouble processing your audio right now. "
            "Please try again in a few minutes."
        )

    def _get_primary_marker(
        self, failed_markers: list[AuthenticityMarker]
    ) -> Optional[AuthenticityMarker]:
        """Get the highest-priority failed marker."""
        priority = [
            AuthenticityMarker.ABSENCE_OF_HEDGING,
            AuthenticityMarker.VERB_TENSE_DISTRIBUTION,
            AuthenticityMarker.FIRST_PERSON_SINGULAR,
            AuthenticityMarker.FILLER_FREQUENCY,
        ]
        for marker in priority:
            if marker in failed_markers:
                return marker
        return failed_markers[0] if failed_markers else None

    def _get_secondary_hint(self, marker: AuthenticityMarker) -> Optional[str]:
        """Get a short secondary hint for a failed marker."""
        hints = {
            AuthenticityMarker.ABSENCE_OF_HEDGING: "Be definitive — no 'maybe' needed.",
            AuthenticityMarker.VERB_TENSE_DISTRIBUTION: "Tell it in present tense.",
            AuthenticityMarker.FIRST_PERSON_SINGULAR: "Make it about you.",
            AuthenticityMarker.FILLER_FREQUENCY: "Don't rehearse it — just talk.",
            AuthenticityMarker.EXCLUSIVE_WORDS: "Where's the tension in this?",
            AuthenticityMarker.SENTENCE_COMPRESSION: "Keep it short and punchy.",
            AuthenticityMarker.DISCOURSE_MARKER_POSITION: "Let the thought flow naturally.",
        }
        return hints.get(marker)


class TelegramReElicitationDispatcher:
    """Dispatches re-elicitation prompts via Telegram.

    Spec: 'DARN-CAT framework prompt dispatched via Telegram.'
    Uses Redis message queue for asynchronous delivery.
    """

    def __init__(
        self,
        redis_client: Optional[object] = None,
        telegram_bot_token: Optional[str] = None,
    ):
        """Initialize with optional Redis and Telegram clients.

        Args:
            redis_client: Redis client for message queueing.
                Spec: 'Redis — Message queue for Telegram delivery on gate failure.'
            telegram_bot_token: Telegram Bot API token for direct delivery.
        """
        self.redis = redis_client
        self.telegram_bot_token = telegram_bot_token
        self.engine = ReElicitationEngine()

    async def dispatch(
        self,
        coach_chat_id: str,
        score: AuthenticityScore,
    ) -> dict:
        """Dispatch a re-elicitation prompt to the coach via Telegram.

        Args:
            coach_chat_id: Telegram chat ID for the coach
            score: AuthenticityScore with failed markers

        Returns:
            Dict with dispatch status and the prompt sent.
        """
        prompt = self.engine.generate_prompt(score)

        message_payload = {
            "chat_id": coach_chat_id,
            "text": prompt,
            "unit_id": score.unit_id,
            "failed_markers": [m.value for m in score.failed_markers],
            "attempt": score.re_elicitation_attempts + 1,
        }

        # Queue via Redis if available (spec: Redis message queue)
        if self.redis is not None:
            try:
                import json
                queue_key = f"re_elicitation:{coach_chat_id}"
                self.redis.rpush(queue_key, json.dumps(message_payload))  # type: ignore
                return {"status": "queued", "prompt": prompt, "via": "redis"}
            except Exception:
                pass  # Fall through to direct dispatch

        # Direct Telegram dispatch as fallback
        if self.telegram_bot_token:
            return await self._send_telegram(coach_chat_id, prompt)

        # No dispatch mechanism available — return prompt for caller to handle
        return {"status": "pending", "prompt": prompt, "via": "none"}

    async def dispatch_insufficient_session(self, coach_chat_id: str) -> dict:
        """Notify coach of an insufficient session.

        Spec: 'coach is notified to continue the conversation over the week.'
        """
        message = self.engine.get_insufficient_session_message()

        if self.redis is not None:
            try:
                import json
                payload = {"chat_id": coach_chat_id, "text": message, "type": "insufficient_session"}
                self.redis.rpush(f"re_elicitation:{coach_chat_id}", json.dumps(payload))  # type: ignore
                return {"status": "queued", "message": message, "via": "redis"}
            except Exception:
                pass

        return {"status": "pending", "message": message, "via": "none"}

    async def _send_telegram(self, chat_id: str, text: str) -> dict:
        """Send message directly via Telegram Bot API."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": text},
                )
                response.raise_for_status()
                return {"status": "sent", "prompt": text, "via": "telegram"}
        except Exception as e:
            return {"status": "failed", "prompt": text, "via": "telegram", "error": str(e)}
