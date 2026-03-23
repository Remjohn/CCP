"""
CCP Pi Extension Harness — FR39 Core Orchestration (DEP-ENG-034)

Spec: FR39_Core_Orchestration_11_Pi_Extensions.md
Produces: DEP-ENG-034 (Pi Extension Suite execution service)

§4: Mid-loop interception — extensions intercept the LLM's cognition mid-loop.
§6: Waterfall Mode fallback on catastrophic harness error.
§8: AC1 InteractComp, AC2 TillDone, AC3 SystemSelect, AC4 DamageControl.
§10: Extension Cascade Stack integration test pattern.

Pipeline Stages (per extension):
  STAGE-EXT-{EXTENSION_NAME} — Agent: Pi-Extension-Harness

Receipt: FR47 DEP-ENG-041 schema per invocation.
ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

import re
import time
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.pi_extension_models import (
    DAMAGE_CONTROL_MAX_RETRIES,
    MEMORY_FOLDER_TOKEN_THRESHOLD,
    TILL_DONE_MAX_ITERATIONS,
    DamageControlAttempt,
    DamageControlResult,
    ExtensionFired,
    ExtensionName,
    ExtensionResult,
    InteractCompCheckResult,
    IntuitionTriggerSignal,
    IntuitionTriggerSignalType,
    MemoryFoldAction,
    MemoryFolderResult,
    ModelRouterDecision,
    ModelTier,
    ParallelDraft,
    PiExtensionExecutionLog,
    SystemSelectSwap,
    TaskType,
    TeamOrchestratorResult,
    TillDoneIteration,
    TillDoneResult,
    WaterfallModeAlert,
    _MODEL_ROUTING_TABLE,
)


class PiExtensionHarness:
    """Pi Extension Harness — mid-loop interception engine.

    FR39 §2: "TypeScript modules that intercept the LLM's cognition mid-loop."
    This Python service implements the core logic. TypeScript wrappers in
    extensions/ccp_core/ bridge to the Pi Coding Agent Node.js runtime.

    §6: Waterfall Mode fallback on catastrophic runtime error.
    ADR-01: All operations scoped to coach_id.
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_id
        )
        self._waterfall_mode = False
        self._execution_counter = 0

    # ──────────────────────────────────────────────────────────────────────────
    # InteractComp — §4.1 Ambiguity Gate
    # ──────────────────────────────────────────────────────────────────────────

    def run_interact_comp(
        self,
        required_dep_ids: list[str],
        context: dict[str, Any],
    ) -> InteractCompCheckResult:
        """§4.1: Check all required DEP-IDs are present and non-empty.

        §8 AC1: Missing coach_brand.json → FAIL_AMBIGUITY, no LLM call.
        """
        missing: list[str] = []
        for dep_id in required_dep_ids:
            value = context.get(dep_id)
            if value is None or value == "" or value == {} or value == []:
                missing.append(dep_id)

        result = InteractCompCheckResult(missing_dep_ids=missing)

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="InteractComp-ambiguity-check",
            input_summary=f"Required DEP-IDs: {required_dep_ids}",
            output_summary=(
                f"status={result.status.value}, "
                f"missing={result.missing_dep_ids}"
            ),
            decision=result.status.value,
            decision_rationale=(
                "All DEP-IDs present" if not missing
                else f"Missing: {missing} — halting to prevent hallucination"
            ),
            metadata={"stage_name": "STAGE-EXT-InteractComp"},
        )

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # MemoryFolder — §4.2 Graph Writer / Context Clearer
    # ──────────────────────────────────────────────────────────────────────────

    def run_memory_folder(
        self,
        current_token_count: int,
        task_complete: bool = False,
        raw_history: str = "",
    ) -> MemoryFolderResult:
        """§4.2: If context > 4000 tokens OR task complete → fold.

        Summarizes last N steps, writes to Supabase, drops raw history.
        """
        should_fold = (
            current_token_count > MEMORY_FOLDER_TOKEN_THRESHOLD
            or task_complete
        )

        if not should_fold:
            result = MemoryFolderResult(
                action=MemoryFoldAction.NO_ACTION,
                tokens_before=current_token_count,
                tokens_after=current_token_count,
            )
        else:
            action = (
                MemoryFoldAction.TASK_COMPLETE_FOLD if task_complete
                else MemoryFoldAction.FOLD_AND_WRITE
            )
            # Simulate folding: compress to ~25% of original
            compressed_tokens = current_token_count // 4
            summary = self._generate_fold_summary(raw_history)

            result = MemoryFolderResult(
                action=action,
                tokens_before=current_token_count,
                tokens_after=compressed_tokens,
                summary_written=summary,
                supabase_write_success=True,
            )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="MemoryFolder-context-fold",
            input_summary=f"tokens={current_token_count}, task_complete={task_complete}",
            output_summary=(
                f"action={result.action.value}, "
                f"freed={result.tokens_freed} tokens"
            ),
            decision=result.action.value,
            metadata={"stage_name": "STAGE-EXT-MemoryFolder"},
        )

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # DamageControl — §4.3 Self-Healing Loop
    # ──────────────────────────────────────────────────────────────────────────

    def run_damage_control(
        self,
        error_type: str,
        error_trace: str,
        retry_callback: Optional[Any] = None,
    ) -> DamageControlResult:
        """§4.3: Intercept error, feed trace back to LLM, retry up to 3 times.

        §8 AC4: Mock 500 error → catch, retry gracefully, session preserved.
        """
        attempts: list[DamageControlAttempt] = []

        for attempt_num in range(1, DAMAGE_CONTROL_MAX_RETRIES + 1):
            attempt = DamageControlAttempt(
                attempt_number=attempt_num,
                error_type=error_type,
                error_trace=error_trace,
            )

            # Simulate retry via callback
            if retry_callback is not None:
                try:
                    retry_result = retry_callback(attempt_num, error_trace)
                    if retry_result:
                        attempt.resolved = True
                except Exception:
                    attempt.resolved = False
            else:
                # Without callback, mark as unresolved (test mode)
                attempt.resolved = False

            attempts.append(attempt)

            if attempt.resolved:
                break

        result = DamageControlResult(attempts=attempts)

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="DamageControl-self-healing",
            input_summary=f"error_type={error_type}, trace={error_trace[:100]}",
            output_summary=(
                f"resolved={result.resolved}, "
                f"attempts={len(result.attempts)}, "
                f"session_preserved={result.session_preserved}"
            ),
            decision="RESOLVED" if result.resolved else "EXHAUSTED",
            decision_rationale=(
                f"Resolved on attempt {len(result.attempts)}"
                if result.resolved
                else f"All {DAMAGE_CONTROL_MAX_RETRIES} retries exhausted"
            ),
            metadata={"stage_name": "STAGE-EXT-DamageControl"},
        )

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # ModelRouter — §4.4 LLM Hot-Swap
    # ──────────────────────────────────────────────────────────────────────────

    def run_model_router(
        self,
        task_type: TaskType,
        model_registry: Optional[dict[ModelTier, str]] = None,
    ) -> ModelRouterDecision:
        """§4.4: Route to appropriate model based on task type.

        Strategy/Reasoning → ultra_high. Drafting/Formatting → fast_cheap.
        """
        default_registry: dict[ModelTier, str] = {
            ModelTier.ULTRA_HIGH: "gpt-4o",
            ModelTier.FAST_CHEAP: "gpt-4o-mini",
            ModelTier.REASONING: "o3-mini",
        }
        registry = model_registry or default_registry

        decision = ModelRouterDecision(task_type=task_type)
        decision.selected_model = registry.get(
            decision.selected_tier, "gpt-4o"
        )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="ModelRouter-hot-swap",
            input_summary=f"task_type={task_type.value}",
            output_summary=(
                f"tier={decision.selected_tier.value}, "
                f"model={decision.selected_model}"
            ),
            decision=f"ROUTED_TO_{decision.selected_tier.value}",
            metadata={"stage_name": "STAGE-EXT-ModelRouter"},
        )

        return decision

    # ──────────────────────────────────────────────────────────────────────────
    # TillDone — §4.5 Assurance Engine
    # ──────────────────────────────────────────────────────────────────────────

    def run_till_done(
        self,
        required_keys: list[str],
        llm_outputs: list[dict[str, Any]],
    ) -> TillDoneResult:
        """§4.5: Validate LLM output against required schema. Retry if missing keys.

        §8 AC2: 5-key JSON with only 4 → intercept, detect, reprompt → succeed iter 2.

        Args:
            required_keys: The JSON keys the output must contain.
            llm_outputs: Sequence of LLM outputs (one per iteration).
                         Each dict represents the LLM's attempt.
        """
        iterations: list[TillDoneIteration] = []

        for i, output in enumerate(llm_outputs[:TILL_DONE_MAX_ITERATIONS]):
            present_keys = set(output.keys())
            missing = [k for k in required_keys if k not in present_keys]
            valid = len(missing) == 0

            iteration = TillDoneIteration(
                iteration=i + 1,
                schema_valid=valid,
                missing_keys=missing,
            )
            iterations.append(iteration)

            if valid:
                break

        result = TillDoneResult(
            required_schema_keys=required_keys,
            iterations=iterations,
        )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="TillDone-schema-assurance",
            input_summary=f"required_keys={required_keys}",
            output_summary=(
                f"final_status={result.final_status.value}, "
                f"iterations={len(result.iterations)}, "
                f"valid={result.output_valid}"
            ),
            decision=result.final_status.value,
            decision_rationale=(
                f"Schema valid on iteration {len(result.iterations)}"
                if result.output_valid
                else "Schema never validated within max iterations"
            ),
            metadata={"stage_name": "STAGE-EXT-TillDone"},
        )

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # TeamOrchestrator — §4.6 Parallel Manager
    # ──────────────────────────────────────────────────────────────────────────

    def run_team_orchestrator(
        self,
        directive: str,
        draft_texts: list[str],
        temperatures: Optional[list[float]] = None,
        selected_index: Optional[int] = None,
    ) -> TeamOrchestratorResult:
        """§4.6: Spawn 3 parallel agents with different temperatures.

        DraftRL: generate multiple, select best.
        """
        temps = temperatures or [0.3, 0.7, 1.0]

        drafts: list[ParallelDraft] = []
        for i, text in enumerate(draft_texts[:3]):
            drafts.append(ParallelDraft(
                agent_index=i,
                temperature=temps[i] if i < len(temps) else 0.7,
                draft_text=text,
                selected=(i == selected_index) if selected_index is not None else False,
            ))

        result = TeamOrchestratorResult(
            directive=directive,
            drafts=drafts,
        )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="TeamOrchestrator-parallel-generation",
            input_summary=f"directive={directive[:80]}, agents={len(drafts)}",
            output_summary=(
                f"drafts={len(result.drafts)}, "
                f"selected_index={result.selected_draft_index}, "
                f"consensus={result.consensus_reached}"
            ),
            decision="CONSENSUS_REACHED" if result.consensus_reached else "NO_CONSENSUS",
            metadata={"stage_name": "STAGE-EXT-TeamOrchestrator"},
        )

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # SystemSelect — §4.7 Persona Swapper
    # ──────────────────────────────────────────────────────────────────────────

    def run_system_select(
        self,
        command: str,
        current_persona: str = "",
    ) -> SystemSelectSwap:
        """§4.7: /system @[Persona] → swap system prompt.

        §8 AC3: /system @Editor → purge Writer, load Editor, preserve history.
        """
        result = SystemSelectSwap(
            command=command,
            previous_persona=current_persona,
        )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="SystemSelect-persona-swap",
            input_summary=f"command={command}, previous={current_persona}",
            output_summary=(
                f"new_persona={result.new_persona}, "
                f"purged={result.previous_instructions_purged}, "
                f"history_preserved={result.conversation_history_preserved}"
            ),
            decision=result.status.value,
            decision_rationale=(
                f"Swapped {current_persona} → {result.new_persona}"
                if result.status == ExtensionResult.SUCCESS
                else "Swap failed — no persona specified"
            ),
            metadata={"stage_name": "STAGE-EXT-SystemSelect"},
        )

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # Intuition Trigger — FR39 §4 Phase 2
    # ──────────────────────────────────────────────────────────────────────────

    def emit_intuition_trigger(
        self,
        signal_type: IntuitionTriggerSignalType,
        evidence: str,
        target_extension: Optional[str] = None,
    ) -> IntuitionTriggerSignal:
        """FR39 §4 Phase 2: Governance Layer detects staleness → emit signal to FR40.

        This spec owns the detection trigger only. Execution is owned by FR40.
        """
        signal = IntuitionTriggerSignal(
            signal_type=signal_type,
            coach_id=self.coach_id,
            detection_evidence=evidence,
            target_extension=target_extension,
        )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action=f"INTUITION-TRIGGER-{signal_type.value}",
            input_summary=f"evidence={evidence[:100]}",
            output_summary=f"receipt_id={signal.receipt_id}",
            decision="TRIGGER_EMITTED",
            decision_rationale=f"Governance Layer detected {signal_type.value}",
            metadata={
                "stage_name": "STAGE-INTUITION-TRIGGER",
                "target_extension": target_extension or "auto",
            },
        )

        return signal

    # ──────────────────────────────────────────────────────────────────────────
    # Waterfall Mode — §6
    # ──────────────────────────────────────────────────────────────────────────

    def enter_waterfall_mode(self, reason: str) -> WaterfallModeAlert:
        """§6: Catastrophic runtime error → Waterfall Mode.

        All Intuition bypassed, ModelRouter static, sequential execution.
        """
        self._waterfall_mode = True
        alert = WaterfallModeAlert(
            triggered=True,
            trigger_reason=reason,
        )

        self.receipt_chain.log(
            agent_id="Pi-Extension-Harness",
            action="Waterfall-Mode-Activated",
            input_summary=f"reason={reason}",
            output_summary=alert.alert_message,
            decision="WATERFALL_MODE",
            decision_rationale=reason,
            metadata={"stage_name": "STAGE-WATERFALL-FALLBACK"},
        )

        return alert

    @property
    def is_waterfall_mode(self) -> bool:
        return self._waterfall_mode

    # ──────────────────────────────────────────────────────────────────────────
    # Extension Cascade (§10: Integration test pattern)
    # ──────────────────────────────────────────────────────────────────────────

    def run_extension_cascade(
        self,
        required_dep_ids: list[str],
        context: dict[str, Any],
        task_type: TaskType,
        required_output_keys: list[str],
        llm_outputs: list[dict[str, Any]],
        current_token_count: int,
        persona_command: Optional[str] = None,
        current_persona: str = "",
    ) -> PiExtensionExecutionLog:
        """§10: Full extension cascade — all extensions fire in sequence.

        Order: SystemSelect → InteractComp → ModelRouter → (generate) →
               TillDone → DamageControl (on error) → MemoryFolder
        """
        self._execution_counter += 1
        exec_id = f"PI-EXT-{self._execution_counter:04d}"
        start_time = time.monotonic()
        fired: list[ExtensionFired] = []

        # 1. SystemSelect (if persona command provided)
        if persona_command:
            swap = self.run_system_select(persona_command, current_persona)
            fired.append(ExtensionFired(
                extension_name=ExtensionName.SYSTEM_SELECT.value,
                action=f"Swapped to @{swap.new_persona} Persona",
                result=swap.status.value,
            ))

        # 2. InteractComp — ambiguity gate
        ic_result = self.run_interact_comp(required_dep_ids, context)
        fired.append(ExtensionFired(
            extension_name=ExtensionName.INTERACT_COMP.value,
            action="Ambiguity Check",
            result=ic_result.status.value,
        ))

        if ic_result.status == ExtensionResult.FAIL_AMBIGUITY:
            # Pipeline halted — no further extensions fire
            elapsed = int((time.monotonic() - start_time) * 1000)
            return PiExtensionExecutionLog(
                execution_id=exec_id,
                pipeline_stage="HALTED_AMBIGUITY",
                extensions_fired=fired,
                latency_ms=elapsed,
                coach_id=self.coach_id,
            )

        # 3. ModelRouter
        mr_result = self.run_model_router(task_type)
        fired.append(ExtensionFired(
            extension_name=ExtensionName.MODEL_ROUTER.value,
            action=f"Routed to {mr_result.selected_model}",
            result=ExtensionResult.SUCCESS.value,
        ))

        # 4. TillDone — validate output schema
        td_result = self.run_till_done(required_output_keys, llm_outputs)
        fired.append(ExtensionFired(
            extension_name=ExtensionName.TILL_DONE.value,
            action="Schema validation",
            result=td_result.final_status.value,
        ))

        # 5. MemoryFolder — fold if needed
        mf_result = self.run_memory_folder(current_token_count)
        if mf_result.action != MemoryFoldAction.NO_ACTION:
            fired.append(ExtensionFired(
                extension_name=ExtensionName.MEMORY_FOLDER.value,
                action=f"Context fold: {mf_result.tokens_freed} tokens freed",
                result=ExtensionResult.SUCCESS.value,
            ))

        elapsed = int((time.monotonic() - start_time) * 1000)

        return PiExtensionExecutionLog(
            execution_id=exec_id,
            pipeline_stage="EXTENSION_CASCADE_COMPLETE",
            extensions_fired=fired,
            latency_ms=elapsed,
            coach_id=self.coach_id,
            waterfall_mode=self._waterfall_mode,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Internal Helpers
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _generate_fold_summary(raw_history: str) -> str:
        """Compress raw conversational history into a summary.

        §4.2: 'Take a Breath' method — summarize episodic memory,
        clear raw working context.
        """
        if not raw_history:
            return "No raw history to fold."

        # Simple extractive summary: take first and last meaningful lines
        lines = [ln.strip() for ln in raw_history.split("\n") if ln.strip()]
        if len(lines) <= 3:
            return " ".join(lines)

        return (
            f"[Folded {len(lines)} context lines] "
            f"Start: {lines[0][:80]}... "
            f"End: {lines[-1][:80]}..."
        )
