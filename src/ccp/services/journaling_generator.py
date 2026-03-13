"""
CCP Journaling Prompt Generator
Task 3.05 — Generates personalized journaling prompts based on Context Premise.

Uses the client's graph data (active fears, patterns, victories)
to craft targeted prompts that gently push growth edges.
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


JOURNALING_PROMPT = """You are generating a journaling prompt for a coaching client.

COACH: {coach_name}
COACH VOICE: warmth={warmth}, directness={directness}

CLIENT CONTEXT:
{client_context}

PROMPT TYPE: {prompt_type}

Generate ONE journaling prompt. Rules:
1. Maximum 2-3 sentences
2. Reference something specific from their context
3. Ask them to explore, not just answer
4. Make it feel safe but slightly uncomfortable (growth edge)
5. Prompt types:
   - fear_exploration: Gently approach a fear they've mentioned
   - pattern_awareness: Help them see a recurring pattern
   - victory_amplification: Build on a recent win
   - dream_clarification: Sharpen a vague aspiration
   - relationship_reflection: Explore an ally or enemy dynamic
   - gratitude_specific: Specific gratitude (not generic)
6. Sound like {coach_name}, not a therapist

Write the journaling prompt:
"""


class JournalingGenerator:
    """Generate personalized journaling prompts from Context Premise data."""

    PROMPT_TYPES = [
        "fear_exploration",
        "pattern_awareness",
        "victory_amplification",
        "dream_clarification",
        "relationship_reflection",
        "gratitude_specific",
    ]

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate(
        self,
        person_id: str,
        prompt_type: Optional[str] = None,
        client_context: str = "",
    ) -> str:
        """Generate a personalized journaling prompt.

        Args:
            person_id: Client Person ID
            prompt_type: Type of prompt (auto-selected if None)
            client_context: Client's Context Premise narrative

        Returns:
            Journaling prompt text
        """
        from google import genai

        if prompt_type is None:
            prompt_type = self._select_prompt_type(client_context)

        # Load coach soul
        soul_path = __import__("pathlib").Path(
            f"coaches/{self.coach_acronym}/config/coach_soul.json"
        )
        soul_data = {}
        if soul_path.exists():
            soul_data = json.loads(soul_path.read_text(encoding="utf-8"))

        prompt = JOURNALING_PROMPT.format(
            coach_name=soul_data.get("coach_name", "Coach"),
            warmth=soul_data.get("content_tone", {}).get("warmth", 0.7),
            directness=soul_data.get("content_tone", {}).get("directness", 0.5),
            client_context=client_context or "New client, building context.",
            prompt_type=prompt_type,
        )

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        result = response.text.strip()

        self.receipt_chain.log(
            agent_id="journaling_generator",
            action="generate_prompt",
            person_id=person_id,
            output_summary=f"{prompt_type}: {result[:80]}...",
            decision="sent",
            metadata={"prompt_type": prompt_type},
        )

        return result

    def _select_prompt_type(self, context: str) -> str:
        """Auto-select the best prompt type based on available context."""
        context_lower = context.lower()
        if "fear" in context_lower or "scared" in context_lower:
            return "fear_exploration"
        if "pattern" in context_lower or "keep doing" in context_lower:
            return "pattern_awareness"
        if "win" in context_lower or "victory" in context_lower:
            return "victory_amplification"
        if "dream" in context_lower or "want to" in context_lower:
            return "dream_clarification"
        return "gratitude_specific"
