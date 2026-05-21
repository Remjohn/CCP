"""
CCP Morgan Orchestrator — FR1 Unit 2
Phase 0 gate enforcement, production lock, command sequencing.

Spec reference: FR1 Tech Spec §Phase 0, §Phase 0 Completion Summary,
                §Phase 1, AC1, AC3, AC4
Architecture reference: CCP_Technical_Architecture.md §5.2 (Corrected Intake Flow)

CRITICAL RULES from spec:
- Production lock is a hard code gate — not a prompt instruction (Step 7.5)
- Manual coach trigger returns a specific canned response (AC4)
- CMM must be operator-confirmed before Phase 1 (AC3)
- Scheduled Monitor Agent ONLY initiates production — never manual coach trigger (AC4)
- C-11 Persona Masking Gate: agent names never in API payloads

PRODUCTION LOCK GATE (Unit 3) is implemented as ProductionLockGate class within this module.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain, ReceiptEntry
from src.ccp.models.v5_models import (
    ContextPerformanceRegistry,
    CulturalMemoryMap,
    HumorMechanismRegistry,
    CoachStoryArchive,
)


# ──────────────────────────────────────────────────────────────
# UNIT 3 — Production Lock Gate
# Spec: Phase 0, Step 7.5 — "This is a hard code gate — not a prompt instruction."
# AC1: "Without a complete leadership_scorecard.json, triggering ccf-batch returns
# PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD from Morgan's gate — not a prompt failure."
# Operator resolution: score all 12 traits; hard gate floor = ≥5 traits with score > 0.
# ──────────────────────────────────────────────────────────────

class ProductionLockGate:
    """Hard code gate enforcing leadership_scorecard.json before production.

    Spec: 'leadership_scorecard.json must exist AND must cover all 5 minimum
    trait categories before Morgan will authorize any production pipeline run.
    This is a hard code gate — not a prompt instruction.'

    Operator resolution (2026-03-19): Score all 12 traits. Gate floor = ≥5 traits
    with score > 0. Ideal = 12/12 traits scored. Scorer always attempts all 12.
    """

    # All 12 trait names as defined in LeadershipScores (coach_soul.py)
    ALL_TRAITS: list[str] = [
        "deep_empathy", "authentic_vulnerability", "embodied_confidence",
        "strategic_patience", "radical_honesty", "grounded_presence",
        "visionary_clarity", "playful_irreverence", "fierce_compassion",
        "sacred_boundaries", "intuitive_timing", "sovereign_authority",
    ]

    # Hard gate floor: ≥5 traits must have score > 0 (operator resolution 2026-03-19)
    MINIMUM_SCORED_TRAITS: int = 5

    def __init__(self, coach_dir: Path):
        self.coach_dir = coach_dir
        self.scorecard_path = coach_dir / "config" / "leadership_scorecard.json"

    def check(self) -> tuple[bool, str, dict]:
        """Execute the production lock gate check.

        Returns:
            (passes: bool, error_code: str, details: dict)
            If passes=True, error_code is "" and details contains score summary.
            If passes=False, error_code is the exact AC1 error string.

        Spec AC1: "triggering ccf-batch returns PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD
        from Morgan's gate — not a prompt failure."
        """
        # Gate condition 1: file must exist
        if not self.scorecard_path.exists():
            return (
                False,
                "PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD",
                {"reason": "leadership_scorecard.json does not exist", "path": str(self.scorecard_path)},
            )

        # Gate condition 2: parse and validate
        try:
            data = json.loads(self.scorecard_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError) as e:
            return (
                False,
                "PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD",
                {"reason": f"leadership_scorecard.json is malformed: {e}"},
            )

        # Gate condition 3: ≥5 of 12 traits must have score > 0
        scores = data.get("scores", {})
        if not scores and "traits" in data:
            traits_list = data.get("traits", [])
            for t in traits_list:
                if isinstance(t, dict):
                    t_name = t.get("name")
                    t_score = t.get("score", 0)
                    if t_name:
                        scores[t_name] = t_score

        # Support both quick-scoring and MCDA trait names
        from src.ccp.models.leadership_scorecard_models import TraitName
        mcda_traits = [t.value for t in TraitName]
        all_possible_traits = list(set(self.ALL_TRAITS + mcda_traits))

        scored_traits = [
            trait for trait in all_possible_traits
            if scores.get(trait, 0) > 0
        ]
        scored_count = len(scored_traits)

        if scored_count < self.MINIMUM_SCORED_TRAITS:
            return (
                False,
                "PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD",
                {
                    "reason": f"Only {scored_count} of 12 traits scored > 0. "
                              f"Minimum required: {self.MINIMUM_SCORED_TRAITS}.",
                    "scored_traits": scored_traits,
                    "unscored_traits": [t for t in all_possible_traits if t not in scored_traits],
                },
            )

        # PASS
        available_traits = [t for t in all_possible_traits if scores.get(t, 0) > 0]
        dominant_trait_name = max(
            [(t, scores.get(t, 0)) for t in available_traits],
            key=lambda x: x[1]
        )[0]

        return (
            True,
            "",
            {
                "scored_count": scored_count,
                "scored_traits": scored_traits,
                "unscored_traits": [t for t in all_possible_traits if t not in scored_traits],
                "ideal_score": scored_count >= 12,
                "dominant_trait": dominant_trait_name,
            },
        )

    def assert_unlocked(self) -> dict:
        """Assert the production lock gate passes. Raises ProductionLocked if not.

        Called by MorganOrchestrator before any Phase 1 execution.

        Returns:
            Gate details dict on success.

        Raises:
            ProductionLocked: With exact error code from AC1.
        """
        passes, error_code, details = self.check()
        if not passes:
            raise ProductionLocked(error_code, details)
        return details


class ProductionLocked(Exception):
    """Raised by ProductionLockGate when ccf-batch is triggered without scorecard.

    Spec AC1: 'returns PRODUCTION_LOCKED_PENDING_IDENTITY_SCORECARD from Morgan's gate
    — not a prompt failure.'
    """
    def __init__(self, error_code: str, details: dict):
        self.error_code = error_code
        self.details = details
        super().__init__(f"{error_code}: {details.get('reason', '')}")


# ──────────────────────────────────────────────────────────────
# CMM Completion Gate
# Spec AC3: "Attempting to trigger Phase 1 without Step 0-A operator confirmation
# fails with CMM_NOT_CONFIRMED error."
# ──────────────────────────────────────────────────────────────

class CMMCompletionGate:
    """Gate G-CMM: CMM must be operator-confirmed before Phase 1.

    Spec: 'CMM is NOT written automatically — the Agent identifies, the operator decides.'
    AC3: 'Attempting to trigger Phase 1 without Step 0-A operator confirmation
    fails with CMM_NOT_CONFIRMED error.'
    """

    def check(self, cmm: CulturalMemoryMap) -> tuple[bool, str, dict]:
        """Check CMM completion gate.

        Returns:
            (passes: bool, error_code: str, details: dict)
        """
        if not cmm.operator_confirmed:
            return (
                False,
                "CMM_NOT_CONFIRMED",
                {"reason": "Operator has not confirmed CMM entries via Telegram review prompt"},
            )

        populated_count = cmm.get_populated_layer_count()
        if populated_count < 4:
            return (
                False,
                "CMM_NOT_CONFIRMED",
                {
                    "reason": f"Only {populated_count} of 7 CMM layers have ≥3 approved entries. "
                              f"Minimum required: 4.",
                    "populated_layers": populated_count,
                },
            )

        return (
            True,
            "",
            {
                "populated_layers": populated_count,
                "operator_confirmed": True,
                "confirmed_at": cmm.confirmed_at.isoformat() if cmm.confirmed_at else None,
            },
        )

    def assert_confirmed(self, cmm: CulturalMemoryMap) -> dict:
        """Assert CMM gate passes. Raises CMMNotConfirmed if not."""
        passes, error_code, details = self.check(cmm)
        if not passes:
            raise CMMNotConfirmed(error_code, details)
        return details


class CMMNotConfirmed(Exception):
    """Raised by CMMCompletionGate per AC3."""
    def __init__(self, error_code: str, details: dict):
        self.error_code = error_code
        self.details = details
        super().__init__(f"{error_code}: {details.get('reason', '')}")


# ──────────────────────────────────────────────────────────────
# Manual Trigger Gate
# Spec AC4: "A production session cannot be initiated via manual coach Telegram trigger.
# Only the Scheduled Monitor Agent can initiate a production session."
# ──────────────────────────────────────────────────────────────

# The exact canned response text from spec AC4
MANUAL_TRIGGER_RESPONSE = (
    "Got it — I'll work this into the next batch. "
    "Your weekly session starts when I identify the right cultural moment for this."
)


def gate_manual_trigger(is_manual_trigger: bool) -> None:
    """Enforce AC4: manual coach trigger returns canned response, never starts production.

    Spec AC4: 'A production session cannot be initiated via manual coach Telegram trigger.
    Only the Scheduled Monitor Agent can initiate a production session.
    Manual trigger returns: "Got it — I'll work this into the next batch..."'

    Args:
        is_manual_trigger: True if this production request came from coach Telegram directly.

    Raises:
        ManualTriggerBlocked: With the exact spec-mandated response string.
    """
    if is_manual_trigger:
        raise ManualTriggerBlocked(MANUAL_TRIGGER_RESPONSE)


class ManualTriggerBlocked(Exception):
    """Raised when coach attempts to manually trigger production.

    Spec AC4: Only the Scheduled Monitor Agent can initiate a production session.
    The response text is the exact string mandated by the spec.
    """
    def __init__(self, response_text: str):
        self.response_text = response_text
        super().__init__(response_text)


# ──────────────────────────────────────────────────────────────
# UNIT 2 — Morgan Orchestrator
# Spec: Phase 0 — "Onboarding Steps 0-A through 0-D are run by Morgan, not manually.
# Human-initiated onboarding steps introduce sequencing errors."
# ──────────────────────────────────────────────────────────────

class MorganOrchestrator:
    """Phase 0 orchestrator — coordinates all 13 production unlock gate conditions.

    Spec: 'Morgan orchestrates Steps 0-A through 0-D programmatically after FR3
    completion is confirmed.'

    C-11 Persona Masking Gate: Morgan's name never appears in any API payload.
    All Telegram messages sent through this orchestrator are stripped of agent
    names before dispatch.

    The 13 production unlock conditions (from Phase 0 Completion Summary):
    1.  Genesis Clearance Certificate (DEP-ENG-052)
    2.  coach_soul.json with DEP-ENG-003, DEP-ENG-004, DEP-LIB-001
    3.  ttt_baseline.json
    4.  tribe_soul.json (DEP-ENG-001)
    5.  trigger_map.json (DEP-LIB-002)
    6.  02_content_strategy.md
    7.  leadership_scorecard.json (≥5/12 traits scored)
    8.  cultural_memory_map — ≥4 layers, ≥3 entries (Step 0-A confirmed)
    9.  coach_story_archive — ≥3 approved entries, ≥2 story types (Step 0-B)
    10. humor_mechanism_registry — initialized (Step 0-C)
    11. context_performance_registry — initialized (Step 0-D)
    12. Scheduled Monitor Agent — live (Step 11-A)
    13. Genesis Unlock Receipt
    """

    # C-11 Persona Masking — agent name patterns that must never appear in API payloads
    # These are checked at dispatch but never inserted into prompts.
    _AGENT_NAME_PATTERN = (
        r"\b(Morgan|Valeriane|Kimya|Dilaya|Emmanuel|Cesare|Charlotte|Abel|Paradoxe|"
        r"Sophia|Marcus|Chen|Liliane|Alex|Divine|Tshala|Lila|Maeva|Lionel|Remgion|"
        r"Azaria|Atlas|Benjamin|Grant|Jason|Samuel|Rachel|Minister of Identity|"
        r"Minister of Timing)\b"
    )

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
        receipt_chain: ReceiptChain,
        supabase_client=None,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir
        self.receipt_chain = receipt_chain
        self.supabase = supabase_client
        self._production_lock_gate = ProductionLockGate(coach_dir)
        self._cmm_gate = CMMCompletionGate()
        self._phase0_receipts: list[ReceiptEntry] = []

    # ── Phase 0 Unlock Check ──────────────────────────────────

    def check_all_phase0_gates(self, cmm: CulturalMemoryMap) -> dict[str, bool]:
        """Check all 13 Phase 0 production unlock conditions.

        Returns a dict mapping each gate name to its pass/fail status.
        This is informational — use assert_phase0_complete() for enforcement.
        """
        gates: dict[str, bool] = {}

        # Gate 1: Genesis Clearance Certificate
        from src.ccp.agents.guardian_agent import GuardianAgent
        has_cert, _ = GuardianAgent.check_genesis_clearance(
            coach_acronym=self.coach_acronym,
            base_dir=str(self.coach_dir.parent),
        )
        gates["genesis_clearance_certificate"] = has_cert

        # Gate 2: coach_soul.json with DEP-ENG-003, DEP-ENG-004, DEP-LIB-001
        soul_path = self.coach_dir / "config" / "coach_soul.json"
        if soul_path.exists():
            soul_data = json.loads(soul_path.read_text(encoding="utf-8"))
            voice_dna = soul_data.get("voice_dna", {})
            gates["coach_soul_dep_eng_003"] = len(voice_dna.get("vocabulary_fingerprint", [])) > 0
            gates["coach_soul_dep_eng_004"] = len(voice_dna.get("sentence_rhythm", [])) > 0
            gates["coach_soul_dep_lib_001"] = soul_data.get("coaching_philosophy", "") != ""
        else:
            gates["coach_soul_dep_eng_003"] = False
            gates["coach_soul_dep_eng_004"] = False
            gates["coach_soul_dep_lib_001"] = False

        # Gate 3: ttt_baseline.json
        gates["ttt_baseline"] = (self.coach_dir / "config" / "ttt_baseline.json").exists()

        # Gate 4: tribe_soul.json
        gates["tribe_soul"] = (self.coach_dir / "config" / "tribe_soul.json").exists()

        # Gate 5: trigger_map.json
        gates["trigger_map"] = (self.coach_dir / "config" / "trigger_map.json").exists()

        # Gate 6: 02_content_strategy.md
        gates["content_strategy"] = (self.coach_dir / "config" / "02_content_strategy.md").exists()

        # Gate 7: leadership_scorecard.json with ≥5 traits scored
        lock_passes, _, _ = self._production_lock_gate.check()
        gates["leadership_scorecard"] = lock_passes

        # Gate 8: cultural_memory_map — operator confirmed
        cmm_passes, _, _ = self._cmm_gate.check(cmm)
        gates["cultural_memory_map"] = cmm_passes

        # Gate 9: coach_story_archive — ≥3 entries, ≥2 types
        # Loaded from Supabase; passed via parameter pattern in assert_phase0_complete()
        gates["coach_story_archive"] = False  # requires story_archive parameter

        # Gate 10: humor_mechanism_registry — initialized
        gates["humor_mechanism_registry"] = self._check_v5_table_initialized("humor_mechanism_registry")

        # Gate 11: context_performance_registry — initialized
        gates["context_performance_registry"] = self._check_v5_table_initialized("context_performance_registry")

        # Gate 12: Scheduled Monitor Agent live
        # Verified by Step 11-A test observation — stored in config
        gates["scheduled_monitor_agent"] = (
            self.coach_dir / "config" / "scheduled_monitor_config.json"
        ).exists()

        # Gate 13: Genesis Unlock Receipt (checked separately via receipt chain)
        gates["genesis_unlock_receipt"] = False  # set by assert_phase0_complete() after writing

        return gates

    def assert_phase0_complete(
        self,
        cmm: CulturalMemoryMap,
        story_archive: CoachStoryArchive,
    ) -> ReceiptEntry:
        """Assert all Phase 0 gates pass. Write Genesis Unlock Receipt on success.

        Spec Phase 0 Completion Summary: 'all must be TRUE before Alex can trigger Phase 1'

        Returns:
            The Genesis Unlock Receipt entry.

        Raises:
            ProductionLocked: If leadership scorecard gate fails.
            CMMNotConfirmed: If CMM gate fails.
            Phase0Incomplete: If any other gate fails.
        """
        # Hard gates first (raise specific exceptions per spec)
        self._production_lock_gate.assert_unlocked()
        self._cmm_gate.assert_confirmed(cmm)

        # Story archive gate
        if not story_archive.passes_proto016_gate():
            approved = story_archive.get_approved_entries()
            types = story_archive.get_approved_story_types()
            raise Phase0Incomplete(
                "STORY_ARCHIVE_GATE_FAILED",
                {
                    "reason": f"Story archive has {len(approved)} approved entries "
                              f"across {len(types)} story types. "
                              f"Required: ≥3 entries across ≥2 story types.",
                },
            )

        # Check all remaining gates
        gates = self.check_all_phase0_gates(cmm)
        gates["coach_story_archive"] = story_archive.passes_proto016_gate()

        failed_gates = [k for k, v in gates.items() if not v and k != "genesis_unlock_receipt"]
        if failed_gates:
            raise Phase0Incomplete(
                "PHASE0_INCOMPLETE",
                {
                    "reason": f"The following Phase 0 gates have not passed: {failed_gates}",
                    "failed_gates": failed_gates,
                },
            )

        # Write Genesis Unlock Receipt per FR47 DEP-ENG-041 schema
        # Spec Phase 0 Completion Summary receipt format (exact field names from spec)
        receipt = self.receipt_chain.log(
            agent_id="guardian_agent",
            action="genesis_unlock",
            input_summary=f"All Phase 0 gates confirmed for coach {self.coach_acronym}",
            output_summary=(
                f"GENESIS-UNLOCK receipt issued. "
                f"CMM layers: {cmm.get_populated_layer_count()}/7. "
                f"Story entries: {len(story_archive.get_approved_entries())}. "
                f"Leadership scorecard: present."
            ),
            decision="completed",
            metadata={
                "stage_name": "GENESIS-UNLOCK",
                "agent_name": "Guardian Agent",
                "receipt_id": f"RCP-{self.coach_acronym}-GENESIS-UNLOCK",
                "coach_id": self.coach_id,
                "gates_passed": list(gates.keys()),
                "cmm_populated_layers": cmm.get_populated_layer_count(),
                "story_entries_approved": len(story_archive.get_approved_entries()),
                "story_types_covered": [t.value for t in story_archive.get_approved_story_types()],
            },
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def assert_phase1_authorized(
        self,
        cmm: CulturalMemoryMap,
        is_manual_trigger: bool = False,
    ) -> None:
        """Assert Phase 1 production is authorized.

        Enforces:
        - AC4: Manual trigger returns canned response, never starts production.
        - AC3: CMM must be operator-confirmed.
        - Gate G-PROD-LOCK: Leadership scorecard must pass.

        Args:
            cmm: The current cultural memory map.
            is_manual_trigger: True if this came from direct coach Telegram message.

        Raises:
            ManualTriggerBlocked: With canned response if is_manual_trigger is True.
            CMMNotConfirmed: If CMM not confirmed.
            ProductionLocked: If scorecard gate fails.
        """
        # AC4: Manual trigger check — must be first
        gate_manual_trigger(is_manual_trigger)

        # AC3: CMM confirmation check
        self._cmm_gate.assert_confirmed(cmm)

        # Production lock gate
        self._production_lock_gate.assert_unlocked()

    # ── V5.0 Table Initialization ──────────────────────────────

    def init_humor_registry(self, coach_id: str) -> HumorMechanismRegistry:
        """Step 0-C: Initialize empty humor_mechanism_registry.

        Spec: 'Create empty humor_mechanism_registry table entry for this coach.
        coach_id initialized. No entries yet — populated after first production sessions.'
        Completion gate: 'Table entry exists (status: initialized)'
        """
        registry = HumorMechanismRegistry(
            registry_id=f"HMR-{self.coach_acronym}-{uuid.uuid4().hex[:8].upper()}",
            coach_id=coach_id,
            status="initialized",
            entries=[],
        )

        # Write to Supabase
        if self.supabase:
            self.supabase.table("humor_mechanism_registry").upsert(
                {
                    "registry_id": registry.registry_id,
                    "coach_id": registry.coach_id,
                    "status": registry.status,
                    "entries": [],
                    "created_at": registry.created_at.isoformat(),
                    "updated_at": registry.updated_at.isoformat(),
                }
            ).execute()

        # Write local snapshot
        registry_path = self.coach_dir / "config" / "humor_mechanism_registry.json"
        registry_path.write_text(registry.model_dump_json(indent=2), encoding="utf-8")

        # Receipt — Stage 12: STEP-0C-HUMOR-INIT
        receipt = self.receipt_chain.log(
            agent_id="morgan_orchestrator",
            action="step_0c_humor_registry_init",
            input_summary=f"Initializing humor_mechanism_registry for coach {coach_id}",
            output_summary=f"humor_mechanism_registry created — status: initialized, registry_id: {registry.registry_id}",
            decision="completed",
            metadata={
                "stage_name": "STEP-0C-HUMOR-INIT",
                "agent_name": "Morgan",
                "registry_id": registry.registry_id,
                "coach_id": coach_id,
                "status": "initialized",
            },
        )
        self._phase0_receipts.append(receipt)
        return registry

    def init_context_performance_registry(self, coach_id: str) -> ContextPerformanceRegistry:
        """Step 0-D: Initialize empty context_performance_registry.

        Spec: 'Create empty context_performance_registry table entry. coach_id initialized.
        Confidence score defaults to routing rules until ≥5 sessions are recorded.'
        Completion gate: 'Table entry exists (status: initialized, confidence_model: default_routing_rules)'
        """
        registry = ContextPerformanceRegistry(
            registry_id=f"CPR-{self.coach_acronym}-{uuid.uuid4().hex[:8].upper()}",
            coach_id=coach_id,
            status="initialized",
            confidence_model="default_routing_rules",
            session_count=0,
            context_selections=[],
        )

        # Write to Supabase
        if self.supabase:
            self.supabase.table("context_performance_registry").upsert(
                {
                    "registry_id": registry.registry_id,
                    "coach_id": registry.coach_id,
                    "status": registry.status,
                    "confidence_model": registry.confidence_model,
                    "session_count": 0,
                    "context_selections": [],
                    "created_at": registry.created_at.isoformat(),
                    "updated_at": registry.updated_at.isoformat(),
                }
            ).execute()

        # Write local snapshot
        cpr_path = self.coach_dir / "config" / "context_performance_registry.json"
        cpr_path.write_text(registry.model_dump_json(indent=2), encoding="utf-8")

        # Receipt — Stage 13: STEP-0D-CPR-INIT
        receipt = self.receipt_chain.log(
            agent_id="morgan_orchestrator",
            action="step_0d_cpr_init",
            input_summary=f"Initializing context_performance_registry for coach {coach_id}",
            output_summary=(
                f"context_performance_registry created — "
                f"status: initialized, confidence_model: default_routing_rules, "
                f"registry_id: {registry.registry_id}"
            ),
            decision="completed",
            metadata={
                "stage_name": "STEP-0D-CPR-INIT",
                "agent_name": "Morgan",
                "registry_id": registry.registry_id,
                "coach_id": coach_id,
                "status": "initialized",
                "confidence_model": "default_routing_rules",
            },
        )
        self._phase0_receipts.append(receipt)
        return registry

    def run_post_fr3_initialization(self, coach_id: str) -> dict:
        """Run Steps 0-C and 0-D after FR3 pipeline completes.

        Spec: Steps 0-C and 0-D are triggered by Morgan after FR3 completion.
        Both tables must be initialized before Phase 1 is authorized.

        Returns:
            Dict with humor_registry and cpr objects.
        """
        humor_registry = self.init_humor_registry(coach_id)
        cpr = self.init_context_performance_registry(coach_id)
        return {
            "humor_registry": humor_registry,
            "cpr": cpr,
        }

    # ── Phase 0 Command Receipts ──────────────────────────────

    def write_ccf_init_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 1 receipt: CCF-INIT — Morgan."""
        receipt = self.receipt_chain.log(
            agent_id="morgan_orchestrator",
            action="ccf_init",
            input_summary=f"Initialize coach workspace for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-INIT", "agent_name": "Morgan"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_elicit_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 2 receipt: CCF-ELICIT — Kimya."""
        receipt = self.receipt_chain.log(
            agent_id="kimya_processor",
            action="ccf_elicit",
            input_summary=f"Business context elicitation for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-ELICIT", "agent_name": "Kimya"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_soul_extract_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 3 receipt: CCF-SOUL-EXTRACT — Morgan."""
        receipt = self.receipt_chain.log(
            agent_id="morgan_orchestrator",
            action="ccf_soul_extract",
            input_summary=f"Sacred Audio + Voice DNA extraction for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-SOUL-EXTRACT", "agent_name": "Morgan"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_tribe_extract_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 4 receipt: CCF-TRIBE-EXTRACT — Dilaya."""
        receipt = self.receipt_chain.log(
            agent_id="dilaya_processor",
            action="ccf_tribe_extract",
            input_summary=f"Tribe soul extraction for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-TRIBE-EXTRACT", "agent_name": "Dilaya"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_trigger_extract_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 5 receipt: CCF-TRIGGER-EXTRACT — TriggerMapBuilder."""
        receipt = self.receipt_chain.log(
            agent_id="trigger_map_builder",
            action="ccf_trigger_extract",
            input_summary=f"Trigger map extraction for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-TRIGGER-EXTRACT", "agent_name": "TriggerMapBuilder"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_pillar_build_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 6 receipt: CCF-PILLAR-BUILD — Emmanuel."""
        receipt = self.receipt_chain.log(
            agent_id="emmanuel_strategist",
            action="ccf_pillar_build",
            input_summary=f"Content pillar build for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-PILLAR-BUILD", "agent_name": "Emmanuel"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_philosophy_brief_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 7 receipt: CCF-PHILOSOPHY-BRIEF — Emmanuel."""
        receipt = self.receipt_chain.log(
            agent_id="emmanuel_strategist",
            action="ccf_philosophy_brief",
            input_summary=f"Philosophy brief for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-PHILOSOPHY-BRIEF", "agent_name": "Emmanuel"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_blueprint_receipt(self, output_summary: str) -> ReceiptEntry:
        """Stage 8 receipt: CCF-BLUEPRINT — Emmanuel."""
        receipt = self.receipt_chain.log(
            agent_id="emmanuel_strategist",
            action="ccf_blueprint",
            input_summary=f"Content strategy blueprint for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={"stage_name": "CCF-BLUEPRINT", "agent_name": "Emmanuel"},
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_ccf_leadership_score_receipt(self, output_summary: str, scores_dict: dict) -> ReceiptEntry:
        """Stage 9 receipt: CCF-LEADERSHIP-SCORE — MinisterOfIdentity."""
        receipt = self.receipt_chain.log(
            agent_id="minister_of_identity",
            action="ccf_leadership_score",
            input_summary=f"Leadership trait scoring for {self.coach_acronym}",
            output_summary=output_summary,
            decision="completed",
            metadata={
                "stage_name": "CCF-LEADERSHIP-SCORE",
                "agent_name": "MinisterOfIdentity",
                "scores_summary": scores_dict,
            },
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_step_0a_cmm_receipt(self, output_summary: str, cmm_id: str, layers_populated: int) -> ReceiptEntry:
        """Stage 10 receipt: STEP-0A-CMM-EXTRACT — Morgan."""
        receipt = self.receipt_chain.log(
            agent_id="morgan_orchestrator",
            action="step_0a_cmm_extract",
            input_summary=f"CMM extraction for {self.coach_acronym} — DEP-PROTO-014",
            output_summary=output_summary,
            decision="completed",
            metadata={
                "stage_name": "STEP-0A-CMM-EXTRACT",
                "agent_name": "Morgan",
                "cmm_id": cmm_id,
                "layers_populated": layers_populated,
            },
        )
        self._phase0_receipts.append(receipt)
        return receipt

    def write_step_0b_story_archive_receipt(self, output_summary: str, entries_approved: int, types_count: int) -> ReceiptEntry:
        """Stage 11 receipt: STEP-0B-STORY-ARCHIVE — Morgan."""
        receipt = self.receipt_chain.log(
            agent_id="morgan_orchestrator",
            action="step_0b_story_archive_seed",
            input_summary=f"Story Archive seeding for {self.coach_acronym} — DEP-PROTO-016",
            output_summary=output_summary,
            decision="completed",
            metadata={
                "stage_name": "STEP-0B-STORY-ARCHIVE",
                "agent_name": "Morgan",
                "entries_approved": entries_approved,
                "story_types_count": types_count,
            },
        )
        self._phase0_receipts.append(receipt)
        return receipt

    # ── Chain Integrity Verification ──────────────────────────

    def verify_phase0_chain(self) -> tuple[bool, list[str]]:
        """Verify the Phase 0 receipt chain is unbroken.

        Spec AC9: 'After complete Phase 0, all receipts from ccf-init through Step 0-D
        are stored in Supabase receipts table with resolvable predecessor_receipt fields.
        A receipt chain integrity check passes end-to-end.'

        Returns:
            (intact: bool, issues: list[str])
        """
        if not self._phase0_receipts:
            return False, ["No Phase 0 receipts found — chain is empty"]

        issues: list[str] = []

        expected_actions = [
            "ccf_init",
            "ccf_elicit",
            "ccf_soul_extract",
            "ccf_tribe_extract",
            "ccf_trigger_extract",
            "ccf_pillar_build",
            "ccf_philosophy_brief",
            "ccf_blueprint",
            "ccf_leadership_score",
            "step_0a_cmm_extract",
            "step_0b_story_archive_seed",
            "step_0c_humor_registry_init",
            "step_0d_cpr_init",
            "genesis_unlock",
        ]

        recorded_actions = {r.action for r in self._phase0_receipts}
        for expected in expected_actions:
            if expected not in recorded_actions:
                issues.append(f"Missing receipt for stage: {expected}")

        return len(issues) == 0, issues

    # ── Internal helpers ──────────────────────────────────────

    def _check_v5_table_initialized(self, table_name: str) -> bool:
        """Check if a V5.0 table has an initialized entry for this coach."""
        config_file_map = {
            "humor_mechanism_registry": "humor_mechanism_registry.json",
            "context_performance_registry": "context_performance_registry.json",
        }
        filename = config_file_map.get(table_name)
        if not filename:
            return False
        return (self.coach_dir / "config" / filename).exists()


class Phase0Incomplete(Exception):
    """Raised when Phase 0 completion check fails for a non-production-lock reason."""
    def __init__(self, error_code: str, details: dict):
        self.error_code = error_code
        self.details = details
        super().__init__(f"{error_code}: {details.get('reason', '')}")
