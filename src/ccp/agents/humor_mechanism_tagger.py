"""
CCP Humor Mechanism Tagger — FR1 Unit 11
Step 11-D: Post-generation humor_mechanism_tag JSONB on content_performance

Spec reference: FR1 Tech Spec §Step 11-D
Architecture reference: CCP_Technical_Architecture.md §3.4

After script generation, every piece of content must have a humor_mechanism_tag
JSONB column populated in the content_performance table.

AC8: 'Every generated script has humor_mechanism_tag populated.
When no mechanism applies, the tag is:
  {"architectures_fired": [], "reason": "no_applicable_mechanism"}'

The tagger classifies which of the 8 humor architectures (if any) is present
in the generated content, then writes the tag to content_performance.

C-11 Persona Masking Gate: no agent names in model-facing prompts.
"""

import json
from datetime import datetime, timezone
from typing import Optional

from src.ccp.models.v5_models import HumorMechanismTag


# 8 Humor Architectures — per spec
HUMOR_ARCHITECTURES = [
    "benign_violation",         # Something is threatening + simultaneously safe
    "incongruity_resolution",   # Expectation violated then resolved
    "superiority_theory",       # Laughing at someone else's misfortune
    "relief_theory",            # Release of psychological tension
    "self_deprecation",         # Coach as the subject of the joke
    "absurdist_pivot",          # Logical chain breaks into absurd conclusion
    "insider_reference",        # Cultural in-group signal
    "observational",            # 'We all do this' audience mirror
]


_HUMOR_CLASSIFICATION_PROMPT = """You are a humor mechanism analyst specializing in professional coaching content.

Analyze the following piece of coaching content and identify which humor mechanisms are present.

CONTENT TO ANALYZE:
{content_text}

CONTENT TYPE: {content_type}

The 8 humor architectures to check for:
1. benign_violation — Something appears threatening but is simultaneously safe/acceptable
2. incongruity_resolution — A pattern is set up and then violated in a satisfying way
3. superiority_theory — Content positions audience above a shared failure/person
4. relief_theory — Tension is built and then released through humor
5. self_deprecation — The author or coach is the subject/target of the humor
6. absurdist_pivot — A logical premise is taken to an unexpected, absurd conclusion
7. insider_reference — A cultural or in-group reference that signals belonging
8. observational — 'We all do this' mirror that validates shared experience

Return ONLY valid JSON:
{{
  "architectures_fired": ["mechanism1", "mechanism2"],
  "reason": "brief explanation of why these mechanisms are or are not present",
  "confidence": 0.0
}}

Rules:
- architectures_fired: EMPTY ARRAY if no humor mechanism is present — do not force humor where there is none
- reason: 10-30 words explaining the classification
- confidence: 0.0–1.0 — how confident you are in this classification
- If no mechanism applies, return: {{"architectures_fired": [], "reason": "no_applicable_mechanism", "confidence": 1.0}}
- Return only the JSON object, no commentary
"""


class HumorMechanismTagger:
    """FR1 Step 11-D: Post-generation humor mechanism classification.

    AC8: Every generated script gets a humor_mechanism_tag JSONB.
    Empty tag format: {"architectures_fired": [], "reason": "no_applicable_mechanism"}

    The tagger:
    1. Receives generated content
    2. Classifies which humor architectures are present (if any)
    3. Returns a HumorMechanismTag for writing to content_performance

    The tag is NEVER omitted — even when no mechanism applies, the explicit
    no_applicable_mechanism record is written (AC8).
    """

    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
    ):
        import os
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for humor mechanism tagging")

    async def tag_content(
        self,
        content_text: str,
        content_type: str = "social_script",
    ) -> HumorMechanismTag:
        """Classify humor mechanisms in a piece of generated content.

        AC8: Returns a tag whether or not humor is present.
        Empty case: {"architectures_fired": [], "reason": "no_applicable_mechanism"}

        Args:
            content_text: The generated content to analyze.
            content_type: Type of content (social_script, email, caption, etc.)

        Returns:
            HumorMechanismTag — always populated, never None.
        """
        from google import genai

        prompt = _HUMOR_CLASSIFICATION_PROMPT.format(
            content_text=content_text[:2000],  # Cap to avoid token overflow
            content_type=content_type,
        )

        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        result = json.loads(response_text)

        # Filter to valid architectures only
        raw_fired = result.get("architectures_fired", [])
        valid_fired = [a for a in raw_fired if a in HUMOR_ARCHITECTURES]

        # AC8: HumorMechanismTag model_post_init enforces the empty-case reason
        tag = HumorMechanismTag(
            architectures_fired=valid_fired,
            reason=result.get("reason") if valid_fired else "no_applicable_mechanism",
            confidence=result.get("confidence", 0.0) if valid_fired else 1.0,
            classified_at=datetime.now(timezone.utc),
        )

        return tag

    async def tag_batch(
        self,
        contents: list[dict],
    ) -> list[tuple[str, HumorMechanismTag]]:
        """Tag a batch of generated content items.

        AC8: All content items receive a tag, even if the mechanism is empty.

        Args:
            contents: List of dicts with 'content_id', 'content_text',
                      and optionally 'content_type'.

        Returns:
            List of (content_id, HumorMechanismTag) tuples.
        """
        import asyncio

        async def tag_one(item: dict) -> tuple[str, HumorMechanismTag]:
            content_id = item["content_id"]
            content_text = item["content_text"]
            content_type = item.get("content_type", "social_script")
            tag = await self.tag_content(content_text, content_type)
            return content_id, tag

        results = await asyncio.gather(*[tag_one(c) for c in contents])
        return list(results)

    def build_supabase_update(
        self,
        content_id: str,
        tag: HumorMechanismTag,
    ) -> dict:
        """Build the Supabase update payload for content_performance.humor_mechanism_tag.

        Args:
            content_id: The content_performance.content_id to update.
            tag: The HumorMechanismTag to serialize as JSONB.

        Returns:
            Dict ready for Supabase .update() call.
        """
        return {
            "content_id": content_id,
            "humor_mechanism_tag": {
                "architectures_fired": tag.architectures_fired,
                "reason": tag.reason,
                "confidence": tag.confidence,
                "classified_at": tag.classified_at.isoformat() if tag.classified_at else None,
            },
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def tag_fallback(self) -> HumorMechanismTag:
        """Return the explicit no-mechanism tag for fallback/error cases.

        AC8: The empty tag is NEVER omitted — always written explicitly.
        This ensures every content_performance row has a humor_mechanism_tag
        value (not NULL), which enables consistent downstream analytics.
        """
        return HumorMechanismTag(
            architectures_fired=[],
            reason="no_applicable_mechanism",
            confidence=1.0,
            classified_at=datetime.now(timezone.utc),
        )
