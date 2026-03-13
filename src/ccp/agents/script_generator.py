"""
CCP Script Generator Core
Task 2.04 — Generates content scripts from ideas using coach Voice DNA.

Takes a ContentIdea + CoachSoul + research context and produces
a draft script. Applies TTT calibration to match the coach's voice.
"""

import json
import os
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul


SCRIPT_GENERATION_PROMPT = """You are writing as coach {coach_name}. Your voice has these characteristics:
- Rhythm: {rhythm}
- Metaphor families: {metaphors}
- Signature vocabulary: {vocabulary}
- Humor style: {humor_style}
- Tone: warmth={warmth}, directness={directness}, humor_weight={humor}

CONTENT BRIEF:
- Format: {format_label}
- Topic: {topic}
- Angle: {angle}
- Opening hook concept: {hook}
- Target trait: {target_trait} ({trait_mode})
- Suggested metaphors: {suggested_metaphors}

CONSTRAINTS (Boredom Ban):
{avoidance_constraints}

{research_context}

Write the full script in the coach's voice. Follow these rules:

1. START with a hook that grabs attention in the first line. No preamble.
2. Write EXACTLY as the coach would speak — use their vocabulary, rhythm, metaphors.
3. If trait_mode is 'exercise', challenge the audience to develop that trait.
4. If trait_mode is 'showcase', demonstrate the coach's mastery of that trait.
5. Match the format requirements:
   - Thread: 5-8 connected posts, each can stand alone
   - Carousel: slide-by-slide text (Slide 1, Slide 2, etc.)
   - Reel Script: spoken word script with timing notes
   - Quote Card: one powerful sentence + optional attribution
   - Meme: setup + punchline + image description
   - Article: 600-800 word long-form piece
   - Story: informal, behind-the-scenes tone
   - Poll: question + 2-4 options + engagement prompt
6. End with a call to engagement (question, challenge, invitation) — NOT a summary.
7. Do NOT use: "Let's dive in", "In today's post", "Without further ado", or any AI clichés.
8. Do NOT use emojis excessively. Maximum 3 per piece, strategically placed.
"""


class ScriptGenerator:
    """Generate content scripts in the coach's voice."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def generate(
        self,
        soul: CoachSoul,
        idea: dict,
        research_context: str = "",
    ) -> dict:
        """Generate a content script from an idea.

        Args:
            soul: Coach soul profile for voice calibration
            idea: ContentIdea dict from ccf-analyze
            research_context: Optional research to inform the content

        Returns:
            Dict with script text, metadata, and quality signals
        """
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        research_section = ""
        if research_context:
            research_section = f"\nRESEARCH CONTEXT:\n{research_context}\n"

        prompt = SCRIPT_GENERATION_PROMPT.format(
            coach_name=soul.coach_name,
            rhythm=", ".join(soul.voice_dna.sentence_rhythm),
            metaphors=", ".join(soul.voice_dna.metaphor_patterns),
            vocabulary=", ".join(soul.voice_dna.vocabulary_fingerprint[:10]),
            humor_style=soul.voice_dna.humor_style or "balanced",
            warmth=soul.content_tone.warmth,
            directness=soul.content_tone.directness,
            humor=soul.content_tone.humor_weight,
            format_label=idea.get("format_label", idea.get("format_type", "Script")),
            topic=idea.get("topic", ""),
            angle=idea.get("angle", ""),
            hook=idea.get("hook_suggestion", ""),
            target_trait=idea.get("target_trait", ""),
            trait_mode=idea.get("trait_mode", "exercise"),
            suggested_metaphors=", ".join(idea.get("suggested_metaphors", [])),
            avoidance_constraints="\n".join(
                f"- {c}" for c in idea.get("avoidance_constraints", [])
            ) or "No constraints.",
            research_context=research_section,
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        script_text = response.text.strip()

        result = {
            "asset_id": idea.get("asset_id", ""),
            "format_type": idea.get("format_type", "SCRP"),
            "format_label": idea.get("format_label", "Script"),
            "topic": idea.get("topic", ""),
            "angle": idea.get("angle", ""),
            "target_trait": idea.get("target_trait", ""),
            "trait_mode": idea.get("trait_mode", ""),
            "script": script_text,
            "word_count": len(script_text.split()),
            "stage": "draft",
        }

        self.receipt_chain.log(
            agent_id="script_generator",
            action="generate_draft",
            asset_id=idea.get("asset_id", ""),
            input_summary=f"{idea.get('format_label', '')}: {idea.get('topic', '')[:80]}",
            output_summary=f"Draft: {len(script_text.split())} words",
            decision="draft_generated",
            metadata={"word_count": result["word_count"]},
        )

        return result
