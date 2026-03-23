"""
CCP Intuition Extension Models — FR40 (DEP-ENG-035)

Spec: FR40_Intuition_Extensions_Tech_Spec.md
Produces: DEP-ENG-035 (Intuition Extension Set)
  DEP-ENG-035_a — SoulResonance injection
  DEP-ENG-035_b — PatternWeaver injection
  DEP-ENG-035_c — GhostContext injection
  DEP-ENG-035_d — AncestralWisdom injection

§4 Stage 1: SoulResonance — vibe checker (emotional flatness / TVR imbalance)
§4 Stage 2: PatternWeaver — synthesizer (staleness / metaphor reuse ≥3)
§4 Stage 3: GhostContext — shadow miner (100% positive sentiment)
§4 Stage 4: AncestralWisdom — reframer (coach echo test failure)

§8: AC1 conditional firing, AC2 GhostContext dark truth, AC3 PatternWeaver
     farthest node, AC4 AncestralWisdom Flesch-Kincaid Grade 8-10.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════════════════════

METAPHOR_REUSE_THRESHOLD: int = 3
"""§4 Stage 2: PatternWeaver fires when metaphor reused ≥3 times in lookback."""

STALENESS_LOOKBACK_DAYS: int = 10
"""§8 AC1: 'metaphor used 3 times in the last 10 days.'"""

ANCESTRAL_WISDOM_READABILITY_MIN: int = 8
"""§8 AC4: Flesch-Kincaid Grade minimum (Grade 8)."""

ANCESTRAL_WISDOM_READABILITY_MAX: int = 10
"""§8 AC4: Flesch-Kincaid Grade maximum (Grade 10)."""

TVR_TRAILING_WINDOW_DAYS: int = 7
"""§4 Stage 1: T/V/R ratio balanced over 7-day trailing window."""


# ══════════════════════════════════════════════════════════════════════════════
# Enums
# ══════════════════════════════════════════════════════════════════════════════

class IntuitionExtensionName(str, Enum):
    """The 4 Intuition Extensions (FR40)."""

    SOUL_RESONANCE = "SoulResonance"
    PATTERN_WEAVER = "PatternWeaver"
    GHOST_CONTEXT = "GhostContext"
    ANCESTRAL_WISDOM = "AncestralWisdom"


class IntuitionAgentName(str, Enum):
    """Sub-agent personas for each Intuition Extension."""

    RESONANCE_SEEKER = "The Resonance Seeker"
    CONNECTOR = "The Connector"
    SHADOW_MINER = "The Shadow Miner"
    PHILOSOPHER = "The Philosopher"


class IntuitionTriggerCondition(str, Enum):
    """Governance Layer trigger conditions per extension."""

    # SoulResonance triggers
    EMOTIONAL_FLATNESS = "EMOTIONAL_FLATNESS"
    TVR_IMBALANCE = "TVR_IMBALANCE"

    # PatternWeaver triggers
    STALENESS_METAPHOR_REUSED = "STALENESS_DETECTED_METAPHOR_REUSED"
    STALENESS_STRUCTURAL = "STALENESS_STRUCTURAL_MONOTONY"

    # GhostContext triggers
    POSITIVE_ONLY_SENTIMENT = "POSITIVE_ONLY_SENTIMENT_NO_L3"

    # AncestralWisdom triggers
    COACH_ECHO_FAILURE = "COACH_ECHO_TEST_FAILURE"


class IntuitionBehaviorType(str, Enum):
    """Behavior injection categories per extension."""

    # SoulResonance (§4 Stage 1)
    VIBE_PASS_REWRITE = "VIBE_PASS_REWRITE"
    EMOTIONAL_POLARITY_INJECTION = "EMOTIONAL_POLARITY_INJECTION"
    TRIBE_MIRROR_CHECK = "TRIBE_MIRROR_CHECK"
    SACRED_MOMENT_SURFACING = "SACRED_MOMENT_SURFACING"

    # PatternWeaver (§4 Stage 2)
    CROSS_DOMAIN_SYNTHESIS = "CROSS_DOMAIN_SYNTHESIS"
    TEMPORAL_PATTERN_DETECTION = "TEMPORAL_PATTERN_DETECTION"
    CONTRADICTION_MINING = "CONTRADICTION_MINING"
    ADJACENT_INDUSTRY_TRANSPLANT = "ADJACENT_INDUSTRY_TRANSPLANT"

    # GhostContext (§4 Stage 3)
    INDUSTRY_DARK_TRUTH_INJECTION = "INDUSTRY_DARK_TRUTH_INJECTION"
    AUDIENCE_FEAR_MAPPING = "AUDIENCE_FEAR_MAPPING"
    HISTORICAL_FAILURE_PATTERN = "HISTORICAL_FAILURE_PATTERN"
    COUNTER_NARRATIVE_GENERATION = "COUNTER_NARRATIVE_GENERATION"

    # AncestralWisdom (§4 Stage 4)
    CMA_FRAMEWORK_REFRAMING = "CMA_FRAMEWORK_REFRAMING"
    FIRST_PRINCIPLES_DECOMPOSITION = "FIRST_PRINCIPLES_DECOMPOSITION"
    PHILOSOPHICAL_LENS_ROTATION = "PHILOSOPHICAL_LENS_ROTATION"
    LEGACY_PATTERN_RECOGNITION = "LEGACY_PATTERN_RECOGNITION"


class PhilosophicalLens(str, Enum):
    """§4 Stage 4: Available philosophical lenses for AncestralWisdom."""

    STOICISM = "Stoicism"
    BEHAVIORAL_ECONOMICS = "Behavioral Economics"
    EXISTENTIALISM = "Existentialism"
    SYSTEMS_THINKING = "Systems Thinking"
    GAME_THEORY = "Game Theory"
    NARRATIVE_PSYCHOLOGY = "Narrative Psychology"


# ══════════════════════════════════════════════════════════════════════════════
# Tool Result Models
# ══════════════════════════════════════════════════════════════════════════════

class SoulResonanceToolResult(BaseModel):
    """Result from tools/soul_resonance_query.py.

    §4 Stage 1 Tool: Neo4j semantic query for highly charged emotional nodes.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    emotional_nodes_found: list[str] = Field(
        default_factory=list,
        description="Highly charged emotional nodes from Sacred Audio DB.",
    )
    sacred_moment: Optional[str] = Field(
        default=None,
        description="A specific sigh, frustrated pause, etc. from voice archive.",
    )
    emotional_register_match: bool = Field(
        default=False,
        description="Does drafted emotional register match Real Time Tribe Relevance?",
    )
    polarity_imbalance: Optional[str] = Field(
        default=None,
        description="E.g., 'Purely Analytical — inject Dark Humor or Vulnerability'.",
    )


class GraphDisconnectToolResult(BaseModel):
    """Result from tools/graph_disconnect_query.py.

    §4 Stage 2 Tool: Shortest-path algorithm between unrelated nodes.
    §8 AC3: Returns conceptually farthest node in coach's graph.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    source_topic: str = Field(..., description="The current primary topic.")
    farthest_node: str = Field(
        ...,
        description="§8 AC3: Conceptually foreign but present in coach's life.",
    )
    topological_distance: int = Field(
        default=0,
        description="Number of edges in shortest path (higher = more foreign).",
    )
    shared_edge_count: int = Field(
        default=0,
        description="Edges shared between source and farthest (lower = better).",
    )
    synthesis_directive: str = Field(
        default="",
        description="The forced cross-domain synthesis directive.",
    )


class GhostContextToolResult(BaseModel):
    """Result from tools/ghost_context_scan.py.

    §4 Stage 3 Tool: Scans historical outputs and audience vibes for blind spots.
    §8 AC2: Must contain directive addressing 'industry dark truth'.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    dark_truth_directive: str = Field(
        default="",
        description=(
            "§8 AC2: Must address 'industry dark truth'. "
            "E.g., 'Address the reality that morning routines are a luxury "
            "of those without caregiving responsibilities.'"
        ),
    )
    audience_fear: Optional[str] = Field(
        default=None,
        description="The objection the audience has but won't say out loud (L3 fear).",
    )
    historical_failure: Optional[str] = Field(
        default=None,
        description="Past failed coaching strategy as cautionary context.",
    )
    counter_narrative: Optional[str] = Field(
        default=None,
        description="Mainstream consensus to disprove using coach's data.",
    )
    blind_spots_found: list[str] = Field(
        default_factory=list,
        description="Unresolved blind spots surfaced from historical analysis.",
    )


class FrameworkCrossReferenceToolResult(BaseModel):
    """Result from tools/framework_cross_reference.py.

    §4 Stage 4 Tool: Maps coach statements against CMA principles,
    philosophical lexicons.
    §8 AC4: Output must remain Flesch-Kincaid Grade 8-10.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    matched_principle: Optional[str] = Field(
        default=None,
        description="CMA principle matched (1 of 14).",
    )
    philosophical_lens: Optional[PhilosophicalLens] = Field(
        default=None,
        description="Selected philosophical lens for reframing.",
    )
    reframing_directive: str = Field(
        default="",
        description="The specific reframing instruction.",
    )
    legacy_pattern: Optional[str] = Field(
        default=None,
        description="Timeless wisdom link (e.g., 'What you describe is what Nash called...').",
    )
    flesch_kincaid_grade: Optional[float] = Field(
        default=None,
        description="§8 AC4: Must be Grade 8-10.",
    )
    readability_compliant: bool = Field(default=True)

    def model_post_init(self, __context: Any) -> None:
        if self.flesch_kincaid_grade is not None:
            self.readability_compliant = (
                ANCESTRAL_WISDOM_READABILITY_MIN
                <= self.flesch_kincaid_grade
                <= ANCESTRAL_WISDOM_READABILITY_MAX
            )


# ══════════════════════════════════════════════════════════════════════════════
# Injection Payload (DEP-ENG-035)
# ══════════════════════════════════════════════════════════════════════════════

class IntuitionInjectionPayload(BaseModel):
    """Primary Output Schema (DEP-ENG-035) — intuition_injection_payload.json.

    §5: The payload that mutates the Executive Prompt.
    """

    intuition_run_id: str = Field(
        ..., description="Unique run ID. Format: INT-{NNNN}."
    )
    triggering_condition: str = Field(
        ..., description="Which Governance Layer condition fired."
    )
    extension_fired: str = Field(
        ..., description="Which of the 4 intuition extensions ran."
    )
    sub_agent_deployed: str = Field(
        ..., description="The agent persona name deployed."
    )
    tool_invoked: str = Field(
        ..., description="Python tool script name invoked."
    )
    injection_payload: dict[str, str] = Field(
        default_factory=dict,
        description="The directive and constraint added to the executive prompt.",
    )
    executive_prompt_mutated: bool = Field(
        default=True,
        description="Whether the executive prompt was mutated.",
    )
    coach_id: str = Field(
        default="", description="ADR-01: Coach scope."
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


# ══════════════════════════════════════════════════════════════════════════════
# Governance Layer Trigger Evaluation
# ══════════════════════════════════════════════════════════════════════════════

class MetaphorUsageEntry(BaseModel):
    """Tracks a metaphor usage for PatternWeaver staleness detection."""

    metaphor: str
    used_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    script_id: str = Field(default="")


class TVRBalance(BaseModel):
    """Teach/Vulnerability/Reaction ratio for SoulResonance trigger.

    §4 Stage 1: Boredom Ban detects TVR imbalance over 7-day window.
    """

    teach_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    vulnerability_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    reaction_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    is_balanced: bool = Field(default=True)
    imbalance_type: Optional[str] = Field(default=None)

    def model_post_init(self, __context: Any) -> None:
        total = self.teach_ratio + self.vulnerability_ratio + self.reaction_ratio
        if total > 0:
            # Imbalanced if any dimension is <15% or >60%
            ratios = {
                "Teach": self.teach_ratio / total,
                "Vulnerability": self.vulnerability_ratio / total,
                "Reaction": self.reaction_ratio / total,
            }
            for name, ratio in ratios.items():
                if ratio < 0.15 or ratio > 0.60:
                    self.is_balanced = False
                    self.imbalance_type = f"{name} at {ratio:.0%} — outside 15-60% band"
                    break


class GovernanceTriggerEvaluation(BaseModel):
    """Result of Governance Layer evaluating whether an intuition extension should fire.

    §8 AC1: 5 unique scripts → NO fire. Stale metaphor 3+ → PatternWeaver fires.
    """

    coach_id: str = Field(..., min_length=3, max_length=3)
    should_fire: bool = Field(default=False)
    target_extension: Optional[IntuitionExtensionName] = Field(default=None)
    trigger_condition: Optional[IntuitionTriggerCondition] = Field(default=None)
    evidence: str = Field(default="")

    # Detection inputs
    metaphor_reuse_count: int = Field(default=0)
    sentiment_positive_ratio: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Ratio of positive/aspirational sentiment in draft.",
    )
    tvr_balance: Optional[TVRBalance] = Field(default=None)
    coach_echo_detected: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        # PatternWeaver: metaphor reused ≥3 times
        if self.metaphor_reuse_count >= METAPHOR_REUSE_THRESHOLD:
            self.should_fire = True
            self.target_extension = IntuitionExtensionName.PATTERN_WEAVER
            self.trigger_condition = IntuitionTriggerCondition.STALENESS_METAPHOR_REUSED
            self.evidence = (
                f"Metaphor reused {self.metaphor_reuse_count} times "
                f"(threshold: {METAPHOR_REUSE_THRESHOLD})"
            )
            return

        # GhostContext: 100% positive without L3
        if self.sentiment_positive_ratio >= 1.0:
            self.should_fire = True
            self.target_extension = IntuitionExtensionName.GHOST_CONTEXT
            self.trigger_condition = IntuitionTriggerCondition.POSITIVE_ONLY_SENTIMENT
            self.evidence = "100% positive/aspirational sentiment without L3 limitations"
            return

        # SoulResonance: TVR imbalance
        if self.tvr_balance and not self.tvr_balance.is_balanced:
            self.should_fire = True
            self.target_extension = IntuitionExtensionName.SOUL_RESONANCE
            self.trigger_condition = IntuitionTriggerCondition.TVR_IMBALANCE
            self.evidence = f"TVR imbalance: {self.tvr_balance.imbalance_type}"
            return

        # AncestralWisdom: coach echo
        if self.coach_echo_detected:
            self.should_fire = True
            self.target_extension = IntuitionExtensionName.ANCESTRAL_WISDOM
            self.trigger_condition = IntuitionTriggerCondition.COACH_ECHO_FAILURE
            self.evidence = "Coach Echo Test failed — parroting without structural value"
            return

        # No trigger — all clear
        self.should_fire = False


# ══════════════════════════════════════════════════════════════════════════════
# Extension-to-Agent-Tool Mapping
# ══════════════════════════════════════════════════════════════════════════════

EXTENSION_AGENT_MAP: dict[IntuitionExtensionName, IntuitionAgentName] = {
    IntuitionExtensionName.SOUL_RESONANCE: IntuitionAgentName.RESONANCE_SEEKER,
    IntuitionExtensionName.PATTERN_WEAVER: IntuitionAgentName.CONNECTOR,
    IntuitionExtensionName.GHOST_CONTEXT: IntuitionAgentName.SHADOW_MINER,
    IntuitionExtensionName.ANCESTRAL_WISDOM: IntuitionAgentName.PHILOSOPHER,
}

EXTENSION_TOOL_MAP: dict[IntuitionExtensionName, str] = {
    IntuitionExtensionName.SOUL_RESONANCE: "soul_resonance_query.py",
    IntuitionExtensionName.PATTERN_WEAVER: "graph_disconnect_query.py",
    IntuitionExtensionName.GHOST_CONTEXT: "ghost_context_scan.py",
    IntuitionExtensionName.ANCESTRAL_WISDOM: "framework_cross_reference.py",
}
