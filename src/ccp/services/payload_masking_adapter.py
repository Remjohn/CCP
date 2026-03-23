"""
CCP Step 7 — Payload Masking Adapter (Adapter-6, Unit 3)
Generates Trojan Horse construction instruction per archetype × mood state
using Excitation Transfer (Zillmann 1971) + Mood Management Theory.

Architecture reference:
    CCP_Evolution_Architecture_Report_V3 §3.2 — payload-masking-adapter
    FR22_Anti_Draft_Intelligence_Tech_Spec.md §Stage 2 — Level 2 Generation
    FR18_Psychological_Routing_Brief_Tech_Spec.md — payload_masking_instruction

Block B injection produces:
    1. Mode-specific Trojan Horse structural instruction (Excitation Transfer)
    2. M3_UNDENIABLE subversion instruction (when DEP-ENG-021 available)
    3. Semantic Affinity Guard clearance status

Activation rule:
    This adapter is CONDITIONAL — activated only when mood_state ≠ Processing.
    Processing mode receives L3 payload directly (no masking needed).

Scientific basis:
    Escape:    Vehicle resolution subtext — truth is punchline, not lesson
    Discovery: Counter-intuitive entry point — competence reward before payload
    Status:    Comparison mechanism — what winners understood, never explicit lesson

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
    CRALFindingIndex,
    CRALMomentKey,
    PayloadMaskingAdapterOutput,
)
from src.ccp.models.psych_routing_models import MoodStatePrimary
from src.ccp.services.payload_masking_library import (
    get_payload_masking_instruction,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "Payload-Masking-Adapter"
STAGE_ADAPTER = "ADAPTER-PAYLOAD-MASKING-BLOCK-B"
ADAPTER_SLOT = AdapterSlot.PAYLOAD_MASKING


# ─── M3 Subversion Instruction Builder ────────────────────────────────────────

def _build_m3_subversion_instruction(
    m3_belief: str,
    mood_state: MoodStatePrimary,
) -> str:
    """Build the Level 2 Anti-Draft instruction from M3_UNDENIABLE finding.

    FR22 §Stage 2: 'Inject the M3 finding explicitly: The draft assumes the
    audience believes [M3 belief]. You must actively tear this assumption down,
    do not cater to it.'

    Mode-specific construction rules from CCP_Evolution_Architecture_Report_V3:
    - Escape: Vehicle mirrors audience's L3 pain domain (semantic affinity breach)
    - Discovery: Mechanism is correct but payload unearned (arrives before stakes)
    - Status: Comparison feeds the wrong narrative (upward/downward mismatch)
    """
    base = (
        f"ANTI-DRAFT LEVEL 2 (M3 Subversion): "
        f"The audience currently believes: \"{m3_belief}\". "
        f"You must actively tear this assumption down — do not cater to it. "
    )

    mode_specific: dict[MoodStatePrimary, str] = {
        MoodStatePrimary.ESCAPE: (
            "In ESCAPE mode: the vehicle must NOT mirror this belief. "
            "If the entertainment vehicle accidentally validates the wrong prediction, "
            "the truth-as-punchline fails — the audience laughs AT the lesson instead of THROUGH it. "
            "Structure the vehicle so it leads the audience to discover their own belief was wrong."
        ),
        MoodStatePrimary.DISCOVERY: (
            "In DISCOVERY mode: the counter-intuitive entry point must directly oppose this belief. "
            "Build the cognitive puzzle so the audience's M3 assumption is the obvious-but-wrong answer. "
            "The competence reward arrives when they abandon this prediction voluntarily."
        ),
        MoodStatePrimary.STATUS: (
            "In STATUS mode: the comparison mechanism must expose this belief as the loser's strategy. "
            "What winners understood is precisely the opposite of this M3 belief. "
            "Never state the correction explicitly — encode it in the comparison structure."
        ),
        MoodStatePrimary.PROCESSING: (
            "In PROCESSING mode: meaning-making scaffolding must hold space for the audience "
            "to recognize this belief on their own. Do not force the correction — companion them to it."
        ),
    }

    suffix = mode_specific.get(
        mood_state,
        "Structure the content so this belief is dismantled through the natural arc."
    )

    return base + suffix


# ─── Semantic Affinity Guard Check ────────────────────────────────────────────

def _check_semantic_affinity(
    mood_state: MoodStatePrimary,
    theme: str,
    semantic_affinity_risk: str,
) -> tuple[bool, list[str]]:
    """Check Semantic Affinity Guard (DEP-PROTO-011) clearance.

    CCP_Technical_Architecture §5.2: Semantic Affinity Guard activates
    before payload-masking-adapter runs for ESCAPE mode. Blocks HIGH
    affinity subjects with ESCAPE audience to prevent psychological harm.

    Returns:
        (cleared, warnings) — cleared=False blocks Escape masking.
    """
    warnings: list[str] = []

    if mood_state == MoodStatePrimary.ESCAPE and semantic_affinity_risk == "HIGH":
        warnings.append(
            f"SEMANTIC AFFINITY GUARD: HIGH affinity risk detected for theme "
            f"'{theme}' in ESCAPE mode. Payload masking BLOCKED to prevent "
            f"psychological harm. Route to PROCESSING mode or select different theme."
        )
        return False, warnings

    if semantic_affinity_risk == "MEDIUM":
        warnings.append(
            f"SEMANTIC AFFINITY GUARD: MEDIUM affinity risk for theme '{theme}'. "
            f"Proceed with caution — monitor generation for affinity breach."
        )

    return True, warnings


# ─── Constraint String Builder ────────────────────────────────────────────────

def _build_masking_constraints(
    output: PayloadMaskingAdapterOutput,
) -> list[str]:
    """Build constraint strings from the adapter output."""
    constraints: list[str] = []

    # Primary masking instruction
    constraints.append(
        f"CONSTRAINT (Payload Masking — {output.mood_state} Mode): "
        f"{output.masking_instruction}"
    )

    # M3 subversion if available
    if output.m3_subversion_instruction:
        constraints.append(output.m3_subversion_instruction)

    # Semantic affinity clearance status
    if output.semantic_affinity_cleared:
        constraints.append(
            "CONSTRAINT (Semantic Affinity): Cleared — "
            "this mood × theme combination has passed DEP-PROTO-011."
        )

    return constraints


# ─── Adapter Engine ───────────────────────────────────────────────────────────

class PayloadMaskingAdapter:
    """Adapter-6 — Generates Trojan Horse construction instruction for Emilio.

    CCP_Evolution_Architecture_Report_V3 §3.2:
        'The most sophisticated adapter instruction in the system.
        Operationalises Excitation Transfer differently for each
        non-Processing mood state.'

    Conditional adapter — activated only when mood_state ≠ Processing.
    When Processing: adapter returns success with a no-op advisory.

    ADR-01: coach_id scopes all operations.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def load(
        self,
        mood_state: MoodStatePrimary,
        coach_id: str,
        archetype_id: str = "",
        cral_finding_index: Optional[CRALFindingIndex] = None,
        semantic_affinity_risk: str = "LOW",
        theme: str = "",
    ) -> AdapterRunResult:
        """Generate payload masking instruction per mood × archetype.

        Args:
            mood_state: The primary mood state for this compilation.
            coach_id: ADR-01 tenant isolation identifier.
            archetype_id: Archetype family for archetype-specific variations.
            cral_finding_index: Optional DEP-ENG-021 for M3_UNDENIABLE extraction.
            semantic_affinity_risk: Risk level from DEP-PROTO-011 (LOW/MEDIUM/HIGH).
            theme: Content theme (required for semantic affinity check).

        Returns:
            AdapterRunResult with Block B injection payload.
        """
        gate_failures: list[str] = []
        warnings: list[str] = []

        # ── Processing mode bypass ────────────────────────────────
        if mood_state == MoodStatePrimary.PROCESSING:
            warnings.append(
                "Payload masking adapter not activated: mood_state=Processing. "
                "Processing mode receives L3 payload directly — no Trojan Horse needed."
            )
            entry = self._rc.log(
                agent_id=AGENT_ADAPTER,
                action=STAGE_ADAPTER,
                input_summary=f"coach={coach_id}, mood=Processing — SKIPPED",
                output_summary="No-op: Processing mode bypass.",
                metadata={
                    "stage_name": STAGE_ADAPTER,
                    "coach_id": coach_id,
                    "adapter_slot": ADAPTER_SLOT.value,
                    "mood_state": mood_state.value,
                    "processing_bypass": True,
                },
            )
            return AdapterRunResult(
                adapter_slot=ADAPTER_SLOT,
                coach_id=coach_id,
                success=True,
                receipt_id=entry.receipt_id,
                warnings=warnings,
            )

        # ── Semantic Affinity Guard (DEP-PROTO-011) ───────────────
        affinity_cleared, affinity_warnings = _check_semantic_affinity(
            mood_state=mood_state,
            theme=theme,
            semantic_affinity_risk=semantic_affinity_risk,
        )
        warnings.extend(affinity_warnings)

        if not affinity_cleared:
            gate_failures.append(
                f"Semantic Affinity Guard BLOCKED: HIGH risk for "
                f"theme '{theme}' in {mood_state.value} mode."
            )
            return AdapterRunResult(
                adapter_slot=ADAPTER_SLOT,
                coach_id=coach_id,
                success=False,
                gate_failures=gate_failures,
                warnings=warnings,
            )

        # ── Fetch masking instruction from library ────────────────
        masking_instruction = get_payload_masking_instruction(mood_state)

        # ── Extract M3_UNDENIABLE if available ────────────────────
        m3_instruction: Optional[str] = None
        if cral_finding_index is not None:
            m3_finding = cral_finding_index.get_finding(CRALMomentKey.M3_UNDENIABLE)
            if m3_finding is not None:
                m3_instruction = _build_m3_subversion_instruction(
                    m3_belief=m3_finding.finding_text,
                    mood_state=mood_state,
                )
            else:
                warnings.append(
                    "CRAL M3_UNDENIABLE finding not available (CRAL_DEGRADED). "
                    "Level 2 Anti-Draft will use mode-only masking without M3 specificity."
                )

        # ── Build adapter output ──────────────────────────────────
        output = PayloadMaskingAdapterOutput(
            coach_id=coach_id,
            mood_state=mood_state.value,
            archetype_id=archetype_id,
            masking_instruction=masking_instruction,
            m3_subversion_instruction=m3_instruction,
            semantic_affinity_cleared=affinity_cleared,
            constraint_strings=[],  # Populated below
        )

        # ── Build constraints ─────────────────────────────────────
        constraints = _build_masking_constraints(output)
        output.constraint_strings = constraints

        # ── Build Block B injection ───────────────────────────────
        block_b = BlockBInjection(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            target=BlockTarget.BLOCK_B,
            section_header="## Payload Masking (Adapter-6 — Trojan Horse Structural Instruction)",
            constraint_strings=constraints,
            metadata={
                "dep_id": "payload-masking-adapter",
                "mood_state": mood_state.value,
                "archetype_id": archetype_id,
                "has_m3": m3_instruction is not None,
                "semantic_affinity_cleared": affinity_cleared,
                "semantic_affinity_risk": semantic_affinity_risk,
            },
        )

        # ── Receipt write ─────────────────────────────────────────
        entry = self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=(
                f"coach={coach_id}, mood={mood_state.value}, "
                f"archetype={archetype_id or 'unspecified'}, "
                f"affinity_risk={semantic_affinity_risk}, "
                f"has_cral={'yes' if cral_finding_index else 'no'}"
            ),
            output_summary=(
                f"Block B injection: {len(constraints)} constraints, "
                f"has_m3={m3_instruction is not None}, "
                f"affinity_cleared={affinity_cleared}"
            ),
            metadata={
                "stage_name": STAGE_ADAPTER,
                "coach_id": coach_id,
                "adapter_slot": ADAPTER_SLOT.value,
                "mood_state": mood_state.value,
                "archetype_id": archetype_id,
                "has_m3": m3_instruction is not None,
                "semantic_affinity_cleared": affinity_cleared,
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
