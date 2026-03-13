"""
CCP Ritual Resonance Delivery
Task 6.05 — Enhances ritual delivery with content-client resonance hits.

When a content piece matches a client's active pattern, the ritual
delivery can reference it naturally:
  "Something your coach just created touched on exactly what
   you've been working through — have you seen it?"

This creates a bridge between CCF content and CBCS client experience.
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.resonance_connector import ResonanceConnector


RESONANCE_RITUAL_PROMPT = """You are coaching as {coach_name}. You want to naturally reference
a content piece that resonates with what your client is working on.

CLIENT'S ACTIVE PATTERN: {pattern}
CONTENT TOPIC: {content_topic}
MATCH STRENGTH: {match_strength:.0%}

INTERACTION TYPE: {interaction_type}

Write a brief, natural reference to this content (1-2 sentences max).
Rules:
1. Don't say "I wrote a post about..." — that sounds self-promoting
2. Frame it as a thought or insight you've been exploring
3. Make it feel like a natural part of the conversation
4. If it's a morning ritual, weave it into the intention
5. If it's an evening ritual, weave it into the reflection
6. Sound like {coach_name}, not an AI suggesting content

Write the resonance reference:
"""


class RitualResonance:
    """Enhance ritual delivery with content-client resonance hits."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.resonance = ResonanceConnector(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def get_resonance_enhancement(
        self,
        person_id: str,
        interaction_type: str = "morning",
    ) -> Optional[str]:
        """Check for resonance hits and generate a natural reference.

        Args:
            person_id: Client Person ID
            interaction_type: Type of ritual (morning, midday, evening)

        Returns:
            Enhancement text to weave into the ritual, or None
        """
        # Get recent resonance hits for this client
        hits = self.resonance.get_hits_for_client(person_id)
        if not hits:
            return None

        # Use the most recent, strongest hit
        best_hit = max(hits, key=lambda h: h.match_strength)

        # Generate the natural reference
        from google import genai

        soul_data = self._load_soul()
        coach_name = soul_data.get("coach_name", "Coach")

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=RESONANCE_RITUAL_PROMPT.format(
                coach_name=coach_name,
                pattern=best_hit.pattern_description,
                content_topic=best_hit.content_topic,
                match_strength=best_hit.match_strength,
                interaction_type=interaction_type,
            ),
        )

        enhancement = response.text.strip()

        self.receipt_chain.log(
            agent_id="ritual_resonance",
            action="generate_enhancement",
            person_id=person_id,
            asset_id=best_hit.content_asset_id,
            output_summary=f"Resonance weave: {enhancement[:60]}...",
            decision="enhanced",
            metadata={"match_strength": best_hit.match_strength},
        )

        return enhancement

    def _load_soul(self) -> dict:
        from pathlib import Path
        soul_path = Path(f"coaches/{self.coach_acronym}/config/coach_soul.json")
        if soul_path.exists():
            return json.loads(soul_path.read_text(encoding="utf-8"))
        return {}
