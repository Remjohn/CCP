"""
CCP Step 5 — Negative Space Loader Adapter (Adapter-2, Unit 2)
Loads DEP-ENG-004 (NegativeSpaceObject) into SKILL.md Block A.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0 — Adapter-2
    FR3_Voice_DNA_Extraction_Tech_Spec.md §Step 5 — Negative Space Excavation

MANDATE 4 (hardcoded, not a prompt instruction):
    This adapter MUST complete successfully before coach-soul-adapter (Adapter-1)
    can execute. The pipeline orchestrator enforces this sequencing at the code level.

GATE PC-03 (L3 Minimum Depth Threshold):
    Spec §Stress Test Q1: 'mathematically less than 15 validated contrastive strings
    → L3_INSUFFICIENT_DEPTH halt + Guardian Agent micro-interview'
    NegativeSpaceObject.total_contrastive_strings() must return ≥ 15.
    This adapter re-validates the gate even if excavation already ran it.

Block A injection produces 3 ordered sections:
    1. Lexical Blacklist (words NEVER used — hard prohibition)
    2. Syntactic Impossibilities (structural patterns with zero occurrence)
    3. Structural Exclusions (macro-level content structures never present)

ADR-01: coach_id scopes all operations.
FR47:   Receipt written per DEP-ENG-041 schema on successful injection.
M-02:   No TTT values in output strings — this adapter does not touch TTT.
"""

from __future__ import annotations

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.adapter_registry_models import (
    AdapterRunResult,
    AdapterSlot,
    BlockAInjection,
    BlockTarget,
)
from src.ccp.models.voice_dna_models import (
    L3_MINIMUM_DEPTH_THRESHOLD,
    NegativeSpaceObject,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "Negative-Space-Loader-Adapter"
STAGE_ADAPTER = "ADAPTER-NEGATIVE-SPACE-BLOCK-A"
ADAPTER_SLOT = AdapterSlot.NEGATIVE_SPACE_LOADER


# ─── Gate Error ───────────────────────────────────────────────────────────────

class NegativeSpaceDepthGateError(Exception):
    """Gate PC-03 failure — total contrastive strings < L3_MINIMUM_DEPTH_THRESHOLD (15).

    Spec §Stress Test Q1:
    'mathematically less than 15 validated contrastive strings →
     L3_INSUFFICIENT_DEPTH halt + Guardian Agent micro-interview.'

    The pipeline MUST NOT proceed to coach-soul-adapter if this gate fails.
    Caller should trigger the Guardian Agent micro-interview re-elicitation flow.
    """
    def __init__(self, found: int, required: int = L3_MINIMUM_DEPTH_THRESHOLD) -> None:
        self.found = found
        self.required = required
        super().__init__(
            f"Gate PC-03 FAIL — L3_INSUFFICIENT_DEPTH: "
            f"found {found} contrastive strings, required ≥ {required}. "
            f"Trigger Guardian Agent micro-interview before proceeding to "
            f"coach-soul-adapter (Adapter-1). Mandate 4 blocks positive space extraction."
        )


# ─── String Builders ──────────────────────────────────────────────────────────

def _build_lexical_blacklist_laws(negative_space: NegativeSpaceObject) -> list[str]:
    """Build Block A structural law strings for the Lexical Blacklist component.

    Produces explicit prohibition strings for all 3 blacklist categories:
        academic   — vocabulary never present in the coach's corpus
        spiritual  — spiritual register words absent from corpus
        banned_intensifiers — hyperbolic intensifiers not used
    """
    laws: list[str] = []
    blacklist = negative_space.lexical_blacklist

    if blacklist.academic:
        joined = ", ".join(f'"{w}"' for w in blacklist.academic[:20])
        laws.append(
            f"LEXICAL PROHIBITION (Academic): Never use these words — "
            f"they are mathematically absent from this coach's corpus: {joined}."
        )

    if blacklist.spiritual:
        joined = ", ".join(f'"{w}"' for w in blacklist.spiritual[:20])
        laws.append(
            f"LEXICAL PROHIBITION (Spiritual Register): Never use these words — "
            f"zero occurrence across all transcripts: {joined}."
        )

    if blacklist.banned_intensifiers:
        joined = ", ".join(f'"{w}"' for w in blacklist.banned_intensifiers[:20])
        laws.append(
            f"LEXICAL PROHIBITION (Intensifiers): Never use these hyperbolic intensifiers — "
            f"they corrupt this coach's authentic register: {joined}."
        )

    return laws


def _build_syntactic_impossibility_laws(negative_space: NegativeSpaceObject) -> list[str]:
    """Build Block A structural law strings for Syntactic Impossibilities.

    Each impossibility is a structural pattern that has zero occurrence
    across the coach's entire corpus — it defines what this coach CANNOT sound like.
    """
    if not negative_space.syntactic_impossibilities:
        return []

    laws: list[str] = [
        "SYNTACTIC PROHIBITION: The following structural patterns have ZERO occurrence "
        "in this coach's corpus. These are not style preferences — they are mathematical "
        "impossibilities. Do not use them:"
    ]
    for pattern in negative_space.syntactic_impossibilities:
        laws.append(f"  • {pattern}")

    return laws


def _build_structural_exclusion_laws(negative_space: NegativeSpaceObject) -> list[str]:
    """Build Block A structural law strings for Structural Exclusions.

    Structural exclusions are opening/closing patterns that are
    never present in the coach's work.
    """
    laws: list[str] = []
    exclusions = negative_space.structural_exclusions

    if exclusions.forbidden_openings:
        joined = "; ".join(f'"{p}"' for p in exclusions.forbidden_openings[:10])
        laws.append(
            f"STRUCTURAL EXCLUSION (Forbidden Openings): Never open content with these patterns — "
            f"they are mathematically absent from this coach's corpus: {joined}."
        )

    if exclusions.forbidden_closings:
        joined = "; ".join(f'"{p}"' for p in exclusions.forbidden_closings[:10])
        laws.append(
            f"STRUCTURAL EXCLUSION (Forbidden Closings): Never close content with these patterns — "
            f"zero occurrence across all transcripts: {joined}."
        )

    return laws


# ─── Adapter ─────────────────────────────────────────────────────────────────

class NegativeSpaceLoaderAdapter:
    """Adapter-2 — Loads DEP-ENG-004 (NegativeSpaceObject) into SKILL.md Block A.

    This is the FIRST adapter to run in the Step 5 pipeline (Mandate 4).
    All other adapters in the voice DNA group depend on this completing successfully.

    Gate PC-03: validated before injection — raises NegativeSpaceDepthGateError
    if total_contrastive_strings() < 15. The pipeline MUST catch this and halt.

    ADR-01: coach_id in all outputs and receipt logs.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def load(
        self,
        negative_space: NegativeSpaceObject,
        coach_id: str,
    ) -> AdapterRunResult:
        """Execute the Negative Space → Block A injection.

        Args:
            negative_space: Validated DEP-ENG-004 from NegativeSpaceExcavator.
            coach_id: ADR-01 coach instance identifier.

        Returns:
            AdapterRunResult with Block A injection payload on success.

        Raises:
            NegativeSpaceDepthGateError: If Gate PC-03 fails (< 15 contrastive strings).
                The pipeline must NOT proceed to coach-soul-adapter if this is raised.
        """
        # ── Gate PC-03 ─────────────────────────────────────────────────────────
        total = negative_space.total_contrastive_strings()
        if not negative_space.passes_depth_gate():
            raise NegativeSpaceDepthGateError(found=total)

        # ── Build Block A structural laws ──────────────────────────────────────
        laws: list[str] = []

        laws.extend(_build_lexical_blacklist_laws(negative_space))
        laws.extend(_build_syntactic_impossibility_laws(negative_space))
        laws.extend(_build_structural_exclusion_laws(negative_space))

        # ── Assemble injection ─────────────────────────────────────────────────
        injection = BlockAInjection(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            target=BlockTarget.BLOCK_A,
            section_header="## Negative Space Laws (Adapter-2 — DEP-ENG-004)",
            structural_laws=laws,
            metadata={
                "dep_id": "DEP-ENG-004",
                "total_contrastive_strings": total,
                "gate_pc03": "PASS",
                "gate_threshold": L3_MINIMUM_DEPTH_THRESHOLD,
                "lexical_blacklist_count": (
                    len(negative_space.lexical_blacklist.academic)
                    + len(negative_space.lexical_blacklist.spiritual)
                    + len(negative_space.lexical_blacklist.banned_intensifiers)
                ),
                "syntactic_impossibility_count": len(negative_space.syntactic_impossibilities),
                "structural_exclusion_count": (
                    len(negative_space.structural_exclusions.forbidden_openings)
                    + len(negative_space.structural_exclusions.forbidden_closings)
                ),
            },
        )

        # ── Receipt Write (FR47 DEP-ENG-041) ──────────────────────────────────
        entry = self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=f"coach_id={coach_id} total_contrastive={total}",
            output_summary=(
                f"Block_A_laws={len(laws)} gate_pc03=PASS "
                f"dep_id=DEP-ENG-004"
            ),
            metadata={
                "stage_name": STAGE_ADAPTER,
                "adapter_slot": ADAPTER_SLOT.value,
                "coach_id": coach_id,
                "dep_id": "DEP-ENG-004",
                "total_contrastive_strings": total,
                "gate_pc03": "PASS",
                "block_a_law_count": len(laws),
                "mandate_4_status": "FIRST_ADAPTER_COMPLETE",
            },
        )

        return AdapterRunResult(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            success=True,
            block_a=injection,
            receipt_id=entry.receipt_id,
            gate_failures=[],
            warnings=[],
        )

    def format_block_a_section(
        self,
        negative_space: NegativeSpaceObject,
        coach_id: str,
    ) -> str:
        """Produce the full Block A Negative Space section text for SKILL.md injection.

        Calls load() internally — raises NegativeSpaceDepthGateError on PC-03 failure.

        Returns:
            Multi-line string ready for SKILL.md Block A injection.
        """
        result = self.load(negative_space, coach_id)
        if result.block_a:
            return result.block_a.to_block_a_text()
        return ""
