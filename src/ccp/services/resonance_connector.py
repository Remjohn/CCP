"""
CCP Resonance Hit Formula Connector
Task 6.04 — Cross-references content themes with client patterns.

When a content piece's theme matches a client's active pattern,
it adds a 🟣 RESONANCE HIT indicator to both the content and
the client record, creating a visible bridge between CCF output
and CBCS client reality.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class ResonanceHit(BaseModel):
    """A detected resonance between content and a client pattern."""

    content_asset_id: str
    content_topic: str
    client_person_id: str
    pattern_description: str
    match_strength: float = Field(ge=0.0, le=1.0)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ResonanceConnector:
    """Detect and surface resonance between content and client patterns."""

    MATCH_THRESHOLD = 0.6  # Minimum match strength for a resonance hit

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._data_dir = Path(
            f"coaches/{self.coach_acronym}/intelligence/memory/semantic"
        )
        self._hits_file = self._data_dir / "resonance_hits.jsonl"
        self._data_dir.mkdir(parents=True, exist_ok=True)

    async def scan_for_hits(
        self,
        content_items: list[dict],
        client_patterns: list[dict],
    ) -> list[ResonanceHit]:
        """Scan for resonance between content and client patterns.

        Args:
            content_items: List of dicts with asset_id, topic, theme
            client_patterns: List of dicts with person_id, patterns

        Returns:
            List of detected resonance hits
        """
        import os
        from google import genai

        if not content_items or not client_patterns:
            return []

        # Format for analysis
        content_summary = "\n".join(
            f"- [{c.get('asset_id', '')}] {c.get('topic', '')}: {c.get('theme', '')}"
            for c in content_items
        )

        patterns_summary = "\n".join(
            f"- [{p.get('person_id', '')}] Patterns: {', '.join(p.get('patterns', []))}"
            for p in client_patterns
        )

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""Cross-reference these content pieces with client patterns to find RESONANCE HITS.

A resonance hit is when a content piece directly addresses or relates to a client's active pattern.

CONTENT:
{content_summary}

CLIENT PATTERNS:
{patterns_summary}

Return JSON array (only include genuine matches with strength >= 0.6):
[
  {{
    "content_asset_id": "...",
    "content_topic": "...",
    "client_person_id": "...",
    "pattern_description": "...",
    "match_strength": 0.0-1.0,
    "connection": "Why this content resonates with this client's pattern"
  }}
]""",
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            raw_hits = json.loads(text)
        except json.JSONDecodeError:
            return []

        hits = []
        for raw in raw_hits:
            if raw.get("match_strength", 0) < self.MATCH_THRESHOLD:
                continue
            hit = ResonanceHit(
                content_asset_id=raw.get("content_asset_id", ""),
                content_topic=raw.get("content_topic", ""),
                client_person_id=raw.get("client_person_id", ""),
                pattern_description=raw.get("pattern_description", ""),
                match_strength=raw.get("match_strength", 0.6),
            )
            hits.append(hit)

            # Save
            with open(self._hits_file, "a", encoding="utf-8") as f:
                f.write(hit.model_dump_json() + "\n")

        if hits:
            self.receipt_chain.log(
                agent_id="resonance_connector",
                action="detect_resonance_hits",
                output_summary=f"🟣 {len(hits)} RESONANCE HITS detected",
                decision="completed",
                metadata={"hit_count": len(hits)},
            )

        return hits

    def get_hits_for_client(self, person_id: str) -> list[ResonanceHit]:
        """Get all resonance hits for a specific client."""
        if not self._hits_file.exists():
            return []
        hits = []
        with open(self._hits_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    hit = ResonanceHit.model_validate_json(line)
                    if hit.client_person_id == person_id:
                        hits.append(hit)
        return hits

    def get_hits_for_content(self, asset_id: str) -> list[ResonanceHit]:
        """Get all resonance hits for a content piece."""
        if not self._hits_file.exists():
            return []
        hits = []
        with open(self._hits_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    hit = ResonanceHit.model_validate_json(line)
                    if hit.content_asset_id == asset_id:
                        hits.append(hit)
        return hits
