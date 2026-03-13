"""
CCP Leadership Trait Scorer
Task 1.13 — Scores the coach across 12 leadership dimensions.

Uses Sacred Audio transcripts + onboarding interview to assess:
- Deep Empathy, Authentic Vulnerability, Embodied Confidence
- Strategic Patience, Radical Honesty, Grounded Presence
- Visionary Clarity, Playful Irreverence, Fierce Compassion
- Sacred Boundaries, Intuitive Timing, Sovereign Authority

Scores drive content format assignment:
  Weak traits → exercise formats (more practice)
  Strong traits → showcase formats (amplification)
"""

import json
import os
from typing import Optional

from src.ccp.models.coach_soul import LeadershipScores


SCORING_PROMPT = """You are the Minister of Identity for the Conscious Coaching Platform.

Your task: Score this coach across 12 leadership dimensions based on their Sacred Audio transcripts and onboarding interview.

SACRED AUDIO TRANSCRIPTS:
{transcripts}

ONBOARDING INTERVIEW:
{interview}

Score each dimension 0-100 based on evidence in the text. A score represents how strongly the coach DEMONSTRATES this trait in their natural communication:

- 0-20: No evidence of this trait
- 21-40: Occasional hints, underdeveloped
- 41-60: Present but inconsistent
- 61-80: Clearly developed and frequently demonstrated
- 81-100: Defining characteristic, deeply embodied

Return ONLY valid JSON:

{{
  "deep_empathy": {{
    "score": 0-100,
    "evidence": "Specific quote or pattern from the text"
  }},
  "authentic_vulnerability": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "embodied_confidence": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "strategic_patience": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "radical_honesty": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "grounded_presence": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "visionary_clarity": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "playful_irreverence": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "fierce_compassion": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "sacred_boundaries": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "intuitive_timing": {{
    "score": 0-100,
    "evidence": "..."
  }},
  "sovereign_authority": {{
    "score": 0-100,
    "evidence": "..."
  }}
}}

Rules:
1. Every score MUST have a specific evidence quote from the text.
2. If no evidence exists for a trait, score it 15-25 (not zero — absence is data, not failure).
3. No trait should score above 90 unless the evidence is overwhelming and repeated.
4. Avoid central tendency — spread your scores. A coach with all 50s is useless for format assignment.
5. Return ONLY the JSON, no markdown, no explanation.
"""


class LeadershipTraitScorer:
    """Score a coach across 12 leadership dimensions using LLM analysis."""

    TRAIT_NAMES = [
        "deep_empathy", "authentic_vulnerability", "embodied_confidence",
        "strategic_patience", "radical_honesty", "grounded_presence",
        "visionary_clarity", "playful_irreverence", "fierce_compassion",
        "sacred_boundaries", "intuitive_timing", "sovereign_authority",
    ]

    def __init__(self, gemini_api_key: Optional[str] = None):
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for leadership scoring")

    async def score(
        self,
        sacred_audio_transcripts: list[str],
        interview_transcript: str,
    ) -> tuple[LeadershipScores, dict[str, str]]:
        """Score a coach across 12 leadership dimensions.

        Args:
            sacred_audio_transcripts: List of transcribed Sacred Audio recordings
            interview_transcript: The onboarding interview transcript

        Returns:
            Tuple of (LeadershipScores, evidence_dict) where evidence_dict
            maps trait names to the supporting evidence quotes.
        """
        from google import genai

        client = genai.Client(api_key=self.api_key)

        prompt = SCORING_PROMPT.format(
            transcripts="\n\n---\n\n".join(sacred_audio_transcripts),
            interview=interview_transcript,
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        # Parse response
        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        raw_scores = json.loads(response_text)

        # Extract scores and evidence
        scores_dict = {}
        evidence_dict = {}
        for trait in self.TRAIT_NAMES:
            trait_data = raw_scores.get(trait, {"score": 20, "evidence": "No data"})
            score = int(trait_data.get("score", 20))
            scores_dict[trait] = max(0, min(100, score))  # Clamp to 0-100
            evidence_dict[trait] = trait_data.get("evidence", "")

        leadership_scores = LeadershipScores(**scores_dict)

        return leadership_scores, evidence_dict

    def format_report(
        self,
        scores: LeadershipScores,
        evidence: dict[str, str],
    ) -> str:
        """Generate a human-readable leadership trait report.

        This report is for the Operator — not the coach.
        """
        lines = ["# Leadership Trait Assessment\n"]

        scores_dict = scores.model_dump()
        sorted_traits = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)

        for trait, score in sorted_traits:
            bar = "🟢" * (score // 10) + "⚪" * (10 - score // 10)
            trait_name = trait.replace("_", " ").title()
            ev = evidence.get(trait, "")
            lines.append(f"**{trait_name}** ({score}/100) {bar}")
            if ev:
                lines.append(f"> {ev}\n")

        # Summary
        lines.append("\n---")
        lines.append(f"\n**Dominant trait:** {scores.dominant_trait().replace('_', ' ').title()}")
        lines.append(f"**Balance ratio:** {scores.trait_balance_ratio():.0%}")
        lines.append(f"\n**Exercise targets** (< 40): {', '.join(t.replace('_', ' ').title() for t in scores.get_weak_traits()) or 'None'}")
        lines.append(f"**Showcase strength** (≥ 70): {', '.join(t.replace('_', ' ').title() for t in scores.get_strong_traits()) or 'None'}")

        return "\n".join(lines)
