"""
FR54 — Promotional Asset Compiler
====================================
Takes intelligence briefs from FR51/FR52 and compiles structured
promotional asset payloads (DEP-ENG-075) for the Excalidraw pipeline
(FR35) and TTS (FR27).

Classes
-------
PayloadCompletenessGate
    Validates Z-Pattern flyer node completeness: hook word count ≤ 6,
    no placeholder coach photo URL, node_1 not null.

PromotionalAssetCompiler
    Orchestrates asset-type routing, gate evaluation, and receipt logging.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.ccp.models.cpsc_models import (
    AssetCompilerError,
    AssetTypeGenerated,
    PayloadCompletenessVerdict,
    StructuredAssetPayloadRow,
    ZPatternNodes,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Flyer hook word limit (§4 Stage 2)
FLYER_HOOK_MAX_WORDS: int = 6

# Placeholder coach photo sentinel (§4 Stage 2)
PLACEHOLDER_PHOTO_SENTINEL: str = "INSERT_COACH_PHOTO"

# Asset type origin keys (§4 Stage 1)
ORIGIN_CHALLENGE_FUNNEL = "challenge_funnel"
ORIGIN_WEBINAR_BRIEF = "webinar_brief"


# ---------------------------------------------------------------------------
# PayloadCompletenessGate
# ---------------------------------------------------------------------------

class PayloadCompletenessGate:
    """
    Validates assembled node arrays before schema dump.

    Parameters
    ----------
    node_1 : str | None
        Top-left hook text. Must be ≤ 6 words and not None.
    node_2 : str | None
        Coach-verified image URL. Must not equal the placeholder sentinel.

    Gate logic (§4 Stage 2)
    -----------------------
    Priority (evaluated in order):
    1. FAIL_BOUNDARY_VIOLATION  : node_1 is None OR len(node_1.split()) > 6
    2. PROVISIONAL_MISSING_ASSET: node_2 is None OR node_2 == PLACEHOLDER sentinel
    3. PASS                     : all checks clear
    """

    def __init__(self, node_1: str | None, node_2: str | None) -> None:
        self._node_1 = node_1
        self._node_2 = node_2

    def evaluate(self) -> PayloadCompletenessVerdict:
        # 1. Hook text violation (hard fail)
        if self._node_1 is None:
            return PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION
        if len(self._node_1.split()) > FLYER_HOOK_MAX_WORDS:
            return PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION

        # 2. Missing coach photo (provisional halt)
        if self._node_2 is None or self._node_2 == PLACEHOLDER_PHOTO_SENTINEL:
            return PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET
        if PLACEHOLDER_PHOTO_SENTINEL in self._node_2:
            return PayloadCompletenessVerdict.PROVISIONAL_MISSING_ASSET

        # 3. All clear
        return PayloadCompletenessVerdict.PASS


# ---------------------------------------------------------------------------
# PromotionalAssetCompiler
# ---------------------------------------------------------------------------

class PromotionalAssetCompiler:
    """
    Orchestrates FR54: routes asset type by generator origin, evaluates
    the Payload Completeness Gate, and returns a StructuredAssetPayloadRow.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain (DEP-ENG-041).
    """

    _AGENT_ID = "promotional-asset-compiler"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compile_flyer(
        self,
        *,
        generator_source_id: str,
        hook_text: str,
        commitment_price: float,
        enemy_contrast_noun: str,
        coach_verified_image_url: str | None,
    ) -> StructuredAssetPayloadRow:
        """
        Compile a Z_PATTERN_FLYER asset payload from a Challenge Funnel brief.

        Parameters
        ----------
        generator_source_id : str
            UUID of the originating ChallengeFunnelBriefRow (DEP-ENG-072).
        hook_text : str
            flyer_hook_text from FR51 (≤ 6 words).
        commitment_price : float
            commitment_price from FR51 (CTA node).
        enemy_contrast_noun : str
            enemy_contrast_noun from FR51 (node_3).
        coach_verified_image_url : str | None
            Authenticated coach portrait URL (ADR-01 scoped).
            None or PLACEHOLDER_PHOTO_SENTINEL → PROVISIONAL.

        Returns
        -------
        StructuredAssetPayloadRow

        Raises
        ------
        ValueError(AssetCompilerError.FAIL_BOUNDARY_VIOLATION)
            If hook_text exceeds 6 words.
        """
        return self._compile(
            asset_type=AssetTypeGenerated.Z_PATTERN_FLYER,
            generator_source_id=generator_source_id,
            node_1=hook_text,
            node_2=coach_verified_image_url,
            node_3=enemy_contrast_noun,
            node_4=str(commitment_price),
            tts_script_body=None,
        )

    def compile_voice_script(
        self,
        *,
        generator_source_id: str,
        tts_script_body: str,
        coach_verified_image_url: str | None,
    ) -> StructuredAssetPayloadRow:
        """
        Compile a VOICE_SCRIPT asset payload from a Webinar Brief.

        Parameters
        ----------
        generator_source_id : str
            UUID of the originating WebinarConversionBriefRow (DEP-ENG-073).
        tts_script_body : str
            TTS script body (< 90 seconds narration).
        coach_verified_image_url : str | None
            Authenticated coach portrait URL (used as node_2 for gate check).

        Returns
        -------
        StructuredAssetPayloadRow
        """
        return self._compile(
            asset_type=AssetTypeGenerated.VOICE_SCRIPT,
            generator_source_id=generator_source_id,
            node_1=tts_script_body[:40] if tts_script_body else None,  # gate check on first 40 chars
            node_2=coach_verified_image_url,
            node_3=None,
            node_4=None,
            tts_script_body=tts_script_body,
        )

    # ------------------------------------------------------------------
    # Private orchestration
    # ------------------------------------------------------------------

    def _compile(
        self,
        *,
        asset_type: AssetTypeGenerated,
        generator_source_id: str,
        node_1: str | None,
        node_2: str | None,
        node_3: str | None,
        node_4: str | None,
        tts_script_body: str | None,
    ) -> StructuredAssetPayloadRow:
        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="asset-type-resolve",
            output_summary=(
                f"coach={self._coach_id} asset_type={asset_type.value} "
                f"source={generator_source_id}"
            ),
        )

        # Gate applies differently per asset type:
        # For Z_PATTERN_FLYER: gate uses hook (node_1) + image URL (node_2)
        # For VOICE_SCRIPT: image check only; hook rule not applicable
        if asset_type == AssetTypeGenerated.Z_PATTERN_FLYER:
            gate_node_1 = node_1
        else:
            # VOICE_SCRIPT: provide a 1-word synthetic to skip hook violation check
            gate_node_1 = "script"

        gate = PayloadCompletenessGate(gate_node_1, node_2)
        verdict = gate.evaluate()

        if verdict == PayloadCompletenessVerdict.FAIL_BOUNDARY_VIOLATION:
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="asset-completeness-gate",
                output_summary=(
                    f"coach={self._coach_id} verdict=FAIL_BOUNDARY_VIOLATION — "
                    f"hook='{node_1}' exceeds {FLYER_HOOK_MAX_WORDS} words"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(AssetCompilerError.FAIL_BOUNDARY_VIOLATION)

        self._rc.log(
            agent_id=self._AGENT_ID,
            action="asset-completeness-gate",
            output_summary=(
                f"coach={self._coach_id} verdict={verdict.value}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        # Build z_pattern_nodes only for flyer type
        z_nodes: ZPatternNodes | None = None
        if asset_type == AssetTypeGenerated.Z_PATTERN_FLYER and node_1 is not None:
            z_nodes = ZPatternNodes(
                top_left_hook=node_1,
                bottom_right_cta=node_4 or "",
            )

        return StructuredAssetPayloadRow(
            asset_payload_id=str(uuid.uuid4()),
            generator_source_id=generator_source_id,
            asset_type_generated=asset_type.value,
            gate_verdict=verdict.value,
            z_pattern_nodes=z_nodes,
            tts_script_body=tts_script_body,
            compiled_at=datetime.now(timezone.utc).isoformat(),
        )
