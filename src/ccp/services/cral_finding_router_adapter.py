"""
CCP Step 7 — CRAL Finding Router Adapter (Adapter-8, Unit 4)
Routes DEP-ENG-021 CRAL findings to correct arc phases for Block B injection.

Architecture reference:
    CCP_Evolution_Architecture_Report_V4 §3.3 — cral-finding-router-adapter
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0 — Adapter-8

Arc Phase Routing Map (V4 §3.3):
    Stakes      → M2_BELIEVABLE + M3_UNDENIABLE
    Mechanism   → M4_RESONANT
    Turn        → M5_SURPRISING
    Result      → M6_IRREFUTABLE
    Implication → M7_RELATABLE
    (M1_TIMELY is a pre-condition check, not injected into an arc phase.)

Block B injection produces:
    1. Per-phase CRAL finding constraints keyed to arc phase entry points
    2. Degraded-phase warnings where findings are absent (CRAL_DEGRADED)
    3. Human evidence counts per finding (FR16 gate: ≥3 named humans required)

Activation rule:
    This adapter is CONDITIONAL — activated only when DEP-ENG-021 is available.
    When DEP-ENG-021 absent, adapter returns success with CRAL_DEGRADED status.
    Partial CRAL findings (< 7 moments) produce per-phase degradation.

Graceful degradation:
    DEP-ENG-021 (CRAL Finding Index) is produced by CRAL Orchestrator (FR14, Step 11).
    Until Step 11 is BUILT, this adapter ALWAYS runs in CRAL_DEGRADED mode.
    The rest of the pipeline continues — CRAL enrichment is additive, not blocking.

ADR-01: coach_id scopes all operations.
FR47:   Receipt written per DEP-ENG-041 schema on successful injection.
M-02:   No TTT hardcoded values in output strings.
"""

from __future__ import annotations

from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import (
    AdapterRunResult,
    AdapterSlot,
    BlockBInjection,
    BlockTarget,
)
from src.ccp.models.adapter_registry_v2_models import (
    ArcPhase,
    ArcPhaseInjection,
    CRALFindingIndex,
    CRALFindingRouterOutput,
    CRALMomentKey,
    STORYTELLING_ARC_PHASE_ROUTING,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "CRAL-Finding-Router-Adapter"
STAGE_ADAPTER = "ADAPTER-CRAL-FINDING-ROUTER-BLOCK-B"
ADAPTER_SLOT = AdapterSlot.CRAL_FINDING_ROUTER

# Minimum human evidence count for FR16 gate compliance
FR16_MIN_HUMAN_EVIDENCE = 3


# ─── Per-Phase Injection Builder ──────────────────────────────────────────────

def _build_phase_injection_text(
    arc_phase: ArcPhase,
    moment_key: CRALMomentKey,
    finding_text: str,
    human_evidence_count: int,
) -> str:
    """Build the injection text for a single CRAL finding at a specific arc phase.

    The injection text is structured as a generation constraint:
    it tells Emilio WHERE in the arc to deploy this research finding
    and HOW MANY named human evidence instances back it.
    """
    evidence_tag = (
        f"[{human_evidence_count} named human evidence instances]"
        if human_evidence_count >= FR16_MIN_HUMAN_EVIDENCE
        else f"[CAUTION: {human_evidence_count} evidence instances — below FR16 threshold of {FR16_MIN_HUMAN_EVIDENCE}]"
    )

    return (
        f"ARC PHASE [{arc_phase.value}] — {moment_key.value} Research Finding: "
        f"{finding_text} {evidence_tag}"
    )


# ─── M1 Timeliness Pre-Condition Check ───────────────────────────────────────

def _check_m1_timeliness(
    cral_index: CRALFindingIndex,
) -> tuple[bool, list[str]]:
    """Check M1_TIMELY pre-condition from the CRAL Finding Index.

    M1_TIMELY is not injected into an arc phase — it validates the topic's
    relevance window before compilation begins. If M1 is missing or has
    degraded quality, emit a warning but do NOT block compilation.

    Returns:
        (timely, warnings) — timely=True if M1 passes or is absent.
    """
    warnings: list[str] = []
    m1 = cral_index.get_finding(CRALMomentKey.M1_TIMELY)

    if m1 is None:
        warnings.append(
            "CRAL M1_TIMELY finding absent — timeliness pre-condition cannot be verified. "
            "Content may lack cultural relevance signal. Proceed with caution."
        )
        return True, warnings  # Non-blocking

    if m1.source_quality == "degraded":
        warnings.append(
            f"CRAL M1_TIMELY quality=degraded: \"{m1.finding_text[:80]}...\". "
            f"Timeliness signal is weak — consider refreshing CRAL research."
        )

    return True, warnings


# ─── Route All Findings ──────────────────────────────────────────────────────

def _route_findings_to_phases(
    cral_index: CRALFindingIndex,
    routing_map: dict[ArcPhase, list[CRALMomentKey]],
) -> tuple[list[ArcPhaseInjection], list[str], list[str]]:
    """Route CRAL findings to their target arc phases per the routing map.

    Returns:
        (injections, degraded_phases, warnings)
    """
    injections: list[ArcPhaseInjection] = []
    degraded_phases: list[str] = []
    warnings: list[str] = []

    for arc_phase, moment_keys in routing_map.items():
        phase_has_injection = False

        for moment_key in moment_keys:
            finding = cral_index.get_finding(moment_key)

            if finding is None:
                warnings.append(
                    f"CRAL_DEGRADED: {moment_key.value} finding missing for "
                    f"arc phase [{arc_phase.value}]. "
                    f"Generation proceeds without this research constraint."
                )
                continue

            # FR16 evidence count warning
            if finding.human_evidence_count < FR16_MIN_HUMAN_EVIDENCE:
                warnings.append(
                    f"FR16 WARNING: {moment_key.value} has only "
                    f"{finding.human_evidence_count} named human evidence instances "
                    f"(minimum {FR16_MIN_HUMAN_EVIDENCE} required for full authority)."
                )

            injection_text = _build_phase_injection_text(
                arc_phase=arc_phase,
                moment_key=moment_key,
                finding_text=finding.finding_text,
                human_evidence_count=finding.human_evidence_count,
            )

            injections.append(ArcPhaseInjection(
                arc_phase=arc_phase,
                moment_key=moment_key,
                injection_text=injection_text,
                quality=finding.source_quality,
            ))
            phase_has_injection = True

        if not phase_has_injection:
            degraded_phases.append(arc_phase.value)

    return injections, degraded_phases, warnings


# ─── Constraint String Builder ────────────────────────────────────────────────

def _build_cral_constraints(
    output: CRALFindingRouterOutput,
) -> list[str]:
    """Build constraint strings from the CRAL router output."""
    constraints: list[str] = []

    # Coverage status header
    if output.coverage_status == "COMPLETE":
        constraints.append(
            "CONSTRAINT (CRAL Research — COMPLETE Coverage): "
            "All arc phases have verified CRAL research findings. "
            "Each phase MUST incorporate its assigned finding as structural evidence."
        )
    else:
        constraints.append(
            f"CONSTRAINT (CRAL Research — DEGRADED Coverage): "
            f"Some arc phases lack CRAL findings ({', '.join(output.degraded_phases)}). "
            f"Use available findings where present; proceed without research constraint "
            f"for degraded phases."
        )

    # Per-phase injection constraints
    for injection in output.phase_injections:
        constraints.append(
            f"CONSTRAINT ({injection.arc_phase.value} Phase — "
            f"{injection.moment_key.value}): {injection.injection_text}"
        )

    return constraints


# ─── Adapter Engine ───────────────────────────────────────────────────────────

class CRALFindingRouterAdapter:
    """Adapter-8 — Routes DEP-ENG-021 CRAL findings to arc phases for Block B.

    CCP_Evolution_Architecture_Report_V4 §3.3:
        'CRAL findings are not injected flat — each finding is routed to the
        specific arc phase where it has maximum structural authority.'

    Conditional adapter — activated only when DEP-ENG-021 is available.
    When absent: adapter returns success with CRAL_DEGRADED advisory.

    Graceful degradation:
        - DEP-ENG-021 absent → full CRAL_DEGRADED (no research constraints)
        - DEP-ENG-021 partial → per-phase degradation with available findings
        - DEP-ENG-021 complete → full research constraint injection

    ADR-01: coach_id scopes all operations.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def load(
        self,
        coach_id: str,
        archetype_id: str = "",
        cral_finding_index: Optional[CRALFindingIndex] = None,
    ) -> AdapterRunResult:
        """Route CRAL findings to arc phases and produce Block B injection.

        Args:
            coach_id: ADR-01 tenant isolation identifier.
            archetype_id: Archetype family for routing map selection.
            cral_finding_index: Optional DEP-ENG-021 from CRAL Orchestrator.

        Returns:
            AdapterRunResult with Block B injection payload.
        """
        warnings: list[str] = []

        # ── Full CRAL_DEGRADED — DEP-ENG-021 absent ──────────────
        if cral_finding_index is None:
            warnings.append(
                "CRAL_DEGRADED: DEP-ENG-021 (CRAL Finding Index) not available. "
                "This is expected until Step 11 (CRAL Orchestrator) is BUILT. "
                "Compilation proceeds without CRAL research constraints."
            )

            entry = self._rc.log(
                agent_id=AGENT_ADAPTER,
                action=STAGE_ADAPTER,
                input_summary=f"coach={coach_id} — DEP-ENG-021 ABSENT (CRAL_DEGRADED)",
                output_summary="No-op: full CRAL_DEGRADED — no findings to route.",
                metadata={
                    "stage_name": STAGE_ADAPTER,
                    "coach_id": coach_id,
                    "adapter_slot": ADAPTER_SLOT.value,
                    "cral_degraded": True,
                    "coverage_status": "DEGRADED",
                },
            )

            return AdapterRunResult(
                adapter_slot=ADAPTER_SLOT,
                coach_id=coach_id,
                success=True,  # Graceful degradation is NOT a failure
                receipt_id=entry.receipt_id,
                warnings=warnings,
            )

        # ── M1 Timeliness pre-condition ───────────────────────────
        _, m1_warnings = _check_m1_timeliness(cral_finding_index)
        warnings.extend(m1_warnings)

        # ── Route findings to arc phases ──────────────────────────
        # Default: storytelling arc phase routing map (V4 §3.3)
        # Future: archetype_id could select different routing maps
        routing_map = STORYTELLING_ARC_PHASE_ROUTING

        injections, degraded_phases, routing_warnings = _route_findings_to_phases(
            cral_index=cral_finding_index,
            routing_map=routing_map,
        )
        warnings.extend(routing_warnings)

        # ── Determine coverage status ─────────────────────────────
        coverage_status = "COMPLETE" if not degraded_phases else "DEGRADED"

        # ── Build adapter output ──────────────────────────────────
        output = CRALFindingRouterOutput(
            coach_id=coach_id,
            archetype_id=archetype_id,
            phase_injections=injections,
            degraded_phases=degraded_phases,
            coverage_status=coverage_status,
            constraint_strings=[],  # Populated below
        )

        # ── Build constraints ─────────────────────────────────────
        constraints = _build_cral_constraints(output)
        output.constraint_strings = constraints

        # ── Build Block B injection ───────────────────────────────
        block_b = BlockBInjection(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            target=BlockTarget.BLOCK_B,
            section_header="## CRAL Research Intelligence (Adapter-8 — Arc Phase Routing)",
            constraint_strings=constraints,
            metadata={
                "dep_id": "DEP-ENG-021",
                "archetype_id": archetype_id,
                "coverage_status": coverage_status,
                "phase_injection_count": len(injections),
                "degraded_phase_count": len(degraded_phases),
                "degraded_phases": degraded_phases,
                "routing_map": "STORYTELLING_ARC_PHASE_ROUTING",
            },
        )

        # ── Receipt write ─────────────────────────────────────────
        entry = self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=(
                f"coach={coach_id}, archetype={archetype_id or 'unspecified'}, "
                f"cral_theme={cral_finding_index.theme}, "
                f"cral_coverage={cral_finding_index.coverage_status}"
            ),
            output_summary=(
                f"Block B injection: {len(constraints)} constraints, "
                f"phase_injections={len(injections)}, "
                f"degraded_phases={len(degraded_phases)}, "
                f"coverage={coverage_status}"
            ),
            metadata={
                "stage_name": STAGE_ADAPTER,
                "coach_id": coach_id,
                "adapter_slot": ADAPTER_SLOT.value,
                "archetype_id": archetype_id,
                "coverage_status": coverage_status,
                "phase_injection_count": len(injections),
                "degraded_phases": degraded_phases,
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
