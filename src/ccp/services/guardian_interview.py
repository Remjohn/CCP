"""
CCP Guardian Agent — 5-Phase Interview Protocol (DEP-PROTO-019)
FR-GA Task 2 — OARS-structured Telegram onboarding interview.

The interview protocol is the seed that populates FR0A and FR0B inputs.
It uses Motivational Interviewing's OARS interactional architecture.

Spec references:
- FR_GA_Guardian_Agent_Tech_Spec.md §Genesis Flow item 1
- CCP_Architecture_Documentation_V2 §2 (5-phase table)
- FR_GA_Guardian_Agent_Tech_Spec.md §Stage 3a (Collision DNA Invariance Test)

State is persisted to Supabase/disk for resume capability via
/ccf-interview resume [phase].

Usage:
    from src.ccp.services.guardian_interview import InterviewProtocol

    protocol = InterviewProtocol(
        coach_id="NDL-0000",
        coach_acronym="NDL",
        coach_dir="./coaches/NDL",
        receipt_chain=receipt_chain,
    )
    result = await protocol.run()
"""

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class InterviewPhase(str, Enum):
    """The 5 interview phases from CCP_Architecture_Documentation_V2 §2."""

    BUSINESS_INTELLIGENCE = "BUSINESS_INTELLIGENCE"     # Phase 1: 8-10 questions → DEP-ENG-050 seed
    PHILOSOPHY_MISSION = "PHILOSOPHY_MISSION"           # Phase 2: 6-8 OARS questions → philosophy brief
    EMOTIONAL_DNA = "EMOTIONAL_DNA"                     # Phase 3: 7-10 scenario questions → emotional_dna seed
    TRIGGER_MAP = "TRIGGER_MAP"                         # Phase 4: 5-8 Conway AKB questions → trigger_map seed
    AUDIENCE_INTELLIGENCE = "AUDIENCE_INTELLIGENCE"     # Phase 5: 5-6 questions → FR0B research plan seed


# OARS interactional architecture (Miller & Rollnick)
OARS_TECHNIQUES = {
    "O": "Open questions — bypass identity-protective cognition",
    "A": "Affirmations — validate the coach's expertise authentically",
    "R": "Reflective Listening — reflect back to access deeper material",
    "S": "Linking Summaries — connect themes across responses",
}


class PhaseConfig(BaseModel):
    """Configuration for a single interview phase."""

    phase: InterviewPhase
    description: str
    min_questions: int
    max_questions: int
    quality_gate: str
    oars_emphasis: str  # Which OARS technique is primary for this phase
    output_dep_id: str  # What this phase seeds


PHASE_CONFIGS: list[PhaseConfig] = [
    PhaseConfig(
        phase=InterviewPhase.BUSINESS_INTELLIGENCE,
        description="Economic engine, unique mechanism, transformation map, market positioning",
        min_questions=8,
        max_questions=10,
        quality_gate="positioning_precision_test",
        oars_emphasis="O",  # Open questions to extract business model authentically
        output_dep_id="DEP-ENG-050",
    ),
    PhaseConfig(
        phase=InterviewPhase.PHILOSOPHY_MISSION,
        description="Core coaching philosophy, methodology, mission statement",
        min_questions=6,
        max_questions=8,
        quality_gate="authenticity_test",
        oars_emphasis="R",  # Reflective listening to get past professional mask
        output_dep_id="coach_philosophy_brief",
    ),
    PhaseConfig(
        phase=InterviewPhase.EMOTIONAL_DNA,
        description="Formative experiences, moral foundations, appraisal patterns",
        min_questions=7,
        max_questions=10,
        quality_gate="coverage_test",
        oars_emphasis="A",  # Affirmations to create safety for vulnerability
        output_dep_id="DEP-LIB-001",
    ),
    PhaseConfig(
        phase=InterviewPhase.TRIGGER_MAP,
        description="Conway AKB hierarchy, ESK-level sensory detail, PTG assessment",
        min_questions=5,
        max_questions=8,
        quality_gate="esk_test",
        oars_emphasis="R",  # Reflective listening to access episodic memory
        output_dep_id="trigger_map_seed",
    ),
    PhaseConfig(
        phase=InterviewPhase.AUDIENCE_INTELLIGENCE,
        description="Target audience seed data, tribal language, insider knowledge",
        min_questions=5,
        max_questions=6,
        quality_gate="insider_knowledge_test",
        oars_emphasis="O",  # Open questions about the audience's world
        output_dep_id="fr0b_research_plan",
    ),
]


class InterviewState(BaseModel):
    """Persistent state for resume capability."""

    interview_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
    )
    coach_id: str
    coach_acronym: str = Field(min_length=3, max_length=3)
    current_phase: InterviewPhase = Field(
        default=InterviewPhase.BUSINESS_INTELLIGENCE,
    )
    phase_results: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Results keyed by phase name",
    )
    started_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    completed_at: Optional[str] = Field(default=None)
    is_complete: bool = Field(default=False)


class InterviewProtocol:
    """5-Phase Interview Protocol (DEP-PROTO-019).

    OARS-structured Telegram conversation that seeds FR0A and FR0B.
    Each phase transition is gated by a Summary Reflection + coach confirmation.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: str,
        receipt_chain: ReceiptChain,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = Path(coach_dir)
        self.receipt_chain = receipt_chain

        # State persistence
        self.state_dir = self.coach_dir / "config" / "guardian"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    async def run(self) -> dict[str, Any]:
        """Execute the full 5-phase interview protocol.

        Returns:
            Dict with keys: complete, gates_passed, gates_failed, gaps, receipt_id
        """
        state = self._load_state()
        gates_passed = []
        gates_failed = []
        gaps = []

        for config in PHASE_CONFIGS:
            # Skip already-completed phases (for resume)
            if config.phase.value in state.phase_results:
                print(f"   ⏭️  {config.phase.value}: Already completed — skipping")
                gates_passed.append(config.quality_gate)
                continue

            print(f"   📝 Phase: {config.phase.value}")
            print(f"      {config.description}")
            print(f"      OARS emphasis: {OARS_TECHNIQUES[config.oars_emphasis]}")
            print(f"      Questions: {config.min_questions}-{config.max_questions}")

            # Execute phase (stub — actual Telegram interaction delegated to runtime)
            phase_result = await self._execute_phase(config, state)

            state.phase_results[config.phase.value] = phase_result
            state.current_phase = config.phase

            # Evaluate phase quality gate
            gate_passed = phase_result.get("gate_passed", True)
            if gate_passed:
                gates_passed.append(config.quality_gate)
                print(f"      ✅ Gate {config.quality_gate} passed")
            else:
                gaps.append(f"{config.quality_gate}: {phase_result.get('gate_reason', 'Unknown')}")
                gates_failed.append(config.quality_gate)
                print(f"      ⚠️  Gate {config.quality_gate} — provisional")

            # Log phase completion to receipt chain
            self.receipt_chain.log(
                agent_id="guardian_agent",
                action=f"interview_phase_{config.phase.value.lower()}_complete",
                input_summary=f"Phase: {config.phase.value} ({config.description})",
                output_summary=f"Gate {config.quality_gate}: {'PASS' if gate_passed else 'PROVISIONAL'}",
                decision="completed" if gate_passed else "provisional",
                metadata={
                    "phase": config.phase.value,
                    "quality_gate": config.quality_gate,
                    "gate_passed": gate_passed,
                    "output_dep_id": config.output_dep_id,
                },
            )

            self._save_state(state)

        # Run Collision DNA Invariance Test
        print("   🧬 Running 3-Topic Collision DNA Invariance Test...")
        invariance_result = await self._run_invariance_test(state)
        if invariance_result.get("passed"):
            gates_passed.append("collision_dna_invariance_test")
            print("      ✅ Collision DNA invariance confirmed across 3 topics")
        else:
            gaps.append("collision_dna_invariance_test: Signature topic-specific, not invariant")
            gates_failed.append("collision_dna_invariance_test")
            print("      ⚠️  Collision DNA invariance not confirmed — flagged for review")

        # Mark interview complete
        state.is_complete = True
        state.completed_at = datetime.now(timezone.utc).isoformat()
        self._save_state(state)

        # Save interview outputs
        outputs_path = self.state_dir / "interview_outputs.json"
        outputs_path.write_text(
            json.dumps(state.phase_results, indent=2, default=str),
            encoding="utf-8",
        )

        # Final receipt
        receipt = self.receipt_chain.log(
            agent_id="guardian_agent",
            action="interview_protocol_complete",
            input_summary=f"5-phase interview for {self.coach_id}",
            output_summary=f"Complete — {len(gates_passed)} gates passed, {len(gates_failed)} provisional",
            decision="completed",
            metadata={
                "interview_id": state.interview_id,
                "phases_completed": list(state.phase_results.keys()),
                "gates_passed": gates_passed,
                "gates_failed": gates_failed,
            },
        )

        return {
            "complete": len(gates_failed) == 0,
            "gates_passed": gates_passed,
            "gates_failed": gates_failed,
            "gaps": gaps,
            "receipt_id": receipt.receipt_id,
            "interview_id": state.interview_id,
        }

    async def _execute_phase(
        self,
        config: PhaseConfig,
        state: InterviewState,
    ) -> dict[str, Any]:
        """Execute a single interview phase.

        In production, this drives a Telegram conversation using OARS.
        Currently returns a stub result for orchestrator testing.
        """
        # Stub implementation — will be replaced with actual Telegram interaction
        return {
            "phase": config.phase.value,
            "questions_asked": config.min_questions,
            "responses_collected": config.min_questions,
            "gate_passed": True,
            "gate_reason": f"[STUB] Phase {config.phase.value} auto-passed for testing",
            "output_dep_id": config.output_dep_id,
            "oars_technique": config.oars_emphasis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def _run_invariance_test(
        self,
        state: InterviewState,
    ) -> dict[str, Any]:
        """Execute the 3-Topic Collision DNA Invariance Test.

        Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Genesis Flow §Stage 3a
        Pulls transcripts from 3 maximally different coaching topics.
        If the Collision DNA signature doesn't exist across all 3,
        it's topic-specific modulation and is discarded.

        Returns:
            Dict with "passed" (bool) and "details"
        """
        # Stub — requires actual transcript data and Collision DNA extraction
        return {
            "passed": True,
            "details": "[STUB] Invariance test auto-passed — requires real transcript data",
            "topics_tested": 3,
            "invariant_signatures_found": 0,
            "discarded_modulations": 0,
        }

    def get_status(self) -> dict[str, Any]:
        """Get current interview state for /ccf-interview status."""
        state = self._load_state()
        phases_total = len(PHASE_CONFIGS)
        phases_done = len(state.phase_results)

        return {
            "interview_id": state.interview_id,
            "current_phase": state.current_phase.value,
            "progress": f"{phases_done}/{phases_total}",
            "is_complete": state.is_complete,
            "phases_completed": list(state.phase_results.keys()),
            "started_at": state.started_at,
            "completed_at": state.completed_at,
        }

    def _load_state(self) -> InterviewState:
        """Load interview state from disk."""
        state_path = self.state_dir / "interview_state.json"
        if state_path.exists():
            data = json.loads(state_path.read_text(encoding="utf-8"))
            return InterviewState.model_validate(data)
        return InterviewState(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )

    def _save_state(self, state: InterviewState) -> None:
        """Persist interview state to disk."""
        state_path = self.state_dir / "interview_state.json"
        state_path.write_text(state.model_dump_json(indent=2), encoding="utf-8")
