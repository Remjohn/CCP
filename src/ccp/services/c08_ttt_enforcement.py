"""
CCP FR8 TTT Enforcement Rule — C-08 TTT Enforcement Check (Unit 3)
JIT Skill Assembler v2.0 Tier 0 pre-flight check C-08.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md §Layer 2: Compilation Enforcement
                §Detection Algorithm (3 phases)

Three detection phases:
  Phase 1: Explicit TTT field name detection (field name pattern matching)
  Phase 2: Implicit TTT value detection (value string regex scanning)
  Phase 3: Block A structural law secondary scan

AC1: Block B field ttt_temperature: "TTT-06" → REJECT TTT_HARDCODED_IN_BLOCK_B
AC2: Block B field_9 "maintain warm register at TTT-04" → REJECT TTT_VALUE_EMBEDDED_IN_BLOCK_B
AC3: Block A structural law "The Hook must hit TTT-08" → REJECT TTT_DIRECTIVE_IN_BLOCK_A
AC4: Block A Field 4 natural affinity range advisory → PASS
AC5: Block B field emotional_heat: 7 → REJECT (alias detection)
AC6: REJECT = zero tokens, zero adapter invocations, zero section assemblies
"""

from src.ccp.models.ttt_models import (
    BlockALaw,
    BlockBField,
    C08Result,
    C08Status,
    C08ViolationType,
    CompiledDesignBrief,
    TTTViolation,
)
from src.ccp.services.ttt_pattern_registry import (
    field_name_matches_ttt_pattern,
    is_rhythm_whitelisted,
    value_contains_ttt_pattern,
)


class C08TTTEnforcement:
    """Block C Check C-08 — TTT Enforcement Gate.

    Runs at JIT Skill Assembler v2.0 Tier 0 (zero tokens, zero generation).

    Spec §Check definition:
      Check: C-08
      Name: TTT Enforcement
      Pass Condition: No hardcoded TTT value in any Block B field
      Failure Behaviour: REJECT — TTT is never a compilation variable

    MANDATE: M-02 (Script Generation Skill Type Guide v1.0)
    """

    CHECK_NAME = "C-08"
    MANDATE = "M-02"

    def run(self, brief: CompiledDesignBrief) -> C08Result:
        """Execute C-08 against a compiled Design Brief.

        Runs Phase 1 → Phase 2 → Phase 3 in sequence.
        On first violation detected, stops scanning and returns REJECT immediately
        (consistent with Tier 0 fail-fast behaviour — no assembly begins).

        Args:
            brief: The compiled Design Brief to scan.

        Returns:
            C08Result with PASS or REJECT status and full violation details.
        """
        violations: list[TTTViolation] = []

        # Phase 1: Explicit TTT field name detection
        phase1_violation = self._phase1_explicit_field_detection(brief.block_b_fields)
        if phase1_violation:
            violations.append(phase1_violation)
            return self._make_reject_result(brief.compilation_id, violations)

        # Phase 2: Implicit TTT value detection
        phase2_violation = self._phase2_implicit_value_detection(brief.block_b_fields)
        if phase2_violation:
            violations.append(phase2_violation)
            return self._make_reject_result(brief.compilation_id, violations)

        # Phase 3: Block A structural law secondary scan
        phase3_violation = self._phase3_block_a_law_scan(brief.block_a_structural_laws)
        if phase3_violation:
            violations.append(phase3_violation)
            return self._make_reject_result(brief.compilation_id, violations)

        # All phases passed
        return C08Result(
            status=C08Status.PASS,
            violations=[],
            tokens_consumed=0,
            adapter_invocations=0,
            section_assemblies=0,
            compilation_id=brief.compilation_id,
        )

    def _phase1_explicit_field_detection(
        self, block_b_fields: list[BlockBField]
    ) -> TTTViolation | None:
        """Phase 1: Scan all Block B field NAMES for TTT pattern matches.

        Spec §Phase 1:
        "Scan all Block B fields for fields named with TTT-related identifiers"
        "IF field.name MATCHES ANY TTT_FIELD_PATTERNS (case-insensitive):
           IF field.value IS a static value (not a DEP-ENG-005 reference):
             RETURN REJECT TTT_HARDCODED_IN_BLOCK_B"

        Exception: Rhythm/syntax fields from adapter-6 are whitelisted (AC4 analogue).
        Exception: Fields whose value is a DEP-ENG-005 reference are permitted.

        Returns:
            TTTViolation if a violation is found, None otherwise.
        """
        for field in block_b_fields:
            # Skip rhythm-whitelisted fields (Structural Mechanic exception)
            if is_rhythm_whitelisted(field.name):
                continue

            if not field_name_matches_ttt_pattern(field.name):
                continue

            # Field name matches — check if value is a DEP-ENG-005 reference
            value_str = str(field.value) if field.value is not None else ""
            if self._is_dep_eng_005_reference(value_str):
                continue  # Permitted: DEP-ENG-005 runtime reference

            # Static TTT value in a TTT-named field → Phase 1 violation
            return TTTViolation(
                check=self.CHECK_NAME,
                violation_type=C08ViolationType.HARDCODED_IN_BLOCK_B,
                violating_field=field.name,
                violating_value=value_str[:200] if value_str else None,  # Truncate for diagnostic
                matched_pattern="TTT_FIELD_PATTERNS",
                mandate_violated=self.MANDATE,
                recovery_instruction=(
                    f"Remove '{field.name}' from Block B. "
                    "TTT is never a compilation variable. "
                    "TTT is resolved at runtime via DEP-ENG-005 Authentication Certificate. "
                    "The template author must correct this field and resubmit."
                ),
            )
        return None

    def _phase2_implicit_value_detection(
        self, block_b_fields: list[BlockBField]
    ) -> TTTViolation | None:
        """Phase 2: Scan all Block B field VALUES for TTT scale references.

        Spec §Phase 2:
        "Scan all Block B field VALUES for TTT scale references"
        "FOR EACH value_string IN field.all_string_values(): IF matches TTT_VALUE_PATTERNS → REJECT"

        Exception: Rhythm/syntax whitelisted fields bypass this check.
        Exception: DEP-ENG-005 references are permitted.

        Returns:
            TTTViolation if a violation is found, None otherwise.
        """
        for field in block_b_fields:
            # Skip rhythm-whitelisted fields
            if is_rhythm_whitelisted(field.name):
                continue

            for value_string in field.all_string_values():
                if self._is_dep_eng_005_reference(value_string):
                    continue  # Permitted: DEP-ENG-005 runtime reference

                matched, pattern = value_contains_ttt_pattern(value_string)
                if matched:
                    return TTTViolation(
                        check=self.CHECK_NAME,
                        violation_type=C08ViolationType.VALUE_EMBEDDED_IN_BLOCK_B,
                        violating_field=field.name,
                        violating_value=value_string[:200],
                        matched_pattern=pattern,
                        mandate_violated=self.MANDATE,
                        recovery_instruction=(
                            f"TTT value detected in Block B field '{field.name}'. "
                            "TTT is resolved at runtime via DEP-ENG-005 only. "
                            "Remove the specific TTT value or scale reference from this field."
                        ),
                    )
        return None

    def _phase3_block_a_law_scan(
        self, structural_laws: list[BlockALaw]
    ) -> TTTViolation | None:
        """Phase 3: Block A structural law secondary scan.

        Spec §Phase 3:
        "Block A should contain TTT affinity range as ADVISORY only"
        "IF law.text CONTAINS TTT_VALUE_PATTERNS:
           IF NOT law.context == 'natural_affinity_range_advisory':
             RETURN REJECT TTT_DIRECTIVE_IN_BLOCK_A"

        AC4: Natural affinity range advisory references in Block A Field 4 MUST pass.

        Returns:
            TTTViolation if a violation is found, None otherwise.
        """
        for law in structural_laws:
            # Natural affinity range advisories are PERMITTED (AC4)
            if law.is_affinity_advisory:
                continue

            matched, pattern = value_contains_ttt_pattern(law.text)
            if matched:
                return TTTViolation(
                    check=self.CHECK_NAME,
                    violation_type=C08ViolationType.DIRECTIVE_IN_BLOCK_A,
                    violating_field=f"block_a.structural_laws.{law.law_id}",
                    violating_value=law.text[:200],
                    matched_pattern=pattern,
                    mandate_violated=self.MANDATE,
                    recovery_instruction=(
                        f"TTT value found in Block A structural law '{law.law_id}'. "
                        "Only TTT natural affinity range (advisory) is permitted in Block A "
                        "(mark as context='natural_affinity_range_advisory'). "
                        "A TTT directive in a structural law encodes the value as invariant — "
                        "violating the Variants-vs-Invariants Test."
                    ),
                )
        return None

    def _make_reject_result(
        self, compilation_id: str | None, violations: list[TTTViolation]
    ) -> C08Result:
        """Create a C-08 REJECT result.

        Spec §AC6: Zero tokens consumed, zero adapter invocations, zero section assemblies.
        """
        return C08Result(
            status=C08Status.FAIL,
            violations=violations,
            tokens_consumed=0,      # AC6: pure logical check
            adapter_invocations=0,  # AC6
            section_assemblies=0,   # AC6
            compilation_id=compilation_id,
        )

    @staticmethod
    def _is_dep_eng_005_reference(value_str: str) -> bool:
        """Check if a field value is a DEP-ENG-005 reference (runtime resolution).

        Fields that reference DEP-ENG-005 are PERMITTED — they declare TTT will be
        resolved at runtime, not hardcoded.

        Args:
            value_str: String representation of the field value.

        Returns:
            True if the value is a DEP-ENG-005 runtime reference.
        """
        dep_markers = [
            "DEP-ENG-005",
            "dep-eng-005",
            "ttt_baseline",
            "authentication_certificate",
            "runtime_ttt",
            "${ttt}",
            "{{ttt}}",
        ]
        lower = value_str.lower()
        return any(marker.lower() in lower for marker in dep_markers)


def run_c08(brief: CompiledDesignBrief) -> C08Result:
    """Module-level convenience function to run C-08 on a compiled brief.

    Args:
        brief: The CompiledDesignBrief to check.

    Returns:
        C08Result with PASS or REJECT status.
    """
    return C08TTTEnforcement().run(brief)
