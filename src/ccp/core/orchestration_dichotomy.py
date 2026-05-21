from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from src.ccp.core.primitive_schemas import (
    CoalitionSignature,
    EdgeProduct,
    PrimitiveCandidate,
    PrimitiveFamily,
)

ANTI_CENTROID_EMOTIONAL_CHARGE_FLOOR = 0.3
EVIDENCE_FIDELITY_MINIMUM = 0.6
EVIDENCE_MINIMUM_COUNT = 2
FAMILY_DIVERSITY_MINIMUM = 2
MAX_DSPY_RETRIES = 2


class DualSourceValidationError(Exception):
    """Raised when a primitive fails YAML registry or PRD module validation."""
    pass


class DichotomyGateRejection(Exception):
    """Raised when the Dichotomy Gate rejects LLM output."""
    def __init__(self, reason: str, details: str = "") -> None:
        self.reason = reason
        self.details = details
        super().__init__(f"{reason}: {details}")


class DualSourceValidator:
    """Validates each PrimitiveCandidate against the YAML registry.
    PRD module source alignment is validated at build-time."""

    def __init__(self, primitives_base_path: str = "primitives") -> None:
        self._base_path = Path(primitives_base_path)

    def validate_candidate(self, candidate: PrimitiveCandidate) -> bool:
        """Cross-reference the candidate's primitive_id with the YAML registry.
        Returns True if the primitive exists in the registry, False otherwise."""
        primitive_id = candidate.primitive_id
        parts = primitive_id.split("-")
        if len(parts) != 3 or parts[0] != "PRM":
            raise DualSourceValidationError(
                f"Invalid primitive_id format: '{primitive_id}'. Must follow PRM-XXX-NNN (ADR-05)."
            )

        # Map family code to directory path
        family_code = parts[1].upper()
        family_dir_map: dict[str, list[str]] = {
            "STR": ["experience/structural"],
            "TNS": ["experience/tension"],
            "IDN": ["experience/identity"],
            "CMP": ["experience/compression"],
            "EMO": ["experience/emotional"],
            "FBK": ["experience/feedback_scoring"],
            "PRG": ["experience/progression"],
            "TRS": ["experience/trust_branding"],
            "PER": ["experience/personalization_identity"],
            "FRC": ["experience/friction_ability"],
        }
        search_dirs = family_dir_map.get(family_code, [])

        for search_dir in search_dirs:
            yaml_path = self._base_path / search_dir / f"{primitive_id}.yaml"
            if yaml_path.exists():
                return True

        # If no exact match found, search all yaml files for the ID
        for yaml_file in self._base_path.rglob("*.yaml"):
            try:
                content = yaml_file.read_text(encoding="utf-8")
                if f"id: \"{primitive_id}\"" in content or f"id: '{primitive_id}'" in content or f"id: {primitive_id}" in content:
                    return True
            except Exception:
                continue

        raise DualSourceValidationError(
            f"Primitive '{primitive_id}' not found in YAML registry. ADR-05 violation."
        )


class PrimitiveExtractor:
    """DSPy module wrapper for primitive candidate extraction.
    Uses TypedPredictor for structured output enforcement."""

    def __init__(self, dspy_client: Any = None) -> None:
        self._dspy_client = dspy_client

    def extract(self, transcript: str, research_context: str) -> list[PrimitiveCandidate]:
        """Extract PrimitiveCandidates from transcript using DSPy.
        Retries up to MAX_DSPY_RETRIES on validation failure.
        Returns empty list on exhausted retries."""
        candidates: list[PrimitiveCandidate] = []

        if self._dspy_client is not None:
            for attempt in range(MAX_DSPY_RETRIES + 1):
                try:
                    raw_result = self._dspy_client.predict(
                        transcript=transcript,
                        research_context=research_context,
                    )
                    if hasattr(raw_result, "candidates"):
                        for raw_candidate in raw_result.candidates:
                            if isinstance(raw_candidate, PrimitiveCandidate):
                                candidates.append(raw_candidate)
                            elif isinstance(raw_candidate, dict):
                                candidates.append(PrimitiveCandidate(**raw_candidate))
                    if candidates:
                        return candidates
                except Exception:
                    if attempt >= MAX_DSPY_RETRIES:
                        return []
                    continue

        return candidates


class DichotomyGate:
    """The hard boundary between creative DSPy/LLM output and the deterministic pipeline.
    Validates PrimitiveCandidates through Anti-Centroid, Evidence Minimum,
    Family Diversity, and Dual-Source Validation checks.
    On failure: loads last validated coalition from coalition_history (fallback)."""

    def __init__(
        self,
        supabase_client: Any = None,
        receipt_chain: Any = None,
        dual_source_validator: DualSourceValidator | None = None,
    ) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._dual_source_validator = dual_source_validator or DualSourceValidator()

    def validate(
        self,
        candidates: list[PrimitiveCandidate],
        coach_id: str,
    ) -> list[PrimitiveCandidate]:
        """Run all gate checks on candidates. Returns validated candidates.
        Raises DichotomyGateRejection on failure."""

        if not candidates:
            raise DichotomyGateRejection(
                reason="NO_CANDIDATES",
                details="No primitive candidates provided to the Dichotomy Gate.",
            )

        # Anti-Centroid Gate: If ALL candidates have emotional_charge < 0.3, reject
        if all(c.emotional_charge < ANTI_CENTROID_EMOTIONAL_CHARGE_FLOOR for c in candidates):
            raise DichotomyGateRejection(
                reason="CENTROID_DRIFT_DETECTED",
                details=f"All {len(candidates)} candidates have emotional_charge < {ANTI_CENTROID_EMOTIONAL_CHARGE_FLOOR}. Output is too safe.",
            )

        # Evidence Minimum: At least 2 candidates must have evidence_fidelity >= 0.6
        high_evidence_count = sum(1 for c in candidates if c.evidence_fidelity >= EVIDENCE_FIDELITY_MINIMUM)
        if high_evidence_count < EVIDENCE_MINIMUM_COUNT:
            raise DichotomyGateRejection(
                reason="EVIDENCE_MINIMUM_NOT_MET",
                details=f"Only {high_evidence_count} candidates have evidence_fidelity >= {EVIDENCE_FIDELITY_MINIMUM}. Need at least {EVIDENCE_MINIMUM_COUNT}.",
            )

        # Family Diversity: Candidates must span at least 2 different PrimitiveFamily values
        unique_families = set(c.family for c in candidates)
        if len(unique_families) < FAMILY_DIVERSITY_MINIMUM:
            raise DichotomyGateRejection(
                reason="FAMILY_DIVERSITY_NOT_MET",
                details=f"Only {len(unique_families)} unique families. Need at least {FAMILY_DIVERSITY_MINIMUM}.",
            )

        # Dual-Source Validation: Each candidate must cross-reference its primitive_id with YAML registry
        for candidate in candidates:
            try:
                self._dual_source_validator.validate_candidate(candidate)
            except DualSourceValidationError as e:
                raise DichotomyGateRejection(
                    reason="DUAL_SOURCE_VALIDATION_FAILED",
                    details=str(e),
                )

        return candidates

    def load_fallback(self, coach_id: str) -> dict | None:
        """Load the last validated coalition for this coach from coalition_history."""
        if self._supabase is not None:
            result = self._supabase.table("coalition_history").select("*").eq(
                "coach_id", coach_id
            ).eq("validation_status", "validated").order("created_at", desc=True).limit(1).execute()
            if result and hasattr(result, "data") and result.data:
                return result.data[0]
        return None

    def log_rejection(self, coach_id: str, reason: str, details: str) -> None:
        """Log a gate rejection to receipt chain and optionally to coalition_history."""
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="dichotomy-gate-rejected", metadata={
                "coach_id": coach_id,
                "reason": reason,
                "details": details,
            })
