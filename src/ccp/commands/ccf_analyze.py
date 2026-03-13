"""
CCP Content Analyze Command (ccf-analyze)
Task 2.02 — Generates ideas.json with 36 content ideas across 14 formats.

Takes coach soul + topic queue + research context and produces
a batch plan: which topics, which formats, which leadership traits
to target, and which constraints to apply (Boredom Ban avoidance).
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.asset_id import AssetIDGenerator, AssetType
from src.ccp.core.boredom_ban import BoredomBan
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.coach_soul import CoachSoul


class ContentIdea(BaseModel):
    """A single content idea in the batch plan."""

    idea_id: int
    asset_id: str
    format_type: str = Field(description="Content format code")
    format_label: str = Field(description="Human-readable format name")
    topic: str = Field(description="Topic or subject matter")
    angle: str = Field(description="Specific angle or argument")
    hook_suggestion: str = Field(description="Opening hook concept")
    target_trait: str = Field(description="Leadership trait this piece exercises or showcases")
    trait_mode: str = Field(description="'exercise' (weak trait) or 'showcase' (strong trait)")
    avoidance_constraints: list[str] = Field(
        default_factory=list, description="Boredom Ban constraints"
    )
    research_context: str = Field(default="", description="Relevant research snippet")
    suggested_metaphors: list[str] = Field(default_factory=list)
    priority: str = Field(default="normal", description="high, normal, low")


class IdeasBatch(BaseModel):
    """The full batch of 36 content ideas."""

    asset_id: str
    coach_acronym: str
    batch_date: datetime
    ideas: list[ContentIdea]
    total_count: int
    format_distribution: dict[str, int]


# Format registry with codes and target counts per batch
FORMAT_REGISTRY = {
    "THRD": {"label": "Thread", "count": 4},
    "CRSL": {"label": "Carousel", "count": 5},
    "REEL": {"label": "Reel Script", "count": 4},
    "QUOT": {"label": "Quote Card", "count": 4},
    "MEME": {"label": "Meme", "count": 2},
    "STRY": {"label": "Story", "count": 3},
    "POLL": {"label": "Poll", "count": 2},
    "ARTC": {"label": "Article", "count": 2},
    "SCRP": {"label": "Case Study", "count": 2},
    "SCRP": {"label": "Tips List", "count": 2},
    "SCRP": {"label": "Tweet Storm", "count": 2},
    "VIMG": {"label": "Visual Explainer", "count": 2},
    "REXP": {"label": "Reaction Explainer", "count": 1},
    "SCRP": {"label": "General Script", "count": 1},
}


IDEA_GENERATION_PROMPT = """You are the CCF Content Strategist for coach {coach_name} ({acronym}).

COACH IDENTITY:
- Philosophy: {philosophy}
- Core message: {core_message}
- Tribe: {tribe}
- Content tone: warmth={warmth}, directness={directness}, humor={humor}

LEADERSHIP TRAIT GUIDANCE:
- Exercise targets (weak, need practice): {weak_traits}
- Showcase targets (strong, amplify): {strong_traits}

TOPIC SUGGESTIONS FROM COACH:
{topic_suggestions}

BOREDOM BAN — MUST AVOID:
{avoidance}

Generate exactly {count} content ideas as a JSON array. Each idea needs:
{{
  "topic": "specific topic",
  "angle": "unique angle or argument",
  "hook_suggestion": "first line concept that grabs attention",
  "format": "one of: {format_list}",
  "target_trait": "which leadership trait this develops",
  "trait_mode": "exercise or showcase",
  "suggested_metaphors": ["1-2 metaphor suggestions"],
  "priority": "high/normal/low"
}}

Rules:
1. Each idea must have a UNIQUE angle — no two ideas should argue the same point.
2. Distribute formats according to this target: {format_distribution}
3. Weak traits get exercise formats (challenges, reflection prompts, how-tos).
4. Strong traits get showcase formats (authority pieces, stories, opinions).
5. Include 2-3 humor pieces (memes, tweets, or humor-angle scripts).
6. NEVER suggest a topic/angle/metaphor in the avoidance list.
7. Return ONLY the JSON array, no markdown.
"""


class CCFAnalyzer:
    """Generates the weekly content idea batch."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.asset_gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        self.boredom_ban = BoredomBan(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def analyze(
        self,
        soul: CoachSoul,
        topic_suggestions: Optional[list[str]] = None,
        target_count: int = 36,
    ) -> IdeasBatch:
        """Generate the weekly content idea batch.

        Args:
            soul: The coach's soul profile
            topic_suggestions: Optional list of coach-suggested topics
            target_count: Number of ideas to generate (default: 36)

        Returns:
            IdeasBatch with all content ideas
        """
        from google import genai

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Get Boredom Ban avoidance constraints
        window_summary = self.boredom_ban.get_window_summary()
        avoidance = "\n".join([
            f"- Theme already used: {t}" for t in window_summary.get("unique_themes", [])
        ]) or "No prior content in window."

        # Build format distribution string
        format_dist = {v["label"]: v["count"] for v in FORMAT_REGISTRY.values()}

        prompt = IDEA_GENERATION_PROMPT.format(
            coach_name=soul.coach_name,
            acronym=self.coach_acronym,
            philosophy=soul.coaching_philosophy,
            core_message=soul.core_message,
            tribe=soul.tribe_archetype,
            warmth=soul.content_tone.warmth,
            directness=soul.content_tone.directness,
            humor=soul.content_tone.humor_weight,
            weak_traits=", ".join(
                t.replace("_", " ").title()
                for t in soul.leadership_scores.get_weak_traits()
            ) or "None identified",
            strong_traits=", ".join(
                t.replace("_", " ").title()
                for t in soul.leadership_scores.get_strong_traits()
            ) or "None identified",
            topic_suggestions="\n".join(
                f"- {t}" for t in (topic_suggestions or [])
            ) or "No specific suggestions this week.",
            avoidance=avoidance,
            count=target_count,
            format_list=", ".join(FORMAT_REGISTRY.keys()),
            format_distribution=json.dumps(format_dist),
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        # Parse response
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        raw_ideas = json.loads(text)

        # Build ContentIdea objects with Asset IDs
        batch_asset_id = self.asset_gen.generate(AssetType.IDEAS_JSON)
        ideas = []
        format_count: dict[str, int] = {}

        for i, raw in enumerate(raw_ideas[:target_count]):
            fmt = raw.get("format", "SCRP")
            format_count[fmt] = format_count.get(fmt, 0) + 1

            # Run Boredom Ban check per idea
            ban_result = self.boredom_ban.check(
                proposed_theme=raw.get("topic", ""),
                proposed_angle=raw.get("angle", ""),
                proposed_metaphors=raw.get("suggested_metaphors", []),
                proposed_format=fmt,
                proposed_keywords=[],
                proposed_hook=raw.get("hook_suggestion", ""),
            )

            idea = ContentIdea(
                idea_id=i + 1,
                asset_id=self.asset_gen.generate(AssetType.SCRIPT),
                format_type=fmt,
                format_label=FORMAT_REGISTRY.get(fmt, {}).get("label", fmt),
                topic=raw.get("topic", ""),
                angle=raw.get("angle", ""),
                hook_suggestion=raw.get("hook_suggestion", ""),
                target_trait=raw.get("target_trait", ""),
                trait_mode=raw.get("trait_mode", "exercise"),
                avoidance_constraints=ban_result.avoidance_instructions,
                suggested_metaphors=raw.get("suggested_metaphors", []),
                priority=raw.get("priority", "normal"),
            )
            ideas.append(idea)

        batch = IdeasBatch(
            asset_id=batch_asset_id,
            coach_acronym=self.coach_acronym,
            batch_date=datetime.now(timezone.utc),
            ideas=ideas,
            total_count=len(ideas),
            format_distribution=format_count,
        )

        # Save ideas.json
        output_dir = Path(f"coaches/{self.coach_acronym}/production/scripts")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"ideas_{datetime.now().strftime('%Y%m%d')}.json"
        output_file.write_text(batch.model_dump_json(indent=2), encoding="utf-8")

        # Log
        self.receipt_chain.log(
            agent_id="ccf_analyzer",
            action="generate_ideas_batch",
            asset_id=batch_asset_id,
            input_summary=f"Soul: {soul.coach_name}, {len(topic_suggestions or [])} suggestions",
            output_summary=f"{len(ideas)} ideas across {len(format_count)} formats",
            decision="completed",
            metadata={"format_distribution": format_count, "ban_conflicts": sum(1 for i in ideas if i.avoidance_constraints)},
        )

        return batch
