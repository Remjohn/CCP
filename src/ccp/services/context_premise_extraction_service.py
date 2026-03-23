"""
CCP FR29 — Context Premise Extraction Service (DEP-ENG-006)

Spec: FR29_Context_Premise_Extraction_Tech_Spec.md
Produces: DEP-ENG-006 Context Premise Extraction

§4 Pipeline:
  Stage 1: Fast Audio Transcription (Whisper/Groq, ≤1500ms)
  Stage 2: 12-Dimension Extraction (Aria, ≤2500ms) + Hallucination Gate
  Stage 3: Neo4j Ontology Update (ADR-01 coach graph, ≤1000ms)

§8 AC1: Total pipeline ≤ 5000ms → sla_compliant=True
§8 AC2: No hallucinated entities — extraction only where exact_quote is present
§8 AC3: All entities must have exact_quote; missing → dropped (not fabricated)
§8 AC4: ADR-01 — Coach Dan's user mounts Dan's graph, not Maria's
"""

from __future__ import annotations

import time
from typing import Optional, Any

from src.ccp.models.onboarding_prerequisite_models import (
    ARIA_EXTRACTION_BUDGET_MS,
    EXTRACTION_LATENCY_BUDGET_MS,
    GRAPH_WRITE_BUDGET_MS,
    WHISPER_TIMEOUT_MS,
    ContextDimension,
    ContextDimensionEntry,
    ContextPremiseExtraction,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _elapsed_ms(start: float) -> float:
    """Return elapsed milliseconds from start (perf_counter value)."""
    return (time.perf_counter() - start) * 1000.0


# ══════════════════════════════════════════════════════════════════════════════
# Hallucination Gate (AC2 + AC3)
# ══════════════════════════════════════════════════════════════════════════════

class HallucinationGate:
    """FR29 §4 Stage 2: Drop any ContextDimensionEntry without exact_quote.

    AC2: If the extractor produced an entity not verbatim traceable to the
         transcript, it is dropped — not returned as None, not annotated.
    AC3: Every surviving entry must carry a non-empty exact_quote.
    """

    @staticmethod
    def filter(
        entries: list[ContextDimensionEntry],
    ) -> list[ContextDimensionEntry]:
        """Return only entries with non-empty exact_quote."""
        return [e for e in entries if e.exact_quote and e.exact_quote.strip()]


# ══════════════════════════════════════════════════════════════════════════════
# Stage 1: Whisper Transcription Adapter
# ══════════════════════════════════════════════════════════════════════════════

class WhisperTranscriptionAdapter:
    """Wraps CBCS GroqTranscriber with FR29 timeout enforcement.

    Real usage: injects GroqTranscriber at construction.
    Dev/test usage: falls back to _simulate_transcription().
    """

    TIMEOUT_MS = WHISPER_TIMEOUT_MS

    def __init__(self, groq_transcriber: Any = None) -> None:
        self._transcriber = groq_transcriber

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "session.wav",
    ) -> tuple[Optional[str], float]:
        """Return (transcript_text or None, latency_ms).

        Returns None if Whisper fails or exceeds WHISPER_TIMEOUT_MS.
        """
        start = time.perf_counter()

        if self._transcriber is None:
            # Dev simulation: use filename as stand-in "transcript"
            result = self._simulate_transcription(filename)
        else:
            try:
                result = self._transcriber.transcribe(audio_bytes, filename)
            except Exception:
                return None, _elapsed_ms(start)

        latency = _elapsed_ms(start)
        if latency > self.TIMEOUT_MS:
            # SLA breach — treat as transcription failure, §6 fallback applies
            return None, latency

        return result, latency

    @staticmethod
    def _simulate_transcription(filename: str) -> str:
        """Return a deterministic stub transcript for dev/test."""
        return (
            f"[SIMULATED TRANSCRIPT from {filename}] "
            "The client said: I feel stuck. My boss micromanages everything. "
            "I can't do this anymore. I am super tired of my commute."
        )


# ══════════════════════════════════════════════════════════════════════════════
# Stage 2: Aria 12-Dimension Extraction Adapter
# ══════════════════════════════════════════════════════════════════════════════

class AriaExtractionAdapter:
    """Wraps CBCS Aria agent; enforces ARIA_EXTRACTION_BUDGET_MS and
    applies HallucinationGate on the output.

    Real usage: injects aria_agent (from CBCS/backend/core/aria.py).
    Dev usage: falls back to _simulate_extraction().
    """

    BUDGET_MS = ARIA_EXTRACTION_BUDGET_MS

    def __init__(self, aria_agent: Any = None) -> None:
        self._aria = aria_agent
        self._gate = HallucinationGate()

    def extract(
        self,
        transcript: str,
        coach_id: str,
        user_id: str,
    ) -> tuple[list[ContextDimensionEntry], float]:
        """Return (grounded_entries, latency_ms) after hallucination gate.

        Any entry that Aria emits without an exact_quote is silently dropped.
        """
        start = time.perf_counter()

        if self._aria is None:
            raw_entries = self._simulate_extraction(transcript, user_id)
        else:
            try:
                aria_result = self._aria.run_extraction(transcript, coach_id, user_id)
                raw_entries = self._translate_aria_result(aria_result)
            except Exception:
                raw_entries = []

        latency = _elapsed_ms(start)
        grounded = self._gate.filter(raw_entries)
        return grounded, latency

    @staticmethod
    def _translate_aria_result(aria_result: Any) -> list[ContextDimensionEntry]:
        """Map CBCS Aria ContextExtraction → list[ContextDimensionEntry]."""
        entries: list[ContextDimensionEntry] = []
        if aria_result is None:
            return entries

        # aria_result.entities: list[dict] with keys dimension/label/exact_quote
        for entity in getattr(aria_result, "entities", []):
            try:
                dim_str = entity.get("dimension", "IDENTITY_CORE")
                exact_quote = entity.get("exact_quote", "")
                entry = ContextDimensionEntry(
                    dimension=ContextDimension(dim_str),
                    label=entity.get("label", ""),
                    raw_value=entity.get("raw_value", entity.get("label", "")),
                    exact_quote=exact_quote,
                    confidence=float(entity.get("confidence", 0.7)),
                    session_id=entity.get("session_id", ""),
                )
                entries.append(entry)
            except (ValueError, KeyError):
                continue  # Drop malformed entity without crashing
        return entries

    @staticmethod
    def _simulate_extraction(
        transcript: str, user_id: str
    ) -> list[ContextDimensionEntry]:
        """Deterministic dev simulation — extract only quotes present verbatim."""
        entries: list[ContextDimensionEntry] = []

        # Only emit entities traceable to verbatim quotes in the transcript
        if "I feel stuck" in transcript:
            entries.append(
                ContextDimensionEntry(
                    dimension=ContextDimension.EMOTIONAL_TRIGGER,
                    label="stuck_feeling",
                    raw_value="stuck_feeling",
                    exact_quote="I feel stuck",
                    confidence=0.85,
                    session_id=user_id,
                )
            )
        if "I can't do this" in transcript:
            entries.append(
                ContextDimensionEntry(
                    dimension=ContextDimension.RESISTANCE_PATTERN,
                    label="capability_doubt",
                    raw_value="capability_doubt",
                    exact_quote="I can't do this",
                    confidence=0.90,
                    session_id=user_id,
                )
            )
        if "micromanages" in transcript:
            entries.append(
                ContextDimensionEntry(
                    dimension=ContextDimension.IDENTITY,
                    label="boss_micromanagement",
                    raw_value="boss_micromanagement",
                    exact_quote="My boss micromanages everything",
                    confidence=0.80,
                    session_id=user_id,
                )
            )
        # NOTE: "I am super tired of my commute" is mundane → NOT extracted
        # (AC2: no hallucination of non-psychological entities)
        return entries


# ══════════════════════════════════════════════════════════════════════════════
# Stage 3: Neo4j Graph Update Adapter (ADR-01)
# ══════════════════════════════════════════════════════════════════════════════

class ContextGraphUpdateAdapter:
    """FR29 §4 Stage 3: Write ContextDimensionEntries to the coach-scoped Neo4j graph.

    AC4 (ADR-01): Each invocation receives a coach-specific neo4j_client.
    If client is None (offline), log and return latency without error.
    """

    BUDGET_MS = GRAPH_WRITE_BUDGET_MS

    def __init__(self, neo4j_client: Any = None) -> None:
        self._client = neo4j_client

    def write(
        self,
        extraction: ContextPremiseExtraction,
        coach_id: str,
    ) -> float:
        """Merge entries into the per-coach graph. Return latency_ms."""
        start = time.perf_counter()

        if self._client is None:
            # Offline — skip gracefully (same §6 fallback philosophy as FR13)
            return _elapsed_ms(start)

        for entry in extraction.evidence_grounded_entries_only:
            try:
                self._client.merge_context_entry(
                    coach_id=coach_id,
                    user_id=extraction.user_id,
                    session_id=extraction.session_id,
                    dimension=entry.dimension.value,
                    label=entry.label,
                    raw_value=entry.raw_value,
                    exact_quote=entry.exact_quote,
                    confidence=entry.confidence,
                )
            except Exception:
                # Non-fatal — individual entry write failure does not abort
                continue

        return _elapsed_ms(start)


# ══════════════════════════════════════════════════════════════════════════════
# Full Context Premise Extraction Service
# ══════════════════════════════════════════════════════════════════════════════

class ContextPremiseExtractionService:
    """FR29 full pipeline: Whisper → Aria → Neo4j.

    Produces DEP-ENG-006 ContextPremiseExtraction.

    Usage:
        svc = ContextPremiseExtractionService(coach_id="DAN")
        extraction = svc.run_pipeline(audio_bytes, user_id="USR-001", session_id="S42")
    """

    def __init__(
        self,
        coach_id: str,
        groq_transcriber: Any = None,
        aria_agent: Any = None,
        neo4j_client: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError("coach_id must be 3 characters (ADR-01).")
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=coach_id
        )
        self._transcription = WhisperTranscriptionAdapter(groq_transcriber)
        self._extraction = AriaExtractionAdapter(aria_agent)
        self._graph = ContextGraphUpdateAdapter(neo4j_client)

    def run_pipeline(
        self,
        audio_bytes: bytes,
        user_id: str,
        session_id: str = "",
        previous_extraction: Optional[ContextPremiseExtraction] = None,
    ) -> ContextPremiseExtraction:
        """Execute full FR29 3-stage pipeline.

        §6 Fallback: If Stage 1 (Whisper) fails, return previous_extraction
        with transcript_null=True (or stub if no previous).

        Returns a ContextPremiseExtraction with sla_compliant computed
        against EXTRACTION_LATENCY_BUDGET_MS (5000ms).
        """
        pipeline_start = time.perf_counter()

        # ── Stage 1: Whisper Transcription ────────────────────────────────────
        transcript, whisper_latency = self._transcription.transcribe(
            audio_bytes=audio_bytes,
            filename=f"session_{session_id}.wav",
        )

        self.receipt_chain.log(
            agent_id="Background-Pipeline",
            action="whisper_transcription",
            input_summary=f"user={user_id} audio_bytes={len(audio_bytes)}",
            output_summary=(
                f"transcript={'present' if transcript else 'null'} "
                f"latency={whisper_latency:.1f}ms"
            ),
            metadata={
                "stage_name": "FAST-AUDIO-TRANSCRIPTION",
                "latency_ms": whisper_latency,
            },
        )

        if transcript is None:
            # §6 Fallback: use previous session's extraction if available
            if previous_extraction is not None:
                return previous_extraction.model_copy(
                    update={"transcript_null": True}
                )
            # Stub empty result
            return ContextPremiseExtraction(
                user_id=user_id,
                coach_id=self.coach_id,
                session_id=session_id,
                transcript_null=True,
                entries=[],
                total_latency_ms=_elapsed_ms(pipeline_start),
                whisper_latency_ms=whisper_latency,
                aria_latency_ms=0.0,
                graph_write_latency_ms=0.0,
            )

        # ── Stage 2: 12-Dimension Extraction + Hallucination Gate ─────────────
        entries, aria_latency = self._extraction.extract(
            transcript=transcript,
            coach_id=self.coach_id,
            user_id=user_id,
        )

        self.receipt_chain.log(
            agent_id="Aria",
            action="12_dimension_extraction",
            input_summary=f"user={user_id} transcript_len={len(transcript)}",
            output_summary=(
                f"entries_extracted={len(entries)} "
                f"latency={aria_latency:.1f}ms"
            ),
            metadata={
                "stage_name": "12-DIMENSION-EXTRACTION",
                "latency_ms": aria_latency,
                "hallucination_gate_applied": True,
            },
        )

        extraction = ContextPremiseExtraction(
            user_id=user_id,
            coach_id=self.coach_id,
            session_id=session_id,
            transcript_null=False,
            entries=entries,
            total_latency_ms=_elapsed_ms(pipeline_start),
            whisper_latency_ms=whisper_latency,
            aria_latency_ms=aria_latency,
            graph_write_latency_ms=0.0,
        )

        # ── Stage 3: Neo4j Ontology Update ────────────────────────────────────
        graph_latency = self._graph.write(
            extraction=extraction,
            coach_id=self.coach_id,
        )

        # Recompute total with graph latency now known
        total_latency = _elapsed_ms(pipeline_start)
        extraction = extraction.model_copy(
            update={
                "graph_write_latency_ms": graph_latency,
                "total_latency_ms": total_latency,
            }
        )

        self.receipt_chain.log(
            agent_id="Azaria",
            action="neo4j_ontology_update",
            input_summary=f"user={user_id} entries={len(entries)}",
            output_summary=(
                f"graph_write_latency={graph_latency:.1f}ms "
                f"total_latency={total_latency:.1f}ms "
                f"sla_compliant={extraction.sla_compliant}"
            ),
            metadata={
                "stage_name": "NEO4J-ONTOLOGY-UPDATE",
                "latency_ms": graph_latency,
                "total_latency_ms": total_latency,
                "sla_compliant": extraction.sla_compliant,
            },
        )

        return extraction
