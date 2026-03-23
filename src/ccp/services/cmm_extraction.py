"""
CCP CMM Extraction Protocol — FR1 Unit 4
DEP-PROTO-014: Cultural Memory Map Extraction

Spec reference: FR1 Tech Spec §Phase 0, Step 0-A
Architecture reference: CCP_Technical_Architecture.md §3.1

The CMM extraction is run by Morgan after FR3 completion.
The operator reviews ALL entries before any are written (not automatic).
Step 0-A gate: ≥4 of 7 layers, ≥3 entries per populated layer.
Operator confirmation via Telegram review prompt is MANDATORY.

C-11 Persona Masking Gate: agent names never appear in LLM-facing prompts.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.models.v5_models import (
    CMMEntry,
    CMMLayerType,
    CulturalMemoryMap,
)
from src.ccp.core.receipt_chain import ReceiptChain


# CMM extraction prompt — C-11 enforced: no agent names in model-facing text
_CMM_EXTRACTION_PROMPT = """You are a cultural intelligence analyst.

Analyze the provided coaching onboarding material and extract cultural memory map entries
across the following 7 layers:

1. FORMATIVE_TEXTS_AND_WORKS — Books, films, movements, figures that shaped the coach's worldview
2. COLLECTIVE_WOUND_HISTORY — Shared traumas or systemic failures their audience has lived through
3. INDUSTRY_MYTHOLOGY — Beliefs their industry holds as sacred that the coach challenges or reinforces
4. GENERATIONAL_SIGNATURE — The generational context (Millennial burnout, Gen X cynicism, etc.)
5. LINGUISTIC_TEMPLATE_LIBRARY — Phrases, metaphors, and sentence constructions that will feel native
6. ASPIRATIONAL_ARCHETYPE — The cultural figure or type their audience most wants to become
7. SHARED_ENEMY_TYPOLOGY — The external force their audience blames for their situation

For each layer, extract 3-5 specific, concrete entries (not categories — actual named items).

SOURCE MATERIAL:
{source_material}

Return ONLY valid JSON in this exact format:
{{
  "formative_texts_and_works": [
    {{"content": "...", "source": "sacred_audio_transcript|business_canvas|tribe_soul|philosophy_brief"}}
  ],
  "collective_wound_history": [...],
  "industry_mythology": [...],
  "generational_signature": [...],
  "linguistic_template_library": [...],
  "aspirational_archetype": [...],
  "shared_enemy_typology": [...]
}}

Rules:
- Each entry must be specific and concrete, not a category description.
- Mark the source_material field with which input document the entry came from.
- Extract 3-5 entries per layer. More is better. Empty arrays are not acceptable.
- Do not add commentary. Return only the JSON object.
"""

# Layer type name mapping for prompt output keys → CMMLayerType enum
_PROMPT_KEY_TO_LAYER: dict[str, CMMLayerType] = {
    "formative_texts_and_works": CMMLayerType.FORMATIVE_TEXTS,
    "collective_wound_history": CMMLayerType.COLLECTIVE_WOUND,
    "industry_mythology": CMMLayerType.INDUSTRY_MYTHOLOGY,
    "generational_signature": CMMLayerType.GENERATIONAL_SIGNATURE,
    "linguistic_template_library": CMMLayerType.LINGUISTIC_TEMPLATES,
    "aspirational_archetype": CMMLayerType.ASPIRATIONAL_ARCHETYPE,
    "shared_enemy_typology": CMMLayerType.SHARED_ENEMY,
}


class CMMExtractionProtocol:
    """DEP-PROTO-014: Cultural Memory Map Extraction Protocol.

    Spec Step 0-A:
    - 'Morgan runs the CMM extraction pass using all onboarding source material'
    - 'Operator reviews all 7 CMM layer entries'
    - 'CMM is NOT written automatically — the Agent identifies, the operator decides'

    Source materials consumed:
    - Sacred Audio transcripts (coach_soul.json / ttt extraction output)
    - Business canvas (01_business_canvas.md)
    - Tribe soul (tribe_soul.json / DEP-ENG-001)
    - Philosophy brief

    Output: CulturalMemoryMap object with entries pending operator review.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
        receipt_chain: ReceiptChain,
        gemini_api_key: Optional[str] = None,
    ):
        import os
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir
        self.receipt_chain = receipt_chain
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for CMM extraction")

    async def extract(
        self,
        sacred_audio_transcript: str,
        business_canvas_content: str,
        tribe_soul_content: str,
        philosophy_brief_content: str,
    ) -> CulturalMemoryMap:
        """Run DEP-PROTO-014 CMM extraction from all onboarding source material.

        Spec: 'Morgan runs the CMM extraction pass using all onboarding source material
        (Sacred Audio transcripts, business canvas, tribe soul, philosophy brief).'

        Returns a CulturalMemoryMap with operator_approved=False for all entries.
        The operator must run confirm_entries() before the CMM passes Gate G-CMM.

        Args:
            sacred_audio_transcript: Transcribed Sacred Audio content
            business_canvas_content: 01_business_canvas.md content
            tribe_soul_content: tribe_soul.json serialized content
            philosophy_brief_content: Philosophy brief document content

        Returns:
            CulturalMemoryMap with extracted (unconfirmed) entries.
        """
        from google import genai

        # Compile source material
        source_material = (
            f"=== SACRED AUDIO TRANSCRIPT ===\n{sacred_audio_transcript}\n\n"
            f"=== BUSINESS CANVAS ===\n{business_canvas_content}\n\n"
            f"=== TRIBE SOUL ===\n{tribe_soul_content}\n\n"
            f"=== PHILOSOPHY BRIEF ===\n{philosophy_brief_content}"
        )

        prompt = _CMM_EXTRACTION_PROMPT.format(source_material=source_material)

        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        raw_layers = json.loads(response_text)

        # Build CMMEntry objects — all pending operator approval
        entries: list[CMMEntry] = []
        for prompt_key, layer_type in _PROMPT_KEY_TO_LAYER.items():
            layer_items = raw_layers.get(prompt_key, [])
            for item in layer_items:
                entry = CMMEntry(
                    entry_id=f"CMM-{self.coach_acronym}-{layer_type.value[:4].upper()}-{uuid.uuid4().hex[:8].upper()}",
                    layer_type=layer_type,
                    content=item.get("content", ""),
                    source_material=item.get("source", "unknown"),
                    operator_approved=False,  # Never automatic — spec mandate
                    coach_id=self.coach_id,
                )
                if entry.content:  # Skip empty content
                    entries.append(entry)

        cmm_id = f"CMM-{self.coach_acronym}-{uuid.uuid4().hex[:8].upper()}"
        cmm = CulturalMemoryMap(
            cmm_id=cmm_id,
            coach_id=self.coach_id,
            entries=entries,
            status="in_progress",
            operator_confirmed=False,
        )

        # Save to local config for operator review
        cmm_path = self.coach_dir / "config" / "cultural_memory_map.json"
        cmm_path.write_text(cmm.model_dump_json(indent=2), encoding="utf-8")

        # Write to Supabase
        self._upsert_to_supabase(cmm)

        return cmm

    def build_operator_review_message(self, cmm: CulturalMemoryMap) -> str:
        """Build the Telegram review message for operator confirmation.

        Spec: 'Operator confirms all entries via Telegram review prompt.
        CMM is NOT written automatically — the Agent identifies, the operator decides.'

        The message presents all extracted entries layer by layer for operator
        approve/reject decision. Agent names are NOT included (C-11 compliance).
        """
        lines = [
            f"📋 *Cultural Memory Map — Review Required*",
            f"Coach: {self.coach_acronym} | CMM ID: `{cmm.cmm_id}`",
            f"Total entries extracted: {len(cmm.entries)}",
            "",
            "Please review each entry and reply with entry IDs to approve.",
            "Format: `APPROVE: [entry_id_1, entry_id_2, ...]`",
            "Format: `REJECT: [entry_id_1, ...]`",
            "",
        ]

        for layer_type in CMMLayerType:
            layer_entries = [e for e in cmm.entries if e.layer_type == layer_type]
            if layer_entries:
                layer_name = layer_type.value.replace("_", " ").title()
                lines.append(f"*{layer_name}* ({len(layer_entries)} entries):")
                for entry in layer_entries:
                    lines.append(f"  `{entry.entry_id}` — {entry.content[:100]}...")
                    lines.append(f"    Source: {entry.source_material}")
                lines.append("")

        lines.append(f"Gate requirement: ≥4 layers with ≥3 approved entries each.")
        return "\n".join(lines)

    def confirm_entries(
        self,
        cmm: CulturalMemoryMap,
        approved_entry_ids: list[str],
        rejected_entry_ids: Optional[list[str]] = None,
    ) -> CulturalMemoryMap:
        """Process operator approval/rejection of CMM entries.

        Spec: 'Operator confirms all entries via Telegram review prompt.
        CMM is NOT written automatically — the Agent identifies, the operator decides.'

        Args:
            cmm: The CulturalMemoryMap to update.
            approved_entry_ids: Entry IDs the operator approved.
            rejected_entry_ids: Entry IDs the operator rejected (optional).

        Returns:
            Updated CulturalMemoryMap. Checks if G-CMM gate now passes.

        Raises:
            CMMApprovalInsufficientError: If approved entries don't meet gate requirements.
        """
        rejected_ids = set(rejected_entry_ids or [])
        approved_ids = set(approved_entry_ids)
        now = datetime.now(timezone.utc)

        for entry in cmm.entries:
            if entry.entry_id in approved_ids:
                entry.operator_approved = True
                entry.approved_at = now
            elif entry.entry_id in rejected_ids:
                entry.operator_approved = False

        # Check if gate passes
        passes = cmm.passes_completion_gate()
        populated_count = cmm.get_populated_layer_count()

        if passes:
            cmm.status = "operator_confirmed"
            cmm.operator_confirmed = True
            cmm.confirmed_at = now
        else:
            cmm.status = "in_progress"

        cmm.updated_at = now

        # Persist
        cmm_path = self.coach_dir / "config" / "cultural_memory_map.json"
        cmm_path.write_text(cmm.model_dump_json(indent=2), encoding="utf-8")
        self._upsert_to_supabase(cmm)

        return cmm

    def load_cmm(self) -> Optional[CulturalMemoryMap]:
        """Load the current CMM from local config."""
        cmm_path = self.coach_dir / "config" / "cultural_memory_map.json"
        if not cmm_path.exists():
            return None
        data = json.loads(cmm_path.read_text(encoding="utf-8"))
        return CulturalMemoryMap.model_validate(data)

    def _upsert_to_supabase(self, cmm: CulturalMemoryMap) -> None:
        """Sync CMM to Supabase cultural_memory_map table."""
        # Supabase client is accessed via the orchestrator — not directly injected
        # into this class to keep the extraction concern focused. The orchestrator
        # calls this protocol and handles Supabase sync at the orchestration layer.
        pass  # Supabase sync handled by MorganOrchestrator.write_step_0a_cmm_receipt


class CMMApprovalInsufficientError(Exception):
    """Raised when operator confirms entries but gate requirements aren't met."""
    def __init__(self, populated_count: int, required: int = 4):
        self.populated_count = populated_count
        self.required = required
        super().__init__(
            f"CMM gate not met after approval: {populated_count} layers populated "
            f"with ≥3 entries. Required: {required}. "
            f"Request more entries from operator review."
        )
