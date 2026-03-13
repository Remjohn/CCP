"""
CCP Monthly Cross-Ecosystem Meeting
Task 6.03 — Anonymized intelligence sharing across coach ecosystems.

Runs monthly. For multi-coach operators, aggregates patterns across
ALL ecosystems without revealing individual client data:
- Format performance (which content types consistently perform)
- Engagement trend patterns (what's working across the board)
- Recovery strategy effectiveness (dormancy approaches that work)
- Seasonal content performance (what resonates when)
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


CROSS_ECOSYSTEM_PROMPT = """You are the Cross-Ecosystem Intelligence Analyst.
Analyze anonymized data from multiple coaching ecosystems to find patterns.

ECOSYSTEM SUMMARIES:
{ecosystem_data}

Produce an intelligence briefing for the operator. Include:
1. FORMAT PERFORMANCE: Which content types consistently perform across ecosystems
2. ENGAGEMENT PATTERNS: What engagement strategies work across different audiences
3. RECOVERY STRATEGIES: Which dormancy recovery approaches are most effective
4. SEASONAL INSIGHTS: Content themes that performed well in the current season
5. EMERGING TRENDS: Patterns that are new or growing across ecosystems

CRITICAL RULE: Do NOT reveal any individual client data. All insights must be
at the ecosystem (coach) level or aggregated across ecosystems.

Return JSON:
{{
  "format_performance": [
    {{"format": "...", "avg_engagement": 0.0-1.0, "recommendation": "..."}}
  ],
  "engagement_patterns": ["pattern 1", "pattern 2"],
  "recovery_effectiveness": [
    {{"strategy": "...", "success_rate": 0.0-1.0, "best_for": "..."}}
  ],
  "seasonal_insights": ["insight 1", "insight 2"],
  "emerging_trends": ["trend 1", "trend 2"],
  "operator_recommendations": ["recommendation 1", "recommendation 2"],
  "ecosystems_analyzed": N
}}
"""


class CrossEcosystemMeeting:
    """Monthly anonymized intelligence sharing across coach ecosystems."""

    def __init__(self):
        self._output_dir = Path("intelligence/cross_ecosystem")
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def run(self, coach_acronyms: list[str]) -> dict:
        """Run the monthly cross-ecosystem meeting.

        Args:
            coach_acronyms: List of coach acronyms to include

        Returns:
            Cross-ecosystem intelligence report
        """
        from google import genai

        # Collect anonymized summaries from each ecosystem
        ecosystem_summaries = []
        for i, acronym in enumerate(coach_acronyms, 1):
            summary = self._collect_ecosystem_summary(acronym, label=f"Ecosystem {i}")
            if summary:
                ecosystem_summaries.append(summary)

        if not ecosystem_summaries:
            return {"status": "no_data", "message": "No ecosystem data available."}

        ecosystem_data = "\n\n".join(ecosystem_summaries)

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=CROSS_ECOSYSTEM_PROMPT.format(ecosystem_data=ecosystem_data),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            report = json.loads(text)
        except json.JSONDecodeError:
            report = {"status": "parse_error", "raw": text[:500]}

        # Save report
        date_str = datetime.now(timezone.utc).strftime("%Y%m")
        output_file = self._output_dir / f"cross_ecosystem_{date_str}.json"
        output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

        return report

    def _collect_ecosystem_summary(self, coach_acronym: str, label: str) -> Optional[str]:
        """Collect anonymized summary from one ecosystem."""
        parts = [f"--- {label} ---"]

        # Sunday Bot Meeting data (already aggregated)
        meeting_dir = Path(f"coaches/{coach_acronym}/intelligence/research")
        if meeting_dir.exists():
            meetings = sorted(meeting_dir.glob("sunday_meeting_*.json"), reverse=True)
            if meetings:
                latest = json.loads(meetings[0].read_text(encoding="utf-8"))
                parts.append(f"Active clients: {latest.get('total_clients_active', 'unknown')}")
                parts.append(f"Sentiment: {latest.get('sentiment_trend', 'unknown')}")
                fears = [f.get("theme", "") for f in latest.get("dominant_fears", [])]
                parts.append(f"Dominant themes: {', '.join(fears)}")

        # Engagement data (aggregated, no client details)
        engagement_dir = Path(f"coaches/{coach_acronym}/intelligence/memory/semantic")
        markers_file = engagement_dir / "resonance_markers.json"
        if markers_file.exists():
            markers = json.loads(markers_file.read_text(encoding="utf-8"))
            formats = [m.get("format_type", "") for m in markers]
            parts.append(f"Resonance formats: {', '.join(set(formats))}")
            parts.append(f"Total resonance markers: {len(markers)}")

        return "\n".join(parts) if len(parts) > 1 else None

    def get_latest(self) -> Optional[dict]:
        """Get the latest cross-ecosystem report."""
        reports = sorted(self._output_dir.glob("cross_ecosystem_*.json"), reverse=True)
        if reports:
            return json.loads(reports[0].read_text(encoding="utf-8"))
        return None
