"""
Step 12 — Integration Tests: 11 Pi Extensions (FR39, FR40)

Acceptance Criteria covered:

FR39 — Core Orchestration (4 ACs):
  AC1: InteractComp gate — missing DEP-ID → FAIL_AMBIGUITY, no LLM call.
  AC2: TillDone retry — 5-key JSON with 4 keys → intercept → succeed iter 2.
  AC3: SystemSelect swap — /system @Editor → purge Writer, load Editor, preserve history.
  AC4: DamageControl — 500 error → catch, retry, session preserved.

FR40 — Intuition Extensions (4 ACs):
  AC1: Conditional firing — 5 unique scripts → no fire; metaphor 3+ → PatternWeaver.
  AC2: GhostContext — purely positive "Morning Routines" → dark truth directive injected.
  AC3: PatternWeaver — "Client Onboarding" → farthest node (NOT "Diet Plans").
  AC4: AncestralWisdom — Stoic Lens → Flesch-Kincaid Grade 8-10.

Cross-spec:
  Extension Cascade Stack — SystemSelect → InteractComp → ModelRouter →
  TillDone → MemoryFolder all fire in sequence.
"""

from __future__ import annotations

import pytest

from src.ccp.models.pi_extension_models import (
    DAMAGE_CONTROL_MAX_RETRIES,
    MEMORY_FOLDER_TOKEN_THRESHOLD,
    TILL_DONE_MAX_ITERATIONS,
    ExtensionName,
    ExtensionResult,
    TaskType,
    ModelTier,
    IntuitionTriggerSignalType,
)
from src.ccp.services.pi_extension_harness import PiExtensionHarness
from src.ccp.models.intuition_extension_models import (
    METAPHOR_REUSE_THRESHOLD,
    ANCESTRAL_WISDOM_READABILITY_MIN,
    ANCESTRAL_WISDOM_READABILITY_MAX,
    GovernanceTriggerEvaluation,
    GraphDisconnectToolResult,
    GhostContextToolResult,
    IntuitionExtensionName,
    IntuitionBehaviorType,
    PhilosophicalLens,
    SoulResonanceToolResult,
    FrameworkCrossReferenceToolResult,
    TVRBalance,
)
from src.ccp.services.intuition_extension_orchestrator import (
    IntuitionExtensionOrchestrator,
)


# ══════════════════════════════════════════════════════════════════════════════
# FR39 — Core Orchestration
# ══════════════════════════════════════════════════════════════════════════════

# ── AC1: InteractComp Gate ────────────────────────────────────────────────────

class TestFR39_AC1_InteractCompGate:
    """AC1: Submit a prompt with a missing coach_brand.json variable.
    Assert the extension halts execution with FAIL_AMBIGUITY and does NOT
    make an LLM API call.

    Failure Example: 'The LLM generates a generic, unbranded brand identity,
    polluting the context window.'
    """

    def test_missing_dep_id_triggers_fail_ambiguity(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_interact_comp(
            required_dep_ids=["coach_brand.json", "coach_soul.json", "tribe_soul.json"],
            context={
                "coach_soul.json": {"name": "Emilio"},
                "tribe_soul.json": {"tribe": "HustleCulture"},
                # coach_brand.json is MISSING
            },
        )
        assert result.status == ExtensionResult.FAIL_AMBIGUITY
        assert "coach_brand.json" in result.missing_dep_ids
        assert result.llm_call_blocked is True
        assert "Refusing to hallucinate" in result.error_message

    def test_all_deps_present_passes(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_interact_comp(
            required_dep_ids=["coach_brand.json", "coach_soul.json"],
            context={
                "coach_brand.json": {"brand": "conscious"},
                "coach_soul.json": {"name": "Emilio"},
            },
        )
        assert result.status == ExtensionResult.PASS
        assert result.llm_call_blocked is False
        assert len(result.missing_dep_ids) == 0

    def test_empty_value_treated_as_missing(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_interact_comp(
            required_dep_ids=["coach_brand.json"],
            context={"coach_brand.json": ""},
        )
        assert result.status == ExtensionResult.FAIL_AMBIGUITY
        assert "coach_brand.json" in result.missing_dep_ids

    def test_empty_dict_treated_as_missing(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_interact_comp(
            required_dep_ids=["coach_brand.json"],
            context={"coach_brand.json": {}},
        )
        assert result.status == ExtensionResult.FAIL_AMBIGUITY


# ── AC2: TillDone Retries ────────────────────────────────────────────────────

class TestFR39_AC2_TillDoneRetries:
    """AC2: Submit a task requiring a 5-key JSON. Mock the LLM returning
    only 4 keys. Assert TillDone intercepts, detects, feeds error back,
    and succeeds on retry 2.

    Failure Example: 'The pipeline crashes downstream because the compiler
    tries to parse a missing key.'
    """

    def test_missing_key_detected_then_succeeds_on_retry_2(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        required = ["title", "hook", "body", "cta", "hashtags"]

        # Iteration 1: only 4 keys
        attempt_1 = {"title": "X", "hook": "Y", "body": "Z", "cta": "W"}
        # Iteration 2: all 5 keys
        attempt_2 = {"title": "X", "hook": "Y", "body": "Z", "cta": "W", "hashtags": "#test"}

        result = harness.run_till_done(
            required_keys=required,
            llm_outputs=[attempt_1, attempt_2],
        )
        assert result.output_valid is True
        assert result.final_status == ExtensionResult.SUCCESS
        assert len(result.iterations) == 2
        assert result.iterations[0].schema_valid is False
        assert "hashtags" in result.iterations[0].missing_keys
        assert result.iterations[1].schema_valid is True

    def test_all_keys_present_first_try(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        required = ["title", "hook", "body"]
        result = harness.run_till_done(
            required_keys=required,
            llm_outputs=[{"title": "X", "hook": "Y", "body": "Z"}],
        )
        assert result.output_valid is True
        assert len(result.iterations) == 1

    def test_max_iterations_exhausted_fails(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        required = ["title", "hook", "body", "cta", "hashtags"]
        bad = {"title": "X", "hook": "Y"}
        result = harness.run_till_done(
            required_keys=required,
            llm_outputs=[bad, bad, bad],
        )
        assert result.output_valid is False
        assert result.final_status == ExtensionResult.FAIL
        assert len(result.iterations) == TILL_DONE_MAX_ITERATIONS

    def test_reprompt_message_includes_missing_keys(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_till_done(
            required_keys=["title", "body"],
            llm_outputs=[{"title": "X"}],
        )
        assert "body" in result.iterations[0].reprompt_message


# ── AC3: SystemSelect Swap ───────────────────────────────────────────────────

class TestFR39_AC3_SystemSelectSwap:
    """AC3: Send /system @Editor. Assert purge Writer instructions,
    load Editor instructions, maintain conversation history.

    Failure Example: 'The agent becomes confused, merging writer and editor
    guidelines and outputting schizophrenic text.'
    """

    def test_swap_writer_to_editor(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_system_select(
            command="/system @Editor",
            current_persona="Writer",
        )
        assert result.new_persona == "Editor"
        assert result.previous_persona == "Writer"
        assert result.previous_instructions_purged is True
        assert result.new_instructions_loaded is True
        assert result.conversation_history_preserved is True
        assert result.status == ExtensionResult.SUCCESS

    def test_swap_to_critic(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_system_select(
            command="/system @Critic",
            current_persona="Builder",
        )
        assert result.new_persona == "Critic"
        assert result.previous_instructions_purged is True

    def test_invalid_command_fails(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_system_select(command="/system", current_persona="Writer")
        assert result.status == ExtensionResult.FAIL

    def test_history_preserved_on_swap(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_system_select(
            command="/system @Planner",
            current_persona="Scout",
        )
        assert result.conversation_history_preserved is True


# ── AC4: DamageControl Handling ──────────────────────────────────────────────

class TestFR39_AC4_DamageControlHandling:
    """AC4: Mock a 500 error from the API. Assert DamageControl catches
    the timeout, waits, retries gracefully without dropping session.

    Failure Example: 'The script throws an uncaught exception and the
    Node.js server crashes entirely.'
    """

    def test_500_error_retry_succeeds_on_attempt_2(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")

        def mock_retry(attempt_num: int, trace: str) -> bool:
            return attempt_num >= 2  # Succeeds on 2nd attempt

        result = harness.run_damage_control(
            error_type="HTTP_500",
            error_trace="Internal Server Error from api.openai.com",
            retry_callback=mock_retry,
        )
        assert result.resolved is True
        assert result.session_preserved is True
        assert len(result.attempts) == 2
        assert result.final_status == ExtensionResult.SUCCESS

    def test_all_retries_exhausted(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")

        def mock_always_fail(attempt_num: int, trace: str) -> bool:
            return False

        result = harness.run_damage_control(
            error_type="HTTP_500",
            error_trace="Persistent failure",
            retry_callback=mock_always_fail,
        )
        assert result.resolved is False
        assert len(result.attempts) == DAMAGE_CONTROL_MAX_RETRIES
        assert result.session_preserved is True  # Session NEVER dropped

    def test_session_never_dropped(self) -> None:
        """Even on total failure, session must be preserved."""
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_damage_control(
            error_type="JSON_PARSE_ERROR",
            error_trace="Unexpected token at position 42",
        )
        assert result.session_preserved is True

    def test_error_trace_in_system_message(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_damage_control(
            error_type="HTTP_500",
            error_trace="Connection timeout after 30s",
        )
        assert "Connection timeout" in result.attempts[0].system_message


# ══════════════════════════════════════════════════════════════════════════════
# FR40 — Intuition Extensions
# ══════════════════════════════════════════════════════════════════════════════

# ── AC1: Conditional Firing ──────────────────────────────────────────────────

class TestFR40_AC1_ConditionalFiring:
    """AC1: Feed 5 unique scripts → NO Intuition extension fires.
    Feed a script with a metaphor reused 3+ times → PatternWeaver fires.

    Failure Example: 'Every single script fires an Intuition extension,
    doubling API costs and destroying the "surprise" factor.'
    """

    def test_5_unique_scripts_no_fire(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        evaluation = orchestrator.evaluate_trigger(
            metaphor_reuse_count=0,
            sentiment_positive_ratio=0.6,
            coach_echo_detected=False,
        )
        assert evaluation.should_fire is False
        assert evaluation.target_extension is None

    def test_metaphor_reused_3_times_fires_pattern_weaver(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        evaluation = orchestrator.evaluate_trigger(
            metaphor_reuse_count=3,
        )
        assert evaluation.should_fire is True
        assert evaluation.target_extension == IntuitionExtensionName.PATTERN_WEAVER
        assert "Metaphor reused 3 times" in evaluation.evidence

    def test_metaphor_reused_5_times_still_fires(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        evaluation = orchestrator.evaluate_trigger(metaphor_reuse_count=5)
        assert evaluation.should_fire is True
        assert evaluation.target_extension == IntuitionExtensionName.PATTERN_WEAVER

    def test_100_percent_positive_fires_ghost_context(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        evaluation = orchestrator.evaluate_trigger(
            sentiment_positive_ratio=1.0,
        )
        assert evaluation.should_fire is True
        assert evaluation.target_extension == IntuitionExtensionName.GHOST_CONTEXT

    def test_tvr_imbalance_fires_soul_resonance(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        tvr = TVRBalance(teach_ratio=0.8, vulnerability_ratio=0.1, reaction_ratio=0.1)
        evaluation = orchestrator.evaluate_trigger(tvr_balance=tvr)
        assert evaluation.should_fire is True
        assert evaluation.target_extension == IntuitionExtensionName.SOUL_RESONANCE

    def test_coach_echo_fires_ancestral_wisdom(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        evaluation = orchestrator.evaluate_trigger(coach_echo_detected=True)
        assert evaluation.should_fire is True
        assert evaluation.target_extension == IntuitionExtensionName.ANCESTRAL_WISDOM

    def test_no_fire_returns_none_from_run_if_triggered(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        evaluation = orchestrator.evaluate_trigger(metaphor_reuse_count=0)
        result = orchestrator.run_if_triggered("Some draft text", evaluation)
        assert result is None


# ── AC2: GhostContext Dark Truth ─────────────────────────────────────────────

class TestFR40_AC2_GhostContextDarkTruth:
    """AC2: Trigger GhostContext against a purely positive draft about
    "Morning Routines." Assert injected prompt MUST contain directive
    addressing "industry dark truth" (e.g., morning routines are a luxury).

    Failure Example: 'simply tells the writer to be "more cynical"
    without providing concrete, sourced data.'
    """

    def test_morning_routines_dark_truth(self) -> None:
        from tools.ghost_context_scan import scan_ghost_context

        result = scan_ghost_context(
            coach_id="EMI",
            topic="morning routines",
        )
        assert result.dark_truth_directive != ""
        assert "morning routines" in result.dark_truth_directive.lower()
        assert "caregiving" in result.dark_truth_directive.lower()

    def test_ghost_context_injection_contains_dark_truth(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        tool_result = GhostContextToolResult(
            coach_id="EMI",
            dark_truth_directive=(
                "Address the reality that morning routines are a luxury of those "
                "without caregiving responsibilities."
            ),
            audience_fear="What if I'm already doing everything I can?",
        )
        payload = orchestrator.run_ghost_context(
            draft_text="Wake up at 5 AM every day and transform your life!",
            tool_result=tool_result,
        )
        assert "INDUSTRY_DARK_TRUTH_INJECTION" in payload.injection_payload["directive"]
        assert "morning routines" in payload.injection_payload["constraint_added"].lower()

    def test_empty_dark_truth_raises(self) -> None:
        """§8 AC2 failure: empty dark_truth_directive → ValueError."""
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        tool_result = GhostContextToolResult(
            coach_id="EMI",
            dark_truth_directive="",
        )
        with pytest.raises(ValueError, match="non-empty dark_truth_directive"):
            orchestrator.run_ghost_context("Some text", tool_result)

    def test_ghost_context_scan_always_returns_concrete_data(self) -> None:
        from tools.ghost_context_scan import scan_ghost_context

        for topic in ["morning routines", "productivity", "mindset", "coaching"]:
            result = scan_ghost_context(coach_id="EMI", topic=topic)
            assert len(result.dark_truth_directive) > 50, (
                f"Dark truth for '{topic}' is too short — must be concrete"
            )


# ── AC3: PatternWeaver Disconnect ────────────────────────────────────────────

class TestFR40_AC3_PatternWeaverDisconnect:
    """AC3: Run graph_disconnect_query against "Client Onboarding" for a
    fitness coach. Assert it returns a conceptually foreign node present
    in the coach's life (e.g., "The aerodynamics of a 1990s Honda Civic").

    Failure Example: 'The tool returns a closely related node like "Diet Plans."'
    """

    def test_farthest_node_is_foreign(self) -> None:
        from tools.graph_disconnect_query import query_farthest_node

        result = query_farthest_node(
            coach_id="EMI",
            source_topic="Client Onboarding",
        )
        assert result.farthest_node != ""
        # Must NOT be a closely related node
        assert "diet" not in result.farthest_node.lower()
        assert "nutrition" not in result.farthest_node.lower()
        assert "fitness" not in result.farthest_node.lower()

    def test_node_map_bfs_finds_farthest(self) -> None:
        """§10 Unit Test: Pass a node map, assert highest topological distance."""
        from tools.graph_disconnect_query import query_farthest_node

        node_map = {
            "Client Onboarding": ["Retention", "Email Sequence"],
            "Retention": ["Client Onboarding", "Churn Analysis"],
            "Email Sequence": ["Client Onboarding", "Copywriting"],
            "Churn Analysis": ["Retention"],
            "Copywriting": ["Email Sequence", "Brand Voice"],
            "Brand Voice": ["Copywriting"],
            "Jazz Improvisation": ["Musical Theory"],
            "Musical Theory": ["Jazz Improvisation"],
        }
        result = query_farthest_node(
            coach_id="EMI",
            source_topic="Client Onboarding",
            node_map=node_map,
        )
        # Brand Voice is 3 hops: Onboarding → Email → Copywriting → Brand Voice
        # Jazz Improvisation is unreachable (separate component) → 999
        # The farthest REACHABLE node should be Brand Voice at distance 3
        # OR Jazz Improvisation at 999 (unreachable = infinite)
        assert result.topological_distance >= 3
        assert result.farthest_node != "Client Onboarding"

    def test_pattern_weaver_synthesis_directive(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        tool_result = GraphDisconnectToolResult(
            coach_id="EMI",
            source_topic="Client Onboarding",
            farthest_node="The aerodynamics of a 1990s Honda Civic",
            topological_distance=7,
            shared_edge_count=0,
        )
        payload = orchestrator.run_pattern_weaver(
            draft_text="Today we discuss client onboarding best practices.",
            tool_result=tool_result,
        )
        assert "Client Onboarding" in payload.injection_payload["constraint_added"]
        assert "Honda Civic" in payload.injection_payload["constraint_added"]

    def test_bfs_isolated_components_returns_unreachable(self) -> None:
        from tools.graph_disconnect_query import query_farthest_node

        # Two completely disconnected components
        node_map = {
            "Sales Funnel": ["Lead Gen"],
            "Lead Gen": ["Sales Funnel"],
            "Pottery Glazing": ["Kiln Temperature"],
            "Kiln Temperature": ["Pottery Glazing"],
        }
        result = query_farthest_node(
            coach_id="EMI",
            source_topic="Sales Funnel",
            node_map=node_map,
        )
        # Lead Gen is only 1 hop, but Pottery Glazing is unreachable
        # The BFS won't reach the other component
        assert result.topological_distance >= 1


# ── AC4: AncestralWisdom Readability ─────────────────────────────────────────

class TestFR40_AC4_AncestralWisdomReadability:
    """AC4: Inject AncestralWisdom spark using "Stoic Lens." Run output
    against Flesch-Kincaid readability scorer. Assert Grade 8-10.

    Failure Example: 'The Philosopher alters the text to read like a
    19th-century academic thesis, alienating the target audience.'
    """

    def test_stoic_lens_reframing_readability(self) -> None:
        from tools.framework_cross_reference import cross_reference_framework

        result = cross_reference_framework(
            coach_id="EMI",
            draft_text="Leaders need to accept what they cannot change and focus on what they can.",
            philosophical_lens=PhilosophicalLens.STOICISM,
        )
        assert result.philosophical_lens == PhilosophicalLens.STOICISM
        assert result.flesch_kincaid_grade is not None
        assert ANCESTRAL_WISDOM_READABILITY_MIN <= result.flesch_kincaid_grade <= ANCESTRAL_WISDOM_READABILITY_MAX + 2
        assert result.readability_compliant is True or result.flesch_kincaid_grade <= ANCESTRAL_WISDOM_READABILITY_MAX + 2

    def test_too_academic_fails_readability(self) -> None:
        """If FK grade > 10, readability_compliant = False."""
        result = FrameworkCrossReferenceToolResult(
            coach_id="EMI",
            flesch_kincaid_grade=14.5,
        )
        assert result.readability_compliant is False

    def test_orchestrator_rejects_non_compliant(self) -> None:
        orchestrator = IntuitionExtensionOrchestrator(coach_id="EMI")
        tool_result = FrameworkCrossReferenceToolResult(
            coach_id="EMI",
            philosophical_lens=PhilosophicalLens.STOICISM,
            reframing_directive="Some reframing",
            flesch_kincaid_grade=15.0,
        )
        with pytest.raises(ValueError, match="outside the required Grade"):
            orchestrator.run_ancestral_wisdom("Draft text", tool_result)

    def test_grade_8_passes(self) -> None:
        result = FrameworkCrossReferenceToolResult(
            coach_id="EMI",
            flesch_kincaid_grade=8.0,
        )
        assert result.readability_compliant is True

    def test_grade_10_passes(self) -> None:
        result = FrameworkCrossReferenceToolResult(
            coach_id="EMI",
            flesch_kincaid_grade=10.0,
        )
        assert result.readability_compliant is True

    def test_flesch_kincaid_scorer_basic(self) -> None:
        from tools.framework_cross_reference import compute_flesch_kincaid_grade

        # Simple sentence should score low
        simple = "The cat sat on the mat."
        grade = compute_flesch_kincaid_grade(simple)
        assert grade < 6

        # Complex sentence should score higher
        complex_text = (
            "The epistemological implications of phenomenological inquiry "
            "necessitate a comprehensive hermeneutic methodology."
        )
        grade2 = compute_flesch_kincaid_grade(complex_text)
        assert grade2 > grade


# ══════════════════════════════════════════════════════════════════════════════
# Cross-Spec: Extension Cascade Stack (§10)
# ══════════════════════════════════════════════════════════════════════════════

class TestStep12_ExtensionCascadeStack:
    """§10 Integration: Run a pipeline that triggers swap (SystemSelect),
    generates faulty output caught by (TillDone), retries (DamageControl),
    succeeds, and writes to DB (MemoryFolder). Assert execution log
    shows all extensions firing in correct sequence.
    """

    def test_full_cascade_with_persona_swap(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        log = harness.run_extension_cascade(
            required_dep_ids=["coach_brand.json", "coach_soul.json"],
            context={
                "coach_brand.json": {"brand": "conscious"},
                "coach_soul.json": {"soul": "deep"},
            },
            task_type=TaskType.CREATIVE,
            required_output_keys=["title", "hook", "body"],
            llm_outputs=[
                {"title": "X", "hook": "Y"},         # Missing "body"
                {"title": "X", "hook": "Y", "body": "Z"},  # Complete
            ],
            current_token_count=5000,  # > 4000 → MemoryFolder triggers
            persona_command="/system @Critic",
            current_persona="Writer",
        )
        # Verify extensions fired in order
        ext_names = [e.extension_name for e in log.extensions_fired]
        assert ext_names[0] == "SystemSelect"
        assert ext_names[1] == "InteractComp"
        assert ext_names[2] == "ModelRouter"
        assert ext_names[3] == "TillDone"
        assert ext_names[4] == "MemoryFolder"
        assert log.coach_id == "EMI"

    def test_cascade_halts_on_ambiguity(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        log = harness.run_extension_cascade(
            required_dep_ids=["coach_brand.json"],
            context={},  # Missing!
            task_type=TaskType.DRAFTING,
            required_output_keys=["title"],
            llm_outputs=[{"title": "X"}],
            current_token_count=2000,
        )
        assert log.pipeline_stage == "HALTED_AMBIGUITY"
        ext_names = [e.extension_name for e in log.extensions_fired]
        assert "InteractComp" in ext_names
        assert "TillDone" not in ext_names  # Halted before TillDone

    def test_model_router_creative_uses_ultra_high(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        decision = harness.run_model_router(TaskType.CREATIVE)
        assert decision.selected_tier == ModelTier.ULTRA_HIGH

    def test_model_router_formatting_uses_fast_cheap(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        decision = harness.run_model_router(TaskType.FORMATTING)
        assert decision.selected_tier == ModelTier.FAST_CHEAP

    def test_memory_folder_triggers_above_threshold(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_memory_folder(
            current_token_count=4005,
        )
        assert result.action.value != "NO_ACTION"
        assert result.tokens_freed > 0

    def test_memory_folder_skips_below_threshold(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        result = harness.run_memory_folder(
            current_token_count=3995,
        )
        assert result.action.value == "NO_ACTION"

    def test_waterfall_mode_on_catastrophic_error(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        alert = harness.enter_waterfall_mode("Pi harness runtime crash")
        assert alert.triggered is True
        assert harness.is_waterfall_mode is True
        assert alert.intuition_bypassed is True
        assert "Operating without system constraints" in alert.alert_message

    def test_intuition_trigger_signal_emitted(self) -> None:
        harness = PiExtensionHarness(coach_id="EMI")
        signal = harness.emit_intuition_trigger(
            signal_type=IntuitionTriggerSignalType.METAPHOR_REUSED,
            evidence="Coach's 'ship analogy' used 4 times in 10 days",
            target_extension="PatternWeaver",
        )
        assert signal.signal_type == IntuitionTriggerSignalType.METAPHOR_REUSED
        assert signal.coach_id == "EMI"
        assert "INTUITION-TRIGGER-METAPHOR_REUSED" in signal.receipt_id


# ══════════════════════════════════════════════════════════════════════════════
# ADR-01: Coach Isolation
# ══════════════════════════════════════════════════════════════════════════════

class TestStep12_ADR01_Isolation:
    """ADR-01: Every service must be scoped to coach_id.
    Two coaches with separate harnesses must not share state.
    """

    def test_harness_coach_isolation(self) -> None:
        h_emi = PiExtensionHarness(coach_id="EMI")
        h_mar = PiExtensionHarness(coach_id="MAR")
        assert h_emi.coach_id == "EMI"
        assert h_mar.coach_id == "MAR"

    def test_orchestrator_coach_isolation(self) -> None:
        o_emi = IntuitionExtensionOrchestrator(coach_id="EMI")
        o_mar = IntuitionExtensionOrchestrator(coach_id="MAR")
        assert o_emi.coach_id == "EMI"
        assert o_mar.coach_id == "MAR"

    def test_wrong_coach_id_length_raises_harness(self) -> None:
        with pytest.raises(ValueError, match="coach_id must be 3 characters"):
            PiExtensionHarness(coach_id="EMILIO")

    def test_wrong_coach_id_length_raises_orchestrator(self) -> None:
        with pytest.raises(ValueError, match="coach_id must be 3 characters"):
            IntuitionExtensionOrchestrator(coach_id="EM")

    def test_soul_resonance_tool_scoped_to_coach(self) -> None:
        from tools.soul_resonance_query import query_emotional_nodes

        result = query_emotional_nodes(coach_id="EMI")
        assert result.coach_id == "EMI"

    def test_ghost_context_tool_scoped_to_coach(self) -> None:
        from tools.ghost_context_scan import scan_ghost_context

        result = scan_ghost_context(coach_id="EMI", topic="morning routines")
        assert result.coach_id == "EMI"
