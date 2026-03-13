"""
CCP SoulResonance — Emotional Continuity Engine
Task 3.10 — Generates context-aware coaching responses that maintain emotional continuity.

This is the core response generator for ALL CBCS client interactions.
Every response passes through SoulResonance to ensure:
1. Voice DNA alignment (sounds like the coach)
2. Context Premise awareness (references client's journey)
3. Emotional continuity (remembers last emotional state)
4. Engagement calibration (adapts depth to interaction type)
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


RESPONSE_PROMPT = """You ARE coach {coach_name}. Not an AI pretending to be a coach — you ARE the coach.

YOUR VOICE:
- Rhythm: {rhythm}
- Metaphors: {metaphors}
- Vocabulary: {vocabulary}
- Humor: {humor_style}
- Tone: warmth={warmth}, directness={directness}

CLIENT CONTEXT:
{client_context}

LAST EMOTIONAL STATE: {last_emotion}

INTERACTION TYPE: {interaction_type}

CLIENT JUST SAID:
"{message}"

{additional_context}

Generate a response. Rules by interaction type:

RITUAL_RESPONSE (reply to accountability check-in):
- Maximum 2 sentences. Quick, warm, specific acknowledgment.
- Name what they committed to. Celebrate small wins.

JOURNAL_RESPONSE (they shared a reflection):
- Maximum 3 sentences. Go deeper on ONE thing they said.
- Mirror their language. Ask a follow-up that pushes gently.

VOICE_RESPONSE (they sent a voice note):
- Maximum 3 sentences. Match their emotional energy.
- Reference something specific from the transcription.

GREETING (they're saying hello or checking in):
- Maximum 2 sentences. Warm, personal, reference recent context.
- If they've been away, acknowledge without guilt.

GENERAL (coaching question or conversation):
- Maximum 4 sentences. Answer with coaching, not advice.
- Ask a question that shifts their perspective.
- Use ONE metaphor from your natural metaphor families.

UNIVERSAL RULES:
1. NEVER start with "Great question!" or "I love that!" or "That's so powerful!"
2. NEVER use the phrase "I hear you" unless you genuinely mean it in context.
3. Match their emotional register. If they're heavy, be grounded. If they're light, be playful.
4. End with a genuine question or invitation, NEVER a summary or cliché.
5. Maximum 1 emoji, and only if it feels natural.
6. You are writing a REAL message to a REAL person. Act like it.

Write your response:
"""


class SoulResonance:
    """Generate emotionally continuous coaching responses."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._memory_dir = Path(
            f"coaches/{self.coach_acronym}/intelligence/memory/episodic"
        )
        self._memory_dir.mkdir(parents=True, exist_ok=True)

    async def generate_response(
        self,
        client_id: str,
        message_text: str,
        interaction_type: str,
        context: Optional[dict] = None,
    ) -> str:
        """Generate a coach-voiced response with emotional continuity.

        Args:
            client_id: Client's identifier (Telegram user ID)
            message_text: The client's message
            interaction_type: Type of interaction
            context: Optional extracted context from Aria

        Returns:
            Response text in the coach's voice
        """
        from google import genai

        # Load coach soul
        soul_data = self._load_soul()

        # Get client context from Neo4j
        client_context = await self._get_client_context(client_id)

        # Get last emotional state for continuity
        last_emotion = self._get_last_emotion(client_id)

        # Additional context from extraction
        additional = ""
        if context:
            emotional_state = context.get("emotional_state", "")
            if emotional_state:
                additional += f"\nCURRENT EMOTIONAL STATE (detected): {emotional_state}\n"
            pattern_alert = context.get("pattern_alert")
            if pattern_alert:
                additional += f"\n⚠️ PATTERN ALERT: {pattern_alert}\n"

        prompt = RESPONSE_PROMPT.format(
            coach_name=soul_data.get("coach_name", "Coach"),
            rhythm=", ".join(soul_data.get("voice_dna", {}).get("sentence_rhythm", [])),
            metaphors=", ".join(soul_data.get("voice_dna", {}).get("metaphor_patterns", [])),
            vocabulary=", ".join(soul_data.get("voice_dna", {}).get("vocabulary_fingerprint", [])[:8]),
            humor_style=soul_data.get("voice_dna", {}).get("humor_style", "warm"),
            warmth=soul_data.get("content_tone", {}).get("warmth", 0.7),
            directness=soul_data.get("content_tone", {}).get("directness", 0.5),
            client_context=client_context,
            last_emotion=last_emotion,
            interaction_type=interaction_type.upper(),
            message=message_text[:1000],
            additional_context=additional,
        )

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        response_text = response.text.strip()

        # Update emotional memory for continuity
        new_emotion = "engaged"
        if context and context.get("emotional_state"):
            new_emotion = context["emotional_state"]
        self._save_emotion(client_id, new_emotion)

        # Save interaction to episodic memory
        self._save_interaction(client_id, message_text, response_text, interaction_type)

        # Log
        self.receipt_chain.log(
            agent_id="soul_resonance",
            action="generate_response",
            person_id=f"{self.coach_acronym}-{client_id}",
            input_summary=f"{interaction_type}: {message_text[:80]}",
            output_summary=f"Response: {len(response_text)} chars",
            decision="sent",
            metadata={
                "interaction_type": interaction_type,
                "emotional_state": new_emotion,
            },
        )

        return response_text

    def _load_soul(self) -> dict:
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        if soul_path.exists():
            return json.loads(soul_path.read_text(encoding="utf-8"))
        return {}

    async def _get_client_context(self, client_id: str) -> str:
        """Get Context Premise narrative from Neo4j."""
        try:
            from src.ccp.scripts.setup_neo4j import ContextPremiseGraph
            graph = ContextPremiseGraph(coach_acronym=self.coach_acronym)
            person_id = f"{self.coach_acronym}-{client_id}"
            narrative = graph.get_narrative(person_id)
            graph.close()
            return narrative
        except Exception:
            return "Building context from conversations..."

    def _get_last_emotion(self, client_id: str) -> str:
        """Get the last recorded emotional state for continuity."""
        emotion_file = self._memory_dir / f"emotion_{client_id}.json"
        if emotion_file.exists():
            data = json.loads(emotion_file.read_text(encoding="utf-8"))
            return data.get("emotion", "neutral")
        return "first_interaction"

    def _save_emotion(self, client_id: str, emotion: str) -> None:
        """Save current emotional state for next interaction."""
        emotion_file = self._memory_dir / f"emotion_{client_id}.json"
        data = {
            "emotion": emotion,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        emotion_file.write_text(json.dumps(data), encoding="utf-8")

    def _save_interaction(
        self, client_id: str, message: str, response: str, interaction_type: str
    ) -> None:
        """Save interaction to episodic memory for future context."""
        memory_file = self._memory_dir / f"interactions_{client_id}.jsonl"
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": interaction_type,
            "client_message": message[:500],
            "coach_response": response[:500],
        }
        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
