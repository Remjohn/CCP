"""
CCP Aria Voice Note Processor
Task 3.06 — Transcribes client voice notes and updates Context Premise.

Pipeline:
  1. Groq transcription (< 5s)
  2. Context Premise extraction (Fears, Enemies, Dreams, Allies, Victories, Patterns)
  3. Update Neo4j graph
  4. Trigger pattern alerts on significant new findings
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.groq_transcriber import GroqTranscriber


EXTRACTION_PROMPT = """You are Aria, the Context Analyst. Extract psychological dimensions from this client message.

CLIENT MESSAGE (transcribed from voice):
"{transcript}"

Extract any of these dimensions that are present. Only include dimensions you are confident about.

Return JSON:
{{
  "fears": [{{"description": "...", "intensity": 0.0-1.0}}],
  "enemies": [{{"description": "...", "type": "internal/external"}}],
  "dreams": [{{"description": "...", "clarity": 0.0-1.0}}],
  "allies": [{{"description": "...", "role": "..."}}],
  "victories": [{{"description": "...", "significance": 0.0-1.0}}],
  "patterns": [{{"description": "...", "pattern_type": "behavioral/emotional/relational", "frequency": "recurring/new/escalating"}}],
  "emotional_state": "current emotional state in 2-3 words",
  "pattern_alert": "null or a brief alert if a significant new pattern is detected"
}}

Rules:
1. Only extract what's explicitly stated or strongly implied. Don't infer too deeply.
2. Use the client's own language where possible.
3. Intensity/clarity scores: 0.3=mild, 0.5=moderate, 0.7=strong, 0.9=overwhelming.
4. Pattern alerts should only fire for truly significant or concerning patterns.
5. Return ONLY the JSON.
"""


class AriaProcessor:
    """Process client voice notes — transcribe and extract Context Premise."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self.transcriber = GroqTranscriber()

    async def process_voice_note(self, message) -> Optional[str]:
        """Process a voice note from a Telegram message.

        Args:
            message: TelegramMessage with voice data

        Returns:
            Response text for the client
        """
        # Download the voice file from Telegram
        voice_url = await self._get_voice_url(message)
        if not voice_url:
            return "I received your voice note but had trouble processing it. Could you try again?"

        # Transcribe
        result = self.transcriber.transcribe_url(voice_url)
        transcript = result.text

        # Extract context dimensions
        extracted = await self._extract_context(transcript)

        # Update Neo4j graph
        person_id = f"{self.coach_acronym}-{message.user.id}"
        await self._update_graph(person_id, extracted)

        # Log
        self.receipt_chain.log(
            agent_id="aria",
            action="process_voice_note",
            person_id=person_id,
            input_summary=f"Voice: {result.duration_seconds:.1f}s → {len(transcript)} chars",
            output_summary=f"Extracted: {self._count_dimensions(extracted)} dimensions",
            decision="completed",
            metadata={
                "duration": result.duration_seconds,
                "processing_ms": result.processing_time_ms,
                "dimensions": self._count_dimensions(extracted),
                "emotional_state": extracted.get("emotional_state", ""),
                "pattern_alert": extracted.get("pattern_alert"),
            },
        )

        # Generate response using SoulResonance
        from src.ccp.services.soul_resonance import SoulResonance
        resonance = SoulResonance(coach_acronym=self.coach_acronym)
        return await resonance.generate_response(
            client_id=str(message.user.id),
            message_text=transcript,
            interaction_type="voice_response",
            context=extracted,
        )

    async def _get_voice_url(self, message) -> Optional[str]:
        """Get the download URL for a Telegram voice note."""
        import httpx

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not bot_token:
            return None

        voice = message.voice or message.audio
        if not voice:
            return None

        file_id = voice.get("file_id", "")
        url = f"https://api.telegram.org/bot{bot_token}/getFile"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params={"file_id": file_id})
            data = response.json()
            file_path = data.get("result", {}).get("file_path", "")
            if file_path:
                return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

        return None

    async def _extract_context(self, transcript: str) -> dict:
        """Extract Context Premise dimensions from transcript text."""
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=EXTRACTION_PROMPT.format(transcript=transcript),
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"emotional_state": "unknown", "pattern_alert": None}

    async def _update_graph(self, person_id: str, extracted: dict) -> None:
        """Update the Neo4j Context Premise graph with extracted dimensions."""
        try:
            from src.ccp.scripts.setup_neo4j import ContextPremiseGraph
            graph = ContextPremiseGraph(coach_acronym=self.coach_acronym)

            import hashlib
            for fear in extracted.get("fears", []):
                fid = hashlib.md5(fear["description"].encode()).hexdigest()[:8]
                graph.add_dimension(
                    person_id, "fear", fid,
                    description=fear["description"],
                    emotional_weight=fear.get("intensity", 0.5),
                    intensity=fear.get("intensity", 0.5),
                    source="voice_note",
                )
            for victory in extracted.get("victories", []):
                vid = hashlib.md5(victory["description"].encode()).hexdigest()[:8]
                graph.add_dimension(
                    person_id, "victory", vid,
                    description=victory["description"],
                    emotional_weight=victory.get("significance", 0.5),
                    significance=victory.get("significance", 0.5),
                    date_achieved=None,
                )
            # Similar for other dimensions...
            graph.close()
        except Exception:
            pass  # Neo4j unavailable — log but don't block

    @staticmethod
    def _count_dimensions(extracted: dict) -> int:
        count = 0
        for key in ["fears", "enemies", "dreams", "allies", "victories", "patterns"]:
            count += len(extracted.get(key, []))
        return count
