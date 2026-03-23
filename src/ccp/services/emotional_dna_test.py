"""
CCP FR3 Emotional DNA Integration Test — Unit 8
Mandate 7: Tests whether generated content activates the coach's wound architecture.

Spec reference: FR3 Tech Spec §Step 9 — Emotional DNA Integration Test (Mandate 7)
Agent: Valeriane + Charlotte (Stream of Consciousness Generator)

Prerequisite gate: DEP-LIB-001 must exist from FR4 execution.
BUILD_AMBIGUITY resolution: If DEP-LIB-001 is absent (FR4 not yet built),
Step 9 is SKIPPED (not failed) with receipt noting deferral.

Test criterion: 'Would someone who shares this coach's specific wound
architecture recognize their own experience in the first 30 words?'

Cycle: Up to 3 rewrites. If 3 cycles fail → flag for operator review.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Optional

from src.ccp.models.voice_dna_models import (
    MAX_MANDATE7_CYCLES,
    Mandate7TestResult,
    NegativeSpaceObject,
    PositiveSpaceObject,
)


class EmotionalDNAIntegrationTest:
    """Executes the Mandate 7 emotional DNA integration test.

    Spec §Step 9: 'Inject the coach's full DEP-LIB-001 wound architecture
    (L3 emotional layer: top moral foundation violation + trigger specificity
    threshold). Generate 3 opening sample sentences using DEP-ENG-003 +
    DEP-ENG-004 as constraints. Evaluate: do the samples activate the wound
    architecture rather than describe it?'

    Build Ambiguity Resolution:
    DEP-LIB-001 comes from FR4 (Emotional DNA Extraction), which may not be
    built yet. If absent, this step is SKIPPED with a receipt noting deferral.
    AC5 is verified with mock DEP-LIB-001 in tests.
    """

    def __init__(
        self,
        coach_dir: Optional[Path] = None,
        llm_client: Optional[Any] = None,
    ):
        """Initialize the integration test.

        Args:
            coach_dir: Coach instance directory (to locate DEP-LIB-001).
            llm_client: LLM client for Charlotte sample generation.
                If None, uses placeholder evaluation.
        """
        self.coach_dir = coach_dir
        self.llm_client = llm_client

    def test(
        self,
        positive_space: PositiveSpaceObject,
        negative_space: NegativeSpaceObject,
        dep_lib_001: Optional[dict] = None,
    ) -> Mandate7TestResult:
        """Execute Step 9: Emotional DNA Integration Test.

        Args:
            positive_space: DEP-ENG-003 from Steps 6-8.
            negative_space: DEP-ENG-004 from Step 5.
            dep_lib_001: Wound architecture from FR4. If None, attempts to
                load from coach_dir. If still None, step is SKIPPED.

        Returns:
            Mandate7TestResult with pass/fail/skip status.
        """
        # ── Prerequisite gate: DEP-LIB-001 ──
        wound_architecture = dep_lib_001 or self._load_dep_lib_001()

        if wound_architecture is None:
            return Mandate7TestResult(
                passed=False,
                cycles_used=0,
                skipped=True,
                skip_reason=(
                    "DEP-LIB-001 not found — FR4 (Emotional DNA Extraction) has not yet "
                    "executed. Step 9 is deferred until FR4 completes. This is a "
                    "prerequisite gate, not a failure."
                ),
            )

        # ── Mandate 7 evaluation cycles ──
        result = Mandate7TestResult()

        for cycle in range(1, MAX_MANDATE7_CYCLES + 1):
            result.cycles_used = cycle

            # Generate 3 opening samples using DEP-ENG-003 + DEP-ENG-004
            samples = self._generate_samples(
                positive_space, negative_space, wound_architecture, cycle
            )
            result.samples = samples

            # Evaluate: do samples activate the wound architecture?
            evaluation = self._evaluate_activation(
                samples, wound_architecture
            )
            result.evaluation_details.append(evaluation["detail"])

            if evaluation["passes_mandate_7"]:
                result.passed = True
                return result

            # Charlotte rewrite with deeper L3 activation instructions
            # (next cycle will use escalated prompts)

        # After 3 cycles without passing → operator review
        result.passed = False
        result.evaluation_details.append(
            f"MANDATE 7 NOT MET after {MAX_MANDATE7_CYCLES} cycles. "
            "Flag for operator review — corpus may not contain enough "
            "wound-level material. More Sacred Audio required."
        )
        return result

    def _load_dep_lib_001(self) -> Optional[dict]:
        """Attempt to load DEP-LIB-001 from coach directory.

        DEP-LIB-001 is produced by FR4 (Emotional DNA Extraction).
        If FR4 hasn't run yet, returns None → step SKIP.
        """
        if self.coach_dir is None:
            return None

        dep_lib_path = self.coach_dir / "config" / "dep_lib_001.json"
        if not dep_lib_path.exists():
            return None

        try:
            return json.loads(dep_lib_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def _generate_samples(
        self,
        positive_space: PositiveSpaceObject,
        negative_space: NegativeSpaceObject,
        wound_architecture: dict,
        cycle: int,
    ) -> list[str]:
        """Generate 3 opening sample sentences using DEPs as constraints.

        Spec §Step 9: 'Generate 3 opening sample sentences using DEP-ENG-003
        + DEP-ENG-004 as constraints.'
        """
        if self.llm_client is None:
            # Placeholder: return empty samples for testing
            return [
                f"[Sample {i+1}, cycle {cycle}] — LLM client not configured. "
                "Use test fixtures for AC5 verification."
                for i in range(3)
            ]

        # Build Charlotte's generation prompt
        prompt = self._build_charlotte_prompt(
            positive_space, negative_space, wound_architecture, cycle
        )

        # Call LLM for sample generation
        try:
            response = self.llm_client.generate(prompt)
            # Parse 3 samples from response
            samples = self._parse_samples(response)
            return samples[:3]
        except Exception:
            return [f"[Generation failed, cycle {cycle}]"] * 3

    def _build_charlotte_prompt(
        self,
        positive_space: PositiveSpaceObject,
        negative_space: NegativeSpaceObject,
        wound_architecture: dict,
        cycle: int,
    ) -> str:
        """Build Charlotte's (SoC Generator) prompt for sample generation."""
        # Extract wound details
        top_violation = wound_architecture.get("top_moral_foundation_violation", "unknown")
        trigger_threshold = wound_architecture.get("trigger_specificity_threshold", "unknown")
        l3_layer = wound_architecture.get("l3_emotional_layer", {})

        # Build voice constraints from DEP-ENG-003 prose
        voice_constraints = []
        for cluster in positive_space.clusters:
            if cluster.prose_description:
                voice_constraints.append(cluster.prose_description)

        # Build negative constraints from DEP-ENG-004
        neg_constraints = []
        for imp in negative_space.syntactic_impossibilities[:5]:
            neg_constraints.append(f"NEVER: {imp}")

        escalation = ""
        if cycle > 1:
            escalation = (
                f"\n\nESCALATION (cycle {cycle}): Previous samples did not activate "
                "the wound architecture. Go DEEPER into L3 emotional territory. "
                "Don't describe the wound — ACTIVATE it. The reader should feel "
                "a visceral recognition in the first 30 words."
            )

        return (
            f"You are Charlotte, the Stream of Consciousness Generator.\n\n"
            f"WOUND ARCHITECTURE:\n"
            f"- Top moral foundation violation: {top_violation}\n"
            f"- Trigger specificity: {trigger_threshold}\n"
            f"- L3 emotional layer: {json.dumps(l3_layer, indent=2)}\n\n"
            f"VOICE CONSTRAINTS (DEP-ENG-003):\n"
            f"{''.join(f'- {c}\n' for c in voice_constraints)}\n"
            f"NEGATIVE CONSTRAINTS (DEP-ENG-004):\n"
            f"{''.join(f'- {c}\n' for c in neg_constraints)}\n"
            f"TASK: Generate exactly 3 opening sentences (≤30 words each) that:\n"
            f"1. Would make someone with this wound architecture recognize their own experience\n"
            f"2. ACTIVATE the wound — don't describe it\n"
            f"3. Stay within the coach's voice DNA constraints\n"
            f"4. Do NOT violate any negative constraints\n"
            f"{escalation}\n\n"
            f"Output each sample on a separate line, prefixed with 'SAMPLE_1:', 'SAMPLE_2:', 'SAMPLE_3:'"
        )

    def _parse_samples(self, response: str) -> list[str]:
        """Parse 3 samples from LLM response."""
        samples = []
        for line in response.strip().split("\n"):
            line = line.strip()
            for prefix in ["SAMPLE_1:", "SAMPLE_2:", "SAMPLE_3:"]:
                if line.upper().startswith(prefix):
                    sample = line[len(prefix):].strip()
                    if sample:
                        samples.append(sample)
        return samples if samples else [response.strip()]

    def _evaluate_activation(
        self, samples: list[str], wound_architecture: dict
    ) -> dict:
        """Evaluate whether samples activate the wound architecture.

        Spec §Step 9: 'Would someone who shares this coach's specific wound
        architecture recognize their own experience in the first 30 words?'
        """
        if self.llm_client is None:
            # Without LLM, we can't evaluate activation
            # Return a conservative "pass" for testing with mock data
            return {
                "passes_mandate_7": False,
                "detail": (
                    "Evaluation skipped — no LLM client configured. "
                    "Cannot assess wound activation without AI evaluation. "
                    "Use mock DEP-LIB-001 in tests for AC5 verification."
                ),
            }

        # Build evaluation prompt
        wound_desc = json.dumps(wound_architecture, indent=2)
        samples_text = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(samples))

        eval_prompt = (
            f"You are evaluating whether these opening sentences would make "
            f"someone with the following wound architecture recognize their "
            f"own experience in the first 30 words.\n\n"
            f"WOUND ARCHITECTURE:\n{wound_desc}\n\n"
            f"SAMPLES:\n{samples_text}\n\n"
            f"CRITERION: Does at least one sample ACTIVATE (not describe) "
            f"the wound? Would the reader feel visceral recognition?\n\n"
            f"Respond with exactly: PASS or FAIL, followed by a brief explanation."
        )

        try:
            response = self.llm_client.generate(eval_prompt)
            passes = response.strip().upper().startswith("PASS")
            return {
                "passes_mandate_7": passes,
                "detail": response.strip(),
            }
        except Exception as e:
            return {
                "passes_mandate_7": False,
                "detail": f"Evaluation error: {e}",
            }
