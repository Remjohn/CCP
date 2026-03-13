"""
Assembler — Ritual Selection & Strategy Agent (v2.0)
=====================================================
Rewired to load system prompt from assembler_SKILL.md via skill_loader.

Architecture:
    assembler_SKILL.md (220 lines of MCDA scoring rules)
         ↓
    skill_loader.load_skill("assembler") → system_prompt
         ↓
    Multi-criteria scoring + Pydantic AI Agent for edge cases
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
import logging

from backend.core.skill_loader import skill_loader

logger = logging.getLogger(__name__)


# ── Models (v2 — matching SKILL.md output spec) ──

class Ritual(BaseModel):
    id: str
    name: str
    description: str
    level_threshold: int
    identity_fit: List[str]
    goal_fit: str
    media_url: str
    script_template: str


class UserProfile(BaseModel):
    id: str
    capacity_score: int = Field(..., ge=0, le=100)
    identity_pillar: Literal['Challenger', 'Nurturer', 'Maker', 'Explorer', 'Rebel']


class ContextPremise(BaseModel):
    primary_pain: str
    ttt_code: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None


class ScoringBreakdown(BaseModel):
    """Transparent MCDA scoring breakdown."""
    capacity: float = Field(..., ge=0, le=10)
    identity: float = Field(..., ge=0, le=10)
    goal: float = Field(..., ge=0, le=10)
    timing: float = Field(5.0, ge=0, le=10)
    freshness: float = Field(5.0, ge=0, le=10)
    total: float = Field(..., ge=0, le=10)


class SelectionReasoning(BaseModel):
    """Why this ritual was selected."""
    candidates_evaluated: int
    candidates_after_filter: int
    scoring_breakdown: ScoringBreakdown
    confidence: Literal['HIGH', 'MEDIUM', 'LOW']
    alternative_ritual: Optional[str] = None
    fallback_level: int = Field(0, description="0=normal, 1/2/3=fallback levels")


class PersuasionLayer(BaseModel):
    """Selected persuasion strategy."""
    id: int = Field(..., ge=1, le=9)
    name: str
    rationale: str


class AssemblyInstructions(BaseModel):
    """Instructions for the Artisan."""
    identity_layer: str
    ttt_state: str
    tone_preset: str
    metaphor_family: str
    sentiment_injection: bool = False
    fact_injection: bool = False
    max_duration_seconds: int = 90
    banned_phrases: List[str] = Field(default_factory=list)
    required_elements: List[str] = Field(default_factory=list)


class RitualSelection(BaseModel):
    """Full Assembler output."""
    reasoning: SelectionReasoning
    selected_ritual: Dict[str, Any]
    persuasion_layer: PersuasionLayer
    assembly_instructions: AssemblyInstructions


# ── Identity Alignment Matrix ──

IDENTITY_BEST_FIT = {
    "Challenger": {"Competition", "Accountability", "Metrics", "Sprint"},
    "Nurturer": {"Community", "Journaling", "Gratitude", "Reflection"},
    "Maker": {"Building", "Systems", "Tracking", "Design"},
    "Explorer": {"Experience", "Variety", "Movement", "Discovery"},
    "Rebel": {"Reframe", "Contrarian", "Challenge", "Breaking"},
}

IDENTITY_WORST_FIT = {
    "Challenger": {"Meditation", "Passive", "Gentle"},
    "Nurturer": {"Confrontation", "Isolation", "Harsh"},
    "Maker": {"Unstructured", "Free-Flow", "Random"},
    "Explorer": {"Rigid", "Repetition", "Same-Place"},
    "Rebel": {"Authority", "Compliance", "Rules"},
}


# ── TTT → Persuasion Layer Mapping ──

TTT_PERSUASION_MAP = {
    "TTT-01": (1, "Gentle Nudge"),
    "TTT-02": (1, "Gentle Nudge"),
    "TTT-03": (2, "Storytelling Bridge"),
    "TTT-04": (4, "Strategic Challenge"),
    "TTT-05": (4, "Strategic Challenge"),
    "TTT-06": (5, "Social Proof"),
    "TTT-07": (6, "Competitive Edge"),
    "TTT-08": (6, "Competitive Edge"),
    "TTT-09": (3, "Grounding"),
    "TTT-10": (3, "Grounding"),
}


# ── Metaphor Families ──

IDENTITY_METAPHORS = {
    "Challenger": "Battle / Competition / Arena",
    "Nurturer": "Garden / Nurturing / Growth",
    "Maker": "Engineering / Construction / Blueprint",
    "Explorer": "Journey / Discovery / Map",
    "Rebel": "Revolution / Breaking Chains / Wildfire",
}


# ── Assembler Service ──

class AssemblerService:
    """
    MCDA-inspired ritual selection with SKILL.md-grade scoring.

    Weights: Capacity 30%, Identity 25%, Goal 20%, Timing 15%, Freshness 10%
    """

    def __init__(self):
        self._skill = skill_loader.load_skill("assembler")
        if self._skill:
            logger.info(f"[Assembler] Loaded SKILL.md v{self._skill.version}")
        else:
            logger.warning("[Assembler] SKILL.md not found, using built-in rules")

        self._recent_rituals: Dict[str, List[str]] = {}  # user_id → [ritual_ids]

    def select_ritual(
        self,
        user: UserProfile,
        context: ContextPremise,
        available_rituals: List[Ritual],
        recent_ritual_ids: Optional[List[str]] = None,
    ) -> RitualSelection:
        """
        Select the optimal ritual using multi-criteria weighted analysis.
        """
        recent = recent_ritual_ids or []

        # ── Step 1: Capacity Filter ──
        candidates = [
            r for r in available_rituals
            if user.capacity_score >= r.level_threshold
        ]

        # Special case: severely depleted
        if user.capacity_score <= 20:
            candidates = [
                r for r in candidates
                if any(kw in r.name.lower() for kw in ["micro", "rest", "breathe", "gentle"])
            ]
            if not candidates:
                candidates = [r for r in available_rituals if r.level_threshold <= 20]

        total_evaluated = len(available_rituals)
        total_after_filter = len(candidates)

        if not candidates:
            return self._fallback_selection(user, context, available_rituals, 3)

        # ── Step 2: Score each candidate ──
        scored = []
        for ritual in candidates:
            cap_score = self._capacity_score(user.capacity_score, ritual.level_threshold)
            id_score = self._identity_score(user.identity_pillar, ritual)
            goal_score = self._goal_score(context.primary_pain, ritual.goal_fit)
            time_score = self._timing_score(ritual.id, recent)
            fresh_score = self._freshness_score(ritual.id, recent)

            total = (
                0.30 * cap_score +
                0.25 * id_score +
                0.20 * goal_score +
                0.15 * time_score +
                0.10 * fresh_score
            )

            scored.append((total, ritual, ScoringBreakdown(
                capacity=cap_score,
                identity=id_score,
                goal=goal_score,
                timing=time_score,
                freshness=fresh_score,
                total=round(total, 2),
            )))

        # ── Step 3: Rank and select ──
        scored.sort(key=lambda x: x[0], reverse=True)

        best_total, best_ritual, best_breakdown = scored[0]

        # Minimum threshold check
        if best_total < 4.0:
            return self._fallback_selection(user, context, available_rituals, 1)

        # Freshness gate: no repeat within 7 days
        if best_ritual.id in recent[:5]:
            if len(scored) > 1:
                best_total, best_ritual, best_breakdown = scored[1]
            else:
                return self._fallback_selection(user, context, available_rituals, 2)

        # ── Step 4: Select persuasion layer ──
        ttt_code = context.ttt_code or "TTT-05"
        layer_id, layer_name = TTT_PERSUASION_MAP.get(ttt_code, (4, "Strategic Challenge"))

        # ── Step 5: Build assembly instructions ──
        pillar = user.identity_pillar

        confidence = "HIGH" if best_total >= 7.0 else ("MEDIUM" if best_total >= 5.0 else "LOW")
        alternative = f"{scored[1][1].name} (score: {scored[1][0]:.2f})" if len(scored) > 1 else None

        return RitualSelection(
            reasoning=SelectionReasoning(
                candidates_evaluated=total_evaluated,
                candidates_after_filter=total_after_filter,
                scoring_breakdown=best_breakdown,
                confidence=confidence,
                alternative_ritual=alternative,
            ),
            selected_ritual={
                "id": best_ritual.id,
                "name": best_ritual.name,
                "description": best_ritual.description,
                "level_threshold": best_ritual.level_threshold,
                "script_template": best_ritual.script_template,
            },
            persuasion_layer=PersuasionLayer(
                id=layer_id,
                name=layer_name,
                rationale=f"User TTT state is {ttt_code}, mapped to {layer_name}",
            ),
            assembly_instructions=AssemblyInstructions(
                identity_layer=pillar,
                ttt_state=ttt_code,
                tone_preset=self._get_tone_preset(pillar, ttt_code),
                metaphor_family=IDENTITY_METAPHORS.get(pillar, "General"),
                banned_phrases=self._get_banned_phrases(pillar),
                required_elements=self._get_required_elements(pillar),
            ),
        )

    # ── Scoring Functions ──

    def _capacity_score(self, user_cap: int, threshold: int) -> float:
        gap = user_cap - threshold
        if gap >= 30:
            return 10.0
        elif gap >= 10:
            return 8.0
        elif gap >= 0:
            return 5.0
        return 0.0  # Should never reach here (filtered)

    def _identity_score(self, pillar: str, ritual: Ritual) -> float:
        best = IDENTITY_BEST_FIT.get(pillar, set())
        worst = IDENTITY_WORST_FIT.get(pillar, set())

        ritual_tags = set(ritual.identity_fit)

        if ritual_tags & best:
            return 10.0
        elif ritual_tags & worst:
            return 2.0
        elif pillar in ritual.identity_fit:
            return 10.0
        else:
            return 5.0  # Neutral

    def _goal_score(self, primary_pain: str, goal_fit: str) -> float:
        if not primary_pain or not goal_fit:
            return 5.0
        if primary_pain.lower() == goal_fit.lower():
            return 10.0
        # Partial match
        pain_words = set(primary_pain.lower().split())
        goal_words = set(goal_fit.lower().split())
        overlap = len(pain_words & goal_words)
        if overlap > 0:
            return 7.0
        return 3.0

    def _timing_score(self, ritual_id: str, recent: List[str]) -> float:
        if ritual_id not in recent:
            return 10.0
        pos = recent.index(ritual_id)
        return max(2.0, 10.0 - pos * 2)

    def _freshness_score(self, ritual_id: str, recent: List[str]) -> float:
        if ritual_id not in recent:
            return 10.0
        return 3.0

    # ── Preset Helpers ──

    def _get_tone_preset(self, pillar: str, ttt_code: str) -> str:
        presets = {
            "Challenger": "Direct, punchy, short sentences, competitive framing",
            "Nurturer": "Warm, empathetic, flowing sentences, supportive framing",
            "Maker": "Precise, structured, logical flow, systems framing",
            "Explorer": "Curious, energetic, varied rhythm, discovery framing",
            "Rebel": "Raw, provocative, unexpected turns, contrarian framing",
        }
        return presets.get(pillar, "Balanced, natural, conversational")

    def _get_banned_phrases(self, pillar: str) -> List[str]:
        base = ["believe in yourself", "manifest your dreams", "you've got this"]
        per_pillar = {
            "Challenger": ["take it easy", "no pressure", "whenever you feel like it"],
            "Nurturer": ["suck it up", "stop whining", "be a man"],
            "Maker": ["just go with the flow", "stop overthinking", "wing it"],
            "Explorer": ["stay where you are", "stick to the plan", "don't experiment"],
            "Rebel": ["follow the rules", "do as you're told", "fall in line"],
        }
        return base + per_pillar.get(pillar, [])

    def _get_required_elements(self, pillar: str) -> List[str]:
        elements = {
            "Challenger": ["metric", "deadline", "accountability signal"],
            "Nurturer": ["encouragement", "self-compassion", "community reference"],
            "Maker": ["specific steps", "tracking method", "system reference"],
            "Explorer": ["novelty element", "discovery frame", "open-ended question"],
            "Rebel": ["pattern break", "contrarian insight", "freedom reference"],
        }
        return elements.get(pillar, ["action step", "timeline"])

    def _fallback_selection(
        self, user: UserProfile, context: ContextPremise,
        rituals: List[Ritual], level: int
    ) -> RitualSelection:
        """Generate a fallback ritual selection."""
        ttt_code = context.ttt_code or "TTT-05"
        layer_id, layer_name = TTT_PERSUASION_MAP.get(ttt_code, (4, "Strategic Challenge"))

        if level <= 2:
            # Try to find a generic ritual
            micro = next(
                (r for r in rituals if "micro" in r.name.lower() or r.level_threshold <= 10),
                rituals[0] if rituals else None,
            )
        else:
            micro = None

        ritual_dict = {
            "id": micro.id if micro else "rest_day",
            "name": micro.name if micro else "Rest & Recovery",
            "description": micro.description if micro else "Take today to rest. You've earned it.",
            "level_threshold": 0,
            "script_template": micro.script_template if micro else "Today is a rest day. No ritual needed.",
        }

        return RitualSelection(
            reasoning=SelectionReasoning(
                candidates_evaluated=len(rituals),
                candidates_after_filter=0,
                scoring_breakdown=ScoringBreakdown(
                    capacity=0, identity=0, goal=0, timing=0, freshness=0, total=0
                ),
                confidence="LOW",
                fallback_level=level,
            ),
            selected_ritual=ritual_dict,
            persuasion_layer=PersuasionLayer(
                id=layer_id, name=layer_name,
                rationale=f"Fallback level {level}: using gentle approach",
            ),
            assembly_instructions=AssemblyInstructions(
                identity_layer=user.identity_pillar,
                ttt_state=ttt_code,
                tone_preset="Gentle, supportive, minimal pressure",
                metaphor_family="General",
            ),
        )

    async def synthesize_script(
        self,
        ritual: Dict[str, Any],
        user_profile: Dict[str, Any],
        identity_layer: Optional[str] = None,
        ttt_code: Optional[str] = None,
        sentiment_report: Optional[str] = None,
        fact_bank: Optional[str] = None,
    ) -> str:
        """
        Uses the Artisan agent to generate a personalized script.
        """
        from backend.core.artisan import artisan, ScriptRequest

        request = ScriptRequest(
            ritual_name=ritual["name"],
            ritual_description=ritual["description"],
            user_name=user_profile.get("name", "User"),
            user_context=f"Capacity: {user_profile.get('capacity_score')}, Identity: {user_profile.get('identity_pillar')}",
            identity_layer=identity_layer,
            ttt_code=ttt_code,
            sentiment_report=sentiment_report,
            fact_bank=fact_bank,
        )

        logger.info(f"Synthesizing script for ritual {ritual['name']}...")
        try:
            result = await artisan.run(str(request.model_dump()))
            return result.data.full_script
        except Exception as e:
            logger.error(f"Script synthesis failed: {e}")
            return ritual.get("script_template", "Take a moment to breathe.")


# Global Instance
assembler = AssemblerService()
