"""
CCP FR3 Corpus Assembler — Unit 2
Loads all validated Thought Units from FR2 extraction_rounds into a unified corpus.

Spec reference: FR3 Tech Spec §Step 1 — Corpus Assembly
Agent: Valeriane (Client Soul Extractor)

Steps:
1. Load all extraction_rounds from coach_soul.json
2. Concatenate into unified extraction corpus
3. Tag each unit with session_id and unit_type
4. Deduplicate (unique text)
5. Verify ≥3,000 unique authenticated words

Gate: Minimum 3,000 unique authenticated words (not total, not with
duplicates collapsed). If below threshold → halt, request more Sacred Audio.
"""

import hashlib
import json
from pathlib import Path
from typing import Optional

from src.ccp.models.voice_dna_models import (
    MINIMUM_CORPUS_WORDS,
    CorpusUnit,
    ExtractionCorpus,
)


class CorpusAssemblyError(Exception):
    """Raised when corpus assembly fails."""
    pass


class InsufficientCorpusError(Exception):
    """Raised when corpus has fewer than 3,000 unique authenticated words.
    Spec §Step 1 Gate: 'halt, request more Sacred Audio.'"""
    pass


class CorpusAssembler:
    """Assembles the extraction corpus from FR2 Sacred Audio sessions.

    Spec §Step 1: 'Load all validated Thought_Units from DEP-ENG-019
    (all sessions to date). Concatenate into a single extraction corpus.
    Tag each unit with session_id and unit_type.'
    """

    def __init__(self, coach_id: str, coach_acronym: str, coach_dir: Path):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir

    def assemble(self) -> ExtractionCorpus:
        """Execute Step 1: Corpus Assembly.

        Returns:
            ExtractionCorpus with all validated Thought Units.

        Raises:
            CorpusAssemblyError: If coach_soul.json is missing or malformed.
            InsufficientCorpusError: If unique word count < 3,000.
        """
        # Load coach_soul.json
        soul_path = self.coach_dir / "config" / "coach_soul.json"
        if not soul_path.exists():
            raise CorpusAssemblyError(
                f"coach_soul.json not found at {soul_path}. "
                "FR2 Sacred Audio pipeline must complete before FR3 can start."
            )

        soul_data = json.loads(soul_path.read_text(encoding="utf-8"))

        # Check prerequisite gate: authenticated_word_count ≥ 3000
        readiness = soul_data.get("extraction_readiness", {})
        authenticated_count = readiness.get("authenticated_word_count", 0)
        if authenticated_count < MINIMUM_CORPUS_WORDS:
            raise InsufficientCorpusError(
                f"Authenticated word count ({authenticated_count}) is below the "
                f"minimum of {MINIMUM_CORPUS_WORDS}. More Sacred Audio sessions "
                "are required before Voice DNA extraction can begin."
            )

        # Load extraction_rounds
        extraction_rounds = soul_data.get("extraction_rounds", [])
        if not extraction_rounds:
            raise CorpusAssemblyError(
                "No extraction_rounds found in coach_soul.json. "
                "FR2 Sacred Audio pipeline must produce at least one extraction round."
            )

        # Build corpus units from all rounds
        corpus = ExtractionCorpus(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )

        seen_texts: set[str] = set()

        for round_data in extraction_rounds:
            session_id = round_data.get("session_id", "unknown")
            units = round_data.get("units", [])

            for unit_data in units:
                text = unit_data.get("text", "").strip()

                # Skip empty or duplicate texts (deduplication)
                if not text:
                    continue
                text_hash = hashlib.sha256(text.encode()).hexdigest()
                if text_hash in seen_texts:
                    continue
                seen_texts.add(text_hash)

                # Only include AUTHENTIC units
                auth_score = unit_data.get("authenticity_score", {})
                if auth_score.get("status", "AUTHENTIC") != "AUTHENTIC":
                    continue

                corpus.units.append(CorpusUnit(
                    unit_id=unit_data.get("unit_id", f"CU-{len(corpus.units)}"),
                    session_id=session_id,
                    text=text,
                    word_count=unit_data.get("word_count", len(text.split())),
                    unit_type="sacred_audio",
                ))

        # Compute stats
        corpus.compute_stats()

        # Gate: ≥3,000 unique authenticated words post-dedup
        if not corpus.passes_word_count_gate():
            raise InsufficientCorpusError(
                f"After deduplication, corpus has {corpus.unique_words} unique words. "
                f"Minimum required: {MINIMUM_CORPUS_WORDS}. "
                "More Sacred Audio sessions are required."
            )

        return corpus

    def check_prerequisite_gate(self) -> tuple[bool, int]:
        """Check the prerequisite gate without assembling.

        Spec: 'coach_soul.json → extraction_readiness.authenticated_word_count ≥ 3000'

        Returns:
            (passes, authenticated_word_count)
        """
        soul_path = self.coach_dir / "config" / "coach_soul.json"
        if not soul_path.exists():
            return False, 0

        soul_data = json.loads(soul_path.read_text(encoding="utf-8"))
        readiness = soul_data.get("extraction_readiness", {})
        count = readiness.get("authenticated_word_count", 0)
        return count >= MINIMUM_CORPUS_WORDS, count
