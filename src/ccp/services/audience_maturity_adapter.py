"""
CCP FR20 — Audience Maturity Adapter (Adapter 8)

JIT Skill Compiler adapter that reads DEP-ENG-017 and injects
depth constraint strings into SKILL.md Block B (Pre-Generation Constraints).

Spec reference: FR20_Audience_Maturity_Lifecycle_Tech_Spec.md §4 Stage 3

Architecture reference:
    JIT_Skill_Compiler_Architecture — Adapter 8 registry slot
"""

from __future__ import annotations

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.audience_maturity_models import (
    AudienceMaturityProfile,
    BroadenAndBuildStatus,
    DepthPermission,
    TMTFunctionAllowed,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "Audience-Maturity-Adapter"
STAGE_ADAPTER = "ADAPTER-COMPILATION-INJECTION"


# ─── Constraint String Templates ─────────────────────────────────────────────

_DEPTH_CONSTRAINT: dict[DepthPermission, str] = {
    DepthPermission.SURFACE: (
        "CONSTRAINT: Your depth_permission is currently <Surface>. "
        "Do not expand the Implication Phase into deep existential or systemic commentary."
    ),
    DepthPermission.MID: (
        "CONSTRAINT: Your depth_permission is currently <Mid>. "
        "The Implication Phase may connect to broader systemic issues "
        "but must not access deep existential or mortality-based roots."
    ),
    DepthPermission.FULL: (
        "CONSTRAINT: Your depth_permission is currently <Full>. "
        "The Implication Phase may access deep psychological and existential roots."
    ),
}

_TMT_CONSTRAINT: dict[TMTFunctionAllowed, str] = {
    TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY: (
        "CONSTRAINT: tmt_function_allowed is <insight_delivery_only>. "
        "Do not invoke worldview defense mechanics or mortality salience framing."
    ),
    TMTFunctionAllowed.WORLDVIEW_CONSTRUCTION_PERMITTED: (
        "CONSTRAINT: tmt_function_allowed is <worldview_construction_permitted>. "
        "Worldview construction and existential depth framing are authorised."
    ),
}

_BROADEN_BUILD_CONSTRAINT: dict[BroadenAndBuildStatus, str] = {
    BroadenAndBuildStatus.NOT_YET_SEEDED: (
        "CONSTRAINT: broaden_and_build_status is <Not_yet_seeded>. "
        "Prioritise positive affect priming (Escape/Discovery) before any Processing depth."
    ),
    BroadenAndBuildStatus.ACTIVE: (
        "CONSTRAINT: broaden_and_build_status is <Active>. "
        "Cognitive scope broadening is in progress — moderate Processing depth permitted."
    ),
    BroadenAndBuildStatus.MATURE: (
        "CONSTRAINT: broaden_and_build_status is <Mature>. "
        "Full Processing load permitted without burnout risk."
    ),
}


# ─── Adapter Engine ──────────────────────────────────────────────────────────


class AudienceMaturityAdapter:
    """Adapter 8 — Reads DEP-ENG-017 and emits constraint strings for Emilio.

    Each constraint string is a literal execution sentence appended to
    the SKILL.md Block B Pre-Generation Constraints section.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def compile_constraints(
        self,
        profile: AudienceMaturityProfile,
    ) -> list[str]:
        """Generate ordered constraint strings from the maturity profile.

        Args:
            profile: Validated DEP-ENG-017 output from the Maturity-Lifecycle-Engine.

        Returns:
            List of CONSTRAINT strings for SKILL.md Block B injection.
        """
        constraints: list[str] = [
            _DEPTH_CONSTRAINT[profile.depth_permission],
            _TMT_CONSTRAINT[profile.tmt_function_allowed],
            _BROADEN_BUILD_CONSTRAINT[profile.broaden_and_build_status],
            f"CONSTRAINT: batch_allocation = {profile.batch_allocation.model_dump()}. "
            f"Adhere to these proportions when structuring the batch composition.",
            f"CONSTRAINT: cohort_classification = <{profile.cohort_classification.value}>.",
        ]

        self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=f"profile_id={profile.profile_id} tenant={profile.tenant_id}",
            output_summary=f"constraints_count={len(constraints)}",
            metadata={
                "stage_name": STAGE_ADAPTER,
                "profile_id": profile.profile_id,
                "tenant_id": profile.tenant_id,
                "constraint_count": len(constraints),
            },
        )

        return constraints

    def format_block_b_section(
        self,
        profile: AudienceMaturityProfile,
    ) -> str:
        """Produce the full Block B Pre-Generation Constraints text block.

        Returns:
            Multi-line string ready for SKILL.md injection.
        """
        constraints = self.compile_constraints(profile)
        header = "## Pre-Generation Constraints (Adapter 8 — Audience Maturity)\n"
        body = "\n".join(f"- {c}" for c in constraints)
        return f"{header}\n{body}\n"
