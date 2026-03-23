"""
CCP Step 7 — Context Premise Adapter (Adapter-3, Unit 2)
Loads DEP-ENG-006 (TribeProfileDistilled / macro audience Context Premise Map)
into SKILL.md Block B for JIT compilation.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0 — Adapter-3 "Graph context"
    FR6_Tribe_Profile_Context_Premise_Map_Tech_Spec.md — DEP-ENG-006 schema
    FR9_Audience_Empathy_Agent_Tech_Spec.md — theme-specific enrichment

IMPORTANT DISTINCTION:
    DEP-ENG-006 = macro audience Context Premise Map (from FR6/FR9) — THIS adapter
    DEP-ENG-030 = 1:1 client Context Premise Map (from FR13 Neo4j) — NOT this adapter
    These are architecturally distinct. This adapter ONLY reads DEP-ENG-006.

Block B injection produces:
    1. L3 pain domain coordinates for the generation agent's awareness
    2. Tribal language terms the generation agent MUST use
    3. Hidden belief summaries for structural depth targeting
    4. Enemy typology for shared-enemy arc construction
    5. Segment-specific depth distribution context

ADR-01: coach_id scopes all operations.
FR47:   Receipt written per DEP-ENG-041 schema on successful injection.
M-02:   No TTT hardcoded values in output strings.
"""

from __future__ import annotations

from typing import Any

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import (
    AdapterRunResult,
    AdapterSlot,
    BlockBInjection,
    BlockTarget,
)
from src.ccp.models.adapter_registry_v2_models import ContextPremiseAdapterOutput
from src.ccp.models.tribe_profile_models import (
    ContextPremiseDimension,
    DepthLevel,
    TribeProfileDistilled,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "Context-Premise-Adapter"
STAGE_ADAPTER = "ADAPTER-CONTEXT-PREMISE-BLOCK-B"
ADAPTER_SLOT = AdapterSlot.CONTEXT_PREMISE


# ─── L3 Extraction Helpers ────────────────────────────────────────────────────

def _extract_l3_entries(dimension: ContextPremiseDimension) -> list[str]:
    """Extract all L3-depth entry texts from a Context Premise dimension."""
    results: list[str] = []
    for entry in dimension.entries:
        if hasattr(entry, "depth") and entry.depth == DepthLevel.L3:
            if hasattr(entry, "text") and entry.text:
                results.append(entry.text)
    return results


def _extract_tribal_terms(profile: TribeProfileDistilled) -> list[str]:
    """Extract verified tribal language terms from the profile's segments."""
    terms: list[str] = []
    for segment in profile.segments:
        if hasattr(segment, "tribal_terms"):
            for term in segment.tribal_terms:
                if isinstance(term, str) and term not in terms:
                    terms.append(term)
        if hasattr(segment, "language_registry"):
            reg = segment.language_registry
            if hasattr(reg, "entries"):
                for entry in reg.entries:
                    term_text = getattr(entry, "term", "")
                    if term_text and term_text not in terms:
                        terms.append(term_text)
    return terms


def _extract_enemy_labels(profile: TribeProfileDistilled) -> list[str]:
    """Extract shared enemy labels from the enemies dimension."""
    labels: list[str] = []
    for entry in profile.enemies.entries:
        text = getattr(entry, "text", "")
        if text and text not in labels:
            labels.append(text)
    return labels


def _extract_hidden_belief_summaries(profile: TribeProfileDistilled) -> list[str]:
    """Extract hidden belief summaries from the hidden_beliefs dimension."""
    summaries: list[str] = []
    for entry in profile.hidden_beliefs.entries:
        text = getattr(entry, "text", "")
        if text and text not in summaries:
            summaries.append(text)
    return summaries


def _compute_depth_distribution(profile: TribeProfileDistilled) -> dict[str, float]:
    """Compute the L1/L2/L3 depth distribution from the profile."""
    dd = profile.depth_distribution
    return {
        "l1_pct": getattr(dd, "l1_percentage", 0.0),
        "l2_pct": getattr(dd, "l2_percentage", 0.0),
        "l3_pct": getattr(dd, "l3_percentage", 0.0),
    }


# ─── Constraint String Builders ───────────────────────────────────────────────

def _build_l3_pain_constraints(l3_domains: list[str]) -> list[str]:
    """Build constraint strings from L3 pain domains."""
    constraints: list[str] = []
    if l3_domains:
        domain_text = "; ".join(l3_domains[:10])  # Cap at 10 for token budget
        constraints.append(
            f"CONSTRAINT (Context Premise — L3 Pain Domains): "
            f"The audience's deepest verified pain coordinates include: {domain_text}. "
            f"Ground emotional payload in these specific L3 domains, not generic equivalents."
        )
    return constraints


def _build_tribal_language_constraints(terms: list[str]) -> list[str]:
    """Build constraint strings mandating tribal language usage."""
    constraints: list[str] = []
    if terms:
        term_text = ", ".join(terms[:15])  # Cap at 15 for token budget
        constraints.append(
            f"CONSTRAINT (Context Premise — Tribal Language): "
            f"The following verified tribal terms MUST appear in the output "
            f"(minimum 3 per section): {term_text}. "
            f"Generic marketing vocabulary is FORBIDDEN — use the audience's own words."
        )
    return constraints


def _build_enemy_constraints(enemies: list[str]) -> list[str]:
    """Build constraint strings from shared enemy typology."""
    constraints: list[str] = []
    if enemies:
        enemy_text = "; ".join(enemies[:5])
        constraints.append(
            f"CONSTRAINT (Context Premise — Shared Enemy Typology): "
            f"The audience's shared enemies: {enemy_text}. "
            f"Arc construction must position these as structural antagonists, "
            f"not metaphorical obstacles."
        )
    return constraints


def _build_hidden_belief_constraints(beliefs: list[str]) -> list[str]:
    """Build constraint strings from hidden beliefs."""
    constraints: list[str] = []
    if beliefs:
        belief_text = "; ".join(beliefs[:5])
        constraints.append(
            f"CONSTRAINT (Context Premise — Hidden Beliefs): "
            f"The audience holds these unspoken beliefs: {belief_text}. "
            f"Content must acknowledge these without directly naming them. "
            f"The reader should feel recognized, not called out."
        )
    return constraints


def _build_depth_distribution_constraint(dist: dict[str, float]) -> list[str]:
    """Build constraint string from depth distribution."""
    l3_pct = dist.get("l3_pct", 0.0)
    constraints: list[str] = []
    if l3_pct >= 0.10:
        constraints.append(
            f"CONSTRAINT (Context Premise — Depth Permission): "
            f"Audience L3 depth verified at {l3_pct:.0%}. "
            f"L3 emotional payload is AUTHORIZED for this audience segment. "
            f"Approach with specificity, not softening."
        )
    else:
        constraints.append(
            f"CONSTRAINT (Context Premise — Depth Limitation): "
            f"Audience L3 depth at {l3_pct:.0%} — below verification threshold. "
            f"Restrict emotional depth to L2 level. Do NOT attempt L3 payload delivery."
        )
    return constraints


# ─── Adapter Engine ───────────────────────────────────────────────────────────

class ContextPremiseAdapter:
    """Adapter-3 — Reads DEP-ENG-006 (TribeProfileDistilled) and emits
    audience context constraints for SKILL.md Block B injection.

    CCP_Technical_Architecture.md §4: Mandatory for ALL CCF script skills.

    This adapter extracts:
    - L3 pain domain coordinates
    - Tribal language terms (mandatory usage in output)
    - Hidden belief summaries
    - Enemy typology
    - Depth distribution context

    ADR-01: coach_id scopes all operations.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def load(
        self,
        context_premise: TribeProfileDistilled,
        coach_id: str,
        theme: str = "",
    ) -> AdapterRunResult:
        """Load DEP-ENG-006 and produce Block B injection.

        Args:
            context_premise: The TribeProfileDistilled (DEP-ENG-006) artifact.
            coach_id: ADR-01 tenant isolation identifier.
            theme: Optional content theme for filtering.

        Returns:
            AdapterRunResult with Block B injection payload.
        """
        gate_failures: list[str] = []
        warnings: list[str] = []

        # ── Validate DEP-ENG-006 ──────────────────────────────────
        if context_premise is None:
            gate_failures.append("DEP-ENG-006 Context Premise Map is None — cannot proceed.")
            return AdapterRunResult(
                adapter_slot=ADAPTER_SLOT,
                coach_id=coach_id,
                success=False,
                gate_failures=gate_failures,
            )

        if context_premise.dep_id != "DEP-ENG-006":
            gate_failures.append(
                f"Expected DEP-ENG-006, got dep_id={context_premise.dep_id}. "
                f"DEP-ENG-030 (1:1 client map from FR13) is NOT valid here."
            )
            return AdapterRunResult(
                adapter_slot=ADAPTER_SLOT,
                coach_id=coach_id,
                success=False,
                gate_failures=gate_failures,
            )

        # ── Extract L3 pain domains ───────────────────────────────
        l3_domains: list[str] = []
        for dim_name in [
            "frustrations", "fears", "insecurities",
            "suspicions", "envy_feelings", "enemies",
        ]:
            dim = getattr(context_premise, dim_name, None)
            if dim is not None:
                l3_domains.extend(_extract_l3_entries(dim))

        # ── Extract tribal terms ──────────────────────────────────
        tribal_terms = _extract_tribal_terms(context_premise)

        # ── Extract enemy typology ────────────────────────────────
        enemy_labels = _extract_enemy_labels(context_premise)

        # ── Extract hidden beliefs ────────────────────────────────
        hidden_beliefs = _extract_hidden_belief_summaries(context_premise)

        # ── Compute depth distribution ────────────────────────────
        depth_dist = _compute_depth_distribution(context_premise)

        # ── Validation warnings ───────────────────────────────────
        if len(tribal_terms) < 10:
            warnings.append(
                f"Tribal term count ({len(tribal_terms)}) below Law 3 minimum (10). "
                f"Generated content may lack subcortical recognition signal."
            )

        if not l3_domains:
            warnings.append(
                "No L3 pain domains extracted from DEP-ENG-006. "
                "Content depth will be limited to L2."
            )

        # ── Build constraint strings ──────────────────────────────
        constraints: list[str] = []
        constraints.extend(_build_l3_pain_constraints(l3_domains))
        constraints.extend(_build_tribal_language_constraints(tribal_terms))
        constraints.extend(_build_enemy_constraints(enemy_labels))
        constraints.extend(_build_hidden_belief_constraints(hidden_beliefs))
        constraints.extend(_build_depth_distribution_constraint(depth_dist))

        # ── Build adapter output ──────────────────────────────────
        adapter_output = ContextPremiseAdapterOutput(
            coach_id=coach_id,
            theme=theme,
            l3_pain_domains=l3_domains[:10],
            tribal_terms=tribal_terms,
            segment_count=len(context_premise.segments),
            depth_distribution=depth_dist,
            enemy_typology=enemy_labels,
            hidden_belief_summaries=hidden_beliefs,
            constraint_strings=constraints,
        )

        # ── Build Block B injection ───────────────────────────────
        block_b = BlockBInjection(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            target=BlockTarget.BLOCK_B,
            section_header="## Context Premise Intelligence (Adapter-3 — DEP-ENG-006)",
            constraint_strings=constraints,
            metadata={
                "dep_id": "DEP-ENG-006",
                "l3_domain_count": len(l3_domains),
                "tribal_term_count": len(tribal_terms),
                "segment_count": len(context_premise.segments),
                "enemy_count": len(enemy_labels),
                "hidden_belief_count": len(hidden_beliefs),
                "depth_distribution": depth_dist,
                "theme": theme,
            },
        )

        # ── Receipt write ─────────────────────────────────────────
        entry = self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=(
                f"DEP-ENG-006 coach={coach_id}, segments={len(context_premise.segments)}, "
                f"theme={theme or 'unspecified'}"
            ),
            output_summary=(
                f"Block B injection: {len(constraints)} constraints, "
                f"L3 domains={len(l3_domains)}, tribal_terms={len(tribal_terms)}, "
                f"enemies={len(enemy_labels)}, hidden_beliefs={len(hidden_beliefs)}"
            ),
            metadata={
                "stage_name": STAGE_ADAPTER,
                "coach_id": coach_id,
                "adapter_slot": ADAPTER_SLOT.value,
                "theme": theme,
                "l3_domain_count": len(l3_domains),
                "tribal_term_count": len(tribal_terms),
            },
        )

        return AdapterRunResult(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            success=True,
            block_b=block_b,
            receipt_id=entry.receipt_id,
            warnings=warnings,
        )
