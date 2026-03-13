"""
CCP Sunday Bot Meeting Aggregator
Task 5.01 — Weekly intelligence report from client interaction patterns.

Runs every Sunday. Aggregates across all of a coach's clients:
- Dominant fears emerging across the client base
- Breakthrough themes (what's working)
- Friction points (where clients get stuck)
- Sentiment trends (improving, declining, stable)

Output feeds into ccf-analyze to make next week's content smarter.
"""

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


class SundayBotMeeting:
    """Weekly client intelligence aggregation."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._memory_dir = Path(
            f"coaches/{self.coach_acronym}/intelligence/memory/episodic"
        )
        self._output_dir = Path(
            f"coaches/{self.coach_acronym}/intelligence/research"
        )
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def run(self) -> dict:
        """Run the Sunday Bot Meeting aggregation.

        Returns:
            Intelligence summary dict
        """
        from google import genai

        # Collect all client interactions from the past week
        interactions = self._collect_weekly_interactions()
        if not interactions:
            return {"status": "no_data", "summary": "No client interactions this week."}

        # Format interactions for analysis
        interaction_text = self._format_interactions(interactions)

        # Use Gemini to aggregate patterns
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""You are the Intelligence Analyst for a coaching practice.
Analyze this week's client interactions and produce a structured intelligence report.

INTERACTIONS:
{interaction_text}

Return JSON:
{{
  "dominant_fears": [{{"theme": "...", "frequency": N, "example": "..."}}],
  "breakthrough_themes": [{{"theme": "...", "client_count": N}}],
  "friction_points": [{{"issue": "...", "frequency": N}}],
  "sentiment_trend": "improving/stable/declining",
  "sentiment_detail": "2-sentence explanation",
  "content_recommendations": [
    {{"topic": "...", "angle": "...", "rationale": "This addresses the dominant fear of..."}}
  ],
  "dormancy_risk_clients": ["person_ids with declining engagement"],
  "total_interactions": N,
  "total_clients_active": N
}}""",
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            summary = json.loads(text)
        except json.JSONDecodeError:
            summary = {"status": "parse_error", "raw": text[:500]}

        # Save summary
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        output_file = self._output_dir / f"sunday_meeting_{date_str}.json"
        output_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        # Log
        self.receipt_chain.log(
            agent_id="sunday_bot_meeting",
            action="weekly_aggregation",
            output_summary=f"Trends: {summary.get('sentiment_trend', 'unknown')}, "
                          f"Active: {summary.get('total_clients_active', 0)}",
            decision="completed",
            metadata=summary,
        )

        return summary

    def _collect_weekly_interactions(self) -> list[dict]:
        """Collect all client interactions from the past 7 days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        all_interactions = []

        if not self._memory_dir.exists():
            return []

        for f in self._memory_dir.glob("interactions_*.jsonl"):
            client_id = f.stem.replace("interactions_", "")
            with open(f, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        ts = datetime.fromisoformat(entry.get("timestamp", ""))
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)
                        if ts >= cutoff:
                            entry["client_id"] = client_id
                            all_interactions.append(entry)
                    except (json.JSONDecodeError, ValueError):
                        continue

        return all_interactions

    def _format_interactions(self, interactions: list[dict]) -> str:
        """Format interactions for LLM analysis."""
        grouped: dict[str, list[dict]] = {}
        for i in interactions:
            cid = i.get("client_id", "unknown")
            grouped.setdefault(cid, []).append(i)

        parts = []
        for client_id, client_interactions in grouped.items():
            parts.append(f"\n--- Client {client_id} ({len(client_interactions)} interactions) ---")
            for ci in client_interactions[-10:]:  # Last 10 per client
                parts.append(f"  [{ci.get('type', '')}] Client: {ci.get('client_message', '')[:100]}")
        return "\n".join(parts)

    def get_latest_summary(self) -> Optional[dict]:
        """Get the most recent Sunday meeting summary."""
        summaries = sorted(self._output_dir.glob("sunday_meeting_*.json"), reverse=True)
        if summaries:
            return json.loads(summaries[0].read_text(encoding="utf-8"))
        return None
