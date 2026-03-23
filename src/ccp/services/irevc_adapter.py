"""
CCP Step 5 — IREVC Adapter (Adapter-5, Unit 5)
Loads DEP-LIB-002 (TriggerMap) + DEP-ENG-005 (TTT Authentication Certificate)
into SKILL.md Block A as pre-load constraints.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0 — Adapter-5
    FR5_Trigger_Map_Builder_Tech_Spec.md — TriggerMap (DEP-LIB-002)
    FR8_TTT_Enforcement_Rule_Tech_Spec.md §Layer 3 — Runtime TTT Resolution (DEP-ENG-005)
    FR4_Emotional_DNA_Extraction_Tech_Spec.md — IREVC protocol (I-R-E-V-C)

IREVC Protocol (I-R-E-V-C):
    The extraction protocol that produced DEP-LIB-002 and DEP-LIB-001.
    I = Initiation (trigger identification)
    R = Resolution (PTG classification)
    E = Emotional mapping (LIWC-22 + V6-V10)
    V = Validation (reconsolidation sensitivity)
    C = Certification (DEP-ENG-005 authentication → TTT baseline)

Block A injection produces 3 ordered sections:
    1. Content-safe trigger pre-load (resolved_dual_layer triggers only — PTG gate)
    2. Archetype activation mapping (emotional states → eligible archetypes)
    3. TTT runtime context (DEP-ENG-005 authenticated temperature/texture/tone)

PTG Safety Gate (hardcoded):
    Spec §Phase 4: raw_unresolved = HARD EXCLUDE from content activation.
    TriggerMap.get_content_safe_triggers() enforces this.
    This adapter only loads content-safe triggers into Block A.

TTT Runtime Resolution (M-02 compliant):
    DEP-ENG-005 authentication certificate provides session-specific TTT.
    The adapter injects TTT as a RUNTIME CONTEXT string — not a hardcoded value.
    Format: "AUTHENTICATED TTT for this session: Temperature={n}, Texture={t}, Tone={r}"
    This string is a factual report of the authenticated state, NOT a template directive.
    C-08 scans for 'TTT-NN' pattern directives — not authenticated state reports.

Minimum viable map gate:
    Spec §AC4: TriggerMap.meets_minimum_viable() — at least 2 resolved_dual_layer triggers.
    If the map does not meet this minimum, a DEGRADED_MAP warning is added to the result
    but the adapter does NOT halt (advisory, not blocking gate for compilation).

ADR-01: coach_id scopes all operations.
FR47:   Receipt written per DEP-ENG-041 schema on successful injection.
M-02:   TTT is injected as authenticated runtime context, not a template directive.
"""

from __future__ import annotations

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import (
    AdapterRunResult,
    AdapterSlot,
    BlockAInjection,
    BlockTarget,
)
from src.ccp.models.ttt_models import TTTBaselineData
from src.ccp.models.trigger_map_models import (
    MINIMUM_RESOLVED_TRIGGERS,
    TriggerMap,
    PTGStatus,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "IREVC-Adapter"
STAGE_ADAPTER = "ADAPTER-IREVC-BLOCK-A"
ADAPTER_SLOT = AdapterSlot.IREVC


# ─── String Builders ──────────────────────────────────────────────────────────

def _build_trigger_preload_laws(trigger_map: TriggerMap) -> list[str]:
    """Build Block A structural law strings for the content-safe trigger pre-load.

    Only includes triggers with PTG status = RESOLVED_DUAL_LAYER or ACTIVE_PROCESSING.
    Spec §Phase 4: raw_unresolved = HARD EXCLUDE from content activation.

    Returns an empty list if no content-safe triggers exist (warns in caller).
    """
    safe_triggers = trigger_map.get_content_safe_triggers()

    if not safe_triggers:
        return []

    laws: list[str] = [
        "TRIGGER MAP PRE-LOAD (DEP-LIB-002 — IREVC Protocol): "
        "The following triggers represent this coach's validated wound architecture. "
        "These are the emotional entry points authenticated through the IREVC protocol. "
        "Only RESOLVED_DUAL_LAYER and ACTIVE_PROCESSING triggers are loaded — "
        "raw_unresolved triggers are HARD EXCLUDED from all content activation:"
    ]

    for trigger in safe_triggers:
        ptg_status_obj = trigger.ptg_status
        ptg_label = ptg_status_obj.status.value if ptg_status_obj.status else "unknown"
        trigger_label = getattr(trigger, "label", "") or getattr(trigger, "trigger_id", "unnamed")
        akb_level = trigger.originating_experience.akb_level
        akb_label = akb_level.value if akb_level else ""
        recon_score = trigger.reconsolidation_sensitivity.score

        trigger_line = (
            f"  • [{ptg_label.upper()} | AKB={akb_label}] "
            f"Trigger: '{trigger_label}'"
        )
        if recon_score is not None:
            trigger_line += f" | Reconsolidation sensitivity: {recon_score}/10"

        laws.append(trigger_line)

    return laws


def _build_archetype_activation_laws(trigger_map: TriggerMap) -> list[str]:
    """Build Block A structural law strings for archetype activation mapping.

    The archetype mapping table connects emotional states to content archetype
    candidates with TTT eligibility — this drives WHICH archetype templates
    are available for compilation based on the coach's trigger architecture.
    """
    archetype_mappings = getattr(trigger_map, "trigger_archetype_map", [])

    if not archetype_mappings:
        return []

    laws: list[str] = [
        "ARCHETYPE ACTIVATION MAP (DEP-LIB-002 — Trigger → Archetype Eligibility): "
        "The following archetype activations are available based on the trigger map:"
    ]

    for mapping in archetype_mappings:
        emotional_state = getattr(mapping, "emotional_state", "")
        primary_archetype = getattr(mapping, "primary_archetype", "")
        secondary_archetype = getattr(mapping, "secondary_archetype", "")
        ttt_minimum = getattr(mapping, "ttt_minimum", "")

        if emotional_state and primary_archetype:
            archetype_str = primary_archetype
            if secondary_archetype:
                archetype_str += f", {secondary_archetype}"
            ttt_note = f" [TTT minimum: {ttt_minimum}]" if ttt_minimum else ""
            laws.append(
                f"  • {emotional_state}{ttt_note} → eligible archetypes: {archetype_str}"
            )

    return laws


def _build_ttt_runtime_context_laws(ttt_baseline: TTTBaselineData) -> list[str]:
    """Build Block A structural law strings for the TTT runtime context.

    M-02 COMPLIANCE: This string is a FACTUAL REPORT of the coach's authenticated
    emotional state for this session. It is NOT a template directive with a TTT-NN
    hardcoded value. C-08 scans for 'TTT-NN' assignment patterns, not factual
    state reports.

    The format 'Authenticated TTT: Temperature={n}' is a runtime context injection
    (FR8 §Layer 3 §Task 8) — the assembler reads this to understand the coach's
    current state and calibrate generation accordingly.
    """
    if not ttt_baseline.liwc_authenticated:
        return [
            "TTT AUTHENTICATION STATUS (DEP-ENG-005): NOT AUTHENTICATED — "
            "LIWC-22 authenticity score below threshold. "
            "TTT runtime context is unavailable for this session. "
            "Generation will proceed without authenticated TTT calibration."
        ]

    return [
        f"AUTHENTICATED TTT CONTEXT (DEP-ENG-005 — Session={ttt_baseline.session_id}): "
        f"Temperature={ttt_baseline.temperature}/10 | "
        f"Texture={ttt_baseline.texture.value} | "
        f"Tone={ttt_baseline.tone.value} | "
        f"LIWC-22 Authenticity={ttt_baseline.liwc_authenticity_score:.1f}/10 [AUTHENTICATED]. "
        f"This is the coach's verified emotional state for this production session — "
        f"calibrate content generation register to match this authenticated baseline.",
    ]


# ─── Adapter ─────────────────────────────────────────────────────────────────

class IREVCAdapter:
    """Adapter-5 — Loads DEP-LIB-002 (TriggerMap) + DEP-ENG-005 (TTT Baseline)
    into SKILL.md Block A as pre-load structural context.

    PTG gate enforced: only RESOLVED_DUAL_LAYER and ACTIVE_PROCESSING triggers
    are loaded. RAW_UNRESOLVED is a HARD EXCLUDE (Spec §Phase 4).

    TTT injection: DEP-ENG-005 provides runtime TTT context (Temperature + Texture + Tone).
    This is a factual authenticated-state report, not a TTT-NN template directive (M-02).

    ADR-01: coach_id in all outputs and receipt logs.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def load(
        self,
        trigger_map: TriggerMap,
        coach_id: str,
        ttt_baseline: TTTBaselineData | None = None,
    ) -> AdapterRunResult:
        """Execute the TriggerMap + TTT Baseline → Block A injection.

        Args:
            trigger_map: Validated DEP-LIB-002 from TriggerMapPipeline.
            coach_id: ADR-01 coach instance identifier.
            ttt_baseline: Optional DEP-ENG-005 Authentication Certificate.
                If provided, injects authenticated TTT runtime context into Block A.
                If None, Block A will note that TTT runtime context is unavailable.

        Returns:
            AdapterRunResult with Block A injection payload on success.
            Warnings are added when:
                - TriggerMap does not meet minimum viable (< 2 resolved triggers)
                - ttt_baseline is not authenticated (LIWC < 7.0)
        """
        warnings: list[str] = []

        # ── Minimum Viable Map Check (advisory, not blocking) ──────────────────
        if not trigger_map.meets_minimum_viable():
            resolved_count = len(trigger_map.get_content_safe_triggers())
            warnings.append(
                f"DEGRADED_MAP: TriggerMap has only {resolved_count} content-safe triggers "
                f"(minimum viable = {MINIMUM_RESOLVED_TRIGGERS}). "
                f"Block A trigger pre-load will be sparse. "
                f"Archetype activation coverage is reduced."
            )

        # ── Build Block A structural laws ──────────────────────────────────────
        laws: list[str] = []

        # Section 1: Trigger pre-load (PTG-gated)
        trigger_laws = _build_trigger_preload_laws(trigger_map)
        laws.extend(trigger_laws)

        # Section 2: Archetype activation mapping
        archetype_laws = _build_archetype_activation_laws(trigger_map)
        laws.extend(archetype_laws)

        # Section 3: TTT runtime context (DEP-ENG-005)
        if ttt_baseline is not None:
            ttt_laws = _build_ttt_runtime_context_laws(ttt_baseline)
            laws.extend(ttt_laws)
            if not ttt_baseline.liwc_authenticated:
                warnings.append(
                    f"TTT_NOT_AUTHENTICATED: LIWC-22 score "
                    f"{ttt_baseline.liwc_authenticity_score:.1f}/10 is below threshold 7.0. "
                    f"DEP-ENG-005 context is degraded. Trigger OARS re-elicitation."
                )
        else:
            laws.append(
                "TTT RUNTIME CONTEXT (DEP-ENG-005): Not available for this compilation run. "
                "Authenticated TTT calibration will not be applied. "
                "Ensure TTTBaselineExtractor runs before production generation."
            )
            warnings.append(
                "DEP-ENG-005_ABSENT: TTT baseline not provided to IREVC adapter. "
                "Generation will proceed without authenticated emotional register calibration."
            )

        # ── Raw unresolved count for metadata ────────────────────────────────
        raw_unresolved_count = sum(
            1 for t in trigger_map.triggers
            if t.ptg_status.status == PTGStatus.RAW_UNRESOLVED
        )

        # ── Assemble injection ─────────────────────────────────────────────────
        safe_trigger_count = len(trigger_map.get_content_safe_triggers())
        injection = BlockAInjection(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            target=BlockTarget.BLOCK_A,
            section_header="## IREVC Trigger Pre-Load (Adapter-5 — DEP-LIB-002 + DEP-ENG-005)",
            structural_laws=laws,
            metadata={
                "dep_lib_002": "DEP-LIB-002",
                "dep_eng_005": ttt_baseline.session_id if ttt_baseline else None,
                "total_triggers": len(trigger_map.triggers),
                "content_safe_triggers": safe_trigger_count,
                "raw_unresolved_excluded": raw_unresolved_count,
                "ptg_gate_status": "ENFORCED",
                "ttt_authenticated": ttt_baseline.liwc_authenticated if ttt_baseline else False,
                "archetype_mappings": len(getattr(trigger_map, "trigger_archetype_map", [])),
                "meets_minimum_viable": trigger_map.meets_minimum_viable(),
            },
        )

        # ── Receipt Write (FR47 DEP-ENG-041) ──────────────────────────────────
        entry = self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=(
                f"coach_id={coach_id} "
                f"safe_triggers={safe_trigger_count} "
                f"raw_excluded={raw_unresolved_count} "
                f"ttt_baseline={'present' if ttt_baseline else 'absent'}"
            ),
            output_summary=(
                f"Block_A_laws={len(laws)} "
                f"ptg_gate=ENFORCED "
                f"ttt_authenticated={ttt_baseline.liwc_authenticated if ttt_baseline else False} "
                f"warnings={len(warnings)}"
            ),
            metadata={
                "stage_name": STAGE_ADAPTER,
                "adapter_slot": ADAPTER_SLOT.value,
                "coach_id": coach_id,
                "dep_lib_002": "DEP-LIB-002",
                "dep_eng_005_session": ttt_baseline.session_id if ttt_baseline else None,
                "content_safe_triggers": safe_trigger_count,
                "raw_unresolved_excluded": raw_unresolved_count,
                "ttt_authenticated": ttt_baseline.liwc_authenticated if ttt_baseline else False,
                "meets_minimum_viable": trigger_map.meets_minimum_viable(),
                "warning_count": len(warnings),
            },
        )

        return AdapterRunResult(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            success=True,
            block_a=injection,
            receipt_id=entry.receipt_id,
            gate_failures=[],
            warnings=warnings,
        )

    def format_block_a_section(
        self,
        trigger_map: TriggerMap,
        coach_id: str,
        ttt_baseline: TTTBaselineData | None = None,
    ) -> str:
        """Produce the full Block A IREVC section text for SKILL.md injection.

        Returns:
            Multi-line string ready for SKILL.md Block A injection.
        """
        result = self.load(trigger_map, coach_id, ttt_baseline)
        if result.block_a:
            return result.block_a.to_block_a_text()
        return ""
