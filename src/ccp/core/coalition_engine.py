from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from src.ccp.core.primitive_schemas import (
    CoalitionSignature,
    EdgeProduct,
    PrimitiveCandidate,
)

# Scoring weights from Stage 4 Step 1
WEIGHT_EVIDENCE_FIDELITY = 0.3
WEIGHT_EMOTIONAL_CHARGE = 0.25
WEIGHT_TRIBAL_DENSITY = 0.2
WEIGHT_SPEAKABILITY = 0.25

COALITION_MINIMUM_CANDIDATES = 2
COALITION_MAXIMUM_CANDIDATES = 5

FATALITY_DELTA_THRESHOLD = -40.0  # >40% below 8-week rolling average

# Edge product type mapping by dominant primitive family code
EDGE_PRODUCT_TYPE_MAP: dict[str, str] = {
    "TNS": "transformation-pressure-edge",
    "STR": "narrative-structure-edge",
    "IDN": "identity-crystallization-edge",
    "CMP": "compression-urgency-edge",
    "EMO": "emotional-resonance-edge",
}


def calculate_combined_score(candidate: PrimitiveCandidate) -> float:
    """Calculate the combined score for a PrimitiveCandidate using the spec-defined weights."""
    return (
        candidate.evidence_fidelity * WEIGHT_EVIDENCE_FIDELITY
        + candidate.emotional_charge * WEIGHT_EMOTIONAL_CHARGE
        + candidate.tribal_density * WEIGHT_TRIBAL_DENSITY
        + candidate.speakability * WEIGHT_SPEAKABILITY
    )


class CoalitionEngine:
    """Combines validated primitives into weighted coalitions and produces EdgeProducts.
    Scoring: (evidence_fidelity * 0.3) + (emotional_charge * 0.25) + (tribal_density * 0.2) + (speakability * 0.25)."""

    def __init__(
        self,
        supabase_client: Any = None,
        receipt_chain: Any = None,
    ) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    def assemble(
        self,
        candidates: list[PrimitiveCandidate],
        coach_id: str,
    ) -> tuple[CoalitionSignature, EdgeProduct]:
        """Assemble a coalition from validated candidates.
        Raises ValueError if fewer than 2 candidates provided."""

        if len(candidates) < COALITION_MINIMUM_CANDIDATES:
            raise ValueError(
                f"Coalition minimum not met: {len(candidates)} candidates, need at least {COALITION_MINIMUM_CANDIDATES}."
            )

        # Step 1: Sort candidates by combined_score descending
        scored = [(c, calculate_combined_score(c)) for c in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)

        # Step 2: Select top 2-5 candidates
        selected = scored[:COALITION_MAXIMUM_CANDIDATES]
        selected_candidates = [c for c, _ in selected]

        # Step 3: Identify dominant primitive (highest combined_score)
        dominant_candidate, dominant_score = selected[0]
        dominant_primitive_id = dominant_candidate.primitive_id

        # Step 4: Calculate combined_force_score as weighted average
        total_score = sum(s for _, s in selected)
        combined_force_score = total_score / len(selected) if selected else 0.0
        combined_force_score = min(max(combined_force_score, 0.0), 1.0)

        # Step 5: Generate edge_product_type from dominant primitive's family code
        family_code = dominant_primitive_id.split("-")[1] if "-" in dominant_primitive_id else ""
        edge_product_type = EDGE_PRODUCT_TYPE_MAP.get(family_code, "generic-edge")

        # Step 6: Extract tension_object from dominant primitive
        tension_object = f"Conflict driven by {dominant_candidate.primitive_name}: {dominant_candidate.evidence_quote[:80]}"

        # Step 7: Calculate anti_centroid_score as inverse average of emotional_charge and speakability
        avg_emotional = sum(c.emotional_charge for c in selected_candidates) / len(selected_candidates)
        avg_speakability = sum(c.speakability for c in selected_candidates) / len(selected_candidates)
        anti_centroid_score = 1.0 - ((avg_emotional + avg_speakability) / 2.0)
        anti_centroid_score = min(max(anti_centroid_score, 0.0), 1.0)

        # Step 8: Build CoalitionSignature
        coalition_id = str(uuid4())
        coalition = CoalitionSignature(
            coalition_id=coalition_id,
            primitives=selected_candidates,
            dominant_primitive_id=dominant_primitive_id,
            combined_force_score=combined_force_score,
            edge_product_type=edge_product_type,
        )

        # Build EdgeProduct
        edge_id = str(uuid4())
        edge_product = EdgeProduct(
            edge_id=edge_id,
            coalition_id=coalition_id,
            tension_object=tension_object,
            ccf_routing_target=edge_product_type,
            cmf_routing_target=None,
            anti_centroid_score=anti_centroid_score,
        )

        # Step 9: Write to coalition_history with validation_status: 'validated'
        if self._supabase is not None:
            self._supabase.table("coalition_history").insert({
                "id": coalition_id,
                "coach_id": coach_id,
                "coalition_signature": coalition.model_dump(),
                "edge_product": edge_product.model_dump(),
                "primitive_candidates": [c.model_dump() for c in selected_candidates],
                "validation_status": "validated",
                "anti_centroid_score": anti_centroid_score,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }).execute()

        # Receipt chain
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="coalition-assembled", metadata={
                "coalition_id": coalition_id,
                "edge_id": edge_id,
                "dominant_primitive_id": dominant_primitive_id,
                "edge_product_type": edge_product_type,
                "combined_force_score": combined_force_score,
            })

        return coalition, edge_product


class CoalitionFatalityLogger:
    """Logs coalition fatalities when post-publication engagement falls >40%
    below the coach's rolling 8-week average."""

    def __init__(
        self,
        supabase_client: Any = None,
        receipt_chain: Any = None,
    ) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    def log_fatality(
        self,
        coalition_id: str,
        edge_product_id: str,
        expected_engagement: float,
        actual_engagement: float,
        diagnosis: str,
    ) -> None:
        """Record a coalition fatality when engagement delta exceeds threshold."""
        delta_percentage = ((actual_engagement - expected_engagement) / expected_engagement) * 100.0 if expected_engagement > 0 else 0.0

        if delta_percentage > FATALITY_DELTA_THRESHOLD:
            return  # Not a fatality — delta is within acceptable range

        if self._supabase is not None:
            self._supabase.table("coalition_fatalities").insert({
                "id": str(uuid4()),
                "coalition_id": coalition_id,
                "edge_product_id": edge_product_id,
                "expected_engagement": expected_engagement,
                "actual_engagement": actual_engagement,
                "delta_percentage": delta_percentage,
                "diagnosis": diagnosis,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }).execute()

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="coalition-fatality-logged", metadata={
                "coalition_id": coalition_id,
                "edge_product_id": edge_product_id,
                "delta_percentage": delta_percentage,
            })
