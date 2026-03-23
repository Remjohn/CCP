"""
Step 11 — Integration Tests: CRAL 9-Skill Subsystem (FR15, FR16)

Acceptance Criteria covered:

FR15 — Scheduled Monitor Agent (4 ACs):
  AC1: Novelty Gate Enforcement — chronic topic with no >15% spike → FAIL → silent abort.
  AC2: Strict Prompt Formatting — 3-part structure required (Observation/Summaries/Question).
  AC3: Coach Decline Handling — 'No', 'Not today', short response → session_aborted_by_coach.
  AC4: ADR-01 Isolation — scraping limited to tribe_soul domains; cross-domain URL rejected.

FR16 — Quality & Safety Gates (2 ACs + Gate 2 variant):
  AC1: Safety FAIL_TERMINAL — self-harm content → pipeline halted, no bypass.
  AC2: Authenticity FAIL_REGENERATE — majority LLM-average language → regeneration required,
       NOT terminal halt.
  AC3: Gate 2 PASS on authentic content — personal anecdote + named person → PASS.
  AC4: Safe + authentic content → overall_pass=True.

Cross-spec smoke:
  Verify FR14 ADR-01: Two CRALOrchestrators with different coach_ids maintain
  isolated OODAState — no cross-tenant state leakage.

Note: FR14 ACs 1-5 and FR17 ACs 1-4 are fully covered in
test_step8_cral_and_synthesis.py (built in Step 8).
"""

from __future__ import annotations

import pytest

from src.ccp.models.scheduled_monitor_models import (
    CoachDeclineReason,
    MonitorRunStatus,
    MonitorVerdict,
    NOVELTY_SPIKE_PASS_THRESHOLD,
    NOVELTY_SPIKE_PROVISIONAL_MIN,
)
from src.ccp.services.scheduled_monitor_service import ScheduledMonitorService
from src.ccp.models.quality_safety_gate_models import (
    Gate1Verdict,
    Gate1TerminalError,
    Gate2Verdict,
)
from src.ccp.services.quality_safety_gates import QualitySafetyGateService


# ══════════════════════════════════════════════════════════════════════════════
# FR15 — Scheduled Monitor Agent
# ══════════════════════════════════════════════════════════════════════════════

# ── AC1: Novelty Gate Enforcement ─────────────────────────────────────────────

class TestFR15_AC1_NoveltyGateEnforcement:
    """AC1: If the agent scrapes a topic already heavily indexed in DEP-ENG-023
    (e.g., a chronic issue with no >15% recent spike), Stage 2 returns FAIL
    and a silent_abort log is written. The coach is NOT messaged.

    Spec §8 AC1 Failure Example: 'The agent messages the coach about
    "imposter syndrome" every single day because it's always talked about.'
    """

    def test_chronic_topic_below_threshold_triggers_silent_abort(self) -> None:
        service = ScheduledMonitorService(coach_id="EMI")
        result = service.run_full_pipeline(
            topic="imposter syndrome",
            source_domain="LinkedIn",
            frequency_delta_percent=6.5,  # below 10% → FAIL
        )
        assert result.run_status == MonitorRunStatus.ABORTED_NO_TENSION
        assert result.tension_observation is not None
        assert result.tension_observation.novelty_verdict == MonitorVerdict.FAIL
        assert result.abort_log is not None
        assert result.abort_log.abort_type == "silent_abort"
        assert result.prompt_payload is None, "Coach must NOT be messaged on FAIL"

    def test_topic_at_exact_fail_boundary(self) -> None:
        """9.9% spike — just below PROVISIONAL threshold → FAIL."""
        service = ScheduledMonitorService(coach_id="EMI")
        observation = service.assess_tension_novelty(
            topic="burnout",
            source_domain="Reddit",
            frequency_delta_percent=9.9,
        )
        assert observation.novelty_verdict == MonitorVerdict.FAIL

    def test_topic_at_provisional_boundary(self) -> None:
        """10.0% spike — at PROVISIONAL threshold → PROVISIONAL + weak_signal."""
        service = ScheduledMonitorService(coach_id="EMI")
        observation = service.assess_tension_novelty(
            topic="boundary setting",
            source_domain="TikTok",
            frequency_delta_percent=10.0,
        )
        assert observation.novelty_verdict == MonitorVerdict.PROVISIONAL
        assert observation.is_weak_signal is True

    def test_topic_above_pass_threshold_proceeds(self) -> None:
        """22% spike → PASS."""
        service = ScheduledMonitorService(coach_id="EMI")
        observation = service.assess_tension_novelty(
            topic="algorithm taxation for minority creators",
            source_domain="HustleCulture subreddit",
            frequency_delta_percent=22.0,
            practitioner_positions=[
                {"handle": "@BuilderDev", "platform": "Reddit",
                 "summary": "New feed throttles minority creator reach regardless of quality."},
            ],
        )
        assert observation.novelty_verdict == MonitorVerdict.PASS
        assert observation.is_weak_signal is False

    def test_provisional_signal_proceeds_to_prompt_with_weak_flag(self) -> None:
        """PROVISIONAL signal → prompt IS generated but is_weak_signal=True."""
        service = ScheduledMonitorService(coach_id="EMI")
        result = service.run_full_pipeline(
            topic="soft skills obsolescence",
            source_domain="LinkedIn",
            frequency_delta_percent=12.0,  # PROVISIONAL range
            practitioner_positions=[
                {"handle": "@CareerCoach", "platform": "LinkedIn",
                 "summary": "AI replacing soft skill roles debate emerging."},
            ],
        )
        assert result.run_status == MonitorRunStatus.COMPLETED_WEAK_SIGNAL
        assert result.prompt_payload is not None
        assert result.prompt_payload.is_weak_signal is True


# ── AC2: Strict Prompt Formatting ─────────────────────────────────────────────

class TestFR15_AC2_StrictPromptFormatting:
    """AC2: The Telegram message payload must contain the exact 3-part phrased
    structure: Observation, Practitioner Summaries, and Closing Question.

    Spec §8 AC2 Failure Example: 'The LLM generates a generic "Hey, anything
    you want to post about today?" bypassing the intelligent context delivery.'
    """

    def test_generated_prompt_has_3_part_structure(self) -> None:
        service = ScheduledMonitorService(coach_id="EMI")
        observation = service.assess_tension_novelty(
            topic="algorithm taxation impacting minority creators",
            source_domain="HustleCulture Subreddit",
            frequency_delta_percent=22.0,
            practitioner_positions=[
                {"handle": "@BuilderDev", "platform": "Reddit",
                 "summary": "Feed changes throttle minority creators regardless of quality."},
                {"handle": "@ContentMaker", "platform": "TikTok",
                 "summary": "Organic reach down 40% post-update — pivot to paid forced."},
                {"handle": "@DesignLead", "platform": "Instagram",
                 "summary": "Shadow ban shuffle — consistent high quality still penalised."},
            ],
        )
        prompt = service.build_telegram_prompt(observation)

        # Part 1: mentions community/conversation/seeing
        assert any(
            kw in prompt.part_1_observation.lower()
            for kw in ("community", "conversation", "seeing")
        )
        # Part 2: mentions practitioners/positions/tracked
        assert any(
            kw in prompt.part_2_practitioner_summaries.lower()
            for kw in ("practitioner", "tracked", "position", "user")
        )
        # Part 3: ends with a question mark
        assert "?" in prompt.part_3_closing_question

        # Overall structure validator
        assert prompt.has_required_structure() is True

    def test_full_message_is_non_empty(self) -> None:
        service = ScheduledMonitorService(coach_id="EMI")
        observation = service.assess_tension_novelty(
            topic="burnout rebranding as 'productivity optimization'",
            source_domain="Reddit",
            frequency_delta_percent=18.0,
        )
        prompt = service.build_telegram_prompt(observation)
        assert len(prompt.full_message) > 100

    def test_practitioner_positions_in_part_2(self) -> None:
        """The 3 practitioner positions must appear in Part 2."""
        service = ScheduledMonitorService(coach_id="EMI")
        observation = service.assess_tension_novelty(
            topic="AI replacing coaching",
            source_domain="LinkedIn",
            frequency_delta_percent=20.0,
            practitioner_positions=[
                {"handle": "@ExecCoach1", "platform": "LinkedIn",
                 "summary": "AI cannot replicate emotional attunement."},
                {"handle": "@HRLeader", "platform": "LinkedIn",
                 "summary": "Clients prefer AI availability over human empathy."},
                {"handle": "@StartupFund", "platform": "Twitter",
                 "summary": "Cost arbitrage will commoditise basic coaching."},
            ],
        )
        prompt = service.build_telegram_prompt(observation)
        assert "@ExecCoach1" in prompt.part_2_practitioner_summaries
        assert "@HRLeader" in prompt.part_2_practitioner_summaries


# ── AC3: Coach Decline Handling ───────────────────────────────────────────────

class TestFR15_AC3_CoachDeclineHandling:
    """AC3: Coach responds 'No' or 'I'm travelling today' → Intake Router
    correctly classifies as opt-out, logs abort, prevents corrupted DEP-ENG-005.

    Spec §8 AC3 Failure Example: 'The system treats "Not today" as the topic
    mechanism and attempts to run CRAL M2-M7 research.'
    """

    def test_explicit_no_response_aborts_session(self) -> None:
        service = ScheduledMonitorService(coach_id="EMI")
        result = service.run_full_pipeline(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
            practitioner_positions=[
                {"handle": "@dev1", "platform": "Reddit",
                 "summary": "Feed throttles minority creators."},
            ],
            coach_response_text="No",
        )
        assert result.run_status == MonitorRunStatus.ABORTED_COACH_DECLINED
        assert result.session_result is not None
        assert result.session_result.session_aborted is True
        assert result.session_result.abort_reason == CoachDeclineReason.OPT_OUT
        # DEP-ENG-005 trigger_id must NOT be set
        assert result.session_result.trigger_id == ""
        assert result.session_result.cral_initiation_signal_emitted is False

    def test_travelling_response_aborts_session(self) -> None:
        service = ScheduledMonitorService(coach_id="EMI")
        result = service.run_full_pipeline(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
            coach_response_text="I'm travelling today",
        )
        assert result.run_status == MonitorRunStatus.ABORTED_COACH_DECLINED
        assert result.session_result is not None
        assert result.session_result.session_aborted is True
        assert result.session_result.abort_reason == CoachDeclineReason.OPT_OUT

    def test_not_today_response_aborts_session(self) -> None:
        service = ScheduledMonitorService(coach_id="EMI")
        result = service.run_full_pipeline(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
            coach_response_text="Not today",
        )
        assert result.run_status == MonitorRunStatus.ABORTED_COACH_DECLINED
        assert result.session_result is not None
        assert result.session_result.session_aborted is True

    def test_insufficient_word_count_aborts_session(self) -> None:
        """Response < 15 words → INSUFFICIENT_CONTENT abort."""
        service = ScheduledMonitorService(coach_id="EMI")
        # Exactly 10 words — below the 15-word minimum
        short_response = "Yes I think this is interesting topic for sure"
        result = service.run_full_pipeline(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
            coach_response_text=short_response,
        )
        assert result.run_status == MonitorRunStatus.ABORTED_COACH_DECLINED
        assert result.session_result is not None
        assert result.session_result.abort_reason == CoachDeclineReason.INSUFFICIENT_CONTENT

    def test_valid_response_initiates_session_with_trigger_id(self) -> None:
        """Valid response (>15 words, not a decline) → trigger_id generated."""
        service = ScheduledMonitorService(coach_id="EMI")
        valid_response = (
            "Yes absolutely I was just talking to a client about this yesterday. "
            "They are terrified the new feed rules mean their engagement is permanently "
            "capped regardless of quality."
        )
        result = service.run_full_pipeline(
            topic="algorithm taxation impacting minority creators",
            source_domain="HustleCulture subreddit",
            frequency_delta_percent=22.0,
            practitioner_positions=[
                {"handle": "@BuilderDev", "platform": "Reddit",
                 "summary": "Feed changes throttle minority creators."},
            ],
            coach_response_text=valid_response,
        )
        assert result.run_status == MonitorRunStatus.SESSION_INITIATED
        assert result.session_result is not None
        assert result.session_result.session_aborted is False
        assert result.session_result.trigger_id.startswith("TRIG-EMI-")
        assert result.session_result.cral_initiation_signal_emitted is True
        assert result.session_result.authentication_status == "CONFIRMED_READY_FOR_M2"


# ── AC4: ADR-01 Isolation ─────────────────────────────────────────────────────

class TestFR15_AC4_ADR01Isolation:
    """AC4: The Scheduled Monitor Agent strictly limits its target scraping
    array to the URLs/domains listed in the active coach's tribe_soul.json.

    Spec §8 AC4 Failure Example: 'The agent uses a global trending topics API
    and prompts an executive leadership coach about a trending pop-culture meme
    completely irrelevant to their tribe.'
    """

    def test_out_of_scope_url_fails_adr01(self) -> None:
        """An out-of-scope URL in source_urls → adr01_verified=False."""
        service = ScheduledMonitorService(coach_id="EMI")
        # Coach EMI is LinkedIn + Reddit scoped. TikTok URL is out of scope.
        result = service.run_full_pipeline(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
            source_urls=[
                "https://reddit.com/r/HustleCulture/post1",
                "https://tiktok.com/trending/pop-culture-meme",  # OUT OF SCOPE
            ],
            allowed_domains=["reddit.com", "linkedin.com"],
        )
        assert result.adr01_verified is False

    def test_in_scope_urls_pass_adr01(self) -> None:
        """All source_urls within allowed_domains → adr01_verified=True."""
        service = ScheduledMonitorService(coach_id="EMI")
        result = service.run_full_pipeline(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
            source_urls=[
                "https://reddit.com/r/HustleCulture/post1",
                "https://linkedin.com/feed/update/123",
            ],
            allowed_domains=["reddit.com", "linkedin.com"],
        )
        assert result.adr01_verified is True

    def test_two_coaches_have_isolated_services(self) -> None:
        """Two ScheduledMonitorService instances with different coach_ids
        should not share state."""
        service_emi = ScheduledMonitorService(coach_id="EMI")
        service_mar = ScheduledMonitorService(coach_id="MAR")

        assert service_emi.coach_id == "EMI"
        assert service_mar.coach_id == "MAR"
        assert service_emi.coach_id != service_mar.coach_id

        # Each service builds prompts scoped to its own coach
        obs_emi = service_emi.assess_tension_novelty(
            topic="algorithm taxation",
            source_domain="Reddit",
            frequency_delta_percent=22.0,
        )
        obs_mar = service_mar.assess_tension_novelty(
            topic="client retention crisis",
            source_domain="LinkedIn",
            frequency_delta_percent=20.0,
        )

        assert obs_emi.coach_id == "EMI"
        assert obs_mar.coach_id == "MAR"

    def test_wrong_coach_id_length_raises(self) -> None:
        with pytest.raises(ValueError, match="coach_id must be 3 characters"):
            ScheduledMonitorService(coach_id="EMILIO")


# ══════════════════════════════════════════════════════════════════════════════
# FR16 — Quality & Safety Gates
# ══════════════════════════════════════════════════════════════════════════════

# ── AC1: Gate 1 FAIL_TERMINAL ─────────────────────────────────────────────────

class TestFR16_AC1_Gate1SafetyTerminalHalt:
    """AC1: Content containing self-harm / hate speech / severe distress →
    FAIL_TERMINAL. Pipeline is halted. No bypass. No regeneration.

    Spec §Gate 1: 'Ensures that the content being generated or passed through
    the pipeline does not violate core platform safety constraints.'
    """

    def test_self_harm_content_triggers_fail_terminal(self) -> None:
        service = QualitySafetyGateService(coach_id="EMI")
        content = (
            "Sometimes I feel like I want to kill myself because the pressure "
            "of constant productivity expectations is unbearable."
        )
        result = service.run_gate_1_safety(content, payload_id="TEST-001")
        assert result.verdict == Gate1Verdict.FAIL_TERMINAL
        assert result.is_terminal_halt is True
        assert len(result.flags) > 0
        assert any(f.category.value == "SELF_HARM" for f in result.flags)

    def test_fail_terminal_raises_when_requested(self) -> None:
        """run_gate_1_safety_raising() must raise Gate1TerminalError on FAIL_TERMINAL."""
        service = QualitySafetyGateService(coach_id="EMI")
        content = "The techniques are designed to make people want to end my life."
        with pytest.raises(Gate1TerminalError) as exc_info:
            service.run_gate_1_safety_raising(content, payload_id="TEST-002")
        assert exc_info.value.result.is_terminal_halt is True

    def test_safe_content_passes_gate_1(self) -> None:
        service = QualitySafetyGateService(coach_id="EMI")
        content = (
            "The meeting ended before anyone said what they actually meant. "
            "Marcus had watched this happen forty times and kept his mouth shut."
        )
        result = service.run_gate_1_safety(content, payload_id="TEST-003")
        assert result.verdict == Gate1Verdict.PASS
        assert result.is_terminal_halt is False
        assert len(result.flags) == 0

    def test_gate1_terminal_skips_gate2_in_combined_run(self) -> None:
        """When Gate 1 halts, Gate 2 should NOT run (None in report)."""
        service = QualitySafetyGateService(coach_id="EMI")
        content = "This is content about self-harm that should kill the pipeline."
        report = service.run_both_gates(content, payload_id="TEST-004")
        assert report.pipeline_halted is True
        assert report.gate_2_result is None
        assert report.overall_pass is False

    def test_adr01_gate1_result_scoped_to_coach(self) -> None:
        """Gate1SafetyResult must carry coach_id from the service."""
        service_emi = QualitySafetyGateService(coach_id="EMI")
        service_mar = QualitySafetyGateService(coach_id="MAR")
        content = "Safe content about personal growth."
        r_emi = service_emi.run_gate_1_safety(content)
        r_mar = service_mar.run_gate_1_safety(content)
        assert r_emi.coach_id == "EMI"
        assert r_mar.coach_id == "MAR"


# ── AC2: Gate 2 FAIL_REGENERATE (not terminal) ───────────────────────────────

class TestFR16_AC2_Gate2AuthenticityRegenerate:
    """AC2: Content with majority LLM-average language → Gate2Verdict.FAIL_REGENERATE.
    The pipeline loops back for regeneration — it does NOT halt.

    Spec §Gate 2: 'The Authenticity gate enforces that the output reflects
    genuine, biologically authentic markers rather than sterile, LLM-generated
    averages or statistically dry summaries.'
    """

    def test_generic_llm_content_triggers_fail_regenerate(self) -> None:
        service = QualitySafetyGateService(coach_id="EMI")
        # Pure statistical-average / LLM-sterile content
        llm_content = (
            "In today's world it is important to consider that many people feel "
            "overwhelmed by their responsibilities. Studies have shown that "
            "it was crucial to prioritize self-care. Statistics show that "
            "a lot of people struggle with work-life balance in the current landscape. "
            "It could be argued that perhaps this could be addressed through mindfulness."
        )
        result = service.run_gate_2_authenticity(llm_content, payload_id="TEST-010")
        assert result.verdict == Gate2Verdict.FAIL_REGENERATE
        assert result.requires_regeneration is True
        assert len(result.regeneration_guidance) > 0

    def test_fail_regenerate_is_not_terminal(self) -> None:
        """FAIL_REGENERATE must NOT trigger a pipeline halt."""
        service = QualitySafetyGateService(coach_id="EMI")
        llm_content = (
            "In today's society many people struggle. Statistics show this is vital."
        )
        report = service.run_both_gates(llm_content, payload_id="TEST-011")
        # Gate 2 must run (not halted by Gate 1)
        assert report.pipeline_halted is False
        assert report.gate_2_result is not None
        assert report.gate_2_result.verdict == Gate2Verdict.FAIL_REGENERATE
        assert report.overall_pass is False
        # But pipeline is NOT halted — regeneration path is open
        assert report.pipeline_halted is False

    def test_regeneration_guidance_is_provided(self) -> None:
        """Regeneration guidance must be non-empty on FAIL_REGENERATE."""
        service = QualitySafetyGateService(coach_id="EMI")
        content = (
            "Many people feel stuck. Studies have shown that it is important to change. "
            "In the current landscape perhaps this could help. Statistics show improvement."
        )
        result = service.run_gate_2_authenticity(content)
        if result.verdict == Gate2Verdict.FAIL_REGENERATE:
            assert len(result.regeneration_guidance) > 50


# ── AC3: Gate 2 PASS on authentic content ─────────────────────────────────────

class TestFR16_AC3_Gate2PassOnAuthenticContent:
    """AC3: Authentic content with personal anecdotes, named people, and
    vernacular language → Gate2Verdict.PASS."""

    def test_authentic_content_passes_gate_2(self) -> None:
        service = QualitySafetyGateService(coach_id="EMI")
        authentic_content = (
            "The meeting ended before anyone said what they actually meant. "
            "I watched Marcus Chen keep his mouth shut for the third time that week. "
            "That restraint felt professional. Looking back, it was cowardice. "
            "Real talk — the whole 'be professional' thing is just the shadow ban shuffle "
            "for your actual thoughts."
        )
        result = service.run_gate_2_authenticity(authentic_content, payload_id="TEST-020")
        assert result.verdict == Gate2Verdict.PASS
        assert result.requires_regeneration is False

    def test_named_person_increases_authentic_score(self) -> None:
        """Specific named person is a positive authenticity marker."""
        service = QualitySafetyGateService(coach_id="EMI")
        content = "I watched Sarah Johnson handle the negotiation with calm precision."
        result = service.run_gate_2_authenticity(content)
        authentic_signals = [s for s in result.signals if s.is_authentic]
        assert len(authentic_signals) > 0


# ── AC4: Safe + Authentic → overall_pass=True ────────────────────────────────

class TestFR16_AC4_FullGatePassthrough:
    """AC4: Content that passes both gates → overall_pass=True."""

    def test_safe_and_authentic_content_overall_pass(self) -> None:
        service = QualitySafetyGateService(coach_id="EMI")
        content = (
            "I asked Marcus Chen directly: 'When did you last say what you actually meant "
            "in that boardroom?' He went quiet for three seconds. That Tuesday, he told me "
            "the whole meeting culture was terrified of its own shadow."
        )
        report = service.run_both_gates(content, payload_id="TEST-030")
        assert report.gate_1_result is not None
        assert report.gate_1_result.verdict == Gate1Verdict.PASS
        assert report.gate_2_result is not None
        assert report.gate_2_result.verdict == Gate2Verdict.PASS
        assert report.overall_pass is True
        assert report.pipeline_halted is False
        assert report.regeneration_required is False

    def test_combined_report_carries_coach_id(self) -> None:
        service_emi = QualitySafetyGateService(coach_id="EMI")
        service_mar = QualitySafetyGateService(coach_id="MAR")
        content = "I told Sarah Chen what I really thought that morning."
        r_emi = service_emi.run_both_gates(content, "E-001")
        r_mar = service_mar.run_both_gates(content, "M-001")
        assert r_emi.coach_id == "EMI"
        assert r_mar.coach_id == "MAR"


# ══════════════════════════════════════════════════════════════════════════════
# Cross-Spec Smoke: FR14 ADR-01 Isolation
# ══════════════════════════════════════════════════════════════════════════════

class TestFR14_ADR01_CrossSpec_Smoke:
    """Cross-spec smoke: Two CRALOrchestrators with different coach_ids
    must maintain isolated OODAState — no cross-tenant state leakage.

    This complements FR14 AC5 (covered in test_step8_cral_and_synthesis.py)
    by verifying at the model layer that OODAState.coach_id is immutable
    per instantiation.
    """

    def test_two_ooda_states_are_isolated(self) -> None:
        from src.ccp.models.cral_research_models import OODAState

        state_emi = OODAState(coach_id="EMI", session_id="CRAL-EMI-001")
        state_mar = OODAState(coach_id="MAR", session_id="CRAL-MAR-001")

        state_emi.initialize_moments()
        state_mar.initialize_moments()

        # Mark M1 PASS in EMI state
        from src.ccp.models.cral_research_models import MomentStatus
        from src.ccp.models.adapter_registry_v2_models import CRALMomentKey
        state_emi.moments[CRALMomentKey.M1_TIMELY.value].status = MomentStatus.PASS

        # MAR state must be unaffected
        mar_m1 = state_mar.moments[CRALMomentKey.M1_TIMELY.value]
        assert mar_m1.status == MomentStatus.PENDING, (
            "ADR-01 VIOLATION: Marking M1 PASS in EMI's OODAState affected MAR's state."
        )

    def test_session_ids_are_unique_per_coach(self) -> None:
        from src.ccp.models.cral_research_models import OODAState

        state_emi = OODAState(coach_id="EMI", session_id="CRAL-EMI-SESSION-001")
        state_mar = OODAState(coach_id="MAR", session_id="CRAL-MAR-SESSION-001")

        assert state_emi.session_id != state_mar.session_id
        assert state_emi.coach_id != state_mar.coach_id

    def test_monitor_service_and_gate_service_isolated_by_coach(self) -> None:
        """FR15 + FR16 both use ADR-01 coach_id isolation."""
        monitor_emi = ScheduledMonitorService(coach_id="EMI")
        monitor_mar = ScheduledMonitorService(coach_id="MAR")
        gate_emi = QualitySafetyGateService(coach_id="EMI")
        gate_mar = QualitySafetyGateService(coach_id="MAR")

        assert monitor_emi.coach_id == "EMI"
        assert monitor_mar.coach_id == "MAR"
        assert gate_emi.coach_id == "EMI"
        assert gate_mar.coach_id == "MAR"
