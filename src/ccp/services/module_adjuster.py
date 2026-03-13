"""
CCP Dynamic Module Adjuster
Task 6.02 — Adjusts webinar module emphasis based on audience Context Premises.

Aggregates all registered clients' Context Premises and ranks
webinar modules by theme relevance to the CURRENT audience.
Adjusts module duration and emphasis accordingly.
"""

import json
import os
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain


ADJUSTMENT_PROMPT = """You are adjusting a webinar's module emphasis based on the current audience.

WEBINAR MODULES:
{modules_summary}

AUDIENCE CONTEXT PREMISES (aggregated):
- Dominant fears: {dominant_fears}
- Breakthrough themes: {breakthroughs}
- Active goals: {goals}
- Friction points: {friction}

Rank each module by relevance to this audience and suggest adjustments.

Return JSON:
{{
  "rankings": [
    {{
      "module_number": N,
      "relevance_score": 0.0-1.0,
      "suggested_duration_change": "+5min / -3min / no change",
      "emphasis_adjustment": "Lean into fear X when teaching this / Add example about Y",
      "audience_connection": "This connects to their dominant fear of..."
    }}
  ],
  "recommended_order": [module numbers in recommended delivery order],
  "critical_module": "Module N is most important because...",
  "optional_module": "Module N could be shortened because..."
}}
"""


class DynamicModuleAdjuster:
    """Adjust webinar module emphasis for the current audience."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def adjust(
        self,
        webinar_json_path: str,
        audience_context: Optional[dict] = None,
    ) -> dict:
        """Adjust module emphasis based on audience data.

        Args:
            webinar_json_path: Path to webinar script JSON
            audience_context: Aggregated audience context (from Sunday Bot Meeting)

        Returns:
            Adjustment recommendations
        """
        from google import genai

        webinar = json.loads(Path(webinar_json_path).read_text(encoding="utf-8"))

        # If no audience context provided, load from Sunday Bot Meeting
        if audience_context is None:
            audience_context = self._load_audience_context()

        # Format modules
        modules_summary = "\n".join(
            f"Module {m.get('module_number', '?')}: {m.get('title', '')} — {m.get('teaching_point', '')[:80]} ({m.get('duration_minutes', 0)}min)"
            for m in webinar.get("modules", [])
        )

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=ADJUSTMENT_PROMPT.format(
                modules_summary=modules_summary,
                dominant_fears=", ".join(
                    f.get("theme", "") for f in audience_context.get("dominant_fears", [])
                ),
                breakthroughs=", ".join(
                    b.get("theme", "") for b in audience_context.get("breakthrough_themes", [])
                ),
                goals=", ".join(audience_context.get("active_goals", ["general growth"])),
                friction=", ".join(
                    f.get("issue", "") for f in audience_context.get("friction_points", [])
                ),
            ),
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            adjustments = json.loads(text)
        except json.JSONDecodeError:
            adjustments = {"rankings": [], "error": "Parse error"}

        self.receipt_chain.log(
            agent_id="module_adjuster",
            action="adjust_modules",
            asset_id=webinar.get("asset_id", ""),
            output_summary=f"Ranked {len(adjustments.get('rankings', []))} modules for audience",
            decision="completed",
        )

        return adjustments

    def _load_audience_context(self) -> dict:
        """Load the latest Sunday Bot Meeting summary as audience context."""
        from src.ccp.services.sunday_bot_meeting import SundayBotMeeting
        meeting = SundayBotMeeting(coach_acronym=self.coach_acronym)
        summary = meeting.get_latest_summary()
        return summary or {"dominant_fears": [], "breakthrough_themes": [], "friction_points": []}
