"""
CCP Contrastive Anti-Draft Pipeline
Task 2.05 — Generates better scripts by first generating what NOT to write.

Pipeline:
  1. Flash model generates an anti-draft (what a generic AI would write)
  2. System extracts 5 failure points from the anti-draft
  3. Pro model generates the real draft using anti-draft + failure analysis as negative anchor

This is the implementation of the Contrastive Prompting Protocol
documented in MCDA_Contrastive_Prompting_Anti_Draft_Protocol.md.
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul


ANTI_DRAFT_PROMPT = """Write a DELIBERATELY GENERIC version of the following content brief.
This should be the kind of content that a lazy AI would produce — full of clichés,
empty motivation, and predictable structure. Make it actively boring.

BRIEF:
- Format: {format_label}
- Topic: {topic}
- Angle: {angle}

Write the anti-draft. Be as generic, predictable, and AI-sounding as possible.
Use every cliché in the book. Start with "In today's fast-paced world..."
"""

FAILURE_EXTRACTION_PROMPT = """Analyze this anti-draft and identify EXACTLY 5 specific failure points.
These are the things that make it boring, generic, and obviously AI-generated.

ANTI-DRAFT:
{anti_draft}

For each failure point, explain:
1. What exactly is wrong
2. What makes it feel AI-generated
3. What should be done instead

Return as JSON array:
[
  {{"failure": "...", "why_bad": "...", "instead": "..."}},
  ...
]
"""

CONTRASTIVE_GENERATION_PROMPT = """You are writing as coach {coach_name}. 

VOICE DNA:
- Rhythm: {rhythm}
- Metaphors: {metaphors}
- Vocabulary: {vocabulary}
- Humor: {humor_style}
- Tone: warmth={warmth}, directness={directness}

CONTENT BRIEF:
- Format: {format_label}
- Topic: {topic}
- Angle: {angle}
- Hook concept: {hook}
- Boredom Ban avoidance: {avoidance}

⛔ ANTI-DRAFT (what NOT to write):
{anti_draft}

⛔ FAILURE ANALYSIS (specific things to AVOID):
{failure_analysis}

Now write the REAL version. Your script must:
1. Be the OPPOSITE of the anti-draft in every way
2. Explicitly avoid every failure point identified
3. Sound like {coach_name} on their best day
4. Start with a hook that the anti-draft would never use
5. Use the coach's actual metaphor families and vocabulary
6. End with a genuine provocation, not a summary

Write the final script:
"""


class ContrastiveDraftPipeline:
    """Generate better content through contrastive prompting."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate(
        self,
        soul: CoachSoul,
        idea: dict,
    ) -> dict:
        """Run the full contrastive pipeline for one content piece.

        Args:
            soul: Coach soul profile
            idea: ContentIdea dict

        Returns:
            Dict with final script, anti-draft, and failure analysis
        """
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Step 1: Generate anti-draft (Flash — fast)
        anti_prompt = ANTI_DRAFT_PROMPT.format(
            format_label=idea.get("format_label", "Script"),
            topic=idea.get("topic", ""),
            angle=idea.get("angle", ""),
        )
        anti_response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=anti_prompt
        )
        anti_draft = anti_response.text.strip()

        # Step 2: Extract failure points (Flash)
        failure_prompt = FAILURE_EXTRACTION_PROMPT.format(anti_draft=anti_draft)
        failure_response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=failure_prompt
        )
        failure_text = failure_response.text.strip()
        if failure_text.startswith("```"):
            failure_text = failure_text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            failures = json.loads(failure_text)
        except json.JSONDecodeError:
            failures = [{"failure": "generic tone", "why_bad": "AI-sounding", "instead": "be specific"}]

        failure_analysis = "\n".join(
            f"{i+1}. {f.get('failure', '')} → Instead: {f.get('instead', '')}"
            for i, f in enumerate(failures[:5])
        )

        # Step 3: Generate real draft with contrastive context (Pro — deep reasoning)
        real_prompt = CONTRASTIVE_GENERATION_PROMPT.format(
            coach_name=soul.coach_name,
            rhythm=", ".join(soul.voice_dna.sentence_rhythm),
            metaphors=", ".join(soul.voice_dna.metaphor_patterns),
            vocabulary=", ".join(soul.voice_dna.vocabulary_fingerprint[:10]),
            humor_style=soul.voice_dna.humor_style or "balanced",
            warmth=soul.content_tone.warmth,
            directness=soul.content_tone.directness,
            format_label=idea.get("format_label", "Script"),
            topic=idea.get("topic", ""),
            angle=idea.get("angle", ""),
            hook=idea.get("hook_suggestion", ""),
            avoidance="\n".join(idea.get("avoidance_constraints", [])) or "None",
            anti_draft=anti_draft,
            failure_analysis=failure_analysis,
        )
        real_response = await client.aio.models.generate_content(
            model="gemini-2.0-flash", contents=real_prompt
        )
        final_script = real_response.text.strip()

        # Log the full pipeline
        self.receipt_chain.log(
            agent_id="contrastive_pipeline",
            action="generate_contrastive_draft",
            asset_id=idea.get("asset_id", ""),
            input_summary=f"Topic: {idea.get('topic', '')[:80]}",
            output_summary=f"Anti-draft: {len(anti_draft.split())}w → {len(failures)} failures → Final: {len(final_script.split())}w",
            decision="completed",
            metadata={
                "anti_draft_words": len(anti_draft.split()),
                "failure_count": len(failures),
                "final_words": len(final_script.split()),
            },
        )

        return {
            "asset_id": idea.get("asset_id", ""),
            "script": final_script,
            "anti_draft": anti_draft,
            "failure_analysis": failures,
            "word_count": len(final_script.split()),
            "stage": "contrastive_draft",
        }
