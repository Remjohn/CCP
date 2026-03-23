"""
CCP Step 5 — Coach Soul Adapter (Adapter-1, Unit 3)
Loads DEP-ENG-003 (PositiveSpaceObject) into SKILL.md Block A.

Architecture reference:
    CCP_Technical_Architecture.md §4 Adapter Registry v2.0 — Adapter-1
    FR3_Voice_DNA_Extraction_Tech_Spec.md §Steps 6-8 — Positive Space + Humor

MANDATE 4 (hardcoded, not a prompt instruction):
    This adapter MUST NOT execute until negative-space-loader-adapter (Adapter-2)
    has completed successfully. The pipeline orchestrator enforces this at code level.
    If called without a pre-validated NegativeSpaceObject proof, raises Mandate4GateError.

Prerequisite gate (DEP-ENG-004 proof required):
    Spec §Step 6: 'Prerequisite gate: DEP-ENG-004 exists in coach_soul.json'
    This adapter accepts a `negative_space_complete: bool` flag from the pipeline.
    If False → raises Mandate4GateError. The flag must be set by the pipeline
    orchestrator AFTER negative_space_loader_adapter.load() returns success=True.

Block A injection produces:
    1. Cluster Prose Descriptions — 5 stylometry clusters → voice instruction strings
    2. Stylometry Summary — compact representation of the coach's stylometric signature
    3. Humor Style Classification — primary humor type + usage guidance

ADR-01: coach_id scopes all operations.
FR47:   Receipt written per DEP-ENG-041 schema on successful injection.
M-02:   No TTT values in output strings.
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
    ClusterProseDescription,
    HumorStyleClassification,
    HumorType,
    PositiveSpaceObject,
    StylometryProfile,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_ADAPTER = "Coach-Soul-Adapter"
STAGE_ADAPTER = "ADAPTER-COACH-SOUL-BLOCK-A"
ADAPTER_SLOT = AdapterSlot.COACH_SOUL


# ─── Gate Error ───────────────────────────────────────────────────────────────

class Mandate4GateError(Exception):
    """Raised when Adapter-1 is invoked without confirmed DEP-ENG-004 completion.

    Spec §Step 6 — AC2: 'the pipeline halts with a DEP-ENG-004_NOT_FOUND error
    (not a prompt failure — a code-level gate)'

    The pipeline orchestrator MUST set negative_space_complete=True only after
    NegativeSpaceLoaderAdapter.load() returns AdapterRunResult(success=True).
    """
    def __init__(self) -> None:
        super().__init__(
            "MANDATE-4-GATE-FAIL: Coach Soul Adapter (Adapter-1) cannot execute "
            "before Negative Space Loader Adapter (Adapter-2) completes. "
            "DEP-ENG-004 must be validated and Block A injection confirmed. "
            "This is a code-level gate — not a prompt instruction."
        )


class IncompletePositiveSpaceError(Exception):
    """Raised when DEP-ENG-003 is incomplete — not all 5 clusters have prose descriptions.

    Spec §Stress Test Q2: 'An incomplete matrix evaluates as status: PARTIAL → FALSE'
    AC3: 'All 5 stylometry clusters must have non-empty prose_description fields.'
    """
    def __init__(self, missing_count: int) -> None:
        super().__init__(
            f"DEP-ENG-003 incomplete: {missing_count} of 5 stylometry clusters "
            f"are missing prose_description. All 5 must be populated before "
            f"Block A injection can proceed."
        )


# ─── String Builders ──────────────────────────────────────────────────────────

# Humor type guidance strings — translate HumorType enum to voice instruction
_HUMOR_GUIDANCE: dict[HumorType, str] = {
    HumorType.AFFILIATIVE: (
        "This coach's humor is AFFILIATIVE — it creates shared belonging and lightens tension "
        "without targeting anyone. Use warmth, self-aware wit, and gentle observation. "
        "Avoid sarcasm directed at the audience."
    ),
    HumorType.SELF_ENHANCING: (
        "This coach's humor is SELF-ENHANCING — it comes from a place of inner resilience and "
        "amused perspective on difficulty. Light irony and philosophical wit are authentic. "
        "Do not manufacture jokes — let the humor emerge from honest observation."
    ),
    HumorType.AGGRESSIVE: (
        "This coach's humor is AGGRESSIVE — it challenges, pokes, and uses pointed critique as "
        "a vehicle for insight. Satire and sharp observation are authentic. "
        "This humor is a structural tool — not cruelty — and must serve the argument."
    ),
    HumorType.SELF_DEFEATING: (
        "This coach's humor is SELF-DEFEATING — it uses vulnerability and self-deprecation as "
        "connection mechanisms. This must be used sparingly and only when it serves to lower "
        "barriers for the audience. Never manufacture self-defeat — it must be genuine."
    ),
}


def _build_cluster_prose_laws(positive_space: PositiveSpaceObject) -> list[str]:
    """Build Block A structural law strings from the 5 stylometry cluster prose descriptions.

    Each cluster's prose_description is a direct voice instruction string already
    suitable for Block A injection — the extractor built these for this purpose.
    """
    laws: list[str] = []
    laws.append(
        "POSITIVE SPACE — Voice DNA Cluster Laws (DEP-ENG-003): "
        "The following 5 stylometry clusters define this coach's authentic voice. "
        "Every word produced must conform to ALL 5 simultaneously:"
    )

    for i, cluster in enumerate(positive_space.clusters, start=1):
        cluster_id = getattr(cluster, "cluster_id", f"CLUSTER-{i}")
        cluster_name = getattr(cluster, "cluster_name", f"Cluster {i}")
        prose = cluster.prose_description

        if prose:
            laws.append(
                f"  [Cluster {i} — {cluster_id} | {cluster_name}]: {prose}"
            )

    return laws


def _build_stylometry_summary_laws(stylometry: StylometryProfile) -> list[str]:
    """Build a compact stylometry summary law string from the StylometryProfile.

    Gives the generation agent quick-reference calibration data for sentence
    rhythm, complexity, and density — without any TTT values (M-02 compliant).
    """
    laws: list[str] = []

    parts: list[str] = []

    avg_len = getattr(stylometry, "average_sentence_length_words", None)
    if avg_len is not None:
        parts.append(f"avg sentence length ≈ {avg_len:.1f} words")

    complexity = getattr(stylometry, "sentence_complexity_score", None)
    if complexity is not None:
        parts.append(f"sentence complexity = {complexity:.2f}/1.0")

    lexical_density = getattr(stylometry, "lexical_density", None)
    if lexical_density is not None:
        parts.append(f"lexical density = {lexical_density:.2f}")

    vocab_richness = getattr(stylometry, "vocabulary_richness", None)
    if vocab_richness is not None:
        parts.append(f"vocabulary richness (TTR) = {vocab_richness:.2f}")

    if parts:
        laws.append(
            "STYLOMETRY BASELINE (DEP-ENG-003): Calibrate output to match these "
            "mathematically extracted voice parameters: " + "; ".join(parts) + "."
        )

    return laws


def _build_humor_law(humor: HumorStyleClassification) -> list[str]:
    """Build a Block A humor style law from the HumorStyleClassification.

    The humor style is a structural voice attribute — the generation agent must
    understand what type of humor is authentic for this coach and deploy it
    accordingly rather than generic "be funny" instructions.
    """
    guidance = _HUMOR_GUIDANCE.get(humor.primary_style, "")
    law = (
        f"HUMOR STYLE LAW (DEP-ENG-003 — Mandate 8): "
        f"This coach's humor type is {humor.primary_style.value.upper()}. "
        f"{guidance}"
    )

    if humor.secondary_style:
        law += (
            f" Secondary style: {humor.secondary_style.value}. "
            f"The primary style dominates — secondary appears contextually."
        )

    return [law]


# ─── Adapter ─────────────────────────────────────────────────────────────────

class CoachSoulAdapter:
    """Adapter-1 — Loads DEP-ENG-003 (PositiveSpaceObject) into SKILL.md Block A.

    MANDATE 4: This adapter must only be invoked after NegativeSpaceLoaderAdapter
    has confirmed successful completion (negative_space_complete=True).
    The pipeline orchestrator is responsible for this enforcement.

    Block A injection: 5 cluster prose laws + stylometry summary + humor style law.

    ADR-01: coach_id in all outputs and receipt logs.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def load(
        self,
        positive_space: PositiveSpaceObject,
        coach_id: str,
        negative_space_complete: bool = False,
        humor: HumorStyleClassification | None = None,
    ) -> AdapterRunResult:
        """Execute the Positive Space → Block A injection.

        Args:
            positive_space: Validated DEP-ENG-003 from PositiveSpaceExtractor.
            coach_id: ADR-01 coach instance identifier.
            negative_space_complete: Must be True — set by pipeline after
                Adapter-2 confirms success. Mandate 4 gate.
            humor: Optional HumorStyleClassification for Mandate 8 humor law.

        Returns:
            AdapterRunResult with Block A injection payload on success.

        Raises:
            Mandate4GateError: If negative_space_complete is False.
            IncompletePositiveSpaceError: If DEP-ENG-003 is missing cluster prose.
        """
        # ── Mandate 4 Gate ─────────────────────────────────────────────────────
        if not negative_space_complete:
            raise Mandate4GateError()

        # ── Completeness Gate (AC3) ────────────────────────────────────────────
        if not positive_space.is_complete():
            missing = sum(
                1 for c in positive_space.clusters
                if not getattr(c, "prose_description", "")
            )
            raise IncompletePositiveSpaceError(missing_count=missing)

        # ── Build Block A structural laws ──────────────────────────────────────
        laws: list[str] = []

        laws.extend(_build_cluster_prose_laws(positive_space))

        if positive_space.stylometry_profile:
            laws.extend(_build_stylometry_summary_laws(positive_space.stylometry_profile))

        if humor:
            laws.extend(_build_humor_law(humor))

        # ── Assemble injection ─────────────────────────────────────────────────
        injection = BlockAInjection(
            adapter_slot=ADAPTER_SLOT,
            coach_id=coach_id,
            target=BlockTarget.BLOCK_A,
            section_header="## Positive Space Voice Laws (Adapter-1 — DEP-ENG-003)",
            structural_laws=laws,
            metadata={
                "dep_id": "DEP-ENG-003",
                "cluster_count": len(positive_space.clusters),
                "mandate_4_gate": "PASSED",
                "humor_style": humor.primary_style.value if humor else None,
                "stylometry_present": positive_space.stylometry_profile is not None,
            },
        )

        # ── Receipt Write (FR47 DEP-ENG-041) ──────────────────────────────────
        entry = self._rc.log(
            agent_id=AGENT_ADAPTER,
            action=STAGE_ADAPTER,
            input_summary=(
                f"coach_id={coach_id} clusters={len(positive_space.clusters)} "
                f"negative_space_complete={negative_space_complete}"
            ),
            output_summary=(
                f"Block_A_laws={len(laws)} dep_id=DEP-ENG-003 "
                f"humor={humor.primary_style.value if humor else 'none'}"
            ),
            metadata={
                "stage_name": STAGE_ADAPTER,
                "adapter_slot": ADAPTER_SLOT.value,
                "coach_id": coach_id,
                "dep_id": "DEP-ENG-003",
                "cluster_count": len(positive_space.clusters),
                "mandate_4_gate": "PASSED",
                "block_a_law_count": len(laws),
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
        positive_space: PositiveSpaceObject,
        coach_id: str,
        negative_space_complete: bool = False,
        humor: HumorStyleClassification | None = None,
    ) -> str:
        """Produce the full Block A Positive Space section text for SKILL.md injection.

        Calls load() internally — raises Mandate4GateError or IncompletePositiveSpaceError.

        Returns:
            Multi-line string ready for SKILL.md Block A injection.
        """
        result = self.load(positive_space, coach_id, negative_space_complete, humor)
        if result.block_a:
            return result.block_a.to_block_a_text()
        return ""
