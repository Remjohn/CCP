"""
CCP Pi Extension Models — FR39 Core Orchestration (DEP-ENG-034)

Spec: FR39_Core_Orchestration_11_Pi_Extensions.md
Produces: DEP-ENG-034 (Pi Extension Suite)

§4 Phase 1: 7 Operational Extensions
  1. InteractComp  — Ambiguity Gate (FAIL_AMBIGUITY on missing DEP-ID)
  2. MemoryFolder   — Graph Writer / Context Clearer (>4000 tokens → fold)
  3. DamageControl  — Self-Healing Loop (3 retries, error trace feedback)
  4. ModelRouter    — LLM Hot-Swap (Strategy→gpt-4o, Drafting→gpt-4o-mini)
  5. TillDone       — Assurance Engine (schema validation loop)
  6. TeamOrchestrator — Parallel Manager (3 temp-varied agents)
  7. SystemSelect   — Persona Swapper (/system @[Persona] command)

§5: Primary Output Schema — pi_extension_execution_log.json
§6: Backward Compatibility Fallback → Waterfall Mode
§8: AC1 InteractComp, AC2 TillDone, AC3 SystemSelect, AC4 DamageControl
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════════════════════

MEMORY_FOLDER_TOKEN_THRESHOLD: int = 4000
"""§4.2: If context > 4000 tokens OR task is complete, trigger fold."""

DAMAGE_CONTROL_MAX_RETRIES: int = 3
"""§4.3: Limits to 3 retries."""

TILL_DONE_MAX_ITERATIONS: int = 3
"""§4.5 + FR24: Max iterations before INCOMPLETE → fail."""

TEAM_ORCHESTRATOR_PARALLEL_COUNT: int = 3
"""§4.6: Spawns 3 identical agents with different temperature variables."""


# ══════════════════════════════════════════════════════════════════════════════
# Enums
# ══════════════════════════════════════════════════════════════════════════════

class ExtensionName(str, Enum):
    """The 11 Pi Extensions — 7 Operational + 4 Intuition (FR40)."""

    # Operational (FR39)
    INTERACT_COMP = "InteractComp"
    MEMORY_FOLDER = "MemoryFolder"
    DAMAGE_CONTROL = "DamageControl"
    MODEL_ROUTER = "ModelRouter"
    TILL_DONE = "TillDone"
    TEAM_ORCHESTRATOR = "TeamOrchestrator"
    SYSTEM_SELECT = "SystemSelect"

    # Intuition (FR40) — defined here for registry completeness
    SOUL_RESONANCE = "SoulResonance"
    PATTERN_WEAVER = "PatternWeaver"
    GHOST_CONTEXT = "GhostContext"
    ANCESTRAL_WISDOM = "AncestralWisdom"


class ExtensionResult(str, Enum):
    """Possible outcomes of an extension invocation."""

    SUCCESS = "SUCCESS"
    FAIL_AMBIGUITY = "FAIL_AMBIGUITY"
    INCOMPLETE = "INCOMPLETE"
    RETRY = "RETRY"
    PASS = "PASS"
    FAIL = "FAIL"
    BYPASSED = "BYPASSED"
    WATERFALL_MODE = "WATERFALL_MODE"


class TaskType(str, Enum):
    """ModelRouter task classification for LLM routing."""

    STRATEGY = "STRATEGY"
    REASONING = "REASONING"
    DRAFTING = "DRAFTING"
    FORMATTING = "FORMATTING"
    CREATIVE = "CREATIVE"
    ANALYSIS = "ANALYSIS"


class ModelTier(str, Enum):
    """LLM model tier for ModelRouter dispatch."""

    ULTRA_HIGH = "ultra_high"    # gpt-4o / Claude Opus equivalent
    FAST_CHEAP = "fast_cheap"    # gpt-4o-mini / Claude Haiku equivalent
    REASONING = "reasoning"      # o1 / o3 equivalent


# ══════════════════════════════════════════════════════════════════════════════
# Extension Invocation Record
# ══════════════════════════════════════════════════════════════════════════════

class ExtensionFired(BaseModel):
    """A single extension invocation within an execution cycle.

    §5: Matches the pi_extension_execution_log.json 'extensions_fired' schema.
    """

    extension_name: str = Field(
        ..., description="Name of the Pi Extension that fired."
    )
    action: str = Field(
        ..., description="Description of the action taken."
    )
    result: str = Field(
        ..., description="Outcome: SUCCESS, FAIL_AMBIGUITY, RETRY, etc."
    )
    details: Optional[str] = Field(
        default=None, description="Additional diagnostic context."
    )
    latency_ms: Optional[int] = Field(
        default=None, description="Extension execution time in milliseconds."
    )


class PiExtensionExecutionLog(BaseModel):
    """Primary Output Schema (DEP-ENG-034).

    §5: pi_extension_execution_log.json
    """

    execution_id: str = Field(
        ..., description="Unique execution cycle ID. Format: PI-EXT-{NNNN}."
    )
    pipeline_stage: str = Field(
        ..., description="Which pipeline stage this execution belongs to."
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    extensions_fired: list[ExtensionFired] = Field(
        default_factory=list,
        description="Ordered list of extensions that fired this cycle.",
    )
    latency_ms: int = Field(
        default=0, description="Total cycle latency in milliseconds."
    )
    coach_id: str = Field(
        default="", description="ADR-01: Coach scope for this execution."
    )
    waterfall_mode: bool = Field(
        default=False,
        description="§6: True if operating without system constraints.",
    )


# ══════════════════════════════════════════════════════════════════════════════
# InteractComp (§4.1)
# ══════════════════════════════════════════════════════════════════════════════

class InteractCompCheckResult(BaseModel):
    """Result of the InteractComp ambiguity gate.

    §4.1: If ANY required [DEP-ID] variable is missing or empty,
    status=FAIL_AMBIGUITY. Halts execution loop instantly.
    §8 AC1: Missing coach_brand.json → FAIL_AMBIGUITY, no LLM call.
    """

    status: ExtensionResult = Field(
        default=ExtensionResult.PASS,
        description="PASS or FAIL_AMBIGUITY.",
    )
    missing_dep_ids: list[str] = Field(
        default_factory=list,
        description="List of required DEP-IDs that are missing or empty.",
    )
    error_message: str = Field(
        default="",
        description="Human-readable halt message.",
    )
    llm_call_blocked: bool = Field(
        default=False,
        description="True if the LLM API call was prevented.",
    )

    def model_post_init(self, __context: Any) -> None:
        if self.missing_dep_ids:
            self.status = ExtensionResult.FAIL_AMBIGUITY
            self.llm_call_blocked = True
            if not self.error_message:
                deps = ", ".join(self.missing_dep_ids)
                self.error_message = (
                    f"Cannot proceed. Missing input context: [{deps}]. "
                    f"Refusing to hallucinate data."
                )


# ══════════════════════════════════════════════════════════════════════════════
# MemoryFolder (§4.2)
# ══════════════════════════════════════════════════════════════════════════════

class MemoryFoldAction(str, Enum):
    """What MemoryFolder does when triggered."""

    FOLD_AND_WRITE = "FOLD_AND_WRITE"
    NO_ACTION = "NO_ACTION"
    TASK_COMPLETE_FOLD = "TASK_COMPLETE_FOLD"


class MemoryFolderResult(BaseModel):
    """Result of a MemoryFolder invocation.

    §4.2: Summarizes last N steps into Working Memory, writes to Supabase,
    drops raw history from context window.
    """

    action: MemoryFoldAction = Field(
        default=MemoryFoldAction.NO_ACTION,
    )
    tokens_before: int = Field(default=0)
    tokens_after: int = Field(default=0)
    tokens_freed: int = Field(default=0)
    summary_written: str = Field(
        default="",
        description="The compressed summary written to Working Memory.",
    )
    supabase_write_success: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        self.tokens_freed = max(0, self.tokens_before - self.tokens_after)


# ══════════════════════════════════════════════════════════════════════════════
# DamageControl (§4.3)
# ══════════════════════════════════════════════════════════════════════════════

class DamageControlAttempt(BaseModel):
    """A single retry attempt within the DamageControl loop.

    §4.3: Feed exact error trace back to LLM. 3 retries max.
    """

    attempt_number: int = Field(ge=1, le=DAMAGE_CONTROL_MAX_RETRIES)
    error_type: str = Field(..., description="API Error Code or JSON Parse Error.")
    error_trace: str = Field(..., description="Exact error trace fed back to LLM.")
    system_message: str = Field(
        default="",
        description="Message injected: 'Action failed with trace [X]. Fix the syntax and retry.'",
    )
    resolved: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        if not self.system_message:
            self.system_message = (
                f"Action failed with trace [{self.error_trace}]. "
                f"Fix the syntax and retry."
            )


class DamageControlResult(BaseModel):
    """Full DamageControl cycle result.

    §4.3: Intercept error before crash. 3 retries.
    §8 AC4: Mock 500 error → catch, wait, retry without session drop.
    """

    attempts: list[DamageControlAttempt] = Field(default_factory=list)
    resolved: bool = Field(default=False)
    final_status: ExtensionResult = Field(default=ExtensionResult.FAIL)
    session_preserved: bool = Field(
        default=True,
        description="§8 AC4: Session must not be dropped during retry.",
    )

    def model_post_init(self, __context: Any) -> None:
        if self.attempts and self.attempts[-1].resolved:
            self.resolved = True
            self.final_status = ExtensionResult.SUCCESS
        elif len(self.attempts) >= DAMAGE_CONTROL_MAX_RETRIES:
            self.final_status = ExtensionResult.FAIL
        self.session_preserved = True  # DamageControl never drops session


# ══════════════════════════════════════════════════════════════════════════════
# ModelRouter (§4.4)
# ══════════════════════════════════════════════════════════════════════════════

# Routing rules per spec §4.4
_MODEL_ROUTING_TABLE: dict[TaskType, ModelTier] = {
    TaskType.STRATEGY: ModelTier.ULTRA_HIGH,
    TaskType.REASONING: ModelTier.ULTRA_HIGH,
    TaskType.DRAFTING: ModelTier.FAST_CHEAP,
    TaskType.FORMATTING: ModelTier.FAST_CHEAP,
    TaskType.CREATIVE: ModelTier.ULTRA_HIGH,
    TaskType.ANALYSIS: ModelTier.REASONING,
}


class ModelRouterDecision(BaseModel):
    """ModelRouter hot-swap decision.

    §4.4: Strategy/Reasoning → ultra_high. Drafting/Formatting → fast_cheap.
    """

    task_type: TaskType
    selected_tier: ModelTier = Field(default=ModelTier.ULTRA_HIGH)
    selected_model: str = Field(
        default="",
        description="Resolved model identifier (e.g., gpt-4o, gpt-4o-mini).",
    )
    hot_swap_performed: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        self.selected_tier = _MODEL_ROUTING_TABLE.get(
            self.task_type, ModelTier.ULTRA_HIGH
        )
        self.hot_swap_performed = True


# ══════════════════════════════════════════════════════════════════════════════
# TillDone (§4.5)
# ══════════════════════════════════════════════════════════════════════════════

class TillDoneIteration(BaseModel):
    """A single TillDone validation attempt."""

    iteration: int = Field(ge=1, le=TILL_DONE_MAX_ITERATIONS)
    schema_valid: bool = Field(default=False)
    missing_keys: list[str] = Field(
        default_factory=list,
        description="Keys missing from the LLM output vs. required schema.",
    )
    reprompt_message: str = Field(
        default="", description="System message appended if invalid.",
    )

    def model_post_init(self, __context: Any) -> None:
        if not self.schema_valid and not self.reprompt_message:
            if self.missing_keys:
                keys = ", ".join(self.missing_keys)
                self.reprompt_message = (
                    f"Requirement not met. Missing keys: [{keys}]. Continue."
                )
            else:
                self.reprompt_message = "Requirement not met. Continue."


class TillDoneResult(BaseModel):
    """Full TillDone assurance result.

    §4.5: If LLM outputs [FINISHED] but schema invalid → INCOMPLETE → reprompt.
    §8 AC2: 5-key JSON with only 4 → intercept, detect, retry, succeed by iter 2.
    """

    required_schema_keys: list[str] = Field(
        default_factory=list,
        description="The JSON keys required by the target schema.",
    )
    iterations: list[TillDoneIteration] = Field(default_factory=list)
    final_status: ExtensionResult = Field(default=ExtensionResult.INCOMPLETE)
    output_valid: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        if self.iterations:
            if any(it.schema_valid for it in self.iterations):
                self.final_status = ExtensionResult.SUCCESS
                self.output_valid = True
            elif len(self.iterations) >= TILL_DONE_MAX_ITERATIONS:
                self.final_status = ExtensionResult.FAIL


# ══════════════════════════════════════════════════════════════════════════════
# TeamOrchestrator (§4.6)
# ══════════════════════════════════════════════════════════════════════════════

class ParallelDraft(BaseModel):
    """A single draft from a parallel agent in TeamOrchestrator."""

    agent_index: int = Field(ge=0, lt=TEAM_ORCHESTRATOR_PARALLEL_COUNT)
    temperature: float = Field(ge=0.0, le=2.0)
    draft_text: str = Field(default="")
    selected: bool = Field(
        default=False,
        description="True if this draft was chosen as the best.",
    )


class TeamOrchestratorResult(BaseModel):
    """TeamOrchestrator parallel generation result.

    §4.6: Spawns 3 agents with different temperatures.
    DraftRL: multiple drafts, select best.
    """

    directive: str = Field(
        ..., description="The multi-perspective directive provided."
    )
    drafts: list[ParallelDraft] = Field(default_factory=list)
    selected_draft_index: Optional[int] = Field(
        default=None,
        description="Index of the selected best draft.",
    )
    consensus_reached: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        selected = [d for d in self.drafts if d.selected]
        if selected:
            self.selected_draft_index = selected[0].agent_index
            self.consensus_reached = True


# ══════════════════════════════════════════════════════════════════════════════
# SystemSelect (§4.7)
# ══════════════════════════════════════════════════════════════════════════════

class SystemSelectSwap(BaseModel):
    """SystemSelect persona swap result.

    §4.7: /system @[Persona] → overwrite system prompt with requested
    YAML constitution. Context preserved.
    §8 AC3: /system @Editor → purge Writer instructions, load Editor.
    """

    command: str = Field(
        ..., description="The raw /system command (e.g., '/system @Editor')."
    )
    previous_persona: str = Field(
        default="", description="The persona being replaced."
    )
    new_persona: str = Field(
        default="", description="The persona being loaded."
    )
    previous_instructions_purged: bool = Field(
        default=False,
        description="§8 AC3: Previous system instructions completely purged.",
    )
    new_instructions_loaded: bool = Field(
        default=False,
        description="New YAML constitution loaded into system prompt.",
    )
    conversation_history_preserved: bool = Field(
        default=True,
        description="§8 AC3: Conversation history maintained during swap.",
    )
    status: ExtensionResult = Field(default=ExtensionResult.SUCCESS)

    def model_post_init(self, __context: Any) -> None:
        # Parse the /system command to extract persona name
        if self.command.startswith("/system"):
            parts = self.command.split("@")
            if len(parts) == 2:
                self.new_persona = parts[1].strip()
        if self.new_persona and self.previous_persona != self.new_persona:
            self.previous_instructions_purged = True
            self.new_instructions_loaded = True
            self.conversation_history_preserved = True
            self.status = ExtensionResult.SUCCESS
        elif not self.new_persona:
            self.status = ExtensionResult.FAIL


# ══════════════════════════════════════════════════════════════════════════════
# Waterfall Mode Fallback (§6)
# ══════════════════════════════════════════════════════════════════════════════

class WaterfallModeAlert(BaseModel):
    """§6: Catastrophic runtime error → Waterfall Mode.

    All Intuition extensions bypassed, ModelRouter defaults to static model,
    pipeline executes sequentially. Severe dashboard alert triggered.
    """

    triggered: bool = Field(default=False)
    trigger_reason: str = Field(default="")
    alert_message: str = Field(
        default=(
            "WARNING: Operating without system constraints. "
            "Output resonance degradation likely."
        ),
    )
    intuition_bypassed: bool = Field(default=True)
    model_router_static: bool = Field(default=True)
    sequential_execution: bool = Field(default=True)


# ══════════════════════════════════════════════════════════════════════════════
# Intuition Trigger Signal (FR39 §4 Phase 2)
# ══════════════════════════════════════════════════════════════════════════════

class IntuitionTriggerSignalType(str, Enum):
    """Types of staleness/flatness detected by the Governance Layer."""

    STALENESS_DETECTED = "STALENESS_DETECTED"
    EMOTIONAL_FLATNESS = "EMOTIONAL_FLATNESS"
    STRUCTURAL_MONOTONY = "STRUCTURAL_MONOTONY"
    METAPHOR_REUSED = "METAPHOR_REUSED"
    COACH_ECHO = "COACH_ECHO"
    TVR_IMBALANCE = "TVR_IMBALANCE"
    POSITIVE_ONLY_SENTIMENT = "POSITIVE_ONLY_SENTIMENT"


class IntuitionTriggerSignal(BaseModel):
    """FR39 §4 Phase 2: Governance Layer activation signal to FR40.

    Detection trigger only — execution logic is owned by FR40.
    Receipt: INTUITION-TRIGGER-{signal_type}-{timestamp}.
    """

    signal_type: IntuitionTriggerSignalType
    coach_id: str = Field(..., min_length=3, max_length=3)
    detected_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    detection_evidence: str = Field(
        default="",
        description="What the Governance Layer observed.",
    )
    target_extension: Optional[str] = Field(
        default=None,
        description="Which FR40 extension should handle this.",
    )
    receipt_id: str = Field(default="")

    def model_post_init(self, __context: Any) -> None:
        if not self.receipt_id:
            self.receipt_id = (
                f"INTUITION-TRIGGER-{self.signal_type.value}-"
                f"{self.detected_at}"
            )
